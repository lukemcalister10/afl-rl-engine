# CURRENT_STATE.md — RETIRED. This file is a tombstone.

**Retired 2026-08-21** by the PLAN_v6 3c act. The file stays at this path, and only at this path, so
that the pointers already written into charters, directives, code comments and the register keep
resolving. It carries no state. Nothing below is current, because nothing below is a value.

## What this file was

The condensed read for an incoming seat: PART A standing (the owner's governing test, his product
laws, the named hazard classes, the norms, the roles, the housing) and PART B the current state,
replaced wholesale at every supervisor pen. It carried an authority banner — *"IF THIS FILE AND THE
REGISTER DISAGREE, THE REGISTER IS RIGHT"* — a single named writer, and a discipline written into the
seat charter.

## Why it was retired

Because none of that worked. Its last pen was **v122, register v642, 2026-08-11**; the register
reached v798 while the file still described the state of v642 — **156 register versions stale**, with
its banner intact the whole time. That is the incident named in `docs/RULEBOOK.md` PART 4 under
process law **P6, GENERATED-ONLY**: *"A derived surface that cannot be generated does not exist. No
derived view is hand-maintained, whatever banner it carries."* PLAN_v6 3c names this file by name as
the retirement that law earns.

A hand-maintained derived view is not fixed by a stricter banner or a more diligent writer. It is
fixed by generating it, or by not having it.

## Where the truth lives now

| you want | read |
|---|---|
| **current identities** — board, store, engine_head, balanced, contract seal, round | **`docs/STATE.md`** — MACHINE-WRITTEN, regenerated at every landing by `tools/landing/state.py`, and asserted current on every run by `acceptance::state_file`. Never hand-edited. |
| **the record** — what happened, what was ruled, what is open | **`docs/register/LATEST.md`** (line 1 = the newest entry) then `docs/register/entries/vNNN.md`; the frozen predecessor `docs/OPEN_ITEMS_REGISTER.md` holds v622–v812, byte-sealed. Reading law: `docs/register/README.md`. |
| **the laws** | **`docs/RULEBOOK.md`** — the single governing document, owner-signed. There is no second laws file, ever (P10). |
| **the meaning layer** — what the engine is for, what each artifact means, the governing test, the owner's product laws, the named hazard classes | **`docs/ENGINE_PRIMER.md`** — §0 carries the owner-signed PART A material rehomed from this file, verbatim. |
| **the seat's norms, roles, housing and environment carries** | **`docs/runbooks/STANDING_PROCEDURES.md`** — the standing-procedure half of this file, rehomed. |
| **how to write to the register** | **`docs/register/README.md`** — `tools/seat/pen.py append`, then an explicit-path commit. The byte-surgery pen mechanics that stood in this file's §ENVIRONMENT CARRIES were already retired by the 3b act (2026-08-21) and pointed here; that pointer is preserved. |

## What was rehomed out of this file, by name

Rehomed in the same act, verbatim except where a dated figure is marked as dated:

1. **THE GOVERNING TEST** (the owner's words of 2026-07-27, its three consequences, and "write
   plainly") → `docs/ENGINE_PRIMER.md` §0. PLAN_v6 3c names the RULEBOOK as its eventual home; that
   move is owner-only (RULEBOOK law 10(a)) and is **owed to the owner**, not taken by a seat.
2. **THE OWNER'S PRODUCT LAWS** (2026-08-04, the v562 correction: the intersections law and the
   no-hard-bands law, with his verbatim quotes) → `docs/ENGINE_PRIMER.md` §0.
3. **THE NAMED HAZARD CLASSES** (all sixteen, numbering preserved — the seat charter cites "hazard
   class 16" by number) → `docs/ENGINE_PRIMER.md` §0.
4. **STANDING NORMS** (screen by re-running, verify before recording, non-vacuity, CI never commits,
   corridor chat carries zero authority, and the rest) → `docs/runbooks/STANDING_PROCEDURES.md`.
5. **ROLES** (owner / seam + supervisor pen / execution supervisors / hands / cold reviewers) →
   `docs/runbooks/STANDING_PROCEDURES.md`.
6. **HOUSING** (the API carrier path for pens; docs-only pens without a per-entry word; ref deletion
   is proxy-forbidden) → `docs/runbooks/STANDING_PROCEDURES.md`.
7. **THE FABLE BUDGET** (owner word 2026-08-06) → `docs/runbooks/STANDING_PROCEDURES.md`.
8. **ENVIRONMENT CARRIES** (the pinned venv, the canonical build, the weekly catchup verb, the N32
   payload recipe, the commit identities and trailers, the book note, evidence retention) →
   `docs/runbooks/STANDING_PROCEDURES.md`.

## What was NOT rehomed, and why

**PART B in its entirety.** It was a v642 snapshot of an act that has since landed, been superseded
and been recorded: current identities are now generated (`docs/STATE.md`), and the standing rulings
PART B carried are on the register with the owner's words and comment ids attached — **THE LEVEL LAW
at register v633, THE LIVE LAW and the ruled-but-not-live ledger at v637, THE COHORT-BOOK LAW at
v642.** Copying a stale snapshot into a new file is the failure this act exists to end, so it was
not copied. Look the entries up rather than trusting any prose about them, this tombstone's included:
`grep -o '· v637 [^·]*' docs/OPEN_ITEMS_REGISTER.md`.
