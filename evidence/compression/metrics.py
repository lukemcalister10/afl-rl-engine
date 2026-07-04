#!/usr/bin/env python3
"""
metrics.py  [BAKED c47cb43d]  READ-ONLY

Quantify + LOCATE the value-scale compression on the baked board.
Reads evidence/compression/dataset.json (built by build_dataset.py from
data/s4_matrix_baked_c47cb43d.json + frozen engine era/REF).

Value field:  V := cur   (live keeper value the owner ranks on)
              peakV := max(Vpath)  (age-neutral engine valuation)
Realised ref: era-normalised production
              recentP (last-2 seasons), peakP (best season), careerP (season-sum)

TRAPS handled explicitly:
  * value != scoring: value is a compressed monotone transform of production
    by design (pick floors, keeper age-decay, scarcity). We therefore measure
    RELATIVE spread (value-gap / realised-gap) and LOCAL elasticity, not raw $.
  * survivorship: the realised reference INCLUDES every drafted player in a
    settled cohort, busts at ~0 (never survivors-only), so the low tail is real.
  * state: every number is labelled [BAKED c47cb43d]; population masks printed.
"""
import json, os, numpy as np
from collections import Counter, defaultdict

D = os.path.dirname(__file__)
recs = json.load(open(os.path.join(D, 'dataset.json')))
TAG = '[BAKED c47cb43d]'
POS = ['MID', 'RUC', 'KEY_FWD', 'GEN_FWD', 'KEY_DEF', 'GEN_DEF']
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); out.append(s); print(s)

def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x)
    if n == 0 or x.sum() == 0: return float('nan')
    return float((2*np.arange(1, n+1)-n-1).dot(x)/(n*x.sum()))

def shape(v):
    v = np.asarray([x for x in v if x is not None], float)
    q = lambda p: float(np.percentile(v, p))
    d = dict(n=len(v), min=float(v.min()), p10=q(10), p25=q(25), p50=q(50),
             p75=q(75), p90=q(90), p95=q(95), p99=q(99), max=float(v.max()),
             mean=float(v.mean()), gini=round(gini(v), 3),
             cv=round(v.std()/v.mean(), 3) if v.mean() else float('nan'))
    d['p90_p50'] = round(d['p90']/d['p50'], 2) if d['p50'] else None
    d['p99_p50'] = round(d['p99']/d['p50'], 2) if d['p50'] else None
    d['p99_p90'] = round(d['p99']/d['p90'], 2) if d['p90'] else None   # TOP-END separation
    # top-decile mean / next-decile(p80-90) mean  -> elite clustering
    hi = v[v >= q(90)]; nxt = v[(v >= q(80)) & (v < q(90))]
    d['topdec_over_nextdec'] = round(hi.mean()/nxt.mean(), 2) if len(nxt) else None
    d['topdec_share'] = round(hi.sum()/v.sum(), 3)
    return d

live = [r for r in recs if not r['retired_now']]
def cur(r): return r['cur'] or 0
def pk(r):  return r['peakV'] or 0

# ============================================================================
P('='*78); P(f'{TAG}  COMPRESSION / SPREAD QUANTIFICATION')
P(f'source: data/s4_matrix_baked_c47cb43d.json   players={len(recs)}   engine md5=c47cb43d')
P('POPULATION: LIVE keeper board = retired_now==False   n=%d' % len(live))
P('  cpos:', dict(Counter(r['cpos'] for r in live)))
P('='*78)

# ---------------------------------------------------------------- SECTION A
P('\n### A. DISTRIBUTION SHAPE — value V=cur  (overall + per current-position)')
P('col: n  p10  p50  p90  p99  max | p90/p50 p99/p50 p99/p90 | topdec/nextdec top10%share gini cv')
def line(name, rows):
    s = shape([cur(r) for r in rows])
    P(f'{name:9s} {s["n"]:4d} {s["p10"]:6.0f} {s["p50"]:6.0f} {s["p90"]:7.0f} {s["p99"]:7.0f} {s["max"]:7.0f} | '
      f'{s["p90_p50"]:5} {s["p99_p50"]:6} {s["p99_p90"]:6} | '
      f'{s["topdec_over_nextdec"]:5} {s["topdec_share"]:6} {s["gini"]:5} {s["cv"]:5}')
    return s
