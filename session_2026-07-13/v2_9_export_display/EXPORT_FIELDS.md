# v2.9 EXPORT/DISPLAY — new field schema (display-only; zero EV movers)

All fields below are ADDITIVE. No existing field changed value; every player `v` and lens value
(`vM2/vM1/v/vP1/vP2`) is byte-identical to the certified board 8a66b4ba. New keys are the only diff.

## Per-row (active + back), in `rl_app_data.json`
| field | meaning | source | null when |
|---|---|---|---|
| `lti_reg` | register disposition tag `{section,designations,out,L,return_arm,ret_year,flags}` | RL_AVAIL state on `MA.data`, resolved by stable key (consumer-wiring fix) | row is not a register name |
| `vPrev` | value on the last-accepted-bake board (all-levers-OFF base, de4baef9 lineage) | certified stage board `g_base` | row is new since the bake |
| `vRaw` | pre-override model figure (= `v`; `v` is never overridden) | stamped post owner-override application | row has no owner override (all rows today — 0 overrides) |
| `levers` | `{L1,L4,L2,L3,L5}` cumulative G-ATTR deltas; **Σ == v − vPrev** | certified stage boards (differenced) | attribution sidecar absent |

## Top-level
| field | meaning |
|---|---|
| `lensPicks` | 60 future-lens phantom pick entries: the `2026-EOY-ND` class (picks 1–30) on the **+1 (2027)** and **+2 (2028)** lenses ONLY, at PVC face value, `labelYear` rolling with the view. Never on the current/−1/−2 player ladder (item-14 exclusion). |
| `lensConservation` | report-only diagnostic: per-lens (−2…+2) `{lensYear,players,picks,total,nPlayers,nPicks}` + `_meta.spread_vs_now`. The year-0 continuity check (item 12): value converts (classes enter as picks, players fade), it does not vanish. Caveat: PVC face value + scrap-floor leakage make future lenses run slightly under. NOT a gate. |

## Consumer (`ui/tools/extract_board_view.py`)
- working bundle: passes `lti_reg`, `vPrev`, `vRaw`, `levers` per row; `lensPicks`, `lensConservation` top-level.
- public bundle: unchanged (sanitised — no attribution, no lens machinery).
- ring-fence unchanged: emitted `srcmd5` must == the re-pinned `expected_boot.board`.

## Provenance
- `engine/rl_after/export_attribution.json` (committed, bootstrap-seeded to cwd like the other sidecars)
  carries `vPrev` + `levers`, built by `scripts/build_export_attribution.py` from the certified stage
  boards (`gen_gattr_chain.sh`; sums asserted 723075→732725). rl_export reads it from cwd; absent ⇒ fields
  ship null (forward-safe).
