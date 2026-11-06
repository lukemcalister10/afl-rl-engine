# P5-5 — Exit risk at the source: the age damper (HIGH; owner word + blind review)

**Goal.** r_pop(draft-age) (LEG F4, _merged_recover.py ~272–290) embeds exit risk for draft-ages 26–32 (about
0.79 by 32) and is inert from 34, so a 36-year-old's +2 value carries no exit probability and a 30-year-old's
carries a population rate unrelated to his own evidence. Replace the embedded exit component with the fitted
survival S_k(age, games) applied absolutely to every projected row (the H1 route), and remove the exit
component from r_pop so it is counted once; the within-cohort rule of the 2026-11-06 act then becomes
unnecessary and is retired in the same act (one carrier of exit risk, as §2.ix originally said).

**Why.** The survival act's disclosed double count (1.27% / 2.76% of the 26–32 lens) and the undamped veterans
(Zorko, Gawn, Pendlebury at +2) are both symptoms of exit risk living in the wrong place.

**Rules.** Value-moving on +1/+2 only; present v untouched. Measure three variants on the live board before
anything: (a) H1 absolute with r_pop's exit component removed, (b) same with the never-played kept at pick
price, (c) same plus the owner's reconciliation check (players + entrant layer within 2–3% of present). Show the
owner the before/after lens boards with movers by age and evidence, as the survival act did. Blind review.
Fit refresh: engine/rl_after/ingestion/fit_survival_hazard.py already reproduces the calibration.

**Proof.** Measurement build per variant; blind review; the landing gate set; acceptance.

**Lands via.** Lever act on the owner's word, movers shown first (RULEBOOK P1), law 11 review.
