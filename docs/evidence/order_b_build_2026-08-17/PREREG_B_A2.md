# PREREG AMENDMENT B-A2 — the measured-bracket step (pushed BEFORE the run it governs)

Where B-A1 stands: its one-iteration budget is SPENT, and the two measured builds bracket the ruled
target from opposite sides —

| built point (tall survivor B; * = called) | 27 | 28 | 29 | 30 | 31 | full-30 |
|---|---|---|---|---|---|---|
| iter-1 (ρ0=.050, g=.0125), s\*=1.3451 | 0.984 | 0.902 | 0.868 | 1.096 | 0.907 | 1.158 |
| iter-2 (ρ0=.025, g=.010), s\*=1.1909 | 1.084 | 1.064 | 1.040 | 1.264 | 1.032 | **1.335\*** |

iter-1 keeps every over-mark call dead but leaves 28/29/31 under the ~0.95 floor; iter-2 clears the
floor everywhere but RESURRECTS the full-view 30-cell over-mark call (1.335, CI-lo > 1) — the hard
ruled constraint. The offline replica transfer proved unstable across s\* re-derivations (missed −0.07
then +0.07); the MEASURED pair is now the better instrument.

## The rule (fixed before running)

- ONE point on the measured segment: parameters (ρ0, g) = iter-1 + t·(iter-2 − iter-1) with
  **t = 0.55**, i.e. **(ρ0 = 0.03625, g = 0.011125)**, chosen from linear interpolation of the
  MEASURED built cells: floor t-window [0.448 (cell 29), 0.69 (full-30 ≤ ~1.28)] — 0.55 is its
  midpoint, balancing the 29-floor margin against the full-30 call margin. Predicted built cells
  ≈ 27: 1.04 · 28: 0.99 · 29: 0.96 · 30: 1.19 (full 1.26) · 31: 0.98.
- s\* re-derived by the standing fixed-point discipline (<0.2% anchor gate).
- Verify by build + emit + W5. PASS = every tall survivor cell ≥ 0.935 (floor 0.945 − the 0.010
  verify tolerance) AND no over-mark call in EITHER view resurrected. FAIL on either bound ⇒ REVERT
  the wired point to iter-1 (ρ0=.050, g=.0125, s\*=1.3451 — the measured point with all calls dead),
  and HALT to the owner with the full trade-off (the bracket table above plus the failed midpoint).
  No further fitting either way.

## Re-run set (on whichever point ships)

Identity rails (both configs, current tree) · determinism ×2 · day-0 emit guard · standing two-sided
suite + entry-year control · ladder-leg + taper-leg ledger + both pages · packet delta.
