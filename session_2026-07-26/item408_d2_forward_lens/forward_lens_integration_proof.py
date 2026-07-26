#!/usr/bin/env python3
"""ITEM 408 · D2 — FORWARD-LENS ADVANCE INTEGRATION PROOF (issue #157 §1-§3).

Proves that the +1/+2 projection view (`vP1`/`vP2`) is a MANDATORY SIBLING of the one atomic advance
transaction: it regenerates from the live model + live store on every advance, it cannot lag the live
board, it fails closed on tamper, and a fault anywhere in the transaction leaves ZERO targets moved.

BUILD-AND-COMPARE ONLY. Scratch only. No real store, no live pin movement, score-write gate never armed.
Every result JSON is written OUTSIDE the Git checkout (register v432 note 6, via proof_out).

  D1  plan is read-only              `plan` reports forward `changed` / `changed_map` and writes NOTHING.
  D2  forward sibling regenerates    reconcile emits the forward reference vector + forward oracle under the
                                     round's OWN board id; the oracle RUNS green standalone; verify() green.
  D3  atomicity — pre-validation     a fault injected before validation leaves ZERO targets moved and NO
                                     forward artifact on disk (aborted pre-commit).
  D4  atomicity — mid-commit          a fault injected after the first replacement ROLLS BACK every target
                                     byte-for-byte, and removes the first-time forward artifacts.
  D5  negative control — reference    a tampered forward reference vector HALTS `check` with rc != 0, naming
                                     its own invariant (G-Y0 / LENS-PROJECTION / seal).
  D6  negative control — oracle       a tampered forward ORACLE HALTS `check` with rc != 0, naming the
                                     oracle-vs-reference invariant.
  D7  negative control — sum-preserving  a forward corruption that preserves every aggregate passes the
                                     no-build gate but FAILS `check --full` on EXACT-FORWARD-VECTOR MISMATCH
                                     (build-and-compare, not a stored literal).
  D8  coverage discrimination         a field the resolver does NOT read stays green while a field it DOES
                                     read reds — the control fires on live key names (v433-era trap).
  D9  no-op control                   a transaction with nothing to change is a no-op and yields
                                     BYTE-IDENTICAL forward artifacts.
  D10 no hardcoded board id           no historical board id appears anywhere in the new forward path; every
                                     identity is asserted against the manifest of record.
  D11 determinism                     two independent derivations of the forward view from the same inputs
                                     are byte-identical.
"""
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
ING = os.path.join(REPO, "engine", "rl_after", "ingestion")
sys.path.insert(0, ING)
sys.path.insert(0, os.path.join(REPO, "session_2026-07-20", "weekly_updater_hardening"))
sys.path.insert(0, os.path.join(REPO, "session_2026-07-23", "item408_sibling_repin"))
import sibling_repin as SR                 # noqa: E402
import forward_lens as FL                  # noqa: E402
import failure_injection_proof as FI       # noqa: E402
import proof_out                           # noqa: E402

RESULTS = []

# The historical board ids this work must NEVER hardcode into the new forward path (the R3/club-curve rule,
# the v432 scratch-relative lesson). Read as data here — the point of D10 is that they appear in THIS
# harness's expectation list and NOWHERE in the shipped forward path.
FORBIDDEN_BOARD_IDS = ("1373e824", "06d8af60", "1f10220c", "f05ebe6", "2ab73a6f", "3dc19fbb",
                       "9ecbe0fa", "de4baef9", "81e48293", "6f07f7cb")
NEW_PATH_FILES = (os.path.join("engine", "rl_after", "ingestion", "forward_lens.py"),)


def record(name, ok, detail=""):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  — %s" % detail) if detail else ""))


