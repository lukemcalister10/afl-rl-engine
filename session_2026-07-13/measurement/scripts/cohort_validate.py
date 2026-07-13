"""Validate the cohort re-pricer against the official matrix Vpath, and find capt-sensitive cells."""
import json, time
import harness as H
import cohort_repricer as CR
MA = H.MA
MPATH = "/home/user/afl-rl-engine/session_2026-07-13/measurement/out/matrix_baseline_tagged.json"
by_key = {p.get("key"): p for p in MA.data}
cells = CR.cohort_cells(MPATH)
print(f"cohort cells (incurve 2004-2020, depth<=7): {len(cells)}  distinct players: {len({c[0] for c in cells})}")

t0 = time.time()
# 1) validate: my price_asof(default capt) vs matrix Vpath — spot-check on a sample + all elite cells
import random
H.capt_default()
sample = cells[:: max(1, len(cells)//400)]   # ~400 spread sample
diffs = []
for key, C, N, y, vp in sample:
    p = by_key.get(key)
    if p is None: continue
    mine = CR.price_asof(p, y)
    if mine is None: continue
    diffs.append(abs(round(mine) - round(vp)))
import numpy as np
print(f"[t={time.time()-t0:.0f}s] VALIDATION on {len(diffs)} sampled cells: max|diff|={max(diffs)} mean|diff|={np.mean(diffs):.3f} exact={sum(d==0 for d in diffs)}/{len(diffs)}")

# 2) sensitive cells: capt_off vs capt_default differ (only these move under the ladder)
t1 = time.time()
sens = []
H.capt_default()
default_val = {}
for key, C, N, y, vp in cells:
    p = by_key.get(key)
    if p is None: continue
    default_val[(key, y)] = CR.price_asof(p, y)
H.capt_off()
for key, C, N, y, vp in cells:
    p = by_key.get(key)
    if p is None: continue
    off = CR.price_asof(p, y)
    dv = default_val.get((key, y))
    if dv is not None and off is not None and round(dv) != round(off):
        sens.append(dict(key=key, player=p["player"], C=C, N=N, year=y,
                         default=round(dv), capt_off=round(off), capt_scar=round(dv)-round(off)))
H.capt_default()
sens.sort(key=lambda s: -abs(s["capt_scar"]))
print(f"[t={time.time()-t1:.0f}s] CAPT-SENSITIVE cohort cells: {len(sens)}  (players: {len({s['key'] for s in sens})})")
for s in sens[:30]:
    print(f"  C{s['C']} N{s['N']} {s['player']:22s} default={s['default']:6d} off={s['capt_off']:6d} capt_scar={s['capt_scar']:+d}")
json.dump(dict(n_cells=len(cells), sensitive=sens),
          open("/home/user/afl-rl-engine/session_2026-07-13/measurement/out/cohort_sensitive.json", "w"), indent=1)
print("wrote out/cohort_sensitive.json")
