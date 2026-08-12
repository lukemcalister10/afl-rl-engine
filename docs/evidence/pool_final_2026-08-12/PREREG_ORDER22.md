# PRE-REGISTRATION — ORDER 22, THE POOL REPRICING SHIPPING PACKET

**Committed BEFORE any measurement is run.** Standing law: pre-register first, score every prediction
honestly at the end, own every breach by name. Nothing in this act lands.

## PINS ASSERTED AT ENTRY AND EXIT

| pin | path | md5 |
|---|---|---|
| board | `data/rl_build/rl_app_data.json` | `1dbd1480a34c7823f330273211cbb76a` |
| store | `engine/rl_after/rl_model_data.json` | `d9a24282357cf3083b1640466e3ecd83` |
| instrument | `docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py` | md5 COMPUTED at run, never hardcoded; expected `0f8220351c64c56ccfa90c60edcdfa5f` |
| ORDER 21 surface | `docs/evidence/pool_retention_2026-08-12/POOL_RETENTION_SURFACE.json` | `00ca5c3d1d4eca7e3b9a7d3ed3877d2e` |

Branch `build/pool-final` from `origin/main` (`a79d580`). Worktree-isolated. No `git add -A`.

## THE STAGED CONFIGURATION (ORDER 21's, reproduced byte-exactly)

> **env** `RL_H_POOLSIT=1.0 RL_H_UNION=1.0` (manifest dials, gate mode, config hash restamped, boot guards armed)
> **patch** `python o21_patch.py <worktree> derived POOL_RETENTION_SURFACE.json`

**CONTROLS, and either failing is a HALT:**
- **C1** unstaged (`nopatch`, HEAD defaults) board reproduces the live board `1dbd1480a34c7823f330273211cbb76a` **byte-identical**.
- **C2** staged (`derived` + both dials) board reproduces ORDER 21's DERIVED board `be89cbac9b0db6d70ecedc28696445ff` **byte-identical**.

## DECLARED TOLERANCE FOR THE ITERATE-TO-TOLERANCE STEP

**Convergence tolerance: 1.0% relative on each pathway's measured λ against the target**, i.e.
`|λ_measured − 1| ≤ 0.010` for every wired pathway, where λ_measured is that pathway's career profile
measured on the rebuilt matrix divided by the freshly measured national target.

Tighter reporting if convergence allows. **Non-convergence or oscillation is a BLOCKER, reported, not forced.**
Iteration cap declared in advance: **8 rounds**. If 8 rounds do not reach tolerance, that is the report.

## THE PREDICTIONS

| # | quantity | prediction |
|---|---|---|
| P1 | fresh arm-split national target on the staged engine | in **0.97 – 1.02** (ORDER 20 read ≈0.9944 pre-fix) |
| P2 | control C1 (unstaged board) | reproduces `1dbd1480` byte-identical |
| P3 | control C2 (staged board) | reproduces `be89cbac` byte-identical |
| P4 | raw λ ordering, layer 1 | SSP > MSD > ND>64 > RD > PDA > UNR > IRE > PDN > PDS |
| P5 | shrinkage weights at K=15 | RD w > 0.97; PDS w < 0.62; every other pathway w in 0.70 – 0.99 |
| P6 | direction of uniform K=15 shrinkage | PDS, PDN, IRE, UNR, PDA rise toward the pool aggregate; SSP and MSD fall |
| P7 | reconciliation, shipped construction, entry-weighted both layers | worst relative residual **≤ 1e-9**, and in fact **< 1e-12** |
| P8 | rule 1 (remainder at pathway value) diagnostic | **FAILS** for at least 3 partially-sampled pathways; rule 2 passes for all nine |
| P9 | layer-2 sampled cells at n ≥ 20 | **13 of 54** (RD 6, ND>64 3, MSD 2, IRE 1, UNR 1) |
| P10 | derived RD positional ordering | RUCK highest, KPD lowest — inverting today's priced order |
| P11 | iteration | converges to the declared 1.0% on **every** pathway within **6** rounds |
| P12 | staged board total after repricing | **falls** relative to the ORDER 21 staged board 751,554 |
| P13 | separation law | ND board rows moved = **0**; national v0 delta = **0 exactly** |
| P14 | all-arm PRIMARY yr1, FINAL vs STAGED 0.7995 | **rises** (pool year-0 falls, produced prices do not) |
| P15 | arbitrage | **0 of 5 readings** open an arbitrage; every margin positive |
| P16 | legacy 1-64 aggregate margin | moves by **≤ 0.05 points** vs SHIP (+6.70%) |
| P17 | `_ruc_prior_cap` on derived pool ruck v0s | **binds** on at least one pathway's rucks |
| P18 | ND65+ curve cap `min(measured_k15, curve[64]=185)` | derived ND>64 level lands **below 185**, so the cap does **not** bind after repricing |
| P19 | age (D7, presented as a packet option, not wired) | RD is the only pathway with a quality-fitted age signal at \|t\| > 2 |
| P20 | integer truncation in `_POOL_LEVELS` (`int(float(v))`) | costs **< 1.0%** relative on every wired level |
| P21 | layer-2 wiring surface | the signed table can express positional cells for **RD only**; the other eight pathways' derived positional cells are DERIVED AND REPORTED but NOT WIRABLE without new structure |
| P22 | ND 1-64 board value under the final configuration | **620,877 exactly**, unchanged from every ORDER 21 variant |
| P23 | pool board rows that move at all | **≤ 120** of 242 (the carry finding: only 82 pool rows were reachable by an entry-price change on the live board, plus the retention movers) |
| P24 | year-4-over-year-0 for the pool, FINAL | **rises** relative to SHIP, and remains **below** ND's year-4-over-year-0 |
| P25 | the four carried flags | all four (O1, RUCK d1=1.000, PDA harsher, plus anything this build adds) are carried unresolved to the owner; **the seat rules none of them** |

## STANDING LAWS RESTATED AS BINDING ON THIS ACT

- **YEAR-4-IS-NOT-A-TARGET.** Both headline metrics are read; neither is aimed at.
- **The play-quality principle.** Availability is never a valuation basis.
- **Derive, never scale.** The multiplier tables are evidence and sizing, not the mechanism.
- **The level law.** No asymmetric level change; the pool's level moves as its own calibration, and the
  national arm is not touched at all (separation).
- **No cherry-picking.** Every figure names its instrument and its population.
- **Canonical instruments copied, never modified.**
- **Nothing lands.** Branch + PR + STOP.
