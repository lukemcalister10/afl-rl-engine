# PLAN — CHAPTER LEVER BUILD + DISCOUNT SWEEP · 2026-07-11 · candidate-only (no bake/tag/main)
### Directive: two owner-ruled levers on the remediated candidate + one read-only discount sweep.
### Branch `claude/chapter-lever-discount-sweep-amqpfx` FROM candidate `c02499a3`
### (claude/pick-convention-remediation-yidlbm). Base verified by fresh ls-remote: tag v2.7 = 8f8c00b1 ·
### main = a6a8aa9c · candidate = c02499a3 (unmoved). Guard 5 PASS on the candidate store 04f38dad.
### Candidate board REPRODUCED BYTE-EXACT before any work: rl_export.py → rl_app_data.json md5 8f3675f3.
### Time band 3–5h CONFIRMED (revised estimate after sizing: ~4h; will flag >2× per session rule 5).

## OWNER RULINGS FOLDED (all binding; OUT-fence enforced)
Replacement bars STAND untouched (derivation-pack BAR results REJECTED — its SIM machinery only is
reused) · G-FLOOR waiver = the named 16 (EYEBALL_LIST.md remediation floor-dipper lens; worst 13 SCAR,
Robert Hansen) · thin-cell rule DEFERRED (NOT implemented) · thresholds ×1.0524 = supervisor's pen (this
build only re-confirms the measured factor: pick_redenomination.json 1.052440, unchanged 4dp) · picks
already scale with currency in the candidate · discount LENS unruled — sweep informs, NO lens change.

## L1 — YOUNG-GDEF TRANSITION CREDIT (data-lever: ycred_table.json GEN_DEF rows only; engine code UNTOUCHED)
Home: the v2.6 L1c family (engine `_merged_recover.py:504-580`, e′ = e·(1 + w·max(R,0)·φ(g)),
w=0.9, φ=(1−g/46)²). The lever REPLACES the GEN_DEF rows of `ycred_table.json` with a TRANSITION-ANCHORED
expected re-rating R* derived by a new committed script (`scripts/derive_ycred_gdef_transition.py`):
- **Establishment** (coherent with the credit's own evidence law): cumulative career games ≥ G0=46
  within the first 6 seasons, as a GEN_DEF. Attrition-inclusive: entrants who never reach it are
  washouts contributing their measured residual (≈0 at maturity).
- **Transition probability P(pick)**: kernel-smoothed on log-pick (EFFN=35 adaptive-bandwidth, the D14
  convention) over GDEF ND/RD entrants of classes with a FULLY OBSERVABLE window (C+6 ≤ T) — trailing,
  leak-free: table_T reads only data ≤ T; years before the first observable window keep the shipped R.
- **Demonstrated-outcome anchor V̄_est,T(pick)**: the as-of-T board's OWN established GDEFs (cum games
  ≥46 as-of T, active, GEN_DEF), their engine values as-of T, kernel-weighted on THEIR draft picks —
  exactly "the established GDEFs already on this board" at T=2026, and the as-of-T equivalents in
  trailing years. Time-value: the expectation is discounted back over the MEASURED median
  years-to-establishment at the board's own live lens d=0.15 (no lens change).
- **R\*(pick) = P(pick)·V̄_est(pick)·(1.15)^(−Δmed) / V̄1(pick) − 1**, V̄1 = the cell's year-1-anchor
  kernel sum on the CREDIT-OFF matrix (derive_ycred basis). Shipped GEN_DEF row =
  max(R*, R_shipped) per grid point (strengthen, never weaken; engine still clips ≥0).
- Size comes OUT of the measurement — no number targeted. Report what it does to
  patterson/travaglia/carmichael/uwland (+duursma-adjacent cell neighbours).
- HARD CONSTRAINTS shown in the artifact: bars untouched (no REPL edit anywhere) · established-GDEF
  prices untouched BY CONSTRUCTION (φ(g≥46)=0 — code-read assertion + named check on the established
  set, e.g. langdon/berry rows byte-identical) · no blanket young multiplier (only GEN_DEF rows move;
  all other cells byte-identical in the table) · leak-free asserted by code reading in the script header.
