# F3 VERIFICATION OF PROTOCOL v0.5 — filed by the supervisor pen 2026-07-24
Reviewer: same F3 cold seat. Result: **F1 PASS** (compliance map true at every citation) ·
**F3 VERDICT: FAIL** — 5 findings resolved (1, 8, 9, 12, 17), 2 resolved-with-new-issues (3, 10),
10 not resolved; 8 remaining blockers (2, 4, 5, 6, 7, 10, 11, 13, 15 — reviewer's own tally lists
nine numbers for eight blockers; the pen carries the numbered list as written). Verbatim below.

---

ITEM 410 — F3 VERIFICATION OF PROTOCOL v0.5

Seat: Same F3 cold review seat
Scope: Verification of all 17 v0.3 findings; renewed F1 compliance-map check
Protocol reviewed: docs/referee/REFEREE_PROTOCOL.md, DRAFT v0.5
Response reviewed: docs/referee/ITEM_410_F3_RESPONSE_2026-07-24.md
Register: v397
Authority: Review only. The owner retains the freeze decision.

A. F1 compliance-map verification

v391
1. Mechanism class is the admission unit → §7.1 — VERIFIED. Section 7.1 states this expressly and adds a parameter-space identity rule.
2. Fresh training-fold tuning, out-of-fold adjudication, not frozen incumbent values → §§2.3, 6, 7.4 — VERIFIED. Section 2.3 confines fitting to train data; C0 and C1R refit per fold; §7.4 jointly retunes the current core and candidate before adjudication-fold scoring.
3. Shapes may generalise from constants to curves → §7.1 — VERIFIED.
4. Rejections mean only "not at any tested construction," with tested space listed → §7.6 — VERIFIED.
5. Variants are declared before scoring under a budget → §7.2 — VERIFIED.

v392
6. Admitted ingredients retune jointly at later admission steps → §§7.4, 7.7 — VERIFIED.
7. Forward and backward/joint-refit passes → §§7.4, 7.7 — VERIFIED. The incorrect v0.3 citation has been corrected.
8. Interaction bundles carry mechanism stories and race as units → §7.3 — VERIFIED.
9. The ceiling supplies a lens-sliced interaction map that guides bundle hunting → §§8.3, 7.3 — VERIFIED.

Owner-read lines
10. Peak-horizon read → M8, TALL-DEV, admission door/guardrails and always-mapped row — VERIFIED.
11. Law-3 interpretive read → §7.10 exception path and §6 certification comparator — VERIFIED AS A MAPPING CLAIM. Both cited sections encode the sealed read described in §11. Whether that encoding remains consistent with the unchanged acceptance twin is addressed under Finding 10.

Additional v397 owner rulings
- Dial 6 — "Vault": VERIFIED AS ENCODED. Selection and confirmation cutoffs are separated; screening is inner-only; confirmation has a single-read section.
- Dial 7 — smooth C0 with certification: VERIFIED AS ENCODED.

F1 RESULT: PASS
Every claim presently appearing in §11 is true at its cited section.
That closes the clerical and cross-reference component of F1. It does not establish that the underlying specification is statistically or mechanically sufficient.

B. Verification of the 17 findings

1. RESOLVED — §11 forward/backward citation. The map now cites both §§7.4 and 7.7. The cited text contains the forward and backward procedures respectively.

2. NOT RESOLVED — BLOCKER. Protocol section: §2.3. The target-safe eligibility rule is correct, but the no-eligible-inner-fold fallback introduces a direct future-information route: "if none exist, that head's dials copy those tuned at the nearest outer fold with eligibility." For the earliest outer cutoffs, every eligible "nearest" fold is later in time. For example, a W6 head at an early outer cutoff has no historical inner cutoff with six fully observed future seasons. Copying tuning from a later outer fold imports tuning selected using data unavailable at the earlier cutoff. "Ties to the earlier fold" does not solve the case where no earlier eligible fold exists. What resolves it: The fallback must never obtain tuning from an outer fold later than t. A fixed predeclared default, a prior-only carry-forward, or an UNMEASURED/excluded early fold would be mechanically origin-safe.

