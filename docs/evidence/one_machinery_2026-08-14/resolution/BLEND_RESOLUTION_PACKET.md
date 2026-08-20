# THE BLEND RESOLUTION PACKET — ONE SURFACE, FOUR ANSWERS, ONE OWNER WORD

**ORDER 30B-R · resolution seat · `land/order-29` · 2026-08-15 · parent tip `7a1c6ee` (preview board
`6a392bca7ad0dee04a6b4f037c758f65`).**

> # NOTHING WIRES UNTIL THE OWNER RULES.
> No engine file was edited. No board was built. No dial was added. `git diff 7a1c6ee..HEAD` touches
> `docs/evidence/one_machinery_2026-08-14/resolution/` **and nothing else**. Every price in §6 is
> **DERIVED, NOT BUILT** — arithmetic on committed legs. The preview is still **pre-numéraire** and
> Step 3's forbidden-set boundary word (STOP §5 Q1–Q4) is still **OPEN**.

**Prereg** `PREREG_30BR.md`, filed and pushed (`e3a1168`) before the first resolution quantity existed.
**Harnesses** `o30br_reading.py` · `o30br_clock.py` · `o30br_join.py` · `o30br_resolved.py`.
**Raw readings** `READING{.json,_out.txt}` · `CLOCK{.json,_out.txt}` · `JOIN{.json,_out.txt}` ·
`RESOLVED_ROWS{.json,_out.txt}`.

---

## 0 · THE FOUR ANSWERS IN ONE SCREEN

| | question | **answer** | status |
|---|---|---|---|
| **T1** | which reading of "the pedigree share"? | **NEITHER of the two offered.** σ was *constructed* as a **value share**, so the wired **weight** form is definitionally wrong — but the fitted equation is **additive with production at unit weight**, `price = P + β(g)·v0`, and **β, not σ, is what the harness estimated.** | **RESOLVED BY DEFINITION** |
| **T2** | recency-weighted clock or raw games? | **RAW GAMES.** The recency clock **lost its own preregistered held-out criterion** (OOF RMSE 722.87 vs 715.15, −1.08%). It wins where evidence is thin and loses badly where careers are long, because `u` **saturates at 26.67** and cannot separate a 71-game player from a 295-game one. | **MEASURED — the candidate fix FAILS as a global clock** |
| **T3** | does the join close the first-game cliff? | **YES.** `josh-smillie` 0→1 goes from **+254.8% to +37.1%**, and the curve becomes **monotone 0→16** in all four rows where the preview was non-monotone in three. **But the cliff is not deleted — it is relocated into the 11–15 bridge, where the two measured curves conflict by +35% to +71%.** | **MEASURED — conflict shown, not averaged** |
| **T4** | v0 or `entry_anchor`? | **THE SEAT RECOMMENDS THE STEP-1 `v0`** and states what is lost. The object is worth far less than the preview implied: **+0.62 pp** of whole-book pedigree share, not the ≥3 pp the seat predicted. | **FRAMED — the owner's word, not taken** |

**Prereg: 8 HELD · 6 BREACHED · 1 NOT COMPUTABLE.** Every breach is owned by number in §8.

---

## 1 · T1 — THE READING, RESOLVED BY DEFINITION

### 1.1 How σ was actually constructed

`o30bm_measure.py::band_fit`, line 531 — the one line the whole question turns on:

```python
sig = b[i] * mv0 / mR if mR > 0 else None      #  sigma := beta_v0 * mean(v0) / mean(R)
```

The fitted equation, within games band `b`:

```
R_i  =  c + γ'Z_i  +  β_b · v0_i  +  ε_i
        Z = [pos dummies, age, age², o, o², cur, cur3, games_at_Y, log1p(g)]
```

Take band means, and write `Π̄ ≡ c + γ'Z̄` for the production block's mean contribution:

```
R̄        =  Π̄  +  β_b · v0̄
σ_b       ≡  β_b · v0̄ / R̄          =   (pedigree contribution) / (TOTAL)
1 − σ_b   =  Π̄ / R̄                 =   (production contribution) / (TOTAL)
```

*(Identity checked in the harness to 1e-12 in all five bands.)*

**σ is a ratio of contributions to the LEVEL OF THE OUTCOME. It is a VALUE share by construction. It was
never fitted as, and is not, a mixing weight.** That settles the brief's ambiguity definitionally, and it
settles it **against** what the preview wired.

### 1.2 The measured bands, and the one number that breaks the weight reading

| band | n | `β_v0` | mean `v0` | mean `R` | **`v0̄/R̄`** | σ |
|---|---:|---:|---:|---:|---:|---:|
| 0–5 | 382 | 0.29683 | 600.2 | 254.1 | **2.362** | 0.7011 |
| 6–15 | 591 | 0.36226 | 730.4 | 398.4 | **1.833** | 0.6641 |
| 16–35 | 834 | 0.22330 | 847.4 | 571.2 | **1.483** | 0.3313 |
| 36–70 | 887 | 0.15315 | 920.5 | 857.0 | **1.074** | 0.1645 |
| 71+ | 1339 | 0.02007 | 1123.8 | 1018.2 | **1.104** | 0.0221 |

`v0̄/R̄ > 1` **in every band.** The weight form's implied value share is `σV/[(1−σ)P + σV]`, which equals
σ **if and only if `V` equals the price**. It never does.

### 1.3 The three wirings, and why the third is the faithful one

