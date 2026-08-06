# #336 AMENDMENT 3 — the continuous experiment. RUN RECIPE + evidence index

**Fired** per issue #336, **AMENDMENT 3 FIRED** (comment 5206579726), owner word in-channel 2026-08-06
*"run it"*. Supersedes amendment 2's binary conditioning and its raw-P unresolved leg; everything else in the
VARIANT DIRECTIVE, Addendum 1 and Owner Catch 2 stands — control, held surface, branch-only, no landing.

**This is an EXPERIMENT.** Nothing landed on main, no pin moved on main, the variant code lives on
`variant/336-bust-inclusive` and is never merged. This directory is SCRATCH. The three prior runs live beside
it in `../act336/` (first cut), `../act336b/` (addendum 1) and `../act336c/` (amendment 2), retained unaltered.

**MANDATED CAPTION, carried on every sheet in this directory:**
> reference layer bust-inclusive; year-zero surface held at the shipped survivors-basis fit;
> the joint re-derivation is #334 stage B, after the ruling.

---

## THE AMENDMENT, in two paragraphs

**(1) THE SWITCH BECOMES A RAMP.** Amendment 2 selected between two anchors on a boolean, which put a cliff
at the six-game bar (measured: up to +58% in board points on a 12-probe difference-in-differences). Amendment
3 replaces it with a resolution weight `r(p) in [0,1]`, **reusing the engine's own continuous evidence
object** — the R100.11 evidence fade at `_merged_recover.py:685,711`, `pw(g)=(g+K)/(g^2+g+K)`, described
there as *"ONE continuous object: smooth, monotone, rational ... NO threshold, NO counter, NO branch
(L-SMOOTH)"*. Its complement `rho(g)=g^2/(g^2+g+K)` is exactly "how far this record has resolved him".
**No new width is set:** `K = 5.8` is the engine's pinned `_ABS_FADE_K` (itself "Fix 1's measured w(g) scale,
RL_DAMP_K"), restated rather than imported because `par_build` cannot import the engine module. The single
construction on top is a normalisation to the ruled bar, disclosed: `r = min(1, rho(g*)/rho(6))`, so
`r(0)=0` and `r(g*>=6)=1` exactly. `g*` is best single-season games — the establishment definition is itself
a max over seasons, so the ramp must run on the statistic the bar tests.

| g  | 0 | 1 | 2 | 3 | 4 | 5 | 6+ |
|----|---|---|---|---|---|---|----|
| r  | 0.000 | 0.170 | 0.450 | 0.671 | 0.824 | 0.927 | 1.000 |

**(2) SINGLE-CHARGE RECONCILIATION.** The band's own charge was measured first, on the population it had
never been measured on. `d_band = ev(unresolved p) / ev(CE(p))` with the anchor undiscounted on both sides,
CE(p) = the same player with establishment made certain. **Measured d_band = 0.7077 against a true class risk
of 0.7075 — the forward band already charges establishment failure IN FULL.** So `D = min(1, target/d_band)
= 0.9996`: the anchor owes nothing further and the reconciliation lands on its floor. Amendment 2's
anchor-side P on unresolved players was a SECOND charge on a band already pricing the whole risk.

The anchor, in one line, for a REAL player: `E[level | establishes] x [ D + r(p) x (1 - D) ]`.

---

## Identities

