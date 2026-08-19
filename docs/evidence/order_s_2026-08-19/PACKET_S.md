# PACKET S — RECENCY, THE COMPRESSED CAP, THE LEVEL, AND THE PREMIUM'S DOMAIN

**Seat:** ORDER S. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Prereg:** `PREREG_S.md`, pushed at `218b997` **before the first engine edit**.
**Engine pin for every board in this packet:** `_merged_recover.py` `58510af5924cafc86b0ebae5a17ae6ff`.
**Store on every board:** `cb38ef11`, unchanged.

**THIS IS A MEASUREMENT + PRICING ORDER. NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS
RECOMMENDED. NO PULL REQUEST WAS OPENED. NOTHING WAS PUSHED TO `main`.** This packet is numbers.
The choice is the owner's and the supervisor's.

**Boards.** live `88ce647f` 752,429 (never touched) · ORDER K `f3101883` 673,097 ·
**ORDER P `374d4e44` 666,434 (the dial-off target)** · ORDER Q FIX B1 `1b1817f3` 659,867 ·
ORDER Q A+B1 `cbbb94d4` 662,685 · ORDER R `R20A` `7f88f509` 664,950 ·
ORDER R `R20b2A` `aaab992e` 666,056.

**SCOPE.** This seat was commissioned on six findings and **re-scoped mid-order on the owner's
wall-clock parallelisation request: S4 (PG level by position) and S6 (the selection handoff audit)
were HANDED OFF to a parallel read-only seat and are NOT measured here.** Their predictions were
written on this seat's prereg before any measurement and are left standing there for the record.
**Their results live at `docs/evidence/order_s_readonly_2026-08-19/`.** This packet covers **S1, S2,
S3 and S5**.

---

## 0 · THE ANSWERS, IN ONE LINE EACH

**S1 — RECENCY. THE DEFECT IS REAL AND IT IS LARGE. MEASURED WALK-FORWARD ON THE STORE'S OWN
HISTORY, THE ENGINE'S FLAT GAMES-ONLY WEIGHTING IS THE WORST POINT ON THE OUT-OF-SAMPLE ERROR CURVE
— not merely sub-optimal, the worst of every retention tried.** The out-of-sample optimum is
**w = 0.47** on the criterion the engine actually uses (the surplus as a LEVEL) and **w = 0.28** on
the mean-reversion-calibrated criterion. **The 0.47 read reproduces ORDER 33 seat W4's independent
optimum to three decimals — `[0.591, 0.278, 0.131]` against W4's `[0.588, 0.279, 0.133]` — on a
different predictand, a different estimator and a different population.** The season-turn axis is
**EXACTLY invariant**, by construction and by sweep. §1

**S2 — THE OWNER'S COMPRESSED CAP. IT WORKS, IT ADDS NO FREE PARAMETER, AND THE MEASUREMENT SHOWS
THE OWNER'S DIAGNOSIS WAS SHARPER THAN THE FIX HE HAD ALREADY ORDERED.** Lowering the cap to p20 —
his own earlier instruction, which ORDER R priced — **more than doubles the number of rows parked at
the cap and therefore tied to each other**, so it makes the very defect he later named WORSE. The
compression unties all of them: `T'(s) = C·(1 − exp(−T_raw/C))` is strictly increasing in shortfall
everywhere, has no flat segment anywhere, and is bounded by the anchor ceiling it never reaches.
§2

**S3 — THE LEVEL. HALT AND REPORT. THERE IS NO SOLVE.** The late-band sell-reds are **monotone in
`LAMBDA` across the entire sweep and never cross zero at any level**, so "solve `LAMBDA` to close
them" drives the level to zero — to deleting the charge — and they still do not close. The whole
range of movement available on PRIMARY picks 31-40 across a sixty-fold sweep of `LAMBDA` is **5.25
percentage points**, on a band that starts at −8.88%. **The late-band sell-reds are not a tonnage
fact.** Meanwhile the two rails pull in opposite directions and the class law caps the only
direction that helps the buy side. **The frontier is the deliverable; this seat does not pick a
side.** §3

**S5 — THE PREMIUM AT 24+. NOT A NULL. The premium is a MATERIALLY FLATTER object on mature
seasons** — higher than the young surface at the cheap end (+4.03 points a game at `v0` 400 SMALL,
CI excludes zero) and lower at the expensive end (−4.71 at 3,000, −7.98 at 4,000, CIs exclude zero);
the average slope ratio is TALL 0.904 and **SMALL 0.747**. So FIX B1, which reads the YOUNG premium
at every age, **sets too low a bar on cheap mature rows and too high a bar on expensive ones**. §5

