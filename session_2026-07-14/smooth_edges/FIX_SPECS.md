# THE THREE FIXES — specification (as measured by overlay_smooth_edges.py)

All three are applied by **monkeypatch overlay** to the live functions `_lvlcurr` / `_coreM1`
(and the `cp._lvl_eff = _inferM1` chain). **Nothing in the committed engine is modified.** All-fixes-OFF
reproduces the base board byte-exact (ev-md5 `b5dbead0` == base). Each fix is default-OFF; ablated
alone and combined. Board of record = `3dc19fbb` (store `340a7a32`), the ITEM-20 successor to tagged
`81e48293`.

## FIX 1 — smooth small-sample damping in `_lvlcurr` (Jamarra's fix; data-derived curvature)
`_lvlcurr` weights each season by `games · ld^decay`. A 3-game season gets the full per-game weight —
no damping. **Empirical shape:** for 10,459 player-seasons, the variance of a season mean's deviation
from the player's leave-one-out career mean scales as `Var ≈ 690/g + 119`. That is the exact signature
of a sample-mean reliability `ρ(g) = g/(g+k)` with **k = 690/119 ≈ 5.8**. So a season's average is only
`ρ(3)=0.34`, `ρ(8)=0.58`, `ρ(22)=0.79` as reliable as a full sample.

**Damping (concave, data-set curvature):** replace the per-season weight `g` with `g·ρ(g) = g²/(g+k)`,
`k=5.8`. A thin season counts *less than proportionally*; a full season is ~unchanged. **This subsumes
the hard `<8 games → 0.25` rule** (`_par_prior`) with a smooth curve. Key property: a **single-season**
player is unchanged (the ρ factor cancels in the normalized ratio) — so first-year kids are untouched
by construction.

## FIX 2 — smooth the tolerance step (LIVE branch: `_coreM1` line 244, `TOL_M1=5.0`)
Base up-branch: `if Lc>=Lo: return (Lo+S·(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq) else Lo` — a hard
step at `TOL_M1=5.0` (credit jumps from 0 to `S·5` at the boundary) plus a boolean `_radq` gate.
**Fix:** ramp the credit fraction smoothly with `smoothstep((Lc-Lo)/TOL_M1)` over `0..TOL_M1`, and
soften `_radq` to a 0.5..1 multiplier instead of an on/off gate: `est = Lo + S·(Lc-Lo)·r·rq`.
_(NB: the directive quotes the dead `_lvl_eff_core` FLAT_TOL step; the live step is TOL_M1 — see
D1_ATTRIBUTION.md. The Blakey/English pair does not straddle this step, so Fix 2 moves neither.)_

## FIX 3 — extend the pedigree fade past PROVEN_N (owner's proposal)
Base: at `n≥PROVEN_N` the established branch has **no** par term; below, `(1-c)·par` with
`(1-c)=0.75/0.50/0.25/0`. **Fix:** carry a small, continuously-decaying pedigree pull past the
boundary — `w_ped(n) = 0.10·0.30^(n-4)` for `n≥4` → **0.75, 0.50, 0.25, 0.10, 0.03, ~0.009, →0**
(the owner's "75→50→25→10→3→0"). Applied as `est = (1-w)·established_level + w·par_prior`. Trust
basis stays on **seasons** (unchanged). Jamarra (n=3) is not touched by Fix 3.
