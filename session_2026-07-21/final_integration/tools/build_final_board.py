#!/usr/bin/env python3
"""CLEAN-ROOM CANONICAL REPRODUCTION + REBUILD-EQUALITY PROOF (final integration 2026-07-21, supervisor req 1;
ITEM 408 present-oracle migration 2026-07-24).

The final canonical board is NO LONGER assembled from a diagnostic artifact. It is produced by the
CANONICAL ENGINE BUILD (rl_export.py under the accepted posture RL_PVC2=1/RL_LEGE=1/RL_LEGF=1) from
ONLY tracked code + the canonical store + the approved sealed F5 input on THIS head. This driver proves it:

  1. re-sync a fresh workspace from the checkout (bootstrap.sh copies HEAD's engine/rl_after +
     engine/forward_valuation + the pinned store/pickles/register/vendor + the sealed F5 structure);
  2. run the canonical engine build (RL_CONFIG_MODE=gate -> the manifest pins the posture);
  3. assert the rebuilt board is BYTE-IDENTICAL to the committed data/rl_build/rl_app_data.json (the board
     is declared byte-canonical);
  4. run the release extraction (extract_board_view.py) + club-valuation ingest and assert the rebuilt
     board-view + public bundles are byte-identical to the committed ones (declared byte-canonical);
  5. PRESENT ORACLE (gating): compare the rebuilt board's present v to the ACCEPTED balanced/strict
     reference vector reference_vector_1373e824.json (committed; the SAME authority invariant_proof.py
     gates against; NEVER derived from the rebuilt board, and NOT Board B). Fail-closed on the reference
     vector's authority metadata (board 1373e824 / active 804 / Sigma v 760253); require the rebuilt active
     key set to equal the reference key set exactly and every rebuilt v to equal the reference exactly.
     FORWARD (structure gating): vP1/vP2 present + numeric for all 804 rebuilt rows and the historical
     Board B key universe matches the rebuilt universe. The Board B forward SEMANTIC comparison (vP1/vP2)
     is owner-DEFERRED (ITEM 408) — a historical R14 diagnostic with no accepted R19 forward oracle: its
     deltas are MEASURED and REPORTED, never asserted as a pass and never used to fail the tool
     (git show 70ef0ff — read-only diagnostic, NEVER a build input).

Overall `ok` reflects ONLY the accepted gating properties (rebuild + present + forward-structure). A missing
or non-numeric forward vector, or a row-universe mismatch, is a HARD failure; semantic inequality to the
superseded Board B is not.

No diagnostic JSON, no other branch/commit, and no pre-existing generated output is a build INPUT here.

Run: RL_REPO=/repo python3 build_final_board.py            # rebuilds + compares; writes evidence; exit 0/1
     (uses the pinned venv on PATH + the /home/claude workspace that bootstrap.sh manages)
"""
import os, sys, json, hashlib, subprocess, shutil, tempfile

