# JOB — `_natcv34` inversion / `_pick_equiv` (PLAN job 4 / directive-B job 5) — **NULL** (proven)

This is the flagged "subtlest site." The PLAN fixed its exact form **at execution from measured
scale-consistency**. Measurement + code both say: **there is nothing to repoint, and repointing would
be wrong.** No engine change.

## The site (`rl_model.py:855-875`)
`_natcv34[k]` is a **national realised-career-value curve**: `_ce([_nv_bwd(p) for p in hist if _in_pvc(p)
and abs(_epk(p)-k)<=4], _alpha_pvc(k))`. `_pick_equiv(v)` returns the pick `k` whose `_natcv34[k]` is
nearest `v`. `PICKEQ[type] = _pick_equiv(pooled_realised_value)` sets `_eff` for the pickless intake
mechanisms → `effpk(p)` → `ev(p)`.

## Why it is a NULL (code proof)
The inversion base and the pooled value are BOTH realised-outcome quantities:
- `_nv_bwd(p)` = posval-VOR on best-2 (busts→0) — **reads no PVC curve.**
- `_alpha_pvc(k)` = a risk-dial ramp in the pick *number* `k` (`PVC_ALPHA_LO→HI`) — **not the PVC
  curve values.**
- `_natcv34`, `_pick_equiv`, `PICKEQ` — **no `PVC` / `_PVC2M` read anywhere in the chain.**

The pick-equivalent is a pick *number*, currency-agnostic by construction. It then flows into the
already-migrated `pedestal`/`unpl_eq` (which read `_PVC2M[effpk]`), so the pickless rows are priced off
the v2 curve **at the correct pick** with no change to the inversion. Realised-vs-realised inversion is
already scale-consistent; there is no v2 currency to invert against here.

## Why repointing would be WRONG (the checkpoint tie-in)
"Inverting against the v2 currency" would replace a realised-outcome inversion with a pricing-curve
inversion — a category error — and would shift `PICKEQ → _eff → effpk → ev`, i.e. it would move a
**shipped per-row `v`** for the pickless intake rows. Per the checkpoint law that is a supervisor
judgment, never a build's call. The correct, in-scope action is to leave the inversion untouched.

## Empirical confirmation (measured this session)
Dumped `MA.effpk(p)` for all 804 players under v3.4 consumers (RL_PVC2=0) vs v2 consumers (RL_PVC2=1)
with the fully-migrated engine:

- **effpk (pickless `_eff` = PICKEQ) movers across the curve: 0 / 804.**  (`out/proj_value_real_movers.txt`)

So `PICKEQ`/`_natcv34` is curve-INDEPENDENT — the null holds not just by inspection but by measurement.
Board effect: none beyond what `unpl_eq`+`pedestal` already produced (`06d8af60` unchanged).

## Verdict
NULL — no repoint. Board `06d8af60` (RL_PVC2=1) and `9829d01a` (RL_PVC2=0) both unchanged. V-parity
trivially holds. Proves the null, hash-equal, stated.
