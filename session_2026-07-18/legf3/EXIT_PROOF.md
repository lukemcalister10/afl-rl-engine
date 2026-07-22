# LEG F3 — EXIT PROOF · seat 13 · 2026-07-18 (single-thread; OPENBLAS/OMP/MKL/NUMEXPR=1, item 349)
Base `7b6dfc52` (F1). Store `968de0c7` · curve `56dd7a7b` — ABSOLUTE, matched. Touched set (⊆ derived fence):
`_merged_recover.py` (the 4 ruled clock sites + `_proj_w4`) · `rl_export.py` (form-anchor carry :96 + §2.iii) ·
`session_2026-07-18/legf3/`. HARD-OUT verified untouched: V0/`_iso_dec` :1121-1171 · q97m · store · curve · ui ·
`rl_model.py` (the INACTIVE `proj_from_peak` copy — REPORTED not deleted, ruling pt 4; the board runs `_proj_w4`).

## BYTE-EXACT CHAIN (the untouchable invariants — ALL PASS)
| config | built | filed | verdict |
|---|---|---|---|
| RL_LEGF=0 RL_LEGE=0 RL_PVC2=1 (balanced k=0) | `06d8af60` | 06d8af60 | **PASS byte-exact** |
| RL_LEGF=0 RL_LEGE=1 RL_PVC2=1 (Leg-E lens)   | `d85901af` | d85901af | **PASS byte-exact** |
| RL_LEGF=0 RL_LEGE=0 RL_PVC2=0 (PVC2 kill)    | `9829d01a` | 9829d01a | **PASS byte-exact** |
- pristine balanced reproduces `06d8af60` 3/3 (container faithful single-thread; the early `30d96f1f` was a
  cold-start transient, withdrawn — see PLAN §0).
- **k=0 DORMANCY UNIT TEST (ruling pt 3): PASS** (clock identity at every edited site — `test_k0_dormancy.py`,
  committed). The whole §2.vi cure is forward-lens-gated (`_LENS_FORM`/offset>0) AND RL_LEGF-gated ⇒ a no-op at
  k=0 / balanced / backward / RL_LEGF=0 BY CONSTRUCTION.
- store `968de0c7` untouched; F3 fixed board (RL_LEGF=1) = `71dbeb58` (moves ONLY the +1/+2 lens + phantom).

## ACCEPTANCE (item-352 harness, frozen-form; `scripts/backtest.py`)
### (2) THE GRADIENT — UN-INVERTED (the item-352 inversion is broken)
| cohort | pristine Δ% | **F3 Δ%** | F3 signed mean |
|---|--:|--:|--:|
| developing ≤23 | −30.5% (WORST) | **−18.5%** | −171 |
| mid 24–27 | −24.1% | −18.3% | −204 |
| veteran ≥28 | −29.1% | **−25.0% (now worst)** | −193 |
Developing went from the STEEPEST decliner (−30.5%) to the shallowest tier (−18.5%, tied with mid); veteran is
now the largest decline (real aging). The inversion (developing craters hardest) is CURED. Residual note: the
signed-mean order is developing(−171) ≥ mid(−204) but mid(−204) < veteran(−193) — not perfectly monotone; mid &
veteran are production-anchored (φ=0, untouched by the pedigree carry).

### (1) THE BACKTEST — IMPROVED BUT NOT ±5% (the honest tension)
| projection | pred | actual | error | ±5% band |
|---|--:|--:|--:|---|
| F2 −1 board → now | **556,300** | 752,427 | −26.1% | [714,806 , 790,048] **OUT** |
| F2 −2 board → −1 | 552,262 | 771,152 | −28.4% | OUT |
Improved from the investigation's `526,851` (+29k) but NOT inside ±5%. Composition-controlled (identical
roster): forward −19.9% (was −28.2%) vs backward −9.0% ⇒ the L-symmetric target is ≈−9%. **The residual is the
BOARD-WIDE forward-vs-backward asymmetry (mid & veteran decline ~2× more forward than backward), NOT the
developing-cohort pedigree strip §2.vi cures.** §2.vi (pedigree-anchored young) closed ~8pt of the ~19pt gap;
the remaining ~11pt is production-cohort forward calibration (L-SYMMETRY board-wide) — OUTSIDE the item-352 /
§2.vi pedigree scope and the ruling-353 grant. **CHECKPOINT LAW: I did NOT hand-tune the developing cohort or
lift mid/veteran forward to force ±5% — that would fake calibration the item-352 verdict does not license.**

## §2.iii DISTRIBUTED RETIREMENT (report-only; replaces the discrete X-bar)
league +1: aggregate liability (residual) = **31,091** (≈ F1 filed net 32,338 / investigation 32,836; measured
superior — names no false retirees) · expected exits ΣP = 49.5 · with-phantom 618,858 / without 602,957.
+2: liability 44,242 · ΣP 89.5. P(retire|age) SEALED (`6100f121`); φ pedigree-carry SEALED (`fd92b6fc`).

## GUARD-5 / NUMERIC STACK ANNEX
Guard-5 rl_model pin: the checkout `cc626d7d` ≠ the boot pin `a5fd3d7d` (data/expected_boot.json) — the KNOWN
PRE-BAKE RED (F1 EXIT §guard-5). FLAGGED, never self-pinned. Stack: py3.12.3 · numpy2.4.4 · scipy1.17.1 ·
sklearn1.8.0 · scipy-openblas 0.3.31.188.0 DYNAMIC_ARCH (SkylakeX dispatch) · threads pinned 1.

## VERDICT
§2.vi + §2.iii implemented, k=0 byte-exact, RL_LEGF=0 chain byte-exact, gradient un-inverted, dormancy proven.
**The ±5% backtest is NOT reached — returned as a tension (board-wide L-SYMMETRY beyond §2.vi), not bent.**
