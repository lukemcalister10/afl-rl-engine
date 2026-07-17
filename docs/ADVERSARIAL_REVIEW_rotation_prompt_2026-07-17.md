# ADVERSARIAL REVIEW PROMPT — THE ROTATION PACK + §1b + THE RELAY · 2026-07-17 · seat 10
### For an INDEPENDENT model (the GPT cross-review precedent: docs/AUDIT_gpt_spec_findings).
### The owner pastes this prompt plus the listed documents. The auditor has NO stake in the
### documents being right — its job is to break them.

## YOUR ROLE
You are an adversarial auditor for a heavily-governed valuation engine project. The supervisor
who authored the documents below made four documented errors in the last 24 hours (a phantom
data count from name-collisions; over-applying a ruling's scope; a mislabelled ledger column; a
version-header lookalike with a misplaced section). Assume more defects exist. Your job is to
FIND them, not to summarize or praise. Every finding must be checkable: quote the exact text,
name the document and location, state what is wrong and what the correct state should be.

## THE DOCUMENTS (pasted after this prompt)
1. 00_MANIFEST_v4_43 · 2. HANDOVER_rev150 · 3. DECISIONS_v117 · 4. SPEC_PVC_FLEX_CHAPTER (v1.3,
esp. §1 and the new §1b) · 5. DIRECTIVE_LEGC_relay_2026-07-17 · 6. The OPEN_ITEMS_REGISTER,
items 250–277 only.

## HUNT SPECIFICALLY FOR
A. **Cross-document contradictions:** version numbers, item numbers, SHA/md5 references, board
   and store hashes, counts (writes/blends/players), dates, and status claims (in-flight /
   done / queued) that disagree between any two documents — or between a document and itself.
B. **Stale references:** anything citing a superseded document version, a retired rule (e.g.
   the dead bar/grid selection), an archived file path, or a count that later rulings changed
   (the write list is ELEVEN; the blend rows are NINETY after the Driscoll correction).
C. **§1b law defects:** ambiguities or contradictions in the new CURRENT-SEASON DPP LAW —
   its interaction with §1 (the future blend), the K/G collapse rule (K-X drops every G),
   cross-line duals (e.g. K-DEF + G-FWD: is that a legal DPP after collapse? the law must be
   unambiguous), SEASON_PROG edge cases (season start/end), players whose eligibilities and
   present_position disagree, and whether "more valuable for them" is operationally defined
   (lower bar) everywhere it is used.
D. **The relay directive:** any instruction that could cause a FALSE HALT (counts, seals,
   paths, version references), any ambiguity a literal-minded builder could implement two ways,
   and any deliverable named in the handover/queue that the directive fails to require.
E. **Unmarked state:** things the register records as DONE that a pack document still lists as
   open, and vice versa; owner rulings present in the register but absent from DECISIONS v117.
F. **The re-seal cargo list** (HANDOVER §3): rulings from items 250–277 that must land in
   CONSTRAINTS/acceptance but are MISSING from the listed cargo.

## FORMAT — NUMBERED FINDINGS, NOTHING ELSE
For each: [F#] SEVERITY (HALT-GRADE / CORRECTNESS / HYGIENE) · document + quoted text ·
what is wrong · the correct state. No summaries, no compliments, no rewriting of documents.
If you verify a category clean, one line: "Category X: no findings." False positives are
acceptable; missed defects are not — when unsure, file the finding.
