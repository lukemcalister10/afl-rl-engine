# THE BLIND COMPARISON — REBAKE DESIGN STUDIES A AND B

**For Luke. Written by the supervisor, 2026-08-21, immediately after reading study A for the first
time.** Protocol of record (your words): *"they commission their own agent without seeing what you
commissioned or the result of your agent, and then once done, compares the two."* Study A
(`docs/proposals/rebake_study_A/`) was commissioned by the pre-compaction supervisor; study B
(`docs/proposals/rebake_study_B/`) was commissioned post-compaction from your verbatim design words
only, with the A directory barred until B filed. B's independence declaration is in its header; the
one leak either direction was a list of A's *filenames* in one of B's grep results, excluded and
unopened. Agreement below = confidence. Divergence = the finding.

---

## 1 · WHERE THEY AGREE — independently, often by different methods

These were measured twice, blind, and landed together. They can be treated as settled.

1. **Deleting pool careers from training loses everywhere, including on the players it was meant to
   protect.** A: +4.45% overall, +13.8% on rookies, +8.1% on deep nationals, and it wrecks the
   band's honest lower tail. B: +6.4% overall, +21% on pool rows, +0.5% even on nationals, measured
   out of sample after B struck its own earlier in-sample number that said otherwise. **Your
   instinct is confirmed twice over; the "pool contamination" register item should close as
   not-a-defect.**
2. **The library's monotonic constraint is NOT exact under quantile loss — the subtlest finding in
   either study, found twice.** A measured it in isolation (185 violations in 240,000 on synthetic
   data, ~1.8% of steps on the real fit). B independently found the same numbers AND the mechanism,
   read out of the pinned sklearn source: quantile loss triggers a post-fit leaf adjustment that
   overwrites the constrained values. Anyone who had shipped the "obvious" fix and deleted the
   ratchet would have shipped a board still violating law 3 on most rows, invisibly. Two blind
   seats both refusing to let that happen is the strongest confidence result of the exercise.
3. **The estimator must change.** The current model class cannot accept a monotonic constraint at
   all — B proved the prereg's declared FIX 1 raises a TypeError as written; A's re-posing of D1
   says the same thing from the other side. Not optional modernisation; the precondition.
4. **The shipped artifacts are stale and both studies dated them to the same store epoch
   (2026-07-15→17) by different forensic methods** — A from the quantile constants stored at each
   forest's root, B from the training-row counts stored in the trees. Both found the same
   consequences baked in: ~300 players taught a guessed age (B: 14.18% of training rows, 38.9% of
   the guesses wrong by ≥1 year), the pre-migration position semantics, ~700 pick moves, and your
   T1 fabricated-zeros rule NOT applied (the artifact predates your word).
5. **The provenance stamp is the cheapest big win, and both found the identical embarrassing
   detail:** the sibling model's build script already writes exactly the right stamp — to a
   directory outside the repository, where nothing can read or assert it. Two output paths fix a
   problem that cost both studies most of their forensic budget.
6. **The sibling models are stale for the same reasons and should join the scope** (q97m,
   peak_model_v4 — B adds that peak_model's own declared falsifier, the guessed-age row count that
   "must fall by exactly the courier's count", has never been taken; A adds pvc_snapshot and
   bust_prior_table to the stale list).
7. **The band's loader still carries the silent-refit-on-cache-miss fallback** its two siblings had
   surgically removed — both name the same one-line fix riding the rebake.
8. **Your unification instinct is already true inside the model.** Both measured that pool and
   national careers train together and the model can separate the arms when it needs to (every pool
   entrant sits at one point on the pick axis). A fitted your unification as explicit features:
   neutral at best, and the variant needing law 4 amended actively hurts — **so law 4 does NOT need
   amending, per both.** B: an explicit pool flag is an exact no-op today, defensible only as
   insurance.
9. **Gentle weighting toward relevant data: small, real, arbitrary.** A weighted by population
   (+best pool calibration), B by recency (+0.18% at a 16-year half-life, after twice getting the
   anchoring wrong and saying so). Both: take it only as a declared dial, never as a derived
   constant; both: deletion of old data always loses.
10. **The population-wide level census must become a standing gate.** Both note the shipped defect
    (about a quarter of all level steps descending) lived behind a proof three archetype rows wide.
    B priced the full census at ~17 minutes; cheap enough to stand at every bake.
11. **Land the rebake in attributable arms, store-alone refit first** — the one arm with no design
    content, whose mover table honestly measures how stale the estate became.

## 2 · WHERE THEY DIVERGE — the findings

**F1 — THE CENTRAL SPLIT: what reaches zero, and what happens to the ratchet.**
- **A recommends:** the stock approximate constraint (~98% of the defect gone at the fit) **plus
  keeping your ratchet at the read site permanently** for the last ~2% — measuring that on a
  constrained surface the ratchet's cost and mint collapse to ~0.004%, making the conservation
  question nearly vanish.
