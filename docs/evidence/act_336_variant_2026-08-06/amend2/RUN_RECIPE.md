# #336 AMENDMENT 2 — resolved-state conditioning. RUN RECIPE + evidence index

**Fired** per issue #336, OWNER CATCH 2 (comment 5205603101) and **AMENDMENT 2 FIRED** (comment 5205615726),
owner word in-channel 2026-08-06 *"amend and rerun"*. Supersedes the conditioning of Addendum 1; Addendum 1's
career-level P and everything else in the VARIANT DIRECTIVE stand.

**This is an EXPERIMENT.** Nothing landed on main, no pin moved on main, the variant code lives on
`variant/336-bust-inclusive` and is never merged. This directory is SCRATCH. The two prior runs live beside it
in `../act336/` (first cut) and `../act336b/` (amendment 1) and are retained unaltered.

**MANDATED CAPTION, carried on every sheet in this directory:**
> reference layer bust-inclusive; year-zero surface held at the shipped survivors-basis fit;
> the joint re-derivation is #334 stage B, after the ruling.

---

## THE AMENDMENT, in one paragraph

The reference a REAL player regresses toward conditions on what has already RESOLVED for him.
Establishment is one season of >= 6 games (`build_cohort_book.py:181-185`), read on his own store record as of
the valuation. An **ESTABLISHED** player anchors to `E[level | ever establishes]` with **no probability
discount**; an **UNRESOLVED** player carries the full bust-inclusive expectation
`P(ever establishes) x E[level | ever establishes]`, with the career-level P of Addendum 1 (tenure only as
window membership). Busts stay in every establishment-rate denominator. The conditional level was also
de-survivored on the tenure axis, so an establisher who faded still teaches at his realized level.

**Structural change forced by the amendment:** under Addendum 1 the P factor was folded into the fitted par
surface, so ONE surface served every consumer. Two states need two anchors, so the fit is now the CONDITIONAL
level and **P is applied at the consumer, once, per player**. That also makes P an exact per-player factor
instead of one smeared through a kernel regression over log-pick.

**Scope fence, widened by the amendment's own terms and recorded here:** per-player conditioning cannot live
inside the original two-file fence, because a class table has no player in it. The amendment names the sites
(lvl_par, the pedigree pole blend, the BPK-anchored per-player consumers), which live in four files:

| file | what changed |
|---|---|
| `engine/forward_valuation/par_build.py` | fit = conditional level (no P folded in); tenure gate `>=6g` -> `>=1g AND ever-established`; `pest_of()` / `resolved_336()` exposed |
| `engine/forward_valuation/par_redesign.py` | `par_at` = unconditional (picks/synthetics); new `par_at_est`, `par_at_p`; `lvl_par` routes through `par_at_p` |
| `engine/rl_after/_merged_recover.py` | `_par_prior`, `par_pole` (+ the `recover()` denominator), the staleness bar; pole prewarm now warms both states |
| `engine/rl_after/rl_model.py` | `BASEPK_EST` / `POOL_COND336` / `basepk_c_p` / `_resolved_336`; five per-player consumers rewired |

**Deliberately left UNCONDITIONAL:** `pick_raw`, `base_prod`, the ISO pick guard and the pole prewarm. A pick
has no resolved state and must carry the full entrant risk. Gated on `_isreal` so a 2x18-game synthetic cannot
read as "established". `rl_export.py:349` (`rec['relc']`, a display field) is enumerated and NOT touched.

---

## Identities

| | value |
|---|---|
| store | `37ced3ce` (all builds, unmoved) |
| v0surf signature | `af556bdca53d`, frozen=True (all builds — **the surface is HELD**, no `RL_V0SURF_REFIT`) |
| baseline `rl_model` / `engine_head` | `33f94073` / `8f0e3eb1` |
| **AMEND-2** `rl_model` / `engine_head` / `fv` | `3b6d12c7` / `3345b3fc` / `432f45a2` |
| **CONTROL board** | `113b36f898a32363c49c2a62fb809f4b` — **byte-reproduced, control PASSES** |
| **AMEND-2 board** | `ecfc824b38d428eae38221eff5073f0e` |
| baseline no-arb matrix | `5fb617d0…` — reproduces `../act336b/`'s, a **second control** |
| AMEND-2 no-arb matrix | `7307bb26…` |
| branch / commit | `variant/336-bust-inclusive` @ `f7a16b5cf6279455eb30d213476eafcd0fe97346` (pushed) |
| parent (amendment 1) | `a7bff5a343af80a33a94924abab07a9606b472d4` |
| `origin/main` before / after | `a8de737…` / `a8de737…` — **UNMOVED** |

---

## The recipe, exactly as run

```
export PATH="/root/rl_venv312/bin:$PATH"
C=<this dir>
ENV="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
W=/home/claude/rl_workspace/rl_after
```

