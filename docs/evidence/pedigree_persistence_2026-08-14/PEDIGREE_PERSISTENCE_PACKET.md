# PEDIGREE PERSISTENCE — THE MEASUREMENT, AND WHAT IT ASKS THE OWNER TO RULE

**ORDER 30B-M · measurement seat · `land/order-29` · 2026-08-14 · READ-ONLY · NOTHING WIRES**
Prereg: `PREREG_30BM.md` (filed and pushed before any quantity was measured, commit `f8c7eeb`).
Evidence: `PERSISTENCE_TABLE.md` / `.json` · harness `o30bm_measure.py` · derivation `o30bm_derive.py`.

The owner's challenge, verbatim (#334 comment `5293885947`):

> *"For a 20 year old, a 44 average for a SF might have a different curve for a former pick 4 vs a
> former pick 60. Whereas what you're telling me is that the growth curve will be the same for all
> positions and not personalised by pick etc?"*

**It is measured. The three answers, in three lines:**

1. **PERSISTENCE — the owner is right that pick keeps mattering, and BOTH standing numbers are wrong.**
   Conditional on output, age and position, pick still predicts remaining delivered value out to ~70
   games. The measured pedigree share at 36 games is **≈ 16–24%** — not the old machinery's ~40%, and
   **three to ten times** the blend's 5.6%. Past 71 games it is measured at 2.2% and is statistically
   indistinguishable from zero.
2. **FORM — the owner's TRAJECTORY hypothesis is NOT supported at these sample sizes.** Pick-conditional
   growth curves did not beat the fading level bonus on any held-out reading; they were, if anything,
   fractionally worse. **The blend's functional shape survives. Its calibration does not.**
3. **POSITION CLOCKS — no signal on the deciding lens.** Per-position development slopes made held-out
   prediction *worse*. A supplementary raw-growth lens does show talls still improving 1.7 years longer
   than smalls — but that lens is post-hoc and descriptive, and it is not enough to wire on.

**The wiring question this changes is not the blend's FORM. It is the blend's FADE RATE — and that
collides with a ruled window, so it goes to the owner rather than into code.**

---

## 1 · WHAT WAS MEASURED, AND ON WHAT

| | |
|---|---|
| population | ND entrants, `effective_pick` 1–64, entry years **2005–2018** |
| panel | **4,033 career states over 767 careers**, state years 2006–2019 |
| a "state" | a player at the end of a played season: pick band × position × age × games-so-far × current output |
| the target | **remaining delivered value over the next 6 observed seasons**, discounted 14%/yr **from the state year** |
| the scorer | ORDER 26B Layer 2's pricing core, unchanged — Ruling 1 bars read live off the engine, Ruling 3's season callable (certified bit-exact against `price6` on 804/804 rows), sqrt games weight, no era normalisation, force-majeure exclusions carried |
| left censoring | store season rows begin in 2005, so 2003–04 entrants are missing their first seasons and are **excluded** |
| right censoring | 2026 is in progress: it contributes no future value and supplies no fitting state |
| survivorship | **zeros stay in** — a career that ends contributes 0 to every remaining sum thereafter; 6–15% of states carry a hard zero |
| projected tails | **none.** Every future season is realized or zero. Engine band projections were deliberately kept out: judging the engine's form on the engine's own projections would be circular, and the owner has already named that evidence "engine-lensed and completion-optimistic" |

**Two things the panel is NOT.** It is not a price — a six-season window from age 20 misses a player's
peak years, so the *level* of these numbers understates a career. And it is not era-normalised, per
Ruling 7. The quantity that transfers to pricing is the pedigree **share**, not the level.

### 1.1 · A free result that arrived on the way: the Step-1 v0 ladder passes its outcome check

| pick band | n | mean realized R6 | mean v0 | **R6 / v0** |
|---|---:|---:|---:|---:|
| A 1–6 | 88 | 883.0 | 2291.8 | **0.385** |
| B 7–12 | 90 | 568.9 | 1324.6 | **0.430** |
| C 13–20 | 120 | 394.8 | 895.3 | **0.441** |
| D 21–40 | 300 | 255.0 | 605.1 | **0.421** |
| E 41–64 | 355 | 112.5 | 280.8 | **0.401** |

