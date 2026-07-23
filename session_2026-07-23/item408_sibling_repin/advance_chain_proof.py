#!/usr/bin/env python3
"""ITEM 408 item 5 — END-TO-END round-advance chain proof (scratch only; NO real store touched).

Drives a GENUINE weekly store advance on a throwaway scratch via the accepted staged_apply transaction
(armed IN-PROCESS against the scratch only — the shipped gate stays OFF), then runs sibling_repin so the
store, canonical board of record, balanced/strict sibling, full FV reference vector, boot manifest
identities, release-contract identities/aggregate/seal and the FV oracle all move COHERENTLY, in lockstep:

  1. staged_apply.apply_snapshot(R20)  -> advances the STORE + CANONICAL BOARD + expected_boot(store/board/
     round) + release_contract(store/board/season); leaves balanced_board_md5 STALE (the pre-advance pin).
  2. sibling_repin.check                -> reports STALE (the gate: siblings drifted from the new store).
  3. sibling_repin.reconcile            -> rebuilds the balanced sibling FROM THE NEW STORE (build-and-
     compare, a NEW md5 != the pre-advance 1373e824), regenerates the FV reference vector, and moves every
     dependent balanced/FV pin + present_lens aggregate + contract re-seal + FV oracle + board_view stamp +
     sidecar coherently. release_contract check PASSES. The canonical board of record (the advance's output)
     is NOT touched by the repin.
  4. sibling_repin.check                -> reports CURRENT.

Reuses the proven failure_injection_proof.make_scratch (staged_apply-capable) + round_entry snapshot build.
This exercises the accepted staged_apply/round_finalize machinery UNCHANGED; only sibling_repin is new.
"""
import hashlib
import json
import os
import shutil
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ING = os.path.join(REPO, "engine", "rl_after", "ingestion")
sys.path.insert(0, ING)
sys.path.insert(0, os.path.join(REPO, "session_2026-07-20", "weekly_updater_hardening"))
import sibling_repin as SR                 # noqa: E402
import staged_apply as SA                  # noqa: E402
import round_entry as RE                   # noqa: E402
import failure_injection_proof as FI       # noqa: E402  (make_scratch, arm, disarm, md5, store_path_of)

GEN = "2026-07-23T00:00:00Z"
R20 = 20
PRE_BALANCED = "1373e82471a81064ef96820f3db065df"
RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  — %s" % detail) if detail else ""))


def augment_scratch(scr):
    """FI.make_scratch gives a staged_apply-capable scratch; add what sibling_repin also needs."""
    for d in ("session_2026-07-20", "ui", "session_2026-07-17"):
        dst = os.path.join(scr, d)
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(REPO, d), dst, symlinks=False)
    for f in ("extract_board_view.py",):        # ensure ui/tools present (copied with ui/)
        pass
    # seed the provenance sidecar as CURRENT for the pre-advance store (as the live tree records it)
    live_side = os.path.join(REPO, SR.SIDECAR_REL)
    if os.path.exists(live_side):
        shutil.copy2(live_side, os.path.join(scr, SR.SIDECAR_REL))


def snapshot_for(scr, rnd, n, base, step):
    store = json.load(open(FI.store_path_of(scr)))
    players = [r for r in store if r.get("stable_player_id") and not r.get("_retired")][:n]
    body = "\n".join("%s,%s" % (r["player"], base + i * step) for i, r in enumerate(players))
    ent = RE.RoundEntry(rnd, store_path=FI.store_path_of(scr))
    resolved, residue = ent.resolve_body(body)
    assert not residue, "unexpected residue in a clean synthetic feed"
    return ent.build_snapshot(resolved, generated_at=GEN)


def boot_of(scr):
    return json.load(open(os.path.join(scr, SR.EXPECTED_BOOT_REL)))


def rc_check(scr):
    import subprocess
    env = dict(os.environ); env["RL_CONFIG_MODE"] = "gate"
    return subprocess.run([sys.executable, os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL), "check"],
                          capture_output=True, text=True, env=env, cwd=scr).returncode == 0


