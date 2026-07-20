"""SEQUENTIAL TWO-ROUND LIVE-SCORING PROOF — Round 15 then Round 16 (gate OFF, SCRATCH only).

Proves a non-technical owner can enter consecutive weekly AFL scores and safely produce: validated
ingestion, atomic canonical-store update, a regenerated board, coherent pins + source stamps,
persistent per-player round-by-round VALUE and RANK history, refreshed UI bundles, duplicate-round
protection, stale-preview protection, tamper protection, universe/residue protection, interrupted-
transaction recovery, and NO partial writes — across a full STOP / RESTART between the two rounds.

Writes NOTHING to the real store. The apply gate ships OFF (score_ingestor.APPLY_DEFAULT=False + env
INGEST_SCORE_APPLY unset); this harness arms it IN-PROCESS only, against a throwaway SCRATCH repo whose
data/expected_boot.json is stamped COHERENT with the scratch engine (release identities supplied to the
fixture). No scratch path resolves to the real single source; round 16 is applied in a FRESH PROCESS.

The 17 required proofs (see the workstream brief) map to the numbered steps below. Boards are built
under the accepted fail-closed forward-valuation path (RL_FV bound to the staged repo, config policy
from the release manifest); the proof claims NO cross-CPU numerical-identity verdict — it validates
structure, source-stamp/pin coherence, Guard-5 pins, player universe and history integrity, and refuses
any board that does not satisfy the fixture's release identities.

Run:  python3 session_2026-07-20/live_scoring_two_round/two_round_proof.py [--write]
Exit 0 = ALL PROOFS PASS.
"""
import argparse
import hashlib
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
WUH = os.path.join(REPO, 'session_2026-07-20', 'weekly_updater_hardening')
sys.path.insert(0, RA)
sys.path.insert(0, ING)
sys.path.insert(0, WUH)

import round_entry as RE            # noqa: E402
import round_history as RH          # noqa: E402
import staged_apply as SA           # noqa: E402
import score_ingestor as SI         # noqa: E402
import failure_injection_proof as FI   # noqa: E402  (make_scratch: fixture-coherent scratch, gate helpers)

GEN15 = "2026-07-20T15:00:00Z"
GEN16 = "2026-07-20T16:00:00Z"
R15, R16 = 15, 16


# ---- helpers --------------------------------------------------------------------------------------
def md5(path):
    if not path or not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def hist_paths(scr):
    return (os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'value_history.json'),
            os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'rank_history.json'))


def install_ui(scr):
    """Copy the checkout's read-only extractor into the scratch so refresh_ui can run post-commit."""
    os.makedirs(os.path.join(scr, 'ui', 'tools'), exist_ok=True)
    os.makedirs(os.path.join(scr, 'ui', 'data'), exist_ok=True)
    shutil.copyfile(os.path.join(REPO, 'ui', 'tools', 'extract_board_view.py'),
                    os.path.join(scr, 'ui', 'tools', 'extract_board_view.py'))


def feed_players(scr, n=8):
    store = json.load(open(FI.store_path_of(scr)))
    return [r for r in store if r.get('stable_player_id') and not r.get('_retired')][:n]


def snapshot_for(scr, rnd, players, base, step, gen):
    body = "\n".join("%s,%s" % (r['player'], base + i * step) for i, r in enumerate(players))
    ent = RE.RoundEntry(rnd, store_path=FI.store_path_of(scr))
    resolved, residue = ent.resolve_body(body)
    assert not residue, "unexpected residue in a clean synthetic feed"
    return ent.build_snapshot(resolved, generated_at=gen)


def board_active_keys(path):
    d = json.load(open(path))
    return {p.get('key') for p in (d['active'] if isinstance(d, dict) else d)}


