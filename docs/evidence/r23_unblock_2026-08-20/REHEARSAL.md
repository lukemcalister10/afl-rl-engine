# R23 rehearsal — the transcript, and the verdict chain that stands after this seat

**Seat:** R23 unblock, build seat · **Date:** 2026-08-20
**Base:** `origin/main` — store `cc02567f`, board `a05fe951`, `as_of_round=22`, ledger 3,086.
**Score file:** SYNTHETIC throughout (R22's 409-name list, patterned fake scores). The owner's real
R23 file at `/root/.claude/uploads/.../37d44c23-R23.csv` was **never read and never applied**.
**The live board never moved.** Verified after every run: store `cc02567f`, board `a05fe951`.

---

## What was run

Three armed catch-up transactions in an isolated scratch export of the tree, and four direct board
builds. Every transaction aborted pre-commit, cleanly, with the store, the board and the ledger
byte-unchanged.

| # | run | result |
|---|---|---|
| 1 | preflight, synthetic `apart` shape | **PREFLIGHT CLEAN** · 409/409 resolved · listed-zero 0 · absent/DNP 395 · `Callum M. Brown → callum-brown-ire (map_all)` fired · Bailey rule correctly not in scope for R23 |
| 2 | armed apply, `apart`, **pre-fix** `staged_apply` | **H1** — `ORDER 41 HALT … SITTER_2026_v1.csv … ABSENT`; aborted pre-commit |
| 3 | armed apply, `apart`, **post-fix** | **H2** — `ORDER 42 HALT: judson-clarke — sheet games_2026=1, store 2`; aborted pre-commit |
| 4 | armed apply, `clean` (408 rows, no `injured=Y` listed), post-fix | canonical board regen **PASSED** incl. its own eps=0 F1 gate → **H3** `SiblingBuildError: sibling board build failed rc=1`; aborted pre-commit |
| 5 | `_run_sibling_build(balanced=True)` on the pristine base, pre-`aebf192` | **96/804** parity failures, all board < engine |
| 6 | same, on `origin/main` **after** `aebf192` | **96/804, identical** — `aebf192` touches `one_source_selftest.py` only and the sibling build never imports it |
| 7 | `_run_sibling_build(balanced=False, config_mode='canonical')` on the pristine base | **rc=0**, board `a05fe951f78482c70520480e184c80ec` **byte-exact to the pin**, `PARITY GATE PASS: all 804` |

Raw logs: `raw/h1run_BEFORE.txt`, `raw/h1run_AFTER.txt`, `raw/h1run_CLEAN.txt`,
`raw/h3_sibling_parity_mainbase.txt`, `raw/h3_canonical_build_pass.txt`.

The full end-to-end rehearsal on a clean run (order item 3) was **not** performed, because it was
conditioned on H3 resolving false-red and its fix landing. H3 resolved **REAL** — see
`H3_DIAGNOSIS.md` — so the advance is still blocked and there is no clean chain to rehearse.

---

## What the rehearsal proves

* **The identity layer is healthy and fully rehearsed.** The resolver, the override machinery, the
  duplicate guard and the listed-⇒-played / absent-⇒-DNP rule all behave exactly as the R22 record
  describes.
* **The transaction discipline is sound.** Three separate mid-flight halts, three clean pre-commit
  aborts, zero partial writes, the ledger never moved.
* **The canonical board regen works** on the landed base once H1 is fixed — and reproduces `a05fe951`
  byte-exact.
* **H1 is closed** (this seat, commit landing with this evidence).
* **H2 has its owner word** (register v790: Armstrong and Clarke returned; the sheet re-cut, the md5
  pin and the Y-count 37→35 ride inside the R23 advance transaction). It is not this seat's act.
* **H3 blocks unconditionally** and is independent of the owner's file.

---

## The verdict chain for the real R23 advance, as it stands today

Running the runbook's command list on the owner's real file **now** would produce:

| step | expected today |
|---|---|
| `md5sum` / `sha256sum scores/R23.csv` | recorded before anything else |
| preflight | `PREFLIGHT CLEAN` — unless the export collapses the two Bailey Williams onto the bare name, in which case `DUPLICATE stable key` and the owner's `(round, score)` mapping is needed (H5: escalate the rule, do not hand-extend it) |
| armed apply → ORDER 41 | **PASSES** (H1 fixed) |
| armed apply → ORDER 42 | passes only once the sheet re-cut of v790 has ridden in; otherwise **HALTS** on any `injured=Y` player who is listed |
| canonical board regen + its own F1 gate | **PASSES** |
| `_stage_sibling` → `build_sibling` | ⛔ **HALTS — 96/804 export↔engine parity, pre-commit** |
| commit | never reached |

**So the real advance is one blocker away, and it is not the owner's.** What remains between the repo
and the real R23 advance is:

1. **H3 — a valuation ruling and a repair, above this seat.** The corrected basis reproduces the board
   of record's own vector 804/804; adopting it moves 96 sibling prices (+0.39 % … +9.65 %, +2,772 on
   the board total) and therefore the balanced board md5, the present-lens baseline and its seal, the
   reference and forward vectors, the forward-lens oracle, both board-view bundles and the sibling
   sidecar. See `H3_DIAGNOSIS.md` §6 for the three questions the owner is being asked.
2. **H2's sheet re-cut**, already ruled, executed as part of the advance order.
3. **The owner's R23 file** and — if the export collapses the Bailey Williams names — his word on which
   score belongs to which club.

Items 2 and 3 are the owner's and the advance seat's. **Item 1 is the only thing standing between the
repo and a one-command advance, and it is a price decision, not a plumbing one.**
