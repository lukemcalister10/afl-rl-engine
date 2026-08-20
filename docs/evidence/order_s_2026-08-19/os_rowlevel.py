#!/usr/bin/env python3
"""ORDER S — the two row-level predictions scored. Pure JSON reads. NO ENGINE RUN.

  S1-P5  rows whose bad seasons are OLD gain; rows whose bad seasons are RECENT lose. Scored as the
         correlation between a row's PRICE MOVE and its SURPLUS MOVE under the recency dial.
  S5-P4  the Setterfield-shaped population — 24+, ABOVE the age bar, BELOW the pedigree bar — is the
         one that moves most under the mature premium. WATCHED, NEVER TARGETED.
"""
import json, os, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
L = []


def P(s=''):
    print(s); L.append(str(s))


def cen(t):
    return {r['key']: r for r in json.load(open(os.path.join(HERE, 'CENSUS_%s.json' % t)))['charge']}


def board(t):
    q = SP + '/os/bb_%s/rl_after/rl_app_data.json' % t
    return {r['key']: r['v'] for r in json.load(open(q))['active']}


P('=' * 118)
P('ORDER S — THE TWO ROW-LEVEL PREDICTIONS. CONSEQUENCES, NEVER TARGETS.')
P('=' * 118)

B1, W = cen('SB1'), cen('SW47')
vB1, vW = board('SB1'), board('SW47')
xs, ys = [], []
for k in B1:
    if k not in W or k not in vB1 or k not in vW:
        continue
    if not B1[k].get('cond') or B1[k].get('s_ped') is None or W[k].get('s_ped') is None:
        continue
    ds = W[k]['s_ped'] - B1[k]['s_ped']          # surplus move under the recency dial
    dp = vW[k] - vB1[k]                          # price move, board points
    xs.append(ds); ys.append(dp)
xs = np.array(xs); ys = np.array(ys)
r = float(np.corrcoef(xs, ys)[0, 1]) if len(xs) > 2 else float('nan')
mv = xs[ys != 0]
P()
P('S1-P5 — DOES THE PRICE MOVE TRACK THE SURPLUS MOVE UNDER THE RECENCY DIAL?')
P('  rows with a charge and a surplus on both boards : %d' % len(xs))
P('  rows whose PRICE moves                          : %d  (%d up, %d down)'
  % (int((ys != 0).sum()), int((ys > 0).sum()), int((ys < 0).sum())))
P('  rows whose SURPLUS RISES under recency (recent seasons BETTER than old): %d' % int((xs > 0).sum()))
P('  rows whose SURPLUS FALLS under recency (recent seasons WORSE  than old): %d' % int((xs < 0).sum()))
P('  PEARSON r between the surplus move and the price move: %+.4f' % r)
P('  S1-P5 bar was r > +0.80: %s' % ('RIGHT' if r > 0.80 else 'WRONG'))
P()
P('  THE ASYMMETRY THAT EXPLAINS THE BOARD FALLING. The surplus moves BOTH ways in almost equal')
P('  numbers, but the charge is CONVEX in the surplus below the centre and FLAT above it — a row')
P('  already producing above its bar pays nothing and cannot pay less, while a row below it pays')
P('  more when its recent seasons are its worse ones. So a symmetric change in the surplus produces')
P('  an ASYMMETRIC change in the board, and the board falls. MEASURED:')
up = ys[xs > 0]; dn = ys[xs < 0]
P('    rows whose surplus ROSE : %d, net price %+d points, of which %d moved at all'
  % (len(up), int(up.sum()), int((up != 0).sum())))
P('    rows whose surplus FELL : %d, net price %+d points, of which %d moved at all'
  % (len(dn), int(dn.sum()), int((dn != 0).sum())))
P()

# ---- S5-P4 -------------------------------------------------------------------------------------
P('S5-P4 — THE WATCHED SHAPE UNDER THE MATURE PREMIUM (24+, ABOVE the age bar, BELOW the pedigree bar)')
M = cen('SM'); vM = board('SM')
pop = {'the watched shape': [], 'other 24+': [], 'under 24': []}
for k, r0 in B1.items():
    if k not in vM or k not in vB1:
        continue
    a = r0.get('age')
    if a is None:
        continue
    if a < 24:
        pop['under 24'].append(k); continue
    sa, sp = r0.get('s_age'), r0.get('s_ped')
    if sa is not None and sp is not None and sa > 0 and sp < 0:
        pop['the watched shape'].append(k)
    else:
        pop['other 24+'].append(k)
P('  %-22s %7s %9s %12s %14s' % ('population', 'rows', 'movers', 'net points', 'per mover'))
S5 = {}
for lab, ks in pop.items():
    d = [vM[k] - vB1[k] for k in ks]
    nm = sum(1 for x in d if x != 0)
    S5[lab] = dict(n=len(ks), movers=nm, net=sum(d),
                   per=(sum(d) / nm if nm else 0.0))
    P('  %-22s %7d %9d %+12d %14.1f' % (lab, len(ks), nm, sum(d), S5[lab]['per']))
P()
w = S5['the watched shape']; o = S5['other 24+']
P('  S5-P4 said the watched shape would move MOST. Per MOVING row: watched %+.1f, other 24+ %+.1f.'
  % (w['per'], o['per']))
P('  S5-P4: %s' % ('RIGHT — it moves most per row'
                   if abs(w['per']) > abs(o['per']) else
                   'WRONG — the other mature rows move more per row'))
P()
P('  THESE ARE POPULATIONS, NOT PLAYERS. No row named in the order gated any number in this file and')
P('  no row\'s value is an acceptance criterion.')

json.dump(dict(S1_P5=dict(n=len(xs), r=r, up=int((ys > 0).sum()), down=int((ys < 0).sum())),
               S5_P4=S5), open(os.path.join(HERE, 'ROWLEVEL_S.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'ROWLEVEL_S_out.txt'), 'w').write('\n'.join(L) + '\n')
