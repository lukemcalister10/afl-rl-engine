# ORDER 8 — THE SPLIT COHORT TABLES, AND WHERE ITEM B'S ×2.0478 CAME FROM

**Measurement and provenance only. No repair, no retune, no dial changed.** `RL_H_MATNONRD` is
untouched at its filed value and awaits the owner's explicit word.

---

# PART 1 — THE OWNER'S TWO-STORIES HYPOTHESIS IS CONFIRMED, ON HIS OWN INSTRUMENT

> *"we have two stories here — ND players, who are priced at X, and appreciate over time to year 4/5,
> where they are worth ~50% more as a ND cohort. And pool players, who do not."*

**Ratios (Σ price at year N ÷ Σ year-0 anchor of the same included set). Base `main`, all-time cohorts:**

| split | n | yr0 | yr1 | yr2 | yr3 | **yr4** | yr5 | yr6 |
|---|---|---|---|---|---|---|---|---|
| **ND 1-64** | 1444 | 1.0000 | 1.0998 | 1.3508 | 1.5026 | **1.5565** | 1.5380 | 1.4818 |
| **Pool-Rookie (RD)** | 688 | 1.0000 | 0.5430 | 0.6565 | 0.6616 | **0.7428** | 0.7250 | 0.6940 |
| **Pool-non-rookie** | 509 | 1.0000 | 0.4338 | 0.6052 | 0.6120 | **0.6748** | 0.6911 | 0.5855 |
| COMBINED | 2641 | 1.0000 | 0.9246 | 1.1280 | 1.2319 | 1.2890 | 1.2712 | 1.2124 |

**Cohorts 2012+ (base `main`):**

| split | n | yr1 | yr2 | yr3 | **yr4** | yr5 | yr6 |
|---|---|---|---|---|---|---|---|
| ND 1-64 | 938 | 1.1399 | 1.3610 | 1.5009 | **1.5045** | 1.5054 | 1.4932 |
| Pool-Rookie | 317 | 0.4847 | 0.5376 | 0.5230 | **0.6326** | 0.6555 | 0.6570 |
| Pool-non-rookie | 421 | 0.4345 | 0.6377 | 0.6780 | **0.7698** | 0.8230 | 0.6920 |
| COMBINED | 1676 | 0.9573 | 1.1310 | 1.2286 | 1.2559 | 1.2624 | 1.2309 |

**EVERY PRE-REGISTERED PREDICTION HELD.**

| | prediction | measured (all-time / 2012+) | verdict |
|---|---|---|---|
| H8.1 | ND yr4 ≥ 1.40 | **1.5565 / 1.5045** | **HELD** |
| H8.2 | Pool-Rookie yr4 < 1.10 | 0.7428 / 0.6326 | **HELD** |
| H8.3 | Pool-non-rookie yr4 < 1.10 | 0.6748 / 0.7698 | **HELD** |
| H8.4 | gap ≥ 0.40 | 0.81 & 0.88 / 0.87 & 0.73 | **HELD** |
| H8.5 | Σv0 moves: ND < 0.5%, pool > 5% | ND **−0.02%**, RD **−25.10%**, non-rookie **−22.40%** | **HELD** |
| H8.6 | 2012+ does not flip signs | identical ordering | **HELD** |

**The owner's "~50% more by year 4/5" is right to the decimal: 1.5565 all-time, 1.5045 on 2012+.**
And neither pool arm appreciates at all — both are still **below their entry price at year 6**.

## Read the totals WITH the ratios — the FULL base is partly a denominator story

**H8.5, the measured Σ year-0 move from `main` to `FULL`:**

| split | Σv0 main | Σv0 FULL | move |
|---|---|---|---|
| ND 1-64 | 1,217,118 | 1,216,928 | **−0.02%** |
| Pool-Rookie | 352,757 | 264,205 | **−25.10%** |
| Pool-non-rookie | 192,830 | 149,640 | **−22.40%** |

