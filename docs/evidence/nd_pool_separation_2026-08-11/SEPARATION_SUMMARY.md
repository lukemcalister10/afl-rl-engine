# ORDER 20 — ND / POOL SEPARATION: THE SWEEP, THE FIXES, AND THE STANDING GUARD

> **THE OWNER'S LAW:** "The ND and pool need to be entirely separated. Nothing here can impact ND pricing."

**The short answer, four sentences.**
**(1)** On the **live board price path the law already holds**: six different pool-price perturbations —
including ×3.0 and one that flattens every signed pool level to 100 — move **zero** of 668 national rows
and **zero** of 64 national pick-curve points. **(2)** On **`nd_profile`, the calibration target every
lambda is measured against, the law is BROKEN**: the same perturbations move it by **−0.3162%** and
**+0.1170%**, and **428 of 1,443 national rows'** structural values move; the arm-split fix takes that to
**exactly 0.0** with **0 rows moving**. **(3)** De-contaminating the fits has a **large one-time cost that
must not be buried**: `nd_profile` **1.0253296290 → 0.9944115616 (−3.0154%)** — it crosses below 1.0 — and
the live board moves **94f1fec5 → 1dbd1480**, national total **−0.2831%** across 279 of 668 rows.
**(4)** **`daniel-butler` is settled by the record: he is a POOL row**, and the disagreement is one
instrument contradicting its own stated principle — not a blocker, no ruling needed.

**Nothing is shipped. Nothing is baked. `data/expected_boot.json` is deliberately NOT restamped, so the
moved board cannot land silently.** Branch `build/nd-pool-separation`, cut from `origin/main` `d3d5f55`.

Pins asserted at **entry and exit**, all three **UNMOVED**:
board `94f1fec59f99c59d5890d5975c79fa9b` · store `d9a24282357cf3083b1640466e3ecd83` ·
instrument `noarb_table_338.py` `0f8220351c64c56ccfa90c60edcdfa5f`.
Pre-registration `PREREG_ORDER20.md`, **committed at `d668615` before any measurement was run**.

---

## 0. THE DISTINCTION THIS ORDER TURNED ON — declared in the pre-registration, before measuring

The order's candidate list mixes two different faults, and conflating them would let a real violation hide
behind an inert one. The pre-registration split them up front:

| | **CLASS A — LIVE PRICE-PATH CONTAMINATION** | **CLASS B — POPULATION CONTAMINATION** |
|---|---|---|
| what it is | a pool **price** or **level** is an input to a national price | a national-arm quantity is **fitted** over rows that include pool rows |
| the law | this **is** the separation law. Zero tolerance. | breaks the arm separation the owner asked for; a **pool price change may not move it at all** |
| test | perturbation → must be exactly zero | population probe → count the rows |
| a non-zero result is | a **BLOCKER** | a **one-time correction cost**, reportable in full |

**This distinction is the whole finding.** Almost every contaminated site in this engine is fitted on
**OUTCOMES** (games, season averages, establishment) — not on prices. That is exactly why the board's
price path survives a ×3.0 pool perturbation untouched while `nd_profile` does not: `nd_profile`'s strata
are built on **realised values**, which *are* prices.

---

## 1. THE SWEEP — SIXTEEN SITES, EVERY ONE NAMED

Membership is `MA.is_pool` throughout — **the engine's own predicate**, quoted not re-derived.
Instrument: `sweep/population_probe.py` → `sweep/POPULATION_PROBE.txt` / `.json` (re-runnable:
`bash sweep/run_probe.sh`). It execs the engine head exactly as the emitters do, so the counts are the
engine's own.

### 1a. VIOLATIONS — FIXED IN THIS ORDER

