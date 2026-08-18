## 2 · WHAT THE TWO DIALS DO, AND THE CONSTANTS THEY MOVE

Two new dials, both default-off, both reaching the ORDER Q charge path only.

| dial | what it sets |
|---|---|
| `RL_O39_TMAXPCT` | the percentile of the young cohort's own surplus that `TMAX` is evaluated at. Unset or 5 = ORDER P's own. Accepts **5, 15, 20** and HALTS on anything else. |
| `RL_O39_BETASAT` | the effective `BETA_sat`. Unset = ORDER P's point estimate. **HALTS outside the published 90% CI** `[0.10416359711151935, 0.1271777523096214]`. |

Setting either with no `RL_O38*` dial live HALTS, so a dial can never silently do nothing while a
board is labelled as though it had.

### 2.1 The percentiles, reproduced from ORDER P's own population before they were used

`MECH_P.json::s_p5` is `np.percentile(sP, 5)` over the 4,143 young-cohort season rows in
`STEP2_P.json`. Re-run here on the same object by the same call:

| percentile | s_pQ | check |
|---:|---:|---|
| **5** (ORDER P's own) | **−33.06133449874688** | **reproduces `MECH_P.json::s_p5` to the last bit — asserted at load, falsifier R10** |
| **15** | **−22.148794633345666** | |
| **20** | **−19.024574086528315** | |

### 2.2 The three `BETA_sat` values, each chosen from a measurement

| tag | `BETA_sat` | why |
|---|---:|---|
| **b0** | 0.11464630061141393 | ORDER P's point estimate. The control. |
| **b1** | **0.111** | The pedigree leg falls with price wherever `dPG/dln(v0) > 1/(BETA_sat·A)`. At saturation the threshold is `1/BETA_sat`. **The SMALL premium's average slope across its whole support is 8.9432** (§1), so the threshold clears at `BETA_sat < 1/8.9432 = 0.111816`. 0.111 is the round value just below. Inside the CI. |
| **b2** | **0.105** | Near the CI floor of 0.10416359711151935. 0.105 is the round value just above it. Inside the CI. **Nothing below the floor is priced.** |

**Neither b1 nor b2 was chosen by looking at a board or a row.**

### 2.3 What follows, and what is recomputed rather than carried

`THETA_R = BETA_sat / LAMBDA`. `TMAX = 1 − THETA_R·(s_pQ − s0)`. **Both are recomputed from the
effective slope every time. A stale `TMAX` HALTS (falsifier R10) and so does `LAMBDA·THETA_R ≠
BETA_sat` (falsifier R9).**

| cell | `THETA_R` | `TMAX` | a 38-game row AT the cap is charged |
|---|---:|---:|---:|
| **p5 · b0** *(ORDER P)* | 0.657439 | **21.1233** | **97.28%** |
| p5 · b1 0.111 | 0.636529 | 20.4833 | 96.97% |
| p5 · b2 0.105 | 0.602122 | 19.4301 | 96.37% |
| **p15 · b0** | 0.657439 | **13.9490** | **90.75%** |
| p15 · b1 0.111 | 0.636529 | 13.5371 | 90.07% |
| p15 · b2 0.105 | 0.602122 | 12.8594 | 88.86% |
| **p20 · b0** | 0.657439 | **11.8950** | **86.86%** |
| p20 · b1 0.111 | 0.636529 | 11.5485 | 86.06% |
| **p20 · b2 0.105** | 0.602122 | **10.9783** | **84.64%** |

**The 97.28% reproduces the owner's 97.3% on Zane Duursma exactly.** These are arithmetic on the
constants. The board consequences are measured below and they are a different thing.

---

## 3 · A FALSIFIER THIS SEAT WROTE FIRED ON ITS OWN FIRST LOAD, AND IT WAS RIGHT TO FIRE

**The assert was wrong, not the dials. It is reported here rather than quietly rewritten.**

The prereg's structural check R-S4 said the ORDER R constants may never charge MORE than ORDER P at
any surplus — "these dials may only SOFTEN". **It halted on the first in-process load**, at
`s = −2.45`, `g = 1.00`, with `0.983396689 < 0.983399171`.

**The reason is real and it is a finding about the mechanism, not a nuisance.**

`T(s0) = 1` on every board by construction. So lowering `BETA_sat` does not lower the `T` line — it
**pivots it about `s0`**. A flatter line sits ABOVE ORDER P's for `s` below `s0` and BELOW it for `s`
above `s0`.

**In plain words: the BETA lever softens the charge on every row producing UNDER the cohort centre —
which is every row the owner's complaint is about — and STIFFENS it very slightly on rows producing
just ABOVE the centre, until the zero clip catches up. The TMAX lever has no such effect. It only
lowers the cap, so it softens everywhere or does nothing.**

The assert was replaced with the true statement rather than the convenient one:

- **R-S4a, WHICH HALTS.** For every `s` at or below `s0`, the ORDER R factor must be ≥ ORDER P's.
  **The softening may never charge an underperformer more.** This passes on every cell built.
- **R-S4b, MEASURED AND PRINTED ON THE BANNER.** The window above `s0` where the charge is harsher is
  bounded and reported. At p20 with `BETA_sat` 0.105 the engine prints:

  > It charges MORE than ORDER P over s in (−2.4500, −0.8000], a window 1.6500 points a game wide,
  > and the WORST extra charge anywhere in it is **1.4472%** of the pedigree leg.

**Eight boards had already been built under the wrong assert. They were DISCARDED and the whole suite
was rebuilt, so every board in this packet carries ONE engine md5 rather than two.** That cost about
half an hour and it is the right trade.
