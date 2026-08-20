# RETIREMENTS — 2026-08-20. Three instruments retired by owner ruling, recorded where they live.

Three things the owner ruled retired are written down here **and into the instruments that carry
them**, in the act that records the rulings. That second half is the whole point: two of the three
had already been retired in conversation, and came back from the dead because nobody had written
them into the file that does the asserting.

| # | retired | instrument | recorded in |
|---|---|---|---|
| 1 | **A9** — the Ginnivan > Ward ordering assertion | `ship_gates_check.py`, `SHIP_GATES.md` | STRUCK, by the A15 mechanism |
| 2 | **B1** — the July-8 cohort rail (hard 1.30 on y4/y5/y6) | `ship_gates_check.py`, `SHIP_GATES.md` | STRUCK, by the A15 mechanism |
| 3 | **the six weekly-update rehearsals** | `.github/workflows/live-scoring-proofs.yml` | file DELETED; pointer repointed in `live-scoring.yml` |

---

## 1 + 2 — A9 AND B1

Full record: `STRIKES.md` in this directory. In brief:

**A9.** OWNER, VERBATIM (2026-08-20): *"Those player ordering assertions were retired and are
outdated. Since they occurred, Ward has hit an excellent run of form."*

**B1.** OWNER, VERBATIM (2026-08-20): *"That cohort rail again was retired. Weeks ago."*

Both were retired BEFORE they were reported red. They reported red only because the frozen suite was
bricked at `ship_gates_check.py:49` throughout, and its first full run after the unbricking
resurrected them. See `STRIKES.md` and the proposed process law P11 in
`docs/proposals/rulebook/AMENDMENT_1b_2026-08-20.md`.

---

## 3 — THE SIX WEEKLY-UPDATE REHEARSALS, SCRAPPED

### The ruling

OWNER, VERBATIM (2026-08-20):

> "The six shelved tests seem cumbersome and adding time and bloat, I'd be happy to scrap them
> unless you disagree?"

The supervisor concurred, on the **coverage-successor condition** — that the ground they covered is
named to a successor rather than dropped. The owner's earlier words on the same six tests stand with
this ruling:

> "That sounds like more and more process and clunky cumbersome."

### What was deleted, and what it was

`.github/workflows/live-scoring-proofs.yml` — **DELETED**. Six jobs, `workflow_dispatch` only, at a
180-minute timeout each:

| job | what it rehearsed |
|---|---|
| `proof-two-round` | R15 → R16 sequential apply; the 17-point live-scoring proof |
| `proof-catchup` | five-round catch-up R15 → R19 on the owner's real files |
| `proof-failure-injection` | 7-point mid-apply fault matrix + crash recovery |
| `proof-finalization-injection` | post-commit fault matrix; restart detects + repairs; no re-apply |
| `proof-storewrite` | scratch apply + dedup ledger + single-env stability |
| `proof-fv-provenance` | staged board build fail-closed on FV provenance |

**Nothing triggered it.** `on: workflow_dispatch` was its only trigger — no push, no pull_request,
no schedule, no `workflow_call`. Deleting it changes no automatic behaviour anywhere in the estate.

### The original de-scope, and why this is a re-adjudication rather than a repair

`#251 part B`, owner ruling **2026-07-29** (his word then: *"agree on the proof jobs"*). The six had
been running on every push and pull_request from `live-scoring.yml`. All six died in ~30 seconds at
the v0surf frozen-signature HALT — they structurally could not pass as wired — so six permanently
red every-push jobs were hiding real reds. They were moved to a manual trigger and **kept**, on the
stated reasoning that their future use was a deliberate one-shot rehearsal when the positional
rebuild changed the engine.

The locked plan (`PLAN_v6` 1a) queued this file specifically because **that recorded de-scope cause
is now false**, and named the correct disposition: *"Dispatch-only live-scoring-proofs is
OWNER-RE-ADJUDICATED (its recorded de-scope cause is now false) — an owner question, not a silent
repair or retirement."* This closes that item. It was put to the owner and he ruled. Nothing was
repaired quietly and nothing was retired quietly.

### THE NAMED SUCCESSOR — a forward commitment on the record

The rehearsals' real content was **crash-injection and abort-path coverage**. That ground is not
dropped; it is assigned, by name, to an instrument that is purpose-built for it:

> **`PLAN_v6` PACKAGE 2a, item 2a.3 — THE LANDER SELF-TEST.** *"the program deliberately breaks each
> step in a sandbox and asserts the failure is caught. THE ABORT PATH is part of the program, not an
> afterthought: a landing that fails mid-flight restores every carrier to its pre-landing identity
> (recorded in the claims file at start), asserts the restoration byte-exact, and reports the failed
> step — tested in the self-test by killing a landing at each step."*

Why the successor is better coverage than what it replaces, stated plainly rather than assumed:

- it **runs**, which the six did not — they HALT in ~30 seconds on the v0surf frozen signature and
  cannot pass as wired, so their coverage has been zero for as long as they have existed in that form;
- it asserts **byte-exact restoration** of every carrier after an injected abort, which is the
  property the rehearsals were reaching for through a full weekly-update dress rehearsal;
- it is **sandboxed and fast** rather than a 180-minute scratch-workspace rehearsal, which is exactly
  the "time and bloat" the owner named.

**This is a commitment, not a hope.** It is deliverable by package 2a of the locked plan, which is the
next package in that plan's sequence (`P1 -> P2a -> ...`). If 2a lands without 2a.3's crash-injection
and abort-path coverage, this retirement has lost coverage and the loss should be raised then. That
is the falsifier for this entry, and it is stated here so it can be checked rather than remembered.

### What is NOT claimed

- **Not claimed:** that the six rehearsals were worthless. They were built as one-off proofs for the
  weekly-updater work and they did that job; their artifacts and proof scripts remain in the tree at
  `session_2026-07-19/storewrite/`, `session_2026-07-20/live_scoring_two_round/`,
  `session_2026-07-20/live_scoring_catchup/` and `session_2026-07-20/weekly_updater_hardening/`.
  **Only the workflow that wrapped them is deleted.** Any of them can still be run by hand.
- **Not claimed:** that the v0surf third-signature question (`65b9fbaf`, cause undetermined) is
  resolved. It is not. It was deliberately unresolved before this ruling and it is deliberately
  unresolved after it. The freeze is not weakened by this act.

### Readers enumerated before the delete (the PRE-ACT discipline)

| reader | what it said | what this act did |
|---|---|---|
| `.github/workflows/live-scoring.yml` (header, bar list) | pointed at `live-scoring-proofs.yml` for bar points 2/2b/3/3b/3c/4/5 | repointed **in the same act**: the ruling verbatim, the successor named, the bar points kept as the record of what the rehearsals covered |
| `docs/OPEN_ITEMS_REGISTER.md` | historical record of #251 part B | **nothing** — the supervisor pen owns it, and this seat never writes it |
| `docs/proposals/process_plan/PLAN_v*.md`, `docs/proposals/process_plan/REVIEW*.md` | queued the re-adjudication / record what was reviewed | **nothing** — history is frozen, never rewritten; this file is the answer to the question PLAN_v6 1a asked |
| `docs/evidence/rulings_sweep_2026-08-13/*` | past-tense inventory rows | **nothing** — same reason |
| any workflow that calls or needs it | none exists — `workflow_dispatch` only, no `workflow_call`, no `needs:` reference | **nothing owed**; measured, not assumed |
