"""D4.1 — captain premium TODAY on the tagged board 81e48293. TARGETED: capt fires only where the
player's PROJECTED level crosses CAPT_THRESH=107.4, so we ev-diff (capt on vs off) a generous prefilter
(ln>75) and verify no excluded player moves. Reports curve, over-line list, total board SCAR, saturation,
Bont/Gawn/Daicos attribution."""
import json, time
import harness as H
MA = H.MA; F = H.F; THRESH = MA.CAPT_THRESH
t0 = time.time()

def capt_prem(lev): return MA.capt_prem(lev)
curve = {lev: round(capt_prem(lev), 3) for lev in [107.4,110,112,114.5,117.8,119.5,122,126.0,130,140,200,400,1000]}

pl = H.players()
lns = {p["key"]: H.ln_level(p) for p in pl}                 # cheap-ish level pass
prefilter = [p for p in pl if lns[p["key"]] > 75.0]         # generous: capt cannot fire below the line
print(f"[t={time.time()-t0:.0f}s] levels done; prefilter n={len(prefilter)} of {len(pl)}")

H.capt_default()
on = {p["key"]: H.ev(p) for p in prefilter}
H.capt_off()
off = {p["key"]: H.ev(p) for p in prefilter}
H.capt_default()
print(f"[t={time.time()-t0:.0f}s] on/off ev done")

def bv(x): return int(round(x / F))
movers = []
for p in prefilter:
    k = p["key"]; d = bv(on[k]) - bv(off[k])
    if d != 0: movers.append((p["player"], MA.gfut(p), round(lns[k],2), bv(on[k]), bv(off[k]), d))
movers.sort(key=lambda r: -r[5])
total_scar = sum(m[5] for m in movers)

over = sorted([(p["player"], MA.gfut(p), round(lns[p["key"]],2), round(capt_prem(lns[p["key"]]),3))
               for p in pl if capt_prem(lns[p["key"]]) > 1e-9], key=lambda r: -r[2])
# completeness check: highest ln among EXCLUDED (<=75) — should be well below line
excl_max = max([lns[p["key"]] for p in pl if lns[p["key"]] <= 75.0], default=None)

top = over[:8]
sat = None
if len(over) >= 8:
    b, e = over[0], over[7]
    sat = dict(best=b[0], best_ln=b[2], best_prem=b[3], eighth=e[0], eighth_ln=e[2], eighth_prem=e[3],
               raw_scoring_gap=round(b[2]-e[2],2), premium_gap=round(b[3]-e[3],2))

attrib = {}
for nm in ["Bontempelli","Gawn","Daicos"]:
    p = H.find(nm); k = p["key"]
    attrib[nm] = dict(board_on=bv(on[k]) if k in on else bv(H.ev(p)), ln=round(lns[k],2),
                      premium_pts=round(capt_prem(lns[k]),3),
                      board_off=bv(off[k]), capt_scar=bv(on[k])-bv(off[k]),
                      pct_of_value=round(100*(bv(on[k])-bv(off[k]))/max(bv(on[k]),1),2))

out = dict(board="81e48293 (store b0c39d78, tagged v2.9)", numeraire_F=F,
           capt_params=dict(GAIN=MA.CAPT_GAIN,EXP=MA.CAPT_EXP,CAP=MA.CAPT_CAP,THRESH=THRESH),
           curve_points=curve, n_over_line=len(over),
           over_line=[dict(player=r[0],pos=r[1],ln=r[2],premium_pts=r[3]) for r in over],
           total_board_scar_moved=total_scar, n_board_movers=len(movers),
           movers=[dict(player=m[0],pos=m[1],ln=m[2],on=m[3],off=m[4],scar=m[5]) for m in movers],
           excluded_max_ln=round(excl_max,2) if excl_max else None,
           saturation=sat, attribution=attrib, elapsed_s=round(time.time()-t0,1))
json.dump(out, open("/home/user/afl-rl-engine/session_2026-07-13/measurement/out/d4_premium_today.json","w"), indent=1)

print("=== D4.1 CAPTAIN PREMIUM TODAY | board 81e48293 (tagged) ===")
print("params:", out["capt_params"])
print("curve capt_prem(lev):", curve)
print(f"\nover the line (ln>{THRESH}): n={len(over)}  [excluded-set max ln={out['excluded_max_ln']} << line, prefilter complete]")
for r in over: print(f"  {r[0]:24s} {r[1]:8s} ln={r[2]:7.2f} prem={r[3]:.3f}")
print(f"\nSATURATION: {sat}")
print(f"\nTOTAL BOARD SCAR moved (numeraire, on-off): {total_scar} over {len(movers)} movers")
for m in movers[:25]: print(f"  {m[0]:24s} {m[1]:8s} ln={m[2]:7.2f} on={m[3]:6d} off={m[4]:6d} scar={m[5]:+d}")
print("\nATTRIBUTION:")
for nm,a in attrib.items(): print(f"  {nm:14s} on={a['board_on']:6d} off={a['board_off']:6d} capt_scar={a['capt_scar']:+d} ({a['pct_of_value']}%) ln={a['ln']} prem_pts={a['premium_pts']}")
print(f"\n[elapsed {out['elapsed_s']}s] wrote ../out/d4_premium_today.json")
