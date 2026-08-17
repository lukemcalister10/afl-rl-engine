# PREREG-LITE — ORDER E, THE DIAGNOSTIC SEAT (pushed BEFORE any measurement)

**Seat:** ORDER E diagnostic, issue #334 comment 5316425330. **STRICTLY READ-ONLY** — no engine
file, board, store or law is touched. Every price experiment is a monkeypatch on the module already
loaded in this process; nothing is written back. The only artifacts are evidence files in this
directory.

**Why this exists.** harry-dean and cooper-duff-tytler sit far below their Candidate-31 values on
the repaired Candidate 32. Three successive fixes aimed at "the age-blind lens" each failed to move
them because nobody had measured which site actually carries the money. Order C
(`docs/evidence/order_c_2026-08-17/PACKET_C.md` §5) eliminated the two normalization denominators
and named the remaining channel as "the age lens inside the production projection `Phat`". This
seat turns that phrase into numbers.

**This is a DIAGNOSTIC, not a proposal.** No predictions are registered — the point of this prereg
is that the SITE LIST is fixed before measurement, so no site can be quietly dropped when it turns
out to be inconvenient. Every site listed below gets a measured number in PACKET_E.md, including
the ones that come back as exactly zero.

---

## 1 · Lane, environment, identity

- Tree: `land/order-29` at `7d04550` (Order C's delivery HEAD), detached.
- Lane: **`RL_O32=1`** — the repaired Candidate 32 (implies `RL_O31`). `RL_O34` unset.
- Env, on every engine run: `PATH=/root/rl_venv312/bin:$PATH`, `PYTHONHASHSEED=0`,
  `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
  VECLIB_MAXIMUM_THREADS=1`, `RL_GAMMA=1.0 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72
  RL_PRIOR_TREES=400 PAR_RAMPS=22`, `RL_V0SURF_PKL=<repo>/data/v0surf.pkl`. Engine loads strictly
  sequential, one process at a time.
- **Currency.** `ev()` returns ENGINE currency. The board prints `int(round(ev / _PL_F))` with
  `_PL_F = 1.0524`. Every number in PACKET_E is quoted in **board points** (`ev/1.0524`) so it is
  comparable with the owner's 2,400 / 1,572 / 2,670 / 1,832.
- Baseline identity check, asserted before any counterfactual: dean 2400, duff-tytler 1572,
  murdock 170 on this lane — the exact repaired-C32 column of PACKET_C §5.

## 2 · Rows measured

| role | key | age | pos | career games |
|---|---|---:|---|---:|
| exhibit | harry-dean | 19 | KPD | 17 |
| exhibit | cooper-duff-tytler | 19 | KPF | 13 |
| control — mature (must be ~0 for any age-correction) | milan-murdock | 26 | SF | 17 |
| control — young mid, deep evidence | levi-ashcroft | 20 | MID | 48 |
| control — young tall NOT considered mispriced | connor-o-sullivan | 21 | KPD | 47 |
| control — young tall NOT considered mispriced (2nd) | logan-morris | 21 | KPF | 65 |

## 3 · THE SITE LIST — fixed here, measured in PACKET_E

Every site below was found by reading the production leg end-to-end for a young row on this lane.
Classification: **(a)** age-aware by design · **(b)** age-blind but consuming young output against
a mature reference · **(c)** age-irrelevant. Only class-(b) sites get a counterfactual; class (a)
and (c) sites are listed with their file:line and their reason, so the list is complete and nothing
is dropped silently.

### 3.1 · Sites inside `Phat` (the production projection core)

| # | site | file:line | class | counterfactual recipe |
|---|---|---|---|---|
| S1 | **the replacement bar in the projection loop** — `posval(base − REPL[g0/gg])` at every horizon k | `_merged_recover.py:1074-1075` (`_proj_w4`), `:1112-1114` (`_prod_floor_w4`), `rl_model.py:1089-1090` (`proj_from_peak`), `:1119-1121` (`prod_floor`); bar object = `REPL[pos] − REPL_DROP(3)` set in `price6` `_merged_recover.py:388` | **(b)** | at horizon k the row is age `a+k`; replace the flat bar with `REPL[pos] − Δ(class, clamp(a+k,18,23))` using the engine's OWN measured development gap `O32_GATE_DELTA` (`_merged_recover.py:3332-3335`), Δ=0 from age 24. Nothing else changes. |
| S2 | **the flat future discount** — `age_disc` returns the flat `LENS['bal']` rate for every age (`RL_AGE_DISC` default off) | `rl_model.py:990-1000`, consumed `_merged_recover.py:1063,1071` | **(b\*)** | set the engine's own declared, already-built dial `RL_AGE_DISC=1` at `MODE=5` (the owner's fifth ladder, `rl_model.py:_V5_KNOTS`). Reported separately because the reference here is a carry rate, not a mature output bar. |
| S3 | **the v7 q97 tail taper + its relax gate** — `asc = interp(age,[20,22,24,27],[1,.76,.58,.40])`, relax denied unless `_lvlcurr − REPL[pos] > 4` | `_merged_recover.py:733-747` | **(a)** with a **(b)** sub-gate (the `_lcr > 4` test reads the MATURE `REPL`) | age-correct the sub-gate only: `_lcr = _lvlcurr − (REPL[pos] − Δ(class, age))`. |
| S4 | **the un-compress ρ axis** — `ρ = Σ u_s·(avg_s − REPL[pos]) / Σ u_s`, normalised by the PROVEN median `RHO_DEN` | `_merged_recover.py:534-549`, consumed `:562-573` | **(b)** | age-correct the per-season margin: `avg_s − (REPL[pos] − Δ(class, age in season s))`. `RHO_DEN` untouched (it is the proven median and is a mature object by construction). |
| S5 | **the `_lvl_eff` exposure shrink** feeding the band features | `conditional_prior.py:111-118`, feature `:120-123` | **(b, minor)** | neutralize the shrink: `_lvl_eff → _lvl_wt`. |
| S6 | **the `_inferM1` upside-fade target bar** — `bar = REPL[pos] − 3.0` | `_merged_recover.py:730` | **(b)** | age-correct the bar the same way as S1. |
| S7 | **the `_est` decliner shed** — `_agemult2(age, Lc − REPL[pos])` | `_merged_recover.py:695`, `_agemult2` `:167` | **(b)** | age-correct the level-above-replacement argument. |
| S8 | **the elite/runway premium** — `elite = clip((lp/PEAK[g] − 0.97)/0.30,0,1)`, `runway = clip((25−a)/6,0,1)` | `_merged_recover.py:1091-1093` | **(c)** for elite (`lp` IS a projected peak, so peak-vs-peak is like-for-like) / **(a)** for runway | none — stated, not measured, with the reason. |
| S9 | **the growth curve** `frac(a,pa,g)` and the year-0 floor `lev = max(lev, cl)` | `rl_model.py:876-879`, `_merged_recover.py:1067-1069` | **(a)** | none. |
| S10 | **`cond_prior_band` (the b6 GBM band)** — `_age_asof` is an input feature | `conditional_prior.py:196-199`, features `:120-123` | **(a)** | none. |
| S11 | **the frozen q97 ceiling** — `q97m.predict(cp._feat(p,Y))`, same age feature, frozen pickle | `_merged_recover.py:373`, load `:86-95` | **(a)** | none. |
| S12 | **the pedigree pole** — `w·recover(perf, par)·max(0, po − pr)`, `perf = _lvl_wt`, `par = par_at(pos, pk, T)`, `wage = clip(1 − (a−20)/6, 0, 1)` | `_merged_recover.py:576-599` | **(a)** — the par is tenure-conditional and the wage is explicitly age-ramped | none, but the leg's SIZE is reported for both exhibits. |
| S13 | **`_dev_advance` / `level_now`** — rolls the level from `BASE_REF` age to `AGE_REF` age | `rl_model.py:809-819` | **(a)**, identity on the now-board (`AGE_REF == BASE_REF`) | none. |
| S14 | **`level_demo` trust/confidence** | `rl_model.py:757-807` | **(a)** (its `old` branch is age-keyed; the growth branch is the young one) | none. |
| S15 | **`_lvlcurr`** — per-group recency decay `LDECAY_G` | `_merged_recover.py:305-309` | **(c)** for age | none. |

