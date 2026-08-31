# HANDOVER — the UI work block of 2026-08-31

Written before a context compaction. Everything a successor needs is HERE or in the repo, not in the
conversation. The one thing this session already lost — the pool-value override — was lost precisely
because it lived only in a working tree.

## Where things stand

The owner filed thirteen UI requests plus two bugs he found. **ALL THIRTEEN, both bugs and both
standing flags are landed and pushed.** What each of them decided is in its own commit message; the commits are the record and are
written to be read.

| # | ask | state |
|---|---|---|
| 1 | club summary depth on one row | DONE |
| 2 | config tab, model changes on/off | DONE — `ui/app/universe.js` |
| 3 | player card: weekly value graph since R14 | DONE — `ui/app/card.js` weeklyValueChart |
| 4 | pool pick value -> 150 | DONE — a display override at the publish seam, board untouched |
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

## What remained, and how it closed

### ~~#4 — the pool pick value -> 150~~ — DONE 2026-08-31, as a DISPLAY OVERRIDE
He then settled the remaining question directly: *"Yes, 237.2 is accurate so fine to stay, just good
for the cosmetic override on the trade desk."* So it landed WITHOUT a board rebuild — declared in
`docs/inputs/OWNER_DISPLAY_OVERRIDES.json`, applied at publish time by
`extract_board_view._apply_pool_override`, carried in the bundle stamp as `pvcPoolOverride`, and
guarded by `release_seam.test.js`. The engine keeps deriving 237.2; only the display moved. Full
record in `docs/pending/POOL_VALUE_150_OWNER_OVERRIDE.md`, including the full-act route that was
NOT taken and why.

**NOTHING IN THIS DOCUMENT IS OUTSTANDING.** All thirteen UI items, both bugs and both flags are
closed. What follows is the record.

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
    node ui/tests/release_seam.test.js           41
    node ui/tests/ui_defects_2026-08-21.test.js  180
    node ui/tests/counting_rule.test.js          31
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

**Both flags in this section are now closed.** They are kept, with their answers, because a closed
flag deleted is a question somebody re-asks.

* **`ui/app/positions_data.js`'s stamp — CLOSED 2026-08-31.** The earlier wording here called it the
  same class as the entry-price defect. It was not. The map is values-free (player key to position
  codes, off the owner's locations CSV), so a price move or a round advance moves the board md5 and
  leaves every code where it was; the stamp named the wrong dependency rather than failing. Measured
  at investigation: stamp said board `f2df6e0a`, live bundle `c8c2f2b6`, coverage 804/804 with no
  stragglers — a stamp claiming a staleness that did not exist.
  The stamp now names its REAL dependencies — the roster (the board's player-key set) and the CSV's
  md5 — via `ui/tools/positions_identity.py`, and `counting_rule.test.js` recomputes both in node
  from the same raw bytes. The board it was built against is retained as `builtAgainstBoard` and
  LABELLED provenance-not-dependency in the artifact itself, because the obvious "fix" for the
  mismatch — a board pin in the reader — would have taken the pocket panel dark on every landing.
  **DELIBERATELY NOT a landing writer.** It could be one, and it would be idempotent, but
  `extract_positions.py` HALTS on a join gap: a landing that adds a player before the CSV is
  re-couriered would abort on it. The suite catching a roster drift is the right guard; an abort
  path added unprompted is not. Revisit only if a roster change ever ships stale in practice.
* **2027 late-round picks pricing above the same round's 2026 picks — RULED INTENDED**, owner,
  2026-08-31, verbatim: *"The 2027 late round picks thing is fine, a chance at a higher pick is
  worth more than a #64 this year."* The mechanism is his year rule pricing an unresolved 2027 pick
  off the ROUND AVERAGE rather than a known finishing position, and that average legitimately beats
  a known-late 2026 pick, because an unresolved pick still carries the chance of landing early. Do
  not "fix" this.
