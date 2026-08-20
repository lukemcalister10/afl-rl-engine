# PREREG_32 — ORDER A: CANDIDATE 32, THE PRE-LANDING RECALIBRATION OF THE YOUNG-PLAYER/SITTER MACHINERY

**Pushed BEFORE the first engine edit.** Authority: #334 comment 5312733761 (owner rulings
2026-08-17, final set). Base: the Candidate 31 (ORDER 31-F) tree at `land/order-29` HEAD `0f24f0a`,
store `cb38ef11`, artifact `78ad9842` (head-fixed), Candidate 31 board
`fe6be9d6ac76ebc34d26ebc11d796505` (total 666,913), live board `88ce647f` (752,429), Step-2-law
board on this tree `bce0c65d` (706,862; original-artifact control `9298...`). **NOTHING LANDS
WITHOUT THE OWNER'S WORD ON THE PACKET.**

---

## 0. THE DIAL LAW

Every engine change in this order sits behind **`RL_O32`** (default OFF). `RL_O32=1` implies
`RL_O31=1` (the one law is the substrate). Sub-dial **`RL_O32_STAGE`** (declared, default 6 = full)
wires mechanisms cumulatively for the decomposition legs:

| stage | adds |
|---|---|
| 1 | M1 age-referenced gate bars |
| 2 | + M2 per-season played credit, G\*=2 |
| 3 | + M3 delivered-season reset of c_u |
| 4 | + M6a joint re-derived constants (Φ stall row; D row if it moves) |
| 5 | + M4 selection relief inside D (λ from M6b) |
| 6 | + M5 the 5–15g re-mix (κ, γ from M6c) — the full candidate |

Identity gates (build-failing, asserted by md5 on built boards):
- `RL_O32` unset, `RL_O31=1` ⇒ **byte-exact `fe6be9d6`** (Candidate 31).
- `RL_O32` unset, `RL_O31` unset ⇒ the Step-2 law on this tree, **byte-exact `bce0c65d`**
  (and, strongest control, with the original artifact `06146b00` restored ⇒ `9298...` — run if the
  artifact is recoverable from git history, reported either way).
- Candidate 32 built twice ⇒ byte-identical (determinism).

## 1. THE MECHANISMS (exact forms fixed here)

**M1 — age-referenced gate bars (S1 C3).** A NEW object `o32_gate_bar(pos, age)` =
`_O30BP_BARS[pos] − Δ(class(pos), clamp(age,18,23))`, Δ = the S1 C3 class-pooled development
offsets (CONSTRUCTIONS_S1.json, transcribed as constants — TALL 18..23 =
22.3344756/20.5550075/16.3063624/11.5886727/7.8268950/6.4397833; SMALL 18..23 =
20.0805111/20.0805111/14.3069775/11.2651674/6.7612473/4.5840525 (the S1 age-18 pool-adjacent
value); TALL = KPD/KPF/RUCK, SMALL = MID/SD/SF; construction-time assert that
`_O30BP_BARS` equals S1's flat bars {KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9}
to 1e-9 and that every constructed bar reproduces the C3 table cell to 1e-6), age = season_year − `_by` (present on all 2,650). Cap law structural: Δ ≥ 0 so
bar ≤ flat; ages ≥ 24 take the flat bar exactly. Consumed ONLY in (a) `o31_stall_run`'s
delivered/AVG test and (b) M3's delivered test. `_O30BP_BARS` itself is NEVER edited (S1 §12:
the production references and both par denominators keep the flat bars).

**M2 — per-season played credit, G\*=2 (owner ruling on S2 P1).** `o31_played_units` credits a
played season `f_y · min(1, g_y/2)` (f_y = `_fEy` for the in-progress season, 1.0 completed),
replacing the any-games full credit. u(0)=0 so day-0 prices are untouched by construction.

**M3 — delivered-season reset (owner ruling on S2 P2).** A season y_d with
`g ≥ 10·f_y AND avg ≥ o32_gate_bar(pos, age at y_d)` resets accumulated c_u as of y_d:
c_u = max(0, clock-after-y_d − credit-after-y_d) where clock-after = (Y − y_d − 1) + `_fEy(Y,p)`
and credit-after sums M2 credits over years > y_d. No delivered season ⇒ the M2 clock from entry,
exactly as today. y_d = the most recent delivered season ≤ Y.

