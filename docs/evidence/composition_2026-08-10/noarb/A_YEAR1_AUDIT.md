# The A-at-year-1 audit — does built-A repair the D1 defect at year 1?

Owner's question: *"the whole point of A was to fix year 1, and it had zero impact at all?"*

**The short answer, given first because it is halt-grade: no. Built-A does not repair D1 at year 1 at
all. It repairs only the years-2+ version, and only for partial seasons.**

---

## 1. Reconciling the fade ladder with the gate finding

The two results are **both correct** and they measure **different factors of the same product**:

```python
_a_share(p,Y) = (1 - lam) * exp(-_ev_qual(p,Y) / _A_TAU)
                ^^^^^^^^^   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                games factor        pedigree-fade factor
lam = interp(min(gy/fE, 6), [0..6], LAM_SIT),  LAM_SIT = [0.0,0.160,0.493,0.547,0.547,0.816,1.0]
```

### Where v1 = 0.3589 was measured

In `item_a_verify.py` §3b, on a **synthetic** whose construction is stated in its own caption:

> `synthetic: identical player, identical 4 games this season, k prior full seasons`

The synthetic holds **4 games this season — deliberately below the six-game pin** — and varies `k`,
the number of prior full seasons. At 4 games, `lam = LAM_SIT[4] = 0.547`, so the games factor is
`1 - 0.547 = 0.453`, and the ladder 0.3589 → 0.0038 is the **pedigree-fade factor moving**, with the
games factor deliberately held fixed. That was its purpose: to isolate the fade.

So **"v1" in that ladder means "career year 1 *with 4 games played*", not "cohort year 1"**. It is not
a claim about what A delivers at a year-1 as-of, and the script did not present it as one.

### The verification script already reported the year-1 zero

This is not a new result overturning the verification — **the verification recorded it**, in the same
file, immediately above the fade test (lines 39-44):

> *"v1 reads 0.0000 because a rung-1 row with ns>=1 is by definition one who played a full season
> (lam=1 -> share 0); the rung-1 rows who did not play are ns==0 and are not in this population at
> all."*

**The finding was disclosed at verification time and was not carried into the act's account of what A
delivers.** That is the actual failure here, and it is mine.

---

## 2. The mutual exclusion, stated exactly

At a **year-1 as-of** the player has exactly one season, so:

```
reaching _a_blend  requires  ns >= 1  ⟺  gy/fE >= 6   (the only season must qualify)
A's share is > 0   requires  lam < 1  ⟺  gy/fE < 6
```

**The condition that admits a row to the A arm at year 1 is the condition that zeroes A's weight.**
Rows with fewer games take the `ns==0` sit-out arm and never reach `_a_blend`. Either way A
contributes exactly nothing at year 1.

From year 2 the exclusion breaks: `ns>=1` can be satisfied by a **prior** season while the **current**
season has `gy/fE < 6`.

## 3. The general form, measured

Every ND cell ITEM A actually moves (720 of them), classified by games in that as-of season:

| games in the as-of season | cells moved |
|---|---|
| **≥6 (full season → lam=1)** | **0** |
| 1-5 (partial season) | 531 |
| 0 / season absent, with a prior qualifying year | 189 |

**A never moves a single ≥6-game row, at any career year.** A acts only where the *current* season is
partial or empty *and* a *prior* season qualified.

*(An earlier version of this test returned "unknown" for all 720 rows because I keyed `games_by` by
season when it is keyed by career year, and my script printed CONFIRMED off a `full==0` that was
really `unknown==720`. That was a false pass in my own logic; the table above is the corrected test,
run off `seasons[]`.)*

---

## 4. Does built-A repair the D1 defect at year 1?

**D1, as the engine states it:** *"at ns>=1 the fitted year-0 prior is DISCARDED."* The defect fires
**at the moment of qualification** — a player's first qualifying game — which for a player who
qualifies in his first season **is cohort year 1**.

**At exactly that moment, A's share is exactly 0.** The taught year-0 correction is still discarded at
the first qualifying game, precisely as before ITEM A.

| | repaired by built-A? |
|---|---|
| Year 1, player qualifies in his first season | **NO** — share exactly 0 |
| Year 1, player does not qualify | **NO** — `ns==0`, sit-out arm, A never reached |
| Year 2+, full season (≥6 games) | **NO** — `lam=1`, share exactly 0 |
| Year 2+, partial or empty season with a prior qualifying year | **YES** — this is A's whole live domain |

**A's ruled purpose is partially undelivered.** The defect A was ruled to fix is a year-1 defect; the
built A repairs its years-2+, partial-season version only. This is reported as a **halt-grade
finding**: the sitting must not weigh A's contribution to the year-1 question as though it were
delivered, and the per-item decomposition already shows the consequence — **ITEM A owns 0.0% of the
main→FULL year-1 drop.**

**What this does not say.** It does not say A is wrongly implemented — it does exactly what its code
says, and the fade property it was verified for is real. It does not say the D1 diagnosis was wrong.
It says the **repair does not reach the year the defect was ruled against**, because the admission
gate and the weight ramp are tied to the same six-game threshold. **Whether to change that is the
owner's call; nothing is re-sited here.**
