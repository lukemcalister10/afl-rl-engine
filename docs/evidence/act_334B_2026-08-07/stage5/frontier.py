"""THE HONEST FRONTIER — the MEASURED discounted future of each yr1 sub-population, on exactly the
ND 1-64 / 2004-2022 no-arb cohort, read off the FROZEN baseline matrix. This is the number the landing
is entitled to reach and no more."""
import os, sys, json, importlib.util
import numpy as np
REPO = os.environ['RL_REPO']
EV = REPO + '/docs/evidence/act_334B_2026-08-07'
S5 = EV + '/stage5'
spec = importlib.util.spec_from_file_location('harness_pvc', S5 + '/noarb/harness_pvc_REPINNED_pass3.py')
H = importlib.util.module_from_spec(spec); sys.modules['harness_pvc'] = H; spec.loader.exec_module(H)
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
DISC = 1.0939
def g1(r): return int(r['games_by']['1'])
def vN(r, n):
    vp = r.get('vpath') or []
    return float(vp[n - 1] or 0.0) if n - 1 < len(vp) else 0.0

for KM in (4, 3, 5):
    print('\n===== horizon K = %d  (F = mean_k v(yr1+k)/%.4f^k, busts/out-of-window = 0) =====' % (KM, DISC))
    print('%-20s %6s %10s %10s %10s %10s %10s'
          % ('sub-population', 'n', 'yr1 BASE', 'yr1 LAND', 'MEASURED F', 'land/F', 'headroom'))
    for nm, f in (('zero games by yr1', lambda k: g1(A[k]) == 0),
                  ('quiet starter 1-5', lambda k: 1 <= g1(A[k]) <= 5),
                  ('played 6+ by yr1  ', lambda k: g1(A[k]) >= 6)):
        ks = [k for k in keys if f(k)]
        # horizon-eligible: the class must have been able to reach yr1+k
        s0 = 0.0; sF = 0.0; sa = 0.0; sb = 0.0
        for k in ks:
            r = A[k]; C = r['year']
            kk = [j for j in range(1, KM + 1) if C + 1 + j <= 2026]
            if not kk: continue
            F = float(np.mean([vN(r, 1 + j) / DISC ** j for j in kk]))
            s0 += r['v0']; sF += F; sa += vN(A[k], 1); sb += vN(B[k], 1)
        print('%-20s %6d %10.4f %10.4f %10.4f %10.4f %+10.4f'
              % (nm, len(ks), sa / s0, sb / s0, sF / s0, (sb / s0) / (sF / s0), (sF - sb) / s0))
    # whole cohort
    s0 = sF = sa = sb = 0.0
    for k in keys:
        r = A[k]; C = r['year']
        kk = [j for j in range(1, KM + 1) if C + 1 + j <= 2026]
        if not kk: continue
        F = float(np.mean([vN(r, 1 + j) / DISC ** j for j in kk]))
        s0 += r['v0']; sF += F; sa += vN(A[k], 1); sb += vN(B[k], 1)
    print('%-20s %6d %10.4f %10.4f %10.4f %10.4f %+10.4f'
          % ('WHOLE COHORT', len(keys), sa / s0, sb / s0, sF / s0, (sb / s0) / (sF / s0), (sF - sb) / s0))
