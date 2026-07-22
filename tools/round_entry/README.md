# Weekly Updater — owner's local runbook

> **STATUS: live-scoring transaction core — proven end-to-end on scratch, store-write gate OFF.**
> The store-write gate is **OFF** and must stay OFF on the committed branch. This branch delivers the
> safe transaction core (staged apply, atomic swap, rollback, crash recovery, strong snapshot identity,
> fail-closed forward-valuation provenance) **plus** the live-scoring layer proven in
> `session_2026-07-20/live_scoring_two_round/`: persistent per-player **value + rank history**,
> post-commit **UI bundle refresh**, and a one-command owner path (`run`). Two consecutive rounds
> (R15 → R16) are proven across a full stop/restart, with duplicate / stale / tamper / universe
> protection and no partial writes. What is still open before real-owner go-live: **`correct` / `undo`**,
> season/round from release metadata, and the accepted-foundation's own stale `engine_head` / `rl_model`
> boot pins (a bake re-stamp, outside this workstream). See
> `session_2026-07-20/weekly_updater_hardening/DESIGN.md`.

One tool, one command, the whole job: place a `name,score` file, review the preview + any unresolved
names, and approve — the tool resolves names to live stable IDs, stamps a self-verifying snapshot,
applies it to the store (staged, validated, atomically swapped, with rollback + crash recovery),
records the persistent value + rank history, and refreshes the UI bundles. **No Python editing. The
real store write is gated OFF by default** (this build applies no real round).

## The one-command path

```
# place the FootyWire `name,score` export for the round as a file, then:
./weekly_update.sh run --round 15 --body-file round15.csv --approve
```

`run` resolves the round, prints a human-readable preview + unresolved-name report, requires an
EXPLICIT approval (`--approve`, or an interactive `yes`), then applies the exact snapshot and refreshes
the UI + history. If a name does not resolve, it stops and points you at the one-tap residue review
(a candidate number or `skip`); finish that with `confirm`, then `run --approve`.

## Catching up several rounds at once (`catchup`)

When you have several consecutive weekly files to apply (e.g. R15–R19), `catchup` does them in one
go — **one** preflight + **one** approval, but internally **every round is a separate sequential
transaction** committed in full before the next begins (never one combined update):

```
# put the round files in a folder (named so each contains its round, e.g. R15.csv … R19.csv):
./weekly_update.sh catchup --dir scores/ --approve
#   or list them explicitly:
./weekly_update.sh catchup --file 15=R15.csv --file 16=R16.csv … --approve
```

The consolidated **preflight** reports, per round: the file's SHA-256, the detected encoding
(CP1252 / UTF-8 with or without BOM are all read without altering names or scores), the listed/played
count, the legitimate listed-zero count, the absent/DNP count vs the active universe, every resolved
stable key, and the identity overrides applied. **It HALTS before the first write** on any unresolved
name, ambiguous name, or duplicate stable-key assignment — never a silent drop, never the wrong row.

**Participation is defined by file membership** (owner ruling): a listed player played (score appended,
+1 game); a listed score of **0 is a legitimate played zero** (+1 game, +0 to the average); an absent
player did not play (no score, no placeholder, no game, no carry-forward). Identity is resolved by
**stable key** — the owner override file (`engine/rl_after/ingestion/catchup_identity_overrides.json`)
carries the authorised disambiguations (the two Bailey Williams by round+score; Callum Brown →
`callum-brown-ire`), so each listed score reaches the correct record and the two Bailey Williams never
collapse.

`catchup` is **restart-safe**: if it stops partway, re-running it skips the already-committed rounds
(the dedup ledger) and resumes from the next unapplied round; a crash mid-commit is refused until
`recover`. Each round keeps its own store, board, hashes, ledger entry, transaction evidence, value /
overall-rank / positional-rank history, and a movers report (with the movement folded into the working
UI bundle). Proven end-to-end on the owner's real R15–R19 files in
`session_2026-07-20/live_scoring_catchup/`.

## Launch

| platform | command |
|---|---|
| Linux / macOS / WSL / Git-Bash | `tools/round_entry/weekly_update.sh <verb> ...` |
| native Windows | `tools\round_entry\weekly_update.bat <verb> ...` |

Both are thin wrappers over the Python CLI (`tools/round_entry/round_entry.py`); they set a portable,
deterministic environment (vendored `unidecode`, `PYTHONHASHSEED=0`, single-thread BLAS) and forward
your arguments. `python3` (or set `PYTHON=...`) must be on PATH with numpy/scipy/scikit-learn.

## The 2-minute workflow

```
# 1. paste the FootyWire `name,score` export for the round (CSV or pasted lines)
./weekly_update.sh enter   --round 15 --body-file round15.csv
#    (or pipe it:  cat round15.csv | ./weekly_update.sh enter --round 15 )

# 2. ONLY if `enter` flagged residue (a name that did not cleanly resolve):
#    edit the ACTION line in the printed residue file — a candidate NUMBER or the word `skip` —
#    then:
./weekly_update.sh confirm --round 15

# 3. inspect the EXACT stamped snapshot before touching anything
./weekly_update.sh show    --round 15

# 4. apply THAT EXACT snapshot (see "Applying for real" — gated OFF by default)
./weekly_update.sh apply   --round 15
```

