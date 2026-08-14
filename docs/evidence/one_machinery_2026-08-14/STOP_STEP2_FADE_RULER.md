# STOP AT STEP 2 — AN OWED OWNER WORD. The fade re-derived against its own ruler is NOT the ruled row.

**ORDER 30B build seat · `land/order-29` · 2026-08-14 · nothing beyond Step 1 is wired · PR #510 stays HELD.**

The brief's rule: *"If a design question arises that the rulings do not cover, STOP and report it as an
owed owner word rather than choosing."* This is that question. It decides the price of every sitter at
depth ≥ 3 by up to **3×**, so the seat will not choose it.

---

## 1. WHAT WAS DONE, AND THAT IT WAS DONE CORRECTLY

**R1 is binding and was obeyed.** Step 1 landed the positional v0 re-fit (`860d370`), and the fade was
then re-derived against the **STEP-1 FINAL v0s** using `o30a2_recut.py` **byte-identical**
(md5 `fe6f436ab23056d717f693091946309a`, verified against the 30A-2 copy). The only thing that changed
under the instrument is `nd_v0.posv` — the denominator of every ratio it forms.

- run: `o30b_fade_rederive.py` → `FADE30B_TABLE.json`, `FADE30B_out.txt`
- drift: `o30b_fade_drift.py` → `FADE30B_DRIFT.json`, `FADE30B_DRIFT_out.txt`

**The re-derivation is sound, and the attribution proves it is not an artefact of Step 1:** the mean `v0`
over the 1,140 common fitted rows moves **+0.05 %** (748.05 → 748.44). The re-fit **redistributed** value
across cells; it did not shift the level. The 2 rows the A2 cure re-admits (`tom-derickx`, `tom-downie`,
both on the old RUCK zero cells that ORDER 30A dropped as `v0 == 0`) are named.

---

## 2. THE READING

| depth | **ON THE 29B v0s — the numbers RULING 1 NAMES** | n | **ON THE 30B v0s — R1's re-derivation** | n | drift |
|---|---:|---:|---:|---:|---:|
| 1 | 1.0000 | 1140 | 1.0000 | 1142 | — |
| 2 | **0.5684** | 462 | **0.5502** | 464 | **−0.0182** |
| 3 | **0.3600** | 100 | **0.2628** | 100 | **−0.0972** (−27 % relative) |
| 4 | *0.3073 — bound* | 11 | *0.3460 — bound* | 11 | **+0.0387** |
| 5 | UNRESOLVED | 2 | UNRESOLVED | 2 | — |

`RAW(1)` normaliser 1.028605 → 1.020106 (**−0.83 %**).

**THE UNCONDITIONAL ROW STAYS MONOTONE ON BOTH RULERS** (0.5502 / 0.1579 / 0.0846 / 0.0509 / 0.0610).
The problem is confined to the **listed-conditional** row — the one that was ruled.

**The cumulative games backbone (ruling 4) barely moves and is NOT in question:**
0.5684 → 0.5502 (≤0) · 0.6560 → 0.6485 (≤2) · 0.6936 → 0.6887 (≤5) · 0.8236 → 0.8223 (≤10).
Max drift 0.0182. **Ruling 4 survives the re-derivation intact.**

---

## 3. THE TWO THINGS THAT BREAK, STATED PLAINLY

### (a) The ruled sequence stops being a decay.

`0.5502 > 0.2628` **`< 0.3460`**. Depth 4 now prices **above** depth 3. On the ruled ruler the sequence
was 0.5684 > 0.3600 > 0.3073 — monotone. **PREREG P9 is BREACHED and is owned here.**

### (b) Ruling 2 stops being evaluable at year 4.

Ruling 2: *"DEEP END = EXTRAPOLATE the fitted decay past yr4."* Fitting `D(c) = exp(−a(c−1)^b)` through
the resolved depths 2 and 3:

| ruler | fitted decay | at c=4 | at c=5 | at c=6 | vs the MEASURED depth-4 cell (n=11) |
|---|---|---:|---:|---:|---|
| **RULING** (29B v0s) | `exp(−0.5650·(c−1)^0.8547)` | 0.2358 | 0.1576 | 0.1069 | measured 0.3073 — **1.30×** the fit |
| **R1** (30B v0s) | `exp(−0.5975·(c−1)^1.1614)` | **0.1176** | 0.0503 | 0.0208 | measured 0.3460 — **2.94×** the fit |

On the ruled ruler the two readings of the deep end were compatible (a 30 % gap over an n=11 cell).
**On R1's ruler they are 3× apart.** "Extrapolate the fitted decay past year 4" has no unambiguous
meaning when the fitted decay says 0.118 at year 4 and the cell it is supposed to continue from says
0.346.

---

## 4. WHY THE SEAT WILL NOT PICK

**The two instructions in front of the seat point opposite ways, and both are the owner's.**

