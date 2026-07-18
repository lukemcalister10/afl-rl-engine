# fwd_calib — forward-lens calibration investigation (item 351) · artifact → stamp map
seat 13 · 2026-07-18 · branch `claude/forward-lens-calibration-qxu8sy` · READ-ONLY · report-only.

**Question:** is the forward board's collapse (now 752,427 → +1 618,248 → +2 485,937 WITH phantom)
CALIBRATED, or systematic under-projection? **Answer: under-projection** (see FINDINGS.md verdict).

| file | what |
|---|---|
| `PLAN.md` | git entry (SHAs asserted), **honest provenance/stamp note**, method, construction choices |
| `FINDINGS.md` | the verdict artifact — 4 jobs + one-paragraph read + engine-site localization |
| `out/findings.json` | machine-readable results for all 4 jobs |
| `out/young_mislabeled_exits.txt` | job-4 cross-link: 155 developing players tripped below the X=207 exit bar |
| `out/exportlog_probe_run.txt` | the read-only probe export log (RL_LEGF=1, single-thread) |
| `scripts/analyze.py` | the analysis (reproducible; reads probe board + F2 boards) |

## Reproduce (read-only)
Probe board built in the pinned workspace, then:
```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
RL_LEGE=1 RL_PVC2=1 RL_LEGF=1  python3 rl_export.py     # -> board 790136a3, per-player vM2/vM1/v/vP1/vP2
python3 scripts/analyze.py                              # -> out/findings.json
```
Provenance caveat (PLAN.md): F1's exact store `968de0c7` is not in-container; the probe runs the same
Leg-E/F lens family at the v2.10 head (store `b1fd0bce`), reproducing F1's WITHOUT-phantom +1 to ~1%.
The verdict is a structural rate/shape property and re-appears on F2's independently-built boards.

## Gate
Report-only. Nothing ruled, baked, or sealed. The balanced board is untouched. NO fix (this build).
