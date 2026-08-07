# 334 stage B / STAGE 6 — THE CONDITIONED DEVELOPMENT CORRECTION (established leg)

Branch `landing/334-stage-b`, built on the stage-5 landing (board `13f8c2e0`, tip `0dde8e8`).
Nothing merges to main; no PR; no tag. **Adoption is the owner's word, and so is the rung.**

> **READ `FRONTIER.txt` SECOND.** Two registered gates bind on the upper half of the ladder. What
> they cost against the owner's ruled range is stated there in one sentence, with the three roads
> out — all three of which are the owner's, not this seat's.

## THE SHIPPED STATE

**`RL_G6_W = 0` and `RL_G6_KPD = 0`.** The shipped board is the stage-5 landing
`13f8c2e0240600733a5fb42414510445`, **byte-exact through the full gated build**, and the correction is
*structurally* inert — with the dials at 0 the branch is not taken and `g6_table.json` is never opened
(proved by rebuilding with the table moved aside; `KILLSWITCH_PROOF.txt`). Addendum 1 F9/F10: the
default protects the owner's ruling from being anchored by a seat that has already picked a rung.
**This seat makes NO recommendation on the rung.**

## THE FOUR-RUNG LANDING — BOTH BASES, full cohort leading (ruling 5217177098)

| population (year 1) | n | pre-s5 | s5 LANDED | rung 0.25 | rung 0.5 | rung 0.75 | rung 1.0 |
|---|---|---|---|---|---|---|---|
| **FULL COHORT ND+pool 2004-2025** | 2517 | 0.908179 | 0.946050 | **0.958020** | **0.970017** | **0.982021** | **0.994018** |
| ND 1-64, 2004-2025 | 1383 | 0.949994 | 0.988526 | 1.003718 | 1.018943 | 1.034177 | 1.049403 |
| pool routes, 2004-2025 | 1134 | 0.752800 | 0.788214 | 0.788214 | 0.788214 | 0.788214 | 0.788214 |
| ND 1-64, 2004-2022 (**teaching window**) | 1197 | 0.950431 | 0.990805 | 1.005681 | 1.020597 | 1.035515 | 1.050429 |
| ND picks 1-20, 2004-2022 | 377 | 0.970665 | 1.001589 | 1.014677 | 1.027820 | 1.040960 | 1.054100 |
| ND picks 21-64, 2004-2022 | 820 | 0.918348 | 0.973706 | 0.991419 | 1.009145 | 1.026882 | 1.044608 |

**The pool leg takes ZERO at every rung, by construction** — the declared pick taper zeroes the pool
index (effpk 65). The pool is stage 7's, on its own measurement (#334 comment 5217529020). The
full-cohort basis therefore never reaches 1.04, which Addendum 1 F4 required printed explicitly, and
**the basis question goes to the owner** — this seat does not resolve it.

## THE ESTIMAND, AND THE STATISTIC PRE-REGISTERED BESIDE IT

The estimand is the **value-weighted aggregate** F′ on the year-1 established leg: **1.0963**
(under-priced by 9.6%). The **median** F′ is **0.9632** — the *typical* year-1 established player is
already priced **4% ABOVE** his own realised discounted future, and only **47.6%** of them out-earn
even the uncorrected price. **The residual is carried by a right tail.**

| rung | corrected aggregate F′ | corrected **median** F′ | typical player over-priced by | fraction who out-earn the corrected price |
|---|---|---|---|---|
| 0 (shipped) | 1.0963 | 0.9632 | 4% | 47.6% |
| 0.25 | 1.0700 | 0.9219 | 8% | 45.4% |
| 0.5 | 1.0449 | 0.8969 | 11% | 44.4% |
| 0.75 | 1.0209 | 0.8743 | 14% | 42.0% |
| 1.0 | 0.9981 | **0.8331** | **20%** | 40.3% |