### 3.2 · Downstream layers (the S6-emit README list) and the level readers

| # | site | file:line | class | counterfactual recipe |
|---|---|---|---|---|
| S16 | **iso remnants** — `iso_eff` pick tax faded on evidence | `_merged_recover.py:629-635` | **(c)** for age (pick-keyed) | none; the realised value for both exhibits is reported. |
| S17 | **ITEM-H `_h_cut`** — the ruled cut list | `_merged_recover.py:2343-2355` | **(c)** — pool-only cells | none; realised factor reported. |
| S18 | **D8 graded staleness** — `qv = season avg / REPL[pos]` | `_merged_recover.py:2536`, consumed `:2602-2606` | **(b)** | age-correct the denominator; report whether the enclosing tenure gate makes it inert. |
| S19 | **the decay gate** — `pr = bestlvl(p,Y)/par`, `par = _O30BP_BARS[pos]` | `_merged_recover.py:2579-2580`, consumed `:2607-2609` | **(b)** — this is ORDER C's site 2 | age-correct `par`; report inertness. |
| S20 | **ITEM C's evidence weight** — `Q = clip(sa/par, 0, 2)`, `par = _O30BP_BARS[pos]` | `_merged_recover.py:2437` | **(b)** — this is ORDER C's site 1 | age-correct `par`; report which consumers are live on this lane. |
| S21 | **KPF compression** | `_merged_recover.py:2556-2571` | **(a)** — explicitly gated `age >= 24` | none. |
| S22 | **the L1c young credit** — `mult = 1 + w·R·φ(g)`, `φ(g) = (1 − g/46)²`, keyed on CAREER GAMES, never on age | `_merged_recover.py:1169-1186`, applied `:1192-1195` | **(b)** — age-blind on an evidence-quantity axis | two bounded directions: (i) neutralize (`mult → 1.0`) to size what is currently paid; (ii) age-key it (`φ → 1` for rows under 24) to size the headroom. |
| S23 | **the M3 clock blend** | `_merged_recover.py:2637-2652` | **(a)** — in-progress-season clock pin | none; report the realised `s` for both exhibits. |
| S24 | **`_PL_F`** — the certified board factor 1.0524 | `_merged_recover.py:1496` | **(c)** — uniform | none. |
| S25 | **the ORDER-31 production weight `rho31(g)`** and its complement the pedigree leg `π(g,c_u,s)·v0` | `_merged_recover.py:3428-3437` (`rho31`), `:3543-3561` (`o31_pi`), blend `:3564-3566` | **(b)** — keyed on career games, so a 19-year-old with 17 games is judged "thin evidence" identically to a 27-year-old with 17 career games | NOT a `Phat` site and it is the RULED re-mix. Measured only as a BOUND, one term at a time: (i) `O32_ETA = 0` (the g-keyed pedigree de-rate PACKET_C §5.4 names for dean's −270); (ii) `rho31 → 1` with the pedigree leg held, reported as an upper bound and explicitly NOT a proposal. |
| S26 | **the `_lvl_wt` / `_lvl_eff` / `_exposure` recency readers** and `_est` hold/shed | `conditional_prior.py:100-118`, `_merged_recover.py:686-695` | **(c)** for age (recency/evidence axes) | none; documented by `docs/evidence/order34_recency_2026-08-17/PACKET_RECENCY.md`. |

## 4 · Joint counterfactuals

The decomposition is NOT expected to be additive (S1 changes the level at which S4's ramp and the
band's own nonlinearities bite). Both individual and joint numbers are reported. The joints that
will be run: **the top-2 by |Δdean|+|ΔCDT|**, **the top-3**, and **all class-(b) sites inside
`Phat` together (S1+S3+S4+S5+S6+S7)**.

## 5 · The class and band side-effects

Under the TOP counterfactual (whichever it turns out to be) and under the minimal set that reaches
the owner-expected neighbourhood, if one exists:

- **the year-1 class**: every live board row in its first year after the draft
  (`type == 'ND'`, `2026 − draft year == 1`, active, non-pool), re-priced whole; the class total,
  the class mean, and the mean ratio to the year-0 anchor are reported with the row count.
- **the five-band year-1 economics**: the same rows split into picks 1-10 / 11-20 / 21-30 / 31-40 /
  41-64, reporting mean(year-1 price) / mean(year-0 anchor) − 1 per band, i.e. the yr0→1
  appreciation the standing two-sided suite watches. The halt condition is a band above **+14%**
  (buy-side red past the carry rule).
- **DISCLOSED LIMITATION, registered here so it cannot be presented as anything else:** the
  committed five-band instrument (`docs/evidence/candidate_31f/ext_2026-08-17/
  t338_extended_DISCLOSED.py`) reads a WALK-FORWARD per-entrant matrix (2004-2022 classes) emitted
  by `emit_matrix_338.py`, which is a full multi-thousand-row re-price. If that matrix is not
  rebuilt under the counterfactual within this seat's budget, the band numbers reported will be the
  **live-2026-board draft-clock proxy** described above and will be LABELLED as the proxy at every
  appearance, with the committed C32R walk-forward table quoted beside it for reference. A proxy
  will never be presented as the standing instrument's number.

## 6 · Honesty rules this seat pre-commits to

1. This is a diagnostic. The output is "site X costs Y points, verified". No wiring recommendation
   beyond that sentence.
2. Where a counterfactual cannot cleanly isolate a site — shared state, a nonlinear coupling, a
   patched function reached by more than one caller — that is SAID and the effect is BOUNDED, not
   quoted to false precision.
3. Every number carries its perturbation recipe (the exact monkeypatch), so any reader can
   reproduce it.
4. Sites that come back at exactly 0.0 are reported at exactly 0.0, with the gate that makes them
   inert named. An inert site is a finding, not an omission.
5. If no minimal set reaches dean ~2,600 / CDT ~1,800 without breaching the +14% early-band rule,
   PACKET_E says so in its first paragraph.

*— ORDER E diagnostic seat. Read-only. Nothing lands, nothing is proposed.*
