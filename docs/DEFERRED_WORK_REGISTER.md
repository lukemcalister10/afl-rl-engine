# Deferred Work Register

**Repository:** `lukemcalister10/afl-rl-engine`  
**Register established:** 2026-07-21  
**Authority:** owner and supervisor  
**Purpose:** preserve non-blocking concerns, future investigations, and postponed decisions so they cannot disappear into chat history, handovers, or superseded implementation branches.

This register is not an instruction to alter the live valuation engine. A registered item may not change production values, ranks, release artifacts, or updater behaviour until it is separately activated under a bounded directive and the owner rules on the resulting evidence.

## Status vocabulary

- **PROPOSED** — suggested work not yet authorized.
- **PARKED** — recognized and intentionally deferred; no present implementation work.
- **ACTIVE-DIAGNOSTIC** — authorized read-only investigation is underway.
- **ACTIVE-IMPLEMENTATION** — owner-authorized implementation is underway under a bounded protocol.
- **BLOCKED** — cannot proceed until a named dependency or owner ruling is resolved.
- **OWNER-RULED** — the owner has made the material decision; implementation or documentation may still remain.
- **CLOSED** — resolved with durable evidence and an explicit closure record.
- **REJECTED** — investigated and deliberately not adopted.

Evidence labels used inside entries:

- **VERIFIED** — independently established from repository objects, committed artifacts, or reproduced results.
- **REPORT-ONLY** — stated by an agent or document but not independently verified.
- **HYPOTHESIS** — plausible explanation requiring testing.
- **OWNER-RULED** — direct owner decision.

## Maintenance rules

1. **Permanent IDs.** Every item receives a stable domain ID such as `VAL-001`, `DATA-001`, `UI-001`, `OPS-001`, or `AUD-001`. IDs are never reused.
2. **Record the discovery path.** Each entry states who noticed the issue, what observation triggered it, and how the repository evidence was traced.
3. **No vague parking.** Every PARKED item must name a reopening trigger, required work, and the owner decision needed at the end.
4. **No deletion.** Closed or rejected items remain in the register with the resolving commit, PR, report, and ruling.
5. **Builders cannot self-close material items.** Claude Code or another builder may supply evidence, but the owner or supervisor must set `OWNER-RULED`, `CLOSED`, or `REJECTED`.
6. **No named-player tuning.** A player example may identify a defect or calibration concern, but any valuation change must be justified by a predeclared population-wide test.
7. **Release review.** At each release-candidate closeout, review all non-closed entries and explicitly state whether each blocks the release, remains parked, or is activated.
8. **Handover review.** Every durable project handover must link this register and summarize any status changes since the prior handover.
9. **Evidence before status change.** An item moves from PARKED to ACTIVE only under a written scope that defines the question, allowed files, forbidden changes, tests, and stop conditions.
10. **One source of truth.** GitHub is authoritative. Chat discussions may explain an item but do not replace updating this file.

## Open-item index

| ID | Title | Status | Current release blocker? | Reopen trigger |
|---|---|---|---:|---|
| `VAL-001` | Possible double-conservatism for young proven elite scorers | PARKED | No | After v2.11 read-only release and live-scoring stabilization; before the next valuation-changing bake |
| `AUD-001` | Independent read-only model architecture and calibration audit | PROPOSED | No | Owner launches a separate audit chat/workstream with the sealed read-only prompt |
| `AUD-004` | Historical validation framework | OWNER-RULED | No | After Stage 1 and live-scoring stabilization, before the next material valuation-changing bake or any claim of predictive validation |
| `AUD-005` | Empirical versus policy layers | OWNER-RULED | No | Future audit finds policy presented as empirical validation, or empirical mechanisms shielded from testing by being called policy |
| `AUD-006` | Weighting and incomplete-career treatment | BLOCKED | No | AUD-004 establishes accepted origin-safe folds, data snapshots, and protocols |
| `AUD-007` | Layer interactions and possible signal reuse | BLOCKED | No | AUD-004 is complete enough to support predeclared ablations |
| `AUD-008` | Known-injury register | OWNER-RULED | No | After Stage 1, before material injury-layer recalibration, or if register-control failures are observed |
| `AUD-009` | Captaincy premium | OWNER-RULED | No | Before the next captaincy-premium recalibration or when suitable data become available |
| `AUD-010` | Structural constraints and floors | OWNER-RULED | No | After Stage 1, before changing any structural surface, threshold, floor, or constraint |
| `AUD-011` | Player/pick common-currency calibration | PARKED | No | After Stage 1 and before the next material PVC or player-value scale change |
| `AUD-012` | Threshold and discontinuity census | PARKED | No | Supervisor activates follow-up review or any threshold-changing implementation is proposed |
| `AUD-013` | DPP valuation treatment | OWNER-RULED | No | Source-data anomaly, eligibility-rule change, or evidence that valid league combinations are rejected |
| `AUD-014` | Experimental reproducibility | CLOSED | No | Closed; requirements remain operative through AUD-004 |
| `AUD-015` | `surv` writer/consumer trace | PARKED | No | AUD-016 consumer and code-authority census or post-Stage-1 cleanup scope |
| `AUD-016` | Canonical-code and dormant-path authority map | PARKED | No | Immediately after Stage 1 stabilization, or earlier only if supervisor explicitly activates the static census for review |
| `AUD-017` | Transparent baselines | BLOCKED | No | AUD-004 origin-safe framework is frozen |

