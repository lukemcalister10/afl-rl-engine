# The no-arbitrage tables, REISSUED on the #338 corrected tenure basis — owner word 2026-08-06

The walk-forward book of record gained the #338 minimum-listing-tenure rule at commit `30996f8`. The
`per_entrant` lineage that feeds these tables still carried the OLD construction, so the tables were
being measured on a basis the book had already left. This act re-emits that lineage under the same
rule and regenerates the tables from it.

**The 2026-08-05 tables are SUPERSEDED AS EVIDENCE, NOT REWRITTEN.**
`docs/evidence/noarb_2026-08-05/` is untouched — it stands on its own basis with its own README. So
are `session_2026-07-29/item271/emit_matrix_271.py` and
`session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py`: filed history and the instrument
of record. Everything in this directory is a COPY.

## The recipe (the prior README's, followed)

1. Reseed the gate workspace — the repo moved:
   `RL_VENDOR=/home/user/afl-rl-engine/vendor bash bootstrap.sh`
   (Guard 5 must report store `37ced3ce`, engine `8f0e3eb1`.)
2. Emit the matrix:
   `OPENBLAS_NUM_THREADS=1 RL_REPO=<repo> RL_FV=<repo>/engine/forward_valuation $RL_VENV/bin/python emit_matrix_338.py`
   → `per_entrant_338_confirmation.json` (~3 min; 24 as-of years).
3. `OPENBLAS_NUM_THREADS=1 $RL_VENV/bin/python noarb_table_338.py` then `noarb_ext_338.py`.
4. The harness asserts the matrix identity pins itself. **If it halts, the pins moved — re-point,
   never patch.** It did halt here, exactly as designed, and it was re-pointed (below).

## Files

| file | what it is |
|---|---|
| `emit_matrix_338.py` | copy of `session_2026-07-29/item271/emit_matrix_271.py` with the #338 rule ported in — three helpers, two changed sites, documented in its header |
| `per_entrant_338_confirmation.json` | the fresh per_entrant matrix (2,645 records; meta block carries store, engine head, n, the rule constants and emitter provenance) |
| `harness_pvc_REPINNED_pass3.py` | copy of the current re-pinned harness from main, identity pins RE-POINTED (never patched) |
| `noarb_table_338.py` / `.json` / `.txt` | copy of `noarb_table.py`, re-pointed; the tables |
| `noarb_ext_338.py` / `.txt` | copy of `noarb_ext.py`, re-pointed; the extended cuts (years 0-9, the 2020 class, the recency windows) |
| `COMPARISON_OLD_vs_NEW.txt` | the seam's hand-to-the-owner sheet: OLD vs NEW headline figures, the five largest movements with causes, and the asymmetry question answered |

## Input identities

| | value |
|---|---|
| store | `37ced3ce` (`rl_model_data.json`) |
| engine head | `8f0e3eb1` (`_merged_recover.py`) |
| v0surf sig | `af556bdca53dee20d4f73e0ae25a8127` (frozen) — **unchanged**; #338 moved the window, not the surface |
| matrix records | 2,645 · ND teaching (`teaches_curve`) 1,444 · ruled pool 1,201 |
| measured population | **1,197** — picks 1-64, classes 2004-2022, 19 distinct classes |
| force majeure | `thomas-boyd` (2013), `paddy-mccartin` (2014), dropped with the one-slot slide |
| windows extended by #338 | 698 of 2,645 records (182 of the measured 1,197) |

**Harness pins, re-pointed 2026-08-06:** `EXPECT_STORE f1e8c9fe -> 37ced3ce`;
`EXPECT_V0SURF af556bdca53d` unchanged; `EXPECT_N 1197 -> 1197`, re-measured on the new matrix, never
assumed. Non-vacuity was proven in BOTH directions before the pin moved (old pin vs new matrix HALTs
naming both values; old pin vs the #328 matrix loads at n=1197) and again after, with the matrices
swapped. The asserts themselves are byte-identical to the instrument's.

## The #338 basis

Rule commit `30996f8`, helpers at `engine/rl_after/s4_matrix_M1v7.py:53-70`, sites at `:81` and `:113`.
A drafted player is on a list for a minimum tenure whether or not the DB kept his numbers:
**4 seasons for ND picks 1-20, 3 for ND 21-40, 2 for everything else** (ND 41+ and every pool route),
counted from the route's own debut convention (entry year + 1, except MSD which debuts in its entry
year). Own data extends the minimum; an explicit `_last_listed` is a known fact and stands even when
shorter; active players are untouched. A year inside listed tenure with no scoring row is a LISTED
SITTING-OUT year, priced by the existing sit-out machinery — no new pricing rule.

The port is faithful, and it is cross-checked against the book's own published counts rather than
asserted: this emitter reaches the same **619** evidence-less store records split the same
**4 / 41 / 133 / 441** by band, with the same **27**-record residue (23 MSD whose entry-year debut
precedes the Yr1 = C+1 index, plus 4 whose explicit `_last_listed` is shorter). `ryan-willits`
(pick 21, 2004) carries `[2005, 2006, 2007]`; `lucas-cook` (pick 12, 2010) carries four years from
2011; `daniel-o-keefe`, `josh-willoughby` and `billy-morrison` each carry four.

**One deliberate reading, disclosed:** `_min_tenure` bands on `MA.effpk` — the engine's own pick,
exactly as the committed helper does — not on this emitter's force-majeure `slid_pick`. #338 is a
claim about how long a player was really on a list, which is a fact about his actual draft position;
the Q-B slide is a fit-population device. Four records (`jack-lonie`, `jack-steele`,
`jake-kolodjashnij`, `jarman-impey`) would band differently under the alternative reading; the count
and the keys are recorded in the matrix meta so the choice is measured, not asserted.

## Busts at zero — unchanged

The teaching-value zero is **downstream** of this emit and was not touched. `never_established` /
`realised_full` / `sofar` in the harness copy are byte-identical to the instrument's: a career with no
season of `>= QUAL_GAMES` (6) games still teaches **0.0** and stays in the denominator. On this
matrix 262 of the 1,197 teaching rows are never-established and every one of them still teaches 0.

`noarb_table_338.py`'s separate `'ended'` zero — a row whose vpath has run out — is also unchanged in
code. It simply fires on fewer rows at years 2-4, because the emit now emits the listed tenure years
those careers always had. The zeros move later; they do not disappear (year 2: 154 → 0, year 3:
212 → 141, year 4: 271 → 258, years 5-7 identical).

## Standing caveat

**These outcomes are under the corrected #338 rule. The shipped curve they are compared against was
derived on the pre-correction basis and re-derives at #334 stage B after the #336 ruling.** Until that
re-derivation lands, a gap between these outcomes and the shipped curve is not evidence of a curve
error.

## One red worth naming

The shipped 2026-08-05 `noarb_table.json` records `store 81d24704`, an **older** basis than the pins
its own README pointed at (`f1e8c9fe`) — i.e. the "re-run on final bytes" step in that README was
never executed against the committed table. So a raw OLD → NEW read spans a basis move as well as
#338. A CONTROL (the pre-#338 construction re-emitted on the current basis) was therefore run to
isolate the rule; the basis move proves small (≤ 4.7 mean points, ≤ 0.006 on any ratio), so the
headline read stands. See `COMPARISON_OLD_vs_NEW.txt` §0 and §3.
