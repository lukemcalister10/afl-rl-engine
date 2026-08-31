# HANDOVER — the UI work block of 2026-08-31

Written before a context compaction. Everything a successor needs is HERE or in the repo, not in the
conversation. The one thing this session already lost — the pool-value override — was lost precisely
because it lived only in a working tree.

## Where things stand

The owner filed thirteen UI requests plus two bugs he found. **TWELVE plus both bugs are landed
and pushed; only #4 remains**, and it is ruled rather than open — it rides the next board rebuild. What each of them decided is in its own commit message; the commits are the record and are
written to be read.

| # | ask | state |
|---|---|---|
| 1 | club summary depth on one row | DONE |
| 2 | config tab, model changes on/off | DONE — `ui/app/universe.js` |
| 3 | player card: weekly value graph since R14 | DONE — `ui/app/card.js` weeklyValueChart |
| 4 | pool pick value -> 150 | **RULED, PENDING A BUILD** — see POOL_VALUE_150_OWNER_OVERRIDE.md |
| 5 | search dropdown >= 5 rows | DONE (see caveat below) |
| 6 | "pick 62" searchable | DONE |
| 7 | future picks searchable | DONE — rebuilt after his correction |
| 8 | draft pathway display (`MSD · 2021`) | DONE |
| 9 | rank/name column further left | DONE |
| 10 | cleaner font on value numbers | DONE — owner chose the system sans; `--fig` split from `--mono` |
| 11 | "vs Pick 1" bar with a ratio | DONE — `MD.valueLine` + the pick-1 tick |
| 12 | Pick Value tab | DONE — `ui/app/pickvalue.js` |
| 13 | draft-day translator | DONE — the Draft day tab, its generator and its writer of record |
| — | entry price missing on player cards | DONE — `ui/tools/v0_identity.py` |
| — | FW1 absent from the movers list | DONE — it was labelled "Model change (MC-17)" |

## What remains: ONE item, and it is ruled rather than open

### #4 — the pool pick value -> 150
The owner's word, verbatim: *"override it to 150 please, noting it's an owner override and knowingly
isn't derived."* The ruling, what it overrides, its blast radius, the exact edit and its falsifier
are all in `docs/pending/POOL_VALUE_150_OWNER_OVERRIDE.md`. It touches `pvc`, which is published in
the board bundle, so it is a carrier move and therefore an ACT — it rides the next board rebuild
(FW2) rather than being a text edit anyone can make. Nothing else is waiting on it.

## What the other twelve decided — the notes worth keeping

* **#3 · the weekly value graph.** Reads `MD.history.series`; derives nothing, because that function
  already owns which universe is on screen, what each point is, and the fact that the value trace is
  complete for every player at every point (so the line needs no did-not-play handling — score
  coverage is the patchy column, value is not). The y axis is not zero-based and the chart says so.
  The season scores the retired "recent form" line drew survive per round in the history table's
  Score column, where each carries its own played / DNP / not-recorded truth.
* **#10 · the figure face.** Two were rendered and put to him; he chose the system sans. The change
  is a token split, not a font sweep: `--fig` is a VALUE (price, delta, ratio, rank, score) and
  `--mono` is an IDENTIFIER or caption (club name, pick slug, stamp, footnote). What monospace was
  actually buying was column alignment, and `tabular-nums lining-nums` keeps it — the suite asserts
  the property (same digit count renders at the same measured width) and not the family name, which
  is his to change.
* **#11 · "vs Pick 1".** The FILL stays anchored 0..top-of-board so the column still ranks the page;
  the NUMBER is the ratio to pick 1; the TICK at pick 1's own position on that track reconciles the
  two. Pick 1 is read off the board's own curve, never hardcoded. Found by looking at the rendered
  page: the foot of the board printed a column of `0.00x` for players worth single digits, which
  reads as "worth nothing" and is false — it says `<0.01x` now, and the suite fails if `0.00x` ever
  returns.
