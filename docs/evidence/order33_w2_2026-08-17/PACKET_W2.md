# PACKET — ORDER 33 SEAT W2: THE FORWARD CALIBRATION
### What SHOULD the year-1 class mark and the young-evidence spread be, judged by hindsight on classes 2005–2021?

Read-only measurement. Prereg: `PREREG_W2.md`, pushed BEFORE any number (commit 792d979).
Instrument: `w2_forward_calibration.py` (this dir), full output `RESULTS_W2.json`.
Object: walk-forward matrix `per_entrant_O31FFINAL.json` (md5 d97f1aee…, store cb38ef11, head 71d9949a,
2,648 records — all identity assertions passed). Ruler: the Order 32 S4 delivered-value construction,
constants lifted verbatim (no new ruler). Seed 33, B=2000, thread-pinned, sequential.

---

## THE HEADLINE, FOR THE OWNER

**The hindsight-fair year-1 class appreciation is ~1.10–1.11 — above your 1.08 "ideal", well above
your 1.03 floor, and comfortably under the 1.14 carry cap.** It is strikingly stable across 17 draft
classes and two eras. Your prior was a good prior; the data says nudge it up, not down.

**The candidate law currently marks year-1 classes at ~1.04 on average (walk-forward, all-arm) — about
6–7 points too low.** The live-board 2025 figure quoted in the commission (1.009 on 105 rows) is even
lower; this matrix's own 2025 class reads 1.033 on 103 rows (board vs walk-forward vantage — recorded
in the prereg, reported here, not reconciled).

**The spread verdict is a re-mix, not an amplification.** The total within-class spread is about right
(calibration slope 0.97, CI includes 1 — the prereg's trigger for a global steepness change does NOT
fire). But the mix is wrong and significantly so: hindsight loads the year-1 **production leg ~1.7×
more heavily relative to the pedigree leg** than the candidate price does (weight ratio 0.116 vs 0.068,
difference CI excludes zero). The cells show exactly where: 10–15-game and 16+-game year-1 players are
underpriced, 5–9-game poor starters are heavily overpriced, 5–9-game risers heavily underpriced.

### Why the fair level sits near the cap — the mechanical identity
Under the carry convention the hindsight-fair appreciation obeys, exactly:
**R\* = 1.14 × (1 − share of forward value delivered in year 1)**.
A year-1 entry class delivers only ~1–4% (median ~2.6%) of its discounted forward value in its first
season — rookies mostly don't play, and when they play they rarely clear the bar. So the fair mark is
mechanically close to the carry: 1.14 × (1 − 0.026) ≈ 1.11. The class appreciates almost at cost of
carry precisely because it delivers almost nothing yet. This is not a stylistic choice; it is the
no-arb law read backwards.

---

## (a) LEVEL — per-class table, ALL-ARM (primary population)

R_cand = candidate's own walk-forward yr-1/entry mark. R\*full = hindsight-fair appreciation
DV1/DV0, all observed seasons ≤2025 (the convention that carries the no-arb identity; complete tails
for early classes). R\*h6 = the prereg'd rolling 6-season window — **disclosed but structurally
invalid for the level question, see the deviation note below**. SV1sh = share of discounted forward
value delivered in year 1. yrsObs = observable future seasons at the year-1 vantage.

