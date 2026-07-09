# PLAN — Store correction (2 rows) + collision sentry + re-seal — auto-mode first artifact

Directive: `DIRECTIVE_store_correction_reseal_v1` (manifest tier 6, MODE=auto, EFFORT medium, band 1.5–3h).
Base = `origin/main` @ **900e4bf** (PR #51 gate-integrity merged; verified fresh vs live remote — local
`main` ref had been stale at 00d82dd per DECISIONS §31; working branch already at 900e4bf). Branch:
`claude/new-session-rahz82`. Feed asserted: acceptance_v1.6.json · CONSTRAINTS_v1.6 · DECISIONS_v87 (§29–§30 govern).

## Verified facts inherited (not re-derived)
- `max-king-stk` (St Kilda KFWD, pick 4, yr 2018) carries `_by: 2007`, `_bd: "2007-01-09"` — both borrowed
  from `max-king-syd`. True DOB **7 Jul 2000** → `_by: 2000`, `_bd: "2000-07-07"`.
- `ben-murphy` (Brisbane, Irish Cat-B, pickless, 0 games) carries `_by: 2027`, `_bd: "2027-02-01"` (future).
  True born early **2007** → `_by: 2007`, `_bd: "2007-02-01"`.
- Impossible-age scan (supervisor, all 2652 rows): these 2 are the ONLY hits.
- Owner ruled: RE-SEAL NOW, at post-fix values (DECISIONS §30).

## Ordered commits (fence §4)
1. **PLAN** (this file) — auto-mode first artifact.
2. **Store fix + boot pin**: correct the 2 rows in the ONE source `engine/rl_after/rl_model_data.json`;
   update `data/expected_boot.json` `store` md5 in the SAME commit (its own `_doc` rule). No other row/field.
3. **Collision sentry** (permanent, halt-not-warn): small in-repo data file `engine/rl_after/collision_sentry.json`
   (extensible; King pair first) + assertion wired into `one_source_selftest.py` (which CI runs). Asserts both
   King rows exist exactly once, fields as pinned (stk: _by 2000/pick 4/yr 2018/StK; syd: _by 2007/pick 49/yr
   2025), and no cross-copied identity fields. Any merge/swap/bleed FAILS the build.
4. **Regenerate + re-seal**: rebuild board+book from the fixed store (bake mode); re-commit the shipped board
   `data/rl_build/rl_app_data.json` (resolves the §26 benign Brodie-block B4 diff as a side effect) and the
   committed book `engine/rl_after/s4_matrix_M1v7.json`; re-seal `data/book_stable_seal.json` at the POST-FIX
   stable-key sha256 (head/store/config/sealed_by/date; cite DECISIONS §30).

## Remnant hunt (fence §2)
Whole-repo sweep already run: NO secondary store carrying `_by`/`_bd` exists (single-source rewire 2026-07-05
deleted the `.pre_stage0`/`.stage0` lookalikes). The engine reads age only from `_by` at `rl_model.py:365` —
no hardcoded King/Murphy override. Slug hits are derived artifacts (book/board — regenerated here) or sealed
historical session outputs + docs (REPORT-ONLY, flagged, not rewritten). Final verdict recorded in the return.

## Proofs the return carries (fence §5)
King/Murphy board BEFORE/AFTER with age attribution (King repriced ~25yo not ~18yo — expect a real move;
Murphy ~minimal, 0 games) · every OTHER board row byte-identical (non-mover parity) · G-COHORT / B1 cohort
values before/after (≈unchanged expected — STOP if material) · frozen-suite reds unchanged (A2/A3/A12 only).

## Green bar (fence §4)
Fresh bootstrap: five single-source guards + panel 10/10 + B-gates + ruling-config + config manifest — all
green; correction-sticks canary shows the fixes SURVIVE a full rebuild. New CI green on the branch.

## Out of scope
Any other store row/field · lever/surface/valuation code · frozen tolerances · docs pack (supervisor's pen) ·
bake/tag/main promotion (owner merges) · second copies of any data file · force-push.
