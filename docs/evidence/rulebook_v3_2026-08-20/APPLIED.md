# THE RULEBOOK v3 — THE AMENDMENT, APPLIED · 2026-08-20 · docs/tooling seat, trimmed ceremony

**THE OWNER'S WORD, VERBATIM (in chat, 2026-08-20):** *"Okay agree to the laws updated."*
Given against the supervisor's presented final form, following his earlier direction *"we can keep
the rulebook minus the redundant ones etc"*. RULEBOOK law 10(a) — changes to the rulebook are an
owner-word act — is satisfied by that sentence and by nothing else in this file.

Base: `main` 68a3a50. Drafted under the locked process plan item 1b as
`docs/proposals/rulebook/AMENDMENT_1b_2026-08-20.md` (four-pass drafting + cold review; every
signable section applied and measured in an isolated worktree before presentation). Applied here.

---

## WHAT MOVED

| | before (68a3a50) | after |
|---|---|---|
| `docs/RULEBOOK.md` | v2.1 · 11 laws · no process laws · "Twin: docs/acceptance_v2_0.json" | **v3 · 12 laws · PART 4 P1–P11 · no twin** |
| `docs/acceptance_v2_0.json` | 13 laws, hand-maintained, no banner, read by no code | **REMOVED** (`git rm`); its thresholds folded into PART 3 |
| `tools/rulebook_twin.py` | the regenerator built so the owner could rule on a real thing | **REMOVED** — with no twin it has no subject |
| `tools/rulebook_lint.py` | R5 TWIN PARITY / R6 TWIN BANNER — 2 FAIL | **R5 TWIN ABSENCE / R6 NO DERIVED VIEW — 0 FAIL** |
| `acceptance/ruled_red.json` | RB1 carried as a presented ruling | **RB1 retired** — its own probe expired it |
| runner | GREEN, 1 ruled-red | **GREEN, 0 ruled-red on this row** — one fewer carried red |

Value-bearing artifacts: **none moved.** `g1_BEFORE.txt` vs `g1_AFTER.txt`, 26 identities,
byte-identical; the only differing lines are in the block the script labels DELIBERATE MOVES.

**A CONCURRENT SEAT MOVED HEAD MID-ACT, and it is named rather than smoothed.** The briefed base
was 68a3a50; while this act ran, the score-trough diagnosis seat landed three commits (163dba9,
4b4a05b, 455d593 — 50 files, `docs/evidence/` plus one `docs/OPEN_ITEMS_REGISTER.md` header line),
so this act's commits sit on top of 455d593. `git diff --name-only 68a3a50 455d593` intersects
**none** of this act's paths, and every claim in `V3_CLAIMS.json` was recomputed against the tree
*after* those commits landed and held — 35 of 35. This is the gap the build lock does not cover:
the lock serialises engine acts through the shared workspace, and a docs commit neither takes it
nor needs to.

---

## THE FIVE RULINGS THIS ACT CARRIES OUT

**1 — The header.** v3, 2026-08-20, the owner's words verbatim, and a one-line provenance naming
the plan item and the drafting chain. Laws 1–10 are byte-unchanged and `verify_v3.py` V3 asserts it
against the base commit rather than against a copy of the text.

**2 — Law 11, amended.** The old law required *both* a numbered claims note *and* a blind
independent review of **every** release. The claims note half stays universal and is now named as
machine-generated (`tools/claims.py`) — it was always the cheap half and it is now the checkable
half. The blind independent review is scoped to **releases that move player values**: a tooling,
docs or process release ships on its claims note and its gates, with the byte-unmoved identity list
as the standing falsifier that it was indeed such a release. The register sentence is untouched.
This is the owner's *"minus the redundant ones"* applied to the one law that was demanding a
ceremony out of proportion to what most acts do.

**3 — Law 12 enters; there is no law 13.** `G-Y0` (year-0 closure, pooled abs pct within 2.0%)
enters PART 1 as law 12, in the drafted wording, verbatim from `patch_A.diff`. **`G-COHORT` does
not.** The drafted patch would have enacted it as law 13, and that draft predates the owner's
ruling: its payload is the 1.30 cohort rail he retired this session — *"That cohort rail again was
retired. Weeks ago."* — already struck in `ship_gates_check.py` as gate B1. Enacting it as a law on
the same day it was retired as a gate would have been the estate arguing with itself. PART 3 now
records it as **RETIRED**, with the owner's words, its retired 1.3 payload, and the cross-reference
to the B1 strike, where it previously said UNMEASURED.

**4 — PART 4 lands, P1 through P11.** P1–P10 verbatim from `patch_B.diff`; P11 from the strike
seat's append (*the retirement is recorded where the gate lives*), whose incident — A9 and B1 struck
into a suite that could not run — happened after patch_B was drafted. P10 gains one sentence
recording that its own incident, the twin, was disposed of by this amendment.

