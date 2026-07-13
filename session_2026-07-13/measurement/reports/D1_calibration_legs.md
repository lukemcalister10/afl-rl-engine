# DELIVERABLE 1 — THE SPEC_2/3 CALIBRATION LEGS (report-only)
**Board of record: tagged v2.9 board 81e48293 (store b0c39d78).** Numéraire (F=1.0524). Mechanism read from the
CODE. Effect size + implied correction SIZE stated. **No proposal.**

---
## 1a. JUH — Jamarra Ugle-Hagan — the 3-game cameo and the `nqual` cliff
**Player:** Jamarra Ugle-Hagan, KEY_FWD, pick 1, 2020. Scoring: 2021 (5g, 47.0) · 2022 (17g, 44.0) ·
2023 (23g, 60.6) · 2024 (22g, 63.8) · **2026 (3g, 26.0)** — the cameo. **Board value today: 187 (numéraire).**

**The mechanism (from the code).** `_nqual(p,Y)` (`_merged_recover.py:106`) counts seasons with games≥10 in the
debut window. JUH has **nqual = 3** (2022/2023/2024; the 5-game 2021 and 3-game 2026 don't qualify) — one short of
PROVEN_N = 4. So he is priced on the **career-thin blend** `c = n/PROVEN_N = 0.75` → `0.75·Lc + 0.25·par_prior`
(`_coreM1`:248), where `Lc = _lvlcurr` is the recency-weighted current level. The 3-game 26.0 cameo enters `_lvlcurr`
with full recency weight and **drags Lc down**, which is what craters the value.

**The cliff, measured** (sweep the 2026 games at avg 26.0; nqual flips 3→4 = PROVEN at games=10):

| 2026 games | 0 | 2 | 3 | 5 | 7 | 9 | **10** | 11 | 14 | 22 |
|---|---|---|---|---|---|---|---|---|---|---|
| nqual | 3 | 3 | 3 | 3 | 3 | 3 | **4** | 4 | 4 | 4 |
| board | 1009 | 483 | 187 | 184 | 142 | 119 | **105** | 105 | 105 | 105 |

**It is a SLOPE first, a cliff second.** The dominant penalty is the recency **slope**: from no cameo (1009) down
through 3/9 games (187/119) as the low-level cameo drags `_lvlcurr`. The `nqual`-threshold **step** (9g→10g:
119→105) is small (−14), but at nqual=4 he becomes PROVEN at a low realized level and **craters to a hard floor of
105, flat thereafter** — so *playing MORE at a low level lowers value* (the register's "1056→106"; measured 1009→105).

**Attribution of the ≈−822 (no-cameo 1009 → actual-cameo 187).** Almost all of it is the **recency-level drag** from
the 3-game 26.0 cameo inside the career-thin blend (he stays at nqual=3 in the actual case, so the nqual step is NOT
paid). Counterfactuals: cameo removed → 1009 (cost of the cameo = **−822**); a healthy 22-game 63.8 2026 → 794 (cost
vs healthy = **−607**). **Effect size: the low cameo costs 607–822 numéraire; the nqual=4 boundary adds a further
step to a hard 105 floor. Implied correction size ≈ 600–820** — but the shape to fix is the perversity (more low
games ⇒ less value), not a level shift. Sample: one named anchor; the cliff sweep is deterministic on the tagged board.

---
## 1b. RYAN — Luke Ryan — the `_fbump`
**The mechanism (from the code).** `_fbump(a,lcr)` (`_merged_recover.py:97`) is an **UP-ONLY, form-conditioned
credit** added to the age-decline multiplier: `_agemult2 = clip(_agemult(age) + _fbump(age,lcr), 0.53, 0.98)`
(:101-104). It is a 2-D interpolated table (age × `lcr` = current level above positional replacement), non-decreasing
in `lcr`, non-increasing in age. It is **reached ONLY on the shed down-branch** — a player with nqual≥4, a level drop
`Lo−Lc > DOWN_TOL(3)`, and `lcr > 0` (still above replacement). It stops a *still-elite* elder being over-sheded by age alone.

**Census (every row where `_fbump` fires: nqual≥4, shed branch, lcr>0, `_agemult2 > _agemult`): 34 players.**
**Total board SCAR the term moves: +917 (numéraire). Median +0, max +418.**

| player | pos | age | lcr | bump | board SCAR |
|---|---|---|---|---|---|
| Sam Walsh | MID | 26 | 18.4 | 0.127 | **+418** |
| Dan Houston | GEN_DEF | 29 | 9.4 | 0.094 | +108 |
| Charlie Curnow | KEY_FWD | 29 | 6.3 | 0.087 | +66 |
| Adam Cerra | MID | 27 | 4.5 | 0.092 | +58 |
| Touk Miller | MID | 30 | 18.7 | 0.106 | +44 |
| **Luke Ryan** | **GEN_DEF** | **30** | **18.2** | **0.105** | **+41** |
| … (28 more, most rounding to 0) | | | | | |

**Ryan is TYPICAL of the term, not an outlier.** Luke Ryan (GEN_DEF, age 30, lcr 18.2) carries **+41 numéraire** —
close to the modest cluster; the **median firing player moves +0** (the predicate fires but the value effect rounds
away). The **outlier is Sam Walsh (+418)**, who alone is ~46% of the term's total. **Effect size: `_fbump` is a
SMALL term (+917 total across 34 players, one player carrying nearly half); Ryan's leg is ~+41.** Implied correction
size for the Ryan case specifically: tens of SCAR, not hundreds. Sample: full board census, deterministic.

---
## 1c. DYLAN MOORE — the missing body-of-work axis
**Player:** Dylan Moore, GEN_FWD, pick 66, 2017. Scoring: 2021 (20g, 76.5) · 2022 (22g, 94.6) · 2023 (23g, 91.0) ·
2024 (25g, 96.5) · 2025 (26g, 87.5) · **2026 (12g, 71.3)** — the dip. **Board value today: 1450 (numéraire).**

**The dip penalty (verified, matches the −694…−1009 read).** Board with the 2026 dip = 1450. Counterfactuals: a
healthy 22-game 90.0 2026 → 2228 (**dip penalty −778**); the 2026 removed → 2409 (**penalty −959**). So a single dip
season costs Moore **778–959 numéraire** — inside the flagged −694…−1009. It is priced through the shed down-branch
(`_coreM1`, `_lvlcurr` dragged by the 71.3 dip) and the KEY/GEN residual paths; the model carries **no term that
lets a five-year 90-plus body of work buffer one down year.**

**The axis that is missing — measured on the walk-forward record.** Across **4,787 player-seasons** (real store rows,
season Y games≥10 and Y+1 games≥6): does a player's **career body of work** (games-weighted mean of prior seasons)
predict his **next season**, over and above his **most recent season**?

- Partial slope (next-season SC per point of career-BoW, controlling for the recent season): **+0.144**
- Partial correlation (BoW ⟂ recent, vs next): **+0.126**
- Incremental R² of adding BoW to a recent-only model: **+0.0069** (R² 0.5603 → 0.5672)
- Smoothed partial-dependence (BoW residual → next-season residual): monotone increasing but shallow — across the
  full BoW spread (−18 to +18) the next-season residual moves only about **−2.0 → +2.9 points**.

**The answer is "real but small."** Career body of work DOES carry information about next season beyond the most
recent year — the owner's direction is supported — but the **effect size is modest**: ~0.14 pts of next-season per
point of body-of-work, <1% incremental R², a few SC points across the whole range. **Implied correction size:** a
durable player's dip should be buffered by a few next-season points (worth a few hundred SCAR at Moore's level),
**not** the full 778–959 the model currently charges. The record does not support pricing Moore as if the dip never
happened — but it does support softening a single-year dip for a long, high body of work by a small, measured amount.
Sample: 4,787 player-seasons; a negative-leaning result, stated plainly as the directive asked.
