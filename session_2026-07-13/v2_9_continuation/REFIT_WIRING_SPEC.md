# REFIT WIRING SPEC — the permanent v2.9 refit (directive item 3) · authorized by the gate PASS

The one combined gate PASSED (COMBINED_GATE.md: y4=126.8/125.2/116.1 ≤130), so the permanent refit is
authorized. This spec is the deterministic on-disk change: every lever's exact source edit is already
VALIDATED (scripts/levers.py reproduces each inherited sim to the dollar — out/lever_validation.md), so
wiring is a mechanical apply-gate-repin, NOT new derivation. ONE refit, ONE engine-md5 move, pins move
IN-COMMIT. L7 LAST. Candidate ONLY (non-bakeable; no tag/main/bake).

## The levers, on disk (repo engine/rl_after/), each behind a kill-switch (G-ATTR honesty)
1. **L1 — `_PVC0` ev-channel swap + V0/RUC rebuild** (gated `RL_PVCADOPT`, default 1 in candidate).
   After `_merged_recover.py:992` (draftval rebind to `_PVC0`), inject the validated block
   (`levers.py:L1_INJECT`): load the L1b smoothed derived curve (pin 3000), `_PVC0.clear/update`,
   clear `_V0C/_V0U/_V0GUARD` + `_RUCCEIL['grid']`, `_build_v0_guard()` + `_build_v0_curve()`,
   `MA._pe_clear()`. The smoothed curve moves into the engine tree (from
   session_2026-07-12/v2_9_candidate/out/pvc_curve_smoothed.json → a stamped engine artifact).
   `RL_PVCADOPT=0` ⇒ block skipped ⇒ base board byte-exact. Verified: board +0.179%, anchors
   byte-identical, knobel 402→505.
2. **L4 — MSD pool exclusion** (facts-based rule; default ON, kill-switch `RL_MSD_POOL_EXCL=0`).
   `_merged_recover.py` pool filter: add `or p.get('type')=='MSD'` (levers.py:L4_PATCH). Author the
   **edit tripwire**: any store edit that would flip a row's training-pool membership HALTS (the named
   load-bearing leg = the trio kept out by debut≤2021, NOT entry-type). Verified: emmett 826, pool
   ND1255/RD640, bont 3708, gawn 2556.
3. **L2 — dial 14** (`rl_model.py:301` LENS['bal'] 0.15→0.14; kill-switch = revert to 0.15). Verified:
   bont 3676, gawn 2501 (== SWEEP 14% col).
4. **L3 — s(age)** (gated `RL_AGE`, default 1). Inject `_S_AGE`+tables at `_merged_recover.py:208`
   (after S_M1) and rewire the up-branch at :225 (levers.py:L3_SAGE/L3_PATCH). `RL_AGE=0` ⇒ flat
   S_M1=0.46 ⇒ base. Verified: butters 6060→5997 (−1.04%, inside G-PEAK 2%).
5. **L5 — trio pickless.** `PRESENT_ID_OVERRIDES` (rl_model.py:806) already sets SSP+re-entry-year+
   _eff=92; complete it: perez/mcandrew `pick`=None, `_pickless`=True (keane already). Cohort-neutral
   (COMBINED_GATE.md); board effect ≈ perez ~7 rows.
6. **L7 — numéraire ÷1.0524, LAST** (register v30 THE NUMÉRAIRE LAW). Apply the uniform divide to the
   combined refit board (players+picks+anchors+absolute-SCAR constants); ASSERT adopted_curve[1]==3000,
   display pick-1 3157→3000, ALL ratios preserved (pre/post), no strict inversion. Wire the numéraire
   ASSERT live (rl_export.py (g) — already staged) + BAKE_CHECKLIST §3. Commit the CONSTRAINTS v1.8
   constants re-quote (A-BONT 3084 · G-CONVEX 180140/178224/107773 · SCALE 6651). Per-lever attribution
   reports in numéraire units.

## Pins that move IN-COMMIT (the coordinated re-pin — do NOT split)
- **engine head md5**: 7a07e369 → new (levers on disk). Combined-matrix engine md5 was 16e97c3a but the
  PERMANENT wiring (gated, artifacts stamped) will differ from the sim-patch md5 — recompute at wiring.
- **boot-pin (boot_guard / PANEL_EXPECTED)**: store b0c39d78 UNCHANGED (levers are engine, not store —
  except L5's override which is store/overrides). Re-pin the panel's 10 named to the REFIT board (regen
  → read the new values → update PANEL_EXPECTED.txt + run_panel PANEL). CLAIM-ACCURACY: the committed
  panel file MUST equal the regenerated board (register v33 hygiene note — a prior seat claimed 10/10
  while the committed panel read FAIL; do not repeat).
- **book re-seal (B3)** + **config** (config_manifest hash if model_config changes; dial is source not
  config, so config likely stable) + **collision sentry** re-assert.

## Certification (the gate suite, on the wired refit — required before the PR calls it done)
Five data guards + Guard 5 + panel (re-pinned) + B1 (the combined gate, PASS shown) + B3 seal + B4
parity (non-movers) + B1 peak + G-MONO + **G-ATTR** (base→+L1→+L1+L4→+L1+L4+L2→+L1+L4+L2+L3; all-off ==
base byte-exact — see out/gattr_*.json). Acceptance v1.7; expected reds EXACTLY {A2,A3,A12}. HALT-not-warn.

## Status
Patches VALIDATED (to the dollar) and the gate PASSES — wiring is mechanical + a coordinated re-pin +
the gate-suite certification. Staged for the refit commit; the board re-pin is the blast-radius step
that must be regenerated-and-verified (no claimed pins). louis-emmett's three-probe corner is on the
G-ATTR board (item below).
