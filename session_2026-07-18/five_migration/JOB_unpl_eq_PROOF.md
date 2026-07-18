# JOB — `unpl_eq` consumer (PLAN job 2 / directive-B job 3) — PROOF (finalized)

**Site** `rl_model.py:821` `unpl_eq=_PVC2M[min(ep,70)]*decu*debut_factor(p)` (code in the WIP `e7c59d0`,
audit disposition KEEP). This finalizes the proof the WIP was HALTED without.

## (a) BEFORE/AFTER board md5 @ RL_PVC2=1  + affected rows NAMED
- BEFORE `270a2c5f` (ACT-2 baseline, no rl_model consumer migrated) → AFTER `01c3645d`.
- **469 rank movers / 804 active.** Full named list: `out/job_unpl_eq_movers.txt` (each row: rank
  before→after, Δ, displayed `v`, type, pick, unpl-flag; REAL/casc per the cumulative proj_value set).
- REAL movers (own ordering value changed): the pre-debut / unplayed pedigree rows — headline
  **Will Darcy #445→#324 (−121)**, then the DOB-corrected re-entry class Fred Rodriguez (#440→#327),
  Riley Onley (#441→#329), Leon Kickett, Ollie Greeves, Nick Driscoll — all `unpl=True`, moving UP as
  the v2 deep tail lifts their `unpl_eq` (v2 pick-70 = 516 vs v3.4 306).
- CASCADE: settled `unpl=False` picks (Kyle Langford, Matthew Kennedy, Bailey Williams, …) displaced
  DOWN by the pedigree rows passing through their band — their own ordering value is unchanged.

## (b) V-PARITY (the checkpoint gate)
`board_movers.py` keyed by `key`: **0 / 804 active `v` movers, 0 pick movers.** Every shipped per-row
`v` (= `ev()`) is byte-identical to `270a2c5f`. The move is pure ordering (rl_model `_v=proj_value(0)`
sort key), not price. **No checkpoint trigger.**

## (c) BYTE-HOLD (kill-switch)
`RL_PVC2=0` board = **`9829d01a`** (byte-exact == pinned baseline). `_PVC2M` is the same object as `PVC`
when the flag is off ⇒ `unpl_eq` reads byte-identical ⇒ v3.4 path intact.

## WHY (one line per moved class)
- REAL/up (unpl pedigree): v2's higher deep-pick currency raises `unpl_eq` ⇒ higher `proj_value` ⇒ up.
- CASCADE/down (settled picks): unchanged value, displaced by the pedigree rows repositioning above them.
