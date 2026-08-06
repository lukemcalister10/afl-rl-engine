# #336 VARIANT — the bust-inclusive reference layer. RUN RECIPE + evidence index

**Fired** per issue #336, VARIANT DIRECTIVE 2026-08-06 (owner word "Fire 336").
**This is an EXPERIMENT.** Nothing landed on main, no pin moved on main, the variant code lives on
`variant/336-bust-inclusive` and is never merged. This directory is SCRATCH — it is not committed to
main; the evidence commit is the seam's call after its non-authoring audit.

**MANDATED CAPTION, carried on every sheet in this directory:**
> reference layer bust-inclusive; year-zero surface held at the shipped survivors-basis fit;
> the joint re-derivation is #334 stage B, after the ruling.

---

## Identities

| | value |
|---|---|
| store | `37ced3ce` (both sides, unmoved) |
| engine head `_merged_recover.py` | `8f0e3eb1` (both sides, **untouched** — not one of the two levers) |
| v0surf signature | `af556bdca53d`, frozen=True (both sides — **the surface is HELD**) |
| baseline `rl_model.py` / fv identity | `33f94073` / `d920557e` |
| variant `rl_model.py` / fv identity | `1b0cc66d` / `c9d9b541` |
| CONTROL board | `113b36f898a32363c49c2a62fb809f4b` — **byte-reproduced, control PASSES** |
| VARIANT board | `bc9f735a301626be75651b5fd5c0d200` |
| branch / commit | `variant/336-bust-inclusive` @ `de507efda94d1ca5b6df9e9d4b63fb8647778060` |

---

## The recipe, exactly as run

```
export PATH="/root/rl_venv312/bin:$PATH"
S=<this dir>
ENV="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
W=/home/claude/rl_workspace/rl_after
```

### 0. two clean checkouts off the same commit

```
git worktree add --detach $S/repo_main a82c0fe          # current origin/main
git branch variant/336-bust-inclusive a82c0fe
git worktree add $S/repo_variant variant/336-bust-inclusive
```

### 1. CONTROL — the baseline board (must byte-reproduce 113b36f8 before the variant is credited)

```
cd $S/repo_main && RL_VENDOR=/home/user/afl-rl-engine/vendor bash $S/repo_main/bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$S/repo_main RL_FV=$S/repo_main/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json    # 113b36f898a32363c49c2a62fb809f4b   <-- CONTROL PASS
cp rl_app_data.json $S/board_baseline.json
```

Log: `control_build.txt`.

### 2. the P(establishes) strata (derived before any engine code was written)

```
cd $W && env OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_REPO=$S/repo_main RL_FV=$S/repo_main/engine/forward_valuation RL_OUT=$S \
  RL_PERENTRANT=/home/user/afl-rl-engine/docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json \
  python3 $S/derive_pest.py                       # -> pest_strata.txt / .json
cd $W && ... python3 $S/proto_bpk.py              # -> proto_bpk.txt / .json (the pre-write prototype)
```

### 3. VARIANT — the two-file change, then the build