### 0. two clean worktrees
```
git worktree add --detach $C/repo_main a82c0fe        # the same commit both prior cuts used
git worktree add $C/repo_variant variant/336-bust-inclusive   # at a7bff5a, amendment 1's code
```
`../act336b/repo_variant` was detached to free the branch; its tree is otherwise untouched.

### 1. CONTROL — must byte-reproduce `113b36f8` before the variant is credited
```
cd $C/repo_main && RL_VENDOR=/home/user/afl-rl-engine/vendor bash bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$C/repo_main RL_FV=$C/repo_main/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json   # 113b36f898a32363c49c2a62fb809f4b   <-- CONTROL PASS
cp rl_app_data.json $C/board_baseline.json
```
Log: `control_build.txt`.

### 2. the strata, derived BEFORE the engine edit was written
```
cd $W && env OPENBLAS_NUM_THREADS=1 PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_REPO=$C/repo_main RL_FV=$C/repo_main/engine/forward_valuation RL_OUT=$C \
  python3 $C/derive_a336c.py        > $C/strata_a2.txt      # P, E[level|est], the A-factors, the BPK cells
  python3 $C/derive_cond_variants.py > $C/cond_variants.txt  # the THREE readings of E[level|established]
```
`derive_cond_variants.py` is the instrument that decided the one genuinely ambiguous clause in the
amendment ("computed over ALL establishers… never over survivors-at-that-tenure"). Its three readings and
the recorded rule that barred the third are in `cond_variants.txt` and quoted in the sheet.

### 3. the amendment, then the build
```
# edit the four files listed above
python3 $C/repin_variant.py $C/repo_variant engines
cd $C/repo_variant && RL_VENDOR=/home/user/afl-rl-engine/vendor bash bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$C/repo_variant RL_FV=$C/repo_variant/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json   # ecfc824b38d428eae38221eff5073f0e
cp rl_app_data.json $C/board_variant.json
```
Guard 5 HALTS the bootstrap on the moved file set — that halt is the guard working and was NOT patched away;
the SCRATCH CHECKOUT's pins are re-stamped by `repin_variant.py` (carried unchanged from `../act336b/`).
**The re-pin is deliberately NOT COMMITTED**: the branch carries the four engine files and nothing else.
Log: `variant_build.txt`. **PARITY GATE PASS** (804 board values == engine gated `ev()`, eps=0).

Two build-time findings, both recorded rather than patched around silently:
1. The pole cache key now carries the resolved state, so the established half had to join the module-load
   **prewarm** — left lazy, a pole could first be computed inside the forward lens, where `price6` walks a
   synthetic through `_dev_advance` and the synth has no `games` key. Same freeze, two states.
2. `rl_model._resolved_336` keys its as-of cutoff on `BASE_REF`, so the walk-forward cannot read a
   resolution the calendar has not reached. **Verified identity-preserving**: the board md5 was
   `ecfc824b` before and after the change, and the no-arb matrix `7307bb26` before and after — the
   emitter already truncates `p['scoring']` to `year <= Y`, so there was no leak to close, only a guard.

### 4. board delta
```
RL_OUT=$C python3 $C/board_diff_files.py $C/board_baseline.json $C/board_variant.json
```
Carried unchanged from `../act336b/`. Output `board_delta.txt` / `.json`.

### 5. the named eight, and the resolved-state split
```
cd $W && ... RL_REPO=$C/repo_variant RL_OUT=$C python3 $C/named_eight.py   > named_eight.txt
                                              python3 (inline) -> resolved_split.txt
```
`named_eight.py` loads the engine through `load_engine.py`, a copy of the shipped loader at
`rl_export.py:68` (exec `_merged_recover.py` truncated at its report block, then pin the clock). Importing
that module whole raises `KeyError 'games'` out of its own report block in a bare shell — measured on the
**baseline** checkout too, so it is pre-existing and out of scope. Noted, not patched.

### 6. hump — the noarb_338 stack, re-run both sides
```
cd $C/noarb_{baseline,variant} && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_REPO=$C/repo_{main,variant} RL_FV=… RL_WORKDIR=$W RL_OUT=. python3 emit_matrix_338.py   # ~3 min each
cd $C/noarb_{baseline,variant} && OPENBLAS_NUM_THREADS=1 python3 noarb_table_338.py && python3 noarb_ext_338.py
python3 (inline) -> hump_compare.txt
```
The three harness identity pins (`EXPECT_STORE`, `EXPECT_V0SURF`, `EXPECT_N`) were RE-MEASURED on the
amended matrix and all three came back unchanged — `37ced3ce` / `af556bdca53d` / n=1197 — so nothing was
re-pointed and no assert was patched. The matrices themselves differ, which repeats both prior findings:
**the harness identity pins cannot discriminate this basis move.**

