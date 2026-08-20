#!/usr/bin/env python3
"""ACT A (THE BACK-ROWS AGE_REF REPAIR), LANDING STEP A — THE ONE PIN THAT MOVES.

ADAPTED, byte-for-byte in structure, from docs/evidence/r23_advance_2026-08-20/land_a_pins.py, which
carries the D8 adoption's adaptation of the C3 pattern: every new value is COMPUTED here, in this
process, from the tree — never typed in from the brief or the prereg.

WHAT IS ADAPTED: the two board ids. The engine_head clause is carried UNCHANGED and is still true
for the same reason — this act, like the F5 act, edits the EXPORTER and not the engine:

  **`engine_head` DOES NOT MOVE, and this script asserts that it does not.**

  `engine_head` is `md5(engine/rl_after/_merged_recover.py)` — measured, not assumed: the accepted
  manifest's value 1867e953 equals that file's md5 exactly. This act edits `engine/rl_after/
  rl_export.py`, the EXPORTER, which no identity pin in `expected_boot.json` or
  `release_contract.json` tracks. The valuation engine is untouched. NOTE THE DIFFERENCE FROM THE F5
  ACT: there, no price moved at all. Here 25 BACK-HISTORY rows move — but they are priced by the
  exporter's own back_extra loop, not by a changed valuation expression, and all 804 ACTIVE rows are
  byte-identical. engine_head still must not move, and this asserts it.

  Every prior landing asserted engine_head MOVED. This one asserts the reverse, for a stated reason.
  Recorded here rather than quietly dropping the check.

WHAT MOVES
  data/expected_boot.json  board  c97a4d9f... -> md5(data/rl_build/rl_app_data.json)

The board artifact + both .srcmd5 sidecars were installed and committed with the act itself (11fe287)
— the build wrote the sidecars, they were not hand-composed. This script verifies that install is
coherent before it touches the pin, then moves the pin.

SURGICAL on expected_boot.json: raw text, exact-value replacement, the old value asserted to occur
EXACTLY ONCE in the whole file before it is touched. json.load/json.dump NEVER rewrite it, so every
note field, key order and byte of whitespace survives. Re-read afterwards and the ONLY differing
bytes are asserted to be the one declared pin.

Run:  python3 land_br_pins.py            (dry run)
      python3 land_br_pins.py --apply
"""
import hashlib, json, os, sys

ROOT = '/home/user/afl-rl-engine'
EXPECT_BOARD = '68be10c79d0ee096455754e084bcf757'    # BUILT by this seat (dev == canonical), not supplied
OLD_BOARD    = 'c97a4d9f9fa42597f85517c7850d3943'    # the F5 board this act supersedes
ENGINE_HEAD  = '1867e953cf844d089ab1da68379b1742'    # MUST NOT MOVE — see the docstring
APPLY = '--apply' in sys.argv

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()

P = lambda *a: os.path.join(ROOT, *a)
print('=' * 100)
print('ACT A (BACK-ROWS) LANDING STEP A — the one pin that moves   (%s)' % ('APPLY' if APPLY else 'DRY RUN'))
print('=' * 100)

# ---- 1. the installed board must BE the board this seat built ------------------------------------
pub = md5(P('data', 'rl_build', 'rl_app_data.json'))
gen = md5(P('engine', 'rl_after', 'rl_app_data.json'))
print('published board  data/rl_build/rl_app_data.json    : %s' % pub)
print('generator board  engine/rl_after/rl_app_data.json  : %s' % gen)
if pub != EXPECT_BOARD:
    raise SystemExit('HALT: published board %s != the built board %s' % (pub, EXPECT_BOARD))
if gen != pub:
    raise SystemExit('HALT: the generator copy %s != the published copy %s' % (gen, pub))
store_md5 = md5(P('engine', 'rl_after', 'rl_model_data.json'))
for rel in ('data/rl_build/rl_app_data.json.srcmd5', 'engine/rl_after/rl_app_data.json.srcmd5'):
    sc = json.load(open(P(rel)))
    print('  %-42s %s' % (rel, json.dumps(sc, sort_keys=True)))
    if sc['own_md5'] != EXPECT_BOARD or sc['source_md5'] != store_md5:
        raise SystemExit('HALT: sidecar %s disagrees with the board or the live store' % rel)
print('  both sidecars agree with the board they sit beside and with the live store. OK.')

# ---- 2. the pin, COMPUTED from the tree ---------------------------------------------------------
print()
new_board  = pub
new_engine = md5(P('engine', 'rl_after', '_merged_recover.py'))
print('COMPUTED from the tree (never typed):')
print('  board       = md5(data/rl_build/rl_app_data.json)      = %s' % new_board)
print('  engine_head = md5(engine/rl_after/_merged_recover.py)  = %s' % new_engine)
if new_engine != ENGINE_HEAD:
    raise SystemExit('HALT: engine_head MOVED to %s. This act edits the EXPORTER, not the engine; if '
                     '_merged_recover.py has changed, something outside this act is in the tree.' % new_engine)
print('  engine_head is UNMOVED, as this act requires: the valuation engine was not touched.')

pin = P('data', 'expected_boot.json')
raw = open(pin, encoding='utf-8').read()
n = raw.count(OLD_BOARD)
print()
print('  expected_boot %-12s %s -> %s   (old value occurs %d time(s) in the file)'
      % ('board', OLD_BOARD[:12], new_board[:12], n))
if n != 1:
    raise SystemExit('HALT: the old board value occurs %d times, refusing a non-unique replacement' % n)

# ---- 3. everything else in the manifest asserted UNMOVED ----------------------------------------
exp_before = json.loads(raw)
MUST_NOT_MOVE = ('config', 'rl_model', 'fv', 'store', 'band', 'register', 'q97m', 'v0surf',
                 'peak_model', 'bust_prior', 'pvc_snapshot', 'balanced_board_md5', 'as_of_round',
                 'release_version', 'engine_head')
new_raw = raw.replace(OLD_BOARD, new_board)
exp_after = json.loads(new_raw)
bad = [k for k in MUST_NOT_MOVE if exp_before.get(k) != exp_after.get(k)]
if bad:
    raise SystemExit('HALT: these must not move and did: %s' % bad)
moved = [k for k in exp_after if exp_before.get(k) != exp_after.get(k)]
print()
print('  fields that moved in expected_boot.json: %s' % sorted(moved))
if sorted(moved) != ['board']:
    raise SystemExit('HALT: expected exactly `board` to move, got %s' % sorted(moved))
print('  must-not-move list: %d checked (engine_head among them), 0 moved' % len(MUST_NOT_MOVE))
if new_raw.replace(new_board, OLD_BOARD) != raw:
    raise SystemExit('HALT: bytes beyond the one declared pin value changed')
print('  byte check: the ONLY bytes that differ are the one declared pin value.')

if APPLY:
    tmp = pin + '.tmp_br'
    open(tmp, 'w', encoding='utf-8').write(new_raw)
    os.replace(tmp, pin)
    back = json.load(open(pin))
    assert back['board'] == new_board, 'the pin did not take'
    assert back['engine_head'] == ENGINE_HEAD, 'engine_head must be untouched'
    print('\nAPPLIED. expected_boot.board == %s ; engine_head still %s.' % (new_board, ENGINE_HEAD))
else:
    print('\nDRY RUN — nothing written.')
