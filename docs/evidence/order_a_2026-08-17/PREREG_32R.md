# PREREG_32R — THE CANDIDATE 32 REPAIR (owner-directed; supersedes the two halts as posed)

**Pushed BEFORE any repair edit.** Authority: the coordinator's repair order relaying the owner's
word. Base: Candidate 32 as shipped (`SHIPPING_PACKET_32.md`, board `6477f6f4`). Laws unchanged:
everything behind `RL_O32`; dial-off stays byte-exact `fe6be9d6`; day-0 prints unmoved; the 1.14
line is hard; halt-and-report outside this scope. The uniform lift is NOT wired and Halt 2 is NOT
decided — this order replaces both.

## The defect being repaired (owner-caught, in plain words)

The re-mix moves price weight onto a young player's shown production — but it reads that
production against the MATURE replacement bars. S1 measured that those bars flag 86–100% of
age-18/19 seasons even on careers that turn out fine. So the re-mix marked down almost every good
young player (dean −136, duff-tytler −196), and W2's "poor starter / riser" buckets were poisoned
the same way: young talls pile into "poor" just for being young. The gate bars were age-corrected
in the build; the production reference the re-mix leans on was not. This repair makes the NEW
mechanisms age-consistent end to end.

## R1 — the age-relative production reference (exact form, fixed here)

- **Engine (stage 6 only).** The re-mix's added production weight credits shown production at the
  player's age-appropriate expectation: the production term becomes
  `rho31_base(g)·Phat + κ·m_u(g)·(1−rho31_base(g))·(Phat + A(p,Y))`, with
  `A(p,Y) = Δ(age at Y, class)·20·_PL_F` — the S1 C3 development gap expressed as one 20-game
  season at Δ points per game, in engine currency; zero from age 24 (cap law), zero at g=0
  (m_u(0)=0, so day-0 prints cannot move). The PRE-EXISTING production leg (`Phat`, ρ31 base) is
  untouched — the same gate-only scope discipline as the bars. The pedigree side keeps its ρ2
  weights and mix factor unchanged in form.
- **The corrected hindsight surface.** W2's scorer machinery re-cut with the shown-production
  classifier age-adjusted: `sv1_age` = the same S4 ruler with the season's bar replaced by
  `bar − Δ(age at the season, class)` (flat from 24). The OUTCOME ruler (delivered value, flat
  bars) does not move — only how a year-1 season is CLASSIFIED as poor/mid/riser and the prod-leg
  regressor in the two-leg W. New targets: the corrected terciles' realized shares and the
  corrected hindsight W band (its 90% CI).
- **Re-calibration.** (κ, γ_u, η, γ_d) re-fit on the corrected surface, objective = n-weighted SSE
  on the corrected cells+terciles, feasibility = {slope ∈ [0.885, 1.115] ∧ W ∈ the corrected
  hindsight CI ∧ max class ≤ 1.139 ∧ ρ2 monotone ∧ the at-bar continuity object on the ledger's
  rows}. Grid as in `REMIX_32.json` with the A-credit live.

## R2 — the residual, properly cut

