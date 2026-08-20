#!/usr/bin/env python3
"""APPEND THE F5 ROUNDING ACT's out-of-round transition to data/release_lineage.json.

ADAPTED FROM docs/evidence/r23_advance_2026-08-20/append_recut_transition.py — itself the D8
adaptation of the landing tail's template.

MEASURED, NOT TYPED. Every identity is read from lineage_measured.json, produced by re-hashing the
committed tree at 2991740 (the commit immediately BEFORE any Act A edit) and the live tree, each side
cross-checked against THAT TREE'S OWN data/expected_boot.json. This script retypes nothing.

THE ONE ADAPTATION THAT MATTERS — THE CHAIN ASSERTION.

The R23 seat's script asserted `register tail destination.board == this entry's source.board`. That
assertion would FALSELY HALT here, and copying it unexamined would have been the wrong move. The tail
(entry 9) ends at `1d5c9f7a`; this entry's source is `7a3f4fe2`. The gap is the R23 ROUND ADVANCE,
which moved the board legitimately and gets NO register entry, because the register records
OUT-OF-ROUND transitions only.

This is not novel: the register already contains two such gaps — entry 4 (`827fb1fd … 6e724cca`) and
entry 6 (`4b448a82 … 88ce647f`). The R23 seat's strict assertion held only because the sheet re-cut
followed the D8 adoption with no round in between.

The gap spans BOTH legs, not just the board: the R23 advance also applied scores, so the store moved
cc02567f -> b745002e across it. (A first draft of this script asserted store-continuity, carried over
from the R23 seat's version, and it HALTED here correctly. The assertion was wrong, not the tree.)

So the chain is asserted in the form that is actually TRUE and still load-bearing: the gap is CLOSED
BY EVIDENCE rather than waved through. A SINGLE `ui/data/movers.js` round report must bridge BOTH
legs — `board_md5_before/after` == (tail destination board, this entry's source board) AND
`source_store_md5_before/after` == (tail destination store, this entry's source store). One report
naming both transitions identifies the round advance that closes the gap. A gap an independent record
can close is a gap; one that nothing can close is a broken chain, and this script halts on it.

This entry's own transition, by contrast, moves the store not at all: board is the ONLY one of eleven
identities it moves.

APPEND-ONLY. Every prior entry preserved byte-verbatim. The file round-trips at json indent=1,
asserted before AND after. The top-level present-lens baseline is asserted UNMOVED.

  python3 append_f5_transition.py <repo_root> [--dry-run]
"""
import json, os, sys

M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lineage_measured.json')))
S, D = M['source'], M['destination']
BOUNDARY = ["23", "the-f5-rounding-20-8"]

