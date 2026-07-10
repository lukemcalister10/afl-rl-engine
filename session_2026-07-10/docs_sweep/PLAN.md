# DOCS SWEEP v1a — PLAN + OUTCOMES · 2026-07-10

Branch: `claude/new-session-6q9qgn`. Directive: DIRECTIVE_docs_sweep_v1a.
Mode:auto first artifact (PLAN), updated in place with outcomes. Owner authorized the
main merges and couriered the available archive docs 2026-07-10 ("Yes, merge into main.
What I have is attached.").

## BASE VERIFICATION — PASS
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git` (full URL, pre-merge):
`refs/heads/main` == `refs/tags/v2.7` == `8f8c00b10e2ef3a1b68dd6864594f5bdfef91340`. Re-verified live again immediately before merging.

## ITEM (a) — MERGE SIX PRs INTO main — DONE (owner-authorized)
Merge-commit policy, PR-number order; fresh full-URL ls-remote after each (main head cited):
- #48 UI direction        -> main `ea62dd4dc9b296a3bc61829a388e0fe2f75e21ca`
- #49 injury spec         -> main `f0ec4b414d61258c78118901fdec0ad1bf2b6825`
- #50 flex spec v1        -> main `fd898387d095d686e20d6addc5ec691e913aae9f`
- #53 flex spec v1.1 LAW  -> main `7cdbbee488e6302ed9ac9935be7962d6586f335b`  (add/add on
       flex_spec/SPEC_positional_flex_v1.md auto-resolved — byte-identical both sides)
- #54 UI pitches          -> main `ae68e1dfda823c3ccbae11cfd522a1fcc0e5d2a3`
- #55 Matchday FINAL LOCK -> main `d113d03727d4117dacc6f52caad56dd0c0124af3`
All six were additive, docs/spec-only (docs/ui_direction, session_2026-07-09/*, docs/ui_styles/*)
— ZERO engine/data/gate files, so no STOP condition fired. tag v2.7 correctly UNMOVED at
8f8c00b (docs merges, not a re-bake). #57 verified CLOSED+MERGED (FF promote) — untouched.

## ITEM (b) — REPO-HOME RETURNS (WD-2) — PARTIAL (all available inputs homed)
- Notepad chain (turns 1-50): HOMED verbatim at
  `docs/returns/COMPILED_NOTEPADS_turns01-50_2026-07-10.md` (body cmp-identical to the courier;
  delimited filing header only). Second identical copy the owner re-attached == this one (no dup).
- STILL MISSING (owner: "what I have is attached" — not available): the round's couriered
  verbatim RETURN BODIES (§7-§13) and the v2.6-seam RETURNS_ARCHIVE_2026-07-09.md §8-§13 bodies.
  The notepad chain INDEXES these returns (SHAs/branches/PRs inline) but is not their bodies.
  WD-2 return-body debt therefore REMAINS OPEN for a future courier.

## ITEM (c) — ARCHIVE ROUND DOCS -> docs/archive/ — PARTIAL (archived all provided)
Homed verbatim ("move, don't rewrite") into `docs/archive/`:
- DECISIONS_v87_2026-07-09.md · DECISIONS_v90_2026-07-10.md · HANDOVER_rev127_2026-07-09.md ·
  00_MANIFEST_v4.3.md   (all four cmp-verbatim to the courier).
NOT provided / not in repo (cannot archive): DECISIONS v86, v88, v89 · LTI_REGISTER_2026-07-02.md
· the superseded round directives. These were never committed to this repo and were not couriered;
left for a future courier. (Note: LTI_REGISTER_2026-07-02.md is superseded by the repo sidecar
`LTI_REGISTER.md` already present.)

## ITEM (d) — STALE-MARKER FIXES — PARTIAL
DONE (advanced to the v2.7 baked identity, mirrored verbatim from the canonical committed
`START_HERE.md`; doc_lint gate: 0 FAIL / 0 WARN):
- README.md — identity bullet + lineage advanced c47cb43d/v2.4 -> 7a07e369/v2.7.
- REQUIRED_INPUTS.md — engine-head row c47cb43d/v2.4 -> 7a07e369/v2.7; store row 73d23a8e ->
  a2fbc9a0 (SINGLE SOURCE).
- CHECKPOINT_MANIFEST.md — added a CURRENT BAKED STATE v2.7 block; the v2.4 Identity +
  verify_restore.sh blocks retained verbatim, re-labelled as the 2026-07-02 restore-SEED cut
  record (NOT re-run at v2.7 — engine runs are out of scope, so no fabricated verify output).
NOT DONE — `data/report_states.json` (OWNER-RULED "Advance it", DECISIONS v91 docs-sweep add):
  the committed file does NOT match the ruling's premise. It is two+ bakes stale (`control` =
  "BAKED v2.5 canonical"; newest entry = candidate `4b08796c`); it has NO v2.7 board entry and
  NO current-board "PROTOTYPE" reporting line to advance (the only PROTOTYPE labels are the old
  D7/D8 heads efc15c6c/a9e1c14b, "wired nowhere"). A faithful v2.7 advance needs a board entry
  referencing `data/s4_matrix_*a2fbc9a0*.json` + `data/gates_snapshots/gates_a2fbc9a0.json`,
  neither of which EXISTS in the repo. Advancing it would fabricate a machine-read entry pointing
  at nonexistent artifacts. Held for the bake seat / owner to supply the a2fbc9a0 board-entry data.

## END STATE
main = post-#55 head (see item a) with the six specs/UI docs landed; tag v2.7 unmoved.
Sweep filing (b/c/d) delivered via candidate PR from claude/new-session-6q9qgn.

## RESIDUAL OWNER/COURIER TO-DOS (surfaced, not actioned here)
1. Courier the §7-§13 return bodies + RETURNS_ARCHIVE_2026-07-09 §8-§13 to finish WD-2.
2. Courier DECISIONS v86/v88/v89 + superseded round directives to complete the (c) archive.
3. Bake seat: supply the a2fbc9a0 board entry (+ its matrix/gates artifacts) so report_states.json
   can be advanced to BAKED v2.7 honestly.
4. Branch sweep (the six now-merged session branches + earlier set) — owner/standard delete pattern.