| # | site | file:line | what is fitted / normed | population | pool share | class | fixed |
|---|---|---|---|---|---|---|---|
| **1** | completion strata | `docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py:339` | `S[(pos,t)]`, the ratio that COMPLETES a live career | callers hand it `elig` = both arms (`profile_measure.py:66`, `derive_vs_scale.py:36`, `phase1_derive.py`) | **1,198 of 2,641 = 45.4%** | **A** | ✅ `separation/harness_armsplit.py` |
| **2** | arm membership of `daniel-butler` | `docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py:101-110`, consumed `:243` | `is_pool` / `teaches_curve` re-derived from the **slid** pick | 1 row | 1 of 1,444 | **A** | ✅ `daniel_butler/fix_matrix_membership.py` |
| **3** | **the par level surface** | `engine/forward_valuation/par_build.py:261-263` → `fit()` `:436` | `levelfn` / `level_grid` (local-linear kernel over log(pick), h=0.40), `gramp`, `base` | 1,015 national + **743 pool** | **42.26%** | B, **LIVE** | ✅ `fit_arms()` + pick routing |
| **4** | `build_pest` all-position **BAND MARGINAL** (the `K_338` shrinkage target) | `par_build.py:211` → `:228` | `pbar = bnum[b]/bden[b]` | same as #3 | **42.26%** | B | ✅ within-arm by construction |
| **5** | `BASE_RATE` play rate | `engine/forward_valuation/par_redesign.py:75-77` → `shortfall()` `:110` | median play rate per `(pos, tenure)` — **no pick axis at all**, so pool teaches national at **full weight**, not through a kernel tail | 1,015 + **743** | **42.26%** | B, **LIVE** | ✅ arm in the key |

**Why #3/#4/#5 are live and not academic:** `par_redesign.py:37` is `F = pb.fit()` — **the par surface is
re-fitted on every single build**, and `PR.par_at` prices national picks at `_merged_recover.py:312`
(`_par_prior`, into the value blend at `:580`), `:397`/`:399` (the pedigree pole), `:497` (the V0 pick
surface synthetics), `:2124` and `:2263`.

**Why the split is safe on the pick alone:** every pool entrant sits at the single index `MA.POOL_PICK`
(65) — the owner's own ruling, `rl_model.py:264-268` — and no national row ever presents that index. So
routing on the pick routes on the arm exactly, with no player argument and **no call-site changes**.

### 1b. VIOLATIONS — FOUND, MEASURED, **NOT** FIXED (each needs an owner decision it would move the board)

| # | site | file:line | what is fitted | population | pool share | why not fixed here |
|---|---|---|---|---|---|---|
| **6** | the **`#336` band tables** — `BPK`, `_pest_336`'s `pbar`, `POOL[b]`, `BASEPK_REG` | `rl_model.py:283` (`hist`), built `:456-502` | band marginals + the **gradient donor** `row[b0]*(POOL[b]/POOL[b0])` for thin national cells | 1,204 national + **770 pool** | **39.01%** | fixing it moves the board a **second** time on top of #3-#5; the two deltas must be attributed separately or neither is interpretable |
| **7** | establishment-P pick curve | `rl_model.py:1639` (`_cohP`) → `_brateP` / `_pavaP` isotonic / `_ovP` / `_grpoffP` / `pick_prior` | monotone establishment rate by pick band, + per-position offsets | 1,015 + **734** | **41.97%** | `P_HOOK=None` (`:1691`) so it is **not** in `value()`; it **is** exported as the per-player `P` field (`compute.py:18`, `rl_export.py:177`). A disclosure field, contaminated |
| **8** | pedigree prior band + the quantile GBR | `distribution_pricing.py:297` → `build_prior` `:119-131`, `build_training` `:88` | per-pick **±4 window** centre/width; GBR quantile models on `_v4_feats` | 1,448 + **1,202** | **45.36%**, and **90.8% of the pick-64 window** | **not on the live board path** — `_merged_recover` uses only `dp.v_at_peak` / `dp.SCALE_DIST`. Latent, not live |
| **9** | the conditional prior forest `cm` | `conditional_prior.py:146` → `build_cond_prior` | GBR quantile forest, feature vector includes `log(pick)` | 1,448 + **1,202** | **45.36%** | **BAKED**: `wire_redesign.py:52-56` LOADS the pinned `cm_400.pkl` and retrains only on a cold bake. The shipped forest was trained on a mixed population and **cannot be de-contaminated without a bake** |
| **10** | `R_SURF` retention surface | `_merged_recover.py:1123` | 24 hardcoded knots | producer `session_2026-07-03/d13/scripts/d13_norm_harvest.py` — **no `_pool` exclusion**, all-draftee norm mixes arms (established by ORDER 18) | — | **frozen literal**, no live channel. Historical contamination baked into the numbers |

