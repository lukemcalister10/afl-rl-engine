#!/usr/bin/env python3
"""ROUND-ENTRY TOOL — DRY-RUN FIXTURE PROOFS (directive step 5). READ-ONLY. SILENCE IS A RED.

Every count below is SCRIPT-EMITTED (never typed). Exit 0 = all proofs PASS; non-zero = a red.

THE FIVE FIXTURES (on committed synthetic pools — the LIVE pool has zero active name-collisions, so
the clash MUST be synthetic per item 305):
  (a) clean round               — all names resolve, residue empty, snapshot written.
  (b) misspelled -> residue     — near-match residue with candidates; owner picks -> confirmed.
  (c) unknown/not-in-DB         — residue with no confident candidate; owner skips -> recorded drop.
  (d) synthetic 2-active clash  — AMBIGUOUS residue with BOTH candidates (never auto-collapsed).
  (e) idempotent re-entry       — re-entering a round REPLACES its artifacts, never duplicates.

THE NO-WRITE PROOFS (against the REAL single source + board):
  * apply() still raises IngestionGatedError (invoked; the raised error captured).
  * the real store md5 is UNCHANGED before/after the whole suite (and == the pinned value).
  * the real board md5 is UNCHANGED (no derived board regeneration happens in this job at all).

THE DETERMINISM CHECK:
  * regenerating a snapshot from identical inputs (incl. a pinned generated_at) is BYTE-IDENTICAL.

Run:  python3 round_entry_fixture_proof.py [--write]   (--write commits PROOF.md + proof.json)
"""
import json
import os
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.dirname(_HERE))     # for id_resolver / score_ingestor
import round_entry as RE                         # noqa: E402

_ROOT = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
_STORE = os.path.join(os.path.dirname(_HERE), "rl_model_data.json")
_BOARD = os.path.join(_ROOT, "data", "rl_build", "rl_app_data.json")
_CLI = os.path.join(_ROOT, "tools", "round_entry", "round_entry.py")
_FX = os.path.join(_ROOT, "session_2026-07-17", "round_entry_tool", "fixtures")
_PINNED_STORE_MD5 = "b1fd0bce"
_PINNED_BOARD_MD5 = "790136a3"
_FIXED_NOW = "2026-07-17T00:00:00Z"      # pinned stamp so determinism is byte-exact incl. all stamps

_POOL_NORMAL = os.path.join(_FX, "pool_normal.json")
_POOL_CLASH = os.path.join(_FX, "pool_clash.json")


class Proof:
    def __init__(self):
        self.checks = []       # (name, passed, detail)

    def check(self, name, passed, detail=""):
        self.checks.append((name, bool(passed), str(detail)))
        print("  [%s] %s%s" % ("PASS" if passed else "FAIL", name,
                               (" — " + detail) if detail else ""))
        return passed

    @property
    def all_pass(self):
        return all(p for _, p, _ in self.checks)


def _body(fname):
    with open(os.path.join(_FX, fname)) as f:
        return f.read()


def _set_first_action(residue_path, value):
    """Simulate the owner's ONE edit: set the first (only) block's ACTION line. Deterministic."""
    lines = open(residue_path).read().splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith("ACTION:"):
            indent = ln[:len(ln) - len(ln.lstrip())]
            lines[i] = "%sACTION: %s" % (indent, value)
            break
    open(residue_path, "w").write("\n".join(lines) + "\n")


# ---- (a) clean round -----------------------------------------------------------------------
def fixture_a(p):
    print("\n(a) CLEAN ROUND")
    ent = RE.RoundEntry(1, store_path=_POOL_NORMAL)
    resolved, residue = ent.resolve_body(_body("feed_a_clean.csv"))
    p.check("a.resolved==3", len(resolved) == 3, "resolved=%d" % len(resolved))
    p.check("a.residue==0", len(residue) == 0, "residue=%d" % len(residue))
    snap = ent.build_snapshot(resolved, generated_at=_FIXED_NOW)
    p.check("a.snapshot.counts", snap["counts"] == {"resolved": 3, "skipped": 0, "residue_open": 0},
            json.dumps(snap["counts"], sort_keys=True))
    p.check("a.retired-excluded (pool=6 not 7)", ent.resolver.active_count == 6,
            "active_pool=%d" % ent.resolver.active_count)
    return snap


