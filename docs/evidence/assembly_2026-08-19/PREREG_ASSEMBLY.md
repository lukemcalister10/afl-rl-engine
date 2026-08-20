# PREREG — THE ASSEMBLY BUILD (THE CANDIDATE)

**Seat:** ASSEMBLY BUILD. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Charter:** register `v748` — the go-word. Rulings consumed: `v741`/`v742` (tracking), `v744` (SD
offset standalone, absence package, the cracks inventory), `v745` (mature refit, slope 0.105),
`v746` (F5), `v747` (forbidden-set, mean basis), `v748` (peak principle, recency 0.47, level stays,
modern 1-10 standing red, GO).

**THIS FILE IS PUSHED BEFORE THE FIRST ENGINE EDIT. Nothing below is a result. Every number here is
either a MEASURED CONSTANT taken from a named prior artifact, or a PREDICTION that can be wrong.**

**THE CANDIDATE IS FOR OWNER REVIEW. NOTHING LANDS. NOTHING MERGES. NO PULL REQUEST. NOTHING ON
`main`. THE LIVE BOARD 88ce647f IS NEVER TOUCHED.**

---

## 0 · THE REFERENCE BOARDS, AND WHAT REPRODUCED BEFORE ANY EDIT

| board | id | total | role |
|---|---|---:|---|
| LIVE | `88ce647f` | 752,429 | never touched |
| ORDER K | `f3101883` | 673,097 | the K/landing chain |
| ORDER P | `374d4e44` | 666,434 | the assembly BASE |
| **R = R20A** | **`7f88f509`** | **664,950** | **the owner's reference — the candidate is tracked as Δ R→cand** |

**Reproduced on this seat's worktree BEFORE any edit, from `bbS.sh` unchanged:**

- ORDER P line, every `RL_O38*`/`RL_O39_*`/`RL_O40_*` unset → **`374d4e442665771801c5f1edd2a7e0e2`** ✓
- + `RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20` → **`7f88f5096ff5b781da4614b7142d332c`** ✓
- day-0 assert **89 of 89** on both.

**Instruments pinned and asserted (charter §3):**

| instrument | path | md5 |
|---|---|---|
| extended-338 | `docs/evidence/candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py` | `d59ad550…` ✓ |
| noarb_table_338 | `docs/evidence/landing_29_2026-08-13/noarb/noarb_table_338.py` | `0f822035…` ✓ |
| harness | `docs/evidence/landing_29_2026-08-13/noarb/harness_pvc_REPINNED_pass3.py` | `02dcf28c…` ✓ |
| S4 ruler | (house delivered-value ruler) | `241842f6…` ✓ |

Engine runs are **STRICTLY SEQUENTIAL** with the five-var thread pinning per `bbS.sh`. Thread pins are
printed per run.

---

## 1 · THE DIAL STACK BEING BUILT

Base **ORDER P** (`RL_O37` on the O36-K stack). **LAMBDA UNTOUCHED at the anchor 0.1743833037** —
`RL_O40_LAMBDA` is NEVER set on any candidate build.

| item | dial | value | ruled at |
|---|---|---|---|
| A · FIX A | `RL_O38A` | 1 | v744/v748 |
| B · B1 | `RL_O38B1` | 1 | v748 |
| C · mature refit | `RL_O40_PGMAT` | 1 | v745 |
| D · compressed cap | `RL_O40_CAPFORM` / `RL_O40_CAPPCT` | smooth / 20 | standing + v748 |
| E · slope | `RL_O39_BETASAT` | 0.105 | v745 |
| F · recency | `RL_O40_RECW` | 0.47 | v748 |
| G · SD level offset | **new** `RL_O41_SDOFF` | 2.98 | v744 |
| I · absence package | **new** `RL_O41_CREDIT` / `RL_O41_RESET` / `RL_O41_INJ` / `RL_O41_R3` | see §4 | v744/v748 |

**H · RUCK — NO DIAL. The diagnosis (§3) says the misfiring object is not the one a premium offset
reaches. Nothing is wired for RUCK.**

