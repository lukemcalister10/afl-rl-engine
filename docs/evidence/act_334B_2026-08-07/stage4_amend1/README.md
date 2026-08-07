# 334 stage B / STAGE 4 AMENDMENT 1 — SURPRISE-SCALED EVIDENCE TRUST

Branch `landing/334-stage-b`, baseline `44950de` (stage 4, board `b490ae8b`). Nothing merges to main; no PR;
no tag. Adoption remains the owner's separate click.

## The result in one screen

| | |
|---|---|
| **the owner's word** | *"4 games of sample, especially when it's so far from the projection, shouldn't be trusted as much, surely."* — with the binding constraint: **no broad hit to young players** |
| **the change** | one engine file. `sitout_ev`'s evidence weight is now conditioned on **SURPRISE** as well as pedigree: `lam_eff = lam ** (1 + PED_BAR·(1−q) + SUR_W·s·u)` |
| **the statistic** | `s = \|log(e_full / anchor_full)\|`, `anchor_full = R × entry_anchor` — **the same anchor leg the blend uses**. The choice is FORCED: it is the only pairing for which "zero surprise" and "this change is inert" are the same statement, identically |
| **the resolution fade** | `u = 1 − rho(gp)/rho(6)`, `rho(g)=g²/(g²+g+K)` — the engine's **own** R100.11 curve at its **own** pinned `K=5.8`, normalised at the ruled 6-game bar. `u` is the complement of `#336`'s `resolve_w`: **the unresolved share** |
| **new constants** | **none.** `K`, the bar and the `min(·,6)` clamp are all existing engine objects |
| **the dial** | **`RL_SUR_W = 5.0`**, one new dial. **`RL_SUR_W=0` reproduces the stage-4 board byte-exact** (`b490ae8b`, through the full gate) |
| **MRAZ** | board **2,898 → 1,585** (−1,313, **−45.31%**) — **2.99×** his pick's value of 530, was 5.47× |
| **the pedigree gap (i)/(ii)** | **1.5298 → 2.3753** (draft-age held) · **1.3305 → 2.1367** (as-of-age held) |
| **movers** | **45 of 804 (5.60%)** — 38 cuts, 7 lifts; board total 654,570 → 652,183 (**−0.365%**); **every mover on the thin-record path** |
| **near-projection** | **6 in band, 2 moved. Continuous max 0.657% — PASS. Integer board max 1.036% — FAIL by one 2-point row.** See ⚠ below |
| **boundary** | **SEAM RATIO 1.0000 on all four probes**; prices AT the bar **byte-identical**; **no new cliff** in a g=1..10 sweep |
| **fit coupling** | **NONE, and measured.** Declared refit at `SUR_W` 0.0 / 5.0 / **20.0** all reproduce the committed pickle `9713ec6c` at signature `3e8e50de5103`. `v0surf` **UNMOVED** |
| **pins** | `engine_head` `9a0c7fdc` → **`bc45d773`** · `config` `0b5d2703` → **`38a73675`** · `board` `b490ae8b` → **`b56bbdde`** · `rl_model` / `fv` / `store` / `v0surf` / band / `q97m` / ladder / numéraire **all UNMOVED** |
| **gates** | Guard 5 **PASS** · PARITY **PASS** 804/804 eps=0 · NUMÉRAIRE GUARD **PASS** (pick-1 = 3000) · BOOK↔BOARD **PASS** · FUT-LABEL **PASS** · ZERO-EMPTY-CLUB **PASS** · CONFIG-MANIFEST **PASS** (61 vars) |
| **self-test** | **PASSED, 143 assertions, 0 FAIL, exit 0** — same count as stage 4, **0 re-points** |
| **BAND (report only)** | peak **year 4, ratio 1.432092** — **INSIDE [1.35, 1.45]**, +0.0321 from the 1.40 target (stage 4: 1.432196). **Nothing retuned.** |

## ⚠ THE ONE THING THE OWNER MUST RULE ON

**The calibration criterion was NOT met as literally written, and that is stated rather than smoothed away.**

The criterion: *Mraz lands in ~1,100–1,600 while players within ±25% of projection move by less than 1%.*
**No rung of the ladder achieves both on the integer board.** At the shipped rung:

| ruler | max abs move in the near-projection band (n=6) | verdict |
|---|---|---|
| **continuous engine price** | **0.6574%** | **PASS** |
| integer board value | 1.0363% | **FAIL** |

**The entire gap is one row.** `Jaxon Artemis` (SD, MSD pool, **board value 193**, 3 games, claiming 1.152×
his projection) moves **193 → 191 — two board points**. His *continuous* move is **−0.6166%**, i.e. **1.19
board points**, well under the bar. But one board point on a 193-point player is already **0.518%**, so a
"<1%" test on that row means *"moves by less than 1.93 board points"* — the integer grid cannot express it.

It is a **measurement-granularity result, not a re-rate**, and it is filed as a criterion failure anyway
because it is one. If the integer reading is binding, `RL_SUR_W = 2.0` satisfies it (band max 0.518% = one
board point) with Mraz at 2,267 — outside the Mraz target. Both are one edit apart. `MEMO.md §5` carries the
full ladder; `NEAR_PROJECTION_PROOF.txt` carries the assertion with denominators.

