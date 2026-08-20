# PREREG I — THE COORDINATED BUILD (RL_O36)

**Pushed before the first engine edit.** Issue #334 comment 5317842435 is the scope and the
acceptance contract. This file fixes, in advance: what is wired, in what order, how the dose is
chosen, what every named row is predicted to do, and every number a gate is measured against.
Nothing below may be edited after the first measurement; deviations are declared as amendments.

Seat: ORDER I, the build seat. Base: `land/order-29` at the landing candidate **1f176444**
(RL_O35 = the pick-curve fade on the repaired Candidate 32). Dial: **RL_O36**, implies RL_O35 →
RL_O32 → RL_O31. **Dial-off must reproduce 1f176444 byte-exact.**

---

## 1 · WHAT IS WIRED — THE THREE MEASURED LEVERS

### Lever 1 — S1, the age-referenced bar inside the projection core

Order E located and priced it (`docs/evidence/order_e_diag_2026-08-17/PACKET_E.md`). The
projection loop and the demonstrated-production floor subtract the **mature** replacement bar from
a young player's output. Four sites, all named in advance:

| site | file:line |
|---|---|
| `_proj_w4`, the projection loop | `engine/rl_after/_merged_recover.py:1080-1081` |
| `_prod_floor_w4`, the floor | `engine/rl_after/_merged_recover.py:1118-1120` |
| `rl_model.proj_from_peak` (the ctx-None / synth path) | `engine/rl_after/rl_model.py:1089-1090` |
| `rl_model.prod_floor` | `engine/rl_after/rl_model.py:1119-1121` |

At those four sites and nowhere else, `MA.REPL[x]` becomes

```
bar(x, age) = MA.REPL[x] - lambda_S1 * DELTA(class(x), clamp(int(age), 18, 23)),   DELTA = 0 from age 24
```

`DELTA` is the engine's own S1 C3 surface, already transcribed in the tree as `O32_GATE_DELTA`
(`_merged_recover.py:3338-3341`; lineage `docs/evidence/order32_s1_2026-08-17/CONSTRUCTIONS_S1.json`).
It has **no pick axis**, it is **capped at the flat bar** (DELTA >= 0), and it is **flat from age
24**, so every mature row is byte-identical store-wide. `age` is the age **at that projection
horizon** (`ah + k` in the loop), not the age today.

`lambda_S1 = 0` reproduces today's board byte-exact. The `_O30BP_BARS` object and both par
denominators are NOT touched (the S1 §12 coupling discipline).

### Lever 2 — the counterweight: the O32 re-mix and relief re-derived on the corrected readings

With S1 live, "below expectation" finally means below AGE-expectation. The re-mix knobs
(`kappa`, `gamma_u`, `eta`, `gamma_d`) and the selection relief (`lambda_rel`) are **re-derived**
on the corrected age-fair hindsight surface using the repair's own machinery
(`docs/evidence/order_a_2026-08-17/o32r_recalibrate.py`, REMIX_32R.json lineage), with the S1
production legs live. The W2 corrected-surface targets are the repair's own: **5-9g risers ~1.94 /
5-9g sub-expectation ~0.84** of entry (`REMIX_32R.json::corrected_surface.terciles_realized`).

The mechanism, stated in advance so the direction cannot be claimed after the fact: raising
`kappa` moves weight from a row's pedigree leg onto his **shown production**, and `eta` charges the
pedigree leg down as games accumulate. A young row who is **above** his age bar therefore gains
twice (bigger Phat from S1, more weight on it); a young row who is **below** his age bar loses,
because weight moves off his large pedigree onto his small production. That is how the S1 lift is
paid to performers and charged to sub-expectation-with-games rows.

### Lever 3 — the tall/small sitter factor on the pick-curve fade

Order H (`docs/evidence/order_h_posfade_2026-08-17/PACKET_H.md` §6, `H_RESULTS.json`). The wired
pooled exponent is replaced by the group form:

```
s(pick, group) = g0 + g1*ln(pick) + h_TALL*(group is TALL)
kappa(pick, group) = clip( s(pick, group) / s_norm', 0.5, 2.0 )
g0 = -0.8778   g1 = +0.7100   h_TALL = -0.6921227120657417   s_norm' = 1.4284052406915069
```

TALL = {KPD, KPF, RUCK} (the engine's own `O32_TALLPOS`). `s_norm'` is H's re-solved
redistribution constant: the pick-weighted mean of `D2^kappa` over H's fitted sitters still equals
the ruled depth-2 fade **0.5582775** exactly (H residual -1.1e-16). Smooth in ln(pick), no band,
no cliff. `m_TALL = 0.677` is the multiplicative translation.

**H's two flagged side effects are pre-declared and WILL be reported with numbers, not discovered:**
(i) the 0.5 clip binds for talls over picks **1-24** and for smalls over picks **1-9**, a flat spot;
(ii) the redistribution is exactly pinned, so **late small sitters pay** for the talls' relief —
a small at pick 64 goes from exponent 1.1533 to 1.4527.

---

## 2 · THE DERIVATION ORDER (fixed, and it will not be re-ordered)

1. Age surface — assert the C3 `O32_GATE_DELTA` object unchanged, cap law and flat-from-24 proved.
2. S1 wired at the four named sites, `lambda_S1` free.
3. **Joint** re-fit of `(lambda_S1, kappa, gamma_u, eta, gamma_d, lambda_rel)` — ONE calibration.
4. Tall/small fade factor applied to the wired pick-curve.
5. Full re-derivation asserts: day-0 89/89 unmoved, determinism x2, dial-off byte-exact, mature
   rows byte-identical, the dial-chain identities re-proven.

The tall factor is applied AFTER the joint fit because it is a redistribution with a pinned total
(it moves fade between talls and smalls without changing the total fade charged). Its effect on
the class and band tables is measured and reported, and if it breaks a gate the calibration is
re-run WITH it live and that re-run is declared as an amendment.

---

## 3 · THE DOSE RULE — registered in advance, no hand-picked lambda

Order E's dose warning binds: full S1 overshoots (dean 3,244; the whole-cohort lift breaches the
rails). **`lambda_S1` is NOT chosen by looking at dean.** It is a grid axis in the joint fit.

**Grid (declared):**

- `lambda_S1` ∈ {0.00, 0.15, 0.25, 0.35, 0.45, 0.55, 0.70, 1.00}
- `kappa` ∈ {0.15 … 0.60 step 0.05}, `gamma_u` ∈ {8, 10, 11, 12, 14, 16}
- `eta` ∈ {0.0, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5}, `gamma_d` ∈ {4, 6, 8, 10, 12, 14}
- `lambda_rel` ∈ {0.80, 1.08, 1.30} (1.08 is the wired value)

A declared refinement pass around the feasible set is permitted (the same discipline the repair
used) and its grid is printed.

**Feasibility (the RULED constraints — these are hard and are not traded):**

- `rho32` monotone in g and strictly below 1;
- the ruled at-bar continuity object (integer game steps 0..20, tolerance 1e-9, age credit
  included) — no price cliff at the bar;
- hindsight weight `W` inside the corrected 90% CI **[0.3117, 0.5560]**;
- calibration slope inside **[0.885, 1.115]**;
- **max class mark <= 1.139** (the 1.14 no-arb line).

**Selection law (registered):** among grid points that satisfy the ruled constraints **and** the
owner's acceptance gates G1-G5 as computed on the calibrator's own instruments, choose the point
with **minimum corrected-surface SSE**. Ties broken by smaller `lambda_S1`. If that set is empty,
the selection falls back to the ruled constraints alone, the closest point is reported, and the
seat **HALTS AND REPORTS with the tension quantified** — it does not silently trade one owner law
for another.

---

## 4 · THE ACCEPTANCE GATES, WITH THEIR NUMBERS

Baseline is the landing candidate 1f176444 unless stated. Every gate is printed pass/fail with its
number in PACKET_I.md.

| gate | object | threshold | baseline (1f176444) |
|---|---|---|---|
| **G1** | year-1 class cohort mark (W2 estimator, `mean_0515`) | **>= 1.03**, ideal ~1.08, **strictly < 1.14** | **1.0421** |
| **G2** | ND bands 31-40 and 41-64, yr0->1, extended-338 | both materially improve; aspiration: no sell-red left | **-12.84% / -7.88%** |
| **G3** | every ND band and every pool arm, yr0->1 | **<= +14%** | ND max +9.20% (11-20); **SSP +50.52% is an INHERITED buy-red** |
| **G4** | harry-dean / cooper-duff-tytler board price | **~2,600 / ~1,800** (their C31 levels 2,670 / 1,832) | **2,526 / 1,654** |
| **G5** | sub-expectation-with-games rows | do not rise | see §5 |
| **G6** | mature rows age 24+ store-wide | byte-identical; murdock whole-row | murdock 178.749128... |
| **G6** | day-0 prints | 89/89 unmoved, tolerance 0 | 89/89 |
| **G6** | determinism | two identical builds, byte-equal | — |
| **G6** | dial-off | RL_O36 unset reproduces 1f176444 byte-exact | — |
| **side** | josh-smillie | owner reference "~700s" | **812.3** — see the pre-declared tension in §5 |

**G3 is registered with a known inherited breach.** On the landing candidate the SSP pool arm
already appreciates **+50.52%** yr0->1 (`docs/evidence/order_d_2026-08-17/NOARB_D_out.txt`). SSP
rows enter at pick 65, outside the 1-64 pick curve. This seat predicts it is **untouched**. It is
declared here so that it is reported as inherited, with its number, and never presented as if this
build created it or as if the gate passed.

---

## 5 · NAMED-ROW DIRECTION PREDICTIONS (the scorecard)

Direction is the prediction. The magnitude ranges are stated where the mechanism supports one, and
a missed range is recorded as a miss on the scorecard, not re-written.

| row | pos / age / pick / games | predicted direction | mechanism | predicted level |
|---|---|---|---|---|
| **harry-dean** | KPD 19 / p3 / 17g, 59.7 (age bar 44.8, **+14.9 clear**) | **UP** | S1 + more weight on a good Phat | **2,560-2,720** |
| **cooper-duff-tytler** | KPF 19 / p4 / 13g, 50.3 (age bar 43.2, **+7.1 clear**) | **UP** | same, smaller margin, lower rho | **1,760-1,900** |
| **xavier-taylor** | SD 19 / p11 / 2g, 42.0 (age bar 55.2, **below**) | **DOWN** | weight moves off pedigree onto a poor Phat | −2% to −10% |
| **oskar-taylor** | SD 19 / p15 / **0g** | **UNCHANGED or up <1%** | no production, no re-mix (m_u(0)=0); fade may not reach him | — |
| **daniel-annable** | MID 19 / p6 / 2g, 38.0 (age bar 57.0, **below**) | **DOWN** | as xavier-taylor | −2% to −10% |
| **dylan-patterson** | SD 19 / p5 / 5g, 35.6 (age bar 55.2, **below**) | **DOWN** | as above, larger g so larger charge | −3% to −12% |
| **josh-smillie** | MID 20 / p7 / **0g** sitter | **UP** | small at pick 7 falls onto the 0.5 clip: exponent 0.579 -> 0.500 | ~840-870 |
| **chris-scerri** | SF 20 / SSP p65 / 7g, 47.6 | **UP** | S1 lifts Phat; pool pedigree is small so production dominates | +3% to +15% |
| **thomas-burton** | SF 19 / SSP p65 / 5g, 39.4 | **UP** (weakly) | same channel, below-bar output | 0% to +10% |
| **milan-murdock** | SF **26** / SSP / 17g | **EXACTLY UNCHANGED** | cap law; whole row byte-identical | 178.74912838553396 |
| **will-green** | RUCK 21 / p16 / 1g sitter | **UP** | TALL at p16: exponent 0.793 -> 0.500 (clip) | +12% to +25% |
| **toby-conway** | RUCK 23 / p24 / 6g | **UP** | TALL at p24: exponent 0.899 -> 0.500 (clip) | +10% to +30% |
| **steely-green** | SF 22 / p55 / 43g, played every year | **UP** (small) | S1 on a high-rho row; the steeper small exponent cannot reach him because his fade clock is spent | 0% to +12% |
| **isaac-kako** | SF 20 / p13 / 36g | **UP** | S1 on a high-rho row | +3% to +20% |
| **alix-tauru** | KPD 20 / p10 / 18g | **UP** | S1, tall gaps are the largest | +5% to +25% |
| **jedd-busslinger** | KPD 22 / p13 / 15g, 70.4 in 2026 | **UP** | S1 + re-mix on an above-age-bar season | +5% to +25% |

**Two tensions are pre-declared, so that they are reported and not discovered:**

1. **smillie is predicted to RISE, away from the owner's "~700s" reference**, purely from Order H's
   clip flat-spot at small picks 1-9. This seat does not get to choose whether that is acceptable;
   it reports the number and the mechanism.
2. **The Order G clock-fair class benchmark is [0.9761, 0.9892]** and the landing candidate at
   1.042 already sits **above** it. G1 asks the class mark to grow toward 1.08, which moves it
   **further above** the clock-fair benchmark while staying below the 1.14 buy rail. Both readings
   will be printed side by side. The owner's law G1 governs; the clock-fair reading is reported as
   the diagnostic it was ruled to be.

---

## 6 · FALSIFIERS (any one firing is reported in the packet, in these words)

- **F1** — murdock, or any age-24+ row, moves by more than 0.0 board points. **Build-failing.**
- **F2** — the day-0 print count is not 89/89 at tolerance 0. **Build-failing.**
- **F3** — RL_O36 unset does not reproduce 1f176444 byte-exact. **Build-failing.**
- **F4** — no grid point satisfies the ruled constraints and the owner's gates jointly. **HALT AND
  REPORT** with the binding pair named and the trade quantified.
- **F5** — dean or duff-tytler cannot reach their neighbourhood without pushing a band over +14%.
  Reported as the exact tension, not softened.
- **F6** — any sub-expectation-with-games named row RISES. Reported by name with its number.
- **F7** — `rho32` non-monotone, the at-bar continuity object shows a cliff, or any continuity
  assert in age / games / pick fires. **Build-failing.**
- **F8** — the tall/small redistribution identity does not reproduce 0.5582775 to 1e-9.
  **Build-failing.**

---

## 7 · INSTRUMENTS (the standing, disclosed ones — nothing new is invented)

- Five-band ND yr0->1 and the yr0-7 year paths: the **extended-338** disclosed copy,
  committed md5 **d59ad550116ebbe3d90ed82becd2c4d5**, run whole, output re-pointed per matrix
  (the one disclosed edit).
- Pool arms, both windows: the **all-arm** reader semantics (cohort clock, `pre` rows excluded and
  counted, never zeroed).
- The class mark: W2's own estimator (`mean_0515`), classes 2005-2015, class bootstrap seed 33.
- The board: `bb32.sh` staging with the full five-variable thread pinning; the walk-forward matrix
  from the ORDER 31-F disclosed emitter, byte-carried.
- Lane on every run: `RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72
  RL_PRIOR_TREES=400 PAR_RAMPS=22`, `PYTHONHASHSEED=0`, `RL_V0SURF_PKL=data/v0surf.pkl`,
  `OPENBLAS/OMP/MKL/NUMEXPR/VECLIB_NUM_THREADS=1`. Engine runs strictly sequential, PID-unique
  staging.

---

## 8 · WHAT THIS SEAT DOES NOT DO

It does not land anything. It does not change a ruled constant outside the three levers. It does
not re-open smillie's fade (ruled elsewhere). It does not touch the pool arms' own machinery. It
does not choose between two owner laws — if they conflict it halts and hands the owner the number.

*— ORDER I, the build seat. Prereg pushed before the first engine edit.*
