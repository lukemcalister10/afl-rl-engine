"""THE YEAR-4 RULER TILT MAP — instrument + per-row build.
Issue #334 comment 5236054423.  READ-ONLY.  Writes only into the session scratchpad.

CURRENCY.  Engine PLAYER board points, pick-1 anchored at 3000 (_P1=3000, PVC[1]=3000,
BOARD_FACTOR=0.65549 already folded into SCALE).  The 1.0524 pick-redenomination factor is NOT
applied anywhere: no board PICK price enters this instrument, only player ev() and player season
prices, which share one currency by construction.

PROXY   = rec['vpath'][3] = ev(p, C+4) walk-forward, scoring truncated to <= C+4.  Career year k is
          CALENDAR-anchored at C+k (emit_matrix_338.py:226); a sitter's year 4 is C+4 regardless of
          games.  Career ended before year 4 -> no vpath entry -> PROXY = 0 (bust, kept).
REALIZED = sum over observed seasons from career year 4 onward of the engine's OWN season price,
          discounted back to career year 4 at 1.0939/yr; plus, for LIVE careers with >=11 seasons of
          data, a terminal stub = rec['cur'] = ev(p,2026) discounted from 2026 back to C+4.
SEASON PRICE (the engine's own, rl_model.py:721 + 800-818):
          sp = SCALE * posval(avg + capt_prem(avg) - REPL[bar]) * games
          posval(x) = S_SH*log(1+exp(x/S_SH)), S_SH=3.0 ; bar = the season's OWN fit bar, quoted from
          the matrix `seasons[].bar` (= MA._fit_bar(p, year), rl_model.py:99-105).
          The engine's *21 (full-season games count) is replaced by the season's ACTUAL games -- that
          is the only edit, and it is what makes the object a realized season rather than a projected
          one.  The KPF/KPD *1.05 key multiplier and the runway*elite kicker (rl_model.py:816-817) are
          CAREER-level projection adjustments, not season pricing: excluded from the headline,
          measured as sensitivity KEY105.
"""
import json, math, os

SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
C = json.load(open(SP + "/r7_scale.json"))
SCALE = C["SCALE"]; S_SH = C["S_SH"]; REPL = C["REPL"]
LB, LM, LW, LG = C["LCAPT"]["BAR"], C["LCAPT"]["M"], C["LCAPT"]["W"], C["LCAPT"]["G"]
DISC = 1.0939
ENG_DISC = 1.0 + C["LENS"]["bal"]      # 1.14, the engine's own per-annum production discount
END = 2026
YR_LO, YR_HI = 2004, 2022


def _softplus(x): return math.log1p(math.exp(x)) if x < 30.0 else x
def capt_prem(lev):
    c = LG * LW * (_softplus((lev - LM) / LW) - _softplus((LB - LM) / LW))
    return c if c > 0.0 else 0.0