**What the criterion WAS met on, unambiguously:** the 109 thin-record players with no live evidence are
**byte-exact**, and the change is ordered by surprise and nothing else — mean absolute move by quartile of
`s`: **1.90% / 4.02% / 16.86% / 25.77%**.

## What the owner asked for, and where each piece is answered

| the ask | answered in |
|---|---|
| the statistic, the composition, the fit-coupling verdict, the calibration criterion and ladder | `MEMO.md` |
| **the near-projection proof** — every band player, denominators, programmatic assertion | `NEAR_PROJECTION_PROOF.txt` · `near_projection_proof.json` · `near_projection_proof.py` |
| **full enumeration** vs `b490ae8b`, every mover, no cap, with the triggering record | `MOVERS_FULL.txt` · `movers_full.csv` · `movers_full.json` |
| the Mraz probe + the pedigree pair, all four arms and the (i)/(ii) ratio | `PROBES.md` · `probes_stage4a1.txt` / `.json` |
| the boundary — SEAM ratio and the g=1..10 no-cliff sweep | `PROBES.md` §(d) · `boundary_stage4a1.txt` / `.json` |
| additive vs multiplicative, and the double-charging measurement | `COMPOSITION_CHECK.txt` · `MEMO.md` §4 |
| the fit-coupling proof | `FIT_COUPLING.md` · `fit_coupling_refit_log.txt` |
| the final measurement — no-arb, band, yr1-to-peak, per-entry-year, top-end | `MEASUREMENT.md` · `noarb/` |
| pins old → new | `PINS.md` |
| the owner review set, with this amendment as a fifth stage column | `../side_by_side/` |

## The three things worth an owner's eye

1. **The pedigree gap widened without a pedigree term.** The top-pick arm of the pedigree pair falls too
   (−15%) — it must, because a pick-3 player claiming the same 4-game re-rate is also making a large claim on
   a thin sample, and `s` does not read the pick. But it falls far less than the pick-35 arm (−45%), because
   its prior was already high, so **the same four games are a much smaller surprise**. The separation the
   owner asked stage 4 to open more than doubles (pure pedigree 1.358 → 1.949) and it emerges from the
   statistic itself.
2. **The change is symmetric, and that means seven players move UP.** `s` is an *absolute* log-ratio, so a
   four-game collapse from a high prior is shrunk toward that prior exactly as hard as a four-game breakout
   of the same log size — and the collapsed player's price rises. Owner law L-SYMMETRY (register item 108); a
   one-sided `max()` would be a branch, refused under L-SMOOTH. All seven are named. Largest lift **+51.52%**
   (Mitch Podhajski, whose 2 games ran at **0.06×** his projection).
3. **Yr1-to-peak went UP again** (whole cohort 1.4910 → 1.5068; deep picks 1.5692 → 1.6063), away from the
   relocation target, because the change cuts year-1 thin-record values and leaves the peak alone. Reported
   straight, compensated for nowhere. **The amendment does not resolve the act's return-trigger.**

## How to re-run

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add /home/claude/a1_landing landing/334-stage-b
RL_VENDOR=/home/claude/a1_landing/vendor bash /home/claude/a1_landing/bootstrap.sh   # Guard 5

export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=<workspace>/rl_after:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
export RL_REPO=/home/claude/a1_landing
export RL_FV=$RL_REPO/engine/forward_valuation
export RL_WORKDIR=<workspace>/rl_after

cd $RL_WORKDIR
rm -f rl_app_data.json
python3 rl_export.py          # PARITY + NUMÉRAIRE GUARD; board -> b56bbddea15fd48e35b5794b1b5e9e23
python3 s4_matrix_M1v7.py     # BOOK<->BOARD PARITY GATE
python3 one_source_selftest.py                        # PASSED, 143 / 0

# the tracking deliverables
S=$RL_REPO/docs/evidence/act_334B_2026-08-07/stage4_amend1
git -C $RL_REPO show 44950de:data/rl_build/rl_app_data.json > /tmp/board_stage4.json
python3 $S/enumerate_movers.py      /tmp/board_stage4.json $RL_WORKDIR/rl_app_data.json
python3 $S/near_projection_proof.py /tmp/board_stage4.json $RL_WORKDIR/rl_app_data.json
python3 $S/composition_check.py
RL_TAG=stage4a1 python3 $S/probes.py
RL_TAG=stage4a1 RL_OUT=$S python3 $S/boundary_did.py

# the measurement chain
cd $S/noarb && RL_OUT=$S/noarb python3 emit_matrix_338.py
mv per_entrant_338_confirmation.json per_entrant_338_stage4a1.json
python3 noarb_table_338.py per_entrant_338_stage4a1.json
python3 noarb_ext_338.py ; python3 goal_metrics.py

# the fit-coupling proof (dev shell — a DECLARED experiment, so NO RL_CONFIG_MODE)
unset RL_CONFIG_MODE
for W in 0 5.0 20.0; do RL_SUR_W=$W RL_V0SURF_REFIT=1 \
  python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify; done

# the kill-switch identity: set RL_SUR_W=0 in data/model_config.json, re-stamp config +
# expected_boot, rebuild -> board b490ae8b3bbd28b908ccb923ed8412c1, byte-exact to stage 4.
```
