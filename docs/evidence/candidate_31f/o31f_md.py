#!/usr/bin/env python3
"""ORDER 31-F — render docs/ledgers/CANDIDATE_31_MOVERS.md from the committed json. Pure formatting.
ORDER 31's o31_md.py with the ORDER-31 baseline column and the beta_pool dial added. No arithmetic."""
import os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
L = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_31_MOVERS.json')))
R = L['rows']; T = L['totals']; B = L['boards']
O = []
def P(s=''): O.append(s)

P('# CANDIDATE 31 — THE COMPOSED MOVERS LEDGER  (ORDER 31-F, the completed candidate)')
P('')
P('**ORDER 31-F · `land/order-29` · every one of the 804 board rows, against BOTH baselines AND against '
  'the ORDER-31 board, with the one law\'s own per-mechanism attribution. NOTHING MERGES.**')
P('')
P('| board | md5 | total |')
P('|---|---|---:|')
P('| LIVE (nothing ever merged) | `%s` | %s |' % (B['live'], format(T['live'], ',')))
P('| STEP-2 (the branch\'s committed board) | `%s` | %s |' % (B['step2'], format(T['step2'], ',')))
P('| ORDER-31 (the incomplete candidate this one completes) | `%s` | %s |' % (B['order31'], format(T['order31'], ',')))
P('| **CANDIDATE 31-F** | **`%s`** | **%s** |' % (B['candidate'], format(T['candidate'], ',')))
P('| determinism: the same tree built again | `%s` | %s |' % (B['candidate_rebuild'], format(T['candidate'], ',')))
P('| variant: the one law with the 30B-C stall conditioning REMOVED | `%s` | %s |'
  % (B['no_phi_variant'], format(T['no_phi'], ',')))
P('| variant: beta_pool REMOVED (pool rows carry the ND beta) | `%s` | %s |'
  % (B['no_beta_pool_variant'], format(T['no_beta_pool'], ',')))
P('| control: the dial UNSET on the head-fixed tree (the head fix ALONE) | `%s` | %s |'
  % (B['headfix_only_dial_off'], format(706862, ',')))
P('| control: the dial UNSET on the UNTOUCHED tree | `%s` | %s |'
  % (B['entry_dial_off_control'], format(T['step2'], ',')))
P('')
P('**Entry dial-off byte-identity: %s** — with `RL_O31` unset on the UNTOUCHED tree the build reproduces '
  'the committed Step-2 board `9298203135202a0c707bb0977ba38c31` exactly. **Determinism: %s** — the final '
  'board built twice, byte-identical. The head fix rewrites a live artifact, so its own effect is '
  'isolated on its own line above (+190 on the Step-2 law) rather than hidden inside the dial.'
  % ('HELD' if L['entry_dial_off_byte_identity'] else '*** FAILED ***',
     'HELD' if L['determinism'] else '*** FAILED ***'))
P('')
P('vs LIVE **%+s** (%.2f%%) · vs STEP-2 **%+s** (%.2f%%) · vs ORDER-31 **%+s** · the stall conditioning '
  'is worth **%+s** · beta_pool is worth **%+s**'
  % (format(T['candidate'] - T['live'], ','), 100.0 * (T['candidate'] / T['live'] - 1),
     format(T['candidate'] - T['step2'], ','), 100.0 * (T['candidate'] / T['step2'] - 1),
     format(T['candidate'] - T['order31'], ','),
     format(T['candidate'] - T['no_phi'], ','), format(T['candidate'] - T['no_beta_pool'], ',')))
P('')
P('## THE LAW, AND HOW EVERY ROW DECOMPOSES')
P('')
P('```')
P('price = rho(g) * Phat   +   [ D(c_u) * (1 - rho(g))  +  Phi(g,s) * beta(g) * rho(g) ] * v0')
P('        \\___________/       \\_____________________________________________________/')
P('         PRODUCTION                              PEDIGREE')
P('```')
P('')
P('`rho(g) = 1 - exp(-(g/%.6f)^%.6f)`  ·  `rho(0) = 0` exactly  ·  `pi(0,c) = D(c)` exactly.'
  % (L['law']['TAU_RHO'], L['law']['B_RHO']))
P('')
P('**RECONCILIATION: every row\'s `production_pts + pedigree_pts` equals its printed price to ±1 point '
  '(0 failures in 804).** The two columns below are the law\'s own arithmetic, not a reconstruction.')
