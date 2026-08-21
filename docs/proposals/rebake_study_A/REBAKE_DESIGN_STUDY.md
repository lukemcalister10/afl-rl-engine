# THE BAND REBAKE — A DESIGN STUDY

**For Luke. Everything below is measured on this box, read-only, this session.**
No build was run, no lock was taken, nothing in the repository was written. Every number has a
script beside it in the same folder and a JSON file with the workings.

You asked for this rather than a quick answer:

> *"Before we lock in this direction, I think we need to really think deeply about our goals, our
> database, and the best way to approach this that gives the best result, instead of just quickly
> brush it off and do whatever's limited and convenient."*

So this paper does not argue. It **fits seven versions of the band, scores them on careers the
model never saw, and reports which won.** Where a figure in the existing scope paper turns out to
be wrong, it says so and gives the corrected one.

**Three things came out that change what the act should be.** They are in §1. The rest is the
evidence.

---

## 1 · THE THREE FINDINGS THAT CHANGE THE ACT

### 1.1 · Your instinct about pool careers is correct, and deleting them is the worst option measured

You said:

> *"at the worst, shouldn't [pool careers] be used to help the model learn about projecting pool
> careers themselves?"*

Measured, on careers held out of training: **removing pool careers from the band's training makes
the band's predictions for rookie-draft players 13.8% worse and for late national selections 8.1%
worse — and it also makes late first-round-to-pick-64 nationals 3.8% worse.** It is the worst of
the seven designs on every single measure: accuracy, calibration, and how often the engine's own
repair code has to fire.

It also breaks something the band's own author wrote down. `conditional_prior.py`'s first paragraph
says the model is *"calibrated to RESOLVED careers … **busts included so the lower tail is
honest**."* Pool careers carry most of the bust mass. Delete them and the floor of every band lifts
where it should not: the 10th-percentile leg goes from covering 13.8% of outcomes to covering
16.2%, when it is supposed to cover 10%.

**The "pool contamination" item in the register is not a contamination. It is the lower tail.**

### 1.2 · The library's monotonic constraint does not actually work for this kind of model

The scope paper's option **D1-a** is "switch to the histogram estimator, which supports monotonic
constraints." I checked whether the constraint is actually *enforced*. On an isolated synthetic
test, pinned library, sklearn 1.8.0:

| what was fitted | descending steps found |
|---|---|
| `HistGradientBoostingRegressor`, ordinary regression, constraint on | **0 of 240,000** — exact |
| `HistGradientBoostingRegressor`, **quantile** regression, constraint on | **185 of 240,000**, worst single step **−0.92** |
| same, on a target shaped like ours (a big lump of zeros) | **186 of 240,000**, worst single step **−2.02** |

It reproduces at every bin count and every tree count I tried. **The band is six quantile models.
So D1-a as written does not deliver "zero descending steps by construction" — it delivers about
93% of the way there and stops.**

On the real data: the constraint takes descending steps from **27.79% of all steps down to 1.83%**,
and the worst fall on a sweep from **1.65% to 0.16%**. That is a very good trade. It is not zero,
and **the scope's acceptance bar D6.1 says zero.**

**What does reach exactly zero is the ratchet you already own** — the ORDER 44 construction that
landed tonight. Applied on top of a constrained fit it hits 0 descending steps on every row tested,
and — this is the part that matters — **it then costs almost nothing:**

| the ratchet applied to… | pinball cost | value it mints | rows it moves |
|---|---|---|---|
| the **unconstrained** surface (what ships today) | +0.038% | **+0.102%** | 731 of 1,487 |
| a **constrained** surface (design b) | +0.007% | **+0.004%** | 107 of 1,487 |

**So the constraint and the ratchet are not alternatives. They are complements, and using both
makes the conservation question (D7) nearly disappear** — a mint of four thousandths of one percent
instead of the +0.61% the read-time-only fix was measured at.

### 1.3 · The band was fitted five weeks and twelve store versions ago, and I can prove exactly when

The pickles carry no training-store stamp — that is the known gap. But they carry an accidental
one. A quantile-loss model starts from a constant equal to **the exact quantile of its own training
target**, and that constant is stored in the pickle:

```
q0.10 -> 42.00000000     q0.70 -> 82.23333333
q0.30 -> 58.86666667     q0.90 -> 99.73333333
q0.50 -> 69.36666667     q0.97 -> 111.43333333   (the ceiling model)
```

I rebuilt the training target from **every one of the 29 historical versions of the store** and
asked which reproduces those six numbers.

**All five match EXACTLY, and only, on the store of 2026-07-15 to 2026-07-17** (`b1fd0bce` /
`968de0c7` / `0efdc5d6`), at **13,225 training rows**. The version before misses two of five; the
version after misses four of five.

Two further things fall out of the same test:

- **The shipped band was trained WITHOUT the T1 rule.** T1 — your word of 2026-07-31, which drops
  training rows for seasons the store cannot see — removes 64 rows. The fingerprint matches the
  **13,225-row** population, not the 13,161-row one. So the fabricated zeros you ruled out are
  still baked into the shipped artifact.
- The register's own "64 such rows of 13,221" reproduces at the 2026-07-26 to 2026-07-30 stores,
  which dates that measurement too.

**This is the answer to "creation date → which store era", and it is a measurement, not an
inference from a commit date.**

---

## 2 · GOALS — WHAT THE BAND IS FOR, STATED FIRST

