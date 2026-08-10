"""HORIZON-CAPPED INSTRUMENT + the full 2x2 (addendum brief 2, issue #334 comment 5236414767).

THE OWNER'S POINT: the engine's forward projection rolls seasons on almost forever, while players
retire at 29-32.  Cap the horizon at career year 11 and mark the tail at the engine's OWN year-11
price, so a career that ended before 11 marks at 0 and a live career is marked, not extrapolated.

  PROXY            = vpath[3]  = ev(p, C+4)                     [UNCHANGED in all four instruments]
  REALIZED-WINDOWED = sum_{k=4..10} sp(C+k)/1.0939^(k-4)  +  vpath[10]/1.0939^7
                      vpath[10] = ev(p, C+11) = the engine's own year-11 price; 0 when the career's
                      window ended before year 11 (nothing remained -- correct by the act's own
                      'ended -> 0' convention, noarb_table_338.py:84-85).
  NO TERMINAL STUB ANYWHERE in the windowed instrument: a live career with >=11 seasons has a REAL
  year-11 price, so it enters exactly.  That is the owner's fairness point, and it is why the
  windowed instrument needs no stub machinery at all.

WINDOW: the primary window (classes 2004-2015) is EXACTLY the set for which career year 11 is
observable (C+11 <= 2026).  The horizon cap therefore adds no censoring of its own.

sp() comes in both flavours: availability-in (kernel x actual games) and rate-based (kernel x 21
when games >= 6, else x actual games).  2x2 = {full-horizon, yr11-capped} x {availability, rate}.
READ-ONLY.
"""
import json, math, os
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
C = json.load(open(SP + "/r7_scale.json"))
SCALE = C["SCALE"]; S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
DISC = 1.0939; END = 2026; FULL = 21.0; T = 6
CAP_K = 11                       # the horizon cap: career year 11


def _s(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt(l):
    c = LG * LW * (_s((l - LM) / LW) - _s((LB - LM) / LW)); return c if c > 0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def kern(a, b): return SCALE * posval(a + capt(a) - REPL[b]) if b in REPL else 0.0


MX = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))
recs = MX["recs"]


def v(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


def nseas_data(r): return sum(1 for s in (r.get("seasons") or []) if s["games"] >= 1)


rows = []
for r in recs:
    if not (2004 <= r["year"] <= 2015): continue          # == exactly where career yr 11 is observable
    done = bool(r["retired_now"] or r["delisted"])
    ns = nseas_data(r)
    if not done and ns < 11: continue
    Cy = r["year"]
    av_full = av_win = rt_full = rt_win = 0.0
    for s in (r.get("seasons") or []):
        k = s["year"] - Cy
        if k < 4 or s["year"] > END: continue
        u = kern(s["avg"], s["bar"]); g = s["games"]; d = DISC ** (k - 4)
        G = FULL if g >= T else g
        av_full += u * g / d; rt_full += u * G / d
        if k <= CAP_K - 1:                                # career years 4..10
            av_win += u * g / d; rt_win += u * G / d
    y11 = v(r, CAP_K)
    assert y11 is not None, "career year 11 unobservable inside the primary window"
    mark = y11 / DISC ** (CAP_K - 4)
    stub = 0.0
    if not done and r.get("cur"): stub = float(r["cur"]) / DISC ** (END - (Cy + 4))
    rows.append(dict(
        key=r["key"], player=r["player"], typ=r["type"], year=Cy, pick=r.get("pick"),
        pickless=bool(r.get("pickless")), is_pool=bool(r["is_pool"]), pos=r["pos"],
        age=r.get("age_draft"), done=done, nseas=ns, proxy=v(r, 4) or 0.0,
        A_av_full=av_full + stub, B_rt_full=rt_full + stub,
        C_av_win=av_win + mark, D_rt_win=rt_win + mark,
        y11=y11, mark=mark, stub=stub,
        obs410_av=av_win, obs410_rt=rt_win,
        g3=next((s["games"] for s in r["seasons"] if s["year"] == Cy + 3), 0),
        g4=next((s["games"] for s in r["seasons"] if s["year"] == Cy + 4), 0),
        g5=next((s["games"] for s in r["seasons"] if s["year"] == Cy + 5), 0),
        sp3=next((kern(s["avg"], s["bar"]) * s["games"] for s in r["seasons"] if s["year"] == Cy + 3), 0.0),
        sp4=next((kern(s["avg"], s["bar"]) * s["games"] for s in r["seasons"] if s["year"] == Cy + 4), 0.0),
        sp5=next((kern(s["avg"], s["bar"]) * s["games"] for s in r["seasons"] if s["year"] == Cy + 5), 0.0),
        reached5=True,
    ))

# self-check vs the two landed row files
OLD = {(x["key"], x["typ"], x["year"]): x for x in json.load(open(SP + "/r20_rows.json"))["rows"]}
bad = sum(1 for x in rows
          if abs(OLD[(x["key"], x["typ"], x["year"])]["realized"] - x["A_av_full"]) > 1e-6
          or abs(OLD[(x["key"], x["typ"], x["year"])]["rate"]["6"] + OLD[(x["key"], x["typ"], x["year"])]["stub"]
                 - x["B_rt_full"]) > 1e-6
          or abs(OLD[(x["key"], x["typ"], x["year"])]["proxy"] - x["proxy"]) > 1e-6)
print("SELF-CHECK full-horizon columns vs r20_rows.json: %d mismatches of %d -> %s"
      % (bad, len(rows), "PASS" if bad == 0 else "FAIL"))

json.dump(dict(meta=dict(store=MX["meta"]["store_md5"], engine_head=MX["meta"]["engine_head"],
                         SCALE=SCALE, DISC=DISC, FULL=FULL, T=T, CAP_K=CAP_K),
               rows=rows), open(SP + "/r24_rows.json", "w"))

P = sum(x["proxy"] for x in rows)
print()
print("THE 2x2  (n=%d, classes 2004-2015, sum PROXY=%.0f -- identical in all four)" % (len(rows), P))
print("  %-42s %10s %8s %8s" % ("instrument", "sumReal", "TILT", "1/tilt"))
for nm, k in (("A  full-horizon x availability-in [LANDED]", "A_av_full"),
              ("B  full-horizon x rate T=6", "B_rt_full"),
              ("C  yr-11 capped x availability-in", "C_av_win"),
              ("D  yr-11 capped x rate T=6", "D_rt_win")):
    R = sum(x[k] for x in rows)
    print("  %-42s %10.0f %8.4f %8.4f" % (nm, R, R / P, P / R))
print()
M = sum(x["mark"] for x in rows); OA = sum(x["obs410_av"] for x in rows)
OR_ = sum(x["obs410_rt"] for x in rows)
print("windowed decomposition:")
print("  discounted year-11 MARK (the engine's own tail)   %10.0f  = %.1f%% of C, %.1f%% of D"
      % (M, 100 * M / (OA + M), 100 * M / (OR_ + M)))
print("  observed seasons career yrs 4-10, availability     %10.0f" % OA)
print("  observed seasons career yrs 4-10, rate             %10.0f" % OR_)
nz = sum(1 for x in rows if x["y11"] <= 0)
print("  rows whose year-11 mark is 0 (career over by yr 11): %d of %d (%.1f%%), carrying %.1f%% of PROXY"
      % (nz, len(rows), 100 * nz / len(rows),
         100 * sum(x["proxy"] for x in rows if x["y11"] <= 0) / P))
print("  live rows (no stub used here):", sum(1 for x in rows if not x["done"]))
print()
print("wrote", SP + "/r24_rows.json")
