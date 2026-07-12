# PLAN — BAKE v2.8 (execution) · 2026-07-12 · branch claude/bake-v2-8-execution-5oyddf

MODE auto, first commit = this PLAN (the bake checklist, ordered). HALT-not-warn throughout.
Owner rulings incorporated (2026-07-11): L1 defender transition credit ADOPTED (incl. CA-4 floor drift +
CA-11b day-zero re-orderings, disclosed/blessed) · discount rate **15%** · Travaglia read WAIVED · Kysaiah
read WAIVED · PVC letter DEFERRED to v2.9 (nothing pick-curve implemented here).

## BASE VERIFICATION (done, first action)
- Full-URL ls-remote: tag **v2.7 = 8f8c00b10e2ef3a1b68dd6864594f5bdfef91340** (unmoved) ✓
- Candidate `claude/chapter-lever-discount-sweep-amqpfx` = **bc2929fe59f018939a8e5b2409da75921f352972**
  (audited head, unmoved — proceed) ✓
- main = **5819bd1** (newer than the directive's c18951c1); delta since a6a8aa9c = docs-only
  (single new file docs/OPEN_ITEMS_REGISTER.md, +94 lines) — verified ✓
- Fresh checkout at the candidate; bootstrap Guard-5 PASS store **04f38dad** == pinned ✓
- ruling_config_check PASS: RL_PVCFIT=0 (engine default + live env + export bake-guard present + guard
  before write) + RL_LTI_CLOCK=advance (engine default + env + manifest pin) — the four R3 layers + R-i ✓

## THE CHECKLIST (ordered)
- **(0) A-DARCY TRIPLE-LOCUS ATTRIBUTION** — closes CA-9 BEFORE gates. From the committed
  L1-only/base/full boards + the injury machinery, emit sam-darcy's attribution across young-convexity
  ceiling · KPF-speculative · availability layer; state which mechanism (or absent/zero). One page,
  committed. → `DARCY_ATTRIBUTION.md`.
- **(1) DISCOUNT RATE** — owner ruled 15% == the candidate's SHIPPED rate. SKIP the config change; note
  it. No regeneration, no re-base. (The sweep measured 14/13/12 read-only; none ship.)
- **(2) FULL GATE SUITE** from clean bootstrap. EXPECT: FAIL exactly {A2, A3, A12} (A12 tests the board,
  stays red at 15% regardless; Travaglia read WAIVED recorded beside it) · B5 raise-only (lowered=0) ·
  B3 seal PASS · B4 parity PASS · B1 PASS · panel 10/10. ANY unexpected deviation = HALT.
- **(3) v2.8 ARTIFACTS + REPORT_STATES** — commit the regenerated v2.8 matrix + gates snapshot; assert
  figures match this run; advance `data/report_states.json` to the v2.8 identity in the SAME commit
  (label + evidence together; the standing "Advance it" ruling executes here per DECISIONS v93 §43).
- **(4) FINALS** — board + book + eyeball list regenerated at 15%; identities table (store · engine ·
  config · matrix · board · book-seal md5s) committed; expected_boot re-pinned to the v2.8 identity.
- **(5) CANDIDATE FINAL** — push; state branch · head SHA. (Bake head, see NOTE below.)
- **(6) STOP** — output the owner's two commands verbatim (v2.8 tag at the bake head; main promote,
  clean fast-forward). I do NOT tag. I do NOT promote.

## KNOWN DEVIATIONS TO RESOLVE / SURFACE (flagged, not buried)
1. **PANEL PIN IS STALE.** `run_panel.sh`'s inline EXPECT array (and `PANEL_EXPECTED.txt`) carry an
   ORPHAN prior candidate's values (W4+L1c, store e1b4d8bf) unrelated to this chapter-lever candidate;
   the candidate's own committed `panel_levered.txt` shows RESULT: FAIL, yet its RETURN/expected_boot
   claim "panel PASS 10/10". The engine reproduces the candidate board (md5 9ecbe0fa) byte-exact (B4
   PASS) and deterministically. Bake resolution (BAKE_CHECKLIST §4 "re-pin expected values ... or the
   candidate's recorded successors; PANEL_EXPECTED 10/10"): re-pin the panel to the reproduced v2.8
   board values, assert 10/10 byte-exact. Surfaced in RETURN for owner sight.
2. **main carries docs/OPEN_ITEMS_REGISTER.md** (added after the candidate branched); the candidate diff
   shows it as a deletion. This is a promote-time merge detail for the owner's fast-forward, not a bake
   artifact. Noted; no doc-pack edit here (OUT of fence).

## NOTE ON BAKE HEAD / PR
The directive's step (5) names PR #60 / the candidate branch as the bake head. My git fence permits pushes
ONLY to the designated branch `claude/bake-v2-8-execution-5oyddf`. The bake work is therefore committed on
that branch, BASED on the candidate head bc2929fe (identical content + the bake finalization commits). The
bake head is this branch's head; the owner's tag/promote commands reference that SHA. Stated explicitly so
the owner tags the right commit.

## FENCE
IN: the checklist above (bake finalization: re-pin panel/expected_boot, regen derived artifacts, advance
report_states, identities table). OUT: no doc-pack/constraint edits · no PVC implementation (v2.9) · no
age-curve · no new levers · no force-push · no tag · no main merge (owner-only).
