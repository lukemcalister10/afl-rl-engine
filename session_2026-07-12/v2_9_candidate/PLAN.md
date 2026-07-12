# PLAN — THE v2.9 COMBINED CANDIDATE (integration) · 2026-07-12 · branch `claude/v2-9-candidate-integration-vtsnhr`

MODE auto; this PLAN is the first committed artifact (directive: "first committed artifact = the
PLAN — lever order + assert order"). HALT-not-warn throughout. One combined candidate, one refit,
one cohort re-measure, one gate suite, per-lever attribution (G-ATTR). **Candidate only — nothing
here tags, bakes, or merges; the full Tier-1 ladder sits above this job.**

## BASE VERIFICATION (done, first action)
- Full-URL ls-remote `github.com/lukemcalister10/afl-rl-engine`:
  - `main = f93de227f63f9265d66f21206f5d11118ed11baa` ✓ (== directive assertion)
  - `refs/tags/v2.8 = 9bd0cfdbf9faff83fee21c843fac2ebb5baa25c9` ✓ (real tag, unmoved)
- Boot store `b0c39d78` == pinned (Guard 5 PASS on entry and on every run_panel) ✓
- Engine `7a07e369`, cm_400 `34faa865`, register `652d83e8` — bootstrap pins asserted ✓
- Baseline panel reproduces **PASS 10/10** (Daicos 8050 · Bont 3721 · Gawn 2538 …) ✓
- Store identical in repo `engine/rl_after/rl_model_data.json` and workspace (`b0c39d78`) ✓

## THE FEED — what actually exists (surveyed at the pinned SHAs; STOP-on-missing honoured)
The three source branches are **research-only session folders; none wires anything into the
engine.** This reframes the levers from "flip a switch" to "build + verify", so the PLAN states
per lever what is a ready input vs. what this build must author.

| input | at | status |
|---|---|---|
| Derived PVC curve `pinned_d15_H10` (picks 1–90) | icbhpu `3c1d610f` `…/pvc_rederivation/out/derived_curve.{json,csv}` | **numbers exist**; still isotonic-stepped (plateaus 6-9=1739, 15-18=1219, 32-40=748, 58-86=343). The **L1 smoothing pass is NOT written** — this build authors it. |
| Option-b sim (L1 oracle) | same `…/out/sim_option_b.json` | parity 805/805 · 26 movers (RUC 24/MID 1/KEY_DEF 1) · board +0.205% · anchors byte-identical. **Ran on the UNsmoothed curve** → shape oracle, not exact values. |
| PICKEQ pedestal supplement | same `…/out/addendum_pickeq.json` | MSD 60→60 (no move); SSP 91.5→**eq 51** (n=24, thin); IRE/UNR/PDA/PDN/PDS all KMAX-capped → no move. SSP move is **L6 = HELD.** |
| Age s(age) curve | l7hinr `394cd16` `…/age_persistence/out/curve.json` (`s_clip`) | up-side breakout-persistence table 20:.915 21:.861 22:.789 25:.490 27:.266 29:.027 30+:0. **No engine code, no env-var** — this build authors both. Register hint "0.86@22" anchors to age **21** (22=.789). |
| MSD-pool refit (L4 mechanism + oracle) | #63 `a3eea59` `…/ruling_pack_v29/scripts/msd_pool_ripple_pass.py` + `out/msd_pool_ripple.json` | **runnable read-only pass** — patches the pool filter, re-execs, asserts parity, reports. Oracle: pool ND 1255/RD 640/MSD 29 · 668 movers · 47 ≥5% · board +0.18% · emmett 1177→826 (−29.82%) · mcandrew +1.25%. |
| SPEC_1–4 measurements | #64 `f62aea7` `…/v29_measurement_specs/SPEC_*.md` | **prose design only — no runnable code, no outputs.** This build authors the report-only scripts. |
| G-Y0 seam identity | #63 `…/out/identity_illustration.json` | numbers committed; the generator is **not** re-runnable (its inputs `derived_curve.csv`/`harvest.json` aren't on #63). Rebuild against the adopted curve. ADVISORY this chapter. |

## THE MECHANISM MAP (jargon → code; every lever traced to file·line·gate)
- **L1 PVC(b)+smoothing** — `MA.PVC` pick/trade-currency dict. `_merged_recover.py:990` `_W4PVC=RL_PVCFIT!=0`;
  `:995-998` loads `pvc_fit_candidate.json['curve']` into `MA.PVC`. `:991-992` snapshots `_PVC0` (frozen
  v3.4) and rebinds `draftval` to `_PVC0` so **player pricing never reads the fit** (cuts fit→board→fit).
  Adoption = regenerate `pvc_fit_candidate.json` from the derived curve **after** the smoothing pass;
  pin pick-1 = `RL_PICK1`=3000. Board write needs `RL_ALLOW_PVCFIT_BOARD=1` (R3 bake-guard,
  `rl_export.py:36`) — candidate is explicitly non-bakeable. Young-RUC movers arise because the RUC
  cap headroom reads `MA.PVC`; anchors are byte-identical (survey + oracle).
- **L2 DIAL 14** — discount is `LENS['bal']` at `rl_model.py:301` (`d=LENS[lens]`, `…*21/((1+d)**k)`
  at `:340/:341/:353`; board ships `value(p,'bal')`). DIAL 14 = `LENS['bal'] 0.15→0.14`.
  **ASSERT ORDER: prove by code-reading that the young-ruck prior-cap artifact is gone via L1(b)
  BEFORE moving the dial** (the emmett −20/−22% at ≤13% is the cap misbehaving; synthesis binds the
  artifact to rates ≥14). At 14% the artifact is not triggered, but the directive requires the proof,
  not the assumption — discharge it or halt L2.
- **L3 AGE(A), GATED** — `_coreM1` up-branch `_merged_recover.py:225`: `S_M1*(Lc-Lo)` (flat 0.46,
  `:208`). Adoption = insert the `s_clip` table + rewire to `clip(s_age(age),0,1)*(Lc-Lo)`; add a
  kill-switch (`RL_AGE`, new). **GATE = the walk-forward G-COHORT re-measure, run ONCE on the fully
  combined candidate** (never per-lever); a breach HALTS the candidate. Watch butters (−1.0%, the
  narrowest G-PEAK margin; tolerance 2%).
- **L4 POOL(a)+membership-stability** — pool filter `_merged_recover.py:17`:
  `if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')): continue`. Exclusion = add MSD via a
  **facts-based rule** (entry-pathway class MSD ∧ debut window) + an **edit tripwire** (any row whose
  training membership would change from a data edit HALTS). Load-bearing leg to NAME: the trio
  (mcandrew p12 / perez p35+_ft) are kept out **only by the debut≤2021 window** (ssp_filter_note) —
  a DOB/window edit could silently re-admit them → the tripwire guards exactly that. Labels stay
  modeling inputs everywhere else.
- **L5 TRIO** — `PRESENT_ID_OVERRIDES` `rl_model.py:806` is **already live and consumed** (`:812-814`):
  perez/mcandrew/keane → SSP, `_eff=92`, but `pick` and `_pickless=False` **retained** (pedigree half
  applied, pick-capital half not). Post-L4 the MSD→SSP relabel is pool-neutral for mcandrew (MSD out
  either way); residual ≈ perez ~7 rows. **This is a state to reconcile, not a from-scratch switch —
  see OPEN GATES.**
- **L6 SSP — HELD.** Do NOT move the 92 pedestal. Run SPEC_4 scarcity read-only, STOP at the SSP
  decision point, return the measurement for the owner's word (ruled (ii); scarcity-empty ⇒ ~51 on
  his confirmation only).

