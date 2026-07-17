# ADVERSARIAL REVIEW — THE PVC RE-DERIVATION CONSTRUCTION (second opinion requested)
2026-07-17 · prepared by the supervisor seat for a cross-model review · **REVIEW, not redesign**

## Your role
You are reviewing a proposed method before it is built. Treat everything below as claims to attack.
Your findings will be handled as HYPOTHESES and independently verified — so be specific and concrete.
Do not redesign from scratch unless you find a fundamental flaw; if you do find one, say exactly what
breaks and under what conditions.

## The system (context you need)
An AFL SuperCoach dynasty valuation engine prices every player and draft pick in one currency
(pick 1 ≡ 3,000 by definition). Player values come from a calibrated model over real production;
a walk-forward book records each player's "as-of" value at the end of each calendar year using only
information available at that time. Draft picks 1–80 must be priced consistently with players.
Roughly: many midfielders are drafted, fewer key-position players, few rucks; positions have
different replacement levels and career shapes. Picks and future-year picks are tradeable assets.

## The defect being cured (measured, not assumed)
The shipped pick-value curve (PVC) was fitted to each drafted player's value at the END OF HIS FIRST
YEAR. Two measured problems:
1. **Circularity.** 1,093 of the 2,083 players in the derivation pool (52%) had played ZERO games by
   that date, so their "value" was the engine's pick-based prior read straight back out — the curve
   was partly fitted to its own output. This worsens with pick depth (9.5% of picks 1–3 are such
   poles; 66.9% of picks 49–99).
2. **Survivor blindness.** The fit reads one year-1 cross-section and smooths with a MEDIAN kernel,
   so what survivors become (peak values 1.7×–2.7× their year-1 value, ratio U-shaped in pick) is
   structurally invisible. Measured residuals against day-after player values are sign-changing:
   picks 1–41 sit −1.6%..−6.2% (curve slightly rich), picks 51+ sit +36%..+54% (curve far too poor).
   The shipped curve also has 15 flat spots (e.g. pick 1 = pick 2 = 3,000) violating a
   strict-descent requirement.

## The proposed construction (what you are reviewing)
**"The composed pathway construction":** the holder of pick p receives a draw from the players
available at that slot, so
  **PVC(p) = Σ_position P(position | pick p) × E[pathway value | position, pick p]**
where:
- **Pathway values are fitted from realized career trajectories** — each drafted/recruited player
  2004–2024 contributes his walk-forward as-of values at end of years 1, 2, 3, … at his real
  outcomes. **Busts carry full weight**: a pick-40 player delisted by year 3 contributes his low
  years then zero; the expectation over outcomes at each slot is mostly busts late, and that is
  what makes late picks cheap. No survivor-only pool, no games floor, no eligibility threshold.
- **Evidence weighting is continuous**: a player-year with real production weighs more than a
  prior-dominated year; the weight fades smoothly with the prior's share — never a hard cutoff.
- The fit is 2-D (pick × career-year), at per-exact-pick resolution, kernel-smoothed (non-median,
  so the convex survivor tail is not flattened).
- **PVC(p) is the year-0 point of the fitted trajectory** — the curve of years 1/2/3+ continued
  back to day one.
- **Entry-end closure:** a zero-evidence draftee's day-after value V0 is then SET FROM this curve
  (definitionally equal). The old circularity becomes harmless because the curve's content now
  comes from outcomes, not from itself.

**Binding constraints the result must satisfy:**
- Strictly descending: curve(p+1) ≤ curve(p) − 1 for p = 1..79 (all 15 shipped flat spots must clear).
- Smooth in pick; no thresholds anywhere in the construction (hard rule of this project).
- Numéraire pin: curve(1) = 3,000 exactly.
- **The day-after identity, population level:** composition-weighted mean day-after player value must
  match the curve within **2% POOLED across the whole 2004–2024 sample (HARD gate)**. Individual
  draft classes may deviate freely (a top-heavy or weak class is not a breach). A per-exact-pick
  kernel-smoothed residual curve is REPORTED for human review (not gated).
- Offline derivation into a stamped artifact, loaded at runtime (no import-time refitting).
**Named fallback if constraints prove unreachable:** a simpler two-ends blend (entry end from pick
pricing, evidence end from late-career production, continuously weighted) — the comparison would be
committed as evidence.

## Questions for you (answer each; number your findings F1, F2, …)
1. Does the entry-end closure (V0 := curve for zero-evidence entrants) hide any problem — e.g. does
   it make the 2% pooled gate vacuous, or leak the prior back into the fit anywhere?
2. The 2-D fit: what estimator risks do you see (thin deep-tail data, ~21 players per exact pick at
   the top, pick×year interaction, kernel choice)? What would you demand of the estimator spec?
3. Busts: is full-weight inclusion at real outcomes sufficient, or do you see a selection effect we
   have missed (e.g. list-management truncation, mechanism differences ND vs rookie draft)?
4. Does reading PVC as the year-0 point of a trajectory fitted to years 1+ introduce an
   extrapolation bias at year 0? How would you bound or test it?
5. The composition weighting P(position | pick): estimated from 21 drafts — any instability or
   drift concern (position-label changes across eras, flex/dual-position players)?
6. What validation would you demand before trusting this curve (beyond the constraints above)?
7. Is the named fallback sensible, and under what measured condition should it trigger?
8. Anything fundamentally better we have not considered, given the stated intent: "reasonably and
   correctly value each pick and pathway to reflect its value to the holder of that pick"?

## What NOT to do
Do not propose survivor-only pools, games floors, or any hard threshold (banned by standing law).
Do not price picks off market/trade sentiment (the engine is the pricer). Keep findings concrete:
what breaks, where, how you'd detect it.