Realized six-season value is a **near-constant 0.39–0.44 of v0 across every pick band** (max/min 1.145).
The re-fitted positional ladder's *pick shape* is confirmed by outcomes at the gate. Nothing in this
order asks for it to move.

---

## 2 · Q1 — THE PERSISTENCE CURVE

Within each games band, remaining value is regressed on production, age, position and output — and then
on `v0`. **σ, the pedigree share, is the fraction of expected remaining value the pick term carries after
production, age and position have taken everything they can.** Cluster-robust on player; 90% CI from a
300-replicate player-cluster bootstrap.

| games so far | n | clusters | β on v0 | cluster t | **σ MEASURED** | σ 90% CI | ruled blend `1−w` | old anchor carry |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **0–5** | 382 | 332 | 0.2968 | **3.76** | **70.1%** | 42.9 … 99.6% | 78.9% | ~40% |
| **6–15** | 591 | 467 | 0.3623 | **5.95** | **66.4%** | 47.7 … 83.0% | 40.4% | ~40% |
| **16–35** | 834 | 571 | 0.2233 | **4.25** | **33.1%** | 20.8 … 45.6% | 12.4% | ~40% |
| **36–70** | 887 | 436 | 0.1532 | **2.39** | **16.5%** | 5.9 … 28.0% | 1.6% | ~40% |
| **71+** | 1339 | 297 | 0.0201 | 0.49 | **2.2%** | −4.6 … 10.5% | 0.2% | ~40% |

**The decay is monotone with no blip (prereg P5 held exactly), and it is real: the pick coefficient is
significant at t = 3.8, 6.0, 4.3 and 2.4 in the first four bands and dies in the fifth.**

**At 36 games — kako's exact count — the interpolated share is 23.8%** (log-linear between the measured
midpoints 25.5 and 53.0; labelled as an interpolation, not a measurement).

**Where the two standing assumptions land:**

| assumption | claim at 36 games | verdict against the measurement |
|---|---:|---|
| the old machinery's anchor carry | ~40% | **too high** — measured 16–24%, and 40% is outside the 90% CI of every band past 16 games |
| the ruled blend `1 − w(36)` | 5.62% | **too low, by 3–10×** — measured 16–24%; the blend's own value sits at or below the bottom of the measured CI from 6 games onward |
| **the measurement** | **16–24%** | the pick effect is real, large in the middle of a career, and gone by 71 games |

**Horizon honesty.** σ at 36–70 games is 16.8% at H = 4, 16.5% at H = 6 and **8.5% at H = 10**. A longer
window dilutes pedigree, because pedigree buys the *next* few seasons more than the distant ones. A
price is an infinite-horizon object, so **the price-relevant share is at the lower end: call it 8–17% at
36–70 games, not 24%.** Every other declared sensitivity (discount 0%, grace-2, linear games weight,
core window, single-season output axis) reproduces the primary curve within 1–4 points.

### 2.1 · The same claim without a model

| games so far | picks 1–12: n / mean residual | picks 21–64: n / mean residual | gap | gap 90% CI |
|---|---:|---:|---:|---:|
| 0–5 | 37 / +133.0 | 293 / −28.2 | **+161.2** | 30.2 … 313.9 |
| 6–15 | 109 / +129.3 | 404 / −57.2 | **+186.5** | 54.9 … 324.1 |
| 16–35 | 196 / +44.9 | 499 / −22.9 | **+67.8** | −51.8 … 199.0 |
| 36–70 | 238 / +52.0 | 498 / −16.1 | **+68.1** | −80.7 … 237.4 |
| 71+ | 479 / +27.7 | 629 / −0.8 | **+28.5** | −90.9 … 146.1 |

Residuals from the *pick-blind* model. High picks beat their own production/age/output projection at
every depth; low picks fall short of theirs at every depth. **The sign never turns.** The interval
crosses zero from 16 games onward — that is the honest statement of the power available at these n, and
it is why the model-based σ (which uses the continuous v0 ladder rather than two coarse classes) is the
primary reading and this is the check.

The cell-matched contrast agrees: after the preregistered thin-cell collapse (quintile → tercile), the
top-minus-bottom pick-band difference is **+159, +849, +273, +127, +201** points across the five bands.
On the un-collapsed quintile lens the 16–35 band has **zero usable strata** — disclosed, not hidden;
that thinness is exactly what the collapse ladder was preregistered for.

