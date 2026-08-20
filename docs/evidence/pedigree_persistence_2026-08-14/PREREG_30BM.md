# PREREG — ORDER 30B-M · THE PEDIGREE-PERSISTENCE MEASUREMENT

**Seat:** ORDER 30B-M measurement seat · `land/order-29` · 2026-08-14
**Authority:** issue #334 comment `5293885947` (owner words + brief; owner go-word "Yes").
**Status of this file:** committed and pushed **BEFORE any outcome quantity was computed.** Everything
below the line "THE PREDICTIONS" is a falsifiable commitment made blind. Structural census facts
(record counts, year ranges, field coverage) were read before writing this file and are stated as
such — no remaining-value, pick-effect, fit or ranking quantity had been computed when this was filed.

**READ-ONLY.** Board, store, engine and curve are untouched. `NOTHING WIRES.` The deliverables are a
measurement and a recommendation; the wiring form follows the owner's ruling on the packet.

---

## 0. THE QUESTION BEING MEASURED

The Step-3 blend is `price = w(g)·production + (1−w(g))·v0·fade`, with
`w(g) = 1 − exp(−(g/11.650213)^0.937162)` (`BLEND30B.json`, P13/P14/P15 held). This form can only
express the pick effect as a **fading level bonus proportional to entry v0**. At 36 games it leaves
`1 − w(36) = 5.62%` of the price on the pedigree leg. The old machinery's anchor carry implied
**≈40%** at the same point. **Neither number was ever fitted to an outcome.**

The owner's challenge (verbatim, 2026-08-14): *"For a 20 year old, a 44 average for a SF might have a
different curve for a former pick 4 vs a former pick 60. Whereas what you're telling me is that the
growth curve will be the same for all positions and not personalised by pick etc?"*

The amended principle on his word: **pick information enters prices only through MEASURED objects.**
This order measures the object.

---

## 1. THE SCORER BASIS (reused, not reinvented — cited)

The delivered-value scorer is ORDER 26B Layer 2's, carried verbatim in its pricing core:

