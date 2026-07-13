"""D1 — the SPEC_2/3 calibration legs on the tagged board 81e48293. JUH nqual cliff · Ryan _fbump · Dylan
Moore body-of-work axis. Mechanism from the CODE; measurement; effect size; implied correction SIZE. No proposal."""
import json, copy, io, contextlib
import numpy as np
import harness as H
MA = H.MA; cp = H.cp; ev = H.ev; G = H.G; F = H.F
_nqual = H._nqual; _agemult = H._agemult; _agemult2 = H._agemult2
_lvlcurr = G["_lvlcurr"]; DOWN_TOL = G["DOWN_TOL"]; PROVEN_N = G["PROVEN_N"]; REPL = MA.REPL
BASE = "/home/user/afl-rl-engine/session_2026-07-13/measurement"
def bv(p): return int(round(ev(p) / F))

def variant(p, scoring2026):
    q = copy.deepcopy(p)
    q["scoring"] = [s for s in q["scoring"] if s["year"] != 2026]
    if scoring2026 is not None:
        q["scoring"].append(scoring2026)
    MA._pe_clear()
    return q

OUT = {"board": "81e48293 (store b0c39d78, tagged v2.9)"}

# ===================== D1a — JUH (Jamarra Ugle-Hagan) nqual cliff & -865 cameo =====================
juh = H.find("Jamarra Ugle-Hagan")
nq = _nqual(juh, 2026)
v_actual = bv(juh)
v_no2026 = bv(variant(juh, None))                          # cameo removed (career ends 2024)
v_healthy = bv(variant(juh, {"year": 2026, "games": 22, "avg": 63.8}))  # healthy continuation at prior level
# nqual cliff: sweep 2026 games at avg 26.0 (games>=10 flips nqual 3->4 = PROVEN)
cliff = []
for gm in [0, 2, 3, 5, 7, 9, 10, 11, 14, 18, 22]:
    q = variant(juh, {"year": 2026, "games": gm, "avg": 26.0} if gm > 0 else None)
    cliff.append(dict(games2026=gm, nqual=_nqual(q, 2026), board=bv(q)))
# matched production, vary nqual via # of qualifying (>=10g) prior seasons at avg 55, pick1 KEY_FWD synth-ish
MA._pe_clear()
OUT["D1a_JUH"] = dict(player="Jamarra Ugle-Hagan", pos=MA.gfut(juh), pick=juh.get("pick"), draft=juh.get("year"),
    nqual_today=nq, PROVEN_N=PROVEN_N,
    scoring=[(s["year"], s["games"], s["avg"]) for s in sorted(juh["scoring"], key=lambda x: x["year"])],
    board_actual=v_actual, board_cameo_removed=v_no2026, board_healthy2026=v_healthy,
    cameo_cost_vs_removed=v_no2026 - v_actual, cameo_cost_vs_healthy=v_healthy - v_actual,
    nqual_cliff_sweep=cliff)

# ===================== D1b — Ryan / _fbump census =====================
Y = 2026
fired = []
for p in H.players():
    try:
        if G["delisted"](p): continue
        Lo = cp._lvl_eff_orig(p, Y); n = _nqual(p, Y)
        if n < PROVEN_N: continue
        Lc = _lvlcurr(p, Y)
        if Lo - Lc <= DOWN_TOL: continue
        lcr = Lc - REPL.get(MA.gfut(p), 0.0)
        if lcr <= 0: continue
        a = cp._age_asof(p, Y)
        am, am2 = _agemult(a), _agemult2(a, lcr)
        if am2 > am + 1e-9:
            fired.append(dict(player=p["player"], pos=MA.gfut(p), age=round(a, 1), Lo=round(Lo, 1),
                              Lc=round(Lc, 1), lcr=round(lcr, 1), bump=round(am2 - am, 4), key=p.get("key")))
    except Exception:
        pass
# SCAR each fired player moves via _fbump (ev with fbump vs fbump-zeroed)
_orig_fb = G["_fbump"]
on = {}
for d in fired: on[d["key"]] = bv(H.find(d["player"]))
G["_fbump"] = lambda a, lcr: 0.0; MA._pe_clear()
off = {}
for d in fired: off[d["key"]] = bv(H.find(d["player"]))
G["_fbump"] = _orig_fb; MA._pe_clear()
for d in fired:
    d["board_on"] = on[d["key"]]; d["board_off"] = off[d["key"]]; d["fbump_scar"] = on[d["key"]] - off[d["key"]]
fired.sort(key=lambda d: -d["fbump_scar"])
total_fb = sum(d["fbump_scar"] for d in fired)
ryan = [d for d in fired if "ryan" in d["player"].lower()]
OUT["D1b_fbump"] = dict(n_fired=len(fired), total_scar_moved=total_fb,
    ryan_carriers=ryan, all_fired=fired,
    median_scar=int(np.median([d["fbump_scar"] for d in fired])) if fired else 0,
    max_scar=max([d["fbump_scar"] for d in fired]) if fired else 0)

