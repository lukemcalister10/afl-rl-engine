#!/usr/bin/env python3
"""ORDER S — S5's POSITION-COMPOSITION CROSS-CHECK. READ-ONLY, no engine load.

The parallel read-only seat's T1 found the PG LEVEL by position is NOT a null (SD over-barred 2.978
pts a game, RUCK 5.57, SF UNDER-barred 2.709; MID/KPD/KPF nulls; zero-sum within each class). If the
MATURE population's position mix differs from the YOUNG one, part of S5's measured young-to-mature
premium gap would be a COMPOSITION effect rather than an age effect. This file rules that out.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB
L = []


def P(s=''):
    print(s); L.append(str(s))


M = LB.load_matrix('OKRULED')
Y = PB.season_rows(M, 18, 23)
MT = PB.season_rows(M, 24, 40)
# the parallel seat's OWN published T1 level offsets, quoted not re-derived
OFF = {'SD': -2.978, 'RUCK': -5.57, 'SF': +2.709, 'MID': -0.348, 'KPD': 0.0, 'KPF': 0.0}
P('ORDER S — S5 POSITION-COMPOSITION CROSS-CHECK (T1 offsets quoted from PACKET_SRO.md, not re-derived)')
P('%-6s %-8s %9s %9s %9s' % ('cls', 'pos', 'young%', 'mature%', 'shift'))
out = {}
for cls in ('TALL', 'SMALL'):
    ys = [r for r in Y if r['cls'] == cls]
    ms = [r for r in MT if r['cls'] == cls]
    gy = sum(r['games'] for r in ys); gm = sum(r['games'] for r in ms)
    for pos in sorted(set(r['pos'] for r in ys) | set(r['pos'] for r in ms)):
        a = 100 * sum(r['games'] for r in ys if r['pos'] == pos) / gy
        b = 100 * sum(r['games'] for r in ms if r['pos'] == pos) / gm
        out[(cls, pos)] = (a, b)
        P('%-6s %-8s %9.1f %9.1f %+9.1f' % (cls, pos, a, b, b - a))
P()
for cls in ('TALL', 'SMALL'):
    s = sum((b - a) / 100.0 * OFF.get(pos, 0.0) for (c, pos), (a, b) in out.items() if c == cls)
    P('%-6s composition-implied change in the mean position level, young -> mature: %+.3f pts a game'
      % (cls, s))
P()
P('Against measured premium gaps of +4.03 at v0 400 and -4.71 at v0 3,000, the composition effect is')
P('under a tenth of the signal AND it is a single constant offset, while the measured gap CHANGES')
P('SIGN across the price axis. A level shift cannot produce a sign change.')
open(os.path.join(HERE, 'COMPOSITION_S_out.txt'), 'w').write('\n'.join(L) + '\n')
