# ITEM 410 — ORIGIN-SAFE REFEREE PROTOCOL (AUD-004 ACTIVATION) · DRAFT v0.5 · design seat · 2026-07-24 · NOT FROZEN · ALL DIALS RULED · PEAK DOOR OPEN · F3 ANSWERED 17/17

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
F3 of v0.3 returned FAIL (docs/referee/F3_REVIEW_v0_3.md, register v396); every finding is
answered by number in ITEM_410_F3_RESPONSE_2026-07-24 and encoded here. Findings 3 and 10 were
resolved as OWNER DIALS 6 and 7 and are now RULED (owner words 2026-07-24, this channel):
Dial-6 = the VAULT (selection/confirmation split); Dial-7 = SMOOTH C0, subject to the §6
baseline certification the owner directed. The owner also gave an INTERPRETIVE READ OF RECORD
on Law 3 (L-SMOOTH), recorded at §12 and encoded at §7.10 and §6. The same F3 seat verifies
this v0.5 before F1 re-runs.

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
2.2 **Cutoffs and windows.** Windows: W1 = {t+1}; W3 = {t+1..t+3}; W6 = {t+1..t+6}. Cutoff sets:
t ∈ {2009,…,2024} for W1; t ∈ {2009,…,2022} for W3; t ∈ {2009,…,2019} for W6 (M8/M6W — the owner
peak-horizon read). Targets use complete seasons only; 2026 is excluded while live. SELECTION vs
CONFIRMATION (Dial-6 — F3 finding 3; RULED "vault," owner word 2026-07-24):
selection cutoffs = {2009,…,2019} for every head, one uniform window; confirmation cutoffs =
everything later that each head reaches (W1 heads: 2020–2024; W3 heads: 2020–2022; W6 heads: none
in-panel — their confirmation arrives via scheduled extensions, §7.12). Confirmation folds are
untouched until §7.12. Scheduled extension: each completed season appends one cutoff under these
identical rules and bumps the panel version (§9.6) — a scheduled event, not an amendment.
2.3 **Fold rule (F3 finding 2).** For each outer t: train = all data ≤ t; adjudication = targets
> t. All parameter fitting, transform fitting (normalizations, percentile maps, position
groupings) and hyperparameter selection happen inside train. Capacity dials tune on inner
chronological cutoffs u whose labels are FULLY observable by t: for a head of horizon h, u is
eligible only if u ≤ t − h; each head uses its three most recent eligible u (fewer if fewer
exist; if none exist, that head's dials copy those tuned at the nearest outer fold with
eligibility, ties to the earlier fold — deterministic). Joint multi-head dials minimize the
unweighted mean of per-head inner losses, each normalized by the current core's inner loss on
that head so units are comparable. Plain coefficients fit on full train. No inner label ever
crosses t.
2.4 **Identity.** The panel builder is deterministic from the store; panel md5, fold-spec md5 and
PANEL VERSION pin at harness build and stamp every scorecard (gate REF-FOLD, HALT on mismatch).

## 3 · ORIGIN-SAFETY FENCES
3.1 **As-of law.** No feature, transform, or parameter may use information from seasons > t —
including indirect routes. Known-leak regression probes, each HALT-not-warn (Law 2 /
SILENCE-IS-RED):
- **REF-LEAK-1** — peak_est (and any successor) receives as-of-t career totals only, never
  full-history aggregates.
- **REF-LEAK-2** — position at t comes from ≤t data or is declared missing; a current-season-only
  field never enters a historical cell.
- **REF-LEAK-3** — no live-season progress constant (the SEASON_PROG=0.79 class) is applied at any
  historical year.
Mechanical enforcement beyond the known leaks (F3 finding 9):
- **REF-MANIFEST** — every feature and transform ships a provenance-manifest row: source columns,
  maximum season referenced as a function of t, and fit scope. A feature without a row HALTs.
  Every join and aggregate carries a season ≤ t assertion evaluated at panel build.
