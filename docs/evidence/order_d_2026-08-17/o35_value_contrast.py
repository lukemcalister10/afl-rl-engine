#!/usr/bin/env python3
"""ORDER D — THE DECISIVE CHECK: the fade-relevant, VALUE-BASED pick contrast (committed evidence).

The fade multiplies the entry price, so the decision-relevant object is not washout odds but
VALUE RETENTION: how much of his entry-relative forward value does a year-one sitter keep,
compared with a same-pick player who played 11+ games. F below 1 = sitting costs value; the
SHAPE of F over pick is the shape the ruled curve must follow. Player bootstrap CIs (B=1000,
seed 35) attached per band.
"""
import json, math
import numpy as np
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LB, LM, LW, LG = 105.0, 109.5, 1.85, 1.00
CARRY = 1.14


def sp(x): return math.log1p(math.exp(x)) if x < 30 else x
def cp(l):
    c = LG * LW * (sp((l - LM) / LW) - sp((LB - LM) / LW))
    return c if c > 0 else 0.0
def pv(x): return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
def ws(g): return min(1.0, math.sqrt(max(0.0, g) / 10.0))


A = json.load(open(SP + '/per_entrant_O32RFINAL.json'))
FM = {'paddy-mccartin', 'thomas-boyd'}
rows = []
for r in A['recs']:
    if r['key'] in FM or not (r.get('teaches_curve') and r['type'] == 'ND'):
        continue
    if not (2005 <= r['year'] <= 2020) or not r.get('pick') or not (1 <= r['pick'] <= 64):
        continue
    # remaining delivered value from year 2 onward, discounted to year 1 (after the observed sit/play year)
    dv = 0.0
    for s in r['seasons']:
        if s['year'] > 2025 or s.get('bar') not in BARS:
            continue
        if s['year'] >= r['year'] + 2:
            dv += (CARRY ** -(s['year'] - (r['year'] + 1))) * ws(s['games']) * pv(s['avg'] + cp(s['avg']) - BARS[s['bar']]) * 21.0
    rows.append(dict(pick=r['pick'], g1=int(r.get('games_yr1') or 0), v0=float(r['v0']), dv=dv))

print('value-based fade contrast by pick region: F = mean(remaining/v0 | sat) / mean(remaining/v0 | 11+)')
print('%-8s %6s %6s %10s %10s %8s' % ('band', 'n_sat', 'n_11+', 'ret_sat', 'ret_11+', 'F'))
xs, ys, ns = [], [], []
for nm, lo, hi in (('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)):
    sat = [r for r in rows if lo <= r['pick'] <= hi and r['g1'] == 0]
    ctl = [r for r in rows if lo <= r['pick'] <= hi and r['g1'] >= 11]
    rs = sum(r['dv'] for r in sat) / sum(r['v0'] for r in sat)
    rc = sum(r['dv'] for r in ctl) / sum(r['v0'] for r in ctl)
    F = rs / rc if rc > 0 else float('nan')
    mid = math.exp(0.5 * (math.log(lo) + math.log(hi)))
    xs.append(math.log(mid)); ys.append(F); ns.append(len(sat))
    print('%-8s %6d %6d %10.3f %10.3f %8.3f' % (nm, len(sat), len(ctl), rs, rc, F))
# weighted log-linear trend of F on ln pick
X = np.column_stack([np.ones(len(xs)), xs])
w = np.array(ns, float)
b = np.linalg.solve((X.T * w) @ X, (X.T * w) @ np.log(np.clip(ys, 1e-6, None)))
print('weighted fit: ln F = %.4f %+.4f * ln(pick)  -> F rises with pick? %s' % (b[0], b[1], b[1] > 0))
# per-band bootstrap CIs on F
rng = np.random.default_rng(35)
print('%-8s %10s %22s' % ('band', 'F', '90% CI (player bootstrap)'))
OUTJ = {}
for nm, lo, hi in (('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)):
    sat = [r for r in rows if lo <= r['pick'] <= hi and r['g1'] == 0]
    ctl = [r for r in rows if lo <= r['pick'] <= hi and r['g1'] >= 11]
    fs = []
    for _ in range(1000):
        ss = [sat[i] for i in rng.integers(0, len(sat), len(sat))]
        cc = [ctl[i] for i in rng.integers(0, len(ctl), len(ctl))]
        den_s = sum(r['v0'] for r in ss); den_c = sum(r['v0'] for r in cc)
        rc = sum(r['dv'] for r in cc) / den_c if den_c else 0
        if rc > 0:
            fs.append((sum(r['dv'] for r in ss) / den_s) / rc)
    F0 = (sum(r['dv'] for r in sat) / sum(r['v0'] for r in sat)) / (sum(r['dv'] for r in ctl) / sum(r['v0'] for r in ctl))
    ci = [float(np.percentile(fs, 5)), float(np.percentile(fs, 95))]
    OUTJ[nm] = dict(F=F0, ci90=ci, n_sat=len(sat), n_ctl=len(ctl))
    print('%-8s %10.3f       [%.3f, %.3f]' % (nm, F0, ci[0], ci[1]))
import json as _j, os as _o
_j.dump(dict(order='ORDER D decisive check — value-based sit contrast by pick',
             F_by_band=OUTJ, weighted_lnF_slope_on_lnpick=float(b[1]),
             reading='the SHAPE the ruled curve must follow; F highest at 1-10 = top-10 sitters '
                     'retain the MOST entry-relative value — the OPPOSITE of the ruled direction'),
        open(_o.path.join(_o.path.dirname(_o.path.abspath(__file__)), 'O35_VALUE_CONTRAST.json'), 'w'), indent=1, sort_keys=True)
print('written: O35_VALUE_CONTRAST.json')
