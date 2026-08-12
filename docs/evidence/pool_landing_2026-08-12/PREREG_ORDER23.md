# PRE-REGISTRATION — ORDER 23: THE FINAL ITERATION AND THE POOL-UPDATE LANDING BRANCH

Issue #334, owner rulings filed at comment **5262928754** (2026-08-12). Branch `land/pool-update`,
cut from `origin/main` `27d9484`.

**Committed BEFORE any board is built, any matrix is emitted and any level is measured on this
branch.** Everything below is a prediction, not a result. Breaches are reported as breaches.

---

## 0. WHAT THE OWNER RULED, AND WHAT THIS ACT DOES WITH IT

1. **Price is an OUTCOME.** Prices are derived from career outcomes; the ratio tables are diagnostic
   presentation, never mechanism. The converged fixed point satisfies this by construction — the old
   levels wash out.
2. **The target stands**: ND-parity, measured fresh, arm-split, on this act's own final matrices.
3. **The ND>64 cap is AMENDED**: the signed `nd65_plus` law's `min(measured_k15, curve[64])` cap is
   REMOVED. The pathway prices at its derived level. The old law text is preserved as history in
   `pvc_curve_v2.json`, not deleted.
4. Standing: O1 OFF · isotonic relaxed at depths ≥2 · class-axis K=10 shrinkage · uniform K=15 at
   layer 1 · K=10 at layer 2 with the renormalisation guard and the residual-group rule ·
   `H_POOLSIT`/`H_UNION` retired to 1.0 · U mean-preserving exactly.

## 1. THE STAGE, DECLARED BEFORE IT IS RUN

The ORDER 22 stage is reproduced exactly and then amended in exactly one place.

| element | value |
|---|---|
| retention surface in force | `POOL_RETENTION_SURFACE_FINAL.json` md5 `b595d49982a083ed760ce629759366b3`, U re-derived per round |
| warm start | ORDER 22's F1 fixed point: `FINAL_LEVELS.json`, surface `d87f79ca17cc9dded3281055e5bbe4bb` |
| env dials | `RL_H_POOLSIT=1.0 RL_H_UNION=1.0` (shipped defaults on the landing tree) |
| patcher | ORDER 21's `o21_patch.py` (`b2c01de9fc8fdb615adf35819ea5f9b3`), **carried, never modified** |
| THE ONE AMENDMENT | `rl_model.py:1423-1424` — `_ND65 = min(measured_k15, curve[64])` becomes `_ND65 = measured_k15` |

**Declared tolerance, unchanged from ORDER 22:** 1.0% relative on every pathway's **shrunk λ** (the
quantity the level step acts on), now over **ALL NINE** pathways rather than eight. **Declared cap: 8
further rounds.** Non-convergence is a BLOCKER and is reported as one.

**Declared update rule, unchanged:** `L ← L × λ`, with the declared secant acceleration from the
second round (β fitted on two consecutive rounds, clipped to [0.25, 3.0], per-round move capped at a
factor of 2, β printed every round). Levels are written as INTEGERS, matching the engine's own
`int(float(v))` truncation.

---

## 2. PREDICTIONS — THE CONTROLS

- **C1.** The **unmodified** landing tree rebuilds the live board `1dbd1480a34c7823f330273211cbb76a`
  **byte-identical**. If it does not, the act HALTS here.
- **C2.** The ORDER 22 staged recipe, re-run from this branch (F1 surface + `FINAL_LEVELS.json`,
  cap still in force, `H=1.0`), reproduces the packet's FINAL board
  `21055b901312f76a8f0b17d362932130` **byte-identical**.
- **C3.** `o22_derive.py`'s own control — `harness_armsplit.structural_values(split=False)`
  reproduces the pinned harness value-for-value — passes on every round.
- **C4.** The landing tree's board is **byte-identical** to the board the task-1 final staged
  configuration produces, and reproduces on a second independent build.

## 3. PREDICTIONS — THE UNCAPPED ITERATION

- **I1.** The iteration **converges**: `|shrunk λ − 1| ≤ 1.0%` on **all nine** pathways, within
  **4** further rounds warm-started from F1 (cap 8).
- **I2.** The target re-measures to **0.9900060981** — identical to the last printed digit, at every
  round, as it has been across all eight ORDER 22 rounds. (If it differs, that is reported.)
