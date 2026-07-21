"""FAILURE-INJECTION + ACCEPTANCE PROOF — weekly updater safe-local hardening (gate OFF, SCRATCH only).

Writes NOTHING to the real store. The apply gate ships OFF (score_ingestor.APPLY_DEFAULT=False + env
INGEST_SCORE_APPLY unset); this harness arms it IN-PROCESS only, against throwaway SCRATCH repos. No
scratch path resolves to the real single source.

It proves the staged transaction (engine/rl_after/ingestion/staged_apply.py) is safe under failure:

  FAILURE INJECTION (7 points). For each, a fault is injected mid-apply and we assert the live scratch
  files are byte-identical to their pre-run bytes (rolled back or never touched), no dedup entry
  remains, no partial board remains, and the transaction evidence explains the failure:
    1 before_store_staging   2 during_board_generation   3 after_board_generation
    4 during_manifest_staging 5 during_ledger_staging
    6 after_first_replacement (commit-phase -> rollback)  7 after_subsequent_replacement (rollback)

  CRASH RECOVERY. A child process HARD-EXITS after the first live replacement (skipping rollback);
  the next apply REFUSES (incomplete transaction) and `recover` restores every original — the store
  is never left with a stale board/manifest/ledger.

  ACCEPTANCE.
    - clean apply succeeds (store+board move, Guard 5 GREEN on the staged build, ledger records)
    - immediate re-send is BLOCKED (dedup)
    - a stale snapshot is BLOCKED (store md5 moved)
    - an altered snapshot hash is BLOCKED (content hash)
    - an invalid round is BLOCKED (season bound)
    - unresolved residue cannot apply (residue-open guard)
    - snapshot -> preview conversion PRESERVES score meaning (equivalent to score_ingestor)

Run:  python3 session_2026-07-20/weekly_updater_hardening/failure_injection_proof.py [--write]
Exit 0 = ALL PROOFS PASS.
"""
import os, sys, json, shutil, tempfile, hashlib, argparse, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RA = os.path.join(REPO, 'engine', 'rl_after')
ING = os.path.join(RA, 'ingestion')
sys.path.insert(0, RA)
sys.path.insert(0, ING)

import round_entry as RE                                        # noqa: E402
import staged_apply as SA                                       # noqa: E402
import score_ingestor as SI                                     # noqa: E402
import scratch_fixture as SF                                    # noqa: E402
from score_ingestor import ScoreIngestor                        # noqa: E402
from round_score_parser import parse_feed                       # noqa: E402

INJECTION_POINTS = [
    'before_store_staging', 'during_board_generation', 'after_board_generation',
    'during_manifest_staging', 'during_ledger_staging',
    'after_first_replacement', 'after_subsequent_replacement',
]
GEN = "2026-07-20T00:00:00Z"


# ---- helpers --------------------------------------------------------------------------------
def md5(path):
    if not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def make_scratch(tag):
    """A throwaway SCRATCH REPO ROOT (never the real repo): everything the board build + Guard 5 need."""
    dst = tempfile.mkdtemp(prefix='wkfi_%s_' % tag,
                           dir=os.environ.get('WK_SCRATCH_BASE') or tempfile.gettempdir())
    shutil.copytree(RA, os.path.join(dst, 'engine', 'rl_after'))
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'),
                    os.path.join(dst, 'engine', 'forward_valuation'))
    ws = os.path.join(dst, 'engine', 'rl_after')
    # fv_provenance.py + boot_guard.py ride along: df5066a's rl_export.py imports them at build time
    # (fail-closed provenance preamble), and the applier's own workspace copy re-copies them from this
    # scratch root — so the scratch must carry them at the root and beside rl_export.
    for f in ('config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py', 'boot_guard.py', 'season_state.py'):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(ws, f))
    for f in ('boot_guard.py', 'config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py', 'season_state.py'):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(dst, f))
    shutil.copytree(os.path.join(REPO, 'data'), os.path.join(dst, 'data'))
    shutil.copytree(os.path.join(REPO, 'session_2026-07-18', 'legf5'),
                    os.path.join(dst, 'session_2026-07-18', 'legf5'))
    SF.stamp_release_identities(dst)     # coherent engine identities for the fixture's Guard 5
    return dst


