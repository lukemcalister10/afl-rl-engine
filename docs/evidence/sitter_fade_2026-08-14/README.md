# `docs/evidence/sitter_fade_2026-08-14/` — ORDER 30A and ORDER 30A-2

**Two acts live here.** ORDER 30A derived the ND sitter discount; **ORDER 30A-2 re-cut it** against
the owner's four corrections. **`SITTER_FADE_PACKET_2.md` is the current ruling basis and supersedes
`SITTER_FADE_PACKET.md`.** ORDER 30A's artifacts stand untouched on their own basis, and 30A's
headline row is reproduced inside the re-cut, from scratch, to `1.1e-16`.

**Start here: `SITTER_FADE_PACKET_2.md`.**

**READ-ONLY. NOTHING WIRES.** No engine file, board, store or curve moved in either act. The old
`los_decay` schedule (`rl_model.py:725-729`) is the **DECLARED FALLBACK** and stays operative until
the owner rules.

### ORDER 30A-2 — the re-cut (current)

Brief: the owner's four corrections,
[#334 comment 5290213551](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5290213551).

| file | what |
|---|---|
| `PREREG_30A2.md` | pre-registration — 25 numbered predictions, committed at `f29d623` **before** `o30a2_recut.py` existed in runnable form and before any cell of any of the four tasks was counted |
| `o30a2_recut.py` → `SITTER_DISCOUNT_TABLE_2.json`, `RECUT30A2_out.txt` | the re-cut harness. Pin-asserted at entry; deterministic (two runs, identical md5 `606b31e1` / `0ff958d6`) |
| **`SITTER_FADE_PACKET_2.md`** | **the owner-facing ruling basis** — both discount rows side by side, the continuous named-row table, the band verdict, the games-transition curve, the recommendation, the prereg scored with all 7 breaches owned by number |

The four tasks: **T1** listed-conditioning on the #338 minimum-listing-tenure reconstruction (two
readings, L-A and L-B, both published) · **T2** the continuous season-fraction depth clock
(`φ = calendar_progress = 0.92`) · **T3** the pick bands re-tested with the A2 near-zero-denominator
guard · **T4** the games transition, `0 / 1-2 / 3-5 / 6-10`.

### ORDER 30A — the original derivation (superseded as the ruling basis, intact as evidence)

Brief: [#334 comment 5289933916](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5289933916).

| file | what |
|---|---|
| `PREREG_30A.md` | pre-registration — 26 numbered predictions, the estimator and the censoring rule, committed at `06bd7be` **before** the harness existed in runnable form and before any cell was counted |
| `o30a_derive.py` → `SITTER_DISCOUNT_TABLE.json`, `DERIVE30A_out.txt` | the derivation harness. Pin-asserted at entry; deterministic (two runs, identical md5) |
| `SITTER_DISCOUNT_TABLE.md` | all three lenses, `n` and dispersion on every cell, the unusable cells named, the anomalies |
| `SITTER_FADE_PACKET.md` | the ORDER 30A packet — the question, the derived surface, the old schedule beside it, the named rows, the recommendation, the prereg scored |

**The headline, after the re-cut.** The ND sitter discount, all picks, all positions, fitted on 1,142
ND 1-64 entrants from the 2004–2021 classes:

| years since entry | 1 | 2 | 3 | 4 | 5+ |
|---|---:|---:|---:|---:|---:|
| **30A-2 listed-conditional (L-B, the candidate law)** | 1.000 | **0.568** | **0.360** | *0.307 — bound only, n=11* | **UNRESOLVED** |
| 30A unconditional (delisting-blind = harsh lower bound) | 1.000 | 0.568 | 0.214 | 0.105 | 0.074 |
| 30A-2 L-A (own-data-extends = generous bound) | 1.000 | 0.568 | 0.344 | 0.463 | *1.072 — outcome-selection leak* |
| old, MID/SD/SF | 1.000 | 0.852 | 0.568 | 0.307 | 0.136 |
| old, KPF/KPD/RUCK | 1.000 | 1.000 | 0.956 | 0.716 | 0.428 |
| n (unconditional / L-B) | 1,140 | 462 / 462 | 234 / 100 | 154 / 11 | 130 / 2 |

The designed schedule is **too generous at every depth the board prices**, and its 2.5-year
key-position/ruck grace is the largest single error in it. Of the three lenses, **years in the system
carries essentially all the signal**; the pick lens is non-monotone and artefact-contaminated, and the
30A-2 re-cut confirms **no wireable band gradient** survives the A2 guard; the six-way position lens
is noise.

**What the re-cut changed.** Listing-conditioning moves depth 3 from 0.214 to **0.360** and cannot
move depth 2 at all. The continuous clock is the larger correction on the live rows: `josh-smillie`
is at true depth **2.92**, not 2, which takes him from 30A's 919 to **604** even after
listing-conditioning raises him. The games transition is measured, and it is neither a cliff nor a
smooth curve — the first game is worth **+0.39** in D, then the sequence dips before rising.

**Inputs, pinned:** Layer 1 `ad1229ea6f44` and `LAYER2.json` (grace-A) from
`origin/build/delivered-value` — read out of git by the harnesses rather than duplicated here; a
fresh checkout needs `git fetch origin build/delivered-value` — plus `pvc_curve_v2.json` (the landed
entry law), `DAY0_29B_FINAL.json` (the 29B printed flat-v0 prices) and `rl_model.py` (imported live
for `disc_factor` and the old schedule's own constants). ORDER 30A-2 additionally pins
`docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json` (the #338 lane's own emit, for
the listing cross-check) and `data/season_state.json` (`calendar_progress`, the T2 clock).

**Upstream:** ORDER 26B, `docs/evidence/delivered_value_2026-08-12/` (the scorer and conventions
borrowed) · ORDER 21, `docs/evidence/pool_retention_2026-08-12/` (the pool's depth construction, used
for the method-symmetry leg) · ORDER 29/29B, `docs/evidence/landing_29_2026-08-13/` (the landed entry
law and the flat-v0 keying this discount would multiply).
