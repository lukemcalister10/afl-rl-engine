# PRE-REGISTRATION — ORDER 24B, THE QUALITY-CONDITIONED PREMIUM (ψ = φ·q)

Issue #334. Brief: comment [5266656676](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5266656676).
Branch `build/pool-quality`, cut from `origin/build/pool-dial` @ `254d2e5`.

**COMMITTED BEFORE ANY PAR IS COMPUTED, ANY q IS FORMED, ANY U″ IS DERIVED AND ANY ENGINE LINE IS
EDITED.** Every prediction below is scored in `SUMMARY.md`. A breach is owned by number and by name;
nothing in this file is edited after commit.

---

## 0. What I read before writing this, and what I deliberately did not

**Read (facts, not measurements of the fix):** ORDER 24's `PREREG_ORDER24.md`, `SUMMARY.md`,
`UPRIME_TABLE.md` and its five harness scripts; the landed `_pr_R` / `_pr_U` / `_pr_phi` / `_pr_mult`
block and the two pool read sites in `engine/rl_after/_merged_recover.py`; the signed levels in
`engine/rl_after/pvc_curve_v2.json`; the ORDER 22 class-axis K=10 shrink in
`docs/evidence/pool_final_2026-08-12/o22_make_relaxed_surface.py:109-127` (the shrink convention this
order carries); and — exactly as ORDER 24's prereg sized its own affected population — a **store read
of every pool board row's 2026 games and 2026 scoring average**, together with the ORDER 24 recorded
boards already on disk. That read is population sizing, and it is declared here rather than hidden.

**Not read / not run / not computed:** no par table, no q for any row, no U″ for any pathway, no ψ
board, no ψ surface. The par values, U″ values and ψ prices below are **forward predictions** from the
seat's four reference points, the code, and the store.

**Board identities in force (recorded now so they cannot drift):**

| board | md5 |
|---|---|
| `pre_act` — main @ `7f4d5d2` | `94f1fec59f99c59d5890d5975c79fa9b` |
| `live` — `origin/main` | `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` — committed on `land/pool-update` / this branch | `665311ca72576df6ff0bbf6dfd007739` |
| `a025` | `322df660ccce6c017ded341403b7215f` |
| `a050` | `87214d5653e0fb8e48b804f1a890b6bc` |
| `a100` — ORDER 24's pure delivery fix, this order's CONTROL | `ca3544d8df9272db191a67001a1bb9e4` |

All six are present in the session scratchpad with those md5s, verified before this file was written.

---

## (a) THE PROPOSED WIRING — exact, and pool-gated only

### The defect the owner caught

ORDER 24 fixed *who* the premium reaches (current participation, not career state). It did not touch
*how much*. `_pr_mult` delivers `φ·U` — a **flat** pathway premium — so a pool player who plays badly
and a pool player who plays well collect the same premium per unit of participation.
`harrison-ramm` (MSD, 4 games in 2026 at **28.75**) is lifted 406 → **620** by the full MSD premium,
while `vigo-visentini` (RD ruck, 1 game at **84.00**) collects 150 → **182**, a fraction, because his
participation share is small. The owner's law: *"we don't value players on whether they play, we value
them on how they play."*

### The rule

```
q(p,Y)  =  clip( avg(p,Y) / par(pathway(p), d(p,Y)) , 0, 1 )
M(p,Y)  =  (1-phi) * R(pathway,cls,tau)  +  phi * ( 1 + q * (U''(pathway) - 1) )
```

`ψ` is the composite weight `φ·q` on the premium leg. `φ` is ORDER 24's participation share,
**untouched**. Three limbs, all declared here:

**1. `avg(p,Y)` — the year's scoring average.** Games-weighted across the year's scoring rows
(`Σ avg·games / Σ games`) so a multi-club season reads as one number. **games>0 with a missing or
zero average ⇒ q = 0**, per the order. `games==0 ⇒ φ=0`, so no q exists for that row at all.

**2. `d(p,Y)` — the depth index — is the harvest's own, not a new one.** ORDER 21's harvest defines
`draftyr(p) = cp.debutyr(p) - 1` and `d = Y - draftyr`, so `d = Y - debutyr + 1`, and at an integer
depth the engine's `np.interp(tau, [0..6], [1.0]+dv)` returns exactly `dv[d-1]`. **The par index is
therefore the same integer the retention surface is indexed on**, clipped to `[1,6]` exactly as
`o24_uderive.py:R_of` clips it. It is *not* `Y - store draft year`: the store's draft-year field and
the harvest's debut-derived draft year disagree for late debutants (`harrison-ramm` sits at store d=1
but harvest d=2), and the par must be read on the axis it was built on. **DECLARED, and it is the one
place my convention may differ from the supervising seat's quick cut.**

