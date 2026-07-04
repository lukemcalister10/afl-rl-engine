# GROWTH-CURVE VALIDATION — FINDINGS

**Evidence 1/3 for the V0/PVC overhaul · read-only diagnostic · 2026-07-04**
**All numbers state-labelled `[BAKED c47cb43d]`. No engine change, no bake, no derivation committed to the engine.**

## STEP 0 — assert (PASS)

```
origin/main = 389ac39            (expect 389ac39)      PASS
HEAD        = 389ac39
md5(engine/rl_after/_merged_recover.py) = c47cb43d  (isolated subprocess)   PASS
board sanity: Nick Daicos 7013 / Max Gawn 2120 reproduce   PASS (engine is live at baked state)
```

## The question

Does the age / production growth-curve **shape** the baked engine *assumes* match what players
**realised** on the baked walk-forward history? Which ages are over-/under-priced, and is any
divergence a **shape** problem (peak location / decline steepness) the overhaul must re-derive?

## What the engine assumes (Section A, constants)

The baked engine layers several age surfaces onto the forward valuation:

| surface | role | shape `[BAKED c47cb43d]` |
|---|---|---|
| `PEAK_AGE[pos]` | vertex of the value curve | MID 25 · GEN_FWD 25 · GEN_DEF 26 · KEY_DEF/KEY_FWD/RUC 27 |
| `DELTAS` / `frac(a-peak)` | fraction-of-peak **value** by (age−peak) | +0→1.00, +5→0.91, +8→0.79, +11→0.58, +14→0.34 |
| `AGE_CURVE[pos][age]` | per-position fraction-of-peak **production** | MID: 24→1.00, 30→0.86, 34→0.67 |
| `_AGEMULT(age)` | decliner shed (realised-fwd/current) | 20→0.92 … 30→0.73 … 37→0.55 |
| `wage=clip(1-(a-20)/6,0,1)` | upside/pole credit weight | 1.0@20 → 0.0@26 (linear) |
| `_v7 asc` | q97 tail age-scale (REAL players) | 1.00@20, 0.76@22, 0.58@24, 0.40@27 |

## Method — the two traps, addressed in writing

**(a) SURVIVORSHIP.** Players who leave the league are absent from late-age buckets, so a *raw*
realised-by-age curve is biased **up** at old ages (only good old players remain). Section C
quantifies it on fully-resolved 2009–2016 cohorts: at age 27 the survivor mean is **77.7** SC-avg
but the cohort-complete mean (washouts retained as 0) is **32.7** — a **2.4× gap**, with only
**42% of the cohort still active**. Reading "the engine under-prices old age" off the survivor
curve would be the trap. **The headline read is therefore the *matched* residual
(predicted−realised on the SAME rows):** predicted is computed on the identical survivor set as
realised, so the survivor bias cancels. We also excluded **6,608 post-career observations** (years
after a player's last active season, where the band still prices frozen history while realised=0 —
these spuriously inflated the old-age residual by +30 SC in the first pass) and added a
**horizon≥5** cut that decouples age from forward-window length (older age ⟺ later Y ⟺ shorter
window). The tilt reproduces under both controls.

**(b) VALUE ≠ SCORING.** Kept as two separate residuals, never mixed: a **PRODUCTION** residual
(engine central forward-best3 projection vs realised forward best-3, SC-avg units) and a **VALUE**
residual (band priced to value vs realised production priced on the engine's own `v_at_peak`
ladder, at the matched evaluation age). **Crucially, the value residual's *level* is not
mispricing:** at age 25 the production residual is **0.01** (calibrated) yet the value residual is
**+209** — that +209 is pure band-optionality (E[v(band)] > v(point) under the convex value
function; young bands are wider ⇒ larger gap). So the calibration verdict is anchored on the
**production** residual; the value residual is read only for *shape*, not level.

## Headline — smoothed residual by age (matched, survivorship-robust, horizon≥5) `[BAKED c47cb43d]`

Sign: residual = predicted − realised. **+ = engine over-projects; − = under-projects.**

```
age       19    20    21    22    23    24    25    26    27    28    29    30    31    32    33    34    35
PROD res +3.2  +2.7  +2.1  +1.5  +0.9  +0.3  -0.3  -0.9  -1.6  -2.2  -3.0  -4.0  -5.2  -6.6  -8.2  -9.8 -11.5
eff-n   4118  4650  4572  4167  3681  3180  2694  2248  1846  1485  1167   887   641   437   281   169    94
```

- **Well-centred**: the production residual **crosses zero at ≈ age 25** — the engine's forward
  projection is unbiased *on average* at prime age. The growth curve is **not broken**.
- **Young end is modestly too generous**: +2 to +4 SC over-projection at ages 19–22 (≈ +5–6% on a
  ~70 base). This bucket has little selection yet (young ≈ full cohort) → survivorship-robust and
  representative. **This is the shape signal most relevant to V0/PVC, which sets young start values.**
