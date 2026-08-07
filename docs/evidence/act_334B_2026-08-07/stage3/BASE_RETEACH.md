# Stage 3 step 1 — THE BASE-CURVE RE-TEACH, era-free

The shipped base ladder `df766dff` was taught while the engine's `REF/era` multiplier was live. The
owner ruling (stage ER, `f7ae027`) abolished era normalization, so the base had to be re-taught on the
clean basis before the re-anchor could sit on it.

## Machinery of record — and the currency mapping, disclosed

The derivation is `session_2026-07-30/item279/panel/harness_pvc.py`, run through the re-pinned copy
`harness_pvc_REPINNED_pass3.py` beside this file:

```
base_erafree = H.pin_and_check( H.kernel_raw( H.structural_values(ND), picks 1..64 ) )
```

* `structural_values()` — the ruled basis: VOR, structural completion, class cut 2022, `QUAL_GAMES=6`,
  `MIN_STRATUM=20`. A never-established career teaches **0.0** and stays in the denominator.
* `kernel_raw()` — the SHIPPED `#271 fit_year0` kernel carried verbatim: Gaussian over `log(pick)`,
  bandwidth grown from 0.10 until effective n reaches `NMIN=35`, capped at 0.60, then a weighted mean.
* `pin_and_check()` — `#271 monotone_strict` carried verbatim: PAVA non-increasing weighted by the
  effective n, then a **HARD SET** `fit[0] = 3000`, then strict descent with minimal integer forcing.

### THE CURRENCY MAPPING IS THE IDENTITY. Here is why, measured not assumed.

`pin_and_check` produces a 64-point integer ladder whose head is 3000 **by a hard set, not by a
rescale**. That is exactly the convention the shipped artifact's own `source` field names for the
superseded `derive_271.py` derivation — *"pava_ni/build_points/fit_year0/monotone_strict verbatim …
pin(1) = 3000"*. Three independent confirmations that the two currencies coincide:

1. the shipped ladder's `curve["1"]` is **3000** exactly, and its `pin` field is 3000;
2. the shipped ladder's `curve["2"]` is **2999** — `3000 − 1`, the exact fingerprint of the hard set
   forcing pick 2 below an overridden head. A pooled-numeraire ladder would carry the PAVA-pooled
   head at pick 2, not a forced decrement. The harness reproduces that same 2999 on the same-store
   matrix (matrix B below), with pick 2 in its `forced` list;
3. the per-pick delta between the shipped ladder and the harness re-derivation is small over values
   spanning 185–3000 (mean |delta| 18.1, table below), which it would not be under a currency change.

**So no scaling is applied when mapping the harness output into the ladder currency.** The artifact's
`numeraire` block is a *separate* field: it scales the **player** side through
`BOARD_FACTOR = (RL_PICK1 / PVC_v34[1]) * s` in `rl_model.py`, and never the ladder. It is dealt with
separately in `NUMERAIRE.md`.

## The attribution — four matrices, one method

The shipped base was derived on the `#328` corrected-store matrix; this stage's basis is the era-free
`#338` matrix. Those two differ in more than the era table, so the same derivation was run across the
whole chain and the delta decomposed. Each matrix is loaded with the harness loader and its identity
pins **RE-POINTED to that matrix's own committed meta, printed old → new** — the asserts run verbatim,
only the constants they compare against move, and `EXPECT_N` is re-measured with the loader's own
predicate before it is pinned.

| step | matrix | store | what it adds |
|---|---|---|---|
| A | `store_328_jujn3g/per_entrant_328_corrected_store.json` | f1e8c9fe | the basis the SHIPPED ladder was derived on |
| B | `noarb_338_2026-08-06/per_entrant_338_confirmation.json` | 37ced3ce | + the current gate store + the #338 minimum-tenure rule |
| C | `act_334B/stage2/per_entrant_338_stage1basis.json` | 37ced3ce | + the #336 reference layer (still era-ADJUSTED) |
| D | `act_334B/stage2_erafree/per_entrant_338_erafree.json` | 37ced3ce | **THE BASIS** — era normalization removed |

All four carry ND = 1197 and an identical provenance split (825 concluded-realised, 301 completed,
71 thin-fallback, 5.931% fallback share), so the population is constant and only the values move.

### Attribution summary (full 64-row table in `base_reteach_table.txt`)

| component | mean | mean abs | max abs | total |
|---|---|---|---|---|
| recipe (derive_271 → the harness, on the SAME 328 matrix) | +8.906 | 9.094 | 62 | +570 |
| #338 minimum tenure + the current gate store | +9.484 | 9.484 | 40 | +607 |
| the #336 reference layer | −31.016 | 31.016 | 60 | −1985 |
| **ERA REMOVAL** | **−0.141** | **0.141** | **1** | **−9** |

**The era removal moves the base by at most ONE board point at any pick, and by −9 over the whole
ladder.** That is the finding the brief predicted: era normalization scaled numerator and denominator
of the same cohort alike, and the ladder-side residue is a rounding-scale effect. The visible drift is
legitimate basis drift — the #336 reference layer (−1985, the dominant term), the #338 tenure basis
(+607) and the recipe difference between `derive_271.py` and the frozen panel harness (+570).

### The re-taught era-free base

`payload 4f6577ad · total 52719 · forced-descent picks [7, 8, 11, 12, 17, 18, 19]`

| pick | shipped | base_erafree | delta | pct |
|---|---|---|---|---|
| 1 | 3000 | 3000 | 0 | 0.000% |
| 10 | 1460 | 1433 | −27 | −1.849% |
| 20 | 990 | 971 | −19 | −1.919% |
| 40 | 514 | 501 | −13 | −2.529% |
| 64 | 185 | 230 | +45 | +24.324% |

whole-ladder: mean delta −12.766, mean |delta| 18.141, max |delta| 45 at pick 64, total
53536 → 52719 (ratio 0.984739).

The deep tail is the one place the delta is large in percentage terms, and it is **entirely the recipe
component** (+62 of the +45 at pick 64): `derive_271.py` carried a `max(210, …)` floor and its own
blend ceiling; the frozen panel harness does not, so the tail is free to sit where the kernel puts it.
That is a known, declared difference between the two instruments, not an era effect — the era column
is `0` for every pick from 26 to 64.

## Then the re-anchor

`f(p)` is read at full precision from the committed stage-2 evidence table
(`stage2_erafree/per_pick_reanchor.json`), unchanged. The candidate is `base_erafree(p) × f(p)`,
then the single numéraire re-base — see `NUMERAIRE.md` and `settled_ladder_table.txt`.

* monotone non-increasing **on the exact product**: **PASS**, no isotonic projection needed.
* strict integer descent after rounding: **one** collision, minimally repaired:
  * **pick 19**: exact product 958.201903, rounded to 958, colliding with pick 18's 958 → set to
    **957** (−1). Re-check PASS.

Settled ladder: `payload 18203822cf438ecef03ed77a771f9942` (in-file `curve_md5` `18203822`),
total 51221, pick 1 = 3000 exactly.
