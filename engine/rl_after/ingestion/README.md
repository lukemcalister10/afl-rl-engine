# `engine/rl_after/ingestion/` — the round-score ingestion module

Two things live here, both **DRY-RUN ONLY**. Nothing in this directory writes the single source
(`engine/rl_after/rl_model_data.json`). The store-**write** path is **absent by design**; go-live is
a separate owner-worded job (`docs/GO_LIVE_round_score_ingestion.md`).

1. **The provision plumbing** — `round_score_parser.py` · `score_ingestor.py` · `dry_run_proof.py`
   (+ `PROOF.md`/`proof.json`). Parses a weekly feed, resolves names to stable IDs, and emits a
   validated PREVIEW of the `scoring` appends it *would* make. `apply()` is hard-gated OFF.

2. **The round-entry tool** — `round_entry.py` (library) + `round_entry_fixture_proof.py` (proofs),
   driven by the thin CLI at `tools/round_entry/round_entry.py`. This is the owner's 2-minute weekly
   workflow: paste a `name,score` body + a round number → resolved rows + a stamped snapshot.

---

## THE ROUND-ENTRY TOOL

### The law it obeys (register item 305, owner ground-truth — verbatim in `round_entry.py`)
> Input of record: a FootyWire weekly export, `name, score`, names identical to the DB, CURRENT
> players only. The owner's workflow is PRESERVED: paste round + name + score — a 2-minute job;
> unique IDs are NOT required and not asked for. The resolver exact-matches name → active-stable-ID
> over the LIVE active pool read at RUN TIME (new-intake IDs picked up automatically the moment they
> enter the DB). The real failure mode is a SILENT MISS, not a clash: any export name that does not
> cleanly resolve is a FLAGGED RESIDUE LINE for a one-tap owner confirm — NEVER a silent drop, NEVER
> attached to the wrong row, NEVER a new-row invention. A scoring player not yet in the DB is residue
> (ask), never a guess.

### The active pool
The resolver reads the store **at run time** and considers only the **active pool**: rows with a
durable `stable_player_id` that are **not** `_retired` (804 today). New-intake IDs are picked up the
moment they enter the DB; retirees drop out automatically. Matching is the engine's own
normalisation (`id_resolver._norm`: unidecode + lowercase + a–z/space + collapse) — **case/whitespace
EXACT, no fuzzy auto-attach.**

### The commands

```
# 1) enter a round's paste (stdin) or a .csv
printf 'name,score\nErrol Gulden,124\nNic Daicoss,101\n' \
  | python3 tools/round_entry/round_entry.py enter --round 12
# ...or:  round_entry enter --round 12 --body-file week12.csv
```

- Every name that resolves to exactly one active player is attached (`stable_player_id · key · score`).
- A **clean** round (no residue) writes the stamped **snapshot** immediately.
- Any name that does **not** cleanly resolve is written to a human-first **residue file** and NO
  snapshot is written (nothing enters a snapshot unresolved).
- Re-running `enter` for a round **REPLACES** that round's artifacts loudly — idempotent, never
  duplicated.

```
# 2) the owner edits the residue file (ONE edit per block), then:
python3 tools/round_entry/round_entry.py confirm --round 12
# 3) inspect:
python3 tools/round_entry/round_entry.py show --round 12
```

### The residue confirm loop
The residue file is human-first: one block per unresolved/ambiguous name, its candidate(s), and a
single `ACTION:` line the owner edits — a **candidate number** to attach the score to that player, or
`skip` to drop the line. Example block:

```
[1] UNRESOLVED  name='Nic Daicoss'  score=101.0
    ACTION:                      <- put a number (1/2/…) or `skip`
    candidates:
      1) Nick Daicos           key=nick-daicos    id=afl-player-v1-…   (near-match 0.90)
      2) Josh Daicos           key=josh-daicos    id=afl-player-v1-…   (near-match 0.62)
```

`confirm` consumes the edited file: a number → a confirmed resolved row (`via: confirm`); `skip` → a
recorded drop (`reason: owner-skip`). A **blank or invalid ACTION is refused loudly** (non-zero exit)
— nothing is guessed, nothing enters the snapshot unresolved. A genuine two-active-exact clash shows
**both** candidates as `AMBIGUOUS`; the owner chooses, the tool never collapses it.

### The snapshot format (the week-to-week UI value-line feed; UI wiring later)
Snapshots are **DERIVED** artifacts under the Single-Source Invariant: read-only, source-stamped,
disposable. One JSON file per round:

```json
{
  "kind": "round_entry_snapshot",
  "round": 12,
  "season_year": 2026,
  "generated_at": "2026-07-17T09:00:00Z",
  "source_store_md5": "b1fd0bce",
  "module_code_md5": "1c11615e",
  "resolved": [
    {"stable_player_id": "afl-player-v1-…", "key": "errol-gulden",
     "name": "Errol Gulden", "score": 124.0, "via": "exact"}
  ],
  "skipped": [{"name": "Rookie Notindb", "score": 63.0, "reason": "owner-skip"}],
  "counts": {"resolved": 1, "skipped": 1, "residue_open": 0}
}
```

- `source_store_md5` — md5 of the single source at generation time (the SSI source stamp).
- `module_code_md5` — md5 of the behaviour-defining code (`round_entry.py` ⊕ `id_resolver.py`).
- `generated_at` — an explicit input to the builder, so **regenerating from identical inputs is
  byte-identical** (the determinism check pins it; the CLI passes wall-clock).
- `resolved` is sorted by `key`; serialization is `sort_keys`+fixed-indent+ascii. Identity is the
  **stable ID**; the name is display only.

### Proofs
`python3 engine/rl_after/ingestion/round_entry_fixture_proof.py [--write]` — the five fixtures
(clean · misspelled→confirmed · unknown→skip · synthetic two-active clash · idempotent re-entry) plus
the no-write proofs (`apply()` still raises `IngestionGatedError`; the real store and board md5 are
byte-unchanged and match their pins) and the snapshot determinism check. Every count is
script-emitted; non-zero exit on any red (**SILENCE IS A RED**). Committed evidence:
`session_2026-07-17/round_entry_tool/proofs/`.

### Scope fence
This tool reads the store READ-ONLY and writes only derived snapshots. It does **not** touch
valuation, the board, the ladder, `rl_model.py`, or the UI. **The write path is absent by design;
go-live is a separate owner-worded job (`docs/GO_LIVE_round_score_ingestion.md`).**
