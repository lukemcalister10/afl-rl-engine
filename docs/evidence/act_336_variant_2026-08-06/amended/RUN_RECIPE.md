# #336 ADDENDUM 1 — the AMENDED bust-inclusive reference layer. RUN RECIPE + evidence index

**Fired** per issue #336, ADDENDUM 1 of 2026-08-06 (owner word *"Amend and re-run."*), which supersedes the
repair-form paragraph of the VARIANT DIRECTIVE. Everything else in that directive stands.

**This is an EXPERIMENT.** Nothing landed on main, no pin moved on main, the variant code lives on
`variant/336-bust-inclusive` and is never merged. This directory is SCRATCH. The first cut's run lives beside
it in `../act336/` and is retained unaltered as the superseded comparison.

**MANDATED CAPTION, carried on every sheet in this directory:**
> reference layer bust-inclusive; year-zero surface held at the shipped survivors-basis fit;
> the joint re-derivation is #334 stage B, after the ruling.

---

## THE AMENDMENT, in one paragraph

At every level-anchor site the probability is **career-level P(ever establishes | position × pick band)** —
never established-by-tenure. Tenure enters only through **#338 window MEMBERSHIP** (who is in the
denominator), never as a probability discount on the anchor. `E[level] = P(ever est) × E[level | ever
establishes]`, with the conditional level still tenure-resolved from establishers' seasons at that tenure.

Only ONE of the two levers actually moved: **`engine/forward_valuation/par_build.py`**, whose `build_pest`
was keyed `(position × band × TENURE)` — the named defect. **`engine/rl_after/rl_model.py`** (BPK / POOL /
BASEPK_REG) was ALREADY career-level and is unchanged in substance; this run adds only a note there
recording that both anchors were checked against the amendment, not just the one that moved. That is why
every BPK/POOL/BASEPK_REG figure and every monotonicity figure in this directory is identical to the first
cut's — it is the same table, correctly so.

---

## Identities

| | value |
|---|---|
| store | `37ced3ce` (all builds, unmoved) |
| engine head `_merged_recover.py` | `8f0e3eb1` (all builds, **untouched** — not one of the levers) |
| v0surf signature | `af556bdca53d`, frozen=True (all builds — **the surface is HELD**) |
| baseline `rl_model` / `fv` | `33f94073` / `d920557e` |
| first cut `rl_model` / `fv` (superseded) | `1b0cc66d` / `c9d9b541` |
| **AMENDED** `rl_model` / `fv` | `915a4c0c` / `61f4d32c` |
| CONTROL board | `113b36f898a32363c49c2a62fb809f4b` — **byte-reproduced, control PASSES** |
| first cut board (superseded) | `bc9f735a301626be75651b5fd5c0d200` |
| **AMENDED board** | `e52ee95dd56d8f5b670887d34aabe094` |
| branch / commit | `variant/336-bust-inclusive` @ `a7bff5a343af80a33a94924abab07a9606b472d4` (pushed) |
| parent commit (first cut) | `de507efda94d1ca5b6df9e9d4b63fb8647778060` |

---

## The recipe, exactly as run

```
export PATH="/root/rl_venv312/bin:$PATH"
S2=<this dir>
ENV="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
W=/home/claude/rl_workspace/rl_after
```

### 0. two clean checkouts

```
git worktree add --detach $S2/repo_main a82c0fe          # the same commit the first cut used
git worktree add $S2/repo_variant variant/336-bust-inclusive     # at de507ef, the first cut's code
```

The first cut's worktree (`../act336/repo_variant`) was detached to free the branch; its tree is otherwise
untouched and still serves the three-way comparison.

### 1. CONTROL — must byte-reproduce `113b36f8` before the variant is credited

```
cd $S2/repo_main && RL_VENDOR=/home/user/afl-rl-engine/vendor bash $S2/repo_main/bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$S2/repo_main RL_FV=$S2/repo_main/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json    # 113b36f898a32363c49c2a62fb809f4b   <-- CONTROL PASS
cp rl_app_data.json $S2/board_baseline.json
```

Log: `control_build.txt`.

### 2. the AMENDED P(ever establishes) strata, derived before the engine edit was measured

```
cd $W && env OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_REPO=$S2/repo_main RL_FV=$S2/repo_main/engine/forward_valuation RL_OUT=$S2 \
  RL_PERENTRANT=/home/user/afl-rl-engine/docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json \
  python3 $S2/derive_pest_amended.py         # -> pest_strata.txt / .json
```

