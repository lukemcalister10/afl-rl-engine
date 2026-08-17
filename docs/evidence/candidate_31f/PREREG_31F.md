# PREREG 31-F — THE COMPLETION. FILED BEFORE ANY 31-F QUANTITY EXISTS.

**ORDER 31-F completion seat · `land/order-29` · brief = #334 comment 5310576233 · original spec #334
comment 5310338355 · basis resolution #334 comment 5310447449.**

> **WHAT EXISTED WHEN THIS FILE WAS WRITTEN.** Only the **F0 controls**, which are controls and not
> quantities of this order:
>
> | control | result |
> |---|---|
> | untouched tree, `RL_O31=1` | **`d9a57cc8770802b83c1264a08356fb60`** — the ORDER-31 candidate board reproduces |
> | untouched tree, dial unset | **`9298203135202a0c707bb0977ba38c31`** — the Step-2 board reproduces byte-exact |
>
> Plus the **census of the shrink rule's own inputs** (§1.1) — population counts and the estimator's
> effective `n`, which are *inputs the rule reads*, not outputs of it. They are printed here in the open so
> that the rule below is fully specified before it is run. **No head-fixed surface, no re-derived
> constant, no 31-F price and no 31-F board existed when this file was committed.**

Every prediction is numbered **F#**, carries a band or a binary verdict able to fail, and is scored by
number in `SHIPPING_PACKET_31.md`. **Nothing in this file is edited after a reading.**

---

## 1 · THE HEAD FIX — THE RULE, DECLARED IN FULL BEFORE IT RUNS

### 1.1 · What is wrong, and the inputs that say so

The shipped `nd_v0.posv` is built as `posv_g(p) = relat_g(p) · curve(p)`, and ORDER 30B Step 1 enforced
per-position monotonicity on it by **weighted PAVA → floor 100 → the −1 ordering tiebreak → one
conservation scalar** (`o30b_v0refit.py`). PAVA pools adjacent violators. Where the raw positional
relativity is estimated on **almost no data**, it is noise, and PAVA pools that noise *backward onto the
head*. The known case, from the committed `V0REFIT30B.json`:

| RUCK pick | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| raw `posv` in | **1,967.7** | 4,221.0 | 4,422.8 | 3,790.3 |
| shipped `posv` out (PAVA-pooled) | **3,477.2** | 3,476.2 | 3,475.3 | 3,474.3 |

**The census of the estimator's own effective `n`** (`o26b_loclin.kernel_loclin`, the same call the surface
is built with), and the hard per-pick cohort counts, on the ORDER-28 ND fit population (1,142 rows):

| pos | rows | eff-n p1 | p2 | p3 | p4 | p10 | p20 | p30 | p40 | pick-blind level |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| MID | 422 | 20.36 | 35.20 | 36.57 | 36.26 | 35.95 | 41.87 | 49.29 | 57.69 | 1.4647 |
| SD | 180 | 1.20 | 2.69 | 6.18 | 10.95 | 36.44 | 35.38 | 35.23 | 36.08 | 0.6050 |
| SF | 212 | 1.87 | 4.59 | 8.68 | 13.76 | 35.55 | 35.76 | 36.04 | 38.51 | 0.5441 |
| KPD | 125 | 1.78 | 4.59 | 8.93 | 13.56 | 32.18 | 33.21 | 31.51 | 35.23 | 0.7142 |
| KPF | 143 | 5.80 | 12.37 | 16.83 | 21.11 | 35.19 | 37.44 | 37.76 | 39.07 | 0.8680 |
| **RUCK** | **60** | **1.73** | **2.79** | **3.48** | **4.32** | **13.04** | **15.22** | **16.06** | **15.31** | **1.4375** |

Hard cohort counts at picks 1–5 are `RUCK 1,1,1,0,1` and `SD 1,0,0,2,1` — **the positional head is
unmeasured for four of the six positions**, and RUCK is thin *everywhere*, not only at the head.

### 1.2 · THE SHRINK RULE (declared; symmetric; applied identically to all six positions)

