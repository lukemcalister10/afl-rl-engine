# F3 COLD REVIEW — REFEREE PROTOCOL DRAFT v0.3 · filed by the supervisor pen 2026-07-24
Reviewer: fresh GPT seat (owner pick, register v395) · cold: filed documents only, no seat rationale.
Verdict: **FAIL** — 8 BLOCKER + 9 AMEND-BEFORE-FREEZE findings; F1 unclosed (one incorrect §11 citation).
Routing: findings → design seat for a numbered response (accept+fix or rebut) and protocol v0.4 →
same F3 seat verifies resolutions → F1 re-verification → owner F4 word. Verbatim review follows.

---

ITEM 410 — F3 COLD REVIEW OF REFEREE PROTOCOL DRAFT v0.3

Seat: F3 cold review
Scope: F1 compliance-map verification and adversarial specification review
Authority reviewed: REFEREE_PROTOCOL.md, ITEM_409_EVIDENCE_MEMO.md, RULEBOOK.md, acceptance_v2_0.json, and the OPEN_ITEMS_REGISTER.md header containing sealed owner reads v390–v392
Disposition: Review only. No freeze or adoption decision is made here.

Part 1 — F1 compliance-map verification

The register's sealed reads require mechanism-class admission with fresh fold tuning and bounded predeclared variants under v391; and continuing joint tuning, backward passes, interaction bundles and ceiling-guided hunting under v392.

§11 compliance-map claim → Result
- v391 — mechanism class is the unit of admission → §7.1 — VERIFIED. §7.1 says exactly that.
- v391 — fresh train-fold tuning, out-of-fold scoring, not frozen incumbent settings → §§2.3, 6, 7.4 — VERIFIED. The cited sections collectively encode fold-contained fitting, C0/C1R refitting and joint out-of-fold evaluation.
- v391 — shapes may generalise from constants to curves → §7.1 — VERIFIED.
- v391 — rejection is only "not at any tested construction," with tested space recorded → §7.6 — VERIFIED.
- v391 — variants predeclared before scoring under a budget → §7.2 — VERIFIED.
- v392 — admitted ingredients retune jointly at subsequent admissions → §§7.4, 7.7 — VERIFIED.
- v392 — forward and backward/joint-refit passes → §7.7 — NOT VERIFIED AS CITED. §7.7 encodes only the backward pass. The forward step is in §7.4.
- v392 — interaction bundles have a mechanism story and are declared/tested as units → §7.3 — VERIFIED.
- v392 — ceiling gap is sliced by lens and guides interaction hunting → §§8.3, 7.3 — VERIFIED.
- Owner peak-horizon read — M8, TALL-DEV, admission door and always-mapped row → §§4, 5.1, 7.5, 8.3 — VERIFIED.

The protocol therefore encodes the substance of all sealed reads, but F1 is not yet satisfied line by line because one §11 claim is not true at its cited section. Section 10 expressly makes completed line-by-line verification a freeze precondition.

Part 2 — Numbered findings

1. AMEND-BEFORE-FREEZE — False/incomplete §11 citation
Protocol section: §11, v392 second compliance-map clause.
The map states that "forward AND periodic backward/joint-refit passes" are encoded at §7.7. Section 7.7 contains the backward pass only; the forward step is §7.4. The substantive rule exists, but F1 requires every cited encoding claim to be true as cited.
Resolution required: Change the compliance-map citation to §§7.4 and 7.7, then repeat F1 verification.

2. BLOCKER — The inner-validation rule cannot remain origin-safe for the long-horizon heads as written
Protocol section: §2.3.
For outer cutoff t, the "final three train seasons" are assigned as inner validation. M4 needs up to three post-cutoff seasons and M8 needs six. Validation cells close to t therefore have labels extending beyond the outer cutoff. An implementer must either: (1) read outcomes after t, causing leakage; (2) use incomplete target windows; or (3) silently choose earlier validation cutoffs not specified by the protocol.
The ambiguity is especially material where one model tunes several heads with different horizons.
Resolution required: Define target-safe inner-fold eligibility separately for each horizon, requiring every inner-validation label to be fully observable by the outer cutoff, and define how joint multi-head tuning handles the resulting unequal eligible sets.

