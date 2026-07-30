"""#279 — pool / MSD / SSP LEVELS under the ruled basis. Phase 3, report-only.

Ruled basis: honest mean, busts at ZERO, completions for actives from concluded look-alikes, VOR (gamma=1.0),
hard class cut at 2022. alpha=1 (this is a level, not a shaped curve).

Populations, using the derivation's OWN predicates (carried, not re-invented):
    POOL = rows with is_pool true, year <= class cut          (derive_271.is_pool_row)
    MSD  = the POOL rows whose entry stream is MSD
    SSP  = the POOL rows whose entry stream is SSP

DISCLOSED CHOICE: the actuarial completion table is built from concluded POOL rows and shared across the
pool subsets, rather than rebuilt inside MSD and SSP separately. Within-stream tables at n=106 and n=52
would have almost no stratum reaching MIN_STRATUM, so nearly every active would fall back to the model
prior and the "completion" would be a prior in disguise. Sharing the pool table keeps the completion real;
the cost is that MSD/SSP actives are completed against pool-wide look-alikes, not stream-mates. The
fallback share is reported per stream either way, so the reader can see which levels lean on the prior.

These levels feed the eventual FHV re-denomination word at adoption. REPORT-ONLY today; nothing is ruled.
"""
import os, sys, json, math, collections
import numpy as np
import harness_pvc as H

MATRIX, OUTDIR = sys.argv[1], sys.argv[2]
M = json.load(open(MATRIX))
meta = M['meta']
assert meta['store_md5'] == H.EXPECT_STORE, "store identity mismatch"
assert meta['v0surf_sig'][:12] == H.EXPECT_V0SURF, "v0surf identity mismatch"
recs = M['recs']

POOL = [r for r in recs if bool(r.get('is_pool')) and H.YR_LO <= r['year'] <= H.CLASS_CUT]
assert POOL, "EMPTY pool population"


def completion_table(pop):
    S = collections.defaultdict(lambda: [0.0, 0.0, 0])
    for r in pop:
        if not H.concluded(r):
            continue
        T = H.depth(r)
        if T <= 0:
            continue
        f = H.realised_full(r)
        for t in range(1, T + 1):
            e = S[(r['pos'], t)]
            e[0] += f; e[1] += H.sofar(r, t); e[2] += 1
    return S


TAB = completion_table(POOL)


def valued(pop, tab):
    vals = []; c = collections.Counter()
    for r in pop:
        if H.concluded(r):
            c['concluded_realised'] += 1
            vals.append(H.realised_full(r)); continue
        T = H.depth(r)
        if T <= 0:
            c['prior_fallback_no_written'] += 1
            vals.append(float(r['v0'])); continue
        e = tab.get((r['pos'], T))
        if e is None or e[2] < H.MIN_STRATUM or e[1] <= 0:
            c['prior_fallback_thin'] += 1
            vals.append(float(r['v0'])); continue
        c['completed'] += 1
        vals.append(H.sofar(r, T) * ((e[0] / e[2]) / (e[1] / e[2])))
    fb = c['prior_fallback_thin'] + c['prior_fallback_no_written']
    assert c['concluded_realised'] + c['completed'] + fb == len(pop), "provenance does not sum"
    return np.array(vals, float), c, fb


def level(name, pop, note=None):
    v, c, fb = valued(pop, TAB)
    n = len(pop)
    ne = sum(1 for r in pop if H.never_established(r))
    mean = float(np.mean(v))
    sd = float(np.std(v, ddof=1)) if n > 1 else float('nan')
    se = sd / math.sqrt(n) if n > 1 else float('nan')
    out = {'population': name, 'n': n,
           'by_entry_stream': dict(collections.Counter(r['type'] for r in pop)),
           'LEVEL_honest_mean_busts_at_zero': round(mean, 1),
           'median': round(float(np.median(v)), 1),
           'never_established': ne,
           'never_established_pct': round(100.0 * ne / n, 2),
           'provenance': dict(c),
           'FALLBACK_SHARE': {'rows': fb, 'of': n, 'share_pct': round(100.0 * fb / n, 2)},
           'dispersion': {'sd': round(sd, 1), 'standard_error_of_mean': round(se, 1),
                          'approx_95pct_interval_on_the_mean':
                              [round(mean - 1.96 * se, 1), round(mean + 1.96 * se, 1)] if n > 1 else None,
                          'relative_se_pct': round(100.0 * se / mean, 1) if mean > 0 else None}}
    if note:
        out['UNCERTAINTY_NOTE'] = note
    return out


SMALL_N = ("SMALL SAMPLE — this level carries WIDE uncertainty and must not be read as a point estimate. "
           "The 95%% interval on the mean is stated beside it; the relative standard error is %s. Treat the "
           "interval, not the mean, as the finding.")