### 2.2 · The owner's question in its rawest form

Every panel state at **30–40 games with output below its own position's median** — the "modest output,
same games" cohort — split by pick:

| cohort | n | mean R6 | p25 | median | p75 | zero |
|---|---:|---:|---:|---:|---:|---:|
| **picks 1–10** | 26 | **691.5** | 3.4 | **102.4** | 1155.5 | 12% |
| **picks 40+** | 49 | **407.8** | 7.7 | **29.2** | 304.1 | 12% |

Same games, same modest output — the high picks delivered **1.7× the mean and 3.5× the median**. And the
names are the argument: from the 1–10 cohort, `andrew-brayshaw` (pk 2, 39 g, 66.1 avg at 20 → R6 3752,
191 career games), `nicholas-naitanui` (pk 2, 32 g, 66.9 → 3040), `dion-prestia` (pk 9, 31 g, 69.0 →
2087), `travis-boak` (pk 6, 31 g, 72.5 → 1833, 387 career games), `paddy-ryder` (pk 7, 30 g, 57.3 →
1672). But the low-pick cohort is not empty at the top — `andrew-swallow` (pk 43 → 3007),
`luke-parker` (pk 42 → 2822), `jarryd-lyons` (pk 61 → 2586), `taylor-walker` (pk 64 → 1651). **Pedigree
shifts the distribution; it does not own the tail.** That is the whole shape of the finding, and it is
why the share is 16–33% in this range rather than 0% or 40%.

---

## 3 · Q2 — THE FORM. THE OWNER'S HYPOTHESIS IS NOT SUPPORTED

Three models, same target, same panel, same folds (5-fold, **grouped by player**, deterministic, no RNG):
`P` production only · `L` = `P` + `v0` + `v0·log1p(games)` (the blend's shape, generalised so the data
picks its own decay rate) · `T` = `L` + **pick-class × development-axis interactions** — the literal
statement that the growth curve itself is pick-conditional.

| form | parameters | held-out RMS | held-out MAE | held-out Spearman |
|---|---:|---:|---:|---:|
| P — production only | 16 | 715.76 | 478.29 | 0.7166 |
| L — fading level bonus | 18 | **709.42** | **471.74** | **0.7277** |
| T — pick-conditional trajectory | 30 | 709.53 | 473.27 | 0.7175 |

| comparison | RMS reduction | folds won | preregistered bar | adopted? |
|---|---:|---:|---|---|
| P → L | 0.89% | **5 / 5** | ≥2.0% AND ≥4/5 | **NO** |
| L → T | **−0.02%** | 2 / 5 | ≥2.0% AND ≥4/5 | **NO** |

**Verdict by the preregistered rule: the simpler form wins by default at every step.** The time-block
hold-out (fit ≤2012, test ≥2013) says the same thing more sharply — `L` 718.92, `T` 724.94: the
trajectory model *degrades* out of its own era.

**This is a real verdict, not a shrug — and it is preregistered.** P6 predicted exactly this outcome and
said so before the data was touched: *"if the data cannot distinguish them at these sample sizes, SAY
SO — that is a verdict, and the simpler form then wins by default."*

**But two things must be said plainly alongside it, because both are the measurement:**

1. **`L` wins 5/5 folds and its pick terms are individually strong** — `v0` at **t = 4.86**, `v0·log(g)`
   at **t = −3.89**, cluster-robust. It just does not move squared error by 2%, because squared error in
   this target is decided by *which handful of players become stars*, and pedigree shifts the whole
   distribution rather than calling the tail. **A 2% RMS bar is a demanding bar in a star-dominated
   target, and the seat set it blind.** The pedigree term is small for *prediction error* and material
   for *expected value* — a price is an expectation, so both facts must reach the owner.
2. **`T` is not merely unproven, it is unhelpful.** Its interaction terms are individually significant
   (`cur × hi` t = 3.10, `log g × hi` t = 3.85, `cur × lo` t = 3.99) — the fit *can* find pick-conditional
   slopes — but they buy nothing out of sample and cost 12 parameters. Where `T` does edge ahead it is
   by fractions in the low-pick class and the 36–70 band, and it loses in the class the owner cares most
   about (picks 1–12: RMS 848.6 vs `L` 844.5) and in the young/thin cell his question is about
   (games ≤ 40 & age ≤ 21: **`L` 689.6, `T` 691.1, `P` 708.6**).

