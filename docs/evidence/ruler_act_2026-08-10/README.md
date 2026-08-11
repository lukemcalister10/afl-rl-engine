# THE RULER ACT INSTRUMENTS — the original scripts, landed 2026-08-10

These are the ORIGINAL instruments of the year-4 ruler act (the tilt map, the rate-based
re-look, the 2x2 availability x horizon ledger, the tail measurement, the age-axis re-cut) —
the scripts that produced every filed F-verdict and the final four-instrument tilt ledger
(#334 comments 5236277043 · 5236425904 · 5236597585 · 5236898284). Landed from the session
scratchpad after the composition build's first-gate halt found them absent from the tree
(PR #399 halt report: the reconstruction attempt could not reproduce the horizon axis; the
originals were never lost — they lived in the seat's scratchpad).

WHAT GOVERNS: the F8 evidence bar reads at PLAYER UNIT from the 2026-08-10 sitting forward.
These scripts pre-date that ruling — any re-run for the ITEM I restatement applies the
player-unit bar on top.

PATH CONVENTION: the scripts reference the session scratchpad root (SP = /tmp/.../scratchpad)
and a repo clone at SP/repoB checked out to the evidence branch. The per-entrant matrices they
read are NOT on main — they live on origin branch `landing/334-stage-b` (tip 3820303) at
  docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json
  docs/evidence/act_334B_2026-08-07/stage5/noarb/per_entrant_338_stage5.json
To re-run: clone/fetch that branch, set SP (or edit the two path constants), run r15_align.py
FIRST — it is the alignment gate ("if this does not print PASS, nothing else in the tilt map
may be read"). Re-verified PASS on 2026-08-10 before this landing (stage4a1 and stage5 both:
n=414 F1=1.1363, KPD 0.6680, RUCK 1.6959; Hurley spot exact).

KEY FILES: r15_align.py (the gate) · r10_tilt.py + r13_map.py (the tilt map) · r20_rate.py +
r22_level.py (the rate-based re-look) · r24_horizon.py + r25_2x2.py (the 2x2 ledger — the
four-instrument basis) · r26_tail.py (the tail beyond year 11) · r30/r34 (the owner's per-age
tables; r30's proj-boundary table is VOID — superseded by r34's true-weight table) ·
r36_dob.py + r37_ageaxis.py (the post-DOB age re-cut) · r16_final.py/.json (the tilt factors)
· RULER_PROGRESS.md (the act's own step log).

The ITEM B pool-factor instrument and the ruck/sitter/markup instruments are separate acts;
their scripts remain in the scratchpad and land the same way if the build needs them re-run.
