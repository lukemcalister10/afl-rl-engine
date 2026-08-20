# PREREG_F — ENTRY TIMING-WEDGE VERIFICATION SEAT

**Order F. Issue #334. Branch `land/order-29`. READ-ONLY: measure and report. Nothing is wired, no
engine/board/law file is touched, no store is written.**

This file is committed and pushed **before any number in this seat is computed**. Everything below is
fixed in advance: the hypothesis as falsifiable predictions, the construction of the wedge, the
tolerance, and what a match and a mismatch each mean.

---

## 0. WHAT I HAD ALREADY READ WHEN I WROTE THIS (full disclosure)

Honesty demands the disclosure, because the seat's own Step 1 is a code read. Before writing this
prereg I read, as source text only:

- `docs/evidence/candidate_31f/o31f_fit.py` (the One Law fit) and `o31f_headfix.py` (the v0 head fix),
- `docs/evidence/grace_adoption_2026-08-13/o28_derive.py` (the curve derivation),
- `docs/evidence/grace_adoption_2026-08-13/inputs/o26b_layer2.py` (the Layer-2 valuation),
- `engine/rl_after/rl_model.py` lines 196-250 and 1004-1025 (the grace-A dial and `disc_factor`),
- `docs/evidence/order32_s4_2026-08-17/s4_shootout.py` (the delivered-value ruler),
- `docs/evidence/order_c_2026-08-17/ATTRIBUTION_34_out.txt` and `NOARB_34_out.txt` (the observed marks).

**No number of my own has been computed.** The P1 verdict below is a code-reading verdict and I state
in this prereg, in advance, what each possible reading obliges me to do next. I am not free to choose
after the fact.

---

## 1. THE HYPOTHESIS UNDER TEST (the supervisor's, not mine)

> The entry surface v0 was fitted to **career-integrated delivered value WITHOUT time-of-delivery
> discounting**. Under the board's 14%/yr carry convention, an entry price equal to an undiscounted
> career total overstates the fair today-price, and it overstates it **by more** for bands and arms
> whose value arrives later. That timing wedge is the V-shape: entry 1.00 → yr1 ~0.92 → yr5 ~1.48 for
> picks 21-64.

My job is to **verify or kill** it. It is a convenient hypothesis — it explains the level, the band
ordering, the SSP inversion and the near-carry late growth all at once — and convenience is exactly
the reason to be adversarial with it.

## 2. THE PREDICTIONS, AS FALSIFIABLE STATEMENTS

**P1 — the fit target is undiscounted.** The value the v0 surface was fitted to is a plain sum of
per-season delivered value with **no** time-of-delivery discount factor. Verified by reading the fit
lineage and quoting the target construction line for line.

**P2 — the wedge matches the observed drop.** For each ND band and each pool arm, the implied timing
wedge

    W = [ sum_k (share of career delivered value arriving in year k) x 1.14^-k ]  /  [ undiscounted total = 1 ]

computed from the historical delivery profile, matches that band's/arm's observed year-0→1 mark ratio
relative to its own fair benchmark. The observed marks fixed in advance (repaired-C32):

| band | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---|---|---|---|---|
| yr1 mark | 1.048 | 1.087 | 1.037 | 0.885 | 0.929 |

| arm | RD | UNR | PDA | PDN | SSP | IRE | PDS |
|---|---|---|---|---|---|---|---|
| yr1 mark | 0.98 | 0.62 | 0.81 | 0.64 | 1.51 | 1.09 | 0.76 |

(The Order-C re-run of the same instrument reads RD 1.002, UNR 0.620, PDA 0.845, PDN 0.661, SSP 1.517,
IRE 1.155, PDS 0.782 — same signs, cited alongside.)

**P3 — SSP's sign.** SSP's +51% inversion corresponds to **immediate delivery**: its cohorts' value
arrives in years 1-3, so its wedge is near 1 (little or no overstatement) while the development arms'
wedges are deep.

