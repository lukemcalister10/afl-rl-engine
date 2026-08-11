# What a #336 design would look like — and what it can and cannot recover

**For the owner. Measurement only. No design is built, no dial is set, nothing ships.**
Filed from #334 ORDER 3 / 3b. Every number names its instrument.

---

## 1. The question

You asked two things:

> "What would a #336 design look like? What do you think it would do to the issue?"

The issue is the year-1 hole. Before the composition package, a draft class was worth about 12% more
one year after the draft than on draft day. After the package it is worth about the same as on draft
day. That is a drop of 11.3%. The measurement said 80.5% of the drop belongs to the #336 reference
layer — about 9.1 points of it.

**This memo answers where those 9.1 points went, and whether a design can get them back.**

---

## 2. How the answer was found

The #336 layer went in as one commit. It had no switch. To measure it you had to remove all of it.

Round 3 gave it three switches, one for each part of what it does, and then priced the whole draft
history three more times — once with each part turned back to the old behaviour. The instrument is
the same cohort table used for every other number in this act: 1,197 draftees, picks 1 to 64, draft
classes 2004 to 2022, busts kept in at zero.

The three parts:

| part | what it does | plain words |
|---|---|---|
| **(a) the bust charge** | multiplies a pick's reference level by the chance a player from that slot ever plays six games in a season | "one in three never establishes, so charge for it" |
| **(b) the level sample** | counts players who established but never had a big season, at their real level instead of leaving them out | "a small career is a small number, not a missing number" |
| **(c) the par sample** | fits the development benchmark on every season an establisher actually played, instead of only his six-plus-game seasons | "a faded season is a low season, not an absent one" |

---

## 3. The answer, in one table

Year-1 cohort book. FULL is the package as it stands. The "give-back" is how much year 1 comes back
when that part is turned off.

| part | year 1 | give-back | share of the 9.1 points |
|---|---|---|---|
| (a) the bust charge | 0.9972 | **−0.0002** | **−0.2%** |
| (b) the level sample | 1.0073 | +0.0099 | 9.7% |
| (c) **the par sample** | 1.0882 | **+0.0908** | **89.2%** |
| sum of the three | | +0.1005 | 98.7% |
| interaction (printed, not tidied away) | | +0.0013 | 1.3% |
| **the whole layer** | 1.0992 | +0.1018 | 100% |

**Almost all of it — 89.2% — is the par sample. The bust charge is worth nothing at all.**

I predicted the opposite before the measurement. I wrote down that the bust charge would be the
largest part, over half. It is the smallest part, and its sign is negative: turning the bust charge
off makes year 1 very slightly worse. That prediction is a breach and it is reported as one. Nothing
was adjusted to rescue it.

---

## 4. Why the bust charge is worth nothing

Two reasons, both already in the code:

1. **A real player never sees it.** Amendment 3 measured that the forward band already charges the
   full risk of never establishing, and set the anchor-side charge to 0.9996 — that is, to nothing.
   So for any player with a record, the bust charge was already switched off before round 3 started.
2. **A pick does see it, but the draft-day price does not come from there.** The year-0 price the
   whole table divides by comes from the frozen year-zero surface, not from the pick reference table
   the charge scales. Measured: 1 draft-day price moves out of 1,197 in every arm, and the sum of
   draft-day prices moves by less than 0.02%.

---

## 5. What this means for the design you asked about

The design idea was: **re-time the bust charge across the career years instead of taking it all at
once.** That is an honest idea. It is also, on this measurement, an empty one.

> **The ceiling for a re-timing design is about 0.02 of the 9.1 points. There is nothing in that
> channel to re-time.**

I probed the two mechanisms that design would use, and both come back the same way.

### Mechanism (a) — the missing discount unwind

The idea: a draft-day price already discounts future football at about 14% a year. One year later,
that same football is one year nearer, so an honest year-1 price should carry one year of unwind.

**The code fact, confirmed.** The anchor a still-unproven player leans on is his draft-day price
multiplied by a retention factor. The retention factor only ever falls. There is no unwind term
anywhere in it.

