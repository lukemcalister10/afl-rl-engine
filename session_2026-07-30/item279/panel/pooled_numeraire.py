"""#279 — the RULED DESIGN: control fitter + POOLED NUMERAIRE pin policy.

OWNER RULING 2026-07-30:
  FITTER      = control (shipped kernel + local-linear boundary correction, exactly as built in the panel)
  PIN POLICY  = pooled numeraire, in principle:
                  plain PAVA at the head (NO pick-1 override; pick 2's measured excess POOLS, nothing
                  truncated) + strict descent, then ONE global factor s = 3000 / pooled-head applied to the
                  whole curve. pick 1 = 3000 is then published as a TRUE UNIT, not an override.

The old policy did `fit[0] = PIN1` — a hard SET that discarded whatever the head actually measured, then
forced pick 2 down below it. Under a fitter whose raw pick 2 exceeds raw pick 1 (which every panel arm
produced), that truncation threw away real measured mass at the very top of the board.

REPORTED HERE, exactly as commissioned: the factor s; which picks joined the head pool; the recovered
clipped mass; the pool / MSD / SSP levels under the design; and the confirmation-condition evidence —
head-anchor noise, pooled band vs raw pick 1, across the panel's fitters and folds.

alpha = 1 here. The player-side x s is STEP-4 PROPAGATION and is NOT touched.
"""
import os, sys, json, math, time, importlib.util, collections
import numpy as np
import harness_pvc as H

MATRIX, PANEL, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]


