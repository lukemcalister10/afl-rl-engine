# AFL RL ENGINE — PACK MANIFEST — v4.8 · 2026-07-13 · supersedes v4.7
### STATUS: OFFICIAL. Canonical pack home = repo `docs/` (truth). Project knowledge = THE SEAM
### PACK (fast start) — owner-ruled 2026-07-13, superseding the Tier-0-only rule of v4.7. This
### manifest is a pointer card: NO operative content; on conflict its text yields to the role
### documents. Changelog: archive/CHANGELOG.

## THE SEAM-PACK RULE (owner-ruled 2026-07-13)
Rotation happens only at a SEAM, and at a seam the whole pack is rewritten — so the pack is
freshest exactly when a new seat needs it. Project knowledge therefore carries the SEAM PACK,
synced by the owner at each seam: **manifest · CORE · HANDOVER · DECISIONS · CONSTRAINTS +
acceptance JSON** (+ SINGLE_SOURCE_INVARIANT, which rarely changes). An incoming seat reads
those and is USEFUL IMMEDIATELY — no clone-and-read tax before it can think.
REPO-ONLY (never parked in Project knowledge — too fast-moving, guaranteed stale):
OPEN_ITEMS_REGISTER (the only list; moved 28× on 2026-07-12 alone) · verbatim returns · round
docs · the LTI sidecar · schemas.
THE FRESHNESS CHECK (mandatory, first act of every incoming seat — this is what makes the copies
safe): run the FULL-URL `ls-remote`, fetch the register's header + the docs/ file list, and
compare versions against the manifest just read. AGREE ⇒ proceed on the pre-loaded pack. DISAGREE
⇒ the repo wins, fetch what drifted, and TELL THE OWNER what was stale (the pack sync was missed).
A copy that is VERIFIED is a shortcut; a copy that is TRUSTED is the phantom-repo scare.
BUILD SEATS: always fetch from the repo — never owner attachments (the standing directive line).

## PRECEDENCE (higher wins on conflict)
1. The owner's word · 2. CONSTRAINTS + acceptance JSON · 3. CORE · 4. HANDOVER · 5. DECISIONS ·
6. OPEN_ITEMS_REGISTER (the only list) · 7. Job-scoped directives · 8. Reference docs.
Between pack filings, the newest supervisor-issued version of a doc governs over the repo copy.

## TIER 0 — hold in full; home = Project knowledge AND repo docs/
| role | file |
|---|---|
| Manifest | 00_MANIFEST_v4.7.md (this file) |
| Core doctrine + conventions | CORE_v2.3.md |

## TIER 1 — read to operate (supervisor seats); home = repo docs/ — FETCH, don't cache
| role | current file |
|---|---|
| State + the action order | HANDOVER_rev133_2026-07-13.md |
| Rulings tracker + owner to-dos | DECISIONS_v96_2026-07-13.md |
| OPEN ITEMS (the only list) | OPEN_ITEMS_REGISTER.md (v35 at this filing; supervisor-maintained) |
| Constraints registry | CONSTRAINTS_v1.7.md + acceptance_v1.7.json (v1.8 folds at the v2.9 seam: numéraire re-quotes · A-FADE three · cycle law · G-Y0 status · the B1 code-vs-prose conformance) |
| Wave synthesis (live) | SYNTHESIS_fable_wave_2026-07-12.md |

## TIER 2 — round docs (archive at round close)
The v2.9 candidate PR #67 + its committed FINDINGS · the go-live runbook
(docs/GO_LIVE_round_score_ingestion.md) · STANDING_DIRECTIVE_pack_filing_v1.md.

## TIER 3 — reference on demand; home = repo docs/
Single-source invariant (SINGLE_SOURCE_INVARIANT_v1.2.md) · verbatim returns (docs/returns/) ·
the LTI register SIDECAR (repo-homed `LTI_REGISTER.md` — canonical; the 2026-07-02 file is its
pre-sidecar ancestor, ARCHIVE, do not read as current) · pick_semantics_schema.md.

## SEED / READ ORDER (new supervisor seat)
Manifest + CORE (Project knowledge) → fresh clone, verify main + tag SHAs live → docs/ HANDOVER
→ DECISIONS → OPEN_ITEMS_REGISTER → the rest on demand. Do not bulk-read the pack.

## STANDING DOC RULES
Versions resolve only here · constraint content only in CONSTRAINTS · one pen + same-turn
present_files · REPO IS HOME (docs reach the repo via pack-filing builds or the supervisor's
docs/-only token pen, SHA cited same turn) · PROJECT KNOWLEDGE = TIER-0 ONLY: a Tier-1+ copy
parked there is a STALE-COPY HAZARD (the one disease this project keeps re-learning) — fetch
from the repo instead · verbatim returns to docs/returns/ (WD-2) · doc jobs pin their base ·
every directive carries the FULL-URL ls-remote base-verification line.
