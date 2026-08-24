# PREREG — REBAKE WEEK · ARM 1 · THE STORE-ALONE ARM

**Filed BEFORE any engine or artifact edit (process law P9).** Charter: register v831 (six rebake
decisions ruled) + v833 (the binding handover); directive
`docs/directives/REBAKE_ARM1_STORE_ALONE_2026-08-24.md`.

This arm has **no design content**. It refits the scoped fitted artifacts with the **incumbent
constructions**, verified against source, on the **current store `daa93053`**, and measures the
movement against the live board `6fd0f7de`. **Nothing here touches the live board**: the live pins,
`data/expected_boot.json` and the release contract stay byte-untouched, and the artifacts land at
distinct in-repo CANDIDATE paths.

Correction discipline: where the tree contradicts a line below, **the tree wins and the correction
is named in `REPORT.md`** — never the reverse (P9, and the F5 incident it names).

---

## 0 · BASELINE, ESTABLISHED BEFORE THIS FILING

The seat's isolated workspace (a copy of this worktree's `engine/rl_after` +
`engine/forward_valuation`, never the shared `/home/claude/rl_workspace`) reproduces the live board
**byte-exact** at `RL_CONFIG_MODE=gate`, single-thread BLAS, pinned venv `/root/rl_venv312`:

    md5(rl_app_data.json) = 6fd0f7ded2b280d1a90962c299a152e3   == data/expected_boot.json 'board'

with store `daa93053…`, engine head `3af8c1f7…`, register `652d83e8…` all measured equal to their
pins. Everything below is measured against that reproduction, not against a claim about it.

---

## 1 · THE INCUMBENT CONSTRUCTIONS, READ FROM SOURCE

Read from the tree at commit `99842b3`, not from the studies' prose. Line references are to this
worktree.

### 1.1 `cm_400` — the five-quantile band forests

| | |
|---|---|
| producer | `engine/forward_valuation/par_redesign.py:138 retrain()` → `dist_redesign.py:50 build()` → `conditional_prior.py:143 build_cond_prior(cap=2026, resolved_cut=2021)` |
| estimator | `sklearn.ensemble.GradientBoostingRegressor` |
| hyperparameters | `loss='quantile'`, `alpha=q` for `q ∈ Q=[0.10,0.30,0.50,0.70,0.90]`, `n_estimators=RL_PRIOR_TREES` (manifest: **400**), `max_depth=4`, `learning_rate=0.05`, `min_samples_leaf=25`, `random_state=0` (`conditional_prior.py:159-161`) |
| feature bind at fit | `cp._lvl_eff = par_redesign.lvl_par` — the PAR-centred level feature (`par_redesign.py:124-127,139`). The engine rebinds `cp._lvl_eff`/`cp._feat` for INFERENCE at `_merged_recover.py:1345`; the fit must use the ORIGINAL `cp._feat` |
| training rows | one row per (player, as-of-year `Y`) over `pool = [p for p in MA.data if MA.GRP.get(p['pos'])]`, keeping `debutyr(p) <= 2021` and `(p['pick'] or p['_ft'])`, `Y` from the draft year `d0 = debutyr-1` through `min(last, cap)`; target `fwd_best3_from(p,Y,2026)` |
| T1 | **PRESENT in this construction** (`conditional_prior.py:154-155`): `if _fo is not None and d0 < Y < _fo: continue`, `_fo = first_observable_season()` derived from the store, never hardcoded |
| MSD | **INCLUDED** (no entry-type exclusion in `build_cond_prior`) |

### 1.2 `q97m` — the frozen ceiling

| | |
|---|---|
| producer | `refit_q97m.py` (committed entry point, **never yet exercised**), fitting from the engine's own `X/yy` (`_merged_recover.py:59-64`) |
| estimator | `sklearn.ensemble.GradientBoostingRegressor` |
| hyperparameters | `Q97M_KW = loss='quantile', alpha=0.97, n_estimators=200, max_depth=4, learning_rate=0.05, min_samples_leaf=25, random_state=0` (`refit_q97m.py:40-41`) |
| feature bind at fit | the engine's import-time `cp._feat` with `cp._lvl_eff` at its ORIGINAL binding (`_merged_recover.py` builds `X` before the `:1345` inference rebind) |
| training rows | `_merged_recover.py:60-64`: `debutyr(p) <= 2021`, `(p['pick'] or p['_ft'])`, **and `type != 'MSD'` when `RL_MSD_POOL_EXCL=1`** (manifest: 1); `Y` from `d0` through `min(last,2026)` |
| T1 | **ABSENT from this construction** — there is no `first_observable_season` skip in the `X/yy` loop |

