"""PER-PLAYER AGE-SHARE CROSS-SECTIONS on the LIVE BOARD (origin/main @ ef7eff8).
Players: willem-duursma, zak-butters, marcus-bontempelli.

METHOD — exact, not modelled.  The shipped board's forward integral is `_proj_w4`
(_merged_recover.py:909-931), which REPLACES MA.proj_from_peak at load (:932).  It has TWO branches:
with a live W4 context it runs the per-k certainty-weighted loop; with ctx None it delegates to the
pre-W4 loop (rl_model.py:581-599).  The context is per-player state torn down when ev() returns, so
it MUST be snapshotted at call time -- the first version of this script did not, replayed the wrong
branch with Wk=1.0, and the transcription assert caught it (mismatch 4661.01 vs 4734.97 on
willem-duursma).  That is what the assert is for; it stays.

  (1) wrap MA.proj_from_peak; during the engine's own ev(p) capture, per call, the exact argument
      tuple, the result, AND a snapshot of _W4CTX['on'] and _BOARD_PATH;
  (2) RESTORE that context, re-call the engine's own function, and assert it reproduces the recorded
      result (proves the restoration is faithful);
  (3) run a verbatim transcription of whichever branch the context selects and assert it equals the
      engine's value to 1e-9.
If both asserts hold the per-age table IS the engine's own integral, term by term.
Only labelled approximation: mapping a projected AGE to a CAREER YEAR via the stored draft year.

CURRENCY: engine PLAYER board points, pick-1 anchored at 3000 -- the live board's own units.
READ-ONLY.
"""
import os, sys, io, json, contextlib, hashlib, time
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
WD = SP + "/rwm"
REPO = SP + "/repoM"
os.environ.setdefault("RL_REPO", REPO)
os.environ.setdefault("RL_FV", REPO + "/engine/forward_valuation")
# main@ef7eff8's OWN committed data/v0surf.pkl carries this build's config signature
# af556bdca53dee20d4f73e0ae25a8127.  Without this the resolver (_merged_recover.py:1290-1291)
# prefers a stale /home/claude/v0surf.pkl and the frozen-signature guard correctly HALTS.
os.environ["RL_V0SURF_PKL"] = REPO + "/data/v0surf.pkl"
sys.path.insert(0, "/home/claude/rl_vendor")
sys.path.insert(0, REPO)
sys.path.insert(0, REPO + "/engine/forward_valuation")
os.chdir(WD); sys.path.insert(0, ".")
print("engine basis: origin/main @ ef7eff8 ; store md5 %s"
      % hashlib.md5(open(WD + "/rl_model_data.json", "rb").read()).hexdigest()[:8], flush=True)