---

## VAL-001 — Possible double-conservatism for young proven elite scorers

**Status:** PARKED  
**Domain:** player valuation / demonstrated level / evidence treatment  
**Current release impact:** non-blocking for the read-only v2.11 release  
**Reopen trigger:** after v2.11 read-only release and live-scoring stabilization, but before any later valuation-changing bake  
**Owner ruling so far:** do not chase during the current build; preserve for later population-wide review

### How the issue was identified

1. **Owner visual observation.** While reviewing a mobile screenshot of the v2.11 release candidate, the owner noticed Luke Jackson ranked first, Nick Daicos second, and Harry Sheezel third.
2. **Owner domain challenge.** The owner compared the displayed ordering with age, draft position, current eligibility, and demonstrated scoring, then supplied the recent seasonal averages:
   - Harry Sheezel: 2026 `115.4`, 2025 `109.1`, 2024 `112.1`;
   - Nick Daicos: 2026 `111.9`, 2025 `118.4`, 2024 `117.1`;
   - Luke Jackson: 2026 `120.8`, 2025 `112.9`, 2024 `94.5`.
3. **Supervisor code trace.** The supervisor inspected the live release lineage rather than assuming a ranking bug. The trace followed the level calculation through:
   - `engine/rl_after/_merged_recover.py`;
   - `engine/forward_valuation/conditional_prior.py`;
   - `session_2026-07-15/evidence_weight/measurement/AFFECTED_ROWS.md`;
   - `session_2026-07-15/improver/measurement/AFFECTED_ROWS.md`;
   - `session_2026-07-15/captaincy/measurement/AFFECTED_ROWS.md`.
4. **Mechanism located.** The investigation found two distinct caution/trust mechanisms that combine before pricing:
   - the continuous evidence-weight layer (`RL_EVW`), including a permanent residual draft-pedigree weight;
   - the elapsed-opportunity/improver layer (`_eo` / `RL_EO2`), which controls how much of the recent-production target is admitted according to career year and exposure.
5. **Asymmetric restoration observed.** The evidence artifacts show that evidence weighting lowered all three players, after which the improver layer restored them by very different amounts.

### Verified observations

**Evidence-weight stage:**

- Harry Sheezel: level `110.5 -> 107.2`;
- Nick Daicos: level `112.6 -> 109.5`;
- Luke Jackson: level `109.2 -> 107.5`.

**Improver stage:**

- Harry Sheezel: level `107.2 -> 110.1`;
- Nick Daicos: level `109.5 -> 112.7`;
- Luke Jackson: level `107.5 -> 116.6`.

The evidence-weight layer derives an effective-qualifying-season quantity `E_q` from a smooth per-season games curve. It then uses `E_q` to control:

- trust in the recency-weighted current level;
- movement toward the established-player treatment;
- a draft-pedigree weight that fades toward, but never below, a residual floor of `0.11`.

The elapsed-opportunity layer then blends the conservative/evidence-weighted level toward a more aggressive demonstrated-production target. Its career-year component gives approximately:

- Sheezel: 50% access to the aggressive target;
- Daicos: 75%;
- Jackson: 100%, subject to exposure.

### Current hypothesis

**HYPOTHESIS:** the architecture may charge related uncertainty twice for players who are young by career tenure but already have substantial high-quality AFL evidence.

Possible overlap:

1. `RL_EVW` already controls trust using qualifying-season evidence and retains a permanent pedigree residual.
2. `_eo` then applies another career-year/exposure ramp before the recent demonstrated target is fully trusted.

This can leave a four-season, 80-game player materially below demonstrated production while a longer-tenure player receives the full target even when that target is driven chiefly by the latest two seasons.

### What has not been concluded

- No implementation bug has been established.
- No conclusion has been reached that Luke Jackson is overvalued.
- No conclusion has been reached that Sheezel or Daicos must rank above Jackson.
- No named player should receive an exception or manual adjustment.
- The issue may reflect valid independent uncertainty controls; that must be tested rather than assumed.

### Required future diagnostic

Before any code change, create a sealed read-only protocol that:

1. Defines the population and historical as-of folds before results are inspected.
2. Separately ablates:
   - the `RL_EVW` pedigree residual;
   - the established-weight transition;
   - the `_eo` career-year term;
   - the `_eo` exposure term;
   - combinations of those components.
3. Measures out-of-sample prediction of next-season and multi-season production, availability, and forward value outcomes.
4. Tests whether each layer adds predictive information after controlling for games, effective qualifying seasons, current level, age, position, and draft pedigree.
5. Reports calibration and error by:
   - career games;
   - effective qualifying seasons;
   - age;
   - position;
   - elite/current-output band;
   - rising, flat, and declining trajectories.
6. Compares against simple transparent baselines, including game-weighted recency averages and shrinkage models.
7. Reports the complete affected-player distribution, not only Sheezel, Daicos, Jackson, or Pickett.
8. Prohibits tuning after named-player results are observed.
9. Ends with a decision memo presenting retain/change/reject options and their population-wide consequences.

### Owner decision required at closure

The owner must rule whether:

- both mechanisms measure distinct risks and should remain;
- one mechanism should be weakened or removed;
- the evidence axes should be consolidated;
- the current behavior is accepted despite the apparent conservatism.

---

## AUD-001 — Independent read-only model architecture and calibration audit

**Status:** PROPOSED  
**Domain:** independent assurance  
**Current release impact:** non-blocking; must not interrupt the active release and updater tracks  
**Proposed execution:** a separate ChatGPT conversation/workstream with read-only GitHub access and no authority to modify branches, PRs, tags, releases, data, or model code

### Purpose

Conduct an adversarial review of the valuation system as a whole, looking for:

- duplicated information or double counting;
- internally inconsistent treatment of evidence, age, trajectory, position, availability, pedigree, and captaincy;
- discontinuities, cliffs, hidden branch effects, and non-monotonic behavior;
- mechanisms that are individually defensible but reinforce one another unexpectedly;
- stale assumptions or superseded layers still affecting the live path;
- leakage, circular calibration, survivorship bias, censoring errors, or in-sample validation presented as predictive evidence;
- fragile determinism or provenance dependencies;
- simpler alternatives that preserve or improve out-of-sample performance;
- missing diagnostics and insufficiently transparent owner-facing explanations.

### Audit boundary

The audit is evidence-gathering only. It may clone, inspect, execute tests, and create local scratch outputs, but must not:

- push commits;
- create or edit GitHub issues or PRs;
- modify repository branches;
- tune parameters after inspecting named-player results;
- recommend adoption solely because a handful of recognizable players look better.

Every finding must distinguish:

- verified defect;
- calibration concern;
- design trade-off;
- unverified hypothesis;
- optimization opportunity.

Findings should be returned to the owner and supervisor for triage into this register. No finding becomes active implementation work without an owner ruling and a separate bounded protocol.

### Proposed acceptance standard

The audit return should include:

1. An executive finding table ranked by materiality and confidence.
2. Exact file and line references.
3. Reproduction commands and generated evidence.
4. The strongest counterargument to every major criticism.
5. Any interaction or double-counting map between model components.
6. A list of recommendations divided into:
   - fix before next valuation bake;
   - investigate later;
   - documentation/transparency only;
   - reject/no action.