**P4 — the late bands' forward growth sits near carry.** Already measured; cited, not recomputed.
Order C, `NOARB_34_out.txt`: yr1→5 growth 31-40 **1.616**, 41-64 **1.489**, against carry
1.14^4 = **1.689**.

## 3. THE WEDGE CONSTRUCTION (fixed here, before it runs)

**Ruler.** The house delivered-value ruler is **reused, not reinvented**: the per-season construction
is lifted **by source text** out of `docs/evidence/order32_s4_2026-08-17/s4_shootout.py` — `BARS`,
`softplus`, `capt_prem`, `posval`, `season_raw`, `w_sqrt`, and the `SV` assembly

    SV[key][year] = w_sqrt(games) * posval(avg + capt_prem(avg) - BARS[bar]) * 21.0

with the same right censor `LAST_REAL_SEASON = 2025`. The lifted text is md5'd and printed.

**Population.** Entry classes **2005-2019** (observable futures; six-plus years of delivery visible for
the last class), from the pinned per-entrant matrix `per_entrant_O31FFINAL.json` (md5 printed).
Force-majeure keys (`paddy-mccartin`, `thomas-boyd`) excluded, as in S4.

**Profile.** For entrant with entry year `e`, the delivery in year `k` after entry is
`v_k = SV[key][e+k]`, `k = 1, 2, ...`. The undiscounted career total is `U = sum_k v_k`. The cohort
profile is the **value-weighted** share `s_k = (sum over cohort of v_k) / (sum over cohort of U)`;
dispersion is reported as the cross-player p25/p50/p75 of each player's own `s_k` and of each player's
own wedge, over players with `U > 0`.

**Wedge.** `W = sum_k s_k * 1.14^-k`. Reported per ND band (the five ruled bands, by stored pick) and
per pool arm (`type`: RD, MSD, SSP, UNR, IRE, PDA, PDN, PDS).

**Bands and arms.** Bands are the ruled five (1-10 / 11-20 / 21-30 / 31-40 / 41-64) on the stored pick.
Arms are the record `type` with `is_pool` true. ND rows with `is_pool` true are excluded from the ND
band tables (they are priced on the pool ladder).

## 4. THE MATCH TEST AND ITS TOLERANCE (fixed here)

The wedge predicts a **fair-mark multiplier**. If the entry price is an undiscounted total `U` while
the fair today-price is `W*U`, then the year-1 mark should undershoot its own fair benchmark by the
factor `W`:

    predicted mark  =  fair_band * W          where fair_band = 1.14 * (1 - s1)  is Order C's own benchmark
    implied wedge   =  observed mark / fair_band

**Tolerance, declared before computing.**

- **MATCH (cell):** `|W_computed - W_implied| <= 0.05` in ratio points.
- **NEAR (cell):** `0.05 < |diff| <= 0.10`.
- **MISS (cell):** `|diff| > 0.10`.
- **Overall SUPPORT** requires all three of: (a) at least 7 of the 12 cells MATCH and no more than 2
  MISS; (b) the **rank correlation** between `W_computed` and `W_implied` across cells is positive with
  the sign test passing on the five ND bands; (c) the two sign tests below both pass.
- **Sign test S1 (SSP):** `W_SSP` must be the **largest** wedge (closest to 1) of the pool arms.
- **Sign test S2 (development arms):** `W_PDS`, `W_PDN`, `W_PDA` must all sit **below** `W_RD`.
- **Overall KILL** if the band ordering of `W_computed` is uncorrelated with or opposite to the band
  ordering of `W_implied`, or if either sign test fails.

A band-uniform `W` is a **MISS on the spread** even if it matches the level: the V-shape's defining
feature is the 0.194 band gap range, and a uniform wedge cannot produce it. This is stated in advance
so that "it explains the level" cannot be sold as "it explains the V-shape".

## 5. THE KILL RULE ON P1 (the one that binds hardest)

