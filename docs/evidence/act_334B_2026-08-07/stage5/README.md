# 334 stage B / STAGE 5 — THE QUIET-STARTER REPRICE · **STOP: the landing floor is not reached**

Branch `landing/334-stage-b`, baseline `c05f214`, ruled baseline board `b56bbdde`. Nothing merges to main;
no PR; no tag. **This stage lands NO product change.** The engine edit, the taught table, the config
amendment and the rebuilt board were all built and gated, and are filed here as EVIDENCE artifacts only.

## THE VERDICT, first

| | |
|---|---|
| **gate 1 (landing floor, yr1 > 1.00)** | **FAIL — yr1 whole-cohort lands at `0.9945`** (from `0.9504`). Short of the floor by **0.0055 of cohort entry value**. |
| **the STOP** | The supervising seat's standing instruction: a re-taught surface that still misses the 1.00 floor **is** the STOP condition. The one permitted re-teach has been used. **Nothing product-side is pushed; the measured frontier is the report.** |
| **gate 3 (band [1.35,1.45])** | **PASS** on whole cohort (`1.432718`, peak yr 4) and on picks 1-20 (`1.429314`, peak yr 4). Picks 21-64 at its own peak (yr 6) reads `1.471250` — **outside, and BYTE-IDENTICAL to the baseline** (`move +0.000000`): a pre-existing property, not something this stage did. |
| **gate 2 (Mraz, tiered)** | **PASS, tier "3.0-3.5x — pass, disclosed"**. Board `1585 -> 1651` = **`3.1151x` his pick's 530**, from `2.9906x`. |
| **the other gates** | every one PASSES — see the table below. |
| **so why STOP?** | Because gate 1 is a floor and it is missed. Gates 1-3 are **not jointly** unreachable (2 of 3 hold), but the floor is the act's binding target and this seat will not iterate a fourth teach to chase it. |

## THE FRONTIER — where the missing 0.0055 actually is

`FRONTIER.txt` decomposes the yr1 landing against each sub-population's **own measured discounted future**
(the round-2 M2 method: `F = mean_k v(yr1+k)/1.0939^k`, `k=1..4`, busts at 0), read off the FROZEN baseline
matrix `b564b12e`:

| sub-population | share of cohort v0 | yr1 BASELINE | yr1 LANDED | **its own MEASURED F** | landed / F | headroom |
|---|---|---|---|---|---|---|
| zero games by yr1 (n=496) | 0.2733 | 0.6462 | **0.6525** | 0.6635 | 98.3% | +0.0110 |
| **quiet starters 1-5 (n=287)** | 0.2283 | 0.7068 | **0.8925** | **0.9541** | **93.5%** | **+0.0616** |
| played 6+ by yr1 (n=414) | 0.4985 | 1.2288 | **1.2288** *(untouched)* | 1.3470 | 91.2% | +0.1183 |
| **WHOLE COHORT** | 1.0000 | 0.9504 | **0.9945** | 1.0706 | 92.9% | +0.0760 |

Read that table before anything else. **The floor is missed by 0.0055 and there is +0.0141 of cohort value
still honestly available inside stage 5's own scope** (the quiet-starter headroom `0.0616 x 0.2283`), plus
**+0.059 fenced in the established leg** (`0.1183 x 0.4985`) which is stage 6's, not this act's.

So the honest sentence is **not** "the sit-out leg cannot reach 1.00". It is: **this seat's taught surface
delivers 93.5% of the quiet-starter class's own measured deficit, and the remaining 6.5% is a teaching
shortfall this seat did not close within its iteration budget.** Round 2's ≈1.01-1.03 estimate is
reachable in principle; it was not reached here.

### Why the surface undershoots, as far as it was diagnosed

The blend is `(1-lam)·G·R·A + lam·e_full`. `G` is taught to solve that equation for the anchor leg at the
**frozen** `lam`, but installing `G` moves `lam` (the surprise statistic reads the lifted anchor — the
site the directive requires `G` to enter). For a quiet starter whose `e_full` sits below his anchor the
re-read is amplifying, but the *cell-aggregate* solve is not the *per-player* solve, and the value-weighted
cell target under-delivers on the players who dominate the cohort denominator. A per-player-consistent
teach (one fixed-point pass, then freeze) would close most of the residual gap. **The directive forbids a fixed
point**, and this seat did not have the budget to test a compliant alternative. That is the honest
statement of where the 6.5% went; it is not a claim that it is unreachable.

## Every gate, as measured

