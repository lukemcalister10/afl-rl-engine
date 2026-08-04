#!/usr/bin/env python3
"""#306 L-C — RECORD THE LANE'S EXPECTED FITTED BYTES, keyed on its DECLARED INPUTS.

WHAT THIS IS FOR
  L-C requires the redesigned fit to be asserted byte-identical ACROSS MACHINES, with the assert
  living IN THE LANE so a future container cannot silently re-introduce the divergence. The assert
  itself is wired into `_build_v0_curve`; this emitter records what it compares against.

  THE KEY IS THE DECLARED INPUTS: basis artifact md5 · anchor payload identity · roster composition
  digest. If all three match a recorded run, the fitted bytes MUST match it too — any difference is
  the BOX. If they do not match, the assert reports INAPPLICABLE and stays silent about box class:
  a legitimate re-basis must never read as a green cross-host proof. That is the vacuity this leg
  exists to refuse, and it is why the record is keyed rather than a bare pin.

  IT COMPARES FITTED OUTPUT BYTES. Never a library version, never a pin hash, never a CPU string.
  "The pin was never the guard" — item 380's OpenBLAS byte-pin passed on both hosts while the
  dispatch tier differed, and this job re-measured exactly that on 2026-08-04.

    python3 emit_lane_expectation.py        # run on a box whose N35 fit-path assert has PASSED
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
OUT = os.path.join(HERE, 'lane_expectation.json')

PROBE = '''
import io, contextlib, json, os
os.environ['RL_V0SURF_REFIT'] = '1'; os.environ['RL_V0_LENS'] = '1'
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
M = g['_V0CURVE_META']
print(json.dumps({'lc': M.get('_lc'), 'basis': M.get('_lens_basis'), 'la': M.get('_la'),
                  'applied_rows': M.get('_la_applied_rows')}))
'''


def main():
    p = subprocess.run([sys.executable, '-c', PROBE], capture_output=True, text=True,
                       cwd='/home/claude/rl_workspace/rl_after')
    if p.returncode != 0:
        raise SystemExit('HALT: the lane probe failed.\n%s' % p.stderr[-3000:])
    got = json.loads(p.stdout.strip().splitlines()[-1])
    lc = got['lc']
    if not lc:
        raise SystemExit('HALT: the lane reported no L-C block — is RL_V0_LENS=1 and the basis present?')

    prev = {}
    if os.path.exists(OUT):
        prev = json.load(open(OUT)).get('expectations', {})
    key = lc['key']
    if key in prev and prev[key]['lens_digest'] != lc['lens_digest']:
        raise SystemExit(
            'HALT: this box disagrees with the RECORDED expectation for identical declared inputs.\n'
            '  key %s\n  recorded %s\n  here     %s\n'
            '  That is exactly the cross-host divergence L-C exists to catch — record it as a '
            'MEASURED DIVERGENCE, do not overwrite the expectation.' % (key, prev[key]['lens_digest'], lc['lens_digest']))

    prev[key] = {'lens_digest': lc['lens_digest'],
                 'basis_md5': got['basis']['md5'], 'basis_rows': got['basis']['rows'],
                 'applied_rows': got['applied_rows'],
                 'constants': {k: got['la'][k] for k in ('B', 'tol', 'h_pick', 'h_age', 'k_conf')
                               if k in (got['la'] or {})},
                 'recorded_by': 'exec_306_zlaarm'}
    doc = {'_what': 'L-C: the lane\'s expected FITTED OUTPUT BYTES, keyed on its declared inputs',
           '_compares': 'fitted output bytes — never a version pin, never a CPU string',
           '_key': 'basis md5 (12) | anchor payload (8) | roster composition digest (12)',
           '_inapplicable_is_not_green': 'if the declared inputs do not match a recorded run the assert '
                                         'reports INAPPLICABLE and says nothing about box class',
           'expectations': prev}
    with open(OUT, 'w') as f:
        json.dump(doc, f, indent=1, sort_keys=True); f.write('\n')
    print('LANE EXPECTATION RECORDED')
    print('  key          %s' % key)
    print('  lens digest  %s' % lc['lens_digest'])
    print('  state on this box: %s' % lc['state'])
    print('  basis %s · %d basis rows · %d applied rows'
          % (got['basis']['md5'][:8], got['basis']['rows'], got['applied_rows']))
    return 0


if __name__ == '__main__':
    sys.exit(main())
