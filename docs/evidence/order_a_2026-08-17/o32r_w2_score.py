#!/usr/bin/env python3
"""ORDER A REPAIR — the W2 scorer on the REPAIRED matrix, plus the corrected-surface scorecard
and the band-level fair-yr1 benchmarks (PREREG_32R amendments A1/A2, addendum 3).

Plain words: this runs the same committed measuring stick as before (nothing re-invented), then
scores the repaired candidate two ways — (a) on the original flat-bar surface, for continuity of
record, and (b) on the CORRECTED age-fair surface, which is the repair's own yardstick. It also
computes, for each pick band and pool arm, the FAIR year-1 mark for that band: 1.14 x (1 - the
share of the band's forward value it delivers in year 1). A band that delivers early should
appreciate less; one that delivers nothing yet should appreciate near the full 14% carry.
"""
import os, sys, json, hashlib, io, contextlib, math

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
SRC = os.path.join(EV, 'order33_w2_2026-08-17', 'w2_forward_calibration.py')

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
SUBS = [
    ("CAND_P = SP + '/per_entrant_O31FFINAL.json'", "CAND_P = SP + '/per_entrant_O32RFINAL.json'"),
    ("assert md5f(CAND_P) == 'd97f1aee4161ebcf785cd635ed095038', 'matrix md5 mismatch'",
     "assert md5f(CAND_P) == 'f43003083af56e4d5074e0f38c2bb605', 'matrix md5 mismatch'"),
    ("assert A['meta']['engine_head'] == '71d9949a', 'engine head mismatch'",
     "assert A['meta']['engine_head'] == 'bf63592c', 'engine head mismatch'"),
    ("print('identity OK: matrix md5 d97f1aee store cb38ef11 head 71d9949a n=2648')",
     "print('identity OK: matrix md5 f4300308 store cb38ef11 head bf63592c n=2648')"),
    ("with open(os.path.join(HERE, 'RESULTS_W2.json'), 'w') as f:",
     "with open(os.path.join(%r, 'W2_32R_RESULTS.json'), 'w') as f:" % HERE),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique: %r' % a[:70]
    _run = _run.replace(a, b)
print('W2 SCORER RUN WHOLE — committed md5 %s, as-run md5 %s' % (HARNESS_MD5, hashlib.md5(_run.encode()).hexdigest()))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(_run, SRC, 'exec'), {'__name__': '__main__', '__file__': SRC})
open(os.path.join(HERE, 'W2_32R_console.txt'), 'w').write(buf.getvalue())

import numpy as np
R = json.load(open(os.path.join(HERE, 'W2_32R_RESULTS.json')))
per = {r['cls']: r['R_cand'] for r in R['level']['per_class_all']}
mean_0515 = float(np.mean([per[y] for y in range(2005, 2016)]))
mx = max(per.values()); mn = min(per.values())
slope = R['spread']['S1']['b']
W_flat = R['spread']['S2']['W_cand']
cells = R['spread']['S3']['buckets']
terc_flat = R['spread']['S3']['terciles']

# ---- corrected-surface metrics: recompute with the age-fair classifier ----------------------------
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
TALL = {'KPD', 'KPF', 'RUCK'}
D_TALL = {18: 22.334475609756097, 19: 20.55500752464971, 20: 16.306362402208926,
          21: 11.588672690048071, 22: 7.826894964594814, 23: 6.439783302063788}
D_SMALL = {18: 20.080511089352214, 19: 20.080511089352214, 20: 14.306977484301457,
           21: 11.265167414136857, 22: 6.761247284555768, 23: 4.584052475875439}


def age_gap(pos, age):
    if age is None or age >= 24:
        return 0.0
    return (D_TALL if pos in TALL else D_SMALL)[max(18, min(23, int(age)))]