7. No repository writes and no claim that a finding is accepted until the owner rules.

---

## AUD-004 — Historical validation framework

**Status:** OWNER-RULED
**Domain:** historical validation / leakage control / model assurance
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** prerequisite framework for AUD-006, AUD-007, AUD-014, and AUD-017
**Reopen trigger:** after Stage 1 and live-scoring stabilization, before the next material valuation-changing bake or any claim of predictive validation
**Owner ruling so far:** the existing historical book is retrospective lifecycle reconstruction, not genuine origin-time validation

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Subsequent owner triage accepted the finding as an owner-ratified validation boundary and future framework requirement.

### Verified observations

**OWNER-RULED:** The existing historical book must be described as retrospective lifecycle reconstruction, not as genuine origin-time validation or validated predictive evidence.

**REPORT-ONLY:** The audit concern is that historical or “walk-forward” presentation can overstate predictive assurance unless historical as-of data, frozen folds, eligibility rules, leakage controls, and immutable evaluation protocols exist.

### Owner ruling and accepted design boundary

The owner ruled that the existing book is preserved but must not be described as leakage-free, out-of-time, or validated predictive evidence. A separate origin-safe framework must be created later before testing model changes.

### What has not been concluded or authorized

No production value, ranking, parameter, or economic-policy change is authorized. This entry does not invalidate the operational board, does not complete origin-safe validation, and does not authorize any model change.

### Required future diagnostic or implementation

Define historical as-of datasets, frozen folds, eligibility rules, leakage controls, immutable evaluation protocols, and predeclared outcomes before testing model changes. The framework must prevent tuning after recognizable named-player outputs are inspected.

### Reopening trigger and closure standard

Reopen after Stage 1 and live-scoring stabilization, before the next material valuation-changing bake or any predictive-validation claim. Closure requires an owner-reviewed origin-safe protocol with reproducible fold artifacts, leakage controls, immutable evaluation artifacts, and explicit evidence that the protocol was followed.

---

## AUD-005 — Empirical versus policy layers

**Status:** OWNER-RULED
**Domain:** model governance / empirical evidence / economic policy
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** none
**Reopen trigger:** a future audit finds owner policy presented as empirical validation, or empirical mechanisms shielded from testing by being called policy
**Owner ruling so far:** the engine is intentionally hybrid

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage converted it into a standing documentation and audit-classification ruling.

### Verified observations

**OWNER-RULED:** Documentation and future audits must distinguish empirically estimated mechanisms, owner policy decisions, structural accounting rules, and defensive constraints.

### Owner ruling and accepted design boundary

The model is intentionally hybrid and is not required to make every component an empirical estimate. Owner policy decisions require owner authority and transparent separation from empirical performance claims.

### What has not been concluded or authorized

No production value, ranking, parameter, or economic-policy change is authorized. This entry does not imply every model component is an empirical estimate and does not allow predictive mechanisms to avoid testing merely by being labelled policy.

### Required future diagnostic or implementation

Future reports should label empirical estimates, owner policies, structural accounting rules, and defensive constraints separately, including incidence and regression-protection language where relevant.

### Reopening trigger and closure standard

Reopen if future documentation or audit evidence blurs these categories. Closure requires durable report language and owner/supervisor agreement that the distinction is preserved.

---

## AUD-006 — Weighting and incomplete-career treatment

**Status:** BLOCKED
**Domain:** historical estimation / weighting / censoring
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** blocked until the origin-safe AUD-004 framework exists
**Reopen trigger:** AUD-004 establishes accepted origin-safe folds, data snapshots, and protocols
**Owner ruling so far:** no weighting or incomplete-career change is authorized

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Triage blocked it behind AUD-004 because fair testing depends on origin-safe evidence.

### Verified observations

**HYPOTHESIS:** Observation weighting, incomplete careers, right-censoring, differing career lengths, and repeated player-season rows may affect estimation or evaluation. No preferred replacement has been established.

### Owner ruling and accepted design boundary

The current treatment is not rejected in advance. Weighting and incomplete-career methods may only be compared under predeclared origin-safe diagnostics.

### What has not been concluded or authorized

No production value, ranking, parameter, weighting method, incomplete-career treatment, or economic-policy change is authorized.

### Required future diagnostic or implementation

