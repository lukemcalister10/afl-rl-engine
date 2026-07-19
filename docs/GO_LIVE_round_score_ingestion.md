# GO-LIVE RUNBOOK — ROUND-SCORE INGESTION
> **VERSION NOTE (item 369): the "v2.9 bake" reference below is historical — read as THE CURRENT CHAPTER'S bake, now v2.11 (BAKE_RUNBOOK_v2_11). The gating principle is unchanged: go-live is the final switch, thrown on the owner's word AFTER the bake ships.**
### Documentation, not activation. This page describes the LATER owner-worded job that turns weekly
### ingestion ON. The provision job (this module) ships with the switch OFF and writes nothing.

## STATUS TODAY (provision only)
- The plumbing is built and dry-run-proven: `engine/rl_after/ingestion/`
  (`round_score_parser.py`, `score_ingestor.py`, `dry_run_proof.py` + `PROOF.md`/`proof.json`).
- The **APPLY SWITCH IS OFF** and the store-write path is **deliberately absent**. `apply()` raises
  `IngestionGatedError` today; even a flipped switch cannot write because there is no write code.
- Nothing has been written to the single source (`engine/rl_after/rl_model_data.json`). Board and
  book are untouched. Expected board movers from this provision job: ZERO.
- OWNER RULING (register v25): live weekly ingestion is the **FINAL** switch, thrown AFTER the v2.9
  batch lands and the reads are mostly landing. Do not go live before then.

## THE SWITCH (two halves, both default OFF)
1. **Code half** — `APPLY_DEFAULT` in `score_ingestor.py` (currently `False`).
2. **Env half** — `INGEST_SCORE_APPLY` (currently unset).
`apply()` refuses unless BOTH are on. This is a deliberate belt-and-braces gate so no stray env
var and no stray code edit can each, alone, arm a store write.

## WHAT THE GO-LIVE JOB MUST BUILD (not present today, by design)
The provision job stops at the validated PREVIEW. The go-live job must add, behind the switch:
1. **The store-write** — apply the preview's `merged_entry` per player to the single source,
   under the FIVE SSI guards (SINGLE_SOURCE_INVARIANT.md): one writable source, source-hash
   re-stamp of every derived artifact, lookalike tripwire, correction-sticks canary, and the
   boot-store assertion. NO second copy of the store — edit the source in place, then regenerate
   board/book/matrices as derived read-only artifacts.
2. **Idempotency / dedup ledger** — a per-(player, season, round) record so a re-sent weekly feed
   cannot double-count. The `duplicate_round` anomaly catches in-feed repeats; the ledger catches
   across-feed repeats (a round already applied). REQUIRED before any real merge.
3. **Owner serialization confirmation** — confirm the exact on-disk weekly format (the parser
   accepts CSV and JSON of `player, round, score, played[, club]`; the owner may pin a specific
   column set / delimiter). Update the parser's aliases if the owner's export differs.
4. **A round/season length sanity bound** — reject rounds beyond the season's real round count.

## FLIP ORDER (when the owner says go)
1. Land the go-live job's store-write + dedup ledger on a fresh branch; keep the switch OFF in code.
2. Run the dry-run proof (`python3 engine/rl_after/ingestion/dry_run_proof.py`) — expect PROOF PASS,
   exceptions 0, anomalies 0, byte-for-byte reproduction. A red here blocks go-live.
3. On a COPY-FREE dry run of the first real weekly feed: `preview(rows)` and eyeball
   `preview.exceptions` (must be empty or every name owner-explained) and `preview.anomalies`
   (each must be owner-cleared). Do NOT proceed with a non-empty exceptions list.
4. Set the code half (`APPLY_DEFAULT = True`) in the go-live commit; set the env half
   (`INGEST_SCORE_APPLY=<owner token>`) in the run environment only.
5. Apply ONE round. Assert the boot-store guard re-pins to the new store md5, the derived board
   regenerates, and the SSI correction-sticks canary is green.
6. Only then wire the recurring weekly loop.

## GUARD EXPECTATIONS AT GO-LIVE
- Boot-store (Guard 5) will change: the store md5 MOVES the moment a real round is applied. Re-pin
  `data/expected_boot.json` in the same commit as the write, exactly as the migration did. A moved
  store with an un-repinned boot pin must HALT the next script (that is the guard doing its job).
- Every derived artifact must carry the NEW source md5 (Guard 2). A stale stamp HALTS.
- The two-Max-Kings collision sentry must stay GREEN — a weekly feed for a collision name MUST
  carry the club (the resolver vetoes on `affl_team`); an `ambiguous` exception is the correct,
  loud refusal, never a guess.

## FIRST-ROUND CHECKLIST (the first live weekly round)
- [ ] Owner confirms the feed's serialization matches the parser (or parser aliases updated).
- [ ] `preview.exceptions` empty (every named player resolves to a stable id) — else STOP and
      hand the named exceptions list back to the owner; never fuzzy-attach.
- [ ] `preview.anomalies` empty or each owner-cleared (duplicate round / impossible score /
      retired / cycle-year per item 13).
- [ ] Merge semantics confirmed: a single-round feed uses `merged_entry` (before + this round);
      a full-season reload uses `batch_entry`. Pick the intended one explicitly.
- [ ] Dedup ledger records the applied (player, season, round) set.
- [ ] Boot pin re-pinned; board/book regenerated; SSI guards 1–5 green from a fresh bootstrap.
- [ ] Board movers reviewed by the owner (weekly scores WILL move value — that is the point; it is
      no longer a zero-mover job once the switch is on).

## SCOPE FENCE (unchanged from the provision directive)
Ingestion writes SCORES into the store's `scoring` arrays only. It never touches valuation logic,
the PVC/curve, rl_export, or the UI. Pricing changes from new scores flow through the existing
engine unchanged — the ingestion boundary adds data, it does not price.
