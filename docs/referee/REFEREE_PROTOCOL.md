# ITEM 410 — ORIGIN-SAFE REFEREE PROTOCOL (AUD-004 ACTIVATION) · DRAFT v0.3 · design seat · 2026-07-24 · NOT FROZEN · DIALS RULED · PEAK DOOR OPEN

Authored read-only at the ITEM 410 design seat against main `13b1618` (register v393). This seat makes
no repo writes; the deliverable routes to the owner; the pen files.
Governing law: RULEBOOK v2.0 — cited by prose law number; gates bound to `docs/acceptance_v2_0.json`
gate IDs per the v393 law-count mapping of record. Referee-specific gates carry REF- IDs; they enter
the acceptance twin only on owner word (Law 10).
Evidence base: ITEM 409 EVIDENCE MEMO as filed (identity f37d9716 / 6f07f7cb / 89c14729; pack-3
workbook md5 e921bd05) — carried as filed, that seat's measurements, re-run rights reserved.
AUD-004 standing: no standalone AUD-004 specification exists in the tree (verified at `13b1618`:
mentions live only in the register header, the memo, and the ITEM 410 charter; archive clean). The
memo carries it as owner-ruled with reopen trigger "before the next material valuation-changing
bake" — that trigger is now. On freeze, THIS document is the AUD-004 specification of record (SSI:
one document per concept; the dangling reference ends here).
Scope: FORECAST-CORE REFEREE ONLY (owner split ruling, 2026-07-24). Pricing-layer validation —
replacement bars, production→SCAR mapping, V_free — is the carried NAMED QUESTION and its own later
design deliverable. Pricing-layer gate IDs (G-MONO, CONSERVATION, L-CAPTAIN, LENS-PROJECTION, G-Y0,
G-COHORT) bind at that layer, not here; the charter's architectural separation is what makes that
boundary clean.
Freeze status: DRAFT, dials ruled (owner words 2026-07-24, this channel; §12 records each with
its provenance). OWNER PEAK-HORIZON READ OF RECORD (owner's words, 2026-07-24, this channel): the
three-season headline stands, but for young players — especially key-position players and rucks —
the value question is the PEAK, often four to six seasons away, not only the next three. Encoded
at §4 M8, §5.1 TALL-DEV slice, §7.5 guardrail AND open admission door (owner word "Open it,"
2026-07-24), §8.3 always-mapped row; compliance line in §11.
Preconditions §10. No official scoring before freeze.

## 1 · OBJECT AND STANDING
One immutable adjudication instrument for the best-model race: identical folds, identical metrics,
identical scoring for every contestant. The referee decides ADMISSION of ingredients to the governed
core and reports the race; it never decides adoption (Law 10 — owner-only words) and never bends to
a result. The referee is also the instrument that unblocks AUD-007 (layer interaction / signal
reuse, carried from the memo): the joint-refit discipline (§7) and the signal-reuse diagnostic
(§5, D3) are exactly what AUD-007 was waiting for.

## 2 · PANEL AND FOLDS
2.1 **Panel.** Cell = (player p, cutoff year t). Inclusion: p has ≥1 AFL game in seasons ≤ t, drawn
from the ONE SOURCE's per-year scoring (Law 1 / ONE-SOURCE; the panel is derived, read-only,
source-stamped). Fields available to candidates: per-season games and scoring averages ≤ t; age;
position-as-of-t where the store carries it, else declared missing — never backfilled from later
seasons; entry pathway and pick; captaincy history ≤ t; availability history ≤ t.
2.2 **Cutoffs.** t ∈ {2009, …, 2024} for Y+1 targets; t ∈ {2009, …, 2022} for Y+1..Y+3;
t ∈ {2009, …, 2019} for the Y+1..Y+6 peak window (M8). The floor
aligns with the committed book machinery's span (2009–2026); the pack-2 panel's 2005–2008 cutoffs
remain design evidence. Targets use complete seasons only; 2026 is excluded from targets while
live. Scheduled extension: each completed season appends one cutoff under these identical rules —
a scheduled event, not an amendment.
2.3 **Fold rule.** For each t: train = all data ≤ t; test = targets > t. All parameter fitting,
transform fitting (normalizations, percentile maps, position groupings), and hyperparameter
selection happen inside train. Capacity dials (regularization and smoothness strengths) tune on an
inner chronological split — the final three train seasons as inner validation; plain coefficients
fit on full train.
2.4 **Identity.** The panel builder is deterministic from the store; panel md5 and fold-spec md5
pin at harness build and stamp every scorecard (gate REF-FOLD, HALT on mismatch).

