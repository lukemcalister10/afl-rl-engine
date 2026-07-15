# RETURN — Form-Conditioned Aging (Tier 3, READ-ONLY, MEASUREMENT ONLY)

Base `9be07b8e` STRICT · Guard 5 store `b1fd0bce` PASS · engine_head `fc7045d6` · board `790136a3`.
Auto mode: PLAN committed first (commit `6e2defc`), before any estimate. Fence clean (writes only under
`session_2026-07-15/form_conditioned_aging/`). No store/engine/config/board/gate/doc write; no wiring.

FINDING — conditioning on flat-or-rising form to date does NOT buy slower decline at 30+:
- 30+ flat/rising (n=133): next-season material-decline hazard H_lower=0.54 / H_upper=0.63; mean ΔLc=−4.1.
  Age cohort unconditioned (n=392): H_lower=0.51 / H_upper=0.65; ΔLc=−3.1. Conditioned ≈ cohort (no slowdown).
- Robust: across 11 definition variants, H_lower(cond)−H_lower(unc) is positive in ALL (+0.004…+0.068).
- Implied runway: flat/rising 30-yo ~2 seasons to first material decline; P(no decline 30→33) ≈ 0.11.
- Survivorship handled by the H_lower/H_upper bracket (32 genuine 30+ exits, 5 still-elite); result holds
  either bound. Mean-reversion handled by using the validated recency level Lc (not a single-season spike).
- Engine: the `_S_AGE` 30+ zero is re-validated CONDITIONALLY (age-29 tail positive, 30+ ≈ nil); `_agemult`
  decline path (0.73@30) is consistent with observed ΔLc. No evidence the age path is too harsh. NO wiring.
- 33–36 thin (n≈12) → pooled + declared; smoothed over age (Gaussian bw=1.5), n reported at every age.

WORKED EXAMPLES (all right-censored — 2026 is a partial season, so-far only): Gawn (35) and Heeney (30) are
currently BEATING their class-conditional expectation in 2026; Bont (31), English (29), Dale (29) near/below.
The persister tail is real but does not move the class average; no individual verdict follows from the class.

PRIOR ART `claude/form-conditioned-aging-decline-5hi0xe`: the origin of the DOWN-arm `_agemult2`/`_fbump`
decliner-shed already in the base engine (session_2026-07-06 / "PR #45"). Construction SOUND (NW 2-D,
eff-n≥35, isotonic-monotone, up-only, washout-inclusive r, kill-switch verified) but answers a DIFFERENT
question (already-declining population's remaining output). NOT reused — everything re-derived independently.

ARTIFACTS (committed): PLAN.md · FINDING.md · OWNER_READ.md · measure.py · plots.py ·
hazard_by_age.csv · sensitivity.csv · worked_examples.csv · summary.json ·
fig_hazard_by_age.png · fig_worked_examples.png · base_store_rl_model_data.json (b1fd0bce byte-copy).

Branch: `claude/form-conditioned-aging-analysis-mjhiul`
Head SHA: <FILL_HEAD>
PR: <FILL_PR>
Time: within the 1.5–3 h band. Measurement only — the owner rules on the return.
