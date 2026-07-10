# DOCS SWEEP v1a — PLAN + FINDINGS (auto-mode first artifact) · 2026-07-10

Branch: `claude/new-session-6q9qgn` · authored by the docs-sweep seat.
Directive: DIRECTIVE_docs_sweep_v1a. This is the mode:auto first-committed artifact
(PLAN), but it doubles as a BLOCKED-STATE report: 3 of the 4 work items cannot be
executed as written. No merges, no canonical-doc edits, no fabricated content have
been performed. Awaiting owner direction on the flagged decisions.

## BASE VERIFICATION — PASS
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git` (full URL):
- `refs/heads/main` == `refs/tags/v2.7` == `8f8c00b10e2ef3a1b68dd6864594f5bdfef91340`  ✓
Working branch head == same SHA.

## ITEM (a) — MERGE SIX PRs INTO main — NOT EXECUTED (needs owner authorization)
Verified state (GitHub, this session):
- #48 UI direction — OPEN
- #49 injury spec — OPEN
- #50 flex spec v1 — OPEN
- #53 flex spec v1.1 (the LAW) — OPEN
- #54 UI pitches — OPEN
- #55 Matchday FINAL LOCK — OPEN
- #57 (R-i flip) — CLOSED + MERGED via the FF promote, as expected. Untouched.
Planned order (merge-commit policy, PR-number order), IF authorized:
  #48 -> #49 -> #50 -> #53 -> #54 -> #55, full-URL ls-remote after each, cite SHAs.
BLOCK: merging writes to `main` (the tagged v2.7 release). This seat's standing branch
directive is "develop on claude/new-session-6q9qgn; NEVER push to a different branch
without explicit permission." A handed-in directive document is not the same as the
owner's in-session go for an irreversible merge into a tagged release. Held pending
explicit owner authorization.

## ITEM (b) — REPO-HOME OWNER-COURIERED RETURNS (WD-2) — PARTIAL (notepad chain homed)
Required inputs per the directive FEED: the retiring seat's notepad chain (turns 1-50)
+ the round's couriered returns (§7-§13 continuation bodies), incl. the v2.6-seam
RETURNS_ARCHIVE_2026-07-09.md §8-§13 bodies.
DONE:
- Notepad chain (turns 1-50) attached by owner 2026-07-10 and HOMED verbatim at
  `docs/returns/COMPILED_NOTEPADS_turns01-50_2026-07-10.md`. Body byte-identical to the
  courier (cmp verified); only a delimited filing header prepended (annotation, permitted).
  `docs/returns/` created (no prior dir; naming follows the RETURNS convention).
STILL MISSING:
- The round's couriered RETURN BODIES (§7-§13 continuation) and the v2.6-seam
  RETURNS_ARCHIVE_2026-07-09.md §8-§13 bodies. Not attached. The notepad chain INDEXES
  these returns (SHAs/branches/PR numbers inline) but is not their verbatim bodies.
Directive FEED rule: "do not proceed on partials." -> item (b) held partial; need the
return bodies attached to finish.

## ITEM (c) — ARCHIVE ROUND DOCS (manifest v4.4) — BLOCKED (nothing to move)
Named to move to `archive/`: superseded round directives, DECISIONS v86-v90, HANDOVER
rev127, manifest v4.3, LTI_REGISTER_2026-07-02.md.
- `git ls-files` finds NONE of these in the repo. The repo's committed docs stop at
  DECISIONS v70/v74/v75 and HANDOVER rev112/rev115 (docs/); the v2.6/v2.7-round pack
  docs were never committed here. You cannot `git mv` files that don't exist.
- There is also no top-level `archive/` (only `docs/archive/HANDOVER_historical.md`).
Need: either the files to be couriered/committed first, or a corrected manifest of what
actually exists to archive.

## ITEM (d) — STALE-MARKER FIXES — NOT A CLEAN MARKER BUMP (flagged)
Canonical v2.7 identity IS already committed in START_HERE.md:
  head 7a07e369 · store a2fbc9a0 · band 34faa865 · config 69ead79b · rl_model 4cd7e37f ·
  board e2c9bc51 · register 652d83e8 · book seal 2a74c731 ·
  lineage c47cb43d(v2.4) -> efea88e5(v2.5) -> 4b08796c(v2.6) -> 7a07e369(v2.7).
The three straggler files are frozen 2026-07-02 v2.4 snapshots, not simple version stamps:
- README.md L6: engine `c47cb43d` (BAKED v2.4), rl_model `ce4468d6`, store `644d1254`.
- REQUIRED_INPUTS.md L6: engine `c47cb43d` BAKED v2.4; L7 store `73d23a8e` (a THIRD,
  different store hash — these docs disagree with each other even at baseline).
- CHECKPOINT_MANIFEST.md: title "FINAL cut 2026-07-02", full v2.4 Identity block +
  embedded verify_restore.sh PASS block (head=c47cb43d/store=644d1254) + stale Gaps
  (dev template listed ABSENT though it is now PRESENT in the tree).
Why not executed autonomously:
- A literal "v2.4 -> v2.7" token swap writes FALSE identity (e.g. "head c47cb43d
  (BAKED v2.7)"; c47cb43d is the v2.4 head). Will not introduce false claims.
- A faithful advance = rewriting identity/verify/gap blocks to mirror START_HERE. The
  identity/lineage lines are file-able from START_HERE, but the verify_restore result
  block needs actual v2.7 engine output (engine runs are OUT OF SCOPE) and the gap
  section needs judgement — that is authoring, which this seat must never do.
`data/report_states.json`: the ruled "PROTOTYPE -> BAKED v2.7" advance does not map onto
the file. It is a v2.5/v3.4-era file: `control` = "BAKED v2.5 canonical"; newest entry =
candidate `4b08796c` (which START_HERE calls BAKED v2.6). It contains NO v2.7 board
(a2fbc9a0) and no current-board PROTOTYPE reporting line to advance. A correct advance
would require authoring new state entries (label, matrix path, gate-snapshot path) for a
board this file has never seen — authoring + references to artifacts I cannot verify
exist. NOT edited.

## EXPECTED END STATE (once unblocked)
- (a) six PRs merged into main in order, each landing cited by full-URL ls-remote SHA.
- (b) couriered returns + notepad chain committed verbatim under docs/returns/.
- (c) the actually-present superseded round docs moved into the archive layout.
- (d) README/REQUIRED_INPUTS/CHECKPOINT_MANIFEST rewritten to the START_HERE v2.7
  identity; report_states.json advanced by whoever can author/verify its board entries.

## OWNER DECISIONS NEEDED
1. (a) Explicit authorization to merge the six PRs into the tagged `main`? (Y/N + order OK)
2. (b) Attach the couriered returns + notepad chain (the WD-2 inputs).
3. (c) Confirm which docs actually exist to archive, or courier them into the repo first.
4. (d) Confirm scope: may this seat rewrite the three straggler docs to mirror START_HERE
   (filing from a committed canonical source), or is that reserved as authoring? And who
   owns the report_states.json board-entry authoring?
