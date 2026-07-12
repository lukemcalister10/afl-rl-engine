# DRY-RUN PROOF — round-score ingestion plumbing

Directive step 4. READ-ONLY replay of the store's own scoring arrays through
parse -> resolve -> preview. Regenerate: `python3 dry_run_proof.py`.

## RESULT: **PROOF PASS**

| field | value |
|---|---|
| proof season | 2026 |
| store md5 | `b0c39d78` |
| players sampled | 625 |
| byte-for-byte reproduced | 625 |
| failed | 0 |
| resolve exceptions (sampled) | 0 |
| anomalies tripped (sampled) | 0 |

## WORKED EXAMPLE
```json
{
  "byte_for_byte": true,
  "feed_rounds": 12,
  "key": "willem-duursma",
  "player": "Willem Duursma",
  "preview_batch_entry": {
    "avg": 86.4,
    "games": 12,
    "year": 2026
  },
  "stable_player_id": "afl-player-v1-0eb1e4c909a009f45d6e",
  "store_entry": {
    "avg": 86.4,
    "games": 12,
    "year": 2026
  }
}
```

## WHAT THIS PROVES
- Names resolve to the correct `stable_player_id`/store key at the boundary (exceptions list empty across all 625 sampled players).
- The aggregator reproduces each known season append **byte-for-byte** (`{year,avg,games}` identical to the store).
- Flat, single-appearance rounds trip no anomaly (duplicate/impossible/cycle/retired).

## HONEST SCOPE
- Per-round scores are flat (== the season avg): the store holds no round-level variance to replay. This exercises the PLUMBING, not round-to-round variance.
- avg reproduces byte-for-byte because the aggregator rounds to the store's own 2dp (verified: every stored avg == round(avg,2)).
- Retirees carry no stable id in this store, so a named retiree is caught at the *exception* layer (`no_stable_id`); the `retired` *anomaly* is forward-safe defense.
