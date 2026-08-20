#!/usr/bin/env python3
"""APPEND THE INJURY-SHEET RE-CUT's out-of-round transition to data/release_lineage.json.

ADAPTED FROM docs/evidence/d8_adoption_2026-08-20/append_d8_adoption_transition.py — itself adapted
from the landing tail's append_landing_transition.py, the template. What is adapted, and why: source
board 5ea978f7 -> destination board 1d5c9f7a; the STORE IS UNCHANGED (cc02567f both sides), because a
pinned-owner-input re-cut writes no store; the owner_ruling citation is the injury-sheet word,
verbatim.

MEASURED, NOT TYPED. Every identity is read from lineage_measured.json, which this seat produced by
re-hashing a checkout of b86bc9e (the tree immediately before the edit commit 024b458 — b86bc9e adds
only the prereg file to d02520e) and the live tree, each side checked against that tree's own
data/expected_boot.json. This script retypes nothing.

APPEND-ONLY. Every prior entry preserved byte-verbatim; nothing rewritten. The file round-trips at json
indent=1, asserted before AND after. The top-level present-lens baseline (balanced_board_md5 06d8af60,
release_version) is asserted UNMOVED — it is a frozen historical anchor and stamp.release reads it.

  python3 append_recut_transition.py <repo_root> [--dry-run]
"""
import json, os, sys

M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lineage_measured.json')))
S, D = M['source'], M['destination']
BOUNDARY = ["22", "the-sheet-recut-20-8"]

