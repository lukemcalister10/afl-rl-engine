# PREREG — RECENCY AUDIT SEAT (Order 33/34 follow-on, issue #334, 2026-08-17)

**Mandate: READ-ONLY.** Measure the engine's EFFECTIVE weighting of past seasons in its
production valuation and compare it to Order 33 seat W4's measured optimum (best convex level
weighting: w* ≈ 0.45–0.5 on the most recent season, ≈ 2 : 1 : ½ across the last three seasons —
`docs/evidence/order33_w4_2026-08-17/PACKET_W4.md` §2). Nothing in the engine, board, store or
law is touched. No store file is ever written; every perturbed player exists only in memory.
This file is committed and pushed BEFORE any measurement runs.

## 1 · Build under measurement

- **Primary: the Candidate-31 lane, dial ON** — the seat's named build. Engine loaded read-only
  in-process from a staged copy of this worktree's `engine/` (the bb31f.sh staging convention:
  same file set, `RL_REPO`/`RL_FV` pointed at the stage, cwd = staged rl_after), environment
  exactly `docs/evidence/candidate_31f/runenv.sh` + `bb31f.sh`: `PYTHONHASHSEED=0`, five-var
  thread pinning (OPENBLAS/OMP/MKL/NUMEXPR/VECLIB = 1), `RL_V0SURF_PKL=$ROOT/data/v0surf.pkl`,
  `RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400
  PAR_RAMPS=22`, plus **`RL_O31=1`** (the dial). Strictly sequential; one engine process at a time.
- **Secondary (disclosure only): `RL_O32=1`** — the ORDER-A-repair candidate wired at this HEAD
  (board 557dbefe). Run on a ~12-player subsample of the same sample to disclose whether the
  repair moves the effective recency weights. Descriptive; the primary verdict rides RL_O31.
- Price read: `ev(p, Y=2026)` — the final one-law price, UNROUNDED under the dial (the engine's
  own convention for the O31 lane), in engine currency. Currency and numeraire cancel in the
  normalized weights.

## 2 · Sample (fixed before any price is computed)

From `MA.data`: real store players (`key` present), not retired, not delisted, not pool-synthetic,
with **2–6 played seasons** (seasons with games > 0 inside the engine's debut window
`(debutyr−1) < year ≤ 2026`) and base price `ev(p) ≥ 100` (so weight normalization is not
division by noise). Stratified draw: for each cell (position group KEY/GEN/MR from the engine's
`_ldg(gfut)` × seasons-of-history 2/3/4/5/6), up to **3 players** drawn by `random.Random(3334)`
from the cell sorted by key; thin cells take what exists. Target n ≈ 30–45. The drawn list is
recorded in the output JSON before perturbation results are appended.

## 3 · The measurement

For each sampled player and EACH played season s (one at a time): an in-memory copy of the player
dict (scoring rows copied) with that season's `avg` increased by **δ = +2.0** points; price
response Δ_s = ev(copy) − ev(base). **Effective season weight** ŵ_s = Δ_s / Σ_s' Δ_s', computed
only when Σ_s' Δ_s' > 0; players with non-positive total response are reported as unresponsive,
not silently dropped. Negative individual Δ_s (nonmonotone layers) are disclosed and kept in the
normalization. References to all perturbed dicts are held alive for the process lifetime (the
engine memoizes one cache on `id(p)`; `b6` clears it per call, this removes the residual hazard).

**Aggregation** (all fixed now): mean / median / IQR of ŵ_s by years-back (0 = the in-progress
2026 season, 1 = 2025, …), overall and split by (a) seasons-of-history 2–3 vs 4–6, (b) latest
completed-season games band (<10, 10–17, 18+), (c) position group. The headline **latest-season
share** = ŵ(2026 in-progress) + ŵ(2025), i.e. the mass on evidence from the most recent
completed season and its in-progress continuation — the object comparable to W4's "weight on the
most recent season" (W4's panel years are completed seasons; the live board's newest evidence is
split across the 2025/2026 pair). ŵ(2025) alone and ŵ(2026) alone are both reported.

**Nonlinearity / perturbation-size sensitivity**: on 10 players (first 10 of the sample by the
same seeded order), δ ∈ {+1, +2, +4}; report per-player max_s |ŵ_s(δ=1) − ŵ_s(δ=4)|. If the
sample median of that quantity exceeds **0.10**, the weights are declared perturbation-size
sensitive and the verdict is downgraded to the noisy call of §4.

## 4 · Decision rule (fixed before results)

Let W_latest = the sample MEDIAN latest-season share (§3), with its IQR.

- **ALIGNED** — W_latest ∈ [0.35, 0.65]: the engine's effective recency sits in W4's optimal
  neighbourhood; no ruling material.
- **UNDER-RECENT** — W_latest < 0.35: the engine effectively flat-averages history relative to
  the measured optimum; ruling material filed (§5).
- **OVER-RECENT** — W_latest > 0.65: the engine over-chases the latest season; ruling material
  filed (§5).
- **TOO NOISY TO CALL** — if the cross-player IQR of the latest-season share exceeds 0.35, or
  the §3 nonlinearity trip fires: reported as the result, per the seat's honesty clause. Class
  splits are then descriptive only.

Honest caveat, fixed now: W4's w* was fitted for predicting NEXT-SEASON output (and agreed in
direction on 3-yr/6-yr targets); the board prices a multi-year forward object, so the optimum is
a neighbourhood, not a point — hence the wide ALIGNED band.

## 5 · Rulings material (only if UNDER- or OVER-RECENT)

Direction and rough size of mispricing on current board rows: rank
`docs/ledgers/CANDIDATE_31_MOVERS.json` rows by |latest-season avg − prior-seasons recency-
weighted avg| (both off the store, same debut window), name the top rows each side, and state
which way the current board mis-weights them. Fix family (named, NOT wired): a re-weighting
inside the production evidence — the `RECENCY_DECAY`/`LDECAY_G`/`level_demo`-conf family —
marked **AWAITING RULING**. No engine edit, no board, no artifact.

## 6 · Outputs

`docs/evidence/order34_recency_2026-08-17/`: this prereg, `recency_measure.py` (the harness),
`RECENCY_WEIGHTS.json` (sample + all Δ and ŵ), `MEASURE_RECENCY_out.txt` (console),
`PACKET_RECENCY.md` (plain-language packet). Push-per-step to `land/order-29`.
