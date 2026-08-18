# PACKET M — ETA WAS SET TO ZERO. THE BOARD DOES NOT SURVIVE IT.

**Seat:** ORDER M, the test seat. **Date:** 2026-08-18.
**Prereg:** `PREREG_M.md`, pushed at commit `b2e445f`, before the first engine run of this order.
**Base:** ORDER K's tree. **Boards built here:** listed in §9.

**Nothing here is adopted. Nothing lands on this seat's word. This order proposes no candidate.**

---

## 1 · THE ANSWER, IN SIX SENTENCES

You ruled that eta must be zero. I set it to zero and built the board.

**It gives you exactly what you asked for on the two rows you named.** Harry Dean goes from 2,403 to
**3,069**. Cooper Duff-Tytler goes from 1,505 to **2,057**. Both clear your stated references.

**It also breaks four of your six laws, and it breaks them by a lot.** The year-1 class mark goes to
**1.2046** against a buy rail of 1.14. Picks 1-10 read **+31.58%** against a rail of +14%. All three
sub-expectation rows rise. The veteran pool moves +2,781 points against a 668-point line.

**And there is no dose that fixes it.** I swept all 7,560 settings the declared grid allows with eta
pinned at zero. **Not one of them is legal.** Not at dose 0.40. Not at dose 0.10. Not at dose 0.00,
which is the age bar switched off entirely.

**This is outcome (b) from the prereg.** The blind half is load-bearing. The age bar cannot ship in
its current form with eta at zero.

---

## 2 · WHY. THE ONE THING THAT MATTERS.

I had this wrong in the prereg, and so did the diagnosis in the order. Both of us thought eta was
paying for the age bar. It is not.

**Eta is the brake on the whole board's first-year appreciation.**

Here is the proof, and it is one number. Set the S1 dose to **0.00**. That is the age bar switched
off completely — no age-referenced projection bar anywhere on the board. Now walk eta down from 0.50.

| eta at dose 0.00 | class mark | worst single class | picks 1-10 | verdict |
|---:|---:|---:|---:|---|
| 0.50 | 0.9912 | 1.0731 | +0.40% | legal |
| 0.41 | 1.0188 | 1.1008 | +4.60% | legal |
| 0.35 | 1.0372 | 1.1192 | +7.41% | legal |
| 0.31 | 1.0494 | 1.1315 | +9.27% | **legal — the last legal step** |
| 0.30 | 1.0525 | 1.1346 | +9.74% | **the +14% band rail breaks** |
| 0.20 | 1.0832 | 1.1665 | +14.42% | broken |
| 0.10 | 1.1138 | 1.2006 | +19.09% | broken |
| **0.00** | **1.1445** | **1.2346** | **+23.76%** | **broken** |

**Read the bottom row.** With no age bar at all, and eta at zero, picks 1-10 appreciate 23.76% in
their first year. Your rail is 14%. A team could buy a top-ten pick on draft day, carry it for a
season at 14%, sell it, and keep nearly ten points of free money.

That has nothing to do with the age bar. That is eta's own job, and eta was doing it.

Source: `TRADEOFF_M_out.txt`, Q3, second walk.

---

## 3 · THE SEARCH, AND WHAT IT RETURNED

I reused ORDER J's sweep machinery whole (`o37_sweep.py`) with eta pinned to `[0.0]`. Gamma_d is
inert once eta is zero — it multiplies a term that is itself multiplied by eta — so it was held at 14
and reported as inert, never swept. That leaves four free axes, exactly as the prereg declared them.

| axis | values swept |
|---|---|
| S1 dose | 0.00 to 1.00, 15 values |
| kappa | 0.15 to 0.60, 14 values |
| gamma_u | 8 to 16, 6 values |
| lambda_rel | 0.80 to 1.30, 6 values |

**7,560 settings. Every one scored on every constraint, not short-circuited on the first failure,
because the order asks what breaks first and at what dose.**

### The result

| set | count |
|---|---:|
| settings legal on **your laws** (G1 floor and rail, G2 improve, G3 +14%, G4) | **0 of 7,560** |
| settings legal on the **inherited ruled constraints** (1.139 no-arb, W band, slope band, rho32 monotone, at-bar continuity) | **0 of 7,560** |

### What breaks, and how many settings it breaks

| rail | settings that break it | whose rail |
|---|---:|---|
| G3 — no ND band above +14% | **7,560 of 7,560** | yours |
| the 1.139 no-arb line on a single class | **7,560 of 7,560** | yours (see the floor probe below — this one *can* be met outside the grid, G3 cannot) |
| G1's 1.14 buy rail | 7,410 of 7,560 | yours |
| the W band | 3,654 | inherited calibration |
| at-bar continuity | 3,276 | ruled |
| rho32 monotonicity | 990 | ruled |
| slope band | 12 | inherited calibration |
| G2 — picks 41-64 improve vs ORDER K | 24 | yours |