**In the exact cell of the owner's question — young, few games — the LEVEL bonus is the best of the
three, and it beats production-only by 2.7%. The pick information is there. It is a level, not a curve.**

---

## 4 · Q3 — POSITION CLOCKS

| model | parameters | held-out RMS | MAE | Spearman |
|---|---:|---:|---:|---:|
| P1 — one development table | 16 | **715.76** | 478.29 | 0.7166 |
| P6 — per-position slopes | 66 | 719.68 | 479.47 | 0.7110 |

**−0.55% (i.e. worse), 0 of 5 folds. Verdict: ONE TABLE.** Fifty extra parameters bought nothing.

**The preregistered peak-age lens carries NO SIGNAL, and P7 is breached on it.** The readout pinned to
the age-18 boundary in all six groups, for a structural reason the seat should have foreseen: *remaining*
value falls with age at a fixed state for horizon reasons alone, so a remaining-value target has no
interior "development peak" to find. The lens was wrong, not the football.

**Supplementary lens — post-hoc, descriptive, and it does NOT re-decide Q3.** Measured directly on
output growth (median change in season average, ≥5 games in both seasons):

| position | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| KPD | +4.0 | +1.4 | +3.2 | −1.5 | +1.3 | +3.1 | −1.5 | +1.9 | −4.2 | −1.5 |
| KPF | +8.1 | +2.9 | +3.1 | +0.8 | +2.5 | +0.7 | +0.4 | +1.1 | −3.3 | **+2.4** |
| MID | +8.1 | +5.5 | +3.8 | +1.7 | +1.7 | −2.0 | +1.1 | −2.6 | +0.4 | −3.9 |
| RUCK | · | **+9.4** | +4.9 | **+5.5** | **+4.6** | −2.2 | −5.1 | −2.4 | +3.7 | −3.4 |
| SD | +5.4 | +3.6 | +3.2 | +1.8 | +2.5 | +1.1 | +1.1 | −2.6 | −1.1 | −3.6 |
| SF | +8.1 | +3.0 | +4.3 | −0.6 | +0.8 | +0.7 | −0.1 | −1.9 | −1.4 | −4.0 |

The football prior is visible: **rucks are still adding 4.6–5.5 points a season at ages 22–23, when mids
are down to 1.7 and forwards to under 1.** Last age with a positive median growth step: tall groups
average 27.0, small/mid 25.3 — **a gap of 1.67 years.** But this is a different target (output growth,
not value), it was looked at after the deciding lens returned, and the deciding lens said one table.
**The seat reports it as a live question, not as evidence to wire on.**

---

## 5 · THE NAMED ROWS

| player | pick | pos | games | age | output | **board price** | old machinery implies pedigree | ruled blend implies | **measured implies** | model-predicted R6 (P / L / T) |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`isaac-kako`** | 13 | SF | **36** | 20 | 50.7 | **1320** | ~40% = **528** | 5.62% = **74** | **≈16–24% = 211–314** | 483 / **449** / 481 |
| `willem-duursma` | 1 | MID | 19 | 19 | 77.0 | 4223 | ~40% = 1689 | 20.6% = 869 | ≈42% = 1791 | 1476 / **2011** / 2171 |
| `dyson-sharp` | 13 | SF | 13 | 19 | 68.2 | 3269 | ~40% = 1308 | 33.0% = 1079 | ≈53% = 1735 | 1102 / **1251** / 1442 |
| `jacob-farrow` | 10 | SD | 18 | 19 | 71.7 | 2765 | ~40% = 1106 | 22.2% = 615 | ≈44% = 1216 | 1073 / **1115** / 1061 |

