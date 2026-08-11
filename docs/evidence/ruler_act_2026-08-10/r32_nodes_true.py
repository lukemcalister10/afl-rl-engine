"""TRUE-WEIGHT NODE CAPTURE at the price6 / v_at_peak boundary (main@ef7eff8).

THE AGGREGATION, read from source (not guessed):
  _merged_recover.py:381-387  price6(p,bb,Y):
      REPL is TEMPORARILY shifted by rd.REPL_DROP for the whole call (:384)
      return SCALE_DIST * _det_dot(WQ6, [dp.v_at_peak(p,L,'bal') for L in bb])
  _merged_recover.py:94       WQ6 = [0.18]*5 + [0.10], then /= sum  (sums to 1.0 already)
  _merged_recover.py:370-380  bb = b6(p,Y): 5 conditional-prior band levels + a 6th from q97m,
                              floored at b[4]
  distribution_pricing.py:260-283  v_at_peak(p,L):
      raw = proj_from_peak(g,L,a,cur,'bal',g0=bnow,fut=futblend,pre_hc)
      if lowbar is not None:  raw = sp*raw + (1-sp)*proj_from_peak(...,g0=lowbar)   sp=SEASON_PROG
      return max(val(raw), prod_floor(p,'bal'))        <-- a node can be carried by the FLOOR
  GAMMA=1.0 (rl_model.py:504) => val(r)=round(SCALE*r) is LINEAR, so allocating a node's value
  across ages in proportion to its raw per-age terms is exact up to val()'s round().

Everything is captured IN-CALL (module state live: REPL shift, _W4CTX, _CAPT_OFF).
READ-ONLY.
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
print("loading engine ...", flush=True); _t = time.time()
src = open("_merged_recover.py").read().split('print("=== AFTER')[0]
G = {"__name__": "_r32"}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G["MA"]; ev = G["ev"]; dp = G["dp"]
print("loaded in %.0fs" % (time.time() - _t), flush=True)
WQ6 = [float(x) for x in G["WQ6"]]
print("WQ6=%s (sum %.6f)  SCALE_DIST=%s  GAMMA=%s  SEASON_PROG=%s"
      % (WQ6, sum(WQ6), dp.SCALE_DIST, MA.GAMMA, MA.SEASON_PROG), flush=True)

O_PROJ = MA.proj_from_peak; O_VAP = dp.v_at_peak; O_P6 = G["price6"]; O_FLOOR = MA.prod_floor
PROJ, FLOORS, NODES, P6 = [], [], [], []


def transcribe(g, lp, a, cur, lens, g0, fut, pre_hc):
    """verbatim _proj_w4 / pre-W4, whichever the LIVE context selects; REPL read live."""
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
        prod += t; rows.append(dict(k=k, age=ag, lev=lev, Wk=Wk, pv=t))
    keymul = 1.05 if g in ("KPF", "KPD") else 1.0
    runway = MA.clamp((25 - ah) / 6.0, 0, 1); elite = MA.clamp((lp / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
    kick = (1 + runway * elite * MA.PMAX)
    prod *= keymul * kick
    for r in rows: r["pv"] *= keymul * kick
    return prod, rows


def rec_proj(g, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0):
    r = O_PROJ(g, lp, a, cur, lens, g0=g0, fut=fut, pre_hc=pre_hc)
    tot, rows = transcribe(g, lp, a, cur, lens, g0, fut, pre_hc)
    PROJ.append(dict(lp=lp, g0=g0, res=r, tot=tot, ok=bool(abs(tot - r) < 1e-9), rows=rows))
    return r


def rec_floor(p, lens="bal"):
    r = O_FLOOR(p, lens); FLOORS.append(float(r)); return r


def rec_vap(p, L, lens="bal"):
    del PROJ[:], FLOORS[:]
    res = O_VAP(p, L, lens)
    NODES.append(dict(L=float(L), res=float(res), projs=list(PROJ), floor=(FLOORS[-1] if FLOORS else None)))
    return res


def rec_p6(p, bb, Y=2026):
    del NODES[:]
    r = O_P6(p, bb, Y)
    P6.append(dict(bb=[float(x) for x in bb], res=float(r), nodes=list(NODES),
                   capt_off=bool(MA._CAPT_OFF["on"])))
    return r


MA.proj_from_peak = rec_proj; dp.v_at_peak = rec_vap; G["price6"] = rec_p6; MA.prod_floor = rec_floor
OUT = {}
for key in ["willem-duursma", "zak-butters", "marcus-bontempelli"]:
    p = next((x for x in MA.data if x.get("key") == key), None)
    if p is None: print("MISSING", key, flush=True); continue
    del P6[:]
    with contextlib.redirect_stdout(io.StringIO()): price = ev(p, 2026)
    prim = [c for c in P6 if not c["capt_off"]]
    print("\n%s  ev=%s  price6 calls=%d (captain-on %d)" % (key, price, len(P6), len(prim)), flush=True)
    for i, c in enumerate(P6):
        chk = dp.SCALE_DIST * sum(w * n["res"] for w, n in zip(WQ6, c["nodes"]))
        print("   p6[%d] capt_off=%-5s res=%9.3f  recon=%9.3f  d=%.2e  nodes=%d  band=%s"
              % (i, c["capt_off"], c["res"], chk, abs(chk - c["res"]), len(c["nodes"]),
                 ["%.2f" % x for x in c["bb"]]), flush=True)
    use = prim[0] if prim else P6[0]
    assert len(use["nodes"]) == len(WQ6), "node/weight length mismatch"
    recon = dp.SCALE_DIST * sum(w * n["res"] for w, n in zip(WQ6, use["nodes"]))
    assert abs(recon - use["res"]) < 1e-6, "PRICE6 RECON MISMATCH %s: %f vs %f" % (key, recon, use["res"])
    print("   PRICE6 RECONSTRUCTION OK: %.6f == %.6f" % (recon, use["res"]), flush=True)
    for j, n in enumerate(use["nodes"]):
        prodv = float(MA.val(sum(x["res"] * (MA.SEASON_PROG if i == 0 else (1 - MA.SEASON_PROG))
                                 for i, x in enumerate(n["projs"]))) if len(n["projs"]) == 2
                      else MA.val(n["projs"][0]["res"]))
        print("     node %d L=%8.3f  v_at_peak=%9.3f  val(raw)=%9.3f  floor=%9.3f  carried_by=%s"
              % (j, n["L"], n["res"], prodv, (n["floor"] or 0.0),
                 "FLOOR" if (n["floor"] is not None and n["floor"] >= prodv - 1e-9) else "integral"),
              flush=True)
    OUT[key] = dict(price=price, WQ6=WQ6, SCALE_DIST=dp.SCALE_DIST, SEASON_PROG=MA.SEASON_PROG,
                    SCALE=MA.SCALE, price6=use["res"], band=use["bb"], nodes=use["nodes"],
                    all_p6=[dict(res=c["res"], capt_off=c["capt_off"]) for c in P6],
                    C=p.get("year"), pos=MA.gfut(p), a_now=MA.age(p), player=p.get("player"),
                    all_proj_ok=all(x["ok"] for c in P6 for n in c["nodes"] for x in n["projs"]))
    print("   all in-call transcriptions ok: %s" % OUT[key]["all_proj_ok"], flush=True)
MA.proj_from_peak = O_PROJ; dp.v_at_peak = O_VAP; G["price6"] = O_P6; MA.prod_floor = O_FLOOR
json.dump(OUT, open(SP + "/r32_nodes_true.json", "w"), indent=1, default=str)
print("\nwrote", SP + "/r32_nodes_true.json", flush=True)
