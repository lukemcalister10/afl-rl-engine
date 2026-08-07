# 334 stage B / STAGE 3 — the base curve re-taught era-free, the re-anchor landed, the numéraire resolved

Branch `landing/334-stage-b`, baseline `93c2a9a`. Nothing merges to main; no PR; no tag. Adoption
remains the owner's separate click, and the `#328` reversal condition is tripped by construction.

## The result in one screen

| | |
|---|---|
| settled ladder payload | **`18203822cf438ecef03ed77a771f9942`** (in-file `curve_md5` `18203822`), total 51221, pick 1 = **3000** |
| numéraire | `published_pin` **3000 UNMOVED** · head 3017.9232 → **3384.3148448406** · s 0.9940610814748366 → **0.8864423487588727** · coherence exact (0.0) |
| ENGINE CHANGE | **NONE.** `engine_head` and `rl_model` pins unmoved. |
| v0surf | `d594dc03…` → **`9713ec6c83270ab916bb4a5e3ded6cb3`**, signature `af556bdca53d` → **`3e8e50de5103`**, 2 signatures frozen |
| entrant seal | `c9e7491b` → **`5c38e8ba`**, re-seal by its own rule, measured intake history byte-identical |
| board | `f94e0778…` → **`6c9f8d3a92ca82c29dfaa8273a4f3ada`** |
| gates | PARITY GATE **PASS** (804/804, eps=0) · NUMÉRAIRE GUARD **PASS** · BOOK↔BOARD PARITY **PASS** · Guard 5 **PASS** (pre and post) · FUT-LABEL **PASS** · ZERO-EMPTY-CLUB **PASS** |
| self-test | **PASSED**, 143 assertions, 0 FAIL, exit 0; 3 pins re-pointed |
| **CONVERGENCE** | **peak year 4, ratio 1.432364, distance to 1.40 = +0.032364 — INSIDE [1.35, 1.45]. ONE iteration. No refinement.** |

## The five things this stage did

1. **BASE-CURVE RE-TEACH** (`BASE_RETEACH.md`). The base ladder was re-derived era-free through
   `harness_pvc.structural_values()` + the shipped `#271` kernel + `monotone_strict`. The currency
   mapping into the shipped ladder is the **identity**, established by three independent measurements,
   not assumed. The era-removal component of the base delta is at most **1 board point at any pick**
   (total −9); the visible drift is the #336 layer (−1985), the #338 tenure basis (+607) and the
   derive_271-vs-harness recipe (+570), each measured on its own matrix. Full 64-row per-pick table
   with the four-way attribution: `base_reteach_table.txt`. No buckets anywhere.
2. **THE RE-ANCHOR APPLIED** on top: `base_erafree(p) × f(p)`, `f` read at full precision from the
   committed stage-2 table. Monotone non-increasing on the exact product **PASS**, no isotonic
   projection. **One** rounding collision, minimally repaired and reported: pick 19, 958 → 957.
