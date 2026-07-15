# CORE — AFL SuperCoach RL engine — v2.7 · 2026-07-15 · supersedes v2.6
### v2.7 (same day): ONE state change — SSI MOVED root → docs/ on the owner's word ("Agree on move SSI",
### 2026-07-15). The fence exception item 85 anticipated is closed permanently. Filename unchanged, content
### unchanged, the version stays in the file's header. Location references updated; nothing else moved.
### v2.6 FOLDS THE R98/R100 PROCESS RULINGS. No doctrine reversed; ONE ORDER corrected:
### (1) THE PEN, SUSPENDED AND RESTORED — recorded together so no future seat reads a flip-flop:
###     R98.8 (owner, 2026-07-14) screened every pack-doc push for seat 5 specifically ("Do not update
###     documentation directly to git, send it to me for screening first"; the REGISTER stayed
###     pen-pushed). R98.9 closed it at the seam; R99.3 reworded the expiry — it expires WHEN FABLE
###     SITS (seat 5's rationale outlived seat 5's rotation to seat 6, another Opus). The docs/-only
###     TOKEN PEN is RESTORED, unscreened, from the Fable seat's first turn.
### (2) THE HANDOVER EXCEPTION (R98.10) + THE CORRECTED ORDER (R100.10, owner-ruled "Yes, check
###     first."): the incoming seat runs the FRESHNESS CHECK FIRST and only then files the pack it was
###     handed. rev136 and manifest v4.16 wrote "file first, then check" — a guard that runs AFTER the
###     thing it guards cannot fire. R98.10's SUBSTANCE is unchanged; only the order moved. Full text
###     in THE SEAM-PACK RULE below.
### (3) SSI LOCATION (closed at v2.7): queued at v2.6 on the owner's word; word GIVEN 2026-07-15 and the
###     move DONE — SSI lives at docs/SINGLE_SOURCE_INVARIANT.md.
### v2.5 closed the v2.9 seam (SPEED RULES S1–S6 · SILENCE IS A RED · THE BASE-PIN RULE · THE POSITION
### TAXONOMY · SSI file note · M1/F11 OBITUARY). v2.4 added THE SEAM-PACK RULE. v2.3 folded the
### v2.8-chapter rules (tiered ladder · concurrency · the register · token pen · journals). v2.2
### (owner-ruled 2026-07-10): "repo is home." Earlier changelogs: archive/CHANGELOG.
### The one document every seat holds in full.
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
**FILE NOTE (v2.7):** the invariant lives at `docs/SINGLE_SOURCE_INVARIANT.md` (moved from repo ROOT
2026-07-15, owner-worded) — the FILENAME carries no version; the VERSION lives in the file's header (v1.3).
Do not create a versioned duplicate filename — that would be a lookalike of the very document that forbids
lookalikes.

## THE SEATS
- **BUILD** — a Claude Code chat, one job per disposable chat, executes only the written directive, does
  ALL git, ends in a candidate PR. Never reused, never AUTHORS docs (a PACK-FILING build commits
  supervisor-authored or owner-couriered documents VERBATIM — filing, not authoring).
- **SUPERVISOR** — the designated Project chat. Plans, writes every directive, verifies returns against
  real artifacts, tracks decisions, holds the one pen on the doc pack. The repo is PUBLIC: the supervisor
  verifies it DIRECTLY — anonymous read-only git in its own sandbox (`git ls-remote`, fresh shallow
  clones), always a fresh fetch, always citing the SHA it read; git commands, not the GitHub web API.
  The supervisor's WRITE access is the TOKEN PEN and it is **docs/-only**: every push docs/-only, the SHA
  cited in the same turn, audited first by each incoming seat. The verifying seat never writes to what it
  verifies — engine, store, board, gates and artifacts are a BUILD's to write, never the supervisor's.
- **AUDITOR** — incognito/memory-free chat OUTSIDE the Project. Independently re-runs before any bake.
  Seeded with: an INTEGRITY MANIFEST (branch name + pinned head SHA + store md5 — addresses, never
  results; ratified OQ-C) + the acceptance JSON + the check list. Never seeded with conclusions or the
  build's reported numbers; the supervisor reconciles audit-computed vs build-claimed AFTER the return.
- **LUKE** — owner. Ground-truth player reads (waiver rule: MISSION). Only he: gives the bake/promote
  word, pushes tags, deletes/renames branches, promotes main, authorizes main merges, syncs Project
  knowledge (the seam pack), and couriers files between chats.

