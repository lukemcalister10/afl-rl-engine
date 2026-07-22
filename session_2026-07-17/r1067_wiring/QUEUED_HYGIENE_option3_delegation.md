# QUEUED HYGIENE — option-3 delegation of the prod_floor duplicate loop (NOT this build)

**Registered:** 2026-07-17 (R106.7 floor-half build, owner Option-2 adjudication condition 5).
**Status:** QUEUED — do NOT execute in this build.

## What
`_merged_recover.py::_prod_floor_w4` is a hand-duplicated copy of `rl_model.prod_floor`'s floor loop, kept for the
proven-player W4 forward path. As of R106.7 both copies carry the identical §1b k==0 split (cross-referenced with a
duplicate-loop hazard comment at both sites + the `v_at_peak` consumer). Any future edit to the floor's k==0 term
must touch BOTH or the shipped board and the base path diverge silently.

## The refactor (option 3)
Collapse the duplicate: make `_prod_floor_w4` delegate to `rl_model.prod_floor` for REPL/§1b bar resolution
(passing only the W4 weight `_w4_W(k,ctx)` as the per-k weight), so there is ONE floor loop and ONE §1b site.

## Binding requirement
A **determinism proof** is mandatory before this ships: the refactor must reproduce the shipped board byte-for-byte
(same board md5) across the CPU/BLAS fleet the determinism note guards — the W4 weight path and the base path fold
identically only if the `_w4_W`/`(1+d)**k`/`*21` ordering is preserved. Ship only against a committed A1-style
native==forced-Haswell==forced-Prescott board-md5 equality, exactly as the 2026-07-14 determinism fix required.

## Why not now
Out of scope for R106.7 (the owner ruled Option 2 = wire the split into both copies for this build). The refactor is
a structural change to an otherwise-OUT Leg-B/W4 module and carries its own proof burden; bundling it here would
mix a value-affecting wiring with a byte-exact refactor and muddy the A/B chain.
