"""#279 — the six-schedule alpha table REBUILT under the RULED DESIGN.

RULED: fitter = control (shipped kernel + local-linear boundary correction)
       pin    = POOLED NUMERAIRE (plain PAVA at the head, strict descent, one global factor s = 3000/pooled-head)

alpha stays PARKED at 1.0. This table is EVIDENCE ONLY; no ruling is implied.

HOW alpha IS APPLIED, and why this way. The control fitter is a kernel MEAN in the interior and a local-linear
WLS in the boundary zones. A CE formula written for a weighted mean cannot be dropped into the local-linear
half, and leaving the boundary zones alpha-invariant would be worst at exactly the tail where the dial matters
most. So alpha is applied at the ESTIMATOR level:

    raw_alpha(p) = [ control_fit( v^alpha ) ](p) ^ (1/alpha)

i.e. the certainty-equivalent of whatever the estimator computes. For the kernel half this reduces EXACTLY to
the engine's own _ce0 form, (sum W v^a / sum W)^(1/a), because the kernel is linear in the values. For the
local-linear half it is the natural generalisation of the same idea. At alpha=1 it returns the control fit
unchanged, which is the control on this harness.

Busts enter at v=0 and 0^alpha = 0 for alpha>0, so the _ce0 semantics (busts floored at 0, not 1) are preserved.
A local-linear fit on transformed values can go negative; those are clamped at 0 before the inverse power and
the count is REPORTED, never silent.

A NOTE ON s: under the pooled numeraire each alpha has its OWN s, because the pooled head moves with alpha.
The pick-class-vs-numeraire ratio sum(2..64)/pick1 is scale-INVARIANT, so s cancels there. Conservation is not
scale-invariant, so it is reported both as published and unit-adjusted; the unit-adjusted figure is the one
that answers "did the dial slash the pick class against mean production".
"""
import os, sys, json, math, time, csv, importlib.util, collections
import numpy as np
import harness_pvc as H

MATRIX, PANEL, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]
EPS = 1e-3


