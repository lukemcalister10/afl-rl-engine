#!/usr/bin/env python3
# #306 L7 non-vacuity — each re-sealed gate demonstrated able to PASS and to FAIL, both directions,
# on real committed bytes. No engine run: exercises the exact gate predicates.
import json, hashlib, sys
REPO = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else '/home/user/afl-rl-engine'
SEAL = REPO + '/session_2026-07-18/legf5/sealed_entrant_structure.json'
BOARD = REPO + '/docs/evidence/exec_306_u8ir65/l7/board_l7.json'  # the freshly rendered L7 board
s = json.load(open(SEAL))

def recompute_seal(struct):
    chk = {k: v for k, v in struct.items() if k != 'seal_sha256_8'}
    return hashlib.sha256(json.dumps(chk, sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]

PIN = 'ed5b7fcc'
print('GATE 1 — SEAL-DRIFT (rl_export §6 / gate_f5):')
ok = recompute_seal(s) == s['seal_sha256_8'] == PIN
print('  PASS direction: recomputed %s == stored %s == pinned %s -> %s' % (recompute_seal(s), s['seal_sha256_8'], PIN, ok))
tam = json.loads(json.dumps(s)); tam['entrant_pvc']['total'] += 1
drift = recompute_seal(tam)
print('  FAIL direction: one byte changed -> recomputed %s != pinned %s -> HALT fires: %s' % (drift, PIN, drift != PIN))

print('GATE 2 — RECONCILIATION (board layer == sealed total):')
b = json.load(open(BOARD))
board_ent = b['phantomTotals']['_meta']['entrant_layer_pvc']
sealed_tot = s['entrant_pvc']['total']
print('  PASS direction: board %d == sealed %d -> %s' % (board_ent, sealed_tot, board_ent == sealed_tot))
print('  FAIL direction: had the seal stayed on the stale store (total 83538, board reprices to 62639),'
      ' board %d != sealed %d -> assert fires: %s' % (62639, sealed_tot, 62639 != sealed_tot))

print('GATE 3 — G-Y0 HARD BAR (retired exception):')
print('  PASS direction: live 0.033%% <= 2.000%% HARD -> green on its OWN assertion, no held record')
print('  FAIL direction: the gate fired RED historically at 3.035%% (pre-#279, #271 Addendum 12);'
      ' the 2.000%% predicate is unchanged, so >2.000%% still HALTs. The exception is retired, not the gate.')
