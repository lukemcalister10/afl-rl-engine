# PREREG_C.md — ORDER C: THE AGE-CONDITIONAL NORMALIZATION SURFACE (dial `RL_O34`)

Pre-registered BEFORE any engine edit, per standing discipline. Authority: #334 comment
5315155802 (the owner's scope grant, "Yes. Go") on top of the repaired Candidate 32
(`docs/evidence/order_a_2026-08-17/SHIPPING_PACKET_32R.md`, board `7802ee97`). Seat: Order C
build seat, worktree, branch `land/order-29`.

Every term used below is defined where it first appears. Nothing in this order lands without
the owner's word.

---

## 1 · The defect this order fixes (verified, restated)

ORDER 31 lawfully deleted the pick-prior par tables (`par_at(pos, pick, tenure)` — the ruled
forbidden set, aimed at the PICK axis) and re-referenced the production leg's TWO retained
normalization denominators to the flat effective positional bars
(`_O30BP_BARS[pos] = MA.REPL[pos] − rd.REPL_DROP[pos]`; the Ruling-1 values
KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9). The deleted pars carried TWO
axes — pick AND development stage (tenure) — and both went together: the pick-blindness was
ruled, the development-blindness was an unflagged side effect. Since then, young output has
been normalized against MATURE standards inside the production core. S1 measured that those
mature bars fail 86–100% of age-18/19 seasons even for players who turn out fine. The two
sites, verified in `engine/rl_after/_merged_recover.py` at this commit:

- **SITE 1 — the evidence weight `Q`** (`_c_w`, ~line 2390): `Q = clip(sa/par, 0, 2)` with
  `sa` = career games-weighted scoring average and `par` = the flat bar. Under the Candidate-32
  law this weight's one live consumer is the RUCK production-ceiling release (`C_H`), so the
  flat denominator suppresses exactly the young-RUCK production credit (the walk-forward's
  worst positional cut, RUCK −0.43).
- **SITE 2 — the decay gate `pr`** (~line 2535): `pr = bestlvl/par` with `bestlvl` = the best
  demonstrated level; `pr < 0.55` after `tenure ≥ onset+2` classifies a row
  "mediocre-for-years" and crushes it to a fraction of entry value. Judged against the mature
  bar, a decent-for-his-age long-tenure young player (ages 22–23 by construction of the
  tenure test) is mis-classified.

**Traced and stated up front, so the named-row predictions below are honest:** neither site
reaches harry-dean's or cooper-duff-tytler's OWN rows on the 2026 board (dean: KPD, tenure 1,
not a RUCK, nowhere near the tenure≥6 decay gate; duff-tytler the same shape). The channel by
which the blind denominators reached them is the CALIBRATION: the repair's re-mix constants
(and its age credit) were derived against engine legs computed with the blind denominators —
the constants consumed the blind surplus. Fixing the denominators therefore obligates the
re-derivation in §4, and dean/duff-tytler's recovery, if it comes, comes through the
re-derived constants — bounded as predicted in §5. The deeper age lens INSIDE the production
projection itself (`Phat`, named in the repair packet §7 as the remaining dean-shaped defect)
stays out of scope, untouched, and named again here.

## 2 · The surface (construction options, and the one chosen)

**The object:** `par34(pos, a)` — the expected output of a developing player of position
class `pos` at age `a`, used ONLY as the denominator at the two sites above.

**Chosen construction (Option A):** the S1 C3 lineage, unchanged:
`par34(pos, a) = _O30BP_BARS[pos] − Δ(class, clamp(a, 18, 23))`, where

- `Δ` = the C3 class-pooled development gaps ALREADY carried by the engine
  (`O32_GATE_DELTA`, transcribed from `docs/evidence/order32_s1_2026-08-17/CONSTRUCTIONS_S1.json::C3`;
  the engine load-asserts the flat-bar identity those offsets were built on);
- `class` = TALL (KPD, KPF, RUCK) / SMALL (MID, SD, SF) — the C3 pooling;
- `a` = age as of the evaluation year: `a = Y − birth year` (integer) — the SAME age basis
  every Candidate-32 age object uses (the gate bars, the age credit);
- **flat from age 24**: `a ≥ 24 ⇒ par34 = _O30BP_BARS[pos]` exactly — this is the core
  identity control (§6.1);
- **capped at the flat bar**: `Δ ≥ 0` everywhere so `par34 ≤ _O30BP_BARS[pos]` always
  (load-asserted, build-failing);
- **NO PICK AXIS** — the forbidden-set ruling stays fully honoured; there is no pick anywhere
  in the object;
- a row with no birth year takes the flat bar (count disclosed in the packet).

**Options considered and rejected:**
- *Option B — fractional-age interpolation (nodes at 18…23, 0 at 24):* rejected. It would
  introduce a SECOND age basis into the engine (every other O32 age object is integer-keyed),
  and it would make the age-24 byte-identity depend on date-of-birth fractions rather than on
  the same clean predicate the gate bars use.
- *Option C — per-position refit of the gaps:* rejected. C3 is the measured, class-pooled
  construction S1 shipped and the repair wired; a per-position refit is a NEW measurement no
  part of this order commissions.

**Site application (the whole engine edit, besides §4's constants):** at SITE 1 and SITE 2,
and ONLY there, `par` becomes `par34(pos, Y−by)` when `RL_O34=1`. The stall gate keeps its own
age bars (already age-referenced by the repair); the v0-language, the instruments, the
entry surfaces and every other reader keep the flat bars. `_O30BP_BARS` itself is never edited.

## 3 · The dial law

`RL_O34=1` implies `RL_O32=1` (which implies `RL_O31=1`), by the same single-`or` pattern the
existing dials use. Identities, all byte-exact and all asserted in the packet:

- `RL_O34` unset, `RL_O32=1` ⇒ the repaired Candidate 32 board `7802ee97` (total 667,398);
- `RL_O32` unset, `RL_O31=1` ⇒ Candidate 31 `fe6be9d6`;
- further off ⇒ the committed Step-2 board, exactly as before (no expression outside the
  dial's guards is edited).

## 4 · The re-derivation (the constants that consumed the blind surplus)

**What must be re-derived:** the repair's re-mix constants `(κ, γ_u, η, γ_d)`
(`O32_KAPPA/O32_GAMMA/O32_ETA/O32_GAMMA_D`, chosen in `REMIX_32R.json`) and the R1 **age
credit** (the term `κ·m_u(g)·(1−ρ_base)·Δ(age)·20·PL_F` added to the price of every young
played row). Both were calibrated on engine legs computed with the blind denominators. With
the denominators corrected, the unchanged credit would DOUBLE-PAY age on every row the sites
now pay correctly. No other O32 constant reads production surplus: the Phi row and the fade
row are ratios measured on delivered-value panels, and the relief λ reads selection (games),
not bar-normalized output — stated here so the packet can confirm rather than discover it.

**Method — the repair's own joint-derivation discipline, carried, with one added constant and
one added gate:**

1. Wire the surface (§2) behind `RL_O34`.
2. Re-read the calibration legs with `RL_O34=1` at stage 5 (the repair's own leg extractor,
   `o32r_recalibrate.py`, carried; leg-identity control must PASS at deviation 0).
3. Re-measure the corrected (age-relative) hindsight surface exactly as the repair did
   (same classifier, same bootstrap, same seed).
4. Joint grid over `(κ, γ_u, η, γ_d, α)` where **`α` is the surviving scale of the R1 age
   credit** (the credit's form is otherwise untouched). Declared grid:
   `κ ∈ {0.15…0.60 by 0.05}`, `γ_u ∈ {8,10,12,14,16}`, `η ∈ {0,.1,.15,.2,.25,.3,.35,.4,.5}`,
   `γ_d ∈ {4,6,8,10,12}` (the repair's grids), `α ∈ {0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5}`.
   One refinement pass around the feasible region is allowed under the repair's declared rule
   (same selection law, disclosed).
5. **Gates (feasibility):** the repair's ruled gates unchanged — slope ∈ [0.885, 1.115], W
   inside the corrected hindsight 90% CI, max class ≤ 1.139 (the 1.14 no-arb line), ρ32
   monotone, the ruled at-bar continuity object (integer steps, credit included) — PLUS the
   Order C gate: **mature-row identity** — every calibration-population row aged 24+ at its
   as-of year, and every named mature control row on the 2026 board, must reconstruct to the
   SAME price as under the repaired constants at board rounding. (Prediction D-1: this gate
   collapses the four re-mix knob axes to the repaired point `κ=.24, γ_u=11, η=.41, γ_d=14`,
   because those knobs are global in `g` and any movement re-prices thin-games mature rows —
   milan-murdock, age 26 at 17 games, is the demonstration row. The gate is COMPUTED inside
   the derivation, not assumed; the unconstrained minimum is also reported, diagnostic-only.)
6. **Selection = min corrected-surface SSE among the feasible set, full stop** (amendment A2
   discipline carried: no named row, no band spread, no vantage-matrix figure enters the
   choice).
7. Wire the chosen constants; build the Order C board; run every suite in §6.

**Derivation order is exactly 1→7 and will be documented in the packet.**

## 5 · Named-row direction predictions (falsifiable, before any build)

Baseline for every prediction: the repaired C32 board `7802ee97`. "UP" means Order C price
above repaired-C32 price.

- **PC-1 harry-dean (KPD, age 19, 17 games, entry 2741):** neither site reaches his row (§1).
  His ONLY Order-C channel is the re-derived credit scale α. Prediction: he moves by
  ≈ `(α−1) × (his repair credit ≈ +50)`, i.e. **at most a PARTIAL recovery of order tens of
  points if α > 1 is selected; flat at α = 1; DOWN if α < 1.** The −270 does NOT come back
  inside this scope, because the channel that priced it away (the age lens inside `Phat`) is
  outside this order and stays named. If the owner's expectation of recovery is not met, the
  packet says so with the full decomposition, no spin — pre-committed here.
- **PC-2 cooper-duff-tytler (KPF, age 19, 13 games):** same mechanism, same direction as
  dean; his games sit nearer the credit's peak weight so his α-sensitivity per point of entry
  value is slightly larger.
- **PC-3 nick-madden (RUCK, age 22, pool):** **UP** through SITE 1 — his career average is
  judged against the age-22 RUCK expectation (67.67) instead of 75.5, so the ceiling release
  grows. The one named row the sites reach directly.
- **PC-4 the young talls — tauru (KPD 20), croft (KPF 21), busslinger (KPD 22), read (KPF 21),
  gallop (KPF 20), west (KPF 20):** the sites do not reach them (not RUCK; tenure < 5). They
  move with sign(α−1), small magnitudes; **direction = dean's direction**, scaled by their
  own games-weight and gap.
- **PC-5 scerri (SF 20), burton (SF 19):** credit-scale channel only; direction = sign(α−1).
- **PC-6 milan-murdock (SF, age 26, 17 games): BYTE-UNMOVED** — asserted, not just predicted
  (the surface is flat at his age; the mature gate pins the knobs; the credit is zero from 24).
- **PC-7 the year-1 class (the 89 printed day-0 rows): unmoved 89/89** — a gameless row
  touches no site and carries no credit (`m_u(0)=0`).
- **PC-8 the year-1 class aggregate (walk-forward):** the under-priced played cells (10–15g
  gap +0.304, 16+g gap +0.194 in the repair) move TOWARD their realized targets — that is
  what the selection minimizes; no class crosses 1.139 (a gate, not a hope).
- **PC-9 the walk-forward RUCK cut (−0.43, the worst positional attribution cell):** shrinks
  (site 1 is aimed at exactly it).

## 6 · Acceptance (halt-and-report on breach; the vantage matrix stays DIAGNOSTIC-ONLY)

1. **Mature-row byte-identity, store-wide:** every active row aged 24+ (integer age,
   2026 − birth year) prices byte-identically to `7802ee97`. Build-failing assert in the
   evidence harness, printed count in the packet. murdock asserted by name.
2. **Day-0 prints unmoved:** 89/89 exact, identical to the repaired board's prints.
3. **Determinism:** the Order C board built twice, byte-identical.
4. **Dial identities:** §3, byte-exact.
5. **The standing two-sided suite:** five ND pick bands + pool arms + the vantage matrix
   (diagnostic-only), BOTH windows, each band judged against its own fair mark
   (fair = 1.14 × (1 − year-one value share)); the band table printed before/after. **If any
   band goes buy-side red (> +14%), HALT and report.** No class above 1.14 (max ≤ 1.139).
6. **W2 scorecard** re-run age-relative (corrected classifier) and **S4 mid-career recovery**
   re-run (the repair had +53%; movement reported either way, both directions honest).
7. **Continuity in age:** the board's Order-C-vs-repaired delta printed by integer age 18→26;
   acceptance = the age-23→24 step in each site's own object equals the measured C3 step
   (Δ(23): TALL 6.44, SMALL 4.58 points — the surface's own granularity, disclosed) and no
   discontinuity beyond it appears in prices; plus the repair's games-continuity object
   (integer game steps, tolerance 1e-9) re-checked with the chosen α.
8. **Named rows** (§5 list) with full mechanism traces (which site, which constant, how many
   points each).
9. **Completeness/reconciliation:** coverage and price reconciliation as the repair ran them.

## 7 · Deliverables

- `PACKET_C.md` — plain language: the defect, the surface (table printed), what moved and
  why, this prereg's scorecard (every PC-numbered prediction marked held/breached), all
  acceptance tables inline including the full two-sided suite.
- `docs/ledgers/ORDER_C_MOVERS.{json,md}` — movers ledger, FOUR value columns per row:
  live `88ce647f` · Candidate 31 `fe6be9d6` · repaired C32 `7802ee97` · Order C, plus
  mechanism legs.
- Both preview pages refreshed in the standing formats with those four columns (the year-1
  page adds v0 and draft order).
- All evidence in `docs/evidence/order_c_2026-08-17/`, push-per-step, explicit refspec.

*— Order C build seat. Candidate only; the owner's word decides.*