Let `relat_g(p) = posv_g(p) / curve(p)` be the pre-refit positional relativity (the artifact's own object),
`n_gp` the **LL estimator's own effective n** for position `g` at pick `p`, and `K = 15` — **this
project's own `K_SHRINK`**, the constant `DERIVE.json::pool.K` already used for the pool cells and for the
pathway ladders. Then, at every pick and for every position:

```
w_gp        =  n_gp / (n_gp + K)                                    the credibility weight
relat'_g(p) =  w_gp · relat_g(p)  +  (1 − w_gp) · 1.0               K-toward-the-all-in relativity
relat"_g(p) =  relat'_g(p) / Σ_h share_h(p) · relat'_h(p)           per-pick renormalisation
posv*_g(p)  =  relat"_g(p) · curve(p)
```

**The shrink target is `1.0` — the all-in curve's own relativity.** That is the exact null of "this pick
carries no position-specific evidence", and it is the **centroid of the per-pick reconciliation identity**
`Σ_g share_g(p)·relat_g(p) = 1`, which the artifact already enforces. The renormalisation step restores
that identity **exactly** at every pick, so the shrink cannot move the all-in curve: **the all-in ladder,
the pooled head `H`, and therefore the numéraire `s`, are untouched by construction.**

**THE ALTERNATIVE READING IS REJECTED, AND WHY, IN ADVANCE.** The other natural target is the position's
own pick-blind level `R_g` (last column above). It is rejected because `R_RUCK = 1.4375` is itself
manufactured by the same defect — RUCK's fitted relativity runs 1.6–2.6 across picks 16–40 on effective
`n` of 13–16 — so shrinking toward it would **raise** the RUCK head rather than lower it, inverting the
direction the brief rules. Shrinking toward a contaminated centre is not a fix. This is declared here,
before the run, so it cannot be presented later as a discovery.

`posv*` is then fed through the **committed `o30b_v0refit.py` pipeline verbatim** — weighted PAVA → floor
100 → the −1 ordering tiebreak → one published conservation scalar λ — with no stage altered.

### 1.3 · Predictions on the head fix

**F1 · ALL SIX POSITIONS AUDITED, ONE RULE.** The same `K`, the same target, the same estimator's
effective `n`, at every one of the 384 cells. **Fails** if any position is exempted, if any cell takes a
hand-set value, or if fewer than six positions are audited.

**F2 · RUCK'S HEAD COMES DOWN.** `posv_RUCK(1)` falls from the shipped **3,477.2** to **inside
[2,300 , 3,050]** — i.e. at or below the all-in curve's own pick-1 value of 3,000, where it was never
credible to sit on effective `n = 1.73`. **Fails** outside that band.

**F3 · RUCK CARRIES THE LARGEST HEAD CORRECTION OF THE SIX**, measured as |Δ| at pick 1. **Fails** if some
other position moves more at pick 1.

**F4 · THE FIX IS SYMMETRIC AND AT LEAST ONE OTHER POSITION MOVES UP.** SF's pick-1 cell (hard `n = 1`,
effective `n = 1.87`, relativity **0.270** — the *opposite* anomaly) moves **UP**, to inside
[1,900 , 3,000]. SD's pick-1 cell (effective `n = 1.20`, the thinnest of all 384) also moves up. **Fails**
if the rule is applied one-sidedly, or if SF(1) lands outside the band.

**F5 · MID MOVES LEAST AT THE HEAD.** MID is the only position with a genuinely sampled head (effective
`n = 20.36` at pick 1). **PREDICTION: |Δ|/posv at MID pick 1 is under 25%, and is the smallest relative
pick-1 move of the six.**

**F6 · CONSERVATION IS EXACT AND THE RULED PROPERTIES SURVIVE.** After the pipeline: the share-weighted
grand total equals `Σ_{p=1..64} curve(p) = 47,315` with `|drift| < 1e-6`; **floor 100 holds at pick 64 for
all six positions**; **per-position monotonicity holds (`ascents` = 0)**; and the **per-pick reconciliation
residual is PRINTED in full**, with `max |ratio − 1| ≤ 0.25`. **Fails** on any breach; the residual being
*absorbed* rather than printed is itself a failure.

