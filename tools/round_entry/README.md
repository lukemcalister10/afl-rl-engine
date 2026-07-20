# Weekly Updater — owner's local runbook

> **STATUS: transaction-core prototype — NOT yet a safe weekly updater, NOT for real owner use.**
> The store-write gate is **OFF** and must stay OFF. This branch delivers the safe transaction core
> (staged apply, atomic swap, rollback, crash recovery, strong snapshot identity, fail-closed
> forward-valuation provenance). It does **not** yet regenerate the Matchday **UI bundles**, generate
> **previous-round movement** data, or provide **immutable weekly history / correction / undo**. Those
> land in a later tranche, after the numerical root result is final, the v2.11 release head exists, and
> this branch is rebased onto it. See `session_2026-07-20/weekly_updater_hardening/DESIGN.md`.

One tool, one command, the whole *entry* job: paste `name,score`, confirm any misses, inspect the
exact snapshot, and (once armed locally) apply it to the store — staged, validated, and atomically
swapped, with rollback and crash recovery. **No Python editing. The real store write is gated OFF by
default** (this build applies no real round).

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
  Players applied    : 7
  Store hash         : 968de0c7  ->  15711cb3
  Board hash         : 270a2c5f  ->  cd45ddf5
  Guard 5 (boot)     : GREEN (validated on the staged build)
  Transaction/backup : .../engine/rl_after/ingestion/.weekly_txn/txn_...
  Duplicate guard    : recorded 7 triple(s); ledger now holds 7 (a re-send is blocked)
  UI regeneration    : STILL REQUIRED — the Matchday UI view bundle is a separate step:
                       python3 ui/tools/extract_board_view.py   (TIER-3, read-only)
  Everything else was staged, validated, and swapped atomically; a crash mid-swap rolls back.
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

## Not yet included (pending a later tranche, after the v2.11 rebase)

`apply` regenerates the store, board (+sidecar), boot manifest and dedup ledger only. It does **not**:
- regenerate the Matchday **UI bundles** (run `python3 ui/tools/extract_board_view.py` yourself);
- produce **previous-round movement** / Round-Review data;
- keep an **immutable per-round history**, or support **`correct`** / **`undo`**;
- read season/round from release metadata (season 2026 / 24 rounds are still defaults).

Until those exist and this branch is rebased onto the baked v2.11 head, treat the tool as a reviewed
transaction core, not a hands-off weekly operator.