### 2.1 · Which rows read it, and at what weight

`_merged_recover.py:1114` — the first line of `raw_ev`, which is the first line of every price:

```
def raw_ev(p, Y=2026):
    _bb = b6(p, Y)              # the six numbers
    pr  = price6(p, _bb, Y)     # SCALE_DIST * WQ6 · [v_at_peak(p, L) for L in _bb]
```

`WQ6 = [0.18, 0.18, 0.18, 0.18, 0.18, 0.10]`, normalised — **the five quantiles carry 18% each and
the ceiling 10%. There is no other term.** Everything downstream (evidence weight, pedigree pole,
depth clock, parity guard, availability) multiplies or shifts *this*. The band is not an input to
the price. For practical purposes it **is** the price.

**And it prices pool players.** The engine's own day-0 print, this session: *"1202 of 1202 pool rows
map to a SIGNED cell (**232 of them on the shipped board**)."* Roughly **232 of the 804 board rows
are pool entrants, and every one of them is priced through this band.** Any design that trains the
band on national careers only is asking a national-only model to price 232 rows it has never seen
the like of.

There is one more mechanical fact that bears directly on your instinct. The band's pick input is
`log(min(effpk, 70))`, and `rl_model.py:258` pins **every** pool entrant at `effpk = POOL_PICK = 65`.
So:

```
an ND pick 64 sits at log(64) = 4.1589
every pool entrant sits at log(65) = 4.1744
```

**0.0155 apart in the one number the trees split on.** The band already treats a late national
selection and a rookie as near-identical rows. Your intuition is not a proposal — it is a
description of what the model already does.

### 2.2 · What "best" means, measurably

Five things, in this order:

| goal | how it is measured here | why it is the right measure |
|---|---|---|
| **1. Accuracy** | **Pinball loss** on careers the model never saw, per quantile, averaged over six | The proper scoring rule for a quantile. Lower is better. It is the only number that can say a change is a genuine improvement rather than a preference. |
| **2. Calibration** | **Coverage** — what fraction of held-out careers actually land below each leg, against its nominal (10/30/50/70/90/97%) | A p90 that only 87% of careers fall below is not a p90. This is what "the band is honest" means. |
| **3. Monotone in skill** | Descending steps on a level sweep 40→120; worst peak-to-trough fall as a % of the band | Your Law 3. More demonstrated level must never be worth less. |
| **4. Smoothness** | Number of distinct steps per row; size of the largest step | A monotone staircase with 5 huge steps still prices two near-identical players very differently. |
| **5. Fairness across populations** | All of 1–4 broken out by ND-early / ND-mid / ND-late / ND-pool / RD-PSD | A design that wins on average by robbing the rookies is not a win. |

**Held out honestly.** A player contributes one row per season, so splitting rows at random would
let a player's own future leak into his own training rows. Every split here holds out **whole
careers, by debut year**, on a rolling origin:

```
fold 1   train debut <= 2012   test debut 2013-2015   (7,383 -> 2,181 rows)
fold 2   train debut <= 2015   test debut 2016-2018   (9,564 -> 2,169 rows)
fold 3   train debut <= 2018   test debut 2019-2021   (11,733 -> 1,487 rows)
```

That is also the question the board actually asks — predict the newest cohort from the older ones.

---

## 3 · THE DATASET, AUDITED

### 3.1 · The population, assembled exactly as `build_cond_prior` does

Store `b745002e`, `FIRST_OBSERVABLE = 2005`, resolved cut 2021, cap 2026.

```
13,283 rows before T1  ->  63 dropped as fabricated zeros  ->  13,220 rows, 1,929 players
```

| entry class | rows | share | players |
|---|---|---|---|
| ND-early (picks 1–18) | 3,497 | 26.5% | 324 |
| ND-mid (19–40) | 3,237 | 24.5% | 396 |
| RD / PSD (rookie + pre-season) | 3,011 | 22.8% | 645 |
| ND-late (41–64) | 2,713 | 20.5% | 420 |
| ND-pool (national 65+) | 648 | 4.9% | 115 |
| SSP / MSD / Irish / unrestricted | 114 | 0.9% | 29 |

| position | rows | | draft era | rows |
|---|---|---|---|---|
| MID | 3,796 (28.7%) | | 2005–09 | 4,222 (31.9%) |
| SD | 2,868 (21.7%) | | 2010–14 | 4,059 (30.7%) |
| SF | 2,563 (19.4%) | | 2015–19 | 3,185 (24.1%) |
| KPD | 1,554 (11.8%) | | 2000–04 | 1,283 (9.7%) |
| KPF | 1,425 (10.8%) | | 2020–21 | 471 (3.6%) |
| RUCK | 1,014 (7.7%) | | | |

### 3.2 · Your instinct, measured directly

You wrote:

> *"ND pick 64 is closer to a rookie draft / SSP talent / level than ND pick 1, so it doesn't make a
> huge amount of sense that late ND borrows from high ND but not pool data."*

Here is what those careers actually turned out to be — the very thing the band predicts:

| class | mean best-3 | median | p90 | never established |
|---|---|---|---|---|
| **ND-early** | **79.31** | 79.44 | 106.62 | 0.4% |
| ND-mid | 70.37 | 68.93 | 99.29 | 1.2% |
| **ND-late** | **63.80** | 64.07 | 92.73 | 3.4% |
| **ND-pool** | **63.03** | 64.80 | 95.03 | 5.6% |
| **RD / PSD** | **61.57** | 64.63 | 93.40 | 9.7% |
| SSP / other | 59.25 | 62.32 | 91.96 | 9.7% |

