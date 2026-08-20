# PREREG — ORDER B BUILD (pushed BEFORE the first engine edit)

Authority: #334 c.5312733761 (Order B commission) · c.5314553763 (the owner's B rulings B-1/B-2/B-3) ·
`docs/evidence/order_b_derivation_2026-08-17/PACKET_B_DERIVATION.md` (the fitted curves + wiring spec).
Checkout base at prereg time: **cf443a6** (land/order-29; the Candidate 32 repair seat is pushing to the
same branch — the base moves, and every identity assert below records which base commit it ran against).
This build wires the VETERAN FIXES behind a NEW dial and **lands only after the repaired Candidate 32
lands** — nothing merges on this seat's say-so.

## 0. Dial law

- Everything behind **`RL_O33`** (default OFF). `RL_O33` unset ⇒ every new expression is inert ⇒ the
  board of the CURRENT tree reproduces **byte-exact** (both the all-default board and the `RL_O32=1`
  board). Re-verified after every rebase.
- Stage sub-dial **`RL_O33_STAGE`** (declared, default 3 = full): 1 = tall ladder + anchor renorm ·
  2 = +output-conditional terminal fade · 3 = +taper retirement. Stages exist for the per-mechanism
  movers legs and the s\* derivation; the candidate is stage 3.
- Dev-shell override **`RL_O33_SSTAR`** (measurement only, never shipped): overrides the pinned s\*
  during its own derivation (set to 1.0 for the ladder-only board the fixed point is computed on).

## 1. Mechanism 1 — the anchored tall ladder (owner ruling B-1)

- **Ladder pinned as ruled** (the derivation's fitted object, adopted): post-peak fraction for
  g ∈ {KPD, KPF} at offset j = age − 27: family ρ_j = 0.030 + 0.025·(j−1), f(j) = Π(1−ρ_i), i.e.
  f(1..5) = **0.970 / 0.917 / 0.843 / 0.755 / 0.657** at ages 28–32, f(6) = 0.555; beyond j = 6 the
  last annual ratio is held flat (the derivation's tail rule — W5 measures nothing past 31, so the tail
  is extrapolation-by-rule, bounded by the existing `frac < 0.42` projection stop). Pre-peak side of
  DELTAS untouched; PEAK_AGE stays 27/27; **RUCK keeps the current curve** (derivation: KEEP confirmed).
- Consumed by `frac(a, pa, g=None)` — a new optional position argument; two-argument callers are
  untouched and dial-off returns the shared DELTAS table verbatim. Wired in all four projection loops
  (`rl_model.proj_from_peak` / `rl_model.prod_floor` and their `_merged_recover` W4 copies — the
  duplicate-loop fence is honored: both edited identically).
- **Anchor-preserving renorm s\***: a single multiplier on the tall PROJECTION production stream (the
  same site as the ×1.05 premium, which stays per the derivation), so prime-age tall values are
  conserved in aggregate. Derived at build time as the fixed point of
  s\* ← s\* × (Σ V_base / Σ V_new) over the board's KPD/KPF rows aged **23–26** (V = the row's board
  value, ladder-only stage, all other stages off), iterated to |Σ V_new/Σ V_base − 1| < 0.002, then
  **pinned in code as a literal** with the derivation recorded. The demonstrated floor is NOT
  multiplied by s\* (the floor is a current-level object; a flat ×s\* there would lift every tall floor
  ~35% and is not what the anchor evidence licenses) — disclosed choice, packet shows the consequence.
