# PREREG J — THE CORRECTED GATE, PUSHED BEFORE ANY DOSE RESULT IS INSPECTED

**Seat:** ORDER J. **Authority:** issue #334 comment **5320813582** (owner, 2026-08-18) — R-TALLFACTOR
adopted, Order J commissioned. **Base:** the landing candidate **1f176444** (RL_O35 stack). **Dial:**
the existing `RL_O36` wire, reused unchanged. **Dial-off must reproduce 1f176444 byte-exact.**

This file fixes, in advance and in one place: the tolerance rule for the counterweight, the reasoning
that produced it, the numbers it evaluates to on this board, the search grid, the selection law, the
named-row predictions and the falsifiers. **Nothing below may be edited after the first dose result is
read.** Any change is an amendment, dated, with the reason, and the original left standing.

---

## 0 · WHAT THIS SEAT WAS TOLD TO CORRECT

Order I concluded there is no joint solution. That verdict was produced in part by a gate error, and
the owner has named the error himself:

> the counterweight keys on **games, not age**, so it inevitably grazes veterans by a few points …
> counterweight knob moves failed at worst-row deltas of **3.35** (eta 0.42) and **5.32** (kappa 0.25)
> points — rounding-level moves failing a tolerance-zero test.

So the zero-tolerance mature test — correct and achievable on the age surface — was wrongly carried
onto the counterweight. This order re-runs the search under a corrected gate.

**The integrity crux.** A tolerance chosen after seeing which settings need it is not a gate, it is a
rationalisation. This file is pushed **before the first dose result of this order is read**, and the
rule below is derived from properties of the board and of the owner's own stated practice — never
from the size of the move any particular setting happens to need.

**What this seat had already seen when it wrote this rule, declared so the reader can judge it:** the
two worst-row numbers 3.35 and 5.32 are printed in the owner's own commissioning comment, so they
could not be unseen. They are not what set the rule. The rule below is set from (i) the unit the board
is printed in, (ii) the grain at which the owner states his own targets, (iii) the instrument's own
measured uncertainty and (iv) the movement the owner has *already ruled acceptable* on the exempt
lever. Clause (iv) sets the per-row ceiling **tighter than a movement the owner has already accepted**,
which is the opposite of a rule bent to let something through. Whether 3.35 and 5.32 pass is a
consequence of the rule, reported as such.

---

## 1 · THE CURRENCY, FIXED FIRST

Every number in this file is in **BOARD POINTS** — the currency the owner reads and the currency the
published board prints. The engine's internal `ev()` is restated in board points by the engine's own
owner-ruled re-denomination scalar:

```
board points = ev / 1.0524        (engine/rl_after/pick_redenomination.json, "factor")
```

The published board rounds that to an integer. Gate arithmetic uses the **unrounded** quotient, so
integer rounding can never blunt or flatter a measurement.

**Baseline facts, measured on 1f176444 with the dial off, before this rule was written**
(`o37_baseline.py` → `BASELINE_J.json`):

| object | board points |
|---|---:|
| active priced rows | **804** |
| BOARD TOTAL | **667,913.3** (published integer sum: 667,916) |
| mature rows, age 24+ | **429** |
| MATURE POOL TOTAL | **362,703.0** (54.30% of the board) |
| young rows, under 24 | 375 |
| young pool total | 305,210.3 |
| mature row value — min / p10 / median / p90 / max | 3.3 / 29.8 / 258.2 / 2,251.9 / 9,385.7 |
| mature rows worth under 200 board points | **176 of 429** |

Those are properties of the base board. They depend on no dose and no knob.

---

## 2 · THE GATE DISCIPLINE — THREE LEVERS, THREE DIFFERENT RULES

### 2.1 · S1, the age surface — **ZERO TOLERANCE, UNCHANGED**

Every active row aged 24 or over must be **byte-identical** to the landing candidate, store-wide,
tolerance exactly 0. This is not softened, because it is **proven achievable**: Order I measured 0 of
429 rows moving at every dose from 0.15 to 1.00. Zero is the right rule here because the mechanism is
keyed on **age** and is flat from 24 by construction — a mature row *cannot* move unless something has
leaked. Order I found three such leaks that way (PACKET_I §2: the load-time denominators, the memoised
synthetic pedigree row, the vantage-vs-row age cap). **Those three fixes are kept.** A regression here
is a defect, not a rounding.