After AUD-004 exists, compare predeclared row, player, career, fold, incomplete-career, right-censoring, and minimum-history treatments. Report overall and cohort-level results without selecting methods after recognizable player outputs are inspected.

### Reopening trigger and closure standard

Reopen when AUD-004 is accepted and frozen. Closure requires comparative origin-safe evidence and an owner ruling to retain or change the current treatment.

---

## AUD-007 — Layer interactions and possible signal reuse

**Status:** BLOCKED
**Domain:** player valuation / layer interaction / double counting
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** blocked until AUD-004 provides an origin-safe test framework
**Reopen trigger:** AUD-004 is complete enough to support predeclared ablations
**Owner ruling so far:** signal reuse is not automatically double counting

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage retained it as a future population-wide ablation question.

### Verified observations

**HYPOTHESIS:** Reliability, pedigree, optionality, availability, floors, and related layers may reuse some factual signals. That possibility does not by itself establish double counting.

### Owner ruling and accepted design boundary

**OWNER-RULED:** Signal reuse is not automatically erroneous. The question is whether predeclared ablations and population-wide outcomes show excessive amplification, cancellation, or non-defensible incremental contribution.

### What has not been concluded or authorized

No production value, ranking, parameter, layer removal, layer weakening, or economic-policy change is authorized.

### Required future diagnostic or implementation

Use AUD-004 origin-safe folds to ablate relevant layers individually and in combinations, measuring incremental predictive contribution, value incidence, amplification, cancellation, and cohort effects while separating empirical layers from owner policy overlays.

### Reopening trigger and closure standard

Reopen when AUD-004 supplies an origin-safe test framework. Closure requires population-wide ablation evidence and owner ruling.

---

## AUD-008 — Known-injury register

**Status:** OWNER-RULED
**Domain:** availability / injury information / external-data governance
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** none
**Reopen trigger:** after Stage 1, before material injury-layer recalibration, or if register-control failures are observed
**Owner ruling so far:** retain the manual known-injury register

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage accepted the manual register as a retained external-information control.

### Verified observations

**OWNER-RULED:** The manual known-injury register is retained. It is an approved way to incorporate known information that score histories may not reveal promptly.

### Owner ruling and accepted design boundary

Do not authorize removal or replacement of the register. Future work is governance and interaction control, not an instruction to infer injuries through an LLM or ignore known confirmed information.

### What has not been concluded or authorized

No production value, ranking, parameter, injury-layer recalibration, register removal, register replacement, or economic-policy change is authorized.

### Required future diagnostic or implementation

Improve provenance, expiry rules, review cadence, stale-entry detection, update authority, and interaction controls with other absence penalties or return-effect logic.

### Reopening trigger and closure standard

Reopen after Stage 1 before material injury-layer recalibration, or earlier if control failures are observed. Closure requires documented controls, interaction evidence, and owner approval.

---

## AUD-009 — Captaincy premium

**Status:** OWNER-RULED
**Domain:** captaincy / market-option valuation
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** AUD-004 origin-safe testing for future empirical review where applicable
**Reopen trigger:** before the next captaincy-premium recalibration or when suitable data become available
**Owner ruling so far:** retain captaincy as a transferable market-option premium

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage ratified the current architecture while preserving future calibration questions.

### Verified observations

**OWNER-RULED:** Captaincy is retained as a transferable market-option premium. Its value is not reduced merely because a current owner already has another captain-quality player.

### Owner ruling and accepted design boundary

The premium remains part of the architecture. Future review should examine convexity, threshold behavior, and scale under origin-safe testing, without treating the premium as pre-rejected.

### What has not been concluded or authorized

No production value, ranking, parameter, captaincy-premium change, captaincy-premium removal, or economic-policy change is authorized.

### Required future diagnostic or implementation

Review convexity, threshold behavior, scale, and population incidence under a frozen protocol. Team-specific alternatives or volatility work remain deferred unless suitable data become available.

### Reopening trigger and closure standard

Reopen before any captaincy-premium recalibration or when suitable data become available. Closure requires population evidence and owner ruling.

---

## AUD-010 — Structural constraints and floors

**Status:** OWNER-RULED
**Domain:** structural constraints / monotonicity / smoothing
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** none
**Reopen trigger:** after Stage 1, before changing any structural surface, threshold, floor, or constraint
**Owner ruling so far:** retain justified structural constraints unless future evidence establishes a better treatment

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage ratified the design boundary for structural constraints.

