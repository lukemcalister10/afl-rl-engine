# M1a — THE VERDICT SPINE. Evidence, 2026-08-20

Build seat for M1a of the modernisation programme. Register v785 commissioned it; register v787 —
the CI-estate audit — is its requirements document.

Tree measured: `origin/main` after the apply/completion seat's final push (register v788).
Store `cc02567f` · board `a05fe951` · engine_head `5ac6780f` · rl_model `6fe7c415` · fv `6e9a370e` ·
config `eed19a75` · register `652d83e8` · as_of_round 22.

**The live board `a05fe951` did not move.** Nothing in this order writes a board, a store, a pin or a
carrier. Every check reads, hashes and compares; the engine was exercised only in an isolated
workspace seeded from the checkout.

---

## Files

| file | what it is |
|---|---|
| `runner_table.txt` | **the one table**, on the live tree. 7 checks, PASS 7, exit 0 |
| `runner.json` | the same rows machine-readable, plus the halted-carrier ledger |
| `checks/*.txt` | the raw output each verdict was read off — one per registered check |
| `spine_selftest.txt` | the runner's self-test: a forced failure in **every** registered check, 45 PASS / 0 FAIL |
| `release_manifest.txt` / `.json` | the widened coherence gate: 40 carrier fields, 8 identities, 7 files |
| `build_lock_proof.txt` | seven lock behaviours, including the required waiting message and a fail-closed timeout |
| `template_selftest.txt` | the slot validator refusing every failure mode, 34 PASS / 0 FAIL |
| `oneliner_a_gamma.txt` | before/after — `ship_gates_check.py` RL_GAMMA, exit 1 → exit 0 |
| `oneliner_b_fixture.txt` | before/after — `scratch_fixture.py` R14 config coherence, exit 1 → exit 0 |
| `oneliner_c_f1lens.txt` | before/after/non-vacuity — the self-test F1 lens fix, 96 → 0 → 1 |

---

## The design principle, standing up on its own

The audit's closing instruction was the order's whole point:

> "The verdict spine's job is to make that legible — one halted carrier, named once, with everything
> downstream of it reported as *blocked* rather than as thirty independent failures. That legibility
> is the deliverable, not a green wall."

The first run of the runner, on the tree as it stood before the completion seat landed its contract
re-stamp, printed exactly that shape:

```
release_manifest         RULED-RED   4 of 40 carrier fields drift, all covered by presented ruling R2
release_contract_seal    BLOCKED     carrier release_contract:engine_head halted by release_manifest
...
AGGREGATE  7 checks  |  PASS 4  FAIL 0  BLOCKED 1  RULED-RED 1
VERDICT    GREEN — no gating failures.
```

`release_contract.py check` **does** fail on that tree, for four stale pins. It is not reported a
second time. R2 was a fork already presented to the owner, so it is non-gating and not a seat's to
clear. One cause, one row.

The table on the current tree is all-PASS because the completion seat repaired R2 while this order
was being built — which produced the other thing worth recording here.

## The ledger expired itself, unprompted, within the hour

`acceptance/ruled_red.json` is the machine-readable known-red list `AUDIT_CI.md` §5/RETIRE asked for
by name. Every entry is **self-expiring**: the moment its carriers become coherent the entry stops
matching and the runner **fails on the stale entry itself**. That fired for real, on the first repair
that happened after it was written:

```
release_manifest  FAIL  STALE RULED-RED ledger entry R2-release-contract-code-identities —
                        its carriers are coherent again, retire it from acceptance/ruled_red.json
```

The estate has retired four instruments for quietly ceasing to be true — the panel 10/10, the movers
"exactly two known-reds", the R14 fixture config pin, `BOARD_MD5_GOOD`. This ledger is built so it
cannot become the fifth, and it has now demonstrated that rather than claimed it.

---

## Two findings this order produced that were not in the audit

**1. A `SEALED-LAG` carrier class, found by a false red of my own.** The first draft of
`release_manifest_check.py` asserted all 40 carriers must equal computed truth. Run the moment the
apply seat moved the store, it reported `book_stable_seal.store_md5` as drift. That looked like the
widened check earning its keep. It was wrong: the book seal is a freeze-stamp that records what the
tree was when the book was last sealed, and it legitimately lags between bakes — traced across its
own history, including a commit where the tree was in exactly today's shape and the lag closed at the
next bake. Asserting equality would have reded the gate on every ordinary store write. Carriers now
declare `live` or `sealed`; sealed carriers that lag are reported in full and gate nothing, while
`MISSING` and `WIDTH` remain hard failures for them. See `M1a(3b)`.

**2. The audit's ranked repair #3 is the wrong half of its own fork.** The order and the audit both
named "add `data/model_config.json` to `_R14_RESTORE`" as a one-line fix. It does clear the reported
failure — and then trips control 17, `test_current_immutable_inputs_stay_current`, a committed test
declaring that file a CURRENT immutable input that must not be restored to R14 bytes. The tree
adjudicated its own fork. The correct half — the audit's stated alternative, "restamp `boot.config`
in the coherence pass" — costs six executable lines, not one, and is flagged as a deviation at the
top of `M1a(4b)` rather than folded in quietly.

---

## What is NOT done, stated plainly

* **`ship_gates_check.py` still cannot run end-to-end.** One-liner (a) clears the gate the suite
  killed itself on, proven in isolation. The *other*, independent blocker stands: line 49 hardcodes
  `RA = '/home/claude/rl_workspace/rl_after'`, and that shared workspace is measurably stale
  (store `cb38ef11`, head `29376d5a`, rl_model `98f16794` against pins `cc02567f` / `5ac6780f` /
  `6fe7c415`). Guard 5 correctly refuses it, before reaching the repaired line. Re-seeding it was
  refused — other seats are live against it, which is precisely the hazard the build lock exists for.
  The audit's repair #2 (~3 lines) is the next thing between this tree and a live
  burn/birthday/class/no-arb/tail run, and it was not sanctioned here.
* **`run_panel.sh` was not executed end-to-end.** It is a full engine act against the shared
  workspace. The lock wiring is proven by `bash -n` on all three edited files plus an exclusion test
  that sources the helper in the exact form and under the exact `set -euo pipefail` the entry points
  use. Same discipline the audit seat applied when it refused to run fv-provenance on a shared box.
* **No generator was migrated to the templates.** The skeletons and validator ship; nothing in
  `ui/tools/` calls `slots.render()` yet. Later tranche, as the order specifies.
* **The seven UI-seam suites and two Track B suites are not registered in the runner yet.** They are
  the natural second tranche and will arrive already wired to carriers.
* **`data/book_stable_seal.json` has not been re-sealed since the store moved.** Reported as
  `SEALED-LAG`, not as a defect — but a gate that consumes the seal as a baseline (`ship_gates` B3)
  is comparing against the pre-apply store, and that is worth someone's decision.
