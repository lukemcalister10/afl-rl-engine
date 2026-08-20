# PREREG — D4 (fold the ramp in) and D5 (the owner's unwind shape)

**Seat:** ASSEMBLY BUILD. **Date:** 2026-08-19. **Branch:** `land/order-29`. **Charter:** register v754+.
**Pushed BEFORE the engine edit it describes** — the F6 discipline, second consecutive pass.

> **NOTHING LANDS. NOTHING MERGES. NO PULL REQUEST. NOTHING ON `main`. THE LIVE BOARD `88ce647f` IS
> NEVER TOUCHED.** The base for this pass is the current candidate **`81cf787b` / 665,238**.

---

## 1 · WHAT IS BEING DONE, IN ORDER

| | ruling | what it is |
|---|---|---|
| **D4** | **RULED — fold it in** | the `f**1.5` in-season ramp stops being a side variant and becomes part of the candidate proper |
| **D5** | **PRICE IT** | the owner's unwind shape replaces **both** binary and fractional as the R3 run-break rule |
| **D6** | **ADJUDICATE** | measure the unwind speed on the returner population; if the data cannot separate, **say so plainly** |

**ENGINE RUNS STRICTLY SEQUENTIAL** (five-var thread pinning per `bbASM.sh`). **The injury-consolidation
order (Decision 6, owner Option A) is QUEUED BEHIND this delivery and no part of it is wired here.**

---

## 2 · D4 — HOW THE RAMP IS FOLDED IN, AND WHAT IS DELIBERATELY *NOT* DONE

