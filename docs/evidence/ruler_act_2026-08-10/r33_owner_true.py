"""THE OWNER'S TABLE, TRUE WEIGHTS (main@ef7eff8).  READ-ONLY.

Every layer captured IN-CALL and reconstructed, with asserts:
  price6 = SCALE_DIST * dot(WQ6, [v_at_peak(p,L) for L in band])          WQ6=[.18]*5+[.10]
  v_at_peak(p,L) = max( val(sp*raw_present + (1-sp)*raw_lowbar) , prod_floor(p) )   sp=SEASON_PROG
  raw_*   = the W4 forward integral (_proj_w4)          -> per-age terms, transcribed + asserted
  floor   = _prod_floor_w4, a <=3-year present value    -> per-age terms, transcribed + asserted
GAMMA=1.0 => val() linear => allocating a node's value across ages in proportion to its own per-age
terms is exact (up to val()'s round()).

A node carried by the FLOOR contributes the FLOOR's age shape (<=3 years), NOT the integral's.
That is tracked per node and reported.

The board price ev(p) sits ABOVE price6 (captaincy add-back, the LEG-B un-compress map, pedigree /
iso layers).  The table's LEVEL is the board price; its SHAPE is the true-weighted production
mixture; the ratio is disclosed per player as `scale`.  Rows sum to the board price by construction
and the CHECK column proves it to 1e-6.
"""
import os, sys, io, json, contextlib, hashlib, time
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
WD = SP + "/rwm"; REPO = SP + "/repoM"
os.environ.setdefault("RL_REPO", REPO)
os.environ.setdefault("RL_FV", REPO + "/engine/forward_valuation")
os.environ["RL_V0SURF_PKL"] = REPO + "/data/v0surf.pkl"
sys.path.insert(0, "/home/claude/rl_vendor"); sys.path.insert(0, REPO)
sys.path.insert(0, REPO + "/engine/forward_valuation")
os.chdir(WD); sys.path.insert(0, ".")
print("basis: main@ef7eff8 store %s"
      % hashlib.md5(open(WD + "/rl_model_data.json", "rb").read()).hexdigest()[:8], flush=True)
_t = time.time()
src = open("_merged_recover.py").read().split('print("=== AFTER')[0]
G = {"__name__": "_r33"}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G["MA"]; ev = G["ev"]; dp = G["dp"]
print("engine loaded in %.0fs" % (time.time() - _t), flush=True)
WQ6 = [float(x) for x in G["WQ6"]]; SP_ = MA.SEASON_PROG
O_PROJ = MA.proj_from_peak; O_VAP = dp.v_at_peak; O_P6 = G["price6"]; O_FLOOR = MA.prod_floor
PROJ, FLOOR, NODES, P6 = [], [], [], []


