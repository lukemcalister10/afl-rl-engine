# PREREG — ORDER 33 SEAT W2: THE FORWARD CALIBRATION (hindsight-correct year-1 class level and spread)

Registered and pushed BEFORE any result number is computed. Read-only mandate: measure and report;
no engine/board/law change. Program brief: issue #334 comment 5312369107.

## 0. THE OWNER'S PRIOR — REGISTERED FIRST, AS COMMISSIONED

Ruling R-CAL (2026-08-17): the year-1 entry class should in aggregate appreciate over its entry
values with **floor 1.03, ideally ~1.08**. This is registered as a **LOOSE PRIOR, not a target**.
This measurement is commissioned to PROPOSE the right number from hindsight on historical classes.
Commitment: if the data says 1.02 or 1.12, that is what the packet will say. No fitting to taste.
Hard constraint that binds any proposal regardless of the data: yr0->1 class appreciation must stay
**under the 14% carry cap** (no-arb law; current all-arm instrument reads +3.76%, margin +10.24).

## 1. OBJECTS AND IDENTITY (asserted before the run; the run HALTS if any fails)

- Primary object: the walk-forward per-entrant matrix
  `/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/per_entrant_O31FFINAL.json`
  - file md5 (full) must equal `d97f1aee4161ebcf785cd635ed095038`
  - `meta.store_md5 == "cb38ef11"`, `meta.engine_head == "71d9949a"`, `meta.n_records == 2648`,
    2648 unique keys.
  - `vpath[i]` = the engine's own as-of valuation at year `yrs[i] = entry_year + 1 + i`; `v0` = the
    landed entry-law day-0 price (29C basis). Year-1 vantage price P1 = `vpath[0]`.
- Ground truth ruler: the Order 32 S4 delivered-value construction, REUSED not reinvented, lifted
  verbatim from `docs/evidence/order32_s4_2026-08-17/s4_shootout.py` (commit history: prereg bf39901):
  season value `SV(year) = w_sqrt(games) * posval(avg + capt_prem(avg) - BARS[bar]) * 21`, with the
  S4 constants (BARS, S_SH=3.0, LCAPT row, w_sqrt = min(1, sqrt(g/10))); discounted delivered value
  from vantage Y: `dvrest(Y) = sum_{t>Y, t<=2025} 1.14^-(t-Y) * SV(t)`. LAST_REAL_SEASON=2025,
  ENTRY_FLOOR=2005, force-majeure exclusions {paddy-mccartin, thomas-boyd} — all as in S4.
- Candidate law constants for interpretation only (rho steepness translation):
  `engine/rl_after/_merged_recover.py` lines ~3181-3230; `rho(g) = 1 - exp(-(g/29.194254)^0.801542)`
  (O31_TAU_RHO, O31_B_RHO), transcribed from `docs/evidence/candidate_31f/LAW31F.json`.

Noted identity fact (recorded as-found, before results): the mandate quotes the CURRENT BOARD year-1
class as 105 rows at 1.009x entry. The registered matrix's own 2025 class is **103 rows** and its
walk-forward yr-1/entry aggregate reads **1.0330** (structural check during prereg; the board and the
walk-forward matrix are different vantages of the same machinery). The matrix is the registered
object for every number in this packet; the board figure is quoted context only. The discrepancy is
reported, not reconciled.

## 2. POPULATION

- Classes = entry years **2005..2021** (futures observable at the year-1 vantage through 2025).
  All-arm (ND + RD + MSD + OTHERPOOL by the S4 `arm_of` rule) is the PRIMARY population — matching
  the all-arm cohort instrument the no-arb margin is quoted on. ND-only is reported as a secondary
  cut. Force-majeure keys excluded. Structural fact recorded pre-run: every 2005-2021 record carries
  an arm; vpath[0] exists for every 2005-2021 record (min-tenure rule 338), so the year-1 vantage
  has no survivor exclusion.
- Two horizon conventions, both reported:
  - **FULL**: all observed seasons through 2025. Complete tails only for early classes; classes
    2016+ carry increasing right-truncation — disclosed per class, with the truncation share.
  - **H6** (primary for era comparability): fixed 6-season window from each vantage —
    DV0_H6 uses seasons yr+1..yr+6 discounted from yr; DV1_H6 uses yr+2..yr+7 discounted from yr+1.
    Full H6 windows exist for classes **2005..2018**; that is the H6 class set.

## 3. QUESTION (a) — LEVEL. Prereg'd estimator.

