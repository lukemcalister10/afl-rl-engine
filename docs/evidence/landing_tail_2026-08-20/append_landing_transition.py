#!/usr/bin/env python3
"""APPEND THE LANDING's out-of-round transition to data/release_lineage.json.

WHY. THE LANDING (main 463e53d, owner word "Land it.", 2026-08-20) moved the live board
88ce647f -> a05fe951 AND the store d9a24282 -> cb38ef11 outside a round, and appended no register
entry. Per this register's own law (entry [2]'s _doc, restated in the file's _doc): "an APPENDED
entry is the shape the validator's own law prescribes for a future out-of-round board move." Because
the entry was never written, the append-only chain still ends at the pre-landing store and every
out-of-round writer that extends it fails closed — which is exactly what
ui/tools/ownership_store_apply.append_transition did at T5 when the owner's ownership apply was run
(docs/evidence/landing_tail_2026-08-20/15_lineage_register_HALT_fork.txt).

WHAT THIS RECORD DOES AND DOES NOT DO. It RECORDS an approval that already exists in the owner's own
words; it does not create one (the 5babe71 precedent, verbatim). The word is quoted below and cited
to register v782, where the supervisor pen recorded it at the landing. The recording itself was put
to the owner as ruling R1 at register v786 and he ruled it be made. A label never blocks a comparison
(ui/app/movers.js) — this entry exists so the Movers dropdown can name the boundary honestly, and so
the store chain the out-of-round writers walk is continuous again.

THE BOUNDARY IS NEW, NOT STOLEN. round_movers.model_changes() keys the register by
`destination.board` and lets a LATER entry supersede an EARLIER one describing the same landing
board. No existing entry declares destination.board a05fe951 (the register's declared destination
boards are f2df6e0a, 827fb1fd, a672ed3a, 4b448a82, plus two entries that declare none), so this
entry creates that boundary's record rather than overwriting anyone's owner_ruling_id. Asserted by
this script before it writes.

MEASURED, NOT TYPED. Every identity in `source` was re-hashed from a checkout of 463e53d^ (the tree
immediately before the landing) and every identity in `destination` was re-hashed from the live tree;
both agree field-for-field with the accepted manifest data/expected_boot.json at their respective
commits. See 19_landing_lineage_identities.txt.

APPEND-ONLY. Every prior entry is preserved byte-verbatim; nothing is rewritten. The file round-trips
at json indent=1, which this script asserts before and after. The top-level present-lens baseline
(balanced_board_md5 06d8af60, release_version) is asserted UNMOVED.

Usage:  python3 append_landing_transition.py <repo_root> [--dry-run]
"""
import json
import os
import sys

