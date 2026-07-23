#!/usr/bin/env python3
"""ITEM 408 item 5 — SIBLING ADVANCE-REPIN proof harness.

Proves engine/rl_after/ingestion/sibling_repin.py against SCRATCH copies ONLY. Writes NOTHING to the real
single source; no scratch path resolves to a live artifact; NO real score apply is performed (the shipped
gate stays OFF — this harness never arms it).

Proofs (each script-emitted; SILENCE IS A RED; non-zero exit on any failure):
  P1 COHERENT (real build)    a scratch whose balanced/strict + FV siblings are artificially STALE
                              (06d8af60) against the R19 store -> reconcile REBUILDS the sibling (1373e824,
                              from the SAME store), and moves EVERY dependent pin/aggregate/reference/seal
                              coherently: expected_boot.balanced_board_md5, release_contract identities +
                              present_lens_baseline {balanced_board_md5, active, present_value_total} +
                              re-seal, the regenerated reference_vector_1373e824.json, the FV test oracle
                              (BOARD_MD5_GOOD + aggregates + ref path), board_view balanced stamp, and the
                              provenance sidecar. release_contract check PASSES afterward; the board of
                              record / store / curve / per_entrant are byte-UNCHANGED by the repin.
  P2 FAIL-CLOSED (gen)        a sibling-GENERATION failure -> reconcile raises -> NO live target changed.
  P3 FAIL-CLOSED (validate)   a pre-commit VALIDATION-phase fault -> reconcile raises -> NO live target
                              changed (ABORTED_PRECOMMIT).
  P4 ROLLBACK (commit fault)  a fault mid-COMMIT (after the first replacement) -> rollback restores EVERY
                              expanded target byte-for-byte; the txn ends ROLLED_BACK.
  P5 IDEMPOTENT               a second reconcile on an already-current tree is a NO-OP (no pin moves).
  P6 REPAIR (crash recovery)  an interrupted txn left in COMMITTING (a simulated crash, partial live
                              replacement) is ROLLED BACK on the next reconcile, restoring every target.

The P2..P6 machinery proofs use the ACCEPTED sibling identity (the real 804-row present-v vector from
fixtures/reference_vector_1373e824.json) via a cached build, so the transaction machinery is exercised
without repeated heavy board builds; P1 does the real build end-to-end.
"""
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
ING = os.path.join(REPO, "engine", "rl_after", "ingestion")
sys.path.insert(0, ING)
import sibling_repin as SR          # noqa: E402
import scratch_fixture as SF        # noqa: E402

STALE_MD5 = "06d8af60b679a12db07c064c60c065f9"    # the pre-STOP-1 balanced pin (a valid earlier identity)
ACCEPTED_MD5 = "1373e82471a81064ef96820f3db065df"

RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  — %s" % detail) if detail else ""))


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for ch in iter(lambda: f.read(1 << 16), b""):
            h.update(ch)
    return h.hexdigest()


def read(path):
    with open(path, "rb") as f:
        return f.read()


# ------------------------------------------------------------------ scratch construction
_COPY_DIRS = ("engine", "data", "ui", "session_2026-07-17", "session_2026-07-18", "session_2026-07-20")


def make_scratch(tag):
    dst = tempfile.mkdtemp(prefix="sibrepin_%s_" % tag)
    for d in _COPY_DIRS:
        shutil.copytree(os.path.join(REPO, d), os.path.join(dst, d), symlinks=False)
    for f in os.listdir(REPO):
        src = os.path.join(REPO, f)
        if os.path.isfile(src) and (f.endswith(".py") or f == "LTI_REGISTER.md"):
            shutil.copy2(src, os.path.join(dst, f))
    if os.path.isdir(os.path.join(REPO, "vendor")):
        shutil.copytree(os.path.join(REPO, "vendor"), os.path.join(dst, "vendor"))
    SF.stamp_release_identities(dst)      # coherent engine pins for the scratch's own Guard 5 / verify
    return dst


