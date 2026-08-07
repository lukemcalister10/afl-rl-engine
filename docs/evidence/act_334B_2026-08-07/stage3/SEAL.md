# Stage 3 step 4 — THE SEALED ENTRANT LAYER, re-pointed by its own rule

## What it is

`session_2026-07-18/legf5/sealed_entrant_structure.json` — the LEG F5 §2.viii entrant slot structure
(MEMO_LEGF v1.3, owner item 359). It is the FULL expected annual intake (~103.4 slots/yr) measured
from **recorded store intake history** over the window 2019–2025, smoothed to a per-effective-pick
mean occupancy, sealed BEFORE any render by the §6 seal-first law, and priced at the v2-curve PVC of
each effective pick. `rl_export.py` re-verifies the seal at render and HALTs on drift.

## How the re-anchor moved it, and the halt that proved it

The seal covers the counts **and** the PVC total those counts price to. The `#306 L7` reconciliation
made that a hard assert: the board reprices the sealed counts at the live curve and refuses to render
if the result disagrees with the sealed total. Moving the ladder moves the reprice. Observed, verbatim,
on the first build against the settled ladder:

```
LEG F5 HALT (#306 L7 reconciliation): board repriced entrant layer 60651 != sealed total 62931.
The seal counts and the live curve/store disagree; re-seal from the live intake history before
rendering.
```

That is the halt the previous, killed run saw. It is not a defect — it is the seal doing its job.

## Its own documented rule, and what re-running it moved

The rule is in the halt text and in the seal script's header: **re-seal from the live intake history**
via `session_2026-07-18/legf5/scripts/seal_structure.py`, run from the workspace `rl_after` with
`RL_REPO` set. Its `_measure_stamp()` reads the live provenance rather than carrying a frozen literal
(`#306 L7`: "a seal that names the wrong provenance is a true hash of the wrong artifact"). It was run
verbatim, unedited.

**The measured intake HISTORY is byte-identical.** These fields did not move:

`basis` · `draft_occupancy` · `mech_occupancy` · `expected_counts` · `expected_slots_per_year` ·
`window` · `n_years` · `law` · `name` · `pickeq` · `per_club`

Only the repricing of those same counts, and the live provenance stamp, moved:

| field | old | new |
|---|---|---|
| `entrant_pvc` | draft 55753 + mech 7178 = **62931** | draft 53474 + mech 7178 = **60651** |
| `round_counts` 1-18 / 19-36 / 37-54 / 55-72 | 30228 / 13263 / 7611 / 4651 | 29539 / 12675 / 6856 / 4404 |
| `mech_summary` MSD `pvc_each` | 224 | 202 |
| `mech_summary` PDA / SSP / UNR `pvc_each` | 197 | 188 |
| `mech_summary` IRE / PDN `pvc_each` | 237 | 237 (pool level, unmoved) |
| `stamp.store_md5` | f1e8c9fe | **37ced3ce** |
| `stamp.curve_file_md5` | f1cf148e | **73d6f679** |
| `stamp.curve_payload_md5` | df766dff | **18203822** |
| `stamp.board_balanced_md5` | 4939d740 | **123deccb** |
| **`seal_sha256_8`** | **c9e7491b** | **5c38e8ba** |

`stamp.store_md5` and `stamp.board_balanced_md5` move because `_measure_stamp()` reads
`data/release_contract.json`'s live identities, which already carried 37ced3ce / 123deccb; the previous
seal's stamp was measured when the contract carried f1e8c9fe / 4939d740.

## The pin, RE-POINTED — never patched

The seal id is pinned as a literal at four live sites. All four moved to `5c38e8ba`; the assertions
themselves are byte-identical, and the three-way equality (`recomputed == stored == pinned`) still
stands, so a doctored structure still HALTs:

| file | line | what |
|---|---|---|
| `engine/rl_after/rl_export.py` | 678 | the render-time seal-verify HALT |
| `engine/rl_after/rl_export.py` | 680 | its message |
| `engine/rl_after/rl_export.py` | 655-660 | the provenance comment, rewritten to name the re-seal and the superseded seal |
| `session_2026-07-18/legf5/scripts/gate_f5.py` | 25, 28 | the F5 gate's own assert + report |
| `session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py` | 36-37, 41 | the k=0 dormancy test's two checks |

The seal was re-run TWICE: once against the settled ladder (`c58c8e3a`), and again after the curve
artifact's `stamp` block was re-derived at step 5 — because `stamp.curve_file_md5` is inside the sealed
payload, so the file's own md5 is part of what the seal covers. The final, landed seal is **`5c38e8ba`**;
`c58c8e3a` was an intermediate that never reached a landed board.

After the re-point the render reports:

```
LEG F5 ENTRANT LAYER (RL_LEGF=1): 18 clubs · §2.viii sealed intake 60651 PVC
(draft 53474 + mech 7178, 103.4 slots/yr, seal 5c38e8ba) · +1 Δ=+60651 · +2 Δ=+60651 · k=0 phantom=NONE
```

**No halt, no guess, no weakening.** The seal's meaning was unambiguous — it seals a measured history
and the price that history carries — so it was re-pointed by its own documented rule rather than
reported as a stop.
