# 00_MANIFEST — v4.17 · 2026-07-14 · supersedes v4.16
### The pointer file. Read it first. It tells you what is current and what to read WHEN.
### **ADDRESSED TO FABLE.** Written at the seam by seat 6 (Opus, overnight).
### **R98.8 (screening) EXPIRES THE MOMENT YOU SIT (R99.3). Your pen is unscreened from turn one.**

## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.17** | 0 | first, always |
| **CORE** | **v2.5** | 0 | in full — BINDING. ⚠ **v2.6 IS YOUR FIRST PEN JOB** (see below) |
| **HANDOVER** | **rev137** | 0 | state + the action order — **addressed to FABLE** |
| **DECISIONS** | **v100** | 0 | rulings + owner to-dos. ⚠ **ALSO READ v98 ITSELF — the owner's verbatim words** |
| **OPEN_ITEMS_REGISTER** | **read its OWN header** ⚠ | 1 | ⚠ **THE DURABLE LOG. IT IS THE REAL RECORD OF THE OVERNIGHT SESSION. READ IT.** |
| **CONSTRAINTS** | **v1.12** | 1 | ONLY when judging a board. **L-SYMMETRY + L-SAGE-FADE are NEW** |
| **acceptance_v1_12.json** | **v1.12** | 1 | ONLY when judging a board — **assert the JSON, never the prose** |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | when touching the store or a derived artifact. ⚠ **still at repo ROOT — move it into `docs/`** |
| ROADMAP · UNRESOLVED · CHANGELOG | — | 2 | on demand |

**NEVER BULK-READ THE PACK. Context is a budget.**

## ⚠⚠ CORE v2.6 IS YOUR FIRST PEN JOB
CORE v2.5 does **not** describe the rules in force. Fold in:
1. **R98.9** (the pen is restored) · **R98.10** (the handover exception).
2. **⚠ THE CORRECTED ORDER: FRESHNESS CHECK *FIRST*, THEN FILE.** rev136, manifest v4.16 and R98.10 all said
   *file first* — **the owner corrected it: a guard that runs AFTER the thing it guards cannot fire.**
3. **Move `SINGLE_SOURCE_INVARIANT.md` from repo ROOT into `docs/`** (seat 6's pen crossed its docs/-only fence
   once, by owner word, to fix a header lookalike — declared as a one-off, register item 85).
4. **File the CAPTAINCY LAW (R98.1) and the SMOOTHNESS LAW (R98.2) into CONSTRAINTS.** Both BINDING. Both still
   absent from the registry.

## ⚠⚠ NO BAKE — AND THE REASON HAS CHANGED
**Item 74's original arithmetic was WRONG and the owner killed it** (item 96): it compared a **per-player**
drift to an **aggregate** margin. **G-COHORT is a class-sum averaged across classes; independent drift falls as
σ/√n — a THIRTIETH of the margin, not a half.** And the measured post-freeze drift is **eight rucks, +1..+4
SCAR. Nothing flips.**
**WHAT NOW BLOCKS THE BAKE IS SIMPLER AND HARDER:**
> ## **CI IS RED, AND THE BOARD HAS NO STABLE NAME ACROSS MACHINES.**
**Four environments produce four boards. Intel-Haswell ≠ AMD-Haswell — same kernel, different chip.** No
environment variable closes it. **The board md5 is the board's NAME** — the tag, the book seal, `expected_boot`,
every register entry and A1 itself are stamped with it. **RULED (R100.7): bisect the divergence and fix the
sums. If it is not localised, a declared tolerance is the answer — and that is an acceptable outcome.**

## WHAT CHANGED AT v4.17
- **THE CHAPTER IS RENAMED — IT IS THE *IMPROVER* CHAPTER** (R100.1). **The engine believes bad news and
  interrogates good news.** Three censuses landed and all three point the same way. **Flattery is a symptom.**
- **CONSTRAINTS → v1.12:** **L-SYMMETRY** and **L-SAGE-FADE** filed as named laws · **G-Y0 → ADVISORY** (the
  identity is sound; **the FIX DIRECTION is stale and points the wrong way**) · **A-FADE** basis approved,
  **provenance UNVERIFIED**.
- **DECISIONS → v100:** R100.1–R100.9.
- **HANDOVER → rev137**, addressed to **FABLE**. **Correction ledger: THIRTEEN.**
- **OPEN_ITEMS_REGISTER:** items 96–109. ⚠ **NEVER PIN ITS VERSION IN A DOCUMENT — THE PEN MOVES IT ON EVERY PUSH.** ⚠ **Items 105–106 REOPEN item 101 — a false mechanism the
  supervisor registered as measured fact.**
- **PR #76 closed (superseded). PR #81 opened** (`4de05f0a`): the q97m freeze + follow-up + **CI's board-md5
  print, which CI had never had.**

## REPO STATE (verify yourself — fresh clone, cite SHAs)
⚠ **MAIN MOVES WHEN THE PACK IS FILED — INCLUDING BY THE VERY COMMIT THAT FILED THIS MANIFEST.** A base pin
reads **"main AT OR AFTER `<SHA>`, and `git diff --name-only <SHA>..main` must be `docs/`-ONLY"** — **NEVER
strict equality** (CORE v2.5, THE BASE PIN). **Do not HALT your freshness check on a docs/-only drift.**
- **main = `60ba0e2`** at authoring; **the seam-pack filing itself moved it to `41c12ce` and the register pen
  moves it again.** · tagged board of record **v2.9 = `9f8ae76`** (board `81e48293` · store
  `b0c39d78` · config `69ead79b` · **pick 1 = 3000**)
- **⚠ A1 IS PROVEN** — the board of record **rebuilds byte-identical** at the tag's own tree (supervisor-verified
  against the tag's own `expected_boot.json`, **not a build's word**). **On this hardware class.**
- working head: store **`340a7a32`** · board **`3dc19fbb`** · engine **`2030e5df`** · rl_model **`952ddb3d`**
- **THE FOUR BOARDS:** Intel-SkylakeX **`3dc19fbb`** · Intel-Haswell **`5546c120`** · **AMD/CI `62d23265`** ·
  SSE **`935c2c29`**
- open PRs: **#81** (`4de05f0a`) · **#73** (`2c0fe48`) · **#78** (`14e2a5fa`) · **#79** (`958c04ae`) ·
  **#80** (`8542299`)
- **in flight: FIX 1 + THE ABSENCE TERM** (⚠ store/engine WRITER) · **DETERMINISM BISECT (HELD — rebase onto Fix
  1's head; same file)**

## THE SEAM PACK (Project knowledge)
**FRESHNESS CHECK FIRST, THEN FILE** (the corrected order). **Compare PK against the repo doc by doc, by header
version. PK ahead or equal ⇒ file. PK BEHIND on ANY doc ⇒ HALT and tell the owner.**
**SCOPE: pack docs ONLY.** SHAs, board/store md5s, the register, returns, code and artifacts are **NEVER** read
from Project knowledge — **verify state live and cite the SHA you fetched.**
