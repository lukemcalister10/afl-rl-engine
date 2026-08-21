"""acceptance/checks/manifest.py — the trunk check: the widened release-manifest coherence gate.

This wraps `release_manifest_check.py` (repo root) into the verdict contract. All of the real work
is there; this file's only job is to turn 43 carrier comparisons into ONE row and the right set of
halted carriers.

The verdict logic is the blocked-once law in miniature:

    no drift                    -> PASS
    drift, all carriers ruled   -> RULED-RED   (presented fork; non-gating; carriers still halted)
    drift, any carrier unruled  -> FAIL        (nobody has seen this; it reds the run)
    a ledger entry gone stale   -> FAIL        (the known-red list has stopped being true)

In all three drift cases the carriers are halted, so downstream checks are BLOCKED either way. A
presented ruling stops a red from GATING; it does not make the tree coherent, and it must not let a
check that reads the broken carrier report a green it has not earned.
"""

import os
import sys

from acceptance import contract as C
from acceptance import known_red

_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_gate(root):
    """Import release_manifest_check.py from the tree UNDER TEST, not from this checkout.

    The runner can be pointed at another root (--root), and when it is, the gate that runs must be
    that tree's gate. Asserting tree A with tree B's instrument is how a check silently certifies
    something it never looked at.
    """
    import importlib.util
    path = os.path.join(root, 'release_manifest_check.py')
    if not os.path.exists(path):
        path = os.path.join(_ROOT, 'release_manifest_check.py')
    spec = importlib.util.spec_from_file_location('_rmc_under_test', path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules['_rmc_under_test'] = mod
    spec.loader.exec_module(mod)
    return mod


#: Every carrier this check is capable of halting. The runner reads this to prove the registry is
#: ordered so that no downstream check can run before its carrier has been adjudicated.
_GROUPS = ('expected_boot', 'release_contract', 'season_state', 'board_sidecar',
           'ui_bundle.stamp', 'ui_bundle.stamp.release', 'book_seal', 'sheet_pins')
_IDENTS = ('store', 'board', 'engine_head', 'rl_model', 'fv', 'config', 'register', 'as_of_round',
           'sheet', 'sheet_rows', 'sheet_injured_y')


def check(ctx):
    """All 11 identities agree across all 43 carrier fields in 8 files."""
    rmc = _load_gate(ctx.root)
    truth = rmc.compute_truth(ctx.root)
    rows, halted, ok = rmc.evaluate(ctx.root)
    text = rmc.render(rows, halted, truth, ctx.root)
    evidence = C.write_evidence(ctx, 'release_manifest.txt', text)

    ncarriers = len(rows)
    entries = known_red.load()

    # A ledger entry that no longer describes anything real is itself a defect — and it fails even
    # on an otherwise perfectly coherent tree, which is exactly when it most needs to be noticed.
    gone = known_red.stale(halted.keys(), entries)
    if gone:
        # One line must carry the whole truth, including the part that is good news. Reporting the
        # stale entry without also saying whether the tree is otherwise coherent would send a
        # reader hunting for a drift that may not exist.
        rest = ('; %d other carrier field(s) still drift' % sum(len(v) for v in halted.values())
                if halted else '; the tree is otherwise coherent')
        return C.Verdict(
            'release_manifest', C.FAIL, evidence,
            'STALE RULED-RED ledger entry %s — its carriers are coherent again, retire it from '
            'acceptance/ruled_red.json%s'
            % (', '.join(e['id'] for e in gone), rest),
            halted_carriers=tuple(halted))

    if ok:
        # Sealed carriers that lag are counted separately and named, never folded into "all agree".
        # A one-line reason that rounds a lag away is how a table stops being worth reading.
        nlag = sum(1 for r in rows if r[5] == 'SEALED-LAG')
        return C.Verdict(
            'release_manifest', C.PASS, evidence,
            '%d of %d carrier fields agree with computed truth across %d identities%s'
            % (ncarriers - nlag, ncarriers, len(_IDENTS),
               '; %d sealed carrier(s) lagging (reported, non-gating)' % nlag if nlag else ''))

    ruled, unruled = known_red.classify(halted.keys(), entries)
    nbad = sum(len(v) for v in halted.values())

    if unruled:
        return C.Verdict(
            'release_manifest', C.FAIL, evidence,
            '%d of %d carrier fields disagree with computed truth; UNRULED carrier(s): %s'
            % (nbad, ncarriers, ', '.join(sorted(unruled))),
            halted_carriers=tuple(halted))

    ids = sorted({e['id'] for _c, e in ruled})
    return C.Verdict(
        'release_manifest', C.RULED_RED, evidence,
        '%d of %d carrier fields drift, all covered by presented ruling(s) %s — %d carrier(s) '
        'halted, downstream BLOCKED, no seat may clear this'
        % (nbad, ncarriers, '/'.join(ids), len(halted)),
        halted_carriers=tuple(halted))


#: Declared for runner.validate_registry(). See acceptance/checks/__init__.py.
check.HALTS = tuple('%s:%s' % (g, i) for g in _GROUPS for i in _IDENTS)

#: Pure file reads and hashes against the checkout — safe on a bare runner (PLAN_v6 1a's per-push
#: host-insensitive floor). See acceptance/checks/standing.py for what the three profiles mean.
check.PROFILE = 'host-insensitive'
