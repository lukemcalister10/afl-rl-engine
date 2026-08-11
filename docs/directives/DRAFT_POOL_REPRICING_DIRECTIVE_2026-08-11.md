# DRAFT — POOL REPRICING DIRECTIVE

**Status: DRAFT. Not issued.** The owner reads and reviews this document himself before it becomes a
directive (his ruling, 2026-08-11: *"I would like to review the directive before it is sent. The layer
between you and subagents bypassing me has meant some errors have not been noticed before the damage
is done."*). Nothing here is wired, built or scheduled. The document ends at the decision list and the
measurement ledger.

**What the owner asked for, verbatim (comment 5250574134):**

> *"Can you please prepare the directive for the pool pricing - we want pool, and the streams within
> it, pricing to be reflective of historical outcomes and the players these picks become."*

**Every number below names where it comes from**, so any figure can be challenged without asking for
its source. Two sources recur:
- **[POOL]** = `docs/evidence/pool_repricing_2026-08-11/pool_measure_out.txt` (produced for this
  document; re-runnable with `python3 pool_measure.py`).
- **[SPLIT]** = `docs/evidence/composition_2026-08-10/noarb/SPLIT_TABLES.txt` and
  `B_PROVENANCE_AND_SPLITS.md` (produced earlier, already reviewed).

**Words used here.** *Stream* = one way a player enters the league (national draft, rookie draft,
mid-season draft, and so on). *Entry price* = what the engine says a player is worth on the day he
enters, before he has played. *Delivery* = what he turned out to be worth later, divided by his entry
price. A delivery of 1.00 means the entry price was exactly right. *Cohort* = everyone who entered in
time to play their first season in the same year.

---

# §0 — THE DECISION LIST

Nine decisions. Each has options, a marked seat lean with its reason, and the measured consequence
where one exists. Four are marked **OPEN QUESTION** — the seat does not have the owner's preference on
record and has not guessed.

---

## D1 — Is the pool entry price the thing that is wrong?

**The evidence.** Delivery per unit of entry price, by year after entry, on the landed board **[POOL,
per-stream table, base SHIP]**:

| stream | n | yr1 | yr2 | yr3 | **yr4** | yr5 | yr6 |
|---|---|---|---|---|---|---|---|
| ND picks 1-64 | 1444 | 1.0665 | 1.3314 | 1.4870 | **1.5493** | 1.5218 | 1.4602 |
| **all pool combined** | 1197 | — | — | — | **0.7106** | — | — |

A national-draft pick returns about **1.55 times** its entry price by year four. The pool as a whole
returns about **0.71**. **[POOL]**

**Seat lean: YES, the entry price is where the defect sits — but only for some streams (see D2).** The
reason is D3's table: several streams never reach 1.00 at any year through year six, which is what an
entry price that is too high looks like.

**The honest counter-argument, stated because it is real.** A ratio below 1.00 can mean the entry price
was too high, *or* that the later prices are too low. These two are not distinguishable inside a ratio
— this was stated when the split tables were first produced **[SPLIT]** and it has not changed. The
seat leans to the entry price because the later prices are production-led and are checked against real
scoring, while the entry price is a prior with no such check.

---

## D2 — One repair for the whole pool, or one per stream?

**The measured spread. This is the decision's whole content.** Year-four delivery by stream, landed
board **[POOL]**:

| stream | n | **yr4 delivery** | reading |
|---|---|---|---|
| SSP | 52 | **1.3507** | returns *more* than entry |
| MSD | 106 | **0.9485** | close to right |
| PDA (academy) | 51 | 0.7709 | too high |
| UNR | 59 | 0.7672 | too high |
| RD (rookie) | 688 | 0.7379 | too high |
| ND picks >64 | 120 | 0.6924 | too high |
| IRE | 57 | **0.2810** | far too high |
| PDN | 43 | **0.2575** | far too high |
| PDS | 21 | **0.1694** | far too high |

**The streams differ by a factor of eight.** **[POOL]**

**Options, with measured consequences [POOL]:**

| | option | what happens |
|---|---|---|
| **A** | change nothing | the table above stands as it is |
| **B** | one number for the whole pool (0.711) | RD lands 1.0382, ND>64 0.9740 — but **SSP is pushed to 1.8967** and **PDS stays at 0.2382**. It fixes the average and fixes almost no individual stream. |
| **C** | one number per stream | every stream lands on 1.00 (RD 0.9998, SSP 1.0020, MSD 1.0000, IRE 0.9978, PDN 0.9972, PDS 0.9953, UNR 0.9994, PDA 0.9998, ND>64 0.9996) |

**Seat lean: C, per stream.** Option B leaves two streams further from a fair price than they are today
and moves a third the wrong way entirely. The owner's own words ask for *"pool, and the streams within
it"* to be reflective, which option B cannot deliver.

**The caution that goes with C:** it trusts every stream's own history, including streams with very few
players. See D4.

---

## D3 — Which year defines a "reflective" price? **OPEN QUESTION**

A stream's delivery is different at every year. RD reads 0.4672 at year one, 0.7379 at year four and
0.6838 at year six **[POOL]**. Picking year four rather than year six changes every number in D2.

Candidates: **the peak year** (where the stream is worth most), **year four** (where the national-draft
book peaks), **year five or six** (a fuller career), or **an average across years**.

**The seat has no ruling from the owner on this and has not chosen one.** Year four is used throughout
this document **only so the options are comparable**, and every table says so. It is not a
recommendation. This is the first thing the review should settle, because every other number depends on
it.

---

## D4 — Thin streams: trust their own history, or pull them toward the pool average? **OPEN QUESTION**

Player counts **[POOL]**: RD 688 · MSD 106 · ND>64 120 · UNR 59 · IRE 57 · SSP 52 · PDA 51 · PDN 43 ·
**PDS 21**.

PDS has twenty-one players and reads 0.1694. Taken at face value that is a very large repricing built
on a very small sample. The engine already uses a standard method for this elsewhere — pull a small
group's own number partway toward the wider average, by an amount that depends on how small it is
(described in the #336 work as `n/(n+K)` shrinkage).

Options: **(i)** use each stream's own number as measured · **(ii)** pull thin streams toward the pool
average · **(iii)** set a minimum player count and merge streams below it.

**The seat has no owner ruling on which, and marks it open.** The seat notes only that PDS ran from
2007 to 2011 and no longer takes entrants **[POOL, stream counts]**, so whatever is decided for it
affects history and not future intake.

---

## D5 — Does the repair change what today's players are worth?

**Measured, and the answer is mostly no. This is the most important number in the document for
expectations. [POOL]**

The engine already lets a player's own playing record take over from his entry price. The seat measured
how much of an entry-price change actually reaches a price, using ITEM B as a natural experiment (ITEM B
multiplied every pool entry price by a known factor and changed nothing else):

| career games | how much of an entry-price change reaches the player's price |
|---|---|
| 0 | **0.996** — essentially all of it |
| 1-9 | 0.119 — almost none |
| **10 or more** | **0.000 — none at all** |

**A player with ten games or more cannot be moved by an entry-price change.** **[POOL]**

Consequence on the live board **[POOL]**:
- 242 pool players are on the board; **only 82 can be reached at all**; their combined value is
  **11,300 points of 745,888 — 1.51% of the board.**
- Board total under option B: **745,888 → 744,661, −0.16%.**

The named players, under both options **[POOL]**:

| player | stream | career games | today | option B | option C |
|---|---|---|---|---|---|
| John Noble | MSD | 158 | 2162 | **2162** | **2162** |
| Max Hall | MSD | 44 | 2820 | **2820** | **2820** |
| James Peatling | MSD | 88 | 1100 | **1100** | **1100** |
| Mark Keane | SSP | 63 | 1514 | **1514** | **1514** |
| Tom McCarthy | MSD | 30 | 1468 | **1468** | **1468** |
| Lachlan McAndrew | SSP | 22 | 1208 | **1208** | **1208** |
| Zac Banch | MSD | 10 | 128 | **128** | **128** |
| Flynn Perez | SSP | 31 | 113 | **113** | **113** |
| Paddy Cross | SSP | 10 | 113 | **113** | **113** |
| Marcus Herbert | MSD | 8 | 1053 | 1011 | 1046 |
| Mitch Podhajski | MSD | 2 | 195 | 187 | 194 |
| Harrison Coe | MSD | 0 | 52 | **37** | **49** |

**The owner's expectation is confirmed exactly: Noble, Hall and Peatling do not move, because they are
priced on their own playing record.** **[POOL]**

**What this means, said plainly and early because it changes what the decision is about.** Repricing the
pool entry level **does not re-rate today's established pool players**. It changes what an unproven
entrant costs, and it changes the cohort tables. If the aim is to move players like Noble, this is not
the mechanism that would do it.

---

## D6 — The effect on the no-arbitrage reading

**Lowering pool entry prices RAISES the all-arm cohort ratios**, because the year-zero figure they are
divided by falls while produced players' prices do not move.

Measured **[POOL]**: all-arm year-one ratio, cohorts 2005-2023, **0.8850 → 0.9628** under option B.

For reference, the same instrument reads **0.9326 on the pre-act engine** and **1.2936 at year four**
**[SPLIT, all-arm table]**.

**Seat note, not a recommendation:** this moves the all-arm year-one figure toward 1.00, i.e. toward a
cohort that neither gains nor loses value in its first year. Whether that is the right target is the
owner's to say and is not assumed here.

---

## D7 — The draft-age question, per stream, on playing quality only

**The standing law:** value players on **how they play**, never on whether they play (owner ruling,
2026-08-11). **The cautionary example is on the record:** ITEM B's draft-age steps were fitted to a
measure that rises when a player plays *more* as well as when he plays *better*, and were retired for
that reason **[SPLIT, B_PROVENANCE_AND_SPLITS.md §3.1]**.

Playing quality by stream, measured on quality alone **[POOL]**:

| stream | quality (games-weighted average) | games played | quality at draft age ≤18 / 19-20 / 21+ |
|---|---|---|---|
| ND 1-64 | 60.83 | 77.1 | 60.73 / 61.38 / 61.98 |
| RD | 59.18 | 38.7 | 56.40 / 62.34 / 62.83 |
| ND>64 | 55.54 | 43.4 | 54.52 / 54.94 / 59.88 |
| PDA | 52.54 | 23.7 | 51.71 / 54.40 / 53.97 |
| IRE | 52.51 | 24.4 | 52.76 / 55.92 / 42.65 |
| SSP | 51.94 | 25.6 | 42.08 / 57.65 / 52.19 |
| MSD | 51.04 | 17.3 | — / 48.68 / 52.58 |
| UNR | 50.90 | 23.5 | 45.05 / 50.50 / 52.22 |
| PDN | 50.05 | 9.7 | 46.39 / 65.13 / 58.74 |
| PDS | 46.54 | 10.1 | 46.03 / 49.60 / — |

**Two things the seat reads from this, offered as readings and not as decisions:**
1. **Quality varies much less between streams than delivery does.** Quality runs 46.5 to 60.8 — a
   spread of about 30%. Delivery runs 0.17 to 1.35 — a spread of about 800% **[POOL]**. So most of the
   delivery gap is **not** explained by how well these players play when they play.
2. **Within a stream, quality by draft age is mostly flat**, and where it is not, the counts are small
   (PDN reads 65.13 at ages 19-20 on part of 43 players). This is the same pattern that retired ITEM B's
   steps.

**Seat lean: any age adjustment must be fitted to quality only, and must be fitted per stream, not
across the pool.** Whether there should be an age adjustment at all is a question the measurements do
not answer, and the seat does not assume one.

---

## D8 — The two sitter cells, translated to the entry-price side

**What exists today.** Two multipliers still apply to a pool player's *finished* price
**[SPLIT, POOL_ARM_ATTRIBUTION.md; and the landed configuration]**: all-pool-sitters **0.804** and the
named union cell **0.280**. Together they take **0.804 × 0.280 = 0.2251** off a player who sits out
**[SPLIT]**. The third cell of that family was retired to 1.0 at the landing on the owner's ruling.

**The owner's standing design direction:** a discount of this kind, if the history supports one,
belongs **in the entry price, where a body of work overcomes it** — not as a multiplier on the finished
price (owner ruling, filed 5249802288).

**The shape such a thing would take, sketched and not wired.** Instead of multiplying the finished
price, the entry price for a stream would already contain the chance that an entrant never plays. That
is the same identity the #336 work uses: *expected value = chance he establishes × value if he
establishes*. A player who then plays moves off that prior on his own record, and nothing multiplies
his finished price at all.

**OPEN QUESTION.** The seat does not have the owner's ruling on whether the sit-out charge should
survive in any form once the entry price itself is reflective of outcomes. There is a real argument
that it should not: if the entry price already contains the chance of never playing, charging a sitter
again is charging the same risk twice — which is exactly the fault the #336 work found and corrected in
a different place.

---

## D9 — Does the existing evidence machinery already do the "overcoming"?

The engine already has the machinery for a player's record to take over from his prior. D5's measured
table is that machinery working: a player at ten games or more shows **zero** carry from his entry
price **[POOL]**.

The pieces are the games ramp (`LAM_SIT`) and the anchor share (`_a_share`), both described in the
composition evidence.

**Seat lean: the existing fade is sufficient and a separate one for the entry prior is not needed** —
on the evidence that the carry is already measured at zero by ten games.

**The caution the seat attaches to its own lean:** ten games is a low bar for "proven". If a reflective
entry price is materially lower than today's, a player could climb off it very quickly, which may or
may not be wanted. The seat has no owner ruling on how fast a body of work should overcome the prior,
and marks that part **OPEN QUESTION**.

---

## §0 SUMMARY — what the review needs to settle

| | decision | seat lean |
|---|---|---|
| D1 | is the entry price the defect? | yes, for the under-delivering streams |
| D2 | one repair or per stream? | **per stream** |
| D3 | which year defines "reflective"? | **OPEN QUESTION** |
| D4 | thin streams: own history or pulled toward the average? | **OPEN QUESTION** |
| D5 | does it re-rate today's players? | measured: no, 1.51% of the board can move at all |
| D6 | the no-arbitrage effect | measured: all-arm year one 0.8850 → 0.9628 under one option |
| D7 | draft age, per stream, on quality only | quality only, per stream; whether at all is open |
| D8 | the sitter cells on the entry-price side | **OPEN QUESTION** — including whether they survive |
| D9 | is the existing evidence fade enough? | yes; how fast it should work is **OPEN QUESTION** |

---

# §1 — THE ITEMS

## ITEM 1 — the entry price level, per stream
The subject of D1, D2, D3 and D4. The measured basis is the per-stream delivery table in D2 **[POOL]**.

## ITEM 2 — the draft-age shape, per stream
The subject of D7. The measured basis is the quality table in D7 **[POOL]**. The retired ITEM B knots
stay in the code behind a switch as the worked cautionary example **[the landed configuration]**.

## ITEM 3 — the sitter cells
The subject of D8. Their present values and their combined effect are on the record **[SPLIT]**.

## ITEM 4 — how a body of work overcomes the prior
The subject of D9. The measured carry table is in D5 **[POOL]**.

## ITEM 5 — the instrument every candidate is judged on
The all-arm cohort table is the deciding lens, with the picks 1-64 table retained as the legacy view
(owner's standing ruling). A no-arbitrage margin is printed beside every candidate. Both instruments
already exist and were used for this document **[SPLIT]**.

---

# §2 — MEASUREMENT LEDGER

**Measured for this document, already done, no further machine time needed:**

| what | where |
|---|---|
| per-stream delivery curves, years 0-6, on the landed board and on the pre-act engine | [POOL] |
| the carry from entry price to player price, by career games | [POOL] |
| option B and option C sized per stream, with resulting delivery | [POOL] |
| the named players under both options | [POOL] |
| board total and all-arm year-one effect | [POOL] |
| how many live rows a level change can reach | [POOL] |
| playing quality and games played, per stream and by draft age | [POOL] |
| the two-stories finding, and the 2012-onwards window | [SPLIT] |
| the ITEM B provenance and why its steps were retired | [SPLIT] |
| the sitter cells' derivation, their intervals and their combined effect | [SPLIT] |

**Flagged to measure only after the owner rules — not run, to respect machine time:**

1. The chosen option built as a board, to confirm the modelled figures in D5 and D6 against a real
   build. The figures above use the **measured** carry curve, which is an estimate for any row and
   exact only where the carry is 0.000 or 0.996.
2. The same option read on both cohort instruments, with margins.
3. Whichever year D3 settles on, if it is not year four — every number in D2 and D5 changes with it.
4. Any shrinkage chosen in D4, applied and re-read.
5. The sit-out charge in entry-price form, if D8 says it survives.

---

# §3 — WHAT SURPRISED THE SEAT, RECORDED SO THE REVIEW SEES IT

1. **The repair's reach is very small.** Only **82 of 242** pool players on the board can be moved by an
   entry-price change at all, worth **1.51% of the board**, and the board total moves **−0.16%**
   **[POOL]**. The seat expected a larger footprint. The repair fixes the *ratio*, mostly by changing
   what the ratio is divided by.
2. **Two pool streams do not under-deliver at all.** SSP reads **1.3507** and MSD **0.9485** at year four
   **[POOL]**. "The pool is over-priced" is not true of the pool as a whole — it is true of IRE, PDN,
   PDS, RD, ND>64, and mildly of PDA and UNR.
3. **The delivery gap is not a playing-quality gap.** Quality across streams spans about 30%; delivery
   spans about 800% **[POOL]**. Whatever separates the streams, it is mostly not how well they play when
   they play.
4. **The carry from entry price to price is close to a step, not a slope**: 0.996 at zero games, 0.119 at
   one to nine, **0.000 at ten or more** **[POOL]**.

---

**Nothing in this document is wired, and nothing is scheduled. It is a draft for the owner's review.**