Under `FULL`, Pool-Rookie's year-4 ratio *improves* from 0.7428 to 0.9474. **That is not the arm
delivering more — it is its entry price falling 25% while its delivered value moves far less.** The
ratio flatters; the totals do not. This is the P7.3 effect, and it is **pool-only**: ND's year-zero
anchors are unmoved at −0.02%.

## What these tables can and cannot settle

They establish **that** the arms deliver very differently against their own entry prices — ND returns
**1.5565** per unit of entry price at year 4, the pool arms **0.7428** and **0.6748**, a ratio of about
**2.1-2.3 to 1**. They **cannot** say which price is wrong: "pool v0 too high" and "ND v0 too low" are
observationally identical in a ratio. Both readings are on the table and the ruling is the owner's.

---

# PART 2 — WHERE ITEM B's ×2.0478 CAME FROM

## The provenance chain

| link | artifact |
|---|---|
| shipped constant | `engine/rl_after/_merged_recover.py:1804-1806` — `_B_KNOTS = [(18, 0.6859), (19, 1.4112), (20, 1.4112), (21, 2.8173)]` |
| applied at | `_merged_recover.py:1826` `_b_factor(p) = _b_renorm() * _b_shape(_b_age(p))`, consumed by `entry_anchor` at `:1834` — **pool rows only** |
| live renormaliser | `k = 0.726863` (state function, re-derived every build) → the shipped effective factor at draft age 21+ is **`k × 2.8173 = 2.0478`** |
| derivation script | `docs/evidence/composition_2026-08-10/item_b_derive.py` |
| derivation output | `item_b_derive_out.txt`, `item_b_factors.json` |
| ruling | comments 5238688172 / 5238860310 |

## The sample and the outcome measure

- **Population**: the **pool teaching population on the corrected ruler — n = 673, classes 2004-2015**
  (`item_b_derive.py:51`, filter `is_pool`, requiring a corrected-ruler value). **It includes RD.**
- **Outcome measure**: `F = Σ(REALIZED / DISC^4) / Σ(v0)` — realized delivered value per unit of
  year-zero price, discounted at `DISC = 1.0939`, the year-0 F verdict of `item_i_restate.py`
  (`item_b_derive.py:8`). Not the N43 signed levels, and not a fitted return-by-age curve — **a
  measured delivery ratio on frozen per-entrant matrices**.
- **The three bands, as derived:**

| band | n | eff-n | Σv0 | **F** | re-derived factor | as filed | 95% CI on F |
|---|---|---|---|---|---|---|---|
| ≤18 | 429 | 367.2 | 132,265 | 0.3591 | 0.6859 | 0.666 | [0.223, 0.529] |
| 19-20 | 111 | 90.9 | 40,645 | 0.7389 | 1.4112 | 1.200 | [0.413, 1.128] |
| **21+** | **133** | **60.5** | **13,666** | **1.4751** | **2.8173** | 2.474 | **[0.821, 2.238]** |

pool-wide `F = 0.523593`; each factor is `F_band / F_pool`, level-preserving by construction.

## The disclosed weakness inside the 21+ band, in the derivation's own words

The script prints the per-single-age detail and **every cell inside 21+ fails the F8 sample bar**:

| age | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 29 |
|---|---|---|---|---|---|---|---|---|
| eff-n | 27.8 | 15.7 | 11.6 | 7.5 | 1.0 | 2.7 | 1.0 | 1.7 |
| measured factor | 2.77 | 3.38 | 3.59 | **0.75** | **0.00** | **0.01** | **0.00** | **0.00** |