**Two of your own laws are broken by every single setting in the grid.** This does not come down to a
calibration diagnostic. I want that clear, because a finding that rested on the W band or the slope
band would be a weaker finding, and this one does not.

### The floor of the grid

The coolest setting reachable inside the declared grid with eta at zero is dose 0.00, kappa 0.15,
gamma_u 16 (lambda_rel makes no difference at all — it moves the worst class by less than 0.0001).

| quantity | the coolest eta=0 setting in the grid | your rail | over by |
|---|---:|---:|---:|
| worst single class | 1.2067 | 1.139 | **0.0677** |
| picks 1-10 | +22.40% | +14% | **8.4 points** |
| class mark | 1.1162 | under 1.14 | inside, just |

### And I went outside the grid too, on purpose, so nobody has to wonder

A reasonable objection: the grid stops kappa at 0.15 and lambda_rel at 0.80. Is a legal board hiding
just past the edge? I checked, going outside the declared grid in the direction that makes the board
coolest. **kappa = 0 is the counterweight switched off entirely.** It is not a setting anyone has ruled
and it is not proposed. It is a bound.

| setting | class | worst class | picks 1-10 |
|---|---:|---:|---:|
| dose 0, **kappa 0** (no counterweight at all), eta 0 | 1.0501 | **1.1285 — inside 1.139** | **+18.30%** |
| dose 0, kappa 0.05, eta 0 | 1.0721 | 1.1546 | +19.93% |
| dose 0, kappa 0.10, eta 0 | 1.0942 | 1.1806 | +21.55% |
| dose 0, kappa 0.15, eta 0 | 1.1162 | 1.2067 | +23.18% |

**At the very bottom of everything the two rails part company, and I am not going to round that away.**
With no counterweight and no age bar, the 1.139 no-arb class line *is* satisfied, at 1.1285. **The +14%
band rail is not.** Picks 1-10 read +18.30%, over by 4.30 points, with every lever in the stack set to
its coolest value and two of them switched off entirely.

**So the law that binds, at the floor of everything, is G3 — your own band rail.**

Why no edge can save it, one line each:

- **lambda_rel** moves the worst class by under 0.0001 across its whole range. It is not a lever here.
- **kappa** — lower is cooler, and it is already at zero above.
- **gamma_u** spans under 0.01 on the worst class across 8 to 16.
- **dose** makes it worse monotonically at every step. Dose 0 is already the coolest.

There is no direction left to travel.

Source: `SWEEP_M_out.txt`, `SWEEP_M.json`, `FLOORPROBE_M_out.txt`.

---

## 4 · WHAT THE BUILT BOARD ACTUALLY READS

The sweep navigates. It decides nothing. Everything below comes off a **built board** and the
**standing instrument**.

**The board:** `73bf961724e77f0bda996825125a07ad`. ORDER K's ruled knobs — dose 0.40, kappa 0.20,
gamma_u 8, gamma_d 14, lambda_rel 1.08 — with **eta set to 0**. Nothing else changed. No engine line
was edited in this order.

### G5 — the point of the order. **DELIVERED, AND THEN SOME.**

| row | age | pick | games | candidate 31 | landing | ORDER K | **ETA = 0** | your reference |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **harry-dean** | 19 | 3 | 17 | 2,670 | 2,400 | 2,403 | **3,069** | ~2,600 — **cleared by 469** |
| **cooper-duff-tytler** | 19 | 4 | 13 | 1,832 | 1,572 | 1,505 | **2,057** | ~1,800 — **cleared by 257** |

Harry Dean gains **+666** against ORDER K. Cooper Duff-Tytler gains **+552**. Both now sit above
candidate 31 as well.

**The diagnosis in the order was right about these two rows.** Eta was charging them hardest because
they are 19, high picks, key-position talls, with few games — and the bump peaks at 14 games. Dean has
17. Duff-Tytler has 13. Take the bump away and they get their pedigree leg back in full.

Isaac Kako, at 36 games, was already most of the way down the far side of the bump. He gains +88,
where Dean gains +666. That is the shape of the thing, measured.

### G6 — the sub-expectation rows. **BREACHED, ALL THREE, AND KAPPA CANNOT CHARGE THEM.**

I said in the prereg that this would happen and why. It happened.

