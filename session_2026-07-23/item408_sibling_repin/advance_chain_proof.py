#!/usr/bin/env python3
"""ITEM 408 item 5 — END-TO-END round-advance chain proof (FOLDED-IN single-transaction design).

Drives a GENUINE weekly store advance on a throwaway scratch via the accepted staged_apply transaction
(armed IN-PROCESS against the scratch only — the shipped gate stays OFF). Under the folded-in architecture
the STORE, the CANONICAL BOARD of record AND the balanced/strict SIBLING (+ FV reference vector, boot
manifest, release-contract identities/aggregate/seal, FV oracle, board-view stamp, sidecar) ALL advance
INSIDE the ONE transaction (staged_apply._stage_sibling). So immediately after the advance:

  1. staged_apply.apply_snapshot(R20)  -> STORE + CANONICAL BOARD advance; the balanced SIBLING advances in
     the SAME transaction (tracks the new store); every dependent pin/vector/oracle/contract/view is coherent.
  2. sibling_repin.check                -> CURRENT immediately (no separate repin step; nothing is stale).
  3. sibling_repin.check --full         -> CURRENT (authoritative build-and-compare: the live reference vector
     equals the freshly-rebuilt sibling vector EXACTLY).
  4. sibling_repin.reconcile            -> a correct NO-OP (changed=False); no committed file moves.

This SUPERSEDES the withdrawn two-step chain (advance -> stale -> separate reconcile): the sibling repin now
lives INSIDE the staged_apply transaction, so there is never a post-advance stale interval. Reuses the proven
failure_injection_proof.make_scratch (staged_apply-capable) + round_entry snapshot build.
"""
import json
import os
import shutil
import subprocess
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

# artifacts that must NEVER move even as the round advances. A genuine round apply advances the store, the
# canonical board of record, the season-state (new-round calendar/exposure) and the score ledger (new triples)
# — so those are excluded; only the curve, the curve contract and the committed per-entrant stay frozen.
NON_ADVANCING = {n: r for n, r in SR.FROZEN_REL.items()
                 if n not in ("store", "board_of_record", "score_ledger", "season_state")}


def record(name, ok, detail=""):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  — %s" % detail) if detail else ""))


def augment_scratch(scr):
    """FI.make_scratch gives a staged_apply-capable scratch; add what the folded-in sibling step needs."""
    for d in ("session_2026-07-20", "ui", "session_2026-07-17"):
        dst = os.path.join(scr, d)
        if not os.path.exists(dst):
            shutil.copytree(os.path.join(REPO, d), dst, symlinks=False)
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
    env = dict(os.environ); env["RL_CONFIG_MODE"] = "gate"
    return subprocess.run([sys.executable, os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL), "check"],
                          capture_output=True, text=True, env=env, cwd=scr).returncode == 0


def committed_rels(scr, new_md5):
    """Every committed live target we snapshot to prove a subsequent standalone reconcile is a NO-OP."""
    return [rel for _n, rel in SA.TARGETS] + [
        SR.FV_TEST_REL, SR.BOARD_VIEW_WORKING_REL, SR.BOARD_VIEW_PUBLIC_REL, SR.SIDECAR_REL,
        os.path.join(SR.FV_FIX_REL, SR._reference_vector_name(new_md5))]


def state_of(scr, rels):
    return {r: (FI.md5(os.path.join(scr, r)) if os.path.exists(os.path.join(scr, r)) else None) for r in rels}


