# Matchday UI — maintainer notes

**This document is for the maintainer. Nothing in it renders in the app.**

The standing design law (owner, 2026-08-28): the app is the owner's product. It shows prices,
moves, ranks, form, history, club ratings and picks — and none of the machinery that made them.
Process, provenance, and self-verification live here (and in the repo's register under
`docs/registers/`), never on a user surface. Guards keep working exactly as before; they simply
report to the console and the test suites instead of the screen.

## What was stripped from the screens (2026-08-28 redesign)

All of the following used to render in the app and now does not. None of the underlying
machinery was deleted — only its screen furniture.

**Masthead** — "Working aid · live board · reads · rules · controls", the board/engine/store
md5 line, the boardID, "vs last accepted bake", "panel 10/10", "real", "guard 5 pass", and the
working/public tier toggle. The app now has a single (fully transparent) tier. Identity of the
live release lives in `engine/rl_after/rl_app_data.json` (`stamp` block) and the board-view
bundles' `stamp` objects; the register entry for the current bake names every hash.

**Player card** — identity stamps, "this figure is his draft's slot", the "Why the price is
what it is" per-lever waterfall, "order is the chain's not the size's", "residual is real and
it is data", and every explanatory essay. The waterfall's data still exists on each player
record (`p.explain` where present) and in the engine's ORDER ledger; read it there.

**Forward projections** — the +1/+2 lens columns and card figures are ruled OFF (owner word:
they were wrong). `lensYears`/`p.lens` are truncated to the first three (backward) entries on
every surface. The forward machinery still exists in the engine; it renders nowhere.

**Board controls** — all/my-reads scope, delta base picker, +1/+2 options, group off/by-club,
lens column picker, debug slugs. Filters that remain: Position, Eligible, Cohort, Age, Club.

**Delta columns** — "delta vs bake" and "over free" are gone. The one movement column is
**Round Δ**: current round vs previous round, from the latest weekly report of record in
`window.__MATCHDAY_MOVERS__` (`value_change` per key). The card's Round Δ is the same figure.

**Footers** — "value, rank and positional rank are complete", the clubs-page essays, the
trade-page "The model speaks; you overrule." Completeness is asserted by the test suites
(`ui_defects_2026-08-21.test.js` and friends), not by a footer.

**Movers page** — board-md5/release identity spans and the debug pills. The model-change
banner survives in one line ("part of the movement is the model, not football") because it is
information about the numbers, not about the process.

## Weekly history: one line per event, and the MC ledger

