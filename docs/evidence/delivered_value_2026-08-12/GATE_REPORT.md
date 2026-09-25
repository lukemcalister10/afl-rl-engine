# GATE REPORT — ORDER 26B STEP 1 (Ruling 9)

**VERDICT: THE GATE FAILS. THE BUILD STOPS HERE, exactly as PREREG §1 P1.5 bound it to.**

Instrument: `o26b_gate.py` → `GATE.json`, `GATE_out.txt`. Read-only; pins asserted at entry and at exit
(store `d9a24282`, board `88ce647f`, `_merged_recover.py` `3f1468e5`, `rl_model.py` `e5eb5e44`,
`dist_redesign.py` `48ea1bfe`). Nothing under `engine/` was written.

---

## 1. THE PINNED PRICE FUNCTION (Ruling 3) — identified, pinned, and certified

```
season_points(X, P) = SCALE · posval( X + capt_prem(X) − (MA.REPL[P] − rd.REPL_DROP[P]) ) · 21
```

| component | file (md5) | line | live value |
|---|---|---|---|
| `posval` | `engine/rl_after/rl_model.py` (`e5eb5e44`) | 785 | `S_SH = 3.0` |
| `capt_prem` | `engine/rl_after/rl_model.py` (`e5eb5e44`) | 676 | `CAPT_THRESH = 107.4` |
| `SCALE` | `engine/rl_after/rl_model.py` (`e5eb5e44`) | 1120, reassigned 1324 | `1.4398232006949683` |
| `MA.REPL` | `engine/rl_after/rl_model.py` (`e5eb5e44`) | 779 | `{MID 80.1, SD 78.3, RUCK 78.5, KPD 68.4, SF 70.9, KPF 66.8}` |
| `REPL_DROP` | `engine/forward_valuation/dist_redesign.py` (`48ea1bfe`) | 39 | uniform `3.0` |
| `disc_factor` | `engine/rl_after/rl_model.py` (`e5eb5e44`) | 906 | `LENS['bal'] = 0.14`, `RL_AGE_DISC` OFF |
| `× 21` (season games) | `engine/rl_after/rl_model.py` (`e5eb5e44`) | 978–979 | — |

**The season term IS `rl_model.py::proj_from_peak`'s k-th term (line 963, 978–979).** It is reused as a
live attribute lookup, never reimplemented and never hand-copied.

Effective bars, computed off the engine's own netting path — **identical to Ruling 1's stated set**:

| | MID | SD | RUCK | KPD | SF | KPF |
|---|---|---|---|---|---|---|
| derived `MA.REPL − REPL_DROP` | **77.1** | **75.3** | **75.5** | **65.4** | **67.9** | **63.8** |
| Ruling 1 as filed | 77.1 | 75.3 | 75.5 | 65.4 | 67.9 | 63.8 |

`GAMMA = 1.0`, so `val(r) = round(SCALE·r)` is **linear** and delivered value is **additive across
seasons in board points**. This is the fact that makes Ruling 11's two-layer split work at all: Layer 2
can price a season at a time and sum.

---

## 2. THE SIX PROJECTED CAREERS ARE CONSTRUCTIBLE — the brief's structural escape does NOT apply

The brief allowed a STOP if "constructing full six-path careers from the band proves structurally
impossible with the engine's own objects". **It is not impossible.** `price6` is

```
price6(p, bb, Y) = SCALE_DIST · Σ_i WQ6[i] · dp.v_at_peak(p, bb[i], 'bal')      (MA.REPL lowered by REPL_DROP)
dp.v_at_peak(p, L) = max( MA.val( proj_from_peak(g, L, a, cur, 'bal', g0, fut, hc) ), MA.prod_floor(p) )
```

