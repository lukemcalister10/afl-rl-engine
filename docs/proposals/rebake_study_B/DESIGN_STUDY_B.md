# DESIGN STUDY B — THE BAND/CEILING REBAKE

**Seat:** REBAKE DESIGN STUDY B (one arm of an owner-ordered blind comparison).
**Date:** 2026-08-21. **Tree:** `/home/user/afl-rl-engine`, store `b745002e`, band pin `34faa865`, ceiling pin `cfdc7321`.
**Independence declaration:** this seat did not open `docs/proposals/rebake_study_A/`, `docs/proposals/REBAKE_SCOPE_2026-08-21.md`, or any register entry summarising study A. Study-A *filenames* appeared once in a repo-wide grep result; no study-A file was read. Every number below was produced by this seat's own scripts, which ship beside this document.

**How to read the claim numbers.** Every load-bearing statement carries a tag.
`M-n` = **MEASURED** by a script in this directory, reproducible with the command in §0.
`I-n` = **INFERRED** — a reading of measured facts, stated as a reading and open to being wrong.
Where a measurement contradicted what this seat expected, or contradicted a document in the tree, it is said so plainly.

---

## THE SHORT VERSION

1. **The band model was fitted on a store this repository has never contained.** Its training-row count
   (13,226) matches no committed store under any of 32 switch settings. The ceiling model `q97m` *is*
   identifiable — 13,111 rows pins it to the 15–17 July store epoch — but it was committed the day *before*
   that store landed, so it too was fitted on something staged and unrecorded. Neither artifact carries a
   stamp saying what it was fitted on. (§1.3)
2. **14 % of the band model's training rows were taught a guessed age.** The DOB courier wrote 302 birth
   years on 10 August; 300 of those players sit in the training pool, carrying 1,874 rows, of which 38.9 %
   had the guess wrong by a year or more and one by five years. The sibling `peak_model_v4` has the same
   wound and its own build script already names the falsifier that has never been taken. (§1.4)
3. **The declared permanent fix cannot be executed as written.** `PREREG_STAIRCASE.md` §8 says FIX 1 is
   `monotonic_cst` on feature 9 at `conditional_prior.py:160-161`. Those lines build a
   `GradientBoostingRegressor`, and that class has no such parameter — it raises `TypeError`. The estimator
   change is the precondition for the repair, not an optional modernisation. (§2.1)
4. **And the obvious replacement is not exact either.** `monotonic_cst` under `loss='quantile'` in the pinned
   sklearn 1.8.0 cuts the violation from 25 % of steps to 1.6 % but leaves 96.5 % of rows with a down-step,
   because the post-hoc leaf line search overwrites the constrained leaf values. There is a four-line
   construction that *is* exact — measured at 0 violations over every design row — and it depends on a
   private sklearn internal. That trade-off is the study's central owner decision. (§2.2–2.3, D1)
5. **The owner's training-data instinct is confirmed, with a correction on the size of the lean.**
   "Use all the data" is right — deleting the pre-2014 half costs 2.1 %. "Lean toward what's relevant" is
   right too, but only gently: a 16-year half-life beats flat by 0.18 %, a 6-year half-life is a wash, and
   anything sharper hurts. This seat measured it three times and got two wrong answers first; the wrong ones
   and their causes are in §3.3, because how the weight is *anchored* mattered more than whether to weight.