**ND-late is 2.2 points from the rookie draft and 15.5 points from ND-early.** Your read is right
by a factor of seven. Whatever else the rebake does, a design that walls late nationals off from
pool careers is walling them off from their own nearest neighbours.

### 3.3 · The 45.36% figure is the wrong denominator

The register (v678) and the scope paper §3.4 both say *"cm_400 trained ~45.36% on pool careers."*

**It is 1,202 ÷ 2,650 = 45.36% — the pool share of the WHOLE STORE, not of the band's training
set.** The store includes every 2022–2026 draftee, none of whom can be a training row (their
careers have not resolved). Measured on the population the band is actually fitted on:

| | measured |
|---|---|
| pool share of **training rows** | **28.54%** |
| pool share of **training players** | **40.90%** |
| the register's figure (whole store) | 45.36% |

Decomposed: rookie/pre-season **22.78%** of all rows, national-65+ **4.90%**, pickless **0.86%**.

The scope paper's §3.4 overstates the exposure by about 1.6× on rows. It does not change the
direction of anything — but a number that has been quoted three times should be right.

### 3.4 · How much of the band's own training data has moved since it was fitted

Fit-era store `b1fd0bce` (2026-07-15, identified in §1.3) against today's `b745002e`, restricted to
the **1,929 players the band trains on** and to **the attributes a training row actually reads**:

| what moved | training players | share |
|---|---|---|
| Seasons added or changed **after 2021** (three rounds of 2026) | 314 | 16.3% |
| **Age: a GUESSED value became a real date of birth** | **300** | **15.6%** |
| **Effective draft pick changed** | **144** | **7.5%** |
| — *of which crossed the pool ↔ national boundary* | **18** | *0.9%* |
| Seasons added or changed **at or before 2021** (moves the answer too) | 47 | 2.4% |
| Position one-hot changed (after normalising the vocabulary rename) | 9 | 0.5% |
| **UNCHANGED on every attribute the band reads** | **1,185** | **61.4%** |

**38.6% of the band's own training players would present a different number to at least one input,
or a different answer, if it were refitted today.**

Two of these deserve a sentence each.

- **The 300 ages.** `conditional_prior._age_asof` falls back to `18.0 + years since debut` — a
  *guess* — when the store has no birth date. Three hundred training players were taught with a
  guessed age and now have a real one. The peak model's own census calls this "the WATCHED NUMBER"
  and says it *"must fall by EXACTLY the number of rows the DOB courier writes."* The courier wrote
  302. Nobody has refitted anything since.
- **The 18 boundary crossers.** Alex Johnson (65→58), Angus Dewar (65→56), Jordan Schroder (65→55)
  and fifteen others taught the shipped band as **pool** entrants and would teach a refit as
  **national picks 55–64**.

Separately, 646 of 1,929 training players have a different raw `pick` value — but most are rookie
picks, and every pool entrant is pinned at 65, so only 144 reach the feature. **This is the
difference between "the store changed" and "the model would change", and it is worth keeping
straight.**

### 3.5 · EVERY LEARNED ARTIFACT — which are trained on data from before the big updates

Six learned artifacts determine the board. Store milestones, for reference:

```
07-05 position strip   07-11 pick convention   07-12 identity migration   07-26 rookie renumber
07-29 position vocabulary   08-06 store completion (51 back-filled seasons)
08-10 DOB courier (302 birth dates)   08-06/10/20 rounds 21, 22, 23
```

| artifact | pin | fit dated | how dated | misses | verdict |
|---|---|---|---|---|---|
| **`cm_400.pkl`** (the band, 5 quantiles) | `34faa865` | **2026-07-15 – 07-17** | **measured** — all five `init_` constants match that store and only that store | vocabulary · rookie renumber · **store completion** · **DOB courier** · **R20–R23** · **the T1 rule** | **STALE — refit** |
| **`q97m.pkl`** (the ceiling) | `cfdc7321` | 2026-07-14 (commit) | `init_` constant consistent with the 07-02 – 07-26 era; the 0.97 quantile is a weaker discriminator | same as the band | **STALE — refit, and it must move with the band** |
| **`peak_model_v4.pkl`** | `f305fe53` | **2026-08-05** (commit `dab9657`) | commit date; the file has changed exactly twice | **store completion (08-06)** · **DOB courier (08-10)** · **R21–R23** | **STALE — should join the scope** |
| **`pvc_snapshot.json`** | `ade79790` | **2026-08-05** | co-emitted by the peak-model build, same commit | same as peak model | **STALE — moves with the peak model** |
| **`bust_prior_table.json`** | `5942aa6a` | **2026-07-29** (commit `995474c`) | commit date | store completion · DOB courier · **R20–R23** | **STALE — oldest but one** |
| **`v0surf.pkl`** | `5dd34ca8` | **2026-08-13** (commit `97c6ecd`) | commit date; declared re-bake | R23 only | **CURRENT — no action** |

**Answering your question directly: five of the six are trained on data from before the big
updates. Only `v0surf` is current, and only because it was deliberately re-cut on 2026-08-13.**

