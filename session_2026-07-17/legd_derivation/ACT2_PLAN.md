# ACT-2 PLAN — LEG D: THE PVC RE-DERIVATION (auto mode, EFFORT High)

Writer branch `claude/legd-pvc-rederivation-act2-l2hqpl`, based at the ACT-1 checkpoint
**`12a0761`** (o290ye), store `968de0c7`, engine `bea8fea8`, board `9829d01a`. First commit =
`ACT2_FIRST_COMMANDS_PROOF.txt` (six EXECUTE-FIRST verdicts PASS). This PLAN is the first artifact
after the proof. The ACT-1 chat is write-retired; I am the sole writer from `e0ee807` forward.

**Branch reconciliation (transparent):** the directive plants writing at the o290ye checkpoint; the
harness fixes my push target at `act2-l2hqpl` with a hard "never push elsewhere" rule. Reconciled by
basing `act2-l2hqpl` at `12a0761` (local-only reset — the governance commits stay safe on
`origin/main`) and opening the candidate PR **stacked on #105** (base `claude/r1067-wiring-v11-m86stv`
@ `33c8b52`, the branch ACT-1 continued from; ACT-1 was never PR'd, so this PR carries ACT-1's
inheritance commits + my ACT-2 work).

**The SEALED twin:** `7c12d0d6  acceptance_v1_21.json @ origin/main` (fetched, hashed, matches).
Version note carried from ACT-1: the engine base ships `docs/acceptance_v1_20.json`
(`6b83e336`, substance-identical operative entries: `pvc_strict_descent` · `g_y0_population` ·
posture `0.10/0.15/0.05` · numéraire `pick1==3000` · `guards[G-Y0]` BINDING /
`fix_direction RE_DERIVE_AT_LEG_D`); `docs/` is OUT of fence. I assert against the present `v1_20`
and pre-view-hash it, and cite the fetched `v1_21` twin as the sealed reference.

---

## THE RULED CONSTRUCTION — R1: THE COMPOSED PATHWAY CONSTRUCTION (owner law; memo-C = named fallback)

`PVC(p) = Σ_position P(position | pick p) × E[pathway value | position, pick p]`, the **YEAR-0 point**
of the fitted 2-D (pick × career-year) trajectory surface.

- **Data:** the ACT-1 `per_entrant.json` (base `968de0c7`) — each in-curve entrant (ND/RD, real
  pick, 2004–2024) carries `pick`, `pos`, `v0` (day-after target = the year-0 datum), `vpath` (the
  walk-forward as-of trajectory, end of years 1,2,3,…), and `pw[k]` (the engine's prior-share
  weight, 1.0 at zero football evidence → 0.11 evidence-rich). The derivation re-stamps this input.
