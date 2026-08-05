# #326 rehearsal — every reader of the pool slot, re-derived at build time

Method: grep for the pool index / `pool_value` across the engine tree, then each candidate confirmed or
refuted by measurement on live bytes (runtime perturbation of the object it reads, and — where the object
is frozen at import — a full rebuild with the pool level moved). Nothing below is carried over from the
directive's list; the directive says that list must not be trusted.

| # | site | object it reads | is it a PLAYER PRICE? | what it reads after #326 |
|---|---|---|---|---|
| 1 | `rl_model.py` ~1010 `_PVC2M` / module `PVC` | the ladder incl. slot 65 = `int(pool_value)` = 237 | no — the ladder object itself | unchanged |
| 2 | `rl_model.py` `value()` `unpl_eq` (:1141) | was `_PVC2M[min(ep,70)]` | **the pricing function the directive names** — but see HALT 1: rl_export overwrites its output | now `_pick_level(p,ep)` → the entrant's signed division level |
| 3 | `rl_model.py` `value()` `pedestal` (:1156) | was `_PVC2M[min(ep,70)]` | same as 2 | now `_pick_level(p,ep)` → the entrant's signed division level |
| 4 | `rl_model.py` `_split_ladder` (:989-991) | asserts a pool level exists | no — a structural assert | unchanged |
| 5 | `_merged_recover.py` :1806 `draftval` → `_PVC0[min(effpk,KMAX)]` | the scaffold copy `_PVC0`, slot 65 | **YES on live bytes** — via `RUC_PRIOR_CAP*draftval(p)*_ruc_head_v0(p)` (:1180/:1184/:1703) it sets 12 board prices, all RUCK. See HALT 2. The audit classified this as scaffold-only. | unchanged (out of the rehearsed scope) |
| 6 | `_merged_recover.py` :1815 (`_PVCADOPT` L1b) | transient basis, superseded 25 lines later | no | unchanged |
| 7 | `_merged_recover.py` :1842 (`RL_PVC2`) | fills `_PVC0` = the scaffold/V0 basis | feeds 5 above, and the frozen V0 surface fit | unchanged |
| 8 | `_merged_recover.py` `_build_v0_curve` / `_build_v0_guard` / `_RUCCEIL` | `_PVC0` | indirectly — the V0 surface signature is curve-sensitive and the surface feeds `v0_start`, the ev() floor | unchanged |
| 9 | `rl_export.py` :138-140 `_ADOPTED` → shipped `PVC` | the artifact, slot 65 = 237 | no — the shipped pick ladder (pick side) | unchanged |
| 10 | `rl_export.py` :151 assert `max(_ADOPTED)==POOL_PICK` | structural | no | unchanged |
| 11 | `rl_export.py` :387-389 `CAT_BY_RANGE` pool band row | shipped `PVC` | no — a display band | unchanged |
| 12 | `rl_export.py` :654-666 LEG F5 entrant intake layer | shipped `PVC[65]` | no — expected annual intake, phantom, never a player's `v`. Total asserted 62931, **unchanged after #326** | unchanged |
| 13 | `ui/tools/ingest_inputs.py` :342 `_POOL_VALUE`, :384 `price_pick` | the artifact `pool_value` | no — prices draft PICKS past 64 for the trade desk | unchanged |
| 14 | `one_source_selftest.py` :483 `_PVC0[65] == pool_value` | the scaffold copy | no — an invariant on the scaffold copy; still true and still measuring what it always measured | unchanged |
| 15 | `s4_matrix_M1v7.py` :87 `draftval` column | `MA.PVC[min(effpk,POOL_PICK)]` | no — a book display column | unchanged |
| 16 | `_merged_recover.py` :1061 `draftval` (pre-rebind) | `MA.PVC` | superseded by the :1806 rebind | unchanged |

**Route taken on pool_value isolation:** a structural assert in the price path
(`rl_model._pick_level`) — a pool entrant returns his division level, and a non-pool entrant that
resolved to the pool index would halt rather than price. The old invariants that bind on `pool_value`
(items 4, 10, 14) are left exactly as they were: they describe the scaffold copy and the shipped ladder,
which is all they ever measured, so re-binding them would have removed a true check rather than fixed a
vacuous one. Proven able to fail: `gate6_isolation_broken_RED.txt`.

The isolation claim is proven for the sites the change owns (2, 3). It is **NOT** true of the board as a
whole: site 5 still puts `pool_value` into 12 ruck board prices. That is HALT 2.
