"""L1c TASK 4 assembly + G-ATTR — all from committed books (each book's `cur` column IS the 2026
board-path value at that w; the engine is exec-once-per-process, so book-reads beat re-execs and are
byte-consistent with the committed artifacts). Writes W_TABLE.md (the owner artifact) + attr_young_loo.json."""
import json, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-08/l1c_rectification/out'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('assemble_wtable', store_path=f'{HERE}/engine/rl_after/rl_model_data.json')

def curmap(path):
    return {v['key']: v['cur'] for v in json.load(open(path)).values() if v.get('key') and v.get('cur') is not None}

books = {w: curmap(f'{OUT}/s4_matrix_w{w}.json') for w in ('05', '07', '085', '10')}
off = curmap(f'{OUT}/s4_matrix_youngoff.json')
baked = {r['key']: r['v'] for r in json.load(open(f'{HERE}/session_2026-07-06/w4_integration/out/baked_board_full.json'))['active']}
pre = {r['key']: r['v'] for r in json.load(open(f'{HERE}/data/rl_build/rl_app_data.json'))['active']}
ratios = {w: json.load(open(f'{OUT}/ratio_l1c_w{w}{"_SHIPPED" if w=="07" else ""}.json')) for w in ('05', '07', '085', '10')}

NAMES = [('willem-duursma', 'Willem Duursma', 'A-DUUR young gun · 2025 pk1 MID · 12g'),
         ('sam-lalor', 'Sam Lalor', 'top-3 pick · 2024 pk1 · 18g'),
         ('errol-gulden', 'Errol Gulden', 'Gulden shape: mid-pick instant producer · 2020 pk34 · 105g'),
         ('sam-darcy', 'Sam Darcy', 'Darcy shape: young KPF ceiling · 2021 pk2 · 51g'),
         ('taylor-goad', 'Taylor Goad', 'Goad shape: sat-out young ruck · 2023 pk20 · 1g'),
         ('dylan-patterson', 'Dylan Patterson', 'pure sit-out · 2025 pk5 · 0 games'),
         ('riley-bice', 'Riley Bice', 'mature-age pick · 2024 pk41 · draft-age 24 · 30g')]

L = []
L.append('# L1c OWNER W-TABLE — w = fraction of the measured cell re-rating paid forward (RL_YCRED_W)')
L.append('## 2026-07-08 · grid {0.5, 0.7, 0.85, 1.0} (owner-amended, matches the investigation simulation) · shipped default = 0.7 (NOT a ruling — the owner rules w on sight)')
L.append('')
L.append('## Per-year G-COHORT landing (conforming measure: class-year SUMS averaged across classes 2004-2020; EACH of y4/5/6 vs min(y1,y2); walk-forward book)')
L.append('| config | y1 figure | y2 figure | y4/den | y5/den | y6/den | verdict (hard <=130, guide 120-125) |')
L.append('|---|---|---|---|---|---|---|')
L.append('| W4 pre-L1c (old runway credit, audited) | 57,558.5 | 70,211.0 | 142.4% | 140.8% | 131.7% | BREACH (owner-upheld) |')
L.append('| credit-off basis (RL_YOUNG=0) | 55,603 | 67,976 | — | — | — | derivation basis |')
for w, lab in (('05', 'w=0.5'), ('07', '**w=0.7 (shipped)**'), ('085', 'w=0.85'), ('10', 'w=1.0')):
    r = ratios[w]; f = r['figures']; rt = r['ratios_y456']
    verdict = 'PASS' if r['gcohort_pass'] else 'BREACH'
    L.append(f"| {lab} | {f['1']:,.1f} | {f['2']:,.1f} | {rt['4']:.1f}% | {rt['5']:.1f}% | {rt['6']:.1f}% | {verdict} (worst {r['worst']:.1f}%) |")