**5 — The twin is removed, and nothing dies with it.** Option B, owner-agreed. The removal owed
three things and paid all three: `docs/RULEBOOK.md:6` (the twin pointer, gone — Section C's diff),
`docs/referee/REFEREE_PROTOCOL.md:10` (repointed to the RULEBOOK, with the repair stated in-line
because that document is FROZEN and a silent edit to a frozen document is worse than a loud one),
and **the thresholds** — every `check` prose line and every numeric payload (`pick1_equals` 3000,
`band_scar` 200, `max_pct` 2.0, `direction_only`, and G-COHORT's retired 1.3) folded into PART 3 as
a compact measurement-thresholds table. `verify_v3.py` V4 reads the payloads out of the **base
commit's twin** and asserts each one appears in PART 3 — the check cannot be satisfied by a
transcription this seat believes it made.

---

## THE DRAFTED PATCHES vs THE AGREED FORM — where they differ, and why

The drafts predate the owner's rulings. Four divergences, all resolved toward the agreed form:

| # | the drafted patch | what was applied | why |
|---|---|---|---|
| 1 | `patch_A.diff` enacts G-COHORT as law 13 | **struck** — 12 laws, no law 13 | the cohort rail was retired this session; PART 3 records the retirement with the owner's words |
| 2 | law 11 left byte-unchanged in every patch | **amended** | the owner's final form scopes the blind review to value-moving releases |
| 3 | `patch_B.diff` carries P1–P10 and was deliberately not regenerated | **P1–P11 applied** | the strike seat's P11 append is part of the presented final form |
| 4 | Option B's reader enumeration says *"any code: none exists"* | **two live code readers repaired** | measured again at 68a3a50: `ship_gates_check.py` (B1's obituary) and `SHIP_GATES.md` §B both cite the twin as the live carrier of G-COHORT. That was true when the enumeration was written and stopped being true when B1 was struck a few hours later. Both repointed to RULEBOOK PART 3. No gate, verdict, dial or threshold in either file changed — comment and citation text only. |

Divergence 4 is the one worth a supervisor's eye: the drafted enumeration was not sloppy, it was
**stale by hours**, and it was the day's own strike act that staled it. The pre-act enumeration
discipline works; it just has to be re-run at the moment of the act rather than read back from the
draft. That is P11's shape pointing at itself.

Untouched, as the drafted enumeration ruled: `docs/referee/F3_REVIEW_v0_3.md` and
`docs/directives/ITEM_408_COLD_REVIEW_partial.md` are past-tense records of what was reviewed —
history is frozen, never rewritten. `REFEREE_PROTOCOL.md:658` is the same shape (a filed record of
the 2026-07-24 twin amendment, executed by the pen at register v400) and is likewise untouched.
`docs/OPEN_ITEMS_REGISTER.md` was not opened.

---

## THE TOOLING, RECONCILED IN THE SAME ACT

**`tools/rulebook_twin.py` — REMOVED, not tombstoned.** With no twin its purpose is gone entirely:
every one of its three modes (`diff`/`write`/`check`) reads or writes a file that no longer exists,
and its refusal path exists to escalate a question the owner has now answered. A no-op with a
tombstone note would have been a second thing to read, a second thing to keep passing lint, and a
file whose whole content is an apology. The tombstone belongs in the law that killed it (PART 4
P10) and in this record. Measured before removing: no code imports it and no workflow runs it; its
one non-documentation reference is `docs/evidence/p1_safety_net_2026-08-20/P1_CLAIMS.json`, a frozen
claims file recording that act's negative control — frozen history, re-run by no standing check.

**`tools/rulebook_lint.py` — R5/R6 reversed polarity.** Left alone they would have red forever on a
file that is supposed to be gone, which is the P7 failure mode with the sign flipped. They now
assert the **absence**: R5 that `docs/acceptance_v2_0.json` stays gone, R6 that no file anywhere
under `docs/` declares itself a derived laws view. **A reappearing second laws file is the new red
— P10's teeth.** The dead parity machinery (`recoverable_from`, `_tokens`, the banner regex) went
with the rules it served. The negative control is asserted, not asserted-to-be-asserted:
`verify_v3.py` V6 replants a derived view in a temporary tree and requires both rules to fire.

**`acceptance/ruled_red.json` RB1 — retired by its own probe.** RB1's `expires_when` read: *"the
owner signs the 1b diff: either the two laws enter PART 1 (parity restored) or the twin is removed
(no derived view to lint)."* He signed; the twin is removed; the entry's probe
(`python3 tools/rulebook_lint.py`, recorded signature `R5 TWIN PARITY`) now exits 0, which under the
ledger's `_probe_contract` is EXPIRED → retire. Left in place it would have **failed** the runner on
a stale ruling, which is the ledger doing its job. Moved to `retired` with the signature cited, so
the history stays legible and `known_red.py` — which reads only `entries` — can never see it again.
`acceptance/checks/standing.py`'s `rulebook_lint` docstring, which described the carried finding as
current, was corrected in the same act.

---

## GATES

| gate | verdict |
|---|---|
| `python3 -m acceptance.runner` | **GREEN** — see `runner_AFTER.txt` |
| `python3 tools/rulebook_lint.py` | **0 FAIL** — 12 laws, P1–P11 — see `rulebook_lint_AFTER.txt` |
| `python3 release_manifest_check.py` | **PASS**, untouched by this act |
| `python3 docs/evidence/rulebook_v3_2026-08-20/verify_v3.py` | **PASS** — V1–V6, including the negative control |
| `python3 tools/claims.py check .../V3_CLAIMS.json` | the claims file for this act |
| G1 | value-bearing identities byte-identical; docs + tools only |

## FILES IN THIS DIRECTORY

- `APPLIED.md` — this record.
- `V3_CLAIMS.json` — the machine-checkable claims for the act (`small-act`), and
  `V3_CLAIMS_CHECK.txt`, the checker's verdict: **35 of 35 verified, GREEN**.
- `verify_v3.py` — the six assertions above, runnable.
- `g1_identity.sh`, `g1_BEFORE.txt`, `g1_AFTER.txt` — the standing falsifier, before and after.
- `rulebook_lint_BEFORE.txt`, `rulebook_lint_AFTER.txt` — 2 FAIL → 0 FAIL.
- `runner_AFTER.txt` — the full-profile runner verdict after the act.
