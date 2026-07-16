# UI v1.3 — CLUB POCKET-PROFILES + POSITIONAL BREAKDOWN · PLAN (first committed artifact)

Directive: `docs/DIRECTIVE_UI_v1_3_pocket_profiles_2026-07-16.md` (register item 196, approved 197(2)).
**TIER 3, `ui/`-fenced, display-only — no value is recomputed, no pricing/rounding/Best-23 change.**
Base = the SHIPPED board (tag **v2.10**, board **790136a3**); asserted below. EFFORT medium.
TIME: 2–3 h wall-clock (as directed); will report actual in the RETURN.

## BASE + RING-FENCE ASSERTIONS (all PASS at plan time — read-only dry run)
- Branched from `main` head `c317e4c`; `git diff --name-only 21d94a4..origin/main` is **docs-only**
  (`DIRECTIVE_UI_v1_3…md`, `OPEN_ITEMS_REGISTER.md`) — no `ui/` or `engine/` mover ⇒ no HALT.
- `ui/app/config.js EXPECTED_BOARD == "790136a3"` ✓ · working bundle `stamp.board`/`stamp.srcmd5 ==
  790136a3…` ✓ · `stamp.tag == v2.10` · `engine fc7045d6` · `store b1fd0bce`. Values come from the
  SHIPPED board's bundles only; the Leg-B candidate does not exist for this job.
- `ui/data/` bundles are the ONLY VALUE SOURCE and are **not** touched (md5s printed in the verdicts
  file, byte-match asserted). `ui/tools/ingest_inputs.py` untouched; `ui/config.js` read-only beyond nothing.

## THE COUNTING RULE (owner, verbatim-in-substance) — the core of task 2
Each player's PLAYER value is distributed across the positions in his `Position/s` cell so that the
**per-player weights sum to exactly 1.0** (value conservation — required for "% of the club's PLAYER
value" to total 100%). The owner's three stated cases:
- single position → **1.0** to that position;
- DPP (two positions) → **0.5 to each**;
- **EXCEPT DPP midfielders** → the non-mid position counts **1**, the midfield component counts **0**.

**One rule reproduces all three verbatim cases, and it is forced (not chosen):**
> **MID collects value only from MID-only players. A player with any non-mid eligibility splits his
> full value equally across his non-mid positions; his MID share is 0.**

- `["GEN_FWD"] → {GEN_FWD:1}` · `["MID"] → {MID:1}` · `["GEN_FWD","KEY_FWD"] → 0.5/0.5` ·
  `["MID","GEN_FWD"] → {GEN_FWD:1, MID:0}` (the exception). ✔ all four match the owner verbatim.
- **Generalisation to the 33 ranked players with 3–4 listed positions** (the CSV carries them; the
  owner worded the rule for ≤2): equal split is the only value-conserving reading of "to each"
  (`0.5×3 = 1.5 > 1` is impossible), and the mid-exception's rationale — attribute to the specialist
  position, not the catch-all MID — applies unchanged. So `["RUC","GEN_FWD","KEY_FWD"] → 1/3 each`;
  `["MID","GEN_FWD","GEN_DEF"] → 0.5/0.5, MID 0`. **This generalisation is FLAGGED in the RETURN and
  in the panel footnote** so the owner sees it at his merge click. No case contradicts the three he gave.
- Position vocabulary maps CSV→board posCode: `K-DEF→KEY_DEF · G-DEF→GEN_DEF · MID→MID · G-FWD→GEN_FWD
  · K-FWD→KEY_FWD · RUCK/RUC→RUC` (6 canonical rows). Join coverage verified: all 804 board players
  have exactly one `Position/s` row (0 missing); the two Max Kings stay distinct by the established
  normalised name key.

Committed unit tests (`ui/tests/counting_rule.test.js`, node-runnable) cover: single non-mid, single
mid, DPP no-mid, **DPP-mid exception**, 3-pos no-mid, 3-pos-with-mid, 4-pos, weight-sum==1 invariant,
and the value-conservation property over a synthetic roster.

## DATA PLAN (no bundle regeneration; ui/data stays byte-identical)
The 7 pocket metrics (overall/player/picks/top5/top10/best23/nonBest23) are already per-club in
`ui/data/club_valuation.js`; league averages = plain means over the 16 ranked clubs, computed at
render. Task 2 needs per-player value×position — value from the board bundle (`v`/`dispVal`), positions
from the CSV. Since the offline `file://` viewer cannot read a CSV at runtime and `ui/data/` +
`ingest_inputs.py` are out of fence, a **values-free** position map is generated once and committed:
- `ui/tools/extract_positions.py` — deterministic, read-only over `docs/inputs/AFFL_Player_Locations.csv`;
  **reuses** the established `nkey` join + the two-Max-Kings distinctness assertion (imported logic,
  not reimplemented); emits `ui/app/positions_data.js` = `window.__CLUB_POSITIONS__ = {stamp:{board,
  generated,n}, byKey:{"<board-key>":["POSCODE",…]}}`. **Carries zero dollar values** — the board
  bundle remains the sole value source. HALT-AND-ASK on any join ambiguity or missing coverage.

## SURFACES (reuse the v1.2 panel/hover/summary patterns)
1. **Pocket-profile panel (task 1).** `ui/app/pocket.js` — on **hover** (and **tap** on touch) of a
   club name anywhere it renders **ranked** (the Clubs summary rows; the board's ranked club headers/
   banner), a panel showing overall / player / picks / top-5 / top-10 / Best-23 / non-Best-23, **each
   three ways: absolute · % of the club's overall · vs league average**. Best-23 = the existing exact
   greedy (read from `club_valuation.best23`; not reimplemented).
2. **Positional breakdown (task 2).** In the same panel (second block): per position (6 rows) —
   **absolute · % of the club's PLAYER value · vs league average** — computed by applying the counting
   rule above to each rostered player's board value. `MD.counting` (pure, exported) holds the rule.
3. **Footnote (task 3).** Small footnote on the panel: *league average = mean over the 16 ranked
   clubs; the Free-Agents pool (75 players) is excluded from every denominator and never ranked
   (item 191)*; plus the ≥3-position generalisation note.
4. **Deferred, NOT built (task 4 / item 196(3)).** Lens-awareness (posture re-render + ±1/±2) stays
   flagged exactly where v1.2 left it. Untouched.

## FILES
IN-fence, all new or additive: `ui/app/counting.js` (pure rule + `module.exports`), `ui/app/pocket.js`,
`ui/app/positions_data.js` (generated, values-free), `ui/tools/extract_positions.py` (generator),
`ui/tests/counting_rule.test.js`, `ui/styles/matchday.css` (+panel styles), `ui/index.html` (+2 script
tags), `ui/app/clubs.js` + `ui/app/board.js` (attach hover/tap to club names — additive). Screenshots
under `ui/screenshots/v1_3/`. **No** engine/store/docs/pricing/Best-23/ingest/bundle edits.

## METHOD / DELIVERABLES
Per-task commits. Screenshots: pocket-profile open on two clubs + positional breakdown on two clubs
(one with a DPP-mid case) + before/after of the changed Clubs page. Committed verdicts file (v1.2
pattern): ring-fence pin asserted · counting-rule tests pass · `ui/data/` md5 byte-match · fence 100%
`ui/`. RETURN ≤30 lines: branch · head SHA · PR number · actual time + plain-terms close.