`derive_pest_amended.py` is an adapted copy of `../act336/derive_pest.py`; the one substantive change is that
lever A is derived career-level. The by-tenure table is still computed and printed, labelled SUPERSEDED,
because the double-charge decomposition needs the exact factors the first cut fed.

### 3. the amendment, then the build

```
# edit engine/forward_valuation/par_build.py  (build_pest -> career-level; gather() -> no T index; report G)
# note-only edit to engine/rl_after/rl_model.py
python3 $S2/repin_variant.py $S2/repo_variant engines
    expected_boot rl_model  33f94073.. -> 915a4c0c..
    expected_boot fv        d920557e.. -> 61f4d32c..
    expected_boot engine_head 8f0e3eb1.. -> 8f0e3eb1..   (UNCHANGED — _merged_recover untouched)
cd $S2/repo_variant && RL_VENDOR=/home/user/afl-rl-engine/vendor bash $S2/repo_variant/bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$S2/repo_variant RL_FV=$S2/repo_variant/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json    # e52ee95dd56d8f5b670887d34aabe094
cp rl_app_data.json $S2/board_variant.json
```

Guard 5 HALTS the bootstrap on the moved file set — that halt is the guard working and was NOT patched away;
the SCRATCH CHECKOUT's pins were re-stamped by `repin_variant.py` (carried from `../act336/`, itself adapted
from `docs/evidence/act_326_2026-08-06/repin.py`). **The re-pin is deliberately NOT COMMITTED**: the branch
carries the two engine files and nothing else. `data/expected_boot.json` and `data/release_contract.json`
show as uncommitted build-harness edits in the variant worktree.

Log: `variant_build.txt`. **PARITY GATE PASS** (804 board values == engine gated `ev()`, eps=0).

### 4. board delta

```
RL_OUT=$S2 python3 $S2/board_diff_files.py $S2/board_baseline.json $S2/board_variant.json
```
Carried unchanged from the first cut (itself an adapted copy of the committed `tools/seat/board_diff.py`,
changed only to take file paths and extended with top-5 cuts/lifts and the scale-vs-relative separation).
Output: `board_delta.txt` / `.json`.

### 5. the DOUBLE-CHARGE CHECK (addendum item 2, the required proof)

```
# run the same dump in all three builds; bootstrap the matching repo before each
for TAG/REPO in (baseline, repo_main) (variant_prior, ../act336/repo_variant) (variant_amended, repo_variant):
  cd $REPO && bash bootstrap.sh
  env $ENV PYTHONPATH=$W:/home/claude/rl_vendor RL_CONFIG_MODE=gate RL_TAG=$TAG RL_OUT=$S2 \
    RL_REPO=$REPO RL_FV=$REPO/engine/forward_valuation RL_WORKDIR=$W python3 $S2/decompose_336b.py
python3 $S2/compare_decomp.py        # -> double_charge.txt / .json
```

`decompose_336b.py` dumps, per player, the ANCHOR block (`par_at`, `basepk`, `lvl_eff`), the BAND block
(`b6` quantiles) and the OUTPUT block (`ev`, `v0_start`). `compare_decomp.py` does the arithmetic:
`dlog(ev) = dlog(anchor) + dlog(band_q50/anchor) + dlog(ev/band_q50)`, exactly additive.

The ten-player cohort is the ten largest ABSOLUTE cuts of the FIRST CUT's board delta — fixed by the prior
run's evidence, before the amended numbers existed, so it cannot have been chosen to flatter the amendment.

### 6. hump — the noarb_338 stack, re-run on the amended variant

```
cd $S2/noarb_variant && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_REPO=$S2/repo_variant RL_FV=$S2/repo_variant/engine/forward_valuation \
  RL_WORKDIR=$W RL_OUT=$S2/noarb_variant python3 emit_matrix_338.py     # ~4 min, 24 as-of years
cd $S2/noarb_{baseline,variant} && OPENBLAS_NUM_THREADS=1 python3 noarb_table_338.py && python3 noarb_ext_338.py
```

