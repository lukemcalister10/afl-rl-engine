"""Year-1 ND cohort landing instrument, re-run on the CURRENT matrix, + ITEM C H-sizing."""
import engine_load, math, json, numpy as np
g = engine_load.load()
MA = g['MA']; cp = g['cp']; PR = g['PR']; ev = g['ev']
entry_anchor = g['entry_anchor']; v0_start = g['v0_start']
_ageR = g['_ageR']; PL_F = g['_PL_F']
Y = 2026; G0 = 8.0; QMAX = 2.0
KMAX = int(cp.KMAX)
data = MA.data

def career_g(p): return sum(x['games'] for x in p['scoring'])
def sa_career(p):
    t = career_g(p)
    return 0.0 if t == 0 else sum(x['games'] * x['avg'] for x in p['scoring']) / t

def cohort(pred):
    return [p for p in data if pred(p)]

def landing(rows, label):
    r = []
    for p in rows:
        a = entry_anchor(p); e = float(ev(p, Y))
        if a > 0: r.append(e / a)
    r = np.array(r)
    print('%-58s n=%4d  mean %.4f  median %.4f  sum/sum %.4f'
          % (label, len(r), r.mean(), np.median(r), sum(float(ev(p, Y)) for p in rows) / sum(entry_anchor(p) for p in rows)))
    return r

print('=== LANDING INSTRUMENT VARIANTS (current matrix, board data 4b448a82 / store d9a24282) ===')
nd25 = cohort(lambda p: p.get('type') == 'ND' and p.get('pick') is not None
              and not MA.is_pool(p) and p.get('year') == 2025)
landing(nd25, 'A: ND in-curve, draft class 2025 (year 1)')
nd25p = cohort(lambda p: p.get('type') == 'ND' and p.get('year') == 2025)
landing(nd25p, 'B: ALL type-ND draft class 2025 (incl. ND65+ pool)')
nd25pl = cohort(lambda p: p.get('type') == 'ND' and p.get('pick') is not None
                and not MA.is_pool(p) and p.get('year') == 2025 and career_g(p) > 0)
landing(nd25pl, 'C: A, played-only (g>0)')
allyr1 = cohort(lambda p: p.get('year') == 2025 and cp.debutyr(p) == 2026)
landing(allyr1, 'D: every 2025-intake row on any route')

print()
print('=== ITEM C SIZING on cohort A (ND in-curve class 2025) ===')
recs = []
for p in nd25:
    gg = career_g(p); sa = sa_career(p)
    a = entry_anchor(p); e = float(ev(p, Y))
    par = PR.par_at(MA.gfut(p), min(MA.effpk(p), KMAX), int(min(max(_ageR(p) - 17, 1), 6)))
    G = gg / (gg + G0); Q = min(max(sa / par, 0.0), QMAX)
    gate = min(max(e / a, 0.0), 1.0); w = G * Q * gate
    recs.append(dict(key=p['key'], g=gg, sa=sa, a=a, e=e, G=G, Q=Q, gate=gate, w=w))
ws = np.array([r['w'] for r in recs])
print('n=%d  mean w %.4f  median w %.4f  n(w=0) %d  max w %.4f'
      % (len(ws), ws.mean(), np.median(ws), int((ws < 1e-9).sum()), ws.max()))
print()
print('  H       mean ceiling/anchor   capped landing (mean min(e,ceil)/a)   vs capped-at-anchor baseline')
base = np.mean([min(r['e'], r['a']) / r['a'] for r in recs])
print('  (cap = anchor exactly, i.e. w=0 everywhere)  capped landing = %.4f' % base)
for H in (1.04, 1.0945, 1.13):
    ratio = np.mean([1 + r['w'] * (H - 1) for r in recs])
    capped = np.mean([min(r['e'], r['a'] * (1 + r['w'] * (H - 1))) / r['a'] for r in recs])
    print('  %-7s %18.4f %30.4f %20.4f' % (H, ratio, capped, capped - base))
print()
print('  UNCAPPED landing (no ceiling at all, = variant A above) = %.4f'
      % np.mean([r['e'] / r['a'] for r in recs]))