**F7 · THE NAMED HEAD-FIX MOVER CLASSES, PREDICTED BEFORE ANY NEW `v0` EXISTS.**
- **RUCK rows fall.** Named in advance: `toby-conway` (ND pick 24, `cg` 6 — the brief's named row),
  `max-knobel` (ND pick 42, **day-0**), `jacob-molier` (ND pick 52, **day-0**), `will-green`,
  `taylor-goad`, `harry-barnett`, `mitchell-edwards`, `nick-bryan`, `luke-jackson` (pick 3),
  `timothy-english`, `dante-visentini`.
- **SF and SD rows at shallow picks rise.** Named in advance: `jack-martin` (SF pick 3),
  `isaac-kako` (SF pick 13), `jacob-farrow` (SD pick 10).
- **MID rows move slightly down.** Named in advance: `willem-duursma` (pick 1), `harry-sheezel` (pick 3),
  `josh-smillie` (pick 7, day-0), `dyson-sharp` (pick 13), `harry-demattia` (pick 25, day-0).
- **Pool rows carry NO head-fix move at all** — pool `v0` comes from `pool_v0.cells`, which this fix does
  not touch. **Fails on a single point of head-fix movement on a pool row.**

**F8 · NO UNDECLARED MOVER CLASS.** Every row that moves against the ORDER-31 board `d9a57cc8` is
attributable, to the point, to one or more of: **the head fix · the re-derived fade · the re-derived
persistence β · the re-calibrated ρ · β_pool · the position gate · the numéraire**. **Fails** if any
row's move fails to reconcile to the sum of its attributed mechanisms at ±1 point.

---

## 2 · THE RE-DERIVATION (R1 RULER DISCIPLINE — the measurement travels with its ruler)

The fade, the persistence β and the ρ backbone calibration were all measured **against the pre-fix `v0`
object**. The head fix moves that object, so all three are re-run on the head-fixed surface with their
**committed harnesses byte-identical**, and the drifts are reported.

**F9 · THE SITTER FADE RE-DERIVED (the 30A-2 harness, byte-identical).** The ruled listed-conditional row
`D(2)/D(3)/D(4+) = 0.5502 / 0.2628 / 0.3460` is re-computed on head-fixed `v0`s, **flat deep end
re-computed per the owner's Step-2 amendment**. **PREDICTION: each of the three drifts by less than
0.060 absolute.** **Fails** outside that band.

**F10 · THE FADE STAYS USABLE — THE STOP CONDITION.** Every wired `D` satisfies `0 < D ≤ 1` and depth 2
remains a **fade** (`D(2) < 1`). **If any re-derived value breaks a ruled property, THE BUILD STOPS AND
THE SEAT REPORTS** — it does not repair it.

**F11 · THE PERSISTENCE β RE-DERIVED (the 30B-M harness).** The five band midpoints
`2.5 / 10.5 / 25.5 / 53.0 / 85.5 → 0.2968 / 0.3623 / 0.2233 / 0.1531 / 0.0201` are re-measured against the
head-fixed `v0`. **PREDICTION: each drifts by less than 0.100 absolute; β(2.5) stays inside [0.20, 0.45];
the monotone projection remains non-increasing and non-negative.**

**F12 · THE ρ BACKBONE RE-CALIBRATION.** `ρ(g) = 1 − exp(−(g/τ)^b)` is re-fitted against the R1 cumulative
backbone knots. **PREDICTION: the RMS residual stays at or under the Step-3 bar of 0.05, `ρ(0) = 0`
exactly, and `τ` lands inside [15, 45].**

**F13 · THE PRINTED-DAY-0 IDENTITY RE-VERIFIES AT 89 OF 89, TOLERANCE 0**, against the **head-fixed**
`v0` cells. The *values* move for the 46 ND day-0 rows and are byte-identical for the 43 pool day-0 rows
except through the re-derived fade. **Fails on a single row of the 89.**

**F14 · THE DAY-0 NAMED ROWS, BANDED BLIND.** Post-head-fix, pre-numéraire, on the final board:
`josh-smillie` (MID 7) in **[380 , 500]** · `harry-demattia` (MID 25) in **[240 , 320]** ·
`max-knobel` (RUCK 42) in **[140 , 290]** — knobel is the row the head fix is *for*, and he must fall.

---

## 3 · β_POOL (the brief's item 2)

**F15 · β_pool IS DERIVED BY THE TRANSPLANTED PANEL CONSTRUCTION**, not by analogy: the committed 30B-M
panel harness is `exec`'d and only the population and the `v0` object are swapped (the same discipline
that produced `D_pool`). **CONTROL, able to fail: the transplanted instrument re-derives the ND pooled β
row to a deviation of ≤ 0.01 at every band.**

