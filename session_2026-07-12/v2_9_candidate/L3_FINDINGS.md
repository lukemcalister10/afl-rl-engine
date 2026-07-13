# L3 — AGE(A) s(age) adoption + the G-COHORT gate · 2026-07-12

## L3a — s(age) wiring, executed + verified (read-only sim)
Adopts the l7hinr up-side breakout-persistence slope (option A): replaces the flat `S_M1=0.46` in
`_coreM1`'s proven-riser up-branch (`_merged_recover.py:225`) with `clip(s_age(age),0,1)` — the
`s_clip` table (age 20:0.915 · 22:0.789 · 25:0.490 · 27:0.266 · 29:0.027 · 30+:0.0), crossing 0.46
at ~25.3. Patched in the source string (`scripts/l3_age_sim.py`); the permanent `RL_AGE` lever
(default 0) rides the refit. To ship in the candidate it needs the cohort gate (below) + it is
GATED per the ruling.

**Reproduces the l7hinr research to the number:**
| metric | l7hinr research | this sim |
|---|---|---|
| movers | 43/46 risers, 20 up / 23 dn | **43 (20 up / 23 dn)** |
| net delta | +1675 | **+1670** |
| top risers | wilmot +460 · callaghan +367 · bowey +315 · berry +214 · macdonald +199 | **+460 · +366 · +314 · +214 · +198** |
| **Butters (G-PEAK margin)** | −1.0% | **6060 → 5997 (−1.04%)** |

**Butters holds:** −1.04% is inside the G-PEAK ≤2% drop tolerance (~0.96pp slack) — the narrowest
guard margin, watched per the directive. Anchors bont/gawn/darcy byte-identical (they don't fire the
up-branch). Old-name drops as researched (xerri −160). max-holmes +2.95% (young riser).

## L3b — the walk-forward G-COHORT re-measure (the GATE) — DELTA measured; absolute needs reconciliation
`scripts/l3_cohort_gate.py`: class-SUM construction (owner-worded G-COHORT — NOT per-capita) on the
sanctioned `value_asof` walk-forward pricer (`_p3_cohort_v6`, scoring truncated ≤ draft+t, leak-free,
inactive→0). Classes = ND picks 2014-2020; denom = min(avg t1, avg t2); years 4/5/6 vs 130%.

| construction | t4 | t5 | t6 |
|---|---|---|---|
| base (this harness) | 137.8% | 139.9% | 144.8% |
| **+ L3 s(age)** | **140.1%** | **141.7%** | **146.3%** |
| **Δ (L3 spend)** | **+2.3 pt** | **+1.8 pt** | **+1.5 pt** |

**L3's measured effect: it SPENDS ~+2.3 pt of year-4 cohort margin** (young proven risers up, the
year-1/2 denominator flat) — exactly the synthesis's "age-(A) SPENDS cohort margin".

⚠️ **ABSOLUTE-LEVEL RECONCILIATION REQUIRED (do not certify PASS/BREACH on this harness yet).** My
baseline reads t4 = **137.8%**, but the banked discount sweep states the y4 margin is **1.4 pt at
15%** (⇒ y4 ≈ **128.6%**) — a ~9 pt disagreement. So this ad-hoc class-sum construction differs from
the project's official G-COHORT harness in some convention (sample set / indexing / de-survivoring /
denominator / the walk-forward book it prices from — likely the s4_matrix backtest path, not a
per-player `value_asof` loop). The **Δ** is robust (same construction both arms); the **absolute
verdict is not** until the harness is reconciled to the audited one.

**What the numbers imply once reconciled (using the sweep's official baseline):**
- L3 at dial 15: 128.6% + 2.3 ≈ **130.9%** → marginal breach.
- Dial-14 **ADDS** margin (sweep: y4 margin widens 1.4→8.6 pt over 15→12; ~+2.4 pt at 14) →
  combined L3+dial-14 ≈ 128.6% − 2.4 + 2.3 ≈ **128.5%** → **holds**.
- This is exactly why they are ONE candidate: L3 spends, the dial adds, and the gate must be run on
  the FULLY-COMBINED world (L1+L4+L2+L3) on the reconciled harness — the definitive "run once" gate.

**Butters** (the −1.0% margin the directive flagged) holds independently at −1.04% (§L3a, inside
G-PEAK 2%). **Checkpoint:** the continuation seat reconciles the G-COHORT harness to the audited
s4_matrix walk-forward, then runs the one combined-candidate gate. L3a (the wiring) is done + verified.