History rows on the player card are ONE LINE PER EVENT. A round renders as its round label.
A model change renders as `Model change (MC-N)` — nothing else. The IDs are sequential over
`window.__MATCHDAY_MOVERS__.model_changes` in bundle order (`MC-` + index+1, keyed by the
change's `between` transition), so they are stable as long as the bundle's list is append-only.
If a rebuild ever rewrites that list's order, restate this ledger in the same commit.

The ledger — what each ID actually was, and the owner rulings that authorized it:

| ID | Change | Transition (`between`) | Owner rulings |
| --- | --- | --- | --- |
| MC-1 | Post R19 Redesign 1 | 19 → post-r19-redesign-1 | ITEM_408_items_6_7_option_A, ITEM_411_D1_restatement_v467 |
| MC-2 | 30/7 rederivation | 20 → rederivation-30-7 | ITEM_271_Addendum_17 |
| MC-3 | 6/8 adoption — redesign era | rederivation-30-7 → redesign-adoption-6-8 | ADOPTION_2026-08-06_review_era |
| MC-4 | 10/8 DOB courier + v0surf re-cut | 22 → dob-courier-10-8 | DOB_COURIER_2026-08-10_refit_authorised |
| MC-5 | 10/8 never-rises restore (R12) | dob-courier-10-8 → g1-never-rises-10-8 | G1_NEVER_RISES_2026-08-10_restore_and_gates |
| MC-6 | 20/8 THE LANDING — campaign board adopted | g1-never-rises-10-8 → the-landing-20-8 | THE_LANDING_2026-08-20_land_it |
| MC-7 | 20/8 D8 adoption — ceiling-only dial shipped default-on | the-landing-20-8 → the-d8-adoption-20-8 | THE_D8_ADOPTION_2026-08-20_yes_im_adopting |
| MC-8 | 20/8 injury-sheet re-cut — Armstrong + Clarke de-listed | the-d8-adoption-20-8 → the-sheet-recut-20-8 | THE_INJURY_SHEET_RECUT_2026-08-20_all_good_fine_by_me |
| MC-9 | 20/8 F5 rounding fix — declared entrant layer 56772→56773 (no player value moved) | 23 → the-f5-rounding-20-8 | THE_F5_ROUNDING_2026-08-20_launch_the_ready_items |
| MC-10 | 20/8 back-rows clock repair — 25 of 198 back-history rows re-priced on the present (no ACTIVE value moved) | the-f5-rounding-20-8 → the-backrows-repair-20-8 | THE_BACKROWS_AGE_REF_REPAIR_2026-08-20_lets_fix_it_now_please |
| MC-11 | 21/8 staircase fix adopted — ORDER 44 level-axis band monotoniser, variant A raw (ratchet, unconserved) default-on | the-backrows-repair-20-8 → the-staircase-adoption-21-8 | THE_STAIRCASE_FIX_ADOPTION_2026-08-21_A_raw_I_prefer_lock_that_in_unconserved |
| MC-12 | 24/8 Will Graham dual corrected — owner store edit p_dual 90 → 40; one mover (−262) | 24 → graham-dual-40-24-8 | WILL_GRAHAM_DUAL_2026-08-24_edit_to_40pct_SF_and_recalculate |
| MC-13 | 25/8 ARM-2 rebake + position-scaled safety net — owner D1/D2/D3; 543bf900 basis, net moves 10 (+922, all t4 today; armed on 19 younger rows, prereg R1) | graham-dual-40-24-8 → order45-arm2-net-24-9 | ARM2_REBAKE_ADOPT_2026-08-25_yes_adopt_the_new_model, SAFETY_NET_SCALED_2026-08-25_scaled_on_the_safety_net, MATURE_AGERS_EXCLUDED_2026-08-25_exclude_mature_agers |
| MC-14 | 27/8 THE COMBINED BUILD — retention surface + step-up clock law + first-banked easing (W=1.0) + S_LL5G day-0 law; 287 movers, net +3,460; blind-review GREEN | order45-arm2-net-24-9 → combined-build-46-47-48-sll5g | MECHANISM_AGREED_2026-08-27_agree_on_your_mechanism, SLL5G_LOCKED_2026-08-27_lock_in_ll5g_then, DEPTH3_CAP_A_2026-08-27_a_for_depth_3_cap, SAT_SEASON_LT2_2026-08-27_lt2_is_fine_for_sat_season, EASING_KEPT_2026-08-27_keep_the_easing, RUCK_RELIEF_2026-08-27_ruck_relief_yes, NOARB_APPROVED_2026-08-27_alright_great_approved |

Full incident records for every ruling ID live in the repo registers (`docs/registers/`).

## Clubs page: the 56-asset rating

The "Rating" column is the 56-asset club rating (owner formula, 2026-08-28): best 41 player
slots + best 5 eligible picks per year (2026/2027/2028) = 56 assets; 150 per vacant slot
(phantom); surplus R1–4 picks replace the lowest counted player when worth more; pick years
valued 2026 = full own projected band, 2027 = ½ own + ½ round average, 2028 = round average;
R5 picks are worth 0 and never occupy a slot. Implementation: `ui/tools/ingest_inputs.py`
(`rating56`), `ui/app/club_totals.js` (`rating56Of`), with a parity oracle in
`ui/tests/test_club_valuation_current.py`. "Depth" is the former Non-Best-23 column.

Clicking a club row filters the board to that club and shows its picks panel at the bottom —
that panel is unconditional whenever a club filter is active.

**Pocket panel methodology** (used to render as the panel's footer): league average = mean over
the ranked clubs; the Free-Agents pool is excluded from every denominator and never ranked.
Positional value uses the owner counting rule, collapse-first — a Key listing absorbs its
General counterpart (Key-Fwd absorbs Gen-Fwd, Key-Def absorbs Gen-Def; the General token is
slot eligibility, not a second position); after the collapse a player counts 1 to his position,
a DPP player 0.5 to each, except a DPP midfielder (the non-mid counts 1, the mid 0). Best-23 is
the exact greedy over the live board; Picks are the ingest's PVC band prices.

## Live identity (for the maintainer, not the screen)

Current bake at the time of this redesign: board 530a4053622c29092274fab0aa1fee7f · engine
a5550b67 · config f233d160 · curve 1c3b22d1 · store b4d23810 · book seal b6f67e94. The
authoritative copy of these is always the newest register entry, not this file.
