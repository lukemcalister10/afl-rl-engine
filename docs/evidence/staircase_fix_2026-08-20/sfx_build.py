#!/usr/bin/env python3
"""THE STAIRCASE FIX — board build driver.

Carried from docs/evidence/d8_ceiling_2026-08-20/d8_build.py with TWO declared changes and nothing
else: (1) the driver's own env-var names are SFX_-prefixed, NEVER RL_-prefixed (the thrice-burned
rule, P-family hardened: a tooling variable that starts with RL_ is read by config_manifest.enforce()
as an unknown model override and HALTS a canonical build); (2) the labels.

Uses the ACCEPTED disposable FV builder
(session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build) exactly as the D8
pricing seat and the H3 repair seat did. Writes NOTHING under the repo; the staging tree is deleted
after each run.

  SFX_REPO   the checkout root
  SFX_TAG    output tag
  SFX_MODE   'canonical' -> config_mode='canonical' ; anything else -> dev-shell (config_mode=None)
  SFX_BAL    '1' -> balanced sibling (RL_PVC2=1 RL_LEGE=0 RL_LEGF=0); anything else -> priced board
  SFX_ENV    JSON dict of extra env overrides (the dial)
  SFX_OUT    output prefix (writes <prefix>.stdout/.stderr/.meta.json and copies the board)
"""
import os, sys, json, importlib.util, time, shutil

REPO = os.environ['SFX_REPO']
TAG  = os.environ.get('SFX_TAG', 'x')
MODE = os.environ.get('SFX_MODE', 'dev')
BAL  = os.environ.get('SFX_BAL', '0') == '1'
OVER = json.loads(os.environ.get('SFX_ENV', '{}'))
OUT  = os.environ['SFX_OUT']

# DISCLOSED, exactly as PREREG_D8 §3 disclosed it: tools/build_lock.sh exports RL_BUILD_LOCK_HELD,
# and config_manifest.enforce() rejects any unknown RL_-prefixed var as a model override, so a
# canonical-mode build launched from inside the lock HALTS. Drop it from the CHILD build's
# environment only; the lock itself is still held by the parent shell's fd.
os.environ.pop('RL_BUILD_LOCK_HELD', None)

spec = importlib.util.spec_from_file_location(
    'fvb_sfx', os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'test_fv_provenance.py'))
m = importlib.util.module_from_spec(spec); sys.modules['fvb_sfx'] = m; spec.loader.exec_module(m)
assert os.path.abspath(m.REPO) == os.path.abspath(REPO), 'builder resolved REPO %s != %s' % (m.REPO, REPO)

t = time.time()
res = m._run_build(OVER, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'),
                   config_mode=('canonical' if MODE == 'canonical' else None), balanced=BAL)
el = time.time() - t
open(OUT + '.stdout', 'w').write(res.get('stdout') or '')
open(OUT + '.stderr', 'w').write(res.get('stderr') or '')
meta = {'tag': TAG, 'mode': MODE, 'balanced': BAL, 'overrides': OVER, 'rc': res.get('rc'),
        'board_md5': res.get('board_md5'), 'elapsed_s': round(el, 1)}
if res.get('board_path'):
    shutil.copyfile(res['board_path'], OUT + '.board.json')
open(OUT + '.meta.json', 'w').write(json.dumps(meta, indent=2))
print('SFX %-12s mode=%-9s bal=%-5s rc=%s board_md5=%s  (%.1fs)'
      % (TAG, MODE, BAL, res.get('rc'), res.get('board_md5'), el))
base = res.get('base')
if base and os.path.isdir(base):
    shutil.rmtree(base, ignore_errors=True)
    print('  staging removed: %s' % base)
