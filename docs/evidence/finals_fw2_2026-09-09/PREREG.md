# PREREG — FINALS WEEK 2 · 2026-09-09

## What this act is

183 players at eight clubs played a final. Each gains **one game** and a **re-averaged 2026 season
row**. That is the whole change to the store.

It is the same act as FW1, second week — and the first finals week landed by **following the
runbook** rather than discovering it. `docs/evidence/finals_fw1_2026-08-30/RUNBOOK_finals_week.md`
is the procedure; this file is that procedure's output, not a fresh derivation.

## The scores

`scores/FW2.csv`, as the owner sent it, byte for byte — 183 rows, sha256
`adc1afb6d7a1e2701f161d0bfb2b93ce5c5d6207041e89873ae31f31df776478`.

**Three name questions, all settled before anything was priced:**

* **Bailey Williams** — the owner named him: *"Bailey Williams is the Western Bulldogs one."* The
  store carries exactly one Bailey Williams, `bailey-williams-wb`, at the Western Bulldogs. The
  general resolver lands on him without help, so the disambiguation confirms the resolution rather
  than correcting it. No override needed, and none added — an override that changes nothing is a
  place for a future error to hide.
* **Alex N-Bullen** and **Hugo H-Kahan** arrive abbreviated and match no store row. Expanded to Alex
  Neal-Bullen and Hugo Hall-Kahan in the plan's `OVERRIDE` map and in the report emitter's
  `ALIASES` map — never in the CSV, so the source file stays exactly what he sent. The two maps
  cannot silently disagree: a name that reached the store under one key and is reported under
  another fails the report's reconciliation.

All 183 resolve to distinct, non-retired store keys, each with exactly one 2026 season row.

## The fixture, derived rather than typed

`scores/fixtures.json` week 26 declares eight clubs: Adelaide, Brisbane, Carlton, Fremantle,
Geelong, Hawthorn, Sydney, Western Bulldogs. That list is **read off the resolved players**, not
entered by hand.

Three listed players sit at a ninth, tenth and eleventh club in the store — Josh Battle (St Kilda),
Jack Ginnivan (Collingwood), Oscar Allen (West Coast). They are **not** evidence those clubs played:
all three have since moved to a club that is in the list. `afl_club` is an identity field, stale for
them, and nothing reads it to price anybody. The fixture entry exists only so that ABSENCE from a
finals score file can be told apart from "your club was not in it" — it is not an input to the edit.

## The edits

    366 edits over 183 players
      scoring[2026].games   g  ->  g + 1
      scoring[2026].avg     a  ->  round((a*g + score) / (g+1), 2)

and nothing else. The career `games` field is deliberately NOT touched: `_merge_into_store`
(round_apply.py:185) does not touch it either, and an edit that also moved it would be a second
writer inventing a rule the ingestor never had.

The averages come from the ingestor's own `_mean` at the ingestor's own `ROUND_DECIMALS = 2`,
called rather than restated.

## Why it is a store edit and not a round

Unchanged from FW1, and not re-opened here. The owner, 2026-08-30: *"We're literally just updating
player averages and game counts."* The store has always agreed — Bontempelli's 2016 row reads 26
games, 22 home-and-away plus four finals.

**A store edit does not recompute season state. It holds it.** Which is now a law rather than a
side effect: the owner, 2026-09-02 — *"The calendar can never get above 1. It gets there at r24 and
holds"* — and `derive_season_state` HALTs on any `calendar_progress` outside (0, 1.0].

## The prediction

`board_after` is null: a board priced from scores nobody has put through the real builder cannot be
predicted without running it, and copying it out of a build already run is not a prediction.

`expected_movers` is the falsifier. The plan measures it on a loaded engine whose control pass
reproduces the live board with 0 diffs — **and it will still be wrong**, because pricing in memory
cannot reproduce the LOAD-TIME CALIBRATION REFIT. FW1 predicted 86 movers and a ripple of exactly
zero; the builder found 234, of which 146 had not played. The first flight is therefore expected to
ABORT on the declaration and restore every carrier byte-exact. That is the falsifier working, and
the measured list is declared for the re-flight, which asserts determinism instead.

### Measured — filled after the first flight

*(pending)*

## What must hold

`as_of_round` is declared UNMOVED, and so is every model pin. The calendar does not move because
nothing in this act asks it to.

## The movers list, and this week's place in it

Owner, 2026-09-02: *"FW1 should be the last point in the moves list. Treated like r23 or r24."*
FW2 takes that place and FW1 becomes the second-last. Three things close this act, all of them in
runbook step 5 and none of them optional:

1. **The weekly report** at feed round 26, emitted from the flown edit and reconciled score by
   score. Without it the week's scores appear nowhere and the retrospective cannot subtract the
   game — the two faults that cost a full re-price at FW1.
2. **The retro window** extended to `ROUNDS 14..26`, calendar clamped at `min(R, 24)`, re-priced on
   ONE engine load. The control is the last round: re-pricing FW2 from the truncated store must
   reproduce the live board with 0 diffs.
3. **The series re-emitted**, because every act that rebuilds the bundle drops it.

Verified afterwards, on a real player, at the numbers: a finalist's game count must read the true
as-at count at every round, and the finals point must equal the live board.
