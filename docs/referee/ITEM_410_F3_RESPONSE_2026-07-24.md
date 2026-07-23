# ITEM 410 — DESIGN SEAT RESPONSE TO F3 REVIEW OF PROTOCOL v0.3 · 2026-07-24
(Filed verbatim by the supervisor pen; protocol v0.5 filed beside it at docs/referee/REFEREE_PROTOCOL.md.)

Answers every finding by number per the owner's routing word; protocol v0.4 accompanies. Same F3
seat verifies these resolutions before F1 re-runs. Review read at main `4fe4c99`
(docs/referee/F3_REVIEW_v0_3.md, register v396). Resolution depth is governed by the sealed v390
priority — minimum sufficient rigor, no over-engineering — and two findings the owner named
(3, 10) are resolved as open owner dials with recommendations, not seat decisions.
Tally note, for the record: the review header says 8 BLOCKER + 9 AMEND; the body labels sum to
9 BLOCKER (2–8, 10, 11) + 8 AMEND (1, 9, 12–17). All 17 are answered; body labels are used below.

**1 · ACCEPT-AND-FIX.** The citation was wrong as written; the forward pass lives at §7.4.
§11 now cites §§7.4, 7.7. F1 re-verification is the F3 seat's to run.

**2 · ACCEPT-AND-FIX.** Correct and material: "final three train seasons" as inner validation
leaks post-cutoff labels for any horizon > 1. v0.4 §2.3 freezes per-head inner eligibility —
inner cutoff u is eligible for a head of horizon h only if u ≤ t − h, so every inner label is
fully observable by the outer cutoff; each head uses its three most recent eligible u; a
deterministic copy-from-nearest-fold fallback covers heads with no eligible u; joint multi-head
dials minimize the unweighted mean of per-head inner losses, each normalized by the current
core's inner loss on that head so units are comparable. No inner label ever crosses t.

