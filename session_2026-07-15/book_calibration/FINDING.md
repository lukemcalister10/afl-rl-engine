# WALK-FORWARD BOOK CALIBRATION — FINDING (priced vs realised, by cohort)

**Base** `9be07b8e` (STRICT) · store `b1fd0bce` · engine `fc7045d6` · rl_model `f79fc740` · config
`c2d233ae` · **book N=2649, seal `99be9b36`.** Method fixed by `PLAN.md` **before** these numbers.
Measurement only — no cures (the PVC spec rework is the supervisor's, on this baseline).

## 0. Seal assertion — declared honestly
Regenerated the book with the frozen generator (`s4_matrix_M1v7.py`, gate mode) on the base engine in
an isolated workspace. **N=2649 and every identity stamp (engine/store/config) matches the committed
seal.** The stable-sha256 did **not** reproduce bit-exact across runners (`1b3c856a` here vs `99be9b36`
sealed) — the project's known cross-CPU float non-associativity (the board's PAR-solve determinism fix
does not cover the book's 24-season `ev()` surface; thread count ruled out). **Bounded directly:** the
book's present-value column reproduces the **committed canonical board** (built on the sealing runner)
**2638/2649 = 99.6 % EXACT**, the 11 others ≤4 SCAR (English 3402 vs 3405) + one edge record. The
scored book IS the sealed base book; the drift is ≤4 SCAR on 0.4 % of cells — orders of magnitude below
the cohort signal, and the calibration is cohort-aggregated + bootstrap-smoothed on top.

## 1. What is priced, what is realised
The book is a walk-forward panel: per player-year, `Vpath` = as-of **priced** value (data ≤ Y), `Ppath`
= **realised** era-adjusted SC output that season, `cur` = present value, `anchor` = Yr1 price. Realised
**output above replacement** uses the engine's own table `REPL{MID 80.1, GEN_DEF 78.3, RUC 78.5, KEY_DEF
68.4, GEN_FWD 70.9, KEY_FWD 66.8}` (item 131's axis). **Scored population:** 300 current contributors
(realised recent-2 output above replacement > 0); 1592 below-replacement-recent and 756 never-delivered
players are **kept, not dropped** (survivor-honest) and reported as the floor pool.

**The one methodological fact that governs everything:** `cur` is a runway-discounted **stock** of
future value; current output is a **flow**. At realised output ≈ 45, `cur` spans **2707 (Gawn, 35) →
9252 (Jackson, 25)** — a 3.4× spread that is pure age/runway. So the calibration is **age-conditioned
throughout**. "Under-priced" is **reference-dependent**, and the two references answer different
questions — both are reported, and keeping them distinct is itself a finding:
- **Marginal / proportional reference** (the owner's frame, item 131: "3–4× more above replacement, yet
  valued much lower relative to it"): does price reward output *proportionally*? Measured by the
  output→price **elasticity β**. **β<1 ⟹ the top is under-rewarded at the margin.**
- **Population-level reference** (is a cohort's absolute price high/low for its band): the signed
  mispricing surface `m`. An elite player can be well-priced vs the population (`m`<0) yet under-rewarded
  at the margin (β<1) — English is exactly this. The defect is in the **shape of the reward curve and
  the pick multiplier, not the absolute price level of any cohort.**

---

## 2. THE THREE NAMED AXES (measured fact)

### AXIS 1 — Top-output compression (item 131) — **CONFIRMED**
Price grows materially slower than realised output.
| map | n | elasticity β (log price ~ log output) | 95 % CI | reading |
|---|---|---|---|---|
| **Peak (age-neutral):** sustained-peak output vs peak price | 598 | **0.364** | [0.322, 0.411] | 2× the output → only 2^0.36 = **1.28× the price** |
| Current, age ≤22 | 19 | 0.111 | [−0.01, 0.29] | (thin; indicative) |
| Current, age 23–26 | 69 | 0.485 | [0.327, 0.728] | strong compression |
| **Current, age ≥27 (proven — English's regime)** | 212 | **0.683** | [0.465, 0.904] | β<1, CI excludes 1; matches item 131's implied 0.69 |

**Pairwise English / Briggs** (both RUC, `wage=0` so age is neutralised — the owner's exact pair):
current realised output **5.77×** (English +28.2 vs Briggs +4.9 above replacement) → priced **1.56×**
(3402 vs 2182); at peak **2.25×** output → **1.78×** price. The register quoted 2.99×→2.14×; **direction
confirmed, and on current output the compression is at least as severe** (Briggs has faded to +4.9 yet is
still priced 2182). The compression is a real property of the output→price map, worst at the top.

### AXIS 2 — Mid-round pick trough (`iso_corr`, item 132) — **CONFIRMED, RUC-severe, remains in full**
`iso_corr(pos, pick)` is a pure function of position × draft pick — **no evidence / age / tenure term** —
multiplying value at every valuation site, every year, permanently. It is **non-monotone**: a *better*
(earlier) pick can carry a *worse* permanent multiplier.
| pos | pick-1 | trough min (pick) | pick-34 | max permanent haircut |
|---|---|---|---|---|
| **RUC** | 1.069 (+6.9 %) | **0.815 (pick 32)** | 1.000 | **−18.5 %** |
| GEN_DEF | 1.000 | 0.913 (pick 28) | 1.024 | −8.7 % |
| GEN_FWD | 1.075 | 0.930 (pick 29) | 1.032 | −7.0 % |
| KEY_DEF | 1.000 | 0.943 (pick 32) | 0.992 | −5.7 % |
| MID | 1.000 | 0.949 (pick 28) | 1.025 | −5.1 % |
| KEY_FWD | 1.161 | 0.968 (pick 29) | 1.000 | −3.2 % |

For **RUC**, all of picks **19–33 carry a permanent −10 to −19 % haircut** while pick-34 escapes at
1.000 and pick-1 gets +6.9 % — the specimen item 132 named (English pick-19 → **0.885**; Grundy pick-22 →
0.819; Gawn pick-33 → 0.82). **38 genuine contributors sit in the trough picks 13–34** (English, Gawn,
Grundy, Merrett, Liberatore, Miller, Hewett, …). The trough is **structural and UNCHANGED by the trio
store reprice** (perez/mcandrew/keane were a store patch; `iso_corr` is a pos×pick function — the trio
touched none of it). **What remains = the whole table**, and its bite is RUC-concentrated. Other
positions have only a shallow late-20s dip.

### AXIS 3 — Young cohorts (item 130) — **conditionally under-priced (by design); unconditionally over-priced**
Two truths, both measured on matured cohorts (draft class ≤ 2021, busts kept):
- **Star-track (players who realised above replacement):** the young Yr1 price was **below** the value
  their realised peak output implies — realised-fair / young-anchor ≈ **1.4× (picks 1–6) → 7.7× (picks
  51–70)**. The convex upside is under-weighted when young, **more so at lower picks** (which get less
  pedigree credit yet still produce stars — Gulden pick-34, Newcombe pick-90). *This is measured through
  the already-compressed peak map (β 0.36), so it is a conservative floor on the under-pricing.*
- **Unconditional (all drafted, busts included):** the median matured player's `cur` collapses to a few
  percent of the Yr1 anchor — the draft-pedigree anchor **over-states** realised value for the median
  pick. Sanders is the exemplar: pick-6, realised `o_top3 = −2.5` (below replacement so far), yet `cur =
  4220` — priced on pedigree + runway, not realisation.

**Verdict for the guard:** young star-track is already under-priced vs realisation — **so any net-cutting
cure on the young side is wrong-direction as measured law (item 130 satisfied).** The under-pricing is
by-design per item 131 (the cohort guard 1.20–1.30 encodes the tolerance); this number is the
**baseline** against which a cure is scored (does it widen the young gap / eat guard headroom), **never a
mandate to lift.**

---

## 3. THE SIGNED MISPRICING SURFACE (under-priced positive) — `cohort_calibration.csv`
`m = log(output-mult) − log(price-mult)` within age band (population reference). At cohort resolution
**most cells are not distinguishable from fair** (bootstrap CI spans 0) — the systematic signal is the
compression (β, Axis 1) and the pick trough (Axis 2), **not** cohort-specific price-level anomalies. The
few cells whose CI excludes 0:
- **UNDER-priced:** `GEN_FWD × age 23–26` (m +0.57, CI [0.17, 1.01], n=14) — prime general forwards
  (Rankine, Mansell, T. Thomas) priced modestly for their output.
- **OVER-priced:** `GEN_FWD × age ≥27` (m −0.77, CI [−1.45, −0.12], n=29 — faded veterans on the
  retained-value floor: McGlynn, Gray, Mayne) · `age ≥27 × pick 1–6` (m −0.76, CI [−1.27, −0.27], n=30 —
  early-pick veterans: Naitanui, Roughead, Brayshaw).
**Read `m` with its reference:** English is `m −1.41` (his absolute price is *high* vs the ≥27
population) **while being under-rewarded at the margin (β<1) and iso-demoted (−11.5 %)**. The surface is
the population backdrop; the owner's mispricing lives in the *curve shape* (Axis 1) and the *pick
multiplier* (Axis 2), which `m` deliberately does not fold in.

## 4. WORKED ROWS — `worked_rows.csv`
| player | pos | age | pick | realised o (rec-2 / peak) | price cur / peak | iso_corr | axis it lands on |
|---|---|---|---|---|---|---|---|
| **Timothy English** | RUC | 29 | 19 | +28.2 / +39.8 | 3402 / 8399 | **0.885** | compression + RUC trough (both) |
| **Kieren Briggs** | RUC | 27 | 34 | +4.9 / +17.7 | 2182 / 4723 | 1.000 | the compression reference; escapes the trough |
| **Ryley Sanders** | MID | 21 | 6 | +4.1 / **−2.5** | 4220 | ~1.0 | young pedigree > realisation (item 130 unconditional) |
| **Marcus Bontempelli** | MID | 31 | 4 | +46.8 / +51.3 | 3773 / 7976 | ~1.0 | top output, runway-discounted at 31 |
| **Jai Newcombe** | MID | 25 | 90 | +21.1 / +22.2 | 4193 | ~1.0 | late-pick star — young under-pricing realised |

**English end-to-end (the owner's case, quantified):** 3–6× more above replacement than Briggs → priced
1.56×. Two independent mechanisms, both on the proven side: (1) the output→price compression (β<1) under-
rewards his output advantage; (2) `iso_corr` docks him a permanent −11.5 % for pick-19 while Briggs's
pick-34 is un-docked (+0 %). Age is not the driver (both `wage=0`). A proven-side defect, end to end.

## 5. Limits (what the numbers do NOT support)
- The contributor pool is 300; fine cells (position × age × pick) thin fast — refinement is support-gated
  and pooling is declared in the CSVs. Cells marked `POOLED/withheld` (n<12) carry no verdict.
- `m` is population-referenced; it is **not** a proportional-reward measure and must not be read as "this
  cohort's price is right/wrong" in the owner's marginal sense — that is β and the iso table.
- Realised output uses `Ppath` (era-adjusted SC average); the book carries no per-season games count, so
  cameo seasons are not weight-adjusted — mitigated by recent-2 / top-3 summaries (sensitivity in the
  CSVs). Age for ~non-board young players is `18+tenure` (flagged `age_est`).
- Instrument 2 (young) is right-censored for active players → restricted to matured cohorts; present
  cohorts (C ≥ 2022) get the current map only.
- This is one runner's regeneration; the seal hash is a machine fingerprint (§0), content bounded 99.6 %
  exact to the canonical board.