| class | n | R_cand | R\*full | R\*h6 | K0_h6 | SV1sh | yrsObs |
|---|---|---|---|---|---|---|---|
| 2005 | 109 | 0.9011 | 1.1161 | 1.3456 | 0.293 | 0.021 | 19 |
| 2006 | 122 | 1.0313 | 1.1198 | 1.3539 | 0.273 | 0.018 | 18 |
| 2007 | 122 | 1.0626 | 1.1086 | 1.3215 | 0.311 | 0.028 | 17 |
| 2008 | 134 | 1.0084 | 1.1020 | 1.2870 | 0.382 | 0.033 | 16 |
| 2009 | 126 | 1.0574 | 1.0692 | 1.2081 | 0.269 | 0.062 | 15 |
| 2010 | 138 | 1.1410 | 1.0998 | 1.2585 | 0.328 | 0.035 | 14 |
| 2011 | 145 | 1.1197 | 1.0978 | 1.2570 | 0.391 | 0.037 | 13 |
| 2012 | 108 | 1.0606 | 1.1165 | 1.3798 | 0.237 | 0.021 | 12 |
| 2013 | 100 | 1.0720 | 1.1329 | 1.3247 | 0.357 | 0.006 | 11 |
| 2014 | 121 | 1.0167 | 1.1288 | 1.4153 | 0.288 | 0.010 | 10 |
| 2015 | 110 | 1.1069 | 1.1038 | 1.3421 | 0.308 | 0.032 | 9 |
| 2016 | 125 | 1.0429 | 1.1130 | 1.3386 | 0.348 | 0.024 | 8 |
| 2017 | 106 | 1.0883 | 1.1014 | 1.3713 | 0.235 | 0.034 | 7 |
| 2018 | 124 | 1.0140 | 1.1012 | 1.3649 | 0.243 | 0.034 | 6 |
| 2019 | 100 | 0.9821 | 1.0968 | — | — | 0.038 | 5 |
| 2020 | 88 | 0.9767 | 1.1214 | — | — | 0.016 | 4 |
| 2021 | 108 | 1.0168 | 1.0532 | — | — | 0.076 | 3 |

