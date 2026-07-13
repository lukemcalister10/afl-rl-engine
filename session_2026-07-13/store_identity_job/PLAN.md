# ITEM 20 — THE STORE-IDENTITY JOB · PLAN (first committed artifact, MODE auto)

Branch `claude/store-identity-job-v2-9-kuers3` · base = main @ 4234bf5 (v2.9 tag 9f8ae76 + 2 docs-only
register commits; store b0c39d78, board 81e48293). Trigger VERIFIED: `refs/tags/v2.9 → 9f8ae76`
(fresh ls-remote) and main == the bake head + docs. Guard 5 GREEN at bootstrap (store == pinned).
One store-writer in flight. Spec of record = register items 20 + 20a (+ 33 for the ten). EFFORT High.

## PRESCREEN FINDINGS (all verified against store b0c39d78 + authoritative_universe_v2.csv, 804 rows)
- Store `eligibilities` == CSV col `eligibilities` for all 804 (normalization operates on this field).
- The ten club-less **active** rows == the only active(804) rows with null `_club`; their CSV
  `legacy_afl_club` == the owner's list VERBATIM (zero discrepancies). The other **325** null-`_club`
  rows are ALL `_retired` historical (off-board, not in CSV, no current-club source) — reported, not
  backfilled (STRICT FENCE honoured).
- houston: `_club`=Port Adelaide · `affl_team`=St Kilda Saints · CSV afl=Collingwood ⇒ after fix
  displays AFL **Collingwood**, AFFL St Kilda, NOT Port Adelaide (owner acceptance met).
- Bramble: 2026 = 15g@62.4 (the ONLY store row exceeding the round-14 ceiling); career `games`=91 =
  exact sum of scoring rows. 15→14 ⇒ sum 90; 872/14 = 62.29 → 62.3 (store 1dp convention).
- K/G normalization: **192** active rows change (91 drop G-DEF, 112 drop G-FWD; 0 emptied). After
  normalization the ONLY cross-end survivors are exactly **gardiner** + **whitlock** (register's
  "TWO FOUND") — owner corrections resolve both; **lukas-cooke** is the 3rd correction (20a).
- Corrections agree with each player's engine class (present/drafted/future_position all K-*).
- Board today: active 804 → 10 empty club; back 198 → 0 empty club (all carry draft club; back∩CSV=0).

## THE EDITS (fenced: source store enumerated edits ONLY · id_resolver club-match · rl_export club
## field + CAT_BY_CLUB rename · collision_sentry rename · CSV archive · derived-artifact regen)

(a) **BRAMBLE** — 2026 games 15→14, avg 62.4→62.3; career `games` 91→90. Value move (games/avg feed
    ev). Produce the COMPLETE affected-`v`-row list (expect bramble + a hairline ripple).
(b) **afl_club** — add to the 804 from CSV `legacy_afl_club` (current club). `affl_team` UNCHANGED.
    Identity field, not read by ev() ⇒ 0 board `v` movers.
(c) **`_club` → `_draft_club` RENAME (store-wide, KEEP)** — rename on every row carrying `_club`
    (consumer CAT_BY_CLUB reads it store-wide). PLUS the **ten-row draft backfill** (register v60):
    for the enumerated ten ONLY, `_draft_club := afl_club` (owner-declared one-club players; null draft
    = missing draft row). STRICT FENCE — no generalisation; 325 other null-draft rows reported, not
    touched.
(d) **id_resolver** — `_club_match` matches on `afl_club` (not affl_team); docstring corrected.
    **rl_export** shipped `club` repointed to `afl_club` with a `_draft_club` fallback for retired
    back-catalogue rows (they carry no current club) — active shows current AFL club, back unchanged,
    **zero empty club board-wide** (register v59 acceptance; the ten are the red-path test).
    CAT_BY_CLUB grouping key `_club` → `_draft_club` (draft club is its correct input; output identical).
(e) **ELIGIBILITIES** — K/G companion-tag law: drop same-end G when same-end K present (cross-end
    survives; swingmen keep both K). Then owner corrections: gardiner→K-DEF · whitlock→K-DEF,K-FWD ·
    cooke→K-DEF. Commit the full before/after tag table. Store carries normalized truth (raw stays in
    the archived CSV). 0 board movers (board does not ship eligibilities).
(f) **ENTRY-BOUND ASSERTIONS** in the importer — HALT with the row named on: 2026 games > 14
    (rounds elapsed) · `_by` out of range · afl_club ∉ the 18 · any normalized tag ∉
    {G-DEF,G-FWD,K-DEF,K-FWD,MID,RUCK}.
(g) **CSV ARCHIVE RULE** — stamp header (`IMPORTED AT <sha>, store <before> → <after>; NOT A SOURCE
    — do not read as current`) and move to `docs/inputs/archive/`.
(h) **REGEN** — bootstrap → rl_export (six-lever refit env, default-ON) → board; s4_matrix → book,
    re-seal at post-fix values; re-pin expected_boot (store, board, panel if the ripple touches it);
    UI re-extract; fresh-bootstrap guard suite (5 SSI guards + canary + red-paths) + ship_gates +
    panel + official cohort gate. Auto-escalate to Tier 1 if any guard goes red.

## ACCEPTANCE
- Store md5 moves b0c39d78 → <new>; derived artifacts re-stamped; Guard 5 re-pinned.
- Board: 0 `v` movers EXCEPT bramble + declared hairline ripple; club field correct (houston=Collingwood);
  ZERO empty club on the exported board (active + back); CAT_BY_CLUB byte-identical.
- Eligibilities before/after table committed; grep-proof no consumer reads the old `_club` name.
- Guard suite + ship_gates + panel + cohort gate all GREEN (gate ratios invariant to the hairline move).
- Deliverables: COMPLETE affected-row list (location + count) · houston/keays/bramble named lines.

## SEQUENCE
1. (this) commit PLAN. 2. Sanity: reproduce current board 81e48293 from b0c39d78 (validate pipeline).
3. Write + run the transform (a–e) with assertions (f) → new store; commit store + transform.
4. Update consumers (d) + collision_sentry rename; grep-proof. 5. CSV archive (g).
6. Regen all derived + re-pin + UI (h); build affected-row list + tag table. 7. Full guard/gate/panel
   suite. 8. Commit, push, PR, RETURN (≤30 lines).
