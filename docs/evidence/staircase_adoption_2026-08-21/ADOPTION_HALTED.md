# THE STAIRCASE FIX ADOPTION — **HALTED BEFORE THE FLIP.** NOTHING ADOPTED.

**Seat:** adoption seat, THE STAIRCASE FIX (ORDER 44), variant B · **Date:** 2026-08-21
**Base:** `main` @ `5deda20` (the pricing seat's final commit) · **Register:** v808 **NOT** earned; the
register is the supervisor's pen and is untouched.

---

## 0 · THE ONE-LINE ACCOUNT

This seat was launched to adopt variant B. **It did not adopt it.** The measurement it was told to take
first — the no-arb reading of the arm the owner actually chose — **failed its stop condition**, so the
engine was never edited, `tools/land lever` was never run, and the live board is untouched.

| | |
|---|---|
| **Engine edited** | **NO.** `RL_O44_LVLMONO` default is still `'0'` (OFF), byte-unmoved. |
| **Flip commit** | **NONE.** |
| **Landing** | **NOT RUN.** `tools/land lever` was never invoked. Its first real landing is still ahead of it. |
| **Live board** | `68be10c79d0ee096455754e084bcf757` / **692,296** / **804** — before and after. |
| **Pins / seals / carriers** | **ALL UNMOVED.** `engine_head 3f4aa10b` · `store b745002e` · `config eed19a75` · `contract 8e6dcdbc` · `balanced 556ad70d` · `as_of_round 23`. |
| **Pushed** | **NO.** Local commit only. |

---

## 1 · WHAT THIS SEAT WAS TOLD, AND IN WHICH ORDER

The launch brief ordered: verify base → adoption prereg → flip → land → thin account. **Mid-flight the
coordinator overruled the sequence** and inserted a gate ahead of the flip, because the priced-delivery
law puts the no-arb reading and the rendered page **ahead of** the adoption:

> **(1)** emit the no-arb bands + pool arms + class mark for B RAW exactly per the pricing seat's
> machinery; **(2)** render the page; **(3)** verdicts: **if NO rail crossing and class inside the law →
> proceed with the landing as briefed** …; **if ANY rail crosses or the class mark breaches → DO NOT
> LAND**: commit the measurement evidence, report the crossing plainly, and **END** — the owner re-rules
> with the reading in front of him.

**THE RULE WAS FIXED BEFORE THIS SEAT READ A SINGLE NUMBER.** That ordering is the only reason this
account is worth anything: the stop was not chosen after seeing an inconvenient result.

**THIS SEAT'S OWN FIRST DRAFT PROPOSED TO CARRY THE GAP FORWARD AND LAND ANYWAY,** on the reasoning that
the owner's word named variant B, that the packet and no-arb legs were committed in history, and that the
pricing seat had called the raw-arm emit completable afterwards. **That reasoning was wrong and the
coordinator was right to overrule it.** A no-arb reading that exists for two arms the owner did not pick
is not a reading of the arm he did. It is recorded here rather than quietly dropped.

---

## 2 · THE GAP, AS THE PRICING SEAT HANDED IT OVER

`PACKET_STAIRCASE.md` §0 names it in its own words: *"THE NO-ARB TABLES AND THE RENDERED PAGE WERE
EMITTED FOR THE CONSERVED PAIR, NOT FOR THE RAW PAIR … the no-arb reading for B RAW is NOT MEASURED by
this seat."* It also predicted the direction: since the raw arms mint more than the conserved arms on
every band it measured, *"the expectation is that B RAW sits at or above B conserved on that cell, i.e.
the breach is more likely, not less — but that is an expectation, not a measurement, and this seat is not
passing it off as one."*

**That seat was right, and it understated the size of it.**

---

## 3 · WHAT RAN

| step | command | result | cost |
|---|---|---|---|
| the emit | `run_emit_SFX.sh` at `SFX_LABEL=SFXBRAW RL_O44_LVLMONO=smooth`, under the build lock | **exit 0**; matrix `per_entrant_SFXBRAW.json` md5 `9379fcf3`; store `b745002e`; engine `3f4aa10b` | **11m27s** |
| ND bands | `braw_noarb_bands.py` | exit 0 | ~10s |
| pool arms | `braw_noarb_tables.py` | exit 0 | ~10s |
| class mark (F4) | `braw_noarb_class.py` | exit 0 | ~10s |
| the rendered page | `braw_noarb_page.py` (`SFX_CAND=SFXBRAW`) | exit 0 — `NOARB_BRAW_SFXBRAW.html`, 73,043 bytes | ~5s |
| the input checks | `braw_noarb_checks.py` | **exit 0 — ALL CHECKS PASS** | ~10s |

**THE INSTRUMENT IS A DECLARED BYTE-CARRY, NOT A NEW TOOL.** `build_braw_instruments.py` carries the
pricing seat's five `sfx_noarb_*.py` into `braw_noarb_*.py` with **three declared changes**, each asserted
to match **exactly once** or the carry halts: (1) `SFXBRAW` added to the label/candidate lists; (2) output
basenames suffixed `_BRAW` so this set can never overwrite the pricing seat's committed artifacts;
(3) `SRC` introduced for the two inputs carried from that seat rather than regenerated
(`DAY0_SFXBASE.json`, the `EMIT_*_out.txt` logs). **That assert fired once during the build** — a
replacement matched twice in `sfx_noarb_page.py` — and the carry halted rather than silently patching the
wrong line. It is the reason the page's provenance table names the files this run actually read.

**THREE INDEPENDENT CROSS-CHECKS THAT THE INSTRUMENT IS SOUND:**

1. It reproduces the pricing seat's committed numbers **exactly** for all three shared arms
   (`SFXBASE` / `SFXACON` / `SFXBCON`) on every cell — e.g. ND PRIMARY picks 11-20 reads
   12.71 % / 13.83 % / 14.11 %, byte-for-byte the pricing seat's own figures.
2. The class instrument reproduced **ORDER K's published 1.0513 / 1.0324 at difference 0.0000** before
   its own numbers were believed.
3. The bands instrument's non-vacuity asserts fired and passed: B RAW ≠ base, B RAW ≠ B conserved.
   The arm measured is the arm labelled.

---

## 4 · THE READING — **FOUR NEW RAIL CROSSINGS, NONE REMOVED**

Every cell read **beside the live board's own cell**, which is how the pricing seat read it: a cell that
already breaches on `68be10c7` and still breaches is an **inherited** red, not a new crossing.

### 4.1 ND bands — three new crossings, all on the standing PRIMARY basis

| cell | live `68be10c7` | **B RAW** | B con | A con | verdict move |
|---|---|---|---|---|---|
| picks **1-20** | +12.98 % | **+15.18 %** | +13.93 % | +13.70 % | **fair → BUY-SIDE RED** |
| picks **1-10** | +13.12 % | **+15.08 %** | +13.84 % | +13.64 % | **fair → BUY-SIDE RED** |
| picks **11-20** | +12.71 % | **+15.38 %** | +14.11 % | +13.83 % | **fair → BUY-SIDE RED** |

### 4.2 Pool arms — one new crossing, and it fails the owner's path test

| cell | live | **B RAW** | B con | A con | verdict move |
|---|---|---|---|---|---|
| `PRIMARY` **IRE** (international rookie, n=47) | +11.71 % | **+14.18 %** | +12.94 % | +12.37 % | **fair → BUY-SIDE RED** |

> `SFXBRAW PRIMARY IRE yr0→1 +14.18 % n=47` — **FAILS** — beats carry in yr 2; still rising at yr 7.

**Both limbs of the owner's path test are required to pass and this cell passes neither.** On the live
board and on **both** conserved arms IRE does not breach at all, so this failing cell exists **only** under
the adopted arm.

### 4.3 The rest of the picture, stated not netted

* **Breaches REMOVED by the candidate: NONE.** The page computes this itself and prints
  `breaches REMOVED by the candidate: NONE`.
* **One sell-side cell improves** — `PRIMARY EX0506` picks 21-64, SELL-RED → fair — but on the
  **sensitivity** basis (2005/06 cohorts removed), not the standing one.
* **The parked SSP breach worsens**: 63.12 % → 66.45 %. Inherited (register v744 C6), never this act's to
  repair, reported rather than counted as a new crossing.
* **B RAW sits above B conserved on every cell in both tables**, without exception.
* **A conserved crosses NOTHING.** B conserved crosses **one**. **B RAW crosses four.**

### 4.4 F4 — the class mark **PASSES**

Registered W2 basis, floor 1.03, buy rail 1.14:

| | live | **B RAW** | B con | A con |
|---|---|---|---|---|
| W2 mark | 1.0738 | **1.0952** | 1.0838 | 1.0829 |
| margin to rail | −0.0662 | **−0.0448** | −0.0562 | −0.0571 |

**Inside the law.** B RAW is the closest of the four to the rail and it passes. **The class mark is not
what stopped this act — the rails are.**

### 4.5 Day-0 — the expectation **HELD**

The emitter's own fail-closed ORDER 31-F guard read **87 of 87 wired entrants on board `68be10c7`
reproducing printed day-0 EXACTLY at tolerance 0**, on the printed integer and the unrounded `derived_v0`,
under `RL_O44_LVLMONO=smooth`. The day-0 reference was **not** re-based (`DAY0_SFXBASE.json`, unmoved).

---

## 5 · WHAT THE OWNER IS OWED, PLAINLY

The owner locked in **"1.22 % and variant B"**. What was in front of him when he ruled was the packet's
movers, the law-9 mint, and a no-arb reading **of the conserved arms**. The reading of **the arm he chose**
did not exist until now. It is `NOARB_BRAW_SFXBRAW.html`.

**It says the adopted arm opens four buy-side no-arb breaches that the live board does not have, and closes
none.** Three of them are the top of the draft — picks 1-10, 11-20 and their union — which is the part of
the board the no-arb rail most directly governs.

**This seat takes no position on what the owner should now decide.** Three things are worth putting in
front of him with the page, and all three are measurements already in hand:

1. **Variant A conserved crosses no rail at all** and was the pricing seat's own standing recommendation
   (`PACKET_STAIRCASE.md` §7, left unedited after the ruling).
2. **Variant B conserved crosses one** rail (picks 11-20, +14.11 %) — but the conservation leg is the thing
   the owner explicitly rejected, and it puts Charlie West, one of the four rows the fix exists for, **below
   where he started** (−2.36 %).
3. **Variant B raw crosses four** and is the arm currently ruled.

The law-3 repair the owner wants is real and is not in question: all four named rows land where the fix
intends under B raw (Kondogiannis 359→409, Dolan 247→311, West 381→**382**, Hayes 180→250). **The cost of
getting it this way is four new no-arb breaches.** That trade is the owner's to make, and he has not yet
been asked it in those terms.

---

## 6 · FINDINGS

**F-1 · THE PRICED-DELIVERY LAW HAS A HOLE THAT THIS ACT FELL INTO, AND IT IS NOT THE PRICING SEAT'S
FAULT.** The law requires the no-arb reading and the rendered page to ride every priced delivery. The
pricing act priced **four** arms (A/B × raw/conserved) and emitted no-arb for **two** — and it said so.
Nothing in the process required the emitted set to cover **the arm the owner would go on to choose**,
because the choice came after. **The gap is structural: the no-arb obligation is discharged per-act, but
the owner chooses per-arm.** Recommendation for the supervisor: either the no-arb leg is owed on **every
priced arm**, or an adoption seat must take it on the chosen arm **before the flip** — which is exactly what
the coordinator ordered here, and it is the only reason this was caught before the board moved.

**F-2 · THE LANDER'S FIRST REAL LANDING IS STILL AHEAD OF IT — but a property of it was found while
preparing.** With process law P9 forcing the engine edit into its own commit ahead of the landing, and the
lander's `preflight` requiring a clean tree, the flip commit is already `HEAD` by the time
`steps._measure_sides` reads its source side via `git show <base>:…`. **`engine_head` therefore falls
OUTSIDE the measured transition** and the lineage entry's `moved_by_transition` cannot list it — where the
D8 adoption (hand scripts, no clean-tree preflight) folded its edit into the landing commit and **did**
record it. Two consequences, both measured by reading the code rather than by running it:
  * the flip commit **must** carry the `engine_head` restamp of all four carriers itself (the lesson of
    repair `1590a37`), or the lander halts at `lineage` with *"base-commit engine_head disagrees with that
    tree's expected_boot"*;
  * the landing must declare `engine_head` **unmoved**, which is the measured truth of the transaction and
    reads as understatement in the register unless the entry's invariants say so in words.
**This is a report, not a defect claim.** Nothing was run against the lander, so nothing about it is
proven here. The prepared spec (`ACT_SPEC_NOT_EXECUTED.json`) validates clean against
`tools/landing/spec.py` and carries the wording that handles it.

**F-3 · THE CARRY'S FAIL-CLOSED ASSERT EARNED ITS KEEP ON ITS FIRST USE** — one declared replacement
matched twice instead of once and halted the build instead of patching the wrong line.

---

## 7 · WHAT IS IN THIS DIRECTORY

| file | what it is |
|---|---|
| `PREREG_ADOPTION.md` | the adoption prereg, written before the act, with the stop rule at §4 and the reading at §4.2 |
| `ADOPTION_HALTED.md` | this file |
| `NOARB_BRAW_SFXBRAW.html` | **the rendered no-arb page for the adopted arm** — every ND band, every pool arm, both windows, each cell beside the live board's own |
| `BANDS_NOARB_BRAW*` · `STANDING_TABLES_NOARB_BRAW*` · `CLASS_BRAW*` | the three instrument passes, machine-readable and rendered |
| `NOARB_BRAW_CHECKS_out.txt` | the inputs checked rather than asserted — ALL CHECKS PASS |
| `EMIT_SFXBRAW_out.txt` · `BRAW_EMIT_out.txt` | the walk-forward emit and its driver log |
| `build_braw_instruments.py` | the declared byte-carry that produced the five instruments |
| `braw_noarb_*.py` | the five carried instruments |
| `run_braw_emit.sh` · `run_braw_noarb.sh` | the two runners |
| `ACT_SPEC_NOT_EXECUTED.json` | the landing spec that was prepared and **never run**. Kept because it shows the act stopped on the measurement, not on inability. |

**The `per_entrant_SFXBRAW.json` matrix (3.4 MB, md5 `9379fcf3`) is NOT committed**, matching the pricing
seat's own handling of its three matrices; it is reproducible from `run_braw_emit.sh`.
