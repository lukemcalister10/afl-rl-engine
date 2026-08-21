"""tools/landing/carriers.py — THE ENUMERATED CARRIER SET, AND THE SNAPSHOT THAT RESTORES IT.

This module is the abort ladder's foundation (PLAN_v6 2a.3): "a landing that fails mid-flight
restores every carrier to its pre-landing identity (recorded in the claims file at start), asserts
the restoration byte-exact, and reports the failed step."

THREE PROPERTIES, EACH FOR A REASON THE RECORD ALREADY PAID FOR.

1. THE SET IS ENUMERATED, NOT DISCOVERED. G1 requires that the churn of any process change be
   ENUMERATED per change; a restore that walked the whole tree would silently acquire the authority
   to revert anything, including a file the landing never touched and another seat did. Every entry
   below names WHY it is a carrier and WHICH writer of record moves it. A landing that writes a file
   outside this set is a landing whose abort cannot restore it — so `verify_scope()` refuses at the
   end of the transaction if git reports a modification outside the declared set.

2. GLOBS ARE FIRST-CLASS, BECAUSE THE SIBLING REPIN CREATES FILES. `sibling_repin` writes
   `forward_vector_<md5>.json` and `test_forward_lens_<md5>.py`, whose NAMES are keyed to the board
   id. A restore that only rewrote known paths would leave the newly created ones behind and call
   the tree restored. Restoration therefore also DELETES files that appeared inside a carrier glob
   after the snapshot, and RECREATES files that were deleted.

3. THE SNAPSHOT LIVES OUTSIDE THE REPO. A snapshot written inside the tree is a dirty working tree
   at the exact moment the tree's cleanliness is the thing being asserted, and it would be caught by
   its own scope check. Default location is a mkdtemp; `LANDING_SNAPSHOT_DIR` overrides it.

   THAT NAME HAS NO `RL_` PREFIX, AND THE FIRST DRAFT'S DID. `RL_LANDING_SNAPSHOT_DIR` cost this
   package a whole acceptance run: `config_manifest.enforce()` rejects any unknown RL_-prefixed
   variable as a divergent model override, the variable was inherited by every probe child the gate
   step spawned, and the r15 ladder proof therefore died a DIFFERENT way than its ruling records —
   which `acceptance/checks/ledger.py` correctly reported as `R15-ladder-proof-GFWD is DRIFTED` and
   red the landing. Reproduced in one line, in both directions:

       RL_LANDING_SNAPSHOT_DIR=/tmp python3 -m acceptance.runner --only ruled_red_ledger   -> FAIL
                               (unset) python3 -m acceptance.runner --only ruled_red_ledger -> PASS

   That module's own header had already written the rule down after the same burn: "A TOOL'S OWN
   FLAGS ARE NEVER RL_*." It is not a rule about flags-as-opposed-to-env-vars; it is a rule about
   THE PREFIX, in any variable this estate's tooling sets. Third occurrence, caught by the instrument
   P1 built for exactly it.

THE STORE IS IN THE SET AND A LEVER LANDING NEVER WRITES IT. That is deliberate. Capturing
`rl_model_data.json` costs one hash and turns "the store did not move" from a claim into a measured
fact at abort time — and the one landing shape that DOES move it (2b's round advance) then needs no
new carrier registration to be covered.
"""

import fnmatch
import hashlib
import json
import os
import shutil
import tempfile


class CarrierError(RuntimeError):
    """A carrier could not be captured, restored, or proved byte-exact. Always fail-closed."""


class Carrier(object):
    """One declared carrier: a file, or a glob of files a writer of record creates by name."""

    __slots__ = ('pattern', 'writer', 'why', 'is_glob')

    def __init__(self, pattern, writer, why, is_glob=False):
        self.pattern = pattern
        self.writer = writer
        self.why = why
        self.is_glob = is_glob

    def __repr__(self):
        return '<Carrier %s>' % self.pattern


F = lambda p, w, y: Carrier(p, w, y, False)                                    # noqa: E731
G = lambda p, w, y: Carrier(p, w, y, True)                                     # noqa: E731


