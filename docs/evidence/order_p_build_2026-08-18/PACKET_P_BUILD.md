# PACKET P-BUILD — THE PEDIGREE-CONDITIONAL CHARGE IS BUILT. IT DOES ALMOST EXACTLY WHAT WAS PREDICTED.

**Seat:** ORDER P BUILD. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**Prereg:** `PREREG_P_BUILD.md`, pushed at `8a75862` before the first engine edit.

**Nothing is adopted and nothing lands on this seat's word.** This is a build, its proofs, and its
failures.

**Pins.** engine `_merged_recover.py` `7df6a923` · `rl_model.py` `e1076eff` · store `cb38ef11` ·
matrix `per_entrant_PBUILT.json` `d4120560`.
**Boards.** live `88ce647f` 752,429 · candidate 31 `fe6be9d6` 666,913 · landing `1f176444` 667,916 ·
**ORDER K `f3101883` 673,097** · **ORDER P `374d4e44` 666,434** · uncharged `73bf9617` 702,734.

---

## 1 · THE ANSWER, IN TWELVE SENTENCES

**The blind charge is gone.** Order K charged a young player's draft pedigree down as a pure function
of games played. It peaked at exactly 14 games and then fell away, so a 36-game player kept more of
his unearned entry price than a 17-game player, whatever either of them had done. That is removed.

**In its place the charge reads performance against the bar the player's own entry price implies.**
`pi *= exp(-LAMBDA * A(g) * T(s_P))` below age 24, with `s_P` measured against the S1 age bar plus
the measured pedigree premium `PG(ln v0, class)`.

**Every constant was carried at full precision from ORDER P and none was re-fitted.** The wired
surface reproduces ORDER P's own `op_lib.Premium` to **0.000e+00 at all 242 grid nodes**, the wired
surplus reproduces `op_lib.perf_surplus_P` to **2.8e-14 over 13,859 vantages**, and
`LAMBDA * THETA_R - BETA_sat` is **exactly zero**.

**With the new dial off the board rebuilds `f3101883` BYTE-EXACT.** Falsifier B1 did not fire.

**THE BUILT NUMBERS MATCH THE OFFLINE ESTIMATE ALMOST PERFECTLY.** Every one of the sixteen band
cells in both windows agrees with ORDER P's estimate to within **0.005 percentage points**. The class
mark agrees to four decimal places. The board total is 16 points off on 666,434. **After ORDER K came
in materially off its predictions, that was not the expected outcome and it is stated first.**

**Picks 1-10 in the full-history window reads +8.62%, against Order K's +8.22%.** The top-of-draft
inflation did not appear. The owner's prediction is confirmed on a built board.

**Every late band is better than Order K, in both windows.** Picks 31-40 −10.70% → **−8.88%**; picks
41-64 −6.89% → **−5.03%**; modern 31-40 −14.27% → **−11.73%**; modern 41-64 −25.06% → **−24.88%**.

**Modern picks 1-10 breaches at +18.85% against the +14% rail.** That was predicted before the build.
It is the branch the owner already agreed to rule on. No cap was bolted on and no constant was moved.

**THERE IS A SECOND BREACH THAT WAS NOT IN THE BRIEF AND IT IS NEW TO THIS BOARD.** Three individual
draft classes go over the 1.14 line: cohorts 2011 (**1.1570**), 2012 (**1.1595**) and 2016
(**1.2047**). Order K's worst single class is 1.1363. **ORDER P's own offline files contain the same
1.2047 and `PACKET_P` did not print it.** §7.

**Everything else holds.** Class mark 1.0613 on the registered basis, day-0 entry values bit-identical
89 of 89 against ORDER K's own reference file, 429 mature rows move by exactly zero, determinism x2,
the dial chain, and continuity on all six axes including the two new ones.

**The peaks are not restored**, exactly as ORDER P said they could not be. §8.

---

## 2 · WHAT WAS BUILT

### 2.1 The one line that changed

At `engine/rl_after/_merged_recover.py`, inside `o31_pi`:

```
before:  pi *= max(0, 1 - ETA*((g/GAMMA_D)*exp(1 - g/GAMMA_D)))          ETA 0.50, GAMMA_D 14
after :  pi *= exp( -LAMBDA * A(g) * T(s_P) )        for a row aged under 24 at the year priced
         pi *= the line above                         for a row aged 24 or over
```

```
A(g)  = 1 - exp(-g / G0)                          A(0) = 0 EXACTLY
T(s)  = clip( 1 - THETA_R * (s - s0), 0, TMAX )   non-increasing in s
s_P   = games-weighted mean of ( season avg - BAR_P ) over every season played to that year
BAR_P = o32_gate_bar(that season's bar, his age that season)  +  PG(ln v0, class)
```

A row with no birth year, no day-0 `v0`, or a season the bar cannot read falls back to the old charge
unchanged — the same fallback ORDER P's own offline pricing used, so the two are comparable line by
line rather than nearly.

### 2.2 The constants, and the proof they are ORDER P's