**3. `par(pathway, d)` — the playing par.** From the SAME complete-window harvest population that
produced `R` (`o24_uharvest.py`'s `WC`: pool careers only, zero national rows, asserted at the gate;
`wc = Y <= 2021`; priceable anchor), restricted to **playing** cells (`games > 0`):

```
par_own(pw,d)   = SUM(avg_y * games) / SUM(games)      over playing cells with that (pw, d)
par_donor(pw)   = SUM(avg_y * games) / SUM(games)      over ALL playing cells of that pathway
w(pw,d)         = n(pw,d) / (n(pw,d) + 10)             n = exact cell count, K = 10
par(pw,d)       = w * par_own + (1-w) * par_donor
```

The K=10 form and the "disclose every cell" discipline are **carried verbatim** from ORDER 22's
class-axis shrink (owner ruling 5262213139, `o22_make_relaxed_surface.py:109-127`): the weight uses
the raw exact-depth `n`, recomputed from the harvest, never transcribed. It is applied at **every**
cell — no thinness threshold, because a threshold would be a new cliff, and the order bars cliffs.
A whole-pool par (`_PR_PAR_ALL`) is derived the same way for rows whose type has no pathway surface.

**4. `U″` — re-derived per pathway so mean preservation holds under the φ·q weights.** Over the same
harvest, entry-weighted by `e = level(division) * _PL_F`:

```
mean = SUM e*[ (1-phi)*R + phi*(1 + q*(U''-1)) ] / SUM e  ==  1.0000000000    (HALT instrument)
=>   U'' = 1 + [ SUM e*(1-phi)*(1-R) ] / [ SUM e*phi*q ]
```

The numerator is **identical** to ORDER 24's U′ numerator, so

```
U'' - 1  =  (U' - 1) * ( SUM e*phi / SUM e*phi*q )  =  (U' - 1) / qbar,     qbar = q-mass ratio <= 1
```

**U″ ≥ U′ for every pathway, always** — premium mass shrinks under q-weighting, so the surviving
premium must be larger to redistribute the same total. Each historical cell carries its **own** q,
from its own year's average against its own cell's par; the harvest gains one field, `avg_y`.

### The two sites

`_pr_mult` is **extended**, not replaced; both existing `p.get('_pool')`-gated call sites are
unchanged in shape. `_pr_phi`, `_pr_R`, `_PR_PATH`, `_PR_WHOLE`, the D12 clock, `_a_share`, `LAM_SIT`,
`_ev_qual`, `_surprise`, `_c_w`, `C_H`, `_h_cut` and `_R_surf` are all untouched. **No national code
path changes.** Sitters (`φ=0`) read `R` and no ψ exists for them. The prior fade (D9) is untouched —
declared, per the brief.

**Levels: FROZEN.** `engine/rl_after/pvc_curve_v2.json` is read from the file as committed on this
branch and is never written; no value from any brief is hardcoded.

---

## (b) THE PREDICTIONS

### Population facts established before predicting (store + the recorded a100 board, 243 pool rows)

| cell | n | can ψ move it? |
|---|---:|---|
| full participants, `gy >= 6*fe` → `φ=1`, anchor share **exactly 0** | 146 | **no** — the multiplier never reaches the price |
| current sitters, `gy == 0` → `φ=0`, `M = R`, no premium leg | 55 | **no** — arithmetically identical to a100 |
| **partial participants, `0 < gy < 6*fe`** | **42** | **yes — and only these** |
| currently-playing pool rows with a missing/zero 2026 average | **0** | (the `q=0` limb is unexercised on this board) |

### Structural predictions

**B1 — CONTROL.** Rebuilding the α=1.0 board on the unmodified branch reproduces
`ca3544d8df9272db191a67001a1bb9e4` byte-identically.

