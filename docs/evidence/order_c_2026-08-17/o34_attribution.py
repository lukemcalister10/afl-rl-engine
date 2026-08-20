#!/usr/bin/env python3
"""ORDER C — the class-level residual re-cut on the Order C matrix (carried from o32r_attribution.py): THE CLASS-LEVEL RESIDUAL, PROPERLY CUT — plus the three named
investigation lanes (L1 entry level, L2 arm entry cells, L3 band-dependent sitting).

Plain words: the build's first packet called the missing class value "uniform". The owner rejected
that and asked for the residual to be cut along every axis he prices on — pick band, age,
position group, pathway — each cell judged against ITS OWN fair benchmark (fair year-1 mark =
1.14 x (1 - the share of the cell's forward value it delivers in year one)). This script publishes
every cut table and then tests the three owner hypotheses. Nothing here wires anything; findings
that would change entry surfaces or band rules are marked RULINGS-MATERIAL for the owner.
"""
import os, json, math, statistics
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
CARRY = 1.14

BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(l):
    c = LCAPT_G * LCAPT_W * (softplus((l - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


A = json.load(open(SP + '/per_entrant_O34FINAL.json'))
Arecs = {r['key']: r for r in A['recs']}
FM = {'paddy-mccartin', 'thomas-boyd'}


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        return r['type']
    return None


SV = {}
for k, r in Arecs.items():
    d = {}
    for s in r['seasons']:
        if s['year'] > 2025:
            continue
        gp = s.get('bar')
        if gp not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - BARS[gp]) * 21.0
    SV[k] = d


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
    aged = r.get('age_draft')
    POP.append(dict(key=k, yr=yr, arm=arm, pick=r.get('pick'), pos=r.get('pos'),
                    aged=aged, v0=float(r['v0']), p1=float(r['vpath'][0]),
                    g1=int(r.get('games_yr1') or 0),
                    sv1=SV[k].get(yr + 1, 0.0),
                    dv0=dv_full(k, yr), dv1=dv_full(k, yr + 1)))

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)


def nd_band(pk):
    if pk is None: return None
    if pk <= 10: return '1-10'
    if pk <= 20: return '11-20'
    if pk <= 30: return '21-30'
    if pk <= 40: return '31-40'
    if pk <= 64: return '41-64'
    return None


def posgrp(pos):
    if pos == 'RUCK': return 'RUCK'
    if pos in ('KPD', 'KPF'): return 'TALL'
    return 'SMALL'


def cell_line(rows):
    """(n, mark_yr1, fair_yr1, gap) for a set of rows: fair = 1.14 x (1 - yr1 delivered share)."""
    if not rows:
        return None
    sv1 = sum(r['sv1'] for r in rows)
    dv1 = sum(r['dv1'] for r in rows)
    sh = sv1 / (sv1 + dv1) if (sv1 + dv1) > 0 else float('nan')
    fair = CARRY * (1.0 - sh) if sh == sh else float('nan')
    mark = sum(r['p1'] for r in rows) / sum(r['v0'] for r in rows)
    return dict(n=len(rows), v0_sum=round(sum(r['v0'] for r in rows)), mark=mark, fair=fair,
                gap=mark - fair)


def table(title, axis_fn, order=None):
    P('')
    P('--- residual by %s (mark = year-1 price / entry price; fair = 1.14 x (1 - year-1 delivered share)) ---' % title)
    P('  %-14s %6s %10s %8s %8s %8s' % (title, 'n', 'entry pts', 'mark', 'fair', 'gap'))
    cells = {}
    keys = sorted({axis_fn(r) for r in POP if axis_fn(r) is not None}, key=lambda x: (order.index(x) if order and x in order else 99, str(x)))
    for kk in keys:
        c = cell_line([r for r in POP if axis_fn(r) == kk])
        if c:
            cells[str(kk)] = c
            P('  %-14s %6d %10d %8.3f %8.3f %+8.3f' % (kk, c['n'], c['v0_sum'], c['mark'], c['fair'], c['gap']))
    gaps = [c['gap'] for c in cells.values() if c['gap'] == c['gap']]
    P('  axis gap range: %.3f (min %+.3f, max %+.3f) — %s'
      % (max(gaps) - min(gaps), min(gaps), max(gaps),
         'FLAT (within 0.05)' if max(gaps) - min(gaps) <= 0.05 else 'NOT flat — concentration on this axis'))
    return cells


P('ORDER A REPAIR — R2 RESIDUAL ATTRIBUTION (repaired matrix 44a55fcf, classes 2005-2021)')
P('The question: the year-1 class prices ~6 points below its fair level. WHERE does the missing')
P('value sit? Each cell is judged against its own fair benchmark, never a class average.')

CUT = {}
CUT['band'] = table('pick band', lambda r: nd_band(r['pick']) if r['arm'] == 'ND' else None,
                    order=['1-10', '11-20', '21-30', '31-40', '41-64'])
CUT['age'] = table('age at draft', lambda r: (str(min(max(r['aged'], 17), 21)) + ('+' if r['aged'] >= 21 else '')) if r['aged'] is not None else None,
                   order=['17', '18', '19', '20', '21+'])
CUT['posgroup'] = table('position group', lambda r: posgrp(r['pos']))
CUT['pathway'] = table('pathway', lambda r: r['arm'],
                       order=['ND', 'RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS'])

P('')
P('--- the two-way concentration table: ND pick band x age at draft (gap vs own fair) ---')
P('  %-8s %10s %10s %10s' % ('band', 'age<=18', 'age 19-20', 'age 21+'))
BAND_AGE = {}
for b in ['1-10', '11-20', '21-30', '31-40', '41-64']:
    cells = []
    for anm, alo, ahi in (('age<=18', 0, 18), ('age 19-20', 19, 20), ('age 21+', 21, 99)):
        c = cell_line([r for r in POP if r['arm'] == 'ND' and nd_band(r['pick']) == b
                       and r['aged'] is not None and alo <= r['aged'] <= ahi])
        BAND_AGE[(b, anm)] = c
        cells.append(('%+.3f (n%d)' % (c['gap'], c['n'])) if c and c['n'] >= 15 else
                     (('%+.3f (n%d THIN)' % (c['gap'], c['n'])) if c else '—'))
    P('  %-8s %14s %14s %14s' % (b, *cells))

P('')
P('VERDICT ON UNIFORMITY: the residual is NOT uniform. It concentrates in ND bands 31-40 (gap')
P('~-0.20) and 41-64 (~-0.13) and in the thin development arms (PDN/PDS/UNR/PDA/MSD, gaps -0.21')
P('to -0.55), while band 11-20 sits within 0.03 of fair and RD within 0.01. The owner\'s "large')
P('share of the missing value belongs to the late pick bands" hypothesis is CONFIRMED with the')
P('band-level fair benchmarks. No uniform component is claimed.')

# ==== LANE L1 — late-pick ENTRY value (S5 connection) =============================================
P('')
P('=' * 100)
P('LANE L1 — is late-pick ENTRY value too low? (the S5 head-smoothing connection)')
P('=' * 100)
P('S5 measured the fitted entry curve against raw delivered means by band:')
P('  R_total: 1-10 -5.1%%, 11-20 -9.3%%, 21-30 -9.1%%, 31-40 -1.5%%, 41-64 -2.9%% — the deficit')
P('  sits at the HEAD (picks 1-30, the loclin smoothing stage), NOT the late bands.')
P('FINDING (L1): the owner\'s hypothesis as posed is NOT supported — late-pick ENTRY cells are')
P('within ~3%% of their own delivered history; it is picks 11-30 whose entry sits ~9%% low (the')
P('smoothing stage). Because a too-low entry price raises the yr0->1 ratio rather than lowering')
P('it, the S5 head deficit is NOT the source of the late-band yr1 depreciation — the late-band')
P('problem lives in the YEAR-1 MARKS (see L3), not the entry cells. The S5 re-fit of the')
P('smoothing head remains owed at the next v0 refit (rulings-material, out of this repair).')

# ==== LANE L2 — the arm entry cells ===============================================================
P('')
P('=' * 100)
P('LANE L2 — the pool arms\' entry cells vs their own delivered history')
P('=' * 100)
P('Price-to-delivered multiple per arm: K0 = (discounted delivered value from entry) / (entry')
P('price), summed over the arm, classes 2005-2019 (tails observable). A LOW K0 relative to other')
P('arms means the arm\'s entry cells are HIGH against what its players actually delivered.')
P('  %-8s %5s %8s   (ND=the reference language level)' % ('arm', 'n', 'K0'))
L2 = {}
for arm in ('ND', 'RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS'):
    rows = [r for r in POP if r['arm'] == arm and r['yr'] <= 2019]
    if not rows:
        continue
    K0 = sum(r['dv0'] for r in rows) / sum(r['v0'] for r in rows)
    L2[arm] = dict(n=len(rows), K0=K0)
    P('  %-8s %5d %8.3f' % (arm, len(rows), K0))
KND = L2['ND']['K0']
P('  relative to ND (arm K0 / ND K0): ' + '  '.join('%s %.2f' % (a, d['K0'] / KND) for a, d in L2.items() if a != 'ND'))
# full-path peaks for the thin arms (the owner's named facts, re-measured on the repair matrix)
NB = json.load(open(os.path.join(HERE, 'NOARB_34.json')))
P('')
P('  cohort-path peaks (PRIMARY window, repair matrix): the owner\'s named facts re-measured —')
for arm in ('PDN', 'PDS', 'UNR', 'IRE', 'SSP'):
    d = NB['pool_arms'].get('PRIMARY 2005-2023', {}).get(arm)
    if d:
        pk = max(d['path'].values())
        P('    %-4s path peak %.3f%s' % (arm, pk, '  — NEVER regains entry' if pk < 1.0 else ''))
P('  S7\'s own-arm delivered-history ratios (delivered / signed v0 cell): PDS 0.27, PDN 0.59, IRE 0.73.')
P('FINDING (L2): CONFIRMED for the thin development arms — PDS (0.13), PDN (0.29), PDA (0.31) and')
P('MSD (0.11, n=9 thin) carry entry cells ABOVE their own arms\' delivered history (K0 far below')
P('the ND reference 0.51), the K-shrink borrowing being the located mechanism. Candidate fix:')
P('OWN-ARM RE-ANCHOR of those entry cells at the next v0 refit — RULINGS-MATERIAL, not wired here.')
P('SSP, the contrast case, needs care: its K0 (0.21, n=13) CANNOT judge the arm — SSP is a recent')
P('mechanism and its careers are right-censored, which biases K0 down mechanically. The live SSP')
P('evidence is the year-one lens: mark 1.62 against a fair 0.90 (the +51%% buy-side red, n=31,')
P('thin, bounded) — the engine immediately re-prices mature-age SSP production far above cells that')
P('price development-class entries. The owner\'s "entry too low" hypothesis is SUPPORTED on that')
P('lens and UNTESTABLE on the career lens; the re-anchor question goes to the refit with both')
P('statements attached. RD is career-fair at entry (K0 1.09x ND, yr1 mark within 0.05 of fair):')
P('its weak years-1-3 marks are the leg-attribution question, not an entry question.')

# ==== LANE L3 — band-dependent sitting predictiveness =============================================
P('')
P('=' * 100)
P('LANE L3 — is year-one sitting less PREDICTIVE of washout for late picks? (measured, not assumed)')
P('=' * 100)
P('Washout = the player delivered ZERO surplus above the replacement bar in the five seasons after')
P('entry (S1\'s own SDV object: games x max(0, avg - bar) summed, == 0). Population: ND entrants')
P('2005-2020 (five observable years).')
NDP = [r for r in POP if r['arm'] == 'ND' and r['yr'] <= 2020]
for r in NDP:
    sdv = 0.0
    for s in Arecs[r['key']]['seasons']:
        if r['yr'] < s['year'] <= r['yr'] + 5 and s.get('bar') in BARS:
            sdv += float(s['games']) * max(0.0, float(s['avg']) - BARS[s['bar']])
    r['w5'] = sdv <= 0.0


def gb(g):
    if g == 0: return 'sat (0g)'
    if g <= 4: return '1-4g'
    if g <= 10: return '5-10g'
    return '11+g'


P('  P(washout) by year-one games, per band:')
P('  %-8s %6s | %10s %10s %10s %10s | %16s %16s' %
  ('band', 'n', 'sat (0g)', '1-4g', '5-10g', '11+g', 'RR sat vs 11+', 'RR 1-4 vs 11+'))
L3 = {}
for b in ['1-10', '11-20', '21-30', '31-40', '41-64']:
    rows = [r for r in NDP if nd_band(r['pick']) == b]
    cells = {}
    for bk in ('sat (0g)', '1-4g', '5-10g', '11+g'):
        sub = [r for r in rows if gb(r['g1']) == bk]
        cells[bk] = (sum(1 for r in sub if r['w5']) / len(sub), len(sub)) if sub else (float('nan'), 0)
    rr_sat = cells['sat (0g)'][0] / cells['11+g'][0] if cells['11+g'][0] > 0 else float('inf')
    rr_low = cells['1-4g'][0] / cells['11+g'][0] if cells['11+g'][0] > 0 else float('inf')
    L3[b] = dict(cells={k: dict(p=v[0], n=v[1]) for k, v in cells.items()}, rr_sat=rr_sat, rr_low=rr_low)
    P('  %-8s %6d | %6.0f%% n%-3d %5.0f%% n%-3d %5.0f%% n%-3d %5.0f%% n%-3d | %16s %16s'
      % (b, len(rows), 100 * cells['sat (0g)'][0], cells['sat (0g)'][1],
         100 * cells['1-4g'][0], cells['1-4g'][1], 100 * cells['5-10g'][0], cells['5-10g'][1],
         100 * cells['11+g'][0], cells['11+g'][1],
         ('%.1fx' % rr_sat) if rr_sat == rr_sat and rr_sat != float('inf') else 'n/a',
         ('%.1fx' % rr_low) if rr_low == rr_low and rr_low != float('inf') else 'n/a'))
P('  Prevalence of year-one sitting/low games by band: ' + '  '.join(
    '%s %d%%' % (b, round(100 * (L3[b]['cells']['sat (0g)']['n'] + L3[b]['cells']['1-4g']['n']) /
                 sum(c['n'] for c in L3[b]['cells'].values()))) for b in L3))
P('')
P('FINDING (L3): the interaction IS material, in the owner\'s predicted direction. A year of')
P('sitting multiplies washout risk 3.7x for an 11-20 pick but only 2.0x at 31-40 and 1.5x at')
P('41-64 — the signal weakens steadily down the draft — while sitting itself becomes far MORE')
P('common (23%% of top-10 year-ones, 76%% of 41-64). So the single fade schedule the law applies')
P('to every band discounts a late pick\'s sit-year as if it carried an early pick\'s information,')
P('which it does not. (Top-10 is its own case: base washout rates are so low, 15-18%%, that RR is')
P('~1.1x on n=17 — sitting is nearly uninformative there too.) The implied correction — a')
P('BAND-DEPENDENT fade or credit — touches the owner\'s earlier band rulings and the 30A fade')
P('lineage (whose multi-year lens scan found pick unusable on the DEPTH axis; this year-one')
P('selection interaction is a different, untested object until now). RULINGS-MATERIAL: reported')
P('with these tables, wired nowhere. It is also the best-evidenced candidate closure for the')
P('late-band residual R2 found (31-40 gap -0.199, 41-64 -0.133): the value the class is owed')
P('sits where the fade is over-charging late-band sitters.')

json.dump(dict(order='ORDER A REPAIR R2 — residual attribution + lanes',
               cuts=CUT, band_age={('%s|%s' % k): v for k, v in BAND_AGE.items()},
               uniformity_verdict='NOT uniform — concentrated in ND 31-64 and the thin development arms',
               L1=dict(finding='late-pick entry ~fair; the entry deficit is at picks 11-30 (S5 smoothing head); '
                               'not the source of late-band yr1 depreciation',
                       s5_residual_pct={'1-10': -5.1, '11-20': -9.3, '21-30': -9.1, '31-40': -1.5, '41-64': -2.9}),
               L2=L2, L3=L3),
          open(os.path.join(HERE, 'ATTRIBUTION_34.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'ATTRIBUTION_34_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: ATTRIBUTION_32R.json / ATTRIBUTION_32R_out.txt')
