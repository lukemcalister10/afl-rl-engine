#!/usr/bin/env python3
"""ITEM 408 item 5 — SINGLE-TRANSACTION sibling-integration proof (blocking-correction evidence).

Proves the CORRECTED design: the balanced/strict sibling advance-repin is folded INTO the accepted
staged_apply weekly round-advance transaction, so the canonical store/board AND the sibling targets
commit under ONE journal + ONE rollback/recovery boundary — there is NEVER an externally-committed
store/board state with stale siblings. Scratch only; no real store; the shipped score-write gate stays
OFF (armed IN-PROCESS against a throwaway scratch only).

  P1  R19 no-op reproduction          build_sibling(live) == 1373e824 / 804 / 760253 / 9542.
  P2  single-transaction advance      genuine R19->R20: store + canonical board + balanced sibling + FV
                                      vector + manifest + contract identities/aggregate/seal + FV oracle +
                                      board-view all move under ONE txn; SIBLING_STAGED precedes COMMIT_BEGIN
                                      (no externally-committed stale-sibling interval); the sibling tracks the
                                      NEW store; release_contract check PASS; ONE txn dir; one manifest target
                                      set covering canonical + sibling.
  P3  sibling-generation failure       injected before commit -> NO live target changed (aborted pre-commit).
  P4  sibling-validation failure       injected before commit -> NO live target changed (aborted pre-commit).
  P5  fault after first canonical      -> rollback restores ALL canonical + sibling targets byte-for-byte.
  P6  fault after a sibling replace    -> rollback restores ALL canonical + sibling targets byte-for-byte.
  P7  crash recovery                   a COMMITTING crash (partial canonical+sibling writes) BLOCKS the next
                                      apply and is RECOVERED (rolled back), restoring every target.
  P8  active-count derived             the FV-oracle edit derives the active count from the built vector — a
                                      synthetic sibling with active=800 yields a staged FV test asserting '== 800'
                                      (no literal 804).
  P9  launchers route through Python   weekly_update.sh, weekly_update.bat and round_entry.py all reach the same
                                      staged_apply transaction (the invariant cannot be bypassed by any launcher).

Second blocking-correction controls (mandatory transaction targets + genuinely complete sibling coherence).
The P1-P9 set (28 checks) is RETAINED; these are ADDED:
  P2/#7  mandatory-target accounting    on the successful advance: manifest target count == collected count ==
                                        replacement-event count; every final live md5 == its validated staged md5.
  P10/#1 public dropped pre-validation  removing board_view_public before validation -> pre-commit refusal; no live change.
  P11/#2 declared target dropped        removing any declared target before collection -> mandatory-target refusal; no partial commit.
  P12/#3 reference value corruption      one refvec value changed (board id kept) -> assert_current fails on the arithmetic.
  P13/#4 FV-oracle drift                 active / sum / Sheezel / reference-filename each drifted (board id kept) -> each fails its own invariant.
  P14/#5 board-bundle corruption         working and public bundles each corrupted -> each fails the coherence gate.
  P15/#6 view-only repair, not no-op     a view-only corruption -> standalone reconcile REPAIRS it (changed, not no_op).

Final completion controls (authoritative full build-and-compare + FV-oracle-only repair):
  P16/D1 exact-vector full compare       a sum-preserving reference-vector corruption passes the no-build gate but
                                        check --full (rebuild + complete-vector compare) fails on EXACT-VECTOR mismatch.
  P17/D2 FV-oracle-only repair           active / sum / Sheezel / reference-filename oracle drift (reference vector
                                        already current): verify() fails, reconcile REPAIRS (changed, not no-op),
                                        verify() + check --full green afterward.
"""
import copy
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
import failure_injection_proof as FI       # noqa: E402

GEN = "2026-07-23T00:00:00Z"
PRE_BALANCED = "1373e82471a81064ef96820f3db065df"
RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  — %s" % detail) if detail else ""))


# repo-relative targets we snapshot for the "no live change" / rollback proofs.
CANON_RELS = [rel for _n, rel in SA.TARGETS]
FIXED_SIB_RELS = [SR.FV_TEST_REL, SR.BOARD_VIEW_WORKING_REL, SR.BOARD_VIEW_PUBLIC_REL, SR.SIDECAR_REL,
                  os.path.join(SR.FV_FIX_REL, "reference_vector_%s.json" % PRE_BALANCED[:8])]


