# PACKET H — does a year-1/2 sit mean something different for a ruck?

**Read-only. Nothing wired.** This is rulings-material. Whether it rides the landing candidate or
follows it is the owner's call.

Your question, 2026-08-17: *"did you only look at it through a pick lens, or positionally as well?
Rucks sitting would be very different to mids sitting in year 1/2."*

Answer up front: **you were half right, and the half you were right about is bigger than I expected.
The half you were wrong about is that it is a ruck thing. It is a tall thing, and the data cannot
separate rucks from key-position players at all.**

Prereg: `PREREG_H.md`, pushed at commit `587bf76` before a single outcome number was computed.
Harness: `oh_posfade.py`. Output: `H_out.txt`, `H_RESULTS.json` (md5 `d117a5e0`, identical on two
runs).

---

## 1. The short version

Four findings.

**One. Your premise is correct, and it is the strongest number in this packet.** Rucks sit far more
than smalls. 66% of rucks played zero games in year one. For smalls it is 36%. Holding draft pick
constant, a ruck is **3.55 times** more likely to sit than a small taken at the same pick.

**Two. A sit does hurt a tall less than a small, at the same pick.** The effect is real and it
survives its confidence interval. A tall who sits carries about **0.69 less in log-odds** of washout
than a small who sits at the same pick.

**Three. It is not specifically a ruck effect.** The ruck number and the key-position number are
almost the same size (−0.65 and −0.68). And the ruck number on its own is **not resolved** — its
interval crosses zero. There are 53 rucks in sixteen draft classes. That is not enough to give rucks
their own rule.

**Four. Order D's headline number has no ruck content in it at all.** D's famous "top-10 sitters keep
0.535 of their value" was computed on 17 players in picks 1-10. **Zero of them are rucks.** Every one
of the 7 rucks taken in the top 10 across sixteen classes played in year one. There has never been a
top-10 ruck sitter in this data.

**What I recommend:** a single smooth tall/small factor on the wired curve, not a ruck rule. It is
described in §6. It has two side effects you need to see before you rule, and they are in §7.

---

## 2. What was measured, and on what

I did not build a new population or a new ruler. I took Order D's and changed nothing.

- **Who is in it.** National-draft entrants who teach the curve, draft classes 2005 to 2020, picks 1
  to 64, minus the two force-majeure players. **1,015 players.** This is D's exact population, same
  file, same filters.
- **What counts as a sit.** Zero games played in year one. This is what the wired curve already keys
  on. I also ran a second version — zero games across years one *and* two — because that is closer to
  the words you used. Both are reported.
- **What counts as a washout.** Over the five years after entry, add up `games × (average − the bar
  for his position)`, counting only the seasons where he beat the bar. If that total is zero, he
  washed out. Bars: KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9. D's ruler exactly.
- **What counts as value retention.** Delivered value from year two onward, discounted back at 1.14
  a year, divided by his day-0 entry price. Then sitters' total over players' total. D's ruler
  exactly. This is the object that produced D's 0.535 and 0.128.
- **Position groups.** RUCK on its own (53). KPP = key defender + key forward (226). SMALL = mid +
  small defender + small forward (736). Smalls are the comparison group.

**One honesty note about position labels.** The position on each record is his career label, not what
he was called on draft night. A tall forward who became a ruck is counted here as a ruck. I cannot fix
that from this store. It is a reason to hold the ruck reading loosely, and it is one more reason I am
not proposing a ruck-specific rule.

---

## 3. Your premise, checked (it holds)

Raw rates:

| group | players | sat year 1 | rate | sat years 1 **and** 2 | rate |
|---|---:|---:|---:|---:|---:|
| SMALL | 736 | 267 | **36.3%** | 131 | 17.8% |
| KPP | 226 | 106 | **46.9%** | 56 | 24.8% |
| RUCK | 53 | 35 | **66.0%** | 19 | 35.8% |

That is the raw picture, but late picks sit more than early picks, and rucks skew late. So I also ran
it holding pick constant — a logistic of "did he sit" on `ln(pick)` plus a group marker. Odds of
sitting, against a small taken at the same pick:

| group | odds of sitting vs a same-pick small | 90% interval |
|---|---:|---|
| KPP | **1.70×** | 1.28 to 2.25 |
| RUCK | **3.55×** | 2.18 to 5.91 |

