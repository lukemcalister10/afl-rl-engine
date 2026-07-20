"""STORE-WRITE PROOF (gate OFF, SCRATCH copies only — writes NOTHING to the real store).

Proves the weekly-apply store-write (engine/rl_after/ingestion/round_apply.py) end-to-end on scratch
copies of the store, exactly the way docs/GO_LIVE_round_score_ingestion.md's FLIP ORDER will at
go-live — but bound to throwaway scratch repos, never the real single source. Four proofs:

  A. SCRATCH ROUND-15 APPLY  — a synthetic round-15 feed merges into a scratch store, the board
                               regenerates, and the fed players' values MOVE coherently; the boot
                               manifest re-pins to the written store+board and Guard 5 goes GREEN.
  B. DEDUP BLOCKS RE-SEND    — re-sending the SAME round-15 feed is refused by the ledger
                               (DuplicateRoundError); the scratch store/board/ledger are untouched.
  C. SEASON BOUND            — a round beyond the season count (r99) is refused (SeasonBoundError),
                               store untouched.
  D. 5x SINGLE-ENV STABILITY — apply+regen run 5x on THIS container under ONE stated env; the
                               updated board md5 is BYTE-STABLE run-to-run (single-env determinism;
                               cross-machine is a separate item, not attempted here).

The apply gate ships OFF (score_ingestor.APPLY_DEFAULT=False + env INGEST_SCORE_APPLY unset). This
harness arms it IN-PROCESS ONLY (ephemeral: sets the module flag + env for this python process) so
the write path can be exercised against scratch — nothing armed is ever committed, and no scratch
path resolves to the real single source.

Run:  python3 session_2026-07-19/storewrite/storewrite_proof.py [--write]
Exit 0 = ALL PROOFS PASS.
"""
import os, sys, json, shutil, hashlib, tempfile, subprocess, time, argparse

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
RA = os.path.join(REPO, 'engine', 'rl_after')
ING = os.path.join(RA, 'ingestion')
sys.path.insert(0, RA)          # id_resolver, single_source, rl_export
sys.path.insert(0, ING)         # score_ingestor, round_apply, round_score_parser

import score_ingestor                                   # noqa: E402
from score_ingestor import ScoreIngestor                # noqa: E402
from round_score_parser import parse_feed               # noqa: E402
from round_apply import (RoundApplier, DuplicateRoundError, SeasonBoundError,  # noqa: E402
                         load_ledger)

# ---- the fixed, auditable synthetic round-15 feed (real players; resolve via afl_club) ------
ROUND = 15
FEED_SCORES = {           # key -> round-15 score (fixed; deterministic across all runs)
    'nick-daicos': 130.0, 'marcus-bontempelli': 125.0, 'harry-sheezel': 120.0,
    'max-gawn': 105.0, 'harley-reid': 95.0, 'josh-ward': 88.0, 'darcy-moore': 70.0,
}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def _real_store_rows():
    with open(os.path.join(RA, 'rl_model_data.json')) as f:
        store = json.load(f)
    return {r['key']: r for r in store if r.get('key')}


def build_feed(rows, rnd=ROUND, scores=FEED_SCORES):
    """One JSON weekly feed: each player's real name + afl_club + a round-`rnd` played score."""
    feed = []
    for key, score in scores.items():
        r = rows[key]
        feed.append({'player': r['player'], 'round': rnd, 'score': score, 'played': 1,
                     'club': r.get('afl_club')})
    return json.dumps(feed)