shapes = {}
shapes['OVERALL'] = line('OVERALL', live)
for p in POS:
    shapes[p] = line(p, [r for r in live if r['cpos'] == p])

P('\n  read: p99/p90 is the TOP-END separation ratio (elite vs merely-good).')
P('  topdec/nextdec ~1.x means the top decile is barely above the next decile = clustering.')

# ---------------------------------------------------------------- SECTION A2
P('\n### A2. Same, but age-neutral engine valuation peakV=max(Vpath)')
P('  (isolates STRUCTURAL compression from current-snapshot age-decay)')
def line2(name, rows):
    s = shape([pk(r) for r in rows])
    P(f'{name:9s} {s["n"]:4d} {s["p10"]:6.0f} {s["p50"]:6.0f} {s["p90"]:7.0f} {s["p99"]:7.0f} {s["max"]:7.0f} | '
      f'{s["p90_p50"]:5} {s["p99_p50"]:6} {s["p99_p90"]:6} | {s["topdec_over_nextdec"]:5} {s["topdec_share"]:6}')
    return s
pkshapes = {'OVERALL': line2('OVERALL', live)}
for p in POS:
    pkshapes[p] = line2(p, [r for r in live if r['cpos'] == p])

# ---------------------------------------------------------------- SECTION B
P('\n### B. VALUE<->PRODUCTION TRANSFER  (realised reference, survivorship-aware)')
P('  population: LIVE players with >=3 real seasons (established); realised R=recentP,')
P('  engine V=cur. Both INCLUDE fringe low-producers (no survivors-only cut).')
est = [r for r in live if r['nseas'] >= 3 and r['recentP'] > 0]
R = np.array([r['recentP'] for r in est]); V = np.array([cur(r) for r in est])
P(f'  n={len(est)}   R(recentP) p50={np.median(R):.0f} p90={np.percentile(R,90):.0f} p99={np.percentile(R,99):.0f}')
# decile bins by realised production; median value per bin; local elasticity dlnV/dlnR
order = np.argsort(R); Rs, Vs = R[order], V[order]
nb = 10; edges = [int(i*len(Rs)/nb) for i in range(nb+1)]
P('  bin  R_med   V_med   (elasticity dlnV/dlnR vs previous bin)')
prev = None; elas = []
for i in range(nb):
    a, b = edges[i], edges[i+1]
    rm, vm = float(np.median(Rs[a:b])), float(np.median(Vs[a:b]))
    e = ''
    if prev and prev[0] > 0 and rm > prev[0] and vm > 0 and prev[1] > 0:
        el = (np.log(vm)-np.log(prev[1]))/(np.log(rm)-np.log(prev[0])); elas.append((i, el))
        e = f'  elast={el:.2f}' + ('  <-- <1 compresses' if el < 1 else '')
    P(f'  {i+1:3d}  {rm:6.1f}  {vm:7.0f}{e}')
    prev = (rm, vm)
# region elasticities
if elas:
    topE = np.mean([e for i, e in elas if i >= 8]); midE = np.mean([e for i, e in elas if 4 <= i <= 6])
    P(f'  TOP-region elasticity (top 2 bins)  = {topE:.2f}')
    P(f'  MID-region elasticity (bins 5-7)    = {midE:.2f}')
    P(f'  -> if TOP << MID, compression is LOCALISED at the elite top end.')

# cross-region value-gap vs realised-gap (compression index)
def gap(vals, hi_pct, ref_pct=50):
    vals = np.asarray(vals, float)
    return np.percentile(vals, hi_pct)/np.percentile(vals, ref_pct)
P('\n  compression index = value-gap / realised-gap  (per region, LIVE est. players)')
for label, hp in [('p99 vs p50 (elite vs median)', 99), ('p90 vs p50 (good vs median)', 90),
                  ('p75 vs p50 (upper-mid vs median)', 75)]:
    vg = gap(V, hp); rg = gap(R, hp); ci = vg/rg
    P(f'   {label:34s}: valuex{vg:.2f} / realisedx{rg:.2f} = {ci:.2f}'
      + ('   <-- value UNDER-separates' if ci < 1 else ''))

