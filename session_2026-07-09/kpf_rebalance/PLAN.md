# PLAN — KPF REBALANCE (pre-bake, on the L1c candidate) · 2026-07-09 · branch `claude/fable-wave-4-integration-w4rfpb` · PR #46

## Fence (asserted)
- Branch checked out by NAME; head asserted `cb8985aff369149a0c23876e81a668ed22e8c72d` before this (first) commit.
- Guard 5 PASS on entry (store e1b4d8bf == pinned; workspace re-seeded from THIS checkout via bootstrap.sh — the
  session-start hook had seeded from the other branch's checkout; re-ran bootstrap on the fence branch, engine
  fbefdc2b == pinned).
- Store NEVER edited (md5 asserted entry + exit). Engine-head pin (data/expected_boot.json) bumps with the final commit.
- FEED gap, declared: DECISIONS_v84 / CONSTRAINTS_v1.5 / HANDOVER_rev125 are not in this checkout (docs/ stops at
  v75/rev115); building from the directive + acceptance_v1.5.json + the committed session artifacts (L1c RETURN,
  book_ratio.py conforming script, W_TABLE). The acceptance JSON carries the constraint content of CONSTRAINTS_v1.5.

## Effort / time
High · mode auto · band 2–4h CONFIRMED (walk-forward matrix builds ~30–60 min each are on the critical path; two
matrix runs budgeted — the rebuilt book + the single allowed re-measure).

## The three in-scope levers (current code coordinates, engine `_merged_recover.py` @ fbefdc2b)
1. **KPFFIX compression** (`ev()` :775–786): established KEY_FWD (nqual≥4 & age≥24) with price above the engine's
   own price of demonstrated level (eP, band pinned at `_lvl_eff`): `e' = eP + 0.55·(e−eP)` — the retention share
   0.55 (`RL_W4_KPFSH`) is FLAT: a residual backed by three high-games seasons (Georgiades) is compressed at the
   same rate as pure band looseness. That flat share is the dishonesty the owner's read caught.
2. **KPF above-replacement reward shape** (`_w4_ctx`/`_w4_W` :331/:345): the concave regime — credit ramp
   `gm = clip((m−10)/20, 0, 1)` (m = demonstrated level above REPL) SATURATES at m=30, and the KPF reward
   multiplier `RL_W4_KPFUP=1.6` is flat. Every top-tier scorer above m≈30 earns exactly what a m=30 player earns:
   elites are structurally under-rewarded. (posval/S_SH and the MID-facing constants are FROZEN — the reshape is
   KEY_FWD-scoped inside the existing `_W4KPF and pos=='KEY_FWD'` gate, so A-BONT/A-GAWN ride untouched levers.)
3. **Young credit KEY_FWD cells** (`_ycred_mult` :455): the L1c evidence-conditioned re-rating credit reads
   per-position rows of ycred_table.json. KEY_FWD cell intensity gets a SLIGHT position-scoped scale.

## Mechanisms (never per-player)
- **T1 — demonstration-keyed retention.** Replace the flat SH with SH(m): retention of the above-demonstrated
  residual rises with the DEMONSTRATED margin above replacement — the same conditioning variable as the #45 shed /
  V7 / W4 legs (never age-keyed, never name-keyed). Shape derived from store history (realized forward delivery of
  established-KPF seasons vs their then-demonstrated margin, walk-forward-safe: outcomes ≤2023 only); level anchored
  at SH(0)=0.55 (zero-margin residual = pure band looseness — the settled T1-shape keeps its bite) rising to a
  measured ceiling at high margin. Continuous clip-ramp, no cliffs. Dial `RL_W4_KPFSH` retired into
  `RL_W4_KPFSH_LO/HI` + ramp knots; `RL_KPFFIX=0` stays byte-exact v2.5.
- **T2 — top-tier segment of the concave regime.** KEY_FWD-scoped: `kpfup(m) = 1.6 + TOP·clip((m−20)/15, 0, 1)`
  (slight TOP, saturating at m=35 — the regime stays concave, the plateau moves up for genuine top-tier scorers).
  Flows into eP too (same context), so T1's compress can never eat the T2 reward. The floor path (`_prod_floor_w4`)
  carries the same W(k) → the credit lands on the certain present, not the speculative tail. Named set must move up
  visibly; magnitudes owner-on-sight. A-DARCY: expected to ride T2 (proven-branch) + retain his protected-young
  exemption from T1; his three-way attribution (young ceiling / kpf_speculative / availability) reported per A-DARCY.
