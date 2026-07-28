# DIRECTIVE — Ownership and pick holdings become a live sidecar, so a trade costs nothing

**Status:** FIRED — owner word 2026-07-28.
**Seat:** one execution supervisor, cold, directing hands. Not #217 and not #225.
**Nature:** UI and inputs. **No valuation change. No store byte written by this job.**

---

## The problem, in the owner's terms

> Without a mechanism for me to locally change where players play and who has what picks easily, this is
> going to be a perpetual bother. As trades happen daily in this league.

Today a trade means editing the authored store and running the whole pipeline, because **ownership lives
inside the store** as `affl_team`. That is why trades don't get reflected and why club totals drifted.

**But ownership does not affect a single player's value.** Verified: `affl_team` appears nowhere in the
valuation path — the only mentions in `rl_export.py` are a comment stating it is a separate field left
untouched, and a default for phantom rows. It is presentation data sitting in a model artifact.

## The two lanes — this is the whole design

| lane | what's in it | cost of a change |
|---|---|---|
| **LIVE** | AFFL ownership (`affl_team`), club/pick holdings | an edit. **No build, no bake, no board move.** |
| **BATCHED** | positions (`present_position`, `future_position`, `drafted_position`) | engine run, board moves, one history column |

**Positions must not ride the live lane.** They feed valuation — change one and the board legitimately
moves. If positions share a lane with ownership, every trade triggers an engine run and you are back to
today's problem. Same source sheet is fine; two lanes out of it.

## What to build

**1 · An ownership sidecar the UI reads directly.** A small committed file — ownership by stable player
key, plus pick holdings by club. The browser reads it for club membership, club totals and any
ownership display.

**2 · Sidecar overrides, store falls back. Do not remove `affl_team` from the store.** Store authorship is
the owner's alone; deleting a field from it is not this job's to do. The UI reads the sidecar where a key
is present and the store where it isn't, so the sidecar can start partial and fill in. Retiring the store
field later is an owner act.

**3 · Pick holdings.** These already come through `docs/inputs/` via `ui/tools/ingest_inputs.py`, which is
close to the right shape already. Establish what actually flows today and report it before changing
anything — if it's already effectively a sidecar, say so and leave it, and just document how the owner
edits it.

**4 · The edit path.** The owner maintains a sheet tracking players, picks, pick valuation projections and
positions. State plainly how he gets an edit from that sheet into the sidecar — the fewest steps you can
achieve, and no engine run among them. If that means a small conversion script, write it and document it
in one page.

## The position cross-reference — and a trap with a precedent

The owner has flagged that some positional data in his sheet may be out of date against the store, so the
two need reconciling. **This is a report, not a write.** Produce a diff, hand it to him, and change
nothing.

**The trap:** the board and the store use different position vocabularies. A previous diff pass compared
board codes (`GEN_DEF`) against store codes (`GDEF`) and reported **556 false differences.** Map the
vocabularies before comparing, and state the mapping you used in the hand-back. A diff count with an
unstated vocabulary is worthless.

## The other half of the baked club file

#222 moved the player-side club metrics into the browser. The **PVC band-priced picks stay with the
ingest**, on the sound reasoning that a pick's price comes from the curve rather than the board, so that
side never went stale when the board moved.

**But a curve change is coming.** #225 re-derives the curve, and when it is adopted those baked pick
prices go stale in exactly the way the player side did. Two options; recommend one and do not decide it:

- compute pick prices in the browser from the shipped curve, closing the file out entirely; or
- make regenerating them a mandatory, named step of curve adoption, so it cannot be forgotten.

## What is NOT in scope

- **Any valuation change.** If your work alters a single player's value, you have left scope — stop.
- Writing the store. Reading it is fine.
- Positions as a live lane. They are batched, always.
- Anything #217 or #225 touches — the curve, the pool, the board, the histories.

## Hand back

On the issue. State: what a trade now costs, step by step, from the owner's sheet to the visible app;
which fields are live and which are batched; that no valuation number moved, with the evidence; the
position diff with its vocabulary mapping named; and your recommendation on the baked pick prices with
the reasoning, not a decision.
