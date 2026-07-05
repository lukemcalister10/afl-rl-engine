# Consolidation Step 1 — Map + Source Extract (READ-ONLY)

**Directive:** BUILD DIRECTIVE — CONSOLIDATION STEP 1: MAP + SOURCE EXTRACT (2026-07-05).
**Nothing decided or deleted here.** Inventory + one export only. Canonical untouched.

## STEP 0 — Ground truth (asserted, re-checkable via `inventory_dump.py`)

| item | value | expected | status |
|---|---|---|---|
| baked head (parent) | `389ac39` (tag `baked-v2.4-2026-07-04`) | `389ac39` | ✅ ancestor of HEAD |
| store md5 | `644d1254` | `644d1254` | ✅ `rl_model_data.json` = `pre_stage0`, authoritative |
| engine baked matrix | `data/s4_matrix_baked_c47cb43d.json` | md5 `c47cb43d` | ✅ (by filename + bootstrap) |
| board md5 | `eb5d6716` | — | `data/rl_build/rl_app_data.json` (== `/home/claude/rl_build/` copy) |
| store size / records | 1,201,231 bytes / **2656** records | — | list, one per player |

> HEAD advanced past `389ac39` **only** by this task's read-only `evidence/` commits.
> `git diff 389ac39..HEAD -- engine/ data/` is empty — no canonical file changed.

---

## TASK 1 — Source-of-truth export (owner sanity-check)

- **Path:** `evidence/consolidation_map/source_of_truth_current.xlsx`
- **Record count:** **2656 rows** (one per player), sorted alphabetically by name.
- **Tab 1 `SOURCE_current`:** SOURCE/input fields only (NO derived prices) — name · key/id · DOB · born-year · draft year · pick (+pickless) · draft type · draft category (`_cat`) · draft channel (`_draft`, carries MSD/Ireland tags) · club · present position · drafted position · `_pos_now` override · retired · career games · most-recent-season (year/avg/games) · has-2026 · force-active · last-listed · raw `_fut` AS-IS · phantom/double-count/pvc-exclude flags.
- **Tab 2 `COLLISIONS`:** 398 shared surnames / 1271 players, keyed by ID (the two Emmetts; 8 Kings incl. `max-king-syd` vs `max-king-stk`, etc.).
- Script: `evidence/consolidation_map/export_source_of_truth.py` (asserts ground truth on run).
- **DATA_SOURCE (every column):** `engine/rl_after/rl_model_data.json`.

---

## TASK 2 — Data-location inventory (every place data lives)

**The pipeline is a single line:** `rl_model_data.json` (+ configs/snapshots) → `rl_model.py` → `_merged_recover.py` (ev) → `rl_export.py` → **`rl_app_data.json`** → `rl_build_html.py` → `rl_draft_engine.html`.

| file | READ by | WRITTEN by | class | authored |
|---|---|---|---|---|
| **`engine/rl_after/rl_model_data.json`** (store, =`.pre_stage0`, `644d1254`) | `rl_model.py:4` (the **only** programmatic read); everything else `import rl_model` | none in pipeline; restored by `bootstrap.sh` from `.pre_stage0` | **SOURCE** | HAND |
| `…rl_model_data.json.pre_stage0` / `.stage0` | `bootstrap.sh` restore / snapshots | one-time | SOURCE snapshot | HAND / GEN |
| `engine/rl_after/params.json` | `rl_model.py:4` | — | **CONFIG** | HAND |
| `engine/rl_after/rl_passmark.json` | `rl_model.py:4` (peak-multiplier `pm_pos`/`pm_band`) | — | **CONFIG** | HAND |
| `engine/rl_after/pvc_snapshot.json` | `rl_model.py:362` (train-time PVC, breaks bootstrap cycle) | baked snapshot | CONFIG snapshot | GEN |
| `engine/rl_after/bust_prior_table.json` | `rl_model.py:361`, `build_peak_model_v4.py` | built once | CONFIG/DERIVED | GEN |
| `engine/rl_after/peak_model_v4.pkl` | `rl_model.py:360` | `build_peak_model_v4.py:66` | DERIVED model | GEN |
| `data/cm_400.pkl` (`34faa865`) | `wire_redesign.py:35` | `wire_redesign.py:39` | DERIVED cache | GEN |
| **`data/rl_build/rl_app_data.json`** (board, `eb5d6716`) | `rl_build_html.py:10`, `_rl_parity.js:4`, `compute.py:21`, `ship_gates_check.py` | `rl_export.py:250` (written in cwd; deployed by `bootstrap.sh:17`) | **DERIVED** app board | GEN |
| `engine/rl_after/s4_matrix_M1v7*.json` | `s4_render_*.py` | `s4_matrix_M1v7*.py` | DERIVED matrix (xlsx book) | GEN |
| `data/s4_matrix_*.json` (baked_c47cb43d, control_8aed420a, v2/v21/v22/nogames/gradedfix) | `ship_gates_check.py`, session scripts | `s4_matrix_*` builders via `S4_MATRIX=` | DERIVED matrix | GEN |
| `data/book_stable_seal.json` | `ship_gates_check.py:300` | baked baseline | DERIVED seal | GEN |
| `data/report_states.json` | `ship_gates_check.py:63`, `s4_render_7147.py:10` | — | **CONFIG** registry | HAND |
| `data/gates_snapshots/gates_*.json` | `ship_gates_check.py:69` | `ship_gates_check.py:509` | DERIVED snapshot | GEN |
| `engine/forward_valuation/dob_corrected.json` | `build_peak_model_v4.py:11` | — | SOURCE/CONFIG | HAND |
| `AFL_RL_DEVELOPMENT_position_template.xlsx` | position-fill input | — | SOURCE template | HAND |
| `docs/…book_*.xlsx`, `session_*/…xlsx` | deliverable books | `s4_render_*` / `_build_book_xlsx.py` / `build_cohort_book.py` | DERIVED book | GEN |