- **B recommends:** a four-line construction that disables the leaf adjustment so the constraint is
  **exact** — 0 negative steps in 1,004,720, proven twice on two different fits, at *better*
  out-of-sample accuracy than the incumbent (3.9213 vs 3.9267, with honestly re-selected
  settings) — and retiring the ratchet with the prereg's must-move proof. Cost: it subclasses a
  private sklearn internal, mitigated by a HALTing bake self-test plus the already-pinned library.
- **The decisive cross-check, verified by the supervisor at `_merged_recover.py:488`:** the
  ratchet's knot-reader walks `estimators_`, an attribute the new estimator class does not have.
  **A's recommended combination — new estimator + ratchet retained — does not run as written; it
  dies at load.** Keeping any read-site smoother through the estimator swap means rewriting it
  against the new estimator's *own* private internals. So both roads carry an internal-API
  dependency; B's is four lines with a self-test, A's alternative is a rewrite of the whole knot
  walker. A did not see this; B measured it (its M-52) and B's larger design survives the check.

**F2 — cm_400's fitting store: A says identified exactly; B says unidentifiable.** A's five root
constants match the 07-15 epoch store at 13,225 rows "exactly and only". B's row count read from
the same pickle says 13,226 — and no committed store under 32 setting combinations produces 13,226.
Both facts can be true (one extra row that leaves six quantiles unchanged), but the one-row
discrepancy is unresolved, either study's method alone would have overclaimed or underclaimed, and
the reconciliation is a small named task for the bake seat. Both studies' remedy is identical and
makes the question obsolete: the stamp.

**F3 — A measured something B never looked at: calibration.** The band's floor sits 4–5 percentage
points too high in *every* design — the "10th percentile" leg is really a ~14th percentile — and
the three lower legs carry 54% of the band's weight. A calls it a larger, more systematic error
than the staircase, currently nobody's item. It should become a named rebake-week agenda item with
its own measurement, whatever else is decided.

**F4 — B measured things A never looked at:** the age shape (single-peaked, not monotone — with a
reparameterisation that makes single-peakedness structural for 100% of rows at 0.10% cost, versus
a naive age constraint that would wrong exactly the young players); the fact that q97m and cm_400
were fitted from two *different* row populations (a coherence wrinkle the bake should unify or
justify); out-of-sample hyperparameter selection (A deliberately held settings fixed; B showed the
incumbent's settings do not transfer and re-derived them with the rule declared first); and the
release manifest's blindness to all five fitted artifacts.

## 3 · THE SUPERVISOR'S RECOMMENDATION AFTER READING BOTH

Take **B's estimator core** (the exact construction, with its HALTing private-contract self-test
and the full-population census as a permanent gate V3) — because both studies agree the bar is
zero, only the exact arm meets it from the fit, it costs no measured accuracy, and F1 shows the
ratchet cannot ride through the swap anyway. Fold in **A's unique contributions**: the calibration
floor as a named agenda item; the standing pinball monitor with A's tables as its zero point; the
wider stale-artifact scope (bust_prior_table, pvc_snapshot join the census even if they don't all
refit in this act). Keep the shared non-negotiables both demand: stamps in-repo beside every pickle
and asserted at boot; T1 applied; the loader HALT; one committed refit entry point; arm-by-arm
landing with the store-alone arm shown to you first.

## 4 · WHAT ONLY YOU CAN DECIDE (distilled from both studies' lists)

1. **The exactness route (B's D1, reshaped by F1):** (a) exact arm, private dependency,
   self-test-guarded, ratchet retired — *recommended*; (b) approximate constraint + a rewritten
   read-site smoother — more kept code, same class of internal dependency; there is no third road
   that keeps the current ratchet unchanged.
2. **Age (B's D2):** no constraint / naive downward / the peak shape (structural single-peakedness,
   one chosen constant). All within 0.19%; a guarantees question, not an accuracy one.
3. **Recency weighting (B's D3 / A's design d):** worth ~0.2%, costs one arbitrary constant. Take
   as a declared dial or leave.
4. **Conservation (both studies' D5/D7):** the rebake will mint, as the ratchet already does under
   your recorded waiver. Re-waive for the baked version, demand it lands conserved, or build the
   standalone value-removal lever you said you'd prefer — settled before the bake, because it
   defines "success".
5. **Scope (D6):** band + ceiling only, or the full stale set (peak_model, pvc_snapshot,
   bust_prior_table) in the same week.
6. **Sequencing (D7):** both studies say store-alone arm first, shown to you alone. Confirm or
   override.

Neither study needs law 4 amended, neither found a case for deleting any data, and both retire the
staircase scaffolding through a proof rather than a promise.