def run():
    print("=" * 90)
    print("SIBLING ADVANCE-REPIN — FOLDED-IN SINGLE-TRANSACTION CHAIN (scratch only; gate armed in-proc only)")
    print("=" * 90)
    scr = FI.make_scratch("advchain")
    try:
        augment_scratch(scr)
        store_before = FI.md5(FI.store_path_of(scr))
        board_before = FI.md5(os.path.join(scr, SR.BOARD_OF_RECORD_REL))
        non_adv_before = {n: FI.md5(os.path.join(scr, r)) for n, r in NON_ADVANCING.items()}

        # -- (1) GENUINE advance via the accepted staged_apply transaction (folds in the sibling) --------
        snap = snapshot_for(scr, R20, n=40, base=88.0, step=1.3)
        FI.arm()
        try:
            res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snap, generated_at=GEN)
        finally:
            FI.disarm()
        store_after = FI.md5(FI.store_path_of(scr))
        board_after = FI.md5(os.path.join(scr, SR.BOARD_OF_RECORD_REL))
        boot1 = boot_of(scr)
        rc = json.load(open(os.path.join(scr, SR.RELEASE_CONTRACT_REL)))
        plb = rc["present_lens_baseline"]
        new_md5 = boot1["balanced_board_md5"]
        refp = os.path.join(scr, SR.FV_FIX_REL, SR._reference_vector_name(new_md5))
        ref = json.load(open(refp)) if os.path.exists(refp) else {}
        refvec = ref.get("vector", {})
        fv = open(os.path.join(scr, SR.FV_TEST_REL), encoding="utf-8").read()
        fo = SR._fv_oracle_aggregates(fv)
        bvw = SR._parse_bundle(os.path.join(scr, SR.BOARD_VIEW_WORKING_REL))
        rct = SR._load_module("acrc", os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL))

        record("CHAIN(1) staged_apply advanced the STORE", store_after != store_before,
               "%s -> %s" % (store_before[:8], store_after[:8]))
        record("CHAIN(1) staged_apply advanced the CANONICAL BOARD of record",
               board_after != board_before, "%s -> %s" % (board_before[:8], board_after[:8]))
        record("CHAIN(1) expected_boot store/board/round advanced to R20",
               boot1["store"] == store_after and boot1["board"] == board_after and boot1["as_of_round"] == R20,
               "round=%s" % boot1.get("as_of_round"))

        # -- (2) the balanced SIBLING advanced IN THE SAME transaction; dependents coherent ---------------
        record("CHAIN(2) balanced SIBLING advanced IN THE SAME TRANSACTION (tracks the new store)",
               new_md5 != PRE_BALANCED, "%s -> %s" % (PRE_BALANCED[:8], new_md5[:8]))
        record("CHAIN(2) FV reference vector coherent (board id + internal arithmetic + present-lens)",
               ref.get("board_md5") == new_md5 and ref.get("active") == len(refvec)
               and ref.get("sum_v") == sum(int(v) for v in refvec.values())
               and ref.get("active") == plb["active"] and ref.get("sum_v") == plb["present_value_total"])
        record("CHAIN(2) FV oracle re-aimed (board id + active + sum + Sheezel + reference filename)",
               fo["board_md5"] == new_md5 and fo["active"] == plb["active"]
               and fo["sum_v"] == plb["present_value_total"]
               and fo["sheezel"] == refvec.get("harry-sheezel")
               and fo["reference_vector"] == SR._reference_vector_name(new_md5))
        record("CHAIN(2) contract identities + present_lens + reseal coherent with the sibling",
               rc["identities"]["balanced_board_md5"] == new_md5 and plb["balanced_board_md5"] == new_md5
               and rc.get("contract_sha256") == rct.contract_hash(rc))
        record("CHAIN(2) board_view balanced stamp advanced; board-of-record stamp = the ADVANCED board",
               bvw["stamp"].get("balanced_board_md5") == new_md5
               and str(bvw["stamp"].get("board", ""))[:8] == board_after[:8])
        record("CHAIN(2) release_contract check PASS on the fully-advanced tree", rc_check(scr))

        # -- (3) the gate is CURRENT IMMEDIATELY after the advance (no separate repin needed) -------------
        sr = SR.SiblingRepin(scr)
        record("CHAIN(3) fast gate CURRENT immediately after the advance", sr.is_current_fast())
        record("CHAIN(3) ordinary verify() coherent immediately after the advance", sr.verify()["ok"])
        full = None
        try:
            full = sr.assert_current(full=True)     # authoritative build-and-compare (rebuild + exact vector)
        except SR.SiblingStaleError as e:
            full = {"err": str(e)[:120]}
        record("CHAIN(3) authoritative check --full CURRENT (build-and-compare, exact vector)",
               isinstance(full, dict) and full.get("mode") == "full+build-and-compare"
               and full.get("balanced_board_md5") == new_md5, "%s" % full)

        # -- (4) a subsequent standalone reconcile is a correct NO-OP -------------------------------------
        before = state_of(scr, committed_rels(scr, new_md5))
        rec = sr.reconcile(round_n=R20)
        after = state_of(scr, committed_rels(scr, new_md5))
        changed_files = [k for k in before if before[k] != after[k]]
        record("CHAIN(4) subsequent standalone reconcile is a NO-OP (changed=False)",
               rec.get("no_op") is True and rec.get("changed") is False,
               "no_op=%s changed=%s" % (rec.get("no_op"), rec.get("changed")))
        record("CHAIN(4) the no-op reconcile moved NO committed file", not changed_files,
               "changed=%s" % changed_files)

        # -- (5) the non-advancing frozen artifacts never moved -------------------------------------------
        non_adv_after = {n: FI.md5(os.path.join(scr, r)) for n, r in NON_ADVANCING.items()}
        moved = [n for n in NON_ADVANCING if non_adv_before[n] != non_adv_after[n]]
        record("CHAIN(5) non-advancing frozen artifacts byte-unchanged (curve/curve_contract/per_entrant/ledger)",
               not moved, "moved=%s" % moved)
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
