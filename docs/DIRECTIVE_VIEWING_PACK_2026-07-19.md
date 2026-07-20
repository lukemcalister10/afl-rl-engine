# DIRECTIVE — THE VIEWING-PACK RENDER · seat 14 · 2026-07-19 · supersedes the 2026-07-18 render
### The owner's ladder viewing. RE-BASED to the F6 head `540b62f` (PR #121): the owner ruled F6
### RIDES AS-IS into the v2.11 bake (no lite, no re-audit — 2026-07-19), so the viewing renders the
### EXACT board that bakes — via the FROZEN v0surf load path, not the pre-freeze fit. Two corrections
### vs the 07-18 draft: (1) base `15a9abd` → `540b62f` STRICT; (2) the balanced-board precondition
### now carries the MANDATORY `RL_LEGE=0 RL_LEGF=0` env — the LEGE=0 correction (rev162 §2b): naming
### the `06d8af60` target WITHOUT the env HALTed F6's first run. READ-ONLY (Tier 3) · report-only ·
### changes NOTHING; never bakes. THREADS=1.
### RE-BASED AGAIN (2026-07-19, env-pin): base `540b62f` → the ENV-PIN head `3055ea5` (item 392), so
### the render runs on the PINNED numpy env — this pinned-env render is CONTAINER #2 of the item-392
### reproduction gate. Run `bash bootstrap.sh` FIRST; its fail-closed ENV-PIN assert must PASS. The
### board is byte-identical to the F6 head (the env pin is value-neutral, k=0), so every figure below stands.

## GIT ENTRY (read-only variant — item-338 law)
`git fetch origin main claude/env-pin-2026-07-19-4y4w0p`; ls-remote must return
`3055ea5ffdc390f81d5e17476a60fbb841f24cff` STRICT (the ENV-PIN head, stacked on PR #121), HALT on mismatch.
It descends from `15a9abd` (item 375) + the F6 freeze (item 381) + the env pin (item 392). **Run `bash
bootstrap.sh` at start — its fail-closed ENV-PIN assert MUST pass before any board build (item 392).** Branch
parent = MAIN; provenance = stamps at load: store `968de0c7` · curve payload `89c14729` ·
per_entrant `40d7da7c` · v0surf `3af2b725` (the frozen V0 surface, Guard-5 asserted).
**REPRODUCTION PRECONDITION (item 366 + the LEGE=0 correction, MANDATORY):** before rendering any
board, build the balanced board **with `RL_LEGE=0 RL_LEGF=0`** and assert it == `06d8af60`
byte-exact. On the PINNED env + F6 head this LOADS the frozen v0surf surface AND runs the pinned numpy
(so np.interp is deterministic — item 391/392); the precondition is robust. If it does NOT reproduce,
HALT and report — the pin is insufficient on this container → we pin deeper (item 392 gate). This
render reproducing `06d8af60` IS the container-#2 leg of the gate. Engine imported READ-ONLY;
never edit engine/store/curve/docs.

## EFFORT: Medium (mostly COLLATION of committed artifacts, not computation — only THREE items are
fresh compute: the per-row Δ-vs-v2.10 join, the Rozee/Reid re-render at the head, and the
reproduction-precondition board build; the rest — board, retro boards, bridge, rider tables, gate +
audit ledger — are existing artifacts gathered and laid out; the ui/app renderer already carries the
Δ/track fields). MODE: auto, PLAN first. TIME: ~1–1.5 h (flag >2×/<½× per S3). Reuse S5: the
board/book emitters, board_diff, the rider outputs @ their pinned heads, the F2 retro boards, the
gate harnesses — DO NOT rebuild what is committed.

## THE PACK (one committed section each; every figure carries its provenance tag —
## owner-seen / re-runnable / report-only — and its source head)
1. **THE BOARD** at `540b62f`, RL_LEGF=1 default: full ranked board (int-v `9d097fce`; Σv 752,427 —
   F6-head-confirmed, the k=0 identity guarantees these hold) + the balanced `06d8af60` confirmation
   line (RL_LEGE=0 RL_LEGF=0, frozen-loaded). Per-row: v · rank · the Δ-vs-v2.10 column (v−the
   shipped 9829d01a-equivalent board, per-row, NAMED movers).
2. **THE MOVERS REPORT:** top value + rank movers v2.10→candidate, NAMED, with a one-line why-class
   each (curve re-rank vs new evidence). **Rozee + Reid re-rendered at 540b62f** (their item-344
   figures were Leg-E-era — supersede with the head values). The raw-pick benefit-of-doubt rows
   (item 344) surfaced as their own named list for the owner's ruling.
3. **THE LENS VIEW:** per-lens board totals bal/+1/+2 WITH and WITHOUT the phantom layer (the
   item-360 split), + the −1/−2 retro boards + the bridge (−2 770,987 → −1 771,152 → now 752,427,
   all provenance-tagged), so the owner sees conservation across all five lenses in one place.
4. **THE RIDERS (i)–(iv):** the calibration/tail-influence/uncertainty views + the replacement
   view's THREE R candidates (R_realized 207 [184–229] · R_owner 220 · R_curve 471) side by side,
   with the gross-vs-net p1/p60 and p1/p90 ratio tables. Verdict-free.
5. **THE GATE + AUDIT LEDGER:** every gate value beside its acceptance threshold (from shard B/D) +
   the five-shard audit verdict (item 375, all green) + the two owned lineage-split findings + **the
   F6 freeze line: k=0 row-diff = 0 rows (F6 moves NO value; frozen==pristine identity across all 4
   configs) + Guard-5 now asserts v0surf `3af2b725`** + the known guard-5 pre-bake red on the OTHER
   pins (rl_model/engine_head, pre-existing) — so the owner sees the full evidentiary state, nothing
   hidden.
6. **THE RATIFICATION LIST (the owner's calls, laid out, each with its seal + what it decides):**
   tail read STAND/RETIRE · R=207 free-intake basis · entrant structure `a17aafed` · φ pedigree
   `fd92b6fc` · r_pop `c62b5ee8` · posture presets `c2e17c49` · the raw-pick benefit-of-doubt · the
   knife-edge note (item 374 — downgraded: weather, now FROZEN OUT by F6). Each: what it is, the
   measured value, what ratifying vs re-ruling changes, and the recommendation with what would change
   it.
7. RENDER as the UI board HTML (the existing ui/app pipeline, read-only) + a companion markdown
   summary. EXIT: README (artifact→provenance map) · PR REPORT-ONLY/DO-NOT-MERGE · RETURN ≤25 lines:
   the reproduction-precondition result FIRST, then the pack manifest.

## FENCE: IN = `session_2026-07-19/viewing_pack/` ONLY. HARD-OUT: every engine/store/curve/docs file.
HALT on any HARD-OUT need. S1–S6 · SILENCE IS A RED · findings not verdicts (the owner rules at the
viewing; the pack informs, never pre-empts).
