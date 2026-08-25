# ARM 2 · RECENCY-LESS REFIT (NOREC) · prereg-style declaration, written BEFORE the run · 2026-08-25

WHY THIS RUN EXISTS: register v847(2) — the recency weighting's ruling (v831 D3) was made on study B's
+0.2% gain, measured on the protocol FB2 proved leaks within-player (76-100% train/test overlap); on the
clean whole-career protocol the sign reverses (~-0.45%). The supervisor's scoped recommendation is
exact+hill, DROP recency; v847 requires this refit run BEFORE the packet so the owner rules on the real
candidate, not an extrapolation. "uniform" was a DECLARED point of the prereg'd half-life grid
(select_arm2.json: uniform mean 3.9174 vs hl12 3.9058 on the walk-forward protocol — the leaky-protocol
+0.296% the owner will see beside the clean-protocol reversal).

CONSTRUCTION: the committed entry point tools/rebake/refit_arm2_design.py (md5 4839da16, arm2-design/1),
selection file = the arm's own select_arm2.json with SELECTION.recency_halflife_years -> null (uniform;
conditional_prior.py:195-196 / exact_monotone.recency_weight(None) -> sklearn no-sample-weight).
a*=21.5 stands: the selection procedure chose a* at stage 2 BEFORE the half-life at stage 3, so the
recency-less world is exactly the stage-2 world. The ceiling re-selects its own capacity under uniform
weights per the entry point's own declared procedure (grid + boundary extension). Root assembly and board
emit follow the canonical reconciled choreography (fingerprint.json env: RL_CM_PKL/RL_Q97M_PKL at
root/data, workspace seeded FROM the root so the peak/pvc cwd-relative loads read candidate bytes —
the v844 loaded-path lesson).

PREDICTIONS (falsifiable, declared now):
P-N1. cm_400 candidate md5 MOVES from 03a05c56 (weights change the fit); q97m moves from d3112824.
P-N2. peak_model_v4 candidate md5 == 5338d0cd BYTE-EXACT and pvc == 4704b829 (recency touches only
      band+ceiling; the peak build takes no half-life input). If this fails, the recency dial reaches
      further than the design says and the packet must say so.
P-N3. The emitted board DIFFERS from 6bcf61b7 (the recency-full arm-2 board) and from live 82fcd8bb.
P-N4. Day-0 86/86 print exactly (draft rows carry no seasons -> weighting-invariant day-0).
P-N5. V3 census at RAW = 0 descending violations on all 804 rows (the exact-monotone constraint is a
      property of the construction, not of the sample weights).
P-N6. The q97m interior-optimum check may land differently than lr1.5/it1600 — whatever it selects is
      reported with its grid, never overridden.
NON-GOALS: no repo write, no live pin touched, no landing — this is the measurement the packet presents.