3. NEW ISSUE INTRODUCED — AMEND-BEFORE-FREEZE. Protocol sections: §§2.2, 7.4 and 7.12. The original adaptive-leakage finding is substantially resolved: screening is restricted to inner folds; selection outcomes require sealed official access; confirmation outcomes remain untouched until the race stops; interaction-map feedback is confined to the selection window. The new problem is that confirmation has no dispositive consequence. Section 7.12 says the confirmation result and ablations are reported, but does not say what happens if: assembled C2 fails to confirm against C0; one or more ingredient ablations fail; the confirmation effect reverses sign; or a provisional M8 unit remains unconfirmed. M8-door units may remain inside assembled C2 and reach the fork report as PROVISIONAL–AWAITING-EXTENSION; nothing expressly bars adoption artifacts from using them before confirmation. What resolves it: Freeze the consequences of confirmation failure and the permissible status of provisional units, including whether an unconfirmed unit may enter an adoption candidate.

4. NOT RESOLVED — BLOCKER. Protocol sections: §§7.5, 7.7, 7.9 and 7.12. The protocol now bounds the number of rounds and re-entries, but it still does not implement cumulative statistical control. Per-round control is not cumulative control: each round receives family-wise level approximately 0.05 through αr = 0.05/mr. Repeating that regime for as many as six rounds does not preserve a race-wide 0.05 error rate. A finite cap bounds the maximum error inflation; it does not correct it. The two admission doors are not counted: each candidate may pass on M4 or M8. Family size mr counts candidates, not the two hypothesis tests available to each candidate. Applying level αr independently to either door can approximately double the candidate-level false-admission probability under a joint null. Backward tests are counted but not adjusted: §7.9 includes scheduled removals in mr, but §7.7 evaluates each removal at unadjusted CI90 rather than at αr. The declared family count therefore does not control the removal tests it includes. Confirmation is not currently a statistical gate: §7.12 reports confirmation at CI90 and ingredient ablations at 0.10/K, but does not make failed confirmation reverse or invalidate selection admissions. It therefore cannot serve as the claimed inferential backstop. What resolves it: Define one race-wide error budget covering every admission door, round, candidate and backward test, or explicitly make selection exploratory and place all binding inferential weight on a predeclared dispositive confirmation gate.

5. NOT RESOLVED — BLOCKER. Protocol section: §4. Most of the standing construction is now exact: eligibility, ranks, ties, weighting, cutoff aggregation and missing predictions are defined, and Appendix A fixes the W1 rank calculation. The binding W3 predicted production functional remains ambiguous: "expected games-weighted mean over W conditional on ≥1 game in W, from its emitted distribution." This can mean materially different quantities: the expectation of the realised games-weighted ratio; the ratio of expected score-points to expected games; a weighting of per-season conditional means by expected games; or a functional of a joint simulated future path. Those quantities are not generally equal. The output contract says contestants emit distributions "over future seasons," but does not state the cross-season joint structure needed for the first interpretation. M8 separately says joint dependence is not demanded, which increases the ambiguity over what contestants must emit for M3/M4. Appendix A tests only W1, where the competing constructions collapse to the same value. What resolves it: Freeze the exact W3 functional algebraically and provide a multi-season fixture in which the alternative calculations give different answers.

6. NOT RESOLVED — BLOCKER. Protocol section: §4 M8/M6W. M6W fixes one part of the original defect by binding the probability of playing at least once somewhere in W6. It does not bind the probability of reaching the particular season that generates the predicted peak. A contestant can assign: a realistic probability of playing somewhere in W6; an extremely low probability of playing in season six; and an extremely high conditional season-six mean. The M8 prediction takes the maximum conditional mean without regard to the season-specific play probability. M6W sees only P(at least one game anywhere in W6) and therefore does not penalise that construction. The aggressive remote peak route identified in the original review consequently remains available, although in a narrower form. What resolves it: The binding peak functional must account mechanically for the probability of reaching the season supplying the peak, or be defined from a fully specified joint peak distribution.

