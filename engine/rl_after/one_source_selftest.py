#!/usr/bin/env python3
"""ONE-SOURCE SELF-TEST (DPP-strip final consolidation, 2026-07-05). Run from engine/rl_after (or the
bootstrapped workspace) under the panel env. Proves the board + book are regenerable from the SINGLE store,
that every published value equals the engine's gated ev(), and that the FOUR single-source guards hold.
Exits NON-ZERO (build FAILS) on any violation -- never warns.

Preconditions: build the board and book first, in this order --
    python3 rl_export.py            # writes rl_app_data.json (+ stamps read-only) ; F1 export<->engine gate
    python3 s4_matrix_M1v7.py       # writes s4_matrix.json  (+ stamps read-only) ; F2 book<->board gate
    python3 one_source_selftest.py  # this file: guards 1-3 + F1/F2 + data ground-truth + regenerability
    python3 guard_correction_canary.py   # GUARD 4 (full-rebuild correction-sticks canary), run separately

Checks:
  GUARD 3  single source: exactly one rl_model_data*.json, no lookalikes; engine opens only classified inputs
  GUARD 1  derived read-only + stamped: board + book are 0o444 and carry a .srcmd5 stamp
  GUARD 2  source-hash: each derived stamp == current source md5
  (1) engine loads from the single store; derived active == 804 (was 805; taylor-adams retired 2026-07-12), keys unique
  (2) EXPORT PARITY (F1): board v == a freshly, independently recomputed engine gated ev(), key-for-key
  (3) BOOK PARITY  (F2): book cur == board v for every shared player
  (4) DATA GROUND TRUTH: Kako 2025 23@55.2 / 2026 6@55.0 ; Bontempelli 13-season track regenerated == source
  (5) POSITION MODEL: store carries drafted/present/future single-valued columns; raw_multipos GONE
"""
import io, os, re, sys, json, stat, contextlib
import single_source as SS

FAIL=[]
def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ")+msg)
    if not cond: FAIL.append(msg)

HERE=os.path.dirname(os.path.abspath(__file__))
def hp(*p): return os.path.join(HERE,*p)

# L7 NUMÉRAIRE (baked 2026-07-13): the board DISPLAYS every player value as round(ev/F) (ev()/engine
# UNCHANGED — display-only re-base). So the F1/F2 single-source parity invariants hold in the numéraire:
# board v == round(engine ev / F) and board v == round(book cur / F). F is the certified 1.0524.
_F = json.load(open(hp('pick_redenomination.json')))['factor'] if os.path.exists(hp('pick_redenomination.json')) else 1.0524
def _num(x): return int(round(x / _F))

print("=== GUARD 5: BOOT-STORE (this dir's store == the checked-out, pinned store) ===")
# The four guards above validate whichever dir this file is imported from (HERE) against ITSELF — so a
# stale-but-self-consistent workspace passes them. GUARD 5 anchors on the CHECKOUT: it asserts HERE's store
# and engine head equal data/expected_boot.json in the repo. Fails the self-test (build) on a stale boot.
_repo=None
for _c in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
           os.path.abspath(os.path.join(HERE,'..','..'))):
    if _c and os.path.exists(os.path.join(_c,'boot_guard.py')): _repo=_c; break
if _repo:
    if _repo not in sys.path: sys.path.insert(0,_repo)
    import boot_guard as _BG
    try:
        _BG.assert_boot('one_source_selftest', store_path=hp('rl_model_data.json'),
                        engine_head_path=hp('_merged_recover.py'),
                        register_path=(hp('LTI_REGISTER.md') if os.path.exists(hp('LTI_REGISTER.md')) else None),
                        halt=False)
        check(True, "GUARD 5: boot-store — this dir's store+head == pinned checkout store")
    except AssertionError as _e:
        _det=[l.strip() for l in str(_e).splitlines() if l.strip() and set(l.strip())!={'='} and 'HALTED' not in l]
        check(False, "GUARD 5: boot-store FAILED — %s"%(' '.join(_det) if _det else "boot-store mismatch"))
else:
    check(False, "GUARD 5: cannot locate the checkout (set RL_REPO/CLAUDE_PROJECT_DIR) to verify the boot store")

