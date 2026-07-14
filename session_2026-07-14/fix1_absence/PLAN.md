# PLAN — FIX 1 + THE ABSENCE TERM (Option C) · candidate build

**Auto-mode first artifact.** Base = `addef03` (q97m-freeze head; engine `2334f570`, store `340a7a32`,
board `3dc19fbb`). Branched from `addef03`, NOT main. **TIER 1 CANDIDATE — no bake, no tag, no merge.**
Main is RED (register item 102); item 74 OPEN. This build ends in a candidate PR; the owner views the list.

File-disjoint from the CI-environment job: **`boot_guard.py` and `bootstrap.sh` ARE NOT TOUCHED.**

## The two levers (owner-ruled; do not re-derive)

**LEVER 1 — FIX 1 (R99.1 TAKE).** Smooth small-sample damping in `_lvlcurr`: season weight `gm` becomes
`w(g)=g²/(g+5.8)`. `w`: 0→0 · 1→0.147 · 2→0.513 · 3→1.02 · 5→2.32 · 8→4.64 · 12→8.09 · 22→17.41. Env-gate
`RL_DAMP` (default ON); `RL_DAMP=0` ⇒ `w=g` ⇒ byte-exact base. It damps a season by its own sample size —
thin evidence counts for little. Fixes Ladhams (1 game @ 97) DOWN and the cold-cameo crash (Jamarra) UP.
Report `w(g)` at 0/1/2/3/5/8/12/22 and state whether `w(1)≈w(0)≈0` holds (it does NOT exactly: w(1)=0.147;
the 0→1 jump is cut 6.8× but is not zero — report plainly).

**LEVER 2 — THE ABSENCE TERM (Option C, owner-ruled 2026-07-14).** A missed season carries a PREDICTIVE,
MULTIPLICATIVE penalty on a returning player's projected level. Env-gate `RL_ABSENCE` (default ON);
`RL_ABSENCE=0` ⇒ byte-exact. NOT a phantom row (rejected — a phantom lifts collapsed players). NOT a
threshold (R98.2). Applied on the projected level `cp._lvl_eff` (= `_inferM1`), the number `ev()` consumes.

Spec, per returning player with a mid-career calendar gap whose return year ≤ Y:
- `age_pre` = age at last-played-season-before-gap (the D2 R2 index).
- `absfrac(age)` = `|truth_adj(age)| / L_REF`, `L_REF=75` (D2 R1 mean pre-absence level), clamped `[0,0.20]`.
  `truth_adj` = the D2 R2 **mean-reversion-adjusted fitted age curve** (out_r2.txt), used verbatim as a
  lookup+interp — NOT bins (CORE rule 7). The positive artifact below age ~20 (data-free extrapolation) is
  clamped to 0 (an absence is never a bonus). Curve (level pts): 22→−5.55 · 23→−5.73 (trough) · 27/28→−3.25
  (prime plateau, NOT zero) · 30→−5.14 · 34→−11.88.
- `fade` = `clip(1 − npost/3, 0, 1)`, `npost` = #(≥10-game seasons after the return year, ≤Y). Full penalty
  in the return season; fades to 0 after 3 re-established seasons. **ASSUMPTION (law 5, NOT measured): the
  penalty is on the return season and FADES; it is not permanent.** Declared, flagged for owner.
- **THE DOUBLE-CHARGE FIX.** The decay `ld^(Y−yr)` already charges absence (D2 R3: mean −1.7 lvl pts; owed
  −4.9 ⇒ shortfall ≈ −3.2). We deliver ONLY the gap by netting the decay PER PLAYER: compute
  `L_nogap = _inferM1(gap-filled copy)` (D2 R3's `shift_out_gap`, REUSED), then
  `L_target = L_nogap·(1 − absfrac·fade)` and return `min(L_base, L_target)`. Because we cap at the
  multiplicative truth and never lift, the NEW term never causes total > truth; where the decay already
  over-charges (Jamarra), the new term contributes 0. **Report per-player: charged-by-decay ·
  charged-by-new-term · TOTAL vs the measured curve. If the NEW TERM drives total past the curve ⇒ HALT.**

Assumptions declared (law 5): (a) multiple absences pay ONCE per return episode (age-indexed, not scaled by
gap length); (b) the penalty fades (above). Population (law 4): applied to NON-established players too
(≥1 prior played season, dropping the ≥2-base filter) — the curve is extrapolated below the established
base; **who is covered and who is not is reported.**

## Attribution (P0, G-ATTR — path-additive, declared order Fix1→Absence)
Four fresh-process boards: base (0,0) · Fix1 (1,0) · Absence (0,1) · Both (1,1). Legs: `L1=fix1−base`,
`L2=both−fix1`; `Σlegs ≡ both−base` by telescoping ⇒ `max|Σlegs−total|=0`. Report each lever's delta.

## Deliverables
- P0 three ablated boards + per-lever deltas + path-additivity.
- P1 complete affected-row list (every gap player: name·age·season(s) missed·level & value before/after·
  ΔSCAR·double-charge split; every Fix-1 mover, esp. the M4 list; Jamarra under (a)(b)(c)), sorted by |ΔSCAR|.
- P2 G-COHORT y4/y5/y6 on the FROZEN suite (B1 July-8 walk-forward). **Breach ⇒ STOP, do not tune.**
- P3 every guard (B1/B5/B6/B3/B2/B4/D14) + anchors (A-BONT clear 3392, A-GAWN, A-PAIRS 2&3, A-FADE, A-PEAK)
  + PICK 1 = 3000 (structural: PVC read from pinned file; synths gap-free & flat-games ⇒ inert). 3 narrowest.
- P4 REBUILD the board + book (`rl_export.py` + `s4_matrix_M1v7.py`); re-pin `expected_boot.json` board md5
  (old 3dc19fbb → new); record old→new for every re-pinned stamp. ⚠ `expected_boot.json` is shared surface
  with the CI job — flag any conflict, do not resolve.
- `w(g)` table; double-charge split; stated assumptions; plain-terms close.

## Fence
IN: `engine/rl_after/_merged_recover.py` (two levers, env-gated) · `data/expected_boot.json` (re-pin only) ·
rebuilt board+book · `session_2026-07-14/fix1_absence/`. OUT: boot_guard.py · bootstrap.sh · the store · the
PVC/pricing curve (R99.4 SMOOTH THE AVERAGES, NOT THE PRICE) · λ · TOL_M1 · _radq · S_AGE · model_config.json
(no new manifest vars ⇒ config pin holds) · docs · CI. NO phantom · NO threshold · NO magnitude tuned to a gate.
