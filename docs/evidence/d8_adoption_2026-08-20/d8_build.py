#!/usr/bin/env python3
"""ORDER D8 board build driver. Uses the ACCEPTED disposable FV builder
(session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build) exactly as the
H3 repair seat did. Writes NOTHING under the repo; the staging tree is deleted after each run.

  D8REPO   the worktree root
  D8TAG    output tag
  D8MODE   'canonical' -> config_mode='canonical' ; anything else -> dev-shell (config_mode=None)
  D8ENV    JSON dict of extra env overrides (the dial)
  D8OUT    output prefix (writes <prefix>.stdout/.stderr/.meta.json and copies the board)
"""
import os, sys, json, importlib.util, time, shutil

REPO = os.environ['D8REPO']
TAG  = os.environ.get('D8TAG', 'x')
MODE = os.environ.get('D8MODE', 'dev')
OVER = json.loads(os.environ.get('D8ENV', '{}'))
OUT  = os.environ['D8OUT']

# PREREG_D8 §3, disclosed: tools/build_lock.sh exports RL_BUILD_LOCK_HELD, and
# config_manifest.enforce() rejects any unknown RL_-prefixed var as a model override, so a
# canonical-mode build launched from inside the lock HALTS. Drop it from the CHILD build's
# environment only; the lock itself is still held by the parent shell's fd.
os.environ.pop('RL_BUILD_LOCK_HELD', None)

spec = importlib.util.spec_from_file_location(
    'fvb_d8', os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'test_fv_provenance.py'))
m = importlib.util.module_from_spec(spec); sys.modules['fvb_d8'] = m; spec.loader.exec_module(m)
assert os.path.abspath(m.REPO) == os.path.abspath(REPO), 'builder resolved REPO %s != %s' % (m.REPO, REPO)

t = time.time()
res = m._run_build(OVER, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'),
                   config_mode=('canonical' if MODE == 'canonical' else None), balanced=False)
el = time.time() - t
open(OUT + '.stdout', 'w').write(res.get('stdout') or '')
open(OUT + '.stderr', 'w').write(res.get('stderr') or '')
meta = {'tag': TAG, 'mode': MODE, 'overrides': OVER, 'rc': res.get('rc'),
        'board_md5': res.get('board_md5'), 'elapsed_s': round(el, 1)}
if res.get('board_path'):
    shutil.copyfile(res['board_path'], OUT + '.board.json')
    # ADOPTION SEAT ADDITION (the ONLY change to the byte-carried D8 driver): the .srcmd5 sidecar the
    # build writes beside the board is preserved too, so the landing installs the pipeline's OWN
    # sidecar rather than one this seat hand-composed.
    _sc = res['board_path'] + '.srcmd5'
    if os.path.exists(_sc):
        shutil.copyfile(_sc, OUT + '.board.json.srcmd5')
open(OUT + '.meta.json', 'w').write(json.dumps(meta, indent=2))
print('D8 %-10s mode=%-9s rc=%s board_md5=%s  (%.1fs)' % (TAG, MODE, res.get('rc'), res.get('board_md5'), el))
base = res.get('base')
if base and os.path.isdir(base):
    shutil.rmtree(base, ignore_errors=True)
    print('  staging removed: %s' % base)
