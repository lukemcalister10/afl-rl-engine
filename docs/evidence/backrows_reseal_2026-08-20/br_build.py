#!/usr/bin/env python3
"""BACK-ROWS REPAIR board build driver.

CARRIED BYTE-FOR-BYTE IN LOGIC from docs/evidence/r23_advance_2026-08-20/recut_build.py (itself the
D8 adaptation of the H3 repair seat's driver). Only this docstring and the env-var prefix differ.

Uses the ACCEPTED disposable FV builder
(session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build) — the FUNCTION is
imported and called; the fv-provenance SUITE is never run on this box.
Writes NOTHING under the repo; the staging tree is deleted after each run.

  BRREPO   the tree root to build from
  BRTAG    output tag
  BRMODE   'canonical' -> config_mode='canonical' ; anything else -> dev-shell (config_mode=None)
  BRENV    JSON dict of extra env overrides
  BROUT    output prefix (writes <prefix>.stdout/.stderr/.meta.json and copies the board + sidecar)
"""
import os, sys, json, importlib.util, time, shutil

REPO = os.environ['BRREPO']
TAG  = os.environ.get('BRTAG', 'x')
MODE = os.environ.get('BRMODE', 'dev')
OVER = json.loads(os.environ.get('BRENV', '{}'))
OUT  = os.environ['BROUT']

# tools/build_lock.sh exports RL_BUILD_LOCK_HELD, and config_manifest.enforce() rejects any unknown
# RL_-prefixed var as a model override, so a canonical-mode build launched from inside the lock
# HALTS. Drop it from the CHILD build's environment only; the lock is still held by the parent's fd.
os.environ.pop('RL_BUILD_LOCK_HELD', None)

spec = importlib.util.spec_from_file_location(
    'fvb_br', os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'test_fv_provenance.py'))
m = importlib.util.module_from_spec(spec); sys.modules['fvb_br'] = m; spec.loader.exec_module(m)
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
    _sc = res['board_path'] + '.srcmd5'
    if os.path.exists(_sc):
        shutil.copyfile(_sc, OUT + '.board.json.srcmd5')
open(OUT + '.meta.json', 'w').write(json.dumps(meta, indent=2))
print('BR %-12s mode=%-9s rc=%s board_md5=%s  (%.1fs)' % (TAG, MODE, res.get('rc'), res.get('board_md5'), el))
base = res.get('base')
if base and os.path.isdir(base):
    shutil.rmtree(base, ignore_errors=True)
    print('  staging removed: %s' % base)
