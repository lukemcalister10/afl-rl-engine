# ITEM A — THE RAMP, IDENTIFIED BY ABLATION: THE READING

Derived from `item_a_ablation.json` / `item_a_ablation_out.txt`. Cohort: year-1+ ND rows carrying
a record, deterministic every-5th sample, n = 60 of 303.

**Correction first, because the transcript is self-contradictory.** `item_a_ablation.py` carried a
pre-written else-branch that says LAM_SIT "moves this cohort … not at all, because none of these
rows reach that site". **Its own numbers refute that**, and the numbers govern. LAM_SIT moves the
cohort from 1.1829 to 1.3437 on `/anchor` — roughly ±6% around the 1.2444 baseline. Writing a
conclusion into a script before running it is exactly the failure the halt-no-surprise discipline
exists to prevent; I did it, the data caught it, and the corrected reading is below. The script's
prose has been fixed so the committed artifact does not carry the false claim.

---

## THE COLUMNS

baseline: mean `ev/anchor` = **1.2444** · mean `ev/production` = 2.7283 · pure production
`prod/anchor` = 1.3386

| object | ZEROED /anchor | SATURATED /anchor | moves the cohort? |
|---|---|---|---|
| **LAM_SIT** (sit-out blend) | 1.1829 | 1.3437 | **yes — 1.18 ↔ 1.34** |
| `_expgate` (POLE_RAMP exposure) | 1.1816 | 1.3025 | yes — 1.18 ↔ 1.30 |
| `iso_eff` `exp(−E_q/τ)` fade | 1.2446 | 1.2478 | **no — 0.3%, inert** |
| `_prod_path` (**CONTROL**) | **0.2293** | 1154.0 | — |

## WHAT PASSES THE ORDERED TEST: NOTHING, AND THAT IS THE FINDING

The test was: zeroed → price collapses to **pure anchor** (`/anchor` → 1.0); saturated → **pure
production**. No candidate passes, and the **CONTROL row explains why the test could never be
passed**:

> Kill the production leg entirely and the price does not fall to the anchor. It falls to
> **0.229 × anchor** — the `floor_frac(yis) × entry_anchor` schedule (0.45 at year 1, 0.35 at
> year 2, 0.28 at year 3 …, averaged over a mixed-rung cohort). Saturate production ×1000 and the
> price goes to 1154 × anchor, i.e. unbounded.

So on the year-1+ path the fitted year-0 prior is **a one-sided lower bound and nothing else**.
There is no upper anchor term, therefore no blend weight between anchor and production, therefore
no object that can "move the price from anchor-dominated to production-dominated" — **because the
year-1+ price is never anchor-dominated in the first place.** That is defect D1 restated as a
measurement rather than a claim, and it independently confirms the cap census in
`C_WIRING_PREP.md` §1, which found by code reading that no upper cap binds on a year-1 ND row.

## WHICH OBJECT IS NEVERTHELESS *THE* RAMP

Three of the four move the cohort, so "moves it" does not identify anything. The discriminator is
**what kind of object it is**:

- **`iso_eff`** — inert (0.3%). It is the *pick tax* fading on evidence, not an anchor term. Not
  the ramp.
- **`_expgate`** — moves the cohort, but it is a multiplicative partner in the **pedigree-pole**
  leg (`w = wage · tfade · expgate` in `raw_ev`), and the sitting ruled that every "what was
  expected of him" quantity — pars, z-gate expectation, **pedigree poles** — **STAYS pick/pedigree**
  under ITEM A. Barred by ruling, not by measurement.
- **`LAM_SIT`** — the engine's **only** anchor↔production blend:
  `sitout_ev = (1−λ)·R·entry_anchor + λ·e_full`. It is a genuine hand-over weight, and it is the
  only candidate whose two ends *are* the anchor and the production path by construction.

**Why LAM_SIT still moves a "year-1+" cohort, which is the whole point.** The cohort is ND rows
with *any* games. A row whose games fall below the prorated qualifying bar (`6 × fE`) still has
`nseas_pro = 0` and therefore still routes through `sitout_ev`. So LAM_SIT is **live exactly where
the anchor blend still exists — the unqualified rows — and dead the instant a row qualifies.** The
1.18 ↔ 1.34 span is the measure of how much price sits on that blend for the rows that still reach
it, and the cliff at the qualification boundary is precisely what ITEM A is ruled to remove.

## THE IDENTIFICATION, AND WHAT IT LICENSES

**THE RAMP IS `LAM_SIT`'s games ramp** — the engine's own anchor↔production hand-over — and ITEM A
is that same ramp **carried forward past `ns == 0`** instead of being switched off at the
qualification boundary, fading on **cumulative** games so that v2 borrows less than v1 and more
than v3.

This is the only reading consistent with all three constraints at once:

1. **"the EXISTING games ramp"** — LAM_SIT is an existing games ramp, and the only existing
   anchor↔production one;
2. **"no new machinery"** — the blend form `(1−λ)·R·anchor + λ·e` is reused verbatim; only λ's
   domain extends;
3. **the fading chain across ALL years** — satisfied by keying λ on cumulative games rather than
   the within-season count that resets each year.

**Wiring constraint, carried from the phase-1 finding and unchanged:** ITEM A blends at the `ev()`
level, **never inside `raw_ev`** — `_v0_uncapped` calls `raw_ev` at `Y = debutyr − 1` to build the
very year-0 prior being borrowed, so blending inside `raw_ev` is self-referential.

## HONEST LIMITS

- n = 60 sampled from 303. The ablation reads direction and magnitude; it is not a level estimate,
  and no sizing is taken from these numbers.
- `mean(ev/production)` = 2.73 at baseline is a mean-of-ratios artifact driven by rows whose
  production is near zero and whose price is held up by the floor. It is reported for completeness
  and nothing rests on it.
- `_expgate` is excluded **by ruling**, not because the measurement rejected it. Had the sitting
  not fixed the pedigree pole as pick/pedigree, `_expgate` would be a live candidate on these
  numbers and the identification would need a further discriminator.
