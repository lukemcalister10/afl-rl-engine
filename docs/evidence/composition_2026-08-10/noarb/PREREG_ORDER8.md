# PRE-REGISTRATION — ORDER 8, THE SPLIT NO-ARB TABLES

**Filed BEFORE the split tables were read.** The owner's hypothesis is stated as *his*, and each split
gets an expected sign that can be breached.

## The owner's hypothesis, verbatim

> *"we have two stories here - ND players, who are priced at X, and appreciate over time to year 4/5,
> where they are worth ~50% more as a ND cohort. And pool players, who do not. Pricing should be
> logical. So if pool players are not going on to provide a similar return on their investment by their
> peaks compared to ND players, then one of them have an incorrect starting price and I'd suspect it's
> the pool or components of it?"*

## The splits, and where ND picks > 64 land

| split | definition (the engine's own fields) |
|---|---|
| **(a) ND 1-64** | `type == 'ND'` and `1 <= pick <= 64` and **not** `is_pool` |
| **(b) Pool-Rookie** | `type == 'RD'` |
| **(c) Pool-non-rookie** | every other `is_pool` row: `SSP`, `MSD`, `PDA`, `PDN`, `PDS`, `IRE`, `UNR`, **and ND picks > 64** |

**ND > 64 goes in (c), and the count is printed.** Under the ruled July-28 pricing split an ND selection
past the curve's last pick collapses to the single pool index (`effpk = POOL_PICK`, `is_pool = True`) and
is priced off its signed division level, not off the pick curve. It is a pool row by the engine's own
typing, it is not a rookie-draft row, so it belongs in the non-rookie pool split. Putting it in (a)
would put a division-level-priced row inside the pick-curve column.

## Instrument

`noarb_table_splits.py` — a sibling of `noarb_table_allarm.py`, same cohort key (draft year + 1, except
MSD = draft year), same value semantics, same `WINDOW_END` derivation. **`noarb_table_338.py` is NOT
modified**; its md5 is asserted at every run. **No new emits** — the stored matrices already carry every
row and every year, so this is a re-read of the same engine runs.

Both **Σ totals** and **ratios** are reported for every (split, year) cell with its **n**, because the
owner asked for totals explicitly and because the two answer different questions: a total moves when
either prices or population move, a ratio divides one by the other.

## PREDICTIONS — the owner's hypothesis, per split, on the **main** base

**H8.1 — ND 1-64 APPRECIATES, and by roughly half.** Predicted year-4 ratio **≥ 1.40**.
*Falsifier: below 1.40.*

**H8.2 — Pool-Rookie (RD) DOES NOT APPRECIATE.** Predicted year-4 ratio **< 1.10**.
*Falsifier: at or above 1.10.*

**H8.3 — Pool-non-rookie DOES NOT APPRECIATE.** Predicted year-4 ratio **< 1.10**.
*Falsifier: at or above 1.10.*

**H8.4 — THE GAP IS THE STORY.** Predicted `ND yr4 ratio − pool yr4 ratio` **≥ 0.40** for both pool
splits. *Falsifier: a gap under 0.40 — which would mean the two-stories reading is an artefact of
pooling the arms together rather than a real difference between them.*

**H8.5 — THE P7.3 EFFECT IS POOL-ONLY.** Σ year-0 anchors should fall main→FULL for both pool splits
and be essentially unmoved for ND 1-64. Predicted: ND Σv0 moves **< 0.5%**, pool Σv0 moves **> 5%**.
*Falsifier: either side breaking.* This is reported beside every ratio so totals and ratios can be read
together — **a pool ratio that looks unmoved may be a numerator and a denominator falling together.**

**H8.6 — THE 2012+ RESTRICTION DOES NOT FLIP THE SIGNS.** Predicted: the same ordering (ND appreciates,
neither pool split does) holds on cohorts 2012+. *Falsifier: any split changing side.*

## What this can and cannot decide

It can say **whether** the arms deliver differently against their own entry prices. It **cannot** say
which entry price is wrong — that is the owner's ruling, and the two candidate answers (pool v0 too
high, or ND v0 too low) are observationally identical in a ratio. Both readings are stated.

**No repair, no retune. Measurement and provenance only.**
