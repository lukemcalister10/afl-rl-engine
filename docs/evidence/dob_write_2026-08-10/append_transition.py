#!/usr/bin/env python3
"""APPEND the DOB-courier out-of-round transition to data/release_lineage.json.

WHY. The board moves outside a round (6e724cca -> a672ed3a at round 22), so the standing owner rule
requires an out-of-round history column, and round_movers.model_changes() LABELS that column from the
append-only `release_transition_register`. Per the register's own law (entry 2's _doc): "an APPENDED
entry is the shape the validator's own law prescribes for a future out-of-round board move."

WHAT THIS RECORD DOES AND DOES NOT DO. It RECORDS an approval that already exists in the owner's own
words; it does not create one. Both words are quoted verbatim below and cited to their comments on
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
        "OUT-OF-ROUND DOB COURIER LANDING + v0surf RE-CUT (#334, 2026-08-10). The 302 staged "
        "birthdates land in the store (the #290 runbook's section-5 courier act, which was specified "
        "and never fired), and the frozen V0 pick-curve surface is re-cut on the owner's authorisation "
        "because the real birth data changes its config signature. Appended, not substituted: every "
        "prior entry is preserved verbatim. THE BOARD MOVES, but barely: 6 of 804 players move by "
        "exactly +/-1 SCAR (William McCabe, Mitchell Marsh, Maxwell King, Luke Urquhart and Isaac "
        "Cumming +1; Jevan Phillipou -1), board total 761583 -> 761587, backward board 0 movers, PICK 1 "
        "numeraire unmoved at 3000. The mechanism: _v0surf_sig hashes every historical national "
        "draftee's DRAFT AGE, which reads _by; with no birthdate the engine assumed draft age 18, and "
        "14 of the 302 are mature-age draftees inside picks 1-64 whose real draft ages are 19-22, so "
        "they move across the surface fit's 18/19 split. No model, curve law, dial or config value "
        "changed: rl_model, engine_head, fv, config and register are all byte-unchanged across this "
        "transition."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["DOB_COURIER_2026-08-10_refit_authorised"],
    "owner_ruling": (
        "Two words on issue #334, both quoted verbatim. 2026-08-10, comment 5235574982, owner: "
        "\"Ruory Kirkby - 4/2/86. Tim Looby - 2/9/87. Write the birthdates.\" — the write, including "
        "the two discrepant rows he settled himself. 2026-08-10, comment 5235816134, owner: "
        "\"Authorise the refit.\" — given after the build seat HALTED on the v0surf frozen-signature "
        "guard and reported the measured board impact, authorising the surface re-cut that carries "
        "the birthdates onto the board."
    ),
    "authority": "Luke McAlister (owner) - sole merge authority; relayed by the seam on #334",
    "applies_to": {
        "bundle": "ui/data/movers.js",
        "boundary": ["22", "dob-courier-10-8"],
    },
    "source": {
        "release_version": "v2.11-final-rc1-PROVISIONAL",
        "board": "6e724cca2bb2fb118ff7ad6ed1f8a4b6",
        "store": "0dd6b4a01e16dabf8d3a388d8f8ac1f2",
        "rl_model": "33f940735281a07e3b6ca19f31bf2ea6",
        "engine_head": "8f0e3eb1b29fee6b2defa0a5cfd7ebec",
        "fv": "d920557ef21d0eec6434853b07869dd4c0b98f64e99e79ecbb8ee54c704ecf4a",
        "config": "cef06fd6250be86804f7d4432fdef8969070f9d9fc938f3e3473547c5b4b4739",
        "register": "652d83e87780e415a01a2de6d8b3cc57",
        "balanced_board_md5": "b4cc0b2b7e4fb0552e9457f2d249cf52",
        "v0surf": "d594dc034e86935b370c49b240a18370",
        "as_of_round": 22,
    },
    "destination": {
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
    "moved_by_transition": ["balanced_board_md5", "board", "store", "v0surf"],
    "unchanged_across_transition": ["config", "engine_head", "fv", "register", "rl_model"],
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted: every identity above was read off the landed "
        "tree. v0surf is carried here as an explicit member because it is the artifact this act "
        "re-cut and it is not part of the schema's usual identity set — a surface move that did not "
        "appear in the transition record would be exactly the silent change the freeze exists to "
        "prevent. The board was rebuilt from the landed store in a clean private workspace under the "
        "canonical gated recipe and reproduced a672ed3a; a refit on the UNWRITTEN store reproduced "
        "the outgoing board 6e724cca byte-exact, which is what isolates this transition's 6 movers "
        "to the birth data alone."
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
