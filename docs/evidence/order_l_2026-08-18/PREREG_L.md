# PREREG — ORDER L: THE NO-ARB DOCUMENT RE-ISSUED (window split + the 2005/06 sensitivity)

Registered and pushed BEFORE any Order L number is computed. This seat is READ-ONLY on the engine,
the board and the law. No price moves. No board is built. Order L re-issues INSTRUMENT TABLES and
one owner document off matrices that already exist.

Program: the owner raised two gaps in Order K's no-arb document
(`docs/evidence/order_k_2026-08-18/ORDER_K_NOARB.html`).

- **Gap 1.** The ND band tables are pooled across all cohorts. Only the pool-arm tables carry the
  primary / modern window split. Owner: *"I can't see where I can view the modern / total split on
  the no arb tables."*
- **Gap 2.** Owner: *"Can we also re issue them, but excluding the first two years of the 2005 and
  2006 class from both the numerator and the denominator?"*

---

## 0. INSTRUMENTS AND INPUTS — REUSED, NOT REBUILT

Nothing in this order re-emits a matrix or re-derives a law. The three objects are the three
walk-forward per-entrant matrices Order K already built and published tables from:

| label | board | file |
|---|---|---|
| `OKRULED` | ORDER K **f3101883** — the current candidate | `$SP/per_entrant_OKRULED.json` |
| `O35FINAL` | the landing candidate **1f176444** | `$SP/per_entrant_O35FINAL.json` |
| `O31FFINAL` | candidate 31 **fe6be9d6** | `$SP/per_entrant_O31FFINAL.json` |

`$SP = /tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad`.

The value semantics, the population filter, the zero convention and the window-end derivation are
lifted **verbatim** from the disclosed instruments:

- ND bands: `docs/evidence/candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py`
  (committed md5 `d59ad550116ebbe3d90ed82becd2c4d5`, the owner's five bands standing) and the
  ORDER-29 re-pointed harness `harness_pvc_REPINNED_pass3.py` whose `load_matrix()` **is** the ND
  population filter: `teaches_curve and pick and 1 <= pick <= 64 and 2004 <= year <= 2022`.
- Pool arms: `docs/evidence/landing_29_2026-08-13/noarb/noarb_table_allarm.py`
  (cohort = draft year + 1, except MSD where cohort = draft year; pre-window rows excluded and
  counted, never scored zero; ended/null = 0 and kept in the denominator).
- Class mark: `docs/evidence/order_k_2026-08-18/ok_class.py` and its `CLASS_K.json`.

Order L copies these files into its own evidence dir and asserts their md5 at run. The Order L
readers re-use their `value_at` / `cohort` bodies unchanged and add **only** a population filter.
Both md5s are printed by the run.

## 1. THE WINDOW SPLIT — DEFINITION FIXED HERE, BEFORE ANY NUMBER

The pool-arm tables already split on the COHORT clock:
`WINDOWS = [('PRIMARY cohorts 2005-2023', 2005, 2023), ('MODERN cohorts 2019-2023', 2019, 2023)]`.
Order L applies **that same definition, unchanged**, to the ND band tables:

- **PRIMARY** = cohorts 2005-2023 = **draft years 2004-2022**.
- **MODERN** = cohorts 2019-2023 = **draft years 2018-2022**.

Registered structural consequence, stated before the run so it cannot be presented as a finding:
the ND population filter is exactly draft years 2004-2022, so **the PRIMARY window is the whole ND
population and the PRIMARY tables must reproduce Order K's published pooled tables cell for cell.**
That equality is a REGISTERED SELF-CHECK (L-SC1): if any PRIMARY cell differs from the corresponding
`STANDING_TABLES_K.json` cell by more than 1e-9, the run HALTS and the packet says so.

For ND rows the draft clock and the cohort clock agree in calendar terms
(`cohort + N - 1 = year + N`), so no value moves when the window is expressed on the cohort clock.
This is registered as self-check **L-SC2**.

## 2. THE 2005/06 EXCLUSION — INTERPRETATION FIXED HERE, IN WORDS, SO THE OWNER CAN CORRECT IT

Interpretation used, and printed on the page in these words:

> **The 2005 and 2006 draft cohorts are removed from the population entirely — from the year-N means
> AND the year-0 means, numerator and denominator alike, everywhere those cohorts would otherwise
> contribute.** On the cohort clock these are classes 2005 and 2006, which are the **2004 and 2005
> national drafts**. It is not a re-weighting and it is not a truncation of their first two seasons:
> the players are simply not in the table.

Why the cohort clock and not the draft-year label: the classes the owner quoted read
**0.899** and **0.856** on the year-1 class measure, and those are exactly `CLASS_K.json`'s cohort
classes 2005 and 2006 on the current candidate. The identification is therefore made against the
number he read, not against a label.

Registered structural consequence: the MODERN window (cohorts 2019-2023) contains no 2005 or 2006
cohort, so **the exclusion must move nothing in the modern window.** Registered self-check **L-SC3**:
every MODERN cell must be identical with and without the exclusion, to 1e-12, or the run HALTS.

**LABELLING.** The exclusion is a **SENSITIVITY ANALYSIS, not a correction.** It is never the
headline number on the page and never the number a gate is scored on. The reason is recorded here
before the result is known: the supervisor checks already run and pass — season-row density for
those classes matches every other class (3.2-3.4 rows per player over years 1-5), and the engine
treats a missing season identically to an owner-confirmed zero-games season. The documented data
gap (`docs/evidence/store_completion_2004_2005/README.md`: 51 season rows back-filled from the
owner's corrected sheet, 14 in 2005 and 37 in 2006, plus 177 owner-confirmed zero-game seasons held
under the no-row convention) is the owner's REASON for asking; it is not evidence that the classes
are wrong.

## 3. TABLE FORMATS — FIXED HERE

### 3.1 ND band table (one per board x window x exclusion variant = 12 tables)

Rows, in this order: `ALL picks 1-64`, `picks 1-20`, `picks 21-64`, then the owner's five bands
`picks 1-10`, `picks 11-20`, `picks 21-30`, `picks 31-40`, `picks 41-64`.

Columns: `#` · `band` · `n` (the band's cohort size in that window) · `yr0` ... `yr7` ·
`yr0->1` · `margin to the 14% rail` · `verdict` · `thin?`

- `yrN` = mean(value at year N over the included set) / mean(year-0 value over **the same** included
  set). `yr0` is 1.000 by construction.
- `yr0->1` = `yr1 - 1`, printed as a percent. `margin` = 14% minus `yr0->1`.
- `verdict` = `SELL-RED` if `yr0->1 < 0`; `BUY-RED` if `yr0->1 > +14%`; otherwise `ok`. Unchanged
  from Order K.
- Every table also carries a per-year `n_included` grid (yr0...yr7) so no cell's sample is hidden.

### 3.2 Thin-cell rule — no smoothing, disclosure only

Fixed before the run, because the modern window will be small for the finer bands:

| n_included at that year | treatment |
|---|---|
| >= 30 | printed plain |
| 10 <= n < 30 | printed, flagged **thin** (marker `*`) |
| 5 <= n < 10 | printed, flagged **very thin** (marker `**`), and the page says do not read it as a measurement |
| n < 5 | **not printed** (dash). This is the pool-arm instrument's own `len(vals) < 5` rule, applied unchanged. |

If a band's `yr1` cell is thin or worse, its verdict is printed with the same marker. No cell is
ever pooled, borrowed, interpolated or smoothed to remove a thin flag.

### 3.3 Pool-arm table (unchanged format, exclusion variant added)

Order K's arm table, format unchanged: `#` · `arm` · `n` · `yr0`...`yr7` · `yr0->1` · `margin` ·
`verdict`, arms in the order `RD, MSD, UNR, IRE, PDA, PDN, SSP, PDS, ALLPOOL`, both windows, now
also with and without the 2005/06 cohorts. The MSD year-1 debut-gap exclusion keeps its existing
worded verdict and is never scored zero.

### 3.4 Year-1 class calibration

`ok_class.py`'s machinery, unchanged: cohort clock; per-class mark = `sum(year-1 value) / sum(v0)`
over that class, `None` if fewer than 5 scorable rows; the published mark is the **mean over classes
2005-2015** (11 classes).

Order L prints, for all three boards:
1. every per-class row 2005-2021,
2. the standing mark (mean over 2005-2015, 11 classes),
3. the exclusion mark (mean over 2007-2015, **9 classes**, after cohort classes 2005 and 2006 are
   dropped from the population entirely),
4. the difference.

Registered arithmetic check **L-SC4**: on the current candidate the supervisor computed **1.0669**
for the exclusion mark. From `CLASS_K.json` the standing mark is 1.0324 over 11 classes with 2005 =
0.8985 and 2006 = 0.8562, so the exclusion mark must equal
`(1.0324x11 - 0.8985 - 0.8562)/9 = 1.0668...`. If the run's own number differs from the supervisor's
by more than 0.0002 the packet reports the correction and shows both.

## 4. THE W2 INSTRUMENT QUESTION

To be answered from the filed record, with the deciding code quoted verbatim and by line:
**which instrument was the class target [1.03 floor / ~1.08 ideal] computed on** — the fast
"navigation" calibrator (`docs/evidence/order_i_2026-08-18/o36_calibrate.py`, analytic `p1_of`) or
the full built walk-forward matrix (`docs/evidence/order33_w2_2026-08-17/w2_forward_calibration.py`,
`R_cand = P1/P0` off `vpath[0]`). The current candidate reads **1.0324** on the built matrix and
**1.0515** on the navigation instrument, so the answer decides whether the floor is cleared
comfortably or barely. The answer is reported as found. No number is adjusted to suit it.

Also to be reported, if the record shows it: whether the two instruments even use the same class
window, since `ok_class.py` marks on the COHORT clock and `w2_forward_calibration.py` marks on the
DRAFT-YEAR clock.

## 5. DELIVERABLES

- `ORDER_L_NOARB.html` — the re-issued owner document. Self-contained, sortable, house conventions,
  the "what is in this board and what is still broken" box carried over from Order K **unchanged**,
  current candidate first, windows side by side, exclusion variant clearly labelled a sensitivity
  check, every definition in plain words.
- `PACKET_L.md` — plain language, short sentences, no metaphors: the numbers and the W2 answer.
- `ol_bands.py`, `ol_arms.py`, `ol_class.py`, `ol_pages.py`, `bb_L.sh`, and the raw console output.

## 6. WHAT WOULD FALSIFY THIS RUN

- L-SC1 fails: the PRIMARY ND tables do not reproduce Order K's pooled tables.
- L-SC2 fails: the two clocks disagree on an ND row.
- L-SC3 fails: the exclusion moves a modern-window cell.
- L-SC4 fails: the class arithmetic does not reproduce.
- Any instrument md5 moves.

Any of these HALTS the run and is reported in the packet rather than worked around.

Seat: ORDER L INSTRUMENT SEAT, 2026-08-18. Read-only. No engine, board or law file is touched.