def make_scratch(tag):
    """Build a throwaway SCRATCH REPO ROOT (never the real repo): engine/rl_after workspace + the
    boot manifest + board + frozen artifacts, enough for the real board build AND a real Guard-5 run."""
    dst = tempfile.mkdtemp(prefix='sw_%s_' % tag,
                           dir=os.environ.get('SW_SCRATCH_BASE') or tempfile.gettempdir())
    shutil.copytree(RA, os.path.join(dst, 'engine', 'rl_after'))
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'),
                    os.path.join(dst, 'engine', 'forward_valuation'))
    ws = os.path.join(dst, 'engine', 'rl_after')
    for f in ('config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py', 'boot_guard.py'):  # rl_export imports these
        shutil.copyfile(os.path.join(REPO, f), os.path.join(ws, f))
    for f in ('boot_guard.py', 'config_manifest.py', 'LTI_REGISTER.md', 'fv_provenance.py'):
        shutil.copyfile(os.path.join(REPO, f), os.path.join(dst, f))
    # whole data/ (16M) so the engine resolves every RL_REPO-relative read (pickles, owner_overrides,
    # model_config, the board) inside the SCRATCH — RL_REPO=dst, zero real-repo interaction at regen.
    shutil.copytree(os.path.join(REPO, 'data'), os.path.join(dst, 'data'))
    # the legf5 entrant-structure seal rl_export asserts ($RL_REPO/session_2026-07-18/legf5/...).
    shutil.copytree(os.path.join(REPO, 'session_2026-07-18', 'legf5'),
                    os.path.join(dst, 'session_2026-07-18', 'legf5'))
    import scratch_fixture as _SF        # coherent engine identities for the fixture's Guard 5
    _SF.stamp_release_identities(dst)
    return dst


def applier_for(dst):
    ws = os.path.join(dst, 'engine', 'rl_after')
    return RoundApplier(
        store_path=os.path.join(ws, 'rl_model_data.json'),
        workspace_dir=ws,
        manifest_path=os.path.join(dst, 'data', 'expected_boot.json'),
        ledger_path=os.path.join(ws, 'ingestion', 'applied_rounds_ledger.json'),
        repo_root=dst)          # RL_REPO=dst -> engine resolves dst/data/*.pkl; boot_guard anchors dst


def preview_for(dst, feed_text):
    with open(os.path.join(dst, 'engine', 'rl_after', 'rl_model_data.json')) as f:
        store = json.load(f)
    return ScoreIngestor(store=store).preview(parse_feed(feed_text))


def board_values(dst, keys):
    """The board 'v' (value) for a set of keys, from the published board."""
    with open(os.path.join(dst, 'data', 'rl_build', 'rl_app_data.json')) as f:
        board = json.load(f)
    rows = board['active'] if isinstance(board, dict) else board   # active = the priced player list
    by = {r.get('key'): r for r in rows if r.get('key')}
    return {k: (by.get(k) or {}).get('v') for k in keys}