**M4 — selection relief inside D (owner ruling, S3 sketch (a), capped).**
`D′ = min(1, D(c_u) · (1 + λ·σ_sel))` — the cap at full pedigree is structural, and the ceiling
stays production-only. σ_sel = max over y ∈ {Y, Y−1} with games of
`clip((g_y − 5·f_y)/(5·f_y), 0, 1)` — the S3 threshold shape (zero below ~5 games, rising 5–10,
flat ≥ 10), season-fraction prorated. Applies to every pathway (the D that enters π), after the
row's own schedule (ND or pool). λ is sized by M6b, NOT by S3's raw coefficients; prereg band
λ ∈ [0, 1.2], grid 0.01.

**M5 — the 5–15g re-mix (R-REMIX, two-sided).**
`ρ32(g) = ρ31(g) + κ · m(g) · (1 − ρ31(g))`, `m(g) = (g/γ)·exp(1 − g/γ)` — a unimodal bump,
m(0)=0 exactly (g=0 rows untouched by construction), peak at γ, vanishing at deep g. Two-sided by
construction: raising ρ at low g moves price weight from the pedigree leg to shown production, so
poor starters CAN fall below entry and risers rise. κ ∈ [0, 0.6], γ ∈ [4, 20], from M6c.
Monotonicity of ρ32 asserted numerically on g ∈ [0, 300] step 0.25 (build-failing). β UNCHANGED
everywhere (R-W1).

**M6 — the joint re-derivation (order documented and fixed):**
1. **bars** (M1 constants, transcribed from S1 — no fit);
2. **stall runs / Φ**: the 30B-C lineage (`o30bc_circ.py` via the `o31f_rederive_phi.py`
   discipline: run WHOLE, character-level substitutions printed) with the DELIVERED predicate
   substituted to the age-referenced bars (age from the harness's own `ENT[...]['birth_year']`),
   on the head-fixed v0 surface (the 31-F substitutions carried). PhiStall rebuilt by
   `o31_fit.py`'s own rule (zero-floor, monotone, ratio to the UNCHANGED 31-F monotone β,
   clip [0,1], monotone) → the stage-4 Φ row. **CONTROL:** the same runner with Δ≡0 must
   reproduce `CIRCULARITY_31F.json` beta_stall at deviation 0.
3. **clock/credit**: G\*=2 fixed by the owner (no fit);
4. **joint D/relief fit**: (a) the 30A-2 lineage (`o30a2_recut.py` run WHOLE, output re-pointed —
   the `o31f_rederive_fade.py` discipline). Its depth-N cells condition on gameless histories, on
   which the new credit/reset/bar definitions coincide with the old, so the PREDICTION is
   **deviation 0.0 from the 31-F row** (D(2)=0.5582775, D(3)=0.2747858, D(4)=0.3972709, flat from
   4) — measured, not assumed. If it moves, the moved row wires at stage 4 and the day-0 delta is
   reported. (b) λ fit on the S2 spectrum surface (`SPECTRUM_S2.json`, the committed instrument's
   cells): each non-thin (n ≥ 10) played cell at depth N with g games in season N−1 is placed at
   its NEW c_u = (N−1+0.92) − min(1, g/2) (no-reset reading, disclosed: cells are not
   delivery-conditioned, so the fit is conservative w.r.t. M3), model
   `min(1, D(c_u)·(1+λ·σ(g)))` vs `min(1, D_cell)`, n-weighted least squares over the λ grid.
   The g=0 cells anchor the fit at λ-invariance (σ(0)=0), so no signal is paid twice: credit moves
   the clock, relief pays only the ≥5-games selection residual, and the cap forbids paying above
   full pedigree.
5. **re-mix calibration**: (κ, γ) fit to W2's hindsight surface — objective = n-weighted SSE of
   candidate year-1 class shares against the REALIZED shares at W2's five games cells and the
   5–9g production terciles (targets from RESULTS_W2.json: cells 0/1–4/5–9/10–15/16+ realized
   0.345/0.907/1.379/2.384/3.389; terciles 5–9 poor 0.840 / mid 1.361 / riser 1.937), subject to
   W ∈ [0.09, 0.16] and slope ∈ [0.885, 1.115], computed with the W2 formulas on year-1 legs
   evaluated by the engine itself at stage 5 (Phat/π/V0 read from the law, ρ32 applied
   arithmetically — then CONFIRMED by a full emit + the W2 scorer run as a disclosed copy).
   Class-mean level is then MEASURED, not targeted (R-CLASSLEVEL).