`enter`/`confirm`/`show` **never** write the store. A name that does not resolve is a flagged
residue line for a one-tap confirm — never a silent drop, never the wrong row, never an invented row.
Nothing enters a snapshot unresolved.

## What a snapshot carries (self-verifying identity)

Each snapshot stamps: round + season, every resolved player's **stable ID** + **exact score**, the
**full** and short **source-store md5**, the **module/version identity**, and a **content hash** over
its own bytes. `apply` re-checks all of it and **refuses before any write** if:

- the live store moved since the snapshot was stamped (**stale**);
- the snapshot was edited after stamping (**content-hash mismatch**);
- residue is still open, the round is out of season bound, the round is a **duplicate**, or the
  apply gate is OFF.

## Applying for real (owner only; gated OFF by default)

This build ships the write gate **OFF** — `apply` prints an explanation and writes nothing. To apply
on your **local** checkout after go-live, arm **both** halves for the run (two env vars — no code
edit):

```
INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=my-local-token ./weekly_update.sh apply --round 15
```

`INGEST_SCORE_APPLY_ARMED=1` is the code half; `INGEST_SCORE_APPLY=<token>` is the env half. Both are
unset in the committed repo, so the shipped default is OFF. Choose your own token string.

A successful apply prints:

```
================ WEEKLY UPDATE APPLIED ================
  Round applied      : R15, season 2026
  Players applied    : 318
  Store hash         : 968de0c7  ->  692d6302
  Board hash         : 270a2c5f  ->  … 
  Guard 5 (boot)     : GREEN (validated on the staged build)
  Transaction/backup : .../engine/rl_after/ingestion/.weekly_txn/txn_...
  Duplicate guard    : recorded 318 triple(s); ledger now holds 318 (a re-send is blocked)
  Value+rank history : rounds [14, 15] recorded for 804 players (append-only; earlier rounds kept)
  FV provenance      : board built from the STAGED valuation module (recorded in the txn)
  UI bundles         : refreshed — working + public (board stamp == committed, public leak-free)
  The store/board/manifest/ledger/history were staged, validated, and swapped atomically;
  a crash mid-swap rolls back. Backups, transaction record, ledger and history are kept.
======================================================
```

## How the apply is safe (staged transaction)

`apply` never mutates the live files while validating. It stages the updated **store, board +
sidecar, boot manifest, and dedup ledger** in a workspace and validates the staged set end-to-end
(store parses; only the fed players' season scores changed; the board regenerates; the board
source-stamp equals the staged store; the boot pins equal the staged store+board; **Guard 5 is
GREEN** against the staged set; the ledger holds the exact snapshot triples; the board's player
universe is unchanged). Only then are the live files replaced **atomically**, inside a transaction
directory that keeps immutable originals + a phase journal.

- **Failure during the swap** → every original is restored (the store is never left with a stale
  board / manifest / ledger).
- **Crash mid-apply** → the next command detects the incomplete transaction and **refuses**; run
  `./weekly_update.sh recover` to roll back to the pre-apply originals. Transaction evidence is
  never silently deleted.

The board build is **fail-closed on valuation provenance**: `RL_FV` is bound to the *staged* repo's
`forward_valuation`, `PYTHONPATH` is the staged repo + the pinned vendor only, every ambient `RL_*`
redirect is cleared, and the build **halts** unless the `distribution_pricing` it would load is inside
the staged repo and byte-identical to the staged source (so a stale ambient module can never produce or
commit a board). The valuation flag policy comes from the release config manifest; an unknown or
conflicting inherited flag halts.

> The board is validated for structure, source-stamp coherence, Guard-5 pins, player universe and
> forward-valuation provenance. No cross-run/cross-machine numerical-determinism verdict is claimed
> here (the value wobble is a separate, external blocker).

## Now included (this workstream)

Each `apply` / `run` / `catchup` round regenerates the store, board (+sidecar), boot manifest and dedup
ledger, **and**:
- records the persistent per-player **value**, **overall-rank** and **positional-rank** history
  (append-only, one entry per round, earlier rounds never overwritten);
- refreshes the Matchday **UI bundles** (working + public) from the committed board, ring-fenced to the
  committed board id, with the public bundle leak-free by construction;
- writes a per-round **movers report** and folds the previous-round movement (`dRound` / `dRoundRank` /
  `dRoundPosRank`) into the working UI bundle (integrated HTML-engine movers data);
- supports the controlled multi-round **`catchup`** (one preflight + one approval, per-round sequential
  transactions, restart-safe).

## Not yet included (pending a later tranche, after the v2.11 rebase)

- **`correct`** / **`undo`** (a mistaken round cannot yet be surgically reverted beyond crash rollback);
- season/round read from release metadata (season 2026 / 24 rounds are still defaults);
- the accepted foundation's own **stale `engine_head` / `rl_model` boot pins** (`40f43772` / `a5fd3d7d`
  vs the checked-out `904722cd` / `cc626d7d`) — a bake re-stamp of `data/expected_boot.json`, an
  owner/bake action OUTSIDE this workstream. The proofs supply coherent engine identities to their
  scratch fixtures so Guard 5 validates against a coherent release, but the real manifest still needs
  that re-stamp before a real go-live.

Until those exist and this branch is rebased onto the baked v2.11 head, treat the tool as a reviewed
transaction core with the live-scoring layer proven on scratch — not yet a real-store operator.
