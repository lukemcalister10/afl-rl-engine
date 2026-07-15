# FINDING — Form-Conditioned Aging (Tier 3, READ-ONLY, MEASUREMENT ONLY)

Base `9be07b8e` STRICT · Guard 5 store `b1fd0bce` PASS · engine_head `fc7045d6` · board `790136a3`.
All re-derived from the committed store (`base_store_rl_model_data.json`, md5 `b1fd0bce`, byte-copy of the
base). No engine import; the level basis is a **validated** replica of the engine's own `_lvlcurr`
(Heeney @2025 = 109.5, exactly the "playing 109.5" stated in register item 128). Definitions per PLAN.md.

## THE QUESTION
Among players aged 29–36 whose **demonstrated form to date is flat-or-rising** (no material decline yet),
how fast/hard does decline arrive next season — and does it arrive **measurably slower** than for the age
cohort as a whole? Motivators: Gawn (35), Bontempelli (31). Engine crux: the UP-arm forward carry `_S_AGE`
is **0 at age 30+** (a 30+ player's demonstrated rise carries forward at fraction zero). The UNCONDITIONAL
30+ residual is statistically zero (item 127, R102.2). The **conditional** version — this job — was open.

## HEADLINE
**Conditioning on flat-or-rising form to date does NOT buy slower decline at 30+. It is robust across every
definition tried.** A flat-or-rising 30+ player faces roughly a **coin-flip** chance of a material
demonstrated-level decline the *very next* season, with mean ΔLc ≈ **−4 SuperCoach points** — statistically
**indistinguishable from, and if anything slightly worse than, the age cohort as a whole.** The engine's
`_S_AGE` 30+ zero and its `_agemult` decline path are therefore **broadly validated conditionally**, not
just unconditionally.

## THE NUMBERS (primary spec: Lc basis, ε=3.0=DOWN_TOL, G_Q≥8, ≥3 prior qual, trailing-2 non-decline)

Two censoring bounds are reported at every age (survivorship is the central threat — the worst faders exit
before we see their decline season): **H_lower** = DECLINE/(CONTINUE+DECLINE) (survivor-only, biased low);
**H_upper** = (DECLINE+GENUINE_EXIT)/(…) (exit-treated-as-decline, biased high). Truth sits between.

| age band | set | n played | H_lower | H_upper | mean ΔLc |
|---|---|---|---|---|---|
| 29 | conditioned | 110 | 0.509 | 0.565 | −3.09 |
| 30–32 | conditioned | 121 | 0.521 | 0.605 | −3.65 |
| 33–36 *(thin, pooled, declared)* | conditioned | **12** | 0.750 | 0.833 | −8.25 |
| **30+** | **conditioned** | **133** | **0.541** | **0.630** | **−4.06** |
| **30+** | **unconditioned cohort** | **392** | **0.513** | **0.646** | **−3.12** |
| 30+ | already-declining (contrast) | 259 | 0.498 | 0.653 | −2.64 |

- **No slowdown.** Conditioned − unconditioned H_lower = **+0.029** (conditioned declines slightly *more*).
  Per-age smoothed (Gaussian kernel, bw=1.5 age-yrs, weighted by n): conditioned H_lower rises 0.51→0.52→
  0.54 across 29→32 and to ~0.63–0.69 through 33–36, tracking **at or above** the cohort at every age.
- **Robustness (11 variants, `sensitivity.csv`):** `H_lower(cond) − H_lower(unc)` is **positive in all 11**
  (+0.004 … +0.068) — conditioning rule (last-step / trailing-2 / never-below-peak / strictly-rising),
  noise band (ε=2/3/5/relative-4%), qualifying bar (6/8/10), min prior seasons (2/3/4). The result does not
  depend on any definitional choice.
- **Implied runway:** at the smoothed conditional hazard, a flat-or-rising 30-yo has **~2 seasons** expected
  to first material demonstrated decline, and **P(surviving 30→31→32→33 with no material decline) ≈ 0.11.**
- **Why not lower (survivorship) — checked:** genuine career-end exits after a flat-or-rising 30+ season
  number 32 (of 133), 5 of them from a still-elite level (`Lc ≥ REPL+15`, most likely non-form/voluntary).
  The H_upper bound already loads those exits as declines; even so the cohort and conditioned bounds
  overlap. Survivorship does not rescue a "safe veteran" story.

### Persistence (engine-facing `_S_AGE` translation)
For flat/rising seasons carrying a lift above the banked record, realized carry `ŝ = (L_fwd − Lo)/(Lc − Lo)`
(Lo = re-derived career games-weighted banked level; declared — it runs a few pts below the engine's
`_lvl_eff_orig`, so treat `ŝ` **directionally / by age-pattern**, not as an absolute vs 0.379): age-29
`ŝ ≈ 0.17`, age 30–31 `ŝ ≈ 0.15–0.25` (thin), age 32+ noisy around zero/negative. **The age-pattern the
engine already wired — a positive age-29 tail fading to ~nil at 30+ — survives the conditioning.** The
conditional data gives **no basis to lift the 30+ carry above zero.**

## COMPARISON TO THE ENGINE'S CURRENT AGE PATH
- **`_S_AGE` (UP-arm carry): 29→0.379, 30+→0.0.** Conditionally re-validated: the 30+ zero is not
  overturned; the age-29 positive tail is reproduced (small-positive here on a different, lower banked base).
- **`_agemult` (DOWN-arm decline mult): 0.73@30 → 0.68@32 → 0.62@34.** Consistent with the observed conditional
  ΔLc ≈ −4 pts on a ~110–125 demonstrated level (≈ −3.5%/yr) accelerating past 33; the engine is **not**
  over-shedding the flat/rising elders relative to what they actually do as a class.
- **Net:** the measurement gives **no evidence** that the current age path is too harsh on no-decline-yet
  30+ players. If anything it is mildly generous on the survivor-only view. **No wiring is implied** — owner rules.

## WORKED EXAMPLES (`worked_examples.csv`, `fig_worked_examples.png`)
All five are **right-censored** — their only in-window season is 2025 and 2026 is a partial, in-progress
season (shown as "so-far" annotation only). The class-conditional estimate for each man's 2026 age is
overlaid.
- **Max Gawn (RUC, 35 in 2026):** Lc 106→124→127 (2023–25), demonstrated 125.9. Class says age-33+ pooled
  E[ΔLc]≈−6.8, H_lower≈0.68. **His 2026 partial (~127) is currently BEATING the class expectation.** In the
  panel his 2023→24 and 2024→25 transitions both CONTINUED (+11.9, +5.5) — a genuine persister to date.
- **Marcus Bontempelli (MID, 31):** demonstrated 128.8, sustained flat/rising; his one in-window transition
  (2024, age 29) CONTINUED (+4.4). Class at 31: E[ΔLc]≈−3.5, H_lower≈0.52. 2026 partial ~119 (a touch soft).
- **Tim English (RUC, 29):** demonstrated ~110, rising; class at 29 E[ΔLc]≈−3.3, H_lower≈0.51. 2026 ~99.
- **Isaac Heeney (MID, 30):** demonstrated 109.5; class at 30 E[ΔLc]≈−3.4, H_lower≈0.51. **2026 partial (~124)
  is BEATING the class expectation** (the item-127 age-29 persister, now 30).
- **Bailey Dale (GDEF, 29):** demonstrated 100.9, rising; class E[ΔLc]≈−3.4. 2026 ~99 (near expectation).
The persister tail is real (Gawn, Heeney live in it right now) — but it does not move the **class** average,
and it cannot be read off the class curve for any single man.

## PRIOR ART (branch `claude/form-conditioned-aging-decline-5hi0xe`, read-only; NOT reused)
**What it is:** the origin of the engine's DOWN-arm `_agemult2`/`_fbump` decliner-shed (session_2026-07-06,
"PR #45"), **already folded into the base engine** at `_merged_recover.py:138`. It fits, for the
**already-declining** shed population (`nq≥PROVEN_N & Lo−Lc>DOWN_TOL`, 2369 player-seasons), the realized
forward multiplier `r = L_fwd/Lc` as a 2-D surface in (age, level-above-replacement `lcr`) — a still-elite
elder who dips sheds ~0.90 of forward, a faded one ~0.11.
**Is it sound?** Yes, for what it does: NW 2-D smoothing with adaptive bw (eff-n≥35/node, all nodes ≥40),
isotonic-monotone (non-decreasing in `lcr`, non-increasing in age), up-only (never sheds *more* than the
age baseline), `lcr≤0` hard-zeroed, kill-switch `RL_FORMDECL=0` byte-exact — and crucially its `r` is
**washout-inclusive** (a non-played forward season counts 0), so it already absorbs survivorship on the
down arm. Construction verified in its DERIVATION and reproduced in the engine comment.
**Why it is NOT this job's answer:** it conditions the **DOWN arm** (players *already* declining — how much
output remains, given how elite they still are). The owner's question is the **UP arm** (players *not*
declining yet — how soon decline *arrives*). Different population, different outcome. Its conclusions were
**not reused**; everything here is re-derived from the committed store, on a different (flat-or-rising)
population, with an independent censoring treatment.

## THREATS / LIMITS (declared)
- **Survivorship ↔ mean-reversion** pull in opposite directions; handled by the H_lower/H_upper bracket and
  by using the smoothed demonstrated level Lc (not a single-season spike — the naive single-season cut
  *inverts* to conditioned-worse via pure regression-to-the-mean; that is an artifact, not the finding).
- **33–36 is thin** (conditioned n≈12) → pooled deliberately and declared; the smoothed curve borrows
  strength but the per-age raw points at 34–35 (n≤3) are not read individually.
- **Right-censoring** of the current elders (Gawn/Bont/Heeney/English/Dale): their 2026 is incomplete →
  excluded from the event counts, reported as "so-far" only. The class result is not an individual verdict.
- **CIs are cluster-bootstrapped by player** (1000 reps) to respect repeat player-seasons.
- Position **pooled** (RUC/ruck thinnest — Gawn/English); banked level re-derived (declared, runs low).