def sib_scratch(tag):
    """The accepted sibling scratch (byte-identical construction to the item-5 harness)."""
    base = FI.make_scratch(tag)
    for rel in (os.path.join("session_2026-07-20", "fv_provenance_remediation"), "ui",
                os.path.join("session_2026-07-17", "legd_derivation")):
        src = os.path.join(REPO, rel)
        if os.path.isdir(src) and not os.path.exists(os.path.join(base, rel)):
            shutil.copytree(src, os.path.join(base, rel))
    return base


def coherent_baseline(scr):
    """Reconcile the deliberately non-R19 scratch to its OWN coherent truth and return the SCRATCH-RELATIVE
    baseline every case derives its expectations from (register v432; no R19 literal anywhere)."""
    boot = json.load(open(os.path.join(scr, SR.EXPECTED_BOOT_REL), encoding="utf-8"))
    round_n = boot.get("as_of_round")
    sr = SR.SiblingRepin(scr)
    res = sr.reconcile(round_n=round_n)
    v = sr.verify()
    bal = res["balanced_board_md5"]
    return {
        "ok": v["ok"], "fails": v["fails"], "round_n": round_n, "balanced_board_md5": bal,
        "forward_vector": FL.forward_vector_name(bal), "forward_oracle": FL.forward_oracle_name(bal),
        "forward_rel": os.path.join(SR.FV_FIX_REL, FL.forward_vector_name(bal)),
        "oracle_rel": os.path.join(SR.FORWARD_ORACLE_DIR_REL, FL.forward_oracle_name(bal)),
    }


