# PREREG Q — PRICING THREE REPAIRS TO THE ORDER P CHARGE

**Seat:** ORDER Q. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**Base board:** ORDER P `374d4e44`, total 666,434. **Comparators:** ORDER K `f3101883` 673,097 ·
live `88ce647f` 752,429 (never touched).

**This is a MEASUREMENT order. Nothing is adopted. Nothing lands. No pull request is opened.**
This seat delivers numbers. It does not recommend a variant.

**This file is pushed before the first engine edit.** Everything below is written down in advance.

---

## 1 · THE TWO DEFECTS BEING PRICED

ORDER P charges a young player's draft pedigree down by

    pi *= exp( -LAMBDA * A(g) * T(s_P) )        for rows aged under 24

with `A(g) = 1 - exp(-g/G0)`, `T(s) = clip(1 - THETA_R*(s - s0), 0, TMAX)`, and `s_P` measured
against the S1 age bar plus a measured pedigree premium `PG(ln v0, class)`.
Constants: `G0` 9.89, `LAMBDA` 0.1743833, `THETA_R` 0.6574385, `s0` -2.4527, `TMAX` 21.1233, and
`LAMBDA * THETA_R = BETA_sat = 0.1146463`.

**DEFECT 1 — THE PICK REVERSAL.** Hold a player's output and games fixed and raise only his entry
price. The pedigree leg is `v0 * exp(-LAMBDA*A*T(out - agebar - PG(ln v0)))`. Raising `v0` raises the
bar he is judged against, which raises his charge. The charge can rise faster than the price. The leg
falls with price whenever `dPG/dln(v0) > 1/(BETA_sat*A)`. At saturation that threshold is
`1/0.1146463 = 8.723`. The measured SMALL premium slope averages about 8.95 across its support.
So the reversal is expected to be board-wide, not exotic.

**DEFECT 2 — THE AGE-24 CLIFF.** `engine/rl_after/_merged_recover.py` about line 3933 reads
`if not _by or (int(Y)-int(_by))>=O37_AGE_GATE: return _old`. At 24 the ORDER P charge does not
switch off. It hands back to ORDER K's games-only charge. So a player's price on his 24th birthday
becomes his ORDER K price, with his games and his output unchanged. The owner's words:
"players shouldn't have drastic price changes for no reason other than getting older."

---

## 2 · STEP 0 — VALIDATE THE SUPERVISOR'S ARITHMETIC FIRST

The supervisor's census of both defects rests on an inference, not on engine internals. For each
young row he took the ORDER K and ORDER P prices and the two charge factors `fK` and `fP`, and
inferred the charged pedigree leg as

    ped_P = (P_K - P_P) * fP / (fK - fP)

treating the production leg and `pi_base` as independent of `v0`.

**This seat will verify that against the engine's own internals before using any of it.** The
engine will be instrumented, behind a read-only measurement dial, to emit per row:

- the production leg `rho31(g)*e`
- the age credit `o32_age_credit(p,Y,g)`
- `pi_base` (the uncharged `pi`)
- `pv_pedigree(p)`
- the charge factor actually applied
- the charged pedigree leg
- the final unrounded price

**Two things get checked, and they are different questions.**

**Check 0A — the identity.** Is `ped_P = (P_K - P_P) * fP / (fK - fP)` equal to the engine's own
charged pedigree leg? This should be exact algebra if and only if the production leg and `pi_base`
are byte-identical between the ORDER K board and the ORDER P board for that row. It is checked, not
assumed.

**Check 0B — the sweep.** The census sweeps entry price downward and asks whether any lower price
prices higher. The supervisor did that sweep on his inferred legs. This seat will do the sweep
**inside the engine**, re-pricing each row at a perturbed `v0`, and compare the verdicts row by row.

**One known channel that could break the sweep assumption is named here in advance.** In `ev()` the
staleness and decay gates read `v0_start(p)` and can cap the production leg at `v0*frac`. That is a
different object from `day0_v0(p)`, but it is still a function of the row's entry value. If that cap
binds on any young row, the production leg is not independent of entry price for that row and the
supervisor's sweep is wrong there. This seat will count the young rows on which it binds and report
the count, whether it is zero or not.

**If the inference is wrong, this seat says so plainly and reports the corrected census.** That
outcome is a valid result, not a failure.

### The supervisor's census, written here to be reproduced or refuted

Young ND+pool rows, age under 24, games above 0, `|fK - fP| >= 0.02`. Sweep every lower entry price
at 2% steps and ask whether any prices higher.

