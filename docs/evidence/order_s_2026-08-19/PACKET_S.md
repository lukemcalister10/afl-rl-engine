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
**EXACTLY invariant** — largest move in the charge factor **2.22e-16, one unit in the last place** —
by construction and by sweep. **BUT THE PRICED VARIANT IS A STIFFENING, NOT A SOFTENING** (−506
board points), **it does not move the year-1 rails AT ALL for a structural reason** (a year-1 row has
one season and a weighted mean over one season is that season under every `w`), and **it reaches
exactly ONE of the three staleness failure modes the parallel seat mapped.** §1, §1.7, §6.8

**S2 — THE OWNER'S COMPRESSED CAP. IT WORKS, IT ADDS NO FREE PARAMETER, AND THE MEASUREMENT SHOWS
THE OWNER'S DIAGNOSIS WAS SHARPER THAN THE FIX HE HAD ALREADY ORDERED.** Lowering the cap to p20 —
his own earlier instruction, which ORDER R priced — **takes the population of rows PARKED at the cap,
and therefore tied to each other, from 12 to 97 — EIGHT TIMES — and widens the band of records inside
which performance stops mattering from 36.7 to 51.0 points a game.** It makes the very defect he
later named WORSE. The
compression unties all of them: **at exactly equal career games it has ZERO inversions and ZERO ties
on all 1,067 pairs, where ORDER P's p5 clip has 9 and ORDER R's p20 clip has 120.** It is also **the
largest single softening in the whole ORDER P/Q/R/S arc (+8,193 against FIX B1)**, it cuts the
relief the deepest decile captures from 99% to 50%, and **it is the only instrument in this packet
that closes a standing sell-red** — PRIMARY picks 21-64 crosses zero for the first time. It pays for
that with buy-side breaches, all of which PASS the owner's loosened-rail path test in the PRIMARY
window. §2, §6.5, §6.7, §6.8, §6.9

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
at every age, **sets too low a bar on cheap mature rows and too high a bar on expensive ones**.
**BUT PRICING THE REPAIR MAKES FIX B1's MATURE-ROW COST WORSE, NOT BETTER — −6,567 to −7,064 — the
opposite of what this seat predicted**, because most mature rows are CHEAP and the cheap end is
where the young surface was too LOW. §5, §6.11

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

### 1.7 WHAT THE RECENCY FIX REACHES, AND WHAT IT CANNOT REACH

**The parallel read-only seat's T2 audit (`docs/evidence/order_s_readonly_2026-08-19/PACKET_SRO.md`)
maps THREE staleness failure modes. This seat's variant reaches ONE of them. That bound is stated
here, in this seat's own packet, rather than left for someone to find.**

| # | the failure mode, as that seat measured it | population | does S1's recency weighting reach it? |
|---|---|---:|---|
| **1** | **the charge weights three-year-old evidence at full weight.** `s_P` reads played seasons with no date at all; the median board row is charged against evidence **2.03 seasons old** at full weight | the whole charged population | **YES. This is exactly and only what `RL_O40_RECW` changes.** |
| **2** | **staleness entirely unpriced by BOTH mechanisms.** A row one season out sits at `c_u ≤ 1` where the fade schedule is 1.000, AND the charge is silent — not because the season is under-weighted but because **it is ABSENT from `s_P` altogether** | **19 of 53 stale rows**, 10 of which move under one board point | **NO, AND IT NEVER CAN.** Reweighting the seasons a row DID play cannot make the charge read a season he did not play. There is no term to reweight. |
| **3** | **the clock credit is a step, not a rate.** `o31_played_units` credits `min(1, games/2)`, so a two-game season buys the same full unit of sitter clock a twenty-two-game season buys | **217 board rows** have at least one 1-2 game season; 120 inside the last four | **NO.** That is the sitter machinery's own clock, and no dial in this order touches it. |

**Said as plainly as it can be said: a recency weighting makes the charge read RECENT EVIDENCE more
heavily. It does not make the charge read the ABSENCE of evidence at all.** The two most expensive
stale rows on the whole board — 4,339 and 3,196 board points, neither having played in 2026 — are in
mode 2, and **`RL_O40_RECW` moves neither of them for that reason**, because both have played
seasons only and nothing to reweight toward a season that is not there.

**THIS SEAT DOES NOT EXTEND ITS SCOPE TO MODE 2.** Whether the charge should read MISSING seasons is
a rulings-level design question — it changes what the surplus IS, not how it is weighted — and it
belongs to the owner, not to a tuning dial. **Mode 3 is likewise untouched and is the sitter
machinery's, not the charge's.**

**Any claim that this order's recency fix "prices non-selection" would be false, and this packet says
so before anyone can make it.**

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