**Dial-chain identity that must hold: all assembly dials off → `374d4e44` BYTE-EXACT**, and the
K/landing chain (`f3101883`, `1f176444`) intact.

---

## 2 · WHAT IS NOT BEING BUILT, AND WHY — SAID BEFORE THE BUILD, NOT AFTER

- **SF is NOT wired.** T1 read SF **+2.709** (under-barred) but the ruling is explicit: SF held on the
  survivor-bias caveat, and wiring it would hurt exactly the rows the owner cares about. v744.
- **RUCK is NOT wired.** §3.
- **LAMBDA is NOT re-solved.** The level stays at the anchor (v748). The frontier is accepted.
- **The modern 1-10 cell is NOT chased and NOT capped.** It is a DOCUMENTED STANDING RED (v748) and
  rides every table flagged.
- **SSP is NOT repaired.** Inherited breach, worsened by ORDER P, parked (C6), reported separately.
- **G0 / the conviction speed is NOT re-derived.** v746's supervisor disposition, four reasons on the
  record. Logged as a named open finding.
- **C2 (veteran board RL_O33 × B1), C3 (Guard 5), C5, C7, C8, C9** are out of this seat by charter.

---

## 3 · THE RUCK DIAGNOSIS — RUN AT PREREG, BEFORE ANYTHING IS WIRED

**Instrument:** `as_ruck.py`, this directory. Output `RUCK_DIAG_out.txt` / `RUCK_DIAG.json`.
**Population and estimator are T1's, unchanged** — ORDER P's `op_lib.Premium`, games-weighted
local-linear kernel on ln(v0), tricube, h=0.40, isotonised, fitted per class; 5,041 season rows,
1,575 players, 58,488 games, asserted equal to `PREMIUM_SURFACE.json`. Bootstrap **clusters on
player**, B=2,000, seed 32.

**CONTROL — T1 reproduced exactly on this residual:** KPD +0.631 · KPF +0.789 · **RUCK −5.569** ·
MID −0.348 · **SD −2.978** · SF +2.709. Same object.

### The discriminator

The residual is `avg − [ bar(pos, age) + PG(ln v0, class) ]`. **`PG` has no age argument. The C3 age
delta `O32_GATE_DELTA` has no price argument.** So the residual's age profile at fixed price is C3's
to answer for, and its price profile is PG's.

### The three tests

**TEST 1 — the age slope.**

| position | age slope (pts/game per year) | 90% CI | excludes 0? |
|---|---:|---|---|
| **RUCK** | **+5.779** | **[+4.139, +7.630]** | **YES** |
| **SD** (control) | **+0.540** | **[−0.214, +1.293]** | **no** |

RUCK's residual runs **−8.96 at 21 → −5.42 at 22 → +3.84 at 23**, a spread of **+12.80** points a
game across two years. SD's runs between −1.53 and −5.57 with no trend.

**TEST 2 — the price slope, with age partialled out first.** RUCK **+4.128 [+1.246, +6.889]**,
excludes zero — the only position of six that does. **PG's shape is wrong for RUCK as well as its
level**, which a flat offset also would not fix.

**TEST 3 — the repair test.** Two repairs fitted on the same rows, scored by residual sum of squares
removed:

| position | RSS none | RSS after a LEVEL | RSS after an AGE COLUMN | age gain |
|---|---:|---:|---:|---:|
| **RUCK** | 320.76 | 289.75 | 238.27 | **17.76%** |
| **SD** | 238.04 | 229.17 | 227.20 | **0.86%** |

An age column removes **twenty times** more of RUCK's residual than a level does. For SD the constant
has already done the work.

### THE VERDICT

**RUCK'S MISFIRE IS THE C3 AGE-DELTA OBJECT (`O32_GATE_DELTA`), NOT `PG`.** RUCK is pooled into TALL
with KPD and KPF; a ruck develops later, and the pooled column averages two timetables. **A level
offset is the wrong repair** — it would fit the average of a swing and be wrong at both ends: too
generous to a 23-year-old ruck and still too harsh on a 21-year-old.

