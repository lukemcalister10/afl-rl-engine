# DIRECTIVE — Four hand-maintained pins and guards that cannot fail

**Status:** FIRED — owner word 2026-07-28.
**Seat:** one execution supervisor, cold, directing hands. Not #217 and not #225.
**Nature:** infrastructure and guards. **No store byte, no board byte, no curve, no pricing logic.**
Runs alongside #217/#225 — it touches none of their files.

---

## Why these four are one job

Every one of them is the same shape: **a value a human has to retype whenever something moves, or a
check that structurally cannot notice when it's wrong.** This project has now been bitten by that shape
four times in two days — the four-surface panel re-pin (retired), a CI diagnostic carrying its own stale
board literal (fixed), and the two below, one of which **took the whole app down**.

The owner's test applies cleanly: these have a demonstrated ability to stop the thing working, because
one of them just did.

## 1 · `EXPECTED_BOARD` — it silently fail-closed the entire app

`ui/app/config.js` pinned `EXPECTED_BOARD: "fa172ac1"` while the shipped board and both bundles were
`8a38cca4`. The board moved twice after the pin was last set, the constant didn't follow, `ringFence()`
rejected the shipped board, and **every tab rendered the fail-closed panel.** The app showed nothing.
#222 re-pinned it and flagged it rather than retiring it, correctly, because retiring a guard is not a
seat's call.

**It is now the owner's call and the answer is: stop hand-maintaining it.** The ring-fence should compare
the loaded board against **the board of record read from the manifest** (`data/expected_boot.json`
`board`), not against a constant someone remembered to update. The check keeps its job — a bundle that
doesn't match the board of record still fail-closes — and loses the failure mode where the *pin* is the
thing that's wrong.

If reading the manifest from the browser isn't available, derive the constant at bundle-generation time
so it moves with the board in the same commit. **Do not leave a hand-typed board id in the app.**

## 2 · `release_seam.test.js` — it cannot fail

It **builds its fixtures from the pin**, so when the pin points at the wrong board the fixtures point
there too and the test passes. It passed throughout the outage above. That is the vacuity class, and it
was guarding the exact thing that broke.

Fix it so it can fail: the fixture's board identity must come from the **manifest or the shipped bundle**,
independently of the pin, so a pin/board disagreement is a red. **Prove it fails** by pointing the pin at
a wrong board and showing the test go red. If it can't be made independent, delete it and say so — a test
that cannot fail is worse than no test, because it reads as coverage.

## 3 · `bootstrap_env.sh` invokes bare `python3` against a cp312-pinned lock

The lock pins the cp312 numpy wheel; the script calls bare `python3` at its verify step and its install
step. On a container defaulting to 3.11 with `python3.12` present, it verifies and installs against the
wrong interpreter and then fails confusingly at the env-pin check. **This has cost two seats.**

`live-scoring.yml` already solves it by discovering `python3.12` by name. Give the local bootstrap the
same treatment. A container without 3.12 should then **halt immediately with a readable message** instead
of half-working — that is the intended outcome, not a regression.

**Never weaken the pin itself.** A different numpy wheel silently reorders the board.

## 4 · The env-pin guard cannot tell the two wheels apart

`bootstrap_env.sh`'s `verify()` checks two things: `np.__version__ == 2.4.4`, and the sha256 of the
bundled OpenBLAS `.so`. **Both are identical across the cp311 and cp312 builds of the same numpy
version** — so the guard cannot detect the wheel swap it exists to detect. That is the exact defect it
was written to catch.

Close it **without adding a hand-maintained constant.** The installed distribution's own `dist-info`
records its wheel build tag; read that and assert it is the cp312 build. pip already wrote it, so there is
nothing new to re-type when numpy next moves.

**Prove it can fail.** Show the check going red against a wheel it should reject. If you cannot construct
that case in this container, say so plainly rather than declaring the guard sound.

## What is NOT in scope

- The store, the board, the curve, the pricing layer, the histories, the movers bundle.
- Anything #217 or #225 touches.
- Adding any new guard beyond the two repairs above. **Before adding a guard, price its upkeep** — that
  is the standing rule and it is what produced three of these four defects.

## Hand back

On the issue. For each of the four: what changed, and **the evidence that the check can now fail** —
shown failing, not argued. Name any of the four you could not do and why. If a fix would require a store,
board or curve write, stop and return it.