Same thing for the two-year version of sitting: KPP 1.64× (1.17 to 2.22), RUCK 2.40× (1.38 to 4.11).

**Verdict on the premise: confirmed, and comfortably.** Both intervals sit well clear of 1. A ruck
sitting is an ordinary event. A small sitting is not. That is exactly what you said.

---

## 4. The interaction — does the sit *mean* less for a tall?

### 4a. A problem I had to solve before I could answer

Order D's contrast is *sitters versus players with 11 or more games in year one*. I counted that
control group by position before writing the prereg:

| group | sitters | played 1+ | **played 11+** |
|---|---:|---:|---:|
| SMALL | 267 | 469 | 188 |
| KPP | 106 | 120 | **24** |
| RUCK | 35 | 18 | **1** |

**There is exactly one ruck in sixteen draft classes who played 11+ games in his first year:
Matthew Kreuzer, pick 1, 2007.** D's contrast cannot be run inside the ruck group. It would be one
man's career.

So I preregistered the swap: the primary contrast here is **sitters versus everyone who played at
all** (1+ games). That is D's own *secondary* specification, already published in `O35_CURVE.json`.
Nothing else about D moved. D's 11+ version is also reported below, and it fails, which I explain.

### 4b. The model

```
logit P(washes out within 5 years)
  = a + b·ln(pick) + group markers
  + SAT · ( g0 + g1·ln(pick) + h_KPP·(is KPP) + h_RUCK·(is RUCK) )
```

`h_KPP` and `h_RUCK` are the answer. They are how much *less* (if negative) a sit costs a tall, in
log-odds, compared with a small at the same pick. The pick slope `g1` is shared across positions — I
preregistered that, because 53 rucks spread across 64 picks cannot support their own pick slope.

### 4c. The result

Primary reading — sat year 1, versus all who played, three groups:

| term | estimate | 90% interval | draws in your direction |
|---|---:|---|---:|
| `h_KPP` | **−0.676** | −1.275 to **−0.030** | 95.6% |
| `h_RUCK` | **−0.654** | −1.751 to **+0.796** | 77.2% |

Pooling rucks and key-position players into one TALL group:

| term | estimate | 90% interval | draws in your direction |
|---|---:|---|---:|
| `h_TALL` | **−0.692** | −1.239 to **−0.080** | 96.8% |

Read those three rows together and the story is clear.

- **The direction is yours in every reading.** All three estimates are negative.
- **The tall effect resolves.** `h_TALL`'s interval clears zero. So does `h_KPP`'s, barely.
- **The ruck effect does not resolve on its own.** `h_RUCK`'s interval runs from −1.75 to +0.80. It
  crosses zero. This is falsifier **F2** from the prereg, and it fires. At 35 ruck sitters and 18
  ruck controls, this is what the sample can do, and no amount of wanting it to be tighter changes
  that.
- **Rucks and key-position players are the same size.** −0.654 against −0.676. There is nothing in
  this data saying a ruck is different from a key forward. Pooling them costs almost nothing, and it
  buys an interval that actually resolves.

### 4d. What −0.69 means in plain numbers

Log-odds are hard to feel. Here is the same fit turned into washout probabilities, straight from the
pooled-TALL coefficients:

| pick | small who sat | small who played | **sit penalty, small** | tall who sat | tall who played | **sit penalty, tall** | difference |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 16 | 66.6% | 40.1% | **+26.5 pts** | 47.8% | 38.1% | **+9.7 pts** | 16.7 pts |
| 24 | 77.6% | 46.6% | **+31.0 pts** | 61.4% | 44.5% | **+16.9 pts** | 14.1 pts |
| 40 | 87.4% | 54.9% | **+32.5 pts** | 76.2% | 52.8% | **+23.4 pts** | 9.2 pts |
| 53 | 91.1% | 59.4% | **+31.7 pts** | 82.4% | 57.4% | **+25.1 pts** | 6.6 pts |

**Worked example, pick 24.** Take two players drafted at pick 24 who both played zero games in year
one. One is a small. One is a tall. The small's chance of never delivering anything above his
positional bar in five years is 77.6%. The tall's is 61.4%. Both are bad. The small's is much worse.

Notice the effect is **largest early and shrinks late**. At pick 16 sitting costs a tall 17 points
less than a small. At pick 53 it costs him only 7 points less. Late in the draft, everyone who sits
is in trouble regardless of height.

