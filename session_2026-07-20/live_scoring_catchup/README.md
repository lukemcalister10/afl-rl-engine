# Controlled five-round catch-up — R14 → R15 → R16 → R17 → R18 → R19

Owner ruling 2026-07-20 (Track-B). Proves the controlled catch-up of the owner's **genuine** R15–R19
weekly score files on a **disposable copy of the accepted Round-14 state**, gate OFF (armed in-process
against the scratch only). No real store / release-candidate / production UI file is touched.

## Run

```
python3 session_2026-07-20/live_scoring_catchup/catchup_proof.py --write
```

Writes `PROOF.md` + `proof.json`. Exit 0 = ALL PASS. (Also runs on a clean GitHub runner via
`.github/workflows/live-scoring.yml`.)

## What is proven

| | |
|---|---|
| **A · preflight** | all five files read + validated: per-file SHA-256, detected encoding (CP1252 for R15–R17, UTF-8 for R18–R19, both read without altering names/scores), listed=played count (318/319/410/406/405), legitimate listed-zero count, absent/DNP vs the active universe, every resolved stable key, and the identity overrides. One consolidated report; HALTS before the first write on any unresolved/ambiguous/duplicate identity. |
| **B · participation** | file membership defines participation — a listed player gains exactly one game per round listed; **Jordan Croft's R19 = 0 is a legitimate played zero** (+1 game, +0 to the average); an **absent** player is byte-unchanged (no game, no placeholder, no carry-forward). |
| **C · identity by stable key** | Callum Brown → `callum-brown-ire`; the two Bailey Williams reach the correct stable records (`bailey-williams-wb`: R18=55, R19=137; `bailey-williams-wc`: R16=67, R17=82, R18=100, R19=84) and never collapse. |
| **D · sequential transactions** | one approval; each round is its own staged STAGE→VALIDATE→ATOMIC-SWAP transaction, committed in full before the next; each round keeps its own store, board, board+store hashes, ledger entry, transaction evidence, and value / overall-rank / positional-rank history + movers report + integrated HTML-engine (working-bundle) movers data. |
| **E · restart / resume + dedup** | a stopped catch-up resumes from the next unapplied round (committed rounds skipped); re-running the whole catch-up applies nothing; a re-sent committed round is blocked by the dedup ledger. |
| **F · no production touched** | the real store, board, boot manifest, ledger, three histories and UI bundles are byte-identical before and after. |

Crash-mid-commit detection + byte-identical recovery is proven by the shared staged-transaction
machinery in `../weekly_updater_hardening/` and `../live_scoring_two_round/`.

## Owner identity ruling (2026-07-20)

Resolved by **stable identity**, never display name or row order — see
`engine/rl_after/ingestion/catchup_identity_overrides.json`:

- **Callum Brown** → `callum-brown-ire` (active "Callum M. Brown", St Kilda). The export omits the
  middle initial; the exact "Callum Brown" in the store is retired. (Owner decision, 2026-07-20.)
- **Bailey Williams** — two active players share the display name, disambiguated by (round, score):
  `bailey-williams-wb` (Collingwood) R18=55, R19=137; `bailey-williams-wc` ("Bailey J. Williams",
  Sydney) R16=67, R17=82, R18=100, R19=84.

## Fixtures

`fixtures/R15.csv … fixtures/R19.csv` are the owner's genuine files, copied **byte-for-byte** (original
encodings preserved: CP1252 / UTF-8). They are inputs to the proof only — never applied to the real
store.