### 2.2 · The counterweight — **J-TOL, the rule preregistered here**

The counterweight is the O32 re-mix (`kappa`, `gamma_u`, `eta`, `gamma_d`) and the selection relief
(`lambda_rel`). It keys on **career games**. A 27-year-old with 141 games sits on the same reliability
curve a 19-year-old with 141 games sits on. Move the curve and he moves. Zero is therefore not
achievable and never was; demanding it is demanding that the mechanism not exist.

What the owner's law actually requires is this, in plain words:

> **This young-player mechanism must not silently reprice veterans.**

"Silently" is the operative word. A veteran has been repriced when a human reading the board would see
a different number for him, or when the veteran pool as a whole has shifted against the young pool.
Both are measurable. So:

> ### J-TOL — a counterweight setting PASSES the mature-row gate if and only if all three hold,
> ### measured store-wide on every active row aged 24+ on the 2026 board, in board points, against
> ### the landing candidate 1f176444.
>
> **(a) PER-ROW CAP.** For every mature row *i*:
> ```
> |Δ_i|  ≤  min( 25.0 ,  max( 1.0 , 0.005 × v_i ) )
> ```
> where `v_i` is the row's own landing-candidate board price.
>
> **(b) AGGREGATE CHURN CAP.** `Σ|Δ_i|` over the mature pool ≤ **0.15% of the board total**
> = **1,001.87** board points.
>
> **(c) AGGREGATE NET CAP.** `|Σ Δ_i|` over the mature pool ≤ **0.10% of the board total**
> = **667.91** board points.
>
> All three are hard. A setting that fails any one of them is not carried, whatever it does for the
> owner's laws.

**Why (a) has that shape, and those three numbers.**

- **A percentage, because "repriced" is a relative idea.** Twenty board points on a 4,500-point
  veteran is invisible. Twenty board points on a 30-point fringe veteran is a two-thirds repricing.
  A flat absolute tolerance would be simultaneously absurdly loose at the top of the board and
  absurdly tight at the bottom. 176 of the 429 mature rows are worth under 200 points; a percentage
  is the only shape that is fair to both ends.
- **0.5%, because that is a tenth of the grain the owner states his own targets in.** The owner
  specifies levels to the nearest hundred board points — "dean ≈ 2,600", "duff-tytler ≈ 1,800",
  "smillie in the ~700s". A half of one percent of a row's value is an order of magnitude finer than
  the resolution at which the owner himself expresses what a row is worth. It is also roughly sixty
  times inside the instrument's own measured uncertainty: the hindsight weight W has a 90% bootstrap
  CI of [0.3117, 0.5560] about 0.4127, a ±29% band.
- **The 1.0-point floor, because the board prints integers.** One board point is the smallest unit the
  published board can express. Holding a 30-point fringe veteran to 0.15 of a point is holding him to
  a number the board cannot display. The floor exists so the bottom 176 rows are gated at the board's
  own resolution rather than below it.
- **The 25-point ceiling, because it must not be possible to hide a real move inside a big row — and
  because the owner has already told us where "acceptable" sits.** The owner has ruled the tall
  factor ADOPTED knowing it moves 50 mature rows, 446 `ev`-points in total, **largest single move
  ≈41 `ev`-points = 39 board points**. The ceiling here is **25 board points — tighter than the
  largest single mature move the owner has already accepted on the exempt lever.** The gate this seat
  is setting for the *gated* mechanism is therefore stricter, per row, than the movement the owner has
  explicitly ruled fine on the *exempt* one. The ceiling binds only on rows worth more than 5,000
  points, of which there are few.

**Why (b) and (c), and those two numbers.**

Per-row caps alone can be gamed by a mechanism that nudges every row a little in the same direction.
That is exactly "silently repricing veterans", and only an aggregate catches it.

- **(c) NET is the sharp instrument.** It asks: has the veteran pool as a whole moved against the
  young pool? 0.10% of the board is 667.9 points — under **0.19%** of the mature pool's own 362,703.0 (0.184%).
  A shift smaller than a fifth of one percent of the veteran pool is not a repricing of veterans; it
  is the residue of a mechanism that is aimed elsewhere.
