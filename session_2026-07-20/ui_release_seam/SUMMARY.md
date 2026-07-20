# v2.11 UI / RELEASE-SEAM — prep (no bake, no board selection/promotion)

Branch `prep/v2.11-ui-release-seam`, based strictly on `3055ea5f` (env-pin #2, board 06d8af60 held).
This prepares the UI-extraction + release-metadata seam so the v2.11 board, once its numerical root
cause is fixed and it is baked, installs and renders **without another implementation cycle**. No board
was generated, selected or promoted; the diagnostic candidate (`6720dfae`) was **read only** as a schema
fixture — its `v` values are not approved and were never merged.

## JOB 1 — pass through all Leg-F fields
`ui/tools/extract_board_view.py` now carries these top-level Leg-F fields on the **working** bundle
(verbatim pass-through; empty container when the board lacks them — carried, never fabricated):
`phantomLayer`, `phantomPicks`, `phantomTotals` (added) + retained `lensPicks`, `lensConservation`.
These are working-tier ONLY; the public bundle receives none of them (leak-safe by construction).

**Entrant-banner proof** (temp extraction of the candidate fixture — see `entrant_banner_proof.json`):
the +1/+2 banner reads `entrant_layer_pvc = 83538`, `expected_slots_per_year = 103.43`,
`seal_sha256_8 = a17aafed` straight out of `phantomTotals._meta`.

## JOB 2 — durable release/round metadata contract (no hardcoded labels)
- `data/expected_boot.json` MAY carry optional `release_version` and `as_of_round` (NOT set in this task).
- The extractor passes them into the working stamp as `releaseVersion` / `asOfRound` (raw; `None` when
  absent). Legacy `tag` alias == `release_version` (`""` when unknown) for `card.js`/`clubs.js`.
- The UI displays them via `MD.releaseLabel` / `MD.roundLabel`; **missing metadata → neutral unknown**
  (`unversioned` / `Round —`), never an invented version or round.
- Hardcoded `"v2.10"` (extractor stamp) and `"Round 17"` (UI display) are **removed**.
  Note: `Round 17` lived in **two** display sites — `ui/app/main.js` (masthead) and `ui/app/board.js`
  (board-view strip). The directive's allowed-paths named a single UI JS file, but JOB 2 requires the
  label gone from the UI *display*, so both were fixed with the same contract.

## JOB 3 — ring-fence intact (fail-closed, not weakened)
board md5 == boot board pin; store md5 == boot store pin; bundle carries the exact board identity;
UI refuses a mismatched board; extractor recomputes nothing. Fixture tests use a **temporary board +
temporary boot manifest** so the candidate runs without weakening any assertion.

## JOB 4 — tests
- `ui/tests/extract_seam.test.py` — 27/27 (phantom transfer, entrant metadata exact, contract from boot,
  missing-metadata neutral, board+store pin mismatch fail-closed, public leak-safety, no-recompute).
- `ui/tests/release_seam.test.js` — 14/14 (label helpers + neutral unknowns, ring-fence accept/refuse,
  no `Round 17` literal in display files). Existing `counting_rule.test.js` still 24/24.

## Not done (by design)
No change to engine/store/canonical board/expected_boot values/fitted artifacts/ingestion/production
bundles/tags/releases. No PR opened or modified.

---

## FOLLOW-UP (same branch) — movement fields + canonical board-identity key

**1. `dRound` / `dRoundRank`** now pass through `row_working` verbatim (they already rode `row_public`);
`None` when the source omits them — never fabricated.

**2. Identity split-brain resolved.** The audit was right: the extractor emitted `stamp.srcmd5` (board
md5) while the retrospective consumer `board.js` read `stamp.source_md5` — which was never emitted, so it
silently fell back to a hardcoded `"968de0c7"`. Resolution:
- Canonical key = **`source_md5`** = the source board identity (`md5(rl_app_data.json)`), emitted by the
  extractor; **`srcmd5`** retained as a temporary identical-value alias for the un-regenerated production
  bundle and any ring-fence code not yet migrated.
- `seam.js` ring-fence reads `source_md5 || srcmd5`.
- `board.js` retrospective consumer now keys its consistency check off the canonical `source_md5`
  (parent-board pointer, with `srcmd5` fallback), dropping the hardcoded `"968de0c7"` and the mismatched
  `store_md5` read — so the UI and the retrospective seam share ONE board identity. `retroFor` is exposed
  on `MD.board` so the test exercises the exact function the UI runs.
- Note: `board.js`'s `source_md5` was, per its own comment/fallback, semantically a *store*-md5 read; it
  was realigned to the board identity per the directive ("same underlying board identity"). The retro
  wiring is dormant (`__MATCHDAY_RETRO__` absent in production), so this is a forward-looking contract
  change with no live behaviour affected.

**3. Red/green tests** (extractor 36/36, UI 21/21, counting 24/24):
movement verbatim on both tiers; absent movement stays null; canonical `source_md5` emitted and read by
seam.js + board.js (+ srcmd5 alias); board pin mismatch still fails closed (UI + retro); no new
public/internal leak (source identity absent from the public bundle).

No production bundle regenerated; no v2.11/Round-14 values set; `expected_boot.json`/engine/store/board
untouched; no PR/merge/tag/release.

---

## FOLLOW-UP 2 (same branch) — explicit, separately-named provenance identities

Corrects FOLLOW-UP 1: the UI ring fence and the retrospective seam must NOT overload one `source_md5`
field with two provenance meanings. The real F2 artifacts (commit cf945898) stamp `store_md5` and
`balanced_board_md5`, NOT the final post-Leg-F working-board md5.

**Working stamp — three explicit identities:**
- `board_md5` = full md5 of the installed working `rl_app_data.json` — the ONLY identity the UI ring
  fence authenticates.
- `store_md5` = full md5 of the actual pinned source store already read + verified by the extractor.
- `balanced_board_md5` = optional, passed VERBATIM from release metadata (`expected_boot`); `null` until
  the final bake sets it. **Not set on this prep branch.**
- `srcmd5` retained as an identical temporary alias of `board_md5`. `source_md5` removed (ambiguous).

**UI ring fence (seam.js):** `board_md5 || srcmd5` vs `EXPECTED_BOARD` — installed board only.

**Retrospective seam (board.js):** validates the F2 contract independently — retro `entry.stamp.store_md5`
must match working `store_md5` AND retro `entry.stamp.balanced_board_md5` must match working
`balanced_board_md5`; both required; a mismatch returns `{state:"mismatch", field}` naming the failed
field. While `balanced_board_md5` is unset (pre-bake) it returns `pending` — never `ok`, never a hardcoded
fallback. It no longer compares against the working-board md5.

**Tests** (extractor 41/41, UI 23/23, counting 24/24): `board_md5`==source-board md5; `store_md5`==verified
store md5; `srcmd5`==`board_md5`; `balanced_board_md5` verbatim (null when absent); ring fence uses board
identity only; F2 stamp with matching store+balanced accepted; wrong store refused; wrong balanced refused;
missing balanced stays pending; no `968de0c7`/`06d8af60` hardcode; no identity leaks to the public bundle;
dRound/dRoundRank tests still green.

Scope held: `balanced_board_md5` value NOT set; `expected_boot` untouched; no production bundle
regenerated; no board selected/installed; no PR/merge/tag/release.
