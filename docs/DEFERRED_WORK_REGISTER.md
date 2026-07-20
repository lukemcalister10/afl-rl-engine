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