#: THE LEVER-LANDING CARRIER SET. Every path a lever landing can write, and who writes it.
LEVER_CARRIERS = (
    # ---- the identity manifests -----------------------------------------------------------------
    F('data/expected_boot.json', 'steps.pins',
      'the accepted boot manifest — the board pin moves here first'),
    F('data/release_contract.json', 'release_contract.restamp_dynamic + steps.contract',
      'the sealed release state: identities, config_sha256, contract_sha256'),
    F('data/release_lineage.json', 'steps.lineage (the append-only transition register)',
      'the out-of-round transition register; append-only, prior entries byte-verbatim'),

    # ---- the board and its sidecars, installed as a lockstep ------------------------------------
    F('data/rl_build/rl_app_data.json', 'the build (installed by steps.pins)',
      'the published board of record'),
    F('data/rl_build/rl_app_data.json.srcmd5', 'the build',
      'the published board sidecar — own_md5 + source_md5, written BY the build'),
    F('engine/rl_after/rl_app_data.json', 'the build (installed by steps.pins)',
      'the generator-side copy; the bake precedent installs it in lockstep with the published one'),
    F('engine/rl_after/rl_app_data.json.srcmd5', 'the build',
      'the generator-side sidecar'),

    # ---- the store: never written by a lever landing, captured so abort can prove it -------------
    F('engine/rl_after/rl_model_data.json', '(nothing, in a lever landing)',
      'the store. A lever landing must leave it byte-unmoved; 2b moves it and inherits this entry'),

    # ---- the histories the out-of-round column writes --------------------------------------------
    F('engine/rl_after/ingestion/value_history.json', 'out_of_round_column.add_column',
      'value history — one point per registered column'),
    F('engine/rl_after/ingestion/rank_history.json', 'out_of_round_column.add_column',
      'rank history'),
    F('engine/rl_after/ingestion/pos_rank_history.json', 'out_of_round_column.add_column',
      'positional rank history'),

    # ---- the UI bundles: BOTH writers, the thrice-proven trap -------------------------------------
    F('ui/data/board_view_working.js', 'extract_board_view + round_movers.inject_release_contract',
      'the html app bundle carrying stamp + stamp.release'),
    F('ui/data/board_view_public.js', 'extract_board_view',
      'the public bundle'),
    F('ui/data/movers.js', 'round_movers (2b) / sibling + column consumers',
      'the movers bundle: points, model_changes, per-round reports'),
    F('ui/data/movers_transition.js',
      'steps.ui writer 3 (ui/tools/generate_movers_transition.py) + round_movers (2b)',
      'the movers transition bundle: the lineage record\'s mirror, projected in the SAME '
      'transaction that appends to the record — supervisor ruling on F-9, 2026-08-21'),

    # ---- the sibling repin's own targets ----------------------------------------------------------
    F('engine/rl_after/ingestion/sibling_repin_state.json', 'sibling_repin.reconcile',
      'the sibling provenance sidecar'),
    F('session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py', 'sibling_repin.reconcile',
      'the FV oracle the repin re-points at the new balanced board'),
    G('session_2026-07-20/fv_provenance_remediation/fixtures/*.json', 'sibling_repin.reconcile',
      'reference + forward vectors, FILENAMES KEYED TO THE BOARD ID — created, not merely edited'),
    G('session_2026-07-20/fv_provenance_remediation/test_forward_lens_*.py', 'sibling_repin.reconcile',
      'forward oracles, filenames keyed to the board id'),
    G('engine/rl_after/ingestion/.sibling_txn/**', 'sibling_repin (its own transaction dir)',
      'the repin transaction dir; an aborted landing must not leave a half-open txn behind'),
)

#: The round lander (2b) adds its carriers to this tuple rather than defining a second set.
ROUND_EXTRA_CARRIERS = ()


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def _walk_glob(root, pattern):
    """Expand a carrier glob to repo-relative paths that EXIST right now.

    `**` means "everything below this directory". Anything else is fnmatch on the basename within
    the pattern's own directory — deliberately shallow, so a glob can never quietly widen.
    """
    found = []
    if pattern.endswith('/**'):
        base = os.path.join(root, pattern[:-3])
        if os.path.isdir(base):
            for dirpath, _dirnames, filenames in os.walk(base):
                for fn in filenames:
                    found.append(os.path.relpath(os.path.join(dirpath, fn), root))
        return sorted(found)
    d, pat = os.path.split(pattern)
    base = os.path.join(root, d)
    if os.path.isdir(base):
        for fn in sorted(os.listdir(base)):
            if fnmatch.fnmatch(fn, pat) and os.path.isfile(os.path.join(base, fn)):
                found.append(os.path.join(d, fn) if d else fn)
    return sorted(found)


def expand(root, carriers=LEVER_CARRIERS):
    """-> sorted list of repo-relative paths currently matched by the carrier set."""
    out = []
    for c in carriers:
        if c.is_glob:
            out.extend(_walk_glob(root, c.pattern))
        else:
            out.append(c.pattern)
    seen, uniq = set(), []
    for p in out:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return sorted(uniq)


def scope_patterns(carriers=LEVER_CARRIERS):
    """The declared patterns, for the end-of-transaction scope assertion."""
    return tuple(c.pattern for c in carriers)


def in_scope(rel, carriers=LEVER_CARRIERS):
    """Is this repo-relative path inside the declared carrier set?"""
    for c in carriers:
        if not c.is_glob:
            if rel == c.pattern:
                return True
        elif c.pattern.endswith('/**'):
            if rel.startswith(c.pattern[:-2]):
                return True
        elif fnmatch.fnmatch(rel, c.pattern):
            return True
    return False