7. NOT RESOLVED — BLOCKER. Protocol section: §4 uncertainty. The paired resampling mechanics, CI form, seed schedule and empty-slice handling are now substantially better specified. The central dependence problem remains: player clustering does not capture common season or cutoff shocks; overlapping W3 and W6 windows make adjacent cutoff results strongly dependent; requiring positive point gain in two-thirds of cutoffs is a sign-consistency gate, not a correction to the bootstrap confidence coverage. The null calibration does not establish coverage. With only 20 perturbations, the smallest non-zero observed false-resolution rate is 5%. At the Bonferroni levels likely to apply, "observed rate must not exceed nominal" usually means simply observing zero failures in a sample too small to estimate the nominal tail. There is also no confidence bound around the observed rate. What resolves it: Use an inference procedure that represents both player and cutoff/season dependence, or provide a calibration study with enough independent null repetitions and a predeclared confidence criterion to demonstrate the claimed operating error rate.

8. RESOLVED — C1 leakage direction. C1 is now a labelled contaminated descriptive comparator and adjudicates nothing. Directional commentary requires evidence for the exact statistic being discussed. The blanket a-fortiori rule has been removed.

9. RESOLVED — indirect origin-safety enforcement. REF-MANIFEST supplies feature/transform provenance and cutoff assertions; REF-CANARY introduces deliberate direct, aggregate and position-join violations that must halt. This is a mechanically reviewable specification, supplemented by the three known-leak probes.

10. NEW ISSUES INTRODUCED — BLOCKER. Protocol sections: §§6 and 7.10. The original C0 conflict is resolved in one respect: the governed seed is now C0-smooth, while the banded construction is only a certification comparator. Two new defects arise. C0-smooth is not uniquely specified: "smooth low-df age curve," "≤4 effective degrees of freedom" and "free non-zero asymptote" do not freeze: curve family or basis; knot locations; penalty; effective-df computation; extrapolation; parameter bounds; optimisation objective; or treatment of sparse ages. Two conforming harness implementers could produce materially different benchmark seeds. The declared-discontinuity path conflicts with the unchanged acceptance twin: §7.10 permits a registered "declared discontinuity" to race and potentially pass. The binding L-SMOOTH gate still says: "no value discontinuities across age/evidence/position." The interpretive read is truthfully encoded, so the §11 mapping passes, but the gate contract and protocol now produce opposing verdicts for the same declared discontinuity. What resolves it: Fully freeze the C0-smooth estimator. Separately, reconcile the exception path with the governing Rulebook/acceptance twin, rather than leaving one instrument to PASS what the other says must fail.

11. NOT RESOLVED — BLOCKER. Protocol section: §8. The map support threshold, row universe, weak-ceiling behaviour and cache identity are now substantially fixed. C3 itself remains adjustable through unspecified LightGBM details: min_child is not a unique LightGBM control; the commonly used parameters min_child_samples and min_child_weight have different meanings; maximum boosting rounds are unspecified; the exact early-stopping metric is unspecified; regularisation, depth, sampling and determinism settings remain defaults; feature encoding is not completely fixed; and the LightGBM version is chosen later at harness build rather than frozen by the protocol. These choices can materially move the ceiling gap and resolved map rows, and therefore the stopping condition. What resolves it: Freeze the complete learner configuration, exact parameter names, objective/validation metrics, maximum iterations, all non-default settings and the implementation version before freeze.

12. RESOLVED — candidate ordering and state transitions. The round-start comparison base, class representative, deterministic tie-breaks, one-admission rule, automatic resealing, overlapping-bundle treatment and removal units are now specified.

