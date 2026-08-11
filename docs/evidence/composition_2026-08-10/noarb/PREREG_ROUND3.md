# PRE-REGISTRATION — ROUND 3 (V5 · the ramp de-couple · the #336 channel split)

**Filed BEFORE any round-3 emit ran.** Written against #334 build brief comment 5248006413. Every
prediction below is stated so it can be BREACHED, and a breach is reported as a breach. Nothing here
is retuned after the fact.

Instrument for every figure: `noarb_table_338.py` UNMODIFIED (md5 `0f8220351c64c56ccfa90c60edcdfa5f`,
verified at the head of this round), pooled Σprice/Σanchor over the harness loader's own population —
1197 ND teaching entrants, picks 1-64, classes 2004-2022, `teaches_curve`, EXPECT_N re-measured per
matrix. Never mean-of-ratios, never a live-board cross-section.

Baselines on that instrument (MENU.txt, this branch):

| row | yr1 | yr4 | own disc @18 | margin |
|---|---|---|---|---|
| main | 1.1239 | 1.5732 | 14.00% | +1.61% |
| FULL | 0.9974 | 1.5310 | 14.00% | +14.26% |
| V2 | 1.0933 | 1.5870 | 12.00% | +2.67% |
| V4 | 1.1382 | 1.5637 | 11.00% | **−2.82% ARB** |
| V3 | 1.1456 | 1.6390 | 10.00% | **−4.56% ARB** |

---

## ORDER 1 — V5, the owner's fifth ladder

`_V5_KNOTS = [(18,.12),(19,.125),(20,.13),(21,.135),(22,.14),(23,.14),(24,.145),(25,.15),(26,.15),(27,.155),(28,.16)]`

Verified by direct call of the engine's own `_pw_interp` BEFORE the emit (rates in %):

| age | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28+ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| V2 | 12.0 | 12.0 | 13.0 | 13.0 | **13.5** | 14.0 | 14.5 | 15.0 | 15.0 | 15.0 | 16.0 |
| V4 | 11.0 | 11.0 | 12.0 | 13.0 | 14.0 | 14.0 | 14.5 | 15.0 | 15.0 | 15.0 | 16.0 |
| V5 | 12.0 | 12.5 | 13.0 | 13.5 | 14.0 | 14.0 | 14.5 | 15.0 | 15.0 | **15.5** | 16.0 |

So: V5 and V4 are IDENTICAL at ages 22-26. V5 is dearer than V4 at every age ≤21 and at 27.
V2 has no 14% shelf at 22 at all (13.5% there, a smooth join 21→25) — the owner's premise that V2 and
V4 "both have 14 from 22" does not hold, and that is why V5's shelf is stated as its own knot pair.

**P1.1 — yr4 lands near V4's 1.5637, and above FULL's 1.5310.** Both pin age 22 at exactly the flat
baseline, and V5's dearer 24 is identical to V4's, so the only yr4 channel that can differ is the
young-side rate reaching year 4 through the peak estimate. Predicted band **1.555 – 1.570**.
*Falsifier: a yr4 outside that band, or below FULL.*

