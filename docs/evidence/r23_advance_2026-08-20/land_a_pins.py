#!/usr/bin/env python3
"""ACT 1 (THE SHEET RE-CUT), LANDING STEP A — THE BOARD ARTIFACT AND THE TWO PINS THAT MOVE.

ADAPTED, byte-for-byte in structure, from docs/evidence/d8_adoption_2026-08-20/land_a_pins.py, which
itself carries the C3 pattern (docs/evidence/landing_prep_2026-08-20/rekey_c3.py + sync_board.sh):
the pin and the artifact move TOGETHER or Guard 5 goes red on the board leg, and every new value is
COMPUTED here, in this process, from the tree — never typed in from the brief or the prereg.

WHAT IS ADAPTED: the source board is this act's BARE build (the sheet re-cut board, B0) instead of the
D8 board; OLD_BOARD is the D8 board 5ea978f7 (B_precut) and OLD_ENGINE is 3cfc4325. EXPECT_BOARD is
NOT a brief value — it is the md5 this seat's own build produced and recorded in
02_recut_builds.txt before this script was written, carried here only so the install can be
cross-checked against the artifact it is installing.

WHAT MOVES
  data/rl_build/rl_app_data.json           <- the BARE build's board       (the PUBLISHED board)
  data/rl_build/rl_app_data.json.srcmd5    <- the BARE build's own sidecar (the build wrote it)
  engine/rl_after/rl_app_data.json         <- the BARE build's board       (the GENERATOR's output;
  engine/rl_after/rl_app_data.json.srcmd5     round_apply.py:141 — THE BAKE 48ec96f and the D8
                                              adoption both moved this pair in lockstep)
  data/expected_boot.json  board       5ea978f7... -> md5(data/rl_build/rl_app_data.json) AFTER install
  data/expected_boot.json  engine_head 3cfc4325... -> md5(engine/rl_after/_merged_recover.py)

SURGICAL on expected_boot.json: raw text, exact-value replacement, each old value asserted to occur
EXACTLY ONCE in the whole file before it is touched. json.load/json.dump NEVER rewrite it, so every
note field, key order and byte of whitespace survives. Re-read afterwards and the ONLY differing
bytes are asserted to be the two declared pins.
"""
import hashlib, json, os, shutil, sys

ROOT = '/home/user/afl-rl-engine'
OUT  = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/r23_work/out'
BARE = os.path.join(OUT, 'BARE_DEV.board.json')
BARE_SC = BARE + '.srcmd5'
EXPECT_BOARD = '1d5c9f7a3898c7cc62d0e91787ee2606'    # B0 — BUILT by this seat, not supplied
OLD_BOARD    = '5ea978f7b6a073abb2012f10cccbc3e3'    # B_precut — the D8 adoption board
OLD_ENGINE   = '3cfc4325aa323b7f26594cb2a202a976'
APPLY = '--apply' in sys.argv

def md5(p):
    h = hashlib.md5()
    with open(p,'rb') as f:
        for c in iter(lambda: f.read(1<<16), b''): h.update(c)
    return h.hexdigest()

P = lambda *a: os.path.join(ROOT,*a)
print('='*100)
print('ACT 1 LANDING STEP A — board artifact + the two pins that move   (%s)'%('APPLY' if APPLY else 'DRY RUN'))
print('='*100)

# ---- 1. the source board must BE the board this seat built, verified before it is copied anywhere --
s = md5(BARE)
print('source board (this seat BUILT it, bare, dev == canonical byte-identical): %s'%s)
if s != EXPECT_BOARD:
    raise SystemExit('HALT: source board %s != the built board %s'%(s, EXPECT_BOARD))
sc = json.load(open(BARE_SC))
if sc['own_md5'] != EXPECT_BOARD or sc['source_md5'] != md5(P('engine','rl_after','rl_model_data.json')):
    raise SystemExit('HALT: the build sidecar disagrees with the board or the live store: %r'%sc)
print('source sidecar (the build wrote it)             : %s'%json.dumps(sc,sort_keys=True))
print()