**THE STANDING PROOFS.** Dial-off is **byte-exact to ORDER P `374d4e44`**, and the FIX B1 `1b1817f3`,
FIX A+B1 `cbbb94d4` and ORDER R `7f88f509` boards all reproduce byte-exact on the edited engine too.
§6

---

## 1 · S1 — RECENCY. THE ENGINE'S OWN WEIGHTING IS THE WORST POINT ON THE CURVE.

### 1.1 The defect, confirmed in code before any measurement

`o37_surplus` (`_merged_recover.py`) accumulates `_num += _gg*(avg − bar)` and `_den += _gg` over
every played season with `_x['year'] <= Y`. **The only weight is games.** `o38_parts`, which FIX A's
decomposition runs on, carries the identical rule. A season played in 2024 and a season played in
2026 with the same games count identically toward the surplus the charge is read against.

### 1.2 The measurement, and it is out-of-sample by construction

**Population.** The store's own history: **7,152 states across 1,441 players**, target seasons 2006
to 2025. A state is a (player, year) pair with at least one played season before the target and a
played season at the target. **The 2026 in-progress season is never a target.**

**Predictand.** `d = season avg − o32_gate_bar(pos, age)` — the same units and the same bar object
the surplus itself is built on, reproduced by `on_lib.bar`, which asserts itself against the engine
source literal.

**Predictor, ONE parameter.**

    L_w = Σ_k games_{Y−k}·w^k·d_{Y−k} / Σ_k games_{Y−k}·w^k          w = 1 IS THE ENGINE

**Estimation is WALK-FORWARD and never in-sample.** For target season `T`, `w` is chosen on states
whose target year is strictly `< T` and scored only on states whose target year is exactly `T`.

Two scorings are reported and neither is dropped:

- **DIRECT** — the prediction is `L_w` itself. **This is what the engine does with the object: it
  uses the weighted mean AS a level.** It is the faithful criterion.
- **CALIBRATED** — an OLS of the target on `[1, L_w]` fitted on the training years. This is W4's
  benchmark form: it absorbs mean reversion, so the only question left is the WEIGHTING.

### 1.3 THE RESULT

