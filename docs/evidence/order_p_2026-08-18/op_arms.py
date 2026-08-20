#!/usr/bin/env python3
"""ORDER P — THE POOL-ARM TABLES (ORDER L/M file, only the board list changed), BOTH WINDOWS, WITH AND WITHOUT THE 2005/06 COHORTS.

Order K already emitted these in both windows. Order L adds the exclusion variant and nothing else.
The cohort key and the value semantics are lifted VERBATIM from noarb_table_allarm.py by way of
Order K's own bb_standing_tablesK.py arm_paths(): cohort = draft year + 1 except MSD, where cohort =
draft year; pre-window rows are EXCLUDED from that year and counted, never scored zero; ended and
null are 0 and stay in the denominator; a cell with fewer than 5 scorable rows is not printed.

SELF-CHECK L-SC5: the ALLCOH tables must reproduce Order K's STANDING_TABLES_K.json arm cells
exactly, since nothing but a population filter has been added.
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
CHARGE = 0.14
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]
EXCLUDED_COHORTS = (2005, 2006)
VARIANTS = [('ALLCOH', 'every cohort in the window (the standing basis)'),
            ('EX0506', 'the 2005 and 2006 cohorts removed entirely — SENSITIVITY, not a correction')]
YEARS = list(range(0, 8))
ARM_TYPES = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS']
LABELS = [('PDERIV', 'ORDER P — the pedigree-conditional charge (ESTIMATE, NOT A BUILD)'),
          ('NVARB', 'ORDER N — the age-only-bar charge, frontier point (ESTIMATE, NOT A BUILD)'),
          ('OKRULED', 'ORDER K f3101883 — the current candidate, eta 0.50'),
          ('M0ETA0', "ORDER M0 73bf9617 — ORDER K's knobs with ETA SET TO ZERO")]
L = []


def P(s=''):
    print(s); L.append(str(s))


ALLARM = os.path.join(REPO, 'docs/evidence/landing_29_2026-08-13/noarb/noarb_table_allarm.py')
P('=' * 118)
P('ORDER P — POOL-ARM TABLES, BOTH WINDOWS, WITH AND WITHOUT THE 2005/06 COHORTS')
P('=' * 118)
P('  semantics source : noarb_table_allarm.py  md5 %s (read, not modified)'
  % hashlib.md5(open(ALLARM, 'rb').read()).hexdigest())
P('  carry charge     : %.0f%%/yr.  SELL-RED below 0.  BUY-RED above the rail.' % (100 * CHARGE))


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def value_at(r, N, wend):
    if N == 0:
        return float(r['v0']), 'v0'
    Y = cohort(r) + N - 1
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs:
        return 0.0, 'ended'
    if Y < yrs[0]:
        return None, 'pre'
    if Y > yrs[-1]:
        return 0.0, 'ended'
    i = yrs.index(Y)
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


def verdict(a):
    return 'SELL-RED' if a < 0 else ('BUY-RED' if a > CHARGE else 'ok')


OUT = {'charge': CHARGE, 'excluded_cohorts': list(EXCLUDED_COHORTS), 'arms': {}}
for lab, nice in LABELS:
    MX = os.path.join(SP, 'per_entrant_%s.json' % lab)
    R = json.load(open(MX))['recs']
    WEND = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0 and r.get('is_pool')]
    P()
    P('#' * 118)
    P('# %s   [%s]   pool rows %d   window end %d' % (nice, lab, len(elig), WEND))
    P('#' * 118)
    for wname, lo, hi in WINDOWS:
        for vkey, vdesc in VARIANTS:
            P()
            P('  %s window (cohorts %d-%d)  ·  %s' % (wname, lo, hi, vdesc))
            P('    %-8s %5s ' % ('arm', 'n') + ' '.join('%8s' % ('yr%d' % n) for n in YEARS) +
              '  %9s %9s   %s' % ('apr0-1', 'buy-mgn', 'verdict'))
            for arm in ARM_TYPES + ['ALLPOOL']:
                pop = [r for r in elig if lo <= cohort(r) <= hi
                       and (arm == 'ALLPOOL' or r['type'] == arm)]
                if vkey == 'EX0506':
                    pop = [r for r in pop if cohort(r) not in EXCLUDED_COHORTS]
                if not pop:
                    continue
                path, nby, npre = [], [], []
                for N in YEARS:
                    reached = pop if N == 0 else [r for r in pop if cohort(r) + N - 1 <= WEND]
                    vals = []; pre = 0
                    for r in reached:
                        v, kind = value_at(r, N, WEND)
                        if kind == 'pre':
                            pre += 1; continue
                        vals.append((v, float(r['v0'])))
                    if len(vals) < 5:
                        path.append(None); nby.append(len(vals)); npre.append(pre); continue
                    mN = sum(v for v, _ in vals) / len(vals)
                    m0 = sum(v0 for _, v0 in vals) / len(vals)
                    path.append(mN / m0 if m0 > 0 else None); nby.append(len(vals)); npre.append(pre)
                a01 = (path[1] / path[0] - 1.0) if (path[0] and path[1] is not None) else None
                verd = ('n/a — MSD debuts in his draft year, so the matrix has no year-1 cell for him; '
                        'those rows are excluded and counted, never scored zero'
                        if (arm == 'MSD' and a01 is None) else
                        ('thin/absent' if a01 is None else verdict(a01)))
                OUT['arms'].setdefault(lab, {})['%s|%s|%s' % (wname, vkey, arm)] = dict(
                    n=len(pop), path=path, n_by_year=nby, n_pre=npre, apprec01=a01,
                    buy_margin=(None if a01 is None else CHARGE - a01), verdict=verd)
                P('    %-8s %5d ' % (arm, len(pop)) +
                  ' '.join(('%8.3f' % v) if v is not None else '%8s' % '-' for v in path) +
                  ('  %+8.2f%% %+8.2f%%   %s' % (100 * a01, 100 * (CHARGE - a01), verd)
                   if a01 is not None else '         -         -   %s' % verd))
            P('    n by year, ALLPOOL: %s'
              % OUT['arms'][lab].get('%s|%s|ALLPOOL' % (wname, vkey), {}).get('n_by_year'))

# ---- L-SC5 ------------------------------------------------------------------------------------------
K = json.load(open(os.path.join(HERE, '..', 'order_k_2026-08-18', 'STANDING_TABLES_K.json')))
P()
P('-' * 118)
P('L-SC5  the ALLCOH arm tables must reproduce ORDER K\'s STANDING_TABLES_K.json arm cells exactly')
nb = 0; nc = 0
for lab, _ in LABELS:
    if lab not in K['arms']:
        P('  %s is an ORDER M board — ORDER K has no arm cells for it, nothing to reproduce' % lab)
        continue
    for wname, _, _ in WINDOWS:
        for arm in ARM_TYPES + ['ALLPOOL']:
            kd = K['arms'][lab].get('%s|%s' % (wname, arm))
            ld = OUT['arms'][lab].get('%s|ALLCOH|%s' % (wname, arm))
            if kd is None and ld is None:
                continue
            if (kd is None) != (ld is None):
                P('  BREACH presence %s %s %s' % (lab, wname, arm)); nb += 1; continue
            nc += 1
            if kd['n'] != ld['n']:
                P('  BREACH n %s %s %s' % (lab, wname, arm)); nb += 1
            for i in range(8):
                a, c = kd['path'][i], ld['path'][i]
                nc += 1
                if a is None or c is None:
                    if (a is None) != (c is None):
                        P('  BREACH None %s %s %s yr%d' % (lab, wname, arm, i)); nb += 1
                    continue
                if abs(a - c) > 1e-12:
                    P('  BREACH %s %s %s yr%d: K %.12f L %.12f' % (lab, wname, arm, i, a, c)); nb += 1
P('  comparisons %d   mismatches %d' % (nc, nb))
P('  L-SC5 %s' % ('PASS — the arm tables are Order K\'s arm tables, unchanged'
                  if nb == 0 else 'FAIL'))
assert nb == 0, 'L-SC5 FAILED'

json.dump(OUT, open(os.path.join(HERE, 'ARMS_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'ARMS_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote ARMS_P.json / ARMS_P_out.txt')
