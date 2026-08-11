# ITEM A cannot act at cohort year 1 — and the prediction that follows

**Filed BEFORE the A-floor and A-drag emits landed.** The mechanism was found in the decomposition;
the prediction below is derived from it and is falsifiable by measurements already running.

---

## The measurement that started it

Per-item decomposition of the main→FULL year-1 drop, canonical instrument, ND teaching population:

| item removed | share of yr1 drop | ND year-1 cells moved |
|---|---|---|
| #336 reference layer | **80.5%** | 657 |
| the surprise law | 10.8% | 269 |
| **ITEM A** | **0.0%** | **0** |
| ITEM H | 0.0% | 1 |

ITEM A returning **exactly** zero is the signature of an inert wiring, so it was checked rather than
accepted. A is **not** inert in general — removing it moves **720 ND cells** — but it moves **zero at
years 0 and 1**, and first acts at year 2:

| yrN | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| noA cells moved | 0 | **0** | 65 | 107 | 122 | 111 | 103 |

---

## Why — a mutual exclusion between A's two gates

My first explanation was that every year-1 row takes the `ns==0` sit-out arm, which returns before
`_a_blend`. **That was incomplete and the data refuted it**: 414 of 1197 (34.6%) have
`games_yr1 >= 6`, so they *do* have `ns>=1` and *do* reach the A arm. The real mechanism is tighter:

**1. The gate that admits a row to A at year 1.** `ev()` returns at `if ns==0`, and
`nseas_pro(p,Y)` counts seasons with `year <= Y` and `games >= 6·fE`. At cohort year 1 the *only*
season is Y itself, so reaching `_a_blend` requires

```
ns >= 1   ⟺   games_yr1 >= 6·fE   ⟺   gy/fE >= 6
```

**2. The gate that zeroes A's weight.**

```python
lam = np.interp(min(gy/fe, 6.0), [0,1,2,3,4,5,6], LAM_SIT)
return (1.0-lam) * exp(-_ev_qual(p,Y)/_A_TAU)          # = A's share s
LAM_SIT = [0.0, 0.160, 0.493, 0.547, 0.547, 0.816, 1.0]
```

At `gy/fE >= 6` the interpolation is pinned at `LAM_SIT[6] = 1.0`, so `s = (1-1.0)·… = 0` **exactly**.

**The condition that admits a row to the A arm at cohort year 1 is the same condition that sets A's
weight to zero.** Rows with fewer games take the sit-out arm and never reach A at all. Either way A
contributes nothing at year 1. From year 2 onward the exclusion breaks — `ns>=1` can be satisfied by
a *prior* season while the *current* season has `gy/fE < 6`, giving `lam < 1` and a live A share.
That is exactly where the 65/107/122 cells appear.

This is **structural**, not a sizing problem. It is the same class of finding as the H ladder: an
evidence-gated mechanism cannot act in the year before the evidence exists.

---

## The prediction, filed before the data

Both round-2 ITEM A variants modify `s`, or the blend that `s` multiplies:

- **A-as-floor**: `max(e_full, b)` where `b = (1-s)·e_full + s·anch`. At `s = 0`, `b = e_full`, so
  `max(e_full, e_full) = e_full` — **a no-op**.
- **A-evidence-faded drag**: scales `s` by `(1-w)`. At `s = 0`, `0·(1-w) = 0` — **a no-op**.

**PREDICTED, and it contradicts both pre-registered expectations in `PREREG_ROUND2.md`:**

| | pre-registered in the order | predicted here |
|---|---|---|
| A-floor yr1 | rises **above** main's 1.1239 | **exactly 0.9974** (= FULL), 0 ND year-1 movers |
| A-drag yr1 | recovers **most** of the −11.3% | **exactly 0.9974** (= FULL), 0 ND year-1 movers |

Both should still move **years 2+**, where A is live — A-floor by removing the drag on hot rows,
A-drag by fading it in proportion to proof. So the variants are **not** broken; they are **correctly
implemented at a site that is structurally silent in the year the sitting cares about.**

**If the emits show year-1 movement, this analysis is wrong** and the mechanism above must be
rejected — that is the falsification condition, stated in advance.

---

## What this does *not* claim

It does **not** say the A-floor design is wrong, or that the directive's "FLOOR basis" reading was
mistaken. It says the **year-1 counterbalance cannot be delivered from the A site**, because that
site is silent at year 1. Where a year-1 counterbalance *could* act is a wiring question — the
decomposition points at the sit-out arm and #336, since those are what actually price cohort year 1
— and **that is the owner's call, not mine. Nothing is re-sited here.**