## LEVER ORDER + ASSERT ORDER
1. **L1** first (foundation; L2 asserts against it; the seam table needs the adopted curve).
   - L1a adopt derived levels → L1b smoothing pass (monotone preserved; deviation table committed)
     → L1c build engine `pvc_fit_candidate.json` (pin 3000) → **ASSERT** anchors byte-identical +
     parity 805/805 + G-MONO + young-RUC mover set ≈ oracle.
   - PICKEQ pedestals: MSD 60→60 verified no-move; SSP HELD (L6). No pedestal ships.
2. **L4** (the refit) — add MSD exclusion + facts-based rule + edit tripwire. **ASSERT** trained pool
   → ND 1255/RD 640/MSD 29; parity off the mover set; emmett ≈826; anchors move as oracle
   (bont −0.35%, gawn +0.67%). L5 residual attributed here (pool-neutral for mcandrew).
3. **L2** — only after discharging the prior-cap-gone proof. `LENS['bal']→0.14`. Attribute.
4. **L3** — insert s(age) + kill-switch. Then the **ONE** walk-forward G-COHORT re-measure on the
   fully-combined L1+L4+L2+L3 world. Breach → halt candidate (raise young side; never cut survivors;
   never bend the derived curve).
5. **Seam table (D2/D3)** — build the G-Y0 identity table against the adopted curve; **ADVISORY**
   (report, never gate this chapter).