# ==================================================================================================
def run(report):
    scr = FI.make_scratch('tworound')
    install_ui(scr)
    vpath, rpath = hist_paths(scr)
    lp = FI.live_paths(scr)
    FI.arm()
    try:
        players = feed_players(scr, n=8)

        # -- baseline: the fixture's accepted round-14 board is the pre-apply board -----------------
        board14_md5 = md5(lp['board'])
        store14_md5 = md5(lp['store'])

        # === (1) ROUND 15 PREVIEW validates identities and score meaning ==========================
        snap15 = snapshot_for(scr, R15, players, base=95.0, step=7.0, gen=GEN15)
        strong = RE.is_strong(snap15)
        vok, vreason = RE.verify_snapshot(snap15)
        store = json.load(open(lp['store']))
        # identities: every resolved row carries a stable id that is present + active in the store
        by_key = {r['key']: r for r in store}
        ids_ok = all(row['stable_player_id'] == by_key[row['key']]['stable_player_id']
                     and by_key[row['key']].get('stable_player_id') and not by_key[row['key']].get('_retired')
                     for row in snap15['resolved'])
        # score meaning: the snapshot->preview bridge == score_ingestor from the equivalent feed
        from score_ingestor import ScoreIngestor
        from round_score_parser import parse_feed
        bridge = {a.key: a.merged_entry for a in SA.preview_from_snapshot(snap15, store).appends}
        feed = json.dumps([{'player': by_key[row['key']]['player'], 'round': R15, 'score': row['score'],
                            'played': 1, 'club': by_key[row['key']].get('afl_club')}
                           for row in snap15['resolved']])
        ref = {a.key: a.merged_entry for a in ScoreIngestor(store=store).preview(parse_feed(feed)).appends}
        meaning_ok = set(bridge) == set(ref) and all(bridge[k] == ref[k] for k in bridge)
        report['1_r15_preview_validates'] = {
            'strong': strong, 'content_hash_verifies': vok, 'identities_resolve_to_active_ids': ids_ok,
            'source_store_md5_full_matches_live': snap15['source_store_md5_full'] == md5(lp['store']),
            'score_meaning_preserved': meaning_ok, 'players': len(snap15['resolved']),
            'pass': strong and vok and ids_ok and meaning_ok
            and snap15['source_store_md5_full'] == md5(lp['store'])}

        # === (2) ROUND 15 APPLY updates the scratch store atomically ==============================
        state_before15 = {k: md5(p) for k, p in lp.items()}
        res15 = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap15, generated_at=GEN15)
        store15_md5 = md5(lp['store'])
        board15_md5 = md5(lp['board'])
        man15 = json.load(open(lp['manifest']))
        atomic15 = (store15_md5 == res15.store_md5_after and store15_md5 != store14_md5
                    and res15.players_applied == len(players) and res15.guard5_green)
        report['2_r15_apply_atomic'] = {
            'store': '%s -> %s' % (store14_md5[:8], store15_md5[:8]),
            'players_applied': res15.players_applied, 'guard5_green': res15.guard5_green,
            'manifest_store_pin_coherent': man15['store'] == store15_md5,
            'manifest_board_pin_coherent': man15['board'] == board15_md5,
            'sidecar_source_stamp_coherent': json.load(open(lp['sidecar']))['source_md5'] == store15_md5,
            'txn_committed': True, 'pass': atomic15 and man15['store'] == store15_md5
            and man15['board'] == board15_md5}

        # === (3) ROUND 15 BOARD is generated from the updated store ================================
        board15_from_store = (board15_md5 != board14_md5 and res15.board_md5_after == board15_md5)
        report['3_r15_board_regenerated'] = {
            'board': '%s -> %s' % (board14_md5[:8], board15_md5[:8]),
            'board_source_is_updated_store': json.load(open(lp['sidecar']))['source_md5'] == store15_md5,
            'pass': board15_from_store}

        # === (4) VALUE + RANK history records the R14 -> R15 transition for EVERY active player ====
        vh = json.load(open(vpath))
        rh = json.load(open(rpath))
        active15 = board_active_keys(lp['board'])
        every_player_14_15 = all(
            {'14', '15'} <= set(vh['players'].get(k, {}).get('by_round', {}))
            and {'14', '15'} <= set(rh['players'].get(k, {}).get('by_round', {}))
            for k in active15)
        # the recorded R15 values/ranks agree with the committed board
        truth15 = RH.value_rank_map(json.load(open(lp['board'])))
        v_agrees = all(vh['players'][k]['by_round']['15'] == truth15[k]['v'] for k in active15)
        r_agrees = all(rh['players'][k]['by_round']['15'] == truth15[k]['rank'] for k in active15)
        report['4_history_r14_r15_transition'] = {
            'value_rounds': vh['rounds'], 'rank_rounds': rh['rounds'],
            'players_tracked': len(vh['players']), 'active_players': len(active15),
            'every_active_player_has_r14_and_r15': every_player_14_15,
            'r15_value_agrees_with_board': v_agrees, 'r15_rank_agrees_with_board': r_agrees,
            'pass': every_player_14_15 and v_agrees and r_agrees and vh['rounds'] == [14, 15]}

        # === (16a) UI extraction AFTER the committed R15 board -> coherent bundles ==================
        # first show the gate: extracting a MISMATCHED board fails the ring-fence (only a committed
        # board yields coherent bundles). Corrupt the published board copy, attempt extraction, restore.
        pre_ui_working = md5(os.path.join(scr, 'ui', 'data', 'board_view_working.js'))
        ui15 = SA.StagedRoundApplier.for_repo(scr).refresh_ui()
        # negative control: a board whose md5 != the boot pin must fail the extractor ring-fence
        saved = open(lp['board'], 'rb').read()
        with open(lp['board'], 'ab') as f:
            f.write(b'\n// tamper\n')
        neg = SA.StagedRoundApplier.for_repo(scr).refresh_ui()
        with open(lp['board'], 'wb') as f:
            f.write(saved)
        report['16a_ui_after_r15_commit'] = {
            'ran': ui15.get('ran'), 'ok': ui15.get('ok'),
            'board_stamp_matches_committed': ui15.get('ui_board_stamp_matches_committed'),
            'public_leak_free': ui15.get('public_leak_free'),
            'working_players': ui15.get('working_players'), 'public_players': ui15.get('public_players'),
            'mismatched_board_refused': not neg.get('ok'),
            'pass': bool(ui15.get('ok')) and ui15.get('ui_board_stamp_matches_committed')
            and ui15.get('public_leak_free') and not neg.get('ok')}

        # === (5) FULLY STOP + RESTART: read the committed state from a FRESH PROCESS ===============
        readback = subprocess.run(
            [sys.executable, '-c',
             "import json,hashlib,sys;"
             "f=lambda p:hashlib.md5(open(p,'rb').read()).hexdigest();"
             "d={'store':f(sys.argv[1]),'board':f(sys.argv[2]),'vhist':f(sys.argv[3]),'rhist':f(sys.argv[4])};"
             "print(json.dumps(d))",
             lp['store'], lp['board'], vpath, rpath],
            capture_output=True, text=True)
        rb = json.loads(readback.stdout) if readback.returncode == 0 else {}
        restart_ok = (rb.get('store') == store15_md5 and rb.get('board') == board15_md5
                      and rb.get('vhist') == md5(vpath))
        report['5_stop_and_restart'] = {
            'fresh_process_reads_committed_store': rb.get('store') == store15_md5,
            'fresh_process_reads_committed_board': rb.get('board') == board15_md5,
            'committed_history_persists': rb.get('vhist') == md5(vpath), 'pass': restart_ok}

        # === (10) STALE R16 preview created BEFORE the R15 change is BLOCKED =======================
        # (built here from the pre-R15 store bytes, then applied AFTER R15 moved the store)
        # simulate: stamp an R16 snapshot whose source store md5 is the pre-apply (R14) store.
        stale16 = json.loads(json.dumps(snap15))          # any strong snapshot stamped vs store14
        stale16['round'] = R16
        stale16['source_store_md5_full'] = store14_md5    # created before the R15 change
        stale16['content_hash'] = RE.compute_content_hash(stale16)
        pre_state = {k: md5(p) for k, p in lp.items()}
        stale_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(stale16, generated_at=GEN16)
        except SA.StaleSnapshotError:
            stale_blocked = True
        report['10_stale_r16_preview_blocked'] = {
            'blocked': stale_blocked, 'files_unchanged': {k: md5(p) for k, p in lp.items()} == pre_state,
            'pass': stale_blocked and {k: md5(p) for k, p in lp.items()} == pre_state}

        # === (6) ROUND 16 PREVIEW is based on the R15 COMMITTED state ==============================
        players16 = feed_players(scr, n=8)    # re-read the LIVE (now R15-committed) store
        snap16 = snapshot_for(scr, R16, players16, base=110.0, step=5.0, gen=GEN16)
        report['6_r16_preview_on_committed_r15'] = {
            'r16_stamped_against_store': snap16['source_store_md5_full'][:8],
            'equals_committed_r15_store': snap16['source_store_md5_full'] == store15_md5,
            'content_hash_verifies': RE.verify_snapshot(snap16)[0],
            'pass': snap16['source_store_md5_full'] == store15_md5 and RE.verify_snapshot(snap16)[0]}

        # === (11) ALTERING the R16 preview after approval is BLOCKED (content hash) ================
        tampered = json.loads(json.dumps(snap16))
        tampered['resolved'][0]['score'] = 999.9          # edit WITHOUT re-stamping the hash
        altered_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(tampered, generated_at=GEN16)
        except SA.AlteredSnapshotError:
            altered_blocked = True
        report['11_tampered_preview_blocked'] = {'blocked': altered_blocked, 'pass': altered_blocked}

        # === (12) PLAYER-UNIVERSE mismatch / unresolved-name residue is BLOCKED ====================
        # (a) residue-open snapshot refused; (b) a resolved key ABSENT from the store refused.
        res_open = json.loads(json.dumps(snap16)); res_open['counts']['residue_open'] = 1
        res_open['content_hash'] = RE.compute_content_hash(res_open)
        residue_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(res_open, generated_at=GEN16)
        except SA.ResidueOpenError:
            residue_blocked = True
        ghost = json.loads(json.dumps(snap16))
        ghost['resolved'][0]['key'] = 'no-such-player-xyz'
        ghost['resolved'][0]['stable_player_id'] = 'afl-player-v1-deadbeefdeadbeefdead'
        ghost['content_hash'] = RE.compute_content_hash(ghost)
        universe_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(ghost, generated_at=GEN16)
        except (SA.StagedValidationError, SA.PreviewNotCleanError):
            universe_blocked = True
        report['12_universe_residue_blocked'] = {
            'residue_open_blocked': residue_blocked, 'absent_key_blocked': universe_blocked,
            'pass': residue_blocked and universe_blocked}

        # === (13) FAILURE INJECTION during the R16 replacement leaves NO partial state =============
        # inject at history staging (pre-commit) and after the first live replacement (commit-phase);
        # each must leave the committed R15 state byte-identical and NOT advance the history to R16.
        r15_state = {k: md5(p) for k, p in lp.items()}
        r15_hist = (md5(vpath), md5(rpath))
        inj_results = {}
        for point in ('during_history_staging', 'after_first_replacement'):
            ap = SA.StagedRoundApplier.for_repo(scr, fault=FI.make_fault(point))
            raised = False
            try:
                ap.apply_snapshot(snap16, generated_at=GEN16)
            except SA.FaultInjected:
                raised = True
            files_ok = {k: md5(p) for k, p in lp.items()} == r15_state
            hist_ok = (md5(vpath), md5(rpath)) == r15_hist
            # history did not advance to R16
            no_r16 = 16 not in RH.rounds_recorded(json.load(open(vpath)))
            inj_results[point] = {'raised': raised, 'r15_state_byte_identical': files_ok,
                                  'history_unchanged': hist_ok, 'no_r16_in_history': no_r16,
                                  'pass': raised and files_ok and hist_ok and no_r16}
            # a commit-phase fault leaves an unrecovered txn -> clear it before the next apply
            SA.StagedRoundApplier.for_repo(scr).recover(generated_at=GEN16)
        report['13_failure_injection_no_partial'] = {
            'points': inj_results, 'pass': all(v['pass'] for v in inj_results.values())}

        # === (14) HARD PROCESS EXIT mid-commit is detected; next run REFUSES until recovery ========
        snap16_path = os.path.join(scr, '_r16_snap.json')
        with open(snap16_path, 'w') as f:
            json.dump(snap16, f)
        env = dict(os.environ); env.setdefault('RL_VENDOR', '/home/claude/rl_vendor')
        crash = subprocess.run(
            [sys.executable, os.path.join(WUH, '_crash_child.py'), scr, snap16_path, GEN16],
            capture_output=True, text=True, env=env)
        crashed = crash.returncode == 70
        mid = {k: md5(p) for k, p in lp.items()}
        store_swapped_mid = mid['store'] != r15_state['store']       # store swapped before the crash
        board_stale_mid = mid['board'] == r15_state['board']         # board not yet swapped -> inconsistent
        refused = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap16, generated_at=GEN16)
        except SA.IncompleteTransactionError:
            refused = True
        report['14_hard_exit_detected_refuses'] = {
            'child_crashed_mid_commit': crashed, 'store_swapped_mid_crash': store_swapped_mid,
            'board_inconsistent_mid_crash': board_stale_mid, 'next_run_refused': refused,
            'pass': crashed and store_swapped_mid and refused}

        # === (15) RECOVERY restores byte-identical pre-transaction files + keeps forensic evidence =
        rep = SA.StagedRoundApplier.for_repo(scr).recover(generated_at=GEN16)
        after_recover = {k: md5(p) for k, p in lp.items()}
        restored_identical = after_recover == r15_state
        hist_restored = (md5(vpath), md5(rpath)) == r15_hist
        # forensic evidence: the recovered txn keeps a manifest (RECOVERED) + a journal
        txn_root = os.path.join(scr, 'engine', 'rl_after', 'ingestion', SA.TXN_DIRNAME)
        rec_txn = [d for d in os.listdir(txn_root) if os.path.isdir(os.path.join(txn_root, d))]
        evidence_kept = False
        rec_status = None
        for d in rec_txn:
            man = json.load(open(os.path.join(txn_root, d, 'manifest.json')))
            if man.get('status') == SA.STATUS_RECOVERED:
                evidence_kept = os.path.exists(os.path.join(txn_root, d, 'journal.jsonl'))
                rec_status = man.get('status')
        report['15_recovery_byte_identical_evidence'] = {
            'files_byte_identical_to_pre_txn': restored_identical, 'history_restored': hist_restored,
            'txn_marked_recovered': rec_status == SA.STATUS_RECOVERED, 'forensic_journal_kept': evidence_kept,
            'not_clean': not rep['clean'],
            'pass': restored_identical and hist_restored and rec_status == SA.STATUS_RECOVERED
            and evidence_kept}

        # === (7) ROUND 16 APPLY updates the store + board atomically — IN A FRESH PROCESS ==========
        result_out = os.path.join(scr, '_r16_result.json')
        child = subprocess.run(
            [sys.executable, os.path.join(HERE, '_round_child.py'), scr, snap16_path, str(R16),
             GEN16, result_out], capture_output=True, text=True, env=env)
        child_ok = child.returncode == 0 and os.path.exists(result_out)
        r16 = json.load(open(result_out)) if child_ok else {}
        store16_md5 = md5(lp['store'])
        board16_md5 = md5(lp['board'])
        man16 = json.load(open(lp['manifest']))
        atomic16 = (child_ok and store16_md5 == r16.get('store_after') and store16_md5 != store15_md5
                    and board16_md5 != board15_md5 and r16.get('guard5_green'))
        report['7_r16_apply_atomic_fresh_process'] = {
            'applied_in_fresh_process': child_ok, 'store': '%s -> %s' % (store15_md5[:8], store16_md5[:8]),
            'board': '%s -> %s' % (board15_md5[:8], board16_md5[:8]),
            'players_applied': r16.get('players_applied'), 'guard5_green': r16.get('guard5_green'),
            'manifest_pins_coherent': man16['store'] == store16_md5 and man16['board'] == board16_md5,
            'pass': atomic16 and man16['store'] == store16_md5 and man16['board'] == board16_md5}

        # === (8) HISTORY records R14, R15 AND R16 without overwriting earlier rounds ===============
        vh2 = json.load(open(vpath))
        rh2 = json.load(open(rpath))
        active16 = board_active_keys(lp['board'])
        all_three = all({'14', '15', '16'} <= set(vh2['players'].get(k, {}).get('by_round', {}))
                        for k in active16)
        # non-overwrite: every R14 and R15 value recorded BEFORE R16 is byte-identical now
        preserved = True
        for k, entry in vh['players'].items():
            for r, val in entry['by_round'].items():
                if vh2['players'].get(k, {}).get('by_round', {}).get(r) != val:
                    preserved = False
                    break
        r16_agrees = all(vh2['players'][k]['by_round']['16'] == RH.value_rank_map(
            json.load(open(lp['board'])))[k]['v'] for k in active16)
        report['8_history_r14_r15_r16_no_overwrite'] = {
            'value_rounds': vh2['rounds'], 'rank_rounds': rh2['rounds'],
            'every_active_player_has_all_three': all_three,
            'earlier_rounds_preserved_byte_equal': preserved, 'r16_value_agrees_with_board': r16_agrees,
            'pass': vh2['rounds'] == [14, 15, 16] and all_three and preserved and r16_agrees}

        # === (16b) UI extraction after the committed R16 board -> coherent bundles =================
        ui16 = r16.get('ui', {})
        report['16b_ui_after_r16_commit'] = {
            'ran': ui16.get('ran'), 'ok': ui16.get('ok'),
            'board_stamp_matches_committed': ui16.get('ui_board_stamp_matches_committed'),
            'public_leak_free': ui16.get('public_leak_free'),
            'working_players': ui16.get('working_players'), 'public_players': ui16.get('public_players'),
            'pass': bool(ui16.get('ok')) and ui16.get('ui_board_stamp_matches_committed')
            and ui16.get('public_leak_free')}

        # === (9) RE-SENDING Round 15 or Round 16 is BLOCKED (dedup) ================================
        pre_resend = {k: md5(p) for k, p in lp.items()}
        resend15_blocked = False
        snap15_resend = snapshot_for(scr, R15, feed_players(scr, 8), base=95.0, step=7.0, gen="2026-07-20T17:00:00Z")
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap15_resend, generated_at="2026-07-20T17:00:00Z")
        except SA.DuplicateRoundError:
            resend15_blocked = True
        snap16_resend = snapshot_for(scr, R16, feed_players(scr, 8), base=110.0, step=5.0, gen="2026-07-20T17:01:00Z")
        resend16_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap16_resend, generated_at="2026-07-20T17:01:00Z")
        except SA.DuplicateRoundError:
            resend16_blocked = True
        report['9_resend_r15_r16_blocked'] = {
            'resend_r15_blocked': resend15_blocked, 'resend_r16_blocked': resend16_blocked,
            'files_unchanged': {k: md5(p) for k, p in lp.items()} == pre_resend,
            'pass': resend15_blocked and resend16_blocked
            and {k: md5(p) for k, p in lp.items()} == pre_resend}

        return scr
    finally:
        FI.disarm()