| row | age | pick | games | landing | ORDER K | **ETA = 0** | move vs landing |
|---|---:|---:|---:|---:|---:|---:|---:|
| xavier-taylor | 19 | 11 | 2 | 1,176 | 1,162 | **1,345** | **+169** |
| daniel-annable | 19 | 6 | 2 | 1,530 | 1,537 | **1,761** | **+231** |
| dylan-patterson | 19 | 5 | 5 | 1,467 | 1,440 | **1,824** | **+357** |

**Say it plainly: kappa alone cannot charge these rows.**

Here is the proof, not the argument.

**First**, take the age bar off entirely — dose 0.00 — and they still rise: Xavier Taylor +131, Daniel
Annable +141, Dylan Patterson +257. So this is not the age bar's doing.

**Second**, turn kappa up as far as the ruled constraints allow. rho32 monotonicity is what caps kappa,
and the highest monotone value on the grid is 0.60 at gamma_u 16 — four times ORDER K's 0.20. I built
that board rather than argue it. The result is in `LADDER_M_out.txt` under tag `KMAX`.

The reason is structural, and it is worth one sentence. **Kappa moves weight between two legs. Eta
charged one leg down.** Those are different operations. Kappa can tilt the balance between pedigree
and shown production; it cannot remove value from the row. Only eta could subtract.

**And this is worse than undoing what ORDER K added.** The landing candidate `1f176444` already
carries eta at 0.41. Setting eta to zero removes a charge the base board was already levying. That is
why these rows rise against the **landing candidate**, not just against ORDER K.

### G1 — the year-1 class, on the registered basis. **BREACHED at the buy rail.**

Reported on the basis your 1.03 floor and your ~1.08 prior were registered against: the W2 scorer,
draft classes 2005-2015, `ENTRY_FLOOR = 2005`. ORDER L settled this and the window confusion is not
reopened here.

| board | registered basis (W2, draft 05-15) | vs the 1.03 floor | vs the 1.14 buy rail | cohort window (ok_class 05-15) |
|---|---:|---:|---:|---:|
| **ETA = 0** | **1.2046** | +0.1746 | **+0.0646 — OVER** | 1.1829 |
| eta = 0, coolest setting | 1.1158 | +0.0858 | −0.0242 | 1.0975 |
| dose 0, eta 0.31 | 1.0491 | +0.0191 | −0.0909 | 1.0316 |
| ORDER K | 1.0513 | +0.0213 | −0.0887 | 1.0324 |
| landing candidate | 1.0421 | +0.0121 | −0.0979 | 1.0232 |
| candidate 31 | 1.0525 | +0.0225 | −0.0875 | 1.0360 |

The floor is cleared easily. **The buy rail is not.** 1.2046 means the average draft class was worth
20% more one year after draft day than on it. Your own no-arb reading says anything above 14% is a
free trade for the buyer.

**Self-check:** this seat's rerun reproduces ORDER K's own class mark to 1.032405 vs 1.032405, and
reproduces ORDER L's 1.0669 exclusion sensitivity. The instrument did not move under me.

### G2 — the late bands. **THE ONE LAW ETA = 0 SATISFIES, and it satisfies it well.**

| band | landing | ORDER K | **ETA = 0** | move vs ORDER K |
|---|---:|---:|---:|---:|
| picks 31-40 | −12.84% | −10.70% | **−1.57%** | **+9.13 points** |
| picks 41-64 | −7.88% | −6.89% | **+1.71%** | **+8.60 points** |

Picks 41-64 turn **positive** for the first time on any board this project has built. Picks 31-40 come
within 1.6 points of neutral. This is real and it should be on the record. It is also the only law of
the six that eta = 0 improves, and it is bought by pushing every other band far through the buy rail.

### G4 — picks 1-10. Not cut. Blown through.

You rejected an earlier setting because it cut picks 1-10 below ORDER K's +8.22%. Eta = 0 does not cut
them. It takes them to **+31.58%** in the primary window and **+37.46%** in the modern one. That is not
a pass on G4. It is a G3 breach on the same band.

---

## 5 · THE BAND TABLES, BOTH WINDOWS, EVERY BAND

Standing since ORDER L: every band table in both windows. Below 0% is a sell-side red. Above +14% is a
buy-side red.

### PRIMARY window — cohorts 2005-2023 (draft years 2004-2022)