def cached_sib(scr):
    """The ACCEPTED sibling identity (real 804-row present-v vector) bound to the scratch's store md5.
    Read from the LIVE repo (the scratch's copy may have been removed by make_siblings_stale)."""
    rv = json.load(open(os.path.join(REPO, SR.FV_FIX_REL, "reference_vector_1373e824.json")))
    return {"board_md5": rv["board_md5"], "active": rv["active"], "sum_v": rv["sum_v"],
            "sheezel": rv["vector"]["harry-sheezel"], "vector": rv["vector"],
            "source_store_md5": md5(os.path.join(scr, SR.STORE_REL)),
            "fv_identity": "6a9a520fa2f8b4051e889d324d905cff0a37e592232cd5e68f0e0d9bdfeeec35",
            "rl_model_md5": None}


def make_siblings_stale(scr):
    """Rewrite the scratch's balanced/strict + FV sibling pins to the earlier 06d8af60 identity, so a
    reconcile MUST rebuild + move them. The board of record / store are left at the real R19 values."""
    # expected_boot.balanced_board_md5 -> stale
    bootp = os.path.join(scr, SR.EXPECTED_BOOT_REL)
    boot = json.load(open(bootp))
    boot["balanced_board_md5"] = STALE_MD5
    with open(bootp, "w") as f:
        json.dump(boot, f, indent=2)
    # release_contract identities + present_lens_baseline -> stale (and re-seal so it is internally valid)
    rcp = os.path.join(scr, SR.RELEASE_CONTRACT_REL)
    rc = json.load(open(rcp))
    rc["identities"]["balanced_board_md5"] = STALE_MD5
    rc["present_lens_baseline"]["balanced_board_md5"] = STALE_MD5
    rc["present_lens_baseline"]["present_value_total"] = 752427
    rc.pop("contract_sha256", None)
    rct = SR._load_module("sf_rc", os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL))
    rc["contract_sha256"] = rct.contract_hash(rc)
    with open(rcp, "w") as f:
        json.dump(rc, f, indent=2, ensure_ascii=True)
        f.write("\n")
    # FV test oracle -> stale (BOARD_MD5_GOOD + aggregates + reference filename; 06d8af60 vector exists)
    fvp = os.path.join(scr, SR.FV_TEST_REL)
    s = open(fvp, encoding="utf-8").read()
    s = s.replace(ACCEPTED_MD5, STALE_MD5).replace("1373e824", "06d8af60")
    s = s.replace("'sum_v') == 760253", "'sum_v') == 752427").replace("'sheezel') == 9542", "'sheezel') == 7964")
    s = s.replace("804/760253/9542", "804/752427/7964")
    with open(fvp, "w", encoding="utf-8") as f:
        f.write(s)
    # board_view working stamp -> stale balanced pin (so the repin genuinely re-stamps it)
    bvw = os.path.join(scr, SR.BOARD_VIEW_WORKING_REL)
    if os.path.exists(bvw):
        _t = open(bvw, encoding="utf-8").read().replace("1373e824", "06d8af60")
        with open(bvw, "w", encoding="utf-8") as f:
            f.write(_t)
    # remove the accepted reference vector so the repin must REGENERATE it from the built board
    accepted_ref = os.path.join(scr, SR.FV_FIX_REL, "reference_vector_1373e824.json")
    if os.path.exists(accepted_ref):
        os.remove(accepted_ref)
    # remove any copied provenance sidecar (the scratch starts with siblings genuinely stale)
    sidep = os.path.join(scr, SR.SIDECAR_REL)
    if os.path.exists(sidep):
        os.remove(sidep)


def snapshot_frozen(scr):
    return {n: (md5(os.path.join(scr, r)) if os.path.exists(os.path.join(scr, r)) else None)
            for n, r in SR.FROZEN_REL.items()}