ENTRY = {
    "_doc": (
        "OUT-OF-ROUND PINNED-INPUT RE-CUT (THE INJURY-SHEET RE-CUT, owner word \"All good on the "
        "injury sheet. Fine by me.\", 2026-08-20; register v790 preregged the remedy). "
        "docs/owner_annotations/SITTER_2026_v1.csv is the single source of injury truth and a PINNED "
        "input: its md5, row count and injured=Y count are asserted in the engine, and ORDER 42 "
        "additionally requires every injured=Y row's games_2026 to equal the store's 2026 games "
        "EXACTLY. A round advance increments games for every listed player, and the owner's real R23 "
        "file lists exactly TWO of the 37 injured-marked players — HARRY ARMSTRONG and JUDSON CLARKE — "
        "so applying R23 would desynchronise the sheet from the store and HALT the board regen inside "
        "the R23 transaction. The runbook (§4 H2) rated this \"a coin flip on the owner's file\"; the "
        "read-only R23 preflight measured the real file and it LANDED. The two rows are therefore "
        "flipped injured Y->N: sheet md5 b26798c3 -> 21361291, 15,948 bytes and 219 rows UNCHANGED, "
        "injured=Y 37 -> 35, CRLF preserved, EXACTLY TWO BYTES DIFFERENT. THE SIX PINS MOVE IN THE SAME "
        "COMMIT AS THE SHEET, ACROSS TWO BLOCKS: register v790 and the seat brief named only the ORDER "
        "42 three (_SHEET_MD5/_SHEET_ROWS/_SHEET_Y), and the preflight caught an EARLIER ORDER 41 block "
        "(O41_INJ_MD5/O41_INJ_ROWS/O41_INJ_Y) that asserts the same three facts and HALTS FIRST — moving "
        "only the ORDER 42 pins would have halted the build at ORDER 41. NEITHER GUARD IS WEAKENED: both "
        "still assert md5 + rows + Y-count + the full name match, and the runbook's alternative option "
        "(b), loosening the check to store_games >= sheet_games, was NOT taken because the owner ruled "
        "the re-cut. THE BOARD MOVES: 5ea978f7 -> 1d5c9f7a, board total 693,753 -> 693,727 over the same "
        "804 active rows (-26). EXACTLY ONE PLAYER MOVES, and it is one of the two named: JUDSON CLARKE "
        "75 -> 49 (-26). HARRY ARMSTRONG is UNMOVED at 518 — he was already parity-lifted to his healthy "
        "value, so de-listing him is a genuine no-op. Zero ripple: 803 of 804 rows are byte-identical "
        "and the PICK 1 numeraire is unmoved at 3,000. THE STORE DOES NOT MOVE: cc02567f both sides; no "
        "round is applied, the ledger stays at 3,086 triples and the round pin stays at 22. Because this "
        "is an out-of-round move, the standing owner rule of 2026-07-28 writes a history column at the "
        "point as well: `the-sheet-recut-20-8`, registered in the value / rank / pos_rank histories from "
        "the re-cut board (804 points each) by the out_of_round_column writer of record. That column is "
        "ALSO what rule M0 requires of the R23 advance that follows: the R22->R23 movers baseline must "
        "share as_of_round with the candidate, and round_finalize compares round 23 against the stored "
        "point IMMEDIATELY BEFORE it — so the D8 adoption and this re-cut both sit on the R22 side of "
        "the boundary and the round-23 movers show only what round 23's scores did. balanced_board_md5 "
        "a49c155f -> e616936e is a REAL, BUILT move, not a re-stamp: sibling_repin.py reconcile rebuilt "
        "the balanced/strict sibling from the same store and derived the pin from the built artifact; "
        "verify went from 8 fails to 0. config_sha256 is UNMOVED and that is correct — the injury sheet "
        "is a PINNED OWNER INPUT, not a manifest dial. The book is NOT re-sealed by this act."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["THE_INJURY_SHEET_RECUT_2026-08-20_all_good_fine_by_me"],
    "owner_ruling": (
        "THE INJURY-SHEET RE-CUT, owner word 2026-08-20, VERBATIM: \"All good on the injury sheet. "
        "Fine by me.\" — given in chat, on the H2 remedy the R23 runbook escalated and register v790 "
        "preregged. Per the 5babe71 precedent this entry RECORDS an approval that already exists in "
        "the owner's own words; it does not create one."
    ),
    "authority": (
        "Luke McAlister (owner) — sole STOP-1/STOP-2/merge authority; the word given directly in chat "
        "2026-08-20 and carried to this seat in its execution brief; written by the R23 advance engine "
        "seat (no interpretive authority)."
    ),
    "applies_to": {"bundle": "ui/data/movers.js", "boundary": BOUNDARY},
    "source": {
        "release_version": S["release_version"], "board": S["board"], "store": S["store"],
        "rl_model": S["rl_model"], "engine_head": S["engine_head"], "fv": S["fv"],
        "config": S["config"], "register": S["register"],
        "balanced_board_md5": S["balanced_board_md5"], "v0surf": S["v0surf"],
        "as_of_round": S["as_of_round"],
    },
    "destination": {
        "release_version": D["release_version"], "board": D["board"], "store": D["store"],
        "rl_model": D["rl_model"], "engine_head": D["engine_head"], "fv": D["fv"],
        "config": D["config"], "register": D["register"],
        "balanced_board_md5": D["balanced_board_md5"], "v0surf": D["v0surf"],
        "as_of_round": D["as_of_round"],
    },
    "moved_by_transition": M["moved"],
    "unchanged_across_transition": M["unchanged"],
    "invariants": {
        "store_unmoved_by_transition": D["store"],
        "config_unmoved_by_transition": D["config"],
        "round_held": "as_of_round 22 on both sides; no round applied, ledger unchanged at 3,086 triples",
        "sheet_pin": "md5 21361291f26d35108b88f92f885c5063, 219 rows, 35 injured=Y — asserted by BOTH "
                     "the ORDER 41 and the ORDER 42 pin blocks",
        "movers": "exactly 1 of 804 rows moved: judson-clarke 75 -> 49. harry-armstrong UNMOVED at 518.",
        "numeraire": "PICK 1 = 3000, unmoved",
        "book_reseal": "NONE — a book re-seal is a separate act and was not smuggled into this one",
    },
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted. Every `source` identity was re-hashed from a "
        "checkout of b86bc9e — the tree immediately before the edit commit 024b458; b86bc9e adds only "
        "docs/evidence/r23_advance_2026-08-20/01_PREREG_SHEET_RECUT.md to main d02520e — board and store "
        "by md5 of data/rl_build/rl_app_data.json and engine/rl_after/rl_model_data.json, engine_head and "
        "rl_model by md5 of engine/rl_after/_merged_recover.py and engine/rl_after/rl_model.py, config by "
        "config_manifest.manifest_hash, fv by fv_provenance.fv_identity over engine/forward_valuation, "
        "register by md5 of LTI_REGISTER.md, v0surf by md5 of data/v0surf.pkl, balanced_board_md5 from "
        "engine/rl_after/ingestion/sibling_repin_state.json — and each agrees with that tree's own "
        "data/expected_boot.json. Every `destination` identity was re-hashed the same way from the live "
        "tree and agrees with the landed data/expected_boot.json. Board totals were measured on the two "
        "board files directly: 804 rows / 693,753 -> 804 rows / 693,727."
    ),
}