| band | burned | of | points |
|---|---:|---:|---:|
| picks 1-10 | 24 | 43 | 1,815 |
| picks 11-20 | 13 | 44 | — |
| picks 21-30 | 12 | 35 | — |
| picks 31-40 | 4 | 28 | — |
| picks 41+ | 13 | 52 | — |
| pool | 10 | 65 | — |
| **TOTAL** | **76** | **267** | **2,323** |

Worst four named: Sam Lalor pick 1, 3,061 -> 3,395 (+334) · Willem Duursma pick 1, 3,920 -> 4,225 ·
Finn O'Sullivan pick 2, 2,810 -> 3,055 · Harley Reid pick 1, 3,724 -> 3,805.

Birthday census: 12 of 81 age-23 rows gain 50% or more from the birthday alone; Josh Sinn 73 -> 357
(4.89x), James Tunstill 42 -> 176, Campbell Chesser 167 -> 333; 2,271 points handed back across all
age-23 rows.

**These are the supervisor's numbers and they are not this seat's acceptance criteria.**

---

## 3 · THE THREE VARIANTS

Each variant sits behind its own new dial. The dials are independent so the two combinations are
just two dials on at once.

| dial | variant |
|---|---|
| `RL_O38A` | FIX A — monotonise the pedigree leg in entry price |
| `RL_O38B1` | FIX B1 — delete the age gate |
| `RL_O38B2` | FIX B2 — ramp the charge out across ages 23 to 26 |

`RL_O38B1` and `RL_O38B2` are mutually exclusive. Setting both halts at load.

### 3.1 FIX A — monotonise the pedigree leg in entry price

**The law being enforced:** a higher pick may never be worth less than a lower pick on identical
output and games.

**The construction, which introduces NO free parameter.** Write `x = ln(v0)` and

    phi(x) = x - LAMBDA * A(g) * T( OUT - PG_w(x) )

where `OUT` is the row's games-weighted production above its AGE bar and `PG_w(x)` is its
games-weighted pedigree premium at price `exp(x)`. The charged pedigree leg is proportional to
`exp(phi(x))`. The fix replaces `phi` by its running maximum from the left:

    phi_A(x) = max over u <= x of phi(u)

and the applied factor becomes `exp(phi_A(x) - x)` times the uncharged leg. This is the same
isotonic idea the ISO multiplier already uses in this engine (`IsotonicRegression`, the Newcombe
trough), applied here in entry price.

**Three properties, asserted at load rather than argued.**
1. `phi_A >= phi` always, so the charge is only ever CAPPED, never raised. Prices under FIX A can
   only move UP against ORDER P, never down.
2. `exp(phi_A(x))` is non-decreasing in `x` by construction, so no lower entry price can price
   higher. The burn census must go to zero.
3. Where `phi` is already at its own running maximum the factor is unchanged, so rows that were
   never burned are byte-identical to ORDER P.

**It is computed exactly, not on a grid.** `PG` is piecewise linear on its published nodes and `T` is
piecewise linear in `s` with two clip breakpoints, so `phi` is piecewise linear in `x`. The maximum
of a piecewise linear function is at a breakpoint, so the running maximum is exact if every
breakpoint is enumerated: the premium grid nodes of both classes, the two clip crossings inside each
segment, the flat-support boundaries, and `x` itself.

### 3.2 FIX B1 — delete the age gate

The `>= O37_AGE_GATE` early return is removed. The charge runs at every age using the same bar. From
age 24 the S1 age bar already equals the flat bar by construction, so the bar for a mature row is the
flat bar plus the measured premium. There is no phase-out and no new parameter.

**The known cost, stated before the measurement:** mature rows are NO LONGER byte-identical to
ORDER K. This seat will measure and report that movement in full, by age and by band. It is the
price of this option and it will not be buried.

### 3.3 FIX B2 — ramp the charge out across ages 23 to 26

The fallback. The applied factor becomes a geometric blend, in the exponent, between the ORDER P
charge and the ORDER K charge:

    ln f = w(age) * ln f_P + (1 - w(age)) * ln f_K
    w(23) = 1, w(24) = 2/3, w(25) = 1/3, w(26) = 0, w = 1 below 23, w = 0 above 26

**The endpoint 26 is a FREE PARAMETER. It was invented by this seat. It was not measured.** It is
reported as such everywhere and never described as derived.

**A prediction that contradicts the order, written down now.** The order expects zero mature-row
movement under B2. This seat expects NON-ZERO movement at ages 24 and 25, because the ramp puts a
partial ORDER P charge on exactly those ages. Rows aged 26 and over should be byte-identical to
ORDER K. If ages 24-25 move, that is the ramp working, not a fault, and the order's expectation was
simply wrong. It will be reported loudly either way.

