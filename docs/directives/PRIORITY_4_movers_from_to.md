# DIRECTIVE — Movers tab becomes a from/to comparison, and Round 20 finalises

**Status:** FIRED — owner word 2026-07-28. Pre-fire audit waived by owner: this changes a view and the gates on that view; the store and board are not written by any of it.
**Supersedes:** the "restructure bundle entry" ruling of 2026-07-28. Do not implement that ruling.
**Seat:** the live #208 execution supervisor. Continues on `claude/item-208-r20-go-live-61dssq`.

---

## Why this exists

The Movers tab is built as a chain: each round must start from the board the previous round
finished on. That assumption holds only if the board never moves except by applying a round. The
board *has* moved outside a round — the ITEM 411 D1/D2 restructure — so round 20 cannot attach to
round 19, and finalisation refuses. It refuses correctly.

This is not a one-off. The re-derivation will move the board outside a round, and so will ITEM 412.
Every future round would inherit the same break. Patching the chain buys one round at a time.

The owner's decision is to replace the chain rather than repair it. The Movers tab becomes a
**from/to comparison**: pick two points, see what changed between them. A comparison that names its
own two endpoints does not need a chain, an integrity flag, or a provenance bridge to be trustworthy.

## The earlier ruling is withdrawn — do not add a synthetic bundle entry

An earlier instruction was to generate the `92a8f3a0 → fa172ac1` jump as its own entry in the movers
bundle, labelled as the restructure. **Do not do this.** The seat that pushed back was right: that
jump already has an owner-approved representation in `ui/data/movers_transition.js`
(`source.board 92a8f3a0…` → `destination.board fa172ac1…`), and a synthetic round entry would be a
second, contradictory answer to a question already settled.

## The data already exists — verified, do not re-derive

All three histories under `engine/rl_after/ingestion/` hold **804 players across rounds 14–20**:

| file | players | rounds held |
|---|---|---|
| `value_history.json` | 804 | 14,15,16,17,18,19,20 |
| `rank_history.json` | 804 | 14,15,16,17,18,19,20 |
| `pos_rank_history.json` | 804 | 14,15,16,17,18,19,20 |

Measured on `3a18ea2` (round 20 applied). On `0b48d9c` the same files hold 14–19. Any two of these
columns can be compared by direct lookup. Nothing needs deriving to compare round to round.

## The work

**1 · Store a column for the post-restructure point.**
The histories go straight from 19 to 20; there is no column at the board the restructure left behind
(`fa172ac1`). Compute it once from the two board files — both exist in history — and store it as an
additional column alongside the numbered rounds, so it is selectable like any other point.

**Its label in the dropdown is `Post R19 Redesign 1` — owner-set, use it verbatim.** The trailing
numeral is deliberate: the re-derivation and ITEM 412 will each add another such point.

Then make it a standing rule: **whenever the board moves outside a round, write a column at that
point.** That is what keeps the dropdown honest, and it is cheap — it is a snapshot of current values,
not a derivation.

**2 · Parameterise the producer.**
`round_movers.build_report` hardcodes `prev_round = round_n - 1` (`round_movers.py:231`). Make the
comparison point an argument so the producer can diff any two stored columns. The rest of
`build_report` already reads from the histories via `by_round(...)` and needs no change in kind.

**3 · Two dropdowns in the tab.**
From and to, over every stored point — rounds 14–20 plus the restructure column. Default to the two
most recent, so the tab's normal behaviour is unchanged for ordinary use.

**4 · Remove the chain machinery.**
It exists to police a fixed consecutive series. It has no job under from/to, and item 4 is what is
currently blocking round 20:

- `round_movers.accumulate_bundle` — the chain walk and the `integrity.board_chain_ok` flag
  (`round_movers.py:522-534`)
- `round_finalize` — the bundle chain / anchor / round-presence checks (`round_finalize.py:396-417`)
- `ui/app/movers.js` — the consecutive board-and-store continuity loop, the `previous_round == round - 1`
  rule, and the `board_chain_ok` rejection (`movers.js:24-27`, `:250-267`)

Delete rather than loosen. A check that cannot fail is worse than no check — that is a named hazard on
this project. Owner word 2026-07-28: these are removed, not weakened.

**Put one assert back in their place:** the newest stored column matches the live board. Five checks
out, one in, and it needs no hand-typed pins. Prove it can fail before you land it.

**The transition record stays — its enforcement goes.** `ui/data/movers_transition.js` is owner-approved
and is not deleted. Remove `bridge()` and its call site in `ui/app/movers.js`, and keep the record as
the machine-readable statement that the model changed between board `92a8f3a0` and `fa172ac1`. The tab
reads it to decide when a selected range needs the model-change label. Future out-of-round board moves
add an entry to it — it becomes the register of those moments, not a gate.

**5 · Finalise round 20.**
Once item 4 lands, finalisation has nothing left to refuse on. Run it, and confirm the tab shows
round 20.

## Rules that still apply

- **Label a range that spans a model change.** If the selected from/to crosses the restructure, part
  of the difference is the model, not the players. The tab must say so on those ranges. A label, not
  a gate — it never blocks the comparison.
- **Never hand-edit `ui/data/movers.js`.** Its own header says so.
- **`3a18ea2` is not merged as a finished round.** It carries a bundle stamped `board_chain_ok: false`.
  Whatever lands must land as a complete change, not as that commit.
- Take current `main` in first. The branch sits on `9345881`, five commits behind `0b48d9c`.
- Screen by re-running, never by reading. Every figure names what it was measured on.

## Hand back

On the issue. State: the restructure column's stored values and how they were computed; that rounds
14–20 plus the restructure point are all selectable; that round 20 is FINALIZED; and what the tab
shows for R19→R20 and for R14→R20.
