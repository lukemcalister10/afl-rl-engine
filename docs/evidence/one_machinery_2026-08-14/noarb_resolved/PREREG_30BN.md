# PREREG_30BN — THE RESOLVED CANDIDATE'S NO-ARB READING

**ORDER 30B-N.** Brief: issue #334 comment 5310246218. Filed **BEFORE any engine run, any board build,
any emit and any instrument execution** in this seat. Branch `land/order-29`, filed at
`origin/land/order-29 = 129d0ce`.

**NOTHING WIRES PERMANENTLY.** This order extends the ORDER 30B-P preview lane's declared default-off
dial with a second default-off dial, `RL_O30B_RESOLVED`. With every dial unset the committed board
`9298203135202a0c707bb0977ba38c31` must reproduce **byte-exact**. No board ships. No numeraire is
re-pinned. The owner has ruled nothing.

---

## 0. WHAT IS BEING PRICED, STATED BEFORE IT IS MEASURED

The **resolved configuration** as ORDER 30B-R closed it (`resolution/BLEND_RESOLUTION_PACKET.md`,
`RESOLVED_ALLROWS.json`):

| task | ruling | consequence for this order |
|---|---|---|
| T1 READING | the **ADDITIVE** form `price = production + β(g)·v0` is the faithful one | replaces the preview's weight blend `(1−σ)P + σ·v0` |
| T2 CLOCK | **RAW career games RETAINED**; the recency clock lost its own held-out criterion | the games axis is `pv_games(p,Y)` unchanged from the preview |
| T3 CURVE | **THE JOIN** — four lanes | the whole shape of the law |
| T4 OBJECT | **OPEN** — the seat does not choose | this order prices the **v0 object**, which is what `RESOLVED_ALLROWS.json` totals |

**THE JOIN, the four lanes, verbatim from the resolution arithmetic
(`o30br_resolved.py::book()` / `o30br_allrows.py`):**

| lane | condition | price |
|---|---|---|
| **sitter** | zero games as of Y (`day0`) | `v0 · D(c)` — the Step-2 sitter law, **already live and untouched** |
| **thin** | `0 < g ≤ 10` | `v0 · D(c) · b_lift(g,c)` — the cumulative backbone as a **lift on the sitter price**. Production does **not** enter. |
| **bridge** | `10 < g < 16` | `thin10 + t·(d16 − thin10)`, `thin10 = v0·D·b_lift(10,c)`, `d16 = P + β(16)·v0`, `t = (ln(1+g)−ln11)/(ln17−ln11)` — a **DECLARED bridge, not a measurement** |
| **deep** | `g ≥ 16` | `P + β(g)·v0` |

`β(g)` is log-linear in log(games) between the five band midpoints, flat outside
(`READING.json::beta_curve`): **(2.5, 0.29683) (10.5, 0.36226) (25.5, 0.22330) (53.0, 0.15315)
(85.5, 0.02007)**. `b_lift` is `JOIN.json::backbone[lane]` normalised so `lift(0)=1`, log-linear in
`log1p(g)`, lane `2` if `c < 2.5` else `3`; backbone `2 = (0,.5684)(2,.656)(5,.6936)(10,.8236)`,
`3 = (0,.36)(2,.5933)(5,.6807)(10,.693)`.

**The lift values this seat will wire, tabled now so they can be checked against the build:**

| g | `b_lift` lane 2 | `b_lift` lane 3 | | g | β(g) |
|---:|---:|---:|---|---:|---:|
| 0 | 1.0000 | 1.0000 | | 10 | 0.359814 |
| 1 | 1.0946 | 1.3705 | | 16 | 0.287915 |
| 2 | 1.1541 | 1.6481 | | 25 | 0.225720 |
| 5 | 1.2203 | 1.8908 | | 50 | 0.157818 |
| 10 | 1.4490 | 1.9250 | | 75 | 0.035021 |

---

## 1. THE CONTROLS (P1–P5) — scored before any reading is believed

**P1 — DIAL-OFF BYTE IDENTITY.** With `RL_O30B_RESOLVED` and `RL_O30B_PREVIEW` both unset, a board
built from this seat's worktree with the resolved lane **in the file** reproduces
`rl_app_data.json` md5 `9298203135202a0c707bb0977ba38c31` **byte-exact**. Any other md5 fails P1 and
the order stops.

**P2 — THE PREVIEW LANE IS UNDISTURBED.** With `RL_O30B_PREVIEW=1` and `RL_O30B_RESOLVED` unset, the
board reproduces the committed preview board `6a392bca7ad0dee04a6b4f037c758f65` byte-exact. The new
dial extends the preview lane; it must not perturb it.

**P3 — THE CURRENT-BOARD ROW CONTROL (the calibration control).** With `RL_O30B_RESOLVED=1`, the
dialed build's 804 named rows reproduce `resolution/RESOLVED_ALLROWS.json` **row-for-row**, and the
book total is of the **715,229 class**.