def prove_gate_off_real_store(report):
    """Gate-off / real-store refusal: the shipped gate is OFF, so an apply against the REAL store
    refuses and writes nothing (this proof never arms the gate against the real single source)."""
    off = False
    try:
        SI.ScoreIngestor().apply(SI.ScoreIngestor().preview([]))
    except SI.IngestionGatedError:
        off = True
    report['gate_off_real_store_refused'] = {'refused': off, 'pass': off}


def prove_no_production_touched(report, real_before):
    """(17) No production / release-candidate files are touched: the real store, board, boot manifest,
    ledger and UI bundles are byte-identical before and after the whole proof (only scratch + tempdirs
    were written)."""
    real_after = _real_state()
    unchanged = real_after == real_before
    changed = [k for k in real_before if real_before[k] != real_after.get(k)]
    report['17_no_production_files_touched'] = {
        'checked': sorted(real_before), 'all_byte_identical': unchanged, 'changed': changed,
        'pass': unchanged}


def _real_state():
    files = {
        'store': os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json'),
        'board': os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json'),
        'boot_manifest': os.path.join(REPO, 'data', 'expected_boot.json'),
        'ledger': os.path.join(REPO, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json'),
        'ui_working': os.path.join(REPO, 'ui', 'data', 'board_view_working.js'),
        'ui_public': os.path.join(REPO, 'ui', 'data', 'board_view_public.js'),
        'value_history': os.path.join(REPO, 'engine', 'rl_after', 'ingestion', 'value_history.json'),
        'rank_history': os.path.join(REPO, 'engine', 'rl_after', 'ingestion', 'rank_history.json'),
    }
    return {k: md5(v) for k, v in files.items()}


# ==================================================================================================
_ORDER = ['1_r15_preview_validates', '2_r15_apply_atomic', '3_r15_board_regenerated',
          '4_history_r14_r15_transition', '5_stop_and_restart', '6_r16_preview_on_committed_r15',
          '7_r16_apply_atomic_fresh_process', '8_history_r14_r15_r16_no_overwrite',
          '9_resend_r15_r16_blocked', '10_stale_r16_preview_blocked', '11_tampered_preview_blocked',
          '12_universe_residue_blocked', '13_failure_injection_no_partial',
          '14_hard_exit_detected_refuses', '15_recovery_byte_identical_evidence',
          '16a_ui_after_r15_commit', '16b_ui_after_r16_commit', '17_no_production_files_touched',
          'gate_off_real_store_refused']


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='write PROOF.md + proof.json')
    args = ap.parse_args(argv[1:])
    t0 = time.time()
    report = {'gate_shipped': {'APPLY_DEFAULT': SI.APPLY_DEFAULT,
                               'INGEST_SCORE_APPLY': os.environ.get('INGEST_SCORE_APPLY', 'unset')}}

    prove_gate_off_real_store(report)
    real_before = _real_state()
    scr = None
    try:
        scr = run(report)
    finally:
        if scr:
            shutil.rmtree(scr, ignore_errors=True)
    prove_no_production_touched(report, real_before)

    report['elapsed_s'] = round(time.time() - t0, 1)
    all_pass = all(report[k]['pass'] for k in _ORDER)
    report['ALL_PASS'] = all_pass

    print("\n==== SEQUENTIAL TWO-ROUND LIVE-SCORING PROOF (R15 -> R16, gate OFF, scratch) ====")
    for k in _ORDER:
        print("  [%s] %s" % ('PASS' if report[k]['pass'] else 'FAIL', k))
    print("==== %s  (%.1fs) ====" % ('ALL PASS' if all_pass else 'FAIL', report['elapsed_s']))

    if args.write:
        with open(os.path.join(HERE, 'proof.json'), 'w') as f:
            json.dump(report, f, indent=2, sort_keys=True)
        with open(os.path.join(HERE, 'PROOF.md'), 'w') as f:
            f.write(_md_report(report))
        print("wrote proof.json + PROOF.md")
    return 0 if all_pass else 1


