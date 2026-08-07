"""#334 stage B / STAGE 5 — GATE 6: the CONVERGENCE statistic (restored as a gate by Addendum 2) and
the CROSS-BAND ORDERING (reported, never decreed — decreeing it would be tuning; round 2 located the
deficit in 21-64 and the taught surface either reproduces that or it does not).

Convergence: |yr1(picks 1-20) - yr1(picks 21-64)| must FALL from the baseline's 0.053.
Read on the committed no-arb convention off the two committed matrices. READ-ONLY.
"""
import os, sys, json, importlib.util
import numpy as np

REPO = os.environ['RL_REPO']
EV = REPO + '/docs/evidence/act_334B_2026-08-07'
S5 = EV + '/stage5'
spec = importlib.util.spec_from_file_location('harness_pvc', S5 + '/noarb/harness_pvc_REPINNED_pass3.py')
H = importlib.util.module_from_spec(spec); sys.modules['harness_pvc'] = H; spec.loader.exec_module(H)
L = []
def say(s=''): L.append(s); print(s)


def load(path):
    meta = json.load(open(path))['meta']
    o = (H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N)
    H.EXPECT_STORE = meta['store_md5']; H.EXPECT_V0SURF = meta['v0surf_sig'][:12]
    m, ND = H.load_matrix(path); H.EXPECT_N = len(ND)
    H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N = o
    return {r['key']: r for r in ND}


A = load(EV + '/stage4_amend1/noarb/per_entrant_338_stage4a1.json')
B = load(S5 + '/noarb/per_entrant_338_stage5.json')
keys = sorted(set(A) & set(B))


def yr1(M, ks):
    v = [float((M[k].get('vpath') or [0])[0] or 0.0) for k in ks]
    v0 = [float(M[k]['v0']) for k in ks]
    return float(np.mean(v)) / float(np.mean(v0))


BANDS = [('1-20', 1, 20), ('21-40', 21, 40), ('41-64', 41, 64), ('21-64', 21, 64)]
say('=' * 96)
say('#334 stage B / STAGE 5 — GATE 6: CONVERGENCE + the CROSS-BAND ORDERING (reported, not decreed)')
say('=' * 96)
say('')
say('  %-8s %6s %12s %12s %10s' % ('band', 'n', 'yr1 BASE', 'yr1 LANDED', 'move'))
say('  ' + '-' * 52)
out = {}
for nm, lo, hi in BANDS:
    ks = [k for k in keys if lo <= A[k]['pick'] <= hi]
    a, b = yr1(A, ks), yr1(B, ks)
    out[nm] = dict(n=len(ks), base=a, landed=b)
    say('  %-8s %6d %12.6f %12.6f %+10.6f' % (nm, len(ks), a, b, b - a))
ga = abs(out['1-20']['base'] - out['21-64']['base'])
gb = abs(out['1-20']['landed'] - out['21-64']['landed'])
say('')
say('  THE CONVERGENCE GATE (Addendum 2): |yr1(1-20) - yr1(21-64)| must FALL')
say('     baseline gap %.6f   ->   landed gap %.6f   (%+.6f, %.1f%% of the gap closed)'
    % (ga, gb, gb - ga, 100.0 * (ga - gb) / ga))
say('     the directive quotes this baseline gap as "0.053"; measured here at %.4f on the committed matrices.' % ga)
say('     GATE 6 (convergence) : %s' % ('PASS — the gap falls' if gb < ga else 'FAIL — the gap does not fall'))
say('')
say('  THE CROSS-BAND ORDERING — REPORTED, NOT DECREED. Reason, stated in line: decreeing an ordering')
say('  would be tuning the surface to a shape rather than teaching it from the measured futures. Round 2')
say('  located the deficit in 21-64; the taught surface either reproduces that or it does not, and this')
say('  is the reading:')
for nm in ('1-20', '21-40', '41-64'):
    say('     %-6s  yr1 %.6f -> %.6f   (%+.6f)' % (nm, out[nm]['base'], out[nm]['landed'],
                                                   out[nm]['landed'] - out[nm]['base']))
mv = {nm: out[nm]['landed'] - out[nm]['base'] for nm in ('1-20', '21-40', '41-64')}
say('     the lift is ordered %s — %s round 2\'s location of the deficit in the deeper picks.'
    % (' < '.join(k for k, _ in sorted(mv.items(), key=lambda z: z[1])),
       'CONSISTENT with' if mv['1-20'] < max(mv['21-40'], mv['41-64']) else 'NOT consistent with'))
open(os.path.join(S5, 'CONVERGENCE.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(dict(bands=out, gap_base=ga, gap_landed=gb, pass_=bool(gb < ga)),
          open(os.path.join(S5, 'convergence.json'), 'w'), indent=1)
