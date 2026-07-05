# DATA-FLOW MAP + DEAD-FEATURE INVENTORY + F1 — READ-ONLY (record only, DO NOT MERGE)

**Directive:** BUILD DIRECTIVE 2026-07-05 v2. **Effort:** HIGH. **Scope:** investigate/map/report — no engine
edits, no strip, no bake, no merge. Canonical head untouched.
**Reproduce every number:** `bash evidence/dataflow_probe/probe.sh` (raw logs in `evidence/dataflow_probe/out/`).

---

## STEP 0 — GROUND TRUTH (asserted before any read)
| item | value |
|---|---|
| git HEAD | **389ac397712e623f927259de930ce266bec51afd** (`389ac39`) |
| tag | **baked-v2.4-2026-07-04** |
| engine md5 (`_merged_recover.py`) | **c47cb43d** ✓ (matches baked head) |
| store md5 (`rl_model_data.json`) | **644d1254** == `rl_model_data.json.pre_stage0` (the "reconciled pre_stage0 authoritative") |
| shipped board md5 (`data/rl_build/rl_app_data.json`) | **eb5d6716** |

Candidate data files (path | bytes | last-commit):
- `data/rl_build/rl_app_data.json` | 1,009,246 | 2026-07-04 — **board file (engine OUTPUT)**
- `engine/rl_after/rl_model_data.json` | 1,201,231 | 2026-07-02 — **store (SOURCE OF TRUTH)**, == `.pre_stage0` (644d1254)
- `engine/rl_after/rl_model_data.json.pre_stage0` | 1,201,231 — identical to the live store
- `engine/rl_after/rl_model_data.json.stage0` | 1,225,496 (91a3de6b) — superseded stage-0 variant, not loaded
- No `afl_master_db.*` exists. `data/s4_matrix_*.json`, `data/cm_400.pkl` = engine internals, not the universe.

---

## TASK 1 — THE DATA-FLOW MAP (primary deliverable)
1. **Source of truth (raw universe):** `engine/rl_after/rl_model_data.json` (== `.pre_stage0`, authoritative). Loaded at
   `rl_model.py:4` `data=json.load(open('rl_model_data.json'))`.
2. **Engine output:** `rl_export.py:250` `json.dump(out, open('rl_app_data.json','w'), sort_keys=True)`. The export execs
   `rl_model.py` + `_merged_recover.py`, computes `_p['_v']=ev(p,2026)` per player (`rl_export.py:28-30`).
3. **What the board reads:** `data/rl_build/rl_app_data.json`. `bootstrap.sh:17` copies it to
   `/home/claude/rl_build/rl_app_data.json`; consumed by `compute.py:21`, `rl_build_html.py:10`, `_rl_parity.js:4`,
   and rendered/projected by `_engine_block_v23.js:77,94`.
4. **LIVE or STALE?** **LIVE.** Regenerating the export from the baked engine + store under the panel env
   (`run_panel.sh` env) reproduces the shipped file **byte-for-byte** (regen md5 **eb5d6716** == shipped **eb5d6716**).
   The `GEN_FWD` / `0.7-0.3` (board) vs `GFWD` / `70-30` (store) difference the clue chased is **NOT a version split** —
   it is export normalization: `rl_model.py:GRP` maps `GFWD→GEN_FWD`, and `futblend()` scales `_fut` weights /100.
   *(An earlier env-less regen gave a different md5 — a false-stale artifact of omitting `RL_RUCK_TAX`/`RL_RECENCY_DECAY`,
   which are load-bearing. With the correct env it is an exact byte match.)*
   **Caveat:** LIVE ≠ correct — the exporter drops the engine's `_REAL`-gated layers (see TASK 3).

**CHAIN (one line):**
`rl_model_data.json (=pre_stage0, SOT) → rl_model.py → _merged_recover.py ev() → rl_export.py → BOARD READS: data/rl_build/rl_app_data.json (→ /home/claude/rl_build/ → rl_build_html.py + _engine_block_v23.js)`

---

## TASK 2 — DEAD-FEATURE INVENTORY (strip-list; delete-don't-disable; NOT stripped)

### Dual-position / DPP  — **LIVE, not inert**
| file | field / site | status |
|---|---|---|
| `engine/rl_after/rl_model_data.json` | `_pos_now` (**131** players) | **LIVE** — `rl_model.py:35 bnow()` → grp + active valuation |
| `engine/rl_after/rl_model_data.json` | `_fut` multi-position (**94** players) | **LIVE** — `rl_model.py:36 gfut()` (max-weight → curve/peak/runway/RUC-detect), `:41 futblend()`, `_merged_recover.py:233` (iso cap "dual→favourable") |
| `data/rl_build/rl_app_data.json` | per-player `grp`,`gf`,`fut` | **LIVE** — `_engine_block_v23.js:77,94 projFromPeak(...p.fut...)` |
| e.g. `christian-petracca` | store `_pos_now:GFWD _fut:[[MID,70],[GFWD,30]]` → board `grp:GEN_FWD gf:MID fut:[[MID,0.7],[GEN_FWD,0.3]] v:3033` | should be MID-only; **still dual-priced & displayed** |
| e.g. `louis-emmett` | store `_fut:[[RUC,50],[KFWD,50]]` | dual RUC/KFWD |

