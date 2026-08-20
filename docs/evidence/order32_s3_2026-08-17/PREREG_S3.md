# PREREG — ORDER 32 SEAT S3: DOES SELECTION ITSELF PREDICT?

**Committed BEFORE any result was computed.** Read-only measurement seat; no engine file is touched.
Program brief: #334 comment 5311991190. Branch basis: land/order-29 @ 53f7433.

## 0. The question, in the owner's terms

The candidate law prices `price = ρ(g)·P̂ + [D(c_u)·(1−ρ) + Φ·β·ρ]·v0`. Games count `g` enters only
through the evidence weight ρ — it decides HOW MUCH the production leg counts, never adds value of its
own. The owner's hypothesis (his words, re kye-annand vs lukas-cooke, cooper-duff-tytler,
milan-murdock): **being selectable — playing lots of games — is in and of itself evidence of future
value, beyond the production delivered in those games; it thins the bust tail.**

Operationalised: **at fixed production surplus, fixed pedigree, and fixed age, does the games count of
a season predict SUBSEQUENT career delivered value?**

## 1. Population and data lane (all pinned, all on this branch)

- **Layer 1**: `docs/evidence/grace_adoption_2026-08-13/inputs/layer1_player_seasons.json`
  (md5 asserted in-script: `ad1229ea6f443538479447132382b21c`) — 2,650 entrants, 11,484 played-season
  rows (year / games / avg / position_played). Raw facts only, per its own law.
- **Layer 2 reference**: `.../inputs/LAYER2.json` — used ONLY to validate my season scorer
  (see §3 gate); no valuation number is taken from it into a regression.
