# P5-1 — One `raw_ev`, one final `ev` (MEDIUM; board byte-identical)

**Depends on.** P5-2 (same file; the tail is gone, so the whole file is the engine). P4-3 (engine_head in `moves`).

**Done when.** engine/rl_after/_merged_recover.py has one `def raw_ev` and one top-level `def ev` whose body calls
the ORDER 43/45/46g/49 stages in today's order as named helpers, every module-level caller still sees the stage it
sees today, and the board is byte-identical.

**Facts (checked at ffb2663b).**
- `def raw_ev` at :907 and :1573 (the second is the W4 wrapper; `_raw_ev_w4_0=raw_ev` at :1572).
- `def ev` at :2968, :3107, :6035 (`__inner=_ev_pre43`, alias :6034), :6153 (`__inner=_ev_pre45`, alias :6152),
  :6227 (`__inner=_ev_pre46g`, alias :6226), :6269 (`__inner=_ev_pre49`, alias :6268). `_ev_click=ev` at :3065
  captures the :2968 stage ("the full-click evaluation").
- The :6153 and :6269 definitions sit inside `if _O45:` (:6124-6125, `RL_O45`) and `if _O49:` (:6264-6265, `RL_O49`).
  Both are manifest-pinned dials ('1' in data/model_config.json `vars`), i.e. config, not stray flags (README
  config rule). Keep both conditions verbatim here; P5-4 does not remove pinned dials either.
- MODULE-LEVEL CALLS BEFORE LATER WRAPPERS EXIST: module-level code calls `ev(_p,2026)` at :5782, :5930, :5942,
  :5952 (availability block), :6000, :6009, :6018 (D7) — all before :6035 — so those measurements are taken on the pre-43 chain BY DESIGN (the D7 comment at
  :5969-5985: "the position is load-bearing"). `o31_D` is also wrapped (:6092-6093, `_o31D_pre43`, own `__inner`).
- Memo/state the stages rely on: `_pe_clear`, the `_POLE` memo, `_O46F` (the :6227 stage flips it, :6231/:6236),
  the ev-time scoring swap-and-restore.

**Change.** Rename each intermediate stage to a named function (`_ev_stage_pre43`, …) and keep each existing alias
name bound to the SAME function object it is bound to today (`_ev_click`, `_raw_ev_w4_0`, `_ev_pre43`, …) so every
caller — including the module-level calls at :5782-:6018 and the `o31_D` chain — resolves to the stage it calls now.
The final `ev` is defined once, after the last stage, and its body calls the stages in order under the same two
`_O45`/`_O49` conditions. Keep every stage comment. Do not change rounding points or the `__inner` call counts inside
a stage (several stages call their inner twice: :6198/:6202, :6286/:6290).

**Must not change.** Arithmetic, call order and rounding inside every stage; memo behaviour; which stage each
module-level call and each alias sees; what a function body that calls the GLOBAL name `ev(` / `raw_ev(` at call
time resolves to (grep every body between :907 and the end for bare calls — rebinding the global changes them); the `_O45`/`_O49` conditions; anything P5-4 owns (the unpinned reads, the
refit lane at :2130-~2438). The board (96896e1c), store, config.

**Prove it.**
- Before editing, record for every row `ev(p,Y)` for Y in 2024..2028 and every module-level result those seven calls
  feed (`_ev_off`, `_ev_p1`, `_AVAIL_MOVERS`, `_D7_ROWS`, and what :5782 sets) from a harness load of the current file; after the edit, the same values, key for key.
- Bare build byte-identical (README recipe); `tools/harness docs/evidence/walkforward_retro_2026-08-29/
  pass_asat_seasons.py` control passes and the as-at banks are byte-identical (`git diff --exit-code`);
  engine/rl_after/one_source_selftest.py (run from engine/rl_after); acceptance `--profile full`.
- The lever act: `moves: [engine_head]`, `prereg.board_before == board_after`.

**Lands via.** Lever act, board unmoved by prediction; the lander proves it.