- **(b) CHURN catches movement that cancels.** Rows moving in both directions can leave the net near
  zero while every individual has been re-rated. 0.15% of the board is 1,001.9 points — under
  **0.28%** of the mature pool (0.276%). Spread over 429 rows that is an average of 2.3 points a row.
- **They are set against the BOARD total, not the mature total, deliberately**, because the harm the
  owner is guarding against is a shift in the *board's* balance between old and young. The mature-pool
  percentages are printed above so the reader can see both readings.
- **They bind.** If every mature row moved its full per-row allowance under (a), `Σ|Δ|` would come to
  roughly 2,100 points. Cap (b) is 1,001.9 — about half of that headroom. (a) and (b) are both live
  constraints; neither is a rubber stamp on the other.

**What J-TOL is NOT.** It is not a percentage of the *move* a setting wants to make. It is not keyed
to any knob, dose or row. It does not know which settings are near it. It is three inequalities in
board points, and it was written down before this order read a single result.

### 2.3 · The ruled tall factor — **EXEMPT, AND DISCLOSED IN FULL**

`m_TALL ≈ 0.677` via `h_TALL = −0.6921227120657417`, with `s_norm'` re-solved so the redistribution
identity holds exactly (Order H solved **1.4284052406915069**; the pick-weighted mean of `D2^kappa`
over H's fitted sitters must still equal the ruled depth-2 fade **0.5582775**).

**R-TALLFACTOR is ADOPTED by the owner.** It is an intended change. It is therefore **not gated** —
not by J-TOL and not by the zero-tolerance test. It is **DISCLOSED**:

- its **full moved-row list** for mature rows, every row named, with age, pick and its move;
- its totals — rows moved, absolute total, net total, largest up, largest down;
- the **redistribution identity residual**, printed, and build-failing if it exceeds 1e-9;
- its effect on the day-0 printed prices of all 89 wired entrants, with the count up and down and the
  extremes named, exactly as Order D disclosed the same class of re-base when the pick-curve fade
  landed;
- the proof that `derived_v0` — the raw entry object the walk-forward matrix writes as year-0 — is
  **bit-identical on 89 of 89**. Entry values do not move. What moves is the printed price of a player
  who has already sat, because that price is entry value × sitting discount and this factor changes
  the discount for talls. That is the intended effect and the owner has said so.

---

## 3 · THE SEARCH — THE OWNER'S LAWS ARE THE ONLY TARGETS

No diagnostic is optimised toward. Not the clock-fair benchmark, not the vantage matrix, not the
corrected-surface SSE except as the declared tie-break below.

| law | what it asks | measured on |
|---|---|---|
| **G1** | year-1 class cohort grows: floor **1.03**, ideal **~1.08**, strictly below the **1.14** buy rail | the W2 estimator `mean_0515`, classes 2005–2015, class bootstrap seed 33 |
| **G2** | picks **31-40** and **41-64** yr0→1 materially improve; **aspiration**: no sell-red band remains. Every band reported. | the standing **extended-338** five-band table, committed md5 `d59ad550116ebbe3d90ed82becd2c4d5` |
| **G3** | no band or pool arm above **+14%** yr0→1 | extended-338 bands + the all-arm pool instrument, both windows |
| **G4** | **dean ≈ 2,600** and **duff-tytler ≈ 1,800** board points (their Candidate-31 levels 2,670 / 1,832) | the 2026 board |
| **G5** | sub-expectation-with-games rows do NOT rise: **xavier-taylor, daniel-annable, dylan-patterson** | the 2026 board |
| **side** | **josh-smillie** holds his ruled ~700s range | the 2026 board |
| **side** | standing continuity asserts — no cliffs in age, games or pick | the ruled at-bar continuity object, `rho32` monotonicity, the tall curve's smoothness |

**SSP's inherited +50.52% buy-red is a preregistered INHERITED breach.** SSP rows enter at pick 65,
outside the 1–64 pick curve; no lever in this order reaches them. It is reported separately, with its
number, and it is **never allowed to stand in for or mask a new breach**. G3 is scored on the bands and
arms this order can reach, and the inherited arm is printed beside it, labelled.

### 3.1 · The grid (declared)

| axis | values |
|---|---|
| `lambda_S1` | the 15 doses already extracted: 0.00, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.85, 1.00 |
| `kappa` | 0.15, 0.18, 0.20, 0.22, **0.24**, 0.26, 0.28, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60 |
| `gamma_u` | 8, 10, **11**, 12, 14, 16 |
| `eta` | 0.00, 0.10, 0.20, 0.30, 0.35, 0.40, **0.41**, 0.45, 0.50 |
| `gamma_d` | 4, 6, 8, 10, 12, **14** |
| `lambda_rel` | 0.80, 0.90, 1.00, **1.08**, 1.20, 1.30 |

Bold is the wired repair point. 408,240 grid points. A declared refinement pass around the feasible
set is permitted and its grid is printed.

### 3.2 · The ruled feasibility constraints (hard, never traded)

- `rho32` monotone in games and strictly below 1;
- the ruled at-bar continuity object — integer game steps 0..20, tolerance 1e-9, age credit included;
- hindsight weight `W` inside the corrected 90% CI **[0.3117, 0.5560]**;
- calibration slope inside **[0.885, 1.115]**;
- **max single class mark ≤ 1.139** — the ruled 1.14 no-arbitrage line;
- **J-TOL** (§2.2) on the counterweight, and **zero** on S1.

### 3.3 · The two instruments, and which one decides

The grid is swept on the **calibrator** — the analytic walk-forward legs, which is the only instrument
cheap enough to visit 408,240 points. The calibrator's ND band subsets are known to **run hotter** than
the standing extended-338 (Order I printed both: at dose 0.25 the calibrator read picks 11-20 at
+16.96% where the extended-338 read +14.49%). The two are **never mixed in one row**.

**Registered now, so it cannot be chosen later:** the calibrator is a **navigation aid**. The
**standing extended-338 and the all-arm pool instrument DECIDE G2 and G3**, run whole and unmodified on
a real built board. The chosen point and a declared set of runners-up are built and run on the standing
instruments, and the standing numbers are the ones the gates are scored on. If the standing instrument
overturns a calibrator result, **the standing instrument wins and the overturn is printed.**

### 3.4 · The order of operations, fixed

1. `o37_baseline.py` — the base-board facts (**done before this file was written**).
2. Push this prereg.
3. `o37_mature_gate.py` — J-TOL measured store-wide on a declared knob ladder AND on the search's
   surviving candidates, with `RL_O36_TALL=0` so the exempt lever is out of the measurement and every
   Δ is attributable to S1 + counterweight alone.
4. `o37_sweep.py` — the analytic grid, ruled constraints, owner's laws.
5. The J-TOL gate run on the top **40** points by the selection law, in rank order, plus the full
   single-axis knob ladder so the admissible region is **mapped**, not spot-checked.
6. If a joint setting survives: build the boards, run the standing instruments, the board gates, the
   ledger, both preview pages, the packet.
7. If none survives: the trade-off curve, the binding law named with its number, no build.

### 3.5 · Selection law (registered)

Among grid points that satisfy **every** ruled constraint in §3.2 **and** the owner's laws G1–G5 as
computed on the calibrator, choose the point with **minimum corrected-surface SSE**. Ties broken by
smaller `lambda_S1`, then by `kappa` closer to the wired 0.24.

If that set is empty, the constraint set is relaxed **in one declared order only** — the *aspirations*
before the *laws*: first G2's "no sell-red" aspiration (the owner wrote it as an aspiration, not a
rail), then G4's neighbourhoods. **G1's rail, G3's +14% line, the ruled 1.139 line, J-TOL and S1's zero
are never relaxed.** Each relaxation step is printed with what it bought.

