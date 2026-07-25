# CI HARNESS MIGRATION — DIAGNOSIS (phase 1, 2026-07-22) — branch ci/harness-migration-r19
Classification of every stale-identity hit (old ids: engine a83c9f6d · store b1fd0bce · board 8d90c9ac):

HEALTHY — no action:
- data/expected_boot.json: operative Guard-5 pins ALREADY at R19 (board 6f07f7cb, engine 7c452715,
  store f37d9716, as_of_round 19). Old ids appear only in prose notes. VERIFIED [ran].
- LTI_REGISTER.md pin 652d83e8: matches current file byte-for-byte. VERIFIED [ran].
- engine/rl_after/*.py: old ids are historical lineage COMMENTS, not pins. Leave.
- ui/tests/club_curve_provenance.test.py: old ids sit in an anti-staleness assert-ABSENT list. Deliberate.
- data/gates_snapshots/*: historical records. Leave.

STALE — re-pin required (phase 2):
- PANEL_EXPECTED.txt + run_panel.sh PANEL list: pinned to pre-R19 boards (8d90c9ac / 270a2c5f era).
  Re-pin the 10 players to R19 board 6f07f7cb values. Player list located in rl_app_data.json (see key note).
- .github/workflows/ci-guards.yml line ~113: "final-integration board of record = 2ab73a6f..." — a
  BUILT-THIS-RUN board md5 from a pre-R19 run. Must be re-derived by actually building the board from
  the released store/engine and pinning the fresh md5 (also the A2 cross-machine proof).

REBUILD — the heavy half (phase 2/3, issue #138):
- Movers + value/rank histories: replay R14→R19 under engine 7c452715; regen movers.js (currently
  92a8f3a0, fails closed) + histories; then live-scoring.yml's Movers acceptance step can go green.

INCIDENT (self-caught, owner-visible):
- The 2026-07-22 branch cull deleted codex/establish-forward-lens-acceptance, which
  final-integration.yml fetches for its Board-B oracle (70ef0ff3). The commit was still fetchable by
  SHA; branch RESTORED at the same tip, fixture verified intact [ran]. Cull rule amended: a branch is
  dead only if no workflow references it — grep .github/workflows for refs before any future cull.

Phase 2 plan: re-pin panel from the released board → run the four suites locally → fresh-build board
for the record-md5 pin → #138 replay → iterate to 4× green, zero waivers → claims note → blind Opus
review → owner merge word.