**The single most striking number in the whole sweep** is #8's window. `distribution_pricing.build_prior`
windows on `min(effpk,70)` with `|k − pick| ≤ 4`, and every pool row sits at 65:

| national pick | national rows in its ±4 window | pool rows | **pool share of the window** |
|---|---|---|---|
| 55 | 205 | 0 | 0.0% |
| 60 | 183 | 0 | 0.0% |
| **61** | 160 | 919 | **85.2%** |
| **62** | 137 | 919 | **87.0%** |
| **63** | 114 | 919 | **89.0%** |
| **64** | 93 | 919 | **90.8%** |

This is precisely the hazard `rl_model.py:296-310` (THE SPLIT, ADDENDUM 1) names in its own words —
"collapsing the pool to ONE index at 65 **CONCENTRATED** the contamination, because every builder samples
within +/-4 effective picks" — and it says the gate must be used "at EVERY site that fits or samples the
pick curve — fixing one and leaving the others is the duplicated-assertion class." ADDENDUM 1 closed the
`rl_model` builders and **never reached `forward_valuation`.**

### 1c. CONTAMINATED POPULATIONS WITH **NO** PRICE CHANNEL — reported so the record is complete

| # | site | file:line | population | pool share | why it is not a Class A channel |
|---|---|---|---|---|---|
| **11** | LEG B un-compress references `_UC_VREFB` / `_UC_RHODEN` / `_UC_C[pos]` | `_merged_recover.py:2487` (`_uncomp_scope`) → `:2489-2519` | 561 national + **243 pool** | **30.22%** | **LIVE** (`UNCOMP_S_DEFAULT=0.10`), and `_UC_C[pos]` multiplies **every** player's production value. But both references are built from `price6()` and `rho_out()`, which are functions of **SCORING ONLY** — no pool level, no entry anchor reaches them. Class B, not A. **Measured: 0 national movers across all six perturbations.** |
| **12** | backward-board conservation factor `_f` | `rl_model.py:1756-1759` | 523 national + **232 pool** | **30.73%** | Structurally it **is** a Class A shape: `_f = Σ_v / Σ_vM` over the shared active set, applied to every national row's `vM1`/`vM2`. It is **dead on the exported board**: `rl_export.py:181-192` re-values `_vM1`/`_vM2` as `_ev(p,2025)` / `_ev(p,2024)` directly and never reads rl_model's `_vM1`. **It would become a live violation the moment any consumer read rl_model's backward board.** |

### 1d. CLEAN — checked and found correctly separated

| # | site | file:line | evidence |
|---|---|---|---|
| **13** | the pick-curve builders `build_pvc` / `build_pvc_v34` / `_natcv34` | `rl_model.py:1169`, `:1225`, `:1585` | gated by `_teaches_curve` (`:313`). Probe: **1,201 national, 0 pool. 0.00%.** ADDENDUM 1 holds |
| **14** | the V0 year-zero pick surface | `_merged_recover.py:1874-1880` | explicit `not MA.is_pool` filter, and its gates were population-corrected on 2026-08-10 |
| **15** | `_b_renorm` (the pool age renormaliser, reverse direction) | `_merged_recover.py:1847` | pool-only by construction (`if not ... q.get('_pool'): continue`) — no national leak |
| **16** | `draftAssetTotals` | board export | **NOT a violation.** It is the one shared object that moves under every perturbation, and only in `players_sum` (622,194 → 616,919 under `flat100`) — the all-player total, which is what it is for. Its **national legs `visible_1_64` (53,536) and `f5_draft_pvc` (55,753) are byte-identical** under all six perturbations |

---

## 2. THE FIXES

### 2a. `structural_values` — the stratum key gains the arm

    contaminated :  S[(pos, t)]
    arm-split    :  S[(arm, pos, t)]        arm = 'POOL' | 'ND', from the ENGINE's is_pool

`separation/harness_armsplit.py`. **The pinned harness is not modified** —
`harness_pvc_REPINNED_pass3.py` is filed evidence of a landed act and this order does not write filed
evidence. Everything but the stratum key is **imported and called** from it (`concluded`, `depth`,
`realised_full`, `sofar`), so the instrument cannot drift from the curve.