and `proj_from_peak`'s loop **is a career**: season k is played at age `a+k` at level
`L·frac(a+k, PEAK_AGE[g])`, floored at the current level while `a+k ≤ peak age` and at `k = 0`, valued at
`bnow(p)` in season 0 and at the `futblend(p)` mix from season 1 (Ruling 5's two uses of position, in the
engine's own words), truncated when `age > 38` or `frac < 0.42`. Those are the six careers, and they are
printed per player in `GATE_out.txt`.

Two projection-side multipliers are carried and **declared**, not hidden: `×1.05` for KPF/KPD, and the
runway×elite premium `(1 + clip((25−a)/6)·clip((L/PEAK[g]−0.97)/0.30)·PMAX)`. Both belong to the engine's
price of a *projected* career; both are named in the harness's config block.

---

## 3. RESULT (a) — THE PRICE-FUNCTION IDENTITY: EXACT

Scoring the six careers with the pinned function and blending at WQ6 reproduces the engine's own
`price6(p, b6(p))`:

| population | n | max \|mine/price6 − 1\| | within 1e-6 |
|---|---|---|---|
| the 12-row panel | 12 | **0.000e+00** | **12 / 12** |
| **every active board row** | **800** | **0.000e+00** | **800 / 800 (100 %)** |

**Bit-exact, board-wide.** The choice of price function is certified against the engine's own
production-value object. (PREREG P1.1 — scored as a VERIFICATION, not a prediction; §0A disclosed it.)

---

## 4. RESULT (b) — RULING 9's GATE vs THE LIVE BOARD PRICE: FAILS

±2 % against `rl_app_data.json::active[].v`:

| key | pos | age | pick | scored blend | price6 | vs price6 | board v | vs board | verdict |
|---|---|---|---|---|---|---|---|---|---|
| **willem-duursma** | MID | 19 | 1 | 4050.00 | 4050.00 | +0.0000 % | 3977 | **+1.84 %** | **PASS** |
| nick-daicos | MID | 23 | 4 | 10554.84 | 10554.84 | +0.0000 % | 10945 | −3.56 % | FAIL |
| harry-sheezel | MID | 22 | 3 | 11433.30 | 11433.30 | +0.0000 % | 11764 | −2.81 % | FAIL |
| marcus-bontempelli | MID | 31 | 4 | 3234.04 | 3234.04 | +0.0000 % | 3876 | −16.56 % | FAIL |
| max-gawn | RUCK | 35 | 33 | 2763.00 | 2763.00 | +0.0000 % | 3336 | −17.18 % | FAIL |
| harley-reid | MID | 21 | 1 | 4269.30 | 4269.30 | +0.0000 % | 3820 | +11.76 % | FAIL |
| **jai-newcombe** | MID | 25 | pool | 4913.14 | 4913.14 | +0.0000 % | 4883 | **+0.62 %** | **PASS** |
| harrison-ramm | KPD | 20 | pool | 794.84 | 794.84 | +0.0000 % | 545 | +45.84 % | FAIL |
| vigo-visentini | RUCK | 21 | pool | 791.84 | 791.84 | +0.0000 % | 182 | **+335.08 %** | FAIL |
| josh-treacy | KPF | 24 | pool | 7157.74 | 7157.74 | +0.0000 % | 6921 | +3.42 % | FAIL |
| izak-rankine | SF | 26 | 3 | 4511.46 | 4511.46 | +0.0000 % | 4685 | −3.70 % | FAIL |
| lachlan-ash | SD | 25 | 4 | 6088.96 | 6088.96 | +0.0000 % | 5728 | +6.30 % | FAIL |

**2 of 12 PASS.** The owner's named row, `willem-duursma`, is one of the two.

Board-wide control (the panel is not a fluke, in either direction):

| population | n | median `mine/board_v` | within ±2 % |
|---|---|---|---|
| **all active** | **804** | **1.0044** | **72 (9.0 %)** |
| ND, ≥4 qualifying seasons | 305 | 0.9870 | 12.5 % |
| ND, <4 qualifying seasons | 256 | 0.9871 | 7.8 % |
| pool, ≥4 qualifying seasons | 89 | 1.0079 | 13.5 % |
| pool, <4 qualifying seasons | 154 | **1.1688** | **1.3 %** |
| MID | 197 | 0.9852 | 13.2 % |
| SD | 173 | 1.0083 | 10.4 % |
| SF | 185 | 0.9648 | 7.6 % |
| KPD | 92 | 1.0512 | 6.5 % |
| KPF | 103 | 0.9982 | 4.9 % |
| RUCK | 54 | 1.1317 | 5.6 % |

Distribution: min 0.0000 · p05 **0.0904** · median 1.0044 · p95 **4.2048** · max 23.5748.

**The median is essentially unbiased (1.0044).** The failure is not a level error in the price function —
it is *dispersion*: the shipped board price differs from the band blend by a factor spanning roughly
0.09× to 4.2× across the middle 90 % of the board.

---

## 5. THE ATTRIBUTION OF THE GAP — five named legs, ZERO RESIDUAL

The shipped board price is not `price6`. Between them sit exactly five multiplicative legs, all in the
engine, all named:

1. **`_uncomp_prod`** — the LEG-B un-compress map at the production-value hook (`RL_UNCOMP = 1`,
   `s = 0.10`), `_merged_recover.py`.
2. **the pedigree-pole blend** in `raw_ev` — `pr + w·recover(perf, par)·max(0, po − pr)`, with
   `w = wage·tfade·expgate` (`_merged_recover.py:458–475`).
3. **`ev/raw_ev`** — `_prod_path`, `iso_eff` (the isotonic pick guard), the RUCK ceiling and W4 KPF
   compression, the sit-out treatment, the `_h_cut`s, and the entry-anchor floor `floor_frac·entry_anchor`.
4. **the L7 numéraire divisor** ≈ 1.0524 (`ev / board_v`).
5. (**the price function itself** — measured at exactly 1.0000 for every row, i.e. it contributes
   *nothing* to the gap.)

| key | mine/p6 | uncomp | pole+ | ev/raw | numéraire | product | measured | residual |
|---|---|---|---|---|---|---|---|---|
| willem-duursma | 1.0000 | 1.0000 | 1.0175 | 1.0155 | 1.0523 | 1.0184 | 1.0184 | −2.2e−16 |
| nick-daicos | 1.0000 | 0.9981 | 1.0931 | 1.0002 | 1.0524 | 0.9644 | 0.9644 | −2.2e−16 |
| harry-sheezel | 1.0000 | 0.9918 | 1.0914 | 1.0004 | 1.0524 | 0.9719 | 0.9719 | 0 |
| marcus-bontempelli | 1.0000 | **1.0986** | **1.1481** | 1.0000 | 1.0524 | 0.8344 | 0.8344 | 2.2e−16 |
| max-gawn | 1.0000 | **1.1004** | **1.1549** | 0.9999 | 1.0525 | 0.8282 | 0.8282 | 1.1e−16 |
| harley-reid | 1.0000 | **0.9171** | 1.0258 | 1.0010 | 1.0524 | 1.1176 | 1.1176 | −2.2e−16 |
| jai-newcombe | 1.0000 | 0.9974 | 1.0499 | 0.9988 | 1.0524 | 1.0062 | 1.0062 | −2.2e−16 |
| harrison-ramm | 1.0000 | 1.0000 | **1.2437** | **0.5806** | 1.0532 | 1.4584 | 1.4584 | −2.2e−16 |
| vigo-visentini | 1.0000 | 1.0000 | 1.1298 | **0.2146** | 1.0549 | **4.3508** | 4.3508 | −8.9e−16 |
| josh-treacy | 1.0000 | 0.9787 | 1.1524 | 0.9023 | 1.0524 | 1.0342 | 1.0342 | −2.2e−16 |
| izak-rankine | 1.0000 | 0.9956 | 1.0975 | 1.0001 | 1.0523 | 0.9630 | 0.9630 | 0 |
| lachlan-ash | 1.0000 | 0.9467 | 1.0456 | 1.0001 | 1.0524 | 1.0630 | 1.0630 | −2.2e−16 |

`product = (mine/p6) × numéraire / (uncomp × pole × ev/raw)` reproduces the **measured** ratio to
floating point. **Max |residual| over the panel: 8.9e−16.** The gap is fully attributed; there is no
unnamed leg. (The harness asserts this and would halt if a residual appeared.)

**Where each leg bites, in plain language:**

- **`ev/raw` is the violent one for thin records.** `vigo-visentini` reads 0.2146 — the sit-out /
  entry-anchor machinery holds him at 182 while the band's own careers price him at 792. `harrison-ramm`
  reads 0.5806 for the same reason. These two rows alone account for the p05 tail.
- **`uncomp` and `pole+` are the veteran legs.** `marcus-bontempelli` and `max-gawn` each take
  ~1.10 × ~1.15 ≈ 1.27 of uplift the band-career score does not carry, which is why both read ~−17 %.
- **The numéraire is a flat 1.0524** on every row — a pure unit change, and the *only* leg that a
  delivered-value derivation could safely absorb.

---

## 6. WHY THIS IS A GATE FAILURE AND NOT A SCORER DEFECT

Ruling 9's gate is written on the premise that a player's board price **is** the WQ6 blend of his six
projected outcome careers. On the shipped engine that premise is false: `price6` is one input to
`raw_ev`, which is one input to `ev`, which is divided by the numéraire to make the board.

So the gate is measuring the distance between **the engine's production-value object** and **the engine's
shipped board price** — not the distance between two candidate scorers. The scorer is exact
(§3, 800/800 bit-exact). The 91 % failure rate is the size of the four non-production legs.

**Two readings are available and I do not choose between them — that is the owner's call:**

- **Reading A (the gate is correctly specified and the answer is informative).** The board price is not a
  discounted-delivered-value object, and any derivation that sets `printed day-0 == derived entry value`
  will move prices by the size of these four legs. The gate has done its job: it has revealed the
  distance before the derivation was built on top of it.
- **Reading B (the gate's target should have been `price6`).** If Ruling 9's intent was to certify the
  *price function*, the target is `price6(p, b6(p))` and the gate passes **800/800 bit-exact**. That is
  the closest achievable identity check, and it was named in PREREG §1 P1.6 **before** the result was
  seen, so it cannot be a post-hoc substitution.

**I did not silently substitute Reading B.** Ruling 9 says "±2 % vs his live board value" and
"gate failure = STOP". Measured against the live board value the gate fails, and the build stops.

---

## 7. PREREG §1 SCORED

| # | prediction | outcome |
|---|---|---|
| P1.1 | scorer reproduces `price6` to 1e-6 for every active row | **HIT** (bit-exact, 800/800) — *verification, per §0A* |
| P1.2 | gate fails; ≤3 of 9 panel rows inside ±2 % | **HIT** (2 of 12; 9.0 % board-wide) |
| P1.3 | failure attributable to named non-production legs | **HIT** (five legs, residual 8.9e−16) |
| P1.4 | daicos `mine/board_v` ∈ [0.85, 0.95]; visentini > 2.0 | **HALF-MISS**: daicos **0.9644** (outside the band, too high); visentini **4.351** HIT |
| P1.5 | STOP on failure; deliver prereg + gate + Layer 1 + packet only | **BINDING, HONOURED** |
| P1.6 | closest achievable check = `== price6` at 1e-6 | **HIT**, and named before the result |
| P5.1 | duursma `mine/board_v` ∈ [0.90, 1.06] | **HIT** (1.0184) |

---

## 8. WHAT THE LANDING ORDER MUST KNOW

1. The price function is settled and pinned. Whoever resumes 26B does not need to re-derive it; it is in
   `o26b_gate.py::season_raw` / `season_points`, five lines, all live engine attributes.
2. `GAMMA = 1.0` — delivered value is additive in board points. Layer 2 can be a straight sum.
3. **The permanent assert the brief describes (`printed day-0 == derived entry value`) cannot be written
   against `ev()` as the engine stands.** It would have to be written against `price6`, or the four
   non-production legs would have to be re-scoped at the day-0 site first. That is an engine question and
   an owner ruling, not a build decision — and it is the single most load-bearing thing this order found.
4. The dispersion is *structured*: pool rows with <4 qualifying seasons read a median 1.1688 and are
   inside ±2 % only 1.3 % of the time. Those are exactly the rows the pool re-pricing is about.