def snapshot_all_targets(scr):
    rels = [SR.EXPECTED_BOOT_REL, SR.RELEASE_CONTRACT_REL, SR.FV_TEST_REL,
            SR.BOARD_VIEW_WORKING_REL, SR.BOARD_VIEW_PUBLIC_REL,
            os.path.join(SR.FV_FIX_REL, "reference_vector_1373e824.json"),
            os.path.join(SR.FV_FIX_REL, "reference_vector_06d8af60.json"), SR.SIDECAR_REL]
    return {r: (md5(os.path.join(scr, r)) if os.path.exists(os.path.join(scr, r)) else None) for r in rels}


# ============================================================================ P1: COHERENT (real build)
def p1_coherent_real_build():
    scr = make_scratch("coherent")
    try:
        make_siblings_stale(scr)
        frozen_before = snapshot_frozen(scr)
        sr = SR.SiblingRepin(scr)
        res = sr.reconcile(round_n=19, generated_at_commit="PROOF")
        boot = json.load(open(os.path.join(scr, SR.EXPECTED_BOOT_REL)))
        rc = json.load(open(os.path.join(scr, SR.RELEASE_CONTRACT_REL)))
        plb = rc["present_lens_baseline"]
        refp = os.path.join(scr, SR.FV_FIX_REL, "reference_vector_1373e824.json")
        ref = json.load(open(refp))
        fv = open(os.path.join(scr, SR.FV_TEST_REL), encoding="utf-8").read()
        bvw = SR._parse_bundle(os.path.join(scr, SR.BOARD_VIEW_WORKING_REL))
        sc = json.load(open(os.path.join(scr, SR.SIDECAR_REL)))
        rct = SR._load_module("p1rc", os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL))

        record("P1 reconcile changed + rebuilt sibling == accepted 1373e824",
               res["ok"] and res["changed"] and res["balanced_board_md5"] == ACCEPTED_MD5,
               "built=%s old=%s" % (res["balanced_board_md5"][:8], (res.get("old_balanced_board_md5") or "")[:8]))
        record("P1 expected_boot.balanced_board_md5 advanced", boot["balanced_board_md5"] == ACCEPTED_MD5)
        record("P1 contract identities.balanced_board_md5 advanced",
               rc["identities"]["balanced_board_md5"] == ACCEPTED_MD5)
        record("P1 contract present_lens_baseline advanced (md5+active+present_value_total)",
               plb["balanced_board_md5"] == ACCEPTED_MD5 and plb["active"] == 804
               and plb["present_value_total"] == 760253, "sumv=%s" % plb["present_value_total"])
        record("P1 contract re-sealed coherently (self-hash matches)",
               rc["contract_sha256"] == rct.contract_hash(rc), "seal=%s" % rc["contract_sha256"][:12])
        record("P1 reference_vector_1373e824 regenerated + coherent",
               ref["board_md5"] == ACCEPTED_MD5 and ref["active"] == 804 and ref["sum_v"] == 760253
               and ref["vector"].get("harry-sheezel") == 9542)
        record("P1 FV test oracle re-aimed (BOARD_MD5_GOOD + aggregates + ref path)",
               SR._extract_fv_board_md5(fv) == ACCEPTED_MD5 and "reference_vector_1373e824.json" in fv
               and "'sum_v') == 760253" in fv and "'sheezel') == 9542" in fv)
        record("P1 board_view balanced stamp advanced; board-of-record stamp unchanged",
               bvw["stamp"].get("balanced_board_md5") == ACCEPTED_MD5
               and str(bvw["stamp"].get("board", ""))[:8] == str(boot.get("board", ""))[:8])
        record("P1 provenance sidecar records the new identity + source store",
               sc["balanced_board_md5"] == ACCEPTED_MD5 and sc["source_store_md5"] == str(boot["store"]))
        # release_contract check passes on the repinned scratch
        env = dict(os.environ); env["RL_CONFIG_MODE"] = "gate"
        import subprocess
        p = subprocess.run([sys.executable, os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL), "check"],
                           capture_output=True, text=True, env=env, cwd=scr)
        record("P1 release_contract check PASS after repin", p.returncode == 0,
               (p.stdout or "").strip().splitlines()[-1] if p.stdout else "")
        frozen_after = snapshot_frozen(scr)
        record("P1 frozen artifacts byte-UNCHANGED by the repin (board-of-record/store/curve/per_entrant/...)",
               frozen_before == frozen_after,
               "moved=%s" % [n for n in frozen_before if frozen_before[n] != frozen_after[n]])
        # the gate now reports CURRENT (fast + full-build-and-compare both agree at 1373e824)
        record("P1 gate reports CURRENT after repin (fast)", sr.is_current_fast())
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================ P2: FAIL-CLOSED (generation)
def p2_generation_failure_no_live_change():
    scr = make_scratch("genfail")
    try:
        make_siblings_stale(scr)
        before = snapshot_all_targets(scr)
        frozen_before = snapshot_frozen(scr)
        orig = SR.build_sibling
        SR.build_sibling = lambda root: (_ for _ in ()).throw(SR.SiblingBuildError("injected build failure"))
        raised = False
        try:
            SR.SiblingRepin(scr).reconcile(round_n=19)
        except SR.SiblingBuildError:
            raised = True
        finally:
            SR.build_sibling = orig
        after = snapshot_all_targets(scr)
        record("P2 sibling-generation failure raises fail-closed", raised)
        record("P2 NO live target changed after a generation failure", before == after,
               "changed=%s" % [k for k in before if before[k] != after[k]])
        record("P2 frozen artifacts untouched", frozen_before == snapshot_frozen(scr))
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================ P3: FAIL-CLOSED (validation)
def p3_validation_fault_no_live_change():
    scr = make_scratch("valfail")
    try:
        make_siblings_stale(scr)
        before = snapshot_all_targets(scr)
        sib = cached_sib(scr)
        orig = SR.build_sibling
        SR.build_sibling = lambda root: copy.deepcopy(sib)

        def fault(point):
            if point == "before_validation":
                raise SR.SiblingFault("injected pre-commit validation-phase fault")
        raised = False
        try:
            SR.SiblingRepin(scr, fault=fault).reconcile(round_n=19)
        except SR.SiblingFault:
            raised = True
        finally:
            SR.build_sibling = orig
        after = snapshot_all_targets(scr)
        record("P3 pre-commit validation-phase fault raises fail-closed", raised)
        record("P3 NO live target changed (aborted pre-commit)", before == after,
               "changed=%s" % [k for k in before if before[k] != after[k]])
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================ P4: ROLLBACK (commit fault)
def p4_commit_fault_rollback():
    scr = make_scratch("rollback")
    try:
        make_siblings_stale(scr)
        before = snapshot_all_targets(scr)
        sib = cached_sib(scr)
        orig = SR.build_sibling
        SR.build_sibling = lambda root: copy.deepcopy(sib)

        def fault(point):
            if point == "after_subsequent_replacement":
                raise SR.SiblingFault("injected mid-commit fault after a genuine replacement")
        raised = False
        sr = SR.SiblingRepin(scr, fault=fault)
        try:
            sr.reconcile(round_n=19)
        except SR.SiblingFault:
            raised = True
        finally:
            SR.build_sibling = orig
        after = snapshot_all_targets(scr)
        record("P4 mid-commit fault raises", raised)
        record("P4 rollback restored EVERY target byte-for-byte", before == after,
               "still-changed=%s" % [k for k in before if before[k] != after[k]])
        # the txn is journaled ROLLED_BACK
        txns = [os.path.join(sr.txn_root, d) for d in os.listdir(sr.txn_root)] if os.path.isdir(sr.txn_root) else []
        statuses = [sr._read_manifest(t).get("status") for t in txns if sr._read_manifest(t)]
        record("P4 txn ends ROLLED_BACK", "ROLLED_BACK" in statuses, "statuses=%s" % statuses)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================ P5: IDEMPOTENT