**PER THE CHARTER: NO PREMIUM OFFSET IS WIRED FOR RUCK.** The finding is reported with its evidence
and `O32_GATE_DELTA` is named as the object a future order would work on.

**SD is the control and it behaves** — its age slope includes zero, so the test can tell flat from
sloped, and SD reads flat. **That is what licenses the SD offset going in standalone and RUCK not.**

**What this diagnosis does NOT claim:** it does not fit a replacement C3 column and it does not price
one. RUCK's age-19 and age-20 cells are thin (below the 40-row floor) and are not read. RUCK holds
the widest pooled interval of the six positions and nothing here narrows it.

---

## 4 · THE ABSENCE PACKAGE — THE EXACT FUNCTIONAL FORMS, PREREGGED

**THE STANDING RULE FOR THIS SECTION: every constant below is copied from a named measured artifact.
Where a form needs a constant no measured curve supplies, THIS SEAT HALTS AND REPORTS rather than
inventing one.**

### 4.1 · I1 — THE CREDIT CURVE (`RL_O41_CREDIT`)

**Replaces** `min(1, games/2)` — the wired per-season played credit.

**Provenance:** `FOLLOWUP_F1.json::iso` — F1's guarded isotonic curve (house pool-adjacent-violators
monotonicity guard, ORDER P's own instrument, 400-draw band), on 1,068 ND entrants 2005-2019 at
depth 2.

| games | credit | wired today |
|---:|---:|---:|
| 0 | 0.0 | 0.00 |
| 1 | 0.1286875208353465 | 0.50 |
| 2 | 0.23834489196711883 | 1.00 |
| 3 | 0.23834489196711883 | 1.00 |
| 4 | 0.23834489196711883 | 1.00 |
| 5 | 0.2455042373957035 | 1.00 |
| 6 | 0.38568558243890977 | 1.00 |
| 7 | 0.38568558243890977 | 1.00 |
| 8 | 0.45188866847720316 | 1.00 |
| 9 | 0.8878514765964253 | 1.00 |
| 10 | 0.8878514765964253 | 1.00 |
| 11+ | 1.0 | 1.00 |

**Form:** `credit(g) = interp(g, the table above)`, linear between integer knots, **held at 1.0 from
11 games**, floored at 0. The existing season proration `_f` multiplies it OUTSIDE, unchanged.
`credit(0) = 0` exactly, so **day-0 prices are untouched by construction.**

**DISCLOSED DECISION — TWO SITES, ONE OBJECT.** The expression `min(1, g/2)` appears at TWO sites:
`o31_played_units` (the charter names this one) and the post-delivery credit loop inside `o31_cu`.
They are the same question — *how much does a season of g games count as played* — and leaving one at
the old step would have the same season credit 0.24 on one clock and 1.00 on the other. **Both sites
take the curve.** This is a deviation from the literal charter text and it is declared here, before
the build, not after.

### 4.2 · I2 — THE GRADED RESET (`RL_O41_RESET`)

**Replaces** the all-or-nothing delivered wipe in `o31_cu` (a delivered season currently zeroes ALL
accrued sitting clock).

**Provenance:** `FOLLOWUP_F2.json::partA.games` — the reversal curve on 134 returners against 760
kept-sitting and 1,704 never-sat rows, scale 0.9347.

| return games | restore fraction `r` | 90% CI | n | wired today |
|---|---:|---|---:|---:|
| 1-2 | 0.17599730114691226 | [+0.053, +0.333] | 38 | 0.0 |
| 3-5 | 0.1690225197655352 | [+0.030, +0.353] | 29 | 0.0 |
| 6-9 | 0.09435725147204567 | [+0.004, +0.214] | 27 | 0.0 |
| 10-14 | 0.21251254122424307 | [+0.054, +0.449] | 22 | **1.0** |
| 15+ | 0.5959292983878227 | [+0.321, +0.886] | 18 | **1.0** |

