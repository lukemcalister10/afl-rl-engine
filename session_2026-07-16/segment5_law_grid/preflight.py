#!/usr/bin/env python3
"""LEG B SEGMENT-5 — PRE-RUN ASSERTIONS (directive step 0, the checkpoint's 3rd committed item).

Asserts the build's pre-conditions BEFORE any grid measurement or board regeneration: the FEED seals, the
ONE owner-set constant landed (UNCOMP_DECAY = 0.25), the acceptance leg_b entries agree with the built law
(decay 0.25 · threshold 0.80 · the grid · recency_invariant · movement_ledger · lambda pre-gate retired),
and the pinned store / A-B baseline board are untouched. HALT (exit 1) on ANY mismatch — silence is a red.

Reads only; writes NOTHING (no store/engine/board/docs). Run from anywhere: it self-locates the repo root.
No engine load — the constant is parsed from source so this is cheap and runs before the heavy grid."""
import json, hashlib, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
def _p(*a): return os.path.join(REPO, *a)
def md5(path):
    h = hashlib.md5(); h.update(open(path, 'rb').read()); return h.hexdigest()

FAIL = []
def chk(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond: FAIL.append(msg)

print("=== FEED seals (mismatch => HALT) ===")
chk(md5(_p('docs/MEMO_LEGB_functional_form_2026-07-16.md')) == 'cf6c00804538a73234a821c5472d1a8f',
    "memo v1.3 md5 == cf6c00804538a73234a821c5472d1a8f (THE LAW)")
chk(md5(_p('docs/acceptance_v1_20.json')) == '6b83e3368ecd19843663ffd9b1c41695',
    "acceptance v1.20 md5 == 6b83e3368ecd19843663ffd9b1c41695")

print("=== the ONE flipped constant landed (parsed from source, no engine load) ===")
_rl = open(_p('engine/rl_after/rl_model.py')).read()
_m = re.search(r'^UNCOMP_DECAY\s*=\s*([0-9.]+)', _rl, re.M)
chk(_m is not None and float(_m.group(1)) == 0.25,
    "UNCOMP_DECAY == 0.25 (owner-set R105.6; the seat's 0.5 retired) — got %s" % (_m.group(1) if _m else None))

print("=== acceptance leg_b agrees with the built law ===")
_acc = json.load(open(_p('docs/acceptance_v1_20.json')))['leg_b']
_rho = _acc['rho_construction']; _sd = _acc['s_dial_selection']
chk(float(_rho['decay_declared']) == 0.25, "acceptance rho_construction.decay_declared == 0.25")
chk('OWNER-SET' in _rho.get('decay_provenance', ''), "acceptance decay provenance == OWNER-SET (R105.6)")
chk(float(_sd['threshold']) == 0.80, "acceptance s_dial_selection.threshold == 0.80 (owner bar)")
chk('OWNER-SET' in _sd.get('threshold_provenance', ''), "acceptance threshold provenance == OWNER-SET (replaces seat 0.85)")
chk([float(x) for x in _sd['grid']] == [0.55, 0.60, 0.65, 0.70],
    "acceptance s_dial grid == [0.55, 0.60, 0.65, 0.70] — got %s" % _sd['grid'])
chk('recency_invariant' in _acc, "acceptance carries leg_b.recency_invariant (R105.5)")
chk('movement_ledger' in _acc, "acceptance carries leg_b.movement_ledger (R105.5)")
chk('lambda_pre_gate' not in json.dumps(_acc), "acceptance: lambda pre-gate RETIRED (R105.6 — the grid is the arbiter)")
chk('exclusion' in _rho['forbidden'] and 'floor' in _rho['forbidden'] and 'phase' in _rho['forbidden'],
    "acceptance rho_construction.forbidden names exclusion + floor + phase (the R105.4 forbidden-list)")

print("=== store + A/B baseline board untouched ===")
_exp = json.load(open(_p('data/expected_boot.json')))
chk(md5(_p('engine/rl_after/rl_model_data.json')) == _exp['store'] == 'b1fd0bced30baa838325814c39d43233',
    "store md5 == b1fd0bce (== expected_boot pin; FENCE: store untouched)")
chk(md5(_p('data/rl_build/rl_app_data.json')) == '8d90c9ac4535f6a9969846a771544ff2',
    "checked-in board == 8d90c9ac (the Leg-A head; the RL_UNCOMP=0 A/B target)")

print("\n" + ("PREFLIGHT FAILED: %d check(s)\n  - " % len(FAIL) + "\n  - ".join(FAIL) if FAIL else
      "PREFLIGHT PASSED: seals + the flip + acceptance + store/board all consistent — cleared to run the grid."))
sys.exit(1 if FAIL else 0)