| gate | result |
|---|---|
| **1 · landing floor** yr1 > 1.00 | **FAIL — 0.9945** (whole). Per band: 1-20 **1.0044** (from 0.9707) · 21-64 **0.9788** (from 0.9183). Distance to the ≈1.01-1.03 expectation: **-0.016 to -0.036**. Distance to the sequence range floor 1.04: **-0.046**. |
| **1b · below-own-pick falls** | **PASS, both populations.** Matrix: **939 -> 875** (-64), mean shortfall 34.34% -> 30.12%. Current board vs the installed ladder: **374 -> 371** (-3), mean shortfall 61.21% -> 60.99%. |
| **2 · Mraz tiered** | **PASS (3.0-3.5x, disclosed).** `1585 -> 1651` = `3.1151x`. Taught `G` at his cell **1.157941**. Full chain in `probes_stage5.txt`. |
| **2b · near-projection re-proof** | **FAIL, DISCLOSED AND NOT SMOOTHED.** 5 of 6 band players move; max **+43.1% continuous**. This is *not* granularity. The criterion is amendment 1's fence around a *cut*; stage 5 is a *lift* whose target population intersects the band by construction. Reasoning and the direction split in `NEAR_PROJECTION_PROOF.txt`. The condition that IS binding — "no broad hit to young players" — is met absolutely: **zero cuts on 804 rows**. |
| **3 · band [1.35,1.45] at each table's own peak** | **PASS** whole (1.432718, yr4) and 1-20 (1.429314, yr4); 21-64 (1.471250, yr6) OUTSIDE but **byte-identical to baseline**. yr2-4 deltas printed in `RIDES.txt` — the taper **does** reach depth 1-2 and it is small (whole cohort yr2 **+0.0123**, yr3 +0.0021, yr4 +0.0006). |
| **4 · entry-year ride, all three tables at own peak + segments** | **PASS (no machine STOP).** Largest entry-year excess over draft day's annualised ride: whole **+3.53pp/yr**, 1-20 **+3.14pp/yr**, 21-64 **+1.84pp/yr** — all under the +5.00pp/yr line. Full tables in `RIDES.txt`. |
| **4b · FRONT-LOADED assert as printed guide** | **PASS as a reading**: yr1->2 increment **+0.192029** strictly exceeds yr3->4 **+0.085429**. Reported, not enforced. |
| **5 · within-class continuity** | **PASS.** `\|Δ ln G\|/Δτ` realised max **0.475835** vs the fitted taper's own max slope **0.567570**. Both conventions printed on both populations (`WITHIN_CLASS.txt`): whole persisting-unproven class value-weighted **baseline -25.4% -> no-taper -31.2% -> LANDED -25.0%**; quiet starters only **-25.4% -> -43.2% -> -34.7%**. The taper recovers **106%** of the no-taper deepening on the whole class and about half of it on the quiet-starter subset. |
| **6 · non-uniformity + convergence** | **PASS.** Cross-cell spread **> 2xSE** at the teaching kernel; the deciding contrast (nonKPP pick 50, τ=1: 5 games vs 0 games) is **3.88 x SE(diff)**. Convergence: the yr1 gap 1-20 vs 21-64 **falls 0.052317 -> 0.025587** (51.1% of the gap closed; the directive quotes the baseline gap as "0.053"). Cross-band ordering REPORTED, not decreed. |
| **7 · pick/player seam** | **PASS at 1.8868% of a ±2.00% tolerance** — inside, but not comfortably. **A claim this seat wrote first was WRONG and is struck in `LADDER_SEAM.txt`**: the lane does *not* read outcomes only, it reads the entrant's own `vpath`, so a price change reaches the implied ladder by construction. The never-established-teaches-zero rule **bounds** the move; it does not zero it. Gate-2/gate-7 coupling stated, not assumed away. |
| **8 · boundary probes** | **PASS.** 6-game bar: prices **byte-identical** across the dial on all 5 probes, seam ratio 1.0000 (`lam(6)=1` kills the blend weight and `u(6)=0` kills the surprise read — inert twice over). Season rollover: τ continuous (`1.000000 -> 1.000032`), **step in G across the knot 9.9e-06**. No-new-cliff sweep g=1..10: **zero** new non-monotone steps. |
| **9 · recalculation law (Addendum 1)** | **PASS.** A synthetic year-2 player with his year-1 season FROZEN and only his year-2 games varied moves G across **1.0695 .. 1.3666** (spread 0.2970). No stored boost anywhere; G is recomputed from `p['scoring']` at every call. |
| **10 · dial-0 structural short-circuit** | **PASS — board `b56bbdde` rebuilt BYTE-EXACT through the full gate** with `RL_G5_W=0` written into the manifest and `config_sha256`/`expected_boot` re-stamped for the run, then restored (`killswitch_check.py`, verified by md5 on the way out). |
| **11 · fit coupling** | **NONE, re-measured.** Declared refit at `RL_G5_W` 0 / 1.0 / 2.0 all reproduce the committed v0surf pin `9713ec6c` at signature `3e8e50de5103`. |
| **12 · machinery** | CONFIG MANIFEST gate-mode **LOADED** (62 vars, hash `74b2a056`) · `config_manifest.py check` **PASS** · Guard 5 **PASS** · PARITY **PASS 804/804 eps=0** · NUMÉRAIRE **PASS pick-1 = 3000** · FUT-LABEL **PASS** · ZERO-EMPTY-CLUB **PASS** · BOOK↔BOARD **PASS** · self-test **143 PASS / 0 FAIL, 0 re-points**. |

## The taught surface

