# TEST LEDGER — after THE APPLY COMPLETION (2026-08-20)

Columns: the prior seat's HEAD (ec2e533, apply halted) · this tree (R1 + R2 + the casing fix + the
apply committed). Every number measured, none carried.

| suite | ec2e533 (apply halted) | THIS TREE | reading |
|---|---|---|---|
| `ui/tools/ownership_store_apply.py verify` | PASS on cb38ef11 | **PASS on cc02567f** | six-way coherence held through the write |
| `ui/tests/movers.test.js` | 63/66 | **66/66** | the 3 known fails were ONE cause — the missing landing column — and all three went green at R1 |
| `ui/tests/ownership_sidecar.test.js` | 21/35 | **35/35** | +14; the mirror is populated, so the era-bound cases resolve |
| `ui/tests/ownership_single_source.test.js` | 9/17 | **16/17** | +7. The 1 residual is a STALE ERA FIXTURE, named below |
| `ui/tests/ownership_store_apply.test.py` | 28/28 | **27/28** | the idempotency case went green (0 rows move on the applied tree); one count assertion is now era-bound, named below |
| `ui/tests/extract_seam.test.py` | 42/42 | **42/42** | held |
| `ui/tests/club_totals_parity.test.js` | 17/17 | **17/17** | held |
| `ui/tests/release_seam.test.js` | 30/30 | **30/30** | held |
| `ui/tests/counting_rule.test.js` | 24/24 | **24/24** | held |
| `ui/tests/adoption_gate.test.js` | 3/3 | **3/3** | held |
| `generate_movers_transition.py --check` | OK | **OK** (8 register entries) | mirror not stale |
| `rebuild_movers_derived.py --check` | OK | **OK** | rebuilt after R1 and again after the apply (the `values` block carries `affl_team`) |
| `sibling_repin.py verify` | 8 fails | **8 fails, THE SAME 8** | unchanged, as ordered — not repaired, it is its own future order |
| `ui/tests/club_curve_provenance.test.py` | 22/35 | **7/35** | ***MOVED, and not by R2.*** Attributed in full in 24_r2_mirror_result.txt: it is 7/35 at 338737c too (R1 landed, R2 not). A harness env leak, named there and below. |
| `engine/rl_after/one_source_selftest.py` | 17 fails (bare checkout) | **15 fails (bare checkout)** | the two FROZEN-RULER curve checks went FAIL -> PASS; every other verdict line identical. Not a clean pass — the bootstrapped workspace is register v782's own open item (1). |

## THE THREE NAMED RESIDUALS — measured, attributed, NOT repaired here

**1. `ownership_single_source.test.js` — one stale era fixture.**
The failing case is *"the owner's 2026-07-29 moves are on the board AND in the mirror (incl. the
name-twin sam-butler-1)"*. Measured, key by key: five of its six fixture rows still hold exactly.
The sixth, `ed-langdon`, is pinned at `West Coast Eagles` — and **the owner's own 2026-08-20 sheet
moves him**, `West Coast Eagles -> Port Adelaide Power`, one of the 112. The mirror is right and the
fixture has been outrun. The load-bearing half of the case — the name-twin `sam-butler-1` landing on
the board player and not his twin — still holds. Remedy, one line: re-pin `ed-langdon` to
`Port Adelaide Power`, or drop that key and keep the five the new sheet did not touch. Not taken
here: re-typing a fixture to match new data is the move the tree warns about, and it is a decision
about what the assertion is for.

**2. `ownership_store_apply.test.py` — one count assertion is era-bound.**
`check(len(ours) == 1, "exactly ONE #283 register entry exists — a re-run appends no second one")`.
`ownership_store_apply.append_transition` stamps every store transition with the standing ruling id
`OWNERSHIP_SINGLE_SOURCE_2026-07-30`, so a genuinely NEW owner sheet correctly produces a second
entry carrying it: entry [2] is the 2026-07-30 apply, entry [8] is this one. The property the case
was written to defend — idempotency, "a re-run appends no second one" — is intact and is proved
green two lines above it (`re-running preflight on the applied tree is a NO-OP`). What is stale is
the fixed count. The entries are harmless to the boundary reader by construction: a store-only
transition deliberately carries NO `destination.board`, so `model_changes()` treats it as a pointer
note that contributes nothing. Remedy: assert one entry PER STORE TRANSITION rather than one in
total. Not taken here — it needs a ruling on what the assertion should become.

**3. `club_curve_provenance.test.py` 22/35 -> 7/35 — a harness environment leak, opened at R1.**
Full attribution in `24_r2_mirror_result.txt`. In short: `ingest_inputs.py` drives the REAL
`ownership_store_apply` transaction while the fixture only redirects the `RL_UI_*` paths. Before R1
that transaction halted at T5 and the suite's negative controls were satisfied by THAT halt —
passing on the wrong halt. After R1 it runs on to T7, where `extract_board_view` resolves
`BOOT = os.environ.get("RL_UI_BOOT", …)` — which the harness has pointed at the REAL manifest — and
ring-fences the staged store against the live pin. Nothing live is broken: the transaction is atomic
and every one of those runs committed nothing. Remedy: the harness should redirect `RL_UI_BOOT` for
the transaction too, or the transaction should not inherit it. Not taken here — a harness/resolver
edit, not in this order.

## TWO GAPS IN THE APPLY ITSELF, FOUND BY RUNNING IT AND REPAIRED BY THEIR WRITERS OF RECORD

* **[T7] drops `board_view_working.stamp.release`.** `extract_board_view` emits `release: null`; the
  full block is written by a SECOND writer, `round_movers.inject_release_contract(22)` — the one the
  prior seat used to repair carrier (a). T7 runs only the first, so the apply silently un-did it and
  `movers.test.js` fell to 65/66 on the one assertion that reads it. Re-injected here by that same
  writer (`28_reinject_release_contract.txt`); 66/66 restored. **T7 should run both.**
* **The apply does not rebuild `ui/data/movers.js` derived blocks.** The `values` block carries
  `affl_team` per player, so 112 ownership moves make it stale (`--check` DRIFT, 3219089 -> 3218999
  bytes). Rebuilt by `ui/tools/rebuild_movers_derived.py`; the per-round REPORTS are byte-verbatim
  through both rebuilds — reports digest `156228623e804da88b52047a04f83b96` before and after.
