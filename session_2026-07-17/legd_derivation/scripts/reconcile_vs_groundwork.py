"""RECONCILE — my re-emitted evidence (base 33c8b52 / store 968de0c7) vs the groundwork's committed
artifacts (base 6306378 / store 0efdc5d6, @9845180). Emits a machine diff of every headline numeric
field. Differences are FINDINGS, not problems (directive ACT-1.1 + groundwork header: provisional).
Reads the groundwork JSONs straight out of git (git show 9845180:...), never from a working copy.
"""
import json, subprocess
BASE = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation'
GW = 'session_2026-07-17/legd_groundwork'

def gw(path):
    return json.loads(subprocess.check_output(['git', 'show', f'9845180:{GW}/{path}'],
                                              cwd='/home/user/afl-rl-engine'))
def mine(path):
    return json.load(open(f'{BASE}/{path}'))

diffs = []
def cmp(label, a, b):
    same = (a == b)
    diffs.append(dict(field=label, groundwork=a, rederivation=b, match=same))
    return same

# --- Job 2 circularity ---
g2, m2 = gw('out/job2_circularity.json'), mine('out/job2_circularity.json')
cmp('job2.pool.all_incurve', g2['pool_sizes']['all_incurve'], m2['pool_sizes']['all_incurve'])
cmp('job2.pool.ND', g2['pool_sizes']['ND'], m2['pool_sizes']['ND'])
cmp('job2.pool.RD', g2['pool_sizes']['RD'], m2['pool_sizes']['RD'])
cmp('job2.pure_V0_pole_total', g2['totals_all']['ge90_pureV0pole'], m2['totals_all']['ge90_pureV0pole'])
cmp('job2.ge75_total', g2['totals_all']['ge75'], m2['totals_all']['ge75'])
cmp('job2.ge50_total', g2['totals_all']['ge50'], m2['totals_all']['ge50'])
cmp('job2.cutA_n_excluded', g2['cut_options']['A_delete_circle_at_entry']['n_excluded'],
    m2['cut_options']['A_delete_circle_at_entry']['n_excluded'])
cmp('job2.cutB_n_kept', g2['cut_options']['B_honest_calibration_end_yr4']['n_kept'],
    m2['cut_options']['B_honest_calibration_end_yr4']['n_kept'])
cmp('job2.band_table_all', g2['band_table_all'], m2['band_table_all'])

# --- Job 3 survivorship ---
g3, m3 = gw('out/job3_survivorship.json'), mine('out/job3_survivorship.json')
cmp('job3.exit_table_2004_2018', g3['exit_table_2004_2018'], m3['exit_table_2004_2018'])
cmp('job3.convex_gap_2004_2018', g3['convex_gap_2004_2018'], m3['convex_gap_2004_2018'])

# --- Job 4a national last pick ---
g4a, m4a = gw('out/job4a_national_last_pick.json'), mine('out/job4a_national_last_pick.json')
cmp('job4a.n_mismatch_vs_store_max', g4a['n_mismatch_vs_store_max'], m4a['n_mismatch_vs_store_max'])
cmp('job4a.years_with_gaps', g4a['years_with_gaps'], m4a['years_with_gaps'])
cmp('job4a.rows', g4a['rows'], m4a['rows'])

# --- Job 4b/4c pickless + counts ---
g4b, m4b = gw('out/job4b_pickless_eff.json'), mine('out/job4b_pickless_eff.json')
cmp('job4b.PICKEQ', g4b.get('PICKEQ'), m4b.get('PICKEQ'))
cmp('job4b.n_pickless_flex_touched', g4b['flex_sensitivity']['n_pickless_flex_touched'],
    m4b['flex_sensitivity']['n_pickless_flex_touched'])
g4c, m4c = gw('out/job4c_sample_counts.json'), mine('out/job4c_sample_counts.json')
cmp('job4c.pool_n', g4c['pool_n'], m4c['pool_n'])
cmp('job4c.per_pick_raw', g4c['per_pick_raw'], m4c['per_pick_raw'])
cmp('job4c.band_counts', g4c['band_counts_presentation_only'], m4c['band_counts_presentation_only'])

# --- Job 5 selftest (shipped curve strict descent) ---
g5, m5 = gw('out/job5_selftest_result.json'), mine('out/job5_selftest_result.json')
cmp('job5.strict_descent.n_violations', g5['strict_descent']['n_violations'],
    m5['strict_descent']['n_violations'])
cmp('job5.strict_descent.violations', g5['strict_descent']['violations'],
    m5['strict_descent']['violations'])

n_match = sum(1 for d in diffs if d['match'])
n_diff = len(diffs) - n_match
out = dict(
    _doc="Reconciliation: re-emitted evidence on base 33c8b52/store 968de0c7 vs groundwork @9845180 "
         "(base 6306378/store 0efdc5d6). Differences are FINDINGS, not problems.",
    base_mine=dict(head='33c8b52', store_md5='968de0c7'),
    base_groundwork=dict(head='6306378', store_md5='0efdc5d6'),
    n_fields=len(diffs), n_match=n_match, n_diff=n_diff,
    all_headline_numbers_identical=(n_diff == 0),
    fields=diffs,
)
json.dump(out, open(f'{BASE}/out/reconcile_vs_groundwork.json', 'w'), indent=1)
print(f"reconcile: {n_match}/{len(diffs)} headline fields identical; {n_diff} differ")
for d in diffs:
    if not d['match']:
        print(f"  DIFF {d['field']}: groundwork={d['groundwork']}  rederivation={d['rederivation']}")
if n_diff == 0:
    print("ALL headline evidence numbers identical across the base change (968de0c7 vs 0efdc5d6).")
print("wrote out/reconcile_vs_groundwork.json")