6. **Deleting the pool sets loses on every arm, including the one it was meant to help.** Out of sample it
   costs 6.4 % overall, 21 % on pool rows and 0.5 % even on national rows. (An earlier in-sample measurement
   of this seat's said the opposite; it is struck, and why is explained.) (§3.4)
7. **Age should not get a single direction — but it can get a shape.** The measured response is
   single-peaked, not monotone. Replacing raw age with distance-from-peak on each side, both constrained
   downward, makes single-peakedness true for **100 % of rows** instead of 7 %, keeps law 3 exact, and costs
   0.10 % of fit. Its price is one chosen constant. (§2.6, D2)
8. **The gate that would have caught all of this does not exist.** B6 checks monotonicity on the *games*
   axis only; the level-axis proof in the record is three archetype rows wide, and half of it is still marked
   open. (§4.1)
9. **The recommended design was built and measured, not sketched.** Refitted on the current store, with
   settings chosen out of sample: **0 negative steps in 1,004,720**, swept across every one of the 13,220
   design rows — against 23.4 % on the shipped artifact — while fitting **better** than the incumbent
   (3.9213 vs 3.9267 walk-forward) in **4 seconds** instead of 36. (§2.5, §5)

---

## 0 · WHAT WAS RUN

Eleven scripts sit beside this file. All are read-only against the repo; they write only into a scratch
directory. `RESULTS.json` carries every number quoted here.

| script | what it measures |
|---|---|
| `m1_artifacts.py` | the fitted estate: every pickle, its estimator, hyperparameters, feature count and **the training-row count baked into its trees** |
| `m2_trainset.py` | rebuilds the real design matrix through `rl_model` + `par_redesign` on the current store — the ground truth every replay below is validated against |
| `m3_storesweep.py` | replays the training-row enumeration over **every committed version of the store** and measures each one's drift against `b745002e` |
| `m4_provenance_grid.py` | searches 32 switch settings × 29 store versions for the row counts found inside the pinned pickles — *which store fitted this artifact?* |
| `m5_estimator.py` | the first estimator bake-off; the law-3 census on the pinned artifacts; the age partial dependence; the pool deletion experiment; weighting vs deletion |
| `m6_agecourier.py` | the blast radius of the 2026-08-10 DOB courier on each fitted artifact |
| `m7_constrained.py` | the exact-constraint construction, and the mechanism behind sklearn's approximate one |
| `m9_tune.py` | out-of-sample hyperparameter selection, the full-population law-3 census, and the three data-design questions |
| `m10_extend.py` | extends the selection grid past its top corner, so the chosen point is not a grid boundary; runs a second independent full-population census |
| `m11_weightanchor.py` | the robustness check that found this seat's own recency-weighting bug |
| `assemble_results.py` | collects all of the above into `RESULTS.json` |

Environment: the pinned venv at `/root/rl_venv312` (**sklearn 1.8.0, numpy 2.4.4, Python 3.12.3** — M-1).

**To reproduce.** `m2` must run first (it writes the design matrix the later scripts read); the rest are
independent. Nothing writes inside `engine/`, `data/`, or the workspace.

```sh
export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO=/home/user/afl-rl-engine CLAUDE_PROJECT_DIR=/home/user/afl-rl-engine
export STUDYB_FV=$RL_REPO/engine/forward_valuation
SCRATCH=<any writable scratch dir>          # m2 writes X_cm.npy / y_cm.npy / meta_cm.json here
cp docs/proposals/rebake_study_B/m*.py "$SCRATCH"/ && cd "$SCRATCH"
python m1_artifacts.py  > m1_out.json       # the artifact census
python m2_trainset.py   > m2_out.json       # the design matrix (writes the .npy files the rest read)
python m3_storesweep.py > m3_out.json       # store drift, all 29 committed versions
python m4_provenance_grid.py > m4_out.json  # which store fitted which pickle
python m6_agecourier.py > m6_out.json       # the DOB-courier blast radius
python m5_estimator.py                      # ~15 min   -> m5_out.json
python m7_constrained.py                    # ~10 min   -> m7_out.json
python m9_tune.py                           # ~35 min   -> m9_out.json   (the full-population census is the slow part)
python m10_extend.py                        # ~20 min   -> m10_out.json
python m11_weightanchor.py                  # ~3 min    -> m11_out.json
python assemble_results.py                  # -> RESULTS.json
```

**Run them one at a time.** This box has four cores and each `HistGradientBoostingRegressor` fit takes all of
them; two of these scripts in parallel thrash badly enough to look like a hang (this seat lost a run that way
and re-ran it serially).

---

## 1 · WHAT THE BAND MODEL ESTATE ACTUALLY IS

### 1.1 The artifacts

**M-2.** Four fitted pickles are tracked in the repo. Measured directly out of the pickles:

| artifact | md5 | estimator | shape | features | **rows in the fitted trees** |
|---|---|---|---|---|---|
| `data/cm_400.pkl` | `34faa865` | **5 × `GradientBoostingRegressor(loss='quantile')`**, α = .10/.30/.50/.70/.90, 400 trees, depth 4, lr 0.05, min_samples_leaf 25, random_state 0 | 5 forests × 400 trees = 2,000 trees, 11,640 nodes each forest | 11 | **13,226** |
| `data/q97m.pkl` | `cfdc7321` | **1 × `GradientBoostingRegressor(loss='quantile')`**, α = 0.97, 200 trees, same shape | 200 trees, 4,624 nodes | 11 | **13,111** |
| `engine/rl_after/peak_model_v4.pkl` | `f305fe53` | **`HistGradientBoostingRegressor(loss='squared_error')`**, 600 iters, depth 5, lr 0.04, l2 2.0 | — | 17 | (hist binning; no tree row count) |
| `data/v0surf.pkl` | `5dd34ca8` | two keyed dicts (isotonic year-zero surfaces), not a forest | — | — | — |

**M-3.** All three forest artifacts carry `_sklearn_version = '1.8.0'` **stored in the pickle bytes** — so the
runtime that pickled them was already the modern sklearn. **Nothing about the incumbent estimator choice was
forced by an old library version.** (First half of the answer to *"why wouldn't we have used this newer model
when we originally built the system?"*; §2.1 has the rest.)

> *Methodological note, because this one nearly went into the study wrong:* do **not** read
> `_sklearn_version` off a loaded estimator. sklearn writes it in `__getstate__`, so calling `__getstate__`
> on an already-unpickled object re-stamps it with the version you are running **now**. The stored value must
> be read from the raw pickle bytes. `m1_artifacts.py` does that and carries the warning in place.

**M-4.** The engine loads, and never fits, all of these. `wire_redesign.build()` loads `cm_400.pkl` from a
pinned cache; `_merged_recover._load_q97m()` loads `q97m.pkl` and there is deliberately no fit path left in
the engine. `data/expected_boot.json` pins `band = 34faa865…`, `q97m = cfdc7321…`, `peak_model = f305fe53…`,
`store = b745002e…`, and `boot_guard.py` asserts all six fitted artifacts **twice** — once as checkout
integrity (block 0d) and once on the resolved **load path** (block 0e), the latter because the workspace copy
and an env var can win over the repo copy.

**M-4b — but the release manifest does not enumerate them.** `release_manifest_check.py`'s identity set is
**11 identities** (store, board, engine_head, rl_model, fv, config, register, as_of_round, sheet,
sheet_rows, sheet_injured_y). None of the fitted artifacts is in it; `fv` covers
`engine/forward_valuation/*.py` — the **source**, not the fitted output. So a rebake moves five pinned
artifacts that the release manifest, by construction, cannot see. Guard 5 catches them; the manifest does
not enumerate them. **I-19:** the fitted set belongs in that table, and a rebake is the natural moment to put
it there.

### 1.2 Who built each one — the fit sites

**M-5.** `cm_400.pkl` is **not** produced by `conditional_prior.build_cond_prior` on its own. The shipped
forest is the **par-centred** one: `wire_redesign.build()` sets `cp._lvl_eff = PR.lvl_par` before use, and
`par_redesign.retrain()` does the same before calling `dist_redesign.build()` → `cp.build_cond_prior()`.
So feature 9 ("level") in the shipped forests is `par_redesign.lvl_par` — the *par-centred* level, which
itself depends on the par surface fitted by `par_build.py` over **draft cohorts 2003–2018** — not the plain
`cp._lvl_eff` that `conditional_prior.py`'s own `__main__` validation block exercises.

**M-6.** `q97m.pkl` is fitted from a **different population** than `cm_400.pkl`. Its `X/yy` come from
`_merged_recover.py:59-64`, which applies the `RL_MSD_POOL_EXCL` filter (mid-season-draft players excluded,
default ON) and **does not** apply the T1 unobservable-season skip that `build_cond_prior` applies. Measured
on the current store, that is a 114-row difference in the MSD leg and a 63-row difference in the T1 leg.
The two shipped models that jointly form the six-leg band are therefore trained on two different row sets.

**M-7.** `q97m.pkl` has a committed, gated refit entry point (`refit_q97m.py`, `--verify` / `--bake`, which
re-pins `expected_boot.json` and HALTs downstream). **`cm_400.pkl` has none.** Its own docstring says so:
*"Freezing WITHOUT a documented refit path just builds a second cm_400.pkl — a model nobody can legitimately
update."* The band model is that second one. `wire_redesign.build()`'s only fit branch is an explicitly
labelled COLD-BAKE fallback that produces a non-canonical forest.

**I-1.** The single largest structural defect in the estate is not the estimator — it is that the shipped
band model has no legitimate way to be regenerated. Everything else in §5 is downstream of fixing that.

### 1.3 Which store fitted each one — measured, not assumed

The owner asked: *"We can probably find out which store fitted it by looking at when the training data model
was created?"* The stronger method is available, and this seat used it: **the number of training rows is
recorded inside every fitted `GradientBoostingRegressor`** (the root node's `weighted_n_node_samples`). Replay
the training-row enumeration over every committed store and look for the match.

**M-8.** `m3_storesweep.py` / `m4_provenance_grid.py` replayed the enumeration over **all 29 committed store
versions**, under 32 switch combinations each (T1 on/off × MSD in/out × resolved_cut 2020/2021 × cap
2025/2026 × two eligibility predicates). The enumeration is validated: on the current store it reproduces the
engine's own live figure of **13,220** rows exactly (M-9, cross-checked against `m2_trainset.py`, which builds
the real design matrix through `rl_model` + `par_redesign`).

**M-10 — `q97m.pkl` (13,111 rows) is identified.** Exactly three committed stores reproduce 13,111, and all
three are the same store epoch: `b1fd0bce` (2026-07-15), `0efdc5d6` and `968de0c7` (2026-07-17), under
*T1-off, MSD-excluded, cut 2021, cap 2026* — which is precisely the `_merged_recover.py` construction. No
other store, under any of the 32 settings, produces that number.

**M-11 — and that store is one day NEWER than the pickle's commit.** `data/q97m.pkl` was committed at
`f14710d`, 2026-07-14 08:42 UTC, and has never been recommitted (`git log --all` shows a single commit for
the file). The store that reproduces its row count landed at `0cf723af`, 2026-07-15 08:01 UTC. **I-2:** the
frozen ceiling was fitted on a *staged, uncommitted* store that already carried the item-108a re-entry-trio
correction, and that store reached `main` a day later. The artifact is real and the correction is real; what
is missing is any record tying them together.

**M-12 — `cm_400.pkl` (13,226 rows) cannot be identified at all.** **No committed store, under any of the 32
switch settings, produces 13,226.** The nearest is 13,225 (Δ = 1 row) at the same 2026-07-15→07-17 epoch under
*T1-off, MSD-included*; the next nearest is 13,228 at 2026-07-21. The store committed **in the same commit as
the pickle** (`f4a4d34`, seed store `644d1254`) produces 13,248/13,120 — not 13,226.

**I-3.** `cm_400.pkl` entered this repository as an opaque binary in the 2026-07-02 seed commit. Its true
fitting store predates the repository, or was a workspace store that was never committed. The one-row gap to
the 07-15 epoch is suggestive but is not a claim: this seat could not close it, and says so.

**M-13 — the shipped band model is stale in seven distinct ways.** Measured drift between the fitting era and
the current store `b745002e`:

| what moved | when | measured |
|---|---|---|
| **The position schema was replaced** | 2026-07-05, the DPP strip | The store went from a single `pos` token plus a *probabilistic dual-position `_fut` list* to three columns (`drafted_position` / `present_position` / `future_position`). `gfut()` — which builds the band's position one-hot — changed from *"max-weight leg of the `_fut` blend"* to *"the `future_position` column"*. cm_400's one-hot was computed under the old semantics. |
| **The position vocabulary was replaced** | 2026-07-29, item #262 | `GRP` keys moved `{MID,RUC,GFWD,KFWD,GDEF,DEF,KDEF}` → `{MID,RUCK,SF,KPF,SD,KPD}`; `GROUPS` moved `['MID','GEN_DEF','GEN_FWD','KEY_DEF','KEY_FWD','RUC']` → `['MID','SD','SF','KPD','KPF','RUCK']`. **M-14: the index order was preserved** (GEN_DEF↔SD, GEN_FWD↔SF, KEY_DEF↔KPD, KEY_FWD↔KPF, RUC↔RUCK), so the one-hot columns did **not** get scrambled. This is a measured *non*-finding and is recorded so nobody re-raises it. |
| **433 players' drafted-position group changed** | by 2026-07-26 | measured against the current store, from the 2026-07-02..2026-07-21 era stores |
| **699–729 players' pick changed** | 2026-07-11 → 2026-08-05 | the pick-convention remediation, rookie/PSD corrections, the id migration, the #334 census |
| **302 birth years were written** | 2026-08-10, the DOB courier | see §1.4 |
| **2,031 players' scoring rows changed** | across the whole window | falling to 411 by 2026-08-10 and 0 at HEAD |
| **The T1 fabricated-zero fix landed** | 2026-08-05 (`dab9657`, owner word 2026-07-31) | `cm_400.pkl` predates it entirely and still carries the 63 fabricated-zero rows the fix removes |

### 1.4 The age feature is the worst of it — and the sibling model has the same wound

**M-15.** The 2026-08-10 DOB courier (`064abca`) wrote **302 birth years**. Before it, `cp._age_asof` fell
back to `18.0 + years-since-debut` — a guess — for every player without `_by`.

- **300 of those 302 players are inside the band model's training pool.** They carry **1,874 of 13,220
  training rows = 14.18% of the design.**
- Of those rows, **38.85% had the guessed age wrong by ≥1 year and 4.80% by ≥2 years**; the largest single
  error is **5 years**.
- At HEAD, **0 store rows are missing a birth year** (1,500 still lack an exact birth *date*, which is a
  first-class store state, not a gap).

**M-16 — the sibling needs it too.** `engine/rl_after/peak_model_v4.pkl` was committed 2026-08-05, **five
days before the courier**. 73 courier players sit in its 2006–2015 debut window, carrying up to 576 training
rows taught a guessed age. Its own build script already declares the falsifier:
`WATCHED_NUMBER_fallback … "must fall by EXACTLY the number of rows the DOB courier writes"`. **That fall has
never been taken** — no rebuild of `peak_model_v4.pkl` has been committed since the courier landed.

**M-17.** `build_peak_model_v4.py` already emits a `training_store_stamp.json` and an `age_source_census.json`
(*"an md5 says 'this is the artifact I expect', a stamp says 'and here is the world it was fitted in'"*), and
already names the gap this study is measuring: *"Today cm_400, q97m, peak_model_v4, pvc_snapshot and
bust_prior_table are pinned by md5 and NONE records the store or curve it was trained on."* **Neither file is
committed anywhere in the tree**, and neither exists in the workspace either.

**M-17a — and the reason is a one-line path bug, not a decision.** Both files are written to
`/home/claude/rl_workspace/rl_after/…` — **outside the repository**. `build_peak_model_v4.py` writes the
model itself to a workspace path too and copies it into place; the stamp and the census get no such copy. So
the provenance mechanism this estate already designed has never been able to reach a commit. That is the
cheapest fix in this entire study: two output paths.

**Answer to the owner's question, plainly: yes, the sibling model needs an update, for exactly the same
reason and by a measured amount.**

---

## 2 · THE ESTIMATOR QUESTION

### 2.1 What the pinned sklearn actually offers

**M-18.** Measured in the pinned venv (sklearn 1.8.0):

| estimator | quantile loss | `monotonic_cst` | `sample_weight` | `interaction_cst` |
|---|---|---|---|---|
| `GradientBoostingRegressor` (**the incumbent**) | yes (`loss='quantile'`, `alpha`) | **NO** | yes | no |
| `HistGradientBoostingRegressor` | yes (`loss='quantile'`, `quantile`) | **YES** | yes | yes |
| `RandomForestRegressor` / `ExtraTreesRegressor` | no | yes | yes | no |

**M-19.** `GradientBoostingRegressor(monotonic_cst=…)` raises
`TypeError: … got an unexpected keyword argument 'monotonic_cst'`. The constraint cannot be passed to the
incumbent estimator at all.

**This is the decisive fact of the whole study.** `PREREG_STAIRCASE.md` §8 declares the permanent repair as
*"FIX 1 — `monotonic_cst` on feature 9 at `conditional_prior.py:160-161` and at `refit_q97m.py`"*, and
`_merged_recover.py:392` repeats it. **FIX 1 as written cannot be executed.** Those two lines construct
`GradientBoostingRegressor`s, and that class has no such parameter. The estimator change is not optional
modernisation dressed up — **it is the precondition for the repair the estate has already committed to.**

**Why wasn't the modern estimator used originally?** **M-20:** it *was*, elsewhere in the same estate —
`build_peak_model_v4.py:22` imports and uses `HistGradientBoostingRegressor`, and that model's pickle carries
`monotonic_cst: None`. So the house already knows the class; the band model simply predates that choice and
was never revisited. **I-4:** there is no recorded engineering reason for the split. The band model's
hyperparameters (400 trees / depth 4 / lr 0.05 / leaf 25) are duplicated verbatim across four files
(`conditional_prior.py`, `refit_q97m.py`, `_gate1_wf.py`, `_gate1_picksplit.py`) — a copy-paste lineage, not a
comparison that was made and won.

### 2.2 The bake-off — and a defect in the obvious fix

Arms fitted on the design matrix rebuilt from the **current** store (13,220 × 11, `m2_trainset.py`). Law-3
census = sweep feature 9 across 42→118 in 0.25 steps on real rows and count how often the six-leg band's
weighted mean **falls while the level rises**. Walk-forward = train on as-of years ≤ T, score T+1…T+3.

**M-21** (`m7_constrained.py`; the pinned-model row from `m5_estimator.py`, same census, same sample):

| arm | fit (5 q) | law-3: % of steps negative — **all rows** | **thin-evidence rows** | worst step | walk-forward pinball 2014 / 2017 / 2020 (mean) |
|---|---|---|---|---|---|
| **PINNED `cm_400` as shipped** | — | **23.40 %** | **25.66 %** | −4.30 % | — |
| A — `GradientBoostingRegressor` quantile (the incumbent construction, refit today) | 36.3 s | 25.15 % | 27.39 % | −9.78 % | 4.1598 / 4.1482 / 3.4721 (**3.9267**) |
| C — `HistGBR` quantile + `monotonic_cst` (**FIX 1 as written, if it could be written**) | 4.6 s | **1.65 %** | 2.58 % | −3.56 % | 4.1600 / **4.1306** / **3.4569** (**3.9158**) |
| F — `HistGBR` + pinball loss **with the leaf line search disabled** + `monotonic_cst` | 5.6 s | **0.0000 %** | **0.0000 %** | **+0.000** | 4.3317 / 4.1870 / 3.5033 (4.0073) *(demonstration settings — see §2.4)* |

Three things follow, and the second is the one this seat did not expect.

**M-22a — the step surface, counted independently.** Reading the split thresholds straight off the pinned
trees: feature 9 (level) carries **1,101 / 1,575 / 1,225 / 1,289 / 1,198** splits in the five band forests and
**630** in `q97m`, over **253 / 394 / 617 / 632 / 520 / 292** distinct threshold values, spanning
**40.7489 – 116.2636**. That range matches `_merged_recover.py:470-471`'s own stated census to four decimal
places, arrived at here independently. Level is the second-most-split feature after log-pick — which is why
the staircase on that axis is as coarse as it is, and why the ratchet had 2,329 knots to walk.

**M-22 — the shipped model's defect is large and it concentrates where the register said it would.** Nearly a
quarter of all level steps on the pinned forests move the band *down* on a *rising* level; on thin-evidence
rows (recency-weighted exposure < 12 games — **36.44 % of the design**, M-23) it is worse. That is the
mechanism behind the register-v806 finding of 44-of-86 thin-evidence rows priced higher by a lower score.

**M-24 — `monotonic_cst` under `loss='quantile'` is NOT exact in sklearn 1.8.0.** Arm C cuts negative steps
from 25.15 % to 1.65 % — a 15× improvement, and it *also* fits better out of sample than the incumbent — but
**96.5 % of rows still contain at least one down-step**, with a worst step of −3.56 % of the band. A minimal
control confirms the constraint itself is sound: on synthetic data, `squared_error` + `monotonic_cst` gives
**0** violations, and so does `quantile` + `monotonic_cst` when the constrained feature is the only driver.
On the real 11-feature design, `squared_error` + `monotonic_cst` gives **0/100** violating rows and
`quantile` + `monotonic_cst` gives **97/100** (M-25).

**M-26 — the mechanism, read out of the pinned sklearn source.**
`sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:962`:

```python
if not self._loss.differentiable:
    _update_leaves_values(loss=self._loss, grower=grower, ...)
```

`PinballLoss.differentiable = False` (`sklearn/_loss/loss.py:624`). So for quantile loss, **after** the grower
has enforced the monotone bounds, every leaf value is **overwritten** with the empirical quantile of that
leaf's residuals — a line search that does not respect the bounds it is overwriting. Under `squared_error`
the overwrite never happens and the constraint is exact.

**I-5.** Anyone who lands FIX 1 by swapping to `HistGBR(loss='quantile', monotonic_cst=[…])` and then removes
`RL_O44_LVLMONO` will ship a board that still violates law 3 on ~96 % of rows, at up to −3.6 % of the band —
smaller than today, and invisible unless someone runs the census. **A rebake must run the census, or it will
retire the scaffolding onto a floor that is still not flat.**

### 2.3 The construction that *is* exact

**M-27.** Disabling the post-hoc leaf line search restores exactness. The mechanism is a four-line subclass:

```python
from sklearn._loss.loss import PinballLoss
class GradOnlyPinball(PinballLoss):
    differentiable = True            # stops gradient_boosting.py calling _update_leaves_values
    need_update_leaves_values = False
```

`HistGradientBoostingRegressor` accepts a `BaseLoss` instance for `loss` in 1.8.0 (it is in the class's own
parameter constraints). With this loss and `monotonic_cst[9] = +1`, the law-3 census returns **0 violating
rows, 0.0000 % negative steps, worst step +0.000000** — at q10, q50 and q90 independently, and on the
composed six-leg band (M-21, M-28).

**The property is structural, not statistical.** The band becomes non-decreasing in demonstrated level
*because every tree in every forest is*, not because a sweep happened to find no counterexample.

**RISK, stated plainly (I-6).** `sklearn._loss` is a **private** module. This construction depends on an
internal contract (`loss.differentiable` gating `_update_leaves_values`) that sklearn is free to change. It is
safe today only because `requirements-lock.txt` pins it (`scikit-learn==1.8.0`, hash-pinned, line 34 — M-59)
and the environment is asserted at boot. The
mitigation is not a comment — it is a **self-test that fits a two-feature toy, asserts exact monotonicity, and
HALTs the bake if the private contract has moved**. Without that self-test this seat would not recommend it.

### 2.4 The honest catch: the exact arm needs its hyperparameters chosen out of sample

**M-29.** At the settings used to *demonstrate* the mechanism (lr 2.0, 1,200 iterations), arm F fits better in
sample (3.977 vs the incumbent's 4.136) and **worse walk-forward** (4.3317 / 4.1870 / 3.5033 vs 4.1598 /
4.1482 / 3.4721). Removing the line search makes each boosting step small and bounded (|gradient| ≤ 1,
hessian ≡ 1), so the learning rate and iteration count that reproduce the incumbent's *fit* are not the ones
that reproduce its *generalisation*. `m9_tune.py` selects them on walk-forward alone, with the rule declared
before the run; results in §2.5.

**I-7.** This is a real cost of the exact construction and it must be priced, not waved through: the
incumbent's hyperparameters do not transfer, so a rebake owes a declared, out-of-sample selection.

### 2.5 Selected settings and the final estimator comparison

**M-53 — the selection, and it settles the estimator question.** `m9_tune.py` swept
(learning rate × iterations) and chose on the **mean walk-forward pinball alone**, with the rule written into
the script before the run. Grid, three splits, five quantiles:

| learning rate | iterations | walk-forward mean pinball |
|---|---|---|
| 0.3 | 400 | 4.4382 |
| 0.3 | 800 | 4.1241 |
| 0.6 | 400 | 4.1190 |
| 0.6 | 800 | 3.9455 |
| 1.0 | 400 | 3.9798 |
| **1.0** | **800** | **3.9213 — selected** |
| — | — | *incumbent `GradientBoostingRegressor`, same splits: **3.9267*** |

**M-54 — THE CENSUS, ON EVERY ROW OF THE DESIGN.** The selected model was refitted on all 13,220 rows and the
level axis swept on **every single one** at a 1-point grid:

> **13,220 rows · 1,004,720 steps · 0 negative steps · worst step 0.000000**

Set beside the shipped artifact's **23.40 % of steps negative**, that is the whole argument. The
exactly-constrained arm:

* is **law-3 clean by construction**, over the entire population, not a sample and not three archetypes;
* fits **better out of sample than the incumbent** (3.9213 vs 3.9267 — a 0.14 % improvement, small but in the
  right direction, and it is not paid for by shape);
* fits in **~4 s** against the incumbent's **36 s**.

**M-58 — the selected point is an interior optimum, not a grid edge.** `m9_tune.py`'s grid topped out at its
own corner (lr 1.0, 800 iterations), which is exactly the situation where a "best" is really a boundary.
`m10_extend.py` searched past it and every extension is worse: lr 1.5 / 800 → 3.9382 · lr 1.0 / 1600 →
3.9586 · lr 1.0 / 1600 leaf 60 → 3.9627 · lr 1.5 / 1600 → 4.0015 · lr 1.0 / 3200 → 4.0310 · lr 2.0 / 1600 →
4.0437 · lr 1.5 / 1600 leaf 60 → 3.9978. **lr 1.0 × 800 stands.**

**M-61 — the exactness is confirmed a second time, independently.** `m10_extend.py` also ran the
full-population census on *its* best point (lr 1.5 × 800, a different model): **0 negative steps in
1,004,720** again. Two different fitted families, two full sweeps, zero violations. The property belongs to
the construction, not to one lucky fit.

**I-21.** The demonstration settings in §2.4 were a red herring of this seat's own making: the arm looked
worse only because lr 2.0 × 1,200 iterations overfits. Chosen properly, exactness is not bought at the price
of accuracy here. That reframes D1: the question is no longer *"how much accuracy does exactness cost?"* — it
costs none that this study can measure — but purely *"is the private-API dependency acceptable?"*

### 2.6 Should age get a signed constraint? — argued both ways from the data

The owner asked *"Why shouldn't age get direction?"* The rulebook already answers half of it: **law 6, AGE
FADES (direction-only)** — *"Veterans decline toward the measured floor."* The question is whether that law can
be made structural in the band model the way law 3 can.

**The case FOR a signed `−1` on age.**

- **M-30.** The measured marginal is not flat: realised forward best-3 by age bucket rises 57.95 (18–19) →
  74.09 (26–27) and then falls to 70.06 (32–33).
- **M-31.** With everything else held at the row's own values, the pinned `cm_400`'s own age response falls
  **−12.90 points** from its peak to age 34, against a rise of only **+3.41** below the peak. The fall is
  3.8× the rise. For veterans it is starker: on rows with tenure ≥ 8 the rise is **+0.74** and the fall is
  **−15.88**.
- **M-32.** Adding `monotonic_cst[age] = −1` on top of the level constraint **improved walk-forward pinball at
  all three horizons** (4.1548 / 4.1288 / 3.4491 vs 4.1600 / 4.1306 / 3.4569 for level-only). The constraint
  acts as a regulariser that the out-of-sample data rewards.
- **I-8.** At *fixed* demonstrated level, exposure and tenure, "older" carries almost no information except
  "fewer seasons of upside left". That is why the conditional slope is so much steeper than the marginal.

**The case AGAINST a signed `−1` on age.**

- **M-33.** The measured shape is **single-peaked, not monotone**. Only **7.5 %** of sampled rows are monotone
  non-increasing in age on the pinned model (10.0 % on tenure ≥ 8; **0.67 %** on tenure ≤ 3), and **0 %** are
  monotone non-decreasing. On a freshly fitted unconstrained model, **79.5 %** of rows are single-peaked, with
  the peak at age ~20 (M-34).
- **M-35.** A `+1` constraint on age (arm E) is refused outright: worst walk-forward of every arm at the 2014
  horizon (4.2465).
- **I-9.** Forcing `−1` would make it structurally impossible for a 19-year-old to be worth more at 21 than at
  19 on identical evidence — which contradicts the measured data on exactly the population the board is most
  sensitive about (recent draftees, tenure ≤ 3, where only 0.67 % of rows are monotone).

**The resolution this seat proposes, and measured.** Single-peakedness *is* expressible as a monotone
constraint — just not on the raw feature. Replace `age` by two derived features around a declared peak `a*`:

```
u = max(0, a* − age)     # years short of peak      constraint −1
v = max(0, age − a*)     # years past peak          constraint −1
```

"Value falls the further you are from the peak, in either direction" is then true **by construction**, it
contains law 6 as its right half, and it does not forbid the measured rise on its left half.

**M-57 — measured, and it works.** With `a* = 22`, the raw age column removed and `u`/`v` appended, both
constrained to `−1`, on the selected exact arm:

| arm | 2014 | 2017 | 2020 | **mean** | rows single-peaked in age |
|---|---|---|---|---|---|
| raw age, no age constraint (the §2.5 selection) | 4.1796 | 4.1334 | 3.4510 | **3.9213** | **7.0 %** |
| raw age + `monotonic_cst[age] = −1` | 4.1658 | 4.1413 | 3.4461 | **3.9177** | — |
| `u`/`v` peak features, both constrained `−1` | 4.1795 | 4.1437 | 3.4521 | **3.9251** | **100.0 %** |
| `u`/`v` peak features, age unconstrained (control) | 4.1783 | 4.1332 | 3.4503 | **3.9206** | 7.0 % |

* **The construction does what it claims:** 100 % of sampled rows are single-peaked in age, against 7.0 %
  without it. The mean curve peaks at **21.5** and runs 71.87 (age 18) → **76.35 (22)** → 68.82 (26) →
  63.92 (30) → 62.52 (34) — a real rise, then law 6's decline.
* **Law 3 survives the reparameterisation exactly:** 0 negative steps in 60,800 measured on the constrained
  peak-feature model. The two constraints do not fight.
* **All four arms sit inside 0.19 % of each other.** The age choice is very nearly free in fit terms, which
  means D2 should be decided on *which property you want guaranteed*, not on the pinball column.

**I-24.** The `−1`-on-raw-age arm has the best number and the worst property; the peak reparameterisation has
the worst number (by 0.10 %) and the only defensible property. If the estate's habit of preferring structural
guarantees over marginal fit holds here, the peak features win — but `a*` is a chosen constant, and this
estate's standing answer to "which constant?" is *"none, if the derivation has a boundary solution."* **`a*`
has no boundary solution. It is a number someone picks.** That is the whole of the case against, and it is
why D2 is the owner's and not this seat's.

---

## 3 · THE TRAINING DATA QUESTION

The owner's instruction is the design brief for this section, verbatim: *"Is there a way we can avoid halving
the training set? Use all the data, but lean and weight towards what's relevant?… I don't know why we would
delete pool sets completely."*

### 3.1 What the current design actually excludes

**M-36.** Arithmetic on the current store `b745002e` (2,650 rows):

| stage | rows kept | what is lost |
|---|---|---|
| store | 2,650 | — |
| position maps to one of the six groups | 2,650 | 0 |
| draft-eligible (`pick` or ND/RD) | 2,367 | 283 |
| **resolved: debut ≤ 2021** | **1,929** | **438 players (18.5 %), carrying 882 scoring rows** |

**M-37.** Of those 438 excluded players, **237 are active in 2026**. They are the recent-draftee population the
board prices most sensitively and they are structurally absent from the model that prices them.

**M-38.** Within the 1,929 that survive, the pool arm is **788 players / 3,773 rows = 28.54 % of the design**
(`is_pool` = rookie-draft entrants plus selections past the national curve). Their target distribution is
genuinely different: mean forward best-3 **61.75 vs 71.79** for the national arm, and a zero (total bust) rate
of **8.98 % vs 1.56 %** (M-39).

### 3.2 Do pre-migration store positions contaminate the *current* training set?

**Measured answer: no — but only because the training set is rebuilt from the store every time, and that is
exactly why the pinned artifact is the problem.**

**M-40.** The design matrix built today reads `MA.data`, i.e. the current store `b745002e`. Every feature is
recomputed. There is no cached pre-migration data path: `m3_storesweep.py` measures **0** players present in
the pre-migration stores but absent from the current one at HEAD, **0** group changes, **0** pick changes and
**0** birth-year changes between the last four store versions and HEAD.

**I-10.** So the *training pipeline* is clean. The contamination is entirely in the **frozen artifact**: the
board today is priced by forests whose position one-hots came from the pre-DPP `_fut` blend, whose picks
predate three rounds of pick corrections, and whose age column is 14.18 % guesses (M-15). The owner's instinct
was right, and the answer is sharper than "the training data is dirty": *the training data is clean and the
model was never refitted on it.*

### 3.3 Weighting versus deletion — the instinct is right, and the right lean is a gentle one

This section was measured three times and the answer moved twice. All three are here, because the way it
moved is itself the finding: **the design of the weight matters more than whether you weight at all.**

**M-41 — attempt one, and why it should not be relied on.** `m5_estimator.py` used a **single** split
(train ≤ 2020, test > 2020) on the approximately-constrained arm: half-life 6y 3.4650 · 10y 3.4703 ·
uniform 3.4889 · delete-pre-2014 3.4993. Recency weighting appeared to win. One split with the test window
sitting immediately after the training window does not measure regime relevance; it measures the gap between
train and test (I-22).

**M-55 — attempt two, three walk-forward splits, and it reversed:** uniform **3.9213** · delete-pre-2010
3.9245 · delete-pre-2014 4.0023 · half-life 10y 4.0026 · 6y 4.1718 · 4y 4.5211. On that reading every weight
was worse than flat.

**M-60 — attempt three, and it found the bug in attempt two.** M-55's weights decayed from a **global**
anchor (`YEAR.max()` = 2026). On the T = 2014 split that leaves every training row far down the curve and the
early cohorts nearly weightless — the weight was measuring the distance to *today* rather than the distance
to the end of its own training window, which is what a rebake would actually use.
`m11_weightanchor.py` re-ran it both ways:

| recency half-life | **global** anchor (as in M-55) | **window** anchor (the correct construction) |
|---|---|---|
| *(uniform, no weight)* | 3.9213 | 3.9213 |
| 6 years | 4.1718 | 3.9230 |
| 10 years | 4.0026 | **3.9152** |
| 16 years | 3.9404 | **3.9143 — best of everything measured** |

**The settled reading.**

* **"Use all the data" is confirmed outright.** Deleting the pre-2014 half costs **2.1 %**; deleting pre-2010
  costs 0.1 %. Deletion never helps at any setting tried.
* **"Lean toward what's relevant" is confirmed too — provided the lean is gentle and correctly anchored.**
  A 16-year half-life beats flat by **0.18 %**, a 10-year half-life by 0.16 %, a 6-year half-life is a wash,
  and anything sharper hurts. The measured gradient runs 16y > 10y > 6y > 4y, so the optimum is a *mild tilt*
  and the study did not find its far edge.
* **A mis-specified weight is worse than no weight at all** — M-55's global anchor made a 6-year half-life
  look 6 % worse than flat when the same idea, anchored properly, is a wash.

**I-11 — and this sits comfortably with the estate's own ruling.** M-42 below records the binding owner ruling
that SuperCoach scores are **era-comparable by construction**. If there is no era drift to correct, one should
not expect a large gain from recency weighting — and there is not one. What the ~0.2 % buys is not an era
correction; it is a mild preference for rows drawn from a football environment closer to the one being
predicted. Small, real, and not the same act as rescaling a score (I-12).

**I-25 — the practical recommendation, stated at the size of the effect.** Take a gentle recency weight
(half-life 10–16 years, anchored to the end of the training window) if it is free to implement — it is one
`sample_weight` argument — and do **not** present it as a significant improvement. It is worth about a fifth
of one per cent. The load-bearing half of this section is the deletion result, not the weighting result.

### 3.4 Should the pool sets be in or out?

**M-43 — a second measurement this seat had to withdraw.** `m5_estimator.py` reported that deleting the
pool rows *improved* national-arm pinball by 1.83 % (3.7952 → 3.7256). **That number is an artefact and
should be struck.** It trained a national-only model and then scored it on the very national rows it was
trained on — in sample, against an all-rows model scored out of its comfort zone. Of course it won.

**M-56 — the same question, out of sample, on three walk-forward splits. Deletion loses on every arm:**

| training design | scored on ALL rows | scored on POOL rows | scored on NATIONAL rows |
|---|---|---|---|
| **A — as is (all rows, no arm feature)** | **3.9213** | **4.3788** | **3.7581** |
| B — all rows **plus an explicit `is_pool` feature** | 3.9213 | 4.3788 | 3.7581 |
| C — **delete the pool rows** | 4.1735 (+6.4 %) | 5.2964 (+21.0 %) | 3.7785 (+0.5 %) |

**Deleting the pool sets is worse everywhere — including on the national arm it was supposed to help.** The
owner's instinct is confirmed outright, and the case for deletion has nothing left in it.

**But the board must price pool players.** The engine's own day-0 print, emitted while `m2_trainset.py` was
loading it, reads verbatim: *"COVERAGE: 1202 of 1202 pool rows map to a SIGNED cell (232 of them on the
shipped board)"* (M-44). A model trained without a single pool career would price those 232 by extrapolation
from a population with a 5.8× lower bust rate.

**M-45.** The estate has already answered this question once, in the other direction. ORDER 20 split
`par_redesign.BASE_RATE` and `par_build`'s surface by arm, because *"before the split a pool career taught the
national base rate at FULL WEIGHT — not through a kernel tail, directly."*

**M-50 — a claim this seat drafted and then had to withdraw.** The draft of this section said the band model
"has no arm axis at all". **That is wrong, and the measurement says so.** `_feat()` carries `log(effpk)`, and
`rl_model.effpk` returns `POOL_PICK = 65` for *every* pool entrant. Measured on the design matrix:
**3,773 of 3,773 pool rows sit at exactly `log(65) = 4.174387`, and 0 of 9,447 national rows do** — the
highest national value is `log(64) = 4.158883`. The arm is therefore **perfectly separable by a single split**
on an existing feature.

**I-20 — and the measurement follows through.** Because the arm is already perfectly separable, adding an
explicit `is_pool` feature should change **nothing**. M-56 below confirms it: arms A and B agree to four
decimal places at every horizon and on every scoring scope. The feature is redundant *today*.

It is still the wrong *shape*, and that is a forward-looking argument rather than a measured one (**I-23**):
a continuous pick axis invites the model to treat pick 65 as "pick 64, but a bit more", and anything the
estate later does to smooth or constrain that axis — it already runs isotonic projections on the pick axis
elsewhere — will bleed the pool arm into picks 60–64. An explicit categorical `is_pool`, or `HistGBR`'s
`categorical_features` (which the incumbent estimator does not have at all), makes the distinction immune to
that. **On today's numbers it is free and it does nothing; the argument for it is insurance, and it should be
sold as insurance, not as an improvement.**

**I-13.** The design question is not *delete or keep* — it is *keep, and say the arm out loud instead of
leaving it hidden at the top of the pick axis*. Deletion throws away 28.5 % of the rows to buy 1.83 % on one
arm and gives up the other arm entirely.

### 3.5 The unresolved-career question (the 438, and the 237 who are active)

**I-14.** This seat did **not** find a safe way to bring unresolved careers into training in one step, and
records the reasons rather than proposing it:

1. The target `fwd_best3_from` is **censored** for them by construction — a 2024 draftee's forward best-3
   through 2026 is not his career best-3, it is a lower bound.
2. Admitting them naively would teach the model that recent draftees are worth less, which is a survivorship
   artifact pointing the wrong way — the mirror image of the `#336` bust-inclusion problem the estate has
   already been bitten by on the par surface.
3. `_merged_recover.py:65-75` carries an explicit **L4 TRIPWIRE** that HALTs if any of Perez / McAndrew /
   Keane is re-admitted to the training pool by a store edit. The debut > 2021 window is load-bearing for a
   named, ruled decision. Moving it is an owner question, not a seat question.

**The honest recommendation is to leave the resolved window alone in this rebake** and to record the censored
population as a named, separate follow-on with its own design (inverse-probability-of-censoring weighting is
the standard tool; it is a second project, not a line in this one).

---

## 4 · THE VALIDATION DESIGN — how a rebaked model proves itself

### 4.1 What already exists and must be reused

**M-46.** The tree already contains a working walk-forward harness that refits the band model:
`engine/rl_after/_gate1_wf.py` calls `cp.build_cond_prior(...)` at 150 trees, holds out each 2014–2018 ND
cohort in turn, refits both `cm` and `q97`, and emits a **structured JSON certificate** with unrounded
per-cell observations plus `engine_head_md5` / `store_md5` / `config_sha256`. Gate **B2** invokes it, asserts
the certificate belongs to the candidate under test, and requires median |IS − WF| leakage ≤ 0.5 %-pts plus
GOOD > BUST separation per position. `_gate1_picksplit.py` does the same on a pick split.

**A rebake does not need a new validation instrument. It needs to run through this one — and it needs the
hyperparameters changed in all four places at once** (`conditional_prior.py`, `refit_q97m.py`,
`_gate1_wf.py`, `_gate1_picksplit.py`), because the harness hard-codes the incumbent construction.

**M-47 — the gap that let law 3 ship.** Gate **B6** tests monotonicity-in-evidence on the **games axis only**
(`ramp(0..14g)`, "more games worth less" dips). There is **no standing gate on the level axis**. That is
precisely why a 23.40 %-of-steps violation shipped and was found by a diagnosis rather than by a gate.

**M-49 — the existing level-axis proof is three rows wide, and half of it is still open.**
`PACKET_STAIRCASE.md` §8 F2 records the monotonicity proof as run *"on three archetype rows (MID/pick-40,
KPD/pick-8, SF/pick-55) over two sweeps"* — and marks as **NOT HELD** the 76-point score sweep through the
true `ev()` on each named victim and the 86-row class sweep (44 of 86 → 0). Its own words: *"This seat did
not re-run them. F2 is therefore OPEN and rides adoption."* **F3 (law 12, G-Y0) also rides adoption,
unmeasured.** The rebake inherits both open falsifiers, and V3 below is deliberately a *population* census —
every design row, not three archetypes — because three rows is how a 23 %-of-steps defect stays invisible.

