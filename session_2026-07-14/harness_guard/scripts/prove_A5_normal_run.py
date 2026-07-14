#!/usr/bin/env python3
# A5 — NOTHING GREEN TURNED RED. A normal (seam-free) run: reds exactly {A2,A3,A12}; B1 PASS on the July-8
# construction (1.2601 / 1.2407 / 1.1521); panel 10/10; Guard 5 green; H1/H2 PASS; store 340a7a32 and board
# 3dc19fbb byte-identical. This is the one full run (matrix regenerated ~3 min); everything else was cheap.
import json, hashlib, os, subprocess, sys
ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
OUT = os.path.join(ROOT, 'session_2026-07-14', 'harness_guard', 'out')

def md5f(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()[:8]

store_md5 = md5f(os.path.join(RA, 'rl_model_data.json'))
board_md5 = md5f(os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json'))

# NORMAL invocation: NO SGC_* in the ambient env. The suite's B1 regen spawns s4_matrix with
# RL_CONFIG_MODE=gate, and config_manifest.enforce REJECTS any ambient SGC_* in gate mode (the item-38
# fail-close). So a leaked SGC_REPORT_DIR would HALT the regen (empty book -> B1 JSONDecodeError). Scrub
# SGC_* to certify on the true default path; the report lands in the default dir and is copied below.
env = {k: v for k, v in os.environ.items() if not k.startswith('SGC_')}
env['RL_REPO'] = ROOT
r = subprocess.run([sys.executable, os.path.join(ROOT, 'ship_gates_check.py')],
                   env=env, capture_output=True, text=True, cwd=ROOT, timeout=1800)
# copy the report the suite wrote (default SGC_REPORT_DIR = session_2026-07-02) into this session's evidence
try:
    import shutil, re as _re2
    _m = _re2.search(r'report: (\S+)', r.stdout)
    if _m:
        shutil.copy(os.path.join(ROOT, _m.group(1)), os.path.join(OUT, 'a5_ship_gates_report.md'))
except Exception:
    pass
suite_out = r.stdout + '\n---STDERR---\n' + r.stderr
open(os.path.join(OUT, 'a5_suite.log'), 'w').write(suite_out)
guard5 = 'boot-store guard (Guard 5) PASS' in suite_out

# panel
rp = subprocess.run(['bash', os.path.join(ROOT, 'run_panel.sh')], capture_output=True, text=True, cwd=ROOT, timeout=600)
panel_out = rp.stdout + rp.stderr
open(os.path.join(OUT, 'a5_panel.log'), 'w').write(panel_out)
panel_10 = 'PASS 10/10' in panel_out and rp.returncode == 0

# reds from the snapshot the suite just wrote (authoritative per-gate status)
HEAD = md5f(os.path.join(RA, '_merged_recover.py'))
snap = json.load(open(os.path.join(ROOT, 'data', 'gates_snapshots', 'gates_%s.json' % HEAD)))
reds = sorted(g for g, v in snap['gates'].items() if v['status'] in ('FAIL', 'ERROR', 'HALT'))
reds_ok = reds == ['A12', 'A2', 'A3']  # sorted
h1 = snap['gates'].get('H1', {}).get('status')
h2 = snap['gates'].get('H2', {}).get('status')
# B1 ratios: the snapshot detail is truncated to 200 chars, so read the FULL suite log for the ratio string.
b1full = open(os.path.join(OUT, 'a5_suite.log')).read()
b1_ok = (snap['gates'].get('B1', {}).get('status') == 'PASS'
         and all(x in b1full for x in ('1.2601', '1.2407', '1.1521')))
b1det = 'ratios 1.2601/1.2407/1.1521 PASS x3' if b1_ok else snap['gates'].get('B1', {}).get('detail', '')[:80]

checks = {
    'reds == {A2,A3,A12}': (reds_ok, reds),
    'B1 PASS 1.2601/1.2407/1.1521': (b1_ok, b1det[:80]),
    'panel 10/10': (panel_10, 'rc=%d' % rp.returncode),
    'Guard 5 green': (guard5, ''),
    'H1 PASS': (h1 == 'PASS', h1),
    'H2 PASS': (h2 == 'PASS', h2),
    'store 340a7a32 byte-identical': (store_md5 == '340a7a32', store_md5),
    'board 3dc19fbb byte-identical': (board_md5 == '3dc19fbb', board_md5),
}
allok = all(v[0] for v in checks.values())
print('HEAD=%s store=%s board=%s suite_rc=%d' % (HEAD, store_md5, board_md5, r.returncode))
for k, (ok, extra) in checks.items():
    print('  [%s] %s  %s' % ('PASS' if ok else 'FAIL', k, extra))
print('\nA5 %s' % ('PASS' if allok else 'FAIL'))
open(os.path.join(OUT, 'rc_A5'), 'w').write(
    '%s  reds=%s B1=%s panel=%s guard5=%s H1=%s H2=%s store=%s board=%s suite_rc=%d\n'
    % ('PASS' if allok else 'FAIL', reds, b1_ok, panel_10, guard5, h1, h2, store_md5, board_md5, r.returncode))
sys.exit(0 if allok else 1)
