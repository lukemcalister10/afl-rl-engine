#!/usr/bin/env python3
"""ORDER S — THE STANDING TWO-SIDED NO-ARB SUITE, in the owner's standing format.

ORDER K's bb_standing_tablesK.py, carried whole. The ONLY changes are the board list and the labels:
the comparison columns are the landing candidate and ORDER K, and the new column is ORDER P.

  * FIVE ND BANDS + THE CLASSIC THREE (ALL 1-64 / 1-20 / 21-64): year paths yr0..yr7, the yr0->1
    appreciation, the buy-side margin against the 14% carry, and a two-sided verdict per band.
  * EVERY POOL ARM, BOTH WINDOWS (primary 2005-2023, modern 2019-2023): same paths, same verdicts.
  * The vantage-consistency matrix (diagnostic).
  * The ENTRY-YEAR CONTROL against the landing candidate.

Reading rule, in plain words: a group is fairly priced if it appreciates between 0% and +14% over
its first year. Below 0% is a SELL-SIDE RED — you could sell at draft day, buy back a year later and
keep the difference. Above +14% is a BUY-SIDE RED — you could buy at draft day and beat the cost of
carrying him. The margin column is how much room is left before the buy rail.

ND band paths come from the DISCLOSED extended instrument's own JSON (t338_extended_DISCLOSED.py,
committed md5 d59ad550116ebbe3d90ed82becd2c4d5, run whole by bb_noarbK.sh). Pool arms are computed
here with noarb_table_allarm.py's own cohort/value semantics (cohort = year+1 except MSD; pre-window
rows excluded and counted, never zeroed; ended/null = 0 kept in the denominator).
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
N36 = SP + '/os/noarb'
CHARGE = 0.14
BANDS5 = ['picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
CLASSIC = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64']
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]
YEARS = list(range(0, 8))
LABELS = [l for l in ('OKRULED', 'PBUILT', 'QB1', 'QAB1', 'R20A', 'SW47', 'SW47A', 'SC20',
                      'SC20A', 'SM', 'SMA', 'SL56', 'SL10', 'SALL')
          if os.path.exists(N36 + '/table_EXT_%s.json' % l)]
NICE = {'OKRULED': 'ORDER K f3101883 — carries the DEFECTIVE blind eta charge',
        'PBUILT': 'ORDER P 374d4e44 — the pedigree-conditional charge, THE BASE',
        'QB1': 'FIX B1 — the settled repair, THE CONTROL 1b1817f3',
        'QAB1': 'FIX A+B1 — THE CONTROL cbbb94d4',
        'R20A': 'ORDER R p20 CLIP + FIX A + B1 — THE CONTROL 7f88f509',
        'SW47': 'ORDER S S1 recency w=0.47 — PRICED, NOT ADOPTED',
        'SW47A': 'ORDER S S1 recency w=0.47 + FIX A — PRICED, NOT ADOPTED',
        'SC20': "ORDER S S2 the owner's COMPRESSION, p20 anchor — PRICED, NOT ADOPTED",
        'SC20A': 'ORDER S S2 compression p20 + FIX A — PRICED, NOT ADOPTED',
        'SM': 'ORDER S S5 the MATURE premium at 24+ — PRICED, NOT ADOPTED',
        'SMA': 'ORDER S S5 mature premium + FIX A — PRICED, NOT ADOPTED',
        'SL56': 'ORDER S S3 LAMBDA 0.56 — the frontier endpoint. PRICED, NOT ADOPTED',
        'SL10': 'ORDER S S3 LAMBDA 0.10 — the frontier endpoint. PRICED, NOT ADOPTED',
        'SALL': 'ORDER S ALL FOUR + FIX A — the far corner. NOT A RECOMMENDATION.'}

OUT = {'charge': CHARGE, 'labels': LABELS, 'nd': {}, 'arms': {}, 'vantage': {}, 'entry_control': {}}
L = []


def P(s=''):
    print(s); L.append(str(s))


T338 = {lab: json.load(open(N36 + '/table_EXT_%s.json' % lab)) for lab in LABELS}


def verdict(a):
    return 'SELL-RED' if a < 0 else ('BUY-RED' if a > CHARGE else 'ok')


P('=' * 118)
P('ORDER S — STANDING TWO-SIDED NO-ARB SUITE. NOTHING IS ADOPTED.  carry charge = 14%/yr.')
P('   SELL-SIDE RED: yr0->1 appreciation < 0.     BUY-SIDE RED: yr0->1 appreciation > +14%.')
P('=' * 118)
P('\n-- ND BANDS (extended-338 disclosed instrument; years 0..7 as mean-ratio vs the same-set yr0) --')
for lab in LABELS:
    P('\n[%s  %s]' % (lab, NICE[lab]))
    P('  %-16s %6s ' % ('band', 'n') + ' '.join('%7s' % ('yr%d' % n) for n in YEARS) +
      '  %9s %9s %9s' % ('apr0-1', 'buy-mgn', 'verdict'))
    for b in CLASSIC + BANDS5:
        rows = {r['N']: r for r in T338[lab]['groups'][b]['rows']}
        n = rows[0]['n_included']
        path = [rows[k]['ratio_meanN_over_mean0'] if k in rows else None for k in YEARS]
        a01 = rows[1]['mean_yearN'] / rows[1]['mean_year0_same_set'] - 1.0
        mgn = CHARGE - a01
        OUT['nd'].setdefault(lab, {})[b] = dict(n=n, path=path, apprec01=a01, buy_margin=mgn,
                                                verdict=verdict(a01))
        P('  %-16s %6d ' % (b, n) + ' '.join(('%7.3f' % v) if v is not None else '      -' for v in path) +
          '  %+8.2f%% %+8.2f%% %9s' % (100 * a01, 100 * mgn, verdict(a01)))
        if b == 'picks 21-64':
            P('  ' + '-' * 112)

BASE = 'PBUILT'
# BOTH BASELINES ON EVERY ROW. ORDER K is where this mechanism path began and ORDER P is the board
# this order changes one thing inside. Printing only one of them hides half the arc.
for lab in [x for x in LABELS if x != BASE]:
    P('\n-- THE MOVE, BAND BY BAND (%s against BOTH baselines, in points of yr0->1 appreciation) --' % lab)
    P('  %-16s %11s %11s %11s %11s %11s   %s'
      % ('band', 'ORDER K', 'ORDER P', lab, 'vs ORDER P', 'vs ORDER K', 'verdict P -> this'))
    for b in CLASSIC + BANDS5:
        ak = OUT['nd']['OKRULED'][b]['apprec01'] if 'OKRULED' in OUT['nd'] else None
        a0 = OUT['nd'][BASE][b]['apprec01']; a1 = OUT['nd'][lab][b]['apprec01']
        P('  %-16s %s %+10.2f%% %+10.2f%% %+11.2f %s   %s -> %s'
          % (b, ('%+10.2f%%' % (100 * ak)) if ak is not None else '          -',
             100 * a0, 100 * a1, 100 * (a1 - a0),
             ('%+11.2f' % (100 * (a1 - ak))) if ak is not None else '          -',
             OUT['nd'][BASE][b]['verdict'], OUT['nd'][lab][b]['verdict']))

# ---- pool arms -------------------------------------------------------------------------------------
ARM_TYPES = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS']


def arm_paths(matrix_path):
    D = json.load(open(matrix_path))
    R = D['recs']
    WINDOW_END = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

    def cohort(r):
        y = r.get('year')
        return None if y is None else (y if r.get('type') == 'MSD' else y + 1)

    def value_at(r, N):
        if N == 0:
            return float(r['v0']), 'v0'
        Y = cohort(r) + N - 1
        yrs = r.get('yrs') or []; vp = r.get('vpath') or []
        if not yrs: return 0.0, 'ended'
        if Y < yrs[0]: return None, 'pre'
        if Y > yrs[-1]: return 0.0, 'ended'
        i = yrs.index(Y)
        return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')

    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0 and r.get('is_pool')]
    out = {}
    for wname, lo, hi in WINDOWS:
        for arm in ARM_TYPES + ['ALLPOOL']:
            pop = [r for r in elig if lo <= cohort(r) <= hi and (arm == 'ALLPOOL' or r['type'] == arm)]
            if not pop: continue
            path, meta, npre = [], [], []
            for N in YEARS:
                reached = pop if N == 0 else [r for r in pop if cohort(r) + N - 1 <= WINDOW_END]
                vals = []; pre = 0
                for r in reached:
                    v, kind = value_at(r, N)
                    if kind == 'pre':
                        pre += 1; continue
                    vals.append((v, float(r['v0'])))
                if len(vals) < 5:
                    path.append(None); meta.append(len(vals)); npre.append(pre); continue
                mN = sum(v for v, _ in vals) / len(vals)
                m0 = sum(v0 for _, v0 in vals) / len(vals)
                path.append(mN / m0 if m0 > 0 else None); meta.append(len(vals)); npre.append(pre)
            out[(wname, arm)] = dict(n=len(pop), path=path, n_by_year=meta, n_pre=npre)
    return out


ARMP = {lab: arm_paths(SP + '/per_entrant_%s.json' % lab) for lab in LABELS}
P('\n-- POOL ARMS (cohort clock, all-arm instrument semantics; MSD yr1 is the debut-gap exclusion, '
  'printed in words, never a silent blank) --')
for lab in LABELS:
    P('\n[%s  %s]' % (lab, NICE[lab]))
    for wname, _, _ in WINDOWS:
        P('  %s window:' % wname)
        P('    %-8s %5s ' % ('arm', 'n') + ' '.join('%7s' % ('yr%d' % n) for n in YEARS) +
          '  %9s %9s %9s' % ('apr0-1', 'buy-mgn', 'verdict'))
        for arm in ARM_TYPES + ['ALLPOOL']:
            d = ARMP[lab].get((wname, arm))
            if d is None: continue
            a01 = (d['path'][1] / d['path'][0] - 1.0) if (d['path'][0] and d['path'][1] is not None) else None
            verd = ('n/a — MSD debuts in his draft year, so the matrix has no year-1 cell for him; '
                    'those rows are excluded and counted, never scored zero'
                    if (arm == 'MSD' and a01 is None) else
                    ('thin/absent' if a01 is None else verdict(a01)))
            OUT['arms'].setdefault(lab, {})['%s|%s' % (wname, arm)] = dict(
                n=d['n'], path=d['path'], n_pre=d['n_pre'],
                apprec01=a01, buy_margin=(None if a01 is None else CHARGE - a01), verdict=verd)
            P('    %-8s %5d ' % (arm, d['n']) +
              ' '.join(('%7.3f' % v) if v is not None else '      -' for v in d['path']) +
              ('  %+8.2f%% %+8.2f%% %9s' % (100 * a01, 100 * (CHARGE - a01), verd)
               if a01 is not None else '         —         —  %s' % verd))

for lab in [x for x in LABELS if x != BASE]:
    P('\n-- THE MOVE, ARM BY ARM (primary window; %s minus ORDER P) --' % lab)
    P('  %-10s %12s %12s %12s   %s' % ('arm', 'ORDER P', lab, 'move', 'verdict move'))
    for arm in ARM_TYPES + ['ALLPOOL']:
        a = OUT['arms'][BASE].get('PRIMARY|%s' % arm)
        b = OUT['arms'][lab].get('PRIMARY|%s' % arm)
        if not a or not b or a['apprec01'] is None or b['apprec01'] is None: continue
        P('  %-10s %+11.2f%% %+11.2f%% %+11.2f   %s -> %s'
          % (arm, 100 * a['apprec01'], 100 * b['apprec01'], 100 * (b['apprec01'] - a['apprec01']),
             a['verdict'], b['verdict']))

# ---- vantage matrix (diagnostic) --------------------------------------------------------------------
P('\n-- VANTAGE-CONSISTENCY MATRIX (implied growth yrV -> yrV+k vs the 14% carry; DIAGNOSTIC ONLY) --')
for lab in LABELS:
    P('\n[%s]' % lab)
    P('  %-16s %3s ' % ('band', 'V') + ' '.join('%8s' % ('k=%d' % k) for k in (1, 2, 3, 4)) + '    carry: ' +
      ' '.join('%8s' % ('%.1f%%' % (100 * (1.14 ** k - 1))) for k in (1, 2, 3, 4)))
    for b in BANDS5:
        rows = {r['N']: r['ratio_meanN_over_mean0'] for r in T338[lab]['groups'][b]['rows']}
        for V in (0, 1, 2):
            gr = [(rows[V + k] / rows[V] - 1.0) if (V in rows and (V + k) in rows and rows[V] > 0) else None
                  for k in (1, 2, 3, 4)]
            OUT['vantage'].setdefault(lab, {})['%s|V%d' % (b, V)] = gr
            P('  %-16s %3d ' % (b if V == 0 else '', V) +
              ' '.join(('%+7.1f%%' % (100 * g)) if g is not None else '       -' for g in gr))

# ---- entry-year control -----------------------------------------------------------------------------
P('\n-- ENTRY-YEAR CONTROL (the entry year must not move: the levers are production/fade corrections and a day-0 row has no production: it is a production correction and a '
  'day-0 row has no production) --')
P('   bound: every ND-band yr0 MEAN within +-0.1% of the ORDER P cell (yr1 is EXPECTED to move)')
br = []
for lab in [x for x in LABELS if x != 'O35FINAL']:
    P('   [%s]' % lab)
    for b in CLASSIC + BANDS5:
        rc = {r['N']: r for r in T338[BASE]['groups'][b]['rows']}
        rn = {r['N']: r for r in T338[lab]['groups'][b]['rows']}
        for N in (0, 1):
            c = rc[N]['mean_yearN']; n_ = rn[N]['mean_yearN']
            rel = n_ / c - 1.0
            ok = (abs(rel) <= 0.001) if N == 0 else True
            OUT['entry_control']['%s|%s|yr%d' % (lab, b, N)] = dict(control=c, other=n_, rel=rel, ok=bool(ok))
            if N == 0 and not ok: br.append((lab, b, rel))
            P('   %-16s yr%d: candidate %9.1f  %-8s %9.1f  %+7.3f%%  %s'
              % (b, N, c, lab, n_, 100 * rel, ('ok' if ok else 'BREACH') if N == 0 else '(yr1 moves by design)'))
P('\nENTRY-YEAR CONTROL: %s' % ('PASS — every yr0 cell inside +-0.1%' if not br else 'BREACHES: %s' % br))
OUT['entry_control']['pass'] = not br

json.dump(OUT, open(os.path.join(HERE, 'STANDING_TABLES_S.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'STANDING_TABLES_S_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote STANDING_TABLES_S.json / STANDING_TABLES_S_out.txt')
