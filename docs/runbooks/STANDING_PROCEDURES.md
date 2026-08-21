# STANDING PROCEDURES — the seat's norms, roles, housing and environment carries

**PROVENANCE.** Every section below is REHOMED from `docs/CURRENT_STATE.md` on 2026-08-21, the act
that retired that file to a tombstone (PLAN_v6 3c; process law P6). None of it is new, and none of it
is authored here: it is the standing-procedure half of the retired file — the half that is neither
law, nor record, nor state, and therefore had nowhere else to go. The owner-signed PART A material
(the governing test and the product laws) went to `docs/ENGINE_PRIMER.md` §0 in the same act.

**WHAT THIS IS NOT.**

- Not law. The laws are `docs/RULEBOOK.md`, and only the owner's word amends them.
- Not the record. The record is `docs/register/` (newest line: `docs/register/LATEST.md`) plus the
  byte-frozen `docs/OPEN_ITEMS_REGISTER.md`.
- Not state. Current identities are `docs/STATE.md`, machine-written at every landing. Nothing in
  this file is a hash, a board id, or a branch tip, and nothing in it should ever become one — that
  is precisely how its predecessor went 156 register versions stale.
- Not a procedure's only home where a tool owns it. Where a tool states the rule in its own header
  (the register's write procedure in `docs/register/README.md`, the round advance in
  `docs/runbooks/R23_RUNBOOK.md`, the pin file's interim-writer rule in `data/sheet_pins.json`), the
  TOOL wins and this file merely points.

**DATED FIGURES.** Where a number below was recorded against a dated tree (a self-test count, a
round number), it is marked as such. It is carried because the PROCEDURE around it is load-bearing,
not because the figure is asserted current. Verify any figure against the tree before relying on it —
which is the first standing norm in the next section.

---

## Standing norms

- **Screen by RE-RUNNING, never by reading.** A predecessor's work is hypothesis until reproduced.
- **Verify before recording.** Trace every figure to the artifact it describes before stating it.
- **No predictions of CI maps.**
- **Non-vacuity:** any guard added must be proven able to fail.
- Directives file as GitHub issues at pre-fire-audit time. Cold-review **openers** do not (v507).
- An audited directive is amended by addendum, never edited in place (v461).
- **CI runs and reports. CI never commits.**
- Corridor chat carries **zero authority**.
- Cold seats open bare, outside any project container (v427).
- Scratch is pristine git state **with full history** — `git fetch --unshallow`, never `git archive`
  alone.
- A seat's read is current only to the version it names. Disclose it.
- The seam verifies and rules; it does not do a seat's work, and never reviews what it authored.

## Roles

| | |
|---|---|
| **Owner** | sole owner-word authority: rulebook, stop-points, merges, tags, score-arm |
| **Seam + supervisor pen** | direction, continuity, the register, independent verification. **Docs-only** |
| **Execution supervisors** | direct hands, screen by re-running. Shell = verify/coordinate, **never author product commits** |
| **Hands** | bounded jobs, build-seat authored, read the directive from the filed issue |
| **Cold reviewers** | third seat, bare session, implementer ≠ reviewer ≠ supervisor |

## Housing

Direct push to main is classifier-blocked in cloud housing. Register pens land via the **API carrier
path**: branch → PR → rebase-merge. The merge under the owner's platform auth is a **housing fact,
not an approval step**. Docs-only pens land **without a per-entry word** (v483, restored by owner
word 2026-07-27), guarded by structural asserts proven pre-commit: line count unchanged, growth equal
to entry length, single stamp, PRIOR chain intact, docs-only diff. **Reversal is self-executing** —
any pen error reaching main restores the per-entry word.

**Ref deletion is proxy-forbidden to seats.** Branch deletes are an owner click. Do not retry it.

## Running this seat well — the FABLE BUDGET (owner word 2026-08-06)

Spend Fable ONLY on judgment — rulings, verifying the two-or-three deciding figures, talking to
the owner. Everything mechanical goes to OPUS subagents with tight checklists (charter law; never
an inherited default). Keep owner replies ~one screen, short plain sentences. The auto-mode
content classifier false-positives on arming/guard vocabulary — rephrase plainly, never work
around it; on repeated blocks, stop and ask the owner. Verify hand-backs by re-running deciding
figures with your own commands BEFORE presenting anything. Present the number that answers the
owner's actual question (the yr1-to-peak lesson: relocating a gap is not closing it). Threads by
comment id only; the register by pointer (grep N-numbers); one pen per boundary, batched.

*(The clause that stood here about "incremental CURRENT_STATE edits must assert count==1 per match
or replace Part B wholesale" is RETIRED WITH ITS SUBJECT: there is no hand-edited state file to edit
incrementally. Its successor is the freshness gate — `acceptance::state_file` regenerates
`docs/STATE.md` and compares byte-for-byte, so the silent no-op that failure mode describes cannot
occur unnoticed.)*

## Environment carries (inlined in full — nothing dangles)

Pinned venv: `bash setup_env.sh` → `/root/rl_venv312` (Python 3.12.3 · numpy 2.4.4 · scipy 1.17.1 ·
sklearn 1.8.0 · openpyxl 3.1.5); then PATH the venv, then `bootstrap_env.sh` (no-op check), then
`RL_VENDOR=<tree>/vendor bash <tree>/bootstrap.sh` (seeds `/home/claude/rl_workspace`; Guard 5
asserts the pinned store).

Canonical build: cd `/home/claude/rl_workspace/rl_after` && `rm -f rl_app_data.json` && single-thread
BLAS env (`OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1`),
`PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor`, `RL_CONFIG_MODE=gate`,
`RL_REPO=<tree>`, `RL_FV=<tree>/engine/forward_valuation`, `python3 rl_export.py`; then
`s4_matrix_M1v7.py`; then `one_source_selftest.py` (the expectation recorded 2026-08-11 was 144
PASS / 0 FAIL — a DATED figure, not a current assertion: read the count off the run).

Weekly rounds: the catchup verb — `tools/round_entry/weekly_update.sh catchup --file N=scores/RN.csv`
unarmed = preview; `INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<any> ... --approve` = apply;
ledger blocks double-apply; exit 6 → `finalize --round N` then `repair --round N`. **The round
lander (`tools/land round`, PLAN_v6 2b) is the writer of record for a round advance since
2026-08-21**; this manual path is the documented fallback, and `docs/runbooks/R23_RUNBOOK.md` is its
procedure.

N32 payload recipe: `{str(pick): int(round(v))}` over the ladder's `curve` object,
`json.dumps(..., sort_keys=True)`, md5. The key TYPE is load-bearing — a string-keyed and an
int-keyed dump of the same ladder hash differently.

Commit identities: product commits are authored `build-seat <build@seam.local>`; every commit ends
with the Co-Authored-By + Claude-Session trailers. Explicit paths only, always (process law P8).

The book (`s4_matrix.json`) is `id()`-keyed — never byte-reproducible; the committed book of record
is `engine/rl_after/s4_matrix_M1v7.json` (its meta block carries its identity).

The owner's cohort artifact (claude.ai): pass its URL to the Artifact tool to update it in place;
its conventions are printed on the page itself.

Evidence trees are RETENTION-PROTECTED from hygiene pruning. Worktrees and workspaces under
`/home/claude/` are EPHEMERAL — container-bound, rebuilt from the branch plus the filed commands;
never cite one as a durable location.

## The register's write procedure

Not repeated here on purpose. `docs/register/README.md` is its home — `tools/seat/pen.py append`,
then an explicit-path commit — and the byte-surgery procedure that used to stand in the retired file
is impossible since the 3b freeze.
