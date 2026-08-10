#!/usr/bin/env python3
"""APPEND the never-rises-restore out-of-round transition to data/release_lineage.json.

WHY. The board moves outside a round (a672ed3a -> 4b448a82 at round 22), so the standing owner rule
requires an out-of-round history column, and round_movers.model_changes() LABELS that column from the
append-only `release_transition_register`. Per the register's own law (entry 2's _doc): "an APPENDED
entry is the shape the validator's own law prescribes for a future out-of-round board move." The DOB
courier landing of the same day walked this identical lane and recorded it.

WHAT THIS RECORD DOES AND DOES NOT DO. It RECORDS an approval that already exists in the owner's own
words; it does not create one. The words are quoted verbatim below and cited to their comment on
issue #334. A label never blocks a comparison (ui/app/movers.js) — this entry exists so the Movers
dropdown can name the boundary honestly.

APPEND-ONLY. Every prior entry is preserved byte-verbatim; nothing is rewritten. The file round-trips
at json indent=1 with no trailing newline, which this script asserts before and after.

Usage:  python3 append_transition.py <repo_root> [--dry-run]
"""
import json
import os
import sys

ENTRY = {
    "_doc": (
        "OUT-OF-ROUND NEVER-RISES RESTORE (#334 rulings 1.1 + 1.2, 2026-08-10). The owner's V0 law "
        "(ledger R12: a year-zero value curve never rises as the pick number rises) was lost by "
        "omission at the #306 anchored-lens landing on 2026-08-05 and is restored here: within each "
        "(position x draft age) profile the composed lens curve is projected to non-increasing over "
        "the log-pick grid by isotonic regression — the deleted _iso_dec step's exact behaviour — "
        "after the lens multiply and after the neutrality fixed point. The frozen V0 pick-curve "
        "surface is re-cut through the declared refit lane because the projection changes it. "
        "Appended, not substituted: every prior entry is preserved verbatim. THE BOARD MOVES, and "
        "small: 439 rising steps inside picks 1-64 fall to 0 across all 90 position x draft-age "
        "profiles (2779 -> 0 over the full 1-90 grid); 82 of 804 players' year-zero value moves "
        "(47 down, 35 up — the merge), 16 displayed board prices move (9 down, 7 up; largest cut -18 "
        "Xavier Taylor, largest rise +24 Daniel Annable), board total 761587 -> 761574 (-13, "
        "-0.0017%), PICK 1 numeraire unmoved at 3000. The store is UNCHANGED: no store write, no "
        "model level, no dial, no teaching. rl_model, fv, config and register are byte-unchanged "
        "across this transition; engine_head moves because the restored step and the D14 gate wiring "
        "live in it."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["G1_NEVER_RISES_2026-08-10_restore_and_gates"],
    "owner_ruling": (
        "Issue #334, comment 5235660463, 2026-08-10, the owner's eleven decisions as filed. "
        "Ruling 1.1 RESTORE — YES, his words verbatim: \"Yes, restore... Realistically, each "
        "position should have a 1-64 curve I would have thought. Their own ones.\" — with the "
        "disposition recorded in the same comment that the restore is the old law's exact method, "
        "the isotonic merge within each position x draft-age profile, and that \"Every moved player "
        "[is] enumerated\". Ruling 1.2 GATES — YES: \"The gate suite wired into the standing "
        "gated-build path (every board build runs it, halts on failure) plus a new surface-level "
        "scan (all cells x picks, not just rostered players).\" Ruling 1.3 (the ledger move) is HELD "
        "and nothing in this transition touches the ledger."
    ),
    "authority": "Luke McAlister (owner) - sole merge authority; relayed by the seam on #334",
    "applies_to": {
        "bundle": "ui/data/movers.js",
        "boundary": ["22", "g1-never-rises-10-8"],
    },
    "source": {
        "release_version": "v2.11-final-rc1-PROVISIONAL",
        "board": "a672ed3a6a1426a262d932f844e8f87b",
        "store": "d9a24282357cf3083b1640466e3ecd83",
        "rl_model": "33f940735281a07e3b6ca19f31bf2ea6",
        "engine_head": "8f0e3eb1b29fee6b2defa0a5cfd7ebec",
        "fv": "d920557ef21d0eec6434853b07869dd4c0b98f64e99e79ecbb8ee54c704ecf4a",
        "config": "cef06fd6250be86804f7d4432fdef8969070f9d9fc938f3e3473547c5b4b4739",
        "register": "652d83e87780e415a01a2de6d8b3cc57",
        "balanced_board_md5": "a970c19cd56ea184e9ca5eb02211d21b",
        "v0surf": "5a03c9ea3e9a32e6cc6e1ffec5293685",
        "as_of_round": 22,
    },
    "destination": {
        "release_version": "v2.11-final-rc1-PROVISIONAL",
        "board": "4b448a821f54180182637983f7a26a9d",
        "store": "d9a24282357cf3083b1640466e3ecd83",
        "rl_model": "33f940735281a07e3b6ca19f31bf2ea6",
        "engine_head": "c0a7e969fdd9327fc0b043af14a4bfc6",
        "fv": "d920557ef21d0eec6434853b07869dd4c0b98f64e99e79ecbb8ee54c704ecf4a",
        "config": "cef06fd6250be86804f7d4432fdef8969070f9d9fc938f3e3473547c5b4b4739",
        "register": "652d83e87780e415a01a2de6d8b3cc57",
        "balanced_board_md5": "234c3414fa001bd9538deb6668e169f0",
        "v0surf": "fbc5b39387b2b135284a2e157f46c810",
        "as_of_round": 22,
    },
    "moved_by_transition": ["balanced_board_md5", "board", "engine_head", "v0surf"],
    "unchanged_across_transition": ["config", "fv", "register", "rl_model", "store"],
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted: every identity above was read off the built "
        "tree. v0surf is carried here as an explicit member because it is the artifact this act "
        "re-cut and it is not part of the schema's usual identity set — a surface move that did not "
        "appear in the transition record would be exactly the silent change the freeze exists to "
        "prevent. THE CLEAN-BOX CONTROL RAN FIRST (N35): on the build container the UNPATCHED engine "
        "refit reproduced the outgoing surface pin 5a03c9ea byte-exact and the unpatched board build "
        "reproduced the outgoing board a672ed3a byte-exact, which is what isolates this transition's "
        "82 v0 movers and 16 price movers to the restored law alone. Every moved player is "
        "enumerated at docs/evidence/g1_never_rises_2026-08-10/movers.csv, per the owner's ruling."
    ),
}


def main():
    root = os.path.abspath(sys.argv[1])
    dry = "--dry-run" in sys.argv
    p = os.path.join(root, "data", "release_lineage.json")
    raw = open(p, "rb").read()
    d = json.loads(raw)
    if (json.dumps(d, indent=1)).encode() != raw:
        raise SystemExit("HALT: release_lineage.json does not round-trip at indent=1; refusing to reformat it")

    reg = d.get("release_transition_register")
    if not isinstance(reg, list):
        raise SystemExit("HALT: release_transition_register missing or not a list")
    before = json.dumps(reg)
    for e in reg:
        if isinstance(e, dict) and e.get("applies_to", {}).get("boundary") == ENTRY["applies_to"]["boundary"]:
            print("already present — no-op")
            return
    reg.append(ENTRY)
    if json.dumps(reg[:-1]) != before:
        raise SystemExit("HALT: a prior register entry changed; append-only violated")

    out = json.dumps(d, indent=1).encode()
    if not dry:
        open(p, "wb").write(out)
    print("appended entry %d; %d -> %d bytes%s"
          % (len(reg), len(raw), len(out), " (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