### Verified observations

**OWNER-RULED:** A threshold, floor, monotonic constraint, band, or smoother is not automatically a defect. Justified structural constraints may be retained where noisy or sparse observations would otherwise produce incoherent ex-ante orderings.

### Owner ruling and accepted design boundary

Future diagnostics should not presume that unconstrained sample means or fully smooth alternatives are economically correct. Constraints remain acceptable unless better evidence and owner ruling support change.

### What has not been concluded or authorized

No production value, ranking, parameter, structural-constraint removal, threshold change, floor change, or economic-policy change is authorized.

### Required future diagnostic or implementation

Measure redistribution, binding counts, discontinuities, cohort effects, value transferred between cohorts, and compensating-error risk. Compare feasible alternatives without presuming all constraints should be removed.

### Reopening trigger and closure standard

Reopen after Stage 1 before any structural surface, threshold, floor, or constraint change. Closure requires incidence evidence, counterfactual comparisons, exact-vector tests where implementation is proposed, and owner ruling.

---

## AUD-011 — Player/pick common-currency calibration

**Status:** PARKED
**Domain:** cross-asset valuation / PVC / common currency
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** owner-authorized diagnostic scope and sealed cohorts
**Reopen trigger:** after Stage 1 and before the next material PVC or player-value scale change
**Owner ruling so far:** independently validate common-currency calibration before changing PVC or player-value scale

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. It is recorded as PARKED because this directive supplied no evidence that an authorized diagnostic is genuinely active.

### Verified observations

**HYPOTHESIS:** The open question is whether release-active player values and PVC are calibrated in a defensible common currency. Discussion of the question is not evidence that a diagnostic is active.

### Owner ruling and accepted design boundary

**OWNER-RULED:** Common-currency calibration must be independently validated before changing PVC or the player-value scale.

### What has not been concluded or authorized

No production value, ranking, parameter, PVC scale, player-value scale, or economic-policy change is authorized. This entry does not presume the current PVC is wrong.

### Required future diagnostic or implementation

Future work should use untouched draft cohorts and a frozen design to examine pick-curve scale, early-versus-late allocation, pathway treatment, discounted realised player value, player/pick trade-equivalence implications, pick 1 = 3,000 as numeraire, and whether player outcomes map sensibly onto the player-value scale.

### Reopening trigger and closure standard

Reopen after Stage 1 before a material PVC or player-scale change, under an owner-authorized diagnostic scope. Closure requires an independent report and owner ruling.

---

## AUD-012 — Threshold and discontinuity census

**Status:** PARKED
**Domain:** thresholds / cliffs / implementation transparency
**Current release impact:** non-blocking for Stage 1 unless separately reclassified based on new evidence; Current release blocker? No
**Dependency:** supervisor disposition and future owner-authorized threshold review
**Reopen trigger:** supervisor activates follow-up review or any threshold-changing implementation is proposed
**Owner ruling so far:** hard boundaries are not automatically defects

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. A later static census is reported for immutable commit `03396bcf8cea8e3cb34b9005b92c5c7eaa490ccc`, but this register does not treat that static work as a completed runtime trace.

### Verified observations

**REPORT-ONLY:** A static threshold and discontinuity census exists for commit `03396bcf8cea8e3cb34b9005b92c5c7eaa490ccc`.

**REPORT-ONLY:** The census did not complete a full runtime import trace because its environment lacked NumPy. Static reachability must not be represented as runtime binding.

**OWNER-RULED:** Hard boundaries are not automatically defects. Season-level data, minimum evidence requirements, and explicit policy rules may justify discrete boundaries.

### Owner ruling and accepted design boundary

The objective is to identify avoidable cliffs while preserving justified discrete rules. Future review requires binding counts, population-wide counterfactuals, and exact-vector tests.

### What has not been concluded or authorized

No production value, ranking, parameter, threshold change, floor change, cap change, eligibility-boundary change, or economic-policy change is authorized. The census itself does not authorize threshold changes.

### Required future diagnostic or implementation

