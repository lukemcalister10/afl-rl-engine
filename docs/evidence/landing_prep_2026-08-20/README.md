# THE LANDING PREP — land/order-29, 2026-08-20

**Ordered at register v778. The pre-word mechanics only: the C3 six-pin re-key, the book re-seal, and
the final all-green verification.**

> ## THIS IS NOT ADOPTION
> Nothing is merged to main. Nothing is tagged. Nothing is promoted. The live board `88ce647f` is
> **untouched**. **Tag push and main promote are OWNER-ONLY, and the owner has not given the landing
> word.** Every artifact here is candidate-state evidence for the supervisor and the owner to read
> *before* that word.

## THE CANDIDATE

| | |
|---|---|
| board | `a05fe951f78482c70520480e184c80ec` / 664,949 / 804 |
| engine | `5f434b9592ad8adb7dcd534da49df3c7` |
| store | `cb38ef1171dcf20aae66ebf12682be0d` (unmoved) |
| branch | `origin/land/order-29` @ `ba37032` |
| dial line | `docs/evidence/parity_2026-08-19/build_D7B.sh` (D5-final stack + `RL_O42=1 RL_O43=1`, U0=7) |

**First act of this seat: reproduce the candidate byte-exact.** Done, before anything was touched —
`a05fe951f78482c70520480e184c80ec`.

## WHAT WAS ORDERED, AND WHAT IT READS

| # | item | outcome |
|---|---|---|
| 1 | **C3 — the six-pin re-key** | **DONE.** 4 pins re-stamped, 2 traced already-correct. → `PINS_C3.md` |
| 2 | **Guard 5 green, verified** | **BOUND: PASS, every leg.** **UNBOUND: RED — the footgun is NOT dead.** Reported, not worked around. → `GUARD5_out.txt`, `BUILD_UNBOUND_out.txt` |
| 3 | **The book re-seal** | **HALTED.** The procedure needs a decision that is not in the record. No seal written. → `RESEAL_HALT.md` |
| 4 | **The final acceptance table** | **PRINTED.** → `LANDING_TABLE_out.txt` |

## THE TWO THINGS A READER MUST NOT MISS

1. **The unbound-surface footgun is alive.** `/home/claude/v0surf.pkl` (`fbc5b393`) sits ahead of the
   branch's own `data/v0surf.pkl` (`5dd34ca8`) in the engine's **own** precedence
   (`_merged_recover.py:1947`). A pin re-key cannot move a precedence that lives in engine code, and
   the C3 v0surf pin was **already correct**. **It is fail-closed at two layers** — Guard 5 names it
   before the build, and the engine's frozen-signature check halts the build at load time. The
   measured unbound build produced **NO BOARD**. No wrong board can be produced silently.
   *Finding:* `bootstrap.sh` does **not** seed `/home/claude/v0surf.pkl`, so the guard's own remedy
   line *"Re-run bootstrap.sh"* is wrong for this artifact.

2. **The book re-seal halted on a real fork**, not on a missing command. Three independent blockers,
   each measured rather than inferred. `data/book_stable_seal.json` is byte-unchanged.

## FILES

**The re-key**
* `PINS_C3.md` — pin-by-pin old→new disclosure, the surgical proof, and the one companion act
* `rekey_c3.py` — the re-key instrument (computes every value from the tree; never trusts the order)
* `REKEY_C3_out.txt` — raw dry-run + apply
* `sync_board.sh` — the `data/rl_build/rl_app_data.json` sync, per the `0260787` precedent

**Guard 5**
* `guard5.sh` — the boot form, three modes: `bound` / `unbound` / `literal`
* `GUARD5_out.txt` — raw, all three
* `build_unbound.sh`, `bbD7_unbound.sh` — the unbound-surface candidate build (one-line diff from `bbD7.sh`)
* `BUILD_UNBOUND_out.txt` — raw

**The book**
* `RESEAL_HALT.md` — the halt, the three blockers, and the three questions the supervisor must rule
* `reseal_probe.sh` / `RESEAL_PROBE_out.txt` — both arms run, raw halts recorded

**The table**
* `landing_table.py` — scrapes every verdict from raw files; nothing typed in
* `LANDING_TABLE_out.txt` — **the deliverable**
* `IDENTITY_CHAIN_out.txt` — the full 7-board identity chain, re-run on the re-keyed branch
* `carried/` — the v777 probe-repair readings (burn, birthday axis), copied unmodified with md5s

## HONESTY NOTES

* **Depths as depths.** No item was upgraded to green because the rest of the table was green.
* Rows the table marks **CARRIED** were *not* re-measured in this seat; they are prior raw outputs,
  md5-recorded, on the board this seat reproduced byte-exact. Rows marked **RE-MEASURED** were run here.
* **No engine edits.** Nothing under `engine/` was modified. Where an item would have required one,
  it halted and is reported.
* **Nothing outside the repo was deleted or modified** to make any check pass.

---

**NOT ADOPTED. OWNER WORD PENDING.**
