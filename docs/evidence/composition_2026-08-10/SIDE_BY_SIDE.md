# THE ADOPTION SIDE-BY-SIDE — old main vs the shipping configuration

**Owner ruling (filed 5249802288), verbatim:** *"H to 1, B to flat, and note these as items of
investigation for the rederivation. I think we should look to build/bake/push live what we've agreed
on with the above in mind, just to put a line in the sand and solidify the progress."*
Scope confirmed with him directly: **XW is included**; **"H to 1" is the MATNONRD cell only** — UNION
and POOLSIT stand as filed until the re-derivation.

**Branch-held. Nothing is merged and nothing is pushed live from here** — the seat runs seam
verification on these bytes and the merge and live push go through the ruled pen/adoption mechanics.

---

## 1. IDENTITIES

| | md5 | board total |
|---|---|---|
| old main (shipped today) | `4b448a821f54180182637983f7a26a9d` | 761,574 |
| pre-ruling composed package | `846560dc1b206996005c7c9e9290207c` | 723,861 |
| **THE SHIPPING BOARD** | **`94f1fec59f99c59d5890d5975c79fa9b`** | **745,888** |

**−2.06% against old main**, and **+3.04%** against the pre-ruling package. **621 of 804 rows move**
against old main (114 up, 507 down). `expected_boot` re-stamped: `board`, `config`, `engine_head`,
`fv`. Left alone deliberately: `balanced_board_md5` (a present-lens baseline that moves at a round
transition, not at a config bake) and `release_version` (the pen/adoption mechanics own promotion).

## 2. WHAT SHIPS — the composed package as ruled

| item | shipped state |
|---|---|
| era removal (salvage 1) | **ON** — as ruled |
| #336 reference layer (salvage 2) | **ON** — as ruled |
| surprise law (salvage 3) | **ON**, `RL_SUR_W=4.0` — as ruled |
| ITEM A, year-1+ anchor blend | **ON** |
| ITEM C cap release | **ON**, `RL_C_H=1.13` |
| ITEM E1 ruck wage ramp | **ON**, `RL_RUC_WAGE=1.0`; E2 wired |
| ITEM H — union sitters | **0.280, AS FILED** *(investigation item)* |
| ITEM H — all-pool sitters | **0.804, AS FILED** *(investigation item)* |
| **ITEM H — mature nonRD** | **1.0 — RETIRED BY THIS RULING** |
| **ITEM B — draft-age shape** | **FLAT — RETIRED BY THIS RULING** (`RL_B_SHAPE=0`) |
| **#336 XW — exposure-weighted par** | **ON — ADOPTED BY THIS RULING** |

**Everything experimental stays OFF and is menu/ablation machinery, not shipping config:** `RL_AGE_DISC`
(V1-V5, V9 and the STACK path), `RL_A_FLOOR`, `RL_A_DRAGFADE`, `RL_A_GSAT`, and the four #336 channel
kill-switches (`RL_336_NOP`, `RL_336_SURVLVL`, `RL_336_CLAMP`, `RL_336_PARSURV`).

## 3. THE TWO AMENDMENTS, WITH THEIR CITATIONS

**H_MATNONRD 0.615 → 1.0** (`_merged_recover.py`, citation recorded at the constant). It was a flat
**end-multiplier on the finished production-led price** (`:2228`) reading only `_pool` / `type` /
draft age and never games, level or establishment — John Noble at 158 career games took the same
0.615 as a zero-game row, and his ITEM A anchor share is exactly `0.000000`, so it was never his draft
arm re-asserting itself. Its derivation **HALTED** and was taken as filed (ruled 0.615 vs F bent
0.7676, corrected 0.5162, **CI [0.115, 1.226] containing 1.0** at eff-n 46.2), and the arm carries
**zero rows** in the canonical deciding population. Owner's standing design direction: a mature-pool
discount, if supported, belongs on the **v0/prior side where a body of work overcomes it**.