| element | value / source |
|---|---|
| per-season production value | `season_points(X,P) = SCALE · posval(X + capt_prem(X) − BARS[P]) · 21` — Ruling 3's pinned callable, certified **bit-exact against `price6` on 804/804 active rows** at the ORDER 26B step-1 gate |
| bars | `BARS[P] = MA.REPL[P] − rd.REPL_DROP[P]`, read live off the engine at import (Ruling 1: KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9 — asserted, never typed) |
| games weight | `w = min(1, sqrt(games/10))` — ≥10 games is a full season at its average (Ruling 10's linear form is a declared sensitivity, §7) |
| season bar group | the engine's own `_fit_bar` rule: split `position_played` on `/`, collapse, take the **lowest-REPL** member; no row position → the declaration column |
| era | **NO era normalisation** (Ruling 7). Averages are the store's raw values. |
| discount | flat 14%/yr, `MA.LENS['bal']`, through the engine's own `disc_factor`; `k ≤ 0` discounts at 1.0 |
| γ | `GAMMA == 1.0` ⇒ `val(r) = SCALE·r` is linear ⇒ delivered value is **additive across seasons** in board points. This is the fact the whole scorer rests on, and the reason a "remaining" sum is well defined. |
| force majeure | `thomas-boyd` and `paddy-mccartin` are EXCLUDED entirely (standing owner ruling, re-filed #334 comment `5274640130`); every ND draftee in their draft years slides up one pick — Layer 1's `effective_pick` already carries the slide, and this harness keys on `effective_pick` |
| data | `docs/evidence/grace_adoption_2026-08-13/inputs/layer1_player_seasons.json`, md5 **`ad1229ea6f443538479447132382b21c`** — the pinned assumption-free Layer 1 (2,650 entries · 11,484 player-seasons). Asserted at entry and at exit. |

**DECLARED DEVIATION 1 — THE DISCOUNT IS RE-ANCHORED AT THE STATE, NOT AT ACQUISITION.** Layer 2
discounts a whole career back to entry (`k = season_year − entry_year`). This order measures **remaining**
value **from a career state**, so each future season is discounted by `1.14^−(y − Y)` where `Y` is the
state year. This is the same ladder, re-indexed; it is the only coherent reading of "what is left from
here". The grace-A exponent shift (`max(0, k − G)`, #334 comment `5275831956`) is an **entry-age-keyed**
convention about a draftee's first seasons; it has no meaning re-anchored at a mid-career state, so the
primary basis carries **no grace**, and a grace-shaped variant is run as a declared sensitivity (§7).

**DECLARED DEVIATION 2 — NO PROJECTED TAILS. OBSERVED SEASONS ONLY.** Layer 2's Ruling-8 tails come from
the engine's own band machinery. Feeding engine projections into a measurement whose purpose is to judge
the engine's functional form would be circular, and the owner has already named that evidence
"engine-lensed and completion-optimistic" (#334 comment `5215167494`). Every future season in this order
is a **realized, played season or a zero**. Censoring is handled by the fixed horizon (§3), not by a model.

---

## 2. POPULATION

**Primary panel.** Layer 1 entries with `type == 'ND'` and `effective_pick` in **1–64** (the national
curve's ruled domain; the pool has no pick ordering and no pick ladder — "there is no price for pick 70").

**Left censoring — stated, and it binds.** The store's season rows begin in **2005**, while entries begin
in 2003. Every 2003 and 2004 entrant (140 careers with rows) is missing its first one or two seasons, so
its games-so-far axis is wrong at every state. **Entry years 2003 and 2004 are EXCLUDED from the primary
panel.** Entry years used: **2005 onward**.

**Right censoring — stated, and it binds.** The 2026 season is in progress (142 zero-game placeholder
rows; the career-games counter lags by 1–2 games on 457 active records — Layer 1's own measured anomaly
`#323`). **2026 contributes no future value to any state and no state to the fitting panel.** States at
2026 exist only as PREDICTION states for the named rows (§8).

**Survivorship — the 30A way, cited.** Zeros stay in. A career that ends contributes **0** to every
remaining-value sum thereafter; a delisted player is not dropped, he is a zero. There is no separate
availability haircut (Layer 2 CFG: *"otherwise UNPRICED"*). The two historical explicit-zero rows
(`tim-mohr` 2015, `stewart-crameri` 2016) and the 142 in-progress 2026 zero rows are carried as Layer 1
carries them; the 2026 rows are outside the panel by the right-censoring rule above.

**Pool comparison band.** ND `effective_pick ≥ 65` plus the whole non-ND pool is measured as ONE extra
descriptive band ("pool") in the persistence table only. It never enters a fit, because it has no v0
ladder position.

---

## 3. THE STATE, THE TARGET, THE BANDS

**A STATE** is a player at the **end of a played season**. For player `i` and played season `Y`:

| axis | definition |
|---|---|
| pick band | `effective_pick` → **A 1–6 · B 7–12 · C 13–20 · D 21–40 · E 41–64** (+ `pool`, descriptive only) |
| position group | the engine's own season-bar rule applied to `position_played` at `Y`; if unresolved, the entry `position_group` |
| age | `Y − birth_year` (Layer 1 has 100% birth-year coverage) — bands **≤19 · 20 · 21 · 22–23 · 24–26 · 27+** |
| games so far | cumulative games through and including `Y` — bands **0–5 · 6–15 · 16–35 · 36–70 · 71+** (the brief's bands) |
| current output | `o` = games-weighted mean `avg` over the state season and the immediately preceding played season if it is within 2 years (else the state season alone) — bands by **quintile within position group**, cut on the primary panel |
| current production | `cur` = the scorer's own undiscounted season points at `Y` (games-weighted); `cur3` = mean of the last up-to-3 played seasons' season points |
| entry ruler | `v0 = posv_out[position group][effective_pick]` from the STEP-1 re-fitted positional v0 artifact (`docs/evidence/one_machinery_2026-08-14/V0REFIT30B.json`, λ = 0.995505141235, 107 ascents → 0) — **the current entry ruler** |

**THE TARGET.** `R_H(i,Y) = Σ_{y=Y+1}^{Y+H} pts(i,y) · 1.14^−(y−Y)`, where `pts` is the scorer's
games-weighted season points at the position played that year, and a season with no row contributes **0**.

**PRIMARY HORIZON `H = 6`.** A state is in the fitting panel iff `Y + 6 ≤ 2025`, i.e. **`Y ≤ 2019`**, so
every state in the panel has its full six-season future observed. Declared secondaries: `H = 4`
(`Y ≤ 2021`) and `H = 10` (`Y ≤ 2015`).

**ENTRY STATES.** A state at `g = 0` (entry year, before any season) has no output and is therefore not
in the fitting panel. Entry states are computed separately and only for one purpose: the **entry-anchor
pick spread**, the denominator against which persistence is expressed.

**NORMALISATION (how the pick increment is isolated).** Two, reported side by side:
1. **Model-based (primary).** Fit remaining value on production/age/position features **without pick**;
   the pick term's share of the fitted value is the **pedigree share** `σ`. This is the quantity directly
   comparable to the blend's `1 − w(g)` and to the old anchor carry's ≈40%.
2. **Matched contrast (non-parametric check).** Within each stratum (position group × age band × games
   band × output quintile), the difference in mean `R_H` between the top pick band present and the bottom
   pick band present, aggregated across strata with `min(n_top, n_bot)` weights. Reported with n and with
   p25/median/p75 of `R_H` in each cell.

**THIN CELLS.** A cell with `n < 8` is not reported as a cell; it is collapsed into the next coarser
level of its own axis (output quintile → output tercile → dropped from the stratum), and **every collapse
is disclosed by name and count** in `PERSISTENCE_TABLE.md`.

---

## 4. THE TWO FORMS (Q2)

All three models predict the same target `R_H` from the same panel, differing only in the pick terms.

**`P` — PRODUCTION BASELINE (pick-blind).** Columns: intercept · 5 position dummies · `age` · `age²` ·
`log1p(g)` · `o` · `o²` · `cur` · `cur3` · `games_at_Y` · `o·age` · `cur·age`.

**`L` — LEVEL FORM (the blend's shape).** `P` + `v0` + `v0·log1p(g)`. This nests a constant pick bonus
and lets the data choose the decay rate in games; it is the blend's functional claim, generalised
generously (the blend's own fade is a special case of a negative `v0·log1p(g)` coefficient).

**`T` — TRAJECTORY FORM (the owner's hypothesis).** `L` + pick-band × development-axis interactions:
pick bands collapsed to three for parameter economy — **hi = picks 1–12 · mid = 13–30 · lo = 31–64** —
each interacted with `age`, `age²`, `o`, `cur` and `log1p(g)`. This is exactly the claim that the growth
curve itself is pick-conditional: the same (age, output, position) state maps to a different remaining
value **shape**, not merely a different level.

**Fitting.** Ordinary least squares by `numpy.linalg.lstsq` on standardised columns (mean/sd from the
training fold only), deterministic, no regularisation path, no search over hyper-parameters.

**THE COMPARISON CRITERION — DECLARED HERE, BEFORE ANY FIT.**
- **PRIMARY: held-out RMS error in delivered-value board points**, under **5-fold cross-validation grouped
  by player key** (all of a player's states live in one fold; folds assigned deterministically by
  position in the sorted key list, `fold = index mod 5` — no RNG anywhere).
- **SECONDARY (reported, not deciding): held-out MAE; held-out Spearman rank correlation; and a
  block-in-time hold-out** (fit on states with `Y ≤ 2012`, test on `Y ≥ 2013`).

**THE DECISION RULE — DECLARED HERE.**
> **`T` is adopted over `L` only if it reduces primary held-out RMS by ≥ 2.0% AND wins in ≥ 4 of the 5
> folds. `L` is adopted over `P` on the same bar. Otherwise the SIMPLER form wins by default, and "the
> data cannot distinguish them at these sample sizes" is reported AS THE VERDICT.**

No tuning after any reading. One pass. If a fit is degenerate the degeneracy is reported, not patched.

---

## 5. POSITION CLOCKS (Q3)

**`P1` — ONE TABLE.** Position enters as a level dummy only; `age`, `age²`, `o`, `cur`, `log1p(g)` slopes
are **shared** across all six groups.
**`P6` — PER-POSITION CLOCKS.** The same five development slopes are estimated **per position group**.

Same criterion, same folds, same 2.0%/4-of-5 decision rule. Additionally reported: for each position
group, the **fitted age at which the development contribution peaks**, with the profile printed, so
"talls develop later" is a number and not a prior.

Q3 is independent of pick and is reported as separately wireable.

---

## 6. THE PREDICTIONS (committed blind, scored by number)

**P1 — PANEL SIZE.** The primary fitting panel (ND 1–64, entry ≥ 2005, `Y ≤ 2019`, `H = 6`) contains
between **2,500 and 6,000 states** over between **700 and 1,050 distinct careers**.

**P2 — SKEW.** Delivered value is star-dominated: in the 16–35 games band, **median `R_6` < 25% of mean
`R_6`**, and **≥ 30%** of states in the ≤ 35-games bands have `R_6` within rounding of zero.

**P3 — PERSISTENCE EXISTS.** Conditional on output, age and position, pick still predicts remaining
value at 16–35 games: the matched contrast (top pick band − bottom pick band) is **positive**, and the
`v0` coefficient in form `L` is **positive** on the full panel.

**P4 — THE MAGNITUDE LANDS BETWEEN THE TWO UNFITTED ASSUMPTIONS.** The measured pedigree share at the
**36–70 games** band lies strictly between the blend's **5.6%** and the old anchor carry's **≈40%**, and
specifically in **8%–25%**.

**P5 — MONOTONE DECAY.** The pedigree share is non-increasing across the five games bands
(0–5 ≥ 6–15 ≥ 16–35 ≥ 36–70 ≥ 71+), allowing a single non-monotone blip of ≤ 2 percentage points.

**P6 — THE FORM VERDICT (the seat predicts AGAINST the owner's hypothesis, and says so now).** Form `T`
does **not** clear the 2.0%/4-of-5 bar over form `L`; the predicted RMS improvement is **< 2%**, and the
verdict will be "the level form suffices; the trajectory difference is not resolvable at these sample
sizes." *If this prediction is wrong, the owner's hypothesis is measured true and the prereg is breached
in his favour — which is the outcome this seat would rather have.*

**P7 — POSITION CLOCKS ARE REAL.** Form `P6` **does** clear the 2.0%/4-of-5 bar over `P1`; and the fitted
peak development age for the tall groups (KPD, KPF, RUCK) is **at least 1.0 year later** than for the
small/mid groups (MID, SF, SD).

**P8 — KAKO.** For `isaac-kako`'s 2026 state (SF, pick 13, 36 games, age 20, output far below the SF bar
of 67.9), every fitted form predicts a remaining 6-season delivered value **below his current board price
of 1,320**, and the level and trajectory forms differ on him by **less than 2×**.

**P9 — THE POOL BAND CARRIES LESS.** The pool band's mean `R_6`, matched on games/age/output/position, is
below the mean of pick band A at the same states — i.e. the pick ladder is not an artefact of the ND/pool
split alone.

**P10 — PROCESS.** One measurement pass. No quantity is tuned after being read. Every breach above is
owned by number in `PEDIGREE_PERSISTENCE_PACKET.md`, and any lens that carries no signal is reported as
carrying no signal.

---

## 7. DECLARED SENSITIVITIES (named before running, so none of them is post-hoc)

1. `H = 4` and `H = 10` horizons.
2. Discount 0% (undiscounted remaining value) and 14% with a **2-season grace** re-anchored at the state
   (`exponent max(0, k − 2)`) — the grace-A shape, transported and labelled as transported.
3. Games weight `w = min(1, games/10)` (Ruling 10's linear sensitivity).
4. Core window only: entry years ≤ 2014 (Ruling 8 tier 1).
5. Output axis on the state season alone rather than the two-season blend.

Sensitivities are reported as agreement/disagreement with the primary reading. **A sensitivity never
replaces the primary reading and never re-decides a verdict.**

---

## 8. NAMED ROWS CARRIED THROUGH

`isaac-kako` (ND 2024, pick 13, SF, 36 games, age 20 — the poster state) · `willem-duursma` (pick 1, MID,
19 games, age 19) · `dyson-sharp` (pick 13, MID/SF, 13 games, age 19) · `jacob-farrow` (pick 10, SD, 18
games, age 19). For each: current board price, the old machinery's implied pedigree share, the level
form's prediction, the trajectory form's prediction.

**Historical validation cohorts, selected by rule and named in full:** every panel career whose state at
**30–40 games** carried output **below the median of its position group** — split into **picks 1–10** and
**picks 40+** — with each player's realized `R_6` printed. The rule is fixed here; the names fall out of it.

---

## 9. WHAT THIS ORDER MAY AND MAY NOT DO

MAY: read the pinned Layer 1, the store, the board, the v0 artifact and the engine's scorer callables;
compute; write into `docs/evidence/pedigree_persistence_2026-08-14/`; push to `land/order-29`.

MAY NOT: modify the board, the store, `rl_model.py`, `pvc_curve_v2.json`, the curve, any config, or any
wiring; merge anything; post GitHub comments; or choose the Step-3 forbidden-set boundary. **The packet
recommends. The owner rules. NOTHING WIRES until he does.**
