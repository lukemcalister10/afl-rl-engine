# P4-4 — Retire `land round` (MEDIUM; after a REAL 2027 round has landed through tools/ingest; owner word)

**Depends on.** P2-1 landed AND one real (or owner-accepted rehearsed) 2027 round ingested through it. P4-3.
Serial rule: steps.py, spec.py, carriers.py. **Owner word (law 10a):** RULEBOOK P13 (RULEBOOK.md:159-164) names
"the round lander" as the one writer of data/sheet_pins.json; retiring the lane changes that law's subject.

**Done when.** The round-advance lane and the code only it uses are deleted unit by unit, the sitter-sheet pins have
a named writer outside the lane (and P13 says so, on the owner's word), every historical round-advance spec still
validates, and acceptance + CI are green.

**Facts (checked at ffb2663b).**
- The lane: ROUND_SEQUENCE steps.py:3843-3858 (preflight, sheet, scores, catchup_preflight, advance,
  generator_sync, day0, contract, ui, movers_page, state, gates, claims, commit); SEQUENCES 'round-advance' (:3879);
  the `tools/land round` verb (tools/land:4; cli.py); spec.py ACT_KINDS (:28), `_validate_round` (:124),
  `_round_template` (:675); the round carriers in carriers.py:267-294 (season_state, applied_rounds_ledger,
  finalization_state/journal, movers/*, .weekly_txn/**, the c3 sibling targets).
- Code only the lane reaches: staged_apply.py (its c3 loads sibling_repin.py, :883-884, which loads forward_lens.py,
  sibling_repin.py:82-84), round_apply.py, round_catchup.py, round_finalize.py, tools/landing/day0_emit.py
  (DAY0_GENERATOR :3438) and the DAY0_CP carrier (carriers.py:306-311; txn.py:376), DELEGATED_PINS 'as_of_round' /
  'season_state' / 'rl_model_data' text (:112-114; P2-1/P3-2 give them a new writer first).
- LIVE READERS that stop a deletion until handled in the same commit: acceptance `oneliner_r14_restore`
  (acceptance/checks/m1a.py:272-292, PROFILE 'host-insensitive', so CI runs it) executes
  engine/rl_after/ingestion/test_weekly_updater.py, which imports round_entry, staged_apply, score_ingestor (:19-21)
  and round_finalize (:295); tools/round_entry/ (weekly_update.sh/.bat) drives round_entry; ui/tools/
  rebuild_movers_derived.py uses round_movers (keep round_movers). round_finalize.py:311 is a movers.js writer (P2-2).
- The sheet step (steps.py:2801, SHEET_PIN_REL :2763) is the only programmatic writer of data/sheet_pins.json.
- Round-advance specs on disk (`grep -rl '"round-advance"' --include='ACT_SPEC*.json' docs/evidence`): 7 —
  fw1_advance_2026-08-30/ACT_SPEC_FW1.json, p2b_round_lander_2026-08-21/ACT_SPEC_DRYRUN.json,
  r24_advance_2026-08-23/ACT_SPEC_R24.json and four r24_rehearsal_2026-08-21/act_specs/*. Not "R15-R24": earlier rounds
  predate the lander. If P4-1b has archived any of them, validate on the archive branch too.
- The RULEBOOK has no "land lever"/"land round" wording (`grep -n "land lever\|land round" docs/RULEBOOK.md`: none).
  Only P13 (above) and P14's tools/ingest wording concern this item.

**Change, one commit per unit.** (1) sheet pins: a new writer (tools/ingest round branch or a `tools/sheet` command)
+ the P13 amendment drafted for the owner; (2) test_weekly_updater / oneliner_r14_restore: retire the check or point
it at the ingest round path — decide with evidence; (3) ROUND_SEQUENCE, its steps (sheet, scores, catchup_preflight,
advance, generator_sync, day0, movers_page), the cli verb, round carriers; (4) staged_apply + sibling_repin +
forward_lens + round_apply + round_catchup + round_finalize + day0_emit (grep each first), and the round legs of tools/landing/selftest.py (16 references to the round lane); (5) spec.py keeps
'round-advance' ACCEPTED for validation of history but no sequence runs it (a clear refusal at launch).

**Must not change.** release_lineage.json, docs/register/, every historical spec's validity, round_movers.py,
the board/store/pins, P2-1's round path.

**Prove it.** Full tools/landing test set (test_txn, test_proofstash, test_store_edit, test_finals_bounds);
`tools/land selftest`; the spec baseline incl. the 7 round-advance specs; P2-1's hybrid replay still reproduces;
acceptance `--profile full` and `--profile host-insensitive`; `python3 tools/rulebook_lint.py`; CI green.

**Lands via.** Plain commits, one per unit; the P13 edit only with the owner's word.