| band | n | **ETA = 0** | eta=0 coolest | dose 0 eta .31 | ORDER K | landing | cand 31 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 1200 | **+21.72% BUY-RED** | +13.52% | +4.66% | +4.23% | +2.98% | +6.62% |
| picks 1-20 | 380 | **+30.90% BUY-RED** | — | — | +9.22% | — | — |
| picks 21-64 | 820 | +7.21% ok | — | — | −3.67% | — | — |
| picks 1-10 | 190 | **+31.58% BUY-RED** | +23.85% | +9.84% | +8.22% | +7.93% | +16.19% |
| picks 11-20 | 190 | **+29.58% BUY-RED** | +20.54% | +11.34% | +11.16% | +9.20% | +12.04% |
| picks 21-30 | 190 | **+19.81% BUY-RED** | +10.79% | +4.81% | +5.26% | +2.76% | +3.68% |
| picks 31-40 | 190 | −1.57% SELL-RED | −7.52% | −10.61% | −10.70% | −12.84% | −12.38% |
| picks 41-64 | 440 | **+1.71% ok** | −7.66% | −8.39% | −6.89% | −7.88% | −11.36% |

### MODERN window — cohorts 2019-2023 (draft years 2018-2022)

| band | n | **ETA = 0** | eta=0 coolest | dose 0 eta .31 | ORDER K | landing | cand 31 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ALL picks 1-64 | 311 | **+15.72% BUY-RED** | +8.57% | −0.03% | −0.96% | −1.69% | +3.00% |
| picks 1-20 | 100 | **+31.27% BUY-RED** | — | — | +9.58% | — | — |
| picks 21-64 | 211 | −9.39% SELL-RED | — | — | −17.97% | — | — |
| picks 1-10 | 50 | **+37.46% BUY-RED** | +29.13% | **+15.11%** | +13.65% | +13.24% | +22.25% |
| picks 11-20 | 50 | **+19.94% BUY-RED** | +12.36% | +3.29% | +2.11% | +1.00% | +4.89% |
| picks 21-30 | 50 | −4.40% SELL-RED | −10.34% | −13.63% | −14.26% | −16.34% | −14.76% |
| picks 31-40 | 50 | −5.46% SELL-RED | −11.01% | −14.68% | −14.27% | −15.92% | −16.55% |
| picks 41-64 | 111 | −18.00% SELL-RED | −23.46% | −24.64% | −25.06% | −23.94% | −23.12% |

**Does eta = 0 improve or worsen the modern window?** Both, and they must not be blurred.

- **It improves the sell-side.** ALL 1-64 goes from ORDER K's **−0.96% SELL-RED to +15.72%**, so the
  sell-red verdict is cured. Picks 21-30 goes from **−14.26% to −4.40%**. Picks 41-64 goes from
  −25.06% to −18.00%.
- **It worsens the buy-side much more.** ALL 1-64 is now a **BUY-RED** at +15.72%. Picks 1-10 goes from
  +13.65% — just inside the rail — to **+37.46%**, which is two and a half times the rail. Picks 11-20
  goes from +2.11% to +19.94%.

**Four modern bands become buy-side reds** — ALL 1-64, picks 1-20, picks 1-10 and picks 11-20. Three of
those four were verdict-clean on ORDER K (1-20 +9.58%, 1-10 +13.65%, 11-20 +2.11%). Trading one red for
a bigger red of the opposite sign is not an improvement, and I am not going to present it as one.

**One thing to note for later, unrelated to eta = 0.** The modern window is *tighter* than the primary
one on picks 1-10. The dose-0 / eta-0.31 setting reads a comfortable +9.84% in the primary window and
**+15.11%** in the modern one — outside your rail. ORDER K's own +13.65% modern reading sits only 0.35
points inside it. Anything that lifts the top of the draft has less headroom than the primary table
suggests.

---

## 6 · THE POOL ARMS, BOTH WINDOWS

| arm | **ETA = 0** | eta=0 coolest | dose 0 eta .31 | ORDER K | landing | cand 31 |
|---|---:|---:|---:|---:|---:|---:|
| **PRIMARY** | | | | | | |
| RD | +3.65% | −5.30% | −4.62% | −3.39% | −2.21% | −6.99% |
| MSD | n/a | n/a | n/a | n/a | n/a | n/a |
| UNR | −40.50% | −41.07% | −42.19% | −42.91% | −42.06% | −36.58% |
| **IRE** | **+16.98% BUY-RED** | −0.16% | +8.80% | +13.34% | +13.51% | −5.29% |
| PDA | −17.20% | −25.16% | −22.35% | −20.70% | −18.33% | −22.77% |
| PDN | −39.35% | −43.33% | −40.71% | −40.32% | −37.81% | −37.16% |
| **SSP** | **+64.96%** | +50.62% | +46.71% | +52.71% | +50.52% | +38.17% |
| PDS | −26.15% | −31.31% | −30.44% | −27.70% | −25.47% | −28.84% |
| ALLPOOL | +1.74% | −7.09% | −6.26% | −4.93% | −3.91% | −8.53% |
| **MODERN** | | | | | | |
| RD | −15.06% | −20.55% | −20.76% | −20.41% | −18.65% | −18.53% |
| UNR | −33.15% | −34.69% | −35.01% | −35.13% | −32.81% | −32.57% |
| IRE | −54.98% | −54.98% | −54.98% | −54.98% | −49.34% | −44.53% |
| PDA | −44.07% | −45.95% | −45.39% | −45.58% | −41.15% | −38.06% |
| PDN | −35.80% | −41.26% | −37.25% | −36.53% | −34.93% | −36.18% |
| **SSP** | **+64.96%** | +50.62% | +46.71% | +52.71% | +50.52% | +38.17% |
| ALLPOOL | −4.66% | −11.64% | −11.88% | −10.47% | −9.15% | −11.61% |

