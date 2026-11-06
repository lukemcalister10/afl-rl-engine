# The plan briefs — Phases 2 to 5 (owner word 2026-11-06: "Yes, please proceed with that plan.")

One brief per item. Each is a complete hand-off for one agent: goal, why, files, the rules that must hold,
the proof to run, and how it lands. Work ONE engine item at a time (never two agents in the same engine file).
Every brief ends with the same contract:

- **Lane.** A change that moves the board, the store or a pinned identity lands through the landing library
  (`tools/landing`, driver pattern in `tools/ingest.py` / `docs/evidence/*/ACT_SPEC.json`), with the
  flip-commit procedure for engine pins (hand-edit `data/expected_boot.json`, `python3 tools/restamp.py apply`,
  commit, then fly). A change that moves none of those is a plain commit after its tests.
- **Proof.** Byte-identical board where the brief says so (a bare build via `tools/landing/_build_child.py` and a
  JSON key-for-key compare against `data/rl_build/rl_app_data.json`); the named test suites; the acceptance
  runner (`python3 -m acceptance.runner --profile host-insensitive`) green; `python3 tools/rulebook_lint.py` clean.
- **Owner word.** Only value-moving items (tier HIGH) need the owner's word and a blind review (RULEBOOK law 11).
  Everything else is the owner-accepted plan.
- **No new knobs.** No environment flags, no kill-switches (the engine has none since 2026-10-14). A measurement
  variant is a module constant flipped for a build, never shipped.

| order | brief | tier | lands via |
|---|---|---|---|
| 1 | P2-1 rounds-on-ingest | LOW | plain commit + a rehearsed dry run |
| 2 | P2-2 movers-single-writer | LOW | plain commit (bundle byte-identical) |
| 3 | P4-1 evidence-archive | LOW | plain commit + archive branch |
| 4 | P4-2 dead-tooling-deletions | LOW | plain commit |
| 5 | P4-3 flip-inside-the-lander | MEDIUM | plain commit (lander change) + one rehearsal act |
| 6 | P4-4 retire-the-round-lane | MEDIUM | plain commit (after 1 and 5) |
| 7 | P2-3 store-writer-and-player-tool | MEDIUM | plain commit (lane verbs) + one rehearsal act |
| 8 | P2-4 season-keyed-ids | MEDIUM | plain commit (UI/ingest) |
| 9 | P5-1 engine-one-ev | MEDIUM | lever act, board byte-identical |
| 10 | P5-2 engine-file-end | MEDIUM | lever act, board byte-identical |
| 11 | P5-3 asat-columns-adopted | MEDIUM | lever act (board bytes move: −1/−2 columns) |
| 12 | P5-4 remaining-flags | MEDIUM | lever act + contract re-seal |
| 13 | P3-1 live-season-constant | MEDIUM | lever act, board byte-identical |
| 14 | P3-2 rollover-tool (AFTER THE DRAFT) | MEDIUM | plain commit + rehearsal on a copy |
| 15 | P5-5 veteran-damper (F3) | HIGH | lever act, owner word, blind review |
| 16 | P5-6 grid-surface-smoothing | HIGH | lever act, owner word, blind review |
| 17 | P4-5 stale-docs-sweep | LOW | plain commit, last |