print("=== GUARD 3: SINGLE SOURCE (lookalike tripwire + engine opens) ===")
_g3=[]
SS.assert_single_source(lambda c,m: _g3.append(m) if not c else None)
SS.assert_engine_opens(lambda c,m: _g3.append(m) if not c else None)
for m in _g3: check(False, m)
check(not _g3, "exactly one rl_model_data*.json, no lookalikes, engine opens only classified inputs")

print("=== GUARD 1 + GUARD 2: derived files read-only + source-md5-stamped + content-intact ===")
_sm=SS.source_md5()
for _name in SS.TIER1_DERIVED:
    _p=hp(_name)
    if not os.path.exists(_p): check(False, "%s present (build it first)"%_name); continue
    _mode=stat.S_IMODE(os.stat(_p).st_mode)
    check(not (_mode & stat.S_IWUSR), "GUARD 1: %s is read-only (mode %o)"%(_name,_mode))
    check(os.path.exists(SS._stamp_path(_p)), "GUARD 1: %s carries a .srcmd5 stamp"%_name)
    check(SS._md5(_p)==SS.read_own_stamp(_name), "GUARD 1: %s content md5 == stamped own_md5 (not hand-edited)"%_name)
    check(SS.read_stamp(_name)==_sm, "GUARD 2: %s stamp == current source md5 %s"%(_name,_sm[:8]))
print("       source md5 = %s"%_sm)

print("=== (1) ENGINE LOADS from the single store; active == 804 ===")
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(hp('_merged_recover.py')).read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']
active_keys=[p['key'] for p in MA.players]
# 805 -> 804 at the ID-primary migration (owner-ruled 2026-07-12): taylor-adams marked _retired
# (mid-season retirement) drops him from the live/active board. Count re-pinned like the panel/board seal.
check(len(active_keys)==804, "engine active players == 804 (got %d)"%len(active_keys))
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
    mism=[(k,board[k],gated.get(k)) for k in board if board[k]!=_num(gated.get(k))]
    check(not mism, "every board v == round(engine gated ev / %.4f) — numéraire display (F1); mismatches=%d %s"%(_F,len(mism),mism[:8]))

print("=== (3) BOOK PARITY (F2): book cur == board v for shared players ===")
book_path=os.environ.get('S4_MATRIX','s4_matrix.json')
if not os.path.exists(book_path):
    check(False, "book %s present (run s4_matrix_M1v7.py first)"%book_path)
elif os.path.exists(board_path):
    book={v['key']:v.get('cur') for v in json.load(open(book_path)).values() if v.get('key')}
    board={r['key']:r['v'] for r in json.load(open(board_path))['active']}
    shared=[k for k in board if k in book]
    absent=[k for k in board if k not in book]
    bmis=[(k,book[k],board[k]) for k in shared if board[k]!=_num(book[k])]
    check(not bmis, "every shared board v == round(book cur / %.4f) — numéraire display (F2); mismatches=%d %s"%(_F,len(bmis),bmis[:8]))
    print("       (%d board players outside the cohort book, _pvc_exclude: %s)"%(len(absent),sorted(absent)))

print("=== (4) DATA GROUND TRUTH: Kako + Bontempelli regenerated from source ===")
store=json.load(open(hp('rl_model_data.json')))
kako=[p for p in store if p['key']=='isaac-kako']
check(len(kako)==1, "exactly one isaac-kako in the store")
if kako:
    ksc={r['year']:(r['games'],r['avg']) for r in kako[0]['scoring']}
    check(ksc.get(2025)==(23,55.2), "Kako 2025 == 23 games @ 55.2 (owner ground truth); got %s"%(ksc.get(2025),))
    check(ksc.get(2026)==(6,55.0),  "Kako 2026 == 6 games @ 55.0; got %s"%(ksc.get(2026),))
