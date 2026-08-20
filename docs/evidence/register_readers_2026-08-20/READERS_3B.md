# READERS OF `docs/OPEN_ITEMS_REGISTER.md` — THE PLAN_v6 3b PRE-ACT

Read-only enumeration. Nothing in the repository was written; no build lock taken. Base: `main` @
`efbe1b6`, RULEBOOK v3, plan of record `docs/proposals/process_plan/PLAN_v6.md`.

*Base moved mid-enumeration:* the pricing seat committed `5f94a44` (the staircase-fix prereg) while
this was being written. **`docs/OPEN_ITEMS_REGISTER.md` is byte-identical across `efbe1b6..5f94a44`**
(`git diff --stat` empty), so every measurement below stands unchanged. Recorded, not smoothed.

> **3b. Open-items-register evolution … PRE-ACT — enumerate every reader of the current file;
> the new form keeps every found reader working or migrates it in the same act.**
> — `docs/proposals/process_plan/PLAN_v6.md:145-147`

This document is that enumeration, plus the measurements the migration has to satisfy.

---

## 0 · THE FILE, MEASURED

| quantity | value | how measured |
|---|---|---|
| size on disk | **2,145,250 bytes** | `ls -la` |
| characters (utf-8 decoded) | **2,117,698** | python `len(read())` |
| lines (`wc -l`) | **8,438** | trailing newline present |
| **line 1 length** | **1,314,529 chars** (62.1 % of the file) | `len(text.split('\n')[0])` |
| lines 2–8,438 | 803,169 chars | remainder |
| dated entry markers `· vNNN (date):` | **182**, v622 → v807, all inside line 1, strictly ascending | `re.finditer` |
| near-miss markers `· vNNN (` with a non-ISO date | **4** (see §3) | same |
| numbered legacy items before `## FABLE'S QUEUE` | **285** (numbers 1–407 with 122 gaps, no duplicates) | pen.py's own `ITEM_RE` |
| items after `## FABLE'S QUEUE` | **124** | same regex |
| `## `/`### ` headings outside line 1 | 12 | grep |
| N-number standing rulings defined | **28 distinct** (N1…N45), 125 occurrences | `\bN\d{1,3}\b` |
| entry body size (marker → next marker) | min 611 · median 3,094 · mean 7,821 · **max 810,588** | see §3 defect 2 |

### The exact header / tail-stamp format

Line 1 is one append-only stream with three fixed regions. Measured by diffing line 1 across
`HEAD~1 → HEAD` (the v806 → v807 pen):

```
[ FIXED PREFIX, 88 chars ]
# OPEN ITEMS REGISTER — the single durable list · maintained by the supervisor pen · v80
                                                                                     ^^^
                                     the version digits begin at char 86 (0-based 85-88)

[ MUTABLE MIDDLE, 1,310,628 chars at HEAD ]
7 2026-08-20 · PEN: ITEM 408: R14→R19 PROVENANCE MIGRATION DIRECTIVE ISSUED …
   … · v622 (2026-08-07): … · v623 (2026-08-07): …  (182 entries, OLDEST FIRST) … · v807 (2026-08-20): …

[ FROZEN TAIL STAMP, exactly 3,813 chars, byte-identical across the last pen ]
. · SEAM v540 (2026-07-29) — HANDOVER PEN: seam rotated at owner word at a clean boundary; …
… CURRENT_STATE Part B replaced wholesale to v32. · prior: ITEM 407
```

So the operative pen transaction today is: **bump the digits at char ~86 in place, and splice the
new `· vNNN (date): …` entry immediately before the 3,813-character `· SEAM v540 (2026-07-29)` tail
stamp.** That is exactly what `docs/CURRENT_STATE.md:393-396` writes down as law:

> *"PEN MECHANICS: register line 1 is the header; edit the version stamp **near char 86** SAME
> LENGTH (`v591 2026-08-06` → next); insert the entry **before the `· SEAM v540 (2026-07-29)`
> marker**; asserts: **line count 8,438 unchanged** · growth == entry length · one new stamp ·
> docs-only diff"*

