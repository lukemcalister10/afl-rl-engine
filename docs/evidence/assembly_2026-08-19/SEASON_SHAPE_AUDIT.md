# THE IN-SEASON RAMP — THE AUDIT, THE SHAPE REUSED, AND THE ONE SITE THAT REFUSED IT

**Owner's instruction:** *"there is already a shape for the in-season ramp built in to other features
— find what's already active for other things and use it."* So: **audit first, fit nothing.**

---

## 1 · EVERY SEASON-PROGRESS SHAPE IN THE ENGINE, AND ITS FORM

| # | object | where | form | axis | convex in season fraction? |
|---|---|---|---|---|---|
| 1 | `SEASON_FE` / `_fEy` | `:110`, `:130` | the raw calendar fraction, 0.92 today | season fraction | **no — it IS the linear baseline** |
| 2 | **`f**1.5` — the D12 concave proration** | **`:2441`, `:2677`** | **`tau = (Y−debut) + f**1.5`** | **season fraction** | **YES — and owner-ruled** |
| 3 | `_expgate` exposure ramp | `:302` | `min(1, exposure / (POLE_RAMP · playable/SEASON))` | exposure vs a **prorated** bar | no — the proration is linear in `f` |
| 4 | `SEASON_PROG` banked/remaining blend | `:1285` | `sp·posval(present bar) + (1−sp)·posval(low bar)` | season fraction | no — a linear mix |
| 5 | `o32_delivered` proration | the delivered predicate | `games ≥ 10·f` | season fraction | no — linear |
| 6 | D8 graded staleness `_staleness_grade` | `:2663` | interpolation over a **quality quantile** `_D8Q` | quality, not time | not on this axis at all |
| 7 | thin-season weight `_wg` | `:181` | `w(g) = g²/(g+5.8)` | **games**, not season fraction | convex — **but on the wrong axis** |
| 8 | `exposure_pace` | `data/season_state.json` | an empirical durable-sample pace, 0.818 vs calendar 0.92 | season progress | a *level*, not a shape |

---

## 2 · THE SHAPE REUSED, AND WHY IT FITS

**`f**1.5` — the D12 concave proration, engine line 2441:**

> `D12: CONCAVE penalty proration tau' = (R/24)^1.5 (Luke OPTION A); completed seasons full (integer
> knots), in-progress season accrues concavely. PENALTY path only.`

It fits on every count that matters, and none of them is a judgement call by this seat:

1. **It is already active**, at two sites — the `sitout_ev` depth clock in `_a_blend` (`:2677`) and the
   D12 penalty clock (`:2441`). Nothing is introduced.
2. **It is OWNER-RULED** — the comment records it as *"Luke OPTION A"* under directive D12.
3. **It is on the right axis** — season fraction, not games.
4. **It has the shape the ruling asks for.** Its rate `1.5·f^0.5` is small early and large late: at
   `f = 0.2` it accrues **0.089** where linear accrues 0.200; at `f = 0.92` it accrues **0.882**.
   **Less at the start, and the accrual accelerates toward the end** — the owner's words, met by an
   object he has already ruled on.
5. **It is a PENALTY-path object by its own comment**, and the absence machinery is a penalty path.
   Extending it here is inside D12's own declared scope, not beyond it.

**No new constant. No fit. No dial-tuned exponent. The exponent is D12's own 1.5.**

---

## 3 · THE SITE THAT REFUSED IT — AND THE ENGINE SAID SO FIRST

The instruction named three sites. **It is applied to two and refused at the third**, on the engine's
own written reasoning rather than this seat's preference. From the comment at `:1534-1538`:

> *"the concave clock `tau = (Y−debutyr) + fe**1.5` is the **DEPTH** convention for the in-progress
> season — how far down the retention curve the row has travelled — and it is a penalty-path object
> by its own comment. It is UNTOUCHED and is **NOT reused as the participation weight**: depth and
> participation are different quantities, and **`fe**1.5` would say a player who has played no games
> is 88% participating, which is the defect inverted.**"*

| site | quantity | ramp applied? |
|---|---|---|
| the sitter-fade clock's in-progress accrual (`o31_cu`) | **DEPTH** — how far down the fade curve | **YES** |
| the R3 current-run fraction (`o41_absence_depth`) | **DEPTH** — how long the current absence is | **YES** |
| the I1 credit's in-season fraction | **PARTICIPATION** — how much this season counts as played | **NO — refused** |

**A previous seat considered exactly this reuse and rejected it for exactly this site, in writing.
That reasoning is correct and it is followed rather than overridden.** Applying `f**1.5` to the credit
would say a gameless row is 88% participating — the defect inverted, in the engine's own words.

---

## 4 · WHAT WAS *NOT* DONE, AND WHY

**The measured-expectation fit from the earlier instruction was NOT attempted, because the data
cannot support it — verified, not assumed.**

`E[end-of-season absence-equivalent | g games so far at season-fraction f]` needs, for **completed
historical seasons**, the games count at **intermediate** fractions. The store does not have it:

- a season row is **exactly** `{year, avg, games, pos}` — one aggregate per season, no rounds, no
  dates, no within-season series. Checked across the store, not on one row.
- the only round-indexed data anywhere in the repo is `ingestion/value_history.json`, and it is the
  **wrong quantity, wrong period and wrong shape**: it records **board VALUE and RANK**, not games;
  only for **2026 rounds 14-22**; and only for the 804 current rows. It carries **no completed-season
  outcome to fit against**, and it starts at round 14 — so it cannot see the early-season region
  (`f ≈ 0.2`) which is exactly where the ramp's shape has to be determined.
- fitting on it would also be **circular**: board value is an output of the very machinery the ramp
  would feed.

**So the fallback was never reached — and it did not need to be, because the audit found the shape
the owner said was already there.**

---

## 5 · CONTINUITY

The ramp is smooth and monotone in `f` on `(0,1)`, and it agrees with the linear form at both ends
(`f→0` and `f=1`), so it introduces **no new discontinuity at the season turn**: a completed season
still enters at exactly 1.0 via `_fEy`'s own `return 1.0`, and the dial is inert there by
construction. The continuity sweep is reported with the built board.

---

## 6 · STATUS

**PRICED, NOT ADOPTED.** `RL_O41_RAMP` is default-off; with it off the board is
**`fbf61d05` — byte-identical to the candidate**, which is the dial-off identity for the new sub-dial.
The ramp board and its day-0 consequence are reported beside it, because **changing an absence DEPTH
clock changes `D(c_u)`, and a day-0 sitter's price IS `v0 × D(c_u)`** — the same collision that
produced the first halt. That is measured and reported rather than assumed either way.