**Is `data/rl_build/rl_app_data.json` the ONLY board the app reads? → YES.** The shipped app is one self-contained HTML: `rl_build_html.py:10` reads the board once at **build** time and inlines it as `const D = {…}` (`:18`). The engine JS (`_engine_block_v23.js`) has **no** `fetch`/`require`/`readFileSync` — it consumes the injected `D`. No runtime data load of any kind; no second board. (`compute.py`/`_rl_parity.js` also read it, but those are analysis/parity harnesses, not the app.) The store copy at `/home/claude/rl_build/rl_app_data.json` is byte-identical to the repo copy (`eb5d6716`).

---

## TASK 3 — Feature / credit inventory (what's live that may be cut)

### MSD / Ireland credits (owner-flagged — LIVE)
Two mechanisms, both live:
1. **Credit phantom records** — hand-authored synthetic rows `Lachlan McAndrew (MSD credit)` (`_phantom`+`_double_count`, type MSD) and `Mark Keane (IRE credit)` (`_phantom`+`_double_count`, type IRE). They are **excluded from the forward board** (`s4_matrix*.py:eligible()` drops `_double_count`/`_phantom`) but **DO enter the backward pathway pool** in the pick-equivalent loop (`rl_model.py:705-733`, `_double_count` comment at `:419`). There they raise each pathway's pooled value → **`PICKEQ`** → assigned as `_eff` pedigree anchor for *every* player of that type.
   - **To whom / magnitude (DATA_SOURCE `rl_app_data.json` PICKEQ/MECH):** MSD → `pick_equiv 59` applied to all **63** active MSD players; IRE → `pick_equiv 94` applied to all **14** active IRE players. (Site: `rl_model.py:734` `if p['type'] in PICKEQ: p['_eff']=PICKEQ[p['type']]`.)
2. **MSD half-season standardisation** — `MSD_Y1_MULT=1.5` (`rl_model.py:11`, floor-multiplies MSD debut-year games) and `MSD_S1_MULT=2.0` (`rl_model.py:736`, doubles MSD debut games for establishment-P). Live, applies to all MSD (`type=='MSD' and not _phantom`).

### Dual-position / DPP machinery (confirmed LIVE — every site)
| site | file:line | role |
|---|---|---|
| `bnow(p)` | `rl_model.py:35` | present-position basis `GRP(_pos_now or pos)` — own active value |
| `gfut(p)` | `rl_model.py:36-40` | settled FUTURE group = max-weight `_fut` — drives curve/peak/runway |
| `futblend(p)` | `rl_model.py:41-46` | normalised `_fut` blend — years-1+ replacement mix |
| dual→favourable cap lift | `rl_model.py:233-235` | a genuine dual's eligible pos lifts the spike cap (e.g. Serong KDEF/MID→0.83) |
| forward-board pos roll | `rl_model.py:409-410` | year-0 present rolls to `gfut` on forward boards |
| board fields | `rl_export.py:44` (`grp`=bnow, `gf`=gfut, `fut`=futblend) | DPP surfaced to app |
| book switch flag | `s4_matrix_M1v7.py:104` (`cpos`=gfut, `sw`=pos≠gfut) | DPP surfaced to xlsx book |
| `_fut` consumers | `rl_model.py:37,42,233` | raw multi-position weights (source: 750 records, 716 non-empty) |