**The sibling's stamp does not exist to read.** `build_peak_model_v4.py:185` writes
`training_store_stamp.json` — but to `/home/claude/rl_workspace/rl_after/`, which is **outside the
repository** and is not seeded in this container. So the one artifact that *does* have the stamp
discipline **writes its stamp somewhere the repository cannot see, and nothing asserts it.** That is
a second, separate gap from "cm_400 has no stamp at all", and the fix for both is the same: the
stamp goes **in the repo, beside the pin, and the boot guard reads it.**

**Two honesty flags on this table.** A commit date is not a fit date — it bounds it from above only.
And "stale" means *the inputs moved*, not *the output is wrong*: for the band specifically, a
previous seat measured the frozen forest's fit quality as **within 0–1.2% of a fresh fit** (register
item 168). Staleness here is a **provenance and reproducibility** problem first, an accuracy problem
second.

---

## 4 · THE CANDIDATE DESIGNS

All six quantiles fitted for each. Where a design uses the histogram estimator, the level input
carries an increasing constraint and nothing else does. Hyperparameters held at the shipped values
throughout (400 trees, depth 4, learning rate 0.05, 25 rows per leaf; ceiling 200 trees) so that
**the design is the only thing changing.**

| | design | what it is |
|---|---|---|
| **a** | **Status quo refit** | The shipped machine — classic `GradientBoostingRegressor`, no constraint — refitted on today's data. The baseline everything is measured against. |
| **b** | **Modern estimator + monotone in level** | `HistGradientBoostingRegressor`, increasing constraint on the level input only. The scope's D1-a. |
| **c** | **b + your unification, in full** | Adds, as inputs: the entry mechanism (ND / rookie / pre-season / mid-season / other), a pool flag, and **one talent ordinal spanning every mechanism** — a national pick is itself, a rookie selection chains onto that year's national end. Mechanisms with no ordinal are left genuinely **missing**; the histogram estimator handles that natively, so nobody has to invent a number. |
| **c1** | **b + your unification, law-safe** | The entry mechanism and pool flag only, **no ordinal past 64**. See the warning below. |
| **d** | **b + relevance weighting** | Every training row weighted `(n / n_class)^0.5`. **Stated plainly: `0.5` is a dial nobody derived.** 0 is unweighted, 1 makes every population count equally regardless of size. This is the honest version of "lean towards what's relevant" for a single model. |
| **e** | **Separate heads** | One model for national picks 1–64, one for the pool. |
| **f** | **Deletion** | Pool careers dropped from training entirely. The scope's old option, fitted as the strawman it is. |

> **A warning about (c) that must reach you before you rule.** RULEBOOK v2.1 law 4 — your own — says
> *"no player's price may vary with a selection number above 64."* Design **(c)** gives the model a
> number above 64 for every rookie and lets his price vary with it. **(c) as specified would need you
> to amend law 4.** That is why **(c1)** exists: it gives the model the *mechanism* without the
> *number*, which law 4 does not forbid. Both were fitted so you can see what the amendment would
> actually buy. (Spoiler: it buys nothing — see §5.)

---

## 5 · THE MEASUREMENTS

### 5.1 · Headline — accuracy, calibration and surface behaviour

Pooled over the three held-out folds. Pinball: lower is better. `covErr`: mean absolute miss on
coverage across the six legs, lower is better.

| design | pinball | vs (a) | covErr | desc-step % | rows with a drop | worst fall | steps/row | sort-fix % | ceil-fix % |
|---|---|---|---|---|---|---|---|---|---|
| **a** status quo | **3.9703** | — | 0.0380 | **27.79%** | **100%** | **1.650%** | 313 | 5.2 | 1.4 |
| **b** monotone | 3.9786 | +0.21% | 0.0380 | **1.83%** | 88% | **0.160%** | 132 | 7.1 | 1.9 |
| **c** unified (full) | 3.9931 | +0.57% | 0.0397 | 1.50% | 76% | 0.330% | 129 | 5.0 | 1.7 |
| **c1** unified (law-safe) | 3.9830 | +0.32% | 0.0398 | **1.35%** | 77% | **0.160%** | 128 | 6.0 | 2.2 |
| **d** weighted | 3.9763 | +0.15% | 0.0391 | 1.58% | 85% | 0.260% | 132 | 7.0 | 2.3 |
| **e** separate heads | 4.0455 | +1.89% | 0.0427 | 2.17% | 89% | 0.690% | 129 | 7.0 | 2.5 |
| **f** deletion | **4.1468** | **+4.45%** | **0.0452** | 2.94% | 95% | 0.220% | 146 | **11.6** | **4.6** |

**Read it like this.** Everything from (a) to (d) is within half a percent on accuracy — they are
the same model to within noise. What separates them is the third column group: **the status quo has
a descending step at 27.79% of all steps and every single row tested has one somewhere. The
constraint takes that to under 2% and cuts the worst fall by ten times, for a fifth of a percent of
accuracy.** That is the trade, and it is a good one.

Then (e) and (f) fall off. **(f) is worse on everything at once**, including — note the last two
columns — needing the engine's own crossing repairs *more than twice as often*, which means it is
producing bands whose legs come out in the wrong order.

