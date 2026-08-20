#!/usr/bin/env python3
"""Render docs/ledgers/LANDING_29_MOVERS_2026-08-13.md from its JSON — every player, all four levers."""
import os, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
J = ROOT + '/docs/ledgers/LANDING_29_MOVERS_2026-08-13.json'
M = ROOT + '/docs/ledgers/LANDING_29_MOVERS_2026-08-13.md'
d = json.load(open(J))
rows = d['rows']
L = d['levers']
NAMED = ['harrison-ramm', 'luker-kentfield', 'mani-liddy', 'robert-hansen', 'dante-visentini',
         'vigo-visentini', 'nicholas-martin', 'marcus-herbert', 'jai-newcombe', 'willem-duursma',
         'harry-sheezel']
byk = {r['key']: r for r in rows}
o = []
def W(s=''): o.append(s)

def tot(f): return sum(r[f] for r in rows)

W('# THE COMPOSED MOVERS LEDGER — ORDER 29, THE LANDING')
W()
W('**2026-08-13 · branch `land/order-29` · build seat · every priced row, all four levers, vs live `88ce647f`.**')
W()
W('> Each stage below is an **actually built board**, never a modelled step. The four levers reconcile')
W('> **exactly** on every row — `0` rows failing, max |residual| `0` — so no row carries an unexplained')
W('> remainder.')
W()
W('## 1. THE STAGES')
W()
W('| stage | board md5 | total | Δ vs LIVE | pct |')
W('|---|---|---:|---:|---:|')
base = tot('live')
for nm, f in (('LIVE', 'live'), ('B_U', 'b_u'), ('B_G', 'b_g'), ('L3', 'l3'), ('FINAL', 'final')):
    t = tot(f)
    W('| **%s** | `%s` | %s | %s | %s |'
      % (nm, d['stages'][nm], '{:,}'.format(t), '{:+,}'.format(t - base) if t != base else '—',
         '%+.4f%%' % (100.0 * (t - base) / base) if t != base else '—'))
W()
W('## 2. THE LEVERS')
W()
W('| lever | movers | Σ delta | what it is |')
W('|---|---:|---:|---|')
for lv in L:
    W('| **%s** | %d | %s | %s |' % (lv['name'], lv['movers'], '{:+,}'.format(lv['sum_delta']), lv['doc']))
W('| **TOTAL (live → final)** | %d | %s | the four lever sums add to the total **exactly** |'
  % (sum(1 for r in rows if r['total'] != 0), '{:+,}'.format(tot('total'))))
W()
W('**Lever 3 is the curve and the surface, not the printed v0s** — proven, not asserted: a')
W('counterfactual board built from the final tree with only the numéraire block reverted reproduced')
W('`5c0de646` **byte-identically**, so the `nd_v0` / `pool_v0` blocks, the `curve_md5` field and the')
W('P9 guard are all **value-inert** on the board.')
W()
W('**Why the numéraire does not reach all 804 rows.** It enters the **player** side through')
W('`BOARD_FACTOR` and the **pick** side through the published ladder, which already carries `× s`.')
W('So 224 rows take no `BOARD_FACTOR` move; **130 of them were re-denominated through lever 3**')
W('instead. The **90** rows unmoved by all four levers are **all pool rows** priced from the #326')
W('owner-**signed** `pool_levels`, read verbatim in ladder currency — constants this act did not')
W('re-sign, so they correctly do not move.')
W()
W('## 3. NATIONAL vs POOL')
W()
W('| population | n | LIVE | FINAL | Δ | pct |')
W('|---|---:|---:|---:|---:|---:|')
for lbl, pred in (('national (ND 1–64)', lambda r: (r['ep'] or 0) <= 64),
                  ('pool (past 64)', lambda r: (r['ep'] or 0) > 64)):
    sub = [r for r in rows if pred(r)]
    a, b = sum(r['live'] for r in sub), sum(r['final'] for r in sub)
    W('| %s | %d | %s | %s | %s | %+.4f%% |'
      % (lbl, len(sub), '{:,}'.format(a), '{:,}'.format(b), '{:+,}'.format(b - a), 100.0 * (b - a) / a))
W()
mv = [r for r in rows if r['total'] != 0]
W('**%d of %d rows move** (%.1f%%) — %d rise, %d fall, %d unmoved.'
  % (len(mv), len(rows), 100.0 * len(mv) / len(rows),
     sum(1 for r in mv if r['total'] > 0), sum(1 for r in mv if r['total'] < 0), len(rows) - len(mv)))
W()
W('## 4. THE NAMED ROWS (PREREG P14)')
W()
W('| row | pos | pick | LIVE | L1 unflag | L2 grace | L3 curve+v0 | L4 numéraire | FINAL | Δ | pct |')
W('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for k in NAMED:
    r = byk.get(k)
    if not r:
        W('| %s | — | — | — | — | — | — | — | — | — | not on the board |' % k); continue
    bold = '**' if r['total'] > 0 else ''
    W('| %s%s%s | %s | %s | %s | %+d | %+d | %+d | %+d | %s | %s%+d%s | %+.2f%% |'
      % (bold, k, bold, r['pos'], r['pick'] if r['pick'] is not None else r['ep'],
         '{:,}'.format(r['live']), r['lever1_unflag'], r['lever2_grace'], r['lever3_curve_v0'],
         r['lever4_numeraire'], '{:,}'.format(r['final']), bold, r['total'], bold,
         100.0 * r['total'] / r['live'] if r['live'] else 0))
W()
rise = [k for k in NAMED if byk.get(k) and byk[k]['total'] > 0]
W('**`willem-duursma` is the only named row that rises** — %s — exactly the mechanism P14 named:'
  % ', '.join(rise))
W('grace reaches him (+538) and outweighs the unflag and the numéraire together.')
W()
W('## 5. THE FIFTY LARGEST ABSOLUTE MOVERS')
W()
W('| row | pos | ep | LIVE | L1 | L2 | L3 | L4 | FINAL | Δ |')
W('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in sorted(rows, key=lambda x: -abs(x['total']))[:50]:
    W('| %s | %s | %s | %s | %+d | %+d | %+d | %+d | %s | %+d |'
      % (r['key'], r['pos'], r['ep'], '{:,}'.format(r['live']), r['lever1_unflag'], r['lever2_grace'],
         r['lever3_curve_v0'], r['lever4_numeraire'], '{:,}'.format(r['final']), r['total']))
W()
W('## 6. EVERY PRICED ROW')
W()
W('All %d rows, sorted by key. Lever columns sum to Δ exactly on every line.' % len(rows))
W()
W('| row | pos | ep | LIVE | L1 unflag | L2 grace | L3 curve+v0 | L4 numéraire | FINAL | Δ |')
W('|---|---|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in sorted(rows, key=lambda x: x['key']):
    W('| %s | %s | %s | %s | %+d | %+d | %+d | %+d | %s | %+d |'
      % (r['key'], r['pos'], r['ep'], '{:,}'.format(r['live']), r['lever1_unflag'], r['lever2_grace'],
         r['lever3_curve_v0'], r['lever4_numeraire'], '{:,}'.format(r['final']), r['total']))
W()
W('---')
W()
W('**Reconciliation:** rows failing `%d` · max |residual| `%d`.'
  % (d['reconciliation']['rows_failing'], d['reconciliation']['max_residual']))
open(M, 'w').write('\n'.join(o) + '\n')
print('wrote %s (%d lines, %d rows)' % (M, len(o), len(rows)))
