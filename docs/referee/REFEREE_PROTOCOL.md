# ITEM 410 — ORIGIN-SAFE REFEREE PROTOCOL (AUD-004 ACTIVATION) · DRAFT v0.8 · design seat · 2026-07-24 · NOT FROZEN · DIALS 1–9 RULED · TWIN FILED · PROSPECTIVE-DISPOSITIVE ARCHITECTURE

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
on Law 3 (L-SMOOTH), recorded at §12 and encoded at §7.10 and §6. F3 verification of v0.5 (docs/referee/F3_VERIFICATION_v0_5.md, register v398): F1 PASS, F3
FAIL. v0.6 closes the reviewer-specified spec-completion set and encodes DIAL-8 (RULED at
register v399, owner word): SELECTION IS EXPLORATORY, CONFIRMATION IS DISPOSITIVE — failed
confirmation strips the unit; provisional M8 units are barred from adoption artifacts until
confirmed. The acceptance-twin L-SMOOTH amendment is FILED (register v400; Law 10 act; F2b CLOSED) —
the exception path and banded comparator are operative. DIAL-9 (RULED at register v402, owner
word): PROSPECTIVE-DISPOSITIVE — the §7.12 vault read claims only the confirmation-era
population with declared limits; the BINDING gate is the §7.13 PROSPECTIVE GATE: every
scheduled panel extension scores the frozen confirmed core vs C0 under predeclared
door-matched rules, failing units strip, adoption is staged and reversible. v0.8 encodes
Dial-9, closes F3v2 findings 6, 10a, 11 and 15 as the reviewer specifies, and conforms the
stale twin language. The same F3 seat verifies v0.8.

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
exist; if NONE exist, that head's capacity dials take their PREDECLARED DEFAULTS — every
registered capacity dial must declare a finite grid, and its default is the grid's median
element, lower median on even grids — and the fold is flagged DEFAULT-TUNED on the scorecard;
no fold ever imports tuning from any other outer fold, earlier or later (F3 verification,
finding 2)). Joint multi-head dials minimize the
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

## 4 · TARGETS AND METRICS (predeclared; exact and uniquely implementable)
**Emission contract (frozen).** Every contestant emits, per cell, per season s ∈ {t+1,…,t+6},
the triple (P_s, G_s, μ_s): P_s = P(plays ≥1 game in s); G_s = E[games in s | plays s]; μ_s =
E[seasonal mean score | plays s]. Every binding quantity below derives from the triples under
ONE frozen convention — independence across seasons — identical for all contestants; joint
dependence is deliberately not demanded (declared limit).
**Eligibility.** For any production metric on window W at cutoff t: eligible cells = cells with
≥1 realized game in W. Zero-game cells are scored by the survival heads, never by production
metrics. Every contestant must emit every triple for every cell; a missing emission sets that
contestant UNMEASURED on the affected metrics at that cutoff (Law 2), and an UNMEASURED binding
metric blocks admission outright (§7.5).
**Realized values.** r_i(W) = games-weighted mean score over W; g_i(W) = realized games in W.
Realized standing = mid-rank percentile among eligible cells at (t, W):
pct(x_i) = (rank_avg(x_i) − 0.5) / N_{t,W} × 100, higher = better.
**Predicted production, frozen functional (F3 verification, finding 5).** For window W:
p_i(W) = Σ_{s∈W} P_s·G_s·μ_s / Σ_{s∈W} P_s·G_s — expected points over expected games. If the
denominator is 0, p_i := 0 and the cell ranks bottom. Predicted standing = the same mid-rank
percentile transform applied to p_i within the same eligible population. Appendix B.1 is a
multi-season fixture on which the rejected alternative readings (unweighted mean of conditional
means; P-weighted mean of means) give provably different values.
**Aggregation.** Per cutoff: weighted MAE = Σ w_i·|pct(p_i) − pct(r_i)| / Σ w_i, w_i = g_i(W).
Across cutoffs: the unweighted mean of per-cutoff values over that metric's eligible cutoff
set — one cutoff, one vote.
- **M1** · Level wMAE, W1 — |p_i − r_i|, games-weighted, eligible cells.
- **M2** · Standing wMAE, W1.
- **M3** · Level wMAE, W3.
- **M4** · Standing wMAE, W3 — **HEADLINE (Dial-1 — RULED, owner word 2026-07-24)**.
- **M5** · Career-remaining, SIX-SEASON TRUNCATION (secondary; never a door or guardrail; the
  truncation is a declared limit). Career complete := last realized game season ≤ last complete
  panel season − 2; comebacks reclassify at the next panel version and are counted. Eligible
  cutoffs: ≥90% of then-eligible cells complete. Realized T_i = Σ_{s=t+1}^{t+6} games_s·mean_s;
  predicted T̂_i = Σ_{s=t+1}^{t+6} P_s·G_s·μ_s. Level = unweighted MAE on totals; standing =
  unweighted MAE on mid-rank percentiles of T̂ vs T among M5-eligible cells; both aggregate as
  the unweighted cutoff mean. Incomplete cells at eligible cutoffs are excluded and counted.