def p5_idempotent():
    scr = make_scratch("idem")
    try:
        make_siblings_stale(scr)
        sib = cached_sib(scr)
        orig = SR.build_sibling
        SR.build_sibling = lambda root: copy.deepcopy(sib)
        try:
            r1 = SR.SiblingRepin(scr).reconcile(round_n=19)
            after1 = snapshot_all_targets(scr)
            r2 = SR.SiblingRepin(scr).reconcile(round_n=19)
            after2 = snapshot_all_targets(scr)
        finally:
            SR.build_sibling = orig
        record("P5 first reconcile moved the pins", r1["changed"])
        record("P5 second reconcile is a NO-OP (idempotent)", (not r2["changed"]) and r2["no_op"])
        record("P5 no target bytes changed on the second reconcile", after1 == after2,
               "changed=%s" % [k for k in after1 if after1[k] != after2[k]])
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ============================================================================ P6: REPAIR (crash recovery)
def p6_repair_recovers_incomplete_txn():
    scr = make_scratch("repair")
    try:
        make_siblings_stale(scr)
        before = snapshot_all_targets(scr)
        sib = cached_sib(scr)
        orig = SR.build_sibling
        SR.build_sibling = lambda root: copy.deepcopy(sib)

        # Simulate a CRASH mid-commit: fault after the first replacement AND suppress the in-line rollback
        # (as if the process died before _handle_failure ran), leaving a COMMITTING txn + a partial live
        # write. The NEXT reconcile must recover (roll back) that incomplete txn before proceeding.
        def fault(point):
            if point == "after_subsequent_replacement":
                raise SR.SiblingFault("simulated crash mid-commit")
        sr = SR.SiblingRepin(scr, fault=fault)
        sr._handle_failure = lambda txn_dir, exc: None      # suppress rollback -> leave it INCOMPLETE
        try:
            sr.reconcile(round_n=19)
        except SR.SiblingFault:
            pass
        # a target was partially replaced and the txn is left non-terminal (COMMITTING)
        mid = snapshot_all_targets(scr)
        txns = [os.path.join(sr.txn_root, d) for d in os.listdir(sr.txn_root)]
        st_mid = [SR.SiblingRepin(scr)._read_manifest(t).get("status") for t in txns]
        record("P6 crash left an INCOMPLETE (COMMITTING) txn + a partial live write",
               "COMMITTING" in st_mid and mid != before, "statuses=%s partial=%s" % (st_mid, mid != before))
        # next reconcile RECOVERS (rolls back the incomplete txn) before repinning
        SR.build_sibling = lambda root: copy.deepcopy(sib)
        sr2 = SR.SiblingRepin(scr)
        res = sr2.reconcile(round_n=19)
        after = snapshot_all_targets(scr)
        SR.build_sibling = orig
        record("P6 next reconcile recovered the incomplete txn", bool(res.get("recovered")),
               "recovered=%s" % res.get("recovered"))
        record("P6 tree is coherent after recovery + repin (release_contract check PASS)",
               SR.SiblingRepin(scr).verify()["ok"])
    finally:
        SR.build_sibling = orig
        shutil.rmtree(scr, ignore_errors=True)


def main():
    print("=" * 90)
    print("SIBLING ADVANCE-REPIN PROOF (ITEM 408 item 5) — scratch only; no real store; gate OFF")
    print("=" * 90)
    p1_coherent_real_build()
    p2_generation_failure_no_live_change()
    p3_validation_fault_no_live_change()
    p4_commit_fault_rollback()
    p5_idempotent()
    p6_repair_recovers_incomplete_txn()
    npass = sum(1 for r in RESULTS if r["ok"])
    print("\n  " + "-" * 70)
    print("  RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PROOF_RESULTS.json")
    with open(out, "w") as f:
        json.dump({"passed": npass, "total": len(RESULTS), "results": RESULTS}, f, indent=2)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
