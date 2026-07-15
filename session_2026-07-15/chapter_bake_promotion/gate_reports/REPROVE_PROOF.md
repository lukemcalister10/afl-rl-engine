# TASK 4 — SHIP-GATES RE-PROVE ON THE FROZEN q97m (bake head) · 2026-07-15

Regenerated `data/gates_snapshots/gates_fc7045d6.json` from a FRESH bootstrap on the candidate/bake head,
clean env (NO `SGC_*` — item-151 leak avoided), frozen q97m `cfdc7321` (NEVER refit; freeze ruling stands).

## RESULT — byte-identical to the committed snapshot (zero drift)
- Regenerated snapshot md5 = `42abe7d5c05465043cc98d6a65a9c039` == the committed `gates_fc7045d6.json`
  (captaincy build 2e96c92). The bake re-prove reproduces the committed artifact exactly — the snapshot at
  the bake head IS what the frozen q97m + frozen board (790136a3) + store (b1fd0bce) + engine (fc7045d6) +
  config (c2d233ae) deterministically produce. Nothing to re-commit; the committed snapshot is proven.

## VERDICT (frozen suite 764a0d91)
`FAIL=3  FEATURE=1  HALT=1  PASS=16  PENDING=4  STRUCK=1`

- **B1 HALT** — CANDIDATE regenerated this run (engine fc7045d6, store b1fd0bce, config c2d233aec104):
  raw class-year sums averaged unweighted; ratios **y4=1.2960 · y5=1.3057 · y6=1.2544**; hard ≤1.30 →
  BREACH at y5 (HALT). BOTH BOUNDS: the frozen-1.30 verdict is HALT (y5 +0.0057 over); the owner's waived
  1.335 CLEARS by **0.0293** (item 143 filed it; the waiver's application authority is register item 159,
  not this suite). The suite exits non-zero by design — the 1.30 gate is owner-only and unamended.
- **FAILs = exactly A2 / A3 / A12** (all data-caused): A2 Curtis 0.753×Ward (ruling D7); A3 Rozee 0.64
  (out for 2026, knife-edge by design); A12 Travaglia>Moraes / Smillie>Retschko. NO other FAIL.
- **A-PAIRS pair-3** (Sanders>Bont, +11.9%) is the standing read (item 151/162), expected until the PVC
  chapter — scored in the build measurement, not a ship_gates FAIL.
- FEATURE=1 = B5 floor-as-pricing-feature (Luke-ruled). B3 book seal 99be9b36 PASS · B4 board 790136a3 PASS.
