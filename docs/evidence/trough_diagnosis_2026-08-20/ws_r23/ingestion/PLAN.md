# PLAN — ROUND-SCORE INGESTION (PROVISION ONLY, SWITCH OFF)
### Directive: ROUND-SCORE INGESTION, PROVISION ONLY — v1 · 2026-07-12 · TIER 2 · OPUS
### First committed artifact (MODE: auto). Branch: claude/round-score-ingestion-x0rclk

## BASE (verified this seat, FULL-URL ls-remote)
- main == `f110721f` (directive base; matches) · tag v2.8 == `9bd0cfd` (ALWAYS; matches)
- boot-store == `b0c39d78` (Guard 5 pinned; matches) · resolver `id_resolver.py` md5 `dc963af5`
- FEED read: DECISIONS v95 · CONSTRAINTS v1.7 + acceptance v1.7 · OPEN_ITEMS_REGISTER v25
  (PROVISION-NOW/INGEST-LAST ruling + item 13 cycle law) · id_resolver.py (the boundary).

## WHAT THIS JOB IS / IS NOT
BUILD the plumbing for weekly round-score ingestion with the APPLY SWITCH OFF. It parses the
owner's weekly format, resolves names to stable IDs at the score boundary, and emits a VALIDATED
PREVIEW of the exact `scoring` appends it WOULD make — plus anomaly checks. It writes NOTHING to
the store/board. LIVE ingestion is a later owner-worded job that flips the switch.

## THE DATA FACTS (from the store + engine, read-only)
- Single source: `engine/rl_after/rl_model_data.json` (SSI — never copied, never hand-edited).
- Each player row carries `scoring`: a list of SEASON aggregates `{year, avg, games}`.
  Weekly rounds roll UP into these: a round adds a data point that updates the CURRENT season's
  `{avg, games}`. Ingestion's unit of append is therefore a season-entry upsert.
- `games` on a season entry = count of rounds the player PLAYED that season; `avg` = mean score
  over PLAYED rounds. The weekly "games flag" is exactly the played/no-played bit per round.
- BASE_REF / live season = 2026 (rl_model.py:57). 626 store rows carry a played-2026 entry.
- Identity boundary: `id_resolver.IdResolver.resolve(name[, club])` → Resolution with status
  RESOLVED/BY_KEY (single stable id) | NO_ID (row, no stable id) | AMBIGUOUS (name collision,
  candidates) | UNRESOLVED (no row). It NEVER collapses a genuine collision (two Max Kings law).

## THE SCHEMA (discoverable from the directive's four named fields + the store target)
Owner's weekly format = **name · round · score · games flag** (directive step 1). The four fields
map cleanly, so the format IS discoverable — no STOP-and-ask. The exact on-disk serialization is
the provision-builder's choice, CONFIRMED with the owner at go-live (flagged in the runbook).
Proposed canonical row (CSV header or JSON list-of-objects, both accepted):

    player      (str)   the player's name as the owner writes it
    round       (int)   round number within the season (1..N)
    score       (num)   that round's rating/fantasy score (only meaningful when played)
    played      (0/1)   the "games flag": 1 = played that round, 0 = named-but-did-not-play
    club        (str, OPTIONAL) disambiguator; passed to the resolver as a VETO, never a guess

Season year is a pipeline CONTEXT (default 2026 = BASE_REF), not a per-row field — the weekly feed
is implicitly the current season. `club` is optional and only ever NARROWS resolution (the store's
`affl_team` is placeholder-ish in this dataset, so club must never be required to attach a score).

## MODULE LAYOUT (engine-adjacent — FENCE IN)
    engine/rl_after/ingestion/
      __init__.py
      PLAN.md                 <- THIS FILE (first artifact)
      round_score_parser.py   <- parse CSV/JSON weekly feed -> validated RoundScore rows
      score_ingestor.py       <- parse -> resolve -> aggregate -> PREVIEW; anomalies; apply GATED OFF
      dry_run_proof.py        <- read-only proof: store season -> synth rounds -> preview == store
      PROOF.md / proof.json   <- committed dry-run proof output
    docs/GO_LIVE_round_score_ingestion.md   <- the go-live runbook (FENCE IN: "the runbook")

