# ORDER 27 — THE REGISTER-WIDE STANDING-RULINGS SWEEP — METHOD

**Seat:** ORDER 27 sweep seat (Opus, isolated worktree, branch `evid/rulings-sweep`).
**Commissioned:** owner word 2026-08-13, filed as #334 comment 5274888553 — *"Yes, please commission a
sub agent to do the register wide standing ruling sweep for anything that might have slipped. Do not
assume the rulings as ground truth, but find-don't-act on them, and bring anything flagged back to me."*
**Committed BEFORE any findings**, per the brief's method discipline.

**Standing posture: FIND, DON'T ACT.** This seat changes no code, fixes nothing, adjudicates nothing,
picks no winner between colliding rulings. It is strictly read-only outside
`docs/evidence/rulings_sweep_2026-08-13/`. Nothing merges.

---

## 1. Sources, primary to secondary

| # | Source | Treatment |
|---|--------|-----------|
| 1 | `docs/OPEN_ITEMS_REGISTER.md` (1,765,759 bytes; line 1 = 962,590 bytes of appended entry prose, v1→v702; 8,438 further lines of SEAM-era content) | **Primary.** Full mechanical pass; see §2–§4. |
| 2 | `data/owner_overrides.json` | Display-layer overrides — each checked for "still applied as documented". |
| 3 | `docs/directives/` | Directives carry rulings in their heads and amendments. |
| 4 | `#334` comment bodies (GitHub) | Fetched **only** where a register entry cites a comment id for owner words AND the register's own quote is truncated AND the distinction is load-bearing. |
| 5 | Engine code / configs / data artifacts / live board files | Phase-3 verification substrate only. Never edited. |

## 2. Chunking the register (the coverage spine)

The register is not line-structured: entry prose is appended onto a single ~962 KB first line, and the
older SEAM-era content follows as ordinary lines. Segmentation is therefore mechanical and reproducible
(`tools/segment_register.py`):

- **line-1 stream** → split on the register's own entry separator `' · '` (with a preceding
  word/punctuation character required, so decimal points and mid-sentence dots do not split) →
  **2,507 SEG units** (mean 380 chars, max 7,957).
- **lines 2+** → split on blank lines → **404 BLK units**.
- **Total 2,911 units**, covering 100% of the file's bytes. Every unit carries a stable id
  (`SEG0000…SEG2506`, `BLK0000…BLK0403`) used as the citation key throughout the inventory.

Version markers (`v1`…`v702`) are *not* reliable delimiters — only 92 distinct `· vNNN` markers exist on
line 1 (the newest era, v622→v702, is delimited that way; earlier entries cite versions inline, e.g.
"(v464, 2026-07-26)"). The inventory therefore records **unit id + the version marker(s) named inside the
unit**, which is the honest form of "which entry says this".

## 3. Screening lexicon (recall-first, two tiers)

**CORE markers** (a unit containing any of these is treated as ruling-bearing and read verbatim):
`OWNER RULING`/`owner-ruled`/`RULED`/`RULING`, `owner word(s)`, `owner override`/`overrule`,
`owner-caught`, `verbatim`, `filed <comment-id>`, `owner-directed`/`owner-ordered`/`owner-driven`/
`owner-raised`/`owner-approved`, `ratified`, `owner said/says`, `DEFERRED (owner…)`, `THE … LAW`,
`STANDING`, `EXCLUDE`/`EXCLUSION`, `FROZEN RULER`, `OWNER INPUT`, `owner act`/`owner release`.

**BROAD-only markers** (weaker ruling vocabulary; units that carry these but no CORE marker are still
read, at a narrower window): `LAW`, `MUST`, `NEVER`, `ALWAYS`, `convention`, `binding`, `mandate`,
`PARKED`, `DEFERRED`, `FROZEN`, `override`, `his word`, `standing`.

## 4. Reading procedure (systematic, not sampled)

`tools/extract_windows.py` cuts, for **every** CORE-marker occurrence anywhere in the register, a
±500-character context window, merging overlaps inside a unit; BROAD-only units get ±320-character
windows. Result: **901 CORE windows (673,582 chars) across 809 units**, plus **357 BROAD-only windows
(169,117 chars)**. All of it — 842,699 chars — is read verbatim by the seat, in ordered chunks, in
register order, start to finish. No window is skipped, and no unit is judged from its id alone.

The residue (units with no ruling vocabulary at all, and the non-window remainder of hit units) is
**mechanically characterised, not read**: it is reported in the coverage statement with exact unit and
byte counts, and the screen that classified it is committed here so the owner can re-run it. This is the
one place where coverage is less than "every byte read by eye", and it is stated plainly rather than
implied away.

## 5. Extraction rubric (Phase 1)

A unit yields a **ruling record** when the register attributes a decision to the owner, or records a
standing law/convention/exclusion the register itself treats as binding. Recorded fields:

- `id` — sweep-local `R###`.
- `units` / `versions` — where it is stated in the register (unit ids; version markers named in-text).
- `quote` — **verbatim** owner/register words where short; a tight citation (unit id + opening words)
  where the passage is long.
- `subject` — subject area (pricing core, store discipline, curve/ruler, pool/pathway, process/seat
  conduct, UI/board display, data/ingestion, gates/CI, …).
- `register_status_claim` — what the register *itself* says the ruling's status is (LANDED, parked,
  superseded, queued…). Recorded as a claim, never adopted as truth.
- `triage` (Phase 2) and `verification` (Phase 3).

### Avoiding double-counting restatements

Rulings are restated constantly (later entries re-quote earlier ones to carry them forward). The rule:

1. **One ruling = one record, keyed to its EARLIEST statement** in the register.
2. A later unit that repeats a ruling without changing its content is appended to that record's
   `units`/`versions` list as a **restatement**, never given its own id. Detection: the later text cites
   the earlier version (`per v###`, `as v### ruled`, `restated`, `carried`), or its ruled sentence is
   substantially the same proposition.
3. A later unit that **changes** the ruling's content gets its own record and the pair is linked
   (`supersedes` / `superseded_by`) — and Phase 2 classes the earlier one SUPERSEDED **without picking a
   winner**; both readings go to the owner where the supersession is not explicit.
4. Where it is genuinely unclear whether a later statement restates or amends, the record is kept
   separate and FLAGGED as AMBIGUOUS rather than silently merged.
5. Rulings issued in the same act but on different objects (e.g. the thirteen 26B rulings) are separate
   records — they bite at different sites and verify differently.

## 6. Triage rubric (Phase 2)

| Class | Test |
|-------|------|
| **LIVE-STANDING** | Should bind the machinery or the process *today*: a law, exclusion, convention, or configuration the board/engine/data is supposed to honour on every run. → Phase 3. |
| **PROCESS-LAW** | Binds the seat's conduct rather than the code (evidence discipline, staging, no-model-IDs, one-lever, owner-word-before-write). → Phase 3 (verified against recent practice where checkable). |
| **ONE-TIME-COMPLETED** | Discharged by a single act, no ongoing bite (a specific pin, a specific correction, a landing). |
| **QUEUED** | Ruled but not yet due (parked with a resurrection trigger, ordered-but-not-fired, deferred to a named later act). |
| **SUPERSEDED** | A later entry changes it. Both entries cited; **no winner picked**. |

Only LIVE-STANDING and PROCESS-LAW proceed to verification. Boundary calls are recorded with the reason.

## 7. Verification rubric (Phase 3)

For each LIVE-STANDING ruling, the seat reads the actual machinery — engine code, configs, data
artifacts, the live board where relevant — and assigns exactly one:

| Class | Meaning | Evidence required |
|-------|---------|-------------------|
| **ENFORCED** | A machine check, config value, or code site implements it such that a regression fails or is impossible. | the check/site named at `file:line`. |
| **DELIVERED-UNGUARDED** | The current state honours it, but nothing prevents regression (no assert, no test, no gate). | the honouring site at `file:line`, plus the absence-of-guard search that was run. |
| **NOT-REFLECTED** | The machinery does not do what the ruling says. **FLAG.** | the code-verified evidence of the divergence. |
| **AMBIGUOUS-OR-CONFLICTING** | The record is unclear, or two rulings collide. **FLAG, both readings stated.** | both citations. |

PROCESS-LAWS are verified against recent practice where checkable (the register's own recent entries,
commit/PR shape, evidence trees); otherwise **UNVERIFIABLE-BY-CODE**.

**Rulings are not ground truth.** Where a ruling looks stale, contradicted by later evidence, internally
inconsistent, or simply wrong on the facts, that is itself a **FLAG with the evidence** — never a silent
judgement in either direction, and never a correction by this seat.

Negative evidence discipline: "no guard exists" is only written after a named search (grep pattern +
paths searched) that is recorded in `VERIFICATION.md`, so the owner can re-run it and disagree.

## 8. Deliverables and phase gates (commit + push each)

| Phase | Deliverable |
|-------|-------------|
| 0 | `METHOD.md` (this file) + `tools/` — committed before any findings. |
| 1 | `RULINGS_INVENTORY.json`, `INVENTORY.md` + coverage statement. |
| 2 | Triage classification folded into both. |
| 3 | `VERIFICATION.md` — per-ruling machinery check with `file:line` citations. |
| 4 | `FLAGS.md` — owner-facing: flags only, severity order, plain language, plus coverage-and-confidence and the inventory summary table. |

Push after every phase (a silent hour reads as a dead build). PR to main at the end. **MERGE NOTHING.**
No model IDs in commits. Never `git add -A` — every commit stages named paths under this evidence
directory only.
