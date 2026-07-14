# 00_MANIFEST — v4.15 · 2026-07-14 · supersedes v4.14
### STATUS: OFFICIAL — owner-screened 2026-07-14; files at the seam.
### The pointer file. Read it first. It tells you what is current and what to read WHEN.

## ⚠ BEFORE ANYTHING ELSE
**MAIN IS RED.** CI's panel fails on all ten players. **PR #74 completed the config manifest and did NOT
fix it.** The live hypothesis is that **the board may not be deterministic** — a `GradientBoostingRegressor`
is refitted at import time on every run. **A job is measuring it. Read that return before you act on
anything in this pack.** See HANDOVER rev135, first section.

## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.15** | 0 | first, always |
| **CORE** | **v2.5** | 0 | in full — it is BINDING. ⚠ **CORE v2.6 is FABLE'S FIRST PEN JOB** — it folds R98.9 (pen restored) and R98.10 (the handover exception). Until it lands, CORE v2.5's rule 8 and its FRESHNESS CHECK do not describe the rules in force. |
| **HANDOVER** | **rev135** | 0 | state + the single action order |
| **DECISIONS** | **v98** | 0 | rulings + owner to-dos |
| **OPEN_ITEMS_REGISTER** | **v81** | 1 | the durable finding log (repo-only; pen-maintained) |
| **CONSTRAINTS** | **v1.11** | 1 | ONLY when judging a board |
| **acceptance_v1.11.json** | **v1.11** | 1 | ONLY when judging a board |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | when touching the store or a derived artifact |
| ROADMAP | v9 | 2 | on demand |
| UNRESOLVED | — | 2 | on demand |
| CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## WHAT CHANGED AT v4.15
- **CONSTRAINTS → v1.11** (+ `acceptance_v1.11.json`): **G-BOOK is FILED** — the owner's BOOK-PARITY LAW
  becomes a named, citable guard. **Filed INCOMPLETE and knowingly so:** the book's stamp does not cover
  `rl_model.py`, the file where `capt_prem` lives. **Closing that gap is a prerequisite of the
  captain-curve wiring.**
- **HANDOVER → rev135:** main is red; the config-manifest diagnosis was wrong; the determinism question is
  now the single action order. Carries the seat-5 correction ledger.
- **DECISIONS → v98:** the captain curve APPROVED (bar 105 · 1:1 from 120) · the SMOOTHNESS LAW · λ
  REJECTED · the games-based trust basis REJECTED · the pedigree must FADE not VANISH · the cliff fix is
  NOT the Jamarra fix · the completeness architecture PARKED FOR FABLE · **documentation is screened before
  it is pushed.**
- **DECISIONS v98 AMENDED after owner screening:** **R98.1's credit line CORRECTED** — the plain-English
  restatement carried `107.4`, which is **CAPT_THRESH from the LIVE, SATURATING curve the new one
  replaces**, not the approved curve's asymptote. **The dials and the credits were always right**
  (Gawn 16.34 · Bont 9.85 · Daicos 4.96 reproduce to the decimal). Credit = **projected level − 109.66**.
  1:1 at 120 reads **0.997** — a logistic approaches 1 and never touches it; **do not gate on "exactly."**
- **R98.9 — R98.8 CLOSES AT THE SEAM; the supervisor's docs/-only TOKEN PEN is RESTORED for Fable.**
- **R98.10 — THE HANDOVER EXCEPTION TO THE FRESHNESS CHECK** (+ its BINDING directional guard: PK behind
  the repo on ANY pack doc ⇒ **HALT**).
- **SINGLE_SOURCE_INVARIANT → v1.3** — the header did not move when SILENCE IS A RED was added, leaving
  two materially different documents both calling themselves v1.2. Corrected.
- **OPEN_ITEMS_REGISTER → v81:** items 65–70 (pen-pushed at `7989d21`) + item 61 CLOSED (the captain
  curve's dials are SET) + R98.9 / R98.10 + this correction ledger.

## THE SEAM PACK (Project knowledge) — SYNCED 2026-07-14
Project knowledge was **verified byte-identical to the repo** and carries the seven files the seam-pack
rule names: **manifest v4.15 · CORE v2.5 · HANDOVER rev135 · DECISIONS v98 · CONSTRAINTS v1.11 +
acceptance v1.11 · SSI v1.3.**

**⚠ R98.10 — THE HANDOVER EXCEPTION (BINDING).** *On disagreement the repo wins — **other than at a seat
handover.*** The incoming seat reads the seam pack from Project knowledge, **files it to the repo as its
first act** (archiving superseded versions), and thereafter the repo is home and wins as before.
**DIRECTIONAL GUARD:** compare PK against the repo **doc by doc, by header version**. PK ahead or equal ⇒
file and proceed. **PK BEHIND on ANY doc ⇒ HALT and tell the owner.**
**SCOPE: pack docs ONLY.** SHAs, board/store md5s, the register, returns, code and artifacts are NEVER
read from Project knowledge — a seat verifies state live and cites the SHA it fetched. The exception
expires the moment the pack is filed.

## REPO STATE (verify yourself — fresh clone, cite SHAs)
- **main MOVES when this pack is filed — VERIFY LIVE, do not trust a SHA quoted here.** At authoring it
  was `7989d21`. · tagged board of record **v2.9 = `9f8ae76`** (board `81e48293` · store `b0c39d78`)
- working head: store **`340a7a32`** · board **`3dc19fbb`** · engine **`2030e5df`** · rl_model **`952ddb3d`**
- open: **PR #73** (`2c0fe48`, prescreened PASS, blocked on green main) · **PR #74** (`ed13177`,
  prescreened PASS, **HOLD — does not fix CI**)
- in flight: **DETERMINISM** · **SMOOTH THE THREE HARD EDGES**
