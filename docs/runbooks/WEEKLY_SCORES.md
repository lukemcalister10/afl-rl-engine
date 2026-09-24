# WEEKLY SCORES — one command

This is the whole procedure for a finals week (FW1–FW4, GF). It replaces the finals-week runbook
(`docs/evidence/finals_fw1_2026-08-30/RUNBOOK_finals_week.md`, kept as history) and the
prereg / arming / predicted-movers / lander-self-test steps it required. Owner ruling 2026-09-24.

    tools/ingest scores/FW3.csv

That's it. The week comes from the file name (`--week FW3` overrides). The owner sending the file is
the go-ahead; nothing else needs arming.

## What it does, in order

1. **Environment.** Pinned numpy, full clone history, playwright for the browser gates, clean tree.
   Fixes what it can, and names anything it can't, before any engine work starts.
2. **Names.** Every CSV name resolves by, in this order: an `--as "Name=key"` ruling given on this
   run, then a standing alias in `engine/rl_after/ingestion/catchup_identity_overrides.json`, then
   an exact name. If any name is ambiguous (two active Bailey Williams) or unknown, it stops before
   touching anything and lists every problem in one pass.
3. **Edits.** Each player who played gets games +1, and their average is re-averaged with the
   ingestor's own `_mean`. Players not in the file are untouched.
4. **Inputs commit.** `scores/<WEEK>.csv`, `scores/resolved/2026_<WEEK>.json` and
   `docs/evidence/ingest/2026_<WEEK>/` are committed first, so a failed run leaves nothing half-done
   and running the same command again is safe.
5. **Landing.** The edit is applied through the lander's store-edit transaction: byte-checked edit,
   build, pins, lineage, contract, UI, state, and every landing gate. It also runs one extra gate,
   `tools/ingest_bounds.py`, which refuses the week if players who did NOT play move by more than a
   median 1.5%, or any one of them by more than max(60 pts, 10%). Real weeks move them about 0.16%,
   so tripping it means something other than football moved the board. On any failure the lander
   restores every file byte-for-byte.
6. **After.** The /home/claude workspace is re-seeded, the movers are summarised, `valueboard.html`
   is rebuilt and smoke-tested, and it is pushed.

## When it stops

It says why, in words. Fix the cause and run the same command again.

- **A name.** Re-run with `--as "Name On Sheet=store-key"`. Once a name recurs, add it to the
  overrides file so it never needs asking again.
- **A gate.** Every file is already back as it was, and the log is in `/tmp/ingest_failed_<WEEK>/`
  (outside the tree, so the re-run starts clean). If the tool itself is wrong, fix the tool; do not
  work around it by hand. On success the log is committed to `docs/evidence/ingest/2026_<WEEK>/`.

`--check` resolves names and computes the edits without building anything (seconds).
`--no-push` commits but does not push. `git revert` undoes a week.

## Proof

Replaying FW2 through this command on a copy of the pre-FW2 tree (2026-09-24) reproduced the FW2
landing: store `a367386a` and board `d3fb6b48` byte-identical, 366 edits, and every player's value,
rank and movers entry identical. It differed only in dates, the engine version stamp and label text.
Measured: preflight 58s, landing 1,042s (the build 274s, the balanced sibling 548s, the UI 148s,
the gates 44s). No retries.
