#!/usr/bin/env python3
"""ORDER 25 -- INSTALL THE LANDED BOARD AND RESTAMP EVERY IDENTITY CARRIER THAT MOVES.

Carried from docs/evidence/pool_landing_2026-08-12/o23_restamp.py. The mechanism is identical; the
EXPECTED MOVED SET is different, and that difference is the whole point of the assertion.

  usage: o25_restamp.py <tree> <board.json>

Follows the ORDER 20C landing (and through it the ORDER 9 bake precedent 7f4d5d2 / 56665de): the
board lands at data/rl_build/rl_app_data.json AND engine/rl_after/rl_app_data.json; the srcmd5 and
provenance sidecars are rewritten; data/expected_boot.json gets the pins that moved and nothing else.

THE MOVED SET IS ASSERTED BEFORE ANYTHING IS WRITTEN TO THE PIN FILE, and every key is printed moved
or not, so "only these four moved" is a check rather than a claim:

    board        the pool update v2 moves 117 board rows
    engine_head  _merged_recover.py: the amended par literals and the re-derived U'''

    config       MUST NOT MOVE -- H_POOLSIT / H_UNION were already retired to 1.0 by ORDER 23 and
                 this act touches no manifest var. ORDER 23 moved it; ORDER 25 must not.
    rl_model     MUST NOT MOVE -- the ND65+ cap amendment was ORDER 23's code change and is already
                 landed. ORDER 25 HAS NO CODE CHANGE AT ALL.
    fv           MUST NOT MOVE -- no engine/forward_valuation source is touched by this act
    store, band, q97m, v0surf, peak_model, pvc_snapshot, bust_prior, register  MUST NOT MOVE

Note that `curve_artifact` (pvc_curve_v2.json) is NOT an expected_boot pin -- it is bound instead by
ui/release_pick_curve.json's pick_curve_file_md5 and by the self-test's contract pin, both of which
moved in the levers commit. That is where the signed table's identity lives, and it is why the pin
file's moved set here is two keys and not three.
"""
import json, hashlib, os, sys, shutil

TREE, BOARD = sys.argv[1], sys.argv[2]
sys.path.insert(0, TREE)
os.environ['RL_REPO'] = TREE
import fv_provenance as F
import config_manifest as CM


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


BOARD_MD5 = md5(BOARD)
STORE = 'd9a24282357cf3083b1640466e3ecd83'
assert md5(TREE + '/engine/rl_after/rl_model_data.json') == STORE, "the store moved -- HALT"

fvdir = os.path.join(TREE, 'engine', 'forward_valuation')
FVID = F.fv_identity(fvdir)
CFG = CM.canonical_hash(CM.load(TREE)['vars'])
RLM = md5(TREE + '/engine/rl_after/rl_model.py')
EHD = md5(TREE + '/engine/rl_after/_merged_recover.py')
print("landed identities: board %s · config %s · rl_model %s · engine_head %s · fv %s"
      % (BOARD_MD5[:8], CFG[:8], RLM[:8], EHD[:8], FVID[:8]))

# ---- 1. the board, both tracked copies ---------------------------------------------------------
for rel in ('data/rl_build/rl_app_data.json', 'engine/rl_after/rl_app_data.json'):
    p = os.path.join(TREE, rel)
    old = md5(p)
    shutil.copyfile(BOARD, p)
    assert md5(p) == BOARD_MD5
    print("board  %-40s %s -> %s" % (rel, old, md5(p)))

# ---- 2. the working board's srcmd5 sidecar -----------------------------------------------------
sp = os.path.join(TREE, 'engine/rl_after/rl_app_data.json.srcmd5')
s = json.load(open(sp))
assert s['source_md5'] == STORE, "srcmd5 names a moved store -- HALT"
print("srcmd5 own_md5             : %s -> %s" % (s['own_md5'], BOARD_MD5))
s['own_md5'] = BOARD_MD5
open(sp, 'w').write(json.dumps(s) + "\n")

# ---- 3. the provenance sidecar -----------------------------------------------------------------
pp = os.path.join(TREE, 'engine/rl_after/rl_app_data.provenance.json')
pv = json.load(open(pp))
for k, v in (('config_manifest_identity', CFG), ('rl_model_md5', RLM)):
    if pv.get(k) != v:
        print("provenance %-24s %s -> %s" % (k, str(pv.get(k))[:16], str(v)[:16]))
        pv[k] = v
assert pv['fv_identity'] == FVID, "fv identity moved but no forward_valuation source was touched -- HALT"
open(pp, 'w').write(json.dumps(pv, indent=2, sort_keys=True) + "\n")

# ---- 4. the pins -------------------------------------------------------------------------------
bp = os.path.join(TREE, 'data/expected_boot.json')
before = json.load(open(bp))
after = dict(before)
after['board'] = BOARD_MD5
after['config'] = CFG
after['engine_head'] = EHD
after['rl_model'] = RLM

moved = [k for k in sorted(set(before) | set(after)) if not k.startswith('_') and before.get(k) != after.get(k)]
print("\nexpected_boot.json -- every key, moved or not:")
for k in sorted(set(before) | set(after)):
    if k.startswith('_'):
        continue
    b, a = before.get(k), after.get(k)
    if b != a:
        print("  MOVED   %-20s %s -> %s" % (k, str(b)[:44], str(a)[:44]))
    else:
        print("  unmoved %-20s %s" % (k, str(b)[:64]))
print("\nkeys moved: %s" % moved)
assert moved == ['board', 'engine_head'], \
    "*** BREACH: the moved pin set is %s, not the pre-registered {board, engine_head} ***" % moved
assert after['fv'] == FVID == before['fv'], "*** BREACH: fv moved ***"
assert after['store'] == STORE, "*** BREACH: store pin moved ***"
open(bp, 'w').write(json.dumps(after, indent=1) + "\n")
assert after['config'] == before['config'], "*** BREACH: config moved -- ORDER 25 touches no manifest var ***"
assert after['rl_model'] == before['rl_model'], "*** BREACH: rl_model moved -- ORDER 25 has no code change ***"
print("PIN CHANGE IS EXACTLY {board, engine_head} -- as pre-registered (D5).")
print("store %s and fv %s asserted UNMOVED before writing." % (STORE[:8], FVID[:8]))
