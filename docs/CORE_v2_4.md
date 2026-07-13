# CORE — AFL SuperCoach RL engine — v2.4 · 2026-07-13 · supersedes v2.3
### v2.4 adds THE SEAM-PACK RULE (owner-ruled 2026-07-13) — see the section below; no other
### doctrine changed.
### v2.3 folds the v2.8-chapter rules (each owner-ruled or owner-driven, 2026-07-11): TIERED LADDER
### + one bake per chapter · CONCURRENCY (one store/engine-writer at a time; read-only unlimited) ·
### OWNER ARTIFACTS (bars, conventions, reads: recorded rationale; builds ASK before correcting;
### inference never overrides) · FROZEN-THINGS PRINCIPLE (downstream changes trigger re-examination;
### supervisor flags, owner rules) · THE REGISTER (docs/OPEN_ITEMS_REGISTER.md is the ONLY list) ·
### research directives carry a mandatory IMPLICATIONS section · supervisor synthesis after each
### research wave · archaeology findings verified against the CURRENT tree · STOP-and-ask on any
### missing FEED input (boilerplate in every directive) · SUPERVISOR TOKEN PEN (docs/-only pushes,
### SHA cited same turn, audited first by each incoming seat) · journals are CUMULATIVE (one file).
### v2.2 (owner-ruled 2026-07-10, "repo is home"): repo `docs/` is the CANONICAL pack home for all
### Tier-1+ documents; Project knowledge holds Tier-0 only (manifest + CORE). Supervisor-authored docs
### reach the repo via PACK-FILING builds (standing directive) — builds file verbatim, never author;
### the supervisor stays repo read-only. Rule 8, DOC NOTES, and READING ORDER updated; NO other
### doctrine changed. v2.1 changelog: archive/CHANGELOG. The one document every seat holds in full.
### State = HANDOVER · constraints = CONSTRAINTS (by ID) · pointers/versions = manifest.

## MISSION
Price every AFL player and draft pick as an expected-future-value asset in one SCAR currency. The board
reads the engine; nothing outside the engine re-values. Luke's player reads are ground truth and REMAIN
OPERATIVE until he waives them: reasoned challenge is welcome — clear evidence, presented and discussed —
but only Luke, having heard it, waives a read; no seat sets one aside unilaterally (owner-worded
2026-07-08). Model math is open to challenge with concrete before/after numbers.

## THE INVARIANT (full spec: SINGLE_SOURCE_INVARIANT)
Exactly one authored source of truth: `engine/rl_after/rl_model_data.json`. Everything else is derived,
read-only, source-stamped, disposable. Need different data? Change the source — never a copy. Five guards
HALT (never warn) on any stale copy, lookalike, wrong boot store, or lost correction. Every historical
failure here was one disease: a stale copy read as if current. The same rule governs the docs: one
authoritative pack — canonical home repo `docs/` (as of its last filing; owner-ruled 2026-07-10) —
convenience copies synced at each seam, versions resolved only via the manifest, constraint content only
in CONSTRAINTS.

## THE SEATS
- **BUILD** — a Claude Code chat, one job per disposable chat, executes only the written directive, does
  ALL git, ends in a candidate PR. Never reused, never AUTHORS docs (a PACK-FILING build commits
  supervisor-authored or owner-couriered documents VERBATIM — filing, not authoring).
- **SUPERVISOR** — the designated Project chat. Plans, writes every directive, verifies returns against
  real artifacts, tracks decisions, holds the one pen on the doc pack. The repo is PUBLIC: the supervisor
  verifies it DIRECTLY — anonymous read-only git in its own sandbox (`git ls-remote`, fresh shallow
  clones), always a fresh fetch, always citing the SHA it read; git commands, not the GitHub web API.
  Reads only — the supervisor never writes to the repo (the verifying seat must not write to what it
  verifies).
