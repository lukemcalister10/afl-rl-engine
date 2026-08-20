#!/usr/bin/env python3
"""APPEND THE D8 ADOPTION's out-of-round transition to data/release_lineage.json.

ADAPTED FROM docs/evidence/landing_tail_2026-08-20/append_landing_transition.py — the template, written
for THE LANDING. What is adapted, and why: source board a05fe951 -> destination board 5ea978f7; the
STORE IS UNCHANGED (cc02567f both sides), because this is a LEVER change and nothing writes the store;
the owner_ruling citation is the D8 adoption word, verbatim, cited to register v797/v798.

MEASURED, NOT TYPED. Every identity is read from lineage_measured.json, which
07_lineage_identities.txt produced by re-hashing a checkout of 16ec23b (the tree immediately before the
engine edit; proven identity-identical to main 028eb4d) and the live tree, each side checked against
that commit's own data/expected_boot.json. This script retypes nothing.

APPEND-ONLY. Every prior entry preserved byte-verbatim; nothing rewritten. The file round-trips at json
indent=1, asserted before AND after. The top-level present-lens baseline (balanced_board_md5 06d8af60,
release_version) is asserted UNMOVED — it is a frozen historical anchor and stamp.release reads it.

  python3 append_d8_adoption_transition.py <repo_root> [--dry-run]
"""
import json, os, sys

M = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lineage_measured.json')))
S, D = M['source'], M['destination']
BOUNDARY = ["22", "the-d8-adoption-20-8"]

