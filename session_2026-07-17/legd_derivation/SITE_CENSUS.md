# SITE CENSUS — the PVC derive / load / refit / consume sites (item-281, from the code)

Base `33c8b52`, store `968de0c7`. Line numbers are on THIS tree (the directive cited `:801`/`:1157`
"re-named from YOUR tree" — the real lines are below). **Two instruments, never blurred** (groundwork
Job 1): the **PVC** = the pick's value the day BEFORE the draft (what we re-derive); the **V0 curve /
`v0_start`** = the player's value the day AFTER (the G-Y0 gate's population instrument).

## A. THE DERIVATION SOURCE (READ; leave untouched)
- **`s4_matrix_7147.py:62`** — `anchor = ASOF.get((id(p), C+1))  # END OF CALENDAR YEAR 1 … = the curve
  anchor`. The as-of end-of-yr1 value that every PVC construction reads. Walk-forward ASOF at
  `s4_matrix_7147.py:24-42`. **The re-derivation reads this; it does not change it.**

## B. WHERE THE PVC IS DERIVED / REFIT
- **IMPORT-TIME FIT (rl_model.py, FENCE-OUT):** `MA.PVC` is built at module import by
  **`build_pvc_v34()` → `rl_model.py:714`**, then `CURVE_H` (:716), the `RL_PICK1=3000` `BOARD_FACTOR`
  pin (:720-722), and `_deplateau` (:726-737). This is a PAVA-isotonic + local-linear + parametric-top
  fit **run at import** — the classic import-time-fit pattern PART 7 flags. It emits with **plateaus
  allowed** (:712, `_deplateau` leaves the deep-tail floor flat) — the structural source of the shipped
  curve's tail flats.
- **OFFLINE-DERIVED ARTIFACT (the shipped ev-channel basis):** `pvc_curve_L1b.json` — derived OFFLINE by
  `l1_adopt_sim.py` (PAVA isotonic + kernel-smoothed adaptive-bandwidth; pick-1 pinned 3000), per the
  artifact's own `source`/`derived_from`/`curve_md5=645fce16` stamp. **Loaded, not refit** — the good
  pattern the new curve must follow.

## C. WHERE THE CURVE IS LOADED (FENCE-IN)
- **`_merged_recover.py:1336-1342`** — the `RL_PVCADOPT` block (default ON): loads `pvc_curve_L1b.json`
  into **`_PVC0`** (`:1338-1339`), then rebuilds the V0 guard, V0 curve, and RUC ceiling
  (`_build_v0_guard()`, `_build_v0_curve()`, `:1340-1341`) and clears the price cache. `RL_PVCADOPT=0`
  ⇒ block skipped ⇒ `_PVC0` stays the frozen v3.4 ruler ⇒ base board byte-exact. **This is the exact
  template for the new `RL_PVC2` load block.**
- `rl_export.py` also reads `pvc_curve_L1b.json` (display/book).

## D. THE V0 INSTRUMENT (import-time `_iso_dec` chain — the G-Y0 gate input, NOT the PVC)
- **`_merged_recover.py:1121`** `_iso_dec` · **`:1122`** `_fit_pick_curve` · **`:1133`** `_fit_mature` ·
  **`:1154-1170`** `_build_v0_curve()` (called at import, `:1170`) · **`:1171`** `v0_start(p)`.
  This builds `_V0CURVE` = the day-after V0 board surface = the G-Y0 gate's population instrument. It is
  an **import-time refit** (the `_iso_dec` determinism input PART 7 names). **The new PVC path is offline
  + loaded and adds NO import-time fit; it does not touch this chain.** The chain is *re-run* by the
  adoption block (`:1341`) because a new `_PVC0` moves `_v0_raw`'s inputs — that is the existing L1b
  behaviour, preserved, not new.

## E. WHERE THE CURVE IS CONSUMED
- **`_PVC0` (the ev-channel basis — moves with the artifact, FENCE-IN):** `draftval(p)`
  **`_merged_recover.py:1331`** → the RUC prior-cap/scaffold (`:1054,:1058,:1234`) and the D12 floor
  basis (`:1317`, `floor_frac × v0_start` — actually re-anchored to V0, draftval purged from penalties).
- **`MA.PVC` (the v3.4 ruler — NOT swapped by `RL_PVCADOPT`, consumed in `rl_model.py`, FENCE-OUT):**
  `PVC[min(ep,70)]` at **`rl_model.py:798`** (pickless `unpl_eq`) and **`:813`** (pedestal); the
  `_natcv34` inversion base **`:834-853`** (pickless `_eff` pick-equivalents); the frozen peak-model
  feature `pvc_snapshot.json`/`_V4PVC` **`:515,:530`** (train-time, must NOT track live PVC — train/serve
  skew).
- **The ladder/board display** reads the pick currency for the pick-band assets (held pick, 2027 picks).

## VERDICT — fence in/out (the checkpoint question)
The **fence-clean re-derivation** wires `RL_PVC2` as an exact parallel of `RL_PVCADOPT`: load the new
stamped curve into `_PVC0` + rebuild the V0 guard/curve/RUC ceiling. That is **fully IN-FENCE**
(`_merged_recover.py` + the artifact + `one_source_selftest.py` wiring); `RL_PVC2=0` reproduces the
shipped L1b path (board `9829d01a`) byte-exact. **What the re-derivation must replace:** the `_PVC0`
contents (the ev-channel/`draftval` basis). **What it must leave:** `s4_matrix:62` anchor, the
`v0_start`/`_iso_dec` V0 instrument (gate input), the walk-forward ASOF, and `MA.PVC`'s import-time
scaffold.

**HALT-AT-CHECKPOINT flag (item-281, I do NOT extend the fence myself):** the census **names live PVC
consumers in `rl_model.py`** — the pickless `unpl_eq` (:798), the pedestal (:813), the `build_pvc_v34`
import fit (:714), the `_natcv34` inversion (:834-853), and the peak-model `pvc_snapshot` feature
(:515). These read `MA.PVC`, which the L1b/`RL_PVCADOPT` precedent leaves on the v3.4 ruler. **I
recommend the fence-clean `_PVC0`-only swap** (matching the shipped design — the held-pick ladder and
the G-Y0 gate both read the ev-channel basis). **Whether the new curve should also reach the
`rl_model.py` `MA.PVC` consumers is a fence-extension question for the owner at the checkpoint.**
SEASON_PROG=0.58 (`rl_model.py:738`) is the owner dial — untouched.
