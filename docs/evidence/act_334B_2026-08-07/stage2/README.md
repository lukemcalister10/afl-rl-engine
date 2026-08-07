# 334 stage B / stage 2 — the per-pick re-anchor, derived from the stage-1 matrix

1. **Basis.** The walk-forward matrix was RE-EMITTED on the stage-1 engine (head `e3527be4`, store `37ced3ce`, v0surf `af556bdca53d`, 2645 records) by the committed `emit_matrix_338.py`. The harness loader's identity pins held; the ND teaching population is 1197 (teaches_curve & pick 1-64 & class 2004-2022). The stage-1-basis no-arb table reproduces the amend3 control exactly — yr1 **1.021**, yr4 **1.535** — so the surface did not move under stage 1.
2. **Peak year = YEAR 4**, derived in-script as the argmax of the whole-cohort ratio over the *full-inclusion* years (n_incl == 1197, i.e. years 0-4). Year 5's 1.534 is on a smaller, attrition-shifted population and is not comparable; restricting to full inclusion also guarantees n(p) is identical at year 0 and at peak.
3. **Construction.** Per pick p: `R_raw(p) = mean(year 4) / mean(year 0)` over that pick's cohort, **busts in at 0** (no row filtered). `R_s(p)` = n(p)-weighted Gaussian kernel smoothing along the pick axis — continuous in the pick index, **no binning, no bands, no bucket steps** (verified: the first difference of R_s is nonzero at all 63 adjacent pairs, min |d1| = 0.000211). `f(p) = R_s(p) / 1.40`; `new(p) = old(p) × f(p)`.
4. **The target's role.** 1.40 appears **only** in `derive_reanchor_stage2.py`, as the divisor setting the level of f. It is not written into any engine file and enters no runtime path. The only artefact leaving this stage is the ladder itself.
5. **f is not uniform** — min 0.888858 (pick 64), max 1.122087 (pick 1), mean 1.057646, max/min 1.2624. A uniform scalar is barred and the script asserts against it.
6. **DISCLOSED DEVIATION — bandwidth.** h = 8.0 picks was chosen, *not* the LOO argmin. LOO's surface is nearly flat (cv 0.2398 at h=8 vs 0.2318 at its argmin h=21 — 3.5%) because per-pick sampling noise (n(p) = 14-19) swamps the signal; its argmin at a third of the whole axis drives R_s toward a global constant, i.e. toward the barred uniform scalar. h=8 is the midpoint of the directive's stated sensible range (~6-10). The full CV surface is printed in the log.
7. **Checks.** (a) Monotone non-increasing on the exact product: **PASS**, no isotonic projection needed. (a2) One rounding collision at pick 19 (exact 1100.145 → 1100.010, both rounding to 1100) broke this file's own `r104_9_strict_descent` rule; a minimal integer repair moved pick 19 to 1099 — **1 pick, 1 board point**, disclosed, re-checked PASS. (b) Smoothness: the only out-of-line drops (picks 9, 10) are inherited from the *old* ladder — the same test flags the same two picks on the old ladder — not introduced by f.
8. **Residual.** Check (c) as specified — weighted mean of `R_s(p)/f(p)` — returns 1.400000, but it is a **tautology**: f is defined as R_s/1.40, so it equals 1.40 for any data whatsoever. The measured check is (c2), the weighted mean of `R_raw(p)/f(p)` over the unsmoothed data: **1.392630** (−0.0074 from target), the gap being the smoother's bias.
9. **Ladder identity.** N32 payload md5 `df766dff94657940e2a892e91da5a6e2` → **`9ddbc5a76373d8066ab852dee136eb3d`**; file md5 **`41692b9db8e01d46df1b7e3cca09fcfe`**. Only the 64 `curve` values changed; key order, types (int) and every other field are byte-preserved.

## Caveats — read before expecting coherence

- **The board is NOT rebuilt this stage.** The frozen year-zero surface is coupled to the curve, so a curve-only board is impossible without stage 3's refit. That is expected, not a failure. `data/expected_boot.json`, `data/v0surf.pkl` and `data/rl_build/rl_app_data.json` are deliberately **untouched**.
- **`curve_md5` inside the file is now STALE** (still `df766dff`). It is a pin and this stage does not move pins. Stage 3 re-stamps it.
- **The numeraire pin is broken, deliberately and openly.** `new(1) = 3000 × 1.122087 = 3366`, so `numeraire_pin1_3000` no longer holds and the committed harness's `ladder[0] == 3000` assert will fire. This stage's spec is `new = old × f` with no renormalisation; re-pinning the numeraire is a board-level decision belonging with stage 3.
- **The true residual is measured only after stage 3's refit.** 1.392630 here is a first-order, curve-side figure computed against the *frozen* surface. Once the surface is re-fit the whole-cohort residual will move. The convergence rule allows **one refinement iteration** of this re-anchor if stage 3's measured residual misses 1.40 by more than the agreed tolerance.

## Manifest

| file | what |
|---|---|
| `derive_reanchor_stage2.py` | the derivation, self-contained and re-runnable from this directory |
| `per_entrant_338_stage1basis.json` | the re-emitted stage-1-basis matrix, md5 `b82e12c139a568868c13a7ddd5d5529e` |
| `noarb_table_stage1basis.{txt,json}` | the stage-1-basis no-arb table (the baseline control) |
| `per_pick_reanchor_table.txt` | the 64-row R_raw / R_s / f / old / new table, per-pick, no buckets |
| `per_pick_reanchor.json` | the same, machine-readable, plus the LOO CV surface and the repair record |
| `stage2_derivation_log.txt` | the full checks output of the run that wrote the ladder |
| `pvc_curve_v2_PRE_stage2.json` | the ladder as it stood before this stage |
| `emit_matrix_338.py`, `noarb_table_338.py`, `noarb_ext_338.py`, `harness_pvc_REPINNED_pass3.py` | the committed stage-1-basis scripts (the derivation imports the loader and `value_at` from two of them rather than re-implementing either) |

### Regeneration

```
cd docs/evidence/act_334B_2026-08-07/stage2
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor \
RL_CONFIG_MODE=gate RL_REPO=$PWD/../../../.. RL_OUT=$PWD \
python emit_matrix_338.py                      # -> per_entrant_338_confirmation.json (rename to *_stage1basis.json)
python noarb_table_338.py per_entrant_338_stage1basis.json
python derive_reanchor_stage2.py               # dry; add --write <path to engine/rl_after/pvc_curve_v2.json>
```
