#!/usr/bin/env python3
# LEG F4 — THE GATE (MEMO_LEGF v1.3 §2.x, owner item 359): ROSTER-MATCHED, ±5%, BOTH transitions.
# Build r(age)=median(vP1/v) from the DAMPED board, project each committed historical roster forward, and
# compare to the SAME players' realized next-year values INCLUDING exiters' realized residuals (off-board=0,
# busts full weight R107.3). Survivor-only view printed as a DIAGNOSTIC (never a gate). Usage: gate_f4.py <damped_board.json>
import json, statistics as st, sys
from collections import defaultdict
BOARD = sys.argv[1]
F2 = '/home/user/afl-rl-engine/session_2026-07-18/legf3/f2_boards/'
A = json.load(open(BOARD))['active']
# r(age) = median vP1/v by draft-year age (== the damper's _lsym_age basis), v>50
rat = defaultdict(list)
for r in A:
    v = r.get('v') or 0; vP1 = r.get('vP1') or 0; yr = r.get('yr')
    if v > 50 and yr is not None:
        a = round((2026 - int(yr)) + 18.5); rat[a].append(vP1 / v)
ratmed = {a: st.median(rat[a]) for a in rat}
def r_age(a): return ratmed[a] if a in ratmed else ratmed[min(ratmed, key=lambda x: abs(x - a))]
def load(fn, asof):
    rows = json.load(open(F2 + fn))['rows']; out = {}
    for r in rows:
        dy = r.get('draft_year') or (asof - 3); a = round((asof - dy) + 18.5); out[r['key']] = (a, r.get('v') or 0)
    return out
bm2 = load('board_minus2_2024.json', 2024); bm1 = load('board_minus1_2025.json', 2025); bnow = load('board_now_2026.json', 2026)
print("=== F4 GATE — ROSTER-MATCHED, ±5%, BOTH transitions (realized INCLUDING exiters' residuals) ===")
allpass = True
for early, late, name in ((bm2, bm1, '-2 -> -1'), (bm1, bnow, '-1 -> now')):
    keys = [k for k, (a, v) in early.items() if v > 0]
    pred = sum(early[k][1] * r_age(early[k][0]) for k in keys)
    realized = sum((late[k][1] if k in late else 0.0) for k in keys)   # exiters -> 0 (full-weight bust)
    err = 100 * (pred / realized - 1); ok = abs(err) <= 5.0; allpass = allpass and ok
    print("  %s : pred=%.0f  realized(incl exiters)=%.0f  err %+.1f%%  %s" % (name, pred, realized, err, 'IN ±5%' if ok else 'OUT'))
print("  GATE:", "PASS (both ±5%)" if allpass else "FAIL")
print("\n--- DIAGNOSTIC (survivor-only; ageing-quality isolation, NOT a gate) ---")
for early, late, name in ((bm2, bm1, '-2 -> -1'), (bm1, bnow, '-1 -> now')):
    keys = [k for k, (a, v) in early.items() if v > 0 and k in late]
    pred = sum(early[k][1] * r_age(early[k][0]) for k in keys)
    realized = sum(late[k][1] for k in keys)
    print("  %s survivors: pred=%.0f realized=%.0f err %+.1f%%" % (name, pred, realized, 100 * (pred / realized - 1)))
sys.exit(0 if allpass else 1)