def load_fitter(name):
    p = os.path.join(PANEL, 'fitter_%s.py' % name)
    spec = importlib.util.spec_from_file_location('f_' + name, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def pava_blocks(vals, wts):
    n = len(vals); sv, sw, sn = [], [], []
    for j in range(n):
        cv, cw, cn = float(vals[j]), float(wts[j]), 1
        while sv and sv[-1] < cv - 1e-12:
            pv, pw_, pn = sv.pop(), sw.pop(), sn.pop()
            cv = (pv * pw_ + cv * cw) / (pw_ + cw); cw = pw_ + cw; cn = pn + cn
        sv.append(cv); sw.append(cw); sn.append(cn)
    out, blocks, i = [], [], 0
    for bv, bn in zip(sv, sn):
        out += [bv] * bn; blocks.append(list(range(i + 1, i + bn + 1))); i += bn
    return np.array(out), blocks


def pooled_numeraire(raw, wts):
    fit, blocks = pava_blocks(raw, wts); fit = fit.copy()
    for i in range(1, len(fit)):
        if fit[i] >= fit[i - 1] - EPS: fit[i] = fit[i - 1] - EPS
    pooled_head = float(fit[0]); s = H.PIN1 / pooled_head
    ic = [max(1, int(round(x * s))) for x in fit]
    forced = []
    for i in range(1, len(ic)):
        if ic[i] >= ic[i - 1]: forced.append(i + 1); ic[i] = ic[i - 1] - 1
    return ic, forced, s, pooled_head, blocks[0]


SCHED = collections.OrderedDict([
 ('a0.6_flat', (lambda k: 0.6, 'flat 0.6')),
 ('a0.8_flat', (lambda k: 0.8, 'flat 0.8')),
 ('a1.0_flat', (lambda k: 1.0, 'flat 1.0 — the ruled setting; returns the control fit unchanged')),
 ('tiered_0.6_to_0.8_by50', (lambda k: 0.6 + 0.2 * min(k - 1, 49) / 49.0,
                             "the engine's own _alpha_pvc: 0.6 at pick 1 -> 0.8 by pick 50, flat after")),
 ('lin_0.8_to_1.00_at64', (lambda k: 0.8 + 0.20 * (k - 1) / 63.0, 'linear 0.8 at pick 1 -> 1.00 at pick 64')),
 ('lin_0.9_to_1.05_at64', (lambda k: 0.9 + 0.15 * (k - 1) / 63.0,
                           'linear 0.9 -> 1.05; crosses 1.0, tail UPSIDE-weighted')),
])

t0 = time.time()
meta, ND = H.load_matrix(MATRIX)
rows, prov = H.structural_values(ND)
ctrl = load_fitter('control')

# alpha=1 reference: the honest mean production, from the control fit itself
raw1, wts1, _d1 = ctrl.full_fit(rows)
raw1 = np.asarray(raw1, float); wts1 = np.asarray(wts1, float)
honest_total = float(np.sum(raw1))
honest_tail = float(np.sum(raw1[1:]))
t_one = time.time() - t0

results = {}
ladders = collections.OrderedDict()
for name, (fn, desc) in SCHED.items():
    ts = time.time()
    if name == 'a1.0_flat':
        raw = raw1.copy(); wts = wts1.copy(); nneg = 0
    else:
        # transform values -> refit with the SAME control estimator -> invert, per pick's own alpha
        alphas = np.array([fn(p) for p in range(1, 65)], float)
        # one refit per DISTINCT alpha, then read each pick off its own fit
        raw = np.zeros(64); wts = np.zeros(64); nneg = 0
        for a in sorted(set(np.round(alphas, 10))):
            tr = [{**r, 'value': (max(r['value'], 0.0)) ** a} for r in rows]
            rr, ww, _ = ctrl.full_fit(tr)
            rr = np.asarray(rr, float); ww = np.asarray(ww, float)
            neg = int((rr < 0).sum()); nneg += neg
            rr = np.maximum(rr, 0.0) ** (1.0 / a)
            sel = np.isclose(alphas, a)
            raw[sel] = rr[sel]; wts[sel] = ww[sel]
    ic, forced, s, ph, head_pool = pooled_numeraire(raw, wts)
    ladders[name] = ic
    results[name] = {
        'description': desc,
        'alpha_at': {str(k): round(fn(k), 4) for k in (1, 2, 10, 24, 32, 40, 50, 57, 64)},
        'seconds': round(time.time() - ts, 3),
        'factor_s': round(s, 6), 'pooled_head_pre_scale': round(ph, 2), 'head_pool_picks': head_pool,
        'published_pick1': ic[0],
        'ladder_total': int(sum(ic)), 'ladder_2_to_64': int(sum(ic[1:])),
        'payload': H.payload(ic),
        'PICK_CLASS_vs_numeraire': round(sum(ic[1:]) / ic[0], 4),
        'CONSERVATION_published': round(sum(ic) / honest_total, 4),
        'CONSERVATION_unit_adjusted': round(sum(ic) / (s * honest_total), 4),
        'n_negative_clamped_before_inverse_power': nneg,
        'raw_monotone_violations': H.raw_monotone_violations(raw),
        'n_forced_descent': len(forced), 'forced_picks': forced,
        'curve': {str(k): ic[k - 1] for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)}}

a1 = results['a1.0_flat']
for n in results:
    results[n]['PICK_CLASS_vs_alpha1_pct'] = round(
        100 * (results[n]['PICK_CLASS_vs_numeraire'] / a1['PICK_CLASS_vs_numeraire'] - 1), 3)
    results[n]['vs_alpha1_by_pick'] = {str(k): round(ladders[n][k - 1] / ladders['a1.0_flat'][k - 1], 4)
                                       for k in (1, 3, 10, 24, 32, 40, 50, 57, 64)}