| constant | wired | ORDER P's own file | match |
|---|---:|---|---|
| `G0` | 9.8900000000000077 | `MECH_P.json::G0` | to the last bit |
| `BETA_sat` | 0.11464630061141393 | `MECH_P.json::BETA_sat` | to the last bit |
| `LAMBDA` | 0.17438330365754029 | `STEP4_P.json::LAMBDA` — **solved**, not chosen | to the last bit |
| `THETA_R` | 0.65743851737411818 | `= BETA_sat / LAMBDA`. Not free | to the last bit |
| `s0` | −2.4527208914690739 | `MECH_P.json::s0` | to the last bit |
| `TMAX` | 21.123281548845981 | `= 1 − THETA_R·(s_P5 − s0)`. Not free | to the last bit |
| age gate | 24 | ORDER N / ORDER P | — |

`LAMBDA * THETA_R - BETA_sat = 0.000e+00`. **There is no free parameter and nothing was tuned.**
Proof: `SURFACE_CHECK_P_out.txt`.

### 2.3 The premium surface

Two 121-node grids over `ln(v0)`, one for TALL (KPD/KPF/RUCK) and one for SMALL (MID/SD/SF),
regenerated by `op_surface_emit.py` from ORDER P's own `op_lib.Premium` on ORDER P's own population
(5,041 season rows, 1,575 players, 58,488 games), monotone-guarded, held flat outside support.

| entry price `v0` | SMALL | TALL |
|---:|---:|---:|
| 100 | −7.04 | −5.45 |
| 300 | −1.26 | +2.65 |
| 600 | +3.68 | +6.39 |
| 1,200 | +7.15 | +9.41 |
| 1,700 | +13.95 | +10.81 |
| 2,400 | +17.77 | +12.26 |
| 3,200 | +23.29 | +22.92 |

Support: `v0` 91.2 to 3,444.3 (SMALL), 96.2 to 2,946.9 (TALL). Outside it the premium is held flat.
**Pooled over age.** The age-carrying variant was measured in ORDER P and is worse on every rail; it
is not built and it is not a dial.

### 2.4 The dial

`RL_O37`. It implies the O36 stack (and so O35/O32/O31) and defaults the six ORDER K constants to
ORDER K's ruled values where they are not passed explicitly.

- `RL_O37` unset, ORDER K's line → **`f3101883` byte-exact**.
- `RL_O37=1` with every `RL_O36_*` **unset** → **`374d4e44`, byte-identical to the explicit line.**
- Base stack, everything off → **`1f176444` byte-exact.**

---

## 3 · BUILT AGAINST ESTIMATED. THE COMPARISON THE ORDER ASKED FOR LOUDLY.

**The prereg fixed "material" in advance, before any result: 0.5 percentage points on a band, 0.002
on a class mark, 0.3% on the board total.** Nothing came close to any of those.

### 3.1 The bands — PRIMARY window, cohorts 2005-2023

| band | n | ORDER K | **ORDER P BUILT** | ORDER P estimate | built − estimate |
|---|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 1200 | +4.23% | **+5.33%** | +5.33% | **−0.00** |
| picks 1-20 | 380 | +9.22% | **+9.79%** | +9.79% | **+0.00** |
| picks 21-64 | 820 | −3.67% | **−1.73%** | −1.73% | **−0.00** |
| picks 1-10 | 190 | +8.22% | **+8.62%** | +8.62% | **+0.00** |
| picks 11-20 | 190 | +11.16% | **+12.07%** | +12.07% | **+0.00** |
| picks 21-30 | 190 | +5.26% | **+7.37%** | +7.38% | **−0.00** |
| picks 31-40 | 190 | −10.70% | **−8.88%** | −8.88% | **−0.00** |
| picks 41-64 | 440 | −6.89% | **−5.03%** | −5.03% | **−0.00** |

### 3.2 The bands — MODERN window, cohorts 2019-2023

| band | n | ORDER K | **ORDER P BUILT** | ORDER P estimate | built − estimate |
|---|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 311 | −0.96% | **+1.45%** | +1.45% | **−0.00** |
| picks 1-20 | 100 | +9.58% | **+12.88%** | +12.88% | **+0.00** |
| picks 21-64 | 211 | −17.97% | **−17.01%** | −17.01% | **−0.00** |
| **picks 1-10** | 50 | +13.65% | **+18.85% BUY-RED** | +18.85% | **+0.00** |
| picks 11-20 | 50 | +2.11% | **+1.94%** | +1.94% | **+0.00** |
| picks 21-30 | 50 | −14.26% | **−13.84%** | −13.84% | **−0.00** |
| picks 31-40 | 50 | −14.27% | **−11.73%** | −11.73% | **+0.00** |
| picks 41-64 | 111 | −25.06% | **−24.88%** | −24.88% | **−0.00** |

### 3.3 Everything else

