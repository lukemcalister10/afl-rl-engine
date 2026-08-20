#!/usr/bin/env python3
"""WALK THE RELEASE CONTRACT'S BAKE-LANE PINS TO THE LANDED VALUES.

WHAT THIS IS. data/release_contract.json still names the PRE-BAKE code identities:

    config_sha256              cef06fd6250b   (live manifest hash is eed19a75f775)
    identities.engine_head     c0a7e969fdd9   (expected_boot 5ac6780f3c49)
    identities.rl_model        33f940735281   (expected_boot 6fe7c4155866)
    identities.fv              d920557ef21d   (expected_boot 6e9a370e5970)

`python3 release_contract.py check` rejects on all four. They were left behind because THE BAKE
(f27482f, register v780-v781) moved them and did not re-stamp this contract, and because
release_contract.restamp_dynamic — the only scripted contract writer in the tree — DELIBERATELY
preserves them ("EVERYTHING ELSE is preserved byte-for-byte: … the immutable engine/rl_model/fv/
register/band identities"). That is a design statement, not an omission, so no writer in the tree
walks them: verified again here by enumerating every module that touches `contract_sha256`
(ownership_store_apply, staged_apply, sibling_repin, one_source_selftest, scratch_fixture,
release_contract) — staged_apply and ownership_store_apply both route through restamp_dynamic, and
sibling_repin writes only balanced_board_md5 + present_lens_baseline off a freshly BUILT sibling.

WHY THIS IS A RE-STAMP AND NOT A BAKE-CLASS ACT. All four values are file identities of files that
are ALREADY in the tree and ALREADY carried by the accepted manifest data/expected_boot.json. Nothing
is built, derived, fitted or compared here: each is re-hashed from the checkout by the tree's own
definition (boot_guard.py) and asserted equal to the manifest before it is written. The gate's own
remedy text — "re-stamp the contract at a bake in the same commit that moves the manifest/board
identity" — describes a commit that is already in history (the manifest moved at THE LANDING,
463e53d); this act is the re-stamp that commit owed and did not make.

WHAT IT MOVES, and nothing else:
    data/release_contract.json  config_sha256              -> config_manifest.manifest_hash(root)
                                identities.engine_head     -> md5(engine/rl_after/_merged_recover.py)
                                identities.rl_model        -> md5(engine/rl_after/rl_model.py)
                                identities.fv              -> fv_provenance.fv_identity(engine/forward_valuation)
                                contract_sha256            -> recomputed by the contract's OWN hasher

DELIBERATELY NOT MOVED — and this is the HALT half of the item, stated rather than papered over:
    identities.balanced_board_md5      234c3414
    present_lens_baseline.balanced_board_md5 / .active / .present_value_total (761574)
These are BUILD-AND-COMPARE values. Their writer of record is
engine/rl_after/ingestion/sibling_repin.py and it moves them ONLY from a freshly BUILT balanced/strict
sibling board — a full sibling engine build that also moves a LANDED pin in data/expected_boot.json.
That IS a bake-class act, it is outside this order, and `sibling_repin.py verify` already reports its
8 fails as a named future order. present_value_total 761574 is the OLD release's present-v sum; the
landed board a05fe951 sums 664,949. Nothing here pretends otherwise.

  python3 repin_contract_bake_identities.py <REPO> [--dry-run]
"""
import hashlib
import importlib.util
import json
import os
import sys

