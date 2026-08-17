# PREREG G — THE CLOCK RE-BASE INSTRUMENT SEAT

**Order G. Issue #334. Branch `land/order-29`. Authority: the owner's **R-CLOCKBASE** ruling
(#334 comment 5317457543) and the derivation it adopts, `docs/evidence/order_f_timing_2026-08-17/PACKET_F.md`.**

**This file is pushed BEFORE any number of this seat is computed.** Everything below is the rule; the
run executes it and PACKET_G.md reports it.

---

## 0. WHAT THIS SEAT IS AND IS NOT

**READ-ONLY on engine, board, law and store.** No engine import that builds anything, no board build,
no store write, no artifact write, no price file touched. This seat changes **REPORTING, not prices.**
Every table it emits will carry that sentence.

It re-emits the standing two-sided no-arb suite with **one added column family**: the clock-fair
benchmark and the gap to it. The two absolute exploit rails keep their existing definitions and their
existing verdicts.

---

## 1. THE THREE READINGS EVERY CELL WILL CARRY

For a cell whose year-0 → year-1 mark accretion is `m` (so `m = 1.0794` means +7.94%):

1. **BUY-SIDE EXPLOIT RAIL — unchanged.** `RED` if `m > 1.14`. (Free money against the 14% carry:
   buy at entry, sell at year 1, beat the cost of holding.)
2. **SELL-SIDE EXPLOIT RAIL — unchanged.** `RED` if `m < 1.00`. (Sell at entry, buy back at year 1,
   pocket the difference.)
3. **CLOCK-FAIR GAP — new.** `gap_G = m − fair_G`, where `fair_G` is constructed in §2. Printed with
   the cell's entry-age mix beside it. This is a **fairness reading, not an arbitrage test**, and it
   carries no RED of its own; it is reported as a signed number.

The two rails are absolute and are **not** re-based. The ruling says so explicitly.

---

## 2. THE CLOCK-FAIR BENCHMARK — EXACT CONSTRUCTION

    fair_G(cell) = acc_mix(cell) x (1 - s1(cell))

### 2.1 The accretion factors — LIFTED FROM ORDER F, NOT RE-DERIVED

`disc_factor` is lifted **by source text** out of `engine/rl_after/rl_model.py` and `exec`'d verbatim,
exactly as `o_f_wedge.py:118-129` does it. The run **asserts the lifted-text md5 is
`93a198a86f7c832dba79e41de5146d8c`** and halts otherwise. Control, as in F:
`disc_factor(18, 0.14, 3, grace=0) == 1.14**3`.

The two accretions are then rebuilt by F's own loop (`o_f_wedge.py:146-162`), byte-for-byte the same
arithmetic, with `G_O = {age<=19: 2, age>=20: 0}` on the curve clock and `G_E = 0` on the engine clock
at the year-1 vantage:

    f0[j] = 1 / disc_factor(a, 0.14, j,     'bal', G_O)      # weight of season j in the ENTRY price
    f1[j] = 1 / disc_factor(a, 0.14, j - 2, 'bal', G_E)      # weight of season j in the YEAR-1 price
    ACC   = f1[j] / f0[j]     for every surviving season j >= 2

The run **asserts** the accretion is uniform across surviving seasons (F's own assert), and asserts

    ACC[age<=19] == 1.00000   exactly
    ACC[age>=20] == 1.14**2 = 1.29960   to 1e-12

**No re-derivation.** If either assert fires the seat halts and reports the halt.

### 2.2 The entry-age mix

- **Which age.** The matrix field `age_draft` — the entrant's age at his draft/entry event. This is
  the field Order F used (`o_f_wedge.py:242`, `aged=r.get('age_draft')`). Coverage on all three
  matrices is complete (no nulls); the run asserts this and prints the count.
- **The boundary.** `<= 19` takes `ACC[age<=19]`; `>= 20` takes `ACC[age>=20]`. This is the ruled
  grace-A boundary (Order 28, reading O), not a fitted cut.
- **The weight.** Entry board points `v0`, exactly F's ALT-2 weighting (`o_f_wedge.py:467-471`):

      acc_mix = sum_i v0_i * ACC(age_i) / sum_i v0_i
      share_le19 = sum_{i: age<=19} v0_i / sum_i v0_i

  **Why v0 and not headcount:** the mark being judged is itself a v0-weighted object
  (`mean(price at yr1) / mean(price at yr0)`), so the benchmark it is compared against must be
  weighted the same way. Head-count mixes will be printed alongside as a disclosed sensitivity.
- **Mid-year entrants (MSD).** A mid-season draftee debuts in the year he is drafted. His `age_draft`
  is used as stored, unadjusted — F's construction. His mark already runs on the cohort clock the
  standing all-arm instrument defines (entry year, not entry year + 1), and the standing MSD
  year-1 exclusion caption is carried unchanged. **Disclosed as a choice point in PACKET_G.**

### 2.3 The year-one delivered share `s1`

Order C's own construction, reproduced by F verbatim (`o_f_wedge.py:361-370`), on the house S4
delivered-value ruler lifted by source text out of
`docs/evidence/order32_s4_2026-08-17/s4_shootout.py` (md5 asserted at `ce730ab0c5fa62da8f920c2c9ec8672c`):

    sv1 = sum over cell of the entrant's FIRST post-entry season value
    dv1 = sum over cell of every later season, discounted to the YEAR-1 clock at 1.14
    s1  = sv1 / (sv1 + dv1)

`s1` is pooled at the cell (value-weighted), not averaged over players — Order C's convention.

### 2.4 What population `s1` and the age mix are computed on

**PRIMARY: the same rows the mark's year-1 cell uses.** Benchmark and mark on one population, so no
cell is judged against a benchmark built on a different set of players.

- Five ND bands and the two aggregate pick windows: the harness ND population
  (`teaches_curve` & `pick in 1..64` & `year in 2004..2022`), with the same year-1 inclusion
  (`draft_year + 1 <= WINDOW_END`) the standing extended-338 instrument applies.
- Pool arms and the two ALLPOOL windows: the standing all-arm reader's own cohort-clock population,
  per window (PRIMARY 2005-2023, MODERN 2019-2023), with `n_pre` rows excluded from the year-1 cell
  exactly as the standing instrument excludes them.

**CONTROL, printed beside it: Order F's own window (entry classes 2005-2019).** Late classes are
right-censored on the delivered-value ruler, which mechanically **overstates** `s1` and therefore
**understates** `fair_G`. Both columns are printed for every cell; the verdicts are read off the
PRIMARY and the control is the disclosure.

### 2.5 The known approximation in F's construction — disclosed in advance

F's `fair_board = ACC x (1 - s1)` uses the **flat-clock** `s1` (Order C's construction) so that the
`fair_C` and `fair_G` columns are directly comparable. The exactly-clock-consistent object would use
the year-one season's share of the **entry-clock** price. The two differ by `O(s1 * 0.14)` — on a
band with `s1 = 0.03` the difference is about **0.004**. The ruling names F's construction as the one
to use, so **F's construction is PRIMARY and is what every verdict is read off**; the exact ratio is
computed as a control and both are printed. No number is chosen after seeing which is friendlier.

---

## 3. THE MARKS — UNCHANGED INSTRUMENTS, RE-RUN

No new mark construction. The seat re-runs the standing instruments the Order D wire ran:

- **Five bands + the two pick windows:** the owner's disclosed extended-338 five-band instrument
  (`docs/evidence/candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py`) over the re-pointed
  harness (md5 must begin `02dcf28c`), the one disclosed edit being the tagged output filename —
  identical to Order D's handling (`o35_noarb.py:37-63`).
- **Pool arms + ALLPOOL, both windows:** the all-arm reader lifted verbatim from `o35_noarb.py:77-124`.

**CONTROL (halting):** the re-run on the Order-D matrix must reproduce `NOARB_D.json`'s own five-band
year-0→1 numbers to 1e-9, and the re-run on C32R must reproduce `NOARB_32R.json`'s. If either
deviates the seat halts.

---

## 4. THE THREE COLUMNS OF BOARDS

The owner's both-baselines law extends to rulers, so every table is emitted for three boards:

| column | board | matrix |
|---|---|---|
| **D** (the LANDING CANDIDATE) | `1f176444` | `per_entrant_O35FINAL.json` |
| **C32R** | `7802ee97` | `per_entrant_O32RFINAL.json` |
| **C31** (Candidate 31) | `fe6be9d6` | `per_entrant_O31FFINAL.json` |

Board identity is asserted from each matrix's `meta.basis_29c.replication_board` before any number is
taken from it. All three carry store `cb38ef11`, so the delivered-value stream (`SV`) and therefore
`s1` are **identical** across the three; only `v0`, the year-1 price, and hence the mark and the
v0-weighted age mix move. The run asserts the `s1` identity across boards and prints it.

---

## 5. TABLE FORMATS — FIXED HERE

### T1 — RE-BASED FIVE-BAND TABLE (per board)

    band | n | mark accretion | entry-age mix (share <=19, acc_mix) | fair_G | gap_G | fair_C | gap_C | SELL rail | BUY rail

### T2 — RE-BASED POOL-ARM TABLE (per window, per board)

Same columns, plus `n_pre` and the standing thin-n bound: **any arm with n < 15 in the window is
printed `THIN` and carries no clock-fair verdict** (the rails still print, as they always have).
SSP and the development arms keep their standing thin-n bounds and their standing caveats verbatim.

### T3 — VANTAGE MATRIX, REFRESHED

The same diagnostic-only matrix, with the yr-1 caption re-based: each band's header prints the
clock-fair year-1 mark and the clock-fair gap instead of the flat-1.14 one. **The carry columns
`1.14^k` are UNCHANGED** — from the year-1 vantage the grace is exhausted and the two clocks agree
(PACKET_F §5, P4), so those legs were already benchmarked correctly and this seat does not touch them.
Diagnostic only; nothing is calibrated toward it.

### T4 — LEG ATTRIBUTION, RE-BASED

The standing "where each band's inconsistency lives" split, with the year-1 leg measured against
`fair_G` instead of `fair_C`, and the later-years leg unchanged.

---

## 6. THE W2 TARGET RE-DERIVATION

The class-level acceptance band **[1.100, 1.117]** (PACKET_W2 §(3).1) was built on the flat identity
`R* = 1.14 x (1 - SV1sh)`. It must be made ruler-consistent.

**Object:** the registered W2 matrix `per_entrant_O31FFINAL.json`, the same class set 2005-2021, the
same all-arm population, the same S4 ruler — so the **only** thing that changes is the benchmark.

**Per class y:**

    SV1sh(y)  = SV1(y) / (SV1(y) + DV1_full(y))          # W2's own field, unchanged
    R*_flat(y) = DV1_full(y) / DV0_full(y)                # W2's own R*full, must reproduce EXACTLY
    acc_mix(y) = sum_i v0_i ACC(age_i) / sum_i v0_i       # v0-weighted, per S2.2
    R*_clock(y) = acc_mix(y) x (1 - SV1sh(y))             # THE RE-DERIVED TARGET

**Controls, all printed:**

- `R*_flat` must reproduce PACKET_W2's published per-class `R*full` column exactly (halting assert).
- The **exact** clock ratio `sum_i Y1_i / sum_i E_i`, where `E_i` is the entrant's delivered stream
  weighted on the entry clock (`1/disc_factor(age,0.14,j,G_O)`) and `Y1_i` on the engine clock
  (`1/disc_factor(age,0.14,j-2,0)`) — the object §2.5 names. Printed beside the primary.
- A **head-count-weighted** `acc_mix` variant, as the §2.2 sensitivity.

**The band.** Same estimator as W2: the **2005-2015** class mean (the well-observed classes), with a
**class bootstrap, B = 2000, seed 33, `numpy.random.default_rng`** — W2's own `cls_boot`, reused, so
the new band is the same kind of object as the old one. Per-class dispersion published in full. Late
classes (2019-2021) are right-truncated and are printed but excluded from the band, exactly as W2 did.

**The verdict sentence, fixed in advance.** The packet will state, in **one plain sentence**, whether
the landing candidate's class mark **1.042** sits inside, below, or above the corrected band — and if
the corrected band has moved down to near 1.042, the packet will say plainly that **the "missing 6
points" was substantially a ruler artifact.** If it has not, the packet will say plainly that **the
missing points survive the re-base.** Both sentences are written here before the number is seen; the
run picks which one is true.

---

## 7. RUN DISCIPLINE

- `PATH=/root/rl_venv312/bin:$PATH`; `OPENBLAS_NUM_THREADS=1`, `OMP_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1`, `VECLIB_MAXIMUM_THREADS=1`, `PYTHONHASHSEED=0`.
- Sequential. One process at a time. No parallel lanes.
- Evidence dir `docs/evidence/order_g_clockbase_2026-08-17/`: this prereg, `o_g_clockbase.py`,
  `CLOCKBASE_G_out.txt` (the full console), `CLOCKBASE_G.json`, `W2_TARGET_G.json`, `PACKET_G.md`.
- Push per step, explicit refspec `git push origin HEAD:land/order-29`, fetch + rebase before each push.

## 8. HONESTY CLAUSES, REGISTERED

1. Every table prints: **this seat changes REPORTING, not prices. No board number moves.**
2. Where the age-mix construction has a choice (which age, mid-year entrants, weighting), F's
   construction is followed and the choice is disclosed at the point of use.
3. SSP and the development arms keep their thin-n bounds; SSP additionally keeps its standing
   right-censoring caveat (a recent mechanism its career-lens numbers cannot judge).
4. `UNR` is expected to get **worse** under the correction (it is a mature-age arm, so the correction
   raises its benchmark). That is registered here so it cannot be read as a surprise or buried.
5. Any cell where the re-base flips a fairness reading from "short" to "over" will be named, not
   only counted.
6. The seat reports what it measures. It proposes no price change and requests no wiring.

---

*Order G, clock re-base instrument seat. Rule fixed before the numbers.*