def posval(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def season_price(avg, games, bar):
    if games <= 0 or bar not in REPL: return 0.0
    return SCALE * posval(avg + capt_prem(avg) - REPL[bar]) * games


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
drops = {"class2003_or_out_of_window": 0, "not_reached_year4": 0, "live_under_11": 0}
for r in recs:
    if not (YR_LO <= r["year"] <= YR_HI):
        drops["class2003_or_out_of_window"] += 1; continue
    if r["year"] + 4 > END:
        drops["not_reached_year4"] += 1; continue
    done = bool(r["retired_now"] or r["delisted"])
    ns = nseas_data(r)
    if not done and ns < 11:
        drops["live_under_11"] += 1; continue
    Cy = r["year"]
    smap = {s["year"]: s for s in (r.get("seasons") or [])}
    # ---- realized: observed seasons from career year 4 (calendar Cy+4) onward ----
    real4 = real5 = real4_eng = real4_key = real4_no26 = 0.0
    for y, s in smap.items():
        k = y - Cy
        if k < 4 or y > END: continue
        sp_ = season_price(s["avg"], s["games"], s["bar"])
        spk = sp_ * (1.05 if s["bar"] in ("KPF", "KPD") else 1.0)
        real4 += sp_ / DISC ** (k - 4)
        real4_eng += sp_ / ENG_DISC ** (k - 4)
        real4_key += spk / DISC ** (k - 4)
        if y <= 2025: real4_no26 += sp_ / DISC ** (k - 4)
        if k >= 5: real5 += sp_ / DISC ** (k - 4)   # ex-dividend: yr-5 onward, still discounted TO yr 4
    # ---- terminal stub for live 11+ ----
    stub = 0.0
    if not done:
        cur = r.get("cur")
        if cur: stub = float(cur) / DISC ** (END - (Cy + 4))
    # PROXY = the engine's price at CAREER YEAR 4 = vpath[3]; v(r,n) maps career year n -> vpath[n-1]
    # (noarb_table_338.py:41 "year N >= 1 -> vpath[N-1]"), so career year 4 is v(r, 4).
    proxy = v(r, 4) or 0.0
    assert (r["year"] + 4 <= END)
    rows.append(dict(
        key=r["key"], player=r["player"], typ=r["type"], year=Cy, pick=r.get("pick"),
        pickless=bool(r.get("pickless")), is_pool=bool(r["is_pool"]), pos=r["pos"],
        age=r.get("age_draft"), done=done, nseas=ns, games_total=r["games_total"],
        proxy=proxy, real4=real4, real5=real5, real4_eng=real4_eng, real4_key=real4_key,
        real4_no26=real4_no26, stub=stub, cur=r.get("cur"),
        last_game_year=r.get("last_game_year"),
        sp3=season_price(smap[Cy + 3]["avg"], smap[Cy + 3]["games"], smap[Cy + 3]["bar"]) if Cy + 3 in smap else 0.0,
        sp4=season_price(smap[Cy + 4]["avg"], smap[Cy + 4]["games"], smap[Cy + 4]["bar"]) if Cy + 4 in smap else 0.0,
        sp5=season_price(smap[Cy + 5]["avg"], smap[Cy + 5]["games"], smap[Cy + 5]["bar"]) if Cy + 5 in smap else 0.0,
        g3=smap.get(Cy + 3, {}).get("games", 0), g4=smap.get(Cy + 4, {}).get("games", 0),
        g5=smap.get(Cy + 5, {}).get("games", 0),
        a3=smap.get(Cy + 3, {}).get("avg", 0.0), a4=smap.get(Cy + 4, {}).get("avg", 0.0),
        a5=smap.get(Cy + 5, {}).get("avg", 0.0),
        reached5=bool(Cy + 5 <= END),
    ))

for x in rows:
    x["realized"] = x["real4"] + x["stub"]

json.dump(dict(meta=dict(matrix=os.path.basename(MATRIX), store=MX["meta"]["store_md5"],
                         engine_head=MX["meta"]["engine_head"], SCALE=SCALE, DISC=DISC,
                         ENG_DISC=ENG_DISC, window=[YR_LO, YR_HI], drops=drops),
               rows=rows), open(SP + "/r10_rows.json", "w"))

print("population rows        : %d" % len(rows))
print("drops                  : %s" % drops)
print("completed              : %d ; live 11+ : %d" % (sum(1 for x in rows if x["done"]),
                                                       sum(1 for x in rows if not x["done"])))
P = sum(x["proxy"] for x in rows); R = sum(x["realized"] for x in rows)
print("OVERALL  sum PROXY=%.0f  sum REALIZED=%.0f  TILT=%.4f" % (P, R, R / P))
S = sum(x["stub"] for x in rows)
print("  terminal-stub share of REALIZED : %.2f%%" % (100 * S / R))
print("  zero-proxy rows (bust before yr4): %d  (they carry ZERO weight in a value-weighted ratio)"
      % sum(1 for x in rows if x["proxy"] <= 0))
print("  rows with proxy>0                : %d" % sum(1 for x in rows if x["proxy"] > 0))
print()
print("variants (overall):")
for nm, num in (("year-4 inclusive [HEADLINE]", lambda x: x["real4"] + x["stub"]),
                ("year-5 onward (ex-dividend)", lambda x: x["real5"] + x["stub"]),
                ("engine 14%%/yr discount     ", lambda x: x["real4_eng"] + x["stub"]),
                ("KEY105 (KPF/KPD x1.05)     ", lambda x: x["real4_key"] + x["stub"]),
                ("2026 season excluded       ", lambda x: x["real4_no26"] + x["stub"]),
                ("no terminal stub           ", lambda x: x["real4"])):
    print("   %-28s tilt=%.4f" % (nm, sum(num(x) for x in rows) / P))
print()
print("wrote", SP + "/r10_rows.json")
