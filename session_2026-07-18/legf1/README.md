# LEG F1 — PHANTOM INTAKE LAYER · session artifacts → stamp map
seat 13 · 2026-07-18 · branch `claude/legf-phantom-intake-build-dvbipz` · base `cc58570` (Leg-E tip).

## What this build is
The +1/+2 forward lens gains a **phantom intake layer** (MEMO_LEGF §2): per-club draft capital (PVC gross),
free intake at R=207, and list-size-conserving exits at X=207 — report/view only, gated on **RL_LEGF**
(default ON). k=0 carries ZERO phantom content; the balanced board is byte-untouched. Engine UNTOUCHED
(pure export/view). F2 (retrospective −1/−2 boards) is a separate parallel build; this UI reads its
artifacts empty-state-safe.

## Reproduce (single-thread pinned — see REPRODUCIBILITY_ANNEX.md)
    scripts/build_board.sh           # pins OPENBLAS_NUM_THREADS=1 etc.; prints board md5
    RL_LEGE=1 RL_PVC2=1 RL_LEGF=0 scripts/build_board.sh   # -> d85901af (Leg-E lens, byte-exact)
    RL_LEGE=1 RL_PVC2=1 RL_LEGF=1 scripts/build_board.sh   # -> e613ca58 (phantom board, default)
    RL_LEGE=0 RL_PVC2=1 RL_LEGF=0 scripts/build_board.sh   # -> 06d8af60 (balanced, byte-exact)

## Artifacts
| file | what | stamp / key result |
|---|---|---|
| `PLAN.md` | job 1 plan · derived fence · baselines | seal 1d180424 |
| `sealed_strawman.json` / `.sha256` | the §6 sealed vector (R=207/X=207/natural-order) | sha256 **1d180424…** |
| `ENTRY_PROOF.md` | git anchor · store/curve · the BLAS resolution | store 968de0c7 · curve 56dd7a7b |
| `REPRODUCIBILITY_ANNEX.md` | numpy/OpenBLAS/lscpu/threads (item 347) | OpenBLAS DYNAMIC_ARCH |
| `out/discriminator.txt` | filed 10-panel: 10/10, max\|Δv\|=0, 0 rank moves | — |
| `out/phantom_totals_report.txt` | §2.v totals, per club+league, WITH/WITHOUT (from the e613ca58 board) | +1 Δ+80480 · +2 Δ+92562 |
| `out/selftest2.txt` | frozen suite / SSI guards | F1 parity mismatches=0 · Guard-5 red (expected) |
| `EXIT_PROOF.md` | the full exit ledger | store 968de0c7 held |
| `scripts/build_board.sh`, `scripts/discriminator.py` | the harnesses | thread-pinned |

## Gate / provenance stamps
- Store `rl_model_data.json` **968de0c7** (HARD-OUT, held entry→exit) · curve `pvc_curve_v2.json` **56dd7a7b**
  (payload 89c14729) · engine `rl_model.py` cc626d7d / `_merged_recover.py` 6ad07bb2 (UNTOUCHED).
- RL_LEGF=0 ⇒ filed d85901af / 06d8af60 / 9829d01a byte-exact. RL_LEGF=1 ⇒ e613ca58, +3 additive keys,
  0 k=0 v-movers.
- Guard-5 boot-store red = the known pre-bake class (re-pins at the bake); flagged, never self-pinned.