**SSP, reported separately, never masked.** SSP's buy-side red is **inherited**. It is +50.52% on the
landing candidate and +38.17% on candidate 31, before this order or ORDER K touched anything. ORDER K
took it to +52.71%. **Eta = 0 takes it to +64.96%, worse by 12.25 points.** It is not caused here and
it is not cured here, and it does not go in the same sentence as the breaches this order creates.

**IRE is a new breach.** It goes from +13.34% on ORDER K — inside the rail — to **+16.98%** on the
eta = 0 board. That is this order's setting doing it, not an inheritance.

---

## 7 · THE TRADE-OFF, PRICED, SO YOU CAN CHOOSE KNOWINGLY

The prereg promised that if outcome (b) obtained I would show the curve rather than assert it. Two
ladders, both built as real boards.

### LADDER A — eta walked at your ruled dose 0.40, every other knob held

<!--LADDER_A-->

### LADDER B — the legal frontier: at each dose, the smallest eta the board can carry

<!--LADDER_B-->

### How much eta the board needs, dose by dose

Kappa, gamma_u, gamma_d and lambda_rel held at your ruled values, so eta is the only thing moving.

| S1 dose | smallest eta that keeps every band inside +14% | smallest eta that keeps every class inside 1.139 | class mark there | picks 1-10 there |
|---:|---:|---:|---:|---:|
| **0.00** | **0.31** | 0.29 | 1.0494 | +9.27% |
| 0.10 | 0.35 | 0.34 | 1.0496 | +8.90% |
| 0.15 | 0.37 | 0.36 | 1.0503 | +8.77% |
| 0.20 | 0.39 | 0.39 | 1.0513 | +8.68% |
| 0.25 | 0.42 | 0.41 | 1.0507 | +8.37% |
| 0.30 | 0.44 | 0.44 | 1.0526 | +8.37% |
| **0.40** | **0.50** | 0.50 | 1.0519 | +7.58% |
| 0.45 | 0.53 | 0.54 | 1.0490 | +6.78% |
| 0.50 | 0.56 | 0.57 | 1.0497 | +6.49% |
| 0.55 | 0.59 | 0.61 | 1.0477 | +5.78% |
| 0.60 | 0.63 | 0.64 | 1.0493 | +5.58% |
| 0.70 | 0.70 | 0.72 | 1.0497 | +4.70% |
| 0.85 | **none exists** | none exists | — | — |
| 1.00 | **none exists** | none exists | — | — |

Two things fall out of this table.

**One. The setting you ruled sits exactly on the frontier.** At dose 0.40 the smallest legal eta is
**0.50**. You ruled 0.50. That was not a coincidence — ORDER I's calibration was solving this same
constraint — but it does mean there is no slack at your dose. Any reduction in eta at dose 0.40 is
immediately illegal.

**Two. Above dose 0.70 no eta works at all.** Even eta at 0.75 cannot hold the board inside the rails
once the age bar is dosed that hard. That is a separate limit on the age bar and it is not what this
order was about, but it is on the record now.

### What the blind charge actually costs, by games played

The charge is `1 − eta·(g/14)·exp(1−g/14)`. Games played is the only input.

| career games | eta 0.10 | eta 0.20 | eta 0.31 | eta 0.41 | eta 0.50 |
|---:|---:|---:|---:|---:|---:|
| 2 | −3.4% | −6.7% | −10.4% | −13.8% | −16.8% |
| 5 | −6.8% | −13.6% | −21.1% | −27.8% | −34.0% |
| 8 | −8.8% | −17.5% | −27.2% | −36.0% | −43.9% |
| 10 | −9.5% | −19.0% | −29.5% | −39.0% | −47.5% |
| **14 (the peak)** | −10.0% | −20.0% | **−31.0%** | −41.0% | −50.0% |
| 20 | −9.3% | −18.6% | −28.8% | −38.2% | −46.5% |
| 30 | −6.8% | −13.7% | −21.2% | −28.0% | −34.2% |
| 36 | −5.3% | −10.7% | −16.6% | −21.9% | −26.7% |
| 50 | −2.7% | −5.5% | −8.5% | −11.2% | −13.6% |
| 80 | −0.5% | −1.0% | −1.6% | −2.1% | −2.6% |
| 141 | −0.0% | −0.0% | −0.0% | −0.0% | −0.1% |

