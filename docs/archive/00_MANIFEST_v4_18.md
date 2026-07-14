# 00_MANIFEST — v4.18 · 2026-07-15 · supersedes v4.17
### The pointer file. Read it first. It tells you what is current and what to read WHEN.
### Maintained by the FABLE seat (sat 2026-07-15). Freshness check run BEFORE this filing (R100.10): PASS.
### ⚠ OWNER-INSTRUCTED 2026-07-15: the Opus seats' JUDGEMENT is not ground truth. Their measured, re-run
### figures carry their provenance tags; their FRAMINGS, groupings and prescreens are HYPOTHESES — verify
### before building on any of them. (R100.1 remains PROPOSED accordingly.)

## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.18** | 0 | first, always |
| **CORE** | **v2.6** | 0 | in full — BINDING. The R98.9 / R98.10 / R100.10 folds are IN. |
| **HANDOVER** | **rev137** | 0 | state at the seat-6 → Fable seam. Still current; rev138 comes at the next seam. |
| **DECISIONS** | **v101** | 0 | rulings + owner to-dos. **R100.11 is now IN THE RECORD.** Read v98 itself for verbatim. |
| **OPEN_ITEMS_REGISTER** | read its OWN header | 1 | THE DURABLE LOG. Items 110–112 are the newest. Repo-only. |
| **CONSTRAINTS** | **v1.13** | 1 | ONLY when judging a board. **L-CAPTAIN + L-SMOOTH filed; ITEM-74 blocker REWRITTEN (PART 7).** |
| **acceptance_v1_13.json** | **v1.13** | 1 | ONLY when judging a board — assert the JSON, never the prose |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | when touching the store or a derived artifact. ⚠ still at repo ROOT — move QUEUED on the owner's word |
| ROADMAP · UNRESOLVED · CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## ⚠⚠ NO BAKE — THE BLOCKER IS REWRITTEN (owner-ordered 2026-07-15)
The old blocker cleared on "the q97m freeze + re-measure on the frozen build." **THE FREEZE DOES NOT FIX THE
CPU DEPENDENCE** (register items 105–106: four environments, four boards, ON THE FROZEN CODE). **ITEM-74 now
clears on BOTH: (1) CPU-CLASS DETERMINISM SETTLED per R100.7** — one board name across environments, the only
accepted proof being **CI GREEN ON THE AMD RUNNER PRINTING THE MATCHING BOARD md5**, OR the owner's **RULED**
tolerance — **AND (2) the reconcile on the build of record.** Machine-readable: `acceptance_v1_13.json`;
prose: CONSTRAINTS v1.13 PART 7.

## STATE AT v4.18
- **BOTH WRITERS HAVE RETURNED:** **PR #82** (Fix 1 + the absence term; prescreened PASS at item 111 by
  seat 6 — **the Fable seat RE-VERIFIES independently before any rung advances**) and **the determinism
  bisect-then-fix** (report with the owner; **not yet seen by any supervisor eye**). Reports courier ONE AT A
  TIME, on the owner's word.
- **R100.11 (evidence-fade) ⇒ PR #82 NEEDS A REWORK before any bake.** The rework directive is drafted after
  both prescreens land; merge-line placement is an OWNER decision (options in DECISIONS v101 §2).
- **CI: red at last measurement.** Whether the determinism return changes that is exactly what its prescreen
  establishes — from its committed artifacts, never its prose.
- **ONE WRITER AT A TIME still governs; no writer is in flight as of this filing.**

## REPO STATE (verify yourself — fresh clone, full-URL ls-remote, cite SHAs)
- **main = `a734559` at authoring; THIS FILING MOVES IT.** Base pins read "at or after + docs/-only diff",
  NEVER strict equality on main (CORE, THE BASE PIN; strict equality is for store/engine bases).
- Tagged board of record **v2.9 = `9f8ae76`** (board `81e48293` · store `b0c39d78` · engine `2030e5df` ·
  config `69ead79b` · rl_model `952ddb3d` · **pick 1 = 3000**). A1 PROVEN on the pinned hardware class.
- PR #82 head **`e7d980eb`** · board **`e6a8e6ef`** · engine **`fef5719d`** · book **`2a2df435`** (item 111,
  seat-6 prescreen — re-verification pending).
- Census branches: flattery `d6c481f6` (**verified twice — item 110, superseded mark**) · discontinuity
  `3ca74f3` (L-SMOOTH's standing instrument).

## WHAT CHANGED AT v4.18
- **CORE → v2.6** — pen restored (R98.9/R99.3, suspension AND restoration recorded) · handover exception
  (R98.10 verbatim) · **CHECK-THEN-FILE order (R100.10)** · SSI move queued on the owner's word.
- **CONSTRAINTS → v1.13 (+ acceptance):** **L-CAPTAIN** (R98.1) and **L-SMOOTH** (R98.2) filed — both
  BINDING; L-CAPTAIN **LOCKED, NOT WIRED** (three wiring prerequisites recorded) · **ITEM-74 blocker
  rewritten** (above) · every measurement_status clearing clause updated.
- **DECISIONS → v101:** R100.11 filed verbatim; its two declared-open assumptions flagged for ruling;
  PR #82 rework disposition recorded. v100 archived.
- **REGISTER → v101 (own header):** item 110's "flattery unverified" **SUPERSEDED IN PLACE** (verified twice;
  the Fable seat re-ran it 2026-07-15 from committed data: **123 / +19,168, exact**) · **item 112** (this
  filing).