REPO = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()
DRY = "--dry-run" in sys.argv
P = lambda *a: os.path.join(REPO, *a)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def main():
    # ---- MEASURE from the tree, by the tree's own definitions (boot_guard.py) -------------------
    sys.path.insert(0, REPO)
    sys.path.insert(0, P("engine", "rl_after"))
    import config_manifest as CM
    import fv_provenance as FV

    measured = {
        "config": CM.manifest_hash(REPO),
        "engine_head": _md5(P("engine", "rl_after", "_merged_recover.py")),
        "rl_model": _md5(P("engine", "rl_after", "rl_model.py")),
        "fv": FV.fv_identity(FV.checkout_fv_dir(REPO)),
    }

    # ---- the accepted manifest must AGREE with every measurement before anything is written -----
    boot = json.load(open(P("data", "expected_boot.json")))
    for k, v in measured.items():
        if boot.get(k) != v:
            raise SystemExit("HALT: measured %s %s != expected_boot %s — the manifest and the tree "
                             "disagree; this act re-stamps a contract, it does not adjudicate a pin"
                             % (k, v, boot.get(k)))
        print("measured %-12s %s   == expected_boot" % (k, v))

    RCT = _load("release_contract_landing", P("release_contract.py"))
    cp = P("data", "release_contract.json")
    raw = open(cp, "rb").read()
    rc = json.loads(raw)
    if (json.dumps(rc, indent=2)).encode() != raw:
        raise SystemExit("HALT: release_contract.json does not round-trip at indent=2; refusing to reformat it")

    old_seal = rc["contract_sha256"]
    if old_seal != RCT.contract_hash(rc):
        raise SystemExit("HALT: the contract seal is not self-consistent BEFORE this act")

    # ---- the frozen half, asserted unmoved -----------------------------------------------------
    frozen_before = {
        "identities.balanced_board_md5": rc["identities"].get("balanced_board_md5"),
        "identities.board": rc["identities"].get("board"),
        "identities.store": rc["identities"].get("store"),
        "identities.band": rc["identities"].get("band"),
        "identities.register": rc["identities"].get("register"),
        "present_lens_baseline": json.dumps(rc.get("present_lens_baseline"), sort_keys=True),
        "release_version": rc.get("release_version"),
        "as_of_round": rc.get("as_of_round"),
        "switch_posture": json.dumps(rc.get("switch_posture"), sort_keys=True),
        "pvc_provenance": json.dumps(rc.get("pvc_provenance"), sort_keys=True),
        "must_be_unset": json.dumps(rc.get("must_be_unset"), sort_keys=True),
        "held_checks": json.dumps(rc.get("held_checks"), sort_keys=True),
        "f5_entrant_reconciliation": json.dumps(rc.get("f5_entrant_reconciliation"), sort_keys=True),
        "season_metadata": json.dumps(rc.get("season_metadata"), sort_keys=True),
        "adopted": json.dumps(rc.get("adopted"), sort_keys=True),
    }

    print()
    print("contract config_sha256          %s -> %s" % (rc["config_sha256"][:12], measured["config"][:12]))
    for f in ("engine_head", "rl_model", "fv"):
        print("contract identities.%-12s %s -> %s" % (f, str(rc["identities"][f])[:12], measured[f][:12]))
    rc["config_sha256"] = measured["config"]
    rc["identities"]["engine_head"] = measured["engine_head"]
    rc["identities"]["rl_model"] = measured["rl_model"]
    rc["identities"]["fv"] = measured["fv"]
    rc.pop("contract_sha256", None)
    rc["contract_sha256"] = RCT.contract_hash(rc)
    print("contract_sha256                 %s -> %s" % (old_seal[:12], rc["contract_sha256"][:12]))

    frozen_after = {
        "identities.balanced_board_md5": rc["identities"].get("balanced_board_md5"),
        "identities.board": rc["identities"].get("board"),
        "identities.store": rc["identities"].get("store"),
        "identities.band": rc["identities"].get("band"),
        "identities.register": rc["identities"].get("register"),
        "present_lens_baseline": json.dumps(rc.get("present_lens_baseline"), sort_keys=True),
        "release_version": rc.get("release_version"),
        "as_of_round": rc.get("as_of_round"),
        "switch_posture": json.dumps(rc.get("switch_posture"), sort_keys=True),
        "pvc_provenance": json.dumps(rc.get("pvc_provenance"), sort_keys=True),
        "must_be_unset": json.dumps(rc.get("must_be_unset"), sort_keys=True),
        "held_checks": json.dumps(rc.get("held_checks"), sort_keys=True),
        "f5_entrant_reconciliation": json.dumps(rc.get("f5_entrant_reconciliation"), sort_keys=True),
        "season_metadata": json.dumps(rc.get("season_metadata"), sort_keys=True),
        "adopted": json.dumps(rc.get("adopted"), sort_keys=True),
    }
    moved = [k for k in frozen_before if frozen_before[k] != frozen_after[k]]
    if moved:
        raise SystemExit("HALT: a field this act must not touch moved: %s" % moved)
    print("frozen fields asserted unmoved: %d checked, 0 moved" % len(frozen_before))

    if DRY:
        print("\n--dry-run: nothing written.")
        return

    tmp = cp + ".tmp_repin"
    with open(tmp, "w") as f:
        json.dump(rc, f, indent=2)
    os.replace(tmp, cp)

    rc2 = json.load(open(cp))
    assert rc2["config_sha256"] == measured["config"], "config pin did not take"
    for f in ("engine_head", "rl_model", "fv"):
        assert rc2["identities"][f] == measured[f], "%s pin did not take" % f
    assert rc2["contract_sha256"] == RCT.contract_hash(rc2), "the contract seal must verify after the write"
    assert rc2["identities"]["store"] == boot["store"], "the store pin must still name the live store"
    assert rc2["identities"]["board"] == boot["board"], "the board pin must still name the live board"
    print("\nRE-STAMPED and re-read. The seal verifies; store and board pins still name the live tree.")


if __name__ == "__main__":
    main()