*(The "steps/row" column is where the histogram estimator loses something: it can only place steps
at bin edges, so it carries ~130 distinct level pieces against the classic estimator's ~313.
Coarser. But **coarser and all-upward beats finer and bidirectional** for the law being enforced,
and §5.5 shows the ratchet's smoothing variant recovers the granularity.)*

### 5.2 · By population — this is where the answer is

Pinball loss, held out, with the change against the status-quo refit:

| design | ND-early | ND-mid | ND-late | ND-pool | RD / PSD |
|---|---|---|---|---|---|
| **a** status quo | 3.4009 — | 3.8394 — | 4.1448 — | 4.7969 — | 4.5058 — |
| **b** monotone | 3.3715 **−0.9%** | 3.8673 +0.7% | 4.1924 +1.1% | 4.7848 **−0.2%** | 4.4978 **−0.2%** |
| **c** unified (full) | 3.3742 −0.8% | 3.8686 +0.8% | 4.1771 +0.8% | 4.8930 **+2.0%** | 4.5952 **+2.0%** |
| **c1** unified (law-safe) | 3.3694 −0.9% | 3.8734 +0.9% | 4.1876 +1.0% | 4.8574 +1.3% | 4.5007 −0.1% |
| **d** weighted | 3.3709 −0.9% | 3.8602 +0.5% | 4.1756 +0.7% | 4.7847 **−0.3%** | 4.5038 −0.0% |
| **e** separate heads | 3.3958 −0.1% | 3.8717 +0.8% | 4.3015 **+3.8%** | 4.9923 **+4.1%** | 4.6108 +2.3% |
| **f** deletion | 3.3958 −0.1% | 3.8717 +0.8% | 4.3015 **+3.8%** | 5.1834 **+8.1%** | 5.1269 **+13.8%** |

**Four things to take from this table.**

1. **Deletion (f) costs the rookies 13.8% and the deep nationals 8.1%.** It is not a neutral
   simplification. It is a large, measured degradation of exactly the rows it claims to protect.
2. **(e) and (f) give byte-identical numbers for every national row** — because a "national head"
   *is* the deletion model. Separate heads is deletion, plus a thin second model for the pool. The
   thin-data cost is visible: the pool head, trained on 28% of the data, is 4.1% worse than the
   pooled model on its own population.
3. **Your unification, as an explicit feature, does not help — and the version needing a law
   amendment actively hurts.** (c) is **2.0% worse** on ND-pool and RD/PSD than plain (b). The
   reason is instructive: the rookie-chain ordinal is mostly noise, and the trees split on it. The
   entry-mechanism flags alone (c1) are neutral. **The pooling you want is already happening — the
   model already learns pool and national together, and telling it which is which adds nothing.**
4. **Weighting (d) does what it says, gently.** Best pool result of any design (−0.3%), best pool
   calibration of any design, essentially free. Small, real, and built on an arbitrary constant.

### 5.3 · Calibration — the miss nobody has been talking about

Observed coverage minus nominal, held out. Positive = the leg sits **too high**.

| design | q0.10 | q0.30 | q0.50 | q0.70 | q0.90 | q0.97 |
|---|---|---|---|---|---|---|
| **a** status quo | **+0.036** | **+0.054** | **+0.049** | +0.028 | −0.005 | −0.005 |
| **b** monotone | +0.038 | +0.054 | +0.044 | +0.019 | −0.008 | −0.006 |
| **c1** law-safe | +0.040 | +0.052 | +0.046 | +0.022 | −0.009 | −0.007 |
| **d** weighted | +0.044 | +0.054 | +0.052 | +0.029 | −0.007 | −0.006 |
| **e** heads | +0.057 | +0.059 | +0.048 | +0.014 | −0.022 | −0.015 |
| **f** deletion | **+0.062** | **+0.066** | **+0.061** | +0.020 | **−0.031** | **−0.022** |

**The band's floor is too high by four to five percentage points, in every design, and this study
fixes none of it.** The "10th percentile" leg actually sits where 13.6–14.4% of careers fall below
it. The three lower legs carry **54% of the band's weight**. This is a larger and more systematic
error than the staircase, and it is currently nobody's item.

It also shows exactly how deletion breaks things: (f) pushes the floor *further* up **and** the
ceiling *down* — it narrows the band from both ends, because the careers that make the tails honest
are the ones being deleted.

### 5.4 · The four staircase victims

The diagnosis's own four rows, swept 40→120 on the level input. *(Their level coordinate here is
`conditional_prior`'s own; the shipped forest was trained on the par-centred rebind, so the level
axes are not the same coordinate and the absolute band values across that boundary are not
comparable. The **roughness** comparison is, and it is the same comparison the diagnosis made.)*

Descending steps on the sweep, and the worst peak-to-trough fall:

| | Kondogiannis | Dolan | Charlie West | Will Hayes |
|---|---|---|---|---|
| **SHIPPED `cm_400`** | 172 steps, **2.14%** | 160, **1.69%** | 168, **3.04%** | 162, **3.00%** |
| **a** status quo refit | 145, 0.85% | 148, 1.07% | 143, 0.88% | 148, 1.00% |
| **b** monotone | 3, **0.006%** | 2, 0.007% | 3, 0.006% | 3, 0.007% |
| **c1** law-safe | 2, 0.024% | 1, 0.009% | **0, 0.000%** | 2, 0.026% |
| **e / f** (identical here) | 6, 0.053% | 5, 0.060% | 6, 0.051% | 5, 0.027% |
| **b + RATCHET** | **0, exactly** | **0, exactly** | **0, exactly** | **0, exactly** |
| **a + RATCHET** | **0, exactly** | **0, exactly** | **0, exactly** | **0, exactly** |

**A plain refit on current data roughly halves the damage and leaves the defect. The constraint
takes it to a rounding error. Only the ratchet takes it to zero.**