| | form | implied value share | does it reproduce the measurement? |
|---|---|---|---|
| **W** | `price = (1−σ)·P + σ·V` — **wired in the preview** | `σV/[(1−σ)P+σV]` | **NO.** Requires `V = price`. **And it multiplies the production block by `(1−σ)`, which the regression NEVER does** — γ is estimated free, and the production contribution at the band mean is `(1−σ)R̄`, not `(1−σ)P̄`. At g = 1, `(1−σ) = 0.0782`: a **92% deletion of the production leg** that no fitted coefficient licenses. |
| **V** | `1/price = (1−σ)/P + σ/V` — harmonic, not built | `σ` **exactly** | **PARTLY.** It reproduces the band-mean identity `β·v0̄ = σ·R̄` exactly. But it is *harmonic* in `(P, V)` while the fit is **linear in `v0`**, so it is not the fitted form either. |
| **A** | `price = P + β(g)·V` — **the regression itself** | `βV/(P+βV)` | **YES.** This *is* the fitted equation. `mean(P + βV) = Π̄ + βv0̄ = R̄`, exact by construction. No `V = price` assumption, no production shrink. **β is what `band_fit` estimated; σ is derived from β, not the other way round.** |

### 1.4 THE VERDICT, STATED PLAINLY

> **The weight reading is not a faithful reading of the measurement, and the value reading is not the
> only alternative. The measurement's own form is ADDITIVE with the production leg at unit weight.
> `β(g)` is the wireable object. σ is a reporting statistic about it.**
>
> **The single mechanism that follows from this — the `(1−σ)` production shrink — is, on the seat's
> reading, the common cause of BOTH of the preview's headline problems**: the first-game cliff (finding 1)
> and "the blend takes more out than it puts back past 5 games" (finding 2). Neither is a measurement
> failure. Both are artefacts of a wiring the measurement did not license.

### 1.5 What the resolution costs, on the four rows T1 names

| row | g | σ | prod `P` | `v0` | β(g) | **W price** | **V price** | **A price** | s_W | s_V | s_A |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`isaac-kako`** | 36 | 0.2391 | 744.3 | 759.8 | 0.1869 | **748.0** | **747.9** | **886.3** | 0.2428 | 0.2391 | 0.1602 |
| `willem-duursma` | 19 | 0.4239 | 4198.2 | 3879.3 | 0.2622 | **4063.0** | **4056.8** | **5215.2** | 0.4047 | 0.4239 | 0.1950 |
| `dyson-sharp` | 13 | 0.5307 | 3247.1 | 1551.0 | 0.3224 | **2347.0** | **2054.7** | **3747.2** | 0.3507 | 0.5307 | 0.1335 |
| `jacob-farrow` | 18 | 0.4396 | 2720.0 | 1284.5 | 0.2700 | **2089.0** | **1824.0** | **3066.9** | 0.2703 | 0.4396 | 0.1131 |

`s_*` is each wiring's **implied value share**. `s_V ≡ σ` by construction; read `s_W` against it.

**On the whole blended book (715 rows):**

| wiring | total | pedigree points | book value share | median row share |
|---|---:|---:|---:|---:|
| **W** (preview as built) | **662,631** | 88,942 | **0.1342** | 0.1688 |
| **V** (harmonic) | 595,059 | 86,990 | **0.1462** | 0.0875 |
| **A** (additive) | **738,221** | 53,989 | **0.0731** | 0.1164 |

*(Control: W reproduces the committed preview blended-row total 662,631 exactly.)*

**Two consequences the owner should see before ruling.**

1. **`kako` prints 886 under the additive form, against 748 under the weight form.** The brief's band was
   **900–1000** and P7 breached **LOW** at 748. **886 is a 33-point miss on a band the preview missed by
   152.** The seat filed **R4 predicting [880, 960] before building** — that prediction was made from the
   algebra, not fitted to the answer.
2. **The additive form RAISES the book by 11.4%** (738,221 vs 662,631) and **cuts the pedigree share by
   half** (0.0731 vs 0.1342). It is not a small re-labelling. The pedigree leg becomes a *smaller*
   additive top-up on an *undamaged* production leg, rather than a large weight on a shrunken one.

### 1.6 The disclosure this verdict carries

**The additive form transfers `β` across a scale boundary, and the seat will not pretend otherwise.**
`β` is measured in units of *remaining 6-season discounted delivered value* per unit of `v0`. Wiring
`P + β·v0` on the board assumes the engine's production leg is on that same delivered-value scale. The
preview asserts it is (the numéraire `s` is inside both legs), and 30B-M's `mean_R` (254–1018) sits in the
same order as board production legs — **but this is an asserted commensurability, not a proven one, and it
is the one assumption the additive verdict rests on.** The weight form does not need it (weights are
scale-free); that is the only respect in which the weight form is the safer object.

---

## 2 · T2 — THE CLOCK, AND THE OWNER'S KAKO YEAR-3 SCENARIO

### 2.1 The re-cut, both clocks, same states, same target

`u = Σ_s games_s × 0.25^(Y − year_s)`, d = 0.25 the **engine's own ruled constant** — not fitted here.
`u` band edges set by the **raw bands' own population fractions**, so no edge was chosen after a reading.

**Control: the rebuilt panel reproduces 30B-M exactly — 4,033 states, 767 players, and every raw-clock
band fit byte-identical (`β` 0.29683 / 0.36226 / 0.22330 / 0.15315 / 0.02007).**

