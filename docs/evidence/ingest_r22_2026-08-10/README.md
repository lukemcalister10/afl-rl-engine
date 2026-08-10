# Round 22 ingestion — evidence tree (2026-08-10)

The owner's round-22 scores applied to the live store on main, and the ONE comparison he asked for:
the round-21 board next to the round-22 board.

Owner's rule for the output (issue #334, comment 5235125560), verbatim:

> "the only comparison I want is to be able to see the before/after of round 21 and round 22... just
> need an apples for apples round 21 to round 22 rankings comparison to see who's changed."

So that is what is here, and nothing else. No earlier board was re-computed. No dial moved. No
re-derivation. The two boards are one store step apart and everything else about them is identical.

---

## What moved

| | before | after |
|---|---|---|
| store `engine/rl_after/rl_model_data.json` | `37ced3ce45914e6feb00d27e26922e9a` | `0dd6b4a01e16dabf8d3a388d8f8ac1f2` |
| board `data/rl_build/rl_app_data.json` | `113b36f898a32363c49c2a62fb809f4b` | `6e724cca2bb2fb118ff7ad6ed1f8a4b6` |
| balanced (sibling) board | `123deccb0838c7370ce614d7f4310b01` | `b4cc0b2b7e4fb0552e9457f2d249cf52` |
| season round | 21 | 22 (calendar progress 0.92) |
| applied-rounds ledger | 2,677 entries | 3,086 entries (+409) |

Source file: `scores/R22.csv` — the owner's couriered file, **byte-unmodified**,
md5 `82b456d5675c18b137180416b82432fc`, sha256 prefix `c8f3748462d0`, 409 rows.

## The files

| file | what it is |
|---|---|
| `R21_vs_R22.md` | the readable comparison: the headline counts, top 20 risers, top 20 fallers, top 20 rank climbers, top 20 rank sliders |
| `board_R21_vs_R22.csv` | **the full board** — all 804 players, rank before, rank after, value before, value after, change, percent — sorted by the size of the move |
| `R21_vs_R22_summary.json` | the same figures as data |
| `compare_r21_r22.py` | the recipe that built the two files above, re-runnable |
| `r22_resolution.json` | every one of the 409 rows: file name, score, the player it attached to, and how it resolved |
| `r22_absent.json` | the 395 active players not listed in the file (did not play, by the standing rule) |
| `resolve_table.py` | the recipe for the two files above, re-runnable, read-only |
| `preflight.txt` | the read-only preflight, run before anything was written |
| `apply.log` | the full apply transcript |
| `gate_*.txt` | the gate outputs (see below) |
| `PINS.md` | every identity that moved, before and after |

## Identity — how the 409 names were matched

409 rows listed, 409 resolved, **409 different players**, zero unresolved, zero ambiguous, zero
duplicates, zero rows dropped. Only **two** rows in the whole file are spelled differently from the
store, and both are covered by the owner's own standing identity rules:

| file name | score | attached to | store name | AFL club | how |
|---|---:|---|---|---|---|
| Bailey Williams | 97 | `bailey-williams-wc` | Bailey J. Williams | West Coast | owner ruling 2026-08-10 |
| Bailey Williams | 89 | `bailey-williams-wb` | Bailey Williams | Western Bulldogs | owner ruling 2026-08-10 |
| Callum Brown | 77 | `callum-brown-ire` | Callum M. Brown | GWS | standing rule (2026-07-20) |

Every other row matched the store's display name letter for letter.

### The Bailey Williams question, and how it was settled