TARGETS = [('data/rl_build/rl_app_data.json',        BARE,    'PUBLISHED board (Guard 5 0c asserts this copy)'),
           ('data/rl_build/rl_app_data.json.srcmd5', BARE_SC, 'published sidecar'),
           ('engine/rl_after/rl_app_data.json',      BARE,    'GENERATOR output (THE BAKE 48ec96f + D8 moved it too)'),
           ('engine/rl_after/rl_app_data.json.srcmd5', BARE_SC,'generator sidecar')]
for rel, src, why in TARGETS:
    before = md5(P(rel))
    print('  %-42s %s -> %s   [%s]'%(rel, before[:12], md5(src)[:12], why))
    if APPLY:
        shutil.copyfile(src, P(rel))
        after = md5(P(rel))
        if after != md5(src): raise SystemExit('HALT: %s did not take'%rel)

# ---- 2. the pins, COMPUTED from the tree AFTER the install --------------------------------------
print()
new_board  = md5(P('data','rl_build','rl_app_data.json'))
new_engine = md5(P('engine','rl_after','_merged_recover.py'))
print('COMPUTED from the tree (never typed):')
print('  board       = md5(data/rl_build/rl_app_data.json)      = %s'%new_board)
print('  engine_head = md5(engine/rl_after/_merged_recover.py)  = %s'%new_engine)
if APPLY and new_board != EXPECT_BOARD:
    raise SystemExit('HALT: installed board %s != %s'%(new_board, EXPECT_BOARD))
if new_engine == OLD_ENGINE:
    raise SystemExit('HALT: engine_head did not move — the six-pin edit is not in the tree')

pin = P('data','expected_boot.json')
raw = open(pin, encoding='utf-8').read()
edits = [('board', OLD_BOARD, new_board), ('engine_head', OLD_ENGINE, new_engine)]
for field, old, new in edits:
    n = raw.count(old)
    print('  expected_boot %-12s %s -> %s   (old value occurs %d time(s) in the file)'%(field, old[:12], new[:12], n))
    if n != 1: raise SystemExit('HALT: %s old value occurs %d times, refusing a non-unique replacement'%(field,n))

# ---- 3. everything else in the manifest asserted UNMOVED (PREREG §3.3) --------------------------
exp_before = json.loads(raw)
MUST_NOT_MOVE = ('config','rl_model','fv','store','band','register','q97m','v0surf','peak_model',
                 'bust_prior','pvc_snapshot','balanced_board_md5','as_of_round','release_version')
new_raw = raw
for field, old, new in edits:
    new_raw = new_raw.replace(old, new)
exp_after = json.loads(new_raw)
bad = [k for k in MUST_NOT_MOVE if exp_before.get(k) != exp_after.get(k)]
if bad: raise SystemExit('HALT: PREREG §3.3 — these must not move and did: %s'%bad)
moved = [k for k in exp_after if exp_before.get(k) != exp_after.get(k)]
print()
print('  fields that moved in expected_boot.json: %s'%sorted(moved))
if sorted(moved) != ['board','engine_head']:
    raise SystemExit('HALT: expected exactly board+engine_head to move, got %s'%sorted(moved))
print('  PREREG §3.3 must-not-move list: %d checked, 0 moved'%len(MUST_NOT_MOVE))
probe = new_raw
for field, old, new in edits: probe = probe.replace(new, old)
if probe != raw: raise SystemExit('HALT: bytes beyond the two declared pin values changed')
print('  byte check: the ONLY bytes that differ are the two declared pin values.')

if APPLY:
    tmp = pin + '.tmp_land'
    open(tmp,'w',encoding='utf-8').write(new_raw)
    os.replace(tmp, pin)
    back = json.load(open(pin))
    assert back['board'] == new_board and back['engine_head'] == new_engine, 'pins did not take'
    print('\nWRITTEN and re-read. expected_boot.board=%s  engine_head=%s'%(back['board'], back['engine_head']))
else:
    print('\n--dry-run: nothing written.')