ENTRY = {
    "_doc": (
        "OUT-OF-ROUND LEVER ADOPTION (THE D8 ADOPTION, owner word \"Yes. I'm adopting.\", 2026-08-20). "
        "ORDER D8's ceiling-only dial RL_O33_TAPEROFF — priced 2026-08-20 and delivered PRICED, NOT "
        "ADOPTED (docs/evidence/d8_ceiling_2026-08-20) — becomes the SHIPPED DEFAULT, flipped default "
        "OFF -> default ON behind a DECLARED KILL-SWITCH through the exact lane THE BAKE used (f27482f, "
        "register v780). THE BOARD MOVES: a05fe951 -> 5ea978f7, board total 664,949 -> 693,753 over the "
        "same 804 active rows (+28,804, +4.3318%), because ORDER B's B-3 taper retirement now fires: "
        "band[5] stays max(q97m, q90) exactly as _b6_core emits it, which kills the ceiling v-inversions "
        "by construction — 407 on the retired board, 0 on this one (PACKET_D8.md F4, measured, not "
        "asserted). 559 of 804 rows move, 551 up and 8 down. THE STORE DOES NOT MOVE: cc02567f both "
        "sides. This is a LEVER change — one engine expression's default literal — and nothing in it "
        "writes the store, applies a round or re-seals the book. The round pin stays at 22, so this is "
        "an out-of-round move and the standing owner rule of 2026-07-28 writes a history column at the "
        "point as well: `the-d8-adoption-20-8`, registered in the value / rank / pos_rank histories from "
        "the adopted board (804 points each) by the out_of_round_column writer of record. Appended, not "
        "substituted: every prior entry is preserved verbatim. WHAT MOVED AND WHAT DID NOT, MEASURED: "
        "board, engine_head and balanced_board_md5 move; store, rl_model, fv, config and v0surf do NOT. "
        "config_sha256 is UNMOVED ON PURPOSE and this is the safety property, not an oversight — "
        "RL_O33_TAPEROFF is a DECLARED KILL-SWITCH and is deliberately absent from "
        "data/model_config.json, so config_manifest.enforce() still REJECTS it as an unknown model "
        "override in bake/gate/canonical mode: no certifying build can CARRY the name, it can only ship "
        "the baked-in default. balanced_board_md5 72fe3a17 -> a49c155f is a REAL, BUILT move, not a "
        "re-stamp: sibling_repin.py reconcile rebuilt the balanced/strict sibling from the same store "
        "and derived the pin from the built artifact. That also discharges the 8-fail sibling backlog "
        "the landing tail named as a future order (09_sibling_repin_verify.txt); verify is now 0 fails. "
        "THE ADOPTION IS PROVED IN BOTH DIRECTIONS: the BARE build (no model-semantics RL_* set at all) "
        "reproduces 5ea978f7 / 693,753 / 804 byte-exact in BOTH dev and canonical posture, and the "
        "kill-switch build (RL_O33_TAPEROFF=0) reproduces the retired board a05fe951 / 664,949 "
        "BYTE-IDENTICAL to the committed file it replaces (docs/evidence/d8_adoption_2026-08-20/"
        "02_proofs_assertions.txt; PREREG_ADOPTION.md F1 and F2, both measured, neither fired). The book "
        "is NOT re-sealed by this act — the head-side sealed-lag widens legitimately and is reported "
        "rather than smuggled shut, exactly as PACKET_D8 §2.1 did."
    ),
    "kind": "movers_release_transition",
    "schema_version": 2,
    "owner_approved": True,
    "owner_ruling_id": ["THE_D8_ADOPTION_2026-08-20_yes_im_adopting"],
    "owner_ruling": (
        "THE D8 ADOPTION, owner word 2026-08-20, VERBATIM: \"Yes. I'm adopting.\" — given in chat "
        "post-compaction, on the ORDER D8 delivery (docs/evidence/d8_ceiling_2026-08-20/PACKET_D8.md "
        "and the movers list MOVERS_D8.md his v772 probation asked for: \"happy to look at still "
        "boosting the younger players pending a look at the movers list\"). Register v797 (main "
        "028eb4d, 2026-08-20) recorded the INTENT — \"the owner intends to adopt D8 post-compaction\" — "
        "and specified the adoption lane; v798 records the ACT. Per the 5babe71 precedent this entry "
        "RECORDS an approval that already exists in the owner's own words; it does not create one."
    ),
    "authority": (
        "Luke McAlister (owner) — sole STOP-1/STOP-2/merge authority; the adoption word given directly "
        "in chat 2026-08-20 and carried to this seat in its execution brief, the intent recorded by the "
        "supervisor pen at register v797; written by the D8 adoption seat (no interpretive authority)."
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
        "kill_switch": "RL_O33_TAPEROFF=0 reproduces board %s byte-exact" % S["board"],
        "bare_build": "no model-semantics RL_* set at all reproduces board %s byte-exact, dev AND canonical" % D["board"],
        "engine_files_touched": "engine/rl_after/_merged_recover.py only (one expression + its comment block)",
        "book_reseal": "NONE — a book re-seal is a separate act and was not smuggled into this one",
    },
    "_measured_note": (
        "moved/unchanged are MEASURED, not asserted. Every `source` identity was re-hashed from a "
        "checkout of 16ec23b — the tree immediately before the engine edit d928bca, proven in "
        "docs/evidence/d8_adoption_2026-08-20/07_lineage_identities.txt to be identity-identical to main "
        "028eb4d (16ec23b adds only PREREG_ADOPTION.md) — board and store by md5 of "
        "data/rl_build/rl_app_data.json and engine/rl_after/rl_model_data.json, engine_head and rl_model "
        "by md5 of engine/rl_after/_merged_recover.py and engine/rl_after/rl_model.py, config by "
        "config_manifest.manifest_hash, fv by fv_provenance.fv_identity over engine/forward_valuation, "
        "register by md5 of LTI_REGISTER.md, v0surf by md5 of data/v0surf.pkl — and each agrees with "
        "that commit's own data/expected_boot.json. Every `destination` identity was re-hashed the same "
        "way from the live tree and agrees with the landed data/expected_boot.json. Board totals were "
        "measured on the two board files directly: 804 rows / 664,949 -> 804 rows / 693,753. "
        "balanced_board_md5 is listed MOVED because it genuinely moved and was genuinely BUILT: unlike "
        "THE LANDING, which left the sibling layer un-run and said so, this act rebuilt it."
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
    print("chain OK: register tail destination.store %s == this entry's source.store" % prev_dest.get("store"))
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
