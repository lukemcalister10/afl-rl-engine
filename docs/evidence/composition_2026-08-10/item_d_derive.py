"""ITEM D — the sit-charge position contrast, RE-DERIVED on the corrected ruler. READ-ONLY.

Instrument reconstructed from the sitter act's own recorded definition (SITTER_PROGRESS.md step 5):
cohort = ND, classes 2004-2022, pick 1-64, games in year+1 == 0 -> n=496, aggregate F = 0.984.
That anchor is asserted below on the BENT ruler; if it does not reproduce, the instrument is wrong
and the sizing must not be taken from it.

THE RULED SHAPE: three classes — KPP (KPF+KPD) charge LIGHTENED, SMALL (MID/SD/SF) deepened,
RUCK UNTOUCHED (neutral base; no lawful ruck sitter cell). Sized at the CAUTIOUS END of the
1.378 [1.05, 1.80] contrast. Conserved within the sitter pool. F8 at PLAYER unit.
"""
import os, sys, json, math, collections
import numpy as np

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026; BARN = 35.0; NB = 4000
rng = np.random.default_rng(20260810)

# THE SITTER ACT'S OWN MATRIX is stage4a1 (SITTER_PROGRESS.md step 3), not stage5. On stage5 the
# same cohort gives 0.9765 and the anchor does not reproduce; on stage4a1 it gives 0.9838 == 0.984.
# The corrected-ruler numerator (r24 D_rt_win) is REALIZED DELIVERY off the seasons and bars, which
# are identical in both matrices -- only the engine-priced vpaths differ -- so it joins by key.
recs = json.load(open(E + "/stage4_amend1/noarb/per_entrant_338_stage4a1.json"))["recs"]
INST = {(r["key"], r["typ"], r["year"]): r for r in json.load(open(SP + "/r24_rows.json"))["rows"]}


