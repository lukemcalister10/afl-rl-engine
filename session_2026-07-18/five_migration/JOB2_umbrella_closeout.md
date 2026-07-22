# JOB 2 CLOSE-OUT (directive-B) — the value()/rank/pick-equiv umbrella (cumulative characterization)

The umbrella over the whole migration: final RL_PVC2=1 board vs the ACT-2 baseline `270a2c5f`, with the
total mover set characterized and board-wide v-parity asserted.

## Cumulative board move
- **`270a2c5f` (ACT-2 ev-channel baseline) → `06d8af60` (all rl_model MA.PVC consumers on v2).**
- Kill-switch: **`RL_PVC2=0 ⇒ 9829d01a`** byte-exact (unchanged throughout).

## Board-wide V-PARITY (the checkpoint assertion)
Keyed by `key`, across the full move `270a2c5f → 06d8af60`:
- **displayed-`v` movers: 0 / 804**  · **pick movers: 0**
Every shipped per-row `v` (= `ev()`) is byte-identical to the ACT-2 baseline. The migration is a pure
rank / pick-equivalent re-ordering. **No checkpoint trigger anywhere in jobs 2–5.**

## Total rank movers — named, real vs cascade
`out/job_umbrella_movers.txt` (full list, each row tagged REAL/casc). Summary:
- **697 rank movers / 804 active** = **394 REAL** (own `proj_value` = the sort key moved) + **303
  cascade** (own value unchanged, displaced by real movers repositioning around them).
- REAL decomposition (`out/proj_value_real_movers.txt`, 399 proj_value movers): **59 unpl=True**
  (pedigree, via `unpl_eq`+`pedestal`) + **340 played** (via `pedestal`'s pick-anchored factor).
- Headline real movers: **Will Darcy #445→#342 (proj_value 277→508)**; the DOB-corrected re-entry class
  Fred Rodriguez / Riley Onley / Leon Kickett / Ollie Greeves / Nick Driscoll (all up ~+220 proj_value);
  played movers Jhye Clark #321→#442, Neil Erasmus, Seth Campbell.
- Cascade examples: Mitchell Lewis, Kyle Langford, Matthew Kennedy, Bailey Williams, James Rowbottom —
  `proj_value` unchanged, displaced downward.

## The pick-equivalent channel
`effpk` (pickless `_eff` = `PICKEQ`) movers across the curve = **0/804** — the `_natcv34`/`_pick_equiv`
inversion is realised-value-based and curve-independent (see `JOB_natcv34_NULL_PROOF.md`). So the
"pick-equivalent" movement in this umbrella is the RANK/pick-label channel (the `proj_value` sort +
`pe()` labels), not a shift of the intake pick-equivalents.

## Net characterization
The five-migration moves the pick **currency** the pedigree/pick-anchored value machinery reads (v3.4 →
v2), which re-orders ~87% of the active board through the `proj_value` sort key, while the shipped
valuations (`ev`) and the intake pick-equivalents (`PICKEQ`) are held byte-exact. Effect class =
RANK / PICK-EQUIVALENT, v-parity board-wide. Consistent with the checkpoint law; nothing to escalate.
