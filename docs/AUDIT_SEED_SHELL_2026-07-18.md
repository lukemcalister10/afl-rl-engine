# AUDIT SEED SHELL — the ladder's S6-sharded cold audit · seat 13 · 2026-07-18
### **STATUS: SHELL — addresses unfilled. Not a seed until seat 13 fills every ⟦SLOT⟧ at the
### ladder (after the Leg-E candidate's prescreen) and the leak-guard scrub passes.** Per CORE
### (AUDITOR seat) · OQ-C (manifest = addresses, never results) · S6 (shard sizing) · items
### 319/323 (leak-guard) · item 328 (shard-noted ladder pattern).

## THE AUDITOR CONTRACT (restated so the seeder never improvises)
Incognito, memory-free, OUTSIDE the Project. Seeded with EXACTLY: this pack's integrity manifest +
`acceptance_v1_21.json` + the shard's check list. NEVER seeded: conclusions, build-reported
numbers, prescreen output, our internal vocabulary. Every check is phrased COMPUTE-AND-REPORT
(the auditor states what it computed and the value it got), never confirm-that-X-equals-Y.
Reconciliation of audit-computed vs build-claimed happens SUPERVISOR-side, after return.

## INTEGRITY MANIFEST TEMPLATE (fill at seeding; addresses only)
repo: https://github.com/lukemcalister10/afl-rl-engine.git
branch: ⟦LADDER-BRANCH⟧ · pinned head SHA: ⟦LADDER-SHA⟧ (assert unmoved by ls-remote on entry)
store: engine/rl_after/rl_model_data.json, md5 ⟦STORE-MD5⟧ (boot-guard asserts before anything)
curve artifact: ⟦CURVE-PATH⟧, payload stamp ⟦CURVE-PAYLOAD-MD5⟧ (a KAT names WHAT it hashes)
acceptance: docs/acceptance_v1_21.json (assert entries by KEY; prose restatements are void)

## SHARD PLAN SKELETON (S6: each shard sized to ONE tool-use window; heavy computes backgrounded
## with completion markers + sparse polling; heavier ⇒ split further or verify-by-stamp)
- **SHARD A — environment + guards:** fresh shallow clone at the pin · boot-store assertion · the
  five SSI guards run · every derived-artifact stamp vs current inputs (S1 pattern) · report each
  verdict + exit code. SILENCE IS A RED: a check with no output FAILED.
- **SHARD B — gates recomputed from the frozen suite:** pooled G-Y0 (report the computed %) ·
  strict-descent violation count · curve(1) value · the R104.5 discount triple as applied ·
  the three narrowest margins observed. No expected values seeded; report what was computed.
- **SHARD C — migration proofs re-run:** per-consumer byte-hold checks re-executed from the
  committed proof artifacts' inputs (not their outputs) · kill-switch-off board hash computed and
  reported · store md5 after full pipeline run.
- **SHARD D — Leg-E invariants re-run:** horizon-zero lens board hash vs balanced board hash
  (computed, both reported) · the single-discount synthetic-pick unit test re-executed per
  posture · the smoothness sweep re-run (violation count reported).
- **SHARD E — external checklist by ADDRESS:** ⟦GPT-§5 list — owner couriers the clean-room §5
  failure-mode list at seeding; each item CONVERTED to a code/artifact address check before
  inclusion. FALLBACK if not couriered: the item-324 category set — draft-order echo/circularity ·
  censoring handling · descent verification · target-definition consistency · external
  calibration cross-check — each likewise converted to an address.⟧

## THE LEAK-GUARD (mechanical; runs on the assembled seed BEFORE sending; items 319/323)
1. Vocabulary scan: grep the seed for our doc terms (leg names, rider labels, memo titles,
   "composed pathway", seat/register language). Hit ⇒ rewrite in neutral terms or drop.
2. Number scan: grep the seed for every md5/percentage/value appearing in build returns and
   prescreens of this chapter; ONLY the manifest's own pins above may survive. Hit ⇒ remove.
3. Conclusion scan: any sentence telling the auditor what it *should* find ⇒ remove.
The scrub's grep lists are assembled at seeding time from the chapter's actual returns; the scan
commands and their exit codes are committed alongside the seed as the guard's proof.

## RETURN FORMAT (per shard, ≤30 lines)
What was computed · the value(s) · exit codes · anything that would not run (a non-run is a
finding, not a skip) · NO pass/fail language against unseeded expectations — verdicts are the
supervisor's reconciliation job.
