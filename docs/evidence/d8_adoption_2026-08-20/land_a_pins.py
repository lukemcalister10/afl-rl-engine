#!/usr/bin/env python3
"""THE D8 ADOPTION, LANDING STEP A — THE BOARD ARTIFACT AND THE TWO PINS THAT MOVE.

THE C3 PATTERN, carried (docs/evidence/landing_prep_2026-08-20/rekey_c3.py + sync_board.sh):
the pin and the artifact move TOGETHER or Guard 5 goes red on the board leg, and every new value is
COMPUTED here, in this process, from the tree — never typed in from the brief or the register.

WHAT MOVES
  data/rl_build/rl_app_data.json           <- the BARE build's board       (the PUBLISHED board, the
                                              copy boot_guard (0c) asserts)
  data/rl_build/rl_app_data.json.srcmd5    <- the BARE build's own sidecar (not hand-composed: the
                                              build wrote it; the KILL build's sidecar is BYTE-
                                              IDENTICAL to the one currently committed, which proves
                                              the writer and the committed file agree)
  engine/rl_after/rl_app_data.json         <- the BARE build's board       (the GENERATOR's output;
  engine/rl_after/rl_app_data.json.srcmd5     round_apply.py:141. THE BAKE 48ec96f moved this pair in
                                              lockstep with the published one; this act does the same.)
  data/expected_boot.json  board       a05fe951... -> md5(data/rl_build/rl_app_data.json) AFTER install
  data/expected_boot.json  engine_head 338a790b... -> md5(engine/rl_after/_merged_recover.py)

DISCLOSED, NOT SMUGGLED: the engine-side sidecar's source_md5 is currently cb38ef11 — a lag left by
THE BAKE, before the ownership store apply advanced the store to cc02567f. Installing the build's own
sidecar moves it to cc02567f, which is what the store actually is. That is a stale value corrected by
a rebuild, not a new claim; the six-way store coherence gate reads the data/rl_build sidecar, which
was already correct.

SURGICAL on expected_boot.json: raw text, exact-value replacement, each old value asserted to occur
EXACTLY ONCE in the whole file before it is touched. json.load/json.dump NEVER rewrite it, so every
note field, key order and byte of whitespace survives. Re-read afterwards and the ONLY differing
bytes are asserted to be the two declared pins.
"""
import hashlib, json, os, shutil, sys

ROOT = '/home/user/afl-rl-engine'
OUT  = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/d8adopt/out'
BARE = os.path.join(OUT, 'BARE_DEV.board.json')
BARE_SC = BARE + '.srcmd5'
EXPECT_BOARD = '5ea978f7b6a073abb2012f10cccbc3e3'
OLD_BOARD    = 'a05fe951f78482c70520480e184c80ec'
OLD_ENGINE   = '338a790b773cfbbff0e1283794c72efe'
APPLY = '--apply' in sys.argv

def md5(p):
    h = hashlib.md5()
    with open(p,'rb') as f:
        for c in iter(lambda: f.read(1<<16), b''): h.update(c)
    return h.hexdigest()

P = lambda *a: os.path.join(ROOT,*a)
print('='*100)
print('LANDING STEP A — board artifact + the two pins that move   (%s)'%('APPLY' if APPLY else 'DRY RUN'))
print('='*100)

# ---- 1. the source board must BE the priced candidate, verified before it is copied anywhere ------
s = md5(BARE)
print('source board (this seat BUILT it, bare, F1 PASS): %s'%s)
if s != EXPECT_BOARD:
    raise SystemExit('HALT: source board %s != the priced candidate %s'%(s, EXPECT_BOARD))
sc = json.load(open(BARE_SC))
if sc['own_md5'] != EXPECT_BOARD or sc['source_md5'] != md5(P('engine','rl_after','rl_model_data.json')):
    raise SystemExit('HALT: the build sidecar disagrees with the board or the live store: %r'%sc)
print('source sidecar (the build wrote it)             : %s'%json.dumps(sc,sort_keys=True))
print()

TARGETS = [('data/rl_build/rl_app_data.json',        BARE,    'PUBLISHED board (Guard 5 0c asserts this copy)'),
           ('data/rl_build/rl_app_data.json.srcmd5', BARE_SC, 'published sidecar'),
           ('engine/rl_after/rl_app_data.json',      BARE,    'GENERATOR output (THE BAKE 48ec96f moved it too)'),
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
    raise SystemExit('HALT: engine_head did not move — the edit is not in the tree')

pin = P('data','expected_boot.json')
raw = open(pin, encoding='utf-8').read()
edits = [('board', OLD_BOARD, new_board), ('engine_head', OLD_ENGINE, new_engine)]
for field, old, new in edits:
    n = raw.count(old)
    print('  expected_boot %-12s %s -> %s   (old value occurs %d time(s) in the file)'%(field, old[:12], new[:12], n))
    if n != 1: raise SystemExit('HALT: %s old value occurs %d times, refusing a non-unique replacement'%(field,n))

# ---- 3. everything else in the manifest asserted UNMOVED (PREREG F4) -----------------------------
exp_before = json.loads(raw)
MUST_NOT_MOVE = ('config','rl_model','fv','store','band','register','q97m','v0surf','peak_model',
                 'bust_prior','pvc_snapshot','balanced_board_md5','as_of_round','release_version')
new_raw = raw
for field, old, new in edits:
    new_raw = new_raw.replace(old, new)
exp_after = json.loads(new_raw)
bad = [k for k in MUST_NOT_MOVE if exp_before.get(k) != exp_after.get(k)]
if bad: raise SystemExit('HALT: PREREG F4 — these must not move and did: %s'%bad)
moved = [k for k in exp_after if exp_before.get(k) != exp_after.get(k)]
print()
print('  fields that moved in expected_boot.json: %s'%sorted(moved))
if sorted(moved) != ['board','engine_head']:
    raise SystemExit('HALT: expected exactly board+engine_head to move, got %s'%sorted(moved))
print('  PREREG F4 must-not-move list: %d checked, 0 moved'%len(MUST_NOT_MOVE))
# byte-level: only the two declared values differ
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