**CONTROL 1, asserted at every run:** with `split=False` this module reproduces the pinned
`structural_values` **value-for-value on all 2,641 eligible rows, 0 differences**. The measurement is
therefore of the split and of nothing else.

Nothing is deleted and no row is dropped. Both arms keep completion strata; each is taught by its own.
Thin per-arm strata degrade to the **same declared fallback** the pinned function already uses, and the
fallback share is counted and returned exactly as before.

### 2b. the par surface — fit twice, route on the pick

`engine/forward_valuation/par_build.py` and `par_redesign.py`:

- `gather(arm)` / `fit(arm)` take the arm; **`fit_arms()`** builds the national fit and attaches the pool
  fit at `F['ARM_POOL']`.
- `_arm_fit(F, pick)` routes: **picks 1-64 → the national fit; pick ≥ 65 → the pool fit.** `level_at`,
  `par_at` and the `ramp_shr` lookup all route.
- `build_pest`'s all-position band marginal is within-arm by construction (`gather` filters first).
- `par_redesign` carries its **own** `par_at`/`_lvl_safe` — the one the board actually calls — so the same
  routing is applied there. Fixing `par_build` and leaving that file reading the national leg for a pool
  player would be exactly the duplicated-assertion class.
- `BASE_RATE` gains the arm in its key; `shortfall()` selects on `MA.is_pool(p)`.

**No dial was added and no shipped default parameter was changed.** Every edit is a population filter or a
routing selector.

### 2c. `daniel-butler` — membership is the engine's, not the slide's

`daniel_butler/fix_matrix_membership.py`. See §4.

---

## 3. THE ONE-TIME DE-CONTAMINATION DELTA — IN FULL, NOT BURIED

The separation law forbids a **pool change** from moving ND. It does **not** forbid the one-time correction
of removing pool rows from an ND fit. That correction is large and it is stated here at full size.

### 3a. `nd_profile` — THE CALIBRATION TARGET MOVES −3.02% AND CROSSES BELOW 1.0

`separation/nd_profile_test.py` → `separation/ND_PROFILE_TEST.json`.

| construction | `nd_profile` (engine arm, n=1,443) | `nd_profile` (published `teaches_curve`, n=1,444) |
|---|---|---|
| **CONTAMINATED** `S[(pos,t)]` — today | **1.0253296290** | **1.0252177109** |
| **ARM-SPLIT** `S[(arm,pos,t)]` | **0.9944115616** | **0.9944131659** |
| **delta** | **−0.0309180674 (−3.0154%)** | **−0.0308045450 (−3.0047%)** |

- **428 of 1,443** national rows' structural values move.
- completion provenance: `completed` **734 → 660**; `prior_fallback_thin` **43 → 117**.
- fallback share **2.310% → 5.112%** — 74 rows can no longer be completed from their own arm's stratum and
  fall back to their own `v0` prior, the same declared fallback the pinned function already used.

**Why this matters more than its size.** `nd_profile` is the denominator of every pathway lambda
(`lambda_X = profile_X / profile_ND1-64`). The contaminated value **1.0253** says the national draft
returns slightly **more** than the entry price paid for it. The de-contaminated value **0.9944** says it
returns slightly **less**. Every pool lambda in the phase-1 repricing work is measured against this number,
and it changes sign relative to break-even. **This is a finding for the owner, not a rounding correction.**
The published `PHASE1_DERIVE.json` on `build/pool-repricing-phase1` was computed against **1.0252**.

### 3b. the live board — `94f1fec5` → `1dbd1480`

`fix/board_delta.py` → `fix/BOARD_DELTA_par_armsplit.json`, `fix/board_FIX_par_build.log`.
Only the §2b fix is in this figure; sites 6-10 are not fixed, so this is **not** the full de-contamination
cost.

| arm | n | movers | total before | total after | **delta** |
|---|---|---|---|---|---|
| **NATIONAL** (`ty=='ND'`, `ep≤64`) | 668 | **279 (41.8%)** | 624,418 | 622,650 | **−1,768 (−0.2831%)** |
| **POOL** (everything else) | 334 | **195 (58.4%)** | 123,939 | 126,244 | **+2,305 (+1.8598%)** |

National mover sizes: 175 at ≤1%, 69 at 1-5%, 30 at 5-15%, **5 above 15%**.
**The national pick curve does not move at all: 0 of 64 PVC points, 0 of 64 `picks[]`. Pick 1 = 3000, the
numéraire law holds.**

