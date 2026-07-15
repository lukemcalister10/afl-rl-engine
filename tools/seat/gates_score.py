#!/usr/bin/env python3
"""gates_score.py <gates_json> [acceptance_json] — SEAT TOOLS (P3) · Tier-3 READ-ONLY scorer.

Reads a data/gates_snapshots/gates_*.json and prints a compact, evidence-bearing table:
  * B1 (G-PEAK) and G-COHORT ratios laid against the hard bound where the snapshot carries them;
  * PICK 1 (the numeraire pin, 3000) wherever it is stated;
  * EVERY FAIL with its note;
  * named anchor values where present.
When the acceptance_json path is supplied, matching entries are scored BY ID (guard alias -> gate,
anchor governed_by / player -> gate) so the snapshot is read against the binding registry, not memory.

House laws: WRITES NOTHING (pure reader). Every line carries raw evidence (a status, a number, a note),
never a bare verdict. Non-zero exit on ANY failure or missing input; the exit code is the authority
(SILENCE IS A RED). python3 stdlib only.
"""
import json
import re
import sys


def die(msg):
    sys.stderr.write("gates_score: FAIL — %s\n" % msg)
    raise SystemExit(1)


def load(path):
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        die("input not found: %s" % path)
    except (json.JSONDecodeError, OSError) as e:
        die("cannot read %s: %s" % (path, e))


# hard bound for the cohort/peak family — G-COHORT ships at <=130 (expected_boot panel note;
# CONSTRAINTS G-COHORT). Overridden per-guard when the acceptance JSON supplies a threshold.
COHORT_BOUND = 130.0

RATIO_RE = re.compile(r"(?<![\d.])(1[0-9]{2}\.[0-9]+)")   # cohort-scale figures, e.g. 126.8
PICK1_RE = re.compile(r"(?:PVC\[1\]|pick[-_ ]?1|PICK1)\s*[=:]?\s*(\d{3,5})", re.I)
ANCHOR_RE = re.compile(r"([A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+)*)\s*=\s*(\d{2,5})")


def main(argv):
    if not (2 <= len(argv) <= 3):
        die("usage: gates_score.py <gates_json> [acceptance_json]")
    snap = load(argv[1])
    acc = load(argv[2]) if len(argv) == 3 else None

    gates = snap.get("gates")
    if not isinstance(gates, dict) or not gates:
        die("no 'gates' object in %s" % argv[1])

    head = snap.get("head", "?")
    store = snap.get("store", "?")
    print("== gates_score · %s ==" % argv[1].split("/")[-1])
    print("head=%s store=%s  (%d gates)" % (str(head)[:8], str(store)[:8], len(gates)))

    # tally by status
    tally = {}
    for v in gates.values():
        s = (v.get("status") if isinstance(v, dict) else str(v)) or "?"
        tally[s] = tally.get(s, 0) + 1
    print("tally: " + "  ".join("%s=%d" % (k, tally[k]) for k in sorted(tally)))

    # --- PICK 1 (numeraire pin) — from acceptance law if present, else scanned from details ---
    pick1 = None
    src = ""
    if acc is not None:
        law = (acc.get("numeraire") or {}).get("law", "")
        m = re.search(r"pick_?1\s*==\s*(\d+)", law)
        if m:
            pick1, src = m.group(1), "acceptance.numeraire.law"
    if pick1 is None:
        for k, v in gates.items():
            if isinstance(v, dict):
                m = PICK1_RE.search(v.get("detail", ""))
                if m:
                    pick1, src = m.group(1), "gate %s detail" % k
                    break
    print("PICK 1     : %s   (%s)" % (pick1 if pick1 else "NOT STATED IN SNAPSHOT", src or "n/a"))

    # --- B1 / G-COHORT ratios vs the hard bound (where the snapshot carries the numbers) ---
    bound = COHORT_BOUND
    if acc is not None:
        for gd in acc.get("guards", []):
            if gd.get("id") == "G-COHORT":
                for cand in (gd.get("bound"), (gd.get("thresholds") or {}).get("max")):
                    try:
                        bound = float(cand)
                    except (TypeError, ValueError):
                        pass
    print("-- cohort/peak vs hard bound (<= %g) --" % bound)
    printed = False
    for gid in ("B1", "G-COHORT", "G-PEAK"):
        g = gates.get(gid)
        if not isinstance(g, dict):
            continue
        det = g.get("detail", "")
        ratios = [float(x) for x in RATIO_RE.findall(det)]
        if ratios:
            verdict = "PASS" if all(r <= bound for r in ratios) else "OVER"
            print("  %-8s %-5s ratios=%s vs %g -> %s" % (
                gid, g.get("status"), "/".join("%.1f" % r for r in ratios), bound, verdict))
        else:
            print("  %-8s %-5s (ratios NOT in snapshot detail — truncated; status is the record)"
                  % (gid, g.get("status")))
        printed = True
    if not printed:
        print("  (no B1/G-COHORT/G-PEAK gate in snapshot)")

    # --- EVERY FAIL with its note ---
    print("-- FAILs (id · dc · note) --")
    fails = [(k, v) for k, v in gates.items()
             if isinstance(v, dict) and v.get("status") == "FAIL"]
    if not fails:
        print("  (no FAIL gates)")
    for k, v in sorted(fails):
        note = (v.get("detail", "") or "").replace("\n", " ")
        print("  %-5s dc=%-5s %s" % (k, v.get("dc"), note[:150]))

    # --- named anchor values where present (scanned from gate details) ---
    print("-- named anchors in details --")
    seen = set()
    n_anchor = 0
    for k, v in gates.items():
        if not isinstance(v, dict):
            continue
        for name, val in ANCHOR_RE.findall(v.get("detail", "")):
            key = (name, val)
            if key in seen:
                continue
            seen.add(key)
            if len(name) >= 4:   # drop stray tokens like 'T5'
                print("  %-26s %s   (%s)" % (name, val, k))
                n_anchor += 1
        if n_anchor >= 12:
            print("  ... (anchor scan capped at 12; snapshot has more)")
            break
    if n_anchor == 0:
        print("  (no Name=value anchors found in details)")

    # --- acceptance scoring BY ID (only when acceptance JSON supplied) ---
    if acc is not None:
        print("-- acceptance scored by id (guards.alias -> gate) --")
        scored = 0
        for gd in acc.get("guards", []):
            alias = gd.get("alias")
            gid = gd.get("id")
            gate = gates.get(alias) if alias else None
            if gate is None:
                continue
            print("  %-9s(alias %-3s) status=%-5s acc.status=%s" % (
                gid, alias, gate.get("status"), gd.get("status")))
            scored += 1
        # anchors: report their governing gate's status when that gate is in the snapshot
        for a in acc.get("anchors", []):
            gov = a.get("governed_by")
            gate = None
            if gov:
                # G-PEAK->B1, G-FLOOR->B5 alias resolution
                alias = {"G-PEAK": "B1", "G-FLOOR": "B5"}.get(gov, gov)
                gate = gates.get(alias)
            if gate is not None:
                print("  %-9s governed_by %-8s -> gate %s" % (
                    a.get("id"), gov, gate.get("status")))
                scored += 1
        if scored == 0:
            print("  (no acceptance ids matched a gate in this snapshot)")

    print("== gates_score OK ==")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