bont=[p for p in store if p['key']=='marcus-bontempelli']
check(len(bont)==1, "exactly one marcus-bontempelli in the store")
if bont:
    src=sorted(((r['year'],r['avg'],r['games']) for r in bont[0]['scoring']))
    ep=[p for p in MA.data if p['key']=='marcus-bontempelli'][0]
    regen=sorted(((r['year'],r['avg'],r['games']) for r in ep['scoring']))
    check(len(src)==13, "Bontempelli has 13 seasons in source (got %d)"%len(src))
    check(src==regen, "regenerated 13-season track == source, season-for-season")
    print("       Bontempelli seasons %s..%s  first=%s last=%s"%(src[0][0],src[-1][0],src[0],src[-1]))

print("=== (5) POSITION MODEL: three single-valued columns; DPP blend GONE ===")
_keys=set(); [_keys.update(p.keys()) for p in store]
check('drafted_position' in _keys and 'present_position' in _keys and 'future_position' in _keys,
      "store carries drafted_position + present_position + future_position")
check('raw_multipos' not in _keys, "raw_multipos (the DPP blend) is GONE from the store")
_multi=[p['key'] for p in store if isinstance(p.get('present_position'),list) or isinstance(p.get('future_position'),list)]
check(not _multi, "present/future positions are single-valued (no list legs); offenders=%s"%_multi[:5])
# in THIS build future == present for every record (the seam resolves identically now)
_seam=[p['key'] for p in store if p.get('future_position')!=p.get('present_position')]
check(not _seam, "future_position == present_position for every record this build; offenders=%s"%_seam[:5])

print("=== COLLISION SENTRY: named-pair identity assertions (halt-not-warn; DECISIONS §29) ===")
# Permanent, data-driven from collision_sentry.json (extensible; pairs ADDED ONLY WHEN THEY BITE). For every
# pinned pair: both keys exist EXACTLY ONCE, every pinned field == the store's value (a bleed makes
# e.g. max-king-stk._by=2007 != pinned 2000 -> FAIL), and the `distinct_fields` still DIFFER between the two
# members (defence-in-depth vs a symmetric swap). Any merge/swap/bleed FAILS the build (FAIL -> sys.exit(1)).
_by_key={}
for _p in store: _by_key.setdefault(_p.get('key'),[]).append(_p)
_sentry_path=hp('collision_sentry.json')
if not os.path.exists(_sentry_path):
    check(False, "collision_sentry.json present (the named-pair identity sentry file)")
else:
    _sentry=json.load(open(_sentry_path))
    _pairs=_sentry.get('pairs',[])
    check(len(_pairs)>=1, "collision sentry carries >=1 named pair (got %d)"%len(_pairs))
    for _pr in _pairs:
        _members={'a':_pr['a'],'b':_pr['b']}
        for _side,_pin in _members.items():
            _k=_pin['key']; _rows=_by_key.get(_k,[])
            check(len(_rows)==1, "collision sentry: %s exists EXACTLY ONCE in the store (found %d)"%(_k,len(_rows)))
            if len(_rows)==1:
                _r=_rows[0]
                for _f,_want in _pin.items():
                    check(_r.get(_f)==_want,
                          "collision sentry: %s.%s == %r (pinned) — got %r%s"%(_k,_f,_want,_r.get(_f),
                          "  <-- IDENTITY BLEED/MERGE" if _r.get(_f)!=_want else ""))
        # defence-in-depth: the two members must still DIFFER on every distinct_field (no cross-copy/swap)
        _ra=_by_key.get(_pr['a']['key'],[None])[0]; _rb=_by_key.get(_pr['b']['key'],[None])[0]
        if _ra and _rb:
            for _f in _pr.get('distinct_fields',[]):
                check(_ra.get(_f)!=_rb.get(_f),
                      "collision sentry: %s.%s (%r) != %s.%s (%r) — must stay distinct (no cross-copy)"%(
                      _pr['a']['key'],_f,_ra.get(_f),_pr['b']['key'],_f,_rb.get(_f)))

print("\n"+("SELF-TEST FAILED: %d check(s)\n  - "%len(FAIL)+"\n  - ".join(FAIL) if FAIL else
      "SELF-TEST PASSED: single source; guards 1-3; board==engine (F1); book==board (F2); Kako+Bontempelli ground-truth; DPP blend stripped; collision sentry (King pair) clean."))
print("  (GUARD 4 — correction-sticks canary — runs separately: python3 guard_correction_canary.py)")
sys.exit(1 if FAIL else 0)