# ---------------------------------------------------------------- SECTION C
P('\n### C. ELITE SEPARATION — actual $ gaps (identity-level)')
def find(n): return next(r for r in recs if r['player'] == n)
P('  -- Petracca vs Bontempelli (owner flag) --')
pe, bo = find('Christian Petracca'), find('Marcus Bontempelli')
P(f'   Bontempelli  cur={bo["cur"]}  recentP={bo["recentP"]}  peakV={bo["peakV"]}  (pick{bo["pick"]}, {bo["year"]})')
P(f'   Petracca     cur={pe["cur"]}  recentP={pe["recentP"]}  peakV={pe["peakV"]}  (pick{pe["pick"]}, {pe["year"]})')
P(f'   VALUE gap cur: ${bo["cur"]-pe["cur"]:+d}  ({100*(bo["cur"]-pe["cur"])/pe["cur"]:+.1f}%)   '
  f'while Bont out-produces Petracca recentP {bo["recentP"]:.0f} vs {pe["recentP"]:.0f} '
  f'(+{100*(bo["recentP"]-pe["recentP"])/pe["recentP"]:.0f}%)')
P('   -> production says Bont clearly ahead; cur has them ~tied = top-end compression.')

P('\n  -- elite KEY_FWD cluster vs next tier --')
kfw = [('Josh Treacy',), ('Sam Darcy',), ('Riley Thilthorpe',), ('Cooper Duff-Tytler',), ('Jonty Faull',)]
for (n,) in kfw:
    r = find(n)
    P(f'   {n:20s} cur={r["cur"]:5}  recentP={r["recentP"]:6}  peakV={r["peakV"]:5}  (pick{r["pick"]}, {r["year"]}, nseas={r["nseas"]})')
tre, sd, thil = find('Josh Treacy'), find('Sam Darcy'), find('Riley Thilthorpe')
dt, fa = find('Cooper Duff-Tytler'), find('Jonty Faull')
elite_lo = min(sd['cur'], thil['cur'], tre['cur']); elite_hi = max(sd['cur'], thil['cur'], tre['cur'])
P(f'   within-cluster spread (cur): {elite_lo}..{elite_hi}  = ${elite_hi-elite_lo} ({elite_hi/elite_lo:.2f}x)')
P(f'   cluster-vs-next-tier gap: min elite {elite_lo} vs top next-tier {max(dt["cur"],fa["cur"])} '
  f'= ${elite_lo-max(dt["cur"],fa["cur"])} ({elite_lo/max(dt['cur'],fa['cur']):.2f}x)')
P('   NOTE state: Duff-Tytler nseas=1, Faull nseas=2 -> next-tier values are PROJECTION-anchored, not realised.')

# top-N clustering per elite position
P('\n  -- top-of-board clustering: gaps among the top 8 by cur --')
for p in ['MID', 'KEY_FWD']:
    top = sorted([r for r in live if r['cpos'] == p], key=cur, reverse=True)[:8]
    vals = [cur(r) for r in top]
    P(f'   {p}: ' + ' '.join(f'{r["player"].split()[-1]}:{cur(r)}' for r in top))
    diffs = [vals[i]-vals[i+1] for i in range(len(vals)-1)]
    P(f'      #1->#2 gap ${diffs[0]}  |  #2..#8 spread ${vals[1]-vals[-1]} across 6 places  '
      f'(avg step ${(vals[1]-vals[-1])//6})')

# ---------------------------------------------------------------- SECTION D
P('\n### D. TAIL STEEPNESS — implied value pick 1 vs pick 60')
fresh = [r for r in recs if r['year'] and r['year'] >= 2023 and r['nseas'] <= 1
         and r['type'] == 'ND' and r['pick'] and not r['pickless']]
P(f'  fresh ND draftees (2023-2026, <=1 season, value=anchor=pick-curve): n={len(fresh)}')
byp = defaultdict(list)
for r in fresh: byp[r['pick']].append(r['anchor'])
for target in [1, 2, 3, 5, 10, 20, 30, 40, 50, 60]:
    near = [r for r in fresh if abs(r['pick']-target) <= 3]
    if near:
        a = np.mean([r['anchor'] for r in near])
        P(f'   pick~{target:2d}: implied anchor ~{a:6.0f}   (n={len(near)}, picks {sorted(set(r["pick"] for r in near))})')