13. NOT RESOLVED — BLOCKER. Protocol section: §5.1. Two problems remain. Position mapping remains discretionary: the raw-to-group table is sealed before score access, which prevents outcome-driven remapping, but the protocol does not define how raw values must map. Two implementers may seal different mappings while both complying with the text. TALL-DEV can be replaced by a different population: when TALL-DEV is thin, its binding guardrail is evaluated on all players aged ≤22. That does not measure the owner-protected TALL-DEV population. It is transparent rather than silent, but it still permits admission without a measured TALL-DEV result. This sits uneasily with both the protocol's own rule that an UNMEASURED binding metric blocks admission, and the Rulebook standard that unmeasurable rules are reported UNMEASURED, never assumed passing or silently waived. What resolves it: Freeze the actual raw-position mapping or deterministic mapping rules before freeze. An unmeasured TALL-DEV guardrail must receive an explicit disposition rather than being satisfied by a different parent population.

14. NOT RESOLVED — AMEND-BEFORE-FREEZE. Protocol section: §7.8. Row identity and panel version are now defined, and the diffuse-gap case has a stated outcome. However, a current row may still be discharged by a bundle tested against the immediately preceding core. After an admission and joint refit, the residual structure can change; a test against the prior core does not mechanically establish that the bundle addresses the row on the current core. What resolves it: A current resolved row should be discharged only by evidence generated against the current core, or by a frozen equivalence rule demonstrating that the prior test remains valid.

15. NOT RESOLVED — BLOCKER. Protocol section: §7.10. The protocol now enumerates the structural gates, but REF-FADE-FLOOR does not test the governing age-fade rule. It checks only that an age-curve family admits a free non-zero asymptote and reports that asymptote's CI. It does not check whether the fitted veteran trajectory: declines toward the measured floor; stays above that floor; or is not propped above the evidence. Those are the actual binding predicates in L-SAGE-FADE. Additionally, the blanket statement that every gate emits a measured value and margin is not matched by margin definitions for several listed gates, including REF-CEIL, REF-MANIFEST and some identity/probe gates. What resolves it: Define the measured floor and mechanically test the fitted age trajectory against every part of the binding direction rule. Specify the measured value and margin—or expressly a non-numeric identity predicate—for each enumerated gate.

16. NOT RESOLVED — AMEND-BEFORE-FREEZE. Protocol sections: §4 M5 and §5.2 D3. The secondary definitions have improved, but they are not yet uniquely implementable. For M5, the standing population, weighting and across-cutoff aggregation of "remaining career total points" are not fully stated. For D3, "contribution(i | core)" is not defined mathematically. The text does not specify: whether the removal model is jointly refit; the exact loss difference and sign; whether the contribution is paired; how per-lens contributions aggregate; or what uncertainty calculation accompanies it. Consequently D3 cannot yet be the mechanical AUD-007 instrument claimed in §1. What resolves it: Add exact formulas and refit/aggregation rules for M5 standing and D3 contribution, with deterministic fixtures.

17. RESOLVED — environment and panel-version comparability. The environment now pins per protocol version, and any change forces complete official-result rescoring before further rounds. Scheduled extensions create a panel-version boundary and require current C0, C3, C2 and C1R reruns before new comparisons.

C. Disposition tally
- Resolved: 1, 8, 9, 12, 17 — 5
- Original route resolved but new issue introduced: 3, 10 — 2
- Not resolved: 2, 4, 5, 6, 7, 11, 13, 14, 15, 16 — 10
The unresolved set includes eight matters assessed here as blockers: 2, 4, 5, 6, 7, 10, 11, 13 and 15.

VERDICT: FAIL
The §11 compliance map now passes F1. The protocol as a whole does not yet pass F3.
The remaining blockers are not merely implementation polish. They affect: whether early-fold tuning is origin-safe; whether the declared multiplicity regime controls the stated error rate; whether M4 and M8 are uniquely and coherently calculated; whether the bootstrap supports the admission claims; whether the benchmark and ceiling are identical across conforming implementations; whether TALL-DEV can be treated as protected when unmeasured; and whether binding Rulebook gates can issue a unique verdict.
Accordingly, v0.5 should not proceed to F4 freeze in its present form. The owner retains the freeze decision.

F3 cold review seat — read-only verification; no repository writes and no freeze decision.
