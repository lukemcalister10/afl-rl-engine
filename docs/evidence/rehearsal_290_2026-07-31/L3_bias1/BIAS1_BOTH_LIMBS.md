# L3 BIAS-1 — BOTH LIMBS MEASURED. **Nothing chosen.**

**#290 L3, 2026-07-31**, window word **A** (the 2003 class stays in the teaching window, so both
limbs are live). Seam word: *both limbs measured, nothing chosen silently.*

Substrate: reconstructed L1-exit tree · store `81d24704` · frozen v0surf `84fb0cde` · E3 applied ·
strictly serial behind `tools/preboot_assert.sh`.

## THE TWO LIMBS

**Limb 1 — the PHANTOM ROWS.** The store's scoring begins in **2005**. A 2003 draftee (debut 2004)
emits a `build_cond_prior` training row at Y=2004 carrying `games=0, exposure=0, level=0` — not
because he did not play, but because the store cannot see 2004. **64 rows**, one per player, of
13,221 = **0.484%**. *(The 214 rows at `Y == d0` are DRAFT-YEAR rows, zero by design per the
function's own docstring — deliberately **not** part of this limb.)*

**Limb 2 — the TENURE OFFSET.** `_feat` uses `ten = Y-(debutyr-1)`. A 2003 draftee at Y=2005 reads
**tenure 2** carrying ONE observable season; a 2004 draftee at Y=2005 reads **tenure 1** carrying
one. Same evidence, one tenure-year older — the class presents as slower developers. Touches **all
641** of the class's training rows.

**Why limb 2 is genuinely arguable, stated rather than assumed:** `ten` is not *wrong* — a 2003
draftee in 2005 really is in his second year since the draft. The distortion is that for every other
class, tenure T arrives with T seasons of observable evidence, and for this class with T−1.
Re-anchoring restores evidence-per-tenure consistency but misstates real elapsed time. Age is carried
**separately** by `_age_asof`, so re-anchoring does not corrupt the age signal — measured, not assumed.

## THE FOUR TREATMENTS

Each is a full independent prior build (400 trees × 5 quantiles). The row loop and feature
construction are copied **verbatim** from `build_cond_prior` / `_feat` with only the limb switches
applied, so any difference is attributable to the limb and not to a rewrite.

| treatment | limb 1 | limb 2 | training rows | fit |
|---|---|---|---|---|
| **T0** baseline | – | – | 13,221 | 36.7s |
| **T1** drop phantom rows | ✔ | – | **13,157** (−64) | 36.7s |
| **T2** tenure re-anchor | – | ✔ | 13,221 (0) | 37.5s |
| **T3** both | ✔ | ✔ | **13,157** (−64) | 37.2s |

## THE CONTROL THAT MAKES THE DELTAS MEAN ANYTHING

**T0 rebuilt in a fresh process → bands BYTE-IDENTICAL, 0 of 804 differ.** The fit-noise floor is
**exactly zero**, so every delta below is the limb and not the refit. Run before reporting any delta,
because without it "the band moved" and "refitting moves bands" are indistinguishable.

## THE EFFECT IS ENTIRELY INDIRECT

**The 2003 draft class has ZERO members on the live board.** They were drafted 23 years ago; all are
concluded, and the board prices only the **804 active**. So bias-1 reprices nobody directly — its
whole effect is those training rows shaping the prior, which is then applied to today's 804.

## BAND DELTAS vs T0 — over all 804 board players

| treatment | movers | median \|Δp50\| | max \|Δp50\| | median rel | **max rel** | direction | net Σ Δp50 |
|---|---|---|---|---|---|---|---|
| **T1** phantom drop | **804 / 804** | 0.5466 | 5.0020 | 0.810% | **9.852%** | 399 up / 405 down | −12.09 |
| **T2** tenure re-anchor | **804 / 804** | 0.5210 | 4.5494 | 0.767% | **8.961%** | 423 up / 381 down | +40.24 |
| **T3** both | **804 / 804** | 0.6821 | 7.7226 | 1.030% | **14.014%** | 368 up / 436 down | −56.08 |

**Every band moves under every treatment.** 64 rows — 0.484% of the training set — move all 804 bands
by a median 0.810% and up to 9.852%. The direction is near-balanced in each case: this is
redistribution, not a level shift.

## THE FINDING THAT CONSTRAINS THE DECISION — **the limbs are NOT additive**

| | Σ Δp50 |
|---|---|
| T1 alone | −12.09 |
| T2 alone | +40.24 |
| **T1 + T2, if independent** | **+28.15** |
| **T3, measured** | **−56.08** |

**T3 ≠ T1 + T2 for 804 of 804 players (100%)** — median interaction residual **0.7959**, max **7.8973**
(`liam-fawcett`). The aggregate does not merely differ in size, it **flips sign**.

**So the two limbs cannot be worded independently.** Choosing limb 1 and limb 2 separately, each on
its own measured effect, does not produce the T3 outcome. The four treatments are four distinct
options, not two binary switches.

## WHAT IS NOT DECIDED HERE

Nothing. All four treatments stand measured and none is recommended. Which limbs land — and whether
they land together — is the owner's word.

## COST

~37s per prior build; **3m16s** for all four in one process (so the band comparisons carry no
cross-process variance); +82s for the determinism control. Reproduce with `bias1_measure.py`
(`L3_ONLY` runs a single treatment).