| tenure | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| retention, a pick-35 non-key-position player | 1.000 | 0.619 | 0.422 | 0.399 | 0.361 | 0.339 | 0.261 |
| what an unwind at 14% would add | 1.000 | 1.140 | 1.300 | 1.482 | 1.689 | 1.925 | 2.195 |

The two run in opposite directions and only one of them is in the engine. The draft-day price itself
was also checked: it is a fixed object and does not re-price as the clock advances (60 rows tested
across three as-of years, all 60 identical).

**But this is not where the #336 drop went.** The retention factor is not part of #336 and #336 did
not change it. Adding an unwind would be a new lift on top of the old engine, not a restoration of
something #336 took. The old engine already showed +12% at year 1 with no unwind in it. So an unwind
is a separate proposal, on its own merits, and it is not a #336 repair. **It is not built.**

### Mechanism (b) — a tenure-conditional bust charge

The idea: for a player who has not established yet at year 2, use the chance that a still-unproven
year-2 player ever establishes, rather than the chance a fresh draftee does.

**Measured, on the engine's own history (1,974 players, six-game bar, same shrinkage rule #336 uses):**

| still unproven entering year | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| chance he ever establishes | 0.531 | 0.362 | 0.203 | 0.079 | 0.045 | 0.023 |

**It falls, hard.** That is arithmetic, not a modelling choice: the players who established in year 1
have left the pool, so what remains is worse each year. A design that used this number would charge
an unproven year-2 player **more** than a year-1 one. **It would deepen the year-1-to-year-2 fall,
not lift year 1.** You asked to be told this plainly whichever way it fell. This is that answer, and
it is why the mechanism is not built.

---

## 6. Where the value actually went — and the one thing that sits there

The 89.2% is the **par sample**: the developmental benchmark every projection leans on.

#336 changed which seasons teach that benchmark. It used to be "seasons of six games or more". It is
now "every season an establisher played at all, down to one game". The reason is sound and it is the
same honesty rule as the rest of the layer: an establisher who faded to three games used to vanish
from the table, so a worse career again became invisible rather than low.

**The effect is front-loaded, by construction.** Re-measured independently from the same rows:

| tenure | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| new sample level ÷ old sample level | **0.897** | 0.949 | 0.959 | 0.968 | 0.971 | 0.978 |

A 10% cut at year 1, fading to 2% by year 6. That is exactly the shape of the hole in the cohort book,
and it is why the hole sits on year 1 and washes out by year 6.

### The one candidate that sits in that channel, stated but NOT built

The par surface is a **per-game** benchmark. Today every season enters it with the same weight: a
one-game debut counts as much as a twenty-game season. Adding all the one-to-five-game seasons was the
honest half of the change; counting them as heavily as full seasons was not part of the honesty, it is
a weighting choice that came along with it.

**Weighting each season by its own exposure** — the games actually played, capped at a full load —
keeps every faded establisher in the sample and refunds no bust charge. Sized on the same rows:

| tenure | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| level, old six-plus-game sample | 57.93 | 60.06 | 63.76 | 66.98 | 69.77 | 72.42 |
| level, #336 sample as built (equal weight) | 51.99 | 56.97 | 61.17 | 64.87 | 67.77 | 70.80 |
| level, #336 sample, **exposure weighted** | **58.20** | 61.37 | 64.81 | 68.11 | 70.73 | 73.40 |

The exposure-weighted number at year 1 lands at 58.20, against 57.93 for the old survivors-only
sample. In other words: **the front-loaded cut looks like a weighting artefact, not the honesty
repair.** The honesty repair is keeping those seasons in. Counting a one-game season as a full one is
a separate decision, and it is the one carrying the year-1 hole.

**Four warnings on that number, so it is not read as more than it is:**

1. It is a **cell average, not a fit**. The real surface runs a kernel regression with isotonic
   priors, and those would carry some of the movement away. Its effect on prices is **unmeasured**.
2. Nothing is wired. No dial exists for it. No emit has been run on it.
3. It changes the benchmark at **every** tenure, not only year 1, so it is not a targeted year-1 fix
   and must not be sold as one.
4. It is a **ruling for you**, not a seat decision, because it changes what the engine treats as
   evidence.

