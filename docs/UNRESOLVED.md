# UNRESOLVED — in-flight workstreams — cut 2026-07-02
_Head `8aed420a`. Five-state vocab (PROPOSED→DERIVED→WIRED→VERIFIED→BAKED). Nothing baked past `e0ac9c377d1e`._

## 1. M1 + refined-v7 — STATE: VERIFIED (proven slice), NOT BAKED
Bake gate = **Luke's read-pass on a fixed named panel** (per BAKE_CHECKLIST.md, to be written first). Params: M1 `TOL_M1=5, G_ADQ=12, WIN=2, S_M1=0.46`; refined-v7 `cB=0.47·clip((e−1)/3,0,1)`, `e=Σmin(games_s/17,1)`, `aSc=interp(age,[20,22,24,27],[1.00,0.76,0.58,0.40])`, tail wt 0.10. Currently applied only in the matrix builder (`engine/rl_after/s4_matrix_M1v7.py`), NOT in `_merged_recover.py`. **Resume/bake:** write BAKE_CHECKLIST.md → cold audit at head → Luke read-pass → wire M1 branch + refined `cB` into `_merged_recover.py` → full re-verify (md5s, 10-panel, Maric/Langdon, book, JS-parity) → `doc_lint` → tarball. Both systemic flags resolved (KEY_FWD over-compression = speculative ceiling; Graham cohort = trust-the-level). NOTE: M1+v7 nudges the already-underpriced Rozee 2026 down ~8% (2679→2460) — flag at read-pass.

## 2. Current-season (2026) drop — STATE: mechanism PINNED (VERIFIED by decomposition); fix REWORK pending Luke's read
Driver = the **exposure-feature / recency-decay channel** (prior season decays to 0.72 while the in-progress season is ~60% elapsed + thin → `_exposure` feature drops → forward model lowers value). Cohort-VARYING (young −48% ≫ old −26%; INVERTED vs aging). NOT `_lvl_wt`, NOT the reliability-shrink multiplier, NOT aging. Two prior diagnoses FALSIFIED (reliability-shrink; correct-aging). Full: `session_2026-07-01/BUILD_report_2026-07-01_mechanism-pinned-rozee.md`. **Resume:** Luke's read on whether the exposure/decay loss is fully artifact vs partly correct; if a fix, act on the `_exposure` decay clock for the in-progress season only, scoped to younger/low-exposure players, kept OUT of `_lvl_wt`.

## 3. Decay-proration prototype (Phase-2) — STATE: PROPOSED, NON-VIABLE as specified, REWORK needed
INERT historically (byte-identical, max|Δ|=0). Lifts only ~10% of thin players (6/62 in the shrink regime); overcorrects ~35% of on-pace players (bidirectional). Overlay kept distinct from head: `session_2026-07-01/decay_proration_overlay.py` (findings in header). Report: `…BUILD_report_2026-07-01_decay-proration-prototype.md`. **Resume:** see workstream 2 rework direction (exposure-only, scoped, out of `_lvl_wt`); do NOT re-run the whole-`_swt` form.

## 4. Directive-v3 low-games / cliff-blend — STATE: PROPOSED (relay open)
+0.1-retain raise lifts Yr1 +5.6% (abs) but the unified w-blend backfires −23% (discounts played 6–22g rookies). Open decisions for Luke: (a) build a **cliff-only-blend** (blend `ns==0` only, ns≥1 stays at production) — would lift Yr1; (b) are played 6–22g rookies over-valued or fine; (c) proceed to pooled PVC-ruler retain re-derivation. Report: `…BUILD_report_2026-07-01_directive-v3-lowgames.md`. Books: `session_2026-07-01/AFL_RL_WALKFORWARD_book_M1v7_retainRaiseOnly*-proto.xlsx`.

## 5. Retain-table (SITOUT_RETAIN) — STATE: DERIVED-as-placeholder; re-derivation PROPOSED
Wired values are a DESIGNED shape placeholder, ABOVE realized measurement for RUC/KPP (nonKPP aligned). The +0.1 placeholder is WRONG-DIRECTION for KPP. **Resume:** pooled PVC-ruler re-derivation at the pick-curve stage; RUC bimodal+thin → ceiling must be DERIVED not picked; w-ramp derivable from DB (within-season penalty proration NOT derivable — season-aggregate data).

## 6. `_fut` data-artifact diagnostic — STATE: PROPOSED (scoped, not executed)
Coe/Puncher/Knevitt/Tunstill (gap ≈ −50), key by ID. Same class as Maric/Langdon (present-position `_pos_now` staleness, not an engine bug). **Resume:** per-player 2×2 decomposition (present-position bar vs `_fut` pole), systematic count.

## 7. Joel Jeffrey mediocre-proven overvaluation — STATE: PROPOSED (Luke's #1 stated priority; diagnosis-first)
Jeffrey 1773 > Ginnivan; year-8 > year-1 wrong. Overvalued list: Jeffrey/Powell/Hollands/Bruhn/O'Driscoll/Chapman/Davies/Angwin/Cox. **Resume:** per-player channel decomposition + convexity plot; separate genuine producers (Parish) from propped. Not started.

## 8. Walk-forward book reissue — STATE: WIRED + VERIFIED (regenerates)
Corrected summary metric = pooled ΣV(yrN)/ΣV(yr1)×100, SUM-RATIO, Yr1=100%, opp-matched, busts=0. `s4_render_no2003.py` variant excludes 2003 + adds a 2015-24 secondary line. Current books in `session_2026-07-01/`.

## 9. The 1.19× uniform sit-out lift — STATE: PARKED (DECISION pending, spans rotations)
Only moves the indexed-peak denominator, not the absolute peak → a bandaid on the peak. Belongs at the PVC stage. Log in DECISIONS.md with default + expiry when created.

## PARK / PVC-stage cluster (create SHIP_GATES.md before curve work — PROCESS_CHANGES §3)
1.19× (w9), SITOUT tail re-derivation (w5), no-games tail derivation — all point at the pick-value-curve stage. The stopping rule (SHIP_GATES.md, ~15-20 named relativities Luke stakes his league record on + cohort-growth + book + JS-parity gates) must exist BEFORE curve work begins.
