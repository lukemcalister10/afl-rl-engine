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
| MC-15 | 28/8 ORDER 49 availability exposure blend — TAU 2.5 owner-locked; the Taylor/Taylor cliff removed at the one law (`final = w·played + (1−w)·sitter`, `w = 1 − exp(−games/2.5)`, tenure 1–4, entry age <22, 1–12 career games); 78 movers, net −1,467 | combined-build-46-47-48-sll5g → order49-avail-blend-28-8 | TAU_LOCKED_2026-08-28_please_lock_in_tau_2_5_and_build_that |

Full incident records for every ruling ID live in the repo registers (`docs/registers/`).

## The walk-forward retrospective (2026-08-29) — retro points

`ui/data/movers.js` now carries eleven extra points, `retro-r14 … retro-r24`, each `kind: "retro"`
with an `after_round`. A retro point is the CURRENT engine's answer for that round's football:
the season clock set to the round's derived `calendar_progress` / `exposure_pace`, every 2026
scoring row truncated to as-at-that-round, the whole active board priced through the engine's own
`ev()`, and every mutated row restored and asserted. They were produced on ONE engine load
(`docs/evidence/walkforward_retro_2026-08-29/pass_retro_series.py` under `tools/harness_run.py`);
the per-round subprocess builds it replaced paid a ~12-minute load eleven times over.

THE CONTROL: R24's truncation is a no-op, so `retro-r24` must reproduce the live board exactly.
It does — 0 diffs, 0 missing over 804 rows (`RETRO_ONELOAD_VERDICT.json`) — which validates the
clock handling, the currency mapping (`ev()/_PL_F` plus the display layer's owner overrides) and
the export path in one assertion. Re-run that control before trusting any re-emission.

A retro point is NOT a board this application ever served, and three places read "the newest /
every point" as the record. All three exclude `kind === "retro"`, and each would be a live defect
without it:

| Place | What excluding retro prevents |
| --- | --- |
| `core.lineage` THE ONE ASSERT (`ui/app/movers.js`) | `retro-r24`'s in-process pricing becomes "the newest stored point", never equals the served board, and fail-closes the entire Movers tab |
| `round_finalize._newest_point_vs_live_board` | the same assert on the producer side halts the NEXT round's finalisation |
| the player-card history (`ui/app/history.js`) | eleven re-pricings interleave into every card, doubling the table with movement that never happened |

The from/to selector is where the two worlds are allowed to meet, and a pair with exactly one retro
end is banner-labelled (`core.crossesWorlds`).

THE DEFAULT PAIR is the newest consecutive retro pair (R23 → R24), not the newest stored report.
A stored report is priced under the model that was live that week — R24's predates ORDER 45/46/47/48
and the ORDER 49 blend — and its `previous_round` is the last out-of-round column, so the tab used
to open on `MC-11 → Round 24`. The owner asked for "round 23 to 24, under the current model"; the
retro pair is literally that, and its `to` end is the live board.

PARTICIPATION ON A ONE-ROUND RETRO PAIR: a range whose two retro ends are one round apart IS that
round, so `core.compare` reads played / DNP / score from that round's own stored report — football
facts do not depend on which engine priced the player. Every other range (multi-round, mixed-world,
spanning an out-of-round column) keeps the honest "not recorded", and `ui_defects_2026-08-21` asserts
both directions so the enrichment can never silently widen.

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

Live as at 2026-08-29: board 4a52cc4490f950c7b7856fc28ddcb949 · engine 17243c16 · config
d4f3c3cf · curve 1c3b22d1 · store b4d23810 · book seal 619fe67f. The ORDER 49 availability
blend moved the board 530a4053 -> 4a52cc44, the engine a5550b67 -> 17243c16, the config
f233d160 -> d4f3c3cf and the seal b6f67e94 -> 619fe67f; the store did not move.

This block is a convenience, and it goes stale the moment an act lands — the AUTHORITATIVE copy
is always the newest register entry, and the machine-readable one is `data/expected_boot.json`.
Read one of those before trusting this.