The three harness identity pins (`EXPECT_STORE`, `EXPECT_V0SURF`, `EXPECT_N`) were RE-MEASURED on the amended
matrix and all three came back unchanged — `37ced3ce` / `af556bdca53d` / n=1197 — so no re-pointing was
required and no assert was patched. The matrices themselves DO differ (`5fb617d0` baseline vs `6155c2c9`
amended vs `f4b3986a` first cut), which repeats the first cut's finding: **the harness identity pins cannot
discriminate this basis move.** `rl_model` / `fv` are the only identities that separate the runs.

### 7. monotonicity proofs and the par surface reports

```
cd $W && ... RL_OUT=$S2 python3 $S2/monotonicity_proofs.py               # -> monotonicity.txt / .json
cd $W && ... python3 $S2/repo_variant/engine/forward_valuation/par_build.py > $S2/par_report_variant.txt
cd $W && ... python3 $S2/repo_main/engine/forward_valuation/par_build.py   > $S2/par_report_baseline.txt
```

---

## File index

| file | what it is |
|---|---|
| `COMPARISON_CURRENT_vs_BUST_INCLUSIVE_AMENDED.txt` | **the draft owner sheet** (COMPARISON pattern; amendment stated at the top; caption carried) |
| `double_charge.txt` / `.json` | **the addendum's required proof** — anchor vs band decomposition, n=10, plus the below-draft-day test |
| `hump_compare.txt` / `hump_rows.json` | the year-ratio table three ways, both appreciation headlines, the pick-cut split |
| `board_delta.txt` / `.json` | mover count, ΣΔ, age buckets, top 5 cuts/lifts, scale vs relative |
| `monotonicity.txt` / `.json` | unclamped monotonicity, the Ablett cell, the three leave-one-out pairs |
| `pest_strata.txt` / `.json` | the AMENDED career-level P per lever, raw counts, pooling declared, the SUPERSEDED by-tenure table, and the per_entrant cross-check |
| `par_report_baseline.txt` / `par_report_variant.txt` | the par surface both sides; §G is the P disclosure |
| `MD5S.txt` | every identity and file md5 quoted anywhere in this directory |
| `variant_amendment.patch` | the amendment diff alone (`de507ef..a7bff5a`) |
| `variant_full.patch` | the whole variant against main (`a82c0fe..a7bff5a`) |
| `board_baseline.json` / `board_variant.json` | the control board and the amended board |
| `decomp_{baseline,variant_prior,variant_amended}.json` | the raw per-player anchor/band/output dumps |
| `noarb_baseline/`, `noarb_variant/` | the matrices, the tables, the harness copies, the emit log |
| `control_build.txt`, `variant_build.txt`, `*bootstrap*.txt` | the build logs |
| `derive_pest_amended.py`, `decompose_336b.py`, `compare_decomp.py` | the new instruments (sources named in their headers) |
| `board_diff_files.py`, `monotonicity_proofs.py`, `repin_variant.py`, `derive_pest.py`, `proto_bpk.py` | carried unchanged from `../act336/` |
| `repo_main/`, `repo_variant/` | the two git worktrees the builds ran from |

---

## Scope fence — held

* Two code files on the branch, never merged: `engine/forward_valuation/par_build.py` (the amendment) and
  `engine/rl_after/rl_model.py` (note only). `git show --stat a7bff5a` shows exactly those two.
* No `RL_V0SURF_REFIT`. The frozen surface loaded unchanged in every build (`v0surf_frozen=True`, signature
  `af556bdca53d`) — the ruled and disclosed basis.
* `main` untouched — `origin/main` still at `a82c0fe`, unmoved by this act. No pin moved outside
  `$S2/repo_variant` (uncommitted).
* `rl_passmark.json` / `params.json` provenance hole: OUT OF SCOPE, unswept, untouched.

## Reds carried out of this run (reported, not patched)

1. **year-1-to-peak 1.439 vs baseline 1.394** — the relocation is ~90% undone but not fully. Residual is
   entirely picks 21-64 and traces to a genuine career-level establishment rate, not to a double charge.
2. **5 of 42 unclamped pick-monotonicity violations** in the bust-inclusive BASEPK_REG. Unchanged from the
   first cut (that lever did not move). Not re-clamped, per the directive.
3. **harry-dean prices 2 points (0.999x) below his draft-day value.** Named cause: the mixed basis the
   mandated held surface creates — an 8.47% uniform board rescale against an un-rescaled draft-day surface.
   1.09x once the uniform rescale is removed. His anchor moved only −4 log points.
