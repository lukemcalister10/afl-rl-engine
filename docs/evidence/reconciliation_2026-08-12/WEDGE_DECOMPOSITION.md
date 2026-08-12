# WEDGE DECOMPOSITION — ORDER 26A

The act's central question, quantified: of the ~2–3× entry-vs-marks wedge, how much is
**(i) ENTRY-INFLATION** from the `realised_full` calibration basis, and how much is
**(ii) MARK-SUPPRESSION** of living pool players?

Scripts: `o26a_wedge.py` → `WEDGE.json` / `WEDGE_out.txt`; `o26a_timing.py` → `TIMING.json` /
`TIMING_out.txt`. Read-only throughout.

**The short answer: it is entry-inflation and MORTALITY. There is no mark-suppression of living
pool players — the measured effect runs the other way.**

---

## 1. THE TWO ENTRY-PRICE OBJECTS

| arm | Σ board v0 | Σ signed anchor | inflation v0/anchor |
|---|---|---|---|
| NATIONAL (ND 1–64, n=1443) | 1,216,754 | 1,216,754 | **1.0000** |
| ALL POOL (n=1200) | 793,355 | 308,185 | **2.5743** |
| RD (n=691) | 503,673 | 189,892 | **2.6524** |

For a national row the two objects are identical by construction. For a pool row they are not, and
the whole wedge lives in that difference.

**Why the inflation exists.** The signed levels were derived in ORDER 25 on the **CAREER PROFILE**
metric — `Σ realised_full / Σ entry` — and that derivation lands ALL POOL at 0.9898 against the
national target 0.9900, a ratio of 0.9998. `realised_full` is a `pw`-weighted mean over the whole
of a player's `vpath` with the never-established scored 0.0
(`harness_pvc_REPINNED_pass3.py:313`). So the signed anchor is, by construction, **the price at
which a pool entrant's whole-career realised value matches a national entrant's**. The board's v0
surface is a different object fitted to a different thing, and on the same career-profile metric it
reads **0.3845** for ALL POOL against 0.9900 national — i.e. the board's v0 over-prices a pool
entrant by 2.57× relative to what pool careers actually realise. **That is the entry-inflation, and
it is real.**

---

## 2. TRAJECTORIES — BOTH AXES (H4)

`SURV` = survivors only (non-zero mark) over **their own entry** — the owner's convention.
`ALL` = dead zeroed and kept — the derivation's convention.

### CALENDAR axis (cohort year N)

| N | NATIONAL ALL | NATIONAL SURV | n_surv | RD@v0 ALL | RD@v0 SURV | RD@anchor ALL | RD@anchor SURV | n_surv |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.0517 | 1.0517 | 1443 | 0.4289 | 0.4289 | 1.1376 | 1.1376 | 691 |
| 2 | 1.3076 | 1.3076 | 1385 | 0.4702 | 0.4724 | 1.2481 | 1.2534 | 682 |
| 3 | 1.4876 | 1.5526 | 1170 | 0.4722 | 1.0502 | 1.2542 | 2.7712 | 305 |
| **4** | **1.5547** | **1.7452** | 982 | **0.5207** | **1.3328** | **1.3798** | **3.5047** | 261 |
| **5** | **1.5250** | **1.8571** | 842 | 0.5018 | 1.5176 | 1.3362 | **3.9442** | 221 |
| 6 | 1.4607 | 1.9317 | 715 | 0.4749 | 1.6792 | 1.2598 | 4.2005 | 193 |
| 7 | 1.2697 | 1.8128 | 613 | 0.4139 | 1.5851 | 1.0893 | 4.0058 | 171 |

### CAREER-AGE axis (seasons since the player's own first playing season)

| a | NATIONAL ALL | NATIONAL SURV | n_surv | RD@v0 ALL | RD@v0 SURV | RD@anchor ALL | RD@anchor SURV | n_surv |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.2103 | 1.2103 | 1250 | 0.8596 | 0.8596 | 2.1759 | 2.1759 | 379 |
| 2 | 1.4347 | 1.4607 | 1149 | 0.8765 | 0.9754 | 2.2229 | 2.4295 | 344 |
| 3 | 1.5518 | 1.6455 | 1019 | 0.9685 | 1.3119 | 2.4498 | 3.3461 | 270 |
| **4** | **1.6417** | **1.8310** | 887 | 1.0407 | 1.6053 | **2.6191** | **4.1627** | 227 |
| 5 | 1.6005 | 1.9272 | 765 | 0.9611 | 1.7239 | 2.4068 | 4.3910 | 195 |
| 6 | 1.5125 | 1.9632 | 661 | 0.8628 | 1.7468 | 2.1643 | 4.4164 | 171 |
| 7 | 1.3059 | 1.8101 | 563 | 0.7167 | 1.5384 | 1.7862 | 3.8944 | 155 |

