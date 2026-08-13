# SHIPPING PACKET — ORDER 28, THE GRACE-A ADOPTION BUILD

**2026-08-13 · branch `build/grace-adoption` · build seat**

> ## NOTHING HAS LANDED.
> The engine dial ships **DEFAULT OFF**. No store byte moved. No board was re-pinned. No curve was
> adopted. No pool level was signed. No identity carrier changed. The movers board in §6 is a
> **variant build in a scratch workspace** — it does not exist on `main` and never touched the
> checkout. This packet is a decision document, not a landing.

---

## 1. WHAT THE OWNER ASKED FOR, AND WHAT IS IN FRONT OF HIM

Three rulings compose in this packet.

**RULING A — GRACE-A EVERYWHERE** (#334 comment 5276077959):

> *"No, I think we can lock grace A in. And also apply it at board level too — so for backtesting and
> the live board, the diminishing seasons only counts from the second season (i.e. age 20 onwards).
> Same implementation as on the curve. And grace A applies for the pool, for the pathways. For
> everything."*

**RULING B — THE ASYMMETRIC BOUNDARY** (same comment):

> *"I also think the loclin effect on the pick 64 is too intense. So I'd be happy to not extend below
> it, and just be inconsistent and apply it north to pick 1 but not south to pick 64."*

**RULING C — THE MONOTONE RULING** (#334 comment 5276216984, as corrected by addendum-2):

> *"I'm reviewing the v0 sheet and it seems like it's non-monotonous? Pick 8 worth more than pick 6.
> And by position too… It doesn't make sense that a lower pick would be worth more than a higher
> pick?"*

Four things are delivered: **the engine dial** (§2–4), **the candidate landing curve and v0s**
(§5), **the board movers packet** (§6), and **the instruments** (§7). §8 scores the pre-registrations
and §9 owns the breaches.

---

## 2. THE ENGINE DIFF, EXPLAINED

Three files, **63 inserted lines, 13 changed**. `git diff origin/main -- engine/` is the whole of it.

### 2.1 The rule

A normal-age entrant (**entry age ≤ 19**) carries **seasons 1 and 2 at full weight**; his **third
season is the first diminished**. An entrant at **20 or older gets no grace** and stays on today's
ladder, byte-for-byte.

### 2.2 Why one rule needs two different exponents

There are two discount clocks in this system, and conflating them is the one way this order could go
wrong quietly. So it is written out.

| | **CURVE SIDE** (the Layer-2 scorer) | **BOARD SIDE** (`disc_factor`) |
|---|---|---|
| index | `k_c = season_year − entry_year` | `k_e` = seasons **ahead of the pricing year** |
| first played season | `k_c = 1`, already carries `1.14⁻¹` | whichever `k_e` it happens to be |
| the free step | none — everything discounts to acquisition | **`k_e = 0` is always 1.0** (standing engine convention) |
| discounts to | the **acquisition date** | **today** |

The board never discounts the present season. So the board needs **one** extra free step, and only
for a player whose present season *is* his first:

```
curve : exponent = max(0, k_c − 2)                      (26B-V Reading O, G_O = 2)
board : exponent = max(0, k_e − r),  r = max(0, 1 − s)  (s = seasons already completed)
```

Season by season, for an entrant at ≤ 19:

| his career season | 1st-year row (s=0) | 2nd-year row (s=1) | 3rd-year row (s=2) |
|---|---|---|---|
| season 1 | `k_e=0` → exp 0 **full** | past | past |
| season 2 | `k_e=1`, r=1 → exp 0 **full** | `k_e=0` → exp 0 **full** | past |
| season 3 | `k_e=2`, r=1 → exp **1** | `k_e=1`, r=0 → exp **1** | `k_e=0` → exp 0 (engine convention) |
| season 4 | exp 2 | exp 2 | exp 1 |

Seasons 1 and 2 full, season 3 first diminished — on every row. **`r` is non-zero only at `s = 0`.**
That is a consequence of the rule, not a design choice, and it is why the live-board effect is narrow.

**Disclosed, not smuggled:** the engine's free present season means a third-year player's *current*
season is undiscounted on the board while the curve charges it `1.14⁻¹`. That divergence is
pre-existing, holds identically on flat-14, is a per-player constant, and is **not created by grace**.

### 2.3 The code

```python
RL_GRACE = os.environ.get('RL_GRACE','0') != '0'   # DIAL, DEFAULT OFF
GRACE_G = 1 ; GRACE_MAX_ENTRY_AGE = 19
def grace_years(p):
    if not RL_GRACE or p is None: return 0
    if (p['year'] - by(p)) > GRACE_MAX_ENTRY_AGE: return 0   # 20+ gets nothing (ruled)
    return max(0, GRACE_G - max(0, AGE_REF - debut(p)))

def disc_factor(a, d, k, lens='bal', grace=0):
    if k <= 0: return 1.0
    if grace:
        k = max(0, int(k) - int(grace))
        if k <= 0: return 1.0
    ...
    return (1.0 + age_disc(a, d, lens)) ** k
```

**Entry age is `p['year'] − by(p)` — the exact arithmetic Layer 1 used** (`o26b_layer1.py:121`,
fallback 18 included), so the curve side and the board side select the identical population.
**Not `_age_at()`**: its `18 + (ref − cycle_year)` floor would shift every off-season entrant by a
year and silently change who gets grace. The trap is named in the code so nobody walks into it later.

### 2.4 Every call site

| site | file | how `grace` gets there |
|---|---|---|
| `proj_from_peak` | `rl_model.py` | new kwarg `grace=0`, threaded from callers (it takes a scalar age, not a record) |
| `prod_floor` | `rl_model.py` | `grace_years(p)` computed locally |
| `_proj_w4` | `_merged_recover.py` | new kwarg, forwarded verbatim |
| `_prod_floor_w4` | `_merged_recover.py` | `MA.grace_years(p)` computed locally |
| `player_raw` | `rl_model.py` | passes `grace=grace_years(p)` |
| `v_at_peak` | `distribution_pricing.py` | one grace passed to **both** §1b legs — one player, one ladder |
| synthetic / pick-level nodes | 3 sites | `grace` omitted → 0. **Declared:** a band node is not a person and has no entry age. |

The engine's own `⚠ DUPLICATE-LOOP HAZARD` fence (`rl_model.py:994`, *"edit BOTH or neither"*) is
honoured: `prod_floor` and `_prod_floor_w4` received the identical two lines.

### 2.5 Mode 9

Mode 9 (the age-keyed path product) is inactive on the live config (flat 14%, `RL_AGE_DISC=False`,
ruled). For coherence, grace drops the earliest factors from the product (`j` runs `grace+1 … k`), so
the same seasons go free under either mode. Declared; unreachable on the live config.

---

## 3. THE BYTE-IDENTITY-OFF PROOF

> **A full board rebuild from a clean staged copy of the MODIFIED engine, with the dial present but
> `RL_GRACE=0`, reproduces the live board `88ce647f531030d8d2e094188b258191` EXACTLY.**

| run | dial | `rl_app_data.json` md5 | what it proves |
|---|---|---|---|
| **base0** — engine as committed on `origin/main` | n/a | `88ce647f531030d8d2e094188b258191` | the harness reproduces the live board |
| **off1** — **modified engine, dial OFF** | `RL_GRACE=0` | **`88ce647f531030d8d2e094188b258191`** | **BYTE-IDENTICAL — PASS** |
| **on1** — modified engine, dial ON | `RL_GRACE=1` | `0ce52771ed8f9ef326dd61f0e4aa71a8` | the dial is **reachable** |
| **on2** — independent rebuild, dial ON | `RL_GRACE=1` | see `DETERMINISM.txt` | determinism |

`base0` is what makes `off1` non-vacuous — the same harness against the *unmodified* engine prints the
same md5, so `off1`'s match is a statement about the change, not about a harness that always prints
`88ce647f`. And `on1` differing proves the dial is not inert when on.

**It is identity by construction, not by tolerance.** At `grace = 0` the new branch is not entered, so
the returned expression is the pre-order one, evaluated with the same float operations in the same
order. Every new call site passes `0` whenever the dial is off, because `grace_years()` returns `0` on
its first line. Full record: `BYTE_IDENTITY_OFF.md`.

---

## 4. THE IDENTITY GATE, RE-RUN WITH THE DIAL ON

Full transcript: `GATE28_out.txt` / `GATE28.json`. Harness: `o28_gate.py`, adapted from `o26b_gate.py`.

**The gate that matters is the PRICE-FUNCTION IDENTITY**: the 26B scorer, running grace, against the
engine's own `price6`, running grace — where the scorer takes its grace from **`MA.grace_years(p)`**,
the engine's own callable, rather than re-implementing the rule. If grace reached one side and not the
other, this is where it would show.

<!--GATE_RESULT-->

**The Ruling-9 ±2% leg is read TWICE, and only one reading means anything.** Against the **live**
board the scorer has moved and the frozen board has not, so young rows must fall out of the ±2% class
— that degradation is the expected reading, not a failure. Against the **dial-ON variant board** the
comparison is like-for-like. Both are printed.

---

## 5. THE CANDIDATE LANDING CURVE AND v0s

Full transcript: `DERIVE28_out.txt` / `DERIVE28.json`. Harness: `o28_derive.py`.

```
raw cohorts ──► LOCLIN (26B-C2) ──► HYBRID south boundary (Ruling B) ──► weighted PAVA (Ruling C) ──► anchor pick 1 = 3000
```

Every estimator is **reused and cited, none reinvented**: `o26b_loclin.kernel_loclin` (the 26B-C2
local-linear), `harness_pvc_REPINNED_pass3.kernel_raw` (the **shipped** weighted-mean aggregator), and
`par_build.py::_pava(increasing=False)` (the **shipped** weighted pool-adjacent-violators, the same
routine the engine already uses for its non-increasing-in-pick prior). **Engine bytes touched by the
derivation: 0.**

### 5.1 The south seam (Ruling B) — the zone, disclosed

| quantity | value |
|---|---|
| interior norm `ν = p90 \|LL/WM − 1\|` over picks 4–48 | **0.0290** (2.90%) |
| **SOUTH TAIL ZONE** | **picks 57–64** (length 8) |
| **SEAM PICK `p₀`** | **56** (the last pure-loclin pick; `HYB(56) = LL(56)` exactly) |
| truncation at pick 50 invoked? | **no** |
| **NO-CLIFF ASSERT** | hybrid max adjacent step **0.0486** vs worst parent **0.1383** — **PASS** |
| tail monotone before PAVA? | **yes** |

The blend is `w(p) = smoothstep((p − p₀)/(64 − p₀))`, `HYB = (1−w)·LL + w·WM`. At the seam `w = 0`
and `S′(0) = 0`, so the value is continuous **and** the weighting adds no kink; at pick 64 `w = 1` and
the curve **is** the weighted-mean reading, which is what the owner ruled.

| pick | LL | WM | LL/WM − 1 | w | HYB |
|---|---|---|---|---|---|
| 56 | 239.9 | 246.2 | −2.54% | 0.000 | 239.9 |
| 57 | 228.4 | 239.1 | −4.50% | 0.043 | 228.8 |
| 58 | 215.1 | 231.8 | −7.22% | 0.156 | 217.7 |
| 59 | 200.2 | 224.4 | −10.79% | 0.316 | 207.8 |
| 60 | 183.9 | 217.0 | −15.25% | 0.500 | 200.5 |
| 61 | 166.7 | 209.9 | −20.59% | 0.684 | 196.2 |
| 62 | 148.7 | 203.0 | −26.74% | 0.844 | 194.5 |
| 63 | 130.5 | 196.6 | −33.59% | 0.957 | 193.7 |
| **64** | **112.5** | **190.5** | **−40.96%** | **1.000** | **190.5** |

### 5.2 The monotone step (Ruling C) — every removed ascent

**8 ascending adjacent pairs**, all in the interior, **none at pick 1**. The owner's own case — pick 8
above pick 6 — is among them.

| pair | pre A | pre B | ascent | raw cohort mean A | raw cohort mean B | PAVA value |
|---|---|---|---|---|---|---|
| 6→7 | 1252.5 | 1322.3 | +69.8 | 493.4 | 1490.9 | 1403.2 |
| 7→8 | 1322.3 | 1553.1 | +230.8 | 1490.9 | 1851.0 | 1403.2 |
| 9→10 | 1368.7 | 1395.9 | +27.3 | 996.0 | 1541.5 | 1403.2 |
| 10→11 | 1395.9 | 1483.8 | +87.9 | 1541.5 | 1402.4 | 1403.2 |
| 16→17 | 796.3 | 819.5 | +23.2 | 704.1 | 835.9 | 864.0 |
| 17→18 | 819.5 | 871.3 | +51.8 | 835.9 | 836.6 | 864.0 |
| 18→19 | 871.3 | 910.1 | +38.8 | 836.6 | 959.2 | 864.0 |
| 19→20 | 910.1 | 914.0 | +3.9 | 959.2 | 1193.7 | 864.0 |

PAVA pools picks **6–12** to 1319.1 (anchored) and picks **15–21** to 812.2. **The data behind them
stays visible** — the raw cohort means are printed above and in the full curve table, so nothing was
replaced silently. *(The honest-data / rational-price split: the cohort means at n = 18 genuinely
ascend; the priced object may not, because pick 6 can select whoever pick 8 would have.)*

**Asserts, each able to fail:**

| assert | result |
|---|---|
| **A1** PAVA did not pool pick 1 with pick 2 | **PASS** |
| **A2** weighted-sum conservation `\|post/pre − 1\|` | **0.000e+00 — PASS** |
| **A3** output non-increasing over picks 1–64 | **PASS** |
| **A4** Ruling-13 reconciliation, post-monotone | **2.220e−16 — PASS** |
| **A5** anchor invariance vs 26B-V grace-A | head/factor/premium identical |

**THE CONSERVATION LEDGER** — the owner's *"in enforcing the curve, total values all in or by
position drop or rise a lot, that is not ideal"*:

| # | quantity | pre | post | drift |
|---|---|---|---|---|
| 1 | weighted `Σ w·value` (w = per-pick cohort n) | 904,041.1015 | 904,041.1015 | **+0.000e+00** (exact by construction) |
| 2 | plain `Σ value` | 50,331.6503 | 50,331.6503 | **+0.0000%** |
| 3 | pre-anchor head / anchor factor | 3191.1790 / 0.9401 | 3191.1790 / 0.9401 | **unmoved** (A1 forbids otherwise) |
| 4 | `Σ posv` MID / SD / SF / KPD / KPF / RUCK | — | — | **−0.012% / +0.021% / +0.129% / +0.044% / +0.031% / +0.073%** |
| | `Σ` all-in | 47,316.4 | 47,316.4 | **+0.0000%** |

Weighted PAVA replaces each violating block by its **weighted mean**, so block sums — and therefore
the whole-curve total — are conserved by construction rather than by adjustment. The plain sum is
conserved too because every pooled block sits inside picks 1–60, where `n = 18` uniformly.

### 5.3 The curve, at the picks the owner reads

| pick | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 | 50 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **CANDIDATE** | **3000** | **2668** | **2569** | **1804** | **1319** | **1319** | **812** | **812** | **607** | **479** | **274** | **179** |
| 26B-V grace-A (pure loclin) | 3000 | 2668 | 2569 | 1804 | 1243 | 1312 | 803 | 859 | 607 | 479 | 274 | 106 |
| flat-14 (the operative 26B C2 basis) | 3000 | 2663 | 2563 | 1802 | 1242 | 1309 | 808 | 868 | 614 | 499 | 283 | 105 |
| **today's landed PVC** | 3000 | 2999 | 2874 | 1881 | 1549 | 1460 | 1030 | 990 | 663 | 514 | 346 | 185 |
| candidate / 26B-V | 1.000 | 1.000 | 1.000 | 1.000 | 1.061 | 1.005 | 1.012 | 0.945 | 1.000 | 1.000 | 1.000 | **1.694** |
| candidate / PVC | 1.000 | 0.890 | 0.894 | 0.959 | 0.852 | 0.904 | 0.789 | 0.820 | 0.915 | 0.932 | 0.792 | **0.968** |

Read it this way: **the candidate differs from 26B-V's grace-A curve in exactly two places and for
exactly two reasons** — in the interior where PAVA flattened an ascent (Ruling C), and in the deep
south where the boundary reverts (Ruling B). Everywhere else it is bit-identical.

### 5.4 Head, factor, premium

| metric | **CANDIDATE** | 26B-V grace-A | flat-14 C2 |
|---|---|---|---|
| pre-anchor head (pick 1) | **3191.2** | 3191.2 | 2463.1 |
| anchor factor | **0.9401** | 0.9401 | 1.2180 |
| **pick-vs-player premium** | **−6.0%** | −6.0% | +21.8% |
| ND cohort mean | 789.1 | 789.1 | 615.5 |

`|candidate head / 26B-V head − 1| = 0.000e+00`. **Neither the boundary nor the monotone step can
reach pick 1**, so the anchor, the factor and the premium are exactly the numbers the owner already
ruled on. His own note stands: at −6.0% the pick-vs-player premium is near parity, which keeps the
pending numéraire-route decision low-stakes.

### 5.5 Positional relativities — the continuous per-pick curves

**The addendum-2 correction is carried in full: the relativity machinery was NOT rebuilt, because it
was never a step function.** The implementation is and always was continuous per pick:

```
posv_g(p) = allin(p) · rawpos_g(p) / Σ_h share_h(p)·rawpos_h(p)
```

with `rawpos_g` a per-position local-linear fit over log(pick). The five-band table in the 26B packet
was a **summary of band means**. `DERIVE28_out.txt` §5 now publishes **all six relativity curves and
all six positional v0 curves at every pick 1–64**, so a band summary can never again be mistaken for
the wiring. The band table is retained and relabelled *"summary means of the continuous curves"*:

| band | MID | SD | SF | KPD | KPF | RUCK | all-in |
|---|---|---|---|---|---|---|---|
| 1–10 | 1.219 | 0.755 | 0.662 | 0.697 | 0.673 | 1.296 | 1887 |
| 11–20 | 1.266 | 1.069 | 0.625 | 0.628 | 0.845 | 1.142 | 965 |
| 21–30 | 1.294 | 0.763 | 0.491 | 0.678 | 0.890 | 2.257 | 686 |
| 31–45 | 1.306 | 0.497 | 0.680 | 0.772 | 0.766 | 2.375 | 493 |
| 46–64 | 1.098 | 0.621 | 0.901 | 1.834 | 0.918 | 0.878 | 238 |

**Per-position monotonicity is NOT enforced**, per the owner's lean that *"it's quite reasonable for a
position to be 'better than all-in' at some parts of the draft and worse than others."* The domination
argument binds the **all-in** curve (pick N can select whoever pick N+1 would); a positional v0 is a
price **conditional on the position actually taken**, where selection effects legitimately produce
non-monotone shapes. **The ascents are disclosed as data and monotonized nowhere:**

| position | ascending adjacent pairs | where |
|---|---|---|
| MID | 14 | 7→8 … 11→12, 18→20, 24→26, 35→40 |
| SD | 19 | 1→3, 6→8, 9→12, and a long late-draft run 52→64 |
| SF | 21 | 1→3, 26→36, 38→39 … |
| **KPD** | **24** | 1→2, 15→18, 41→48 … — the late-draft KPD rise the owner would expect to see |
| KPF | 13 | 1→2, 10→12, 15→17, 57→64 |
| RUCK | 15 | 1→3, 10→12, 15→23, 26→28 … |

**One disclosed artefact:** the RUCK relativity floors at **0.0000 at picks 63–64** — the per-position
local-linear fit goes negative in the thinnest part of the tail and is floored at zero (the
`kernel_loclin` `floored` flag, which is reported, not silently clipped). It is a thin-cell artefact
of the deepest two picks, it does not affect the all-in curve, and the reconciliation law still holds
at 2.2e−16. **Named here rather than left to be found.**

### 5.6 The pick-64 threshold and the pathway equivalents

| reading | anchored value at pick 64 |
|---|---|
| 26B-V grace-A, pure loclin | 105.8 |
| **CANDIDATE (hybrid + PAVA)** | **179.1** |
| today's landed PVC | 185 |

The owner's *"198-class"* shorthand is the weighted-mean curve anchored on **its own** head
(`190.5 × 1.0127 = 193.0`). On the **ruled loclin head** the same estimator reads **179.1**.
**The difference is the anchoring, not the estimator**, and it is disclosed rather than reconciled
away — the ruling fixed the head at loclin, so the head is loclin.

| pathway | n | anchored all-in | equiv pick, CANDIDATE | equiv, 26B-V | equiv, flat-14 | in/out of 64 |
|---|---|---|---|---|---|---|
| MSD | 29 | 334.6 | 47 | 47 | 45 | INSIDE |
| ND>64 | 114 | 263.9 | 52 | 52 | 50 | INSIDE |
| RD | 611 | 230.6 | 56 | 56 | 54 | INSIDE |
| SSP | 24 | 216.1 | 57 | 57 | 53 | INSIDE |
| PDA | 38 | 187.9 | 61 | 60 | 59 | **INSIDE** (by 5%) |
| UNR | 46 | 124.7 | **>64** | 63 | 62 | **OUTSIDE** |
| PDN | 24 | 111.0 | **>64** | 64 | 63 | **OUTSIDE** |
| PDS | 21 | 101.0 | >64 | >64 | 64 | OUTSIDE |
| IRE | 47 | 94.5 | >64 | >64 | >64 | OUTSIDE |

**Every pathway's own anchored value is unchanged** from 26B-V grace-A — the pool ladder does not read
the ND curve. Only the *equivalent pick label* moves, and that is the entire point of raising the
threshold: **UNR and PDN cross from inside to outside**, joining PDS and IRE.

### 5.7 Pooled aggregates

| metric | **CANDIDATE** | 26B-V grace-A | flat-14 C2 |
|---|---|---|---|
| pooled derived / printed | **0.3477** | 0.3477 | 0.3906 |
| pooled derived / signed ANCHOR | **0.8950** | 0.8950 | 1.0056 |
| n compared | 1200 | 1200 | 1200 |

`|candidate/26B-V − 1| = 0.000e+00` on both. **Pre-registered as a falsifiable claim and it held**:
the boundary and the monotone step move the ND curve and *only* the ND curve. If these had moved, the
boundary would have leaked somewhere it had no business being.

---

## 6. THE BOARD MOVERS PACKET

Full transcript: `MOVERS28_out.txt` / `MOVERS28.json`. **Variant build. Not landed.**

LIVE `88ce647f` (dial off) → VARIANT `0ce52771` (dial on). Same 804 rows both sides.

### 6.1 Totals

| population | live | variant | delta |
|---|---|---|---|
| whole board | 752,429 | 757,152 | **+4,723 (+0.6277%)** |
| the eligible set **E** (75 rows) | 53,426 | 58,129 | **+4,703 (+8.80%)** |
| the 3 indirect movers | 484 | 504 | +20 (+4.13%) |
| **everything else (765 rows)** | 698,519 | 698,519 | **exactly 0** |

### 6.2 Dispersion (never a bare mean)

| | min | p05 | median | mean | p95 | max |
|---|---|---|---|---|---|---|
| relative | −0.21% | +0.83% | **+8.70%** | +8.78% | +13.97% | +14.05% |
| absolute | −1 | +1 | +40 | +121.1 | +409 | +544 |

The ceiling on the pure production leg is `×1.14` — one discount step removed from every future
season. The measured median sits below it because the pedigree pole, `iso_eff`, the position caps and
the numéraire all damp it.

### 6.3 The top 15 movers, named

| # | key | type | pick | entry age | games | before | after | delta | delta % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **willem-duursma** | ND | 1 | 18 | 17 | 3977 | 4521 | **+544** | +13.68% |
| 2 | dyson-sharp | ND | 13 | 18 | 11 | 3091 | 3500 | +409 | +13.23% |
| 3 | sullivan-robey | ND | 9 | 18 | 14 | 2981 | 3381 | +400 | +13.42% |
| 4 | jacob-farrow | ND | 10 | 18 | 16 | 2601 | 2960 | +359 | +13.80% |
| 5 | harry-dean | ND | 3 | 18 | 15 | 2577 | 2935 | +358 | +13.89% |
| 6 | josh-lindsay | ND | 19 | 18 | 12 | 2335 | 2654 | +319 | +13.66% |
| 7 | sam-cumming | ND | 7 | 18 | 13 | 2288 | 2605 | +317 | +13.85% |
| 8 | samuel-grlj | ND | 8 | 18 | 17 | 1735 | 1975 | +240 | +13.83% |
| 9 | cooper-duff-tytler | ND | 4 | 18 | 11 | 1561 | 1779 | +218 | +13.97% |
| 10 | beau-addinsall | ND | 18 | 18 | 6 | 1521 | 1731 | +210 | +13.81% |
| 11 | dylan-patterson | ND | 5 | 18 | 4 | 1628 | 1792 | +164 | +10.07% |
| 12 | talor-byrne | ND | 45 | 18 | 13 | 857 | 976 | +119 | +13.89% |
| 13 | samuel-swadling | ND | 37 | 18 | 5 | 776 | 885 | +109 | +14.05% |
| 14 | louis-emmett | ND | 27 | 18 | 5 | 749 | 849 | +100 | +13.35% |
| 15 | jai-murray | ND | 17 | 18 | 7 | 1138 | 1237 | +99 | +8.70% |

All 39 movers are listed in `MOVERS28_out.txt`, each tagged DIRECT or INDIRECT.

### 6.4 Concentration

| cut | cell | n | delta % | median % |
|---|---|---|---|---|
| **entry age** | 18 | 34 | +10.89% | +8.88% |
| | 19 | 5 | +7.64% | +8.11% |
| **career stage** | 6–14 games | 17 | +12.50% | +11.13% |
| | 15+ games | 5 | +11.48% | +13.80% |
| | 1–5 games | 16 | +7.32% | +7.26% |
| | 0 games | 1 | −0.21% | −0.21% |
| **ND / pool** | ND 1–64 | 30 | +11.04% | +11.13% |
| | pool (SSP/MSD/RD/PDA) | 9 | +7.27% | +7.47% |
| **position** | MID | 11 | +12.13% | +13.42% |
| | KPD | 1 | +13.89% | +13.89% |
| | KPF | 4 | +10.81% | +13.35% |
| | SD | 9 | +8.81% | +7.59% |
| | SF | 14 | +8.79% | +8.47% |
| **pick band** | ND 1–10 | 10 | +11.52% | +13.80% |
| | ND 11–20 | 8 | +11.12% | +11.13% |
| | ND 21–40 | 6 | +8.68% | +8.47% |
| | ND 41+ | 6 | +9.56% | +8.22% |

**The effect concentrates exactly where the owner said it would**: current entry-age-≤19 early-career
players, led by willem-duursma. Depth of the pick matters little; **evidence** matters — a player with
6–14 games moves +12.5% while a 1–5-game player moves +7.3%, because the graced future seasons only
pay where there is a demonstrated level to project.

### 6.5 The control group

The **30 debut-2026 rows at entry age ≥ 20** moved by **exactly zero**. That is the ruled
discrimination, visible in the data rather than asserted in a sentence — `marcus-herbert` (24),
`latrelle-pickett` (20), `mitch-podhajski` (27) and 27 others sit still while their 18-year-old
team-mates rise.

### 6.6 Determinism

<!--DETERMINISM_RESULT-->

---

## 7. THE INSTRUMENTS

Full transcript: `INSTRUMENTS28_out.txt`. Both instruments carry every convention from
`INSTRUMENTS_PRESTATEMENT.md` verbatim — depth axis, dead-zeroed-and-kept, `B = 2000`, seed
`20260812`, 97.5th percentile, thin at n < 40, no FAIL verdict under 8 entrants.

### 7.1 Mark-path progression — **PASS on all 10 arms**

| arm | n@d4 | d0 | d1 | d2 | d3 | d4 | d5 | d6 | peak | at d |
|---|---|---|---|---|---|---|---|---|---|---|
| **ND 1-64** | 1200 | 1.127 | 1.403 | 1.593 | **1.667** | 1.633 | 1.564 | 1.363 | **1.667** | 3 |
| RD | 655 | 1.291 | 1.414 | 1.424 | **1.566** | 1.522 | 1.433 | 1.240 | 1.566 | 3 |
| SSP [thin] | 24 | 1.863 | 1.863 | **2.185** | 1.815 | 1.360 | 0.648 | 0.396 | 2.185 | 2 |
| MSD | 44 | — | 0.958 | 0.921 | 0.865 | 0.969 | **1.325** | 0.570 | 1.325 | 5 |
| IRE | 48 | 1.476 | 1.716 | 1.478 | 1.606 | 1.763 | 1.539 | **2.170** | 2.170 | 6 |
| PDA [thin] | 38 | 0.914 | 1.138 | 1.311 | 1.536 | **1.808** | 0.836 | 1.290 | 1.808 | 4 |
| PDN [thin] | 24 | 1.109 | 1.446 | 1.147 | 1.200 | 1.067 | **1.630** | 1.146 | 1.630 | 5 |
| PDS [thin] | 21 | 1.006 | 0.788 | 0.366 | 0.988 | **1.404** | 1.099 | 0.524 | 1.404 | 4 |
| UNR | 46 | 0.502 | 0.709 | 0.961 | 1.535 | **1.848** | 1.139 | 0.409 | 1.848 | 4 |
| ND>64 | 114 | 1.102 | 1.349 | 1.279 | 1.434 | 1.338 | 1.288 | **1.624** | 1.624 | 6 |

The **MSD debut-year gap** is carried, not rediscovered (ORDER 26A anomaly 5): the emitter builds
`yrs` from draft year + 1 on every route while `cohort()` for MSD is the draft year itself, so MSD's
`d = 0` denominator is empty and its entry reference re-bases on `d = 1`. Printed, not patched.

### 7.2 Reverse no-arb — **PASS on all 10 arms**

No pathway is a systematic guaranteed-loss hold at the candidate entry prices. Smallest
`max m(d≥1)` is **1.3248 (MSD)**, 32% above the failure line; bootstrap upper limits run 1.78 to 5.06.

**Non-vacuity, stated honestly:** limb 1 is red for **no arm** on this basis, so the PASS must be read
as *"every arm clears by a printed margin"*, not as *"a hard test was survived"*. The predicate can go
red — it does so for any pathway whose derived entry price exceeds every mark its cohort ever carries
— but no arm is near it here.

---

## 8. THE PRE-REGISTRATIONS, SCORED

`PREREG_ORDER28.md` and `PREREG_ORDER28_ADDENDUM.md` were both committed and pushed **before** the
code and the numbers they predict existed. Git history is the proof, not this paragraph.

| # | prediction | outcome |
|---|---|---|
| **P1** | movers ⊆ E (75 rows), 60–75 of them, all up, median +6…14%, board total +0.5…1.5% | **PARTIAL BREACH** — see §9.1 and §9.2. Median **+8.70%** ✓, board total **+0.6277%** ✓ |
| **P2** | byte-identity off PASSES | **HIT** — `88ce647f`, exact |
| **P3** | price-function identity bit-exact with the dial on | see §4 |
| **P4** | head/factor/premium and the north/interior curve identical to 26B-V grace-A | **HIT on the anchor** (0.000e+00); **superseded on the interior** by Ruling C, which arrived after P4 was written and legitimately moves picks 6–12 and 15–21 |
| **P5** | seam `p₀ ∈ [50,58]`, zone 6–14 picks, `ν ∈ [0.02,0.06]` | **HIT** — `p₀ = 56`, zone 8, `ν = 0.0290` |
| **P6** | pick-64 anchored ∈ [160, 210], point 183 | **HIT** — **179.1** |
| **P7** | 4–5 pathways outside 64; UNR/PDN/PDS/IRE out, PDA on the boundary inside; pathway values unchanged | **HIT, exactly** |
| **P8** | pooled aggregates identical to 26B-V grace-A | **HIT** — 0.3477 / 0.8950, `0.000e+00` |
| **P9** | reconciliation < 1e−12, C1 asserts pass | **HIT** — 2.220e−16, PASS |
| **P10** | dial-ON board deterministic across two builds | see §6.6 |
| **P11** | duursma's derived v0 unmoved (3157.2) while his board price moves | **HIT** — v0 3157.2 both bases; board 3977 → 4521 |
| **P12** | 6–12 ascents removed, none at pick 1, the owner's 8>6 case among them | **HIT** — 8 ascents, A1 PASS, 6→7→8 among them |
| **P13** | the anchor does not move | **HIT** — 3191.2 / 0.9401 / −6.0% |
| **P14** | weighted total conserved to fp; plain total drifts < 0.5% | **HIT** — both exact |
| **P15** | positional totals move < 2% each | **HIT** — max +0.129% (SF) |
| **P16** | ≥ 2 positions non-monotone per pick; KPD among them | **HIT** — all six are; KPD has 24 ascents |

---

## 9. BREACHES AND ANOMALIES, OWNED

### 9.1 P1 breach — three rows moved outside the eligible set

`shadeau-brain` (+1), `tom-hanily` (+7), `will-mclachlan` (+12). **20 points, 0.0027% of the board.**

P1 predicted **zero**. The channel is identified rather than guessed: `_merged_recover.py` builds its
V0 / cohort-book objects with `MA`'s clock at **historical** years — `rl_export.py:113` re-pins it to
2026 afterwards and says so in its own comment — and at a historical `AGE_REF` a player who is not
first-season in 2026 **was** first-season then. Grace fires inside those builds, and the built
reference objects move with it. That is the ruled *"for backtesting and the live board … for
everything"* behaviour flowing through the same indirect reference-table channel the owner accepted at
#334 stage A (154 indirect movers there). **But the prediction said zero, so it is a breach, and a
landing-time assert is owed: the indirect set must be re-measured and named at landing rather than
rediscovered.**

### 9.2 P1 breach — 39 movers, not 60–75, and one down-mover

**39 of the 75 eligible rows have ZERO career games**, and an un-debuted prospect is priced on
**pedigree alone** (`rl_model.py`: *"unplayed prospects … valued on pedigree alone, like the old
engine"*). His price never enters `proj_from_peak`, so the discount ladder cannot reach him.

> **The dial moves nothing for a 0-game rookie.** What moves him at landing is the **curve**, through
> his pedigree anchor — a different lever with a different ruling. These two must not be conflated
> when reading the movers table.

The single down-mover, `aidan-schubert` (−1, −0.21%), is a 0-game row where a floor or blend leg does
touch the ladder. Stated so the "0-game rows are pedigree-pure" claim is not over-general.

### 9.3 Declared breach — the instruments' marks are off-dial

The instrument **denominators** are re-read on the candidate basis; the **numerators** (`vpath` marks)
come from the pinned walk-forward matrix `per_entrant_O25R4.json`, which was emitted **off-dial**.
A dial-ON matrix re-emit is **not run here** and is named as the follow-up.

The direction of the gap is knowable and is stated: dial-ON marks would be **higher at the shallow
depths only** and unchanged deeper, so every progression above **understates** the rise. **The PASS
shape cannot be manufactured by the gap** — but the gap is real and the follow-up is owed.

### 9.4 Disclosed artefact — RUCK relativity floors at 0 at picks 63–64

The per-position local-linear fit goes negative in the thinnest part of the tail and is floored at
zero (reported by the estimator's own `floored` flag, never silently clipped). A thin-cell artefact of
the last two picks; it does not touch the all-in curve, and reconciliation still holds at 2.2e−16.

### 9.5 The methodological inconsistency, on the record

The curve uses **loclin at the north and the weighted mean in the deep south**. The owner accepted
this explicitly (*"just be inconsistent"*). It is stated here rather than smoothed over in prose,
because a future reader will otherwise ask why one curve carries two estimators. The zone (57–64), the
seam (56), the blend weight at every pick and the method label per pick are all printed in
`DERIVE28_out.txt` §3.

### 9.6 Scope note — the standing gate suite was NOT run

`one_source_selftest.py`, the parity gate, and the movers/transition/preflight suites were **not run**
on this branch. The reason is stated rather than assumed: with the dial off the engine is
**byte-identical** on a full board rebuild (§3), so every one of those gates reads exactly what it
reads on `main` — their verdicts are unchanged **by construction**, not by measurement. That argument
covers the dial-OFF state and nothing else. **Running the full suite with the dial ON is a
landing-time obligation**, and it is listed in §10.

### 9.7 A landing-time item the dial does not yet satisfy

`config_manifest.enforce()` in `bake`/`gate` mode **clears the ambient model environment and rejects
unknown `RL_*` overrides**. `RL_GRACE` is not in `data/model_config.json`. Every build in this packet
ran outside gate mode (as the byte-identity control proves), so nothing here is affected — **but a
canonical landing build will reject the dial until `RL_GRACE` is added to the pinned manifest.**
Named now so it is not discovered at the landing.

---

## 10. WHAT THIS PACKET IS FOR

**NOTHING LANDED.** This packet, together with the remaining landing rulings — **MSD Way B ·
ascents** *(now ruled — Ruling C above)* **· the two n = 0 cells · the numéraire route** — constitutes
**the landing configuration**.

**The 2011-insertions fix order runs FIRST.** It is a store-touching change (unflag `shiel` and
`treloar`, transcribe `cameron` at notional ND-2011 pick 12) and the store is upstream of every
number in this packet. Landing this configuration before that fix would bake a curve derived on an
incomplete 2011 class.

When the owner gives his word, the landing act needs, in one commit:

1. `RL_GRACE` added to the pinned config manifest and defaulted ON (§9.7);
2. the candidate curve and v0s written, and every identity carrier re-pinned in the same act;
3. the **full standing gate suite re-run with the dial ON** — selftest, both parity gates,
   movers/transition/preflight (§9.6);
4. the indirect-mover assert from §9.1 armed, so the indirect set is **named**, not rediscovered;
5. the **dial-ON walk-forward matrix re-emitted** and both instruments re-read on it (§9.3);
6. the movers registry written **only after** the adoption word (the #334 finding-11 lesson: an
   un-adopted board must never be registered, and the column id is poisoned if it is).

**Until then the dial is OFF, the board is `88ce647f`, and the curve of record is the landed PVC.**

---

### Evidence index

| file | what |
|---|---|
| `PREREG_ORDER28.md` | the plumbing design, the seam rule, P1–P11 — filed before any engine byte moved |
| `PREREG_ORDER28_ADDENDUM.md` | the monotone ruling, PAVA spec, A1–A5, P12–P16 — filed before the derivation existed |
| `BYTE_IDENTITY_OFF.md` | the dial-off proof and its non-vacuity control |
| `o28_gate.py` · `GATE28_out.txt` · `GATE28.json` | the identity gate under the dialed engine |
| `o28_derive.py` · `DERIVE28_out.txt` · `DERIVE28.json` | the candidate landing curve and v0s |
| `o28_movers.py` · `MOVERS28_out.txt` · `MOVERS28.json` | the board movers packet |
| `o28_instruments.py` · `INSTRUMENTS28_out.txt` · `INSTRUMENTS28.json` | both committed instruments |
| `DETERMINISM.txt` | the two dial-ON builds |
| `inputs/` | the 26B harness inputs, copied verbatim with md5s, so this branch stands alone |
