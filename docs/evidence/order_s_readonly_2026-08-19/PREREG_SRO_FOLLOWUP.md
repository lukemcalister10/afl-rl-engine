# PREREG ADDITION — ORDER S READ-ONLY, THE FOUR FOLLOW-UP MEASUREMENTS

**Seat:** ORDER S READ-ONLY. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Extends:** `PREREG_SRO.md` (`09d5e3f`) and `PACKET_SRO.md` (`6625d53`). Same rules, unchanged.

**NO ENGINE EDIT. NO DIAL. NO BOARD. NO STORE WRITE. NO PULL REQUEST. NOTHING ADOPTED.
NO FIX IS PROPOSED IN ANY OF THE FOUR.** Deliverables go only to
`docs/evidence/order_s_readonly_2026-08-19/` as a `FOLLOWUP_` set.

**This file is pushed BEFORE any number in the four measurements exists.**

**Out of scope by instruction.** The injury-stream design — logged-injured absence exempted from the
fade via the owner-authored LTI register — is a live-board wiring question the owner has not ruled
on. **This seat does not touch it.** F1 and F2 are therefore stated in a form usable under EITHER the
current pooled fade or a future injured/unexplained split: every curve is reported as a function of
the observable (games, avg-vs-bar) with no absence-cause term in it, so a later split can re-cut the
same population by cause without re-deriving anything here.

**No named-player targets.** Madden and Conway are exhibits. They gate nothing.

---

## 0 · WHAT IS ALREADY MEASURED, AND WHAT IS NEW

Before predicting anything, this seat records what it found by reading, so nothing below is claimed
as new when it is not.

**ORDER 30A-2 already measured a games transition** (`docs/evidence/sitter_fade_2026-08-14/`, T4:
"THE GAMES TRANSITION — D(k games by depth N), the 0→1 boundary measured not assumed"). It reports
D(k, N) at coarse buckets 0 / 1-2 / 3-5 / 6-10 / 11+, at depths 2, 3 and 4, under two listing
readings, and its own reading was: *"the 0 → 1-2 boundary is a LARGE step but not the largest, and
the sequence is NOT monotone, so the measurement supports neither a clean cliff nor a smooth curve at
this resolution."*

**What F1 adds and 30A-2 did not do:** a CONTINUOUS curve in games rather than five buckets, cut by
AGE BAND and by POSITION CLASS, and expressed on the same [0,1] scale as the wired credit so the two
can be laid side by side. **Where the buckets overlap, 30A-2's numbers are the control this seat
checks itself against, and any disagreement is reported as a disagreement.**

**The estimand differs and that is declared, not discovered.** 30A-2 measured delivered value off the
DV lane's Layer-1/Layer-2 artifacts, which live on `origin/build/delivered-value`. This seat measures
on the **house S4 delivered-value ruler** (`s4_shootout.py`, md5 `241842f6…`) over the per-entrant
matrix, the same ruler ORDER N, P, Q and R all used. **The two rulers are different objects and the
levels will not match. Only the SHAPE is compared, and that is stated here before the run.**

---

## 1 · F1 — THE CREDIT CURVE

### 1.1 The wired object

`o31_played_units` credits `min(1, games/2)` per season against the sitter clock `c_u`. **A two-game
season buys the same full unit of clock credit that a twenty-two-game season buys. A one-game season
buys half.** That is a step at two games, not a curve.

### 1.2 The construction, fixed before the run

**Estimand.** ORDER 30A-2's T4 estimand, on the house ruler:

```
D(g, N)  =  E[ V_from_N / v0  |  the season at depth N-1 had g games ]   /   E[ same | g >= 11 baseline ]
V_from_N =  the discounted sum of house-ruler season values from depth N onward
```

**PRIMARY CELL: depth 2.** At depth 2 the "seasons 1..N−1" window is season 1 alone, so the
cumulative object and the per-season object COINCIDE. **That is the only depth at which the estimand
matches the wired per-season credit without a further control, and it is the largest cell.** Depths 3
and 4 are secondary, and there the prior seasons' games are reported alongside so that a cumulative
reading is not mistaken for a per-season one.