The round-22 export **regressed**: it writes both Bailey Williams players under the one bare name
"Bailey Williams" (97 and 89). Rounds 20 and 21 wrote them apart ("Bailey Williams" and "Bailey J.
Williams"), matching the store exactly, which is why the disambiguation rule had been retired.

With the rule retired, both rows resolved to the Bulldogs man, and the preflight **halted** on a
duplicate stable-key assignment. That halt is the guard working. Nothing in the file and nothing in
the store distinguishes the two scores, so the seat refused to guess and put the question to the
owner.

**His word, verbatim: "97 = West Coast, 89 = Bulldogs".**

That ruling is recorded in `engine/rl_after/ingestion/catchup_identity_overrides.json` as a
(round, score) mapping scoped to round 22 only — the identity record, not the data. The owner's score
file is untouched. The retirement of the rule still stands for any round whose export writes the two
players apart.

## Absences

395 of the 804 active players are not in the file. Under the standing owner ruling (2026-07-20) file
membership defines participation: a player absent from a round file **did not play** — nothing is
appended, no game is added to any denominator, and absence is not an unresolved-input condition. So
there is no such thing as a store player who played round 22 and is missing from the file: the file
IS the record of who played. All 395 are named in `r22_absent.json`.

## Gates

| gate | result |
|---|---|
| catch-up preflight (read-only, before any write) | CLEAN — 409/409 resolved, 0 duplicate, 0 ambiguous, 0 unresolved |
| transaction status | COMMITTED, `failure: null` |
| Guard 5 boot-store, inside the transaction | GREEN |
| Guard 5 boot-store, independent re-run on the landed store | PASS — store `0dd6b4a0` == pin, rl_model `33f94073` == pin, fv `d920557e` == pin |
| identity carriers moved together | 17 of 17 targets staged and swapped in one transaction |
| numéraire | PICK 1 = **3000** (unmoved) |
| ledger | 3,086 entries = 2,677 + 409, no double-count |
| finalization | FINALIZED (movers report + UI bundles + round-delta injection all completed) |
| catch-up preflight suite | 5 / 5 PASS |
| movers transition suite (Python) | 39 / 39 PASS |
| movers suite (JS) | 66 / 66 PASS |
| F1 export↔engine parity (board v == freshly recomputed gated `ev()`) | **PASS, 0 mismatches** across 804 |
| F2 book↔board parity (book cur == board v) | **PASS, 0 mismatches** |
| one-source self-test | **PASSED — 142 PASS / 0 FAIL / 0 STALE** (see the note below on the count) |
| Guard 4 correction-sticks canary (full rebuild, sentinel) | **PASSED** — a source correction reaches board and book |
| Guards 1–3 (derived read-only, source-md5 stamped, single source, no lookalikes) | PASS |
| board re-derivation from the landed store, clean workspace, off the transaction | **reproduced `6e724cca2bb2fb118ff7ad6ed1f8a4b6` BYTE-EXACT** |

### The self-test count moved 144 → 142, and here is exactly why

Nothing was weakened, nothing failed, nothing went stale. The self-test emits some checks only when
the data puts them in scope, and two went out of scope this week:

- The "#326 currency end-to-end" check is emitted only for a level whose named live entrant re-prices
  **via the floor**. Two levels changed route this round: **PDA** (now Sam Wicks via the ruck cap,
  was Harry Cunningham via the floor) and **UNR** (Mark Blicavs, floor → ruck cap). Their two
  currency checks therefore did not apply. Both levels are still checked by the "reaches a real
  entrant's BOARD price" assertion, which passed.

That is 144 − 2 = 142. (The 144 of record was itself 145 − 1, the owner's Kako anchor retirement on
2026-08-06, commit `1ec4773`.) The route change is a normal consequence of prices moving; it is named
here rather than absorbed silently.

### Two test files were bumped, exactly as every weekly round bumps them

`engine/rl_after/ingestion/test_movers_transition.py` and `ui/tests/movers.test.js` carry
round-advance expectations that name the current round. They are bumped every week — the round-21
landing did the same (commit `441a6f4`, "four round-advance expectations bumped, future-append fixture
moved to R22"). Here: the manifest round expectation moves 21 → 22, the future-append fixture moves
R22 → R23, and the production bundle now carries R15–R22 (eight reports). No assertion was weakened
and none was removed; each still fails if the thing it names is wrong.

## Cross-check

The comparison in `board_R21_vs_R22.csv` was checked player-by-player against two independent
records the system wrote for itself:

- `engine/rl_after/ingestion/value_history.json` — 0 value mismatches across 804 players, both rounds;
- `engine/rl_after/ingestion/movers/movers_R22.csv` — 0 mismatches on value before, value after,
  rank before and rank after, across all 804 players.

Ranks are the board's own published overall ranks (`rank_history.json`), not recomputed here — which
is what keeps the two columns apples for apples.

## Scope fence

This act touched main's store and the artifacts derived from it, and nothing else. No dial, no curve,
no surface, no engine maths. The stage-B act branch, the two read-only audits and the tables job are
untouched; the act re-bases later at adoption, as normal.
