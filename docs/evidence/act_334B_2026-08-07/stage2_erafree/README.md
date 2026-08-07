# 334 stage B / stage 2 RE-DERIVED ON THE ERA-FREE BASIS — the per-pick re-anchor

1. **Supersedes `../stage2/`**, retained as history: that ladder was taught through the engine's `REF/era` multiplier, which the owner ruling (stage ER, `f7ae027`) abolished. Method here is **unchanged** — same loader, same `value_at`, same kernel, same checks; only the basis moved, engine head `e3527be4` → **`a0a20d6e`**.
2. **The era-free hump** (whole cohort n=1197, busts at 0), years 0-9: **1.0000 / 1.0211 / 1.2792 / 1.4476 / 1.5345 / 1.5335 / 1.4946 / 1.2986 / 1.0692 / 0.8281**. **Peak = year 4**, argmax over the full-inclusion years 0-4.
3. **Delta vs the prior era-adjusted basis** (1.021/1.279/1.448/1.535) is tiny and uniformly negative: `+0.0000 / −0.0000 / −0.0001 / −0.0002 / −0.0006` at years 0-4; max |delta| anywhere is `−0.0009` (year 6).
4. **That difference is the finding:** era normalization was **very nearly a no-op on this ratio** — it scaled numerator and denominator of the same cohort alike, and year-0 means are identical to the cent (839.18) because `v0_start` is a draft-day pedigree value with no scoring history for the multiplier to touch. The ladder was still wrong at the root to keep; the correction it needed is just small.
5. **Construction:** `R_raw(p) = mean(year 4)/mean(year 0)` per pick, busts in every denominator; `R_s` = n(p)-weighted Gaussian kernel along the pick axis; `f(p) = R_s(p)/1.40`; `new(p) = old(p) × f(p)`.
6. **Bandwidth h = 8.0 picks — deliberately NOT the LOO argmin (h=21)**, reason restated from the prior run: the CV surface is flat (0.2397 vs 0.2316, 3.5%) and h=21 collapses R_s toward a global constant, i.e. toward the **barred uniform scalar**; h=8 is the midpoint of the directive's stated range.
7. **No binning, no bands, no bucket steps anywhere, including the reported tables** — the 1-20/21-64 split shown in `noarb_table_erafree.txt` is a **readout only**; no estimator bands on it.
8. **The target's role:** 1.40 lives ONLY in `derive_reanchor_stage2_erafree.py`, as the divisor setting f's level. It is written into no engine file and enters no runtime path — this is a **teaching stage only**.
9. **f is non-uniform** (asserted in-script): min 0.888844 (pick 64), max 1.121405 (pick 1), mean 1.057449, max/min 1.2616.
10. **Checks:** monotone non-increasing on the exact product **PASS** (no isotonic projection needed); strict integer descent had **2 rounding collisions** (picks 18, 19 — exact product falls, both rounded to 1100), minimally repaired to 1099 (−1) and 1098 (−2), re-check PASS; smoothness — the only out-of-line drops (picks 9, 10) are **inherited from the old ladder**, the same test flags the same two picks on it.
11. **Residual:** the specified `R_s/f` check returns 1.400000 but is a **tautology** (f ≡ R_s/1.40, so it equals 1.40 for any data); the honest measured figure is the n-weighted mean of `R_raw(p)/f(p)` = **1.392606** (−0.0074), the gap being smoother bias.
12. **Ladder identity:** payload md5 `df766dff…` → **`77408ecdad734a7816bfdd9f3be7568a`**; file md5 `988135ef…` → **`0c798f363418da038be93c8473fe54de`**. Only the 64 `curve` values changed; key order, field order and int types byte-preserved.

## Caveats — read before expecting coherence

