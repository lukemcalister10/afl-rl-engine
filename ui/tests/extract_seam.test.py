#!/usr/bin/env python3
"""v2.11 UI/RELEASE-SEAM — focused extractor proof (fail-closed; TEMP board + TEMP boot only).

    Run:  python3 ui/tests/extract_seam.test.py     (exit 0 = all pass, exit 1 = a failure)

Proves the extract_board_view.py seam WITHOUT baking, selecting or promoting any board:
  1. a Leg-F board transfers ALL required phantom fields to the working bundle;
  2. entrant metadata (PVC 83538 / expected slots ~103.4 / seal a17aafed) survives extraction exactly;
  3. working-bundle release/round metadata comes from the boot manifest (release_version / as_of_round);
  4. MISSING release/round metadata renders neither "v2.10" nor "Round 17";
  5. a mismatched board pin (and a mismatched store pin) STILL fails closed;
  6. the public bundle does not leak prohibited (owner/internal/phantom/lens/id) fields.

Every run uses a TEMPORARY board (the read-only diagnostic candidate fixture) and a TEMPORARY boot
manifest under a scratch dir. Production data/ and ui/data/ are never read or written. No ring-fence
assertion is weakened to make the fixture run — the fixture is given a self-consistent temp environment.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXTRACT = os.path.join(REPO, "ui", "tools", "extract_board_view.py")
STORE = os.path.join(REPO, "engine", "rl_after", "rl_model_data.json")
# The seam is exercised against a COMMITTED, self-contained schema fixture — NO git / network / remote-branch
# access at test time. The fixture is a reduced, byte-for-byte-authentic slice of the recovery board that used
# to be read at runtime via `git show`; that source commit is dangling in GitHub's object DB and unreachable
# from any advertised branch/tag (Actions fetch-depth:0 cannot supply it), which made the runtime read
# non-portable. Provenance (source commit / path / blob SHA + "reduced schema fixture, not a production board
# or accepted valuation oracle") is recorded in the fixture's own `_fixture_provenance` block:
#   source commit 6720dfae438ec4eef87a956d63ee4468c05105f4
#   source path   recovery_artifacts/v2.11/post_legf_candidate/rl_app_data.json
#   source blob   e119b9e34bf3ff1e415a41d8150034e437e25d62
FIXTURE = os.path.join(HERE, "fixtures", "extract_seam_legf_schema.json")

fails = 0
n = 0


def check(cond, label, extra=""):
    global fails, n
    n += 1
    if cond:
        print("  [PASS] " + label)
    else:
        fails += 1
        print("  [FAIL] " + label + ("  " + extra if extra else ""))


def md5_file(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def load_bundle(path, key):
    t = open(path).read()
    return t, json.loads(t[t.index("{"):t.rindex("}") + 1])


def run_extractor(src, boot, out_dir, store=STORE):
    env = dict(os.environ)
    env.update(RL_UI_SRC=src, RL_UI_BOOT=boot, RL_UI_STORE=store, RL_UI_OUT_DIR=out_dir)
    return subprocess.run([sys.executable, EXTRACT], env=env, capture_output=True, text=True)


def write_boot(path, board_md5, store_md5, release_version="__OMIT__", as_of_round="__OMIT__",
               balanced_board_md5="__OMIT__"):
    boot = {
        "board": board_md5,
        "store": store_md5,
        "engine_head": "deadbeefdeadbeefdeadbeef",
        "register": "652d83e87780e415a01a2de6d8b3cc57",
        "config": "c2d233aec1041a2d24a66990a584f552d59b3902f97eddbf76867d724071b53b",
        "panel": "PASS 10/10 (fixture)",
    }
    if release_version != "__OMIT__":
        boot["release_version"] = release_version
    if as_of_round != "__OMIT__":
        boot["as_of_round"] = as_of_round
    if balanced_board_md5 != "__OMIT__":
        boot["balanced_board_md5"] = balanced_board_md5
    json.dump(boot, open(path, "w"))


def main():
    print("v2.11 UI/RELEASE-SEAM — extractor proof (temp board + temp boot; fail-closed)\n  " + "-" * 66)

    # ---- load the COMMITTED schema fixture, staged as a TEMPORARY board (no git / no network) ------
    check(os.path.exists(FIXTURE),
          "read committed schema fixture %s (schema fixture only, NOT a production board)" % os.path.relpath(FIXTURE, REPO))
    if not os.path.exists(FIXTURE):
        print("  fixture missing; aborting")
        return 1
    fixture_text = open(FIXTURE).read()
    src_doc = json.loads(fixture_text)
    check(isinstance(src_doc, dict) and isinstance(src_doc.get("active"), list) and len(src_doc["active"]) > 0,
          "committed fixture is a valid board (non-empty active list)")
    store_md5 = md5_file(STORE)

    tmp = tempfile.mkdtemp(prefix="seam_")
    src_path = os.path.join(tmp, "rl_app_data.json")
    open(src_path, "w").write(fixture_text)
    board_md5 = md5_file(src_path)

    # ==== SCENARIO A — full Leg-F board, boot carries release_version + as_of_round =================
    boot_a = os.path.join(tmp, "boot_a.json")
    write_boot(boot_a, board_md5, store_md5, release_version="v2.11-TEST", as_of_round=14)
    out_a = os.path.join(tmp, "out_a")
    r = run_extractor(src_path, boot_a, out_a)
    check(r.returncode == 0, "extractor runs fail-closed on the candidate fixture (temp board + temp boot)",
          r.stderr.strip()[-200:])
    wtxt, w = load_bundle(os.path.join(out_a, "board_view_working.js"), "__MATCHDAY_WORKING__")

    # (1) all required phantom fields transfer + lens fields retained
    check("phantomLayer" in w and isinstance(w["phantomLayer"], dict) and len(w["phantomLayer"]) > 0,
          "JOB1: phantomLayer transferred (non-empty)")
    check("phantomPicks" in w and isinstance(w["phantomPicks"], list) and len(w["phantomPicks"]) > 0,
          "JOB1: phantomPicks transferred (non-empty)")
    check("phantomTotals" in w and isinstance(w["phantomTotals"], dict) and w["phantomTotals"],
          "JOB1: phantomTotals transferred (non-empty)")
    check("lensPicks" in w and "lensConservation" in w,
          "JOB1: existing lensPicks / lensConservation retained")

    # (2) entrant metadata survives EXACTLY
    meta = w.get("phantomTotals", {}).get("_meta", {})
    check(meta.get("entrant_layer_pvc") == 83538,
          "JOB1 proof: entrant PVC 83538 exact", "got %r" % meta.get("entrant_layer_pvc"))
    check(abs((meta.get("expected_slots_per_year") or 0) - 103.43) < 1e-9,
          "JOB1 proof: expected slots ~103.4 exact", "got %r" % meta.get("expected_slots_per_year"))
    check(meta.get("seal_sha256_8") == "a17aafed",
          "JOB1 proof: seal a17aafed exact", "got %r" % meta.get("seal_sha256_8"))

    # (3) release/round metadata from the boot manifest
    st = w["stamp"]
    check(st.get("releaseVersion") == "v2.11-TEST",
          "JOB2: stamp.releaseVersion from boot manifest", "got %r" % st.get("releaseVersion"))
    check(st.get("asOfRound") == 14,
          "JOB2: stamp.asOfRound from boot manifest", "got %r" % st.get("asOfRound"))
    check(st.get("tag") == "v2.11-TEST",
          "JOB2: legacy tag alias == release_version (not hardcoded)", "got %r" % st.get("tag"))

    # ring-fence identity: three EXPLICIT, separately-named provenance identities (no overloaded field)
    check(st.get("board_md5") == board_md5,
          "FOLLOWUP2: stamp.board_md5 == actual source-board md5", "got %r" % st.get("board_md5"))
    check(st.get("store_md5") == store_md5,
          "FOLLOWUP2: stamp.store_md5 == actual verified store md5", "got %r" % st.get("store_md5"))
    check(st.get("srcmd5") == st.get("board_md5") == board_md5,
          "FOLLOWUP2: srcmd5 retained, identical to board_md5")
    check(st.get("board_md5") != st.get("store_md5"),
          "FOLLOWUP2: board_md5 and store_md5 are distinct identities (not overloaded)")
    check("source_md5" not in st,
          "FOLLOWUP2: ambiguous 'source_md5' key removed from the stamp")
    check(st.get("balanced_board_md5") is None,
          "FOLLOWUP2: balanced_board_md5 absent in boot -> null (verbatim, never invented)")
    check(st.get("board") == board_md5,
          "JOB3: stamp.board == the pinned (temp) board id")
    # no-recompute spot check: a player's `v` is passed through byte-for-byte from the source board
    src_active = src_doc["active"]
    vmatch = all(w["players"][i].get("v") == src_active[i].get("v") for i in range(min(25, len(src_active))))
    check(vmatch, "JOB3: player values passed through verbatim (extractor recomputes nothing)")

    # no stale labels anywhere in the generated working bundle
    check("v2.10" not in wtxt, "JOB2: no 'v2.10' in generated working bundle")
    check("Round 17" not in wtxt, "JOB2: no 'Round 17' in generated working bundle")

    # (6) public bundle leak-safety
    ptxt, pub = load_bundle(os.path.join(out_a, "board_view_public.js"), "__MATCHDAY_PUBLIC__")
    prohibited_top = ["phantomLayer", "phantomPicks", "phantomTotals", "lensPicks",
                      "lensConservation", "picks", "pvc", "back"]
    leaked_top = [k for k in prohibited_top if k in pub]
    check(not leaked_top, "JOB4#6: public bundle carries no phantom/lens/pick machinery",
          "leaked %r" % leaked_top)
    prohibited_row = ["key", "posCode", "ov", "levers", "lti_reg", "track", "owner_rule",
                      "cat", "pk", "vPrev", "vRaw"]
    row0 = pub["players"][0] if pub.get("players") else {}
    leaked_row = [k for k in prohibited_row if k in row0]
    check(not leaked_row, "JOB4#6: public player rows carry no id/owner-rule/mech fields",
          "leaked %r" % leaked_row)
    check("83538" not in ptxt and "a17aafed" not in ptxt,
          "JOB4#6: entrant/seal internals do not leak to the public bundle")
    check("v2.10" not in ptxt and "Round 17" not in ptxt,
          "JOB2: no stale labels in the public bundle")
    # internal provenance identities must NOT ride the public bundle (no leak)
    pub_stamp = pub.get("stamp", {})
    id_keys = ("board_md5", "store_md5", "balanced_board_md5", "srcmd5", "source_md5", "board", "store", "engine")
    id_leak = [k for k in id_keys if k in pub_stamp]
    check(not id_leak, "FOLLOWUP2: public stamp carries no internal provenance identity", "leaked %r" % id_leak)
    leaked_txt = [k for k in ("board_md5", "store_md5", "balanced_board_md5", "srcmd5", "source_md5") if k in ptxt]
    check(not leaked_txt, "FOLLOWUP2: no internal identity key anywhere in the public bundle text",
          "leaked %r" % leaked_txt)

    # ==== SCENARIO B — MISSING release/round metadata -> neutral, never v2.10 / Round 17 ===========
    boot_b = os.path.join(tmp, "boot_b.json")
    write_boot(boot_b, board_md5, store_md5)  # no release_version / as_of_round
    out_b = os.path.join(tmp, "out_b")
    r = run_extractor(src_path, boot_b, out_b)
    check(r.returncode == 0, "extractor runs with a boot manifest that omits release/round")
    wtxt2, w2 = load_bundle(os.path.join(out_b, "board_view_working.js"), "__MATCHDAY_WORKING__")
    st2 = w2["stamp"]
    check(st2.get("releaseVersion") is None and st2.get("asOfRound") is None,
          "JOB2: absent metadata -> null in the stamp (never invented)")
    check(st2.get("tag") == "", "JOB2: legacy tag alias neutral ('') when release_version absent")
    check("v2.10" not in wtxt2 and "Round 17" not in wtxt2,
          "JOB4#4: missing metadata does NOT reintroduce v2.10 / Round 17")

    # ==== SCENARIO C — mismatched BOARD pin still fails closed =====================================
    boot_c = os.path.join(tmp, "boot_c.json")
    write_boot(boot_c, "0badc0de" + board_md5[8:], store_md5, release_version="v2.11-TEST")
    r = run_extractor(src_path, boot_c, os.path.join(tmp, "out_c"))
    check(r.returncode != 0 and "RING-FENCE FAIL" in (r.stderr + r.stdout),
          "JOB3: mismatched board pin STILL fails closed (assertion not weakened)")

    # ==== SCENARIO D — mismatched STORE pin still fails closed =====================================
    boot_d = os.path.join(tmp, "boot_d.json")
    write_boot(boot_d, board_md5, "0badc0de" + store_md5[8:], release_version="v2.11-TEST")
    r = run_extractor(src_path, boot_d, os.path.join(tmp, "out_d"))
    check(r.returncode != 0 and "STORE RING-FENCE FAIL" in (r.stderr + r.stdout),
          "JOB3: mismatched store pin STILL fails closed (assertion not weakened)")

    # ==== SCENARIO E — dRound / dRoundRank verbatim pass-through (working AND public) ===============
    # A synthetic board: one player carries movement fields, one omits them entirely. Movement must
    # survive verbatim on BOTH tiers, and an absent field must stay null (never fabricated to 0/steady).
    synth = {
        "BASE_YEAR": 2026,
        "active": [
            {"key": "p-move", "name": "Mover", "grp": "MID", "club": "X", "v": 5000,
             "dRound": 37, "dRoundRank": -4},
            {"key": "p-still", "name": "Stiller", "grp": "MID", "club": "Y", "v": 4000},
        ],
        "back": [],
    }
    synth_path = os.path.join(tmp, "synth.json")
    open(synth_path, "w").write(json.dumps(synth))
    synth_md5 = md5_file(synth_path)
    boot_e = os.path.join(tmp, "boot_e.json")
    write_boot(boot_e, synth_md5, store_md5, release_version="v2.11-TEST", as_of_round=14)
    out_e = os.path.join(tmp, "out_e")
    r = run_extractor(synth_path, boot_e, out_e)
    check(r.returncode == 0, "extractor runs on the synthetic movement board", r.stderr.strip()[-200:])
    _, we = load_bundle(os.path.join(out_e, "board_view_working.js"), "__MATCHDAY_WORKING__")
    _, pe = load_bundle(os.path.join(out_e, "board_view_public.js"), "__MATCHDAY_PUBLIC__")
    wm, ws = we["players"][0], we["players"][1]
    pm, ps = pe["players"][0], pe["players"][1]
    check("dRound" in wm and "dRoundRank" in wm and wm["dRound"] == 37 and wm["dRoundRank"] == -4,
          "FOLLOWUP: working row carries dRound / dRoundRank VERBATIM", "got %r/%r" % (wm.get("dRound"), wm.get("dRoundRank")))
    check(pm.get("dRound") == 37 and pm.get("dRoundRank") == -4,
          "FOLLOWUP: public row carries dRound / dRoundRank verbatim (unchanged behaviour)")
    check("dRound" in ws and ws["dRound"] is None and "dRoundRank" in ws and ws["dRoundRank"] is None,
          "FOLLOWUP: absent movement fields remain NULL on the working tier (never fabricated)",
          "got %r/%r" % (ws.get("dRound"), ws.get("dRoundRank")))
    check(ps.get("dRound") is None and ps.get("dRoundRank") is None,
          "FOLLOWUP: absent movement fields remain null on the public tier")

    # ==== SCENARIO F — balanced_board_md5 passes through VERBATIM when the manifest sets it ==========
    # (Proves the passthrough path only; this prep branch never sets the real value in expected_boot.)
    BAL = "06d8af60ffffffffffffffffffffffff"
    boot_f = os.path.join(tmp, "boot_f.json")
    write_boot(boot_f, board_md5, store_md5, release_version="v2.11-TEST", as_of_round=14, balanced_board_md5=BAL)
    out_f = os.path.join(tmp, "out_f")
    r = run_extractor(src_path, boot_f, out_f)
    check(r.returncode == 0, "extractor runs with balanced_board_md5 present in the manifest")
    _, wf = load_bundle(os.path.join(out_f, "board_view_working.js"), "__MATCHDAY_WORKING__")
    check(wf["stamp"].get("balanced_board_md5") == BAL,
          "FOLLOWUP2: balanced_board_md5 passed through verbatim from the manifest",
          "got %r" % wf["stamp"].get("balanced_board_md5"))

    print("  " + "-" * 66)
    print("  " + str(n - fails) + "/" + str(n) + " passed" + ("  (%d FAILED)" % fails if fails else ""))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
