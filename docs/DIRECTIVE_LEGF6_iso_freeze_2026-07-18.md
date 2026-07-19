# DIRECTIVE — LEG F BUILD 6: FREEZE _iso_dec (THE RESIDUAL WEATHER) · seat 13 · 2026-07-18
### Owner-ruled "fix it" (item 381) on the item-380 diagnosis. WRITER build, the determinism
### closer. Freezes the one live fit q97m's 2026-07-14 freeze missed. The SAME pattern already
### owner-blessed for q97m. Tier-1-lite by construction (k=0 diff bounded to ≤1 row).

## GIT ENTRY (verbatim; item-334 law)
`git fetch origin main claude/legf5-entrant-layer-conservation-p4susl`; ls-remote must return
`15a9abd996f8f7426e98f173d83a0d600b966a3c` STRICT → checkout → `git checkout -b
claude/legf6-iso-freeze-<suffix>`. Docs on MAIN; never join lineages; this-session fetch; THREADS=1
(OPENBLAS/OMP/MKL/NUMEXPR). Entry stamps: store `968de0c7` · curve `56dd7a7b`/`89c14729` · q97m
`cfdc7321`.

## ★ THE CLEAN-INSTANCE PRECONDITION (MANDATORY — DO THIS FIRST, HALT IF IT FAILS) ★
Before freezing ANYTHING: build the balanced board and assert == `06d8af60` byte-exact (Σv
752,427, Sheezel 7964). **If this instance is a weather box (`83a4b21d`/Sheezel −95): HALT and
request a fresh instance — DO NOT freeze on a weather container** (freezing the flipped value
would bake the WRONG number in permanently — the one real risk, item 380). Only a clean instance
may produce the frozen artifact.

## EFFORT: Medium (localized: one function, freeze + assertion + proof). Why not Low: it touches
the value path (the V0 surface) so it earns full k=0 proof + a re-audit. MODE: auto, PLAN first.
TIME: ~1 h; flag >2×/<½×.

## FEED: item 380 (the diagnosis) · the q97m freeze precedent (`_merged_recover.py:49` note +
`data/q97m.pkl` load pattern at :64) · expected_boot.json (the pin schema) · MEMO_LEGE/LEGF v1.x
· acceptance JSON.

## THE JOB LIST (one commit each)
1. PLAN. Confirm the ONLY live import-time/board-time fit remaining is `_iso_dec` (:1222, called
   :1233/:1249); confirm _dev_advance/v_at_peak/PAR/NW are already frozen-or-order-fixed (they
   are, 2026-07-14 + Leg F). If a SECOND live fit is found: STOP, report — scope is one.
2. **FREEZE `_iso_dec` the q97m way:** compute the V0 pick-curve surface ONCE on this
   (clean-asserted) instance, pickle to `data/v0surf.pkl` (or the minimal frozen output the
   surface needs), and LOAD it thereafter — never fit at board-build. Mirror the q97m mechanics
   exactly (load-or-halt, md5-pinned). Alternative if cleaner: order-fix / rational-quantise the
   `_iso_dec` input grid so PAVA tie-breaks are BLAS-invariant — builder's choice, whichever gives
   byte-stability with the smaller surface-area; state which in the return.
3. **PIN IT:** add the new artifact's md5 to `data/expected_boot.json` (the fitted-artifact block,
   exactly as q97m/peak_model are pinned) so guard-5 asserts it on entry.
4. **THE PROOF (the re-audit, bounded):** k=0 balanced board == `06d8af60` byte-exact on THIS
   clean instance ✓; then the determinism claim — the frozen board must be byte-identical when the
   pickle is loaded on a DIFFERENT-seed/forced-kernel run (simulate the weather: force a BLAS
   coretype change or perturb, reload the pickle, assert the board holds `06d8af60`). Report the
   FULL k=0 row-diff vs the pre-freeze clean board: **it must be EMPTY (0 rows) — the freeze of a
   clean-instance fit changes nothing on a clean instance; the ONLY thing it removes is the
   weather flip.** If ANY row differs on a clean instance ⇒ HALT and return the diff (that would
   mean the pickle path is not identity — the item-380 second-order risk).
5. EXIT: RL_LEGF=0 chain byte-exact · dormancy suites (F3/F4/F5) still PASS · store untouched ·
   guard-5 now asserts v0surf too (the pre-bake red persists on the OTHER pins until the bake) ·
   annex · PR stacked on #119 · RETURN ≤25 lines: the clean-instance precondition result FIRST ·
   the k=0 row-diff (expect 0) · the forced-kernel determinism result.

## FENCE: IN = `engine/rl_after/_merged_recover.py` (`_iso_dec` + its load path) ·
`data/v0surf.pkl` (new) · `data/expected_boot.json` (the one pin add) · `session_2026-07-18/legf6/`.
HARD-OUT: the store · the curve · rl_model.py · the rest of the V0/`_iso_dec` chain logic (freeze
the OUTPUT, don't re-derive the surface) · pins beyond the one add · docs · ui. Any k=0 change
beyond removing the weather flip ⇒ HALT. S1–S6 · SILENCE IS A RED.