# ---- (b) misspelled -> residue -> confirmed ------------------------------------------------
def fixture_b(p, tmp):
    print("\n(b) MISSPELLED -> RESIDUE -> CONFIRMED")
    _run_cli(["enter", "--round", "2", "--body-file", os.path.join(_FX, "feed_b_misspelled.csv"),
              "--store", _POOL_NORMAL, "--out", tmp, "--now", _FIXED_NOW])
    residue_path = os.path.join(tmp, "round_2.residue.txt")
    p.check("b.residue-file-written", os.path.exists(residue_path))
    ent = RE.RoundEntry(2, store_path=_POOL_NORMAL)
    resolved, residue = ent.resolve_body(_body("feed_b_misspelled.csv"))
    p.check("b.1-exact-1-residue", len(resolved) == 1 and len(residue) == 1,
            "resolved=%d residue=%d" % (len(resolved), len(residue)))
    cand_names = [c["name"] for c in residue[0].candidates] if residue else []
    p.check("b.near-candidates-list-Nick-Daicos", "Nick Daicos" in cand_names,
            "candidates=%s" % cand_names)
    p.check("b.reason==unresolved", residue and residue[0].reason == "unresolved")
    # the owner's ONE edit: pick the candidate index whose name is the correct store row
    pick_idx = next(c["index"] for c in residue[0].candidates if c["name"] == "Nick Daicos")
    _set_first_action(residue_path, str(pick_idx))
    out = _run_cli(["confirm", "--round", "2", "--store", _POOL_NORMAL, "--out", tmp,
                    "--now", _FIXED_NOW])
    snap = json.load(open(os.path.join(tmp, "round_2.snapshot.json")))
    p.check("b.confirmed.counts", snap["counts"] == {"resolved": 2, "skipped": 0, "residue_open": 0},
            json.dumps(snap["counts"], sort_keys=True))
    vias = sorted(r["via"] for r in snap["resolved"])
    p.check("b.one-exact-one-confirm", vias == ["confirm", "exact"], "vias=%s" % vias)
    p.check("b.confirmed-row-is-Nick-Daicos-key",
            any(r["key"] == "nick-daicos" and r["via"] == "confirm" for r in snap["resolved"]))
    return out


# ---- (c) unknown/not-in-DB -> residue -> skip ----------------------------------------------
def fixture_c(p, tmp):
    print("\n(c) UNKNOWN / NOT-IN-DB -> RESIDUE -> SKIP")
    _run_cli(["enter", "--round", "3", "--body-file", os.path.join(_FX, "feed_c_unknown.csv"),
              "--store", _POOL_NORMAL, "--out", tmp, "--now", _FIXED_NOW])
    residue_path = os.path.join(tmp, "round_3.residue.txt")
    ent = RE.RoundEntry(3, store_path=_POOL_NORMAL)
    resolved, residue = ent.resolve_body(_body("feed_c_unknown.csv"))
    p.check("c.1-exact-1-residue", len(resolved) == 1 and len(residue) == 1,
            "resolved=%d residue=%d" % (len(resolved), len(residue)))
    p.check("c.unknown-name-in-residue", residue and residue[0].name == "Rookie Notindb")
    _set_first_action(residue_path, "skip")
    _run_cli(["confirm", "--round", "3", "--store", _POOL_NORMAL, "--out", tmp, "--now", _FIXED_NOW])
    snap = json.load(open(os.path.join(tmp, "round_3.snapshot.json")))
    p.check("c.skip.counts", snap["counts"] == {"resolved": 1, "skipped": 1, "residue_open": 0},
            json.dumps(snap["counts"], sort_keys=True))
    p.check("c.skipped-is-the-unknown", snap["skipped"] and
            snap["skipped"][0]["name"] == "Rookie Notindb" and
            snap["skipped"][0]["reason"] == "owner-skip")
    p.check("c.unknown-NOT-in-resolved",
            all(r["name"] != "Rookie Notindb" for r in snap["resolved"]))


# ---- (d) synthetic two-active-exact clash --------------------------------------------------
def fixture_d(p):
    print("\n(d) SYNTHETIC TWO-ACTIVE-EXACT CLASH")
    ent = RE.RoundEntry(4, store_path=_POOL_CLASH)
    resolved, residue = ent.resolve_body(_body("feed_d_clash.csv"))
    p.check("d.no-auto-resolve", len(resolved) == 0, "resolved=%d" % len(resolved))
    p.check("d.one-residue-line", len(residue) == 1, "residue=%d" % len(residue))
    if residue:
        r = residue[0]
        p.check("d.reason==ambiguous", r.reason == "ambiguous", "reason=%s" % r.reason)
        p.check("d.BOTH-candidates-shown", len(r.candidates) == 2,
                "candidates=%d" % len(r.candidates))
        keys = sorted(c["key"] for c in r.candidates)
        p.check("d.both-active-exact-keys", keys == ["sam-clash-a", "sam-clash-b"], "keys=%s" % keys)
        p.check("d.both-kind-active-exact",
                all(c["kind"] == "active exact" for c in r.candidates))


