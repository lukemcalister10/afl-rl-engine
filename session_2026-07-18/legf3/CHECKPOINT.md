# LEG F3 — PROJECTION FIX · CHECKPOINT (measure-first; the localization does not hold) · seat 13 · 2026-07-18
**Status: HALT-AND-RETURN pending an owner ruling on scope. No engine file edited. Balanced board untouched.
Container-relative entry proven. The item-352 finding REPRODUCES; its *localization* to the two named sites
does NOT survive contact with the engine.** SILENCE IS A RED — this is the finding, stated.

Branch base: re-based (local only, not yet pushed) onto the code-lineage tip
`7b6dfc52` (GIT ENTRY mandate; my harness branch was mis-based on the disjoint docs-lineage `main`).
DATA anchors ABSOLUTE + matched: store `968de0c7` · curve `56dd7a7b` (payload `89c14729`).

---

## A. ENTRY PROOF — FILED HASHES REPRODUCE BYTE-EXACT (correction; supersedes the first-build reading)
**CORRECTION (register-worthy):** an early single build reported balanced k=0 = `30d96f1f` and I wrongly
generalized "SkylakeX ≠ Haswell, container-relative." A controlled re-test **refutes** that:
- Pristine balanced (`RL_LEGE=0 RL_PVC2=1 RL_LEGF=0`, single-thread) = **`06d8af60` on 3/3 consecutive
  builds** — the FILED hash, byte-exact, matching F1's container and item 349. The `30d96f1f` was a
  **cold-start / first-build anomaly** (not reproduced since); it is NOT a stable SkylakeX board.
- The `OPENBLAS_CORETYPE=Haswell` diagnostic that printed `30d96f1f` was run in that same early window; it is
  **not** evidence of a kernel-invariant board and I withdraw the "physical-chip, pin-nothing" conclusion for
  THIS container. The standing doctrine (item 347, container-relative + numeric-stack annex) still governs the
  *reporting*, but on THIS box the filed absolutes DO reproduce, so the byte-exact gates are stated against
  them (`06d8af60` / and the RL_LEGF=0 chain), exactly as the directive entry asks.
- DATA anchors absolute + matched: store `968de0c7` · curve `56dd7a7b`.
- Numeric stack: py3.12.3 · numpy2.4.4 · scipy1.17.1 · sklearn1.8.0 · scipy-openblas 0.3.31.188.0
  DYNAMIC_ARCH · threads pinned 1 (OPENBLAS/OMP/MKL/NUMEXPR). LESSON: warm the build; never generalize a
  reproducibility claim from a single cold run (SILENCE-IS-A-RED corollary: a WRONG flag is also a red).

## B. ITEM-352 REPRODUCED ON THIS CONTAINER (probe_decomp.py, RL_LEGE=1 RL_PVC2=1, single-thread)
| cohort | n | Δ now→+1 | % |
|---|--:|--:|--:|
| developing ≤23 | 375 | −112,574 | **−30.8%** (steepest — the inverted gradient) |
| mid 24–27 | 210 | −59,737 | −24.2% |
| veteran ≥28 | 219 | −51,316 | −28.9% |
| **total** | 804 | −223,627 | **−28.3%** |
young ≤23 / pick ≤20 / games ≤40 (n=62): **−34.1%**. Matches the investigation (−33.3% / −37.5%). CONFIRMED.

## C. THE MEASURED MECHANISM (probe_legs.py + probe_validate.py) — TWO DRIVERS, NEITHER AT A NAMED SITE
For a young pedigree row (e.g. Jagga Smith 20, pk3: v26=3587, v27=971, V0=3469):
1. **(A) Pedigree-prior fade with the AGE clock.** `raw_ev ≈ _par_prior` for thin evidence
   (`_merged_recover.py:334`: `(1−_ev_pw(Eq))·prod + _ev_pw(Eq)·_par_prior`). Forward, `raw_ev` drops
   3622→2681 (−26%) even though projected *level* RISES — because the pedigree prior fades with the
   advancing **seasons/age clock** (`decay≈1−(seasons−1)/4.5`, rl_model.py:1131 self-diagnosis), keyed on
   `AGE_REF`, not on projected evidence. This is the §2.vi violation: age erases pedigree.
