# DIRECTIVE — FIVE-MIGRATION BUILD B (completion) · seat 13 · 2026-07-18
### Completes the rescued v2 job (items 339/340). Job 1 DONE (HOLD, accepted); jobs 2–5 + the
### rider + exit proofs remain. Ruled R107.5 · census = map of record @ e4177c2.

## GIT ENTRY (verbatim; the item-334 law)
`git fetch origin main claude/five-migration-pvc-consumers-kxykfd`
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git claude/five-migration-pvc-consumers-kxykfd`
must return exactly `e7c59d07cfbbe44882ea0642cbba6f09e2da44e5` (STRICT; HALT on mismatch).
`git checkout claude/five-migration-pvc-consumers-kxykfd` — CONTINUE ON THIS BRANCH (same job,
same PR line). Discard any auto-created branch. Governance docs live on MAIN; never join
lineages; every repo claim cites a this-session fetch; anything "hard-to-reverse" = HALT.
Entry assertions: store `968de0c7` · curve payload `89c14729` · `RL_PVC2=0` ⇒ board `9829d01a`
byte-exact (re-proof).

## EFFORT: High (engine writer; board-order changes; the `_natcv34` inversion is the subtlest
site). Why not Extra: half the job is done and proven; the remainder is mechanical with per-step
proofs. MODE: auto — first commit = PLAN. TIME: ~2–3 h; flag >2×/<½×; report actual.

## FIRST ACTS (in the PLAN commit)
1. **WIP AUDIT:** commit `e7c59d0` ("WIP-HALTED") captured uncommitted job-3 wiring + partial
   job-2 work. Audit it line-by-line; KEEP what meets the proof standard, REVERT-AND-REDO what
   does not; state the disposition per hunk.
2. **FENCE CURE (the 322 pattern, again):** the job-1..3 work edited
   `engine/rl_after/single_source.py` (ALLOWED_OPENS += `pvc_curve_v2.json`) — correct and
   mechanically required, but ABSENT from the PLAN's derived fence. Re-derive the fence from the
   job list INCLUDING it, with the one-line justification, and carry
   `one_source_selftest.py` as census-IN if execution requires it (own justification if touched).

## THE JOB LIST (per-consumer commits; census wins)
3. **Finalize JOB 3 (`unpl_eq` :798):** complete the proof — RL_PVC2=1 board hash + FULL named
   rank-mover list (real movers vs pure cascade, the Will Darcy #446→#325 class) + v-PARITY proof
   (per-row shipped v byte-equal) + RL_PVC2=0 ⇒ `9829d01a` re-proof.
4. **JOB 4 (pedestal :813)** then 5. **JOB 5 (`_natcv34` :834-853)** — one commit each, same
   proof template (board hash · named movers · v-parity · kill-switch byte-hold).
6. **JOB 2 close-out:** the value()/rank/pick-equiv umbrella — the cumulative characterization:
   final RL_PVC2=1 board vs `270a2c5f` (the ACT-2 baseline), total rank movers named, v-parity
   asserted board-wide.
7. **THE RIDER (report-only, items 326/327 — rider (iv) WAITS on this):** emit the engine-side R
   inputs (the free-intake pick-equivalents) as a committed report. No value change.
8. EXIT: frozen suite (S4) · five SSI guards · **RL_PVC2=0 ⇒ `9829d01a` byte-exact (final
   proof)** · store md5 `968de0c7` unchanged · gates snapshot · PR raised on this branch ·
   RETURN ≤30 lines: branch · head SHA · PR # · actual vs band · three narrowest margins ·
   plain-terms close.

## THE CHECKPOINT LAW (BINDING; new in Build B)
The expected effect class of jobs 3–6 is RANK / PICK-EQUIVALENT movement with shipped per-row `v`
values UNCHANGED (parity-gated; the ev-channel moved at ACT-2, not here). If ANY commit moves a
shipped per-row `v` at RL_PVC2=1: **HALT, commit nothing further, return the row list to the
supervisor** — that is a checkpoint judgment, never a build's call. Job 1 stays CLOSED (HOLD per
R107.5); do not reopen; the retrain rides post-bake.

## FENCE (derived in the PLAN per FIRST ACT 2)
IN expected: `rl_model.py` · `single_source.py` (the allowlist line, now recorded) ·
`one_source_selftest.py` census-IN if required · `session_2026-07-18/five_migration/`.
HARD-OUT unchanged: the store · `pvc_curve_v2.json` as a write · `_merged_recover.py`'s
V0/`_iso_dec` chain · `s4_matrix_7147.py` · SEASON_PROG · `docs/`. HALT on any HARD-OUT need.

## STANDING: S1–S6 · SILENCE IS A RED (every check verdicts or HALTs; exit codes propagate).
