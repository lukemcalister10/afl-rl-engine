# The no-arbitrage measurement — owner order 3 (5186108632), measured 2026-08-05

Whole-cohort mean engine value at years 0..7 (extended 0..9) after draft, for the 1,197 national-draft
picks 1-64, classes 2004-2022. Busts stay in the denominator at zero at every year. Values are the
engine's own as-of valuations (not raw scores), VOR board points. Full method and captions are in the
scripts' own headers; results as measured are in `noarb_table.json` and the register v573 entry.

HEADLINES (measured on the pre-re-closure basis; the re-closure moved the ladder by at most 2 points
at any pick, so these shapes stand): draft-day 1.00x -> 1.57x at years 4-5 -> 0.84x by year 9.
The 2020 class never delivers the hump (0.92-1.13x). Recency windows keep it (~1.5x).

TO RE-RUN ON FINAL BYTES (the review-set commit should do exactly this):
1. Copy the current matrix (the store-act confirmation emit, committed at
   `docs/evidence/store_328_jujn3g/per_entrant_328_confirmation.json` on the merged history) beside
   these scripts as `pass3_matrix.json` (the scripts' expected input name), and the CURRENT re-pinned
   harness from main (`session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py`) as
   `harness_pvc_REPINNED_pass3.py` (the scripts' import name).
2. `OPENBLAS_NUM_THREADS=1 $RL_VENV/bin/python noarb_table.py` then `noarb_ext.py`.
3. The harness asserts the matrix identity pins itself; if it halts, the pins moved - re-point, never
   patch. Update the expected md5 note inside noarb_table.py's header if the input matrix is the newer
   one (the header documents the 2026-08-05 input; the METHOD is version-independent).