## 3 · ORIGIN-SAFETY FENCES
3.1 **As-of law.** No feature, transform, or parameter may use information from seasons > t —
including indirect routes. The three present-state leaks the memo found in existing replay
machinery are named regression probes here, each HALT-not-warn (Law 2 / SILENCE-IS-RED):
- **REF-LEAK-1** — peak_est (and any successor) receives as-of-t career totals only, never
  full-history aggregates.
- **REF-LEAK-2** — position at t comes from ≤t data or is declared missing; a current-season-only
  field never enters a historical cell.
- **REF-LEAK-3** — no live-season progress constant (the SEASON_PROG=0.79 class) is applied at any
  historical year.
3.2 **Incumbent exception, declared.** The incumbent (C1, §6) races AS-IS with its full leakage
inventory attached (18 inputs; parameters full-history-fitted; per the memo). Predeclared
asymmetric-validity rule: results AGAINST the incumbent are a fortiori valid; results FOR it over
origin-safe contestants carry the leakage label and decide nothing. No other contestant may carry
leakage.
3.3 **Ceiling included.** The ceiling (§8) obeys every fence in §3.1 — a leaky ceiling sizes a
fictional prize.

## 4 · TARGETS AND METRICS (predeclared; the charter's five families, made exact)
Targets per cell: realized games and games-weighted scoring average in the window; standing =
percentile of realized games-weighted production among same-cutoff eligible cells (the pack-3
rp_pct construction); attrition indicator = zero games at Y+1.
- **M1** · Level wMAE, Y+1 — weighted by realized Y+1 games; conditional on ≥1 game.
- **M2** · Standing wMAE, Y+1 — same weighting and conditioning.
- **M3** · Level wMAE, Y+1..Y+3 — games-weighted across the window; conditional on ≥1 game in it.
- **M4** · Standing wMAE, Y+1..Y+3 — **HEADLINE (Dial-1 — RULED, owner word 2026-07-24)**. Rationale: ordering at the multi-year
  horizon is what dynasty pricing consumes, and it is where the memo's verdict and the age-tilt
  finding live.
- **M5** · Career-remaining — for cutoffs where ≥90% of the cohort's careers are complete by panel
  end (career deemed complete when the last game season ≤ panel end − 2): predicted vs realized
  remaining games-weighted production, level and standing forms; censored cells excluded and
  counted.
- **M6** · Attrition log-loss, Y+1 — per-cell log-loss on P(zero games); unweighted; reliability
  curve reported.
- **M7** · Calibration curves (diagnostic, non-binding) — predicted vs realized percentile by lens
  band; the F1/F2/F5 instrument; the transition-width study reads from here.