### 4e. The two readings that did *not* resolve, reported because I preregistered them

**D's own 11+ control.** Nothing positional resolves under it. `h_KPP` = −0.164 (interval −1.26 to
+1.46). `h_RUCK` = **+13.09**, which is not a number, it is the fit collapsing because the ruck
control group has one member. This is the degenerate result the prereg predicted and it is reported
as unusable, not as evidence against you.

**Sitting across years 1 and 2.** Every sign is still yours: `h_KPP` = −0.300, `h_RUCK` = −0.962,
`h_TALL` = −0.482. But every interval crosses zero. Halving the sitter count (408 down to 206) costs
the resolution. So falsifier **F6** passes on direction and gives nothing on size.

**Honest summary of §4:** the effect resolves in exactly one of the four specifications I
preregistered. That one is the specification with the most data in it, and the other three agree with
it in sign. That is a real finding, but it is a 90%-interval finding that only just clears zero, not
a landslide.

---

## 5. Value retention — D's 0.535 / 0.128 object, split by position

The odds of washing out are not what the fade multiplies. The fade multiplies a price. So the
deciding ruler is value retention, as D's own packet argued. Falsifier **F3** said: if value
disagrees with odds, the adjustment dies even if the odds look clean.

`F` below is: (what sitters kept, as a share of their entry price) divided by (what players kept, as
a share of theirs). `F` under 1 means sitting cost value. Higher `F` = sitting cost less.

**All picks 1-64:**

| group | sitters | players | sitters kept | players kept | **F** | 90% interval |
|---|---:|---:|---:|---:|---:|---|
| SMALL | 267 | 469 | 0.276 | 0.635 | **0.435** | 0.314 to 0.572 |
| KPP | 106 | 120 | 0.285 | 0.517 | **0.551** | 0.348 to 0.811 |
| RUCK | 35 | 18 | 0.611 | 0.768 | **0.795** | 0.375 to 1.487 |

The ordering is yours: smalls lose most, rucks lose least. But that table mixes picks, and ruck
sitters live late while ruck players live early. So here is the same thing inside one pick window at
a time.

**Picks 31-64 — where the ruck sitters actually are (32 of the 35):**

| group | sitters | players | **F** | 90% interval |
|---|---:|---:|---:|---|
| SMALL | 197 | 183 | **0.309** | 0.179 to 0.501 |
| KPP | 75 | 43 | **0.345** | 0.186 to 0.632 |
| RUCK | 32 | **5** | **0.885** | 0.397 to 2.341 |

**Picks 1-30:**

| group | sitters | players | **F** | 90% interval |
|---|---:|---:|---:|---|
| SMALL | 70 | 286 | **0.489** | 0.303 to 0.698 |
| KPP | 31 | 77 | **0.616** | 0.339 to 1.006 |
| RUCK | **3** | 13 | **0.208** | 0.001 to 0.593 |

**Falsifier F3 does not fire in the window where the data lives.** In picks 31-64 the ruck retention
is 0.885 against 0.309 for smalls, and the ruck interval's floor (0.397) sits above the small point
estimate. Value agrees with odds there.

**But look at the two cells I have bolded, because they are the whole weakness of this packet.**

The 0.885 for rucks at picks 31-64 has a denominator built on **five careers**. They are named in
`H_out.txt` §2c and here: Scott Lycett (pick 31, delivered), Zachary Clarke (37, delivered), Sean
Darcy (38, delivered), Justin Bollenhagen (51, washed), Brayden Crossley (52, washed). If Sean Darcy
had done what Justin Bollenhagen did, that ratio moves a long way.

The picks 1-30 ruck cell **reverses** — rucks look *worse* there, not better. It is **three players**:
Ayce Cordy (pick 14, washed out), Matthew Lobbe (pick 16, delivered), Brent Renouf (pick 25, washed
out). I am reporting the reversal rather than dropping the cell, because dropping cells that point
the wrong way is how a fit gets talked into a conclusion. But three players is three players, and I
do not think it should move a ruling either way.

**And the fact that matters most for how you read Order D:** in picks 1-10 there are **7 rucks and
zero of them sat.** D's headline 0.535 retention for top-10 sitters was measured on 17 players, none
of whom were rucks. So when you look at that number, you are looking at a small-and-key-position
number that was presented as a general one.