def sib_scratch(tag):
    """FI.make_scratch (accepted, byte-unchanged) + the trees the SIBLING-integrated transaction needs in
    the workspace: the accepted FV builder + fixtures (session_2026-07-20/fv_provenance_remediation), the
    board-view extractor + bundles (ui/), and the per-entrant tree — so staged_apply._stage_sibling builds
    + stages the sibling from the SAME workspace as the canonical board. Keeps failure_injection_proof.py
    (accepted evidence) untouched."""
    base = FI.make_scratch(tag)
    for rel in (os.path.join("session_2026-07-20", "fv_provenance_remediation"), "ui",
                os.path.join("session_2026-07-17", "legd_derivation")):
        src = os.path.join(REPO, rel)
        if os.path.isdir(src) and not os.path.exists(os.path.join(base, rel)):
            shutil.copytree(src, os.path.join(base, rel))
    return base


def state_of(scr, rels):
    return {r: (FI.md5(os.path.join(scr, r)) if os.path.exists(os.path.join(scr, r)) else None) for r in rels}


def new_reference_vectors(scr):
    d = os.path.join(scr, SR.FV_FIX_REL)
    return sorted(f for f in os.listdir(d) if f.startswith("reference_vector_")
                  and f != "reference_vector_%s.json" % PRE_BALANCED[:8]
                  and f != "reference_vector_06d8af60.json")


def snapshot_for(scr, rnd, n=30, base=90.0, step=1.1):
    store = json.load(open(FI.store_path_of(scr)))
    players = [r for r in store if r.get("stable_player_id") and not r.get("_retired")][:n]
    body = "\n".join("%s,%s" % (r["player"], base + i * step) for i, r in enumerate(players))
    ent = RE.RoundEntry(rnd, store_path=FI.store_path_of(scr))
    resolved, residue = ent.resolve_body(body)
    assert not residue, "unexpected residue"
    return ent.build_snapshot(resolved, generated_at=GEN)


def rc_check(scr):
    env = dict(os.environ); env["RL_CONFIG_MODE"] = "gate"
    return subprocess.run([sys.executable, os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL), "check"],
                          capture_output=True, text=True, env=env, cwd=scr).returncode == 0


def _bundle_io(path):
    """Split a `window.__X__ = {...};` bundle into (prefix, obj, suffix) so a corruption round-trips."""
    s = open(path, encoding="utf-8").read()
    i, j = s.index("{"), s.rindex("}")
    return s[:i], json.loads(s[i:j + 1]), s[j + 1:]


def _bundle_write(path, pre, obj, suf):
    with open(path, "w", encoding="utf-8") as f:
        f.write(pre + json.dumps(obj) + suf)


def journal_events(txn_dir):
    return [json.loads(l) for l in open(os.path.join(txn_dir, "journal.jsonl")) if l.strip()]


# ================================================================================ P1
def p1_noop_reproduction():
    sib = SR.build_sibling(REPO)
    record("P1 R19 no-op reproduction: sibling rebuilds to 1373e824 / 804 / 760253 / 9542",
           sib["board_md5"] == PRE_BALANCED and sib["active"] == 804 and sib["sum_v"] == 760253
           and sib["sheezel"] == 9542,
           "md5=%s active=%s sumv=%s sheezel=%s" % (sib["board_md5"][:8], sib["active"], sib["sum_v"], sib["sheezel"]))


