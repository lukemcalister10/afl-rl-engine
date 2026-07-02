# START_HERE — AFL SuperCoach RL keeper engine — authoritative first-read
_Cut 2026-07-02. Head `8aed420a` (candidate). Nothing baked past `e0ac9c377d1e`. Diagnostic-only session preceded this cut._

## 0. FOUR-STEP RESUME
1. **Restore** into a clean dir (`tar xzf rl_complete_8aed420a_*.tar.gz`).
2. **Bootstrap:** `bash bootstrap.sh` — recreates the absolute `/home/claude/...` layout the engine hardcodes. `verify_restore.sh` FAILs on a clean tree if this is skipped.
3. **Verify by SCRIPT:** `bash verify_restore.sh` — reports PASS/FAIL with actual values (md5 axes + Maric/Langdon + harness presence + 10-panel tail). Never verify by inspection.
4. **Read `docs/KICKOFF_PROMPT.md`** (binding process rules + your first tasks — note the path: it lives under `docs/`, NOT repo root), then `docs/UNRESOLVED.md` (the live queue), then HOLD for directive.

## 1. IDENTITY / MD5 AXES (all verified this cut)
- code→head: `engine/rl_after/_merged_recover.py` = **`8aed420a`**
- data→store: `engine/rl_after/rl_model_data.json` (=`.pre_stage0`) = **`644d1254`**
- band: `data/cm_400.pkl` = **`34faa865`**
- file→bundle: see CHECKPOINT_MANIFEST.md (recorded at cut).
- **BAKED = nothing past `e0ac9c377d1e`.** Lineage in `docs/CHANGELOG.md`.

## 2. FULL ENV (every engine command)
```
PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 \
RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
PYTHONPATH=<tree>/engine/rl_after:<tree>/engine/forward_valuation:<tree>/vendor
```
- **Pinned interpreter + packages (VERIFIED 9/9 exact + panel 10/10, 2026-07-02): Python 3.12.3, numpy 2.4.4, scipy 1.17.1, scikit-learn 1.8.0** (openpyxl 3.1.5 for xlsx). NOT vendored — pip-install at restore. Off-pin combos reproducibly drift the GBR/prior-trained path (SHAKEDOWN.md: Python 3.11.15 + numpy 2.3.5 gave Maric 1426 vs 1409, Langdon 611 vs 593).
- `PAR_RAMPS=22` — the default 14 is WRONG.
- **ONE exec-load per fresh process.** The `_lvl_eff_infer`↔`_lvl_eff_core` `RecursionError` is a DOUBLE-LOAD harness artifact, NOT an engine bug — do not re-escalate it. `verify_restore.sh` embeds the correct single-load pattern.

## 3. FILE MAP (query, don't display — no full trees)
- Engine: `engine/rl_after/_merged_recover.py` (head); base modules `engine/forward_valuation/` (`conditional_prior.py` holds the cont.25 recency machinery — `_swt`, `_exposure`, `_lvl_wt`, `_lvl_eff`, `LEVEL_RAMP=14`; `_swt(yr,Y)=0.72^max(0,Y-yr)`).
- Data: `data/cm_400.pkl` (band), `engine/rl_after/rl_model_data.json` (+`.pre_stage0`), `data/s4_matrix_nogames.json`, `data/traj_out_*.json`.
- Book/harnesses: `engine/rl_after/s4_matrix_M1v7.py`(+.json), `s4_render_M1v7.py`, `s4_render_no2003.py`, `_gate1_wf.py`, `_gate1_picksplit.py`. Board/parity: `rl_build_html.py`, `rl_export.py`, `rl_model.py`.
- Session artifacts: `session_2026-07-01/` (reports, notepads, `scripts/` analysis, `decay_proration_overlay.py`).
- Docs: `docs/CHANGELOG.md`, `docs/HANDOVER.md`, `docs/KICKOFF_PROMPT.md`, `docs/UNRESOLVED.md`, `PROVENANCE_2026-07-01.md`, `REQUIRED_INPUTS.md`, `CHECKPOINT_MANIFEST.md`; `docs/process/` (four binding/record process docs).
- Gates: `verify_restore.sh`, `doc_lint.py` (run before every re-cut).

## 4. LIVE QUEUE
See `docs/UNRESOLVED.md` (every workstream + five-state + exact resume). Headlines: M1+v7 VERIFIED not baked (gate = Luke read-pass); current-season-drop mechanism PINNED (exposure-feature/decay channel) with fix rework pending Luke's read; decay-proration PROPOSED but NON-VIABLE as specified; dev-position fold-in blocked on the ABSENT template; Joel Jeffrey mediocre-overvaluation (Luke's #1) not started; 1.19× parked.

## 5. LANDMINES
- **EXACT-name player matching** — never loose substring (Ed Langdon vs Zac Giles-Langdon; **Max King → "Maxwell King" rename guard**; two Uwlands; 8 name-collisions — key by pick/cohort/id).
- **No full stop in an xlsx filename STEM** (Excel reports the valid file as corrupt). Dot-free stems only. LibreOffice at `/usr/bin/libreoffice` re-serialises if needed.
- **Retain-table numbers are DESIGNED placeholders, above measurement for RUC/KPP** (UNRESOLVED §5).
- Never grep the tarball broadly (matches `players.json` → dumps the DB). Never print full trees/listings.
- The word "closed"/"done" are BANNED as status — use the five-state vocab.

## 6. PROCESS
`docs/process/` holds four docs; PROCESS_CHANGES, CONTEXT_BUDGET_RULES and BUILD_AGENT_FEEDBACK are BINDING and folded into `docs/KICKOFF_PROMPT.md`; SUPERVISOR_AGENT_FEEDBACK rides along for the record.
