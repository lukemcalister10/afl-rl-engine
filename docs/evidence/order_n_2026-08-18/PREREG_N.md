# PREREG N — THE PROPERTY, THE OUTCOME SURFACE, AND THE DERIVED CHARGE

**Seat:** ORDER N. **Date:** 2026-08-18. **Base:** `land/order-29` at `4af260b` (ORDER M's tree).

**This seat is READ-ONLY on the engine, the board and the law. It builds no board. It adopts nothing.
It proposes a mechanism specification and an offline estimate, for the owner to rule on.**

This document is pushed **before any measurement number is produced**. Everything below is fixed in
advance: the windows, the constructions, the statistics, the derivation rule, and the falsifiers.

---

## 0 · WHAT THE ORDER ASKS, RESTATED

The owner's words are the brief:

> *"We shouldn't be using dean and duff tytler specifically and reverse engineering a rule to suit
> them. We should be looking at the effect - which is that young players who perform well are being
> punished, while those who are not performing well are not being punished as much, and addressing
> that. Focus on the spirit, not on hitting technical bars you've set for yourself. We want this to
> value correctly."*

**There are no named-player targets in this order.** No number in this seat's work is chosen to move
any player to any value. Named rows appear once, at the very end of the packet, as illustrations of
where the derived rule puts them. If a named row lands somewhere the owner does not like, that is a
finding about the rule, not a reason to change the rule.

**The defect, as a property.** The counterweight's charge on the pedigree leg
(`engine/rl_after/_merged_recover.py`, `o31_pi`) is

```
pi *= max(0, 1 - ETA * (g/GAMMA_D) * exp(1 - g/GAMMA_D))       GAMMA_D = 14
```

Career games `g` is its only input. Two nineteen-year-olds with the same games count are charged
identically whether one is far above what is normal for his age or far below it. The companion half
(KAPPA, `rho31`) is performance-conditional but ORDER M proved it can only tilt weight between legs —
it cannot mark a row down (PACKET_M §4: at eta = 0 all three sub-expectation rows RISE, and rise
further at the hardest permitted kappa). ORDER M also proved eta is load-bearing for the whole
board's year-1 anchoring, not only for the age bar: at S1 dose 0.00 the board still needs eta ≥ 0.31.

---

## 1 · WHAT WAS LOOKED AT BEFORE THIS DOCUMENT WAS WRITTEN

Full disclosure, so nobody has to wonder what was known when the design was fixed.

1. The engine source for `o31_pi`, `rho31`, `beta31`, `phi31`, `o31_D`, `o32_gate_bar`,
   `o32_age_credit`, and the O32/O36 knob block. Structure only; no board was run.
2. The schema of the committed ledger `docs/ledgers/ORDER_K_MOVERS.json` and of the emitted
   walk-forward matrices (`per_entrant_*.json`). Field names, row counts, one printed row.
3. The S1 C3 age-gap surface `docs/evidence/order32_s1_2026-08-17/CONSTRUCTIONS_S1.json` — printed in
   full, because it is the fixed input the surplus is measured against.
4. `docs/evidence/order32_s4_2026-08-17/s4_shootout.py` in full — the house delivered-value ruler,
   which this seat reuses rather than reinvents.
5. PACKET_M.md and PACKET_K.md in full.
6. **One arithmetic identity was checked before this prereg was written, and it is declared here
   rather than presented later as a discovery.** The engine price is exactly linear in ETA at fixed
   knobs, because ETA enters only as the factor `(1 - ETA*m_d(g))` multiplying `pi`. This was
   confirmed against PACKET_M's own published ladder A: Harry Dean's board points fall 3069 → 2936 →
   2803 → 2670 → 2536 → 2403 across eta 0.00 → 0.50, a constant step of 133 points, and
   `0.10 · pi_pre · pedigree · m_d(17)` reproduces that step. This identity is the whole basis of the
   Step 4 offline pricing and it had to be known to be sound before the design could be written.

Nothing else was computed. No relationship between performance and price, and no relationship
between performance and outcomes, has been looked at.

---

## 2 · FIXED CONSTRUCTIONS

### 2.1 The age-appropriate expectation (the bar)

The engine's own object, `o32_gate_bar`, read from the S1 C3 surface. For a season played at age `a`
by a row whose future position class is `pos`:

```
bar(pos, a) = bars_flat[pos]                                   if a >= 24
            = bars_flat[pos] - DELTA[class(pos)][clip(a,18,23)] if a <  24
class(pos)  = TALL  if pos in {KPD, KPF, RUCK} else SMALL
```

`bars_flat` and `DELTA` are taken byte-for-byte from `CONSTRUCTIONS_S1.json` (`bars_flat`, `C3meta`
→ `delta`). No refit. The C3 surface is class-pooled TALL/SMALL, which is S1's own published choice.

### 2.2 PERFORMANCE SURPLUS (the quantity the whole order turns on)

For a row `p` at a vantage year `Y`:

```
PS(p, Y) = SUM_s [ games_s * (avg_s - bar(bar_s, age_s)) ]  /  SUM_s [ games_s ]
```

over every season `s` with `year_s <= Y` and `games_s > 0`, where
`age_s = age_draft + (year_s - draft_year)`.

- Units: AFL Fantasy points per game.
- **Positive means the row is producing above what is normal for a player of his age in his
  position class. Negative means below.**
- Games-weighted, so a two-game season cannot outvote a twenty-game season.
- Undefined when `g = 0`. Gameless rows are excluded from every population in this order. This is
  not a convenience: `m_d(0) = 0` is a structural law of the engine, gameless rows carry no charge
  today, and no mechanism proposed here may change that.

### 2.3 The young window

**Step 1 (board rows).** Ledger rows with `age <= 22` as of 2026 and `1 <= g <= 60`.

Justification, stated before the numbers:
- The age bar has content only below 24 (`o32_gate_bar` is flat from 24 by the ruled cap law), so
  "performance against age expectation" is only defined below 24.
- Age ≤ 22 keeps the population clear of the flat boundary, where the C3 delta has decayed to 4.6
  (SMALL) / 6.4 (TALL) points and the surplus is nearly the mature reading. Age ≤ 23 is reported as
  a pre-declared sensitivity.
- `g <= 60`: at 60 games the eta charge at ETA = 0.50 is 8.5% and falling; above that the mechanism
  is not the thing setting the price. `g >= 1`: see 2.2.

**Step 2 (outcome cohorts).** ND and pool entrants with `draft year >= 2005` (the S4 ruler's
`ENTRY_FLOOR`), scored at vantages `N = 1..6` years after entry, with `age at vantage <= 22` and
`1 <= g <= 60`, and requiring at least one observable future season (`vantage year + 1 <= 2025`, the
S4 ruler's `LAST_REAL_SEASON` right-censor). Force-majeure keys `paddy-mccartin`, `thomas-boyd` are
excluded, as the house ruler excludes them.

### 2.4 The delivered-value ruler

Reused whole from `docs/evidence/order32_s4_2026-08-17/s4_shootout.py`. Not reinvented, not retuned.
Copied into this evidence directory and md5-asserted at run.

```
w_sqrt(g)      = min(1, sqrt(max(0,g)/10))
capt_prem(x)   = 1.00 * 1.85 * (softplus((x-109.5)/1.85) - softplus((105.0-109.5)/1.85)), floored 0
season_raw(x,grp) = 3.0 * log(1+exp(min((x + capt_prem(x) - BARS[grp])/3.0, 40))) * 21.0
SV[k][year]    = w_sqrt(games) * season_raw(avg, bar)
DV1(k,Y)       = SV[k][Y+1]
DVREST(k,Y)    = SUM_{t>Y} 1.14^{-(t-Y)} * SV[k][t]
BARS = {KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9}
```

`BARS` here are the ruler's MATURE bars and they are left exactly as the house ruler has them.
**The age bar is used to measure the INPUT (performance surplus); the mature bar is used to measure
the OUTPUT (delivered value).** That is deliberate and it is the honest direction: a young player's
future value is worth what it is worth in the league, not what is impressive for his age.

### 2.5 The boards read

| tag | what | md5 | source |
|---|---|---|---|
| `OKRULED` | the current candidate, ORDER K's ruled setting, eta 0.50 | `f3101883…` | committed ledger + emitted matrix |
| `O35FINAL` | the landing candidate | `1f176444…` | emitted matrix, ledger column `landing` |
| `M0ETA0` | ORDER K's knobs with ETA = 0 | `73bf9617…` | emitted matrix (ORDER M) |

---

## 3 · STEP 1 — THE PROPERTY TEST

**Question.** Holding career games roughly constant, does the board pay a young row more for
producing above his age expectation?

**Price response.** `R = board price / v0` — the board's own appreciation on the row against its
entry price, in the same currency as the ledger. Reported on `orderk` and on `landing`.

**Statistics, all pre-declared:**

1. OLS slope of `R` on `PS`, unconditional; and with games controlled by fixed effects on the bins
   `[1,4] [5,9] [10,15] [16,24] [25,39] [40,60]`.
2. Spearman rank correlation of `R` with `PS` overall and within each games bin.
3. Binned means: `R` by PS tercile within each games bin, with counts.
4. **The eta charge in isolation:** `charge(g) = ETA * m_d(g)` at ETA = 0.50, and the same three
   statistics against PS. The charge is a pure function of `g`, so the within-bin correlation is
   predicted to be ~0 by construction; the unconditional correlation is whatever the empirical
   `g ~ PS` relationship makes it, and that number is the interesting one.
5. The same for the **realised** eta charge in board points, `Δ = v(ETA=0) - v(ETA=0.50)`, taken from
   the two matrices — this reads the charge in money rather than in percent.

**What would confirm the owner's claim.** A within-games-bin relationship between price response and
performance surplus that is flat or negative, together with an eta charge that is flat in PS at
fixed games and *larger* for above-bar rows unconditionally.

**What would refute it.** A clearly positive within-bin slope of `R` on `PS` that survives the
pedigree control — the board already rewards over-performance and the complaint is about levels, not
about the property.

---

## 4 · STEP 2 — WHAT PERFORMANCE-VS-AGE ACTUALLY PREDICTS

**Question.** For young players at each level of career games, how much does performance surplus
predict subsequent delivered value, over and above pedigree?

**Estimands, per career-games bin, on the pooled young cohort:**

- **E1 — partial rank association.** Spearman correlation of `PS` with `DVREST`, and the *partial*
  Spearman controlling `v0` (rank-residual method). Bootstrap 90% CI, 2000 resamples, seed 32 (the
  S4 ruler's own B and seed).
- **E2 — the multiplicative slope.** OLS of `ln(1 + DVREST)` on `ln(v0)` and `PS`:
  `ln(1+DVREST) = a + c·ln(v0) + BETA·PS`. `BETA` is the estimand: the proportional change in
  subsequent delivered value per one point per game of surplus, at fixed pedigree. Bootstrap 90% CI.
- **E3 — pedigree's own decay.** The partial Spearman of `v0` with `DVREST` controlling `PS`, per
  games bin. This is the measurement requirement (c) needs: does the prior lose information as
  evidence accumulates, and how fast?
- **E4 — dispersion and sample size.** For every cell: n, the interquartile range of `PS`, the mean
  and median of `DVREST`, and the share of rows with `DVREST = 0`.

**Bins.** Career games `[1,3] [4,7] [8,12] [13,17] [18,24] [25,39] [40,60]`, reported at the order's
requested anchors 2, 5, 10, 15, 20, 30 games (the bin containing each anchor).

**Splits.** (i) position class TALL vs SMALL; (ii) pick band `1-10`, `11-20`, `21-40`, `41+ and
pool`. Reported with counts; a cell with n < 30 is reported as thin and never carries a derivation.

**Horizons.** `DVREST` is primary. `DV1` is reported alongside as a secondary read.

**Overlap disclosure.** A player contributes a row at more than one vantage. Rows are therefore not
independent. Every CI is bootstrapped by **clustering on player key**, not on row, so the dependence
is priced rather than ignored.

---

## 5 · STEP 3 — THE DERIVATION RULE, FIXED BEFORE THE NUMBERS

**Functional form, declared now:**

```
pi *= max(0, 1 - ETA_N * A(g) * P(s))

A(g) = 1 - exp(-g/G0)              MONOTONE in evidence, A(0) = 0 exactly, saturating at 1
P(s) = clip( exp(-THETA * (s - s0)), PMIN, PMAX )
s    = PS(p, Y)   (section 2.2)
```

**Where each constant comes from — and this is the discipline the order asks for:**

| constant | derived from | never from |
|---|---|---|
| `THETA` | Step 2's `BETA` — the measured proportional payoff to a point of surplus | any player's price |
| `G0` | Step 2's `E3` — the measured decay of pedigree's incremental predictive power | any player's price |
| `s0` | the games-weighted mean `PS` of the young population, so `P` has mean ≈ 1 | — |
| `PMIN`,`PMAX` | the 10th and 90th percentile of `exp(-THETA*(s-s0))` on the young population, so the tilt is bounded by the data's own spread rather than by a hand-picked clamp | — |
| `ETA_N` | solved by the **anchoring identity**: the aggregate pedigree-leg charge over the class-mark population is held equal to the current board's | — |

**The separation is the point.** The *shape* of the charge — how it varies with evidence and with
performance — is derived from outcomes. The *level* of the charge is not an outcome question at all;
it is a no-arbitrage calibration, and ORDER M proved it is load-bearing. So the level is set by
matching what eta already levies, and the tilt redistributes that level between over- and
under-performers without changing it.

**Pre-committed structural properties the derived charge must satisfy, or it is not proposed:**

- **N-S1.** `A(0) = 0` exactly, so `pi(0) = D` and every day-0 print is untouched. Non-negotiable.
- **N-S2.** `A` is non-decreasing in `g` on `[0, ∞)`. This is requirement (c).
- **N-S3.** `P` is non-increasing in `s`. A row further above his age bar is never charged more.
- **N-S4.** The whole factor stays in `(0, 1]` for every row on the board — no negative pedigree.
- **N-S5.** The charge is zero for rows with no age bar content (age ≥ 24 at vantage) **only if** the
  measurement supports it; otherwise `P` evaluates at `s` measured against the flat bar. Declared as
  an open construction choice, to be settled by Step 2 and stated explicitly in the packet.

**Pre-committed honesty clause.** If Step 2 finds `BETA` indistinguishable from zero at a games
level, `THETA` is set to zero at that games level and the packet says the owner's intuition is not
supported by the outcome data there. No signal will be manufactured. If the anchoring requirement and
the performance conditioning conflict — that is, if no `ETA_N` holds the board while giving the tilt
the measurement justifies — the conflict is quantified and both sides are presented. This seat will
not choose for the owner.

---

## 6 · STEP 4 — THE OFFLINE PRICING IDENTITY

**The identity, declared before use (see §1.6):**

At fixed knobs, for every row and every vantage `N`,

```
v(ETA)  =  v(0) - ETA * pi_pre(g) * pedigree * m_d(g)
```

so, from the two emitted matrices,

```
B_N  = ( v_M0ETA0[N] - v_OKRULED[N] ) / 0.50           the realised charge at ETA = 0.50
C_N  = B_N / m_d(g_N)                                   the charge BASE, pi_pre * pedigree
v_new[N] = v_M0ETA0[N] - C_N * charge_new(row, N)
```

`g_N` is `games_by[N]` from the matrix — the row's career games at that vantage.

**Verification, pre-registered as a hard gate.** The identity must reproduce ORDER K's own emitted
values from the eta = 0 matrix at ETA = 0.50 to within 1e-6 relative on **every** row and vantage. If
it does not, Step 4 is not reported and the packet says so.

**What is then estimated, and it is an ESTIMATE, not a build:**

1. The Step 1 property test re-run on the estimated prices — is the price response now monotone in
   performance surplus?
2. The year-1 class mark, on ORDER L's registered basis (W2 scorer, draft classes 2005-2015,
   `ENTRY_FLOOR = 2005`) and on `ok_class.py`'s cohort clock, by rewriting `vpath` in the matrix and
   running the committed `om_class.py` machinery unchanged.
3. The ND band tables, **both windows** — PRIMARY cohorts 2005-2023 and MODERN cohorts 2019-2023 —
   by the same route through the committed band machinery. This is the standing owner requirement and
   it is not optional.
4. Whether the board plausibly stays under the 14% buy rail, band by band.

**Every number in Step 4 is labelled an estimate pending a build.** The estimate is exact for the
pedigree-leg arithmetic and it is exact for the instruments, because both are recomputed by the
committed code on the modified matrix. It is an estimate because no board was built, no engine assert
wall was run, and the standing acceptance suite (continuity, rho32 monotonicity, day-0 identity, the
veteran caps) cannot be run without a build.

---

## 7 · FALSIFIERS

Fired means the finding it guards is withdrawn or restated, in the packet, in the same words.

| # | falsifier | what it kills |
|---|---|---|
| **N1** | The Step 4 identity does not reproduce `OKRULED` from `M0ETA0` at ETA = 0.50 to 1e-6 relative on every row and vantage. | All of Step 4. Nothing is priced offline. |
| **N2** | The S1 C3 surface as read here does not reproduce `o32_gate_bar` for a spot-check grid of (position, age) taken from the engine's own constants. | The performance-surplus construction. Step 1 and Step 2 both stop. |
| **N3** | The S4 ruler copy does not md5-match `docs/evidence/order32_s4_2026-08-17/s4_shootout.py`. | The delivered-value ruler. Step 2 stops. |
| **N4** | Step 1 finds a **positive** within-games-bin slope of price response on performance surplus, significant at the 90% level, on the current candidate. | The owner's claim that good young performers are punished. The packet reports the refutation as the headline. |
| **N5** | Step 2 finds `BETA` not distinguishable from zero at every games level in the young window. | The whole case for performance conditioning. The packet says the mechanism cannot be justified from outcomes and proposes nothing. |
| **N6** | Step 2 finds `BETA` **negative** — over-performing young players deliver *less* subsequently. | The direction of the tilt. The packet reports it and does not invert the mechanism to suit the owner. |
| **N7** | Step 2's `E3` finds pedigree's incremental predictive power **rising** with career games. | Requirement (c)'s justification. A monotone-decaying prior would then be the wrong shape and the packet says so. |
| **N8** | No `ETA_N` in `(0, 1]` reproduces the current aggregate charge under the derived `A` and `P`. | The anchoring half. The conflict is quantified and presented; nothing is proposed. |
| **N9** | The derived charge violates any of N-S1 … N-S4 on any row of the board. | The proposal. It is not put forward. |

---

## 8 · WHAT THIS SEAT WILL NOT DO

- It will not build a board.
- It will not edit the engine, the law, or any ledger.
- It will not adopt, rule, or recommend on its own word.
- It will not tune any constant to move any named player to any value.
- It will not report a Step 4 number without the words "estimate, pending a build" attached.

**Deliverable:** `PACKET_N.md` in this directory — the property diagnosis, the measured surface, the
derived mechanism, the offline estimate. Plain language, short sentences, worked examples.
