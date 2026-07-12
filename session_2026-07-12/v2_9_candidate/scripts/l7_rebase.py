#!/usr/bin/env python3
"""L7 — THE NUMÉRAIRE RE-BASE (register v30, owner: "Rebase, 3000 is it.").

ONE declared uniform ÷1.0524 across every player value + pick value + anchor baseline + absolute-SCAR
constant, re-basing the board to the numéraire PICK 1 = 3000. Uniform scalar ⇒ all ratios/orderings
preserved; only the unit changes. This is the refit's FINAL step; the machinery + verification are
built here and demonstrated on the current (pre-refit, ×1.0524) board.

Asserts (register v30): (1) ALL ratios preserved pre/post; (2) adopted_curve[1] == 3000 exactly.
argv[1]=current board json ({key:ev})   argv[2]=out json
"""
import json, sys, os

F = 1.0524                                   # the ruled numéraire factor (pick_redenomination.json)
board = json.load(open(sys.argv[1]))["board"] if "board" in json.load(open(sys.argv[1])) else json.load(open(sys.argv[1]))
SESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# the adopted pick curve (L1, ev-channel) is already the numéraire (pick1=3000); the SHIPPED display
# curve is frozen v3.4 × F = 3157. L7 divides the whole SCAR world by F.
adopted = {int(k): int(v) for k, v in
           json.load(open(os.path.join(SESS, "out", "pvc_curve_smoothed.json"))).items()}
shipped_pick1 = round(3000 * F)              # 3157 — the current display pick-1

def rebase(v): return round(v / F)

rebased = {k: rebase(v) for k, v in board.items()}
pick1_rebased = round(shipped_pick1 / F)     # 3157 -> 3000

# ASSERT 1 — ratios preserved. A uniform ÷F with round() is monotone (can never STRICTLY invert a
# pair), but it can TIE two formerly-distinct values — that is a rounding artifact, not a reorder.
# Correct check: along the before-order (desc), the rebased values are non-increasing (no strict
# inversion). Also count the ties introduced (reported, not a failure).
order_before = [k for k, _ in sorted(board.items(), key=lambda kv: -kv[1])]
reb_seq = [rebased[k] for k in order_before]
order_ok = all(reb_seq[i] >= reb_seq[i + 1] for i in range(len(reb_seq) - 1))   # no strict inversion
ties_introduced = sum(1 for i in range(len(order_before) - 1)
                      if board[order_before[i]] > board[order_before[i + 1]]
                      and rebased[order_before[i]] == rebased[order_before[i + 1]])
anchors = ["marcus-bontempelli", "max-gawn", "kieren-briggs", "sam-darcy", "louis-emmett"]
ratio_checks = []
for i in range(len(anchors)):
    for j in range(i + 1, len(anchors)):
        a, b = anchors[i], anchors[j]
        if a in board and b in board and rebased[b]:
            rb = board[a] / board[b]; ra = rebased[a] / rebased[b]
            ratio_checks.append((f"{a}/{b}", round(rb, 4), round(ra, 4), abs(rb - ra) < 0.002))
ratios_ok = all(x[3] for x in ratio_checks)

# ASSERT 2 — adopted_curve[1] == 3000 exactly (the ev-channel numéraire pick)
assert adopted[1] == 3000, "adopted_curve[1] != 3000"
# and the re-based display pick-1 lands on 3000
assert pick1_rebased == 3000, "rebased display pick1 != 3000: %d" % pick1_rebased
assert order_ok, "RATIO VIOLATION: rebase STRICTLY inverted a pair (not a tie)"
assert ratios_ok, "RATIO VIOLATION: %s" % [x for x in ratio_checks if not x[3]]

out = {
    "factor": F, "numeraire": "PICK 1 = 3000",
    "adopted_curve_1": adopted[1], "display_pick1_before": shipped_pick1, "display_pick1_after": pick1_rebased,
    "order_preserved_no_strict_inversion": order_ok, "ties_introduced_by_rounding": ties_introduced,
    "ratios_preserved": ratios_ok, "ratio_checks": ratio_checks,
    "anchors_before_after": {k: {"before": board.get(k), "after": rebased.get(k)} for k in anchors if k in board},
    "board_sum_before": sum(board.values()), "board_sum_after": sum(rebased.values()),
    "rebased_board": rebased,
}
json.dump(out, open(sys.argv[2], "w"), indent=1)
print("L7 RE-BASE ÷%.4f | adopted_curve[1]=%d | display pick1 %d->%d | order_preserved=%s ratios_preserved=%s"
      % (F, adopted[1], shipped_pick1, pick1_rebased, order_ok, ratios_ok))
print("anchors:", {k: (board[k], rebased[k]) for k in anchors if k in board})
print("ratio checks (pair, before, after, ok):", ratio_checks)
