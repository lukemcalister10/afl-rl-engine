"""SELECTION SENSITIVITY — how much the owner's '>= 11 seasons' live rule moves the answer.
Rebuilds the same instrument admitting EVERY live career that reached career year 4 (stub-terminated
the same way), so the size of the selection is a number, not an adjective.  READ-ONLY, no design."""
import json, math
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
C = json.load(open(SP + "/r7_scale.json"))
SCALE = C["SCALE"]; S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
DISC = 1.0939; END = 2026


def _sp(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt(l):
    c = LG * LW * (_sp((l - LM) / LW) - _sp((LB - LM) / LW)); return c if c > 0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def spz(a, g, b): return 0.0 if (g <= 0 or b not in REPL) else SCALE * posval(a + capt(a) - REPL[b]) * g


recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]


def build(min_live_seasons):
    out = []
    for r in recs:
        if not (2004 <= r["year"] <= 2015): continue
        if r["year"] + 4 > END: continue
        done = bool(r["retired_now"] or r["delisted"])
        ns = sum(1 for s in (r.get("seasons") or []) if s["games"] >= 1)
        if not done and ns < min_live_seasons: continue
        Cy = r["year"]
        real = 0.0
        for s in (r.get("seasons") or []):
            k = s["year"] - Cy
            if k < 4 or s["year"] > END: continue
            real += spz(s["avg"], s["games"], s["bar"]) / DISC ** (k - 4)
        stub = 0.0
        if not done and r.get("cur"): stub = float(r["cur"]) / DISC ** (END - (Cy + 4))
        vp = r.get("vpath") or []
        proxy = float(vp[3] or 0.0) if len(vp) >= 4 else 0.0
        out.append((proxy, real + stub, stub, done, Cy))
    return out


print("=" * 104)
print("SELECTION SENSITIVITY — the live-career admission bar (owner's rule = 11 seasons)")
print("classes 2004-2015; every completed career always admitted; the bar moves only the LIVE arm")
print("=" * 104)
print("  %-16s %6s %6s %10s %10s %8s %8s %8s" %
      ("live bar", "n", "n_live", "sumProxy", "sumReal", "TILT", "1/tilt", "stub%"))
for bar in (99, 15, 13, 11, 9, 7, 5, 0):
    rs = build(bar)
    P = sum(x[0] for x in rs); R = sum(x[1] for x in rs); S = sum(x[2] for x in rs)
    nl = sum(1 for x in rs if not x[3])
    lab = ("completed only" if bar == 99 else ("ALL live admitted" if bar == 0 else ">= %d seasons" % bar))
    print("  %-16s %6d %6d %10.0f %10.0f %8.4f %8.4f %7.1f%%" %
          (lab, len(rs), nl, P, R, R / P, P / R, 100 * S / R))
print()
print("  READ: the owner's 11-season bar sets the LIVE arm's share of the denominator.  The two arms")
print("  are structurally different populations -- see the split below -- so the mixture weight is")
print("  itself a measurement choice, and it is disclosed here as a number.")
rs11 = build(11)
for arm, f in (("completed careers", lambda x: x[3]), ("live 11+ careers", lambda x: not x[3])):
    sub = [x for x in rs11 if f(x)]
    P = sum(x[0] for x in sub); R = sum(x[1] for x in sub)
    print("     %-20s n=%4d  sumProxy %9.0f (%4.1f%% of weight)  TILT %.4f"
          % (arm, len(sub), P, 100 * P / sum(x[0] for x in rs11), R / P))
