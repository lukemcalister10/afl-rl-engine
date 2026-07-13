# REFIT WIRING — PLAN OF RECORD (final v2.9 continuation, directive item 3.1)

**Seat:** refit-certification (final build continuation). **Branch of record:** `claude/v2-9-candidate-integration-kq4dae`
(owner-authorized 2026-07-13 to continue ON it; built on 5cb7f80; never rebased; **PR #67 is the candidate of record**).
**Candidate ONLY** — no tag, no main merge, no bake; owner word required up the ladder.

This is the first commit of the final continuation (per the directive: *"first commit = the wiring plan-of-record"*). It
records the deterministic on-disk plan BEFORE any engine edit. The patches are pre-validated
(`session_2026-07-13/v2_9_continuation/scripts/levers.py` reproduces each inherited sim to the dollar —
`out/lever_validation.md`); wiring is a mechanical apply-gate-repin + gate-suite certification, NOT new derivation.

## BASE + PIN (asserted this seat, first act)
- `main` == `cd1cb08` ✓ · tag `v2.8` == `9bd0cfd` ✓ · branch `kq4dae` == `5cb7f80` EXACT ✓
- boot store `b0c39d78` == pinned ✓ (Guard 5 PASS on bootstrap + run_panel) · engine `_merged_recover.py` md5 `7a07e369` ✓
- cm_400 `34faa865` ✓ · register (LTI) `652d83e8` ✓ · **base panel reproduces 10/10** ✓ (clean starting point)
- Law read: `docs/OPEN_ITEMS_REGISTER.md` v35 items 17–19 (the ruling card, the mid-chapter findings, the combined-gate PASS);
  the 5 `L*_FINDINGS.md`; `REFIT_WIRING_SPEC.md`; the answer-key `out/` (lever_validation, gattr, gate_base/combined, l7).

## RUNTIME LAYOUT (how the wiring lands)
`bootstrap.sh` copies repo `engine/rl_after/` → workspace `/home/claude/rl_workspace/rl_after/` (the engine cwd);
`run_panel.sh` runs Guard 5, `cd`s to the workspace, runs `_merged_recover.py`, checks the 10 named panel. **I edit the
repo `engine/rl_after/*.py` + add the stamped curve artifact, re-bootstrap, regenerate, re-pin.** Engine JSON artifacts load
by bare filename (cwd == workspace rl_after), so the L1 curve becomes `engine/rl_after/pvc_curve_L1b.json`.

## THE LEVERS ON DISK — each behind a kill-switch (G-ATTR honesty; convention = existing `RL_*` flags, default ON, all-off ⇒ base byte-exact)

### L1 — `_PVC0` ev-channel swap + V0/RUC rebuild  ·  gate `RL_PVCADOPT` (default 1)
`_merged_recover.py:992` — after the `draftval` rebind to `_PVC0`, inject the gated block (levers.py `L1_INJECT`, wrapped
in `if os.environ.get('RL_PVCADOPT','1')!='0':`): load the L1b smoothed derived curve (pin 3000), `_PVC0.clear()/update()`,
clear `_V0C/_V0U/_V0GUARD` + `_RUCCEIL['grid']`, `_build_v0_guard()`, `_V0CURVE.clear()`, `_build_v0_curve()`, `MA._pe_clear()`.
Curve source → **stamped engine artifact** `engine/rl_after/pvc_curve_L1b.json` (`{"curve":{pk:val}, "pin":3000, "source":…}`,
values byte-identical to `pvc_curve_smoothed.json`; loaded via `['curve']`). `RL_PVCADOPT=0` ⇒ block skipped ⇒ base byte-exact.
**Target:** board sum +1296 (+0.179%), anchors byte-identical, knobel 402→505, 24–25 movers (all RUC + 1 KEY_DEF).

### L4 — MSD training-pool exclusion + edit tripwire  ·  gate `RL_MSD_POOL_EXCL` (default 1)
`_merged_recover.py:16` pool filter → append `or (_L4_MSD and p.get('type')=='MSD')` (define `_L4_MSD` before the pool loop).
`_L4_MSD=0` ⇒ base. **Edit tripwire** (new, after the pool loop): the re-entry trio (Perez/McAndrew/Keane, debut∈{2026,2025,2023})
are kept OUT of the training pool by the **debut>2021 window, NOT entry-type**; any store edit that flips a named row's pool
membership HALTS for a ruling (the silent-re-admit hole, L4_AND_TRIO_FINDINGS). **Target:** emmett 1178→826 (−29.9%, the armed
football-nonsense trigger), bont 3708, gawn 2556; MSD 29→0; pool ND1255/RD640.

### L2 — dial 14  ·  gate `RL_DIAL14` (default 1)
`rl_model.py:301` `LENS['bal']` 0.15→`(0.14 if RL_DIAL14 else 0.15)` (add `import os` to rl_model.py). `RL_DIAL14=0` ⇒ 0.15 ⇒ base.
**Target:** bont 3676, gawn 2501 (== SWEEP 14% col).

### L3 — s(age)  ·  gate `RL_AGE` (default 1)
`_merged_recover.py:208` inject `_S_AGE` breakout-persistence table + `_L3_AGE` flag after the `S_M1=0.46` anchor;
`:225` up-branch `S_M1*(Lc-Lo)` → `(_S_AGE(cp._age_asof(p,Y)) if _L3_AGE else S_M1)*(Lc-Lo)`. `RL_AGE=0` ⇒ flat 0.46 ⇒ base.
**Target:** butters 6060→5997 single-lever (−1.04%, inside G-PEAK 2%); 5986 combined.

### L5 — trio pickless (completion)  ·  gate `RL_L5_PICKLESS` (default 1)
`rl_model.py:806` override loop — for SSP overrides set `pick=None`, `_pickless=True` (Perez/McAndrew move; Keane already so).
The `_eff=92` SSP pedestal is **NOT** touched (L6 STOP). Cohort-neutral (trio are SSP, not ND/RD gate members). `RL_L5_PICKLESS=0`
⇒ base. **Target:** residual ≈ perez ~7 rows; mcandrew pool-neutral post-L4.

### L7 — numéraire ÷1.0524 (LAST)  ·  register v30/v35 item 17 THE NUMÉRAIRE LAW
`rl_export.py (g)` numéraire assert is **already staged** (pick-1 ≠ 3000 ⇒ HALT once in the numéraire world). Wire the actual
re-base as `RL_NUMERAIRE=1` export mode: pick factor→1.0 (picks = 3000-anchored adopted curve) + player values ÷1.0524 uniform
+ constants re-quote; ASSERT `adopted_curve[1]==3000`, display pick-1 3157→3000, **ALL** anchor-pair ratios preserved (pre/post),
no strict inversion. `BAKE_CHECKLIST §3` numéraire ship-gate + the CONSTRAINTS v1.8 constants re-quote (A-BONT 3084 · G-CONVEX
180140/178224/107773 · SCALE 6651). Per-lever attribution reports quoted in numéraire units. **L7 is ratio-invariant / does not
move ev() — the panel re-pin is on the pre-L7 combined ev; L7 is the export/board unit.**

## PINS THAT MOVE IN-COMMIT (coordinated re-pin — do NOT split; one atomic refit commit)
- **engine md5** `_merged_recover.py` 7a07e369 → new (levers on disk) — recompute at wiring, update every pin that quotes it.
- **panel**: regenerate with levers default-ON → read the 10 named → update `run_panel.sh` PANEL + `PANEL_EXPECTED.txt`.
  **CLAIM-ACCURACY (register v33/v35 hygiene):** the committed panel MUST equal the regenerated board — no claimed pins.
- **boot-pin** (`boot_guard.py` / `data/expected_boot.json`): store `b0c39d78` UNCHANGED (levers are engine, not store; L5 is
  a runtime override, not a store edit) — re-pin only the board/engine stamps that changed.
- **B3 book re-seal** + **config** (`config_manifest` hash only if `model_config` changes; dial is source not config) +
  **collision sentry** re-assert.

## CERTIFICATION (gate suite on the wired refit — required before the PR calls it done)
Five data guards + Guard 5 + panel (re-pinned) + B1 (the combined cohort gate, PASS reproduced 126.8/125.2/116.1) + B3 seal +
B4 parity (declared movers only) + B1 peak + G-MONO + **G-ATTR** (base→+L1→+L1+L4→+L1+L4+L2→+L1+L4+L2+L3; all-off == base
byte-exact). Acceptance v1.7; expected reds EXACTLY {A2, A3, A12}. HALT-not-warn. louis-emmett named in the G-ATTR tables.

## DEVIATIONS FROM `levers.py` (declared)
levers.py applies the patches **unconditionally** (it built sim variants by string-patching). The permanent wiring wraps each in
its **env kill-switch** (default ON), so the SAME engine reproduces base (all-off, byte-exact) and each cumulative G-ATTR variant.
When every gate is ON the behaviour is byte-identical to the validated sims (verified at certification). L5/L7 are added on top
(levers.py does not source-patch them — cohort-neutral / ratio-invariant by construction).

## AFTER THE REFIT (this seat, budget-permitting; checkpoint-and-say-so per the directive)
item 3 SPEC_1–4 + seam table + the **L6 STOP** (return the ruck-scarcity measurement for the owner's SSP word; the 92 pedestal
does not move without it) · item 4 export bundle + UI re-extract. Findings = reports + PROPOSED corrections; **nothing unruled ships.**
Ladder above this return: seat-4 prescreen → cold audit → owner board+book vs SEALED reads → bake word → tag v2.9.