---

## 7. What is not on the table, and why

Channels (b) and (c) **are** the honesty repair itself. The standing ruling is that softening the
de-survivored levels re-admits survivor bias — "you can't say busts are counted as busts and then
exclude them from the sample when it's convenient". Their counterfactual arms exist only to bound the
design. **They are not candidates and no version of this memo proposes turning them off.**

The exposure-weighting candidate in section 6 is deliberately different in kind: it does not remove a
single faded season from the sample, and it does not touch the bust charge. It changes how much a
one-game season counts against a twenty-game one, in a table whose unit is per-game.

---

## 8. Two honest qualifications on the measurement itself

1. **A guard in the #336 layer is already failing, before any of this.** Amendment 2 promised that an
   established player's benchmark can never sit below the general one for his own slot, and said it
   was "asserted, not assumed". It is only a computed list; nothing stops the build on it. At the
   current package it is failing in one cell — key-position defenders in the top pick band, by 0.59%.
   Reported, not repaired, because repairing it is a design change nobody has ruled on.
2. **The level-sample arm (b) is the weakest of the three rows.** Its counterfactual carries two
   failing guard cells instead of one. It is also the smallest channel at 9.7%, so the overall reading
   does not depend on it.

---

## 9. Summary

- The year-1 hole from #336 is **89.2% par sample**, **9.7% level sample**, **−0.2% bust charge**.
- **A design that re-times the bust charge has a ceiling of about 0.02 of the 9.1 points.** The
  channel is empty. Both mechanisms sketched for it were probed and neither works: the discount
  unwind is real as a code fact but is not what #336 changed, and the tenure-conditional bust charge
  would deepen the hole rather than lift it.
- The value is in the par sample, and the front-loaded shape of that cut looks like an **equal-weight
  sampling choice**, not the honesty repair. Exposure weighting is the one candidate that sits in the
  right channel without re-admitting survivor bias — **sized, not built, and yours to rule on.**

---

# PART 2 — the design, tested and measured

**Added after your word "let's look at your 336 design". The candidate from section 6 has now been
put through a kill test and then measured. It is still not shipped and no dial is on by default.**

## 10. What a par is an expectation OVER — the question underneath all of this

This is the conceptual answer, and it is worth reading before any number, because the same three
choices keep coming back under different names.

A par is a **level** — points per game. To build one you average a lot of players' seasons. But
*which* average?

| the choice | the question it answers | what it does with a one-game debut |
|---|---|---|
| **equal weight per season** — what the engine does today | *"in a typical SEASON by a player of this pedigree, what was the level?"* | counts it as much as a twenty-game year |
| **weight by games played** — the design | *"in a typical GAME played by a player of this pedigree, what was the level?"* | counts it as one game against twenty |
| **survivors only** — the old, ruled-out way | *"in a typical season THAT WENT WELL ENOUGH to reach six games, what was the level?"* | deletes it |

The third is the one you ruled out, for the right reason. The first two are both defensible. They are
different questions, and the engine should answer the one its own consumers are asking.

**And there is a mismatch today that has nothing to do with busts.** The par is used as the bottom of
a fraction: the engine measures a player by `his own average ÷ the par for his slot`. His own average
is **games-weighted** — a season where he played twenty games counts twenty times a season where he
played one. So the top of the fraction is a per-game number and the bottom is a per-season number.
They are not the same unit. That is true whichever way the rest of this memo falls.

**But a right unit does not make a biased sample honest.** So the test came first.

## 11. The kill test — is exposure weighting just survivor bias again?

The suspicion is the correct one to have: busts play few games, so weighting by games might quietly
delete them, which is the thing you already ruled out. **The rule for killing the design was written
down before the numbers were computed**, and it included a fourth comparison specifically to stop the
test being fudged.

Three ways it could have died. None of them fired.

**(A) Does it just reproduce the old survivors-only answer?** Measured on 44 (tenure × pick-band)
cells where there was anything to see: **7 look the same, 37 are clearly different.** Pooled: it
matches survivors-only at year 1, and separates from it at every year after.