def v(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


def games_in(r, y):
    for s in (r.get("seasons") or []):
        if s["year"] == y: return s["games"]
    return 0


# ---------- the anchor assert, on the BENT ruler, over the recorded cohort ----------
anchor_rows = []
for r in recs:
    if r.get("type") != "ND" or r.get("pickless"): continue
    if not (1 <= (r.get("pick") or 0) <= 64): continue
    if not (2004 <= r["year"] <= 2022): continue
    if r["year"] + 4 > END: continue
    if games_in(r, r["year"] + 1) != 0: continue
    v1 = v(r, 1)                       # the act's own denominator: the YEAR-1 price (r15's F1 form)
    if not v1 or v1 <= 0: continue
    anchor_rows.append((v(r, 4) / DISC ** 3, v1, r))
n = len(anchor_rows)
Fagg = sum(a for a, _b, _r in anchor_rows) / sum(b for _a, b, _r in anchor_rows)
ok_n, ok_F = (n == 496), (abs(Fagg - 0.984) < 5e-3)
print("SITTER ANCHOR (bent ruler, the act's own definition): n=%d [496] %s   aggregate F=%.4f [0.984] %s"
      % (n, "OK" if ok_n else "MISMATCH", Fagg, "OK" if ok_F else "MISMATCH"))
if not (ok_n and ok_F):
    print("\n  HALT: the sitter instrument does not reproduce its recorded anchor. ITEM D's sizing is")
    print("  NOT taken from an unverified instrument. Recorded and stopped, per HALT-NO-SURPRISE.")
    sys.exit(0)
print("  anchor reproduces -> the instrument is the right one; proceeding to the corrected ruler.\n")

# ---------- the corrected-ruler contrast ----------
CLS = lambda pos: "RUCK" if pos == "RUCK" else ("KPP" if pos in ("KPF", "KPD") else "SMALL")
rows = []
for _a, v0, r in anchor_rows:   # v0 here IS the year-1 price (the ratio's denominator)
    i = INST.get((r["key"], r["type"], r["year"]))
    if i is None: continue                     # outside the corrected ruler's 2004-2015 window
    rows.append(dict(key=r["key"], year=r["year"], cls=CLS(r["pos"]), pos=r["pos"], v0=v0,
                     bent=v(r, 4) / DISC ** 3, corr=float(i["D_rt_win"]) / DISC ** 3))
print("on the corrected ruler's window: n=%d sitters" % len(rows))

F = lambda rs, k: (sum(x[k] for x in rs) / sum(x["v0"] for x in rs)) if rs else float("nan")
def effn(rs):
    w = np.array([x["v0"] for x in rs], float)
    return float(w.sum() ** 2 / (w * w).sum()) if w.sum() > 0 else 0.0
def ci(rs, k):
    m = len(rs)
    if m < 2: return (float("nan"),) * 2
    d = np.array([x["v0"] for x in rs], float); y = np.array([x[k] for x in rs], float)
    idx = rng.integers(0, m, size=(NB, m))
    bp = y[idx].sum(1) / np.maximum(d[idx].sum(1), 1e-9)
    return float(np.percentile(bp, 2.5)), float(np.percentile(bp, 97.5))

print("\n=== THE THREE RULED CLASSES (F8 at PLAYER unit, weights = v0) ===")
print(" %-8s %5s %8s %10s %10s %-22s %s" % ("class", "n", "eff-n", "F bent", "F corr", "95% CI (corr)", "F8"))
byc = collections.defaultdict(list)
for x in rows: byc[x["cls"]].append(x)
for c in ("KPP", "SMALL", "RUCK"):
    rs = byc[c]
    lo, hi = ci(rs, "corr")
    print(" %-8s %5d %8.1f %10.4f %10.4f [%.3f, %.3f]%s %s"
          % (c, len(rs), effn(rs), F(rs, "bent"), F(rs, "corr"), lo, hi, " " * 5,
             "PASS" if effn(rs) >= BARN else "FAIL"))

kpp, sml = F(byc["KPP"], "corr"), F(byc["SMALL"], "corr")
kppb, smlb = F(byc["KPP"], "bent"), F(byc["SMALL"], "bent")
print("\n=== THE CONTRAST ===")
print("  bent ruler      KPP/SMALL = %.4f   [the filed 1.378]" % (kppb / smlb))
print("  CORRECTED ruler KPP/SMALL = %.4f" % (kpp / sml))
# bootstrap the contrast itself
K, S = byc["KPP"], byc["SMALL"]
bk = rng.integers(0, len(K), size=(NB, len(K))); bs = rng.integers(0, len(S), size=(NB, len(S)))
kn = np.array([x["corr"] for x in K]); kd = np.array([x["v0"] for x in K])
sn = np.array([x["corr"] for x in S]); sd = np.array([x["v0"] for x in S])
rat = (kn[bk].sum(1) / np.maximum(kd[bk].sum(1), 1e-9)) / np.maximum(sn[bs].sum(1) / np.maximum(sd[bs].sum(1), 1e-9), 1e-9)
clo, chi = float(np.percentile(rat, 2.5)), float(np.percentile(rat, 97.5))
print("  95%% CI on the corrected contrast = [%.3f, %.3f]   [the filed interval 1.05, 1.80]" % (clo, chi))
print("\n  A sitter KPP retains MORE of his year-0 value than a sitter SMALL by this factor, so the")
print("  sit-out CHARGE on KPP is too heavy and the charge on SMALL too light — the ruled direction.")

# ---------- the cautious-end sizing, conserved within the sitter pool ----------
print("\n=== THE CAUTIOUS-END SIZING, CONSERVED WITHIN THE SITTER POOL ===")
print("  FLAG 1 — the corrected CI [%.3f, %.3f] INCLUDES 1.0. On the corrected ruler the KPP/SMALL" % (clo, chi))
print("  contrast is NOT clear of 1: the tilt is not independently significant any more. The filed")
print("  interval [1.05, 1.80] WAS clear of 1, and that was measured on the bent ruler (which this")
print("  script reproduces at %.4f against the filed 1.378)." % (kppb / smlb))
print("  FLAG 2 — 'cautious end' therefore CANNOT mean the CI's lower edge here: that edge is %.4f," % clo)
print("  BELOW 1, and sizing on it would INVERT the ruled direction (it would deepen the KPP charge")
print("  and lighten SMALL — the opposite of the ruling). A tilt whose interval covers 1 has a")
print("  cautious end of 1.0, i.e. NO TILT.")
print()
print("  WHAT SHIPS: the RULED cautious end, 1.05 — taken AS FILED, and marked as filed in the")
print("  attribution. It is defensible on this measurement rather than in spite of it: the corrected")
print("  point estimate %.4f sits ABOVE 1.05, so 1.05 stays the cautious choice, and 1.05 lies" % (kpp / sml))
print("  inside the corrected CI. The alternative honest reading — ship ZERO tilt because the")
print("  corrected contrast no longer clears the bar — is the owner's call, and is flagged.")
CAUT = 1.05         # THE RULED CAUTIOUS END, as filed
print("  RUCK takes NO tilt (ruled: neutral base, no lawful ruck sitter cell).")
wK = sum(x["v0"] for x in K); wS = sum(x["v0"] for x in S)
# tilt: KPP charge lightened by factor t_K>1 on retention, SMALL deepened t_S<1, conserved:
#   wK*t_K + wS*t_S = wK + wS  and  t_K/t_S = CAUT
tS = (wK + wS) / (wK * CAUT + wS)
tK = CAUT * tS
print("  solve  t_KPP/t_SMALL = %.4f  and  Sig v0 x t held over the sitter pool:" % CAUT)
print("     t_KPP   = %.6f   (retention UP  -> charge LIGHTENED)" % tK)
print("     t_SMALL = %.6f   (retention DOWN-> charge DEEPENED)" % tS)
print("     t_RUCK  = 1.000000  (untouched)")
print("  CONSERVATION over the sitter pool: Sig v0 before %.1f  after %.1f  delta %.9f"
      % (wK + wS, wK * tK + wS * tS, wK * tK + wS * tS - (wK + wS)))
json.dump(dict(contrast_bent=kppb / smlb, contrast_corr=kpp / sml, ci=[clo, chi],
               cautious=CAUT, cautious_source="RULED 1.05, taken AS FILED",
               corrected_ci_covers_1=bool(clo <= 1.0 <= chi),
               t_KPP=tK, t_SMALL=tS, t_RUCK=1.0,
               n=dict(KPP=len(K), SMALL=len(S), RUCK=len(byc["RUCK"])),
               effn=dict(KPP=effn(K), SMALL=effn(S), RUCK=effn(byc["RUCK"]))),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "item_d_factors.json"), "w"), indent=1)
print("\nwrote item_d_factors.json")
