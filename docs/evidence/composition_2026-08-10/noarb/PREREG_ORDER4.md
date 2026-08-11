# PRE-REGISTRATION — ORDER 4, THE EXPOSURE-WEIGHT DESIGN

**Filed BEFORE the step-1 grid was computed.** The decision rule below is fixed here so it cannot be
chosen after seeing the numbers. A breach is reported as a breach; nothing is retuned to rescue a
prediction.

**Disclosure of what was already known when this was written.** ORDER 3b already produced the POOLED
tenure-level figures that raised the suspicion — at tenure 1, exposure-weighted 58.20 against
survivors-only 57.93 and as-built 51.99. Those six pooled rows were in hand. The per-band grid, the
weight-share statistics and the fourth estimator below were NOT, and they are what the rule decides on.

---

## STEP 1 — THE DISCRIMINATING HONESTY TEST

### The suspicion being tested against

Exposure-weighting down-weights low-exposure seasons. Busts and faders have low exposure. So
exposure-weighting may be survivor bias re-entering under a new name — the exact failure mode this
project's last eight weeks are full of. **The design must be assumed guilty until the grid clears it.**

### The four estimators, all on the same par cohort

Every one is computed from the identical row set that `par_build.gather()` collects — the par cohort's
(position × tenure) played seasons, target `CP._lvl_wt(p, Y)`, no re-invention:

| | sample | weight |
|---|---|---|
| **(i) as-built** | every ever-establisher's played season, `g >= 1` | equal |
| **(ii) exposure-weighted** | **same as (i)** — nothing dropped | `min(g, 18)` |
| **(iii) old survivors-only** | seasons with `g >= 6` | equal |
| **(iv) the discriminator** | seasons with `g >= 6` | `min(g, 18)` |

**(iv) is the estimator that makes the test sharp, and it is added here rather than in the order.**
(ii) and (iii) differ in TWO ways at once — the sample AND the weighting — so "(ii) ≈ (iii)" alone
cannot say which one did it. (iv) holds the sample at survivors-only and applies the same weighting,
so **(ii) vs (iv) isolates the contribution of the sub-6-game seasons under exposure weighting.**

### THE DECISION RULE — fixed here, before the grid

**Criterion A — the order's own test.** Per cell (tenure 1-6 × band, and pooled), let

> `R = |(ii) − (iii)| / |(iii) − (i)|`

R is the residual distance to survivors-only as a fraction of the gap the design is meant to close.
**"Coincides" means R < 0.10.** Cells where the gap `|(iii) − (i)|` is under 1% of (iii) are
UNINFORMATIVE (there is nothing for the design to close) and are excluded from the verdict, with their
count reported rather than hidden.

**Criterion B — the mechanism test.** The share of total fit weight carried by the sub-6-game seasons
under exposure weighting, set beside their share of the sample COUNT. If the weight share is **under
2%** pooled while the count share is materially larger, the weighting has de facto re-dropped the rows
the #336 repair added.

**Criterion C — the discriminator.** If **|(ii) − (iv)| < 0.5%** of (iv) across tenures, the added
sub-6-game rows contribute essentially nothing once exposure-weighted.

### THE VERDICT, pre-committed

- **DESIGN DEAD** if Criterion A coincides in **every informative cell**, OR Criterion B fires, OR
  Criterion C fires. In that case: report the finding, **do not wire anything**, stop at step 1.
- **DESIGN PROCEEDS** only if (ii) tracks (iii) at tenure 1 but **diverges materially at later
  tenures or in identifiable bands** — and then the report must say exactly WHERE the busts still
  carry weight, not merely that they do.
- Any other pattern (e.g. (ii) overshooting past (iii)) is reported as measured and returned for a
  ruling rather than being read as a pass.

### A weighting choice that must not be hidden

`CP._lvl_wt(p, Y)` reads **every season from debut to Y**, games × recency weighted. So a par
observation at tenure T is a CAREER-TO-DATE level, not that one season's average — except at tenure 1,
where the window contains only the debut season. Two weights are therefore defensible and **both are
computed and reported**:

- `w = min(g_season, 18)` — that season's own exposure (what ORDER 3b sized), and
- `w = Σ g·recency` — the exposure actually behind the target, i.e. the precision of the estimate.

Reporting only the one that flatters the design would be exactly the failure this test exists to catch.
The uncapped variant is reported too, so the cap is not doing hidden work.

---

## THE CONCEPTUAL QUESTION — what is a par an expectation OVER?

To be answered in plain language in the memo **independently of the outcome**, because the owner needs
the concept, not just the arithmetic.

- **Equal-weight over seasons** answers: *"in a typical SEASON by a player of this pedigree, what was
  the level?"* — every season counts once, a one-game cameo as much as a full year.
- **Exposure-weight over games** answers: *"in a typical GAME played by a player of this pedigree,
  what was the level?"* — every game counts once.
- **Survivors-only** answers: *"in a typical season THAT WENT WELL ENOUGH TO REACH SIX GAMES, what was
  the level?"* — the question the owner already ruled out.

**The pre-registered argument, which does not depend on how the grid falls.** Par is consumed as a
denominator against player statistics that are THEMSELVES games-weighted: ITEM C's evidence weight is
`Q = sa/par`, and `sa` is the career **games-weighted** average (`_c_career`, `_merged_recover.py:2075-2080`
— `gt += games; num += games*avg`). An equal-weight par therefore divides a games-weighted numerator by
a season-weighted denominator. That is a unit mismatch and it exists whichever way this grid falls.

**That argument is NOT a licence.** A correct unit does not make a biased sample honest. If the grid
says exposure-weighting reproduces survivors-only, the design is dead regardless of how good the unit
argument is, and the unit mismatch becomes a separate finding for the owner rather than a route to
re-admitting survivor bias.

---

## STEP 2 — ONLY IF STEP 1 CLEARS THE DESIGN

Dial `RL_336_XW`, default OFF, byte-exact when off. Bust inclusion PRESERVED: every row in the #336
sample stays in the sample; the dial changes weights only and drops nothing.

- **P4.1** — yr1 RISES. The par leg owns 89.2% of the +0.1018 #336 give-back, and exposure weighting
  restores roughly the whole tenure-1 par gap. Predicted yr1 **1.05 – 1.11**.
  *Falsifier: yr1 at or below FULL's 0.9974, or above 1.11.*
- **P4.2** — yr4 approximately unchanged. Predicted within **±1.0%** of FULL's 1.5310.
  *A move beyond that is a BREACH and is reported as one.*
- **P4.3** — **0 year-zero anchor movers** beyond the 1 pre-existing row seen in every arm.
  *Falsifier: 2 or more v0 movers, or sum(v0) beyond 0.05%.*
- **P4.4** — the amendment-2 monotonicity guard must not gain failures. The reference config already
  fails 1 cell (KPD band 0, −0.59%). *Falsifier: 2 or more failing cells in the emitted arm.*
- **P4.5** — margin printed against the unchanged 14.00% charge; no prediction on its size. A yr1 lift
  toward 1.11 would put appreciation near 11% against 14% charged, so the margin should stay POSITIVE
  (legal). *Falsifier: a negative margin, i.e. the design opens an arbitrage.*

Identity at final HEAD with the dial off: matrix `recs` byte-identical and board md5 unchanged, or
nothing above may be read.
