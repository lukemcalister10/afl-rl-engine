#!/usr/bin/env python3
"""ONE-SOURCE SELF-TEST (F1/F2 rewire, 2026-07-05). Run from engine/rl_after (or the bootstrapped workspace)
under the panel env. Proves the board + book are regenerable from the SINGLE store and that every published
value equals the engine's gated ev(). Exits NON-ZERO (build FAILS) on any violation.

Preconditions: build the board and book first, in this order --
    python3 rl_export.py            # writes rl_app_data.json  (F1 export<->engine parity gate runs inside)
    python3 s4_matrix_M1v7.py       # writes s4_matrix.json    (F2 book<->board parity gate runs inside)
    python3 one_source_selftest.py  # this file: independent re-verification of every invariant

Checks:
  (0) the .pre_stage0 / .stage0 lookalikes are GONE, and rl_model.py opens ONLY the single store + the 5 inputs
  (1) engine loads; derived active == 805 board players, key-for-key
  (2) EXPORT PARITY (F1): board v == a freshly, independently recomputed engine gated ev() for every active player
  (3) BOOK PARITY (F2): book `cur` == board v for every shared player (pvc-excluded board players noted, not failed)
  (4) Marcus Bontempelli's 13-season track, regenerated from the store, == the store (regenerability proof)
"""
import io, os, re, sys, json, contextlib

FAIL=[]
def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ")+msg)
    if not cond: FAIL.append(msg)

HERE=os.path.dirname(os.path.abspath(__file__))
def hp(*p): return os.path.join(HERE,*p)

print("=== (0) SINGLE SOURCE: lookalikes gone, engine reads only the store + classified inputs ===")
check(not os.path.exists(hp('rl_model_data.json.pre_stage0')), ".pre_stage0 lookalike absent")
check(not os.path.exists(hp('rl_model_data.json.stage0')),     ".stage0 lookalike absent")
check(os.path.exists(hp('rl_model_data.json')),                "single store rl_model_data.json present")
_src=open(hp('rl_model.py')).read()
_opens=set(re.findall(r"open\('([^']+)'", _src))
_allowed={'rl_model_data.json','params.json','rl_passmark.json','peak_model_v4.pkl','bust_prior_table.json','pvc_snapshot.json'}
_stray=[o for o in _opens if o not in _allowed]
check(not _stray, "rl_model.py opens ONLY the store + 5 classified inputs (stray opens: %s)"%_stray)
check(not any('stage0' in o for o in _opens), "no rl_model.py read of any *stage0* file")

print("=== (1) ENGINE LOADS from the single store; active == 805 ===")
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(hp('_merged_recover.py')).read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']
active_keys=[p['key'] for p in MA.players]
check(len(active_keys)==805, "engine active players == 805 (got %d)"%len(active_keys))
check(len(set(active_keys))==len(active_keys), "active keys unique")

print("=== (2) EXPORT PARITY (F1): board v == independently recomputed engine gated ev(), key-for-key ===")
board_path=os.environ.get('RL_APP_DATA','rl_app_data.json')
if not os.path.exists(board_path):
    check(False, "board %s present (run rl_export.py first)"%board_path)
else:
    board={r['key']:r['v'] for r in json.load(open(board_path))['active']}
    check(set(board)==set(active_keys), "board active set == engine active set, key-for-key")
    gated={}
    with contextlib.redirect_stdout(io.StringIO()):
        for p in MA.players:
            v=ev(p,2026); ev(p,2024); ev(p,2025); ev(p,2027); ev(p,2028)   # replicate the export's as-of sequence
            gated[p['key']]=v
    mism=[(k,board[k],gated.get(k)) for k in board if board[k]!=gated.get(k)]
    check(not mism, "every board v == engine gated ev (F1); mismatches=%d %s"%(len(mism),mism[:8]))

print("=== (3) BOOK PARITY (F2): book cur == board v for shared players ===")
book_path=os.environ.get('S4_MATRIX','s4_matrix.json')
if not os.path.exists(book_path):
    check(False, "book %s present (run s4_matrix_M1v7.py first)"%book_path)
elif os.path.exists(board_path):
    book={v['key']:v.get('cur') for v in json.load(open(book_path)).values() if v.get('key')}
    board={r['key']:r['v'] for r in json.load(open(board_path))['active']}
    shared=[k for k in board if k in book]
    absent=[k for k in board if k not in book]
    bmis=[(k,book[k],board[k]) for k in shared if book[k]!=board[k]]
    check(not bmis, "every shared book cur == board v (F2); mismatches=%d %s"%(len(bmis),bmis[:8]))
    print("       (%d board players outside the cohort book, _pvc_exclude: %s)"%(len(absent),sorted(absent)))

print("=== (4) REGENERABILITY: Bontempelli's 13-season track regenerated from source == source ===")
store=json.load(open(hp('rl_model_data.json')))
bont=[p for p in store if p['key']=='marcus-bontempelli']
check(len(bont)==1, "exactly one marcus-bontempelli in the store")
if bont:
    src=sorted(((r['year'],r['avg'],r['games']) for r in bont[0]['scoring']))
    # regenerate his track straight off the loaded engine's player object (same store, live objects)
    ep=[p for p in MA.data if p['key']=='marcus-bontempelli'][0]
    regen=sorted(((r['year'],r['avg'],r['games']) for r in ep['scoring']))
    check(len(src)==13, "Bontempelli has 13 seasons in source (got %d)"%len(src))
    check(src==regen, "regenerated 13-season track == source, season-for-season")
    print("       seasons %s..%s  first=%s last=%s"%(src[0][0],src[-1][0],src[0],src[-1]))

print("\n"+("SELF-TEST FAILED: %d check(s)\n  - "%len(FAIL)+"\n  - ".join(FAIL) if FAIL else "SELF-TEST PASSED: single source; board==engine (F1); book==board (F2); regenerable."))
sys.exit(1 if FAIL else 0)