- **REF-CANARY** — the harness ships ≥3 canary features that deliberately violate as-of (a direct
  future statistic; a full-history aggregate; a future-season position join). The probe suite must
  HALT on every canary, re-run at every harness change; a canary that passes is a red build.
3.2 **Incumbent — contaminated descriptive comparator (F3 finding 8).** C1 races AS-IS with its
full 18-input leakage inventory attached (parameters full-history-fitted; per the memo). Its
scores are reported, labelled CONTAMINATED, and adjudicate nothing — no admission, no guardrail,
no stopping input. Directional commentary ("flattered and still lost") is permitted only where
the leak's advantage direction has been separately established for the exact statistic in view,
as the memo did at Y+1. No blanket a fortiori rule. No other contestant may carry leakage.
3.3 **Ceiling included.** The ceiling (§8) obeys every fence in this section — a leaky ceiling
sizes a fictional prize.

## 4 · TARGETS AND METRICS (predeclared; exact and uniquely implementable — F3 findings 5, 6, 7)
**Eligibility.** For any production metric on window W at cutoff t: eligible cells = cells with ≥1
realized game in W. Zero-game cells are scored by the survival heads (M6, M6W), never by
production metrics. Every contestant must emit every head for every cell; a missing prediction
sets that contestant UNMEASURED on that metric at that cutoff (Law 2), and an UNMEASURED binding
metric blocks admission outright (§7.5).
**Realized values.** r_i(W) = games-weighted mean score over W; g_i(W) = realized games in W.
Realized standing = mid-rank percentile among eligible cells at (t, W):
pct(x_i) = (rank_avg(x_i) − 0.5) / N_{t,W} × 100, higher production = higher percentile.
**Predicted values.** p_i(W) = the contestant's expected games-weighted mean over W conditional on
≥1 game in W, from its emitted distribution. Predicted standing = the same mid-rank percentile
transform applied to p_i within the same eligible population — ranks score against ranks, so a
common monotone level bias cancels by construction.
**Aggregation.** Per cutoff: weighted MAE = Σ w_i·|pct(p_i) − pct(r_i)| / Σ w_i, w_i = g_i(W).
Across cutoffs: the unweighted mean of per-cutoff values over that metric's eligible cutoff set —
one cutoff, one vote.
- **M1** · Level wMAE, W1 — |p_i − r_i|, games-weighted, eligible cells, aggregated as above.
- **M2** · Standing wMAE, W1.
- **M3** · Level wMAE, W3.
- **M4** · Standing wMAE, W3 — **HEADLINE (Dial-1 — RULED, owner word 2026-07-24)**.
- **M5** · Career-remaining (secondary; never a door or guardrail). Career complete := last
  realized game season ≤ last complete panel season − 2; a later comeback reclassifies at the
  next panel version and is counted. Eligible cutoffs: ≥90% of then-eligible cells complete.
  Score = MAE on remaining career total points, level and standing forms; incomplete cells at
  eligible cutoffs are excluded and counted — no censoring estimator, a declared minimalism.
- **M6** · Attrition log-loss, W1 — per-cell log-loss on P(zero games in W1), all cells, p
  clipped to [1e-4, 1−1e-4]; reliability curve on fixed decile edges 0.1–0.9.
- **M6W** · Window survival, W6 — log-loss on P(≥1 game in W6), same clipping, cells at
  W6-eligible cutoffs. BINDING GUARDRAIL: the survival horizon of the peak door carries a binding
  score (F3 finding 6).
- **M7** · Calibration curves (diagnostic, non-binding) — predicted vs realized percentile by
  lens band; the F1/F2/F5 instrument.