For each candidate threshold, distinguish static reachability from runtime binding, report file and line, mechanism and purpose, deliberate policy versus inherited implementation, values immediately below/at/above the threshold, absolute valuation effect, binding counts, affected cohorts, and population-wide counterfactuals. Any implementation proposal requires exact-vector tests.

### Reopening trigger and closure standard

Reopen if supervisor activates follow-up review or a threshold-changing implementation is proposed. Closure requires supervisor/owner disposition of the census, binding evidence where relevant, exact-vector tests for any proposed implementation, and owner ruling.

---

## AUD-013 — DPP valuation treatment

**Status:** OWNER-RULED
**Domain:** position eligibility / replacement bars / future-position uncertainty
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** none
**Reopen trigger:** source-data anomaly, eligibility-rule change, or evidence that valid league combinations are rejected
**Owner ruling so far:** DPP is value-add only

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage confirmed the intended DPP valuation treatment and eligibility law.

### Verified observations

**OWNER-RULED:** Current known eligibility uses the advantageous replacement bar. Future eligibility uses a probability-weighted advantageous bar. DPP is value-add only.

**OWNER-RULED:** Key eligibility is locked. KEY_FWD includes the ability to occupy a general-forward slot, KEY_DEF includes the ability to occupy a general-defender slot, and RUC is a key eligibility. Owner-confirmed invalid key/general combinations remain invalid.

### Owner ruling and accepted design boundary

Do not reinterpret or change this policy. A less advantageous alternate eligibility should not reduce current-season value, while future advantageous eligibility is probability-weighted.

### What has not been concluded or authorized

No production value, ranking, parameter, DPP redesign, eligibility-policy change, trajectory-blending change, broad recalibration, or economic-policy change is authorized.

### Required future diagnostic or implementation

Future work is limited to visible source-data error reporting and consistency checks if anomalies, rule changes, or rejected valid combinations appear.

### Reopening trigger and closure standard

Reopen on a source-data anomaly, eligibility-rule change, or evidence that valid league combinations are rejected. Closure requires visible error reporting and confirmation that valid combinations are handled consistently.

---

## AUD-014 — Experimental reproducibility

**Status:** CLOSED
**Domain:** experimental reproducibility
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** incorporated into AUD-004
**Reopen trigger:** none as a separate project; use AUD-004 for operative origin-safe reproducibility requirements
**Owner ruling so far:** documentation consolidation only

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage closed it as a separate register project because its requirements are incorporated into AUD-004.

### Verified observations

**OWNER-RULED:** The closure basis is incorporation into AUD-004. This does not mean origin-safe validation has been completed.

### Owner ruling and accepted design boundary

The reproducibility requirements remain operative through AUD-004, including frozen folds, frozen data, frozen fitted artifacts, artifact hashes, no silent refit on missing artifacts, declared reproducibility tolerance, and same-environment comparisons where practical.

### What has not been concluded or authorized

No production value, ranking, parameter, refit, artifact replacement, validation claim, or economic-policy change is authorized.

### Required future diagnostic or implementation

No separate AUD-014 project remains. Any substantive reproducibility work proceeds through AUD-004.

### Reopening trigger and closure standard

Closed as documentation consolidation. If reproducibility work becomes active, it reopens under AUD-004, not as an independent implementation authorization.

---

## AUD-015 — `surv` writer/consumer trace

**Status:** PARKED
**Domain:** export schema / dormant logic
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** linked to AUD-016 and post-Stage-1 cleanup
**Reopen trigger:** AUD-016 consumer and code-authority census or post-Stage-1 cleanup scope
**Owner ruling so far:** do not revive a survival model without evidence and a material owner ruling

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. A later snapshot finding was reported for audited commit `03396bcf8cea8e3cb34b9005b92c5c7eaa490ccc` and is parked behind AUD-016.

### Verified observations

**VERIFIED for `03396bcf8cea8e3cb34b9005b92c5c7eaa490ccc` only:** at that audited commit, the exporter calculated a local survival-like value but exported `surv: 1.0`; current values and ranks did not depend on the exported field.

**REPORT-ONLY:** Later PR #132 commits require a focused delta check before this snapshot finding is projected onto live state.

### Owner ruling and accepted design boundary

Do not revive a survival model without evidence and a material owner ruling. Do not mark this item closed before consumer tracing and safe removal or quarantine evidence exist.