This is the defect you named, in one table. Harry Dean at 17 games and Daniel Annable at 2 games are
charged by the same rule, and neither charge reads a single point of what either man produced.

---

## 8 · THE REST OF THE STANDING SUITE

Everything the standing acceptance suite asks for was run, on the eta = 0 board.

| # | law | result | number |
|---|---|---|---|
| **M1** | dial-off reproduces the landing candidate | **PASS** | `1f17644445f074d11e631b5cbae98a9a` |
| **M2** | ORDER K's own setting rebuilds byte-exact | **PASS** | `f3101883a60b0a7b8cb50f9d8a5abfff` |
| **M3** | determinism ×2 on the eta = 0 board | **PASS** | `73bf9617` = `73bf9617` |
| **M5 / G9** | day-0 entry values bit-identical | **PASS** | **89 of 89** on `derived_v0` |
| — | the printed day-0 of a sitter | **DISCLOSED, regenerates** | 87 of 89 move, 30 up / 57 down — same as ORDER K, same cause (the ruled tall factor changes the sitting discount) |
| **G7** | josh-smillie holds his ruled ~700s | **PASS** | **772** on every board in this order |
| **G8** | S1's zero-tolerance mature law | **PASS** | **0 of 429** mature rows move on the age-bar leg |
| **G12** | continuity in age | **PASS** | bar rises, never above flat, exact from 24 |
| **G12** | continuity in games | **PASS** | 8 at-bar rows, 0 falling steps |
| **G12** | continuity in pick | **PASS** | largest 0.01-pick step 5.0e-4 |
| **G12** | rho32 monotone and < 1 | **PASS** | 0 violations over g = 0 to 300 |
| **M-SC1** | the arm tables reproduce ORDER K's published cells | **PASS** | 459 comparisons, 0 mismatches |
| **M6** | the sweep instrument reproduces `REMIX_32R` | **PASS** | deviation 0.00e+00 |
| **M6** | the landing-candidate control | **PASS** | 1.0421 |
| **M7** | eta = 0 must materially raise harry-dean | **DID NOT FIRE** | +666 |
| **J-TOL** | veteran pool, per-row cap | **BREACH** | 105 of 429 rows over their own cap (ORDER K, same lane: 79) |
| **J-TOL** | veteran pool, churn cap ≤ 1,001.87 | **BREACH** | **2,923** (ORDER K, same lane: 947 — inside) |
| **J-TOL** | veteran pool, net cap ≤ 667.92 | **BREACH** | **+2,781** (ORDER K, same lane: −601 — inside) |

**The veteran breach deserves its own paragraph, and the lanes must be named or the comparison is
wrong.** The three J-TOL numbers above are read on the **whole board** lane — every lever live,
including the exempt tall factor — for both ORDER K and eta = 0, so they are like for like.

On that lane ORDER K is **inside** all three caps: churn 947 against 1,001.87, net −601 against
667.92. (ORDER K's own packet reported −695 against 667.92, over by 27; that is a **different lane** —
the gated levers with the tall factor removed — and this seat is not going to blur the two.)

**Eta = 0 is outside all three, and in the opposite direction.** Net **+2,781** against a 668 line, four
times out of tolerance. Veterans get *more expensive*, not cheaper. The cause is the one ORDER K
named: the counterweight keys on **career games**, not on age, so a 27-year-old with 20 games sits on
exactly the same curve as a 19-year-old with 20 games. Removing eta releases both.

**The board total** goes from 667,916 to **702,734**, up 34,818 points — 5.2% of the whole board. For
comparison ORDER K moved it 5,181. **444 of 804 rows move and not one of them falls**, because eta = 0
can only ever raise a price.

**Where the money goes, by career games** (eta = 0 minus ORDER K):

| career games | rows | total points | per row |
|---|---:|---:|---:|
| 0 | 89 | +0 | 0.0 |
| 1-4 | 48 | +2,569 | 53.5 |
| 5-9 | 51 | +4,875 | 95.6 |
| **10-15** | 48 | **+6,554** | **136.5** |
| **16-29** | 80 | **+11,084** | **138.6** |
| 30-59 | 100 | +4,002 | 40.0 |
| 60+ | 388 | +553 | 1.4 |

