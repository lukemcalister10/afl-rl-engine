#!/usr/bin/env python3
"""ORDER 32 S5 STEP 2 -- fit residuals by pick band, with stage decomposition + composition control.

Sign convention (PREREG_S5.md): R = FITTED v0 MINUS RAW.  R < 0 = the band is UNDERPRICED at entry.
Stages (player-weighted over the 1,142 fit rows; each row valued at its (pos,pick) cell):
    R_total  = mean(fit)      - mean(raw value)     fit vs the data
    R_smooth = mean(loclin)   - mean(raw value)     what the local-linear estimator moved
    R_shrink = mean(pava_in)  - mean(loclin)        what the K=15 thin-sample shrink moved
    R_pava   = mean(fit)      - mean(pava_in)       what PAVA + floor + tiebreak + lambda moved
    R_total == R_smooth + R_shrink + R_pava  (identity, asserted)
Writes S5_RESIDUALS.json + s5_step2_out.txt.
"""
import json, os, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
INP = json.load(open(os.path.join(HERE, 'S5_INPUTS.json')))
_OUT = []
def P(s=''):
    print(s); _OUT.append(s)

POS = sorted(INP['posv_fitted'].keys())
PICKS = list(range(1, 65))
fin = {g: {int(k): v for k, v in INP['posv_fitted'][g].items()} for g in POS}
pin = {g: {int(k): v for k, v in INP['posv_pava_input'][g].items()} for g in POS}
loc = {g: {int(k): v for k, v in INP['posv_raw_loclin'][g].items()} for g in POS}
rows = INP['rows']