> **P3 CARRIES A DECLARED, PRE-STATED TOLERANCE, AND ITS SOURCE IS NAMED NOW RATHER THAN DISCOVERED
> LATER.** `RESOLVED_ALLROWS.json` is **derived, not built**. Its production column
> `production_pts` was **not** read off the engine: `o30bp_movers.py:52` recovers it by **inverting
> the weight blend on the ROUNDED PRINTED preview price** —
> `prod = (v_printed − σ·v0) / (1 − σ)`. The printed price is an integer, so every `production_pts`
> carries a rounding residue of up to `0.5 / (1 − σ(g))` board points. The ev()-level wiring consumes
> the **true unrounded production leg**, so the two cannot agree to zero and it would be dishonest to
> claim they will.
>
> **PRE-STATED BANDS.** The residue reaches the price only through the lanes that consume `P`:
> * **sitter (89 rows) and thin (99 rows): EXACTLY ZERO.** Production does not enter either lane, so
>   these 188 rows must match to **< 0.05** board points. A miss here is a WIRING ERROR, not rounding.
> * **bridge (44 rows):** residue ≤ `t · 0.5/(1−σ(g))`, `g ∈ 11..15` → **≤ 1.2** board points.
> * **deep (572 rows):** residue ≤ `0.5/(1−σ(g))`, `g ≥ 16` → **≤ 1.0** board points.
> * **max |Δ| over all 804 rows: predicted ≤ 1.2 board points**, and the count of rows with
>   `|Δ| > 1.5` predicted to be **0**.
> * **book total: predicted within ±150 of 715,228.6** (804 zero-mean residues; ±0.02%).
>
> If max |Δ| exceeds 1.5, or if any sitter/thin row moves, **P3 FAILS and the finding is reported as
> a failure**, not re-tuned.

**P4 — DETERMINISM.** Two independent foreground builds at `RL_O30B_RESOLVED=1` produce identical
`rl_app_data.json` md5. Two independent emits produce identical matrix md5.

**P5 — THE INSTRUMENT PINS HOLD.** The Order-29 disclosed instrument copies run
**byte-unmodified**; `noarb_table_338.py` md5 `0f8220351c64c56ccfa90c60edcdfa5f` and the standing
emitter `bffde2f786be85037483e9f5f1563068` are asserted **at run**, never hardcoded into a claim.
Matrix-identity literals are re-pointed **only if identities actually moved**, with the header log
appended. **If a pin refuses, THE HALT IS THE FINDING** and is reported verbatim.

---

## 2. THE BASIS, FIXED BEFORE THE READING

**Year 0 is the LANDED ENTRY LAW** — `emit_matrix_29c.py`'s one declared change, the same year-0
column the 29C reading and the 2026-08-13 sitter-law preview used. It is **NOT** moved by this
order's dial: `_landed_v0_board()` reads `pvc_curve_v2.json::nd_v0.posv` and `MA.pool_v0_of`, which
is **the same arithmetic** as the engine's `day0_v0()` — verified by reading both, and re-verified
at run by the emitter's own fail-closed 89-of-89 replication proof against `DAY0_29B_FINAL.json`.

**Therefore every margin in this order moves only through the NUMERATOR.** `margin = 14% − apprec(0→1)`
with a fixed denominator. This is stated now because it is the whole logic of the predictions below.

---

## 3. THE PREDICTIONS (P6–P14) — the directional core

### The continuity column being predicted against

The **2026-08-13 sitter-law preview, SITALL variant**
(`landing_29_2026-08-13/noarb_sitter_preview/README.md`), and the LIVE board `88ce647f`:

| reading | LIVE (88ce647f) | landed law (O29CFINAL) | **SITALL** |
|---|---:|---:|---:|
| all-arm PRIMARY | +33.23% no arb | −19.10% ARB | **−4.39% ARB** |
| all-arm MODERN | +31.75% no arb | −12.48% ARB | **+2.13% no arb** |
| ND ALL 1–64 | +6.70% no arb | −16.74% ARB | **−4.76% ARB** |
| ND 1–20 | +1.82% no arb | −17.12% ARB | **−11.28% ARB** |
| ND 21–64 | +14.04% no arb | −16.12% ARB | **+5.67% no arb** |

SITALL faded **only the zero-game cells**. Every **played** cell in SITALL is still the landed law's
**un-rewired** evidence machinery. The resolved candidate re-prices **every** cell.

### P6 — THE YEAR-1 NUMERATOR FALLS, AND IT FALLS HARD. **DIRECTION: DOWN.**

