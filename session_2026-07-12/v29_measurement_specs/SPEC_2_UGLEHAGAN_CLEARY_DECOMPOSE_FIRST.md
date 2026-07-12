# SPEC 2 — UGLE-HAGAN / CLEARY DECOMPOSE-FIRST ATTRIBUTION — v2.9 investigation spec · 2026-07-12
### Register item 6 (OPEN_ITEMS v8) · TIER-3 spec (design only) · FABLE
### Owner reads: jamarra-ugle-hagan 196 "a bit low" · caiden-cleary 779 "a bit high".
### Mandate: layer-by-layer attribution, SIZED PER LAYER, before any fix is proposed.

## 0 — SUBJECTS AS THE BOARD CARRIES THEM (verified this session, board 9ecbe0fa)
**jamarra-ugle-hagan** — KEY_FWD, ND 2020 **pick 1**, born 2002-04-04 (24), 70 games, ev **196**.
Line: 47.0(5g) → 44.0(17) → 60.6(23) → 63.8(22) → **2025 ABSENT (no scoring row at all)** → 26.0(3g, 2026).
Two engine facts that kill the obvious theories immediately:
- He is **NOT in the LTI/availability register** (`_avail_hc`=0.0, no `_lti_reg`). The "absence
  machinery" of register item 6 is NOT the Part-1 availability layer — his absence is digested by
  the ordinary FORM machinery (recency level + qualification counts).
- He is **NOT floor-bound**: `ev_prefloor` = 196 = ev; the B5 floor at year-6 would be 106. The 196
  is the form machinery's own answer, not a clamp.
**caiden-cleary** — MID drafted, **priced as GFWD** (`future_position` GFWD), ND 2023 pick 24
(Academy), born 2005-03-05 (21), 21 games, ev **779**. Line: 28.8(5g) → 45.0(12) → 60.8(5, in-progress).
Qualifying seasons (≥10 games): exactly ONE (2025) → nqual=1 → the thin-career blend prices him
**0.25 × current level + 0.75 × pedigree par prior** (pick-24 GFWD par at his tenure).

## 1 — PILOT LAYER SIZINGS (read-only in-memory counterfactuals, this session — these become the
##      spec's expected magnitudes; the v2.9 job re-runs them as the attribution ladder's spine)
| JUH counterfactual | ev | Δ vs as-is |
|---|---|---|
| as-is | 196 | — |
| 2025 played at his 2024 level (22g @ 63.8) | 634 | +438 |
| 2026 cameo removed (2025 still absent, no 2026 row) | **1056** | **+860** |
| 2026 cameo extended to 10g @ 26.0 (nqual flips 3→4) | **106** | **−90** |
| 2026 on-pace return at former level (13g @ 63.8) | 726 | +530 |
| never-absent twin (2025 @ 63.8 + 2026 13g @ 63.8) | 812 | +616 |
Readings, each a designed measurement below:
(a) **The 3-game 26.0 cameo, not the missing 2025, is the dominant suppressor (−860).** With the
KEY-group recency decay LDECAY=0.40, a 3-game current-season sample carries more weight than the
entire 2023–24 demonstrated level. (b) **Non-monotone in evidence:** a man who never returned
(1056) prices ABOVE the man who returned and played 2026 at his demonstrated 63.8 (812) — absence
falls back to pedigree-anchored paths (pick-1 V0) while ANY return evidence pins to production.
(c) **Qualification cliff:** 7 more games at the same 26.0 would CUT him 196→106 (nqual 3→4 flips
him from the thin-career par-prior blend into the full down-branch shed). (d) The engine's own
"honest" price of his demonstrated level at 24, had he simply kept playing, is ≈ 800–1050 — the
196 is ~600–850 below every counterfactual in which 2025–26 are ordinary seasons.

## 2 — MEASUREMENT DESIGN
**M-A · The attribution ladder (both players; deterministic; G-ATTR discipline).** Freeze the
engine; price a single-change ladder from as-is to a declared reference profile, one layer per
rung, Δ recorded in SC points, rungs sum to the total gap:
- JUH rungs: input representation (2025 absent-row vs zero-games row vs played) · cameo weight
  (2026 row in/out; games 3→10→13; avg 26→63.8) · nqual state (3 vs 4: thin-blend vs down-branch)
  · recency decay (KEY 0.40 — sensitivity ±band) · par-prior leg (pick-1 KFWD par at 0.25 weight)
  · M3 in-progress blend (s=0.727 at 3 games) · staleness gates (el/onset — verify inert) · KPF
  machinery (exempt: nqual<4 — verify byte-inert) · floor (verified non-binding).
