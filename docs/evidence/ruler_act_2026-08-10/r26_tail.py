"""TAIL SHARE — the direct test of the owner's 'we never price players to retire' conjecture.
What share of the year-4 price sits in projected seasons BEYOND career year 11?

TWO MEASUREMENTS, one exact and one labelled approximate.

(1) EXACT, ENGINE-NATIVE — the YEAR-11 CARRY.
    carry = sum_i vpath_i[10]/1.0939^7  /  sum_i vpath_i[3]
    The engine's OWN repricing of the same player seven years later, discounted back at the act's
    hurdle, as a share of the year-4 price.  No model: two numbers the matrix already contains.

(2) APPROXIMATE, LABELLED — the STRUCTURAL TAIL of the engine's own career integral.
    Engine loop rl_model.py:800-818:
        for k in 0..17: ag=a+k ; break if ag>38 or frac(ag,pa)<0.42
            lev=lp*frac(ag,pa) ; prod += posval(lev+capt_prem(lev)-REPL[g])*21/(1+d)^k , d=0.14
    Evaluated at a = draft age + 4 (the player's age in career year 4), with the engine's own
    PEAK_AGE / DELTAS / REPL / posval / capt_prem constants.  tail = share from k>=7 (k=0 is career
    year 4, so k=7 is career year 11).
    APPROXIMATION, STATED: the engine's peak-level input lp comes from its learned peak_est model,
    which needs a full walk-forward run to reproduce.  lp is set two ways, both engine objects --
    PEAK[pos] (params.json) and the player's own bestlvl at year 4 (max avg over games>=6,
    year<=C+4, computed exactly from the matrix; falls back to PEAK[pos] when no qualifying season
    exists) -- and a +/-15% band on lp is printed so the reader can see whether it is load-bearing.
    NOT approximated: the age path, the break rules, the discount, the position constants.
    Also stated: this is the tail of the PRODUCTION integral, the dominant but not only part of ev().

Age bands cover the classes carrying a draft age today.  The age-axis TILT re-cut is deferred to the
DOB-written store per the owner's order; nothing here is an age-tilt finding.
READ-ONLY.
"""
import json, math
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
RB = SP + "/repoB/engine/rl_after"
C = json.load(open(SP + "/r7_scale.json"))
S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
P = json.load(open(RB + "/params.json"))
PEAK = P["PEAK"]; PEAK_AGE = P["PEAK_AGE"]
DELTAS = {-8: .58, -7: .62, -6: .68, -5: .74, -4: .80, -3: .86, -2: .92, -1: .97, 0: 1.0,
          1: .99, 2: .98, 3: .96, 4: .94, 5: .91, 6: .88, 7: .84, 8: .79, 9: .73, 10: .66,
          11: .58, 12: .50, 13: .42, 14: .34}
D_LENS = 0.14
CAP_K = 11


def _s(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt(l):
    c = LG * LW * (_s((l - LM) / LW) - _s((LB - LM) / LW)); return c if c > 0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def frac(a, pa): return DELTAS[max(-8, min(14, int(round(a - pa))))]


def tail_share(a, g, lp):
    pa = PEAK_AGE[g]; head = 0.0; tail = 0.0
    for k in range(18):
        ag = a + k
        if ag > 38 or frac(ag, pa) < 0.42: break
        lev = lp * frac(ag, pa)
        term = posval(lev + capt(lev) - REPL[g]) * 21.0 / ((1 + D_LENS) ** k)
        if k >= (CAP_K - 4): tail += term
        else: head += term
    tot = head + tail
    return (tail / tot) if tot > 0 else float("nan")


MX = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))
byk = {(r["key"], r["type"], r["year"]): r for r in MX["recs"]}
ROWS = json.load(open(SP + "/r24_rows.json"))["rows"]
for x in ROWS:
    rec = byk[(x["key"], x["typ"], x["year"])]
    bl = [s["avg"] for s in rec["seasons"] if s["games"] >= 6 and s["year"] <= x["year"] + 4]
    x["bestlvl4"] = max(bl) if bl else 0.0

TALL = ("KPF", "KPD", "RUCK"); RUN = ("MID", "SD", "SF")


def carry(rows):
    p = sum(r["proxy"] for r in rows)
    return ((sum(r["mark"] for r in rows) / p) if p > 0 else float("nan")), p


def struct(rows, mode, mult=1.0):
    num = den = 0.0
    for r in rows:
        if r["age"] is None: continue
        a = r["age"] + 4; g = r["pos"]
        lp = PEAK[g] if mode == "peak" else (r["bestlvl4"] if r["bestlvl4"] > 0 else PEAK[g])
        ts = tail_share(a, g, lp * mult)
        if ts != ts: continue
        num += r["proxy"] * ts; den += r["proxy"]
    return ((num / den) if den > 0 else float("nan")), den


