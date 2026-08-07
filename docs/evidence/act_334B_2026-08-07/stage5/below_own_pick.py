"""#334 stage B / STAGE 5 — THE BELOW-OWN-PICK COUNT, BOTH POPULATIONS (gate 1's second limb).

  (a) THE MATRIX POPULATION — the 1197 ND 2004-2022 entrants of the no-arb book, at their YEAR-1
      evaluation, against their own entry level v0. This is the historical statement.
  (b) THE CURRENT BOARD — every live ND 1-64 row, against the value of HIS OWN PICK on the installed
      ladder (pvc_curve_v2.json, payload 18203822). This is the statement the owner reads.

Both counts and both mean shortfalls, before and after. READ-ONLY.
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

say('=' * 104)
say('#334 stage B / STAGE 5 — BELOW-OWN-PICK, BOTH POPULATIONS (gate 1, second limb)')
say('=' * 104)
say('')
say('(a) THE MATRIX POPULATION — 1197 ND 2004-2022 entrants at their YEAR-1 evaluation vs their own v0')
say('    %-10s %8s %10s %14s %16s' % ('arm', 'n below', 'of', 'mean shortfall', 'total shortfall'))
RES = {}
for nm, M in (('BASELINE', A), ('LANDED', B)):
    def v1(r):
        vp = r.get('vpath') or []
        return float(vp[0] or 0.0) if vp else 0.0
    bo = [k for k in keys if v1(M[k]) < float(M[k]['v0'])]
    sh = [(float(M[k]['v0']) - v1(M[k])) / float(M[k]['v0']) for k in bo]
    tot = sum(float(M[k]['v0']) - v1(M[k]) for k in bo)
    say('    %-10s %8d %10d %13.4f%% %16.0f' % (nm, len(bo), len(keys), 100 * float(np.mean(sh)), tot))
    RES['matrix_' + nm] = dict(n_below=len(bo), n=len(keys), mean_shortfall=float(np.mean(sh)), total=tot)
say('    MOVE: %+d players (%s)' % (RES['matrix_LANDED']['n_below'] - RES['matrix_BASELINE']['n_below'],
                                    'FALLS — gate limb met' if RES['matrix_LANDED']['n_below'] <
                                    RES['matrix_BASELINE']['n_below'] else 'does not fall'))
say('')

# ---- (b) the current board vs the installed ladder ------------------------------------------------
LAD = json.load(open(REPO + '/engine/rl_after/pvc_curve_v2.json'))['curve']
def rows(d):
    r = d['active'] if isinstance(d, dict) and 'active' in d else d
    return list(r.values()) if isinstance(r, dict) else r
OLD = {p['key']: p for p in rows(json.load(open(os.environ['RL_OLDBOARD']))) if p.get('v') is not None}
NEW = {p['key']: p for p in rows(json.load(open(os.environ['RL_NEWBOARDFILE']))) if p.get('v') is not None}

# the pick each board row entered on — read from the walk-forward matrix (the engine's own effpk)
PK = {}
for k in set(A):
    if A[k].get('pick') and 1 <= A[k]['pick'] <= 64: PK[k] = A[k]['pick']
# and from the emitted stage-5 matrix for rows the baseline matrix does not carry
MX = json.load(open(S5 + '/noarb/per_entrant_338_stage5.json'))['recs']
for r in MX:
    if r.get('type') == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64:
        PK.setdefault(r['key'], r['pick'])

say('(b) THE CURRENT BOARD — live ND pick-1-64 rows vs the value of THEIR OWN PICK on the installed')
say('    ladder pvc_curve_v2.json (payload 18203822, pick 1 = 3000)')
say('    %-10s %8s %10s %14s %16s' % ('arm', 'n below', 'of', 'mean shortfall', 'total shortfall'))
pop = sorted(k for k in set(OLD) & set(NEW) if k in PK)
for nm, M in (('BASELINE', OLD), ('LANDED', NEW)):
    bo = []; sh = []; tot = 0.0
    for k in pop:
        pv = float(LAD[str(PK[k])])
        if M[k]['v'] < pv:
            bo.append(k); sh.append((pv - M[k]['v']) / pv); tot += pv - M[k]['v']
    say('    %-10s %8d %10d %13.4f%% %16.0f' % (nm, len(bo), len(pop), 100 * float(np.mean(sh)), tot))
    RES['board_' + nm] = dict(n_below=len(bo), n=len(pop), mean_shortfall=float(np.mean(sh)), total=tot)
say('    MOVE: %+d players (%s)' % (RES['board_LANDED']['n_below'] - RES['board_BASELINE']['n_below'],
                                    'FALLS — gate limb met' if RES['board_LANDED']['n_below'] <
                                    RES['board_BASELINE']['n_below'] else 'does not fall'))
open(os.path.join(S5, 'BELOW_OWN_PICK.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(RES, open(os.path.join(S5, 'below_own_pick.json'), 'w'), indent=1)