**If the v0 fit target turns out to be discounted already, the hypothesis dies at Step 1.** I then
stop the wedge computation as specified above, report the kill with the code quoted, and the packet
documents (a) the kill and (b) **what the V-shape needs instead** — i.e. the timing profiles are still
built, because the replacement account of the V-shape has to be measured against the same data, but
the "undiscounted career total" wedge is reported only as a **counterfactual bound**, clearly labelled,
never as the operative finding.

Concretely, in that branch I will instead measure the **residual wedge**: the ratio between the entry
price's own discount ladder and a strict 14%/yr carry ladder, per band and per arm, and test the same
match. If the entry ladder and the board's live ladder are the **same** ladder, there is no wedge to
find and I will say so plainly and look for the V-shape's cause in the benchmark or in the year-1 marks
instead.

## 6. THE ADVERSARIAL ALTERNATIVE (tested against the same data, not waved at)

**ALT-1: the year-1 marks are simply too low.** The entry prices are right and the board's year-1
re-pricing under-values first-year players (the sit-cost / washout machinery), which would produce the
same yr0→1 dip and the same near-carry recovery afterwards.

Discriminator, fixed in advance: ALT-1 predicts the deficit is concentrated in **who sat** and in the
year-1 re-pricing inputs, and predicts **no** relationship between a band's delivery timing and its
drop. The timing hypothesis predicts the opposite: the drop tracks how late the value arrives,
regardless of year-1 games. If `W_computed` is flat across bands while the observed drops span 0.194,
the evidence prefers ALT-1 on the spread. If both stories fit the level and neither fits the spread, I
will say the evidence **cannot tell** rather than pick.

**ALT-2: the fair benchmark itself is wrong.** Order C's fair mark is `1.14 * (1 - s1)`, which assumes
the entry→year-1 step earns a full carry. If the board's own discount convention does **not** accrete
over that step, the benchmark, not the price, is the thing that is off. This alternative is checked by
the same arithmetic that decides P1, using the engine's own `disc_factor` and `grace_years` with no
re-implementation.

## 7. LIMITATIONS DISCLOSED IN ADVANCE

1. **Right censoring.** The 2019 class has six visible years; a career runs longer. Profiles are
   therefore truncated for the late classes. I will report the wedge both on the full observable window
   and on a **fixed 6-year horizon** common to every class, and use the fixed-horizon reading whenever
   the two disagree.
2. **Observed leg only.** The fit target's `total` = observed leg + a projected tail for live careers.
   My profiles are built from **observed** seasons only, so a live career's future seasons are absent
   from its profile. This biases profiles toward earlier delivery and therefore biases the wedge
   **upward** (toward 1) — i.e. against the hypothesis. Stated so the direction cannot be re-chosen
   later.
3. **Thin arms.** SSP n≈13-31, PDS n≈21, PDN n≈17-33, MSD n≈9 in the observable window. These are
   thin, right-censored and in SSP's case a recent mechanism. No arm cell with n < 15 in the observable
   window carries a verdict; it is printed and marked THIN.
4. **Zero-delivery careers.** Players with `U = 0` (never above the bar) have no profile. They are
   counted and excluded from the share arithmetic; their exclusion is a known upward bias on the wedge
   and is reported.
5. **The wedge is a pricing identity, not a causal claim.** Even a perfect quantitative match would
   show the entry surface is on a different clock from the benchmark — it would not by itself prove
   which clock is right. The recommendation is written accordingly.

## 8. WHAT GETS PUBLISHED EITHER WAY

`PACKET_F.md` — plain language: the fit-code quote, the timing profiles, the wedge table against the
observed drops, the verdict, and, **only if supported**, a proposed entry-discount curve (smooth in
pick per the owner's trend law; per-arm factors for the pools) for the entry-refit round. Not wired.
If a curve is proposed, the interaction is stated: the yr0→1 no-arb tables would have to be **re-based**
onto the discounted entries, and I will state which reds close by construction and which remain.

---

*Committed before computation. Order F, seat: entry timing-wedge verification.*
