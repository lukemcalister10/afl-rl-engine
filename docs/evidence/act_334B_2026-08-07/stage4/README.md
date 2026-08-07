# 334 stage B / STAGE 4 — PEDIGREE-CONDITIONED REACTIVITY

Branch `landing/334-stage-b`, baseline `c0ea507` (stage 3). Nothing merges to main; no PR; no tag.
Adoption remains the owner's separate click.

## The result in one screen

| | |
|---|---|
| **the change** | one engine file. `sitout_ev`'s evidence weight `lam` — the ONE site where a thin record overrides its draft-day anchor — is conditioned on prior expectation: `lam_eff = lam ** (1 + PED_BAR·(1−q))`, `q = ped(pick) × sit(sit-out depth)` |
| **the dial** | **`RL_PED_BAR = 0.5`**, one dial, half the family's natural unit (the owner's standing "slight"). `RL_PED_BAR=0` reproduces the stage-3 board **byte-exact**, proven on 2650/2650 real rows |
| **new constants** | **none.** `ped` reuses the `_R_surf` log-pick axis and its `[1,90]` clamp; `sit` is a ratio of the already-computed D13 retention surface |
| **MRAZ** | board **3358 → 2898** (−460, **−13.70%**); engine `ev()` 3534 → 3050 |
| **the pedigree gap (i)/(ii)** | **1.3585 → 1.5298** — the identical record is now worth much more to a top-5 pick than to a pick-35 sit-out |
| **movers** | **51 of 804 (6.34%)** — 41 cuts, 10 lifts; board total 655759 → 654570 (**−0.181%**); **every mover is on the thin-record path** |
| **boundary** | **SEAM RATIO = 1.000 on all four probes** — prices AT the establishment bar are byte-identical across the change |
| **fit coupling** | **NONE, and measured.** Declared refit at `PED_BAR` 0.0 / 0.5 / 2.0 all reproduce the committed pickle `9713ec6c` at signature `3e8e50de5103`. `v0surf` UNMOVED, not in `_V0SURF_GATES` |
| **pins** | `engine_head` `a0a20d6e` → **`9a0c7fdc`** · `config` `cef06fd6` → **`0b5d2703`** · `board` `6c9f8d3a` → **`b490ae8b`** · `rl_model` / `fv` / `store` / `v0surf` / band / q97m **all UNMOVED** |
| **gates** | Guard 5 **PASS** (×2) · PARITY GATE **PASS** 804/804 eps=0 · NUMÉRAIRE GUARD **PASS** (pick-1 = 3000) · BOOK↔BOARD **PASS** · FUT-LABEL **PASS** · ZERO-EMPTY-CLUB **PASS** · CONFIG-MANIFEST **PASS** |
| **self-test** | **PASSED, 143 assertions, 0 FAIL, exit 0** — same count as stage 3, **0 re-points** |
| **BAND (report only)** | peak **year 4, ratio 1.432196** — **INSIDE [1.35, 1.45]**, +0.0322 from the 1.40 target (stage 3: 1.432364). **Nothing retuned.** |

## What the owner asked for, and where each piece is answered

| the ask | answered in |
|---|---|
| the mechanism, why continuous, why slight, the investigation that found the site | `MEMO.md` |
| the fit-coupling proof | `FIT_COUPLING.md` |
| **(a)** every moved player, with the triggering record, no cap | `MOVERS_FULL.txt` · `movers_full.csv` · `movers_full.json` |
| **(b)** the Mraz probe, old → new, path in two sentences | `PROBES.md` §(b) |
| **(c)** the pedigree pair, stage-4 and stage-3, and the gap | `PROBES.md` §(c) |
| **(d)** the boundary DiD at the establishment bar | `PROBES.md` §(d) · `boundary_*.txt` |
| the final measurement, no-arb, band, yr1-to-peak, per-entry-year, top-end | `MEASUREMENT.md` · `noarb/` |
| pins old → new | `PINS.md` |

## The three things worth an owner's eye

1. **The site was not where the directive's candidate list suggested it would be.** `E_q`, `_ev_rec`,
   `_ev_pw` and the `#336` ramp are all ~inert for a four-game record (`E_q = 0.0017`). The whole re-rate
   runs through `sitout_ev`'s `lam`, and `lam` was pedigree-blind. `MEMO.md` §1 measures all five.
