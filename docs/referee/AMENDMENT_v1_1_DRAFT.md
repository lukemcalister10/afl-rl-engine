# REFEREE PROTOCOL AMENDMENT v1.0 → v1.1 — STREAM-AWARE PATHWAY/PICK SLICES · DRAFT, NOT IN FORCE
Pen-drafted 2026-07-26 under the sealed reads v437/v438/v439 (pathway structure) and the §10
freeze rules. The protocol at docs/referee/REFEREE_PROTOCOL.md remains FROZEN at v1.0 and is
untouched by this filing. This document is the exact wording awaiting the OWNER'S WORD, which
per the standing sequencing (v415, execution pack D3) lands AFTER the ITEM 411 D1 bake, so the
protocol never references store fields main does not yet carry. On the word, the pen applies
the edit below verbatim (the v400 twin-amendment execution pattern): one surgical replacement,
header version bump, ledger append. Amendments are owner-only; pre-round-0 the §10
next-round-effective and full-re-score clauses are vacuous (v408 reading) — this amendment is
free.

## MOTIVATION (appended verbatim to docs/referee/REFEREE_LEDGER.md on application)
The ITEM 411 restructure creates the two-stream world of record (owner reads R-STREAMS and
R-ERA, v408/v438): national-draft and rookie-draft picks are separate mechanisms, and pick
meaning is era-relative. The v1.0 slice vocabulary ("draft pick bands {1–5, 6–20, 21–40, 41+,
ND/SSP/other pathway}") bands raw blended picks and lumps every pathway into one bucket — it
measures a fiction once the store carries streams. This amendment makes the referee's
REPORTING see the same world the store now records. Slices are reporting bins only (§5.1);
no estimator, target, metric, fence, budget or bar changes. Filed pre-round-0; no result
exists that it could reverse.

## THE EXACT EDIT — §5.1, one clause replaced

REPLACE the clause (exact current text):

    draft pick bands {1–5, 6–20, 21–40, 41+, ND/SSP/other pathway};

WITH:

    pathway/pick slices (v1.1, stream-aware; source fields: the store's `draft_stream` and
    `stream_pick` — as-of-entry facts under the knowable-at-the-time edit law (ITEM 411
    charter, Amendment 2: `stream_pick` is the owner-ruled compressed continuous entrant
    order per year×stream, fixed at entry), hence origin-safe at every t ≥ entry by the same
    construction as drafted position): **ND-1–5 · ND-6–20 · ND-21–40 · ND-41–64** (draft_stream
    ND with stream_pick ≤ 64) · **POOL** (ND stream_pick ≥ 65, RD, and every other pathway not
    named here — post-draft academy, post-draft NGA, unregistered, Ireland, OTHER) · **SSP** ·
    **MSD** (the v439 observation lanes of record). Declared pooling parents under this
    section's support rule: ND bands → ND-ALL; SSP and MSD → POOL; POOL and ND-ALL →
    ALL-ENTRANTS. Pathway × drafted-position pairs follow the standard slice-pair support
    rule with the pathway member as the declared parent;

## APPLICATION CHECKLIST (pen executes on the word; all asserted, none assumed)
1. The current clause occurs EXACTLY ONCE in REFEREE_PROTOCOL.md — count-asserted before
   replacement; any other count is a STOP.
2. Header line gains: `· v1.1 (amendment 1 — stream-aware pathway/pick slices, owner word
   [DATE], register [vNNN])` and the version token `v1.0` in the title updates to `v1.1`.
3. REFEREE_LEDGER.md (append-only) gains the MOTIVATION block above verbatim plus the owner's
   word and register citation.
4. Nothing else changes — the seven-row position vocabulary, TALL-DEV, SUPPORT_MIN, targets,
   metrics, fences, and §2's feature list ("entry pathway and pick", a registry input, not a
   slice) are all untouched.
5. Post-edit assertions: the new clause occurs exactly once; the old clause occurs zero
   times; the file's section count is unchanged.

## DIALS SURFACED, NOT DECIDED (owner may rule either way at the word; the draft stands
without them)
- **RD sub-row (optional):** the sealed v438 shape pools rookie-drafted players into POOL.
  R-STREAMS names RD a separate mechanism, and RD is ~693 players — if the owner wants RD
  visible as its own OBSERVATION ROW inside POOL (reported, never separately priced), it is
  one added token (`· RD (observation row within POOL)`) with parent POOL. Unruled = omitted.
- **ND band edges:** drawn here to mirror the v1.0 bands with the tail closed at the
  published scale (41–64, per the v439 fixed 1–64 product ruling). The owner may word
  different edges; edges are reporting bins and carry no pricing meaning.

— supervisor pen, seam seat · draft only · the owner's word applies it, nothing else does
