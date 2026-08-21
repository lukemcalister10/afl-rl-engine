# R24 DRESS REHEARSAL — THE PREREG, WRITTEN BEFORE THE FLIGHT

**SYNTHETIC. SANDBOX ONLY. NOT A ROUND. NOT OWNER DATA. THE BOARD THIS PRODUCES IS SYNTHETIC AND
NEVER LEAVES THE SANDBOX.**

Date 2026-08-21. Sandbox: a `git worktree` of live HEAD `94bca14` under the seat scratchpad. The
live tree is never written by this act except the evidence directory that carries this report.

## WHAT IS BEING REHEARSED

`tools/land round`'s **REAL, ARMED PATH** — the one no run has ever taken. The self-test's built-in
round rehearsal declares `round.scores: null`; every one of its eighteen round cases therefore runs
with nothing armed and nothing applied. This act flies the other half.

## THE INPUTS, AND WHAT IS SYNTHETIC ABOUT THEM

| input | shape | synthetic how |
|---|---|---|
| `scores/R24.csv` | `Player,2026 R24`, cp1252, CRLF, 411 rows | names carried off the R23 export; scores re-dealt under seed 20260824 with 10 declared risers / 10 declared fallers |
| `docs/owner_annotations/SITTER_2026_v1.csv` | the pinned owner sheet | re-cut ONLY if H2 trips (it is engineered to trip) |
| identity overrides | asserted, never authored | the R24 file writes the Bailey pair APART, so it needs NONE |

## PREDICTIONS (falsifiers, every one)

1. **P1 — H2 TRIPS.** `scores/R24.csv` lists two players the pinned sheet marks `injured=Y`
   (Tom Green, Connor Rozee). `catchup_preflight` must HALT before anything is armed, naming both.
2. **P2 — the preflight is otherwise CLEAN**: listed 411 / resolved 411 / listed-zero 0 /
   absent-DNP 393, `sha256 6e9003d5…`, one identity override consulted (Callum Brown).
3. **P3 — the sheet re-cut path writes the pins.** After the owner-worded re-cut flipping those two
   rows `Y -> N`, `data/sheet_pins.json` reads `sheet_injured_y: 33`, rows unchanged at 219, and
   `engine_head` is UNMOVED across the sheet commit.
4. **P4 — the advance moves store, board and `as_of_round` 23 -> 24**, ledger 3497 -> 3908
   (delta 411, no duplicate), `guard5=True`, `final=FINALIZED`, histories reaching 24.
5. **P5 — the movers move the right way.** Every one of the ten declared risers rises on the R24
   movers report; every one of the ten declared fallers falls.
6. **P6 — the day-0 step's ACTIVE path prints a row diff and installs.** This is its first exercise
   in the positive direction: the self-test only ever proves the M1b guard (activated + zero movers
   = halt).
7. **P7 — the live tree ends byte-identical.** board `b3e8da99…`, store `b745002e…`, engine head
   `3af8c1f7…`.

## FALSIFIERS THAT WOULD END THE REHEARSAL BADLY

* a halt whose cause is the MACHINE rather than the synthetic inputs — reported, never patched here
  (a rehearsal that rewrites the machine invalidates itself);
* any write to the live tree outside `docs/evidence/r24_rehearsal_2026-08-21/`;
* the synthetic board escaping the sandbox.
