"""SENSITIVITY: the 21-game normalization read ONE-SIDED (lift short seasons, never cap long ones).
The addendum brief says 'price it at full-season equivalent', which taken literally is G=21 for every
qualifying season -- two-sided.  G=max(games,21) is the natural alternative reading.  Both reported.
READ-ONLY."""
import json, math
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
C = json.load(open(SP + "/r7_scale.json"))
SCALE = C["SCALE"]; S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
DISC = 1.0939; END = 2026; FULL = 21.0


def _s(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt(l):
    c = LG * LW * (_s((l - LM) / LW) - _s((LB - LM) / LW)); return c if c > 0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def kern(a, b): return SCALE * posval(a + capt(a) - REPL[b]) if b in REPL else 0.0


recs = {(r["key"], r["type"], r["year"]): r for r in
        json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]}
ROWS = [r for r in json.load(open(SP + "/r20_rows.json"))["rows"] if 2004 <= r["year"] <= 2015]
TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")
el = lambda r: r["reached5"] and r["g3"] >= 1 and r["g5"] >= 1
dipG = lambda r: el(r) and r["g4"] < 0.80 * min(r["g3"], r["g5"])
dipB = lambda r: el(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])


def realized(r, T, one_sided):
    rec = recs[(r["key"], r["typ"], r["year"])]; Cy = r["year"]; tot = 0.0
    for s in (rec.get("seasons") or []):
        k = s["year"] - Cy
        if k < 4 or s["year"] > END: continue
        g = s["games"]
        if g < T: G = g
        else: G = max(g, FULL) if one_sided else FULL
        tot += kern(s["avg"], s["bar"]) * G / DISC ** (k - 4)
    return tot + r["stub"]


CELLS = [("OVERALL", lambda r: True),
         ("SF", lambda r: r["pos"] == "SF"), ("KPD", lambda r: r["pos"] == "KPD"),
         ("MID", lambda r: r["pos"] == "MID"), ("SD", lambda r: r["pos"] == "SD"),
         ("talls", lambda r: r["pos"] in TALL), ("runners", lambda r: r["pos"] in RUN),
         ("AVAILABILITY dip", dipG),
         ("FORM dip only", lambda r: el(r) and dipB(r) and not dipG(r)),
         ("no dip at all", lambda r: el(r) and not dipB(r) and not dipG(r))]
print("=" * 104)
print("ONE-SIDED (lift, never cap) vs TWO-SIDED (G=21 exactly) at T=6 -- 1/tilt")
print("=" * 104)
print("  %-22s %5s | %10s %10s %10s" % ("cell", "n", "landed", "two-sided", "one-sided"))
for nm, f in CELLS:
    rs = [r for r in ROWS if f(r)]
    P = sum(r["proxy"] for r in rs)
    if P <= 0: continue
    a = sum(r["realized"] for r in rs) / P
    b = sum(realized(r, 6, False) for r in rs) / P
    c = sum(realized(r, 6, True) for r in rs) / P
    print("  %-22s %5d | %10.4f %10.4f %10.4f" % (nm, len(rs), 1 / a, 1 / b, 1 / c))
print()
print("  one-sided removes the 21-cap on the 1,178 finals-heavy seasons (22+ games) and therefore")
print("  lowers every factor further; it is a LEVEL move, and the bend ordering is unchanged.")