def block(title, cells):
    print()
    print("=" * 118)
    print(title)
    print("-" * 118)
    print("  %-30s %5s %10s | %8s | %9s %8s %8s | %9s" %
          ("cell", "n", "sumPROXY", "CARRY", "struct pk", "-15%", "+15%", "struct bl"))
    for nm, rs in cells:
        if not rs: print("  %-30s (empty)" % nm); continue
        c, p = carry(rs)
        s1, _ = struct(rs, "peak"); s2, _ = struct(rs, "peak", 0.85); s3, _ = struct(rs, "peak", 1.15)
        s4, _ = struct(rs, "best")
        print("  %-30s %5d %10.0f | %7.1f%% | %8.1f%% %7.1f%% %7.1f%% | %8.1f%%" %
              (nm, len(rs), p, 100 * c, 100 * s1, 100 * s2, 100 * s3, 100 * s4))


print("TAIL SHARE OF THE YEAR-4 PRICE BEYOND CAREER YEAR 11")
print("  CARRY     = EXACT: sum vpath[10]/1.0939^7 / sum vpath[3]")
print("  struct pk = APPROX: k>=7 share of the engine's own production integral, lp = PEAK[pos]")
print("  -15/+15   = the same with lp scaled -- how load-bearing the lp approximation is")
print("  struct bl = the same with lp = the player's own demonstrated best level at year 4")
print("  every cell value-weighted by the year-4 price (the tilt map's own weights)")

block("BY POSITION", [(p, [r for r in ROWS if r["pos"] == p])
                      for p in ("MID", "SD", "SF", "KPF", "KPD", "RUCK")]
      + [("talls", [r for r in ROWS if r["pos"] in TALL]),
         ("runners", [r for r in ROWS if r["pos"] in RUN]),
         ("ALL", ROWS)])

AB = [("<=18", lambda a: a <= 18), ("19-20", lambda a: 19 <= a <= 20),
      ("21-22", lambda a: 21 <= a <= 22), ("23+", lambda a: a >= 23)]
block("BY DRAFT-AGE BAND (classes carrying a draft age today)",
      [(nm, [r for r in ROWS if r["age"] is not None and f(r["age"])]) for nm, f in AB]
      + [("young <=20", [r for r in ROWS if r["age"] is not None and r["age"] <= 20]),
         ("mature 21+", [r for r in ROWS if r["age"] is not None and r["age"] >= 21])])

block("POSITION x AGE BAND",
      [("%s x %s" % (p, b), [r for r in ROWS if r["pos"] == p and r["age"] is not None
                             and ((r["age"] <= 20) if b == "young" else (r["age"] >= 21))])
       for p in ("MID", "SD", "SF", "KPF", "KPD", "RUCK") for b in ("young", "mature")])

print()
print("=" * 118)
print("WHAT THE TAIL ACTUALLY DELIVERED — the engine's year-11 mark vs what followed it")
print("=" * 118)
TP = sum(r["proxy"] for r in ROWS)
alive = [r for r in ROWS if r["y11"] > 0]; dead = [r for r in ROWS if r["y11"] <= 0]
print("  careers still priced at year 11 : %4d rows, %5.1f%% of PROXY weight"
      % (len(alive), 100 * sum(r["proxy"] for r in alive) / TP))
print("  careers over by year 11         : %4d rows, %5.1f%% of PROXY weight (tail marks 0)"
      % (len(dead), 100 * sum(r["proxy"] for r in dead) / TP))
pa = sum(r["A_av_full"] - r["obs410_av"] - r["stub"] for r in ROWS)
pstub = sum(r["stub"] for r in ROWS)
mk = sum(r["mark"] for r in ROWS)
print("  OBSERVED realized value delivered after career year 10 (availability basis, disc to yr 4):")
print("     %10.0f = %5.1f%% of the year-4 price   (plus %.0f of live-tail stub in instrument A)"
      % (pa, 100 * pa / TP, pstub))
print("  the engine's own YEAR-11 MARK (instrument C/D tail):")
print("     %10.0f = %5.1f%% of the year-4 price" % (mk, 100 * mk / TP))
print("  -> the year-11 mark stands %.2fx above the observed post-year-10 delivery; the horizon cap"
      % (mk / pa))
print("     REPLACES a long thin realized tail with a fatter engine mark, which is why the capped")
print("     instrument's LEVEL is only modestly below the full-horizon one.")