**Distributions (R\*full):** all 17 classes: mean 1.1048, median 1.1038, IQR [1.0998, 1.1165],
range [1.0532, 1.1329]. Well-observed classes 2005–2015 (≥9 future seasons): **mean 1.1087, median
1.1086**, class-bootstrap 90% CI on the mean **[1.0999, 1.1167]**, per-class range [1.0692, 1.1329].
Late classes (2019–2021) are right-truncated, which mechanically overstates SV1sh and biases their
R\*full DOWN (2021's 1.053 is a floor, not an estimate). Candidate marks: mean R_cand 1.0411, median
1.0429, range [0.9011, 1.1410].

**Era stability (the honesty clause): the level is era-stable.** 2005–2014 mean 1.1091; 2015–2018
mean 1.1049; the per-class spread within eras (±0.03) exceeds the era gap (0.004). No era bound is
needed on the level proposal. ND-only runs slightly hotter: 2005–2015 mean 1.1181 (range
1.0898–1.1375) — young ND pedigree holds value into year 1 a touch better than the pool arms.

**Diagnostics:** K0_full ≈ 0.56, K1_full ≈ 0.59 (early classes) — the price language sits ~1.7–1.8×
above realized discounted delivered value in ruler units at both vantages. This is a LANGUAGE-level
constant (prices embed beyond-ruler expectations), nearly identical at entry and year 1, which is
exactly why the internal ratio R\* is the right level instrument: the language level cancels.

**Prereg deviation, disclosed:** the prereg named the H6 rolling window "primary for era
comparability". The run exposed that H6 cannot answer the LEVEL question: its two windows do not
nest (DV1_h6 contains season yr+7, DV0_h6 does not), so it measures window-rolling growth, not asset
appreciation — and it mechanically breaches the 1.14 cap (mean 1.326) for any cohort whose seasons
grow into year 7, which is every young class. The registered identity R\* = 1.14×(1−SV1sh) holds
only on FULL. The level answer therefore stands on FULL (published above in full, both conventions);
H6 is retained where it is valid — the within-class SPREAD instruments, where the window is common
to every player in the class and cancels in shares. No number was moved; the interpretation rule is
the deviation and it is disclosed here.

## (a) PROPOSED NUMBER

**Class-level year-1 appreciation target: 1.10, with the mean of marks across classes expected in
[1.100, 1.117] (bootstrap 90% CI) and any single class inside the observed dispersion band
[1.07, 1.13].** Against the owner's prior: the 1.03 floor is cleared by every one of 17 classes; the
1.08 ideal is ~2 points below what hindsight paid; the proposal stays 3–4 points under the 1.14 cap
with the margin coming directly from year-1 delivery (~2.6%) — classes that debut more players
faster (2009: R\*=1.069, SV1sh 6.2%) fairly appreciate less. The candidate's current ~1.04 is the
number to move: **+6 to +7 points of class-level appreciation is owed to the year-1 class**, most
naturally via the class-level entry basis / early-curve carry rather than via spread steepening
(see (b)).

---

## (b) SPREAD — was the thin-evidence response too flat?

All at the year-1 vantage, within-class shares, classes 2005–2018 pooled (n=1,690), H6 horizon
(valid here: common window cancels in shares).

**S1 — calibration slope (the prereg's primary trigger).** OLS of realized share on price share:
**b = 0.9675, 90% CI [0.851, 1.081]** — the CI contains 1: the registered rule for a GLOBAL
steepness change does NOT fire. Robustness: winsorized-99 slope 0.913, Spearman 0.605. Per-era:
2005–2014 0.939, 2015–2018 1.041. Per-class range 0.647 (2016) to 1.328 (2018) — noisy at class
grain, centered on 1. Verdict: the candidate's total within-class spread is the right SIZE.

**S2 — the two legs (registered, and it bites).** Regressing on the production leg (house-scored
year-1 season value) and the pedigree leg (entry v0), in class shares:

| | prod weight | ped weight | ratio W=prod/ped | 90% CI |
|---|---|---|---|---|
| hindsight (realized) | 0.567 | 4.898 | **0.1158** | [0.082, 0.163] |
| candidate (price) | 0.407 | 5.951 | **0.0684** | [0.057, 0.084] |

Difference W_hind − W_cand: 90% CI **[0.017, 0.087] — excludes zero.** Hindsight loads year-1
production ~1.7× more heavily relative to pedigree than the candidate price does. The evidence
response is too shallow — but S1 says the total spread must not grow, so the correction is a
**re-mix: move weight from the pedigree leg to the production leg**, not a global amplification.

**S3 — where exactly (games_yr1 cells; gap = realized share − price share):**

| g yr1 | n | price share | realized share | gap |
|---|---|---|---|---|
| 0 | 912 | 0.357 | 0.345 | −0.012 |
| 1–4 | 294 | 1.052 | 0.907 | **−0.145** |
| 5–9 | 192 | 1.481 | 1.379 | **−0.102** |
| 10–15 | 145 | 2.067 | 2.384 | **+0.317** |
| 16+ | 147 | 3.206 | 3.389 | **+0.183** |

Production terciles inside the thin-evidence cells:

| cell | n | price share | realized share | gap |
|---|---|---|---|---|
| 1–4 / poor | 98 | 1.043 | 0.902 | −0.141 |
| 1–4 / mid | 98 | 1.106 | 0.923 | −0.183 |
| 1–4 / riser | 98 | 1.007 | 0.895 | −0.112 |
| 5–9 / poor | 64 | 1.529 | 0.840 | **−0.689** |
| 5–9 / mid | 64 | 1.449 | 1.361 | −0.088 |
| 5–9 / riser | 64 | 1.466 | 1.937 | **+0.471** |

The picture is coherent: sitters (g=0) are priced almost exactly right — the sitter fade D(c) is
calibrated. The 1–4-game sliver is uniformly a touch rich (playing 2 games is worth less than the
mark says, regardless of how the 2 games went — evidence too thin for ρ to have signal, but the mark
carries pedigree plus a small ρ bump). The money cell is 5–9 games: the candidate prices poor
starters and risers nearly identically (1.53 vs 1.47) where hindsight pays 0.84 vs 1.94 — **a 2.3×
realized spread the price reads as flat.** And the established 10+ rookies are systematically cheap.

## (b) PROPOSED ADJUSTMENT

Per the registered rule, S1 forces no global ρ steepening (CI contains 1) — and honestly, a pure
ρ-steepening wired alone would widen total spread that is already the right size. The registered
S2/S3 instruments, which DO clear significance, support this targeted proposal for Order A:

- **Raise the production-leg loading at the year-1 vantage by ~1.7× relative to the pedigree leg**
  (target the two-leg ratio W into hindsight's band [0.09, 0.16] from today's 0.068). If wired
  purely through ρ at the thin-evidence median (g=7): ρ(7) 0.273 → 0.46, i.e. TAU_RHO 29.19 → 12.7
  at the current B_RHO — but then the pedigree leg must come down in step so the S1 slope stays in
  [0.885, 1.115]. Any wiring achieving the W band without breaking the slope band is equivalent.
- The correction concentrates in g∈[5,15]: steeper response to HOW the games went (5–9 cell), and a
  higher mark for 10–15-game debutants. The g=0 sitter cell needs nothing — do not disturb D(c) for
  spread reasons.

Constraint check: the re-mix is within-class (spread-neutral by construction at class level); the
LEVEL move (+6–7 points to ~1.10) stays under the 1.14 carry with margin 0.03–0.04. Jointly safe.

---

## (3) ACCEPTANCE BANDS FOR ORDER A (Candidate 32: G\*=2 sitter credit, delivered-season reset, age-referenced stall bars, deeper β)

Scored on THIS instrument: same matrix construction re-emitted for Candidate 32, same S4 ruler, same
class set. Numbers fixed by the measurement above (prereg SS6 form):

1. **LEVEL band.** Walk-forward all-arm class marks R_cand: the 2005–2015 class mean must land in
   **[1.100, 1.117]**; every individual class in **[1.07, 1.13]**; hard fail outside [1.00, 1.14).
   The live-board year-1 (2025) class aggregate should read ~1.10.
   *Falsified if:* the class-mean mark sits below 1.07 or above 1.13, or any class's walk-forward
   yr0→1 aggregate reaches 1.14 (no-arb breach — ONE breach falsifies the build).
2. **SPREAD-size band.** Recomputed S1 slope on Candidate 32 year-1 prices must have its point in
   **[0.885, 1.115]** (1 ± the half-width measured here).
   *Falsified if:* its CI excludes 1 on the low side with a point below 0.885 (still/more too
   aggressive-flat in the wrong mix) or the point overshoots above 1.115 (overcorrection larger than
   the candidate's current miss).
3. **SPREAD-mix band.** Recomputed two-leg ratio W = prod/ped must land in **[0.09, 0.16]**
   (hindsight's 90% CI). Direction check at the cells: the 5–9/poor gap (now −0.689) and 5–9/riser
   gap (now +0.471) must both shrink by at least half in absolute value.
   *Falsified if:* W stays below 0.084 (the candidate's current upper CI — no detectable re-mix) or
   the 5–9 tercile gaps do not shrink.
4. **Sitter guard.** The G\*=2 credit must not disturb the g=0 cell, which is currently priced right:
   recomputed g=0 gap must stay within **±0.10** (now −0.012).

## (4) HONESTY LEDGER

- Per-class dispersion is published in full above; the pooled numbers never stand alone.
- The level is era-STABLE (era gap 0.004 vs within-era spread ±0.03); the spread slope is noisier at
  class grain (0.65–1.33) and its proposal is correspondingly conservative (re-mix, banded, no
  global steepening).
- Right truncation: classes 2016+ have incomplete tails on FULL; their R\*full is biased down;
  the proposal rests on 2005–2015. H6 published, and its structural invalidity for LEVEL disclosed
  (prereg deviation note, section (a)) — the only deviation this seat took.
- The owner's prior (floor 1.03 / ideal 1.08) was registered before computation. The answer is
  ~1.10–1.11: the prior's floor is safe, its ideal is ~2 points shy. Reported as measured.
- Board-vs-matrix: commission quotes 105 rows @ 1.009; the registered matrix's 2025 class is
  103 rows @ 1.033. Both stated; the matrix is the registered object; not reconciled here.

Files: `PREREG_W2.md` (792d979, pre-results) · `w2_forward_calibration.py` · `RESULTS_W2.json` · this packet.
Seat W2, 2026-08-17. Read-only: no engine, board, or law file touched.