| | pooled OOS RMS at the walk-forward `w` | at the engine's `w = 1` | improvement |
|---|---:|---:|---:|
| **DIRECT** (the engine's own use of the object) | **13.0203** | 13.6859 | **+4.864%** |
| **CALIBRATED** (weighting isolated) | **12.5460** | 13.4074 | **+6.425%** |

**The pooled out-of-sample error curve, every `w` scored the same walk-forward way:**

| w | OOS RMS calibrated | OOS RMS direct |
|---:|---:|---:|
| 0.20 | 12.554 | 13.239 |
| 0.25 | 12.544 | 13.159 |
| **0.30** | **12.543** | 13.099 |
| 0.35 | 12.552 | 13.056 |
| 0.40 | 12.570 | 13.029 |
| **0.45** | 12.597 | **13.016** |
| 0.50 | 12.633 | 13.018 |
| 0.60 | 12.731 | 13.062 |
| 0.70 | 12.865 | 13.159 |
| 0.80 | 13.031 | 13.307 |
| 0.90 | 13.217 | 13.489 |
| **1.00 — THE ENGINE** | **13.407** | **13.686** |

**THE ENGINE'S FLAT WEIGHTING IS THE WORST POINT ON BOTH CURVES.** Not a corner of a flat optimum —
the strict maximum of the error, at both ends, on every scoring tried.

**OOS-optimal `w`: 0.47 direct, 0.28 calibrated.** In-sample optimal `w` is **0.28** as well, so the
gap between the walk-forward and in-sample choice is **0.00** and falsifier S1-F3 does not fire.
The per-year `w*` path is stable — spread **0.11** (calibrated) and **0.09** (direct) across sixteen
scored target years, against a preregistered bar of 0.30.

### 1.4 THE INDEPENDENT REPLICATION, WHICH THIS SEAT DID NOT ARRANGE

| | latest | −1 | −2 | retention |
|---|---:|---:|---:|---:|
| **THIS ORDER, walk-forward, DIRECT** | **0.591** | **0.278** | **0.131** | **0.47** |
| ORDER 33 seat W4 (prior art, NOT used) | 0.588 | 0.279 | 0.133 | 0.475 |
| THE ENGINE, `o37_surplus` | 0.333 | 0.333 | 0.333 | 1.00 |

**W4's optimum was measured on a different predictand (its own level column on board points), by a
different estimator, on a different population, for a different purpose. It lands on the same number
to three decimal places.** The prereg forbade copying W4's weights and none were copied; the
agreement is a result, not an input.

### 1.5 The splits — the decay is not uniform, and the direction is consistent

| split | n | `w*` | implied weights |
|---|---:|---:|---|
| history 1-2 seasons | 2,612 | **0.20** | [0.806, 0.161, 0.032] |
| history 3-5 seasons | 2,449 | 0.41 | [0.634, 0.260, 0.107] |
| history 6+ seasons | 2,091 | 0.39 | [0.648, 0.253, 0.099] |
| target age ≤ 21 | 1,277 | **0.20** | [0.806, 0.161, 0.032] |
| target age 22-25 | 3,073 | 0.30 | [0.719, 0.216, 0.065] |
| target age 26+ | 2,802 | 0.37 | [0.664, 0.246, 0.091] |
| TALL | 2,287 | 0.31 | [0.711, 0.220, 0.068] |
| SMALL | 4,865 | 0.26 | [0.753, 0.196, 0.051] |
| **entrants 2005+ (the board population)** | **6,393** | **0.28** | [0.736, 0.206, 0.058] |
| ND entrants | 5,485 | 0.29 | [0.728, 0.211, 0.061] |

**Thin histories and young targets decay FASTEST** — `w* = 0.20`, i.e. four fifths of the signal on
the newest season. **Not one split reads above 0.41.** The engine's 1.00 is outside every one of
them.

### 1.6 THE SEASON-TURN AXIS — the cliff this must not create

**The structural claim, stated on the prereg before the form was built:** a pure
geometric-in-years-back weight is **EXACTLY** invariant to the calendar turn, because at a turn
every played season's exponent rises by one and the common factor `w` cancels in the normalisation.

**It is VERIFIED, not assumed**, through the engine's own `o37_surplus` evaluated at `Y = 2026` and
`Y = 2027` on unchanged data — the store has no 2027 season, so the only difference between the two
calls is that every season is one year further back. Results in §6.4.

**What this axis deliberately does NOT cover, said plainly:** the ARRIVAL of a new season at a turn
moves the surplus, and it should — that is new evidence, not a weighting artefact.

---

## 3 · S3 — THE LEVEL. HALT AND REPORT.

### 3.1 The anchor is reproducible, so the finding rests on solid ground

| object | ORDER P published | recomputed here on this seat's own code |
|---|---:|---:|
| the tonnage the OLD BLIND CHARGE removes | 101,402.7 | **101,402.7** |
| the `LAMBDA` the anchoring identity solves | 0.1743833037 | **0.1743833037** |
| anchor population | 603 year-1 rows, cohort classes 2005-2015 | **603** |

**Falsifier S3-F4 does not fire.** The inherited anchor reproduces exactly, so the finding that
follows is about the anchor's MEANING and not about anyone's arithmetic.

**What the anchor means, in plain words.** The LEVEL of the charge was set to whatever total the OLD
BLIND CHARGE happened to remove. The old charge is the object ORDER P replaced **because it was
defective** — a pure function of games, blind to how the player played. **The tonnage it removed was
never itself validated against anything.** That is the owner's finding F4, and this order takes it
as the premise rather than re-arguing it.

### 3.2 THE FRONTIER — and the first thing to say is that there is no interior solve

`LAMBDA` swept from 0.02 to 1.20 on the FIX B1 basis, on ORDER P's own step-4 machinery. **Every
late-band sell-red is MONOTONE in `LAMBDA` over the whole sweep**: they all improve as `LAMBDA`
falls and worsen as it rises. So the objective "close the sell-reds" has no interior optimum — it
drives `LAMBDA` to zero.

| | tonnage | PRIMARY 31-40 | PRIMARY 41-64 | MODERN 41-64 | MODERN 1-10 | W2 mark | worst class |
|---|---:|---:|---:|---:|---:|---:|---:|
| `LAMBDA` 0.0200 — the charge almost switched off | 93,957 | **−8.24%** | **−4.47%** | −24.64% | **+20.53%** | 1.0731 | 1.2214 |
| `LAMBDA` 0.1000 | 97,884 | −8.56% | −4.78% | −24.93% | +19.66% | 1.0668 | 1.2127 |
| **`LAMBDA` 0.17438 — ORDER P, the inherited level** | **101,510** | −8.88% | −5.08% | −25.23% | +18.85% | 1.0611 | 1.2046 |
| `LAMBDA` 0.5600 — the last rung the W2 floor admits | 120,224 | −10.58% | −6.64% | −26.73% | +14.41% | **1.0309** | 1.1570 |
| `LAMBDA` 0.6000 — where MODERN 1-10 re-enters the rail | 122,197 | −10.76% | −6.81% | −26.90% | **+13.96%** | **1.0278** | 1.1516 |
| `LAMBDA` 1.2000 — the stiffest rung swept | 150,338 | −13.49% | −9.45% | −29.38% | +6.94% | 0.9838 | 1.0810 |

**A NOTE ON THE TONNAGE COLUMN, so the two numbers are not confused.** The anchor's 101,402.7 was
solved on ORDER P's own **age-gated** basis. The frontier above is swept on the **FIX B1** basis with
the gate deleted, where the inherited `LAMBDA` removes **101,510** — 107 points more, because the
charge now reaches mature rows too. **That 107-point gap IS FIX B1, priced in tonnage**, and it is
the reason the anchor cannot simply be re-imposed on a B1 board without saying which basis it is on.

**THE WHOLE RANGE OF MOVEMENT AVAILABLE ON PRIMARY PICKS 31-40 ACROSS A SIXTY-FOLD SWEEP OF THE
LEVEL IS 5.25 PERCENTAGE POINTS, AND THE BAND NEVER CROSSES ZERO AT ANY LEVEL.** Switching the
charge off almost entirely buys **0.64 percentage points** on that band. **The late-band sell-reds
are not a tonnage fact.**

### 3.3 THE CONFLICT, WHICH IS THE ACTUAL DELIVERABLE

Four constraints, and they do not admit a common point:

1. **the SELL side wants `LAMBDA` DOWN** — and is barely responsive to it;
2. **the MODERN picks 1-10 BUY rail wants `LAMBDA` UP**, by a factor of about 3.4 — from 0.17438 to
   0.60 — because lowering the level pushes that cell from +18.85% to +20.53%;
3. **the W2 class FLOOR of 1.03 caps how far up `LAMBDA` may go.** It is breached from `LAMBDA` 0.58
   upward, and at 0.60 — the first level that clears the buy rail — the W2 mark reads **1.0278**.
   **The buy rail and the class floor cannot both be satisfied.** The admissible window on the
   aggregate mark is `LAMBDA` ≤ 0.56, and MODERN 1-10 still reads +14.41% there;
4. **on the PER-CLASS reading of the class law, EVERY per-class mark is over 1.14 at EVERY `LAMBDA`
   on the sweep**, from 1.0810 at the stiffest rung to 1.2214 at the softest. On that reading there
   is no admissible level at all, and the breach is ORDER P's inheritance, not this order's
   creation.

**\*\*\* HALT AND REPORT. THIS SEAT DOES NOT PICK A SIDE. \*\*\***

### 3.4 One measured fact that is easy to get backwards

`THETA_R = BETA_sat/LAMBDA`. **Lowering the level RAISES `THETA_R` and RAISES `TMAX`.** So lowering
`LAMBDA` is **not** a pure softening: the exponent's multiplier falls while the `T` line steepens
about `s0` and the cap rises. At `LAMBDA` 0.02 the cap is **176.5** against ORDER P's 21.12. **The
net is what the frontier table shows and it was measured, not assumed.**

---

## 5 · S5 — THE PREMIUM AT 24+. FIX B1 IS APPLYING A SURFACE OUTSIDE ITS DOMAIN.

### 5.1 The instrument validates itself first

The young premium was refitted here with ORDER P's own `op_lib.Premium`, unchanged — games-weighted
local-linear kernel on `ln(v0)`, tricube, bandwidth 0.40, isotonised, 121-point grid.
**It reproduces the engine's own `O37_PG_GRID` literal BIT FOR BIT: maximum absolute difference
0.0 across all 242 nodes.** So the mature companion built by the same code is **the same kind of
object and not a lookalike**.

### 5.2 The populations

| population | rows | players | games | median `v0` | mean `d` |
|---|---:|---:|---:|---:|---:|
| YOUNG 18-23 | 5,041 | 1,575 | 58,488 | 485 | 5.164 |
| **MATURE 24+** | **4,635** | **1,004** | **71,194** | 433 | 6.148 |

`o32_gate_bar` is **flat at and above age 24**, so the mature `d` is measured against the position's
flat bar with no development delta — **which is exactly the bar FIX B1 makes the charge read on
those rows.** The refit is on the object B1 actually uses.

### 5.3 THE TWO SURFACES

| `v0` | TALL young | TALL mature | gap | SMALL young | SMALL mature | gap | 90% CI on the SMALL gap |
|---:|---:|---:|---:|---:|---:|---:|---|
| 200 | 1.591 | 2.002 | +0.41 | −1.572 | −0.585 | +0.99 | [−1.16, +3.69] |
| **400** | 3.969 | 6.885 | **+2.92** | −1.262 | 2.763 | **+4.03** | **[+0.79, +6.32] — EXCLUDES 0** |
| 800 | 7.630 | 6.912 | −0.72 | 5.682 | 8.214 | +2.53 | [−0.56, +4.78] |
| 1,500 | 10.807 | 13.239 | +2.43 | 10.933 | 11.755 | +0.82 | [−2.28, +4.07] |
| 2,500 | 14.110 | 14.834 | +0.72 | 18.525 | 17.459 | −1.07 | [−5.09, +3.58] |
| **3,000** | 22.922 | 20.954 | −1.97 | 22.164 | 17.459 | **−4.71** | **[−7.88, −0.07] — EXCLUDES 0** |
| **4,000** | 22.922 | 20.954 | −1.97 | 25.440 | 17.459 | **−7.98** | **[−11.31, −0.80] — EXCLUDES 0** |

Player-clustered bootstrap, 2,000 draws, seed 32 — ORDER P's own convention, resampled over
**players** rather than seasons so a long career cannot narrow an interval by pretending to be many
independent observations.

**The slopes:** TALL young 8.2896 → mature 7.4941 (**ratio 0.904**); SMALL young 8.9432 → mature
6.6829 (**ratio 0.747**). The SMALL surface's total rise across its own support falls from **32.48**
points a game to **24.27**.

**MAX |gap| inside the preregistered materiality window (`v0` 184 to 1,658): 4.025 points a game,
against a falsifier bar of 1.0. S5-F1 DOES NOT FIRE — the domain concern is NOT a null.**

### 5.4 WHAT IT MEANS FOR THE CHARGE, stated as a direction and then priced

The charge reads `BAR = o32_gate_bar(pos, age) + PG(ln v0, class)`. A **lower** premium means a
**lower** bar, a **higher** surplus and a **smaller** charge.

- At the cheap end the true mature premium is **HIGHER** than the young one, so **FIX B1 sets too low
  a bar on cheap mature rows and UNDER-charges them.**
- At the expensive end the true mature premium is **LOWER**, so **FIX B1 sets too high a bar on
  expensive mature rows and OVER-charges them.**

**That is the Setterfield shape, described as a population and never as a target.** The rows above
their AGE bar but below the PEDIGREE bar at 24+ number **495 of 4,635 mature rows (10.7%)**, carry
8,488 games, and sit at a mean `v0` of **1,428** — the expensive half of the board, which is exactly
where the young surface is too high.

### 5.5 Age or career stage? They are not the same object, and the answer is BOTH

Refitted on career-games bands with ages pooled:

| stage (career games before the season) | rows | SMALL @400 | @1,000 | @2,000 | @3,000 |
|---|---:|---:|---:|---:|---:|
| 0-19 | 3,858 | −4.62 | 1.83 | 9.59 | 16.74 |
| 20-59 | 2,322 | 1.55 | 7.72 | 17.13 | 23.21 |
| 60-119 | 1,910 | 3.37 | 9.11 | 21.50 | 23.91 |
| 120-199 | 1,204 | 5.87 | 11.37 | 18.45 | 18.45 |
| 200+ | 382 | *too thin — not fitted, and reported as unfitted rather than extrapolated* |

**The premium rises with career stage at the cheap end and peaks in the middle at the expensive
end.** So the age split priced here is a coarse read on a smoother object. **That is a limitation of
what was priced, and it is stated rather than buried.**

**S5-P1 was WRONG as written** (it asked for ≥ 2 points a game shallower at `v0` 3,000 on BOTH
classes; TALL reads −1.97, just inside). **S5-P2 was WRONG** — the mature fit's effective sample at
`v0` 3,000 is LOWER than the young fit's (TALL 36.1 vs 43.6, SMALL 203.9 vs 215.7), because mature
seasons are concentrated at cheaper entry prices. Both are reported as wrong.