- **I3.** ND>64's final level lands **above the packet's 274**, in **[270, 305]**. Grounds: at 274 the
  pathway still returns ≈3.6% more than target (its numerator is invariant to its own level — the
  packet measured 0 of 9 ND>64 rucks on the `_ruc_prior_cap`, the only route by which a pool level
  reaches `v0_start`), so one more step is required.
- **I4.** **Every other level moves DOWN** vs the packet's FINAL_LEVELS, by **≤2.0%** each. Grounds:
  uncapping raises the pool's total entry price, dropping the ALL-POOL aggregate λ from 1.0389 to
  ≈1.001; each pathway's shrunk λ falls by `(1−w)×0.038`, i.e. −0.08% at RD's w=0.979 and −1.6% at
  PDS's w=0.583.
- **I5.** The six **RD positional** levels move by **≤1 integer unit** each (RD's w = 0.979).
- **I6.** The **ALL POOL** aggregate λ at the fixed point is within **0.5%** of 1.000.
- **I7.** At the fixed point the **raw** λ is within **1.0%** on **all nine** pathways — the packet's
  identity argument (`raw = (shrunk − (1−w)·pool_agg)/w`) says the raw/shrunk gap collapses once the
  pool aggregate itself sits at 1.
- **I8.** The reconciliation identity holds: worst relative residual **≤ 1e-9** (in fact < 1e-12) on
  all nine pathways, entry-weighted in both layers.
- **I9.** U stays **mean-preserving exactly**: 0 pathways whose post-redistribution entry-weighted
  mean differs from 1.0000000000.

## 4. PREDICTIONS — SEPARATION (the standing law)

- **S1.** ND 1-64 board rows moved = **0**, on every lever and on the landed board.
- **S2.** ND 1-64 board value = **620,877** before and after.
- **S3.** National records repriced on any year of the 24-year walk-forward = **0**.
- **S4.** National records whose `v0` moved = **0 EXACTLY**, not merely small.
- **S5.** Any non-pool board row moved = **0**.

## 5. PREDICTIONS — THE BOARD AND THE LEDGER

- **B1.** The landed board total is **above** the packet's 753,668 — the ND>64 pathway now reprices
  upward instead of being held at 185.
- **B2.** Board rows moved vs live `1dbd1480` is **above 109** and **below 160**.
- **B3.** The ND>64 pathway's board value rises by **more than +117** (the packet's capped figure).
- **L1.** The composed movers ledger carries **one row per moved board row**, each with the
  three-lever decomposition (H retirement / retention / repricing) for every mover ≥50 points, and
  the three lever components sum to the total delta for every row.

## 6. PREDICTIONS — THE LANDING MECHANICS

- **P1.** The pins that move in `data/expected_boot.json` are **exactly**
  `{board, config, engine_head, rl_model}`. `fv` does **not** move (no
  `engine/forward_valuation` source is touched). The restamp script **asserts the moved set before
  writing**.
- **P2.** `store` stays `d9a24282357cf3083b1640466e3ecd83`; **no frozen pickle is regenerated**
  (`q97m`, `v0surf`, `peak_model`, `pvc_snapshot`, `bust_prior`, the band pickle) — every one
  asserted equal to `origin/main` by computed md5.
- **P3.** The boot guard **passes** on the landed tree.
- **P4.** The book re-seal moves F2 book↔board parity from **>0 mismatches to 0**, in its own
  isolated commit.
- **P5.** The instrument files are **untouched**; their md5s are **computed at run, never
  hardcoded**, and equal `origin/main`'s.
- **A1.** **0 of 20** instrument readings open an arbitrage (margin vs 14% negative). Any arbitrage
  opened is a BLOCKER.
- **A2.** The legacy `noarb_table_338.py` picks 1-64 aggregate margin moves by **≤0.05 points**.
- **N1.** The N43 literals in `one_source_selftest.py` are re-signed to the final derived levels, the
  selftest's **structure is kept**, and its ND65+ check is rewritten to the amended law (no cap)
  rather than deleted.

---

## 7. WHAT THIS ACT WILL NOT DO

- It will not merge. Branch + PR + **STOP**. Only the owner's word merges.
- It will not touch the store, any pickle, any instrument, the national retention surface, or the
  national pick curve.
- It will not wire an age adjustment, will not wire layer-2 structure for the eight non-RD pathways,
  and will not turn O1 on. Those remain owner questions carried from the packet.

_Pre-registered by the build seat, ORDER 23, 2026-08-12._