| clock | band | n | clusters | `β_v0` | t | σ | σ 90% CI | median clock |
|---|---|---:|---:|---:|---:|---:|---|---:|
| **raw g** | 0–5 | 382 | 332 | 0.29683 | 3.76 | 70.1% | 42.9 … 99.6% | 3.0 |
| | 6–15 | 591 | 467 | 0.36226 | 5.95 | 66.4% | 47.7 … 83.0% | 10.0 |
| | 16–35 | 834 | 571 | 0.22330 | 4.25 | 33.1% | 20.8 … 45.6% | 23.0 |
| | 36–70 | 887 | 436 | 0.15315 | 2.39 | 16.5% | 5.9 … 28.0% | 50.0 |
| | 71+ | 1339 | 297 | 0.02007 | 0.49 | 2.2% | −4.6 … 10.5% | 117.0 |
| **recency u** | U1 | 382 | 305 | 0.16666 | 2.91 | 49.6% | 26.3 … 84.2% | 2.00 |
| | U2 | 592 | 399 | 0.13837 | 3.33 | 42.6% | 21.8 … 64.9% | 6.00 |
| | U3 | 836 | 462 | 0.24420 | 4.96 | 47.2% | 33.0 … 63.0% | 11.72 |
| | U4 | 896 | 427 | 0.07525 | 1.55 | 10.3% | 0.1 … 22.3% | 19.81 |
| | U5 | 1327 | 343 | 0.08085 | 1.52 | 6.9% | −0.4 … 14.1% | 27.30 |

**The recency curve is NON-MONOTONE** (49.6 → 42.6 → **47.2** → 10.3 → 6.9). The raw curve is monotone
after its known shallow blip. Refitting the **ruled family** `exp(−(x/τ)^β)` to each:

| clock | τ | β | n-weighted SSE |
|---|---:|---:|---:|
| raw g | 22.50 | 0.76 | **89,564** |
| recency u | 8.00 | 0.59 | **472,092** |

**The recency clock does not admit the ruled functional form.** Its SSE is **5.3×** the raw clock's.

### 2.2 THE PREREGISTERED HELD-OUT CRITERION — AND ITS VERDICT

5-fold cluster CV, folds by `md5(key) mod 5`, pooled out-of-fold RMSE. **Lower wins. Fixed in advance.**

| clock | **OOF RMSE** | OOF MAE | OOF R² |
|---|---:|---:|---:|
| **RAW g** | **715.152** | 485.776 | **0.53271** |
| RECENCY u | 722.868 | 491.370 | 0.52257 |

**`u` is 1.08% WORSE. RAW GAMES WINS THE CRITERION.** Paired cluster bootstrap (1,000 draws) on
`RMSE(g) − RMSE(u)`: median **−7.52**, 90% interval **[−16.44, +1.78]**, and only **9.7%** of draws favour
`u`. The interval brushes zero, so the loss is **consistent** but **not decisive** — stated as such.

**Where each clock wins, which is the useful part:**

| cg class | n | RMSE g | RMSE u | u better? |
|---|---:|---:|---:|---|
| 0–5 | 382 | 494.481 | **481.135** | **YES** |
| 6–15 | 591 | **585.790** | 586.659 | no |
| 16–35 | 834 | 724.883 | **723.658** | **YES** |
| 36–70 | 887 | **793.814** | 810.751 | no |
| 71+ | 1339 | **757.970** | 770.912 | no |

**THE MECHANISM, NAMED.** With d = 0.25 a full-season player converges to `20/(1−0.25) = 26.67`. Raw games
span **1 … 295** (295×); `u` spans **1.00 … 33.69** (33.7×). **The entire 71+ band (n = 1,339, raw games 71
to 295) is compressed into `u` 2.89 … 33.69.** The recency clock throws away exactly the durability
information the deep book is priced on. That is why it loses, and it is a property of d = 0.25, not of the
idea.

**POST-HOC, NOT PREREGISTERED, NOT ELIGIBLE TO WIN** — the band table points at a hybrid (u in the thin
bands, g in the deep ones), so the seat scored it rather than let it be discovered later: OOF RMSE
**715.355**, i.e. **−0.03% against raw g**, bootstrap median −0.229, 90% [−0.748, +0.325], **25.3%** of
draws favouring it. **A dead heat. The hybrid does not rescue the recency clock either.**

### 2.3 THE KAKO YEAR-3 SCENARIO

Stipulated: SF, effective pick 13, age 20 at end of year 3, Step-1 `v0` = 759.8. Path **A** — 18 games in
each of years 1 and 2 (36 total) at a *modest* average, then 20 games @ 75 in year 3. Path **B** — no games
in years 1–2, then the **identical** year-3 season. *"Modest" is not a number, so the whole grid is
published; the SF bar is 67.9.*

```
path A:  raw g = 56.00     recency u = 25.62        path B:  raw g = 20.00     recency u = 20.00
```

**LENS 1 — the measurement's own currency** (predicted remaining 6-season delivered value, from the band
model each clock selects):

| modest avg | clock | band A | band B | R̂(A) | R̂(B) | **B over A** |
|---:|---|---|---|---:|---:|---:|
| 55 | raw g | 36–70 | 16–35 | 1110.2 | 1187.8 | **+6.99%** |
| 55 | recency u | U5 | U4 | 1448.4 | 1303.4 | **−10.01%** |
| 60 | raw g | 36–70 | 16–35 | 1152.1 | 1187.8 | **+3.10%** |
| 60 | recency u | U5 | U4 | 1489.5 | 1303.4 | **−12.50%** |
| 65 | raw g | 36–70 | 16–35 | 1211.4 | 1187.8 | −1.95% |
| 65 | recency u | U5 | U4 | 1541.9 | 1303.4 | **−15.47%** |
| 70 | raw g | 36–70 | 16–35 | 1307.9 | 1187.8 | −9.18% |
| 70 | recency u | U5 | U4 | 1624.9 | 1303.4 | **−19.79%** |

**Caveat stated, not buried:** A and B straddle a **band edge** under both clocks, so these figures carry a
banded-model step. That is a property of the banded design 30B-M chose, and it is why Lens 2 exists.

**LENS 2 — the board's arithmetic, with the production leg HELD IDENTICAL between the paths, so the ONLY
thing priced is the clock:**

