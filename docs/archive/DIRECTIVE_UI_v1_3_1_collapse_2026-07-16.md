# DIRECTIVE — UI v1.3.1: THE COLLAPSE RULE (owner-ruled 2026-07-16) · seat 9 (Fable)
### Tier 3, ~30-45 min, Low effort, fresh Claude Code (Opus) chat. CONTINUES the v1.3 branch
### `claude/club-pocket-profiles-positional-ph5p4g` at `1a272ff` STRICT — never a sibling (item 202).
### PR #101's merge is HELD for this; one viewing, one click closes it.

## THE RULINGS (register item 216)
1. **K ABSORBS G (owner-worded):** a K-FWD listing absorbs a G-FWD listing; K-DEF absorbs G-DEF.
   The G is slot ELIGIBILITY, never a DPP. Apply this collapse FIRST, then the counting rule.
2. **The locations CSV is CORRECTED at main ≥ `cf0a410`** (four rows: Matt Whitlock →
   "K-DEF,K-FWD"; Flanders/Oskar Baker/Ed Langdon → "G-DEF,G-FWD"). **Regenerate
   `ui/app/positions_data.js` from the corrected CSV via the committed
   `ui/tools/extract_positions.py`** — no hand edits to the generated file.
3. After collapse + corrections, NO ranked player carries 3+ effective positions (the 15 RUCK+K-FWD
   and 12 K-family swingmen become plain DPPs; Langford = K-FWD/MID, the DPP-mid exception verbatim).
   **Assert it:** a committed test FAILS if any player's post-collapse position count exceeds 2.

## THE JOB
(1) `counting.js`: collapse-first, then the owner rule unchanged (1 / DPP 0.5-0.5 / DPP-mid non-mid
1, mid 0). (2) **DELETE the equal-split 3-4-position generalisation with an OBITUARY** (delete-
don't-disable — it is dead code post-collapse). (3) Regenerate positions_data.js (item 2 above);
stamp block updated. (4) Update tests: the 15/15 suite + the ≤2-positions assertion + one case per
collapsed pattern (a RUCK/K-FWD, a four-way swingman, Langford, one corrected pure-general). (5)
Update the panel footnote (collapse rule stated; the 3-4-position caveat REMOVED). (6) Refresh the
positional screenshots (one club containing a collapsed swingman).

## FENCE
IN: ui/app/counting.js · ui/app/positions_data.js (generated only) · tests · footnote text ·
screenshots/v1_3. OUT: everything else ui/ · ui/data bundles · ingest · engine/ · docs/. Bundle
byte-match re-proven in an updated verdicts file. Base pin: main at-or-after this filing's SHA,
docs/-only diff from it. RETURN ≤15 lines: head SHA · verdicts · actual time.