# ================================================================================ P2
def p2_single_transaction_advance():
    scr = sib_scratch("single")
    try:
        store0 = FI.md5(FI.store_path_of(scr))
        board0 = FI.md5(os.path.join(scr, "data/rl_build/rl_app_data.json"))
        FI.arm()
        try:
            res = SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snapshot_for(scr, 20), generated_at=GEN)
        finally:
            FI.disarm()
        boot = json.load(open(os.path.join(scr, SR.EXPECTED_BOOT_REL)))
        con = json.load(open(os.path.join(scr, SR.RELEASE_CONTRACT_REL)))
        plb = con["present_lens_baseline"]
        new_md5 = boot["balanced_board_md5"]
        refp = os.path.join(scr, SR.FV_FIX_REL, "reference_vector_%s.json" % new_md5[:8])
        fv = open(os.path.join(scr, SR.FV_TEST_REL), encoding="utf-8").read()
        bvw = SR._parse_bundle(os.path.join(scr, SR.BOARD_VIEW_WORKING_REL))
        rct = SR._load_module("p2rc", os.path.join(scr, SR.RELEASE_CONTRACT_TOOL_REL))
        jn = open(os.path.join(res.txn_dir, "journal.jsonl")).read()
        man = json.load(open(os.path.join(res.txn_dir, "manifest.json")))
        tgt_names = [t["name"] for t in man["targets"]]

        record("P2 store advanced", res.store_md5_after != store0,
               "%s->%s" % (store0[:8], res.store_md5_after[:8]))
        record("P2 canonical board advanced", res.board_md5_after != board0,
               "%s->%s" % (board0[:8], res.board_md5_after[:8]))
        record("P2 expected_boot store/board/round advanced to R20",
               boot["store"] == res.store_md5_after and boot["board"] == res.board_md5_after
               and boot["as_of_round"] == 20)
        record("P2 balanced SIBLING advanced + tracks the NEW store (md5 != pre-advance 1373e824)",
               new_md5 != PRE_BALANCED, "balanced=%s" % new_md5[:8])
        record("P2 contract identities + present_lens + reseal coherent with the sibling",
               con["identities"]["balanced_board_md5"] == new_md5 and plb["balanced_board_md5"] == new_md5
               and con["contract_sha256"] == rct.contract_hash(con))
        record("P2 FV reference vector regenerated + FV oracle re-aimed",
               os.path.exists(refp) and json.load(open(refp))["board_md5"] == new_md5
               and SR._extract_fv_board_md5(fv) == new_md5)
        record("P2 board_view balanced stamp advanced; board stamp = the advanced canonical board",
               bvw["stamp"].get("balanced_board_md5") == new_md5
               and str(bvw["stamp"].get("board", ""))[:8] == res.board_md5_after[:8])
        record("P2 SINGLE transaction: SIBLING_STAGED precedes COMMIT_BEGIN (no committed stale-sibling interval)",
               "SIBLING_STAGED" in jn and jn.index("SIBLING_STAGED") < jn.index("COMMIT_BEGIN"))
        record("P2 ONE manifest target set covers canonical + sibling (one rollback boundary)",
               "store" in tgt_names and "sibling_reference_vector" in tgt_names and "sibling_sidecar" in tgt_names,
               "targets=%d" % len(tgt_names))
        record("P2 release_contract check PASS on the fully-advanced tree", rc_check(scr))

        # --- control #7 (2nd blocking correction): mandatory-target accounting on a successful advance ---
        events = journal_events(res.txn_dir)
        sc_ev = next((e for e in events if e.get("event") == "STAGED_COLLECTED"), None)
        cv_ev = next((e for e in events if e.get("event") == "COMMIT_VERIFIED"), None)
        n_replaced = sum(1 for e in events if e.get("event") == "REPLACED")
        collected = sc_ev.get("collected") if sc_ev else None
        record("P2/#7 manifest target count == collected count",
               len(tgt_names) == collected == (sc_ev.get("declared") if sc_ev else None),
               "manifest=%d collected=%s declared=%s" % (len(tgt_names), collected,
                                                         sc_ev.get("declared") if sc_ev else None))
        record("P2/#7 collected count == replacement-event count (== COMMIT_VERIFIED replaced)",
               collected == n_replaced and cv_ev is not None and cv_ev.get("replaced") == n_replaced
               and cv_ev.get("declared") == len(tgt_names),
               "collected=%s replaced=%s commit_verified=%s" % (collected, n_replaced,
                                                               cv_ev and cv_ev.get("replaced")))
        smd5 = man.get("staged_md5") or {}
        live_md5_ok = (bool(smd5) and len(smd5) == len(tgt_names)
                       and all(smd5.get(t["name"]) == FI.md5(os.path.join(scr, t["live"]))
                               for t in man["targets"]))
        record("P2/#7 every final live target md5 == its validated staged payload",
               live_md5_ok, "staged_md5_entries=%d of %d" % (len(smd5), len(tgt_names)))
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P3 / P4 (fail-closed)
def _no_live_change_proof(tag, sabotage):
    scr = sib_scratch(tag)
    try:
        before = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        FI.arm()
        raised = False
        try:
            ap = SA.StagedRoundApplier.for_repo(scr)
            sabotage(ap)
            ap.apply_snapshot(snapshot_for(scr, 20), generated_at=GEN)
        except (SA.StagedValidationError, SR.SiblingRepinError, SA.FaultInjected, RuntimeError):
            raised = True
        finally:
            FI.disarm()
        after = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        changed = [k for k in before if before[k] != after[k]]
        return raised, changed, new_reference_vectors(scr)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def p3_generation_failure():
    def sab(ap):
        def boom(*a, **k):
            raise SR.SiblingBuildError("injected sibling-generation failure")
        ap._stage_sibling = boom
    raised, changed, newrv = _no_live_change_proof("genfail", sab)
    record("P3 injected sibling-GENERATION failure aborts pre-commit", raised)
    record("P3 NO live target changed after a generation failure", not changed and not newrv,
           "changed=%s newrv=%s" % (changed, newrv))