**Limitation of this study, stated in the same breath (I-18).** This seat's census is measured at the **band**
(the six-leg vector), not through the true `ev()`. Band monotonicity is necessary for law 3 but the engine
composes the band with the pole, the ISO correction, the taper and the projection lens before a player has a
price. A rebake must close F2's open half by sweeping through `ev()`, exactly as the packet says it owes.

### 4.2 The gates a rebake must pass

| # | check | threshold | why |
|---|---|---|---|
| V1 | **B2 leakage**, re-run on the rebaked construction | median \|IS−WF\| ≤ 0.5 %-pts, GOOD > BUST per position | the existing law; unchanged |
| V2 | **Walk-forward pinball** vs the incumbent, on the declared splits | rebake ≤ incumbent at every horizon | a rebake that fits worse is not a rebake |
| V3 | **THE LEVEL-AXIS CENSUS — new, and permanent** | **0** negative steps over every design row at a declared grid | the missing gate; without it the ratchet cannot be retired safely |
| V4 | **The age-shape census** — if the peak reparameterisation is taken | 100 % of rows single-peaked | makes law 6 structural instead of asserted |
| V5 | **B6 games ramp** | unchanged | must not be broken by the estimator change |
| V6 | **Law 12, G-Y0** (year-0 closure ≤ 2.0 %) | unchanged | the band feeds year-0 pricing |
| V7 | **Law 9 conservation**, stated not netted | `band_scar` 200 (±0.029 %) | *the rebake will breach this; see below* |
| V8 | **Law 4 G-MONO** (pick curve 1–64 descending, pick 1 = 3000) | unchanged | the band feeds the curve's consumers |
| V9 | **The provenance stamp** | present, and matching | see §5.3 |

