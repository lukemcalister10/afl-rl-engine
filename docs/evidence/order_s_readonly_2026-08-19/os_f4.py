#!/usr/bin/env python3
"""ORDER S READ-ONLY — F4. THE SCHEDULE INVERSION: PROVENANCE AND SAMPLE FIRST.

NO SMOOTHING IS PROPOSED. NO REPLACEMENT ROW IS DERIVED. NOTHING IS ADOPTED. This file READS the
published artifacts and reports n, the summary statistics as filed, and the one comparison that
decides whether the inversion is a measured feature or a thin cell — the listed-conditioned reading
against the unconditional one on the same depths.

Artifacts read (none written, none re-derived):
  docs/evidence/candidate_31f/FADE_31F.json                     the LIVE wired row and its cells
  docs/evidence/sitter_fade_2026-08-14/SITTER_DISCOUNT_TABLE_2.json   ORDER 30A-2, three listings
  docs/evidence/sitter_fade_2026-08-14/RECUT30A2_out.txt        30A-2's own console, T4 included
  engine/rl_after/_merged_recover.py                            the wired literal, asserted

  usage: python3 os_f4.py
"""
import json, os, re, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
L = []


def P(s=''):
    print(s); L.append(str(s))


FADE = json.load(open(os.path.join(REPO, 'docs/evidence/candidate_31f/FADE_31F.json')))
T2 = json.load(open(os.path.join(REPO, 'docs/evidence/sitter_fade_2026-08-14/SITTER_DISCOUNT_TABLE_2.json')))
SRC = open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py')).read()

P('=' * 118)
P('ORDER S READ-ONLY — F4. THE ND FADE SCHEDULE INVERSION. PROVENANCE AND SAMPLE, NOTHING ELSE.')
P('=' * 118)
P('NO SMOOTHING IS PROPOSED. NO REPLACEMENT ROW IS DERIVED. NO ENGINE FILE IS EDITED. NOTHING IS')
P('ADOPTED. Every number below is READ out of a published artifact and is quoted as filed.')
P()

# ---- 1 · the wired literal, asserted against the artifact ---------------------------------------------
m = re.search(r"O31_FADE_D=\{(.*?)\}", SRC, re.S)
assert m, 'F4-A1 FIRED: cannot find O31_FADE_D in the engine source'
lit = eval('{' + m.group(1) + '}', {'__builtins__': {}}, {})
P('-' * 118)
P('1 · THE WIRED ROW, AND THAT IT IS THE ARTIFACT\'S ROW')
P('-' * 118)
P('   %-38s %s' % ('engine literal O31_FADE_D', {k: round(v, 10) for k, v in sorted(lit.items())}))
P('   %-38s %s' % ('FADE_31F.json::wired', {int(k): round(v, 10) for k, v in sorted(FADE['wired'].items())}))
for k in lit:
    assert abs(lit[k] - FADE['wired'][str(k)]) < 1e-15, 'F4-A1 FIRED: engine %s != artifact at depth %s' % (lit[k], k)
P('   ASSERTED equal at every depth. Falsifier F4-A1 did not fire.')
P()
P('   THE THREE VINTAGES OF THE SAME ROW, all published in FADE_31F.json:')
P('   %-34s %9s %9s %9s %9s | %-22s' % ('vintage', 'D(1)', 'D(2)', 'D(3)', 'D(4)', 'depth 3 -> depth 4'))
VINT = {}
for nm, key in (('ORDER A / R1, the previously ruled row', 'r1'),
                ('ORDER 31-F re-derived — LIVE / WIRED', 'rederived')):
    d = FADE[key]
    v = [d.get(str(i)) for i in (1, 2, 3, 4)]
    inv = 'INVERTS (+%.4f)' % (v[3] - v[2]) if v[3] > v[2] else 'monotone down (%.4f)' % (v[3] - v[2])
    VINT[nm] = dict(D=v, inverts=v[3] > v[2])
    P('   %-34s %9.4f %9.4f %9.4f %9.4f | %-22s' % (nm, v[0], v[1], v[2], v[3], inv))