- **Busts at REAL outcomes, FULL WEIGHT** — no survivor pool, no games floor, no threshold anywhere
  (L-SMOOTH / weight-don't-gate BIND). Every entrant is IN.
- **Continuous evidence weighting:** each player-year is weighted by its evidence share
  `w = 1 − (pw−0.11)/(1−0.11)` — a prior-dominated (circular) year fades smoothly toward 0, never a
  cutoff. The year-0 datum (`v0`) carries the entry weight.
- **Fit:** per-EXACT-pick, kernel-smoothed **NON-MEDIAN** (Gaussian-kernel weighted MEAN over
  log-pick, adaptive bandwidth widening into the sparse tail; the median flattened the survivor tail
  — ACT-1 evidence). The pooled per-pick sample carries the natural position mix, so the pooled fit
  IS composition-weighted; the explicit per-position decomposition is computed for the item-256
  ledgers. The 2-D fit lets adjacent career-years inform the year-0 slice (the "pathway" credit),
  bounded by the G-Y0 gate.
- **PVC(p) = year-0 point.** Pin `curve(1)=3000` (numéraire, L7 re-base). Enforce **R104.9 strict
  descent HARD** (isotonic-decreasing + minimal ε to clear all 15 shipped plateau violations).
- **ENTRY CLOSURE (owner's safe tautology):** a zero-evidence entrant's `v0_start == draftval ==
  _PVC0[pick] == the new curve`. Implemented explicitly by the `_PVC0` swap; **asserted in the
  selftest**.
- **FALLBACK TRIGGER (measured):** build memo-C (two-ends continuous blend) far enough to COMMIT the
  R1-vs-C comparison artifact. C rules ONLY if R1 cannot satisfy the constraints; the trigger
  artifact names which constraint failed and by how much. **If the R2 pooled 2% gate is unreachable
  under R1 → HALT back to the supervisor with the measured residual (never a quiet widen/fallback).**

## THE GATES (all halt-not-warn; per-gate committed verdicts, silence is a RED)

- **R2 — G-Y0:** per-draft-class NO gate. **POOLED |comp-weighted mean day-after V0 − curve| ≤ 2% —
  HARD.** Diagnostic: the residual **per exact pick, kernel-smoothed**, committed as a curve artifact
  for owner viewing. **NO decile/band tables as gated or headline numbers** (CORE rule 7).
- **R104.9** strict descent HARD (15 plateau violations clear) · **curve(1)==3000** · **R104.5**
  posture `{balanced 0.10 · contender 0.15 · rebuilder 0.05}` EXACT in every artifact · numéraire ·
  stamp-assert-not-stale.
- **RL_PVC2=0 ⇒ board `9829d01a` byte-exact** (md5-asserted) · **curve(1)==3000 asserted**.

## THE FENCE — R3: ev-channel ONLY (owner-reconfirmed)

IN: `_merged_recover.py` `RL_PVC2` block (the `_PVC0` swap + V0 guard/curve/RUC-ceiling rebuild, an
exact parallel of `RL_PVCADOPT` at `:1336-1342`) · the stamped curve artifact `pvc_curve_v2.json` ·
`one_source_selftest.py` + the job-5 harness promotion · derived board/book/panel + `expected_boot`
re-pin · my session dir. **OUT — the five `rl_model.py` `MA.PVC` consumers the ACT-1 census named
(pickless :798 · pedestal :813 · `build_pvc_v34` :714 · `_natcv34` :834 · `pvc_snapshot` :515): they
migrate in a SEPARATE pre-ladder build; my census is their map; I do NOT touch them.** Also OUT: the
source store (read-only whole leg), `docs/`, Leg-B dials, SEASON_PROG (0.58), lens/posture code.

## JOB LIST (directive §6–§10)

6. **Derive** offline → stamped `pvc_curve_v2.json` (md5 of store+code+config), LOADED not refit (no
   import-time fit; the `_iso_dec`/`_fit_pick_curve` chain untouched). `RL_PVC2=0 ⇒ 9829d01a`
   byte-exact; `curve(1)==3000`.
7. **Gates** wired, halt-not-warn, verdicts committed (R104.9 · R2 pooled-2% + smoothed per-pick
   residual curve · R104.5 exact · numéraire · stamp-assert) via the promoted job-5 harness (S4/S5).
8. **Pick bands:** held pick = LIVE curve over ladder band [low,high] (mean); 2027 picks ×
   (1 − posture discount), one application.
9. **Planned tests** RUN + committed: multi-start (audit #34/#35) · prior-removed (audit #44) ·
   the R1-vs-C comparison. Divergence = a FINDING with numbers.
10. **Derived + battery:** rebuild board/book/panel · re-pin `expected_boot` (F2 designed-behaviour)
    · full battery, frozen-suite-only (S4), hash-cached (S1). **HALT SEMANTICS: G-COHORT 1.30 cap is
    the SOLE hard halt; a sub-1.08 floor reading is REPORTED. The 2019 annotation stays REPORT-ONLY.**

## DELIVERABLES
The directive's list + the R1-vs-C comparison artifact · the entry-closure selftest · the smoothed
per-pick residual curve (owner-viewing) · per-gate committed verdicts with exit codes · named rows
(top-10 picks old→new · Bontempelli · Reid · Sanders · Gawn · two largest young movers · every held
pick) · both item-256 ledgers (positional-rank tie-break) · candidate PR stacked on #105 · RETURN
≤30 lines.

## CONDUCT (rev158 §3)
Proof-first · one writer · counts script-emitted not typed · per-gate committed verdicts (silence is
a red) · sites from the code · store READ-ONLY this leg · pre-view hashes are LAW (memo mutation
halts the ladder) · L-SMOOTH / L-SYMMETRY / weight-don't-gate / L-AXIS (the derivation is NEVER
result-conditioned on the Sanders/Bontempelli A-pair; both pairs scored and reported).

## FEASIBILITY (confirmed up front)
Engine runs on my base: `run_panel.sh` PASS 10/10 (Guard 5 PASS, store `968de0c7`, config gate
hash `c2d233ae`). TIME estimate 4–6 h, confirmed in range.
