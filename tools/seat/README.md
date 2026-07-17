# SEAT TOOLS (P3) — standing orientation + prescreen readers

Three **read-only** scripts a supervisor seat runs on entry and before it touches a candidate.
Tier-3 tooling: **no ladder, no store/engine/board/docs writes.** They answer three questions with
raw evidence, never a bare verdict:

| script | question it answers |
|---|---|
| `orient.sh` | *Am I looking at the live tree, and does Project-Knowledge match the repo?* |
| `prescreen.sh <branch> <base_sha>` | *What does this candidate branch touch, does it hold the fence — and was it cut from the pinned base?* |
| `gates_score.py <gates_json> [acceptance_json]` | *What do a build's gates say against the binding registry?* |

**SEAT TOOLS 2 (item 148)** — three more, to cut the supervisor's per-turn tool+context burn. The
first is the one non-reader in this directory: it makes a register push a single, asserted call.

| script | question / job |
|---|---|
| `pen.py append …` / `pen.py verify` | *Append an item + bump the header + push — with every replace asserted (the item-147 law).* |
| `board_diff.py <revA> <revB> [--names …]` | *How did the board move between two revs?* (the standard prescreen diff) |
| `gates_brief.py <gates_json> [acceptance_json]` | *The one-glance gate read — FAILs cross-checked against the standing-fails list.* |

**THE BASE GUARD (items 264 · 270 · 298 · 299)** — the wrong-base failure (a build cut from `main`,
or content-copied to match, instead of branched FROM the pinned base) recurred three times, twice on a
store writer. The defence was prose; nothing failed loudly when skipped. This mechanizes it.

| script | question / job |
|---|---|
| `first_commands.sh BRANCH_REF EXPECTED_SHA NEW_BRANCH [STORE_MD5] [SYMBOL[:FILE]]` | *Stand this build on the PINNED base — by proof, not by prose — and leave the transcript as the branch's first artifact.* |
| `prescreen.sh` **FIRST check** | *Does the candidate's FIRST commit carry that proof, and does the SHA it recorded equal the branch's actual base?* |

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

