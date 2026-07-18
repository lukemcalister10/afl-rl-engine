# JOB — `pedestal` consumer (PLAN job 3 / directive-B job 4) — PROOF

**Site** `rl_model.py:836` `pedestal = _PVC2M[min(ep,70)]*relative*surv*decay_eff` (`PVC → _PVC2M`).
The pedigree pedestal is read on the played AND unplayed paths, so it reorders more rows than `unpl_eq`.

## (a) BEFORE/AFTER board md5 @ RL_PVC2=1  + affected rows NAMED
- BEFORE `01c3645d` (after `unpl_eq`) → AFTER `06d8af60`.
- **688 rank movers / 804 active.** Full named list: `out/job_pedestal_movers.txt`.
- Because `pedestal` feeds `proj_value` for BOTH tracks, the movers now include many `unpl=False`
  (played) rows whose `proj_value` shifts as their pick-anchored pedestal reprices under v2, plus the
  continuing pedigree reordering.

## (b) V-PARITY (checkpoint gate)
`board_movers.py` vs `01c3645d`: **0 / 804 active `v` movers, 0 pick movers.** Displayed `v` (= `ev()`)
byte-identical. Ordering-only. **No checkpoint trigger.**

## (c) BYTE-HOLD
`RL_PVC2=0` board = **`9829d01a`** byte-exact. `_PVC2M is PVC` when off ⇒ pedestal reads v3.4 ⇒ intact.

## WHY
`pedestal = PVC[ep]·relative·surv·decay_eff`; only the `PVC[ep]` factor moves (to v2). Rows whose
`min(ep,70)` sits where v2 ≠ v3.4 reprice their pedestal, shifting `proj_value` (the sort key) — never
the shipped `ev`. Same-`ep` rows move coherently; the rest cascade.
