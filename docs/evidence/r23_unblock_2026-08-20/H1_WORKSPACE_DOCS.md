# H1 — the transaction workspace does not carry `docs/`. Before / after.

**Seat:** R23 unblock, build seat · **Date:** 2026-08-20 · **Register:** v789/v791
**Base:** `origin/main` — store `cc02567f`, board `a05fe951`, `as_of_round=22`, ledger 3,086.
**Fix:** `engine/rl_after/ingestion/staged_apply.py`, `_build_workspace` copytree allow-list.

Rehearsed in an isolated scratch export of the tree. **The live repo was never written; the owner's
R23 file was never read.** The score file used is SYNTHETIC — R22's exact 409-name list with
obviously-fake patterned scores, carried over from the recon
(`scratchpad/r23_recon/scores/R23_SYNTH_*.csv`).

---

## The defect

`staged_apply._build_workspace` builds the throwaway workspace the weekly round-advance transaction
regenerates the board in, from an **allow-list**: `engine/rl_after`, `engine/forward_valuation`, six
root `.py`/`.md` files, `data/`, `session_2026-07-18/legf5`,
`session_2026-07-20/fv_provenance_remediation`, `ui`, `session_2026-07-17/legd_derivation`.

**No `docs/` subtree.** Since the ORDER 41/42 bake (register v780 — *"RL_O41_RESET / RL_O41_INJ /
RL_O41_R3 ARE NOW DEFAULT-ON"*) the engine reads three `RL_REPO`-relative **pinned owner inputs**
that live under `docs/`:

| file | read at | if absent |
|---|---|---|
| `docs/owner_annotations/SITTER_2026_v1.csv` | `_merged_recover.py:4167` (ORDER 41 I3 injury stream) | **SystemExit HALT** |
| `docs/owner_annotations/SITTER_2026_v1.csv` | `_merged_recover.py:5862` (ORDER 42 consolidation) | **SystemExit HALT** |
| `docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json` | `_merged_recover.py:2154` (v0 lens basis) | **SystemExit HALT** unless `RL_LENS_BASIS` set |
| `docs/evidence/exec_306_zlaarm/basis/lane_expectation.json` | `_merged_recover.py:2373` | optional, no halt |

All four are tracked and correct in the checkout. R22 landed 2026-08-10, **before** the bake — so the
weekly transaction has **never been run since these inputs became mandatory**. This is a plumbing gap,
not a data problem.

---

## BEFORE — `staged_apply.py` md5 `f81c4d9ca7dc92921d17023c09048c01` (unmodified `origin/main`)

```
python3 tools/round_entry/round_entry.py catchup --file 23=scores/R23.csv --approve
    (INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<scratch token>)
```

```
================ CATCH-UP PREFLIGHT ================
  season 2026 · 1 round(s) · identity overrides: Bailey Williams, Callum Brown
  R23  enc=utf-8     listed/played=409  resolved=409  listed-zero=0   absent/DNP=395   sha256 79ad59fac439
        identity override: Callum M. Brown        -> callum-brown-ire       (score 97, owner-override:map_all)
  PREFLIGHT CLEAN — every name resolves to a stable identity; no duplicate/ambiguous.
===================================================

About to apply rounds [23] — each as its own sequential transaction, committed in order.
round_entry: FAIL — StagedValidationError: staged board regen FAILED rc=1
ORDER 41 HALT: RL_O41_INJ=1 but the owner's annotation file is ABSENT at
  /tmp/wkupd_ws_0alj9tzj/docs/owner_annotations/SITTER_2026_v1.csv. The injury stream reads a
  PINNED OWNER INPUT and will not run without it, and will not substitute a guess for it.
```

Aborted pre-commit. Store `cc02567f` and board `a05fe951` **byte-unchanged**.
Full log: `raw/h1run_BEFORE.txt`.

---

## AFTER — with the fix (md5 `0fdd07df6691caac908c2838a5743734` in scratch)

Same file, same command.

```
round_entry: FAIL — StagedValidationError: staged board regen FAILED rc=1
ORDER 42 HALT: judson-clarke — the sheet reads games_2026=1 and the store reads 2. The store is
  the single source of production and the sheet is the single source of injury; a disagreement
  between them is an input defect, not something to average away.
```

**ORDER 41 no longer fires.** The staged build reads the pinned sheet and proceeds; the halt advances
to ORDER 42 — which is **H2**, the owner's item, ruled at register v790 (Armstrong and Clarke returned;
the sheet re-cut rides inside the R23 advance transaction). Aborted pre-commit, store/board
byte-unchanged. Full log: `raw/h1run_AFTER.txt`.

---

## PAST H2 — the `clean` variant (H2 dodged, 408 rows, no `injured=Y` player listed)

```
round_entry: FAIL — sibling_repin_txn.SiblingBuildError: sibling board build failed: rc=1 ::
  josh-rachele: board=1814 engine=1857 | bailey-humphrey: board=2293 engine=2386 |
  cameron-mackenzie: board=2109 engine=2194 | nick-madden: board=1056 engine=1127
```

The canonical board regen **completed**, including its own eps=0 F1 export↔engine parity gate, and the
transaction reached `_stage_sibling`, where it stopped at **H3**. Aborted pre-commit, store/board
byte-unchanged. Full log: `raw/h1run_CLEAN.txt`.

---

## Verdict

The predicted hazard chain reproduces **in order**: H1 → (fix) → H2 → (H2 dodged) → H3.
The falsifier did not fire: ORDER 41 stopped firing, nothing else changed, and all three aborted
transactions left the store, the board and the ledger byte-unchanged.

**What this fix does not do.** It copies two already-tracked, already-pinned input subtrees into a
disposable workspace. It moves no value, no identity, no pin and no expectation. It does not touch
ORDER 42 (H2) and it does not touch H3.