### 5.5 · What the ratchet costs, out of sample

Refitted on debut ≤ 2018, measured on the 1,487 held-out rows of debut 2019–2021:

| surface | pinball before → after | cost | band mean before → after | **minted** | rows moved |
|---|---|---|---|---|---|
| **unconstrained** (today's machine) | 4.2290 → 4.2306 | +0.038% | 70.141 → 70.212 | **+0.102%** | 731 / 1,487 |
| **constrained** (design b) | 4.2220 → 4.2223 | +0.007% | 70.002 → 70.005 | **+0.004%** | 107 / 1,487 |

Minting by population on the constrained surface: ND-early +0.002%, ND-mid +0.002%, ND-late
+0.001%, **ND-pool +0.019%, RD/PSD +0.017%** — it lifts the pool rows about ten times as much as the
national ones, which is the correct direction (they are the rows sitting on the roughest part of the
surface) and still four-hundredths of a percent.

**Caveat, stated rather than buried: these are band-space figures, not board prices.** `v_at_peak`
is not linear, so a +0.004% band lift is not a +0.004% price lift. The board-level number needs a
build and this seat did not run one.

---

## 6 · THE RECOMMENDATION

### 6.1 · Ranked

| rank | design | the case | the cost |
|---|---|---|---|
| **1** | **(b) + the ratchet retained**, with the T1 rule, on the current store | Kills 98% of the defect at the fit and the last 2% at the read, for +0.21% accuracy and a mint of 0.004%. Best or equal-best on every population. Nothing to amend, nothing to invent. | The read-site code does **not** retire (§7). The estimator changes, so every row moves. |
| **2** | **(d) = (b) + relevance weighting** | Everything rank 1 has, plus the best pool accuracy and the best pool calibration of any design. | Rests on an arbitrary `0.5`. If you take it, take it *as a declared dial with a kill-switch*, not as a derived constant. |
| **3** | **(c1) law-safe unification** | Fewest descending steps before the ratchet; one victim reaches zero unaided. Costs +0.32%. | Buys nothing the ratchet does not already buy for free. |
| **4** | **(a) status quo refit alone** | Cheapest to certify — same machine, new data. Best raw accuracy. | **Leaves the defect.** 145 descending steps and a 1% fall on Kondogiannis *after* the refit. |
| **5** | **(c) full unification** | Fewest descending steps of the unconstrained-ordinal designs. | 2.0% worse on both pool populations **and needs law 4 amended.** Do not take this. |
| **6** | **(e) separate heads** | Nothing measured recommends it. | +1.89% overall, +3.8% ND-late, +4.1% ND-pool. |
| **7** | **(f) deletion** | Nothing. | +4.45% overall, **+13.8% rookies**, worst calibration, double the crossing repairs. **Ruled out on measurement.** |

### 6.2 · The one-paragraph case

**Take design (b) — the histogram estimator with an increasing constraint on the level axis only —
fit on the current store with your T1 rule applied, and keep the ORDER 44 ratchet at the read site
rather than retiring it.** The constraint removes 98% of the staircase for a fifth of a percent of
held-out accuracy, which is inside fold noise; the ratchet removes the remaining 2% exactly, and on
a constrained surface it costs 0.007% and mints 0.004% — so the conservation question that
dominated the bounded fix simply stops being a question. Everything the owner's instinct asked for
is already true of this design: the model trains on all the data at once, pool and national
together, and the measurements say that pooling is not a contamination but the source of the band's
honest lower tail — deleting it costs the rookies 13.8% and the deep nationals 8.1%. Adding entry
type and draft position as explicit inputs was fitted and measured and does not help, and the
version of it that needs law 4 amended actively hurts the pool rows by 2%; so the unification is
achieved by *not* separating, which is cheaper than any of the alternatives and requires no ruling
at all. **The one thing this study will not let anyone claim is that the fit alone makes the defect
impossible by construction: it does not, because sklearn's monotonic constraint is not exact under
quantile loss, and that is measured and reproducible.**

---

## 7 · WHAT DISSOLVES FROM THE SEVEN DECISIONS

| | decision as posed | what the measurements do to it |
|---|---|---|
| **D1** | *Which machine — switch estimator (a), project the current one (b), or don't refit (c)?* | **RE-POSED, not answered as asked.** The options are not exclusive. D1-a **does not deliver** what the paper claims (§1.2). D1-b — the projection — is your ratchet, it is **already built and adopted**, and it is the only thing that reaches zero. **The measured answer is "a *and* b".** D1-c (don't refit) is separately dead: §3.4 shows 38.6% of the training population has moved. |
| **D2** | *Which other inputs get the constraint — level only, or level + games?* | **STANDS, unmeasured here, and now cheaper to settle.** Adding a second constraint is one more entry in a list. But note it can no longer be *justified* by "it retires the games patch", because §1.2 says a constraint does not reach zero on any axis. |
| **D3** | *Training window — same rule with current data, or move the cutoff forward?* | **PARTLY DISSOLVES.** The paper frames D3-i as "the smallest change". §1.3 shows it is not small: the fit-era store is five weeks and twelve versions old, 38.6% of training players moved, and **the shipped artifact does not carry your own T1 rule**. D3-i is the right choice, but it should be recorded as *"restore the artifact to the code that already exists"*, not *"a minimal refresh"*. D3-ii stays genuinely open and is now cheap to measure. |
| **D4** | *Hyperparameters — finer stairs?* | **LARGELY DISSOLVES.** The histogram estimator's step count is capped by its bin count (~130 pieces here against the classic estimator's ~313), so "more trees, shallower" no longer buys granularity the way the paper assumes. With the ratchet's smoothing variant already implemented, granularity is a **read-site** setting, not a hyperparameter. The shipped values were never chosen by measurement and they can stay unchanged without embarrassment. |
| **D5** | *The sentence sanctioning the refit of the frozen artifacts.* | **STANDS, AND GROWS.** §3.5: **five** of the six learned artifacts are stale, not two. The sanction should name them and rule which ride. Also — you already ruled most of this on **2026-07-15** (register item 171): fit on the fixed `par_build` so the result is re-derivable forever, correct the false `wire_redesign` comment, and commit the pinball measurement as a standing drift monitor. **This study's rank-1 recommendation is compatible with all three.** |
| **D6** | *Acceptance — what "it worked" means.* | **ONE BAR IS UNREACHABLE AS WRITTEN.** D6.1 says "zero descending steps". §1.2 proves the fit alone cannot deliver it. Either the bar becomes *"zero, with the ratchet live"* — which is achievable and was measured at exactly zero on every row — or it becomes a tolerance. **It cannot stay "zero, from the fit".** D6.2 (the 44-of-86 counterfactual going to zero) needs a build and is not measured here. |
| **D7** | *Conservation — does the pool total move?* | **LARGELY DISSOLVES.** The question was a symptom of ratcheting an unconstrained surface. Constrain first and the ratchet mints **+0.004%** instead of +0.102% in band space (§5.5). The refit itself still moves the board — that is unmeasured and needs a build — but the *fix's* one-sidedness stops being the issue it was. |
| **scope call** | *Does the pool-contamination retrain ride?* | **DISSOLVES ENTIRELY.** There is no contamination to retire. §5.2: removing pool careers is the single worst change measured. **The recommendation is not "defer" — it is "close the item, on measurement, as not a defect."** |
| **scope call** | *Does anything else from the bake queue ride?* | **ONE THING SHOULD.** Not a lever — a **fact**: `peak_model_v4` / `pvc_snapshot` (fitted 2026-08-05) and `bust_prior_table` (2026-07-29) both predate the store completion and the DOB courier. They are stale on the same inputs for the same reason. Whether they ride is your call; that they are stale is now measured, not suspected. |