**The falsifiers — the results that would kill the design, named in advance. Labelled FB* so they are not
confused with the packet's own F1–F4.**

- **FB1.** V3 returns any negative step on the constrained forests → the exact construction did not survive the
  real fit, and the private-API dependency has moved. **Kill the design; do not retire `RL_O44_LVLMONO`.**
- **FB2.** V2 shows the rebake worse than the incumbent at any horizon after out-of-sample selection → the
  constraint is buying shape at a cost the data refuses. **Report and stop.**
- **FB3.** The board built from the constrained forests **without** the ratchet does *not* reproduce the
  monotone behaviour the ratchet produces today → the must-move proof of `PREREG_STAIRCASE.md` §8 has failed.
- **FB4.** The `sklearn._loss` self-test (§2.3) fails → the private contract moved. **HALT the bake.**
- **FB5.** The mover table shows movement concentrated in a population the diagnosis did *not* predict → the
  rebake is doing something other than what it claims.

**M-48 — V7 will fail and that has to be said before the run, not after.** The current `ratchet` default
already mints **+8,460 SCAR = +1.2220 %** against a 200-SCAR (±0.029 %) rail — **42.3×** — accepted by explicit
owner word (*"happy to waive the no arb reading for this"*, and on conservation: *"in principle I don't like
'enforcing conservation'… I'd prefer to find a lever to remove value that works on its own"*). A rebake that
bakes the same monotone floor into the fit will mint a similar amount. **Whether that mint is re-waived, or
whether the rebake is expected to land conserved, is an owner decision (§6, D5) and it must be settled before
the bake, because it changes what "success" means.**

### 4.3 The must-move proof

`PREREG_STAIRCASE.md` §8 already binds this rebake: *"its removal is a rebake MUST-MOVE PROOF: the rebake is
not complete until this dial and its code are gone from `_merged_recover.py` and the board built without them
reproduces the monotone behaviour from the constrained forests alone."*

**The proof, concretely:** build three boards — (a) today's shipped board (`RL_O44_LVLMONO=ratchet`,
incumbent forests), (b) the rebaked forests **with** the ratchet still on, (c) the rebaked forests with the
ratchet **removed from the source**. Board (c) must pass V3 with zero violations and must be within a declared
tolerance of board (b) — if (b) and (c) differ materially, the ratchet was still doing work and the fit did
not absorb it.