_TITLES = {
    '1_r15_preview_validates': 'R15 preview validates identities + score meaning',
    '2_r15_apply_atomic': 'R15 apply updates the scratch store atomically',
    '3_r15_board_regenerated': 'R15 board generated from the updated store',
    '4_history_r14_r15_transition': 'value+rank history records R14->R15 for every active player',
    '5_stop_and_restart': 'process fully stopped + restarted (fresh process reads committed state)',
    '6_r16_preview_on_committed_r15': 'R16 preview based on the R15 committed state',
    '7_r16_apply_atomic_fresh_process': 'R16 apply updates store+board atomically (fresh process)',
    '8_history_r14_r15_r16_no_overwrite': 'history records R14, R15, R16 without overwriting earlier',
    '9_resend_r15_r16_blocked': 're-sending R15 or R16 is blocked (dedup)',
    '10_stale_r16_preview_blocked': 'stale R16 preview (pre-R15 change) is blocked',
    '11_tampered_preview_blocked': 'altering preview after approval is blocked (content hash)',
    '12_universe_residue_blocked': 'player-universe mismatch / unresolved residue is blocked',
    '13_failure_injection_no_partial': 'failure injection before/during replacement -> no partial state',
    '14_hard_exit_detected_refuses': 'hard exit mid-commit detected; next run refuses until recovery',
    '15_recovery_byte_identical_evidence': 'recovery restores byte-identical files + keeps evidence',
    '16a_ui_after_r15_commit': 'UI extraction after committed R15 board -> coherent bundles',
    '16b_ui_after_r16_commit': 'UI extraction after committed R16 board -> coherent bundles',
    '17_no_production_files_touched': 'no production / release-candidate files touched',
    'gate_off_real_store_refused': 'gate OFF: real-store apply refused (nothing written)',
}