def store_path_of(scr):
    return os.path.join(scr, 'engine', 'rl_after', 'rl_model_data.json')


def live_paths(scr):
    return {
        'store':   store_path_of(scr),
        'board':   os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json'),
        'sidecar': os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json.srcmd5'),
        'manifest': os.path.join(scr, 'data', 'expected_boot.json'),
        'ledger':  os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json'),
    }


def snapshot_bytes_state(scr):
    return {k: md5(p) for k, p in live_paths(scr).items()}


def build_snapshot(scr, n_players=5, rnd=15, base=90.0, step=7.0, store_path=None):
    """Build a stamped snapshot for `n_players` real active players against the scratch store."""
    sp = store_path or store_path_of(scr)
    store = json.load(open(sp))
    active = [r for r in store if r.get('stable_player_id') and not r.get('_retired')][:n_players]
    body = "\n".join("%s,%s" % (r['player'], base + i * step) for i, r in enumerate(active))
    ent = RE.RoundEntry(rnd, store_path=sp)
    resolved, residue = ent.resolve_body(body)
    assert not residue, "unexpected residue in a clean synthetic feed"
    return ent.build_snapshot(resolved, generated_at=GEN), active


def arm():
    SI.APPLY_DEFAULT = True
    os.environ['INGEST_SCORE_APPLY'] = 'failure-injection-proof-token'
    os.environ.setdefault('RL_VENDOR', '/home/claude/rl_vendor')


def disarm():
    SI.APPLY_DEFAULT = False
    os.environ.pop('INGEST_SCORE_APPLY', None)


def make_fault(target):
    def fault(phase):
        if phase == target:
            raise SA.FaultInjected(phase)
    return fault


def ledger_count(scr):
    return len(SA.load_ledger(live_paths(scr)['ledger']).get('applied', []))


def read_last_txn(scr):
    txn_root = os.path.join(scr, 'engine', 'rl_after', 'ingestion', SA.TXN_DIRNAME)
    if not os.path.isdir(txn_root):
        return None, None
    dirs = [os.path.join(txn_root, d) for d in os.listdir(txn_root)
            if os.path.isdir(os.path.join(txn_root, d))]
    if not dirs:
        return None, None
    d = sorted(dirs, key=lambda p: os.path.getmtime(p))[-1]
    man = json.load(open(os.path.join(d, 'manifest.json')))
    journal = [json.loads(l) for l in open(os.path.join(d, 'journal.jsonl')) if l.strip()]
    return man, journal


