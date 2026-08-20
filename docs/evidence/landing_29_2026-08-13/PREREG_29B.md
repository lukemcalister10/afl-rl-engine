# PREREGISTRATION — ORDER 29B, THE ENTRY WIRING

**Filed 2026-08-13, branch `land/order-29`, entry tip `53e7c92`, board `86c8d5d9ba5b95e2cba05c78fbc31f78`.
COMMITTED BEFORE ANY WIRING IS WRITTEN AND NEVER EDITED.** Everything below is computable in advance
from the landed artifact plus the landed board; nothing here is a hope, and every number is derived and
stated so that a breach is a NUMBER and not an opinion.

> **THE ACT IN ONE SENTENCE.** ORDER 29 landed the day-0 OBJECTS (the ruled curve, the six positional
> ND v0 curves, the pool pathway×position v0 cells, the numéraire) and **nothing consumes them**;
> ORDER 29B makes the **printed day-0 price** equal **derived v0 × numéraire**, exactly and only.

---

## 0. THE DEFINITIONS THIS PREREG IS SCORED AGAINST

Stated first, because three of the predictions below are only falsifiable once these are pinned.

### 0.1 THE ENTRANT POPULATION — P12's, NOT A NEW ONE

`o29_day0.py:36-37` defines a **fresh entrant** as a board `active` row with `cg == 0`, `ty == 'ND'`
and `1 <= pk <= 64`. That is **46 rows** and it is the population the P12 identity is scored on.
It is used here unchanged.

The **wiring** population is wider by construction, because a pool entrant is an entrant too and the
brief names his object explicitly (his pathway×position cell). Measured on the landed board, the
`cg == 0` rows split **46 ND-in-curve + 43 pool** = **89**. Every one of the 43 resolves to a signed
pathway (`MSD`, `RD`, `IRE`, `PDA`, `PDN`, `UNR`, and `ND>64` for national selections past pick 64);
there is no third class. The 89 are enumerated row by row in §5 and §6.

### 0.2 "DERIVED v0 × NUMÉRAIRE" — WHICH OBJECT, IN WHICH CURRENCY

Both landed day-0 objects are published **already anchored**: `nd_v0.posv[g][p] = relat_g(p) × curve(p)`
where `curve` is **the shipped tiebroken ladder** (which is raw × `s`), and `pool_v0.cells` are the raw
Way-A cells **× `anchor_factor` = `s` = 0.9400914291048137**. So the numéraire `s` is **inside both
objects already**, and applying it again would be the double-count the E6 design exists to prevent.

The engine prices in **engine-value currency** and the board prints **board currency**, related by the
certified board factor `_PL_F = _F = 1.0524` (`pick_redenomination.json`). ORDER 28's own canonical
derived-v0 function states the same conversion (`o28_derive.py:266-271`):

```
dv0(ND 1..64) = allin[pick] * NUM        NUM = pick_redenomination factor = 1.0524
dv0(pool)     = cell * af   * NUM        af  = anchor_factor = s
```

so the identity this act delivers, written end to end, is

```
   derived v0 (board currency, s already inside)  ×  _PL_F   =  ev(p, Y)          [engine currency]
   printed    = int(round(ev / _F))                          =  round(derived v0) [board currency]
```

**PREDICTION 0.2a:** the wiring returns the day-0 price **unrounded** in engine currency, so the print's
own `int(round(x/_F))` is the **only** rounding in the chain and the identity is **EXACT**, not
tolerance-bounded: `printed == int(round(derived v0 board))` for every wired row.
**Tolerance: 0. Any row off by even 1 is a breach of this line and is reported as one.**
*(This is not free: pre-rounding inside `ev()` would put a second `round()` in the chain and was
measured to break the identity on **18 of the 89** rows. That is why the branch returns a float.)*

### 0.3 THE IDENTITY INSTRUMENT — AND THE ONE PLACE THIS SEAT RE-POINTS P12's HARNESS, DECLARED

`o29_day0.py` compares the printed day-0 to **`curve[pick]`** — the **position-blind all-in** ladder.
That is what P12 could compare against when it was written, because the positional object was published
in the same act and **nothing consumed it**.