### 1.3 `peak_model_v4` (+ `pvc_snapshot`, co-emitted)

| | |
|---|---|
| producer | `engine/forward_valuation/build_peak_model_v4.py` |
| estimator | `sklearn.ensemble.HistGradientBoostingRegressor` |
| hyperparameters | `max_iter=600, max_depth=5, learning_rate=0.04, min_samples_leaf=30, l2_regularization=2.0, random_state=0` (`:82`) |
| training rows | `build(2006,2015)` — debut window 2006–2015; one DRAFT row per player plus one row per scored year `Y` that has ≥1 future ≥6-game season; 17 features (`:62`) incl. `bust_prior` from `bust_prior_table.json` |
| co-emit | `pvc_snapshot.json` = `{str(k): float(MA.PVC[k])}` over the asserted 1..65 domain (`:110-120`) — regenerates with its model, never separately (v831 D6; `rl_model.py:1234`) |
| T1 | not applicable — a different construction with its own row rule; draft rows are real zeros by design |

### 1.4 `bust_prior_table` — **NO PRODUCER EXISTS IN THE REPOSITORY**

Searched the whole tree and the whole filesystem: the only code that names
`bust_prior_table.json` **reads** it (`build_peak_model_v4.py:26-27`, `rl_model.py:1233`,
`single_source.py:35`, `boot_guard.py:227`) or **renames position keys inside it**
(`session_2026-07-29/item262/migrate_positions.py:128`). `git log --follow` shows exactly two
commits: the initial verified seed and the #262 vocabulary rename. `SHIP_GATES.md:295` asserts it is
"regenerated ONLY by `build_peak_model_v4.py` at a bake" — **that claim is false against source**;
that script only reads it.

**PREDICTION P0 (a blocker, declared before the work):** this arm will NOT be able to refit
`bust_prior_table` with an incumbent construction, because no incumbent construction exists to
verify. Per the directive's stop rule, the seat will STOP at that artifact and report it rather than
invent a construction. `docs/directives/PRIORITY_1_STAGE_1_fit_measurement.md` §3 anticipated exactly
this and ruled the finding is the deliverable.

---

## 2 · THE EXHAUSTIVE SHIPPED-vs-REFIT DIFFERENCE LIST

The directive names two differences. Confirmed against the tree, with one correction:

1. **The training store is current (`daa93053`) rather than the 2026-07-15→17 epoch** — holds for
   all refitted artifacts. Study A dated the shipped band/ceiling from the quantile constants at each
   forest root; study B from the training-row counts in the trees (`cm_400` 13,226 / `q97m` 13,111).
2. **T1 (the fabricated-zeros rule) is applied** — **holds for `cm_400` only.** T1 lives in
   `conditional_prior.build_cond_prior` and in no other construction. `q97m`'s row rule
   (`_merged_recover.py:60-64`) has never carried it; `peak_model_v4`'s row rule is a different
   object entirely. **CORRECTION FILED IN ADVANCE:** applying T1 to `q97m` would be a change to its
   training-row rule — i.e. design content — and this arm carries none, so the `q97m` candidate is
   fitted **without** T1, exactly as its committed entry point specifies. The q97m-with-T1 row count
   and artifact hash will be measured and REPORTED as a side reading so the owner can rule on it in a
   later arm; it will not be the candidate.
3. **Consequential, not a third choice:** the `pvc_snapshot` co-emit tracks whatever `MA.PVC` is on
   the current store/curve, so it moves with its model by construction.

Nothing else changes. Same estimator classes, same hyperparameters, same feature binds, same row
rules, same `random_state`. **The read-site ratchet (`RL_O44_LVLMONO`, code default `'ratchet'`,
absent from the manifest so gate mode leaves the code default standing) stays ON.**

---

## 3 · DECLARED SWITCHES — every one of them, wired at one site, defaulting to shipped

No undeclared environment variable will be introduced. Exactly these:

| name | site | default | why it is needed |
|---|---|---|---|
| `RL_CM_PKL` | `engine/rl_after/wire_redesign.py build()` — the single cm load site | **unset ⇒ `/home/claude/cm_<RL_PRIOR_TREES>.pkl`, byte-identical to shipped** | the band is the ONE fitted artifact loaded from an absolute out-of-repo path with no override; a candidate board cannot read a candidate band without one, and the directive forbids overwriting `/home/claude/cm_400.pkl` |
| `RL_CM_PKL` (guard mirror) | `boot_guard.py _resolve_cm_load()` | same | `_resolve_cm_load` must mirror the engine's precedence **byte-for-byte** or Guard 5 certifies a path the engine does not take (the block's own stated rule). This is not a second switch; it is the same switch's mandatory mirror |
| `RL_CM_PKL`, `RL_Q97M_PKL` | `config_manifest.INFRA_ALLOW` | n/a | both are PATH vars, not model semantics. `RL_Q97M_PKL` is already wired in the engine (`_merged_recover.py:87`) and already mirrored in Guard 5 (`boot_guard.py:255`) but is **absent from `INFRA_ALLOW`**, so `enforce('gate')` rejects it as an UNKNOWN model override — a shipped switch the gate cannot tolerate. Adding both to `INFRA_ALLOW` does not move `config_sha256` (the hash is over `manifest['vars']` only) — **this will be measured, not assumed** |
| `RL_ARM1_OUT` | `engine/forward_valuation/build_peak_model_v4.py`, one resolver | **unset ⇒ the shipped output paths** | lets the peak-model build emit a CANDIDATE set without touching the live pickles |

`RL_BAKE_REFIT` is the existing gate on `refit_q97m.py --bake`; this arm does **not** use `--bake`
(it re-pins `expected_boot.json`, which is forbidden here) and adds a candidate mode instead.

---

## 4 · WHAT WILL BE BUILT

1. `tools/rebake/refit_arm1_store_alone.py` — ONE committed, versioned orchestrator, emitting to
   `docs/evidence/rebake_arm1_store_alone_2026-08-24/candidates/`:
   `cm_400.candidate.pkl`, `q97m.candidate.pkl`, `peak_model_v4.candidate.pkl`,
   `pvc_snapshot.candidate.json`, plus `training_stamp_<artifact>.json` **beside each pickle**
   (training store md5, row count, hyperparameters, feature bind, old→new artifact md5, library
   versions) — every hash **measured from the artifact**, never typed (P4).
2. `engine/rl_after/wire_redesign.py` — the **cm loader HALT**: the silent-refit-on-cache-miss
   fallback (`:55-62`) deleted, replaced by a HALT naming the missing path, matching the sibling
   q97m and v0surf freezes.
3. `engine/forward_valuation/build_peak_model_v4.py` — its **two out-of-repo output paths**
   (`training_store_stamp.json`, `age_source_census.json`, both written to
   `/home/claude/rl_workspace/rl_after/`, where nothing can read or assert them) made repo-anchored.
4. A **candidate root** in scratch: a copy of this checkout with the candidate artifacts at the
   pinned artifact paths and its OWN `expected_boot.json` re-pinned, so Guard 5 runs **honestly**
   against a coherent candidate world. The worktree's committed `data/expected_boot.json` is
   byte-untouched and will be shown so.
5. The candidate board, and a **third board** with T1 disabled at the cm fit and nothing else
   changed, for the T1 attribution.

---

## 5 · PREDICTIONS

Numbered so each can be scored right or wrong.

**Movement**

- **P1.** The candidate board will differ from `6fd0f7de`. Predicted movers: **> 600 of 804 rows**
  (the store moved twelve versions, ~700 pick moves, ~300 players' guessed ages replaced, and the
  band feeds `price6` at weight 0.90 across every row).
- **P2.** Movement will be **two-directional, not a level shift**: both up-movers and down-movers
  will exceed 100 rows. Falsified if either direction is under 100.
- **P3.** The median absolute move will be **under 8%**; the distribution will be long-tailed with a
  small number of large movers. Falsified if the median |move| exceeds 15%.
- **P4.** The largest movers will concentrate in **young / thin-evidence rows** (tenure ≤ 3), because
  those rows are priced mostly by the prior and least by their own demonstrated level.
- **P5.** T1's own contribution to the board will be **small next to the store's** — under 15% of
  the total absolute movement. It removes ~0.5% of training rows (64 of 13,221 measured at the word).

**Artifacts**