The variant moves `rl_model.py` and the `forward_valuation` source set, so **Guard 5 HALTS the
bootstrap.** That halt is the guard working, and it was NOT patched away: the SCRATCH CHECKOUT's pins
were re-stamped by `repin_variant.py` (adapted from `docs/evidence/act_326_2026-08-06/repin.py`,
same recipe, plus the `fv` pin #326 did not have to move).

**The re-pin is deliberately NOT COMMITTED.** The branch carries the two engine files and nothing
else; `data/expected_boot.json` and `data/release_contract.json` show as uncommitted build-harness
edits in the variant worktree. No pin moved anywhere outside this scratch tree.

```
python3 $S/repin_variant.py $S/repo_variant engines
    expected_boot rl_model  33f94073.. -> 1b0cc66d..
    expected_boot fv        d920557e.. -> c9d9b541..
    expected_boot engine_head 8f0e3eb1.. -> 8f0e3eb1..   (UNCHANGED — _merged_recover untouched)
cd $S/repo_variant && RL_VENDOR=/home/user/afl-rl-engine/vendor bash $S/repo_variant/bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$S/repo_variant RL_FV=$S/repo_variant/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json    # bc9f735a301626be75651b5fd5c0d200
cp rl_app_data.json $S/board_variant.json
```

Log: `variant_build.txt`. PARITY GATE PASS (804 board values == engine gated ev(), eps=0) on both sides.

### 4. board delta

```
RL_OUT=$S python3 $S/board_diff_files.py $S/board_baseline.json $S/board_variant.json
```
`board_diff_files.py` is an adapted COPY of the committed `tools/seat/board_diff.py` — changed only to
take FILE PATHS instead of git revs, and extended with top-5 (not top-3) cuts/lifts and the
scale-vs-relative separation the directive requires. Output: `board_delta.txt` / `.json`.

### 5. hump ratio — the noarb_338 stack, re-run on the variant

Copies of `emit_matrix_338.py`, `noarb_table_338.py`, `noarb_ext_338.py`,
`harness_pvc_REPINNED_pass3.py` live in `noarb_variant/`; `noarb_baseline/` holds the same table
scripts run against the COMMITTED baseline matrix (which was itself emitted on this exact store and
engine head, so it IS the control for this measurement).

```
cd $S/noarb_variant && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_REPO=$S/repo_variant RL_FV=$S/repo_variant/engine/forward_valuation \
  RL_WORKDIR=$W RL_OUT=$S/noarb_variant python3 emit_matrix_338.py     # ~3 min, 24 as-of years
cd $S/noarb_{baseline,variant} && OPENBLAS_NUM_THREADS=1 python3 noarb_table_338.py && python3 noarb_ext_338.py
```

**ON THE HARNESS PINS — a finding, not a formality.** The directive expected the identity pins to
halt on the moved basis. **THEY DID NOT, and that is itself worth reporting.** All three were
RE-MEASURED on the variant matrix rather than assumed, and all three came back unchanged:

| pin | baseline | variant | verdict |
|---|---|---|---|
| `EXPECT_STORE` | `37ced3ce` | `37ced3ce` | unmoved — the store did not move |
| `EXPECT_V0SURF` | `af556bdca53d` | `af556bdca53d` | unmoved — **the frozen surface is HELD, by design** |
| `EXPECT_N` | 1197 | 1197 (re-counted) | unmoved — the population filter is blind to the levers |

So no re-pointing was required and no assert was patched. The matrices themselves DO differ
(`5fb617d0` vs `f4b3986a`), which means **the harness identity pins cannot discriminate this basis
move** — the same blindness `_v0surf_sig` has to par/BPK, one layer out. `rl_model` / `fv` are the
only identities that separate the two runs and they are recorded in `MD5S.txt`.

NON-VACUITY was proven on the variant matrix — each of the three asserts was made to fire by
perturbing its pin, then restored:
```
EXPECT_STORE  deadbeef      -> assert FIRED
EXPECT_V0SURF 000000000000  -> assert FIRED
EXPECT_N      1198          -> assert FIRED
```

### 6. monotonicity proofs and the par surface reports

```
cd $W && ... RL_OUT=$S python3 $S/monotonicity_proofs.py          # -> monotonicity.txt / .json
cd $W && ... python3 $S/repo_variant/engine/forward_valuation/par_build.py > $S/par_report_variant.txt
cd $W && ... python3 $S/repo_main/engine/forward_valuation/par_build.py    > $S/par_report_baseline.txt
```

---

## File index

| file | what it is |
|---|---|
| `COMPARISON_CURRENT_vs_BUST_INCLUSIVE.txt` | **the draft owner sheet** (the `COMPARISON_OLD_vs_NEW` pattern) |
| `MD5S.txt` | every identity and file md5 quoted anywhere in this directory |
| `variant.patch` | the committed two-file diff |
| `board_baseline.json` / `board_variant.json` | the two boards |
| `board_delta.txt` / `.json` | mover count, ΣΔ, age buckets, top 5 cuts/lifts, scale vs relative |
| `hump_compare.txt` | the year-ratio table both sides, all three pick cuts |
| `monotonicity.txt` / `.json` | the unclamped monotonicity measurement, the Ablett cell, the three spot pairs |
| `pest_strata.txt` / `.json` | P(establishes) per (position × band × tenure), raw counts, n distribution, and the live-vs-per_entrant.json cross-check (14 of 48 strata differ, max \|dP\| 0.0435 — population, not method; see the sheet §6) |
| `proto_bpk.txt` / `.json` | the pre-write prototype (construction measured before the engine was edited) |
| `par_report_baseline.txt` / `par_report_variant.txt` | the par surface both sides; §G is the P disclosure |
| `noarb_baseline/`, `noarb_variant/` | the matrices, the tables, the harness copies, the emit log |
| `control_build.txt`, `variant_build.txt` | the two board build logs |
| `derive_pest.py`, `proto_bpk.py`, `board_diff_files.py`, `monotonicity_proofs.py`, `repin_variant.py` | the instruments, all adapted copies with their sources named in their headers |
| `repo_main/`, `repo_variant/` | the two git worktrees the builds ran from |

---

## Scope fence — held

* Two code files changed, on a branch, never merged: `engine/forward_valuation/par_build.py`,
  `engine/rl_after/rl_model.py`. `git show --stat` on the branch commit shows exactly those two.
* No `RL_V0SURF_REFIT`. The frozen surface loaded unchanged on both sides (`v0surf_frozen=True`,
  signature `af556bdca53d`), which is the ruled and disclosed basis.
* `main` untouched. No pin moved outside `$S/repo_variant` (uncommitted).
* `rl_passmark.json` / `params.json` provenance hole: OUT OF SCOPE, unswept, untouched.
