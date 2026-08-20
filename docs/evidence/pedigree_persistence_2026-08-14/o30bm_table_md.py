#!/usr/bin/env python3
"""Emits PERSISTENCE_TABLE.md from PERSISTENCE_TABLE.json + DERIVATION.json. Presentation only --
it computes no quantity that is not already in those two files."""
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'PERSISTENCE_TABLE.json')))
D = json.load(open(os.path.join(HERE, 'DERIVATION.json')))
L = []
def W(s=''):
    L.append(s)


GB = ['0-5', '6-15', '16-35', '36-70', '71+']
PB = ['A 1-6', 'B 7-12', 'C 13-20', 'D 21-40', 'E 41-64']
POSES = ['KPD', 'KPF', 'MID', 'RUCK', 'SD', 'SF']
m = T['meta']


def f(x, d=1):
    return '—' if x is None else ('%.*f' % (d, float(x)))


W('# PERSISTENCE TABLE — ORDER 30B-M')
W()
W('Machine-readable twin: `PERSISTENCE_TABLE.json` (every cell, including the ones too thin to print).')
W('Harness: `o30bm_measure.py` · derivation: `o30bm_derive.py` · prereg: `PREREG_30BM.md`.')
W('**READ-ONLY. NOTHING WIRES.**')
W()
W('## 0 · Population, window, censoring')
W()
W('| | |')
W('|---|---|')
W('| population | %s |' % m['population'])
W('| panel | **%d states** over **%d careers**; state years 2006–2019, entry years 2005–2018 |' % (m['n_states'], m['n_careers']))
W('| left censoring | %s |' % m['censor_left'])
W('| right censoring | %s |' % m['censor_right'])
W('| survivorship | %s |' % m['survivorship'])
W('| scorer | %s |' % m['scorer'])
W('| bars (engine-read, Ruling 1 asserted) | %s |' % ', '.join('%s %.1f' % (k, v) for k, v in sorted(m['bars'].items())))
W('| discount | flat %.0f%%/yr, re-anchored at the state year |' % (100 * m['disc']))
W('| horizon | H = %d observed seasons (H=4 / H=10 as declared sensitivities) |' % m['horizon_primary'])
W('| force majeure | %s (excluded entirely; the pick slide is carried in `effective_pick`) |' % ', '.join(m['force_majeure']))
W('| pool band | %d states, descriptive only — never fitted (no v0 ladder position) |' % m['n_pool_states'])
W('| pins | layer1 `%s` · v0 artifact `%s` · board `%s` · store `%s` · rl_model `%s` |'
  % (m['pins']['layer1'][:8], m['pins']['v0_artifact'][:8], m['pins']['board'][:8],
     m['pins']['store'][:8], m['pins']['rl_model'][:8]))
W()
W('## 1 · The shape of the target — remaining 6-season delivered value, by games-so-far')
W()
W('| games so far | n | mean | p25 | median | p75 | zero share |')
W('|---|---:|---:|---:|---:|---:|---:|')
for g in GB:
    d = T['skew_by_games_band'][g]
    W('| %s | %d | %s | %s | %s | %s | %.1f%% |' % (g, d['n'], f(d['mean']), f(d['p25']), f(d['median']), f(d['p75']), 100 * d['zero_share']))