The 10-15 and 16-29 rows are where `GAMMA_D = 14` puts the peak of the bump. Gameless rows do not
move at all, which is the structural guarantee `m_d(0) = 0` promises, holding exactly.

**The largest single rises** are Willem Duursma +883, Sam Lalor +788, Sid Draper +714, Jagga Smith
+711, **Harry Dean +666**. Every one of them is 19 or 20 years old with between 10 and 22 games. That
is the bump, released.

---

## 9 · THE PREREG SCORECARD, INCLUDING WHAT I GOT WRONG

### Named rows

| row | predicted | actual | result |
|---|---|---|---|
| harry-dean | UP, into 2,550-2,700 | **3,069** | **direction HIT, range MISS — he overshot by 369** |
| cooper-duff-tytler | UP, into 1,620-1,780, short of 1,800 | **2,057** | **direction HIT, range MISS — and he was NOT short of 1,800** |
| isaac-kako | UP, by more than +44 | +88 | **HIT** |
| xavier-taylor | RISES, G6 breach | +169 | **HIT** |
| daniel-annable | RISES by more than +7 | +231 | **HIT** |
| dylan-patterson | RISES, G6 breach | +357 | **HIT** |
| josh-smillie | 772 unchanged | 772 | **HIT** |
| the four talls | relief retained in full | retained | **HIT** |
| murphy-reid, noah-mraz, logan-morris, levi-ashcroft, colby-mckercher | rise further | all rise | **HIT** |
| milan-murdock | moves toward 0 | he was −14 vs landing on ORDER K; on eta = 0 he is **+26** | **direction HIT, he went past 0 rather than to it** |

### Bands and class

| prediction | actual | result |
|---|---|---|
| class rises above 1.0513 | 1.2046 | **HIT on direction, badly short on size** |
| picks 1-10 in 7.5% to 9.5% | +31.58% | **MISS, by 22 points** |
| picks 11-20 in 10% to 13% | +29.58% | **MISS** |
| picks 21-30 in 4% to 7% | +19.81% | **MISS** |
| picks 31-40 in −12% to −9% | −1.57% | **MISS, on the good side** |
| picks 41-64 in −8% to −6% | +1.71% | **MISS, on the good side** |
| ALL 1-64 modern still sell-red, −3% to +1% | +15.72% BUY-RED | **MISS** |
| picks 21-30 modern still sell-red | −4.40% sell-red | **HIT** |
| max single class rises; the 1.139 line breaks first | it rose to 1.3087, and the +14% band rail broke at the same time | **HIT** |

**7 of 9 band predictions missed, and I want to be direct about why.** I wrote the prereg believing
what the order believed — that eta was paying for the age bar, so removing eta and lowering the dose
would roughly cancel. That model was wrong. Eta is a brake on the whole board, not a payment for one
lever. Every band prediction inherited that error, and every one of them missed in the same direction
and by roughly the same amount.

The named-row predictions, which reasoned about the mechanism on individual rows rather than about
the board, were **10 of 10 correct on direction**. The two that missed on range missed because I
under-estimated the size of the same charge.

### Falsifiers

| # | fired? |
|---|---|
| M1 dial-off ≠ 1f176444 | no |
| M2 ORDER K does not rebuild | no |
| M3 determinism | no |
| M4 S1's mature law | no — 0 of 429 |
| M5 derived_v0 not 89/89 | no — 89/89 |
| M6 the sweep instrument | no — reproduces exactly |
| M7 eta = 0 does not raise harry-dean | no — +666, so the order's diagnosis of the DEFECT was correct |
| M8 continuity | no — all four objects pass |

---

## 10 · WHAT I THINK THIS MEANS, STATED AS OPINION AND LABELLED AS OPINION

Everything above is measurement. This section is not.

**Your ruling is right about the mechanism.** A charge that reads only games played, and charges Harry Dean,
who is 14.9 points a game clear of his own age bar, exactly as hard as Daniel Annable, who is 19.0
points below his,
is not a defensible feature. Harry Dean at +221 lift and −218 charge is the proof, and it is why you
called it.

**But eta is doing two jobs, and only one of them is the bad one.** The bad job is the one you named:
it charges by games, blind to performance. The other job is holding the board's first-year
appreciation inside the no-arb rails, and it is doing that job across the entire board — every pick,
every arm, every age. Deleting eta deletes both jobs at once.

**So the honest options are three, and none of them is "set eta to zero and ship".**

1. **Keep eta and accept Dean at 2,403.** That is ORDER K. It is legal on four of six laws, breaches
   G6 by 7 points on Annable and misses your Dean and Duff-Tytler references.