2. **(B) Staleness gate on the advancing tenure clock.** `_merged_recover.py::ev` (~:1262):
   `if tenure≥onset and produced_seasons≤1: e = min(e, 0.25·V0)` → then floored to `0.28·V0`.
   `tenure` advances with `AGE_REF` (via `cp._feat`), produced-seasons cannot (no future scoring rows),
   so the forward lens mislabels developing top picks as **stalled prospects** and crushes them to ~0.28·V0
   (Jagga _prod_path 2681 → ev 971). This is the "155 mislabeled exits" defect, upstream of the exit rule.

**Verified by patch:** anchoring only the passed eval-year `Y` moved nothing (−28.3%→−28.2%) — the clocks read
`AGE_REF`/`cp._feat`, not `Y`. The correct anchor is BASE_REF on the pedigree-fade + staleness clocks.

## D. THE FENCE / LOCALIZATION TENSION (the reason this is a checkpoint, not a diff)
The addendum §2.vi localizes to `rl_model.py::proj_from_peak` + `rl_export.py:96` (form anchor) + the exit.
The engine says otherwise:
- **The board's active `proj_from_peak` is `_proj_w4` (`_merged_recover.py:787`)**, a parallel W4 copy that
  reimplements the loop and carries its OWN runway/elite term (`:806`). rl_model.py:456 is delegated-to only
  for synths/lever-off. Editing rl_model's copy alone does NOT move the board (the codebase's own
  "edit BOTH or neither" duplicate-loop doctrine, cf. `prod_floor`/`_prod_floor_w4`).
- **Drivers (A) and (B) both live in `_merged_recover.py`** (pedigree-prior fade in `raw_ev`; staleness in
  `ev`), both consume `AGE_REF`. proj_from_peak's runway/elite gate is a *contributor* to (A) but not the
  dominant term; the rl_export:96 form anchor already splits AGE/BASE for `level_demo`/`peak_est` — it simply
  does NOT reach the pedigree-fade or the staleness clock.
- The fence marks `_merged_recover.py` V0/`_iso_dec` chain HARD-OUT. The needed edits are the **form-anchor's
  unfinished consumption sites** (pedigree-fade clock + staleness clock → BASE_REF in the forward lens) — NOT
  the V0 curve / isotonic chain itself — but they ARE in `_merged_recover.py`.

## E. THE PROPOSED REID-COMPLIANT FIX (for the ruling — NOT yet applied)
Complete the form anchor: in the forward lens (`AGE_REF>BASE_REF`), the **pedigree/evidence blend keys on
projected EVIDENCE (BASE_REF), not the advancing AGE clock**. Concretely, forward-gated (so k=0 byte-exact by
construction, `AGE_REF==BASE_REF`):
1. Pedigree prior `_par_prior` / `_ev_pw` fade → evaluate the pedigree-decay clock at BASE_REF (games/Eq held
   at now), decaying smoothly with projected evidence (φ, no cliff). "One more year of thin production does
   not erase draft pedigree." No new multiplier, no lens-only growth term — a REMOVED lens-only *penalty*.
2. Staleness gate in `ev` → tenure/produced-seasons keyed at BASE_REF, so a developing pick is not relabeled
   "stalled" purely by the clock advancing. This also un-mislabels the exit-side (feeds §2.iii cleanly).
3. §2.iii distributed retirement (rl_export exit) + §2.vi proj_from_peak runway (pedigree-carry, both copies)
   applied as signed — but they are secondary to 1–2.

**This edits `_merged_recover.py` beyond the two named sites** (though not the V0/_iso_dec chain). That is the
scope decision. Per the directive's own law — "justify or HALT", "hard-to-reverse = HALT", "HALT and return
the tension, never bend a law to pass a number" — I am returning it rather than silently widening the fence
or hacking proj_from_peak to force ±5%.

## F. WHAT I HAVE NOT DONE (deliberately)
No engine edit. No force-push. No k=0 movement. The ±5% number is NOT yet produced because the only path to
it that the engine supports requires the scope ruling in §D/E. Awaiting: (a) fence ruling; (b) confirm the
container-relative reproducibility doctrine for the byte-exact gates.