| quantity | ORDER K | **ORDER P BUILT** | ORDER P estimate | difference |
|---|---:|---:|---:|---:|
| board total | 673,097 | **666,434 (−0.99%)** | 666,450 (−0.99%) | **16 points, 0.0024%** |
| rows that move | — | **280 (125 up, 155 down)** | 288 (133 up, 155 down) | 8 rows |
| W2 class mark (drafts 2005-2015) | 1.0513 | **1.0613** | 1.0613 | **−0.0000** |
| cohort-clock mark | 1.0324 | **1.0322** | 1.0322 | **0.0000** |
| veteran churn / net (vs landing) | 947 / −601 | **947 / −601** | 951 / −595 | 4 / 6 points |
| ALLPOOL primary | −4.93% | **−3.60%** | −3.60% | **0.00** |
| SSP primary | +52.71% | **+58.17%** | +58.17% | **0.00** |

**Every peak in the primary window matches its estimate to three decimal places and lands in the same
year.** §8.

**The honest reading.** ORDER P priced this mechanism offline through a linear identity on two built
matrices. The identity has now been tested against a real build and it held to a degree this seat did
not expect. The one place the offline arithmetic showed rounding noise — 89 gameless rows reading
−7 points between them — the built board reads **exactly zero**, which is better than the estimate,
not worse.

---

## 4 · THE OWNER'S LAWS, SCORED ON THE BUILT BOARD

| law | result |
|---|---|
| the year-1 class COHORT must GROW, floor 1.03 on the registered W2 basis (drafts 2005-2015) | **PASS — 1.0613**, +0.0313 over the floor, against ORDER K's 1.0513 |
| strictly under the 1.14 rail | **PASS — 1.0613**, 0.0787 under |
| no pick band above +14% year 0→1 | **ONE BREACH: modern picks 1-10 at +18.85%.** Predicted. §6 |
| no pool arm above +14% | **ONE BREACH: SSP at +58.17%. INHERITED — ORDER K reads +52.71%.** §7.2 |
| picks 31-40 and 41-64 materially improve vs ORDER K | **PASS in the primary window** — +1.82 and +1.86 points. **In the modern window 31-40 improves +2.54 and 41-64 improves only +0.17**, which is not much; it matches the estimate exactly and it is stated rather than rounded up to "improves" |
| picks 1-10 stay near ORDER K's +8.22% | **PASS — +8.62%**, forty basis points above |
| day-0 ENTRY values bit-identical, 89/89 | **PASS.** §5.3 |
| determinism ×2 | **PASS** |
| full dial-chain identities | **PASS** |
| continuity in age, games and pick | **PASS on all six axes.** §9 |
| mature rows untouched by the age bar | **PASS — 429 rows aged 24+ move by EXACTLY ZERO** |
| no row prices above its own uncharged price | **PASS — 0 of 804.** §10 |
| **a line NOT in the brief, and it breaks** | **three individual draft classes go over 1.14.** §7.1 |

**The instrument was validated before any ORDER P number was quoted.** `op_class.py` reproduces ORDER
K's own published marks off ORDER K's own matrix — W2 1.0513 and cohort 1.0324, both to 0.0000.

---

## 5 · THE BUILD-LEVEL PROOFS

### 5.1 The dial chain

| board | command | md5 | required |
|---|---|---|---|
| `candP` | base stack, every ORDER I/P dial off | `1f176444` | the landing candidate. **PASS** |
| `Kref` | ORDER K's ruled line, `RL_O37` UNSET | `f3101883` | **B1: byte-exact. PASS** |
| `P` | the same line + `RL_O37=1` | `374d4e44` | the decision board |
| `Pimp` | `RL_O37=1` alone, every `RL_O36_*` unset | `374d4e44` | **the dial carries the stack. PASS** |
| `P2` | an identical repeat of `P` | `374d4e44` | **B2: determinism. PASS** |
| `Peta0` | the same stack with the charge off (`RL_O36_ETA=0`) | `73bf9617` | the uncharged ceiling |

**`Peta0` came out `73bf9617`, which is the same eta-zero board ORDER P priced against offline.** The
uncharged board totals 702,734.

### 5.2 The wired mechanism is ORDER P's mechanism

`op_surface_check.py` reads the grid and the constants **out of the engine source** and compares them
against ORDER P's own files and a fresh re-fit of `op_lib.Premium`:

- worst node-for-node difference over 242 nodes: **0.000e+00**
- worst difference over 8,002 dense points, support ±1 log unit: **4.97e-14**
- worst surplus difference over **13,859 vantages**: **2.84e-14**, with **0** None/not-None disagreements
- `LAMBDA · THETA_R − BETA_sat`: **exactly 0**
- `A(0)`: **exactly 0**

**B11 and B9 did not fire.**

### 5.3 Day 0

**B3 did not fire, and it was tested the hard way.** The emit's own replication proof was pointed at
**ORDER K's own `DAY0_K.json`**, not at a regenerated reference. Run on the ORDER P engine it printed:

> `ORDER 31-F REPLICATION: 89 of 89 wired entrants on board f3101883 reproduce printed day-0 EXACTLY`
> `(tolerance 0, on the printed integer AND the unrounded derived_v0)`

