"""REALIZED-RATE re-build (addendum brief, issue #334 comment 5236376068).

THE OWNER'S PRINCIPLE, implemented literally: the price is for the IDEA of the output rate.
Availability is deliberately NOT priced on the price side, so it must not enter the realized side
either -- except as UNAVAILABILITY, a season so thin the sample is dubious.

  sp_rate(season) = SCALE * posval(avg + capt_prem(avg) - REPL[bar]) * G
      G = FULL   if games >= T      (the idea of the output: the engine's own projected count)
      G = games  if games <  T      (unavailability: prices at what was actually delivered)
  FULL = 21, the engine's OWN projected per-season count in the pricing kernel
         (rl_model.py:814-815 `*21`, and :845 in prod_floor).  NOT cp.SEASON=22, which is the
         availability-accounting constant used by _playable (rl_model.py:133) -- a different object.
         Using 22 would multiply every rate-based number by 22/21 = 1.0476 uniformly: a pure level
         shift, zero effect on the bend.

UNCHANGED from the landed instrument, so the two columns are comparable:
  PROXY = vpath[3]                      (so Kish eff-n is IDENTICAL by construction)
  career end = no season row = delivers nothing
  terminal stub for live 11+ = ev(p,2026) discounted from 2026 to C+4
  discounting = 1.0939/yr back to career year 4
  population, censoring window, bar, poolings, caveats

SELF-CHECK: the availability-in column recomputed here must equal r10_rows.json exactly.
READ-ONLY.
"""
import json, math, os
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
C = json.load(open(SP + "/r7_scale.json"))
SCALE = C["SCALE"]; S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
DISC = 1.0939; ENG_DISC = 1.0 + C["LENS"]["bal"]; END = 2026
FULL = 21.0                       # rl_model.py:814-815 -- the engine's own pricing count
THRESHOLDS = [5, 6, 8, 10, 13, 15]
HEADLINE_T = 6