- **Gates**: prime-tall 23–26 aggregate board value within ±3% of the pre-wire board (the derivation's
  tall-anchor gate) · rank-ordering among 27+ rows preserved (max/mean rank move reported; the W5-
  validated veteran ordering must not be disturbed — halt if the tall-cohort ordering visibly reshuffles,
  i.e. any Spearman(board_old, board_new) within the 27+ tall cohort < 0.95) · no age cliff: the
  board-value age profile of a synthetic tall at fixed level steps smoothly into the ladder (max
  neighbouring-age step reported; the ladder's own fitted decline is not a cliff — a cliff is a jump
  that exceeds the ladder's local annual rate by more than 2× between adjacent ages).

## 2. Mechanism 2 — the OUTPUT-CONDITIONAL terminal fade (owner ruling B-2; replaces the flat schedule)

The universal knob is withdrawn; the fitted-34% boundary value is **dead**. The fade is re-derived here,
continuous in BOTH age and output-above-replacement, fit rules fixed now, before fitting:

- **Family**: r(a, s) = 0.14 + **A·φ(a)·G(s)**, φ(a) = clip((a−27)/4, 0, 1) (linear in continuous age,
  zero at ≤27 — the young end stays put by construction — flat at ≥31), G(s) = exp(−s/s0),
  s = output-above-replacement. Two parameters (A, s0). No cliffs by construction (linear × exponential,
  both continuous). Monotone: non-decreasing in age, non-increasing in output.
- **Surplus measure**: offline (fit): s = max(0, L − REPL[bar]), L = the trailing-2 season level (the
  same L the derivation's replica anchors on), REPL the engine's own replacement row. In-engine (wire):
  s = max(0, cur − REPL[g0]) at the projection hook (cur = level_now, g0 = the present-position REPL the
  k=0 term nets against; when cur is unavailable the curve level lp·frac stands in). Balanced lens only
  (the wiring spec's scope); k=0 is never discounted, so the current season is untouched at every output.
- **Evidence base + machinery**: W5's tier cuts (RESULTS_W5.json `tiers` — star B 0.95–1.10 at all ages
  27–31, every CI covering 1.0; role tier up to 3.59 at 29) + the derivation's hazard decomposition
  (RESULTS_B_FIT.json). Fit in **delta-space** on the rebuilt W5 rows from `per_entrant_O31FFINAL.json`
  (md5 asserted d97f1aee; the C-REP control failed ±3pp in the derivation, so the replica is used ONLY
  for counterfactual ratios — carried rule): new_mark(x) = mark(x) × rep(x; ladder, r(a,s)) /
  rep(x; ladder, 0.14), the mandated tall ladder applied in BOTH numerator and denominator (the fade
  fits the residual after the ladder, the derivation's stage order). Rows with no trailing-2 L keep
  ratio 1.0 (counted, disclosed).
- **Loss**: survivor-view anchored-B, tier×age cells (star/mid/role × 27–31), target B = 1, weights =
  inverse variance of each W5 survivor tier-cell CI (width/3.29 squared, the W5 CIs as published).
  Anchors (23–26) recomputed per candidate (the fade never reaches ≤27, so anchors move only through
  the ladder — flat multipliers cancel in the anchored instrument, so s\* is omitted from the fit and
  that identity is stated).
- **Over-correction floors** (hard constraints): full-view predicted B ≥ B_pt/CI_hi for every tier×age
  cell AND every position×age cell (the derivation's floor rule, extended to the tier cuts).
- **Grid**: A ∈ {0.00, 0.02, …, 0.60}; s0 ∈ {2, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 32, 40, 50, 64}
  (points of level above replacement). Seed 35, cluster bootstrap by player, B = 500, 90% CIs.
- **Identification rule** (decides fitted vs fallback, fixed now): the conditional fit PASSES
  identification iff (i) the 90% bootstrap CI of A excludes 0, AND (ii) the fade is genuinely
  output-conditional on the observed range: the 90% bootstrap CI of G(s̄_star) lies entirely below 0.5,
  where s̄_star = the mean surplus of star-tier rows aged 28–31 (i.e. in ≥95% of draws the fade at
  star-level output runs at under half strength). If either fails → **FALLBACK**: the flat
  hazard-arithmetic knots (28: 0.14 · 29: 0.211 · 30: 0.232 · 31: 0.246, ~25% at the top), wired
  output-flat, and the packet says so plainly with the failed identification shown.
- **Thin-cell pooling rule**: any survivor tier-cell with n < 20 at ages 30–31 is pooled with its
  age-neighbour (30–31 pooled per tier) before entering the loss; if a tier stays under 20 pooled, it
  is dropped from the loss and disclosed. (W5 as published: min survivor cell n = 23 → expected unused.)
- **Star-preservation gate** (the owner's core requirement, checked BY FIT not assumption): predicted
  star-tier B at every age 27–31 stays inside that cell's published W5 CI, and moves from the measured
  point by ≤ 0.05. Verified twice: on the fit's own delta-space prediction, and on the built board via
  the W5 harness re-run (star cells must stay ~1.0 while the tall 28–30 cells close toward 1.0).

## 3. Mechanism 3 — taper retirement (owner ruling B-3)

- The v7 ascending age-taper on the q97 ceiling band is retired: at stage ≥3 the `_v7` compression of
  `bb[5]` is not applied (asc ≡ 1 ⇒ `bb[5] = max(q97m, q90)` exactly as `_b6_core` emits it). The frozen
  q97m model is NOT touched (its refit is bake-time per R-W6). Dial-off keeps the v7 taper byte-exact.
- **Verify**: the 341 ▼ ceiling inversions die (count band[5] < band[4] on the emitted vantages = 0);
  ceiling-scenario delta reported (derivation preview: +30,224 pts over 566 rows); the price effect
  flows through the 0.10 WQ6 weight and is reported per row in the taper leg.

## 4. Acceptance suite (halt-and-report on breaches)

1. Dial-off identity: byte-exact board vs the CURRENT tree base (default env AND RL_O32=1), re-run
   after every rebase, base commit recorded each time.
2. Determinism: the candidate board built twice, identical md5. Boot guard green.
3. Day-0 prints unchanged (the 89 wired entrants print identically with the dial on).
4. Rank-ordering among 27+ rows: report max/mean rank moves; tall-cohort Spearman ≥ 0.95.
5. Continuity: no cliffs in age (synthetic age sweep through the ladder and the fade) or output
   (synthetic surplus sweep through G at fixed age); max neighbouring steps reported.
6. THE STANDING TWO-SIDED NO-ARB SUITE: five ND bands (1-10/11-20/21-30/31-40/41-64) + per-arm pool
   tables + the vantage-consistency matrix, two-sided (sell-side red for negative yr0→1; buy-side red
   for appreciation above 14%), on the built matrix beside the O32R control. **Entry-year control**:
   the mechanisms hit veterans, so the entry-year (yr0/yr1) tables must be nearly unmoved — asserted
   and reported explicitly (prereg'd bound: every band/arm yr0 and yr1 cell within ±1.5% of the O32R
   control's cell).
7. W5 harness re-run (the w5_veteran_mark.py pattern, byte-carried ruler) on the built matrix:
   tall 28–30 B cells close toward 1.0; star cells stay ~1.0 (inside their CIs).
8. Numeraire: report whether s (the Step-6 numeraire pin) moves. Nothing is re-pinned here.
9. Landing dependency stated in the packet: full landing acceptance re-runs on top of the repaired
   C32 once it lands (row overlap: taper lifts some young talls); this seat never merges the repair
   seat's work.

## 5. Named-row direction predictions (scored in the packet)

Board = C32-base + RL_O33 stage 3, vs the C32-base column; direction (and rough size class) predicted
from the derivation preview ADJUSTED for B-2 (conditional fade replaces the flat knots — the flat-knot
part of the 31+ cuts should largely vanish for star-output rows):

| row | pos/age | prediction |
|---|---|---|
| callum-wilkie | KPD 30 | DOWN, large (ladder leg dominates; fade adds little — mid/star output) |
| peter-wright | KPF 30 | DOWN small on production, taper up ⇒ net small (either sign, small) |
| harris-andrews | KPD 30 | DOWN, clear (ladder) |
| josh-battle | KPD 28 | DOWN, clear (ladder at j=1..; fade ~0 at 28 unless low output) |
| harry-mckay | KPF 29 | UP (ln>pn flat-renorm subsidy + taper — the derivation's flagged heterogeneity) |
| charlie-curnow | KPF 29 | DOWN, clear (ladder; ln<pn) |
| ned-moyle | RUCK 24 | UP (taper only; RUCK keeps its curve, no fade at 24) |
| lachlan-mcandrew | RUCK 26 | UP, small (taper only) |
| sam-de-koning | KPD 25 | UP, small-moderate (renorm ≥ ladder at 25 + taper) |
| tom-de-koning | RUCK 27 | UP (taper, the biggest single taper riser in W6) |
| marcus-bontempelli | MID 31 | ~UNMOVED to slightly up (star output ⇒ fade ~0; taper +small) — STAR EXHIBIT |
| jack-sinclair | SD 31 | ~UNMOVED (star output ⇒ fade ~0; taper +small) — STAR EXHIBIT |
| zachary-merrett | MID 31 | ~UNMOVED (star output ⇒ fade ~0; taper ~0 per preview) — STAR EXHIBIT |

Cohort predictions: young talls ≤24 rise ~+3–5% under the renorm (Order A overlap, stated for the
landing re-run); tall 28–30 production leg cut in aggregate; non-tall 31+ moves concentrated on
LOW-output rows only (the B-2 re-scope); entry-year tables ~unmoved; board total dominated by the
taper's +~30k ceiling-leg points.

## 6. Deliverables

PACKET_B_BUILD.md (plain language; conditional-fade fit with CIs and star-preservation evidence side by
side; prereg scorecard; every acceptance table inline including the two-sided suite) · movers ledger vs
BOTH baselines (live 88ce647f, Candidate 31 fe6be9d6) with per-mechanism legs · both preview pages
refreshed (player board: Live · C31 · C32-base · B-preview; year-1 page with unchanged rows asserted) ·
named rows traced. Evidence: this directory; push-per-step, explicit refspec `HEAD:land/order-29`.
