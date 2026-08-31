# HANDOVER — the UI work block of 2026-08-31

Written before a context compaction. Everything a successor needs is HERE or in the repo, not in the
conversation. The one thing this session already lost — the pool-value override — was lost precisely
because it lived only in a working tree.

## Where things stand

The owner filed thirteen UI requests plus two bugs he found. NINE plus both bugs are landed and
pushed. What each of them decided is in its own commit message; the commits are the record and are
written to be read.

| # | ask | state |
|---|---|---|
| 1 | club summary depth on one row | DONE |
| 2 | config tab, model changes on/off | DONE — `ui/app/universe.js` |
| 3 | player card: weekly value graph since R14 | **TODO** |
| 4 | pool pick value -> 150 | **RULED, PENDING A BUILD** — see POOL_VALUE_150_OWNER_OVERRIDE.md |
| 5 | search dropdown >= 5 rows | DONE (see caveat below) |
| 6 | "pick 62" searchable | DONE |
| 7 | future picks searchable | DONE — rebuilt after his correction |
| 8 | draft pathway display (`MSD · 2021`) | DONE |
| 9 | rank/name column further left | DONE |
| 10 | cleaner font on value numbers | **TODO** |
| 11 | "vs Pick 1" bar with a ratio | **TODO** |
| 12 | Pick Value tab | DONE — `ui/app/pickvalue.js` |
| 13 | draft-day translator | **TODO** — the only one that is new analysis, not new display |
| — | entry price missing on player cards | DONE — `ui/tools/v0_identity.py` |
| — | FW1 absent from the movers list | DONE — it was labelled "Model change (MC-17)" |

## The remaining four, with what has already been settled

### #3 — the weekly value graph
Replace "recent form" on the player card with a value-over-time chart since R14, x and y axes
labelled. The data is `MD.history.series(key)` — it already returns one row per point with `v`, and
it now respects the universe (below), so the default chart is the current-model progression, which is
what the owner asked for. Do NOT re-derive the series; read it.

### #10 — the font on value numbers
Owner: "something that looks a little cleaner and less mechanical". Needs a choice put to him — offer
two, do not pick silently. Tabular figures matter (columns of numbers must align).

### #11 — "vs Pick 1"
Owner: the "vs top" bar becomes "vs Pick 1" with a ratio to two decimal places rendered ON the bar
and legible against it. Pick 1 = 3000 in the shipped `pvc`, so 9000 reads 3.00x and 300 reads 0.10x.
Read the curve; do not hardcode 3000.

### #13 — the draft-day translator
Feasibility was checked and it is real: the store carries 1570 ND-drafted rows of which 232 (15%)
NEVER played a game, so busts are represented and base rates would not be survivorship-inflated.
Per-year counts (67-78) are about a full national draft class. Two things to build in rather than
paper over: thin samples at individual picks, and an age cutoff for recent classes (19 of 71 from
2024 have not debuted — that is youth, not failure).

## THE ONE CORRECTION OWED (owner ruling, 2026-08-31)

`ui/app/pickvalue.js` carries a provenance line framing the v0-vs-pvc divergence as a caveat about
two artifacts that "do not reconcile". **The owner has ruled that the divergence is BY DESIGN and the
wording must say so:**

> "They are linked, but shouldn't average out strictly, as that weights each position equally. (i.e.
> Ruck + SD + SF + MID + KPF + KPD v0 for pick 1 should not strictly = 6 x pick 1 pvc) There are way
> less rucks drafted than midfielders, so the weighting is different. And mids and rucks provide
> better returns on investments than the average pick, so it makes sense they're > the all in curve.
> That's by design."

So MID at 1.15-1.42x and KPD at 0.64-0.90x is the model working. Reword the page to give the design
reason — position mix is not uniform, and mids/rucks genuinely return more per pick — instead of
implying an unresolved gap. Do NOT delete the numbers; they are useful. Change what they are said to
mean.

## Things learned the expensive way this session — do not re-learn them

1. **`ui/data/board_view_working.js` has TWO writers.** `extract_board_view.py` AND
   `round_movers.inject_release_contract`. Running only the first empties `stamp.release`, the app's
   balanced_board_md5 falls back to the wrong value, and `movers.test.js` goes red. This was done
   twice, a day apart, by the same seat. If you run a writer of record by hand, check
   `tools/landing/carriers.py` for how many that carrier has.
2. **A retro point is a round.** Its coverage, DNP truth and score belong to round N while its own id
   is `retro-r21`. `history.js` joins on `roundKey` for exactly this reason.
3. **`model_changes` no longer means "every out-of-round column".** A finals week is a column and is
   NOT a model change (`round_movers.football_column`). Anything deriving one from the other is wrong.
4. **The retrospective series is dropped by any act that rebuilds the movers bundle** and must be
   re-emitted (`docs/evidence/walkforward_retro_2026-08-29/emit_retro_series.py`, byte-idempotent).
   `ui/tests/movers.test.js` now fails if the shipped bundle is missing it.
5. **Chromium IS available** despite what `playwright-core` reports. `ui_222_items.test.mjs` and
   `responsive_layout.test.mjs` drive a real browser — layout work can and should be render-verified.
6. **Cost discipline, at the owner's prompt.** Run the full suite once per work block, not per edit.
   Batch shell calls. Prefer one agent with a wide brief over three narrow ones; each agent re-reads
   the codebase from scratch, and four of them cost ~610k tokens in this block.

## The suites, and what green looks like

    cd ui/tests
    node movers.test.js                 87
    node release_seam.test.js           33
    node ui_defects_2026-08-21.test.js  180
    node counting_rule.test.js          24
    node club_totals_parity.test.js     41
    node universe.test.js               13
    node pickvalue.test.js              90
    node ui_222_items.test.mjs          72   (browser)
    node responsive_layout.test.mjs     72   (browser, six widths)
    python3 tools/restamp.py check           ALL 5 STAMPS AGREE

## Two open flags nobody has actioned

* `ui/app/positions_data.js` is pinned to board `f2df6e0a` while the working bundle is `c8c2f2b6`,
  and `pocket.js:12` reads it with NO pin check. Same class of defect as the entry-price one: a file
  pinned to a board nobody re-checks.
* 2027 late-round picks can price above the same round's 2026 picks. It falls out of the owner's own
  year rule lifting late picks via the round average. He has seen it; it may be intended.
