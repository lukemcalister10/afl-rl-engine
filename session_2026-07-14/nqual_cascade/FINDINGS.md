# FINDINGS — THE nqual CASCADE, MEASURED

**Tier 3, READ-ONLY. Board of record named beside every figure.**
tag `9f8ae76` · board **`81e48293`** · store **`b0c39d78`** · engine `2030e5df` · Guard 5 PASS.
Board reconstruction is **byte-exact**: 804/804 shipped `v` reproduced, maxdiff 0. Census basis identity
confirmed independently — `n∈{1,2,3}=545` and cliff `n=3+n=4=253` reproduce item 88 exactly.

`_nqual(p,Y)` (`_merged_recover.py:106`) counts seasons with `games>=10`. That integer `n` sorts every
player into four regimes with completely different pedigree behaviour. The live level bind is `_coreM1`
(`:225`), NOT the dead twin `_lvl_eff_core`:
- `n=0` — exposure-shrunk `Lo`; the pedigree does not apply.
- `n=1,2,3` — blend `c=n/4`: `level = c·Lc + (1−c)·par`; pedigree weight `1−c` = **0.75 / 0.50 / 0.25**.
- `n≥4` (PROVEN) — the blend is discarded; **the pedigree par does not appear at all** (weight 0).

---

## T1 — THE FOUR-REGIME POPULATION (board `81e48293`)

Shipped board population (804). `lvlcurr` = trend-aware current level; `lvl_ship` = `cp._lvl_eff`; `v` = shipped value.

| regime | pedigree wt | count | mean par | mean lvlcurr | mean lvl_ship | median v | mean v |
|--------|-------------|-------|----------|--------------|---------------|----------|--------|
| n=0    | n/a (Lo)    | **256** | 58.9 | 25.5 | 55.9 | 319 | 407 |
| n=1    | 0.75        | **85**  | 63.5 | 54.0 | 59.4 | 611 | 892 |
| n=2    | 0.50        | **53**  | 65.4 | 62.2 | 62.1 | 680 | 989 |
| n=3    | 0.25        | **62**  | 69.1 | 66.2 | 65.9 | 775 | 1182 |
| PROVEN | 0 (vanished)| **348** | 71.7 | 76.6 | 73.1 | 559 | 1122 |

Blend regimes (n=1..3) = **200 board players** live on the ramp; **256** sit at n=0 (one 10-game season
from switching the pedigree ON); **348** are proven (one lost season from switching it back OFF at n=4).
Full priced pool (2652, incl. historical/non-shipped): n=0 1318 · n=1 255 · n=2 153 · n=3 137 · PROVEN 789.
(`results/t1_regime.csv`.)

---

## T2 — THE IN-PROGRESS DISTORTION (the census's 551 is inflated by the half-finished season)

We are at **R14 of 24**; `_nqual` uses a **raw** `games>=10` for the in-progress 2026 season (the D10
proration applies to the FIRST qualifying season only). `SEASON_FE=0.58`.

**The near-bar split** (my explicit definition; the census's 551 uses a wider proximity window I could not
bit-reproduce without its script — candidates bracket it: any season `==9` → 347, any season `∈{9,10}` → 606):

| proximity | full pool | board |
|-----------|-----------|-------|
| completed-season (year<2026) `==9` games — a **settled** knife-edge | 316 | 88 |
| in-progress-season (2026) `==9` games | 38 | 38 |
| union (any season `==9`) | 347 | 119 |
| **2026 games in [5.8, 10) — clears the *prorated* bar, not the raw bar** | 138 | **138** |

**How hard is the bar mid-season?** Qualifying needs 10 games; playable-so-far ≈ 22·0.58 = **12.8**. So the
effective bar is **10/12.8 = 78% of playable** now vs **10/22 = 45%** at season's end — **1.72× harder
mid-season.**

**How much of the proximity is a half-season artefact?** The 38 board players at exactly 2026`==9` are
transient, but the real distortion is a **138-strong shadow population**: board players currently *below*
the raw 10-bar in 2026 (games in [5.8,10)) who project to clear 10 by R24. Their `n` — and therefore their
regime, level and value — is pinned to the *pre-crossing* state purely by snapshot timing. Of the 138:
**41 sit at n=0** (pedigree will switch ON by R24) and **9 sit at n=3** (pedigree will VANISH by R24):
Cadman, O. Hollands, R. Maric, N. O'Driscoll, M. Rioli, H. Young, C. Brown, N. Coffield…

