#!/usr/bin/env python3
# LEG F3 — THE ACCEPTANCE BACKTEST (frozen-form; reuses the item-352 harness S5, analyze.py job-1(B)).
# Build the smoothed one-year forward ratio r(age)=median(vP1/v) by age from the FIXED single-run board,
# then project F2's -1 board forward -> reproduce now (752,427) within ±5%; and -2 -> -1 (771,152).
import json, statistics as st, sys
from collections import defaultdict
BOARD = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/rl_ws_legf/rl_after/rl_app_data.json'
F2 = '/home/user/afl-rl-engine/session_2026-07-18/legf3/f2_boards/'
A = json.load(open(BOARD))['active']
# ratio vP1/v by age (median, v>50), smoothed by nearest-age fill
rat = defaultdict(list)
for r in A:
    v = r.get('v') or 0; vP1 = r.get('vP1') or 0; a = r.get('age')
    if v > 50 and a is not None: rat[a].append(vP1 / v)
ratmed = {a: st.median(rat[a]) for a in rat}
def ratio_for_age(a):
    if a in ratmed: return ratmed[a]
    return ratmed[min(ratmed, key=lambda x: abs(x - a))]
def backtest(board_file, asof):
    rows = json.load(open(board_file))['rows']
    pred = 0.0
    for r in rows:
        dy = r.get('draft_year') or r.get('yr') or (asof - 3)
        a = round((asof - dy) + 18.5)
        pred += (r.get('v') or 0) * ratio_for_age(a)
    return round(pred), round(sum((r.get('v') or 0) for r in rows))
p_now, m1_tot = backtest(F2 + 'board_minus1_2025.json', 2025)
p_m1, m2_tot = backtest(F2 + 'board_minus2_2024.json', 2024)
AN, AM1 = 752427, 771152
def band(pred, actual):
    e = pred - actual; return "%+d (%+.1f%%) %s" % (e, 100 * e / actual, "IN ±5%" if abs(e) <= 0.05 * actual else "OUT")
print("=== THE BACKTEST (F3 fixed board ratios applied to F2 boards) ===")
print("  -1 board %d  --project-->  now: pred %d  vs actual %d   %s" % (m1_tot, p_now, AN, band(p_now, AN)))
print("  -2 board %d  --project-->  -1 : pred %d  vs actual %d   %s" % (m2_tot, p_m1, AM1, band(p_m1, AM1)))
# composition-controlled (same roster) forward vs backward, for the record
Sv = sum(r.get('v') or 0 for r in A); SvP1 = sum(r.get('vP1') or 0 for r in A); SvM1 = sum(r.get('vM1') or 0 for r in A)
print("  [comp-controlled same-roster: fwd %+.1f%% | backward %+.1f%% | symmetric-target fwd≈%d]" %
      (100 * (SvP1 / Sv - 1), 100 * (Sv / SvM1 - 1), round(Sv * (Sv / SvM1))))
# gradient
coh = defaultdict(lambda: [0, 0.0, 0.0])
for r in A:
    a = r.get('age');
    if a is None: continue
    c = 'developing(<=23)' if a <= 23 else 'mid(24-27)' if a <= 27 else 'veteran(>=28)'
    coh[c][0] += 1; coh[c][1] += r.get('v') or 0; coh[c][2] += r.get('vP1') or 0
print("=== THE GRADIENT (signed mean Δ per player; un-inverted iff developing ≥ mid ≥ veteran) ===")
for c in ('developing(<=23)', 'mid(24-27)', 'veteran(>=28)'):
    n, now, fwd = coh[c]; print("  %-16s n=%3d  mean Δ %+7.1f   (%+.1f%%)" % (c, n, (fwd - now) / n, 100 * (fwd - now) / now))
