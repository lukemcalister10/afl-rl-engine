"""TASK 3 conservation sums + extra ITEM C sizing splits. READ-ONLY."""
import engine_load, json, numpy as np
g = engine_load.load()
MA = g['MA']; cp = g['cp']; PR = g['PR']; ev = g['ev']
entry_anchor = g['entry_anchor']; v0_start = g['v0_start']; _ageR = g['_ageR']
PL_F = g['_PL_F']; Y = 2026; G0 = 8.0; QMAX = 2.0; KMAX = int(cp.KMAX)
data = MA.data
B = json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))
A = B['active']
byk = {x['key']: x for x in A}

print('=== BOARD ===')
print('active rows            :', len(A))
print('board total  sum(v)    :', sum(x['v'] for x in A))
print('board keys of interest :', [k for k in B if 'ohort' in k or 'Total' in k])
print('draftAssetTotals       :', json.dumps(B['draftAssetTotals'])[:400])
print('cohort                 :', json.dumps(B['cohort'])[:600])
print('intakePickSum          :', B['intakePickSum'])
print('lensConservation       :', json.dumps(B['lensConservation'])[:300])

print()
print('=== YEAR-0 BOOK (entry anchors, board currency = engine/1.0524) ===')
real_on_board = [p for p in data if p['key'] in byk]
print('store rows priced on the board :', len(real_on_board))
tot_v0_eng = sum(entry_anchor(p) for p in real_on_board)
print('Sigma entry_anchor  engine ccy : %.1f' % tot_v0_eng)
print('Sigma entry_anchor  board  ccy : %.1f' % (tot_v0_eng / PL_F))
nd_curve = [p for p in real_on_board if p.get('type') == 'ND' and p.get('pick') is not None and not MA.is_pool(p)]
print('ND in-curve rows on board      :', len(nd_curve))
print('  Sigma entry_anchor board ccy : %.1f' % (sum(entry_anchor(p) for p in nd_curve) / PL_F))
print('  Sigma board v                : %d' % sum(byk[p['key']]['v'] for p in nd_curve))

print()
print('=== COHORT BOOK (the ITEM C consumer: year-1+ ND) ===')
for yr, lab in ((2025, 'draft class 2025 = year 1'), (2024, 'class 2024 = year 2'), (2023, 'class 2023 = year 3')):
    c = [p for p in nd_curve if p.get('year') == yr]
    print('  %-28s n=%3d  Sigma anchor(board) %9.1f  Sigma board v %8d'
          % (lab, len(c), sum(entry_anchor(p) for p in c) / PL_F, sum(byk[p['key']]['v'] for p in c)))
cohort_all = [p for p in nd_curve if (p.get('year') or 0) >= 2019]
print('  ND in-curve classes 2019-2026  n=%d  Sigma anchor(board) %.1f  Sigma board v %d'
      % (len(cohort_all), sum(entry_anchor(p) for p in cohort_all) / PL_F,
         sum(byk[p['key']]['v'] for p in cohort_all)))

print()
print('=== ITEM C w SPLITS on the year-1 ND cohort ===')
def career_g(p): return sum(x['games'] for x in p['scoring'])
def sa_career(p):
    t = career_g(p)
    return 0.0 if t == 0 else sum(x['games'] * x['avg'] for x in p['scoring']) / t
nd25 = [p for p in nd_curve if p.get('year') == 2025]
recs = []
for p in nd25:
    gg = career_g(p); sa = sa_career(p); a = entry_anchor(p); e = float(ev(p, Y))
    par = PR.par_at(MA.gfut(p), min(MA.effpk(p), KMAX), int(min(max(_ageR(p) - 17, 1), 6)))
    G = gg / (gg + G0); Q = min(max(sa / par, 0.0), QMAX)
    gate = min(max(e / a, 0.0), 1.0)
    recs.append(dict(key=p['key'], g=gg, w=G * Q * gate, e=e, a=a))
played = [r for r in recs if r['g'] > 0]
sat = [r for r in recs if r['g'] == 0]
for lab, rs in (('all 58', recs), ('played (g>0)', played), ('sat out (g=0)', sat)):
    if not rs: continue
    ws = np.array([r['w'] for r in rs])
    print('  %-14s n=%3d  mean w %.4f' % (lab, len(rs), ws.mean()), end='  ')
    for H in (1.04, 1.0945, 1.13):
        print('H%s->%.4f' % (H, 1 + ws.mean() * (H - 1)), end='  ')
    print()
print()
print('  per-row w (year-1 cohort, sorted desc):')
for r in sorted(recs, key=lambda r: -r['w'])[:20]:
    print('    %-28s g%-3d w %.4f' % (r['key'], r['g'], r['w']))