### 7. monotonicity, the new guard, and the seam
```
cd $W && ... RL_OUT=$C python3 $C/monotonicity_proofs.py   # -> monotonicity.txt / .json, seam_basepk.json
cd $W && ... RL_TAG=variant  python3 $C/seam_boundary.py   # on the VARIANT build
cd $W && ... RL_TAG=baseline python3 $C/seam_boundary.py   # on the CONTROL build
python3 (inline) -> seam_report.txt                        # the difference-in-differences
cd $W && ... python3 $C/repo_{main,variant}/engine/forward_valuation/par_build.py > par_report_{baseline,variant}.txt
python3 (inline) -> strata_report.txt
```
`monotonicity_proofs.py` is `../act336b/`'s, with PROOF 1c appended (the established-conditional table, the
`est >= unconditional` guard, and the per-cell seam). `seam_boundary.py` is new: it re-prices REAL players
(identity and key preserved, so `_isreal` holds) with a single season of 5 games and of 6 games, on BOTH
builds, and reports the ratio of ratios so the pre-existing 5g->6g machinery step is netted out.

---

## File index

| file | what it is |
|---|---|
| `COMPARISON_CURRENT_vs_BUST_INCLUSIVE_AMEND2.txt` | **the draft owner sheet** (COMPARISON pattern; both amendments stated at the top; caption carried) |
| `named_eight.txt` / `.json` | **the eight named players**, baseline / 1st cut / amend-1 / amend-2 / draft-day, with their season lines |
| `seam_report.txt`, `seam_{baseline,variant}.json`, `seam_basepk.json` | **the resolved-boundary seam** — anchor and price, difference-in-differences |
| `hump_compare.txt` | the year-ratio row three ways, both appreciation headlines, the pick split |
| `board_delta.txt` / `.json`, `resolved_split.txt` | movers, ΣΔ, age buckets, top 5 cuts/lifts, scale vs relative, and the established/unresolved split |
| `monotonicity.txt` / `.json` | unclamped monotonicity (4 tables), the Ablett cell, the three leave-one-out pairs, the new guard |
| `strata_report.txt`, `strata_a2.txt` / `.json`, `cond_variants.txt` / `.json` | every rate and level with its denominator; the three readings and why (iii) was barred |
| `par_report_{baseline,variant}.txt` | the par surface both sides; §E2 is the two-anchor disclosure, §G the P disclosure |
| `MD5S.txt` | every identity and file md5 quoted anywhere in this directory |
| `board_baseline.json` / `board_variant.json` | the control board and the amendment-2 board |
| `noarb_baseline/`, `noarb_variant/` | the matrices, the tables, the harness copies, the emit logs |
| `control_build.txt`, `variant_build.txt`, `variant_bootstrap.txt`, `repin.txt` | the build logs |
| `derive_a336c.py`, `derive_cond_variants.py`, `named_eight.py`, `seam_boundary.py`, `load_engine.py` | the new instruments (sources named in their headers) |
| `board_diff_files.py`, `monotonicity_proofs.py`, `repin_variant.py` | carried from `../act336b/` (monotonicity has PROOF 1c appended) |
| `repo_main/`, `repo_variant/` | the two git worktrees the builds ran from |

---

## Scope fence — held (as widened by the amendment)

* Four code files on the branch, never merged. `git show --stat f7a16b5` shows exactly those four.
* No `RL_V0SURF_REFIT`. The frozen surface loaded unchanged in every build (`v0surf_frozen=True`,
  signature `af556bdca53d`) — the ruled and disclosed basis.
* `main` untouched — `origin/main` at `a8de737…` before and after this act.
* `rl_passmark.json` / `params.json` provenance hole: OUT OF SCOPE, unswept, untouched.

## Reds carried out of this run (reported, not patched)

1. **year-1-to-peak 1.525 vs baseline 1.394** — WIDER than the first cut's residual and wider than
   amendment 1's 1.439, and year-0-to-peak only closes 1.572 -> 1.533. The resolved-state fix and the
   hump compression pull against each other; this run measured the trade-off rather than hiding it.
2. **the resolved-boundary cliff** — 1/P at the anchor (max 2.434x, KPF 49-99), up to 1.582x in board
   points on 12 difference-in-differences probes. An L-SMOOTH conflict. A continuous form exists and is
   deliberately NOT built: the amendment ruled binary conditioning and a taper is an unruled dial.
3. **5 of 42 unclamped pick-monotonicity violations** in the bust-inclusive BASEPK_REG (unchanged from
   both prior cuts); **14 of 42** in the new established-conditional BASEPK_EST. Not re-clamped.
4. **the est >= unconditional guard fails in 1 of 48 cells** — KPD band 1-3, -0.6%, a cell holding one
   player and therefore gradient-filled from a different donor than its unconditional twin.
5. **harry-dean 0.984x draft-day** raw (1.023x with the uniform rescale removed) — the mixed basis the
   mandated held surface creates, unchanged in kind from amendment 1.
6. **zac-taylor 0.579x draft-day** — but he was already 0.708x on the CURRENT board. Named so it is not
   misread as variant-created.
7. `_merged_recover` cannot be imported whole in a bare shell (`KeyError 'games'` from its own report
   block, on the baseline checkout too). Pre-existing, out of scope, worked around by using the shipped
   loader.