**The 21+ factor is carried entirely by ages 21-23 and collapses to essentially zero from 24 on.** The
band is pooled flat at 2.8173 and the pooling is declared ("mature-21+ unnameable → base factor,
pooling disclosed"). So a 25-year-old pool entrant, whose own cell measured **0.00**, receives the same
**×2.0478** as a 22-year-old whose cell measured 3.38.

**Banch is draft age 22 and Podhajski 21 — both inside the supported part of the band.** The mechanism
that doubled them is `entry_anchor × 2.0478`, and because a no-evidence entrant's price *is* his entry
anchor, the anchor move passes through to the board almost in full.

## TENSION (i) — B vs THE OWNER'S INTUITION. The empirical judge, and it favours the owner

> *"Pool v0 of mature non-rookie draft might make sense to be less given historical data."*

**These are the cells that answer it** (base `main`, year-4 delivery per unit of entry price, split by
draft age *within* each pool arm):

| draft age | **Pool-non-rookie** yr4 | **Pool-Rookie (RD)** yr4 |
|---|---|---|
| ≤18 | 0.4869 | 0.5820 |
| 19-20 | **0.9851** | 0.6142 |
| **21+** | **0.7708** | **3.0092** |

**B's gradient is supported on the ROOKIE arm and contradicted on the NON-ROOKIE arm.** RD entrants
drafted at 21+ deliver **3.01×** their entry price at year 4 — that is exactly the effect B measured.
Non-rookie pool entrants drafted at 21+ deliver **0.77×**, *below* their own 19-20 slice at 0.99.

**And B applies the same ×2.0478 to both**, because `_b_shape` reads draft age alone and `_b_factor` is
applied to every `_pool` row regardless of type. B's derivation sample pools RD with non-RD by
construction (`item_b_derive.py:51` filters on `is_pool` only).

> **THE FINDING: the evidence carrying ITEM B's 21+ lift comes substantially from the ROOKIE arm, and
> the lift is then applied to the NON-ROOKIE arm, where the same measurement runs the other way. On
> that arm the owner's intuition is supported by the data and ITEM B is pushing against it.**

This is a measurement, not a proposal. Nothing is changed.

## TENSION (ii) — B vs H. Same instrument, same sample, opposite signs

| | ITEM B | ITEM H (mature nonRD) |
|---|---|---|
| instrument | `DISC = 1.0939`, `BARN = 35.0`, `NB = 4000`, corrected ruler | **identical constants** (`item_h_derive.py:20`) |
| population filter | `is_pool` (**includes RD**) | `is_pool` (**mature nonRD cell excludes RD**) |
| corrected-ruler sample | **n = 673** | pool rows n=1001, **673 with a corrected-ruler value** |
| the mature cell | 21+ : n=133, eff-n **60.5**, F **1.4751** | mature nonRD : n=99, eff-n **46.2**, F bent **0.7676**, F corr **0.5162** |
| what it does | **multiplies the ENTRY ANCHOR by 2.0478 (+105%)** | **multiplies the FINISHED PRICE by 0.615 (−38.5%)** |
| derivation status | reproduces; bridge to filed priors printed | **HALTED — "does not reproduce", taken AS FILED**; CI [0.115, 1.226] contains 1.0 |

**The samples overlap and the instrument is the same one.** Both are the 673-row corrected-ruler pool
population; B's 21+ band and H's mature-nonRD cell are the same demographic minus RD.

**They are not contradictory as measurements** — B's factor is normalised to the *pool mean* (a
level-preserving reshape: someone in the pool must go down for these to go up), while H's factor is a
delivery ratio against *fair* (an absolute cut). **They are incoherent as a design**, and on a real
player the two compose:

> a mature-drafted non-rookie pool entrant has his **year-0 anchor raised 105%** because his band
> out-delivers the rest of the pool, and his **finished price cut 38.5%** because the same demographic
> under-delivers fair. Both were ruled. Neither ruling was shown the other's effect.

And the owner has now ruled the H *form* out: a mature-pool discount, if the data supports one,
belongs on the **v0/prior side where a body of work overcomes it** — which is precisely where ITEM B
already sits, pushing the opposite way.

---

## Reproduction