**Form.** Let `c_pre` be the clock accrued up to and including the delivered season, and `r` the
restore fraction at that season's games. Then

```
c_u  =  (1 - r) * c_pre  +  c_post
```

where `c_post` is the post-delivery clock net of credit, exactly as wired now. **`r = 1` reproduces
today's full wipe exactly**, which is the dial-off identity. `r` is read as a **step function on the
measured bands** — NOT interpolated — because F2's own verdict is that the sample **cannot separate a
step from a smooth curve** (F2-P4's preregistered NULL stands), and inventing a smooth interpolant
would be claiming a shape the measurement declines to supply.

**NO POSITION CUT ON `r`.** F2 has no position cut; the 0.60 is pooled and ruck-specific recovery is
unmeasured (v741). **The tall/small exponent carries through** the existing `o36_kappa` exponent on
`D` in `o31_D`, which acts on the clock this reset produces — so position differentiation continues
to come from the object that measured it, and is not double-applied here.

**F4 ABSORBED — the depth ≥3 shape.** The wired `O31_FADE_D` carries D(3)=0.2748, **D(4)=0.3973 — an
INVERSION resting on an 11-row cell whose mean is 4.9× its median** and whose ordering flips under a
change of `v0` basis (F4 §19). **It is not relied on.** For depth ≥3 the candidate takes the
**UNCONDITIONAL monotone population's row** (`FOLLOWUP_F4.json::readings["UNCONDITIONAL (ORDER 30A)"]`,
strictly monotone down, **154 rows at depth 4**):

| depth | wired today | candidate | source |
|---:|---:|---:|---|
| 1 | 1.0 | 1.0 | unchanged |
| 2 | 0.5582775239783688 | **0.5582775239783688** | **unchanged — the charter scopes this to depth ≥3** |
| 3 | 0.2747857941376827 | **0.21432976349908311** | F4 unconditional |
| 4 | 0.39727085107749216 | **0.10522475297738024** | F4 unconditional |

`O31_FADE_FLAT_FROM = 4` is unchanged. **DISCLOSED:** the unconditional row is a *different
conditioning* (it does not condition on still being listed), and its depth-2 value (0.5684) differs
from the wired one (0.5583). Only depths 3 and 4 are taken, per the charter, so the candidate row
mixes two conditionings at the depth-2/depth-3 join. **That is a real seam and it is declared here
rather than smoothed over.**

### 4.3 · I3 — THE INJURY STREAM (`RL_O41_INJ`) — **LIVE BOARD ONLY**

**Owner-ruled, no backtest.** Pinned input `docs/owner_annotations/SITTER_2026_v1.csv`.

**PINNED INPUT ASSERT: md5 `b26798c35adcd9bda5cef50ff2c884da`, 219 data rows, exactly 37 with
`injured=Y`. If the file is absent or any of these three differ, THE BUILD HALTS LOUDLY.**

**PROVENANCE NOTE, DECLARED:** the file is committed on `main` (`046d853`) and is **not** on
`land/order-29`. This seat brings it onto the branch unmodified and asserts its md5 — it is the
owner's file, byte for byte, not a copy this seat authored.

**Matching rule:** normalise apostrophes and non-alphanumerics to a hyphen key and match to the
engine's own `key`/`player` fields. **Verified before the build: 37 of 37 injured rows match, and
219 of 219 rows overall match.** The build asserts 37/37 and halts otherwise.

**The two-channel design, exactly as ruled:**

1. **DELIVERED players** (a `_yd` exists — they have a delivered season) marked `injured=Y`:
   **the logged-injured absence PAUSES the sitting clock — those weeks accrue nothing.** The live
   year's absence contribution `_fEy(Y,p)` is removed from `c_pre`/`_clk`, floored at 0.
2. **DELIVERED players NOT marked injured:** unexplained absence gets **NO grace year** — the
   entry-style clock, fading continuously via the existing `fE` season fraction. **This is the
   behaviour as wired**; the two-channel law makes it the explicit default rather than a side effect.