Largest national movers, named:

| player | type | pick | before → after | delta |
|---|---|---|---|---|
| Harry Dean | ND | 3 | 2815 → 2577 | **−238 (−8.45%)** |
| Ty Gallop | ND | 42 | 1355 → 1199 | −156 (−11.51%) |
| Christian Moraes | ND | 38 | 1043 → 906 | −137 (−13.14%) |
| Jacob Farrow | ND | 10 | 2734 → 2601 | −133 (−4.86%) |
| Dyson Sharp | ND | 13 | 3216 → 3091 | −125 (−3.89%) |
| Angus Clarke | ND | 39 | 680 → 555 | −125 (**−18.38%**) |
| Harvey Johnston | ND | 49 | 224 → 329 | **+105 (+46.88%)** |
| Willem Duursma | ND | 1 | 4067 → 3977 | −90 (−2.21%) |
| James Leake | ND | 17 | 476 → 563 | +87 (+18.28%) |

**The movement is NOT confined to the deep end**, and that is worth stating plainly: pick 1 and pick 3 move
too. The kernel-tail channel (log(65) at bandwidth 0.40 reaching picks ~44+) explains only part of it. The
rest is `gramp` / `ramp_shr` and `BASE_RATE`, which have **no pick axis at all** — removing pool rows from
those moves **every** pick.

**Direction:** removing pool rows from the national fit **lowers** national prices by 0.28%; removing
national rows from the pool fit **raises** pool prices by 1.86%. Each arm was being pulled toward the other.

**THE BOARD MOVES, SO NOTHING SHIPS.** `data/expected_boot.json` is deliberately **not** restamped in this
branch, so the moved board cannot land silently — a build on this branch will halt on the boot guard until
an owner bakes it. That is the intended state.

---

## 4. `daniel-butler` — SETTLED BY THE RECORD. HE IS **POOL**. NOT A BLOCKER.

Full working: `daniel_butler/DANIEL_BUTLER_VERDICT.md`.

- **The store says pool.** `type ND` · `year 2014` · **`pick 65`** · `_pickless False` · `draft_stream ND`
  · `stream_pick 65`. No null, no conflicting row, no correction note.
- **The ruling says pool.** `rl_model.py:264-268`: "A national selection at 65 or deeper is NOT on the
  curve — it enters the pool." The engine agrees at build time: `_eff 65`, `_pool True`,
  `is_pool_engine True`, `teaches_curve_engine False`, division `ND65+`.
- **The matrix says national only because of the Q-B slide.** `paddy-mccartin` is the excluded 2014 pick-1
  row, so butler's 65 slides to `pick_slid 64`, and `slid_membership()` re-derives `is_pool` from the
  **slid** pick, which `teaches_curve` consumes.
- **The emitter already forbids this, in its own header** (`emit_matrix_338.py:49-52`): "the Q-B slide is a
  fit-population device for the curve, **not an assertion that anyone was drafted a slot earlier**." It
  honours that for `_min_tenure` and breaks it for arm membership one screen later. Its own `crossers` line
  has printed `['Daniel Butler']` on every emit, including all three run for this order.

**Owned honestly:** the arm-split strata alone do **not** close this channel on principle. Under the split
butler lands in `prior_fallback_thin` and takes his own `v0 = 349.4`, which happens to be price-invariant,
so the published-population `nd_profile` came out at exactly zero drift **incidentally**. His `vpath` **does**
move under a pool perturbation (`88→47`, `68→37`). The membership fix is what closes it structurally.

Effect: the national teaching population goes **1,444 → 1,443**.

---

## 5. THE STANDING SEPARATION GUARD

`separation/run_separation_test.sh [board|full]` — committed, re-runnable, and **it is the guard for the
law, not a one-off check.**

It perturbs the **pool price primitive** — the signed per-division levels in `pvc_curve_v2.json`, the only
owner-signed input that sets what a pool entrant is worth (`rl_model.py:1419-1425`) — rebuilds the board
from a scratchpad copy of the checkout each time, and asserts **exactly zero**, not "below tolerance".