| clock / curve | σ(A) | σ(B) | price A | price B | **B over A** |
|---|---:|---:|---:|---:|---:|
| raw g, 30B-P wired curve | 0.1303 | 0.4089 | 746.3 | 750.6 | **+0.58%** |
| raw g, this order's refit | 0.1354 | 0.4008 | 746.4 | 750.5 | +0.55% |
| **recency u, this order's refit** | 0.1370 | 0.1796 | 746.4 | 747.1 | **+0.09%** |

*(at kako's own legs, `P` = 744.3 ≈ `v0` = 759.8 — the two legs nearly coincide, so the distortion nearly
vanishes.)* **Sweeping the production leg is what reveals the structure:**

| clock / curve | P = 300 | P = 600 | P = 900 | P = 1500 | P = 2500 |
|---|---:|---:|---:|---:|---:|
| raw g, 30B-P wired curve | **+35.59%** | +7.17% | −4.43% | −14.69% | −21.33% |
| raw g, this order's refit | +33.68% | +6.82% | −4.22% | −14.03% | −20.40% |
| **recency u, this order's refit** | **+5.39%** | **+1.09%** | **−0.68%** | **−2.25%** | **−3.27%** |

### 2.4 THE CLOCK VERDICT, AND WHAT THE SCENARIO ACTUALLY SAYS

> **1. The owner's diagnosis is confirmed, and its scope is narrower than stated.** The "B outprices A"
> distortion is **NOT a property of the clock alone**. It is the clock **times the gap between the
> production leg and `v0`**. It reaches the owner's ~25–30% only when production is **well below**
> pedigree (`P ≈ 300–400`); at kako's own legs it is **+0.58%**. The scenario is a *thin-production*
> pathology, not a *many-games* pathology.
>
> **2. The recency clock does exactly what the owner hoped — where it applies.** It compresses the A-vs-B
> gap by **roughly 6–7× at every production level** (+35.6% → +5.4%; +7.2% → +1.1%). **It does not fully
> close it (+5.39% at P = 300), as the seat predicted.**
>
> **3. But it LOSES its own preregistered criterion as a global clock, and it does not admit the ruled
> functional form.** Adopting it would fix the thin lane by degrading the deep book, where 1,339 of 4,033
> states live.
>
> **THE SEAT'S READING: keep RAW CAREER GAMES as the evidence clock.** The Kako pathology is real, but the
> measurement says the recency clock is the wrong instrument for it — and **T3's join addresses the same
> pathology from the correct side**, by fixing what happens in the thin lane rather than by re-scaling
> the axis for the whole book.

---

## 3 · T3 — THE JOIN, AND THE FIRST-GAME CLIFF

### 3.1 The construction (fixed in the prereg, before it was fitted)

| lane | law | source |
|---|---|---|
| **g = 0** | `price = v0 × D(c)` | the **wired sitter law**, exactly — nothing re-levelled |
| **1 ≤ g ≤ 10** | `price = v0 × D(c) × b(g; c)`, `b = B(≤g)/B(≤0)` | the 30A2 **cumulative backbone**, §6.4, as a **relative lift on the sitter price**; log-linear in `log1p(g)` |
| **11 ≤ g ≤ 15** | linear in `log1p(g)` between the two ends | **A DECLARED BRIDGE. It is not a measurement and it is not called one.** |
| **g ≥ 16** | the deep lane, **both readings shown** | the σ persistence curve where it was measured |

Backbone knots, **string-asserted against the committed packet**: depth 2 — 0.5684 / 0.6560 / 0.6936 /
0.8236 (lift 1.000 / 1.154 / 1.220 / **1.449**); depth 3 — 0.3600 / 0.5933 / 0.6807 / 0.6930 (lift 1.000 /
1.648 / 1.891 / **1.925**). Depth-2 lane for `c < 2.5`, depth-3 for `c ≥ 2.5`; **depth 4 is not
extrapolated** (30A2 §6.5 declines to wire it), so `c ≥ 3.5` holds the depth-3 lift. Disclosed.

**The production leg was not re-derived.** It was **inverted** out of the committed preview continuity
curves, `P(g) = [price(g) − σ(g)v0]/(1−σ(g))` — exact given the committed numbers. **Control: every row's
0-game print reproduces `v0 × D(c)` to agreement 1.00.** The published prices are integers, so `P(g)`
inherits a `±0.5/(1−σ)` band: **±6.40 at g = 1**, ±0.98 at g = 15. Printed per point in `JOIN_out.txt`.

### 3.2 THE CONTINUITY CURVE — price vs games 0→16 at fixed output

**`josh-smillie`** (ND 7, MID, `c` 2.92, `v0` 1688.8, `D` 0.2788, depth lane 3) — the row the ruling
turns on:

| g | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **PREVIEW** | 471 | **1671** | 1659 | 1640 | 1621 | 1598 | 1591 | 1582 | 1562 | 1545 | 1545 | 1547 | 1561 | 1564 | 1585 | 1607 | — |
| **JOIN (W)** | 470.8 | **645.3** | 775.9 | 821.5 | 858.6 | 890.2 | 894.3 | 897.8 | 901.0 | 903.8 | 906.3 | 1049.4 | 1181.1 | 1303.0 | 1416.4 | 1522.6 | 1622.3 |
| **JOIN (A)** | 470.8 | **645.3** | 775.9 | 821.5 | 858.6 | 890.2 | 894.3 | 897.8 | 901.0 | 903.8 | 906.3 | 1134.7 | 1344.7 | 1539.2 | 1720.3 | 1889.6 | 2048.7 |
| **lane** | sitter | backbone | backbone | backbone | backbone | backbone | backbone | backbone | backbone | backbone | backbone | BRIDGE | BRIDGE | BRIDGE | BRIDGE | BRIDGE | deep |

### 3.3 THE SMILLIE STEP, AND THE OTHER THREE