def main():
    root = os.path.abspath(sys.argv[1]); dry = "--dry-run" in sys.argv
    p = os.path.join(root, "data", "release_lineage.json")
    raw = open(p, "rb").read(); d = json.loads(raw)
    if json.dumps(d, indent=1).encode() != raw:
        raise SystemExit("HALT: release_lineage.json does not round-trip at indent=1; refusing to reformat it")
    base_balanced, base_version = d.get("balanced_board_md5"), d.get("release_version")
    reg = d.get("release_transition_register")
    if not isinstance(reg, list):
        raise SystemExit("HALT: release_transition_register missing or not a list")
    before = json.dumps(reg)
    for e in reg:
        if isinstance(e, dict) and e.get("applies_to", {}).get("boundary") == BOUNDARY:
            print("already present — no-op"); return

    dest_board = ENTRY["destination"]["board"]
    for e in [d.get("release_transition") or {}] + [e for e in reg if isinstance(e, dict)]:
        if (e.get("destination") or {}).get("board") == dest_board:
            raise SystemExit("HALT: an existing record already declares destination.board %s (ruling %r) "
                             "— appending would supersede it" % (dest_board, e.get("owner_ruling_id")))
    prev_dest = (reg[-1].get("destination") or {}) if reg else {}
    if str(prev_dest.get("store")) != ENTRY["source"]["store"]:
        raise SystemExit("HALT: register tail destination.store %s != this entry's source.store %s"
                         % (prev_dest.get("store"), ENTRY["source"]["store"]))
    if str(prev_dest.get("board")) != ENTRY["source"]["board"]:
        raise SystemExit("HALT: register tail destination.board %s != this entry's source.board %s — the "
                         "chain would skip a board" % (prev_dest.get("board"), ENTRY["source"]["board"]))
    print("chain OK: register tail destination.store %s == this entry's source.store" % prev_dest.get("store"))
    print("chain OK: register tail destination.board %s == this entry's source.board" % prev_dest.get("board"))
    print("boundary %r is NEW; destination.board %s is declared by no existing record." % (BOUNDARY, dest_board))

    reg.append(ENTRY)
    if json.dumps(reg[:-1]) != before:
        raise SystemExit("HALT: a prior register entry changed; append-only violated")
    if d.get("balanced_board_md5") != base_balanced or d.get("release_version") != base_version:
        raise SystemExit("HALT: release_lineage top-level present-lens baseline moved — it must never move")
    print("append-only OK: %d prior entries byte-verbatim; top-level baseline %s / %s UNMOVED"
          % (len(reg) - 1, base_balanced, base_version))
    out = json.dumps(d, indent=1).encode()
    if not dry:
        open(p, "wb").write(out)
        back = open(p, "rb").read()
        d2 = json.loads(back)
        if json.dumps(d2, indent=1).encode() != back:
            raise SystemExit("HALT: the written file does not round-trip at indent=1")
        if json.dumps(d2["release_transition_register"][:-1]) != before:
            raise SystemExit("HALT: re-read shows a prior entry changed")
        print("re-read OK: round-trips at indent=1; prior entries still byte-verbatim.")
    print("appended entry %d; %d -> %d bytes%s" % (len(reg), len(raw), len(out), " (dry run)" if dry else ""))
    print("  source      board %s  store %s  engine_head %s  balanced %s"
          % (ENTRY["source"]["board"], ENTRY["source"]["store"], ENTRY["source"]["engine_head"], ENTRY["source"]["balanced_board_md5"]))
    print("  destination board %s  store %s  engine_head %s  balanced %s"
          % (ENTRY["destination"]["board"], ENTRY["destination"]["store"], ENTRY["destination"]["engine_head"], ENTRY["destination"]["balanced_board_md5"]))
    print("  moved     : %s" % ENTRY["moved_by_transition"])
    print("  unchanged : %s" % ENTRY["unchanged_across_transition"])


if __name__ == "__main__":
    main()