- **P6.** Every candidate artifact hash will differ from its shipped pin. A candidate that reproduces
  its pin would mean the store did not move the fit and would be reported as such.
- **P7.** `cm_400`'s candidate training-row count will differ from the 13,226 read out of the shipped
  pickle, and will be **lower than the same fit with T1 disabled**, by exactly the fabricated-zero
  count.

**Gates and batteries**

- **P8.** The full-population level census (V3) at the read site, over all 804 board rows across the
  model's level range, returns **ZERO descending steps** — by construction, because the ratchet is a
  running maximum over a nested sample set. The RAW (pre-ratchet) band census will **not** be zero
  and will land near the shipped artifact's own 23.40% (study B M-21) and the incumbent-refit 25.15%.
  Both numbers will be reported; reporting only the zero would be dishonest.
- **P9.** B2 / B6 / G-Y0 all PASS on the candidate board. Falsifier: any of them fails.
- **P10.** Pinball, measured on the study-A §5.1 protocol (rolling-origin by debut year, whole
  careers held out, three folds), lands **within ±1.5%** of the §5.1 design-(a) baseline **3.9703**.
  A store-alone refit is the same estimator on a fresher store, so a large move would mean the store
  changed the problem, not the model — and would be reported as such.
- **P11.** The law-9 mint will be **non-zero and positive** (the ratchet is a one-sided operator and
  already mints under the recorded waiver). Reported, not gated (v830).
- **P12.** The per-arm no-arb reading will be taken on THIS arm's candidate and will not be inherited
  from any sibling.
- **P13.** Fit-twice reproducibility: the two fits will be **byte-identical on this one box** for the
  `random_state=0` tree fits, and this is NOT a claim about other boxes — `wire_redesign.py`'s own
  CACHE HONESTY note records a measured non-reproduction (`b271ed2e` vs `34faa865`), and OpenBLAS is
  DYNAMIC_ARCH. Whichever way it lands it is recorded honestly (scope paper §5.5). **This prediction
  is the one this seat is least confident of.**

**Byte-unmoved**

- **P14.** After the `wire_redesign.py` loader HALT lands, the board rebuilt from the live artifacts
  is **byte-identical `6fd0f7de`** (P1 of the rulebook). The deleted branch is proven unreachable
  with the cache present AND proven able to fire (non-vacuity) by pointing `RL_CM_PKL` at a missing
  file.
- **P15.** `data/expected_boot.json`, `data/release_contract.json`, the live pickles and
  `/home/claude/cm_400.pkl` are byte-unmoved at the end of the arm, shown by measured md5s.

---

## 6 · FALSIFIERS — results that would stop this arm

- **FA1.** The seat cannot reproduce `6fd0f7de` from the isolated workspace → the environment is not
  the pinned one and **no measurement in this arm means anything**. *(Already discharged: §0.)*
- **FA2.** A candidate artifact cannot be produced by the incumbent construction read from source —
  i.e. the construction is not verifiable. **STOP at that artifact and report.** Declared in advance
  for `bust_prior_table` (P0).
- **FA3.** The board rebuilt from live artifacts after the loader HALT is not `6fd0f7de` → the
  "behaviour-unchanged" claim is false; **revert the edit** and report (the H3 back-rows precedent).
- **FA4.** The deleted fallback cannot be shown able to fire → the HALT is a vacuous guard and fails
  the standing non-vacuity norm.
- **FA5.** Adding names to `INFRA_ALLOW` moves `config_sha256` → the change is not
  infrastructure-only; **revert** and find another route.
- **FA6.** The level census at the read site returns any descending step → the ratchet does not do
  what its own docstring proves, and the arm reports a live law-3 breach rather than a candidate.
- **FA7.** Any gate cannot be RUN (as opposed to failing) → report UNMEASURED, never "assumed
  passing" (PART 3, and process law P5: a gate's name is not coverage).
- **FA8.** The arm moves any live pin, tag, or the release contract → an abort, not a footnote.

---

## 7 · WHAT THIS ARM WILL NOT DO

No design content of any kind: no estimator change, no monotone constraint, no age reparameterisation,
no recency weighting, no hyperparameter re-selection, no ratchet retirement, no scope beyond v831 D6.
`v0surf` is untouched. No tags, no live-pin moves, no rulebook edits, no `docs/register/` writes, no
PRs, no pushes. The board moves ONCE, at week's end, on the owner's word, through `tools/land lever`.
