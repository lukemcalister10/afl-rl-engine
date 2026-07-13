# RETURN — JOB A v2 — B1 CODE-CONFORM + SILENT-GATE FIX

- **Branch:** `claude/b1-conform-silent-gate-pgm98w` · **Work head SHA:** `cb5b31bfca47367003058e840b9ef22b864f9317` (this RETURN adds one commit on top) · **PR:** #70 (candidate — NOT merged, NOT tagged).
- **Base drift (reported, benign):** main `87cc7bd` = the directive's `d8acc802` + one docs/register-only commit (register v67, the announcement of this job); `d8acc802` is an ancestor; store `340a7a32` / board `3dc19fbb` / Guard 5 unmoved. AskUserQuestion couldn't deliver (non-interactive); proceeded on the recommended path and recorded it.
- **B1 ratios (4dp):** y4 **1.2601** · y5 **1.2407** · y6 **1.1521** — PASS ×3 (hard ≤ 1.30).
- **Five class sums:** y1 **69,840.0** · y2 **79,298.2** · y4 **88,002.4** · y5 **86,652.9** · y6 **80,460.5** (avg of raw class-year sums across the 17 classes 2004–2020, incurve ND+RD).
- **Denominator:** min(y1, y2) = **y1 = 69,840.0**.
- **Matrix:** regenerated at head via `s4_matrix_M1v7.py` (gate mode); verify-shard md5 **8e4e68179943435906a9c767e59b5832**, `__meta__` engine 2030e5df / store 340a7a32 / n_players 2649.
- **Red-path proofs:** breach HALT → `session_2026-07-13/b1_conform/scripts/prove_breach_halts.py` (exit 0). silence HALT → `session_2026-07-13/b1_conform/scripts/prove_silence_halts.py` (exit 0, missing + unreadable matrix, B1 named).
- **Store & board byte-unchanged:** store `340a7a32` and board `3dc19fbb` identical before/after the full suite (B4 also re-derived the board to `3dc19fbb`).
- **Suite reds exactly {A2, A3, A12}:** full suite VERDICT FAIL=3 (A2/A3/A12) PASS=17 FEATURE=1(B5) PENDING=4 STRUCK=1; exit code 1.
- **Obituary:** `session_2026-07-13/b1_conform/OBITUARY_cohort_gate_official.md` (+ one line in `SHIP_GATES.md`); `cohort_gate_official.py` deleted; historical `run_suite.sh` untouched.
- **Indexed reading:** kept only as a labelled non-gating SHAPE diagnostic (peak position + pre-peak dip); 126.8/125.2/116.1 never printed as the gate.

## In plain terms
The cohort gate now does the sum the owner actually asked for — add up each draft class's player values year by year, average across classes, and check the later years never sit more than 1.30× above the earliest; on today's data it lands at 1.26/1.24/1.15, comfortably fine. Just as important, the gate can no longer "pass" by staying silent: if it can't run, can't read its input, or blows up, it now shouts RED and the whole suite fails loudly instead of printing a green tick over an empty result — the exact failure that slipped through last time. Nothing else on the board moved.