| | value |
|---|---|
| store | `37ced3ce` (all builds, unmoved) |
| v0surf signature | `af556bdca53d`, frozen=True (all builds — **the surface is HELD**, no `RL_V0SURF_REFIT`) |
| baseline `rl_model` / `engine_head` / `fv` | `33f94073` / `8f0e3eb1` / `d920557e` |
| **AMEND-3** `rl_model` / `engine_head` / `fv` | `b35c5521` / `e3527be4` / `0976195c` |
| **CONTROL board** | `113b36f898a32363c49c2a62fb809f4b` — **byte-reproduced, control PASSES** |
| **AMEND-3 board** | `de5110bb57a04d9b24e9c761241e54c7` (PARITY GATE PASS, 804/804, eps=0) |
| baseline no-arb matrix | `5fb617d0…` — reproduces `../act336c/`'s, a **second control, PASSES** |
| AMEND-3 no-arb matrix | `b82e12c1…` |
| branch / commit | `variant/336-bust-inclusive` @ `3bbc6882662e9b774db2e0cca9c8636bfa5ffb8c` (pushed) |
| parent (amendment 2) | `f7a16b5cf6279455eb30d213476eafcd0fe97346` |
| `origin/main` before / after | `823e27e2…` / `823e27e2…` — **UNMOVED by this act** (proven by `git ls-remote` either side of the push; it sits ahead of the branch's base `a82c0fe` because other sessions have landed on main since the branch was cut — this act moved it not at all) |

---

## The recipe, exactly as run

```
export PATH="/root/rl_venv312/bin:$PATH"
C=<this dir>;  W=/home/claude/rl_workspace/rl_after
ENV="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
```

### 0. two clean worktrees
```
git worktree add --detach $C/repo_main a82c0fe                 # the commit all four cuts used
git worktree add $C/repo_variant variant/336-bust-inclusive    # at f7a16b5, amendment 2's code
```
`../act336c/repo_variant` was detached to free the branch; its tree is otherwise untouched.

### 1. CONTROL — must byte-reproduce `113b36f8` before the variant is credited
```
cd $C/repo_main && RL_VENDOR=/home/user/afl-rl-engine/vendor bash bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$C/repo_main RL_FV=$C/repo_main/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json    # 113b36f898a32363c49c2a62fb809f4b   <-- CONTROL PASS
```
Log `control_build.txt`; board kept as `board_baseline.json`.

### 2. THE DERIVATION PASS — measured BEFORE the constants were pinned
```
cd $W && env $ENV ... RL_336_DFORCE=1.0 RL_336_TAG=_und            python3 $C/derive_a3.py
                      RL_336_DFORCE=0.5 RL_336_RFORCE=0 RL_336_TAG=_r0 python3 $C/derive_a3.py
                      RL_336_DFORCE=0.8 RL_336_RFORCE=0 RL_336_TAG=_r0 python3 $C/derive_a3.py
```
`RL_336_DFORCE` / `RL_336_RFORCE` are **declared measurement ablation levers** (precedent: `RL_ABSENCE`,
`_merged_recover.py:684`), documented beside the constants they derive and **unset on every reported build**.
`DFORCE=1` is the undiscounted-anchor build `d_band` is read on; `RFORCE=0` isolates the pass-through from the
ramp (with `r` free, forcing `D` moves the anchor only by `D + r(1-D)`, so a 93%-resolved player barely moves
and the price rounds to the same integer — the estimate would measure the ramp, not the pass-through).

**Three findings from the derivation, all recorded rather than worked around silently:**
1. One `D` **per process**: the engine rebinds `cp._lvl_eff` at load, so a second `exec` in the same
   interpreter wraps the first wrapper and recurses to the stack limit. Measured, then split into processes.
2. `_PE_CACHE` keys on `id(p)`; a freed counterfactual copy's id can be reused by the next copy and hit a
   stale entry. Every copy is now **held** and the cache cleared before each `ev()`.
3. The **per-player mean** of `d_band` (0.98) and its **value-weighted** aggregate (0.71) disagree sharply,
   because 60% of the unresolved subset is priced off the fixed pick curve and cannot move. The question is
   about VALUE, so the value-weighted statistic is operative; **both** are reported.

### 3. the reconciliation, then the pins, then the build
```
RL_OUT=$C python3 $C/reconcile_a3.py            # -> dband.json, reconcile.txt
# pin A3_DBAND=0.707707 / A3_TARGET=0.707455 into par_build.py and rl_model.py
python3 $C/repin_variant.py $C/repo_variant engines
cd $C/repo_variant && RL_VENDOR=/home/user/afl-rl-engine/vendor bash bootstrap.sh
cd $W && rm -f rl_app_data.json && env $ENV ... RL_REPO=$C/repo_variant ... python3 rl_export.py
md5sum rl_app_data.json    # de5110bb57a04d9b24e9c761241e54c7
```
Guard 5 HALTS the bootstrap on the moved file set — that halt is the guard working and was NOT patched away;
the SCRATCH CHECKOUT's pins are re-stamped by `repin_variant.py` (carried unchanged from `../act336c/`).
**The re-pin is deliberately NOT COMMITTED**: the branch carries the four engine files and nothing else.
**PARITY GATE PASS** (804 board values == engine gated `ev()`, eps=0).

### 4. the measurements
```
RL_OUT=$C python3 $C/board_diff_files.py $C/board_baseline.json $C/board_variant.json   # board_delta.txt
cd $W && ... RL_REPO=$C/repo_variant python3 $C/named_eight.py        # named_eight.txt  (four cuts)
                                     python3 $C/monotonicity_proofs.py
                                     RL_TAG=variant    python3 $C/seam_boundary.py
                                     RL_TAG=variant_d1 RL_336_DFORCE=1.0 python3 $C/seam_boundary.py   # ABLATION
                                     RL_TAG=variant    python3 $C/games_sweep.py
                                     RL_336_TAG=_a3live python3 $C/derive_a3.py         # the PROOF probe
                                     RL_TAG=variant_a3  python3 $C/decompose_336b.py
cd $C/repo_main && bash bootstrap.sh                                  # workspace back to the control engine
cd $W && ... RL_REPO=$C/repo_main    RL_TAG=baseline python3 $C/seam_boundary.py
                                     RL_TAG=baseline python3 $C/games_sweep.py
                                     RL_TAG=baseline python3 $C/decompose_336b.py
cd $C/noarb_{baseline,variant} && ... python3 emit_matrix_338.py && python3 noarb_table_338.py && python3 noarb_ext_338.py
```
**A build-discipline finding, recorded:** the no-arb emitter and every engine instrument read
`_merged_recover.py` from the WORKSPACE, not from `RL_REPO`. Running the baseline side while the workspace
still held the variant engine **HALTED LOUDLY** (`AttributeError: module 'PR' has no attribute 'par_at_est'`)
rather than emitting a silently-wrong control matrix. Each side is therefore bootstrapped into the workspace
before its own instruments run. The halt was not patched around.

The three harness identity pins (`EXPECT_STORE`, `EXPECT_V0SURF`, `EXPECT_N`) were RE-MEASURED on the
amended matrix and all three came back unchanged — `37ced3ce` / `af556bdca53d` / n=1197 — so nothing was
re-pointed and no assert was patched. The matrices themselves differ, repeating all three prior findings:
**the harness identity pins cannot discriminate this basis move.**

---

## File index

| file | what it is |
|---|---|
| `COMPARISON_CURRENT_vs_BUST_INCLUSIVE_AMEND3.txt` | **the draft owner sheet** (COMPARISON pattern; all three amendments stated; caption carried) |
| `hump_compare.txt` | **the steering numbers** — the hump row on FOUR bases, yr4, peak, yr1-to-peak, pick split |
| `reconciliation.txt` | **the single-charge proof** — probe set, `d_band` three ways, the finding, total/target = 1.0000 |
| `seam_report.txt` | **the boundary seam** — 12-probe DiD, the ablation control, the 1..10-game sweep |
| `establisher_probe.txt` | Addendum 1's double-charge check re-run, and what it does and does not now isolate |
| `named_eight.txt` / `.json` | the eight named players, baseline / 1st cut / a1 / a2 / **a3** / draft-day, with `r(p)` |
| `board_delta.txt` / `.json` | movers, ΣΔ, age buckets, top 5 cuts/lifts, scale vs relative, top-end, ladders |
| `monotonicity.txt` / `.json` | unclamped monotonicity, the Ablett cell, three leave-one-out pairs, the guard |
| `dband.json`, `reconcile.txt`, `probe_*.json` | the derivation dumps: every probe price behind the pins |
| `sweep_{baseline,variant}.json` | the 1..10-game sweep that attributes the residual DiD |
| `seam_{baseline,variant,variant_d1}.json` | the seam probes and the ablation control |
| `par_report_{baseline,variant}.txt` | the par surface both sides |
| `MD5S.txt` | every identity and file md5 quoted anywhere in this directory |
| `board_baseline.json` / `board_variant.json` | the control board and the amendment-3 board |
| `noarb_baseline/`, `noarb_variant/` | the matrices, the tables, the harness copies, the emit logs |
| `control_build.txt`, `variant_build.txt`, `*_bootstrap.txt`, `repin.txt` | the build logs |
| `derive_a3.py`, `reconcile_a3.py`, `games_sweep.py` | the new instruments (sources named in their headers) |
| `seam_boundary.py`, `named_eight.py`, `monotonicity_proofs.py`, `board_diff_files.py`, `repin_variant.py`, `decompose_336b.py`, `load_engine.py` | carried from `../act336b/` and `../act336c/` |
| `repo_main/`, `repo_variant/` | the two git worktrees the builds ran from |

---

## Scope fence — held

* **Four code files on the branch, never merged.** `git show --stat <commit>` shows exactly those four.
* No `RL_V0SURF_REFIT`. The frozen surface loaded unchanged in every build (`v0surf_frozen=True`,
  signature `af556bdca53d`) — the ruled and disclosed basis.
* `main` untouched — `origin/main` at `823e27e2…` before and after this act, proven by `git ls-remote` on both sides of the push. Only `refs/heads/variant/336-bust-inclusive` moved, `f7a16b5 -> 3bbc688`.
* `rl_passmark.json` / `params.json` provenance hole: OUT OF SCOPE, unswept, untouched.

## Reds — see the owner sheet's own reds section (8 items)

The two that steer stage B: **the hump does not fall** (1.535 vs 1.572, only 6.5% of the way to 1.0) and
**the relocation is not gone** (yr1-to-peak 1.503 vs the shipped 1.394/1.400).