| row | depth lane | **preview 0→1** | **JOIN 0→1** | preview monotone 0–15 | **JOIN monotone 0–16** |
|---|---:|---:|---:|---|---|
| **`josh-smillie`** | 3 | **+254.8%** | **+37.1%** | **NO** | **YES** (both readings) |
| `harry-demattia` | 3 | +191.7% | **+37.1%** | **NO** | **YES** |
| `max-knobel` | 3 | +186.8% | **+37.1%** | **NO** | **YES** |
| `dyson-sharp` | 2 | +76.6% | **+9.5%** | YES | **YES** |

> **THE CLIFF CLOSES.** `josh-smillie`'s first-game step falls from **+254.8% to +37.1%** — an **85.4%
> reduction** — and **Ruling 6's continuity acceptance curve PASSES under the join in all four rows,
> where it FAILED in three of four under the preview.** The step is **+37.1% for every depth-3 row and
> +9.5% for the depth-2 row**, because it is now the backbone's own measured first-game lift, not an
> artefact of `σ(1) = 0.9218`.

### 3.4 THE CONFLICT — SHOWN, NOT AVERAGED

**The two curves do not meet.** In the 11–15 overlap, the backbone carried up on its own `≤5 → ≤10` slope
against the σ blend carried down:

| row | depth | thin extrap @13 | deep **W** @13 | deep **A** @13 | **W/thin** | **A/thin** |
|---|---:|---:|---:|---:|---:|---:|
| `dyson-sharp` | 2 | 1388.8 | 2347.0 | 3747.2 | **+69.0%** | **+169.8%** |
| `josh-smillie` | 3 | 912.8 | 1564.0 | 1967.4 | **+71.3%** | **+115.5%** |
| `max-knobel` | 3 | 557.1 | 927.0 | 1303.9 | **+66.4%** | **+134.0%** |
| `harry-demattia` | 3 | 584.4 | 790.0 | 963.4 | **+35.2%** | **+64.8%** |

**And the conflict is worse than a gap in the overlap — it is a LEVEL conflict throughout the thin lane.**
The implied pedigree weight `λ(g) = [price_join(g) − P(g)]/v0` is **NEGATIVE at every point 1–10 in all
four rows** (smillie −0.483 … −0.251; sharp −0.615 … −1.082):

> **The backbone's price for a 1–10-game player sits BELOW what the engine's own production machinery
> prices him at, on its own, at fixed output.** So in the thin lane the join is not a blend at all — the
> backbone **is** the whole price law and the production leg does not enter. That is a real, load-bearing
> consequence of taking the backbone at its word, and the seat is not going to soften it.

**THE HONEST T3 VERDICT:**

> **The join closes the first-game cliff and RELOCATES the discontinuity into the 11–15 bridge, where the
> two measured curves genuinely disagree by +35% to +71% (weight reading) or +65% to +170% (additive
> reading). It is a discontinuity spread over five games instead of concentrated in one, and it sits
> exactly where neither curve was measured.** The bridge is **declared**, not fitted. **The additive
> reading, which T1 resolves in favour of, WIDENS this conflict rather than narrowing it** — that is a
> genuine cost of T1's verdict and it is stated here, not left for the owner to find.

---

## 4 · T4 — THE OBJECT, FRAMED FOR THE OWNER

### 4.1 Both options, quantified

`entry_anchor` read live off the engine for **715 of 715** blended rows — **zero missing, zero fallback**.

| `entry_anchor / v0_step1` | n | share > 1 | median | p25 | p75 | p10 | p90 | sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **all blended** | 715 | **0.6615** | **1.0791** | 0.9157 | 1.3738 | 0.7397 | 1.6902 | 0.4131 |
| ND (non-pool) | 515 | 0.647 | 1.0682 | 0.9115 | 1.3049 | — | — | — |
| POOL | 200 | 0.700 | 1.1427 | 0.9890 | 1.7077 | — | — | — |

**The anchor is larger more often than not — but only just, and the dispersion is wide (p10 0.74, p90
1.69).** It is **not** a uniform uplift; a third of the book moves **down** on it.

**Whole-book pedigree as a share of printed, by object and by wiring:**

| wiring | obj = `v0` total | share | obj = `entry_anchor` total | share | **Δ share** |
|---|---:|---:|---:|---:|---:|
| **W** (weight) | 662,631 | **0.1342** | 667,414 | **0.1404** | **+0.62 pp** |
| **A** (additive) | 738,221 | **0.0731** | 741,399 | **0.0771** | **+0.40 pp** |

**The named rows under both objects:**

| row | g | prod | `v0` | **anchor** | W(`v0`) | W(anch) | **A(`v0`)** | **A(anch)** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`isaac-kako`** | 36 | 744.3 | 759.8 | **1069.0** | 748.0 | 821.9 | **886.3** | **944.1** |
| `willem-duursma` | 19 | 4198.2 | 3879.3 | **3435.7** | 4063.0 | 3875.0 | **5215.2** | **5098.9** |
| `dyson-sharp` | 13 | 3247.1 | 1551.0 | **1597.7** | 2347.0 | 2371.8 | **3747.2** | **3762.3** |
| `jacob-farrow` | 18 | 2720.0 | 1284.5 | **942.0** | 2089.0 | 1938.4 | **3066.9** | **2974.4** |
| `cooper-trembath` * | 26 | 2346.8 | 217.5 | **354.7** | 1652.0 | 1696.8 | **2394.4** | **2424.4** |
| `chris-scerri` * | 7 | 491.6 | 124.4 | **325.2** | 242.0 | 378.5 | **534.2** | **603.0** |
| `josh-smillie` | day-0 | — | 1688.8 | **1821.3** | 470.8 | 507.8 | 470.8 | 507.8 |
| `harry-demattia` | day-0 | — | 890.6 | **911.6** | 301.4 | 308.6 | 301.4 | 308.6 |
| `max-knobel` | day-0 | — | 830.5 | **641.5** | 287.4 | 221.9 | 287.4 | **221.9** |

