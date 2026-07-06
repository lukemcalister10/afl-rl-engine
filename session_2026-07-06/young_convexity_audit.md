# YOUNG-PLAYER CONVEXITY / OPTION-VALUE AUDIT — v2.5 — 2026-07-06

READ-ONLY. Measures + proposes only. No fit, no board/store/source change, cannot reduce any young value.
Base: `git fetch --all --prune` done; v2.5 read from `origin/main` by name; store md5 **e1b4d8bf** == pinned,
engine head **efea88e5**, band **34faa865**, `boot_guard.py` PASS `[planaudit]`.

---

## RETURN

- **Store-assert (board untouched):** store md5 `e1b4d8bf` == pinned at start AND end (Guard 5 PASS
  `[planaudit_end]`); `_merged_recover.py` `efea88e5`; `run_panel.sh` PASS 10/10 unchanged. Zero writes to
  `rl_model_data.json` or any pricing code.
- **INTEGRATES vs collapses → IT INTEGRATES.** v2.5 prices young players as `E[value(outcome)]`, not
  `value(mean)`. Three live layers: (A) board quadrature `price6 = Σ WQ6·v_at_peak(L)` over a 6-node forward-peak
  band [q10,q30,q50,q70,q90,**q97**] (`_merged_recover.py:111-117`; design comment "the convex map E[v(L)] pays
  the upside tail"); (B) a 5-node Gauss-Hermite `E[value|level~N]` present-value layer (`rl_model.py:820-844`,
  exposed as `_cvx`); (C) an explicit runway kicker `×(1+runway·elite·PMAX)`, PMAX=0.25 (`rl_model.py:319`), with
  the projection horizon itself age-gated (younger = longer). The value map is a steep hockey-stick (0 below
  replacement, convex above), so the machinery pays real option value. The only "collapse" (`peak_est`) is the
  integrand, not the price.
- **Current premium (engine), by band, value-weighted:** `_cvx` present-value premium ≤21 **+3.2%**, 22-24 **+4.2%**,
  25-26 **+1.8%** (bounded [0,+25%]; 5/18/11 players already AT the +25% cap; 53 zero-game ≤21 unproven EXCLUDED
  from this layer). Forward-band convexity is far larger and dominates the board: for the unproven, option value is
  ~55-89% of their whole value (Smillie 87%, Green 89%, Goad 85%), collapsing correctly as they prove out
  (Sheezel 0.9%, Daicos 1.4%).
- **Implied premium (empirical forward-outcome dist, washouts=0, matched draft-state, same value map):** built
  from 1,194 resolved ND cohorts (debut≤2020) via `fwd_best3_from`. Compared apples-to-apples through the SAME
  zero-evidence draft ref's convex map. See the coverage table below.
- **Shortfall (implied − engine), value-weighted, draft-state:** **NEGATIVE in every young band**
  (≤21 −141, 22-24 −117, 25-26 −109 SCAR/player-equiv). i.e. the engine is **NOT** averaging young upside away —
  on net it applies *more* convex uplift than the empirical outcome distribution warrants, driven by an optimistic
  band CENTRE for deep picks and over-stated bust risk for elite MIDs. This **confirms** the pulled
  "19-22 over-optimism" diagnosis rather than overturning it.
- **Proposed correction shape → HOLD, with one narrow RAISE.** HOLD young value board-wide (the convex premium is
  adequate-to-generous; a broad raise would worsen the over-optimism and is unwarranted). RAISE only the genuinely
  UNDER-priced pocket: **young RUCKS picks 1-20** (coverage 0.61-0.73 — the engine's ruck band under-weights a real
  boom tail, p90≈115), and mildly KEY_FWD pk4-10 (0.80) / MID pk11-20 (0.83). Shape: lift the young-ruck upper-tail
  (q90/q97) contribution toward the empirical boom, age/tenure-gated (spare nothing below; first-year/unproven
  floor and years-4-7 survivor peak untouched). NB the ruck ceiling is the owner-set `RUC_PRIOR_CAP=1.4` (D13) —
  so this RAISE must be reconciled with that dial → **owner ruling** (see flags).