**3 · ACCEPT — RESOLVED AS OWNER DIAL-6 (owner-named).** The finding is the deepest in the set
and the seat accepts all three parts: unlimited unofficial screening against outer outcomes,
map-feedback adjudicated on the outcomes that generated it, and no untouched final estimate.
Recommended regime, encoded in v0.4 as text-in-force pending the owner's word (§§2.2, 7.4, 7.12):
(i) screening of any kind touches INNER folds only — outer outcomes are readable solely by sealed
official runs and the map computation; (ii) the cutoffs split into a uniform SELECTION window
(2009–2019, every head) and untouched CONFIRMATION folds (2020 onward, per head's reach), read
once at race end for the fork report, with a one-shot batch per-ingredient ablation on them;
(iii) M8/M6W have no in-panel confirmation cutoffs, so peak-door admissions are labelled
PROVISIONAL–AWAITING-EXTENSION and confirm on genuinely future seasons as scheduled extensions
land. Adaptive reuse inside the selection window remains, deliberately — that is where selection
happens — and is controlled by the finding-4 regime plus the confirmation gate. The alternative
(no split; all cutoffs selectable; control by query budgets alone) buys selection power on the
five most recent seasons at the price of no untouched final number. The dial is the owner's.

**4 · ACCEPT-AND-FIX.** Publishing counts is honesty, not control — agreed. v0.4 defines the
complete per-round family and a cumulative regime (§§7.2, 7.5, 7.9, 7.12): family m_r = sealed
forward candidates + scheduled backward removals, enumerated in the ledger before scoring;
admission level α_r = 0.05/m_r one-sided — a Bonferroni tightening of the owner's ruled CI90
base, never a loosening; round cap R_MAX = 6 (owner-extendable by word); class lifetime cap of
3 raced rounds with fresh variants and a stated reason per re-entry; an anti-fragmentation rule —
class identity is the registered parameter-space signature, overlapping spaces must register as
variants of the existing class, every registration carries distinctness notes (REF-FRAG); the
screening ban (Dial-6) removes screening from the family entirely; and the untouched confirmation
gate backstops the whole race. One narrow rebuttal: slice-guardrail multiplicity is left
deliberately uncorrected because guardrails only veto — more uncorrected chances to veto make
admission strictly harder, which is conservative in the only direction that matters.

**5 · ACCEPT-AND-FIX.** Every listed ambiguity is real. v0.4 §4 freezes the full construction:
eligibility (≥1 realized game in window; zero-game cells belong to the survival heads); mid-rank
percentile formula pct = (rank_avg − 0.5)/N × 100; predicted standing = the same transform on the
contestant's conditional expected production, ranked within the same eligible population — ranks
against ranks, so common monotone level bias cancels; weights = realized games in window, on M2
and M4 alike; per-cutoff weighted MAE then an unweighted mean across cutoffs — one cutoff, one
vote; missing prediction ⇒ UNMEASURED at that cutoff, and an UNMEASURED binding metric blocks
admission outright; bootstrap resamples recompute eligibility, percentiles and weights inside
each resample. Appendix A supplies a five-cell worked fixture with the exact expected value
(6.6667), and REF-FIXTURE HALTs unless the harness reproduces it bit-exactly.

**6 · ACCEPT-IN-PART, WITH ONE REBUTTAL.** Accepted and fixed: the peak functional is now exact —
predicted peak = max over window seasons of E[seasonal mean | plays that season], conditional
means only, dependence deliberately not demanded of contestants, and the protocol now states the
limit the reviewer offered: an M8 admission establishes ordering of conditional peaks among
realized survivors, nothing more. Accepted and fixed: the survival horizon of the door is now
covered by a BINDING score — new M6W, log-loss on P(≥1 game in the six-year window), sits in the
guardrail set for every admission, so a contestant cannot buy peak rank with survival fantasy at
zero cost. Also fixed: M8's binding form is STANDING ONLY; the max-of-means vs mean-of-max level
bias is common to all contestants and cancels in ranks; the level form is demoted to diagnostic.
The rebuttal, narrow: "can reward incoherent peak forecasts" overstates one path — cells with
zero realized games exit M8's population entirely, so aggressive peaks on non-survivors are
unscored in both directions and cannot manufacture gain; the exploitable surface was the
unpenalized survival probability itself, and M6W now binds exactly that.

**7 · ACCEPT-AND-FIX.** v0.4 §4 freezes the algorithm: paired player-clustered bootstrap — a
drawn player contributes all its cells at all cutoffs; both comparison sides computed on the
identical resample; paired gain distribution is the statistic; percentile CI; B = max(2000,
⌈50/α⌉) so small Bonferroni levels keep tail resolution; seed schedule 20260724 + 10,000·round +
registry-index; empty-slice resamples contribute NA with a ≥90% non-NA floor else UNMEASURED;
models are not refit inside resamples, a declared limit. Season common shocks: accepted that
player clustering cannot see them, and rather than invent a two-way bootstrap the panel affords
no power for, v0.4 adds a mechanical cutoff-robustness gate — admission requires a positive
point-estimate gain in ≥⅔ of the head's eligible selection cutoffs. Coverage is demonstrated,
not asserted: before round 1 the harness files a null-candidate calibration — ≥20 sealed null
perturbations of C0 through the identical pipeline; observed false-resolution rate must not
exceed nominal (REF-NULLCAL, HALT), repeated after any harness change.

**8 · ACCEPT-AND-FIX.** The reviewer is right that leakage direction is not uniform across
metrics, slices and future panels, and the memo's finding was Y+1-specific. §3.2 is recast: C1 is
a CONTAMINATED DESCRIPTIVE COMPARATOR — reported, labelled, adjudicating nothing; directional
"flattered and still lost" commentary is permitted only where the leak's advantage direction has
been separately established for the exact statistic in view, as the memo did at Y+1. The blanket
a fortiori rule is gone.

**9 · ACCEPT-AND-FIX.** A panel md5 proves repeatability, not legality — agreed. v0.4 §3.1 adds
REF-MANIFEST (every feature and transform ships a provenance row: source columns, maximum season
referenced as a function of t, fit scope; missing row HALTs; every join and aggregate carries a
season ≤ t assertion evaluated at panel build) and REF-CANARY (the harness ships ≥3 deliberate
as-of violations — a direct future stat, a full-history aggregate, a future-season position
join — and the probe suite must HALT on every one at every harness change; a passing canary is a
red build). The three named probes stay as the known-leak regression set.

**10 · ACCEPT — RESOLVED AS OWNER DIAL-7 (owner-named).** The conflict is real: §5.1 applies
L-SMOOTH to estimators while C0 seeds the governed core with a four-entry step table, and the
protocol cannot silently exempt itself from a binding law. Recommended resolution, encoded as
text-in-force pending the owner's word (§6): C0's drift term becomes a smooth low-df age curve —
≤4 effective df, free non-zero asymptote per REF-FADE-FLOOR, fit per fold — so the seed itself
obeys Law 3; the pack-2 step-table figures remain design evidence only, and nothing is lost
because the referee re-fits constants per fold regardless. The alternative preserved for the
owner: keep the literal step-table C0 raced as a comparator under an explicit owner-worded
Law-10 exemption, with a smoothed twin as the seed — continuity with the ITEM 409 verdict
artifact, at the cost of a standing law exemption. The dial is the owner's.

**11 · ACCEPT-AND-FIX.** v0.4 §8.1 freezes C3 completely: LightGBM, per-head objectives (L2
production, log-loss survival), the frozen panel manifest as features, a fixed small grid
(num_leaves {15,31,63} × lr {0.03,0.1} × min_child {20,50}) selected per fold on finding-2
inner-eligible validation, early stopping 50 on inner loss, native missing handling, declared
seed schedule, library version pinned at harness build. §8.3 freezes the row universe — all
single slices plus all slice-pairs at pooled selection support ≥ SUPPORT_MIN = 200 eligible
cells, set now, below-support rows UNMEASURED-THIN and pooled to parent — and §8.2 defines the
weak-ceiling case: if C3's pooled gain over C0 is unresolved, captured-share is UNMEASURED, the
resolved-row machinery suspends, stopping reduces to zero-admissions plus explicit owner
notification, because a weak ceiling is itself a finding, not a free pass.

**12 · ACCEPT-AND-FIX.** v0.4 §7.11 adds the deterministic state machine: all sealed candidates
score against the round-start core; class representative = best passing variant by (headline
point gain, then α-percentile lower bound, then earliest registry index); exactly ONE admission
per round by the same key; other passers flag PASSED-NOT-ADMITTED and auto-reseal next round —
no new budget consumed, counted in the next round's family; joint refit then produces the next
round-start core; the backward pass runs; bundles overlapping an admitted class re-declare as
their incremental complement; removal units are the registered admission units. No tie ever
resolves by seat discretion.

**13 · ACCEPT-AND-FIX.** v0.4 §5.1 freezes what the protocol can freeze now and seals the rest
before any score access: groups frozen here; the raw→group table is produced by one read-only
enumeration of the store's distinct position values at harness build and SEALED in the claims
note before any score access, unmapped values HALT (REF-VOCAB); hybrids join TALL-DEV if any
listed position maps to key-forward, key-back or ruck; missing position excludes from TALL-DEV
and lands in a counted MISSING-POS row; the universal support-and-pooling rule (SUPPORT_MIN =
200, pool to declared parent, stated on the scorecard) implements the rulebook's deliberate-
pooling requirement; where TALL-DEV itself is UNMEASURED-THIN the guardrail evaluates on its
parent (age ≤22 pooled) and the fallback is flagged — the owner-protected row can never
silently vanish or silently pass.

**14 · ACCEPT-AND-FIX.** v0.4 §7.8: row identity = (metric, slice tuple, panel version); the
stopping test evaluates on the CURRENT map against the CURRENT core, and a row is discharged
only by a bundle tested against the current or immediately-preceding core version — older tests
lapse; the vacuous case is closed by the diffuse-gap clause — if the pooled C3−C2 gap stays
resolved while no row resolves, stopping is still permitted but the fork report must state the
undischarged pooled gap explicitly for the owner's eyes.

**15 · ACCEPT-AND-FIX.** v0.4 §7.10 enumerates every structural gate with its predicate, margin
and failure output: REF-RECENCY (all weight deltas ≤ 0 over the years-back grid; margin = max
delta), REF-WDG and REF-SMOOTH-EST (max adjacent-grid step of any fitted 1-D shape or count
transform ≤ 5% of its fitted range; margin = largest step share), REF-SYMMETRY (no direction-
conditional branch on performance deltas; a registered asymmetric mechanism must be one shared
fitted curve evaluated identically everywhere, its fitted asymmetry reported with CI as the
margin — machinery symmetric, shape free), REF-FADE-FLOOR (age-curve families admit a free
non-zero asymptote; margin = fitted asymptote CI), plus REF-CEIL, the leak probes, REF-CANARY,
REF-FIXTURE, REF-NULLCAL, REF-SEAL, REF-JOINT, REF-FOLD, REF-VOCAB, REF-FRAG. "Green" = every
listed gate emits PASS with measured value and margin; a missing emission is a RED (Law 2).

**16 · ACCEPT-AND-FIX.** v0.4 freezes the secondaries: M5 — career complete := last game season
≤ last complete panel season − 2, comebacks reclassify at the next panel version and are
counted, eligible cutoffs need ≥90% cohort completeness, incomplete cells excluded and counted
with no censoring estimator, a declared minimalism for a metric that is never a door or
guardrail; M6/M6W — clip [1e-4, 1−1e-4], fixed decile reliability bins; D1 — defined inline
(within-band mid-rank percentiles for within-band error; band-mean standing error for
cross-band; the inline definition governs over pack archaeology); D2 — MAE on expected total
window points, Σ P(plays s)·E[games_s|plays]·E[mean_s|plays] vs realized, diagnostic; D3 —
frozen as ablation-based joint-vs-marginal contribution over pairs sharing declared registry
inputs, so it can serve as the mechanical AUD-007 instrument §1 claims.

**17 · ACCEPT-AND-FIX.** v0.4 §9.4/§9.6: the environment pins per PROTOCOL VERSION — image
digest and lockfile recorded at the first official run, stamped on every scorecard; any
environment change forces a full re-score of all official results before further rounds, the
re-scored ledger controls and prior numbers archive. A scheduled extension bumps the PANEL
VERSION; before any post-extension round, C0, C3, the current C2 and C1R re-run on the new
version; admissions stand as history under their panel version, forward comparisons and the
fork report cite current-version numbers only, and M8's confirmation additions land per §7.12.

**Disposition.** Fifteen findings accepted and fixed; one accepted in part with a narrow
rebuttal (6); two resolved as the owner dials the routing word named (3 → Dial-6, 10 → Dial-7),
each carrying recommended text in force pending the owner's word so verification can proceed on
concrete language. v0.4 accompanies; the same F3 seat verifies before F1 re-runs.

*Design seat, ITEM 410 · returns to the owner and the F3 seat; the pen files.*