2. **The change is symmetric, and that means ten players move UP.** A thin record BELOW its anchor is the
   same small sample as one above it, so a low-pedigree player whose few games went badly is also held
   nearer his anchor. This is the owner's own L-SYMMETRY law (item 108) and a one-sided `max()` would be a
   branch, but it is the one place the change does something not literally asked for. All ten are named.
3. **Yr1-to-peak went UP, away from the relocation target** (whole cohort 1.4833 → 1.4910; deep picks
   1.5500 → 1.5692), because the change cuts year-1 thin-record values and leaves the peak alone. Reported
   straight, compensated for nowhere.

## How to re-run

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add /home/claude/stage4_landing landing/334-stage-b
RL_VENDOR=/home/claude/stage4_landing/vendor bash /home/claude/stage4_landing/bootstrap.sh   # Guard 5

export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
export RL_REPO=/home/claude/stage4_landing
export RL_FV=$RL_REPO/engine/forward_valuation

cd /home/claude/rl_workspace/rl_after
rm -f rl_app_data.json
python3 rl_export.py          # PARITY + NUMÉRAIRE GUARD; board -> b490ae8b3bbd28b908ccb923ed8412c1
python3 s4_matrix_M1v7.py     # BOOK<->BOARD PARITY GATE
python3 one_source_selftest.py                        # PASSED, 143 / 0

# the tracking deliverables, from this directory
S=$RL_REPO/docs/evidence/act_334B_2026-08-07/stage4
git -C $RL_REPO show c0ea507:data/rl_build/rl_app_data.json > /tmp/board_stage3.json
python3 $S/enumerate_movers.py /tmp/board_stage3.json $RL_REPO/data/rl_build/rl_app_data.json
RL_TAG=stage4 python3 $S/probes.py
RL_TAG=stage4 python3 $S/boundary_did.py
#   for the stage-3 contrast, put c0ea507's _merged_recover.py in the workspace and re-run with RL_TAG=stage3

# the fit-coupling proof (dev shell — a DECLARED experiment, so NO RL_CONFIG_MODE)
unset RL_CONFIG_MODE
for B in 0 0.5 2.0; do RL_PED_BAR=$B RL_V0SURF_REFIT=1 \
  python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify; done

# the final measurement
cd $S/noarb
RL_OUT=$PWD python3 emit_matrix_338.py      # -> per_entrant_338_stage4.json (6a36cd7a)
python3 noarb_table_338.py per_entrant_338_stage4.json
python3 noarb_ext_338.py
python3 goal_metrics.py
```

## Manifest

| file | what |
|---|---|
| `MEMO.md` | the design memo: the investigation, the mechanism, why continuous, why slight, the dial ladder |
| `FIT_COUPLING.md` | the fit-coupling proof — static reachability + the three-sided declared refit |
| `PINS.md` | every pin old → new, what did NOT move and why, the gate table |
| `PROBES.md` | (b) Mraz · (c) the pedigree pair, both holds, stage-3 contrast · (d) the boundary DiD |
| `MEASUREMENT.md` | the final whole-cohort row, peak, band verdict, yr1-to-peak, per-entry-year, top-end, board delta |
| `MOVERS_FULL.txt` · `movers_full.csv` · `movers_full.json` | **the full enumeration** — every moved player + triggering record, sorted by \|rel\|, no cap |
| `enumerate_movers.py` · `probes.py` · `boundary_did.py` | the three instruments (sources and disclosures in their headers) |
| `probes_stage4.txt` / `probes_stage3.txt` (+`.json`) | the probe runs, both builds |
| `boundary_stage4.txt` / `boundary_stage3.txt` (+`.json`) | the cliff test, both builds |
| `board_delta.py` · `board_delta_vs_6c9f8d3a.txt` · `board_build_log.txt` | the board delta and the build log |
| `selftest_full_output.txt` | the self-test, 143 / 0 |
| `killswitch_proof.txt` | `RL_PED_BAR=0` == the stage-3 engine, 2650/2650 rows |
| `fit_coupling_refit_log.txt` | the raw three-sided `--verify` output |
| `noarb/` | the matrix, the tables, the four instruments as re-run, the emit log, the stage-4 board copy |