If the region is still empty, the seat **HALTS AND REPORTS**: which law binds, by how much, and the
**trade-off curve** — what class level is reachable at each late-band improvement level — so the owner
can choose knowingly.

---

## 4 · NAMED-ROW PREDICTIONS (the scorecard)

Direction is the prediction; it is scored as stated and never rewritten.

| row | pos / age / pick / games | predicted | mechanism |
|---|---|---|---|
| **harry-dean** | KPD 19 / p3 / 17g, 59.7 vs age bar 44.8 | **UP** | S1: he is 14.9 a game clear of his own age bar |
| **cooper-duff-tytler** | KPF 19 / p4 / 13g, 50.3 vs 43.2 | **UP** | same, smaller margin |
| **xavier-taylor** | SD 19 / p11 / 2g, 42.0 vs 55.2 | **DOWN** | *if the counterweight moves*: weight off pedigree onto a poor production leg. FLAT-to-UP if J-TOL pins it |
| **daniel-annable** | MID 19 / p6 / 2g, 38.0 vs 57.0 | **DOWN** | as xavier-taylor |
| **dylan-patterson** | SD 19 / p5 / 5g, 35.6 vs 55.2 | **DOWN** | as above, larger g so larger charge |
| **oskar-taylor** | SD 19 / p15 / **0g** | **UP, from the tall/small fade only** | no games, so S1 and the re-mix cannot reach him; the ruled fade can |
| **josh-smillie** | MID 20 / p7 / **0g** sitter | **UP, out of the ~700s** | the ruled tall factor's 0.5 clip at small picks 1-9. **Pre-declared tension** — reported, not cured |
| **milan-murdock** | SF **26** / SSP / 17g | **moves, and inside J-TOL** | age 26 with 17 games sits inside the re-mix's active zone. Under J-TOL his cap is 1.0 board point. Printed either way |
| **chris-scerri** | SF 20 / SSP p65 / 7g | **UP** | pool row, small pedigree, production dominates |
| **thomas-burton** | SF 19 / SSP p65 / 5g | **UP** weakly | same channel, below-bar output |
| **will-green** | RUCK 21 / p16 / 1g sitter | **UP** | ruled tall factor at p16 |
| **toby-conway** | RUCK 23 / p24 / 6g | **UP** | ruled tall factor at p24 |
| **steely-green** | SF 22 / p55 / 43g | **DOWN** small | late small pays for the talls' relief; his fade clock is spent |
| **isaac-kako** | SF 20 / p13 / 36g | **UP** | S1 on a high-rho row |
| **alix-tauru** | KPD 20 / p10 / 18g | **UP** | S1; tall age gaps are the largest |
| **jedd-busslinger** | KPD 22 / p13 / 15g | **UP** | S1 + ruled fade on an above-age-bar season |

