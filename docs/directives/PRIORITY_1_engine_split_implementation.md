# DIRECTIVE — Implement the ruled pricing split in the engine

**Status:** FIRED — owner word 2026-07-28. **This one writes the store and the board.**
**Seat:** one fresh execution supervisor, cold, directing hands. Not #207 and not #208.
**Sequencing:** read in and prepare now; **do not move the board** until #208's three closing tasks
have landed — the schema-version bump, the Bailey Williams override retirement, and the removal of the
four-surface panel re-pin. The panel one matters to you directly: until it is gone, every board move
costs a hand-typed re-pin across four surfaces, and this job moves the board.

---

## Why this comes before more measurement

The owner has ruled the pricing structure seven or eight times, and seats keep returning questions that
assume picks past 64 are priced. The cause is not comprehension. The old structure is implemented in the
code, in every artifact shaped 1–99, in the tests, and across the register; the new structure exists in
owner rulings and one page of `docs/CURRENT_STATE.md`. A seat doing work reads code and artifacts, so it
rebuilds the old model from the material in front of it. The ruling loses to the code.

This job makes the ruling true in the place seats actually read. Everything measured before it is
measured against a structure that does not exist.

## The structure, and it is already ruled — you are not designing it

**The national curve stops at pick 64.** Everything past 64 enters a **pool**: ND 65+, all rookie draft,
all post-draft selections. Valued **by position**. **Order of selection is irrelevant inside the pool.**
SSP and MSD are valued at the pool but tracked separately.

**There is no price for pick 70.** A player taken there is priced from the pool by position, not from a
curve. If your work produces a value indexed to a pick number above 64, you have reverted to the old
model — stop and re-read this section.

## The work

**1 · Remove the chaining.** `rl_model.py:209` and `:215` give RD and PSD entrants an effective pick of
`last_national_pick + their_pick`, putting them on the same ladder as national draftees. Both go.

**2 · End the curve at 64.** The pick curve covers picks 1–64. Nothing past it.

**3 · Give the pool one index.** Every pool player sits at a single index. Do not build a positional
valuation path — **one already exists**: `iso_corr(pos, pk)` takes position and pick, and
`_v0_curve_assert` asserts V0* is a function of `(pos, ageR, pick)`. A key forward at pick 1 is already
priced differently from a midfielder at pick 1. One index plus the existing position layer gives you one
value per position, which is exactly the ruling. What is position-blind is only `_PVC0`/`draftval`, the
raw pick ladder underneath — that is not the layer that prices players.

**4 · Do not re-derive `national_draft_last_pick.json`.** Lines 209 and 215 are its only consumers and
both are being removed.

## G-MONO — read this before you touch the curve

`docs/RULEBOOK.md` §4: *"THE CURVE DESCENDS (G-MONO). The pick curve is strictly decreasing; pick 1 =
3000 exactly."* That is law. The engine's own assert (`rl_export.py:137`) is weaker — `>=`, non-increasing
— so the code will not stop you breaking the rule. The rulebook will.

Under the ruled structure the pick curve is 1–64 and descends, and the pool is a value per position not
indexed by pick, so **G-MONO is satisfied as written and no amendment is needed.** That reading is with
the owner for confirmation.

If your implementation finds itself needing the rule changed, **stop and return it.** Rulebook wording is
a Law-10 act: exact wording pre-filed, owner's explicit word, never a seat decision.

## The fence — this is the part that has failed repeatedly

**Implement exactly what is ruled and decide nothing else.** Anything you find yourself *choosing* —
curve family, era handling, how the boundary is measured, how the replacement bar is keyed — belongs to
ITEM 412 and goes back to the owner. It is not yours to settle because you happened to reach it.

## Sequencing — why you cannot start yet

This job re-prices every player and **moves the board**. That is the same out-of-round board move that
broke the Movers chain and left round 20 unfinalised. #208 is currently finalising R20 and building a
history column against the current board; landing this underneath them invalidates their column
mid-flight and recreates the failure.

**Wait for #208 to land.** Its from/to work is the prerequisite that makes the board safe to move at all.

When you do move the board, the standing rule applies: **write a history column at that point**, so the
Movers tab can compare across it. The column's label is owner-set — ask for it, do not invent one.

## Rules that still apply

- Run `bash bootstrap_env.sh && bash bootstrap.sh` first and never bypass the pin — an unpinned numpy
  silently reorders the board. If it fails, say so and stop rather than working around it. Note the known
  fault: the script invokes bare `python3` while the lock pins the cp312 wheel.
- Screen by re-running, never by reading. Every figure names what it was measured on and how many rows.
- The container shallow-clones by default — `git fetch --unshallow` before any ancestry claim.
- Take current `main` in before you start.

## Hand back

On the issue. State: that lines 209 and 215 are gone and what replaced them; the curve's last pick; the
pool index and the per-position values it produces; the board before and after; the history column you
wrote and its label; and any point at which you had to choose something rather than implement it.
