# DIRECTIVE — The player card's weekly history, the Public navigation defects, and the tab tidy-up

**Status:** FIRED — owner word 2026-07-28.
**Seat:** one execution supervisor, cold, directing hands. Not the #217 engine seat.
**Nature: UI ONLY.** No store byte, no board byte, no engine file, no curve, no pricing logic.

Ten items from issue #139, grouped into three clusters that share files. They are bundled because
splitting them means three seats reopening `ui/app/main.js` in the same week.

---

## Why now

The Movers rework (#208) stored per-player history properly for the first time — value, rank and
positional rank for **804 players at every one of eight points**, and per-round scores in the
finalisation state. The player card has been carrying a placeholder waiting for exactly this. Nothing
here needs new data; it needs the existing data surfaced.

None of it touches anything the engine split (#217) touches. It can run alongside.

## CLUSTER 1 — The player card (#139 items 3, 17, 18)

**Item 3 · Replace the round-by-round placeholder.** `ui/app/card.js:111` currently renders
*"Round-by-round rating · reserved · wired in the weekly-loop phase."* Replace it with the real
history: rating, value movement, rank movement, positional rank movement, and score.

The data: `value_history.json`, `rank_history.json`, `pos_rank_history.json` under
`engine/rl_after/ingestion/`, each carrying 804 players across the eight points
(`14`…`20` plus `post-r19-redesign-1`). Per-round scores are in `finalization_state.json` under each
round's `played` map.

**Three things about that data, and getting them wrong produces a card that lies:**

1. **The valuation trace is complete and needs no caveat.** Every one of the 804 players has a value,
   rank and positional rank at every point, whether or not they played. A player who did not play
   still moves, because everyone else did. Do not gate the trace on participation.
2. **Score coverage is NOT uniform.** R15 carries 318 players, R16 319, R17–R20 405–410, because the
   early catch-up feeds were partial. **A player absent from an early round's score map did not
   necessarily miss the game — the feed did not carry them.** Show the score where it exists and leave
   it blank where it does not. **Never print "DNP" for a round whose data was never collected**: that
   asserts a football fact the data does not support. If you show a played/DNP indicator at all, it may
   only be shown for rounds with full coverage.
3. **`post-r19-redesign-1` is not a round and has no score.** It is the ITEM 411 D1/D2 restructure. It
   shows as value and rank movement, labelled as a model change, never as a week of football.

**Item 17 · Recent form in Public.** The Recent form section already exists at `ui/app/card.js:108`
and is not exposed on the public tier. This is an exposure change, not a build.

**Item 18 · Public / Working card parity.** Public may show draft pick, and rank **with its
denominator** (`rank X of Y`). The tier switch is `ui/app/main.js:34` (`s.tier === "public"`). Close
the gaps that are general player facts. Anything genuinely private stays hidden **by explicit
decision, named in the hand-back** — not by defaulting to hidden because it was easier.

## CLUSTER 2 — Navigation (#139 items 12, 16, 15)

All three are the same routing fault family, in `ui/app/board.js`, `ui/app/clubs.js` and
`ui/app/main.js`.

- **Item 12** — clicking a club profile in Public returns the user to the all-player list instead of
  the selected club.
- **Item 16** — clicking a player in Public does not open that player's profile.
- **Item 15** — universal Back: the Back control must return to the actual previous product page,
  including club→player and player→club, rather than being player-card-specific.

Fix all three together. Doing 12 and 16 without 15 guarantees someone reopens these files next week.

## CLUSTER 3 — Tabs and labels (#139 items 2, 13, 14, 5)

**Item 2 · Retire the Round review tab. Owner word 2026-07-28: "Movers is fine, round review can
go."** Remove the `["review", "Round review"]` entry from the tab list at `ui/app/main.js:62`, and
retire `ui/app/review.js` and its styles in `ui/styles/matchday.css`. Movers is the weekly-review
surface and survives. Update the references in `ui/PLAN.md` and `ui/README.md` so they do not describe
a tab that no longer exists.

**Items 13 and 14 · Rename and subtitle.** Board becomes **AFFL Rankings**. Each tab gets a subtitle
beneath the main title: AFFL Rankings → `Player Rankings` · Clubs → `Club Breakdown` · Player Card →
`Player Profiles` · Trade Desk → `Trade Desk` · Movers → `Weekly Review`.

**Item 5 · The duplicate Free agents category — DISPLAY ONLY, AND THIS ONE HAS A TRAP.**
The duplicate does not originate in the UI. **The authored store carries both spellings: 73 rows as
`Free agents` and 2 as `Free Agents`** (Liam Stocker and Tyler Brockman). Canonicalise for **display
and filtering only**, in the UI.

**Do not edit the store.** Store authorship is the owner's alone, and this job has no store authority
of any kind. Do not "fix" the two rows at source, do not regenerate the store, do not open it for
writing. If you believe the store is the right place for this, say so in the hand-back and stop.

## Explicitly out of scope — recorded so nobody folds them in

- **#139 item 7** (expose drafted / development / model / eligibility / future position on cards).
  This turns on the distinction between eligibility and model group, which is an open **ITEM 412**
  design question, and the future-eligibility instrument it needs **does not exist as a store field**.
  Not buildable yet.
- **#139 item 8** (exclude picks 65–80 from club pick totals). As of 2026-07-28 the national pick curve
  stops at pick 64 and everything past it is pool-valued by position — this is law in `RULEBOOK.md`
  v2.1 law 4. Picks 65–80 are no longer priced on the curve at all, so this item's shape changes once
  the engine split (#217) lands. Do not build it against the old structure.
- **Anything touching the pricing structure, the curve, the store, the board, or the engine.** That is
  #217's, and it is the one job in flight that writes those.

## Rules

- **UI only.** If your change requires a store, board, engine or curve write, you have left scope —
  stop and return it.
- Screen by re-running, never by reading. Every count names its denominator.
- The container shallow-clones by default — `git fetch --unshallow` before any ancestry claim.
- **Take current `main` in first, and do not build on a stale base.** A branch that keeps building on
  already-merged history conflicts with itself at merge time — both seats hit that on 2026-07-28.
  Diff against your branch's own merge base, never `main..branch`.

## Hand back

On the issue. State: what the card now shows and where each column's data came from; how you
distinguished "no score recorded" from "did not play", and on which rounds you show a played
indicator at all; how the restructure point is labelled; that all three navigation paths work in
Public; which Public/Working parity gaps you closed and which you deliberately left, with the reason;
and confirmation that no store byte moved.