**Population.** ND entrants from 2005 with a positive `v0`, force-majeure keys excluded, on the #338
minimum-listing basis the matrix is emitted on. **Right-censoring rule, declared in advance: the
entry year must be early enough that at least FOUR seasons after the depth being scored are inside
the observed window (to 2025).** For depth 2 that is entry year 2019 or earlier. A sensitivity at six
seasons (2017 or earlier) is run and printed.

**The credit scale.** So the measured curve and the wired step are on one axis:

```
c_hat(g)  =  ( D(g) - D(0) ) / ( D(FULL) - D(0) )          FULL = g >= 11, declared here
c_wired(g) =  min(1, g/2)
```

**Cuts.** Pooled; by TALL/SMALL; by entry-age band (18 / 19 / 20+); per position where the cell holds
at least 40 players, and marked THIN below that. Per-integer games cells 0,1,2,…,10 and 11+, plus
30A-2's own buckets for the control.

**Intervals.** Player-level bootstrap, 2,000 draws, seed 32. One row per player at depth 2, so the
cluster is the row.

### 1.3 Predictions

- **F1-P1.** Predicted: **`c_hat(2)` is materially below 1.0** — a two-game season does NOT clear the
  non-selection signal the way a ten-game season does. **Falsified if `c_hat(2)`'s 90% CI contains
  1.0**, which would vindicate the wired step.
- **F1-P2.** Predicted: `c_hat(g)` rises through the whole range 0 to 11+ rather than saturating at
  2, so the wired step is above the measured curve over 3 ≤ g ≤ 10. **Falsified if the measured curve
  is at or above the wired step anywhere in that range.**