**F16 · β_pool AT THE SHALLOW BAND lands inside [0.00 , 0.70]** at the 2.5-game midpoint, with `n` and
dispersion published on every cell, thin pathways **K-shrunk (K = 15) toward the pooled pool row with the
borrowing printed per cell**, MSD first-season-is-season-1 on games-of-12, and listed-conditioning applied
where resolvable.

**F17 · THE DEPTH-3 POOL-FADE INVERSION STAYS UNWIRED.** `D_pool(3) = 2.2635` on `n = 17` with 45%
censored remains **published and not wired**, under the pre-declared rule *wire the deepest cell that
clears the n floor **and is a fade** (`D ≤ 1`), then hold flat*. It is filed as an **OWED OWNER
CONFIRMATION** in the packet. Binary; **fails** if it is wired, or if it is dropped from the packet.

**F18 · Φ ON POOL ROWS IS STATED, NOT ASSUMED.** The packet states explicitly whether the pool panel
supports the 30B-C Φ conditioning by the same construction, or whether pool rows carry an **ND-borrowed**
or **unconditioned** Φ. Binary; **fails by omission**.

---

## 4 · THE POSITION GATE (original Step 4)

**F19 · EVERY ACTIVE ROW'S POSITION KEY IS AUDITED** against the store's own position evidence, and the
owner's **proportionate Baker proposal** is applied where reachable. Counts published: rows audited · rows
reachable · rows re-keyed · rows flagged as residual. **Fails** if any residual is papered over rather
than named.

**F20 · THE GATE IS PRICE-BOUNDED.** **PREDICTION: fewer than 40 rows are re-keyed**, because the position
key drives only the *bar* and the *v0 cell*, and the store's position field is the same field the board has
always priced against. Band: **0–40 re-keyed rows.**

---

## 5 · THE NUMÉRAIRE RE-PIN (original Step 5)

**F21 · THE RE-PIN RUNS THROUGH `_load_numeraire`, PICKS AND PLAYERS TOGETHER, AND THE E6 ASSERTS HOLD.**
`|published_pin / H − s| < 1e-9` on the final artifact; `RL_PICK1` agrees with the published pin; the
exact `s` is reported old → new at full precision.

**F22 · `s` IS PREDICTED UNMOVED, AND THE REASON IS DECLARED BEFORE IT IS MEASURED.** `s = published_pin /
pooled_head_pre_scale`, and `pooled_head_pre_scale = 3191.178971663107` is the **all-in ladder's**
pre-anchor head. The head fix is a **re-split of the all-in curve across positions under an exact
renormalisation and an exact conservation scalar** — it cannot move the all-in ladder. **PREDICTION:
`s_new = s_old = 0.9400914291048137` EXACTLY, `|s_new/s_old − 1| = 0`, and the board carries no numéraire
scaling.** **Fails** on any movement in the 16th decimal — and a movement would mean the head fix leaked
into the all-in ladder, which is itself the failure.

---

## 6 · THE ASSERT WALL ON THE FINAL BOARD

**F23 · CONTINUITY (build-failing).** `lim_{g→0+} price(g) = price(0)` to better than **1e-6 relative** on
every continuity row (the ORDER-31 reading was 3.9e-08); monotone-in-evidence where the held output is at
or above the position bar; no dead zones; the CONTINUITY artifact emitted.

**F24 · COMPLETENESS (build-failing).** The 26A forbidden set is unreachable from any printed price; the
audit is committed.

**F25 · CELL COVERAGE 100.0%**, zero fallbacks, zero halts.

**F26 · RECONCILIATION.** `production + pedigree == price` at ±1 point for **0 of 804** failures.

---

## 7 · THE INSTRUMENTS (original Step 7)

**F27 · YEAR-0 IS THIS CANDIDATE'S OWN ENTRY LAW**, per the filed supervisor resolution (#334 comment
5310447449): a **declared re-point** of the `emit_matrix_29c` lineage's year-0 source and its
`RL_DAY0_FINAL`-class guard, the header log appended, and **the guard re-proven FAIL-CLOSED at 89 of 89
against THIS board's actual day-0 prints**. Binary, able to fail on a single row.

