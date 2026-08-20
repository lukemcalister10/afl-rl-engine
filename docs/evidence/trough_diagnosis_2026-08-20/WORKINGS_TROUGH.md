# THE THIN-EVIDENCE SCORE TROUGH — MECHANISM SITE IDENTIFIED

Read-only diagnosis. No build lock, no board build, no write to `/home/user/afl-rl-engine`.
Engine loaded in-process against a scratch copy (`ws_r23/` = a copy of `engine/rl_after`,
`repo_r23/` = a symlink-only scratch repo root), exactly as `probe3.py` does. Load: **53.7 s**
(the originating seat's 35-minute stalls were box contention, not the load).
Store `b745002e`, season state as_of_round 23 / calendar_progress 0.96 — the shipped R23 side.
Every sweep restores the row and re-asserts the shipped price (`rt=True` on all 100+ rows swept).

---

## 1 · THE ANSWER IN ONE LINE

The price of a thin-evidence player is, essentially, a **weighted sum of six numbers read off a
frozen gradient-boosted forest** — and that forest is a **step function of his level, with steps in
both directions**. Kondogiannis's 71 pushed his level feature across a run of *downward* steps in
the top of that band. Nothing evaluated his 71 and decided it was bad. He fell off a stair.

## 2 · THE SITE

```
engine/rl_after/_merged_recover.py:936     raw_ev()      _bb = b6(p,Y);  pr = price6(p,_bb,Y)
engine/rl_after/_merged_recover.py:374-383 b6()
engine/rl_after/_merged_recover.py:370-372 _b6_core()    b = cp.cond_prior_band(p, cm, Y)
                                                          return np.append(b, max(q97m.predict(cp._feat(p,Y)), b[4]))
engine/forward_valuation/conditional_prior.py:164-167     <== THE SITE
        def cond_prior_band(p, models, Y=None):
            f = np.array([_feat(p,Y)])
            return np.sort(np.array([float(models[q].predict(f)[0]) for q in Q]))
engine/rl_after/_merged_recover.py:385-390 price6()   SCALE_DIST * WQ6 · [dp.v_at_peak(p, L) for L in bb]
engine/rl_after/_merged_recover.py:96      WQ6 = [0.18]*5 + [0.10], normalised
```

`models` is `cm`, built at `conditional_prior.py:143-162`:

```
models = {q: GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=400, max_depth=4,
                                       learning_rate=0.05, min_samples_leaf=25, random_state=0).fit(X,y)
          for q in Q}                                  Q = [0.1, 0.3, 0.5, 0.7, 0.9]
```

shipped as the pinned forest `/home/claude/cm_400.pkl` (md5 `34faa865`, Guard-5 asserted;
`wire_redesign.py:43-63`, "not byte-reproducible by a fresh fit"). `q97m` is the sixth, same shape,
frozen at `data/q97m.pkl`.

**A gradient-boosted forest is a sum of regression trees. Its output is piecewise constant in every
input, and it carries no monotonicity constraint** (`monotonic_cst` is not passed at the fit site).
Measured on the shipped forest, on feature index 9 — the level, `cp._feat(p,Y)[9]` =
`cp._lvl_eff(p,Y)`:

| model | distinct split thresholds on the level feature | range |
|---|---|---|
| q0.1 | 253 | 40.75 – 114.32 |
| q0.3 | 394 | 40.75 – 116.15 |
| q0.5 | 617 | 40.75 – 116.26 |
| q0.7 | 632 | 41.14 – 116.15 |
| q0.9 | 520 | 42.10 – 116.20 |
| q97m | 292 | 44.12 – 116.26 |

That is the piecewise-constant lookup §6a was hunting. It is **the band itself**.

### The secondary (minor) step site, for completeness
`rl_model.py:1320` — `val = lambda r: round(SCALE*r**GAMMA) if r>0 else 0`. Each of the six
`v_at_peak` legs is rounded to a whole unit before `price6` weights it. Granularity ≈ 0.001–0.1
board points. It explains the residual sub-0.05 % wobble on the plateaus and nothing larger.

## 3 · WHY 71 < 40 FOR THESE ROWS — PLAIN LANGUAGE

The engine does not price a round's score. It prices a **band of futures** — six quantiles of "what
this player's peak could be" — and it looks that band up in a trained forest, keyed on his position,
pick, exposure, age and his **level**. One extra score changes only the level, by about a tenth of a
point of season average, which is about **0.04–0.08 of a unit** of the level feature.

The forest does not respond smoothly to that. It sits still for a stretch, then a tree split is
crossed and one of the six quantiles jumps by half a point or two points — **and the jump is as
likely to be down as up**, because nothing ever told the forest that more level must mean more
value. The top two legs of the band (p90 and the q97 tail) are where nearly all of the value is
(for Dolan the bottom two legs price at **zero** and the top leg at **1178**), so a −2 step in p90
or a −1.4 step in q97 is worth 8–12 % of the row.

Kondogiannis's 71 walked his level feature from 47.2 to 49.3 across a run of those steps in which
the band's upper tail **descends**: p90 87.43 → 82.92, q97 96.70 → 92.79. Price 386.8 → 324.3.
Score higher again (140) and he crosses the steps back up: 428.7.

**That is the whole mechanism.** Not the evidence weight, not the pedigree blend, not the parity
guard, not a band boundary in the ruled sense — the trained band surface's own roughness.

## 4 · MEASUREMENT — THE DECOMPOSITION AT THE KINKS

1-point score sweep, both anchored rows, full internals (`tasks/task_01_finesweep.*`). At every
material step the *only* discontinuous quantity is `bb`; everything upstream is smooth.

Kondogiannis, score 74 → 75 (avg 40.34 → 40.44):
```
lvl_eff      48.49797 -> 48.54539   (+0.047, smooth)      exposure  10.0 -> 10.0 (unmoved)
lvlcurr      40.34    -> 40.44      (+0.10,  smooth)      Eq/ev_rec/ev_est/ev_pw  all smooth
_h_cut        1.0     ->  1.0                             iso_eff    1.0 -> 1.0
ITEM A anchor share s = 0.0000 on BOTH sides (the anchor blend is inert for him)
bb   39.19 51.23 59.46 69.92 85.93 92.79
  -> 39.57 51.23 58.65 69.92 81.43 92.79      <== p50 -0.81, p90 -4.50  ON A RISING LEVEL
price6      318.14 -> 245.60   (-72.5, -22.8 %)
v_board     352.23 -> 339.36
```

Josh Dolan, score 40 → 42 (avg 49.081 → 49.281):
```
bb   44.61 52.80 59.33 63.20 75.22 80.52
  -> 44.61 52.80 58.58 63.20 72.54 80.52      <== p50 -0.75, p90 -2.68
price6      237.94 -> 196.36
v_board     261.19 -> 235.21
```

**Excluded, by measurement, at these steps:** the evidence weights `E_q / _ev_rec / _ev_est /
_ev_pw` (continuous, monotone), `_par_prior` (constant), `v0_start` / `entry_anchor` (constant),
`_h_cut` (1.0), `iso_eff` (1.0), the ITEM A anchor blend (`_a_share` = 0.0000 for every row probed,
so it is inert, not merely small), `nseas_pro` / `PR.tenure` (constant), the D8 and mediocre-for-
years staleness caps (branch `none` for both anchored rows), the year-zero floor (inert for both),
`o31_D` / the depth clock (1.0, and moves +0.0045 across the whole sweep), the D7/`RL_O43` parity
guard (not engaged), `_radq` and `o32_delivered` (already eliminated by §6a; confirmed False
throughout), `MA.prod_floor` (0.0 for Dolan; binds on no leg).

## 5 · THE PREDICTION TEST — THE EXACT RISER LOCATIONS

The site's formula gives the riser positions with no free parameters: the price changes across an
interval **iff** that interval contains a tree-split threshold on the level feature.

Run on §6a's own grid (Dolan, games fixed at 10, average 46.00 → 53.40 step 0.2). Breakpoints
located by bisection to 1e-9 **in average units**, from the band model alone — no `ev()` call —
then the true `ev()` run on the same grid (`tasks/task_08_exactkink.*`).

**56 breakpoints predicted in [46.00, 53.40]. Result: 30 of 37 grid steps predicted correctly.
All three named risers and all three named plateaus hit exactly:**

| §6a's observation | predicted from the band model | true `ev()` |
|---|---|---|
| avg 49.0 → 49.2 = **−24.2** | 3 breakpoints inside (49.0280 q97 −1.430 · 49.0391 q97 −0.466 · 49.1870 p90 −0.605) | **−24.163** |
| avg 49.2 → 49.4 = **−19.5** | 1 breakpoint (49.2069: p50 −0.750, p90 −2.076) | **−19.507** |
| avg 49.6 → 49.8 = **exact plateau** | no breakpoint | **bit-identical** (235.2416369028) |
| avg 49.8 → 50.0 = **+12.0** | 1 breakpoint (49.8780: p90 +1.342) | **+11.967** |
| avg 52.4 → 52.6 = **+30.5** | 3 breakpoints, dominant 52.4068: **q97 +3.144** | **+30.533** |
| avg 46.6/46.8/47.0 plateau | no breakpoint 46.6→46.8 | **bit-identical** (294.8031519805) |
| avg 48.0/48.2 plateau | (predicted a move; see below) | **bit-identical** (297.5779368357) |

The 7 misses are **all** sub-0.1-board-point (≤ 0.04 %) and of two known kinds: (a) predicted-move /
actually-identical, where the stepping quantile is one whose `v_at_peak` leg prices at 0 or is
absorbed by the `val()` rounding — e.g. the 46.921 breakpoint moves p30 by +0.116 but that leg's
`v_at_peak` is **0.000 on both sides**, so it cannot reach the price; (b) predicted-identical /
actually-moved by 0.001–0.100, the smooth residual from the player's own `level_now` inside
`v_at_peak`. **Every move larger than 0.1 board points in the whole sweep is predicted correctly.**

### Independent third-player prediction (written before the confirming sweep — `PREDICTION.md`)
Band-only predictor run blind over all 86 rows; Kondogiannis ranked **#2 of 86**, Dolan **#8**.
Named predictions and outcomes:

| player | predicted (band only) | true `ev()` | verdict |
|---|---|---|---|
| **Charlie West** (7 g, prior 32.33) | price at 110 ≥ 20 % below price at 59 (predicted 38.0 %) | **−28.5 %**, same score pair, corr(pred,true) = **1.000** | CONFIRMED |
| **Will Hayes** (8 g, prior 36.97) | price at 35 ≥ 20 % below price at 0 (predicted 43.0 %) | **−28.1 %**, corr = **1.000** | CONFIRMED |
| **Billy Cootee** (8 g, prior 47.71) | ≥ 25 % drop 7 → 15 | **1.1 %** | **FALSIFIED** — see below |
| controls: Herbert / Keane / Lalor / Day | max drop < 6 % | 0.0 / 2.9 / 0.7 / 0.7 % | CONFIRMED |

**Cootee is the informative failure and it sharpens the bound.** The live blend is ORDER 31
(`_merged_recover.py:5194-5199`): `price = rho31(g)·e + o31_pi(p,Y,g)·ped + age_credit`, where `e`
is the production leg that carries `price6`. Cootee's production leg is **10.1** against a pedigree
leg of ~140 — his **production share is 0.029**. The band can move his production leg by 50 % and
his price will not notice. So the band's roughness bites a row only in proportion to how much of
its price is production. That is a bound, and it is now measured rather than assumed.

## 6 · WHAT CLASS OF ROW IT BITES — MEASURED BOUNDS

True `ev()` sweeps, all **86** rows with 5–13 games in 2026 that played round 23 (the same 86 as
§6, reproduced exactly), score 0 → 150 (`tasks/task_05_class.*`, `tasks/task_10_owner_stat.*`):

**The owner's own question, counted:**
> **44 of the 86 (51.2 %) would have been priced HIGHER by some round-23 score LOWER than the one
> they actually made.** 24 of 86 (27.9 %) by more than 1 %; 7 of 86 (8.1 %) by more than 5 %;
> 4 of 86 (4.7 %) by more than 10 %.

```
Will Hayes       48 -> 180.0   a 4  would have priced 242.7   +34.8 %
Josh Dolan       48 -> 247.2   a 12 would have priced 300.7   +21.6 %
Jack Williams    44 -> 411.3   a 40 would have priced 461.4   +12.2 %
Max Kondogiannis 71 -> 358.9   a 40 would have priced 399.0   +11.2 %
Lachlan Gulbin   53 -> 234.3   a 10 would have priced 250.9    +7.1 %
Rhett Bazzo      64 -> 514.0   a 62 would have priced 542.7    +5.6 %
Bailey Macdonald 45 -> 106.1   a 16 would have priced 111.9    +5.4 %
```

Counterfactual depth (worst fall anywhere in the 0–150 sweep): 33 of 86 exceed 5 %, 16 exceed 10 %,
5 exceed 20 %. Median 3.2 %.

**The bound is the LEVEL, not the games count.**
```
corr(max-drop, level feature)   = -0.52   (log: -0.57)   <== the discriminator
corr(max-drop, prior average)   = -0.43
corr(max-drop, board value)     = -0.26
corr(max-drop, 2026 games)      = -0.08   (essentially none)
```
Every row bitten >10 % has a level feature below 70; the worst sit at **44–54**, which is exactly
where the forest's training rows are thinnest and its trees roughest. Rows with level ≥ 80 are
effectively immune (max-drop < 1 %). Position is not a factor; pick is not a factor.

So the class is: **rows whose level feature sits in roughly [42, 70], whose production share is
material (≳ 0.3), and whose season average moves enough per round to cross splits — i.e. thin-
evidence rows.** A 22-game veteran at level 90 is safe on all three counts simultaneously.

## 7 · LAW 3 (NO CLIFFS / L-SMOOTH) — VERDICT

> **3. NO CLIFFS (L-SMOOTH).** Value moves smoothly across age, evidence, and position;
> no wide-bin jumps, no discontinuities a player could fall off. — `docs/RULEBOOK.md:13-14`

**This is a law-3 violation, not a quirk.** Stated with the grounds:

1. **It is a genuine discontinuity, not a steep smooth curve.** Bit-identical prices across distinct
   inputs, with 8–12 % risers between them, reproduced to the last digit and predicted in advance
   from the tree thresholds. §6a established the plateaus; §5 above establishes they are exactly the
   intervals between splits in a piecewise-constant forest.
2. **It is on the evidence axis, which law 3 names explicitly.** The level feature *is* the evidence
   channel. A single round's score is the smallest evidence increment the board can receive, and it
   moves a player by up to 12 % in the wrong direction.
3. **It is a discontinuity a player can fall off.** Dolan sits at 247.2 — 12 points above the 235.2
   floor of a two-step cliff and 12 below the recovery. Kondogiannis's shipped price is inside the
   descending run.
4. **The engine has already ruled on the identical defect on the sibling axis.** `_prod_path`
   (`_merged_recover.py:2944-2962`) declares in its own docstring: *"the band prior is a stepwise
   (GBR) surface whose exposure-axis steps (measured +957 in one game on the B6 synth) … leave the
   evidence ramp non-monotone (B6 law: more games at the same rate never worth less)"* — and
   installs a 3-point moving average to fix it, **on the games axis only, and only for the
   first-evidence family**. The same surface, the same defect, one axis over, unsmoothed and
   unrestricted. The law that was applied there applies here.
5. It is not a rounding artefact and not a board-advance artefact: it reproduces at fixed store,
   fixed season state, fixed everything but the one score.

What it is *not*: it is not a designed penalty, and it is not evidence of anything wrong with the
level estimate, the evidence weights, the pedigree blend or the parity guard — all measured
smooth and all excluded.

## 8 · IS A PRINCIPLED FIX VISIBLE — YES, TWO, AND THEY DIFFER IN CEREMONY

The principle is already written in this engine's own words: **"more … at the same rate never worth
less"** (the B6 law, `_prod_path`). It is stated for games. It must equally hold for level. Both
options below enforce exactly that and change nothing else.

### FIX 1 — constrain the forest at the fit (the clean one)
`conditional_prior.py:160-161` — pass sklearn's `monotonic_cst` with `+1` on feature 9 to all five
quantile fits, and the same at `refit_q97m.py`. "More demonstrated level is never worth less"
becomes true **by construction**, for every row, permanently.
*Ceremony:* this is a **refit of a pinned, Guard-5-asserted frozen artifact** (`cm_400.pkl`,
`q97m.pkl`, and by dependency the v0 surface). `wire_redesign.build()` states the cache is *"not
byte-reproducible by a fresh fit"*. That is a bake, a re-pin, a re-stamp of `expected_boot.json`,
and a full re-certification — the same ceremony the q97m and v0surf freezes already carry. Blast
radius is the whole board and is **not** bounded by anything measured here.

### FIX 2 — monotonise at the read site (the one this seat can bound)
`_b6_core` (`_merged_recover.py:370-372`) — re-apply the house isotonic instrument along the level
axis before the band is returned, i.e. exactly what LEG A already does to `iso_corr`
(`_merged_recover.py:986`, *"the ratio is non-monotone even though the numerator is"*) and
what `_iso_dec` / `_fit_pick_curve` do on the pick axis. No refit, no re-pin: the frozen forests are
read exactly as they are.

**Measured blast radius of FIX 2** (`tasks/task_06_blastradius.*`; isotonic-increasing per quantile
over the level grid 40 → 120 step 0.5 at each row's own other features, then `price6`, on all **804**
board rows):

```
median  +0.00 %    mean  +0.61 %    p90  +2.81 %    p99  +20.0 %    max  +84.9 %
466 of 801 rows unmoved (<0.05 %)
215 move >0.5 %  ·  168 >1 %  ·  104 >2 %  ·  39 >5 %  ·  25 >10 %  ·  8 >20 %

by 2026 games   g0     median +0.14 %  p90 +2.96 %      by level  40-50  median +0.52 %  p90 +23.3 %
                g1-4   median +0.00 %  p90 +3.64 %                50-60  median +0.00 %  p90  +3.79 %
                g5-13  median +0.00 %  p90 +5.44 %                60-70  median +0.02 %  p90  +2.05 %
                g14-21 median +0.00 %  p90 +1.12 %                70-80  median +0.00 %  p90  +0.22 %
                g22-40 median +0.00 %  p90 +0.50 %                80-120 median +0.00 %  p90  +0.41 %
```

**And it removes the trough completely.** Band-only sweeps under the isotonic band:
```
Max Kondogiannis  raw max-drop 40.2 %  ->  isotonic 0.0 %
Josh Dolan        raw max-drop 27.2 %  ->  isotonic 0.0 %
Charlie West      raw max-drop 34.1 %  ->  isotonic 0.0 %
Will Hayes        raw max-drop 39.8 %  ->  isotonic 0.0 %
```

### What a fix-act would have to measure (not done here — this is a diagnosis seat)
1. **Conservation (law 9).** As measured, FIX 2 is **one-sided**: an isotonic-increasing projection
   takes the running maximum, so it only ever raises. Mean +0.61 % across 801 rows **mints value**.
   A fix act must either renormalise (the engine's own `lam(pick)` local-neutrality pattern, or a
   pool renormalisation) or the owner must rule that the lift is the correction rather than an
   inflation. This is the single largest open question on the fix and it is not a small one.
2. **Direction of the correction.** Isotonic-increasing is not the only monotone projection —
   a decreasing-side variant, or a two-sided conserving isotonic (fit to the weighted mean rather
   than the running max), would move rows down as well as up. The choice is a ruling.
3. **The window.** FIX 2 as measured monotonises across the full model domain [40, 120]. A local
   window is cheaper and less disruptive but leaves long descending runs partly intact. The window
   is a dial and needs sizing against the measured run lengths (Kondogiannis's run spans ~2.1 level
   units; Dolan's ~0.5).
4. **Re-run of the score-sweep monotonicity check on all 86** (the harness exists here) plus the
   standing gates, the movers ledger, and the day-0 / printed-identity asserts, which read `b6`.
5. **Whether the q97 tail leg should be monotonised at all**, given `_b6_core` already applies
   `max(q97, b[4])` — the interaction of two monotone instruments needs one reading, not two.

---

## 9 · PROVENANCE

* engine: `ws_r23/` = byte copy of `engine/rl_after` at HEAD (`813e5cd`); `repo_r23/` = symlinks to
  `data/`, `docs/`, `engine/`, `tools/`, `vendor/`, `scores/`. Nothing written to the repo.
* store R23 `b745002e` (`data/season_state.json` `source_store_md5`), season state as_of_round 23.
* store R22 `cc02567f` extracted read-only to scratch (`git show b7ec627^:...`) for the prior-average
  side of every score sweep.
* band forest `/home/claude/cm_400.pkl` md5 `34faa865`; `q97m` from `data/q97m.pkl`.
* every mutation restored; `rt=True` / shipped-price re-assert on every swept row.
* scripts + outputs: `tasks/task_01_finesweep` (1-point sweep + full decomposition),
  `task_02_bandprobe` (threshold census + band breakpoints), `task_03_predict` (blind band-only
  ranking over the 86), `task_04_confirm` (third-player prediction test), `task_05_class`
  (86 true sweeps + drivers), `task_06_blastradius` (FIX 2 on 804 board rows),
  `task_07_final` (exact thresholds), `task_08_exactkink` (the §6a grid prediction test),
  `task_09_transmission` (rho31 / production share), `task_10_owner_stat` (the owner's count).
  Prediction recorded before its test in `PREDICTION.md`. Curve dump: `curve_dump.txt`.
