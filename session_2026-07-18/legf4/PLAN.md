# LEG F4 — MID/VETERAN FORWARD CALIBRATION · PLAN + ENTRY PROOF (read-only diagnosis) · seat 13 · 2026-07-19
Re-scopes item-354: the residual ~11pt board-wide forward-vs-backward asymmetry (composition forward −19.9%
vs realized backward −9.0%) living in the mid/veteran PRODUCTION cohorts (φ=0, untouched by F3). **WRITER
build, CHECKPOINT-GATED — this session is DIAGNOSIS ONLY (read-only); no engine edit before the supervisor
answers the mechanism.** Base: F3 exit `bccc231` (F3's cures are the floor, never re-opened).

## 0 — GIT ENTRY (item-334 law; this-session fetch)
`git fetch origin main claude/legf3-projection-fix-tbvxu5` — F3 ls-remote returns
`bccc23145e154f5b83385ffe8c06a54beab09030` STRICT (matched). Branch `claude/legf4-midvet-calibration-o6x36j`
re-based onto F3 exit `bccc231` (was sitting at the disjoint docs-lineage `main`; c0736a6 is an ancestor of
bccc231 so the re-base is a clean fast-forward, no F4 work discarded). Docs stay on MAIN — never joined.

## 1 — ENTRY PROOF (container-faithful; THREADS=1 on every hash-bearing run)
F3's build tree of record is the repo `engine/rl_after/` at `bccc231` — SELF-CONSISTENT and matched:
store `rl_model_data.json`=**968de0c7** · curve `pvc_curve_v2.json`=**56dd7a7b** · `rl_model.py`=**cc626d7d**
(all == F3's stamped anchors; the runtime workspace is seeded at the *bake-pin* f79fc740 which lacks Leg-B
`_UNCOMP` — a docs/store-lineage mismatch, so the diagnosis builds from the repo F3 tree, not the workspace).
Numeric stack: py3.12.3 · numpy2.4.4 · scipy1.17.1 · sklearn1.8.0 · scipy-openblas DYNAMIC_ARCH · threads
pinned 1 (OPENBLAS/OMP/MKL/NUMEXPR).

FAITHFULNESS (structural, stronger than a truncated file-md5 whose recipe is F3-ephemeral):
- **k=0 / backward DORMANCY invariant PASS** — RL_LEGF=0 vs RL_LEGF=1 boards are BYTE-IDENTICAL on v / vM1 /
  vM2 (804/804); only vP1 differs (639 rows). F3's cure is forward-only + RL_LEGF-gated, exactly as sealed.
- **The residual of record reproduces** — comp-controlled same-roster forward **−19.6%** (F3 record −19.9%),
  backward **−9.1%** (record −9.0%); backtest −1→now pred **558,568** vs 752,427 = **−25.8% OUT ±5%** (F3
  filed 556,300); cohort gradient developing −18.2% / mid −18.0% / veteran −24.8% (EXIT_PROOF −18.5/−18.3/
  −25.0). All within container numeric noise (<0.5pt) — the F3 board is faithfully rebuilt for diagnosis.

## 2 — THE JOB (read-only; reuse F3's harness + probes)
Localize WHY mid/veteran (φ=0) rows project forward ~2× steeper than their realized backward path —
per-mechanism decomposition with `_merged_recover.py` addresses, composition-controlled, per-cohort, no wide
bins. Output: DIAGNOSIS.md + CHECKPOINT.md. **No engine edit. HALT at the checkpoint for the fence grant +
MEMO addendum v1.2.**

## FENCE (pre-checkpoint): IN = `session_2026-07-18/legf4/` ONLY (diagnosis read-only). HARD-OUT: store ·
curve · V0/`_iso_dec` :1121-1171 · `rl_model.py` · pins/acceptance · `docs/` · ui · SEASON_PROG.
