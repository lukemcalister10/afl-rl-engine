# SEAT TOOLS (P3) — standing orientation + prescreen readers

Three **read-only** scripts a supervisor seat runs on entry and before it touches a candidate.
Tier-3 tooling: **no ladder, no store/engine/board/docs writes.** They answer three questions with
raw evidence, never a bare verdict:

| script | question it answers |
|---|---|
| `orient.sh` | *Am I looking at the live tree, and does Project-Knowledge match the repo?* |
| `prescreen.sh <branch> <base_sha>` | *What does this candidate branch touch, and does it hold the fence?* |
| `gates_score.py <gates_json> [acceptance_json]` | *What do a build's gates say against the binding registry?* |

## What each prints

**`orient.sh`** — one command, no args:
`git ls-remote` of `main` + tag `v2.9` against the canonical URL (RAW SHAs) · the checked-out
`HEAD` SHA beside them · `LTI_REGISTER.md`'s own header line · the `docs/` listing · a table of
every pack doc's HEADER VERSION (MANIFEST, CORE, HANDOVER, DECISIONS, CONSTRAINTS, acceptance, SSI)
for the PK-vs-repo comparison R98.10 / R100.10 require. Globs each doc by prefix so a version bump
is still found; prints filename + raw header string.

**`prescreen.sh <branch> <base_sha>`** — reads the candidate straight off the canonical remote
(`git fetch`, no checkout) and lays its fence-relevant facts beside the base, ≤35 output lines:
live head `rev-parse` · `merge-base --is-ancestor` verdict with both SHAs · `diff --name-status`
(fence-relevant paths named; `session_*/` scratch rolled up per dir to hold the line budget) ·
board md5 **recomputed** from `data/rl_build/rl_app_data.json` at the head, printed beside
`expected_boot.json`'s board pin · the changed-field list of `expected_boot.json` (base→head) ·
`book_stable_seal.json` summary plus any `__meta__` stamped in a `data/s4_matrix*.json` at head ·
`run_panel.sh` env-pin diff · the **NEW-ENV-READ CHECK** (register item 114): any *added*
`os.environ.get` / `getenv` in `engine/` vs base — a board-changing dial must be pinned, not read
live.

**`gates_score.py <gates_json> [acceptance_json]`** — from a `data/gates_snapshots/gates_*.json`:
the status tally · **PICK 1** (the numeraire pin, 3000) from `acceptance.numeraire.law` when the
acceptance JSON is supplied, else scanned from a gate detail · **B1 / G-COHORT / G-PEAK** ratios
against the hard bound (`<= 130`) where the snapshot carries the numbers · **every FAIL** with its
`dc` flag and note · **named anchor values** scanned from details. With the acceptance JSON it also
scores matching entries **by id** (`guards.alias → gate`, `anchors.governed_by → gate`).

## House laws — each is cited where it bites

1. **Scripts WRITE NOTHING.** Pure readers; the only writes are temp under `/tmp`. `git fetch` in
   `prescreen.sh` populates the `.git` *object cache* (the directive-authorized way to READ a remote
   branch) — it never touches the working tree, store, board, or docs.
2. **Every line carries RAW EVIDENCE** — a SHA, an md5, a number, a note — never a bare verdict.
   `MATCH`/`DRIFT`/`YES`/`NO` always sit beside the two values that produced them.
3. **Non-zero exit on ANY failure or missing input, and the exit code PROPAGATES.** Bash scripts run
   `set -euo pipefail` and route every failure through `die()` (exit 1); `gates_score.py` raises
   `SystemExit(1)`. No check is piped through `tail`/`head` unchecked. **SILENCE IS A RED** (CORE
   rule 1) — a script that cannot prove its claim exits non-zero rather than printing a hollow PASS.
4. **Network: the canonical URL only.** Every `ls-remote`/`fetch` targets
   `https://github.com/lukemcalister10/afl-rl-engine.git`. **POSIX bash + python3 stdlib only** — no
   pip, no non-stdlib import.

Traps these encode, by register item: **110** (state facts against committed data, not memory — the
scripts recompute md5s and read headers live), **114** (board-changing dials must be pinned — the
NEW-ENV-READ CHECK), **115** (evidence read from the record, not asserted).

## Proof (sample outputs in `samples/`)

- `samples/orient.out.txt` — `orient.sh` against live state (main `5738f2b2`, v2.9 `9f8ae761`).
- `samples/prescreen.out.txt` — `prescreen.sh claude/board-hardware-independent-az0iz5
  e7d980eb…` — known-good: **ancestry YES, board `800bf461` MATCH**, 27 lines.
- `samples/gates_score.out.txt` — `gates_score.py gates_fef5719d.json` — known-good:
  **B1 PASS, PICK 1 = 3000, three FAILs (A2/A3/A12)**; plus the acceptance-scored run.

## One thing the scripts could not encode

The **G-COHORT / B1 cohort ratios** (e.g. `126.8/125.2/116.1 ≤ 130`) are **truncated out of the
gates snapshots** — every `gates_*.json` caps `detail` at 200 chars, so the three ratios are not in
the file. `gates_score.py` therefore reports B1's PASS *status* (the record) and says plainly the
ratios are absent, rather than inventing them. To score the ratios themselves you need the untruncated
B1 detail, which these snapshots do not carry.
