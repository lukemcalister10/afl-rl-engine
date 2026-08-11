"""ITEM C — the C-Q3 faller demonstration + the C-Q2 H ladder. READ-ONLY.

Conventions VERIFIED against all six of the directive's worked rows (exact match on w):
  g  = career games total ; sa = career games-weighted average
  par= par_at(pos, min(effpk,KMAX), T) with T = clip(draft_age-18, 1, 6)  [the eff_ten draft-age bridge]
  G  = g/(g+8) ; Q = clip(sa/par,0,2) ; gate = min(ev/entry_anchor, 1) ; w = G*Q*gate
"""
import sys, math, json
sys.path.insert(0, '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad')
from engine_load import load
import numpy as np
g_ = load()
MA = g_['MA']; cp = g_['cp']; PR = g_['PR']
ev = g_['ev']; entry_anchor = g_['entry_anchor']
G0, QMAX, Y = 8.0, 2.0, 2026
real = [p for p in MA.data if g_['_isreal'](p)]

def career(p):
    gt = num = 0.0
    for s in p['scoring']:
        if s['games'] <= 0: continue
        gt += s['games']; num += s['games'] * s['avg']
    return gt, (num / gt if gt else 0.0)

def parT(p):
    T = int(min(max(g_['_ageR'](p) - 18, 1), 6))
    return float(PR.par_at(MA.gfut(p), min(MA.effpk(p), cp.KMAX), T)), T

def wrow(p):
    gm, sa = career(p); par, T = parT(p)
    a = float(entry_anchor(p)); e = float(ev(p, Y))
    G = gm / (gm + G0) if gm > 0 else 0.0
    Q = float(np.clip(sa / par, 0, QMAX)) if par > 0 else 0.0
    gate = min(e / a, 1.0) if a > 0 else 0.0
    return dict(p=p, name=p.get('player'), pick=p.get('pick'), pos=MA.gfut(p), g=gm, sa=sa,
                par=par, G=G, Q=Q, gate=gate, w=G * Q * gate, anchor=a, e=e,
                ratio=(e / a if a > 0 else 0.0))

# ---------- the year-1 cohort: ND in-curve, draft class 2025 ----------
coh = [p for p in real if p.get('type') == 'ND' and not MA.is_pool(p) and p.get('year') == 2025]
print('YEAR-1 COHORT (ND in-curve, class 2025): n = %d   [directive says 58]' % len(coh))
rows = [wrow(p) for p in coh]
played = [r for r in rows if r['g'] > 0]
sitters = [r for r in rows if r['g'] == 0]
print('  played-only n=%d (mean w %.4f)   sitters w=0 n=%d   all-rows mean w %.4f  [directive: 34 / 0.3873 / 24 / 0.2271]'
      % (len(played), float(np.mean([r['w'] for r in played])) if played else 0, len(sitters),
         float(np.mean([r['w'] for r in rows]))))

# ---------- C-Q2: the H ladder on the PLAYED-ONLY basis ----------
# ceiling = taught_level_basis x (1 + w x (H-1)); the landing is mean(ceiling/anchor).
print('\n=== C-Q2  THE H LADDER (ceiling/anchor landing; target band [1.04, 1.13]) ===')
print(' %-6s %-14s %-14s' % ('H', 'played-only', 'all-rows'))
for H in (1.04, 1.06, 1.0945, 1.10, 1.13, 1.16, 1.20, 1.25, 1.30, 1.35, 1.40):
    lp = float(np.mean([1 + r['w'] * (H - 1) for r in played])) if played else 0.0
    la = float(np.mean([1 + r['w'] * (H - 1) for r in rows]))
    mark = '   <-- enters [1.04,1.13]' if 1.04 <= lp <= 1.13 else ''
    print(' %-6.4f %-14.4f %-14.4f%s' % (H, lp, la, mark))

# ---------- C-Q3: the faller demonstration ----------
print('\n=== C-Q3  THE FALLER DEMONSTRATION ===')
print('A faller = a top-10 pick whose record sits BELOW entry expectation (ev/entry_anchor < 1).')
print('The drafted gate min(ev/anchor,1) protects a row only where that ratio < 1.\n')
top10 = sorted([wrow(p) for p in real
                if p.get('type') == 'ND' and not MA.is_pool(p)
                and p.get('pick') is not None and p['pick'] <= 10
                and not p.get('_retired') and not g_['delisted'](p)
                and (p.get('year') or 0) >= 2019],                # THE COHORT BOOK: classes 2019-26
               key=lambda r: r['ratio'])
print(' top-10-pick rows in the cohort book (ND in-curve, classes 2019-26): %d' % len(top10))
print(' %-24s %-4s %-5s %-9s %-9s %-7s %-7s %-7s' % ('player', 'pk', 'pos', 'anchor', 'ev', 'ev/anc', 'gate', 'w'))
for r in top10[:12]:
    print(' %-24s %-4s %-5s %-9.1f %-9.1f %-7.3f %-7.3f %-7.4f'
          % (r['name'], r['pick'], r['pos'], r['anchor'], r['e'], r['ratio'], r['gate'], r['w']))
prot = [r for r in top10 if r['gate'] < 1.0]
print('\n TOP-10 PICKS WITH gate < 1.0 (i.e. actually protected): %d of %d' % (len(prot), len(top10)))
for r in prot[:10]:
    print('   %-24s pk%-3s ev/anchor=%.3f  gate=%.3f  w=%.4f' % (r['name'], r['pick'], r['ratio'], r['gate'], r['w']))

# named row from the directive
z = [r for r in top10 if r['name'] == 'Zeke Uwland']
if z:
    print('\n THE NAMED ROW — Zeke Uwland (pick 2): ev/anchor = %.3f -> gate = %.3f  (ABOVE entry: the gate does nothing)'
          % (z[0]['ratio'], z[0]['gate']))

# ---------- the designated fallback: the scoring-average check as C's gate ----------
print('\n=== THE DESIGNATED FALLBACK GATE (sa check, one reader, inside C) ===')
print('gate_sa = clip(sa/par, 0, 1) — the same sa/par reading Q already makes, clipped at 1 instead of 2,')
print('so C keeps ONE sa reader on the leg (the double-counting assertion holds by construction).')
print(' %-24s %-4s %-7s %-8s %-8s %-8s' % ('player', 'pk', 'sa/par', 'gate_z', 'gate_sa', 'w_sa'))
for r in top10[:12]:
    gsa = float(np.clip(r['sa'] / r['par'], 0, 1)) if r['par'] > 0 else 0.0
    print(' %-24s %-4s %-7.3f %-8.3f %-8.3f %-8.4f' % (r['name'], r['pick'], r['sa'] / r['par'] if r['par'] else 0,
                                                       r['gate'], gsa, r['G'] * r['Q'] * gsa))
psa = [r for r in top10 if (r['sa'] / r['par'] if r['par'] else 0) < 1.0]
print('\n TOP-10 PICKS PROTECTED BY THE sa GATE (sa/par < 1): %d of %d' % (len(psa), len(top10)))
