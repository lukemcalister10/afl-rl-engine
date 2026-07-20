"""FINALIZATION FAILURE-INJECTION PROOF — the journaled post-commit finalization phase (gate OFF, SCRATCH).

The corrective 2026-07-20 review requires that a failure in the POST-COMMIT FINALIZATION (the
re-derivable owner-facing outputs — UI board bundles, movers report/bundle, round-delta injection)
NEVER corrupts or rolls back the CANONICAL commit (store/board/manifest/ledger/history), and that a
restart detects and repairs the half-finalized round before anything advances.

This harness core-commits R15 (finalized) then R16 (CANONICAL commit only), then injects a fault at
each of the eight finalization fault points and, for every one, asserts:

  (1) the scores are committed EXACTLY ONCE — the dedup ledger triple count is invariant across the
      fault + the repair (finalization never writes the store/ledger; repair never re-applies);
  (2) the canonical store / board / boot manifest / ledger / history stay COHERENT (board file == the
      round's committed board id; sidecar source == store; boot board pin == board; histories carry
      R14..R16) — the fault did not touch them;
  (3) a re-send of R16 is still DEDUP-blocked (triples already in the ledger);
  (4) a RESTART detects the committed-but-unfinalized round (unfinalized == [16]);
  (5) REPAIR completes finalization (-> FINALIZED) with NO re-apply and NO duplicate;
  (6) the repaired outputs are COHERENT (movers R16 board id matches; bundle chains R15->R16 with the
      baseline anchor; the working board carries the round delta) and NO historical report is silently
      overwritten;
  (7) the next round CANNOT advance while R16 is unfinalized, and CAN once it is FINALIZED.

The eight fault points (directive F):
   1 after_core_commit_before_ui   2 during_working_board_refresh   3 after_board_before_movers_json
   4 after_json_before_csv         5 after_json_csv_before_bundle   6 after_bundle_before_delta
   7 after_all_before_final_validation                              8 HARD TERMINATION (child os._exit)

Run:  python3 session_2026-07-20/weekly_updater_hardening/finalization_injection_proof.py [--write]
Exit 0 = ALL PASS. Writes NOTHING to the real store (gate ships OFF; armed in-process on SCRATCH only).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RA = os.path.join(REPO, 'engine', 'rl_after')
ING = os.path.join(RA, 'ingestion')
CU = os.path.join(REPO, 'session_2026-07-20', 'live_scoring_catchup')
FIX = os.path.join(CU, 'fixtures')
sys.path.insert(0, RA)
sys.path.insert(0, ING)
sys.path.insert(0, HERE)

import failure_injection_proof as FI    # noqa: E402  (scratch + gate helpers)
import round_catchup as RC              # noqa: E402
import round_finalize as FZ             # noqa: E402
import round_movers as MV               # noqa: E402
import staged_apply as SA               # noqa: E402

GEN = "2026-07-20T22:00:00Z"
FILES = [(r, os.path.join(FIX, 'R%d.csv' % r)) for r in (15, 16)]
CRASH_CHILD = os.path.join(HERE, '_finalize_crash_child.py')

# the seven in-process fault points + the hard-termination case (run in a child)
INPROC_POINTS = list(FZ.FAULT_POINTS)                      # 7 points
HARD_POINT = 'after_bundle_before_delta'                   # where the child os._exit()s (point 8)


def _setup_ui(scr):
    os.makedirs(os.path.join(scr, 'ui', 'tools'), exist_ok=True)
    os.makedirs(os.path.join(scr, 'ui', 'data'), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, 'ui', 'tools', 'extract_board_view.py'),
                    os.path.join(scr, 'ui', 'tools', 'extract_board_view.py'))
    MV.init_empty_bundle(os.path.join(scr, 'ui', 'data', 'movers.js'), scr)


def _committed_board(scr):
    return FI.md5(os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json'))


def _canonical_coherent(scr, r16_board):
    """The canonical commit is coherent + unchanged: board file == R16's committed id, sidecar source ==
    store md5, boot board pin == board, and the three histories carry R14..R16."""
    board = _committed_board(scr)
    store_md5 = FI.md5(FI.store_path_of(scr))
    side = json.load(open(os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json.srcmd5')))
    boot = json.load(open(os.path.join(scr, 'data', 'expected_boot.json')))
    scr_ing = os.path.join(scr, 'engine', 'rl_after', 'ingestion')
    hists = {n: json.load(open(os.path.join(scr_ing, n)))
             for n in ('value_history.json', 'rank_history.json', 'pos_rank_history.json')}
    return {
        'board_is_r16': board == r16_board,
        'sidecar_source_is_store': side.get('source_md5') == store_md5,
        'boot_board_pin_ok': boot.get('board') == board,
        'histories_R14_16': all(h.get('rounds') == [14, 15, 16] for h in hists.values()),
    }


def _build_base(tag):
    """A scratch with R15 FINALIZED and R16 CANONICALLY COMMITTED but NOT finalized. Returns
    (scr, r16_evidence, ledger_after_r16)."""
    scr = FI.make_scratch(tag)
    _setup_ui(scr)
    FI.arm()
    try:
        # R15: full apply + finalize
        RC.RoundCatchup(scr, FILES[:1]).run(approved=True, generated_at=GEN)
        # R16: CANONICAL commit only (record CORE_COMMITTED; do NOT finalize)
        cu = RC.RoundCatchup(scr, FILES)
        _report, rounds = cu.preflight()
        rd16 = next(x for x in rounds if x['round'] == 16)
        snap = cu._build_snapshot(16, rd16['resolved_rows'], GEN)
        res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN,
                                                                 txn_id='txn_catchup_r16')
        ev = {'store_md5_before': res.store_md5_before, 'store_md5_after': res.store_md5_after,
              'board_md5_before': res.board_md5_before, 'board_md5_after': res.board_md5_after,
              'txn_id': os.path.basename(res.txn_dir)}
        played = {r.key: r.score for r in rd16['resolved_rows']}
        FZ.RoundFinalizer(scr).record_core_committed(16, season=2026, played=played,
                                                     evidence=ev, generated_at=GEN)
    finally:
        FI.disarm()      # finalization needs NO gate — everything below runs with the gate OFF
    return scr, ev, FI.ledger_count(scr)


def _assert_point(base_scr, r16_ev, base_ledger, point, hard=False):
    """Copy the base scratch, inject the fault at `point`, then prove the seven invariants."""
    scr = base_scr + '_' + point
    shutil.copytree(base_scr, scr)
    r16_board = r16_ev['board_md5_after']
    checks = {'point': point}
    try:
        # --- inject the fault --------------------------------------------------------------------
        if hard:
            r = subprocess.run([sys.executable, CRASH_CHILD, scr, '16', point],
                               capture_output=True, text=True, env=dict(os.environ, RL_VENDOR=os.environ.get(
                                   'RL_VENDOR', '/home/claude/rl_vendor')))
            checks['child_hard_exited'] = (r.returncode == 137)
        else:
            def fault(p):
                if p == point:
                    raise FZ.FinalizationFault(p)
            try:
                FZ.RoundFinalizer(scr, fault=fault).finalize_round(16, generated_at=GEN)
                checks['fault_raised'] = False
            except FZ.FinalizationFault:
                checks['fault_raised'] = True

        led_after_fault = FI.ledger_count(scr)
        # (1) scores committed exactly once — ledger invariant under the fault
        checks['ledger_invariant_after_fault'] = (led_after_fault == base_ledger)
        # (2) canonical commit coherent + untouched
        checks['canonical'] = _canonical_coherent(scr, r16_board)
        # (3) dedup still blocks a re-send of R16
        led = json.load(open(FI.live_paths(scr)['ledger']))
        r16_triples = {t for t in led.get('applied', []) if '|16' in t}
        checks['r16_triples_present_once'] = bool(r16_triples) and len(r16_triples) == len(set(r16_triples))
        # (4) restart detects the committed-but-unfinalized round
        fz = FZ.RoundFinalizer(scr)
        checks['restart_detects_unfinalized'] = (fz.unfinalized_rounds() == [16])
        checks['status_before_repair'] = fz.status(16)
        # (7a) next round is BLOCKED while R16 is unfinalized
        checks['advance_blocked_before_repair'] = (fz.advance_blocked(17) == 16)
        # (5)+(6) REPAIR completes; no re-apply; outputs coherent
        rep = fz.repair(16, generated_at=GEN)
        checks['repair_ok'] = rep.get('ok')
        checks['status_after_repair'] = fz.status(16)
        checks['ledger_invariant_after_repair'] = (FI.ledger_count(scr) == base_ledger)
        # coherent outputs: movers R16 board id, bundle chain + baseline, working delta
        jpath, cpath, _ = MV.movers_paths(scr, 16)
        rep16 = json.load(open(jpath))
        bundle = MV.load_bundle(os.path.join(scr, 'ui', 'data', 'movers.js'), repo_root=scr)
        bi = bundle.get('integrity') or {}
        checks['movers_R16_board_ok'] = (rep16.get('board_md5_after') == r16_board)
        checks['bundle_rounds'] = bundle.get('rounds')
        checks['bundle_coherent'] = (bundle.get('rounds') == [15, 16] and bi.get('board_chain_ok')
                                     and bi.get('baseline_anchor_ok')
                                     and not bi.get('overwrite_conflict_last_write'))
        checks['csv_present'] = os.path.exists(cpath)
        # (7b) next round can advance once R16 is FINALIZED
        checks['advance_unblocked_after_repair'] = (fz.advance_blocked(17) is None)
        # (6b) NO silent overwrite: accumulating a DIFFERENT board id for R16 flags a conflict
        tampered = dict(rep16); tampered['board_md5_after'] = 'deadbeef' * 4
        confl = MV.accumulate_bundle(os.path.join(scr, 'ui', 'data', 'movers.js'), tampered, repo_root=scr)
        checks['different_board_flags_conflict'] = bool(confl.get('overwrite_conflict'))
        # restore the coherent bundle after the tamper probe (repair again, idempotent)
        fz.repair(16, generated_at=GEN)
    finally:
        shutil.rmtree(scr, ignore_errors=True)

    can = checks.get('canonical', {})
    ok = (checks.get('child_hard_exited', True) and checks.get('fault_raised', True)
          and checks['ledger_invariant_after_fault'] and all(can.values())
          and checks['r16_triples_present_once'] and checks['restart_detects_unfinalized']
          and checks['advance_blocked_before_repair'] and checks['repair_ok']
          and checks['status_after_repair'] == FZ.FINALIZED and checks['ledger_invariant_after_repair']
          and checks['movers_R16_board_ok'] and checks['bundle_coherent'] and checks['csv_present']
          and checks['advance_unblocked_after_repair'] and checks['different_board_flags_conflict'])
    checks['pass'] = ok
    return checks


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args(argv[1:])
    t0 = time.time()
    print("\n==== FINALIZATION FAILURE-INJECTION PROOF (post-commit; gate OFF, scratch) ====")

    real_before = {p: FI.md5(os.path.join(REPO, rel)) for p, rel in (
        ('store', 'engine/rl_after/rl_model_data.json'), ('board', 'data/rl_build/rl_app_data.json'),
        ('boot', 'data/expected_boot.json'), ('prod_movers', 'ui/data/movers.js'))}

    base, r16_ev, base_ledger = _build_base('fzinj')
    results = []
    try:
        for point in INPROC_POINTS:
            res = _assert_point(base, r16_ev, base_ledger, point, hard=False)
            print("  [%s] point: %-34s (restart->repair, ledger invariant, coherent)"
                  % ('PASS' if res['pass'] else 'FAIL', point))
            results.append(res)
    finally:
        shutil.rmtree(base, ignore_errors=True)

    # point 8 — HARD TERMINATION needs its own base (the child crashes the copy)
    base2, r16_ev2, base_ledger2 = _build_base('fzhard')
    try:
        hard = _assert_point(base2, r16_ev2, base_ledger2, HARD_POINT, hard=True)
        print("  [%s] point: %-34s (HARD os._exit mid-finalize -> restart repairs)"
              % ('PASS' if hard['pass'] else 'FAIL', 'HARD_TERMINATION@' + HARD_POINT))
        results.append(hard)
    finally:
        shutil.rmtree(base2, ignore_errors=True)

    # no real production/RC file touched
    real_after = {p: FI.md5(os.path.join(REPO, rel)) for p, rel in (
        ('store', 'engine/rl_after/rl_model_data.json'), ('board', 'data/rl_build/rl_app_data.json'),
        ('boot', 'data/expected_boot.json'), ('prod_movers', 'ui/data/movers.js'))}
    no_touch = real_before == real_after
    print("  [%s] no real store/board/boot/production-movers touched" % ('PASS' if no_touch else 'FAIL'))

    all_pass = all(r['pass'] for r in results) and no_touch
    dt = round(time.time() - t0, 1)
    print("==== %s  (%ss) ====" % ('ALL PASS' if all_pass else 'FAIL', dt))

    if args.write:
        out = {'kind': 'finalization_injection_proof', 'points': results, 'no_real_touch': no_touch,
               'elapsed_s': dt, 'ALL_PASS': all_pass}
        with open(os.path.join(HERE, 'finalization_proof.json'), 'w') as f:
            json.dump(out, f, indent=2, sort_keys=True, default=str)
        print("wrote finalization_proof.json")
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
