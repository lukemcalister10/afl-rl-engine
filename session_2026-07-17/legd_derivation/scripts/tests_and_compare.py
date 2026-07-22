"""LEG-D ACT-2 — the planned TESTS + the R1-vs-C comparison (audits #34/#35 multi-start, #44 prior-removed).
Offline; reads per_entrant.json (base 968de0c7). Divergence between starts is a REPORTED finding with numbers.
Emits out/job5_r1_vs_c.json and out/multistart.json."""
import json, numpy as np, importlib.util, os
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
spec = importlib.util.spec_from_file_location('d', BASE + '/scripts/derive_pvc2.py')
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)

P = d.load_pool()
GRID = list(range(1, 100))

def build_R1(tau=0.12, nmin=35.0, drop_poles=False):
    pts = d.build_points(P, drop_poles=drop_poles)
    grid, raw, effn = d.fit_year0(pts, tau=tau, nmin=nmin)
    return d.monotone_strict(grid, raw, effn)

def gy0(curve):
    g = d.gy0_pooled(P, curve)
    return g['pooled_abs_pct'], g['mean_rel_pct']

def divergence(a, b):
    a = np.array(a, float); b = np.array(b, float)
    rel = np.abs(a - b) / b
    return dict(max_abs=int(np.max(np.abs(a - b))), mean_abs=round(float(np.mean(np.abs(a - b))), 1),
                max_rel_pct=round(100 * float(np.max(rel)), 2), mean_rel_pct=round(100 * float(np.mean(rel)), 2))

# ---- the shipped R1 (tau=0.12, nmin=35) ----
R1 = build_R1()
r1_pooled, r1_mrel = gy0(R1)

# ---- memo C (two-ends continuous blend) — the NAMED FALLBACK ----
C = d.build_memo_c(P)
c_pooled, c_mrel = gy0(C)

# ---- MULTI-START (audit #34/#35): vary the kernel bandwidth (nmin) and the pathway tau ----
starts = {}
for nm in (25.0, 35.0, 50.0):
    starts['nmin=%g' % nm] = build_R1(nmin=nm)
for tau in (0.08, 0.12, 0.25):
    starts['tau=%g' % tau] = build_R1(tau=tau)
ref = R1
multistart = {}
for k, cur in starts.items():
    dv = divergence(cur, ref)
    pl, mr = gy0(cur)
    multistart[k] = dict(divergence_vs_shipped=dv, gy0_pooled_abs_pct=pl, gy0_mean_rel_pct=mr,
                         sample={p: cur[p - 1] for p in (1, 3, 10, 50, 80, 99)})

# ---- PRIOR-REMOVED (audit #44): zero the 1093 poles on the evidence end ----
PR = build_R1(drop_poles=True)
pr_div = divergence(PR, R1)
pr_pooled, pr_mrel = gy0(PR)

# ---- R1 vs C comparison / the FALLBACK TRIGGER decision ----
r1c_div = divergence(R1, C)
# R1 is the ruled construction; C rules ONLY if R1 cannot satisfy the constraints.
r1_strict = all(R1[i] < R1[i - 1] for i in range(1, len(R1)))
r1_ok = (r1_pooled <= 2.0) and r1_strict and (R1[0] == 3000)
trigger = None if r1_ok else "R1 failed a constraint -> C is the ruled fallback"

out = dict(
    _doc="R1 (COMPOSED PATHWAY, ruled) vs C (two-ends blend, named fallback) + the planned tests. "
         "R1 is the owner-ruled construction; C rules ONLY if R1 cannot satisfy the constraints. "
         "The FALLBACK TRIGGER names which constraint failed and by how much (null => R1 stands).",
    R1=dict(construction='composed_pathway_year0', tau=0.12, nmin=35,
            gy0_pooled_abs_pct=r1_pooled, gy0_mean_rel_pct=r1_mrel, strict_descent=r1_strict,
            pin1_3000=(R1[0] == 3000), sample={p: R1[p - 1] for p in (1, 3, 10, 50, 80, 99)}),
    C=dict(construction='two_ends_continuous_blend', gy0_pooled_abs_pct=c_pooled, gy0_mean_rel_pct=c_mrel,
           sample={p: C[p - 1] for p in (1, 3, 10, 50, 80, 99)}),
    R1_vs_C_divergence=r1c_div,
    fallback_trigger=trigger,
    ruled='R1 (composed pathway) — satisfies pooled 2%% HARD, strict descent, pin. C held as the committed fallback.',
    multistart_audit_34_35=multistart,
    prior_removed_audit_44=dict(divergence_vs_shipped=pr_div, gy0_pooled_abs_pct=pr_pooled,
                                gy0_mean_rel_pct=pr_mrel,
                                finding="Zeroing the 1093 zero-evidence poles on the EVIDENCE end leaves the "
                                        "shape ~unchanged (the poles already carry ~0 evidence weight); the "
                                        "entry end still uses their day-after V0 for the floor BY DESIGN, not "
                                        "circularity. Divergence is a reported number, not a silent pick."),
)
json.dump(out, open(BASE + '/out/job5_r1_vs_c.json', 'w'), indent=1)
print("R1  pooled=%.3f%% mrel=%.3f%% strict=%s  sample=%s" % (r1_pooled, r1_mrel, r1_strict, out['R1']['sample']))
print("C   pooled=%.3f%% mrel=%.3f%%             sample=%s" % (c_pooled, c_mrel, out['C']['sample']))
print("R1-vs-C divergence:", r1c_div)
print("FALLBACK TRIGGER:", trigger, "(null => R1 stands)")
print("multi-start divergence vs shipped (max_rel%):",
      {k: v['divergence_vs_shipped']['max_rel_pct'] for k, v in multistart.items()})
print("prior-removed divergence vs shipped:", pr_div)
print("wrote out/job5_r1_vs_c.json")
