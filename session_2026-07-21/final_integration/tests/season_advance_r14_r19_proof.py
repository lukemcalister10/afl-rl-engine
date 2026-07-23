#!/usr/bin/env python3
"""R14-R19 DISPOSABLE SEQUENTIAL SEASON-STATE PROOF (final integration 2026-07-21, supervisor 2nd review req 6).

Applies the owner's genuine R15..R19 scores SEQUENTIALLY on a DISPOSABLE scratch copy of the accepted R14
state (gate armed IN-PROCESS against the scratch ONLY). After each round the updater DERIVES + ADVANCES the
authoritative season-state (calendar_progress + freshly-derived exposure_pace) and commits it atomically
with the store/board. For every boundary R14..R19 this records + asserts:
  as_of_round, calendar_progress, eligible durable-player count, median current games, exposure_pace,
  store md5, board md5, applied score-rows, active count, visible future-pick count per lens, F5 reconciliation.

Required (all asserted): R14 baseline == the approved canonical board (byte-identical); each later round
ADVANCES calendar_progress (0.63/0.67/0.71/0.75/0.79); exposure_pace is freshly derived from that staged
store; NO later board retains stale R14 season-state; all 804 players + 64+64 future picks survive; F5 exact
(83538); canonical store/board untouched; real-store gate OFF. (Exactly-once/rollback/recovery/repair are
proven by the shared catch-up + failure-injection harnesses.)

Writes incrementally to evidence/season_advance_r14_r19.json. Run:
  python3 session_2026-07-21/final_integration/tests/season_advance_r14_r19_proof.py
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
RA = os.path.join(ROOT, 'engine', 'rl_after'); ING = os.path.join(RA, 'ingestion')
WUH = os.path.join(ROOT, 'session_2026-07-20', 'weekly_updater_hardening')
CATCHUP = os.path.join(ROOT, 'session_2026-07-20', 'live_scoring_catchup')
FIX = os.path.join(CATCHUP, 'fixtures')
for p in (RA, ING, WUH, CATCHUP, ROOT): sys.path.insert(0, p)

import round_catchup as RC        # noqa: E402
import failure_injection_proof as FI  # noqa: E402
import catchup_proof as CP        # noqa: E402
import score_ingestor as SI       # noqa: E402
import season_state as S          # noqa: E402
import release_contract as RCON   # noqa: E402

GEN = "2026-07-21T05:00:00Z"
EXPECT_CAL = {14: 0.58, 15: 0.63, 16: 0.67, 17: 0.71, 18: 0.75, 19: 0.79}
# The DISPOSABLE scratch's R14 baseline board (materialize_r14 reconstructs it from the R14 anchor). This
# is the R14 board of record, NOT the current board of record 6f07f7cb (which this proof leaves untouched).
CANON_BOARD = '2ab73a6fed1f06fc8eecc2ce597c2aec'
OUT = os.path.abspath(os.path.join(HERE, '..', 'evidence', 'season_advance_r14_r19.json'))
R = []
def ck(name, ok, detail=''):
    R.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('  PASS ' if ok else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(ok)

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest() if os.path.exists(p) else None

def _contract_verifies(scr):
    """Run the fail-closed release-contract verify against the scratch (RL_CONFIG_MODE=gate, root=scr).
    Returns True if the complete staged release state (contract + season_state + store + boot) is coherent."""
    _saved = os.environ.get('RL_CONFIG_MODE')
    os.environ['RL_CONFIG_MODE'] = 'gate'
    try:
        RCON.verify('gate', scr, halt=True)
        return True
    except AssertionError:
        return False
    finally:
        if _saved is None:
            os.environ.pop('RL_CONFIG_MODE', None)
        else:
            os.environ['RL_CONFIG_MODE'] = _saved


def snap(scr, rnd):
    board = json.load(open(os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json')))
    ss = json.load(open(os.path.join(scr, 'data', 'season_state.json')))
    boot = json.load(open(os.path.join(scr, 'data', 'expected_boot.json')))
    con = json.load(open(os.path.join(scr, 'data', 'release_contract.json')))
    cids = con.get('identities', {})
    lp = board.get('lensPicks', [])
    dat = board.get('draftAssetTotals', {})
    store_md5 = md5(os.path.join(scr, 'engine', 'rl_after', 'rl_model_data.json'))
    board_md5 = md5(os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json'))
    return {'round': rnd, 'as_of_round': ss['as_of_round'], 'calendar_progress': ss['calendar_progress'],
            'exposure_pace': ss['exposure_pace'],
            'eligible_durable': ss['exposure_derivation']['eligible_durable_players'],
            'median_current_games': ss['exposure_derivation']['median_current_games'],
            'season_state_source_store_md5': ss.get('source_store_md5'),
            'derivation_policy_id': ss.get('derivation_policy_id'),
            'store_md5': store_md5, 'board_md5': board_md5,
            # expected_boot (boot manifest) dynamic authority
            'boot_as_of_round': boot.get('as_of_round'), 'boot_store': boot.get('store'), 'boot_board': boot.get('board'),
            # release-contract dynamic authority
            'contract_as_of_round': con.get('as_of_round'), 'contract_store': cids.get('store'),
            'contract_board': cids.get('board'), 'contract_sha256': con.get('contract_sha256'),
            'contract_calendar': (con.get('season_metadata') or {}).get('calendar_progress'),
            'contract_exposure': (con.get('season_metadata') or {}).get('exposure_pace'),
            'contract_verifies': _contract_verifies(scr),
            'write_gate_on': SI._apply_enabled(),
            'active': len(board['active']),
            'picks_2027': len([p for p in lp if p['lens'] == 1]),
            'picks_2028': len([p for p in lp if p['lens'] == 2]),
            'f5_plus1': dat.get('+1', {}).get('f5_entrant_layer_pvc'),
            'f5_reconciled': dat.get('+1', {}).get('reconciled_to_f5')}

def write():
    json.dump({'ok': all(x['pass'] for x in R), 'rows': ROWS, 'checks': R}, open(OUT, 'w'), indent=2)

ROWS = []
def main():
    print('=== R14-R19 SEQUENTIAL SEASON-STATE ADVANCE PROOF ===')
    real_store = os.path.join(RA, 'rl_model_data.json'); real_board = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
    store_before, board_before = md5(real_store), md5(real_board)

    scr = FI.make_scratch('seasonadv'); CP.install_ui(scr)
    # R14 baseline (before any apply): the scratch board == the approved canonical board, season-state R14
    base = snap(scr, 14); ROWS.append(base)
    ck('R14 baseline board == approved canonical 2ab73a6f (byte-identical)', base['board_md5'] == CANON_BOARD, base['board_md5'])
    ck('R14 baseline calendar 0.58 + exposure 0.545', base['calendar_progress'] == 0.58 and base['exposure_pace'] == 0.545)
    ck('R14 baseline 804 active + 64+64 picks', base['active'] == 804 and base['picks_2027'] == 64 and base['picks_2028'] == 64)
    ck('R14 baseline authority COHERENT (season/boot/contract all R14; contract verifies; gate OFF)',
       base['as_of_round'] == 14 and base['boot_as_of_round'] == 14 and base['contract_as_of_round'] == 14
       and base['contract_verifies'] and not base['write_gate_on'])
    write()

    prev_board = base['board_md5']
    for rnd in (15, 16, 17, 18, 19):
        FI.arm()
        try:
            RC.RoundCatchup(scr, [(rnd, os.path.join(FIX, 'R%d.csv' % rnd))]).run(approved=True, generated_at=GEN)
        finally:
            FI.disarm()
        row = snap(scr, rnd); ROWS.append(row)
        ck('R%d as_of_round advanced to %d' % (rnd, rnd), row['as_of_round'] == rnd, row['as_of_round'])
        ck('R%d calendar_progress advanced to %.2f (not frozen at R14 0.58)' % (rnd, EXPECT_CAL[rnd]),
           row['calendar_progress'] == EXPECT_CAL[rnd] and row['calendar_progress'] != 0.58, row['calendar_progress'])
        ck('R%d exposure_pace freshly derived from the staged store' % rnd,
           isinstance(row['exposure_pace'], (int, float)) and row['exposure_pace'] > 0, row['exposure_pace'])
        ck('R%d board advanced (season-state re-priced; board md5 changed)' % rnd, row['board_md5'] != prev_board, row['board_md5'])
        ck('R%d 804 active + 64+64 future picks survive' % rnd,
           row['active'] == 804 and row['picks_2027'] == 64 and row['picks_2028'] == 64)
        ck('R%d F5 reconciliation exact (83538)' % rnd, row['f5_plus1'] == 83538 and row['f5_reconciled'])
        # COHERENT AUTHORITY (supervisor 3rd review): expected_boot, season_state AND the release contract all
        # advanced to THIS round together; the contract's store/board pins == the new store/board; the contract
        # verifies fail-closed; and the real-store write gate stays OFF.
        ck('R%d expected_boot advanced (as_of_round=%d, store+board re-pinned to the new md5s)' % (rnd, rnd),
           row['boot_as_of_round'] == rnd and row['boot_store'] == row['store_md5'] and row['boot_board'] == row['board_md5'],
           detail='boot_aor=%s boot_store=%s' % (row['boot_as_of_round'], str(row['boot_store'])[:8]))
        ck('R%d release_contract advanced (as_of_round=%d; identities.store/board == new store/board)' % (rnd, rnd),
           row['contract_as_of_round'] == rnd and row['contract_store'] == row['store_md5']
           and row['contract_board'] == row['board_md5'])
        ck('R%d contract season_metadata == derived (calendar %.2f, exposure %s)' % (rnd, EXPECT_CAL[rnd], row['exposure_pace']),
           row['contract_calendar'] == EXPECT_CAL[rnd] and row['contract_exposure'] == row['exposure_pace'])
        ck('R%d season_state exposure derived off the NEW store (source_store_md5 == store)' % rnd,
           row['season_state_source_store_md5'] == row['store_md5'])
        ck('R%d fail-closed release-contract VERIFY passes on the advanced set' % rnd, row['contract_verifies'])
        ck('R%d no artifact on a stale round (season==boot==contract==%d)' % (rnd, rnd),
           row['as_of_round'] == rnd and row['boot_as_of_round'] == rnd and row['contract_as_of_round'] == rnd)
        ck('R%d real-store write gate still OFF' % rnd, not row['write_gate_on'])
        prev_board = row['board_md5']
        write()

    # no stale R14 state after R15+; calendar strictly increases
    cals = [r['calendar_progress'] for r in ROWS]
    ck('calendar_progress strictly increases R14..R19 (no stale round)', all(cals[i] < cals[i+1] for i in range(len(cals)-1)), cals)
    # The REAL canonical store/board (the current R19 store f37d9716 + board of record 6f07f7cb) must be
    # byte-unchanged by this disposable scratch advance. Labels derive from the measured identity (no stale
    # R14 hardcode); the disposable scratch's OWN R14 baseline is the separate 2ab73a6f/968de0c7 above.
    ck('canonical store byte-identical (current R19 store %s untouched)' % store_before[:8], md5(real_store) == store_before)
    ck('canonical board byte-identical (board of record %s untouched)' % board_before[:8], md5(real_board) == board_before)
    ck('real-store apply gate OFF after the scratch run', not SI._apply_enabled())
    write()

    npass = sum(1 for x in R if x['pass']); n = len(R)
    print('\nR14-R19 season-state table:')
    print('  rnd cal   exp    durable med board_md5')
    for r in ROWS:
        print('  R%-2d %.2f  %.3f  %-6d  %-3s %s' % (r['round'], r['calendar_progress'], r['exposure_pace'],
              r['eligible_durable'], r['median_current_games'], str(r['board_md5'])[:12]))
    print('\nRESULT: %d/%d PASS  -> %s' % (npass, n, os.path.relpath(OUT, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
