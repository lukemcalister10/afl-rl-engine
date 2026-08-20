#!/usr/bin/env python3
"""tools/build_twice_determinism.py — TWO BARE BUILDS, BYTE-IDENTICAL.

    tools/build_lock.sh run determinism -- python3 tools/build_twice_determinism.py [--json PATH]

    exit 0 = the two builds produced the same board bytes; 1 = they did not.

This is the M1a adopted-but-never-built determinism leg (PLAN_v6 1f), promoted out of per-act
scratch drivers into a named tool (3d's rule, applied early because a determinism proof that lives
in one act's evidence directory is a proof nobody can re-run).

WHAT IT ASSERTS, and what it deliberately does not. It asserts SAME TREE -> SAME BOARD, twice in a
row, on this box. It does NOT assert cross-machine reproduction: the record's cross-machine leg is
DEFERRED (no second architecture; owner ruling 2026-07-22) and this tool does not quietly claim it.
It also reports, without gating on it, whether those bytes equal the PINNED board — a tree whose
two builds agree with each other but not with data/expected_boot.json is a different and much
louder fact, and the caller is told rather than reded at, because the pin can legitimately lag a
work-in-progress tree while determinism still holds.

MECHANICS, carried from the accepted driver rather than reinvented: the builds go through
`session_2026-07-20/fv_provenance_remediation/test_fv_provenance._run_build`, the same function the
R23 advance and the back-rows repair built through, staging OUTSIDE the repo and writing nothing
under it. PYTHONHASHSEED=0 and single-threaded BLAS are set here because a determinism claim made
without pinning them is a claim about luck.

THE LOCK IS NOT OPTIONAL AND IS NOT TAKEN HERE. /home/claude/rl_workspace is a single shared
mutable workspace; two overlapping engine acts produce results that look clean and are void. This
tool REFUSES TO RUN unless it can see the lock is held (RL_BUILD_LOCK_HELD), rather than taking the
lock itself — taking it would make it easy to nest inside a caller that already holds it, which
flock handles badly and which hides the ownership question. Run it through
`tools/build_lock.sh run <tag> -- ...`.
"""

import argparse
import importlib.util
import json
import os
import shutil
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_builder(root):
    path = os.path.join(root, 'session_2026-07-20', 'fv_provenance_remediation',
                        'test_fv_provenance.py')
    spec = importlib.util.spec_from_file_location('_fvb_determinism', path)
    m = importlib.util.module_from_spec(spec)
    sys.modules['_fvb_determinism'] = m
    spec.loader.exec_module(m)
    if os.path.abspath(m.REPO) != os.path.abspath(root):
        raise SystemExit('builder resolved REPO %s != %s — refusing to certify a tree it is not '
                         'building' % (m.REPO, root))
    return m


def build_once(builder, root, tag):
    """One bare build. -> dict(tag, rc, board_md5, elapsed_s)."""
    t0 = time.time()
    res = builder._run_build({}, rl_fv=os.path.join(root, 'engine', 'forward_valuation'),
                             config_mode=None, balanced=False)
    el = time.time() - t0
    base = res.get('base')
    if base and os.path.isdir(base):
        shutil.rmtree(base, ignore_errors=True)
    return {'tag': tag, 'rc': res.get('rc'), 'board_md5': res.get('board_md5'),
            'elapsed_s': round(el, 1)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--root', default=os.environ.get('RL_REPO') or ROOT)
    ap.add_argument('--json', dest='json_path', default=None)
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)

    if not os.environ.get('RL_BUILD_LOCK_HELD'):
        print('REFUSED: the build lock is not held. Run me as:')
        print('  tools/build_lock.sh run determinism -- python3 tools/build_twice_determinism.py')
        return 2

    os.environ.setdefault('PYTHONHASHSEED', '0')
    for v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        os.environ.setdefault(v, '1')

    builder = _load_builder(root)
    runs = [build_once(builder, root, 'A'), build_once(builder, root, 'B')]
    for r in runs:
        print('  build %s  rc=%s  board_md5=%s  (%.1fs)'
              % (r['tag'], r['rc'], r['board_md5'], r['elapsed_s']))

    pinned = None
    boot = os.path.join(root, 'data', 'expected_boot.json')
    if os.path.exists(boot):
        pinned = json.load(open(boot)).get('board')

    ok = (runs[0]['rc'] == 0 and runs[1]['rc'] == 0
          and runs[0]['board_md5'] and runs[0]['board_md5'] == runs[1]['board_md5'])
    same_as_pin = bool(pinned) and runs[0]['board_md5'] == pinned
    print('  pinned board (data/expected_boot.json): %s  -> builds %s the pin'
          % (pinned, 'MATCH' if same_as_pin else 'DO NOT match'))
    print('determinism: two bare builds are %s'
          % ('BYTE-IDENTICAL' if ok else 'NOT identical — this is a determinism failure'))

    if a.json_path:
        with open(a.json_path, 'w', encoding='utf-8') as fh:
            json.dump({'runs': runs, 'identical': ok, 'pinned_board': pinned,
                       'matches_pin': same_as_pin}, fh, indent=2, sort_keys=True)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
