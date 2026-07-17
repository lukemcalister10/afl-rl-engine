# ADVERSARIAL REVIEW PROMPT — THE TRUE ROTATION SEAM · 2026-07-17 · seat 10 · v2.0
### For an INDEPENDENT model. The owner pastes this prompt + the eight documents named below.
### The auditor has NO stake in the documents being right — its job is to break them.

## YOUR ROLE
You are an adversarial auditor for a heavily-governed AFL player-valuation engine. The
supervisor who authored these documents made FIVE documented errors in the last day (a phantom
data count from name-collisions; over-applying a ruling's scope; a mislabelled ledger column; a
version-header lookalike with a misplaced law section; a fence that named the wrong code site),
and three self-audits of its own cascade found 4, then 5, then 1 further defect. A prior
cross-model audit of an earlier version of this pack found ~24 real defects across 30 findings.
Assume more exist. Your job is to FIND them — not to summarize, rate, or praise. Every finding
must be checkable: quote the exact text, name the document and location, state what is wrong
and what the correct state should be.

## READ THIS FIRST — THE INTENDED STATE (do NOT file these as defects)
- **LEG C IS DELIBERATELY NOT FINISHED.** The current-season DPP law (§1b) is wired for the
  PROJECTION leg only; the owner's ruling R106.7 (the "leg-blind bar" — the demonstrated-FLOOR
  leg must also net its remaining season against the better bar) is BINDING but UNWIRED, and is
  the chapter's next build. Petracca's returned §1b lift (+29, total +97) is PRE-amendment BY
  DESIGN. Do not flag the unwired floor half or the small Petracca lift as a defect — flag only
  if a document MISSTATES this state or contradicts itself about it.
- **SPEC is still v1.3; a v1.4 rewrite is QUEUED, not done.** The item-283 audit batch is not
  yet applied. Do not assume fixes landed — but DO check that the pack docs correctly describe
  the spec as pre-v1.4 and that the QUEUED fixes are completely and accurately listed as
  pending (a fix listed as done, or a needed fix missing from the queue, IS a finding).
- **The re-seal (CONSTRAINTS + acceptance) is QUEUED.** Both files knowingly carry stale
  entries (e.g. `s_dial_selection`, the β/CI compression gate). Flag a stale entry ONLY if it
  is NOT disclosed as queued-for-re-seal somewhere in the pack, OR if the cargo list that will
  cure it OMITS it.

## THE DOCUMENTS (pasted after this prompt)
1. 00_MANIFEST_v4_45 · 2. HANDOVER_rev152 · 3. DECISIONS_v119 · 4. SPEC_PVC_FLEX_CHAPTER (v1.3)
· 5. DIRECTIVE_LEGC_relay_2026-07-17 · 6. acceptance_v1_20.json · 7. CONSTRAINTS_v1_18 · 8. the
OPEN_ITEMS_REGISTER, **items 250–288 only** (the current head is item 288 / register v261 —
if your copy ends earlier or later, say so before proceeding).

## HUNT SPECIFICALLY FOR
A. **Cross-document contradictions:** versions, item numbers, SHAs/md5s, board & store hashes,
   counts (11 writes / 90 blends / 115 sincerity rows), dates, and status (in-flight / done /
   queued) that disagree between any two documents or within one.
B. **Stale references:** any live (non-changelog) citation of a superseded doc version, an
   archived path, a retired rule, or a count a later ruling changed.
C. **§1b + R106.7 law coherence (the newest, least-tested surface — hunt hard):**
   - the K/G collapse across lines, and the item-284 DATA-ERROR rule (cross-class duals:
     K-DEF+G-FWD, K-FWD+G-DEF, RUC+G-FWD, RUC+G-DEF — flagged, single-position, no halt). Is it
     stated identically everywhere it appears? Is same-line K/G (the silent collapse) kept
     distinct from cross-class (the flag)?
   - "the more valuable bar" — is it defined as the LOWER replacement bar, and nothing else,
     EVERY place it appears (spec, directive, DECISIONS, HANDOVER)?
   - SEASON_PROG: exact formula, units, clamping, and season-start / season-end endpoints —
     defined unambiguously, or implementable two opposite ways?
   - R106.7 leg-blindness: is it stated so a builder wires BOTH projection and floor, with the
     year-1+ leg untouched and the banked/played component untouched?
   - present_position ∉ the collapsed eligibility set: is the flag-and-continue policy stated
     wherever the level-path-vs-bar relationship is described?
D. **The relay directive & the coming R106.7 build:** any instruction that could cause a FALSE
   HALT, any ambiguity a literal builder could implement two ways, any deliverable named in the
   handover/queue that the directive fails to require, and whether the FIRST-COMMANDS /
   stable-ID / site-from-the-code standing rules are actually present where a build will read
   them.
E. **Unmarked state:** anything the register records as DONE that a pack doc still lists open,
   or vice versa; any R106 ruling in the register but absent or mis-stated in DECISIONS v119;
   the four DEFERRED post-return checks (item 287) — are they carried forward intact as seat-11
   ACT 1?
F. **The re-seal cargo completeness (HANDOVER §2):** every ruling from items 250–288 that must
   land in CONSTRAINTS/acceptance — is each in the cargo? Name any omission. Cross-check the
   cargo against acceptance_v1_20.json and CONSTRAINTS_v1_18 directly: a rule the cargo will
   NOT cure that is ALSO stale in the JSON/prose is a HALT-grade gap.
G. **acceptance_v1_20.json specifically:** read the JSON against the R106 rulings. Any entry
   that contradicts a ruling and is not disclosed as queued-for-re-seal is a finding
   (e.g. a cap-only G-COHORT bound vs the two-sided 1.08–1.30 band; a pair-2 band ≠ ±15%;
   any surviving machine-selection field).

## FORMAT — NUMBERED FINDINGS, NOTHING ELSE
For each: [F#] SEVERITY (HALT-GRADE / CORRECTNESS / HYGIENE) · document + quoted text · what is
wrong · the correct state. No summaries, no compliments, no rewritten documents. If you verify a
category clean, one line: "Category X: no findings." False positives are acceptable; missed
defects are not — when unsure, FILE IT.
