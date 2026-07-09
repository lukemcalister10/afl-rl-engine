#!/usr/bin/env python3
"""Red-path proof for gate-integrity (a): B1/B3 certify the CANDIDATE, not the baked v2.5 matrix.

Mirrors the exact __meta__ predicate the ship_gates_check.py candidate-matrix regen runner applies:
  - a regenerated matrix must carry __meta__ whose engine/store/config hashes equal the candidate under
    test, or the gate FAILS (not a warning);
  - the baked v2.5 matrix (data/s4_matrix_baked_efea88e5.json) carries NO __meta__ -> it can NEVER be
    passed off as "the candidate" (it is the NAMED v2.5 comparator only);
  - a matrix regenerated under a DIVERGENT config (different config hash) is REJECTED — this is the exact
    'stale/other artifact certified as current' hole the fix closes.
Run:  python3 session_2026-07-09/gate_integrity/test_a_matrix_provenance.py
"""
import os, sys, json

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HEAD, STORE, CONFIG = '4b08796c', 'e1b4d8bf', 'd88404f076333cec017e3db5b2829024e4467e5d2e5bfa35a29861d6b4c591c6'
fails = []


def expect(label, cond, detail=''):
    print(("  PASS " if cond else "  FAIL ") + label + ('' if cond else '  <-- ' + detail))
    if not cond:
        fails.append(label)


def meta_ok(meta):
    # verbatim predicate from ship_gates_check.py candidate-matrix regen check
    ok = bool(meta) and meta.get('engine_head_md5', '')[:8] == HEAD and meta.get('store_md5', '')[:8] == STORE
    if CONFIG is not None:
        ok = ok and (meta.get('config_sha256') == CONFIG)
    return ok


print("=== gate-integrity (a) candidate-matrix provenance red-path proof ===")

# 1) genuine candidate meta -> accepted
expect("genuine candidate __meta__ accepted",
       meta_ok({'engine_head_md5': HEAD + '0' * 24, 'store_md5': STORE + '0' * 24, 'config_sha256': CONFIG}))

# 2) the baked v2.5 matrix carries NO __meta__ -> can never be certified as the candidate
v25 = os.path.join(ROOT, 'data', 's4_matrix_baked_efea88e5.json')
if os.path.exists(v25):
    _d = json.load(open(v25))
    expect("baked v2.5 matrix has NO __meta__ (comparator only)", '__meta__' not in _d,
           "v2.5 matrix unexpectedly carries __meta__")
    expect("v2.5 matrix rejected as candidate (no __meta__)", not meta_ok(_d.get('__meta__', {})))
else:
    print("  SKIP v2.5 comparator not present at", v25)

# 3) divergent-config matrix (right code+store, wrong config) -> REJECTED
expect("divergent-config matrix REJECTED",
       not meta_ok({'engine_head_md5': HEAD + '0' * 24, 'store_md5': STORE + '0' * 24, 'config_sha256': 'f' * 64}))

# 4) stale-engine matrix (v2.5 engine head efea88e5) -> REJECTED
expect("stale-engine (efea88e5) matrix REJECTED",
       not meta_ok({'engine_head_md5': 'efea88e5' + '0' * 24, 'store_md5': STORE + '0' * 24, 'config_sha256': CONFIG}))

print("\nRESULT:", "ALL PASS" if not fails else "FAILED: " + ", ".join(fails))
sys.exit(1 if fails else 0)