```
python3 noarb_table_splits.py                 # SPLIT_TABLES.txt / .json — both bases, both windows
python3 pool_arm_probe.py                     # the B renormaliser k and the per-channel measurements
cat item_b_derive_out.txt item_b_factors.json # ITEM B's derivation, sample and per-age detail
cat item_h_derive_out.txt item_h_factors.json # ITEM H's derivation, and its halt
```

`noarb_table_338.py` md5 `0f8220351c64c56ccfa90c60edcdfa5f` — unmodified, asserted at every run of both
sibling readers. No new emits: every table above is a re-read of the stored matrices.

---

# PART 3 — ADDENDUM UNDER THE PLAY-QUALITY PRINCIPLE (owner ruling 5249619354)

> *"we don't value players on whether they play, we value them on how they play. So it doesn't make
> sense to add value to those guys unless we have data that they play well."*

## 3.1 WAS ITEM B FITTED TO PLAY QUALITY OR TO PARTICIPATION? — **PARTICIPATION-INCLUSIVE. IT FAILS THE RULED PRINCIPLE.**

**The measure, traced to its definition.** B's outcome variable is `D_rt_win`, taken from the corrected
ruler `r24_rows.json` (`item_b_derive.py:55`). What that quantity is, in the project's own words at
`item_d_derive.py:22-23`:

> *"The corrected-ruler numerator (r24 `D_rt_win`) is **REALIZED DELIVERY off the seasons and bars**"*

**It is a delivered-VALUE quantity, not a scoring-rate quantity.** A player raises it by playing *better*
**or** by playing *more* — seasons and qualification bars are both inputs. So B was **not** fitted to
play quality; it was fitted to a composite that participation moves. **Under the ruled principle it does
not meet the standard, and it cannot be defended as a play-quality fit.**

**And the separation, measured directly** (base `main`; *quality* = career games-weighted scoring
average; *participation* = career games):

| split | draft age | n | **quality** | **participation** | n with 0 games |
|---|---|---|---|---|---|
| ND 1-64 | ≤18 | 1302 | 60.73 | 76.1 | 181 |
| ND 1-64 | 19-20 | 74 | 61.38 | 93.5 | 8 |
| ND 1-64 | 21+ | 68 | 61.98 | 77.3 | 4 |
| Pool-Rookie | ≤18 | 436 | 56.40 | 31.6 | 227 |
| Pool-Rookie | 19-20 | 119 | 62.34 | 50.1 | 54 |
| **Pool-Rookie** | **21+** | 136 | **63.00** | **51.0** | 31 |
| Pool-non-rookie | ≤18 | 212 | 51.47 | 24.7 | 99 |
| Pool-non-rookie | 19-20 | 133 | 52.98 | 31.7 | 50 |
| **Pool-non-rookie** | **21+** | 165 | **53.33** | **21.6** | 54 |

**On the NON-ROOKIE arm — the arm the owner is asking about — there is essentially no quality gradient
at all: 51.47 → 52.98 → 53.33, a spread of 3.6%. And the 21+ slice PLAYS THE LEAST of the three (21.6
career games, below both younger bands).** ITEM B nonetheless multiplies their entry anchor by
**2.0478 (+105%)**.

On the rookie arm the 21+ slice does look better, but the edge is **participation-dominated**:
**+61%** on games against **+11.7%** on quality.

> **VERDICT UNDER THE RULED PRINCIPLE: ITEM B's ×2.0478 is not supported by play-quality data on either
> arm, and on the non-rookie arm the quality series is flat while participation is the worst of the
> three bands. The lift adds value for being mature, not for playing well.**

Measurement only. Nothing is changed and no factor is touched.

## 3.2 THE OWNER'S PAIR — PODHAJSKI AND HERBERT, SIDE BY SIDE

