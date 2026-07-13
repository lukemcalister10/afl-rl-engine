"""D4.1 (definitive over-line list) — the captaincy level a player is valued at = the k=0 lev fed to
capt_prem in the BOARD projection _proj_w4 (present-year). Reproduces the supervisor's Gawn 126.0/7.71,
Bont 119.5/5.50, Daicos 114.5/3.31. Ranks the players over CAPT_THRESH=107.4 and measures the saturation."""
import json
import harness as H
MA = H.MA; G = H.G; F = H.F; THRESH = MA.CAPT_THRESH
_proj0 = MA.proj_from_peak
_grab = {"lev": None}
def _proj_capture(g, lp, a, cur, lens, g0=None, fut=None, pre_hc=0.0):
    if _grab["lev"] is None and G["_BOARD_PATH"] and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
        pa = MA.PEAK_AGE[g]; cl = cur if cur else lp * MA.frac(a, pa)
        lev0 = lp * MA.frac(a, pa)
        if a <= pa: lev0 = max(lev0, cl)
        lev0 = max(lev0, cl)                       # k==0 rule
        _grab["lev"] = lev0
    return _proj0(g, lp, a, cur, lens, g0=g0, fut=fut, pre_hc=pre_hc)
MA.proj_from_peak = _proj_capture

def capt_level(p):
    _grab["lev"] = None
    MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
    H.ev(p)
    return _grab["lev"]

board = [p for p in H.players() if not G["delisted"](p)]
rows = []
for p in board:
    lv = capt_level(p)
    if lv is None: continue
    prem = MA.capt_prem(lv)
    rows.append((p["player"], MA.gfut(p), round(lv, 2), round(prem, 3)))
over = sorted([r for r in rows if r[3] > 1e-9], key=lambda r: -r[2])

# saturation: best vs 8th
sat = None
if len(over) >= 8:
    b, e = over[0], over[7]
    sat = dict(best=b[0], best_lev=b[2], best_prem=b[3], eighth=e[0], eighth_lev=e[2], eighth_prem=e[3],
               raw_scoring_gap=round(b[2]-e[2], 2), premium_gap=round(b[3]-e[3], 2))

out = dict(board="81e48293 (store b0c39d78, tagged v2.9)", THRESH=THRESH,
           n_board_evaluated=len(rows), n_over_line=len(over),
           over_line=[dict(player=r[0], pos=r[1], capt_level=r[2], premium_pts=r[3]) for r in over],
           saturation=sat)
json.dump(out, open("/home/user/afl-rl-engine/session_2026-07-13/measurement/out/d4_overline_clean.json", "w"), indent=1)
print(f"=== D4.1 OVER-LINE (present k=0 captain level) | board 81e48293 ===")
print(f"board players evaluated (non-delisted, projected): {len(rows)}")
print(f"OVER THE LINE (capt_level > {THRESH}): n={len(over)}")
for r in over: print(f"  {r[0]:24s} {r[1]:8s} capt_level={r[2]:7.2f}  premium={r[3]:.3f}")
print(f"\nSATURATION (best vs 8th): {sat}")
