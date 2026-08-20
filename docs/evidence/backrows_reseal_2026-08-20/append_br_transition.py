#!/usr/bin/env python3
"""APPEND THE BACK-ROWS AGE_REF REPAIR's out-of-round transition to data/release_lineage.json.

ADAPTED FROM docs/evidence/f5_and_sort_2026-08-20/append_f5_transition.py — itself the R23/D8
adaptation of the landing tail's template. The mechanics are carried verbatim; what is re-pointed is
this act's facts.

MEASURED, NOT TYPED. Every identity is read from lineage_measured.json, produced by measure_lineage.py
by re-hashing the committed tree at 15729e7 (the PREREG commit, immediately before any Act A edit) and
the live tree, each side cross-checked against THAT TREE'S OWN data/expected_boot.json. This script
retypes nothing.

THE CHAIN ASSERTION IS CARRIED IN THE FORM THE F5 SEAT ESTABLISHED — tail-destination == source on
BOTH board and store, or else a SINGLE movers round report must bridge both legs. Here the strict form
is expected to hold: the F5 act's entry is the register tail, its destination is c97a4d9f, and that is
exactly this entry's source. If it does not hold, the script halts rather than waving it through.

THIS ENTRY MOVES TWO IDENTITIES OF ELEVEN — board and balanced_board_md5 — and that second one is the
difference from the F5 entry. It is expected and prereged (P9): the cured residue is present under the
balanced posture too, and larger there (RL_LEGE=0 leaves BASE_REF=AGE_REF=2028 entering the back loop),
so the sibling board moves with the canonical one. It was moved by its own writer of record
(sibling_repin reconcile, build-and-compare), never by a value typed anywhere.

APPEND-ONLY. Every prior entry preserved byte-verbatim. The file round-trips at json indent=1,
asserted before AND after. The top-level present-lens baseline is asserted UNMOVED.

  python3 append_br_transition.py <repo_root> [--dry-run]
"""
import json, os, sys

M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lineage_measured.json')))
S, D = M['source'], M['destination']
BOUNDARY = ["23", "the-backrows-repair-20-8"]

