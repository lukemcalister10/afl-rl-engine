# PLAN — CI GUARD WORKFLOW + BRODIE OVERRIDE WIRING — 2026-07-09

Auto-mode first artifact (committed before any implementation). Base: main @ d4e8f6dc (tag v2.6).
Branch: `claude/ci-guard-brodie-override-xow6zn`. Effort: Medium. Time band: 1–2h (confirmed).

## Decided state inherited (not re-derived)
store `e1b4d8bf` (2652 rows) · board 799b2290 · engine head `4b08796c` · main = tag v2.6 = d4e8f6dc.
RL_PVCFIT engine default `'0'` (`_merged_recover.py:936`) · R3 export bake-guard (`rl_export.py:32`).

## Part A — CI guard workflow (`.github/workflows/ci-guards.yml`)
Runs on every `push` + `pull_request`. FAILS (never warns) unless ALL pass. Thin orchestration of
EXISTING entry points — no guard logic reimplemented in CI. Sequence (verified green locally today):
1. `sudo mkdir -p /home/claude && chown` — the engine uses absolute `/home/claude/...` paths.
2. `actions/setup-python@v5` pinned `3.12.3`; `bash setup_env.sh` (numpy 2.4.4 · scipy 1.17.1 ·
   sklearn 1.8.0 · openpyxl 3.1.5).
3. `bash bootstrap.sh` — seeds workspace + **Guard 5 (boot-store)** at boot via `boot_guard.py` +
   `data/expected_boot.json`.
4. Build board + book (needed for the parity guards): `rl_export.py`, `s4_matrix_M1v7.py`.
5. `one_source_selftest.py` — **Guards 1 (read-only/stamp), 2 (source-hash), 3 (lookalike tripwire),
   5 (boot-store)** + F1/F2 parity.
6. `guard_correction_canary.py` — **Guard 4 (correction-sticks canary)**.
7. `run_panel.sh` — **panel 10/10** (+ Guard 5 on entry).
8. `ruling_config_check.py` (NEW, config-vs-rulings assertion, DECISIONS §16) — **RULING-CONFIG**:
   asserts `RL_PVCFIT` resolves to `0` by default (engine source + CI env) AND the R3 export
   bake-guard block is present/active in `rl_export.py`. Static assertion on the shipped source; no
   engine math. Exits non-zero on any drift.
Timeouts generous (canary ≈ 6 min; whole job ≈ 12 min).

## Part B — Brodie override wiring (display-only, excluded from everything a guard measures)
Insertion point (clean, verifiable, guard-safe): the **export/board-JSON layer**. Guards, aggregates,
book (F2), B4 and JS parity all read `active[].v` or engine `ev()` — NEVER any override field. So the
override is applied by ADDING a marked field to the matched row and NEVER touching `v`.
- `data/owner_overrides.json` — repo-homed, machine-readable, read-once input. Owner adds a row (no
  code change); delete a row to remove. Carries the courier's Brodie ×0.50 ruling + provenance.
- `engine/rl_after/owner_overrides.py` — helper: locate repo (RL_REPO/CLAUDE_PROJECT_DIR), load the
  file, apply to the active board rows. Verifies `will-brodie` is a live board key; reports key-drift
  loudly (toby-briggs/jeremy-cameron precedent) rather than guessing.
- `rl_export.py` — call the helper AFTER the export↔engine parity gate, BEFORE `json.dump`. For each
  matched row add `ov = {factor, dispv=round(v*factor), mark:"OWNER OVERRIDE ×0.50", note, prov}`.
  `v` is untouched → the value every guard/aggregate/book reads is byte-identical. `dispv` is the
  displayed halved value; `mark` is the visible override marker. Env `RL_NO_OWNER_OVERRIDES=1` skips
  application (the on/off toggle the exclusion test uses).
- Display note: the HTML render assets (`_features_v23.js`, `_body.html`, …) are NOT in this repo; the
  board JSON is the read-once display data source (`const D=…`). The marked override value is carried
  in the board data for the renderer to surface; `v`/`val` (engine + JS parity) are left untouched.

## Tests (`session_2026-07-09/ci_guard_brodie/`)
- Part A red-path proof: a deliberately-wrong ruling config (RL_PVCFIT flipped on / bake-guard
  removed) makes `ruling_config_check.py` exit non-zero — demonstrated + captured locally
  (`redpath_proof.txt`) since a live red push to a protected branch is impractical.
- Part B exclusion test (`test_owner_override_exclusion.py`): build the board with the override ON vs
  OFF; assert the two boards are byte-identical after stripping Brodie's added `ov` field, Brodie's
  `v` identical in both, and ONLY Brodie's displayed (`ov`) row differs.

## Commits → one candidate PR against main
(1) PLAN · (2) Part A workflow + ruling_config_check · (3) Part B override wiring · (4) tests.
No engine-value/guard-logic/store changes. No bake/tag/main action. No second copy of any data file.

## STOP condition honored
If Part B's clean insertion conflicts with "display-only, excluded from aggregates," STOP and return
the conflict. No conflict found: adding a marked field without touching `v` is display-only by
construction and excluded from every guard/aggregate/book input.
