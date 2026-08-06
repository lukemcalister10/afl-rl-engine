# #326 second rehearsal — the identity re-pin, reconciled

Method: a two-axis sweep at build time (never from the directive). OUTGOING — grep the whole tree for
each superseded literal (`2b7c1a00`, `15525b03`, `3b011802`, `b7389fe4`, `5b7c108c`, `9d155e8e`).
INCOMING — grep for each new literal to be sure it landed only where it belongs. Live paths only;
`docs/`, `session_*/` and `backups/` are sealed history and were read, not written.

## RE-PINNED in this change

| carrier | field | from | to | why |
|---|---|---|---|---|
| `data/expected_boot.json` | `engine_head` | `15525b03…` | `9f258a3b…` | `_merged_recover.py` carries the entry anchor |
| `data/expected_boot.json` | `rl_model` | `3b011802…` | `33f94073…` | `rl_model.py` resolves the levels and the division lookup |
| `data/expected_boot.json` | `board` | `2b7c1a00…` | `864b6726…` | pool entry prices move, by ruling |
| `data/release_contract.json` | `identities.engine_head` | `15525b03…` | `9f258a3b…` | must equal the boot pin |
| `data/release_contract.json` | `identities.rl_model` | `3b011802…` | `33f94073…` | must equal the boot pin |
| `data/release_contract.json` | `identities.board` | `2b7c1a00…` | `864b6726…` | must equal the boot pin |
| `data/release_contract.json` | `contract_sha256` | `9d155e8e…` | `8cc7d897…` | recomputed by `release_contract.contract_hash`'s own recipe (sha256 over the contract minus `contract_sha256` and `_doc`, sorted, compact separators) |
| `engine/rl_after/one_source_selftest.py` | `_contract_md5` | `5b7c108c…` | `eae593f2…` | `ui/release_pick_curve.json` now mirrors `pool_levels`, as it already mirrors `pool_value` |
| `ui/release_pick_curve.json` | `pick_curve_file_md5` | `b7389fe4…` | `988135ef…` | the curve artifact gained the `pool_levels` block |
| `data/rl_build/rl_app_data.json` + `.srcmd5` `own_md5` | — | `2b7c1a00…` | `864b6726…` | the checkout's board copy is what `boot_guard` asserts on entry |

## REGENERATED (not hand-pinned — rebuilt from the change)

| artefact | tool | note |
|---|---|---|
| `ui/data/board_view_working.js` | `ui/tools/extract_board_view.py` | ring-fence re-verified: bundle head md5 == the new board id |
| `ui/data/board_view_public.js` | same | same run |
| `s4_matrix.json` (workspace) | `s4_matrix_M1v7.py` | book re-sealed; F2 book==board parity green |
| `rl_app_data.json` (workspace) | `rl_export.py` | the board itself |

`ui/data/club_valuation.js`, `movers.js`, `movers_transition.js`, `ownership.js` were NOT regenerated:
they are produced by other tools on their own cadence and carry no pin on the board or engine identity
that this act moves. Named here so the omission is a decision, not an oversight.

## LEFT ALONE, and why

| identity | why it does not move |
|---|---|
| `curve payload df766dff` | the ladder was not touched. `add_pool_levels.py` ASSERTS it equal before and after; `pick_curve_curve_md5` is unchanged in both the artifact and the contract |
| `store f1e8c9fe` | no store row was written |
| `band 34faa865`, `fv d920557e`, `register 652d83e8`, `config cef06fd6` | untouched inputs |
| `v0surf d594dc03` | the frozen year-zero surface must LOAD, and does — signature `af556bdc` was already in that pickle before this act existed, which is the proof the signature did not move |
| `q97m`, `peak_model`, `bust_prior`, `pvc_snapshot` | frozen train-time caches; no retrain here |
| `balanced_board_md5 4939d740` | the immutable present-lens baseline. `release_contract.restamp_dynamic` preserves it by design; it is lineage, not an output of this build |
| `release_version` | not a release |
| the book (`s4_matrix.json`) and its `.srcmd5` | rebuild themselves — regenerated this run, F2 book==board green |
| `data/book_stable_seal.json` | NOT re-sealed here, and it must not be: B3 re-seals only at a bake, on the owner's word. Its sealed head is `40f43772`, already behind `15525b03` before this act, so B3 reports DIFFERS-BY-DESIGN either way. Named so the untouched seal is a decision |
| `release_lineage` | sealed history |
| `ui/tests/ownership_store_apply.test.py` | its `2b7c1a00` is prose in a comment describing what #328 did, and a historical constant in the assert beside it. Still true |
| `docs/evidence/**`, `session_*/**` | sealed evidence trees. Several carry `15525b03` / `3b011802` as the state THEY measured, which is what they are for |

## Verification

After the sweep, the only live-path occurrences of `b7389fe4` and `5b7c108c` are inside the re-pin
comments that record them as PREVIOUS PIN — the convention this file follows from the acts before it.
`2b7c1a00` survives only in sealed evidence and in the historical comment named above.
