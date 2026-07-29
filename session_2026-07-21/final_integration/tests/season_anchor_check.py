#!/usr/bin/env python3
"""SEASON-STATE ANCHORS — ONE executable definition, called from every site (#251 part C).

WHY THIS FILE EXISTS. The season-state assertion lived at TWO executable sites — season_progress_test.py
and an inline `python3 -c` in .github/workflows/final-integration.yml — carrying the same hand-typed R19
values. Fixing one left the other red (hazard class 2, duplicated assertion). Both sites now call in here,
so there is one definition and nothing to keep in step by hand.

TWO ANCHORS OF DIFFERENT KINDS, deliberately kept apart.

  1. THE FIXED HISTORICAL ANCHOR (R14) — unchanged, and #251 fences it explicitly.
     It derives from the EXACT R14 store bytes at the accepted authority anchor (968de0c7 @ 93bd01af), an
     immutable git blob. Its expectation (calendar 0.58, exposure 0.545) cannot go stale because its input
     cannot move. Hand-typed here, correctly: it is a historical fact.

  2. THE CURRENT-ROUND ANCHOR — this is the one that went red, and it is rebuilt.
     It used to hand-type the R19 answer: calendar 0.79, exposure 0.727, store c120cfd5. R20 was applied,
     the store legitimately moved to e3aaba77 and derives 0.83 / 0.773, and nothing re-typed the three
     numbers. Same shape as the Kako ground-truth anchor #245 round-scopes: a value a human must retype
     when the world moves.

     Following the pattern #245 lands, but for a check of a different KIND, so the shape differs where the
     kind does:

       - THE ROUND COMES FROM THE MANIFEST, never from the store being checked
         (data/expected_boot.json `as_of_round`). This is #245's rule exactly: an anchor that took its
         scope from the artifact it checks would let a store that had silently advanced also widen the
         window meant to catch it.

       - THE EXPECTATION IS THE COMMITTED STAMP, not a literal. Kako is an OWNER GROUND-TRUTH anchor — the
         human assertion is the point, so deriving it would make it check the store against itself and it
         must announce staleness instead. This is not that. This is a DERIVATION check: its job is that the
         stamped season state (data/season_state.json + the release contract's season_metadata) is what the
         live store actually derives. So it re-derives from the store and compares against the STAMP — two
         independent artifacts, moved atomically by the weekly transaction. That is why it needs no
         staleness announcement and no owner re-anchor: there is nothing hand-typed left to go stale.

     What that buys, per #251: the check survives the next round application without a human retyping a
     number (round and stamp both advance in the same commit), and a genuinely wrong derivation still reds
     — change the policy in season_state.py, move the store without re-deriving, or hand-edit a stamped
     value, and the re-derivation stops matching. Proven both directions by
     season_anchor_check_nonvacuity.py.

Run directly (`python3 season_anchor_check.py`) for PASS/FAIL + exit code, or call run() for the checks
and the derived states.
"""
import os, sys, json, hashlib, tempfile, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT)
import season_state as S  # noqa: E402

# The R14 authority anchor: an immutable historical commit. Its store bytes are md5 968de0c7 and the
# approved R14 season state derived from them is calendar 0.58 / exposure 0.545. ITEM 408 item 5.1.
R14_ANCHOR_COMMIT = '93bd01af86db00c169714652714a364bd2635764'
R14_ANCHOR_STORE_MD5 = '968de0c7'
R14_CALENDAR = 0.58
R14_EXPOSURE = 0.545


def r14_anchor_store(root=None):
    """Materialize the exact R14 store bytes (git blob at the R14 anchor) to a temp file; md5 968de0c7."""
    root = root or ROOT
    p = os.path.join(tempfile.mkdtemp(prefix='r14_store_'), 'rl_model_data.json')
    with open(p, 'wb') as f:
        f.write(subprocess.check_output(
            ['git', 'show', '%s:engine/rl_after/rl_model_data.json' % R14_ANCHOR_COMMIT], cwd=root))
    return p


def _read_json(root, *parts):
    with open(os.path.join(root, *parts)) as f:
        return json.load(f)


def check_r14_anchor(root=None):
    """The FIXED historical anchor. Returns (checks, derived_state)."""
    root = root or ROOT
    st = S.derive(14, r14_anchor_store(root), season_year=2026, season_total_rounds=24)
    d = st['exposure_derivation']
    checks = [
        ('R14 anchor: calendar_progress == %.2f (derived from the fixed historical store)' % R14_CALENDAR,
         st['calendar_progress'] == R14_CALENDAR, st['calendar_progress']),
        ('R14 anchor: exposure_pace == %.3f from the exact anchor store %s @ %s (305 durable, median 12, 12/22)'
         % (R14_EXPOSURE, R14_ANCHOR_STORE_MD5, R14_ANCHOR_COMMIT[:8]),
         st['exposure_pace'] == R14_EXPOSURE and d['eligible_durable_players'] == 305
         and d['median_current_games'] == 12
         and str(st.get('source_store_md5', '')).startswith(R14_ANCHOR_STORE_MD5),
         '%s %s' % (st['exposure_pace'], st.get('source_store_md5', '')[:8])),
    ]
    return checks, st


