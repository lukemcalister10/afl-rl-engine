# POOL REPRICING DIRECTIVE

**Status: ISSUED.** The owner read this document himself and approved it with amendments on 2026-08-11
(issue #334, comment 5250723606): *"All is okay on the directive… Other than that, it is good to go."*
His amendments are folded in below and each is marked **[OWNER AMENDMENT, 2026-08-11]**. His review was
required by his own process ruling of the same day (*"I would like to review the directive before it is
sent."*).

**Nothing here is wired, built or scheduled.** The document ends at the decision list and the
measurement ledger. Three decisions remain **OPEN** and need the owner's words before any work begins
on those specific items — they are named in the §0 summary.

**What the owner asked for, verbatim (comment 5250574134):**

> *"Can you please prepare the directive for the pool pricing - we want pool, and the streams within
> it, pricing to be reflective of historical outcomes and the players these picks become."*

**Every number below names where it comes from**, so any figure can be challenged without asking for
its source. Two sources recur:
- **[POOL]** = `docs/evidence/pool_repricing_2026-08-11/pool_measure_out.txt` (produced for this
  document; re-runnable with `python3 pool_measure.py`).
- **[SPLIT]** = `docs/evidence/composition_2026-08-10/noarb/SPLIT_TABLES.txt` and
  `B_PROVENANCE_AND_SPLITS.md` (produced earlier, already reviewed).
- **[PROFILE]** = `docs/evidence/pool_repricing_2026-08-11/profile_measure_out.txt` (the ruled-basis
  measure, added when D3 was ruled; re-runnable with `python3 profile_measure.py SHIP`).
- **[DERIVE]** = `docs/evidence/pool_repricing_2026-08-11/derive_vs_scale_out.txt` (added when the
  same-derivation principle was ruled; re-runnable with `python3 derive_vs_scale.py`).
- **[RECON]** = `docs/evidence/pool_repricing_2026-08-11/reconciliation_out.txt` (the two-layer
  reconciliation test; re-runnable with `python3 reconciliation.py`).

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

**[OWNER AMENDMENT, 2026-08-11] — answering his question on this table.** He asked: *"the ND numbers
are a little lower in year 4 than I thought. Did we manage to bring them down a touch?"* **Yes.** The
national-draft year-four figure was **1.5565** on the pre-act engine and is **1.5493** on the landed
board — down **0.5%**. The all-arm view agrees, reading **1.5237 → 1.5166** for the same arm
**[POOL, per-stream tables on both bases; SPLIT, all-arm by-arm table]**. The change came from the
landed composition, and it moved in the direction the earlier rulings intended.

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

**The measured spread. This is the decision's whole content.**

> **~~SUPERSEDED by the D3 ruling of 2026-08-11.~~** The table immediately below is the **year-four**
> reading. It is kept, not deleted, because the decision was framed on it — but the ruled basis is the
> full outcome profile in **D3**, and **the re-landed option table is in D3A below.** Year four is now
> one consulted data point.

*Year-four delivery by stream, landed board* **[POOL]**:

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
| **B** | one number for the whole pool (~~0.711~~ **superseded**) | RD lands 1.0382, ND>64 0.9740 — but **SSP is pushed to 1.8967** and **PDS stays at 0.2382**. It fixes the average and fixes almost no individual stream. |
| **C** | one number per stream (~~lands every stream on 1.00~~ **superseded — the target is ND's profile, not 1.00**) | on the year-four basis every stream landed on 1.00 (RD 0.9998, SSP 1.0020, MSD 1.0000, IRE 0.9978, PDN 0.9972, PDS 0.9953, UNR 0.9994, PDA 0.9998, ND>64 0.9996) |

**The reading that survives the basis change is the ranking, not the numbers:** the streams differ by a
large factor, one number cannot serve them all, and SSP and MSD do not under-deliver. All three hold on
the ruled basis (D3A).

**Seat lean: C, per stream.** Option B leaves two streams further from a fair price than they are today
and moves a third the wrong way entirely. The owner's own words ask for *"pool, and the streams within
it"* to be reflective, which option B cannot deliver.

**The caution that goes with C:** it trusts every stream's own history, including streams with very few
players. See D4.


### [OWNER RULING, 2026-08-11 — comment 5251055803] THE SAME-DERIVATION PRINCIPLE: **DERIVE, DO NOT SCALE**

**Owner, verbatim:**

> *"Year four would have been flattering the pool because it is the peak of value for most players. So
> if we only measured ND outcomes from year 4, it'd be flattered too. But we don't, the ND pick value
> and v0 values are derived from historical career outcomes. We should be deriving pool valuations and
> v0s the same way we do for ND picks, right? Or else it makes no sense?"*

**RULED: pool entry values, and the v0 of players entering through each pool mechanism, are DERIVED
from historical career outcomes by the same method the ND pick curve is derived by — not scaled toward
it.** The per-stream multiplier table in **D3A** does not disappear; **it changes job.** It is now the
**evidence and the sizing** — what the derivation should come out near, and how far today's prices are
from it — and **no longer the mechanism.**

#### What the ND analogue is, and what it is not — said precisely

**The ND curve is a function of an ordered slot.** Picks 1 to 64 form one ranked sequence, every draft
uses the same sequence, and the curve is a smooth function along it. **Most pool streams have no
comparable ordering.** The rookie draft has pick numbers. SSP and MSD have selection order but not a
stable, comparable slot scale across years. IRE, UNR and the academy/post-draft routes have no ordering
at all.

**So the analogue is exact in method and adapted in structure:**

| | ND pick curve | pool derivation under this ruling |
|---|---|---|
| **built from** | historical career outcomes | **the same** — identical measure, the same function (D3) |
| **the outcome measure** | `realised_full` over the whole career | **the same**, exactly |
| **structure carried** | the ordered slot (picks 1-64) | **position always**; **pick order only where a stream has one** (RD) |
| **what is fitted** | a smooth function along the slot | a level per cell the stream's samples support |
| **where it is EXACT** | — | the method, the measure, and the principle that price comes from outcomes |
| **where it is an ADAPTATION, and must be labelled one** | — | there is no universal pool slot to be smooth along, so the derivation is **per stream, per cell**, not a curve |

**This is stated plainly so nobody later claims the pool has "a curve like ND's".** It does not and
cannot, because the thing an ND curve is a function *of* does not exist for most pool streams.

#### Why the mechanism matters — a multiplier fixes the level and keeps the wrong shape

**[DERIVE]** — the rookie draft, the one pool stream whose samples support both approaches. A cell at
**1.000** returns what an ND pick returns for the same money.

| position | n | profile | vs ND | **SCALE lands at** | residual error | **DERIVE lands at** | Σ entry now | Σ entry derived |
|---|---|---|---|---|---|---|---|---|
| MID | 176 | 0.5892 | 0.575 | 1.126 | 0.126 | **1.000** | 85,670 | 49,235 |
| SD | 158 | 0.4818 | 0.470 | 0.921 | 0.079 | **1.000** | 90,527 | 42,544 |
| SF | 147 | 0.6581 | 0.642 | 1.258 | 0.258 | **1.000** | 48,990 | 31,448 |
| **KPD** | 72 | 0.2825 | 0.276 | **0.540** | **0.460** | **1.000** | 70,425 | 19,407 |
| KPF | 64 | 0.4180 | 0.408 | 0.799 | 0.201 | **1.000** | 28,974 | 11,813 |
| **RUCK** | 71 | 0.9584 | 0.935 | **1.832** | **0.832** | **1.000** | 26,458 | 24,735 |
| **RD total** | 688 | 0.5233 | 0.510 | 1.000 *by design* | — | 1.000 *per cell* | **351,045** | **179,181** |

**Under a single multiplier the whole error survives inside the stream.** Rookie-draft positions still
land between **0.540** and **1.832** against ND — **a factor of 3.4**, exactly the spread that was there
before. A multiplier moves every position by the same factor, so it cannot change any position's
standing relative to any other. Rookie-draft key-position defenders would remain priced at about half
what their outcomes support, and rookie-draft rucks at nearly double.

**AND THE COST IS THE SAME. THIS IS AN IDENTITY, NOT A COINCIDENCE:** the rookie draft's entry total
goes **351,045 → 179,181 under scale**, and **351,045 → 179,181 under derivation** — *the same number*.
It must, algebraically: scaling by the stream's own ratio and deriving each cell from its own outcomes
both land on total realised value divided by the ND profile. **So derivation is not the more expensive
option. It moves exactly the same money and simply puts it in the right places.**

### [OWNER AMENDMENT, 2026-08-11] — positional lenses where the samples permit

Owner: *"it would be good to have positional lenses where possible for pool players, but samples may
make it hard."* **His caveat is correct, and here is exactly how correct [POOL].** Cells with at least
twenty players, by stream:

| stream | n | MID | SD | SF | KPD | KPF | RUCK | usable cells |
|---|---|---|---|---|---|---|---|---|
| RD | 688 | 176 | 158 | 147 | 72 | 64 | 71 | **6 of 6** |
| ND>64 | 120 | 28 | 25 | 30 | 12 | 16 | 9 | 3 |
| MSD | 106 | 23 | 13 | 23 | 14 | 19 | 14 | 2 |
| UNR | 59 | 8 | 4 | 5 | 9 | 3 | 30 | 1 |
| IRE | 57 | 5 | 35 | 4 | 6 | 5 | 2 | 1 |
| SSP · PDA · PDN · PDS | 52 · 51 · 43 · 21 | — | — | — | — | — | — | **0** |

**Where a positional lens IS possible it matters a great deal.** Year-four delivery by position, only
where the cell holds twenty or more players **[POOL]**:

| stream | MID | SD | SF | KPD | KPF | RUCK |
|---|---|---|---|---|---|---|
| ND 1-64 | 1.5439 | 1.5032 | 1.4809 | 1.4740 | 1.7471 | 1.6388 |
| **RD** | **0.9193** | **0.5961** | **1.0529** | **0.3598** | **0.5462** | **1.3339** |
| ND>64 | 0.8802 | 0.6316 | 0.5186 | — | — | — |
| MSD | 2.0130 | — | 0.2839 | — | — | — |
| IRE | — | 0.3089 | — | — | — | — |
| UNR | — | — | — | — | — | 0.1374 |

**This changes D2's shape and the seat says so plainly.** Inside the rookie draft — the largest pool
stream by far, 688 players — delivery runs from **0.3598** for key-position defenders to **1.3339** for
rucks. **That spread is wider than the gap between several whole streams.** A single rookie-draft
number would be badly wrong at both ends.

**Seat lean, amended: per stream, and within the rookie draft also per position.** For every other pool
stream the samples do not support a positional split and the directive says so rather than forcing one.
Thin cells are shown as blanks above, disclosed, never filled in.

---

## D3 — Which outcome basis defines a "reflective" price? **RULED, 2026-08-11**

**Owner, verbatim (issue #334, comment 5250813929):**

> *"We should not be measuring only year 4 outcomes for this, though. We are looking to determine what
> the pool pick price equivalent should be, and then the v0 of players selected through the pool
> mechanism. We don't look at only year 4 for ND players. It should be one data point we consult, and
> place in context with other data points."*

**RULED: the basis is the FULL OUTCOME PROFILE across career years — the same basis the national-draft
pick curve prices from. Year four is one consulted data point in context and has no special status.**
This sits with the standing **YEAR-4-IS-NOT-A-TARGET** law, which already forbids treating a single
year as the thing being aimed at.

**The objective, restated in the owner's own frame.** Two steps, in his order:
1. **the pool pick price equivalent, per stream** — what a selection through that mechanism is worth,
   set so it returns what a national-draft pick returns for the same money; then
2. **the v0 of the players selected through that mechanism** — flowing from the stream's price exactly
   as an ND player's entry price flows from the pick curve.

### What "the same basis the ND pick curve prices from" is, read from the code

The pick curve is taught by `structural_values()` in `harness_pvc_REPINNED_pass3.py:339`. Its
per-player value is `realised_full(r)` at `:313`:

> `realised_full(r) = Σ_k e_k · vpath[k] ÷ Σ_k e_k` over **every** career year k,
> with `e_k = max(0, 1 − (pw_k − 0.11)/(1 − 0.11))`, and **0.0 for a player who never played a
> six-game season**.

**A correction the seat must make to its own order.** ORDER 12 described this as a *discounted* measure
using the engine's discount rate. **It is not.** There is no discount rate at that site at all. The
weighting `e_k` is the engine's **own evidence weight** — a career year counts in proportion to how much
real evidence it carries, so empty early years count for little and played years count fully. The
measure below therefore **calls the harness functions themselves** rather than re-implementing a
discount integral, so the directive and the pick curve cannot drift apart. **[PROFILE]**

### The measure, per stream

**[PROFILE]** — headline column is the pick curve's own method, which completes unfinished careers the
way the curve does; the years beside it are context, and **year four is one of them, nothing more**.

| stream | n | **PROFILE** | fallback rows | yr1 | yr2 | yr3 | *yr4* | yr5 | yr6 |
|---|---|---|---|---|---|---|---|---|---|
| **ND 1-64** | 1444 | **1.0252** | 35 | 1.0665 | 1.3314 | 1.4870 | *1.5493* | 1.5218 | 1.4602 |
| SSP | 52 | **1.0287** | 0 | 1.2295 | 1.3208 | 1.6006 | *1.3507* | 0.9226 | 0.4262 |
| MSD | 106 | **0.9418** | 18 | — | 0.8897 | 0.9307 | *0.9485* | 1.0886 | 1.4533 |
| ND>64 | 120 | **0.5477** | 3 | 0.3257 | 0.5161 | 0.5719 | *0.6924* | 0.6637 | 0.6380 |
| RD | 688 | **0.5233** | 2 | 0.4672 | 0.6057 | 0.6419 | *0.7379* | 0.7147 | 0.6838 |
| PDA | 51 | **0.4279** | 2 | 0.3669 | 0.4815 | 0.5987 | *0.7709* | 0.8885 | 0.4175 |
| UNR | 59 | **0.3493** | 1 | 0.3182 | 0.3920 | 0.4541 | *0.7672* | 1.0073 | 0.6208 |
| IRE | 57 | **0.2006** | 0 | 0.2385 | 0.3450 | 0.2932 | *0.2810* | 0.3301 | 0.3206 |
| PDN | 43 | **0.1422** | 0 | 0.1741 | 0.2575 | 0.2183 | *0.2575* | 0.2322 | 0.4056 |
| PDS | 21 | **0.1259** | 0 | 0.2165 | 0.1896 | 0.0653 | *0.1694* | 0.2518 | 0.2006 |
| **ALL POOL** | 1197 | **0.5218** | 26 | 0.4351 | 0.5867 | 0.6227 | *0.7106* | 0.6995 | 0.6524 |

**THE CALIBRATION TARGET IS ND'S OWN PROFILE — 1.0252 — NOT 1.00.** That figure is the measure
validating itself: the pick curve is *taught* to reproduce realised value, so the stream it is taught on
must land near one. Nothing else is required to.

**On this basis ND delivers 1.96 times what the pool delivers per unit of entry price** (1.0252 against
0.5218). **[PROFILE]**

**A caveat that changes which column to trust for young streams.** A second measure — concluded careers
only, no completion of any kind — reads MSD at **0.1215** and SSP at **0.4129** against the headline's
0.9418 and 1.0287 **[PROFILE]**. The gap is not a contradiction: MSD began in 2019 and SSP in 2018, so
only 43 of 106 MSD careers have finished, and a career that has *already* finished in a stream that
young is one that ended early — that is, one that went badly. Measuring those two streams on finished
careers alone selects their failures. The headline column completes unfinished careers by the pick
curve's own method, and its fallback count is printed above so the modelling is visible.

## D3A — THE OPTION TABLE, RE-LANDED ON THE RULED BASIS

**This replaces the option sizing in D2.** Every figure **[PROFILE]**. `λ` is the multiplier on that
stream's **entry prices**. The right-hand columns say where the stream's delivery lands **relative to
ND** — 1.0000 means it returns exactly what a national-draft pick returns for the same money.

| stream | n | profile | vs ND | **λ_B** (one number) | lands at | **λ_C** (per stream) | lands at | Σ entry now | Σ entry @C |
|---|---|---|---|---|---|---|---|---|---|
| RD | 688 | 0.5233 | 0.510 | 0.509 | 1.0030 | **0.510** | 1.0000 | 351,045 | 179,181 |
| SSP | 52 | 1.0287 | 1.003 | 0.509 | **1.9717** | **1.003** | 1.0000 | 12,286 | 12,328 |
| MSD | 106 | 0.9418 | 0.919 | 0.509 | **1.8051** | **0.919** | 1.0000 | 32,294 | 29,667 |
| IRE | 57 | 0.2006 | 0.196 | 0.509 | 0.3844 | **0.196** | 1.0000 | 22,943 | 4,488 |
| PDA | 51 | 0.4279 | 0.417 | 0.509 | 0.8202 | **0.417** | 1.0000 | 20,485 | 8,551 |
| PDN | 43 | 0.1422 | 0.139 | 0.509 | 0.2726 | **0.139** | 1.0000 | 17,425 | 2,418 |
| PDS | 21 | 0.1259 | 0.123 | 0.509 | 0.2412 | **0.123** | 1.0000 | 9,916 | 1,217 |
| UNR | 59 | 0.3493 | 0.341 | 0.509 | 0.6696 | **0.341** | 1.0000 | 12,506 | 4,261 |
| ND>64 | 120 | 0.5477 | 0.534 | 0.509 | 1.0497 | **0.534** | 1.0000 | 63,638 | 33,997 |
| **ALL POOL** | 1197 | 0.5218 | 0.509 | 0.509 | 1.0000 | per stream | — | **542,537** | **276,109** |

**Option B still fails for the same reason it failed on the old basis, and worse:** one number pushes
**SSP to 1.97** and **MSD to 1.81** — nearly doubling two streams that are already priced about right —
while leaving PDS at 0.24. **The seat's lean on D2 is unchanged: per stream.**

### What the basis change did, and it went one way

**Year four flattered the pool.** Every stream's multiplier falls when the full profile replaces year
four, because year four sits at or near the top of most streams' profiles **[PROFILE, the year columns
in D3]**:

| stream | λ on the year-four basis *(superseded)* | **λ on the ruled basis** | change |
|---|---|---|---|
| UNR | 0.767 | **0.341** | **−56%** |
| PDA | 0.771 | **0.417** | **−46%** |
| PDN | 0.258 | **0.139** | **−46%** |
| RD | 0.738 | **0.510** | **−31%** |
| IRE | 0.281 | **0.196** | **−30%** |
| PDS | 0.169 | **0.123** | **−27%** |
| SSP | 1.351 | **1.003** | **−26%** |
| ND>64 | 0.692 | **0.534** | **−23%** |
| MSD | 0.948 | **0.919** | −3% |

The pooled entry total for the pool falls from **388,329** on the old basis to **276,109** on the ruled
one — the repricing is materially deeper than year four alone implied.

**Two conclusions are basis-invariant and should be read as the robust part:** the streams differ by a
large factor, and **SSP (1.003) and MSD (0.919) are already about right and barely move.**

## D3B — RD BY POSITION, ON THE RULED BASIS

The positional lens the owner asked for (D2), restated on the ruled measure **[PROFILE]**. Cells under
twenty players are left blank with their counts, never forced.

| position | n | **profile** | vs ND | *yr4 (context)* |
|---|---|---|---|---|
| RUCK | 71 | **0.9584** | 0.935 | *1.3339* |
| SF | 147 | 0.6581 | 0.642 | *1.0529* |
| MID | 176 | 0.5892 | 0.575 | *0.9193* |
| SD | 158 | 0.4818 | 0.470 | *0.5961* |
| KPF | 64 | 0.4180 | 0.408 | *0.5462* |
| KPD | 72 | **0.2825** | 0.276 | *0.3598* |

**Inside the rookie draft the spread is 0.276 to 0.935 against ND — a factor of 3.4.** Rookie-draft
rucks are already close to fairly priced; rookie-draft key-position defenders return a bit over a
quarter of what a national-draft pick returns for the same money. A single rookie-draft number would be
wrong at both ends, and the samples support the split here and nowhere else in the pool.

## D4 — Thin streams: trust their own history, or pull them toward the pool average? **OPEN QUESTION**

Player counts **[POOL]**: RD 688 · MSD 106 · ND>64 120 · UNR 59 · IRE 57 · SSP 52 · PDA 51 · PDN 43 ·
**PDS 21**.

PDS has twenty-one players and reads 0.1694. Taken at face value that is a very large repricing built
on a very small sample. The engine already uses a standard method for this elsewhere — pull a small
group's own number partway toward the wider average, by an amount that depends on how small it is
(described in the #336 work as `n/(n+K)` shrinkage).


### [ORDER 13] CAN EACH STREAM ACTUALLY BE DERIVED? — the counts decide, and they are printed

A cell needs **at least twenty players** to be derived on its own outcome history. **[DERIVE]**

| stream | n | MID | SD | SF | KPD | KPF | RUCK | derivable cells | verdict |
|---|---|---|---|---|---|---|---|---|---|
| ND 1-64 | 1444 | 432 | 306 | 304 | 153 | 173 | 76 | 6 | *(the reference)* |
| **RD** | 688 | 176 | 158 | 147 | 72 | 64 | 71 | **6** | **per-position derivation: FULL** |
| ND>64 | 120 | 28 | 25 | 30 | 12 | 16 | 9 | 3 | per-position: PARTIAL |
| MSD | 106 | 23 | 13 | 23 | 14 | 19 | 14 | 2 | per-position: PARTIAL |
| UNR | 59 | 8 | 4 | 5 | 9 | 3 | 30 | 1 | per-position: PARTIAL |
| IRE | 57 | 5 | 35 | 4 | 6 | 5 | 2 | 1 | per-position: PARTIAL |
| SSP | 52 | 5 | 8 | 16 | 5 | 12 | 6 | **0** | stream-level derivation only |
| PDA | 51 | 14 | 10 | 14 | 2 | 6 | 5 | **0** | stream-level derivation only |
| PDN | 43 | 4 | 14 | 16 | 5 | 2 | 2 | **0** | stream-level derivation only |
| **PDS** | 21 | 7 | 5 | 3 | 4 | 1 | 1 | **0** | **stream-level only, AND THIN** |

**So the ruling is fully achievable for one pool stream and partly achievable for four.** The rookie
draft — the largest by a distance, 688 players — supports derivation in every position. Four streams
support it in some positions. Four support only a stream-level number, and **PDS at twenty-one players
supports that only weakly.**

**THE FALLBACK IS AN OPEN QUESTION AND THE SEAT DOES NOT CHOOSE IT.** For a cell too thin to derive,
the candidates are: **(i)** use the stream-level number for that cell · **(ii)** pull the cell's own
number partway toward the stream number by how thin it is (the `n/(n+K)` method the engine already uses
elsewhere) · **(iii)** borrow the shape from a stream that *is* derivable — the rookie draft — and carry
only the level from the thin stream · **(iv)** leave the thin stream unchanged until it has the sample.

**This is D4, and it is now the question that gates how much of the ruling can be delivered.** It needs
the owner's words.

Options for D4 itself: **(i)** use each stream's own number as measured · **(ii)** pull thin streams toward the pool
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

**This finding is basis-invariant, and the seat verified that rather than assuming it.** The carry is
measured from a board experiment about how much of an *entry-price* move reaches a *price*. It never
touches the outcome measure, so ruling D3 changes the multiplier λ and does not change the carry
**[PROFILE]**.

Consequence on the live board, **restated on the ruled basis** **[PROFILE]**:
- 242 pool players are on the board; **only 82 can be reached at all**; their combined value is
  **11,300 points of 745,888 — 1.51% of the board.**
- Board total: **745,888 → 743,727 under option B (−0.29%)**, **→ 744,040 under option C (−0.25%)**.
  *(On the superseded year-four basis this read −0.16%.)*

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
| Marcus Herbert | MSD | 8 | 1053 | 971 | 1042 |
| Mitch Podhajski | MSD | 2 | 195 | 180 | 193 |
| Harrison Coe | MSD | 0 | 52 | **26** | **48** |

*(Figures on the ruled basis* **[PROFILE]***. On the superseded year-four basis the three movers read
1011/1046, 187/194 and 37/49. Every unchanged player above is unchanged on both bases.)*

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

Measured on the ruled basis **[PROFILE]**: all-arm year-one ratio, cohorts 2005-2023, **0.8850 →
1.0266** under option B and **→ 1.0355** under option C. *(On the superseded year-four basis this read
0.9628.)*

**A consequence the seat flags rather than buries: on the ruled basis this pushes the all-arm year-one
figure ABOVE 1.00.** A cohort that gains value in its first year is the condition the free-money check
exists to watch, and §4's flagged year-two step is about the very next rung. Whether landing above 1.00
is acceptable is the owner's to say; the seat does not assume it.

For reference, the same instrument reads **0.9326 on the pre-act engine** and **1.2936 at year four**
**[SPLIT, all-arm table]**.

### **RULED, 2026-08-11 (comment 5251055803): year-one cohort appreciation is acceptable**

**Owner, verbatim:** *"Cohorts gaining value in its first year makes sense."*

**The arithmetic that makes it consistent, printed so the ruling can be checked rather than trusted:**

| | all-arm year-one | appreciation | charge | **margin** | verdict |
|---|---|---|---|---|---|
| today | 0.8850 | −11.50% | 14.00% | +25.50% | legal |
| option B | **1.0266** | **+2.66%** | 14.00% | **+11.34%** | **legal** |
| option C | **1.0355** | **+3.55%** | 14.00% | **+10.45%** | **legal** |

**Free money requires appreciation to EXCEED the charge.** A cohort gaining 2.7% to 3.6% in a year
while the engine charges 14% to hold it is not free money — it is a book that still grows more slowly
than the discount, by about ten to eleven points. The ruling and the no-arbitrage law agree.

**§4's year-two step is NOT covered by this ruling and stays flagged.** That step is **+24.8% against
the same 14% charge**, which is the opposite sign of margin, and it sits at a rung the free-money check
has never been computed at. It remains a separate discussion item.

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

**[OWNER AMENDMENT, 2026-08-11] — the positional caveat applies here too.** Any age work carries the
same sample limit set out in D2: a positional lens is available inside the rookie draft and nowhere
else in the pool. An age-by-position split would divide the samples again and the counts in D2 say that
is not supportable outside the rookie draft. Where a cell is too thin it is shown empty, with its count,
and is not filled in.

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

### [OWNER AMENDMENT, 2026-08-11] — THE MEAN-PRESERVING SITTER SPLIT: the FORM is now settled

**Owner, verbatim:**

> *"I note that if we are looking at sitters and then applying a penalty to reflect our data that
> sitting is bad for long term prospects, if we apply that penalty from an already well calibrated base
> (not that this is calibrated well now), there would need to be a bonus added to other players too, do
> you agree? Just like if we took our existing ND 1-64 v0 values and applied a sitter penalty, they are
> already calibrated to reflect the return of those picks, so applying a penalty just throws it out."*

**He asked whether the seat agrees. The seat agrees, and the reason is arithmetic.** Once a group's
entry price is set so the group as a whole returns 1.00, that price already contains every outcome in
the group — the players who sit out included. Taking value off the sitters after that point removes
value the group's own history already accounted for, so the group stops averaging 1.00 and the
calibration that was just done is undone. His national-draft example is the clean case: those prices
are calibrated to what those picks return, so a bare sitter penalty on top would push the whole book
below its own measured return.

**THE STANDING PRINCIPLE, as it now binds this work:** *any sitter differential applied inside a group
whose entry price is calibrated to that group's realized returns must be a **redistribution** — value
taken from sitters and given back to the rest of the group — and never a net charge.*

**Note his own parenthesis, which the seat reads as load-bearing:** *"(not that this is calibrated well
now)"*. The principle binds **after** the repricing in ITEM 1 has calibrated each stream. It is not a
statement that today's pool prices are calibrated — the measurements in D1 and D2 say plainly that they
are not.

**WHAT REMAINS OPEN.** The form is settled; **whether a sitter differential should exist at all is
not**. The seat's reading, offered and not assumed: if a stream's entry price already contains the
chance that an entrant never plays, then a further sitter charge risks charging the same risk twice —
the fault the #336 work found and corrected in a different place. The owner has not ruled on this and
the seat does not decide it.

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

**PRIORITY, from the owner's ruling of 2026-08-11: LAYER 2 (the player v0) is the load-bearing
deliverable; LAYER 1 (the pathway value) is a nice-to-have, as the pick curve is. If the sitting's time
is limited, layer 2 is what must be right.** The architecture is set out in **§0A**.

| | decision | seat lean |
|---|---|---|
| D1 | is the entry price the defect? | yes — and **RULED 2026-08-11: pool values are DERIVED from outcomes the ND way, not scaled**; the λ table is now evidence and sizing, not the mechanism |
| D2 | one repair or per stream? | **per stream** |
| D3 | which year defines "reflective"? | **OPEN QUESTION** |
| D4 | thin streams: own history or pulled toward the average? | **OPEN QUESTION** |
| D5 | does it re-rate today's players? | measured: no, 1.51% of the board can move at all |
| D6 | the no-arbitrage effect | measured: all-arm year one 0.8850 → 0.9628 under one option |
| D7 | draft age, per stream, on quality only | quality only, per stream; whether at all is open |
| D8 | the sitter cells on the entry-price side | **FORM SETTLED** by owner amendment (mean-preserving); **whether it exists at all is OPEN** |
| D9 | is the existing evidence fade enough? | yes; how fast it should work is **OPEN QUESTION** |

**STATUS AFTER THE OWNER'S REVIEW OF 2026-08-11 (comment 5250723606).**
The leans on **D1, D2, D5, D6 and D7 stand as approved** — *"All is okay on the directive… it is good
to go."* **D8's form is settled** by his mean-preserving amendment; its existence question stays open.
**D3 IS NOW RULED (2026-08-11, comment 5250813929): the full outcome profile, year four one data point
in context.** All option sizing is re-landed on that basis in **D3A**, the year-four numbers are marked
superseded in place rather than deleted, and the positional lens is restated in **D3B**.
**D1's MECHANISM and D6 are now also RULED (2026-08-11, comment 5251055803): derive rather than scale,
and year-one cohort appreciation is acceptable.**
**D4 (thin streams) and D9 (how fast a body of work overcomes the prior) REMAIN OPEN and need the
owner's words before any work begins on those specific items.** D4 has become the gating question: the
counts show derivation is fully achievable for one pool stream, partly for four, and stream-level only
for four more — so D4 decides how much of the same-derivation ruling can actually be delivered.


---

# §0A — THE TWO-LAYER ARCHITECTURE  **[OWNER RULING, 2026-08-11 — comment 5251155728]**

**Owner, verbatim:**

> *"There are two different values here. 'What is a rookie draft pick worth' - which is broad, but we
> have a number for what a national draft pick 1 is worth. Before the player is taken… We should be
> able to have an 'all inclusive' value, before positions for each of the pathways within the pool, RD,
> PSD, SSP, etc. like we do on the pick curve. Then we should have v0 ratings for players who are
> drafted/selected out of the pool. That's where the positional layer comes on, and the ruck/key
> defender lens can be applied. And like the ND, v0 may differ from the 'all-in value' of the
> selection, but across all possibilities, it doesn't. The average v0 of all pool (or pathways within
> it) players should be near identical to the all-in value. The second one is far more important for
> setting player priors etc. and ensuring these players comply with the no-arb book check and measure.
> But the first is a 'nice to have' for me, like the pick value curve is a nice to have."*

**The act produces TWO objects. The priority order is his and it is stated first, because it decides
what must be right if the sitting's time runs short.**

## LAYER 2 — THE PLAYER v0. **THE LOAD-BEARING DELIVERABLE.**
The entry value of a **specific player** selected through a pathway. **This is where the positional
layer lives** — the ruck and key-defender lens. It sets player priors and it is the thing that must
satisfy the no-arbitrage book check. **If only one layer can be got right, it is this one.**

## LAYER 1 — THE PATHWAY VALUE ("all-inclusive"). **A NICE-TO-HAVE, as the pick curve is.**
One **positionless** value per pathway — RD, SSP, MSD, the academy/post-draft legs, IRE, UNR, ND>64 —
answering *what is a selection through this pathway worth before the player is known*. It is the pool
analogue of the pick curve's value at a slot.

**A real methodological difference from the ND curve, and it is the owner's point:** the ND curve
**smooths across slots** because each slot holds only about twenty players. **The pool needs no such
smoothing** — a pathway is measured whole, and the rookie draft alone pools **688** players
**[DERIVE]**. **So layer 1 is a direct measurement, not a fitted curve, and nothing is borrowed between
pathways.**

## THE RECONCILIATION LAW, AS A CHECKABLE TEST

**The law (owner-stated, standing):** an individual v0 may differ from its pathway's all-inclusive
value, but **across all selections the entry-weighted average v0 of a pathway must equal that pathway's
all-inclusive value** — exactly as ND v0s reconcile to the pick curve.

**The test the build runs, per pathway:**

> **layer 1** `P_s = Σ_stream realised_full ÷ Σ_stream v0 ÷ ND`
> **layer 2** `λ_c = Σ_cell realised_full ÷ Σ_cell v0 ÷ ND`
> **PASS if** `Σ_c ( v0_c · λ_c ) = ( Σ_c v0_c ) · P_s` **within 1e-9 relative**

**The tolerance is 1e-9 and that is deliberate: this is an IDENTITY, not an approximation.** A
pathway's profile *is* the entry-weighted mean of its cell profiles, so layer 2 sums back to layer 1 by
construction. Anything above floating-point noise means the build has broken the construction, not that
the data disagreed. **The derive-equals-scale identity already established — the rookie draft landing
on 179,181 either way [DERIVE] — is this same law written as money.**

### THE THREE CONDITIONS. Two were known; the third the seat found by running the test.

**(a) THE WEIGHTING CONVENTION MUST MATCH ACROSS LAYERS. THE ACT ADOPTS ENTRY-WEIGHTING IN BOTH.**
A headcount average weights a 21-player cell like a 176-player one and does **not** reconcile. Measured
cost of mixing the two **[RECON]**: RD **+8.8%**, MSD **+34.5%**, IRE **+23.3%**, UNR **−22.9%**,
ND>64 **−5.2%**.

**(b) IT HOLDS ACROSS SAMPLED CELLS.** Where a positional cell is too thin to derive, those players get
no positional differentiation. See the status table below.

**(c) — FOUND BY RUNNING THE TEST, AND IT CORRECTS AN ASSUMPTION THE SEAT HAD WRITTEN DOWN.**
It was assumed that thin cells could simply *"collapse to layer 1"*, carrying the pathway value, and
would then reconcile trivially. **That is true only when NO cell is sampled. On a PARTIALLY sampled
pathway it BREAKS THE LAW** — measured **[RECON]**:

| pathway | sampled cells | **rule 1**: remainder carries the pathway value | **rule 2**: remainder priced as its own residual group |
|---|---|---|---|
| RD | 6 of 6 | PASS (0.00e+00) | PASS (0.00e+00) |
| **MSD** | 2 of 6 | **FAIL — 1.52e-01** | **PASS (0.00e+00)** |
| **IRE** | 1 of 6 | **FAIL — 1.36e-01** | **PASS (2.84e-16)** |
| **UNR** | 1 of 6 | **FAIL — 7.78e-02** | **PASS (1.63e-16)** |
| **ND>64** | 3 of 6 | **FAIL — 3.93e-02** | **PASS (0.00e+00)** |
| SSP · PDA · PDN · PDS | 0 of 6 | PASS (trivially) | PASS (trivially) |

**Why rule 1 fails:** the unsampled remainder's own outcome profile is **not** the pathway average. MSD's
remainder measures **0.6977** against a pathway value of **0.9187**; ND>64's measures **0.5926** against
**0.5342** **[RECON]**. Giving the remainder the pathway average leaves the sampled cells' deviation
unoffset, and the pathway no longer averages to its own value.

> **THE ACT MUST USE RULE 2: on a partially sampled pathway the unsampled remainder is priced as its
> own residual group, not at the pathway average.** With rule 2 every pathway reconciles at float noise.
> This is a construction requirement, not a decision — it is what makes the owner's law true in the
> built system.

## LAYER-2 STATUS PER PATHWAY — D4's decision surface, and the seat does not choose

**[RECON]** · a cell is sampled at n ≥ 20 · "covered" counts players in sampled cells

| pathway | n | MID | SD | SF | KPD | KPF | RUCK | covered | **layer-2 status** |
|---|---|---|---|---|---|---|---|---|---|
| **RD** | 688 | 176 | 158 | 147 | 72 | 64 | 71 | **688** | **DERIVABLE — all cells** |
| ND>64 | 120 | 28 | 25 | 30 | 12 | 16 | 9 | 83 | PARTIAL — 3 of 6 |
| MSD | 106 | 23 | 13 | 23 | 14 | 19 | 14 | 46 | PARTIAL — 2 of 6 |
| IRE | 57 | 5 | 35 | 4 | 6 | 5 | 2 | 35 | PARTIAL — 1 of 6 |
| UNR | 59 | 8 | 4 | 5 | 9 | 3 | 30 | 30 | PARTIAL — 1 of 6 |
| SSP | 52 | 5 | 8 | 16 | 5 | 12 | 6 | 0 | **COLLAPSES TO LAYER 1** |
| PDA | 51 | 14 | 10 | 14 | 2 | 6 | 5 | 0 | **COLLAPSES TO LAYER 1** |
| PDN | 43 | 4 | 14 | 16 | 5 | 2 | 2 | 0 | **COLLAPSES TO LAYER 1** |
| PDS | 21 | 7 | 5 | 3 | 4 | 1 | 1 | 0 | **COLLAPSES TO LAYER 1 — and thin** |

**The load-bearing layer is fully deliverable for the rookie draft — 688 of the 1,197 pool players, the
majority.** Four pathways get partial positional differentiation; four get none and receive their
pathway value. **Whether the four that get none should instead borrow a shape, be shrunk, or be left
alone is D4, and it is still open.**

## WHERE EVERY EXISTING MEASUREMENT NOW SITS

| measurement | layer | source |
|---|---|---|
| per-stream outcome profiles (RD 0.5233, SSP 1.0287, …) | **layer 1** — the pathway values themselves | [PROFILE] |
| the per-stream λ table in D3A | **layer 1** — evidence and sizing | [PROFILE] |
| the year 1-6 context columns | **layer 1** — context for the pathway value | [PROFILE] |
| per-position cells within RD (KPD 0.276 … RUCK 0.935) | **layer 2** — the player v0 differentiation | [DERIVE] |
| the derive-vs-scale comparison | **layer 2** — why the mechanism must derive | [DERIVE] |
| the positional census and feasibility counts | **layer 2** — where it can be delivered | [DERIVE] |
| the reconciliation test and its three conditions | **the join between the layers** | [RECON] |
| the carry curve (0.996 / 0.119 / 0.000) | **layer 2** — how much of a v0 change reaches a price | [POOL] |
| board totals, all-arm effects, named lines | consequences of layer 2 | [POOL] / [PROFILE] |

**Nothing measured for this directive is orphaned.**

## A SEAT FLAG FOR THE OWNER'S CONSIDERATION — not a recommendation

**Layer 1 stops being a nice-to-have and becomes load-bearing IF future pool selections are tradeable
assets in the league.** The engine already prices future **ND** picks off the pick curve; if a future
rookie-draft or mid-season-draft selection can be traded, its price would come from the pathway value
the same way, and layer 1 would then sit directly under real transactions rather than beside them.
**The owner knows his league's rules; the seat states the conditional and does not assume the answer.**

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
| positional cell counts per stream, and year-four delivery by position where n>=20 (added at the owner's amendment of 2026-08-11) | [POOL] |
| **the full outcome profile per stream, on the pick curve's own function, with the year columns beside it as context** (D3 ruling) | **[PROFILE]** |
| **the option table re-landed against ND's own profile as the calibration target** | **[PROFILE]** |
| **RD by position on the ruled basis** | **[PROFILE]** |
| **consequences restated on the ruled basis, and the carry finding verified basis-invariant** | **[PROFILE]** |
| **derive-vs-scale on the rookie draft, per position, with the residual error under scaling** | **[DERIVE]** |
| **per-stream feasibility of derivation, cell counts printed** | **[DERIVE]** |
| the two-stories finding, and the 2012-onwards window | [SPLIT] |
| the ITEM B provenance and why its steps were retired | [SPLIT] |
| the sitter cells' derivation, their intervals and their combined effect | [SPLIT] |

**Flagged to measure only after the owner rules — not run, to respect machine time:**

1. The chosen option built as a board, to confirm the modelled figures in D5 and D6 against a real
   build. The figures above use the **measured** carry curve, which is an estimate for any row and
   exact only where the carry is 0.000 or 0.996.
2. The same option read on both cohort instruments, with margins.
3. ~~Whichever year D3 settles on~~ — **DONE**: D3 was ruled and every affected number is re-landed in
   D3A, D3B, D5 and D6.
4. Any shrinkage chosen in D4, applied and re-read — **now the gating item**, because it decides which
   cells can be derived and which need a fallback.
6. The derived per-cell entry values themselves, once D4 fixes the fallback rule. This document sizes
   the derivation and proves the mechanism; it does not produce the numbers that would ship.
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
5. **YEAR FOUR WAS FLATTERING THE POOL, and by a lot.** Moving to the ruled basis lowers **every**
   stream's multiplier — UNR by 56%, PDA and PDN by 46%, the rookie draft by 31% **[PROFILE]**. Year
   four sits at or near the top of most streams' profiles, so measuring there understated how
   over-priced they are. The pooled pool entry total falls from 388,329 to **276,109**.
6. **ND's own profile is 1.0252, not 1.00 — and that is the measure checking itself.** The pick curve is
   taught to reproduce realised value, so the stream it is taught on must land near one. It also means
   **the calibration target is ND's profile, not 1.00**, which is what "the pool pick price equivalent"
   means in the owner's frame.
7. **On the ruled basis the all-arm year-one figure goes ABOVE 1.00** (0.8850 → 1.0266 / 1.0355)
   **[PROFILE]** — a cohort that gains value in its first year, which is the condition the free-money
   check watches, and the very rung before §4's flagged year-two step.
8. **DERIVING COSTS THE SAME AS SCALING — it is an identity, and the seat did not expect it to be
   exact.** The rookie draft's entry total lands on **179,181** under a single multiplier and on
   **179,181** under per-position derivation **[DERIVE]**. Both equal total realised value divided by
   the ND profile, so they cannot differ. **Derivation is not the more expensive option; it moves the
   same money and puts it in the right places** — which removes what would otherwise be the main
   argument for scaling.
9. **Scaling leaves the whole shape error untouched, and the size of what it leaves is large:** under a
   single rookie-draft multiplier the positions still land between **0.540** and **1.832** against ND
   **[DERIVE]** — the same 3.4× spread as before, just recentred.
10. **Added after the owner's amendment, and still the largest positional finding:**
   inside the rookie draft, year-four delivery runs from **0.3598** for key-position defenders to
   **1.3339** for rucks **[POOL]**. **That spread inside one stream is wider than the gap between
   several whole streams.** The owner asked for positional lenses "where possible" expecting the
   samples to be the obstacle; the samples do block it for every small stream, but they permit it
   exactly where the players are — and where it is permitted, it matters more than the stream label.


---

# §4 — FLAGGED FOR DISCUSSION, NOT A DECISION IN THIS DIRECTIVE

## THE YEAR-ONE TO YEAR-TWO STEP  **[OWNER AMENDMENT, 2026-08-11]**

**Owner, verbatim:** *"I also note the jump from year 1 to 2, which is quite steep. Flagging that for
further discussion."*

**The measured step.** On the landed cohort book, national draft picks 1-64 move **1.0884 at year one
to 1.3586 at year two — a rise of 24.8% in one year** **[SPLIT, the landed picks 1-64 table]**. The
engine charges **14%** a year for holding a future value.

**Why this is worth his flag.** The "free money" check in this project has only ever been computed at
one rung: from entry to year one. A rise of 24.8% against a 14% charge is the same shape of gap that
check exists to catch — but at the year-one-to-year-two rung, where nobody has been looking. On the
numbers above the step clears the charge by roughly ten percentage points.

**What the seat notes, and does not act on.** The margin discipline appears to belong on **every rung**,
not only the first. That is a change to how candidates are judged, not a change to pool pricing, so it
does not belong in this directive and nothing here acts on it.

**Nothing in this directive depends on the year-two step, and no work is proposed for it.** It is
recorded so the discussion the owner asked for has its numbers ready.

---

**Nothing in this directive is wired, and nothing is scheduled.** Work begins only on the owner's word,
and only on the items whose decisions are settled — D3, D4 and D9 remain open.