- **M8** · Peak window, Y+1..Y+6 (owner peak-horizon read, 2026-07-24; numbered after the original
  seven so prior references stay stable). Realized peak = the maximum seasonal games-weighted
  average across Y+1..Y+6; predicted peak = the maximum of the candidate's predicted season means
  over the same window. Scored in level and standing forms — standing = percentile of realized
  peak among same-cutoff eligible cells — with cell weight = games in the realized peak season,
  so flukey short-season peaks weigh little without any hard floor (weight-don't-gate).
  Conditional on ≥1 game in the window; censoring counted. Long-window attrition is not smuggled
  in here — M6 and D2 score it; M8 answers one question: among those who played, did we rank the
  peaks right. The smaller cutoff set (§2.2) means wider margins, reported like every other.
Uncertainty: player-clustered bootstrap, B = 2,000, seeded; CI90 convention throughout (matches the
memo). Every reported number carries its margin; the three narrowest margins lead every scorecard
(rulebook Part 3). Anything unmeasurable in a run is reported UNMEASURED — never assumed passing,
never silently waived.

## 5 · LENS SLICES AND DECLARED DIAGNOSTICS
5.1 **Slices** — reporting bins only; estimator structure stays smooth (Law 3 / L-SMOOTH as applied
to estimators, per the memo's Addendum-2 constraint): age {≤22, 23–26, 27–29, 30+}; position groups
as-of t (confound caveat stands — position enters as a candidate INGREDIENT only via an
age-controlled race); draft pick bands {1–5, 6–20, 21–40, 41+, ND/SSP/other pathway}; career-year
{1–2, 3–5, 6–9, 10+}; evidence volume (career games at t: {≤10, 11–40, 41–100, 100+}) — the
thin-evidence lens the Mraz class demands. NAMED SLICE OF RECORD — **TALL-DEV**: age ≤22 ×
position group {key forward, key back, ruck} as-of t (owner peak-horizon read: the cohort whose
peak sits beyond the headline window). Position vocabulary is normalized at panel build and
declared in the harness claims note — no vocabulary mismatch may silently empty a slice (Law 2).
Every §4 metric reports per slice, for every contestant, identically.
5.2 **Declared diagnostics** (non-binding, always reported):
- **D1** · Cross-band vs within-band decomposition of standing error (the pack-3 pm_pct
  construction) — the finding that allocation, not within-band ordering, carries the error must
  stay visible round to round.
- **D2** · Unconditional expected-production check — the forecast distribution integrated over the
  zero-games branch vs realized production including zeros; catches level/attrition head
  interactions that conditional metrics hide.
- **D3** · Signal-reuse audit (the AUD-007 instrument) — for admitted ingredients sharing an input
  (age, games), joint-vs-marginal contribution per lens; double-encoding shows here.

## 6 · CONTESTANTS
- **C0 · BENCHMARK.** The five-constant shape (one recency λ + four-entry age-drift table; two
  ingredients). Constants RE-FIT per fold on train only — v391 applies to the benchmark too; its
  pack-2 values were in-sample. C0 is the governed core's seed.
- **C1 · INCUMBENT, frozen.** As-is, leakage declared (§3.2).
- **C1R · INCUMBENT RE-TUNED ("recalibrate").** The incumbent's mechanism set with parameters
  re-fit fresh per fold under §3 fences, per v391. This gives the recalibrate arm of the
  recalibrate-vs-rebuild fork its own measured lane — the owner's "middle" is raced, not argued.
- **C2 · GOVERNED CORE ("rebuild").** Grown from C0 by §7. Output contract: per-player distribution
  over future seasons (games, average) including the zero-games branch.
- **C3 · CEILING.** §8. Never adoptable — structurally: no ceiling output may enter any adoption
  artifact (gate REF-CEIL, HALT).
Every contestant emits a prediction for every target head; a head a contestant cannot emit scores
UNMEASURED on that metric and is reported as such (Law 2). C0 carries a declared base-rate attrition
head (per-age rates fit on train) so the benchmark scores all heads.
The recalibrate-vs-rebuild fork goes to the owner formally when C1R and C2 both hold referee
results (charter §5).

## 7 · MECHANISMS, VARIANTS, BUNDLES, SELECTION (the v391/v392 machinery)
7.1 **Registry.** The unit of admission is the MECHANISM CLASS. Every class registers before any
scoring: ID; one-paragraph mechanism story; parameter space with shapes allowed to generalize
(constants → smooth curves — Law 3 on estimators); structural guards asserted per candidate —
per-game recency weight monotone non-increasing in years-back (REF-RECENCY, HALT; the charter's
carried L-RECENCY constraint — not a rulebook law, bound here by charter authority), weight-don't-
gate (no hard evidence floors), and upside/downside evidence processed by identical machinery
(Law 5 / L-SYMMETRY); tuning procedure (train-only); lens hypotheses — where the mechanism should
help, which makes the interaction map targeted. Seed library from the charter: λ(age) arc; age
drifts; cohort blend w(age); career-year-indexed pedigree; attrition/survival; young-decliner
rebound; position (age-controlled race only); availability.
7.2 **Declaration seal.** A round's variant set and bundle set are declared to the referee ledger
and SHA-sealed BEFORE any test-fold scoring in that round (gate REF-SEAL: no official score without
a seal predating the run; HALT). Budgets (Dial-3 — seat-set under owner delegation, §12): ≤5 declared variants per class per
round; ≤3 bundles per round. Post-hoc variants after seeing results are barred; the next round may declare
afresh.
7.3 **Bundles.** An interaction bundle = two or more classes with a stated joint mechanism story,
tested and admitted or rejected as a unit, under the same seal and budget discipline. From round 2
onward, every bundle declaration must cite an interaction-map row (§8.3) or new external evidence —
evidence-guided hunting, not combinatorial brute force.
7.4 **Forward step.** Each declared candidate is evaluated by FULL JOINT RE-FIT: the current core's
parameters and the candidate's are re-tuned together on train folds — nothing holds its entry
settings (v392) — and out-of-fold scores computed. Screening may use approximations; any
admission-deciding run must be a full joint refit (gate REF-JOINT, HALT).
7.5 **Admission bar (Dial-2 — RULED: CI90 · peak door — RULED OPEN, owner words 2026-07-24).**
Admission = bootstrap-resolved out-of-fold gain (CI90 excluding zero) on the headline M4 **or** on
M8 (standing form, pooled) — the peak door — AND guardrails either way: no resolved regression on
M2, on M6, or on the non-door member of {M4, M8}, pooled or within any declared slice including
TALL-DEV; all structural gates green. Both doors' evaluations land in §7.9's published counts.
7.6 **Rejection record.** "REJECTED — not at any tested construction," with the tested space listed
in full (v391), so revisits are cheap and bounded: re-entry requires a newly declared variant set
plus a stated reason — a map row or new evidence.
7.7 **Backward pass (Dial-4 — RULED by owner adoption of the recommendation: after every
admission).** After every admission: each admitted ingredient is removed in turn
with the remainder jointly re-fit; an ingredient whose removal yields resolved gain is dropped and
recorded. Joint refit is inherent to every step, so the core never fossilizes at entry settings.
7.8 **Stopping rule.** The race stops when a round closes with zero admissions AND every resolved
interaction-map row has at least one declared-and-tested bundle against it — or on the owner's
word. The fork report (§6) then goes to the owner. Captured share is reported throughout:
(C0→C2 gain) / (C0→C3 gap), pooled and per lens — the ceiling sizes the prize and the stopping
rule reads from it.
7.9 **Multiplicity honesty.** The ledger counts every test-fold evaluation per round; budgets cap
the forking paths; the resolved-CI bar is the control. No per-test correction is applied; the count
is published.

## 8 · THE CEILING AND THE INTERACTION MAP
8.1 **Spec, frozen with the protocol.** One flexible learner (gradient-boosted trees or declared
equivalent), all §2.1 origin-safe features, per-fold fit with inner-split early stopping,
out-of-fold predictions only. Deliberately unconstrained by estimator-shape laws — which is exactly
why REF-CEIL bars its outputs from adoption artifacts forever.
8.2 **The prize.** Ceiling-vs-C0 and ceiling-vs-C2 gaps on M2/M4 with CIs: the size of the prize
and the denominator of captured share.
8.3 **The interaction map.** Each round: the C3−C2 gap on M4 — and on M8 where measurable — per
lens slice, and per slice-pair where cell counts stay above a declared minimum, ranked with CIs,
published in the ledger; TALL-DEV is always a mapped row. Rows whose CIs
exclude zero are RESOLVED ROWS — the hunting ground: bundle stories cite rows (§7.3).
Feature-attribution views of C3 are permitted as guidance, labelled report-only.
8.4 **Cache.** C3 out-of-fold predictions compute once per freeze (and per scheduled panel
extension) and are cached; the map recomputes against the evolving C2 each round.

## 9 · GOVERNANCE, IDENTITY, ENVIRONMENT
9.1 **Documents.** On filing: this protocol → `docs/referee/REFEREE_PROTOCOL.md`; an append-only
`docs/referee/REFEREE_LEDGER.md` (declaration seals, scorecards, admissions and rejections with
tested spaces, interaction maps, evaluation counts, amendments). One pen files both; the register
carries pointers, not copies (SSI).
9.2 **Seats.** The design seat authors (this document); build seats implement the harness post-408
under a written directive with identity pins; implementer ≠ reviewer: one cold blind review of the
harness against this protocol before the first official run (Law 11 / SEAM-PATTERN). Referee runs
are read-only with respect to store and engine; scorecards are [re-runnable] artifacts.
9.3 **Identity.** Every scorecard stamps: protocol version, panel md5, fold-spec md5, harness
identity, contestant registry entry, declaration-seal SHA, seeds, environment.
9.4 **Environment.** The known cross-environment float drift (board-determinism record) applies:
official comparisons within a round run in one pinned environment; a cross-environment difference
is a re-measurement to reconcile, never a result.
9.5 **Blocks and pre-history.** Harness and store work stay BLOCKED until ITEM 408 merges. Protocol
freeze may precede that merge; official scoring may not precede freeze plus the harness blind
review. Pre-freeze measurements (the ITEM 409 packs) are design evidence, never referee results.

## 10 · FREEZE RULES
Preconditions, in order: **F1** — the §11 compliance map verified line-by-line; **F2** — the owner
rules Dials 1–5; **F3** — one cold blind review of THIS protocol by a seat that is neither its
author nor the harness implementer (Dial-5 confirms); **F4** — the owner's freeze word, recorded in
the register. Status at v0.3: F2 CLOSED (peak door ruled open, owner word 2026-07-24); F1 verification and
F3 (the cold review) follow; F4 closes.
After freeze: the rules of the game — folds, targets, metrics, slices, fences, budgets, bars,
procedures — are immutable except by owner-worded amendment, version-bumped, effective only from
the NEXT round, with all official results re-scored under the amended version so every number in
the ledger is comparable under one protocol version. The no-bending rule: an amendment may never be
proposed in the same round as a result it would reverse, and every amendment states its motivation
in the ledger. The candidate SET evolves freely under the frozen rules — that is the design, not an
exception: declarations, admissions, joint re-tuning and backward passes are the frozen procedure
operating.

## 11 · v391/v392 COMPLIANCE MAP (freeze precondition F1)
**v391** — mechanism class as the unit of admission → §7.1 · re-tuned fresh on training folds,
out-of-fold, never the incumbent's frozen values → §§2.3, 6 (C0, C1R), 7.4 · shapes allowed to
generalize (constants → curves) → §7.1 · rejections recorded "not at any tested construction" with
the tested space listed → §7.6 · variants declared before scoring under a budget → §7.2.
**v392** — admission is not the end of tuning; admitted ingredients re-tune jointly at every
subsequent admission step → §§7.4, 7.7 · forward AND periodic backward/joint-refit passes → §7.7 ·
interaction bundles with stated mechanism stories, declared and tested as units under the same
discipline → §7.3 · the ceiling doubles as the interaction map, its gap sliced by lens guiding the
hunt → §§8.3, 7.3.
**Owner peak-horizon read (2026-07-24, this channel)** — the three-season headline stands, and the
peak, often four to six seasons out for young key-position players and rucks, must be measured and
protected → §4 M8 (metric) · §5.1 TALL-DEV (named slice) · §7.5 (guardrail + open admission door,
owner word 2026-07-24) · §8.3 (always-mapped row).

## 12 · DIAL RULINGS OF RECORD (2026-07-24, this channel)
- **Dial-1 · Headline metric — RULED: M4** (standing wMAE, Y+1..Y+3), owner word "3 seasons,"
  carrying the owner peak-horizon read encoded per the header (M8 · TALL-DEV · guardrail · map).
  The peak-door fork is RULED — the routing note below records it.
- **Dial-2 · Admission bar — RULED: CI90** plus the §7.5 guardrails. Owner word.
- **Dial-3 · Budgets — owner-DELEGATED; figures SEAT-SET:** 5 declared variants per class per
  round; 3 bundles per round. Provenance: the delegation is the owner's word; the figures are
  seat-authored under it and are never to be cited as owner-worded numbers. Rationale of record:
  the CI90-resolved bar and the declaration seal carry the anti-noise-mining load; the budget
  bounds compute and the forking-path count — 5/3 covers the seeded library each round without
  inviting dice-rolls, and either figure moves on one owner word without redesign.
- **Dial-4 · Backward-pass cadence — RULED by owner adoption of the seat recommendation:** after
  every admission.
- **Dial-5 · Blind review of the protocol before freeze — RULED: YES,** one cold seat. Owner word.

ROUTING NOTE — RESOLVED. The peak-door fork was put to the owner and RULED OPEN (owner word
"Open it," 2026-07-24, this channel): admission is also granted on bootstrap-resolved M8 gain with
no resolved regression on any other guardrail — encoded at §7.5. Seat note on scope, recorded for
the reviewer: the door reads M8 POOLED, the form the owner approved; if a mechanism's peak gain
concentrates in TALL-DEV without resolving pooled, the always-mapped row still surfaces it and a
variant may be redeclared next round — widening the door to TALL-DEV-resolved gain is available on
one owner word and is NOT in force.

*Design seat, ITEM 410 · returns to the owner; the pen files.*
