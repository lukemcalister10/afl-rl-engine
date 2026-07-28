# PRIORITY 1 · STAGE 1 — MEASURE WHAT THE RESTRUCTURE MOVED

**Seat:** one fresh execution supervisor (build seat), directing hands. One writer.
**Authority:** owner word, 2026-07-28. This is his priority 1.
**Nature:** MEASUREMENT ONLY. Nothing is adopted, baked, re-pinned or released by this job.

---

## WHY

Everything the engine fits was fitted before the store restructure landed. The store moved on
2026-07-27 (`f37d9716 → c120cfd5`); not one fitted artifact moved with it. Nobody has measured what
changed, and nothing downstream is trustworthy until someone does.

Two facts that make this concrete rather than theoretical:

- The live pick curve `pvc_curve_v2.json` **declares its own source store** as `968de0c7` — the store
  as at 17 July. The store has moved twice since. It was already stale before the restructure.
- D1 moved the `store` and `board` pins in `data/expected_boot.json` and **left the `v0surf` pin
  untouched** (`3af2b725`, unchanged before and after). The board of record `fa172ac1` was therefore
  built with the old V0 surface on the new store.

---

## 0 · THE PIN — READ THIS BEFORE ANYTHING ELSE

**Work from a pinned checkout. Do not re-read `main` after you start.**

| | |
|---|---|
| base commit | `85e39ee` |
| store | `c120cfd5` (`engine/rl_after/rl_model_data.json`, 1,808,700 B, 2,651 players) |
| board | `fa172ac1` (`data/rl_build/rl_app_data.json`, 1,255,256 B) |

**This runs concurrently with the Round-20 go-live job, which MOVES THE STORE.** That is safe only
because you are pinned. Every figure you report is stamped to store `c120cfd5` and stays true for it
regardless of what main does underneath you. If you re-read main mid-job your numbers become a
mixture of two stores and the deliverable is worthless.

**You write nothing to the tree.** No store byte, no board byte, no pin, no curve file, no pickle in
`data/` or `engine/`. Every output goes to your own session directory.

## 0b · ENVIRONMENT CHECK — FIRST ACT, BEFORE ANY FITTING

    bash bootstrap_env.sh    # installs pinned numpy 2.4.4, hash-verified
    bash bootstrap.sh        # asserts the pin; HALTS if the container is on an unpinned numpy

This is deterministic per container, not intermittent — the check is a sha256 of the OpenBLAS library
bundled inside the numpy wheel, so an environment either matches or never will. It needs PyPI
reachable. **Confirm it passes before doing anything else.** Five minutes here saves finding out at
hour three.

**Never bypass this check.** Different numpy wheels compile `np.interp` differently; the divergence
is ~1e-8 against a board rank-flip threshold of ~1e-12, so an unpinned wheel silently reorders the
board. This guard prevents a *wrong* board, not an imperfect one.

---

## 1 · THE POPULATION — NINE ARTIFACTS, NOT FOUR

The tasking named four. The project's own registry at `boot_guard.py:223` names five, and there are
four more outside it. Enumerated from the artifact, not from the brief:

| # | artifact | pinned in `expected_boot.json` | what it is |
|---|---|---|---|
| 1 | `data/q97m.pkl` | ✔ `q97m` | q97 ceiling model (gradient-boosted trees). Producer: `refit_q97m.py` |
| 2 | `data/v0surf.pkl` | ✔ `v0surf` | V0 surface. Producer: `session_2026-07-18/legf6/scripts/refit_v0surf.py` |
| 3 | `engine/rl_after/peak_model_v4.pkl` | ✔ `peak_model` | peak model. Producer: `engine/forward_valuation/build_peak_model_v4.py` |
| 4 | `engine/rl_after/pvc_snapshot.json` | ✔ `pvc_snapshot` | the peak model's TRAIN-TIME PVC. **See §2 — matched pair with #3** |
| 5 | `engine/rl_after/bust_prior_table.json` | ✔ `bust_prior` | the bust priors. **Producer unknown — see §3** |
| 6 | `data/cm_400.pkl` | ✔ `band` | gradient-boosted tree ensemble, 4.2 MB. Verified by reading the pickle's class references (`sklearn.ensemble._gb`, `DecisionTreeRegressor`, `GradientBoostingRegressor`). Producer not yet identified |
| 7 | `engine/rl_after/pvc_curve_v2.json` | ✗ **not pinned** | the live pick curve. Producer: `session_2026-07-17/legd_derivation/scripts/derive_pvc2.py` |
| 8 | `engine/rl_after/params.json` | ✗ **not pinned** | `AGE_CURVE`, `PEAK`, `PEAK_AGE`. **No provenance record — see §3** |
| 9 | `engine/rl_after/national_draft_last_pick.json` | ✗ **not pinned** | the national/rookie boundary. **See §4** |

Items 7–9 are not pinned, so nothing halts when they go stale. They just quietly are.

**Why these are exposed to the restructure**, traced through `rl_model.py`: the engine sets
`p['pos'] = p['drafted_position']` (`:42`), which keys the cohort curves and the age-curve lookup;
`present_position` sets the year-0 replacement bar; and `pick` feeds `effpk`, which sets the band
pools the pick curve is fitted over. Measured store delta across D1: `pick` 679 changes,
`drafted_position` 538, `present_position` 499, `future_position` 1 — 572 distinct players with at
least one position field moved, plus four new fields populated across 8,711 rows.

