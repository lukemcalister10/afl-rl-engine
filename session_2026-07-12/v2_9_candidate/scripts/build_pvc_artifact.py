#!/usr/bin/env python3
"""L1c — build the engine artifact pvc_fit_candidate.json from the L1b smoothed derived curve.
Writes to the repo engine dir AND the live workspace. Stamped, non-bakeable candidate."""
import json, os, hashlib

SESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "/home/user/afl-rl-engine"
WS   = "/home/claude/rl_workspace/rl_after"

curve = {int(k): int(v) for k, v in
         json.load(open(os.path.join(SESS, "out", "pvc_curve_smoothed.json"))).items()}
store_md5 = hashlib.md5(open(os.path.join(REPO, "engine/rl_after/rl_model_data.json"), "rb").read()).hexdigest()[:8]

art = {
    "curve": {str(k): curve[k] for k in sorted(curve)},
    "fitted_from": "derived_curve.json pinned_d15_H10 (icbhpu 3c1d610f) + L1b local-linear smoothing h=0.20",
    "store_md5": store_md5,
    "n_anchors": 543,
    "window": "2004-2016 classes, d15 live lens, H=10; PICKEQ pedestals per addendum (SSP 92->51 HELD, L6)",
    "smoothing": "local-linear (LOESS deg1) log-pick tricube h=0.20; monotone re-imposed; pick1 pinned 3000; deviations in out/pvc_smoothing_deviation.csv",
    "candidate": "v2.9 L1 — NON-BAKEABLE (R3 bake-guard; needs RL_ALLOW_PVCFIT_BOARD=1)",
}
for d in (os.path.join(REPO, "engine/rl_after"), WS):
    with open(os.path.join(d, "pvc_fit_candidate.json"), "w") as f:
        json.dump(art, f, indent=1)
    print("wrote", os.path.join(d, "pvc_fit_candidate.json"))
print("store_md5", store_md5, "curve picks", min(curve), "-", max(curve), "pick1", curve[1])