# ============================================================================================
# FAILURE INJECTION
# ============================================================================================
def prove_injection(target):
    scr = make_scratch('inj')
    try:
        snap, _ = build_snapshot(scr)
        before = snapshot_bytes_state(scr)
        led_before = ledger_count(scr)
        ap = SA.StagedRoundApplier.for_repo(scr, fault=make_fault(target))
        raised = None
        try:
            ap.apply_snapshot(snap, generated_at=GEN)
        except SA.FaultInjected as e:
            raised = str(e)
        after = snapshot_bytes_state(scr)
        man, journal = read_last_txn(scr)
        commit_phase = target in ('after_first_replacement', 'after_subsequent_replacement')
        expected_status = SA.STATUS_ROLLED_BACK if commit_phase else SA.STATUS_ABORTED_PRECOMMIT
        files_restored = (after == before)
        no_dedup = (ledger_count(scr) == led_before == 0)
        no_partial_board = (after['board'] == before['board'])
        evidence_ok = bool(man) and man.get('status') == expected_status and \
            man.get('failure') and target in (man['failure'].get('error') or '')
        journal_has_failure = any(e.get('event') == 'FAILURE' for e in (journal or []))
        rolled_back_evt = (not commit_phase) or any(e.get('event') == 'ROLLBACK_OK' for e in (journal or []))
        ok = all([raised is not None, files_restored, no_dedup, no_partial_board,
                  evidence_ok, journal_has_failure, rolled_back_evt])
        return {
            'point': target, 'fault_raised': raised is not None,
            'files_byte_identical_after': files_restored,
            'no_dedup_entry': no_dedup, 'no_partial_board': no_partial_board,
            'txn_status': man.get('status') if man else None, 'expected_status': expected_status,
            'txn_evidence_explains': evidence_ok, 'rollback_journaled': rolled_back_evt,
            'pass': ok,
        }
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================================
# CRASH RECOVERY
# ============================================================================================
def prove_crash_recovery():
    scr = make_scratch('crash')
    try:
        snap, _ = build_snapshot(scr)
        before = snapshot_bytes_state(scr)
        snap_path = os.path.join(scr, '_crash_snap.json')
        with open(snap_path, 'w') as f:
            json.dump(snap, f)
        # child hard-exits after the first live replacement (skips rollback) -> incomplete txn
        env = dict(os.environ); env.setdefault('RL_VENDOR', '/home/claude/rl_vendor')
        r = subprocess.run([sys.executable, os.path.join(HERE, '_crash_child.py'), scr, snap_path, GEN],
                           capture_output=True, text=True, env=env)
        crashed = (r.returncode == 70)
        mid = snapshot_bytes_state(scr)
        store_changed_mid = (mid['store'] != before['store'])          # store swapped before the crash
        board_stale_mid = (mid['board'] == before['board'])            # board NOT yet swapped -> inconsistent
        man_mid, _ = read_last_txn(scr)
        incomplete_detected = bool(man_mid) and man_mid.get('status') not in SA._TERMINAL
        # a fresh apply must REFUSE while the txn is unrecovered
        refused = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        except SA.IncompleteTransactionError:
            refused = True
        except Exception:
            refused = False
        # recover -> roll back to originals
        rep = SA.StagedRoundApplier.for_repo(scr).recover(generated_at=GEN)
        after = snapshot_bytes_state(scr)
        man_after, journal_after = read_last_txn(scr)
        fully_restored = (after == before)
        no_dedup = (ledger_count(scr) == 0)
        recovered_terminal = bool(man_after) and man_after.get('status') == SA.STATUS_RECOVERED
        ok = all([crashed, store_changed_mid, board_stale_mid, incomplete_detected, refused,
                  fully_restored, no_dedup, recovered_terminal, not rep['clean']])
        return {
            'child_crashed_after_first_replacement': crashed,
            'mid_crash_store_changed': store_changed_mid,
            'mid_crash_board_stale_inconsistent': board_stale_mid,
            'incomplete_detected': incomplete_detected,
            'next_apply_refused': refused,
            'recover_restored_all_originals': fully_restored,
            'no_dedup_entry_after_recover': no_dedup,
            'txn_marked_recovered': recovered_terminal,
            'pass': ok,
        }
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================================
# ACCEPTANCE
# ============================================================================================
def prove_clean_and_resend():
    scr = make_scratch('clean')
    try:
        snap, active = build_snapshot(scr)
        before = snapshot_bytes_state(scr)
        res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        after = snapshot_bytes_state(scr)
        clean = {
            'store_moved': before['store'] != after['store'],
            'board_moved': before['board'] != after['board'],
            'store_before': res.store_md5_before[:8], 'store_after': res.store_md5_after[:8],
            'board_before': (res.board_md5_before or '')[:8], 'board_after': res.board_md5_after[:8],
            'players_applied': res.players_applied, 'guard5_green': res.guard5_green,
            'ledger_total': res.ledger_total, 'manifest_pins_coherent': None,
        }
        man = json.load(open(live_paths(scr)['manifest']))
        clean['manifest_pins_coherent'] = (man['store'] == after['store'] and man['board'] == after['board'])
        clean['pass'] = all([clean['store_moved'], clean['board_moved'], clean['guard5_green'],
                             clean['manifest_pins_coherent'], res.players_applied == len(active),
                             res.ledger_total == len(active)])

        # immediate re-send: a FRESH snapshot stamped against the NOW-moved store; dedup must block.
        snap2, _ = build_snapshot(scr)     # re-stamped against the moved store (so NOT stale)
        pre = snapshot_bytes_state(scr)
        blocked = False; err = None
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap2, generated_at="2026-07-20T00:01:00Z")
        except SA.DuplicateRoundError as e:
            blocked = True; err = str(e)[:80]
        resend = {'blocked': blocked, 'error': err,
                  'files_unchanged': snapshot_bytes_state(scr) == pre}
        resend['pass'] = blocked and resend['files_unchanged']

        # stale snapshot: the ORIGINAL snap (stamped against the pre-apply store) must be refused now.
        stale_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at="2026-07-20T00:02:00Z")
        except SA.StaleSnapshotError:
            stale_blocked = True
        stale = {'blocked': stale_blocked, 'files_unchanged': snapshot_bytes_state(scr) == pre}
        stale['pass'] = stale_blocked and stale['files_unchanged']
        return clean, resend, stale
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def prove_altered_invalid_residue():
    """Refusals that fire BEFORE any staging (no board regen needed): altered hash, invalid round,
    residue-open. Each must leave the scratch files byte-identical."""
    scr = make_scratch('refuse')
    try:
        before = snapshot_bytes_state(scr)
        results = {}

        # altered snapshot hash: tamper a score after stamping
        snap, _ = build_snapshot(scr)
        snap_bad = json.loads(json.dumps(snap))
        snap_bad['resolved'][0]['score'] = 999.9      # edit WITHOUT re-stamping the content hash
        altered = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap_bad, generated_at=GEN)
        except SA.AlteredSnapshotError:
            altered = True
        results['altered_hash_blocked'] = altered

        # invalid round: build a round-99 snapshot (season bound is [1,24])
        snap99, _ = build_snapshot(scr, rnd=99)
        invalid = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap99, generated_at=GEN)
        except SA.SeasonBoundError:
            invalid = True
        results['invalid_round_blocked'] = invalid

        # unresolved residue: hand-craft a snapshot with residue_open>0 (never produced by the tool,
        # but the apply must still refuse a snapshot claiming open residue)
        snap_res = json.loads(json.dumps(snap))
        snap_res['counts']['residue_open'] = 2
        snap_res['content_hash'] = RE.compute_content_hash(snap_res)   # re-stamp so ONLY residue trips
        residue_blocked = False
        try:
            SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap_res, generated_at=GEN)
        except SA.ResidueOpenError:
            residue_blocked = True
        results['residue_open_blocked'] = residue_blocked

        results['files_unchanged'] = snapshot_bytes_state(scr) == before
        results['pass'] = all([altered, invalid, residue_blocked, results['files_unchanged']])
        return results
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def prove_snapshot_preview_equivalence():
    """The snapshot -> preview conversion must not change score meaning: the merged season entries it
    produces must equal what score_ingestor.preview produces from the equivalent structured feed."""
    store = json.load(open(store_path_of_real()))
    active = [r for r in store if r.get('stable_player_id') and not r.get('_retired')][:8]
    scores = {r['key']: 100.0 + i * 6 for i, r in enumerate(active)}
    body = "\n".join("%s,%s" % (r['player'], scores[r['key']]) for r in active)
    ent = RE.RoundEntry(15, store=store)
    resolved, _ = ent.resolve_body(body)
    snap = ent.build_snapshot(resolved, generated_at=GEN)
    bridge = SA.preview_from_snapshot(snap, store)
    feed = json.dumps([{'player': r['player'], 'round': 15, 'score': scores[r['key']],
                        'played': 1, 'club': r.get('afl_club')} for r in active])
    ref = ScoreIngestor(store=store).preview(parse_feed(feed))
    bmap = {a.key: a.merged_entry for a in bridge.appends}
    rmap = {a.key: a.merged_entry for a in ref.appends}
    same_keys = set(bmap) == set(rmap)
    mism = [k for k in bmap if bmap[k] != rmap.get(k)]
    return {'players': len(active), 'same_keys': same_keys, 'mismatches': mism,
            'pass': same_keys and not mism}


