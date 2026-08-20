# PACKET — ORDER B DERIVATION SEAT (rulings-material; nothing wired)

**Read-only.** Authority: #334 comment 5312733761 (R-W5 adopted — the veteran build is its own order behind
Candidate 32; R-W6 — taper re-derivation rides it). Prereg `PREREG_B.md` pushed before any derivation
(commit d8ea4ca). Nothing in `engine/` was touched or executed; every number below is offline arithmetic
over the W5/W6 measured surfaces and the emitted matrices. The Order B build wires ONLY after Candidate 32
lands, re-runs these frozen procedures on the Candidate 32 matrix, and lands on the owner's word.

Inputs (md5-asserted at run time): `per_entrant_O31FFINAL.json` d97f1aee · `cand31.json` d4e80349
(per-row baselines: cand=fe6be9d6, live=88ce647f) · W5 `RESULTS_W5.json` (reproduced exactly, control
C-W5: anchors 2.8800/2.4213 and every TALL B cell to 4dp) · W6 `W6_VANTAGES.csv` (9,877 vantages) +
`W6_BOARD_IMPACT.json` · S6 emit. Seed 34, cluster bootstrap by player, 90% CIs.

---

## 0. The one-paragraph answer

**The tall defect is not a skill-decline defect — it is an availability/delivery defect that the level
path never prices.** Veteran talls who play keep scoring near their level (per-game ratios 0.96–0.99/yr,
statistically the same as the engine's DELTAS table); what collapses is *delivered value* — games credit,
missed seasons, and the posval bar-proximity amplification — at −12 to −28%/yr in the ruler's own units.
The fitted replacement is therefore an **effective** post-peak ladder for KPD/KPF (3.0%/yr at 28 growing
+2.5pp/yr, i.e. f = 0.970/0.917/0.843/0.755/0.657 at 28–32), which closes the called W5 tall bias
(survivor B 1.21/1.28/1.33/1.66/1.41 → 1.00/0.97/0.95/1.15/1.05) while leaving RUCK on the current
machinery (fitting RUCK with the tall ladder would break it to B≈0.77–0.86 — "rucks age differently" is
confirmed priced about right). The terminal discount fit lands r = 14/15/16/22/34% at ≤27/28/29/30/31 —
the 31-knot is a **boundary solution**: the family exhausts at the level-calibration floors having closed
only ~5pp of the 15.4pp called terminal-rate gap, an honest tension between W5's rate and level
instruments, with the hazard arithmetic (r(31)≈0.25) as the conservative sensitivity. The ×1.05 premium
is **unidentified by W5's anchored instrument** (a flat multiplier cancels exactly — shown numerically)
and the prime-age anchors say talls are if anything cheap at 23–26 (2.42 vs pooled 2.88): **the premium
stays**. The W6 taper re-derived as a quantile object returns the **boundary asc\*=1 at every age band
below 27** — no taper in (0,1] is calibrated anywhere it currently bites — so the derived object is
**retirement** (band[5] = max(q97m, q90)), which kills all 341 ▼ inversions by construction and returns
+30,224 pts (+4.53%) to the board's ceiling scenarios.

## 1. Object 1 — the tall decline curves (fitted, with the measured surfaces behind them)

**Measured surface A — per-game level among talls who play** (`b1_curves.py`, within-player consecutive
pairs, both seasons ≥4 games, weight min(g,g',22), cluster bootstrap B=2000; `RESULTS_B_CURVES.json`):

| step | n | TALL ratio | 90% CI | engine DELTAS implies |
|---|---|---|---|---|
| 27→28 | 100 | 0.971 | [0.947, 0.995] | 0.990 |
| 28→29 | 89 | 1.012 | [0.986, 1.038] | 0.990 |
| 29→30 | 68 | 0.969 | [0.940, 0.998] | 0.980 |
| 30→31 | 49 | 0.965 | [0.928, 1.003] | 0.979 |
| 31→32 | 34 | 0.990 | [0.941, 1.038] | 0.968 |
| 32→33 | 28 | 0.973 | [0.932, 1.013] | 0.968 |

Per-game skill does NOT fall off a cliff — the engine's gentle level table is *about right for what it
measures*. KPD/KPF split check (prereg): level-scale peaks 27 [25,27] vs 29 [27,30] — no called
disagreement, the pooled TALL fit is retained. Age 33+ cells thin (n<20): bounded, never smoothed.

**Measured surface B — delivered value among alive talls** (`b1b_effective.py`, disclosed extension per
the prereg's closure rule: the level-scale estimator is blind to availability, and availability is what
the W5 ruler credits; ratio-of-sums of season value SV between consecutive ages, alive at both, missed
seasons count as 0; career-complete players only; `RESULTS_B_EFFECTIVE.json`): TALL SV ratios
0.88/0.92/0.79/0.68 at 27→28…30→31 (CIs wide, e.g. 30→31 [0.52, 0.87]) — steep, noisy, right-signed.
The posval bar-proximity amplification reconciles A and B: a −3% level step near the tall bars is a
−15–20% value step.

**The fitted object** (`b2_fit.py`, closure fit in remaining-value space — the mandate's own target —
family ρ_j = ρ0 + g·(j−1), f(j) = Π(1−ρ_i), grid-fit to close the W5 anchored TALL profile, weights =
inverse CI variance, over-correction floors = B_pt/CI_hi; `RESULTS_B_FIT.json`):

| object | wired today | FITTED | 90% CI |
|---|---|---|---|
| peak age (KPD+KPF) | 27 | **27** | [27, 27] |
| ρ0 (decline at peak+1) | 1% | **3.0%/yr** | [0.0, 8.0] |
| g (growth per step) | ~+1pp | **+2.5pp/yr** | [+1.0, +4.5] |
| f(1..5) ages 28–32 | .99/.98/.96/.94/.91 | **.970/.917/.843/.755/.657** | see JSON per-step CIs |

Closure: TALL survivor B 1.21/1.28/1.33/1.66/1.41 → **1.00/0.97/0.95/1.15/1.05** (full view
0.97/0.98/0.96/1.24/1.12). The age-30 cell (B=1.76, CI [1.33,2.62]) does not fully close inside the
smooth family without over-cutting its neighbours — its residual (1.15–1.24) is disclosed, and its own
CI is the widest of the called cells. Tail beyond age 32: last fitted annual rate held flat
(extrapolation-by-rule; W5 measures nothing past 31). **Rank ordering survives**: Spearman(mark, R) at
27–31 moves 0.747/0.722/0.692/0.634/0.562 → 0.737/0.709/0.688/0.632/0.544 (max −0.018, bound −0.05).

**RUCK: keep.** Current machinery B = 0.95/1.07/1.08/1.15 (nothing called); the tall ladder applied to
RUCK would print 0.86/0.84/0.77/0.77 — a manufactured under-mark. SMALL: not in scope (mildly cheap at
27, ruled Order-A-adjacent; untouched).

**Controls**: C-W5 exact reproduction PASS. C-REP (replica vs engine step declines, ±3pp) **FAIL** at
27→28 (+6.5pp) and 28→29 (+5.9pp) — the replica cannot carry the engine's form-updating machinery.
Handled per the prereg's fallback: everywhere below, the replica is used **only for counterfactual
ratios** (delta-space), never for its absolute levels. The closure fit itself is ratio-based and
inherits this robustness.

## 2. Object 2 — the age-dynamic terminal discount (fitted, boundary disclosed)

Fitted in delta-space on the survivor-linked pairs (new_step = engine-measured step × replica
counterfactual ratio), r(a≤27) = 0.14 **pinned** (the young end stays put — verified identity), knots
monotone, constrained WLS with the over-correction floors:

| age | flat today | parked V2/V5 | **FITTED (constrained)** | knot CI | hazard arithmetic |
|---|---|---|---|---|---|
| ≤27 | 14% | 13.5–15.5% | **14% (pinned)** | — | 13.9% |
| 28 | 14% | 16% | **15%** | [0.14, 0.14] | 13.9% |
| 29 | 14% | 16% | **16%** | [0.14, 0.20] | 21.1% |
| 30 | 14% | 16% | **22%** | [0.14, 0.34] | 23.2% |
| 31+ | 14% | 16% | **34% (BOUNDARY)** | [0.34, 0.34] | 24.6% |

Reading, honestly: (i) the confident core is the **terminal rise at 30–31** — every bootstrap draw pins
the 31-knot at the family's ceiling; W5's "parked ladders are half the size" is confirmed and then some.
(ii) The 28/29 knots are small and not individually demanded (CIs include 0.14). (iii) The 31-knot is a
boundary: even at 34%/yr the family closes only 0.786→0.738 of the 30→31 step against realized 0.632,
because a 31-year-old's mark is mostly his undiscounted current season — the level-CI floors (no group
pushed below B_pt/CI_hi at any age) stop anything steeper. **The rate and level instruments genuinely
tension**: levels at 28–31 are approximately calibrated after the tall fix (final full B: ALL
0.91/0.91/0.92/0.97, TALL 0.97/0.95/1.21/1.08, SMALL 0.89/0.90/0.83/1.00, RUCK 1.06/1.05/1.05 — all
inside their floors), while the terminal step stays partially open (+10.6pp residual at 30→31). The
un-closable remainder lives in a channel this family cannot reach: **survival-weighting of the current
season itself** (k=0 exit hazard), named for a future order, not smuggled in here. The hazard-arithmetic
column (r = 0.14 + Δexit-share) is the conservative sensitivity the owner can choose instead; both
variants are carried through the board preview.

## 3. Object 3 — the ×1.05 tall premium: THE PREMIUM STAYS

Three measured facts (`RESULTS_B_FIT.json` §premium): (i) **exact invariance** — recomputing every W5
anchored B with the premium stripped reproduces the same profile to 4dp; a flat all-age multiplier
cancels in the anchored instrument, so its marginal contribution to the *called* bias is exactly zero.
(ii) The prime-age raw anchors read talls **cheap**, not rich: TALL 2.42 vs SMALL 3.08 / RUCK 2.64 /
pooled 2.88 (cross-position caveats — REPL offsets, bar levels, posval convexity — stated in prereg).
(iii) Removing it is a flat −4.76% on every tall mark at every age — it cannot repair an age-shape
defect. Verdict per the prereg decision rule: **keep**; the called defect is closed by Objects 1–2; a
re-derivation would need a cross-position level instrument (S4/no-arb territory), named as future work.

## 4. Object 4 — the taper, re-derived as a quantile object: RETIREMENT

Per age band, the exceedance of realized forward best-3 over the ceiling at candidate asc′ (taper median
m recovered exactly per vantage where invertible; target 3%; `RESULTS_B_TAPER.json`):

| band | n | v7 as-priced | asc′=1 (retire) [Wilson 95%] | fitted asc\* |
|---|---|---|---|---|
| ≤19 | 2,710 | 3.58% | 3.58% [2.94, 4.35] | **1.00 (boundary)** |
| 20–21 | 2,236 | 4.74% | 3.40% [2.72, 4.23] | **1.00 (boundary)** |
| 22–23 | 1,821 | 10.60% | 4.17% [3.35, 5.19] | **1.00 (boundary)** |
| 24–26 | 1,818 | 13.64% | 4.35% [3.50, 5.38] | **1.00 (boundary)** |
| 27+ | 1,292 | 16.25% | 2.17% [1.50, 3.11] | 0.95 (CI-compatible with 1.00) |

Exceedance is monotone in asc′, and at asc′=1 it already sits at-or-above the 3% target in every band
the taper currently bites — **no taper in (0,1] is calibrated; the fitted object is the boundary,
i.e. retirement** (`bb[5] = max(q97m, q90-band)`, asc ≡ 1). The one band where a taper would be
tolerable (27+, raw mildly conservative at 2.17%) is within noise of 1.00 and on the safe side. The
residual +0.4–1.4pp above target at asc′=1 is q97m's own and belongs to the censoring-aware bake refit
already ruled (R-W6); sensitivity ≤2016 window: 3.70%. RUCK: 12.16% → 4.26%. Effects: **all 341 ▼
inversions die by construction** (W6 C2: 0 of 9,877 pre-taper); the S6 page's sixth scenario rises by
the W6 variant-A deltas (+30,224 pts / +4.53% over 566 rows, RUCK-heavy: T.De Koning +207, Bryan +166,
S.Ryan +164); the relabel of scenario 6 as "price if the ceiling lands" (W6 §7.4) still applies.

## 5. Object 5 — board impact preview, BOTH baselines (`BOARD_PREVIEW_B.json`, 804 rows)

Applied offline: tall ladder + **anchor-preserving renormalization s\* = 1.365** (wiring W-A below) +
constrained discount knots + taper retirement. First-order on the production leg, engine's own per-row
inputs (pn/ln/gf/fut); pedigree leg untouched. Totals: cand31 666,913 → preview **691,815**
(+24,902 = +3.7% vs Candidate 31; −60,614 = −8.1% vs live 752,429). Decomposition: production −5,322
(veteran cuts net of young-tall renorm rises) + taper +30,224.

| row | pos/age | live | cand31 | Δprod | Δtaper | preview | vs cand31 | vs live |
|---|---|---|---|---|---|---|---|---|
| Callum Wilkie | KPD 30 | 3,633 | 3,422 | −1,521 | +28 | 1,929 | **−1,493** | −1,704 |
| Peter Wright | KPF 30 | 1,619 | 1,522 | −180 | +103 | 1,444 | −78 | −175 |
| Harris Andrews | KPD 30 | 1,623 | 1,521 | −416 | +17 | 1,122 | −399 | −501 |
| Josh Battle | KPD 28 | 2,028 | 1,879 | −622 | +56 | 1,313 | −566 | −715 |
| Harry McKay | KPF 29 | 1,735 | 1,626 | +126 | +92 | 1,844 | +218 | +109 |
| Charlie Curnow | KPF 29 | 1,365 | 1,289 | −561 | +97 | 825 | −464 | −540 |
| Ned Moyle | RUCK 24 | 2,285 | 1,545 | 0 | +120 | 1,665 | +120 | −620 |
| Sam De Koning | KPD 25 | 936 | 841 | +113 | +92 | 1,046 | +205 | +110 |
| Tom De Koning | RUCK 27 | 1,830 | 1,664 | 0 | +207 | 1,871 | +207 | +41 |
| Marcus Bontempelli | MID 31 | 3,876 | 3,677 | −328 | +32 | 3,382 | −295 | −494 |
| Jack Sinclair | SD 31 | 3,322 | 3,180 | −258 | +25 | 2,947 | −233 | −375 |
| Zachary Merrett | MID 31 | 2,704 | 2,542 | −121 | 0 | 2,421 | −121 | −283 |
| Isaac Heeney (control) | MID 30 | 3,537 | 3,359 | −197 | +79 | 3,241 | −118 | −296 |
| Tim English (control) | RUCK 29 | 3,535 | 3,289 | −61 | +41 | 3,269 | −20 | −266 |
| Nick Madden | RUCK 22 | 1,766 | 715 | 0 | +41 | 756 | +41 | −1,010 |

Constituencies: the 38 tall rows aged 28–30 (18,662 cand pts) take **−4,108** production pts (W5's
illustrative sizing was −5,942 via 1/B; the replica distributes it by profile). Non-tall 31+ rows (68)
take −2,322 under the fitted knots (−1,374 under the hazard variant — both carried per-row). Young talls
≤24 (100 rows, 73,828 pts) RISE +3,072 under W-A's renorm — see Object 6. Named single-row flags, honest:
**McKay (+218) and Jeremy Cameron (33, +285) rise** because their current form sits above their learned
peak (ln>pn), so the flat renorm subsidizes their k=0-dominated streams — a within-cell heterogeneity of
the W-A wiring the build must watch (the anchored evidence fixes cell means, not row shares); Cameron and
all 32+ talls are **outside the measured surface** (W5 ends at 31) and flagged in the JSON.

## 6. Object 6 — Order A interaction check

**Mechanism overlap: NONE.** Order A works the pedigree/discount-frame legs (gate bars, per-season
played-credit, c_u reset, selection-relief in D, 5–15g remix, joint D/Φ re-derivation, class residual).
Order B works the production-leg level path (DELTAS/PEAK_AGE for talls + s\*), the balanced-lens rate at
ages 28+ only, and the band[5] ceiling taper. No shared constant, table, or code object.
**Row overlap: REAL, quantified, three channels.** (i) The terminal discount reaches **zero** rows below
age 28 — by construction (r(a≤27)=0.14 identity) and verified numerically (reach grid: combined ==
ladder-only at every age ≤27). (ii) The tall ladder under W-A back-propagates through young talls'
projection streams: naive wiring (no renorm) would cut prime/young talls 17–30% — **rejected by the
prime-anchor evidence**; with the anchor-preserving s\*, young talls ≤24 net **+3,072 pts (+4.2%)**
(Mraz +337, Darcy +572, Treacy +487) — inside Order A's constituency, so **Order A's acceptance suite
(W2 bands, S4 scorer) must re-run after Order B wires**. (iii) Taper retirement lifts young rows'
band[5]/scenario values (+3,778 over 102 early rows per W6) — ceiling display leg only, none of Order
A's channels. Sequencing already ruled: B wires only after Candidate 32 lands.

## 7. WIRING SPEC for the Order B build (proposal; owner's word decides)

**Objects** (all fitted here, to be re-derived on the Candidate 32 matrix with these frozen procedures):
1. `TALL_POST_PEAK` ladder {1:0.970, 2:0.917, 3:0.843, 4:0.755, 5:0.657, 6:0.555, …} consumed by
   `frac()` when g∈{KPD,KPF} and j>0; pre-peak side of DELTAS untouched; PEAK_AGE stays 27/27.
2. `TALL_RENORM s*` — derived at build time as Σ M_old/Σ M_new over the tall anchor rows (23–26) so
   prime-tall marks are conserved in aggregate (this is the level-placement the anchored instrument
   cannot pin and the raw anchors argue for). Alternatives on the menu: renorm on lp only (kills the
   ln>pn subsidy, changes young reach), or a pricing-age-≥27 switch (zero young reach, but a ~−17%
   26→27 mark cliff into the no-arb frame). W-A (flat renorm) is this seat's recommendation.
3. `RL_AGE_DISC` new fitted mode: knots (27,0.14)(28,0.15)(29,0.16)(30,0.22)(31,0.34), flat beyond,
   `_pw_interp` machinery already in place; hazard variant (29,0.21)(30,0.23)(31,0.25) as the
   conservative dial position. Balanced lens only.
4. Taper retirement: delete the v7 asc application from `_b6_core`'s band[5] (delete-don't-disable per
   SSI rule 7), leaving `bb[5]=max(q97m, q90)`; the q97m refit itself stays at the bake (R-W6).
   ×1.05 premium: unchanged.

**Derivation order at build**: (a) taper retirement (independent); (b) re-run W5 instrument on the C32
matrix; (c) refit ladder (closure); (d) derive s\* on the C32 engine; (e) refit discount knots on the
residual; (f) emit.
**Acceptance suite**: C-W5 reproduction on the C32 matrix · tall-anchor gate (prime-tall 23–26 aggregate
marks within ±3% of pre-wire) · closure gates (TALL surv B at 27–31 inside [B_pt/CI_hi, ~1.15]; no
group×age full B below its floor) · rank gate (Spearman ≥ old −0.05 at 27–31) · terminal-step
improvement ≥ 4pp at 30→31 · full no-arb + continuity (watch tall age-neighbour steps) · S6 zero ▼ +
raw-exceedance re-check · dial-off byte-exact to Candidate 32 · **Order A acceptance re-run** (young
talls move under W-A) · both-baseline movers ledger per the standing presentation ruling.

## 8. Honesty ledger

Prereg deviations, all disclosed above: (1) the b1b delivered-value estimator is an extension forced by
the prereg's own closure rule (the prereg'd level-scale estimator measures true skill but cannot close a
remaining-value bias — publishing both is the finding); (2) C-REP failed ±3pp → all downstream use of
the replica is delta-space only. Boundary solutions stated as boundaries: the 31-knot (family
exhaustion), asc\*=1 (every band), r beyond 31 and the ladder beyond 32 (out of surface, held flat).
Thin cells bounded, never smoothed (b1 33+; b1b flagged steps). The 30-cell tall residual (B→1.15–1.24)
left open rather than chased. Within-cell heterogeneity of the W-A preview (McKay/Cameron rises) flagged
as wiring-sensitive, not evidence. The terminal-rate gap is only partially closable inside the discount
family at the level floors; the k=0 survival channel is named, not built. Board preview is first-order
production-leg arithmetic (pedigree legs and full-engine feedbacks not simulated) — the build's own
emit decides.

## 9. Files

`PREREG_B.md` (pushed first) · `b1_curves.py` → `RESULTS_B_CURVES.json` · `b1b_effective.py` →
`RESULTS_B_EFFECTIVE.json` · `b2_fit.py` → `RESULTS_B_FIT.json` (C-W5/C-REP controls, ladder fit,
knot fit, rank, reach grids, premium) · `b3_taper.py` → `RESULTS_B_TAPER.json` · `b4_board.py` →
`BOARD_PREVIEW_B.json` (804 rows, both baselines, both discount variants) · this packet.
Reproduce: `export PATH=/root/rl_venv312/bin:$PATH`, thread pins to 1, run b1→b1b→b2→b3→b4 sequentially.