def load_fitter(name):
    p = os.path.join(PANEL, 'fitter_%s.py' % name)
    spec = importlib.util.spec_from_file_location('f_' + name, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def pava_blocks(vals, wts):
    """PAVA, returning the pooled value per position AND the block structure, so the head pool is visible."""
    n = len(vals)
    sv, sw, sn = [], [], []
    for j in range(n):
        cv, cw, cn = float(vals[j]), float(wts[j]), 1
        while sv and sv[-1] < cv - 1e-12:
            pv, pw_, pn = sv.pop(), sw.pop(), sn.pop()
            cv = (pv * pw_ + cv * cw) / (pw_ + cw); cw = pw_ + cw; cn = pn + cn
        sv.append(cv); sw.append(cw); sn.append(cn)
    out, blocks, i = [], [], 0
    for bv, bn in zip(sv, sn):
        out += [bv] * bn
        blocks.append(list(range(i + 1, i + bn + 1)))       # 1-indexed picks
        i += bn
    return np.array(out), blocks


EPS = 1e-3


def curve_old(raw, wts):
    """The SUPERSEDED policy: hard-set pick 1, then strict descent. Kept only for the comparison."""
    fit, _ = pava_blocks(raw, wts)
    fit = fit.copy(); fit[0] = H.PIN1
    for i in range(1, len(fit)):
        if fit[i] >= fit[i - 1] - EPS: fit[i] = fit[i - 1] - EPS
    ic = [int(round(x)) for x in fit]; ic[0] = H.PIN1
    forced = []
    for i in range(1, len(ic)):
        if ic[i] >= ic[i - 1]: forced.append(i + 1); ic[i] = ic[i - 1] - 1
    return ic, forced


def curve_pooled(raw, wts):
    """The RULED policy: plain PAVA (no override) + strict descent, then ONE global factor s."""
    fit, blocks = pava_blocks(raw, wts)
    fit = fit.copy()
    for i in range(1, len(fit)):
        if fit[i] >= fit[i - 1] - EPS: fit[i] = fit[i - 1] - EPS
    pooled_head = float(fit[0])
    s = H.PIN1 / pooled_head
    scaled = fit * s
    ic = [max(1, int(round(x))) for x in scaled]
    forced = []
    for i in range(1, len(ic)):
        if ic[i] >= ic[i - 1]: forced.append(i + 1); ic[i] = ic[i - 1] - 1
    head_pool = blocks[0]
    return ic, forced, s, pooled_head, head_pool, fit


t0 = time.time()
meta, ND = H.load_matrix(MATRIX)
rows, prov = H.structural_values(ND)
fa = H.folds(rows)
ctrl = load_fitter('control')
raw, wts, diag = ctrl.full_fit(rows)
raw = np.asarray(raw, float); wts = np.asarray(wts, float)

old_ic, old_forced = curve_old(raw, wts)
new_ic, new_forced, s, pooled_head, head_pool, fit_unscaled = curve_pooled(raw, wts)
t_build = time.time() - t0

# ---- recovered clipped mass: what the hard set threw away at the head ----
# old policy assigns PIN1 to pick 1 and forces every head-pool pick below it; the pooled policy keeps the
# PAVA-pooled level for the whole block. The clipped mass is the head-pool value the old policy discarded.
pooled_block_raw = [float(raw[k - 1]) for k in head_pool]
old_head_assigned = [old_ic[k - 1] for k in head_pool]
new_head_assigned = [new_ic[k - 1] for k in head_pool]
clipped = {
 'head_pool_picks': head_pool,
 'raw_at_head_pool': [round(x, 2) for x in pooled_block_raw],
 'pava_pooled_head_value_pre_scale': round(pooled_head, 2),
 'raw_pick1': round(float(raw[0]), 2),
 'pooled_head_minus_raw_pick1': round(pooled_head - float(raw[0]), 2),
 'old_policy_assigned_at_head_pool': old_head_assigned,
 'ruled_policy_assigned_at_head_pool': new_head_assigned,
 'RECOVERED_CLIPPED_MASS_pre_scale_units': round(
        sum(pooled_head - a for a in [H.PIN1, H.PIN1 - 1][:len(head_pool)]), 2),
 'clipped_per_pick_pre_scale': [round(pooled_head - a, 2)
                                for a in [H.PIN1, H.PIN1 - 1][:len(head_pool)]],
 'post_scale_head_assignment_is_unchanged': (old_head_assigned == new_head_assigned),
 'WHERE_THE_RECOVERY_SHOWS_UP': (
     'NOT as extra board units at the head — post-scale the head pool lands on the same integers either way. '
     'The old policy clipped %.2f pre-scale units off the pooled head block (PAVA measured %.2f there; the '
     'hard set wrote 3000 and 2999). The ruled policy honours that measurement and redefines the UNIT '
     'instead: dividing by pooled_head/3000 scales every pick BELOW the head down by %.2f%%. So the recovery '
     'is expressed as the rest of the ladder becoming cheaper RELATIVE to a correctly-measured head, not as '
     'the head becoming dearer. The ladder total falls accordingly.'
     % (sum(pooled_head - a for a in [H.PIN1, H.PIN1 - 1][:len(head_pool)]), pooled_head, 100 * (1 - s))),
 'note': ('the old policy hard-SET pick 1 to 3000 and forced the rest of the head pool strictly below it, '
          'discarding the excess PAVA had pooled there. The ruled policy keeps the pooled level and rescales '
          'the whole curve instead, so nothing at the head is truncated.')}

RES = {'status': 'the RULED design. alpha=1 here; the six-schedule alpha table is rebuilt separately.',
 'ruling': {'fitter': 'control (shipped kernel + local-linear boundary correction)',
            'pin_policy': 'POOLED NUMERAIRE — plain PAVA at the head, strict descent, one global factor s',
            'player_side_scaling': 'NOT APPLIED — the player-side x s is step-4 propagation work'},
 'build_seconds': round(t_build, 3),
 'basis': {'gamma': '1.0 VOR', 'basis': 'STRUCTURAL', 'class_cut': H.CLASS_CUT,
           'store_md5': meta['store_md5'], 'v0surf_sig': meta['v0surf_sig'][:12],
           'fallback_share_pct': prov['fallback_share_pct']},
 'THE_FACTOR_S': {'s': round(s, 6), 'pooled_head_pre_scale': round(pooled_head, 4),
                  'published_pick1': new_ic[0],
                  'reading': ('pick 1 = %d is now a TRUE UNIT: the curve is scaled so that the pooled head '
                              'measures 3000, rather than pick 1 being overwritten with 3000.' % new_ic[0])},
 'HEAD_POOL': clipped,
 'ladders': {'ruled_pooled_numeraire': new_ic, 'superseded_hard_set': old_ic},
 'ladder_totals': {'ruled': int(sum(new_ic)), 'superseded': int(sum(old_ic)),
                   'delta': int(sum(new_ic) - sum(old_ic)),
                   'pct': round(100.0 * (sum(new_ic) / sum(old_ic) - 1), 4)},
 'payloads': {'ruled': H.payload(new_ic), 'superseded': H.payload(old_ic)},
 'forced_descent': {'ruled': new_forced, 'superseded': old_forced,
                    'reading': 'the pooled policy needs fewer forced picks because it is not fighting an '
                               'override it just imposed'},
 'per_pick': {str(k): {'superseded': old_ic[k - 1], 'ruled': new_ic[k - 1],
                       'ratio': round(new_ic[k - 1] / old_ic[k - 1], 4)}
              for k in (1, 2, 3, 5, 10, 24, 32, 40, 50, 57, 64)}}

# ================= CONFIRMATION CONDITION: head-anchor noise =================
# Across every panel fitter and every fold: how noisy is the raw pick-1 anchor, versus the pooled head?
# If the pooled head is the more stable anchor, the pooled numeraire is the better-conditioned unit.
anchor = {'question': ('is the POOLED head a less noisy anchor than RAW PICK 1? This number decides at step 4 '
                       'whether the pooled numeraire stands or reverts on one word.'),
          'method': ('for each panel fitter and each of the 5 folds, refit on the 4/5 training rows and record '
                     '(a) raw pick 1 and (b) the PAVA-pooled head. Dispersion across folds is the anchor noise.'),
          'per_fitter': {}}
for name in ('control', 'loclin', 'powerspine', 'distfirst'):
    m = load_fitter(name)
    r1s, phs, pools = [], [], []
    for f in range(H.K_FOLDS):
        tr = [r for r in rows if fa[r['key']] != f]
        rw, wt, _d = m.full_fit(tr)
        rw = np.asarray(rw, float); wt = np.asarray(wt, float)
        fit, blocks = pava_blocks(rw, wt)
        fit = fit.copy()
        for i in range(1, len(fit)):
            if fit[i] >= fit[i - 1] - EPS: fit[i] = fit[i - 1] - EPS
        r1s.append(float(rw[0])); phs.append(float(fit[0])); pools.append(len(blocks[0]))
    r1 = np.array(r1s); ph = np.array(phs)
    anchor['per_fitter'][name] = {
        'raw_pick1_by_fold': [round(x, 2) for x in r1s],
        'pooled_head_by_fold': [round(x, 2) for x in phs],
        'head_pool_size_by_fold': pools,
        'raw_pick1_sd': round(float(r1.std(ddof=1)), 2),
        'pooled_head_sd': round(float(ph.std(ddof=1)), 2),
        'raw_pick1_cv_pct': round(100 * float(r1.std(ddof=1) / r1.mean()), 3),
        'pooled_head_cv_pct': round(100 * float(ph.std(ddof=1) / ph.mean()), 3),
        'noise_reduction_pct': round(100 * (1 - float(ph.std(ddof=1)) / float(r1.std(ddof=1))), 2)
                               if r1.std(ddof=1) > 0 else None,
        'pooled_band_vs_raw_pick1_mean_gap': round(float(ph.mean() - r1.mean()), 2)}
sds_r = [anchor['per_fitter'][n]['raw_pick1_sd'] for n in anchor['per_fitter']]
sds_p = [anchor['per_fitter'][n]['pooled_head_sd'] for n in anchor['per_fitter']]
anchor['ACROSS_ALL_FITTERS'] = {
    'mean_raw_pick1_sd': round(float(np.mean(sds_r)), 2),
    'mean_pooled_head_sd': round(float(np.mean(sds_p)), 2),
    'pooled_is_quieter_in_n_of_4': int(sum(1 for a, b in zip(sds_p, sds_r) if a < b)),
    'mean_noise_reduction_pct': round(float(np.mean([anchor['per_fitter'][n]['noise_reduction_pct']
                                                     for n in anchor['per_fitter']])), 2)}
RES['CONFIRMATION_CONDITION_head_anchor_noise'] = anchor

# ================= pool / MSD / SSP levels UNDER THE DESIGN =================
allrecs = json.load(open(MATRIX))['recs']
POOLROWS = [r for r in allrecs if bool(r.get('is_pool')) and H.YR_LO <= r['year'] <= H.CLASS_CUT]


def ctab(pop):
    S = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for r in pop:
        if not H.concluded(r): continue
        T = H.depth(r)
        if T <= 0: continue
        f = H.realised_full(r)
        for t in range(1, T + 1):
            e = S[(r['pos'], t)]; e[0] += f; e[1] += H.sofar(r, t); e[2] += 1
    return S


TAB = ctab(POOLROWS)


def lvl(pop):
    vals = []; c = collections.Counter()
    for r in pop:
        if H.concluded(r):
            c['concluded'] += 1; vals.append(H.realised_full(r)); continue
        T = H.depth(r)
        if T <= 0:
            c['fallback'] += 1; vals.append(float(r['v0'])); continue
        e = TAB.get((r['pos'], T))
        if e is None or e[2] < H.MIN_STRATUM or e[1] <= 0:
            c['fallback'] += 1; vals.append(float(r['v0'])); continue
        c['completed'] += 1
        vals.append(H.sofar(r, T) * ((e[0] / e[2]) / (e[1] / e[2])))
    v = np.array(vals, float); n = len(v)
    sd = float(v.std(ddof=1)); se = sd / math.sqrt(n)
    return {'n': n, 'level_unscaled': round(float(v.mean()), 1),
            'LEVEL_under_design_x_s': round(float(v.mean()) * s, 1),
            'median_unscaled': round(float(np.median(v)), 1),
            'ci95_under_design': [round((float(v.mean()) - 1.96 * se) * s, 1),
                                  round((float(v.mean()) + 1.96 * se) * s, 1)],
            'relative_se_pct': round(100 * se / float(v.mean()), 1) if v.mean() > 0 else None,
            'never_established_pct': round(100.0 * sum(1 for r in pop if H.never_established(r)) / n, 2),
            'fallback_share_pct': round(100.0 * c['fallback'] / n, 2), 'provenance': dict(c)}


RES['levels_under_the_design'] = {
 'note': ('the whole pick-side ladder is scaled by s, so the levels are reported x s to stay in the same '
          'currency as the curve. The unscaled figure is shown beside it.'),
 'scale_factor_applied': round(s, 6),
 'POOL': lvl(POOLROWS),
 'MSD': lvl([r for r in POOLROWS if r['type'] == 'MSD']),
 'SSP': lvl([r for r in POOLROWS if r['type'] == 'SSP']),
 'DENOMINATOR_WARNING': ('MSD and SSP rest on far fewer rows than the store-level stream counts of 106 and 52 '
                         '(those are all-2651-row counts). Under the ruled class cut they are much smaller and '
                         'the intervals are correspondingly wide. Read the interval, not the mean.')}

os.makedirs(OUTDIR, exist_ok=True)
p = os.path.join(OUTDIR, 'pooled_numeraire_279.json')
json.dump(RES, open(p, 'w'), indent=1, sort_keys=True)
open(p, 'a').write("\n")
print(json.dumps({k: RES[k] for k in ('THE_FACTOR_S', 'HEAD_POOL', 'ladder_totals', 'payloads',
                                      'forced_descent', 'build_seconds')}, indent=1, sort_keys=True))
print("\nCONFIRMATION CONDITION:", json.dumps(RES['CONFIRMATION_CONDITION_head_anchor_noise']['ACROSS_ALL_FITTERS'], indent=1))
for n, v in RES['CONFIRMATION_CONDITION_head_anchor_noise']['per_fitter'].items():
    print("  %-11s raw_pick1_sd %8.2f  pooled_head_sd %8.2f  noise_reduction %6.2f%%  pool_sizes %s"
          % (n, v['raw_pick1_sd'], v['pooled_head_sd'], v['noise_reduction_pct'], v['head_pool_size_by_fold']))
print("\nLEVELS UNDER THE DESIGN:")
for k in ('POOL', 'MSD', 'SSP'):
    v = RES['levels_under_the_design'][k]
    print("  %-5s n=%4d  level %8.1f  ci95 %s  median(unscaled) %6.1f  neverEst %5.2f%%  fallback %5.2f%%"
          % (k, v['n'], v['LEVEL_under_design_x_s'], v['ci95_under_design'], v['median_unscaled'],
             v['never_established_pct'], v['fallback_share_pct']))