3. **Rookies / never-delivered rows:** **CAUSE-BLIND, UNCHANGED.** Owner-ruled — the same penalty
   either way. **No annotation is read for a row with no delivered season**, whatever its `injured`
   flag says.

**SCOPE, DECLARED:** the annotation is a **2026 log**. It carries no statement about earlier seasons.
So the pause applies to the **live year's** absence only. Extending it backwards would be inventing
injury history the owner did not write. The dial is inert on every non-live evaluation year, which is
what "live board only, no backtest" means mechanically.

### 4.4 · I4 — THE R3 PRODUCTION FADE (`RL_O41_R3`)

**The owner:** *"his production leg should fade with 2 seasons out."* Conway is the exhibit, never the
target.

**Attachment point:** the finished production leg `e` at the ORDER 30B-P blend site — after the D8
graded staleness, the ruck ceiling and the ITEM H cuts have all been applied, i.e. the point where
`e` is the production leg and nothing downstream re-reads it.

**THE SIZING LAW IS THE OWNER'S R1 COMBINED-TAKE LAW: ONE CALIBRATED TOTAL, HOWEVER MANY
COLLECTORS.** The target is not this seat's choice — it is F3's measured cost of absence:

**Provenance:** `FOLLOWUP_F3.json::dcurve` — the seat's own re-measurement on the house ruler, NOT a
read-back of the wired schedule (which would be circular).

| depth c | unplayed seasons | measured cost `1 − D` | 90% CI | n |
|---:|---:|---:|---|---:|
| 2 | 1 | **0.36723755424736493** | [+0.201, +0.513] | 463 |
| 3 | 2 | 0.7628696536230766 | [+0.680, +0.836] | 242 |
| 4 | 3 | 0.8883339330826462 | [+0.822, +0.947] | 161 |
| 5 | 4 | 0.945109511421381 | [+0.872, +0.994] | 132 |

**Form.** For a row at unexplained depth `c_x` (the clock of §4.2/§4.3, injured time already removed):

```
target(c_x)     = interp(c_x, the F3 cost curve), flat from depth 5, ZERO below depth 2
taken_already   = (the pedigree-fade take + the D8 staleness take) / the absence-free price
residual        = max(0, target(c_x) - taken_already)
R3 factor on e  = 1 - min(1, residual * price_absence_free / production_leg)
```

- **Zero below depth 2 by construction** — F3 cannot speak about depth 1 (it is the normaliser), and
  the owner's words are "2 seasons out". `c_x < 2` ⇒ factor 1.0 ⇒ **day-0 and one-season-out rows are
  untouched.**
- **The D8 overlap reconciles by construction.** `taken_already` includes D8, so the 8 double-priced
  rows of F3 §12 collect the one fact ONCE, at the calibrated total. This is the reconciliation the
  charter asks for — not a subtraction bolted on afterwards.
- **`price_absence_free` is computed in-engine** by evaluating the same row with the two existing
  absence collectors neutralised (`D → 1`, D8 release → 1). It is a reference quantity, never a
  price that is written.
- **INJURED-ANNOTATED ROWS ARE EXEMPT** — the two-channel law. Their `c_x` excludes the paused time,
  and a row whose entire absence is logged-injured has `c_x < 2` and therefore factor 1.0.

**THE STRUCTURAL CEILING IS RESPECTED AND REPORTED, NOT ASSUMED AWAY.** F3 §15 published that in
three of four `c_u` bands the CEILING of both existing collectors sits **below** the lower limit of
the measured cost — no setting of the sitter fade and no size of the D8 cap can reach it. **The
production leg is the collector that can reach**, which is exactly why R3 exists. The packet will
report, per band, the achieved total take against the measured cost and against that ceiling.

**THE LIMITATION F3 STATED, CARRIED FORWARD:** a row whose absence already depressed his production
leg has paid somewhere these attributions do not count, so F3's gap is an **UPPER bound** on the
shortfall. **The candidate therefore CAPS the R3 factor so the total take can never EXCEED the
measured cost's point estimate** — `min(1, …)` above — and the packet reports where the cap binds.

