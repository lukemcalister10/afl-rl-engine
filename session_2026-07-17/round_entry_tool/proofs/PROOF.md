# ROUND-ENTRY TOOL — DRY-RUN FIXTURE PROOFS

Directive step 5. READ-ONLY. Every count script-emitted. Regenerate:
`python3 engine/rl_after/ingestion/round_entry_fixture_proof.py --write`.

## RESULT: **PROOF PASS** (32/32 checks)

| immutability | before | after | pinned |
|---|---|---|---|
| real store md5 | `b1fd0bce` | `b1fd0bce` | `b1fd0bce` |
| real board md5 | `790136a3` | `790136a3` | `790136a3` |

- **apply() raised:** `round-score APPLY is OFF (APPLY_DEFAULT=False, env INGEST_SCORE_APPLY unset). This provision job writes nothing to the store; go-live is a separate owner-worded job.`
- **determinism** (byte-identical snapshot regen) md5: `770a4b63`
- **module_code_md5:** `1c11615e`

## CHECKS
| # | check | verdict | detail |
|---|---|---|---|
| 1 | a.resolved==3 | PASS | resolved=3 |
| 2 | a.residue==0 | PASS | residue=0 |
| 3 | a.snapshot.counts | PASS | {"residue_open": 0, "resolved": 3, "skipped": 0} |
| 4 | a.retired-excluded (pool=6 not 7) | PASS | active_pool=6 |
| 5 | b.residue-file-written | PASS |  |
| 6 | b.1-exact-1-residue | PASS | resolved=1 residue=1 |
| 7 | b.near-candidates-list-Nick-Daicos | PASS | candidates=['Nick Daicos', 'Josh Daicos'] |
| 8 | b.reason==unresolved | PASS |  |
| 9 | b.confirmed.counts | PASS | {"residue_open": 0, "resolved": 2, "skipped": 0} |
| 10 | b.one-exact-one-confirm | PASS | vias=['confirm', 'exact'] |
| 11 | b.confirmed-row-is-Nick-Daicos-key | PASS |  |
| 12 | c.1-exact-1-residue | PASS | resolved=1 residue=1 |
| 13 | c.unknown-name-in-residue | PASS |  |
| 14 | c.skip.counts | PASS | {"residue_open": 0, "resolved": 1, "skipped": 1} |
| 15 | c.skipped-is-the-unknown | PASS |  |
| 16 | c.unknown-NOT-in-resolved | PASS |  |
| 17 | d.no-auto-resolve | PASS | resolved=0 |
| 18 | d.one-residue-line | PASS | residue=1 |
| 19 | d.reason==ambiguous | PASS | reason=ambiguous |
| 20 | d.BOTH-candidates-shown | PASS | candidates=2 |
| 21 | d.both-active-exact-keys | PASS | keys=['sam-clash-a', 'sam-clash-b'] |
| 22 | d.both-kind-active-exact | PASS |  |
| 23 | e.first-entry-2-resolved | PASS | resolved=2 |
| 24 | e.re-entry-announces-REPLACING | PASS | cli said REPLACING |
| 25 | e.replaced-not-merged | PASS | keys=['zak-butters'] |
| 26 | e.single-snapshot-no-dup | PASS | snapshot files=['round_5.snapshot.json'] |
| 27 | nw.apply-raises-IngestionGatedError | PASS | round-score APPLY is OFF (APPLY_DEFAULT=False, env INGEST_SCORE_APPLY unset). Th |
| 28 | det.byte-identical | PASS | md5 770a4b63 == 770a4b63 |
| 29 | nw.store-md5-unchanged | PASS | b1fd0bce -> b1fd0bce |
| 30 | nw.store-md5==pinned | PASS | b1fd0bce (pin b1fd0bce) |
| 31 | nw.board-md5-unchanged | PASS | 790136a3 -> 790136a3 |
| 32 | nw.board-md5==pinned | PASS | 790136a3 (pin 790136a3) |

## WHAT THIS PROVES
- The resolver exact-matches over the LIVE active pool; retirees are excluded (fixture a).
- A misspelling is RESIDUE with the nearest active candidates, resolved only by the owner's
  one-tap pick — never a silent auto-attach (fixture b).
- A not-yet-in-DB scorer is RESIDUE and is skipped on the owner's word, never invented
  as a new row (fixture c).
- A genuine two-active-exact clash is AMBIGUOUS with BOTH candidates, never collapsed
  (fixture d — synthetic, because the live pool has zero active name-collisions).
- Re-entering a round REPLACES its artifacts loudly and never duplicates (fixture e).
- NO-WRITE: `apply()` still refuses; the real store + board md5 are byte-unchanged and
  match their pins; snapshot regeneration is byte-identical.

## SCOPE
- Fixtures a–e run on committed SYNTHETIC pools (`fixtures/pool_*.json`) for determinism
  and to construct the clash the live pool cannot supply. The immutability proofs run
  against the REAL single source and board.
- The store-write path is absent by design; go-live is a separate owner-worded job
  (docs/GO_LIVE_round_score_ingestion.md).