Re-run the class-level attribution on the corrected surface over: pick band (1-10/11-20/21-30/
31-40/41-64/ND>64) × age at entry (≤18 / 19 / 20 / 21+ ) × position group (TALL=KPD+KPF / RUCK /
SMALL) × pathway (ND/RD/MSD/other-pool). Per cell: the candidate's year-1 mark ratio
(Σp1/Σv0) against the cell's OWN hindsight-fair ratio (Σdv1_full/Σdv0_full), n and value weight.
Publish every cut table. "Uniform" may be claimed ONLY if flat across ALL axes. Prediction
(the owner's hypothesis, adopted): the residual is NOT uniform — it concentrates in the LATE pick
bands (31-40, 41-64) and the youngest ages; the closure is cell-wise via R1's age credit + the
recalibrated re-mix. If a genuinely flat component remains after honest cuts: halt with the
tables.

## R3 — two-sided, five-band no-arb as standing gates

- The 338 instrument runs with the owner's five bands STANDING via the disclosed
  `t338_extended_DISCLOSED.py` pattern (bands 1-10/11-20/21-30/31-40/41-64, years 0..12), on the
  repaired matrix and the C31 control.
- A SELL-SIDE leg joins every table: any window/band with yr0→1 appreciation < 0 flags **RED**
  regardless of the buy-side margin; both sides printed everywhere (buy-side margin = 14% −
  appreciation, arb iff < 0; sell-side = the appreciation itself, red iff < 0).
- State to beat: picks 1-20 +8.74% vs 21-64 −8.29% (17.0-point spread); MODERN all-arm −2.91%.
- **Acceptance targets:** after R1+R2, no five-band yr0→1 appreciation below 0, and the five-band
  spread (max−min) materially narrowed — prereg'd as: spread ≤ half the pre-repair five-band
  spread (measured on the pre-repair matrix in the first R3 run and quoted before the repair
  numbers). Exact per-band numbers reported either way; misses are halts, not adjustments.

## R3(c) — the vantage-consistency matrix (owner addendum, his own arithmetic)

The owner's finding on the shipped C32 tables: from the year-1 vantage, picks 21-64 are priced to
grow +60.8% over yr1→5 while picks 1-20 grow +36.3% over yr1→6. Two bands of one asset class
cannot both be fairly priced while expected to grow at wildly different rates from the same
vantage: fair pricing puts every band's forward growth near the carry from EVERY vantage year.

- **The matrix, standing:** for each of the five ND bands and the two all-arm windows, the implied
  forward growth yrV→yrV+k for vantages V = 0, 1, 2 and horizons k = 1..4, printed beside the
  carry benchmark (1.14^k), with the band-vs-band spread at each vantage explicit.
- **Acceptance:** the yr1-vantage forward-growth spread between any two ND bands must narrow
  materially from the current ~25–30 points; exact before/after reported. If a residual spread
  survives the corrected calibration, BOUND it and attribute it to the leg that carries it
  (late-band yr1 marks too low vs early-band yr1 marks too high) — never averaged away.
- **Both directions examined, per the owner's note:** 21-64 yr1→5 +60.8% is close to carry-fair
  (+68.9%) while 1-20 yr1→6 +36.3% is far under (+92.5%) — so the correction is expected to RAISE
  late-band yr1 marks (R2's hypothesis), and the early-band yr1 marks are examined for being too
  HIGH rather than assuming one side only.
- Printed in the delivery in plain language with the carry column beside it.

## R4 — re-run and re-deliver

Full suite: corrected-surface W2 bands · S4 recovery re-check · five-band two-sided no-arb ·
continuity incl. the carmichael one-game case · completeness · day-0 (89/89 AND byte-identical to
`fe6be9d6`'s prints) · determinism · both dial-off identities · refreshed movers ledger + both
preview pages · named rows traced: dean, duff-tytler, wilson, gothard, madden, scerri, burton,
murdock, annand, cooke + late-pick young rows gallop (ty-gallop), charlie-west, dodson, mccabe,
busslinger. Packet addendum and final report in PLAIN LANGUAGE (short sentences, terms defined).

## AMENDMENT A1 (owner addendum 2, filed before the affected analyses ran)

- **Pool arms join the standing tables.** Every no-arb delivery includes the per-arm pool table
  (RD / MSD / UNR / IRE / PDA / PDN / SSP / PDS year-paths, both windows) AND the pooled all-pool
  path (every non-ND arm, the all-arm reader construction), under the SAME two-sided rules: sell-
  side RED for any arm with negative yr0→1; buy-side RED for any arm whose yr0→1 appreciation
  exceeds the 14% carry. Arms join the R3(c) vantage-consistency matrix. MSD's yr1 cell carries a
  plain-words caption for the debut-gap exclusion — never a silent nan.
- **Named breach to investigate (NOT wire): SSP.** yr0→1 +51.0% in C32 (+38.2% in C31), n=31 —
  thin, bound honestly. Hypothesis to test: the SSP entry cells (v0 ~124–209) price development-
  class entries while SSP entrants are mature-age and convert production immediately. Report the
  finding and the candidate fix direction (likely an SSP entry-cell re-anchor at the next v0
  refit); an entry-surface change is rulings-material and is NOT wired here.
- **R3(c) diagnosis refinement (supersedes the 'early yr1 marks too high' line).** The fair yr1
  level PER BAND = 1.14 × (1 − that band's yr1 delivered share). Compute the band-level fair yr1
  numbers explicitly (early picks deliver more in yr1, so their fair yr1 sits BELOW the class
  ~1.10; picks 1-20 at ~1.087 is close to fair on that test). Attribute each band's vantage
  inconsistency to the specific leg — the yr1 mark vs the later-year marks (the remaining S4
  mid-career residual) — against the band-level fair benchmarks, never by averaging.
- **Continuity gate precision note:** feasibility tests the ruled ledger gate EXACTLY (integer
  game steps 0..20, tolerance 1e-9, at-bar rows); the first diagnosis run's 0.25-step check was
  stricter than the ruled object and is retired.

## AMENDMENT A2 (owner-directed, binding — filed before the re-calibration's chosen point was wired)

- **The vantage matrix is DIAGNOSTIC-ONLY.** The R3(c) acceptance language ("the yr1 cross-band
  spread must narrow materially") is STRUCK. Nothing in this repair is calibrated toward the
  matrix; no parameter choice may be justified by its effect on the cross-band spread. Permitted
  changes remain exactly R1 (justified by the measured age-gap surface) and R2 closures
  (justified by the attribution's own published cut tables). The matrix REPORTS the surviving
  divergence as a red-printed FINDING with candidate root causes ranked by evidence. If two
  evidence-equivalent parameterisations differ only in matrix greenness: stop and report both.
- **Procedural consequence, disclosed:** the recalibrator's draft selection rule preferred
  feasible points where all five bands appreciate. That preference is REMOVED (selection = min
  corrected-surface SSE among the ruled-gate-feasible set, full stop). On the measured grid the
  preference was VACUOUS — the feasible set has one point — so the chosen point is unchanged;
  the rule is cleaned so the provenance is clean.
- **R2 gains three named investigation lanes (measure, don't assume; report positive or null):**
  L1 late-pick entry value too low (connect to S5's loclin −9% head-underpricing finding);
  L2 the v0 level per band as the divergence source (band-level price-to-delivered multiples);
  L3 band-dependent sitting predictiveness — P(washout | low yr1 games) by pick band and the
  fade/credit channel's predictive strength by band (the year-one selection interaction, which
  the 30A multi-year lens scan did NOT test). If the signal is materially weaker down the draft,
  the implied band-dependent correction is RULINGS-MATERIAL: reported, never wired here.

## AMENDMENT A3 (owner round — named evidence for lane L2, filed before the lane ran)

Named facts to carry into L2: on the C32 matrix (yr0–12 extension, all-arm construction) PDN's
cohort path PEAKS at 0.862 and PDS at 0.720 — both arms never regain their entry value at any
year. S7's own-arm raw-mean ratios: PDS/PDN/IRE delivered history = 0.27 / 0.59 / 0.73 of their
signed v0 cells (the K-shrink borrowing made visible). Together: the thin development arms' entry
cells sit ABOVE own-arm delivered history — the owner's "priced too high to begin with" hypothesis
is likely TRUE for PDN/PDS (partially IRE), the borrowing being the located mechanism. Report as a
formal L2 finding with the candidate fix (own-arm re-anchor of those cells at the next v0 refit —
rulings-material, no entry-surface change wired here). Contrast case in the same lane: SSP entry
too LOW (the +51% yr1 buy-side breach of amendment A1). The big-arm (RD) ambiguity stays with the
leg-attribution machinery (entry fitted career-fair by construction vs yr1–3 marks too low).

## Predictions

- **PR1** dean and duff-tytler recover toward Candidate 31 or above (the age credit offsets the
  poor-side re-mix leg); taylor/annable (2-game, below even age expectation) stay down.
- **PR2** the corrected terciles move young talls out of "poor"; the corrected hindsight W is in
  the same region as the flat-bar W (the CI overlaps [0.08, 0.17]).
- **PR3** the class mean rises from 1.0334 toward the band; the residual cuts show concentration
  in bands 31-64 and ages ≤20, NOT uniformity.
- **PR4** the five-band table shows the late bands' negative yr1 appreciation shrinking toward 0;
  whether it fully clears 0 is the R3 gate and is reported, not assumed.
- **PR5** S4 years-4–6 recovery stays positive (the repair touches the re-mix, not Φ/D/reset).
- **PR6** all byte identities hold; day-0 prints unmoved; determinism holds.

*— Order A seat, repair leg, 2026-08-17. Committed before any repair edit.*