The brief orders the **positional** object consumed: *"ND entrants: positional ND v0 at their pick. Pool
entrants: their pathway×position cell."* Those two statements cannot both be satisfied by one number:
`posv_g(p) = relat_g(p) × curve(p)` and `relat_g(p) ≠ 1` at essentially every (position, pick) — the
reconciliation `Σ_g share_g(p)·posv_g(p) = curve(p)` is a **population** identity, not a per-row one.

**This seat resolves the fork in the open, before measuring, and does not get to change its mind after:**

* the **population** is P12's, unchanged (§0.1);
* the **value** is the row's OWN derived v0 — positional for ND, cell for pool — because that is the
  object the act is ordered to make consumed, and because wiring `curve[pick]` would leave `nd_v0`
  exactly as unconsumed as it is today;
* the identity instrument is therefore `o29b_day0.py`, which is `o29_day0.py`'s population and structure
  with the comparand moved from `curve[pick]` to the row's own derived v0. **The legacy position-blind
  reading is NOT dropped — it is printed alongside in the same run**, so the re-point is visible as a
  number rather than as a sentence.

---

## 1. THE PRINTED-DAY-0 IDENTITY

**P29B-1.** On the P12 population (46 rows), the identity `printed == derived v0 × numéraire` moves
**0 / 46 → 46 / 46**, exact (tolerance 0, per P29B-0.2a).

**P29B-2.** On the full wired population (89 rows: 46 ND + 43 pool) the identity holds **89 / 89**,
exact. `kalani-white` is among them, through the borrowed `PDN|KPF` cell (§4).

**P29B-3 — THE HONEST COUNTERPART.** Under the **legacy position-blind** reading (`printed` vs
`curve[pick]`), the same 46 rows read **0 / 46 both before and after**. This is predicted as a
**non-move**, not as a success: the positional relativities are ≠ 1 everywhere, so an act that wires the
positional object cannot also collapse to the all-in ladder. Any other outcome here is a surprise and
is reported as one.

**P29B-4.** The pre-wiring ratio statistics P12 measured (`printed/ladder` min 0.3166 · max 0.9037 ·
mean 0.5274 over 46) are **re-measured unchanged on the entry board** as a control that the instrument
is reading the same object it read in ORDER 29.

---

## 2. THE MOVER SET

**P29B-5 — THE `v` MOVER SET IS EXACTLY THE ENTRANT POPULATION.** Exactly **89** of the 804 active rows
move on the printed present value `v`, and they are exactly the 89 rows of §0.1. **Predicted coupled
movers on `v`: ZERO.** The classes, and why the list is closed:

| class | n | why it moves / does not |
|---|---:|---|
| ND in-curve entrants, `cg == 0` | 46 | wired: `posv[gfut][pick]` |
| pool entrants, `cg == 0` (MSD·RD·IRE·PDA·PDN·UNR·ND>64) | 43 | wired: `cells[pathway\|position]` |
| **any row with `cg > 0`** | 715 | **UNMOVED** — the legacy legs, the fade paths and the year-1+ machinery are out of scope and untouched |
| ND national **non-entrant** rows (`cg > 0`) | — | **UNMOVED**, asserted explicitly (brief clause) |
| pool rows with `cg > 0` | — | **UNMOVED** — they price from the #326 signed `pool_levels`, which this act does not touch |

**P29B-6 — THE ENTRANT-COUPLED OBJECTS, ENUMERATED IN ADVANCE.** Exactly two objects are touched that a
non-entrant could in principle read, and both are predicted **inert** on `v`:

1. **`pool_v0.cells`** gains two signed values (`PDN|KPF`, `PDS|KPF`). Before this act **no pricing leg
   read `pool_v0` at all**; after it, the ONLY reader is the day-0 print. So the borrowed cells can
   reach **only** rows that stand in them: `kalani-white` (active), plus `conrad-williams` (inactive
   `back` list) and `scott-reed` (neither list). **Predicted active rows affected by the borrow: 1.**