- **Ruling 1 adopted numbers.** "FADE LAW ADOPTED — listed-conditional years-only
  **0.5684 / 0.3600 / 0.3073-bound**". The brief says *"Expect values near 0.5684/0.3600/0.3073; report
  the drift"* — which reads as: the ruled row is the law, the re-derivation is a check, report the
  difference. Under this reading I wire the ruled constants.
- **R1 mandated a ruler.** "v0 re-fit FIRST, then RE-DERIVE the fade against the FINAL v0s
  (calibration-ruler consistency)." The fade is a **ratio to v0**. v0 moved. Wiring the old ratio against
  new denominators prices sitters on a ruler that no longer exists. Under this reading I wire 0.5502 /
  0.2628 / and something at 4.

R1 exists precisely because the seat was expected to find *small* drift. It found small drift at depth 2
(−0.018) and a **sign-flipping 27 % move at depth 3** that turns the law non-monotone. **The pre-flight
risk anticipated the question; it did not answer it.**

---

## 5. WHAT IT COSTS — THE NAMED ROWS, PRICED UNDER EACH OPTION

Continuous clock `c = (Y − debut) + 1 + φ`, `φ = 0.92`, log-linear, on the **Step-1 v0s**:
`smillie` `posv[MID][7]` = **1688.81** · `demattia` `posv[MID][25]` = **890.60** ·
`knobel` `posv[RUCK][42]` = **830.54** (all three cells barely moved in the re-fit).

| option | law wired at 2 / 3 / 4 | deep end | `smillie` c=2.92 | `demattia` c=3.92 | `knobel` c=4.92 |
|---|---|---|---:|---:|---:|
| **A** — the ruled constants, drift disclosed | 0.5684 / 0.3600 / 0.3073 | fitted, past 4 | D 0.3734 → **631** | D 0.3112 → **277** | D 0.1663 → **138** |
| **B** — R1 re-derived, measured depth-4 kept | 0.5502 / 0.2628 / 0.3460 | fitted, past 4 | D 0.2788 → **471** | D 0.3385 → **301** | D 0.0587 → **49** |
| **C** — R1 re-derived, fitted decay from 4 on | 0.5502 / 0.2628 / *0.1176* | fitted, from 4 | D 0.2788 → **471** | D 0.1255 → **112** | D 0.0539 → **45** |

*(arithmetic on the packet's own convention, `named.py`-class scratch; **nothing is wired**.)*

**The spread is 2.7× on `demattia` (277 / 301 / 112) and 2.8× on `knobel` (138 / 49 / 45).** And note
B and C nearly agree on `knobel` while disagreeing by 2.7× on `demattia` — the option boundary does not
fall where intuition puts it, which is another reason the seat will not pick it.

**A SECOND, SMALLER THING THE OWNER SHOULD SEE WHILE RULING.** Packet 2 §4.2 printed `knobel` at **256**
under *"held flat at the deepest resolved L-B depth"*. **Ruling 2 replaced held-flat with EXTRAPOLATE**,
and on the ruled constants alone that takes him **256 → 138** before any re-derivation is considered.
That is a consequence of ruling 2, not of R1, and it is disclosed here rather than inside a board.

---

## 6. THE WORD THE SEAT IS ASKING FOR

**Q1 — WHICH NUMBERS.** Does the fade wire the **ruled constants** (0.5684 / 0.3600 / 0.3073, drift
reported as a disclosed sensitivity), or the **R1 re-derived** row (0.5502 / 0.2628 / …)?

**Q2 — THE DEEP END.** If R1's row is wired: at depth 4, does the law take the **measured n=11 cell**
(0.3460, and accept that the schedule is non-monotone there), or the **fitted decay** (0.1176, monotone
but 3× below the cell and below the bound ruling 1 published)?

**Q3 — MONOTONICITY.** Is the fade schedule *required* to be monotone non-increasing in depth? If yes,
that is a constraint the derivation must be given (an isotonic pass over the resolved depths), and it
answers Q2 by itself. If no, the kink at 4 is wired as measured and disclosed.

---

## 7. STATE AT THE STOP

| | |
|---|---|
| branch / tip | `land/order-29` — see the push accompanying this note |
| board | **`84c9ea16f8ac5ac45e4e2359a718e7d2`** (Step 1 only), total **718,019** (entry 717,527, +492) |
| entry control | **PASS** — `36d5dfc7` reproduced byte-exact before the prereg was written |
| Step 1 | **COMPLETE** — 107 ascents → 0, A2 cured, conservation exact, residual disclosed, 43 movers all `cg == 0` |
| printed-day-0 identity | **PASS — 89 of 89, tolerance 0**, re-verified against the new cells |
| Step 2 | **DERIVED, NOT WIRED.** No fade is in the engine. `los_decay` remains the operative fallback |
| Steps 3–7 | **NOT STARTED** — every one of them consumes the wired fade |
| store / `v0surf` / `rl_model.py` | **UNMOVED** |
| PR #510 | **HELD — `[HELD — DO NOT MERGE]`** |

**Nothing was tuned after seeing the reading. The re-derivation was run once, against the final v0s, with
a byte-identical instrument, and this note was written from its first output.**
