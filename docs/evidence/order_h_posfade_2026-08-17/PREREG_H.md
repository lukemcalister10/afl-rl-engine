# PREREG_H — the position lens on the year-1/2 sitter fade

**Pushed before any outcome number was computed.** Read-only seat. Nothing wires.

Brief: the owner, 2026-08-17, on issue #334 — *"did you only look at it through a pick lens, or
positionally as well? Rucks sitting would be very different to mids sitting in year 1/2"*.

Order D fitted the sitter fade as a curve in draft pick and nothing else. The curve it produced
(`kappa(pick)`) is position-blind. This seat asks whether that is a mistake at the year-1/2 grain.

---

## 1. The owner's hypothesis, registered as this seat's prediction

**H1.** At a fixed draft pick, a year-one sit raises the odds of a five-year washout **LESS** for a
ruck than for a small (mid / small defender / small forward).

**H2.** The same holds, more weakly, for key-position players (key defender + key forward).

**H3 (the premise behind H1/H2).** Early sitting is **more common** for rucks and key-position
players than for smalls. This is the owner's stated reason — tall development normally includes
sitting, so a tall who sits is an ordinary tall, while a small who sits is a warning.

**H4 (the decision-relevant version).** The same ordering shows up in **value retention**, not only
in washout odds. Order D's own packet said value retention is the object that matters, because the
fade multiplies an entry price. So H1 must survive on that ruler too, or it does not carry.

If all four hold, the rulings-material output is a **smooth position adjustment** to the wired
`kappa` curve. If they do not, the finding is that the pick curve stands position-blind.

---

## 2. What is already known, so this seat does not re-litigate it

- Order D, `docs/evidence/order_d_2026-08-17/` — fitted `s(p) = 0.1286 + 0.4536 * ln(pick)` on
  washout odds, solved the redistribution constant `s_norm = 1.7472`, and published the value
  contrast: top-10 sitters keep **0.535** of entry-relative forward value, picks 21-30 keep
  **0.128**. Position was never entered.
- Order 30A / 30A-2, `docs/evidence/sitter_fade_2026-08-14/` — tested a six-way position lens at
  **multi-year depth** and ruled it **noise**, recommending a position-blind discount. That test was
  at depth 2-5 on the whole fade, not on the year-1/2 sitting *signal* at fixed pick. The owner's
  question is at a grain 30A did not test.
- Order C / repair attribution — young **RUCK** was the worst-marked cell on the board, −43 points
  against fair. That is a hint the position carries something the pooled law is missing, and it is
  the reason this seat is worth running.

---

## 3. Population and ruler — transplanted from Order D, unchanged

Both are copied from `docs/evidence/order_d_2026-08-17/o35_fit_curve.py` and
`o35_value_contrast.py`. No constant is re-derived here.

- **Source:** `per_entrant_O32RFINAL.json` (store `cb38ef11`, engine `bf63592c`, board
  `7802ee97`).
- **Population:** national-draft entrants that teach the curve, classes **2005-2020**, picks
  **1-64**, minus the two force-majeure keys (`paddy-mccartin`, `thomas-boyd`). **n = 1015.**
- **Washout ruler:** sum over seasons `year+1 .. year+5` of `games x max(0, avg - positional bar)`.
  Bars `KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9`. Washout = that sum is zero.
- **Value ruler:** delivered value from `year+2` onward, discounted to year 1 at carry `1.14`,
  divided by `v0` (the landed day-0 entry price). Retention `F` for a group is
  `sum(dv over sitters) / sum(v0 over sitters)` divided by the same ratio over that group's
  controls. Identical to D's `o35_value_contrast.py` down to the softplus constants.

---

## 4. The specification choice, and why it is being declared here

Before writing this prereg I counted **cell sizes and base rates only** — how many players sit, per
position, per pick band. No washout outcome and no value number was computed. I am declaring the
counts because they force a specification choice that must not be made after seeing results.

| group | n | sat year 1 (0 games) | played 1+ | played 11+ |
|---|---:|---:|---:|---:|
| RUCK | 53 | 35 | 18 | **1** |
| KPP (KPD+KPF) | 226 | 106 | 120 | 24 |
| SMALL (MID+SD+SF) | 736 | 267 | 469 | 188 |

**Order D's primary contrast — sitters vs players with 11+ games — does not exist for rucks.**
There is exactly one such ruck in sixteen draft classes. Any ruck interaction estimated against that
threshold would be a single player's career.

Therefore, **declared in advance**:

- **PRIMARY spec for this seat: sitters (0 games) vs ALL who played (1+ games) in year one.** This
  is Order D's own *secondary* specification, reported in `O35_CURVE.json` as
  `secondary_all_played`. It is being promoted to primary here for the single stated reason that the
  11+ control is empty for rucks. Nothing else about D changes.
- **SECONDARY spec: D's primary (0 vs 11+).** Reported for SMALL and KPP. Reported for RUCK only
  pooled into TALL, and flagged unusable if the pooled ruck control is still under 10.

Both are published side by side whatever they say.

## 4b. Position groups

- **RUCK** = `pos == RUCK` (n=53).
- **KPP** = `KPD + KPF` (n=226).
- **SMALL** = `MID + SD + SF` (n=736) — the reference group.
- **TALL** = RUCK + KPP (n=279), the pooled alternative.

**Declared in advance:** the primary reading is the **three-group** split, because the owner's
question is specifically about rucks and pooling them into talls would answer a different question.
The **TALL pooled** reading is published beside it in every table. If the two disagree in sign on
the ruck term, the seat reports the question **unresolved** and proposes nothing.