- **Store**: `engine/rl_after/rl_model_data.json` (the branch's committed store) — used only for the
  season-bar fallback rule and the named-row read-through.
- **Entrant window**: `entry_year` 2004–2021 (the engine's own teaching window floor 2004 = YR_LO;
  2022+ is the ruled sensitivity-only tier and is EXCLUDED from every fit — named exclusion #1).
- **Force majeure**: thomas-boyd and paddy-mccartin excluded; the whole-draft slide applied to 2013/
  2014 ND picks, split taken on the SLID pick — the standing ruling, replicated verbatim from
  `o26b_layer2.py::attribute` (named exclusion #2).
- **Season rows with no resolvable position bar** are dropped and counted (named exclusion #3;
  Layer 2's own census says this is rare — the dual-label rule below handles most).

## 2. Unit of analysis, outcomes, observation-window rule

**Focal season** = a player-season with k = season_year − entry_year ∈ {1, 2, 3}. PRIMARY spec: k = 1
(the first played season — the cleanest match to the named players, all early-career). k = 2, 3 are
replications; when pooled across k, SEs cluster by player.

**Outcomes** (subsequent delivered value, in Layer-2 board points — the units where pick 1 ≙ 3000):

| name | definition | observability rule |
|---|---|---|
| Y1 | delivered points in focal_year + 1 (0 if no row — a did-not-play season carries no row by store law and credits 0) | focal_year ≤ 2024 (2026 is an in-progress season — round-lagged — and may not serve as an outcome year; named exclusion #4) |
| Y5 | sum of delivered points over focal_year+1 .. focal_year+5 | focal_year ≤ 2020 (all five outcome years complete, ≤ 2025) |
| Yrc | full rest-of-career delivered points | retired == True only (sensitivity; right-censoring for actives disclosed, never imputed) |

Per-season delivered points replicate the Layer-2 scorer exactly:
`pts(s) = SCALE · posval(avg + capt_prem(avg) − BAR[pos_played]) · 21 · min(1, sqrt(games/10))`
with the engine's own posval/capt_prem/BARS (BARS: KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3,
SF 67.9) and the engine's own dual-label season-bar rule (split on '/', lowest-REPL member; declaration
-column fallback). **Outcomes are UNDISCOUNTED** (primary): discounting to acquisition would let
entry age leak into the outcome; a flat-14-discounted-to-focal-year variant is reported as sensitivity.

## 3. Validation gate (must pass before any regression is read)

My season scorer, summed per career with the flat-14 discount to acquisition, must reproduce
`LAYER2.json::base[key].obs` to ≤ 1e-6 relative error on ≥ 99% of careers (mismatches counted and
named). If the gate fails I report the failure and stop rather than regress on an uncertified scorer.

## 4. Regressors and controls

- **G** = focal-season games (the treatment).
- **S** = focal-season production surplus = avg − BAR[position_played] (the "fixed output" control).
- **age** = age in the focal season (entry_age + k; Layer-1 entry_age, year−18 fallback only where null
  — Layer 1's own convention).
- **Pedigree cells**: ND pick bands 1-10 / 11-20 / 21-30 / 31-40 / 41-64 (the owner's tighter bands,
  ext_2026-08-17), ND>64, and each pool pathway (RD / MSD / SSP / IRE / PDA / PDN / PDS / UNR) as its
  own cell.
- **Position** = position_played in the focal season (dual labels resolved by the engine's rule).
- **Cohort year** = entry_year.

## 5. Model specs (declared)

1. **Cell spec**: within cohort-year × pick-band × position cells, demean Y, G, S, age and regress
   demeaned Y on demeaned G with S and age partialled — reported pooled across cells (cells with n < 3
   drop, counted). This is "at fixed pedigree/cohort/position" with no functional-form assumption on
   the cell effects.
2. **Pooled spec**: OLS Y ~ G + S + age + dummies(band) + dummies(cohort_year) + dummies(position),
   HC1 (heteroskedasticity-robust) SEs; cluster by player when k is pooled.
3. **Shape**: replace G with (a) sqrt(G), (b) linear spline in G with knots {5, 10, 15}, (c) games
   terciles. Report which form fits (adj-R², and the spline segment slopes with CIs) — linear vs
   saturating vs threshold.
4. **Stability**: spec 2 re-run per pick band, per era (entry 2004–2012 vs 2013–2021), per position
   group. A sign that holds in the pooled spec but flips across most bands/eras is reported as
   unstable, not averaged away.

**Effect size unit**: Y5 board points per marginal focal-season game at fixed output, and that number
as a fraction of the relevant v0 cell so the owner can read it against pedigree money.

## 6. Distributional reading (the owner's actual intuition)

**Bust definition (declared now)**: Y5 = 0 exactly — under the Layer-2 law a below-bar or unplayed
season credits 0 and never negative, so "delivered nothing above replacement in the next five years"
is literally Y5 = 0. Secondary threshold Y5 < 100 board points (≈ one modest above-bar part-season)
to show the reading is not knife-edge-dependent.

- P(bust) by focal-games tercile, within surplus band (below-bar / 0–10 above / 10+ above) ×
  pedigree band — full table.
- Logistic: bust ~ G + S + age + band + cohort + position.
- Quantile regressions of Y5 at q25 / q50 / q75 on the spec-2 controls: if the owner is right, the
  G coefficient should be LARGEST at q25 (tail-thinning), not uniform across quantiles.

## 7. Hypotheses and falsifiers (stated before results)

- **H1 (owner)**: ∂Y/∂G > 0 at fixed S, age, cell — for Y1 and Y5. *Falsified if* the pooled
  controlled coefficient is ≤ 0 or its 95% CI covers 0 AND the sign is not consistently positive
  across bands/eras.
- **H2 (shape)**: the effect saturates in G (concave; sqrt or spline beats linear). *Falsified if*
  linear fits as well and segment slopes do not decline.
- **H3 (bust tail)**: P(bust) falls with games tercile at fixed surplus band and pedigree, and the
  q25 games coefficient exceeds the q75 one. *Falsified if* tercile bust rates are flat/rising at
  fixed surplus, or quantile effects are uniform.
- **H4 (channel)**: decompose — does G predict subsequent GAMES (selection persistence), subsequent
  per-game surplus, or both? Reported as two auxiliary regressions (future games; future avg-surplus
  among played seasons). No falsifier — this is descriptive attribution.
- **H5 (the NEW-channel test — what is beyond ρ)**: the law already lets games govern how much the
  produced average is believed (ρ's channel). Under a PURE evidence-weighting story, more games at
  BELOW-BAR output is more evidence of badness and should predict a WORSE subsequent career than few
  games at the same bad output. Under the owner's selection story, coaches' repeated selection is
  itself information and the games coefficient stays ≥ 0 even at below-bar output. **Declared test**:
  spec 2 plus G × 1[S < 0] interaction; the owner's channel is supported iff the games slope within
  the below-bar stratum (G coefficient + interaction) is > 0. This is the sharpest available
  separation of "selection signal" from "evidence weight", and it is declared before looking.

## 8. THE OPPORTUNITY CONFOUNDER — named, and what the repo can and cannot control

Selection is partly team context: rebuilding teams play kids; contenders don't. What the repo
actually has (searched `data/`, `docs/`, the store, and Layer 1 before this prereg was written):

- Per-season club affiliation: **DOES NOT EXIST**. The store carries `_draft_club` (club that drafted
  the player) and current `afl_club` / `affl_team` only. No season-by-season club history.
- Historical AFL ladder / team win-rate data: **DOES NOT EXIST** anywhere in the repo (every "ladder"
  hit in data/docs is the discount ladder or a metaphor).

Ruled consequence (per the brief: do NOT fake one): the available control is
**draft_club × focal_year fixed effects** — exact for players still at their draft club in the focal
season (the large majority at k ≤ 3), misattributed for early movers, and the movement rate is
UNOBSERVABLE in this store; that limitation is disclosed, not patched. Spec 2 is reported with and
without these FE. If the games coefficient survives draft_club × year FE, within-club-cohort variation
carries it; if it collapses, the effect is confounded with club context and is reported as
**"exists but opportunity-confounded — unresolved"**, with the plausible bias direction bounded in
prose (rebuilding clubs grant more games AND may face weaker internal competition for selection, which
biases the naive games coefficient — sign of the bias argued, not measured, because the data to
measure it is not in the repo).

## 9. Named rows

kye-annand (9g @ 59.8, MSD KPD, age 23), lukas-cooke (2g @ 43.5, same cell), cooper-duff-tytler
(13g @ 50.3, ND4 KPF, 19), harry-dean (17g @ 59.7, ND3 KPD, 19), milan-murdock (17g @ 70.1, SSP SF,
26) — each is read through whatever the historical cells say: the historical Y5 distribution of their
(games tercile × surplus band × pedigree band) cell, and the counterfactual read at the other games
terciles at their own surplus.

## 10. If the effect is real — wiring sketches (AWAITING RULING, not wired)

2–3 candidate forms will be sketched in the packet, each honouring the **no-double-counting
constraint**: games already drive ρ, so any proposal must isolate what is NEW beyond ρ's channel
(H5 is the measurement of exactly that residual). Nothing is wired at this seat.

## 11. Honesty commitments

Dispersion on every estimate; a null is a result; every exclusion named and counted; full tables in
the packet; the in-progress-2026 rule and the censoring rules above are the complete observation-
window law — no other row is dropped.