**A second disclosure.** Age in this engine is the integer `int(Y) - int(birth year)`. There is no
finer resolution. So B2 does not remove the step; it replaces one step of full size with three steps
of a third the size. That is what a ramp can be on an integer axis and it is stated rather than
implied.

---

## 4 · WHAT WILL BE REPORTED FOR EVERY VARIANT

- the burn census re-run, by band
- the birthday census re-run, by band
- the full no-arb tables in the STANDING format: year paths yr0-7, appreciation, margin, verdict,
  for bands 1-10 / 11-20 / 21-30 / 31-40 / 41+ plus ALL / 1-20 / 21-64, in BOTH windows (full
  history and modern 2019-2023), plus the pool arms both windows, both baselines per row
- class marks on the W2 basis (DRAFT classes 2005-2015, ENTRY_FLOOR 2005) and the PER-CLASS table,
  including whether draft 2010 (1.1570), 2011 (1.1595) and 2015 (1.2047) move
- board total, the named rows, the movers ledger
- mature-row movement
- continuity on every axis, INCLUDING the age axis across 23/24

---

## 5 · FALSIFIERS. TEN OF THEM HALT.

| # | falsifier | halt? |
|---|---|---|
| **Q1** | with all three new dials unset the board is not `374d4e44` BYTE-EXACT | HALT |
| **Q2** | determinism x2 fails on any variant board | HALT |
| **Q3** | a variant dial does not carry the O37/O36/O35/O32/O31 stack on its own defaults | HALT |
| **Q4** | the base stack with everything off no longer rebuilds `1f176444` | HALT |
| **Q5** | ORDER K's ruled line with every new dial unset no longer rebuilds `f3101883` | HALT |
| **Q6** | **under FIX A the burn census is not ZERO** | HALT |
| **Q7** | under FIX A any row prices BELOW its ORDER P price | HALT (A can only cap the charge) |
| **Q8** | any variant prices a row ABOVE its own uncharged (eta-zero) price | HALT |
| **Q9** | any variant moves a day-0 print, or any of the 89 gameless rows | HALT (`A(0)=0` still) |
| **Q10** | under B2 a row aged 26 or over is not byte-identical to ORDER K | HALT |
| Q11 | the W2 class mark falls below 1.03 or reaches 1.14 on any variant | report, do not halt |
| Q12 | a pick band or pool arm goes above +14% beyond the two already disclosed | report |
| Q13 | the age axis shows a step at 23/24 under B1 or B2 larger than the ORDER P step | report |
| Q14 | the ORDER P continuity suite did NOT test the charge across ages 23/24 | report; this is a claim about ORDER P, confirmed or refuted |
| Q15 | Step 0 shows the supervisor's inference is wrong | report as the headline, do not halt |

---

## 6 · PREDICTIONS, WRITTEN BEFORE THE FIRST BUILD

These are predictions. Being wrong about them is a finding, not a failure.

1. Step 0 check 0A will agree essentially exactly, because the algebra is exact whenever the
   production leg is common to both boards. The interesting risk is in check 0B, the sweep.
2. FIX A raises the board total against ORDER P, because it can only cap the charge.
3. FIX A's effect is concentrated in picks 1-10, because the premium slope is steepest at the
   dear end and `A(g)` is largest for rows with games.
4. FIX B1 moves mature rows a LOT, and downward, because at high games `A(g)` is near 1 while
   ORDER K's blind charge has already decayed to nearly nothing past 14 games. This is the largest
   single number in the order.
5. FIX B1 makes the board total FALL substantially against ORDER P.
6. FIX B2 moves rows aged 24 and 25 and no others.
7. The two combinations are not additive. FIX A caps the charge and B1 extends where the charge
   applies, so A on top of B1 should give back more points than A on top of ORDER P.
8. The W2 class mark is measured over draft classes 2005-2015, whose rows are now mature, so B1
   and B2 should move it and A should move it only a little.

**Materiality is fixed here, before any result: 0.5 percentage points on a band, 0.002 on a class
mark, 0.3% on the board total.**

---

## 7 · CONVENTIONS THIS SEAT IS HELD TO

- **NO named-player targets.** No player's value is an acceptance criterion. Named rows are reported
  as consequences only. This is a standing prohibition in this project after a real error.
- **Nulls reported as nulls.** Never scored zero, never dropped.
- **Halt and report on any law breach.** Never trade one law for another silently.
- **Built against expected, reported loudly.**
- **Plain speech.** Short sentences. One idea each. No metaphors for mechanics. What is MEASURED is
  marked apart from what is asserted and not checked.
- The working directory `/home/user/afl-rl-engine` is shared and its checked-out branch is not
  changed by this seat. All work is in a separate `git worktree`.
- Engine runs are STRICTLY SEQUENTIAL. Board and store pins are threaded and printed on every run.