**M7 — R-CLASSLEVEL target + residual rule (verbatim discipline).** Build with mechanisms only;
run W2's scorer (disclosed copy of `w2_forward_calibration.py`, only the matrix path/md5/head
identity re-pointed) on the emitted Candidate 32 matrix. If the 2005–2015 class mean lands in
**[1.100, 1.117]**: done. If not: attribute the residual by cell via the hindsight surface and
close it CELL-WISE where measured (within the M5/M6 parameter bands, at the measured cells only);
if any UNIFORM component appears needed, **HALT AND REPORT** — that wire requires an explicit
owner word. No silent level lift, ever.

## 2. ACCEPTANCE THRESHOLDS (all fixed here; breach ⇒ halt-and-report, never self-adjust)

| # | gate | threshold |
|---|---|---|
| A1 | W2 level | class mean (2005–2015) ∈ [1.100, 1.117]; every class ∈ [1.07, 1.13]; **HARD FAIL if any class ≥ 1.14** (no-arb line) |
| A2 | W2 slope | S1 calibration slope ∈ [0.885, 1.115] |
| A3 | W2 mix | W = prod/ped ∈ [0.09, 0.16] |
| A4 | W2 cells | 5–9g poor gap (−0.689) and riser gap (+0.471) both at least HALVED in absolute value |
| A5 | W2 sitter guard | g=0 gap within ±0.10 (now −0.012) |
| A6 | S4 | re-score Candidate 32 vs the old law (per_entrant_O29CFINAL, prereg rules unchanged) — REPORT the years-4–6 recovery; no pass/fail target |
| A7 | no-arb | fresh per-entrant matrix (standing emitter, disclosed-copy convention), noarb_table_338.py (md5 0f822035) + all-arm + harness (02dcf28c) + margins (14% carry): **no group margin < 0** |
| A8 | continuity | price-vs-games curve smooth, no discontinuity at g→0 (gap ≤ 1e−6 rel), no dead zone, monotone where at-bar; Carmichael one-game case: the new jump ≈ HALF a cure (D after one 2026 game ≈ 0.765 vs 1.000 wired today; predicted step ≈ +30% vs +71%) |
| A9 | completeness | 26A forbidden set unreachable; every priced row resolves a v0 object (cell coverage 100%) |
| A10 | printed day-0 | 89/89 board rows reproduce printed = round(v0·D(c_u)) at tolerance 0 AND the 89 prints are UNCHANGED vs fe6be9d6 (mechanisms act on evidence/clocks, not entry prints; prediction P-D0) |
| A11 | identity | dial-off gates of §0, plus double-build byte-identity, boot guard clean |
| A12 | numeraire | report whether s moves; if a re-pin is triggered, full composed-ledger discipline |

## 3. PREDICTIONS

**P-D0.** The M6b-4(a) re-run reproduces the 31-F fade row at deviation 0.0, so all 89 printed
day-0 rows are byte-identical to fe6be9d6.