**Live distortion or counting artefact? BOTH, precisely.** It is a counting artefact in that "within one
game" mid-season over-states proximity (everyone is mid-accumulation). It is a *live* distortion for the
138 whose regime is provisional and **will flip by R24** — including 9 who cross the n=3→4 pedigree-vanish
cliff. This 138 is exactly the population the rejected board-wide prorated 10-bar tried to pre-credit, and
where O'Driscoll (2026=6g) and Cadman (2026=8g) live.

---

## T3 — THE CLIFF LEDGER (pure counter-tick: tick `n→n+1`, hold every level input fixed)

The counter-tick isolates the regime switch — "the lever never touched their levels; it moved them across
a cliff." **Validation that this IS the cliff and nothing else:** ticking `n` for the 240 proven players
(4→5, 5→6) moves **exactly 0** on every one. The cliff exists ONLY at 0→1 (switch ON) and 3→4 (VANISH),
plus the 1→2 / 2→3 ramp steps. Full per-regime cliff height (all pool, board `81e48293`):

| start regime | players | mean |Δ| | max |Δ| | net Σ |
|---|---|---|---|---|
| 0→1 (pedigree ON) | 1318 | 3.8 | 982 | +2232 |
| 1→2 (0.75→0.50)   | 255  | 21.4| 610 | −2154 |
| 2→3 (0.50→0.25)   | 153  | 33.9| 680 | +2945 |
| **3→4 (VANISH)**  | 137  | **67.1** | 584 | −1977 |
| 4→5 proven | 116 | **0.0** | 0 | 0 |
| 5→6 proven | 124 | **0.0** | 0 | 0 |

### T3a — the 0→1 crossers (switch pedigree ON), live, ranked by |ΔSCAR|
90 live, 50 on-board, net **+2451**, 29 with non-zero Δ (most n=0 are so exposure-shrunk that the tick
does not move the rounded price).

| player | grp | 2026g | v now | v at n=1 | ΔSCAR | note |
|---|---|---|---|---|---|---|
| **Elijah Tsatas** | MID | 6 | 1181 | **2163** | **+982** | **A8 anchor — BREAKS A8** |
| Jake Rogers | GEN_FWD | 5 | 601 | 938 | +337 | completed-9 |
| Max Gruzewski | KEY_FWD | 8 | 437 | 639 | +202 | |
| Sam Butler | GEN_FWD | 7 | 105 | 253 | +148 | |
| Ned Moyle | RUC | 6 | 1630 | 1499 | **−131** | RUC prior-cap: switch-ON *drops* value |
| Matthew Jefferson | KEY_FWD | 7 | 575 | 693 | +118 | |
| Liam Fawcett | KEY_FWD | 6 | 554 | 670 | +116 | |
| Nick Bryan | RUC | 6 | 814 | 924 | +110 | |
| Hugh Bond | GEN_DEF | 7 | 225 | 333 | +108 | |

**A8 CONFIRMED BROKEN.** A8 = "Sam Berry > Elijah Tsatas by ≥2×." Now: Berry **2731** / Tsatas **1181**
= **2.31×** (PASS). If Tsatas crosses 0→1: Berry 2731 / Tsatas **2163** = **1.26×** → **A8 fails**. This is
the exact break the rejected board-wide prorated 10-bar produced (older board: +940). Tsatas is *not*
literally one game away (best season 7g); he is moved by the **proration channel** (2026=6g ≥ prorated
5.8), which switches his high pedigree ON — the level lifts 66.7→77.2 with no new production.

### T3b — the 3→4 crossers (pedigree VANISHES), live, ranked by |ΔSCAR|
29 live, 14 on-board, net **−1147**, 11 with non-zero Δ.

