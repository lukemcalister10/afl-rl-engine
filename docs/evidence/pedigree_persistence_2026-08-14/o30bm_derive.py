#!/usr/bin/env python3
"""ORDER 30B-M -- POST-MEASUREMENT DERIVATION (clearly labelled as such).

This file computes NOTHING new from the data. It reads PERSISTENCE_TABLE.json -- the measurement,
already emitted and already scored against the prereg -- and derives three things the owner needs in
order to RULE on the Step-3 boundary:

  1. the entry ruler's own outcome check: realized 6-season delivered value as a fraction of v0, by
     pick band (does the v0 ladder's SHAPE survive contact with outcomes?);
  2. what a blend re-calibrated to the MEASURED pedigree share would look like -- the same functional
     form the owner already ruled, `1 - w(g) = exp(-(g/tau)^beta)`, refitted to the five measured sigma
     points instead of to an unfitted assumption;
  3. the named rows' pedigree components under the fitted level form.

NOTHING HERE RE-DECIDES A PREREGISTERED VERDICT. It is arithmetic on the measurement, offered so the
owner's ruling has numbers under it. NOTHING WIRES.
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'PERSISTENCE_TABLE.json')))
OUT = os.path.join(HERE, 'DERIVATION.json')
LOG = []
def P(s=''):
    print(s); LOG.append(str(s))


P('=' * 100)
P('ORDER 30B-M -- POST-MEASUREMENT DERIVATION (arithmetic on the measurement; nothing re-decided)')
P('=' * 100)

# ---- 1. the entry ruler against outcomes -----------------------------------------------------------
P('\n1. THE ENTRY RULER AGAINST OUTCOMES -- realized R6 as a fraction of v0, by pick band')
P('   (states at g=0; the pick ladder\'s SHAPE is what is being checked, not its level)')
ea = T['entry_anchor']['by_pick_band']
ratios = {}
P('   %-9s %5s %10s %10s %10s' % ('pickband', 'n', 'mean R6', 'mean v0', 'R6/v0'))
for b in ['A 1-6', 'B 7-12', 'C 13-20', 'D 21-40', 'E 41-64']:
    d = ea[b]
    r = d['mean'] / d['mean_v0']
    ratios[b] = r
    P('   %-9s %5d %10.1f %10.1f %10.4f' % (b, d['n'], d['mean'], d['mean_v0'], r))
rs = list(ratios.values())
P('   spread of R6/v0 across the five bands: min %.4f  max %.4f  max/min %.3f'
  % (min(rs), max(rs), max(rs) / min(rs)))
P('   READING: a FLAT R6/v0 across pick bands means the v0 ladder\'s pick shape is confirmed by')
P('   outcomes; a sloped one would mean the ladder is mis-shaped. This is a check on the STEP-1 ruler.')

# ---- 2. the blend re-calibrated to the measured pedigree share --------------------------------------
P('\n2. THE BLEND\'S OWN FORM, REFITTED TO THE MEASURED PEDIGREE SHARE')
bf = T['q1_persistence']['band_fits']
BANDS = [('0-5', 2.5), ('6-15', 10.5), ('16-35', 25.5), ('36-70', 53.0), ('71+', 85.5)]
pts = [(g, bf[b]['sigma'], bf[b]['n']) for b, g in BANDS if isinstance(bf.get(b), dict) and bf[b].get('sigma') is not None]
P('   measured points (games midpoint, sigma, n): %s' % [(g, round(s, 4), n) for g, s, n in pts])

TAU0, BETA0 = 11.650213, 0.937162
def share(g, tau, beta):
    return math.exp(-((g / tau) ** beta))


def sse(tau, beta, wts=True):
    s = 0.0
    for g, sg, n in pts:
        w = n if wts else 1.0
        s += w * (share(g, tau, beta) - sg) ** 2
    return s


best = None
for tau in np.arange(2.0, 400.0, 0.5):
    for beta in np.arange(0.20, 2.01, 0.01):
        v = sse(float(tau), float(beta))
        if best is None or v < best[0]:
            best = (v, float(tau), float(beta))
_, TAU1, BETA1 = best
P('   ruled blend      : tau %10.6f  beta %8.6f   n-weighted SSE vs measured %.5f'
  % (TAU0, BETA0, sse(TAU0, BETA0)))
P('   refitted to data : tau %10.6f  beta %8.6f   n-weighted SSE vs measured %.5f'
  % (TAU1, BETA1, sse(TAU1, BETA1)))
P('   %-8s %10s %12s %12s' % ('games', 'measured', 'ruled blend', 'refitted'))
for g, sg, n in pts:
    P('   %-8.1f %9.1f%% %11.1f%% %11.1f%%' % (g, 100 * sg, 100 * share(g, TAU0, BETA0), 100 * share(g, TAU1, BETA1)))
P('   crossover (w = 0.5) : ruled %.3f games   refitted %.3f games'
  % (TAU0 * (math.log(2.0)) ** (1.0 / BETA0), TAU1 * (math.log(2.0)) ** (1.0 / BETA1)))
P('   pedigree share at the named states:')
for g in (13, 18, 19, 36, 50, 100):
    P('     g=%3d  measured-form %6.1f%%   ruled blend %6.1f%%' % (g, 100 * share(g, TAU1, BETA1), 100 * share(g, TAU0, BETA0)))
P('   CAVEAT, stated: sigma is the pedigree share of EXPECTED REMAINING DELIVERED VALUE over a')
P('   6-season window; 1-w is the weight on the v0-fade leg of a PRICE. They are the same concept')
P('   only to the extent the price is that expectation. The refit is offered as a CALIBRATION')
P('   CANDIDATE for the owner to rule on, not as a wiring.')

# ---- 3. the named rows' pedigree components ---------------------------------------------------------
P('\n3. NAMED ROWS -- the pedigree component under the fitted LEVEL form')
co = T['q2_form']['coefficients']['L']
bv0, bvlg = co['v0']['beta'], co['v0_lg']['beta']
P('   level-form pedigree term = (%.6f %+.6f * log1p(g)) * v0' % (bv0, bvlg))
rows = []
P('   %-16s %4s %6s %8s %9s %9s %9s %8s %9s %9s'
  % ('player', 'pk', 'games', 'v0', 'board v', 'pred L', 'ped part', 'ped %', 'old 40%', 'blend'))
for r in T['named_rows']:
    g = float(r['games']); v0 = float(r['v0'])
    ped = (bv0 + bvlg * math.log1p(g)) * v0
    predL = float(r['pred_L'])
    bp = r['board_price']
    rows.append(dict(key=r['key'], pick=r['pick'], games=g, v0=v0, board=bp, pred_L=predL,
                     ped_component=ped, ped_share_of_pred=(ped / predL if predL else None),
                     old_machinery_implied=0.40 * (bp or 0), blend_implied=r['blend_ped_share_at_games'] * (bp or 0),
                     measured_form_share=share(g, TAU1, BETA1),
                     measured_form_implied=share(g, TAU1, BETA1) * (bp or 0)))
    P('   %-16s %4d %6.0f %8.1f %9s %9.1f %9.1f %7.1f%% %9.1f %9.1f'
      % (r['key'], r['pick'], g, v0, str(bp), predL, ped, 100 * ped / predL if predL else float('nan'),
         0.40 * (bp or 0), r['blend_ped_share_at_games'] * (bp or 0)))
P('   columns: "old 40%%" = the old machinery\'s anchor-carry share of TODAY\'S board price;')
P('            "blend"    = the ruled blend\'s 1-w(g) share of the same price.')

json.dump(dict(entry_ruler_R6_over_v0=ratios,
               blend_ruled=dict(tau=TAU0, beta=BETA0, sse=sse(TAU0, BETA0)),
               blend_refitted_to_measured_sigma=dict(tau=TAU1, beta=BETA1, sse=sse(TAU1, BETA1),
                                                     grid='tau 2..400 step 0.5, beta 0.20..2.00 step 0.01, n-weighted least squares on the five measured sigma points'),
               sigma_points=[dict(games=g, sigma=s, n=n) for g, s, n in pts],
               named_rows_pedigree=rows,
               status='POST-MEASUREMENT DERIVATION. Arithmetic on PERSISTENCE_TABLE.json. Re-decides nothing. NOTHING WIRES.'),
          open(OUT, 'w'), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, 'DERIVATION_out.txt'), 'w').write('\n'.join(LOG) + '\n')
P('\nwrote %s' % OUT)
