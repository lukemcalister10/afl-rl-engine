# P5-2 — The engine file ends where the engine ends (MEDIUM; board byte-identical)

**Goal.** `_merged_recover.py` is exec'd by rl_export.py and deliberately stops at the line
`print("=== AFTER (wired: delist + staleness + isotonic) — named players ===")` (line 6299 of 6347): the 48
lines after it are dead diagnostic prints that the exec never reaches because rl_export truncates the source
at that marker. Delete the tail, delete the truncation in rl_export.py, and make the module importable
(`import _merged_recover`) as well as exec-able, so tools can load it without the string surgery.

**Why.** A file whose last 48 lines are never run, and a loader that finds a print statement to know where
the program ends, is the kind of thing that makes every change slow.

**Rules.** The exec'd region must be byte-identical in effect: same module-level statements in the same
order. rl_export.py's loader (`exec` of the sliced source) becomes a plain exec of the whole file or an import;
the day-0 and the `one_source_selftest` loaders that mirror rl_export's call order (`session_2026-07-21/…`,
one_source_selftest.py:153) must be updated in the same commit.

**Proof.** Bare build byte-identical; one_source_selftest; the harness control; acceptance green. engine_head moves.

**Lands via.** Lever act, board declared unmoved.