ENTRY = {
    "_doc": (
        "OUT-OF-ROUND PRESENTATION-CONSISTENCY REPAIR (THE F5 ROUNDING ACT, 2026-08-20; authority "
        "docs/runbooks/F5_OFFBYONE_DIAGNOSIS.md, executed on the owner word \"Launch the ready items "
        "please\"). THE DEFECT: a double-rounding artifact at the F5 seal boundary. `draft` and `mech` "
        "were each rounded to an integer independently, and the TOTAL was rounded independently AGAIN "
        "from the unrounded sum, with no assertion that the triple closed. round(a)+round(b) and "
        "round(a+b) may differ by 1 and on the ORDER 29 curve head they did — draft .5606 and mech .7109 "
        "both rounded UP (+0.7285) while the sum's own .2715 rounded DOWN — so the board stated the SAME "
        "quantity twice, by two conventions, 56773 beside 56772: three times over on the board (_meta, "
        "league, draftAssetTotals) and once more in the sealed file. The code defect is OLDER than the "
        "symptom: the three-independent-roundings pattern dates from the seal's creation on 2026-07-18 "
        "and stayed invisible for three seals purely by luck of the fractional parts. Nothing broke on "
        "08-13; a latent defect became observable. THE FIX: one rounding decision, at one boundary. The "
        "PARTS are the primitive and the integer total is DEFINITIONALLY their sum, never rounded a "
        "third time. THE DECLARED LAYER MOVES 56772 -> 56773. NO MONEY MOVES: the per-club allocation "
        "reads the UNROUNDED floats, so all 804 players' v/vM2/vM1/vP1/vP2 and all 198 back-history rows "
        "are BYTE-IDENTICAL across this transition, and the PICK 1 numeraire is unmoved at 3,000. The "
        "complete board diff is TEN FIELDS, all of them in the report-only F5 lens block: "
        "f5_entrant_layer_pvc x2 lenses, phantomTotals._meta.entrant_layer_pvc, the seal id, and league "
        "delta / entrantValue / withPhantom at each of the two forward lenses. Lens 0 — the balanced "
        "board — is UNMOVED at 692,296, the k=0 zero-phantom invariant. TWO GUARDS THAT COULD NOT FAIL "
        "WERE MADE REAL: the #306 L7 HALT compared the board's round(sum) against the seal's round(sum), "
        "the same convention on both sides, and was structurally blind to this class; and "
        "`reconciled_to_f5` was an algebraic TAUTOLOGY, True for any inputs, which is why it printed PASS "
        "on the very board whose strengthened cross-check was FAILing. Both now close against the seal's "
        "own total, and the seal writer asserts its triple closes so it can never go latent again. THE "
        "SEAL MOVES cbb7c431 -> ccc26a9e with entrant_pvc.total 56772 -> 56773 as its ONLY changed field: "
        "the occupancy COUNTS and the provenance STAMP are byte-identical, nothing was re-measured and "
        "nothing was re-stamped. A literal re-run of seal_structure.py was REFUSED because it would have "
        "restamped store_md5, board_balanced_md5 and curve_file_md5 and re-counted against a store that "
        "has moved three times — a RE-COUNT, which is not what was ruled. THE BOARD MOVES 7a3f4fe2 -> "
        "c97a4d9f. ENGINE_HEAD IS UNMOVED at 1867e953 and that is correct: this act edits "
        "engine/rl_after/rl_export.py, the EXPORTER, which no identity pin tracks; the valuation engine "
        "is untouched, which is exactly why no price moves. The STORE DOES NOT MOVE (b745002e both "
        "sides), no round is applied and the round pin stays at 23. config_sha256, rl_model, fv, "
        "register, v0surf and balanced_board_md5 are all UNMOVED — the board is the ONLY identity this "
        "transition moves, which is the smallest move any entry in this register records. Because this "
        "is an out-of-round move, the standing owner rule of 2026-07-28 writes a history column at the "
        "point: `the-f5-rounding-20-8`, registered in the value / rank / pos_rank histories from the new "
        "board (804 points each) by the out_of_round_column writer of record — and MEASURED there, 804 of "
        "804 players carry the same value at that column as at round 23, so the history itself records "
        "that this act moved no player value. It is the FIRST column written under the repaired "
        "chronological sort (commit 4c3dedd), stamped with an explicit seq rather than winning an "
        "alphabetical race. Two consumers go green as a consequence: invariant_proof.py's per-push lane "
        "26/28 -> 28/28, and the identical strengthened assertion in r15_ladder_survival_proof.py. The "
        "book is NOT re-sealed by this act, and data/book_stable_seal.json is untouched."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["THE_F5_ROUNDING_2026-08-20_launch_the_ready_items"],
    "owner_ruling": (
        "Owner word 2026-08-20, VERBATIM: \"Launch the ready items please\" — given in chat and carried "
        "to this seat in its execution brief, which names THE F5 ROUNDING ACT as one of two "
        "post-R23-eligible ready items and names docs/runbooks/F5_OFFBYONE_DIAGNOSIS.md as its "
        "AUTHORITY, with the declared move 56772 -> 56773 stated in the brief itself. Per the 5babe71 "
        "precedent this entry RECORDS an approval that already exists in the owner's own words; it does "
        "not create one. The runbook's own sequencing note asked for exactly this shape: \"Land it as "
        "its own isolated act, before or after R23, with its own prereg.\""
    ),
    "authority": (
        "Luke McAlister (owner) — sole STOP-1/STOP-2/merge authority; the word given directly in chat "
        "2026-08-20 and carried to this seat in its execution brief; written by the F5 engine seat (no "
        "interpretive authority)."
    ),
    "applies_to": {"bundle": "ui/data/movers.js", "boundary": BOUNDARY},
    "source": {k: S[k] for k in ("release_version", "board", "store", "rl_model", "engine_head", "fv",
                                 "config", "register", "balanced_board_md5", "v0surf", "as_of_round")},
    "destination": {k: D[k] for k in ("release_version", "board", "store", "rl_model", "engine_head", "fv",
                                      "config", "register", "balanced_board_md5", "v0surf", "as_of_round")},
    "moved_by_transition": M["moved"],
    "unchanged_across_transition": M["unchanged"],
    "invariants": {
        "store_unmoved_by_transition": D["store"],
        "config_unmoved_by_transition": D["config"],
        "engine_head_unmoved_by_transition": D["engine_head"],
        "round_held": "as_of_round 23 on both sides; no round applied, no store written",
        "no_value_moved": "804 of 804 active rows byte-identical (v/vM2/vM1/vP1/vP2); 198 of 198 back "
                          "rows byte-identical; measured by full recursive diff of the control build "
                          "against the F5 build, docs/evidence/f5_and_sort_2026-08-20/06_f5_builds.txt",
        "k0_invariant": "phantomTotals.league['0'] byte-unmoved; balanced board total 692,296",
        "numeraire": "PICK 1 = 3000, unmoved",
        "seal": "cbb7c431 -> ccc26a9e; entrant_pvc.total 56772 -> 56773 is the ONLY changed field; "
                "occupancy counts and provenance stamp byte-identical",
        "book_reseal": "NONE — data/book_stable_seal.json untouched; the full book re-seal remains "
                       "owner-pending per docs/evidence/landing_prep_2026-08-20/RESEAL_HALT.md",
    },
    "_chain_note": (
        "This entry's source board 7a3f4fe2 is NOT the register tail's destination 1d5c9f7a. The gap is "
        "the R23 ROUND ADVANCE, which moved the board legitimately and gets no register entry because "
        "this register records OUT-OF-ROUND transitions only. The gap is closed by an independent "
        "record rather than waved through: ui/data/movers.js's R23 report carries board_md5_before "
        "1d5c9f7a and board_md5_after 7a3f4fe2, naming exactly that advance. Two prior entries have the "
        "same shape — entry 4 (827fb1fd ... 6e724cca) and entry 6 (4b448a82 ... 88ce647f) — so this is "
        "the register's normal behaviour, not an exception carved for this act. The STORE is continuous "
        "and unmoved across both the gap and this transition."
    ),
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted. Every `source` identity was re-hashed from the "
        "committed tree at 2991740 — the commit immediately before any Act A edit — board and store by "
        "md5 of data/rl_build/rl_app_data.json and engine/rl_after/rl_model_data.json, engine_head and "
        "rl_model by md5 of engine/rl_after/_merged_recover.py and engine/rl_after/rl_model.py, register "
        "by md5 of LTI_REGISTER.md, v0surf by md5 of data/v0surf.pkl, balanced_board_md5 from "
        "engine/rl_after/ingestion/sibling_repin_state.json — and each agrees with that tree's own "
        "data/expected_boot.json. Every `destination` identity was re-hashed the same way from the live "
        "tree and agrees with the landed data/expected_boot.json; config and fv were additionally "
        "RE-MEASURED on the live side by config_manifest.manifest_hash and fv_provenance.fv_identity "
        "rather than read from the manifest. EXACTLY ONE identity of eleven moved: board."
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
            raise SystemExit("HALT: an existing record already declares destination.board %s (ruling %r)"
                             % (dest_board, e.get("owner_ruling_id")))

    # ---- THE CHAIN, ASSERTED IN THE FORM THAT IS TRUE (see the module docstring) -----------------
    # The gap spans BOTH board and store: the R23 round advance moved the board AND applied scores.
    # Both legs must be bridged BY THE SAME round report, or this is a broken chain and not a gap.
    prev_dest = (reg[-1].get("destination") or {}) if reg else {}
    tail_board, tail_store = str(prev_dest.get("board")), str(prev_dest.get("store"))
    src_board, src_store = ENTRY["source"]["board"], ENTRY["source"]["store"]
    if (tail_board, tail_store) == (src_board, src_store):
        print("chain OK: register tail destination == this entry's source on both board and store")
    else:
        mv = os.path.join(root, "ui", "data", "movers.js")
        txt = open(mv).read(); b = json.loads(txt[txt.index('{'):txt.rindex('}') + 1])
        bridge = next((r for r in sorted(b.get("reports", {}), key=int)
                       if b["reports"][r].get("board_md5_before") == tail_board
                       and b["reports"][r].get("board_md5_after") == src_board
                       and b["reports"][r].get("source_store_md5_before") == tail_store
                       and b["reports"][r].get("source_store_md5_after") == src_store), None)
        if bridge is None:
            raise SystemExit(
                "HALT: register tail destination (board %s / store %s) != this entry's source "
                "(board %s / store %s), and NO SINGLE movers round report bridges BOTH legs. That is a "
                "broken chain, not a gap." % (tail_board, tail_store, src_board, src_store))
        print("chain GAP, CLOSED BY EVIDENCE — bridged by the ROUND %s ADVANCE:" % bridge)
        print("   board  %s -> %s   (movers report %s board_md5_before/after)"
              % (tail_board[:8], src_board[:8], bridge))
        print("   store  %s -> %s   (movers report %s source_store_md5_before/after)"
              % (tail_store[:8], src_store[:8], bridge))
        print("   A round advance moves both and gets no register entry — this register records "
              "OUT-OF-ROUND transitions only. Precedent: entries 4 and 6 have the same shape.")
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
        back = open(p, "rb").read(); d2 = json.loads(back)
        if json.dumps(d2, indent=1).encode() != back:
            raise SystemExit("HALT: the written file does not round-trip at indent=1")
        if json.dumps(d2["release_transition_register"][:-1]) != before:
            raise SystemExit("HALT: re-read shows a prior entry changed")
        print("re-read OK: round-trips at indent=1; prior entries still byte-verbatim.")
    print("appended entry %d; %d -> %d bytes%s" % (len(reg), len(raw), len(out), " (dry run)" if dry else ""))
    print("  source      board %s  store %s  engine_head %s" % (S["board"], S["store"], S["engine_head"]))
    print("  destination board %s  store %s  engine_head %s" % (D["board"], D["store"], D["engine_head"]))
    print("  MOVED by this transition: %s   (of %d identities)" % (M["moved"], len(M["moved"]) + len(M["unchanged"])))


if __name__ == "__main__":
    main()
