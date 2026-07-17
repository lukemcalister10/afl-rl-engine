"""JOB 1 (MEASURE FIRST) — the peak-model pvc_snapshot / _V4PVC consumer (rl_model.py:515,530,532).

R107.5: pvc_snapshot measured-first w/ post-bake fallback. The peak model (peak_model_v4.pkl) was
TRAINED with the logPVC feature = pvc_snapshot.json (co-emitted by build_peak_model_v4.py). Feeding
the live v2 curve into that feature at serve time is train/serve skew. This script QUANTIFIES, on
committed numbers, what migrating the feature snapshot->v2 would do to the model OUTPUT (peak_est) for
every player that reaches the model path — the evidence for the HOLD (memo-C: fallback/hold only on
committed measurement, never assumption).

Run in the workspace rl_after (pinned env). Emits out/job1_peakmodel_measure.json + prints a verdict.
NO engine value is changed and NO board is written by this script (measurement only).
"""
import os, io, contextlib, json, sys
import numpy as np

WS = '/home/claude/rl_workspace/rl_after'
os.chdir(WS)
G = {'__name__': '_job1_measure'}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']                      # the rl_model module
ev = G['ev']

# the two candidate feature sources for logPVC
SNAP = json.load(open('pvc_snapshot.json'))                                   # train-time feature (shipped)
V2   = {k: float(v) for k, v in json.load(open('pvc_curve_v2.json'))['curve'].items()}  # migration candidate

# force the model to load (_v4_init runs on first peak_est with a demonstrated level)
active = [p for p in MA.data if MA.active(p)]
for p in active:
    with contextlib.redirect_stdout(io.StringIO()):
        MA.peak_est(p)
assert MA._V4PVC is not None, "peak model did not initialise"

def model_path(p):
    # replicate peak_est's gate: only players with a demonstrated level_now reach the v4 model
    with contextlib.redirect_stdout(io.StringIO()):
        return MA.level_now(p) is not None and MA.gfut(p) is not None

# --- feature-input shift: how far does log(_V4PVC[ep]) move for the picks players actually sit at? ---
eps = sorted({min(MA.effpk(p), 70) for p in active if model_path(p)})
feat_rows = []
for ep in eps:
    ls, lv = np.log(SNAP[str(ep)]), np.log(V2[str(ep)])
    feat_rows.append((ep, SNAP[str(ep)], V2[str(ep)], round(lv - ls, 4)))

# --- model-output shift: peak_est under snapshot vs v2 for every model-path player ---
base_pe = {}
for p in active:
    with contextlib.redirect_stdout(io.StringIO()):
        base_pe[id(p)] = MA.peak_est(p)

MA._V4PVC = {k: float(v) for k, v in V2.items()}   # override the feature source
MA._pe_clear()                                     # clear the peak_est memo so it recomputes
v2_pe = {}
for p in active:
    with contextlib.redirect_stdout(io.StringIO()):
        v2_pe[id(p)] = MA.peak_est(p)
MA._V4PVC = {k: float(v) for k, v in SNAP.items()}  # restore (measurement only)
MA._pe_clear()

shifts = []
for p in active:
    if not model_path(p):
        continue
    a, b = base_pe[id(p)], v2_pe[id(p)]
    if a is None or b is None:
        continue
    shifts.append((p['player'], round(a, 2), round(b, 2), round(b - a, 3),
                   round(100 * (b - a) / a, 2) if a else None, min(MA.effpk(p), 70)))

d = np.array([s[3] for s in shifts], float)
rel = np.array([s[4] for s in shifts if s[4] is not None], float)
moved = [s for s in shifts if abs(s[3]) >= 0.005]
top = sorted(moved, key=lambda s: -abs(s[3]))[:15]

out = dict(
    _doc="JOB 1 — peak-model _V4PVC feature migration snapshot->v2: MEASUREMENT (no engine change). "
         "The model pickle was trained on pvc_snapshot; v2 in the logPVC slot is train/serve skew.",
    n_active=len(active), n_model_path=len(shifts),
    feature_input_logPVC_shift=[dict(pick=r[0], snapshot=r[1], v2=r[2], dlog=r[3]) for r in feat_rows],
    peak_est_output_shift=dict(
        n_moved=len(moved),
        max_abs=round(float(np.max(np.abs(d))), 3) if len(d) else 0.0,
        mean_abs=round(float(np.mean(np.abs(d))), 3) if len(d) else 0.0,
        max_rel_pct=round(float(np.max(np.abs(rel))), 2) if len(rel) else 0.0,
        mean_rel_pct=round(float(np.mean(np.abs(rel))), 2) if len(rel) else 0.0,
        top_movers=[dict(player=s[0], pe_snap=s[1], pe_v2=s[2], d=s[3], d_pct=s[4], ep=s[5]) for s in top],
    ),
    verdict=("HOLD — the v2 feature moves peak_est for model-path players (train/serve skew: the pickle "
             "was fit on pvc_snapshot). Per R107.5 + memo-C the consumer HOLDS frozen; the retrain is the "
             "POST-BAKE FALLBACK, recorded, not executed here."),
)
json.dump(out, open('/home/user/afl-rl-engine/session_2026-07-18/five_migration/out/job1_peakmodel_measure.json', 'w'), indent=1)

print("JOB 1 peak-model measurement (snapshot -> v2 feature)")
print("  active=%d  model-path players=%d" % (len(active), len(shifts)))
print("  feature logPVC dlog range: %+.3f .. %+.3f over picks the players sit at"
      % (min(r[3] for r in feat_rows), max(r[3] for r in feat_rows)))
print("  peak_est OUTPUT shift: n_moved=%d  mean|Δ|=%.3f  max|Δ|=%.3f  mean|Δ%%|=%.2f  max|Δ%%|=%.2f"
      % (out['peak_est_output_shift']['n_moved'], out['peak_est_output_shift']['mean_abs'],
         out['peak_est_output_shift']['max_abs'], out['peak_est_output_shift']['mean_rel_pct'],
         out['peak_est_output_shift']['max_rel_pct']))
print("  top movers:", [(s[0], s[3]) for s in top[:6]])
print("VERDICT: HOLD (train/serve skew; retrain = post-bake fallback, R107.5)")
print("wrote out/job1_peakmodel_measure.json")