# ===================== D1c — Dylan Moore penalty + body-of-work axis =====================
moore = H.find("Dylan Moore")
mv_actual = bv(moore)
mv_healthy = bv(variant(moore, {"year": 2026, "games": 22, "avg": 90.0}))   # healthy continuation ~ his 2022-25 body
mv_no2026 = bv(variant(moore, None))
MA._pe_clear()
# body-of-work axis: does career body-of-work predict next-season score OVER AND ABOVE the most recent season?
# population: real store player-seasons with year Y (games>=10) and Y+1 (games>=6) both observed; completed seasons only (<=2025)
rows = []
for p in MA.data:
    if not MA.GRP.get(p.get("pos")): continue
    sc = {s["year"]: s for s in p["scoring"] if s.get("games", 0) >= 1}
    yrs = sorted(sc)
    for Yv in yrs:
        if Yv >= 2025: continue
        if sc[Yv]["games"] < 10 or (Yv + 1) not in sc or sc[Yv + 1]["games"] < 6: continue
        prior = [sc[y] for y in yrs if y < Yv and sc[y]["games"] >= 6]
        if not prior: continue
        recent = sc[Yv]["avg"]
        gw = sum(s["games"] for s in prior)
        bow = sum(s["avg"] * s["games"] for s in prior) / gw   # career games-weighted mean, prior to Y
        rows.append((recent, bow, sc[Yv + 1]["avg"]))
recent = np.array([r[0] for r in rows]); bow = np.array([r[1] for r in rows]); nxt = np.array([r[2] for r in rows])
# partial effect of bow on next, controlling for recent (residualize both on recent via linear fit)
def resid(y, x):
    A = np.vstack([x, np.ones_like(x)]).T
    b = np.linalg.lstsq(A, y, rcond=None)[0]
    return y - A @ b, b
r_next, b_nr = resid(nxt, recent)      # next | recent
r_bow, b_br = resid(bow, recent)       # bow  | recent
# partial slope: next-resid ~ bow-resid
A = np.vstack([r_bow, np.ones_like(r_bow)]).T
slope = np.linalg.lstsq(A, r_next, rcond=None)[0][0]
partial_r = np.corrcoef(r_bow, r_next)[0, 1]
# incremental R^2 of adding bow to recent-only model
def r2(y, X):
    X = np.column_stack([X, np.ones(len(y))]); b = np.linalg.lstsq(X, y, rcond=None)[0]
    yp = X @ b; return 1 - np.sum((y - yp) ** 2) / np.sum((y - y.mean()) ** 2)
r2_recent = r2(nxt, recent.reshape(-1, 1))
r2_both = r2(nxt, np.column_stack([recent, bow]))
# smoothed partial-dependence: bin bow-residual into quantile knots, mean next-residual (report as smoothed curve, fine)
order = np.argsort(r_bow); K = 9
pd_curve = []
for i in range(K):
    lo, hi = i / K, (i + 1) / K
    idx = order[int(lo * len(order)):int(hi * len(order))]
    pd_curve.append(dict(bow_resid_mid=round(float(np.mean(r_bow[idx])), 2),
                         next_resid_mean=round(float(np.mean(r_next[idx])), 2), n=len(idx)))
OUT["D1c_moore"] = dict(player="Dylan Moore", pos=MA.gfut(moore), pick=moore.get("pick"), draft=moore.get("year"),
    scoring=[(s["year"], s["games"], s["avg"]) for s in sorted(moore["scoring"], key=lambda x: x["year"])],
    board_actual=mv_actual, board_healthy2026=mv_healthy, board_no2026=mv_no2026,
    dip_penalty_vs_healthy=mv_healthy - mv_actual, dip_penalty_vs_no2026=mv_no2026 - mv_actual,
    bow_axis=dict(n=len(rows), partial_slope_next_per_bow=round(float(slope), 4),
                  partial_corr=round(float(partial_r), 4),
                  r2_recent_only=round(float(r2_recent), 4), r2_recent_plus_bow=round(float(r2_both), 4),
                  incremental_r2=round(float(r2_both - r2_recent), 4),
                  smoothed_partial_dependence=pd_curve))

json.dump(OUT, open(BASE + "/out/d1_carriers.json", "w"), indent=1)
print("=== D1a JUH ===", json.dumps(OUT["D1a_JUH"], indent=1))
print("\n=== D1b _fbump ===  n_fired=%d total_scar=%d median=%d max=%d" % (OUT["D1b_fbump"]["n_fired"], OUT["D1b_fbump"]["total_scar_moved"], OUT["D1b_fbump"]["median_scar"], OUT["D1b_fbump"]["max_scar"]))
print("Ryan carriers:", json.dumps(ryan, indent=1))
print("top fbump movers:", json.dumps(fired[:12], indent=1))
print("\n=== D1c Moore ===", json.dumps(OUT["D1c_moore"], indent=1))
print("\nwrote out/d1_carriers.json")