- **No board rebuild this stage.** `data/v0surf.pkl`, `data/expected_boot.json` and the board are untouched; a curve-only board is impossible without stage 3's refit. Expected, not a failure.
- **`curve_md5` inside the file is STALE** (still `df766dff`). It is a pin; **stage 3 re-stamps it**, per the directive.
- **The numeraire pin is broken, openly.** `new(1) = 3000 × 1.121405 = 3364`, so `numeraire_pin1_3000` no longer holds and the committed harness's `ladder[0] == 3000` assert will fire. The spec here is `new = old × f` with no renormalisation; **re-pinning is stage 3's.**
- **1.392606 is a first-order, curve-side figure** measured against the frozen surface. The true residual is known only after stage 3's refit.

## Instrument era-scaling audit (step 1 of the directive)

`emit_matrix_338.py`, `noarb_table_338.py`, `noarb_ext_338.py`, `harness_pvc_REPINNED_pass3.py` were grepped for `era`/`REF` before use. **Nothing was found and nothing was stripped.** The only hits are `MA.BASE_REF` / `MA.AGE_REF` in the emitter's walk-forward loop — the as-of **anchor years** that define the matrix (the evaluation date), not a per-year score rescale — plus prose ("pass-3-era") and `enumerate` substrings. The engine itself carries four `era` hits, all four comments recording the removal. Harness pins held unmoved: store `37ced3ce`, v0surf `af556bdca53d`, EXPECT_N 1197, 2645 records; **no re-point was needed.**

## Manifest

| file | what |
|---|---|
| `derive_reanchor_stage2_erafree.py` | the derivation, self-contained and re-runnable from this directory |
| `per_entrant_338_erafree.json` | the era-free walk-forward matrix, md5 `e4b38436d3890e05c671a0170fde5dfc` (3.4MB, committed) |
| `noarb_table_erafree.{txt,json}` | the era-free no-arb table (years 0-7, whole cohort + both pick splits) |
| `noarb_ext_erafree.txt` | the extended cuts — **years 0-9**, the 2020 class, the recency windows |
| `per_pick_reanchor_table.txt` | the 64-row `R_raw / R_s / f / old / new` table, per-pick, no buckets |
| `per_pick_reanchor.json` | the same machine-readable, plus the LOO CV surface, band splits, prior-basis deltas, repair record |
| `stage2ef_derivation_log.txt` | the full checks output of the run that wrote the ladder |
| `pvc_curve_v2_PRE_stage2ef.json` | the ladder as it stood before this stage (`df766dff` payload) |
| `emit_matrix_338.py`, `noarb_table_338.py`, `noarb_ext_338.py`, `harness_pvc_REPINNED_pass3.py` | the committed instruments (the derivation imports the loader and `value_at` rather than re-implementing either) |

### Regeneration

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add /home/claude/s2ef_landing landing/334-stage-b
RL_VENDOR=/home/claude/s2ef_landing/vendor bash /home/claude/s2ef_landing/bootstrap.sh   # engine a0a20d6e
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
export RL_REPO=/home/claude/s2ef_landing
export RL_FV=/home/claude/s2ef_landing/engine/forward_valuation
cd /home/claude/s2ef_landing/docs/evidence/act_334B_2026-08-07/stage2_erafree
export RL_OUT=$PWD

python emit_matrix_338.py                              # -> per_entrant_338_confirmation.json
mv per_entrant_338_confirmation.json per_entrant_338_erafree.json   # md5 e4b38436d3890e05c671a0170fde5dfc
python noarb_table_338.py per_entrant_338_erafree.json > noarb_table_erafree.txt
mv noarb_table_338.json noarb_table_erafree.json
ln -sf per_entrant_338_erafree.json per_entrant_338_confirmation.json   # noarb_ext_338.py hardcodes this name
python noarb_ext_338.py > noarb_ext_erafree.txt        # years 0-9
rm -f per_entrant_338_confirmation.json

python derive_reanchor_stage2_erafree.py               # dry run; prints every check
python derive_reanchor_stage2_erafree.py --write ../../../../engine/rl_after/pvc_curve_v2.json
```