**THIS IS THE ONE PLACE THIS SEAT COULD HAVE INVENTED A CONSTANT AND DID NOT.** There is no free
parameter in the form above: the target curve is measured, the taken-already is computed, and the
allocation to the production leg is the owner's R3 ruling. **If the build finds the form needs a
constant the measurement does not supply — for instance if `price_absence_free` cannot be formed
for some row class — THIS SEAT HALTS AND REPORTS rather than picking a number.**

---

## 5 · PREDICTIONS — THESE CAN BE WRONG

**P1 · The dial-chain identity holds.** All assembly dials off → `374d4e44` byte-exact, and
`f3101883` / `1f176444` intact. *(If this fails the build is void.)*

**P2 · Mature rows.** B1 + the mature refit move mature rows by about **−7,064** board points before
interactions. **The built number will differ** because six other levers are live. **Predicted built
total movement on mature rows: between −5,000 and −10,000.** Reported built-vs-expected loudly either
way.

**P3 · Board total.** The candidate lands **below R (664,950)**. The absence package only ever takes
away, the SD offset takes away, and the compression takes away; recency and the mature refit move
both directions. **Predicted candidate total: 630,000 to 660,000.** A total ABOVE R falsifies my
understanding of the stack and I will say so.

**P4 · The tail calibration reads near F5's ~1.04.** v746 computed that BETA_sat 0.105 + the p20 cap
land the measured tail at **≈1.04** (floor alone 1.62, floor+p20 1.04) against the wired 1.90. **On
the real candidate board I predict the deep-underperformer cell reads between 0.90 and 1.25.**
Outside that band I report the miss loudly rather than reframing the benchmark.

