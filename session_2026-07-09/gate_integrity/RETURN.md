# RETURN — GATE INTEGRITY REPAIR — BUILD-REPORTED — 2026-07-09

**Branch** `claude/new-session-3fagg1` · **base** main @ `60663bd` (CI guard PR #47 merged; local `main`
was a stale `00d82dd` upload until fetched) · **head** `09f7cc3` · **PR** #51 · **effort** High ·
**time** within band 3–5h.

All five FENCE items landed, one commit each (b+a share ship_gates_check.py Section B and are committed
together — they interleave in one diff hunk; splitting risked a broken intermediate). NO engine valuation
math changed. Board byte-identity held throughout (no player value moved).

## What changed
- **(c) PAR_RAMPS default 14→22** (`par_redesign.py`) — clean-shell now equals the official env; START_HERE
  called 14 wrong. par_redesign is a standalone mock, off the board/book path. PROOF: official-env board
  rebuild = `799b2290` byte-identical.
- **(d) Stale state strings → BAKED v2.6** — `START_HERE.md` (header + code→head + BAKED marker) and
  `expected_boot.json` `tag` now declare BAKED v2.6 / engine `4b08796c` / board `799b2290` / store
  `e1b4d8bf` (unchanged since v2.5), lineage preserved. Guard 5 asserts only store/engine_head/band md5s
  (untouched) — re-run PASS, now printing the v2.6 tag.
- **(e) Config manifest** — `data/model_config.json` (39 model vars) + `config_manifest.py`. Bake/gate mode
  (opt-in `RL_CONFIG_MODE`) clears the ambient model env, rejects unknown/divergent overrides (halt), loads
  the manifest, stamps its hash `d88404f0…` into boot identity, book seal, and the gate report. Guard 5
  now checks code+store+CONFIG. Dev-shell unchanged. CI runs the build in bake mode + a config-check step.
- **(b) B2 runs its own producer** — `_gate1_wf.py` emits a JSON certificate (unrounded observations +
  code/store/config hashes); B2 invokes it, asserts the hashes == candidate, computes leakage at FULL
  precision (tol 0.5 unchanged), reports per-cell gaps + pooled median, labelled leave-cohort-out
  sensitivity. A handcrafted text file / stale cert no longer passes.
- **(a) B1/B3 test the candidate** — the gate runner regenerates the candidate matrix in a clean subprocess,
  requires its embedded `__meta__` hashes == candidate (mismatch = FAIL), and B1/B3 run against it. The
  baked v2.5 matrix is now a NAMED "v2.5 comparator" only. Fixed the exact defect: the recorded v2.6 gate
  had B1 (`AVG peak 143`) and B3 both certifying `s4_matrix_baked_efea88e5.json` (v2.5).

## Suite (green-path, from fresh bootstrap) — `session_.../ship_gates_report_4b08796c.md`
B1 **PASS** (CANDIDATE regen, AVG peak 130, path_ok; v2.5 comparator 143 NAMED, not certified) · B2 **PASS**
(leave-cohort-out, leakage 0.000 %-pts full precision, GOOD>BUST clear, cert hashes verified) · B3
**DIFFERS-BY-DESIGN** (candidate vs v2.5 sealed head; owner re-seal at bake — below) · B4 **PASS** (board
`799b2290` == shipped, byte-identical) · B5 **FEATURE** · B6 **PASS** · D14a/b/c **PASS**. The 3 FAILs are
the SAME pre-existing reds — A2 (owner-ruled ships-red), A3 & A12 ([DC] data-caused) — **no new
engine-caused reds**. Gate report header now carries head+store+**config d88404f0** and every B-verdict
names WHICH artifact it certifies. Local CI-equivalent: bake-mode build + one_source_selftest + canary +
panel 10/10 + ruling-config + config-manifest all green; GitHub CI run #9 on this head.

## (d) string inventory (swept; edited vs preserved)
EDITED (stale current-state): `START_HERE.md` (3 lines), `data/expected_boot.json` tag.
PRESERVED (history / comparator / out-of-scope, listed): `data/report_states.json` v2.5 CONTROL comparator;
`_merged_recover.py` "ALL-OFF byte-exact baked v2.5" invariant comments; `run_panel.sh` baked-v2.5
comparator note; `PANEL_EXPECTED.txt` (genuine v2.5 VALUES, correctly labelled — a v2.6 panel is a
bake/value action, owner-only); `CHECKPOINT_MANIFEST.md` (historical v2.4 cut record); `evidence/` +
`session_*/` (history); `docs/*` (supervisor's pen).

## (e) variable inventory
MODEL (39, in the manifest): RL_GAMMA RL_PICK1 RL_RUCK_TAX RL_REPL_DROP RL_RECENCY_DECAY RL_PRIOR_TREES
PAR_RAMPS PAR_BW PAR_MING PAR_K RL_EXPO_F RL_EXPO_INPROG_Y RL_LEVEL_RAMP RL_M3_FE RL_M3_INPROG_Y RL_FORMDECL
RL_FWDRECAL RL_YOUNG RL_OVPX RL_KPFFIX RL_V7FORM RL_V7_FORM_W RL_W4_CRED RL_W4_KPFUP RL_W4_FADE RL_W4_OVPX
RL_W4_KPFSH RL_W4_KPFSH_DEM RL_W4_KPFTOP RL_W4_KPFM0 RL_W4_KPFMS RL_YCRED_W RL_YCRED_KPF RL_RUC_PRIOR_CAP
RL_W4_RUC RL_RUC_CEIL_HEAD RL_RUC_CEIL_REFPK RL_RUC_YRH RL_PVCFIT.
INFRA (excluded, allowed ambient): RL_REPO CLAUDE_PROJECT_DIR RL_APP_DATA RL_FV RL_NO_OWNER_OVERRIDES
RL_ALLOW_PVCFIT_BOARD RL_CONFIG_MODE RL_VENV PYTHONHASHSEED. (RL_RUCK_TAX is orphaned on the live path but
pinned for env-parity; noted in the manifest.)

## expected_boot.json — exactly what changed there (Guard 5 coordination)
`tag` string → v2.6 (print-only; NOT asserted). ADDED `config` field `d88404f0…` (Guard 5 now also asserts
config==manifest, backward-compatible). store/engine_head/rl_model/band/board md5s UNCHANGED.

## OWNER ACTION REQUIRED (flagged, NOT performed — bake-only)
B3 now seals the CANDIDATE (head `4b08796c`) vs the v2.5 baseline seal (head `efea88e5`, `5799a9ce…`).
The candidate book legitimately differs → B3 reports **DIFFERS-BY-DESIGN** (new head; re-seal at bake).
Re-sealing `book_stable_seal.json` (stable_sha256 → the v2.6 book `ff6cf9d8…`, head → `4b08796c`) is an
owner-only BAKE action — NOT done here. Until then B3 is honest-but-not-a-clean-PASS on the candidate.

## Fenced / not done
No player-value/lever/surface/valuation change (except (c) with its byte-identity proof). Frozen
tolerances/thresholds reported, never amended (B2 tol 0.5 unchanged). No bake/tag/main action; no re-seal;
no second copy of any data file (the regenerated matrix + B2 cert are ephemeral tmp artifacts); no
force-push; no Brodie/OWNER_OVERRIDES change; no docs/ pack edit.

## IN PLAIN TERMS
The release gates now test the actual candidate instead of quietly grading last version's board, the leakage
check reads a hashed number it computed itself instead of a text file anyone could fake, one config file now
pins every knob so a stray setting can't sneak into a bake, and the front-page/boot labels finally say v2.6.
