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

   FOURTH OCCURRENCE, 2026-08-21, AND THE FIRST CAUGHT BY AN ARMED RUN — `RL_BUILD_LOCK_FILE`.
   `selftest.Sandbox.env()` set it to keep its sandboxes off the shared lock, and the self-test never
   arms, so it never fired there; it fired on the first seat that followed the isolation recipe and
   then ARMED. R24 dress rehearsal §3.3, RUN D, on the real invocation:

       staged_apply.ConfigPolicyError: the board build must use the accepted release policy…
         - UNKNOWN inherited valuation flag RL_BUILD_LOCK_FILE='…' (not in the release config manifest)

   A message about VALUATION FLAGS, for what is a lock path. REPAIRED, NOT ALLOW-LISTED: the lock
   tooling's own flags are now `BUILD_LOCK` / `BUILD_LOCK_FILE` / `BUILD_LOCK_FD` /
   `BUILD_LOCK_TIMEOUT` in `tools/build_lock.sh` and `txn.Ctx.acquire_lock`, and the legacy names are
   HALTED rather than ignored in both — an isolation flag that stops being read is a sandbox
   silently contending for the shared lock. Adding the name to `config_manifest.INFRA_ALLOW` was the
   available alternative and was refused: it would have taught the config policy to expect a tooling
   variable inside the engine's own namespace, which is the habit that produced all four burns.
   `RL_BUILD_LOCK_HELD` is the ONE survivor of the class and it is REPORTED, NOT FIXED: it is the
   reentrancy token `build_lock.sh` exports and three separate places already pop before any engine
   child (`txn.child_env`, `_build_child`, `ui/tools/gen_v0_sidecar`), so it cannot reach an armed
   build today — but it is the same defect and it should be renamed by the seat that next opens
   those four files.

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
    F('engine/rl_after/rl_model_data.json',
      '(nothing, in a lever landing) — `land round` (a score application) and `land edit` '
      '(steps.store_edit, THE EDIT VERB 2026-08-24, a surgical owner-worded field edit)',
      'the store. A lever landing must leave it byte-unmoved; 2b moves it and inherits this entry, '
      'and so does the edit verb — whose store_edit step needed NO new carrier entry precisely '
      'because this one has been captured since the first draft, so an abort can put an in-flight '
      'edit back byte-exact'),

    # ---- the sheet pin declaration: PLAN_v6 3a took these OUT of the engine -----------------------
    F('data/sheet_pins.json',
      '(nothing, in a lever landing) — SOLE WRITER: `land round` (steps.sheet), PLAN_v6 2b, '
      '2026-08-21; the amended R23 runbook manual path is the documented fallback until the '
      'owner\'s stand-down word (2a.4)',
      'the ONE pin declaration for the owner injury/sitter sheet (md5 + row count + injured=Y count) '
      'that ORDER 41 and ORDER 42 both read. Same argument as the store entry above: a lever landing '
      'must leave it byte-unmoved, and capturing it turns "the pins did not move" from a claim into a '
      'measured fact at abort time. 2b, which DOES move it in a sheet-carrying round, inherits the '
      'entry rather than registering a second one'),

    # ---- the generated state file: PLAN_v6 3c ----------------------------------------------------
    F('docs/STATE.md', 'steps.state (tools/landing/state.py, the SOLE writer)',
      'THE GENERATED STATE FILE. It is a carrier for the same reason the board is: a landing writes '
      'it, so an abort must be able to put it back byte-exact. It is also the one carrier whose '
      'content is a pure function of the others — which is why `acceptance::state_file` can '
      'regenerate it and compare, and why a hand edit is a red rather than a merge conflict'),

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
    F('ui/data/movers.js',
      'steps.ui writer 4 (ui/tools/rebuild_movers_derived.py) + round_movers (2b) / column consumers',
      'the movers bundle: its DERIVED blocks (points, values, model_changes) are rebuilt in the SAME '
      'transaction as the lineage append they derive from — supervisor ruling on F-10, 2026-08-21; '
      'the per-round reports are frozen era history and are carried through byte-verbatim'),
    F('ui/data/movers_transition.js',
      'steps.ui writer 3 (ui/tools/generate_movers_transition.py) + round_movers (2b)',
      'the movers transition bundle: the lineage record\'s mirror, projected in the SAME '
      'transaction that appends to the record — supervisor ruling on F-9, 2026-08-21'),
    F('ui/data/ownership.js',
      'steps.ui writer 5 (ui/tools/ingest_inputs.py --mirror-only) + ownership_store_apply (#283)',
      'THE OWNERSHIP MIRROR — the fifth UI bundle, and the same class F-9 and F-10 closed one '
      'carrier at a time. It mirrors the store\'s `affl_team` and is PINNED to the board + store it '
      'was generated from; `MD.ownership.pin()` REFUSES a mirror whose pin does not match the loaded '
      'app, so a landing that moves either identity and does not rewrite this file does not ship a '
      'stale club — it ships a DISABLED live ownership lane, silently. Measured on 2026-08-21: the '
      'tree stood on board b3e8da99 / store b745002e (R23) while the shipped mirror still carried '
      'a05fe951 / cc02567f (R22), because the R23 advance moved the store and nothing regenerated '
      'the mirror. ui/tests/ownership_sidecar.test.js was 22/35 for exactly that reason. Two writers, '
      'as with the movers bundles: the ownership store-apply transaction (#283) writes it when the '
      'OWNER moves a club, and the lander writes it when a LANDING moves the pin — same projector, '
      'same law, no conflict'),
    F('ui/data/club_valuation.js',
      'steps.ui writer 6 (ui/tools/ingest_inputs.py --clubs-only) + ownership_store_apply (#283, T8)',
      'THE PICKS BUNDLE — the SIXTH UI bundle, and the same class F-9, F-10 and the ownership mirror '
      'closed one carrier at a time. It carries the owner\'s PICK LOCATIONS and each held pick\'s '
      'price off the engine\'s canonical curve, and it is stamped with the board + store it was '
      'generated from. Measured on 2026-08-21 (register v827): the tree stood on board b3e8da99 / '
      'store b745002e (R23) while the shipped bundle carried a05fe951 / cc02567f (R22) — and unlike '
      'the ownership mirror it had NO reader-side guard, so the pocket and club pages showed '
      'R22-board pick VALUES with nothing refusing and nothing flagged. Owner, the same night: "It is '
      'essential that the UI displays the correct player locations and pick locations." Both halves '
      'landed in v827: `MD.clubTotals.pin()` now refuses a bundle whose stamp is not the loaded '
      'app\'s, and this entry names the writer that keeps it from ever needing to. IT COULD NOT BE A '
      'CARRIER BEFORE THAT ACT: its stamp carried a wall-clock `generated` field, so no restore could '
      'be proved byte-exact and no drift guard could be an equality; dropping that field is what made '
      'the entry possible. TWO WRITERS, exactly as the ownership mirror has: the #283 store-apply '
      'transaction writes it (its target T8) when the OWNER moves a club, and the lander writes it '
      'when a LANDING moves the board or the store'),

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