W()
W('Delivered value is star-dominated at every depth — the median is a fraction of the mean throughout.')
W('Every table below reports n and dispersion for this reason; no bare mean stands alone.')
W()
W('## 2 · The entry anchor — the pick spread with NO output information')
W()
W('| pick band | n | mean R6 | p25 | median | p75 | zero share | mean v0 | **R6 / v0** |')
W('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for b in PB:
    d = T['entry_anchor']['by_pick_band'][b]
    W('| %s | %d | %s | %s | %s | %s | %.1f%% | %s | **%.4f** |'
      % (b, d['n'], f(d['mean']), f(d['p25']), f(d['median']), f(d['p75']), 100 * d['zero_share'],
         f(d['mean_v0']), D['entry_ruler_R6_over_v0'][b]))
rr = list(D['entry_ruler_R6_over_v0'].values())
W()
W('**The Step-1 v0 ladder survives its own outcome check.** Realized six-season delivered value is a')
W('near-constant fraction of v0 across all five pick bands (%.4f–%.4f, max/min %.3f). The ladder\'s'
  % (min(rr), max(rr), max(rr) / min(rr)))
W('PICK SHAPE is confirmed by outcomes; what the rest of this table measures is how long that shape')
W('keeps mattering once games arrive.')
W()
W('## 3 · Q1 — THE PERSISTENCE CURVE')
W()
W('Within each games band: `R6 ~ position dummies + age + age² + output + output² + current production')
W('+ 3-season production + games this season + log1p(games so far) + v0`. `σ` is the pedigree share —')
W('`β_v0 · mean(v0) / mean(R6)` — the fraction of expected remaining value carried by the pick term')
W('after production, age and position have taken everything they can. Standard errors are')
W('cluster-robust on player; the CI is a 300-replicate player-cluster bootstrap.')
W()
W('| games so far | n | clusters | β_v0 | cluster t | **σ (pedigree share)** | σ 90% CI | ruled blend `1−w` at midpoint | old anchor carry |')
W('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for g in GB:
    d = T['q1_persistence']['band_fits'][g]
    ci = d.get('sigma_ci') or [None, None]
    W('| %s | %d | %d | %.5f | %.2f | **%.1f%%** | %.1f%% … %.1f%% | %.1f%% | ~40%% |'
      % (g, d['n'], d['n_clusters'], d['beta_v0'], d['t_v0'], 100 * d['sigma'],
         100 * ci[0], 100 * ci[1], 100 * d['blend_implied_share_at_midpoint']))
W()
W('**At `g = 36` exactly** (isaac-kako\'s games count), log-linear interpolation between the measured')
W('band midpoints 25.5 and 53.0 — *an interpolation, labelled as one*:')
W()
W('| | pedigree share at 36 games |')
W('|---|---:|')
W('| **MEASURED (this order)** | **%.1f%%** |' % (100 * T['q1_persistence']['sigma_interpolated_at_36_games']))
W('| the ruled blend, `1 − w(36)` | %.2f%% |' % (100 * T['q1_persistence']['blend_share_at_36_games']))
W('| the old machinery\'s anchor carry | ~40% |')
W()
W('### 3.1 · The same claim without a model — matched contrasts')
W()
W('Stratum = position × age band × output band; a cell needs n ≥ 8 to be used; the preregistered')
W('collapse ladder is quintile → tercile → stratum dropped, and both rungs are printed.')
W()
W('| games so far | quintile lens: strata | Δ (top − bottom pick band) | tercile lens: strata | Δ | weight |')
W('|---|---:|---:|---:|---:|---:|')
for g in GB:
    a = T['q1_persistence']['matched_quintile'][g]
    b = T['q1_persistence']['matched_tercile'][g]
    W('| %s | %d | %s | %d | %s | %.0f |'
      % (g, a['n_strata_used'], f(a['delta_weighted']), b['n_strata_used'], f(b['delta_weighted']), b['weight']))
W()
W('The quintile lens leaves **0 usable strata at 16–35 games** — that is the thin-cell case the')
W('preregistered ladder exists for, and it is disclosed rather than quietly collapsed. Cells collapsed')
W('out: %d on the quintile lens, %d on the tercile lens.'
  % (T['q1_persistence']['n_collapsed_quintile'], T['q1_persistence']['n_collapsed_tercile']))
W()
W('**Residual contrast** — the same claim with the whole panel behind it. The pick-blind production')
W('model is fitted within each games band; the mean residual by pick class is the pick information the')
W('production features could not carry. 90% CI is a player-cluster bootstrap.')
W()
W('| games so far | n picks 1–12 | mean residual | n picks 21–64 | mean residual | gap | gap 90% CI |')
W('|---|---:|---:|---:|---:|---:|---:|')
for g in GB:
    d = T['q1_persistence']['residual_contrast'][g]
    if d.get('gap') is None:
        W('| %s | — | — | — | — | — | — |' % g); continue
    ci = d['gap_ci90']
    W('| %s | %d | %s | %d | %s | **%s** | %s … %s |'
      % (g, d['n_hi'], f(d['mean_hi']), d['n_lo'], f(d['mean_lo']), f(d['gap']), f(ci[0]), f(ci[1])))
W()
W('The gap is positive at every depth and its sign never turns; the confidence interval crosses zero')
W('from 16–35 games onward, which is the honest statement of the power available at these n.')
W()
W('### 3.2 · The pool band (never fitted, carried for the record)')
W()
W('| games so far | n pool | mean R6 pool | n band A | mean R6 A | n band E | mean R6 E |')
W('|---|---:|---:|---:|---:|---:|---:|')
for g in GB:
    d = T['pool_band'][g]
    W('| %s | %d | %s | %d | %s | %d | %s |' % (g, d['pool']['n'], f(d['pool']['mean']),
                                                d['band_A']['n'], f(d['band_A']['mean']),
                                                d['band_E']['n'], f(d['band_E']['mean'])))
W()
W('## 4 · Q2 — THE FORM')
W()
W('Same target, same panel, same folds. `P` = production only · `L` = `P` + `v0` + `v0·log1p(g)` (the')
W('blend\'s shape, generalised) · `T` = `L` + pick-class × development-axis interactions (the owner\'s')
W('hypothesis: the growth curve itself is pick-conditional). Criterion and decision rule preregistered:')
W('**≥ 2.0% held-out RMS reduction AND ≥ 4 of 5 folds**, folds grouped by player, no RNG.')
W()
W('| form | parameters | held-out RMS | held-out MAE | held-out Spearman |')
W('|---|---:|---:|---:|---:|')
for k in ('P', 'L', 'T'):
    c = T['q2_form']['cv'][k]
    W('| %s | %d | **%.2f** | %.2f | %.4f |' % (k, c['k_params'], c['rms'], c['mae'], c['spearman']))
W()
cpl, clt = T['q2_form']['compare_P_L'], T['q2_form']['compare_L_T']
W('| comparison | RMS reduction | folds won | bar | adopted? |')
W('|---|---:|---:|---:|---|')
W('| P → L | %.2f%% | %d / 5 | 2.0%% + 4/5 | **%s** |' % (100 * cpl['rms_reduction'], cpl['folds_won_by_richer'], 'YES' if cpl['adopt_richer'] else 'NO'))
W('| L → T | %.2f%% | %d / 5 | 2.0%% + 4/5 | **%s** |' % (100 * clt['rms_reduction'], clt['folds_won_by_richer'], 'YES' if clt['adopt_richer'] else 'NO'))
W()
W('**Q2 VERDICT, by the preregistered rule: %s.**' % T['q2_form']['verdict'])
W()
W('Time-block hold-out (fit on state years ≤ 2012, test on ≥ 2013 — 1,219 train / 2,814 test):')
W()
W('| form | RMS | MAE | Spearman |')
W('|---|---:|---:|---:|')
for k in ('P', 'L', 'T'):
    t = T['q2_form']['time_block'][k]
    W('| %s | %.2f | %.2f | %.4f |' % (k, t['rms'], t['mae'], t['spearman']))
W()
W('### 4.1 · The pick terms themselves (full panel, cluster-robust on player)')
W()
co = T['q2_form']['coefficients']
W('| term | β | cluster SE | t |')
W('|---|---:|---:|---:|')
for n in ('v0', 'v0_lg'):
    c = co['L'][n]
    W('| `%s` | %.6f | %.6f | **%.2f** |' % (n, c['beta'], c['se'], c['t']))
W()
W('The level form\'s two pick terms are individually strong (t = %.2f and t = %.2f) and say exactly what'
  % (co['L']['v0']['t'], co['L']['v0_lg']['t']))
W('the persistence curve says: a positive pick effect that decays in log games. What they do NOT do is')
W('move held-out squared error by 2% — because squared error in this target is dominated by which')
W('handful of players become stars, and the pedigree term moves the whole distribution modestly rather')
W('than calling the tail. Both facts are the measurement.')
W()
W('Form `T`\'s interaction terms (reference class = picks 13–30):')
W()
W('| term | β | cluster SE | t |')
W('|---|---:|---:|---:|')
for n, c in co['T'].items():
    if '_x_' in n or n.startswith('d_'):
        W('| `%s` | %.4f | %.4f | %.2f |' % (n, c['beta'], c['se'], c['t']))
W()
W('### 4.2 · Where each form is right and wrong (held-out RMS by cell; same predictions, sliced)')
W()
for lab in ('games_band', 'pick_class', 'young_thin'):
    W('**by %s**' % lab.replace('_', ' '))
    W()
    W('| cell | n | RMS P | RMS L | RMS T | best |')
    W('|---|---:|---:|---:|---:|---|')
    bc = T['q2_form']['by_cell_heldout_rms'][lab]
    for k in sorted(bc['P']):
        a, b, c = bc['P'][k], bc['L'][k], bc['T'][k]
        best = min((('P', a['rms']), ('L', b['rms']), ('T', c['rms'])), key=lambda t: t[1])[0]
        W('| %s | %d | %.1f | %.1f | %.1f | %s |' % (k, a['n'], a['rms'], b['rms'], c['rms'], best))
    W()
W('## 5 · Q3 — POSITION CLOCKS')
W()
q3 = T['q3_clocks']
W('| model | parameters | held-out RMS | MAE | Spearman |')
W('|---|---:|---:|---:|---:|')
for k in ('P1', 'P6'):
    c = q3['cv'][k]
    W('| %s | %d | %.2f | %.2f | %.4f |' % (k, c['k_params'], c['rms'], c['mae'], c['spearman']))
W()
W('P1 → P6: %.2f%% RMS reduction, %d/5 folds. **Q3 VERDICT, by the same rule: %s.**'
  % (100 * q3['compare']['rms_reduction'], q3['compare']['folds_won_by_richer'], q3['verdict']))
W()
W('**The preregistered peak-age lens carries NO SIGNAL, and the prereg is breached on it.** %s'
  % q3['preregistered_peak_age_lens'])
W()
W('**Supplementary (post-hoc, descriptive, does NOT re-decide Q3):** the raw development clock —')
W('median change in season average from one season to the next, players with ≥ 5 games in both.')
W()
ages = list(range(18, 29))
W('| position | ' + ' | '.join('age %d' % a for a in ages) + ' |')
W('|---' * (len(ages) + 1) + '|')
for p in POSES:
    row = q3['supplementary_raw_growth_clock'][p]
    W('| **%s** | ' % p + ' | '.join((('%+.1f' % row[str(a)]['median_delta_avg']) if str(a) in row else '·') for a in ages) + ' |')
W('| *n (all groups)* | ' + ' | '.join(str(sum(q3['supplementary_raw_growth_clock'][p][str(a)]['n']
                                               for p in POSES if str(a) in q3['supplementary_raw_growth_clock'][p]))
                                       for a in ages) + ' |')
W()
lp = q3['supplementary_last_positive_growth_age']
W('Last age with a positive median growth step: ' + ' · '.join('**%s** %s' % (p, lp[p]) for p in POSES) + '.')
W('Tall mean %.2f vs small/mid mean %.2f — a gap of **%.2f years**.'
  % (sum(lp[p] for p in ('KPD', 'KPF', 'RUCK')) / 3.0, sum(lp[p] for p in ('MID', 'SF', 'SD')) / 3.0,
     q3['supplementary_gap_years']))
W()
W('## 6 · Named rows')
W()
W('| player | pick | pos | games | age | output | board price | v0 | pred P | pred L | pred T |')
W('|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in T['named_rows']:
    W('| `%s` | %d | %s | %.0f | %d | %.1f | %s | %.1f | %.1f | %.1f | %.1f |'
      % (r['key'], r['pick'], r['pos'], r['games'], r['age'], r['output'], r['board_price'],
         r['v0'], r['pred_P'], r['pred_L'], r['pred_T']))
W()
W('*Prediction states are 2026 — in progress. `cur` for these rows is a part-season at full-season')
W('weight (≥10 games caps the weight at 1), which is disclosed, not corrected.*')
W()
W('## 7 · Historical validation cohorts')
W()
W('Selection rule, fixed in the prereg: **a state at 30–40 games whose output is below the median of')
W('its own position group.** The names fall out of the rule.')
W()
hc = T['historical_cohorts']
for c in ('picks_1_10', 'picks_40_plus'):
    s = hc['summary'][c]
    W('**%s** — n %d · mean R6 %s · p25 %s · median %s · p75 %s · zero %.0f%%'
      % (c.replace('_', ' '), s['n'], f(s['mean']), f(s['p25']), f(s['median']), f(s['p75']), 100 * s['zero_share']))
    W()
    W('| player | pick | pos | year | age | games | output | **realized R6** | career games |')
    W('|---|---:|---|---:|---:|---:|---:|---:|---:|')
    for d in hc['cohorts'][c]:
        W('| `%s` | %d | %s | %d | %d | %.0f | %.1f | **%.1f** | %s |'
          % (d['key'], d['pick'], d['pos'], d['year'], d['age'], d['games'], d['output'], d['R6'], d['career_games']))
    W()
W('## 8 · Declared sensitivities')
W()
W('| variant | panel n | P→L RMS | folds | L→T RMS | folds | verdict | σ(36–70) |')
W('|---|---:|---:|---:|---:|---:|---|---:|')
for k, v in T['sensitivities'].items():
    if 'cv' not in v:
        W('| %s | — | — | — | — | — | %s | — |' % (k, v.get('note', ''))); continue
    a, b = v['compare_P_L'], v['compare_L_T']
    s = v['sigma_by_games_band'].get('36-70', {}).get('sigma')
    W('| %s | %d | %.2f%% | %d/5 | %.2f%% | %d/5 | %s | %s |'
      % (k, v['n'], 100 * a['rms_reduction'], a['folds_won_by_richer'],
         100 * b['rms_reduction'], b['folds_won_by_richer'], v['verdict'],
         ('%.1f%%' % (100 * s)) if s is not None else '—'))
W()
W('Every declared sensitivity agrees with the primary reading on both verdicts. The pedigree share is')
W('stable across horizon, discount, grace, games-weight and output-axis choices; it falls to 8.5% at')
W('H = 10 (a 10-season window is only observable for state years ≤ 2015, so that reading is thinner')
W('and older) and to 12.3% on the core window alone.')
W()
W('## 9 · Prereg scored by number')
W()
W('| # | verdict | claim | measured |')
W('|---|---|---|---|')
for k in sorted(T['prereg_scored'], key=lambda x: int(x[1:])):
    d = T['prereg_scored'][k]
    W('| **%s** | %s | %s | %s |' % (k, 'HELD' if d['held'] else '**BREACH**', d['claim'],
                                     str(d['measured']).replace('|', '/')))
W()
W('## 10 · All cells')
W()
W('Every cell with n ≥ 8 (position × age band × games band × output quintile × pick band). The full')
W('%d-cell table, including the %d cells too thin to print, is in `PERSISTENCE_TABLE.json` under'
  % (len(T['cells_all_states']), len(T['cells_all_states']) - len(T['cells_reported'])))
W('`cells_all_states`; the thin-cell collapse is disclosed there cell by cell.')
W()
W('| position | age | games | output | pick band | n | mean | p25 | median | p75 | zero |')
W('|---|---|---|---|---|---:|---:|---:|---:|---:|---:|')
for k in sorted(T['cells_reported']):
    d = T['cells_reported'][k]
    p, a, g, o, b = k.split('|')
    W('| %s | %s | %s | %s | %s | %d | %s | %s | %s | %s | %.0f%% |'
      % (p, a, g, o, b, d['n'], f(d['mean']), f(d['p25']), f(d['median']), f(d['p75']), 100 * d['zero_share']))
W()
open(os.path.join(HERE, 'PERSISTENCE_TABLE.md'), 'w').write('\n'.join(L) + '\n')
print('wrote PERSISTENCE_TABLE.md (%d lines)' % len(L))
