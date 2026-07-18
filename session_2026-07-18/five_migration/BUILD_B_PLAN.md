# FIVE-MIGRATION BUILD B — PLAN (completion of the rescued v2 job)

**Branch** `claude/five-migration-pvc-consumers-kxykfd` · **base (STRICT)** `e7c59d0` (the WIP-HALTED
head; `git ls-remote` == `e7c59d07cfbbe44882ea0642cbba6f09e2da44e5`, MATCH) · **ruling** R107.5 ·
**mode** auto (first commit = this PLAN). Continues the same PR line; the auto-created `build-b` branch
(== main, lacks the engine WIP + `pvc_curve_v2.json`) is discarded, nothing pushed from it.

## ENTRY RE-PROOF (every line a command run THIS session; SILENCE IS A RED)
All measured on this container (py3.12.3 / np2.4.4 / scipy1.17.1 / sklearn1.8.0), dev-shell recipe
(`RL_REPO` set, `PYTHONHASHSEED=0`, no `RL_CONFIG_MODE`; `RL_PVC2` toggled), board =
md5(`rl_app_data.json`) built by `rl_export.py`:

| assertion | expected | measured | verdict |
|-----------|----------|----------|---------|
| `git ls-remote … pvc-consumers` | `e7c59d0…44e5` | `e7c59d0…44e5` | PASS |
| store `rl_model_data.json` md5 | `968de0c7` | `968de0c7` | PASS |
| curve `pvc_curve_v2.json` file md5 | `56dd7a7b` | `56dd7a7b` | PASS |
| curve payload stamp `curve_md5` | `89c14729` | `89c14729` (in file `stamp`) | PASS |
| **RL_PVC2=0 board (kill-switch / byte-hold)** | `9829d01a` | `9829d01a` | PASS |
| **RL_PVC2=1 board (ACT-2 ev-channel baseline)** | `270a2c5f` | `270a2c5f` | PASS |

Reproduced twice (pre-WIP engine `a2ee7aa` via bootstrap AND via the direct-seed measurement harness) —
byte-exact both ways ⇒ engine deterministic here, harness validated, no HALT condition.

## FIRST ACT 1 — WIP AUDIT (commit `e7c59d0`, line-by-line disposition)
The HALTED commit captured three hunks. Audited against the proof standard:

| hunk | content | disposition |
|------|---------|-------------|
| `rl_model.py` `+_PVC2M` conduit (`:738-751`) | loads `pvc_curve_v2.json` under `RL_PVC2` (default ON); numéraire + strict-descent asserts; `_PVC2M=PVC` when off ⇒ same-object byte-hold | **KEEP** — matches the PLAN's ruled indirection (OFFLINE+LOADED, no import-time fit); byte-hold verified (`RL_PVC2=0 ⇒ 9829d01a`). |
| `rl_model.py` `unpl_eq` `PVC[…] → _PVC2M[…]` | first leaf consumer repointed | **KEEP** — mechanically correct; UNPROVEN in the WIP, proof finalized this build (`job_unpl_eq`). |
| `single_source.py` `ALLOWED_OPENS += 'pvc_curve_v2.json'` | allowlist line | **KEEP** — mechanically REQUIRED: `rl_model.py` now opens the curve and Guard 3b (`assert_engine_opens`) enforces engine-opens ⊆ ALLOWED_OPENS. |
| `session_.../scripts/board_movers.py` | active-row + pick `v` differ (keyed by `key`) | **KEEP** — the v-parity instrument; used unmodified. |

No hunk fails the standard; nothing reverted-and-redone. The WIP was HALTED as UNPROVEN, not as wrong;
this build supplies the missing proofs and completes the remaining consumers.

## FIRST ACT 2 — FENCE CURE (re-derived INCLUDING the recorded allowlist line)
Union of files the job list mechanically names:
- **`engine/rl_after/rl_model.py`** — all consumer sites (`unpl_eq`, `pedestal`, `_natcv34` inversion,
  the `build_pvc_v34` global producer swap + residual print-readers).
