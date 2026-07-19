# 00_MANIFEST — v4.52 · 2026-07-17 · supersedes v4.51
### v4.52 (item 329): THE SEAT-12 ROTATION FILING. HANDOVER → rev159 (Leg D COMPLETE + SHARD-AUDITED
### at PR #109 `e4177c2`; seat-13 queue = five-migration → Leg E → ladder → ONE bake → v2.11).
### DECISIONS → v123 (R107.x folded; the open tail read; the incremental-currency design). Seat 12
### CLOSES (correction ledger ×5, owned).
### v4.51 (item 314): THE RE-SEAL FILING (seat 12's sealing job DONE). CONSTRAINTS → **v1.19** ·
### acceptance → **v1.21** — the ⚠ stale flags CURED (s_dial_selection RETIRED, s=0.10 OWNER-SET per
### R106.3; G-Y0 BINDING + fix_direction → RE_DERIVE_AT_LEG_D) — + the item-301 RECONCILIATION TABLE
### at CONSTRAINTS PART 8. SPEC v1.4 → **OPERATIVE** (seat-12 review APPROVED, item 313; one minor
### line-51 provenance survivor rides the next spec version). HANDOVER → rev158. NEXT: the LEG-D
### directive (groundwork @ `9845180`).
### v4.50 (item 312): THE SEAT-11 ROTATION FILING. HANDOVER → rev157 (the true seam: Leg C
### CONTENT-COMPLETE at PR #105 `33c8b52`, prescreen GREEN; the parallel batch delivered and
### owner-merged; seat-12 queue = the v1.4 review → the re-seal → Leg D → E → ladder).
### DECISIONS → v122. SPEC → **v1.4 PENDING SEAT-12 REVIEW — v1.3 governs until the verdict**
### (item 310). The CONSTRAINTS+acceptance RE-SEAL = SEAT 12's SEALING JOB, after the v1.4 review (item 311;
### cargo = item 290, grown by 295/300/306/310).
## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.52** | 0 | first, always |
| **CORE** | **v2.8** | 0 | in full — BINDING. |
| **HANDOVER** | **rev159** | 0 | THE ROTATION DOC — the seam state · seat-13 queue · standing conduct. |
| **DECISIONS** | **v123** | 0 | carried rulings (R107.x folded) + open reads + to-dos. Register for verbatim. |
| **OPEN_ITEMS_REGISTER** | read its OWN header | 1 | THE DURABLE LOG. Repo-only. |
| **CONSTRAINTS** | **v1.19** | 1 | REPO-ONLY. Sealed at item 314 (+ the PART-8 reconciliation table). |
| **acceptance_v1_21.json** | **v1.21** | 1 | REPO-ONLY — assert the JSON. The v1.20 ⚠ flags are CURED (item 314). |
| **SPEC_PVC_FLEX_CHAPTER** | **v1.4 — OPERATIVE (review APPROVED, item 313)** | 1 | §1 + §1b BINDING. |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | before touching the store or a derived artifact. |
| ROADMAP · UNRESOLVED · CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## STATE AT v4.52 (THE SEAT-12 ROTATION SEAM)
- **SHIPPED:** tag v2.10 = `d14efae` (790136a3 · b1fd0bce). Unchanged.
- **CANDIDATE LINE:** …273463e (f2f077b2, PR #103) → 6306378 (PR #104; ee70335a · 0efdc5d6) →
  **`33c8b52` (PR #105; board 9829d01a · store 968de0c7 · book 228ed814) — PRESCREEN GREEN,
  triggers clear (item 306)**. QUARANTINED: 2b64630 · f2bf728.
- **LEG D COMPLETE + SHARD-AUDITED (items 313–328):** candidate …→ `33c8b52` (PR #105) → `12a0761`
  (ACT-1) → **`e4177c2` (PR #109; board `270a2c5f` · store `968de0c7` · curve payload `89c14729`)**.
  THEN: the FIVE-MIGRATION build → Leg E → the ladder (riders i–iv ride the viewing) → ONE bake →
  **v2.11**. Round-entry tool on main (PR #108 merged).
- **TOOLS ON MAIN:** first_commands.sh + the prescreen proof-hook · viewing_pack.py (owner-merged
  PRs #106/#107).
- Seat 12 CLOSED (ledger ×5, owned). Owner at this seam: PK sync (v4.52 · rev159 · v123) · the
  seat-13 token + revoke seat-12's · fire the five-migration directive when issued.
