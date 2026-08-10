"""SEAT verification — independent re-derivation of the deciding figures.
Own arithmetic + own cohort selection; only the loader is shared."""
import engine_load, math
g = engine_load.load()
MA = g['MA']; cp = g['cp']; PR = g['PR']; ev = g['ev']
entry_anchor = g['entry_anchor']; _ageR = g['_ageR']; PL_F = g['_PL_F']
Y = 2026; KMAX = int(cp.KMAX)

def w_of(p, gg=None, sa=None):
    sc = p['scoring']
    tg = sum(x['games'] for x in sc)
    if gg is None: gg = tg
    if sa is None: sa = (sum(x['games']*x['avg'] for x in sc)/tg) if tg else 0.0
    pos = MA.gfut(p); pk = min(MA.effpk(p), KMAX)
    T = int(min(max(_ageR(p) - 17, 1), 6))
    par = PR.par_at(pos, pk, T)
    a = entry_anchor(p); e = float(ev(p, Y))
    G = gg/(gg+8.0); Q = min(max(sa/par, 0.0), 2.0)
    gate = min(e/a, 1.0)
    return dict(g=gg, sa=round(sa,2), par=round(par,2), anchor=round(a,1),
                e=round(e,1), G=round(G,4), Q=round(Q,4), gate=round(gate,4),
                w=round(G*Q*gate,4))

def get(k): return next(p for p in MA.data if p.get('key')==k)

print('MRAZ   ', w_of(get('noah-mraz')))
print('CONWAY ', w_of(get('toby-conway')))
print('CONW-1H', w_of(get('toby-conway'), gg=1, sa=120.0))
print('Z.UWL  ', w_of(get('zeke-uwland')))
print('BEECKEN', w_of(get('luke-beecken')))

# cohort: ND in-curve, draft class 2025 (year 1 in 2026)
coh = [p for p in MA.data if p.get('type')=='ND' and p.get('year')==2025
       and MA.effpk(p) <= 64]
n = len(coh)
ratios = [float(ev(p,Y))/entry_anchor(p) for p in coh]
ws = [w_of(p)['w'] for p in coh]
played = [p for p in coh if sum(x['games'] for x in p['scoring']) > 0]
wp = [w_of(p)['w'] for p in played]
anch_book = sum(entry_anchor(p) for p in coh)/PL_F
print('COHORT n=%d  landing mean(ev/anchor)=%.4f  sum-ratio=%.4f' %
      (n, sum(ratios)/n, sum(float(ev(p,Y)) for p in coh)/sum(entry_anchor(p) for p in coh)))
print('mean w (all)=%.4f  n_played=%d  mean w (played)=%.4f  zero-g rows=%d' %
      (sum(ws)/n, len(played), sum(wp)/len(wp), sum(1 for p in coh if sum(x['games'] for x in p['scoring'])==0)))
print('year-1 anchor book (board ccy) = %.1f' % anch_book)
for H in (1.04, 1.0945, 1.13):
    print('H=%.4f  mean ceil/anchor (all)=%.4f  (played)=%.4f' %
          (H, 1 + (sum(ws)/n)*(H-1), 1 + (sum(wp)/len(wp))*(H-1)))
