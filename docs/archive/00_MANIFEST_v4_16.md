# 00_MANIFEST — v4.16 · 2026-07-14 · supersedes v4.15
### STATUS: OWNER-SCREENED 2026-07-14. NOT YET IN THE REPO — it files at SEAT 6's ACT 1 (the owner's word is given, R98.10). From that filing the repo copy is canonical.
### R98.8 (screening) remains LIVE until FABLE sits (R99.3).
### The pointer file. Read it first. It tells you what is current and what to read WHEN.

## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.16** | 0 | first, always |
| **CORE** | **v2.5** | 0 | in full — it is BINDING. ⚠ **CORE v2.6 is FABLE'S FIRST PEN JOB** — it folds R98.9 (pen restored) and R98.10 (the handover exception). Until it lands, CORE v2.5's rule 8 and its FRESHNESS CHECK do not describe the rules in force. |
| **HANDOVER** | **rev136** | 0 | state + the action order — **addressed to SEAT 6** |
| **DECISIONS** | **v99** | 0 | rulings + owner to-dos |
| **OPEN_ITEMS_REGISTER** | **v83** | 1 | the durable finding log (repo-only; pen-maintained) |
| **CONSTRAINTS** | **v1.12** | 1 | ONLY when judging a board |
| **acceptance_v1.12.json** | **v1.12 (REGENERATED 2026-07-14)** | 1 | ONLY when judging a board — **assert the JSON, never the prose** |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | when touching the store or a derived artifact |
| ROADMAP | v9 | 2 | on demand |
| UNRESOLVED | — | 2 | on demand |
| CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## ⚠ NO BAKE — REGISTER ITEM 74
Every guard, anchor and census figure in this pack was measured **in incognito sandboxes, not the bake
environment**. The cross-environment drift (0.35–1.8%/player) is **half G-COHORT's ~3% margin.** They are
**CONSISTENT, NOT VERIFIED.** **Once `q97m` is frozen, RE-MEASURE and RECONCILE every one of them. No bake
until then.** This is now machine-readable in `acceptance_v1.11.json` (`bake_blocker`) — not only prose.

## WHAT CHANGED AT v4.16
- **DETERMINISM ANSWERED.** The rev135 banner (*"read the determinism return before you act on anything in
  this pack"*) is **RETIRED — it has landed.** The board is deterministic within an environment; the CI
  mismatch is cross-environment; the mover is **`q97m`**, refit at import. ⚠ **The CAUSE is UNTESTED**
  (item 76) — do not state OpenBLAS as fact. **Freeze is correct either way.**
- **`_iso_dec`** (`_merged_recover.py:801`) — a **SECOND runtime fit that D3 missed.** If CI is still red
  after the freeze, that is **not a failed freeze** — look here first.
- **`acceptance_v1.11.json` REGENERATED:** G-BOOK's `known_gap` corrected in BOTH directions (the
  `rl_model` pin **EXISTS and is CORRECT**; `boot_guard` simply never asserts it), and **item 74 is now
  MACHINE-READABLE** — the bake blocker lives on the artifact a prescreen asserts against, not only in prose.
- **HANDOVER → rev136**, addressed to **SEAT 6**. Correction ledger now reads **SIX**.
- **DECISIONS → v99:** PR #75 ruled (Fix 1 TAKE · Fix 2 REJECT · Fix 3 HOLD) · **FREEZE `q97m`** ruled ·
  **R98.9 REWORDED** (screening expires when **FABLE** sits, not at this rotation) · the stale to-dos killed.
- **OPEN_ITEMS_REGISTER → v83** (pen-pushed at `bce9f7b`): items 74–78 (the drift/margin problem, `cm_400.pkl`'s
  unreproducibility, the untested cause, the lost SHAKEDOWN finding, the book's memory-address keys) **+ 79–82**
  (PR #75 ruled · **`_iso_dec`** · R98.9 reworded · the ledger closing at SIX).

## THE SEAM PACK (Project knowledge) — SYNCED, AND SEAT 6 FILES IT
PK was verified byte-identical to the repo. **R98.10 (BINDING):** *on disagreement the repo wins — **other
than at a seat handover.*** The incoming seat reads the pack from PK and **files it to the repo as its first
act** (the owner's word IS given for seat 6's Act 1). Thereafter the repo is home and wins as before.
**DIRECTIONAL GUARD:** compare PK against the repo **doc by doc, by header version.** PK ahead or equal ⇒
file and proceed. **PK BEHIND on ANY doc ⇒ HALT and tell the owner.**
**SCOPE: pack docs ONLY.** SHAs, board/store md5s, the register, returns, code and artifacts are **NEVER**
read from Project knowledge — verify state live and cite the SHA you fetched.

## REPO STATE (verify yourself — fresh clone, cite SHAs; main MOVES when the pack is filed)
- **main = `bce9f7b`** at authoring · tagged board of record **v2.9 = `9f8ae76`** (board `81e48293` · store
  `b0c39d78`)
- working head: store **`340a7a32`** · board **`3dc19fbb`** · engine **`2030e5df`** · rl_model **`952ddb3d`**
- open: **PR #73** (`2c0fe48`, prescreened PASS) · **PR #74** (`ed13177`, prescreened PASS, **does not fix
  CI — do not merge it red**) · **PR #75** (`3b69335`, **ruled: 1 take · 2 reject · 3 hold**)
- in flight: **q97m FREEZE** (⚠ store/engine WRITER — no second writer) · **DISCONTINUITY CENSUS** (read-only)
