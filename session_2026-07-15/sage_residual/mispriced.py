#!/usr/bin/env python3
"""Current-store players the S_AGE zero touches: implied (Lo) vs measured (Lo + s_real*gap).
Read-only; writes only under the fence. Evaluates at Y=2025 (last completed season -> unpinned age,
matches the historical realised measurement). s_real(age) = kernel-smoothed slope from the residual run."""
import io, contextlib, os, csv
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
import config_manifest; config_manifest.enforce()
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']
_lvlcurr=g['_lvlcurr']; _nqual=g['_nqual']; _radq=g['_radq']; _S_AGE=g['_S_AGE']
lvl_orig=cp._lvl_eff_orig; PROVEN_N=g['PROVEN_N']; TOL_M1=g['TOL_M1']
data=[p for p in MA.data if MA.GRP.get(p.get('pos')) and not p.get('_retired')]

# kernel-smoothed s_real(age) from the residual measurement (h=1.5), hard-coded from residual_by_age.csv
S_REAL = {29:0.379, 30:0.236, 31:0.061, 32:-0.061, 33:-0.147, 34:-0.359, 35:-0.743, 36:-1.046}
# raw age-only central (for the honest CI-includes-zero flag)
S_RAW  = {29:0.551, 30:-0.476, 31:-0.396, 32:0.829, 33:-0.047}

Y=2025  # last completed season: unpinned age, realised-consistent
recs=[]
for p in data:
    if _nqual(p,Y) < PROVEN_N: continue
    Lo=lvl_orig(p,Y); Lc=_lvlcurr(p,Y); gap=Lc-Lo
    if gap < TOL_M1 or not _radq(p,Y,Lo): continue
    age=cp._age_asof(p,Y)
    if age is None or age < 29: continue
    a=int(round(age))
    s=S_REAL.get(a, S_REAL[36]); implied=Lo; measured=Lo + s*gap
    recs.append(dict(player=p['player'], pos=p['pos'], by=p.get('_by'),
                     age_2025=a, age_2026=(2026-p['_by']) if p.get('_by') else '',
                     Lo=round(Lo,2), Lc=round(Lc,2), gap=round(gap,2),
                     sage_engine=round(_S_AGE(age),3), s_real=round(s,3),
                     implied_level=round(implied,2), measured_level=round(measured,2),
                     mispricing_lvlpts=round(measured-implied,2)))

recs.sort(key=lambda r: -abs(r['mispricing_lvlpts']))
with open(os.path.join(OUT,'mispriced_30plus.csv'),'w',newline='') as f:
    wr=csv.DictWriter(f, fieldnames=list(recs[0].keys())); wr.writeheader(); wr.writerows(recs)

print(f"# current (Y=2025) proven up-branch (gap>=5, radq) players age>=29: {len(recs)}")
print(f"{'player':<24}{'pos':<9}{'age26':>6}{'Lo':>8}{'Lc':>8}{'gap':>7}{'s_real':>8}{'implied':>9}{'measur':>9}{'mispx':>8}")
for r in recs:
    print(f"{r['player']:<24}{r['pos']:<9}{str(r['age_2026']):>6}{r['Lo']:>8}{r['Lc']:>8}{r['gap']:>7}{r['s_real']:>8}{r['implied_level']:>9}{r['measured_level']:>9}{r['mispricing_lvlpts']:>+8}")

# split 30+ (as asked) vs the 29 companion where the signal is robust
print("\n# ---- age 30+ (the strict question; measured slope CI INCLUDES ZERO -> exposure, not confident mispricing) ----")
for r in [x for x in recs if x['age_2025']>=30]:
    print(f"  {r['player']:<22} age {r['age_2026']}  Lo {r['Lo']}  Lc {r['Lc']}  gap {r['gap']}  implied {r['implied_level']}  measured {r['measured_level']}  ({r['mispricing_lvlpts']:+} lvl)")
print("\n# ---- age 29 companion (fade arrives a year early; realised +0.55, 0 OUTSIDE CI -> the robust signal) ----")
for r in [x for x in recs if x['age_2025']==29]:
    print(f"  {r['player']:<22} age {r['age_2026']}  Lo {r['Lo']}  Lc {r['Lc']}  gap {r['gap']}  implied {r['implied_level']}  measured {r['measured_level']}  ({r['mispricing_lvlpts']:+} lvl)")
