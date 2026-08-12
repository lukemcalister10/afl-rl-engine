# PRE-REGISTRATION ADDENDUM 1 — the mid-flight owner ruling of 2026-08-12

**Dated 2026-08-12, written and committed AFTER the ruling arrived and BEFORE any measurement was
taken on the relaxed surface.** The original `PREREG_ORDER22.md` is NOT rewritten. Predictions
anchored to the superseded (isotonic) surface are scored **as superseded**, with their measured value
printed, never hidden.

## WHAT CHANGED

Owner ruling, #334 comment 5262159933, verbatim:

> *"I am actually ok with this not being isotonic as it's logical. If you are not good, you can be
> delisted. Especially with pool players starting on one year contracts, survival can be a more
> positive sign — whereas a lot of year 1 sitters sit because they're not up to the level, so would be
> delisted after a year. Those who are not are not for a reason. So I think it would be fine for 2
> year sitters/3 year sitters to reflect the data we have."*

The pool retention surface is re-derived with the non-increasing projection **relaxed at depths ≥ 2**,
whole-pool layer and pathway layer, clip `[0.05, 1.0]` retained, **national surface untouched**.

| | md5 | status |
|---|---|---|
| ORDER 21 surface (isotonic) | `00ca5c3d1d4eca7e3b9a7d3ed3877d2e` | **SUPERSEDED** — the stage the act opened on |
| **ORDER 22 surface (relaxed)** | **`0f3d1a24b9fb132a531e460885f16fa5`** | **IN FORCE** |

Built by `o22_make_relaxed_surface.py`, which reads ORDER 21's `pool_retention_derive.py`
(md5 `6df38acbdf860db7c8387b4f87159342`, **never written**), applies six printed textual
substitutions, and runs the copy from the scratchpad. **CONTROL PASSED: depth-1 is unchanged at all
30 wired vectors, 0 differences.** 42 depth-over-depth rises are now wired across the 27
pathway × class vectors.

## WORK ALREADY DONE ON THE SUPERSEDED SURFACE — KEPT, NOT DISCARDED

Rounds A0–A4 of the iterate-to-tolerance step ran on the isotonic surface and **converged**. That
trajectory is filed in `ITERATION.md` and scored as a superseded-surface result. It is also the warm
start for the relaxed rounds (R1…), which is declared here rather than presented as a fresh start.

## RE-REGISTERED PREDICTIONS (relaxed surface)

| # | quantity | prediction |
|---|---|---|
| **R1** | staged board on the relaxed surface (checkout levels) | **differs from `be89cbac`**; new hash declared; total **above** ORDER 21's 751,554, because depths ≥ 2 rise for nonKPP and RUCK |
| **R2** | unstaged control | still reproduces `1dbd1480` byte-identical |
| **R3** | depth-1 row of the relaxed surface | **identical** to ORDER 21's at all 30 vectors |
| **R4** | convergence on the relaxed surface, warm-started from the isotonic fixed point | **≤ 3 further rounds** to the declared 1.0% on every pathway except any structurally blocked one |
| **R5** | O1 (KPP := max(KPP, nonKPP)) on the relaxed surface | binds at **MORE than 3 of 6** KPP depths and by **larger** gaps than on the isotonic surface |
| **R6** | pool sitters whose board value RISES year-over-year while sitting | **> 0** — the wired consequence the owner accepted |
| **R7** | arbitrage under the relaxed surface | **0 of 5** readings open one |
| **R8** | separation | ND rows moved = **0**; national v0 delta = **0 exactly** — unchanged by the amendment |

## PREDICTIONS FROM THE ORIGINAL PREREG THAT THE AMENDMENT SUPERSEDES

**P3** (staged board reproduces `be89cbac`) — retained as the ORDER 21 reproduction control, which
**was run and PASSED before the ruling arrived**; it no longer describes the shipping stage.
**P12** (board total falls relative to 751,554) — its baseline moves; re-scored against the relaxed
staged board.
**P11** (convergence within 6 rounds) — re-scored as R4 above, with the isotonic rounds counted and
declared.

Everything else in the original pre-registration stands.