def p4_validation_failure():
    def sab(ap):
        orig = ap._validate_sibling_staged
        ap._validate_sibling_staged = lambda ws, b: ["injected sibling-validation failure"]
    raised, changed, newrv = _no_live_change_proof("valfail", sab)
    record("P4 injected sibling-VALIDATION failure aborts pre-commit", raised)
    record("P4 NO live target changed after a validation failure", not changed and not newrv,
           "changed=%s newrv=%s" % (changed, newrv))


# ================================================================================ P5 / P6 (rollback)
def _rollback_proof(tag, fault):
    scr = sib_scratch(tag)
    try:
        before = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        FI.arm()
        raised = False
        try:
            SA.StagedRoundApplier.for_repo(scr, fault=fault).apply_snapshot(snapshot_for(scr, 20), generated_at=GEN)
        except (SA.FaultInjected, RuntimeError):
            raised = True
        finally:
            FI.disarm()
        after = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        changed = [k for k in before if before[k] != after[k]]
        return raised, changed, new_reference_vectors(scr)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def p5_fault_after_first_canonical():
    def fault(point):
        if point == "after_first_replacement":
            raise SA.FaultInjected("fault after the first canonical replacement (store)")
    raised, changed, newrv = _rollback_proof("rbfirst", fault)
    record("P5 fault after the first canonical replacement raises", raised)
    record("P5 rollback restored ALL canonical + sibling targets", not changed and not newrv,
           "still-changed=%s newrv=%s" % (changed, newrv))


def p6_fault_after_sibling_replacement():
    st = {"n": 0}
    def fault(point):
        if point == "after_subsequent_replacement":
            st["n"] += 1
            if st["n"] >= 10:      # after the ~11th target = a sibling target (10 canonical precede)
                raise SA.FaultInjected("fault after a sibling replacement")
    raised, changed, newrv = _rollback_proof("rbsib", fault)
    record("P6 fault after a sibling replacement raises", raised)
    record("P6 rollback restored ALL canonical + sibling targets", not changed and not newrv,
           "still-changed=%s newrv=%s" % (changed, newrv))


# ================================================================================ P7 (crash recovery)
def p7_crash_recovery():
    scr = sib_scratch("crash")
    try:
        before = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        st = {"n": 0}
        def fault(point):
            if point == "after_subsequent_replacement":
                st["n"] += 1
                if st["n"] >= 10:
                    raise SA.FaultInjected("simulated crash mid-commit (after a sibling replacement)")
        FI.arm()
        try:
            ap = SA.StagedRoundApplier.for_repo(scr, fault=fault)
            ap._handle_failure = lambda txn_dir, exc: None      # suppress rollback -> leave INCOMPLETE
            try:
                ap.apply_snapshot(snapshot_for(scr, 20), generated_at=GEN)
            except SA.FaultInjected:
                pass
            mid = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
            incomplete = SA.StagedRoundApplier.for_repo(scr).scan_incomplete()
            # a later advance is BLOCKED while the transaction is incomplete
            blocked = False
            try:
                SA.StagedRoundApplier.for_repo(scr).apply_snapshot(snapshot_for(scr, 21), generated_at=GEN)
            except SA.IncompleteTransactionError:
                blocked = True
            # recover rolls back the expanded (canonical + sibling) single transaction
            SA.StagedRoundApplier.for_repo(scr).recover(generated_at=GEN)
        finally:
            FI.disarm()
        after = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        changed = [k for k in before if before[k] != after[k]]
        record("P7 crash left an INCOMPLETE transaction with a partial commit",
               bool(incomplete) and mid != before, "incomplete=%d partial=%s" % (len(incomplete), mid != before))
        record("P7 the next advance is BLOCKED while the transaction is incomplete", blocked)
        record("P7 recovery rolled back the expanded single transaction (all targets restored)",
               not changed and not new_reference_vectors(scr), "still-changed=%s" % changed)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P8 (active derived)
