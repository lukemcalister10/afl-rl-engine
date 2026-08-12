# PREREG — ORDER 26A: the reconciliation and the wedge decomposition

**Committed BEFORE any measurement is run.** Read-only forensic order. Nothing under `engine/` is
written, no board is built, no pin is moved. Evidence + scripts only.

Seat: ORDER 26A. Brief: issue #334, comment 5269252799 (ORDER 26A BRIEF), treated as binding.
Branch: `evid/order26a` off `origin/main` @ `8b1cdb8` (pool update v2 landed; board `88ce647f`;
total 752,429).

---

## 0. THE QUESTION, RESTATED

The ORDER 25 packet carries two figures both named "yr4/yr0" that disagree by roughly 2.7×.

| instrument | file | RD yr4/yr0 | n |
|---|---|---|---|
| ORDER 25 derivation §6 | `docs/evidence/pool_landing_v2_2026-08-12/o25_derive.py`, function `yr4()` | **1.379793** | 691 |
| all-arm cohort instrument | scratchpad `o22/noarb/noarb_table_allarm.py`, PRIMARY window by-arm | **0.5090** | 623 |

Same landed matrix (`per_entrant_O25R4.json`, md5 `3c6ffcde…`), same store `d9a24282`, same
v0surf `6ef67f07db98`. The ORDER 25 packet also carries ALL POOL 1.338050 and NATIONAL 1.554717
from the derivation, against the all-arm instrument's ND-arm yr4 1.4803.

The order is to reconcile **to zero residual**: same players, same years, row by row, with every
point of the difference attributed to exactly one of

- **(a) POPULATION** — who is counted;
- **(b) YEAR INDEXING** — derive `cohort+3` vs allarm `N=4`;
- **(c) THE VALUE OBJECT** — what `vpath` actually is vs the board as-of mark.

## 0A. DISCLOSURE — WHAT I READ BEFORE WRITING THIS PREREG

Honesty about the state of my knowledge at prereg time, so the hypothesis scoring below cannot be
scored generously after the fact. Before writing this file I had **read** (not run):

1. `o25_derive.py` in full, including `cohort()`, `anchor_of()`, `profile()` and `yr4()`.
2. `noarb_table_allarm.py` in full, including `cohort()`, `value_at()` and the by-arm block.
3. `harness_pvc_REPINNED_pass3.py` lines 270–380 (`never_established`, `depth`, `realised_at`,
   `realised_full`, `sofar`, `structural_values`).
4. The **published** outputs `DERIVE_FINAL_V2_out.txt` and `allarm_O25FINAL.txt` — prior evidence
   already in the record, not new measurement.

From that reading alone, two things were already visible to me and I state them here so I cannot
claim them as blind predictions:

- **The year index appears to be the SAME in both instruments.** derive computes `Y = cohort(r)+3`;
  allarm at `N=4` computes `Y = cohort(r) + N - 1 = cohort(r) + 3`. If that holds under measurement,
  **H3 is dead on arrival** and I will score it FALSIFIED, not "confirmed small".
- **The denominators are different objects.** derive's `yr4()` divides by `V0(r)`, which under
  `--basis anchor` is `anchor_of(r)` = signed level × `_PL_F` for a pool row. allarm divides by
  `float(r['v0'])`, the emitted year-zero board price. The ORDER 25 output already prints both
  sums for ALL POOL: **anchor basis 308,185 vs v0 basis 793,355** — a factor of 2.574. That is
  suspiciously close to the 2.71× gap under investigation.

This disclosure is itself a partial pre-answer. I register it rather than hide it. The hypotheses
below are scored against it.

---

## 1. PRE-REGISTERED HYPOTHESES

Every one is scored in `SUMMARY.md`. Breaches are owned **by name**.

### H1 — OWNER'S: survivor bias through the skip branches
`o25_derive.py:yr4()` carries two `continue` branches (`Y > W`, and `Y < yrs[0]`) which remove the
player's ENTRY from the denominator entirely, against the zeroed-dead branch (`Y > yrs[-1]` → `v=0`)
which KEEPS the entry in the denominator. The claim: 1.38 is effectively **survivors over THEIR OWN
entry**, and the pool's dead men have been dropped from the denominator rather than zeroed.

**Numeric check, pre-registered:** if H1 is the mechanism, the surviving entry share must be
≈ 0.509 / 1.380 ≈ **36.9%** — i.e. the rows that survive the skip branches must carry only ~37% of
the RD arm's total entry price.

**Pre-registered falsifier:** if the surviving entry share is ≈ 100% — if the two instruments admit
the *same* rows and skip the *same* rows — H1 is FALSIFIED and the owner's hypothesis is wrong.
I will say so plainly and in those words.

### H2 — the value object is not the board as-of mark
`vpath` is not the board's as-of mark but a realised/evidence-weighted or otherwise transformed
series, and that transformation contributes materially to the gap.

**Pre-registered test:** read the emitter's construction of `vpath`/`yrs`, and check whether the
value read at `Y` by each instrument is byte-identical row by row. If both instruments read the
SAME `vpath[i]` for the SAME row and year, the numerators are identical and H2 contributes **zero to
the yr4 gap** — whatever `vpath` turns out to be. In that case H2 is FALSIFIED *as an explanation of
this gap* and any finding about `vpath`'s nature is reported separately as an anomaly, not as bridge
mass.