| player | grp | 2026g | v now | v at n=4 | ΔSCAR | note |
|---|---|---|---|---|---|---|
| **Nathan O'Driscoll** | MID | 6 | 951 | 397 | **−554** | proration channel (rejected-lever −525) |
| **Ryan Maric** | MID | 9 | 1231 | 922 | **−309** | **A7 position anchor** |
| Oliver Hollands | GEN_DEF | 9 | 1494 | 1339 | −155 | |
| **Aaron Cadman** | KEY_FWD | 8 | 3006 | 2895 | **−111** | pick-1 KPF (rejected-lever −253) |
| Matthew Flynn | RUC | 4 | 693 | 748 | +55 | lc>par → vanish *helps* |
| Maurice Rioli | GEN_FWD | 7 | 82 | 41 | −41 | |
| Connor Budarick | GEN_DEF | 11 | 154 | 127 | −27 | |

The off-board n=3 crossers (Curtis Taylor, Ellis-Yolmen, …) are retired/inactive scrap (Δ=0). The **live,
on-board** VANISH population that the owner rules over is O'Driscoll, Maric (A7), Hollands, Cadman, Rioli,
Budarick.

### T3 — the ramp steps are the *biggest* single movers (belong to T4's question)
Because high-production kids are held DOWN by low pedigree, ticking `n` in the *blend* (1→2, 2→3) can move
far more than the boundary switches: Archie Roberts 2→3 **+680**, Josh Lindsay 1→2 +610, Sam Darcy 2→3
+559, Murphy Reid +529, Hugo Garcia +473, Mark Keane +422, Jacob Farrow +417, Jagga Smith +361, and on the
other side Archer Reid 1→2 **−252**, Sid Draper −209. These are not "one game away" (2026 already ≥10) —
they are mid-regime, and they are the T4 story.

**A-anchor / near-anchor boundary scan:** the only anchors *at* a regime boundary are **Tsatas (A8, breaks)**,
**Ryan Maric (A7, −309)**, and **Bodhi Uwland (A1 near, n=3, +550 if crossed — held DOWN by pedigree)**.
Every other named anchor (Berry, Ward, Ginnivan, Curnow, X. Duursma) is PROVEN — Δ=0, cliff-immune.
(`results/t3_cliff_ledger.csv`.)

---

## T4 — WHAT THE PEDIGREE IS WORTH, PER BLEND PLAYER (n=1..3, board)

Counterfactual: collapse the blend to pure current level and reprice. Δ>0 = pedigree HOLDS UP; Δ<0 = HOLDS DOWN.

**Net across the 200 on-board blend players = −6,820 SCAR.** The pedigree *suppresses* more than it flatters:
112 held up (Σ **+12,195**) vs 69 held down (Σ **−19,015**).

- **Held UP** (production below par — pedigree props value up): young unproven — Zeke Uwland **+526**,
  Isaac Kako +433, Samuel Grlj +391, Harry Rowston +379, Alix Tauru +353, Jed Walter +346,
  Cooper Duff-Tytler +344, Archer Reid +334, Sid Draper +317.
- **Held DOWN** (production above par — pedigree suppresses value): the breakouts — Archie Roberts
  **−1449**, Josh Lindsay −1203, Murphy Reid −999, Hugo Garcia −895, Sam Darcy −880, Mark Keane −832,
  Lachlan McAndrew −830, Max Hall −759, Tom McCarthy −732, Jacob Farrow −679, Bodhi Uwland −653.

Per-regime, the sign flips as production emerges — the fixed schedule over-weights pedigree exactly where
players are breaking out:

| n | pedigree wt | mean ped_worth | median | mean |worth| | max |worth| |
|---|---|---|---|---|---|
| 1 | 0.75 | **+52.8** (flattered) | +65 | 160 | 1203 |
| 2 | 0.50 | **−121.9** (suppressed) | +2 | 202 | 1449 |
| 3 | 0.25 | **−78.1** (suppressed) | −1 | 111 | 653 |

(`results/t4_pedigree_worth.csv`.)

---

## T5 — THE SHAPE OF THE EVIDENCE, MEASURED (Fable's `w`, not designed — measured)

Walk-forward, leak-free (record & pedigree ≤Y; forward = realised avg over Y+1..Y+3). 7,317 player-seasons,
1,295 players, as-of 2010–2024. `w*` = optimal record weight in `future ≈ w·record + (1−w)·pedigree`;
cluster-bootstrapped over players. Engine record weight = `c=n/4`.

