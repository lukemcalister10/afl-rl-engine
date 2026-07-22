# JOB 1 — peak-model `pvc_snapshot` / `_V4PVC` (rl_model.py:515,530,532): **HOLD (frozen)**

**Ruling basis:** R107.5 — "pvc_snapshot measured-first w/ post-bake fallback"; memo-C — fallback/hold
only on committed measurement, never assumption. **MEASURE FIRST, then decide.**

## What was measured (committed: `out/job1_peakmodel_measure.json`, script `scripts/measure_job1_peakmodel.py`)
The peak model `peak_model_v4.pkl` was **trained** with its logPVC feature = `pvc_snapshot.json`
(co-emitted by `build_peak_model_v4.py`). The migration question is: feed the live `pvc_curve_v2`
into that feature slot instead. Measurement of the model **input** and **output** under that swap:

- **Feature input** `log(_V4PVC[ep])` shift over the picks players actually sit at: `+0.000 .. +0.592`
  (deep picks lift most — v2's deep tail is far above the snapshot: e.g. pick 70 = 306 → 516).
- **Model output** `peak_est` shift, all 655 model-path players (of 745 active):
  - moved: **600 / 655**
  - mean |Δ| = **1.726** peak-pts · max |Δ| = **9.52**
  - mean |Δ%| = **2.62%** · max |Δ%| = **16.06%**
  - top movers: Kieren Briggs −9.52, Samson Ryan −9.23, Max Gawn −8.65, Joel Hamling −8.59,
    Bailey J. Williams −8.24, Maurice Rioli −8.15.

## Verdict: HOLD — do NOT migrate this consumer
The swap moves the model output for **600/655** model-path players by up to **16%**. That is
definitional **train/serve skew**: the pickle learned its coefficients against the snapshot feature
distribution; substituting a different curve at serve time makes every prediction off-manifold. The
committed numbers show a **retrain IS required** — therefore, per R107.5 + memo-C, the consumer holds
frozen on `pvc_snapshot.json`, and the retrain (rebuild `peak_model_v4.pkl` + re-emit `pvc_snapshot.json`
against v2) is recorded as the **POST-BAKE FALLBACK**. It is **not executed here** (out of this build's
scope; a peak-model rebuild is its own chapter).

## Board proof (the null, by construction)
This job makes **zero engine changes** — line `:515` `_V4PVC=json.load(open('pvc_snapshot.json'))` is
left byte-for-byte as shipped. Therefore job 1 moves **no board row** at either flag state:
`RL_PVC2=1` board stays `270a2c5f`, `RL_PVC2=0` stays `9829d01a`. Null proven by the untouched code
(the value-moving proof is the *counterfactual* measurement above, which is exactly why we HOLD).