L.append('')
L.append('SIM-vs-BUILT NOTE (owner amendment asked this table to carry the simulated landings): the investigation ')
L.append('grid simulated **0.85 -> ~120.0 (guide floor)** and **1.0 -> ~116.7 (below guide)**. The BUILT engine lands ')
L.append('0.85 -> worst 129.4% (y4) and 1.0 -> worst 126.9% (y4) — the simulated values match the built **y6** almost ')
L.append('exactly (119.7 / 117.1) but not the binding y4. Mechanism of the gap, in order of size: (i) the credit is ')
L.append('EVIDENCE-FADED at the y1 anchor (a played year-1 player has ~half his phi burnt by the end-of-y1 anchor; the ')
L.append('simulation paid full credit to the whole y1 sum), (ii) played-cell re-ratings are much smaller than sat-cell ')
L.append('ones and the blend s(g) moves players onto the played curve within 6 games, (iii) the TRAILING (leak-free) ')
L.append('table gives classes 2004-05 zero credit and 2006-08 thin-window credit, dragging the 17-class average, ')
L.append('(iv) negative-measured cells are clipped to zero, and capped rucks keep the RUC prior cap. These are the ')
L.append("directive's own constraints (evidence-keyed fade, trailing leak-free, clip>=0, cap out of scope) — reported ")
L.append('as built, not re-tuned.')
L.append('')
L.append('## Named players (2026 board values; before = baked v2.5 and the W4 pre-L1c candidate)')
L.append('| player | baked v2.5 | W4 pre-L1c | credit-off | w=0.5 | w=0.7 | w=0.85 | w=1.0 | shape |')
L.append('|---|---|---|---|---|---|---|---|---|')
rows_json = {}
for k, nm, note in NAMES:
    vals = [baked.get(k), pre.get(k), off.get(k)] + [books[w].get(k) for w in ('05', '07', '085', '10')]
    rows_json[k] = dict(zip(['baked', 'preL1c', 'off', 'w05', 'w07', 'w085', 'w10'], vals), note=note)
    L.append('| ' + nm + ' | ' + ' | '.join(str(v) if v is not None else '—' for v in vals) + f' | {note} |')
L.append('')
# G-ATTR leave-one-out from books: w07 (all-on) vs credit-off (RL_YOUNG=0, all else on)
keys = set(books['07']) & set(off)
deltas = {k: books['07'][k] - off[k] for k in keys if books['07'][k] != off[k]}
tot_on = sum(books['07'][k] for k in keys); tot_off = sum(off[k] for k in keys)
neg = {k: d for k, d in deltas.items() if d < 0}
top = sorted(deltas.items(), key=lambda t: -t[1])[:10]
L.append('## G-ATTR — RL_YOUNG leave-one-out at w=0.7 (book `cur` columns, all-on vs credit-off)')
L.append(f'- players compared: {len(keys)} · movers: {len(deltas)} · pool delta: +{tot_on-tot_off:,.0f} SCAR = {100*(tot_on/tot_off-1):+.2f}% of the credit-off board')
L.append(f'- negative movers: {len(neg)}' + (f' — {sorted(neg.items(), key=lambda t: t[1])[:5]} (investigate)' if neg else ' (credit clipped >=0 by construction)'))
L.append(f'- top recipients: ' + ', '.join(f'{k} +{d}' for k, d in top))
L.append('')
L.append('## A-DUUR direction')
d = rows_json['willem-duursma']
L.append(f"- Duursma baked {d['baked']} -> shipped w=0.7 {d['w07']} ({100*(d['w07']/d['baked']-1):+.1f}%); "
         f"credit-off {d['off']} -> w=0.7 {d['w07']} — direction UP: {'PASS' if d['w07'] > max(d['off'], d['baked']) else 'CHECK'}")
open(f'{OUT}/W_TABLE.md', 'w').write('\n'.join(L) + '\n')
json.dump({'named': rows_json, 'attr': {'n': len(keys), 'movers': len(deltas), 'pool_pct': 100*(tot_on/tot_off-1),
           'negative_movers': len(neg), 'deltas': deltas}}, open(f'{OUT}/attr_young_loo.json', 'w'))
print('\n'.join(L))
