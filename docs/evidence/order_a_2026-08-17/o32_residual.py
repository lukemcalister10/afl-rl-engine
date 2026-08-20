#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — M7: THE R-CLASSLEVEL RESIDUAL ATTRIBUTION (owner ruling, verbatim
discipline: "build with mechanisms only -> measure the class -> close any residual CELL-WISE via
the hindsight surface; a uniform component only if the measured residual is itself uniform, and
only on an explicit owner word (halt-and-ask)").

The measurement (W2_32_RESULTS.json, the committed instrument's own numbers):
  class mean 2005-15 = 1.0334, target band [1.100, 1.117] -> residual +6.7 to +8.4 points.

THE ATTRIBUTION, BY CELL, WITH THE ALGEBRA STATED: the hindsight surface's cells are WITHIN-CLASS
SHARES (each class's prices and realized values normalized to their own class means). By
construction Σ n_b·share_b = N on BOTH sides, so the n-weighted cell gaps sum to ~zero and closing
every cell gap to its realized value moves the class-mean LEVEL by ~ZERO. This script verifies
that identity numerically on the candidate's own cells. CONSEQUENCE: no cell-wise closure via the
hindsight surface can reach the level band — the measured residual is a UNIFORM (level) component,
which is exactly the shape W2's mechanical identity predicts (R* = 1.14 x (1 - SV1share): the fair
mark is a carry statement, not a cell statement) and exactly what W2 proposed to wire "via the
class-level entry basis / early-curve carry rather than via spread steepening".

VERDICT: F2 FIRES — HALT AND REPORT. The uniform wire requires an explicit owner word; nothing is
added silently.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, 'W2_32_RESULTS.json')))
import numpy as np
per = {r['cls']: r['R_cand'] for r in R['level']['per_class_all']}
mean_0515 = float(np.mean([per[y] for y in range(2005, 2016)]))
cells = R['spread']['S3']['buckets']
terc = R['spread']['S3']['terciles']

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

P('ORDER A / CANDIDATE 32 — M7 RESIDUAL ATTRIBUTION (R-CLASSLEVEL)')
P('')
P('  measured class mean 2005-15 .... %.4f' % mean_0515)
P('  target band .................... [1.100, 1.117]')
P('  residual ....................... %+.1f to %+.1f points of year-1 class appreciation'
  % (100 * (1.100 - mean_0515), 100 * (1.117 - mean_0515)))
P('')
P('  BY CELL (within-class shares; gap = realized - candidate price):')
P('  %-8s %5s %12s %12s %8s %22s' % ('cell', 'n', 'price share', 'real share', 'gap', 'n-weighted gap (level)'))
tot_w = 0.0
N = 0
for b in ('0', '1-4', '5-9', '10-15', '16+'):
    c = cells[b]
    tot_w += c['n'] * c['gap']; N += c['n']
    P('  %-8s %5d %12.3f %12.3f %+8.3f %22.1f' % (b, c['n'], c['mean_price_share'], c['mean_real_share'], c['gap'], c['n'] * c['gap']))
P('  %-8s %5d %35s %+8.4f  <- the shares identity: ~0' % ('SUM', N, '', tot_w / N))
P('')
P('  THE ALGEBRA: shares are normalized within class, so Σ n·gap ≈ 0 (measured %.4f per row).' % (tot_w / N))
P('  Closing every cell to its realized share moves the class-mean LEVEL by ~zero. The residual')
P('  has NO cell-wise closure on the hindsight surface: it is a UNIFORM level component —')
P('  W2\'s own identity (R* = 1.14·(1−SV1sh) ≈ 1.11) says the fair level is a CARRY statement.')
P('')
P('  WHAT REMAINS CELL-WISE (the mix, already pushed to its feasible edge): the 5-9g terciles')
P('  still gap (poor %+.3f, riser %+.3f) because the ruled at-bar continuity object caps the' % (terc['5-9/poor']['gap'], terc['5-9/riser']['gap']))
P('  pedigree de-rating at η=0.30 (REMIX_32.json). Closing THOSE would need a channel that')
P('  discriminates SHOWN production inside the cell beyond ρ·Phat — out of the ruled scope,')
P('  named for the owner.')
P('')
P('  VERDICT: F2 FIRES — the residual is uniform. HALT AND REPORT: the +6.7 to +8.4 point')
P('  class-level component requires an explicit owner word (W2\'s named wire: the class-level')
P('  entry basis / early-curve carry). NOTHING IS ADDED SILENTLY. Note the constraint the owner')
P('  will face: a uniform +8 points lifts the hot classes (2010 at 1.1352) through the 1.14')
P('  no-arb line unless the wire acts on the ENTRY BASIS (the denominator) rather than the')
P('  year-1 marks — stated here so the halt question arrives with its geometry attached.')

json.dump(dict(mean_0515=mean_0515, band=[1.100, 1.117],
               residual_points=[100 * (1.100 - mean_0515), 100 * (1.117 - mean_0515)],
               cells={b: cells[b] for b in cells}, terciles=terc,
               n_weighted_gap_sum_per_row=tot_w / N,
               attribution='UNIFORM — the shares identity makes cell-wise closure level-neutral',
               verdict='F2 HALT: uniform component requires an explicit owner word',
               owner_geometry='a uniform lift on year-1 marks breaches 1.14 at the hot classes; '
                              'an entry-basis wire does not'),
          open(os.path.join(HERE, 'RESIDUAL_32.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'RESIDUAL_32_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: RESIDUAL_32.json / RESIDUAL_32_out.txt')