**ONE READING NOTE ON THE ENGINE BANNER, so a number on it is not misread.** The banner prints "a row
at the effective cap with 38 games is charged 86.86%" on a p20 compression board — the SAME figure a
p20 hard clip prints. That is correct and it is the compression's ASYMPTOTE: `T' → C`, so the
supremum charge equals the clip's charge at the same anchor. **No real row reaches it: the deepest
charge actually observed on `SC20` is 81.59%** (§6.6). The ceiling is shared; the approach to it is
what differs.

**AND WHERE THE ASSERTS RUN, stated because it is easy to assume wrongly.** The ORDER S banner and
its structural asserts sit at MODULE scope and execute on every load of `_merged_recover.py`,
including inside every board build. **The banner TEXT does not appear in `export_stdout.txt` — the
export path does not carry that stream — so the banner is shown in this packet from an in-process
load on the identical dial line. The asserts themselves are plain statements and would have failed
the build; the boards exist, so they passed.** The same is true of ORDER P's, Q's and R's asserts and
was true before this order.

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

| anchor | `TMAX` | cap crossing `s_cross` | **charged rows PARKED at the cap** | **the span of records tied together** |
|---|---:|---:|---:|---:|
| p5 (ORDER P) | 21.1233 | −33.06 | **12** | 36.7 pts a game |
| p15 (ORDER R) | 13.9490 | −22.15 | **64** | 47.9 |
| **p20 (ORDER R, the owner's own earlier instruction)** | **11.8950** | **−19.02** | **97** | **51.0** |

**LOWERING THE CAP MAKES THE DEFECT HE LATER NAMED WORSE, not better.** It buys relief for the
deepest rows by *widening* the band inside which performance stops mattering at all. That is exactly
why a compression and a lower cap are different instruments, and why he was right to ask for the
second thing after having asked for the first. **Eight times the tied population, and 14.3 more points a game of record inside the tie. Full detail in §6.5 and `CAP_S_out.txt`.**

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

### 5.6 IS THE YOUNG/MATURE GAP REALLY AN AGE EFFECT? THE POSITION-COMPOSITION CROSS-CHECK

**The parallel seat's T1 found the PG LEVEL by position is NOT a null** — SD over-barred by 2.978
points a game `[−4.329, −1.661]`, RUCK by 5.57 `[−8.18, −2.90]`, SF UNDER-barred by 2.709
`[+1.83, +3.67]`, with MID/KPD/KPF nulls and the offsets summing to zero within each class.

**That creates a live confound for this section and it has to be ruled out rather than ignored.** If
the mature population's POSITION mix differs from the young one, part of the young-to-mature premium
gap measured above would be a composition effect wearing an age costume.

**MEASURED. The mix does shift, and the shift is far too small to carry the gap:**

| class | position | young games share | mature games share | shift |
|---|---|---:|---:|---:|
| TALL | KPD | 36.3% | 40.9% | +4.6 |
| TALL | KPF | 50.6% | 38.8% | **−11.8** |
| TALL | RUCK | 13.1% | 20.3% | +7.2 |
| SMALL | MID | 37.5% | 36.7% | −0.8 |
| SMALL | SD | 26.0% | 30.2% | +4.2 |
| SMALL | SF | 36.6% | 33.1% | −3.4 |

Weighting those shifts by **the parallel seat's OWN published level offsets** (KPD and KPF nulls
carried as zero) gives the composition-implied change in each class's mean position level:

- **TALL: −0.399 points a game.**
- **SMALL: −0.214 points a game.**

**Against measured young-to-mature premium gaps of +4.03 at `v0` 400 and −4.71 at `v0` 3,000, the
composition effect is under a tenth of the signal and it has the WRONG SHAPE — it is a single
constant offset, while the measured gap CHANGES SIGN across the price axis.** A level shift cannot
produce a sign change. **The young/mature difference is an age/stage effect, not a position-mix
artefact.**

**THE TWO OBJECTS ARE KEPT DISTINCT AND NEITHER ABSORBS THE OTHER.** T1's finding is about the
POSITION axis of the bar; S5's is about the AGE axis of the premium. `RL_O40_PGMAT` changes the
premium surface read on mature seasons and **does not touch any position term** — the position bar
`o32_gate_bar(pos, age)` is untouched by every dial in this order. **If a position-level repair is
ever adopted it must be applied to the position bar, not folded into the premium, or the two would
double-count.** This packet prices no position repair and recommends none.

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

## 6 · THE BOARDS. EVERY BUILD-LEVEL IDENTITY PASSES.

**Twenty-seven boards. ONE engine md5 across all of them: `58510af5`. ONE store: `cb38ef11`.**

### 6.1 The identities that would have failed the build

| # | check | result |
|---|---|---|
| **S-F0** | every ORDER S dial unset does not rebuild ORDER P `374d4e44` byte-exact | **no — `374d4e44`** |
| — | + `RL_O38B1` does not rebuild FIX B1 `1b1817f3` | **no — `1b1817f3`** |
| — | + `RL_O38A RL_O38B1` does not rebuild FIX A+B1 `cbbb94d4` | **no — `cbbb94d4`** |
| — | + `RL_O39_TMAXPCT=20` does not rebuild **ORDER R's own `R20A` `7f88f509`** | **no — `7f88f509`** |
| **S-D1** | `RL_O38B1` + the S2 dials ALONE do not carry the O37/O36/O35/O32/O31 stack | **no — `fcca7db8` both ways** |
| **S-D2** | determinism x2 fails on any variant | **no — all ELEVEN identical on a repeat** |
| **S-F1** | `LAMBDA·THETA_R ≠ BETA_sat` at load | **no — asserted at 1e-15 on every board** |
| **S-F2** | `TMAX` is stale rather than recomputed from the effective `THETA_R` | **no — asserted at 1e-12 on every board** |
| **S-S1/2/3** | `T` rises with surplus · the factor leaves (0,1] · `A(0) ≠ 0` | **no — asserted on a dense sweep at load** |
| **S-S4** | the compression has a FLAT SEGMENT | **no — 0 ties on 22,001 sweep points, every compression board** |
| **S-S5** | the compression charges MORE than the clip it replaces, at any surplus | **no — asserted against the anchor clip AND ORDER P's p5 clip** |
| **S-F3** | FIX A's decomposition stops reconstructing `o37_surplus` under the new dials | **no — worst 1.776e-14 on 715 rows, all EIGHT dial lines** |
| **S-F4** | FIX A's node maximum is not exact under the compression | **no — 0.000e+00 on 14,475 segments** *(and see §2.4 — the first version of this check was wrong and fired)* |
| **the law** | any row with ZERO CAREER GAMES moves | **no — 0 of 89 on every variant** |
| **the law** | any row prices above its own uncharged price (`73bf9617`) | **no — 0 of 804 on every variant** |
| — | FIX A lowers a price rather than only capping a charge | **no — 0 rows on every A-on pair** |
| — | day-0 printed rows | **89 of 89 print EXACTLY, on all 27 builds** |

### 6.2 THE BOARDS

| board | cell | md5 | total | vs ORDER P | vs ORDER K | vs FIX B1 |
|---|---|---|---:|---:|---:|---:|
| ORDER K | — | `f3101883` | 673,097 | +6,663 | — | +13,230 |
| **ORDER P** | dial-off | `374d4e44` | **666,434** | — | −6,663 | +6,567 |
| SB1 | FIX B1, the control | `1b1817f3` | 659,867 | −6,567 | −13,230 | — |
| SAB1 | FIX A+B1 | `cbbb94d4` | 662,685 | −3,749 | −10,412 | +2,818 |
| SR20A | ORDER R p20 CLIP + A | `7f88f509` | 664,950 | −1,484 | −8,147 | +5,083 |
| **SW47** | **S1 recency w = 0.47** | `e8278e5a` | **659,361** | −7,073 | −13,736 | **−506** |
| **SW28** | S1 recency w = 0.28 | `7240540c` | 659,049 | −7,385 | −14,048 | **−818** |
| SW47A | S1 w = 0.47 + A | `5f93d8c2` | 662,490 | −3,944 | −10,607 | +2,623 |
| **SC15** | **S2 compression p15** | `08e5f1a5` | **666,901** | **+467** | −6,196 | **+7,034** |
| **SC20** | **S2 compression p20** | `fcca7db8` | **668,060** | **+1,626** | −5,037 | **+8,193** |
| **SC20A** | **S2 compression p20 + A** | `eeb9b650` | **669,506** | **+3,072** | −3,591 | **+9,639** |
| SL56 | S3 `LAMBDA` 0.56 | `2db7ef05` | 651,204 | −15,230 | −21,893 | −8,663 |
| SL10 | S3 `LAMBDA` 0.10 | `e85a1c54` | 661,569 | −4,865 | −11,528 | +1,702 |
| **SM** | **S5 mature premium** | `61ebbb60` | **659,370** | −7,064 | −13,727 | **−497** |
| SMA | S5 mature + A | `ee388c2e` | 662,126 | −4,308 | −10,971 | +2,259 |
| **SALL** | all four + A, the far corner | `5e2e36f1` | **668,806** | **+2,372** | −4,291 | **+8,939** |
| Peta0 | the UNCHARGED ceiling | `73bf9617` | 702,734 | +36,300 | +29,637 | +42,867 |

**THE HEADLINE, AND IT IS NOT WHAT THE ORDER'S FRAMING ASSUMED: TWO OF THE FOUR REPAIRS ARE
STIFFENINGS, NOT SOFTENINGS.**

- **The recency weighting REMOVES points** — 506 at `w = 0.47`, 818 at `w = 0.28`. Weighting recent
  seasons more heavily charges MORE in aggregate, because the population the charge reaches is
  dominated by rows whose recent seasons are their worse ones. **S1-P4 predicted `|Δ| < 4,000` and
  is RIGHT; the DIRECTION was not predicted and it is reported as unpredicted.**
- **The mature premium also removes points** — 497. §6.6.
- **The compression is by far the largest single softening in the whole ORDER P/Q/R/S arc: +8,193
  against FIX B1, against FIX A's +2,818 and ORDER R's p20 clip at +5,083.**

### 6.3 ADDITIVITY

| combination | additive prediction | actual | gap | % of board |
|---|---:|---:|---:|---:|
| `SW47A` = SW47 + A | 662,179 | 662,490 | +311 | +0.047% |
| `SMA` = SM + A | 662,188 | 662,126 | −62 | −0.009% |
| `SC20A` = SC20 + A | 670,878 | 669,506 | **−1,372** | **−0.205%** |
| `SALL` = SW47 + SC20 + SM + A | 669,875 | 668,806 | −1,069 | −0.160% |

**The recency and mature repairs are additive with FIX A to within a twentieth of a percent. The
COMPRESSION is not** — it gives FIX A 1,372 points less to work with, for the same reason ORDER R
measured on its own cap lever: **softening and monotonising are partly the same job.**

### 6.4 CONTINUITY — INCLUDING THE AXIS S1 HAD TO BE TESTED ON

| axis | every ORDER S board |
|---|---|
| **THE SEASON TURN**, `o37_surplus` at Y and Y+1 on unchanged data | **largest move in the charge factor 2.220446e-16 — ONE UNIT IN THE LAST PLACE.** S1-F2 does not fire. **The turn is EXACTLY invariant, as the prereg claimed and as the cancellation requires.** |
| AGE, the charge factor, 18-30 at 20 games | **0.0000 at every age** (every variant carries FIX B1) |
| AGE, the price, every real row re-priced one year older | **0 rows move** |
| GAMES, the charge across 0-400 at 0.01, seven surplus levels | the charge rises with games at **0 of 280,000** |
| SURPLUS, across 100 points at 0.01 | a better player charged more at **0 of 10,000** |

**S1-P3 IS RIGHT AND IT IS THE PREDICTION THIS SEAT MOST WANTED TO BE RIGHT ABOUT.** The geometric
form cannot create a calendar cliff, because at a turn every exponent rises by one and the common
factor cancels in the normalisation. Measured, not assumed: the residual is one ULP of a double.

### 6.5 S2 ON REAL ROWS — THE PARKED POPULATION AND THE PAIRWISE TEST

**How many charged rows are PARKED at the cap, and how far apart their records are:**

| anchor | `TMAX` | crossing | **rows parked** | their `s_ped` range | **span tied away** |
|---|---:|---:|---:|---|---:|
| p5 — ORDER P | 21.1233 | −33.06 | **12** | −70.1 .. −33.3 | 36.7 pts a game |
| p15 — ORDER R | 13.9489 | −22.15 | **64** | −70.1 .. −22.2 | 47.9 |
| **p20 — ORDER R, the owner's own earlier instruction** | 11.8950 | −19.02 | **97** | −70.1 .. −19.1 | **51.0** |

**Lowering the cap from p5 to p20 takes the tied population from 12 rows to 97 — EIGHT TIMES — and
widens the band of records inside which performance stops mattering from 36.7 to 51.0 points a
game.** The owner's earlier instruction and his later diagnosis point in opposite directions, and
this is the number that shows it.

**THE DECISIVE TEST. Every pair of charged rows at EXACTLY equal career games**, so `A(g)` is held
fixed and the record is the only thing left. Pairs where both rows are charged nothing are dropped —
both are producing above their bar and a tie at zero is the mechanism working, not the cap.

| board | pairs | **inverted** | of which exact **TIES** | **worst gap tied away** |
|---|---:|---:|---:|---:|
| SB1 — ORDER P's p5 clip | 1,067 | 9 | 9 | 25.83 pts a game |
| **SR20A — ORDER R's p20 CLIP + A** | 1,067 | **120** | **104** | **47.56** |
| **SC15 — the compression, p15** | 1,067 | **0** | **0** | **0.00** |
| **SC20 — the compression, p20** | 1,067 | **0** | **0** | **0.00** |
| SC20A — the compression p20 + FIX A | 1,067 | 10 | **0** | **0.00** |
| SALL | 1,117 | 7 | **0** | **0.00** |

**S2-P3 IS CONFIRMED EXACTLY. On the compression with FIX A off, worse per-game play costs strictly
more on ALL 1,067 equal-games pairs — zero inversions, zero ties.** ORDER R's p20 clip inverts 120
of them and ties 104. **The ten residual inversions on `SC20A` carry ZERO ties: they are FIX A's own
entry-price cap doing its job, not the surplus cap, and they are reported as what they are.**

### 6.6 THE CHARGE DISTRIBUTION, AND WHICH REPAIRS SOFTEN

| board | n | **max charge** | **>90%** | >75% | >50% |
|---|---:|---:|---:|---:|---:|
| SB1 — ORDER P's clip + B1 | 715 | 97.28% | **20** | 119 | 237 |
| SAB1 | 715 | 95.73% | 19 | 106 | 221 |
| SR20A — ORDER R p20 clip + A | 715 | 87.44% | **0** | 98 | 218 |
| **SC15 — compression p15** | 715 | **84.50%** | **0** | **32** | 193 |
| **SC20 — compression p20** | 715 | **81.59%** | **0** | **17** | 186 |
| **SC20A — compression p20 + A** | 715 | **81.59%** | **0** | **16** | **178** |
| **SW47 — recency 0.47** | 715 | **97.49%** | **31** | **142** | **272** |
| SW47A | 715 | 97.26% | 27 | 129 | 258 |
| **SM — mature premium** | 715 | **97.28%** | **28** | 123 | 250 |
| SMA | 715 | 96.05% | 24 | 112 | 236 |
| **SL56 — `LAMBDA` 0.56** | 715 | **98.13%** | **51** | 167 | 316 |
| SL10 — `LAMBDA` 0.10 | 715 | 97.07% | 15 | 108 | 222 |
| SALL | 715 | 83.61% | **0** | 37 | 236 |

**The compression moves the WHOLE distribution, not just its tail — `>75%` falls from 119 rows to
17, where ORDER R's cap lever only took it to 98.** That is the difference between an instrument that
reaches rows parked at the cap and one that reaches every row below the cohort centre.

**And the two stiffening repairs are visible here too: recency takes `>90%` from 20 rows to 31 and
`>50%` from 237 to 272.** A recency-weighted surplus is a HARSHER charge on this board.

### 6.7 RELIEF REGRESSIVITY — the owner's second F1 question, answered

Relief against the ORDER P baseline, in points of the pedigree leg, by decile of `s_ped` on the
baseline board. **D1 is the deepest tenth.**

| lever | total relief | D1 | D2 | D3 | D4 | D5 | D6+ |
|---|---:|---:|---:|---:|---:|---:|---:|
| **ORDER R's p20 CLIP + A** | 663.0 | **99%** | 1% | 0 | 0 | 0 | 0 |
| **S2 COMPRESSION p20 + A** | **2,133.1** | **50%** | 19% | 18% | 6% | 6% | 1% |
| S2 compression p15 | 2,199.3 | 42% | 17% | 20% | 9% | 10% | 1% |
| S2 compression p20 | 2,540.5 | 42% | 17% | 20% | 9% | 11% | 1% |

**S2-P4 IS RIGHT. The cap-lowering lever puts 99% of its relief in the single deepest decile. The
compression puts 50% there and spreads the rest down the distribution — and it delivers more than
three times as much relief in total.** That is the regressivity the owner named, measured, and
reduced.

### 6.8 THE RAILS, BOTH WINDOWS

**PRIMARY window, cohorts 2005-2023.** Below 0% is a SELL-side red; above +14% is a BUY-side red.

| board | ALL 1-64 | 1-20 | 21-64 | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ORDER K | +4.23% | +9.22% | −3.67% | +8.22% | +11.16% | +5.26% | −10.70% | −6.89% |
| **ORDER P** | +5.33% | +9.79% | −1.73% | +8.62% | +12.07% | +7.37% | −8.88% | −5.03% |
| QB1 / **SW47** | +5.34% | +9.79% | −1.69% | +8.62% | +12.07% | +7.54% | −8.88% | −5.08% |
| QAB1 / **SW47A** | +6.45% | +11.59% | −1.66% | +11.18% | +12.38% | +7.57% | −8.88% | −5.03% |
| SR20A | +7.81% | +13.14% | −0.62% | +12.56% | **+14.26% BUY** | +9.02% | −7.93% | −4.33% |
| **SC20** | +9.26% | **+14.63% BUY** | **+0.77%** | +13.59% | **+16.65% BUY** | +10.90% | **−6.81%** | **−3.23%** |
| **SC20A** | +9.67% | **+15.30% BUY** | **+0.78%** | **+14.58% BUY** | **+16.71% BUY** | +10.91% | −6.81% | −3.20% |
| SM | +5.33% | +9.79% | −1.71% | +8.62% | +12.07% | +7.54% | −8.91% | −5.13% |
| **SALL** | +9.67% | **+15.30% BUY** | **+0.76%** | **+14.58% BUY** | **+16.71% BUY** | +10.91% | −6.83% | −3.24% |

**MODERN window, cohorts 2019-2023.**

| board | ALL 1-64 | 1-20 | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **ORDER P** | +1.45% | +12.88% | **+18.85% BUY** | +1.94% | −13.84% | −11.73% | −24.88% |
| QB1 / **SW47** | +1.40% | +12.88% | **+18.85%** | +1.94% | −13.84% | −11.73% | −25.23% |
| QAB1 / **SW47A** | +2.36% | **+14.41% BUY** | **+20.83%** | +2.66% | −13.82% | −11.73% | −25.15% |
| SR20A | +3.46% | **+15.53% BUY** | **+21.78%** | +4.08% | −12.36% | −10.63% | −24.53% |
| **SC20** | +4.82% | **+17.03% BUY** | **+22.87%** | +6.34% | **−11.01%** | **−9.90%** | **−23.23%** |
| **SC20A** | +5.23% | **+17.68% BUY** | **+23.78%** | +6.52% | −11.00% | −9.90% | −23.19% |
| SM | +1.40% | +12.88% | +18.85% | +1.94% | −13.84% | −11.73% | −25.26% |
| **SALL** | +5.23% | **+17.68% BUY** | **+23.78%** | +6.52% | −11.00% | −9.90% | −23.20% |

**THREE THINGS HAVE TO BE SAID ABOUT THESE TABLES.**

1. **THE RECENCY WEIGHTING DOES NOT MOVE THE RAILS AT ALL, AND THE REASON IS STRUCTURAL, NOT
   NUMERICAL.** `SW47` reproduces `QB1` on every band in both windows to the last decimal, and
   `SW47A` reproduces `QAB1`. **A year-1 cell reads a row that has played AT MOST ONE SEASON, and a
   weighted mean over one season is that season under EVERY `w`.** The recency dial is INVISIBLE at
   year 1 by construction. It moves prices only where a row has a history to re-weight, which the
   year-1 rails never see. **That is a real and previously unstated property of the rail instrument
   and it is reported here as a finding, not a convenience.**
2. **THE COMPRESSION IS THE ONLY INSTRUMENT IN THIS PACKET THAT CLOSES A STANDING SELL-RED.** PRIMARY
   picks 21-64 has been red on ORDER K (−3.67%), ORDER P (−1.73%) and every ORDER Q and R cell.
   **`SC20` takes it to +0.77% and `SC20A` to +0.78% — it crosses zero.** Picks 31-40 improve from
   −8.88% to −6.81% and 41-64 from −5.03% to −3.20%, both the best in the whole arc.
3. **It pays for that on the buy side.** PRIMARY 1-20 and 11-20 breach, and MODERN 1-10 goes from
   ORDER P's already-breaching +18.85% to +23.78%.

### 6.9 THE OWNER'S PATH TEST ON EVERY BREACHING CELL

Carry compounds at 14%: 1.140 / 1.300 / 1.482 / 1.689 / 1.925 / 2.195 / 2.502.
**27 breaching ND cells across all twelve boards. 9 PASS. 18 FAIL.**

**EVERY NEW BREACH THE COMPRESSION CREATES IN THE PRIMARY WINDOW PASSES THE OWNER'S LOOSENED RAIL:**

| band | board | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | limb (a) | limb (b) | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| PRIMARY 1-10 | **SC20A** | +14.58% | 1.230 | 1.384 | 1.524 | 1.493 | 1.402 | 1.231 | pass | pass | **PASSES** |
| PRIMARY 1-10 | **SALL** | +14.58% | 1.235 | 1.390 | 1.531 | 1.493 | 1.397 | 1.227 | pass | pass | **PASSES** |
| PRIMARY 1-20 | **SC20** | +14.63% | 1.238 | 1.377 | 1.527 | 1.537 | 1.456 | 1.300 | pass | pass | **PASSES** |
| PRIMARY 1-20 | **SC20A** | +15.30% | 1.250 | 1.385 | 1.533 | 1.540 | 1.458 | 1.302 | pass | pass | **PASSES** |
| PRIMARY 1-20 | **SALL** | +15.30% | 1.254 | 1.392 | 1.538 | 1.540 | 1.454 | 1.298 | pass | pass | **PASSES** |
| PRIMARY 11-20 | **SC20** | +16.65% | 1.285 | 1.386 | 1.548 | 1.631 | 1.565 | 1.441 | pass | pass | **PASSES** |
| PRIMARY 11-20 | **SC20A** | +16.71% | 1.287 | 1.389 | 1.550 | 1.632 | 1.566 | 1.442 | pass | pass | **PASSES** |
| PRIMARY 11-20 | **SALL** | +16.71% | 1.292 | 1.394 | 1.552 | 1.633 | 1.563 | 1.438 | pass | pass | **PASSES** |
| PRIMARY 11-20 | SR20A *(ORDER R's, reproduced)* | +14.26% | 1.268 | 1.371 | 1.536 | 1.623 | 1.559 | 1.438 | pass | pass | **PASSES** |

**Every one of them breaches in year 1 and then behaves exactly as the owner said a breach must: it
never beats carry again, and it ENDS FALLING and far under carry (1.23-1.44 against 2.502).**

**THE CELLS THAT FAIL ARE THE MODERN ONES, AND THEY ARE INHERITED, NOT CREATED.**

| cell | boards | limb (a) | limb (b) | the failure, in words |
|---|---:|---|---|---|
| MODERN picks 1-10 | 11, **including ORDER P itself** | pass | **FAIL** | still RISING at the end: yr6 1.40 → yr7 1.59 |
| MODERN picks 1-20 | 7, including **ORDER Q's `QAB1`** | pass | **FAIL** | still RISING at the end: yr6 1.33 → yr7 1.54 |
| SSP arm, both windows | every board including ORDER K | **FAIL(2)** | pass | beats carry in years 2 and 3 |

**MODERN 1-10 fails on ORDER P itself and the SSP arm fails on ORDER K itself. `SW47A` and `SMA`
breach MODERN 1-20 at exactly `QAB1`'s +14.41% — the same number, because the recency dial is
invisible at year 1 — so they inherit ORDER Q's failure rather than creating one.** The compression
makes the level of these inherited failures worse; it does not change the verdict.

**THE WEAKNESS IN THE TEST, CARRIED FROM ORDER R AND NOT BURIED:** limb (b) reads years 6 and 7 on
FEWER ROWS than year 1 — on MODERN picks 1-20 the counts run 100/100/100/100/100/80/60/40. **The limb
that decides every one of these failures is read on 40 of the 100 rows that produced the breach.**

### 6.10 THE CLASS MARKS

| board | **W2 mark (the rail's basis)** | cohort clock | worst single class | at cohort |
|---|---:|---:|---:|---:|
| ORDER K | 1.0513 | 1.0324 | 1.1363 | 2012 |
| **ORDER P** | **1.0613** | 1.0322 | **1.2047** | 2016 |
| QB1 / **SW47** | 1.0611 | 1.0321 | 1.2046 | 2016 |
| QAB1 / **SW47A** | 1.0696 | 1.0409 | 1.2083 | 2016 |
| SR20A | 1.0820 | 1.0552 | 1.2098 | 2016 |
| **SC20** | **1.0960** | 1.0696 | 1.2171 | 2016 |
| **SC20A** | **1.0992** | 1.0729 | 1.2192 | 2016 |
| **SM** | **1.0606** | 1.0316 | **1.2044** | 2016 |
| SMA | 1.0692 | 1.0405 | 1.2080 | 2016 |
| **SALL** | **1.0989** | 1.0726 | 1.2190 | 2016 |

**EVERY VARIANT IS INSIDE THE OWNER'S LAW ON THE REGISTERED W2 BASIS: above the 1.03 floor and under
the 1.14 rail.** The instrument was validated first — it reproduces ORDER P's own published mark
`1.0613` to `−0.0000`. **S2-P5 is RIGHT.**

**AND THE BAD HALF, REPORTED AS BADLY AS IT READS.** The three draft classes ORDER P put over 1.14
(2010 1.1570, 2011 1.1595, 2015 1.2047) are **not repaired by anything in this order, and the
compression makes all three worse** — the worst single class goes 1.2047 → 1.2192. **`SM`, the
mature premium, is the ONLY cell in the whole packet that improves it, and only to 1.2044.** This
remains an open ruling from ORDER P.

### 6.11 MATURE-ROW MOVEMENT — AND S5's PREDICTION IS WRONG IN DIRECTION

"Mature" is aged 24 and over: the 429 rows byte-identical to ORDER K under ORDER P.

| board | rows 24+ | moving | **net vs ORDER K** |
|---|---:|---:|---:|
| **SB1 — FIX B1, the cost S5 was aimed at** | 429 | 245 | **−6,567** |
| SAB1 | 429 | 245 | −6,106 |
| **SM — the mature premium** | 429 | **255** | **−7,064** |
| SMA | 429 | 253 | −6,665 |
| SC20 — the compression | 429 | 247 | **−4,887** |
| SC20A | 429 | 246 | **−4,672** |
| SW47 — recency | 429 | 274 | −7,646 |
| SW28 | 429 | 287 | −8,212 |
| SALL | 429 | 289 | −6,036 |

**S5-P3 IS WRONG, AND WRONG IN DIRECTION.** The prereg predicted the mature refit would cut B1's
mature-row cost by more than 20%. **It makes it 7.6% WORSE: −6,567 → −7,064.**

**Why, measured rather than excused.** The prediction looked at the EXPENSIVE end, where the mature
premium is lower and the charge therefore falls. But the mature population's median entry price is
**433**, and at the cheap end the mature premium is HIGHER than the young one (+4.03 points a game
at `v0` 400 SMALL). **A higher premium is a higher bar, a lower surplus and a BIGGER charge. Most
mature rows are cheap, so the cheap end wins the aggregate.** The domain defect is real and
two-sided, and correcting it costs the veterans money rather than giving it back.

**The instrument that actually shrinks B1's mature cost is the COMPRESSION** — −6,567 to −4,887 —
and it was not aimed at that population at all.

### 6.12 THE POOL ARMS, AND THE ENTRY-YEAR CONTROL

Year-1 appreciation by pool arm, both windows, on the all-arm instrument's own cohort semantics.
MSD has no year-1 cell by construction (he debuts in his draft year); those rows are excluded and
counted in words, never scored zero.

| board | PRIMARY ALLPOOL | RD | IRE | SSP | MODERN ALLPOOL | RD |
|---|---:|---:|---:|---:|---:|---:|
| ORDER K | −4.93% | −3.39% | +13.34% | **+52.71% BUY** | −10.47% | −20.41% |
| **ORDER P** | −3.60% | −1.86% | +13.62% | **+58.17% BUY** | −8.99% | −19.74% |
| QB1 / **SW47** | −3.77% | −2.04% | **+14.04% BUY** | +56.71% | −9.76% | −20.48% |
| QAB1 / **SW47A** | −3.73% | −2.00% | **+14.04% BUY** | +56.96% | −9.66% | −20.37% |
| SR20A | −3.18% | −1.39% | **+14.58% BUY** | +57.21% | −9.44% | −20.05% |
| **SC20** | **−2.30%** | **−0.51%** | **+14.98% BUY** | +58.44% | **−8.59%** | **−19.20%** |
| SC20A | −2.29% | −0.49% | +14.98% | +58.44% | −8.59% | −19.20% |
| SM | −3.93% | −2.21% | +14.02% | +56.55% | −9.84% | −20.53% |
| **SALL** | −2.40% | −0.60% | +14.96% | +58.32% | −8.64% | −19.24% |

**The compression improves every pool sell-side arm and takes RD from −1.86% to −0.51%, the closest
to flat anywhere in the arc, without closing it.** The **IRE** arm's +14% breach is **ORDER Q FIX
B1's**, inherited by every cell here (QB1 already reads +14.04%), and the **SSP** arm has been over
the rail since ORDER K. **Neither is created by this order and neither is repaired by it.**

**THE ENTRY-YEAR CONTROL PASSES ON EVERY BOARD** — every year-0 cell is inside ±0.1%. The dials in
this order are production and charge corrections and a day-0 row has no production, so its entry
price must not move; it does not.

### 6.13 THE TWO ROW-LEVEL PREDICTIONS, SCORED

**S1-P5 — the recency dial's row-level shape.** The prereg said rows whose bad seasons are OLD would
gain and rows whose bad seasons are RECENT would lose, with a correlation above +0.8 between the
price move and the surplus move.

| | rows | net price |
|---|---:|---:|
| surplus RISES under recency (recent seasons better than old) | 291 | **+2,246** |
| surplus FALLS under recency (recent seasons worse than old) | 321 | **−2,752** |
| **net** | | **−506** |

**The SIGN STRUCTURE is exactly as predicted. The CORRELATION is +0.3525, not +0.8, and the reason
is measured rather than excused: the charge is FLAT above the cohort centre.** A row already
producing above its bar pays nothing and cannot be made to pay less, however much its surplus rises;
a row below the bar pays more the moment its recent seasons are its worse ones. **So a roughly
symmetric change in the surplus (291 up, 321 down) produces a one-sided change in the board.** That
asymmetry IS the answer to why a recency weighting stiffens rather than softens, and it was not
foreseen on the prereg.

**S5-P4 — the watched shape.** Rows aged 24+, ABOVE their age bar and BELOW their pedigree bar,
under `SM` against `SB1`:

| population | rows | movers | net points | per moving row |
|---|---:|---:|---:|---:|
| **the watched shape** | 61 | 45 | −153 | **−3.4** |
| other 24+ | 365 | 104 | −344 | −3.3 |
| **under 24** | **289** | **0** | **+0** | **0.0** |

**The prediction is right by a whisker and this seat reports it as effectively a NULL:** −3.4 against
−3.3 is not a distinction worth defending. **What IS worth stating is the third row: not one row
under 24 moves under the mature dial, which is the structural confirmation that `RL_O40_PGMAT`
touches only rows with a season at 24 or over — measured, not asserted.**

**These are POPULATIONS, not players. No named row gated any number and no row's value is an
acceptance criterion.**

---

## 7 · PREDICTIONS SCORED. NINETEEN WERE WRITTEN. SIX WERE WRONG.

| # | prediction, written before the first measurement | outcome |
|---|---|---|
| **S1-P1** | the OOS-optimal `w` lies strictly inside (0.30, 0.85) | **WRONG on the calibrated read** — 0.28, just outside. **RIGHT on the direct read** — 0.47 |
| S1-P2 | the per-year `w*` path is stable, spread ≤ 0.30 | **RIGHT** — 0.11 calibrated, 0.09 direct |
| **S1-P3** | the season-turn sweep produces a step of EXACTLY 0.0000 | **RIGHT** — 2.22e-16, one ULP |
| S1-P4 | recency moves rows both ways, `\|total − B1\| < 4,000` | **RIGHT** — −506 and −818. **The DIRECTION was not predicted: recency is a STIFFENING** |
| **S1-P5** | rows with OLD bad seasons gain and rows with RECENT bad seasons lose; correlation > +0.8 | **WRONG on the number, RIGHT on the shape** — r = +0.3525. The sign structure is exactly as predicted; the correlation is weak for a measured reason, §6.12 |
| S2-P1 | the compression is softer than the clip at the same anchor everywhere | **RIGHT** — +8,193 against +5,083, max charge 81.59% against 87.44%, and 0 rows lower on the board |
| **S2-P2** | at p20 the max charge falls below 80% | **WRONG, narrowly** — 81.59%. Directionally right, the bar was too tight |
| **S2-P3** | 0 inversions in shortfall on a dense pair sweep | **RIGHT, and exactly** — 0 of 1,067 equal-games pairs on both A-off compression boards |
| **S2-P4** | the compression concentrates less relief in the deepest decile | **RIGHT** — 50% against the cap lever's 99% |
| S2-P5 | the W2 mark rises and stays under 1.14 | **RIGHT** — 1.0992, with 0.0408 of room |
| S3-P1 | the solved `LAMBDA` is below 0.17438, tonnage below 101,402.7 | **RIGHT in direction and USELESS in size** — the objective is monotone, so there is no solve |
| S3-P2 | the aggregate W2 mark does not bind first | **RIGHT** — it admits 0.02 to 0.56 |
| S3-P3 | the per-class reading binds immediately and is already breached | **RIGHT** — every per-class mark is over 1.14 at every `LAMBDA` |
| **S3-P4** | the late-band sell-reds do not close at any admissible `LAMBDA` | **RIGHT, and more strongly than written** — they do not close at ANY `LAMBDA` at all, admissible or not |
| S3-P5 | lowering `LAMBDA` is not a pure softening; `THETA_R` and `TMAX` rise | **RIGHT** — at `LAMBDA` 0.02 the cap is 176.5 against 21.12 |
| **S5-P1** | the mature premium is ≥ 2 pts a game shallower at `v0` 3,000 on both classes | **WRONG** — SMALL −4.71, TALL −1.97 |
| **S5-P2** | the mature fit's ESS at `v0` 3,000 exceeds the young fit's | **WRONG** — 36.1 against 43.6 (TALL), 203.9 against 215.7 (SMALL) |
| **S5-P3** | pricing the mature refit cuts B1's mature-row cost by > 20% | **WRONG IN DIRECTION** — it makes it 7.6% worse, −6,567 → −7,064 |
| **S5-P4** | the Setterfield-shaped population moves most under the mature refit | **RIGHT BY A WHISKER, AND REPORTED AS EFFECTIVELY A NULL** — −3.4 points per moving row against −3.3 for other mature rows, §6.13 |

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
- **TWO SCORER BUGS OF THIS SEAT'S OWN FIRED AND BOTH ARE REPORTED RATHER THAN QUIETLY FIXED.**
  (a) `os_census.py` was ORDER R's scorer and unpacked `o38_parts` as a THREE-tuple; this order makes
  it return FIVE (the two mature sub-shares are appended so the `RL_O40_PGMAT` decomposition stays
  exact). **Fourteen of fifteen censuses raised on the first pass and were re-run after the fix** —
  `rerun_censusS.sh`, and the raised runs are still on disk in `os_census_*_run.txt`.
  (b) `os_cap.py`'s first pairwise run **did not exclude pairs where BOTH rows are charged nothing**,
  and so counted the ZERO-CLIP region as if it were the cap: it reported 475 "ties" on a compression
  board that has none. The exclusion is stated in the file. **Neither bug touched an engine, a board
  or a dial — both were in this seat's own reading of boards already built.**
- **S-F4 FIRED ON THIS SEAT'S OWN FIRST VERSION AND THE CHECK WAS WRONG, NOT THE ENGINE.** §2.4.
- **THE RECENCY DIAL DOES NOT MOVE THE YEAR-1 RAILS AT ALL, AND THAT IS STRUCTURAL.** A year-1 cell
  reads rows that have played at most one season, and a weighted mean over one season is that season
  under every `w`. `SW47` reproduces `QB1` on every band in both windows to the last decimal.
  **Anyone reading the rail tables should know the recency dial is INVISIBLE to that instrument by
  construction, not because it does nothing.** §6.8
- **CONTINUITY WAS RUN ON NINE CELLS, NOT FIFTEEN, AND THE NINE ARE NAMED IN `run_measureS.sh`.**
  Both controls, both recency cells (the only ones that can move the season-turn axis), both
  compression cells (the only ones that change the shape of `T`), both mature cells and the far
  corner. `SW28`, `SC15` and the two `LAMBDA` endpoints were not swept. **Every ORDER S variant
  carries FIX B1, which collapses the 23→24 age step to exactly zero on every cell, so the age axis
  is structurally identical across all eleven. THIS IS A WALL-CLOCK CHOICE AND IT IS DISCLOSED.**
- **SEVEN WALK-FORWARD MATRICES WERE EMITTED, NOT ELEVEN.** `SW28`, `SC15`, `SL56` and `SL10` have
  BOARDS, CENSUSES and totals but **no standing no-arb tables of their own**. `SC15`'s bands are
  bracketed by `SB1` and `SC20`; `SW28`'s by `SB1` and `SW47`, which are themselves identical to
  `QB1` on the rails; and **S3 HALTS, so the two `LAMBDA` endpoints have no proposal to test rails
  against — their frontier is delivered offline over 61 rungs on machinery first validated against
  ORDER R's BUILT boards.** **This is a real gap in coverage and it is named rather than papered
  over.**
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