def p8_active_count_derived():
    scr = sib_scratch("active")
    try:
        rv = json.load(open(os.path.join(REPO, SR.FV_FIX_REL, "reference_vector_1373e824.json")))
        # a SYNTHETIC sibling with a DIFFERENT active count + md5 (drop 4 players) — proves the FV-oracle
        # edit derives the active count from the built vector, not a literal 804.
        vec = dict(list(rv["vector"].items())[:800])
        sib = {"board_md5": "a" * 32, "active": 800, "sum_v": sum(vec.values()),
               "sheezel": vec.get("harry-sheezel", 9542), "vector": vec,
               "source_store_md5": FI.md5(os.path.join(scr, SR.STORE_REL)),
               "fv_identity": None, "rl_model_md5": None}
        plan = SR.RepinPlan(scr, sib, round_n=20)
        fv_bytes = plan.targets["fv_test"][1].decode("utf-8")
        record("P8 FV-oracle active count DERIVED from the built vector (== 800, not a literal 804)",
               "'active') == 800" in fv_bytes and "'active') == 804" not in fv_bytes)
        # confirm the FV-oracle re-aim CODE (comments stripped) contains no hardcoded 804 literal — every
        # aggregate is derived from the built sibling. Covers the _compute fv_test block + _repair_fv_oracle.
        src = open(os.path.join(REPO, "engine", "rl_after", "ingestion", "sibling_repin.py"), encoding="utf-8").read()
        block = (src[src.index("def _repair_fv_oracle("):src.index("def _board_view_coherence(")]
                 + src[src.index("oracle = _fv_oracle_aggregates(fv_src)"):src.index('self.changed_map["fv_test"]')])
        code_only = "\n".join(ln.split("#", 1)[0] for ln in block.splitlines())
        record("P8 sibling_repin FV-oracle re-aim has no literal 804 in its CODE (comments aside)",
               "804" not in code_only, "code_has_804=%s" % ("804" in code_only))
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P9 (launchers)
def p9_launchers_route_through_python():
    sh = open(os.path.join(REPO, "tools/round_entry/weekly_update.sh"), encoding="utf-8").read()
    bat = open(os.path.join(REPO, "tools/round_entry/weekly_update.bat"), encoding="utf-8").read()
    cli = open(os.path.join(REPO, "tools/round_entry/round_entry.py"), encoding="utf-8").read()
    record("P9 weekly_update.sh routes through round_entry.py (the Python transaction)",
           "round_entry.py" in sh)
    record("P9 weekly_update.bat routes through round_entry.py (the Python transaction)",
           "round_entry.py" in bat)
    record("P9 the round_entry CLI drives staged_apply (StagedRoundApplier.apply_snapshot) — the invariant path",
           "StagedRoundApplier" in cli and "apply_snapshot" in cli)
    record("P9 staged_apply.apply_snapshot folds in the sibling (_stage_sibling) — no launcher can bypass",
           "_stage_sibling" in open(os.path.join(REPO, "engine/rl_after/ingestion/staged_apply.py")).read())