**P-TOT.** Candidate 32 total rises vs 666,913 — predicted band **+1% to +9%** (reset/relief/
re-mix upside outweighs the credit's two-sided cost) and remains below live 752,429.

**P-CLASS.** The mechanisms move the year-1 class mean up from 1.041; after M6c the mean lands in
[1.100, 1.117] without any uniform component (falsifier: a uniform residual ⇒ HALT per M7).

**P-S4.** Years-4–6 recovery is POSITIVE but partial (W1: the Φ/D channels are where recovery
would come from; the additive β channel recovered 0%). Predicted: at least one of the old-law-won
M1 cells flips or narrows; median recovery > 0%. REPORT-only.

**P-NOARB.** All groups: yr0→1 appreciation rises toward ~1.10, margins vs 14% stay ≥ 0
(predicted ~+3 to +10pp), no new arb anywhere.

**P-NAMED — the twenty rows, direction vs Candidate 31 (fe6be9d6), with the driving mechanism:**

| row | cand31 | direction | why (mechanism) |
|---|---:|---|---|
| lachlan-carmichael | 453 | **unchanged** (g=0) | no mechanism touches a gameless clock; his CONTINUITY case: one 2026 game now cures HALF the in-progress season (c_u 1.92→1.46, D 0.585→≈0.765, step ≈ +31% vs today's +71% cliff) |
| josh-smillie | 459 | **unchanged** (g=0) | same; his one-game jump halves too |
| phoenix-gothard | 1012 | **UP, large** | M3: 2026 (15g @ 68.8 ≥ SF 67.9) is DELIVERED ⇒ c_u 3.0→0, D 0.275→1.0 |
| billy-wilson | 547 | **UP, large** | M1×M3: 73.5 ≥ age-21 SD bar 64.0 (was < flat 75.3) ⇒ delivered ⇒ reset; + 16+g re-mix |
| harry-dean | 2670 | **UP** | M1: 59.7 ≥ age-19 KPD bar 44.8 ⇒ s 1→0, Φ→1; + re-mix at 17g (riser side) |
| cooper-duff-tytler | 1832 | **UP, modest** | M1: s 1→0 (50.3 ≥ 43.2); two-sided tension disclosed: re-mix weights his below-par production more |
| kye-annand | 334 | **small, sign uncertain (|Δ| < ~10%)** | games-leg stall stands (9 < 9.2, S1 §3); D already 1.0 so relief no-op; Φ re-derivation (softer) vs re-mix poor-side (59.8 < flat KPD bar) pull opposite ways |
| lukas-cooke | 338 | **DOWN, small** | re-mix: 1–4g cell is rich; 2 games = full credit under G\*=2 (unchanged clock) |
| chris-scerri | 232 | **DOWN** | re-mix two-sided: 5–9g poor starter (47.6 well under every SF bar) |
| thomas-burton | 213 | **DOWN** | same cell, poorer (39.4) |
| milan-murdock | 187 | **UP, small** | mature: bars/cap-law untouched (murdock guard); re-mix 16+ cell + above-bar riser |
| nick-madden | 715 | **UP** | M4 relief (σ≈0.52 on 7g @ 0.92) on D_pool 0.555; re-mix 10–15 cell riser (78.4 ≥ 75.5); Φ_pool re-derived |
| jedd-busslinger | 469 | **UP** | M4 relief (σ≈0.74) on D 0.275; re-mix riser (70.4 ≥ flat 65.4); games-leg stall itself stands (S1 §10) |
| isaac-kako | 806 | **UP, modest** | M1: 2025 (55.2 ≥ age-19 SF 47.8) delivered ⇒ s 2→1, Φ up at g=36; D already 1.0 |
| alex-dodson | 175 | **DOWN** | M2 two-sided: one 2025 game now buys 0.5 season, c_u 1.92→2.42, D 0.585→≈0.42 (S2's clean case) |
| will-green | 338 | **UP, small** | M2 deepens c_u 3.0→3.46 which RISES on the ruled depth-4>3 selection kink (D 0.275→≈0.33) — the kink is kept unsmoothed per standing ruling, disclosed |
| william-mccabe | 316 | **DOWN, small** | re-mix 1–4g poor (31.8); clock unchanged (4g = full credit) |
| charlie-edwards | 340 | **DOWN, small** | re-mix 1–4g cell |
| xavier-taylor | 1288 | **DOWN, small** | re-mix 1–4g poor (42.0); D already 1.0 |
| daniel-annable | 1633 | **DOWN, small** | re-mix 1–4g poor (38.0); D already 1.0 |

## 4. FALSIFIERS / HALT CONDITIONS

- **F1** any A-gate hard-fails (A1's 1.14 line above all) ⇒ halt-and-report, no self-adjustment
  beyond the ruled scope.
- **F2** the M7 residual wants a uniform component ⇒ HALT AND REPORT (owner word required).
- **F3** the Φ control (Δ≡0 rerun) does not reproduce CIRCULARITY_31F at deviation 0 ⇒ the
  substitution machinery is not inert ⇒ halt.
- **F4** the fade re-run moves the D row (P-D0 fails) ⇒ wire the moved row, report the day-0
  delta explicitly — and if any printed day-0 print moves, A10 fails and the packet says so.
- **F5** ρ32 non-monotone anywhere on the grid ⇒ build fails.
- **F6** identity gates (A11) fail ⇒ halt; nothing else runs until byte-identity is restored.

## 5. DELIVERABLES

SHIPPING_PACKET_32.md (per-mechanism what/why, prereg scorecard by number, every acceptance table
inline, owed words in one section — no bare verdicts) · CANDIDATE_32_MOVERS.{json,md} (all ~804
rows, live 88ce647f AND Candidate 31 fe6be9d6 baselines per row + per-mechanism legs
bars/credit/reset/refit/relief/re-mix) · two self-contained sortable HTML preview pages (house
conventions): the full player table (rank, player, pathway, pos, games, Live, C31, C32, deltas vs
both) and the year-1 class page in draft order (ND by pick, then RD, pathways, SSP, MSD; + v0) ·
the twenty named rows traced through every mechanism.

*— Order A integrating build seat, 2026-08-17. Committed before any engine edit.*