The mechanism, stated so it can be falsified: at the yr1 cell the fade clock is `c ≈ 2.0`, so
`D(c) = 0.5502` and the backbone is lane 2. A yr1 entrant with **1–10 games lands in the THIN lane**,
where **production does not enter at all** and his price is `v0 · 0.5502 · b_lift(g)`, i.e.
**0.602·v0 at one game rising to 0.797·v0 at ten**. SITALL left exactly those cells on the
un-rewired marks, which sat near **1.37·v0** (decomposing SITALL's ND 1.1876 against the landed
1.3074). The thin lane is therefore a **~40% haircut on played rookies** relative to SITALL.

**BAND: ND ALL 1–64 yr1 ratio in [0.60, 1.05]** (SITALL: 1.1876). Point estimate **0.77**.

### P7 — EVERY ONE OF THE FIVE CONTINUITY MARGINS MOVES GREENER (more positive) THAN SITALL.
No exceptions predicted. **BAND: ND ALL 1–64 margin in [+9%, +54%]**, point estimate **+37%**.

### P8 — ARBITRAGE COUNT. **PREDICTED: 0 of 5** continuity readings red (SITALL: 3 of 5 red).
Stated as the sharp form; P9 names the one I expect to be closest to the line.

### P9 — THE ORDERING IS PRESERVED: **ND 1–20 stays the reddest ND reading, ND 21–64 the greenest.**
Top-20 picks play more games in year 1, so more of them clear `g ≥ 16` into the **deep** lane, where
production re-enters and `P + β(16)·v0` pays. **BAND: ND 1–20 margin in [+2%, +45%]**, and
`margin(1–20) < margin(21–64)`.

### P10 — THE ALL-ARM READINGS IMPROVE **LESS** THAN THE ND-ONLY READINGS. **A sharp, arm-level claim.**
`fade30b_of()` returns **1.0 for every pool row** — pool fade is Step 4's work and is **not derived**.
SITALL faded pool sitters at D(2)=0.624 / D(≥3)=0.380. So under the resolved wiring **pool sitter
cells RISE** relative to SITALL while ND sitter cells barely move. The all-arm instrument carries
902 pool rows; the 338 instrument is ND-only. **Predict: `Δmargin(PRIMARY) < Δmargin(ND ALL 1–64)`.**

### P11 — THE SITTER CELLS THEMSELVES BARELY MOVE FOR ND, AND MOVE THE WRONG WAY AT DEPTH 4.
Wired `D(2)=0.5502 · D(3)=0.2628 · D(4+)=0.3460 FLAT` vs SITALL's candidate
`0.5684 / 0.3600 / 0.3073`. Depth 2 and 3 are **lower** (greener), depth 4+ is **higher** (redder).
The depth-4 kink is **selection, n=11**, kept and disclosed — not smoothed.

### P12 — THE COHORT PATH STEEPENS: a deep yr1 dip followed by a strong climb.
The additive reading pays **deep** players more (`+11.12%` book at the 2026 board before the join
claws back to `+5.20%`). **Predict `ratio(yr4)/ratio(yr1)` is materially HIGHER under the resolved
candidate than under SITALL**, and that the resolved PRIMARY path is **non-monotone-improving**:
lowest at yr1, rising through yr4.

### P13 — BY ARM, yr1/yr4. Predict **ND and RD yr1 both fall below 1.0**; predict **MSD** remains the
anomalous arm (its d=0 denominator is empty — ORDER 26A anomaly 5, carried, not rediscovered).

### P14 — MARK-PATH AND REVERSE NO-ARB. The 29B landed reading was mark-path **6 of 10** and reverse
no-arb **10 of 10, 0 fail**. Predict reverse no-arb **holds at 10/10**; predict mark-path
**does not improve above 6/10** and may fall further, because the thin lane deliberately flattens
d1–d2 against d0.

---

## 4. ANOMALIES I EXPECT TO HAVE TO REPORT (named before they are seen)

1. **The thin lane is a cliff, not a curve.** A rookie who plays one game is priced at ~0.60·v0 while
   his teammate who plays none is priced at 0.5502·v0 — but the landed law paid the first ~1.37·v0.
   The resolved candidate's green margins at yr1, if they arrive, arrive **because rookie marks
   collapse**, and that is a finding about the join, not a vindication of the law.
2. **Pool β is provisional** — pool `v0` cells are Step 4's work and pool fade is forced to `D=1.0`.
3. **The ruck-head defect is OPEN.**
4. **PRE-NUMERAIRE** — Step 6's re-pin has not run. Read the MOVEMENT, not the level.
5. The MSD games-of-12 scaling (ruling 5) makes 38 of 804 rows carry **fractional** games; it is the
   only place the games axis is not raw games.

## 5. SCORING

Each of P1–P14 is scored **HELD / BREACHED / PARTIAL / NOT SCORABLE** against the run output. **No
prediction is edited after a reading exists, and no parameter is tuned to close a margin. Red is red
and gets reported.** Any wiring question the resolution arithmetic does not determine: **STOP and
report** rather than choose.