The words "on board f3101883" are the label stored inside ORDER K's reference file, not the board
being built. **The board being built is `374d4e44`, and it reproduces ORDER K's printed day-0 prices
exactly on all 89 rows.**

**The prereg disclosed that the sitter PRINT reference might have to regenerate, because every ruled
fade change so far has required it. IT DID NOT.** ORDER P is not a fade change: it changes what a
young player is worth *after* he has played, and `A(0) = 0` exactly, so a player who has not played
cannot move. On the board, all **89** rows with zero career games move by **exactly zero points**.

---

## 6 · THE ONE EXPECTED BREACH: MODERN PICKS 1-10

**+18.85% against the +14% rail, on 50 rows.** ORDER K reads +13.65% there — about a third of a point
of room before this order touched anything.

**This was written down in the prereg before the engine was edited, and in the register before this
seat was launched.** It is the branch trigger the owner already agreed to rule on. This seat has not
capped it, has not re-tuned anything to move it, and does not rule on it.

Three facts to read beside it:

1. **The same band in the full-history window reads +8.62%**, forty basis points above ORDER K, and is
   inside the rail. That window carries 190 rows against the modern window's 50.
2. **ORDER P did not lift the top of the draft on purpose.** On the young board cross-section the mean
   charge on picks 1-10 rises from 26.8% (ORDER K) to 33.6% (ORDER P). The modern cell moves because
   the solved LAMBDA is low, not because the tilt favours high picks.
3. **ORDER P's own ladder said the joint requirement is a 0.012-wide gap that nothing sits in**:
   the modern rail needs LAMBDA ≥ 0.596 and the 1.03 class floor allows ≤ 0.584. Nothing in this build
   changes that arithmetic.

---

## 7 · THE BREACHES THAT ARE NOT THE EXPECTED ONE

### 7.1 THREE INDIVIDUAL DRAFT CLASSES GO OVER 1.14, AND THIS IS NEW

The rule the owner reads is the **average** over draft classes 2005-2015, and that average is fine.
But the engine's own O32/O36 calibration was held to a second condition, written into the engine
source: *"max class ≤ 1.139 (the 1.14 no-arb line)"*. ORDER K satisfies it. **This board does not.**

| cohort year | draft class | ORDER K | **ORDER P** | move |
|---:|---:|---:|---:|---:|
| 2011 | 2010 | 1.1359 | **1.1570** | +0.0211 |
| 2012 | 2011 | 1.1363 | **1.1595** | +0.0232 |
| **2016** | **2015** | 1.1060 | **1.2047** | **+0.0987** |

ORDER K's worst single class is **1.1363**. ORDER P's is **1.2047**.

Two of the three were already within half a point of the line and this board pushes them through it.
The 2015 draft class moves much further, and it is the largest single-class move in the order.

**This was measurable offline and was not printed.** ORDER P's own `CLASS_P.json` carries
`PDERIV max 1.2047 at 2016`, and `PACKET_P` does not mention it. This build did not create the number;
it found it. **It is disclosed here and on all three owner pages rather than left to be discovered.**

**This seat is not fixing it and is not trading it against another law.** It is reported.

### 7.2 SSP — INHERITED, AND THIS ORDER MAKES IT WORSE

| arm | landing | ORDER K | **ORDER P** | move vs K |
|---|---:|---:|---:|---:|
| **SSP** | +50.52% | **+52.71%** | **+58.17%** | **+5.46** |

**SSP was over the +14% buy rail before this order existed.** It is reported on its own line and is
never folded into a pass. The mechanism is understood: SSP players enter outside the 1-64 pick curve
at low entry prices, so the bar this order sets for them is low and they clear it easily. Nothing in
this order reaches them, and fixing it is a separate ruling.

**Every other pool arm improves or is flat**, and the whole pool book improves:

| arm | n | landing | ORDER K | **ORDER P** | ORDER P estimate |
|---|---:|---:|---:|---:|---:|
| RD | 623 | −2.21% | −3.39% | **−1.86%** | −1.86% |
| UNR | 49 | −42.06% | −42.91% | **−43.12%** | −43.12% |
| IRE | 47 | +13.51% | +13.34% | **+13.62%** | +13.62% |
| PDA | 43 | −18.33% | −20.70% | **−20.26%** | −20.25% |
| PDN | 33 | −37.81% | −40.32% | **−40.77%** | −40.78% |
| PDS | 21 | −25.47% | −27.70% | **−26.15%** | −26.15% |
| **ALLPOOL** | 1016 | −3.91% | −4.93% | **−3.60%** | −3.60% |

MSD reads `n/a` in both windows and always has: a mid-season draftee debuts in his own draft year, so
the matrix has no year-1 cell for him. Those 55 rows are excluded and counted, never scored zero.
**That is a null reported as a null.**

---

## 8 · THE PEAKS, WHICH ARE NOT RESTORED

The maximum of each band's year-0-to-7 path and the year it falls in. PRIMARY window.