# ---- (e) idempotent re-entry replaces ------------------------------------------------------
def fixture_e(p, tmp):
    print("\n(e) IDEMPOTENT RE-ENTRY REPLACES")
    _run_cli(["enter", "--round", "5", "--body-file", os.path.join(_FX, "feed_e1_first.csv"),
              "--store", _POOL_NORMAL, "--out", tmp, "--now", _FIXED_NOW])
    snap1 = json.load(open(os.path.join(tmp, "round_5.snapshot.json")))
    p.check("e.first-entry-2-resolved", snap1["counts"]["resolved"] == 2,
            "resolved=%d" % snap1["counts"]["resolved"])
    out2 = _run_cli(["enter", "--round", "5", "--body-file", os.path.join(_FX, "feed_e2_second.csv"),
                     "--store", _POOL_NORMAL, "--out", tmp, "--now", _FIXED_NOW])
    p.check("e.re-entry-announces-REPLACING", "REPLACING" in out2, "cli said REPLACING")
    snap2 = json.load(open(os.path.join(tmp, "round_5.snapshot.json")))
    keys = [r["key"] for r in snap2["resolved"]]
    p.check("e.replaced-not-merged", keys == ["zak-butters"], "keys=%s" % keys)
    # exactly ONE snapshot file for the round — no duplication
    snaps = [f for f in os.listdir(tmp) if f.startswith("round_5.snapshot")]
    p.check("e.single-snapshot-no-dup", len(snaps) == 1, "snapshot files=%s" % snaps)


# ---- NO-WRITE proofs -----------------------------------------------------------------------
def no_write_proofs(p):
    print("\nNO-WRITE PROOFS (real single source + board)")
    from score_ingestor import ScoreIngestor, IngestionGatedError, parse_feed  # real plumbing
    raised = None
    try:
        ing = ScoreIngestor(store_path=_STORE)
        pv = ing.preview(parse_feed('[{"player":"Willem Duursma","round":1,"score":90,"played":1}]'),
                         merge_with_store=False)
        ing.apply(pv)
    except IngestionGatedError as e:
        raised = str(e)
    p.check("nw.apply-raises-IngestionGatedError", raised is not None,
            (raised or "")[:80])
    return raised


def _md5(path):
    return RE.md5_of_file(path)


# ---- determinism check ---------------------------------------------------------------------
def determinism(p):
    print("\nDETERMINISM CHECK (byte-identical regen incl. stamps)")
    ent = RE.RoundEntry(1, store_path=_POOL_NORMAL)
    resolved, _ = ent.resolve_body(_body("feed_a_clean.csv"))
    b1 = RE.snapshot_bytes(ent.build_snapshot(resolved, generated_at=_FIXED_NOW))
    ent2 = RE.RoundEntry(1, store_path=_POOL_NORMAL)
    resolved2, _ = ent2.resolve_body(_body("feed_a_clean.csv"))
    b2 = RE.snapshot_bytes(ent2.build_snapshot(resolved2, generated_at=_FIXED_NOW))
    import hashlib
    m1, m2 = hashlib.md5(b1).hexdigest()[:8], hashlib.md5(b2).hexdigest()[:8]
    p.check("det.byte-identical", b1 == b2, "md5 %s == %s" % (m1, m2))
    return m1


def _run_cli(argv):
    r = subprocess.run([sys.executable, _CLI] + argv, capture_output=True, text=True)
    if r.returncode != 0:
        # a red inside a step is caught by the calling check; surface the stderr
        return (r.stdout + r.stderr)
    return r.stdout