def _sp(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt_prem(l):
    c = LG * LW * (_sp((l - LM) / LW) - _sp((LB - LM) / LW))
    return c if c > 0.0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def kern(avg, bar): return SCALE * posval(avg + capt_prem(avg) - REPL[bar]) if bar in REPL else 0.0


MATRIX = E + "/stage5/noarb/per_entrant_338_stage5.json"
MX = json.load(open(MATRIX))
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
    if not (2004 <= r["year"] <= 2022): continue
    if r["year"] + 4 > END: continue
    done = bool(r["retired_now"] or r["delisted"])
    ns = nseas_data(r)
    if not done and ns < 11: continue
    Cy = r["year"]
    real_av = 0.0                               # availability-in (the landed instrument)
    rate = {t: 0.0 for t in THRESHOLDS}
    rate_no26 = {t: 0.0 for t in THRESHOLDS}
    n_full = {t: 0 for t in THRESHOLDS}; n_unav = {t: 0 for t in THRESHOLDS}
    for s in (r.get("seasons") or []):
        y = s["year"]; k = y - Cy
        if k < 4 or y > END: continue
        u = kern(s["avg"], s["bar"]); g = s["games"]
        d = DISC ** (k - 4)
        real_av += u * g / d
        for t in THRESHOLDS:
            G = FULL if g >= t else g
            if g >= t: n_full[t] += 1
            elif g >= 1: n_unav[t] += 1
            rate[t] += u * G / d
            if y <= 2025: rate_no26[t] += u * G / d
    stub = 0.0
    if not done and r.get("cur"):
        stub = float(r["cur"]) / DISC ** (END - (Cy + 4))
    proxy = v(r, 4) or 0.0
    smap = {s["year"]: s for s in (r.get("seasons") or [])}
    rows.append(dict(
        key=r["key"], player=r["player"], typ=r["type"], year=Cy, pick=r.get("pick"),
        pickless=bool(r.get("pickless")), is_pool=bool(r["is_pool"]), pos=r["pos"],
        age=r.get("age_draft"), done=done, nseas=ns, proxy=proxy, stub=stub,
        real_av=real_av, realized=real_av + stub,
        rate={str(t): rate[t] for t in THRESHOLDS},
        rate_no26={str(t): rate_no26[t] for t in THRESHOLDS},
        n_full={str(t): n_full[t] for t in THRESHOLDS}, n_unav={str(t): n_unav[t] for t in THRESHOLDS},
        g3=smap.get(Cy + 3, {}).get("games", 0), g4=smap.get(Cy + 4, {}).get("games", 0),
        g5=smap.get(Cy + 5, {}).get("games", 0),
        a3=smap.get(Cy + 3, {}).get("avg", 0.0), a4=smap.get(Cy + 4, {}).get("avg", 0.0),
        a5=smap.get(Cy + 5, {}).get("avg", 0.0),
        sp3=kern(smap[Cy + 3]["avg"], smap[Cy + 3]["bar"]) * smap[Cy + 3]["games"] if Cy + 3 in smap else 0.0,
        sp4=kern(smap[Cy + 4]["avg"], smap[Cy + 4]["bar"]) * smap[Cy + 4]["games"] if Cy + 4 in smap else 0.0,
        sp5=kern(smap[Cy + 5]["avg"], smap[Cy + 5]["bar"]) * smap[Cy + 5]["games"] if Cy + 5 in smap else 0.0,
        reached5=bool(Cy + 5 <= END),
    ))

# ---- SELF-CHECK against the landed row file -------------------------------------------------
OLD = {(x["key"], x["typ"], x["year"]): x for x in json.load(open(SP + "/r10_rows.json"))["rows"]}
bad = 0
for x in rows:
    o = OLD.get((x["key"], x["typ"], x["year"]))
    if o is None: bad += 1; continue
    if abs(o["proxy"] - x["proxy"]) > 1e-6 or abs(o["real4"] - x["real_av"]) > 1e-6 \
       or abs(o["stub"] - x["stub"]) > 1e-6 or abs(o["sp4"] - x["sp4"]) > 1e-6:
        bad += 1
print("SELF-CHECK availability-in column vs landed r10_rows.json: %d mismatches of %d rows -> %s"
      % (bad, len(rows), "PASS" if bad == 0 else "FAIL"))

json.dump(dict(meta=dict(matrix=os.path.basename(MATRIX), store=MX["meta"]["store_md5"],
                         engine_head=MX["meta"]["engine_head"], SCALE=SCALE, DISC=DISC,
                         FULL=FULL, thresholds=THRESHOLDS, headline_T=HEADLINE_T),
               rows=rows), open(SP + "/r20_rows.json", "w"))

W = [x for x in rows if 2004 <= x["year"] <= 2015]
P = sum(x["proxy"] for x in W)
print()
print("PRIMARY window 2004-2015: n=%d  sum PROXY=%.0f (UNCHANGED -- eff-n identical by construction)"
      % (len(W), P))
print()
print("  %-28s %10s %8s %8s   %s" % ("instrument", "sumReal", "TILT", "1/tilt", "stub share"))
Rav = sum(x["realized"] for x in W)
print("  %-28s %10.0f %8.4f %8.4f   %5.2f%%" %
      ("availability-in (landed)", Rav, Rav / P, P / Rav, 100 * sum(x["stub"] for x in W) / Rav))
for t in THRESHOLDS:
    R = sum(x["rate"][str(t)] + x["stub"] for x in W)
    tag = "  <== HEADLINE" if t == HEADLINE_T else ""
    print("  %-28s %10.0f %8.4f %8.4f   %5.2f%%%s" %
          ("REALIZED-RATE  T=%d games" % t, R, R / P, P / R, 100 * sum(x["stub"] for x in W) / R, tag))
print()
print("season accounting at each threshold (seasons from career year 4 on, primary window):")
for t in THRESHOLDS:
    nf = sum(x["n_full"][str(t)] for x in W); nu = sum(x["n_unav"][str(t)] for x in W)
    print("   T=%-3d full-rate seasons %5d | unavailability seasons (1..%d games) %4d | share unavail %4.1f%%"
          % (t, nf, t - 1, nu, 100 * nu / max(nf + nu, 1)))
print()
print("wrote", SP + "/r20_rows.json")