The tail stamp is a fossil: it is the last thing `tools/seat/pen.py` ever wrote (`· prior: ITEM 407`
is pen.py's `first_clause()` pointer, §1 reader R1), and every pen since has appended *in front of
it* by hand rather than through the tool.

### Marker format variants, by era

| era | form | count | where |
|---|---|---|---|
| **pen-tool era** (to ~v540) | `· vN YYYY-MM-DD · PEN: <body> · prior: <clause>` — ONE stamp, rewritten each pen | 1 (the surviving header) | line 1, char 0-88 |
| **seam block** (v540) | `· SEAM v540 (2026-07-29) — HANDOVER PEN: …` | 1 | the frozen tail |
| **numbered-item era** (items 1–407) | `NNN. **TITLE (date).** prose`, blank-line separated, markdown-bold | 285 + 124 queued | lines 2-8,438 |
| **current entry era** (v622 → v807) | `· vNNN (YYYY-MM-DD): <BODY>` | **182** | line 1 |
| **current era, malformed dates** | `· vNNN (2026-08-10/11):`, `(2026-08-12/13):`, `(2026-08-17, late):`, `(2026-08-17/18):` | **4** | line 1 |
| inline back-references | `(vNNN)`, `register vNNN`, `NNN` item numbers, `N29`-style N-numbers | 115 / 556 / 334 / 202 | tree-wide |

There is **no entry marker at all** for v541–v621 — the record between the seam and the first dated
marker is undelimited prose. `tools/incident_index.py` states this on its own front page and refuses
to index it, which is the right call and must survive 3b.

---

## 1 · THE READERS — COMPLETE TABLE

Legend for **reads**: `HDR` = line 1 header only · `L1` = the whole of line 1 · `MARK` = the
`· vNNN (date):` markers · `TAIL` = the frozen `SEAM v540 … prior:` stamp · `ITEM` = the numbered
`NNN.` items · `FULL` = the whole file · `PTR` = cites an address into the file without opening it.

### A · EXECUTABLE READERS (code that opens the file)

| # | file:line | what it reads | what it does with it | 3b constraint |
|---|---|---|---|---|
| **R1** | `tools/seat/pen.py:30` `DEFAULT_REGISTER`; `:34` `HDR_RE = · v(\d+) (\d{4}-\d{2}-\d{2}) · PEN: (.*)$`; `:35` `ITEM_RE = ^(\d+)\. `; `:32` `FABLE_MARKER = "## FABLE'S QUEUE"`; `:90-129` `cmd_append`; `:170-190` `cmd_verify` | `HDR` + `ITEM` + the `## FABLE'S QUEUE` marker | **The only sanctioned writer.** `append` bumps vN→vN+1 in the header, splices item text before `## FABLE'S QUEUE`, asserts every replacement matches exactly once (the item-147 law), asserts item-number uniqueness, commits and pushes `HEAD:main` with `PEN_TOKEN`. `verify` prints version/date/item count/duplicates. | **3b names this explicitly**: *"tools/seat/pen.py (and any tool defaulting to the old file) is repointed IN THE SAME ACT"*. Note it is ALREADY stale against practice — it writes items into `## FABLE'S QUEUE` position and rewrites the PEN summary, which is not how any of the last ~180 entries were made. Repointing it is not enough; **its append model must be replaced, not redirected**, or it will corrupt the frozen file on its first real invocation. `verify` should be repointed to a new-form validator. |
| **R2** | `tools/seat/orient.sh:33-44` | `HDR` — `head -n1`, asserts non-empty (SILENCE IS A RED), truncates to first 200 chars | Tier-3 freshness check printed to every incoming seat; a missing/empty file is a hard `die`. | The new form must keep **a single first line whose first 200 characters carry the version + the freshest summary**, or orient.sh must be repointed in the same act. Note orient.sh currently slurps 1.3 MB into a bash variable to print 200 bytes — the freeze is an opportunity to fix that, but the *contract* is "line 1, first 200 chars, non-empty". |
| **R3** | `tools/incident_index.py:48` `REGISTER_REL`; `:57` `ENTRY = ' · v(\d+) \((\d{4}-\d{2}-\d{2})\):'`; `:105-113` `entries()`; `:60-68` `RULES`; `:88` `_EXPLICIT = incident:\s*(yes\|no)` | `MARK` + the body between consecutive markers | Generates `docs/incidents/INDEX.md` + `index.json`. **Never writes the register.** Already designed for 3b: post-3b entries MAY carry an explicit `incident: yes\|no` field which the generator PREFERS. | **The binding input contract** (PLAN_v6 1e). Frozen history must keep the marker bytes exactly. New-form entries must either (a) still emit a ` · vNNN (YYYY-MM-DD):` marker the generator can find, or (b) the generator gains a second, file-based front end in the SAME act. Its docstring's measured claim ("178 entries, v622-v803") is now stale — see §3 defect 1. |
| **R4** | `docs/evidence/rulings_sweep_2026-08-13/tools/segment_register.py:16` `REG`; `:18` `SEP = (?<=[.)”"a-zA-Z0-9]) · `; `:46-56` | `FULL` — splits line 1 on the bare ` · ` separator, splits lines 2+ into blank-line blocks | ORDER 27 rulings sweep: produced `units.json` → `RULINGS_INVENTORY.json`. Read-only on the register. | Evidence-tree tool, retention-protected. It hard-codes both the "line 1 is one prose stream" and the "lines 2+ are blank-line blocks" assumptions. It will not run against a new form. **Decide explicitly: freeze it beside the frozen file as a historical instrument (recommended — it is evidence, not live tooling), or repoint.** Do not leave it silently broken and citable. |
| **R5** | `docs/evidence/rulings_sweep_2026-08-13/tools/build_inventory.py:1252` | `PTR` — names the register in a `sources` list; consumes R4's `units.json` | Builds the rulings inventory of record. | Same disposition as R4. Its `sources` string is a provenance claim about a file whose form is about to change; the freeze tombstone is what keeps that claim true. |
| **R6** | `docs/evidence/landing_tail_2026-08-20/append_landing_transition.py:73` | `PTR` — hard-coded citation string `"docs/OPEN_ITEMS_REGISTER.md v782 (2026-08-20): \"THE LANDING. Owner word verbatim…\""` | Wrote that string into `data/release_lineage.json:379` — a durable, owner-ruled lineage record. | **A frozen citation into a frozen file: this one is SAFE by construction** provided history is frozen byte-exact. It is the clearest argument for tombstone-then-freeze over rewrite. |
| **R7** | `session_2026-07-29/item262/migrate_positions.py:234` `EXEMPT_FILES = ('docs/OPEN_ITEMS_REGISTER.md', 'LTI_REGISTER.md')` | `PTR` — an *anti*-reader: names the register so a tree-wide position-token rewrite skips it | Directive-level exemption ("archives and the register — exempt by directive"). | **A migration hazard, not a reader hazard.** Any future tree-wide migration will exempt the *old path only*. If the record continues in new files, **the exemption must be extended to the new location in the same act**, or the next sweep will rewrite the durable record's prose. |

### B · GENERATED / DERIVED ARTIFACTS THAT CARRY THE REGISTER'S CONTENT

| # | file:line | reads | 3b constraint |
|---|---|---|---|
| **R8** | `docs/incidents/INDEX.md:1-14` + `docs/incidents/index.json` | R3's output; the banner names the register as the durable record | Regenerated by R3. Coverage line is prose ("178 register entries, v622–v803") and goes stale silently — **currently stale**, see §3. |
| **R9** | `data/release_lineage.json:379` | `PTR` — quotes register v782 verbatim as the provenance of an owner ruling | Frozen citation; safe iff history is frozen byte-exact and `vNNN` stays resolvable as an address. |
| **R10** | `tools/seat/samples/orient.out.txt:10,27` | golden sample of R2's output, including the line `-- open-items register header (docs/OPEN_ITEMS_REGISTER.md line 1) --` | If R2 is repointed, this sample must be regenerated **in the same act** or it becomes a stale golden. |

### C · CI

| # | file:line | reads | 3b constraint |
|---|---|---|---|
| **R11** | `.github/workflows/live-scoring.yml:56,137`; `.github/workflows/fv-provenance.yml:20` | `PTR` — comment-grade `register item 399` ("stale-boot-pin bug") justifying a scoped exclusion | Not parsed. Survives the freeze provided `item 399` stays resolvable. |
| **R12** | *(negative finding)* | — | **No CI job and no acceptance check reads the register, and none runs `tools/incident_index.py check`.** Verified by grep over `.github/workflows/`, `.github/actions/`, `acceptance/checks/`. `acceptance/checks/__init__.py` registers `doc_lint` and `rulebook_lint`, and neither touches the register. **Consequence: the 1e generator has no gate, which is why its staleness (§3) went unnoticed.** 3b should land `incident_index check` as an acceptance check in the same act — otherwise the generated index repeats the exact CURRENT_STATE failure mode P6 names. |

### D · AUTHORITY DOCUMENTS THAT CITE IT AS THE RECORD

| # | file:line | what it says | 3b constraint |
|---|---|---|---|
| **R13** | `docs/RULEBOOK.md:96` — law 11 SEAM PATTERN | *"register is the single durable list"* | Owner-signed law text. If the record continues in a different container, **law 11's wording is about the record, not the file** — confirm with the owner whether the amendment he must give for the single-list rule (see R18) also needs a law-11 wording pass. Do not amend the RULEBOOK silently. |
| **R14** | `docs/RULEBOOK.md:135` (P6 GENERATED-ONLY incident), `:144` (P8 EXPLICIT PATHS incident, *"register v786"*), `:49` | Both process laws name the register as the evidence of the incident that created them | `register vNNN` must stay a resolvable address after the freeze. |
| **R15** | `docs/ENGINE_PRIMER.md:9` | *"Where it disagrees with the register or a primary document, the primary record wins"* | Pointer-only; survives a freeze, but the primer's `:1` header cites `register v598 / v593 / v591` as its own provenance. |
| **R16** | `docs/ENGINE_PRIMER.md:201-205` | *"'N-numbers' (N29, N32, N35, N43, N45 …) are the register's numbered standing rulings — **look one up by grepping the register for its number**; never read the register front to back"* + *"the laws of record: … the register (by pointer only)"* | **A grep-shaped reading contract.** 28 distinct N-numbers, 125 occurrences, all inside the frozen text. A split into many files breaks a single-file grep unless the new form ships a documented `grep -r` idiom or a generated N-number index. |
| **R17** | `docs/CURRENT_STATE.md:7-8` (*"the register wins and this file is wrong"*), `:33` (the one-line rule), `:113`, `:184` (*"register v629 (8,438 lines)"*), `:376` (*"the register by pointer (grep N-numbers)"*), `:415` (reading order; *"the v604 register entry IN FULL is mandatory"*) | Live-state doc; also the file PLAN_v6 3c retires | `:184` hard-codes the **line count 8,438** as an identity. That number becomes permanent on the freeze — good. But 3b and 3c interact: **do the 3b repointing before or with 3c, not after**, or the 3c act inherits a doc full of pointers to a file that just changed form. |
| **R18** | `docs/CURRENT_STATE.md:393-396` — PEN MECHANICS | the char-86 offset, the `· SEAM v540 (2026-07-29)` insertion point, and the **line count 8,438 / growth == entry length** asserts | **This is the operative write procedure, and it lives in the file 3c retires.** 3b must rehome it (or explicitly retire it) in the same act. A frozen file with a live "how to append to it" procedure sitting in another doc is exactly the class P11 legislates against. |
| **R19** | `docs/directives/SEAT_CHARTER_seam.md:11-13` | *"Supervisor pen: the ONLY writer of the durable register (`docs/OPEN_ITEMS_REGISTER.md`, header-pen style, version + PRIOR chain; history in git)"* | Names the path AND the form. Owner-directed charter — repoint in the same act. |
| **R20** | `docs/directives/SEAT_CHARTER_seam.md:41,47-49` | *"read ONLY the register sections your first task touches, via the version pointers CURRENT_STATE gives you"*; *"**THE FULL-HEADER READ IS RETIRED.** It cost 75–100k tokens, the header now exceeds 320KB … The register remains the record … read BY POINTER, never front-to-back"* | The 320 KB figure is now **1.31 MB** — the charter's own datum is 4× stale. The new form's headline benefit to state plainly to the owner: a fresh seat can read the current state without loading a megabyte. |
| **R21** | `docs/proposals/process_plan/PLAN_v6.md:5, 80-88, 145-155` | the lock-in pen requirement; the 1e input contract; 3b itself | Self-referential: 3b is defined by this text. |
| **R22** | `docs/OPEN_ITEMS_REGISTER.md` lines 2-4 — the in-file rule block | *"### RULE (owner-driven, 2026-07-11): nothing is 'on a list' unless it is in THIS file. Every parked, deferred, gated, or owner-raised item lives here with its SOURCE and its TRIGGER. Chat memory is not a register."* | **THE OWNER-AUTHORED RULE.** PLAN_v6 3b: *"the owner's word amending the register's own single-list rule … RIDES THE ACT — that rule is owner-authored and only his word amends it."* **This is a hard gate, not a step.** |
| **R23** | `docs/incidents/INDEX.md:4` (banner), `docs/HANDOVER_R19_MVP_RELEASE_2026-07-22.md`, `docs/directives/ITEM_408_claims_note.md`, `docs/referee/F3_REVIEW_v0_3.md`, `docs/referee/FHV_MARKET_STUDY_2026-07-29.md`, `docs/proposals/process_plan/REVIEW.md`, `REVIEW_COLD_OPUS.md`, ~20 `docs/evidence/*/` prereg + FINAL_STATE files, 53 `docs/archive/00_MANIFEST_v4_*.md`, 5 `docs/archive/CORE_v2_*.md`, 4 `docs/archive/DECISIONS_v9*.md`, 11 `docs/archive/HANDOVER_rev1*.md`, `ui/PLAN_v1.3.md`, `ui/data/movers_transition.js`, `engine/rl_after/ingestion/PLAN.md`, `FIRST_COMMANDS_PROOF.txt` | `PTR` — 168 path references across **119 files** | Archive/evidence citations are **retention-protected history** and must NOT be rewritten. This is the second argument for freeze-in-place: the only migration that keeps 119 files honest is one where the old path keeps resolving to the old bytes. |

### E · HUMAN READING CONVENTIONS RECORDED IN THE TREE

These are readers too — they are the instructions a compacted seat follows, and 3b changes every
one of them.

| # | where | the convention, verbatim |
|---|---|---|
| **R24** | register line 1, **char 1,097,892** (inside entry **v736**) | *"**NOTE FOR A FUTURE COMPACTED SUPERVISOR: this register file is ONE LINE and entries accumulate OLDEST-FIRST before the SEAM marker — grep for the HIGHEST v number, do not read from the start.**"* |
| **R25** | register line 1, **char 1,179,759** (entry **v763**) | *"the register is ONE LINE, entries oldest-first — **grep the HIGHEST v number**; pen via the scratchpad `pen_vNNN.py` template (byte-exact asserts)"* |
| **R26** | register line 1, **char 1,279,718** (entry **v797**) | *"THE LAWS RIDE: … the register is ONE LINE, **grep the HIGHEST v.**"* |
| **R27** | register line 1, char 320,473 | *"if it cannot plausibly stop the thing working it gets ONE LINE in the register and nothing else"* — the one-line triage rule, echoed at `docs/CURRENT_STATE.md:33` |
| **R28** | `docs/ENGINE_PRIMER.md:201-205` | the N-number grep law (see R16) |
| **R29** | `docs/CURRENT_STATE.md:376` | *"the register by pointer (grep N-numbers); one pen per boundary, batched"* |
| **R30** | `docs/directives/SEAT_CHARTER_seam.md:47-49` | *"THE FULL-HEADER READ IS RETIRED … read BY POINTER, never front-to-back"* |

**Note on R25:** the pen of record is *"the scratchpad `pen_vNNN.py` template"* — a per-pen throwaway
script, not `tools/seat/pen.py`. The tool named in the charter (R19) and in PLAN_v6 3b has not been
the actual writer for ~180 entries. **3b must say so out loud**, or it will "repoint" a tool that
nobody uses while the real practice — hand byte-surgery from a scratchpad script — walks straight
into the new form. *3b's stated retirement is "pen byte-surgery"; this is the byte-surgery.*

### F · THE DIFFUSE READER CLASS — CITATION BY ADDRESS

Not files that open the register, but **addresses into it that must keep resolving.** Measured
tree-wide (excluding `.git`, `.claude/worktrees`, `__pycache__`, `vendor`, and the register itself):

| address form | occurrences | files |
|---|---|---|
| `register vNNN` | **556** | **336** |
| `register item NNN` | **334** | **98** — including `engine/rl_after/_merged_recover.py` (×6), `rl_export.py` (×2), `rl_model.py` (×2), and 3 CI workflow comments |
| N-numbers (`N29`/`N32`/`N35`/`N41`-`N45`) | **202** | **80** |
| explicit `OPEN_ITEMS_REGISTER` path | **168** | **119** |

**Engine source cites the register by item number.** `_merged_recover.py:37,65,75,192,323,1018,1031,1077`
carry `register item 106 / 17 / 65 / 134 / 128 / 108`; `rl_model.py:895,2047` carry `265 / 17`;
`rl_export.py:122,733` carry `26 / 24`. These are comments, but they are the provenance of live
pricing behaviour, and P11 (*the retirement is recorded where the gate lives*) makes them
load-bearing. Any migration that renumbers, re-keys or re-splits the historical record breaks them.

---

## 3 · DEFECTS FOUND IN THE PRE-ACT (report these; do not fix in a read-only seat)

**Defect 1 — the generated incident index is STALE, and nothing gates it.**
`python3 tools/incident_index.py check` → **exit 1**, `104 incidents / 182 indexed entries; 2 stale
generated file(s)`. The committed `docs/incidents/INDEX.md:10` still reads *"Coverage: 178 register
entries, v622–v803"*; the register is at 182 entries, v622–v807. The generator's own module
docstring carries the same stale measurement (`tools/incident_index.py:23-25`). It is not wired into
CI or the acceptance runner (R12), so a GENERATED-ONLY surface is drifting exactly the way
`docs/CURRENT_STATE.md` did — the incident P6 exists for. **Land `incident_index check` as an
acceptance check in the 3b act.** *(Trivial to close: `tools/incident_index.py write` regenerates it.
Not done here — this seat writes nothing to the repo.)*

**Defect 2 — the last entry's body is the entire rest of the file.**
`entries()` slices each marker to the *next* marker, and the last marker to `len(text)`. The last
marker is v807 at char 1,307,089; line 1 ends at 1,314,529; **the remaining 803,169 characters —
every numbered legacy item, the whole pre-marker record — are attributed to entry v807.** Its body
measures **810,588 chars against a 3,094-char median.** Consequences: v807 will always classify as
an incident, and its reported snippets are drawn from prose written weeks earlier. The freeze makes
this permanent unless the generator gains an end-of-region sentinel. **Cheapest correct fix, and it
belongs in the 3b act: make the tombstone line a terminating sentinel the generator honours, so the
frozen region ends where the record ends.**

**Defect 3 — four entries are invisible to the generator because their date field is not a date.**
`· v640 (2026-08-10/11):` · `· v700 (2026-08-12/13):` · `· v727 (2026-08-17, late):` ·
`· v728 (2026-08-17/18):`. `ENTRY` requires `\d{4}-\d{2}-\d{2}`, so these four never open an entry
and their prose is silently absorbed into the preceding entry's body — mis-attributing days of
record. 186 marker-shaped strings, 182 parsed. **The generator's docstring already says "four
further `· vNNN (` occurrences carry no date and are not entry markers" — it noticed them and
classified them as non-markers. They are markers.** The freeze makes this permanent. Fix the regex
(widen the date group and normalise) in the 3b act, *not* the register text — retro-editing the
append-only record is precisely what 1e forbids.

**Defect 4 — the sanctioned pen tool is already divergent from practice.** See R1 / R25 note.

---

## 4 · THE MIGRATION CONSTRAINTS THIS IMPLIES

Numbered so the act can be checked against them one by one.

**C1 — FREEZE MEANS BYTE-EXACT, AND THE OLD PATH KEEPS RESOLVING.**
119 files and 168 path references, 556 `register vNNN` citations, 334 `register item NNN`
citations — 12 of them inside live engine source — and one owner-ruled provenance record
(`data/release_lineage.json:379`) that quotes v782 verbatim. **`docs/OPEN_ITEMS_REGISTER.md` must
stay at its current path with its current bytes.** No renumbering, no re-splitting, no reflowing of
line 1, no retro-tagging (1e forbids it in terms). The tombstone is an *append* — and it is the
**last** append: it lands in the mutable middle, before the frozen tail stamp, exactly like every
entry since v622, and it bumps the version digits at char 86 one final time.

**C2 — THE OWNER'S WORD ON R22 IS A GATE, NOT A STEP.**
*"nothing is 'on a list' unless it is in THIS file"* is owner-authored (2026-07-11) and only his
word amends it. It rides the act. **No part of 3b may land ahead of it**, because every other step
presumes the record continues somewhere else. Present it as one sentence and one consequence, not as
a plan.

**C3 — R3'S INPUT CONTRACT IS THE ONE MACHINE CONTRACT, AND IT IS ALREADY WRITTEN.**
`tools/incident_index.py` parses ` · vNNN (YYYY-MM-DD):` and nothing else, and it already carries the
post-3b escape hatch (`incident: yes|no`, preferred over the pattern rules). Therefore: **new-form
entries carry an explicit `incident:` field** — that is the designed path, and it makes the pattern
rules a fallback for frozen history only. The generator needs, in the same act: a second front end
over the new-form files, the end-of-frozen-region sentinel (defect 2), and the widened date group
(defect 3). Its coverage prose must become computed, never typed.

**C4 — THE FOUR MACHINE READERS MUST BE DISPOSED OF EXPLICITLY, EACH BY NAME.**
- `tools/seat/pen.py` — **replace, don't repoint** (R1). Its append model targets `## FABLE'S QUEUE`
  and rewrites a PEN summary; pointed at a new-form directory it is wrong in a new way. `verify`
  becomes a new-form validator (version monotonicity, no duplicate entry ids, marker well-formedness).
- `tools/seat/orient.sh` — repoint, **and regenerate `tools/seat/samples/orient.out.txt` in the same
  commit** (R10). Contract to preserve: *one first line, first 200 chars, non-empty, carries the
  version and the freshest summary; missing or empty is a hard die.*
- `tools/incident_index.py` — extend per C3.
- `segment_register.py` / `build_inventory.py` — **freeze as historical instruments beside the frozen
  file** (recommended) or repoint. Either way, say which, in writing, in the act. An evidence tool
  that silently stops running is the P5 pattern ("a gate's name is not coverage").

**C5 — THE HUMAN CONVENTIONS ARE THE MOST-USED READER AND THE EASIEST TO STRAND.**
Six recorded conventions (R24–R30) all say the same three things: *one line · oldest-first · grep the
HIGHEST v · never read front to back.* Every one is false the moment the form changes. The new form
must ship its own reading law **in a durable home, not in a register entry** — the frozen file's
tombstone will not be where a fresh seat looks. Candidates, in the estate's own idiom: the RULEBOOK
(PART 4, as a process law) plus the new record's own directory README. It must answer, in one screen:
*where is the newest entry · how do I find entry vNNN · how do I find `N32` · how do I find `item 399`.*

**C6 — `vNNN` AND `item NNN` MUST REMAIN GLOBAL, MONOTONE ADDRESSES ACROSS THE SEAM.**
890 citations depend on it. The new form continues the **same** version counter (v808, v809, …) — it
does not restart. Item numbers do not get reused. A generated index that resolves a version or an
item number to a file+offset is the cheapest way to keep 890 pointers honest, and it is generated, so
it is allowed to exist under P6.

**C7 — THE WRITE PROCEDURE MUST MOVE OUT OF `docs/CURRENT_STATE.md` IN THIS ACT.**
`CURRENT_STATE.md:393-396` is the operative pen procedure and hard-codes char 86, the `SEAM v540`
insertion point, and the 8,438-line assert. The file it lives in is retired by 3c. Leaving a live
append procedure for a frozen file inside a doc that is about to be deleted is a P11 breach waiting
to be filed. **Rehome or explicitly retire it, in the same act as the freeze.**

**C8 — CURRENT_STATE'S IDENTITY CLAIMS FREEZE TOO.** `:184` reads *"register v629 (8,438 lines)"*.
After the freeze that line count is permanent and the claim becomes a *true* historical identity —
which is a small argument for stating the frozen file's final identity (bytes, lines, entry count,
final version) **in the tombstone itself** so the freeze has a falsifier: `2,145,250 bytes ·
8,438 lines · 285 numbered items + 124 queued · 182 dated entries · v622–v8NN` at the sealing commit.

**C9 — EXTEND THE MIGRATION EXEMPTION.** `migrate_positions.py:234`'s `EXEMPT_FILES` names the old
path only (R7). The new record's location inherits the exemption, or the next tree-wide token sweep
edits the durable record's prose.

**C10 — THE ACT ITSELF MUST BE PENNED INTO THE OLD FILE.** PLAN_v6:5 requires the lock-in penned
verbatim to the register. The freeze act's own record is the last thing the old file receives —
tombstone, owner's word on R22, and the final identity (C8) in one entry, then the file never moves
again.

---

## 5 · WHAT 3b HAS TO DELIVER, AS A CHECKLIST

1. Owner's word amending R22 (the single-list rule) — **obtained first** (C2).
2. Final entry penned to `docs/OPEN_ITEMS_REGISTER.md`: tombstone + where the record continues +
   the frozen identity (C1, C8, C10).
3. `tools/seat/pen.py` **replaced** by the new-form writer; `verify` becomes the new-form validator (C4).
4. `tools/seat/orient.sh` repointed **+ `samples/orient.out.txt` regenerated** (C4).
5. `tools/incident_index.py`: new-form front end · frozen-region sentinel (defect 2) · widened date
   group (defect 3) · computed coverage prose (defect 1) — and **wired into the acceptance runner** (R12).
6. `segment_register.py` / `build_inventory.py` dispositioned by name in writing (C4).
7. `migrate_positions.py` exemption extended (C9).
8. `SEAT_CHARTER_seam.md:11-13,41,47-49` repointed; its stale "320KB" datum corrected (R19, R20).
9. The reading law rehomed to a durable home (RULEBOOK PART 4 + the new record's README), answering
   the four lookup questions (C5).
10. `CURRENT_STATE.md:393-396` pen mechanics rehomed or retired (C7); sequenced with 3c (R17).
11. A generated address index: `vNNN` → file, `item NNN` → file, `N-number` → file (C6).
12. Regenerate `docs/incidents/INDEX.md` + `index.json` (defect 1) — before the freeze, so the last
    generated index of the old world is current.

**Reader count: 30 enumerated readers (R1–R30) across 7 executable scripts, 3 generated/derived
artifacts, 3 CI comment sites, 11 authority-document sites and 7 recorded human conventions —
plus a diffuse class of 1,260 address citations (556 `register vNNN` · 334 `register item NNN` ·
202 N-numbers · 168 path references) spread over 119+ files.**