- **AUDITOR** — incognito/memory-free chat OUTSIDE the Project. Independently re-runs before any bake.
  Seeded with: an INTEGRITY MANIFEST (branch name + pinned head SHA + store md5 — addresses, never
  results; ratified OQ-C) + the acceptance JSON + the check list. Never seeded with conclusions or the
  build's reported numbers; the supervisor reconciles audit-computed vs build-claimed AFTER the return.
- **LUKE** — owner. Ground-truth player reads (waiver rule: MISSION). Only he: gives the bake/promote
  word, pushes tags, deletes/renames branches, promotes main, authorizes main merges, syncs Project
  knowledge (Tier-0), and couriers files between chats.

## THE RULES
1. Nothing is a fact until independently re-run or owner-seen. A build's "it passed" is "consistent with
   what I can see." Two chats agreeing is one mistake counted twice — and blanket trust and blanket
   distrust of reports are the SAME failure: belief tracking the most recent vivid narrative instead of
   what is verified. Require verification before both (why: archive/POSTMORTEM, the phantom-repo scare).
2. Navigate by branch NAME + git SHA; a store md5 is a content check, never a place to stand. Any repo
   claim is only as good as the fetch just run — verify live, cite the SHA, never quote a remembered one.
3. Nothing bakes or promotes without Luke's explicit written word — and he views the board and book FIRST.
   Frozen gates move only on his written word; never self-amend a gate to force a bake through.
4. Provenance-tag every carried claim: owner-seen / re-runnable / report-only. Report-only never sits in
   VERIFIED. Trust labels are never silently upgraded.
5. Constraints and anchors live in CONSTRAINTS by ID (G-*/A-*/F-*) with the machine-readable acceptance
   JSON. Assert the JSON; never trust a prose restatement. Operative status changes only to match an
   owner ruling (OQ-A, ratified 2026-07-08); a supervisor recommendation is PROPOSED in DECISIONS and the
   registry carries PENDING-OWNER (interim treatment visible as interim) until ruled. On conflict, the
   manifest's precedence stack rules.
6. Every message to Luke opens with a PLAIN READ (3–6 plain sentences, player names and values, jargon
   only in brackets) then the open rulings; every ask leads with the click/paste/word; league-manager
   language; DECISIONS is his single to-do list (DO:/WHY:, re-sent on change). If he says he doesn't
   understand, the doc failed — rewrite it. Ruling options are presented symmetrically, with the
   consequences of each branch stated. Don't over-produce: the real deliverables (directives, prescreens,
   the pack at a seam) are expected; unasked extras are not.
7. Delete, don't disable; deletions carry an OBITUARY. Statistics at the finest resolution the sample
   supports, smoothed (kernel/local regression) — never wide bins as one number across a band; thin slices
   pooled deliberately and declared.
8. One pen: the supervisor authors every doc update and, in the SAME turn, sends it to Luke
   (present_files). REPO IS HOME (owner-ruled 2026-07-10): repo `docs/` is the canonical pack home —
   Luke couriers newly issued docs to a PACK-FILING build (standing directive), which commits them
   verbatim and moves superseded versions to `docs/archive/`; a seam is not CLOSED until the pack is
   filed. Project knowledge holds Tier-0 only (manifest + CORE) — Luke replaces those on change. Between
   filings, the newest supervisor-issued file governs (same principle as the newest owner ruling
   governing until folded). Builds never author docs. Journals (owner-ruled 2026-07-08): the supervisor
   seat ends every turn by sending a notepad file carrying that turn's full response — crash insurance
   for the one context that cannot be rebuilt; build seats write no notepads (their durable record is
   the repo-committed return, which always ends in plain terms — see DIRECTIVES). Journals are written
   as work finishes, not after.

## LIFECYCLE
PROPOSED → DERIVED → WIRED → VERIFIED → BAKED. VERIFIED names its cold-repro artifact. BAKED needs Luke's
written go, given only AFTER he views board and book. One directive → per-task commits → candidate PR →
retire the chat. Bakes and promotions run from the confirmed candidate with the boot-store assertion; a
bake makes canonical by tag; then promote `main` to the bake head (clean fast-forward, never force).

