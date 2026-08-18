## X · WHAT WAS NOT BUILT, AND WHY — SAID IN ADVANCE ON THE PREREG, NOT AS AN EXCUSE AFTERWARDS

The full grid is 3 percentiles × 3 `BETA_sat` × 2 FIX A = **18 cells. TWELVE were built.** The six
that were not are named here and were named on `PREREG_R.md` before the first build.

| not built | why |
|---|---|
| **(p5, b1, A on)** and **(p5, b2, A on)** | the A-on reading of the BETA lever at p5. FIX A's increment is measured at four other points — p5/b0 (`RB1`→`RAB1`), p15/b0 (`R15`→`R15A`), p20/b0 (`R20`→`R20A`) and p20/b2 (`R20b2`→`R20b2A`). If A's increment turned out to depend on the BETA lever by more than the materiality threshold, the omission would have mattered; §Y reports whether it does. |
| **(p15, b2)**, **(p20, b1)** and their A-on partners | the interior of the 3×3 lever grid. Cells `RB1`/`R15`/`R20` give the TMAX lever at fixed b0; `RB1`/`Rb1`/`Rb2` give the BETA lever at fixed p5; `R15b1` and `R20b2` give two diagonal readings of the interaction. §Y reports whether the diagonals are close to the sum of the two single-lever moves — if they are, the interior is interpolable and the omission is harmless. |
| **any cell WITHOUT FIX B1** | the order fixes B1 as the base for every variant. B1 is settled and independent and this order does not re-litigate it. |
| **`LAMBDA` re-solved** | see the disclosure below. It is a real choice and not an oversight. |
| **FIX B2 in any combination** | ORDER Q priced B2 and the order fixes B1 as the base. No ORDER R cell carries B2. |
| **`BETA_sat` above ORDER P's point estimate** | the owner ruled the charge should be SOFTENED. Stiffening it was not asked for and is not priced. The dial would accept it up to the CI ceiling; nothing was built there. |
| **any `TMAX` percentile other than 5, 15 and 20** | the owner named 15 and 20. The dial HALTS on anything else rather than letting a percentile be invented at the command line. |

---

## Z · EVERY DISCLOSURE, AND EVERYTHING THIS SEAT COULD NOT MEASURE

- **NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED. NO PULL REQUEST WAS OPENED.
  NOTHING WAS PUSHED TO `main`.** This seat delivers prices.
- **`LAMBDA` IS NOT RE-SOLVED, AND THAT IS A CHOICE.** On ORDER P, `LAMBDA` was SOLVED by an
  anchoring identity: bisection so the new charge removes exactly the same total points from the
  year-1 class-mark population as ORDER K's blind charge did. **Moving `BETA_sat` or `TMAX` BREAKS
  that anchor.** This order holds `LAMBDA` fixed because the order says to, and because re-solving it
  would claw back exactly the softening the owner asked for — holding the total constant is the
  anchor's whole job. **The consequence is that every variant here removes LESS total charge than
  ORDER P by construction. That is the softening.** It is on the prereg and on the engine banner.
- **The premium surface `PG` IS NOT REFITTED.** It is ORDER P's published grid, byte for byte.
- **`s0` IS NOT MOVED.** `T(s0) = 1` on every board, so a row at the cohort centre pays the same base
  charge everywhere. Only the cap and the slope move.
- **The BETA lever is NOT a pure softening.** §3. It stiffens the charge by up to 1.4472% of the
  pedigree leg over a 1.65-point-a-game window just above the cohort centre. Measured, not asserted,
  and printed on the engine banner of every board that carries it.
- **THE PERCENTILE IS UNWEIGHTED.** `s_p5` in `MECH_P.json` is an unweighted `np.percentile` over the
  4,143 season rows, while `s0` is a GAMES-WEIGHTED mean over the same rows. **That inconsistency is
  ORDER P's, not this order's**, and it is carried unchanged so p15 and p20 are the same kind of
  object as the p5 they replace. Changing it would have made the three percentiles incomparable.
  **It is disclosed rather than silently harmonised.**
- **The percentile is of SEASON ROWS, not of players.** A player with six seasons contributes six
  rows. That is ORDER P's population and it is carried unchanged.
- **There is no hold-out.** These variants act on ORDER P's premium surface, which is estimated on the
  same board's `v0` it is applied to. ORDER P disclosed that and it is unchanged here.
- **The position test is READ-ONLY and built no board.** It measures whether a per-position premium
  is supportable. It does not build one, and this order does not propose one.
- **The position test's bootstrap is over PLAYERS, not seasons**, on ORDER P's own seed 32. Resampling
  seasons would have understated the spread and made the intervals look narrower than they are.
- **RUCK's bootstrap interval is degenerate** (upper limit +918.83). That is reported as a degenerate
  interval, not trimmed to look like a wide one.
- **The three draft classes over 1.14 are ORDER P's breach and this order does not repair them.**
- **The `run_panel.sh` / Guard 5 lane does not pass on this branch and did not pass before this
  order.** The register's v737 entry records five stale pins on `land/order-29`, all predating
  ORDER P. This seat has not touched the workspace, `data/expected_boot.json` or
  `engine/forward_valuation`. The `engine_head` pin necessarily moves again because this order edits
  `_merged_recover.py`; re-stamping it is a landing act and this order lands nothing.
- **Every board was built through `bbR.sh`**, which pins the store, the engine, the
  forward-valuation tree and the five thread variables explicitly and prints their md5s on every run.
  **The store is `cb38ef11` on every board, unchanged.**
- **The two control matrices were REUSED, not re-emitted.** `per_entrant_QB1.json` is this order's
  `RB1` (p5/b0/A-off) and `per_entrant_QAB1.json` is its `RAB1` (p5/b0/A-on), both built by ORDER Q
  from the identical dial line. Re-emitting them would have burned nine minutes reproducing a file
  byte for byte. **Declared here rather than left to be noticed.**
- **ORDER K has no census run of its own.** Its charge factor is the `f_K` field the leg recorder
  captures on every board — the same object, computed by the engine at the same call site in the same
  clock state — and the whole-arc movers file reads it off the ORDER P census.
- **The owner's path test reads years 6 and 7 on FEWER ROWS than year 1.** A cohort only has a year-7
  cell if it drafted seven years ago. On MODERN picks 1-20 the counts run 100/100/100/100/100/80/60/40
  across years 0 to 7, so limb (b) is read on 40 of the 100 rows that produced the year-1 breach.
  **That is a real weakness in the test and it is stated rather than buried.** Per-cell counts are in
  `PATHTEST_R.json` under `n_included`.
- **The whole-arc movers page compares boards with DIFFERENT TOTALS.** ORDER K is 673,097 and ORDER P
  is 666,434, so most rows fall in absolute points for a reason that has nothing to do with any
  individual player. **RANK is the fair comparison. Absolute points are not.** That warning is at the
  top of the page, in the CSV documentation and in the JSON summary.
- **The "spanning variant" in the movers page is NOT a recommendation.** It is the far corner of the
  grid. This seat recommends nothing.
- **NO NAMED-PLAYER TARGETS.** Not one constant in this order was chosen with any row in view and no
  row's value is an acceptance criterion. Named rows are consequences only. This is a standing
  prohibition in this project after a real error.
- **The veteran board (RL_O33) is still parked.** Nothing here touches it.