### What has not been concluded or authorized

No production value, ranking, parameter, survival-model revival, field removal, UI change, exporter change, or economic-policy change is authorized. The snapshot finding must not be silently projected onto later PR #132 commits.

### Required future diagnostic or implementation

Trace all internal and external consumers, then remove or quarantine the false constant only with exact-vector and UI regression tests. Coordinate this with AUD-016's post-Stage-1 authority map.

### Reopening trigger and closure standard

Reopen under AUD-016 or a post-Stage-1 cleanup scope. Closure requires consumer tracing, safe removal or quarantine evidence, exact-vector tests, UI regression tests where relevant, and owner/supervisor closure.

---

## AUD-016 — Canonical-code and dormant-path authority map

**Status:** PARKED
**Domain:** code authority / duplicate implementation / maintainability
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** Stage 1 completion and owner/supervisor activation of cleanup scope
**Reopen trigger:** immediately after Stage 1 stabilization, or earlier only if supervisor explicitly activates the static census for review
**Owner ruling so far:** no deletion, consolidation, refactor, or valuation change is authorized now

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. A later static authority census is reported for immutable commit `03396bcf8cea8e3cb34b9005b92c5c7eaa490ccc`, but this register does not treat it as a completed runtime graph.

### Verified observations

**REPORT-ONLY:** A static authority census exists for commit `03396bcf8cea8e3cb34b9005b92c5c7eaa490ccc`.

**REPORT-ONLY:** The full runtime graph was not executed because NumPy was unavailable. Module authority does not prove every function inside that module is live. Later PR #132 commits require a focused delta review. Several census risks were overstated because existing guards were not fully credited.

### Owner ruling and accepted design boundary

The item is PARKED because this directive supplies no evidence that the static census is explicitly still under active supervisory review. Any later cleanup must preserve exact accepted vectors and updater safety.

### What has not been concluded or authorized

No production value, ranking, parameter, deletion, consolidation, refactor, dormant-path removal, updater change, or economic-policy change is authorized. This item does not prove specific functions are live or dead without further authority mapping.

### Required future diagnostic or implementation

After Stage 1, produce a canonical authority map, trace imports and runtime reachability, identify genuinely dormant or duplicate paths, and plan removal or archival under bounded commits that preserve exact accepted vectors and updater safety.

### Reopening trigger and closure standard

Reopen immediately after Stage 1 stabilization, or earlier only if supervisor explicitly activates the static census for review. Closure requires accepted authority map, prioritized cleanup plan, exact-vector-preserving changes if any, updater-safety checks, and owner/supervisor closure.

---

## AUD-017 — Transparent baselines

**Status:** BLOCKED
**Domain:** predictive benchmarking / model complexity / incremental value
**Current release impact:** non-blocking for Stage 1; Current release blocker? No
**Dependency:** blocked until AUD-004 establishes the origin-safe framework
**Reopen trigger:** AUD-004 origin-safe framework is frozen
**Owner ruling so far:** baselines are benchmarks, not pre-authorized replacement engines

### How the issue was identified

**REPORT-ONLY:** This item arose from the independent read-only audit of immutable commit `ad9ab59c2ffe45df4ccd0ac9110c203ef6420bc0`. Owner triage blocked execution until AUD-004 provides origin-safe data and protocols.

### Verified observations

**OWNER-RULED:** Two deliberately simple, transparent baselines should be built for comparison after AUD-004. They are benchmarks, not replacement engines.

### Owner ruling and accepted design boundary

Baseline 0 should be a no-training persistence model. Baseline 1 should be a small transparent structured model with a frozen feature set. Neither baseline should become another complex engine.

### What has not been concluded or authorized

No production value, ranking, parameter, engine replacement, model-selection change, or economic-policy change is authorized.

### Required future diagnostic or implementation

After AUD-004, compare the transparent baselines, empirical core, and complete model against predeclared observable outcomes such as next-season average, next-season games, next-season total points, meaningful-season probability, multi-year cumulative production, and list survival where observable. Report owner economic overlays separately from empirical predictive improvement.

### Reopening trigger and closure standard

Reopen when the AUD-004 origin-safe framework is frozen. Closure requires a predeclared baseline protocol, reproducible results, and owner ruling on whether added complexity demonstrates sufficient incremental value.