**Pre-declared tension, restated so it is reported and not discovered:** G1's ideal of 1.08 moves the
class mark **further above** Order G's clock-fair benchmark [0.9761, 0.9892], while staying under the
1.14 rail. Both readings are printed side by side. The owner's law G1 governs; the clock-fair reading
is the diagnostic it was ruled to be.

---

## 5 · FALSIFIERS — any one firing is reported in the packet, in these words

- **F1** — any mature row moves under **S1 alone**, at any dose, by more than 0.0. **Build-failing.**
- **F2** — a carried setting fails **J-TOL**. **Not carried**, and the number printed.
- **F3** — `RL_O36` unset does not reproduce **1f176444** byte-exact. **Build-failing.**
- **F4** — `derived_v0` is not bit-identical on 89 of 89. **Build-failing.** (The *printed* day-0 of
  sitters moving is the ruled fade's disclosed effect, not a failure.)
- **F5** — the tall redistribution identity misses **0.5582775** by more than 1e-9. **Build-failing.**
- **F6** — `rho32` non-monotone, or any continuity assert in age / games / pick fires. **Build-failing.**
- **F7** — no grid point satisfies the ruled constraints, J-TOL and the owner's laws jointly.
  **HALT AND REPORT** with the binding law named, its shortfall in its own units, and the trade-off
  curve printed.
- **F8** — any sub-expectation-with-games named row RISES. Reported by name with its number.
- **F9** — determinism ×2 differs. **Build-failing.**

---

## 6 · WHAT THIS SEAT DOES NOT DO

It does not amend J-TOL after seeing a result. It does not optimise toward any diagnostic. It does not
relax G1's rail, G3's line, the ruled 1.139 line, J-TOL or S1's zero. It does not decide whether the
day-0 re-base is acceptable — that is the owner's ruling and it is disclosed for him to make. It does
not re-open smillie's fade. It does not land anything on its own word.

*— ORDER J. Prereg pushed before the first dose result of this order was read.*
