#!/usr/bin/env python3
"""tools/landing/_build_child.py — the board build, IN A CHILD PROCESS, out of the lock's env.

CARRIED IN LOGIC from `docs/evidence/backrows_reseal_2026-08-20/br_build.py` (itself the D8 seat's
driver, itself the H3 repair seat's). Only the env-var names and the caller differ, and the reason it
stays a separate process is written in its own header there:

    tools/build_lock.sh exports RL_BUILD_LOCK_HELD, and config_manifest.enforce() rejects any unknown
    RL_-prefixed var as a model override, so a canonical-mode build launched from inside the lock
    HALTS. Drop it from the CHILD build's environment only; the lock is still held by the parent's fd.

Uses the ACCEPTED disposable FV builder — the FUNCTION
`session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build` is imported and called.
THE FV-PROVENANCE SUITE IS NEVER RUN (it overwrites a shared pickle; PLAN_v6 2a.1). Writes nothing
under the repo; the staging tree is deleted after each run.

Argv: <repo_root> <tag> <mode:dev|canonical> <out_prefix> <env_overrides_json>
"""
import importlib.util
import json
import os
import shutil
import sys
import time

REPO, TAG, MODE, OUT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
OVER = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}

os.environ.pop('RL_BUILD_LOCK_HELD', None)

spec = importlib.util.spec_from_file_location(
    'fvb_landing', os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation',
                                'test_fv_provenance.py'))
m = importlib.util.module_from_spec(spec)
sys.modules['fvb_landing'] = m
spec.loader.exec_module(m)
if os.path.abspath(m.REPO) != os.path.abspath(REPO):
    raise SystemExit('builder resolved REPO %s != %s' % (m.REPO, REPO))

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
    sc = res['board_path'] + '.srcmd5'
    if os.path.exists(sc):
        shutil.copyfile(sc, OUT + '.board.json.srcmd5')
        meta['sidecar'] = True
open(OUT + '.meta.json', 'w').write(json.dumps(meta, indent=2))
print('BUILD %-12s mode=%-9s rc=%s board_md5=%s  (%.1fs)'
      % (TAG, MODE, res.get('rc'), res.get('board_md5'), el))
base = res.get('base')
if base and os.path.isdir(base):
    shutil.rmtree(base, ignore_errors=True)
    print('  staging removed: %s' % base)