**THE MEDIAN-NEUTRAL RUNG IS BELOW ZERO.** No positive rung improves the typical player's honesty;
every rung worsens it while improving the value-weighted aggregate. That is the whole of the
tail-vs-typical tension the directive named as the central pub-test item, stated as a number.

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
| **zero-cell, absolute units** | **rung 0.25 PASS both readings · rung 0.5 PASS on the surface's own axis, +0.08pp over on the `pr` reading · rungs 0.75 and 1.0 BREACH → STRUCK** (`FRONTIER.txt` §2) |
| **boundary** · picks 41-64 ≤0.5pp | PASS at 0.25/0.5/0.75 (0.129 / 0.258 / 0.387pp); **+0.516pp at rung 1.0, 0.016pp over — disclosed, endpoints NOT re-picked** |
| **boundary** · draft age 19+ | **PASS — exactly 0.000 at every rung** |
| **draft age UNKNOWN ⇒ correction ≡ 0** | **PASS** — 29 rows / 29 players, enumerated in `teach_log.txt` |
| **monotonicity** · a strictly better career never prices lower | **PASS** — min `d/dln(e)[e(1+δ)]` = **+0.053337** at rung 1.0, after the declared L-SMOOTH shrink κ = 0.693842 |
| **band [1.35,1.45]** at each table's own peak | **PASS** — whole **1.432651** (yr4), 1-20 **1.429314** (yr4) at every rung; 21-64 **1.471250** (yr6) outside but **byte-identical to the stage-5 baseline** |
| **rides** · printed always, machine STOP only ≥5pp/yr | **PASS, no STOP** — worst entry-year excess over draft day **+3.11 / +2.56 / +2.02 / +1.49 pp/yr** at rungs .25/.5/.75/1.0 against the +5.00 line |
| **FRONT-LOADED guide** (printed, not a cap) | **PASS** — yr1→2 **+0.1351** strictly exceeds yr3→4 **+0.0856** at rung 1.0 |
| **fade shape** · ≈0 at year-2-evaluation states BY MEASUREMENT | **PASS** — raw pooled residual τ=1/2/3 = **+0.1284 / −0.0447 / −0.1690**; installed after isotonic clamp **[1, 0, 0, 0]**; correction at τ=2 is **0.0000** |
| **rollover / round-by-round** | **PASS** — max observed step equals the surface's own max slope exactly; no integer-year cliff; the fade is linear in the continuous clock |
| **recalculation law** | **PASS** — with year 1 frozen at 10 games, varying only YEAR-2 games moves δ across a spread of **0.008561**; nothing is stored |
| **within-class continuity** (F8, stage 5's gate imported) | **PASS** — realised slope equals the surface's own knot slope on every axis in every class |
| **convergence** (reported, never decreed) | picks 1-20 vs 21-64 year-1 gap **0.052317 → 0.027884 (s5) → 0.023 / 0.019 / 0.014 / 0.009** |
| **pick/player seam** vs `18203822`, ±2% | **PASS 0.605% / 1.159% / 1.739%**; **rung 1.0 BREACH at 2.338%** |
| **fit coupling** | **NONE** — declared refit at `RL_G6_W` 0 / 0.5 / 1.0 all reproduce v0surf `9713ec6c` at sig `3e8e50de5103`. `_V0SURF_GATES` untouched |
| **machinery** | config manifest gate-mode LOADED (**64 vars**, `697da6f8`) · Guard 5 PASS · PARITY 804/804 eps=0 · NUMÉRAIRE pick-1 = 3000 · FUT-LABEL PASS · ZERO-EMPTY-CLUB PASS · BOOK↔BOARD PASS · **self-test 143 PASS / 0 FAIL** |
| **conservation** (bleed + double-count in one line) | Z = **0.715015**, so **\|Z−1\| = 0.285** is the measured double-count of the mandated marginal decomposition |
| **store untouched** | **PASS** — no store write in this act |

## MOVERS

| rung | board md5 | movers | up | down | board total |
|---|---|---|---|---|---|
| 0.25 | `e5fee49b` | 41 | 41 | **0** | 654,569 → 655,510 (+0.144%) |
| 0.5 | `56b6c21c` | 43 | 43 | **0** | 654,569 → 656,452 (+0.288%) |
| 0.75 | `b963e36a` | 44 | 44 | **0** | 654,569 → 657,391 (+0.431%) |
| 1.0 | `17c96ca4` | 44 | 44 | **0** | 654,569 → 658,330 (+0.575%) |

Every mover at every rung moves **UP**; **zero rows fall**. Largest single moves at rung 1.0:
`max-kondogiannis` 355 → 594 (+67.3%) and `louis-emmett` 619 → 1024 (+65.4%); at rung 0.25, +16.6%
and +16.3%. The corner-amplification finding behind those figures is `FRONTIER.txt` §5.

## THE TAUGHT SURFACE

`g6_table.json` (md5 `5656dd8bbb19b193e1acde5063664cc5`) — a frozen committed table the engine loads,
in the `lti_return_table.json` / `ycred_table.json` / `g5_table.json` precedent. Taught **once** from
the frozen matrix `b564b12e` at board `b56bbdde`, pooling the year-1/2/3 evaluation rows
(414 + 684 + 818) so the fade is endogenous.

* **kernel — the only fitted object, TWO axes** (Addendum 1): log-pick × the engine's three position
  classes, Gaussian, bandwidth grown to eff-n ≥ 35 on the value weight. `nonKPP` resolves per class
  (n=334, eff-n 52-205); **`KPP` (n=34) and `RUCK` (n=11) cannot reach eff-n 35 and are POOLED,
  DECLARED**. KPD rows are excluded from every class and ride their own sub-dial.
* **declared shape gates**: `Stau` the measured fade (isotonic non-increasing, clamped to [0,1]) ·
  `Sz` over z = log(e / entry_anchor), **the demonstrated-level axis, chosen over `bestlvl/par` by
  the printed axis probe** (value-weighted R² 0.072 vs 0.024) and because it — and only it —
  reproduces the owner's "already priced in" cell (that cell reads **0.92** on this axis) ·
  `Sg` cumulative career games · the declared pick taper 34→48 · the declared draft-age boundary.
* **the recalculation law**: every input is recomputed from the record to date at every call; `z`
  reads the PRE-correction production leg, never the corrected price, so there is no build-to-build
  feedback and no fixed point.
* **the KPD sub-dial** `RL_G6_KPD`, default 0: KPDs measure **0.7484** (over-priced) and the owner's
  words described a bonus, so a −25% class markdown never rides the bonus dial. At the shipped
  sub-dial a KPD takes **exactly zero**.

## Files

`FRONTIER.txt` (read second) · `MEMO.md` (design, roads not taken, the two ordering defects) ·
`PINS.md` · `OWNER_BASIS.txt` · `PROBES.txt` + `probes_stage6.json` · `RIDES_rung*.txt` ·
`WITHIN_CLASS.txt` · `LADDER_SEAM_rung*.txt` · `KILLSWITCH_PROOF.txt` ·
`movers_rung*.csv` / `.json` · `sitout_population.json` · `teach_log.txt` · `g6_table.json` ·
`s6_rows.json` · `measure_g6.py` · `axis_probe.py` · `teach_g6.py` · `rung_build.py` ·
`fit_coupling_refit_log.txt` · `selftest_full_output.txt` · `noarb/` (four matrices, four table sets,
four goal-metric sets) · `boards/` (four rung boards) · `REPRODUCE.md`.
The workbook is `../side_by_side/board_before_after.xlsx` — stage 6 is the **seventh** stage column
(zero by construction at the shipped dial) plus its own **`stage 6 rungs`** sheet carrying all four
rungs per row with the identity `landed + Δ == rung` asserted on every cell.