- **`engine/rl_after/single_source.py`** — the `ALLOWED_OPENS` line (justification above). Now RECORDED
  in-fence (absent from the ACT-era derived fence; this is the 322-pattern cure).
- **`session_2026-07-18/five_migration/`** — proofs, measurements, out/.
- **`one_source_selftest.py`** — census-IN **only if execution requires**. It does NOT: it reads
  `ALLOWED_OPENS` from `single_source` (already updated) and its Leg-D curve instrument is `RL_PVC2`-gated
  and structural. **NOT TOUCHED** (no mechanically-required edit found).

**HARD-OUT (asserted, none touched):** the store (`968de0c7`) · `pvc_curve_v2.json` as a WRITE (READ-only
here) · `_merged_recover.py` V0/`_iso_dec` chain · `s4_matrix_7147.py` · SEASON_PROG (`rl_model.py:761`,
owner dial 0.58 — untouched) · `docs/`. HALT on any HARD-OUT need. **`data/expected_boot.json` &
`data/rl_build/rl_app_data.json`:** NOT re-pinned / NOT re-sealed this build — the migration rides the bake
(R107.5 pre-ladder). See EXIT for the single flagged pin item (Guard 5 rl_model, supervisor/bake call).

## THE MECHANISM (why the effect class is RANK, not `v`)
The shipped board `v`/`vM2…vP2` are set by `ev(p,·)` in `rl_export.py:94-95`, which **overwrites** the
rl_model-internal `_v`. The `active` array is emitted in `players` order, and `players` is sorted by
rl_model's `_v = proj_value(0)` (`rl_model.py:1020`). `value()`→`proj_value` is exactly where `unpl_eq`
and `pedestal` read the curve. So migrating those consumers changes the **sort key**, reordering rows,
while the **displayed `v` (=ev) is byte-identical**. That is the checkpoint-law-compliant signature:
rank/pick-equivalent movement, per-row shipped `v` UNCHANGED. Verified board-wide (0 `v` movers).

## JOB MAP (numbering reconciled: consumer name is authoritative)
The Build-B directive and PLAN.md number these differently; commits are labelled by CONSUMER (unambiguous)
with both schemes cross-referenced.

| consumer / site | PLAN.md | directive-B | action | board effect (measured) |
|---|---|---|---|---|
| peak-model `_V4PVC` `:515` | job 1 | job 1 | **HOLD** (train/serve skew; retrain = post-bake) | null (untouched) |
| `unpl_eq` `:821` | job 2 | job 3 | `PVC→_PVC2M` (WIP) | `270a2c5f→01c3645d`, v-parity ✓ |
| `pedestal` `:836` | job 3 | job 4 | `PVC→_PVC2M` | `01c3645d→06d8af60`, v-parity ✓ |
| `_natcv34`/`_pick_equiv` `:863-875` | job 4 | job 5 | **NULL** (realised-value inversion; no PVC read) | null (effpk movers = 0) |
| `build_pvc_v34` global swap `:760` (after `_PVC2M`) | job 5 | — | `PVC:=_PVC2M` under flag (residual print-readers) | board-null (`06d8af60` unchanged) |
| value()/rank/pick-equiv umbrella | — | job 2 | cumulative characterization | `270a2c5f→06d8af60`: 697 rank (394 real/303 casc) |

## CHECKPOINT LAW (binding)
Expected class = RANK / PICK-EQUIVALENT movement, shipped per-row `v` UNCHANGED (parity-gated). If any
commit moved a shipped `v` at RL_PVC2=1 → HALT, return rows to supervisor. **Board-wide result: 0 `v`
movers across every commit. No checkpoint trigger.** Job 1 stays CLOSED (HOLD, R107.5).

## EXIT
Frozen suite (S4) · SSI guards · `RL_PVC2=0 ⇒ 9829d01a` final byte-exact · store `968de0c7` unchanged ·
gates snapshot · rider (report-only) · PR on this branch · RETURN ≤30 lines.