**F28 · BOTH COHORT INSTRUMENTS + MARK-PATH + REVERSE NO-ARB ARE EMITTED**, as the disclosed copies, with
matrix-identity literals re-pointed **only as declared**. Year paths as **% of entry with yr0 = 100**,
**LIVE vs CANDIDATE side by side**, plus the by-arm yr1/yr4 view and the year-1/2/3 class views with named
rows.

**F29 · THE NO-ARB BANDS.** **PREDICTION: on the candidate's own-entry-law basis, every cohort cell with
`n ≥ 8` has a year-1 mark inside [55% , 145%] of entry, and no cell is negative.** **Fails** outside.

**F30 · EVERY MARGIN IS PRINTED WITH ITS SIGN**, including the negative ones, and the count of negative
margins is stated rather than summarised away.

---

## 8 · BOARD TOTALS

**F31 · THE FINAL CANDIDATE BOARD TOTAL lands inside `[600,000 , 720,000]`.** Anchors: live **752,429** ·
Step-2 **706,672** · the ORDER-31 board **664,058**. The head fix cuts the inflated RUCK pedigree legs and
lifts the thin SF/SD/KPD heads; the two partly offset, and the re-derived constants move it either way.

**F32 · THE HEAD FIX'S OWN BOARD COST, ISOLATED, lands inside `[−25,000 , +15,000]`** against `d9a57cc8`
before the re-derived constants are applied.

---

## 9 · CONTROLS (all mandatory, all able to fail)

| # | control | verdict |
|---|---|---|
| **F33** | **entry byte-identity** | `d9a57cc8` with `RL_O31=1` and `92982031` dial-off on the untouched tree. **CLOSED AT FILING TIME — PASS.** |
| **F34** | **deterministic double-build** | the final board built twice, byte-identical md5. |
| **F35** | **dial-off byte-identity** | with `RL_O31` unset, the final tree reproduces `9298203135202a0c707bb0977ba38c31` byte-exact. **This is the strongest control in the order: the head fix rewrites a live artifact, so a dial-off drift would prove the fix leaked outside its lane.** |
| **F36** | **identity gate** | the `o29_gate` lineage re-point is **DECLARED** before it is made; no identity literal moves undeclared. |
| **F37** | **boot guard** | passes on every build; the `expected_boot` fv pin stays **stale by design** and is stated. |
| **F38** | **pins, moved-set asserted** | **DECLARED IN ADVANCE: `engine/rl_after/pvc_curve_v2.json`'s md5 MOVES** — the head fix rewrites `nd_v0.posv`, and every carrier of that md5 is re-stamped in the same act. **Any OTHER pin move is a build failure.** |
| **F39** | **`noarb_table_338.py` byte-identical** everywhere it appears. |
| **F40** | **active-provenance guard** | no foreign `rl_model.py` is installed for any board that ships a number to the owner; every build is staged. |
| **F41** | **book re-seal** | run if fired, in isolation, and reported. |
| **F42** | **nothing merges** | PR #510 title unchanged, `[HELD — DO NOT MERGE]`; `main` untouched. |

---

## 10 · THE DISCLOSURES OWED WHATEVER THE NUMBERS SAY

Filed here so they cannot be presented later as discoveries. **All of ORDER 31's own owed words are
inherited and re-printed in the completed packet**, plus:

1. **The depth-3 pool-fade inversion** (2.2635, `n` 17, 45% censored) — published, not wired, **owed
   confirmation**.
2. **The object confirmation** — β was fitted against the Step-1 `v0`; the head fix moves that object, and
   the re-derivation is the seat's answer to it. The owner's confirmation of the object is still owed.
3. **The deep-β CI spans zero** (71+: `t = 0.49`, 90% CI −4.6% … +10.5%).
4. **The head fix's own reconciliation residual** is printed per pick, not absorbed.
5. **The shrink `K` is the project's own K = 15**, transplanted from the pool construction to the
   positional heads. It is a **transplant**, and its transplant is the head fix's load-bearing assumption.
6. **The position gate's residuals** are flagged precisely rather than papered over.
7. **Pre/post numéraire is stated on every table.**

---

## 11 · THE LINE

Nothing merges. `main` is untouched. Engine runs are **strictly sequential** on the pinned venv under
five-var thread pinning with `RL_V0SURF_PKL` set; every build is staged in its own workspace.
`noarb_table_338.py` is byte-identical everywhere. The `expected_boot` fv pin stays stale.

**Breaches are owned by number in the packet. This file is not edited after a reading.**
