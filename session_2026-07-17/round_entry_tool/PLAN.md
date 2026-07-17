# PLAN — THE ROUND-ENTRY TOOL (resolver + preview + stamped snapshots; DRY-RUN ONLY)
### Directive: DIRECTIVE_ROUND_ENTRY_tool_2026-07-17 · item-305 frame · EFFORT Medium · MODE auto
### First committed artifact after FIRST_COMMANDS_PROOF. Branch: claude/round-entry-tool-zvh7vw

## BASE (verified this seat, FULL-URL ls-remote — see FIRST_COMMANDS_PROOF.txt)
- main == `0339e373` · AT-OR-AFTER base `4848f80`; `4848f80..0339e373` = docs/-ONLY (3 files) ✓
- ANCESTOR-PROOF-PASS ✓ · module `engine/rl_after/ingestion/` present ✓ · gate present,
  `APPLY_DEFAULT False`, `IngestionGatedError` ✓ (write path ABSENT BY DESIGN)
- boot store `b1fd0bce` (Guard 5 pinned) · board `data/rl_build/rl_app_data.json` md5 `790136a3`
- FEED read: register items **305** (THE LAW — supersedes 303's identity para) + 297 (dial deferral)
  · docs/GO_LIVE_round_score_ingestion.md · docs/SINGLE_SOURCE_INVARIANT.md (v1.3) · CONSTRAINTS
  (context) · the existing module (`round_score_parser.py`, `score_ingestor.py`, `id_resolver.py`,
  `dry_run_proof.py`).

## WHAT THIS JOB IS / IS NOT
BUILD the owner-facing ROUND-ENTRY TOOL on top of the existing provision plumbing: a thin CLI that
takes a pasted/`.csv` FootyWire weekly `name,score` body + `--round N`, EXACT-matches each name to a
live active `stable_player_id`, flags every non-clean name as a one-tap RESIDUE line, and emits a
per-round SSI-conformant stamped snapshot (the week-to-week UI value-line feed). It writes NOTHING
to the single source: the store is READ-ONLY at run time and the store-WRITE code stays ABSENT
(go-live is a separate owner-worded job). EXPECTED BOARD MOVERS: ZERO.

## THE LAW (item 305, owner ground-truth — carried VERBATIM in the module docstring)
Input of record: a FootyWire weekly export, `name, score`, names identical to the DB, CURRENT
players only. Owner workflow PRESERVED: paste round + name + score (a 2-minute job); unique IDs NOT
required. The resolver EXACT-matches name → active-stable-ID over the LIVE active pool read at RUN
TIME (new-intake IDs picked up automatically). The real failure mode is a SILENT MISS, not a clash:
any export name that does not cleanly resolve is a FLAGGED RESIDUE LINE for a one-tap owner confirm
— NEVER a silent drop, NEVER attached to the wrong row, NEVER a new-row invention. A scoring player
not yet in the DB is residue (ask), never a guess.

## THE ACTIVE POOL (defined from the store, read-only)
- Active pool = store rows with a `stable_player_id` AND NOT `_retired`. Measured this seat: 2652
  rows total → **804 active** (804 with id; 1848 retired == every id-less row). 625 of the 804 carry
  a played-2026 entry. Retirees carry NO stable id here, so they are naturally out of the pool.
- Active name-collisions in the LIVE pool = **ZERO** today (matches item 305: the one live clash,
  the Max Kings, has neither player active). So fixture (d)'s clash is SYNTHETIC by necessity.
- Normalisation = the engine's `id_resolver._norm` (unidecode + lower + a-z/space + collapse) —
  case/whitespace-insensitive EXACT, no fuzzy auto-attach. Reused, never re-implemented, never edited.

## MODULE LAYOUT (FENCE IN)
    engine/rl_after/ingestion/
      round_entry.py                 <- NEW library: ActivePoolResolver · name,score parse ·
                                        enter/confirm · residue read/write · stamped snapshot builder
      round_entry_fixture_proof.py   <- NEW: the 5 fixtures + no-write + determinism proofs (script-
                                        emitted counts, exit codes; SILENCE IS A RED)
      README.md                      <- NEW (engine-side module README; step 6)
    tools/round_entry/               <- NEW thin CLI (mirrors tools/seat house style)
      round_entry.py                 <- argparse CLI: `enter` · `confirm` · `show`
      __init__.py
      samples/                       <- committed sample CLI output (green run)
    session_2026-07-17/round_entry_tool/
      FIRST_COMMANDS_PROOF.txt       <- committed (first commit)
      PLAN.md                        <- THIS FILE
      fixtures/                      <- synthetic pools + feed bodies (committed inputs)
      proofs/                        <- committed proof output (counts + exit codes)

OUT (untouched): the SOURCE STORE (read-only run time; write path ABSENT) · docs/ · every Leg-D
fence file · `rl_model.py` · UI code · `id_resolver.py`/`round_score_parser.py`/`score_ingestor.py`
(imported READ-ONLY; not modified — zero-mover guarantee). A need outside the fence ⇒ HALT-and-ask.

## THE FIVE TASKS
1. **RESOLVER** (`ActivePoolResolver`): read store at run time → build norm-name → [active rows]
   index over the active pool only. `resolve(name)` → RESOLVED (single active exact: stable_id·key·
   canonical name) | AMBIGUOUS (≥2 active exact: BOTH candidates) | RESIDUE (none: nearest candidates
   via `difflib` for the one-tap confirm). No fuzzy auto-attach — a near-miss is residue WITH names.
2. **ENTRY PATH** (`enter --round N` + body): parse `name,score` (CSV w/ or w/o header, or pasted
   lines; both accepted). Resolve each. Write PREVIEW (resolved rows) + RESIDUE file (if any). Clean
   round (no residue) → snapshot written immediately. Idempotent per round: re-`enter` REPLACES that
   round's preview/residue/snapshot LOUDLY, never duplicates.
3. **RESIDUE CONFIRM LOOP**: residue file human-first — one block per unresolved/ambiguous name, its
   candidate(s), and a single `ACTION:` the owner edits (a candidate number, or `skip`). `confirm
   --round N` consumes the edited file: pick→resolved row, skip→recorded drop. A blank/invalid ACTION
   ⇒ REFUSE loudly (SILENCE IS A RED). NOTHING enters a snapshot unresolved; only confirm writes the
   snapshot for a round that had residue.
4. **STAMPED SNAPSHOTS** (SSI-conformant, derived/read-only/disposable): JSON carrying round ·
   season_year · resolved rows (sorted by key) · `source_store_md5` at generation · `module_code_md5`
   · `generated_at`. Deterministic serialization (sort_keys, fixed indent, ensure_ascii). Determinism
   check: regen from identical inputs (incl. a pinned `generated_at`) is BYTE-IDENTICAL — committed.
5. **PROOFS** (committed, script-emitted counts + exit codes): (a) clean round · (b) misspelled →
   residue → confirmed · (c) unknown/not-in-DB → residue → skip · (d) SYNTHETIC two-active-exact
   clash → residue with BOTH candidates · (e) idempotent re-entry replaces. NO-WRITE: `apply()` still
   raises `IngestionGatedError` (invoked, raised error committed) · real store md5 UNCHANGED
   (`b1fd0bce`) before/after the whole suite · board md5 UNCHANGED (`790136a3`) · plus the snapshot
   determinism check. One harness, non-zero exit on any red.
6. **MODULE README** (engine side): the commands, the residue loop, the snapshot format, and the line
   "the write path is absent by design; go-live is a separate owner-worded job (GO_LIVE runbook)."

## SNAPSHOT FORMAT (documented in README; UI wiring later)
    {"kind":"round_entry_snapshot","round":N,"season_year":2026,"generated_at":<iso>,
     "source_store_md5":<8hex>,"module_code_md5":<8hex>,
     "resolved":[{"stable_player_id":..,"key":..,"name":..,"score":..,"via":"exact|confirm"}],
     "skipped":[{"name":..,"score":..,"reason":"owner-skip"}],
     "counts":{"resolved":..,"skipped":..,"residue_open":0}}
`module_code_md5` = md5 over `round_entry.py` ⊕ `id_resolver.py` (the behaviour-defining code).
`generated_at` is an explicit input to the builder (CLI passes wall-clock; the determinism check
pins it) so "same inputs → byte-identical" is honest, stamps included.

## VERIFICATION BEFORE PUSH
- `git status` shows ONLY new files under `engine/rl_after/ingestion/`, `tools/round_entry/`, and the
  session dir. No store/board/gate/engine edits.
- All five fixture proofs GREEN + the three no-write proofs + determinism check GREEN (exit 0).
- Real store still `b1fd0bce`; board still `790136a3`; `id_resolver.py` byte-unchanged.
- `apply()` still raises `IngestionGatedError` (committed).