| band | ORDER K | **ORDER P BUILT** | P vs K | ORDER P estimate |
|---|---|---|---:|---|
| ALL picks 1-64 | 1.532 at yr5 | **1.501 at yr5** | **−2.01%** | 1.501 at yr5, −2.01% |
| picks 1-20 | 1.566 at yr5 | **1.527 at yr5** | **−2.47%** | 1.527 at yr5, −2.47% |
| picks 21-64 | 1.510 at yr6 | **1.509 at yr6** | **−0.01%** | 1.509 at yr6, −0.01% |
| picks 1-10 | 1.552 at yr4 | **1.502 at yr4** | **−3.22%** | 1.502 at yr4, −3.22% |
| picks 11-20 | 1.660 at yr5 | **1.620 at yr5** | **−2.43%** | 1.620 at yr5, −2.43% |
| picks 21-30 | 1.686 at yr6 | **1.686 at yr6** | **+0.01%** | 1.686 at yr6, +0.01% |
| picks 31-40 | 1.403 at yr5 | **1.384 at yr5** | **−1.31%** | 1.384 at yr5, −1.31% |
| picks 41-64 | 1.512 at yr6 | **1.513 at yr6** | **+0.07%** | 1.513 at yr6, +0.07% |

MODERN window: ALL 1.376→1.335 (−2.98%), 1-20 1.578→1.548 (−1.90%), 1-10 1.667→1.639 (−1.66%),
31-40 1.539→1.507 (−2.08%), 11-20 / 21-30 / 41-64 unchanged.

**The peaks come in 0.0% to 3.2% below Order K's, at the same peak years. That is exactly what ORDER
P predicted, to three decimal places.** The reason is structural and was stated before the build: the
anchoring identity pins how many points the charge removes from the **year-1** population, not what
happens at year 4 or 5, and `A(g)` never falls, so a row with 30 or 50 games keeps paying where the
blind charge had already let him off. **Restoring the peaks needs a charge that falls back with games
— which is the defect the owner asked to remove.** The two cannot both be had from this shape.

---

## 9 · CONTINUITY — B8, ON SIX AXES

| axis | result |
|---|---|
| **AGE** — the S1 bar, ages 18-30, every position | **PASS.** Rises with age, never above the flat bar, exactly the flat bar from 24. Unchanged by this order. |
| **GAMES (the charge itself)** — swept at 0.01 games from 0 to 400, at seven surplus levels | **PASS.** Largest jump **3.7e-03**. It **rises at 0 of 280,000 steps.** |
| **GAMES — the charge being replaced, same sweep** | it **RISES at 38,600 of 40,000 steps**, every one of them past 14 games. **That is the defect, measured.** |
| **PICK** — the live fade exponent, 0.01-pick resolution | **PASS.** Largest step 5.0e-04 (SMALL), 2.0e-04 (TALL). Unchanged. |
| **SURPLUS (new axis)** — the factor across 100 points of surplus at 0.01 | **PASS.** Largest jump 1.1e-03. A better player is charged more at **0 of 70,000 steps.** |
| **ENTRY PRICE (new axis)** — the premium across 40 to 6,000 at 0.1% of price | **PASS.** Largest jump 5.7e-02. The premium **falls with price at 0 steps**. |
| **rho32** — monotone in games, strictly below 1 | **PASS.** 0 violations over g = 0 to 300. Unchanged. |

### 9.1 The ruled at-bar continuity object, run against BOTH bars, and reported both ways

| object | rows | worst step | falling rows |
|---|---:|---:|---:|
| ORDER K, the blind charge (the base) | 8 | +6.4673 | **0** |
| ORDER P, rows at their **AGE** bar | 4 | +2.4517 | **0** |
| ORDER P, the same rows at their **PEDIGREE** bar | 8 | +3.9477 | **0** |

The object asks whether a row sitting exactly on his bar can see his price FALL as career games step
0, 1, 2 … 20. It does not, on any of the three readings.

**Two disclosures.** The ORDER P age-bar reading covers 4 of the 8 at-bar rows, because the other four
carry no readable `s_P` in the matrix; that is stated rather than counted as a pass. And in principle
this object *could* have shown a fall under ORDER P, because a row at his AGE bar is not at his own bar
if he was expensively drafted — the charge would grow with his games. It did not fire here, and if it
had, that would have been the mechanism working rather than a cliff.

---

## 10 · THE FORBIDDEN-SET BOUND, MEASURED ON A BUILT BOARD

ORDER P argued the pedigree-conditional bar is not the deleted par machinery returning, because par
entered price as `max(0, pole − production)` — strictly non-negative, so a high pick was PAID for
being a high pick — while this object enters a **charge** and `T` is non-increasing in surplus, so
raising an expensive row's bar RAISES his charge.

**The bound is now measured on a real board, not argued.** The uncharged board (`73bf9617`, the same
stack with the charge switched off) totals 702,734.

| board | rows priced ABOVE their own uncharged price |
|---|---:|
| ORDER K | **0 of 804** |
| **ORDER P** | **0 of 804** |

**B10 did not fire.** The ceiling this mechanism can reach is a board the forbidden set is already
absent from. It cannot add value anywhere.

