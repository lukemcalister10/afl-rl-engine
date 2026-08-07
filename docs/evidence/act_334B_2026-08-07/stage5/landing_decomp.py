"""Where the yr1 landing comes from — the decomposition, on the two matrices, ND 1-64 2004-2022."""
import os, sys, json, importlib.util
import numpy as np
REPO = os.environ['RL_REPO']
EV = REPO + '/docs/evidence/act_334B_2026-08-07'
S5 = EV + '/stage5'
spec = importlib.util.spec_from_file_location('harness_pvc', S5 + '/noarb/harness_pvc_REPINNED_pass3.py')
H = importlib.util.module_from_spec(spec); sys.modules['harness_pvc'] = H; spec.loader.exec_module(H)

def load(path):
    meta = json.load(open(path))['meta']
    old = (H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N)
    H.EXPECT_STORE = meta['store_md5']; H.EXPECT_V0SURF = meta['v0surf_sig'][:12]
    m, ND = H.load_matrix(path)
    H.EXPECT_N = len(ND)
    H.EXPECT_STORE, H.EXPECT_V0SURF, H.EXPECT_N = old
    return {r['key']: r for r in ND}

A = load(EV + '/stage4_amend1/noarb/per_entrant_338_stage4a1.json')
B = load(S5 + '/noarb/per_entrant_338_stage5.json')
keys = sorted(set(A) & set(B))
print('ND cohort n =', len(keys))

def v1(r): return float((r.get('vpath') or [0])[0] or 0.0)
def v0(r): return float(r['v0'])

# sub-populations on the BASELINE reading (never on the landed one — the split must not move)
def split(k):
    r = A[k]
    g1 = r['games_by']['1'] if isinstance(r['games_by'], dict) else r['games_by'][0]
    return int(g1)

GRP = {'zero games by yr1': lambda k: split(k) == 0,
       'quiet starter 1-5': lambda k: 1 <= split(k) <= 5,
       'played 6+ by yr1  ': lambda k: split(k) >= 6}
print()
print('%-20s %6s %10s %10s %10s %10s %10s %10s'
      % ('sub-population', 'n', 'sum v0', 'share v0', 'yr1 BASE', 'yr1 LAND', 'contrib B', 'contrib L'))
S0 = sum(v0(A[k]) for k in keys)
for nm, f in GRP.items():
    ks = [k for k in keys if f(k)]
    s0 = sum(v0(A[k]) for k in ks)
    a1 = sum(v1(A[k]) for k in ks); b1 = sum(v1(B[k]) for k in ks)
    print('%-20s %6d %10.0f %10.4f %10.4f %10.4f %10.4f %10.4f'
          % (nm, len(ks), s0, s0 / S0, a1 / s0 if s0 else 0, b1 / s0 if s0 else 0, a1 / S0, b1 / S0))
tot_a = sum(v1(A[k]) for k in keys); tot_b = sum(v1(B[k]) for k in keys)
print('%-20s %6d %10.0f %10.4f %10.4f %10.4f %10.4f %10.4f'
      % ('WHOLE COHORT', len(keys), S0, 1.0, tot_a / S0, tot_b / S0, tot_a / S0, tot_b / S0))
print()
print('to reach yr1 == 1.0000 the cohort needs another %.1f value points (%.4f of sum v0)'
      % (S0 - tot_b, (S0 - tot_b) / S0))
qk = [k for k in keys if 1 <= split(k) <= 5]
s0q = sum(v0(A[k]) for k in qk)
print('  if taken ENTIRELY from the quiet starters (share %.4f) they would have to land at %.4f of entry'
      % (s0q / S0, (sum(v1(B[k]) for k in qk) + (S0 - tot_b)) / s0q))
zk = [k for k in keys if split(k) == 0]
s0z = sum(v0(A[k]) for k in zk)
print('  if taken ENTIRELY from the zero-games class (share %.4f) they would have to land at %.4f of entry'
      % (s0z / S0, (sum(v1(B[k]) for k in zk) + (S0 - tot_b)) / s0z))

# below-own-pick counts
print()
for nm, M in (('BASELINE', A), ('LANDED  ', B)):
    bo = [k for k in keys if v1(M[k]) < v0(M[k])]
    sh = [(v0(M[k]) - v1(M[k])) / v0(M[k]) for k in bo]
    print('%s below-own-entry-level at yr1 : %4d of %d   mean shortfall %.4f  total shortfall %.0f'
          % (nm, len(bo), len(keys), float(np.mean(sh)), sum(v0(M[k]) - v1(M[k]) for k in bo)))