`*` pool rows — v0 cells provisional, Step 4.

### 4.2 THE FINDING THE PREVIEW'S FRAMING OVERSTATED

**The preview named `kako`'s 759.8 vs 1069.0 as the object worth "the whole of finding (2)". It is not.**
On the whole book the object is worth **+0.62 pp of pedigree share and +4,783 board points on 662,631
(+0.72%)**. `kako` is a **large-gap** row, not a representative one — the median row's gap is **7.9%**, and
**33.9% of rows move the other way**. The seat filed **R13 predicting ≥3 pp** and was **wrong by a factor of
five**; that breach is owned in §8 and it is the most useful thing this task found, because it means
**the object question is nowhere near as load-bearing as the reading question (T1), which moves the book
11.4%.**

### 4.3 THE SEAT'S RECOMMENDATION, WITH REASONS — AND WHAT IS GENUINELY LOST

> **RECOMMENDATION: the STEP-1 POSITIONAL `v0`.** Three reasons, in order of weight:
>
> 1. **It is the ruled delivered-value language.** Step 1 built the positional `v0` surface *as* the
>    pedigree object in delivered-value currency, and the numéraire `s` is already inside it. `entry_anchor`
>    is a *price* object — a division level or a `v0_start` curve point — and mixing a price object into a
>    delivered-value sum re-imports the currency question the whole of Steps 1–3 exists to retire.
> 2. **`entry_anchor` is precisely the object the acts have been retiring.** `_a_blend`, `sitout_ev`'s
>    `ns == 0` arm and the year-zero floor `floor_frac × entry_anchor` are all being **REPLACED, not
>    wrapped** (STOP §5 Q4). Re-adopting the same object one layer up would leave the engine carrying two
>    live definitions of "what a thin record leans on".
> 3. **The measured `β` and σ were fitted against the Step-1 `v0`.** 30B-M's `v0` column *is*
>    `POSV[entry_pos][pick]`. **Substituting `entry_anchor` into a coefficient estimated on `v0` is a
>    silent re-scaling of `β` by the object ratio — median 1.08 but p10 0.74 and p90 1.69.** The
>    measurement does not transfer.
>
> **WHAT IS GENUINELY LOST, STATED AGAINST THE SEAT'S OWN RECOMMENDATION:**
>
> - **`entry_anchor` levels encode OWNER-SIGNED pool values.** For the 200 pool rows it is
>   `pool_level(p) × _PL_F × _b_factor(p)` — a signed division level with a live halt behind it. The
>   Step-1 `v0` cells for the same rows are **thin** and their fade is **Step 4's, not yet derived**.
>   On the pool arm the anchor is the better-attested object today, and `cooper-trembath` (217.5 vs
>   354.7) and `chris-scerri` (124.4 vs 325.2) are exactly where that shows.
> - **The anchor carries the ITEM B age shape and the C5 renormaliser**, which the positional `v0`
>   surface is pick-keyed and age-blind about.
> - **A live-store object tracks owner repricings that a fitted surface does not.** Choosing `v0` means
>   accepting that pedigree stops following signed pool moves until Step 4 re-derives them.
>
> **A THIRD OPTION THE SEAT WILL NAME BUT NOT TAKE:** `v0` on the ND arm, `entry_anchor` on the pool arm —
> each row on its better-attested object, until Step 4 derives the pool cells and the split can be
> retired. It is a split definition, which is a cost of its own. **This is an owner word and the seat does
> not take it.**

---

## 5 · THE THREE GAPS, CLOSED OR NOT

| gap | status after 30B-R |
|---|---|
| **G1** first-game cliff | **CLOSED IN SHAPE, RELOCATED IN SUBSTANCE.** smillie +254.8% → **+37.1%**; monotone 0→16 in all four rows. But the 11–15 bridge is declared, not measured, and the two curves conflict there by **+35% … +71%**, and the backbone prices the thin lane **below the engine's own production leg**. |
| **G2** pedigree object | **QUANTIFIED, NOT CHOSEN.** Worth **+0.62 pp** of book pedigree share, not the headline the preview implied. Seat recommends `v0`; the loss on the pool arm is named. **Owner's word.** |
| **G3** the reading | **RESOLVED BY DEFINITION.** σ is a value share; the fitted form is **additive with production at unit weight**; **β is the wireable object**. The weight wiring's `(1−σ)` production shrink is the common cause of the preview's findings (1) and (2). |

---

## 6 · WHAT THE PREVIEW BOARD'S NUMBERS BECOME — **DERIVED, NOT BUILT**

> **NO ENGINE RAN FOR THIS TABLE. NO BOARD EXISTS.** These are arithmetic on committed legs under the
> resolved configuration: **additive reading (T1) · raw career games, retained (T2) · the join (T3) ·
> object OPEN (T4, both printed)**. **Pre-numéraire: read the movement, not the level.**