**(B) Do the small seasons still count for anything?** They are 19.7% of the rows and they keep
**4.8% of the say** — 11.5% at year 1. Down-weighted about fourfold. **Not deleted.**

**(C) Do they still move the answer?** Yes — including them drags the year-1 level **3.05% below**
what it would be without them, fading to 0.54% by year 6.

**The result that settles it.** At year 1, in the **late pick bands**, the exposure-weighted par comes
out **BELOW** the old survivors-only par:

| band | 21-27 | 28-35 | 36-48 | 49-99 |
|---|---|---|---|---|
| exposure-weighted | 54.37 | 55.13 | 54.82 | 59.78 |
| old survivors-only | 54.75 | 56.75 | 56.20 | 59.91 |

In exactly the cells where late-pick bust risk lives, this benchmark is **harder** than the one you
ruled out. Survivor bias cannot produce that; deleting bad seasons can only ever flatter.

**Where the busts still carry their weight, precisely:** at year 1 (11.5% of the say, pulling the
level 3.05% down), fading to year 6 (3.1%, 0.54%); and by band, the year-1 similarity to survivors-only
is confined to the **late** bands — every early band (picks 1-3, 4-7, 8-12, 13-20) is clearly different
at year 1.

## 12. The measured result

Nothing is dropped from the sample. Only the weights change. Cap: a season's exposure counts up to a
full load of 18 games — the most conservative of the three weightings measured.

| | year 1 | year 2 | year 3 | year 4 | year 5 | growth yr0→yr1 | charged | margin |
|---|---|---|---|---|---|---|---|---|
| main (before the package) | 1.1239 | 1.3773 | 1.5098 | 1.5732 | 1.5670 | +12.39% | 14.00% | +1.61% |
| FULL (the package today) | 0.9974 | 1.2401 | 1.4276 | 1.5310 | 1.5328 | −0.26% | 14.00% | +14.26% |
| **the design** | **1.0884** | 1.3585 | 1.4941 | 1.5660 | 1.5500 | **+8.84%** | 14.00% | **+5.16%** |

- It recovers **0.0910 of the 0.1265** the package took off year 1, and leaves year 1 **3.2% below**
  where it was before the package.
- **The margin stays positive at +5.16%** — the book grows more slowly than the engine charges, so
  this does **not** open the free-money hole that V3 and V4 open.
- Mraz: **1707**, which is 3.043× his pick's value (today 1649 = 2.939×) — inside the slack you granted.
- The draft-day prices do not move: 1 of 1197, and the total moves by 0.017%.
- The monotonicity guard picks up **no new failing cells** (still the one pre-existing cell).

## 13. What I got wrong, and one thing you should not be fooled by

**A prediction I filed was breached.** I registered that year 4 would move by less than 1%. **It moved
+2.29%.** This is not a year-1 fix: weighting by exposure lifts the benchmark at *every* career year,
and at year 4 it goes past even the old survivors-only level. The evidence for that was sitting in my
own step-1 grid before I ran the price measurement and I did not read it. The number stands; my
prediction does not, and the cost is real — **this design lifts the whole book, not just its young end.**

**The thing not to be fooled by.** At year 1 the design lands **1.0884**, and simply going back to the
old survivors-only sample lands **1.0882**. Those are the same number. **The year-1 figure alone cannot
tell the two apart.** What separates them is everything else — years 2, 4 and 5 all differ — and, more
importantly, the fact proven in section 11: one of them keeps every faded season in the sample, and the
other deletes them. **Judge this design on how it is built, not on its year-1 number.** If it is ever
sold to you on the year-1 number alone, that is the same mistake in a new coat.

## 14. Where this leaves the question you asked

- The design you asked about — **re-timing the bust charge** — is still empty. Nothing changed there.
- The design that exists is a different one: **the par sample's weighting**, which is where the
  measurement says 89.2% of the year-1 hole actually is.
- It survives the honesty test on three independent criteria, and in the late pick bands it is harsher
  than the sample you ruled out.
- **It is dial-gated and OFF. Nothing ships. It moves year 4 by an amount no order asked for, and that
  is on the table beside the year-1 gain, not under it.**
