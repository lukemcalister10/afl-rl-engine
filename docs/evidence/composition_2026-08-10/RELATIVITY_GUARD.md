# THE RELATIVITY GUARD — DEFINITION AND PRE-REGISTERED EXPECTATION

Owner condition, verbatim: *"we're not introducing the idea that peak players will be worth more
than picks/young players by more than they already are."*

**Written and committed BEFORE the measurement is taken.** A guard whose threshold is chosen after
seeing the number is not a guard.

---

## 1. THE RATIO — EXACT DEFINITION, SO THE CHECK IS REPRODUCIBLE

Career rung, for a board row, on the board's own evaluation year `Y = 2026`:

    rung(p) = Y - MA.debut(p) + 1        # 1 = his first season; <= 0 = not yet debuted

Two books, both summed over the **same board file**, in **board currency** (`active[].v`):

| book | membership |
|---|---|
| **YOUNG** | every draft **pick** asset priced on the board, **plus** every player with `rung(p) <= 1` (i.e. the year-0 entrants and the year-1 cohort) |
| **PEAK** | every player with `rung(p) in {4, 5, 6}` |

    RELATIVITY = Sigma(YOUNG book) / Sigma(PEAK book)

Rules that make it a fair before/after:

- computed by **one function, run twice** — once on the pre-act board, once on the post-act board —
  never by two code paths;
- **membership is frozen on the PRE-act board and reused on the post-act board**, keyed by player
  key. A player does not change rung between the two boards (the store and the calendar are
  identical), but freezing it removes any doubt that the ratio moved because the *population*
  moved rather than because prices moved;
- the pick side is the board's own priced pick ladder (the 160 picks the release prices off the
  canonical curve), taken from the same artifact on both sides;
- **no re-weighting, no winsorising, no exclusions.** Whole books.

Reported beside the ratio, so a move can be attributed rather than guessed:

- each book's own total, before and after, and its percentage move;
- the ratio before, after, and the change in percentage points;
- the same three lines **per item** (B, A, C, E1, E2, H) as each is composed, so a move can be
  traced to the item that caused it.

---

## 2. THE PRE-REGISTERED EXPECTATION

**The package should NARROW the peak-vs-young gap — i.e. RELATIVITY should RISE, or at worst hold.**

The mechanism reasoning, stated now so it can be checked against the outturn rather than fitted to
it:

- **ITEM C** lifts the *played* year-1 rows (the evidence-weight cap release; `w = 0` rows are
  untouched by construction) → adds to the YOUNG book.
- **ITEM A** restores the fitted year-0 prior to the year-1+ anchor leg, whose measured
  per-position effect includes KPD **+16,546** and SD **+8,289** — young-side protection → adds to
  the YOUNG book, though A's net across positions is negative before the conservation re-teach, so
  A's sign here is the one genuinely uncertain input.
- **ITEM B** is level-preserving **within the pool** (Σ held exactly), so its net effect on this
  ratio is ~0 by construction — it moves value *between pool ages*, not between rungs. Any move it
  shows is second-order, through the sit-out blend and the floor.
- **ITEM H** cuts pool-sitter and mature cells, most of which sit in **neither** book (they are
  rung 2-3 or older pool rows) — so H's effect is expected to be small and mixed.
- **ITEMS E1/E2** are ruck-only and small.

**HALT CONDITION (not a tweak):** if RELATIVITY **falls** materially — the package moving value
*away* from picks and young players toward the peak rungs — that is a **top-of-report flag for the
owner before adoption**. It will not be rebalanced silently to pass, and no component will be
retuned to move it. Materiality is judged against the pre-act ratio and stated as a percentage
point change, with the per-item attribution beside it so the owner sees which item did it.

**Why the direction matters beyond this act:** an asymmetric move here is the same family of
error the LEVEL LAW bars. Moving one rung's prices without the others manufactures an arbitrage —
in the level law's case pick-hoarding, here its mirror. The guard exists so the composition cannot
introduce one by accident while every individual item looks conserved on its own book.

---

## 3. STATUS

Definition and expectation registered. The measurement runs as part of the side-by-side, once
ITEMS A / C / E1 / E2 / H are composed onto the ITEM B board. ITEM D is **parked** by owner ruling
(5240605334) and contributes nothing to either book.
