# P2-2 — One writer and one serialiser for `ui/data/movers.js` (LOW)

**Depends on.** Nothing. First in the order. Serial rule applies (touches the lander's writer 4c path).

**Done when.** Every program that writes ui/data/movers.js loads and dumps it through ONE new module,
engine/rl_after/ingestion/movers_bundle.py (`load(path) -> (head, obj, tail)`, `dumps(obj) -> str`,
`write(path, head, obj, tail)`), the committed file is byte-identical before and after, and a standalone
full-cycle drift check (below) is green on the live tree.

**Facts (checked at 9a400286).**
- Writers of movers.js: round_movers.write_bundle (round_movers.py:585-595, `ensure_ascii=False`, insertion
  order) via accumulate_bundle (:857), called by round_finalize.py:311 (and read at :426) and by
  ui/tools/rebuild_movers_derived.py:67 = lander WRITER 4 (steps.py:2466-2480); finals_report.py:254
  (`sort_keys=True, ensure_ascii=False`) = WRITER 4c (steps.py:2593 on); docs/evidence/walkforward_retro_2026-08-29/
  emit_retro_series.py:116 (`ensure_ascii` default True, insertion order) = WRITER 4b (steps.py:2559).
  emit_fw1_report.py / emit_fw2_report.py under docs/evidence/fw*_report_* are historical: leave them.
- NOT movers.js writers: emit_asat_seasons.py writes board_view_working.js and asat_boards.js (:45, :48);
  ui/tools/ownership_store_apply.py:782-792 and generate_movers_transition.py write movers_transition.js.
- Private brace-slice readers to switch to `load`: tools/ingest.py:112-124, steps.py:1380, :1996-1998,
  retro_walkforward.py:61, emit_retro_series.py:31, rebuild_movers_derived.py:50, plus the writers' own readers
  finals_report._load_bundle (:48) and round_movers.load_bundle (:603-613, called at :877), and
  session_2026-07-21/final_integration/tests/season_anchor_check.py:130. Leave steps.py `_js_obj`
  (:2164-2174): it deliberately copies the gate's own parser (test_movers_transition._loadjs) and reads other bundles.
- The committed file: 7,461,298 bytes; ONE raw non-ASCII character, an em dash in the `// GENERATED —` header
  comment (round_movers.py:589 writes it), none in the JSON body; the body has 166 `\u` escapes and is reproduced
  exactly by `json.dumps(obj, ensure_ascii=True, separators=(',', ':'))` with NO sort_keys (measured); with
  `ensure_ascii=False` or `sort_keys=True` it is not. So the canonical form is the bytes on disk; keep the header.
- The drift guard exists: `ui/tools/rebuild_movers_derived.py --check` (:31, :93-101). It is RED standalone on
  today's tree (committed 7,461,298 vs rebuilt 6,853,651 bytes) because writer 4 drops the retro series that 4b
  re-adds (steps.py:2496-2507); the ui step runs it between 4 and 4b (:2475-2480), the only place it is valid.

**Change.**
1. movers_bundle.py with the canonical serialiser = `ensure_ascii=True`, compact separators, insertion order,
   the existing `window.__MATCHDAY_MOVERS__ = …;\n` wrapper and header lines as they are on disk.
2. Point the three live writers and the readers above at it (load by path where the lander loads by path).
   finals_report stops passing `sort_keys=True` (key order then comes from the parsed bundle and the report dict).
3. Add a full-cycle check (a `--full` mode or a test): copy the bundle to scratch, run writer 4 then 4b there,
   compare to the committed bytes. Keep the existing `--check` as the ui step's mid-step guard.

**Must not change.** movers.js bytes. Report contents. movers_transition.js and its writers — never apply
sort_keys there: the ITEM 408 record must stay a byte-verbatim prefix (ownership_store_apply.py:775-790).
The ui step's writer order 3 → 4 → 4 --check → 4b → 4c (WRITER 0, the conditional v0 sidecar at steps.py:2363-2397,
and WRITER 9, the positions map at :2896, are new since ffb2663b; neither touches movers.js).

**Prove it.**
- load+dumps of the committed file == committed (sha256 printed in the commit message).
- `python3 engine/rl_after/ingestion/test_movers_transition.py`; `python3 engine/rl_after/ingestion/test_finals_report.py`
  (it rebuilds the shipped FW1 report — must stay green with the new serialiser); `node ui/tests/movers.test.js`,
  `node ui/tests/ui_defects_2026-08-21.test.js`, `node ui/tests/ui_222_items.test.mjs`.
- the full-cycle check green; `python3 docs/evidence/walkforward_retro_2026-08-29/emit_retro_series.py` then
  `git diff --exit-code ui/data/movers.js`; acceptance `--profile full` green.

**Lands via.** Plain commit (no identity moves).