ROOT = os.environ.get('RL_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
WS = '/home/claude/rl_workspace/rl_after'
VENDOR = '/home/claude/rl_vendor'
# PRESENT-LENS ORACLE (accepted, ITEM 408 STOP-1): the committed balanced/strict reference vector 1373e824 —
# the SAME authority invariant_proof.py gates against. Loaded from the checkout; NEVER derived from the
# rebuilt board.
REF_VECTOR = 'session_2026-07-20/fv_provenance_remediation/fixtures/reference_vector_1373e824.json'
PRESENT_BALANCED_MD5 = '1373e82471a81064ef96820f3db065df'
PRESENT_ACTIVE = 804
PRESENT_TOTAL = 760253
# Board B is retained ONLY as a historical R14 forward diagnostic (vP1/vP2) — never a present oracle, never a
# gating pass. Its semantic equality is owner-DEFERRED (no accepted R19 forward oracle).
BOARD_B = ('70ef0ff36ca7633aa4097a9b7c1a730013870abe',
           'session_2026-07-21/forward_lens_acceptance/board_B_lege1_legf1.json')
EV = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'evidence', 'cleanroom_repro.json'))
R = []
def ck(name, ok, detail=''):
    R.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('  PASS ' if ok else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(ok)

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

def run(cmd, cwd=ROOT, env=None, timeout=600):
    e = dict(os.environ, RL_REPO=ROOT, RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
    if env: e.update(env)
    return subprocess.run(cmd, cwd=cwd, env=e, shell=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)

def main():
    print('=== CLEAN-ROOM CANONICAL REPRODUCTION + REBUILD-EQUALITY ===')
    committed_board = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')
    committed_md5 = md5(committed_board)

    # (1) re-sync the workspace from the checkout (HEAD's tracked engine code + pinned inputs)
    bs = run('RL_VENDOR=%s/vendor bash %s/bootstrap.sh' % (ROOT, ROOT))
    ok1 = ck('(1) bootstrap re-sync from checkout OK (Guard 5 store/rl_model/fv pins)', bs.returncode == 0,
             'rc=%d' % bs.returncode)

    # (2) canonical engine build from tracked code + store + sealed F5 input.
    # Clean-room posture: the build must NOT inherit any ambient RL_*/PAR_* dev-shell override
    # (config_manifest in gate mode fail-closes on unknown overrides such as RL_VENDOR — a class-B
    # infra var used only by bootstrap.sh, never by the build). Scrub every ambient RL_*/PAR_* and
    # re-set ONLY the three the build legitimately consumes: RL_REPO (season_state.json lookup),
    # RL_FV (forward-valuation source), RL_CONFIG_MODE=gate (manifest posture). Vendored offline deps
    # are found via PYTHONPATH, not RL_VENDOR.
    build_env = {k: v for k, v in os.environ.items() if not (k.startswith('RL_') or k.startswith('PAR_'))}
    build_env.update({'PYTHONPATH': '%s:%s' % (WS, VENDOR), 'RL_CONFIG_MODE': 'gate',
                      'RL_REPO': ROOT, 'RL_FV': os.path.join(ROOT, 'engine', 'forward_valuation')})
    built = os.path.join(WS, 'rl_app_data.json')
    if os.path.exists(built):
        os.remove(built)  # guard against a stale board masking a build failure
    bd = subprocess.run('python3 rl_export.py', cwd=WS, env=build_env, shell=True, text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)
    built_md5 = md5(built) if os.path.exists(built) else None
    ok2 = ck('(2) canonical engine build (RL_PVC2/LEGE/LEGF=1) succeeds', bd.returncode == 0 and built_md5 is not None,
             'rc=%d' % bd.returncode)
    if not ok2:
        sys.stderr.write('\n[build tail]\n%s\n' % '\n'.join((bd.stdout or '').splitlines()[-25:]))

    # (3) rebuilt board == committed board, BYTE-IDENTICAL
    ok3 = ck('(3) rebuilt board BYTE-IDENTICAL to committed data/rl_build/rl_app_data.json',
             built_md5 is not None and built_md5 == committed_md5,
             'rebuilt %s vs committed %s' % (str(built_md5)[:12], committed_md5[:12]))

    ok4_all = False
    ok_present = False
    ok_forward_structure = False
    rebuilt_sum_v = None
    present_added = present_removed = present_mismatch = None
    forward_comparison = {'status': 'DEFERRED', 'gating': False,
                          'note': 'not evaluated — canonical rebuild did not produce a board'}

    if built_md5 is not None:
        # (4) release extraction reproduces the committed UI bundles byte-identically
        tmp = tempfile.mkdtemp()
        shutil.copy(built, os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json'))  # install rebuilt (== committed)
        ex = run('python3 ui/tools/extract_board_view.py')
        ok4_all = True
        for rel in ('ui/data/board_view_working.js', 'ui/data/board_view_public.js'):
            # compare against git HEAD's committed bytes
            head_bytes = subprocess.check_output(['git', 'show', 'HEAD:%s' % rel], cwd=ROOT)
            now_bytes = open(os.path.join(ROOT, rel), 'rb').read()
            ok4_all = ck('(4) %s byte-identical to committed (HEAD)' % rel.split('/')[-1], head_bytes == now_bytes,
                         'match' if head_bytes == now_bytes else 'DIFFERS') and ok4_all
        shutil.rmtree(tmp, ignore_errors=True)

        F = json.load(open(built))
        fa = {p['key']: p for p in F['active']}

        # (5-present) PRESENT ORACLE (gating) — rebuilt present v vs the ACCEPTED reference vector 1373e824.
        # Loaded from the committed checkout; the present oracle is NEVER derived from the rebuilt board and is
        # NOT Board B. Fail closed on the reference vector's authority metadata.
        RV = json.load(open(os.path.join(ROOT, REF_VECTOR)))
        rv_ident = str(RV.get('board_md5', ''))
        rv_auth = ((rv_ident == PRESENT_BALANCED_MD5 or rv_ident.startswith('1373e824'))
                   and RV.get('active') == PRESENT_ACTIVE and RV.get('sum_v') == PRESENT_TOTAL)
        ok_p_auth = ck('(5-present) reference vector authority is the accepted 1373e824 (active 804, Sigma v 760253) [fail-closed]',
                       rv_auth, 'board_md5=%s active=%s sum_v=%s' % (rv_ident[:12], RV.get('active'), RV.get('sum_v')))
        rvec = {k: int(v) for k, v in RV['vector'].items()} if rv_auth else {}
        present_added = sorted(set(fa) - set(rvec))     # rebuilt keys absent from the reference vector
        present_removed = sorted(set(rvec) - set(fa))   # reference keys absent from the rebuilt board
        ok_p_keys = ck('(5-present) rebuilt active key set == reference-vector key set (exact)',
                       rv_auth and not present_added and not present_removed,
                       '%d rebuilt / %d reference; +%d added %s / -%d removed %s' % (
                         len(fa), len(rvec), len(present_added), present_added[:5],
                         len(present_removed), present_removed[:5]))
        present_mismatch = [k for k in fa if k in rvec and int(fa[k]['v']) != rvec[k]]
        ok_p_v = ck('(5-present) every rebuilt present v == reference vector (0 mismatches)',
                    rv_auth and not present_added and not present_removed and not present_mismatch,
                    '%d mismatches%s' % (len(present_mismatch),
                      (' e.g. ' + ', '.join('%s(rebuilt %s vs ref %s)' % (k, fa[k]['v'], rvec[k])
                                             for k in present_mismatch[:5])) if present_mismatch else ''))
        rebuilt_sum_v = sum(int(p['v']) for p in F['active'])
        ok_present = ok_p_auth and ok_p_keys and ok_p_v

        # (5-forward-structure) FORWARD gating — vP1/vP2 present + numeric for ALL rows, and (Board B retained)
        # the historical Board B key universe matches the rebuilt active universe. A missing/non-numeric forward
        # vector or a row-universe mismatch is a HARD failure; Board B SEMANTIC (value) inequality is NOT.
        def _num(x):
            return isinstance(x, (int, float)) and not isinstance(x, bool)
        fwd_missing = [p['key'] for p in F['active'] if not (_num(p.get('vP1')) and _num(p.get('vP2')))]
        ok_f_num = ck('(5-forward-structure) vP1 & vP2 present + numeric for all %d rebuilt active rows' % len(fa),
                      len(fa) == PRESENT_ACTIVE and not fwd_missing,
                      'active=%d non-numeric/missing=%d %s' % (len(fa), len(fwd_missing), fwd_missing[:5]))
        B = json.loads(subprocess.check_output(['git', 'show', '%s:%s' % BOARD_B], cwd=ROOT))
        ba = {p['key']: p for p in B['active']}
        bb_added = sorted(set(fa) - set(ba))     # rebuilt keys absent from Board B
        bb_removed = sorted(set(ba) - set(fa))   # Board B keys absent from the rebuilt board
        ok_f_univ = ck('(5-forward-structure) historical Board B key universe == rebuilt active universe',
                       not bb_added and not bb_removed,
                       '%d rebuilt / %d Board B; +%d added %s / -%d removed %s' % (
                         len(fa), len(ba), len(bb_added), bb_added[:5], len(bb_removed), bb_removed[:5]))
        ok_forward_structure = ok_f_num and ok_f_univ

        # (5-forward-DEFERRED) Board B SEMANTIC comparison — MEASURED, never asserted as a pass, never gating.
        # Board B (70ef0ff) is a HISTORICAL R14 forward diagnostic; no accepted R19 forward oracle exists, so
        # vP1/vP2 semantic equality is owner-DEFERRED (ITEM 408). We record the deltas; we do NOT pass/fail on them.
        common = [k for k in fa if k in ba]
        vP1_equal = sum(1 for k in common if fa[k].get('vP1') == ba[k].get('vP1'))
        vP2_equal = sum(1 for k in common if fa[k].get('vP2') == ba[k].get('vP2'))
        vP1_changed = len(common) - vP1_equal
        vP2_changed = len(common) - vP2_equal
        forward_comparison = {
            'basis': 'historical R14 Board B (git 70ef0ff:%s)' % BOARD_B[1],
            'status': 'DEFERRED', 'gating': False, 'is_accepted_R19_oracle': False,
            'reason': 'forward-lens (vP1/vP2) semantic equality to the superseded R14 Board B is owner-DEFERRED '
                      '(no accepted R19 forward oracle exists); the deltas are MEASURED and REPORTED, never '
                      'asserted as a pass and never used to fail the tool.',
            'common_keys': len(common),
            'vP1_equal': vP1_equal, 'vP1_changed': vP1_changed,
            'vP2_equal': vP2_equal, 'vP2_changed': vP2_changed,
            'keys_missing_vs_boardB': bb_removed, 'keys_added_vs_boardB': bb_added}
        print('  DEFERRED (5-forward) Board B semantic comparison — historical R14 forward diagnostic, NOT an '
              'accepted R19 oracle, NOT a gating PASS:')
        print('           vP1 equal=%d changed=%d | vP2 equal=%d changed=%d | +%d added / -%d removed keys '
              '(measured, not asserted)' % (vP1_equal, vP1_changed, vP2_equal, vP2_changed, len(bb_added), len(bb_removed)))

    # Overall acceptance = accepted GATING properties ONLY (the Board B semantic deltas are excluded).
    ok_rebuild = bool(ok1 and ok2 and ok3 and ok4_all)
    overall_ok = bool(ok_rebuild and ok_present and ok_forward_structure)
    npass = sum(1 for r in R if r['pass']); n = len(R)
    res = {
      'ok': overall_ok,                       # accepted GATING properties only (Board B semantic deltas excluded)
      'ok_rebuild': ok_rebuild,
      'ok_present': ok_present,
      'ok_forward_structure': ok_forward_structure,
      'forward_lens_deferred': True,
      'forward_comparison': forward_comparison,   # measured Board B deltas + deferred reason (NON-gating)
      'committed_board_md5': committed_md5,
      'rebuilt_board_md5': built_md5,
      'rebuilt_present_sum_v': rebuilt_sum_v,
      'present_reference': {'path': REF_VECTOR, 'board_md5': PRESENT_BALANCED_MD5,
                            'active': PRESENT_ACTIVE, 'sum_v': PRESENT_TOTAL,
                            'added_keys': present_added, 'removed_keys': present_removed,
                            'v_mismatches': present_mismatch},
      'n_pass': npass, 'n': n, 'checks': R}
    os.makedirs(os.path.dirname(EV), exist_ok=True)
    json.dump(res, open(EV, 'w'), indent=2)
    print('\nGATES: ok_rebuild=%s ok_present=%s ok_forward_structure=%s  (forward-lens Board B DEFERRED, non-gating)'
          % (ok_rebuild, ok_present, ok_forward_structure))
    print('RESULT: overall_ok=%s  gating %d/%d PASS  (rebuilt md5 %s)  -> %s'
          % (overall_ok, npass, n, str(built_md5)[:12], os.path.relpath(EV, ROOT)))
    return 0 if overall_ok else 1

if __name__ == '__main__':
    sys.exit(main())