`g5_table.json` (md5 `1dc66750a51d04eb9b35b33685960feb`) — a frozen committed table the engine loads, in the
`lti_return_table.json` / `ycred_table.json` precedent. Taught ONCE from the frozen baseline walk-forward
matrix `per_entrant_338_stage4a1.json` (md5 `b564b12e`) at board `b56bbdde`; **never re-emitted for teaching**.

* **axes** τ (the engine's continuous round-driven clock) × **CUMULATIVE career games** (Addendum 1) × log-pick,
  per retention class RUCK/KPP/nonKPP. Knots: pick `[5,15,30,50,65]`, games `[0,2,5,10]`, τ `[1,2,3,4,6]`,
  with `G(τ=0) ≡ 1` prepended exactly as `_R_surf` prepends its own 1.0, and flat past the last knot.
* **kernel** Gaussian, bandwidth grown until eff-n ≥ 35 on the **influence** weight (kernel × value) — the
  engine's own `_fit_pick_curve` idiom. **117 of 300 nodes class-resolved; 183 POOLED over the three
  retention classes, DECLARED.**
* **measured knots** τ=1 / τ=2 / τ=3 were all **measured before the fit** (1649 / 1254 / 383 teaching rows),
  with the owner's phase-out shape as PRIOR only. The taught fade decided: quiet-starter G at τ=1 runs
  **1.28-1.76** across the pick range, at τ=2 **1.00-1.61**, at τ=3 **1.00-1.28**, and **1.0000 at τ=6**.
  Max G anywhere on the shipped surface **1.7640** (nonKPP, pick 65, 2 games, τ=1).
* **Mraz's cell** KPP, pick 35, τ=1.8255, 4 cumulative games → **G = 1.157941**, anchor leg `211.61 -> 245.03`,
  composed `G·R = 0.5312`.
* **laws** G ≥ 1 · non-increasing in τ · → 1 at the deep knot · zero-games knots bounded by the measured
  honesty gap (+0.02 in R) · composed `G·R` non-increasing over the engine's own asserted domain τ∈[1,6] ·
  **no cell taught a price above its own entry anchor**.

## ⚠ THE TWO THINGS THE SUPERVISING SEAT MUST SEE

1. **The pre-stated Mraz arithmetic in Addendum 2 is wrong by ~3.3x, and it was wrong in the direction that
   matters.** Addendum 2 pre-states "≈13.7 display points per 1pp anchor lift; G ≥ ~1.20 breaches 3.5×,
   ≥ ~1.31 breaches 3.8×". **Measured: ≈4.3 display points per 1pp; 3.5× needs G = 1.7382; 3.8× needs
   G = 2.2851.** The reason is measurable and printed in `precheck_mraz.py`: at his cell the anchor leg is
   ~8.7% of his price and `lam·e_full` carries the rest, so a 1pp lift on the anchor cannot move his display
   value by 1pp of the *whole* price. Had the pre-stated figures been trusted, this build would have
   branch-held at a G of 1.16 that is in fact nowhere near the tolerance zone.
2. **The teach budget was spent, and how.** Pass 1 was taught, built and fully gated (board `2772d386`,
   yr1 **0.9914**). Its measurement diagnosed two kernel boundary-smearing defects **and** one over-strict
   law reading by this seat. The single permitted re-teach carries all three corrections at once; its
   intermediate diagnostic state (yr1 0.9942) was never built or gated. Pass 1's table is filed as
   `teach_g5_PASS1_superseded.py`. **No third teach was run.** `MEMO.md §3` states each correction and why
   it is a method fix rather than a tune, including the one that lifted the landing.

## Files

| what | where |
|---|---|
| design, roads not taken, the corrections and their justification | `MEMO.md` |
| the frontier decomposition — where the missing 0.0055 is | `FRONTIER.txt` · `LANDING_DECOMP.txt` |
| the taught artifact + the teach + the raw measurement | `g5_table.json` · `teach_g5.py` · `teach_log.txt` · `measure_surface.py` |
| the engine change, as an evidence artifact (NOT landed) | `engine_sitout_ev.patch` |
| pins that WOULD move, measured from the built artifacts | `PINS.md` |
| every moved player, all mechanism fields | `MOVERS_FULL.txt` · `movers_full.csv` · `movers_full.json` |
| Mraz + Nairn chains, recalculation law, bar seam, rollover, cliff sweep | `probes_stage5.txt` / `.json` · `precheck_mraz.py` |
| rides, segments, band, taper reach | `RIDES.txt` · `rides.json` |
| within-class path, three arms, both conventions | `WITHIN_CLASS.txt` · `within_class.json` |
| gate 7 and the struck claim | `LADDER_SEAM.txt` · `ladder_seam.json` |
| near-projection, disclosed failure | `NEAR_PROJECTION_PROOF.txt` |
| below-own-pick, both populations | `BELOW_OWN_PICK.txt` |
| dial-0 byte-exactness through the full gate | `killswitch_check.py` · `KILLSWITCH_PROOF.txt` |
| fit-coupling refit at three dial values | `fit_coupling_refit_log.txt` |
| the re-emitted book, tables, per-entry-year, goal metrics | `noarb/` |
| machinery | `selftest_full_output.txt` · `book_parity_log.txt` · `board_build_log.txt` |