### Old PVC — **retired from penalties; ONE live pricing use survives = the retained ruck cap**
| file | site | status |
|---|---|---|
| `engine/rl_after/_merged_recover.py:238` | `draftval(p)=MA.PVC[...]` | LIVE but scoped |
| `_merged_recover.py:317,493` | `RUC_PRIOR_CAP*draftval(p)` (ruck cap, baked 1.73→**1.4**) | LIVE in engine — **the one retained PVC use** (owner kept the ruck cap). **BUT dropped on the board** by the export `_REAL` bug (TASK 3) → inert on the board. |
| `_merged_recover.py:496` | staleness penalties | old-PVC draftval **already PURGED** (comment + D10) |
| `_merged_recover.py:537,556` | floor | **RE-ANCHORED** off draftval → live V0 start (Luke R8) |
| `rl_export.py:244-249` | `PVC`/`intake`/`picks` (board asset values) | LIVE — board economics, not player pricing |

---

## TASK 3 — F1 RUCK-CAP TEST — **CONFIRMED**
| Louis Emmett (louis-emmett, RUC, pick27/2025, 5g) | value |
|---|---|
| **Gated engine** ev (cap 1.4 ON, `id∈_REAL`=True) | **853** |
| **Shipped board** `v` | **1361** |
| Export-path `_ev` (`id∈_REAL`=False) | **1361** (== board) |
| Ruck cap present in shipped file? | **NO** — board = uncapped 1361 |

**The `id(p) in _REAL` dual-namespace pattern exists and DROPS the baked layers at export — YES.** Mechanism:
`rl_export.py` execs `rl_model.py` **twice** — once directly for the priced `players` (`rl_export.py:6`) and again via
`import rl_model as MA` inside the `_merged_recover.py` exec (`rl_export.py:25`). `_REAL` is built from the *second* copy's
`MA.data` (`_merged_recover.py:194 _REAL=set(id(p) for p in MA.data)`), so the priced players are foreign objects:
**0 of 805** exported players have `id(p) in _REAL` (verified). Every `_REAL`-gated layer is therefore skipped at export:
- ruck cap — `_merged_recover.py:317` `return min(v,RUC_PRIOR_CAP*draftval(p)) if (id(p) in _REAL and MA.gfut(p)=='RUC') else v`
- ruck production-leg cap — `:492 if id(p) in _REAL and MA.gfut(p)=='RUC':`
- v7 age-taper — `:196 if id(p) in _REAL: return _v7(bb,p,Y)`
- year-schedule floor — `:552 if id(p) not in _REAL ... : return v`

---

## TASK 4 — POPULATION (board's real file)
- Board active rows: **805** = export `active`=**805** (1 row carries `v=0`). No 794/805 gap surfaced — both sides reconcile at 805.
- Store `_retired=True`: **1849**; **0** appear on the board active list; **0** retired carry non-zero board value.
- Injured **NOT** mislabeled retired: `toby-conway` `_retired=False g=6 v=468`; `max-king-syd` (Maxwell King) `_retired=False g=0 v=347`. Both correctly active.

---

## TASK 5 — RECONCILE THE COLD REVIEW — **the review's sweep is CONFIRMED (not suspect)**
Re-ran the board-vs-engine sweep from the baked gated engine (`data/rl_build/rl_app_data.json` `v` vs true single-namespace `ev`):

| metric | my reproduction (baked engine) | cold review (c62k2c @ 283cd9b) |
|---|---|---|
| divergent | **536 / 804 (67%)** | 537 / 805 (67%) |
| median board-vs-engine | **+12.57%** | +12.5% |
| mean | +32.7% | — |
| rucks diverging | 47 | — |

Agreement is exact (off-by-one = the single `v=0` row). Root cause of the divergence is the TASK-3 export `_REAL` layer-drop:
board values are the engine's ev() **with the real-player layers stripped**. (My baked ev(Daicos)=7013 == the review's
`ev_own`=7013; both differ from the board's 7063.)

---

## RETURN — PLAIN TERMS
Our real data is the engine store `rl_model_data.json` (the reconciled pre-stage0 player universe); the board reads
`data/rl_build/rl_app_data.json`, which the exporter writes. That board file is **not stale** — the current engine
regenerates it byte-for-byte — but it **is wrong**: the exporter prices players through a *second, separate copy* of the
model, so the engine's "real-player" safety layers (ruck cap, age-taper, floor) never fire when the board is built.
That is essentially **one bug with a wide blast radius** — ~536 of 805 players (**67%**) are mispriced on the board,
typically **~12-13% too high**, worst on rucks (Louis Emmett shows **1361** but the engine says **853**). Separately, the
retired **dual-position/DPP** tags (Petracca et al.) are still live and shaping prices — a second, distinct clean-up the
strip hasn't done yet.
