# PENDING ACT — POOL PICK VALUE 237.2 → 150, OWNER OVERRIDE

**Status:** ruled, not yet applied. Rides on the next act that rebuilds the board (FW2 expected).

## The ruling, verbatim

> "On the trade desk, the pool pick is set at 237 when pick 64 is now at 177 so I'm not sure that's
> accurate. Can we just set the pool pick value to 150 for now as a stop-gap"

and, after being shown why the derived value legitimately sits above pick 64:

> "override it to 150 please, noting it's an owner override and knowingly isn't derived."

## What is being overridden, so the override can be read against it

The derived pool level is **237.2** and it is not a defect. The pool is not "pick 65": it is the whole
population off the national curve — national 65+, the entire rookie draft, the pre-season draft and
every pickless mechanism — valued by position, with order of selection carrying no value. Its ladder
level reflects that population and legitimately beats the last national pick (177.8). The seam ruling
of 2026-08-06 says exactly this and refuses to read index 65 as a curve step.

The owner was shown that reasoning in those terms and ruled 150 anyway. This is a **stop-gap by his
own word**, not a re-derivation: nothing is refitted, and `pool_value_derived: 237.2` is retained
beside the override so it can be undone by deleting three keys.

## Blast radius, measured

* **No player valuation moves.** `pool_value` RETIRED FROM PRICING under the owner ruling recorded at
  `_merged_recover.py:3342` (addendum 5 item 3) — a pool entrant's entry anchor comes from
  `MA.pool_v0_of` (pathway × position), not from this scalar.
* **No club rating moves.** The 48 ledger picks past #64 are all round-5 and carry value 0, so they
  never consult the pool level.
* **Only the trade desk reads it**, as the "Pool pick — position-blind level" item.

## Why it is not a text edit

The pick curve — including index 65 — is **baked into the board**: `data/rl_build/rl_app_data.json`
carries a 65-entry `PVC` table (`64 = 177`, `65 = 237`), and `extract_board_view` publishes it from
there, not from the curve artifact. So editing `engine/rl_after/pvc_curve_v2.json` alone would leave
the input saying 150 and the shipped board saying 237 — an input/output divergence with no guard on
it, which is worse than the number being wrong.

**It must therefore be an ACT**: curve artifact + board rebuild + the landing transaction. Expected
shape: board md5 moves, **0 player movers**, one out-of-round column.

## The edit to make, when the act runs

In `engine/rl_after/pvc_curve_v2.json`:

    "pool_value": 150,
    "pool_value_derived": 237.2,
    "pool_value_override": {
      "value": 150, "supersedes_derived": 237.2, "date": "2026-08-31",
      "authority": "OWNER OVERRIDE — knowingly NOT derived",
      "owner_word": "override it to 150 please, noting it's an owner override and knowingly isn't derived."
    }

Check afterwards that `data/rl_build/rl_app_data.json`'s `PVC["65"]` reads 150 and that the movers
report for the act shows zero player movers. A player mover means `pool_value` has crept back onto
the pricing path and the act should abort.

## Why this file exists

The edit was made on 2026-08-31, verified, reported to the owner as done — and never committed. The
container was reclaimed and the working tree came back from origin, taking it with it. A ruling that
lives only in a working tree is a ruling that has not been recorded.
