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
  3. UNKNOWN / CONFLICTING / MISSING curve selection FAILS CLOSED — unknown pathway, wrong release store,
     missing contract, and an engine curve file whose md5 drifted from the contract;
  4. a board-id mismatch STILL FAILS CLOSED (the ring fence is preserved);
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
    check(str(st.get("board", ""))[:8] == "06d8af60", "CASE1 board id 06d8af60 in stamp")
    check(st.get("releaseVersion") == "v2.11-rc1" and st.get("asOfRound") == 14,
          "CASE1 stamp carries releaseVersion v2.11-rc1 + asOfRound 14")
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
    check(rc == 2 and b is not None and b.get("halt"),
          "CASE2a L1b path under RL_PVC2 fails closed", "rc=%d" % rc)

    # ---- CASE 2b: a board whose PVC is the L1b curve while the contract adopts RL_PVC2 ----------------
    lb = load_real_board()
    lb["pvc"] = {str(k): v for k, v in load_curve_values("pvc_curve_L1b.json").items()}
    l1bboard = os.path.join(TMP, "board_l1b_pvc.js")
    write_board(l1bboard, lb)
    rc, b, log = run_ingest(TMP, RL_UI_BOARD_BUNDLE=l1bboard, RL_UI_OUT=os.path.join(TMP, "o2b.js"))
    check(rc == 2 and b is not None and b.get("halt"),
          "CASE2b L1b-PVC board under an RL_PVC2 contract fails closed", "rc=%d" % rc)

    # ---- CASE 3a: unknown pathway ---------------------------------------------------------------------
    c3 = json.load(open(REAL_CONTRACT)); c3["adopted_pathway"] = "RL_BOGUS"
    bad3 = os.path.join(TMP, "contract_unknown.json"); json.dump(c3, open(bad3, "w"))
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=bad3, RL_UI_OUT=os.path.join(TMP, "o3a.js"))
    check(rc == 2 and b is not None and b.get("halt"), "CASE3a unknown adopted_pathway fails closed", "rc=%d" % rc)

    # ---- CASE 3b: conflicting release store -----------------------------------------------------------
    c3b = json.load(open(REAL_CONTRACT)); c3b["store_md5"] = "deadbeefdeadbeefdeadbeefdeadbeef"
    bad3b = os.path.join(TMP, "contract_store.json"); json.dump(c3b, open(bad3b, "w"))
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=bad3b, RL_UI_OUT=os.path.join(TMP, "o3b.js"))
    check(rc == 2 and b is not None and b.get("halt"), "CASE3b wrong release store fails closed", "rc=%d" % rc)

    # ---- CASE 3c: missing contract --------------------------------------------------------------------
    rc, b, log = run_ingest(TMP, RL_UI_CURVE_CONTRACT=os.path.join(TMP, "nope.json"),
                            RL_UI_OUT=os.path.join(TMP, "o3c.js"))
    check(rc == 2 and b is not None and b.get("halt"), "CASE3c missing contract fails closed", "rc=%d" % rc)

    # ---- CASE 3d: engine curve file md5 drift (temp engine dir with a mutated v2 curve) ---------------
    eng2 = os.path.join(TMP, "engine_drift")
    os.makedirs(eng2)
    for nm in ("pvc_curve_v2.json", "pvc_curve_L1b.json"):
        doc = json.load(open(os.path.join(REAL_ENGINE, nm)))
        if nm == "pvc_curve_v2.json":
            doc["_tamper"] = "byte drift — changes the FILE md5 (curve values untouched)"
        json.dump(doc, open(os.path.join(eng2, nm), "w"))
    rc, b, log = run_ingest(TMP, RL_UI_ENGINE_DIR=eng2, RL_UI_OUT=os.path.join(TMP, "o3d.js"))
    check(rc == 2 and b is not None and b.get("halt"),
          "CASE3d engine curve file md5 drift fails closed", "rc=%d" % rc)

    # ---- CASE 4: board-id mismatch still fails closed (ring fence) ------------------------------------
    mm = load_real_board()
    mm.setdefault("stamp", {})["board"] = "a" * 32
    mm["stamp"]["board_md5"] = "a" * 32
    mm_board = os.path.join(TMP, "board_mismatch.js")
    write_board(mm_board, mm)
    rc, b, log = run_ingest(TMP, RL_UI_BOARD_BUNDLE=mm_board, RL_UI_OUT=os.path.join(TMP, "o4.js"))
    check(rc == 2 and b is not None and b.get("halt"),
          "CASE4 board-id mismatch still fails closed (ring fence)", "rc=%d" % rc)

print("\n  " + "-" * 66)
print("  %d/%d passed" % (n - fails, n))
sys.exit(1 if fails else 0)
