# JOB — `build_pvc_v34` GLOBAL PRODUCER SWAP (PLAN job 5) — PROOF (board-null)

**Site** `rl_model.py:760` `PVC=_PVC2M` (placed immediately after the `_PVC2M` block, before
`SEASON_PROG`). This unifies the module-level `PVC` onto the migrated curve under the flag, so the
producer's v3.4 output no longer feeds any downstream reader.

## Scope (what this catches)
After the leaf consumers (`unpl_eq`, `pedestal`) already read `_PVC2M`, the only remaining `PVC[...]`
readers are the **print-only diagnostics**: `pe(v)` (value→pick-label, `:1108-1110`) used by `rk()` and
the `TOP 15` / `PVC:` stdout lines. The global swap points those at v2 for consistency. It is placed
AFTER the `build_pvc_v34` import fit + `CURVE_H`/`BOARD_FACTOR`/`SCALE` (`:714-737`), so **`SCALE` is
untouched** — no player is rescaled.

## (a) BEFORE/AFTER board md5 @ RL_PVC2=1
- BEFORE `06d8af60` (after `pedestal`) → AFTER `06d8af60`. **Byte-identical (board-null).**
- `board_movers.py`: 0 active `v` movers, 0 pick movers, 0 rank movers.

## (b) V-PARITY / (c) BYTE-HOLD
- V-parity trivial (board byte-identical).
- `RL_PVC2=0` board = **`9829d01a`** byte-exact — with the flag off `_PVC2M is PVC`, so `PVC=_PVC2M`
  is literally `PVC=PVC`, a no-op.

## Verified concern: `g['PVC']` key-set
`rl_export` grabs `g['PVC']` but rebuilds its OWN shipped curve as `{k:_ADOPTED[k] for k in PVC if k in
_ADOPTED}` — the values come from rl_export's own `pvc_curve` artifact and the key-set is intersected
with `_ADOPTED`, so any change in `g['PVC']`'s key-set does not reach the board. Confirmed empirically:
the RL_PVC2=1 board is byte-identical before/after the swap.

## Verdict
Board-null; the migration's board-visible effect is entirely carried by `unpl_eq`+`pedestal`. This swap
completes the producer→consumer unification (print-layer + future readers) with zero board movement.