3. BLOCKER — Outer test folds are used for exploration, selection and adjudication
Protocol sections: §§7.2, 7.4, 7.9 and 8.3.
The declaration seal applies before an "official" test-fold score, while §7.4 expressly permits approximate screening. Nothing prohibits unlimited unofficial screening against the outer-fold outcomes before sealing the selected variant.
Independently, §8.3 publishes outer-fold C3−C2 gaps and feature-attribution guidance, then §7.3 permits those results to determine bundles tested in the next round. The same outcomes are therefore deliberately used to generate hypotheses and later adjudicate those hypotheses.
Even perfectly chronological predictions become adaptively overfit when the same historical outcomes are repeatedly queried. The final C2 score is consequently not an untouched out-of-sample estimate of the selected program.
Resolution required: State that no screening, map interpretation or candidate construction may inspect adjudication-fold outcomes before the candidate's eligibility is fixed, and provide untouched adjudication evidence for the adaptively selected final core—or otherwise specify a valid inference method for the complete adaptive selection procedure.

4. BLOCKER — The declared budgets do not cap multiplicity
Protocol sections: §§7.2, 7.6–7.9.
The limits are per class and per round. The protocol places no limit on: the number of mechanism classes; the number of rounds; repeated re-entry of the same mechanism; class fragmentation into several narrowly named classes; approximate screening attempts; slice and slice-pair comparisons; backward-removal tests; or hypotheses generated from the interaction map.
A motivated seat can therefore obtain effectively unlimited attempts while remaining within "five variants per class per round." Publishing the number of attempts is honesty, but it is not statistical control. A two-sided CI90 exclusion rule permits roughly a 10% false-resolution rate per null comparison before adaptive selection and dependence are considered.
Resolution required: Define the complete experiment family and a cumulative control that covers all variants, classes, bundles, rounds, screening accesses, map-derived hypotheses and backward tests. Mechanism-class identity also needs an anti-fragmentation rule.

5. BLOCKER — The headline standing metric is not mathematically defined
Protocol sections: §4 M2/M4 and §7.5.
The protocol defines realized standing as a percentile of realized production, but does not define the contestant's predicted standing. Material choices remain open: rank predictions directly within each cutoff, or map predicted production through a reference distribution; include or exclude zero-game cells from the percentile denominator; weighted or unweighted M4—the "same weighting" wording appears for M2 but not M4; tie convention and percentile formula; treatment of missing predictions; pooling across cutoffs before or after calculating errors; and whether bootstrap resamples recompute percentile targets.
These choices can yield different admissions on the protocol's binding headline.
Resolution required: Freeze complete formulas for predicted and realized standing, eligibility, weights, ties, cutoff aggregation and bootstrap treatment, with fixed test fixtures producing exact expected values.

6. BLOCKER — M8 is ambiguous and can reward incoherent peak forecasts
Protocol sections: §4 M8 and §7.5.
Contestants must emit future distributions, but predicted peak is defined as the maximum of "predicted season means." It is not stated whether those means are conditional on playing or include the zero-games branch. More fundamentally, the maximum of six marginal means is not the predicted mean of the maximum under a joint future distribution.
M8 excludes all cells with no games across the window and has no binding multi-year attrition score. M6 covers only Y+1, while D2 is non-binding. A contestant can therefore create an aggressive remote-season peak without bearing a corresponding binding penalty for the probability of reaching that season.
Because M8 is an admission door, this is not merely a reporting imperfection.
Resolution required: Define the exact peak functional from the contestant's future distribution, including survival conditioning, dependence between seasons and aggregation of the zero-games branch. The binding guardrail must cover the same survival horizon used by the admission door, or the protocol must expressly limit what an M8 admission establishes.

7. BLOCKER — The bootstrap specification is insufficient for an admission gate
Protocol section: §4, "Uncertainty."
"Player-clustered bootstrap, B=2,000, seeded" leaves unresolved: paired versus independent resampling of contestant losses; percentile, basic, studentised or another CI construction; resampling globally or within cutoff; handling players absent from some folds; recomputation of standings and weights; treatment of empty slices; whether model fitting is repeated; whether one seed or a seed derivation schedule applies; and how shared cutoff/season shocks are represented.
Player clustering captures repeated observations for a player but not the common shocks shared by all players in a season. The effective evidence for future-season generalisation includes only a small number of cutoff years, while the overlapping target windows are highly dependent.
Resolution required: Freeze the paired statistic and complete resampling algorithm and demonstrate that its uncertainty coverage is appropriate for dependence across both players and cutoff seasons.