**I-15.** The same must-move logic applies to `RL_O33_TAPEROFF`, but it is a *different kind* of dial and this
seat is careful not to conflate them. `RL_O33_TAPEROFF` gates one taper-suppression expression on the ceiling
side (`_merged_recover.py:1337`, default ON since 2026-08-20 on the owner word *"Yes. I'm adopting."*). It is
**not** a patch on a fit defect — it is a value judgement about post-peak taper that the owner looked at and
adopted. Retiring it "into the rebake" means re-deriving `asc == 1` from the rebaked ceiling model and showing
the boundary solution still binds; it does **not** mean it will vanish on its own because the forests changed.
If the rebaked `q97m` does not reproduce `asc == 1`, that is a finding to bring back, not a thing to fix in
flight.

---

## 5 · THE RECOMMENDED DESIGN

### 5.1 What it is, in six lines

1. **Estimator:** `HistGradientBoostingRegressor` with a pinball loss whose post-hoc leaf line search is
   disabled, so `monotonic_cst` is exact. Five quantile forests plus the q97 ceiling, same six-leg band.
   Settings selected out of sample: **learning_rate 1.0, max_iter 800, max_depth 4, min_samples_leaf 25**
   (M-53) — re-select at the bake against the store of the day; do not carry these numbers as literals.
