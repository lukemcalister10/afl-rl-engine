#!/usr/bin/env python3
# LEG F5 — THE CONSERVATION GATE (MEMO_LEGF v1.3 §2.x, owner item 359).
#  (A) F5 LEAGUE-LEVEL, ±5%, BOTH transitions: project each committed historical roster forward under the
#      population rate, ADD the §2.viii entrant layer at PVC, vs the REALIZED league total (F2 bridge_totals,
#      ~flat 771k/771k/752k). This is the owner's conservation law itself.
#  (B) F4 ROSTER-MATCHED, ±5%, BOTH transitions (re-run — must stay IN): same-players realized incl exiters.
#  (C) Survivor-only DIAGNOSTIC (ageing-quality isolation; never a gate).
# The roster projection reuses F4's harness: r(age)=median(vP1/v) from the DAMPED board (== r_pop by the
# s(age) bisection). The r_pop-direct variant is also reported. The entrant layer value is read from the
# SEALED structure (seal-verified) and cross-checked against the board's emitted phantomTotals.
# Usage: gate_f5.py <damped_board.json> <sealed_entrant_structure.json>
import json, statistics as st, sys, hashlib
from collections import defaultdict

BOARD = sys.argv[1]
SEAL = sys.argv[2]
REPO = '/home/user/afl-rl-engine'
F2 = REPO + '/session_2026-07-18/legf3/f2_boards/'
board = json.load(open(BOARD)); A = board['active']

# ---- entrant layer (seal-verified) ----
struct = json.load(open(SEAL))
chk = {k: v for k, v in struct.items() if k != 'seal_sha256_8'}
seal = hashlib.sha256(json.dumps(chk, sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]
assert seal == struct['seal_sha256_8'] == 'a17aafed', 'SEAL DRIFT %s/%s' % (seal, struct['seal_sha256_8'])
ENT = struct['entrant_pvc']['total']
board_ent = board.get('phantomTotals', {}).get('_meta', {}).get('entrant_layer_pvc')
print('ENTRANT LAYER (sealed a17aafed): %d PVC (draft %d + mech %d)  | board emitted: %s  | MATCH %s'
      % (ENT, struct['entrant_pvc']['draft'], struct['entrant_pvc']['mech'], board_ent, board_ent == ENT))

# ---- realized league totals (F2 bridge_totals, the reality) ----
BR = json.load(open(F2 + 'bridge_totals.json'))['totals']
realized = {'minus2': BR['minus2']['total_v'], 'minus1': BR['minus1']['total_v'], 'now': BR['now']['total_v']}
print('REALIZED league totals (F2 bridge): minus2=%d  minus1=%d  now=%d  (~flat)'
      % (realized['minus2'], realized['minus1'], realized['now']))

# ---- r(age) = median vP1/v by draft-year age from the DAMPED board (F4 harness, S5 reuse) ----
rat = defaultdict(list)
for r in A:
    v = r.get('v') or 0; vP1 = r.get('vP1') or 0; yr = r.get('yr')
    if v > 50 and yr is not None:
        a = round((2026 - int(yr)) + 18.5); rat[a].append(vP1 / v)
ratmed = {a: st.median(rat[a]) for a in rat}
def r_board(a): return ratmed[a] if a in ratmed else ratmed[min(ratmed, key=lambda x: abs(x - a))]

# ---- r_pop-direct (sealed population rate) ----
rpop = {int(k): v for k, v in json.load(open(REPO + '/session_2026-07-18/legf4/sealed_rate_pop.json'))['r_pop'].items()}
rk = sorted(rpop)
def r_pop(a): return rpop[min(rk, key=lambda x: abs(x - a))]

def load(fn, asof):
    rows = json.load(open(F2 + fn))['rows']; out = {}
    for r in rows:
        dy = r.get('draft_year') or (asof - 3); a = round((asof - dy) + 18.5); out[r['key']] = (a, r.get('v') or 0)
    return out
bm2 = load('board_minus2_2024.json', 2024); bm1 = load('board_minus1_2025.json', 2025); bnow = load('board_now_2026.json', 2026)

TR = ((bm2, bm1, realized['minus1'], '-2 -> -1'), (bm1, bnow, realized['now'], '-1 -> now'))

print("\n=== (A) F5 CONSERVATION GATE — LEAGUE-LEVEL, ±5%, BOTH transitions (roster @ r_pop + §2.viii entrant layer) ===")
allpass = True
for early, late, real_tot, name in TR:
    keys = [k for k, (a, v) in early.items() if v > 0]
    proj = sum(early[k][1] * r_board(early[k][0]) for k in keys)
    pred = proj + ENT
    err = 100 * (pred / real_tot - 1); ok = abs(err) <= 5.0; allpass = allpass and ok
    print("  %s : roster_proj=%.0f + entrant=%d = pred=%.0f  vs realized=%d  err %+.1f%%  %s"
          % (name, proj, ENT, pred, real_tot, err, 'IN ±5%' if ok else 'OUT'))
print("  F5 LEAGUE GATE:", "PASS (both ±5%)" if allpass else "FAIL")

print("  [r_pop-direct variant]:")
for early, late, real_tot, name in TR:
    keys = [k for k, (a, v) in early.items() if v > 0]
    proj = sum(early[k][1] * r_pop(early[k][0]) for k in keys)
    pred = proj + ENT; err = 100 * (pred / real_tot - 1)
    print("    %s : pred=%.0f vs %d  err %+.1f%%  %s" % (name, pred, real_tot, err, 'IN' if abs(err) <= 5 else 'OUT'))

print("\n=== (B) F4 ROSTER-MATCHED GATE (re-run — must stay IN ±5%; realized = SAME players incl exiters) ===")
f4pass = True
for early, late, real_tot, name in ((bm2, bm1, None, '-2 -> -1'), (bm1, bnow, None, '-1 -> now')):
    keys = [k for k, (a, v) in early.items() if v > 0]
    pred = sum(early[k][1] * r_board(early[k][0]) for k in keys)
    rz = sum((late[k][1] if k in late else 0.0) for k in keys)
    err = 100 * (pred / rz - 1); ok = abs(err) <= 5.0; f4pass = f4pass and ok
    print("  %s : pred=%.0f  realized(incl exiters)=%.0f  err %+.1f%%  %s" % (name, pred, rz, err, 'IN ±5%' if ok else 'OUT'))
print("  F4 ROSTER-MATCHED GATE:", "PASS (both ±5%)" if f4pass else "FAIL")

print("\n--- (C) DIAGNOSTIC (survivor-only; ageing-quality isolation, NOT a gate) ---")
for early, late, real_tot, name in ((bm2, bm1, None, '-2 -> -1'), (bm1, bnow, None, '-1 -> now')):
    keys = [k for k, (a, v) in early.items() if v > 0 and k in late]
    pred = sum(early[k][1] * r_board(early[k][0]) for k in keys)
    rz = sum(late[k][1] for k in keys)
    print("  %s survivors: pred=%.0f realized=%.0f err %+.1f%%" % (name, pred, rz, 100 * (pred / rz - 1)))

sys.exit(0 if (allpass and f4pass) else 1)
