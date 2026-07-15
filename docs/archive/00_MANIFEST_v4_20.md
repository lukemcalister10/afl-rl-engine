# 00_MANIFEST — v4.20 · 2026-07-15 · supersedes v4.19
### The pointer file. Read it first. It tells you what is current and what to read WHEN.
### Maintained by the FABLE seat (sat 2026-07-15). Freshness check run BEFORE this filing (R100.10): PASS.
### ⚠ OWNER-INSTRUCTED 2026-07-15: the Opus seats' JUDGEMENT is not ground truth. Their measured, re-run
### figures carry their provenance tags; their FRAMINGS, groupings and prescreens are HYPOTHESES — verify
### before building on any of them. (R100.1 remains PROPOSED accordingly.)

## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.18** | 0 | first, always |
| **CORE** | **v2.7** | 0 | in full — BINDING. R98.9 / R98.10 / R100.10 folds IN; SSI move closed at v2.7. |
| **HANDOVER** | **rev138** | 0 | state at the Fable → Fable rotation seam (2026-07-15). |
| **DECISIONS** | **v101** | 0 | rulings + owner to-dos. **R100.11 is now IN THE RECORD.** Read v98 itself for verbatim. |
| **OPEN_ITEMS_REGISTER** | read its OWN header | 1 | THE DURABLE LOG. Items 110–112 are the newest. Repo-only. |
| **CONSTRAINTS** | **v1.13** | 1 | ONLY when judging a board. **L-CAPTAIN + L-SMOOTH filed; ITEM-74 blocker REWRITTEN (PART 7).** |
| **acceptance_v1_13.json** | **v1.13** | 1 | ONLY when judging a board — assert the JSON, never the prose |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | when touching the store or a derived artifact. ✅ at `docs/SINGLE_SOURCE_INVARIANT.md` (moved 2026-07-15, owner-worded) |
| ROADMAP · UNRESOLVED · CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## ⚠⚠ NO BAKE — THE BLOCKER IS REWRITTEN (owner-ordered 2026-07-15)
The old blocker cleared on "the q97m freeze + re-measure on the frozen build." **THE FREEZE DOES NOT FIX THE
CPU DEPENDENCE** (register items 105–106: four environments, four boards, ON THE FROZEN CODE). **ITEM-74 now
clears on BOTH: (1) CPU-CLASS DETERMINISM SETTLED per R100.7** — one board name across environments, the only
accepted proof being **CI GREEN ON THE AMD RUNNER PRINTING THE MATCHING BOARD md5**, OR the owner's **RULED**
tolerance — **AND (2) the reconcile on the build of record.** Machine-readable: `acceptance_v1_13.json`;
prose: CONSTRAINTS v1.13 PART 7.

## STATE AT v4.20
- **A2 IS PROVEN AT THE HEAD `a2a06c7`** — the AMD runner's own log prints board `800bf461` == the box
  (supervisor-read from the run log; register item 115). **ITEM-74 LEG 1: SETTLED via the fix road.**
- **The R100.11 REWORK DIRECTIVE IS ISSUED** (couriered to the owner; base = `a2a06c7` STRICT). HANDOVER
  rev138 filed; **seat rotation OPEN** — the incoming seat reads rev138 first.
- ⚠ **PR #81's commits are NOT ancestors of the candidate line** (merge-base, item 116) — reconcile its
  disposition before any merge word. **Do NOT merge #83 from the PR page** — one merge/promotion at chapter
  end, after the ladder, on the owner's word.

## STATE AT v4.19 (retained)
- **PR #83 (determinism fix) RETURNED AND PRESCREENED — PASS WITH NOTES (register item 114).** Mechanism
  MEASURED: the PAR table's `np.linalg.solve` (`par_build.py:70`), NOT item 106's NW story (superseded in
  place). Fix = order-fixed fsum/LU + declared fallback on one singular cell. Board `e6a8e6ef` → `800bf461`
  (8 rucks +1..+4, 796 unchanged, PICK 1 = 3000). **A1 proven; A2 PROVEN AT `84fd13f`** (AMD runner printed
  the identical md5 — first time on record). ⚠ **A2 AT THE HEAD `a2a06c7` IS PENDING** its own CI print —
  load-bearing, since the head commit touched the (unpinned) `par_build.py` after the proof.
- **ITEM-74 LEG 1: provisionally settled via the FIX road** pending that head print — no tolerance ruling
  needed. **LEG 2 (the reconcile) folds into the chapter ladder** — with hardware-independence proven, the
  environment-of-record constraint dissolves and incognito cold audits are valid instruments again.
- **NEXT: the R100.11 rework directive** (evidence-fade), recommended base = #83's surviving head; merge
  line `#81 → #82 → #83 → rework`, ONE ladder, ONE bake. **Seat rotation at this seam PROPOSED to the owner.**

## STATE AT v4.18 (retained)
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
