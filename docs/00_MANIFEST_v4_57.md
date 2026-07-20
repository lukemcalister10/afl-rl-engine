# 00_MANIFEST — v4.57 · 2026-07-19 · supersedes v4.56 (same day)
### v4.57 (items 394–403): HANDOVER → **rev164**, DECISIONS → **v125** — the determinism saga RESOLVED
### by a strategic pivot (bake round-14 via the reproduction gate; the cross-machine determinism moves
### to pre-go-live, very likely a non-issue on a single environment) + the boot-identity fix + the
### go-live scope truth (the weekly store-WRITE was never built) + the BAKE + go-live STORE-WRITE now
### FIRING in parallel + a SEAT ROTATION (owner-called). THE OWNER'S TRUST IS BROKEN — HANDOVER §3/§4
### are mandatory before the incoming seat's first reply. Register → v376. CORE v2.8 + SSI v1.3 UNCHANGED.
### Prior v4.56: HANDOVER → rev163 (the determinism saga folded). Earlier: archive/CHANGELOG.
## THE PACK — CURRENT VERSIONS
| doc | version | tier | when to read |
|---|---|---|---|
| **00_MANIFEST** | **v4.57** | 0 | first, always |
| **CORE** | **v2.8** | 0 | in full — BINDING (v2.9 fold queued post-bake) |
| **HANDOVER** | **rev164** | 0 | THE ROTATION DOC — state · the in-flight bake+store-write · §3/§4 the trust+calibration mandate. |
| **DECISIONS** | **v125** | 0 | R108.x + the WAIVED viewing reads + the current to-dos. |
| **OPEN_ITEMS_REGISTER** | read its OWN header (≈v376 at this filing) | 1 | THE DURABLE LOG (items 380–403 = the saga + pivot). Repo-only. |
| CONSTRAINTS **v1.19** + **acceptance** | — | 1 | REPO-ONLY; assert the JSON. Acceptance v1_21 = DEFERRED post-bake housekeeping (reviews waived). |
| SPEC v1.4 · MEMO_LEGE v1.0 · **MEMO_LEGF v1.0–v1.3** | — | 1 | the construction docs of record. |
| **SINGLE_SOURCE_INVARIANT** | **v1.3** | 1 | before touching the store or a derived artifact. |
| **DIRECTIVE_BAKE_v2_11 · DIRECTIVE_STOREWRITE_weekly_apply** (2026-07-19) · GO_LIVE_round_score_ingestion | — | 1 | the ladder's live instruments (bake + store-write FIRING). |
**NEVER BULK-READ THE PACK. Context is a budget.**
## STATE AT v4.57
SHIPPED: **v2.10** = `d14efae` (canonical, owner-usable, untouched). v2.11 CANDIDATE STACK:
`15a9abd` (F5, #119) ← `540b62f` (F6, #121) ← `3055ea5` (env-pin, #123); **the BAKE builds on 3055ea5
(FIRING)** → tag-ready v2.11 head (owner tags + FF-promotes). Store `968de0c7` = **ROUND-14** (board of
record `06d8af60`; the bake ships the round-14 board — NOT round-19). IN FLIGHT (parallel): the bake +
the go-live STORE-WRITE (weekly apply; gated OFF). REMAINING toward the owner's product: store-write →
per-player rank TRACKING → single-env go-live wiring (rounds 15→19 one-by-one). NO promised clocks.
DO-NOT-MERGE: `fc7045d6` · `8b8ab7d` · `b854fbf` · the dispatch-pin branch. OWNER: LOW ON FABLE; TRUST
BROKEN — calibration mandate (HANDOVER §3). Rotate the seat at the next clean point (owner-called).