Six perturbations, four of them large: `x1.5`, `x0.5`, `x3.0`, `tilt` (RD ×2.0 / rest ×0.6 — a *reshape* of
the pool's internal mix), `rd_only` (×2.5, one division alone), `flat100` (every level := 100, destroying
the level structure entirely).

### LEG 1 — the board. **PASS, on HEAD and on the fixed engine.**

| perturbation | pool rows moved | **national rows moved** | **national curve points moved** | verdict |
|---|---|---|---|---|
| `x1.5` | 199 | **0** of 668 | **0** of 64 | HOLDS |
| `x0.5` | — | **0** | **0** | HOLDS |
| `x3.0` | 209 | **0** | **0** | HOLDS |
| `tilt` | 220 | **0** | **0** | HOLDS |
| `rd_only` | 55 | **0** | **0** | HOLDS |
| `flat100` | 221 | **0** | **0** | HOLDS |

(HEAD-engine run: `separation/prefix_HEAD/perturbations_HEAD_out.txt` + the six `*_NDDIFF.json`.)

Compared fields per national row: `v`, `vRaw`, `vP1`, `vP2`, `vM1`, `vM2` — every priced field the board
carries — plus `PVC[1..64]`, `picks[1..64]`, `pick_band_mean`, `BASEPK_REG`, `POOL`, `MIX`, `pm_pos`,
`pm_band`, `SCALE`, `REPL`, `BAND_ANCHOR`, `lensPicks`.

### LEG 2 — `nd_profile`. **FAILED ON HEAD. PASSES UNDER THE FIX.**

| perturbation | CONTAMINATED `S[(pos,t)]` | national rows moved | ARM-SPLIT `S[(arm,pos,t)]` | rows moved |
|---|---|---|---|---|
| `x3.0` | **−0.0032420145 (−0.3162%)** | **428** | **+0.0000000000** | **0** |
| `flat100` | **+0.0011996469 (+0.1170%)** | **428** | **+0.0000000000** | **0** |

**This is the violation ORDER 19 found, reproduced on a different lever, measured larger (−0.3162% vs
−0.1939%), and closed to exactly zero.**

---

## 6. PRE-REGISTRATION SCORED — 5 BREACHES OF 17, EVERY ONE OWNED

