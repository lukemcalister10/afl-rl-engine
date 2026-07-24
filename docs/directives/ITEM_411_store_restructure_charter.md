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


## AMENDMENT 1 · pen-filed 2026-07-24 (owner words, supervisor channel)
**Correction class clarified (owner: "it'd be a correction, not hindsight").** The pass contains
TWO edit classes: (a) CORRECTIONS to existing fields (picks, positions, player rows) — these DO
move the current board and lenses, deliberately; the guard is ATTRIBUTABILITY, not immobility:
at the bake, every board delta must trace to a manifest row, and ZERO unattributed movement is
the release assertion the owner views. (b) NEW stream fields — move nothing in the current world;
feed the panel, harness, and pricing rebuild. "Foundation-level change is the point" (owner):
wild shifts in draft-pick valuations or positional history are expected OUTPUTS of the rebuild
reading corrected truth — the manifest is what makes them auditable rather than mysterious.

**ITEM 411 EXECUTION SEAT (owner-directed).** A fresh GPT Sol instance stewards this job under
the standing Sol-family charter (docs/directives/SEAT_CHARTER_sol.md — all carve-outs apply:
no owner-word attestation, no self-review, CI never commits, seat-authored commits via Code
hands, signs as what it is). Scope: (1) direct Code hands to EXTRACT the current store to
spreadsheet form for the owner — one row per player, all authored fields, plus per-season
production, current value, games, age, pathway, and replacement-relevant aggregates so the owner
can prototype pricing experiments in the same workbook; read-only, no repo writes beyond the
exported artifact routed to the owner; (2) RECEIVE the owner's edited workbook, validate it
against this schema, and compile the CHANGE MANIFEST (player, field, old, new, reason) with a
population-impact report (percentile/replacement shifts from removals/additions); (3) PLAN the
post-408 bake: sequencing, assertions (manifest-attributability, stream-field inertness),
board-delta preview for the owner's viewing, protocol-amendment trigger. HARD FENCE: no store
byte moves until ITEM 408 merges and the owner words the restructure release; store AUTHORSHIP
is the owner's alone — the seat validates and stages, never edits content.

**Pricing experiments (owner read, sealed).** The owner will experiment with LOWERING REPLACEMENT
BARS and ADDING CONVEXITY around them. This is PRICING-LAYER design — the owner-ruled layer, the
carried named question (bars + production→SCAR mapping never directly validated) — and does NOT
touch the frozen forecast-core referee (no protocol amendment needed for it). Route: the owner
experiments in the extraction workbook; findings return as owner reads that seed the
pricing-layer design deliverable. His original ITEM 409 instinct (the floor is too convex against
solid non-elite players; +2 above replacement is not −10 below) is the sealed context.