def store_path_of_real():
    return os.path.join(RA, 'rl_model_data.json')


# ============================================================================================
def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='write PROOF.md + proof.json')
    ap.add_argument('--points', help='comma-separated subset of injection points (default: all)')
    args = ap.parse_args(argv[1:])
    t0 = time.time()

    report = {'gate_shipped': {'APPLY_DEFAULT': SI.APPLY_DEFAULT,
                               'INGEST_SCORE_APPLY': os.environ.get('INGEST_SCORE_APPLY', 'unset')},
              'real_store_written': False}

    # confirm the gate ships OFF on the REAL store before arming anything (scratch-only arming)
    real_off = False
    try:
        SI.ScoreIngestor().apply(SI.ScoreIngestor().preview([]))
    except SI.IngestionGatedError:
        real_off = True
    report['gate_off_on_real_store'] = real_off
    print("[gate] real-store apply refused (gate OFF): %s" % real_off)

    # equivalence (no arming needed; read-only)
    equiv = prove_snapshot_preview_equivalence()
    report['snapshot_preview_equivalence'] = equiv
    print("[equiv] snapshot->preview preserves score meaning: %s (%d players)"
          % (equiv['pass'], equiv['players']))

    arm()
    try:
        points = (args.points.split(',') if args.points else INJECTION_POINTS)
        report['injection'] = {}
        for p in points:
            res = prove_injection(p)
            report['injection'][p] = res
            print("[inject:%-26s] restored=%s no_dedup=%s no_partial_board=%s status=%s => %s"
                  % (p, res['files_byte_identical_after'], res['no_dedup_entry'],
                     res['no_partial_board'], res['txn_status'], 'PASS' if res['pass'] else 'FAIL'))

        rec = prove_crash_recovery()
        report['crash_recovery'] = rec
        print("[recover] crashed=%s incomplete_detected=%s next_apply_refused=%s restored_all=%s => %s"
              % (rec['child_crashed_after_first_replacement'], rec['incomplete_detected'],
                 rec['next_apply_refused'], rec['recover_restored_all_originals'],
                 'PASS' if rec['pass'] else 'FAIL'))

        clean, resend, stale = prove_clean_and_resend()
        report['clean_apply'] = clean
        report['resend_blocked'] = resend
        report['stale_blocked'] = stale
        print("[clean] store %s->%s board %s->%s players=%s guard5=%s pins=%s => %s"
              % (clean['store_before'], clean['store_after'], clean['board_before'],
                 clean['board_after'], clean['players_applied'], clean['guard5_green'],
                 clean['manifest_pins_coherent'], 'PASS' if clean['pass'] else 'FAIL'))
        print("[resend] blocked=%s files_unchanged=%s => %s"
              % (resend['blocked'], resend['files_unchanged'], 'PASS' if resend['pass'] else 'FAIL'))
        print("[stale]  blocked=%s files_unchanged=%s => %s"
              % (stale['blocked'], stale['files_unchanged'], 'PASS' if stale['pass'] else 'FAIL'))

        refusals = prove_altered_invalid_residue()
        report['refusals'] = refusals
        print("[refuse] altered=%s invalid_round=%s residue_open=%s files_unchanged=%s => %s"
              % (refusals['altered_hash_blocked'], refusals['invalid_round_blocked'],
                 refusals['residue_open_blocked'], refusals['files_unchanged'],
                 'PASS' if refusals['pass'] else 'FAIL'))
    finally:
        disarm()

    report['elapsed_s'] = round(time.time() - t0, 1)
    all_pass = (real_off and equiv['pass'] and rec['pass'] and clean['pass'] and resend['pass']
                and stale['pass'] and refusals['pass']
                and all(v['pass'] for v in report['injection'].values()))
    report['ALL_PASS'] = all_pass
    print("\n==== FAILURE-INJECTION + ACCEPTANCE PROOF: %s  (%.1fs) ===="
          % ('ALL PASS' if all_pass else 'FAIL', report['elapsed_s']))

    if args.write:
        with open(os.path.join(HERE, 'proof.json'), 'w') as f:
            json.dump(report, f, indent=2, sort_keys=True)
        with open(os.path.join(HERE, 'PROOF.md'), 'w') as f:
            f.write(_md_report(report))
        print("wrote proof.json + PROOF.md")
    return 0 if all_pass else 1