OUT = {'status': 'REPORT-ONLY. alpha stays PARKED at 1.0; no ruling is implied by this table.',
 'ruled_design': {'fitter': 'control (kernel + local-linear boundary correction)',
                  'pin_policy': 'pooled numeraire (plain PAVA head, strict descent, global factor s)',
                  'gamma': '1.0 VOR', 'basis': 'STRUCTURAL', 'class_cut': H.CLASS_CUT},
 'alpha_application': ('raw_alpha(p) = [control_fit(v^alpha)](p)^(1/alpha) — the certainty-equivalent of the '
                       'estimator, so the dial applies uniformly across BOTH halves of the control fitter. '
                       'Reduces exactly to the engine _ce0 form on the kernel half; alpha=1 returns the '
                       'control fit unchanged.'),
 'fallback_share_pct': prov['fallback_share_pct'],
 'conservation_yardstick': {'total_mean_production_1_64_control_alpha1': round(honest_total, 1),
   'published_vs_unit_adjusted': ('each alpha has its OWN s under the pooled numeraire, so the published '
       'ladder is in that alpha\'s unit. The unit-adjusted column divides it back out and is the figure that '
       'answers "did the dial slash the pick class against mean production". The pick-class-vs-numeraire '
       'ratio is scale-invariant, so s cancels there entirely.')},
 'control_alpha1_reproduces_ruled_pooled_curve': results['a1.0_flat']['payload'],
 'schedules': results,
 'nonvacuity': {'schedules_distinct': len({results[n]['payload'] for n in results}) == len(results),
                'upside_schedule_exceeds_alpha1_somewhere':
                    any(ladders['lin_0.9_to_1.05_at64'][k] > ladders['a1.0_flat'][k] for k in range(64)),
                's_varies_with_alpha': len({results[n]['factor_s'] for n in results}) > 1},
 'total_seconds': round(time.time() - t0, 2), 'first_fit_seconds': round(t_one, 3)}

os.makedirs(OUTDIR, exist_ok=True)
json.dump(OUT, open(os.path.join(OUTDIR, 'alpha_ruled_design_279.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(OUTDIR, 'alpha_ruled_design_279.json'), 'a').write("\n")
names = list(SCHED.keys())
with open(os.path.join(OUTDIR, 'alpha_ruled_ladders_279.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['pick'] + names + ['alpha_' + n for n in names])
    for k in range(1, 65):
        w.writerow([k] + [ladders[n][k - 1] for n in names] + [round(SCHED[n][0](k), 4) for n in names])
    w.writerow(['LADDER_TOTAL'] + [sum(ladders[n]) for n in names] + [''] * len(names))
    w.writerow(['FACTOR_S'] + [results[n]['factor_s'] for n in names] + [''] * len(names))
    w.writerow(['CONSERVATION_unit_adjusted'] + [results[n]['CONSERVATION_unit_adjusted'] for n in names] + [''] * len(names))
    w.writerow(['PICK_CLASS_vs_numeraire'] + [results[n]['PICK_CLASS_vs_numeraire'] for n in names] + [''] * len(names))
print(json.dumps({k: OUT[k] for k in ('nonvacuity', 'total_seconds', 'first_fit_seconds',
                                      'control_alpha1_reproduces_ruled_pooled_curve')}, indent=1))
print("\n%-24s %8s %9s %8s %11s %10s %9s %6s" % ('schedule', 's', 'pooled_hd', 'ladder', 'conserv_uadj',
                                                 'class/num', 'vs a1 %', 'clamp'))
for n in names:
    r = results[n]
    print("%-24s %8.5f %9.1f %8d %11.4f %10.4f %9.2f %6d"
          % (n, r['factor_s'], r['pooled_head_pre_scale'], r['ladder_total'], r['CONSERVATION_unit_adjusted'],
             r['PICK_CLASS_vs_numeraire'], r['PICK_CLASS_vs_alpha1_pct'], r['n_negative_clamped_before_inverse_power']))
