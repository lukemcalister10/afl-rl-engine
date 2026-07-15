#!/usr/bin/env python3
"""gates_brief.py <gates_json> [acceptance_json] [--full] — SEAT TOOLS 2 · Tier-3 READ-ONLY gate brief.

A terse wrapper over gates_score's reader (register item 148): the one-glance gate read a seat needs
before it touches a candidate.
  * status tally;
  * PICK 1 (numeraire pin) — from acceptance.numeraire.law where supplied, else scanned from a detail;
  * B1 (G-PEAK) status;
  * every FAIL id, one per line (notes only with --full);
  * standing-fails cross-check: each FAIL id is scored against acceptance.standing_fails
    (STANDING-FAIL). Any FAIL that is NOT a listed standing-fail is flagged **NEW-DEFECT**.
Output <=10 lines.

House laws: WRITES NOTHING (pure reader). Every line carries raw evidence. Loud non-zero exit on ANY
failure or missing input (SILENCE IS A RED). python3 stdlib + git only. Reuses gates_score.load /
PICK1_RE so the two tools read a snapshot the same way.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gates_score  # noqa: E402  (sibling reader — the thing we wrap)


def die(msg):
    sys.stderr.write("gates_brief: FAIL — %s\n" % msg)
    raise SystemExit(1)


def main(argv):
    rest = argv[1:]
    full = "--full" in rest
    rest = [a for a in rest if a != "--full"]
    if not (1 <= len(rest) <= 2):
        die("usage: gates_brief.py <gates_json> [acceptance_json] [--full]")
    snap = gates_score.load(rest[0])
    acc = gates_score.load(rest[1]) if len(rest) == 2 else None

    gates = snap.get("gates")
    if not isinstance(gates, dict) or not gates:
        die("no 'gates' object in %s" % rest[0])

    # tally
    tally = {}
    for v in gates.values():
        s = (v.get("status") if isinstance(v, dict) else str(v)) or "?"
        tally[s] = tally.get(s, 0) + 1

    # PICK 1 — acceptance law first, else scanned from a detail (same logic as gates_score)
    pick1, src = None, "n/a"
    if acc is not None:
        m = re.search(r"pick_?1\s*==\s*(\d+)", (acc.get("numeraire") or {}).get("law", ""))
        if m:
            pick1, src = m.group(1), "acceptance.numeraire.law"
    if pick1 is None:
        for k, v in gates.items():
            if isinstance(v, dict):
                m = gates_score.PICK1_RE.search(v.get("detail", ""))
                if m:
                    pick1, src = m.group(1), "gate %s" % k
                    break

    b1 = gates.get("B1")
    b1s = b1.get("status") if isinstance(b1, dict) else "(no B1 gate)"

    fails = sorted(k for k, v in gates.items() if isinstance(v, dict) and v.get("status") == "FAIL")

    # standing-fails cross-check
    standing = {}
    if acc is not None:
        for sf in acc.get("standing_fails", []):
            if sf.get("status") == "STANDING-FAIL":
                standing[sf.get("id")] = sf.get("source", "")

    print("== gates_brief · %s  (head=%s store=%s) ==" % (
        rest[0].split("/")[-1], str(snap.get("head", "?"))[:8], str(snap.get("store", "?"))[:8]))
    print("tally  : " + "  ".join("%s=%d" % (k, tally[k]) for k in sorted(tally)))
    print("PICK 1 : %s  (%s)" % (pick1 or "NOT STATED", src))
    print("B1     : %s" % b1s)
    new_defects = []
    if not fails:
        print("FAILs  : none")
    for fid in fails:
        if acc is None:
            tag = ""
        elif fid in standing:
            tag = "STANDING-FAIL" + ((" — " + standing[fid][:70]) if full else "")
        else:
            tag = "NEW-DEFECT (not in acceptance.standing_fails)"
            new_defects.append(fid)
        print("  %-5s %s" % (fid, tag))
    if acc is not None:
        if new_defects:
            print("xcheck : %d NEW-DEFECT — %s" % (len(new_defects), ",".join(new_defects)))
        else:
            print("xcheck : all %d FAIL(s) are listed standing-fails (0 NEW-DEFECT)" % len(fails))
    else:
        print("xcheck : (no acceptance JSON — FAILs not cross-checked)")

    if new_defects:
        die("gates_brief RED — NEW-DEFECT FAIL(s): %s" % ",".join(new_defects))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
