# PREREG — ORDER 30A: THE ND SITTER DISCOUNT, DERIVED FROM EVIDENCE

**Committed BEFORE any quantity of interest was measured.** Nothing in this file has been edited
after the first measurement ran; breaches are owned by number in `SITTER_FADE_PACKET.md` §Prereg
scored, and the prediction text is left exactly as filed.

Act: ORDER 30A, the measurement seat. Brief:
[#334 comment 5289933916](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5289933916).
Branch `land/order-29`. **READ-ONLY**: no engine file, no board, no store, no curve is touched by
this act. **NOTHING WIRES.** The old `los_decay` schedule stands as the DECLARED FALLBACK until the
owner rules on the packet.

---

## 0. THE QUESTION, RESTATED

The engine's ND sitter penalty is a **designed** schedule with no fit provenance
(`engine/rl_after/rl_model.py:725-729`):

```
GRACE = {'KPF':2.5,'KPD':2.5,'RUCK':2.5,'MID':1.0,'SD':1.0,'SF':1.0}
LOS_C = 0.16 ; LOS_P = 1.82
los(p)        = AGE_REF - p['year']                      # years since entry, s
los_decay(p)  = exp( -LOS_C * max(0, s - GRACE[gfut])**LOS_P )
```

Owner ruling, verbatim (2026-08-14): *"we keep the old formula that was logical but not derived from
evidence as a backup plan, and look to derive what a reasonable sitter discount would be for players
in the ND. Considering all lenses - position, draft pick, and years in the system."*

This act derives the discount. It does not wire it.

---

## 1. THE ESTIMATOR, PRESTATED (so it cannot be chosen after seeing the answer)

**Depth.** `N = s = (season year) - (entry year)`, the engine's own `los()` clock. `N = 1` is a
normal draftee's first season. A player is **STILL SITTING AT DEPTH N** iff he has **zero games in
every season k = 1 … N-1**. `N = 1` is therefore the whole entry class (nobody has sat yet) and is
the **baseline row**.

**Numerator — the outcome.** The delivered-value lane's grace-A career score
(`docs/evidence/delivered_value_2026-08-12/LAYER2.json::grace_a[key].total`, built by
`o26b_layer2.py` on Layer-1 `ad1229ea6f443538479447132382b21c`), **re-anchored to the valuation
moment**:

```
V_N(i) = grace_a[i].total  x  DF_i(N-1)          DF_i(k) = disc_factor(entry_age_i, 0.14, max(0, k-G_i))
```

`grace_a[i].total` is discounted **to acquisition (day 0)**. Multiplying by `DF_i(N-1)` re-anchors it
to the start of year N, which is the moment the price is being formed. **This is not an optional
nicety**: without it a player who sat one year and then delivered a fresh entrant's career from a
year later would read a 0.877 discount that is pure time-value and carries no information about
sitting. A day-0-anchored column is reported alongside as reading **D0**.

*Because a sitter has zero games before depth N, he has zero delivered value before depth N: the
whole career score IS the from-depth-N score. No per-season decomposition is required for the
sitter rows and none is performed.*

**Denominator — the landed entry law.** `engine/rl_after/pvc_curve_v2.json::nd_v0.posv[g][p]`, the
ORDER-29 positional ND day-0 v0, read at the player's **acquisition slot**: `g = day0_position`
(Layer-1 `day0_position`, the drafted position — Ruling 5) and `p` = the **attributed** pick
(`LAYER2.json::attribution[key].pick`, i.e. the force-majeure whole-draft slide applied; the two
excluded keys are dropped entirely).

**The cell statistic.**

```
r_i     = V_N(i) / posv[g_i][p_i]
RAW(N)  = mean_i r_i        over the cell
D(N)    = RAW(N) / RAW(1)   -- THE DERIVED SITTER DISCOUNT, normalised on the depth-1 baseline
```

The normalisation on the depth-1 row is deliberate and prestated: it cancels every level offset
between the outcome basis (grace-A, store `d9a24282`) and the price basis (`pvc_curve_v2`, store
`f1e8c9fe`, numeraire `s = 0.94009`), so what survives is only the **conditional** effect of having
sat. `RAW(1)` is published so the offset is visible and not hidden.

Every cell publishes: **n · mean · median · p25 · p75 · pooled (Σnum/Σden) · mean tail share**.
Never a bare mean.

**Comparison object.** `los_decay` evaluated on the same depth axis, per position group, using the
engine's own constants read out of `rl_model.py`.

---

## 2. THE CENSORING RULE, STATED BEFORE THE COUNT IS KNOWN

- **CENSOR-1 (window).** The fitted population is ND entrants with attributed pick 1-64 and
  `entry_year ∈ [2004, 2021]` — the delivered-value lane's **core** (≤2014) plus **augmented**
  (2015-2021) tiers. `entry_year ≥ 2022` is the lane's **sensitivity tier** and is **EXCLUDED from
  every fitted number**, reported only as a separate panel. Recent classes cannot show deep-sit
  outcomes and will not be silently mixed in.
- **CENSOR-2 (depth observability).** A row may enter the depth-N cell only if seasons k = 1 … N-1
  are **completed** seasons (`entry_year + N - 1 ≤ 2025`; 2026 is in progress). Under CENSOR-1 this
  binds only at N ≥ 6.
- **CENSOR-3 (outcome observability).** The outcome leg is observed seasons **+** the lane's gated
  projected tail. A cell whose **mean tail share exceeds 0.50** is flagged **NOT USABLE AS
  EVIDENCE** — it is mostly the engine's own projection of the very players in question, and
  fitting on it would be circular.
- **CENSOR-4 (no store drift laundering).** The outcome basis was built on store `d9a24282`; this
  branch carries store `cb38ef11`. Layer 1 (`ad1229ea`) is byte-identical, so the population and the
  sit facts are unaffected. The store drift is disclosed, and the depth-1 normalisation absorbs any
  level effect. No number is recomputed on the new store.

---

## 3. THE PREDICTIONS

### Shape

**P1.** The all-pick derived discount `D(N)` is **monotone decreasing** in N over N = 1, 2, 3, 4+ on
the primary basis. `D(1) = 1.000` by construction.

**P2.** `D(2) ∈ [0.70, 0.95]`. The old schedule's year-2 value (0.852 for MID/SD/SF; 1.000 for
KPF/KPD/RUCK under the 2.5 grace) is **approximately right** at depth 2 — within ±0.15 of the
derived all-pick number.