### Old-PVC remnants (beyond the retained ruck cap)
- **Retained ruck cap (LIVE):** `RUC_PRIOR_CAP` in `_merged_recover.py:315` — **baked 1.73→1.4** at v2.4 (`RL_RUC_PRIOR_CAP` env override preserved). 1.73 was the class's own ND-ruck median V0/PVC; capped at 1.4× PVC for real rucks (`_ruc_prior_cap` `:316`, applied `:431,:492`).
- **`draftval`** (`s4_matrix_M1v7.py:105` = `PVC[effpk]`) — a legacy PVC-value column still emitted in the xlsx book record. Inert for pricing; display-only remnant.
- **`realized_cv` / `_natcv`** (`rl_model.py:678-690`) — LEGACY national realised-value curve, comment: "retained ONLY for `rl_export`'s father-son/academy/next-gen overshoot panel". The live board uses `_natcv34` instead. Legacy panel remnant.

### Other special-case / bespoke adjustments (LIVE unless noted)
| flag / knob | file:line | records | effect |
|---|---|---|---|
| `_pvc_exclude` | `rl_model.py:110-114` | 3 (Shiel, Cameron, Treloar) | dropped from PICK-CURVE builders + slide-up of picks behind them; forward board unaffected |
| `_phantom` bust rows | `rl_model.py:14,796` | 2 (`phantom-2019nd35`, `phantom-2022msd11`) | synthetic busts in ND/MSD pools; never reset |
| `_force_active` / `_unplayed` | `rl_model.py:421` | 63 | force a player treated as active |
| `_has26` | `rl_model.py:423,946` | 2656 (true where relevant) | recent-activity gate |
| establishment-P (`pgrid`/`P_estab`/`P_HOOK`) | `rl_model.py:735+` | all | per-player bust-risk personalisation (ported from compute.py, now single-source) |
| Brodie role-reliability ×0.5 | `rl_model.py:642` | signalled | non-ruck 5+ seasons never-durable level≥80 → value ×0.5 |

---

## TASK 4 — Position-field inventory (collapse to present + drafted)

| field | where | meaning |
|---|---|---|
| `pos` | SOURCE | **drafted position** — 7 codes: MID·GFWD·GDEF·KFWD·KDEF·RUC·DEF |
| `_pos_now` | SOURCE (131) | **present position** override (e.g. Dangerfield pos=MID → `_pos_now`=GFWD) |
| `_fut` | SOURCE (750) | raw multi-position future weights `[[pos,wt],…]` |
| `GRP` | engine map (`rl_model.py:31`) | collapses 7 codes → 6 valuation groups (MID·RUC·GEN_FWD·KEY_FWD·GEN_DEF·KEY_DEF; **DEF→GEN_DEF**) |
| `bnow` | engine | `GRP(_pos_now or pos)` = **present** group |
| `gfut` / `gf` | engine / board | `GRP(max-weight _fut)` = **future settled** group |
| `futblend` / `fut` | engine / board | normalised future weight blend |
| `grp` | board (`active`/`back`) | = `bnow` (present group) |
| `cpos` | book (s4_matrix) | = `gfut` (settled future) |
| `sw` | book (s4_matrix) | switch flag: drafted `pos` ≠ `gfut` |
| `pm_pos` | params/passmark | peak-multiplier curve key `'band\|group'` (not a player position) |

**Collapse target — exactly TWO fields:**
- **`present_position`** = `_pos_now or pos` (source: 131 explicit overrides; board `grp`/`bnow`).
- **`drafted_position`** = `pos` (source; book `pos` uses drafted, board `grp` currently uses present).

`_fut` (DPP blend), `gfut`, `futblend`, `cpos`, `sw`, `pm_pos` are all **derived** from the above two + weights — none is an independent source of position truth.

---

## IN PLAIN TERMS

Right now the player data lives in essentially **one hand-authored source file** (`rl_model_data.json`, 2656 players) that flows through a single build chain into **one derived app board** (`rl_app_data.json`) — that board is the only thing the app reads, so the sprawl is really "one source + one board + a pile of configs/snapshots/matrix variants that hang off the build," not multiple competing sources. The confusing live credits are: two **fake phantom players** (McAndrew-MSD and Keane-Ireland) that quietly lift the whole Mid-Season pathway to pick-59 and the whole Ireland pathway to pick-94, the **1.5×/2.0× MSD half-season game boosts**, and leftover **old-PVC bits** (`draftval`, the legacy `realized_cv` panel curve) beyond the ruck cap you kept (now 1.4×). Position is currently spread across **eight-ish names** (`pos`, `_pos_now`, `_fut`, `grp`, `gf`/`gfut`, `futblend`, `cpos`, `sw`) that all derive from just two facts. The cleanest single-source shape: **one row per player keyed by ID**, with exactly **two position columns — present and drafted** — plus the raw `_fut` weights retained as-is, and every synthetic credit/phantom either promoted to an explicit, labelled adjustment or removed.
