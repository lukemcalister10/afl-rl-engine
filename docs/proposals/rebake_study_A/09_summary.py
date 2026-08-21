"""SUMMARY TABLES — the measured comparison across designs (a)-(f), overall and per population,
pooled over the three held-out folds. Emits results_summary.json + printable tables.
"""
import json, os, collections
import numpy as np

S = os.environ['STUDY']
OUT = os.path.join(S, 'out')
H = json.load(open(os.path.join(OUT, 'candidates_holdout.json')))
SF = json.load(open(os.path.join(OUT, 'candidates_surface.json')))
ORDER = ['a_status_quo', 'b_mono', 'c_unified', 'c1_entryonly', 'd_weighted', 'e_heads', 'f_delete']
CLASSES = ['ND-early', 'ND-mid', 'ND-late', 'ND-pool', 'RD/PSD']
Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]

base = H['a_status_quo']['pooled']['pb_mean']
summary = {}
for nm in ORDER:
    p = H[nm]['pooled']
    s = SF[nm]
    row = dict(
        label=H[nm]['label'],
        pinball_mean=p['pb_mean'],
        pinball_vs_status_quo_pct=round(100.0 * (p['pb_mean'] - base) / base, 2),
        coverage_abs_err=p['cov_abs_err'],
        sort_repair_pct=round(float(np.mean([f['sort_repair_pct'] for f in H[nm]['folds']])), 2),
        ceil_repair_pct=round(float(np.mean([f['ceil_repair_pct'] for f in H[nm]['folds']])), 2),
        desc_step_pct=s['descending_step_pct'],
        rows_with_a_drop_pct=s['rows_with_a_descending_step_pct'],
        worst_fall_pct=s['worst_peak_to_trough_drop_pct'],
        steps_per_row=s['mean_distinct_steps_per_row'],
        by_class={})
    for c in CLASSES:
        k = 'pbc_' + c
        if k in p:
            row['by_class'][c] = dict(pinball=p[k], cov_abs_err=p.get('cvc_' + c))
    summary[nm] = row

# per-class relative to status quo
for c in CLASSES:
    b = summary['a_status_quo']['by_class'].get(c, {}).get('pinball')
    if b is None:
        continue
    for nm in ORDER:
        v = summary[nm]['by_class'].get(c)
        if v:
            v['vs_status_quo_pct'] = round(100.0 * (v['pinball'] - b) / b, 2)

json.dump(summary, open(os.path.join(OUT, 'results_summary.json'), 'w'), indent=1)

W = 30
print('=' * 132)
print('TABLE 1 — HELD-OUT ACCURACY AND SURFACE BEHAVIOUR  (3 rolling-origin folds, whole careers held out)')
print('=' * 132)
print('%-14s %9s %9s %9s | %9s %9s %9s %8s | %7s %7s' %
      ('design', 'pinball', 'vs (a)%', 'covErr', 'desc-step%', 'rows-drop%', 'worstfall%',
       'steps/row', 'sortfix%', 'ceilfix%'))
print('-' * 132)
for nm in ORDER:
    r = summary[nm]
    print('%-14s %9.4f %+9.2f %9.4f | %9.2f %10.1f %10.3f %8.0f | %7.1f %7.1f' %
          (nm, r['pinball_mean'], r['pinball_vs_status_quo_pct'], r['coverage_abs_err'],
           r['desc_step_pct'], r['rows_with_a_drop_pct'], r['worst_fall_pct'],
           r['steps_per_row'], r['sort_repair_pct'], r['ceil_repair_pct']))

print()
print('=' * 132)
print('TABLE 2 — PINBALL LOSS BY POPULATION (held-out, pooled over folds; lower is better; '
      'the %% is vs the status-quo refit)')
print('=' * 132)
hdr = '%-14s' % 'design'
for c in CLASSES:
    hdr += ' %18s' % c
print(hdr)
print('-' * 132)
for nm in ORDER:
    line = '%-14s' % nm
    for c in CLASSES:
        v = summary[nm]['by_class'].get(c)
        line += ' %10.4f %+6.1f%%' % (v['pinball'], v['vs_status_quo_pct']) if v else ' %18s' % '-'
    print(line)

print()
print('=' * 132)
print('TABLE 3 — COVERAGE ERROR BY POPULATION (mean |observed - nominal| across the six quantiles; '
      'lower is better)')
print('=' * 132)
print(hdr)
print('-' * 132)
for nm in ORDER:
    line = '%-14s' % nm
    for c in CLASSES:
        v = summary[nm]['by_class'].get(c)
        line += ' %18.4f' % v['cov_abs_err'] if v else ' %18s' % '-'
    print(line)

print()
print('=' * 132)
print('TABLE 4 — PER-FOLD PINBALL (is the ranking stable across time?)')
print('=' * 132)
print('%-14s %12s %12s %12s' % ('design', 'fold1 13-15', 'fold2 16-18', 'fold3 19-21'))
print('-' * 132)
for nm in ORDER:
    print('%-14s %12.4f %12.4f %12.4f' % (nm, *[f['pinball_mean'] for f in H[nm]['folds']]))
print()
print('wrote out/results_summary.json')
