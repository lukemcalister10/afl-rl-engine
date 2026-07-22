#!/usr/bin/env python3
"""v2.11-rc1 — CLUB-VALUATION CURVE-PROVENANCE + conservation proof (fail-closed; TEMP fixtures only).

    Run:  python3 ui/tests/club_curve_provenance.test.py   (exit 0 = all pass, exit 1 = a failure)

Proves the CORRECTED ui/tools/ingest_inputs.py release-active pick-curve resolver (it no longer hardcodes
pvc_curve_L1b.json; it resolves the release-active curve deterministically from the explicit fail-closed
contract ui/release_pick_curve.json + the engine curve's OWN self-declared identity):

  1. the ACCEPTED v2.11 curve (RL_PVC2 / pvc_curve_v2.json) PASSES + club/pick totals conserved (16 clubs,
     160 picks; Sum per-club picks == 160) and every pick is priced from the v2 curve (not the workbook);
  2. L1b supplied while RL_PVC2 is active FAILS CLOSED — both (a) a contract that points the RL_PVC2 pathway
     at pvc_curve_L1b.json, and (b) a board whose PVC is the L1b curve while the contract adopts RL_PVC2;
  3. UNKNOWN / CONFLICTING / MISSING curve selection FAILS CLOSED — unknown/missing pathway, wrong frozen
     curve-source store, missing contract, both curve-md5 axes, pin1 and engine-file drift;
  4. board id/store/round mismatch and an incomplete live manifest STILL FAIL CLOSED (ring fence preserved);
  5. NO workbook value is used as a valuation input — pick prices equal the engine-curve mean (price_pick),
     independent of the pick workbook's value columns;
  6. existing Board/Player/Trade views cannot regress — the ingest writes ONLY club_valuation.js and never
     touches the board_view bundles (asserted byte-unchanged across a fixture run).

Every case runs ui/tools/ingest_inputs.py as a SUBPROCESS with RL_UI_* path overrides into a scratch dir.
Production ui/data/club_valuation.js is never overwritten (RL_UI_OUT -> temp). No guard is weakened to pass.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
INGEST = os.path.join(REPO, "ui", "tools", "ingest_inputs.py")
REAL_BOARD = os.path.join(REPO, "ui", "data", "board_view_working.js")
REAL_CONTRACT = os.path.join(REPO, "ui", "release_pick_curve.json")
REAL_ENGINE = os.path.join(REPO, "engine", "rl_after")
REAL_BOOT = os.path.join(REPO, "data", "expected_boot.json")
REAL_INPUTS = os.path.join(REPO, "docs", "inputs")

fails = 0
n = 0


def check(cond, label, extra=""):
    global fails, n
    n += 1
    if cond:
        print("  [PASS] %s%s" % (label, ("  (%s)" % extra) if extra else ""))
    else:
        fails += 1
        print("  [FAIL] %s%s" % (label, ("  (%s)" % extra) if extra else ""))


def _bundle_obj(js_text):
    return json.loads(js_text[js_text.index("{"): js_text.rindex("}") + 1])


def read_bundle(path):
    if not path or not os.path.exists(path):
        return None
    return _bundle_obj(open(path, encoding="utf-8").read())


def write_board(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        f.write("window.__MATCHDAY_WORKING__ = " + json.dumps(obj, ensure_ascii=False) + ";\n")


def halt_text(bundle):
    """Return the live fail-closed reason emitted by ingest_inputs.py, never a guessed label."""
    halt = (bundle or {}).get("halt") or ""
    return str(halt.get("reason") if isinstance(halt, dict) else halt)


def halt_names(bundle, *needles):
    text = halt_text(bundle).lower()
    return bool(text) and all(str(n).lower() in text for n in needles)


def dump_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)
    return path


def temp_curve_and_contract(TMP, tag, mutate_curve):
    """Scratch-only fixture: write a temp engine dir holding a MUTATED pvc_curve_v2.json, plus a temp
    contract whose pick_curve_file_md5 tracks the mutated file bytes and whose pick_curve_curve_md5 stays
    mutually equal to the curve's OWN curve_md5 field. This clears the resolver's name / file-md5 /
    curve-md5 guards deliberately, so the tamper reaches the SPECIFIC downstream guard under test rather
    than tripping an earlier md5 guard. Never touches production data. Returns (engine_dir, contract_path)."""
    engdir = os.path.join(TMP, "eng_" + tag)
    os.makedirs(engdir)
    curve = json.load(open(os.path.join(REAL_ENGINE, "pvc_curve_v2.json")))
    mutate_curve(curve)
    cpath = os.path.join(engdir, "pvc_curve_v2.json")
    with open(cpath, "w", encoding="utf-8") as f:
        json.dump(curve, f)
    contract = json.load(open(REAL_CONTRACT))
    contract["pick_curve_file_md5"] = hashlib.md5(open(cpath, "rb").read()).hexdigest()
    contract["pick_curve_curve_md5"] = str(curve.get("curve_md5"))
    return engdir, dump_json(os.path.join(TMP, "contract_" + tag + ".json"), contract)


def run_ingest(scratch, **overrides):
    """Run the ingest subprocess. Defaults are the REAL production artifacts; overrides redirect paths.
    Returns (returncode, out_bundle_obj_or_None, combined_log)."""
    env = os.environ.copy()
    out = overrides.pop("RL_UI_OUT", os.path.join(scratch, "club_valuation.js"))
    env["RL_UI_OUT"] = out
    env.setdefault("RL_UI_BOARD_BUNDLE", REAL_BOARD)
    env.setdefault("RL_UI_CURVE_CONTRACT", REAL_CONTRACT)
    env.setdefault("RL_UI_ENGINE_DIR", REAL_ENGINE)
    env.setdefault("RL_UI_BOOT", REAL_BOOT)
    env.setdefault("RL_UI_INPUTS", REAL_INPUTS)
    for k, v in overrides.items():
        env[k] = v
    r = subprocess.run([sys.executable, INGEST], capture_output=True, text=True, env=env)
    return r.returncode, read_bundle(out), (r.stdout + r.stderr)


def load_real_board():
    return _bundle_obj(open(REAL_BOARD, encoding="utf-8").read())


def load_curve_values(name):
    doc = json.load(open(os.path.join(REAL_ENGINE, name), encoding="utf-8"))
    return {int(k): int(v) for k, v in doc["curve"].items()}


# =====================================================================================================
print("=== CLUB-VALUATION CURVE-PROVENANCE + conservation proof ===")

with tempfile.TemporaryDirectory(prefix="clubprov_") as TMP:

    # ---- CASE 1: the accepted v2.11 curve passes + totals conserved + priced from the curve ----------
    board_before = open(REAL_BOARD, "rb").read()
    rc, b, log = run_ingest(TMP)
    check(rc == 0, "CASE1 accepted v2.11 curve: clean exit 0", "rc=%d" % rc)
    check(b is not None and b.get("halt") is None, "CASE1 no HALT object in the bundle")
    check(b is not None and len(b.get("clubs", [])) == 16, "CASE1 16 clubs present",
          "%s" % (len(b.get("clubs", [])) if b else None))
    npk = sum(len(v) for v in (b or {}).get("picksByTeam", {}).values())
    check(npk == 160, "CASE1 160 picks present", "picks=%d" % npk)
    check(b is not None and sum(c["nPicks"] for c in b["clubs"]) == 160,
          "CASE1 pick-count conservation: Sum per-club nPicks == 160")
    st = (b or {}).get("stamp", {})
    check(st.get("pvcPathway") == "RL_PVC2", "CASE1 resolved pathway == RL_PVC2", st.get("pvcPathway"))
    check(st.get("pvcCurveMd5") == "89c14729", "CASE1 resolved curve_md5 == 89c14729", st.get("pvcCurveMd5"))
    check(str(st.get("board", ""))[:8] == "2ab73a6f", "CASE1 board id 2ab73a6f in stamp")
    check(st.get("releaseVersion") == "v2.11-final-rc1-PROVISIONAL" and st.get("asOfRound") == 14,
          "CASE1 stamp carries releaseVersion v2.11-final-rc1-PROVISIONAL + asOfRound 14")
    for stale in ("790136a3", "v2.10", "pvc_curve_L1b", "b1fd0bce", "fc7045d6"):
        raw = json.dumps(b)
        check(stale not in raw, "CASE1 no stale token '%s' carried forward" % stale)

    # no-workbook-value: every pick price == the engine-curve mean (price_pick), never a sheet value.
    sys.path.insert(0, os.path.join(REPO, "ui", "tools"))
    import ingest_inputs as ing  # noqa: E402  (imported for the pure price_pick, no path dependency)
    v2 = load_curve_values("pvc_curve_v2.json")
    priced_ok = True
    sample = 0
    for team, picks in (b or {}).get("picksByTeam", {}).items():
        for p in picks:
            expect = round(ing.price_pick(v2, p["low"], p["high"], p["year"]))
            if expect != p["value"]:
                priced_ok = False
            sample += 1
    check(priced_ok and sample == 160,
          "CASE1 all 160 pick values == engine-curve mean (no workbook value ingested)", "checked=%d" % sample)

    # ---- CASE 6: existing views cannot regress — ingest wrote ONLY club_valuation.js -----------------
    check(open(REAL_BOARD, "rb").read() == board_before,
          "CASE6 board_view_working.js byte-unchanged by the ingest (Board/Player/Trade views intact)")
    need_fields = {"team", "display", "overall", "totalPlayer", "totalPicks", "best23", "nPicks", "best23Keys"}
    club_ok = b is not None and all(need_fields <= set(c) for c in b["clubs"])
    check(club_ok, "CASE6 every club carries the fields the Club view reads (no shape regression)")

    # ---- CASE 2a: L1b supplied while RL_PVC2 active — contract points RL_PVC2 at pvc_curve_L1b.json ---
    c1 = json.load(open(REAL_CONTRACT))
    c1["pick_curve_path"] = "engine/rl_after/pvc_curve_L1b.json"
    bad1 = os.path.join(TMP, "contract_l1b_path.json")
    json.dump(c1, open(bad1, "w"))
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=bad1, RL_UI_OUT=os.path.join(TMP, "o2a.js"))
    check(rc == 2 and halt_names(b, "must load", "pvc_curve_l1b"),
          "CASE2a L1b path under RL_PVC2 fires the pathway/filename conflict halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 2b: a board whose PVC is the L1b curve while the contract adopts RL_PVC2 ----------------
    lb = load_real_board()
    lb["pvc"] = {str(k): v for k, v in load_curve_values("pvc_curve_L1b.json").items()}
    l1bboard = os.path.join(TMP, "board_l1b_pvc.js")
    write_board(l1bboard, lb)
    rc, b, log = run_ingest(TMP, RL_UI_BOARD_BUNDLE=l1bboard, RL_UI_OUT=os.path.join(TMP, "o2b.js"))
    check(rc == 2 and halt_names(b, "stale-curve guard", "byte-match"),
          "CASE2b L1b-PVC board under an RL_PVC2 contract fires the stale-curve byte-match halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 3a: unknown pathway ---------------------------------------------------------------------
    c3 = json.load(open(REAL_CONTRACT)); c3["adopted_pathway"] = "RL_BOGUS"
    bad3 = os.path.join(TMP, "contract_unknown.json"); json.dump(c3, open(bad3, "w"))
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=bad3, RL_UI_OUT=os.path.join(TMP, "o3a.js"))
    check(rc == 2 and halt_names(b, "unknown curve-selection", "rl_bogus"),
          "CASE3a unknown adopted_pathway fires the unknown-pathway halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 3b: curve/source-store binding (the resolver's REAL key) --------------------------------
    c3b = json.load(open(REAL_CONTRACT))
    c3b["curve_source_store_md5"] = "deadbeefdeadbeefdeadbeefdeadbeef"
    bad3b = dump_json(os.path.join(TMP, "contract_curve_source_store.json"), c3b)
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=bad3b, RL_UI_OUT=os.path.join(TMP, "o3b.js"))
    check(rc == 2 and halt_names(b, "binds store", "deadbeef"),
          "CASE3b wrong curve_source_store_md5 fires the live curve-store-binding halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 3c: missing contract --------------------------------------------------------------------
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=os.path.join(TMP, "nope.json"),
                            RL_UI_OUT=os.path.join(TMP, "o3c.js"))
    check(rc == 2 and halt_names(b, "release pick-curve contract missing"),
          "CASE3c missing contract fires the contract-missing halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 3d: engine curve file md5 drift (temp engine dir with a mutated v2 curve) ---------------
    eng2 = os.path.join(TMP, "engine_drift")
    os.makedirs(eng2)
    for nm in ("pvc_curve_v2.json", "pvc_curve_L1b.json"):
        doc = json.load(open(os.path.join(REAL_ENGINE, nm)))
        if nm == "pvc_curve_v2.json":
            doc["_tamper"] = "byte drift — changes the FILE md5 (curve values untouched)"
        json.dump(doc, open(os.path.join(eng2, nm), "w"))
    rc, b, log = run_ingest(TMP, RL_UI_ENGINE_DIR=eng2, RL_UI_OUT=os.path.join(TMP, "o3d.js"))
    check(rc == 2 and halt_names(b, "curve drift", "engine curve file changed"),
          "CASE3d engine curve file md5 drift fires the file-md5 CURVE DRIFT halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 4: board-id mismatch still fails closed (ring fence) ------------------------------------
    mm = load_real_board()
    mm.setdefault("stamp", {})["board"] = "a" * 32
    mm["stamp"]["board_md5"] = "a" * 32
    mm_board = os.path.join(TMP, "board_mismatch.js")
    write_board(mm_board, mm)
    rc, b, log = run_ingest(TMP, RL_UI_BOARD_BUNDLE=mm_board, RL_UI_OUT=os.path.join(TMP, "o4.js"))
    check(rc == 2 and halt_names(b, "board id mismatch", "regenerate board_view"),
          "CASE4 board-id mismatch fires the ring-fence board-id halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 5: live round enforcement + manifest completeness (the resolver's REAL keys) -------------
    round_bad = load_real_board()
    round_bad.setdefault("stamp", {})["asOfRound"] = int(json.load(open(REAL_BOOT))["as_of_round"]) - 1
    bad5 = os.path.join(TMP, "board_round_mismatch.js")
    write_board(bad5, round_bad)
    rc, b, log = run_ingest(TMP, RL_UI_BOARD_BUNDLE=bad5, RL_UI_OUT=os.path.join(TMP, "o5a.js"))
    check(rc == 2 and halt_names(b, "board round", "mismatch"),
          "CASE5a board-stamp asOfRound mismatch vs expected_boot fires the live round halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    boot5b = json.load(open(REAL_BOOT)); boot5b.pop("as_of_round", None)
    bad5b = dump_json(os.path.join(TMP, "boot_noround.json"), boot5b)
    rc, b, log = run_ingest(TMP, RL_UI_BOOT=bad5b, RL_UI_OUT=os.path.join(TMP, "o5b.js"))
    check(rc == 2 and halt_names(b, "manifest lacks", "as_of_round"),
          "CASE5b missing expected_boot.as_of_round fires manifest-incomplete halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 7: every remaining fail-closed identity key has a live tamper case ------------------------
    # release_version
    c7rv = json.load(open(REAL_CONTRACT)); c7rv["release_version"] = "v0-tampered"
    p7rv = dump_json(os.path.join(TMP, "contract_release_version.json"), c7rv)
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=p7rv, RL_UI_OUT=os.path.join(TMP, "o7rv.js"))
    check(rc == 2 and halt_names(b, "release_version", "v0-tampered"),
          "CASE7 release_version mismatch fires its live halt", "rc=%d halt=%s" % (rc, halt_text(b)))

    # curve payload md5 (distinct from CASE3d's full-file md5)
    c7cm = json.load(open(REAL_CONTRACT)); c7cm["pick_curve_curve_md5"] = "deadbeef"
    p7cm = dump_json(os.path.join(TMP, "contract_curve_payload_md5.json"), c7cm)
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=p7cm, RL_UI_OUT=os.path.join(TMP, "o7cm.js"))
    check(rc == 2 and halt_names(b, "curve_md5", "deadbeef"),
          "CASE7 pick_curve_curve_md5 mismatch fires its live halt", "rc=%d halt=%s" % (rc, halt_text(b)))

    # pin1
    c7p1 = json.load(open(REAL_CONTRACT)); c7p1["numeraire_pin1"] = 2999
    p7p1 = dump_json(os.path.join(TMP, "contract_pin1.json"), c7p1)
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=p7p1, RL_UI_OUT=os.path.join(TMP, "o7p1.js"))
    check(rc == 2 and halt_names(b, "pin1", "numeraire"),
          "CASE7 numeraire_pin1 mismatch fires its live halt", "rc=%d halt=%s" % (rc, halt_text(b)))

    # board source store
    store_bad = load_real_board()
    store_bad.setdefault("stamp", {})["store_md5"] = "b" * 32
    store_bad["stamp"]["store"] = "b" * 8
    p7st = os.path.join(TMP, "board_store_mismatch.js"); write_board(p7st, store_bad)
    rc, b, log = run_ingest(TMP, RL_UI_BOARD_BUNDLE=p7st, RL_UI_OUT=os.path.join(TMP, "o7st.js"))
    check(rc == 2 and halt_names(b, "board store", "mismatch"),
          "CASE7 board source-store mismatch fires its live halt", "rc=%d halt=%s" % (rc, halt_text(b)))

    # contract required-field completeness: pathway itself missing, not merely unknown
    c7miss = json.load(open(REAL_CONTRACT)); c7miss.pop("adopted_pathway", None)
    p7miss = dump_json(os.path.join(TMP, "contract_missing_pathway.json"), c7miss)
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=p7miss, RL_UI_OUT=os.path.join(TMP, "o7miss.js"))
    check(rc == 2 and halt_names(b, "incomplete", "adopted_pathway"),
          "CASE7 missing pathway fires contract-incomplete halt", "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 8: curve self-declared GATE mismatch (resolver gate/pathway guard) ----------------------
    # Temp engine curve whose gate token declares the WRONG pathway; contract file-md5 updated so the
    # earlier file-md5 guard passes and curve payload identity stays coherent -> the GATE guard fires.
    def _mut_gate(c):
        c["gate"] = "RL_PVCADOPT (tampered gate token — declares the wrong pathway)"
    eng8, k8 = temp_curve_and_contract(TMP, "gate", _mut_gate)
    rc, b, log = run_ingest(TMP, RL_UI_ENGINE_DIR=eng8, RL_UI_CURVE_CONTRACT=k8,
                            RL_UI_OUT=os.path.join(TMP, "o8.js"))
    check(rc == 2 and halt_names(b, "self-declares gate", "adopted pathway"),
          "CASE8 curve self-declared gate mismatch fires the gate/pathway halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 9: engine curve document PIN != 3000 (resolver engine-curve numeraire guard) ------------
    def _mut_pin(c):
        c["pin"] = 2999
    eng9, k9 = temp_curve_and_contract(TMP, "enginepin", _mut_pin)
    rc, b, log = run_ingest(TMP, RL_UI_ENGINE_DIR=eng9, RL_UI_CURVE_CONTRACT=k9,
                            RL_UI_OUT=os.path.join(TMP, "o9.js"))
    check(rc == 2 and halt_names(b, "pin != 3000", "numeraire drift"),
          "CASE9 engine curve top-level pin != 3000 fires the engine-curve numeraire halt",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 10: board PVC pick-1 != 3000 (assert_pvc pick-1 guard; byte-match cleared first) --------
    # Board PVC and the resolved engine curve are made to BYTE-MATCH (both carry pick1=2999), so the
    # earlier byte-match guard passes and the PVC pick-1 numeraire guard is the one that fires.
    def _mut_curve_p1(c):
        c["curve"]["1"] = 2999
    eng10, k10 = temp_curve_and_contract(TMP, "pvcpick1", _mut_curve_p1)
    b10 = load_real_board()
    b10["pvc"] = {str(k): v for k, v in load_curve_values("pvc_curve_v2.json").items()}
    b10["pvc"]["1"] = 2999
    brd10 = os.path.join(TMP, "board_pvc_pick1.js"); write_board(brd10, b10)
    rc, b, log = run_ingest(TMP, RL_UI_ENGINE_DIR=eng10, RL_UI_CURVE_CONTRACT=k10,
                            RL_UI_BOARD_BUNDLE=brd10, RL_UI_OUT=os.path.join(TMP, "o10.js"))
    check(rc == 2 and halt_names(b, "pvc pick1 != 3000", "numeraire drift"),
          "CASE10 board PVC pick-1 != 3000 fires the PVC pick-1 numeraire halt (byte-match cleared first)",
          "rc=%d halt=%s" % (rc, halt_text(b)))

    # ---- CASE 11: board PVC non-monotone (assert_pvc monotonicity guard; byte-match+pick1 cleared) ----
    # Board PVC and engine curve are made to BYTE-MATCH with pick1==3000 intact, but carry ONE increase
    # (pick 60 lifted above pick 59), so the monotonicity guard is the specific one that fires.
    def _mut_curve_mono(c):
        c["curve"]["60"] = 600   # > pick 59 (545); pick 1 stays 3000; exactly one increase
    eng11, k11 = temp_curve_and_contract(TMP, "pvcmono", _mut_curve_mono)
    b11 = load_real_board()
    b11["pvc"] = {str(k): v for k, v in load_curve_values("pvc_curve_v2.json").items()}
    b11["pvc"]["60"] = 600
    brd11 = os.path.join(TMP, "board_pvc_mono.js"); write_board(brd11, b11)
    rc, b, log = run_ingest(TMP, RL_UI_ENGINE_DIR=eng11, RL_UI_CURVE_CONTRACT=k11,
                            RL_UI_BOARD_BUNDLE=brd11, RL_UI_OUT=os.path.join(TMP, "o11.js"))
    check(rc == 2 and halt_names(b, "monotone non-increasing"),
          "CASE11 board PVC non-monotone fires the monotonicity halt (byte-match + pick1 cleared first)",
          "rc=%d halt=%s" % (rc, halt_text(b)))

print("\n  " + "-" * 66)
print("  %d/%d passed" % (n - fails, n))
sys.exit(1 if fails else 0)
