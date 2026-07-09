# PLAN — GATE INTEGRITY REPAIR — 2026-07-09

Auto-mode first artifact (committed before any implementation). Effort: **High**. Time band: **3–5h**
(confirmed). Branch: `claude/new-session-3fagg1`.

## Entry state (cited on entry, per directive)
- **Base = main @ `60663bd`** (origin/main after fetch = the CI guard PR #47 merge; local `main` was a
  stale `00d82dd` upload before the fetch). The directive was written against tag v2.6 = `d4e8f6dc`;
  the CI PR has since landed, so file/line cites below are **re-located**, not assumed.
- Decided facts inherited (asserted, not re-derived): store `e1b4d8bf` (2652 rows) · board `799b2290`
  · engine head `4b08796c` · rl_model `121a45d0` · band `34faa865` · G-COHORT 128.8/127.3/119.6.
  RL_PVCFIT engine default `'0'` (`_merged_recover.py:936`) + export R3 bake-guard (`rl_export.py:32`)
  + CI RULING-CONFIG (`ruling_config_check.py`) — all preserved, none weakened.
- **Byte-identity anchor established on entry**: `rl_export.py` under the official env rebuilds
  `rl_app_data.json` md5 `799b2290` = shipped (verified, ~85s). This is the green-path proof target
  that must hold before/after every commit.

## Order (dependency-driven; one commit per lettered item)
(c) → (d) → (e) → (b) → (a). Rationale: (b) and (a) embed the **config hash** produced by (e), so the
(e) manifest/helper lands first; (c)/(d) are self-contained and cheap, done first to de-risk.