*"Measured implies" applies the measured pedigree-share curve (§6's refit) to today's board price. The
`R6` predictions are six-season slices, NOT prices — a 20-year-old's peak seasons fall outside a
six-season window, so those columns understate a career and must not be read as a valuation. The old
machinery's ~40% is pinned by the brief **at 36 games** — kako's state; for the three 13–19 game rows it
is carried as a reference line, not as a claim about what that machinery would have printed there (it
would have carried more, not less).*

**On kako specifically — the poster state:**
- **The old machinery would have carried ≈528 of his 1320 on pedigree. The ruled blend carries ≈74.
  The measurement says ≈211–314.** The truth is much nearer the old machinery than the new blend, and
  neither is right.
- The fitted level form puts **123.3 points of his predicted 449 (27.5%)** on the pick term — arrived at
  from a completely independent direction, and it agrees with the band curve.
- **The level and trajectory forms differ on him by 7%** (449 vs 481). The owner's hypothesis, applied to
  the exact player it was raised about, changes his number by less than the width of one cell's error
  bar. That is the cleanest single answer to the challenge: *at pick 13 and 36 games, the pick still
  matters a lot — but it matters as a level, not as a different curve.*
- His measured peers say the same thing. Of the 26 historical picks 1–10 sitting at 30–40 games with
  below-median output, the median realized R6 was 102 and the p75 was 1156: **most of that cohort never
  arrived, and the ones that did, arrived big.** Pedigree at this state is optionality, not a floor.

---

## 6 · WHAT THIS SAYS ABOUT THE BLEND'S FINAL FORM

**The form survives. The fade rate does not.**

The ruled blend is `1 − w(g) = exp(−(g/τ)^β)`, `τ = 11.650213`, `β = 0.937162`. Refitting **that same
ruled functional form** to the five measured σ points (n-weighted least squares, grid `τ` 2–400 step 0.5,
`β` 0.20–2.00 step 0.01) gives:

| | τ | β | crossover (w = 0.5) | n-weighted SSE vs measured |
|---|---:|---:|---:|---:|
| ruled blend | 11.650 | 0.937 | **7.879 games** | 98.86 |
| **refitted to the measurement** | **23.000** | **0.800** | **14.547 games** | **13.53** |

| games | measured σ | ruled blend | refitted |
|---:|---:|---:|---:|
| 2.5 | 70.1% | 78.9% | 84.4% |
| 10.5 | 66.4% | 40.4% | 58.6% |
| 25.5 | 33.1% | 12.4% | 33.8% |
| 53.0 | 16.5% | 1.6% | 14.2% |
| 85.5 | 2.2% | 0.2% | 5.7% |

**AND HERE IS THE OWED OWNER WORD.** The refit's crossover is **14.5 games**. Ruling 4's window — held as
prereg P15 and reported as HELD at the Step-3 stop — is **6–10 games**. *The measurement and the ruled
window disagree.* The seat will not resolve that by choosing:

- The ruled window came from the R1 re-derived cumulative backbone — a measurement of **price ratios
  against entry** in the sitter/fade lane.
- This order measures **realized remaining delivered value**, a different quantity on a different basis.

Both are measured objects. They are not the same object, and where they conflict it is a ruling, not a
fit. **Three routes, priced for the owner, none taken:**

1. **Hold ruling 4's window; the blend keeps `τ = 11.65`.** Consequence, stated: established young
   players carry 3–10× less pedigree than the outcomes support, and the entire pick effect between 10
   and 70 games is priced out of the book.
2. **Re-calibrate to the measurement (`τ ≈ 23`, `β ≈ 0.80`).** Consequence: the crossover moves to ~14.5
   games, outside the ruled window, and every young established row re-prices upward.
3. **Rule a new window from the measured curve and re-derive inside it.** The seat's arithmetic says the
   measured curve cannot be reached with a crossover below ~12 games without leaving the 16–70 game
   range badly under-weighted.

---

## 7 · WHAT IT SAYS ABOUT THE STOP §5 BOUNDARY QUESTIONS

The owner deferred the forbidden-set ruling until this reported. Here is what the measurement does and
does not reach. **Where it does not reach, the seat says so and does not choose.**

**Q1 — THE ISO PICK-TAX (`par_at` site 2), the par-built isotonic pick correction on the production leg.
THE MEASUREMENT REACHES THIS ONE, AND IT POINTS ONE WAY.** The ISO table is a **pick-conditional
multiplier on the production leg** — structurally the same *kind* of claim as form `T`, which is the
claim the data declined to support: that pick belongs *inside* the production channel rather than beside
it. It is also unfitted — built by probing `raw_ev` on par synths, never against outcomes. Under the owner's amended principle — *pick information enters prices only through MEASURED
objects* — an unfitted pick multiplier on production is exactly the object the amendment excludes, and
the measured object that does its job is the `v0` term, whose coefficient this order has now measured
(0.49 at entry → 0.16 at 36 games → 0.10 at 70 games → indistinguishable from zero past 71).
**Seat's recommendation: DELETE the ISO pick-tax, and let the re-calibrated `v0` leg carry the pick
effect.** The STOP's third option — "the ISO table as re-derived without the pole" — is equally unfitted
and is excluded by the same principle. *This is a −16.9k to −19.3k board consequence across 271–401 rows;
the seat recommends and does not choose.*

**Q2 — THE EVIDENCE WEIGHT (`_c_w`'s `Q = clip(sa/par, 0, 2)`). NO SIGNAL. THIS MEASUREMENT DOES NOT
BEAR ON IT.** `Q` carries no pick information — it compares a player to par, not a pick to an outcome.
Nothing in this order measures whether `par` or something in the v0 language is the right denominator.
The seat notes only that it is not a pedigree object and therefore not what the amended principle is
aimed at; the ruling stays the owner's.

**Q3 — THE DECAY GATE (`ev:2438`'s `pr = bestlvl/par`). NO SIGNAL, same reason.** A form/decay gate on a
player's own level carries no pedigree. Outside this measurement.

**Q4 — THE SUPERSESSION LIST. THE MEASUREMENT SUPPORTS THE SEAT'S "REPLACE, NOT WRAP" READING.** σ is a
share **of the whole**: production and pedigree sum to one expectation. If the ruled blend wraps
machinery that already carries an anchor leg (`_a_blend`, `sitout_ev`'s `ns==0` arm, the year-zero
floor), pedigree is counted twice and the measured share is exceeded by construction. **One blend, one
pedigree leg, at the measured weight.** On ITEM H's ruled cuts, D8 graded staleness, the ruck ceiling and
KPF compression: **no signal — this order does not measure them and the seat will not sort them.**

---

## 8 · THE SEAT'S RECOMMENDATION

1. **Answer the owner's challenge honestly: he is right about persistence, and not supported on
   trajectory.** Pick keeps predicting out to ~70 games; it does so as a fading LEVEL, not as a
   personalised growth curve. **Do not build pick-conditional development curves** — 12 extra parameters
   bought −0.02% and lost the era hold-out.
2. **Re-open the blend's calibration, not its form.** The measured pedigree curve is 3–10× the ruled
   blend's through the 10–70 game range. The refit of the ruled form is `τ ≈ 23.0, β ≈ 0.80`. **It
   breaks ruling 4's 6–10 game crossover window, so it is an owner ruling, not a seat act.**
3. **Wire nothing on Q3.** One table stands on the deciding lens. If the owner wants the tall/small clock
   pursued, it needs a growth-shaped target and its own prereg — the raw lens says there is something
   there (1.67 years), and the value lens says it does not pay.
4. **On the forbidden-set boundary: delete the ISO pick-tax (Q1); the seat has no evidence on Q2/Q3 and
   will not choose; Q4's replace-not-wrap reading is confirmed.**
5. **One more measured object is now available for free:** the entry ruler's outcome check (§1.1). If any
   future act wants to move the v0 ladder's pick shape, this table is the thing it has to beat.

---

## 9 · PREREG SCORED BY NUMBER — BREACHES OWNED

| # | verdict | what it claimed | what was measured |
|---|---|---|---|
| **P1** | HELD | panel 2,500–6,000 states over 700–1,050 careers | 4,033 states, 767 careers |
| **P2** | **BREACH** | median R6 < 25% of mean at 16–35 games; ≥30% zeros in the ≤35-game bands | median/mean **0.283** (predicted <0.25) and zero share **11.3%** (predicted ≥30%). **Both legs wrong, in the same direction: delivered value is skewed, but less brutally than the seat assumed, and outright zeros are far rarer than assumed — a player who reaches a state has usually banked something.** |
| **P3** | HELD | pick still predicts at 16–35 games | tercile-collapsed matched Δ **+272.6** over 7 strata; residual gap **+67.8**; β_v0 **0.223** at cluster **t = 4.25**; full-panel β_v0 **0.491**. Scored on the preregistered collapse ladder — the un-collapsed quintile lens has **zero usable strata** at this band and that is disclosed, not papered over |
| **P4** | HELD | pedigree share at 36–70 games strictly between 5.6% and 40%, specifically 8–25% | **16.5%** |
| **P5** | HELD | share non-increasing across games bands (one ≤2pp blip allowed) | 70.1 → 66.4 → 33.1 → 16.5 → 2.2; **zero up-steps** |
| **P6** | HELD | trajectory does NOT clear the 2.0%/4-of-5 bar (the seat predicted against the owner) | **−0.02% RMS, 2/5 folds.** The seat's blind prediction was right and the owner's hypothesis is not supported |
| **P7** | **BREACH** | per-position clocks clear the bar AND tall peak ≥ small peak + 1.0y | **Both legs failed.** P6 was worse (−0.55%, 0/5), and the peak-age lens was **degenerate** — it pinned to the age-18 boundary in all six groups because a *remaining-value* target declines with age for horizon reasons and has no interior peak. **The lens was mis-designed at prereg time. Owned.** The supplementary raw-growth clock (post-hoc, non-deciding) does show a 1.67-year tall/small gap |
| **P8** | HELD | kako below 1320 under every form; L and T within 2× | 483 / 449 / 481 vs board 1320; L vs T differ by 7% |
| **P9** | HELD | pool band below band A at comparable states | pool 142/236/362/590/599 vs band A 272/1084/1086/1457/1311 |
| **P10** | HELD | one pass, nothing tuned after a reading | single execution; verdicts as scored on first output; the two lenses added afterwards (the preregistered tercile collapse and the raw growth clock) are labelled where they appear and re-decide nothing |

**8 held, 2 breached (P2, P7). Neither breach touches a verdict:** P2 was a claim about the target's
shape, P7 was a mis-designed instrument whose failure is itself the Q3 answer's honest caveat.

---

## 10 · ANOMALIES AND LIMITATIONS, STATED

1. **A six-season window is not a career.** For a 20-year-old the window ends at 26 and misses the peak.
   The **share** transfers to pricing; the **level** does not. The H = 10 sensitivity shows the share
   itself is horizon-sensitive at depth (16.5% → 8.5% at 36–70 games) and stable early (33.1% → 31.6% at
   16–35). Price-relevant reading: **8–17% at 36–70 games**.
2. **The sitter has no state.** The store's ruled convention gives a did-not-play season no row, so a
   player sitting out mid-career produces no state that year — he re-appears when he next plays, with
   the sat-out year correctly contributing zero to any remaining sum spanning it. The sitter *lane*
   (30A) measured that population directly; this order does not re-open it.
3. **No era normalisation** (Ruling 7). Scoring-era drift sits inside the panel untouched. The time-block
   hold-out is the check on it and it is mild: RMS 709 → 719 across a 13-year gap.
4. **Cell thinness is real.** 1,378 full cells exist; **94 clear n ≥ 8**. That is why the primary reading
   is model-based with the cell contrast as the check, and it is why the trajectory question cannot be
   settled by cells — there are not enough of them, which is itself the honest answer to Q2.
5. **The 2026 rows are in progress.** The named-row predictions use a part-season at full weight (≥10
   games caps the games weight at 1). Disclosed, not corrected.
6. **The board on this branch is the entry board `36d5dfc7`**, not the Step-2 board `92982031`; kako's
   1320 is identical on both (the Step-2 fade moved only `cg == 0` rows).
7. **The v0 artifact read is `V0REFIT30B.json`'s `posv_out`** — the Step-1 re-fitted positional ladder,
   which is the current entry ruler but is **not** the file installed at `engine/rl_after/pvc_curve_v2.json`.
   Stated so nobody reads the two as the same object.

---

## 11 · THE LINE

**NOTHING WIRES.** No board, store, engine, curve or config file was touched by this order; the two
harnesses are read-only and the engine was loaded from a staged copy for its scorer callables alone.
PR #510 stays HELD, the Step-2 fade stands as wired, and the Step-3 forbidden-set boundary stays
**UNRULED**. The seat has measured the object the owner asked for, recommended, and stopped.

**The owner's word is owed on three things:** the blend's fade calibration against ruling 4's crossover
window (§6), the ISO pick-tax under the amended principle (§7 Q1), and whether the tall/small clock is
worth its own order (§4).
