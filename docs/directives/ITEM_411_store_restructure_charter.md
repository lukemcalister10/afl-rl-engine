# STORE RESTRUCTURE — ITEM 411 CHARTER (PREP PHASE) · pen-filed 2026-07-24 · owner-directed
Status: PREPARATION ONLY. No store byte moves until ITEM 408 merges; the restructure then lands as
its own owner release through the item-5 atomic bake machinery. The owner authors the store (Law 1:
the ONE SOURCE is the single authored artifact); this charter exists so his edit pass, the panel
builder, the protocol amendment, and the pricing rebuild all agree the first time.

## OWNER READS OF RECORD (sealed, 2026-07-24, supervisor channel)
- **R-STREAMS:** The rookie draft and national draft are separate mechanisms and must be valued as
  separate streams; the historical blend let rookie picks needlessly prop up the ND tail.
- **R-ERA:** Draft-pick meaning is era-relative — the ND (and RD) have shortened over time as SSP
  and MSD created new league-entry pathways; pick 60 fifteen years ago is not pick 60 today. Pick
  lenses must be able to read pick-in-era context, not raw pick number alone.
(These reconcile with the ITEM 409 curve-tail triangle: the owner's late-ND-picks-overpriced
instinct now carries a mechanism — a blended tail population plus era drift.)

## ADDITIVE SCHEMA (new fields; existing fields UNTOUCHED so the current world provably doesn't move)
Per player:
- `draft_stream` ∈ {ND, RD, SSP, MSD, PRE_AFL_ERA, OTHER} — the mechanism that brought the player in.
- `stream_pick` — pick number WITHIN that stream's draft that year; null for non-drafted pathways.
- `stream_year` — the entry year the stream_pick refers to (usually = entry year; explicit anyway).
- `pick_correction_note` — nullable; REQUIRED on any player whose historical pick/position/identity
  the owner corrects (see edit law below).
Per year (small reference table, since drafted-never-played players are absent from the store and
draft sizes are therefore NOT derivable): `nd_total_picks`, `rd_total_picks` by season — what R-ERA
needs for pick-percentile-within-year lenses.
Existing blended fields remain byte-identical: the current engine, board, frozen curve, and the
incumbent contestant keep reading them unchanged.

## THE EDIT LAW — KNOWABLE-AT-THE-TIME (binding on the whole pass)
Corrections restore what was TRUE AND KNOWABLE AT THE TIME; they never encode hindsight. Fixing a
recording error (the pick was actually 23, not 32; he was listed KEY-DEF on draft night) is a
correction. Re-classifying a historical position or pick because of how the career TURNED OUT is
retrospective revision — exactly the indirect-leakage route the frozen referee's origin-safety
fences name — and is barred from historical fields. Where the owner wants an outcome-informed
view, it belongs in a NEW, dated field, never overwriting the historical one.

## ONE DECLARED PASS + CHANGE MANIFEST
All edits (stream fields, pick corrections, position corrections, player removals/additions, and —
owner's option — the ITEM 409 store-hygiene trio) land as ONE declared edit pass with a CHANGE
MANIFEST: one row per edit — player, field, old, new, reason, source. The manifest files beside
the release; it is what lets the referee treat the corrected store as clean rather than suspect,
and what the blind reviewer audits instead of diffing blind.

## REMOVALS — population warning
Standings, replacement bars, and percentile metrics are computed AGAINST THE POPULATION. Deleting
players changes every percentile around them. Remove only true errors (duplicates, phantom rows);
for "shouldn't count" players prefer a flagged exclusion field with a reason, which lenses can
honor without rewriting history. Additions carry the same manifest discipline.

## SEQUENCED CONSEQUENCES (all post-408, in order)
1. Owner edits the store against this schema; manifest accompanies. 2. The restructure release:
atomic bake via item-5 machinery, board provably unmoved on the blended fields (asserted, not
assumed), owner views the assertion evidence. 3. Protocol amendment v1.1 (owner-worded, drafted by
a design seat): stream-aware pathway/pick-band slices + R-ERA context availability to candidates —
cheap while nothing is scored, priced in re-scoring after round 0. 4. Panel builder and harness
read the stream fields from day one. 5. The pricing-layer rebuild (charter §4) prices the two
streams as separate entrant distributions — R-STREAMS lands there natively.