class Snapshot(object):
    """The restore-point: every carrier's bytes and md5, captured before the first write.

    `entries` maps repo-relative path -> md5, with None meaning THE FILE DID NOT EXIST. That
    distinction is the whole reason restore can undo a `forward_vector_<newmd5>.json` the repin
    created: absent-then-present is a change like any other, and it is reverted by deletion.
    """

    __slots__ = ('root', 'store_dir', 'entries', 'carriers', '_owned')

    def __init__(self, root, carriers=LEVER_CARRIERS, store_dir=None):
        self.root = os.path.abspath(root)
        self.carriers = carriers
        self.entries = {}
        self._owned = store_dir is None
        self.store_dir = store_dir or tempfile.mkdtemp(
            prefix='rl_landing_snap_', dir=os.environ.get('LANDING_SNAPSHOT_DIR') or None)
        if os.path.abspath(self.store_dir).startswith(self.root + os.sep):
            raise CarrierError(
                'the snapshot store %s is INSIDE the tree being landed. A restore-point that dirties '
                'the tree it protects is not a restore-point.' % self.store_dir)

    # ------------------------------------------------------------------------------------ capture
    def capture(self):
        """Read every carrier's bytes into the store. Returns self."""
        os.makedirs(self.store_dir, exist_ok=True)
        for rel in expand(self.root, self.carriers):
            src = os.path.join(self.root, rel)
            if os.path.isfile(src):
                dst = os.path.join(self.store_dir, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copyfile(src, dst)
                self.entries[rel] = _md5(src)
            else:
                self.entries[rel] = None
        with open(os.path.join(self.store_dir, '_manifest.json'), 'w', encoding='utf-8') as fh:
            json.dump({'root': self.root, 'entries': self.entries}, fh, indent=1, sort_keys=True)
        return self

    def identities(self):
        """The captured identities, for the claims file's restore-point block."""
        return dict(self.entries)

    def present(self):
        return {k: v for k, v in self.entries.items() if v is not None}

    # ------------------------------------------------------------------------------------ compare
    def current(self):
        """The carriers' identities RIGHT NOW, over the union of captured and freshly created."""
        now = {}
        for rel in set(self.entries) | set(expand(self.root, self.carriers)):
            p = os.path.join(self.root, rel)
            now[rel] = _md5(p) if os.path.isfile(p) else None
        return now

    def diff(self):
        """-> [(rel, before, after)] for every carrier whose identity is not what was captured."""
        now = self.current()
        moved = []
        for rel in sorted(set(self.entries) | set(now)):
            b, a = self.entries.get(rel), now.get(rel)
            if b != a:
                moved.append((rel, b, a))
        return moved

    # ------------------------------------------------------------------------------------ restore
    def restore(self):
        """Put every carrier back to the captured identity. Returns [(rel, action)].

        Three actions, and all three are needed: `rewrite` (the file moved), `delete` (the file did
        not exist at capture and does now), `recreate` (it existed and was removed). A restore that
        only rewrote would leave the repin's newly named forward vector standing.
        """
        actions = []
        for rel, before, after in self.diff():
            dst = os.path.join(self.root, rel)
            if before is None:
                if os.path.isfile(dst):
                    os.remove(dst)
                    actions.append((rel, 'delete'))
                continue
            src = os.path.join(self.store_dir, rel)
            if not os.path.isfile(src):
                raise CarrierError('snapshot store is missing %s — cannot restore byte-exact' % rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            actions.append((rel, 'recreate' if after is None else 'rewrite'))
        # Empty directories the repin created are swept, so `git status` reads clean.
        for c in self.carriers:
            if c.is_glob and c.pattern.endswith('/**'):
                base = os.path.join(self.root, c.pattern[:-3])
                if os.path.isdir(base):
                    for dirpath, dirnames, filenames in os.walk(base, topdown=False):
                        if not filenames and not dirnames and dirpath != base:
                            os.rmdir(dirpath)
        return actions

    def assert_restored(self):
        """THE ABORT PROOF. Every carrier byte-exact to the capture, or raise naming what is not."""
        moved = self.diff()
        if moved:
            raise CarrierError(
                'ABORT DID NOT RESTORE THE TREE. %d carrier(s) still differ from the restore point:\n'
                % len(moved)
                + '\n'.join('    %-64s %s -> %s' % (r, (b or 'ABSENT')[:12], (a or 'ABSENT')[:12])
                            for r, b, a in moved))
        return True

    def discard(self):
        if self._owned and os.path.isdir(self.store_dir):
            shutil.rmtree(self.store_dir, ignore_errors=True)
