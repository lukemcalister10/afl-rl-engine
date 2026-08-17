# PACKET — ORDER 33 SEAT W4: THE TRAJECTORY NULL, RE-POSED ONCE. IT HOLDS.

**Seat:** W4 (measurement, READ-ONLY — nothing in the engine, board, or law was touched).
**Program brief:** issue #334 comment 5312369107. **Prereg:** `PREREG_W4.md`, pushed before any
result; one amendment (A1, quantile bootstrap size only), filed before the run.
**Verdict, by the rule fixed in advance: O3 — NULL CONFIRMED.**

---

## 1 · What was asked

The candidate prices a player's production evidence as an evidence-weighted **LEVEL**. A player who
went 40→55→70 over three seasons is priced identically to one who went 70→55→40. The license for
that came from ORDER 30B-M (re-run under 31-F): a trajectory form lost to the level form. But that
original test was a **pick-conditional** trajectory (12 extra parameters asking whether the growth
curve differs by draft class), on **4,033 ND-only states**, with **no age adjustment** — and its own
packet admitted *"the trajectory question cannot be settled by cells — there are not enough of
them."* The owner and supervisor's standing discomfort: that null deserved one properly-powered
re-pose before being accepted forever. This seat is that re-pose — designed to give trajectory its
best legitimate shot, and preregistered so the answer binds either way.

## 2 · How the re-pose was made stronger (all fixed before results)

| dilution in the original | fix here |
|---|---|
| trajectory entered as a 12-df pick-class interaction | **one degree of freedom**: the last-2-season slope itself |
| no age adjustment — a 20-year-old's rise fought the age curve | slope measured **net of the population age-expected change** at his age × position (the age curve was built from the same store: rises of ~+40–55 pts/season through 24, cliff to −50…−90 after 29) |
| ND picks 1–64 only, n=4,033 | **the whole store**: every entry type, 2005–2026 → **7,924 states / 1,445 players** on the primary target |
| benchmark was a plain level form | benchmark is the **best convex level weighting** `L_w`: current and prior seasons blended with weight w chosen per training fold. This absorbs the mean-reversion trap — "recent seasons are noisy reads of the level" is the benchmark's job, so trajectory only wins if **direction per se** predicts beyond every such blend |
| one 6-year target only | three: **(a) next-season output** (primary, max power), (b) 3-yr discounted value, (c) the original 6-yr target |

The chosen benchmark weight came out at **w\* ≈ 0.45–0.5 in every fold**: the best level-only
predictor already blends roughly 2 : 1 : ½ across the last three seasons. That IS the shrinkage a
naive "trajectory" test would have faked its wins against; here it was conceded to the level side
before trajectory was scored.

Distinct object, kept distinct: the ORDER 30B-R **recency games-clock** failure (a decaying weight
on the *evidence clock*, which lost its own prereg and threw away durability) is a different
question from this seat's *production-shape* test. Neither verdict touches the other.

## 3 · The confirmatory result (primary target: next-season output)

n = 7,924 states, 1,445 players, 5-fold player-clustered CV, decision rule fixed in the prereg.

| | held-out RMS | Spearman |
|---|---:|---:|
| L\* — best level-only | 216.73 | 0.6965 |
| T\* — level + trajectory | 216.56 | 0.6970 |

- RMS reduction **+0.081%** (adoption bar: ≥ 2.0%); folds won by T\* **3/5** (bar: ≥ 4/5).
- Full-sample slope coefficient: **+10.2 points of next season per 1 SD of trajectory**
  (SD = 232 slope points), cluster-robust **t = +2.44** — below the preregistered |t| ≥ 3.0;
  bootstrap 95% CI [+2.2, +18.2].
- Re-pricing consequence if adopted anyway: mean rank movement between the two predictions is
  **0.74 percentile points** — trajectory barely reorders the board at all.

**By the rule set before any number existed: O3 — NULL CONFIRMED.** Secondary targets agreed:
3-yr value t = +0.40; the original 6-yr target t = +2.09 with reduction +0.044% (4/5 folds) —
same whisper, same size, nowhere near either bar.

## 4 · The honesty section — what the whisper is, and why it is not signal about form

A fair reading of the tables shows a residual positive association, and it must be shown, not
buried:

- Median (quantile) regression: **q50 +19.2 per SD, CI [+11.0, +27.6]** — excludes zero. q10 is
  dead flat (−0.15, CI [−1.05, +0.60]); q90 wide and inconclusive (+14.3, CI [−11.2, +35.2]). So
  the association lives in the middle of the distribution, **not** in the tails — trajectory does
  not find breakouts and does not predict floors.
- The owner-readable sort (within age-band × level-quintile, rising vs falling tercile): pooled
  within-cell T3−T1 gap **+21.9 points of next season, CI [+8.4, +34.4]** — real, and small: ~4%
  of a Q4–Q5 season level. Full 28-cell table with dispersion in `MEASURE_W4_out.txt`.
- **The killer: sensitivity s1.** Re-measure the slope in **raw scoring average** (games ≥ 6 both
  seasons, so the games-weight cannot masquerade as form): the coefficient flips to **t = −0.88**
  — nothing. The whisper is therefore carried by **games-count dynamics** (a player whose games
  are ramping up scores more board points next season), not by scoring form. Games exposure is
  already the engine's evidence-weight axis, and the level family with its controls absorbs
  almost all of it — the residual is the +0.08% seen above.
- 3-season slope (s2): t = +0.10. Age localisation: no age band reaches significance (largest is
  22–25 at t = +1.99). Sign split: improvers t = +0.99, decliners t = +1.69 — no asymmetry. Era
  split: null in both halves. The whisper has no home — it is diffuse, tiny, and form-fragile.

Under the prereg these reads are descriptive and cannot overturn; on their merits they wouldn't
anyway — a candidate feature that (i) fails its raw-form construction, (ii) improves held-out
prediction by 0.08%, and (iii) moves prices by three-quarters of a percentile is not a law.

## 5 · The register-ready sentence

> **TRAJECTORY — SETTLED (null, twice).** Within-career shape (improving vs declining) carries no
> pricing signal beyond the evidence-weighted level: tested as a pick-conditional form (O30-BM,
> n=4,033; −0.02% RMS, 2/5 folds) and re-posed once at full power as an age-adjusted 1-df slope
> against the best convex level weighting on the whole store (O33-W4, n=7,924 states / 1,445
> players; +0.08% RMS, 3/5 folds, cluster t=+2.44 < 3.0, raw-average form t=−0.88). The candidate
> prices production evidence as LEVEL ONLY; this question is closed absent new kinds of evidence
> (not merely more seasons of the same).

No wiring proposal is filed — the prereg reserved wiring sketches for a signal verdict, and there
is none.

## 6 · Files

All in `docs/evidence/order33_w4_2026-08-17/` on `land/order-29`:

| file | what |
|---|---|
| `PREREG_W4.md` | the binding design, decision rules O1–O4, amendment A1 — pushed before any result |
| `w4_build.py` / `W4_PANEL.json` / `CENSUS_W4_out.txt` | panel build (engine scorer staged read-only, o30bm convention), the measured age curve, census |
| `w4_measure.py` | the harness: CV compare, cluster SEs, 1000-rep player bootstraps, pinball-LP quantile regression |
| `TRAJ_W4.json` / `MEASURE_W4_out.txt` / `MEASURE_W4_console.txt` | every number above, full fold and cell tables |