2. **Shape:** `monotonic_cst[level] = +1` — law 3 becomes a property of the fit. Age handled per §2.6 by the
   owner's choice (D2).
3. **Data:** **all** resolved rows, **no deletion** — deletion loses on every arm and every scope measured
   (M-56, M-60). A **gentle recency weight** (half-life 10–16 years, anchored to the end of the training
   window) is optional and worth ~0.18 % (M-60, D3). An explicit `is_pool` feature is also optional: it is
   measurably a no-op today (M-56), worth taking only as insurance against a future smoothing of the pick
   axis (I-23).
4. **Store:** refit on `b745002e` (or whatever store is current at the bake), which alone repairs 1,874 rows
   of guessed age, 433 position moves, ~700 pick moves and the T1 fabricated zeros.
5. **Siblings:** `q97m` refits in the same act through `refit_q97m.py`; **`peak_model_v4` refits too**, and
   its own `WATCHED_NUMBER_fallback` falls by exactly the courier's row count as its self-declared falsifier.
6. **Provenance:** every artifact ships with a `training_store_stamp.json` beside it — the mechanism
   `build_peak_model_v4.py` already wrote and nobody landed.

### 5.2 What it retires

**M-51 — a property of both dials, verified rather than taken on trust.** Neither `RL_O44_LVLMONO` nor
`RL_O33_TAPEROFF` appears in `data/model_config.json` (which carries 87 `RL_*` names). Both source blocks
claim this deliberately — *"config_sha256 stays UNMOVED and a canonical build still cannot CARRY this name —
it can only ship its baked-in default."* It is true. The consequence for the rebake: **retiring them moves
`engine_head`, not `config`**, and the paired gate the modernisation programme's M3 already specifies applies
— the default board byte-exact *and* the retired branch reproducing its historical identity before removal.