`RL_O41_RAMP` applies the engine's own D12 concave proration `tau' = f**1.5` — **already active and
already owner-ruled at two existing sites** — to the two **DEPTH** clocks (the sitter-fade clock's
in-progress accrual and the R3 current-run fraction). It is deliberately **not** applied to the I1
credit, which is a **participation weight**, on the engine's own stated reasoning at the D12 site.
None of that changes. What changes is that the dial goes **on** in the candidate.

**THE DIAL IS NOT BEING DEFAULTED ON, AND THAT IS THE WHOLE POINT.** Folding in means adding
`RL_O41_RAMP=1` to **the candidate's dial line**. It does **not** mean flipping `_O41_RAMP`'s default,
because the standing identity law is that **with every ORDER 41 dial unset the board is `374d4e44`**.
Flipping the default would make "unset" mean "on" and would break that identity at the root. **The
dial stays default-off; the candidate turns it on.** Anyone can still reproduce `374d4e44` by unsetting
everything, which is exactly what falsifier `D-A1` below checks.

**PREDICTED COST:** the ramp measured **+11 board points on 8 rows** as a standalone variant
(`db1ccef5` / 665,249 against `81cf787b` / 665,238). Folded in **underneath D5**, it may differ,
because the ramp governs the season fraction that D5's unwind then reads. **Both are built and both
are reported.**

---

## 3 · D5 — THE UNWIND SHAPE, STATED EXACTLY BEFORE IT IS WIRED

**THE OWNER'S WORDS:** *"their first 5 games on return each knock 20% off the sitter penalty."*
**THE FORM:**

```
u(g) = min(1.0, g / U0)        U0 = 5        # LINEAR. 20% per game. 5 games ⇒ fully unwound.
```

### 3.1 WHERE IT GOES — a third `RL_O41_BREAK` mode, replacing both existing ones

`RL_O41_BREAK` ∈ {`binary` (default, wired), `fractional` (priced v754), **`unwind` (new)**}. The
run walk in `o41_absence_depth` becomes, for **completed** seasons walking back from `Y`:

```
if u(g_yy) >= 1.0: break                    # 5+ games in a season fully unwinds ⇒ the run is broken
_n += 1.0 - u(g_yy)                         # otherwise that season leaves its un-unwound share standing
```

and for the **in-progress** season `Y` (this is item (4) of the order, stated exactly):

```
_n += max(0.0, 1.0 - u(g_Y)) * _o41_fe(Y, p)     # the residual absence × THE RAMPED SEASON FRACTION
if u(g_Y) >= 1.0: return 1.0                     # 5+ games this season ⇒ run broken outright
```

`_o41_fe` is the ramped fraction **because D4 folds the ramp in** — so the in-progress season's
residual absence is weighted `f**1.5`, not `f`. **That is the exact interaction the order asked to be
stated: the GAMES are counted raw and are NOT prorated; the ABSENCE they fail to unwind is what
carries the in-season weight.**

**THE ALTERNATIVE READING I AM NOT WIRING, NAMED SO THE CHOICE IS VISIBLE:** one could instead prorate
the *games threshold* — `u = min(1, g_Y / (U0 · f))` — so that at 92% elapsed only 4.6 games are needed
for a full unwind. **I am not wiring that.** The owner's phrase is *"their first 5 games on return"* —
a count of games actually played, not a count adjusted for how much season is left. Prorating the
threshold would mean a player needs **fewer** games to clear his penalty the later it gets, which
inverts the plain meaning. **If he meant the other one, this is the line to point at.**

### 3.2 WHAT IS STRUCTURALLY THE SAME AS `fractional`, SAID PLAINLY RATHER THAN DRESSED UP AS NEW

**Mechanically, `unwind` IS `fractional` with `u(g) = min(1, g/U0)` substituted for the F1 guarded
credit curve.** Same walk, same break condition, same in-progress term. **The only difference is the
SHAPE and the SPEED of the curve** — the F1 credit curve is concave and saturates at 11 games; the
owner's unwind is linear and saturates at 5. **That is not a criticism of the ruling; it is the reason
D6's adjudication is exactly the right question**, because "which curve, saturating when" is the only
thing separating the two rules.

### 3.3 THE CONSTANT, AND WHAT IT IS HONESTLY LABELLED

`U0 = 5` **is not measured by anything this seat holds.** It is exposed as `RL_O41_UNWIND` (default
`5`) so D6 can sweep it. **Unless D6 separates, `U0 = 5` is labelled RULED, NOT MEASURED**, on the
owner's word — which is lawful and has precedent in this engine (`G* = 2`, dose `0.40`, `eta 0.50`).
**It will never be described as measured.**

---

## 4 · D6 — THE BREAK-SPEED ADJUDICATION, AND ITS PREREGISTERED DESIGN

**THE ESTIMAND.** How much of an accrued absence penalty has genuinely unwound after a return season
of `g` games.

**THE MEASURED OBJECT ALREADY IN THE BOARD.** F2 measured exactly this on **134 returners** and the
engine already carries the result as `O41_REVERSAL`, which I2 consumes:

| return games | n | measured reversal | 90% CI |
|---|---:|---:|---|
| 1-2 | 38 | 0.1760 | [0.053, 0.333] |
| 3-5 | 29 | 0.1690 | [0.030, 0.353] |
| 6-9 | 27 | 0.0944 | [0.004, 0.214] |
| 10-14 | 22 | 0.2125 | [0.054, 0.449] |
| 15+ | 18 | 0.5959 | [0.321, 0.886] |

F2 itself published **`step_separable: false`**.

**THE TEST.** For each `U0 ∈ {3, 5, 7, 11}`, score `u(g) = min(1, g/U0)` as a predictor of the
**per-row** measured reversal on the same 134 returners, out of sample, by the **same instrument
already used and reviewed for the I1 credit-form adjudication** (`as_creditoos.py`): held-out folds,
bootstrap CI on every **pairwise** difference, and **the test is declared SILENT on any pair whose CI
straddles zero.** Thin cells marked. The reversal curve itself is included as a fifth arm so the
owner can see the owner-constant candidates against the measurement rather than only against each
other.

### 4.1 MY PREREGISTERED PREDICTIONS — WRITTEN BEFORE THE MEASUREMENT RUNS

| # | prediction | falsifier |
|---|---|---|
| **P-D-1** | **The adjudication will NOT separate the four speeds.** F2 already found its own bins non-separable on this sample, and 134 rows split five ways gives cells of 18-38 with CIs 0.3 wide. | any pair separating at the preregistered CI |
| **P-D-2** | **`U0 = 5` will score WORSE than the slower speeds against the measured curve**, and possibly worst of the four. The measurement says reversal is **~0.10-0.21 flat from 1 game to 14** and only reaches 0.60 at 15+. `min(1, g/5)` asserts **100% unwound at 5 games**; the measurement at 3-5 games reads **0.169**. **The owner's shape is roughly five times faster than the measured curve in that region.** | `U0=5` scoring best |
| **P-D-3** | **The unwind board will collect MORE than binary and LESS than fractional.** Unwind saturates at 5 games where the F1 credit saturates at 11, so more rows break their run under unwind. | any other ordering |
| **P-D-4** | **Brodie (1 game) is STRIPPED under unwind** — `u(1) = 0.2`, leaving 80% of the run standing. | Brodie restored |
| **P-D-5** | **Madden (7 games) is RESTORED under unwind** — `u(7) = 1.0` — where **fractional stripped him for 947**. This is the one place the owner's shape is plainly kinder than fractional. | Madden stripped |
| **P-D-6** | **day-0 stays 89/89 bit-identical.** The prediction most worth being wrong about. **A gameless row has no return games, so `u(0) = 0` and the unwind cannot reach him** — but that was true of the last three absence objects too and one of them broke it anyway. | 88 or fewer |
| **P-D-7** | no acceptance law moves: dial-off `374d4e44`, burn 0, class inside [1.03, 1.14), continuity clean | any of them moving |

**IF P-D-2 HOLDS, I WILL SAY SO IN THOSE WORDS AND I WILL NOT SOFTEN IT**, and I will **still deliver
the board the owner ruled**, because pricing a ruled shape and reporting that the measurement
disagrees with it are two different jobs and both are mine.

---

## 5 · FALSIFIERS ON THE BUILD ITSELF

| | fires if |
|---|---|
| **D-A1** | every ORDER 41 dial unset ≠ `374d4e44` |
| **D-A2** | day-0 ≠ 89/89 on any board built this pass |
| **D-A3** | determinism ×2 differs on any board |
| **D-A4** | `RL_O41_BREAK=unwind` with `RL_O41_R3` unset does not HALT |
| **D-A5** | `RL_O41_UNWIND` ≤ 0 or non-numeric does not HALT |
| **D-A6** | the ramp-folded board with `RL_O41_BREAK` unset ≠ the ramp-folded binary board (unset must equal binary) |
| **D-A7** | any board in the lever stack **at or before `L5C`** moves — the edit is confined to R3 and the ramp, so `L5C` **rebuilt on the edited engine must return `1270991c` byte-identical** |
| **D-A8** | the class mark leaves [1.03, 1.14) on the registered basis |

---

## 6 · WHAT THIS PASS DELIBERATELY DOES **NOT** DO

- **It does not touch the injury registers.** Decision 6 (owner Option A — retire `LTI_REGISTER.md`'s
  consumption) is **queued behind this delivery** and gets **its own prereg**. Engine edits stay
  strictly sequential; nothing here anticipates it.
- **It does not repair the continuity harness.** The R3-blindness found last pass
  (`os_lib.assemble` rebuilds the ORDER 31 law with no R3 term) is logged as a **named follow-up —
  INSTRUMENT, NOT BOARD** — on the coordinator's explicit instruction not to fix it inside this pass.
  **Consequence carried forward: the harness's age axis stays unreadable on any board carrying R3,
  and the birthday law is measured this pass with `as_r3age.py` instead.**
- **It does not adopt anything.** D5 is **priced**; the owner chooses between binary, fractional and
  unwind. D4 is **ruled**, so it is folded in.
- **It does not invent a break speed.** If D6 cannot separate, `U0 = 5` stands as an **owner constant,
  labelled RULED**, and no other value is wired.
- **It does not re-open LAMBDA**, which stays untouched at the anchor `0.1743833037`.