**The forbidden-set WORD is still the owner's to say.** This seat has measured the bound; it has not
ruled.

---

## 11 · WHERE THE MONEY MOVES

**280 of 804 rows move. 125 up, 155 down. Board 673,097 → 666,434, −0.99%.**

| career games | rows | total points | per row |
|---|---:|---:|---:|
| **0** | 89 | **+0** | **+0.0** |
| 1-4 | 48 | −918 | −19.1 |
| 5-9 | 51 | −865 | −17.0 |
| 10-15 | 48 | **+860** | **+17.9** |
| 16-29 | 80 | −1,570 | −19.6 |
| 30-59 | 100 | −3,043 | −30.4 |
| 60+ | 388 | −1,127 | −2.9 |

| age in 2026 | rows | total points |
|---|---:|---:|
| 20 and under | 158 | −885 |
| 21-23 | 217 | −5,778 |
| **24 and over** | **429** | **+0** |

**The 24-and-over line is exactly zero. Not "one point across 429 rows" — zero.** The age gate holds
absolutely against ORDER K.

**The veteran caps, two readings, because ORDER P's published estimate was taken against the LANDING
CANDIDATE and reporting only one would mislead:**

| comparison | rows moving | churn | rail | net | rail | verdict |
|---|---:|---:|---:|---:|---:|---|
| ORDER P vs ORDER K | **0** | **0** | 1,010 | **+0** | ±673 | inside both |
| ORDER P vs the landing candidate | 124 | **947** | 1,010 | **−601** | ±673 | inside both |
| ORDER K vs the landing candidate | 124 | 947 | 1,010 | −601 | ±673 | inside both |

**Every point of the veteran movement is ORDER K's own. This order adds none of it.** The published
estimate was 951 / −595 on the landing-candidate basis; the built board reads 947 / −601, which is
ORDER K's number exactly.

**The 10-15 games band is the one that goes UP** (+860 points over 48 rows). Those are young players
who have shown enough to clear their own bar, and the old charge was near its peak on them.

---

## 12 · THE CHARGE, AND WHERE IT FALLS

Percentage of the pedigree leg removed, at age 19.

| games | ORDER K, blind | s_P = −25 | s_P = −10 | s_P = 0 | s_P = +10 |
|---:|---:|---:|---:|---:|---:|
| 2 | 16.8% | 39.7% | 17.3% | 0.0% | 0.0% |
| 5 | 34.0% | 66.5% | 33.8% | 0.0% | 0.0% |
| 10 | 47.5% | 82.7% | 48.4% | 0.0% | 0.0% |
| 14 | 50.0% | 87.6% | 54.5% | 0.0% | 0.0% |
| **17** | **49.0%** | 89.6% | 57.4% | 0.0% | 0.0% |
| 30 | 34.2% | 92.8% | 62.8% | 0.0% | 0.0% |
| **36** | **26.7%** | 93.2% | 63.7% | 0.0% | 0.0% |
| 50 | 13.6% | 93.6% | 64.4% | 0.0% | 0.0% |

**Read the 17-game row against the 36-game row in the ORDER K column: 49.0% falls to 26.7%.** The
ORDER P column never falls anywhere.

**The zero point.** `T` hits zero at `s_P = −0.93`. A young player producing within about a point a
game of what a player at his price normally produces, at his age, **pays nothing at all**.

### 12.1 Where the charge lands by pick band, on the 2026 board — AND A CAVEAT

| pick band | rows | charge ORDER K | **charge ORDER P** | median s vs AGE bar | median s vs PEDIGREE bar |
|---|---:|---:|---:|---:|---:|
| 1-10 | 84 | 26.8% | **33.6%** | +4.57 | −4.42 |
| 11-20 | 57 | 27.9% | **44.1%** | −5.02 | −11.83 |
| 21-40 | 68 | 29.6% | **40.2%** | −7.33 | −10.44 |
| 41-64 and pool | 80 | 34.0% | **34.7%** | −7.91 | −7.18 |

**This is NOT the same object ORDER P published, and the difference must not be glossed.** ORDER P's
table (39.7 / 35.2 / 33.0 / 27.6, falling monotonically with pick) was measured over **4,143 young
vantage rows across the whole history**. This table is the **289 young rows on the 2026 board**. On
this cross-section the charge is **not** monotone in pick: picks 11-20 carry the heaviest charge and
picks 1-10 and 41-64 are within a point of each other.

**What survives on both objects** is the thing the owner's insight was about: the median surplus goes
from strongly ordered by pick against the age bar (+4.57 down to −7.91) to nearly flat against the
pedigree bar (−4.42 to −7.18). **The pick axis is largely out of the surplus.** The charge level on
any one 2026 band also depends on how many games those particular players happen to have played, and
the 2026 top ten are unusually low-games.

---

## 13 · THE NAMED ROWS — CONSEQUENCES, NEVER TARGETS

