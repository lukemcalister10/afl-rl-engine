# DIRECTIVE — LEG D ACT 2: THE PVC RE-DERIVATION (re-fire; a FRESH chat continues from the ACT-1 checkpoint)
**v1.0** · 2026-07-17 · supervisor seat 12 · build model: **Opus via Claude Code** · ONE JOB, ONE CHAT (S2)
STATUS: ISSUED — fire when pasted by the owner. **The ACT-1 chat is RETIRED FROM WRITING** (answer-only
if consulted); YOU are the one writer on this branch from your first commit. This directive is
self-contained: everything ACT 1 learned is committed on the branch you check out — read it there,
never from chat memory you do not have.

## ⛔ EXECUTE FIRST — BEFORE READING ANYTHING ELSE (your first committed artifact is this block's proof)
```
git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/claude/legd-pvc-rederivation-o290ye
#   MUST print 12a076179525db21b6e30a37bfe16bb9d904ff47 — anything else: HALT, report, stop
#   (a moved head means the retired chat wrote after retirement — a real incident, not yours to fix).
git fetch origin claude/legd-pvc-rederivation-o290ye
git checkout claude/legd-pvc-rederivation-o290ye && git reset --hard 12a076179525db21b6e30a37bfe16bb9d904ff47
git merge-base --is-ancestor 33c8b52cb7a38d5fda2ceff5d3fb96841575c2e7 HEAD && echo ANCESTOR-PROOF-PASS
md5sum engine/rl_after/rl_model_data.json    # MUST begin 968de0c7 — else HALT.
md5sum session_2026-07-17/legd_derivation/MEMO_LEGD_construction.md
#   MUST begin abe387d9 (the ACT-1 pre-view hash; mutation ⇒ HALT THE LADDER, not just this job).
git fetch origin main && git show origin/main:docs/acceptance_v1_21.json > /tmp/acc_v121.json
md5sum /tmp/acc_v121.json                    # MUST begin 7c12d0d6 — the SEALED twin; else HALT.
```
Commit the output as `session_2026-07-17/legd_derivation/ACT2_FIRST_COMMANDS_PROOF.txt` — your FIRST
commit, before your PLAN. Then READ, from the branch: `MEMO_LEGD_construction.md` · `SITE_CENSUS.md` ·
`CHECKPOINT.md` · `PRE_VIEW_HASHES.txt` · `out/gy0_residuals.json` — they are your ACT-1 inheritance.

## THE FIVE (CORE)
- **EFFORT: High.** Why not Extra: the construction is OWNER-RULED below to the letter and ACT 1
  committed the site map and evidence — this is disciplined implementation plus gates, not open
  design. Why not Medium: it derives the curve every pick and young player prices through, wires a
  new BINDING gate, and produces the board the owner views at the ladder.