2. **the day-0 branch in `ev()`**. It returns before the legacy chain, so it cannot perturb it.
   `entry_anchor`, `v0_start`, `pool_level`, `_cap_basis`, `_b_factor`, the floor schedule, `sitout_ev`,
   ITEM A/B/C/E2/H and the staleness family are **read-unchanged and called unchanged** for every row
   that is not a day-0 entrant.

**If a coupled mover appears on `v` that is not one of these two, this seat STOPS at that step and
reports rather than explaining it afterwards.**

**P29B-7 — ROWS WITH EVIDENCE, AND THE AS-OF LENSES.** The day-0 print is a property of a player *at an
as-of year*, so the branch keys on **games as of `Y`**, not on career total. Consequences, predicted:

* `v` (Y=2026) and `vP1`/`vP2` (2027/2028, no further scoring data exists): **the same 89 rows, no others.**
* `vM1` (Y=2025): additional movers **≤ 89** — rows that have a career now but had **zero games as of
  2025**. Their **present** price does not move.
* `vM2` (Y=2024): additional movers **≤ 183**, same reason.
* These are the ONLY rows with evidence that move, and they move **only** on a lens whose price path
  literally passes through a day-0 print. **`v` stays byte-identical for all 715 of them.**

**P29B-8 — THE BOARD TOTAL.** `706,018 → 717,527` (**+11,509, +1.6301%**), of which ND **+8,495** and
pool **+3,014**. This is a **row-by-row prediction summed**, not a band. **Bound: ±5** on the total to
admit float/rounding edge cases; anything outside ±5 is a breach and is reported by number.
**Predicted sign: UP** — the wiring removes the sit-out retention discount, the `_h_cut` and the floor
from the day-0 print, which is exactly the ~47%-of-anchor gap P12 sized.

