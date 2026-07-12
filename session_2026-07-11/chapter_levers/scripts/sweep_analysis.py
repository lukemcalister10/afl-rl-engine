"""SWEEP analysis — one comparison table from the four boards (15/14/13/12 %/yr), read-only.
Anchor set / per-position + per-age-band mean d%/step / top-15 movers per step / board-level guard
margins per rate + the break-rate line. G-COHORT (book-level) recomputed at the extreme arm only
(12%; separate matrix) — appended by sweep_gcohort.py.
Usage: sweep_analysis.py <board15> <board14> <board13> <board12> <out.md>
"""
import json, sys

paths = dict(zip(('15', '14', '13', '12'), sys.argv[1:5]))
OUTMD = sys.argv[5]
boards = {r: {p['key']: p for p in json.load(open(f))['active']} for r, f in paths.items()}
RATES = ('15', '14', '13', '12')
L = []

ANCH = ['max-gawn', 'kieren-briggs', 'marcus-bontempelli', 'dylan-patterson', 'tobie-travaglia',
        'lachlan-carmichael', 'zeke-uwland', 'kysaiah-pickett', 'sam-darcy', 'willem-duursma']
L.append('## Anchor set at each rate (SCAR; levered board)')
L.append('| player | 15%/yr (SHIPPED) | 14% | 13% | 12% | 15→12 Δ% |')
L.append('|---|---|---|---|---|---|')
for k in ANCH:
    vs = [boards[r][k]['v'] for r in RATES]
    L.append(f"| {k} | **{vs[0]}** | {vs[1]} | {vs[2]} | {vs[3]} | {100*(vs[3]-vs[0])/vs[0]:+.1f}% |")

L.append('\n## A-GAWN ordering + A-BONT floor at each rate')
L.append('| rate | gawn | briggs | gawn−briggs (margin) | bont | vs 3246 pin (×1.0524 re-denominated) |')
L.append('|---|---|---|---|---|---|')
for r in RATES:
    g, b, m = boards[r]['max-gawn']['v'], boards[r]['kieren-briggs']['v'], boards[r]['marcus-bontempelli']['v']
    L.append(f"| {r}% | {g} | {b} | {g-b:+d} ({100*(g-b)/b:+.1f}%) | {m} | {100*(m-3246)/3246:+.1f}% |")

L.append('\n## Per-position and per-age-band mean Δ% per 1-pt rate step (vs the 15% shipped board)')
import collections
def dpct(r, k):
    a, b = boards['15'][k]['v'], boards[r][k]['v']
    return 100 * (b - a) / a if a else 0.0
keys = [k for k in boards['15'] if all(k in boards[r] for r in RATES) and boards['15'][k]['v'] >= 20]
L.append('| slice | n | 15→14 | 15→13 | 15→12 |')
L.append('|---|---|---|---|---|')
for tag, sel in [('pos ' + p, lambda k, p=p: boards['15'][k]['gf'] == p) for p in ('MID', 'GEN_DEF', 'GEN_FWD', 'KEY_DEF', 'KEY_FWD', 'RUC')] + \
                [('age ' + a, lambda k, lo=lo, hi=hi: lo <= boards['15'][k]['age'] <= hi) for a, lo, hi in
                 (('≤21', 0, 21), ('22-25', 22, 25), ('26-29', 26, 29), ('30+', 30, 99))]:
    ks = [k for k in keys if sel(k)]
    if not ks: continue
    ms = [sum(dpct(r, k) for k in ks) / len(ks) for r in ('14', '13', '12')]
    L.append(f"| {tag} | {len(ks)} | {ms[0]:+.1f}% | {ms[1]:+.1f}% | {ms[2]:+.1f}% |")

for r in ('14', '13', '12'):
    mv = sorted(((dpct(r, k), k) for k in keys), key=lambda t: -abs(t[0]))[:15]
    L.append(f'\n## Top-15 movers, 15% → {r}% (|Δ%|, value ≥20 SCAR)')
    L.append('| player | 15% | ' + r + '% | Δ% | pos | age |')
    L.append('|---|---|---|---|---|---|')
    for d, k in mv:
        L.append(f"| {k} | {boards['15'][k]['v']} | {boards[r][k]['v']} | {d:+.1f}% | {boards['15'][k]['gf']} | {boards['15'][k]['age']} |")

L.append('\n## Board-level guard margins at each rate (registry anchors computable from the board)')
def margins(r):
    B = boards[r]
    out = {}
    out['A1 duursma>uwland'] = 100 * (B['willem-duursma']['v'] - B['zeke-uwland']['v']) / B['zeke-uwland']['v']
    out['A5 ginnivan≥1600'] = 100 * (B['jack-ginnivan']['v'] - 1600) / 1600
    out['A5 bowey≥2100'] = 100 * (B['jake-bowey']['v'] - 2100) / 2100
    out['A5 blakey≥2600'] = 100 * (B['nick-blakey']['v'] - 2600) / 2600
    out['A8 berry≥2×tsatas'] = 100 * (B['sam-berry']['v'] / B['elijah-tsatas']['v'] - 2.0) / 2.0
    out['A9 ginnivan>ward'] = 100 * (B['jack-ginnivan']['v'] - B['josh-ward']['v']) / B['josh-ward']['v']
    out['A11 farrow>patterson'] = 100 * (B['jacob-farrow']['v'] - B['dylan-patterson']['v']) / B['dylan-patterson']['v']
    out['A11 cumming>annable'] = 100 * (B['sam-cumming']['v'] - B['daniel-annable']['v']) / B['daniel-annable']['v']
    out['A-GAWN gawn>briggs'] = 100 * (B['max-gawn']['v'] - B['kieren-briggs']['v']) / B['kieren-briggs']['v']
    out['A-BONT ≥3246'] = 100 * (B['marcus-bontempelli']['v'] - 3246) / 3246
    return out
allm = {r: margins(r) for r in RATES}
L.append('| margin (% above its bar) | 15% | 14% | 13% | 12% |')
L.append('|---|---|---|---|---|')
for k in allm['15']:
    L.append(f"| {k} | " + ' | '.join(f"{allm[r][k]:+.1f}%" for r in RATES) + ' |')
for r in RATES:
    n3 = sorted(allm[r].items(), key=lambda t: t[1])[:3]
    L.append(f"- three narrowest at {r}%: " + ' · '.join(f"{k} {v:+.1f}%" for k, v in n3))

# break-rate line
brk = []
for k in ('A-GAWN gawn>briggs', 'A-BONT ≥3246'):
    xs = [(int(r), allm[r][k]) for r in RATES]
    neg = [r for r, v in xs if v <= 0]
    if neg:
        brk.append(f'{k} BREAKS at {max(neg)}%/yr')
    else:
        r1, v1 = xs[0]; r2, v2 = xs[-1]
        slope = (v2 - v1) / (r2 - r1)  # % margin per rate point (negative rate direction)
        est = r1 - v1 / slope if slope != 0 else None
        brk.append(f'{k}: margin {v1:+.1f}%@15 → {v2:+.1f}%@12 (does NOT break in-range' +
                   (f'; linear extrapolation crosses ≈{est:.0f}%/yr)' if est and 0 < est < 15 else '; no in-range or extrapolated crossing)'))
L.append('\n**BREAK-RATE LINE:** ' + ' · '.join(brk))
open(OUTMD, 'w').write('\n'.join(L) + '\n')
print('\n'.join(L[-8:]))
print('wrote', OUTMD)
