# DIRECTIVE — BAKE v2.11 (ROUND-14; reviews WAIVED by owner) · seat 14 · 2026-07-19
### Owner ruled: bake now — viewing / sealed-reads / ratification / cold-audit WAIVED (2026-07-19).
### ONE build: the boot prerequisite + the bake prep, then it HANDS THE OWNER the tag+promote
### (owner-only). Board of record is ROUND-14 (store 968de0c7) — this bakes THAT. Boot fix is
### VALUE-NEUTRAL; no pricing change anywhere.

## ⚠️ ENTRY ORDER (READ FIRST): do NOT run `bash bootstrap.sh` or any Guard-5 gate BEFORE Step 1. On
## base 3055ea5 the engine pins are STALE and Guard 5 WILL HALT (item 399) — Step 1 FIXES that. Run
## Step 1's md5 verification + re-stamp FIRST; bootstrap.sh is asserted only AFTER the re-stamp (Step
## 1's last line). A bootstrap HALT *before* Step 1 is EXPECTED — it is not a stop.

## STEP 1 — BOOT-IDENTITY RE-STAMP (unblocks Guard 5) — VERIFY BEFORE STAMP
Guard 5 HALTs because expected_boot.json's engine pins lag: rl_model=a5fd3d7d, engine_head=40f43772
(last stamped at Leg-D-Act-2; legs E/F5/F6 advanced the engine and the boot file was never re-stamped).
- VERIFY (SSI — NEVER stale-agrees-with-stale): md5 the engine at base 3055ea5 — assert
  `rl_model.py == cc626d7d` AND `_merged_recover.py == 904722cd`, AND confirm 3055ea5 descends from the
  audit-clear head 15a9abd (#119) + F6 540b62f (#121). ANY mismatch → STOP + report; do NOT stamp.
- RE-STAMP data/expected_boot.json: `engine_head → 904722cd`, `rl_model → cc626d7d`. ONLY these two;
  every other pin (store 968de0c7, q97m cfdc7321, v0surf 3af2b725, band, notes) BYTE-UNCHANGED.
- VERIFY + CLOSE the build_board.sh engine-assert BYPASS: make board builds run the SAME Guard-5 assert
  as bootstrap.sh (no silent skip). If it isn't where reported, report what you find before changing.
- PROVE: bootstrap.sh + Guard 5 GREEN 5/5; the balanced board is UNCHANGED (RL_LEGE=0 RL_LEGF=0 → same
  md5 as pre-stamp; a re-stamp cannot move the board). Value-neutral (k=0).

## STEP 2 — REPRODUCTION GATE (the ONE guard kept — it's free and it's correctness, not review)
Build the balanced board (RL_LEGE=0 RL_LEGF=0) and assert == `06d8af60` byte-exact. If this container
does NOT reproduce (a diverging box) → HALT + request a fresh container. Bake ONLY on a reproducing
container — the flipped board reorders the top board (item 394); we do not ship that.

## STEP 3 — TAG-READY (make canonical; the TAG + PROMOTE are OWNER-ONLY)
The Step-1-re-stamped, Step-2-reproducing head IS the bake head — nothing more is needed to make it a
usable canonical round-14 engine. Do NOT chase the STALE `BAKE_RUNBOOK` (it predates this saga — see the
banner on it). Viewing / sealed-reads / ratification / cold-audit / gate-checks are WAIVED — do not run
or block on them. TWO lineage items are DEFERRED post-bake housekeeping, NOT blockers (note them, do not
chase): acceptance v1_21 (a gate-review JSON on docs/main; does not affect board usability) and the
INFRA_ALLOW entries. ONLY if the boot or the tag genuinely fails without an INFRA_ALLOW allowance, set
the MINIMAL needed and report it — otherwise skip.

## GIT ENTRY: base = `3055ea5` (#123) STRICT, HALT on mismatch. Stack on #123. THREADS=1.
## EFFORT: High (a bake — irreversible-adjacent; the boot verify-before-stamp + the reproduction gate
must be exact). MODE: auto, PLAN first. TIME: ~45–75 min incl. container retries. FENCE: IN =
data/expected_boot.json (the 2 engine pins ONLY) + the build_board.sh assert path +
session_2026-07-19/bake_v211/. HARD-OUT: store VALUES, curve, q97m, v0surf,
rl_model.py/_merged_recover.py (engine — read-only, we stamp its md5, never edit it), every pricing
value. **Do NOT push the tag or promote main — that is the owner's.**
## EXIT (≤25 lines): Step-1 verify result (both md5s + lineage) FIRST, then bootstrap GREEN + board
`06d8af60` reproduced + the tag-ready head SHA + the EXACT owner commands (`git tag v2.11 <head>` ·
push tag · FF-promote main). Branch · head SHA · PR stacked on #123.