ENTRY = {
    "_doc": (
        "OUT-OF-ROUND VALUATION REPAIR OF THE BACK-HISTORY BASIS (THE BACK-ROWS AGE_REF REPAIR, "
        "2026-08-20; authority docs/evidence/backrows_reseal_2026-08-20/01_PREREG_BACKROWS.md, "
        "executed on the owner word \"Let's fix it now please.\"). THIS IS THE OWNER RULING THE H3 "
        "SEAT ASKED FOR. THE DEFECT: entering rl_export.py's `back_extra` loop the ambient engine clock "
        "was BASE_REF=2026 but AGE_REF=2028 — left standing by the players loop's last forward call "
        "ev(_p, 2028) — and these rows do not traverse the _b6_core/price6 re-pin that would correct it. "
        "A retired row's recalled price therefore depended on the fact that 804 OTHER rows had just been "
        "priced forward to 2028: a price on an accident, not on a basis. It is the same defect CLASS the "
        "H3 repair (register v792) cured on the ACTIVE value loop; the identical statement in this loop "
        "was prereged, applied and MEASURED at H3 time, moved 26 of the 198 back rows, fired H3's "
        "falsifier F1, and was REVERTED and REPORTED because curing it is a valuation act on the board "
        "of record that no owner word then covered. That word was given on 2026-08-20. WHERE THE RESIDUE "
        "LIVED, MEASURED NOT ASSUMED: the EXPORT PATH, not a cached input — back_extra rows are priced "
        "inline on every build from _ev(_p, 2026), nothing caches a back-row value in a sidecar, a store "
        "field or a pickle, and the only post-loop writer (owner_overrides) adds a display block and "
        "never touches `v`. THE FIX IS THEREFORE ONE STATEMENT — g['BASE_REF']=g['AGE_REF']=2026; "
        "g['_pe_clear']() at the top of that loop — and from it EVERY BARE BUILD produces the corrected "
        "back rows FOREVER. No number was hand-edited, no expression, constant, threshold or law was "
        "touched. WHAT MOVED: the complete recursive board diff is 131 leaves — 125 of them the 25 moved "
        "back rows x their five value fields, and 6 of them lensConservation, which aggregates over "
        "those rows. NOTHING ELSE. All 804 ACTIVE rows are BYTE-IDENTICAL (v/vM2/vM1/vP1/vP2 and every "
        "other field), the active total is HELD at 692,296, PICK 1 = 3,000 is unmoved, the F5 entrant "
        "layer stays 56,773 with seal ccc26a9e, and lens 0 — the k=0 zero-phantom invariant — is HELD. "
        "No player price, club total, pick price or numeraire moves. EXACTLY 25 of 198 back-history rows "
        "move, ALL DOWN, aggregating 772 -> 700 (-72) with the whole 198-row back section 3,190 -> 3,118; "
        "lensConservation lens -1 755,307 -> 755,235 and lens -2 782,108 -> 782,036, each -72. The mover "
        "set matches the read-only probe's list (docs/evidence/f5_and_sort_2026-08-20/"
        "14_actc_ageref_probe.txt) EXACTLY by key, name, current and corrected value — parsed from the "
        "committed probe file rather than retyped — including the H3-era named examples charlie-dean "
        "41->39 and jacob-bauer 29->27. THE FALSIFIER THAT MATTERED IS MET BYTE-EXACT: the repaired bare "
        "build reproduces the probe's fixed-clock rebuild 68be10c7 exactly, dev and canonical agreeing, "
        "and a CONTROL build of the unmodified tree first reproduced the live board c97a4d9f exactly, so "
        "every leaf of the diff is attributable to the one statement. THE BOARD MOVES c97a4d9f -> "
        "68be10c7 AND THE BALANCED BOARD MOVES 3970156c -> 556ad70d: the residue is present under the "
        "balanced posture too and larger there (RL_LEGE=0 leaves BASE_REF=AGE_REF=2028 entering the "
        "loop), so the sibling was rebuilt and re-pinned by its own writer of record, build-and-compare; "
        "its ACTIVE vector is unmoved (sum_v 692,296, sheezel 10,428, both identical to the pre-act "
        "sibling state). ENGINE_HEAD IS UNMOVED at 1867e953 and that is correct: this act edits "
        "engine/rl_after/rl_export.py, the EXPORTER, which no identity pin tracks; the valuation engine "
        "is untouched, which is why no active price moves. The STORE DOES NOT MOVE (b745002e both "
        "sides), no round is applied and the round pin stays at 23. config_sha256, rl_model, fv, register "
        "and v0surf are all UNMOVED. Because this is an out-of-round move, the standing owner rule of "
        "2026-07-28 writes a history column at the point: `the-backrows-repair-20-8`, registered from "
        "the new board by the out_of_round_column writer of record, seq 1 under the repaired "
        "chronological sort. MEASURED THERE: 804 of 804 ACTIVE players carry the same value at that "
        "column as at round 23 — TRUE, not a concealment, because the value/rank/pos_rank histories "
        "carry active rows only and the movement is entirely in the back section, which they do not "
        "track; the column LABEL says so. invariant_proof per-push lane: 28/28 PASS on the new board. "
        "STILL REFERRED, NOT SMUGGLED IN: the strictly larger in-ev() structural cure "
        "(H3_DIAGNOSIS.md §6 q2/q3) — making ev(p,Y) pin its own clock before ANY evaluation — is NOT "
        "done here. This removes the EXPOSURE on this loop; the ambient-state sensitivity of ev() "
        "remains a modernisation item with its own prereg to write. The book re-seal is NOT part of this "
        "entry: it is the owner's separate word (\"And I'll re seal once that is done\") and follows as "
        "its own act, so that the book signs the CORRECTED board."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["THE_BACKROWS_AGE_REF_REPAIR_2026-08-20_lets_fix_it_now_please"],
    "owner_ruling": (
        "Owner word 2026-08-20, VERBATIM: \"Let's fix it now please.\" — given in chat and carried to "
        "this seat in its execution brief, which names the back-rows AGE_REF repair as ACT A and "
        "docs/evidence/f5_and_sort_2026-08-20/14_actc_ageref_probe.txt as the measurement to make "
        "shipped. It is the answer to the question H3_REPAIR_RESULT.md §4 referred: the back-history "
        "AGE_REF residue needed an owner ruling of its own because curing it moves the board of record. "
        "Per the 5babe71 precedent this entry RECORDS an approval that already exists in the owner's own "
        "words; it does not create one. The owner's second word of the same session — \"And I'll re seal "
        "once that is done\" — sequences the book re-seal AFTER this act and is recorded in the act that "
        "carries it, not here."
    ),
    "authority": (
        "Luke McAlister (owner) — sole STOP-1/STOP-2/merge authority; the word given directly in chat "
        "2026-08-20 and carried to this seat in its execution brief; written by the back-rows engine "
        "seat (no interpretive authority)."
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
        "no_active_value_moved": "804 of 804 active rows byte-identical (v/vM2/vM1/vP1/vP2 and every "
                                 "other field); active total HELD at 692,296; measured by full "
                                 "recursive diff of the control build against the repaired build, "
                                 "docs/evidence/backrows_reseal_2026-08-20/03_builds_and_proofs.txt",
        "back_rows_moved": "EXACTLY 25 of 198, ALL DOWN; movers aggregate 772 -> 700 (-72); whole back "
                           "section 3,190 -> 3,118; the mover set equals the probe's list exactly by "
                           "key, name, current and corrected value",
        "lens_conservation": "lens -1 755,307 -> 755,235 and lens -2 782,108 -> 782,036, each -72",
        "k0_invariant": "phantomTotals.league['0'] byte-unmoved; balanced board total 692,296",
        "numeraire": "PICK 1 = 3000, unmoved",
        "f5_layer": "entrant layer HELD at 56,773; seal ccc26a9e HELD; this act does not touch it",
        "byte_exact_reproduction": "the repaired bare build == the read-only probe's fixed-clock "
                                   "rebuild 68be10c7, byte-exact, dev and canonical agreeing",
        "book_reseal": "NOT IN THIS ENTRY — data/book_stable_seal.json is untouched by this act and is "
                       "re-sealed by the owner's separate word in its own act, so the book signs the "
                       "CORRECTED board.",
    },
    "_chain_note": (
        "The register tail is the F5 rounding act's entry, whose destination board c97a4d9f and store "
        "b745002e are EXACTLY this entry's source on both legs. The chain is continuous with no gap, "
        "which is the strict form the append instrument asserts first; no bridging evidence was needed."
    ),
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted, by "
        "docs/evidence/backrows_reseal_2026-08-20/measure_lineage.py. Every `source` identity was "
        "re-hashed out of git from the committed tree at 15729e7 — the PREREG commit, immediately "
        "before any Act A edit — board and store by md5 of data/rl_build/rl_app_data.json and "
        "engine/rl_after/rl_model_data.json, engine_head and rl_model by md5 of "
        "engine/rl_after/_merged_recover.py and engine/rl_after/rl_model.py, register by md5 of "
        "LTI_REGISTER.md, v0surf by md5 of data/v0surf.pkl, balanced_board_md5 from "
        "engine/rl_after/ingestion/sibling_repin_state.json — and each agrees with that tree's own "
        "data/expected_boot.json. Every `destination` identity was measured the same way from the live "
        "tree and agrees with the landed data/expected_boot.json; config and fv were additionally "
        "RE-MEASURED on the live side by config_manifest.manifest_hash and fv_provenance.fv_identity "
        "rather than read from the manifest. EXACTLY TWO identities of eleven moved: board and "
        "balanced_board_md5."
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

    # ---- THE CHAIN, ASSERTED IN THE FORM THAT IS TRUE --------------------------------------------
    prev_dest = (reg[-1].get("destination") or {}) if reg else {}
    tail_board, tail_store = str(prev_dest.get("board")), str(prev_dest.get("store"))
    src_board, src_store = ENTRY["source"]["board"], ENTRY["source"]["store"]
    if (tail_board, tail_store) == (src_board, src_store):
        print("chain OK: register tail destination == this entry's source on both board and store")
        print("   board  %s   store %s" % (src_board, src_store))
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
        print("chain GAP, CLOSED BY EVIDENCE — bridged by the ROUND %s ADVANCE" % bridge)
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
    print("  source      board %s  store %s  balanced %s" % (S["board"], S["store"], S["balanced_board_md5"]))
    print("  destination board %s  store %s  balanced %s" % (D["board"], D["store"], D["balanced_board_md5"]))
    print("  MOVED by this transition: %s   (of %d identities)" % (M["moved"], len(M["moved"]) + len(M["unchanged"])))


if __name__ == "__main__":
    main()
