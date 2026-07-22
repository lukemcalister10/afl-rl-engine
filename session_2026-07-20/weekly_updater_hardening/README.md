# session 2026-07-20 · weekly_updater_hardening

Hardens the PR #125 weekly round-score updater's **transaction core** for safe LOCAL use (gate stays
OFF; no real round applied). **This is a transaction-core prototype, NOT yet a safe weekly updater** —
UI regeneration, previous-round movement, immutable history and correction/undo are pending a later
tranche after the v2.11 rebase. See `DESIGN.md` (architecture + audit reconciliation), `PROOF.md` /
`proof.json` (transaction proof), and `FV_PROOF.md` / `fv_proof.json` (forward-valuation provenance).

## Contents
- `DESIGN.md` — the full design (gaps corrected, snapshot identity, staged transaction, rollback,
  the 2026-07-20 forward-valuation provenance hardening, corrected scope + audit reconciliation).
- `failure_injection_proof.py` — the transaction proof: 7 failure-injection points + crash recovery +
  acceptance (clean apply, dedup re-send, stale, altered-hash, invalid round, residue, snapshot→preview
  equivalence). Scratch copies only; arms the gate in-process; writes nothing to the real store.
- `fv_provenance_proof.py` — fail-closed forward-valuation provenance + config-policy proof: the
  stale `21d530bf` on the RL_FV default path HALTS (never produces/pins/commits the `d7a95e8d` board);
  the staged `d0c8c69f` is used; an adversarial inherited `RL_FV` is forced back to the staged module;
  a conflicting inherited valuation flag halts.
- `_crash_child.py` — helper that hard-exits mid-commit to simulate a crash (for the recovery case).
- `PROOF.md`, `proof.json`, `FV_PROOF.md`, `fv_proof.json` — generated results (`--write`).

## Run
```
python3 session_2026-07-20/weekly_updater_hardening/failure_injection_proof.py --write
```
Exit 0 = ALL PROOFS PASS. Needs the engine env (numpy/scipy/sklearn + vendored unidecode); set
`RL_VENDOR` if not already seeded. Runs several board regenerations, so allow a few minutes.

## Owner tooling (shipped)
- CLI: `tools/round_entry/round_entry.py` — `enter` / `confirm` / `show` / `apply` / `recover`.
- Launcher: `tools/round_entry/weekly_update.sh` (Linux/macOS/WSL/Git-Bash) + `weekly_update.bat`
  (Windows) + `README.md`.

The board is validated for structure, source-stamp coherence, Guard-5 pins and player universe — not
for cross-run/cross-machine numerical determinism (the value wobble is a separate, external item and
is not touched here).
