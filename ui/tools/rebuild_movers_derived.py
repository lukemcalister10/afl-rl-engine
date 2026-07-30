#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI — MOVERS BUNDLE DERIVED-BLOCK REBUILD (#274 item 1, ERA SUCCESSION).

`ui/data/movers.js` carries two kinds of content. The per-round REPORTS are the record: frozen era
history, never rewritten (#271 A15/A16 — "a later round never rewrites an earlier report's identity").
The DERIVED BLOCKS — `points`, `values`, `model_changes` — are recomputed from the committed histories
on every bundle write (round_movers.accumulate_bundle). This tool rebuilds the derived blocks and
NOTHING else, so a change to how they are derived can reach the shipped bundle without a hand edit and
without re-running a round.

WHY IT EXISTS. #274 item 1 changed `round_movers.model_changes()` to read every entry of the transition
register, which flips the 30/7 boundary from `owner_approved_record: false` to true. That value is
BAKED into the bundle at write time, so the reader change alone does not move the shipped file. The
full finalization/repair lane would move it, but that lane also writes the per-round report JSON/CSV
under engine/rl_after/ingestion/movers/ and the finalization state + journal — none of which need to
change here, and all of which are outside this wave's fence. So this drives exactly ONE of the
primitives round_finalize drives step-by-step (`accumulate_bundle`), the only one whose output is the
shipped bundle.

HOW THE REPORTS STAY BYTE-VERBATIM. The report handed back to `accumulate_bundle` is the bundle's OWN
committed copy, read from the bundle itself — not re-read from movers_R<n>.json, whose keys are stored
sorted and would reorder the bundle's bytes on a round-trip (measured at #274: a 0-content, 0-length
byte diff purely from key order). Same identity in, same identity out, so the module's own conflict
guard treats it as the idempotent replace it is, and the reports' bytes are carried through rather than
regenerated. Verified at head before any change: this rebuild was a BYTE-IDENTICAL no-op, which is what
makes any diff it now produces attributable to the derivation change alone.

Run:  python3 ui/tools/rebuild_movers_derived.py            (rebuild the derived blocks)
      python3 ui/tools/rebuild_movers_derived.py --check    (verify committed == rebuilt; no write)
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
BUNDLE = os.path.join(REPO, "ui", "data", "movers.js")
INGESTION = os.path.join(REPO, "engine", "rl_after", "ingestion")

DERIVED = ("points", "values", "model_changes")


def _load_wrapped(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return json.loads(text[text.index("{"): text.rindex("}") + 1])


def _rebuild_into(path):
    """Run the module's own bundle-write primitive against `path`, handing back that bundle's own
    committed latest report. Returns the report's round."""
    if INGESTION not in sys.path:
        sys.path.insert(0, INGESTION)
    import round_movers as MV

    bundle = _load_wrapped(path)
    rounds = sorted(int(r) for r in (bundle.get("reports") or {}))
    if not rounds:
        raise SystemExit("■ HALT — %s carries no reports; nothing to rebuild from"
                         % os.path.relpath(path, REPO))
    latest = str(rounds[-1])
    report = bundle["reports"][latest]        # the bundle's OWN copy, in its own key order
    res = MV.accumulate_bundle(path, report, repo_root=REPO)
    if res.get("overwrite_conflict"):
        raise SystemExit("■ HALT — identity conflict on R%s; the bundle was left byte-unchanged" % latest)
    if not res.get("wrote"):
        raise SystemExit("■ HALT — the bundle write did not run")
    return latest


def main(argv):
    check = "--check" in argv[1:]
    unknown = [a for a in argv[1:] if a != "--check"]
    if unknown:
        raise SystemExit("usage: rebuild_movers_derived.py [--check]")
    if not os.path.exists(BUNDLE):
        raise SystemExit("■ HALT — %s does not exist" % os.path.relpath(BUNDLE, REPO))

    with open(BUNDLE, "rb") as f:
        before = f.read()

    tmpdir = tempfile.mkdtemp(prefix="movers_derived_")
    scratch = os.path.join(tmpdir, "movers.js")
    try:
        shutil.copyfile(BUNDLE, scratch)
        latest = _rebuild_into(scratch)
        with open(scratch, "rb") as f:
            after = f.read()

        if check:
            if after != before:
                print("■ DRIFT — %s derived blocks are not what the committed histories rebuild to.\n"
                      "  committed %d bytes / rebuilt %d bytes — regenerate with "
                      "python3 ui/tools/rebuild_movers_derived.py"
                      % (os.path.relpath(BUNDLE, REPO), len(before), len(after)))
                return 1
            print("derived blocks OK — committed == rebuilt (%d bytes, latest report R%s)"
                  % (len(before), latest))
            return 0

        # Report what moved BEFORE overwriting, so the write is never silent.
        old, new = _load_wrapped(BUNDLE), json.loads(after.decode("utf-8")[
            after.decode("utf-8").index("{"): after.decode("utf-8").rindex("}") + 1])
        moved = [k for k in DERIVED if old.get(k) != new.get(k)]
        other = [k for k in set(old) | set(new) if k not in DERIVED and old.get(k) != new.get(k)]
        if other:
            raise SystemExit("■ HALT — the rebuild moved something outside the derived blocks: %s.\n"
                             "  Nothing written. The reports are the record and this tool may not "
                             "touch them." % ", ".join(sorted(other)))
        shutil.copyfile(scratch, BUNDLE)
        print("wrote: %s (%d -> %d bytes, latest report R%s)"
              % (os.path.relpath(BUNDLE, REPO), len(before), len(after), latest))
        print("derived blocks changed: %s" % (", ".join(moved) if moved else "none (byte-identical)"))
        return 0
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