**P29B-9 — THE NAMED ROWS ARE UNMOVED.** All ten of ORDER 29's P14 named rows (`ramm · kentfield ·
liddy · hansen · visentini · martin · herbert · newcombe · duursma · sheezel`) have careers and are
predicted **0 delta** on `v`. **`kalani-white` is the eleventh named row of this act and moves 84 → 92.**

---

## 3. WHERE THE WIRING GOES — THE SITE SET, DECLARED BEFORE IT IS CUT

**P29B-10.** There is exactly **ONE** site at which a player price becomes a printed number:
`_merged_recover.py`'s outermost `ev(p, Y)` — the floor-wrapping definition. Every printed player price
in the system is `ev(p, Y)` at some `Y`:

| consumer | call |
|---|---|
| board `v` / `vM1` / `vM2` / `vP1` / `vP2` | `rl_export.py:191-193,197` — `int(round(ev(p, 20XX)/_F))` |
| the numéraire parity re-check | `rl_export.py:617` — `int(round(ev(p,2026)/_F))` |
| the 24-year as-of matrix (the no-arb basis) | `emit_matrix_338.py:193` — `ev(p, Y)` under truncated scoring |
| the cohort book / `back_extra` rows | the same `ev` |

**The set is complete because the wrapper is the function itself**, not a call site: nothing can print a
player price without going through it. The pick side (`PVC`), the sealed entrant layer (occupancy ×
ladder) and the display bands are **not player prices** and are deliberately **not** in the set — the
LEG F5 #306 reconciliation reads `draft_occupancy × _lf_pvc`, so **P29B-11: the book does NOT need
re-sealing and the L7 reconciliation does NOT fire.**

**P29B-12.** The day-0 branch is guarded by the same population predicate the year-zero floor already
uses — real store rows only, never retired/delisted, never gate synthetics, pool **or** national-draft
non-pickless, and `Y >= draft year` — so a delisted or retired zero-game row keeps its existing
treatment byte-for-byte.

---

## 4. THE BORROWED CELLS — OWNER OPTION A, DERIVED AND STATED AS NUMBERS

Owner ruling (#334 comment 5280881134) Option A: the two n=0 cells take the **K-shrink limiting case**,
i.e. **100% borrow** — the pathway level × the pool-wide positional relativity of KPF.

The derivation is `o28_derive.py:250-256`, verbatim:
`cells[(m,g)] = w·own + (1−w)·path[m].shrunk · lens[g]`, `w = n/(n+K)`, `K = 15`.
At **n = 0** ⇒ **w = 0** ⇒ `cell = path[m].shrunk × lens[KPF]` — the limiting case IS the ruling.

| quantity | value |
|---|---|
| pool-wide KPF positional relativity `lens[KPF]` | **0.8318314538303737** |
| PDN pathway level (anchored) | 111.03059757763138 |
| PDS pathway level (anchored) | 100.95452630298730 |
| **`PDN\|KPF` borrowed, anchored board points** | **92.35874340265629** → prints **92** |
| **`PDS\|KPF` borrowed, anchored board points** | **83.97715038537063** → prints **84** |

**P29B-13.** These reproduce ORDER 29's published `declined_unsigned` **92.4 / 84.0 exactly** to their
own 1-dp precision — which is the proof that Option A is the same arithmetic the derivation already ran
and declined, now **signed** rather than back-filled. Predicted match: **exact**.

**P29B-14.** Each borrowed cell carries a **disclosed flag on the cell** in the artifact (a `borrowed`
provenance field naming the ruling, the basis, `n=0`, the pathway level and the relativity) — never a
silent number. `unsigned_cells` becomes `[]`.

**P29B-15 — THE GUARD IS REPLACED, NOT REMOVED.** The unsigned-cell **halt** retires for cells signed
this way. In its place: a build-time assert that **every** pathway×position cell an **active entrant**
maps to carries a signed value (borrowed or fitted). `pool_v0_of()` stays the single accessor and still
raises on a null, so a future unsigned cell is still fail-closed. **Predicted: the coverage assert
passes over all 43 active pool entrants, and `kalani-white` now maps to a SIGNED cell.**

---

## 5. THE 46 ND ENTRANTS — EVERY EXPECTED NEW PRINT, TABLED IN ADVANCE

`predicted new print = int(round(nd_v0.posv[position][pick]))`. `all-in curve[pick]` is printed as the
P29B-3 disclosure column, **not** as the comparand.

| # | row | pos | pick | old print | **derived ND v0 (posv)** | **predicted new print** | Δ | all-in curve[pick] |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | `josh-smillie` | MID | 7 | 818 | 1616.974 | **1617** | +799 | 1321 |
| 2 | `oskar-taylor` | SD | 15 | 501 | 945.957 | **946** | +445 | 815 |
| 3 | `lachlan-carmichael` | SD | 21 | 472 | 761.109 | **761** | +289 | 809 |
| 4 | `mitchell-marsh` | KPF | 22 | 443 | 698.479 | **698** | +255 | 782 |
| 5 | `harley-barker` | MID | 24 | 596 | 885.607 | **886** | +290 | 696 |
| 6 | `adam-sweid` | SF | 25 | 350 | 305.972 | **306** | -44 | 671 |
| 7 | `harry-demattia` | MID | 25 | 379 | 891.822 | **892** | +513 | 671 |
| 8 | `blake-thredgold` | KPD | 26 | 332 | 426.394 | **426** | +94 | 657 |
| 9 | `ned-bowman` | SF | 26 | 229 | 292.886 | **293** | +64 | 657 |
| 10 | `brayden-george` | SF | 26 | 208 | 292.886 | **293** | +85 | 657 |
| 11 | `avery-thomas` | SD | 28 | 358 | 391.898 | **392** | +34 | 637 |
| 12 | `sam-allen` | MID | 29 | 563 | 839.585 | **840** | +277 | 623 |
| 13 | `thomas-matthews` | SF | 30 | 310 | 331.065 | **331** | +21 | 607 |
| 14 | `tyan-prindable` | MID | 32 | 503 | 692.373 | **692** | +189 | 573 |
| 15 | `james-barrat` | KPD | 32 | 208 | 409.783 | **410** | +202 | 573 |
| 16 | `hunter-holmes` | MID | 33 | 485 | 660.502 | **661** | +176 | 560 |
| 17 | `charlie-nicholls` | KPF | 34 | 189 | 447.759 | **448** | +259 | 549 |
| 18 | `jevan-phillipou` | SF | 35 | 263 | 361.438 | **361** | +98 | 539 |
| 19 | `kayle-gerreyn` | KPF | 37 | 170 | 386.262 | **386** | +216 | 520 |
| 20 | `koby-evans` | SF | 38 | 244 | 368.955 | **369** | +125 | 509 |
| 21 | `tylah-williams` | SF | 39 | 237 | 371.770 | **372** | +135 | 495 |
| 22 | `tobyn-murray` | SF | 40 | 219 | 350.691 | **351** | +132 | 479 |
| 23 | `ollie-murphy` | KPD | 41 | 154 | 359.493 | **359** | +205 | 460 |
| 24 | `luke-lloyd` | KPD | 42 | 146 | 361.536 | **362** | +216 | 437 |
| 25 | `max-knobel` | RUCK | 42 | 365 | 833.837 | **834** | +469 | 437 |
| 26 | `ben-camporeale` | MID | 43 | 217 | 616.272 | **616** | +399 | 413 |
| 27 | `tai-hayes` | SF | 44 | 167 | 265.339 | **265** | +98 | 387 |
| 28 | `koby-coulson` | MID | 46 | 259 | 494.180 | **494** | +235 | 338 |
| 29 | `joel-cochran` | KPD | 47 | 130 | 392.382 | **392** | +262 | 317 |
| 30 | `hugo-mikunda` | SF | 48 | 143 | 261.859 | **262** | +119 | 300 |
| 31 | `max-king-syd` | SF | 49 | 124 | 270.505 | **271** | +147 | 285 |
| 32 | `cooper-bell` | KPD | 49 | 121 | 408.516 | **409** | +288 | 285 |
| 33 | `finnegan-davis` | SD | 51 | 132 | 89.028 | **89** | -43 | 265 |
| 34 | `kye-fincher` | MID | 52 | 194 | 306.957 | **307** | +113 | 257 |
| 35 | `jacob-molier` | RUCK | 52 | 219 | 250.701 | **251** | +32 | 257 |
| 36 | `patrick-snell` | KPD | 53 | 90 | 421.001 | **421** | +331 | 250 |
| 37 | `zac-mccarthy` | KPF | 55 | 117 | 190.372 | **190** | +73 | 235 |
| 38 | `riak-andrew` | KPD | 55 | 108 | 414.573 | **415** | +307 | 235 |
| 39 | `matthew-leray` | MID | 56 | 170 | 235.337 | **235** | +65 | 226 |
| 40 | `luke-urquhart` | MID | 57 | 109 | 216.808 | **217** | +108 | 215 |
| 41 | `will-darcy` | KPD | 58 | 145 | 398.199 | **398** | +253 | 205 |
| 42 | `tyler-welsh` | KPF | 59 | 62 | 191.606 | **192** | +130 | 195 |
| 43 | `patrick-said` | SF | 60 | 63 | 148.236 | **148** | +85 | 188 |
| 44 | `jaren-carr` | SF | 63 | 60 | 70.135 | **70** | +10 | 182 |
| 45 | `cody-anderson` | SF | 64 | 60 | 17.992 | **18** | -42 | 179 |
| 46 | `reece-torrent` | MID | 64 | 76 | 56.657 | **57** | -19 | 179 |
| | **46 rows** | | | **11508** | | **20003** | **+8495** | |

**P29B-16 — THE FOUR FALLERS ARE PREDICTED, NOT DISCOVERED.** `adam-sweid` (−44), `finnegan-davis`
(−43), `cody-anderson` (−42) and `reece-torrent` (−19) fall because the **positional relativity in a
thin part of the tail is well below 1**, not because anything is broken. `cody-anderson` at SF pick 64
prints **18**, the sharpest consequence of consuming the positional object, and it is stated here in
advance so it cannot be presented afterwards as a surprise. The published RUCK floor at picks 63–64 is
**0.0**; **no fresh entrant stands there** (the two RUCKs are at picks 42 and 52), so the wiring never
prints a zero in this act — asserted, not assumed.

---

## 6. THE 43 POOL ENTRANTS — EVERY EXPECTED NEW PRINT, TABLED IN ADVANCE

`predicted new print = int(round(pool_v0.cells[pathway|position]))`.

| # | row | pathway | pos | cell | old print | **derived pool v0 (cell)** | **predicted new print** | Δ |
|---:|---|---|---|---|---:|---:|---:|---:|
| 1 | `ben-murphy` | IRE | SD | `IRE&#124;SD` | 85 | 87.030 | **87** | +2 |
| 2 | `cillian-bourke` | IRE | SD | `IRE&#124;SD` | 85 | 87.030 | **87** | +2 |
| 3 | `cillian-burke` | IRE | SD | `IRE&#124;SD` | 43 | 87.030 | **87** | +44 |
| 4 | `eamonn-armstrong` | IRE | SD | `IRE&#124;SD` | 43 | 87.030 | **87** | +44 |
| 5 | `kobe-mcdonald` | IRE | SD | `IRE&#124;SD` | 85 | 87.030 | **87** | +2 |
| 6 | `matt-duffy` | IRE | SD | `IRE&#124;SD` | 43 | 87.030 | **87** | +44 |
| 7 | `rob-monahan` | IRE | SD | `IRE&#124;SD` | 45 | 87.030 | **87** | +42 |
| 8 | `caleb-may` | MSD | RUCK | `MSD&#124;RUCK` | 322 | 448.213 | **448** | +126 |
| 9 | `harrison-coe` | MSD | RUCK | `MSD&#124;RUCK` | 322 | 448.213 | **448** | +126 |
| 10 | `iliro-smit` | MSD | RUCK | `MSD&#124;RUCK` | 204 | 448.213 | **448** | +244 |
| 11 | `max-mapley` | MSD | RUCK | `MSD&#124;RUCK` | 322 | 448.213 | **448** | +126 |
| 12 | `zac-walker` | MSD | SD | `MSD&#124;SD` | 152 | 358.535 | **359** | +207 |
| 13 | `max-beattie` | MSD | SF | `MSD&#124;SF` | 181 | 207.682 | **208** | +27 |
| 14 | `oliver-griffin` | MSD | SF | `MSD&#124;SF` | 181 | 207.682 | **208** | +27 |
| 15 | `logan-smith` | ND | RUCK | `ND>64&#124;RUCK` | 185 | 566.043 | **566** | +381 |
| 16 | `keighton-matofai-forbes` | ND | SD | `ND>64&#124;SD` | 104 | 260.291 | **260** | +156 |
| 17 | `lennox-hoffman` | ND | SD | `ND>64&#124;SD` | 104 | 260.291 | **260** | +156 |
| 18 | `river-stevens` | ND | SF | `ND>64&#124;SF` | 104 | 103.022 | **103** | -1 |
| 19 | `liam-hetherton` | PDA | KPF | `PDA&#124;KPF` | 168 | 117.305 | **117** | -51 |
| 20 | `nathan-wardius` | PDA | SF | `PDA&#124;SF` | 77 | 86.649 | **87** | +10 |
| 21 | `noah-chamberlain` | PDA | SF | `PDA&#124;SF` | 86 | 86.649 | **87** | +1 |
| 22 | **`kalani-white`** | PDN | KPF | `PDN&#124;KPF` **(BORROWED)** | 84 | 92.359 | **92** | +8 |
| 23 | `jesse-mellor` | PDN | MID | `PDN&#124;MID` | 84 | 112.725 | **113** | +29 |
| 24 | `benny-barrett` | PDN | SF | `PDN&#124;SF` | 50 | 54.678 | **55** | +5 |
| 25 | `jai-saxena` | PDN | SF | `PDN&#124;SF` | 84 | 54.678 | **55** | -29 |
| 26 | `ricky-mentha` | PDN | SF | `PDN&#124;SF` | 50 | 54.678 | **55** | +5 |
| 27 | `ryda-luke` | PDN | SF | `PDN&#124;SF` | 84 | 54.678 | **55** | -29 |
| 28 | `toby-whan` | PDN | SF | `PDN&#124;SF` | 84 | 54.678 | **55** | -29 |
| 29 | `xavier-walsh` | RD | KPD | `RD&#124;KPD` | 143 | 204.374 | **204** | +61 |
| 30 | `fred-rodriguez` | RD | MID | `RD&#124;MID` | 201 | 212.400 | **212** | +11 |
| 31 | `nick-driscoll` | RD | MID | `RD&#124;MID` | 201 | 212.400 | **212** | +11 |
| 32 | `riley-onley` | RD | MID | `RD&#124;MID` | 201 | 212.400 | **212** | +11 |
| 33 | `aiden-riddle` | RD | RUCK | `RD&#124;RUCK` | 151 | 372.076 | **372** | +221 |
| 34 | `joe-pike` | RD | RUCK | `RD&#124;RUCK` | 151 | 372.076 | **372** | +221 |
| 35 | `harry-charleson` | RD | SD | `RD&#124;SD` | 105 | 254.659 | **255** | +150 |
| 36 | `asher-eastham` | RD | SF | `RD&#124;SF` | 94 | 200.779 | **201** | +107 |
| 37 | `leon-kickett` | RD | SF | `RD&#124;SF` | 151 | 200.779 | **201** | +50 |
| 38 | `oscar-berry` | UNR | KPD | `UNR&#124;KPD` | 53 | 95.398 | **95** | +42 |
| 39 | `jacob-moss` | UNR | KPF | `UNR&#124;KPF` | 36 | 91.403 | **91** | +55 |
| 40 | `zak-evans` | UNR | MID | `UNR&#124;MID` | 29 | 264.746 | **265** | +236 |
| 41 | `jaime-uhr-henry` | UNR | RUCK | `UNR&#124;RUCK` | 26 | 79.687 | **80** | +54 |
| 42 | `patrick-carr` | UNR | RUCK | `UNR&#124;RUCK` | 31 | 79.687 | **80** | +49 |
| 43 | `indy-cotton` | UNR | SD | `UNR&#124;SD` | 48 | 107.696 | **108** | +60 |
| | **43 rows** | | | | **5082** | | **8096** | **+3014** |