**P3.** `D(3) ∈ [0.35, 0.65]`. The old year-3 value 0.568 is within ±0.20 of the derived number.

**P4.** `D(4+) < 0.30`, and the derived discount at depth 4+ is **HARSHER** than the old schedule's
year-4 value of 0.308. A top-64 pick with zero games after three full seasons is, in the evidence,
close to worthless.

**P5.** The old schedule reads **TOO HARSH in the middle** and **TOO GENEROUS at the extremes**:
specifically too harsh at depth 3 for the KPP/RUCK positions it grants a 2.5-year grace to (the
grace over-protects them relative to what they deliver), and too generous at depth 4+ everywhere.

### Sample thinness — the cells I expect to be unusable

**P6.** All-pick row counts, fitted window: `n(N=2) ≥ 80`, `n(N=3) ∈ [15, 45]`, `n(N=4+) < 15`.

**P7.** The **position lens** carries **no usable signal at N ≥ 3** — every six-way position cell at
depth 3 or deeper has n < 10 and must be collapsed. At depth 2 only a two-way collapse
(**KPP+RUCK** vs **non-KPP**) will be readable.

**P8.** **Every three-way cell** (depth × pick band × position) is unusable at N ≥ 2. The table will
publish the two two-way lenses (depth × pick band, depth × position) and never the three-way cross.

**P9.** At N ≥ 4 the pick lens collapses too: no pick band at depth 4+ reaches n = 10, so the depth-4+
row is **all-pick only** and the pick-band cells there are shrunk essentially all the way to it.

### The lenses

**P10.** Of the three lenses, **years-in-system carries essentially all the signal**. The pick lens
carries a **second-order but real** effect; the position lens carries **none that survives its own n**.

**P11.** Direction on the pick lens: at a given depth ≥ 2 the derived discount is **STEEPER
(harsher) for picks 1-20 than for picks 41-64**. The denominator scales steeply with pick while a
sitter's realised delivery does not, so the early-pick sitter loses proportionally more.

**P12.** K-shrinkage pulls every pick-band cell **more than 50 % of the way** toward the all-pick row
at N ≥ 3.

**P13.** The RUCK/KPF/KPD grace of 2.5 years in `los_decay` is **NOT supported** by the evidence: the
derived KPP/RUCK depth-3 discount does not exceed the non-KPP depth-3 discount by anything like the
factor the grace implies (`1.000` vs `0.568`), or the cell is too thin to say — either way the grace
does not earn its place as a measured object.

