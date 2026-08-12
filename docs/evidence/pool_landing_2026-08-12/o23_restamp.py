#!/usr/bin/env python3
"""ORDER 23 -- INSTALL THE LANDED BOARD AND RESTAMP EVERY IDENTITY CARRIER THAT MOVES.

  usage: o23_restamp.py <tree> <board.json>

Follows the ORDER 20C landing (and through it the ORDER 9 bake precedent 7f4d5d2 / 56665de): the
board lands at data/rl_build/rl_app_data.json AND engine/rl_after/rl_app_data.json; the srcmd5 and
provenance sidecars are rewritten; data/expected_boot.json gets the pins that moved and nothing else.

THE MOVED SET IS ASSERTED BEFORE ANYTHING IS WRITTEN TO THE PIN FILE, and every key is printed moved
or not, so "only these four moved" is a check rather than a claim:

    board        the pool update moves 117 board rows
    config       H_POOLSIT / H_UNION retired to 1.0 in the manifest
    engine_head  _merged_recover.py: the derived retention surface wired + the H defaults retired
    rl_model     rl_model.py: the ND65+ cap amendment

    fv           MUST NOT MOVE -- no engine/forward_valuation source is touched by this act
    store, band, q97m, v0surf, peak_model, pvc_snapshot, bust_prior, register  MUST NOT MOVE
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
assert moved == ['board', 'config', 'engine_head', 'rl_model'], \
    "*** BREACH: the moved pin set is %s, not the pre-registered {board, config, engine_head, rl_model} ***" % moved
assert after['fv'] == FVID == before['fv'], "*** BREACH: fv moved ***"
assert after['store'] == STORE, "*** BREACH: store pin moved ***"
open(bp, 'w').write(json.dumps(after, indent=1) + "\n")
print("PIN CHANGE IS EXACTLY {board, config, engine_head, rl_model} -- as pre-registered (P1).")
print("store %s and fv %s asserted UNMOVED before writing." % (STORE[:8], FVID[:8]))
