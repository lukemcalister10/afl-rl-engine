# D1 — ATTRIBUTION OF JAMARRA UGLE-HAGAN 1009 → 187 (term by term)

**Board of record measured:** `3dc19fbb` (store `340a7a32`, engine `2030e5df`) — the ITEM-20
successor to the v2.9-tagged board `81e48293` (store `b0c39d78`). Per the boot note ITEM 20 moved
`81e48293 → 3dc19fbb` with **bramble (+1)** the only value mover; Jamarra is byte-identical between
the two. Baseline rebuilt twice, byte-identical (`3dc19fbb == 3dc19fbb == committed`), panel PASS 10/10.

## The transition
Jamarra record: `2021:5g@47.0 · 2022:17g@44.0 · 2023:23g@60.6 · 2024:22g@63.8 · 2025:DNP · 2026:3g@26.0`.
- **BEFORE** (67 career games, no 2026 cameo): **ev/F = 1009**
- **AFTER** (70 career games, +2026 3g@26.0): **ev/F = 187**  (raw ev 1062 → 197)

## Term-by-term (all measured, not inferred)

| quantity            | BEFORE (67g) | AFTER (70g) | moved? |
|---------------------|-------------:|------------:|--------|
| `_nqual`            | 3            | 3           | **NO — never crosses PROVEN_N=4** |
| `_par_prior` (pedigree) | 66.18    | 66.18       | **NO — unchanged** |
| `_lvlcurr` (recency level) | **61.21** | **48.75** | **YES −12.46 (−20%)** |
| `_coreM1` (=0.75·Lc+0.25·par) | 62.45 | 53.11    | −9.34 |
| `_inferM1` (final level, eo-faded) | 61.26 | 48.75 | −12.51 |
| **ev/F**            | **1009**     | **187**     | **−822 (−81%)** |

## Verdict on the supervisor's attribution: **CORRECT on mechanism.**
1. `_nqual` is 3 before and after → the nqual cliff and the vanishing-pedigree formula switch
   **never fire for him**. `_par_prior` is 66.18 both sides — the pedigree term does not move. ✔
2. The entire collapse is **`_lvlcurr`**, which has **no small-sample damping**. Decay-weight shares
   (KEY decay ld=0.40, Y=2026):

   | season | games@avg | decay ld^(Y-yr) | weight | share (AFTER) |
   |--------|-----------|-----------------|-------:|--------------:|
   | 2021   | 5@47.0    | 0.0102          | 0.051  | 0.6% |
   | 2022   | 17@44.0   | 0.0256          | 0.435  | 5.1% |
   | 2023   | 23@60.6   | 0.0640          | 1.472  | 17.4% |
   | 2024   | 22@63.8   | 0.1600 (decayed **twice** — 2025 gap) | 3.520 | 41.5% |
   | 2026   | **3@26.0**| 1.0000          | 3.000  | **35.4%** |

   Three cameo games at 26.0 carry **35.4%** of his entire level weight (full decay weight 1.0 vs
   2024's 0.16), pulling `_lvlcurr` 61.21 → 48.75. Supervisor's "~35% / 61.2 → 48.8" is exact. ✔

3. **Amplification (the −20% level move → −81% value move):** the value curve is steeply convex where
   his level lands (near the KEY_FWD replacement bar 66.8). Measured ev/F(level) for Jamarra:
   L=48.75→ev/F≈172, L=52→400, L=55→493, L=61→927. A near-cliff sits between L≈49 and L≈52. His level
   drop crosses it, so the modest level move is amplified ~4–5× into the value collapse.

## THE ONE CORRECTION TO THE DIRECTIVE (verified, load-bearing)
The directive locates Fix 2 in **`_lvl_eff_core`** (line ~129, the `FLAT_TOL_G = {KEY:10.3…}` step).
**That function is DEAD.** `_lvl_eff_core`/`_lvl_eff_infer` are dormant twins; the live bind is
`cp._lvl_eff = _inferM1 → _coreM1` (line 287). `FLAT_TOL_G` is referenced ONLY inside the dead
`_lvl_eff_core`. The **live** established up-branch is `_coreM1` line 244:
`if Lc>=Lo: return (Lo+S·(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq) else Lo` — a hard step at
**TOL_M1 = 5.0** (uniform, not 10.3/12/14), plus a boolean `_radq` gate. Fix 1 (`_lvlcurr`) and Fix 3
(the n≥PROVEN_N formula switch) ARE on the live path and correctly located; only Fix 2's line
reference and per-group constants describe the dead twin. All three fixes in this session are applied
to the **live** `_lvlcurr`/`_coreM1`.