| row | path | g | lane | prod `P` | `v0` | anchor | LIVE | STEP-2 | PREVIEW | **RESOLVED** | Δ% | w/ anchor | weight-rd |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **`isaac-kako`** | ND | 36 | deep | 744.3 | 759.8 | 1069.0 | 1413 | 1320 | 748 | **886** | **+18.5%** | 944 | 748 |
| `willem-duursma` | ND | 19 | deep | 4198.2 | 3879.3 | 3435.7 | — | 4223 | 4063 | **5215** | +28.4% | 5099 | 4063 |
| `dyson-sharp` | ND | 13 | **bridge** | 3247.1 | 1551.0 | 1597.7 | 3091 | 3269 | 2347 | **2811** | +19.8% | — | 2031 |
| `jacob-farrow` | ND | 18 | deep | 2720.0 | 1284.5 | 942.0 | 2601 | 2765 | 2089 | **3067** | +46.8% | 2974 | 2089 |
| `cooper-trembath` * | MSD | 26 | deep | 2346.8 | 217.5 | 354.7 | — | 2055 | 1652 | **2394** | +44.9% | 2424 | 1652 |
| `chris-scerri` * | SSP | 7 | **thin** | 491.6 | 124.4 | 325.2 | — | 467 | 242 | **165** | **−32.0%** | 431 | 165 |
| `josh-smillie` | ND | 0 | sitter | — | 1688.8 | 1821.3 | — | 471 | 471 | **471** | −0.0% | 508 | 471 |
| `harry-demattia` | ND | 0 | sitter | — | 890.6 | 911.6 | — | 301 | 301 | **301** | +0.1% | 309 | 301 |
| `max-knobel` | ND | 0 | sitter | — | 830.5 | 641.5 | — | 287 | 287 | **287** | +0.1% | 222 | 287 |

`*` **provisional — pool values pending Step 4.** `chris-scerri` additionally sits in the **thin lane where
the pool fade is not derived** (`D` forced to 1.0), so his −32.0% is the least trustworthy number in this
packet and is flagged twice. `dyson-sharp` sits in the **declared bridge** — his 2811 is an interpolation
between two ends, not a measurement.

**The whole book, same arithmetic, all 804 rows:**

| configuration | book total | vs preview |
|---|---:|---:|
| **PREVIEW as built** (weight, `v0`, no join) — *control* | **679,874** | **−0.00%** |
| weight reading, `v0`, **JOINED** | 667,260 | −1.86% |
| **ADDITIVE** reading, `v0`, no join | 755,464 | +11.12% |
| **RESOLVED: additive, `v0`, JOINED** | **715,229** | **+5.20%** |
| RESOLVED: additive, **anchor**, JOINED | 715,377 | +5.22% |

**Control:** the composer reproduces the committed preview total **679,875** to **one point** (integer
rounding). Lane populations under the resolved configuration: **sitter 89 · thin 99 · bridge 44 · deep 572**.

**Read this table as two independent moves.** The join **subtracts** 1.9% (it cuts the thin lane, because
the backbone prices below the σ blend there); the additive reading **adds** 11.1% (it stops shrinking the
production leg). They are separable and the owner can rule on them separately. The object (T4) moves the
book **+0.02%** and is, on this evidence, the smallest of the three questions.

---

## 7 · WHAT THIS ORDER DID NOT DO

- **Nothing wires.** No engine file, no `data/`, no board, no dial, no committed artifact outside
  `docs/evidence/one_machinery_2026-08-14/resolution/`. No GitHub comment was posted.
- **The seat did not choose the object (T4).** It recommended, with reasons, and named what is lost.
- **The seat did not reconcile the 11–15 conflict.** It measured it, published both curves, and declared
  the bridge a bridge.
- **STOP §5 Q1–Q4 remain OPEN.** This packet does not re-open them and does not close them.
- **The numéraire is not re-pinned.** Steps 4–7 have not run. Pool values are Step 4's.

---

## 8 · PREREG SCORED BY NUMBER — BREACHES OWNED

| # | verdict | reading |
|---|---|---|
| **R1** | **HELD** | σ is constructed as `β·v0̄/R̄`, a ratio of contributions to the outcome level — a **value share**. Identity checked to 1e-12 in all five bands. The weight wiring is not faithful. |
| **R2** | **HELD** | The fitted equation is additive with production at unit weight; **β is the estimated object and σ is derived from it.** Neither offered wiring is the regression. |
| **R3** | **BREACHED** | Predicted the weight form would **overstate** the pedigree value share in aggregate. It **UNDERSTATES** it: book value share **0.1342 (W) vs 0.1462 (σ)**, and `s_W < σ` on **three of the four** named rows (kako 0.2428 vs 0.2391 is the only overstatement). **The seat's reasoning was right about the mechanism (`v0` vs price) and wrong about the sign, because it read `v0̄/R̄` off the 30B-M panel where `R` is 6-season remaining value, while on the live board the established rows' production legs dwarf `v0`.** A scale confusion in the seat's own prediction, owned. |
| **R4** | **HELD** | Predicted kako in **[880, 960]** under the additive form; measured **886.3**. Filed blind, from the algebra, before building. |
| **R5** | **HELD** | Predicted the harmonic form would land in **[720, 760]**; measured **747.9**. |
| **R6** | **BREACHED** | Predicted the recency clock would beat raw games by ≥0.5% on pooled OOF RMSE. It **LOST by 1.08%** (722.868 vs 715.152), with only 9.7% of bootstrap draws favouring it. **The criterion was fixed in advance and the seat abides by it: raw games wins.** |
| **R7** | **NOT COMPUTABLE — owned as a breach** | Predicted the recency clock would shrink the AGE_LENS ≤20-vs-24+ gap by ≥30%. **The gap could not be computed on either clock**: re-cutting the *panel* (rather than the committed *cell table* the preview pooled) empties the 24+ × 16–35 cell at min-cell 8 **and** at min-cell 3 on the raw clock. **The seat did not reproduce the preview's +532.9 baseline and therefore claims no shrinkage.** What it can report: the recency clock moves the 24+ subgroup from **n = 82** in the raw 16–35 band to **n = 223** in U3, so the mechanism the prediction named (older players' games decay, lowering `u`) is visible — but the prediction as written is unanswerable and is scored a breach, not a pass. |
| **R8** | **FIRST LEG BREACHED, SECOND LEG HELD** | Predicted raw-clock B/A of **+20–30%**. Measured **+0.58%** at kako's own legs, reaching **+35.59%** only at `P = 300`. **The distortion is production-dependent, not universal — the seat's prediction stated it as a property of the clock and it is not.** Second leg: predicted the recency clock closes the gap to ≤10% but not to 0 — measured **max +5.39%**, never 0. **HELD.** |
| **R9** | **BREACHED** | Predicted smillie's joined 0→1 step ≤ **+25%**; measured **+37.1%**. **The cliff closed by 85.4% but not as far as the seat predicted. Nothing was re-tuned to reach the band.** |
| **R10** | **HELD** | The joined curve is monotone non-decreasing 0→16 for smillie — and for all four continuity rows, under **both** readings. Ruling 6's continuity curve **passes**. |
| **R11** | **HELD** | Predicted ≥25% conflict at g = 13. Measured **+35.2% to +71.3%** (weight) and **+64.8% to +169.8%** (additive). Both curves published; the bridge declared; nothing averaged. |
| **R12** | **HELD** | `entry_anchor > v0` on **66.15%** of blended rows (predicted ≥60%); median ratio **1.0791** (predicted [1.05, 1.45]). |
| **R13** | **BREACHED** | Predicted the object switch would raise whole-book pedigree share by **≥3 pp**. Measured **+0.62 pp** (weight) / **+0.40 pp** (additive) — **wrong by a factor of five**. This is the most useful breach in the order: it says the object question is the *smallest* of the three. |
| **R14** | **HELD** | `git diff 7a1c6ee..HEAD` touches `docs/evidence/one_machinery_2026-08-14/resolution/` only. No engine, no data, no board, no dial, no comment. |
| **R15** | **HELD** | Every number reproduces from committed artifacts plus a read-only engine load. Three independent controls held: the T2 panel reproduces 30B-M's 4,033 states and band fits byte-identically; the T3 inversion reproduces every 0-game print as `v0 × D`; the §6 composer reproduces the committed preview total 679,875 to one point. |