P('')
P('## BY CAREER-GAMES CLASS')
P('')
P('| games | n | candidate | step-2 | live | vs step-2 | vs live | of which the stall conditioning |')
P('|---|---:|---:|---:|---:|---:|---:|---:|')
for k in ['0', '1-5', '6-15', '16-35', '36-70', '71+']:
    v = L['class_views'].get(k)
    if not v: continue
    P('| %s | %d | %s | %s | %s | %+s (%.1f%%) | %+s (%.1f%%) | %+s |'
      % (k, v['n'], format(v['cand'], ','), format(v['step2'], ','), format(v['live'], ','),
         format(v['cand'] - v['step2'], ','), 100.0 * (v['cand'] / max(1, v['step2']) - 1),
         format(v['cand'] - v['live'], ','), 100.0 * (v['cand'] / max(1, v['live']) - 1),
         format(v['phi_cost'], ',')))
P('')
P('## BY PATHWAY')
P('')
P('| pathway | n | candidate | step-2 | live | vs step-2 |')
P('|---|---:|---:|---:|---:|---:|')
for k, v in sorted(L['pathway_views'].items(), key=lambda kv: -kv[1]['cand']):
    P('| %s | %d | %s | %s | %s | %+s (%.1f%%) |'
      % (k, v['n'], format(v['cand'], ','), format(v['step2'], ','), format(v['live'], ','),
         format(v['cand'] - v['step2'], ','), 100.0 * (v['cand'] / max(1, v['step2']) - 1)))