ENTRY = {
    "_doc": (
        "OUT-OF-ROUND LANDING (THE LANDING, owner word \"Land it.\", 2026-08-20; main 463e53d). The "
        "campaign candidate line — ORDER 29 / ORDER 31-F and everything baked on it (f27482f) — "
        "replaces the live release. THE BOARD MOVES, and far from small: 88ce647f -> a05fe951, board "
        "total 752,429 -> 664,949 over the same 804 active rows, because the live board's unbounded "
        "~19% year-0->1 exploit is retired (the all-pool year-0->1 line moves -59.18% -> -5.99% "
        "PRIMARY, register v782). THE STORE MOVES WITH IT: d9a24282 -> cb38ef11, the store the "
        "candidate line was built on. This is an out-of-round move — no round was applied and the "
        "round pin stays at 22 — so the standing owner rule of 2026-07-28 writes a history column at "
        "the point as well: `the-landing-20-8`, registered in the value / rank / pos_rank histories "
        "from the landed board (804 points each) by "
        "docs/evidence/landing_tail_2026-08-20/register_landing_column.py. Appended, not substituted: "
        "every prior entry is preserved verbatim. rl_model, engine_head, fv, config and v0surf all "
        "move because the whole candidate line lands at once; the LTI register pin is byte-unchanged, "
        "and balanced_board_md5 does NOT move because the balanced/strict sibling layer was not re-run "
        "at the landing — that is honest, not an assertion of sameness, and it is the named open item "
        "the sibling_repin reconcile order owns (docs/evidence/landing_tail_2026-08-20/"
        "09_sibling_repin_verify.txt, 8 fails). NOTE ON THE BOARD CHAIN: this entry's `source` board "
        "88ce647f is the board that was actually live on main at 463e53d^, which is NOT the previous "
        "entry's destination board 4b448a82 — the live line moved 4b448a82 -> ... -> 88ce647f through "
        "the ORDER 9 / 20C / 23 / 25 adoption bakes, none of which appended a register entry. That "
        "gap is pre-existing, is NOT closed here, and is recorded rather than papered over; the STORE "
        "chain, which is what the out-of-round writers walk, IS continuous (d9a24282 -> cb38ef11)."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["THE_LANDING_2026-08-20_land_it"],
    "owner_ruling": (
        "THE LANDING, owner word 2026-08-20, VERBATIM: \"Land it.\" — recorded at "
        "docs/OPEN_ITEMS_REGISTER.md v782 (2026-08-20): \"THE LANDING. Owner word verbatim: \\\"Land "
        "it.\\\" — EXECUTED. main = 463e53d, a clean zero-conflict merge of land/order-29 f27482f "
        "(1,887 files); THE LIVE BOARD IS NOW a05fe951 / 664,949 / 804. The campaign board 88ce647f / "
        "752,429 — and its unbounded ~19% year-0->1 exploit — is RETIRED... PR #510 is MERGED AND "
        "CLOSED (auto-marked at the push, merged_by the owner's credential, 2026-08-20T02:24:39Z).\" "
        "THE RECORDING of that word in this register was itself put to the owner as ruling R1 at "
        "register v786 (2026-08-20) — \"append THE LANDING's lineage entry — board boundary, citing "
        "his v782 word (\\\"Land it.\\\", 2026-08-20) — which unblocks the apply\" — and he ruled it "
        "be made. Per the 5babe71 precedent this entry RECORDS an approval that already exists in his "
        "words; it does not create one."
    ),
    "authority": (
        "Luke McAlister (owner) - sole STOP-1/STOP-2/merge authority; the landing word relayed and "
        "recorded by the supervisor pen at register v782, the recording ruled at v786; written by the "
        "build seat (no interpretive authority)."
    ),
    "applies_to": {
        "bundle": "ui/data/movers.js",
        "boundary": ["22", "the-landing-20-8"],
    },
    "source": {
        "release_version": "v2.11-final-rc1-PROVISIONAL",
        "board": "88ce647f531030d8d2e094188b258191",
        "store": "d9a24282357cf3083b1640466e3ecd83",
        "rl_model": "e5eb5e4405c09eebef45a9db89f014bc",
        "engine_head": "3f1468e5468462ab789e49aace264c90",
        "fv": "2621b56a32805f15b5084a45f851e882d1a0c6cf9c4fc2512550d394760f7dc6",
        "config": "bf0121056ee4437f407c9af42fbb760c1f4fd2a1fa7bfb9e13cdd94450615672",
        "register": "652d83e87780e415a01a2de6d8b3cc57",
        "balanced_board_md5": "234c3414fa001bd9538deb6668e169f0",
        "v0surf": "fbc5b39387b2b135284a2e157f46c810",
        "as_of_round": 22,
    },
    "destination": {
        "release_version": "v2.11-final-rc1-PROVISIONAL",
        "board": "a05fe951f78482c70520480e184c80ec",
        "store": "cb38ef1171dcf20aae66ebf12682be0d",
        "rl_model": "6fe7c4155866d80e8045bed2d3bf2802",
        "engine_head": "5ac6780f3c4931edcaa527576bbdfb88",
        "fv": "6e9a370e5970c5aefa859858070f4c3420f0177b4698d6fac90bd08bf1780346",
        "config": "eed19a75f775aeafe4ee5ea4b3990667192d8f90389ad6b0e8318e91062d14c1",
        "register": "652d83e87780e415a01a2de6d8b3cc57",
        "balanced_board_md5": "234c3414fa001bd9538deb6668e169f0",
        "v0surf": "5dd34ca82735f5c8f021b1c7320df8f8",
        "as_of_round": 22,
    },
    "moved_by_transition": ["board", "config", "engine_head", "fv", "rl_model", "store", "v0surf"],
    "unchanged_across_transition": ["balanced_board_md5", "register"],
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted. Every `source` identity was re-hashed from a "
        "checkout of 463e53d^ — board and store by md5 of data/rl_build/rl_app_data.json and "
        "engine/rl_after/rl_model_data.json, engine_head and rl_model by md5 of "
        "engine/rl_after/_merged_recover.py and engine/rl_after/rl_model.py, config by "
        "config_manifest.manifest_hash, fv by fv_provenance.fv_identity over "
        "engine/forward_valuation, register by md5 of LTI_REGISTER.md, v0surf by md5 of "
        "data/v0surf.pkl — and each agrees with that commit's own data/expected_boot.json. Every "
        "`destination` identity was re-hashed the same way from the live tree and agrees with the "
        "landed data/expected_boot.json. balanced_board_md5 is listed UNCHANGED because it genuinely "
        "did not move: the sibling layer was not rebuilt at the landing, so 234c3414 is still the "
        "balanced sibling of the PRE-landing store+engine and is stale by design-gap, not by "
        "agreement. It is named here rather than silently re-stamped. Board totals were measured on "
        "the two board files directly: 804 rows / 752,429 -> 804 rows / 664,949."
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

    base_balanced = d.get("balanced_board_md5")
    base_version = d.get("release_version")

    reg = d.get("release_transition_register")
    if not isinstance(reg, list):
        raise SystemExit("HALT: release_transition_register missing or not a list")
    before = json.dumps(reg)
    for e in reg:
        if isinstance(e, dict) and e.get("applies_to", {}).get("boundary") == ENTRY["applies_to"]["boundary"]:
            print("already present — no-op")
            return

    # THE BOUNDARY MUST BE NEW. model_changes() keys by destination.board and a later entry supersedes
    # an earlier one on the same board — declaring a board another entry already declares would
    # silently steal its owner_ruling_id. Refuse rather than do that.
    dest_board = ENTRY["destination"]["board"]
    for e in [d.get("release_transition") or {}] + [e for e in reg if isinstance(e, dict)]:
        if (e.get("destination") or {}).get("board") == dest_board:
            raise SystemExit("HALT: an existing record already declares destination.board %s (ruling %r) "
                             "— appending would supersede it" % (dest_board, e.get("owner_ruling_id")))

    # The store chain must be continuous: this entry's source store must be the register tail's
    # destination store, which is precisely what ownership_store_apply.append_transition asserts.
    prev_dest = (reg[-1].get("destination") or {}) if reg else {}
    if str(prev_dest.get("store")) != ENTRY["source"]["store"]:
        raise SystemExit("HALT: register tail destination.store %s != this entry's source.store %s"
                         % (prev_dest.get("store"), ENTRY["source"]["store"]))

    reg.append(ENTRY)
    if json.dumps(reg[:-1]) != before:
        raise SystemExit("HALT: a prior register entry changed; append-only violated")
    if d.get("balanced_board_md5") != base_balanced or d.get("release_version") != base_version:
        raise SystemExit("HALT: release_lineage top-level present-lens baseline moved — it must never move")

    out = json.dumps(d, indent=1).encode()
    if not dry:
        open(p, "wb").write(out)
    print("appended entry %d; %d -> %d bytes%s"
          % (len(reg), len(raw), len(out), " (dry run)" if dry else ""))


if __name__ == "__main__":
    main()