8. BLOCKER — The incumbent's leakage does not support an automatic "a fortiori" direction
Protocol section: §3.2.
The rule declares every result against C1 to be a fortiori valid. Leakage is not guaranteed to improve a model on every metric, fold or slice; a leaked variable or full-history parameter can also degrade a particular comparison.
The evidence memo establishes that the full-history-fitted incumbent lost on the measured Y+1 race and describes those parameters as flattering it there. It does not prove that every listed leak favours C1 on M2, M4, M6, M8, all slices and every future panel extension.
Resolution required: Treat C1 as a contaminated descriptive comparator. Directional "conservative against C1" claims may be made only where the direction of the leakage advantage has itself been established for the exact statistic being interpreted.

9. AMEND-BEFORE-FREEZE — The generic origin-safety fence is not mechanically enforceable
Protocol sections: §§2.1–2.4 and 3.1.
The three named regression probes cover known existing leaks, but "including indirect routes" has no corresponding machine-checkable specification. Uncovered routes include: target-derived feature engineering; preprocessing or imputation fitted across outer-test cells; joins to present-day aggregates that contain historical information; position or availability fields revised retrospectively; feature selection informed by outer-fold results; cohort definitions using post-cutoff facts; and cross-head tuning that sees labels outside the permitted horizon.
A panel MD5 proves repeatability of whatever the builder produced; it does not prove that the panel obeys the as-of rule.
Resolution required: Require a per-feature and per-transform provenance manifest, cutoff assertions for every join and aggregate, and negative controls that deliberately introduce representative direct and indirect leaks and must HALT.

10. BLOCKER — C0 conflicts with the protocol's own application of L-SMOOTH
Protocol sections: §5.1, §6 C0 and §7.1.
Section 5.1 says age bands are reporting bins only and estimator structure remains smooth. C0 nevertheless contains a four-entry age-drift table. C0 is not merely a disposable comparator: §6 says it is the governed core's seed.
The governing Rulebook prohibits wide-bin jumps and discontinuities across age, evidence and position. The acceptance twin also marks L-SMOOTH as binding.
Resolution required: Reconcile C0's step-table construction with L-SMOOTH before freeze, or obtain an explicit owner-worded governing-law amendment or exemption. The protocol itself cannot silently create one.

11. BLOCKER — The "ceiling" and interaction map are adjustable enough to change the stopping result
Protocol sections: §§8.1–8.4 and 7.8.
C3 may be a gradient-boosted tree "or declared equivalent." The protocol does not freeze its learner, objective, capacity, hyperparameter ranges, feature encoding, missing-data treatment or early-stopping rule. A weak C3 reduces the apparent prize and the number of resolved interaction rows; an overfit or unstable C3 expands them.
The minimum cell count for slice-pairs is also merely "declared," with no value or declaration timing. It can be set high to suppress rows or low to generate noisy resolved rows. Since the stopping rule depends on whether all resolved rows have been tested, these choices can alter when the race stops.
Resolution required: Freeze the complete C3 specification and the interaction-map row universe, support minimum and declaration timing. Define denominator handling where the purported ceiling does not beat C0 or produces a near-zero gap.

12. AMEND-BEFORE-FREEZE — Candidate selection order is undefined
Protocol sections: §§7.2–7.7.
The protocol does not state: which variant represents a mechanism class if several pass; how ties are resolved; whether all candidates in a round are compared with the round-start core or with an evolving core; the order when several candidates qualify; whether later candidates must be rescored after an earlier admission; what happens when bundles overlap with admitted individual classes; or what constitutes an "ingredient" when removing part of an admitted bundle.
Different reasonable implementations produce different cores.
Resolution required: Add a deterministic state-transition and ordering rule covering variant selection, simultaneous passers, rescoring, ties, overlapping bundles and backward removal units.

