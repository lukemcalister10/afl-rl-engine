#!/usr/bin/env python3
# LEG F4 §2.vii — measure the REALIZED backward-transition rate r_real(a) per age-transition, from F3's
# committed -2/-1/now boards (stamped F2 artifacts). READ-ONLY, no engine. This is the SEAL input.
import json, statistics as st, sys
from collections import defaultdict
F2 = '/home/user/afl-rl-engine/session_2026-07-18/legf3/f2_boards/'
def load(fn, asof):
    rows = json.load(open(F2 + fn))['rows']
    out = {}
    for r in rows:
        dy = r.get('draft_year') or r.get('yr') or (asof - 3)
        a = round((asof - dy) + 18.5)
        out[r['key']] = (a, r.get('v') or 0)
    return out
bm2 = load('board_minus2_2024.json', 2024)
bm1 = load('board_minus1_2025.json', 2025)
bnow = load('board_now_2026.json', 2026)

# realized one-year transitions: age-at-start a -> ratio v(next)/v(start), pooled over both consecutive pairs
trans = defaultdict(list)
for early, late in ((bm2, bm1), (bm1, bnow)):
    for k, (a, v) in early.items():
        if k in late and v > 50:
            vn = late[k][1]
            if vn > 0: trans[a].append(vn / v)
print("=== REALIZED backward-transition rate r_real(a) = median v(a+1)/v(a), pooled -2/-1/now ===")
print("  age  n   r_real   (decline%)")
ages = sorted(trans)
raw = {}
for a in ages:
    m = st.median(trans[a]); raw[a] = m
    print("  %3d %3d  %.4f  (%+.1f%%)" % (a, len(trans[a]), m, 100 * (m - 1)))

# overall realized
allr = [x for a in trans for x in trans[a]]
print("  pooled median r_real = %.4f (%+.1f%%) over n=%d transitions" % (st.median(allr), 100*(st.median(allr)-1), len(allr)))
json.dump({str(a): raw[a] for a in raw}, open('/tmp/r_real_raw.json', 'w'))