- Cleary rungs: par-prior weight (n=1 ⇒ 75% pedigree) · position basis (priced GFWD REPL 70.9 vs
  drafted-MID 80.1 — re-price under each) · pole/upside term (age-21 wage 0.83 × tenure-3 tfade
  0.40 × exposure gate) · in-progress 2026 credit (5g @ 60.8: the _coreM1 f1 fractional credit +
  M3) · iso_corr(pick 24) · convexity (\_cvx = 1.0 — verify inert).
Output per player: ONE table, layer → points → which of the owner's "too low/too high" it feeds.
**M-B · The evidence check behind the two big layers (walk-forward; the part that can move dials).**
1. **Absence-return calibration (JUH's layer (a)/(b)):** cohort = players with ≥2 qualifying
   seasons who then have a FULL season with zero games (any cause: injury absences from the games
   record; the rare non-injury sabbaticals cannot be distinguished in-store — POOLED AND DECLARED)
   and who return. Estimand: forward delivered level (Y_return+1..+3, engine ruler) as a fraction
   of pre-absence demonstrated level, kernel over age. Question the board is implicitly answering
   today: JUH at 196 ⇒ the engine expects ~scrap forward output. Does the comeback population
   support that, or do returners revert toward pre-absence level?
2. **Cameo-return weighting (layer (a)/(c)):** within the same cohort, does the FIRST-return
   partial season (<10 games) predict the following full season better than the pre-absence level
   does? If pre-absence level dominates, the 0.40-decay's cameo dominance and the nqual cliff are
   measured-wrong for returners; if the cameo dominates, 196 is honest.
3. **Academy/rising-thin calibration (Cleary):** cohort = nqual≤1 players at age 20–22 with a
   rising in-progress line, priced heavily off the par prior. Estimand: delivered Y+1..+3 value vs
   the price's par-prior component. Tests the 75% pedigree weight at n=1 — Cleary's "a bit high"
   is the claim that 0.75 × pick-24 par overpays a 21-game evidence base.

## 3 — EXACT DATA CUTS
- Store 04f38dad basis (re-pin at fire time); extraction seasons Y ≤ 2022 so +3 outcomes complete
  by 2025 — leak-free vs the 2026 board. WALK-FORWARD BASIS: asserted by CODE READING of the
  extraction script (evaluation at Y reads only ≤Y), per the G-COHORT basis rule.
- M-B1 cohort cut: absent-season = list-year with zero scoring rows or zero games; pre-absence
  demonstrated level = games-weighted mean of the last 2 qualifying seasons; ages 21–28 at return;
  positions POOLED (KEY cell shown — JUH is KFWD and KEY careers mature late; POOLING DECLARED).
  Expected n: SMALL (tens). Thin-slice doctrine: pool to the coarsest cut that reaches eff-n ≥ 35
  per kernel node, and DECLARE every pool in the output; if even pooled n < ~25, report the raw
  event list itself (finest resolution the sample supports IS the list) and hand the owner names,
  not curves.
- M-B2: same cohort, first-return seasons with 1–9 games vs 10+; outcome = next season level.
- M-B3 cohort cut: nqual ∈ {0 with f1-credit, 1} · age 20–22 · pick 15–40 · any position (GFWD
  cell shown); event seasons 2010–2022; outcome Y+1..+3 delivered vs priced components.
- Both lenses (15% live + undiscounted) on any value-denominated quantity.
## 4 — TEST DESIGN
- M-A is deterministic engine arithmetic — its "test" is G-ATTR completeness: rungs sum to the
  total gap (tolerance: rounding only), every rung reproducible from the committed script.
- M-B: kernel-smoothed estimands with cluster-bootstrap bands (B=1000, by player). Support standard
  = bands-separate (the l7hinr convention), informing the owner; NO pre-registered statistical
  acceptance gates (doctrine). Each estimand is reported alongside what the CURRENT board implies
  for the same quantity, so the owner reads "engine says X, history says Y" per layer.
- Named-row closure: after M-B, re-state JUH's 196 and Cleary's 779 as (layer table) + (which
  layers history supports / contradicts / cannot resolve at this n). Any dial change is a SEPARATE
  v2.9 lever job with its own candidate + gate run — this spec ends at attribution.

## 5 — EXPECTED CONFOUNDS
1. **Absence cause is unobservable in-store** (injury vs personal vs suspension) — the comeback
   base rates may differ by cause. Control: none available in the pinned store — POOL AND DECLARE;
   flag to the owner that JUH's case (non-injury) is being priced off a mostly-injury pool. The
   LTI register (R-REG=R2) covers current absences only, not history.
2. **Return-year selection** — players who return AT ALL are the survivors of absence; delisted
   non-returners never enter the return cohort. For pricing a player who HAS returned (JUH has: 3
   games) this conditioning is correct, not a bias — state it.
3. **JUH's 2026 cameo quality** (26.0 on 3 games) — tiny-sample level estimate inside the event
   itself; M-B2 measures exactly whether such samples deserve their current weight. Sensitivity
   rung in M-A: avg 26.0 ± 15.
4. **Cleary's position flip** (drafted MID, priced GFWD) — par priors and REPL bars differ by 9.2
   pts; if the flip date is mid-history his early seasons were played in a different role. Control:
   M-A prices both bases; the owner's read may partly BE a position-basis read.
5. **In-progress season** (both: 3g and 5g, M3 live) — run every M-A rung at season-complete
   convention as well; the owner rules on the season-complete table, the live table shows drift.
6. **Age boundary** (JUH is 24.2; KPF compression starts at 24 AND nqual≥4) — one more qualifying
   season flips TWO regimes at once (down-branch + KPF-established). The ladder must show the
   regime map, not just today's cell, or next season's re-price will look like a mystery move.

## 6 — REFUTATION CLAUSE (owner doctrine §49)
Both reads can lose. JUH: if returners in M-B1 deliver ≈ scrap (the engine's implied forecast),
196 is measured-honest, the "a bit low" is refuted, and the finding is filed as absence-machinery
VALIDATED (the cameo-dominance and non-monotonicity of §1 would then be quirks with the right
answer, flagged for hygiene only). Cleary: if M-B3's thin-riser cohort delivers ≥ its par-prior
component, 779 is honest and "a bit high" is refuted. The pilot magnitudes in §1 are hypotheses
about WHERE the price comes from, not verdicts that it is wrong.

## 7 — IMPLICATIONS (mandatory)
- **The absence question generalizes.** The same form-machinery path prices every future full-season
  absentee (contract holdouts, personal leave, long suspensions). Today that path produces: cameo
  dominance (−860 on a 3-game sample), an evidence non-monotonicity (returning at your demonstrated
  level prices BELOW never returning), and a 7-games-from-now cliff (196→106 at nqual 4). Whatever
  M-B says about the LEVEL, these three shapes are candidate mechanism defects — any fix is a
  form-machinery lever (recency floor for returners / absence-aware nqual / cameo shrinkage),
  NEVER a JUH hand-edit or a "returnee multiplier" (blanket multipliers forbidden).
- **Guard/anchor contacts of any eventual fix:** softening cameo dominance touches every low-games
  current season (M3/SEASON_PROG interplay — B6 "more games at the same rate never worth less" must
  survive; §1(c) is PRIMA FACIE adjacent to a B6-style violation and must be re-checked under any
  change). A-FADE untouched (faders are at-floor). G-COHORT: returners are years-4+ — lifting them
  lifts the numerator (adverse direction) — re-measure walk-forward if a lever ships.
- **Cleary connects to two live v2.9 items:** the par-prior leg he rides is PICKEQ/par machinery —
  the PVC option (b) re-expression and the SSP 92→~51 line move the SAME surfaces (his pick-24 par
  under the derived curve is +37–56% richer mid-round — his "a bit high" would get WORSE under
  option (b) unless the thin-career weight is also examined). SEQUENCE: this attribution must land
  BEFORE the PVC adoption job re-prices him, or the owner will be reading a moved target.
- **The register's own framing is confirmed by the pilot:** "likely the absence machinery" — yes,
  but the operative absence machinery is the RECENCY/QUALIFICATION core, not the LTI layer. The
  v2.9 lane fencing should route any fix through the form-machinery owner (M1/M3 lineage), not the
  availability build.
- **Cost of not running it:** JUH re-prices catastrophically on his next 7 games whichever way they
  go (±90 to ±600 swings across §1's counterfactuals) — the owner would be reading unexplained
  moves on a name he has already flagged, with no layer table to point at.