## RESOLVER WIRING + EXCEPTIONS (step 2 — FAIL LOUDLY, never guess/fuzzy-attach)
For each parsed row, call the resolver. Outcome routing:
- RESOLVED / BY_KEY  → attach {stable_player_id, key}; row is INGESTABLE.
- NO_ID              → EXCEPTION `no_stable_id` (row exists but no durable id — cannot key a write).
- AMBIGUOUS          → EXCEPTION `ambiguous` (list candidates; owner/club must disambiguate).
- UNRESOLVED         → EXCEPTION `unresolved` (unknown name).
Every non-ingestable row lands in a NAMED EXCEPTIONS LIST with its reason and the raw input. The
pipeline NEVER fuzzy-matches and NEVER picks a candidate on its own.

## PREVIEW / APPLY SPLIT (step 3 — SSI-safe)
- PREVIEW ARTIFACT: for each resolved player, the exact resulting `scoring` season entry (the
  append/upsert it WOULD make) rendered as a DIFF (before → after), keyed by stable id. This is a
  diff artifact, NOT a store and NOT a store copy.
- ANOMALY CHECKS on the preview (each flags, never silently drops):
  - duplicate round     : same (player, round) twice in the feed, or a round already reflected.
  - impossible score    : played round with score outside a documented sane band (config bound).
  - retired / out-of-universe : resolved row has `_retired` True (or not a live player).
  - cycle-year sanity   : per item 13 — the season year must be >= the player's debut year
    (`debut(p)`: MSD debuts draft-year, all others year+1); a score before debut is impossible.
- APPLY: hard-gated OFF. Guard = env `INGEST_SCORE_APPLY` (default unset) **and** code
  `APPLY_DEFAULT = False`. When not enabled, `apply()` raises `IngestionGatedError`. Even if the
  switch were flipped, the store-write itself is DELIBERATELY NOT IMPLEMENTED in this job (raises
  `NotImplementedError` pointing at the runbook) — so this job contains ZERO store-write code, by
  construction. Flipping AND implementing the write is the future owner-worded go-live job.

## DRY-RUN PROOF (step 4 — commit it)
Read-only. Pick players with a played-2026 store season entry. For each, synthesize `games` round
rows (round 1..games, score = the store's own season `avg`, played=1) — a faithful reconstruction
whose mean is the stored `avg` and whose played-count is the stored `games`. Run parse → resolve →
preview and ASSERT the previewed season entry reproduces the store's `{year, avg, games}`
byte-for-byte AND the exceptions list is empty. Prove across a broad sample (all 626), report a
named worked example, and honestly disclose that flat rounds are a reconstruction (the plumbing,
not round variance, is what's under proof). Commit PROOF.md + proof.json.

## GO-LIVE RUNBOOK (step 5 — documentation, not activation)
One committed page: the exact owner-worded flip order, guard expectations, and first-round
checklist to turn ingestion on later. States what the future job must add (the store-write behind
the switch) and the confirm-the-serialization-with-owner step.

## FENCE / EXPECTED MOVERS
IN: new ingestion module files · dry-run proof · runbook. OUT: any store/board/gate/data write ·
valuation logic · rl_export/UI · docs-pack authoring · flipping the apply switch. No existing file
that the engine imports is touched → EXPECTED BOARD MOVERS = ZERO (any mover = automatic STOP).

## VERIFICATION BEFORE PUSH
- `git status` shows ONLY new files under ingestion/ + the runbook (no engine/store/board edits).
- Run dry-run proof green (byte-for-byte, empty exceptions).
- Confirm `apply()` refuses with the switch off (and refuses to write even if toggled).
- Boot-store still `b0c39d78`; resolver unchanged.
