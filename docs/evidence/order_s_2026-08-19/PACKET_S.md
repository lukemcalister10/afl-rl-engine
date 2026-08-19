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

## 2 · S2 — THE OWNER'S COMPRESSED CAP

### 2.1 The spec, and the form that meets it

> "what if P20 was just the floor, and everything scaled in between? So someone at P10 would still
> appear a little ahead of P5, but both would be at or above the old P20. Means everyone is lifted a
> bit, but gaps between players still count."

    T_raw(s) = max( 1 − THETA_R·(s − s0), 0 )        the charge with only the ZERO clip
    C        = 1 − THETA_R·(s_pQ − s0)               the anchor ceiling, Q ∈ {15, 20}
    T'(s)    = C · ( 1 − exp( −T_raw(s)/C ) )        THE COMPRESSION

**WHY THIS FORM AND NO OTHER — the "say why" the order asked for:**

1. `T'(0) = 0`. A row at the cohort centre's crossing is untouched; the zero end of the scale does
   not move.
2. `dT'/dT_raw = exp(−T_raw/C)`, **strictly positive for every finite `T_raw`. There is no flat
   segment anywhere.** Worse play always costs strictly more. This is the owner's requirement met
   exactly rather than approximately, and it is asserted in the engine at load on a dense sweep
   (S-S4) on every board that carries the form.
3. `dT'/dT_raw → 1` as `T_raw → 0`. **The compression agrees with the uncompressed charge TO FIRST
   ORDER at the shallow end**, so it is not a rescaling of the whole line — it bends only where the
   line was going to be clipped.
4. `T' < C` everywhere, approaching `C` and never reaching it. So **every row pays at most the
   hard-clip-at-Q charge**: "both would be at or above the old P20" holds for EVERY row, not only
   for the capped ones. Asserted at load (S-S5) against both the anchor clip AND ORDER P's own p5
   clip.

**Requirements 1 and 3 — value AND slope matched at zero — fix the exponential's rate to `1/C`
uniquely. The only quantity chosen is `C`, and `C` is the anchor percentile's own `TMAX`, the SAME
object the hard clip used. THERE IS NO FREE PARAMETER BEYOND THE ANCHOR PERCENTILE.** A hard clip
fails (2); a linear rescale `T'=T_raw·C/TMAX_p5` fails (3) and moves rows that were never near the
cap; a power or logistic form needs a second constant.

### 2.2 THE MEASUREMENT THAT MATTERS MOST, AND IT SHARPENS THE OWNER'S OWN DIAGNOSIS

The charge at 38 games (`A = 0.9793`), as a share of the pedigree leg, by surplus:

| cell | s = −5 | s = −15 | s = −25 | s = −33 | s = −45 | s = −60 |
|---|---:|---:|---:|---:|---:|---:|
| ORDER P — clip at p5 | 36.65% | 79.37% | 93.28% | **97.26%** | **97.28%** | **97.28%** |
| ORDER R `R15` — clip at p15 | 36.65% | 79.37% | **90.75%** | **90.75%** | **90.75%** | **90.75%** |
| ORDER R `R20` — clip at p20 | 36.65% | 79.37% | **86.86%** | **86.86%** | **86.86%** | **86.86%** |
| **S2 — compression, p15 anchor** | 33.99% | 68.46% | 80.11% | **84.36%** | **87.53%** | **89.28%** |
| **S2 — compression, p20 anchor** | 33.55% | 66.61% | 77.53% | **81.45%** | **84.31%** | **85.80%** |

**Read the `R20` row across. Three players whose per-game records are 35 points a game apart pay the
IDENTICAL rate.** Under the compression they are strictly ordered, and the ordering is monotone all
the way down.

**AND HERE IS THE FINDING THE OWNER WILL WANT, because it is about his own earlier instruction.**
Lowering the cap RAISES the crossing, so it puts MORE rows into the tied region:

| anchor | `TMAX` | cap crossing `s_cross` | charged rows PARKED at the cap | the span of records tied together |
|---|---:|---:|---:|---:|
| p5 (ORDER P) | 21.1233 | −33.06 | *see* `CAP_S_out.txt` | |
| p15 (ORDER R) | 13.9490 | −22.15 | | |
| **p20 (ORDER R, the owner's own earlier instruction)** | **11.8950** | **−19.02** | | |

**LOWERING THE CAP MAKES THE DEFECT HE LATER NAMED WORSE, not better.** It buys relief for the
deepest rows by *widening* the band inside which performance stops mattering at all. That is exactly
why a compression and a lower cap are different instruments, and why he was right to ask for the
second thing after having asked for the first. **Counts are in §6.5 and in `CAP_S_out.txt`.**

### 2.3 The offline band and class read, at the inherited `LAMBDA`

| cell | `C` | W2 mark | worst class | PRI 1-10 | PRI 11-20 | MOD 1-20 | PRI 31-40 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ORDER P clip p5 | 21.1233 | 1.0611 | 1.2046 | +8.62% | +12.07% | +12.88% | −8.88% |
| ORDER R clip p15 | 13.9490 | 1.0690 | 1.2054 | +9.52% | +13.27% | +13.58% | −8.25% |
| ORDER R clip p20 | 11.8950 | 1.0740 | 1.2061 | +10.12% | +13.99% | **+14.06%** | −7.93% |
| **S2 compression p15** | 13.9490 | 1.0913 | 1.2155 | +12.90% | **+16.05%** | **+16.46%** | −7.07% |
| **S2 compression p20** | 11.8950 | 1.0960 | 1.2171 | +13.59% | **+16.65%** | **+17.03%** | −6.81% |

**The compression is a MUCH larger softening than the cap lever at the same anchor** — because it
reaches every row below the centre, not only the parked ones. **It buys the most sell-side relief of
anything in this packet (PRIMARY 31-40 from −8.88% to −6.81%) and it pays for that with the biggest
buy-side breaches.** These offline reads reproduce ORDER R's own BUILT numbers exactly where they
overlap (`R15` W2 1.0690, `R20` 1.0740, `R20` PRI 1-10 +10.12%), so the instrument is calibrated
against a known board before it is used on an unknown one. **The built boards are in §6 and they
are the authority.**

### 2.4 FIX A is still exact under the compression — and a falsifier fired on the way there

`FIXA_S_out.txt`. FIX A searches only a finite candidate set, which is only correct if `psi` attains
its segment maxima at endpoints. Under the hard clip `psi` is piecewise affine and that is trivial.
**Under the compression it is not, so it had to be proved.**

`psi` IS convex where `T_raw > 0` — linear plus a positive multiple of `exp` of an affine function.
**But at the ZERO CROSSING `psi'` drops from 1 to `1 − LAMBDA·A·beta`, which is a CONCAVE kink, so
the crossing must be in the candidate set.** The engine already adds it.

**THIS SEAT'S OWN FIRST VERSION OF THE CHECK LEFT IT OUT AND THE FALSIFIER FIRED, at 1.358e-02 of
`psi`.** The check was wrong, not the engine. With the crossing in the set the miss is **0.000e+00
on all 14,475 segments**, and on the mature-premium node set too. **Both runs are printed in
`FIXA_S_out.txt` so the correction is auditable rather than silently made.**

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

---

## 4 · S4 AND 6 · S6 — HANDED OFF MID-ORDER

**S4 (PG level by position) and S6 (the selection handoff audit) were re-scoped away from this seat**
on the owner's wall-clock parallelisation request, after this seat's prereg was written and pushed
but before the first engine edit. **Their predictions stand on `PREREG_S.md` §4 and §6 exactly as
written — they were written before any measurement and are not withdrawn — and they are scored by
the parallel read-only seat.** Nothing in this packet measures them and nothing here should be read
as an answer to them.

**Their results live at `docs/evidence/order_s_readonly_2026-08-19/`.**

One cross-reference this seat owes that seat, because it bears on S6 and was read in code here:
`o37_surplus`'s loop skips unplayed seasons outright (`if _gg<=0.0: continue`) and `o31_stall_run`
carries the comment *"A GAMELESS season is SKIPPED, never counted: unplayed time is D(c_u)'s channel
and counting it in both would be exactly the double-discount the no-stacking constraint forbids."*
**The no-stacking rule is explicit in the source. Whether it holds in the measured board population
is that seat's question, not this one's, and this seat does not answer it.**


---

## 8 · EVERY DISCLOSURE, AND EVERYTHING THIS SEAT COULD NOT MEASURE

- **NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED. NO PULL REQUEST WAS OPENED.
  NOTHING WAS PUSHED TO `main`.** This seat delivers prices.
- **S3 HALTS. There is no solved `LAMBDA` in this packet and there is not meant to be one.** The two
  boards `SL56` and `SL10` are the frontier's endpoints, built so the offline frontier could be
  checked against real boards. **Neither is a proposal.**
- **A FALSIFIER THIS SEAT WROTE FIRED ON ITS OWN FIRST RUN AND THE CHECK WAS WRONG, NOT THE ENGINE.**
  S-F4's first version left the zero crossing out of FIX A's candidate set and read a 1.358e-02 miss.
  Both runs are printed in `FIXA_S_out.txt`. §2.4
- **S1's two priced retentions come from TWO DIFFERENT CRITERIA and this seat does not choose between
  them.** `w = 0.47` is the optimum of the DIRECT criterion, which is what the engine does with the
  object; `w = 0.28` is the optimum of the CALIBRATED criterion, which isolates the weighting from
  mean reversion. **Both are priced. The choice is a judgement about what the surplus is FOR, and
  that is the owner's.**
- **THE RECENCY FIT IS ON A DIFFERENT PREDICTAND FROM THE ONE THE CHARGE USES.** It predicts NEXT
  SEASON's per-game production. The charge reads the surplus as a statement about a player's whole
  record to date. **Those are related but not identical objects, and the weights transfer on the
  argument that a season's worth as evidence about the near future is the right measure of its worth
  as evidence at all. That argument is stated, not proved.**
- **THE RECENCY WEIGHT IS GEOMETRIC AND ONE-PARAMETER BY CHOICE.** Richer forms — a games-dependent
  decay, an age-dependent decay, a per-class decay — were NOT priced, even though §1.5 measures that
  the optimum differs by history depth (0.20 to 0.41). **Pricing a decay that varies by cohort would
  introduce a second free parameter and this order priced the minimal form. That is a limitation.**
- **THE MATURE PREMIUM IS PRICED AS A HARD AGE-24 SWITCH, and §5.5 measures that the true object
  varies smoothly with CAREER STAGE rather than jumping at a birthday.** An age-faded premium was
  named on the prereg as an alternative and **was NOT built**. The switch is placed at 24 because
  that is where `o32_gate_bar` already goes flat and where FIX B1's own domain question sits, so it
  introduces no new constant — but it is a coarse read on a smoother object and it is disclosed as
  one. **The 200+ career-games stage band was TOO THIN TO FIT (382 rows) and is reported as unfitted
  rather than extrapolated.**
- **THE PREMIUM SURFACES HAVE NO HOLD-OUT.** ORDER P disclosed that `PG` is estimated on the same
  board's `v0` it is applied to. **The mature companion inherits exactly that defect** and it is
  unchanged, not repaired, here.
- **`BETA_sat` IS NOT MOVED** in this order. ORDER R priced that lever and this order does not
  re-price it.
- **`s0` IS NOT MOVED.** `T(s0) = 1` on every board.
- **THE PERCENTILES ARE UNWEIGHTED** — `s_p5`/`s_p15`/`s_p20` are `np.percentile` over the 4,143
  young-cohort SEASON ROWS while `s0` is a games-weighted mean over the same rows. **That
  inconsistency is ORDER P's**, carried unchanged by ORDER R and carried unchanged here so the
  compression's anchor is the same kind of object as the cap it replaces.
- **S4 AND S6 WERE HANDED OFF MID-ORDER** on the owner's parallelisation request and are NOT measured
  here. §4/§6.
- **The three draft classes over 1.14 are ORDER P's breach and this order does not repair them.** On
  the PER-CLASS reading of the class law there is no admissible `LAMBDA` anywhere on the S3 frontier.
- **The `run_panel.sh` / Guard 5 lane does not pass on this branch and did not pass before this
  order** (register v737: five stale pins on `land/order-29`, all predating ORDER P). This seat has
  not touched the workspace, `data/expected_boot.json` or `engine/forward_valuation`. The
  `engine_head` pin necessarily moves because this order edits `_merged_recover.py`; re-stamping it
  is a landing act and this order lands nothing.
- **CONTROL BOARDS AND MATRICES WERE REUSED WHERE THEY ARE PROVABLY IDENTICAL, AND THE REUSE IS
  DECLARED RATHER THAN LEFT TO BE NOTICED.** ORDER K's board `f3101883` and ORDER P's uncharged
  ceiling `73bf9617` are read off ORDER R's and ORDER P's own scratch dirs; the `QB1`, `QAB1`,
  `PBUILT` and `R20A` matrices are ORDER Q/P/R's, emitted from the identical dial line. **This seat
  proved byte-exact board identity on `SRoff`, `SB1`, `SAB1` and `SR20A` with its own edited engine
  first**, which is the stronger test.
- **NO NAMED-PLAYER TARGETS.** Not one constant in this order was chosen with any row in view and no
  row's value is an acceptance criterion. Draper, Travaglia, Barnett, Setterfield, Pickett and the
  Duursmas inform BAND-LEVEL evidence only. This is a standing prohibition in this project after a
  real error.
- **The veteran board (RL_O33) is still parked.** Nothing here touches it.

---

## 9 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_S.md` | the prereg, pushed at `218b997` **before the first engine edit**, with the S4/S6 handoff recorded on it |
| `os_recency.py` · `RECENCY_S.json` · `RECENCY_S_out.txt` | **S1** — the walk-forward recency fit, both scorings, the splits, the prereg scored |
| `os_mature.py` · `MATURE_S.json` · `MATURE_S_out.txt` | **S5** — the mature premium refit, the player-clustered bootstrap, the career-stage axis |
| `os_lambda.py` · `LAMBDA_S.json` · `LAMBDA_S_out.txt` | **S3** — the anchor reproduced, the `LAMBDA` frontier, and **S2's offline read** |
| `os_fixa.py` · `FIXA_S.json` · `FIXA_S_out.txt` | **falsifier S-F4** — FIX A's node maximum under the compression, including this seat's own wrong first check |
| `os_identity.py` · `run_identityS.sh` · `IDENTITY_S_*` | **falsifier S-F3** — FIX A's decomposition identity re-proved under every ORDER S dial, on every real row |
| `bbS.sh` · `build_allS.sh` · `BUILD_S_out.txt` | the board suite: four controls, eleven variants, the dial-implies test, eleven determinism repeats |
| `os_boards.py` · `BOARDS_S.json` · `BOARDS_S_out.txt` | totals, the build-failing identities, movers, mature-row movement, the two laws |
| `os_census.py` · `CENSUS_*.json` | the burn census, the birthday census, **the charge distribution** and the named rows, per board |
| `os_continuity.py` · `CONTINUITY_*` | continuity on every axis **including the SEASON-TURN axis**, on each board's effective constants and through the engine's own cap function |
| `os_cap.py` · `CAP_S.json` · `CAP_S_out.txt` | **S2 scored on real rows** — the parked-row counts, the pairwise gap test, the relief regressivity |
| `run_emit_S.sh` · `run_emits_S.sh` · `EMITS_S_out.txt` | the walk-forward matrices, day-0 guard pointed at ORDER K's own reference |
| `bb_noarbS.sh` · `NOARB_S_out.txt` · `t338ext_*.txt` | the disclosed no-arb instruments, md5-pinned at run |
| `os_bands.py` · `BANDS_S.json` · `BANDS_S_out.txt` | the ND band tables in **both** windows |
| `os_tables.py` · `STANDING_TABLES_S.json` · `STANDING_TABLES_S_out.txt` | the standing suite, pool arms both windows, both baselines |
| `os_pathtest.py` · `PATHTEST_S.json` · `PATHTEST_S_out.txt` | **the owner's two-limb path test on every breaching cell** |
| `os_class.py` · `CLASS_S.json` · `CLASS_S_out.txt` | the class marks on both bases and the per-class table |
| `run_measureS.sh` · `run_afterbuildS.sh` · `MEASURE_S_out.txt` · `AFTERBUILD_S_out.txt` | the sequential run chain |