def run():
    print("=" * 90)
    print("SIBLING ADVANCE-REPIN — END-TO-END ROUND-ADVANCE CHAIN (scratch only; gate armed in-proc only)")
    print("=" * 90)
    scr = FI.make_scratch("advchain")
    try:
        augment_scratch(scr)
        store_before = FI.md5(FI.store_path_of(scr))
        board_before = FI.md5(os.path.join(scr, SR.BOARD_OF_RECORD_REL))
        boot0 = boot_of(scr)

        # -- (1) GENUINE store advance via the accepted staged_apply transaction ------------------
        snap = snapshot_for(scr, R20, n=40, base=88.0, step=1.3)
        FI.arm()
        try:
            res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        finally:
            FI.disarm()
        store_after = FI.md5(FI.store_path_of(scr))
        board_after = FI.md5(os.path.join(scr, SR.BOARD_OF_RECORD_REL))
        boot1 = boot_of(scr)
        record("CHAIN(1) staged_apply advanced the STORE", store_after != store_before,
               "%s -> %s" % (store_before[:8], store_after[:8]))
        record("CHAIN(1) staged_apply regenerated the CANONICAL BOARD of record",
               board_after != board_before, "%s -> %s" % (board_before[:8], board_after[:8]))
        record("CHAIN(1) expected_boot store/board/round advanced to R20",
               boot1["store"] == store_after and boot1["board"] == board_after
               and boot1["as_of_round"] == R20, "round=%s" % boot1.get("as_of_round"))
        record("CHAIN(1) balanced_board_md5 is now STALE (unchanged by the store advance)",
               boot1["balanced_board_md5"] == PRE_BALANCED)

        # -- (2) the GATE detects the post-advance staleness --------------------------------------
        sr = SR.SiblingRepin(scr)
        stale_detected = not sr.is_current_fast()
        record("CHAIN(2) gate reports STALE after the advance (siblings drifted from the new store)",
               stale_detected)

        # -- (3) sibling_repin moves the siblings in lockstep with the advance --------------------
        frozen_before = {n: FI.md5(os.path.join(scr, r)) for n, r in SR.FROZEN_REL.items()}
        rec = sr.reconcile(round_n=R20, generated_at_commit="ADVANCE-CHAIN")
        boot2 = boot_of(scr)
        rc = json.load(open(os.path.join(scr, SR.RELEASE_CONTRACT_REL)))
        plb = rc["present_lens_baseline"]
        new_md5 = rec["balanced_board_md5"]
        refp = os.path.join(scr, SR.FV_FIX_REL, SR._reference_vector_name(new_md5))
        ref = json.load(open(refp)) if os.path.exists(refp) else {}
        fv = open(os.path.join(scr, SR.FV_TEST_REL), encoding="utf-8").read()
        bvw = SR._parse_bundle(os.path.join(scr, SR.BOARD_VIEW_WORKING_REL))
        rct = SR._load_module("acrc", os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL))

        record("CHAIN(3) balanced SIBLING rebuilt from the NEW store (md5 changed, tracks the store)",
               rec["changed"] and new_md5 != PRE_BALANCED and new_md5 == boot2["balanced_board_md5"],
               "new=%s pre=%s active=%s sumv=%s" % (new_md5[:8], PRE_BALANCED[:8], rec["active"], rec["sum_v"]))
        record("CHAIN(3) full FV reference vector regenerated from the built sibling",
               ref.get("board_md5") == new_md5 and ref.get("active") == rec["active"]
               and ref.get("sum_v") == rec["sum_v"] and ref.get("vector", {}).get("harry-sheezel") == rec["sheezel"])
        record("CHAIN(3) manifest + contract identities + present_lens aggregate coherent with the sibling",
               boot2["balanced_board_md5"] == new_md5 and rc["identities"]["balanced_board_md5"] == new_md5
               and plb["balanced_board_md5"] == new_md5 and plb["active"] == rec["active"]
               and plb["present_value_total"] == rec["sum_v"])
        record("CHAIN(3) release-contract RE-SEALED coherently (self-hash matches)",
               rc.get("contract_sha256") == rct.contract_hash(rc), "seal=%s" % str(rc.get("contract_sha256"))[:12])
        record("CHAIN(3) FV oracle re-aimed to the new sibling (BOARD_MD5_GOOD + aggregates + ref path)",
               SR._extract_fv_board_md5(fv) == new_md5 and SR._reference_vector_name(new_md5) in fv
               and ("'sum_v') == %d" % rec["sum_v"]) in fv and ("'sheezel') == %d" % rec["sheezel"]) in fv)
        record("CHAIN(3) board_view balanced stamp advanced; board-of-record stamp = the ADVANCED board",
               bvw["stamp"].get("balanced_board_md5") == new_md5
               and str(bvw["stamp"].get("board", ""))[:8] == board_after[:8])
        record("CHAIN(3) release_contract check PASS on the fully-advanced tree", rc_check(scr))
        frozen_after = {n: FI.md5(os.path.join(scr, r)) for n, r in SR.FROZEN_REL.items()}
        record("CHAIN(3) the repin did NOT touch the store / advanced board of record / frozen artifacts",
               frozen_before == frozen_after,
               "moved=%s" % [n for n in frozen_before if frozen_before[n] != frozen_after[n]])

        # -- (4) the gate now reports CURRENT -----------------------------------------------------
        record("CHAIN(4) gate reports CURRENT after the lockstep repin", SR.SiblingRepin(scr).is_current_fast())
    finally:
        shutil.rmtree(scr, ignore_errors=True)

    npass = sum(1 for r in RESULTS if r["ok"])
    print("\n  " + "-" * 70)
    print("  RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ADVANCE_CHAIN_RESULTS.json")
    with open(out, "w") as f:
        json.dump({"passed": npass, "total": len(RESULTS), "results": RESULTS}, f, indent=2)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(run())