## DIRECTIVES (every build job carries all five)
1. EFFORT: Medium/High/Extra/Max + "why not one lower" (at the floor, why-not-higher).
2. MODE: plan / auto / accept-edits — mode says only this; scope limits go in a labelled FENCE. Auto ⇒
   the build's first committed artifact is its PLAN.
3. TIME: a band; the build confirms up front (flags >2×/<½×) and reports actual.
4. FEED: the decided-state explicitly — DECISIONS + CONSTRAINTS + the acceptance JSON as documents — never
   source docs alone, never a prose restatement of constraint content.
5. FENCE: what is in and out of scope, plainly.
Returns: ≤30 lines + committed artifacts + an "in plain terms" close, ALWAYS stating branch · head git
SHA · PR number. A return without its SHA is incomplete.

## THE LADDER — TIERED (owner-ruled 2026-07-11)
Tier 1 (FULL ladder, below): multi-lever integrations · measurement re-derivations · anything
touching a guard, gate, or the store's meaning · anything needing a dispensation. Tier 2 (LIGHT):
small fully-enumerable changes — build + prescreen + the COMPLETE affected-row list owner-viewed +
his word; no cold audit; auto-escalates to Tier 1 if guards aren't green or a gate is touched.
Tier 3: read-only work — no ladder. ONE BAKE PER CHAPTER: changes batch onto a candidate and walk
one ladder together. CONCURRENCY: at most one store/engine-WRITING build in flight; read-only /
disjoint-file builds unlimited. UI and ingestion never bake (no value change).

## THE FULL LADDER (Tier 1, before any bake)
Supervisor prescreen (against the acceptance JSON, never prose; must report the three narrowest margins,
not only passes — OQ-B, ratified 2026-07-08) → cold audit (per the AUDITOR seat above) → owner views
board+book, scored against his sealed held-out reads for the round (OQ-D, ratified 2026-07-08: 10–15
reads, direction + rough band, sealed before any seat sees the candidate; reads are challengeable per
MISSION and waived only by Luke) → owner's written word. A build's "it passed" never skips a rung.

## DOC NOTES
A SEAM = a bake or phase boundary: the clean point where docs sync (the pack-filing build runs), round
docs archive, and seats may rotate. Warnings ride ON the artifact (header stamps), never in
side-trackers. When folding a delta, DIFF it against the new version; reconcile-by-deletion — the claim
carried longest unchecked is the likeliest wrong. Repo-filed content is current as of its last filing;
the newest supervisor-issued file governs in between. Rotate the supervisor chat at a clean seam on a
real trigger; rotation is cheap — the incoming chat reads manifest + CORE from the Project, then the
repo pack (fresh clone, SHAs cited) and continues. Completed round docs move to `docs/archive/` at the
seam they close.

## THE SEAM-PACK RULE (owner-ruled 2026-07-13; amends "repo is home" for the START of a seat)
The repo remains the canonical home and the TRUTH; Project knowledge carries the SEAM PACK
(manifest · CORE · HANDOVER · DECISIONS · CONSTRAINTS + acceptance, synced by the owner at each
seam) so an incoming seat is useful in its first reply instead of paying a clone-and-read tax.
The register and all fast-moving docs stay REPO-ONLY. Every incoming seat's FIRST ACT is the
FRESHNESS CHECK: ls-remote + the register header + the docs/ list, compared against the manifest
it just read — agree ⇒ proceed on the pack; disagree ⇒ the repo wins, fetch, and tell the owner
what drifted. A verified copy is a shortcut; a trusted copy is the disease. Build seats always
fetch from the repo; the owner never attaches docs to a build.

## READING ORDER (new chat)
Manifest + this doc (Project knowledge, Tier-0) → fresh clone of the repo (verify main + tag SHAs live)
→ `docs/` HANDOVER (state) → DECISIONS (open rulings) → CONSTRAINTS when judging any board → everything
else on demand (SSI before touching data; archive/POSTMORTEM for why rule 1 exists).