### Distribution and calibration

**P14.** `RAW(1) ≠ 1.000`. It lands in `[0.70, 1.40]`. The depth-1 normalisation is therefore
load-bearing and is not cosmetic.

**P15.** Dispersion is enormous and one-sided: **p25 = 0.000 exactly at every depth N ≥ 2** (busts
deliver exactly zero and the scorer floors at zero), and **median / mean < 0.60 at every depth
N ≥ 2**.

**P16.** The **median** discount is far harsher than the mean, and at N ≥ 3 the median is **exactly
0.000**. The seat will therefore recommend the **mean** (the price of an expectation is an
expectation) and will say so explicitly.

**P17.** Mean tail share in the fitted sitter cells is **< 0.25 at N = 2** and **< 0.10 at N ≥ 3** —
deep sitters are old classes and are retired, so CENSOR-3 will not bite the fitted rows. It **will**
bite the 2022+ sensitivity panel, where I expect mean tail share **> 0.90**.

**P18.** At least one **raw (unshrunk)** cell somewhere in the three-lens table is **non-monotone in
depth**. Thinness, not signal.

### Method symmetry (the one-machinery law)

**P19.** The ORDER-21 pool retention surface (`whole_pool` nonKPP `0.624 0.380 0.380 …`, KPP
`0.817 0.500 0.467 0.359 …`) is **more generous at shallow depth and harsher at deep depth** than
`los_decay`, and my ND-derived surface will land **closer to the ORDER-21 pool shape than to
`los_decay`** at depths 2-3 — i.e. the two pathways, measured the same way, will look like each
other, which is what the one-machinery law predicts.

**P20.** The pool's construction divides by a **same-depth norm** over all cells at that depth
(`norm(cls,d) = E[winsor(O/entry_anchor, 2.0)]`) to strip survivor selection, where this act
normalises on the **depth-1 baseline**. I predict the two readings differ materially — by more than
0.10 at depth 3 — and that the norm-divided reading is the **more generous** of the two, because the
depth-N surviving population is itself a selected (worse-than-entry) set.

### Named test rows

**P21.** `josh-smillie` (ND 2024, MID, pick 7, depth 2). 29B flat v0 prints **1,617**; old
`los_decay` gives 1,617 × 0.852 = **1,378**. The derived price lands in **[1,150, 1,500]** — below
the flat print, above nothing.

**P22.** `harry-demattia` (ND 2023, MID, pick 25, depth 3). 29B flat **892**; old 892 × 0.568 =
**507**. Derived lands in **[300, 550]**.

**P23.** `max-knobel` (ND 2022, RUCK, pick 42, depth 4). 29B flat **834**; old `los_decay` with the
RUCK 2.5 grace gives 834 × exp(-0.16·1.5^1.82) ≈ **600**. The derived price is **materially harsher
than the old one — below 400** — because the RUCK grace is the weakest-evidenced part of the old
schedule (P13) and depth 4 is the harshest part of the derived one (P4).

**P24.** `harrison-ramm` (MSD pick 3), `mani-liddy` (MSD pick 15), `vigo-visentini` (RD pick 5) are
**POOL** rows and are carried for **method-symmetry commentary only**. No ND-derived discount is
applied to them in this act, and I predict all three carry ≥ 1 career game and are therefore not
sitters on this act's own definition at all.

**P25.** Of the 43 currently-reinflated year-2+ 0-game rows named in the 29B finding, **≥ 30 sit in
the 2022+ sensitivity tier** and therefore contribute **nothing** to any fitted number in this act.

### The recommendation I expect to make

**P26.** I expect to recommend a **depth-keyed, position-blind, pick-shrunk** discount — one column
in years-sat, with the pick lens disclosed but shrunk, and the position lens declared **not
measurable** — because at these sample sizes the other two lenses do not carry signal, and fitting
them would be fitting noise.

---

## 4. WHAT WOULD FALSIFY THE ACT

If the fitted depth-2 cell has n < 40, or the depth-3 cell has n < 10, the seat will say **the
evidence does not support replacing the fallback at that depth** rather than publish a number it
cannot defend. Thin cells are reported with their n and marked, never smoothed into confidence.

---

*Filed 2026-08-14, before `o30a_derive.py` existed in runnable form and before any cell was counted.*