**P1.2 — yr1 lift is BELOW V4's 1.1382.** V5 discounts the young future harder everywhere ≤21
(12–13.5% vs V4's 11–13%), so it lifts young value less. Predicted band **1.100 – 1.135**, i.e. above
V2's 1.0933 and below V4's 1.1382. *Falsifier: yr1 ≥ 1.1382 or ≤ 1.0933.*

**P1.3 — the margin is BETTER (less negative) than V4's −2.82%.** Two effects push the same way: less
yr0→yr1 appreciation, AND a dearer own-discount at draft age 18 (12.00% vs V4's 11.00%).
**WHETHER IT COMES OUT LEGAL (positive) IS NOT PREDICTED.** It is the question this row exists to
answer and it is measured, not asserted. Registered range: **−1.5% to +2.5%**, with the sign OPEN.
*Falsifier: a margin at or below V4's −2.82%.*

---

## ORDER 2 — the ramp de-couple (RL_A_GSAT), two SAFE forms

Built per `RAMP_DECOUPLE_SPEC.md`: A's copy of the fade de-couples only; the admission bar stays
`ns>=1` at 6·fE prorated; `sitout_ev`'s LAM_SIT read is untouched. **G_SAT = 18** — the spec leaves the
value open at "~15-20" and 18 is the SEAT'S choice inside that range, recorded as such. It is not an
owner number and it is not measured-optimal.

### THE DIRECTION, MEASURED BEFORE THE EMIT — and it CONTRADICTS the spec's filed expectation

`yr1_direction.py` walks the year-1 as-of exactly as `emit_matrix_338.py` does (same truncation, same
BASE_REF/AGE_REF, same `_pe_clear`) and records `(e_full, anch, s)` at the A site for every ADMITTED
row. Measured on the harness population, n=1198 rows walked:

- **416 rows reach the A site at cohort year 1.** They are admitted; the built-A share `s` is
  **exactly 0.000000 on all 416** — the year-1 silence, re-confirmed independently.
- Of those 416: **DRAG (anch < e_full) 346 rows = 83.2%**; SUPPORT (anch > e_full) 70 rows = 16.8%.
- `anch/e_full` median **0.5540**; **pooled Σanch / Σe_full = 0.5150**.
- career games at year 1: median 12; 313 rows below G_SAT=18, 103 at or above it (so a majority do
  sit part-way up the de-coupled ramp, which is the mechanism working as specified).

The spec predicted "**Year 1 rises, by construction**" for BOTH admissible forms, and put A-DRAGFADE
"between FULL and de-couple+floor". **That is wrong for A-DRAGFADE and I am saying so before the
emit, not after.** The spec reasoned from the anchor being a support; on the actual year-1 population
the anchor sits at roughly HALF the production price on five rows in six.

**P2.1 — A-FLOOR + de-couple: yr1 RISES, by a SMALL amount.** The floor is `max(e_full, b)`, which is
inert on every drag row, so only the 70 support rows (16.8%) can move at all. Predicted yr1 in
**1.000 – 1.020** (FULL is 0.9974). *Falsifier: yr1 below 0.9974, or above 1.020.*

**P2.2 — A-DRAGFADE + de-couple: yr1 FALLS below FULL.** Drag is permitted (faded by `1-w`, clipped),
and 83.2% of the movable rows are drag rows against a pooled anchor at 0.515× production. Predicted
yr1 in **0.960 – 0.997**. **This is a filed BREACH of RAMP_DECOUPLE_SPEC.md's own expectation**, filed
in advance so it cannot later be reported as a surprise. *Falsifier: yr1 at or above FULL's 0.9974.*

**P2.3 — yr1 full-season movers become NONZERO in both forms.** The number was 0 under built-A
(A never moved a ≥6-game row at any career year). Predicted: **> 0**, and specifically that the moved
set is dominated by rows with career games < 18. *Falsifier: 0 movers — that would mean the dial did
not reach the site.*

**P2.4 — yr4 largely unaffected, but this is stated as FALSIFIABLE, not assumed.** At year 4 most rows
are far past 18 career games, so the de-coupled ramp saturates and the change is inert. Predicted yr4
within **±0.5%** of FULL's 1.5310 for both forms. *Falsifier: a move beyond ±0.5%. The H ladder's
pre-registration got exactly this shape of claim wrong, which is why it is registered as a test.*

**P2.5 — the no-arb margin is PRINTED for both forms.** No prediction is made on its size; the
discount charged is unchanged at 14.00%, so the margin moves one-for-one with yr1. A rise past ~+14%
appreciation would open an arbitrage; neither form is expected to get close.

**P2.6 — sitout_ev is byte-unchanged with the de-couple dial on.** Asserted by direct measurement
over the whole population, not by inspection. *Falsifier: any row whose `sitout_ev` output differs.*

---

## ORDER 3 — the #336 channel split. THE GROUPING, FIXED HERE BEFORE ANY COUNTERFACTUAL EMIT

The 13 ported hunks of `9a8bbd9` are grouped into three channels. The grouping is decided by what the
code actually does, and it was checked by an in-process table probe before any emit (below).

### (a) THE P-LEG — `RL_336_NOP=1`
The unconditional probability factor `P(ever establishes)`, applied to picks and to unresolved rows.
Reverting it: `BPK[(g,b)] = E[level|est]` instead of `P × E[level|est]`; `POOL[b]` becomes the
establisher-only band marginal instead of the bust-inclusive one (the whole-band mean with
never-establishers at 0.0 IS `P_band × the establisher-only mean`, so this is the same factor at the
band marginal); and the residual anchor-side discount `D` goes from 0.999644 to 1.0.
**This is the RE-TIMEABLE channel — the bust CHARGE. Design territory.**

### (b) THE DE-SURVIVORED E-LEVELS — `RL_336_SURVLVL=1 RL_336_CLAMP=1`
The conditional mean's SAMPLE reverts to the pre-#336 survivor definition (membership
`pkbest(p) is not None`, i.e. a ≥10-game season, at the level `pkbest` itself), so the 148
established-but-never-10-game players stop teaching; and the v3.4 late-pick clamp is restored on both
baseline tables. `P`'s own numerator is NOT touched and stays on the ruled ≥6-game bar, so (a) and (b)
are orthogonal in code. **This is the HONESTY REPAIR ITSELF and is NOT design territory — softening it
re-admits survivor bias (owner's standing ruling). It is measured only to bound the design.**

### (c) THE PAR_BUILD CONSUMER LEG — `RL_336_PARSURV=1`
`par_build.gather()`'s observation gate reverts to the shipped pre-#336 `g >= MIN_GAMES`
(survivors-at-that-tenure) from `g >= 1 and ever-established`.

**FINDING, filed here because it shaped the grouping: amendment 2/3's par-side machinery is DEAD ON
THE VALUE PATH.** `build_pest` / `pest_of` / `resolved_336` / `resolve_w` / `dpar_of` and the A3
reconciliation constants have NO consumer outside `par_build.py` — `par_redesign.py` carries its own
`par_at` (:68) composing `pb.level_at` with `F['ramp_shr']` and never calls them; a repo-wide search
finds no other reader. So the ONE gate above is the complete par-side counterfactual, not a partial
one, and the "amendment 3 / forward_valuation side" named in the brief reaches the engine only through
which observations the par surface is fitted to.

### THE 3-WAY GATE IS CLEAN — proven by table probe before the emits

| arm | rl_model BASEPK_REG | par surface | amendment-2 guard breaches | BASEPK_REG non-monotone cells |
|---|---|---|---|---|
| BASE (FULL, as built) | — | — | **1** — (KPD, band 0): est 75.3392 < reg 75.7857, −0.4465 | 5 |
| (a) NOP | moves (→ equals BASEPK_EST) | **unchanged** | 0 | 14 |
| (b) SURVLVL+CLAMP | moves | **unchanged** | **2** — (RUCK,0) −0.2515, (RUCK,1) −0.6190 | 0 |
| (c) PARSURV | **unchanged** | moves | 1 (same cell as BASE, unchanged) | 5 |

(a) and (c) touch disjoint files and neither disturbs the other's tables — a clean gate.

**TWO HONEST QUALIFICATIONS, filed before the measurement:**

1. **The monotonicity guard `basepk_est >= basepk` DOES NOT HOLD AT THE COMPOSED BUILD ITSELF.**
   `_A2_GUARD` is non-empty at HEAD/95dfbde: 1 cell, (KPD, band 0), by −0.4465 points (−0.59%). The
   amendment-2 header says it is "Asserted below, not assumed" — but `_A2_GUARD` is only a computed
   list; nothing raises on it. So the brief's precondition "the guard must hold in every emitted
   config" is not met by the REFERENCE config, before any ablation. This is reported, not repaired.
2. **Channel (b)'s arm carries 2 guard breaches against BASE's 1**, in different cells (RUCK bands
   0 and 1 replace the KPD one). Isolated by probe: the v3.4 clamp alone does NOT cause it
   (`RL_336_CLAMP=1` alone leaves the guard at BASE's single KPD cell); the survivor SAMPLE does. So
   channel (b) distorts the layer's internal consistency by one additional cell in a thin position,
   and **its attribution is the least trustworthy of the three**. The split is still run 3-way rather
   than falling back to 2-way, because 2 breached cells out of ~56 (positions × 8 bands), at −0.26%
   and −0.70%, is a bounded distortion in RUCK only — but the number is on the table and the reader
   is told which row to trust least.

### Predictions for the split

The whole-layer give-back is known: `no336` yr1 1.0992 vs FULL 0.9974, i.e. **+0.1018 = 80.5%** of the
−0.1265 main→FULL year-1 drop ≈ **−9.1pp of the −11.3%**.

**P3.1 — the P-leg (a) is the LARGEST of the three at year 1.** It is the only channel that applies a
multiplicative discount below 1 to every pick baseline; the measured `POOL` gap is large (band 7:
34.0 bust-inclusive vs 69.5 establisher-only). Predicted share of the +0.1018 give-back: **> 50%**.
*Falsifier: (a) below 50%, or not the largest.*

**P3.2 — the E-levels (b) are SMALL at year 1, under 20% of the give-back.** The bulk of the
de-survivoring is carried by the P factor (never-establishers entering the DENOMINATOR); channel (b)
is only the 148-player level extension plus the clamp. *Falsifier: (b) ≥ 20%.*

**P3.3 — the par leg (c) is small at year 1 but NOT zero**, because par feeds ITEM C's `Q = sa/par`
and the engine's par_pole. Predicted **0 < (c) < 20%**. *Falsifier: (c) ≥ 20% or exactly 0.*

**P3.4 — the three shares will NOT sum to 100%.** Reverting all three is not the same object as the
whole-commit revert: with (a) on, `BASEPK_REG == BASEPK_EST` and `D == 1.0`, so the amendment-2/3
consumer re-siting (`basepk_c → basepk_c_p`) collapses to identity and has no residual to strip. The
gap is an interaction residual and is **PRINTED, NOT NORMALISED** — the same convention as DECOMP.txt.

---

## IDENTITY — the gate every number above rides on

At final HEAD, with **all** new dials off (`RL_A_GSAT=0`, `RL_336_NOP=0`, `RL_336_SURVLVL=0`,
`RL_336_CLAMP=0`, `RL_336_PARSURV=0`, `RL_AGE_DISC=0`):

- the emitted per-entrant matrix must be **byte-identical** to `per_entrant_FULL.json`
  (md5 `c698b5b2763d29e299c14315576b48f1`) — a price-level identity, not a file copy; and
- the built board must be byte-identical (md5) to the board built at `95dfbde` under the same env.

If either fails, **nothing after it may be read.**