---

## 2 · THE PEAK MODEL AND ITS SNAPSHOT ARE ONE ACTION, NOT TWO

`pvc_snapshot.json` is described in the engine as "FROZEN by design". **That is a coupling rule, not
a permanent one, and it must not be read as "leave it alone".**

`build_peak_model_v4.py` trains the peak model with `logPVC` as one of seventeen input features and
**co-emits `pvc_snapshot.json` in the same run** (`:71–:90`) — the file is, in its own words, "a
DERIVED artifact of THIS build". What is barred is moving the snapshot *on its own*, which would feed
the model inputs from a distribution it never saw.

**So: if the pick curve is re-derived, retrain the peak model on it and let the script re-emit the
snapshot.** One action, one script. Do not preserve the old snapshot against a new curve, and do not
refresh the snapshot without retraining.

**Owner ruling of record (2026-07-28):** the snapshot is re-derived along with everything else, as
part of retraining, not held back.

---

## 3 · THE UNKNOWN ROOT — DO THIS BEFORE THE ARITHMETIC

`bust_prior_table.json` and `params.json` carry **no provenance stamp of any kind** and both were last
written on 2 July. We have not identified what produces them.

This matters more than any delta, because `build_peak_model_v4.py` takes `bust_prior_table.json` as an
**input**. The dependency order is:

    priors  →  peak model + PVC snapshot  →  pick curve

and the first link has no known producer. Candidates to check first:
`engine/forward_valuation/build_peak_model_v4.py`, `engine/forward_valuation/build_cohort_book.py`.

**If nothing in the repository regenerates them, say so plainly and stop treating it as a gap in the
measurement — it IS the finding.** It would mean two inputs to every valuation are hand-set numbers
that cannot be re-derived, which is a larger fact than any number this job produces.

---

## 4 · THE STREAM SPLIT EXISTS IN THE STORE AND NOT IN THE ENGINE

D1 added `draft_stream`, `stream_pick` and `stream_year` and populated them across the store
(2,651 / 2,651 / 2,368 rows). **Nothing reads them.** The engine still derives the national/rookie
boundary from `national_draft_last_pick.json`, last touched 11 July, which D1 did not change —
`rl_model.py:197–:215`, where `_NDC` sets rookie-draft effective picks as
`last_national_pick[year] + pick`.

Report whether that table is still correct under the split. Do not change it.

---

## 5 · THE JOIN CHECK — CHEAP, AND RUN IT

The shipped pick curve is fitted over engine-produced values (`v0`, `vpath` from `per_entrant.json`),
so there is a circularity. The fit already answers it by weighting each point by evidence share, with
prior-dominated years fading to zero — but the year-0 datum carries full weight by design, and the
time kernel `exp(-t/tau)` runs at **`tau = 0.12`**, which gives a year-1 observation about 0.0002 of a
year-0 one. The artifact records the development pathway's total influence on the year-0 point as
0.26%.

**A join test on the national draft has already been run and it PASSES.** Comparing players held
against picks paid, national draft only: 2021 1.37 · 2022 1.00 · 2023 1.18 · 2024 1.00 · **2025 0.90**.
There is no entry discontinuity.

**Recorded as a warning, because the seam got this wrong once:** an earlier version of that test mixed
`ND`, `RD`, `MSD`, `SSP` and post-draft entries and priced them all off the national curve, producing
a false 0.17 for the most recent cohort. `PICKLESS={'SSP','MSD','IRE','UNR','PDA','PDN','PDS'}` and
`rl_model.py:218` says it directly — *"MSD/SSP are separate drafts, excluded here."* The mid-season
draft is a separate, weaker pool with no slot on the national curve. **Filter on `type` before you
compare anything to a pick price.**

Re-run the join test on the re-derived curve and report whether it still holds. `build_points()` in
`derive_pvc2.py` already takes `drop_poles` — described in the code as "the prior-removed test" — if
you want the evidence-only variant. This is a sanity check, not the deliverable.

---

## 6 · THE DELIVERABLE — ONE TABLE

For each of the nine:

| column | meaning |
|---|---|
| artifact | path |
| fitted on | the store it declares, or "no record" |
| producer | the script, or "none found" |
| re-derived | its identity when re-run against `c120cfd5` |
| moved? | identical / changed, with the size of the change |
| board effect | how far the board moves if adopted — **scratch board only** |

Board effects are measured on **disposable scratch boards**. Never a bake, never a pin move. Note
that `rl_export.py` refuses to write a bakeable board with `RL_PVCFIT` on (the R3 bake guard), which
is correct and is not to be worked around.

Plus a short recommendation: which of the nine you would adopt, in what order, and what you would
leave alone. The adoption decision is the owner's and belongs to stage 2.

---

## 7 · FENCES

- Read-only against the real store, board, curve files, pickles and `expected_boot.json`.
- No bake, no tag, no release, no score-arm, no pin movement.
- No commit to `main`. Outputs to your own session directory.
- Do not re-read `main` after your pinned checkout (§0).
- Every count names its population — the MSD error in §5 is what happens when it doesn't.
- State plainly anything you could not do. Do not paper it.

## 8 · RETURN

To the seam, with: the environment check result; the nine-row table; the unknown-root finding from
§3; the stream-split answer from §4; the join-test result from §5; your recommendation; and anything
you could not do.

*Filed by the seam authority + supervisor pen, 2026-07-28, on the owner's word. Docs-only.*