- **`RL_O44_LVLMONO`** — retired **into the fit**, with the §4.3 must-move proof. The read-site block
  (`_merged_recover.py:370-549`) and its five modes, memo, knot cache and suspend flag all delete.
- **`RL_O33_TAPEROFF`** — retired **only if** the rebaked ceiling re-derives `asc == 1`. See I-15: this is a
  re-derivation, not a consequence.
- **The `cm_400` no-refit-path defect** — the rebake's largest permanent gain is that `cm_400` acquires the
  gated, provenance-logging entry point `q97m` has had since 2026-07-14.

### 5.3 The provenance stamp — the smallest change with the largest return

**I-16.** This study spent most of its measurement budget answering *"which store fitted this?"* and, for
`cm_400`, **failed** (M-12). That failure is avoidable forever with a JSON file per artifact carrying
`store_md5`, `curve_payload_md5`, `v0surf_md5`, `gamma`, the training-row count, the switch settings, the
sklearn version and the hyperparameters. `build_peak_model_v4.py:171-188` already writes exactly this. The
rebake should land it for all five pinned fitted artifacts and add it to the release manifest.

**And it is nearly free (M-17a):** the code is written; it writes to the wrong directory. Two output paths
and a `git add` turn "which store fitted this?" from a day of forensics into a `cat`.

### 5.4 Cost

| item | measured / estimated |
|---|---|
| Fit time, 5 quantile forests | **~4 s** (HistGBR at the selected settings) vs **~36 s** (incumbent `GradientBoostingRegressor`) — roughly **9× faster** (M-21, M-53) |
| The full-population law-3 census (V3) | ~17 min for 13,220 rows × 77 grid points × 5 forests, single box (M-54). Cheap enough to be a standing gate; too slow for an inner loop — the gate should run at the bake, not per build |
| `_gate1_wf.py` walk-forward battery | 5 cohorts × 2 refits; currently timeout-bounded at 2,400 s in gate B2 |
| Code touched | 4 files carry the duplicated hyperparameter block (`conditional_prior.py`, `refit_q97m.py`, `_gate1_wf.py`, `_gate1_picksplit.py`) + a new `cm` refit entry point + the O44 block deletion |
| Pins that move | `band`, `q97m`, `peak_model`, `pvc_snapshot`, `board`, `balanced_board_md5`, `engine_head`, `fv`, the book seal, the release contract seal — of which **only** `board`, `engine_head` and `fv` are in the release manifest's identity set (M-4b) |
| Re-certification | the full Guard-5 / boot_guard / ship-gates / release-manifest chain — a **bake-class transaction**, per `refit_q97m.py`'s own downstream-HALT block |
| Human time | the movers list is the real cost: this moves every player |

### 5.5 Risks