**Not one constant in this build was chosen with any of these rows in view, and no row's value is an
acceptance criterion. That is a standing prohibition in this project after a real error.** The prereg
wrote a DIRECTION for each row before the engine was touched. The direction is scored; the value is
not.

| row | age | pick | g | v0 | premium | s vs age | s vs ped | chg K | chg P | ORDER K | **ORDER P** | prereg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Harry Dean | 19 | 3 | 17 | 2438 | +12.95 | +14.86 | **+1.91** | 49.0% | **0.0%** | 2403 | **3069** | up ✓ |
| Cooper Duff-Tytler | 19 | 4 | 13 | 1858 | +10.81 | +7.06 | **−3.75** | 49.9% | **21.1%** | 1505 | **1824** | up ✓ |
| Xavier Taylor | 19 | 11 | 2 | 1355 | +9.23 | −13.22 | **−22.45** | 16.8% | **36.3%** | 1162 | **950** | down ✓ |
| Daniel Annable | 19 | 6 | 2 | 1661 | +13.54 | −19.02 | **−32.56** | 16.8% | **48.5%** | 1537 | **1115** | down ✓ |
| Dylan Patterson | 19 | 5 | 5 | 1679 | +13.73 | −19.62 | **−33.35** | 34.0% | **76.8%** | 1440 | **955** | down ✓ |
| Isaac Kako | 20 | 13 | 36 | 938 | +6.53 | +0.84 | **−5.70** | 26.7% | **41.3%** | 832 | **784** | down ✓ |
| Josh Smillie | 20 | 7 | 0 | 1660 | — | — | — | 0.0% | 0.0% | 772 | **772** | flat ✓ |
| Milan Murdock | 26 | pool | 17 | 131 | −7.04 | +2.17 | +9.21 | 49.0% | 49.0% | 156 | **156** | flat ✓ |
| **Zeke Uwland** | 19 | 2 | 17 | 2583 | +19.22 | **−1.64** | **−20.86** | **49.0%** | **84.7%** | 1949 | **1486** | down ✓ |
| **Cooper Harvey** | 22 | 56 | 17 | 265 | −1.26 | **−1.80** | **−0.54** | **49.0%** | **0.0%** | 331 | **373** | up ✓ |

**10 of 10 prereg directions correct.**

**The matched pair, on the built board.** Uwland and Harvey have both played 17 games and both sit
about 1.7 points a game below what is normal for their age in their position. **Under ORDER K they
paid the identical 49.0%, to the last decimal, because the charge read only games.** Uwland was pick 2
and cost 2,583; a player at that price produces 19.2 points a game clear of the age bar, so against
what is priced into him he is 20.9 short and he pays 84.7%. Harvey was pick 56 and cost 265; a player
at that price produces 1.3 BELOW the age bar, so he is half a point short and he pays nothing.
**Same production for their age, same games, opposite verdicts.**

**Isaac Kako is the other row worth reading.** He is at his age bar with 36 games — the most evidence
here. Under ORDER K he paid 26.7%, LESS than Dean's 49.0%, because 36 games sits on the far side of
the blind bump. Under ORDER P he pays 41.3%. That inversion is the defect, removed.

The ten largest moves in each direction are in `LEDGER_P_out.txt`. The largest rise is Jagga Smith
(pick 3, 20 games, +11.82 against his pedigree bar) at +711; the largest fall is Finn O'Sullivan
(pick 2, 39 games, −15.32 against his pedigree bar) at −652.

---

## 14 · THE FALSIFIER SCORECARD

| # | falsifier | fired? |
|---|---|---|
| **B1** | the dial-off board is not `f3101883` byte-exact | **no** — `f3101883a60b0a7b8cb50f9d8a5abfff` |
| **B2** | determinism ×2 fails | **no** — `374d4e44` twice |
| **B3** | any of the 89 wired day-0 ENTRY values moves | **no** — 89 of 89 exact against ORDER K's OWN reference; all 89 zero-games rows move 0 points |
| **B4** | the veteran pool breaches churn 1,010 or net ±673 | **no** — 0/+0 against ORDER K; 947/−601 against the landing candidate, both inside |
| **B5** | the W2 class mark falls below 1.03 or reaches 1.14 | **no** — 1.0613 |
| **B6** | a pick band or pool arm above +14% other than SSP and modern picks 1-10 | **no** — those two only, both disclosed on their own lines |
| **B7** | picks 31-40 or 41-64 do not materially improve | **no** — +1.82 and +1.86 primary, +2.54 and +0.17 modern |
| **B8** | a cliff in age, games or pick | **no** — six axes, largest jump 5.7e-02 on the price axis |
| **B9** | `LAMBDA · THETA_R != BETA_sat` | **no** — residual exactly 0 |
| **B10** | a row prices above its own uncharged price | **no** — 0 of 804 |
| **B11** | the baked surface does not reproduce `op_lib.Premium` | **no** — 0.000e+00 at every node |
| **B12** | the S1 bar changes at or after age 24 | **no** — exactly the flat bar from 24, every position |
| **B13** | a built number differs MATERIALLY from the estimate | **no, and by a wide margin** — worst band difference 0.005pp against a 0.5pp threshold |

