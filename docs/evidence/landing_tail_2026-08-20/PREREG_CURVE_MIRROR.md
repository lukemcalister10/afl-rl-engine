# PREREGISTRATION — R2, THE PICK-CURVE MIRROR RE-STAMP

**Pushed BEFORE the edit.** Nothing in this file is written after the fact. Every number below that
can be known in advance is stated in advance; the one that cannot (the re-stamped file's own md5,
which depends on bytes that do not exist yet) is declared as a *procedure* rather than a value, and
the procedure is checkable.

## THE RULING

Register **v786** (2026-08-20) put ruling **R2** to the owner:

> re-stamp the ui/release_pick_curve.json MIRROR to the landed curve 9729f0c5 (his own workbook's
> Ladder already sums 47,315 = that exact curve) + the one-line pin at one_source_selftest.py:492,
> PREREGGED (an engine-file edit) — the payload moved under ORDER 31-F so the #326 mirror-restamp
> precedent does not cover it alone.

The owner ruled: **"yes, the pick curve should be updated"**.

The prior seat halted here and was right to (`05_curve_contract_HALT_fork.txt`): the curve PAYLOAD
identity moved (`df766dff -> 9729f0c5`), so this is not the pure file-bytes-only mirror re-stamp the
#326 precedent covers, and re-stamping requires touching an engine file. Both blockers are what the
owner has now ruled through. **This act is the recording of that ruling, not a curve adoption
decision**: the curve is *already live* — it is the curve the landed board a05fe951 was built on
(measured: 64 shared picks, 0 disagree, `05_...`), it is the curve the engine loads, and it is the
curve in the owner's own workbook (Ladder row 29 "Board value each year (fixed)" moved
54333 -> **47315**, which is exactly this curve's 1-64 ladder sum). `ui/release_pick_curve.json` is
the last stale mirror of an adoption that already happened.

## WHAT WILL CHANGE — exactly two fields and one pin

**`ui/release_pick_curve.json`** (the release-active pick-curve provenance contract, a MIRROR):

| field | from | to |
|---|---|---|
| `pick_curve_file_md5` | `f6f3027fc56615fc77cd455638a5fa79` | `78ad9842525ae4f09875b95afc2e2b39` |
| `pick_curve_curve_md5` | `df766dff` | `9729f0c5` |

plus one appended sentence in `_doc`, in the file's own established re-stamp-note style, naming this
act and its ruling. No other key is touched.

**`engine/rl_after/one_source_selftest.py:492`** — the FROZEN-RULER pin
`_contract_md5 = 'bdc21f33eb70d49dd481f7e63a1b0398'` re-pins to the md5 of the re-stamped
`ui/release_pick_curve.json`, **in the same commit**, with the history comment extended in the exact
form the four prior re-pins used. This is the paired procedure the pin's own comment prescribes:
*"this pin moves in the same commit exactly as prior acts did."* It is the ONE sanctioned engine-file
edit of this order, and it is a one-line md5 pin — it changes no valuation, no constant, no code path.

## WHAT WILL NOT CHANGE — declared in advance, and measured now

Measured on the tree **before** the edit:

* `pool_levels` in the contract vs in the artifact `engine/rl_after/pvc_curve_v2.json`:
  **IDENTICAL** (whole-block JSON compare, all 13 keys). No re-mirror is required. *If they had
  differed, the mirror block would move too — declaring that here so a silent extra edit is
  impossible.*
* `pool_value` 237.2 in both. `curve_source_store_md5` f1e8c9fe in both. `per_entrant_md5` 999d24c8
  in both. `numeraire_pin1` 3000. `release_version` v2.11-final-rc1-PROVISIONAL.
* `adopted_at_round`, `adopted_pathway`, `pick_curve_domain`, `pick_curve_path`, `pool_index`,
  `split_note`, `supersedes`, `_pool_levels_note`, `_pool_value_adoption_note` — untouched.
* The artifact `engine/rl_after/pvc_curve_v2.json` is **not touched at all**. It is the authority;
  this file mirrors it.

The artifact's own measured identity, for the record: file md5
`78ad9842525ae4f09875b95afc2e2b39`, self-declared `curve_md5` `9729f0c5`, 64-entry domain 1-64,
ladder sum **47,315**, pick1 3000 / pick2 2668 / pick64 179.

## FALSIFIERS — stated before the act, reported whatever they say

1. **F1 — the payload must match EXACTLY.** After the edit, `pick_curve_curve_md5` must equal the
   artifact's own `curve_md5` string and `pick_curve_file_md5` must equal `md5(pvc_curve_v2.json)`,
   compared as full strings, not prefixes. Any inequality: HALT.
2. **F2 — the selftest must PASS.** `engine/rl_after/one_source_selftest.py` must pass after, with
   the re-pinned `_contract_md5` equal to the md5 of the re-stamped file *as it is committed*. If it
   fails, or if it passes for any reason other than the pin matching, HALT and revert.
3. **F3 — the board must be BYTE-IDENTICAL.** `data/rl_build/rl_app_data.json` must be
   `a05fe951f78482c70520480e184c80ec` before and after. This is display/mirror only. **If the board
   moves, HALT.**
4. **F4 — nothing else moves.** The commit's diff must contain exactly two files:
   `ui/release_pick_curve.json` and `engine/rl_after/one_source_selftest.py` (plus this evidence
   directory). Anything else: HALT.
5. **F5 — store and round unmoved.** Store `cb38ef11...` (still unwritten at this stage), round pin
   22 everywhere, six-way store coherence PASS after.
6. **F6 — the curve-provenance suite.** `ui/tests/club_curve_provenance.test.py` stands at **22/35**
   with 4 residual FAILs which the prior seat attributed to this one drift (the live CURVE DRIFT
   halt pre-empting three negative controls' own tamper halts, and CASE1 pricing 0 picks).
   **PREDICTION: it goes to 35/35.** If it does not, the attribution was wrong and that is reported
   as a finding, not smoothed over.
7. **F7 — the ingest's curve gate.** `ui/tools/ingest_inputs.py` must stop halting at the curve
   contract: the two checks *"release-active curve file md5 == contract"* and *"release-active curve
   curve_md5 == contract"* must both read OK.

## WHAT THIS ACT DOES NOT CLAIM

It does not adopt a curve. It does not re-derive one. It does not move a price. Every held draft pick
in `ui/data/club_valuation.js` is priced off this curve — and it already was, because the engine and
the landed board already load `pvc_curve_v2.json`. What changes is that the provenance contract stops
disagreeing with the artifact it exists to guard. The contract's stated purpose is *"to stop the curve
moving SILENTLY"*; this move is ruled, declared here in advance, and recorded.

*Pushed before the edit, per the order. Build seat, 2026-08-20.*