S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
CARRY = 1.14


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(l):
    c = LCAPT_G * LCAPT_W * (softplus((l - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        return t if t in ('RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS') else 'OTHERPOOL'
    return None


A = json.load(open(SP + '/per_entrant_O32RFINAL.json'))
Arecs = {r['key']: r for r in A['recs']}
FM = {'paddy-mccartin', 'thomas-boyd'}
SV, SVA1 = {}, {}
for k, r in Arecs.items():
    d = {}
    yr = r['year']; aged = r.get('age_draft')
    for s in r['seasons']:
        if s['year'] > 2025:
            continue
        gp = s.get('bar')
        if gp not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - BARS[gp]) * 21.0
        if s['year'] == yr + 1:
            a1 = (aged + 1) if aged is not None else None
            SVA1[k] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - (BARS[gp] - age_gap(gp, a1))) * 21.0
    SV[k] = d


def dv_h6(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if Y < t <= Y + 6)


def dv_full(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


POP = []
for k, r in Arecs.items():
    if k in FM:
        continue
    arm = arm_of(r)
    if arm is None:
        continue
    yr = r['year']
    if yr < 2005 or yr > 2021:
        continue
    POP.append(dict(key=k, yr=yr, arm=arm, pick=r.get('pick'), v0=float(r['v0']),
                    p1=float(r['vpath'][0]), g1=int(r.get('games_yr1') or 0),
                    sv1=SV[k].get(yr + 1, 0.0), sv1_age=SVA1.get(k, 0.0),
                    dv1_h6=dv_h6(k, yr + 1), dv0_full=dv_full(k, yr), dv1_full=dv_full(k, yr + 1)))

CLASSES_H6 = list(range(2005, 2019))
rows_s = []
for y in CLASSES_H6:
    rows = [q for q in POP if q['yr'] == y]
    mp1 = np.mean([q['p1'] for q in rows]); mdv = np.mean([q['dv1_h6'] for q in rows])
    mA = np.mean([q['sv1_age'] for q in rows]) or 1.0
    mped = np.mean([q['v0'] for q in rows])
    for q in rows:
        rows_s.append(dict(key=q['key'], g1=q['g1'], x=q['p1'] / mp1, y=q['dv1_h6'] / mdv,
                           prodA=q['sv1_age'] / mA, ped=q['v0'] / mped))
X = np.array([r['x'] for r in rows_s]); Yv = np.array([r['y'] for r in rows_s])
PRA = np.array([r['prodA'] for r in rows_s]); PD = np.array([r['ped'] for r in rows_s])


def ols(Xm, yv):
    A1 = np.column_stack([np.ones(len(yv))] + list(Xm))
    b, *_ = np.linalg.lstsq(A1, yv, rcond=None)
    return b


bc = ols([PRA, PD], X)
W_age = float(bc[1] / bc[2])
bh = ols([PRA, PD], Yv)
W_hind_age = float(bh[1] / bh[2])


def bucket(g):
    if g == 0: return '0'
    if g <= 4: return '1-4'
    if g <= 9: return '5-9'
    if g <= 15: return '10-15'
    return '16+'


TERC_AGE = {}
for b in ('5-9',):
    rs = sorted([r for r in rows_s if bucket(r['g1']) == b], key=lambda r: r['prodA'])
    n3 = len(rs) // 3
    for nm, seg in (('poor', rs[:n3]), ('mid', rs[n3:2 * n3]), ('riser', rs[2 * n3:])):
        TERC_AGE['%s/%s' % (b, nm)] = dict(n=len(seg),
                                           price=float(np.mean([r['x'] for r in seg])),
                                           real=float(np.mean([r['y'] for r in seg])))
        TERC_AGE['%s/%s' % (b, nm)]['gap'] = TERC_AGE['%s/%s' % (b, nm)]['real'] - TERC_AGE['%s/%s' % (b, nm)]['price']

# ---- band-level fair yr1 (addendum 3): 1.14 x (1 - band yr1 delivered share) ----------------------
def nd_band(pk):
    if pk is None: return None
    if pk <= 10: return '1-10'
    if pk <= 20: return '11-20'
    if pk <= 30: return '21-30'
    if pk <= 40: return '31-40'
    if pk <= 64: return '41-64'
    return None


BANDS_OUT = {}
for grp, sel in ([(b, (lambda q, b=b: q['arm'] == 'ND' and nd_band(q['pick']) == b)) for b in
                  ('1-10', '11-20', '21-30', '31-40', '41-64')] +
                 [(arm, (lambda q, a=arm: q['arm'] == a)) for arm in
                  ('RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS')]):
    rows = [q for q in POP if sel(q)]
    if not rows:
        continue
    sv1 = sum(SV[q['key']].get(q['yr'] + 1, 0.0) for q in rows)
    dv1 = sum(q['dv1_full'] for q in rows)
    sh = sv1 / (sv1 + dv1) if (sv1 + dv1) > 0 else float('nan')
    fair = CARRY * (1.0 - sh) if sh == sh else float('nan')
    Rb = sum(q['p1'] for q in rows) / sum(q['v0'] for q in rows)
    BANDS_OUT[grp] = dict(n=len(rows), yr1_delivered_share=sh, fair_yr1=fair, mark_yr1=Rb,
                          gap_vs_fair=Rb - fair)

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

P('==== REPAIRED CANDIDATE — W2 SCORECARD, BOTH SURFACES ====')
P('flat-bar surface (continuity of record): mean 2005-15 %.4f | classes [%.4f, %.4f] | slope %.4f | W %.4f'
  % (mean_0515, mn, mx, slope, W_flat))
P('  hard 1.14 line: max class %.4f -> %s' % (mx, 'PASS' if mx <= 1.14 else 'FAIL'))
P('  g=0 gap %.4f (band +-0.10) -> %s' % (cells['0']['gap'], 'PASS' if abs(cells['0']['gap']) <= 0.10 else 'FAIL'))
P('')
P('CORRECTED (age-fair) surface — the repair\'s own yardstick:')
P('  W (age-adjusted prod leg): candidate %.4f vs hindsight %.4f, CI [0.3117, 0.5560] -> %s'
  % (W_age, W_hind_age, 'IN BAND' if 0.3117 <= W_age <= 0.5560 else 'OUT'))
P('  5-9g terciles (price vs realized, age-fair cuts):')
for tk, t in TERC_AGE.items():
    P('    %-10s n %3d  price %.3f  realized %.3f  gap %+.3f' % (tk, t['n'], t['price'], t['real'], t['gap']))
P('')
P('BAND-LEVEL FAIR YR1 (addendum 3): fair = 1.14 x (1 - the band\'s own year-1 delivered share)')
P('  %-8s %5s %14s %10s %10s %12s' % ('band', 'n', 'yr1 dlv share', 'fair yr1', 'mark yr1', 'gap vs fair'))
for grp, d in BANDS_OUT.items():
    P('  %-8s %5d %14.3f %10.3f %10.3f %+12.3f' % (grp, d['n'], d['yr1_delivered_share'], d['fair_yr1'], d['mark_yr1'], d['gap_vs_fair']))

json.dump(dict(flat=dict(mean_0515=mean_0515, min_class=mn, max_class=mx, slope=slope, W=W_flat,
                         cells={b: cells[b] for b in cells}, terciles=terc_flat),
               corrected=dict(W_cand_age=W_age, W_hind_age=W_hind_age, W_ci=[0.3117, 0.5560],
                              terciles_age=TERC_AGE),
               band_fair_yr1=BANDS_OUT, per_class=per),
          open(os.path.join(HERE, 'W2_32R_SCORECARD.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'W2_32R_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: W2_32R_RESULTS.json / W2_32R_SCORECARD.json / W2_32R_out.txt')