| risk | severity | mitigation |
|---|---|---|
| **`sklearn._loss` is private API** (I-6) | **high** | a bake self-test that fits a toy and asserts exact monotonicity, HALTing if the contract moved (FB4); the version is already pinned and asserted |
| Hyperparameters do not transfer (M-29) | medium — **resolved** | out-of-sample selection with the rule declared before the run; done, §2.5, and the selected arm beats the incumbent (M-53) |
| Law 9 mint (M-48) | medium | settle D5 **before** the bake |
| Everything moves at once — estimator + store + weighting + features | **high** | **land it in declared arms** (§5.6), each priced separately, so a bad mover table names its own cause |
| `HistGBR` bins features (255 bins) where `GBR` splits on exact values | low | the level axis has 2,329 distinct thresholds today; binning coarsens the surface, which is *desirable* here, but it must be reported not discovered |
| `_o44_xs()` reads `estimators_` directly | **not a risk — a safety feature** | see M-52 below |

**M-52 — the estimator swap makes the dial's retirement forced, not optional.** `_o44_xs()`
(`_merged_recover.py:487-489`) walks `_m.estimators_` and reads `tree_.threshold` off every fitted tree to
find the step surface's knots. **`HistGradientBoostingRegressor` has no `estimators_`** (measured: its trees
live in the private `_predictors` as `TreePredictor` objects with a `nodes` record array, and its thresholds
are binned). So a build that swaps the estimator and leaves the O44 block in place **raises `AttributeError`
at load** rather than quietly doing the wrong thing. That is the good failure: the dial cannot survive the
rebake by accident, and the must-move proof cannot be skipped by forgetting. It also means arms 2 and 5 in
§5.6 cannot be separated — the estimator swap and the dial deletion land in one commit.

### 5.6 The landing shape

One arm at a time, each with its own mover table, so that the movement can be attributed:

**Arm 1 — the store alone.** Refit the *incumbent* construction on `b745002e`. Nothing changes but the data.
This prices the 1,874 guessed-age rows, the 433 position moves and the T1 fix on their own.
**Arm 2 — the estimator + the level constraint + the `RL_O44_LVLMONO` deletion + the must-move proof.** On
the same store. These cannot be separated: M-52 shows the dial's knot-reader cannot survive the estimator
swap, so they are one commit whether or not one wants them to be.
**Arm 3 — the data design** (recency weight, `is_pool` feature).
**Arm 4 — the age reparameterisation**, if the owner takes D2.
**Arm 5 — `RL_O33_TAPEROFF`**: re-derive `asc == 1` on the rebaked ceiling, and retire the dial only if the
boundary solution still binds (I-15).

**I-17.** Arm 1 is the one that most deserves to be run first and shown to the owner on its own, because it is
the only arm with no design content at all — it is purely *"the model, on the data we actually have."* If its
mover table is large, that is the honest measure of how stale the estate has become; if it is small, the case
for the rest of the rebake gets simpler to argue, not harder.

---

## 6 · DECISIONS THAT ARE THE OWNER'S — listed neutrally

Each of these is a judgement, not a measurement. This seat has stated the measured facts on both sides and
does not need to be told which way to go.

**D1 — Is the private-sklearn dependency acceptable? (the study's central question)**
Making law 3 structural requires subclassing `sklearn._loss.PinballLoss` — a private module (M-27, I-6). The
measured trade has only one term left in it: at settings chosen out of sample, the exact arm is **0 negative
steps in 1,004,720** and fits **better** than the incumbent (3.9213 vs 3.9267, M-53/M-54), so exactness costs
no measurable accuracy. What it costs is a dependency on an internal sklearn contract. Three options:
(a) take the private dependency, with a bake self-test that fits a toy, asserts exact monotonicity and HALTs
if the contract has moved; (b) take the stock approximate constraint (1.65 % of steps still negative, M-24)
and **keep** `RL_O44_LVLMONO`, honestly redescribed as a permanent residual monotoniser rather than
scaffolding — which means the `PREREG_STAIRCASE.md` §8 retirement clause is withdrawn rather than satisfied;
(c) take the exact arm **and** keep the ratchet as belt-and-braces, with the census standing as the proof it
never fires — safe, but it leaves dead code the estate has a law against.

**D2 — Should age get a direction, and in which form?** All three options land within **0.19 %** of each
other on walk-forward pinball (M-57), so this is a choice about guarantees, not accuracy.
(a) **No constraint** — the data's own shape, as today; 7 % of rows single-peaked, no property guaranteed.
(b) **`−1` on raw age** — the best number (3.9177) and the worst property: it would make it structurally
impossible for a 19-year-old to be worth more at 21 on identical evidence, on exactly the tenure ≤ 3
population where only 0.67 % of rows support monotonicity (M-33).
(c) **The peak reparameterisation** (§2.6, M-57) — **100 % single-peaked by construction**, contains law 6 as
its right half, costs 0.10 % against (a), and law 3 survives it exactly. Its price is one chosen constant
`a*`, and this estate's standing answer to *"which constant?"* is *"none, if the derivation has a boundary
solution"* — `a*` has none (I-24).

**D3 — Recency weighting: take it or leave it, and the honest answer is that it barely matters.**
Correctly anchored, a gentle weight helps by about **0.18 %** (16-year half-life) and a sharp one hurts
(M-60). The decision is whether a fifth of a per cent is worth carrying a parameter that has no boundary
solution and that this seat mis-specified twice before getting right. Arguments both ways: *for* — it is one
`sample_weight` argument and the gradient is consistent across three splits; *against* — the estate's own
era-comparability ruling says there should be nothing here to correct (I-11), and a dial that small is a dial
that will one day be tuned to a target. **Whether the game has changed in ways SuperCoach's fixed 3,300
points per match does not capture is a claim about football, not about the fit, and it is the owner's.**

**D4 — In or out: the pool arm, and the unresolved careers.**
Pool: **there is no longer a decision here on the numbers** — deletion loses on every arm out of sample
(M-56), and the explicit arm feature is a measured no-op (I-20). The only live question is whether to add the
`is_pool` feature as insurance against a future pick-axis smoothing (I-23), which is a taste question about
carrying a feature that currently does nothing. Unresolved careers (438 players, 237 of them active — M-37)
is the real decision: this seat recommends leaving the debut ≤ 2021 window **alone** this time (I-14), partly
because `_merged_recover.py`'s L4 tripwire makes that window a ruled, named decision that a seat should not
move on its own.

**D5 — Conservation.** The rebake will mint, as the ratchet already does at 42.3× the rail (M-48). Is the
law-9 waiver re-given for the baked version, is the rebake expected to land conserved, or is a separate
value-removing lever wanted first — which is what the owner said he would prefer?

**D6 — Scope: how far does "the estate" reach?**
`q97m` and `peak_model_v4` are measurably stale for the same reason (M-15, M-16). `v0surf` and the pick curve
were rebuilt more recently. Does this rebake cover all the fitted artifacts, or the band and ceiling only?

**D7 — Sequencing.** Does arm 1 (the store alone, no design change) get run and shown first (I-17), or does
the whole design land as one transaction?

---

## 7 · WHAT THIS SEAT COULD NOT ANSWER

- **M-12 stands unresolved:** `cm_400.pkl`'s fitting store is not recoverable from this repository. The
  nearest committed store is one row away and this seat could not close the gap. If study A closed it, its
  method should be preferred to this one's.
- The 1-row discrepancy between the pinned `cm_400` (13,226) and the best-matching committed store (13,225)
  has a cause this seat did not find.
- **I-15** is a reading, not a measurement: this seat did not re-derive `asc == 1` on a rebaked ceiling, so
  whether `RL_O33_TAPEROFF` genuinely retires into the rebake is untested here.
- No board was built. Every number above is measured on the design matrix and the fitted artifacts, not on
  priced player values. The mover tables in §5.6 are the missing half and they belong to the bake, not to a
  study. **I-18** says the same thing about the law-3 census specifically: it is a band-level census, and the
  packet's open F2 (the sweep through the true `ev()`) is still open.
- `peak_model_v4` was **not** refitted here. Its staleness is measured (M-16); the size of the movement that
  a refit would cause is not, because the refit writes into the workspace and this seat was read-only.
- The recency half-life surface was sampled at 4/6/10/16 years and the best point (16) is the **edge of the
  sample** — the gradient still points outward, so the true optimum is longer than anything tried and may
  simply be "no weight at all". D3 should not treat 16 as derived.
- The age peak `a*` was fixed at 22 and never searched. The 100 %-single-peaked result is a property of the
  construction and does not depend on `a*`, but the 0.10 % fit cost does.