- Inputs: fresh CREDIT-OFF walk-forward matrix regenerated on THIS candidate (RL_YOUNG=0
  s4_matrix_M1v7.py), never the stale 2026-07-08 artifact.

## L2 — SUSTAINED-FORM WEIGHTING (measure FIRST; implement only if the data supports)
Home: the M1 up-branch (`_merged_recover.py:208-225`): proven risers keep S_M1=0.46 of (Lc−Lo),
UNCONDITIONED on persistence — a sustained 2-season riser (kysaiah-pickett 90-95 twice) is haircut the
same 46% as a one-year spike; the stale early career holds Lo down (the owner's "that's silly").
- **Measure the population**: all proven players (n≥PROVEN_N) with a SUSTAINED 2-season rise — last two
  completed seasons each ≥ G_ADQ games and each avg > Lo + TOL/2 — whose board price lags the sustained
  level; list kysaiah-pickett + bailey-smith + full movers.
- **Derive from realized outcomes** (leak-free, historical seasons only): refit the M1 persistence
  fraction s = Σ(Lc−Lo)(rf−Lo)/Σ(Lc−Lo)² (the committed _m1_refine methodology) STRATIFIED:
  s_sustained (2-season risers) vs s_other (1-season risers). If s_sustained materially > 0.46 with a
  defensible n, implement a persistence-conditioned up-branch: S = s_sust when the rise is 2-season
  sustained, else the refit base — engine edit gated by a new manifest var RL_M1SUST (=0 byte-exact
  old path; config re-pin rides the lever commit). If the data does NOT support it (s_sustained ≈ 0.46
  or n too thin), commit the measurement + verdict and STOP — no forcing; owner rules on the evidence.

## ACCEPTANCE (owner's tests, all in the RETURN)
1. patterson/travaglia/uwland new values + the transition expectation stated plainly.
2. kysaiah + bailey-smith on the sustained 2-year level — or the honest data verdict.
3. PROJECTION TEST: levered board projected 6–7 yrs forward (engine's own aging machinery + the
   credit's transition expectation for in-window young); report future top-end positional mix —
   young GDEFs vanishing = FAIL regardless of guards.
4. Full gate suite on the levered candidate: reds exactly {A2, A3} expected (A12 SHOULD flip — report
   either way); G-FLOOR trips only within the waived 16; B3 candidate re-seal; B4 byte-parity;
   expected_boot re-pinned in the same commit as each artifact move.
5. G-ATTR separability: base / L1-only / L2-only / both boards committed; assert
   Δ(both) = Δ(L1)+Δ(L2) within rounding per player; 0 established-GDEF movers on L1-only.

## SWEEP — DISCOUNT SENSITIVITY (read-only SIM on the LEVERED board; NO lens change ships)
Reuse the derivation-pack SIM harness (branch f686872: run_sim.sh / patch_C_lens.py / movers.py):
patch LENS['bal'] 0.15→0.14/0.13/0.12 in the WORKSPACE engine copy only, regen board per rate, restore
+ md5-verify pristine after each. Deliver ONE table: anchor set (max-gawn vs kieren-briggs ·
marcus-bontempelli · patterson/travaglia/carmichael/uwland · kysaiah-pickett · sam-darcy ·
willem-duursma) at each rate · per-position and per-age-band mean Δ% per step · top-15 movers per
step · guard margins (three narrowest) at each rate · ONE line: the rate at which A-GAWN ordering or
A-BONT (3246 re-denominated pin) would break, if any. Frozen pick sidecar noted (does not regen with
the lens — flagged, per the pack's gotcha).

## COMMITS (per-task, G-ATTR discipline)
1. this PLAN · 2. L1 (derivation script + census + new table + L1-only evidence board + named checks)
· 3. L2 (measurement + verdict; engine+config only if supported + L2-only evidence board) · 4. levered
regen: board + book + candidate re-seal + expected_boot re-pin + full gate suite + G-ATTR ladder +
projection test · 5. sweep pack · 6. eyeball pack vs baked v2.7 (make_eyeball_list vs
board_baked_v27.json) + RETURN. Candidate PR at the end (supersedes #59 — noted in body; #59 left open).

## FENCE (OUT)
No bar changes · no thin-cell rule · no lens change shipped · no other levers · no doc-pack/constraint
edits · no bake/tag/main merge · no force-pushes.
