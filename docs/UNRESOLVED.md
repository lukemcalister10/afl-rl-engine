# UNRESOLVED — in-flight workstreams — cut 2026-07-02
_Head `8aed420a`. Five-state vocab (PROPOSED→DERIVED→WIRED→VERIFIED→BAKED). Nothing baked past `e0ac9c377d1e`._
_D4 (02/07 pm): BAKE CANDIDATE exists — branch `claude/d4-bake-candidate-m2-m1v7` (engine `fb39d88a`, M1+v7 + M2 wired,
board 11P/6F) — holds for the external cold audit + Luke's bake word. Canonical head untouched. See §1/§2 updates below,
`session_2026-07-02/directive4_notes.md`, and `BOARD_LAYERS_OBITUARY.md` (ONE-price executed, workstream 10)._
_D5 (02/07 late): B1 REDEFINED by Luke (cross-cohort AVERAGE law; per-cohort UNGATED but printed every board run) — the D4
B1 bake-blocker DISSOLVES (new-B1 PASS at head/candidate/control). M1+v7 decomposed PER TERM: M1 owns the whole A3 −0.034;
v7-cB owns the Curtis squeeze AND an indiscriminate half of the 2020 markdown (ρ≈0, producers hit like mediocrity); v7-asc
owns the mediocrity-concentrated half (ρ=+0.71 — Luke's shocking-draft read confirmed on concentration) plus the B5 blowout
(implicated in 27 of the 31 candidate joiners). Yr8+ tail floors derived from the generating rule (.011/.012/.021/.012 for
d=8/9/10/11+ vs flat .05 — numbers only, decision pending Luke). LTI register CONTENT committed (32 LTI + 11 out-for-2026).
See `session_2026-07-02/d5_ask2_perterm_decomposition.md` + `directive5_notes.md`._

## 1. M1 + refined-v7 — STATE: WIRED (bake candidate, D4 02/07), NOT BAKED
D4: transplanted verbatim into `_merged_recover.py` ON THE CANDIDATE BRANCH (commit `0806d90`); read-pass endorsed per the
D4 directive; full candidate verification run (board 11P/6F; A5/A9 flip green; Maric 1409→1178, Langdon 593→575 — the
canonical restore-verify pins move at candidate by design). OPEN + ENGINE-CAUSED (D4 control): B1 per-cohort backstop
16/17 on the candidate-rebuilt book — cohort 2020 yrs4-6 R=97/98/95 vs 109/110/110 on the same-builder canonical control
→ the M1+v7 wiring breaks the 2020 cohort's growth-law backstop; live bake-blocker for the cold audit + Luke's read.
Also priced: the overlay costs A3 ~0.05 (see §2) — the A2/A5/A9 repairs vs A3/B1 damage is now Luke's explicit tradeoff.
D5 SUPERSEDES the B1 line above: Luke REDEFINED B1 (cross-cohort average; per-cohort ungated) → the 2020 backstop failure
NO LONGER BLOCKS (new-B1 PASS at the candidate, avg peak N=4 at 147.6). The overlay tradeoff is now priced PER TERM
(`d5_ask2_perterm_decomposition.md`): M1 = Curtis +184 / A3 −0.034 / 2020 +3.9%; v7-cB = Curtis −195, Ward −324,
2020 −8.0% INDISCRIMINATE (ρ≈0); v7-asc = 2020 −7.9% mediocrity-concentrated (ρ=+0.71), B5 +29. Luke's overlay ruling
reads from that doc.
Pre-D4 text (params + provenance) follows:
Bake gate = **Luke's read-pass on a fixed named panel** (per BAKE_CHECKLIST.md, to be written first). Params: M1 `TOL_M1=5, G_ADQ=12, WIN=2, S_M1=0.46`; refined-v7 `cB=0.47·clip((e−1)/3,0,1)`, `e=Σmin(games_s/17,1)`, `aSc=interp(age,[20,22,24,27],[1.00,0.76,0.58,0.40])`, tail wt 0.10. Currently applied only in the matrix builder (`engine/rl_after/s4_matrix_M1v7.py`), NOT in `_merged_recover.py`. **Resume/bake:** write BAKE_CHECKLIST.md → cold audit at head → Luke read-pass → wire M1 branch + refined `cB` into `_merged_recover.py` → full re-verify (md5s, 10-panel, Maric/Langdon, book, JS-parity) → `doc_lint` → tarball. Both systemic flags resolved (KEY_FWD over-compression = speculative ceiling; Graham cohort = trust-the-level). NOTE: M1+v7 nudges the already-underpriced Rozee 2026 down ~8% (2679→2460) — flag at read-pass. DIRECTIVE-2 (02/07): read-pass pack produced (`session_2026-07-02/readpass_pack_M1v7_8aed420a.md`, 2025 basis, 2026 column excluded); in scratch the prototype flips A9 (Ginnivan 1677 > Ward 1253) and the Weddle leg of A2 and clears the A5 floors, but Curtis (1087) stays below Ward (1253) — the Ward-pattern reds are NOT fully explained by the un-baked prototype (H-WARD falsified as sole cause).

## 2. Current-season (2026) drop — STATE: M2 WIRED (bake candidate, D4 02/07) + M3 sibling DERIVED (D4); acceptance ceiling QUANTIFIED
D4: M2-exposure wired in `conditional_prior._exposure` on the candidate (Luke's written go; f=0.545, kill-switch RL_EXPO_F;
byte-exact at f=1 re-verified; A3 0.642→0.658 on the candidate base). M3 (proportional tenure/age — the sibling lever Luke
queued) DERIVED, NOT wired: design + backtest `session_2026-07-02/m3_design_proportional_tenure.md` — zero on-pace collateral,
B-gates hold, Rozee +10.7%, but A3 reaches only 0.728 @fE=0.58 (full-pin ceiling 0.863) → **pre-registered A3 ≥0.80 NOT
reachable via the clock channels; the residual is (a) the M1+v7 overlay's own −0.05 on the A3 base (Rozee −8% v7 flag) and
(b) Rozee's thin-2026 level channel.** Luke reads M3 + rules on the A3-vs-overlay tension. A10 resolved separately: amended
0.70→0.50 (data-caused, provisional) — PASS 0.55 at candidate. Pre-D4 text (mechanism pin — still valid) follows:
DIRECTIVE-3: split bundle shows channel a is AGE/TENURE-dominated (young −40.1% age/ten vs −12.9% decay/exp; old −26.1% vs −0.6%).
Derived lever (prorated exposure clock, f=0.545, evidence-replacement scope s=clip(1−g_Y/11,0,1)) passes every safety bar — ZERO
on-pace collateral (0/288 >2%), byte-exact at f=1 + historically, B-gates hold — but reaches only A3 0.706 (need 0.80) and cannot
touch A10 (Curnow 13g on-pace → DATA-CAUSED candidate under [DC] triage). Design doc (Luke reads before wiring):
`session_2026-07-02/dropfix_design_M2exposure.md`. Decisions: (a) wire M2-exposure as-is; (b) rule on the age/tenure sibling lever
(same calendar asymmetry, engine-wide meaning change); (c) A10 uphold-or-amend. Pre-D3 text follows (mechanism pin — still valid):
Driver = the **exposure-feature / recency-decay channel** (prior season decays to 0.72 while the in-progress season is ~60% elapsed + thin → `_exposure` feature drops → forward model lowers value). Cohort-VARYING (young −48% ≫ old −26%; INVERTED vs aging). NOT `_lvl_wt`, NOT the reliability-shrink multiplier, NOT aging. Two prior diagnoses FALSIFIED (reliability-shrink; correct-aging). Full: `session_2026-07-01/BUILD_report_2026-07-01_mechanism-pinned-rozee.md`. **Resume:** Luke's read on whether the exposure/decay loss is fully artifact vs partly correct; if a fix, act on the `_exposure` decay clock for the in-progress season only, scoped to younger/low-exposure players, kept OUT of `_lvl_wt`. DIRECTIVE-2 (02/07): decomposition re-run at head reproduced the pinned numbers exactly (Rozee −827/−368; d_level +5/+1/+5%); the `_lvl_wt` thin-below-par hypothesis (H1) is again FALSIFIED.

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

## 10. ONE-price ruling (board vs engine) — STATE: EXECUTED (D4 02/07; Luke ruled delete-not-disable, in writing)
D4: board valuation path DELETED (commit `f2bb22b`); `rl_export.py` renders engine `ev()` (named-row parity byte-exact);
`BOARD_LAYERS_OBITUARY.md` carries per-layer magnitude/rationale/resurrection refs; view re-plumbed to as-of-year engine
values (retired back-rows flat until the Y-aware `delisted()` lands — a candidate-branch item). REMAINING: the actual re-cut of Luke's
trading board file waits for the bake decision (ONE new board total); B4 stays red vs the orphaned `b8f9e998` until then.
Pre-D4 evidence text follows:
Gates price `_merged_recover.ev()`; the traded board prices `TR.production_value` (a different function). Dual-path ruler:
A4/A9/A11 flip PASS↔FAIL between paths; board −7.6% total, median player |Δ| 24.9%, 57% differ >20%, Spearman 0.90. Live board
`b8f9e998` = orphaned pre-2026-06-21 export-code artifact (PVC[1]=3883 pre-anchor; 785 players; no git state reproduces it —
D3 ASK 4). Pack: `session_2026-07-02/board_layers_pack_D3.md`. **Resume:** Luke's ruling (his presumption on record: ONE price —
at-rest board == engine; layers promoted-or-deleted), then re-ship the board from the ruled path.

## 11. A2 residual (Curtis vs Ward, amended gate) — STATE: drop-contamination FALSIFIED (D3); next isolation PROPOSED
Curtis's lowness is NOT the calendar artifact (decay/exposure share +0.5%; scoped fix moves him 0.0%). The v7 band compression
holds him down (M1-only lifts him to 1441; v7-only cuts him to 977); post-overlay he sits 66% of his pick-age-matched producer
line (Ward 77%). **Resume:** per-term v7 ablation (cB-only vs asc-only) across Curtis + the matched five + a GEN_FWD-vs-MID
replacement/pole check. Amended A2 (Curtis >= 0.90×Ward, Luke 02/07) stays red until that isolation runs.

## PARK / PVC-stage cluster (create SHIP_GATES.md before curve work — PROCESS_CHANGES §3)
1.19× (w9), SITOUT tail re-derivation (w5), no-games tail derivation — all point at the pick-value-curve stage. The stopping rule (SHIP_GATES.md, ~15-20 named relativities Luke stakes his league record on + cohort-growth + book + JS-parity gates) must exist BEFORE curve work begins.