Known limitation, stated now: `pos` is the record's career position label, not a draft-night label.
A player drafted as a key forward who became a ruck is counted as a ruck. This cannot be fixed from
this store and is not treated as a defect to be smoothed over — it is a reason to hold the ruck
reading loosely.

## 4c. Sitting at the year-1/2 grain

The owner said "year 1/2". Two treatments, both published:

- **SAT1** = zero games in year one. This is D's treatment, and it is what the wired curve keys on.
- **SAT12** = zero games in years one **and** two combined. Counts: RUCK 19, KPP 56, SMALL 131.

SAT1 is primary because it is the treatment the wired curve already uses; SAT12 is the direct read
of the owner's phrase and is reported in full beside it.

---

## 5. The model

Logistic, fitted by the same IRLS routine as D, on the pooled fit rows:

```
logit P(washout in 5 years)
    = a + b*ln(pick)
    + c_KPP*I(KPP) + c_RUCK*I(RUCK)
    + SAT * ( g0 + g1*ln(pick) + h_KPP*I(KPP) + h_RUCK*I(RUCK) )
```

`h_RUCK` and `h_KPP` are **the interaction coefficients**, in log-odds, relative to SMALL. They are
the answer to the owner's question.

**H1 predicts `h_RUCK < 0`. H2 predicts `h_KPP < 0`.**

The pick slope of the sit penalty, `g1`, stays **pooled across positions**. Declared in advance:
with 53 rucks spread over 64 picks, a ruck-specific pick slope is not identifiable, and fitting one
would produce a number with no information in it. A tall-pooled version of that slope is fitted as a
reported secondary only.

**Uncertainty:** player-level bootstrap, B=1000, seed 35 (D's seed), 90% percentile intervals.
Reported for every coefficient, plus the share of draws in which `h_RUCK < 0`.

**Determinism:** the harness is run twice and the two output md5s are published. If they differ the
result is withdrawn.

---

## 6. Falsifiers — declared before any result

The hypothesis is the owner's, so the falsifiers are written to be able to embarrass it.

- **F1.** `h_RUCK >= 0` at the point estimate. The direction is wrong; H1 fails; no adjustment.
- **F2.** The 90% bootstrap interval on `h_RUCK` contains 0. The seat reports **unresolved at this
  sample size** and proposes nothing. A thin cell that leans the right way is not evidence.
- **F3.** Value retention contradicts washout odds — i.e. `F_RUCK <= F_SMALL` at comparable picks.
  Under D's own logic value is the deciding ruler, so this kills the adjustment even if the odds
  interaction is clean.
- **F4.** The base-rate premise fails — sitting is **not** more common for rucks/talls than for
  smalls. Then the owner's stated mechanism is not in this data and the seat says so.
- **F5.** The three-group and TALL-pooled readings disagree in sign on the ruck term → unresolved.
- **F6.** The SAT1 and SAT12 readings disagree in sign on `h_RUCK` → the effect is not stable across
  the two ways of reading "year 1/2" → reported as unresolved rather than as a law.
- **F7.** Any proposed adjustment that would need a **cliff** — a different rule for rucks than for
  the pick either side of a boundary — is not proposed at all. The owner's trend law forbids it.

---

## 7. The shape of the proposed adjustment, committed in advance

So the fit cannot be reverse-engineered into a convenient form after the fact.

If and only if F1-F7 all pass, the proposal is the **natural extension of D's own construction**:

```
s(p, g) = g0 + g1*ln(p) + h_g                 (h_SMALL = 0 by construction)
kappa(p, g) = clip( s(p, g) / s_norm' , 0.5, 2.0 )
```

`s_norm'` is re-solved by the same bisection D used, so the same identity still holds: the mean over
the fitted sitters of `D2 ^ kappa(p,g)` equals the ruled depth-2 fade `D2 = 0.5582775`. **The
adjustment redistributes the fade across positions; it does not change the total.** That is the same
promise D made across picks.

This is a **smooth shift in log-odds**, which is a smooth shift on kappa. No cliffs, no bands.

The owner named a multiplicative position factor. That form is also published: the implied
`m_g = mean over picks 1-64 of kappa(p,g) / kappa(p)`, so the adjustment can be taken in the shape
he asked for. The additive-in-log-odds form is the one the fit produces and is the one recommended;
the multiplicative factor is the translation.

**Sizing is read off the fit. It is not chosen.**

---

## 8. Named rows to be shown either way

The current roster rows the owner will actually price, shown with what the adjustment would do —
or, if the finding is null, shown unchanged as a demonstration that nothing moves:

`will-green` (RUCK, pick 16, 2023) · `alex-dodson` (RUCK, pick 53, 2024) ·
`toby-conway` (RUCK, pick 24, 2021) · `ned-moyle` (pool RUCK, 2021) ·
`nick-madden` (pool RUCK, 2022) — plus **mid/small sitters at the same picks** as the contrast,
which is the comparison the owner actually asked for.

Stated in advance: every one of these is a 2021-2024 entrant and therefore **outside the 2005-2020
fitting window**. They are what the ruling would price, not what it is fitted on. Pool rows
(`ned-moyle`, `nick-madden`) sit outside the ND 1-64 curve entirely and are shown for orientation
only — a pick-keyed curve does not reach them.

---

## 9. What this seat will not do

No engine file, board, store, law or curve is touched. This produces `PACKET_H.md` and its
supporting JSON. Whether it rides the landing candidate or follows it is the owner's call.
