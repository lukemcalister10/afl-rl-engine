# 00_MANIFEST — v4.27 · 2026-07-15 · supersedes v4.26
### The pointer file. Read it first. It tells you what is current and what to read WHEN.
### Maintained by the FABLE seat (seat 7). THIS FILING: THE v2.10 SEAM — the "evidence over calendars"
### chapter is BAKED (tag v2.10 = d14efae) + PROMOTED (main = a64c47f, two-parent PR #97). The 1.335
### G-COHORT waiver REVERTS to 1.30 (CONSTRAINTS v1.16 + acceptance v1.16). DECISIONS → v104 (the R103.x
### seam set) · HANDOVER → rev142 (the merged PVC+FLEX chapter's whole queue). CORE/SSI unchanged.
### ⚠ OWNER-INSTRUCTED: prior seats' JUDGEMENT is not ground truth — verify before building.

## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.27** | 0 | first, always |
| **CORE** | **v2.8** | 0 | in full — BINDING. |
| **HANDOVER** | **rev142** | 0 | THE POST-BAKE SEAM handover — the merged PVC+FLEX chapter's whole queue. |
| **DECISIONS** | **v104** | 0 | rulings + the owner's CURRENT to-dos. Read the register for verbatim. |
| **OPEN_ITEMS_REGISTER** | read its OWN header | 1 | THE DURABLE LOG (v155+). Repo-only. |
| **CONSTRAINTS** | **v1.16** | 1 | REPO-ONLY (P1) — fetch + grep when judging a board. **G-COHORT bound back to 1.30 (waiver reverted)** · AXIS RULE (PENDING-OWNER). |
| **acceptance_v1_16.json** | **v1.16** | 1 | REPO-ONLY (P1) — `cohort_waiver` REVERTED (1.30) + `standing_fails` + `audit_rule`. |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | when touching the store or a derived artifact (docs/). |
| ROADMAP · UNRESOLVED · CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## STATE AT v4.27 (THE v2.10 SEAM)
- **BAKED + PROMOTED:** tag **v2.10 = `d14efae`** (byte-identical shipped state to the CI-verified bake
  `83f945a`) · main **`a64c47f`** (two-parent PR #97; parents 7ba44a3 + d14efae) · board `790136a3` ·
  store `b1fd0bce` · seal `99be9b36` · pick 1 = 3000. Prior tag v2.9 = `9f8ae76` intact. Verify main CI
  went GREEN (AMD runner printing 790136a3).
- **WAIVER REVERTED:** G-COHORT HALTs at 1.30 again. The v2.10 y5 was 1.3057 (waived zone) — a fresh
  board there would now HALT; the merged chapter must return under 1.30 or seek a new waiver.
- **L-CAPTAIN OPERATIVE.** **cm_400 FROZEN (R103.7) — item 75's ingestion blocker CLEARED.**
- **NEXT: PVC + FLEX (merged, R103.2)** — baseline set complete (calibration item 170 · census-v2 item
  165 · aging closed) · opens on the AXIS RULE ruling + the flex registers. See HANDOVER rev142.

## STATE AT v4.22 (the chapter's finish line, pre-loaded — RETAINED for lineage)
- **CHAPTER (owner-ruled EXTEND then SPLIT):** Fix 1 + absence (PR #85) + determinism (#83) +
  evidence-weight (#89, prescreen PASS item 134) + THE IMPROVER BUILD (**WRITER IN FLIGHT** — _eo
  two-directional · L-SYMMETRY · the S_AGE 29-tail). Candidate line `#82→#83→#85→#89→improver`, every
  base STRICT, one straight history.
- **IN FLIGHT (Tier 3, parallel):** the pedigree DEEP-TAIL measurement (item 136 — the owner rules the
  tail's shape on its return; a one-constant re-pin leg may ride before the ladder) · the book
  CALIBRATION v1.1 (the PVC chapter's scoring baseline).
- **QUEUED (fires on the improver's return):** the rl_model-PIN job (Tier-1-lite; L-CAPTAIN prerequisite
  1; file-overlap with the improver's fence forbids running it earlier).
- **THE LADDER IS PRE-LOADED:** the cold-audit seed skeleton is authored (item 137 — two placeholders:
  final branch + head). Owner's sealed reads: WRITTEN (on paper, pre-viewing — OQ-D satisfied).
- **ITEM-74:** LEG 1 SETTLED (item 115). **LEG 2 = the measured-vs-claimed reconcile of THIS chapter's
  cold audit** — the blocker clears at this ladder. Then: bake on the owner's word → promote → main GREEN.
- **A9 (Ginnivan/Ward):** EXPECTED-FAIL-BY-LAW (owner-ruled item 135) — the auditor scores it, never
  flags it (acceptance_v1_14 `standing_fails`).
- **NEXT CHAPTER (opens at the bake):** PVC/pick-curve on the REWORKED spec — items 130–132 verbatim law;
  consumes the baked evidence-weight machinery; the calibration baseline + tail ruling are its inputs.

## THE ITEM-74 BLOCKER (as rewritten at v4.21; LEG 1 since SETTLED — see STATE AT v4.22)
The old blocker cleared on "the q97m freeze + re-measure on the frozen build." **THE FREEZE DOES NOT FIX THE
CPU DEPENDENCE** (register items 105–106: four environments, four boards, ON THE FROZEN CODE). **ITEM-74 now
clears on BOTH: (1) CPU-CLASS DETERMINISM SETTLED per R100.7** — one board name across environments, the only
accepted proof being **CI GREEN ON THE AMD RUNNER PRINTING THE MATCHING BOARD md5**, OR the owner's **RULED**
tolerance — **AND (2) the reconcile on the build of record.** Machine-readable: `acceptance_v1_13.json`;
prose: CONSTRAINTS v1.13 PART 7.

## STATE AT v4.21
- **P1 EXECUTED (owner-ruled):** PK now carries Tier-0 + SSI only; CONSTRAINTS + acceptance are REPO-ONLY.
- **P3 RULED:** the seat-tools directive is ISSUED (Tier-3, `tools/seat/`, read-only, disjoint fence — runs
  IN PARALLEL with the rework per S3).
- **THE R100.11 REWORK IS IN FLIGHT** (owner fired it 2026-07-15) — the one store/engine writer.

## STATE AT v4.20 (retained)
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