- **M8** · Peak window, W6 (owner peak-horizon read, 2026-07-24). Realized peak = max over
  seasons s ∈ W6 of the realized seasonal mean; cell weight = games in that arg-max season, so
  flukey short-season peaks weigh little without any hard floor (weight-don't-gate). Predicted
  peak = max over s ∈ W6 of the contestant's E[seasonal mean_s | plays s] — conditional means
  only; joint-dependence modelling is deliberately not demanded of contestants, a declared limit
  (F3 finding 6): an M8 admission establishes ordering of conditional peaks among realized
  survivors, nothing more. BINDING FORM = STANDING ONLY (mid-rank percentiles on peaks); the
  level form is diagnostic. Eligibility ≥1 game in W6; censoring counted; survival itself binds
  through M6W beside the door.
**Uncertainty — frozen resampling algorithm (F3 finding 7).** Paired player-clustered bootstrap:
resample players with replacement; a drawn player contributes all its cells at all cutoffs;
within each resample recompute eligibility, percentiles, weights and per-cutoff metrics (a
cutoff empty in a resample drops from that resample's cutoff-mean) for BOTH sides of a
comparison on the identical resample; the paired gain distribution is the statistic. Fitted
models are NOT refit inside resamples — uncertainty is over the evaluation population given the
fitted candidates, a declared limit. B = max(2,000, ⌈50/α⌉) for the admission level α in force
(§7.5); percentile CI; seed schedule = 20260724 + 10,000·round + registry-index. "Resolved at
level α" := the (α·100)th percentile of the paired gain distribution exceeds zero; "resolved at
CI90" := resolved at α = 0.05. Slice CIs: a resample where the slice is empty contributes NA; a
slice needs ≥90% non-NA resamples, else UNMEASURED. Cutoff-robustness gate, mechanical: any
admission additionally requires a positive point-estimate gain in ≥⅔ of the head's eligible
selection cutoffs — season-shock insurance the player bootstrap cannot see. Coverage evidence:
before round 1 the harness files a null-candidate calibration — ≥20 sealed null perturbations of
C0 through the identical pipeline; the observed false-resolution rate at the round-1 α must not
exceed nominal (REF-NULLCAL, HALT), repeated after any harness change.
Every reported number carries its margin; the three narrowest margins lead every scorecard
(rulebook Part 3). Anything unmeasurable is reported UNMEASURED — never assumed passing, never
silently waived. Appendix A gives a five-cell worked standing fixture with the exact expected
value; the harness must reproduce it bit-exactly (REF-FIXTURE, HALT).

## 5 · LENS SLICES AND DECLARED DIAGNOSTICS
5.1 **Slices** — reporting bins only; estimator structure stays smooth (Law 3 / L-SMOOTH as
applied to estimators, per the memo's Addendum-2 constraint): age {≤22, 23–26, 27–29, 30+};
position groups as-of t (confound caveat stands — position enters as a candidate INGREDIENT only
via an age-controlled race); draft pick bands {1–5, 6–20, 21–40, 41+, ND/SSP/other pathway};
career-year {1–2, 3–5, 6–9, 10+}; evidence volume (career games at t: {≤10, 11–40, 41–100,
100+}) — the thin-evidence lens the Mraz class demands.
NAMED SLICE OF RECORD — **TALL-DEV**: age ≤22 × position group {key forward, key back, ruck}
as-of t (owner peak-horizon read: the cohort whose peak sits beyond the headline window).
Frozen slice mechanics (F3 finding 13): the GROUPS are frozen here; the raw→group mapping table
is produced by one read-only enumeration of the store's distinct position values at harness
build and SEALED in the claims note BEFORE any score access; an unmapped raw value at panel
build HALTs (REF-VOCAB). Hybrids: a cell joins TALL-DEV if ANY listed position at t maps to
key-forward, key-back or ruck. Missing position at t: excluded from TALL-DEV and counted in a
reported MISSING-POS row. Support and pooling, universal: any slice or slice-pair with pooled
selection-fold support < SUPPORT_MIN = 200 eligible cells (§12 constants ledger) is
UNMEASURED-THIN and pools into its declared parent (slice-pairs → their age-band member;
position slices → all-positions; the pooling is stated on the scorecard) — thin slices pooled
deliberately and declared, per rulebook Part 3. TALL-DEV guardrail fallback: where TALL-DEV is
UNMEASURED-THIN for a needed statistic, the guardrail evaluates on its parent (age ≤22 pooled)
and the scorecard flags the fallback — the owner-protected row can never silently vanish or
silently pass. Every §4 metric reports per slice, for every contestant, identically.
5.2 **Declared diagnostics** (non-binding, always reported; exact forms — F3 finding 16):
- **D1** · Cross-band vs within-band decomposition of standing error. Within-band: wMAE of
  mid-rank percentiles computed INSIDE each age band (predicted vs realized). Cross-band: wMAE
  of band-mean standing error. This inline definition governs. The allocation-not-ordering
  finding stays visible round to round.
- **D2** · Unconditional expected-production check: MAE on expected total window points —
  Σ_s P(plays s)·E[games_s | plays s]·E[mean_s | plays s] vs realized total points, unweighted —
  the level/attrition interaction conditional metrics hide.
- **D3** · Signal-reuse audit (the AUD-007 instrument), frozen as ABLATION-based: for each
  admitted pair (i, j) sharing a declared registry input, contribution(i | core) vs
  contribution(i | core − j) on the headline, per lens. Double-encoding shows here.

## 6 · CONTESTANTS
- **C0 · BENCHMARK (Dial-7 — RULED, owner words 2026-07-24: smooth it, and test that the
  smoothing actually helps).** Two ingredients: one recency λ and an age-drift term as a SMOOTH
  low-df age curve — ≤4 effective degrees of freedom, free non-zero asymptote (REF-FADE-FLOOR),
  fit per fold. C0-smooth seeds the governed core. BASELINE CERTIFICATION (owner-directed): at
  round 0, before any candidate scoring, C0-smooth races C0-banded — the literal pack-2
  four-entry step table, present under the owner's Law-3 interpretive read as a declared,
  measured exception; certification comparator only, never seed, never adoptable — paired, full
  §4 suite, selection folds only, sealed and logged. The owner's stated expectation is on
  record: the curve should outperform the brackets. If C0-banded resolvedly beats C0-smooth on
  the headline at CI90, the race pauses and the owner is notified before proceeding — the seed
  choice returns to him; otherwise C0-smooth stands, and the certification files in the ledger
  either way. Constants re-fit per fold on train only — v391 applies to the benchmark too.
- **C1 · INCUMBENT, frozen.** Contaminated descriptive comparator per §3.2 — reported, labelled,
  adjudicating nothing.
- **C1R · INCUMBENT RE-TUNED ("recalibrate").** The incumbent's mechanism set with parameters
  re-fit fresh per fold under §3 fences, per v391. The recalibrate arm of the
  recalibrate-vs-rebuild fork, raced in its own lane — the owner's "middle," measured.
- **C2 · GOVERNED CORE ("rebuild").** Grown from C0 by §7. Output contract: per-player
  distribution over future seasons (games, average) including the zero-games branch.
- **C3 · CEILING.** §8. Never adoptable — structurally: no ceiling output may enter any adoption
  artifact (gate REF-CEIL, HALT).
Every contestant emits a prediction for every target head; a head a contestant cannot emit
scores UNMEASURED on that metric and is reported as such (Law 2); an UNMEASURED binding metric
blocks admission (§7.5). C0 carries a declared base-rate survival head (per-age rates fit on
train) so the benchmark scores all heads.
The recalibrate-vs-rebuild fork goes to the owner formally when C1R and C2 both hold referee
results (charter §5), carried by the §7.12 fork report.

## 7 · MECHANISMS, VARIANTS, BUNDLES, SELECTION (the v391/v392 machinery)
7.1 **Registry.** The unit of admission is the MECHANISM CLASS. Every class registers before any
scoring: ID; one-paragraph mechanism story; parameter space with shapes allowed to generalize
(constants → smooth curves — Law 3 on estimators); tuning procedure (train-only); lens
hypotheses — where it should help. Class identity = the registered parameter-space signature
(F3 finding 4): a proposed class whose declared space overlaps an existing class's must register
as variants of the existing class; every registration carries a one-line distinctness note
against each prior class; a registration without them HALTs (REF-FRAG). Seed library from the
charter: λ(age) arc; age drifts; cohort blend w(age); career-year-indexed pedigree;
attrition/survival; young-decliner rebound; position (age-controlled race only); availability.
7.2 **Declaration seal, budgets, caps.** A round's variant set and bundle set are declared to
the referee ledger and SHA-sealed BEFORE any adjudication-fold scoring in that round (gate
REF-SEAL: no official score without a seal predating the run; every adjudication-outcome access
is logged; unlogged access is a red; HALT). Budgets (Dial-3 — seat-set under owner delegation,
§12): ≤5 declared variants per class per round; ≤3 bundles per round. Caps (F3 finding 4): the
race runs at most R_MAX = 6 rounds (owner-extendable by word); a class races in at most 3
rounds lifetime — its debut plus ≤2 re-entries, each re-entry with fresh declared variants and
a stated reason (map row or new evidence). Post-hoc variants after seeing results are barred.
7.3 **Bundles.** An interaction bundle = two or more classes with a stated joint mechanism
story, tested and admitted or rejected as a unit, under the same seal and budget discipline.
From round 2 onward, every bundle declaration must cite an interaction-map row (§8.3) or new
external evidence. A bundle containing an already-admitted class re-declares as its incremental
complement, story intact.
7.4 **Forward step.** Each sealed candidate is evaluated by FULL JOINT RE-FIT: the round-start
core's parameters and the candidate's re-tuned together on train folds — nothing holds its
entry settings (v392) — and adjudication-fold scores computed. SCREENING RULE (Dial-6 — F3
finding 3; RULED "vault," owner word 2026-07-24): screening of any kind touches
INNER folds only (§2.3); no seat, script, or construction step may read selection-fold outcomes
except sealed official scoring runs and the §8.3 map computation; confirmation folds are
untouchable until §7.12. Any admission-deciding run must be a full joint refit (gate REF-JOINT,
HALT).
7.5 **Admission bar (Dial-2 — RULED: CI90 base, owner word 2026-07-24 · peak door — RULED OPEN,
owner word 2026-07-24 · family control per F3 finding 4).** Admission = resolved gain at level
α_r on the headline M4 **or** on M8 (standing form, pooled) — the peak door — where α_r =
0.05 / m_r one-sided and m_r = the round's enumerated family (§7.9); a Bonferroni tightening of
the owner's CI90 base, never a loosening. AND, either door: no resolved-at-CI90 regression on
M2, on M6, on M6W, or on the non-door member of {M4, M8}, pooled or within any declared slice
(TALL-DEV per the §5.1 fallback); AND the §4 cutoff-robustness gate; AND every §7.10 structural
gate green with measured margins; AND every binding metric measured — UNMEASURED blocks.
Guardrail multiplicity is deliberately uncorrected: guardrails only veto, so more uncorrected
chances to veto make admission strictly harder — conservative by direction.
7.6 **Rejection record.** "REJECTED — not at any tested construction," with the tested space
listed in full (v391), so revisits are cheap and bounded: re-entry per the §7.2 lifetime cap,
with a newly declared variant set and a stated reason.
7.7 **Backward pass (Dial-4 — RULED by owner adoption of the recommendation: after every
admission).** After every admission: each admitted unit is removed in turn with the remainder
jointly re-fit; a unit whose removal yields resolved gain (at CI90) is dropped and recorded.
The removal unit is the registered admission unit — a bundle admitted as a unit removes as a
unit. Scheduled removal tests count in the round's family m_r. Joint refit is inherent to every
step, so the core never fossilizes at entry settings.
7.8 **Stopping rule (F3 findings 14, 11).** Row identity = (metric, slice tuple, panel
version); the test evaluates on the CURRENT map against the CURRENT core. The race stops when a
round closes with zero admissions AND every currently-resolved row carries a bundle tested
against the current or immediately-preceding core version — older tests lapse — with the
diffuse-gap clause: if the pooled C3−C2 gap stays resolved while no row resolves, stopping is
permitted but the fork report must state the undischarged pooled gap explicitly. Weak-ceiling
case per §8.2. Or the owner's word, any time. Then §7.12 runs and the fork report goes to the
owner. Captured share is reported throughout: (C0→C2 gain) / (C0→C3 gap), pooled and per lens.
7.9 **Multiplicity honesty (F3 finding 4).** The complete per-round experiment family is
enumerated in the ledger BEFORE scoring: m_r = sealed forward candidates + scheduled backward
removals. Every adjudication-outcome access is logged. The cumulative regime = per-round
Bonferroni (§7.5) × the lifetime re-entry cap × the round cap × the §7.12 confirmation gate;
the screening ban removes screening from the family entirely.
7.10 **Structural gates, enumerated (F3 finding 15).** Each gate emits PASS/FAIL with a
measured value and margin; a missing emission is a RED (Law 2 / SILENCE-IS-RED):
- **REF-RECENCY** — per-game weight deltas over the years-back grid all ≤ 0; margin = max delta.
- **REF-WDG** — every evidence-count transform: max adjacent-count step ≤ 5% of the transform's
  fitted range; margin = largest step share. No hard evidence floors, ever.
- **REF-SMOOTH-EST** — every fitted 1-D shape over age, evidence, or ordinal position: max
  adjacent-grid step ≤ 5% of fitted range (Law 3 on estimators); margin = largest step share.
  Per the owner's Law-3 interpretive read (§12): an UNDECLARED step beyond the bound HALTs; a
  mechanism may instead REGISTER a declared discontinuity — story stated, step measured and
  reported as the margin — and race on its merits as a flagged exception. Smoothness is the
  firm default; declared, measured drops are lawful; silent ones never are. REF-WDG is NOT
  softened by this read — hard evidence floors stay permanently rejected.
- **REF-SYMMETRY** — Law 5: declared forms contain no direction-conditional branch on
  performance deltas; a registered asymmetric mechanism must be ONE shared fitted curve
  evaluated identically for every cell — machinery symmetric, shape free — with its fitted
  asymmetry reported with CI as the margin.
- **REF-FADE-FLOOR** — Law 6, direction-only analogue: age-curve families admit a free non-zero
  asymptote; margin = fitted asymptote CI.
- **REF-CEIL** — no C3 output in any adoption artifact.
- Plus the §3 probes (REF-LEAK-1/2/3, REF-MANIFEST, REF-CANARY), REF-FIXTURE, REF-NULLCAL,
  REF-SEAL, REF-JOINT, REF-FOLD, REF-VOCAB, REF-FRAG. The 5% step bounds are seat-set constants
  (§12 ledger).
7.11 **Determinism (F3 finding 12).** All sealed candidates in a round score against the
ROUND-START core. Class representative = the best passing variant by (headline point gain, then
the α-level percentile lower bound, then earliest registry index). Exactly ONE admission per
round — the passing candidate leading by the same key; every other passer flags
PASSED-NOT-ADMITTED and auto-reseals next round, consuming no new budget and counting in the
next round's family. The joint refit after admission produces the next round-start core; the
backward pass then runs. No tie ever resolves by seat discretion.
7.12 **Confirmation (Dial-6 — F3 finding 3; RULED "vault," owner word 2026-07-24).** At stop: the assembled C2 (and C1R) score ONCE on the confirmation folds (§2.2).
Reported in the fork report beside selection results: the confirmation-fold paired gain vs C0
on the headline at CI90; a one-shot batch per-ingredient ablation on confirmation folds at
level 0.10/K (K = admitted units). M8-door admissions carry the label
PROVISIONAL–AWAITING-EXTENSION until scheduled extensions make confirmation-era peak windows
measurable, then confirm the same way. After the fork report, confirmation folds retire into
selection for any owner-worded follow-on race (panel-version bump).

## 8 · THE CEILING AND THE INTERACTION MAP
8.1 **Spec, frozen with the protocol (F3 finding 11).** Learner: LightGBM gradient-boosted
trees; per-head objectives (L2 on production heads; log-loss on survival heads); features = the
frozen panel manifest (§3.1), all origin-safe, native missing-value handling; hyperparameter
grid, fixed: num_leaves ∈ {15, 31, 63} × learning_rate ∈ {0.03, 0.1} × min_child ∈ {20, 50},
selected per fold on §2.3 inner-eligible validation; early stopping 50 rounds on inner loss;
seed schedule = 20260724 + fold-index; library version pinned at harness build and recorded on
every scorecard. Deliberately unconstrained by estimator-shape laws — which is exactly why
REF-CEIL bars its outputs from adoption artifacts forever.
8.2 **The prize, and the weak-ceiling case.** Ceiling-vs-C0 and ceiling-vs-C2 paired gaps on
M2/M4 with CIs: the size of the prize and the denominator of captured share. If C3's pooled
gain over C0 is not resolved at CI90, captured share reports UNMEASURED, the resolved-row
machinery suspends, and stopping reduces to zero-admissions plus explicit owner notification —
a weak ceiling is itself a filed finding, not a free pass.
8.3 **The interaction map.** Computed on SELECTION folds only. Row universe, frozen: every §5.1
single slice plus every slice-pair with pooled selection-fold support ≥ SUPPORT_MIN = 200
eligible cells; below-support rows are UNMEASURED-THIN and pool to their declared parent
(§5.1). Each round: the C3−C2 paired gap on M4 — and on M8 where measurable — per row, ranked
with CIs, published in the ledger; TALL-DEV is always a mapped row. Rows whose CIs exclude zero
are RESOLVED ROWS — the hunting ground: bundle stories cite rows (§7.3). Row identity =
(metric, slice tuple, panel version). Feature-attribution views of C3 are permitted as
guidance, labelled report-only.
8.4 **Cache.** C3 out-of-fold predictions compute once per protocol version and per panel
version and are cached; the map recomputes against the evolving C2 each round.

## 9 · GOVERNANCE, IDENTITY, ENVIRONMENT
9.1 **Documents.** On filing: this protocol → `docs/referee/REFEREE_PROTOCOL.md`; an append-only
`docs/referee/REFEREE_LEDGER.md` (declaration seals, enumerated families, scorecards,
admissions and rejections with tested spaces, interaction maps, outcome-access logs,
amendments). One pen files both; the register carries pointers, not copies (SSI).
9.2 **Seats.** The design seat authors (this document); build seats implement the harness
post-408 under a written directive with identity pins; implementer ≠ reviewer: one cold blind
review of the harness against this protocol before the first official run (Law 11 /
SEAM-PATTERN). Referee runs are read-only with respect to store and engine; scorecards are
[re-runnable] artifacts.
9.3 **Identity.** Every scorecard stamps: protocol version, panel version, panel md5, fold-spec
md5, harness identity, contestant registry entry, declaration-seal SHA, family size m_r, seeds,
environment.
9.4 **Environment (F3 finding 17).** The adjudication environment pins per PROTOCOL VERSION:
container image digest and dependency lockfile recorded at the first official run and stamped
on every scorecard. Any environment change before the race ends forces a full re-score of all
official results in the new environment before further rounds; the re-scored ledger controls;
prior numbers archive. The board-determinism record stands: a cross-environment difference is a
re-measurement to reconcile, never a result.
9.5 **Blocks and pre-history.** Harness and store work stay BLOCKED until ITEM 408 merges.
Protocol freeze may precede that merge; official scoring may not precede freeze plus the
harness blind review. Pre-freeze measurements (the ITEM 409 packs) are design evidence, never
referee results.
9.6 **Panel versioning (F3 finding 17).** A scheduled extension bumps the PANEL VERSION.
Before any post-extension round: C0, C3, the current C2 and C1R re-run on the new version.
Admissions stand as history under their panel version; all forward comparisons and the fork
report cite current-version numbers only; M8/M6W confirmation additions land per §7.12.

## 10 · FREEZE RULES
Preconditions, in order: **F1** — the §11 compliance map verified line-by-line; **F2** — the owner
rules Dials 1–5; **F3** — one cold blind review of THIS protocol by a seat that is neither its
author nor the harness implementer (Dial-5 confirms); **F4** — the owner's freeze word, recorded in
the register. Status at v0.5: F2 FULLY CLOSED — all seven dials ruled, the Law-3 interpretive read
recorded; F3's findings are answered and encoded — the same F3 seat verifies v0.5; then F1
re-verification; F4 closes.
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
subsequent admission step → §§7.4, 7.7 · forward AND periodic backward/joint-refit passes → §§7.4, 7.7 ·
interaction bundles with stated mechanism stories, declared and tested as units under the same
discipline → §7.3 · the ceiling doubles as the interaction map, its gap sliced by lens guiding the
hunt → §§8.3, 7.3.
**Owner peak-horizon read (2026-07-24, this channel)** — the three-season headline stands, and the
peak, often four to six seasons out for young key-position players and rucks, must be measured and
protected → §4 M8 (metric) · §5.1 TALL-DEV (named slice) · §7.5 (guardrail + open admission door,
owner word 2026-07-24) · §8.3 (always-mapped row).
**Owner Law-3 interpretive read (2026-07-24, this channel)** — smoothness is a firm guide, not
an absolute demand; occasional drops are lawful when declared and measured → §7.10
(REF-SMOOTH-EST exception path) · §6 (C0 baseline certification comparator).

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

- **Dial-6 · Adaptive-reuse regime — RULED: THE VAULT** (owner word "Vault," 2026-07-24):
  inner-fold-only screening; selection 2009–2019; confirmation 2020-on untouched until the
  §7.12 single read; M8/M6W confirm on scheduled extensions, peak-door admissions provisional
  till then. Encoded §§2.2, 7.4, 7.12.
- **Dial-7 · C0 vs L-SMOOTH — RULED: SMOOTH, WITH CERTIFICATION** (owner words 2026-07-24):
  the seed is the smooth ≤4-df age curve, AND the smoothing itself is tested — C0-smooth vs
  C0-banded at round 0 per §6, with the owner notified before the race proceeds if the brackets
  resolvedly win the headline. Owner's stated expectation on record: the curve should win.
- **OWNER INTERPRETIVE READ OF RECORD — Law 3 / L-SMOOTH** (owner words, 2026-07-24, this
  channel; paraphrase): smoothness is a firm guide, not an absolute demand — there will
  occasionally be times a drop has to happen. An interpretation of application, not a rulebook
  text change (Law 10 untouched). Encoded: §7.10 declared-exception path; §6 certification
  comparator. The pen is asked to seal this read in the register.

SEAT-SET CONSTANTS LEDGER (the Dial-3 delegation pattern; each figure moves on one owner word,
none may be cited as owner-worded): SUPPORT_MIN = 200 eligible cells; smoothness/WDG step bound
= 5% of fitted range; R_MAX = 6 rounds; class lifetime = 3 raced rounds; selection/confirmation
boundary = 2019/2020; canaries ≥ 3; null-candidates ≥ 20; probability clip = 1e-4; B = max(2000,
⌈50/α⌉); bootstrap seed base = 20260724.

## APPENDIX A · WORKED STANDING FIXTURE (REF-FIXTURE; harness must reproduce bit-exactly)
One cutoff, W1, five eligible cells. Realized means r = (90, 80, 70, 60, 50); realized games
g = (20, 10, 20, 5, 20); predictions p = (85, 82, 60, 65, 40). Mid-rank percentiles, higher =
better: realized → (90, 70, 50, 30, 10); predicted → (90, 70, 30, 50, 10). Per-cell |Δpct| =
(0, 0, 20, 20, 0); weights = g. Weighted MAE = (20·0 + 10·0 + 20·20 + 5·20 + 20·0) / 75 =
500 / 75 = **6.6667** (4 dp). Any harness not reproducing 6.6667 on this fixture HALTs.

*Design seat, ITEM 410 · returns to the owner; the pen files.*
