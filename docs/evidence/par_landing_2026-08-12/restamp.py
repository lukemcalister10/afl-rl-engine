"""ORDER 20C — install the rebuilt FIX board and restamp every identity carrier that moves.

Follows the ORDER 9 bake precedent (7f4d5d2 / 56665de) exactly: the board lands at
data/rl_build/rl_app_data.json AND engine/rl_after/rl_app_data.json; the srcmd5 sidecar and the
provenance sidecar are rewritten; data/expected_boot.json gets the two pins that moved and nothing
else. Every field this touches is printed before/after so the diff is auditable.
"""
import json, hashlib, os, sys, shutil

ROOT = '/home/user/afl-rl-engine/.claude/worktrees/agent-a6af0d68789879235'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o20c'
FIXBOARD = os.path.join(SP, 'board_FIX.json')
EXPECT_BOARD = '1dbd1480a34c7823f330273211cbb76a'

sys.path.insert(0, ROOT)
os.environ['RL_REPO'] = ROOT
import fv_provenance as F


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


assert md5(FIXBOARD) == EXPECT_BOARD, "rebuilt board is not %s" % EXPECT_BOARD

# ---- 0. the landed forward-valuation identity -------------------------------------------------
fvdir = os.path.join(ROOT, 'engine', 'forward_valuation')
fvid = F.fv_identity(fvdir)
print("landed fv_identity        :", fvid)
srcsha = {f: hashlib.sha256(open(os.path.join(fvdir, f), 'rb').read()).hexdigest()
          for f in sorted(os.listdir(fvdir)) if f.endswith('.py')}

# ---- 1. the board, both tracked copies ---------------------------------------------------------
for rel in ('data/rl_build/rl_app_data.json', 'engine/rl_after/rl_app_data.json'):
    p = os.path.join(ROOT, rel)
    print("board %-40s %s -> " % (rel, md5(p)), end='')
    shutil.copyfile(FIXBOARD, p)
    print(md5(p))
    assert md5(p) == EXPECT_BOARD

# ---- 2. the working board's srcmd5 sidecar -----------------------------------------------------
sp = os.path.join(ROOT, 'engine/rl_after/rl_app_data.json.srcmd5')
s = json.load(open(sp))
print("srcmd5 own_md5            :", s['own_md5'], "->", EXPECT_BOARD)
assert s['source_md5'] == 'd9a24282357cf3083b1640466e3ecd83', "store moved — HALT"
s['own_md5'] = EXPECT_BOARD
open(sp, 'w').write(json.dumps(s) + "\n")

# ---- 3. the provenance sidecar -----------------------------------------------------------------
pp = os.path.join(ROOT, 'engine/rl_after/rl_app_data.provenance.json')
pv = json.load(open(pp))
print("provenance fv_identity    :", pv['fv_identity'], "->", fvid)
pv['fv_identity'] = fvid
pv['fv_identity_expected'] = fvid
for f, h in srcsha.items():
    if pv['fv_source_hashes'].get(f) != h:
        print("provenance src %-24s %s -> %s" % (f, pv['fv_source_hashes'].get(f), h))
        pv['fv_source_hashes'][f] = h
open(pp, 'w').write(json.dumps(pv, indent=2, sort_keys=True) + "\n")

# ---- 4. the pins -------------------------------------------------------------------------------
bp = os.path.join(ROOT, 'data/expected_boot.json')
before = json.load(open(bp))
e = json.load(open(bp))
e['board'] = EXPECT_BOARD
e['fv'] = fvid
open(bp, 'w').write(json.dumps(e, indent=1) + "\n")
after = json.load(open(bp))

print("\nexpected_boot.json — every key, moved or not:")
moved = []
for k in sorted(set(before) | set(after)):
    if k.startswith('_'):
        continue
    b, a = before.get(k), after.get(k)
    if b != a:
        moved.append(k)
        print("  MOVED   %-20s %s -> %s" % (k, str(b)[:40], str(a)[:40]))
    else:
        print("  unmoved %-20s %s" % (k, str(b)[:60]))
print("\nkeys moved: %s" % moved)
assert moved == ['board', 'fv'], "*** BREACH: pins moved beyond board+fv: %s ***" % moved
print("PIN CHANGE IS EXACTLY {board, fv} — as pre-registered (P1/P2).")