**B2 — SEPARATION.** ND movers (`ty=='ND'`, `ep<=64`) between `live` `1dbd1480` and the ψ board:
**exactly 0**. *(This is the seat's presented expectation S7 as well.)*

**B3 — MEAN PRESERVATION.** All nine pathways and ALL POOL print `1.0000000000` to 1e-9.

**B4 — `U″ ≥ U′` FOR EVERY PATHWAY, WITHOUT EXCEPTION,** and strictly greater wherever that pathway's
q-mass ratio is below 1. Equivalently `(U″−1)/(U′−1) = 1/qbar ≥ 1` on all ten rows.

**B5 — qbar (the q-mass ratio `Σeφq / Σeφ`) lands in [0.65, 0.92] for every pathway.** Reasoning: par
is a games-weighted mean of the same averages q is formed from, so un-clipped `E[q] ≈ 1`; the clip at
1 removes all the upside and none of the downside, so qbar must sit meaningfully below 1 but cannot
collapse.

**B6 — THE ONLY ROWS THAT MOVE a100 → ψ ARE PARTIAL PARTICIPANTS.** All **146** full participants and
all **55** current sitters are byte-identical to `a100`. Any mover outside the 42 is a defect and I
will report it as one.

**B7 — DIRECTION IS DECIDED BY `q` AGAINST `qbar`, NOT BY PRICE.** `M_ψ − M_a100 = φ(U′−1)(q/qbar − 1)`,
so a partial with `q > qbar` **rises** and one with `q < qbar` **falls**, monotonically in q. I predict
this holds on **every one of the 42 rows** with no exception.

**B8 — MOVER COUNT a100 → ψ: [24, 40] of the 42**, of which **at least 18 down** and **at most 16 up**.
The rows that do not move are deep careers whose evidence fade has extinguished the anchor leg
(`reilly-o-brien`, `peter-ladhams`, `adam-saad`, `mitchell-hinge`, `matt-guelfi`, `matt-owies`,
`toby-pink`, `darragh-joyce`, `harry-edwards`, `brandon-zerk-thatcher` are the candidates).

### The par table

**B9 — my predicted pars, before measurement** (games-weighted, post-shrink, on my declared depth
axis). Scored against the measured table cell by cell, ±5%:

| pathway | d1 | d2 | d3 | d4 |
|---|---:|---:|---:|---:|
| MSD | **58** | **62** | **66** | **69** |
| RD | **55** | **62** | **66** | **70** |
| SSP | **58** | **65** | **69** | **72** |
| ND>64 | **56** | **63** | **68** | **71** |

**B10 — PARS RISE MONOTONICALLY WITH DEPTH on every pathway across d1→d4**, because the population at
each depth is the survivors of the one before. Scored per pathway; a single non-monotone step is a
breach for that pathway.

**B11 — RECONCILIATION WITH THE SEAT'S REFERENCE POINTS.** The seat computed, from store md5
`d9a24282`, complete-window ≤2021, `d = Y − draftyr`: **MSD d1 58.9 (n=162) · MSD d2 61.4 (n=174) ·
RD d3 66.5 (n=2,878) · SSP d1 57.7 (n=166)**. I predict my four corresponding cells land **within 5%**
of those four numbers, and that **my cell counts `n` are far smaller** — the seat's `n` cannot be cell
counts on the harvest population (the whole harvest is of order 3,300 complete-window cells, so RD d3
alone cannot be 2,878 cells); I predict the seat's `n` are **games**, not cells, and that my games
totals reproduce them to within 10%. If the par values disagree by more than 5% I will explain the
gap and **not** force agreement.

### U″

**B12 — U″(MSD) ∈ [2.00, 2.25].** *(The seat's presented expectation S5 is ≈ 2.1; mine is the band
around it, derived as `1 + 0.904/qbar` with `qbar ≈ 0.82`.)* U′(MSD) on this branch is **1.9040**.

**B13 — the U″ ordering across pathways is the U′ ordering**, because `U″−1 = (U′−1)/qbar` and qbar
varies far less than U′−1 does. Scored as Spearman-identical ranking of the nine pathways.

### The eight named rows

Store facts, read before predicting: `harrison-ramm` MSD, debut 2025, 4 games @ 28.75, φ=0.7246,
a100 620 · `luker-kentfield` MSD, debut 2026, 3 games @ 32.33, φ=0.5435, a100 496 ·
`vigo-visentini` RD RUCK, debut 2025, 1 game @ 84.00, φ=0.1812, a100 182 · `mani-liddy` 0 games ·
`robert-hansen` 0 games · `nicholas-martin` 0 games · `marcus-herbert` 8 games (φ=1) ·
`jai-newcombe` 21 games (φ=1).

**The seat's presented expectations, recorded verbatim to be scored:**

| # | the seat's expectation |
|---|---|
| **S1** | `harrison-ramm` ≈ **540 ± 30** |
| **S2** | `luker-kentfield` ≈ **420 ± 30** |
| **S3** | `vigo-visentini` ≈ **185 ± 5**, slightly **UP** vs a100's 182 |
| **S4** | `mani-liddy` **168 EXACT** — φ=0, untouched to the point |
| **S5** | `U″(MSD)` ≈ **2.1** |
| **S6** | pool total within **~1%** of a100's **132,734** |
| **S7** | ND movers **0** |

**My own point predictions on top**, computed from the two recorded boards' implied price-per-unit-M
slope and my predicted pars (arithmetic shown so a breach is diagnosable, not just owned):

**B14 — `harrison-ramm` = 563, band [530, 600].** d=2 (debut 2025), par ≈ 62 → q ≈ 0.464;
τ = 1 + 0.92^1.5 = 1.8824 → R(MSD,nonKPP) = 0.4293. `M_a100 = 1.4979`, `M_ψ = 1.2160`.
pr469→a100 was 406→620 across ΔM = 1.0686, so ≈ 200 points per unit M → −56. **This sits at the top of
the seat's S1 band; I predict S1 HOLDS only if the MSD par is nearer 59 than 62, and I am recording
that I expect ramm ABOVE the seat's midpoint.**

**B15 — `luker-kentfield` = 446, band [415, 480].** d=1 (debut 2026), par ≈ 58 → q ≈ 0.557;
τ = 0.8824 → R = 0.5351. `M_a100 = 1.2791`, `M_ψ = 1.1180`, slope ≈ 306 → −49.

**B16 — `vigo-visentini` = 184, band [180, 190], direction UP.** avg 84.00 against an RD d2 par near
62 gives **q = 1.0 after the clip** — he is the row the clip is for. His premium leg therefore moves
from `U′(RD) = 1.2399` to `U″(RD) ≈ 1.28`, and φ=0.1812 makes the move small and positive.

**B17 — `mani-liddy` = 168 EXACT, `robert-hansen` = 143 EXACT, `nicholas-martin` = 3513 EXACT** —
all three are φ=0, so `M = R` with no premium leg at all, and U″ cannot reach them. Byte-identical to
a100, to the point.

**B18 — `marcus-herbert` = 906 EXACT and `jai-newcombe` = 4883 EXACT** — φ=1 gives anchor share
exactly 0, so no multiplier of any kind reaches their prices. Byte-identical to a100 and to `pr469`.

### Which a100 risers fall

**B19 — the fallers, named before measurement.** Of the 24 rows that rose `pr469 → a100`, I predict
these **fall** at ψ (their 2026 average is below ~0.8 × their cell's par):
`caleb-lewis` (12.5) · `matt-hill` (24.0) · `balyn-o-brien` (26.8) · `jacob-newton` (27.7) ·
`harrison-ramm` (28.8) · `hudson-o-keeffe` (29.7) · `tom-cochrane` (30.7) · `noah-howes` (32.0) ·
`luker-kentfield` (32.3) · `aidan-johnson` (34.0) · `thomas-burton` (39.4) · `max-ramsden` (40.5) ·
`wil-parker` (42.4) · `jayden-nguyen` (42.6) · `ben-jepson` (43.3) · `lukas-cooke` (43.5) ·
`ollie-greeves` (44.0) · `mitch-podhajski` (48.5).
And these **hold or rise**: `jaxon-artemis` (54.3) · `liam-reidy` (64.3) · `alex-van-wyk` (69.0) ·
`oliver-francou` (71.5) · `flynn-riley` (80.0) · `vigo-visentini` (84.0).
Scored as a hit-rate over all 24; I predict **≥ 20 of 24 correct**.

**B20 — the largest single faller a100 → ψ is `harrison-ramm` or `luker-kentfield`**, and the largest
single riser is one of `oliver-francou` / `flynn-riley` / `alex-van-wyk`.

### Counts and totals

**B21 — POOL TOTAL.** a100's pool total is **132,734**. Only 42 rows can move and the fallers
outweigh the risers, so I predict the ψ pool total lands in **[131,300, 132,900]** — comfortably
inside the seat's S6 ±1% band `[131,407, 134,061]`, and **below** 132,734.

**B22 — THE TABLE.** `MOVERS_TABLE_PSI.md` carries **[140, 175]** rows (ORDER 24's table had 152; the
ψ column adds materiality only where ψ diverges from a100, which is a subset of rows already in).

**B23 — DETERMINISM.** The ψ board built twice from scratch produces one md5.

---

## (c) Instruments that halt

- **Control mismatch** (B1 fails) → BLOCKER: stop, commit what exists, report.
- **Any mean-preservation cell ≠ 1.0 within 1e-9, any pathway** → HALT, report.
- **Any ND mover on the ψ board** → HARD FAILURE, asserted in code before any table is written.
- **Non-deterministic board build** → BLOCKER.
- **Any `U″ < U′`** → not a halt, but a reported anomaly with its arithmetic, since B4 says it cannot
  happen by construction.

## (d) The absolute-price caveat, carried verbatim into every artifact

> levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing

## (e) Scope fence

Nothing lands. `engine/rl_after/pvc_curve_v2.json` is not modified. The store is not modified. `main`
is not touched, PR #469 is not touched, PR #473 is not touched. The PR opened by this order is based
on `build/pool-dial`. **MERGE NOTHING.**
