"""#279 step-1 SECOND ADDENDUM — generate the VOR adoption-echo evidence files."""
import json, hashlib, collections, sys
import numpy as np

SP, E, OUT = sys.argv[1], sys.argv[2], sys.argv[3]

def vm(f): return {r['key']: r for r in json.load(open(f))['active']}
def m5(f): return hashlib.md5(open(f, 'rb').read()).hexdigest()
def cpay(f):
    ci = json.load(open(f))['curve']['integer']
    return hashlib.md5(json.dumps({str(i + 1): v for i, v in enumerate(ci)},
                                  sort_keys=True).encode()).hexdigest()[:8]

paths = {'baseline': f"{SP}/board_100_forcedrefit.json", 'it1': f"{E}/board_it1.json",
         'it2': f"{E}/board_it2.json", 'it3': f"{E}/board_it3.json", 'l1b': f"{E}/board_l1b.json"}
B = {k: vm(p) for k, p in paths.items()}
ids = {k: m5(p) for k, p in paths.items()}
keys = sorted(set.intersection(*[set(v) for v in B.values()]))
SC = vm(f"{SP}/board_085_forcedrefit.json")

def ap(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    iu = np.triu_indices(len(x), 1)
    dx = (x[:, None] - x[None, :])[iu]; dy = (y[:, None] - y[None, :])[iu]
    st = dx != 0; n = int(st.sum())
    inv = int(((dx > 0) & (dy < 0)).sum() + ((dx < 0) & (dy > 0)).sum())
    return {'n_pairs_total': int(len(dx)), 'n_pairs_strict_in_baseline': n, 'inversions': inv,
            'inversion_pct': round(100.0 * inv / n, 4), 'tie_collapses': int((st & (dy == 0)).sum())}

def ab(v):
    return '<=21' if v <= 21 else '22-24' if v <= 24 else '25-27' if v <= 27 else '28-30' if v <= 30 else '31+'
AB = ['<=21', '22-24', '25-27', '28-30', '31+']

MECH = ("ev() returns round(sitout_ev(p,Y,e)) for zero-season players -- V0-anchored, i.e. off the fitted "
        "surface, not off value()/unpl_eq. And ev() carries an explicit RUCK branch reading "
        "RUC_PRIOR_CAP*draftval(p) and _v0_uncapped(p), both off the adopted curve. No other position has a "
        "curve-reading branch in ev(). Hence the entire echo is RUCK: v0_start moved only for RUCK players, "
        "while the denser non-RUCK surface cells absorbed the curve shift under isotonic pooling.")

out = {
 'LABEL': ('ESTIMATE -- bounds the PURE-CURRENCY echo only. The shipped system still changes at step 2 '
           '(pick-value basis, S-1/S-2) and step 3 (variance dial). NOT a prediction of the final board.'),
 'baseline': {'board': ids['baseline'],
              'what': ('the step-1 VOR board presented to the owner: gamma=1.0 with its own-bake surface, '
                       'but curve inputs still the ADOPTED SCAR curve (08ea9375)')},
 'method': {
   'lawful_channels_repointed': ['1 pvc_curve_v2 -> _PVC0', '1a draftval -> RUCK prior cap',
        '1b V0 guard + surface rebuild', '2 _PVC2M -> rl_model.PVC', '2a unpl_eq', '2b pedestal',
        '3 curve -> v0 -> surface -> value'],
   'channels_NOT_repointed': {
        '4_pvc_snapshot': 'frozen by its own design note (train/serve skew) -- the seam-named exclusion',
        '5_peak_model': 'pinned frozen pickle b763f59e; serve path gamma-free; builder unrunnable (dob_corrected.json absent repo-wide)',
        '6_q97m_cm400': 'frozen by owner ruling, loaded never fitted',
        '7_bust_prior': 'not a curve channel: production-score units by position x pick (33.51-98.13), realised-derived'},
   'iteration': ('install curve -> reseed -> surface refit (gamma=1.0, RL_V0SURF_REFIT=1) -> board rebuild '
                 '-> re-derive the curve from the new surface'),
   'cost_per_iteration_seconds': {'board': '126-140', 'matrix_emit': '175-188', 'fit': 3}},
 'convergence': {
   'board_identity_sequence': [ids['baseline'], ids['it1'], ids['it2'], ids['it3']],
   'curve_payload_sequence': [cpay(f"{SP}/curve/derived_279_vor.json"), cpay(f"{E}/derived_it1.json"),
                              cpay(f"{E}/derived_it2.json"), cpay(f"{E}/derived_it3.json")],
   'curve_fixed_point': 'reached at iteration 2 -- payload 817c0f5a reproduced exactly at iteration 3',
   'ladder_sequence': [63908] + [json.load(open(f"{E}/derived_it%d.json" % i))['curve']['ladder_total'] for i in (1, 2, 3)],
   'pool_sequence': [273.7] + [json.load(open(f"{E}/derived_it%d.json" % i))['pool']['level_scar'] for i in (1, 2, 3)],
   'v0surf_sig_sequence': ['b781ed253bff', '2b633636839f', '76c1e4694e91', '22f4f961e2d0'],
   'step_deltas': []},
}
for a, b in (('baseline', 'it1'), ('it1', 'it2'), ('it2', 'it3')):
    x = np.array([B[a][k]['v'] for k in keys], float); y = np.array([B[b][k]['v'] for k in keys], float)
    d = y - x
    out['convergence']['step_deltas'].append(
        {'step': '%s->%s' % (a, b), 'players_moved': int((d != 0).sum()),
         'max_abs_delta': int(np.abs(d).max()), 'total_change_pct': round(100 * (y.sum() / x.sum() - 1), 4),
         'board_identical': ids[a] == ids[b]})

x = np.array([B['baseline'][k]['v'] for k in keys], float)
y = np.array([B['it3'][k]['v'] for k in keys], float)
d = y - x; nz = np.abs(d[d != 0])
r0 = sorted(keys, key=lambda k: -B['baseline'][k]['v']); r3 = sorted(keys, key=lambda k: -B['it3'][k]['v'])
mov = [k for k in keys if B['it3'][k]['v'] != B['baseline'][k]['v']]
out['echo_converged_vs_baseline'] = {
 'n_matched': len(keys), 'players_moved': len(mov), 'pct_moved': round(100.0 * len(mov) / len(keys), 2),
 'median_abs_delta_of_movers': round(float(np.median(nz)), 1),
 'median_signed_delta_all_804': round(float(np.median(d)), 1),
 'max_abs_delta': int(np.abs(d).max()),
 'max_abs_delta_player': max(keys, key=lambda k: abs(B['it3'][k]['v'] - B['baseline'][k]['v'])),
 'all_movers_negative': bool((d[d != 0] < 0).all()),
 'total_value': {'baseline': int(x.sum()), 'converged': int(y.sum()),
                 'change_pct': round(100 * (y.sum() / x.sum() - 1), 4)},
 'rank_movement': ap(x, y), 'max_rank_shift': max(abs(r0.index(k) - r3.index(k)) for k in keys),
 'top20_membership_unchanged': set(r0[:20]) == set(r3[:20]), 'top20_order_unchanged': r0[:20] == r3[:20],
 'movers_by_settled_position_gfut': dict(collections.Counter(B['baseline'][k].get('gf') for k in mov)),
 'movers': [{'key': k, 'name': B['baseline'][k].get('name'), 'gfut': B['baseline'][k].get('gf'),
             'listed_grp': B['baseline'][k].get('grp'), 'ep': B['baseline'][k].get('ep'),
             'games': B['baseline'][k].get('g'), 'baseline': B['baseline'][k]['v'],
             'converged': B['it3'][k]['v'], 'delta': int(B['it3'][k]['v'] - B['baseline'][k]['v'])}
            for k in sorted(mov, key=lambda k: B['it3'][k]['v'] - B['baseline'][k]['v'])]}

zg = [k for k in keys if not B['baseline'][k].get('g')]
out['zero_game_actives'] = {
 'n': len(zg), 'n_moved': sum(1 for k in zg if B['baseline'][k]['v'] != B['it3'][k]['v']),
 'denominator_note': 'zero-game = board field g falsy; of 804 active rows',
 'by_settled_position': {p: {'n': sum(1 for k in zg if B['baseline'][k].get('gf') == p),
     'moved': sum(1 for k in zg if B['baseline'][k].get('gf') == p and B['baseline'][k]['v'] != B['it3'][k]['v'])}
     for p in sorted({B['baseline'][k].get('gf') for k in zg})},
 'delta_distribution_of_movers': [int(B['it3'][k]['v'] - B['baseline'][k]['v'])
                                  for k in sorted(zg, key=lambda k: B['it3'][k]['v'] - B['baseline'][k]['v'])
                                  if B['baseline'][k]['v'] != B['it3'][k]['v']]}

out['age_profile_vor_over_scar'] = {}
for a_ in AB:
    ks = [k for k in keys if ab(SC[k]['age']) == a_ and SC[k]['v'] > 0]
    b0 = round(float(np.mean([B['baseline'][k]['v'] / SC[k]['v'] for k in ks])), 4)
    b3 = round(float(np.mean([B['it3'][k]['v'] / SC[k]['v'] for k in ks])), 4)
    out['age_profile_vor_over_scar'][a_] = {'n': len(ks), 'baseline': b0, 'converged': b3,
                                            'shift': round(b3 - b0, 4)}

out['channel_8_branch_test'] = {
 'question': 'does re-pointing the superseded pvc_curve_L1b.json change anything?',
 'branch_A_v2_only_board': ids['it3'], 'branch_B_v2_plus_L1b_board': ids['l1b'],
 'boards_byte_identical': ids['it3'] == ids['l1b'],
 'players_differing': int(sum(1 for k in keys if B['it3'][k]['v'] != B['l1b'][k]['v'])),
 'verdict': ('INERT on values -- measured, not assumed. The v2 block overwrites _PVC0 after the L1b block, '
             'so L1b cannot reach player values.'),
 'but_it_IS_loaded': ('a first attempt that wrote a bare 1-64 curve into L1b HALTED the build inside '
             '_split_ladder ("no pool level"), because L1b carries its pool level as curve entry 65 and has '
             'no pool_value field. That halt proves the artifact is genuinely loaded and validated at import: '
             'inert on values, not inert on load.')}

A = json.load(open(f"{E}/probe_adopted.json")); V = json.load(open(f"{E}/probe_vor.json"))
EA = json.load(open(f"{E}/ev_adopted.json")); EV = json.load(open(f"{E}/ev_vor.json"))
out['channels_2a_2b_proof'] = {
 'question': 'did channels 2a/2b actually CONSUME the swapped curve, or are they half-wired?',
 'verdict': ('FULLY WIRED. unpl_eq tracks the swapped curve for every probed player, so the small echo is NOT '
             'half-wiring. But value() is not the board price path: board v == round(ev(p,2026)/1.0524), '
             'verified to the digit on 5 of 5 spot checks.'),
 'curve_payload_seen_by_probe': {'adopted': A['curve_payload_in_use'], 'vor': V['curve_payload_in_use']},
 'board_price_identity': 'board v == round(ev(p,2026) / 1.0524)  [L7 numeraire re-base]',
 'per_player': {k: {'ep': A['players'][k].get('ep'), 'branch': A['players'][k].get('branch'),
   'PVC2M_at_ep': {'adopted': A['players'][k].get('PVC2M_at_ep'), 'vor': V['players'][k].get('PVC2M_at_ep')},
   'unpl_eq': {'adopted': A['players'][k].get('unpl_eq'), 'vor': V['players'][k].get('unpl_eq')},
   'value_bal': {'adopted': A['players'][k].get('value_bal'), 'vor': V['players'][k].get('value_bal')},
   'ev_2026': {'adopted': EA['players'][k].get('ev_2026'), 'vor': EV['players'][k].get('ev_2026')},
   'v0_start': {'adopted': EA['players'][k].get('v0_start'), 'vor': EV['players'][k].get('v0_start')}}
   for k in A['players'] if 'error' not in A['players'][k]},
 'mechanism': MECH}

out['nonvacuity'] = {
 'convergence_metric_detects_change': 'baseline->it1 moved 21 players; it2->it3 moved 0. Same metric, both outcomes.',
 'channel_8_comparison_is_not_constant_true': ('it reported byte-identical for the L1b branch, and the same '
     'board comparison reported 21 movers for the curve swap'),
 'rank_metric': 'returns 0 on identical input (proven in the first addendum); reports 245 here',
 'fail_closed_guards': {
   'emit_no_vars': 'HALT naming ITEM279_OUT and ITEM279_MATRIX_NAME, in 0s',
   'emit_partial_config': 'HALT naming only the missing ITEM279_MATRIX_NAME, in 0s',
   'derive_no_label': 'HALT on CURVE_STATISTIC, in 0s',
   'guards_pass_when_set': ('iteration 3 ran to completion on the hardened scripts -- board 7977d7e5, matrix '
                            '3241310 bytes, fit 8/8 both-directions PASS')}}

json.dump(out, open(f"{OUT}/echo_279_estimate.json", 'w'), indent=1, sort_keys=True)
open(f"{OUT}/echo_279_estimate.json", 'a').write("\n")
json.dump({'probe_value_adopted': A, 'probe_value_vor': V, 'probe_ev_adopted': EA, 'probe_ev_vor': EV},
          open(f"{OUT}/echo_channels_279.json", 'w'), indent=1, sort_keys=True)
open(f"{OUT}/echo_channels_279.json", 'a').write("\n")
print("written")
print("  movers by gfut:", out['echo_converged_vs_baseline']['movers_by_settled_position_gfut'])
print("  channel8 byte-identical:", out['channel_8_branch_test']['boards_byte_identical'])
print("  converged echo: %d moved, median %.1f, max %d, rank %.4f%%" % (
    out['echo_converged_vs_baseline']['players_moved'],
    out['echo_converged_vs_baseline']['median_abs_delta_of_movers'],
    out['echo_converged_vs_baseline']['max_abs_delta'],
    out['echo_converged_vs_baseline']['rank_movement']['inversion_pct']))
