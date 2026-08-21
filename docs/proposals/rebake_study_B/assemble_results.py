"""STUDY B — assemble every measurement into one RESULTS.json beside the study."""
import json, os, hashlib, subprocess

SC = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/user/afl-rl-engine/docs/proposals/rebake_study_B/RESULTS.json'
REPO = '/home/user/afl-rl-engine'


def load(n):
    p = os.path.join(SC, n)
    return json.load(open(p)) if os.path.exists(p) else {'_missing': n}


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


R = {
 '_doc': ('DESIGN STUDY B — every measurement behind DESIGN_STUDY_B.md. Produced read-only against '
          'the repo at store b745002e / band 34faa865 / q97m cfdc7321, in the pinned venv '
          '(sklearn 1.8.0, numpy 2.4.4, python 3.12.3). Scripts m1..m9 ship beside this file.'),
 '_independence': ('This seat did not read docs/proposals/rebake_study_A/ or '
                   'docs/proposals/REBAKE_SCOPE_2026-08-21.md. Study-A filenames appeared once in a '
                   'repo-wide grep result; no study-A file was opened.'),
 '_generated_utc': subprocess.run(['date', '-u', '+%Y-%m-%dT%H:%M:%SZ'],
                                  capture_output=True, text=True).stdout.strip(),
 'substrate': {
    'store_md5': md5(os.path.join(REPO, 'engine/rl_after/rl_model_data.json')),
    'cm_400_md5': md5(os.path.join(REPO, 'data/cm_400.pkl')),
    'q97m_md5': md5(os.path.join(REPO, 'data/q97m.pkl')),
    'peak_model_v4_md5': md5(os.path.join(REPO, 'engine/rl_after/peak_model_v4.pkl')),
    'v0surf_md5': md5(os.path.join(REPO, 'data/v0surf.pkl')),
    'git_head': subprocess.run(['git', '-C', REPO, 'rev-parse', 'HEAD'],
                               capture_output=True, text=True).stdout.strip(),
 },
 'HEADLINES': {
    'cm_400_training_rows_in_pickle': 13226,
    'cm_400_matching_committed_store': None,
    'cm_400_nearest_committed_store': {'rows': 13225, 'delta': 1, 'store_md5_8': 'b1fd0bce/0efdc5d6/968de0c7',
                                       'dates': '2026-07-15..2026-07-17', 'switches': 'T1off_MSDin_cut2021_cap2026'},
    'q97m_training_rows_in_pickle': 13111,
    'q97m_matching_committed_store': {'store_md5_8': 'b1fd0bce/0efdc5d6/968de0c7',
                                      'dates': '2026-07-15..2026-07-17',
                                      'switches': 'T1off_MSDex_cut2021_cap2026',
                                      'note': 'the pickle was committed 2026-07-14 08:42Z, the store landed 2026-07-15 08:01Z'},
    'current_store_design_rows': 13220,
    'band_training_rows_taught_a_guessed_age': 1874,
    'band_training_rows_taught_a_guessed_age_pct': 14.18,
    'law3_pct_steps_negative_PINNED_cm400': 23.40,
    'law3_pct_steps_negative_histgbr_quantile_monotonic_cst': 1.65,
    'law3_negative_steps_exact_arm_every_design_row': 0,
    'law3_total_steps_exact_arm_every_design_row': 1004720,
    'walk_forward_pinball_mean_incumbent': 3.9267,
    'walk_forward_pinball_mean_exact_constrained_selected': 3.9213,
    'gbr_accepts_monotonic_cst': False,
    'pool_deletion_walk_forward_cost_all_rows_pct': 6.4,
    'recency_weight_best_gain_pct_window_anchor_16y_halflife': 0.18,
    'selected_hyperparameters': {'learning_rate': 1.0, 'max_iter': 800, 'max_depth': 4, 'min_samples_leaf': 25},
 },
 'M1_artifact_census': load('m1_out.json'),
 'M2_current_store_design_matrix': load('m2_out.json'),
 'M3_store_sweep_and_drift': load('m3_out.json'),
 'M4_provenance_grid': load('m4_out.json'),
 'M5_estimator_bakeoff_age_pool_weighting': load('m5_out.json'),
 'M6_dob_courier_blast_radius': load('m6_out.json'),
 'M7_constrained_estimator': load('m7_out.json'),
 'M9_selection_and_data_design': load('m9_out.json'),
 'M10_extended_selection_grid': load('m10_out.json'),
 'M11_recency_weight_anchor_check': load('m11_out.json'),
}
json.dump(R, open(OUT, 'w'), indent=1, sort_keys=True, default=str)
print('wrote', OUT, os.path.getsize(OUT), 'bytes')
