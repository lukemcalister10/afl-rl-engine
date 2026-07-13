#!/usr/bin/env python3
"""Build engine/rl_after/export_attribution.json from the certified G-ATTR stage boards.

Reads the six stage boards produced by session_2026-07-13/v2_9_refit_cert/scripts/gen_gattr_chain.sh
(base, +L1, +L1+L4, +L1+L4+L2, +L1+L4+L2+L3, FULL) — each a board_pass.py dump {board:{key:ev}} — and
emits per-player:
  vPrev[key]  = value on the all-levers-OFF base (the last-accepted-bake board, de4baef9 lineage)
  levers[key] = {L1,L4,L2,L3,L5} cumulative deltas that sum EXACTLY to FULL - base for that key

This is the CERTIFIED attribution, not a new computation: it asserts the committed stage sums
(723075/724371/725799/731106/732725/732725). DISPLAY-ONLY consumer of the certified boards; touches no ev().
"""
import json, os, sys

OUT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  # repo root (scripts→v2_9_export_display→session_2026-07-13→repo)
STAGE_DIR = os.path.join(OUT_DIR, "session_2026-07-13", "v2_9_refit_cert", "out")
DEST = os.path.join(OUT_DIR, "engine", "rl_after", "export_attribution.json")

STAGES = [("base", "g_base.json"), ("+L1", "g_L1.json"), ("+L1+L4", "g_L1L4.json"),
          ("+L1+L4+L2", "g_L1L4L2.json"), ("+L1+L4+L2+L3", "g_L1L4L2L3.json"), ("FULL", "g_full.json")]
EXPECT_SUM = {"base": 723075, "+L1": 724371, "+L1+L4": 725799,
              "+L1+L4+L2": 731106, "+L1+L4+L2+L3": 732725, "FULL": 732725}
LEVER_OF = {"+L1": "L1", "+L1+L4": "L4", "+L1+L4+L2": "L2", "+L1+L4+L2+L3": "L3", "FULL": "L5"}


def main():
    boards = {}
    for label, fn in STAGES:
        p = os.path.join(STAGE_DIR, fn)
        if not os.path.exists(p):
            sys.exit("MISSING stage board %s (run gen_gattr_chain.sh first)" % p)
        d = json.load(open(p))
        boards[label] = d["board"]
        got = d["board_sum"]
        assert got == EXPECT_SUM[label], "stage %s sum %d != certified %d" % (label, got, EXPECT_SUM[label])
    keys = list(boards["base"].keys())
    prev_label = "base"
    vPrev = {k: boards["base"][k] for k in keys}
    levers = {k: {} for k in keys}
    for label, _ in STAGES[1:]:
        lev = LEVER_OF[label]
        for k in keys:
            levers[k][lev] = boards[label].get(k, 0) - boards[prev_label].get(k, 0)
        prev_label = label
    # invariant: base + Σ levers == FULL, per key AND in aggregate
    bad = [k for k in keys if vPrev[k] + sum(levers[k].values()) != boards["FULL"].get(k, 0)]
    assert not bad, "lever split does not close for %d keys, e.g. %s" % (len(bad), bad[:5])
    out = {"source": "certified G-ATTR stage boards (gen_gattr_chain.sh; engine 2030e5df, store b0c39d78)",
           "base_sum": EXPECT_SUM["base"], "full_sum": EXPECT_SUM["FULL"], "n": len(keys),
           "lever_order": ["L1", "L4", "L2", "L3", "L5"], "vPrev": vPrev, "levers": levers}
    json.dump(out, open(DEST, "w"), sort_keys=True)
    print("wrote %s | n=%d base_sum=%d full_sum=%d | split closes for all keys" %
          (os.path.relpath(DEST, OUT_DIR), len(keys), EXPECT_SUM["base"], EXPECT_SUM["FULL"]))


if __name__ == "__main__":
    main()
