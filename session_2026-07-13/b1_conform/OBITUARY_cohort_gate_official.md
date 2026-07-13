# OBITUARY — `cohort_gate_official.py`

**Path (deleted):** `session_2026-07-13/v2_9_continuation/scripts/cohort_gate_official.py`
**Retired:** 2026-07-13 (B1 code-conform job, register item 40 / seat 5)
**Cause of deletion:** it was a second, drifting copy of the B1 gate — the exact lookalike the
single-source invariant exists to forbid (CORE rule 7: *delete, don't disable*).

## What it was
A standalone script that lifted `ship_gates_check.py`'s `_b1_rows` **verbatim** (byte-for-byte,
marked "do-not-edit") and ran it on a walk-forward matrix path to print a G-COHORT verdict. It was
adopted by the v2.9 continuation (`CONTINUATION_PLAN.md`, `HARNESS_RECONCILIATION.md`,
`COMBINED_GATE.md`) as "the OFFICIAL G-COHORT gate".

## Why it had to go
1. **It computed the DEMOTED construction.** `_b1_rows` is the per-class **yr1=100 renormalisation +
   mean-of-ratios** (the owner's 02/07 D5 wording). On 2026-07-13 the owner ruled the **July-8
   construction** (raw class-year sums averaged across classes; each of y4/y5/y6 vs min(y1,y2) ≤ 1.30)
   is THE gate, and demoted the indexed reading to a non-gating shape diagnostic (register v52;
   CONSTRAINTS v1.8 G-COHORT obituary). The script's own docstring still called itself "the official
   gate" — a label written **before** the ruling. Its headline `126.8/125.2/116.1` is the indexed row,
   never the gated number.
2. **It silently no-oped at the item-20 job (item 38).** Its `__main__` reads the matrix path from
   `sys.argv[1]`. At the item-20 suite it was invoked with **no matrix argument**, raised
   `IndexError: list index out of range`, and produced **nothing**. The traceback was swallowed by a
   `| tail -8` pipe (`session_2026-07-13/store_identity_job/scripts/run_suite.sh:31`), no exit code
   was checked, and the suite reported **"official cohort gate 126.8/125.2/116.1 PASS"** — figures
   carried from the v2.9 boot note, never measured in that job. A binding guard reported green
   **without ever running.** A gate that silently does not run is worse than a red one.
3. **Two copies drift.** With B1 now computing the ruled construction inside the frozen suite, a
   second verbatim copy of the old construction is dead weight that can only diverge.

## What replaces it
`ship_gates_check.py` **B1** is now the ONE cohort gate. It computes the July-8 construction directly
(`_b1_july8`), keeps the indexed reading only as a labelled non-gating **shape diagnostic**
(`_b1_rows`), and — with the suite-wide silent-gate fix — turns any exception / missing input / None
result into a **named HALT** that exits the suite non-zero. The completeness net additionally HALTs the
suite if any gate produces no verdict at all. The item-38 failure mode (silence reported as PASS) can
no longer happen inside the suite.

## Not touched (deliberately)
The historical `session_2026-07-13/store_identity_job/scripts/run_suite.sh` — which invoked this script
behind the `| tail -8` pipe — is a **record of what happened** and is left exactly as it was (directive
§3; historical session logs are out of scope). It now references a deleted script; that is the correct
archaeological state. The standing invocation rule (never pipe a gate through `tail`/`head` without
checking its exit code) is recorded in `SHIP_GATES.md` so every FUTURE suite inherits the fix.

*Requiescat: it computed the right arithmetic for the wrong construction, and on its last outing it
computed nothing at all and was called a pass.*