- **Over-priced flags (NOT applied — owner ruling):** 15 cohorts with coverage >1.4, headed by deep picks
  (GEN_FWD 41-70 **2.14**, GEN_DEF/KEY_DEF 41-70 ~1.7, MID 41-70 1.55) and elite top picks (MID 1-3 **2.09**,
  KEY_DEF 1-3 1.70), plus RUC 21-40 (1.59). These reflect band-centre over-optimism (the known Wave-2 lever) and
  over-stated elite-MID bust risk. FLAGGED only; this audit cannot and does not reduce them.
- **Proposed guard thresholds (candidates from measurements):**
  1. **Young floor (never craters):** keep B5 per-player floor `{1:.45,2:.35,3:.28,4:.21,5:.13,6:.09}×v0_start`
     UNCHANGED; ADD a band-aggregate regression floor — value-weighted young value must not drop below baked −2%:
     ≤21 ≥ **180,140**, 22-24 ≥ **178,224**, 25-26 ≥ **107,773** SCAR.
  2. **Convexity-premium acceptance (never collapses):** per young cohort, coverage = engine_gap/implied_gap must
     stay **≥ 0.60** (current min 0.61 @ RUC pk4-10 — the board just passes; this locks the floor). Ceiling **1.60**
     for the over-flag (current max 2.14; existing >1.60 grandfathered as flagged, not auto-failed). Also lock the
     `_cvx` layer: band-value-weighted `_cvx−1` ≥ current −0.5pt (≤21 ≥ 2.7%, 22-24 ≥ 3.7%, 25-26 ≥ 1.3%).
  3. **Peak preservation:** reuse B1 — years-4-6 cohort-curve peak index must not fall > **2%** vs baked
     (B1 already gates AVG[peak]>100 & pre-peak dips <5%).
- **Time:** estimate 3-5 build-hours confirmed up front; **actual within the 3-5h envelope** (dominated by
  engine-build wall-clock on each measurement pass).

**In plain terms:** the engine is *pricing* young upside, not averaging it away — the option-value machinery is
real, multi-layered, and for unproven kids it already makes 55-89% of their value pure upside. If anything the dial
is turned a touch too far for deep picks and elite-MID draftees (over-optimism, already on the roadmap), which we
FLAG for your ruling but do not touch. The one place young value should genuinely move UP is young ruckmen at picks
1-20, where an owner-set cap is clipping a real boom tail — and even that needs your call because it collides with
the 1.4 ruck-cap you set. So: hold young values where they are, don't raise across the board, and the only upward
move worth making is a modest, owner-approved lift to young-ruck upside.

---

## SUPPORTING DETAIL

### 1. Mechanism (where the integration lives)
| layer | location | what it integrates | young effect |
|---|---|---|---|
| A. board quadrature | `_merged_recover.py:111-117,107-110,19-20` | forward-peak band [q10..q90]+q97, weights WQ6=[.18×5,.10] | full boom tail; v7 taper (`:190-193`) keeps ≤20 tail whole, compresses from age 22 |
| B. present-value convexity | `rl_model.py:820-844` | 5-node Gauss-Hermite over level~N(μ,s); `_cov_age` .23(≤24)/.18, `_upside_w`→0 by 31 | `_cvx∈[1.00,1.25]`; **0-game young excluded** |
| C. runway kicker | `rl_model.py:319,308-310` | `×(1+runway·elite·PMAX)`, PMAX=.25; horizon breaks at frac<0.42/age>38 | younger+elite → up to +25%, longer horizon |
| value map | `distribution_pricing.py:250-255` | `max(proj_from_peak(L), prod_floor)` — floored downside ⇒ convex | hockey-stick: 0 below repl, explodes above |