| # | prediction | outcome | verdict |
|---|---|---|---|
| P1 | ≥ 6 mixed-population sites | **16 sites enumerated, 12 of them mixed** | TRUE |
| P2 | `hist` includes pool rows | 1,204 national / **770 pool = 39.01%** | TRUE |
| P3 | `par_build.gather()` unfiltered | 1,015 / **743 = 42.26%** | TRUE |
| P4 | curve builders already clean | **1,201 national, 0 pool** | TRUE |
| P5 | `R_SURF` frozen, no live channel | hardcoded literal `_merged_recover.py:1123` | TRUE |
| P6 | ≥ 1 site not anticipated | **four**: `BASE_RATE` (#5), `conditional_prior` (#9), LEG B refs (#11), the backward conservation factor (#12) | TRUE |
| P7 | a #336/BASEPK fix moves national prices > 0.01% | **NOT TESTED** — site #6 was not fixed | **BREACH (unresolved)** |
| P8 | combined national board move between 0.1% and 5.0% | **−0.2831%** from the par fix alone | TRUE (within band, but on a partial fix) |
| P9 | `nd_profile` moves non-zero and < 1.0% absolute | **−3.0154%** | **BREACH** — off by a factor of three, and in the direction that matters: it crosses below 1.0 |
| P10 | no shipped default dial changed | none changed; every edit is a population filter or a router | TRUE |
| P11 | the record settles `daniel-butler` | it does, unambiguously | TRUE |
| P12 | he is a pool row | he is | TRUE |
| P13 | the test FAILS on HEAD; specifically `nd_profile` moves | `nd_profile` moved (−0.3162%) — **but the board leg PASSED on HEAD at exactly zero, which this seat did not predict** | **PARTIAL BREACH** |
| P14 | after the fixes, exactly zero everywhere | exactly `0.0` on `nd_profile` and 0 rows; 0/668 and 0/64 on the board | TRUE |
| P15 | `daniel-butler` is the only reachable crosser, and removing him closes the channel entirely | he **is** the only crosser — but removing him does **not** close the channel: **428** national rows move through the shared **strata**, which is a different and far larger mechanism | **BREACH** — the premise carried over from ORDER 19 was wrong about the size |
| P16 | ≥ 4 perturbations, one ≥ 50%, committed and re-runnable | **six**, three ≥ 50% (`x3.0`, `x0.5`, `flat100`), committed | TRUE |
| P17 | the live board WILL move | `94f1fec5` → `1dbd1480` | TRUE |

**Breaches: P7, P9, P13, P15 — and P8 passes only on a partial fix, which is recorded as a qualified pass
rather than a clean one.** The instructive breach is **P15**: this seat inherited ORDER 19's framing that
`daniel-butler` was the material cross-arm channel. He is one row. The **strata** are 428.

---

## 7. WHAT IS UNRESOLVED OR BLOCKING

**Nothing in this order is a blocker in the "stop and ask" sense — the separation test has no non-zero
residue anywhere.** What follows are open items that need an owner decision, not seat judgement:

1. **THE BOARD MOVED, SO THE FIX IS NOT SHIPPED.** `94f1fec5 → 1dbd1480`, national −0.2831% across 279
   rows. Per the order this seat stops at the PR. `data/expected_boot.json` is **not** restamped.
2. **`nd_profile` −3.02% is a repricing-grade finding, not a cleanup.** It crosses below 1.0. Every lambda
   on `build/pool-repricing-phase1` was measured against the contaminated **1.0252**. Whether phase 1 is
   re-derived against **0.9944** is an owner decision and is **not** made here.
3. **Sites 6-10 are found and measured but NOT fixed** (`#336` band tables 39.01% pool; establishment-P
   41.97%; `distribution_pricing` 45.36% and 90.8% of the pick-64 window; `conditional_prior` 45.36%,
   **baked into `cm_400.pkl`**; `R_SURF`, frozen). Each moves the board again, and #9 and #10 cannot be
   corrected without a bake.
4. **Site #12 is a live Class A shape that is currently unreachable.** The backward-board conservation
   factor mixes arms and would move national `vM1`/`vM2` — it is inert only because `rl_export.py:181-192`
   re-values those fields from `ev()` directly. Any future consumer that reads rl_model's backward board
   reopens it. It should be fixed even though it does not currently fire.
5. **The `daniel-butler` membership fix lives in a staged patch**, because the canonical emitter is filed
   evidence. Landing it in `emit_matrix_338.py` is a one-line edit for whoever owns that file.
6. **The board leg of the guard is a 6-point empirical zero, not a proof.** It is strong (three ≥50%
   perturbations, one that destroys the level structure) and §1c gives the *mechanism* for why the two
   candidate Class A channels cannot fire — both are built from scoring, not prices. But it is evidence,
   and it is labelled as evidence.

---

## 8. REPRODUCTION

    export PATH="/root/rl_venv312/bin:$PATH"
    cd <this worktree>

    # the sweep (~2 min)
    bash docs/evidence/nd_pool_separation_2026-08-11/sweep/run_probe.sh

    # the standing guard, board leg (~7 min: 1 base + 6 perturbed boards)
    bash docs/evidence/nd_pool_separation_2026-08-11/separation/run_separation_test.sh board

    # the standing guard, both legs (~14 min: adds 3 matrix emits at ~2 min each)
    bash docs/evidence/nd_pool_separation_2026-08-11/separation/run_separation_test.sh full

    # the one-time board delta (needs a board built from origin/main and one from this branch)
    python3 docs/evidence/nd_pool_separation_2026-08-11/fix/board_delta.py <BEFORE.json> <AFTER.json>

`build_board_o20.sh` and `emit_matrix_o20.sh` **copy** the tree with `tar` into `$SP` rather than running
`git worktree add` against `/home/user/afl-rl-engine`, because this order may not touch the primary
checkout. They restamp the config hash and boot identities in the **copy** so the guards stay armed, run
the build, copy the artifact out, and delete the copy. **The checkout's `data/rl_build/rl_app_data.json`
and `engine/rl_after/rl_app_data.json` are never written.**

Board md5s: `origin/main` → **`94f1fec59f99c59d5890d5975c79fa9b`** (reproduced exactly, twice);
this branch → **`1dbd1480a34c7823f330273211cbb76a`** (reproduced exactly, twice).