#: THE ROUND LANDER'S EXTRA CARRIERS (PLAN_v6 2b). This tuple is ADDED to `LEVER_CARRIERS`; it is not
#: a second set, and that is the S7 law in one line — the round lander and the lever lander share the
#: enumeration, the snapshot, the restore and the scope check, and differ only by these entries.
#:
#: EVERY ENTRY IS A PATH THE PROVEN R23 HAND-WALK ACTUALLY MOVED, read off the commit table in
#: `docs/evidence/r23_advance_2026-08-20/FINAL_STATE.md` §1 (commits 2, 4 and 5) rather than guessed
#: at. Anything that landing wrote and this set omitted would be a file the abort ladder could not put
#: back — which is the only way this tuple can be wrong, so it is enumerated against the record.
ROUND_EXTRA_CARRIERS = (
    # ---- the owner's inputs of record ------------------------------------------------------------
    G('scores/*.csv', 'the owner (couriered, byte-unmodified) — staged by steps.scores',
      'the round score file of record. The lander NEVER edits it: it is placed, hashed, asserted '
      'against the act spec\'s declared md5/sha256, and committed byte-unmodified. It is a carrier '
      'because a landing that stages one and aborts must not leave it behind half-staged'),
    F('docs/owner_annotations/SITTER_2026_v1.csv',
      'the owner (re-cut on his word) — staged and committed by steps.sheet',
      'THE PINNED OWNER INPUT the ORDER 41 / ORDER 42 guards read. A round advance increments every '
      'listed player\'s games_2026, so an injured=Y row that played desynchronises the sheet and '
      'halts the board regen INSIDE the transaction (runbook §4 H2). The re-cut is the owner\'s; the '
      'lander measures it, pins it, and refuses a re-cut whose measured facts are not the disclosed '
      'ones'),
    F('engine/rl_after/ingestion/catchup_identity_overrides.json',
      'the seat, on the owner\'s verbatim word — asserted (never authored) by steps.scores',
      'the identity-override record. An owner ruling on a name lives HERE, never in the score file '
      '— the R22 Bailey ruling and the R23 WBD binding are both entries in this file'),

    # ---- what the staged round transaction writes -------------------------------------------------
    F('data/season_state.json', 'staged_apply (season_state writer) — the round clock',
      'the season clock: as_of_round and the calendar fraction. It moves ONLY at an advance'),
    F('engine/rl_after/ingestion/applied_rounds_ledger.json', 'round_apply (the dedup ledger)',
      'the (stable_id|season|round) triples that make a re-sent feed impossible to double-count'),
    F('engine/rl_after/ingestion/finalization_state.json', 'round_finalize',
      'the finalization state machine\'s current state'),
    F('engine/rl_after/ingestion/finalization_journal.jsonl', 'round_finalize (append-only journal)',
      'the five-line journal shape a clean round writes; the R20 contrast (two INCOMPLETEs and three '
      'force:true retries) is what a bad one looks like'),
    G('engine/rl_after/ingestion/movers/*', 'round_finalize / round_movers',
      'the round movers reports (movers_R<N>.json/.csv) — CREATED, not merely edited, so the glob '
      'is load-bearing exactly as the sibling repin\'s fixtures are'),
    G('engine/rl_after/ingestion/.weekly_txn/**', 'staged_apply (its own transaction dir)',
      'the weekly staged-transaction records; tracked (R15…R23 all are). An aborted landing must not '
      'leave a half-open txn behind'),

    # ---- the weekly fixture bumps -----------------------------------------------------------------
    F('engine/rl_after/ingestion/test_movers_transition.py', 'the advance (weekly round expectation)',
      'the py movers suite carries the round it expects and the future-append fixture; both are '
      'bumped every week by the advance (R22 bumped 21->22, R23 bumped 22->23)'),
    F('ui/tests/movers.test.js', 'the advance (weekly round expectation)',
      'the js movers suite, same weekly bump'),

    # ---- the day-0 standing reference -------------------------------------------------------------
    F('docs/evidence/final_candidate_2026-08-19/DAY0_CP.json',
      'steps.day0 — REGENERATED AT THE ADVANCE, never mid-round (register v810 item 1)',
      'the standing day-0 print reference. It goes stale at a round clock advance and its natural '
      'home for regeneration is the advance itself; it is a carrier so that an activated re-base '
      'which then aborts puts the standing reference back byte-exact. THE EMITTER IS CARRIED, NOT '
      'ACT-PINNED: tools/landing/day0_emit.py (steps.DAY0_GENERATOR) regenerates it from the tree\'s '
      'own board and store — every emitter before it read a named scratch directory and hard-'
      'asserted named movers, and none of them could run for the next round (R24 rehearsal §5)'),
)