| n | rows | corr(record) | corr(pedigree) | **w\* record** | engine c | **ped wt = 1−w\*** | 95% CI | engine ped wt |
|---|---|---|---|---|---|---|---|---|
| 0 | 1094 | 0.307 | 0.109 | 0.164 | — (Lo) | 0.836 | [0.78, 0.89] | — |
| 1 | 1160 | 0.552 | 0.144 | 0.594 | 0.25 | 0.406 | [0.34, 0.48] | 0.75 |
| 2 | 925  | 0.656 | 0.192 | 0.840 | 0.50 | 0.160 | [0.10, 0.23] | 0.50 |
| 3 | 799  | 0.699 | 0.264 | 0.889 | 0.75 | 0.111 | [0.05, 0.19] | 0.25 |
| **4** | 727 | 0.770 | 0.398 | 0.893 | **1.00** | **0.107** | **[0.04, 0.17]** | **0.00** |
| 5 | 600  | 0.810 | 0.477 | 0.873 | 1.00 | 0.127 | [0.07, 0.18] | 0.00 |
| 6+| 2012 | 0.762 | 0.380 | 0.693 | 1.00 | 0.307 | [0.27, 0.36] | 0.00 |

Games axis (R98.4, "games decide how much we trust the record"): w\* rises **0.23 (1–20g) → 0.71 (21–40g)
→ 0.90 (41–70g)** then eases (0.65 by 161+g, aging faders). Record-only RMSE 14.41 < pedigree-only 16.33;
best static blend 13.11 at w\*=0.62. (`results/t5_evidence_curve.csv`.)

**What the data says, plainly:**
1. **The record out-predicts the pedigree at *every* evidence level, including n=0** (corr 0.307 vs 0.109).
   There is no regime in which the pedigree is the better predictor. The "record beats pedigree" crossover
   is **immediate** — it happens before the first qualifying season.
2. **The engine under-trusts the record across the whole blend.** It sets record weight 0.25/0.50/0.75 at
   n=1/2/3; the data wants **0.59 / 0.84 / 0.89**. That mis-weighting is precisely why the T4 breakouts are
   held down.
3. **The 4-season cutoff is NOT supported.** Nothing discontinuous happens at n=4 — w\* rises smoothly and
   is already flat (~0.89) by n=3. And the optimal pedigree weight does **not** reach 0 at n=4: it fades to
   a **small, significantly-positive residual ≈ 0.11** (CI excludes 0) and then *rises* again for long
   careers (0.31 at n=6+, as par acts as a mean-reversion anchor for faders). The engine's hard drop to
   exactly 0 at the 4th season is an artefact, not a data feature.
4. **The measured curve is exactly R98.5's "fade, not vanish" and R98.4's trust-on-games:** one continuous
   record weight that rises with games and saturates near-full by ~40–70 career games, leaving a small
   pedigree residual that never cleanly disappears. Seasons-count (`nqual`) is a coarse proxy for the real
   axis, which is games; the four hard regimes approximate a smooth curve badly.

---

## IN PLAIN TERMS

`_nqual` is one counter with four cliffs hanging off it, and the three "edges" the owner keeps hitting are
the same line of code — the weight on the pedigree par. One extra 10-game season switches the pedigree ON
(n=0→1: Tsatas +982, which breaks A8), steps it down (0.75→0.50→0.25), or deletes it outright (n=3→4:
O'Driscoll −554, Maric −309 — an A7 anchor, Cadman −111). Proven→proven ticks move nobody, which proves
these are switches, not ramps. Half the "within one game of the bar" alarm is a mid-season mirage: 138
board players will simply cross by round 24, 9 of them straight off the pedigree cliff. And the pedigree
itself, measured against what actually predicts future output, is **mis-shaped in every direction at once**:
it under-trusts real production (net −6,820 SCAR of suppression on the breakouts), it out-weights a
pedigree that the record already beats from game one, and it zeroes that pedigree at exactly four seasons
when the data wants it to fade to a small residual that never quite vanishes. The replacement is one
continuous weight that rises with games and keeps a whisper of pedigree forever — which is Fable's job.
This is the evidence base; nothing here was wired, ruled, or proposed.