---

## 6. The proposed adjustment

Only proposed because falsifiers F1, F3, F4, F5, F6 and F7 all passed. F2 fired **for rucks alone**,
which is why this is a tall/small factor and not a ruck factor.

### The shape

The same construction Order D used, with one term added:

```
s(pick, group) = g0 + g1·ln(pick) + h_TALL·(is a tall)
kappa(pick, group) = clip( s(pick, group) / s_norm' , 0.5 , 2.0 )
```

with `g0 = −0.8778`, `g1 = +0.7100`, `h_TALL = −0.6921`, all read straight off the fit. Nothing here
is chosen.

`s_norm'` is re-solved by the same bisection D used, so **the same promise D made still holds**: the
average, across the fitted sitters, of `D2^kappa` still equals the ruled depth-2 fade
0.5582775 exactly. Residual is −1.1e−16. **This redistributes the fade between talls and smalls. It
does not change the total fade the board charges.** `s_norm'` comes out at **1.428405** against D's
1.747207.

**It is smooth.** It is one constant added inside a logarithmic curve. There is no band, no
threshold, no cliff. A tall at pick 30 and a tall at pick 31 differ by the same tiny amount that any
two neighbouring picks differ by. That was falsifier F7 and it is respected.

### The size

`m_TALL = 0.677` — a tall's kappa averages 68% of a small's kappa across picks 1-64. That is the
multiplicative form you asked for. The additive-in-log-odds form above is what the fit produces and is
the one I recommend; `0.677` is the translation.

### The curve

Depth-2 price multiplier (`D2^kappa`), which is what actually multiplies the entry price:

| pick | small | tall | D's wired pooled value |
|---:|---:|---:|---:|
| 1 | 0.7472 | 0.7472 | 0.7472 |
| 10 | 0.7342 | 0.7472 | 0.6761 |
| 16 | 0.6408 | 0.7472 | 0.6297 |
| 24 | 0.5697 | 0.7472 | 0.5922 |
| 30 | 0.5341 | 0.7084 | 0.5726 |
| 40 | 0.4914 | 0.6517 | 0.5482 |
| 53 | 0.4529 | 0.6007 | 0.5253 |
| 64 | 0.4288 | 0.5687 | 0.5106 |

---

## 7. Two side effects you must see before you rule

**Side effect one: D's clip floor swallows the whole top third of the draft for talls.**

D's kappa is clipped to a minimum of 0.5. Shifting talls down by 0.69 pushes them onto that floor
for **picks 1 through 24 — 24 of the 64 picks.** Look at the table above: a tall sitter at pick 1,
pick 10, pick 16 and pick 24 all get the identical multiplier, 0.7472. Over that range the **clip**
is setting the price, not the fit. That is a flat spot, and a flat spot that ends abruptly at pick 25
is closer to the cliff you have ruled against than I am comfortable with. (Smalls hit the same floor,
but only over picks 1-9.)

If you want this adjustment, I think the clip needs revisiting alongside it. I am not proposing a
clip change here — that is D's constant and outside this seat's brief — but I am telling you it binds.

**Side effect two: the talls' relief is paid for by the smalls.**

Because the total fade is pinned, giving talls a gentler fade forces a steeper one on smalls. Not
"leaves them alone" — steeper:

| pick | small under D (wired) | small under this proposal | change |
|---:|---:|---:|---|
| 10 | 0.6761 | 0.7342 | gentler |
| 30 | 0.5726 | 0.5341 | steeper |
| 64 | 0.5106 | 0.4288 | **notably steeper** |

A small sitter at pick 64 loses about 16% more of his price than the wired curve charges him today.
That is the arithmetic of a redistribution and it is not a bug, but somebody's price goes down for
every price that goes up, and it is the late small sitters who pay.

---

## 8. The named rows

What the proposal does to the depth-2 fade multiplier on the rows you named:

