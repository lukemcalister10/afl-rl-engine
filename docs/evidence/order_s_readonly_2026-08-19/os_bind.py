#!/usr/bin/env python3
"""ORDER S READ-ONLY — T1, the SIZE of the level offset on the ACTUAL BOARD.

T1 measured the offsets in points a game. This file asks what they are worth in board points, and
on how many rows, so the answer is in the owner's units rather than the estimator's.

THIS IS NOT A PROPOSAL AND NOTHING IS ADOPTED. It is a counterfactual READ: hold everything else
fixed and move each row's s_P by his POSITION's own measured offset, which is exactly what the bar
would have done if it carried that position's level instead of the pooled one. NO ENGINE FILE IS
EDITED, NO DIAL IS ADDED, NO BOARD IS BUILT. The wrapper lives in the loaded namespace only and is
proved inert at offset zero.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_bind.py
"""
import os, sys, io, json, math, contextlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as SL                                                          # noqa: E402
import numpy as np                                                           # noqa: E402

Y = 2026
L = []


def P(s=''):
    print(s); L.append(str(s))


LEV = json.load(open(os.path.join(HERE, 'LEVEL_SRO.json')))
OFF = {g: LEV['point']['%s|ALL' % g] for g in ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF')}
CUT = LEV['cuts']

NS = SL.load(RL_O37='1')
NS['_REC'] = SL.install_recorder(NS)
MA = NS['_MA']
FNUM = json.load(open(SL.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
EV = NS['ev']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        EV(p, Y)
ROWS = {p['key']: SL.assemble(NS, p, Y) for p in MA.players}
RAW = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        RAW[p['key']] = EV(p, Y)
BOARD = {k: int(round(RAW[k] / FNUM)) for k in RAW}

P('=' * 118)
P('ORDER S READ-ONLY — T1b. WHAT THE POSITION LEVEL OFFSET IS WORTH ON THE ACTUAL BOARD.')
P('=' * 118)
P('NOTHING IS ADOPTED. NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. This is a')
P('counterfactual READ, in the engine\'s own currency, so the T1 offsets can be quoted in board points.')
P('board total (numeraire): %d' % sum(BOARD.values()))
P()
P('   the offsets carried in from LEVEL_SRO.json, pooled over price, in points a game:')
for g in ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF'):
    lo, hi, _ = LEV['ci']['%s|ALL' % g]
    P('     %-6s %+8.3f   90%% CI [%+7.3f, %+7.3f]%s'
      % (g, OFF[g], lo, hi, '   CI EXCLUDES ZERO' if (lo > 0 or hi < 0) else ''))
P()

# the young charged population: the only rows the ORDER P charge can reach
POP = [p for p in MA.players
       if ROWS[p['key']] is not None and ROWS[p['key']].get('price') is not None
       and p.get('_by') and (Y - int(p['_by'])) < NS['O37_AGE_GATE']
       and NS['pv_games'](p, Y) > 0 and ROWS[p['key']]['s_P'] is not None]
P('   the population the charge can reach: age under %d, career games > 0, an s_P the bar can read.'
  % NS['O37_AGE_GATE'])
P('   %d rows of %d on the board.' % (len(POP), len(BOARD)))
P()


def band_of(p):
    r = ROWS[p['key']]
    v0 = NS['day0_v0'](p)
    c = 'TALL' if r['tall'] else 'SMALL'
    med, p90 = CUT[c]
    if v0 is None:
        return 'no v0'
    return 'TAIL' if v0 > p90 else ('ABOVE' if v0 > med else 'BELOW')


# the counterfactual: s_P moves by the position's own offset. NOTHING ELSE MOVES.
RES = []
for p in POP:
    r = ROWS[p['key']]
    pos = MA.gfut(p)
    if pos not in OFF:
        continue
    g = NS['pv_games'](p, Y)
    A = 1.0 - math.exp(-g / NS['O37_G0'])
    s = r['s_P']
    f0 = math.exp(-NS['O37_LAMBDA'] * A * min(max(1.0 - NS['O37_THETA_R'] * (s - NS['O37_S0']), 0.0), NS['O37_TMAX']))
    s1 = s - OFF[pos]        # the bar drops by the offset => the surplus RISES by it when OFF < 0
    f1 = math.exp(-NS['O37_LAMBDA'] * A * min(max(1.0 - NS['O37_THETA_R'] * (s1 - NS['O37_S0']), 0.0), NS['O37_TMAX']))
    d = (f1 - f0) * r['pi_base_eff'] * r['ped'] / FNUM
    RES.append(dict(key=p['key'], name=p.get('player'), pos=pos, band=band_of(p), g=g, A=A,
                    s_P=s, f=f0, f_cf=f1, d=d, board=BOARD[p['key']],
                    v0=NS['day0_v0'](p), age=Y - int(p['_by'])))
# the identity check: a zero offset must move nothing at all
for p in POP[:50]:
    r = ROWS[p['key']]
    g = NS['pv_games'](p, Y)
    A = 1.0 - math.exp(-g / NS['O37_G0'])
    s = r['s_P']
    f0 = math.exp(-NS['O37_LAMBDA'] * A * min(max(1.0 - NS['O37_THETA_R'] * (s - NS['O37_S0']), 0.0), NS['O37_TMAX']))
    assert abs(f0 - r['f_eff']) < 1e-9, 'SRO-B1 FIRED: the recomputed factor is not the engine\'s (%s)' % p['key']
P('   FALSIFIER SRO-B1 did not fire: the charge factor recomputed here reproduces the engine\'s own')
P('   f on every row checked, to under 1e-9. At offset zero the counterfactual moves nothing.')
P()
P('-' * 118)
P('WHAT THE OFFSET IS WORTH, PER POSITION AND PER PRICE BAND — BOARD POINTS')
P('-' * 118)
P('   POSITIVE = the row is currently charged TOO MUCH and would gain that many points if the bar')
P('   carried his own position\'s level. NEGATIVE = he is currently charged too little.')
P()
P('   %-6s %6s %10s %10s %10s | %-34s' % ('pos', 'rows', 'total', 'median', 'worst row', 'by price band (rows / points)'))
OUT = {}
for g in ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF'):
    s = [r for r in RES if r['pos'] == g]
    if not s:
        continue
    bands = []
    for b in ('BELOW', 'ABOVE', 'TAIL'):
        sb = [r for r in s if r['band'] == b]
        bands.append('%s %d/%+.0f' % (b[0], len(sb), sum(r['d'] for r in sb)))
    OUT[g] = dict(n=len(s), total=sum(r['d'] for r in s),
                  med=float(np.median([r['d'] for r in s])),
                  worst=max(s, key=lambda r: abs(r['d']))['d'],
                  bands={b: dict(n=len([r for r in s if r['band'] == b]),
                                 pts=sum(r['d'] for r in s if r['band'] == b))
                         for b in ('BELOW', 'ABOVE', 'TAIL')})
    P('   %-6s %6d %10.0f %10.1f %10.0f | %-34s'
      % (g, len(s), OUT[g]['total'], OUT[g]['med'], OUT[g]['worst'], '  '.join(bands)))
P('   %-6s %6d %10.0f' % ('ALL', len(RES), sum(r['d'] for r in RES)))
P()
P('   NOTE, and it matters: the six numbers do NOT net to zero on the board even though the')
P('   position offsets net to zero within each class on the FITTED population. The board is a')
P('   different population — one as-of year, one age window, one set of prices — and a row only')
P('   moves in proportion to his own pedigree leg and his own A(g).')
P()
P('-' * 118)
P('THE TEN ROWS THE OFFSET MOVES MOST, either way. CONSEQUENCES, NEVER TARGETS.')
P('-' * 118)
P('   %-24s %5s %4s %5s %7s %8s %8s %9s %8s'
  % ('row', 'pos', 'age', 'g', 'v0', 'f now', 'f cf', 'board', 'move'))
for r in sorted(RES, key=lambda z: -abs(z['d']))[:10]:
    P('   %-24s %5s %4d %5.0f %7.0f %8.3f %8.3f %9d %+8.0f'
      % (r['name'][:24], r['pos'], r['age'], r['g'], (r['v0'] or 0), r['f'], r['f_cf'], r['board'], r['d']))
P()
P('   THE SHARE OF THE YOUNG CHARGED BOARD EACH POSITION CARRIES, because a large offset on a small')
P('   population is a small problem and the packet should not pretend otherwise:')
P()
P('   %-6s %8s %12s %14s %12s' % ('pos', 'rows', 'share of rows', 'board points', 'share of pts'))
tb = sum(r['board'] for r in RES)
for g in ('KPD', 'KPF', 'RUCK', 'MID', 'SD', 'SF'):
    s = [r for r in RES if r['pos'] == g]
    if not s:
        continue
    OUT[g]['share_rows'] = len(s) / len(RES)
    OUT[g]['board'] = sum(r['board'] for r in s)
    P('   %-6s %8d %11.1f%% %14d %11.1f%%'
      % (g, len(s), 100 * len(s) / len(RES), sum(r['board'] for r in s),
         100 * sum(r['board'] for r in s) / max(1, tb)))
P()

json.dump(dict(offsets=OFF, per_pos=OUT, n=len(RES), total=sum(r['d'] for r in RES),
               rows=[{k: v for k, v in r.items()} for r in sorted(RES, key=lambda z: -abs(z['d']))[:60]]),
          open(os.path.join(HERE, 'BIND_SRO.json'), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'BIND_SRO_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote BIND_SRO.json and BIND_SRO_out.txt')
