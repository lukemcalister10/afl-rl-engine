THE OWNER'S TWO INPUTS STAGED — the 112-row store write proves clean and the board does not move, then the transaction fails closed on a SIXTH landing-tail carrier

THE OWNER'S BYTES, VERBATIM. docs/inputs/AFFL_Player_Locations.csv (md5 e38398005e5ee825af81765c91da6d1a)
and docs/inputs/AFFL_Pick_Locations.xlsx (md5 6ba0464c6423c650455d60b5ab289eea) are byte-identical to
the uploads. Nothing normalised, nothing re-saved.

PRE-DIFF, INDEPENDENTLY REPRODUCED (10_owner_csv_prediff.txt, 12_owner_picks_prediff.txt):
  AFFL_Player_Locations.csv  header identical · 804 data rows both sides · name set identical ·
    Player Name 0 changes · Position/s 0 · AFL Club 0 · AFFL Team 112. The 112 are enumerated in
    11_the_112_movers.json. Free-agent spelling split ('Free agents','Free Agents') 73/2 -> 87/2,
    preserved exactly as authored — canonicalising on the way IN would rewrite rows the owner never
    edited, and ui/tests/ownership_store_apply.test.py asserts that law is load-bearing.
  AFFL_Pick_Locations.xlsx   sheets identical · Picks header on ROW 2, exact columns as briefed ·
    160 data rows, ID set identical · ID 0 · Year 0 · Round 0 · Origin Team 0 · OWNER 23 (enumerated
    in 13_the_23_pick_owner_changes.json) · Pick (low) 70 · Pick (high) 70 · Band 120 — all formula
    cascade from 13 changed Ladder rows · Raw Value 158 / Value (counted) 158 and the Pick Values tab
    (81 rows, width 4 -> 3) are reference-only-never-read, tolerated as briefed.
    NOTED FOR THE CURVE FORK BELOW: Ladder row 29 "Board value each year (fixed)" moved 54333 -> 47315,
    and 47315 is exactly the LANDED curve artifact's own 1-64 ladder sum. The owner has pasted the
    landed curve into his workbook.

WHAT THE INGEST PROVED BEFORE IT HALTED (14_ingest_owner_inputs.txt, exit 2):
  [P1] cp312 pinned
  [P3] six-way incoming coherence — all read cb38ef11   <-- the landing-tail repair holding
  [P8] serializer identity — dumps(loads(store)) == store bytes (1,978,110)
  [P4] CSV utf-8 · 805 lines = 1 header + 804 players (CRLF preserved)
  [P5] join by key — 0 unmatched, 0 board keys missing from the store, 804 resolved
  [P6] club spellings — all 804 authored values are known spellings
  [P7] plan — 112 of 804 authored rows move, every one printed
  [T1] store written on the overlay  cb38ef11 -> cc02567f
  [T2] STORE DIFF PROOF — affl_team ONLY, on exactly 112 planned keys; byte-attribution OK
  [T3] pins moved — expected_boot.store · release_contract.identities.store + re-seal ·
       season_state.source_store_md5 · board srcmd5.source_md5; season derived values proven
       unchanged (calendar_progress 0.92, exposure_pace 0.818)
  [T4] BOARD UNMOVED — a05fe951 byte-identical, no engine build

  ■ HALT at T5 — "register tail destination.store d9a24282 != the store being superseded cb38ef11"

