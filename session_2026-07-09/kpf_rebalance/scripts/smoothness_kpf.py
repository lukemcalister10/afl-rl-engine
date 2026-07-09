"""KPF REBALANCE smoothness — owner continuity law (no new cliffs; the declared evidence-axis dip
unchanged). One engine load (all-on candidate). Guard 5 on entry.
Axes exercised:
  (1) GAMES axis across the 12-bar (the new _kpf_LD qualifying bar): an established KPF's in-progress
      season swept g=0..18 at his own scoring rate — the T1/T2 demonstration coordinates move as the
      season qualifies; measure the max one-game value step.
  (2) DEMONSTRATION (dm) axis: sweep the in-progress season's avg so dm crosses the regime knots
      (start 8, kt saturation 24) and the eD split activates — measure max one-point-of-avg step.
  (3) EVIDENCE axis (declared dip): Duursma games 0..14 — must match the L1c declared shape (no new cliff).
Usage: smoothness_kpf.py <out.json>"""
import io, contextlib, json, os, sys
import numpy as np
HERE = '/home/user/afl-rl-engine'
sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('smoothness_kpf', store_path='/home/claude/rl_workspace/rl_after/rl_model_data.json')
out = sys.argv[1]
os.chdir('/home/claude/rl_workspace/rl_after')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']
res = {}

def evq(p):
    with contextlib.redirect_stdout(io.StringIO()):
        return g['ev'](p, 2026)

def sweep(key, field, values):
    p = next(x for x in MA.data if x.get('key') == key)
    row = next((x for x in p['scoring'] if x['year'] == 2026), None)
    if row is None:
        return None
    keep = row[field]
    vals = []
    try:
        for v in values:
            row[field] = v
            vals.append(evq(p))
    finally:
        row[field] = keep
    return vals

# (1) games axis across the 12-bar — established KPFs (one hot, one moderate)
for key in ('riley-thilthorpe', 'jake-waterman', 'mitch-georgiades'):
    vals = sweep(key, 'games', list(range(0, 19)))
    steps = [abs(vals[i + 1] - vals[i]) / max(vals[i], 1) for i in range(len(vals) - 1)]
    res[f'games_sweep/{key}'] = {'values': vals, 'max_step_pct': round(100 * max(steps), 2)}
    print(f'{key} games 0..18: {vals}')
    print(f'  max one-game step {100*max(steps):.1f}%')

# (2) dm axis: sweep 2026 avg 40..110 (crosses LD entry, gm start 8, kt sat 24, eD split)
for key in ('jake-waterman', 'charlie-curnow'):
    vals = sweep(key, 'avg', list(range(40, 111, 2)))
    steps = [abs(vals[i + 1] - vals[i]) / max(vals[i], 1) for i in range(len(vals) - 1)]
    res[f'avg_sweep/{key}'] = {'values': vals, 'max_step_pct_per_2pts': round(100 * max(steps), 2)}
    print(f'{key} avg 40..110 (step 2): max step {100*max(steps):.1f}% / 2 avg-pts')

# (3) declared evidence-axis dip (Duursma) — unchanged vs L1c
vals = sweep('willem-duursma', 'games', list(range(0, 15)))
steps = [abs(vals[i + 1] - vals[i]) / max(vals[i], 1) for i in range(len(vals) - 1)]
res['duursma_evidence_axis'] = {'values': vals, 'max_step_pct': round(100 * max(steps), 2)}
print(f'duursma games 0..14: {vals}  max one-game move {100*max(steps):.1f}%')
json.dump(res, open(out, 'w'), indent=1)
print('wrote', out)