def _md_report(r):
    L = ["# FAILURE-INJECTION + ACCEPTANCE PROOF — weekly updater safe-local (gate OFF, scratch only)",
         "", "Writes **nothing** to the real store (gate ships OFF: `APPLY_DEFAULT=False` + env "
         "`INGEST_SCORE_APPLY` unset; real-store apply refused = `%s`). Every write below is on a "
         "throwaway scratch repo." % r['gate_off_on_real_store'],
         "", "## RESULT: **%s**  (%.1fs)" % ('ALL PASS' if r['ALL_PASS'] else 'FAIL', r['elapsed_s']),
         "", "## Failure injection (7 points) — rollback leaves the scratch byte-identical",
         "| injection point | files byte-identical | no dedup entry | no partial board | txn status | pass |",
         "|---|---|---|---|---|---|"]
    for p in INJECTION_POINTS:
        d = r['injection'].get(p)
        if not d:
            continue
        L.append("| `%s` | %s | %s | %s | %s | %s |" % (
            p, d['files_byte_identical_after'], d['no_dedup_entry'], d['no_partial_board'],
            d['txn_status'], '✅' if d['pass'] else '❌'))
    rc = r['crash_recovery']
    L += ["", "## Crash recovery (hard-exit mid-commit -> refuse -> recover)",
          "| check | value |", "|---|---|",
          "| child crashed after first replacement | %s |" % rc['child_crashed_after_first_replacement'],
          "| mid-crash: store changed, board still stale (inconsistent) | %s / %s |"
          % (rc['mid_crash_store_changed'], rc['mid_crash_board_stale_inconsistent']),
          "| incomplete transaction detected | %s |" % rc['incomplete_detected'],
          "| next apply REFUSED until recovered | %s |" % rc['next_apply_refused'],
          "| recover restored ALL originals (byte-identical) | %s |" % rc['recover_restored_all_originals'],
          "| no dedup entry after recover | %s |" % rc['no_dedup_entry_after_recover'],
          "| transaction marked RECOVERED (evidence kept) | %s |" % rc['txn_marked_recovered'],
          "", "## Acceptance",
          "| case | result |", "|---|---|",
          "| clean apply: store `%s`→`%s`, board `%s`→`%s`, %d players, Guard 5 GREEN, pins coherent | %s |"
          % (r['clean_apply']['store_before'], r['clean_apply']['store_after'],
             r['clean_apply']['board_before'], r['clean_apply']['board_after'],
             r['clean_apply']['players_applied'], '✅' if r['clean_apply']['pass'] else '❌'),
          "| immediate re-send BLOCKED (dedup), files unchanged | %s |" % ('✅' if r['resend_blocked']['pass'] else '❌'),
          "| stale snapshot BLOCKED (store md5 moved), files unchanged | %s |" % ('✅' if r['stale_blocked']['pass'] else '❌'),
          "| altered snapshot hash BLOCKED | %s |" % ('✅' if r['refusals']['altered_hash_blocked'] else '❌'),
          "| invalid round BLOCKED (season bound) | %s |" % ('✅' if r['refusals']['invalid_round_blocked'] else '❌'),
          "| unresolved residue cannot apply | %s |" % ('✅' if r['refusals']['residue_open_blocked'] else '❌'),
          "| snapshot→preview preserves score meaning (== score_ingestor, %d players) | %s |"
          % (r['snapshot_preview_equivalence']['players'], '✅' if r['snapshot_preview_equivalence']['pass'] else '❌'),
          "", "> Single-env, scratch-only. No numerical-determinism verdict is claimed — the board is "
          "validated for structure, source-stamp coherence, Guard-5 pins and player universe, not for a "
          "cross-run/cross-machine value guarantee (a separate, external item).",
          "> Boards here are built under the hardened, fail-closed forward-valuation path (RL_FV bound to "
          "the staged repo + config policy from the release manifest) — see `FV_PROOF.md`.", ""]
    return '\n'.join(L)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
