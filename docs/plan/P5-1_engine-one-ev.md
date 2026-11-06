# P5-1 — One `ev()` (MEDIUM; board byte-identical)

**Goal.** `_merged_recover.py` defines `raw_ev` twice (907, 1573) and `ev` six times (2968, 3107, 6035, 6153,
6227, 6269), each later definition wrapping the previous (`__inner=_ev_pre43`, `_ev_pre45`, `_ev_pre46g`,
`_ev_pre49`). Collapse to one `raw_ev` and one `ev` whose body applies the ORDER 43/45/46/49 stages in order,
with the stage helpers kept as named functions.

**Why.** The review's first finding on complexity: nobody can read what a price is without unwinding six
wrappers; the D3 hard-wiring removed the switches but not the layering.

**Rules.** Pure refactor: identical arithmetic in identical order, identical rounding points, identical memo
behaviour (`_pe_clear`, the `_POLE` memo, the ev-time scoring swap-and-restore). Keep the stage comments. The
truncation marker (`print("=== AFTER…`) and the tail after it are P5-2's; do not touch them here.

**Proof.** Bare build byte-identical to the live board (key-for-key JSON compare); the as-at harness control
(`tools/harness docs/evidence/walkforward_retro_2026-08-29/pass_asat_seasons.py` — its Y=2026 control must
still give 0 diffs, and the as-at banks must reproduce byte-identical); engine/rl_after/one_source_selftest.py;
acceptance green. engine_head moves (flip or P4-3).

**Lands via.** Lever act, `moves: [board]` only if bytes change (they must not) — declare `board` unmoved and
let the lander prove it.
