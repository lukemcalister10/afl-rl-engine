# DIRECTIVE — GO-LIVE STORE-WRITE (WEEKLY INGESTION APPLY) · seat 14 · 2026-07-19
### PARALLEL background job (owner: "in the background, get the weekly loop working"). The ingestion
### PLUMBING (parse→resolve→aggregate→PREVIEW) exists at engine/rl_after/ingestion/, but the APPLY /
### store-write is deliberately absent (apply() raises IngestionGatedError; no write code). Build the
### write — BEHIND the existing double-OFF gate — so a submitted round can be applied to the store ONE
### round at a time and the board regenerates. Spec: docs/GO_LIVE_round_score_ingestion.md
### ("WHAT THE GO-LIVE JOB MUST BUILD"). NOTHING is written to the real store in this build.

## THE JOB (PLAN FIRST)
0. **GREEN-BOOT PRE-STEP (base 3055ea5 has STALE engine pins — item 399; without this you HALT on
   Guard 5 the moment you dry-run or regen):** before any engine load, re-stamp data/expected_boot.json's
   TWO engine pins to the VERIFIED engine md5s (`rl_model → cc626d7d`, `engine_head → 904722cd` — md5 the
   engine files FIRST to confirm, same as the parallel bake) so Guard 5 / bootstrap is GREEN for your
   tests. BYTE-IDENTICAL to the bake's re-stamp (reconciles cleanly); ONLY these two pins; every other pin
   byte-unchanged. This is NOT your deliverable — the apply()+ledger is — it just unblocks your boot.
1. **STORE-WRITE** — implement apply(): merge the validated preview's per-player round entry into the
   SINGLE SOURCE (engine/rl_after/rl_model_data.json) IN PLACE (never a copy), under ALL FIVE SSI GUARDS
   (SINGLE_SOURCE_INVARIANT.md), then regenerate board/book as derived read-only artifacts + re-stamp
   expected_boot.json (source-hash). Keep BOTH gate halves default-OFF (APPLY_DEFAULT=False + env
   INGEST_SCORE_APPLY unset) — belt-and-braces, no accidental arm.
2. **DEDUP LEDGER** — a per-(player, season, round) record so a re-sent round can't double-count
   (across-feed repeats; the existing duplicate_round anomaly covers in-feed). REQUIRED before any real merge.
3. **SEASON BOUND** — reject rounds beyond the real season round count.
4. **FORMAT** — keep the parser's CSV/JSON `player,round,score,played[,club]`; the owner confirms his
   exact export columns/delimiter at go-live (update aliases then if needed) — do NOT block on it now.
5. **PROVE (gate OFF, no real-store write):**
   - Existing dry-run: `python3 engine/rl_after/ingestion/dry_run_proof.py` → PROOF PASS, 0 exceptions,
     0 anomalies, byte-for-byte.
   - APPLY DRY-RUN on a SCRATCH COPY of the store with a synthetic round-15 feed: show the write+regen
     produces a coherent updated board AND the dedup ledger BLOCKS a re-sent round-15.
   - **SINGLE-ENV STABILITY** (the owner's actual use — one-by-one submission on one setup): run the
     apply+regen 5× on THIS container with ONE stated env (the shipping default) each run; assert the
     updated board is BYTE-STABLE run-to-run. (Cross-machine reproducibility is a SEPARATE item — do not
     attempt to solve it here; just confirm single-env stability.)

## GIT ENTRY: base = `3055ea5` (#123) STRICT (PARALLEL to the bake, CONFLICT-FREE: both re-stamp
`expected_boot.json`'s 2 engine pins to the SAME verified values cc626d7d/904722cd (git reconciles
identical changes cleanly); otherwise disjoint — this = `engine/rl_after/ingestion/` + a ledger, the
bake = `build_board.sh`). Stack on #123; this branch REBASES onto the baked v2.11 head before go-live.
THREADS=1. Read SINGLE_SOURCE_INVARIANT.md first.
## EFFORT: High (it is the SINGLE-SOURCE WRITE path — the highest-care code; the gates + dedup + SSI
re-stamp must be airtight). MODE: auto, PLAN first. TIME: a real build — NO promised clock. FENCE:
IN = engine/rl_after/ingestion/ + the dedup ledger file + data/expected_boot.json (the 2 engine pins,
Pre-Step 0 ONLY — identical to the bake's) + session_2026-07-19/storewrite/. HARD-OUT:
the pricing/value logic, the curve, the model (apply MERGES scores then REGENERATES; it never touches
pricing), docs, and the REAL store (gate stays OFF; scratch copies only). HALT on any HARD-OUT need.
## EXIT (≤25 lines): the dry-run PROOF + the scratch-apply demo (round-15 → updated board; dedup blocks
re-send) + the 5× single-env stability result + gates-OFF confirmation; branch · head SHA · PR (its own,
report-only, DO-NOT-MERGE until go-live). SILENCE IS A RED · halt-not-warn.
