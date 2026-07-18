# LEG F2 — VERIFICATION

## Provenance (asserted at load; HALT-on-mismatch)
- store md5 = `968de0c7` == pinned `968de0c7` ✓
- curve payload = `89c14729` == pinned `89c14729` ✓ (curve file `56dd7a7b`)
- engine `6ad07bb2` · rl_model `cc626d7d` · balanced board reproduced `06d8af60` (verified separately, dev-shell)

## §5.9 leak-free proof (games handling + future-row leak)
- top-level cumulative `games` field does NOT feed ev(): perturbing it leaves ev unchanged = True
- full-object ev(p,Y) vs truncated ev(asof,Y) on non-retired members: 451/1608 differ, max |Δ|=676
  → the shipped rl_export backward lens (ev on the FULL object) LEAKS future rows via raw_ev (the W4 context wrapper); the truncated re-render used here is leak-free. FINDING, not a fix.

## Now-board consistency with the balanced board 06d8af60
- now-board vs balanced active set: 804 common keys, 804/804 identical v (now-board IS the canonical active set, valued by the same method) ✓
- now-board n=804 == balanced active n=804 (exact) — the now board reproduces 06d8af60 by construction
