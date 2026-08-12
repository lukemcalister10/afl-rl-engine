# ORDER 20B — ADOPTION EVIDENCE FOR THE PAR ARM-SPLIT FIX

> **Measurement only.** No shipped default is changed, no board is promoted, `data/expected_boot.json`
> is not restamped. Branch `build/par-adoption-evidence`, cut from `origin/main` `9ecc4e9`.
> Pre-registration `PREREG_ORDER20B.md`, committed at `4cda93b` **before any measurement was run**.

Subject: the ORDER 20 arm-split fix (`build/nd-pool-separation` `78d5c38`, PR #457) on
`engine/forward_valuation/par_build.py` + `par_redesign.py`.

**Pins asserted at entry and exit, all three UNMOVED:**
board `94f1fec59f99c59d5890d5975c79fa9b` (rebuilt from `origin/main`, reproduced exactly) ·
store `d9a24282357cf3083b1640466e3ecd83` · instrument `noarb_table_338.py` `0f8220351c64c56ccfa90c60edcdfa5f`.

**CONTROL — the harness is anchored to the board the owner is deciding about.** The in-process engine
reproduces ORDER 20's committed `BOARD_DELTA_par_armsplit.json` exactly: national n=668, movers 279,
624418 → 622650 (−1768); pool n=334, movers 195, 123939 → 126244 (+2305); and every named mover's
before/after to the unit. (PREREG P21 — TRUE.)

---

## THE FOUR RESULTS THAT SHOULD DRIVE THE DECISION

1. **A par consumer ORDER 20 never named carries a third of the national board move.**
   `par_redesign.lvl_par:126` — bound as `cp._lvl_eff` by `wire_redesign.build()` and frozen as
   `cp._lvl_eff_orig` at `_merged_recover.py:171`, read as `Lo` in the live level core at `:571` and
   into the conditional-prior band features at `:368`. It is the **highest-traffic par consumer on the
   board** (38,159 calls against 18,002 for the pedigree blend) and it is absent from ORDER 20's
   sixteen-site sweep. It carries **−545** of the −1768 national delta, and it is the **dominant**
   channel for three of the five >15% movers.

2. **`BASE_RATE` is dead on the board path — it contributes EXACTLY ZERO.**
   `shortfall()` / `BASE_RATE` / `tilt_band()` have no consumer outside `par_redesign.py`'s
   `if __name__=='__main__'` report block (repo-wide grep). The one-at-a-time switch measures **+0**
   on every row and on the whole national arm. ORDER 20's summary attributes part of the shallow-pick
   movement to `BASE_RATE`; that attribution is wrong, and the order's Dean hypothesis rests on it.

3. **The v0 the board actually consumes does not move for national rows at all.**
   `v0_start` on the board path returns the D14 surface, whose signature (`_v0surf_sig`) hashes
   {pick curve, roster, gate env} and takes **no par input**; the lens fits from the #279 basis
   artifact × the PVC anchor, and ORDER 20 measured the PVC curve 0/64 moved. National `v0_start`:
   **0 of 668 rows move.** What moves is `_v0_uncapped`/`_v0_raw` (−3.25% national) — latent, off the
   board, but it is what the ruck cap reads.

4. **The definitive post-adoption `nd_profile` is `0.9900060981`, not the published `0.9944115616`.**

---

## TASK 1 — v0 DELTAS UNDER THE FIX

Instrument `scripts/engine_probe.py` → `scripts/v0_delta.py`. Population: the **1002 rows the board
carries** (active 804 + back 198) = the population `BOARD_DELTA_par_armsplit.json` scored.
Full tables `v0/V0_DELTA.txt`, machine-readable `v0/V0_DELTA.json`.

### By arm

| quantity | arm | n | movers | total before | total after | delta | pct |
|---|---|---|---|---|---|---|---|
| `v0_start` | NATIONAL | 668 | **0** | 646 599.0 | 646 599.0 | 0.0 | **0.0000%** |
| `v0_start` | POOL | 334 | 300 | 138 179.5 | 209 292.9 | +71 113.4 | **+51.4645%** |
| `_v0_uncapped` | NATIONAL | 668 | **668** | 773 743.8 | 748 627.9 | −25 115.9 | **−3.2460%** |
| `_v0_uncapped` | POOL | 334 | 334 | 144 540.6 | 226 125.7 | +81 585.2 | +56.4445% |
| `_v0_raw` | NATIONAL | 668 | 662 | 773 081.9 | 747 078.8 | −26 003.1 | **−3.3636%** |
| `_v0_raw` | POOL | 334 | 300 | 138 179.5 | 209 292.9 | +71 113.4 | +51.4645% |

**Read this carefully.** `v0_start` is the number the board consumes; `_v0_uncapped`/`_v0_raw` are the
pre-curve quantities. The national arm's board-consumed v0 is **inert**, and its uncapped v0 falls
**3.25%**. The pool arm's board-consumed v0 rises **51.46%**.

### `v0_start` by arm × position

| arm | pos | n | movers | delta | pct |
|---|---|---|---|---|---|
| NATIONAL | MID / SD / SF / KPD / KPF / RUCK | 193 / 142 / 150 / 72 / 84 / 27 | **0** each | 0.0 | **0.0000%** |
| POOL | MID | 44 | 44 | +5 873.0 | +32.97% |
| POOL | SD | 73 | 73 | +11 783.2 | +33.37% |
| POOL | SF | 85 | 85 | +12 418.8 | +48.76% |
| POOL | KPD | 43 | 43 | +14 734.9 | +49.01% |
| POOL | KPF | 45 | 45 | +25 468.8 | **+157.58%** |
| POOL | RUCK | 44 | 10 | +834.7 | +6.25% |

### `v0_start` by arm × pick band (the #338 bands)

Every national band — 1-3, 4-7, 8-12, 13-20, 21-27, 28-35, 36-48, 49-99 — moves **0 rows, 0.0000%**.
The entire pool arm sits in one band (49-99) by construction and moves +51.46%.

### THE KPD VERDICT — the owner's question, answered

**"Does the v0 for KPDs go backwards too?" — NO. Not on the board.**

All **72 national KPD rows** move by **exactly 0.00** in `v0_start`: 0 up, 0 down, 72 flat. This holds
at every pick from Jacob Weitering (pk1, 2494.93) and Harry Dean (pk3, 2330.83) through to Ben Miller
(pk62, 228.72). The per-row table is in `v0/V0_DELTA.txt`.

Two honest qualifications, because "no" is only true of the quantity the board reads:

- **Latently, national KPD v0 does go backwards.** The KPD par *level* curve falls **−4.44% flat from
  pick 3 to pick 60** (−3.20% at pk1, −8.84% at pk64), and `_v0_uncapped` falls with it. That
  movement is currently absorbed by the D14 surface, which does not read par.
- **Pool KPD v0 rises +49.01%**, and pool KPF +157.58% — the largest position effect anywhere in this
  measurement.

**PREREG P4 — my prediction was WRONG in its stated form.** I predicted KPD v0 would have *mixed sign
across picks* with shallow picks moving <3%. The actual answer is stronger and simpler: national KPD
`v0_start` does not move at all, and the underlying level moves uniformly *down*, not mixed. Recorded
as a breach.

### Largest v0 movers by name

All 25 largest by percentage are pool rows at pick 65. Largest by absolute size: Levi Casboult (POOL
KPF, 846.76 → 2230.75, +163.45%), Matthew Taberner (+1111.57), Finnbar Maley (+815.05), Cooper
Trembath / Anthony Caminiti / Noah Howes / Hayden McLean / Tom Fullarton (each +804.63, +163.45%).
**No national row appears in either list, because no national `v0_start` moves.**

### PREREG P2 / P3 — BOTH FALSIFIED, and the falsification is the finding

I predicted (P2) the `_v0_uncapped` ratio would be a pure function of (position, effective pick), and
(P3) that it would equal `iso_corr_FIX/iso_corr_HEAD` — on the reasoning that the pole and the `_ev_pw`
leg are both zero-weight at the V0 clock, leaving the ISO synthetic table as the only par channel into
v0.

- **P2: FALSE.** 100 of 187 multi-row (pos, effpk) cells have a non-constant ratio.
- **P3: FALSE.** Worst |v0 ratio − iso ratio| = 1.25e+01.

The two premises I checked were both right — the pole weight at the V0 clock is **exactly 0.000000**
for every mover measured (Task 5), and `_ev_pw(0) = 0`. What I missed is that `price6(p, b6(p,Y), Y)`
is **not** par-independent: `b6` → `cp._feat` → `cp._lvl_eff` → `_coreM1` → `Lo = cp._lvl_eff_orig` =
**`par_redesign.lvl_par`**, which reads `par_at(pos, effpk, tenure)`. That is result (1) above, and it
is why the ISO table moves national picks *up* (+0.13% to +10.71%) while national `_v0_uncapped` moves
*down* 3.25%.

---

## TASK 2 — v0-CHAIN LAWS ON THE FIXED ENGINE

Instrument `scripts/gates_report.py`. Full output `gates/GATES.txt`, JSON `gates/GATES.json`.
Population for D14a/D14b: 1448 real ND rows with a pick, 122 pool rows excluded — the surface's own
population, per the 2026-08-10 correction.

### NO GATE FLIPS RED. All five are GREEN under the fix.

| gate | quantity | law | HEAD | FIX | verdict |
|---|---|---|---|---|---|
| **D14a** | `cross_draft_maxdisp` | 0.0 | 0.0 | **0.0** | GREEN |
| **D14b** | `within_cell_inversions` | 0 | 0 | **0** | GREEN |
| **D14c** | `kpp_depth_monotone` | True | True | **True** | GREEN |
| **D14d** | `rising_steps_1_64` | 0 | 0 | **0** | GREEN |
| **D14d** | `rising_steps_full_grid` | 0 | 0 | **0** | GREEN |

**And the green is not vacuous — I tested that specifically.** The obvious objection is that
`v0_start` reads a frozen artifact, so D14a/D14b cannot move whatever par does. Three checks:

1. `_v0surf_sig` (`:1343`) hashes `{pvc curve, roster (pos, ageR, pick), gate env}` — **no par input**.
2. A forced refit (`RL_V0SURF_REFIT=1`) reproduces `v0_start` on **all 1002 rows**, because the
   declared refit path fits the lens from the #279 basis artifact × the PVC anchor, neither of which
   the par fix touches.
3. On the **`RL_V0_LENS=0` lane** — the retired pre-#306 free fit, the *one* path where the surface is
   fitted from `_v0_raw` and par therefore does reach national `v0_start` — national `v0_start` moves
   on **all 668 rows (−2.9025%)** and the national board moves a further −0.4499%… **and every D14
   gate is still green** (D14a 0.0, D14b 0, D14c True, D14d 0/0), on both HEAD and FIX.

So the gates hold on the lane where they could have failed. (PREREG P6/P7/P8/P10 — all TRUE.)

### `_ruc_prior_cap` — THE ONE v0-CHAIN QUANTITY THAT MOVES, AND IT MOVES AGAINST THE FIX

Population: every real RUCK row the board carries (n=71: 27 national, 44 pool).

| arm | n | binds HEAD | binds FIX | total cut HEAD | total cut FIX | newly binding | released |
|---|---|---|---|---|---|---|---|
| NATIONAL | 27 | 6 | **12** | 661.9 | **1549.1** | **6** | 0 |
| POOL | 44 | 34 | **40** | 6 361.1 | **16 832.9** | **6** | 0 |

**The ceiling itself does not move on a single row (0 of 71)** — `RUC_PRIOR_CAP · _cap_basis · _ruc_head_v0`
is par-independent. What changes is what the ceiling is applied to: `_v0_uncapped` **rises** for these
rucks and pushes them through a stationary cap. Newly binding, national:

| player | eff pick | `_v0_uncapped` HEAD → FIX | ceiling (unmoved) |
|---|---|---|---|
| Samson Ryan | 42 | 599.4 → 794.5 | 681.8 |
| Lachlan Smith | 47 | 423.6 → 572.5 | 546.0 |
| Rhys Stanley | 47 | 438.4 → 592.5 | 546.0 |
| Marc Pittonet | 50 | 389.1 → 521.8 | 484.4 |
| Jacob Molier | 52 | 354.1 → 474.5 | 457.8 |
| Alex Dodson | 53 | 395.7 → 524.2 | 443.8 |

**PREREG P9 — BREACHED.** I predicted the binding set would not grow (FIX ≤ HEAD + 2). National ruck
binding **doubled** (6 → 12) and the total national cut rose **×2.34**. This is not a red gate — the
cap is a designed clamp, not an assertion — but it means the fix's effect on deep-pick rucks is being
partly absorbed by a scaffold that was calibrated against the pre-fix v0 distribution. It is a real
adoption consequence and it is the owner's call whether the cap should be re-derived alongside.

### Report-only figures that moved (not gates)

`report_only_all_nd_maxdisp` 324.16 → 424.58 and `report_only_all_nd_inversions` 412 → 565. These are
the whole-ND readings the 2026-08-10 population correction declared **unsatisfiable** — they compare
pool division-level prices against national surface prices, two different price objects. They got
worse because pool `v0_start` rose 51%, widening the gap. Reported so the record is complete; they are
not evidence for or against adoption.

---

## TASK 3 — `nd_profile` AT FIXED-ENGINE v0s

Instrument: ORDER 20's own `nd_profile_test.py` + `harness_armsplit.py`, **imported and run, not
re-derived**. Its CONTROL 1 passes on both matrices (split=False reproduces the pinned
`harness_pvc_REPINNED_pass3.structural_values` value-for-value, 0 differences). Matrices emitted by the
pinned `emit_matrix_338.py` (md5 `bffde2f786be85037483e9f5f1563068`) on each staged tree.
Output `ndprofile/ND_PROFILE_ORDER20B.txt`, `ndprofile/ND_PROFILE_DECOMP.txt`.

Population: the engine-arm national teaching set, **n = 1443**.

### The four corners

| construction | HEAD-emitted matrix | **FIX-emitted matrix** |
|---|---|---|
| CONTAMINATED `S[(pos,t)]` | 1.0253296290 | 1.0196846297 |
| ARM-SPLIT `S[(arm,pos,t)]` | 0.9944115616 *(the published figure, reproduced exactly)* | **0.9900060981** |

### THE NUMBER ORDER 22 MUST CALIBRATE AGAINST

```
nd_profile (post-adoption, engine arm, n=1443)  =  0.9900060981
```

Published-vs-definitive: **0.9944115616 → 0.9900060981**, delta **−0.0044054635 (−0.4430%)**.
Today's shipped state to full adoption: **1.0253296290 → 0.9900060981**, delta **−0.0353235309
(−3.4451%)**.

### v0-side vs strata-side, separated

| leg | measured | delta | pct |
|---|---|---|---|
| **STRATA-side** (the `S` key change) at **fixed-engine** v0s | 1.0196846297 → 0.9900060981 | −0.0296785316 | **−2.9106%** |
| STRATA-side at HEAD-engine v0s *(ORDER 20's published leg)* | 1.0253296290 → 0.9944115616 | −0.0309180674 | −3.0154% |
| **ENGINE-side** (HEAD-emit → FIX-emit) under arm-split strata | 0.9944115616 → 0.9900060981 | −0.0044054635 | **−0.4430%** |
| ENGINE-side under contaminated strata | 1.0253296290 → 1.0196846297 | −0.0056449993 | −0.5506% |
| **interaction** (non-additivity of the two legs) | — | **+0.0012395358** | — |

**A correction to the order's framing.** The order says "`nd_profile`'s denominator is Σv0", which is
true, but **the denominator does not move**: Σv0 over the 1443 national teaching rows is
**1216753.5000 → 1216753.5000, byte-identical, 0 of 1443 rows** — because national `v0_start` is
par-independent (Task 1/2). The engine-side leg reaches `nd_profile` entirely through the **numerator**,
via the matrix fields that do move: `vpath` (1766 rows), `peak` (1590), `cur` (1233), `v0` (1084 — all
pool), `anchor` (1007). So "v0-side" is a misnomer for this leg; it is a *numerator* effect and should
be described that way when ORDER 22 quotes it.

Completion provenance on the FIX-emitted matrix is unchanged in shape: `completed` 734 → 660,
`prior_fallback_thin` 43 → 117, fallback share 2.307% → 5.106%.

**PREREG P11 TRUE** (it differs from the published figure), **P12 TRUE** (|Δ| = 0.4430% < 0.5%),
**P13 TRUE** (0.9900 stays below 1.0 — the sign flip relative to break-even survives).

---

## TASK 4 — PER-MOVER CHANNEL DECOMPOSITION

Instrument `scripts/channel_harness.py` → `scripts/mover_decomp.py`.
Method: `PR.par_at` is replaced by a dispatcher installed **before** the engine head is exec'd, so
import-time readers (ISO, POLE) route through it too. Each call is attributed to its consumer by the
**actual calling frame** (function name + line), not by assumption, and every call is counted:

| channel | call site | calls per build |
|---|---|---|
| **LVLPAR** | `par_redesign.lvl_par:126` | **38 159** |
| BLEND | `_par_prior:312` → `_ev_pw` leg `:590` | 18 002 |
| POLE | `par_pole:397` / `:399` | 13 913 |
| BAR | `ev:2263` (2646) + `_c_w:2124` (2092) | 4 738 |
| ISO | `<module>:497` V0 pick-surface synthetics | 420 |
| BASE | `shortfall` / `BASE_RATE` | **0** |

**CONTROL 1** (asserted every run): the reconstructed HEAD surface equals the HEAD tree's own `par_at`
over the whole (pos × pick 1..70 × tenure 1..6) grid at **worst |Δ| = 0.00e+00**, and the FIX surface
likewise. **CONTROL 3**: `ALL_HEAD` reproduces 624418/123939 and `ALL_FIX` reproduces 622650/126244 —
the committed board totals.

### Two attributions, reported side by side because they disagree

Switching one channel is not additive — the par surface enters `ev()` through terms that multiply and
clamp each other. Both directions are therefore measured and the gap is reported as the interaction,
rather than picking whichever decomposition looks tidier:

- **one-at-a-time (OAAT)**: `v(only c on FIX) − v(ALL_HEAD)`
- **leave-one-out (LOO)**: `v(ALL_FIX) − v(all but c on FIX)`

### Whole national arm

| channel | OAAT | share of −1768 | LOO | share |
|---|---|---|---|---|
| ISO | **+1651** | −93.4% | +1539 | −87.0% |
| BLEND | **−1563** | +88.4% | −1573 | +89.0% |
| POLE | **−1196** | +67.6% | −1315 | +74.4% |
| **LVLPAR** | **−545** | +30.8% | −547 | +30.9% |
| BAR | +4 | −0.2% | +2 | −0.1% |
| **BASE** | **+0** | **0.0%** | **+0** | **0.0%** |
| sum | −1649 | | −1894 | |
| **actual** | **−1768** | | residual OAAT **−119**, LOO **+126** | |

The two attributions agree on sign and rank for every channel, and agree closely on magnitude for
BLEND (−1563 / −1573) and LVLPAR (−545 / −547). They differ most on ISO and POLE, which is where the
interaction lives.

**PREREG P14 — TRUE.** `BASE_RATE` contributes exactly 0.0, on every row, under **both** attributions.
**PREREG P19 — TRUE.** The channels are not additive; the board-level residual is −119 / +126.

### The seven movers

`before → after`, then each channel's contribution (OAAT, with LOO in brackets where it differs):

| player | pos | pick | before → after | Δ | ISO | POLE | BLEND | BAR | BASE | **LVLPAR** | resid OAAT |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Harry Dean | KPD | 3 | 2815 → 2577 | −238 | +21 [+23] | 0 [+3] | **−251** [−262] | 0 | **0** | 0 [−9] | −8 (3%) |
| Angus Clarke | SD | 39 | 680 → 555 | −125 | +13 [+10] | **−82** [−107] | −29 [−46] | 0 | **0** | −3 [+1] | −24 (19%) |
| Harvey Johnston | SD | 49 | 224 → 329 | **+105** | +11 [+13] | +1 [0] | 0 [0] | 0 | **0** | **+92** [+94] | +1 (1%) |
| James Leake | SD | 17 | 476 → 563 | +87 | +16 [+19] | +3 [+3] | 0 [0] | 0 | **0** | **+66** [+68] | +2 (2%) |
| Willem Duursma | MID | 1 | 4067 → 3977 | −90 | +9 [+10] | 0 [0] | **−70** [−99] | 0 | **0** | 0 [−29] | −29 (32%) |
| Will Hayes | SF | 56 | 461 → 378 | −83 | +11 [+9] | −23 [−22] | 0 [0] | 0 | **0** | **−71** [−71] | +0 (0%) |
| Luke Cleary | SD | 61 | 37 → 29 | −8 | 0 [0] | −5 [−4] | −5 [−3] | 0 | **0** | −1 [0] | +3 (38%) |

Every mover's dominant channel is the same under both attributions. The residual exceeds 5% of the
delta for Clarke (19%), Duursma (32%) and Cleary (38%) — **PREREG P19**, and the reason no single
number should be quoted as "the" channel share for those three.

*(Luke Cleary, pk61 SD, −21.62%, is the fifth >15% national mover. He is absent from
`BOARD_DELTA_par_armsplit.json`'s top-40, which is ranked by absolute delta, and his is only −8.)*

**All five >15% national movers are named**: Harvey Johnston (+46.88%), Luke Cleary (−21.62%), Angus
Clarke (−18.38%), James Leake (+18.28%), Will Hayes (−18.00%). **Four of the five are SD; the fifth is
SF.** No MID, KPD, KPF or RUCK row moves more than 15%.

### The par surface's per-cell direction — on the record

`par_at(pos,pick,T) = level_at(pos,pick) + ramp_shr[pos][T]`. `ramp_shr` is re-anchored to 0 at T=1
(`par_build.py:568`), so **for any tenure-1 player the no-pick-axis leg is exactly zero by
construction**. Each mover's own cell, at the tenure the engine reads for him:

| player | pos | pick | T | par HEAD → FIX | Δpar | Δlevel | Δramp |
|---|---|---|---|---|---|---|---|
| Harry Dean | KPD | 3 | 1 | 59.249 → 56.617 | −2.632 | **−2.632** | **0.000** |
| Willem Duursma | MID | 1 | 1 | 73.246 → 72.803 | −0.443 | −0.443 | 0.000 |
| James Leake | SD | 17 | 3 | 65.383 → 66.101 | **+0.717** | −1.439 | +2.156 |
| Angus Clarke | SD | 39 | 2 | 60.404 → 56.192 | −4.212 | −3.547 | −0.664 |
| Harvey Johnston | SD | 49 | 3 | 62.760 → 61.369 | −1.391 | −3.547 | +2.156 |
| Will Hayes | SF | 56 | 2 | 58.810 → 56.724 | −2.085 | −1.249 | −0.837 |
| Luke Cleary | SD | 61 | 5 | 68.572 → 64.572 | −4.000 | −5.311 | +1.311 |

The **level-only curve moves DOWN at essentially every national pick**, and UP sharply at 65-70 (the
pool arm): KPD −3.20% (pk1) to −4.44% (flat pk3-60) to −8.84% (pk64), then **+17.08% at pk65**; SD
−1.29% to −8.94%, then **+13.61%**; MID −0.60% to −3.47%, then +11.36%; KPF −1.63% to −4.97%, then
**+35.30%**. SF and RUCK are the only positions that rise at shallow picks, and only by +0.34% / +0.46%.

---

## THE TWO ADJUDICATIONS

### CLARKE (pk39 SD, −18.4%) vs JOHNSTON (pk49 SD, +46.9%)

**The decisive per-cell fact: they read the SAME cell.** SD `level_at` is one flat kernel value across
picks 25-49 — pk25, 30, 35, **39**, 42, 45, **49** all read `59.4054 → 55.8580`, identically. The
"adjacent picks" are not merely adjacent; they are the same number. So **no per-cell surface direction
can explain their opposite signs** — whatever the cells did, they did it to both equally. Their only
cell-level difference is *tenure* (Clarke T2, Johnston T3), which changes the **magnitude** of the par
drop (−4.212 vs −1.391) but not its **sign**: both fall.

**Neither retracted explanation is right, and each is wrong in a different way.**

- **(a) "pool dragged the surface down, fix raised it; prior-carried players should rise and
  bar-measured players fall" — REFUTED ON THE CELLS.** The direction is backwards. The fix **lowers**
  national SD par at every pick 1-64 (−1.29% at pk1 to −8.94% at pk64) and lowers the level at
  Clarke's and Johnston's shared cell by −5.97%. Pool rows were holding the national deep end **up**,
  not down. (a)'s *shape* — two classes of player moving in opposite directions — is right, but with
  both signs inverted, which makes its stated conclusion wrong for every player it names.

- **(b) "the deep SD cells fell, prior-carried Clarke fell with them, bar-suppressed Johnston rose" —
  RIGHT ON THE PREMISE, WRONG ON THE MECHANISM.** The deep SD cells did fall (−5.97% at the shared
  level). But the premise cannot do the work asked of it, for two independent reasons:
  1. Johnston's cell is Clarke's cell and fell identically, so "the deep cells fell" does not
     distinguish them.
  2. **Johnston is not bar-measured at all.** Measured in the engine at the engine's own clock: his
     stalled-bar state is `el = 3, ns = 2`, and the branch requires `ns <= 1`. **The stalled bar does
     not fire for him.** The `BAR` channel measures **+0** for him, and +4 across the entire national
     arm. The stalled bar is essentially inert in this whole delta; it fires for exactly one of the
     seven movers (Luke Cleary).

**What actually drives each, measured:**

- **Clarke falls through POLE (−82, LOO −107) and BLEND (−29, LOO −46).** He is genuinely
  prior-carried — `_ev_pw` weight
  **0.3641**, near its peak. The pole is the larger leg because `par_pole` prices a synthetic built
  **at par** (`synth(pk, PR.par_at(...), pos)` at `:397`): a lower par lowers the pole ceiling `po`
  itself, shrinking `max(0, po − pr)`. He gets no offsetting lift from `recover(perf, par)` because his
  ratio `pr = bestlvl/par = 0.977` sits on the **saturated** arm of the recover curve
  (`RECY = 1.00` for ratio ≥ 0.82), so a lower par buys him nothing there.
- **Johnston rises through LVLPAR (+92, LOO +94)** — the consumer ORDER 20 never named — with
  everything else contributing +12 between them, and a residual of just +1 (1% of his delta). His
  `_ev_pw` weight is **0.0159**: the pedigree blend is **dead** for him, so the par drop has no
  downward channel, while `lvl_par`'s sensitivity `1 − w = 0.4927` is among the highest of the seven.
  His is the single cleanest attribution in the set: 87.6% of a +46.88% move on one channel.

**So the correct one-line account is:** *the sign is set by which consumer is live for the player, not
by the cell. Par fell for both. Clarke is prior-carried and pole-exposed, so he falls with it; Johnston
is neither — his blend is dead and his bar never fires — and his move comes almost entirely through the
`lvl_par` level feature, the channel the sweep missed.*

### DEAN (pick 3 KPD, −8.5%)

**The claim to adjudicate:** "the kernel cannot carry index-65 rows to pick 3 — confirm or refute that
his move comes through the no-pick-axis channels (`BASE_RATE`) and/or band marginals."

**The kernel premise is CORRECT. The conclusion drawn from it is REFUTED, on both limbs.**

- **`BASE_RATE`: exactly 0.0**, under both attributions. Measured, and structurally guaranteed —
  `shortfall()`/`BASE_RATE` have no consumer on the board path at all (repo-wide grep; 0 dispatcher
  calls in a full build). This limb is not merely small, it is empty.
- **The no-pick-axis `ramp_shr` leg: exactly 0.000.** Dean's tenure is 1, and `ramp_shr` is re-anchored
  to 0 at T=1 by construction. So the no-pick-axis channel contributes **nothing** to him either.
- **His move is the BLEND leg: −251 of −238** (105% of the total; LOO agrees at −262. ISO +21 offsets;
  residual −8, only 3% of his delta, so his decomposition is one of the cleanest of the seven). The
  `_ev_pw` pedigree-par leg at `:590`, weight **0.3601**, reading `_par_prior` → `par_at(KPD, 3, 1)`.

**And pick 3 does move, without any kernel reach.** The KPD par cell (3, T1) falls 59.249 → 56.617
(−4.44%), **100% through the level leg**. The reason is not the kernel tail: the whole KPD level curve
shifts by a near-uniform **−4.44% flat from pick 3 to pick 60**. Removing 743 pool rows changes the
*level* of the national additive backfit, and that shift is pick-independent across most of the curve.
So "the kernel cannot reach pick 3" is true and beside the point — the surface's **level**, not its
kernel shape, is what moved Dean.

Band marginals (`build_pest`'s all-position band marginal, site #4) are **not** a live channel into
Dean's price: `pest` is disclosure-only on this path (`par_at` does not read it; `par_at_p`/`pest_at`
have no `_merged_recover` consumer). It is not in his decomposition because it cannot be.

**PREREG P15 — BREACHED.** I predicted ISO + ramp would account for ≥70% of Dean's delta. ISO is +21
(the wrong sign) and ramp is 0. The dominant channel is BLEND at −251. My mechanism section had the
right premises about the V0 clock but drew the wrong conclusion about the *2026* price path, where the
blend weight is 0.36 rather than 0.

---

## TASK 5 — THE DEAD-ZONE CROSS-CHECK

Instrument `scripts/gating_probe.py`, evaluated **inside the engine at the engine's own clock**
(the stalled-bar tenure `el` is read under `_form_anchor_clock`, as `:2262` does).
Output `movers/GATING_HEAD.json`, `movers/GATING_FIX.json`.

| player | Eq | `_ev_pw` | BLEND | el / ns | bar branch | `pr = bestlvl/par` | pole w (2026) | **pole w at V0 clock** | `1−w` (LVLPAR sens.) |
|---|---|---|---|---|---|---|---|---|---|
| Harry Dean | 0.9957 | 0.3601 | **ACTIVE** | 1 / 1 | none | 1.008 *(saturated)* | 0.8432 | **0.000000** | 0.2273 |
| Angus Clarke | 0.9393 | 0.3641 | **ACTIVE** | 2 / 1 | none | 0.977 *(saturated)* | 0.4724 | **0.000000** | 0.3851 |
| Harvey Johnston | 0.0719 | 0.0159 | **DEAD** | 3 / 2 | **none** | 0.635 *(steep)* | 0.1691 | **0.000000** | 0.4927 |
| James Leake | 0.0050 | 0.0001 | **DEAD** | 3 / 0 | **SIT-OUT** | 0.000 | 0.1096 | **0.000000** | 0.6713 |
| Willem Duursma | 0.9993 | 0.3598 | **ACTIVE** | 1 / 1 | none | 1.051 *(saturated)* | 0.9400 | **0.000000** | 0.1364 |
| Will Hayes | 0.0260 | 0.0022 | **DEAD** | 2 / 1 | none | 0.629 *(steep)* | 0.2927 | **0.000000** | 0.6149 |
| Luke Cleary | 0.9919 | 0.3604 | **ACTIVE** | 5 / 1 | **STALLED** | 0.841 *(saturated)* | 0.0127 | **0.000000** | 0.2406 |

**The attribution is consistent with the engine's own gating at every point:**

- **The pole cannot touch v0.** `w = wage · tfade · expgate` is **exactly 0.000000** at the V0 clock
  for all seven — the engine's own "V0-INERT BY CONSTRUCTION" comment at `:465`, re-measured rather
  than quoted.
- **BLEND fires exactly where `_ev_pw` is non-trivial.** Dean −251, Duursma −70, Clarke −29, Cleary −5
  (all pw ≈ 0.36); Johnston, Leake, Hayes all measure **+0** (pw ≤ 0.016). No player gets a blend
  contribution his weight does not license.
- **BAR fires for exactly one player.** Cleary is the only STALLED row; Leake is on the SIT-OUT branch;
  the other five hit no staleness branch. The whole-arm BAR channel is +4.
- **LVLPAR's magnitude tracks its own gate.** `lvl_par = par + (lvl_wt − par)·w`, `w = min(1,
  exposure/RAMP)`, so `d(lvl_par)/d(par) = 1 − w`. Ordered by `1−w`: Duursma 0.136 → **0**, Dean 0.227
  → **0**, Cleary 0.241 → −1, Clarke 0.385 → −3, Johnston 0.493 → **+92**, Hayes 0.615 → **−71**,
  Leake 0.671 → **+66**. The channel is inert for high-exposure players and dominant for low-exposure
  ones, exactly as the gate predicts.
- **The `recover()` curve explains the pole's sign asymmetry.** `RECX = [0.30, 0.52, 0.67, 0.82, 0.97,
  1.30]`, `RECY = [0.54, 0.64, 0.84, 1.00, 1.00, 1.00]` — flat at 1.00 above ratio 0.82. Players at or
  above par (Dean 1.008, Duursma 1.051, Clarke 0.977, Cleary 0.841) are **saturated** and get no lift
  from a lower par; players well below (Johnston 0.635, Hayes 0.629) sit on the steep segment.

**One honest limit, stated rather than smoothed.** LVLPAR's *magnitude* is gated as above, but its
*sign* is not: Johnston +92 and Hayes −71 are both low-exposure players whose par fell. The level
feature feeds the **baked** conditional-prior forest (`cm_400.pkl`) via `cp._feat`, and that forest is
not monotone in it, so a par-driven level shift can price either way. I report the measured
attribution and do not offer a sign rule I cannot evidence. **PREREG P18 — TRUE** (Johnston's blend and
bar are both provably not firing).

**PREREG P16 — TRUE** (Clarke and Johnston are driven by different channels: POLE+BLEND vs LVLPAR).
**PREREG P17 — PARTIALLY TRUE**: I predicted deep SD cells fall (they do, −5.97%), that (b) is
directionally right and (a) wrong (correct), and that neither is complete (correct) — but I attributed
Johnston's rise to the stalled bar in P16's reasoning, and the bar does not fire for him at all.

---

## PRE-REGISTRATION SCORED — 6 BREACHES OF 21, EVERY ONE OWNED

| # | prediction | outcome | verdict |
|---|---|---|---|
| P1 | ≥1 in 4 national rows show a non-zero `v0_start` delta | **0 of 668** | **BREACH** |
| P2 | v0 ratio is a pure function of (pos, effpk) | 100 of 187 cells inconsistent | **BREACH** |
| P3 | that ratio equals the `iso_corr` ratio | worst diff 1.25e+01 | **BREACH** |
| P4 | KPD v0 mixed-sign, shallow picks <3% | national KPD `v0_start` moves **0.00**; underlying level moves uniformly down | **BREACH** (wrong in stated form) |
| P5 | pool v0 moves more than national in mean abs pct | pool +51.46% vs national 0.00% | TRUE |
| P6 | D14a stays 0.0 | 0.0 | TRUE |
| P7 | D14b stays 0 | 0 | TRUE |
| P8 | D14c stays True | True | TRUE |
| P9 | `_ruc_prior_cap` binding does not grow (≤ HEAD+2) | national **6 → 12**, cut ×2.34 | **BREACH** |
| P10 | no D14 gate flips red | none does, incl. on the `RL_V0_LENS=0` lane | TRUE |
| P11 | fixed-engine `nd_profile` differs from 0.9944115616 | 0.9900060981 | TRUE |
| P12 | \|Δ\| < 0.5% | −0.4430% | TRUE |
| P13 | stays below 1.0 | 0.9900 | TRUE |
| P14 | `BASE_RATE` contributes exactly 0 | exactly 0, every row | TRUE |
| P15 | Dean: ISO+ramp ≥70% of his delta | ISO +21 (wrong sign), ramp 0; **BLEND −251** | **BREACH** |
| P16 | Clarke and Johnston driven by different channels | POLE+BLEND vs LVLPAR | TRUE |
| P17 | deep SD cells fall; (b) directionally right, (a) wrong; neither complete | all three hold | TRUE |
| P18 | ≥1 mover has a provably inactive dominant consumer | Johnston: blend dead AND bar never fires | TRUE |
| P19 | channels non-additive, residual >5% of delta for ≥1 mover | board residual −119; Duursma residual −29 (32%) | TRUE |
| P20 | three pins unmoved at entry and exit | all three unmoved, board rebuilt to `94f1fec5` | TRUE |
| P21 | harness reproduces the committed board values exactly | exact on all totals and every named mover | TRUE |

**Breaches: P1, P2, P3, P4, P9, P15 — six, not the five I would have guessed.** Five of them (P1-P4,
P15) share **one root cause**: my pre-registered mechanism section said the ISO synthetic table was the
only par channel into v0 and that the `_ev_pw` leg was zero-weight. Both premises were verified true
**at the V0 clock** — and I then wrongly carried them to the 2026 price path, where `_ev_pw` is 0.36
and where `lvl_par` (which I had not identified as a consumer at all) reaches `price6`/`b6`. The
instructive breach is that I reasoned about v0's mechanism carefully and never asked what else called
`par_at`; the call-site counter in the harness is what found it, and it found it only because I
instrumented the residual `OTHER` bucket instead of letting 38,159 unattributed calls sit there.

---

## WHAT IS UNRESOLVED, AND WHAT THE OWNER STILL HAS TO DECIDE

1. **`par_redesign.lvl_par:126` is an unswept par consumer on the live price path.** It is not in
   ORDER 20's sixteen-site table, it is the highest-traffic consumer of the surface, and it carries
   −545 of the −1768. The fix routes it correctly (it calls `PR.par_at`, which is arm-routed), so this
   is **not a defect in the fix** — but ORDER 20's sweep is incomplete as a description of what the
   surface feeds, and any later act reasoning from that table will be reasoning from a short list.
2. **`BASE_RATE` is dead code on the board path.** ORDER 20 fixed it (site #5, "LIVE") and its summary
   attributes part of the movement to it. The fix is harmless; the *attribution* is wrong. Whether the
   dead path should be deleted or wired is not decided here.
3. **The ruck prior-scaffold cap now binds on twice as many national rucks.** The cap's height was
   calibrated against the pre-fix v0 distribution. Whether it should be re-derived alongside an
   adoption is an owner decision; this order only measures it.
4. **The national v0 movement is latent, not absorbed forever.** `_v0_uncapped` falls 3.25% and the
   board does not see it only because the D14 surface takes no par input. That is a genuine structural
   independence, not a stale freeze (verified three ways) — but it does mean the par surface and the
   V0 surface now disagree about deep national picks by ~3%, and nothing reconciles them.
5. **ORDER 22's calibration constant.** `nd_profile = 0.9900060981`, and its engine-side leg is a
   **numerator** effect, not a Σv0 effect. Quoting it as "the v0-side" would misdescribe it.
6. **Not re-measured here:** ORDER 20's sites 6-10 (the #336 band tables, establishment-P,
   `distribution_pricing`, the baked `conditional_prior`, `R_SURF`) remain unfixed, so the −1768 is
   still a partial de-contamination cost, exactly as ORDER 20 said.

---

## REPRODUCTION

```bash
export PATH="/root/rl_venv312/bin:$PATH"
cd <this worktree>
D=docs/evidence/par_adoption_2026-08-12/scripts

bash $D/stage_trees.sh                    # stage HEAD + FIX into scratchpad copies (checkout untouched)
bash $D/run_probe.sh HEAD  <out.json>     # ~1.5 min each
bash $D/run_probe.sh FIX   <out.json>
bash $D/run_probe_refit.sh HEAD <out>     # the forced V0-surface refit  (~2.5 min)
bash $D/run_probe_lens0.sh HEAD <out>     # the RL_V0_LENS=0 lane        (~2.5 min)
bash $D/run_v0.sh                         # Task 1 tables
bash $D/run_gates.sh                      # Task 2 gates + ruc cap
bash $D/emit_matrix.sh HEAD <out>         # ~3.5 min each
bash $D/emit_matrix.sh FIX  <out>
bash $D/run_ndprofile.sh                  # Task 3
bash $D/run_all_chan.sh                   # Task 4: 14 engine configs, ~21 min
bash $D/run_movers.sh                     # Task 4 tables
bash $D/run_gating.sh HEAD <out>          # Task 5

# the entry/exit board pin
bash $D/build_board_o20b.sh <out.json> -  # -> 94f1fec59f99c59d5890d5975c79fa9b
```

All scripts **copy** the tree into `$SP` rather than running `git worktree add`; the primary checkout
is never touched, and neither `data/rl_build/rl_app_data.json` nor `engine/rl_after/rl_app_data.json`
is ever written.
