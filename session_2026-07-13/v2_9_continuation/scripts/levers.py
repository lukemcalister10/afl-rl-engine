#!/usr/bin/env python3
"""SINGLE SOURCE of the v2.9 lever source-patches (used by both board passes and matrix builds).

Each patch is asserted present exactly once before it is applied (halt-not-warn). The patches
faithfully replicate the inherited, audited single-lever sims:
  L1  = l1_adopt_sim.py option-(b) recipe: swap the ev-channel basis _PVC0 to the L1b SMOOTHED
        derived curve (pin 3000) + rebuild V0 guard / V0 curve / RUC ceiling grid. Injected as a
        LOAD-TIME source block right after draftval is rebound to _PVC0 (_merged_recover.py:992).
  L4  = l4_pool_sim.py: add `or type=='MSD'` to the training-pool filter (MSD pool exclusion).
  L2  = run_discount_sweep.sh: LENS['bal'] 0.15 -> 0.14 (dial 14), in rl_model.py.
  L3  = l3_age_sim.py: replace flat S_M1=0.46 in _coreM1's proven-riser up-branch with the l7hinr
        s(age) breakout-persistence slope (clip(s_age(age),0,1)); _S_AGE injected at module level.
Not source-patched here (argued in the gate report):
  L5  = trio pickless — cohort-neutral for the ND/RD B1 gate (trio are SSP, not cohort members).
  L7  = numeraire ÷1.0524 — a uniform scalar; per-cohort indexing (yr1=100) is scale-invariant.
"""
import os

REPO = "/home/user/afl-rl-engine"
SMOOTHED = os.path.join(REPO, "session_2026-07-12/v2_9_candidate/out/pvc_curve_smoothed.json")

# --- L4: MSD pool exclusion (l4_pool_sim.py) ---
L4_FILTER = "if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')): continue"
L4_PATCH = "if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')) or p.get('type')=='MSD': continue"

# --- L3: s(age) up-branch (l3_age_sim.py) ---
L3_ANCHOR = "TOL_M1=5.0; G_ADQ=12; WIN=2; S_M1=0.46"
L3_SAGE = (
    L3_ANCHOR
    + "\n_L3_AX=[20,21,22,23,24,25,26,27,28,29,30,31]"
    + "\n_L3_AY=[0.915376,0.860795,0.789170,0.700837,0.599107,0.489589,0.377802,0.265858,0.150620,0.026915,0.0,0.0]"
    + "\ndef _S_AGE(a): return float(np.clip(np.interp(a,_L3_AX,_L3_AY),0.0,1.0)) if a is not None else 0.46"
)
L3_ORIG = "if Lc>=Lo: return (Lo+S_M1*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo"
L3_PATCH = "if Lc>=Lo: return (Lo+_S_AGE(cp._age_asof(p,Y))*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo"

# --- L2: dial 14 (rl_model.py) ---
L2_LENS = "LENS={'now':0.34,'bal':0.15,'fut':0.05}"
L2_PATCH = "LENS={'now':0.34,'bal':0.14,'fut':0.05}"

# --- L1: _PVC0 ev-channel swap + V0/RUC rebuild (l1_adopt_sim.py option-b), load-time injection ---
L1_ANCHOR = "def draftval(p): return float(_PVC0[min(MA.effpk(p),cp.KMAX)])   # rebind: runtime cap/scaffold callers read the FROZEN curve"
L1_INJECT = (
    L1_ANCHOR
    + "\n# ===== L1(b) candidate (v2.9): swap ev-channel basis _PVC0 to the smoothed derived curve (pin 3000)"
    + "\n#       + rebuild V0 guard / V0 curve / RUC ceiling grid — verbatim the l1_adopt_sim option-b recipe."
    + "\nimport json as _l1j"
    + "\n_L1CURVE={int(_k):int(_v) for _k,_v in _l1j.load(open(%r)).items()}" % SMOOTHED
    + "\n_PVC0.clear(); _PVC0.update(_L1CURVE)"
    + "\n_V0C.clear(); _V0U.clear(); _V0GUARD.clear(); _RUCCEIL.pop('grid',None)"
    + "\n_build_v0_guard(); _V0CURVE.clear(); _build_v0_curve()"
    + "\nMA._pe_clear()"
)


def patch(levers, mr, rlm):
    """Apply the named levers to the engine source strings. Returns (mr, rlm). Asserts each anchor
    is present exactly once (halt-not-warn). `levers` = iterable or comma-string of {L1,L2,L3,L4}."""
    if isinstance(levers, str):
        ls = set(x.strip() for x in levers.split(",") if x.strip())
    else:
        ls = set(levers)
    unknown = ls - {"L1", "L2", "L3", "L4"}
    assert not unknown, "unknown levers: %s" % unknown
    if "L1" in ls:
        assert mr.count(L1_ANCHOR) == 1, "L1 anchor (draftval rebind) not found exactly once"
        assert os.path.exists(SMOOTHED), "L1 smoothed curve missing: %s" % SMOOTHED
        mr = mr.replace(L1_ANCHOR, L1_INJECT)
    if "L4" in ls:
        assert mr.count(L4_FILTER) == 1, "L4 pool filter not found exactly once"
        mr = mr.replace(L4_FILTER, L4_PATCH)
    if "L3" in ls:
        assert mr.count(L3_ANCHOR) == 1, "L3 anchor (S_M1 def) not found exactly once"
        assert mr.count(L3_ORIG) == 1, "L3 up-branch not found exactly once"
        mr = mr.replace(L3_ANCHOR, L3_SAGE).replace(L3_ORIG, L3_PATCH)
    if "L2" in ls:
        assert rlm.count(L2_LENS) == 1, "L2 LENS literal not found exactly once"
        rlm = rlm.replace(L2_LENS, L2_PATCH)
    return mr, rlm
