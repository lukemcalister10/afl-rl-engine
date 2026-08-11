# THE TWO UI REVIEWS — SYNTHESIS · 2026-08-10 · supervisor seat

Two independent reviews of ui/ (the live app, rendered and screenshotted in Chromium at 1440px
and 390px), run in parallel with no visibility of each other:
- SIGHTED (sighted/): full project context, ordered to honor existing intent (README, PLANs,
  the parked card-and-navigation priority). 51 screenshots.
- BLIND (blind/): the owner's own protocol ("avoid being corrupted by our existing vision") —
  saw ONLY the rendered app; barred from all docs, code, and the other review; its first task
  was a comprehension test (what is this app, view by view, from the interface alone).
  58 screenshots (16 representative landed here; full set in the session record).
  One minor contamination event disclosed inside its report (an authoring comment in the page
  head, seen while probing the DOM; both affected reads were set aside).

Seat verification: the deciding contrast figure re-computed independently — #525c6d on
#181c25 = 2.53:1 exactly as reported; the font-size sprawl confirmed (31 distinct sizes in
matchday.css alone; the review's 41 counts JS-injected styles).

## THE COMPREHENSION VERDICT (blind, the measurement no invested seat can produce)
The bones communicate: with zero context the blind seat correctly identified the product
(a valuation board for a fantasy/dynasty AFL league; one currency over 804 players + picks;
16 league clubs over the real 18; a single owner-user with a WORKING/PUBLIC split), and rated
7 of 9 views "certain". The Clubs drill-in is "the best screen in the app"; the Trade Desk
"works"; PUBLIC mode is "the cleanest idea in the product". THE REDESIGN IS A REFINEMENT
PROBLEM, NOT A REBUILD.

## CONVERGENT (both reviews independently — the high-confidence redesign core)
1. THE ENGINEERING LEAKS INTO THE PRODUCT. Hashes, guard badges, seals in the masthead;
   documentation essays pasted into layouts; the +2yr lens dumps a reconciliation block that
   made the blind reviewer think the app was broken. → One provenance line/footer + progressive
   disclosure. (Blind: decode failures 1/3; sighted: offender 3, verdict 4.)
2. TYPOGRAPHY HAS NO SYSTEM. No self-hosted face, OS fallbacks, 31-41 distinct sizes, no
   scale. → One family (true condensed cut + tabular figures), ~seven-step scale, three
   typographic voices. (Sighted verdict 2; blind direction.)
3. THE ACCENT IS SPENT EVERYWHERE. The volt/lime carries club names, totals, tags — so
   nothing is loud. → Volt gets ONE job (the user's position / the number they came for);
   club identity to the neutral ramp; green/red strictly for direction with the arrow
   grammar. (Blind change 2; sighted verdict 7 + direction.)
4. TABLES ARE NOT YET TABLES. 804 rows, 51,202px of scroll, no search, no sort, no sticky
   header, ~8 players per screen. → Search + sortable columns + sticky header; density up
   (~36px rows, hairline rules); virtualize past ~100 rows. (Blind 3/6; sighted 3.)
5. DEAD COLUMNS SHIP BY DEFAULT. Three columns of dashes (Δ VS ROUND et al.) + OVER FREE
   (= VALUE − 190, rank-identical to its neighbour). → Delete; flip DELTA_BASE_DEFAULT to
   the populated basis. (Blind 1; sighted 4.)
6. THE TRADE DESK IS UNFINISHED MECHANICALLY though its idea is the product's best: no
   remove control on staged assets, no clear, clipped typeahead. (Blind 10; sighted 5.)
7. THE VALUE BAR ENCODES NOTHING AT DEPTH (identical stub for 88% of rows; hue ramp).
   → One desaturated fill on a rank-relative or log scale. (Blind 7; sighted 7.)
8. MOBILE DROPS THE WRONG COLUMNS (position lost, dead pill kept; tooltip blocks its own
   trigger). (Blind 5; sighted 10.)
9. THE DIRECTION IS SHARED — both landed, independently, on: a broadcast-grade data
   terminal — keep near-black + volt, push the discipline the rest of the way, don't
   replace the identity. This matches the owner's stated instinct.

## DIVERGENT (where our assumptions became visible — the blind protocol earning its keep)
- THE VOCABULARY IS NEVER DEFINED. Only the blind seat could find this: AFFL, SCAR, "bake",
  the GUARD badges — the tab name and the currency itself are unexpanded anywhere in the
  interface; the sighted seat (inside our frame) never tested them. Worse: WORKING labels a
  stat "Δ VS LAST BAKE" where PUBLIC labels the same field "Δ VS PREV ROUND" — the two modes
  disagree about what it measures. → Define-on-first-use + a consistent label.
- TWO OUTRIGHT BUGS (blind): the Movers table labels EVERY row DNP — including players whose
  own cards show a Round 22 score; the trade translator goes out of range (−11,376 called
  "roughly a top-1 pick" when pick 1 = 3,000). → Fix regardless of any redesign ruling.
- QUANTITATIVE FLOOR FAILURES (sighted): --faint #525c6d at 2.53:1 carries every column
  header, unit label, rank, AFL club name and footnote in the product — 44% short of the
  AA floor (seat-verified); 16-colour palette with 3 gradient-only stops and a duplicate red.
- Native OS <select> controls inside the bespoke control bar (sighted offender 1) — the
  single loudest "default, not designed" tell.

## THE PROPOSED REDESIGN ACT (for the owner's ruling — not started)
Phase 0 (bug fixes, no ruling needed beyond a word: the DNP mislabel + the trade translator
range — small, testable). Phase 1 (CSS-only: contrast floor, accent discipline, value bar,
focus/hover states, define-on-first-use). Phase 2 (layout: typography system, toolbar rebuild,
density, mobile column priority, provenance footer). Phase 3 (structural: search/sort/sticky/
virtualized rankings, player picker on the card, trade desk completion, diagnostics switch).
Each phase lands behind the same discipline as every act: branch-held, before/after
screenshots as the side-by-side, the owner's word to merge.