2. **Keep the brake, change what it reads.** Replace the games-only bump with a charge that is
   conditional on performance against the age bar — so it still restrains the board's appreciation,
   but a man ahead of his bar pays little or none of it, and a man behind it pays more. This is a new
   mechanism and it needs its own order, its own prereg and its own calibration. **This seat did not
   build it and is not recommending it on its own word.** It is named because the measurement points
   straight at it: the brake is needed, the blindness is not.
3. **Delete eta and accept a board where a draft class appreciates 20% in a year.** The numbers for
   that board are in §4, §5 and §6. It is your call and not mine, but it should be made with the
   +31.58% on picks 1-10 in front of you.

**What I would not do is present option 3 as "the ruling delivered".** It delivers Dean and
Duff-Tytler. It also hands anyone holding a top-ten pick a free 31%.

---

## 11 · WHAT WAS BUILT, AND WHERE EVERYTHING IS

All boards built with `docs/evidence/order_m_2026-08-18/bbM.sh`, strictly sequential, one tag per
directory, five-var thread pinning on every run. No engine line was changed by this order.

| tag | setting | md5 |
|---|---|---|
| cand | dial off — the landing candidate | `1f17644445f074d11e631b5cbae98a9a` |
| K | ORDER K's ruled setting, rebuilt | `f3101883a60b0a7b8cb50f9d8a5abfff` |
| s1 | the age bar alone at dose 0.40 | `0423c8b20c0571fab0e5dd5ebc01c394` |
| **M0** | **ORDER K's knobs with ETA = 0** | `73bf961724e77f0bda996825125a07ad` |
| M0R | determinism repeat of M0 | `73bf961724e77f0bda996825125a07ad` |
| MLO | the coolest eta = 0 point in the grid | `ba97fb732cedcc653bb93cae493eccd3` |
| MMIN | dose 0.00, eta 0.31 — the smallest legal eta anywhere | `d0fa4ab799abd681516f6346bf8c9f62` |
| E10 E20 E30 E40 | ladder A, eta 0.10 / 0.20 / 0.30 / 0.40 at dose 0.40 | see `BUILD_LADDER_M_out.txt` |
| F20 F60 F70 | ladder B, the legal frontier at doses 0.20 / 0.60 / 0.70 | see `BUILD_LADDER_M_out.txt` |

Walk-forward matrices emitted for `M0ETA0`, `MLOETA0` and `MMIN031`. ORDER K's, the landing
candidate's and candidate 31's matrices were **reused, not rebuilt**.

| file | what it is |
|---|---|
| `PREREG_M.md` | the prereg, pushed before the first engine run |
| `om_sweep.py` · `SWEEP_M.json` · `SWEEP_M_out.txt` | the eta = 0 sweep, 7,560 settings, every constraint scored |
| `om_tradeoff.py` · `TRADEOFF_M.json` · `TRADEOFF_M_out.txt` | the trade-off curve — how much eta each dose needs |
| `bbM.sh` · `build_allM.sh` · `BUILD_M_out.txt` | the board suite and its identities |
| `build_ladderM.sh` · `BUILD_LADDER_M_out.txt` | the trade-off ladder boards |
| `om_gates.py` · `GATES_M.json` · `GATES_M_out.txt` | the owner's laws in board points, row by named row |
| `om_ladder.py` · `LADDER_M.json` · `LADDER_M_out.txt` | the ladder read in board points |
| `run_emit_M.sh` · `emit_allM.sh` · `EMIT_M_shell.txt` | the walk-forward emits |
| `om_bands.py` · `BANDS_M.json` · `BANDS_M_out.txt` | ND bands, both windows, six boards |
| `om_arms.py` · `ARMS_M.json` · `ARMS_M_out.txt` | pool arms, both windows, six boards |
| `om_class.py` · `CLASS_M.json` · `CLASS_M_out.txt` | the year-1 class mark on both instruments |
| `om_continuity.py` · `CONTINUITY_M.json` | age, games, pick, rho32 — at eta = 0 |
| `om_day0_identity.py` · `DAY0_IDENTITY_M.json` | derived_v0, 89 of 89 |
| `om_pages.py` · `ORDER_M_NOARB.html` | the owner document |

**Why there are not three owner documents.** The prereg declared that the player list, the year-1
class page and the no-arb tables would be produced **if outcome (a) obtained** — if a legal setting
existed. It does not. Publishing a player list for a board that breaches four of your six laws would
present it as a candidate, and it is not one. The no-arb document is produced because you need to see
the tables to make the choice in §10. `ORDER_M_NOARB.html` carries ORDER K's "what is in this board
and what is still broken" box sliced byte for byte, plus ORDER M's own additions to that list.