**8 HELD · 6 BREACHED · 1 NOT COMPUTABLE.** **Every breach is the seat's own prediction being wrong about
a measurement it had not yet made. None of the six was reached by re-tuning, and the two verdicts that
went against the seat's hypothesis (R6, the clock; R13, the object) are reported as the verdicts, not
argued around.**

---

## 9 · ANOMALIES AND LIMITATIONS, STATED

1. **The additive form's scale assumption is asserted, not proven** (§1.6). It is the single load-bearing
   assumption under T1's verdict.
2. **`β(g)` is an interpolation.** Log-linear in `log(games)` between the five band midpoints, flat
   outside — the same interpolation `o30bm_measure.py::sigma_at` uses for σ. **`β` is non-monotone**
   (0.297 → 0.362 → 0.223 → 0.153 → 0.020), so the interpolant carries a genuine hump at 6–15 games that
   is a property of the measurement, not of the interpolation. Not smoothed.
3. **The 71+ σ band is not significant** (t 0.49, CI spanning zero, −4.6 … 10.5%). Everything the deep
   book's pedigree leg does rests on a coefficient that cannot be distinguished from zero. Carried
   unchanged from 30B-M; flagged again here.
4. **`P(g)` is inverted from integer-rounded published prices**, with amplification ±6.40 at g = 1
   (§3.1). It is not noise at the resolution used, but it is not exact either.
5. **`P(16)` is a one-game log-linear extrapolation** off `P(10..15)` for the four continuity rows.
   Declared.
6. **The Kako scenario's Lens 1 straddles a band edge** under both clocks, so it carries a banded-model
   step. Lens 2 exists to isolate the clock from that.
7. **The recency clock's own σ curve is non-monotone and fits the ruled family 5.3× worse.** Even if the
   owner overrides T2's criterion, the wired functional form does not transfer to that axis.
8. **The T3 thin lane implies a NEGATIVE pedigree weight throughout** (§3.4). Taking the backbone at its
   word means the production leg does not enter below 10 games at all. That is a design consequence the
   owner has not ruled on.
9. **`chris-scerri` is the least trustworthy row in §6** — pool, thin lane, and a fade that is Step 4's
   and currently forced to 1.0.
10. **The AGE_LENS question (R7) is left open,** not answered. The preview's instrument (committed cell
    table) and this order's instrument (panel re-cut) are different objects and the seat did not bridge
    them.

---

## 10 · THE WORDS THE OWNER STILL OWES

1. **THE READING.** T1 says the faithful form is **additive**, `P + β(g)·v0`, not the wired
   `(1−σ)P + σ·v0`. **Accepting it raises the book 11.1% and cuts the pedigree share by half.** §1.
2. **THE OBJECT.** `v0` (seat's recommendation) or `entry_anchor`, or the ND/pool split the seat named
   and declined to take. Worth **+0.62 pp**. §4.
3. **THE JOIN.** Accept the backbone as the whole price law below 10 games — including that the
   production leg does not enter there — and accept a **declared bridge** across an 11–15 gap of **+35%
   to +71%**? Or rule the conflict resolved some other way? §3.
4. **THE CLOCK.** The recency clock **lost** its own criterion but fixes the Kako pathology in the thin
   lane. Keep raw games (seat's reading), or override the criterion for the thin lane only? §2.
5. **STOP §5 Q1–Q4 ARE STILL OPEN.** Unchanged by this order.

---

*Prereg filed and pushed (`e3a1168`) before the first resolution quantity existed. Every harness ran
foreground and sequential under the pinned five-var environment. Nothing was tuned after any reading.
Dispersion and n accompany every fitted quantity. Conflicts are shown, not averaged.*

> ## NOTHING WIRES UNTIL THE OWNER RULES.