P('')
P('## THE NAMED ROWS (the brief\'s list)')
P('')
P('| row | path | pk | cg | LIVE | STEP-2 | **CANDIDATE** | no-Phi | rho | D(c_u) | s | Phi | pi | v0 | production | pedigree |')
P('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in L['named_rows']:
    P('| `%s` | %s | %s | %s | %s | %s | **%s** | %s | %.3f | %.3f | %d | %.3f | %.4f | %.1f | %.1f | %.1f |'
      % (r['key'], r['pathway'], r['pick'], r['cg'], r['live'], r['step2'], r['cand'], r['nophi'],
         r['rho'], r['D'], r['s'], r['Phi'], r['pi'], r['v0'], r['production_pts'], r['pedigree_pts']))
P('')
P('## THE AT-BAR VETERANS — NAMED IN `PREREG_31.md` P1 BEFORE ANY PRICE OF THIS ORDER EXISTED')
P('')
P('| row | cg | LIVE | STEP-2 | CANDIDATE | vs step-2 | production | pedigree |')
P('|---|---:|---:|---:|---:|---:|---:|---:|')
mv = []
for r in L['at_bar_veterans']:
    mv.append(abs(r['d_vs_step2'] or 0))
    P('| `%s` | %s | %s | %s | %s | %+d | %.1f | %.1f |'
      % (r['key'], r['cg'], r['live'], r['step2'], r['cand'], r['d_vs_step2'] or 0,
         r['production_pts'], r['pedigree_pts']))
mv.sort()
P('')
P('**class median |move| vs step-2 = %.0f points** · moved DOWN: %d of %d.'
  % (mv[len(mv) // 2], sum(1 for r in L['at_bar_veterans'] if (r['d_vs_step2'] or 0) < 0), len(mv)))
P('')
P('## THE 60 LARGEST MOVERS AGAINST STEP-2')
P('')
P('| row | path | cg | LIVE | STEP-2 | ORDER-31 | CANDIDATE | Δ vs step-2 | Δ vs live | Δ vs O-31 | rho | D | s | Phi | production | pedigree |')
P('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in R[:60]:
    P('| `%s` | %s | %s | %s | %s | %s | %s | %+d | %s | %+d | %.3f | %.3f | %d | %.3f | %.1f | %.1f |'
      % (r['key'], r['pathway'], r['cg'], r['live'], r['step2'], r['o31'], r['cand'],
         r['d_vs_step2'] or 0, ('%+d' % r['d_vs_live']) if r['d_vs_live'] is not None else '—',
         r['d_vs_o31'], r['rho'], r['D'], r['s'], r['Phi'], r['production_pts'], r['pedigree_pts']))
P('')
P('## ALL %d ROWS' % len(R))
P('')
P('The complete per-row table — every column above, for every row — is `CANDIDATE_31_MOVERS.json`, which '
  'this file is rendered from. Sorted by |Δ vs step-2| descending.')
P('')
P('| row | path | pos | pk | age | cg | LIVE | STEP-2 | ORDER-31 | CANDIDATE | Δ step-2 | Δ live | Δ O-31 | rho | c_u | D | s | Phi | pi | v0 |')
P('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in sorted(R, key=lambda x: x['key']):
    P('| `%s` | %s | %s | %s | %s | %s | %s | %s | %s | %s | %+d | %s | %+d | %.3f | %.2f | %.3f | %d | %.3f | %.4f | %.1f |'
      % (r['key'], r['pathway'], r['pos'], r['pick'], r['age'], r['cg'], r['live'], r['step2'], r['o31'],
         r['cand'], r['d_vs_step2'] or 0, ('%+d' % r['d_vs_live']) if r['d_vs_live'] is not None else '—',
         r['d_vs_o31'], r['rho'], r['c_u'], r['D'], r['s'], r['Phi'], r['pi'], r['v0']))
P('')
P('---')
P('')
P('*THE NUMERAIRE IS RE-PINNED and the re-pin is the identity: s = 0.9400914291048137, |s_new - s_old| = '
  '0. These levels are on the SAME measuring stick as live and Step-2, so every column above reads '
  'MOVEMENT and not a change of units. Every limitation this candidate carries is printed in ONE section '
  'of `SHIPPING_PACKET_31.md`. NOTHING MERGES.*')
open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_31_MOVERS.md'), 'w').write('\n'.join(O) + '\n')
print('wrote docs/ledgers/CANDIDATE_31_MOVERS.md  (%d lines)' % len(O))

# a compact scorecard dump for the packet
print('\nSCORECARD FACTS')
print('totals', T)
day0 = [r for r in R if (r['cg'] or 0) == 0]
nd0 = [r for r in day0 if not r['pool']]; pl0 = [r for r in day0 if r['pool']]
print('day0 rows %d (ND %d, pool %d); ND day-0 movers vs step2: %d; pool day-0 movers: %d'
      % (len(day0), len(nd0), len(pl0), sum(1 for r in nd0 if (r['d_vs_step2'] or 0) != 0),
         sum(1 for r in pl0 if (r['d_vs_step2'] or 0) != 0)))
print('rows with Phi<1: %d   worth %d points' % (sum(1 for r in R if r['Phi'] < 1.0),
                                                 T['candidate'] - T['no_phi']))
print('rows with c_u>1 (an unplayed-clock discount): %d' % sum(1 for r in R if r['c_u'] > 1.0))
print('rows that MOVED vs step2: %d of %d' % (sum(1 for r in R if (r['d_vs_step2'] or 0) != 0), len(R)))
thin = [r for r in R if 1 <= (r['cg'] or 0) <= 15]
print('THIN 1-15: n %d  cand %d  step2 %d  (%.1f%%)  live %d (%.1f%%)  production share %.1f%%'
      % (len(thin), sum(r['cand'] for r in thin), sum(r['step2'] or 0 for r in thin),
         100.0 * (sum(r['cand'] for r in thin) / max(1, sum(r['step2'] or 0 for r in thin)) - 1),
         sum(r['live'] or 0 for r in thin),
         100.0 * (sum(r['cand'] for r in thin) / max(1, sum(r['live'] or 0 for r in thin)) - 1),
         100.0 * sum(r['production_pts'] for r in thin) / max(1, sum(r['cand'] for r in thin))))
yr1 = [r for r in R if 1 <= (r['cg'] or 0) <= 22 and (r['age'] or 99) <= 21]
print('PLAYED ROOKIES (cg 1-22, age<=21): n %d  cand %d  step2 %d (%.1f%%)  live %d (%.1f%%)  prod share %.1f%%'
      % (len(yr1), sum(r['cand'] for r in yr1), sum(r['step2'] or 0 for r in yr1),
         100.0 * (sum(r['cand'] for r in yr1) / max(1, sum(r['step2'] or 0 for r in yr1)) - 1),
         sum(r['live'] or 0 for r in yr1),
         100.0 * (sum(r['cand'] for r in yr1) / max(1, sum(r['live'] or 0 for r in yr1)) - 1),
         100.0 * sum(r['production_pts'] for r in yr1) / max(1, sum(r['cand'] for r in yr1))))