lb = T2['T1']['D']['L-B outcome-blind floor']
v = [lb[str(i)] for i in (1, 2, 3, 4)]
VINT['ORDER 30A-2 L-B as filed'] = dict(D=v, inverts=v[3] > v[2])
P('   %-34s %9.4f %9.4f %9.4f %9.4f | %-22s'
  % ('ORDER 30A-2 L-B as filed', v[0], v[1], v[2], v[3],
     'INVERTS' if v[3] > v[2] else 'monotone down (%.4f)' % (v[3] - v[2])))
P()

# ---- 2 · n per depth cell -----------------------------------------------------------------------------
P('-' * 118)
P('2 · n PER DEPTH CELL — THE LIVE ROW\'S OWN POPULATION (FADE_31F.json::cells)')
P('-' * 118)
P('   %-7s %7s %8s %8s %10s %10s %10s %10s %10s %10s'
  % ('depth', 'n', 'n_ever', 'n_zero', 'mean', 'median', 'p25', 'p75', 'POOLED', 'tail share'))
CELLS = {}
for d in ('1', '2', '3', '4', '5', '6'):
    c = FADE['cells'][d]
    CELLS[d] = c
    P('   %-7s %7d %8d %8d %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f'
      % (d, c['n'], c['n_ever'], c['n_zero'], c['mean'], c['median'], c['p25'], c['p75'],
         c['pooled'], c['tail_share']))
P()
P('   THE WIRED VALUE IS THE MEAN, NORMALISED BY THE DEPTH-1 MEAN. Verified here rather than assumed:')
raw1 = FADE['raw1_31f']
for d in ('2', '3', '4'):
    calc = FADE['cells'][d]['mean'] / raw1
    P('     depth %s : cell mean %.10f / raw1 %.10f = %.10f   wired %.10f   |diff| %.2e'
      % (d, FADE['cells'][d]['mean'], raw1, calc, FADE['wired'][d], abs(calc - FADE['wired'][d])))
P()
P('   FALSIFIER F4-P1 — is the depth-4 cell thin (under 30 observations)?')
P('     depth 4 holds %d observations, of which %d ever delivered anything and %d are exact zeros.'
  % (CELLS['4']['n'], CELLS['4']['n_ever'], CELLS['4']['n_zero']))
P('     VERDICT: %s' % ('THIN — F4-P1 did NOT fire' if CELLS['4']['n'] < 30 else 'NOT THIN — F4-P1 FIRED'))
P()
P('   FALSIFIER F4-P4 — does every published statistic on the depth-4 cell invert in the same direction?')
P('   %-14s %12s %12s %12s %-24s' % ('statistic', 'depth 3', 'depth 4', 'difference', 'direction'))
SAME = []
for st in ('mean', 'median', 'p25', 'p75', 'pooled'):
    a, b = CELLS['3'][st], CELLS['4'][st]
    SAME.append(b > a)
    P('   %-14s %12.4f %12.4f %+12.4f %-24s'
      % (st, a, b, b - a, 'INVERTS (4 above 3)' if b > a else 'no inversion'))
P('     the POOLED aggregate — the sum of delivered value over the sum of v0 on the same rows — reads')
P('     %.4f at depth 3 and %.4f at depth 4, a difference of %+.4f. On that statistic the inversion is'
  % (CELLS['3']['pooled'], CELLS['4']['pooled'], CELLS['4']['pooled'] - CELLS['3']['pooled']))
P('     %.1f%% of the mean-based inversion of %+.4f.'
  % (100 * abs(CELLS['4']['pooled'] - CELLS['3']['pooled']) / abs(CELLS['4']['mean'] - CELLS['3']['mean']),
     CELLS['4']['mean'] - CELLS['3']['mean']))
P('     VERDICT: %s' % ('F4-P4 did NOT fire — the statistics disagree' if not all(SAME)
                        else 'F4-P4 FIRED — every statistic inverts'))
P()