### The composition trap in the career-age axis — disclosed, not smoothed

The career-age axis has no year for a man who **never played**, so he silently leaves it.

| arm | n | ever played | never played |
|---|---|---|---|
| NATIONAL | 1443 | 1250 (86.6 %) | 193 (13.4 %) |
| ALL POOL | 1200 | 685 (57.1 %) | 515 (42.9 %) |
| RD | 691 | 379 (54.8 %) | 312 (45.2 %) |

RD loses 45.2 % of its rows to that axis and NATIONAL only 13.4 %. Reading the raw axis switch as
"timing" would hand the pool a survivorship windfall of roughly 0.50× and call it a debut offset.
**It is not timing. It is composition.** The timing leg below is therefore measured by reweighting,
not by switching axes.

---

## 3. THE TIMING LEG (iii), MEASURED PROPERLY

Entry-weighted career-age mix of the rows **alive at calendar N=4**:

- NATIONAL: mean career age **3.481** (n=976)
- RD: mean career age **3.061** (n=261)
- the pool is **0.419 seasons earlier in career time** at the same calendar year

The national survivor own-entry curve by career age is the yardstick:

| a | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| NATIONAL SURV | 1.2103 | 1.4607 | 1.6455 | 1.8310 | 1.9272 | 1.9632 | 1.8101 |

- yardstick on the NATIONAL's own career mix: **1.7668**
- yardstick reweighted onto the POOL's career mix: **1.6923**
- **TIMING LEG (iii) = 1.7668 / 1.6923 = 1.0440×**

The debut offset is real, legitimate, and **small: 4.4 %**. The brief's expectation of a 1–2 year
offset is not what the data shows — the measured first-play offset from cohort is +0.502 seasons
national, +0.773 seasons RD, a difference of only **0.27 seasons**, and 0.419 seasons once
entry-weighted at N=4.

---

## 4. THE DECOMPOSITION

Multiplicative, split in log space so the shares sum to 100 %. Exact — the check residual is
0.00e+00 on both lines.

### On the derivation's own convention (ALL-IN, dead zeroed and kept), calendar N=4

| leg | factor | share |
|---|---|---|
| **TOTAL WEDGE** ND 1.5547 / RD@board-v0 0.5207 | **2.9857×** | 100.0 % |
| **(i) ENTRY-INFLATION** RD@anchor 1.3798 / RD@v0 0.5207 | **2.6498×** | **89.1 %** |
| **(iii) TIMING** yardstick as-read / reweighted | **1.0440×** | **3.9 %** |
| **(ii) MARK-RESIDUAL** the remainder | **1.0793×** | **7.0 %** |

### On the owner's convention (SURVIVORS' own entry), calendar N=4

| leg | factor | share |
|---|---|---|
| **TOTAL WEDGE** ND 1.7452 / RD@board-v0 1.3328 | **1.3094×** | 100.0 % |
| **(i) ENTRY-INFLATION** RD@anchor 3.5047 / RD@v0 1.3328 | **2.6295×** | +358.6 % |
| **(iii) TIMING** | **1.0440×** | +16.0 % |
| **(ii) MARK-RESIDUAL** | **0.4770×** | **−274.6 %** |

The negative share is not an artefact. It says the entry rederivation **overshoots the whole wedge
on this convention**: a mark-residual of 0.4770 means pool survivors, once entry is restated on the
signed anchor, read **2.097× the national survivor yardstick** at matched career age. Living pool
players are marked *generously*, not suppressed.

**Answer to the act's central question, in the terms it was asked:**

- **(i) ENTRY-INFLATION: 89.1 %** of the wedge on the all-in convention, and **more than 100 %** of
  it on the survivors' convention.
- **(ii) MARK-SUPPRESSION: 7.0 %** on the all-in convention (a 1.0793× shortfall — pool marks 7.9 %
  below the national line after the entry fix), and **NEGATIVE — −274.6 %, i.e. mark ELEVATION of
  2.097×** — on the survivors' convention.

---

## 5. WHY THE TWO CONVENTIONS DISAGREE: THE MORTALITY IDENTITY

For any arm at any year, exactly (the dead contribute 0 to the numerator and their entry stays in
the denominator):

```
ALL-IN  =  SURVIVORS' own-entry  ×  SURVIVING ENTRY SHARE
```

At calendar N=4:

| arm | ALL-IN | SURV | alive entry share | check |
|---|---|---|---|---|
| NATIONAL (v0 = anchor) | 1.5547 | 1.7452 | **89.09 %** | 1.554717 |
| RD @ signed anchor | 1.3798 | 3.5047 | **39.37 %** | 1.379793 |
| RD @ board v0 | 0.5207 | 1.3328 | 39.07 % | 0.520725 |
| ALL POOL @ signed anchor | 1.3381 | 3.2532 | 41.13 % | 1.338050 |
| ALL POOL @ board v0 | 0.4999 | 1.2009 | 41.63 % | 0.499940 |