* **#13 · Draft day.** A generator (`ui/tools/gen_draft_outcomes.py`), a tab (`ui/app/draftday.js`),
  63 tests, and a writer of record in the landing. Its two hard-won facts are below.

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
   Batch shell calls. Four subagents cost ~610k tokens in this block because each re-reads the
   codebase from scratch, and the owner noticed: 67% of a five-hour allowance in 24 minutes.

   **HIS RULING, 2026-08-31, verbatim: "for now inline, but subagents are a resource we can and
   should use if the situation suits it."** So the default is inline. A subagent is justified when a
   task genuinely needs its own large context and is well isolated by file — #13, the draft
   translator, is the one remaining item that qualifies. Three narrow agents editing neighbouring
   files is the pattern to avoid: it triples the reading cost and produced two collisions in this
   block. Ask before spending it, rather than after.

## Two facts the Draft day build turned up, both of which outlive it

7. **THE STORE'S TOP-LEVEL `games` IS STALE for every player with a live season.** Measured: all 981
   national-draft players with no 2026 season have `games` equal to the sum of their own `scoring`
   rows; only 196 of the 589 with one do. Six read `games == 0` while their season rows recorded
   football this year. The season rows are what the weekly ingest writes — the FW1 edit moved them
   and left the scalar where it was — so **career games is the sum of the seasons, and the scalar is
   a copy that lags**. Anything computing a career total from `row['games']` is wrong for a third of
   the population. Found by an assertion, not by reading.
8. **The tab strip could not hold eight tabs.** It was a non-wrapping inline-flex row with
   `overflow:hidden`, so the eighth clipped off the end at 720px with no scroll affordance to
   recover it. It wraps now. `responsive_layout`'s clipping probe caught it, which is what that
   probe is for. Related: `ui_222_items`'s runtime loop is now driven off `MD.TABS` instead of a
   hand-kept list of five view names — that list had already fallen behind twice.

## The suites, and what green looks like

    node ui/tests/movers.test.js                 87
    node ui/tests/release_seam.test.js           33
    node ui/tests/ui_defects_2026-08-21.test.js  180
    node ui/tests/counting_rule.test.js          27
    node ui/tests/club_totals_parity.test.js     41
    node ui/tests/universe.test.js               13
    node ui/tests/pickvalue.test.js              90
    node ui/tests/draftday.test.js               63   (new)
    node ui/tests/ui_222_items.test.mjs          87   (browser)
    node ui/tests/responsive_layout.test.mjs     72   (browser, six widths)
    python3 tools/landing/test_finals_bounds.py  OK
    python3 tools/landing/test_store_edit.py     15
    python3 tools/landing/test_proofstash.py     23
    python3 tools/restamp.py check                    ALL 5 STAMPS AGREE

Preflight against a SPENT spec shows two reds that are not regressions: `clean_tree` on any
uncommitted work, and `store_sanity`, because a spec whose edits have already flown no longer
matches the store its old-value assertions were written against.

## Open flags

* **`ui/app/positions_data.js` — investigated, and the earlier wording here was wrong.** It is not
  the same class as the entry-price defect. The map is VALUES-FREE (player key to position codes,
  off the owner's locations CSV), so it does not depend on the board and a price move cannot stale
  it; the board md5 in its stamp is simply the wrong pin rather than a failed one. And the reader is
  already honest about a miss: `pocket.js` accumulates an uncovered player's value into an
  alarm-coloured **"Unlisted"** row with its share of the club, which is a better guard than a board
  md5 would have been. Coverage measured 804/804 with no stragglers.
  WHAT WAS ACTUALLY MISSING, now closed: a gap went to a row on screen rather than red in a suite.
  `counting_rule.test.js` now asserts set equality both ways and names the offending keys.
  STILL OPEN, and small: the stamp should name what the file actually derives from (the roster key
  set and the CSV) instead of a board. That means touching `ui/tools/extract_positions.py`, a writer
  of record, so it belongs in an act rather than in a UI block.
* 2027 late-round picks can price above the same round's 2026 picks. It falls out of the owner's own
  year rule lifting late picks via the round average. He has seen it; it may be intended.
