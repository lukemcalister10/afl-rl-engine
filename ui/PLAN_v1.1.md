# PLAN — Matchday UI **v1.1** · team-context lens + the owner's feedback batch (first committed artifact)

**Directive:** MATCHDAY UI v1.1 (supervisor seat, 2026-07-15) · **TIER 3** (never bakes; moves no value —
the SSI read-only-board doctrine) · MODE **auto** (this PLAN is the first commit) · EFFORT **medium**.
**Branch:** `claude/matchday-ui-team-context-8w98ef`. **Candidate only — the owner views the UI himself
before any merge word.**

## BASE VERIFICATION (done — self-gating on the bake)
- **FULL-URL ls-remote** of `https://github.com/lukemcalister10/afl-rl-engine.git`: tag **`v2.10`** present at
  `d14efaef`. (On first entry the tag had not yet appeared; the owner confirmed it should be tagged and the
  push had lagged — re-checked live, `v2.10` resolved, so the bake **has** promoted. Not based on a branch.)
- Branch reset onto **`v2.10`** (`git checkout -B … v2.10`); the prior branch head `e778d12` is the exact base
  `v2.10` was built from, so this is a clean fast-forward — no work lost.
- **Guard 5 / ring-fence:** the tagged board is `rl_app_data.json` md5 **`790136a3`** (== `expected_boot.board`).
  The checked-in bundles + `config.EXPECTED_BOARD` were stale at `3dc19fbb` → **base-refresh commit** moves the
  ring-fence pin with the tagged board (directive: "all view bundles regenerate via `extract_board_view.py`
  from the tagged board; the ring-fence pin moves with it").

## THE AFFL CLUB RANKING PAGE — located? **NO → owner-ruled DEFER**
Item 2 names "the AFFL club ranking page **as previously specced**." I searched exhaustively —
`docs/ui_direction/`, `docs/ui_styles/`, `DESIGN_DIRECTION.md`, both registers, the notepads, and full
`git log --all` over the UI-doc paths — **no such page spec exists anywhere** (the only `affl_team` hits are
the store/identity data field; the only "rank" hits are the unrelated armband value ladder). Per the FEED
("locate and cite, or **HALT-AND-ASK** rather than inventing one") I halted and asked the owner.
**Owner ruling (2026-07-15): "Build rest, defer page."** → I build the two *lens* halves of item 2
(group/filter by AFFL club · club ΣSCAR totals) and **defer the standalone ranking PAGE**; flagged in RETURN.
No page is invented.

## VISUAL LAW (the Matchday LOCK is law — with ONE owner amendment)
`docs/ui_styles/theme_03_matchday_FINAL/LOCK.md` — near-black pitch `#0a0c10`, one **volt** accent `#c8f04a`,
condensed caps for names/labels, mono tabular figures; **full names everywhere** (wrap, never clip),
**comma digit grouping** on every value; colour never the sole carrier (pills/figures always signed).
- **AMENDMENT (item 3, register item 163, owner-worded 2026-07-15):** the v1.0 "segmented ten-block power
  bar, **no continuous rail**" device is **superseded** — the value bar becomes a **continuous filling line
  with a colour spectrum along the fill**. This PLAN records the amendment; the item-3 commit cites item 163.
  The old squares are **not** treated as protected.

## THE FEEDBACK BATCH — one commit + one screenshot each (screenshot-per-change checklist) — ALL TICKED
- [x] **0 · PLAN** (this file) — `b4a559a`. *(no screenshot — the artifact is the plan)*
- [x] **A · base refresh** — `extract_board_view.py` stamp `v2.8→v2.10`; regenerate bundles from tagged board
      `790136a3`; `config.EXPECTED_BOARD 3dc19fbb→790136a3` — `35c8922`. → `screenshots/01_board_working.png`.
- [x] **1 · clubs per player** — extractor reads the pinned store **read-only** (md5-verified, fail-closed),
      joins on `key`, adds `afl_club` + `affl_team` **DISPLAY** fields (no value change). Board + card show
      both — `e5d1f2e`. → `screenshots/10_clubs_afl_affl.png`, `10_clubs_card.png`.
- [x] **2 · team-context lens v1** (page deferred) — board **group/filter by AFFL club** + **club ΣSCAR
      totals** — `ee03dc4`. → `screenshots/11_team_context_lens.png`, `11_team_context_grouped.png`.
- [x] **3 · value bar → continuous filling line + colour spectrum** (cite item 163) — `be7676c`. →
      `screenshots/12_value_line_spectrum.png`.
- [x] **4 · column headings on every column** (working + public) — `b1ca723`. →
      `screenshots/13_column_headings.png`, `03_board_public.png`.
- [x] **5 · filter by position** — `0987239`. → `screenshots/14_filter_position.png`.
- [x] **6 · trade desk** — every pick **1–80** individually selectable · players **type-ahead searchable** ·
      dropdown font **matched to the board type style** — `b1c1315`. → `screenshots/07_trade_desk.png`,
      `07_trade_pick_search.png`.
- [x] **7 · public board de-clunk** — fix the duplicated "steady" (row-end **and** misaligned under the name;
      the 7th grid cell overflowing the 6-col template) → one instance, correctly aligned — `0b62c50`. →
      `screenshots/03_board_public.png`.
- [x] **8 · +1/+2 lens toggle DISABLED** with tooltip "projection law lands next chapter". **THE NUMBERS ARE
      NOT TOUCHED** — the ruled LENS PROJECTION LAW fix rides the next (merged PVC+flex) chapter — `90c789d`.
      → `screenshots/15_lens_disabled.png`.

## RETURN NOTES
- **Fence held:** every change is under `ui/` (app, styles, extractor, bundles, screenshots, dev driver).
  No `rl_export.py`, engine, store, `config`, gate, or `docs/` file touched; no computed value or lens
  number changed (verified: `git diff --name-only v2.10..HEAD` is 100% `ui/`).
- **Ring-fence intact:** the UI still fail-closes on a board-id mismatch (verified — forcing a wrong
  `EXPECTED_BOARD` renders the alarm-red rejection; `09_fail_closed.png`). Guard-5-analogue live.
- **DEFERRED (owner-ruled):** the standalone AFFL club ranking PAGE — no spec was locatable; the ranking
  *information* ships inline via the group-by-club view. Awaiting the owner's spec to build the page.

## FENCE (honoured)
**IN:** `ui/**` + `ui/tools/extract_board_view.py` (display fields only) + this job's session dir.
The extractor's only new read is the **pinned store** (`engine/rl_after/rl_model_data.json`), **strictly
read-only, md5-verified** — item 1 directs it ("the master database carries both; the extractor adds them as
DISPLAY fields"). No store write.
**OUT:** `rl_export.py`, the engine, the store, `config`, gates, `docs/` · ANY computed value or lens-number
change · the lens projection engine fix (next chapter's) · the standalone ranking page (owner-deferred).
Scope growth ⇒ STOP and return.

## DATA SEAM (unchanged doctrine)
Pure view; computes **no** price. Two tiered, stamped bundles; the public bundle stays leak-proof by
construction (no keys/slugs/md5/guard/owner-rule). Clubs are public-safe display strings and are the only
new fields on the public bundle. Ring-fence fail-closes if the loaded board's md5 head ≠ `EXPECTED_BOARD`.
