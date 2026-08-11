# ROUND 3 — THE IDENTITY PROOF, AND THE COMMANDS THAT PRODUCED IT

Round 3 added five dials. Every one is default OFF. This file is the proof that with all five off the
engine is the same engine, so that every measured number in MENU.txt is a measurement of the dial and
not of the wiring.

The dials: `RL_A_GSAT`, `RL_336_NOP`, `RL_336_SURVLVL`, `RL_336_CLAMP`, `RL_336_PARSURV`
(plus `RL_AGE_DISC_MODE=5`, which is a new value of an existing declared dial, not a new dial).

---

## 1. PRICE-LEVEL MATRIX IDENTITY — the emit, all dials off

```
bash docs/evidence/composition_2026-08-10/emit_variant.sh IDENT5 HEAD          # no dials
```

| | file md5 | `recs` md5 | records |
|---|---|---|---|
| `per_entrant_FULL.json` (emitted at 95dfbde) | `c698b5b2763d29e299c14315576b48f1` | `3eb4a686e36e4e299f1134e153c566bd` | 2645 |
| `per_entrant_IDENT5.json` (emitted at the round-3 tip) | `4f7633d755ddc6f75180c747e9ca1695` | `3eb4a686e36e4e299f1134e153c566bd` | 2645 |

**The prices are byte-identical.** `recs` — every player, every as-of year, every path value —
matches exactly. Year-1 movers across the 1,197 teaching rows: **0**.

**The FILES differ, and here is the complete list of why.** Only `meta` differs, in two fields:

| field | FULL | IDENT5 | reason |
|---|---|---|---|
| `meta.engine_head` | `4fc44090` | `3feb8e02` | `_merged_recover.py` gained the `RL_A_GSAT` dial and its comment block. A source md5 moving is expected; it is the *prices* that must not. |
| `meta.emitter.workdir` | `.../wt_emit_FULL/...` | `.../wt_emit_IDENT5/...` | the emitter records its own throwaway worktree path, which is derived from the label. |

This is the price-level identity the brief required, not a file-copy test. A file-copy test would
have failed here for two reasons that carry no price.

## 2. BOARD IDENTITY — the built board, all dials off

```
bash docs/evidence/composition_2026-08-10/build_board_at.sh 95dfbde  <out>
bash docs/evidence/composition_2026-08-10/build_board_at.sh <tip>    <out>
```

| ref | board md5 |
|---|---|
| `95dfbde` (the branch tip before round 3) | `846560dc1b206996005c7c9e9290207c` |
| the round-3 wiring commit | `846560dc1b206996005c7c9e9290207c` |

**Byte-identical, same environment** (`RL_CONFIG_MODE=gate`, `PYTHONHASHSEED=0`,
`OPENBLAS_NUM_THREADS=1`, all BLAS thread counts pinned to 1).

## 3. DENOMINATOR INTEGRITY — the year-zero surface in every arm

The cohort ratio divides by `mean(v0)`. If `v0` moved, a year-1 move could be a denominator artefact.

| arm | v0 movers (of 1197) | sum(v0) change |
|---|---|---|
| C336P | 1 | −0.00001% |
| C336E | 1 | +0.00024% |
| C336C | 1 | +0.01834% |
| AGSATF | 0 | 0.00000% |
| AGSATD | 0 | 0.00000% |
| V5 | 1 | +0.00299% |

The frozen year-zero surface is intact in every arm. The single mover is the same one row the V4
diagnosis already identified. **No reported year-1 move is a denominator effect.**

## 4. THE INSTRUMENT WAS NOT TOUCHED

`noarb_table_338.py` md5 `0f8220351c64c56ccfa90c60edcdfa5f`, verified at the head of round 3 and
re-verified inside `round3_tables.sh` on every copy it makes, which **halts** on a mismatch. The
table lanes run in separate directories precisely so the instrument's own output file cannot race
between them; that is a lane-isolation change, not a change to the script.

The harness `harness_pvc_REPINNED_pass3.py` is unchanged: `EXPECT_STORE 'd9a24282'`,
`EXPECT_V0SURF '6ef67f07db98'`, and `EXPECT_N=1197` re-measured on each of the seven new matrices
(every table reports the same n=1197 included rows at year 1).

## 5. THE COMMANDS, END TO END

```
# 1. the emits (three lanes, staggered; each ~2.5-6 min)
bash round3_chain.sh "IDENT5:" "C336P:RL_336_NOP=1" "C336C:RL_336_PARSURV=1"
bash round3_chain.sh "V5:RL_AGE_DISC=1,RL_AGE_DISC_MODE=5" "C336E:RL_336_SURVLVL=1,RL_336_CLAMP=1"
bash round3_chain.sh "AGSATF:RL_A_FLOOR=1,RL_A_GSAT=18" "AGSATD:RL_A_DRAGFADE=1,RL_A_GSAT=18"

# 2. the canonical tables (instrument md5 asserted inside)
bash round3_tables.sh A IDENT5 V5 C336C
bash round3_tables.sh B AGSATF C336P
bash round3_tables.sh C AGSATD C336E

# 3. the proofs and readers
bash run_arm.sh decouple_proof.py decouple_proof_OFF.txt RL_A_GSAT=0
bash run_arm.sh decouple_proof.py decouple_proof_ON.txt  RL_A_GSAT=18
bash probe_arm.sh BASE ; bash probe_arm.sh NOP RL_336_NOP=1        # tbl336_probe.py, the table probe
python3 yr1_direction.py        # the PRE-EMIT direction probe (feeds PREREG_ROUND3.md)
python3 design336_probe.py      # ORDER 3b, the two design mechanisms + the par sizing
python3 round3_movers.py        # the mover census and the Mraz column
python3 menu_table.py           # regenerates MENU.txt / MENU.json
```

`run_arm.sh` / `probe_arm.sh` exist because gate mode requires the environment to match the manifest
**and** the manifest hash to match the pinned boot config. They set both for the duration of one run
and restore both on exit, including on failure. They never leave the tree dirty; `git status` on
`data/` is checked after every use.

## 6. THE ONE PLACE THE PROOF IS NON-VACUOUS ON PURPOSE

`decouple_proof.py` hashes **two** vectors in the same pass:

| | RL_A_GSAT=0 | RL_A_GSAT=18 | required |
|---|---|---|---|
| `sitout_ev` over 15,882 evaluations | `2a11b8b17a854e33d9d51ab050581021` | `2a11b8b17a854e33d9d51ab050581021` | **MATCH** ✓ |
| `_a_share` over 7,941 evaluations | `53640643bd5520eb6be59379dfffc7d4` | `88b9c45c02988355845a09169bcdddb0` | **DIFFER** ✓ |

Without the second row, a proof that `sitout_ev` did not move would also pass if the dial did nothing
anywhere at all. With it, the proof distinguishes "the dial is inert" from "the dial acts, but not
here" — and it is the second.
