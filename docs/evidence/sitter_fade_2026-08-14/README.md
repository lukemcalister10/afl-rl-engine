# `docs/evidence/sitter_fade_2026-08-14/` — ORDER 30A

**The act:** ORDER 30A, the ND sitter discount **derived from evidence**, across the owner's three
lenses — position, draft pick, years in the system. Brief and the owner's ruling verbatim:
[#334 comment 5289933916](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5289933916).

**Start here: `SITTER_FADE_PACKET.md`.**

**READ-ONLY. NOTHING WIRES.** No engine file, board, store or curve moved. The old `los_decay`
schedule (`rl_model.py:725-729`) is the **DECLARED FALLBACK** and stays operative until the owner
rules on the packet.

| file | what |
|---|---|
| `PREREG_30A.md` | pre-registration — 26 numbered predictions, the estimator and the censoring rule, committed at `06bd7be` **before** the harness existed in runnable form and before any cell was counted |
| `o30a_derive.py` → `SITTER_DISCOUNT_TABLE.json`, `DERIVE30A_out.txt` | the derivation harness. Pin-asserted at entry; deterministic (two runs, identical md5) |
| `SITTER_DISCOUNT_TABLE.md` | all three lenses, `n` and dispersion on every cell, the unusable cells named, the anomalies |
| `SITTER_FADE_PACKET.md` | the owner-facing packet — the question, the derived surface, the old schedule beside it, the named rows, the recommendation, the prereg scored |

**The headline.** The derived ND sitter discount, all picks, all positions, fitted on 1,142 ND
1-64 entrants from the 2004–2021 classes:

| years since entry | 1 | 2 | 3 | 4 | 5+ |
|---|---:|---:|---:|---:|---:|
| **derived** | 1.000 | **0.568** | **0.214** | **0.105** | **0.074** |
| old, MID/SD/SF | 1.000 | 0.852 | 0.568 | 0.307 | 0.136 |
| old, KPF/KPD/RUCK | 1.000 | 1.000 | 0.956 | 0.716 | 0.428 |
| n | 1,140 | 462 | 234 | 154 | 130 |

The designed schedule is **too generous at every depth the board prices**, and its 2.5-year
key-position/ruck grace is the largest single error in it. Of the three lenses, **years in the system
carries essentially all the signal**; the pick lens is non-monotone and artefact-contaminated; the
six-way position lens is noise, though the two-way KPP+RUCK vs nonKPP collapse is a real
second-order effect at depth 2.

**Inputs, pinned:** Layer 1 `ad1229ea6f44` and `LAYER2.json` (grace-A) from
`origin/build/delivered-value` — read out of git by the harness rather than duplicated here — plus
`pvc_curve_v2.json` (the landed entry law), `DAY0_29B_FINAL.json` (the 29B printed flat-v0 prices)
and `rl_model.py` (imported live for `disc_factor` and the old schedule's own constants).

**Upstream:** ORDER 26B, `docs/evidence/delivered_value_2026-08-12/` (the scorer and conventions
borrowed) · ORDER 21, `docs/evidence/pool_retention_2026-08-12/` (the pool's depth construction, used
for the method-symmetry leg) · ORDER 29/29B, `docs/evidence/landing_29_2026-08-13/` (the landed entry
law and the flat-v0 keying this discount would multiply).