- **M6** · Attrition log-loss, W1 — per-cell log-loss on P(zero games in W1) = 1 − P_{t+1},
  clipped to [1e-4, 1−1e-4]; reliability curve on fixed decile edges 0.1–0.9.
- **M6W** · Window survival, W6 — log-loss on P(≥1 game in W6) = 1 − Π_{s∈W6}(1 − P_s), same
  clipping, cells at W6-eligible cutoffs. BINDING GUARDRAIL.
- **M7** · Calibration curves (diagnostic, non-binding) — predicted vs realized percentile by
  lens band; the F1/F2/F5 instrument.
- **M8** · Peak window, W6 (owner peak-horizon read, 2026-07-24). Realized peak = max over
  seasons s ∈ W6 of the realized seasonal mean; cell weight = games in that arg-max season
  (weight-don't-gate). Predicted peak, REACH-WEIGHTED (F3 verification, finding 6): sort the
  window's seasons by μ descending as μ_(1) ≥ … ≥ μ_(6) with play probabilities P_(j); then
  predicted peak = Σ_j μ_(j) · P_(j) · Π_{i<j}(1 − P_(i)) / (1 − Π_{s∈W6}(1 − P_s))  — the expected
  maximum of the emitted conditional means under the frozen independence convention (F3v2,
  finding 6 note). A season the contestant says
  is barely reachable contributes almost nothing regardless of its conditional mean: the remote-
  peak route is closed mechanically, and M6W binds window survival beside the door. If all
  P_s = 0, predicted peak := 0 and the cell ranks bottom. BINDING FORM = STANDING ONLY; the
  level form is diagnostic. Eligibility ≥1 game in W6; censoring counted. Appendix B.2 is the
  discriminating fixture (reach-weighted 99.51 vs naive max-of-means 150).
**Uncertainty — frozen resampling with DECLARED LIMITS (F3 verification, finding 7).** Primary:
paired player-clustered bootstrap exactly as follows — resample players with replacement; a
drawn player contributes all its cells at all cutoffs; within each resample recompute
eligibility, percentiles, weights and per-cutoff metrics (an empty cutoff drops from that
resample's cutoff-mean) for BOTH comparison sides on the identical resample; the paired gain
distribution is the statistic; percentile CI; B = max(2,000, ⌈50/α⌉); seed schedule = 20260724
+ 10,000·round + registry-index; fitted models are not refit inside resamples. "Resolved at
level α" := the (α·100)th percentile of the paired gain distribution exceeds zero; "resolved at
CI90" := resolved at α = 0.05. Slice CIs need ≥90% non-NA resamples, else UNMEASURED.
**DECLARED LIMIT L-U1, printed on every scorecard:** the primary interval quantifies
player-sampling uncertainty ONLY; season/cutoff common shocks are NOT captured — with eleven
selection cutoffs and overlapping W3/W6 windows, the effective independent season sample is a
handful of blocks, below what any resampling scheme can calibrate, and this protocol does not
pretend otherwise. Companion evidence, always reported beside the primary CI: (i) a
leave-one-cutoff-out jackknife over per-cutoff paired gains — eleven leave-outs, descriptive,
never gating; (ii) the cutoff-robustness screen — positive point-estimate gain in ≥⅔ of the
head's eligible selection cutoffs, mechanical, labelled a sign-consistency screen and not
coverage. Null calibration, numeric criterion (finding 7): before round 1 the harness runs
N = 200 sealed null perturbations of C0 through the identical pipeline; PASS iff observed
resolutions ≤ c where c = min{c : BinomCDF(c; N, α) ≥ 0.95} at the round-1 α (c = 15 at
α = 0.05); margin = c − observed (REF-NULLCAL, HALT), repeated after any harness change. Under
Dial-8 every selection-era statistic is EXPLORATORY, and under Dial-9 the §7.12 vault read
claims only the fixed confirmation-era population — the BINDING gate is the §7.13 PROSPECTIVE
GATE, whose sampling unit is future seasons as they complete: the honest answer to temporal
dependence that neither eleven selection cutoffs nor three vault cutoffs can certify (F3v2,
finding 7).
Every reported number carries its margin; the three narrowest margins lead every scorecard
(rulebook Part 3). Anything unmeasurable is reported UNMEASURED — never assumed passing, never
silently waived. Appendix A (W1 standing, 6.6667) and Appendix B (W3 functional 92.0;
reach-weighted peak 99.51; D3 identity test) must reproduce bit-exactly (REF-FIXTURE, HALT).

## 5 · LENS SLICES AND DECLARED DIAGNOSTICS
5.1 **Slices** — reporting bins only; estimator structure stays smooth (Law 3 / L-SMOOTH as
applied to estimators, per the memo's Addendum-2 constraint): age {≤22, 23–26, 27–29, 30+};
position groups (below); draft pick bands {1–5, 6–20, 21–40, 41+, ND/SSP/other pathway};
career-year {1–2, 3–5, 6–9, 10+}; evidence volume (career games at t: {≤10, 11–40, 41–100,
100+}) — the thin-evidence lens the Mraz class demands.
**Position, deterministic and frozen (F3 verification, finding 13).** The store's position
vocabulary was enumerated read-only at main `ef3670f` and is frozen HERE, not at harness build:
MID → MIDFIELD · GDEF → GEN-DEF · DEF → GEN-DEF · KDEF → KEY-DEF · KFWD → KEY-FWD ·
GFWD → GEN-FWD · RUC → RUCK. Any raw value outside these seven HALTs (REF-VOCAB); extending the
table is an owner-worded amendment. Position at cutoff t = the DRAFTED position
(`drafted_position`) — time-stamped at entry, hence origin-safe at every t ≥ draft year by
construction, and aligned with the Lens Projection doctrine (cohort lenses read off drafted
position); `present_position`, `future_position` and `alternate_position` are current-era
fields and are BANNED from historical cells (REF-LEAK-2). Cells with no drafted position are
excluded from position slices and counted in a reported MISSING-POS row.
NAMED SLICE OF RECORD — **TALL-DEV**: age ≤22 × drafted position ∈ {KEY-FWD, KEY-DEF, RUCK}
(owner peak-horizon read: the cohort whose peak sits beyond the headline window).
**Support and pooling, universal:** any slice or slice-pair with pooled selection-fold support
< SUPPORT_MIN = 200 eligible cells (§12 ledger) is UNMEASURED-THIN and pools into its declared
parent (slice-pairs → their age-band member; position slices → all-positions; the pooling is
stated on the scorecard) — thin slices pooled deliberately and declared, per rulebook Part 3.
**TALL-DEV unmeasured disposition (F3 verification, finding 13 — replaces the struck parent
fallback):** if TALL-DEV is UNMEASURED for any statistic an admission decision requires, that
admission is BLOCKED — no substitute population, no silent waiver (Law 2; the protocol's own
UNMEASURED-blocks rule applies to the owner-protected row above all). The owner may waive a
specific round by explicit word, sealed in the ledger — the register's named-waiver pattern —
and the waiver is reported on every affected scorecard. Every §4 metric reports per slice, for
every contestant, identically.
5.2 **Declared diagnostics** (non-binding, always reported; exact forms):
- **D1** · Cross-band vs within-band decomposition of standing error. Within-band: wMAE of
  mid-rank percentiles computed INSIDE each age band (predicted vs realized). Cross-band: wMAE
  of band-mean standing error. This inline definition governs.
- **D2** · Unconditional expected-production check: MAE on expected total window points —
  Σ_s P_s·G_s·μ_s vs realized total points, unweighted.
- **D3** · Signal-reuse audit (the AUD-007 instrument), exact (F3 verification, finding 16).
  contribution(i | S) := M4_sel(core(S∖{i})) − M4_sel(core(S)), where core(X) = the ingredient
  set X JOINTLY REFIT on train folds (§7.7 machinery) and M4_sel = the headline computed on
  selection folds; positive = i helps; paired player-bootstrap CI90 reported, descriptive. For
  an admitted pair (i, j) sharing a declared registry input, the reuse statistic is
  Δ_ij := contribution(i | S) − contribution(i | S∖{j}), reported with both CIs, per lens, no
  cross-lens aggregation. Identity fixture (Appendix B.3): with ingredient B constructed as an
  exact duplicate of A, the harness must return contribution(A | S) = 0 exactly.

## 6 · CONTESTANTS
- **C0 · BENCHMARK (Dial-7 — RULED, owner words 2026-07-24: smooth it, and test that the
  smoothing actually helps).** Two ingredients, FROZEN TO THE DESIGN MATRIX (F3v2, finding 10a).
  LEVEL: L_i(t) = Σ_{s≤t} e^(−λ(t−s))·g_s·m_s / Σ_{s≤t} e^(−λ(t−s))·g_s (g, m = season games
  and mean); λ on the frozen grid {0.05, 0.10, …, 0.60}. DRIFT: drift(a) = c₁ + c₂·a′ +
  c₃·X₁(a′) + c₄·X₂(a′), a′ = clamp(a, 18, 33) — constant extrapolation by input clamping; the
  value at a′ = 33 is the asymptote REF-FADE reads — with the unnormalized restricted-cubic-
  spline basis on knots k = (20, 24, 28, 32), coefficient order exactly as written:
  X_j(a′) = (a′−k_j)₊³ − (a′−k₃)₊³·(k₄−k_j)/(k₄−k₃) + (a′−k₄)₊³·(k₃−k_j)/(k₄−k₃), j ∈ {1, 2}.
  Exactly four coefficients. FIT, deterministic per fold: the model predicts mean_{t+1} =
  L_i(t) + drift(age at t+1); for each grid λ, L is computed and (c₁..c₄) solve closed-form
  weighted least squares of (mean_{t+1} − L_i(t)) on the basis, weight = games_{t+1}, over
  train transition cells; the reported (λ, c₁..c₄) is the grid minimizer of the weighted
  objective, ties to the smaller λ. The response and the joint λ–drift relationship are thereby
  fixed; Appendix B.4 pins the basis numerically. Two conforming implementers cannot diverge. C0-smooth seeds the governed core. BASELINE CERTIFICATION (owner-directed): at
  round 0, before any candidate scoring, C0-smooth races C0-banded — the four-entry step table on the
  frozen bands {≤22, 23–26, 27–29, 30+}, values refit per fold; present under the owner's Law-3
  interpretive read as a declared, measured exception, operative — the worded twin
  amendment is FILED (register v400; F2b CLOSED); certification comparator only, never seed,
  never adoptable — paired, full
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
- **C2 · GOVERNED CORE ("rebuild").** Grown from C0 by §7. Output contract: the §4
  emission triples (P_s, G_s, μ_s) for every season to t+6.
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
7.5 **Admission bar (Dial-2 — RULED: CI90 base · peak door — RULED OPEN · Dial-8 — RULED:
selection admissions are EXPLORATORY; owner words 2026-07-24).** A selection admission
assembles the candidate core; it binds nothing — every binding claim waits for §7.12.
Admission = resolved gain at level α_r on the headline M4 **or** on M8 (standing form, pooled)
— the peak door — where α_r = 0.05 / m_r one-sided and m_r = the round's enumerated family of
TESTS (§7.9): each sealed candidate contributes one test per declared door, plus the scheduled
removal tests (F3 verification, finding 4); a Bonferroni tightening of the owner's CI90 base,
never a loosening, retained as exploratory hygiene. AND, either door: no resolved-at-CI90 regression on
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
jointly re-fit; a unit whose removal yields resolved gain at level α_r is dropped and
recorded — the removal tests are scored at the same family level they are counted at (F3
verification, finding 4).
The removal unit is the registered admission unit — a bundle admitted as a unit removes as a
unit. Scheduled removal tests count in the round's family m_r. Joint refit is inherent to every
step, so the core never fossilizes at entry settings.
7.8 **Stopping rule (F3 findings 14, 11).** Row identity = (metric, slice tuple, panel
version); the test evaluates on the CURRENT map against the CURRENT core. The race stops when a
round closes with zero admissions AND every currently-resolved row carries a bundle tested
against the CURRENT core version — tests against any earlier core never discharge; a stopping
round has zero admissions, so its round-start core IS the current core and that round's own
sealed bundle tests discharge mechanically (F3 verification, finding 14) — with the
diffuse-gap clause: if the pooled C3−C2 gap stays resolved while no row resolves, stopping is
permitted but the fork report must state the undischarged pooled gap explicitly. Weak-ceiling
case per §8.2. Or the owner's word, any time. Then §7.12 runs and the fork report goes to the
owner. Captured share is reported throughout: (C0→C2 gain) / (C0→C3 gap), pooled and per lens.
7.9 **Multiplicity honesty (F3 finding 4; Dial-8).** The complete per-round experiment family
is enumerated in the ledger BEFORE scoring: m_r = Σ over sealed candidates of their declared
door-tests, plus scheduled backward removals. Every adjudication-outcome access is logged; the
screening ban keeps screening out of the family entirely. Under Dial-8 this per-round regime is
EXPLORATORY HYGIENE, not the race's inferential claim: the round cap and lifetime re-entry caps
bound the exploration, and the single binding family is §7.12's dispositive confirmation event.
7.10 **Structural gates, enumerated with predicates and margins (F3 verification, finding
15).** Numeric gates emit PASS/FAIL with a measured value and margin; identity gates are
expressly non-numeric predicates (present/absent, match/mismatch); a missing emission from
either class is a RED (Law 2 / SILENCE-IS-RED).
NUMERIC GATES:
- **REF-RECENCY** — per-game weight deltas over the years-back grid all ≤ 0; margin = max delta.
- **REF-WDG** — every evidence-count transform: max adjacent-count step ≤ 5% of the transform's
  fitted range; margin = largest step share. No hard evidence floors, ever. NOT softened by the
  Law-3 interpretive read.
- **REF-SMOOTH-EST** — every fitted 1-D shape over age, evidence, or ordinal position: max
  adjacent-grid step ≤ 5% of fitted range (Law 3 on estimators); margin = largest step share.
  Exception path (per the owner's Law-3 interpretive read, §12): an UNDECLARED step beyond the
  bound HALTs; a mechanism may instead REGISTER a declared discontinuity — story stated, step
  measured and reported as the margin — and race as a flagged exception. The exception path is
  OPERATIVE — the owner-worded twin amendment is FILED (register v400; F2b CLOSED); the twin
  and this protocol now state one rule.
- **REF-FADE** — the L-SAGE-FADE predicates on TOTAL FITTED PREDICTIONS, per fold (owner
  routing word 2026-07-24; F3v2, finding 15). MEASURED FLOOR := the realized games-weighted
  mean production of train cells aged ≥ 33, all positions pooled, with its player-clustered
  bootstrap CI90 [floor_lo, floor_hi] — the floor's measured CI is the ONLY tolerance anywhere
  in this gate. F-1 DECLINE: per-age-year games-weighted mean TOTAL predictions over train
  cells are monotone non-increasing across ages 30, 31, 32, 33+ (margin = max positive
  adjacent step; no band). F-2 NEVER BELOW: EVERY individual total prediction for a train cell
  aged ≥ 33 is ≥ floor_lo (margin = min over cells of prediction − floor_lo). F-3 TOWARD, NOT
  PROPPED: the pooled games-weighted mean total prediction over train cells aged ≥ 33 lies
  inside [floor_lo, floor_hi] (margin = distance to the violated bound). ESCALATION CLAUSE
  (owner word): if round-0 or certification measurement shows these strict predicates
  unworkable — for example, C0 itself cannot pass — the seat escalates to the owner with the
  measurements; the predicates never silently loosen.
- **REF-MANIFEST** — provenance rows missing = 0; margin = 0 − missing.
- **REF-CANARY** — canaries halted − canaries shipped = 0; margin = that difference.
- **REF-FIXTURE** — max absolute deviation across Appendices A–B = 0 exactly; margin = the
  deviation.
- **REF-NULLCAL** — observed null resolutions ≤ c per §4; margin = c − observed.
IDENTITY GATES (non-numeric predicates, declared as such):
- **REF-CEIL** — hash scan: no C3 output present in any adoption artifact.
- **REF-SEAL** — every official score is preceded by its declaration seal; every
  adjudication-outcome access appears in the log.
- **REF-JOINT** — the full-joint-refit flag is asserted on every admission-deciding run.
- **REF-FOLD** — panel md5, fold-spec md5 and panel version match their pins.
- **REF-VOCAB** — every raw position value is inside the §5.1 frozen table.
- **REF-FRAG** — every registry addition carries distinctness notes against each prior class.
- **REF-C3PIN** — the environment lockfile shows LightGBM 4.3.0 exactly (§8.1).
- **REF-SYMMETRY** — Law 5, mechanical form: declared estimator forms contain no direction-
  conditional branch on performance deltas; a registered asymmetric mechanism must be ONE
  shared fitted curve evaluated identically for every cell — machinery symmetric, shape free —
  with its fitted asymmetry reported with CI as a numeric margin where present.
"Green" = every enumerated gate emits its verdict in its declared class. The 5% step bounds
are seat-set constants (§12 ledger).
7.11 **Determinism (F3 finding 12).** All sealed candidates in a round score against the
ROUND-START core. Class representative = the best passing variant by (headline point gain, then
the α-level percentile lower bound, then earliest registry index). Exactly ONE admission per
round — the passing candidate leading by the same key; every other passer flags
PASSED-NOT-ADMITTED and auto-reseals next round, consuming no new budget and counting in the
next round's family. The joint refit after admission produces the next round-start core; the
backward pass then runs. No tie ever resolves by seat discretion.
7.12 **The vault read — ERA-SCOPED (Dial-8 · Dial-9, RULED at register v402: the vault claims
only the confirmation-era population).** Selection assembles; the vault housekeeps; the
prospective gate (§7.13) decides. At stop, ONE sealed batch, run list sealed before the vault
opens, one physical touch:
(1) **Era scores.** C0, assembled C2 and C1R scored on confirmation folds, paired.
(2) **Door-matched ingredient ablations (F3v2, finding 6).** Each admitted unit k is tested by
removal against ITS OWN door metric — M4-door units on M4. M8-door units have no in-panel W6
confirmation folds: they pass to §7.13 as PROVISIONAL, untested here. A unit CONFIRMS-IN-ERA
iff its removal resolvedly harms its door metric at 0.10/K one-sided.
(3) **STRIP (Dial-8, owner word).** Units failing (2) are stripped. PG-CORE (the
prospective-gate core) = C2 minus stripped units, jointly refit on train.
(4) **SCOPE OF EVERY CLAIM (Dial-9; F3v2, findings 3, 4, 7).** Every statistic in this section
is a claim about the FIXED confirmation-era population — the 2020-onward cutoff cohorts —
under player-resampling uncertainty only. DECLARED LIMIT L-U2: no inference to future seasons
is made or implied by the vault. DECLARED LIMIT L-U3: the post-strip PG-CORE's era score vs C0
(reported at α = 0.05, descriptive) is computed on the folds that selected the strip branch —
one of up to 2^K branches — and is therefore labelled BRANCH-SELECTED, carries no multiplicity
claim, and decides nothing. The branch circularity the F3 seat identified is real; it is
broken at the binding layer, where §7.13 scores the frozen PG-CORE on seasons that did not
exist when the branch was chosen.
(5) **NULL RESULT.** If assembled C2 fails to resolvedly beat C0 in-era, or the effect
reverses sign (flagged in its own right), the fork report says so plainly; no PG-CORE issues;
the owner rules next steps.
(6) **Fork report.** Presents the ADOPTION-ELIGIBLE core (era-confirmed units only) and the
TRACKING core (plus provisional M8 units), never conflated. Adoption eligibility beyond the
fork report belongs to §7.13. After the event, confirmation folds retire into selection for
any owner-worded follow-on race (panel-version bump).

7.13 **THE PROSPECTIVE GATE — BINDING (Dial-9, RULED at register v402, owner word:
prospective-dispositive; adoption staged and reversible).** The only binding inference in this
protocol. Its sampling unit is future seasons as they complete — evidence no selection or
strip decision can have touched, because it did not exist.
(1) **Freeze at fork report.** PG-CORE and C0 freeze as RECIPES: ingredient set, functional
forms and the per-fold refitting procedure — no new ingredients, no re-selection, ever;
parameters refit on train ≤ t per the frozen recipe at each evaluation. Every PG-CORE unit
carries its door label (M4-door / M8-door); M8-door units carry PROVISIONAL status and remain
barred from adoption artifacts until confirmed here (Dial-8).
(2) **Cadence.** Each scheduled panel extension (completed season S; §9.6) creates the newly
completed prospective cutoffs: t = S−1 (W1), t = S−3 (W3), t = S−6 (W6/M8). Each cutoff is
claimed once, at the extension that completes it; the prospective evidence set at any moment =
all such cutoffs accrued since the fork report, pooled.
(3) **Door-matched scoring (F3v2, finding 6).** Core claim: PG-CORE vs C0, paired, on M4 over
accrued W3-complete prospective cutoffs — and on M8 over accrued W6-complete cutoffs once any
exist. Unit tests: removal ablations against each unit's OWN door metric on the accrued
door-relevant cutoffs, PG-CORE-minus-unit jointly refit per the frozen recipe.
(4) **Predeclared levels and accrual floor.** Core claim resolved at α = 0.05 one-sided on the
pooled prospective set, paired player-clustered bootstrap per §4 — honestly labelled: early
accruals are few and prospective power grows season by season; the seasons themselves are the
independent draws no historical resampling could supply. Unit family at each extension:
α_unit = 0.10 / K_p one-sided, K_p = units under prospective test at that extension. ACCRUAL
FLOOR: MIN_PROS = 3 door-relevant prospective cutoffs must have accrued before any
fail-to-confirm strip can fire; until then a unit's status is UNDER PROSPECTIVE TEST.
Exception: a unit whose removal shows resolved door-metric IMPROVEMENT — resolved harm from
the unit — strips immediately at any accrual.
(5) **Strip and re-freeze.** A stripped unit leaves PG-CORE; the reduced recipe re-freezes and
continues; its future evaluations occur on later extensions — data that does not exist at
strip time, so no strip branch is ever assessed on the evidence that selected it (F3v2,
finding 3, resolved at the binding layer by temporal ordering).
(6) **Staged, reversible adoption (owner words; Law 10 untouched).** The gate stages
ELIGIBILITY only; every adoption act is the owner's word under the seam pattern. STAGE 1
eligibility: the core claim resolves on M4 at the first extension with ≥1 W3-complete
prospective cutoff. STAGE 2 eligibility: the core claim holds resolved at two consecutive
extensions. REVERSIBILITY: every owner-worded adoption release records its rollback target; if
at any later extension the pooled core claim shows resolved harm — PG-CORE resolvedly losing
to C0 on M4 — a REVERSION FLAG raises to the owner with the rollback path; a post-adoption
unit strip raises a re-release flag. Flags raise; only the owner's word acts.
(7) **Ledger.** Every extension's prospective scorecard — accrued cutoffs, K_p, levels,
margins, strips, stage status, flags — files in the referee ledger under the extension's
panel version.

## 8 · THE CEILING AND THE INTERACTION MAP
8.1 **Spec, fully frozen (F3 verification, finding 11).** Implementation: LightGBM **4.3.0
exactly**, pinned by this protocol — the environment lockfile must show it (REF-C3PIN, HALT).
Exact configuration, parameter names as the library spells them: boosting_type='gbdt';
objective='regression' with metric='l2' for production heads, objective='binary' with
metric='binary_logloss' for survival heads; n_estimators=5000 with early_stopping_rounds=50 on
the §2.3 inner-eligible validation set using the head's metric above; grid, selected per fold
by lowest inner metric with ties to smaller num_leaves, then smaller learning_rate, then
smaller min_child_samples: num_leaves ∈ {15, 31, 63} × learning_rate ∈ {0.03, 0.1} ×
min_child_samples ∈ {20, 50}; all remaining parameters fixed, not defaulted silently:
max_depth=-1, min_child_weight=1e-3, min_split_gain=0.0, lambda_l1=0.0, lambda_l2=0.0,
bagging_fraction=1.0, bagging_freq=0, feature_fraction=1.0, use_missing=True,
zero_as_missing=False, deterministic=True, force_row_wise=True, num_threads=1,
seed = bagging_seed = feature_fraction_seed = 20260724 + fold-index. NO-INNER-VALIDATION
RULE (F3v2, finding 11): on outer folds where the head has no §2.3 inner-eligible cutoff (W1
at t = 2009; W3 at t ≤ 2011; W6 at t ≤ 2014), early stopping is DISABLED, n_estimators is
FIXED at 300, and the grid collapses to its §2.3 default cell — num_leaves = 31,
learning_rate = 0.03, min_child_samples = 20, the grid medians, lower on even — with the fold
flagged DEFAULT-TUNED. Features = the frozen
§3.1 manifest, all origin-safe; position enters as the §5.1 frozen groups via
categorical_feature, declared in the manifest. Deliberately unconstrained by estimator-shape
laws — which is exactly why REF-CEIL bars its outputs from adoption artifacts forever.
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
report cite current-version numbers only; each extension also fires the §7.13
prospective evaluation, and M8/M6W confirmation-era additions land per §§7.12–7.13.

## 10 · FREEZE RULES
Preconditions, in order: **F1** — the §11 compliance map verified line-by-line; **F2** — the owner
rules Dials 1–5 (since extended: 1–8); **F2b** — the acceptance-twin L-SMOOTH amendment
worded and filed, else the §7.10 exception path and the §6 banded comparator stay struck;
**F3** — one cold blind review of THIS protocol by a seat that is neither its
author nor the harness implementer (Dial-5 confirms); **F4** — the owner's freeze word, recorded in
the register. Status at v0.8: Dials 1–9 ruled; the twin amendment FILED (register v400; F2b CLOSED). F3v2
findings 3, 4 and 7 resolve under Dial-9's prospective-dispositive architecture; 6, 10a, 11
and 15 close by full specification; stale twin language conformed — the same F3 seat verifies
v0.8; then F1 re-verification; F4 closes.
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
- **Dial-8 · Inferential architecture — RULED: SELECTION EXPLORATORY, CONFIRMATION DISPOSITIVE**
  (owner word, register v399, 2026-07-24). Encoded §7.12: failed confirmation STRIPS the unit;
  provisional M8 units are BARRED from adoption artifacts until confirmed; selection-era
  statistics are exploratory hygiene, never binding claims (§§7.5, 7.9, §4).
- **Dial-9 · Binding architecture — RULED: PROSPECTIVE-DISPOSITIVE** (owner word, register
  v402, 2026-07-24). The §7.12 vault read claims only the confirmation-era population with its
  declared limits stated (L-U2, L-U3); the BINDING gate is §7.13: every scheduled panel
  extension scores the frozen PG-CORE vs C0 under predeclared door-matched rules; failing
  units strip; adoption is staged and reversible — eligibility mechanical, every adoption act
  the owner's word (Law 10).

TWIN AMENDMENT — FILED (owner words "Twin line approved," 2026-07-24, this channel; Law 10
act executed by the pen at register v400; F2b CLOSED). acceptance_v2_0.json, gate L-SMOOTH,
the governing line as filed on main:
"check": "no undeclared value discontinuities across age/evidence/position; a discontinuity
is lawful only if registered before scoring with its step measured and reported as a margin"
Filed and live on main; §7.10's exception path and §6's banded comparator are operative.

SEAT-SET CONSTANTS LEDGER (the Dial-3 delegation pattern; each figure moves on one owner word,
none may be cited as owner-worded): SUPPORT_MIN = 200 eligible cells; smoothness/WDG step bound
= 5% of fitted range; R_MAX = 6 rounds; class lifetime = 3 raced rounds; selection/confirmation
boundary = 2019/2020; canaries ≥ 3; null-candidates ≥ 20; probability clip = 1e-4; B = max(2000,
⌈50/α⌉); bootstrap seed base = 20260724; NULLCAL N = 200 with pass bound c = min{c : BinomCDF(c; N, α)
≥ 0.95} (c = 15 at α = 0.05); REF-FADE tolerance = the measured floor's CI90, nothing else; C0-smooth knots
{21, 24, 27, 30}, boundary {18, 33}; M5 truncation = 6 seasons; capacity-dial default = grid
median; LightGBM = 4.3.0 exactly; C3 no-inner rule: n_estimators = 300 fixed on the default grid
cell (31, 0.03, 20); MIN_PROS = 3 door-relevant prospective cutoffs; adoption staging:
Stage 1 = first resolved extension, Stage 2 = two consecutive extensions.

## APPENDIX A · WORKED STANDING FIXTURE (REF-FIXTURE; harness must reproduce bit-exactly)
One cutoff, W1, five eligible cells. Realized means r = (90, 80, 70, 60, 50); realized games
g = (20, 10, 20, 5, 20); predictions p = (85, 82, 60, 65, 40). Mid-rank percentiles, higher =
better: realized → (90, 70, 50, 30, 10); predicted → (90, 70, 30, 50, 10). Per-cell |Δpct| =
(0, 0, 20, 20, 0); weights = g. Weighted MAE = (20·0 + 10·0 + 20·20 + 5·20 + 20·0) / 75 =
500 / 75 = **6.6667** (4 dp). Any harness not reproducing 6.6667 on this fixture HALTs.

## APPENDIX B · DISCRIMINATING FIXTURES (REF-FIXTURE; harness must reproduce bit-exactly)
**B.1 · W3 predicted-production functional.** One cell, W3, emitted triples (P, G, μ):
s1 = (1.0, 20, 100); s2 = (0.5, 10, 60); s3 = (0.0, –, –). Frozen functional:
p = (1.0·20·100 + 0.5·10·60) / (1.0·20 + 0.5·10) = 2300 / 25 = **92.0** exactly. Rejected
readings provably differ on this fixture: unweighted mean of conditional means = 80.0;
P-weighted mean of means = 86.6667. Any harness not returning 92.0 HALTs.
**B.2 · Reach-weighted peak.** One cell, W6, (μ, P) with three live seasons: (150, 0.01),
(100, 0.9), (90, 1.0); remaining seasons P = 0. Π(1−P) = 0.99·0.1·0 = 0 → denominator 1.
Predicted peak = 150·0.01 + 100·(0.99·0.9) + 90·(0.99·0.1·1.0) = 1.5 + 89.1 + 8.91 =
**99.51** exactly. The naive max-of-conditional-means reading returns 150 — the closed
remote-peak route. Any harness not returning 99.51 HALTs.
**B.3 · D3 identity test.** With ingredient B constructed as an exact duplicate of A inside
the core, the harness must return contribution(A | S) = 0 exactly, per the §5.2 formula.
**B.4 · C0-smooth basis rows (F3v2, finding 10a).** Knots (20, 24, 28, 32), unnormalized
restricted-cubic-spline basis per §6, coefficient order (1, a′, X₁, X₂): at a′ = 26 the row is
exactly (1, 26, 216, 8); at a′ = 33 the row is exactly (1, 33, 1824, 480). Any harness not
reproducing both rows bit-exactly HALTs (REF-FIXTURE).

*Design seat, ITEM 410 · returns to the owner; the pen files.*