def t_proj(g, lp, a, cur, lens, g0, fut, pre_hc):
    ctx = G["_W4CTX"]["on"]; bp = G["_BOARD_PATH"]
    if g0 is None: g0 = g
    if fut is None: fut = [(g, 1.0)]
    pa = MA.PEAK_AGE[g]; d = MA.LENS[lens]; prod = 0.0; rows = []
    _off = (MA.AGE_REF - MA.BASE_REF) if (ctx is not None and G["_LEGF_ON"]) else 0
    ah = a - _off if _off > 0 else a
    cl = cur if cur else lp * MA.frac(ah, pa)
    for k in range(18):
        ag = ah + k
        if ag > 38 or MA.frac(ag, pa) < 0.42: break
        lev = lp * MA.frac(ag, pa)
        if ag <= pa: lev = max(lev, cl)
        if k == 0: lev = max(lev, cl)
        if k == 0 and pre_hc > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026: lev *= (1 - pre_hc)
        if ctx is not None and bp and k == ctx.get("ret_k", -1) and ctx.get("ret_hc", 0.0) > 0:
            lev *= (1 - ctx["ret_hc"])
        base = lev + MA.capt_prem(lev)
        Wk = G["_w4_W"](k, ctx) if ctx is not None else 1.0
        if k == 0: t = Wk * MA.posval(base - MA.REPL[g0]) * 21 / ((1 + d) ** k)
        else: t = Wk * sum(w * MA.posval(base - MA.REPL[gg]) for gg, w in fut) * 21 / ((1 + d) ** k)
        prod += t; rows.append(dict(age=ag, pv=t))
    km = 1.05 if g in ("KPF", "KPD") else 1.0
    rw = MA.clamp((25 - ah) / 6.0, 0, 1); el = MA.clamp((lp / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
    kick = (1 + rw * el * MA.PMAX)
    for r in rows: r["pv"] *= km * kick
    return prod * km * kick, rows


def t_floor(p, lens):
    """verbatim _prod_floor_w4 (_merged_recover.py:955-967); returns (val(prod), rows) or None."""
    ctx = G["_W4CTX"]["on"]
    if ctx is None or ctx.get("n", 0) < G["PROVEN_N"] or not G["_W4FWD"]: return None
    g = MA.bnow(p); a = MA.age(p); pa_ = MA.PEAK_AGE[g]; cur = MA.level_now(p)
    if cur is not None and G["_lsym_active"]():
        cur = G["_lsym_blend"](MA.level_demo(p), cur, G["_lsym_age"](p))
    if cur is None: return None
    lowbar = MA.y0dpp_bar(p) if (MA.AGE_REF == MA.BASE_REF) else None
    d = MA.LENS[lens]; H = MA.clamp((40 - a) / 3.0, 1.0, 3.0); prod = 0.0; k = 0; rows = []
    while k < H:
        ag = a + k; wt = min(1.0, H - k)
        lev = cur * min(1.0, MA.frac(ag, pa_) / max(MA.frac(a, pa_), 1e-6))
        if k == 0 and p.get("_avail_hc", 0) > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
            lev *= (1 - p["_avail_hc"])
        base = lev + MA.capt_prem(lev)
        if k == 0 and lowbar is not None:
            pv = SP_ * MA.posval(base - MA.REPL[g]) + (1.0 - SP_) * MA.posval(base - MA.REPL[lowbar])
        else:
            pv = MA.posval(base - MA.REPL[g])
        t = G["_w4_W"](k, ctx) * wt * pv * 21 / ((1 + d) ** k)
        prod += t; rows.append(dict(age=ag, pv=t)); k += 1
    return MA.val(prod), rows


def rec_proj(g, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0):
    r = O_PROJ(g, lp, a, cur, lens, g0=g0, fut=fut, pre_hc=pre_hc)
    tot, rows = t_proj(g, lp, a, cur, lens, g0, fut, pre_hc)
    assert abs(tot - r) < 1e-9, "PROJ MISMATCH %.10f vs %.10f" % (tot, r)
    PROJ.append(dict(g0=g0, res=r, rows=rows)); return r


def rec_floor(p, lens="bal"):
    r = O_FLOOR(p, lens); tr = t_floor(p, lens)
    if tr is not None:
        assert abs(tr[0] - r) < 1e-6, "FLOOR MISMATCH %.6f vs %.6f" % (tr[0], r)
        FLOOR.append(dict(res=float(r), rows=tr[1], transcribed=True))
    else:
        FLOOR.append(dict(res=float(r), rows=None, transcribed=False))
    return r


def rec_vap(p, L, lens="bal"):
    del PROJ[:], FLOOR[:]
    res = O_VAP(p, L, lens)
    NODES.append(dict(L=float(L), res=float(res), projs=list(PROJ),
                      floor=(FLOOR[-1] if FLOOR else None))); return res


def rec_p6(p, bb, Y=2026):
    del NODES[:]
    r = O_P6(p, bb, Y)
    P6.append(dict(res=float(r), nodes=list(NODES), capt_off=bool(MA._CAPT_OFF["on"]),
                   bb=[float(x) for x in bb])); return r


MA.proj_from_peak = rec_proj; dp.v_at_peak = rec_vap; G["price6"] = rec_p6; MA.prod_floor = rec_floor
OUT = {}
for key in ["willem-duursma", "zak-butters", "marcus-bontempelli"]:
    p = next((x for x in MA.data if x.get("key") == key), None)
    if p is None: continue
    del P6[:]
    with contextlib.redirect_stdout(io.StringIO()): price = float(ev(p, 2026))
    use = [c for c in P6 if not c["capt_off"]][0]
    recon = dp.SCALE_DIST * sum(w * n["res"] for w, n in zip(WQ6, use["nodes"]))
    assert abs(recon - use["res"]) < 1e-6, "P6 RECON %s" % key
    cells = {}; tot_w = 0.0; carried = []
    for w, n in zip(WQ6, use["nodes"]):
        blended = {}
        if len(n["projs"]) == 2:
            for r in n["projs"][0]["rows"]: blended[r["age"]] = blended.get(r["age"], 0.0) + SP_ * r["pv"]
            for r in n["projs"][1]["rows"]: blended[r["age"]] = blended.get(r["age"], 0.0) + (1 - SP_) * r["pv"]
        else:
            for r in n["projs"][0]["rows"]: blended[r["age"]] = blended.get(r["age"], 0.0) + r["pv"]
        integ = float(MA.val(sum(blended.values())))
        fl = n["floor"]
        by_floor = bool(fl and fl["rows"] is not None and n["res"] > integ + 1e-9)
        shape = ({r["age"]: r["pv"] for r in fl["rows"]} if by_floor else blended)
        carried.append("FLOOR" if by_floor else "integral")
        s = sum(shape.values())
        for a, v in shape.items():
            cells[a] = cells.get(a, 0.0) + w * n["res"] * (v / s)
        tot_w += w * n["res"]
    assert abs(tot_w * dp.SCALE_DIST - use["res"]) < 1e-6, "WEIGHTED SUM %s" % key
    scale = price / use["res"]
    cells = {int(round(a)): v * scale for a, v in sorted(cells.items())}
    OUT[key] = dict(price=price, price6=use["res"], scale=scale, cells=cells, carried=carried,
                    band=use["bb"], WQ6=WQ6, C=p.get("year"), pos=MA.gfut(p), a_now=MA.age(p),
                    n_p6=len(P6))
    print("%-20s ev=%7.0f price6=%9.3f scale=%.4f carried=%s"
          % (key, price, use["res"], scale, carried), flush=True)
MA.proj_from_peak = O_PROJ; dp.v_at_peak = O_VAP; G["price6"] = O_P6; MA.prod_floor = O_FLOOR
json.dump(OUT, open(SP + "/r33_owner_true.json", "w"), indent=1, default=str)
print("wrote", SP + "/r33_owner_true.json", flush=True)