**The whole story in one line.** Pool survivors are marked **2.008×** the national survivors' level
relative to entry, but only **0.442×** as much of the pool's entry survives to year 4. The two
nearly cancel: 2.008 × 0.442 = 0.887 — which is exactly the 1.3798 / 1.5547 = 0.887 the derivation
reads.

**The pool board is barbell-shaped against the national board.** Far more of it dies; what lives is
marked far higher per unit of signed entry. The signed levels have already absorbed that trade,
because `realised_full` is an all-in career average that carries the deaths at 0.

---

## 6. WHAT THIS MEANS FOR ORDER 26B

### Does the entry rederivation alone deliver the ND-like curve?

**On the all-in convention — the convention the signed levels are actually derived on — YES,
essentially.** The pre-registered decision rule (`PREREG_ORDER26A.md` §4) set "materially" at ±15 %.
After the entry rederivation, RD reads 1.3798 against the national 1.5547 at year 4 — **11.3 %
below** — and once the 4.4 % timing offset is removed, **7.9 % below**. That is inside the band.
**The marks owe at most a ~8 % correction, and the honest reading is that they owe nothing that can
be distinguished from the timing and composition noise around it.**

Year by year, the post-entry all-in gap (national ÷ RD@anchor): N=3 1.186×, **N=4 1.127×**,
N=5 1.141×, N=6 1.160×, N=7 1.166×. Stable, single-digit-to-low-teens percent, always the same
sign. It is a level effect of order 10 %, not a 2–3× wedge.

### Is there a mark correction owed?

**No — and 26B must be warned off the opposite conclusion.** The wedge the owner identified is
**not** entry-inflation plus mark-suppression. It is entry-inflation (89 %) plus a small legitimate
timing offset (4 %) plus a small residual (7 %). Applying a mark uplift to living pool players on
top of the entry rederivation would push pool survivors from 3.50× their signed entry — already
**2.0× the national survivors' 1.75×** — further above the national line.

### The real hazard for 26B

The hazard is not suppression, it is **the convention switch**. If 26B rederives entry on the
signed anchor and then reads the result on a **survivors'** basis — which is the natural thing to
do when looking at a live squad, because dead players are not on it — the pool will read **~3.5×
entry at year 4 against the national ~1.75×**, and every living pool player will look like a
bargain by a factor of two. That is not a bargain. It is the mortality the all-in calibration
already charged for, reappearing as apparent alpha because the dead were dropped.

**Concretely, for 26B:** the entry rederivation is sufficient and should be shipped on its own. Any
mark correction should be **zero** unless it is derived on the same all-in convention as the levels,
in which case its size is at most **1.08×** (7.9 % uplift to pool marks) and it is inside the noise
of the timing and composition effects measured here. **The number 26B must NOT use is a ~2× uplift
inferred from a survivors' reading.**

---

## 7. THE OWNER'S YARDSTICK (H4), MEASURED

The brief's yardstick was: "computed on the own-entry convention, ND survivors at yr4–5 read
≈ 2.2–3.1× their own entry (1.55 ÷ 0.5–0.7 surviving entry share)."

| measure | value | vs 2.2–3.1 band |
|---|---|---|
| NATIONAL survivors' own entry, calendar yr4 | **1.7452** (n=982) | **BELOW BAND** |
| NATIONAL survivors' own entry, calendar yr5 | **1.8571** (n=842) | **BELOW BAND** |
| NATIONAL survivors, career-age a=4 | **1.8310** | **BELOW BAND** |
| NATIONAL survivors, career-age a=5 | **1.9272** | **BELOW BAND** |

The band was built on an assumed national surviving-entry share of 0.5–0.7. **The measured share is
0.8909** — the national arm's mortality is far lower than assumed, and the yardstick is
correspondingly lower: ~1.75–1.93×, not 2.2–3.1×. The lower yardstick makes the pool's post-entry
position *better*, not worse, and strengthens §6's conclusion.

Pool vs national survivor own-entry trajectories, side by side:

| | calendar yr4 | calendar yr5 | career-age a=4 | career-age a=5 |
|---|---|---|---|---|
| NATIONAL survivors | 1.7452 | 1.8571 | 1.8310 | 1.9272 |
| RD survivors @ signed anchor | **3.5047** | **3.9442** | **4.1627** | **4.3910** |
| RD survivors @ board v0 | 1.3328 | 1.5176 | 1.6053 | 1.7239 |
| RD @ anchor ÷ NATIONAL | **2.008×** | **2.124×** | **2.274×** | **2.278×** |

On both axes, at both years, and on the survivors' convention the owner specified: **the pool's
survivors sit roughly twice the national line once entry is restated on the signed anchor.**