6. **Measurements** SPEC_1–4 read-only on the post-L4 world → reports + PROPOSED mechanism
   corrections for owner ruling. **No unruled fix ships.**
7. **Export bundle** rides the same candidate (vPrev/vRaw/levers fields; barker/thredgold lti_reg
   consumer-wiring fix; +1/+2 phantom pick-asset lens entries off the adopted curve at dial 14;
   lens-total quasi-conservation DIAGNOSTIC).

## THE GATE SUITE (one suite, on the combined candidate)
Five data guards + panel + B3 seal + B4 parity (non-movers) + B1 peak + G-MONO + G-ATTR + the
walk-forward G-COHORT re-measure (L3 gate). Anchors asserted from acceptance v1.7; **expected reds
EXACTLY {A2, A3, A12}** ([DC], carried). louis-emmett: full per-lever attribution (the three-probe
corner: cap-removal via L1/L2 · pool-isolation via L4); the owner's football-nonsense review
trigger is ARMED on the pool refit.

## G-ATTR METHOD (per-lever separability, BINDING)
Boards at: base(b0c39d78) → +L1 → +L1+L4 → +L1+L4+L2 → +L1+L4+L2+L3(full). Each lever's delta =
diff of consecutive boards, per row; emmett + the anchor set carried explicitly. All levers OFF must
reproduce the base board byte-exact (kill-switch honesty: `RL_PVCFIT=0 RL_AGE=0`, `LENS['bal']=0.15`,
MSD-exclusion off).

## HONEST PARTITION — what this session executes vs. what it reports/gates
- **EXECUTED + VERIFIED this session:** L1 (smoothing pass + deviation table + engine artifact +
  board verified against the option-b oracle: anchors byte-identical, parity, G-MONO). Read-only
  reproduction of the L4 refit oracle + characterisation of the trio/pool state.
- **STAGED, needs its gate/proof before it ships in the candidate:** L2 (prior-cap-gone proof), L3
  (new engine code + the one cohort re-measure), L4 permanent (the refit + tripwire).
- **OWNER-WORD GATES (return, do not decide):** L6 SSP 92→~51 · the L3 cohort-gate outcome · every
  SPEC_1–4 PROPOSED mechanism correction · the L5 trio full-switch reconciliation.

## OPEN GATES / DECISIONS FOR THE LADDER (surfaced, not buried)
1. **L5 trio override is live but half-applied** — pedigree switched (SSP/`_eff`=92), pick capital
   retained (`pick`=35/12, `_pickless`=False); perez ev=14. The register calls the trio "deferred /
   no engine override"; the #63 ripple note confirms the SSP-typed-with-pick state is current and
   concrete. Needs an explicit reconciliation ruling: complete the switch (pickless) vs. keep the
   half-state as the membership-stability facts-based row. Attribution ≈ perez ~7 rows either way.
2. **`pvc_fit_candidate.json` on main is the OLD discredited year-1 W4 fit**, not the re-derivation —
   `RL_PVCFIT=1` today would load the wrong curve. L1c replaces it (stamped candidate).
3. **SPEC scripts do not exist** (#64 is prose) — the measurements are authored here, report-only.

## FENCE
IN: the store/engine levers above + the seam table + the export + derived re-pins. OUT: docs-pack
authoring · UI code · the dead-code strip + flex (WAVE 2, supervisor's word only, after green).
No force-push · no tag · no main merge · no bake (owner-only, up the ladder).
