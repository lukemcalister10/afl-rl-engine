"""D2 — the G-Y0 seam re-measure on the TAGGED BAKED board 81e48293 (store b0c39d78), in the NUMERAIRE.
Construction (as the original): weighted-mean position-conditioned V0 per pick band vs derived PVC per band;
deviations; the y0 -> wk1 -> y1 trough -> y2 recovery chain (walk-forward). The original (session
v2_9_continuation) was PRE-BAKE/PRE-NUMERAIRE: comp-weighted V0 > PVC in every band (+19..+281). We re-quote
on the baked board in the numeraire and state whether the conclusion survives."""
import json
import numpy as np
import harness as H
MA = H.MA; cp = H.cp; G = H.G; F = H.F
v0_start = G["v0_start"]; BANDS = MA.BANDS; PVC = MA.PVC
BASE = "/home/user/afl-rl-engine/session_2026-07-13/measurement"

# unit check: v0_start is raw ev-space (pick-1 ~3157); PVC is engine-pinned (RL_PICK1=3000). Put BOTH in numeraire.
def num(x): return x / F   # raw ev -> numeraire

# pick-1 anchor sanity
nd = [p for p in MA.data if G["_isreal"](p) and p.get("type") == "ND" and p.get("pick")]
pk1 = [p for p in nd if p.get("pick") == 1]
v0_pk1 = np.mean([v0_start(p) for p in pk1]) if pk1 else None

# per-band: comp-weighted V0 (mean over real ND players whose recorded pick sits in the band) vs derived PVC
def bandlabel(lo, hi): return f"{lo}-{hi}"
seam = []
for lo, hi in BANDS:
    grp = [p for p in nd if lo <= (p.get("pick") or 999) <= hi]
    if not grp: continue
    v0_raw = np.mean([v0_start(p) for p in grp])           # comp-weighted (natural position mix in the band), RAW ev units
    v0_num = num(v0_raw)                                    # numeraire = raw/F
    pvc_raw = np.mean([PVC[min(p.get("pick"), 99)] for p in grp])   # derived PVC over the same picks, RAW (RL_PICK1=3000 pin)
    pvc_band = num(pvc_raw)                                 # SAME numeraire divisor as V0 (both raw/F) — sign is unit-invariant
    seam.append(dict(band=bandlabel(lo, hi), n=len(grp),
                     posmix={pos: sum(1 for p in grp if MA.gfut(p) == pos) for pos in sorted({MA.gfut(p) for p in grp})},
                     compwt_V0_numeraire=round(v0_num, 1), derived_PVC=round(pvc_band, 1),
                     deviation=round(v0_num - pvc_band, 1),
                     deviation_pct=round(100 * (v0_num - pvc_band) / pvc_band, 2)))

all_pos = all(s["deviation"] > 0 for s in seam)
net = round(sum(s["deviation"] for s in seam), 1)

# the y0 -> wk1 -> y1 trough -> y2 recovery chain (walk-forward), aggregate over the ND curve pool, in numeraire.
# y0 = V0 (draft start); y1 = end-of-calendar-yr1 anchor; y2 = depth-2. From the official matrix (numeraire).
m = json.load(open(BASE + "/out/matrix_baseline_tagged.json"))
inc = [v for k, v in m.items() if not k.startswith("__") and v["incurve"] and 2004 <= int(v["year"]) <= 2020]
def depth(v, N):
    return v["Vpath"][N-1] if len(v["Vpath"]) >= N and v["Vpath"][N-1] is not None else None
y1 = [num(depth(v,1)) for v in inc if depth(v,1) is not None]
y2 = [num(depth(v,2)) for v in inc if depth(v,2) is not None]
# V0 (y0) for the same pool, by key
by_key = {p.get("key"): p for p in nd}
y0 = [num(v0_start(by_key[v["key"]])) for v in inc if v.get("key") in by_key]
chain = dict(y0_V0_mean=round(float(np.mean(y0)),1), y1_mean=round(float(np.mean(y1)),1),
             y2_mean=round(float(np.mean(y2)),1),
             shape=f"y0={round(np.mean(y0))} -> y1={round(np.mean(y1))} -> y2={round(np.mean(y2))}",
             y1_below_y0=float(np.mean(y1)) < float(np.mean(y0)),
             y2_above_y1=float(np.mean(y2)) > float(np.mean(y1)))

out = dict(board="81e48293 (store b0c39d78, tagged baked v2.9)", numeraire_F=F,
           v0_pick1_raw=round(float(v0_pk1),1) if v0_pk1 else None,
           v0_pick1_numeraire=round(num(v0_pk1),1) if v0_pk1 else None, PVC_pick1=PVC[1],
           seam_table=seam, all_bands_V0_gt_PVC=all_pos, net_deviation=net, chain=chain)
json.dump(out, open(BASE + "/out/d2_gy0.json", "w"), indent=1)
print("=== D2 G-Y0 SEAM (tagged baked board 81e48293, numeraire) ===")
print(f"pick-1 anchor: V0_raw={out['v0_pick1_raw']} V0/F={out['v0_pick1_numeraire']} PVC[1]={PVC[1]}")
print(f"{'band':8s} {'n':>4s} {'V0(num)':>9s} {'PVC':>8s} {'dev':>8s} {'dev%':>7s}")
for s in seam:
    print(f"{s['band']:8s} {s['n']:4d} {s['compwt_V0_numeraire']:9.1f} {s['derived_PVC']:8.1f} {s['deviation']:8.1f} {s['deviation_pct']:6.2f}%")
print(f"\nall bands V0 > PVC: {all_pos}   net deviation (numeraire): {net}")
print(f"CHAIN: {chain['shape']}  (y1<y0={chain['y1_below_y0']}, y2>y1={chain['y2_above_y1']})")
print("wrote out/d2_gy0.json")