---

## 8 · WHAT EVERY DESIGN MUST CARRY (non-negotiable, and free)

These are not options. They cost minutes and they are the reason this study could be written at all.

1. **A training-store stamp beside every pickle, IN THE REPOSITORY.** Store md5, row count, the
   population rule (resolved cut, cap, T1 on/off), hyperparameters, library version, feature
   definition (which `_lvl_eff` binding was live at training — the par-centred one or the raw one),
   and the old→new artifact hashes. `build_peak_model_v4.py:172-186` already writes exactly this
   object — **copy its discipline, and fix its destination**: it currently writes to
   `/home/claude/rl_workspace/`, outside the repo, where nothing can assert it (§3.5).
2. **The boot guard asserts the stamp, not just the md5.** A pin proves the file has not changed. A
   stamp proves what world it was fitted in. Register item 75 is the whole argument for this and it
   is still open.
3. **One committed, versioned refit script producing all the artifacts that move together**, with a
   reproducibility measurement recorded honestly whichever way it goes. Note the record already
   contradicts the scope paper's pessimism here: item 168 measured `PR.retrain()` as **byte-
   deterministic across two fresh interpreters**. §5.5 of the scope says non-reproducibility is "the
   *expected* state today". That is a same-box vs different-box distinction and the paper does not
   draw it — **the measured claim is narrower and more favourable than the paper's.**
4. **The pinball number becomes a standing monitor.** Your own item-171 ruling (iii). This study
   produces the baseline: the numbers in §5.1 are that monitor's zero point.
5. **The T1 rule applied.** The shipped artifact does not carry your 2026-07-31 word. A refit that
   does not apply it re-bakes the fabricated zeros back in.
6. **The band's loader gets the same HALT `q97m` and `v0surf` already have.** It is the last of the
   three that can still silently re-fit itself (correction 5 in §10). The rebake touches this loader
   anyway; the fix is one branch.

---

## 9 · WHAT THIS STUDY COULD NOT MEASURE — HONESTLY

1. **Board-level movement. Nothing here is a price.** Everything is measured in band space. `v_at_peak`
   is non-linear, so a 0.2% pinball change and a 0.004% band mint do not translate into board
   percentages at any fixed rate. **The blast radius of the estimator switch is unmeasured and it is
   the largest open risk.** It needs a build, and this seat took no lock and ran none.
2. **The 44-of-86 counterfactual.** D6.2's bar is a zero-tolerance count over true `ev()` sweeps. The
   surface measurements say the constrained-plus-ratcheted surface should send it to zero; that is
   an inference from the band, not the measurement of the count. It needs the engine.
3. **The par-centred level coordinate.** The shipped forest was trained with `cp._lvl_eff` rebound to
   `PR.lvl_par` (`par_redesign.retrain`), and the engine rebinds it again to `_inferM1` at inference.
   **Every candidate here was fitted on `conditional_prior`'s own `_lvl_eff`.** That makes the
   candidates internally consistent and comparable to each other, and makes the *roughness*
   comparison against the shipped forest fair — but it means a real rebake must decide which binding
   trains the artifact, and my numbers would shift (not, I expect, their ranking) under the
   par-centred one. **This is the largest methodological caveat in the study.**