**P29B-17.** Every row in this table that shares a cell prints the **same number** afterwards, whatever
it printed before (see the seven `IRE|SD` rows: 85/85/43/43/85/43/45 → **87 × 7**). That collapse is the
point of the act — a day-0 price is a property of the cell, not of the row — and it is predicted here so
it is read as the intended consequence rather than as lost information.

---

## 7. THE CONTROLS

**P29B-18 — CONTROL AT ENTRY.** A full board rebuild on the untouched tree reproduces
`86c8d5d9ba5b95e2cba05c78fbc31f78` byte-exactly. *(Run before this file was committed: **PASS**,
`rl_model a0854d1e`, store `cb38ef11`.)*

**P29B-19 — DETERMINISM.** Two independent fresh-workspace builds of the wired tree produce the **same**
board md5.

**P29B-20 — THE IDENTITY GATE (P16's instrument).** Re-run on the new final board after **exactly ONE
declared re-point** in the `o29_gate.py` copy lineage — its `PINS_ASSERT['board']` literal, from
`86c8d5d9` to the new board. Nothing else in the gate moves: not the 1e−6 identity tolerance, not
Ruling 9's ±2% band, not the `_maxres < 1e-3` halt, not the scorer, not the panel. Predicted:
**price-function identity bit-exact `0.000e+00` on the panel and board-wide**, attribution residual
≤ 2.220e-16, pins re-verified unmoved at exit.

**P29B-21 — THE BOOT GUARD.** Guard 5 green on everything ORDER 29B controls; **red on `fv` alone**, the
inherited ORDER-28 staleness, which this act does not touch and does not launder.

**P29B-22 — THE PIN MOVED-SET.** Predicted movers, and nothing else:

| pin | moves? | why |
|---|---|---|
| `board` | **YES** | the entry wiring |
| `rl_model` | **YES** | the P9 guard replaced by the signed-cell coverage assert |
| `engine_head` (`_merged_recover.py`) | **YES** | the day-0 branch in `ev()` |
| `pvc_curve_v2.json` (not in `expected_boot`) | **file md5 moves** | the two borrowed cells + their disclosure. `curve_md5` stays **`9729f0c5`** — the curve payload is **untouched** |
| `store` · `v0surf` · `config` · `band` · `bust_prior` · `peak_model` · `q97m` · `pvc_snapshot` · `register` | **NO** | asserted unmoved. `_v0surf_sig` hashes the **curve**, which does not move, so **no re-bake** |
| `fv` | **NO** | the inherited ORDER-28 red, reported not restamped |

**Anything moving outside this set is a stop-and-report, not a restamp.**

**P29B-23 — THE BOOK.** No re-seal. The #306 L7 entrant reconciliation reads occupancy × ladder, not
player prices (P29B-11); it is predicted to **pass silently**.

---

## 8. NO-ARB — THE EXPECTATION, SET HONESTLY AND IN ADVANCE

The as-of matrix is re-emitted under the wired engine and **both** cohort instruments plus mark-path and
reverse no-arb are run on it, using ORDER 29's disclosed copies under `noarb/`.

**P29B-24 — NO RE-POINT IS NEEDED.** The three blocking literals are `EXPECT_STORE cb38ef11`,
`EXPECT_V0SURF 4405cba2b42f`, `EXPECT_N 1200`. **This act moves none of them** — the store does not
move, the surface does not re-bake, and the teaching population does not change. Predicted: the
instruments **run without any literal being touched**. If one refuses, that is a finding and the halt is
reported verbatim rather than worked around.

**P29B-25 — WHAT MOVES IN THE MATRIX.** The matrix **store identity does NOT move**. What moves is
`ev(p, Y)` **at those (player, year) cells where the player had zero games as of Y** — i.e. the yr0
denominator wherever the mark is a genuine day-0 print, and nowhere else. The matrix file md5 therefore
moves; its pinned identities do not.

**P29B-26 — THE ARBITRAGES ARE NOT EXPECTED TO CLOSE.** ORDER 29 opened **2 of 10** readings as
arbitrages (legacy ND ALL picks 1–64 at +21.73% vs the 14% carry, and picks 1–20 at +29.92%). Those
arbitrages live in the **year-1+ marks**, which this act is ruled not to touch. **Predicted: the ND
cohort arbitrage does NOT close and the pool yr0→yr1 cliffs do NOT close.** What is predicted to move is
the **direction**: raising the day-0 denominator **reduces** measured yr0→1 appreciation wherever the
yr0 mark is a day-0 print, so the ND legacy readings should move **toward** the carry line without
necessarily crossing it. **NO TUNING. The reading is reported exactly as it comes out, in both
directions, and a reading that moves the wrong way is reported as such.**

**P29B-27.** mark-path progression and reverse no-arb: predicted **10 of 10 PASS** on both, as in
ORDER 29 — they read the landed board's marks and this act moves only day-0 marks.

**P29B-28.** `noarb_table_338.py` (all copies) stays byte-identical at md5
`0f8220351c64c56ccfa90c60edcdfa5f`, asserted at run.

---

## 9. THE LEDGER

**P29B-29.** `docs/ledgers/LANDING_29B_MOVERS_2026-08-13.{md,json}` carries every one of the 804 rows
twice over: the **entry-wiring lever** vs `86c8d5d9`, and the **composed five-lever** view vs live
`88ce647f` (unflag / grace / curve+v0 / numéraire / entry-wiring). **Predicted: both reconcile EXACTLY —
0 rows failing, max |residual| 0**, and the five lever sums add to the live→final total to the unit.

**P29B-30.** Nothing merges. PR #510 keeps its `[HELD — DO NOT MERGE]` title and its body intact.

---

## 10. THE STOP CONDITIONS

This seat STOPS at the step, pushes, and reports precisely if:

* the printed-day-0 identity is not exact on every wired row (P29B-1/2, tolerance 0);
* the `v` mover set is not exactly the 89 (P29B-5), or a coupled mover appears that P29B-6 did not name;
* any row with `cg > 0` moves on `v` (P29B-7);
* the board total lands outside `717,527 ± 5` (P29B-8);
* the borrowed cells do not reproduce `declined_unsigned` (P29B-13);
* a pin outside P29B-22's set moves;
* the two cohort instruments refuse the matrix on a pin (P29B-24);
* the two builds disagree (P29B-19).

**No improvising around a failure. No smoothing. No tuning toward a no-arb reading. Breaches are owned
by number.**