3. **THE NUMÉRAIRE RESOLVED** (`NUMERAIRE.md`) — the single global re-base by `g = f(1) = 1.121405224905`,
   applied to **both** sides (the ladder ÷ g, the numéraire block's `s` ÷ g). That is the exporter's own
   standing instruction and the E6 two-sided law already in `rl_model._load_numeraire`, so it required
   **no engine change**. Requirement (iv) — established players' engine values untouched — is reported
   **not satisfiable** alongside (i)–(iii), with the proof that the choice is forced and the disclosed
   cost: a uniform 10.83% re-denomination of every player.
4. **THE DECLARED SURFACE REFIT** around the settled ladder, and **THE SEALED ENTRANT LAYER**
   (`SEAL.md`) re-pointed by its own documented rule after its `#306 L7` reconciliation HALT fired.
5. **PIN COHERENCE** (`PINS.md`), the board landed with its `.srcmd5` sidecar, and the
   **CONVERGENCE MEASUREMENT** (`CONVERGENCE.md`) + **GOAL METRICS** (`GOAL_METRICS.md`).

## Board delta vs the era-removal board `f94e0778`

**708 movers of 804 (88.06%) — 707 cuts, 1 lift.** Total `732696 → 655759`, ratio **0.894995**
(delta −76937). Mean |relative move| 8.6900% board-wide, 9.8683% across the movers.

This is dominated by the numéraire re-denomination: every player carries the same factor
`1/g = 0.891738`. The one "lift", jack-martin +2 (107 → 109), and the 1-point moves at the bottom of the
lift list are integer-rounding at small values — the ladder-driven component of a low-value row falls by
`f(p)/g` rather than `1/g`, which is a smaller cut, and rounding then goes either way.

| top 10 cuts | | top 10 "lifts" (all ±1 except the first) | |
|---|---|---|---|
| harry-sheezel | 11963 → 10668 (−1295, −10.83%) | jack-martin | 107 → 109 (+2, +1.87%) |
| nick-daicos | 10820 → 9649 (−1171, −10.82%) | sam-wicks | 12 → 11 (−1) |
| luke-jackson | 9722 → 8670 (−1052, −10.82%) | sam-sturt | 40 → 39 (−1) |
| nasiah-wanganeen-milera | 9681 → 8633 (−1048, −10.83%) | river-stevens | 77 → 76 (−1) |
| max-holmes | 8399 → 7490 (−909, −10.82%) | paddy-dow | 158 → 157 (−1) |
| tristan-xerri | 7976 → 7113 (−863, −10.82%) | mitch-podhajski | 108 → 107 (−1) |
| will-ashcroft | 7204 → 6423 (−781, −10.84%) | mark-o-connor | 10 → 9 (−1) |
| zak-butters | 7085 → 6317 (−768, −10.84%) | liam-ryan | 24 → 23 (−1) |
| errol-gulden | 6802 → 6065 (−737, −10.84%) | liam-henry | 63 → 62 (−1) |
| josh-treacy | 6803 → 6067 (−736, −10.82%) | lennox-hoffman | 77 → 76 (−1) |

**Age buckets** — the young end is cut LESS, which is the re-anchor showing through the uniform
re-base (young/year-zero values are ladder-driven and fall by `f(p)/g`, not `1/g`):

| bucket | n | movers | total | ratio |
|---|---|---|---|---|
| ≤22 | 294 | 254 | 251064 → 225541 | **0.898341** |
| 23-26 | 245 | 214 | 292729 → 261511 | 0.893355 |
| ≥27 | 265 | 240 | 188903 → 168707 | 0.893088 |

Full list: `board_delta_vs_f94e0778.txt`.

## Manifest

| file | what |
|---|---|
| `BASE_RETEACH.md` | the base re-teach memo: machinery, the currency-mapping disclosure, the four-matrix attribution |
| `base_reteach.py` · `base_reteach_table.txt` · `base_reteach.json` | the derivation, its full 64-row per-pick delta + attribution table, machine-readable |
| `NUMERAIRE.md` | the numéraire memo: what the engine asserts, why the choice is forced, the arithmetic, and (iv) reported straight |
| `settle_ladder.py` · `settled_ladder_table.txt` · `settled_ladder.json` | `base × f / g`, the checks, the repair, the numéraire arithmetic |
| `install_ladder.py` · `pvc_curve_v2_PRE_stage3.json` | the installer and the artifact as it stood before this stage |
| `refit_v0surf_log.txt` | the declared surface refit, full log |
| `SEAL.md` · `sealed_entrant_structure_PRE.json` | the entrant-layer seal: the halt, the rule, old → new, the four re-pointed sites |
| `PINS.md` · `pins.json` · `repin_contract.py` · `release_pick_curve_PRE_stage3.json` | the pin table, the old-identity sweep, the contract re-derivation |
| `SELFTEST.md` · `selftest_full_output.txt` | the re-point enumeration, the one data-driven emission, and the closed 144→146 register item |
| `CONVERGENCE.md` · `noarb_table_stage3.{txt,json}` · `noarb_ext_stage3.txt` · `convergence_stage3.json` | the convergence tables, the peak, the splits, yr1→peak |
| `GOAL_METRICS.md` · `goal_metrics.py` · `goal_metrics.txt` · `escalator_probe_log.txt` | top-end ratio, per-entry-year table, front-loaded assert, no-escalator proof |
| `board_delta.py` · `board_delta_vs_f94e0778.txt` · `board_build_log.txt` | the board delta and the build log |
| `per_entrant_338_stage3.json` | the FINAL stage-3 matrix, md5 `b7ed144ec5e4d44263d553a2c23d919b` |
| `emit_matrix_338.py` · `noarb_table_338.py` · `noarb_ext_338.py` · `harness_pvc_REPINNED_pass3.py` | the four instruments as re-run (the harness carrying its one re-pointed pin) |

## How to re-run

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add /home/claude/stage3_landing landing/334-stage-b
RL_VENDOR=/home/claude/stage3_landing/vendor bash /home/claude/stage3_landing/bootstrap.sh   # Guard 5

export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
export RL_REPO=/home/claude/stage3_landing
export RL_FV=/home/claude/stage3_landing/engine/forward_valuation

cd /home/claude/rl_workspace/rl_after
rm -f rl_app_data.json
python3 rl_export.py          # PARITY GATE + NUMÉRAIRE GUARD; board -> 6c9f8d3a92ca82c29dfaa8273a4f3ada
python3 s4_matrix_M1v7.py     # BOOK<->BOARD PARITY GATE
python3 one_source_selftest.py                        # PASSED, 143 / 0

# the derivation, from this directory (it re-reads the committed matrices and the stage-2 f table)
cd /home/claude/stage3_landing/docs/evidence/act_334B_2026-08-07/stage3
python3 base_reteach.py       # -> base_reteach.json, the attribution table
python3 settle_ladder.py      # -> settled_ladder.json, payload 18203822...

# the convergence measurement, on the final engine
RL_OUT=$PWD python3 emit_matrix_338.py                # -> per_entrant_338_confirmation.json (b7ed144e)
python3 noarb_table_338.py per_entrant_338_stage3.json
python3 goal_metrics.py
```
