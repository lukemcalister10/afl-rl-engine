# DIRECTIVE — THE ROUND-ENTRY TOOL (resolver + preview + stamped snapshots; DRY-RUN ONLY)
**v1.0** · 2026-07-17 · supervisor seat 12 · build model: **Opus via Claude Code** · ONE JOB, ONE CHAT (S2)
STATUS: ISSUED — fire when pasted by the owner. **Runs PARALLEL to the Leg-D writer by design:
tools-disjoint, store READ-ONLY, expected board movers ZERO.**

## ⛔ EXECUTE FIRST — BEFORE READING ANYTHING ELSE (your first committed artifact is this block's proof)
```
git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/main
#   Record the SHA. Base rule: main AT OR AFTER 4848f80bf97fe2103beed95dbeb4c945ad39f678, and
#   git diff --name-only 4848f80bf97fe2103beed95dbeb4c945ad39f678..<printed-SHA> must be docs/-ONLY
#   (the supervisor's pen moves main). Any non-docs drift: HALT, report, stop.
git fetch origin main && git checkout -b claude/round-entry-tool origin/main
git merge-base --is-ancestor 4848f80bf97fe2103beed95dbeb4c945ad39f678 HEAD && echo ANCESTOR-PROOF-PASS
ls engine/rl_after/ingestion/   # MUST list round_score_parser.py · score_ingestor.py · dry_run_proof.py — else HALT.
grep -n "IngestionGatedError\|APPLY_DEFAULT" engine/rl_after/ingestion/score_ingestor.py | head -4
#   MUST show the gate present and APPLY_DEFAULT False — the write path is ABSENT BY DESIGN; if you
#   cannot see the gate, HALT.
```
Commit the output as `session_2026-07-17/round_entry_tool/FIRST_COMMANDS_PROOF.txt` — your FIRST
commit, before the PLAN (prescreen rejects any branch whose first commit is not the proof).

## THE FIVE (CORE)
- **EFFORT: Medium.** Why not High: the plumbing exists (the provision module), the UX is fully ruled
  (item 305 verbatim below), no value changes, no gate touched, no store write — this is enumerated
  tool work. Why not lower: the residue-handling law has hard NEVERs whose violation silently corrupts
  the owner's weekly data, and the snapshot format must honour SSI stamping exactly.
- **MODE: auto.** First committed artifact after the proof = the PLAN.
- **TIME: 2–4 h.** Confirm up front; flag >2×/<½×; report actual.
- **FEED (documents, not restatements):** register item **305** (THE RULING OF RECORD — its frame
  supersedes item 303's identity paragraph) + item 297 (the dial deferral) · docs/GO_LIVE_round_score_
  ingestion.md (the provision state + the two-half switch; the WRITE half stays ABSENT — that is the
  post-delivery go-live job, NOT yours) · SINGLE_SOURCE_INVARIANT.md (snapshots are DERIVED:
  read-only, source-stamped, disposable) · CONSTRAINTS v1.19 (context only; no gate binds a zero-mover
  tool build) · the existing module `engine/rl_after/ingestion/`.
- **FENCE.** IN: `engine/rl_after/ingestion/**` · a thin CLI entry `tools/round_entry/` (new) · your
  `session_2026-07-17/round_entry_tool/` dir (fixtures, proofs, previews). OUT: **the SOURCE STORE
  (READ-ONLY at run time by design — and the store-WRITE code path stays ABSENT; building it is the
  post-delivery job on the owner's word, register v25/GO_LIVE)** · docs/ (always) · every Leg-D fence
  file (`_merged_recover.py` · `s4_matrix_7147.py` · `one_source_selftest.py` · the curve artifacts ·
  `expected_boot.json`) · `rl_model.py` · UI code (the snapshot FORMAT feeds the UI line later; the UI
  wiring is not this job). A need outside the fence ⇒ HALT-and-ask, never self-extend.

## THE LAW (item 305, owner ground-truth — carry verbatim in the module docstring)
Input of record: a FootyWire weekly export, `name, score`, names identical to the DB, CURRENT players
only. The owner's workflow is PRESERVED: paste round + name + score — a 2-minute job; unique IDs are
NOT required and not asked for. The resolver **exact-matches name → active-stable-ID over the LIVE
active pool read at RUN TIME** (new-intake IDs picked up automatically the moment they enter the DB).
**The real failure mode is a SILENT MISS, not a clash:** any export name that does not cleanly resolve
is a **FLAGGED RESIDUE LINE for a one-tap owner confirm — NEVER a silent drop, NEVER attached to the
wrong row, NEVER a new-row invention.** A scoring player not yet in the DB is residue (ask), never a guess.

## THE JOB (in this order)
1. **THE RESOLVER.** Exact-match over the live active pool (case/whitespace-normalised exact; no fuzzy
   auto-attach — a near-miss is residue WITH the nearest candidates listed for the one-tap confirm,
   the owner choosing, never the tool). Ambiguity (two active exact matches) = residue with both
   candidates shown. Output per round: the resolved set (stable-ID · name · score) + the residue file.
2. **THE ENTRY PATH.** One command taking `--round N` + a pasted/`.csv` `name,score` body (both
   accepted). Idempotent per round: re-entering a round REPLACES that round's preview/snapshot,
   loudly, never duplicates.
3. **THE RESIDUE CONFIRM LOOP.** The residue file is human-first: one line per unresolved name, the
   proposed resolution(s), and a single edit the owner makes (pick a candidate / mark skip). A second
   command consumes the confirmed file. NOTHING enters a snapshot unresolved.
4. **PER-ROUND STAMPED SNAPSHOTS (SSI-conformant).** Derived, read-only, carrying: round · the
   resolved rows · source store md5 at generation · module code md5 · generation time. These are the
   week-to-week UI value-line feed (format documented in the module README; UI wiring later).
   Regenerating from the same inputs must be byte-identical (determinism check committed).
5. **DRY-RUN PROOFS on committed fixtures** (script-emitted counts, never typed): (a) a clean round
   (all resolve) · (b) a misspelled name → residue, then confirmed via the loop · (c) an unknown/
   not-yet-in-DB name → residue, skip path · (d) a synthetic two-active-exact-match clash → residue
   with both candidates · (e) idempotent re-entry replaces. Plus the NO-WRITE proofs: `apply()` still
   raises (invoke it, commit the raised error) · store md5 UNCHANGED before/after every fixture run ·
   board untouched (no derived board regeneration in this job at all).
6. **MODULE README** updated (in-tree, engine side — builds never author docs/): the commands, the
   residue loop, the snapshot format, and the line "the write path is absent by design; go-live is a
   separate owner-worded job (GO_LIVE runbook)."

## DELIVERABLES
The proof · the PLAN · per-task commits · the five fixture proofs + no-write proofs (committed, with
exit codes — SILENCE IS A RED) · the snapshot determinism check · the module README · candidate PR
against MAIN (tools path — no bake, no board, no ladder; the owner can merge on prescreen like
PRs #106/#107). RETURN ≤30 lines · branch · head SHA · PR number · "in plain terms" close · actual time.

## STANDING CONDUCT (HANDOVER rev158 §3 — binding here)
Proof-first (298/299) · stable-ID identity — resolution output is IDs, names are display (269) ·
counts script-emitted (295/309) · SILENCE IS A RED · one authored source: the store is read, snapshots
are derived-stamped, nothing else exists (SSI) · no terminal item-counts · the owner's 2-minute
workflow is the design bar — if a step costs him more than a paste and a one-tap confirm, it is wrong.
