#!/usr/bin/env python3
"""board_diff.py <revA> <revB> [--names n1,n2,…] — SEAT TOOLS 2 · Tier-3 READ-ONLY board prescreen.

The standard prescreen diff, terse — replaces the ~30 lines of ad-hoc python the seat rewrote five
times in a sitting (register item 148). Reads data/rl_build/rl_app_data.json at two revs (git show,
no checkout) and lays their board-shape facts side by side:
  * mover count (players whose num-SCAR `active[].v` changed) + added/removed;
  * ΣΔ num-SCAR (signed net + gross);
  * age-bucket ΣΔ at the head rev (<=22 / 23–26 / >=27);
  * top-3 cuts + top-3 lifts by name;
  * any --names rows before->after;
  * PICK 1 both sides (`picks` n=1) + pair-2 / pair-3 ratios (pick2/pick1, pick3/pick1).
Output <=15 lines.

House laws: WRITES NOTHING (git show reads history into memory). Every line carries raw evidence.
Loud non-zero exit on ANY failure or missing input (SILENCE IS A RED). python3 stdlib + git only.
"""
import json
import os
import subprocess
import sys

BOARD = "data/rl_build/rl_app_data.json"


def die(msg):
    sys.stderr.write("board_diff: FAIL — %s\n" % msg)
    raise SystemExit(1)


def repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", ".."))


def load_board(root, rev):
    p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, BOARD)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        die("%s not readable at rev %s: %s" % (BOARD, rev, (p.stderr or "").strip()[:120]))
    try:
        return json.loads(p.stdout)
    except json.JSONDecodeError as e:
        die("board at %s is not valid JSON: %s" % (rev, e))


def by_key(board):
    out = {}
    for pl in board.get("active", []):
        k = pl.get("key")
        if k is not None:
            out[k] = pl
    if not out:
        die("board has no keyed `active` players")
    return out


def pick_v(board, n):
    for p in board.get("picks", []):
        if p.get("n") == n:
            return p.get("v")
    return None


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main(argv):
    rest = argv[1:]
    names = []
    if "--names" in rest:
        i = rest.index("--names")
        if i + 1 < len(rest):
            names = [s.strip() for s in rest[i + 1].split(",") if s.strip()]
        rest = rest[:i] + rest[i + 2:]     # drop the flag AND its value
    args = [a for a in rest if not a.startswith("--")]
    if len(args) != 2:
        die("usage: board_diff.py <revA> <revB> [--names n1,n2,…]")
    revA, revB = args
    root = repo_root()
    A, B = by_key(load_board(root, revA)), by_key(load_board(root, revB))

    common = set(A) & set(B)
    added, removed = set(B) - set(A), set(A) - set(B)
    movers = []
    for k in common:
        va, vb = fnum(A[k].get("v")), fnum(B[k].get("v"))
        if va is None or vb is None or va == vb:
            continue
        movers.append((k, va, vb, vb - va, B[k].get("name", k), B[k].get("age")))

    net = sum(m[3] for m in movers)
    gross = sum(abs(m[3]) for m in movers)
    buckets = {"<=22": 0.0, "23-26": 0.0, ">=27": 0.0}
    for _, _, _, dv, _, age in movers:
        a = fnum(age)
        key = "<=22" if (a is not None and a <= 22) else (">=27" if (a is not None and a >= 27) else "23-26")
        buckets[key] += dv

    cuts = sorted(movers, key=lambda m: m[3])[:3]
    lifts = sorted(movers, key=lambda m: -m[3])[:3]

    def row(m):
        return "%s %g->%g (%+g)" % (m[4], m[1], m[2], m[3])

    print("== board_diff · %s..%s ==" % (revA[:8], revB[:8]))
    print("movers     : %d / %d common  (+%d added, -%d removed)" % (
        len(movers), len(common), len(added), len(removed)))
    print("ΣΔ SCAR    : net %+g  (gross %g over movers)" % (net, gross))
    print("age ΣΔ     : <=22 %+g | 23–26 %+g | >=27 %+g" % (
        buckets["<=22"], buckets["23-26"], buckets[">=27"]))
    print("top cuts   : " + ("; ".join(row(m) for m in cuts) if cuts else "(none)"))
    print("top lifts  : " + ("; ".join(row(m) for m in lifts) if lifts else "(none)"))

    p1a, p1b = pick_v(load_board(root, revA), 1), pick_v(load_board(root, revB), 1)
    print("PICK 1     : A %s -> B %s" % (p1a, p1b))

    def ratios(rev):
        bd = load_board(root, rev)
        p1, p2, p3 = pick_v(bd, 1), pick_v(bd, 2), pick_v(bd, 3)
        r2 = "%.3f" % (p2 / p1) if (fnum(p1) and fnum(p2)) else "?"
        r3 = "%.3f" % (p3 / p1) if (fnum(p1) and fnum(p3)) else "?"
        return r2, r3

    ra, rb = ratios(revA), ratios(revB)
    print("pair ratios: A p2/1=%s p3/1=%s | B p2/1=%s p3/1=%s" % (ra[0], ra[1], rb[0], rb[1]))

    if names:
        print("-- --names rows (before->after) --")
        for want in names:
            hits = [k for k in common if want.lower() in (B[k].get("name", "") or "").lower()]
            if not hits:
                print("  %-18s (not in both revs)" % want)
                continue
            for k in hits[:3]:
                va, vb = A[k].get("v"), B[k].get("v")
                mark = "" if va == vb else "  MOVED"
                print("  %-18s %s -> %s  (age %s)%s" % (
                    B[k].get("name", k)[:18], va, vb, B[k].get("age"), mark))

    print("== board_diff OK ==")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