THE SIXTH CARRIER (15_lineage_register_HALT_fork.txt). data/release_lineage.json's
release_transition_register still ends at entry [5] G1_NEVER_RISES (store d9a24282 -> d9a24282,
board a672ed3a -> 4b448a82). THE LANDING moved the board 4b448a82 -> a05fe951 and the store
d9a24282 -> cb38ef11 outside a round and appended NO entry, so the append-only chain is broken at
the landing and every out-of-round writer that extends it fails closed. The lineage file's own _doc
says an appended entry "is the shape the validator's own law prescribes for a future out-of-round
board move"; the standing owner rule of 2026-07-28 says a board move outside a round also writes a
column at that point. Neither exists for THE LANDING.
I did not author it. That entry is an OWNER-APPROVAL RECORD (owner_approved / owner_ruling_id /
owner_ruling VERBATIM / authority) and the 5babe71 precedent is explicit: "It RECORDS an approval
that already exists in his words; it does not create one." Writing it needs the landing's boundary
label + out-of-round column id, its owner citation, a ruling on whether THE LANDING declares a board
boundary (a misdeclaration silently overwrites another record's owner_ruling_id), and 804
value/rank/pos-rank history points. None of that is in my record. FORK stated in the evidence file.

BEHIND IT, A SEVENTH: ui/release_pick_curve.json (05_curve_contract_HALT_fork.txt) — CURVE DRIFT
78ad9842 != f6f3027f with the PAYLOAD identity also moved df766dff -> 9729f0c5 under ORDER 31-F.
That is a curve ADOPTION, not a mirror re-stamp, and it cannot be done without editing
engine/rl_after/one_source_selftest.py:492 (_contract_md5), which this order forbids. Both halts
must be ruled before the apply can complete; one `python3 ui/tools/ingest_inputs.py` finishes
everything the moment they are.

THE TREE IS BYTE-UNCHANGED WHERE IT MATTERS. The transaction is atomic and it committed nothing:
data/rl_build/rl_app_data.json, engine/rl_after/rl_model_data.json, data/expected_boot.json,
data/release_contract.json and data/season_state.json all md5sum -c OK against their pre-run hashes.
THE BOARD IS STILL a05fe951f78482c70520480e184c80ec. The store is still cb38ef11 — UNWRITTEN.
Six-way coherence re-verified PASS after the halt.

WHAT THIS COMMIT CARRIES: the owner's two authored inputs, in place and untouched, ready for the
apply; the ingest's own outputs, which are the DESIGNED refusal (ui/data/club_valuation.js and
ui/data/ownership.js now carry the halt reason and render nothing). Shipping the refusal rather than
leaving the pre-landing overlay in place is the doctrine: a stale club-valuation/ownership overlay
under a freshly landed board is exactly the "one player, two clubs" silent-drift state these guards
exist to prevent.

SPOT-CHECKS (16_spot_checks.txt) are on the RESOLVED JOIN, since the store was not written:
Matt Johnson -> matt-johnson-1, Maurice Rioli -> maurice-rioli-1 (both name-twin hazard keys the
#283 design names, resolved correctly through board -> key, never name -> store),
Marcus Bontempelli -> St Kilda Saints, Sam Walsh -> St Kilda Saints, Taylor Walker -> Free agents,
Aaron Naughton -> Brisbane Lions. Nick Daicos unchanged, as a non-mover control.

NO ENGINE EDIT. NO ROUND ADVANCE. NO BOARD MOVEMENT.

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015btatc67QZdz4vV8FwJ7t6

--------------------------------------------------------------------------------
FILING NOTE. This account was written as the commit message for the owner-inputs
stage. While it was being composed, a concurrent supervisor-pen session in the same
Claude-Session committed 6ff0d69 ("register v785 + programme status") from the shared
git index and swept this stage's already-staged files into it, then pushed. The
CONTENT is therefore correct and on origin/main (docs/inputs/AFFL_Player_Locations.csv
e38398005e..., docs/inputs/AFFL_Pick_Locations.xlsx 6ba04646..., the halted
ui/data/club_valuation.js + ui/data/ownership.js, and evidence files 10-16) — only its
message landed under the register commit's title. Pushed history is not rewritten; the
account is filed here instead so the record is durable and findable beside its evidence.

STATE AT HAND-OFF
  origin/main  6ff0d69
    5280da0  THE LANDING TAIL — carriers (a)(b)(c) reconciled  [this seat]
    6ff0d69  register v785 (+ this seat's owner-input stage, swept in)
  six-way store coherence   PASS, all six read cb38ef11
  board                     a05fe951f78482c70520480e184c80ec  UNCHANGED
  store                     cb38ef1171dcf20aae66ebf12682be0d  UNWRITTEN
  as_of_round               22, unmoved
  BLOCKED ON, in the order they fire:
    1. data/release_lineage.json release_transition_register tail  (15_..._HALT_fork.txt)
    2. ui/release_pick_curve.json curve provenance                 (05_..._HALT_fork.txt)
    3. data/release_contract.json code identities + config_sha256  (08_..._residual_HALT.txt)
    4. the sibling layer, named not run                            (09_sibling_repin_verify.txt)
  Once 1 and 2 are ruled, ONE `python3 ui/tools/ingest_inputs.py` completes the apply:
  the 112 player moves and the 23 pick-owner moves are staged and proven clean already.
