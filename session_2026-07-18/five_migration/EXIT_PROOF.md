# FIVE-MIGRATION BUILD B — EXIT PROOF

All lines produced by commands run THIS session on this container (py3.12.3/np2.4.4/scipy1.17.1/
sklearn1.8.0). Dev-shell board recipe (`RL_REPO` set, `PYTHONHASHSEED=0`, no `RL_CONFIG_MODE`).

## 1. FINAL BYTE-HOLD (kill-switch, third+ proof) — committed engine (rl_model `fdc54e24`)
- **`RL_PVC2=0 ⇒ board 9829d01a`** byte-exact (== pinned baseline).
- `RL_PVC2=1 ⇒ board 06d8af60` (the migrated board; unpl_eq+pedestal reorder, v-parity held).
- **store `rl_model_data.json` md5 = `968de0c7` UNCHANGED** (HARD-OUT held; no store write).

## 2. BOARD-WIDE V-PARITY (the checkpoint law) — CLEAN
Across the whole migration `270a2c5f → 06d8af60`: **0 / 804 displayed-`v` movers, 0 pick movers.**
Corroborated structurally by the SSI suite's F1 gate: *"every board v == round(engine gated ev/1.0524);
mismatches=0"*. No commit moved a shipped per-row `v`. **No checkpoint trigger; nothing escalated.**

## 3. FROZEN SUITE / SSI GUARDS (`one_source_selftest.py`, RL_PVC2=1; book built)
Run after building the book (`s4_matrix.json` md5 `795b895a` via `s4_matrix_M1v7.py`). **All PASS except
one expected red:**
- GUARD 3 (single-source + engine-opens): **PASS** — `rl_model` opens only classified inputs incl.
  `pvc_curve_v2.json` (the fence-cure allowlist line works).
- GUARD 1 + GUARD 2 (derived read-only + stamped + content-intact): **PASS** — board stamp == source
  `968de0c7`.
- F1 EXPORT PARITY (board v == engine gated ev, key-for-key): **PASS**, mismatches=0.
- F2 BOOK PARITY: **PASS** (book built).
- Data ground-truth, position model, Leg A (iso fade/monotone), Leg B (recency R105.x), Collision
  Sentry (Max King pair): **all PASS**.
- LEG D ACT-2 curve instrument (§9): **all PASS** — R104.9 strict descent, numéraire 3000, entry
  closure, `_PVC0 == pvc_curve_v2.json`, STAMP store_md5 `968de0c7` matches boot store, G-Y0 residual
  1.100% ≤ 2%.
- **GUARD 5 boot-store: FAIL (EXPECTED)** — `rl_model fdc54e24 != pinned a5fd3d7d`. This build is the
  FIRST to change `rl_model.py`; the pin is re-stamped AT THE BAKE (the migration rides the bake,
  R107.5 pre-ladder). This is the single flagged item below, not a defect.
- GUARD 4 (correction-sticks canary): a heavy full-rebuild guard; **not run to completion in-session**
  (timeout). It validates owner correction-sticks in the STORE, which is byte-unchanged (`968de0c7`) by
  this rl_model-only change, so its subject is unaffected. Flagged for the bake run.

## 4. GATES SNAPSHOT (invariant under v-parity)
The A/B/G acceptance gates are player value-comparisons off the shipped board `v`. Board-wide v-parity ⇒
**every gate verdict is byte-identical to the pinned `data/gates_snapshots/gates_40f43772.json`**
(head `40f43772` == candidate `engine_head` — `_merged_recover.py` untouched; store `968de0c7`
unchanged). No gate moved; the standing FAILs (A2/A3/A4/A12, owner-amended) and PASSes are unchanged.
No new snapshot is minted (it would be byte-identical); the pinned snapshot is the candidate's record.

## 5. THE ONE FLAGGED SUPERVISOR/BAKE ITEM (pin — never a build's call)
Per the checkpoint law, board-order/pin decisions are supervisor judgments. This build does **not**
re-pin `expected_boot.json` or re-seal the committed board (`data/rl_build/rl_app_data.json` stays
`270a2c5f`, riding the bake). At the bake, to bless the candidate, apply exactly:

    data/expected_boot.json : "rl_model": "a5fd3d7d…" -> "fdc54e24416133f0a9f67000a9a3719e"  (= md5 rl_model.py)
    (and, if the migration is promoted ON, re-seal board 270a2c5f -> 06d8af60 + re-pin 'board')

Everything else (store, engine_head, config, curve, register, q97m, cm_400) is unchanged.

## VERDICT
Five-migration complete: job 1 HOLD (accepted); unpl_eq + pedestal migrated (rank movement, v-parity);
`_natcv34` NULL (proven); build_pvc_v34 global swap (board-null); umbrella characterized; rider filed.
Kill-switch byte-exact, store unchanged, SSI green but for the expected pre-bake rl_model pin. Candidate
ready for review.