BANDS = [('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)]
def band_of(p):
    for nm, lo, hi in BANDS:
        if lo <= p <= hi: return nm
def sd(vs):
    n = len(vs); m = sum(vs) / n
    return math.sqrt(sum((v - m) ** 2 for v in vs) / (n - 1)) if n > 1 else 0.0

def agg(rws):
    n = len(rws)
    if n == 0: return None
    vals = [r['value'] for r in rws]
    mfit = sum(fin[r['pos']][r['pick']] for r in rws) / n
    mpin = sum(pin[r['pos']][r['pick']] for r in rws) / n
    mloc = sum(loc[r['pos']][r['pick']] for r in rws) / n
    mraw = sum(vals) / n
    o = dict(n=n, raw_mean=mraw, raw_sd=sd(vals), raw_se=sd(vals) / math.sqrt(n),
             fit_mean=mfit, pava_in_mean=mpin, loclin_mean=mloc,
             R_total=mfit - mraw, R_smooth=mloc - mraw, R_shrink=mpin - mloc, R_pava=mfit - mpin)
    assert abs(o['R_total'] - (o['R_smooth'] + o['R_shrink'] + o['R_pava'])) < 1e-9
    o['R_total_pct'] = 100.0 * o['R_total'] / mfit
    o['R_pava_pct'] = 100.0 * o['R_pava'] / mfit
    return o

P('ORDER 32 S5 STEP 2 -- RESIDUALS BY BAND (R = fitted v0 minus raw; R<0 = underpriced at entry)')
P('  population: %d fit rows, entry years 2004-2021; all values on the #338 min-tenure delivered basis' % len(rows))
P('')

byband = collections.defaultdict(list)
for r in rows:
    byband[band_of(r['pick'])].append(r)

pooled = {}
P('POOLED (player-weighted), FULL WINDOW')
P('  %-6s %4s %9s %8s %9s %9s %9s | %8s %8s %8s %8s | %7s %7s' %
  ('band', 'n', 'raw_mean', 'raw_se', 'raw_sd', 'fit_mean', 'pava_in', 'R_total', 'R_smth', 'R_shrk', 'R_pava', 'Rtot%', 'Rpav%'))
for nm, lo, hi in BANDS:
    a = agg(byband[nm]); pooled[nm] = a
    P('  %-6s %4d %9.1f %8.1f %9.1f %9.1f %9.1f | %+8.1f %+8.1f %+8.1f %+8.1f | %+6.1f%% %+6.1f%%' %
      (nm, a['n'], a['raw_mean'], a['raw_se'], a['raw_sd'], a['fit_mean'], a['pava_in_mean'],
       a['R_total'], a['R_smooth'], a['R_shrink'], a['R_pava'], a['R_total_pct'], a['R_pava_pct']))
G = pooled['21-30']['R_total'] - pooled['31-40']['R_total']
Gp = pooled['21-30']['R_pava'] - pooled['31-40']['R_pava']
P('')
P('  THE GAP STATISTIC  G = R_total(21-30) - R_total(31-40) = %+.1f v0 points' % G)
P('  PAVA-stage gap        R_pava(21-30) - R_pava(31-40)   = %+.1f v0 points' % Gp)
P('')

# ---- composition ----------------------------------------------------------------------------------
P('COMPOSITION -- position mix per band (share of band n)')
mix = {}
P('  %-6s' % 'band' + ''.join('%12s' % g for g in POS))
for nm, lo, hi in BANDS:
    c = collections.Counter(r['pos'] for r in byband[nm]); tot = len(byband[nm])
    mix[nm] = {g: c.get(g, 0) for g in POS}
    P('  %-6s' % nm + ''.join('%7d %3.0f%%' % (c.get(g, 0), 100.0 * c.get(g, 0) / tot) for g in POS))
P('')

within = {}
P('WITHIN-POSITION RESIDUALS PER BAND (composition control: does the 21-30 pattern survive inside position?)')
for g in POS:
    within[g] = {}
    line = '  %-5s' % g
    for nm, lo, hi in BANDS:
        rws = [r for r in byband[nm] if r['pos'] == g]
        a = agg(rws); within[g][nm] = a
        line += '  %s' % ('%s n%d R%+.0f' % (nm, a['n'], a['R_total']) if a else '%s n0' % nm)
    P(line)
P('')
P('  R_total per position x band, as %% of the position-band fitted mean (n in parens)')
P('  %-6s' % 'pos' + ''.join('%16s' % nm for nm, _, _ in BANDS))
for g in POS:
    line = '  %-6s' % g
    for nm, _, _ in BANDS:
        a = within[g][nm]
        line += '%16s' % ('-' if not a else '%+.0f%% (%d)' % (a['R_total_pct'], a['n']))
    P(line)
P('')
P('  within-position gap sign check, positions with n>=20 in BOTH 21-30 and 31-40:')
signs = {}
for g in POS:
    a, b = within[g]['21-30'], within[g]['31-40']
    if a and b and a['n'] >= 20 and b['n'] >= 20:
        gg = a['R_total'] - b['R_total']
        signs[g] = gg
        P('    %-5s G_within = R(21-30)-R(31-40) = %+.1f  (n %d/%d)' % (g, gg, a['n'], b['n']))
P('')

# ---- the constraint at the cell level in 21-40 ----------------------------------------------------
P('WHERE THE MONOTONE MACHINERY MOVED VALUE IN PICKS 21-40 (fit - pava_input, per cell, player-n weighted view)')
P('  %-5s %s' % ('pos', 'cells with |fit-pava_in| > 1 point, picks 21-40'))
for g in POS:
    moved = [(p, fin[g][p] - pin[g][p]) for p in range(21, 41) if abs(fin[g][p] - pin[g][p]) > 1.0]
    P('  %-5s %s' % (g, '  '.join('%d:%+.0f' % (p, d) for p, d in moved) or '(none)'))
P('')
P('  PAVA pooled blocks (from Step 1): %s' % json.dumps(INP['pava_blocks']))

json.dump(dict(order='ORDER 32 S5 STEP 2', bands=[b[0] for b in BANDS],
               pooled=pooled, gap_R_total=G, gap_R_pava=Gp, mix=mix,
               within_position=within, within_gap_signs=signs),
          open(os.path.join(HERE, 'S5_RESIDUALS.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 's5_step2_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
P('')
P('S5_RESIDUALS.json written.')