## (c) PAR_RAMPS default alignment — `engine/forward_valuation/par_redesign.py`
`par_redesign.py:27` defaults `PAR_RAMPS` `'14'`; START_HERE + every official script use `22` and call
14 wrong. par_redesign is a STANDALONE mock ("nothing wired into engine value()"); `PAR_RAMPS` is read
nowhere on the live board/book path (the engine's confidence ramp is `RL_LEVEL_RAMP`, distinct). Fix:
code default `'14'` → `'22'` (line 27 + the docstring run-line). **PROOF**: official-env board stays
byte-identical `799b2290` (the official env already exports `PAR_RAMPS=22`, so only the clean-shell
`par_redesign.py` path moves).

## (d) Stale state strings — `START_HERE.md`, `data/expected_boot.json` (+ swept siblings)
Update strings that MISDESCRIBE the CURRENT baked state as v2.5; **preserve all lineage/history and the
named v2.5 comparator labels**. Declare BAKED **v2.6** / engine `4b08796c` / board `799b2290` / store
`e1b4d8bf` (content hashes are authoritative and stable; git-head nuance noted in the RETURN).
- `START_HERE.md` header ("BAKED v2.5 … Head efea88e5") + "BAKED = nothing past e0ac9c37" line.
- `data/expected_boot.json` `tag` string ("candidate-… on v2.5 store"). **Guard-5 coordination**: Guard 5
  asserts only `store`/`engine_head`/`band` md5s (unchanged); `tag` is a printed human string it does
  NOT assert → suite stays green. Exactly what changed there is stated in the RETURN.
- Sweep (`git grep`) and LIST every same-class hit in the RETURN. Historical `data/gates_snapshots/*`,
  `report_states.json` lineage map, and the v2.5 CONTROL comparator are PRESERVED (they are history).
  The doc pack under `docs/` is the supervisor's pen — OUT OF SCOPE.

## (e) Minimal config manifest — the durable half of R3
- **`data/model_config.json`** (versioned, in-repo): every model-semantics RL_*/PAR_* variable with its
  canonical value (= today's effective value under the official env; enumerated in the RETURN) + a
  canonical SHA over the sorted (name,value) pairs. Infra/path vars (RL_REPO, CLAUDE_PROJECT_DIR,
  RL_APP_DATA, RL_FV, PYTHONHASHSEED, RL_NO_OWNER_OVERRIDES display toggle) are NOT model semantics and
  are excluded (listed as such).
- **`config_manifest.py`** (repo root, thin, no engine math): `enforce(mode)` — in **bake/gate mode
  only** (opt-in via explicit `RL_CONFIG_MODE=bake|gate`): (1) snapshot+clear ambient model RL_*/PAR_*
  vars, (2) reject any model override whose value ≠ the manifest (unknown/divergent → `SystemExit`
  halt-not-warn), (3) load the manifest values into `os.environ`, (4) return the canonical hash.
  Ordinary dev-shell runs (no `RL_CONFIG_MODE`) are UNCHANGED — experimentation stays possible.
- **Stamp the config hash** into: boot identity (`expected_boot.json` new `config` field), the
  regenerated book/matrix meta (e), and the gate report string. **NOT into `rl_app_data.json`'s value
  bytes** — the board must stay byte-identical `799b2290` (directive green-path), so the board-side
  stamp is an identity record, never a payload byte. This reconciles "stamp into board" with "board
  byte-identical throughout"; called out explicitly in the RETURN.
- Because every canonical value = the current code default (post-(c)) = the official-env value, clearing
  ambient + loading the manifest reproduces the board/book/panel byte-for-byte.
- Existing RL_PVCFIT bake-guard + CI RULING-CONFIG remain on top, untouched.

## (b) B2 runs its own producer, stops trusting text — `_gate1_wf.py`, `ship_gates_check.py`
- `_gate1_wf.py` emits a structured JSON certificate (UNROUNDED observations per (pos,tag,tenure) +
  code/store/config hashes) alongside its human print.
- B2 in `ship_gates_check.py`: invoke the producer in a clean subprocess, read the JSON, assert its
  hashes == candidate under test, compute leakage at FULL precision (tol **0.5** unchanged — frozen
  gate number, reported never amended), report per-cell gaps beside the pooled median. Label the check
  honestly as **leave-cohort-out sensitivity** (its true construction).
- **Red path**: a handcrafted 4-line text certificate no longer parses/passes (JSON+hash required); a
  rounding counterexample (true gap 0.98 %-pts) is now measured at full precision, not masked to 0.

## (a) B1/B3 test the candidate, not v2.5 — `ship_gates_check.py`, `s4_matrix_M1v7.py`
- **STOP-condition check (a):** the matrix can carry embedded code/store/config hashes via a `__meta__`
  record added by `s4_matrix_M1v7.py` — thin plumbing, NO engine-valuation code touched. No conflict →
  proceed (if it had required engine changes I would STOP and return the conflict).
- Gate runner regenerates the CANDIDATE matrix itself in a clean subprocess (~3 min), requires the
  regenerated `__meta__` hashes == candidate (engine/store/config); a mismatch is a **FAIL**, not a
  warning. B1/B3 then run against the regenerated candidate matrix. The baked `s4_matrix_baked_efea88e5`
  stays as an explicitly NAMED "v2.5 comparator" (never "current"); the gate report states WHICH
  artifact each verdict certifies. B3's immutability/seal logic is preserved, re-pointed accordingly.
- **Red path**: feeding the stale v2.5 matrix as the candidate artifact (hash mismatch) FAILs the gate.

## Tests & proofs (`session_2026-07-09/gate_integrity/`)
Red-path proofs for (a), (b), (e); green-path: full suite from a fresh bootstrap passes and the
official-env board is byte-identical `799b2290` throughout (this job moves NO player value). The new CI
must be green on this branch (build + one_source_selftest + canary + panel + RULING-CONFIG).

## OUT OF SCOPE (fenced)
No player-value/lever/surface/valuation change (except (c)'s default, with its byte-identity proof).
Frozen tolerances/thresholds reported, never amended. No measurement-integrity-chapter territory. No
Brodie/OWNER_OVERRIDES change. No docs/ pack edits. No bake/tag/main action (owner-only). No second copy
of any data file (SSI). No force-push, no branch deletion.

## Deliverable
Per-item commits → ONE candidate PR against main. BUILD-REPORTED until supervisor prescreen.