def main(argv):
    write = "--write" in argv
    p = Proof()

    store_md5_before = _md5(_STORE)
    board_md5_before = _md5(_BOARD)

    import tempfile
    tmp = tempfile.mkdtemp(prefix="round_entry_fixtures_")

    snap_a = fixture_a(p)
    fixture_b(p, tmp)
    fixture_c(p, tmp)
    fixture_d(p)
    fixture_e(p, tmp)
    raised = no_write_proofs(p)
    det_md5 = determinism(p)

    store_md5_after = _md5(_STORE)
    board_md5_after = _md5(_BOARD)
    print("\nSTORE / BOARD IMMUTABILITY")
    p.check("nw.store-md5-unchanged", store_md5_before == store_md5_after,
            "%s -> %s" % (store_md5_before, store_md5_after))
    p.check("nw.store-md5==pinned", store_md5_after == _PINNED_STORE_MD5,
            "%s (pin %s)" % (store_md5_after, _PINNED_STORE_MD5))
    p.check("nw.board-md5-unchanged", board_md5_before == board_md5_after,
            "%s -> %s" % (board_md5_before, board_md5_after))
    p.check("nw.board-md5==pinned", board_md5_after == _PINNED_BOARD_MD5,
            "%s (pin %s)" % (board_md5_after, _PINNED_BOARD_MD5))

    passed = sum(1 for _, ok, _ in p.checks if ok)
    total = len(p.checks)
    print("\n==== ROUND-ENTRY DRY-RUN PROOFS: %d/%d PASS -> %s ===="
          % (passed, total, "PROOF PASS" if p.all_pass else "PROOF FAIL"))

    result = {
        "proof_pass": p.all_pass,
        "checks_passed": passed, "checks_total": total,
        "store_md5_before": store_md5_before, "store_md5_after": store_md5_after,
        "store_md5_pinned": _PINNED_STORE_MD5,
        "board_md5_before": board_md5_before, "board_md5_after": board_md5_after,
        "board_md5_pinned": _PINNED_BOARD_MD5,
        "apply_raised": raised,
        "determinism_snapshot_md5": det_md5,
        "clean_snapshot_counts": snap_a["counts"],
        "module_code_md5": RE.module_code_md5(),
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in p.checks],
    }
    if write:
        outdir = os.path.join(_ROOT, "session_2026-07-17", "round_entry_tool", "proofs")
        os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir, "proof.json"), "w") as f:
            json.dump(result, f, indent=2, sort_keys=True)
        with open(os.path.join(outdir, "PROOF.md"), "w") as f:
            f.write(_md_report(result))
        print("wrote proofs/PROOF.md + proofs/proof.json")
    return 0 if p.all_pass else 1


def _md_report(res):
    L = [
        "# ROUND-ENTRY TOOL — DRY-RUN FIXTURE PROOFS",
        "",
        "Directive step 5. READ-ONLY. Every count script-emitted. Regenerate:",
        "`python3 engine/rl_after/ingestion/round_entry_fixture_proof.py --write`.",
        "",
        "## RESULT: **%s** (%d/%d checks)" % (
            "PROOF PASS" if res["proof_pass"] else "PROOF FAIL",
            res["checks_passed"], res["checks_total"]),
        "",
        "| immutability | before | after | pinned |",
        "|---|---|---|---|",
        "| real store md5 | `%s` | `%s` | `%s` |" % (
            res["store_md5_before"], res["store_md5_after"], res["store_md5_pinned"]),
        "| real board md5 | `%s` | `%s` | `%s` |" % (
            res["board_md5_before"], res["board_md5_after"], res["board_md5_pinned"]),
        "",
        "- **apply() raised:** `%s`" % (res["apply_raised"] or "").replace("\n", " "),
        "- **determinism** (byte-identical snapshot regen) md5: `%s`" % res["determinism_snapshot_md5"],
        "- **module_code_md5:** `%s`" % res["module_code_md5"],
        "",
        "## CHECKS",
        "| # | check | verdict | detail |",
        "|---|---|---|---|",
    ]
    for i, c in enumerate(res["checks"], start=1):
        L.append("| %d | %s | %s | %s |" % (
            i, c["name"], "PASS" if c["pass"] else "FAIL", c["detail"].replace("|", "\\|")))
    L += ["", "## WHAT THIS PROVES",
          "- The resolver exact-matches over the LIVE active pool; retirees are excluded (fixture a).",
          "- A misspelling is RESIDUE with the nearest active candidates, resolved only by the owner's",
          "  one-tap pick — never a silent auto-attach (fixture b).",
          "- A not-yet-in-DB scorer is RESIDUE and is skipped on the owner's word, never invented",
          "  as a new row (fixture c).",
          "- A genuine two-active-exact clash is AMBIGUOUS with BOTH candidates, never collapsed",
          "  (fixture d — synthetic, because the live pool has zero active name-collisions).",
          "- Re-entering a round REPLACES its artifacts loudly and never duplicates (fixture e).",
          "- NO-WRITE: `apply()` still refuses; the real store + board md5 are byte-unchanged and",
          "  match their pins; snapshot regeneration is byte-identical.",
          "",
          "## SCOPE",
          "- Fixtures a–e run on committed SYNTHETIC pools (`fixtures/pool_*.json`) for determinism",
          "  and to construct the clash the live pool cannot supply. The immutability proofs run",
          "  against the REAL single source and board.",
          "- The store-write path is absent by design; go-live is a separate owner-worded job",
          "  (docs/GO_LIVE_round_score_ingestion.md).",
          ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
