# RETURN — BAKE v2.8 (execution) · 2026-07-12

**Branch:** `claude/bake-v2-8-execution-5oyddf` (bake work based on the audited candidate `bc2929fe`).
**Bake head SHA:** set at the final commit of this branch (this RETURN commit) — see `git rev-parse HEAD`.
The tagged/promoted content identity (store/engine/board/book-seal) is pinned in `IDENTITIES.md` +
`data/expected_boot.json` and is independent of which commit carries this note.

## BASE VERIFICATION
tag v2.7 `8f8c00b` unmoved · candidate `claude/chapter-lever-discount-sweep-amqpfx` `bc2929fe` unmoved
(audited head) · main `5819bd1` (newer than the directive's c18951c1; delta since a6a8aa9c = docs-only,
one file `docs/OPEN_ITEMS_REGISTER.md`) · bootstrap Guard-5 PASS store `04f38dad` · RL_PVCFIT=0 (four
layers) + RL_LTI_CLOCK=advance asserted.

## PER-STEP COMMITS
- (0) PLAN — `988cb79`
- (0) A-DARCY triple-locus attribution (closes CA-9) — `7c134d4`
- (1) Discount rate 15% == candidate shipped rate → SKIP the config change, noted (no regen, no re-base).
- (2) Full gate suite reproduced byte-exact + panel re-pinned — `ddf3479`
- (3) v2.8 matrix + report_states advanced (label+evidence together) — `bce91a2`
- (4) Finals: expected_boot re-pinned + identities table — `abd612c`
- (5) Push — done (this RETURN is the final record commit).

## DARCY ATTRIBUTION VERDICT (CA-9 CLOSED)
Availability layer is the SOLE active suppressor: `avail_nerf −677` (present-season proration for his
real 2026 absence; LTI Section A, out 2026 / return 2027), `lti_return_hc 0.0` (no return haircut).
Young-convexity ceiling ABSENT (`cvx 1.0`). KPF-speculative ABSENT (`mech None`). No layer clips his
ceiling; he lifts to **4013** (layer-off ≈ 4690). L1 is GEN_DEF-only and does not touch him.

## GATE RESULTS (reproduced byte-exact, clean bootstrap)
`VERDICT: FAIL=3 FEATURE=1 PASS=17 PENDING=4 STRUCK=1` — reds **exactly {A2, A3, A12}** as ruled.
A12 [DC] board test (Travaglia 792 vs Moraes 1023) stays red at 15%; Travaglia read WAIVED (recorded).
B1/B3/B4 PASS · B3 seal a19b3cb8 · B4 regen board 9ecbe0fa == shipped · B5 lowered=0 (raise-only) ·
panel 10/10 (re-pinned to board 9ecbe0fa — see NOTE).
**Three narrowest margins (class-sum convention):** G-COHORT y4 128.6 vs 130 → 1.4 pts · A10 Curnow
0.55 vs 0.50 → +0.05 · A8 Berry 2.14× vs 2.00× → +0.14×.

## RATE APPLIED
15% (owner ruling) — identical to the candidate's shipped rate; no re-base, no unexpected reds.

## REPORT_STATES ADVANCED
CONTROL → **v2.8** (head 7a07e369 / store 04f38dad / board 9ecbe0fa / book-seal a19b3cb8) — this also
registered the head as BAKED (was PROTOTYPE/UNREGISTERED). PREVIOUS → v2.5 efea88e5 (outgoing control).
The standing "Advance it" ruling executed here (DECISIONS v93 §43).

## FINDINGS SURFACED (not buried)
1. **Panel pin was stale.** `run_panel.sh` + `PANEL_EXPECTED.txt` carried an ORPHAN prior candidate's
   values (W4+L1c, store e1b4d8bf, never baked); the candidate's own `panel_levered.txt` read FAIL while
   its RETURN/expected_boot claimed 10/10. The board itself reproduces byte-exact (B4 PASS, md5 9ecbe0fa,
   deterministic ×2). Resolved per BAKE_CHECKLIST §4 by re-pinning the panel to the v2.8 baked board →
   PASS 10/10. Not test-fitting: the pinned values equal the B4 board and the SWEEP 15% shipped column.
2. **Main promote is NOT a clean fast-forward.** See OWNER COMMANDS below.

## OWNER COMMANDS (owner-only — I did NOT tag, I did NOT promote)

### 1. Tag v2.8 at the bake head (lightweight, matching v2.6/v2.7)
```
git fetch origin claude/bake-v2-8-execution-5oyddf
git tag v2.8 origin/claude/bake-v2-8-execution-5oyddf     # tags the branch tip (baked state pinned in IDENTITIES.md)
git push origin v2.8
```

### 2. Promote to main — MERGE, not fast-forward (the directive's "clean fast-forward" is NOT available)
Main diverged from the bake lineage at `a6a8aa9c` and kept moving during the bake (latest `6e409fa`, a
docs seam-pack: HANDOVER rev130, DECISIONS v94, CORE v2.3, MANIFEST v4.6): it carries 8 docs-only commits
(`OPEN_ITEMS_REGISTER.md` + the board-view ruling records + the seam pack) that the candidate branched
*before*. All are under `docs/`, none touched by the bake — re-verified conflict-free against the latest
main via `git merge-tree`. A
fast-forward is therefore impossible. A force-push would DESTROY those main commits — do not. The safe,
**conflict-free** promote (verified via `git merge-tree`: result preserves `OPEN_ITEMS_REGISTER.md` AND
carries the bake's board/matrix/report_states) is a merge commit, consistent with the repo's standing
merge-commit policy:
```
git checkout main
git pull origin main
git merge --no-ff claude/bake-v2-8-execution-5oyddf -m "Promote BAKED v2.8 (chapter-lever L1 + pick redenomination) to main"
git push origin main
```
Tag first, then merge (so `v2.8` points at the audited baked head, which the merge makes an ancestor of
main — the same shape as v2.7). If you would rather main be linear, rebase the branch onto main first,
but that rewrites the audited candidate SHAs and needs re-tagging — the merge above is cleaner and keeps
the audited head intact.

## TIME ACTUAL
~1h55m (band 1–2h confirmed; no blow-out).

## IN PLAIN TERMS (for the owner)
The v2.8 board bakes clean at your 15% dial. Your young defenders' transition credit is in, the three
gates that were always going to stay red on the data are red exactly as expected, and everything else
passes. Sam Darcy checks out: the only thing holding his number down is his real 2026 injury (a
present-season discount that unwinds when he's back in 2027) — nothing in the model is unfairly capping
his ceiling. Two honest snags I fixed/flagged: the fixed-panel check was pointing at an old, unrelated
board and reading FAIL, so I re-pointed it at the actual v2.8 board and it now reads 10/10; and the
final "promote to main" step can't be the simple fast-forward the plan assumed, because main has moved on
with your board-view ruling notes since this candidate was cut — so promote with the one-line merge I've
written out above (it keeps your notes and never force-pushes), not a fast-forward. The v2.8 tag and the
main promote are yours to run — I stopped here.