**Prereg deviations, declared.**

1. **The prereg disclosed the sitter PRINT reference might regenerate. It did not, and the emit was
   pointed at ORDER K's own file specifically so that would be a test rather than an assumption.**
2. The prereg disclosed that the engine's games axis is `pv_games` (with the MSD games-of-12 scaling)
   while ORDER P's offline surplus used raw career games. That difference is live and is measurable
   only on MSD rows in their own entry season; the band agreement to 0.005pp bounds its effect.
3. The engine's `v0` is rounded to one decimal to match the matrix emitter's own convention, as
   disclosed. The season `avg` is NOT rounded in the engine where the offline files carried it to two
   decimals; that difference is also inside the same bound.
4. Two objects were ADDED that the prereg did not promise: the uncharged board `Peta0`, built so that
   B10 could be measured on a real board rather than argued, and the two new continuity axes.
5. **§7.1, the three individual draft classes over 1.14, is not a prereg falsifier and not in the
   brief's acceptance list. It is reported because it is a real breach of a line the engine's own
   earlier calibrations were held to, and because ORDER P's own files contain the number and its
   packet did not print it.**

---

## 15 · WHAT IS OWED, AND WHAT THIS SEAT COULD NOT DO

- **Nothing here rules on the modern picks 1-10 cell.** §6 gives the numbers under both readings. The
  register already records the branch: if that cell is binding, the owner rules on replacing the
  year-1-only rail with a path-wide test.
- **Nothing here rules on §7.1.** Three draft classes over 1.14 is a new breach and the owner has not
  been asked about it before. It needs a ruling.
- **The forbidden-set WORD is still owed.** The bound is measured; the word is the owner's.
- **The peaks are not restored and cannot be inside this shape family.** §8.
- **The pedigree premium is a lower bound**, because it is estimated on players who play. The bar is
  if anything less demanding of expensive players than the truth. Not repaired here, as ORDER P said.
- **The TALL premium is thin at both ends** (effective sample 19 cheap, 47 dear) and held flat outside
  support.
- **There is no hold-out.** The premium is estimated on the same board's `v0` that the charge is
  applied to. A stronger test would fit it on pre-2015 entrants and price the post-2015 ones.
- **The pick-band charge cross-section on the 2026 board is not monotone in pick** (§12.1), unlike the
  historical vantage measurement ORDER P published. Both are printed.
- **The load-time banner counters read zero** in the standalone-import context this seat used to
  capture them (`0 rows carry a stall run`, `0 carry relief`, and my own `0 active rows`). That is a
  pre-existing property of every order's banner in that context, not a property of this mechanism —
  the real counts are on the board and in the ledger. Disclosed rather than quietly corrected.
- **The veteran board (RL_O33) is still parked**, so key-position talls aged 28-30 remain about 30%
  over-priced. Nothing in this order touches them.

---

## 16 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_P_BUILD.md` | the prereg, pushed at `8a75862` before the first engine edit |
| `op_surface_emit.py` · `PREMIUM_SURFACE.json` · `O37_PG_GRID.py.txt` | the premium surface regenerated from ORDER P's own `op_lib.Premium` and emitted as the engine literal |
| `op_surface_check.py` · `SURFACE_CHECK_P.json` · `SURFACE_CHECK_P_out.txt` | B11/B9 — the wired mechanism proved to be ORDER P's, node by node and vantage by vantage |
| `bbP.sh` · `build_allP.sh` · `BUILD_P_out.txt` | the board suite: the base stack, the dial-off byte-exact test, the decision board, the dial-implies test, the determinism repeat |
| `run_emit_P.sh` · `EMIT_PBUILT_out.txt` | the walk-forward emit, with the day-0 proof pointed at ORDER K's own reference |
| `op_gates.py` · `GATES_P.json` · `GATES_P_out.txt` | the owner's laws on the built board |
| `op_continuity.py` · `CONTINUITY_P.json` · `CONTINUITY_P_out.txt` · `ENGINE_BANNER_P.txt` | B8 on six axes, and the engine's own load banner |
| `op_bands_build.py` · `BANDS_BUILD.json` · `BANDS_BUILD_out.txt` | the ND band tables, BOTH windows, with ORDER P's offline estimate kept beside the build |
| `bb_noarbP.sh` · `op_tables.py` · `STANDING_TABLES_P.json` · `STANDING_TABLES_P_out.txt` | the standing suite, the pool arms in both windows, the vantage matrix, the entry-year control |
| `op_class.py` · `CLASS_P.json` · `CLASS_P_out.txt` | the class mark on BOTH bases, with the instrument validated against ORDER K's published numbers |
| `op_ledger.py` · `LEDGER_P_out.txt` · `docs/ledgers/ORDER_P_MOVERS.json` | the movers ledger, five board columns plus the mechanism legs |
| `op_pages.py` · `ORDER_P_PLAYERS.html` · `ORDER_P_YEAR1.html` · `ORDER_P_NOARB.html` | the three owner documents |