**P5 · Year-1 class.** The W2 mark on the **REGISTERED basis (draft classes 2005-2015, ENTRY_FLOOR
2005 — NOT `ok_class.py`'s 2004-2014 window)** stays inside **[1.03, 1.14)**. This is an ACCEPTANCE
gate, not just a prediction: a breach HALTS.

**P6 · Censuses.** Burn census **0** of all young rows (Fix A) and birthday census **0 at every age**
(B1), as ORDER Q measured. A non-zero census HALTS.

**P7 · The credit curve is the largest single absence lever**, because it touches every row with a
short season rather than the handful the reset reaches. F2 measured only **6 rows** with anything
riding on the delivered cliff, worth **201 points** in total. **Predicted: I1 moves more board points
than I2.**

**P8 · The injury stream moves few rows and only downward-sparing ones.** 37 annotated injured rows,
of which only those with a delivered season are eligible. **Predicted: fewer than 25 rows move, all
upward** (a pause can only remove clock).

**P9 · R3 is the biggest absence collector by points**, because F3 found the existing take undershoots
in every band and the structural ceiling blocks the others. **Predicted: R3 moves more than I1, I2 and
I3 combined.**

**P10 · Modern picks 1-10 still fails the loosened path test.** No lever in this assembly reaches it
(S3 proved lambda cannot; recency structurally cannot). **It is a DOCUMENTED STANDING RED and will be
flagged in every table, not chased and not capped.**

---

## 6 · FALSIFIERS — EACH ONE HALTS THE BUILD AND IS REPORTED

| id | fires if | consequence |
|---|---|---|
| **A-F1** | all assembly dials off does NOT reproduce `374d4e44` byte-exact | **VOID** — nothing else is believable |
| **A-F2** | the K/landing chain (`f3101883`, `1f176444`) moves | **VOID** |
| **A-F3** | day-0 ENTRY values are not bit-identical **89/89** | HALT |
| **A-F4** | determinism: any board differs on an identical repeat | HALT |
| **A-F5** | burn census ≠ 0 on any young row | HALT |
| **A-F6** | birthday census ≠ 0 at any age | HALT |
| **A-F7** | any row prices ABOVE its uncharged price | HALT |
| **A-F8** | continuity breaks on any axis, **including age 23/24 and the season turn** | HALT |
| **A-F9** | year-1 class W2 mark outside **[1.03, 1.14)** on the REGISTERED basis | HALT |
| **A-F10** | `SITTER_2026_v1.csv` absent, or md5 ≠ `b26798c3…`, or ≠ 37 injured rows, or < 37/37 matched | HALT |
| **A-F11** | the credit curve is non-monotone or exceeds 1.0 at any games count | HALT |
| **A-F12** | `RL_O41_RESET` at its identity setting (`r ≡ 1`) does not reproduce the pre-reset board byte-exact | HALT |
| **A-F13** | `RL_O41_CREDIT` at its identity setting (`min(1,g/2)`) does not reproduce byte-exact | HALT |
| **A-F14** | the R3 factor is < 0, > 1, or non-1.0 on any row with `c_x < 2` | HALT |
| **A-F15** | the R3 total take EXCEEDS the measured cost point estimate on any band | HALT (the cap failed) |
| **A-F16** | the injury stream moves any row DOWNWARD, or moves any never-delivered row at all | HALT |
| **A-F17** | LAMBDA is not the anchor `0.1743833037` on the candidate | HALT |
| **A-F18** | the R9/R10 asserts on THETA_R/TMAX fail at `BETA_sat = 0.105` | HALT |
| **A-F19** | a form needs a constant no measured curve supplies | **HALT AND REPORT — do not invent** |

**On any halt: report, do not trade laws silently.**

---

## 7 · ACCEPTANCE, RESTATED

- Year-1 class W2 mark in **[1.03, 1.14)** on the REGISTERED basis (2005-2015, ENTRY_FLOOR 2005).
- Burn census **0** of all young rows · birthday census **0** at every age.
- **No row above its uncharged price.**
- Day-0 ENTRY values **bit-identical 89/89** · **determinism ×2**.
- **Continuity on every axis INCLUDING age 23/24 and the season-turn axis.**
- **Mature-row movement fully reported** — built vs the ~−7,064 expectation, loudly, with interactions
  named.
- **The tail calibration REPORTED against F5's expectation ~1.04.**
- **MODERN PICKS 1-10 = a DOCUMENTED STANDING RED**, flagged in every table, not chased, not capped.
- **SSP reported separately** (inherited breach). The owner's loosened-rail **PATH TEST** scored on
  every breaching cell (yr0-7 path vs compounding 14% carry).
- **Dial-chain identities:** all assembly dials off → `374d4e44` byte-exact; K/landing chain intact.

---

## 8 · DELIVERABLES THIS PREREG COMMITS TO

1. **This prereg**, pushed before the first engine edit.
2. **THE CANDIDATE** board + `PACKET_ASSEMBLY.md`.
3. **THE TRACKER** (v741/v742): all-moved-rows HTML — live · K · Δlive→K · P · ΔK→P · R(`7f88f509`) ·
   ΔP→R · CANDIDATE · ΔR→cand · **Δlive→cand** · ΔK→cand; absolute points; every column sortable;
   board totals in the header; plus CSV.
4. **THE PER-LEVER BREAKDOWN** (separate HTML): R → +recency → +compression+slope → +mature refit →
   +SD offset → +absence package (sub-parts separable where the dials allow), each lever's marginal
   board and named-row effect, built from the dial stack, **strictly sequential builds**.
5. **The three owner documents** in the standing format: the 804-row player list with mechanism legs ·
   the year-1 class in draft order · the no-arb tables (five bands + ALL/1-20/21-64, **BOTH windows**,
   pool arms both windows, both baselines) — each carrying the plain-words **"what is in this board
   and what is still broken"** box, with the modern 1-10 red and SSP named in it.
6. **The movers ledger JSON.**

**CONVENTIONS:** plain speech · **no named-player targets** (Pickett/Conway/Travaglia/Sims illustrate,
never gate) · nulls as nulls · say what was NOT built and why · thread pins printed per run ·
built-vs-estimated reported loudly wherever a prior estimate exists.
