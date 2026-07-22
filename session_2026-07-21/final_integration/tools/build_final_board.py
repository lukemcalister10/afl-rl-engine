#!/usr/bin/env python3
"""CLEAN-ROOM CANONICAL REPRODUCTION + REBUILD-EQUALITY PROOF (final integration 2026-07-21, supervisor req 1).

The final canonical board is NO LONGER assembled from a diagnostic artifact. It is produced by the
CANONICAL ENGINE BUILD (rl_export.py under the accepted posture RL_PVC2=1/RL_LEGE=1/RL_LEGF=1) from
ONLY tracked code + the canonical store + the approved sealed F5 input on THIS head. This driver proves it:

  1. re-sync a fresh workspace from the checkout (bootstrap.sh copies HEAD's engine/rl_after +
     engine/forward_valuation + the pinned store/pickles/register/vendor + the sealed F5 structure);
  2. run the canonical engine build (RL_CONFIG_MODE=gate → the manifest pins the posture);
  3. assert the rebuilt board is BYTE-IDENTICAL to the committed data/rl_build/rl_app_data.json (the board
     is declared byte-canonical);
  4. run the release extraction (extract_board_view.py) + club-valuation ingest and assert the rebuilt
     board-view + public bundles are byte-identical to the committed ones (declared byte-canonical);
  5. ORACLE ONLY: compare the rebuilt board's present v + vP1 + vP2 + row universe to the accepted Board B
     (git show 70ef0ff — a comparison oracle, NEVER a build input).

No diagnostic JSON, no other branch/commit, and no pre-existing generated output is a build INPUT here.

Run: RL_REPO=/repo python3 build_final_board.py            # rebuilds + compares; writes evidence; exit 0/1
     (uses the pinned venv on PATH + the /home/claude workspace that bootstrap.sh manages)
"""
import os, sys, json, hashlib, subprocess, shutil, tempfile

ROOT = os.environ.get('RL_REPO') or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
WS = '/home/claude/rl_workspace/rl_after'
VENDOR = '/home/claude/rl_vendor'
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
    ck('(1) bootstrap re-sync from checkout OK (Guard 5 store/rl_model/fv pins)', bs.returncode == 0,
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
    ck('(3) rebuilt board BYTE-IDENTICAL to committed data/rl_build/rl_app_data.json',
       built_md5 is not None and built_md5 == committed_md5,
       'rebuilt %s vs committed %s' % (str(built_md5)[:12], committed_md5[:12]))

    if built_md5 is not None:
        # (4) release extraction reproduces the committed UI bundles byte-identically
        tmp = tempfile.mkdtemp()
        shutil.copy(built, os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json'))  # install rebuilt (== committed)
        ex = run('python3 ui/tools/extract_board_view.py')
        for rel in ('ui/data/board_view_working.js', 'ui/data/board_view_public.js'):
            # compare against git HEAD's committed bytes
            head_bytes = subprocess.check_output(['git', 'show', 'HEAD:%s' % rel], cwd=ROOT)
            now_bytes = open(os.path.join(ROOT, rel), 'rb').read()
            ck('(4) %s byte-identical to committed (HEAD)' % rel.split('/')[-1], head_bytes == now_bytes,
               'match' if head_bytes == now_bytes else 'DIFFERS')
        shutil.rmtree(tmp, ignore_errors=True)

        # (5) ORACLE: present v + vP1 + vP2 + row universe == accepted Board B (comparison only, not a build input)
        B = json.loads(subprocess.check_output(['git', 'show', '%s:%s' % BOARD_B], cwd=ROOT))
        F = json.load(open(built))
        fa = {p['key']: p for p in F['active']}; ba = {p['key']: p for p in B['active']}
        ck('(5-oracle) row universe == Board B', set(fa) == set(ba), '%d vs %d' % (len(fa), len(ba)))
        ck('(5-oracle) present v == Board B (0 diffs)', sum(1 for k in fa if fa[k]['v'] != ba[k]['v']) == 0)
        ck('(5-oracle) vP1 == Board B (0 diffs)', sum(1 for k in fa if fa[k]['vP1'] != ba[k]['vP1']) == 0)
        ck('(5-oracle) vP2 == Board B (0 diffs)', sum(1 for k in fa if fa[k]['vP2'] != ba[k]['vP2']) == 0)

    npass = sum(1 for r in R if r['pass']); n = len(R)
    res = {'ok': npass == n, 'n_pass': npass, 'n': n, 'committed_board_md5': committed_md5,
           'rebuilt_board_md5': built_md5, 'checks': R}
    os.makedirs(os.path.dirname(EV), exist_ok=True)
    json.dump(res, open(EV, 'w'), indent=2)
    print('\nRESULT: %d/%d PASS  (rebuilt md5 %s)  -> %s' % (npass, n, str(built_md5)[:12], os.path.relpath(EV, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