print("loading engine (_merged_recover, main basis) ...", flush=True)
_t0 = time.time()
src = open("_merged_recover.py").read().split('print("=== AFTER')[0]
G = {"__name__": "_r27"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G["MA"]; ev = G["ev"]
print("engine loaded in %.0fs. BASE_REF=%s AGE_REF=%s" % (time.time() - _t0, MA.BASE_REF, MA.AGE_REF),
      flush=True)

TARGETS = ["willem-duursma", "zak-butters", "marcus-bontempelli"]
players = {p.get("key"): p for p in MA.data if p.get("key") in TARGETS}
print("found:", sorted(players), flush=True)

ORIG = MA.proj_from_peak
CALLS = []


def rec(g, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0):
    """Capture AND transcribe IN-CALL, while every module flag the loop reads is live.
    Replaying later is wrong: player_raw outside raw_ev's context takes the pre-W4 branch."""
    ctx = G["_W4CTX"]["on"]
    bp = G["_BOARD_PATH"]
    r = ORIG(g, lp, a, cur, lens, g0=g0, fut=fut, pre_hc=pre_hc)
    c = dict(g=g, lp=lp, a=a, cur=cur, lens=lens, g0=g0, fut=fut, pre_hc=pre_hc,
             res=r, ctx=(dict(ctx) if ctx is not None else None), bp=bp)
    tot, rows, extra = transcribe(c)          # <-- same instant, live state
    c.update(tot=tot, rows=rows, extra=extra, ok=bool(abs(tot - r) < 1e-9))
    CALLS.append(c)
    return r


def transcribe(c):
    """verbatim transcription of whichever branch the captured context selects."""
    g, lp, a, cur, lens = c["g"], c["lp"], c["a"], c["cur"], c["lens"]
    g0, fut, pre_hc, ctx, bp = c["g0"], c["fut"], c["pre_hc"], c["ctx"], c["bp"]
    if g0 is None: g0 = g
    if fut is None: fut = [(g, 1.0)]
    pa = MA.PEAK_AGE[g]; d = MA.LENS[lens]; prod = 0.0; rows = []
    if ctx is None:
        # ---- rl_model.py:581-599 (the pre-W4 loop) ----
        branch = "pre-W4"; ah = a
        cl = cur if cur else lp * MA.frac(a, pa)
        for k in range(18):
            ag = a + k
            if ag > 38 or MA.frac(ag, pa) < 0.42: break
            lev = lp * MA.frac(ag, pa)
            if ag <= pa: lev = max(lev, cl)
            if k == 0: lev = max(lev, cl)
            if k == 0 and pre_hc > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026: lev *= (1 - pre_hc)
            base = lev + MA.capt_prem(lev)
            if k == 0: term = MA.posval(base - MA.REPL[g0]) * 21 / ((1 + d) ** k)
            else: term = sum(w * MA.posval(base - MA.REPL[gg]) for gg, w in fut) * 21 / ((1 + d) ** k)
            prod += term
            rows.append(dict(k=k, age=ag, lev=lev, base=base, Wk=1.0, disc=(1 + d) ** k, pv=term))
    else:
        # ---- _merged_recover.py:909-931 (the shipped W4 loop) ----
        branch = "W4"
        _off = (MA.AGE_REF - MA.BASE_REF) if G["_LEGF_ON"] else 0
        ah = a - _off if _off > 0 else a
        cl = cur if cur else lp * MA.frac(ah, pa)
        for k in range(18):
            ag = ah + k
            if ag > 38 or MA.frac(ag, pa) < 0.42: break
            lev = lp * MA.frac(ag, pa)
            if ag <= pa: lev = max(lev, cl)
            if k == 0: lev = max(lev, cl)
            if k == 0 and pre_hc > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026: lev *= (1 - pre_hc)
            if bp and k == ctx.get("ret_k", -1) and ctx.get("ret_hc", 0.0) > 0: lev *= (1 - ctx["ret_hc"])
            base = lev + MA.capt_prem(lev)
            Wk = G["_w4_W"](k, ctx)
            if k == 0: term = Wk * MA.posval(base - MA.REPL[g0]) * 21 / ((1 + d) ** k)
            else: term = Wk * sum(w * MA.posval(base - MA.REPL[gg]) for gg, w in fut) * 21 / ((1 + d) ** k)
            prod += term
            rows.append(dict(k=k, age=ag, lev=lev, base=base, Wk=Wk, disc=(1 + d) ** k, pv=term))
    keymul = 1.05 if g in ("KPF", "KPD") else 1.0
    runway = MA.clamp((25 - ah) / 6.0, 0, 1); elite = MA.clamp((lp / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
    kick = (1 + runway * elite * MA.PMAX)
    prod *= keymul * kick
    for r in rows: r["pv"] *= keymul * kick
    return prod, rows, dict(branch=branch, keymul=keymul, runway=runway, elite=elite, kick=kick,
                            cl=cl, pa=pa, d=d, ah=ah)


OUT = {}
for key in TARGETS:
    p = players.get(key)
    if p is None: print("  MISSING:", key, flush=True); continue
    print("  pricing %s ..." % key, flush=True)
    CALLS.clear()
    MA.proj_from_peak = rec
    with contextlib.redirect_stdout(io.StringIO()):
        price = ev(p, 2026)
    MA.proj_from_peak = ORIG
    with contextlib.redirect_stdout(io.StringIO()):
        gf, pe, ag_, ln = MA.gfut(p), MA.peak_est(p), MA.age(p), MA.level_now(p)
    print("    ev=%s, %d calls captured; target args g=%s lp=%.4f a=%s cur=%s"
          % (price, len(CALLS), gf, pe, ag_, ln), flush=True)
    # the production-integral call: the one player_raw makes, matched on all four level/age args
    def match(c):
        return (c["g"] == gf and abs(c["lp"] - pe) < 1e-9 and abs(c["a"] - ag_) < 1e-9
                and ((c["cur"] is None and ln is None) or
                     (c["cur"] is not None and ln is not None and abs(c["cur"] - ln) < 1e-9)))
    for i, c in enumerate(CALLS):
        print("      call %2d g=%-4s lp=%9.4f a=%-5s cur=%-8s lens=%-4s ctx=%-4s res=%10.3f ok=%s"
              % (i, c["g"], c["lp"], c["a"], c["cur"], c["lens"],
                 ("live" if c["ctx"] is not None else "None"), c["res"], c["ok"]), flush=True)
    cands = [c for c in CALLS if match(c) and c["lens"] in ("bal", "balanced")]
    if not cands:
        # the production-integral call is the one player_raw makes: ctx LIVE, g==gfut, a==age.
        cands = [c for c in CALLS if c["ctx"] is not None and c["g"] == gf
                 and abs(c["a"] - ag_) < 1e-9 and c["lens"] in ("bal", "balanced")]
        print("    no all-arg match; %d ctx-live g/a matches" % len(cands), flush=True)
    assert cands, "no production-integral call identified for %s" % key
    pick = cands[-1]
    tot, rows, extra = pick["tot"], pick["rows"], pick["extra"]
    assert pick["ok"], \
        "TRANSCRIPTION MISMATCH %s: %.10f vs %.10f (branch %s)" % (key, tot, pick["res"], extra["branch"])
    print("    OK  branch=%s  ctx=%s  engine %.6f == transcribed(in-call) %.6f"
          % (extra["branch"], "live" if pick["ctx"] is not None else "None", pick["res"], tot),
          flush=True)
    with contextlib.redirect_stdout(io.StringIO()):
        pf = float(MA.prod_floor(p, "bal"))
        unpl = float(MA._PVC2M[min(MA.effpk(p), 70)] * MA.los_decay(p) * MA.debut_factor(p))
        vfn = float(MA.value(p, "bal"))
    prod_v = float(MA.val(pick["res"]))     # the BOARD's production integral (ctx live), not a replay
    OUT[key] = dict(price=price, call={k: v for k, v in pick.items() if k != "ctx"},
                    ctx_keys=(sorted(pick["ctx"]) if pick["ctx"] else None),
                    rows=rows, extra=extra, a_now=ag_, C=p.get("year"), pos=gf,
                    pick_no=p.get("pick"), games=p.get("games"), level_now=ln, peak_est=pe,
                    seasons=[dict(year=s["year"], games=s["games"], avg=s["avg"]) for s in p["scoring"]],
                    n_calls=len(CALLS), SCALE=MA.SCALE, prod_v=prod_v, prod_floor=pf,
                    unpl_eq=unpl, value_fn=vfn, player=p.get("player"),
                    # EVERY node of the forward distribution, with its own per-age terms, so the
                    # age-share can be tested for stability across nodes (the node weights live in
                    # the distribution layer and are NOT visible here -- see the report).
                    nodes=[dict(lp=c["lp"], res=c["res"], ok=c["ok"],
                                rows=[dict(k=r["k"], age=r["age"], lev=r["lev"], Wk=r["Wk"],
                                           disc=r["disc"], pv=r["pv"]) for r in c["rows"]])
                           for c in CALLS])

json.dump(OUT, open(SP + "/r27_xsec.json", "w"), indent=1, default=str)
print("wrote", SP + "/r27_xsec.json", flush=True)