### 2. Current premium by band (segmented) — value-weighted
| band | n | totEV | _cvx prem (vw, def/excl/atcap) | fwd-band E[v]/v(mean)−1 (vw) |
|---|---|---|---|---|
| ≤21 | 230 | 183,816 | +3.2% (177/53/5) | huge (unproven mean-outcome ≈ replacement) |
| 22-24 | 200 | 181,861 | +4.2% (198/2/18) | +246% |
| 25-26 | 108 | 109,972 | +1.8% (102/6/11) | +60% |
| 27+ | 267 | 184,676 | +0.6% (262/5/1) | +15% |

_(unproven vs proven split confirms the premium is an UNPROVEN-ness phenomenon: 22-24 unproven +5.6% vs proven +3.3%;
25-26 unproven +3.0% vs proven +1.7%.)_

### 3. Draft-state matched comparison — convexity coverage = engine_gap / implied_gap
(both distributions run through the same zero-evidence draft ref's convex value map; <1 = engine under-prices convexity, >1 = over)

| coverage | cohorts |
|---|---|
| **UNDER (<0.85) — RAISE candidates** | RUC 4-10 (0.61), RUC 11-20 (0.64), RUC 1-3 (0.73), KEY_FWD 4-10 (0.80), MID 11-20 (0.83) |
| well-matched (0.85–1.40) | MID 4-10/21-40, GEN_FWD 4-10/11-20/21-40, KEY_FWD 11-20/21-40, KEY_DEF 4-10/11-20/41-70, GEN_DEF 4-10, RUC 41-70 |
| **OVER (>1.40) — FLAG, owner ruling** | GEN_FWD 41-70 (2.14), MID 1-3 (2.09), GEN_DEF 41-70 (1.70), KEY_DEF 21-40 (1.70), KEY_DEF 1-3 (1.70), RUC 21-40 (1.59), MID 41-70 (1.55), GEN_DEF 21-40 (1.48), + KEY_FWD 41-70, GEN_DEF 1-3, GEN_FWD 21-40 (~1.3-1.44) |

Driver of the OVER cohorts: engine band CENTRE > empirical realized mean for deep picks (e.g. MID 41-70 eng 67 vs
emp 50; GEN_DEF 41-70 eng 67 vs emp 48) — a LEVEL over-optimism, not excess spread; plus over-stated bust risk for
elite MIDs at draft (MID 1-3 engine convexity fraction 51% vs empirical 23%, bust rate 0.00).

### 4. Method / pooling declared
- Age = chronological `2026 − _by` (store carries `_by`/`_bd`); `MA.age` is a clock construct (unreliable for banding).
- Cohort = position group × pick-bucket {1-3,4-10,11-20,21-40,41-70}; empirical n<20 → widen buckets symmetrically,
  then pool to all-picks (declared per row in the run log). Resolved pool = ND, pick present, debut ≤ 2020 (forward
  fully observed by 2026); washouts enter as `fwd_best3_from → 0`.
- Both sides valued through ONE zero-evidence draft ref per cohort (age ~20, no scoring), so the comparison isolates
  distribution shape only (value scale cancels). SCALE_DIST=1.0.
- **Caveat (stated):** the resolved pool captures store-retained washouts (bust rates up to 0.36 for deep KEY_FWD),
  but any drafted player who never entered the store is absent — this could understate bust mass and thus *understate*
  implied convexity, making the "engine over-applies" net finding conservative (robust) for the mean and directional
  for the tail.

### Files (read-only): `engine/rl_after/_merged_recover.py`, `engine/rl_after/rl_model.py`,
`engine/forward_valuation/distribution_pricing.py`, `engine/forward_valuation/conditional_prior.py`,
`engine/rl_after/bust_prior_table.json`. Reproducible harness + raw outputs committed alongside:
`young_convexity_harness.py`, `young_convexity_run.txt`, `young_convexity_out.json`.