| | **Mitch Podhajski** (KPF, 27, draft 2026, 2 career games) | **Marcus Herbert** (MID, 24, draft 2026, 30 career games) |
|---|---|---|
| main | **101** | **1060** |
| after ITEM B | 203 (**+102**) | 1060 (**+0**) |
| after era removal | 203 (+0) | 1060 (+0) |
| **FULL** | **245** (net **+144, +142.6%**) | **627** (net **−433, −40.8%**) |
| ITEM H, removed | 397 (**+152**) | 1020 (**+393**) |
| surprise law, removed | 129 (**−116**) | 627 (+0) |
| ITEM A / C / E1, removed | +0 each | +0 each |
| #336 channels, removed | 0 / 0 / +1 | −1 / +9 / +16 |
| XW · V5 · STACK | 246 · 245 · 246 | 648 · 639 · 659 |

**Both are the same demographic — mature-drafted non-rookie pool — and they are moved by different items
because of ONE thing: whether they have production.**

- **Podhajski has 2 games, so his price IS his entry anchor.** ITEM B's +105% passes through almost in
  full (+102), the surprise law adds a further +116, and ITEM H takes −152. **B wins the net: +142.6%.**
- **Herbert has 30 games, so his anchor is already faded out of his price.** ITEM B reaches him by
  **exactly zero**. Only ITEM H reaches him, and it takes **−393**, the full 38.5%. **H alone: −40.8%.**

**That pair is the whole incoherence in two rows: the same ruled machinery doubles the man who has not
played and halves the man who has.** No menu candidate repairs it — XW, V5 and the STACK move Podhajski
by ≤1 point and Herbert by +12 to +32 against a −433 cut.

## 3.3 THE UNION CELL — the same three questions asked of `H_UNION`

The seat has put `H_UNION` into the H re-derivation scope alongside `H_MATNONRD`. Its audit:

| question | `H_MATNONRD` (0.615) | **`H_UNION` (0.280)** |
|---|---|---|
| **reproduces?** | **NO** — ruled 0.615 vs F bent 0.7676, `HALT-NO-SURPRISE`, taken AS FILED | **NO** — ruled 0.280 vs F bent **0.1670**, same halt, taken AS FILED |
| **CI on F** | [0.115, **1.226**] — **contains 1.0**, cannot exclude *no cut* | [0.010, **0.639**] — **excludes 1.0**; a cut IS supported in direction | 
| **disclosed?** | factor named in the directive; **no board-effect figure anywhere** | factor named in the directive; **no board-effect figure anywhere** |
| n / eff-n | 99 / 46.2 | 95 / 60.3 |
| corrected-ruler reading | 0.5162 | 0.2301 |

**The two cells fail differently, and the difference matters for the re-derivation.**
`H_MATNONRD` is **unsupported** — its own interval cannot exclude no cut at all. `H_UNION` is
**supported in direction but ruled MILDER than its own evidence** (0.280 against a bent 0.167 and a
corrected 0.230), so re-deriving it would, on this evidence, make it *deeper*, not shallower.

**AND THE THING NEITHER CELL'S EVIDENCE SHOWS: THE COMPOSITION.** The engine multiplies the cells
together (`_h_cut`, `_merged_recover.py:1999-2011`). Measured on the three MSD rucks the owner flagged:

> Harrison Coe / Caleb May / Max Mapley — noH **472** → FULL **66**, ratio **0.1398**
> `H_POOLSIT × H_UNION × H_MATNONRD = 0.804 × 0.280 × 0.615 = 0.1384`

**An 86% cut from three cells composing.** A search of the directive, `PHASE2.md` and
`item_h_derive_out.txt` finds **no composed factor anywhere** — the derivation lists the three cells
independently and the engine multiplies them. The composed number was never put in front of the owner.

> **The union cell therefore joins `H_MATNONRD` in the re-derivation scope on the same grounds as the
> HALT-GRADE finding of ORDER 6: it did not reproduce, it was taken as filed, and neither its own board
> effect nor its composition with the other two cells appears in any ruled evidence.**
