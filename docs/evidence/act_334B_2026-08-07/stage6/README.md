# 334 stage B / STAGE 6 — THE CONDITIONED DEVELOPMENT CORRECTION (established leg)

Branch `landing/334-stage-b`, built on the stage-5 landing (board `13f8c2e0`, tip `0dde8e8`).
Nothing merges to main; no PR; no tag. **Adoption is the owner's word, and so is the rung.**

> **AMENDED 2026-08-07 by the CONFORMANCE REPAIR** — issue #334 comment `5219329372`. The original
> build (tip `d405afb`) deviated from its own pre-registered directive in two measurable ways. Both
> are corrected here. **The shipped board does not move** and no design decision was re-opened.
> The superseded artifacts are preserved — see **HISTORY** at the foot of this file.
>
> **READ `FRONTIER.txt` SECOND.** Registered gates bind on three quarters of the ladder now. What
> they cost against the owner's ruled range is stated there in one sentence, with the roads out —
> both of which are the owner's, not this seat's.

## WHAT THE REPAIR CORRECTED

| | the original build | **the registered convention** |
|---|---|---|
| **estimand** | rolling 4-year mean `mean_k[v(Y+k)/1.0939^k]` → year-1 aggregate **1.0963** | **F = v(career year 4) discounted back at the 1.0939 hurdle** (the engine's no-arb identity; 1.0939⁴ = 1.432 = the year-4 band) → **1.1363**, n=414 |
| **performance axis** | `pr = bestlvl/par`, wrongly named as the cross-section's axis | **`sa`, the SEASON SCORING AVERAGE in the evaluation year** — the axis the cross-section terciled |

The registered statistic reproduces the cross-section of record at all three evaluation years —
**1.1363 / 1.0041 / 0.9733** against the filed **1.136 / 1.004 / 0.973** — reads **exactly 1.0000**
at evaluation year 4 (the identity that proves the convention), and on the `sa` axis reproduces
every named cell to the third decimal, including the owner's "already priced in" cell:
**picks 1-10 × top-tercile = 1.0039, dead par.** The surface was under-taught: it conserved 72.2%
of the registered residual. **`MEMO.md` §10** states what was wrong, what changed, and why this is
conformance and not tuning.

## THE SHIPPED STATE — UNCHANGED BY THE REPAIR

**`RL_G6_W = 0` and `RL_G6_KPD = 0`.** The shipped board is the stage-5 landing
`13f8c2e0240600733a5fb42414510445`, **byte-exact through the full gated build**, and the correction is
*structurally* inert — with the dials at 0 the branch is not taken and `g6_table.json` is never opened
(proved by rebuilding with the table moved aside; `KILLSWITCH_PROOF.txt`). Addendum 1 F9/F10: the
default protects the owner's ruling from being anchored by a seat that has already picked a rung.
**This seat makes NO recommendation on the rung.**

## THE FOUR-RUNG LANDING — BOTH BASES, full cohort leading (ruling 5217177098)

| population (year 1) | n | pre-s5 | s5 LANDED | rung 0.25 | rung 0.5 | rung 0.75 | rung 1.0 |
|---|---|---|---|---|---|---|---|
| **FULL COHORT ND+pool 2004-2025** | 2517 | 0.908179 | 0.946050 | **0.962364** | **0.978708** | **0.995053** | **1.011399** |
| ND 1-64, 2004-2025 | 1383 | 0.949994 | 0.988526 | 1.009230 | 1.029973 | 1.050717 | 1.071461 |
| pool routes, 2004-2025 | 1134 | 0.752800 | 0.788214 | 0.788214 | 0.788214 | 0.788214 | 0.788214 |
| ND 1-64, 2004-2022 (**teaching window**) | 1197 | 0.950431 | 0.990805 | 1.011071 | 1.031377 | 1.051681 | 1.071991 |
| ND picks 1-20, 2004-2022 | 377 | 0.970665 | 1.001589 | 1.019343 | 1.037165 | 1.054967 | 1.072792 |
| ND picks 21-64, 2004-2022 | 820 | 0.918348 | 0.973706 | 0.997954 | 1.022200 | 1.046470 | 1.070721 |
| | | | | **FEASIBLE** | **STRUCK** | **STRUCK** | **STRUCK** |

**The pool leg takes ZERO at every rung, by construction** — the declared pick taper zeroes the pool
index (effpk 65). The pool is stage 7's, on its own measurement (#334 comment 5217529020). The
full-cohort basis therefore never reaches 1.04, which Addendum 1 F4 required printed explicitly, and
**the basis question goes to the owner** — this seat does not resolve it.

**THE HONEST CEILING.** Solved as a continuum rather than at a presented rung, the maximum intensity
the registered gates permit is **rung 0.4193** (bound by picks 1-20 × above-median `sa`), landing
year 1 at **1.024847** on the teaching window. That is the most this act can deliver honestly at any
intensity, and it is **short of the 1.04 floor by 0.0152**. The presented ladder is deliberately NOT
re-cut to sit on it: inventing a rung to land on the frontier is the tuning the strike law prevents.

> The reconciliation forecast a ceiling of ~1.0178 at a max rung of ~0.3, on an invariance argument.
> **Measured, it is 1.0248 at rung 0.4193** — the re-teach changed the surface's shape, not only its
> level, so the year-1 gain grew faster than the zero-cell move. The reconciliation's *direction* is
> confirmed in full (the frontier shrank, more rungs are struck, the band is unreachable); its
> arithmetic was an approximation. `FRONTIER.txt` §4 states the difference plainly rather than
> forcing agreement.

## THE ESTIMAND, AND THE STATISTIC PRE-REGISTERED BESIDE IT

The estimand is the **value-weighted aggregate** F′ on the year-1 established leg: **1.1363**
(under-priced by 13.6%). The **median** F′ is **0.8672** — the *typical* year-1 established player is
already priced **15% ABOVE** his own realised discounted future, and only **45.2%** of them out-earn
even the uncorrected price. **The residual is carried by a right tail.**

| rung | corrected aggregate F′ | corrected **median** F′ | typical player over-priced by | fraction who out-earn the corrected price |
|---|---|---|---|---|
| 0 (shipped) | 1.1363 | 0.8672 | 15% | 45.2% |
| 0.25 | 1.0997 | 0.8153 | 23% | 43.5% |
| 0.5 | 1.0653 | 0.7725 | 29% | 42.0% |
| 0.75 | 1.0331 | 0.7472 | 34% | 41.3% |
| 1.0 | 1.0027 | **0.7173** | **39%** | 40.3% |

**THE MEDIAN-NEUTRAL RUNG IS BELOW ZERO.** No positive rung improves the typical player's honesty;
every rung worsens it while improving the value-weighted aggregate. The registered estimand makes
this tension **sharper** than the superseded one did (the typical player was 4% over-priced on the
old statistic and is 15% over on the registered one), and it is the central pub-test item.

## THE FENCE — the gate the directive puts first

| | |
|---|---|
| sit-out population, engine-enumerated (`ns==0` at 2026, not delisted) | **165** |
| **integer-identical at rung 0.25 / 0.5 / 0.75 / 1.0** | **165 / 165 at every rung — PASS** |
| Mraz (pick 35, 2024, year-1 sit-out) | **1645 at every rung** = **3.1038× his pick** — tier "3.0-3.5×, pass disclosed", unmoved |
| Nairn | **605 at every rung**, unmoved |
| unattributed movers | **0 at every rung** |

The fence is structural: the correction is applied **only** in the `ns>=1` arm of `ev()`, strictly
after the sit-out return, so `e_full` — which `_prod_path` computes before the leg dispatch and which
feeds the sit-out blend and surprise terms — cannot carry it. Addendum 1 F1-F3's heaviest catch,
honoured by construction *and* proved positively.

## EVERY GATE

| gate | result |
|---|---|
| **fence** · 165 sit-out prices integer-identical at every rung | **PASS** (165/165 × 4 rungs) |
| **dial-0** · shipped state == stage-5 landed board through the full gate | **PASS — `13f8c2e0` byte-exact**, and structurally inert (table moved aside, board unchanged) |
| **zero-cell, absolute units, REGISTERED axis `sa`** | **rung 0.25 PASS · rungs 0.5 / 0.75 / 1.0 BREACH → STRUCK** (`FRONTIER.txt` §2). The `z` and `pr` readings are printed as disclosed secondaries and **agree on every rung** |
| **boundary** · picks 41-64 ≤0.5pp | PASS at 0.25/0.5 (0.177 / 0.354pp); **0.531pp at 0.75 and 0.708pp at 1.0 — BREACH**, endpoints NOT re-picked (`MEMO.md` §7b) |
| **boundary** · draft age 19+ | **PASS — exactly 0.000 at every rung** |
| **draft age UNKNOWN ⇒ correction ≡ 0** | **PASS** — 29 rows / 29 players, enumerated in `teach_log.txt` |
| **monotonicity** · a strictly better career never prices lower | **PASS** — min `d/dln(e)[e(1+δ)]` = **+0.023790** at rung 1.0, after the declared L-SMOOTH shrink κ = 0.912673 |
| **band [1.35,1.45]** at each table's own peak | **PASS** — whole **1.432700** (yr4), 1-20 **1.429300** (yr4) at every rung; 21-64 **1.471200** (yr6) outside but **byte-identical to the stage-5 baseline** |
| **rides** · printed always, machine STOP only ≥5pp/yr | **PASS, no STOP** — worst entry-year excess over draft day **+2.91 / +2.17 / +1.45 / +0.75 pp/yr** at rungs .25/.5/.75/1.0 against the +5.00 line |
| **FRONT-LOADED guide** (printed, not a cap) | **PASS at every rung** — yr1→2 **+0.1791 / +0.1635 / +0.1479 / +0.1322** strictly exceeds yr3→4 **+0.0856** |
| **fade shape** · measured, not decreed | raw pooled residual τ=1/2/3 = **+0.1796 / +0.0306 / −0.0134**; installed after isotonic clamp **[1, 0.170, 0, 0]**; correction at τ=2 is **17% of full**, not zero — and the horizon-non-stationarity caveat is filed (`MEMO.md` §10.4) |
| **rollover / round-by-round** | **PASS** — max observed step **0.007766** vs the surface's own max slope **0.009357** over the same step; no integer-year cliff |
| **recalculation law** | **PASS** — with year 1 frozen at 10 games, varying only YEAR-2 games moves δ across a spread of **0.024145**; nothing is stored |
| **within-class continuity** (F8, stage 5's gate imported) | **PASS** — realised slope equals the surface's own knot slope on every axis in every class |
| **convergence** (reported, never decreed) | picks 1-20 vs 21-64 year-1 gap **0.052317 → 0.027884 (s5) → 0.0214 / 0.0150 / 0.0085 / 0.0021** |
| **pick/player seam** vs `18203822`, ±2% | **PASS 1.014% / 1.926%**; **rungs 0.75 and 1.0 BREACH at 2.754% / 3.768%** |
| **fit coupling** | **NONE** — declared refit at `RL_G6_W` 0 / 0.5 / 1.0 all reproduce v0surf `9713ec6c` at sig `3e8e50de5103`. `_V0SURF_GATES` untouched |
| **machinery** | config manifest gate-mode LOADED (**64 vars**, `697da6f8`) · Guard 5 PASS · PARITY 804/804 eps=0 · NUMÉRAIRE pick-1 = 3000 · FUT-LABEL PASS · ZERO-EMPTY-CLUB PASS · BOOK↔BOARD PASS (802 shared, 2 `_pvc_exclude`) · **self-test 143 PASS / 0 FAIL** |
| **conservation** (the repair's headline gate) | measured year-1 aggregate residual **+0.136328** (F′ = **1.136328**), taught at rung 1.0 **+0.133257** — **the surface conserves the REGISTERED estimand.** Z = **0.772923**, so **\|Z−1\| = 0.227** is the measured double-count of the mandated marginal decomposition |
| **store untouched** | **PASS** — no store write in this act |

## MOVERS

| rung | board md5 | movers | up | down | board total |
|---|---|---|---|---|---|
| 0.25 | `9883420b` | 65 | 60 | **5** | 654,569 → 656,129 (+0.238%) |
| 0.5 | `b0a3369f` | 70 | 64 | **6** | 654,569 → 657,689 (+0.477%) |
| 0.75 | `f43cdf45` | 72 | 65 | **7** | 654,569 → 659,245 (+0.714%) |
| 1.0 | `a270286f` | 73 | 66 | **7** | 654,569 → 660,810 (+0.953%) |

**A CHANGE FROM THE ORIGINAL BUILD, DISCLOSED.** The original ladder had **zero** rows falling. The
registered estimand measures picks 1-10 at only **+9.0%** against **+39.2%** at picks 21-40, so the
taught nonKPP kernel goes slightly **negative at the very top of the pick axis** (base knot at pick 3
= −0.0806, where it was +0.183 before). Seven rows therefore fall at rung 1.0, **all picks 1-3, none
by more than 1.95%**: `zeke-uwland` −1.95% · `willem-duursma` −1.25% · `finn-o-sullivan` −0.44% ·
`sam-lalor` −0.29% · `jagga-smith` −0.24% · `harley-reid` −0.03% · `colby-mckercher` −0.03%. This is
the directive's own **"NEGATIVE-CAPABLE where measured over-priced"** clause operating on the pick
axis, subject to the monotonicity law, which holds. **It is NOT the KPD class markdown** — that
stays on its own sub-dial at 0 (Addendum 1 F11). At rung 0.25 five rows fall, worst −0.50%.

Largest single moves at rung 1.0: `max-kondogiannis` 355 → 660 (+85.9%) and `louis-emmett`
619 → 1094 (+76.7%); at rung 0.25, +21.4% and +19.1%. The corner-amplification finding behind those
figures is `FRONTIER.txt` §5.

## THE TAUGHT SURFACE

`g6_table.json` (md5 **`61450f0b63f725b8666a49349857b02d`**) — a frozen committed table the engine
loads, in the `lti_return_table.json` / `ycred_table.json` / `g5_table.json` precedent. Taught
**once** from the frozen matrix `b564b12e` at board `b56bbdde`, pooling the year-1/2/3 evaluation
rows (414 + 684 + 818) so the fade is endogenous.

* **kernel — the only fitted object, TWO axes** (Addendum 1): log-pick × the engine's three position
  classes, Gaussian, bandwidth grown to eff-n ≥ 35 on the value weight. `nonKPP` resolves per class
  (n=334, eff-n 38-56); **`KPP` (n=34) and `RUCK` (n=11) cannot reach eff-n 35 and are POOLED,
  DECLARED**. KPD rows are excluded from every class and ride their own sub-dial.
* **declared shape gates**: `Stau` the measured fade (isotonic non-increasing, clamped to [0,1]) ·
  `Sz` over z = log(e / entry_anchor), the demonstrated-level axis — **unchanged by the repair, and
  deliberately so** (`MEMO.md` §2 amendment note: what was false was the *claim* that its rejected
  comparator `pr` was the cross-section's axis, not the choice itself) · `Sg` cumulative career
  games · the declared pick taper 34→48 · the declared draft-age boundary.
* **the recalculation law**: every input is recomputed from the record to date at every call; `z`
  reads the PRE-correction production leg, never the corrected price, so there is no build-to-build
  feedback and no fixed point.
* **the KPD sub-dial** `RL_G6_KPD`, default 0: KPDs measure **0.6680** under the registered estimand
  (the cross-section filed **0.67**) — over-priced — and the owner's words described a bonus, so a
  −33% class markdown never rides the bonus dial. At the shipped sub-dial a KPD takes **exactly
  zero**.

## Files

`FRONTIER.txt` (read second) · `MEMO.md` (design, roads not taken, **§10 the conformance repair**) ·
`PINS.md` · `OWNER_BASIS.txt` · `PROBES.txt` + `probes_stage6.json` · `RIDES_rung*.txt` ·
`WITHIN_CLASS.txt` · `LADDER_SEAM_rung*.txt` · `KILLSWITCH_PROOF.txt` ·
`movers_rung*.csv` / `.json` · `sitout_population.json` · `teach_log.txt` · `g6_table.json` ·
`s6_rows.json` · `measure_g6.py` · `axis_probe.py` + `AXIS_PROBE.txt` · `teach_g6.py` · `rung_build.py` ·
`fit_coupling_refit_log.txt` · `selftest_full_output.txt` · `noarb/` (four matrices, four table sets,
four goal-metric sets) · `boards/` (four rung boards + `BOARD_MD5S.txt` carrying the superseded
identities) · `REPRODUCE.md`.
The workbook is `../side_by_side/board_before_after.xlsx` — stage 6 is the **seventh** stage column
(zero by construction at the shipped dial) plus its own **`stage 6 rungs`** sheet carrying all four
rungs per row with the identity `landed + Δ == rung` asserted on every cell.

---

# HISTORY — THE ORIGINAL STAGE-6 BUILD (tip `d405afb`), SUPERSEDED BY THE CONFORMANCE REPAIR

Preserved because it is a decision record: it is what was measured, what was reported to the owner
in comment `5219180436`, and what the reconciliation was run against. Nothing below is deleted.

**Files kept verbatim, `_SUPERSEDED` suffix:** `measure_g6_SUPERSEDED.py` · `teach_g6_SUPERSEDED.py`
· `g6_table_SUPERSEDED.json` · `teach_log_SUPERSEDED.txt` · `probes_g6_SUPERSEDED.py` ·
`PROBES_SUPERSEDED.txt` · `FRONTIER_SUPERSEDED.txt` · `MEMO_SUPERSEDED.md` · `README_SUPERSEDED.md`.

**Rung artifacts NOT kept as files** (22 MB of duplicate boards and matrices); their md5s ARE the
decision record and are carried in `boards/BOARD_MD5S.txt`, in `PINS.md`, and in the landing comment:

| rung | superseded board | superseded matrix | superseded landing (teaching window) | then |
|---|---|---|---|---|
| 0.25 | `e5fee49b` | `2eff80a4` | 1.005681 | FEASIBLE |
| 0.5 | `56b6c21c` | `8553acf0` | 1.020597 | FEASIBLE, disclosed |
| 0.75 | `b963e36a` | `22402f35` | 1.035515 | STRUCK |
| 1.0 | `17c96ca4` | `ca6cd25d` | 1.050429 | STRUCK ×2 |

The superseded surface `g6_table.json` md5 `5656dd8bbb19b193e1acde5063664cc5` conserved **1.0963**,
the rolling-4-year-mean statistic — 72.2% of the registered residual — and its zero-cell gate was
read on `z` and on `pr`. Its FRONTIER §4 offered the owner a road (a): rule on the zero-cell bound,
"registered by the audit at figures taken from a cross-section whose at-par cell this build
re-measures at +5.6%". **That road is WITHDRAWN.** The cell is at par (+0.39%) on its true axis under
either horizon; the challenge rested entirely on the mis-identified axis; the bound is vindicated and
if anything conservative. Roads (b) — stage 5's entry-anchor cap — and (c) — stage 7's pool leg —
stand, and carry more of the story than they did.