# draftval PVC pick1 vs deep
dv1 = [r['draftval'] for r in fresh if r['pick'] == 1]
P(f'  draftval(PVC) pick1 sample: {sorted(set(dv1))}')
p1 = np.mean([r['anchor'] for r in fresh if r['pick'] <= 2])
p60 = np.mean([r['anchor'] for r in fresh if 55 <= r['pick'] <= 65])
if p60:
    P(f'  implied pick~1 anchor {p1:.0f}  vs pick~60 anchor {p60:.0f}  = {p1/p60:.1f}x  (tail ratio)')

# ---------------------------------------------------------------- SECTION E
P('\n### E. REALISED SETTLED-COHORT SEPARATION (survivorship-aware)')
P('  cohorts drafted 2008-2016 (careers essentially complete). Include EVERY ND')
P('  drafted player, busts at ~0 (NOT survivors-only). realised R=careerP.')
settled = [r for r in recs if r['type'] == 'ND' and r['pick'] and r['year'] and 2008 <= r['year'] <= 2016]
Rc = np.array([r['careerP'] for r in settled])
Pkv = np.array([r['peakV'] for r in settled])
P(f'  n={len(settled)}   busts (careerP<50): {int((Rc<50).sum())}  ({100*(Rc<50).mean():.0f}%)')
sr = shape(Rc); sv = shape(Pkv)
P(f'  REALISED careerP : p50={sr["p50"]:.0f} p90={sr["p90"]:.0f} p99={sr["p99"]:.0f} | '
  f'p90/p50={sr["p90_p50"]} p99/p50={sr["p99_p50"]} p99/p90={sr["p99_p90"]} gini={sr["gini"]}')
P(f'  ENGINE peakV     : p50={sv["p50"]:.0f} p90={sv["p90"]:.0f} p99={sv["p99"]:.0f} | '
  f'p90/p50={sv["p90_p50"]} p99/p50={sv["p99_p50"]} p99/p90={sv["p99_p90"]} gini={sv["gini"]}')
P(f'  -> realised-vs-engine spread ratio:  p99/p50 {sr["p99_p50"]}/{sv["p99_p50"]}='
  f'{sr["p99_p50"]/sv["p99_p50"]:.2f}   p99/p90 {sr["p99_p90"]}/{sv["p99_p90"]}={sr["p99_p90"]/sv["p99_p90"]:.2f}')
P('  (>1 = players separated MORE in reality than the engine values them => engine under-separates)')

# ---------------------------------------------------------------- SECTION F
P('\n### F. UNIFORM vs LOCALISED VERDICT')
P('  compression index (value-gap/realised-gap) by POSITION, elite region p99/p50:')
ci_by_pos = {}
for p in POS:
    e = [r for r in live if r['cpos'] == p and r['nseas'] >= 3 and r['recentP'] > 0]
    if len(e) < 8:
        P(f'   {p:9s}: n={len(e)} (too few for stable p99)'); continue
    Vp = np.array([cur(r) for r in e]); Rp = np.array([r['recentP'] for r in e])
    ci = gap(Vp, 90)/gap(Rp, 90)   # p90 for stability at position-level n
    ci_by_pos[p] = ci
    P(f'   {p:9s}: n={len(e):3d}  value p90/p50={gap(Vp,90):.2f}  realised p90/p50={gap(Rp,90):.2f}  '
      f'index={ci:.2f}' + ('  <-- under-separates' if ci < 1 else ''))
if ci_by_pos:
    worst = min(ci_by_pos, key=ci_by_pos.get)
    P(f'  most-compressed position: {worst} (index {ci_by_pos[worst]:.2f})')
P('\n  region summary (LIVE established, from B): top-end elasticity vs mid-region elasticity')
P('  -> see Section B TOP vs MID elasticity; Section A p99/p90 top-end ratios per position.')

json.dump({'shapes_cur': shapes, 'shapes_peakV': pkshapes, 'ci_by_pos': ci_by_pos},
          open(os.path.join(D, 'metrics_out.json'), 'w'), indent=1, default=float)
open(os.path.join(D, 'metrics_report.txt'), 'w').write('\n'.join(out))
P('\nwrote metrics_out.json + metrics_report.txt')