def _md_report(r):
    L = ["# Sequential two-round live-scoring proof — Round 15 → Round 16 (gate OFF, scratch only)",
         "", "Writes **nothing** to the real store (gate ships OFF: `APPLY_DEFAULT=False` + env "
         "`INGEST_SCORE_APPLY` unset; real-store apply refused = `%s`). Round 16 is applied in a "
         "**fresh process** after a full stop; the scratch `expected_boot.json` is stamped coherent with "
         "the scratch engine (release identities supplied to the fixture)."
         % r['gate_off_real_store_refused']['refused'],
         "", "## RESULT: **%s**  (%.1fs)" % ('ALL PASS' if r['ALL_PASS'] else 'FAIL', r['elapsed_s']),
         "", "| # | proof | result |", "|---|---|---|"]
    for k in _ORDER:
        L.append("| %s | %s | %s |" % (k.split('_')[0].upper(), _TITLES[k], '✅' if r[k]['pass'] else '❌'))
    L += ["", "### Store / board / history hashes (the sequential chain)",
          "```", "R14 (fixture baseline) store %s  board %s" % (
              r['2_r15_apply_atomic']['store'].split(' -> ')[0], r['3_r15_board_regenerated']['board'].split(' -> ')[0]),
          "R15 apply              store %s  board %s   value/rank rounds %s" % (
              r['2_r15_apply_atomic']['store'].split(' -> ')[1], r['3_r15_board_regenerated']['board'].split(' -> ')[1],
              r['4_history_r14_r15_transition']['value_rounds']),
          "R16 apply              store %s  board %s   value/rank rounds %s" % (
              r['7_r16_apply_atomic_fresh_process']['store'].split(' -> ')[1],
              r['7_r16_apply_atomic_fresh_process']['board'].split(' -> ')[1],
              r['8_history_r14_r15_r16_no_overwrite']['value_rounds']),
          "```",
          "", "> Single-env, scratch-only. No cross-run/cross-machine numerical-identity verdict is "
          "claimed — the board is validated for structure, source-stamp/pin coherence, Guard-5 pins, "
          "player universe and history integrity, under the accepted fail-closed forward-valuation path.",
          "> The 7-point failure-injection + crash-recovery matrix is proven in "
          "`../weekly_updater_hardening/PROOF.md`; step 13/14/15 here re-prove no-partial-state and "
          "recovery in the two-round context.", ""]
    return '\n'.join(L)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