- **MODE: auto.** First committed artifact after the proof = your PLAN (name the ruled construction in it).
- **TIME: 4–6 h.** Confirm up front; flag >2×/<½×; report actual.
- **FEED:** the branch's ACT-1 artifacts (above) · `docs/DIRECTIVE_LEGD_derivation_2026-07-17.md`
  (on main — ACT 2's job list §6–§10 and deliverables govern except where amended HERE) ·
  DECISIONS v122 · CONSTRAINTS v1.19 · the fetched `acceptance_v1_21.json` (assert:
  `leg_d_placeholders.*` · `guards[G-Y0]` BINDING / fix_direction **RE_DERIVE_AT_LEG_D** — the
  retired raise-young-side remedy is history, never an instruction · `leg_c.season_prog` 0.58 untouched).
- **FENCE:** as the original directive, RE-CONFIRMED BY THE OWNER post-census: IN =
  `engine/rl_after/_merged_recover.py` (the `_PVC0` swap + V0 guard/curve/RUC-ceiling rebuild —
  ev-channel ONLY) · the curve artifact successor · `one_source_selftest.py` + the job-5 harness
  promotion · derived + `expected_boot` re-pin · your session dir. OUT = **the five `rl_model.py`
  `MA.PVC` consumers your ACT-1 census named (pickless :798 · pedestal :813 · build_pvc_v34 :714 ·
  `_natcv34` :834 · pvc_snapshot :515) — OWNER-RULED OUT: they migrate in a SEPARATE pre-ladder
  build; your census is their map; do not touch them** · the SOURCE STORE (read-only, whole leg) ·
  docs/ · Leg-B dials · SEASON_PROG · lens code.

## THE OWNER'S RULINGS (the law of this build — implement to the letter)
**R1 — CONSTRUCTION: THE COMPOSED PATHWAY CONSTRUCTION** (supersedes the memo's C-vs-A/B frame;
memo-C = the NAMED FALLBACK):
`PVC(p) = Σ_position P(position | pick p) × E[pathway value | position, pick p]`
- Pathway values fitted from realized career TRAJECTORIES: the walk-forward as-of values, end of
  years 1, 2, 3, …, over the 2004–2024 pool. **Busts at their REAL outcomes at FULL WEIGHT** — no
  survivor pool, no games floor, no threshold anywhere (L-SMOOTH / weight-don't-gate BIND).
- Evidence weighting CONTINUOUS: a prior-dominated player-year fades smoothly by the prior's share;
  never a cutoff.
- Fit 2-D (pick × career-year), per-EXACT-pick resolution, kernel-smoothed **NON-MEDIAN** (the median
  flattened the survivor tail — your own ACT-1 evidence).
- **PVC(p) = the YEAR-0 point of the fitted trajectory.**
- **ENTRY CLOSURE (the owner's named tautology, made safe):** a zero-evidence entrant's V0 is SET
  FROM the new curve — definitionally equal; the curve's content comes from outcomes, so nothing
  leaks. Implement the closure explicitly and assert it in the selftest.
- **FALLBACK TRIGGER (measured, never a preference):** build the two-ends blend (memo option C) far
  enough to COMMIT the comparison; C rules ONLY if the composed construction cannot satisfy the
  constraints below, and the trigger artifact names which constraint failed and by how much.
**R2 — THE G-Y0 GATE (owner-worded):** per-draft-class: NO gate (a strong/weak class is not a
breach). **POOLED across the whole sample: |composition-weighted mean day-after V0 − curve| ≤ 2% —
HARD.** Diagnostic: the residual PER EXACT PICK, kernel-smoothed across picks, committed as a curve
artifact for the owner's viewing — **NO decile/band tables as gated or headline numbers** (CORE
rule 7). If 2% pooled is unreachable under R1: **HALT back to the supervisor with the measured
residual — never a quiet widen, never a silent fallback.**
**R3 — FENCE:** ev-channel-only, as the FENCE above; the five-consumer migration is NOT yours.

## THE JOB (the original directive's ACT-2 list, amended by the rulings)
6. Derive per R1: OFFLINE into a STAMPED artifact (md5 of store+code+config), LOADED not refit — no
   new import-time fits (the `_iso_dec` disease; your memo's retirement/bypass plan governs).
   **`RL_PVC2=0` ⇒ board `9829d01a` byte-exact (assert the md5). `curve(1) == 3000` asserted.**
7. Gates, halt-not-warn, verdicts committed: **R104.9 strict descent HARD — all 15 shipped plateau
   violations clear** · **the R2 pooled 2% gate + the smoothed per-pick residual curve** · R104.5
   `{balanced 0.10 · contender 0.15 · rebuilder 0.05}` EXACT in every artifact · numéraire ·
   stamp-assert-not-stale · the promoted job-5 harness as the one instrument (S4/S5).
8. Pick bands wire: held pick = the LIVE curve over its ladder band [low, high] (mean); 2027 picks
   × (1 − posture discount), one application (no double-count with any lens machinery — none exists yet).
9. Planned tests RUN and committed: multi-start · prior-removed (audit #34/#35/#44) · the R1-vs-C
   comparison. Divergence = a FINDING with numbers.
10. Derived + battery: rebuild board/book/panel · re-pin `expected_boot` (the F2 designed-behaviour
    class — say so in the commit) · full battery, frozen-suite-only (S4), hash-cached (S1). **HALT
    SEMANTICS: the G-COHORT 1.30 cap is the SOLE hard halt; a sub-1.08 floor reading is REPORTED.**
    The 2019 annotation stays REPORT-ONLY (register 316/319).

## DELIVERABLES — as the original directive's list, plus:
the R1-vs-C comparison artifact · the entry-closure selftest · the smoothed per-pick residual curve
(owner-viewing) · the fetched-twin hash line (`7c12d0d6  acceptance_v1_21.json @ origin/main`) in
your PLAN. Per-gate committed verdicts with exit codes (SILENCE IS A RED) · named rows (top-10 picks
old→new · Bontempelli · Reid · Sanders · Gawn · the two largest young movers · every held pick) ·
both item-256 ledgers (positional-rank tie-break) · candidate PR **stacked on #105** · RETURN ≤30
lines · branch · head SHA · PR number · "in plain terms" close · actual time.

## STANDING CONDUCT (HANDOVER rev158 §3 — binding here)
Proof-first · one writer (the ACT-1 chat is retired from writing) · counts script-emitted, never
typed · sites from the code · stable-ID identity · SSI: the store is read-only, the curve is a
stamped derived artifact · no terminal item-counts · pre-view hashes are LAW (memo mutation halts
the ladder) · L-SMOOTH / L-SYMMETRY / weight-don't-gate / L-AXIS (the derivation is never
result-conditioned on A-PAIRS; both pairs are SCORED and reported).