# ================================================================================ P10 (control #1)
def p10_public_removed_before_validation():
    """Remove board_view_public.js AFTER sibling staging but BEFORE validation -> pre-commit refusal
    (the full-coherence staged validation now checks the public bundle), every live target unchanged."""
    scr = sib_scratch("pubrm")
    try:
        before = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        FI.arm()
        raised = False
        try:
            ap = SA.StagedRoundApplier.for_repo(scr)
            _orig = ap._stage_sibling
            def wrapped(ws, *a, **k):
                r = _orig(ws, *a, **k)
                os.remove(os.path.join(ws, SR.BOARD_VIEW_PUBLIC_REL))
                return r
            ap._stage_sibling = wrapped
            ap.apply_snapshot(snapshot_for(scr, 20), generated_at=GEN)
        except (SA.StagedValidationError, RuntimeError):
            raised = True
        finally:
            FI.disarm()
        after = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        changed = [k for k in before if before[k] != after[k]]
        record("P10/#1 removing board_view_public before validation aborts pre-commit", raised)
        record("P10/#1 NO live target changed", not changed and not new_reference_vectors(scr),
               "changed=%s" % changed)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P11 (control #2)
def p11_target_removed_before_collection():
    """Remove one declared target from the validated workspace just before collection -> the mandatory-
    target invariant refuses in _collect_staged (pre-commit); no partial commit."""
    scr = sib_scratch("tgtrm")
    try:
        before = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        FI.arm()
        raised = False
        msg = ""
        try:
            ap = SA.StagedRoundApplier.for_repo(scr)
            _orig = ap._collect_staged
            def wrapped(ws, txn_dir):
                man = ap._read_txn_manifest(txn_dir) or {}
                rel = next(t["live"] for t in man.get("targets", [])
                           if t["name"] == "sibling_reference_vector")
                os.remove(os.path.join(ws, rel))       # a declared target vanishes before collection
                return _orig(ws, txn_dir)
            ap._collect_staged = wrapped
            ap.apply_snapshot(snapshot_for(scr, 20), generated_at=GEN)
        except SA.StagedValidationError as e:
            raised = "MANDATORY TARGET MISSING" in str(e)
            msg = str(e).splitlines()[0][:80]
        finally:
            FI.disarm()
        after = state_of(scr, CANON_RELS + FIXED_SIB_RELS)
        changed = [k for k in before if before[k] != after[k]]
        record("P11/#2 removing a declared target before collection refuses (mandatory-target invariant)",
               raised, msg)
        record("P11/#2 NO partial commit — every live target unchanged",
               not changed and not new_reference_vectors(scr), "changed=%s" % changed)
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P12 (control #3)
def p12_reference_value_corruption():
    """Corrupt ONE reference-vector player value while retaining its board id -> assert_current fails
    (the reference vector's internal arithmetic no longer holds)."""
    scr = sib_scratch("refval")
    try:
        refp = os.path.join(scr, SR.FV_FIX_REL, "reference_vector_%s.json" % PRE_BALANCED[:8])
        rv = json.load(open(refp))
        k = next(iter(rv["vector"]))
        rv["vector"][k] = int(rv["vector"][k]) + 7            # board_md5 + stored sum_v retained
        json.dump(rv, open(refp, "w"), indent=2)
        raised = False
        reason = ""
        try:
            SR.SiblingRepin(scr).assert_current()
        except SR.SiblingStaleError as e:
            raised = True
            reason = str(e).splitlines()[0][:90]
        v = SR.SiblingRepin(scr).verify()
        record("P12/#3 reference-vector value corruption (board id retained) -> assert_current FAILS",
               raised, reason)
        record("P12/#3 verify names the reference-vector arithmetic invariant",
               any("reference vector sum_v" in f for f in v["fails"]),
               "%s" % [f for f in v["fails"] if "reference vector" in f][:1])
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P13 (control #4)
def p13_fv_oracle_corruptions():
    """Corrupt the FV oracle's active count, sum, Sheezel value and reference filename INDEPENDENTLY while
    retaining the board id -> each fails on its OWN invariant in the live coherence gate."""
    scr = sib_scratch("fvorc")
    try:
        fvp = os.path.join(scr, SR.FV_TEST_REL)
        pristine = open(fvp, encoding="utf-8").read()
        cases = [
            ("active", "'active') == 804", "'active') == 803", "FV oracle active"),
            ("sum", "'sum_v') == 760253", "'sum_v') == 760252", "FV oracle sum_v"),
            ("sheezel", "'sheezel') == 9542", "'sheezel') == 9541", "FV oracle sheezel"),
            ("reference-filename", "reference_vector_1373e824.json", "reference_vector_deadbeef.json",
             "FV oracle reference-vector filename"),
        ]
        for label, old, new, needle in cases:
            open(fvp, "w", encoding="utf-8").write(pristine.replace(old, new))
            v = SR.SiblingRepin(scr).verify()
            record("P13/#4 FV-oracle %s drift (board id retained) fails on its invariant" % label,
                   (not v["ok"]) and any(needle in f for f in v["fails"]),
                   "%s" % [f for f in v["fails"] if needle in f][:1])
            open(fvp, "w", encoding="utf-8").write(pristine)      # restore for per-case isolation
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P14 (control #5)
def p14_board_bundle_corruptions():
    """Corrupt the working and public board bundles INDEPENDENTLY -> each fails the live coherence gate."""
    scr = sib_scratch("bvwork")
    try:
        wp = os.path.join(scr, SR.BOARD_VIEW_WORKING_REL)
        pre, obj, suf = _bundle_io(wp)
        obj["stamp"]["balanced_board_md5"] = "0" * 32
        _bundle_write(wp, pre, obj, suf)
        v = SR.SiblingRepin(scr).verify()
        record("P14/#5 working board-view corruption fails the coherence gate",
               (not v["ok"]) and any("working balanced_board_md5 stamp" in f for f in v["fails"]),
               "%s" % [f for f in v["fails"] if "working" in f][:1])
    finally:
        shutil.rmtree(scr, ignore_errors=True)
    scr = sib_scratch("bvpub")
    try:
        pp = os.path.join(scr, SR.BOARD_VIEW_PUBLIC_REL)
        pre, obj, suf = _bundle_io(pp)
        obj["players"][0]["v"] = int(obj["players"][0]["v"]) + 111
        _bundle_write(pp, pre, obj, suf)
        v = SR.SiblingRepin(scr).verify()
        record("P14/#5 public board-view corruption fails the coherence gate",
               (not v["ok"]) and any("public rows disagree" in f for f in v["fails"]),
               "%s" % [f for f in v["fails"] if "public" in f][:1])
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P15 (control #6)
def p15_view_only_reconcile_repairs():
    """A view-only corruption (pins/contract/FV board id all current) must NOT read as a no-op: standalone
    reconcile REPAIRS the board view and reports changed, not no_op."""
    scr = sib_scratch("viewrepair")
    try:
        wp = os.path.join(scr, SR.BOARD_VIEW_WORKING_REL)
        pre, obj, suf = _bundle_io(wp)
        obj["stamp"]["balanced_board_md5"] = "0" * 32
        _bundle_write(wp, pre, obj, suf)
        stale = SR.SiblingRepin(scr).verify()
        res = SR.SiblingRepin(scr).reconcile(round_n=19)
        healed = SR.SiblingRepin(scr).verify()
        record("P15/#6 view-only corruption makes the live gate STALE (not silently current)",
               not stale["ok"] and any("working" in f for f in stale["fails"]))
        record("P15/#6 standalone reconcile REPAIRS the view (changed, NOT a no-op)",
               res.get("changed") is True and res.get("no_op") is False,
               "changed=%s no_op=%s" % (res.get("changed"), res.get("no_op")))
        record("P15/#6 the live gate is coherent again after repair", healed["ok"],
               "fails=%s" % healed["fails"][:1])
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P16 (final correction 1)
def p16_sum_preserving_vector_full_compare():
    """A SUM-PRESERVING reference-vector corruption (player A +1, player B -1; board id, active, total and
    Sheezel all unchanged) passes the no-build internal-arithmetic gate but MUST fail the authoritative
    `check --full`, which rebuilds the sibling and compares the COMPLETE vector."""
    scr = sib_scratch("sumpreserve")
    try:
        refp = os.path.join(scr, SR.FV_FIX_REL, "reference_vector_%s.json" % PRE_BALANCED[:8])
        rv = json.load(open(refp))
        keys = list(rv["vector"])
        a, b = keys[0], keys[1]
        rv["vector"][a] = int(rv["vector"][a]) + 1
        rv["vector"][b] = int(rv["vector"][b]) - 1        # sum-preserving; active/total/Sheezel unchanged
        json.dump(rv, open(refp, "w"), indent=2)
        v = SR.SiblingRepin(scr).verify()
        record("P16/D1 no-build verify() MISSES the sum-preserving corruption (internal arithmetic intact)",
               v["ok"], "verify_ok=%s" % v["ok"])
        reason = ""
        try:
            SR.SiblingRepin(scr).assert_current(full=True)
        except SR.SiblingStaleError as e:
            reason = str(e).splitlines()[0]
        record("P16/D1 authoritative check --full FAILS specifically on the EXACT-VECTOR mismatch",
               "EXACT-VECTOR MISMATCH" in reason, reason[:90])
    finally:
        shutil.rmtree(scr, ignore_errors=True)


# ================================================================================ P17 (final correction 2)
def p17_fv_oracle_only_reconcile_repairs():
    """FV-oracle-only drift (a wrong active / sum / Sheezel / reference filename while the reference vector
    is already current): for EACH, verify() fails on its named invariant, standalone reconcile reports
    changed=True (NOT a no-op) and REPAIRS the actual corrupt token, and verify() + check --full are green
    afterward."""
    cases = [
        ("active", "'active') == 804", "'active') == 803", "FV oracle active", "'active') == 804"),
        ("sum", "'sum_v') == 760253", "'sum_v') == 760252", "FV oracle sum_v", "'sum_v') == 760253"),
        ("sheezel", "'sheezel') == 9542", "'sheezel') == 9541", "FV oracle sheezel", "'sheezel') == 9542"),
        ("reference-filename", "reference_vector_1373e824.json", "reference_vector_deadbeef.json",
         "FV oracle reference-vector filename", "reference_vector_1373e824.json"),
    ]
    for label, old, new, needle, repaired_token in cases:
        scr = sib_scratch("fvonly_%s" % label.split("-")[0])
        try:
            fvp = os.path.join(scr, SR.FV_TEST_REL)
            src = open(fvp, encoding="utf-8").read()
            open(fvp, "w", encoding="utf-8").write(src.replace(old, new))
            v = SR.SiblingRepin(scr).verify()
            record("P17/D2 %s drift: verify() fails on its invariant" % label,
                   (not v["ok"]) and any(needle in f for f in v["fails"]),
                   "%s" % [f for f in v["fails"] if needle in f][:1])
            res = SR.SiblingRepin(scr).reconcile(round_n=19)
            after = open(fvp, encoding="utf-8").read()
            v2 = SR.SiblingRepin(scr).verify()
            record("P17/D2 %s drift: reconcile REPAIRS it (changed, not a no-op) + verify() green" % label,
                   res.get("changed") is True and res.get("no_op") is False
                   and repaired_token in after and new not in after and v2["ok"],
                   "changed=%s no_op=%s repaired=%s verify=%s"
                   % (res.get("changed"), res.get("no_op"), repaired_token in after, v2["ok"]))
            full = None
            try:
                full = SR.SiblingRepin(scr).assert_current(full=True)
            except SR.SiblingStaleError as e:
                full = {"err": str(e)[:100]}
            record("P17/D2 %s drift: check --full green afterward" % label,
                   isinstance(full, dict) and full.get("mode") == "full+build-and-compare", "%s" % full)
        finally:
            shutil.rmtree(scr, ignore_errors=True)


def main():
    print("=" * 96)
    print("SINGLE-TRANSACTION SIBLING INTEGRATION PROOF (ITEM 408 item 5) — scratch only; gate OFF")
    print("=" * 96)
    p1_noop_reproduction()
    p2_single_transaction_advance()
    p3_generation_failure()
    p4_validation_failure()
    p5_fault_after_first_canonical()
    p6_fault_after_sibling_replacement()
    p7_crash_recovery()
    p8_active_count_derived()
    p9_launchers_route_through_python()
    p10_public_removed_before_validation()
    p11_target_removed_before_collection()
    p12_reference_value_corruption()
    p13_fv_oracle_corruptions()
    p14_board_bundle_corruptions()
    p15_view_only_reconcile_repairs()
    p16_sum_preserving_vector_full_compare()
    p17_fv_oracle_only_reconcile_repairs()
    npass = sum(1 for r in RESULTS if r["ok"])
    print("\n  " + "-" * 74)
    print("  RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "INTEGRATION_RESULTS.json")
    with open(out, "w") as f:
        json.dump({"passed": npass, "total": len(RESULTS), "results": RESULTS}, f, indent=2)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