- **F1-P3.** Predicted: **a one- or two-game season predicts closer to a ten-game season than to a
  zero-game season** — i.e. `c_hat(2) > 0.5` — because 30A-2 already measured the 0→1-2 step at +0.39,
  46% of the whole 0→6-10 range. **Falsified if `c_hat(2) < 0.5`.** *(F1-P1 and F1-P3 are deliberately
  a squeeze: this seat is predicting the truth is in between and that BOTH the current step and "a
  2-game season is a 0-game season" are wrong.)*
- **F1-P4.** Predicted: the curve is NOT monotone at per-integer resolution, because 30A-2's bucketed
  version was not monotone and per-integer cells are smaller. **Falsified if it is monotone.** This is
  a prediction about noise and it is written down so a non-monotone result is not read as a finding.
- **F1-P5.** Predicted: the age and class cuts will NOT separate — no two age bands' or class curves'
  intervals will be disjoint at `g = 2`. **Falsified if any pair separates**, which would be a real
  finding about who a token season means something for.

---

## 2 · F2 — THE GRADED RESET

### 2.1 The wired object

`o32_delivered(p, Y, x)` is binary: `games >= 10*f` **AND** `avg >= o32_gate_bar`. A delivered season
sets accumulated `c_u` to zero as of that season. **Everything before it is wiped; nothing partial
exists.**

The owner's exhibit: a row with 7 games at 78.4 clears the bar and the four sat seasons behind him
cost zero; the same row at 5 games does not clear it and sits at depth 3.0 with `D = 0.263`.
*(Both halves of that exhibit are checked against the engine's own predicate in the packet, because
7 games is below the 10-game leg and the exhibit only works if the in-progress season fraction
prorates the threshold. It is an exhibit and it gates nothing.)*

### 2.2 The construction, fixed before the run

**Population — RETURNERS.** A player-season at depth N such that the player had at least TWO
consecutive prior seasons with zero games inside his listed window, and then played `g > 0` at depth
N with season average `a`.

**Outcome.** `V_from_(N+1) / v0` on the house ruler — the value delivered AFTER the return season, so
the return season's own output is not inside the outcome.

**The reversal scale**, declared here:

```
reversal(g, m)  =  ( V(g, m) - V_sat ) / ( V_never - V_sat )
   V_sat   = the same-depth population that played ZERO at depth N (kept sitting)
   V_never = the same-depth population with NO prior sitting at all
   m       = a - o32_gate_bar(position, age)   -- the season's margin over its own bar, continuous
```

`reversal = 0` means the return bought nothing; `reversal = 1` means it fully restored a
never-sat comparable. **The wired reset is the step function `1 if (g >= 10 and m >= 0) else 0` on
this same scale**, so the two are directly comparable.

**Cuts.** `g` continuous; `m` in bands; the joint cell where sample allows. Every cell prints n and
is marked THIN under 25 players.

**The threshold census — a separate, exact object.** On the ORDER P board at `Y = 2026`, count rows
with at least one season inside 2 games of the 10-game delivered threshold either side (8, 9, 10, 11,
12 games prorated by that season's fraction), split by whether the avg leg clears its bar, and count
how many rows' DELIVERED status would flip if their games moved by ±1 and ±2. **That is an engine
read with no estimation in it and it is reported separately from the reversal curve.**

### 2.3 Predictions

- **F2-P1.** Predicted: the reversal curve is **smooth and rising in `g`, with no step at 10**. The
  wired reset therefore over-rewards a 10-game return and under-rewards a 7-game one. **Falsified if a
  step at 10 fits the data better than a smooth curve, or if the cells straddling 10 have
  non-overlapping intervals in the direction the step predicts.**
- **F2-P2.** Predicted: `reversal` at the wired threshold (`g = 10`, `m = 0`) is **materially below
  1.0** — a bare-minimum delivered season does not restore a never-sat comparable, so a FULL wipe
  over-credits it. **Falsified if the interval at that point contains or exceeds 1.0.**
- **F2-P3.** Predicted: the margin `m` matters as much as the games leg or more. **Falsified if the
  outcome is flat in `m` at fixed `g`.**
- **F2-P4 — THE HONEST ONE.** Predicted: **the returner population is too thin to separate a step
  from a smooth curve at conventional confidence, and the primary result will be a NULL on F2-P1.**
  This is preregistered so that a null is reported as a null and not dressed as support for either
  shape. **Falsified if any cell comparison across the threshold is separable.**
- **F2-P5.** Predicted: the ±2-game threshold census holds **at least 20 board rows**. **Falsified if
  it holds fewer**, which would make the cliff a small-population problem.

---

## 3 · F3 — THE COMBINED-TAKE CALIBRATION

### 3.1 The owner's reframe, recorded as his

**The owner's words, recorded here as the frame this measurement is built on: split collection across
mechanisms is NOT a defect; the defect is an uncalibrated TOTAL.** This seat's own T2 packet framed
double-pricing as a defect in itself (§16, §18). **That framing is superseded by the owner's, and the
supersession is recorded rather than quietly applied.** Whether two collectors or one collect the
absence cost is irrelevant if the total is right; what matters is the total against the measured cost.

### 3.2 The construction, fixed before the run

Two populations, both carried over unchanged from `PACKET_SRO.md` §16 and §17.1:

- **the 8 double-priced rows** — the D8 staleness cap binds AND the sitter fade is below 1;
- **the 19 zero-priced rows** — stale(1) with `D_final = 1.000`.

For each row, the **ABSENCE TAKE** — the share of the row's absence-free price that the
absence-driven mechanisms removed:

```
absence_take = ( a_fade + a_D8 ) / ( board + a_fade + a_D8 )
```

`a_fade` and `a_D8` are the attributions already measured in `PACKET_SRO.md` §12 and §16, on the
engine's own legs. **The ORDER P charge is NOT in the numerator: it prices production against a bar,
not absence.** The TOTAL take including the charge is printed beside it so both readings are visible,
and the packet says which is which.

The **MEASURED TOTAL COST OF THE ABSENCE FACT** is `1 - D_measured(c_u)`, where `D_measured` is this
seat's OWN re-measurement of retention at unplayed depth from F1's machinery at `g = 0` — the same
washout evidence both wired mechanisms were separately fitted on, re-measured here on the house ruler
with an interval, rather than read back off the schedule the fade already carries. **Reading the
schedule back would be circular and this seat is not doing it.**

**Verdict rule, fixed before any number:**

| condition | verdict |
|---|---|
| `absence_take` inside the 90% CI of `1 - D_measured(c_u)` | **APPROXIMATES** — keep both collectors as they are |
| `absence_take` above the upper limit | **OVERSHOOTS** — the split needs scaling; precedence is irrelevant |
| `absence_take` below the lower limit | **UNDERSHOOTS** — the gap, and its size |

Reported **per row and per population**, never only as an average.

### 3.3 Predictions

- **F3-P1.** Predicted: the **19 zero-priced rows UNDERSHOOT** by essentially the whole measured cost,
  because their combined take is zero by construction and the measured cost at their depth is not.
  **Falsified if the measured cost at `c_u <= 1` is itself indistinguishable from zero**, which would
  mean the first unplayed season genuinely costs nothing and the zero take is correct.
- **F3-P2.** Predicted: the **8 double-priced rows APPROXIMATE or UNDERSHOOT rather than OVERSHOOT**,
  because seven of the eight carry a D8 cap of 10 board points or less. **Falsified if the population
  overshoots.** *(This seat's T2 packet implied overshoot by calling the double-pricing a defect. The
  prediction here runs against that implication on purpose.)*
- **F3-P3.** Predicted: **Billy Dowling, the one row where both legs are large, is the only row of the
  eight that could overshoot**, and he is reported individually whichever way he lands. He is an
  exhibit and gates nothing.
- **F3-P4.** Predicted: the measured cost curve `1 - D_measured(c)` is **materially above zero from
  depth 2 onward and indistinguishable from zero at depth 1 or below**. **Falsified either way and the
  falsification is the finding**, because the wired fade's floor at depth 1 is exactly what §17.1 of
  the packet found 19 rows sitting inside.

---

## 4 · F4 — THE SCHEDULE INVERSION

### 4.1 The object

The live ND fade row is `D(1)=1.0, D(2)=0.5583, D(3)=0.2748, D(4)=0.3973`, flat from 4. **Depth 3
fades harder than depth 4.** The order quotes the ORDER-A/R1 row `1.0 / 0.5502 / 0.2628 / 0.3460`,
which carries the same inversion; **both rows are printed in the packet so it is clear the inversion
is not an artifact of which vintage is quoted.**

### 4.2 The construction

**Provenance first, as instructed, and no smoothing is proposed.** The artifacts are read, not
re-derived:

- `docs/evidence/candidate_31f/FADE_31F.json` — the live wired row, its per-depth cells, and the
  instrument and md5 it was produced by;
- `docs/evidence/sitter_fade_2026-08-14/` — ORDER 30A-2, the instrument itself, its T4 tables and its
  own prereg scorecard;
- `docs/evidence/candidate_31/` — the ORDER 31 law and its curve table.

Reported: **n per depth cell**, `n_ever`, `n_zero`, mean, median, p25, p75, the POOLED aggregate
statistic, and the tail share — every one of them as published. A CI is reported **if and only if it
is recoverable from the published artifacts**; if the per-observation values are not published the
packet says so plainly and gives the distribution-free statement that IS recoverable instead of
inventing one.

**The one comparison that decides it, named in advance:** the listed-conditioned (L-B) row against
the UNCONDITIONAL row at the same depths. If the inversion is present under one conditioning and
absent under the other, the conditioning is the cause and the packet says which.

### 4.3 Predictions

- **F4-P1.** Predicted: **the depth-4 cell is thin — under 30 observations.** **Falsified if it is
  larger.**
- **F4-P2.** Predicted: **the inversion is a survivorship feature of the listed conditioning, not a
  property of the underlying population** — i.e. it is present under the listed-conditioned reading
  and absent under the unconditional one. **Falsified if the unconditional row inverts too**, which
  would make it a real feature of the whole population.
- **F4-P3.** Predicted: **"real feature" and "thin cell" are the SAME answer here, not alternatives**
  — the conditioning that creates the special population is the same operation that empties the cell.
  **Falsified if the depth-4 cell is thin under BOTH conditionings, or large under both.**
- **F4-P4.** Predicted: at least one published aggregate statistic on the depth-4 cell shows **no
  inversion at all**, so the inversion depends on which summary is taken. **Falsified if every
  published statistic inverts in the same direction.**
- **NO SMOOTHING IS PROPOSED AND NO REPLACEMENT ROW IS DERIVED.** Provenance and sample only.

---

## 5 · WHAT THIS SEAT WILL REPORT REGARDLESS

Sample sizes for every cell; thin cells printed THIN and not read; censoring rules stated with their
cutoffs; nulls reported as nulls; every prediction above scored HELD or FIRED by number; and the
declared difference in ruler between this seat and ORDER 30A-2 restated wherever a level is quoted.

**No fix is recommended in any of the four. No engine file is edited. Nothing is adopted.**