def check_current_round(root=None):
    """The CURRENT-ROUND anchor: re-derive from the live store at the MANIFEST's round and require the
    committed stamp to be exactly that. No current-round value is typed here. Returns (checks, state)."""
    root = root or ROOT
    boot = _read_json(root, 'data', 'expected_boot.json')
    stamp = _read_json(root, 'data', 'season_state.json')
    contract = _read_json(root, 'data', 'release_contract.json')
    sm = contract.get('season_metadata') or {}
    store = os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')

    rnd = boot.get('as_of_round')                 # the round comes from the MANIFEST, not the store
    total = int(stamp.get('season_total_rounds') or S.SEASON_TOTAL_ROUNDS_DEFAULT)
    year = int(stamp.get('season_year') or 2026)
    checks = []

    if rnd is None:
        checks.append(('current round: data/expected_boot.json carries as_of_round (the anchor scope)',
                       False, 'absent — the anchor has no round to derive against'))
        return checks, None
    rnd = int(rnd)

    # Every artifact must agree on WHICH round this is, before any value is compared. A stamp for a
    # different round than the manifest is the failure the old hand-typed constant was standing in for.
    checks.append(('current round: manifest, season_state and contract all stamp round %d' % rnd,
                   int(stamp.get('as_of_round', -1)) == rnd and int(sm.get('as_of_round', -1)) == rnd,
                   'expected_boot=%s season_state=%s contract=%s'
                   % (rnd, stamp.get('as_of_round'), sm.get('as_of_round'))))

    derived = S.derive(rnd, store, season_year=year, season_total_rounds=total)
    live_md5 = hashlib.md5(open(store, 'rb').read()).hexdigest()

    checks.append(('current round R%d: re-deriving from the live store reproduces the stamped '
                   'calendar_progress' % rnd,
                   derived['calendar_progress'] == stamp.get('calendar_progress'),
                   'derived %s vs stamped %s' % (derived['calendar_progress'], stamp.get('calendar_progress'))))
    checks.append(('current round R%d: re-deriving from the live store reproduces the stamped '
                   'exposure_pace' % rnd,
                   derived['exposure_pace'] == stamp.get('exposure_pace'),
                   'derived %s vs stamped %s' % (derived['exposure_pace'], stamp.get('exposure_pace'))))
    checks.append(('current round R%d: the stamp names the LIVE store (%s), so the derivation is not from a '
                   'stale one' % (rnd, live_md5[:8]),
                   stamp.get('source_store_md5') == live_md5,
                   'stamped %s vs live %s' % (str(stamp.get('source_store_md5'))[:8], live_md5[:8])))
    checks.append(('current round R%d: the release contract carries the same derived pair' % rnd,
                   sm.get('calendar_progress') == derived['calendar_progress']
                   and sm.get('exposure_pace') == derived['exposure_pace'],
                   'contract %s/%s' % (sm.get('calendar_progress'), sm.get('exposure_pace'))))
    checks.append(('current round R%d: the derivation POLICY is the one the artifacts were stamped under'
                   % rnd,
                   stamp.get('derivation_policy_id') == S.policy_id()
                   and sm.get('derivation_policy_id') == S.policy_id(),
                   S.policy_id()[:12]))
    # The two are distinct concepts and must not be silently collapsed into one dial.
    checks.append(('current round R%d: calendar_progress and exposure_pace are DISTINCT concepts, separately '
                   'derived' % rnd,
                   derived['calendar_progress'] != derived['exposure_pace'],
                   '%s vs %s' % (derived['calendar_progress'], derived['exposure_pace'])))
    return checks, derived


def run(root=None):
    """Both anchors. Returns (checks, {'r14': state, 'current': state})."""
    c1, r14 = check_r14_anchor(root)
    c2, cur = check_current_round(root)
    return c1 + c2, {'r14': r14, 'current': cur}


def main():
    print('=== SEASON-STATE ANCHORS (fixed R14 historical + current round from the manifest) ===')
    checks, states = run()
    for name, ok, detail in checks:
        print(('  PASS ' if ok else '  FAIL ') + name + ((' -- %s' % detail) if detail != '' else ''))
    npass = sum(1 for _, ok, _ in checks if ok)
    cur = states.get('current') or {}
    print('\nRESULT: %d/%d PASS  (R14 anchor 0.58/0.545 fixed; current round R%s -> calendar %s / exposure %s,'
          ' both re-derived not typed)'
          % (npass, len(checks), cur.get('as_of_round'), cur.get('calendar_progress'), cur.get('exposure_pace')))
    return 0 if npass == len(checks) else 1


if __name__ == '__main__':
    sys.exit(main())