## THE RULES
1. Nothing is a fact until independently re-run or owner-seen. A build's "it passed" is "consistent with
   what I can see." Two chats agreeing is one mistake counted twice — and blanket trust and blanket
   distrust of reports are the SAME failure: belief tracking the most recent vivid narrative instead of
   what is verified. Require verification before both (why: archive/POSTMORTEM, the phantom-repo scare).
   **SILENCE IS A RED (v2.5).** A check that produces NO result — it crashed, its input was missing, it
   returned `None`, its output was swallowed by a pipe — has FAILED. It has not passed. Every gate,
   guard, and assertion must produce a verdict or HALT, and every harness must propagate a non-zero exit;
   never pipe a check through `tail`/`head` without checking its exit code. (Why: on 2026-07-13 a BINDING
   gate raised an exception behind a `| tail -8`, printed nothing, and the suite reported PASS. The
   number in the return had been carried from an older note. Halt-not-warn applies to the GATE, not only
   to its verdict.)
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
   the supervisor's docs/-only TOKEN PEN files it directly (SHA cited same turn), or Luke couriers newly
   issued docs to a PACK-FILING build, which commits them verbatim and moves superseded versions to
   `docs/archive/`; a seam is not CLOSED until the pack is filed. Project knowledge holds THE SEAM PACK —
   Luke syncs it on change. Between filings, the newest supervisor-issued file governs. Builds never
   author docs. Journals (owner-ruled 2026-07-08): the supervisor seat ends every turn by sending a
   notepad file carrying that turn's full response — crash insurance for the one context that cannot be
   rebuilt; build seats write no notepads (their durable record is the repo-committed return). Journals
   are written as work finishes, not after.

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
**THE BASE PIN (v2.5).** Every directive carries a FULL-URL `ls-remote` base-verification line. While the
supervisor's docs pen is live, main MOVES between a directive being written and being pasted — often with
the very commit that ANNOUNCES the job. So a base pin reads: **"main AT OR AFTER `<SHA>`, and
`git diff --name-only <SHA>..main` must be `docs/`-ONLY"** — never strict SHA equality. Strict equality is
correct only for a store/engine base. A tag-pinned job is immune by construction. (Why: on 2026-07-13 a
build correctly HALTED on a base drift that was nothing but the supervisor's own register push.)
Returns: ≤30 lines + committed artifacts + an "in plain terms" close, ALWAYS stating branch · head git
SHA · PR number. A return without its SHA is incomplete.

## THE SPEED RULES (S1–S6) — owner-ruled 2026-07-13; OPERATIVE in every directive
No quality trade: validation coverage, gate breadth and artifact verification are untouched.
- **S1. HASH-CACHED EXPENSIVE ARTIFACTS.** Deterministic compute (gate matrices, walk-forward books,
  boards) is stamped with the md5 of every input that determines it (store + engine code + config). Every
  consumer FIRST asserts stamp == current inputs: match ⇒ reuse; mismatch ⇒ recompute and restamp. Same
  logic as SSI Guard 2, pointed at compute. A stale-stamp reuse is a build defect.
- **S2. ONE JOB PER CHAT, FENCE-ENFORCED.** Fences are sized so the chat finishes inside its token budget
  with a clean RETURN — never a checkpoint apology. Mid-flight scope growth goes to a NEW directive and a
  NEW chat, never appended.
- **S3. PARALLEL-ANALYSIS DEFAULT.** Read-only jobs (SPECs, investigations, audits, measurements) run
  ALONGSIDE the single store/engine writer, never queued behind it. Concurrency already permits this; S3
  makes it the default, not the exception.
- **S4. FROZEN-SUITE-ONLY MEASUREMENT** (boilerplate in every directive): gates and guards are measured
  with the FROZEN repo suite only. Ad-hoc constructions are FINDINGS to report, never verdicts to act on.
- **S5. THE STANDING CERT HARNESS.** Certification tooling is committed and reused (grown toward
  one-command certify), never rebuilt per chat.
- **S6. AUDIT-SIZING** (owner-raised after the S1/S2 shard strain): incognito audit shards are sized to
  finish inside ONE tool-use window. Long computes run backgrounded with completion markers and SPARSE
  polling (few tool calls); anything heavier than one background compute is either split further or
  verified-by-stamp instead of recomputed.
**REFUSED LEVERS** (recorded so no future seat "optimises" into them): fewer validation passes · trusting
reported numbers · thinner gate coverage. Exhibit A: the v2.8 panel claim-accuracy defect.

## THE POSITION TAXONOMY (stated in CORE because a previous seat got it wrong, and it DRIVES the pricing)
The DPP weighted blend is DELETED (2026-07-05). The store carries THREE clean single-valued columns:
- **`drafted_position`** — the career/draft position. **It DRIVES THE COHORT CURVES** (the engine's
  internal `p['pos']`; `rl_model.py`: `_p['pos'] = _p['drafted_position']`). Verified against the tree,
  2026-07-13.
- **`present_position`** — the player's CURRENT position; the YEAR-0 leg of his own valuation.
- **`future_position`** — his SETTLED FUTURE position; the YEARS-1+ leg, and the curve / peak / runway.
Pricing reads `present_position` for the year-0 replacement bar and `future_position` for the years-1+
bar and the peak/curve. Never infer one from another; never re-introduce a probabilistic leg.

## THE LADDER — TIERED (owner-ruled 2026-07-11)
Tier 1 (FULL ladder, below): multi-lever integrations · measurement re-derivations · anything
touching a guard, gate, or the store's meaning · anything needing a dispensation. Tier 2 (LIGHT):
small fully-enumerable changes — build + prescreen + the COMPLETE affected-row list owner-viewed +
his word; no cold audit; auto-escalates to Tier 1 if guards aren't green or a gate is touched.
Tier 3: read-only work — no ladder. ONE BAKE PER CHAPTER: changes batch onto a candidate and walk
one ladder together. CONCURRENCY: at most one store/engine-WRITING build in flight; read-only /
disjoint-file builds unlimited. UI and ingestion never bake (no value change).
**TIER-1-LITE** (owner-ruled 2026-07-13, for a gate change that moves NO player value): supervisor
prescreen + the job's own red-path proofs + the owner's written word; no cold audit and no board view —
the rung is empty by construction. Record WHY it was empty, so a later seat does not read it as a rung
skipped.

## THE FULL LADDER (Tier 1, before any bake)
Supervisor prescreen (against the acceptance JSON, never prose; must report the three narrowest margins,
not only passes — OQ-B, ratified 2026-07-08) → cold audit (per the AUDITOR seat above) → owner views
board+book, scored against his sealed held-out reads for the round (OQ-D, ratified 2026-07-08: 10–15
reads, direction + rough band, sealed before any seat sees the candidate; reads are challengeable per
MISSION and waived only by Luke) → owner's written word. A build's "it passed" never skips a rung.

## DOC NOTES
A SEAM = a bake or phase boundary: the clean point where docs sync, round docs archive, and seats may
rotate. Warnings ride ON the artifact (header stamps), never in side-trackers. When folding a delta, DIFF
it against the new version; reconcile-by-deletion — the claim carried longest unchecked is the likeliest
wrong. Repo-filed content is current as of its last filing; the newest supervisor-issued file governs in
between. Rotate the supervisor chat at a clean seam on a real trigger; rotation is cheap — the incoming
chat reads the seam pack, runs the FRESHNESS CHECK, then the repo pack (fresh clone, SHAs cited) and
continues. Completed round docs move to `docs/archive/` at the seam they close.
**M1 / F11 — OBITUARY (v2.5).** The gate-legend "queued fix items" M1 and F11, carried in the docs since
before seat 3, were verified against the CURRENT tree on 2026-07-13: they exist in **no gate and no
code** — only in prose (ROADMAP v9, HANDOVER, archives). They were doc ghosts. RETIRED. Do not chase
them; do not resurrect them.

## THE SEAM-PACK RULE (owner-ruled 2026-07-13)
The repo remains the canonical home and the TRUTH; Project knowledge carries the SEAM PACK
(manifest · CORE · HANDOVER · DECISIONS · CONSTRAINTS + acceptance + SSI, synced by the owner at each
seam) so an incoming seat is useful in its first reply instead of paying a clone-and-read tax.
The register and all fast-moving docs stay REPO-ONLY. Every incoming seat's FIRST TWO ACTS, IN THIS ORDER
(R100.10, owner-ruled 2026-07-14, "Yes, check first."):
**ACT 1 — THE FRESHNESS CHECK:** full-URL ls-remote + the register header + the docs/ list, and the handed
pack compared against the repo DOC BY DOC, BY HEADER VERSION. **ACT 2 — FILE THE PACK IT WAS HANDED**
(R98.10, owner-worded: "on disagreement, the repo wins, OTHER THAN at seat handover. The supervisor should
file the pack they receive to the repo, and then keep it updated in the repo."), archiving superseded
versions to docs/archive/. **A guard that runs after the thing it guards cannot fire — the check comes
first, always.** **DIRECTIONAL GUARD (BINDING):** pack ahead or equal on every doc ⇒ file and proceed;
pack BEHIND on ANY doc ⇒ HALT and tell the owner — filing a stale pack writes old docs over newer ones,
the stale-copy disease itself. The exception expires the moment the pack is filed; thereafter the repo is
home and wins on any disagreement, as before. A verified copy is a shortcut; a trusted copy is the disease. Build seats always
fetch from the repo; the owner never attaches docs to a build (the ONE exception is a PACK-FILING
build, which exists precisely to commit documents that are not yet in the repo).

## READING ORDER (new chat)
Manifest + this doc (Project knowledge, Tier-0) → THE FRESHNESS CHECK (fresh clone; verify main + tag
SHAs live) → FILE THE HANDED PACK (ahead-or-equal ⇒ file; BEHIND on ANY doc ⇒ HALT — R98.10/R100.10) → `docs/` OPEN_ITEMS_REGISTER (the only list) → HANDOVER (state) → DECISIONS (open rulings) →
CONSTRAINTS when judging any board → everything else on demand (SSI before touching data;
archive/POSTMORTEM for why rule 1 exists).
