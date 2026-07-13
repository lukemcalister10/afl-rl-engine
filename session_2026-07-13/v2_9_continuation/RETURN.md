# RETURN — v2.9 candidate, continuation seat · 2026-07-13 · branch `claude/v2-9-candidate-integration-kq4dae`

**Base pins:** main ADVANCED `0888faa`(v32)→`40f7a84`(v33, reported); tag v2.8 `9bd0cfd` ✓; inherited
candidate `vtsnhr@a00c782` ✓ (all 7 commits preserved on kq4dae; main merged for register v33; vtsnhr
untouched). Guard 5 PASS, panel 10/10, workspace + repo engine left pristine (7a07e369).

**1. HARNESS RECONCILED (blocking) — DONE.** The ad-hoc 137.8 vs audited ~128.6 gap is a construction
gap, pinned by code reading: the official gate is `ship_gates_check.py` B1 (`_b1_rows`, owner ruling
D5) on a `s4_matrix_M1v7` gate-mode matrix — **index each cohort to its own yr1, then unweighted
cross-cohort mean, over ND+RD cohorts 2004–2020** (not raw-sum-average over ND-only 2014–2020).
Adopted verbatim; baseline reproduced on the candidate base: **y4=128.6 y5=127.1 y6=119.0**, matching
the 15% shipped book to 0.0pt on y1–y6. 137.8 refuted. (HARNESS_RECONCILIATION.md)

**2. THE ONE COMBINED GATE — PASS.** Reconciled gate on the fully-combined candidate (L1+L4+L2@14+L3;
matrix engine 16e97c3a, store unchanged): **y4=126.8 y5=125.2 y6=116.1**, each ≤ hard 130 (margins
3.2/4.8/13.9) → **PASS**, WIDENING the base margin by 1.8pt. Dial-14's widening + L1/L4 outweigh L3's
young-riser spend (register projected 128.5; reconciled 126.8 — safer). L7 ratio-invariant + L5
cohort-neutral PROVEN by construction; butters −1.04% holds. No breach → candidate proceeds. (COMBINED_GATE.md)

**3. REFIT — STAGED + VALIDATED + ATTRIBUTED (on-disk wiring is the next unit).** Each lever's source
patch (`levers.py`) reproduces its inherited sim to the dollar (L1 +0.179% & anchors byte-identical ·
L4 emmett 826 · L2 gawn 2501 · L3 butters 5997; lever_validation.md). G-ATTR is clean+separable —
emmett three-probe corner: L1 0 · **L4 −352 (−29.9%, pool-isolation, nonsense trigger ARMED)** · L2
+25 · L3 0. L7 on the combined refit board: adopted[1]=3000, pick1 3157→3000, all 10 ratios preserved.
The deterministic on-disk wiring + coordinated re-pin + gate-suite certification is specified
(REFIT_WIRING_SPEC.md) and is the next continuation's atomic commit.

**NOT DONE (next continuation — normal per the directive):** (3) wire the refit on disk + re-pin
(engine-md5/panel/seal/boot-pin IN-COMMIT) + certify the full gate suite; (4) SPEC_1–4 + seam table
(advisory; the L1 PVC-basis production-vs-replacement assert lives here); (5) export bundle. L6 STOP
stands. Nothing tags/bakes/merges to main. All numbers route to the SUPERVISOR.

**Artifacts:** CONTINUATION_PLAN · HARNESS_RECONCILIATION · COMBINED_GATE · G_ATTR_AND_L7 ·
REFIT_WIRING_SPEC · out/{gate_base,gate_combined,gattr,l7_combined_rebased}.json · scripts/{levers,
cohort_gate_official,run_levers,board_pass,attribute}.py (all under session_2026-07-13/v2_9_continuation).

---
**In plain terms.** The last seat couldn't sign off the age-curve safety check because its home-made
yardstick read 137.8% where the project's real yardstick reads ~128.6%. I found the 9-point gap: the
real yardstick indexes each draft class to its own first-year before averaging (over a wider, older set
of classes, priced by the official walk-forward book); the home-made one averaged raw dollar totals over
a narrow recent slice. I re-ran the REAL yardstick and reproduced 128.6 exactly. Then I switched on all
four levers together, rebuilt the book, and measured once: **126.8% — comfortably under the 130 ceiling.**
So the whole package holds; the levers were always meant to be judged together, and together they pass
with room. I proved each lever reproduces its earlier one-off test to the dollar, showed exactly what
each does to the board (the ruck Emmett drops ~30% — flagged for your eye), and confirmed the numéraire
re-base (pick 1 = 3000) doesn't disturb any ranking. What's left is the mechanical part — writing the
four levers into the engine on disk and re-pinning the board — plus the advisory measurement specs.