#: THE ROUND-LANDING CARRIER SET = the lever set PLUS the round extras. One enumeration, two acts.
ROUND_CARRIERS = LEVER_CARRIERS + ROUND_EXTRA_CARRIERS

#: THE EDIT CARRIER SET (`land edit`, THE EDIT VERB, 2026-08-24) — the LEVER SET PLUS EXACTLY ONE
#: ENTRY, and both halves of that sentence were measured rather than designed.
#:
#: THE STORE NEEDED NO NEW ENTRY. `engine/rl_after/rl_model_data.json` has been in `LEVER_CARRIERS`
#: since the library's first draft, captured precisely so an abort could PROVE it byte-unmoved. The
#: same entry that made "the store did not move" a measured fact for a lever landing makes "the store
#: moved and was put back" a measured fact for an aborted edit.
#:
#: THE SEASON CLOCK DID, and the self-test found it on this step's first run: `release_contract.py
#: check` refuses a tree whose `data/season_state.json` names a store that is not the live one
#: ("exposure_pace was derived from a STALE store"), so `steps.store_edit` re-derives the clock's
#: provenance stamp from the edited store — and a file a landing writes must be a file its abort can
#: put back. The entry is TAKEN FROM `ROUND_EXTRA_CARRIERS` rather than written again: one
#: enumeration, three acts.
SEASON_STATE_CARRIER = tuple(c for c in ROUND_EXTRA_CARRIERS if c.pattern == 'data/season_state.json')
EDIT_CARRIERS = LEVER_CARRIERS + SEASON_STATE_CARRIER


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