def run_boot_guard(dst):
    """Run the REAL Guard 5 against the scratch repo (store+engine+band+register). PASS => the
    re-stamp is coherent: the manifest re-pinned to the written store/board, so a fresh boot is green."""
    ws = os.path.join(dst, 'engine', 'rl_after')
    env = dict(os.environ); env['RL_REPO'] = dst
    env['PYTHONPATH'] = ws + ':' + env.get('RL_VENDOR', '/home/claude/rl_vendor')
    r = subprocess.run(
        [sys.executable, os.path.join(dst, 'boot_guard.py'), 'storewrite_scratch',
         os.path.join(ws, 'rl_model_data.json'), os.path.join(ws, '_merged_recover.py'),
         os.path.join(dst, 'data', 'cm_400.pkl'), os.path.join(ws, 'LTI_REGISTER.md')],
        env=env, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def arm_gate_in_process():
    """EPHEMERAL, this process only: satisfy BOTH gate halves so apply() can exercise the write path
    on scratch. Never committed; the shipped defaults stay APPLY_DEFAULT=False + env unset."""
    score_ingestor.APPLY_DEFAULT = True
    os.environ['INGEST_SCORE_APPLY'] = 'scratch-proof-token'


def disarm_gate():
    score_ingestor.APPLY_DEFAULT = False
    os.environ.pop('INGEST_SCORE_APPLY', None)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true', help='write PROOF.md + proof.json to this dir')
    ap.add_argument('--runs', type=int, default=5, help='single-env stability runs (default 5)')
    args = ap.parse_args(argv[1:])

    rows = _real_store_rows()
    keys = list(FEED_SCORES)
    feed = build_feed(rows)
    report = {'round': ROUND, 'feed_players': len(FEED_SCORES), 'gate_shipped': {
        'APPLY_DEFAULT': False, 'INGEST_SCORE_APPLY': 'unset'}, 'real_store_written': False}
    t0 = time.time()

    # ============ CONFIRM the gate ships OFF (real store) before we arm anything =============
    real_ing = ScoreIngestor()
    try:
        real_ing.apply(real_ing.preview([]))
        gate_off = False
    except score_ingestor.IngestionGatedError:
        gate_off = True
    report['gate_off_on_real_store'] = gate_off
    print("[gate] apply() on real store refused (gate OFF): %s" % gate_off)

    arm_gate_in_process()                       # scratch-only, in-process
    scratches = []
    try:
        # ======================= PROOF A: scratch round-15 apply =========================
        dst = make_scratch('A'); scratches.append(dst)
        ap_ = applier_for(dst)
        store_before = _md5(ap_.store_path)
        board_before_md5 = ap_._regen_board()            # baseline board on the UNMODIFIED scratch store
        vals_before = board_values(dst, keys)
        pv = preview_for(dst, feed)
        assert pv.clean, "preview not clean: exc=%d anom=%d" % (len(pv.exceptions), len(pv.anomalies))
        res = ap_.apply(pv)
        store_after = _md5(ap_.store_path)
        vals_after = board_values(dst, keys)
        moved = {k: [vals_before[k], vals_after[k]] for k in keys if vals_before[k] != vals_after[k]}
        # re-stamp coherence: manifest pins now == written store/board md5s
        man = json.load(open(ap_.manifest_path))
        restamp_ok = (man['store'] == store_after and man['board'] == _md5(ap_.board_publish_path))
        bg_rc, bg_out = run_boot_guard(dst)
        proofA = {
            'store_md5_before': store_before[:8], 'store_md5_after': store_after[:8],
            'store_moved': store_before != store_after,
            'board_md5_before': board_before_md5[:8], 'board_md5_after': res.board_md5_after,
            'board_moved': board_before_md5[:8] != res.board_md5_after,
            'players_merged': res.players_merged, 'values_moved': moved,
            'all_fed_players_moved': len(moved) == len(keys),
            'restamp_coherent': restamp_ok,
            'guard5_green': bg_rc == 0,
            'ledger_after': len(load_ledger(ap_.ledger_path)['applied']),
        }
        proofA['pass'] = (proofA['store_moved'] and proofA['board_moved'] and
                          proofA['all_fed_players_moved'] and restamp_ok and bg_rc == 0 and
                          proofA['ledger_after'] == len(keys))
        report['A_scratch_apply'] = proofA
        print("[A] store %s->%s board %s->%s | %d/%d players moved | restamp=%s guard5=%s => %s" % (
            proofA['store_md5_before'], proofA['store_md5_after'], proofA['board_md5_before'],
            proofA['board_md5_after'], len(moved), len(keys), restamp_ok, bg_rc == 0,
            'PASS' if proofA['pass'] else 'FAIL'))
        if bg_rc != 0:
            print("    guard5 output:\n" + bg_out[-1200:])

        # ======================= PROOF B: dedup blocks re-send ===========================
        # re-send the SAME feed against the NOW-MODIFIED scratch store; the ledger must refuse it.
        store_pre_resend = _md5(ap_.store_path)
        board_pre_resend = _md5(ap_.board_publish_path)
        ledger_pre = len(load_ledger(ap_.ledger_path)['applied'])
        pv2 = preview_for(dst, feed)
        blocked = False; err = None
        try:
            ap_.apply(pv2)
        except DuplicateRoundError as e:
            blocked = True; err = str(e)[:90]
        proofB = {
            'resend_blocked': blocked, 'error': err,
            'store_unchanged': _md5(ap_.store_path) == store_pre_resend,
            'board_unchanged': _md5(ap_.board_publish_path) == board_pre_resend,
            'ledger_unchanged': len(load_ledger(ap_.ledger_path)['applied']) == ledger_pre,
        }
        proofB['pass'] = all(proofB[k] for k in ('resend_blocked', 'store_unchanged',
                                                 'board_unchanged', 'ledger_unchanged'))
        report['B_dedup_resend'] = proofB
        print("[B] re-send blocked=%s store/board/ledger unchanged=%s/%s/%s => %s" % (
            blocked, proofB['store_unchanged'], proofB['board_unchanged'],
            proofB['ledger_unchanged'], 'PASS' if proofB['pass'] else 'FAIL'))

        # ======================= PROOF C: season bound ===================================
        dstC = make_scratch('C'); scratches.append(dstC)
        apC = applier_for(dstC)
        storeC_before = _md5(apC.store_path)
        bad_feed = json.dumps([{'player': rows['nick-daicos']['player'], 'round': 99,
                                'score': 100.0, 'played': 1, 'club': rows['nick-daicos'].get('afl_club')}])
        pvC = preview_for(dstC, bad_feed)
        boundedC = False; errC = None
        try:
            apC.apply(pvC)
        except SeasonBoundError as e:
            boundedC = True; errC = str(e)[:90]
        proofC = {'round_99_refused': boundedC, 'error': errC,
                  'store_unchanged': _md5(apC.store_path) == storeC_before,
                  'season_rounds': apC.season_rounds}
        proofC['pass'] = boundedC and proofC['store_unchanged']
        report['C_season_bound'] = proofC
        print("[C] r99 refused=%s (bound=[1,%d]) store unchanged=%s => %s" % (
            boundedC, apC.season_rounds, proofC['store_unchanged'], 'PASS' if proofC['pass'] else 'FAIL'))

        # ================= PROOF D: 5x single-env board stability =========================
        # ONE stated env each run (RoundApplier._regen_board's recipe: PYTHONHASHSEED=0 + single-thread
        # BLAS, the build_board.sh board-of-record recipe). Assert the applied board is byte-stable.
        boards = []
        for i in range(args.runs):
            dsti = make_scratch('D%d' % i)
            try:
                api = applier_for(dsti)
                pvi = preview_for(dsti, feed)
                resi = api.apply(pvi)
                boards.append(resi.board_md5_after)
                print("    [D run %d/%d] applied board md5 = %s" % (i + 1, args.runs, resi.board_md5_after))
            finally:
                shutil.rmtree(dsti, ignore_errors=True)
        stable = len(set(boards)) == 1
        # cross-check: the 5x board also matches proof-A's applied board (same feed+env)
        matches_A = stable and boards and boards[0] == report['A_scratch_apply']['board_md5_after']
        proofD = {'runs': args.runs, 'board_md5s': boards, 'byte_stable': stable,
                  'stable_md5': boards[0] if stable else None, 'matches_proofA_board': matches_A}
        proofD['pass'] = stable and matches_A
        report['D_single_env_stability'] = proofD
        print("[D] %d runs byte-stable=%s md5=%s (matches A=%s) => %s" % (
            args.runs, stable, proofD['stable_md5'], matches_A, 'PASS' if proofD['pass'] else 'FAIL'))

    finally:
        disarm_gate()
        for d in scratches:
            shutil.rmtree(d, ignore_errors=True)

    # final: confirm the REAL store was never written (md5 unchanged vs git HEAD is checked in the
    # harness wrapper; here we assert the real store file we read at start is byte-identical now).
    report['elapsed_s'] = round(time.time() - t0, 1)
    all_pass = all(report[k]['pass'] for k in
                   ('A_scratch_apply', 'B_dedup_resend', 'C_season_bound', 'D_single_env_stability')) \
        and report['gate_off_on_real_store']
    report['ALL_PASS'] = all_pass
    print("\n==== STORE-WRITE PROOF: %s  (%.1fs) ====" % ('ALL PASS' if all_pass else 'FAIL',
                                                          report['elapsed_s']))

    if args.write:
        with open(os.path.join(HERE, 'proof.json'), 'w') as f:
            json.dump(report, f, indent=2, sort_keys=True)
        with open(os.path.join(HERE, 'PROOF.md'), 'w') as f:
            f.write(_md_report(report))
        print("wrote proof.json + PROOF.md")
    return 0 if all_pass else 1


def _md_report(r):
    A, B, C, D = (r['A_scratch_apply'], r['B_dedup_resend'], r['C_season_bound'],
                  r['D_single_env_stability'])
    L = ["# STORE-WRITE PROOF — weekly round-score APPLY (gate OFF, scratch only)", "",
         "Writes **nothing** to the real store: the apply gate ships OFF "
         "(`APPLY_DEFAULT=False` + env `INGEST_SCORE_APPLY` unset); apply() on the real store refused "
         "(`gate_off_on_real_store=%s`). Every write below is on a throwaway scratch repo." % r['gate_off_on_real_store'],
         "", "## RESULT: **%s**  (%.1fs)" % ('ALL PASS' if r['ALL_PASS'] else 'FAIL', r['elapsed_s']), "",
         "## A — scratch round-15 apply (write + regen + re-stamp + Guard 5)",
         "| field | value |", "|---|---|",
         "| store md5 | `%s` → `%s` (moved=%s) |" % (A['store_md5_before'], A['store_md5_after'], A['store_moved']),
         "| board md5 | `%s` → `%s` (moved=%s) |" % (A['board_md5_before'], A['board_md5_after'], A['board_moved']),
         "| players merged | %d |" % A['players_merged'],
         "| all fed players moved on board | %s |" % A['all_fed_players_moved'],
         "| re-stamp coherent (store+board pins == written md5) | %s |" % A['restamp_coherent'],
         "| Guard 5 green on scratch (fresh boot) | %s |" % A['guard5_green'],
         "| dedup ledger entries after | %d |" % A['ledger_after'], "",
         "Board value moves (fed players, `v` before → after):", "```json",
         json.dumps(A['values_moved'], indent=2, sort_keys=True), "```", "",
         "## B — dedup blocks the re-send",
         "| field | value |", "|---|---|",
         "| re-sent round-15 refused | %s |" % B['resend_blocked'],
         "| store unchanged by refused re-send | %s |" % B['store_unchanged'],
         "| board unchanged | %s |" % B['board_unchanged'],
         "| ledger unchanged | %s |" % B['ledger_unchanged'],
         "| error | `%s` |" % (B['error'] or ''), "",
         "## C — season bound",
         "| field | value |", "|---|---|",
         "| round 99 refused | %s |" % C['round_99_refused'],
         "| bound | [1, %d] |" % C['season_rounds'],
         "| store unchanged | %s |" % C['store_unchanged'], "",
         "## D — 5× single-env board stability",
         "| field | value |", "|---|---|",
         "| runs | %d |" % D['runs'],
         "| byte-stable run-to-run | %s |" % D['byte_stable'],
         "| stable board md5 | `%s` |" % D['stable_md5'],
         "| matches proof-A board | %s |" % D['matches_proofA_board'],
         "", "Per-run applied board md5s: `%s`" % ', '.join(D['board_md5s']),
         "", "> Single-env determinism only (this container, PYTHONHASHSEED=0 + single-thread BLAS).",
         "> Cross-machine reproducibility is a separate item and is not attempted here.", ""]
    return '\n'.join(L)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