- **T3 — slight KEY_FWD trim of the young credit.** Position-scoped intensity scale inside `_ycred_mult`:
  `R → YKPF·R` for KEY_FWD only, new dial `RL_YCRED_KPF` default ≈0.90–0.95 ("slight" — final value set with the
  guard geometry, below). F-YOUNG honored: no wipe; these are year-1 denominator members — the denominator cost of
  every point taken is measured and reported (Δy1 figure, Δy2 figure, Δratio decomposition).
- Levers FROZEN and untouched: FWDRECAL constants (W4_CRED/W4_FADE/gm ramp for non-KPF) · W4_RUC · FORMDECL ·
  V7FORM · OVPX · young credit outside KEY_FWD · pick curve · RL_PVCFIT (off).

## Guard geometry (Task 4, measured before building)
Current conforming ratios (ratio_l1c_w09_RULED): y4 128.55 / y5 126.86 / y6 118.83, den=y1 63,821.9 — margin 1.45pt.
ALL THREE tasks push ratios UP (T1/T2 raise y5–y6 numerators at the proven tail; T3 cuts the y1 denominator).
Mitigation by construction: the T1/T2 gates (nqual≥4, and age≥24 for T1) sit mostly ABOVE career-years 4–6
(draft-age ≈18 ⇒ age 21–24 in-window), so the board-visible softening/reward lands mainly outside the tested years.
Budget: T3 at −0.5% y1 costs ≈+0.65pt on y4; T1+T2 numerator effect in-window must stay ≤ ~0.5%. If the rebuilt book
breaches: reduce T2 TOP and/or T3 trim ONCE within "slight", re-measure ONCE; if it still breaches — STOP, commit,
report the size-vs-guard trade table, owner rules. The guard, its script (book_ratio.py conforming construction) and
its bounds are never altered.

## Measurement / suite plan
- Baselines: one-engine-load-per-process board dumps (ON / RL_KPFFIX=0 / RL_YOUNG=0) — reproduce the directive's
  measured takes (McDonald −292/−27.3% …) before touching anything; verify PROVEN_N/m values of the named sets.
- Task 5 acceptance table (committed): six top-tier names · softened-take set · speculative set (Croft, Sims,
  Whitlock ×2 — both matt- and jack-whitlock exist; reported separately, flagged for the owner · Armstrong, Reid,
  Faull, Read, Walter, Dear, Marsh, Curtin) · GEORGIADES vs WHITLOCK ordering · A-BONT/A-GAWN/A-DUUR (>0.5% move =
  finding) · net KPF-position and whole-board movement.
- Task 6 suite: frozen gates (ship_gates_check.py) + panel 10/10 + all-switches-off byte-exact v2.5 + G-ATTR LOO
  with the reshaped KPFFIX and YOUNG separable (RL_KPFFIX=0 / RL_YOUNG=0 single-switch toggles) + smoothness (m-axis
  sweep across the new SH(m)/kpfup(m) ramps: no new cliffs; the declared evidence-axis dip unchanged). OQ-B: three
  narrowest margins reported.
- Task 7 key check: DONE at survey — store key for Jeremy Cameron is **`jeremy-cameron`** (ND, pick 13, active;
  verified against the store, not guessed). A **`charlie-cameron`** row EXISTS and is a DIFFERENT player (RD, pick 6,
  active — the Brisbane small forward); the A-CAM anchor logic must key `jeremy-cameron` per the owner's
  confirmation; the registry's charlie-cameron key is the documented drift, correction pending. Nothing in this
  build's mechanisms keys on either row (position-scoped only — charlie-cameron is not a KEY_FWD; verified in the
  acceptance table).

## Commit cadence
PLAN (this) → T1–T3 mechanism + board acceptance table → conforming book + G-COHORT verdict → suite + RETURN
(+ engine pin bump). Each script asserts Guard 5 on entry.
