# P5-3 — The export writes the as-at −1/−2 columns itself (MEDIUM; board bytes move, values do not)

**Goal.** rl_export.py stops computing vM1/vM2 as `ev(p,2024)/ev(p,2025)` on the current roster
(rl_export.py:210-212) and instead reads the banked as-at values (docs/evidence/walkforward_retro_2026-08-29/
values_asat_2025.json / 2024.json, or their new home after P4-1): a current player's vM1/vM2 = his as-at value,
null when he was not on that board. The `back` section (the old retiree recall, 228 rows) is deleted from the
board; the full as-at rosters incl. retirees stay in ui/data/asat_boards.js (emit_asat_seasons.py becomes the
one writer of that file and is run by the landing's UI step, so an extract never puts the old columns back).

**Why.** Owner ruling 2026-10-14: −1/−2 are as-at boards. Today the engine still writes the backward lens and
the emitter patches it after the fact (ui/MAINTAINER.md).

**Rules.** The banks are build inputs (proofstash BUILD_INPUT_FILES) and the export halts if a bank is missing
or its stamp (store/board it was cut on) is older than the current store's as-at roster facts — define that
rule explicitly: a bank is valid for a store whose `_last_listed`/`_retired`/scoring facts for seasons ≤ Y are
unchanged; the pass re-runs otherwise (document the re-run command). Present v, vP1, vP2 unchanged. The UI
card's "Value by year" and any reader of `back` updated; ui/tests fixtures updated.

**Proof.** Build: v/vP1/vP2 identical key-for-key; vM1/vM2 equal the banks; `back` absent; all ui/tests;
standalone smoke; acceptance green. engine_head unmoved (rl_export is not pinned).

**Lands via.** Lever act, `moves: [board]`, movers declared (the vM1/vM2 column change on 804 rows is not a
value move; say so in the NOTE).