4. **The exact fit-era store is identified by proxy, not by record.** §1.3's fingerprint matches
   three consecutive store versions (07-15 and the two of 07-17) which are identical on the
   attributes the target reads. It cannot distinguish between them, and it is blind to changes that
   touch only the *features* (positions, dates of birth, picks) — so it dates the band's **scoring
   and population** content, not the whole store. That is exactly the ambiguity a stamp removes.
5. **`q97m`'s fit is dated more loosely than the band's** — one constant is a weaker discriminator
   than five, and it matches a wider range of stores.
6. **Hyperparameters were deliberately held fixed.** D4 is therefore informed but not settled here.
7. **The 2022–2026 cohorts cannot be evaluated at all.** Their careers have not resolved. The rows
   the defect bites hardest — thin-evidence young players — are precisely the rows no held-out test
   can ever score. Every number in §5 is a proxy for them, drawn from the newest cohorts that *have*
   resolved.
8. **One weighting scheme was tried, at one exponent.** (d) at `gamma = 0.5`. A sweep might find
   something better; it would also be fitting a constant to a test set, which is worse.

---

## 10 · PROVENANCE

Read-only throughout. No build lock taken, no build run, no write to `/home/user/afl-rl-engine`.
The engine was loaded in-process against a scratch copy of `engine/rl_after` with a symlink-only
scratch repo root, exactly as `docs/evidence/movers_questions_2026-08-20/probe3.py` does. All fits
single-threaded. Base `main` @ `f071a33`, store `b745002e`, band `34faa865`, ceiling `cfdc7321`.

Scripts and results, all in this folder:

| script | what it produced |
|---|---|
| `01_store_drift.py` | `store_drift.json` — whole-store drift, fit-era seed vs today |
| `02_provenance_forensic.py` | `provenance_forensic.json` — the `init_` fingerprint method |
| `03_store_sweep.py` | `store_sweep.json` — **the fit dated against all 29 store versions** |
| `04_dataset_audit.py` | `dataset_audit.json`, `design.npz` — the population, counted |
| `05_candidates.py` | `candidates_holdout.json`, `candidates_surface.json`, `full_fits.pkl` |
| `06_monotone_check.py` | `monotone_check.json` — are the residual violations real? |
| `07_sklearn_mono_probe.py` | `sklearn_mono_probe.json` — **the library finding, isolated** |
| `08_victims.py` | `victims.json` — the four spot exhibits + the ratchet test |
| `09_summary.py` | `results_summary.json` — tables 5.1–5.2 |
| `10_ratchet_and_coverage.py` | `ratchet_and_coverage.json` — coverage direction |
| `11_ratchet_oos.py` | `ratchet_oos.json` — ratchet cost and mint, out of sample |
| `12_fitera_drift.py` / `13_feature_drift.py` | `fitera_drift.json`, `feature_drift.json` — drift on the band's own rows |

Sources read: `engine/forward_valuation/conditional_prior.py` · `par_redesign.py` ·
`dist_redesign.py` · `build_peak_model_v4.py` · `engine/rl_after/_merged_recover.py` ·
`rl_model.py` · `wire_redesign.py` · `boot_guard.py` · `bootstrap.sh` · `data/expected_boot.json` ·
`docs/proposals/REBAKE_SCOPE_2026-08-21.md` · `docs/evidence/trough_diagnosis_2026-08-20/` ·
`docs/OPEN_ITEMS_REGISTER.md` items 75, 168, 171, v678 · `docs/evidence/rulings_sweep_2026-08-13/INVENTORY.md`
· the git history of every fitted artifact and of the store.

**Corrections this study makes to the existing record, in one place:**

1. `45.36%` is the pool share of the **store**, not of the band's training set. The training figures
   are **28.54% of rows / 40.90% of players**.
2. The scope's **D1-a does not deliver "zero descending steps by construction"** — measured, isolated,
   reproducible.
3. The scope's **§3.1 retirement claim is falsified in advance**: with the new forests loaded, the
   read-time smoother will **not** find nothing to fix. It will still find ~1.8% of steps.
4. The **"pool contamination"** item is not a defect. Removing pool careers is the worst change
   measured.
5. **The band is the last of the three frozen artifacts still carrying the silent-refit footgun.**
   `cm_400.pkl` does live in the repo at `data/cm_400.pkl` — but `wire_redesign.build()` never reads
   it. Its precedence is `/home/claude/cm_{RL_PRIOR_TREES}.pkl` **and nothing else**, seeded there by
   `bootstrap.sh:73`. And on a miss it does not halt — it falls through to `PR.retrain()` and
   **silently fits a non-canonical forest**. `q97m` (owner word 2026-07-14) and `v0surf` (owner word
   2026-07-28, `_merged_recover.py:2203-2212`) both had exactly this fallback **deleted** and replaced
   with a HALT, for exactly this reason. **The band never got that fix.** `boot_guard` does catch it
   (`_resolve_cm_load` returns `None` → LOAD-PATH unresolved → HALT), so it is guarded rather than
   open — but the guard is the only thing standing between a stray `RL_PRIOR_TREES` and a quietly
   re-fitted board. **This is a one-line change and it should ride the rebake**, which touches this
   loader anyway.
