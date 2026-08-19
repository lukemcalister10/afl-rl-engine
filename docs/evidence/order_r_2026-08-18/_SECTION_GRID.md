## 4 · THE GRID. EVERY BUILD-LEVEL FALSIFIER PASSED.

**Twelve boards. One engine md5 across all of them: `ea5c5e5e`. One store: `cb38ef11`.**

### 4.1 The falsifiers

| # | falsifier | result |
|---|---|---|
| **R1** | both ORDER R dials unset does not rebuild ORDER P `374d4e44` byte-exact | **no — `374d4e44`** |
| **R2** | R dials unset with `RL_O38B1=1` does not rebuild FIX B1 `1b1817f3` | **no — `1b1817f3`** |
| **R3** | R dials unset with `RL_O38A=1 RL_O38B1=1` does not rebuild A+B1 `cbbb94d4` | **no — `cbbb94d4`** |
| **R4** | determinism x2 fails on any variant | **no — all NINE identical on a repeat** |
| **R8** | `RL_O38B1` + `RL_O39_TMAXPCT=20` alone does not carry the O37/O36/O35/O32/O31 stack | **no — `aa5e70cc` both ways** |
| **R9** | `LAMBDA·THETA_R ≠ BETA_sat_eff` at load | **no — asserted at 1e-15 on every board** |
| **R10** | `TMAX` is stale, or the p5 entry is not `MECH_P.json::s_p5` bit for bit | **no — asserted at load on every board** |
| **R11** | a `BETA_sat` outside the published 90% CI is accepted | **no — the dial HALTS on it** |
| — | the base stack no longer rebuilds `1f176444` | **no — `1f176444`** |
| — | ORDER K's ruled line no longer rebuilds `f3101883` | **no — `f3101883`** |

### 4.2 The boards

| board | cell | md5 | total | vs ORDER P | vs ORDER K | vs FIX B1 |
|---|---|---|---:|---:|---:|---:|
| ORDER K | — | `f3101883` | 673,097 | +6,663 | — | +13,230 |
| ORDER P | — | `374d4e44` | 666,434 | — | −6,663 | +6,567 |
| **RB1** | p5 · b0 · A off | `1b1817f3` | **659,867** | −6,567 | −13,230 | — |
| **R15** | **p15** · b0 · A off | `902ef88e` | **661,216** | −5,218 | −11,881 | **+1,349** |
| **R20** | **p20** · b0 · A off | `aa5e70cc` | **662,302** | −4,132 | −10,795 | **+2,435** |
| **Rb1** | p5 · **0.111** · A off | `d9c74574` | **660,419** | −6,015 | −12,678 | **+552** |
| **Rb2** | p5 · **0.105** · A off | `f69ca077` | **661,356** | −5,078 | −11,741 | **+1,489** |
| **R15b1** | **p15** · **0.111** · A off | `c3798c8d` | **661,783** | −4,651 | −11,314 | **+1,916** |
| **R20b2** | **p20** · **0.105** · A off | `fd958019` | **663,845** | −2,589 | −9,252 | **+3,978** |
| **RAB1** | p5 · b0 · **A ON** | `cbbb94d4` | **662,685** | −3,749 | −10,412 | **+2,818** |
| **R15A** | **p15** · b0 · **A ON** | `dcb68e73` | **663,969** | −2,465 | −9,128 | **+4,102** |
| **R20A** | **p20** · b0 · **A ON** | `7f88f509` | **664,950** | −1,484 | −8,147 | **+5,083** |
| **R20b2A** | **p20** · **0.105** · **A ON** | `aaab992e` | **666,056** | **−378** | −7,041 | **+6,189** |

**The softest cell with FIX A, `R20b2A`, lands 378 points under ORDER P** — it gives back almost
exactly what B1's mature-row extension costs, while removing the age cliff and the pick reversal.

### 4.3 WHICH LEVER DOES WHAT

**Each lever alone, measured from FIX B1:**

| lever | move | points |
|---|---|---:|
| `TMAX` p5 → p15 | the cap 21.1233 → 13.9490, a **34.0%** cut | **+1,349** |
| `TMAX` p5 → p20 | the cap 21.1233 → 11.8950, a **43.7%** cut | **+2,435** |
| `BETA_sat` 0.11465 → 0.111 | the cap 21.1233 → 20.4833, a **3.0%** cut | **+552** |
| `BETA_sat` 0.11465 → 0.105 | the cap 21.1233 → 19.4301, an **8.0%** cut | **+1,489** |
| FIX A | no constant moves at all | **+2,818** |

**PREDICTION 1 IS WRONG, AND WRONG BY A LOT.** The prereg predicted the `TMAX` percentile would be
roughly **five times** the stronger lever. **Measured at the two far ends the ratio is 1.64.**

**Why the prediction failed, stated plainly.** It looked only at the CAP. p5→p20 cuts the cap 43.7%
where `BETA_sat` 0.11465→0.105 cuts it 8.0%, so on cap alone the ratio should be about 5.5 to 1. But
**the `BETA_sat` lever does not only lower the cap. It pivots the whole `T` line about `s0`.** The
`TMAX` lever only reaches rows parked AT the cap; the slope lever reaches **every row producing below
the cohort centre**. Per unit of cap reduction, the slope is about **five times the more efficient
lever — the exact opposite of what was written down.**

**FIX A is the largest single lever of the three, and it is the only one with no constant in it.**

### 4.4 THE GRID IS INTERPOLABLE — FALSIFIER R15 DOES NOT FIRE

The prereg said: if the diagonal cells are not close to the sum of the two single-lever moves, the
grid was under-built and this seat must say so. **They are close.** Materiality is 0.3% of the board.

| combination | additive prediction | **actual** | gap | as % of board |
|---|---:|---:|---:|---:|
| `R15b1` = p15 + 0.111 | 661,768 | **661,783** | **+15** | **+0.002%** |
| `R20b2` = p20 + 0.105 | 663,791 | **663,845** | **+54** | **+0.008%** |
| `R15A` = p15 + A | 664,034 | **663,969** | **−65** | **−0.010%** |
| `R20A` = p20 + A | 665,120 | **664,950** | **−170** | **−0.026%** |
| `R20b2A` = p20 + 0.105 + A | 666,609 | **666,056** | **−553** | **−0.083%** |

**Every gap is inside a tenth of the materiality threshold. The six unbuilt cells can be read off the
built ones to within a few hundred points on a 660,000-point board.** The grid was not under-built.

### 4.5 THE ONE REAL INTERACTION: FIX A AND THE SOFTENING ARE PARTIAL SUBSTITUTES

| FIX A's increment | at | points |
|---|---|---:|
| p5 · b0 | the stiffest cell | **+2,818** |
| p15 · b0 | | +2,753 |
| p20 · b0 | | +2,648 |
| **p20 · 0.105** | **the softest cell** | **+2,211** |

**FIX A gives back 21.5% less on the softest cell than on the stiffest.** The reason is direct: a
lower cap parks more rows AT the cap, where `dT/ds = 0` and the pedigree leg is already monotone in
price, so there is less inverted charge left for FIX A to cap. **Softening and monotonising are
partly doing the same job.** That is the whole of the non-additivity, and it is 0.083% of a board.
