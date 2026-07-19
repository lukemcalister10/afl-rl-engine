# LEG F3 — CHECKPOINT 2 (granted-scope fix implemented + measured; acceptance NOT reachable in scope) · 2026-07-18
**Per ruling item 353 point (2): "if any required edit falls inside [the V0/_iso_dec chain :1121-1171], HALT
again." It does. This is that HALT — with the granted-scope fix built, k=0 byte-exact, and the residual
driver measured and attributed. Nothing bent; no cohort hand-tuned.**

## WHAT WAS BUILT (all four granted sites, ruling 353; RL_LEGF=0, single-thread, container 06d8af60-faithful)
`_merged_recover.py`, forward-lens-gated (MA._LENS_FORM set) so **k=0 identical BY CONSTRUCTION**:
1. `_form_anchor_clock()` + `_fa_year()` — evaluate the pedigree/tenure clocks at the FORM ANCHOR (BASE_REF)
   in the forward lens; no-op at k=0/balanced/backward.
2. **pedigree-fade decay** — `_par_prior` tenure re-keyed on BASE_REF (the `pw·par` pedigree term in `_coreM1`).
3. **staleness block** — `ev`'s `el=PR.tenure` re-keyed on BASE_REF (developing picks not relabeled "stalled").
4. **PR.tenure clock keying** — via `_fa_year(Y)` (BASE_REF year-arg) at every pedigree/tenure site; and the
   `raw_ev` pedigree-pole fade (`wage`/`tfade`).
5. **proj_from_peak (`_proj_w4`, ruling pt 4 "still implicated")** — the horizon age-shape + young-runway
   credit form-anchored (`ah=a-offset`); growth flows through the advancing level/`_dev_advance`. Reid: same
   map at the projected evidence state, no new multiplier / lens-only growth term.

## MEASURED RESULT (board ground-truth, not the probe)
- **k=0 balanced `RL_LEGE=0` = `06d8af60` — BYTE-EXACT** (pristine==edited, 2/2 + 3/3 pristine). The edits are
  provably dormant at k=0 (clock identity). Backward lens byte-exact by the same construction.
- Forward (composition-controlled, 804 roster), now-total Sv=752,427:

| cohort | pristine Δ% | **F3 fixed Δ%** | signed mean (fixed) |
|---|--:|--:|--:|
| total | −28.2% | **−23.7%** | — |
| developing ≤23 (n=375) | −30.5% | −26.6% | **−247** |
| mid 24–27 (n=210) | −24.1% | −18.4% | −206 |
| veteran ≥28 (n=219) | −29.1% | −25.0% | −193 |

Real, Reid-compliant improvement (+4.5pt total, +3.9pt developing). **But the two acceptance criteria are
NOT met:**
- **Gradient still INVERTED:** required developing ≥ mid ≥ veteran (developing least-negative). Measured signed
  means: developing −247 **<** mid −206 **<** veteran −193 — the exact inverse. Developing still declines MOST.
- **Backtest band:** total −23.7% vs the ~−9% symmetric expectation (backward on the identical roster is −9.0%);
  the −1→now projection would still undershoot ±5% of 752,427.

## RESIDUAL DRIVER — WHAT THE GRANTED FIX CLOSED, AND WHAT REMAINS (measured, board ground-truth)
The granted-scope fix DID lift the floored/mislabeled young rows OFF the floor (post-fix, board-verified):
Jagga Smith `vP1 972→2610` (was `0.28·v0` floored by the staleness gate; now `[prefloor]`=prod_path), Xavier
`597→1566`, Sam `3171→3240`. So the staleness re-keying (item 353 site 3/4) WORKS as intended — the
"155-mislabeled-exits" defect is cured on the forward side. **The residual is NOT the v0 floor (rows are now
above it) and NOT the band** (`RL_F3_EXP_BAND` form-anchoring `cp.cond_prior_band`+`cp._feat` = BYTE-IDENTICAL
board `c6d776ce`; reverted before commit — the band does not de-pedigree on the age clock).

**The residual is the `prod_path = raw_ev·iso = pr + pole` forward decline itself:** young pedigree still loses
~25–35% via `pr = price6(b6)` → `dp.v_at_peak` → `proj_from_peak` over the horizon (Jagga prod_path
3696→2610 −29%, Jed 1380→878 −36%, Nate 1876→1249 −33%). `proj_from_peak` (site 5, V2 age-shape anchor) closed
~4pt of it; the rest sits in the price6/`v_at_peak` pricing of the (age-advanced) horizon — I could NOT fully
isolate the last term within the four granted sites (band excluded by measurement; proj partially addressed;
the remainder is in `dp.v_at_peak` / the posval nonlinearity, `distribution_pricing.py` — OUTSIDE the grant).
Honest statement: **I have not root-caused the last ~22pt to a single granted site; the granted sites,
correctly and fully applied, move the developing cohort −30.5%→−26.6% and no further.**

## THE TENSION (for the owner/supervisor)
The four granted sites, correctly applied (k=0 `06d8af60` byte-exact, RL_LEGF=0 chain byte-exact), soften the
collapse (total −28.2%→−23.7%, developing −30.5%→−26.6%, floored young rows recovered) but do NOT un-invert the
gradient or reach ±5%. The residual is the forward `prod_path` de-valuation of young pedigree, which lives in
the **`dp.v_at_peak` production pricing (`distribution_pricing.py`)** — outside the four granted sites and NOT
attributable to the band (measured inert) or the v0 floor (measured non-binding post-fix). I will NOT bend Reid
or hand-tune the developing cohort to force ±5% (CHECKPOINT LAW).

**Returning the partial (real, k=0 byte-exact, Reid-compliant) + this measured tension for a scope ruling.
Options:**
- **(a)** grant `dp.v_at_peak` / the forward pricing as a site: carry the pedigree/evidence blend through the
  horizon pricing at the projected-evidence state (form-anchor the pricing-side age where it de-pedigrees),
  φ(games)-decayed. I'll validate against ±5% + the gradient if granted.
- **(b)** grant a forward-lens-only, evidence-decayed pedigree-carry FLOOR at the form anchor (rl_export:96,
  IN the original fence): `vP_k = max(vP_k, φ(games)·v_now)`, φ=(1−g/G0)² — re-supplies the pedigree anchor at
  +k (the findings' exact language), smooth in games, inert for evidence-complete rows (φ→0 ⇒ byte-exact),
  k=0-safe (φ≤1 ⇒ max is a no-op at k=0). This is the most direct §2.vi reading and needs no HARD-OUT edit; I
  can implement + validate immediately if granted.
- **(c)** accept the measured partial as F3's landing (+4.5pt, floored-rows cured, k=0 byte-exact) and re-scope
  the v_at_peak remainder to a dedicated build.

I recommend **(b)** — it is the cleanest, in-fence, Reid-defensible closure; I have the harness staged to
validate ±5% + the un-inverted gradient the moment it is granted.