13. AMEND-BEFORE-FREEZE — TALL-DEV and other slices are not frozen sufficiently
Protocol sections: §5.1 and §8.3.
The position vocabulary is deferred to a later harness claims note. The protocol does not freeze the raw-position mapping, treatment of hybrids or missing positions, minimum sample support, or pooling rule.
That permits materially different TALL-DEV populations, even though TALL-DEV is both an admission guardrail and an always-mapped owner-protected row. It also conflicts with the Rulebook requirement that thin slices be deliberately pooled and declared, because no support criterion says when a slice is reported, pooled or UNMEASURED.
Resolution required: Freeze the position mapping and missing/hybrid rules before any score access, together with objective support and pooling thresholds for every slice.

14. AMEND-BEFORE-FREEZE — The stopping test can count stale interaction work
Protocol section: §7.8.
The map recomputes as C2 evolves, but the stopping rule only requires that each resolved row have "at least one" tested bundle against it. It does not say whether that test must have been performed against the current C2 and current map version.
A bundle tested against an earlier core can therefore potentially discharge a row that later reappears under materially different residual structure. Conversely, a round with no resolved rows satisfies the row condition vacuously.
Resolution required: Define row identity and freshness, whether old tests survive a C2 change, and the behaviour when no row resolves despite a materially uncertain ceiling gap.

15. AMEND-BEFORE-FREEZE — Several "structural gates" are assertions rather than checks
Protocol sections: §§7.1, 7.5 and 9.3.
REF-RECENCY has a stated monotonic predicate, but the following do not have complete mechanical predicates: "weight-don't-gate"; identical upside/downside machinery; smoothness across age, evidence and position; when a learned asymmetry violates L-SYMMETRY; what measured floor applies to age fade; and what constitutes all structural gates being "green."
The Rulebook requires measured values and margins, not merely pass/fail, while the acceptance twin marks SILENCE-IS-RED, L-SMOOTH and L-SYMMETRY binding.
Resolution required: Enumerate every applicable structural gate, its exact measured predicate, threshold, failure output and scorecard margin.

16. AMEND-BEFORE-FREEZE — Secondary metrics and diagnostics permit incompatible implementations
Protocol sections: §4 M5/M6 and §5.2.
Examples include: M5 does not define "cohort," whether panel end includes the live 2026 season, or how two years without a game distinguish retirement from temporary absence; "censored cells excluded and counted" does not define the censoring estimator or denominator; M6 does not define probability clipping, treatment of exact zero/one predictions or reliability-curve bins; D1 imports an unspecified pm_pct construction; D2 does not identify a scored statistic; and D3 does not define "joint-vs-marginal contribution," so it could mean ablation, coefficient comparison, permutation importance or another incompatible calculation.
D3 therefore cannot yet serve as a mechanical AUD-007 instrument despite §1's claim that it unblocks AUD-007.
Resolution required: Supply exact formulas, eligibility rules and deterministic fixtures for M5, M6 and D1–D3.

17. AMEND-BEFORE-FREEZE — Cross-round and panel-extension comparability is not secured
Protocol sections: §§2.2, 8.4, 9.4 and 10.
The environment is pinned only within a round, although admissions compare an evolving core across rounds. "Remeasurement to reconcile" does not specify which contestants are rerun or which result controls.
Similarly, a completed-season panel extension is declared not to be an amendment, but it changes folds, targets, sample composition, CIs, the ceiling and interaction rows. The protocol does not require the existing race and admissions to be rerun on the extended panel before further selection.
Resolution required: Pin the adjudication environment for the full protocol version or require complete round-history rescoring after any environment change. Define a panel-version boundary and the exact rescoring consequences of scheduled extensions.

Verdict

FAIL

Draft v0.3 should not advance to the owner's F4 freeze word in its present form.

The formal F1 condition is unclosed because the §11 map has one incorrect citation. More importantly, the protocol's admission evidence can be adaptively mined through screening, interaction-map feedback and unlimited future rounds; its long-horizon inner validation is not origin-safe as specified; its central metrics and bootstrap are not uniquely implementable; and the ceiling, multiplicity regime and stopping conditions remain controllable by discretionary choices.

These are specification failures affecting whether an apparent admission represents genuine out-of-sample evidence. They cannot be treated as harmless harness details after freeze.

F3 cold review seat — filed-document review only; no repository writes and no freeze decision.
