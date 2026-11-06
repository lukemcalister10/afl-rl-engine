# P2-2 — One writer and one serialiser for `ui/data/movers.js` (LOW)

**Depends on.** Nothing. First in the order. Serial rule applies (touches the lander's writer 4c path).

**Done when.** Every program that writes ui/data/movers.js loads and dumps it through ONE new module,
engine/rl_after/ingestion/movers_bundle.py (`load(path) -> (head, obj, tail)`, `dumps(obj) -> str`,
`write(path, head, obj, tail)`), the committed file is byte-identical before and after, and a standalone
full-cycle drift check (below) is green on the live tree.

**Facts (checked at ffb2663b).**
- Writers of movers.js: round_movers.write_bundle (round_movers.py:585-595, `ensure_ascii=False`, insertion
  order) via accumulate_bundle (:857), called by round_finalize.py:311 (and read at :426) and by
  ui/tools/rebuild_movers_derived.py:67 = lander WRITER 4 (steps.py:1975-1989); finals_report.py:254
  (`sort_keys=True, ensure_ascii=False`) = WRITER 4c (steps.py:2117 on); docs/evidence/walkforward_retro_2026-08-29/
  emit_retro_series.py:116 (`ensure_ascii` default True, insertion order) = WRITER 4b (steps.py:2068).
  emit_fw1_report.py / emit_fw2_report.py under docs/evidence/fw*_report_* are historical: leave them.
- NOT movers.js writers: emit_asat_seasons.py writes board_view_working.js and asat_boards.js (:45, :48);
  ui/tools/ownership_store_apply.py:678-688 and generate_movers_transition.py write movers_transition.js.
- Private brace-slice readers to switch to `load`: tools/ingest.py:112-124, steps.py:936, :1541-1543,
  retro_walkforward.py:61, emit_retro_series.py:31, rebuild_movers_derived.py:50. Leave steps.py `_js_obj`
  (:1708-1714): it deliberately copies the gate's own parser (test_movers_transition._loadjs) and reads other bundles.
- The committed file: 7,376,123 bytes, 0 raw non-ASCII characters, 59 `\u` escapes. Its body is reproduced
  exactly by `json.dumps(obj, ensure_ascii=True, separators=(',', ':'))` with NO sort_keys (measured); with
  `ensure_ascii=False` or `sort_keys=True` it is not. (Reviewer said "one raw non-ASCII char and one \u escape":
  not what this tree holds. The point stands — the writers disagree — and the choice is: the bytes on disk.)
- The drift guard exists: `ui/tools/rebuild_movers_derived.py --check` (:31, :93-101). It is RED standalone on
  today's tree (committed 7,376,123 vs rebuilt 6,767,373 bytes) because writer 4 drops the retro series that 4b
  re-adds (steps.py:2005-2016); the ui step runs it between 4 and 4b (:1984-1989), the only place it is valid.

**Change.**
1. movers_bundle.py with the canonical serialiser = `ensure_ascii=True`, compact separators, insertion order,
   the existing `window.__MATCHDAY_MOVERS__ = …;\n` wrapper and header lines as they are on disk.
2. Point the three live writers and the readers above at it (load by path where the lander loads by path).
   finals_report stops passing `sort_keys=True` (key order then comes from the parsed bundle and the report dict).
3. Add a full-cycle check (a `--full` mode or a test): copy the bundle to scratch, run writer 4 then 4b there,
   compare to the committed bytes. Keep the existing `--check` as the ui step's mid-step guard.

**Must not change.** movers.js bytes. Report contents. movers_transition.js and its writers — never apply
sort_keys there: the ITEM 408 record must stay a byte-verbatim prefix (ownership_store_apply.py:665-686).
The ui step's writer order 3 → 4 → 4 --check → 4b → 4c.

**Prove it.**
- load+dumps of the committed file == committed (sha256 printed in the commit message).
- `python3 engine/rl_after/ingestion/test_movers_transition.py`; `python3 engine/rl_after/ingestion/test_finals_report.py`
  (it rebuilds the shipped FW1 report — must stay green with the new serialiser); `node ui/tests/movers.test.js`,
  `node ui/tests/ui_defects_2026-08-21.test.js`, `node ui/tests/ui_222_items.test.mjs`.
- the full-cycle check green; `python3 docs/evidence/walkforward_retro_2026-08-29/emit_retro_series.py` then
  `git diff --exit-code ui/data/movers.js`; acceptance `--profile full` green.

**Lands via.** Plain commit (no identity moves).
