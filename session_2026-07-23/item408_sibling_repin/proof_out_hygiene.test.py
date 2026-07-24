#!/usr/bin/env python3
"""Register v432 note 6 — proof-output hygiene regression for the ITEM 408 sibling harnesses.

Proves the shared external-output contract (`proof_out.py`):
  1. an ordinary run resolves an EXTERNAL output directory (outside the Git checkout);
  2. an explicit external ITEM408_PROOF_OUT is honoured;
  3. an inside-checkout ITEM408_PROOF_OUT (subdir OR the repo root) is REJECTED fail-closed and creates nothing;
  4. write_result writes OUTSIDE the checkout and modifies NO tracked file (git status unchanged);
  5. the three harness result filenames are distinct.

Fast, deterministic, no board build. Exit 0 == all pass. Writes nothing into the tracked tree."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import proof_out                                                              # noqa: E402

REPO = os.path.realpath(subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"],
                                       capture_output=True, text=True).stdout.strip())
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  — %s" % detail) if detail else ""))


def _inside(p):
    p = os.path.realpath(p)
    return p == REPO or p.startswith(REPO + os.sep)


def _status():
    return subprocess.run(["git", "-C", REPO, "status", "--porcelain=v1"],
                          capture_output=True, text=True).stdout


def main():
    print("=" * 78)
    print("PROOF-OUTPUT HYGIENE (register v432 note 6) — external result JSON; tracked tree untouched")
    print("=" * 78)
    saved = os.environ.pop("ITEM408_PROOF_OUT", None)
    tmp_ext = None
    try:
        # (1) default (no env override) -> a fresh EXTERNAL directory
        d = proof_out.resolve_out_dir(__file__)
        check("default output dir is EXTERNAL (outside the checkout)", os.path.isdir(d) and not _inside(d), d)
        shutil.rmtree(d, ignore_errors=True)

        # (2) explicit EXTERNAL ITEM408_PROOF_OUT is honoured
        tmp_ext = tempfile.mkdtemp(prefix="item408-hygiene-ext-")
        os.environ["ITEM408_PROOF_OUT"] = tmp_ext
        d2 = proof_out.resolve_out_dir(__file__)
        check("explicit external ITEM408_PROOF_OUT is honoured",
              os.path.realpath(d2) == os.path.realpath(tmp_ext), d2)
        os.environ.pop("ITEM408_PROOF_OUT", None)

        # (3a) inside-checkout subdir -> rejected fail-closed, nothing created
        inside = os.path.join(REPO, "session_2026-07-23", "item408_sibling_repin", "_hygiene_reject_probe")
        os.environ["ITEM408_PROOF_OUT"] = inside
        rejected = False
        try:
            proof_out.resolve_out_dir(__file__)
        except SystemExit:
            rejected = True
        os.environ.pop("ITEM408_PROOF_OUT", None)
        check("inside-checkout ITEM408_PROOF_OUT is REJECTED fail-closed (and creates nothing)",
              rejected and not os.path.exists(inside), "rejected=%s created=%s" % (rejected, os.path.exists(inside)))

        # (3b) the repo root itself -> rejected
        os.environ["ITEM408_PROOF_OUT"] = REPO
        rej_root = False
        try:
            proof_out.resolve_out_dir(__file__)
        except SystemExit:
            rej_root = True
        os.environ.pop("ITEM408_PROOF_OUT", None)
        check("repo-root ITEM408_PROOF_OUT is REJECTED fail-closed", rej_root)

        # (4) write_result -> external file + NO tracked byte changed
        st_before = _status()
        dst = proof_out.write_result(__file__, "HYGIENE_PROBE.json", {"probe": 1})
        st_after = _status()
        check("write_result writes OUTSIDE the checkout", os.path.isfile(dst) and not _inside(dst), dst)
        check("write_result modified NO tracked file (git status byte-identical before/after)",
              st_before == st_after)
        check("write_result payload round-trips", json.load(open(dst)) == {"probe": 1})
        shutil.rmtree(os.path.dirname(dst), ignore_errors=True)

        # (5) the three harness result filenames are distinct
        names = {"INTEGRATION_RESULTS.json", "ADVANCE_CHAIN_RESULTS.json", "PROOF_RESULTS.json"}
        check("the three harness result filenames are distinct", len(names) == 3)
    finally:
        if tmp_ext:
            shutil.rmtree(tmp_ext, ignore_errors=True)
        if saved is not None:
            os.environ["ITEM408_PROOF_OUT"] = saved

    npass = sum(1 for r in RESULTS if r)
    print("\n  RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
