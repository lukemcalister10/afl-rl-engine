step 1: seat start, progress file created
step 2: read stage6 MEMO.md + teach_g6.py (kernel conventions, D1 estimand, eff-n>=35, Z conservation, kappa L-SMOOTH)
step 3: reproduced shipped two-axis teach exactly (g6_table md5 61450f0b, Z=0.772923, kappa=0.912673) from s6_rows.json
step 4: first pass 3-axis teach done. control reproduces shipped exactly (Wmax 0.4193 -> 1.024847). 3-axis variants A/B/C all WORSE (0.2557/0.3895/0.3129), all newly bound by the picks 41-64 declared taper.
step 5: pass2 done - thin-cell CIs (median 90pct CI width 3.39xD1 for 3-axis vs 2.3xD1 for 2-axis), controls E/F, seam proxy, fallers, taper sensitivity
step 6: pass3+4 done - 6 three-axis specs + 2 controls, seam proxy, tail-vs-typical, taught-vs-measured at the registered cells. VERDICT: no material gain.
step 7: report written and returned. no repo writes, no posts. scratch: probe3ax*.py / probe3ax*_out.txt