**ITEM B draft-age shape → FLAT** (`RL_B_SHAPE`, knots kept in code for the re-derivation). The
shipped factor at 21+ was `k × 2.8173 = 2.0478` (**+104.8%** on the entry anchor). It was **not fitted
to play quality**: the outcome measure `D_rt_win` is *"REALIZED DELIVERY off the seasons and bars"*
(`item_d_derive.py:22-23`), a composite raised by playing **more** as well as **better**. On the
non-rookie arm quality is flat across draft age (51.47 / 52.98 / 53.33) while the 21+ slice plays the
**least** (21.6 career games). Under a flat shape `_b_factor == 1.0` on all 1202 pool rows, so
conservation holds **trivially — delta 0.000e+00** (no value moves between ages at all).

## 4. THE COHORT TABLES, BOTH INSTRUMENTS

**Legacy picks 1-64 ND (n=1197):**

| row | yr1 | yr2 | yr3 | yr4 | yr5 | apprec | disc | margin | verdict |
|---|---|---|---|---|---|---|---|---|---|
| old main | 1.1239 | 1.3773 | 1.5098 | 1.5732 | 1.5670 | +12.39% | 14.00% | +1.61% | legal |
| pre-ruling package | 0.9974 | 1.2401 | 1.4276 | 1.5310 | 1.5328 | −0.26% | 14.00% | +14.26% | legal |
| **SHIPPING** | **1.0884** | 1.3586 | 1.4941 | **1.5660** | 1.5500 | **+8.84%** | 14.00% | **+5.16%** | **legal** |

**All-arm — the owner's deciding instrument (cohorts 2005-2023):**

| row | n | yr1 | yr2 | yr3 | yr4 | yr5 | apprec | margin |
|---|---|---|---|---|---|---|---|---|
| old main | 2209 | 0.9326 | 1.1354 | 1.2288 | 1.2936 | 1.2843 | −6.74% | +20.74% |
| pre-ruling package | 2210 | 0.8695 | 1.0835 | 1.2480 | 1.3568 | 1.3558 | −13.05% | +27.05% |
| **SHIPPING** | 2209 | **0.8850** | 1.1051 | 1.2113 | **1.2859** | 1.2685 | **−11.50%** | **+25.50%** |

**Cohorts 2019-2023 (n=540):** shipping yr1 0.8862, yr4 1.0985, margin +25.38%.

**By arm, year 4 — the repairs pull every pool arm back to within a point or two of old main:**

| arm | n | SHIP yr1 | **SHIP yr4** | **main yr4** |
|---|---|---|---|---|
| ND | 1310 | 1.0447 | **1.5166** | 1.5237 |
| RD | 620 | 0.4806 | **0.7214** | 0.7266 |
| MSD | 55 | — | **0.9485** | 0.9620 |
| UNR | 49 | 0.3276 | 0.7672 | 0.8127 |
| IRE | 47 | 0.2537 | 0.2628 | 0.3320 |
| PDA | 43 | 0.3681 | 0.7709 | 0.7778 |
| PDN | 33 | 0.1475 | 0.2575 | 0.2775 |
| SSP | 31 | 1.2499 | 1.3507 | 1.3768 |
| PDS | 21 | 0.2165 | 0.1694 | 0.1828 |

## 5. THE NAMED LINES