def cli(scr, *args):
    """Run the shipped CLI exactly as an operator/CI would; return (rc, combined output)."""
    p = subprocess.run([sys.executable, os.path.join(scr, "engine", "rl_after", "ingestion",
                                                     "sibling_repin.py"), *args, "--repo", scr],
                       capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def tree_state(scr):
    """md5 of every file under the scratch that this transaction could possibly touch."""
    out = {}
    for rel_root in ("data", "ui/data", "engine/rl_after/ingestion",
                     "session_2026-07-20/fv_provenance_remediation"):
        root = os.path.join(scr, rel_root)
        for dirpath, _dn, fns in os.walk(root):
            if ".sibling_txn" in dirpath or "__pycache__" in dirpath:
                continue
            for fn in fns:
                p = os.path.join(dirpath, fn)
                out[os.path.relpath(p, scr)] = FI.md5(p)
    return out


# ================================================================================ D1 / D2
def d1_d2_plan_and_regenerate():
    scr = sib_scratch("d2_regen")
    try:
        before = tree_state(scr)
        rc, out = cli(scr, "plan")
        after = tree_state(scr)
        doc = json.loads(out[out.index("{"):out.rindex("}") + 1])
        record("D1 plan reports forward changed/changed_map",
               rc == 0 and "forward_vector" in doc["changed_map"] and "forward_oracle" in doc["changed_map"]
               and isinstance(doc.get("forward"), dict) and doc["forward"].get("vector", "").startswith(
                   "forward_vector_"),
               "changed_map forward_vector=%s forward_oracle=%s vector=%s"
               % (doc["changed_map"].get("forward_vector"), doc["changed_map"].get("forward_oracle"),
                  doc.get("forward", {}).get("vector")))
        record("D1 plan WROTE NOTHING (build-and-compare only)", before == after,
               "%d file(s) differ" % len(set(before.items()) ^ set(after.items())))

        base = coherent_baseline(scr)
        fwdp = os.path.join(scr, base["forward_rel"])
        orcp = os.path.join(scr, base["oracle_rel"])
        record("D2 forward reference vector + oracle regenerated under the round's OWN board id",
               base["ok"] and os.path.exists(fwdp) and os.path.exists(orcp),
               "board=%s vector=%s oracle=%s fails=%s"
               % (base["balanced_board_md5"][:8], base["forward_vector"], base["forward_oracle"],
                  base["fails"][:1]))
        fdoc = json.load(open(fwdp, encoding="utf-8"))
        l1, l2 = fdoc["lenses"]["+1"], fdoc["lenses"]["+2"]
        record("D2 forward view is the FULL two-lens vector over the exact active universe",
               len(l1["vector"]) == len(l2["vector"]) == fdoc["active"]
               and set(l1["vector"]) == set(l2["vector"]) and not FL.continuity_fails(fdoc),
               "active=%d +1 sum=%d sheezel=%s | +2 sum=%d sheezel=%s | seal=%s"
               % (fdoc["active"], l1["sum"], l1["sheezel"], l2["sum"], l2["sheezel"],
                  fdoc["vector_sha256"][:12]))
        pr = subprocess.run([sys.executable, orcp], capture_output=True, text=True)
        record("D2 the regenerated forward ORACLE runs green standalone",
               pr.returncode == 0, (pr.stdout or pr.stderr).strip().splitlines()[-1:][0][:130]
               if (pr.stdout or pr.stderr).strip() else "rc=%s" % pr.returncode)
        rcf, outf = cli(scr, "check", "--full")
        record("D2 check --full gates the forward view on REBUILD-AND-COMPARE",
               rcf == 0 and "forward_vector_sha256" in outf, outf.strip().splitlines()[-1:][0][:150])
        return base, scr
    except BaseException:
        shutil.rmtree(scr, ignore_errors=True)
        raise


# ================================================================================ D3 / D4 atomicity
def _fault_case(label, point, expect_rollback):
    """Inject a fault at `point` inside the ONE transaction and prove ZERO targets moved."""
    scr = sib_scratch("d2_fault_%s" % label)
    try:
        # start from a scratch that is NOT yet forward-current, so the transaction has real work to do
        # (forward_vector + forward_oracle + sidecar are all `changed`).
        before = tree_state(scr)
        boot = json.load(open(os.path.join(scr, SR.EXPECTED_BOOT_REL), encoding="utf-8"))

        def fault(p):
            if p == point:
                raise SR.SiblingFault("injected fault at %s" % p)

        sr = SR.SiblingRepin(scr, fault=fault)
        raised = ""
        try:
            sr.reconcile(round_n=boot.get("as_of_round"))
        except BaseException as e:                       # noqa: BLE001 — the injected fault
            raised = "%s: %s" % (type(e).__name__, str(e)[:60])
        after = tree_state(scr)
        moved = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        fwd_left = [f for f in os.listdir(os.path.join(scr, SR.FV_FIX_REL)) if f.startswith("forward_vector_")]
        orc_left = [f for f in os.listdir(os.path.join(scr, SR.FORWARD_ORACLE_DIR_REL))
                    if f.startswith("test_forward_lens_")]
        record("%s injected fault at %s -> ZERO targets moved (incl. the forward sibling)" % (label, point),
               bool(raised) and not moved and not fwd_left and not orc_left,
               "raised=%s moved=%s forward_files_left=%s oracle_files_left=%s"
               % (raised, moved[:3], fwd_left, orc_left))
        if expect_rollback:
            txns = [d for d in os.listdir(sr.txn_root)] if os.path.isdir(sr.txn_root) else []
            statuses = []
            for d in txns:
                m = os.path.join(sr.txn_root, d, "manifest.json")
                if os.path.exists(m):
                    statuses.append(json.load(open(m)).get("status"))
            record("%s the transaction journal records the rollback" % label,
                   "ROLLED_BACK" in statuses, "txn statuses=%s" % statuses)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def d3_d4_atomicity():
    _fault_case("D3 pre-validation", "before_validation", expect_rollback=False)
    _fault_case("D4 mid-commit", "after_first_replacement", expect_rollback=True)


# ================================================================================ D5-D8 negative controls
def _tamper(scr, base, mutate, label, needle, *, full=False, expect_red=True):
    """Restore the pristine forward pair, apply `mutate`, run the shipped CLI gate, restore again."""
    fwdp = os.path.join(scr, base["forward_rel"])
    orcp = os.path.join(scr, base["oracle_rel"])
    pris_f, pris_o = open(fwdp, "rb").read(), open(orcp, "rb").read()
    try:
        mutate(fwdp, orcp)
        args = ("check", "--full") if full else ("check",)
        rc, out = cli(scr, *args)
        named = needle in out
        ok = ((rc != 0 and named) if expect_red else (rc == 0))
        record(label, ok, "rc=%s named=%s :: %s" % (rc, named, out.strip().splitlines()[-1:][0][:170]
                                                    if out.strip() else ""))
        return rc, out
    finally:
        open(fwdp, "wb").write(pris_f)
        open(orcp, "wb").write(pris_o)


def d5_d8_negative_controls(scr, base):
    def bump_p1_value(fwdp, _orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        k = sorted(d["lenses"]["+1"]["vector"])[0]
        d["lenses"]["+1"]["vector"][k] = int(d["lenses"]["+1"]["vector"][k]) + 7   # sum now disagrees
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
    _tamper(scr, base, bump_p1_value,
            "D5 tampered forward REFERENCE (one +1 value) -> HALT, rc!=0, names the G-Y0 sum invariant",
            "forward view: +1 sum")

    def bump_p1_aggregate(fwdp, _orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        d["lenses"]["+1"]["sum"] = int(d["lenses"]["+1"]["sum"]) + 1
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
    _tamper(scr, base, bump_p1_aggregate,
            "D5 tampered forward REFERENCE aggregate (+1 sum) -> HALT, rc!=0, named",
            "forward view: +1 sum")

    def break_seal(fwdp, _orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        d["vector_sha256"] = "0" * 64
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
    _tamper(scr, base, break_seal,
            "D5 tampered forward REFERENCE seal (vector_sha256) -> HALT, rc!=0, names the seal invariant",
            "vector_sha256 seal != recomputed seal")

    def drop_a_key(fwdp, _orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        k = sorted(d["lenses"]["+2"]["vector"])[0]
        del d["lenses"]["+2"]["vector"][k]
        d["lenses"]["+2"]["sum"] = sum(int(x) for x in d["lenses"]["+2"]["vector"].values())
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
    _tamper(scr, base, drop_a_key,
            "D5 a player dropped from the +2 lens -> HALT, rc!=0, names LENS-PROJECTION/G-COHORT",
            "LENS-PROJECTION")

    def tamper_oracle_sum(_fwdp, orcp):
        s = open(orcp, encoding="utf-8").read()
        cur = FL.forward_oracle_aggregates(s)["sum_p1"]
        new = s.replace("!= %d:" % cur, "!= %d:" % (cur - 1))
        assert new != s, "oracle +1 sum token not found — the control did not fire on a live key name"
        open(orcp, "w", encoding="utf-8").write(new)
    _tamper(scr, base, tamper_oracle_sum,
            "D6 tampered forward ORACLE (+1 sum token) -> HALT, rc!=0, names the oracle-vs-reference invariant",
            "forward oracle +1 sum != forward reference +1 sum")

    def tamper_oracle_id(_fwdp, orcp):
        s = open(orcp, encoding="utf-8").read()
        cur = FL.forward_oracle_aggregates(s)["board_md5"]
        open(orcp, "w", encoding="utf-8").write(
            s.replace("FORWARD_BOARD_MD5_GOOD = '%s'" % cur, "FORWARD_BOARD_MD5_GOOD = '%s'" % ("d" * 32)))
    _tamper(scr, base, tamper_oracle_id,
            "D6 tampered forward ORACLE board id -> HALT, rc!=0, named",
            "forward oracle FORWARD_BOARD_MD5_GOOD != forward reference board_md5")

    def tamper_oracle_seal(_fwdp, orcp):
        s = open(orcp, encoding="utf-8").read()
        cur = FL.forward_oracle_aggregates(s)["vector_sha256"]
        open(orcp, "w", encoding="utf-8").write(
            s.replace("FORWARD_VECTOR_SHA256 = '%s'" % cur, "FORWARD_VECTOR_SHA256 = '%s'" % ("e" * 64)))
    _tamper(scr, base, tamper_oracle_seal,
            "D6 tampered forward ORACLE seal -> HALT, rc!=0, named",
            "forward oracle FORWARD_VECTOR_SHA256 != forward reference vector_sha256")

    # --- D7: the strongest forward tamper — sum-preserving AND fully self-consistent. Two players' +1
    #     values are swapped in magnitude (A +1, B -1) so active / sum / Sheezel / the conservation row are
    #     ALL unchanged; the document is then RESEALED and the oracle's seal token is updated to match. The
    #     artifact set is now internally perfect and disagrees with reality only. Nothing short of rebuilding
    #     the board and comparing the complete vector can see it — which is precisely why `check --full`
    #     must be build-and-compare and never a stored-literal check. ---
    def sum_preserving(fwdp, orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        vec = d["lenses"]["+1"]["vector"]
        keys = [k for k in sorted(vec) if k != "harry-sheezel"]
        a, b = keys[0], keys[1]
        vec[a] = int(vec[a]) + 1
        vec[b] = int(vec[b]) - 1                      # sum, sheezel, active, conservation all unchanged
        old_seal = d["vector_sha256"]
        new_seal = FL.vector_seal(d["lenses"])
        d["vector_sha256"] = new_seal                 # reseal the reference…
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
        s = open(orcp, encoding="utf-8").read()       # …and re-aim the oracle at the new seal
        s2 = s.replace(old_seal, new_seal)
        assert s2 != s, "oracle seal token not found — the control did not fire on a live key name"
        open(orcp, "w", encoding="utf-8").write(s2)
    _tamper(scr, base, sum_preserving,
            "D7 sum-preserving forward corruption is INVISIBLE to the no-build gate (verify stays green)",
            "SIBLING CHECK: CURRENT", expect_red=False)
    _tamper(scr, base, sum_preserving,
            "D7 the SAME corruption FAILS check --full on EXACT-FORWARD-VECTOR MISMATCH (build-and-compare)",
            "EXACT-FORWARD-VECTOR MISMATCH", full=True)

    # --- D8: coverage discrimination — the control must fire on keys the resolver ACTUALLY reads ---
    def touch_unread_field(fwdp, _orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        d["_doc"] = "PROSE CHANGED BY THE COVERAGE CONTROL — not a key any resolver reads"
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
    _tamper(scr, base, touch_unread_field,
            "D8 a field the resolver does NOT read leaves the gate GREEN (the control is discriminating)",
            "SIBLING CHECK: CURRENT", expect_red=False)

    def touch_read_field(fwdp, _orcp):
        d = json.load(open(fwdp, encoding="utf-8"))
        d["lenses"]["+2"]["conservation"]["players"] = int(
            d["lenses"]["+2"]["conservation"]["players"]) + 3
        open(fwdp, "w", encoding="utf-8").write(json.dumps(d, indent=2, sort_keys=True))
    _tamper(scr, base, touch_read_field,
            "D8 a conservation field the resolver DOES read reds immediately (G-Y0)",
            "conservation players")


# ================================================================================ D9 no-op control
def d9_noop_control(scr, base):
    fwdp = os.path.join(scr, base["forward_rel"])
    orcp = os.path.join(scr, base["oracle_rel"])
    scp = os.path.join(scr, SR.SIDECAR_REL)
    b_f, b_o, b_s = open(fwdp, "rb").read(), open(orcp, "rb").read(), open(scp, "rb").read()
    res = SR.SiblingRepin(scr).reconcile(round_n=base["round_n"])
    a_f, a_o, a_s = open(fwdp, "rb").read(), open(orcp, "rb").read(), open(scp, "rb").read()
    record("D9 no-op control: a transaction with nothing to change is a NO-OP",
           res.get("changed") is False and res.get("no_op") is True,
           "changed=%s no_op=%s wrote_sidecar=%s"
           % (res.get("changed"), res.get("no_op"), res.get("wrote_sidecar")))
    record("D9 no-op control: forward artifacts are BYTE-IDENTICAL across the no-op",
           b_f == a_f and b_o == a_o and b_s == a_s,
           "forward_vector=%s forward_oracle=%s sidecar=%s"
           % (b_f == a_f, b_o == a_o, b_s == a_s))


# ================================================================================ D10 no hardcoded id
def d10_no_hardcoded_board_id():
    hits = []
    for rel in NEW_PATH_FILES:
        src = open(os.path.join(REPO, rel), encoding="utf-8").read()
        for bad in FORBIDDEN_BOARD_IDS:
            if bad in src:
                hits.append("%s carries the historical board id %s" % (rel, bad))
        for m in re.findall(r"(?<![0-9a-zA-Z_])[0-9a-f]{32}(?![0-9a-zA-Z_])", src):
            hits.append("%s carries a bare 32-hex identity literal %s" % (rel, m[:8]))
    record("D10 no hardcoded historical board id (or any bare md5 identity) in the new forward path",
           not hits, "hits=%s" % hits[:3])
    # every forward identity is keyed to the manifest of record's own board id
    boot = json.load(open(os.path.join(REPO, SR.EXPECTED_BOOT_REL), encoding="utf-8"))
    bal = boot.get("balanced_board_md5")
    record("D10 forward filenames derive from the manifest of record, not a literal",
           FL.forward_vector_name(bal) == "forward_vector_%s.json" % bal[:8]
           and FL.forward_oracle_name(bal) == "test_forward_lens_%s.py" % bal[:8],
           "manifest balanced=%s -> %s / %s" % (bal[:8], FL.forward_vector_name(bal),
                                                FL.forward_oracle_name(bal)))


# ================================================================================ D11 determinism
def d11_determinism(scr, base):
    fwdp = os.path.join(scr, base["forward_rel"])
    doc = json.load(open(fwdp, encoding="utf-8"))
    a = FL.dumps_forward_vector(doc)
    b = FL.dumps_forward_vector(json.loads(json.dumps(doc)))     # a different dict insertion order
    shuffled = {k: doc[k] for k in sorted(doc, reverse=True)}
    c = FL.dumps_forward_vector(shuffled)
    record("D11 forward serialization is byte-identical under a different dict order", a == b == c,
           "len=%d md5=%s" % (len(a), __import__("hashlib").md5(a).hexdigest()[:12]))
    o1 = open(os.path.join(scr, base["oracle_rel"]), encoding="utf-8").read()
    fwd_built = {k: v for k, v in doc.items() if k in ("board_md5", "active", "lenses", "vector_sha256")}
    o2 = FL.render_forward_oracle(fwd_built)
    record("D11 forward oracle re-renders byte-identically from the same derived values", o1 == o2,
           "len=%d/%d" % (len(o1), len(o2)))


def main():
    print("=" * 96)
    print("ITEM 408 · D2 — FORWARD-LENS ADVANCE INTEGRATION PROOF (scratch only; gate OFF; no live moves)")
    print("=" * 96)
    d10_no_hardcoded_board_id()
    base, scr = d1_d2_plan_and_regenerate()
    try:
        d5_d8_negative_controls(scr, base)
        d9_noop_control(scr, base)
        d11_determinism(scr, base)
    finally:
        shutil.rmtree(scr, ignore_errors=True)
    d3_d4_atomicity()

    npass = sum(1 for r in RESULTS if r["ok"])
    print("\n  " + "-" * 74)
    print("  RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    out = proof_out.write_result(__file__, "D2_FORWARD_LENS_RESULTS.json",
                                 {"passed": npass, "total": len(RESULTS), "results": RESULTS})
    print("  results written OUTSIDE the checkout: %s" % out)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
