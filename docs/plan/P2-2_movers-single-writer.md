# P2-2 — One writer and one serialiser for `ui/data/movers.js` (LOW)

**Goal.** Every writer of the movers bundle goes through one function (parse → mutate → serialise) with one
canonical serialisation (sorted keys, compact separators, the `window.__MATCHDAY_MOVERS__ = …;` wrapper), so a
re-serialise of an unchanged bundle is byte-identical and the drift guards ("committed == rebuilt") can never
disagree over whitespace.

**Why.** The review found four writers with their own `_load_bundle`/dump code: engine/rl_after/ingestion/
round_movers.py, finals_report.py, tools/landing/steps.py (writer 4c + the drift guard), tools/ingest.py, plus
emit_retro_series.py / emit_asat_seasons.py / retro_walkforward.py in docs/evidence/walkforward_retro_2026-08-29.
Each re-implements the brace-matching loader. One copy is the mirrored-pair hazard the landing library exists
to refuse.

**Files.** New engine/rl_after/ingestion/movers_bundle.py: `load(path) -> (head, obj, tail)`, `dump(path, obj)`,
`canonical(obj) -> str`. Every writer above imports it (by path where the lander loads modules by path).

**Rules.** The first commit must leave ui/data/movers.js byte-identical (prove: load+dump of the committed
file reproduces it; if the committed bytes are not canonical, the SECOND commit canonicalises them once with
the drift guard's own rebuild proving nothing but bytes moved). No report content changes.

**Proof.** python3 engine/rl_after/ingestion/test_movers_transition.py, test_finals_report.py, node ui/tests/
movers.test.js, ui_defects_2026-08-21.test.js, ui_222_items.test.mjs; a run of the lander's drift guard
(`python3 -m tools.landing.steps` has none standalone — use the `ui` step's guard function on the live tree,
or re-run the retro emitter and assert byte-identity); acceptance green.

**Lands via.** Plain commit(s).