# ---- 3 · the comparison that decides it ---------------------------------------------------------------
P('-' * 118)
P('3 · THE COMPARISON NAMED IN ADVANCE — LISTED-CONDITIONED AGAINST UNCONDITIONAL, SAME DEPTHS')
P('-' * 118)
P('   ORDER 30A-2 published all three readings on one population. The L-B floor is the one the live')
P('   engine row was re-derived on. n comes from 30A-2\'s own T4 zero-games cells.')
P()
NLB = {'2': 462, '3': 100, '4': 11}
NUNC = {'2': 462, '3': 234, '4': 154}
NLA = {'2': 462, '3': 146, '4': 35}
P('   %-30s %8s %8s %8s %8s | %-26s' % ('reading', 'D(1)', 'D(2)', 'D(3)', 'D(4)', 'depth 3 -> 4'))
DEC = {}
for nm, key, nn in (('UNCONDITIONAL (ORDER 30A)', 'UNCONDITIONAL (ORDER 30A)', NUNC),
                    ('L-A reconstruction as filed', 'L-A reconstruction as filed', NLA),
                    ('L-B outcome-blind floor', 'L-B outcome-blind floor', NLB)):
    d = T2['T1']['D'][key]
    v = [d[str(i)] for i in (1, 2, 3, 4)]
    inv = v[3] > v[2]
    DEC[nm] = dict(D=v, n=nn, inverts=inv)
    P('   %-30s %8.4f %8.4f %8.4f %8.4f | %-26s'
      % (nm, v[0], v[1], v[2], v[3], 'INVERTS (+%.4f)' % (v[3] - v[2]) if inv else 'monotone down (%.4f)' % (v[3] - v[2])))
P()
P('   %-30s %8s %8s %8s %8s' % ('n at each depth', '', 'depth 2', 'depth 3', 'depth 4'))
for nm, nn in (('UNCONDITIONAL (ORDER 30A)', NUNC), ('L-A reconstruction as filed', NLA),
               ('L-B outcome-blind floor', NLB)):
    P('   %-30s %8s %8d %8d %8d' % (nm, '', nn['2'], nn['3'], nn['4']))
P()
P('   READ IT IN ONE LINE. The conditioning that creates the "still listed after four sat years"')
P('   population is the SAME operation that empties the cell: depth 4 goes from %d rows unconditioned'
  % NUNC['4'])
P('   to %d under L-A and %d under L-B. And the UNCONDITIONAL row is strictly monotone DOWN at every'
  % (NLA['4'], NLB['4']))
P('   depth — %.4f, %.4f, %.4f, %.4f — with NO inversion anywhere.'
  % tuple(DEC['UNCONDITIONAL (ORDER 30A)']['D']))
P()

# ---- 4 · the stability check nobody asked for but that settles it --------------------------------------
P('-' * 118)
P('4 · THE SAME ELEVEN ROWS, TWO v0 BASES — THE DEPTH-4 NUMBER IS NOT STABLE')
P('-' * 118)
P('   ORDER 31-F re-derived the fade on HEAD-FIXED v0. The population did not change materially:')
P('   the L-B depth-3 and depth-4 cells hold %d and %d rows in 30A-2 and %d and %d in 31-F.'
  % (NLB['3'], NLB['4'], FADE['cells']['3']['n'], FADE['cells']['4']['n']))
P()
P('   %-40s %10s %10s %-26s' % ('v0 basis', 'D(3)', 'D(4)', 'depth 3 -> depth 4'))
a = T2['T1']['D']['L-B outcome-blind floor']
P('   %-40s %10.4f %10.4f %-26s'
  % ('30A-2, as filed', a['3'], a['4'],
     'monotone down (%.4f)' % (a['4'] - a['3']) if a['4'] <= a['3'] else 'INVERTS'))
b = FADE['rederived']
P('   %-40s %10.4f %10.4f %-26s'
  % ('31-F, head-fixed v0 — THIS IS THE LIVE ROW', b['3'], b['4'],
     'INVERTS (+%.4f)' % (b['4'] - b['3']) if b['4'] > b['3'] else 'monotone down'))
