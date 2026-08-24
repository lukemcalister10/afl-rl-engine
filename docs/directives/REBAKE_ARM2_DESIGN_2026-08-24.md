# REBAKE WEEK · ARM 2 — THE DESIGN ARM · directive 2026-08-24

**Charter:** register v831 (all six decisions ruled, owner words verbatim), v833 (binding handover),
v834 (ARM 1 landed and verified — build on it). Studies: `docs/proposals/rebake_study_B/DESIGN_STUDY_B.md`
(the construction of record), `rebake_study_A/` (the baseline tables), `REBAKE_COMPARISON_2026-08-21.md`.

**Base your branch on `rebake/arm1-store-alone` (tip `4124fd6`)** — it carries the refit entry
points, the declared switches (RL_CM_PKL), the loader HALT, and the in-repo stamp machinery. Reuse,
don't refork.

## THE RULED CONSTRUCTION (no design decisions are open — execute and measure)

1. **Exact monotone constraint** (owner: "Exact it is"): the study B §2.3 construction — the
   ~4-line `GradOnlyPinball(PinballLoss)` subclass with `differentiable=True`, defeating sklearn
   1.8.0's leaf line search so `monotonic_cst` is EXACT under quantile loss, on
   `HistGradientBoostingRegressor`. Zero negative level steps FROM THE FIT (study B proved 0 in
   1,004,720 twice). Ships with the HALTING private-contract self-test (FB4): the bake asserts the
   subclass contract against the pinned sklearn before any fit, and HALTs if the internals moved.
2. **Hyperparameters re-selected OUT OF SAMPLE** on a grid DECLARED in the prereg before the run
   (study B's selected `lr=1.0, max_iter=800, max_depth=4, min_samples_leaf=25` is the prior, not
   the answer). The incumbent's settings measurably do not transfer.
3. **The age hill** (owner's peak challenge recorded): features `u = max(0, a* − age)`,
   `v = max(0, age − a*)`, both constrained −1 — single-peakedness structural. `a*` SELECTED OUT OF
   SAMPLE over a declared grid that includes 21, 22, 23, 24; report the numbers for the owner's
   prior (~23) and the study's fitted peak (~21.5) side by side.
4. **Mild recency weighting** on training rows: window-anchored per study B M-60, half-life
   selected OOS on a declared 10–16y grid.
5. **T1 applied** (as ARM 1); attribute its share.
6. **Scope:** cm_400 + q97m + peak_model_v4 (+pvc_snapshot co-emit). `v0surf` UNTOUCHED.
   **bust_prior:** train the peak model on the FROZEN table for now — the rederivation ruling is
   with the owner; expect ONE cheap refit pass when the table and the final store are settled (the
   Graham store edit lands separately; fits are minutes, the entry points make this one command).
7. **The ratchet retires** — forced by M-52 (`_o44_xs()` walks `estimators_`, which the new
   estimator lacks). Deliver the MUST-MOVE proof: with the exact-constrained artifacts loaded, the
   read-site ratchet finds nothing to fix on any row (a measured no-op), then the retirement diff.
   O33 retires only if asc==1 re-derives; otherwise it stays.

## BATTERY (every verdict with value and margin)

- **V3 census at RAW must read ZERO** — this is the arm's whole point; the read-site census too.
- B2 / B6 / G-Y0 · pinball vs the PAR-centred zero point **3.9788** (filed at ARM 1) and vs the
  incumbent · law-9 mint measured and REPORTED (waived as gate, v830) · P12 no-arb reading ·
  fit-twice · stamps in-repo · Guard-5-coherent candidate root (ARM 1's make_candidate_root pattern).
- **Movers TWICE:** vs the live board `6fd0f7de` AND vs ARM 1's candidate `02a554b5` — the second
  diff is the pure design effect, cleanly separated from staleness, and it is the owner's deciding
  table.

## PRACTICES (breach = abort)

Prereg FIRST (P9) with predictions + falsifiers. Candidate paths only — live pickles, pins,
`/home/claude/*` byte-untouched. Isolated worktree, explicit-path commits, configured identity,
never `docs/register/`, no pushes — the supervisor reviews, verifies by re-running deciding
figures, and lands nothing without the owner's word. Any new switch: declared, one site, default
shipped. Assume you find something not on this list; report it, never absorb it.

## RETURN
Branch + tip; prereg commit; per-artifact hashes/rows/settings AS MEASURED with the OOS selection
tables (every grid point's score); a* selection table; both movers summaries; full battery with
margins; the ratchet must-move proof; T1 share; anything off-list.