Per class c: P0_c = sum v0, P1_c = sum vpath[0]; DV0_c = sum dvrest(entry year), DV1_c = sum
dvrest(entry year + 1). Report per class:
- Candidate's mark: R_cand_c = P1_c / P0_c.
- **PRIMARY hindsight-fair appreciation: R*_c = DV1_c / DV0_c** — the ratio a perfectly-informed
  price path would have shown, independent of any level bias between the price language and the
  delivered-value language. Identity (mechanical, from the ruler's own recursion): R*_c =
  1.14 x (1 - SV1share_c) where SV1share_c = SV_yr+1 / (SV_yr+1 + DV1) — so R* < 1.14 by
  construction: the no-arb cap is respected automatically, and the fair appreciation equals the
  carry times the fraction of forward value NOT delivered in year 1.
- Level diagnostics: K0_c = DV0_c/P0_c, K1_c = DV1_c/P1_c (language-level calibration of the entry
  basis and the year-1 mark); secondary reading DV1_c/P0_c (the "unbiased-in-ruler-units" mark).
- Distribution across classes: per-class table (both conventions), mean/median/IQR, era split
  2005-2014 vs 2015+ (H6: 2015-2018), and class-bootstrap 90% CI on the pooled central value
  (resample classes, B=2000, seed=33). Era instability is reported plainly if present.

## 4. QUESTION (b) — SPREAD. Prereg'd estimators (all at the year-1 vantage, H6 primary).

Normalization: within class c, price share x_i = P1_i / mean_c(P1), realized share y_i =
DV1_i / mean_c(DV1). Pooled across classes 2005-2018 (H6).
- **S1 calibration slope (primary)**: OLS y ~ a + b x pooled on shares. b > 1 = candidate spread
  too FLAT (hindsight wants steeper); b < 1 = too aggressive. Player-cluster bootstrap (B=2000,
  seed=33) 90% CI; per-class slopes and per-era slopes reported. Robustness: slope with y,x
  winsorized at the 99th pct, and Spearman rho.
- **S2 two-leg regression**: production leg PROD_i = SV(yr+1)_i (house-scored year-1 season, 0 if
  no games), pedigree leg PED_i = v0_i, both in class shares. Hindsight: y ~ b_prod PROD + b_ped PED
  (+intercept). Candidate: x ~ c_prod PROD + c_ped PED (+intercept). Verdict statistic: the weight
  ratio W_hind = b_prod/b_ped vs W_cand = c_prod/c_ped. W_hind > W_cand = hindsight loads more on
  the production leg than the candidate price does = rho's evidence response too shallow.
- **S3 low-g cells**: buckets by games_yr1 {0, 1-4, 5-9, 10-15, 16+}; per bucket, mean price share
  vs mean realized share (mispricing = y-x). Within buckets 1-4 and 5-9: tercile split by year-1
  production SV(yr+1) among g>=1 rows — were risers underpriced and poor starters overpriced?

## 5. QUESTION (c) — PROPOSAL RULE (fixed before results)

- LEVEL proposal: the central value of R*_c on the H6 convention over the most era-relevant stable
  set (all classes if era-stable; the later era if the eras disagree materially, with the earlier
  era bounding). Uncertainty: class-bootstrap 90% CI + era range. Constraint: proposal < 1.14; if
  the data-implied number breaches the floor 1.03 or the ideal 1.08 in either direction, it is
  reported against the prior without adjustment.
- SPREAD proposal: if S1 slope b's 90% CI excludes 1, propose scaling the within-class evidence
  response by b — translated to rho as the tau' that solves rho'(g_med) = min(0.95, b x rho(g_med))
  at the cohort median games_yr1 g_med (same B_RHO shape), reported alongside the raw b so Order A
  can wire it any equivalent way. If the CI includes 1, propose NO steepness change.
- Both proposals carry the falsification criteria of SS6.

## 6. ACCEPTANCE BANDS FOR ORDER A (Candidate 32) — form fixed now, numbers filled by the data

Scored on THIS instrument (same matrix construction re-emitted for Candidate 32, same S4 ruler,
same class set, H6 convention):
- LEVEL band: Candidate 32's year-1 class aggregate mark (2025 class on its board, and the
  historical-class mean R_cand under walk-forward) must land inside [propose_lo, propose_hi] :=
  the class-bootstrap 90% CI of the LEVEL proposal, widened to the era range if eras disagree; hard
  fail outside [1.00, 1.14). FALSIFIED if the historical-class mean R_cand differs from R* central
  by more than the era range on the outside, or breaches the carry cap.
- SPREAD band: the recomputed S1 slope on Candidate 32 prices must have its point inside
  [1 - w, 1 + w] where w = half-width of the S1 slope 90% CI measured here (i.e., the build must
  move the slope to statistical indistinguishability from 1). FALSIFIED if the recomputed slope CI
  excludes 1 on the same side as the candidate's current miss (no improvement) or overshoots past
  1 by more than the candidate's current miss (overcorrection).
- The G*=2 sitter credit / delivered-season reset / stall bars in Candidate 32 must not push any
  class's walk-forward yr0->1 aggregate above 1.14 (no-arb law) — one breach falsifies.

## 7. HONESTY CLAUSES

Per-class dispersion always shown, never only the pooled number. Era instability reported plainly
and the proposal bounded by it. Right-truncation shares disclosed per class on FULL. The owner's
prior is echoed next to the answer, whatever the answer is. Zero degrees of freedom left open:
constants above are final; anything else found necessary is reported as a deviation in the packet.

Seat W2, 2026-08-17. Registered before computation; results follow in PACKET_W2.md.