P()
P('   ON ESSENTIALLY THE SAME ELEVEN ROWS, changing the v0 basis moves D(4) by %+.1f%% and FLIPS the'
  % (100 * (b['4'] / a['4'] - 1)))
P('   ordering against depth 3. FADE_31F.json\'s own drift column records it: %.4f at depth 4 against'
  % FADE['drift_vs_r1']['4'])
P('   %.4f at depth 3 and %.4f at depth 2 — the drift GROWS as the cell empties.'
  % (FADE['drift_vs_r1']['3'], FADE['drift_vs_r1']['2']))
P()
P('   THE DEEPER CELLS, printed because they show where this ends: depth 5 holds %d rows and depth 6'
  % FADE['cells']['5']['n'])
P('   holds %d, and their re-derived values are %.4f and %.4f — ABOVE 1.0 at depth 6, i.e. a player'
  % (FADE['cells']['6']['n'], FADE['rederived']['5'], FADE['rederived']['6']))
P('   who sat six years is measured as delivering MORE than his entry price. The schedule is HELD FLAT')
P('   from depth 4 precisely so those two rows never price anything, and that is the engine\'s own')
P('   O31_FADE_FLAT_FROM = 4.')
P()

# ---- 5 · is a CI recoverable? -------------------------------------------------------------------------
P('-' * 118)
P('5 · IS A CONFIDENCE INTERVAL RECOVERABLE FROM THE PUBLISHED ARTIFACTS? — NO, AND HERE IS WHAT IS')
P('-' * 118)
P('   The per-observation ratios behind each depth cell are NOT published. FADE_31F.json files the')
P('   summary statistics only, and SITTER_DISCOUNT_TABLE_2.json\'s per-player block carries the')
P('   career aggregates but not the per-depth V_from_N share. So a bootstrap CI on the depth-4 cell')
P('   CANNOT be recomputed from the artifacts, and this seat is not inventing one.')
P()
P('   WHAT IS RECOVERABLE, distribution-free, on the depth-4 cell as filed:')
c4, c3 = CELLS['4'], CELLS['3']
P('     n = %d, of which %d are exact zeros. The interquartile range is [%.4f, %.4f] and the median'
  % (c4['n'], c4['n_zero'], c4['p25'], c4['p75']))
P('     is %.4f. The MEAN is %.4f — %.1f times the median, so the cell is carried by its upper tail.'
  % (c4['median'], c4['mean'], c4['mean'] / max(1e-9, c4['median'])))
P('     Its tail share is %.4f against %.4f at depth 3 and %.4f at depth 2, so the depth-4 estimate'
  % (c4['tail_share'], c3['tail_share'], CELLS['2']['tail_share']))
P('     also leans hardest of the three on PROJECTED value rather than observed value.')
P()
P('     With eleven observations a 90% interval on a mean has, at best, its limits set by single')
P('     observations. The published p25 and p75 are the 3rd and 9th of eleven ordered values.')
P('     Any interval this seat printed would be a statement about three data points.')
P()
P('   ORDER 30A-2 SCORED THIS ITSELF, in its own prereg, and it is quoted rather than re-discovered:')
for q in T2['prereg_scored']:
    if q['q'] in ('Q5', 'Q6', 'Q10'):
        P('     %-5s %-9s %s' % (q['q'], q['verdict'], q['detail']))
P()

json.dump(dict(wired=lit, vintages={k: v for k, v in VINT.items()}, cells=CELLS,
               readings={k: dict(D=v['D'], n=v['n'], inverts=v['inverts']) for k, v in DEC.items()},
               drift=FADE['drift_vs_r1'], raw1=raw1,
               ci_recoverable=False),
          open(os.path.join(HERE, 'FOLLOWUP_F4.json'), 'w'), indent=1)
open(os.path.join(HERE, 'FOLLOWUP_F4_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote FOLLOWUP_F4.json and FOLLOWUP_F4_out.txt')