- **Old-survivor end**: −4 to −13 SC under-projection at 30–35 — but this bucket is the elite
  survivor selection (eff-n collapses 887→94). It says a *single unconditional* age curve cannot
  credit elite survivors without over-crediting the (now-absent) washouts, not that the curve is
  simply "too steep."

## Anchor check (Section E) — modelled `ev` vs realised trajectory `[BAKED c47cb43d]`

Identity printed for name-collision guard:

| player | id | pos | pick/eff | cohort | `_by` | age2026 |
|---|---|---|---|---|---|---|
| Max Gawn | (printed) | RUC | 33/33 | 2009 | 1991 | 35 |
| Marcus Bontempelli | (printed) | MID | 4/4 | 2013 | 1995 | 31 |
| Isaac Heeney | (printed) | MID | 4/4 | 2014 | 1996 | 30 |

- **Gawn** — modelled `ev` rises 1010(20) → **5918(27, peak)** → 2120(35); realised forward best-3
  held elite ~126–132 throughout. **PASS**: shape agrees — the `ev` decline tracks the shrinking
  keeper runway, not a production collapse.
- **Bontempelli** — `ev` **6952(21, peak)** → 3085(31); realised fwd best-3 ~128 sustained. **PASS**.
- **Heeney** — `ev` 3360(19) → 5157(22) → dip 1346(27, after down 2021–23 seasons) → recover
  3301(30); realised fwd best-3 ~116–124. **PASS**: engine correctly tracked the mid-career dip and recovery.

All three agree on the **value-trajectory shape** (rise to a mid-20s peak, decline driven by
runway). The only visible divergence is that for these elite survivors the engine's forward
*production* projection sits slightly below their sustained realised output — the same
old-survivor effect as the residual, and it does **not** distort the value shape.

## Assumed value shape, isolated (Section D) `[BAKED c47cb43d]`

Holding demonstrated level fixed and advancing only the age clock, the engine's assumed
**keeper-value** curve is **monotonically decreasing in age** (e.g. MID normalised: 100@20, 67@25,
38@30). This is **correct and is value≠scoring in action**: keeper value integrates the *remaining*
career, so a younger player at the same demonstrated level is worth more (runway) even though the
*production* curve (`AGE_CURVE`) peaks at 24–27. Do not confuse the two.

## SHAPE VERDICT — what the overhaul must re-derive

1. **Peak location: essentially right.** Production residual zero-crosses at ≈25; `PEAK_AGE`
   (25 for MID, 26–27 elsewhere) is defensible. **Not the priority.**
2. **Young-end slope: modestly too generous — re-derive.** The engine over-projects forward
   production for 19–22-year-olds by ~+3–4 SC (~5–6%). Because value is runway-amplified at the
   young end, this is exactly where the growth curve feeds the V0/PVC start values the overhaul is
   re-deriving. **Highest-leverage finding for the overhaul.**
3. **Decline is unconditional — the structural limitation.** A single age multiplier cannot serve
   both elite survivors (under-credited at 30+) and washouts (over-credited, seen once post-career
   contamination is removed). The overhaul should consider a decline **conditioned on demonstrated
   level / retention**, not a flat age curve. Lower leverage (small n; value is runway-dominated at
   old age anyway).
4. **Do not re-tune off the value residual's level** — it is dominated by band optionality
   (+209 at calibrated-production age 25). Tune the growth curve off the **production** residual.

**Bottom line:** the growth curve's shape is **broadly right** (calibrated at prime, peak roughly
correct), with one actionable shape defect for the overhaul — a **~5–6% young-age over-optimism in
forward production** that propagates into young start values — plus a structural note that the
old-age decline needs survival-conditioning rather than a single unconditional multiplier.

## Files (re-runnable)

| file | contents |
|---|---|
| `growth_curve_validation.py` | the full diagnostic (READ-ONLY on engine/data; run instructions in header) |
| `growth_curve_report.txt` | full printed report (all sections) |
| `wf_frame.csv` | walk-forward observation frame, one row per (player, Y) |
| `residual_by_age.csv` | smoothed residual-by-age curves + eff-n (production & value) |
| `assumed_vs_realised.csv` | assumed value shape (age-sweep) per position |
| `anchors.csv` | Gawn / Bontempelli / Heeney modelled-vs-realised trajectories |

**Reproduce:** `cd /home/claude/rl_workspace/rl_after` with the panel env
(`PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22`,
`PYTHONPATH=…/rl_after:…/rl_vendor`), then
`python3 <repo>/evidence/growth_curve/growth_curve_validation.py`. Engine dir overridable via
`RL_AFTER=…`, output dir via `GC_OUT=…`.