| player | position | pick | class | year-1 games | D wired | this proposal | change |
|---|---|---:|---:|---:|---:|---:|---:|
| **Will Green** | RUCK | 16 | 2023 | 0 (and 0 through year 2) | 0.6297 | **0.7472** | **+18.7%** |
| **Toby Conway** | RUCK | 24 | 2021 | 0 (1 game through year 2) | 0.5922 | **0.7472** | **+26.2%** |
| **Alex Dodson** | RUCK | 53 | 2024 | **1** | 0.5253 | **0.6007** | **+14.3%** |
| **Steely Green** | SF (small) | 55 | 2022 | 0 (6 through year 2) | 0.5224 | **0.4480** | **−14.2%** |
| Ned Moyle | RUCK | — | 2021 | 0 | — | — | pool route (MSD) |
| Nick Madden | RUCK | — | 2022 | 0 | — | — | pool route (PDA) |

Three things to notice.

**Alex Dodson is not a sitter under the year-1 rule.** He played one game. The wired curve's sitter
test is zero games, so it does not fire on him at all. He appears above only because a tall
adjustment would still touch his row through the position term. If you want the one-game case handled
as sitting, that is a separate ruling about where the sitter line sits, and Order 30A-2 already
measured that first game as worth +0.39 in D.

**Ned Moyle and Nick Madden cannot be priced by this at all.** They came through pool routes at pick
65. A curve keyed on picks 1-64 does not reach them. Any tall relief for pool rucks would have to be
built separately, and this seat did not build it.

**The two Greens are your comparison, and they are almost perfect for it.** Will Green and Steely
Green both played zero games in their first year. Will Green is a ruck taken at 16. Steely Green is a
small forward taken at 55. The wired curve today charges them 0.6297 and 0.5224 — it separates them
only by pick, because pick is all it knows. Under this proposal they go to 0.7472 and 0.4480. The gap
between them roughly doubles.

**The same-pick version of your question**, which is the cleanest way to see it:

| pick | small who sat | tall who sat | what D charges both today |
|---:|---:|---:|---:|
| 16 | 0.6408 | **0.7472** | 0.6297 |
| 24 | 0.5697 | **0.7472** | 0.5922 |
| 53 | 0.4529 | **0.6007** | 0.5253 |

The small sitters sitting at those picks in the live classes are real players, not hypotheticals —
Oskar Taylor (SD, pick 15), James Leake (SD, 17), Tom Brown (SD, 17), Harley Barker (MID, 24),
Charlie Clarke (SF, 24), Harry DeMattia (MID, 25). The full list is in `H_out.txt` §4.

---

## 9. The prereg, scored

| # | falsifier | fired? |
|---|---|---|
| F1 | `h_RUCK ≥ 0` — wrong direction | no. −0.654 |
| F2 | `h_RUCK` interval contains 0 | **YES.** −1.751 to +0.796. This is why there is no ruck-specific rule |
| F3 | value retention contradicts the odds | no, not in picks 31-64 where the ruck data lives. It does contradict in picks 1-30, on 3 players |
| F4 | base-rate premise fails | no. 3.55× for rucks, 1.70× for KPP, both clear of 1 |
| F5 | three-group and pooled disagree in sign | no. Both negative |
| F6 | one-year and two-year sitting disagree in sign | no. All signs negative. But the two-year version resolves nothing |
| F7 | the adjustment needs a cliff | no cliff proposed. But D's existing 0.5 clip creates a flat spot over picks 1-24, §7 |

**One amendment I owe you.** The prereg's §7 said the adjustment is proposed only if F1 through F7
all pass. F2 fired. I am still bringing you a proposal, but a **different** one from the one the
prereg contemplated — a single tall/small factor rather than the three-group version, because the
tall term is the one that resolved. The three-group arithmetic is published anyway in
`H_RESULTS.json` under `adjustment_arithmetic`, so you can see what I did not recommend.

---

## 10. What I would say if you asked me straight

You were right that rucks sit more, and it is not close — 3.55 times more at the same pick.

You were right that a sit means less when a tall does it. That effect is real, it is worth about 14
to 17 percentage points of washout risk at picks 16 to 24, and it barely clears its confidence
interval.

You were wrong that it is a ruck thing specifically. Key forwards and key defenders show the same
size effect, and the ruck-only number cannot be told apart from zero at 53 players.

Order D's pick curve is not *wrong* being position-blind, but it is charging a 46% sitting rate group
and a 66% sitting rate group the same penalty as a 36% group, and its most-quoted number — the 0.535
for top-10 sitters — happens to contain no rucks at all.

If you want one line: **the curve should know about talls, not about rucks, and D's clip floor needs
looking at before any tall factor goes near it.**