### H3 — the year-indexing off-by-one contributes materially
Per §0A I expect this to be FALSIFIED (both resolve to `cohort+3`). Registered anyway, and it will
be measured, not assumed: I will compute the two instruments' year keys row by row and report the
count of rows where they differ. Prediction: **0 rows**.

### H4 — OWNER'S COMPARATIVE YARDSTICK
On the own-entry convention, ND survivors at yr4–5 read ≈ **2.2–3.1×** their own entry
(1.55 ÷ a 0.5–0.7 surviving-entry share). The pool survivors' own-entry trajectory is to be measured
against the ND survivors' on **BOTH**:

- the **calendar axis** (cohort year N, the instrument's own clock), and
- the **career-age axis** (seasons since the player's own first emitted season).

Pool players debut 1–2 years later than ND players, so a calendar-yr4 pool survivor is EARLIER in
career-time. **This timing offset is a legitimate effect and must be SEPARATED from mark suppression
before any conviction is recorded.** Pre-registered: I will report the pool-vs-ND own-entry ratio on
both axes, and the share of the gap that closes when the axis is switched from calendar to career-age.

### H5 (mine, added) — the bridge closes on the denominator alone
Given §0A, my own expectation is that the entire 2.71× is (a) a small population step plus (c') a
large **denominator-object** step (`v0` → `entry_anchor`), and that (b) and the numerator contribute
zero. Registered so that if the bridge fails to close on those two steps I must report the residual
rather than absorb it.

**Note on taxonomy:** the brief's category (c) is named "THE VALUE OBJECT". The denominator swap
`v0` → `entry_anchor` is an ENTRY-PRICE object, not a numerator value object. If the bridge lands on
the denominator, I will report it under a distinguished heading **(c′) THE ENTRY-PRICE OBJECT** and
say explicitly that the brief's (c) as literally worded — the numerator `vpath` vs the board mark —
scored zero. This is a deviation from the brief's taxonomy and is registered here in advance.

---

## 2. THE BRIDGE PROTOCOL (pre-registered, so the steps cannot be chosen to fit)

Start at the **all-arm** RD reading (0.5090) and apply differences ONE AT A TIME, in this fixed
order, landing on the **derive** RD reading (1.379793):

1. **P — population**: relax the cohort window 2005–2023 to derive's "all eligible cohorts".
2. **I — indexing**: swap allarm's `N=4` key for derive's `cohort+3` key.
3. **S — skip/zero semantics**: swap allarm's reached/pre/ended handling for derive's `continue`/`0.0`
   branches.
4. **A — aggregation form**: swap `mean/mean` for `sum/sum`.
5. **D — denominator object**: swap `r['v0']` for `anchor_of(r)`.

The order is fixed NOW. Steps are non-commutative in general, so the table will also report each
step's delta measured from the running state (path-dependent) and the final residual against
1.379793 must be **< 1e-9 in ratio terms**. Any residual above that is reported as UNEXPLAINED and
the order is failed on that point, not smoothed.

**Row-level requirement:** each bridge step names the players it moves — counts and worked examples.

## 3. THE WEDGE DECOMPOSITION (pre-registered method)

The act's central question: of the ~2–3× entry-vs-marks wedge, how much is

- **(i) ENTRY-INFLATION** — the pool entry price the board carries (`v0`) sits above the signed
  entry anchor because the calibration basis is `realised_full`, a pw-weighted CAREER AVERAGE, not
  a year-4 point mark; versus
- **(ii) MARK-SUPPRESSION** — living pool players carry board marks below what an ND survivor of
  equal career-age and comparable production would carry.

Method, fixed now: hold the ND survivor trajectory as the yardstick (H4), measured on the own-entry
convention on both axes. Attribute to (i) the part of the wedge that is removed by restating pool
entry on the signed anchor; attribute to (ii) the residual gap between pool survivors' own-entry
trajectory and the ND survivors' at MATCHED CAREER AGE. The calendar-vs-career-age difference is
reported as a THIRD, legitimate component **(iii) TIMING**, and is NOT charged to either (i) or (ii).

Splitting the wedge three ways rather than the brief's two is a deviation, registered here in
advance, and made because charging the debut-timing offset to "mark suppression" would manufacture
a conviction the evidence does not support.

## 4. WHAT WOULD MAKE ME REPORT "26B's ENTRY REDERIVATION IS NOT ENOUGH"

Pre-registered decision rule, so the conclusion is not chosen after seeing the number:

- If, after restating pool entry on the signed anchor, pool survivors' own-entry trajectory at
  matched career age lands **within the ND survivors' band** (H4's 2.2–3.1×), then the entry
  rederivation alone delivers the ND-like curve and the marks owe nothing.
- If it lands **materially below** that band at matched career age, the marks owe a correction, and
  I will state its rough size as the multiplicative shortfall at matched career age.
- "Materially" is fixed now at **±15%** of the band edge.

## 5. STANDING CONSTRAINTS

- READ-ONLY. Nothing written under `engine/`. No board built. No pin moved.
- No `git add -A`; explicit paths only. No model IDs in commit messages.
- Scratchpad instruments are copied into this evidence directory so the record is durable.
- MERGE NOTHING.
