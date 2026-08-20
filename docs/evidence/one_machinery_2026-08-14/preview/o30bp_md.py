#!/usr/bin/env python3
"""ORDER 30B-P — emit PREVIEW_MOVERS.md from PREVIEW_MOVERS.json. ALL 804 rows, no truncation,
sorted by |delta vs Step-2| descending. Pure formatter; it computes nothing."""
import json, sys, os

J = json.load(open(sys.argv[1])); OUT = sys.argv[2]
rows = J['rows']
POOL = {'MSD', 'SSP', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR'}
rows.sort(key=lambda r: (-abs(r['d_vs_step2']), r['key']))
mv = [r for r in rows if r['d_vs_step2'] != 0]
tot = J['totals']

def fmt(r):
    prov = ' *' if r['pool'] else ''
    return ('| `%s` | %s%s | %s | %s | %s | %s | %s | %s | %s | **%s** | %+d | %+.1f%% | %s | %s |'
            % (r['key'], (r['name'] or ''), prov, r['pathway'], r['pick'] if r['pick'] is not None else '—',
               r['pos'], r['age'], r['cg'], r['live'], r['step2'], r['preview'], r['d_vs_step2'],
               r['pct_vs_step2'] if r['pct_vs_step2'] is not None else 0.0,
               ('%.4f' % r['sigma']) if r['sigma'] is not None else 'day-0',
               ('%.0f' % r['v0_step1_board']) if r['v0_step1_board'] is not None else '—'))

L = []
L.append('# PREVIEW MOVERS — ALL 804 ROWS · ORDER 30B-P STEP-3 PREVIEW BOARD')
L.append('')
L.append('> **NOTHING IS GREENLIT.** The Step-3 forbidden-set boundary word is still **OPEN**. This board is')
L.append('> produced behind the declared default-off dial `RL_O30B_PREVIEW`; with the dial off the committed')
L.append('> Step-2 board `9298203135202a0c707bb0977ba38c31` reproduces **BYTE-EXACT**.')
L.append('>')
L.append('> **THE PREVIEW IS PRE-NUMERAIRE.** Step 6\'s re-pin has **not** run. Every price in this table is')
L.append('> in the current numéraire and will move again when the re-pin happens. **Do not read levels across')
L.append('> this boundary; read the movement.**')
L.append('>')
L.append('> **Pool rows are marked `*` and are PROVISIONAL — pool values pending Step 4.** They are priced')
L.append('> under the *same* formula with their *own* signed pool `v0` cells; their pathway-specific')
L.append('> derivations (and the pool fade) are Step 4\'s work and have not run.')
L.append('')
L.append('| | |')
L.append('|---|---|')
L.append('| live board (main) | `88ce647f531030d8d2e094188b258191` — total **%d** |' % tot['live'])
L.append('| Step-2 provisional | `9298203135202a0c707bb0977ba38c31` — total **%d** |' % tot['step2'])
L.append('| **PREVIEW** | **`6a392bca7ad0dee04a6b4f037c758f65`** — total **%d** (%+d vs Step-2, %+.4f%%) |'
         % (tot['preview'], tot['delta'], 100.0 * tot['delta'] / tot['step2']))
L.append('| movers vs Step-2 | **%d of %d** · the 89 day-0 rows move **zero** |' % (len(mv), len(rows)))
L.append('| σ | `exp(-(g/%.4g)^%.4g)` — the 30B-M refit of ruling 4\'s form to the five measured band midpoints |'
         % (J['sigma']['tau'], J['sigma']['beta']))
L.append('| pedigree leg | the **STEP-1 positional v0** (pool: the signed pool cell) × %.4f (BOARD→ENGINE) |'
         % J['numeraire_factor'])
L.append('| re-referenced denominators | the effective positional bars: %s |'
         % ' · '.join('%s %.1f' % (k, v) for k, v in sorted(J['bars'].items())))
L.append('')
L.append('**Columns.** `LIVE` = today\'s board `88ce647f`. `STEP-2` = the last provisional board `92982031`.')
L.append('`PREVIEW` = this board. `Δ` and `%` are **against Step-2**, as the brief asks. `σ` is the pedigree')
L.append('**weight** this row carries (`day-0` = the row never enters the blend and keeps the Step-2 fade).')
L.append('`v0` is the Step-1 positional v0 in board points — the object the pedigree leg is made of.')
L.append('')
L.append('| key | name | path | pick | pos | age | games | LIVE | STEP-2 | PREVIEW | Δ vs S2 | % vs S2 | σ | v0 |')
L.append('|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
for r in rows: L.append(fmt(r))
L.append('')
L.append('`*` provisional — pool values pending Step 4.')
L.append('')
L.append('*Machine-readable, with σ, the fade clock, the sat-counterfactual and the recovered production leg')
L.append('for every row: `PREVIEW_MOVERS.json`.*')
open(OUT, 'w').write('\n'.join(L) + '\n')
print('wrote %s (%d rows, %d movers)' % (OUT, len(rows), len(mv)))
