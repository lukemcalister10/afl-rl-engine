# INSTRUMENT PRE-STATEMENT — ORDER 26B STEP 5

**Filed 2026-08-12, and committed and pushed BEFORE either instrument was computed.**

The ORDER 26B brief orders, of the reverse no-arb test: *"state the exact test form BEFORE computing
it (in the artifact, dated), then compute."* This file is that statement. It is committed in its own
commit, ahead of `o26b_compare.py` existing, so that the ordering is a fact in the git history and not
a claim in a paragraph.

Both instruments were already fixed in `PREREG_ORDER26B.md` §6, committed 2026-08-12 before any of
this order's quantities were measured. **Nothing here weakens or re-scopes that text.** What this file
adds is the operational detail §6 left open — the depth axis, the population rule, the bootstrap
specification and the exact PASS/FAIL predicate — stated now, before the numbers exist.

Inputs, pinned:

| object | identity |
|---|---|
| walk-forward matrix | `per_entrant_O25R4.json` md5 `3c6ffcdeaac9786473f3f017dba1d61e` (the matrix ORDER 26A measured on) |
| store | `d9a24282357cf3083b1640466e3ecd83` |
| year-zero surface | `6ef67f07db98258786189a6316ce24f9` |
| derived v0s | `DERIVE.json`, step 4 of this order |

---

## 1. THE SHARED SUBSTRATE — how a derived v0 becomes a day-0 price

Both instruments need one number per entrant: **his derived day-0 price**. It is built in three
declared multiplications and no others:

```
DERIVED_v0_board(i)  =  cell_v0(i)  ×  ANCHOR_FACTOR  ×  NUMERAIRE
```

- `cell_v0(i)` — for a pool entrant, the Ruling-12 borrowing-ladder value of his
  (pathway × day-0 position) cell from step 4; for a national draftee, the all-in curve value at his
  pick. Units: raw delivered board points.
- `ANCHOR_FACTOR = 1.4200` — the single scalar that pins the derived curve at pick 1 = 3000
  (Ruling 6). Reported at step 4 before either instrument existed.
- `NUMERAIRE = 1.0524` — `engine/rl_after/pick_redenomination.json::factor`, the display numéraire.
  This is the same divisor the gate leg measured flat on every board row (`ev / board_v` ≈ 1.0524,
  GATE_REPORT.md §5 leg 4) and the same factor the owner's signed pool levels are multiplied by at
  the engine-value sites (`pvc_curve_v2.json::pool_levels._doc`, currency clause). It is the leg the
  owner's landing ruling names: **printed day-0 = derived v0 × the display numéraire.**

## 2. THE DEPTH AXIS

`d` is **career depth measured from the entry cohort**, using the two instruments' own shared
primitive (`o26a_bridge.py::cohort`, itself verbatim from both `o25_derive.py` and
`noarb_table_allarm.py`):

```
cohort(r) = r['year']          if r['type'] == 'MSD'
          = r['year'] + 1      otherwise
Y(d)      = cohort(r) + d,     d = 0 .. 6
```

Row semantics are `o25_derive.py::yr4()`'s branch structure, carried verbatim (`sem_derive`):
`Y > window_end` → **the row leaves the denominator** (his year `d` has not happened yet);
`Y < yrs[0]` → the row leaves the denominator (pre-first-season);
`Y > yrs[-1]` → **0.0, kept in the denominator** (the career ended — the dead are zeroed, never
dropped); a null mark inside the window → 0.0, kept. This is the convention ORDER 26A proved moves
the reading by exactly 0.000000, so it cannot be a thumb on the scale.

## 3. THE MARK-PATH PROGRESSION TEST

```
m_allin(d)  =  Σ_i vpath_i[Y(d)]  /  Σ_i DERIVED_v0_board(i)      (the PRIMARY reading)
m_mean(d)   =  mean_i ( vpath_i[Y(d)] / DERIVED_v0_board(i) )     (the prereg's literal wording)
```

Both are printed for every pathway. **The PRIMARY reading is `m_allin`**, the sum/sum form, because
PREREG §6's own words are "all-in (dead kept at 0 in the numerator, entry kept in the denominator)",
which is sum/sum language, and because it is the convention both landed instruments use. The
mean-of-ratios form is printed beside it so a reader who reads §6's `mean_i` literally can check the
verdict against his own reading. **Where the two disagree on a verdict, that disagreement is
reported, not resolved silently.**

**PASS for a pathway iff** `m_allin(d)` attains a maximum `m*` at some `d ≥ 2` with `m* > m_allin(0)`
— the ND shape: rising from entry toward a peak above it. Pathways with fewer than 40 rows in the
denominator at `d = 4` are reported as **THIN** and their failures are read as thin-sample failures,
per PREREG P6.2, which said so before any of this was measured.

The ND 1-64 arm is computed on the identical construction and printed as the reference shape.

## 4. THE REVERSE NO-ARB TEST

**The claim under test.** A pathway is a *systematic guaranteed-loss hold* if a club that acquires an
entrant through it, at the derived entry price, is strictly better off selling at entry than holding
— in expectation, at the whole-cohort grain, with the dead carried.

**The predicate, stated before computation:**

> A pathway **FAILS** (is a guaranteed-loss hold) iff **both**:
> 1. `m_allin(d) < 1` for **every** `d = 1 … 6` at which the pathway has any denominator; **and**
> 2. the **upper end of a 95 % bootstrap interval on `max_{d≥1} m_allin(d)` is also below 1**.
>
> **PASS = no pathway fails.** A pathway that clears either limb passes.

**The bootstrap, specified now so it cannot be tuned later:** `B = 2000` resamples, entrants drawn
with replacement **at the entrant level** (an entrant's whole path travels together — resampling
player-years would destroy the very dependence the test is about), `numpy.random.RandomState`
seeded at **`20260812`**, the statistic recomputed as `max_{d≥1} m_allin(d)` on each resample, and
the interval read as the **97.5th percentile** of the resample distribution (the upper end of a
two-sided 95 % interval). Pathways with n < 8 entrants are reported with the bootstrap printed and
explicitly marked **UNRELIABLE**; no verdict of FAIL is issued on fewer than 8 entrants.

**Non-vacuity.** This predicate can go red. It goes red for any pathway whose derived entry price
exceeds every mark its cohort ever carries. The instrument prints, for every pathway, the whole
`m_allin(1..6)` vector and the bootstrap upper limit, so a reader can see how far each pathway sits
from the failure line rather than reading a bare verdict word.

## 5. THE DISPERSION LAW

Every distributional claim in the step-5 artifact reports **p05 / median / p95**, never a bare mean.
This is not a style preference: it is the binding lesson of this order's own gate leg, where a
board-wide median of `1.0044` — apparently perfect — sat on a distribution spanning `0.0904` to
`4.2048` across the middle 90 %. A mean without its dispersion would have reported that gate as a
pass.