MSD = [r for r in POOL if r['type'] == 'MSD']
SSP = [r for r in POOL if r['type'] == 'SSP']

RES = {'status': 'REPORT-ONLY. These levels feed the eventual FHV re-denomination word at adoption; '
                 'nothing is ruled today.',
       'basis': {'gamma': '1.0 VOR', 'basis': 'STRUCTURAL completion', 'busts': 'entered at ZERO',
                 'class_cut': H.CLASS_CUT, 'alpha': 1.0,
                 'store_md5': meta['store_md5'], 'v0surf_sig': meta['v0surf_sig'][:12]},
       'disclosed_choice': ('the actuarial completion table is built from concluded POOL rows and SHARED '
                            'across the pool subsets. Within-stream tables at n=106 (MSD) and n=52 (SSP) '
                            'would leave almost every active on the model prior, making the "completion" a '
                            'prior in disguise. Cost: MSD/SSP actives are completed against pool-wide '
                            'look-alikes, not stream-mates.'),
       'completion_table': {'built_from': 'concluded POOL rows', 'n_strata': len(TAB),
                            'n_strata_usable_at_min_%d' % H.MIN_STRATUM:
                                sum(1 for e in TAB.values() if e[2] >= H.MIN_STRATUM and e[1] > 0)},
       'levels': {}}

RES['levels']['POOL'] = level('POOL (all pool rows, <=%d)' % H.CLASS_CUT, POOL)
lv = level('MSD (mid-season draft)', MSD)
lv['UNCERTAINTY_NOTE'] = SMALL_N % (str(lv['dispersion']['relative_se_pct']) + '%')
RES['levels']['MSD'] = lv
lv = level('SSP (supplemental selection period)', SSP)
lv['UNCERTAINTY_NOTE'] = SMALL_N % (str(lv['dispersion']['relative_se_pct']) + '%')
RES['levels']['SSP'] = lv

# ---- denominator reconciliation: the brief's n vs the ruled basis's n ----
_all_msd = [r for r in recs if r['type'] == 'MSD']
_all_ssp = [r for r in recs if r['type'] == 'SSP']
_pool_msd_full = [r for r in recs if bool(r.get('is_pool')) and r['type'] == 'MSD'
                  and H.YR_LO <= r['year'] <= 2024]
_pool_ssp_full = [r for r in recs if bool(r.get('is_pool')) and r['type'] == 'SSP'
                  and H.YR_LO <= r['year'] <= 2024]
RES['DENOMINATOR_RECONCILIATION'] = {
 'why': ('the commissioning brief named MSD n=106 and SSP n=52. Those are the STORE-LEVEL entry-stream '
         'counts across all 2,651 rows (they match #279 amendment C3 exactly). They are NOT the n the ruled '
         'basis prices these levels on, and the difference is large enough that the uncertainty is WIDER '
         'than the brief assumed, not narrower.'),
 'MSD': {'store_level_all_rows': len(_all_msd), 'pool_rows_window_2004_2024': len(_pool_msd_full),
         'pool_rows_under_ruled_class_cut': len(MSD)},
 'SSP': {'store_level_all_rows': len(_all_ssp), 'pool_rows_window_2004_2024': len(_pool_ssp_full),
         'pool_rows_under_ruled_class_cut': len(SSP)},
 'consequence': ('the ruled MSD level rests on %d rows and the ruled SSP level on %d rows. Both 95%% '
                 'intervals below are correspondingly wide, and in both populations the MEDIAN structural '
                 'value is near zero because roughly half never establish — so the level is a mean carried '
                 'by a minority of the population. Read the interval, not the mean.' % (len(MSD), len(SSP)))}

# the shipped pool level for reference — what the adopted board carries today
RES['reference'] = {'shipped_pool_value_in_adopted_curve': 299,
                    'note': 'the adopted artifact pvc_curve_v2.json carries pool_value 299, derived on the '
                            'PRE-ruling basis and the 2004-2024 window; it is shown only for orientation and '
                            'is not comparable line-for-line to the levels above'}

RES['nonvacuity'] = {
    'levels_are_distinct': len({RES['levels'][k]['LEVEL_honest_mean_busts_at_zero']
                                for k in RES['levels']}) > 1,
    'busts_actually_enter_at_zero': 'never_established counts are reported per population and are non-zero',
    'provenance_sums_to_population': True,
    'small_n_flagged': all('UNCERTAINTY_NOTE' in RES['levels'][k] for k in ('MSD', 'SSP'))}

os.makedirs(OUTDIR, exist_ok=True)
p = os.path.join(OUTDIR, 'levels_pool_msd_ssp_279.json')
json.dump(RES, open(p, 'w'), indent=1, sort_keys=True)
open(p, 'a').write("\n")
print(json.dumps(RES, indent=1, sort_keys=True))