**`pen.py append --item-file F --header-summary "…" -m MSG`** — the register pen, mechanised.
Inserts F's item text **before** the `## FABLE'S QUEUE` section, bumps the header `vN → vN+1` (date
kept), and rewrites **only** the PEN summary's leading segment, keeping a short `· prior: <old first
clause>` pointer so headers stay SHORT (item 148). **Every replacement is asserted to match exactly
once** — a `str.replace` that matches 0 or 2 times is a HARD FAIL *before any commit* (this is the
item-147 law: the silent-no-op that stuck the header at a v130 draft and left item 145 twice). It also
asserts `new_version == old+1` and that item numbers are unique. Then it `git add`s the register only,
commits `MSG`, pushes `HEAD:main` with a token read from **`PEN_TOKEN`** (env only — never echoed,
never written to any file; the push URL is built in memory and errors are stripped of the token), and
re-reads the pushed commit's header first-200-chars, printing it beside the new main SHA and a `git
diff --name-only` proving docs/-only. One call, ≤12 lines. `--dry-run` runs every assert but writes /
commits / pushes nothing (used for the committed samples). `pen.py verify` prints header version +
item count + a duplicate-item scan (≤6 lines). **`PEN_TOKEN` is checked EARLY** — unset ⇒ loud fail
before any write, nothing token-shaped printed.

**`board_diff.py <revA> <revB> [--names n1,…]`** — the standard prescreen diff, terse (replaces ~30
lines of ad-hoc python the seat had rewritten five times). Reads `data/rl_build/rl_app_data.json` at
both revs with `git show` (no checkout) and prints: mover count (`active[].v` changed) + added/removed
· ΣΔ num-SCAR (signed net + gross) · age-bucket ΣΔ at the head rev (≤22 / 23–26 / ≥27) · top-3 cuts +
top-3 lifts by name · any `--names` rows before→after · PICK 1 both sides (`picks` n=1) · pair-2 /
pair-3 ratios (pick2/pick1, pick3/pick1). ≤15 lines.

**`gates_brief.py <gates_json> [acceptance_json] [--full]`** — wraps `gates_score`'s reader for the
one-glance read: status tally · PICK 1 · B1 status · every FAIL id one-per-line (notes only with
`--full`) · **standing-fails cross-check** — each FAIL is scored against `acceptance.standing_fails`
(STANDING-FAIL); any FAIL that is **not** a listed standing-fail is flagged **NEW-DEFECT** and the tool
exits non-zero. ≤10 lines.

**`first_commands.sh BRANCH_REF EXPECTED_SHA NEW_BRANCH [EXPECTED_STORE_MD5] [REQUIRED_SYMBOL[:FILE]]`**
— runs the directive's EXECUTE-FIRST base block as six ordered checks, each an explicit PASS/FAIL beside
its raw SHA/md5: **[0]** refuse on a dirty tree (uncommitted changes to *tracked* files — untracked
scratch survives `checkout -B`, so it is tolerated) · **[1]** `ls-remote BRANCH_REF == EXPECTED_SHA`
(the pin is live on the canonical URL) · **[2]** fetch the pinned object · **[3]** `checkout -B NEW_BRANCH
EXPECTED_SHA` (branch **from** the pin) · **[4]** `merge-base --is-ancestor` proof · **[5]** optional store
md5 == `EXPECTED_STORE_MD5` on the Guard-5 store `engine/rl_after/rl_model_data.json` (the pinned store
travels with the tree — item 264) · **[6]** optional `git grep -c REQUIRED_SYMBOL ≥ 1` (a base-only tree
lacks the candidate's symbol — item 298). On full success it writes the whole transcript to
`FIRST_COMMANDS_PROOF.txt` in the CWD — carrying a machine-readable `base_sha` line — and prints the one
line the build commits it with as its **first** commit. Any failure routes through `die()` (exit 1) and
writes **no** green proof — SILENCE IS A RED (the [6] miss is guarded so the zero-count fails *loudly*,
not at the assignment).

**`prescreen.sh`'s FIRST check** — before it reads anything else (the item-298 SEAM NOTE), it locates the
branch's first commit above the base, asserts that commit carries `FIRST_COMMANDS_PROOF.txt`, and that the
`base_sha` the proof recorded equals BOTH the commit's **actual** parent AND the pinned base handed to
prescreen. A content-copied branch (item 270/298) fails here: its first commit sits on `main`, not the pin.

## House laws — each is cited where it bites

1. **Scripts WRITE NOTHING** — with **two** authorized exceptions, each writing only what its whole job
   is: `pen.py append`'s single intended commit+push of the register (gated by the asserts; `--dry-run`
   writes nothing), and `first_commands.sh`'s `checkout -B NEW_BRANCH` + its `FIRST_COMMANDS_PROOF.txt`
   transcript in the CWD (standing a build on the pinned base *is* a branch+proof write; it never touches
   the store, board, engine, or docs, and writes no green proof on a failed base). Every other script is a
   pure reader; the only writes are temp under `/tmp`. `git fetch` in `prescreen.sh`/`first_commands.sh`
   and `git show` in `board_diff.py` populate/read the `.git` *object cache* (the directive-authorized way
   to READ history) — never the working tree, store, board, or docs.
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
- `samples/pen.out.txt` — `pen.py verify` + `append --dry-run` (GREEN) + the **red-path proofs**:
  a replace matching 0/2 times HARD-FAILs, a duplicate item number is caught, and `PEN_TOKEN` unset
  fails loud (exit 1) with nothing token-shaped printed.
- `samples/board_diff.out.txt` — `board_diff.py e1d8d78 71a8860 --names "Nick Daicos,Timothy English"`
  — known-good: **758 movers, PICK 1 held 3000, pair curve reshaped (p2/1 0.834→1.000)**, English
  2916→3132 (the item-107 anchor).
- `samples/gates_brief.out.txt` — `gates_brief.py` on `gates_2030e5df.json` (clean: 3 standing FAILs,
  0 NEW-DEFECT) and `gates_7c199a1f.json` (**B4 unlisted → NEW-DEFECT, exit 1**).
- `session_2026-07-17/base_guard/` — `first_commands.sh` red-path proofs: (a) wrong `EXPECTED_SHA` →
  **[1] ls-remote MISMATCH**, (b) wrong store md5 → **[5] store md5 MISMATCH**, (c) missing symbol →
  **[6] symbol MISSING** — all exit 1; plus the green run against the live `main` pin (all six PASS) and
  the two `prescreen.sh` FIRST-check transcripts (green: proof records base == parent == pin; red: first
  commit above a wrong base carries no proof → exit 1).

## One thing the scripts could not encode

The **G-COHORT / B1 cohort ratios** (e.g. `126.8/125.2/116.1 ≤ 130`) are **truncated out of the
gates snapshots** — every `gates_*.json` caps `detail` at 200 chars, so the three ratios are not in
the file. `gates_score.py` therefore reports B1's PASS *status* (the record) and says plainly the
ratios are absent, rather than inventing them. To score the ratios themselves you need the untruncated
B1 detail, which these snapshots do not carry.