| player | old main | pre-ruling | **SHIPPING** | vs main |
|---|---|---|---|---|
| **Noble** | 2192 | 1330 | **2162** | **−1.4%** |
| **Hall** | 2855 | 1721 | **2820** | **−1.2%** |
| **McCarthy** | 1481 | 892 | **1468** | **−0.9%** |
| **Peatling** | 1116 | 677 | **1100** | **−1.4%** |
| **Herbert** | 1060 | 627 | **1053** | **−0.7%** |
| **Keane** | 1529 | 914 | **1514** | **−1.0%** |
| McAndrew | 1252 | 743 | 1208 | −3.5% |
| Sharman | 450 | 265 | 430 | −4.4% |
| **Banch** | 128 | 263 | **128** | **0.0%** |
| **Perez** | 113 | 232 | **113** | **0.0%** |
| **Cross** | 113 | 232 | **113** | **0.0%** |
| Podhajski | 101 | 245 | 195 | +93.1% |
| Coe / May / Mapley (MSD rucks) | 231 | 66 | **52** | **−77.5%** |
| Dovaston | 608 | 457 | 490 | −19.4% |
| Bontempelli | 3930 | 3875 | 3876 | −1.4% |
| Gawn | 3384 | 3336 | 3336 | −1.4% |
| Harry Dean | 2703 | 2328 | 2815 | +4.1% |
| **Mraz** | 3555 | 1649 | **1707** | **−52.0%** |

**Mraz sits at 1707 / 561 = 3.043× his pick-35 ruler — inside the owner's 3.5-3.8× slack.** His
remaining cut is the ruled **surprise-law** correction, which stands; ITEM H never touched him
(`_h_cut` = 1.0000, he is a national draftee at draft age 18).

**Three things that need saying plainly:**

1. **The eight named pool players are restored to within 0.7-4.4% of old main.** That is H → 1.0 doing
   exactly what the ruling intended.
2. **Banch, Perez and Cross return to EXACTLY their old main values.** B-flat un-doubled them precisely.
   **Podhajski does not** — he sits at +93.1%, because only part of his lift was ITEM B; the rest is the
   **surprise law**, which is a separately-ruled item that still ships.
3. **THE MSD RUCKS GO DOWN, NOT UP — and this is the bake working, not a defect.** Coe/May/Mapley move
   231 → 66 (pre-ruling) → **52**. Measured decomposition: XW's own effect on them is **zero**; the
   fall is B-flat removing their ×2.0478 anchor lift (×0.488), partly offset by H → 1.0 (×1.626), net
   ×0.794 — which reproduces 66 → 52 exactly. They are mature-drafted pool **sitters with no
   production**, precisely the class the ruling says should not be doubled. Their residual **−77.5%
   against old main is the surviving union-cell composition** `H_POOLSIT × H_UNION = 0.804 × 0.280 =
   0.2251`, which stands as filed and **is a recorded investigation item**.

## 6. INVESTIGATION ITEMS CARRIED TO THE POOL REPRICING ACT

1. **`H_UNION` = 0.280** — does not reproduce (F bent 0.1670, same halt, taken as filed). Unlike
   MATNONRD its **CI [0.010, 0.639] excludes 1.0**, so a cut is supported in *direction* — but 0.280 is
   **milder** than both its readings, so re-deriving on this evidence would **deepen** it.
2. **`H_POOLSIT` = 0.804** — same halt, same as-filed status.
3. **THE COMPOSITION, which no ruled evidence has ever shown.** The cells **multiply**. Before this
   bake a union-cell pool sitter took `0.804 × 0.280 × 0.615 = 0.1384` (measured 0.1398) — an **86%
   cut**. The surviving composed factor is **0.2251**.
4. **ITEM B's draft-age question**, re-opened on a play-quality basis: the shape must be fitted to *how
   they play*, not to a delivery composite that participation moves. And the arm split must be
   respected — the 21+ gradient is supported on the **rookie** arm (year-4 delivery 3.0092) and
   contradicted on the **non-rookie** arm (0.7708, below its own 19-20 slice at 0.9851).
5. **The owner's design direction for any mature-pool discount:** the **v0/prior side**, where a body of
   work overcomes it — never a flat multiplier on the finished price.
6. **The two-stories finding** that motivates the whole act: ND 1-64 returns **1.5565** per unit of
   entry price at year 4; Pool-Rookie **0.7428**; Pool-non-rookie **0.6748**. Neither pool arm is above
   its entry price even at year 6.
