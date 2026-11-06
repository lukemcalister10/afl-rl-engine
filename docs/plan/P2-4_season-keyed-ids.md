# P2-4 — Season-keyed ids everywhere a round number is a key (MEDIUM)

**Goal.** Every place that keys a report, a point or a bank by a bare round number (`reports["29"]`, `rounds:
[15..29]`, `values_r24.json`, `retro-r24`, feed rounds 25–29 as finals "ledger keys") carries the season:
`2026-R24`, `2026-FW1`… so 2027's Round 1 cannot collide with 2026's and the UI can show two seasons.

**Why.** The finals weeks already had to borrow "feed rounds 25–29" as pseudo-rounds because the key space is a
bare integer; the rollover (P3-2) cannot start a new season on top of integer keys.

**Files.** engine/rl_after/ingestion/round_movers.py, finals_report.py, round_history.py (value_history.json
columns), tools/ingest.py (column ids: already `<prefix><slug>-<SEASON>`), docs/evidence/walkforward_retro_
2026-08-29/*.py (banks and point ids), ui/app/movers.js, history.js, card.js, board.js (every `Number(r) > 24`
style test — grep `> 24`, `>= 25`, `slice(7)`, `retro-r`), ui/tests/* fixtures.

**Rules.** One migration of ui/data/movers.js and data/value_history.json keys in one commit, with a
reversible mapping written beside it; the UI reads only the new shape (no dual-shape readers left behind).
The lander's drift guards must rebuild the migrated bundle byte-identical. Values, rows and reports unchanged.

**Proof.** Every ui/tests suite; test_movers_transition, test_finals_report, the retro and as-at dry tests;
standalone smoke; acceptance green.

**Lands via.** Plain commit (UI data migration is not a board move) — but run the full landing gate set.
