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
  (4) DATA GROUND TRUTH: Kako 2025 23@55.2 / 2026 10@45.4 ; Bontempelli 13-season track regenerated == source
  (5) POSITION MODEL: store carries drafted/present/future single-valued columns; raw_multipos GONE
"""
import io, os, re, sys, json, stat, contextlib, hashlib
import single_source as SS

FAIL=[]
def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ")+msg)
    if not cond: FAIL.append(msg)

def stale(msg):
    """An owner anchor whose round window has been outrun.

    This is a FAILURE — an anchor that quietly stops checking once its scope lapses is a guard that has
    switched itself off, which is the defect class this file is full of. But it is reported as STALE
    rather than as a value mismatch, because the number was never wrong: it described the rounds it was
    typed for, and the store moved past them. The fix is an owner re-anchor, not a re-typed literal, and
    the message has to say so or the next seat "corrects" it and restarts the same clock."""
    print("  STALE "+msg)
    FAIL.append("STALE: "+msg)

HERE=os.path.dirname(os.path.abspath(__file__))
def hp(*p): return os.path.join(HERE,*p)

# ---- DECLARED CHECK HOLDS (#271 stage B) -----------------------------------------------------------
# A hold on a CHECK FAMILY (not on a bound release identity) lives in release_contract.json's `held_checks`.
# It is sealed by contract_sha256 and invisible to held_candidates' identity schema, so the contract gate and
# this self-test both accept it. Reading it here, once, keeps the two consumers on one record.
def _held_check(family):
    for _c in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
               os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))):
        if not _c: continue
        _p=os.path.join(_c,'data','release_contract.json')
        if not os.path.exists(_p): continue
        try:
            for _h in (json.load(open(_p)).get('held_checks') or []):
                if _h.get('check_family')==family: return _h
        except Exception: return None
        return None
    return None

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
# ---- OWNER GROUND-TRUTH ANCHORS, ROUND-SCOPED ---------------------------------------------------
# An anchor is a figure the OWNER states, checked against the store. It is deliberately hand-typed and
# must NEVER be derived from the store — an anchor that read its own expectation from the thing it
# checks would pass on any corruption, which is the whole reason it exists.
#
# But a CURRENT-SEASON anchor is only true for the rounds it was measured over, and this one proved it:
# `2026 == (10, 45.4)` was typed when R19 was the latest round. R20 was applied, Kako scored 32, and
# nothing re-typed it — 454 + 32 = 486, / 11 = 44.18, exactly what the store now holds. The figure was
# never wrong. Re-typing it would just wind the same clock up again and it would break at R21.
#
# So each anchor carries the round window it describes, the shape #208 gave the Bailey Williams override
# (`applies_to_rounds`). Where this deliberately DIFFERS from that precedent: an out-of-scope override
# simply does not apply and the general path handles the row, so nothing is lost. An out-of-scope anchor
# leaves NOTHING checking the store. So lapsing is not a quiet no-op here — it is announced as STALE and
# it fails, and the only thing that clears it is an owner re-anchor.
# (If the owner ever wants lapsed anchors to warn instead of fail, `stale()` is the single place to change.)
KAKO_ANCHORS = [
    # year, (games, avg), last round the figure covers (None == completed season, cannot move), provenance
    (2025, (23, 55.2), None,
     "completed season — no round scope; it is final and cannot go stale"),
    # The 2026 current-season anchor is RETIRED by owner word 2026-08-06, given at R21: "Kako is now
    # correct - 12 at 42.75. Retire the anchor." The R20 anchor (11, 44.18, thru=20) lapsed loudly at
    # the R21 apply exactly as designed; the owner confirmed the store's R21 reading (12 games @ 42.75)
    # as correct and retired the anchor rather than re-winding a clock that breaks every round. The
    # scope mechanism stays for any future anchor. Recorded once so no reviewer re-flags the absence.
]

def _as_of_round():
    """The round the CHECKOUT is at, read from data/expected_boot.json.

    Deliberately the release manifest and not the store: the store is what the anchors check, so taking
    the scope from it would let a store that had silently advanced also silently widen the window that
    is supposed to catch it."""
    if not _repo:
        return None
    try:
        return json.load(open(os.path.join(_repo, 'data', 'expected_boot.json'))).get('as_of_round')
    except Exception:
        return None

if kako:
    ksc={r['year']:(r['games'],r['avg']) for r in kako[0]['scoring']}
    _round=_as_of_round()
    # No round -> no scope decision can be made, and passing anyway would be the silent-guard failure
    # this block exists to prevent. Fail closed and say which input is missing.
    check(_round is not None,
          "as_of_round readable from data/expected_boot.json (owner anchors are scoped by it)")
    for _yr, _want, _thru, _prov in KAKO_ANCHORS:
        _got=ksc.get(_yr)
        if _thru is not None and _round is not None and _round > _thru:
            stale("Kako %d anchor covers rounds through R%d, the store is at R%d — the anchor is out of "
                  "date, not wrong. Owner re-anchor required. anchor=%s store=%s (%s)"
                  %(_yr, _thru, _round, _want, _got, _prov))
        else:
            check(_got==_want,
                  "Kako %d == %d games @ %s (owner ground truth%s); got %s"
                  %(_yr, _want[0], _want[1],
                    '' if _thru is None else ', covers rounds through R%d'%_thru, _got))
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
# LEG C FLEX-ERA INVARIANTS (item 271; REPLACES the obsolete `future==present for every record` seam check —
# that assertion held ONLY for the DPP-strip build; the flex build populates future_position (the 11) and the
# dual streams (the 90), so the seam is EXPECTED to differ). The new guard asserts the FLEX SCHEMA: (a) every
# future_position is in the position vocab; (b) at most ONE alternate per row (single-valued, never a list —
# the "<=1 alternate" law); (c) blend params register-consistent (alternate in vocab, 0<p_dual<=100,
# alternate != primary; alt/p_dual set together). GUARD CHANGE, named for the cold audit. SILENCE IS A RED.
_VOCAB=set(MA.GRP)   # the engine's OWN position vocab (incl. the 'SD'->SD legacy alias on back-catalogue rows)
_futbad=[p['key'] for p in store if p.get('future_position') and p.get('future_position') not in _VOCAB]
check(not _futbad, "flex: every future_position in vocab; offenders=%s"%_futbad[:5])
_altlist=[p['key'] for p in store if isinstance(p.get('alternate_position'),list)]
check(not _altlist, "flex: at most ONE alternate per row (single-valued, never a list); offenders=%s"%_altlist[:5])
_dualbad=[]
for p in store:
    ap=p.get('alternate_position'); pd=p.get('p_dual_stream')
    if ap is None and pd is None: continue
    if (ap is None)!=(pd is None): _dualbad.append((p['key'],'alt/p_dual half-set'))
    elif ap not in _VOCAB: _dualbad.append((p['key'],'alt not in vocab'))
    elif not (0.0<float(pd)<=100.0): _dualbad.append((p['key'],'p_dual out of (0,100]'))
    elif ap==p.get('future_position'): _dualbad.append((p['key'],'alt==primary'))
check(not _dualbad, "flex: blend params register-consistent (alt in vocab, 0<p_dual<=100, alt!=primary); offenders=%s"%_dualbad[:5])

print("=== (6) LEG A — iso_corr EVIDENCE-FADE + ISO MONOTONIZATION (item 132; RL_ISOFADE) ===")
# The fade dissolves the pick tax on the v2.10 evidence weight w=E_q; the ISO multiplier is monotonized
# non-increasing in pick. Asserted here so a regression in either HALTs the build (SILENCE IS A RED).
_iso_eff=g['iso_eff']; _iso_corr=g['iso_corr']; _ISO=g['ISO']; _evq=g['_ev_qual']
_isreal=g['_isreal']; _cp=g['cp']; _ISOFADE=g['_ISOFADE']
_reals=[p for p in MA.players if _isreal(p)]
with contextlib.redirect_stdout(io.StringIO()):
    # (a) ZERO-EVIDENCE (the V0 leg): at Y=debutyr-1, E_q==0 => fade==1 => iso_eff == iso_corr, unchanged BY CONSTRUCTION
    _ze_ok=True; _ze_ex='ok'
    for _p in _reals[:80]:
        _y0=_cp.debutyr(_p)-1
        if _evq(_p,_y0)!=0.0: _ze_ok=False; _ze_ex=(_p['key'],'E_q!=0 at debutyr-1'); break
        if _iso_eff(_p,_y0)!=_iso_corr(MA.gfut(_p),MA.effpk(_p)): _ze_ok=False; _ze_ex=(_p['key'],'iso_eff!=iso_corr at w=0'); break
    # (b) SATURATED-EVIDENCE: the most-proven real player's iso has dissolved to ~1.0
    _sat=max(_reals, key=lambda p:_evq(p,2026)); _satEq=float(_evq(_sat,2026)); _satiso=float(_iso_eff(_sat,2026))
check(_ze_ok, "LEG A fade: zero-evidence (Y=debutyr-1, E_q==0) => iso_eff == iso_corr, unchanged (sample 80; %s)"%(_ze_ex,))
if _ISOFADE:
    check(_satEq>5.0 and abs(_satiso-1.0)<0.02,
          "LEG A fade: saturated player %s (E_q=%.1f) iso_eff=%.4f ~= 1.0 (|d|<0.02)"%(_sat['key'],_satEq,_satiso))
    _mono_bad=[]
    for _pos,(xs,fs) in _ISO.items():
        for _i in range(len(fs)-1):
            if float(fs[_i]) < float(fs[_i+1])-1e-9: _mono_bad.append((_pos,int(xs[_i]),round(float(fs[_i]),4),round(float(fs[_i+1]),4))); break
    check(not _mono_bad, "LEG A monotone: ISO[pos] multiplier non-increasing in pick, every position (violations=%s)"%(_mono_bad[:4]))
else:
    print("  NOTE  RL_ISOFADE=0 (v2.10 base path): fade/monotone assertions skipped; the zero-evidence identity above holds either way.")

print("=== (7) LEG B — L-RECENCY invariant (R105.5) + ρ FORBIDDEN-LIST (R105.4); halt-not-warn ===")
# TWO owner-ruled guards on the un-compress ρ axis, suite-wired so a future decay/kernel change or a
# re-introduced season gate HALTs the build (SILENCE IS A RED). Both hold whether RL_UNCOMP is on or off:
# they inspect the ρ kernel + the rho_out source, not the live board (the map is inert until s is set).
_rho_out = g['rho_out']; _d = float(MA.UNCOMP_DECAY)
# ---- R105.5 L-RECENCY (register 241, owner verbatim): an individual match's influence must count for EQUAL
# OR MORE than a match from an earlier season => the PER-GAME recency weight is NON-INCREASING in years-back
# across the store's full observed season range. memo v1.3 conforms by construction (per-game weight =
# d^yearsback, d=UNCOMP_DECAY=0.25); this guard LOCKS it against silent inversion. The binding probe drives
# the SHIPPED rho_out with a two-season synthetic and RECOVERS the engine's own per-game weight, so a future
# edit to the kernel INSIDE rho_out (not just the declared formula) is caught.
_bs = sorted({2026 - x['year'] for p in store for x in (p.get('scoring') or []) if (x.get('games',0) or 0) > 0})
check(0.0 < _d <= 1.0, "L-RECENCY: decay d in (0,1] (d=%.4f) — a non-inflating recency kernel (R105.6 owner-set 0.25)"%_d)
check(len(_bs) >= 2, "L-RECENCY: store spans >=2 distinct years-back (range %d..%d) to test monotonicity"%(_bs[0],_bs[-1]))
# declared-kernel monotonicity (fast, explicit)
_wpg = [_d**_b for _b in _bs]
check(all(_wpg[i] >= _wpg[i+1]-1e-15 for i in range(len(_wpg)-1)),
      "L-RECENCY: declared kernel d^yearsback non-increasing over the store range yearsback=%d..%d"%(_bs[0],_bs[-1]))
# engine-recovered kernel: rho_out of a 2-season synthetic (ref @ yb=0, probe @ yb=b) => w_b = (r-A)/(B-r) == d^b
_pos = sorted(MA.REPL)[0]; _repl = MA.REPL[_pos]; _A, _B = 10.0, 20.0
_rec = []; _probe_ok = True
for _b in [b for b in _bs if b >= 1]:
    _synth = {'scoring':[{'year':2026,'games':1,'avg':_repl+_A},{'year':2026-_b,'games':1,'avg':_repl+_B}]}
    _r = _rho_out(_synth, _pos)
    if _r is None or not (_A < _r < _B): _probe_ok = False; break
    _rec.append((_b, (_r-_A)/(_B-_r)))
check(_probe_ok and len(_rec)>=1, "L-RECENCY: engine rho_out evaluates the 2-season synthetic across the store range")
if _probe_ok and _rec:
    check(all(w > 0.0 for _,w in _rec), "L-RECENCY: engine per-game weight POSITIVE for every played years-back (no season wiped)")
    check(all(_rec[i][1] >= _rec[i+1][1]-1e-12 for i in range(len(_rec)-1)),
          "L-RECENCY: engine rho_out per-game weight NON-INCREASING in years-back (recovered kernel; R105.5)")
    check(all(abs(w - _d**b) <= 1e-9 + 1e-6*(_d**b) for b,w in _rec),
          "L-RECENCY: recovered engine weight == d^yearsback exactly (games-independent per-game weight, no inversion)")
# ---- R105.4 FORBIDDEN-LIST (register 240, owner-ruled WEIGHT-DON'T-GATE): rho_out carries NO season-level
# exclusion, NO games floor, NO career-phase test — the ONLY season filter is games>0. Assert the SHIPPED
# rho_out source (AST; docstring stripped so the descriptive "NO exclusion/floor/phase" comments do not
# false-trip) so a future edit re-introducing a floor/exclusion/phase gate HALTs the build.
import ast as _ast
_eng_ast = _ast.parse(open(hp('_merged_recover.py')).read())
_rho_fn = next((n for n in _ast.walk(_eng_ast) if isinstance(n,_ast.FunctionDef) and n.name=='rho_out'), None)
check(_rho_fn is not None, "R105.4: rho_out present in the engine source (the wired ρ law)")
if _rho_fn is not None:
    _fb = _rho_fn.body
    if _fb and isinstance(_fb[0],_ast.Expr) and isinstance(getattr(_fb[0],'value',None),_ast.Constant) and isinstance(_fb[0].value.value,str):
        _fb = _fb[1:]                                             # strip the docstring (comments are not in the AST)
    _mod = _ast.Module(body=list(_fb), type_ignores=[])
    # (a) games is compared ONLY to 0 (the games>0 / games<=0 filter) — any other numeric threshold is a floor
    _bad_floor = []
    for _n in _ast.walk(_mod):
        if isinstance(_n,_ast.Compare):
            _dump = _ast.dump(_n)
            if 'games' in _dump or "'_gm'" in _dump or 'id=\'_gm\'' in _dump or '_gm' in _dump:
                for _c in _ast.walk(_n):
                    if isinstance(_c,_ast.Constant) and isinstance(_c.value,(int,float)) and _c.value not in (0, 0.0):
                        _bad_floor.append((_ast.dump(_n), _c.value))
    check(not _bad_floor, "R105.4: rho_out compares games only to 0 (games>0 filter) — NO games floor (offenders=%s)"%(_bad_floor[:2]))
    # (b) no exclusion / floor / phase / classify / qualify token in EXECUTABLE code (docstring already stripped)
    _forb = ('qualif','floor','exclud','exclus','phase','classif','interrupt','delist')
    _idents = set(); _strs = []
    for _n in _ast.walk(_mod):
        if isinstance(_n,_ast.Name): _idents.add(_n.id.lower())
        if isinstance(_n,_ast.Attribute): _idents.add(_n.attr.lower())
        if isinstance(_n,_ast.Constant) and isinstance(_n.value,str): _strs.append(_n.value.lower())
    _hit = sorted({t for t in _forb if any(t in i for i in _idents) or any(t in s for s in _strs)})
    check(not _hit, "R105.4: rho_out executable code carries no exclusion/floor/phase/classify/qualify token (offenders=%s)"%_hit)

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

print("=== (8) item-284 — DPP DATA-ERROR classes: fixture proofs + store flag-and-name (report-only) ===")
# item-284 (DECISIONS v121): the four CROSS-CLASS combos and present_position ∉ collapsed are DATA ERRORS —
# SINGLE-POSITION for §1b (y0dpp_bar -> None), REPORTED BY NAME, build CONTINUES (never a halt). Same-line K/G is
# the SILENT R105.1 collapse (no flag). (a) FIXTURE PROOFS are hard invariants — a guard regression is a real FAIL.
# (b) the STORE SCAN is REPORT-ONLY: it NAMES offending rows without failing the suite (item-284: continue), and
# ALWAYS emits a verdict line even at zero rows (SILENCE IS A RED).
_y0=MA.y0dpp_bar; _col=MA._collapse_elig
_reg_boardbuild=dict(MA._DPP_DATA_ERRORS)    # SNAPSHOT the real board-build registry BEFORE the fixtures pollute it
def _fix(elig,present,drafted=None):     # minimal row exercising bnow/_collapse_elig/y0dpp_bar
    dp=drafted or present
    return {'eligibilities':elig,'present_position':present,'drafted_position':dp,'pos':dp,
            '_pos_now':(present if present!=dp else None),'player':'FIXTURE','stable_player_id':'fixture'}
for _e,_pr in [('KPD,SF','KPD'),('KPF,SD','KPF'),('RUCK,SF','RUCK'),('RUCK,SD','RUCK')]:
    check(_y0(_fix(_e,_pr)) is None,
          "item-284 fixture: cross-class %s (present %s, collapsed %s) -> single-position (y0dpp_bar None)"%(_e,_pr,sorted(_col(_e))))
check(_y0(_fix('SD,SF','MID','MID')) is None,
      "item-284 fixture: present-not-in-set SD,SF present MID -> single-position (y0dpp_bar None)")
# ITEM 271 Addendum 4/5: §1b RETIRES from the year-0 path by SUPERSESSION, not deletion. The invariant is
# UNCHANGED -- a valid dual still resolves the LOWER declared bar -- but it now resolves AT SOURCE, in bnow,
# from the very `eligibilities` column §1b always read. So the fixture asserts the same fact at its new site
# and additionally pins the supersession itself. Both halves can still fail: if bnow stopped resolving the
# column, the first breaks; if §1b came back and double-applied on top of an already-lowered bar, the second.
check(MA.bnow(_fix('MID,SF','MID','MID'))=='SF',
      "item-284 fixture: VALID MID,SF present MID resolves the LOWER declared bar (SF) at source in bnow")
check(_y0(_fix('MID,SF','MID','MID')) is None,
      "item-284 fixture: §1b superseded — y0dpp_bar adds nothing once bnow already IS the lower bar")
_errs=[]
for _p in MA.data:
    _es=_col(_p.get('eligibilities'))
    if len(_es)<2: continue
    if frozenset(_es) in MA._CROSS_CLASS: _reason='cross-class'
    elif MA.bnow(_p) not in _es: _reason='present-not-in-set'
    else: continue
    _errs.append((_p.get('player'),_p.get('stable_player_id'),_reason,sorted(_es),_p.get('present_position'),_p.get('eligibilities')))
print("  item-284 STORE SCAN verdict: %d DPP data-error row(s) (report-only, build CONTINUES — never a halt)"%len(_errs))
for _pl,_sid,_rs,_cs,_pp,_el in sorted(_errs):
    print("    - %-24s [%s] %-16s elig=%-13s collapsed=%s present=%s"%(_pl,_sid,_rs,_el,_cs,_pp))
print("  item-284 runtime registry (y0dpp_bar flagged across the full board build, section 1): %d row(s)"%len(_reg_boardbuild))
for _sid,_v in sorted(_reg_boardbuild.items()):
    print("    - %-24s [%s] %-16s elig=%-13s collapsed=%s present=%s"%(_v['player'],_sid,_v['reason'],_v['eligibilities'],_v['collapsed'],_v['present']))

print("=== (9) LEG D ACT-2 — PVC RE-DERIVATION gates + ENTRY CLOSURE (RL_PVC2; promoted job-5 harness) ===")
# The one instrument for the Leg-D curve. Gated on RL_PVC2 (the v2-specific asserts); the ENTRY CLOSURE is
# structural and holds for whichever curve is loaded. HALT-not-warn: any FAIL -> sys.exit(1) below.
_pvc2_on = os.environ.get('RL_PVC2','1')!='0'
_PVC0=g['_PVC0']; _v0s=g['v0_start']; _dval=g['draftval']
# THE SPLIT (RULEBOOK v2.1 law 4). This check was shaped to the old model in BOTH its domain and its reach: it
# built _PVC0 over range(1,100) and asserted strict descent for p=1..79 — i.e. it demanded an ORDERING over
# picks that the ruling says carry no order, and it read 34 indices past the end of the curve. It now asserts
# over the domain the law governs, 1..64, and asserts the split itself: the ladder ends at the pool index.
_ND_LAST=MA.ND_CURVE_LAST; _POOL=MA.POOL_PICK
def _sd_viol(cur):
    return [p for p in range(1,_ND_LAST) if not (cur[p+1] <= cur[p] - 1)]
_p0i={k:int(round(_PVC0[k])) for k in sorted(_PVC0)}
_viol=_sd_viol(_p0i)
check(len(_viol)==0, "G-MONO strict descent on the national curve _PVC0 (p=1..%d, no plateaus): %d violation(s) %s"%(_ND_LAST,len(_viol),_viol[:6]))
check(_p0i[1]==3000, "numeraire: _PVC0(1)==3000 (got %d)"%_p0i[1])
# THE SPLIT, asserted directly: the national curve is exactly 1..64 and the only thing past it is the ONE pool
# index. If either fails, the 1-99 ladder has come back and picks past 64 are being priced again.
check(sorted(k for k in _p0i if k<=_ND_LAST)==list(range(1,_ND_LAST+1)),
      "split: national curve covers exactly 1..%d"%_ND_LAST)
check(max(_p0i)==_POOL, "split: ladder ends at the pool index %d (got %d) — there is no price for a pick past %d"%(_POOL,max(_p0i),_ND_LAST))
check(sorted(_p0i)==list(range(1,_ND_LAST+1))+[_POOL],
      "split: ladder is the national curve 1..%d plus exactly one pool entry, no other index"%_ND_LAST)
# ADDENDUM 1 (owner, 2026-07-28): NO POOL ROW MAY TEACH THE NATIONAL CURVE. Removing the chaining fixed where a
# pool entrant SITS; this asserts his outcome does not train the fit. Collapsing the pool to one index at 65 put
# every pool row inside the +/-4 sampling window of picks 61-64 at once, so without this the contamination is
# CONCENTRATED at the boundary rather than removed.
#
# THIS CHECK OBSERVES; IT DOES NOT RE-DERIVE. The previous version re-implemented the builders' filter here and
# asserted on its own copy, so it only ever tested the shared helper — the seam broke the exclusion at _natcv's
# own line and at the build_pvc call site and the suite stayed GREEN both times. Now every fit site registers the
# ACTUAL row list it sampled (rl_model._curve_sample), and this reads those recorded populations. Break the
# exclusion at any ONE site and that site's own sample carries pool rows, so it fails BY NAME.
_SAMPLES=MA._CURVE_SAMPLES
# (a) every expected site must have registered — deleting a registration must not buy silence.
_missing=[s for s in MA.CURVE_FIT_SITES if s not in _SAMPLES]
check(not _missing, "ADDENDUM 1: every curve fit site registered its sample (missing: %s)"%_missing)
# (b) per site, on the rows THAT SITE actually sampled: no pool row anywhere on the national curve.
for _site in MA.CURVE_FIT_SITES:
    _obs=_SAMPLES.get(_site) or {}
    if not _obs:
        check(False, "ADDENDUM 1: fit site '%s' registered NO sample — cannot be verified"%_site); continue
    _dirty=sorted((k,sum(1 for p in rows if MA.is_pool(p))) for k,rows in _obs.items())
    _dirty=[(k,n) for k,n in _dirty if n]
    _n=sum(len(r) for r in _obs.values())
    check(not _dirty,
          "ADDENDUM 1: fit site '%s' sampled NO pool row on the national curve (%d rows observed across %d picks; "
          "contaminated picks: %s)"%(_site,_n,len(_obs),_dirty[:6]))
# ENTRY CLOSURE (owner's named tautology, made safe): a zero-evidence entrant's evidence-free V0 basis is the
# pick-prior scaffold draftval, which == _PVC0[pick] == the loaded curve. Definitionally equal; the curve's
# content comes from OUTCOMES (derived from realized trajectories), so pricing a zero-evidence entrant leaks
# nothing. Assert on a real zero-games in-curve entrant.
_INC={'ND','RD'}
def _elig(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
_pool=[p for p in MA.data if _elig(p) and p.get('type') in _INC and MA.effpk(p) and 2004<=(p.get('year') or 0)<=2024]
_zero=[p for p in _pool if not any(r.get('games',0)>=1 and r['year']==(p.get('year')+1) for r in p['scoring'])]
if _zero:
    _z=_zero[0]; _pk=min(MA.effpk(_z),70)
    with contextlib.redirect_stdout(io.StringIO()): _dv=_dval(_z)
    check(abs(_dv-_PVC0[_pk])<1e-6, "ENTRY CLOSURE: draftval(zero-evidence %s pk%d)=%.1f == _PVC0[%d]=%.1f"%(_z['player'][:16],MA.effpk(_z),_dv,_pk,_PVC0[_pk]))
    check(abs(_dv-_p0i[_pk])<1.0, "ENTRY CLOSURE: the entrant's evidence-free V0 basis IS the loaded curve (no separate pick-prior path)")
if _pvc2_on:
    _v2=json.load(open(hp('pvc_curve_v2.json')))
    _v2c={int(k):int(v) for k,v in _v2['curve'].items()}
    # THE SPLIT: the artifact is now the national curve 1..64 plus a separate 'pool_value', so this comparison
    # walks the artifact's own domain instead of a hardcoded range(1,100) — which after the split read 35 keys
    # past the end of the curve and raised KeyError rather than reporting anything.
    check(all(_p0i[k]==_v2c[k] for k in _v2c), "_PVC0 curve == pvc_curve_v2.json over its %d-entry domain 1..%d"%(len(_v2c),max(_v2c)))
    check(_p0i[MA.POOL_PICK]==int(_v2['pool_value']), "_PVC0 pool index %d == pvc_curve_v2.json pool_value (%s)"%(MA.POOL_PICK,_v2.get('pool_value')))
    # ITEM 408 / owner R1=C — pvc_curve_v2 is a FROZEN RULER, not a derivative of the weekly live store.
    # This is a later self-test invariant (introduced after the five SSI guards), NOT Guard 1/2/3/4/5.
    # HALT-not-warn on the TRUE immutable provenance: the curve stamp binds the contract's frozen source
    # store, the per-entrant derivation, and the byte-frozen contract. Live-store divergence means
    # "re-derivation due" in the claims note/checklist; it is not curve corruption and must not re-alarm weekly.
    _curve_contract_path=(os.path.join(_repo,'ui','release_pick_curve.json') if _repo else None)
    _contract_md5='eae593f220460d880be20da38e3de39d'   # RE-PINNED by #326 (per-division pool entry anchors):
    # the curve artifact gains the N43 signed pool_levels block beside pool_value, so the artifact FILE md5
    # moves b7389fe4 -> 988135ef and the contract's pick_curve_file_md5 + its pool_levels mirror move with it.
    # The curve PAYLOAD identity df766dff is UNCHANGED — the ladder itself was not touched — which is why
    # pick_curve_curve_md5 below does not move. Both pins move in this one change, as prior acts did.
    # PREVIOUS PIN: 5b7c108c230b9afc18089a8db0aeb650 — RE-PINNED by the #274 adoption mop-up act (owner word
    # 2026-07-30): ui/release_pick_curve.json carried the STALE pool_value 528 after the 30/7 rederivation moved
    # the pool price to 299. The release-active artifact (engine/rl_after/pvc_curve_v2.json) already carried 299
    # and self-documents the move at stamp.prev_pool_value = 528, so the contract was a stale mirror, not a
    # second decision. Re-stamping it moves this md5, which is why the pin moves in the SAME commit.
    # PREVIOUS PIN: 432f0153cbe326d0ac0d0b50ec22aeb6 — RE-PINNED at THE SPLIT (2026-07-28), when the adopted
    # curve's DOMAIN went 1-99 -> 1-64 + pool. Values over 1-64 are byte-identical; that pin moved because the
    # contract file records the new domain, the pool index and the supersession. Curve SOURCE store and
    # per_entrant are UNCHANGED below - nothing was re-derived, so those two pins MOVE in this commit.
    _curve_source_store='f1e8c9fed35462536d00add604f69a3f'
    _per_entrant_md5='999d24c8'
    if not _curve_contract_path or not os.path.exists(_curve_contract_path):
        check(False, "FROZEN-RULER provenance contract present at ui/release_pick_curve.json")
    else:
        _cc=json.load(open(_curve_contract_path))
        _cc_md5=hashlib.md5(open(_curve_contract_path,'rb').read()).hexdigest()
        _stamp=_v2.get('stamp',{})
        check(_cc_md5==_contract_md5,
              "FROZEN-RULER contract byte-untouched: md5=%s (expected %s)"%(_cc_md5,_contract_md5))
        check(str(_cc.get('curve_source_store_md5'))==_curve_source_store,
              "FROZEN-RULER contract source store == %s (got %s)"%(_curve_source_store[:8],str(_cc.get('curve_source_store_md5'))[:8]))
        # ITEM 271 stage B — DECLARED HELD-UNTIL-ADOPTION. The four checks below bind the curve ARTIFACT to a
        # provenance contract that lives in ui/, and R3-2 freezes the whole UI pair until the owner's adoption
        # commit. #271 re-derived the curve, so the artifact side moved and the contract side cannot. They are
        # therefore unpassable pre-adoption BY CONSTRUCTION -- the club_curve_provenance shape, not a defect.
        # The hold is not a skip: it is gated on an explicit release_contract.json `held_candidates` declaration,
        # it still RUNS and REPORTS the delta, and it FAILS LOUDLY the moment the declaration is removed (which
        # the adoption commit does). A surviving declaration is itself a rejection.
        # The record lives in release_contract.json's `held_checks` — a SIBLING of held_candidates, not a
        # member of it. held_candidates' schema admits only BOUND RELEASE IDENTITIES (release_contract.py:126),
        # so a check-family hold was gate-illegal there and Final Integration rejected it at step 10 even
        # though its semantics were sound. `held_checks` is ignored by that schema and still covered by
        # contract_sha256, so BOTH gate readers accept it. Naming unified on the check family, FROZEN-RULER.
        _held_curve=_held_check('FROZEN-RULER') is not None
        def _curve_check(ok,msg):
            if ok or not _held_curve: return check(ok,msg)
            print("  HELD %s   [#271 stage B: declared held-until-adoption, ui/ contract frozen by R3-2]"%msg)
        _curve_check(str(_stamp.get('store_md5'))==str(_cc.get('curve_source_store_md5'))[:8],
              "FROZEN-RULER curve stamp store=%s == contract curve_source_store=%s"%(
                  _stamp.get('store_md5'),str(_cc.get('curve_source_store_md5'))[:8]))
        _curve_check(str(_stamp.get('per_entrant_md5'))==_per_entrant_md5,
              "FROZEN-RULER curve stamp per_entrant=%s == %s"%(_stamp.get('per_entrant_md5'),_per_entrant_md5))
        _curve_file_md5=hashlib.md5(open(hp('pvc_curve_v2.json'),'rb').read()).hexdigest()
        _curve_check(str(_cc.get('pick_curve_file_md5'))==_curve_file_md5,
              "FROZEN-RULER curve bytes == contract file md5 %s"%_curve_file_md5[:8])
        _curve_check(str(_cc.get('pick_curve_curve_md5'))==str(_v2.get('curve_md5')),
              "FROZEN-RULER curve payload md5=%s == contract"%_v2.get('curve_md5'))
    check(_v2.get('numeraire_pin1_3000') is True and _v2.get('r104_9_strict_descent') is True, "curve artifact self-declares pin(1)=3000 + strict descent")
    # posture discounts EXACT (BINDING; acceptance leg_d_placeholders.posture_2027_discounts)
    if os.path.exists(board_path):
        _bd=json.load(open(board_path)); _pd=_bd.get('posture_2027_discounts')
        check(_pd=={'balanced':0.10,'contender':0.15,'rebuilder':0.05}, "R104.5 posture discounts EXACT {0.10/0.15/0.05} in the board (got %s)"%_pd)
    # G-Y0 POOLED HARD gate: |comp-weighted mean day-after V0 - curve| <= 2%
    # THE SPLIT separates this into two measurements that used to be one, because after the ruling they mean
    # different things and only ONE of them is this gate's subject:
    #   (a) THE NATIONAL CURVE, picks 1-64. This is the per-pick curve fit the 2% tolerance was calibrated for.
    #       It is STILL GATED HARD at 2%, unchanged. If the split had damaged the curve, this is where it shows.
    #   (b) THE POOL, one index. This is NOT a curve fit — it asks how well ONE number fits every pool entrant,
    #       and its answer is a direct function of the pool's LEVEL, which the owner has not yet ruled. The
    #       engine currently carries the pre-split artifact's own value at index 65, because inventing a level
    #       here would be settling ITEM 412 / #207 stage-2 adoption by side effect. So the pool leg is REPORTED
    #       WITH ITS NUMBER and marked UNMEASURED — per RULEBOOK Part 3, never assumed passing, never silently
    #       waived. It is deliberately NOT gated at a tolerance calibrated for something else, and it is
    #       deliberately NOT tuned to pass: tuning it IS the owner's decision, taken without him.
    from collections import defaultdict as _dd
    _byp=_dd(list)
    for _p in _pool:
        with contextlib.redirect_stdout(io.StringIO()): _byp[MA.effpk(_p)].append(_v0s(_p))
    def _gy0(_keys):
        _n=sum(len(_byp[k])*(sum(_byp[k])/len(_byp[k]) - _p0i[k]) for k in _keys)
        _d=sum(len(_byp[k])*_p0i[k] for k in _keys)
        return (100.0*_n/_d if _d else float('nan')), sum(len(_byp[k]) for k in _keys)
    _ndk=[k for k in _byp if k<=MA.ND_CURVE_LAST]; _plk=[k for k in _byp if k>MA.ND_CURVE_LAST]
    _nd_r,_nd_n=_gy0(_ndk)
    # ITEM 271 Addendum 12 (owner word 2026-07-29): "Accept G-Y0 as ruled." A DATED exception pending #279,
    # NOT a waiver and NOT a re-pin -- the 2% bar is untouched and the live figure is printed every run. The
    # exception carries a DO-NOT-EXCEED ceiling: breach is a HARD FAIL. Removing the record is ALSO a FAIL,
    # so the exception cannot lapse into silence -- the failure mode this file exists to prevent.
    _gy0_hold=_held_check('G-Y0')
    _gy0_msg=("G-Y0 NATIONAL CURVE 1-%d |comp-weighted mean V0 - curve| = %.3f%% <= 2%% HARD (n=%d over %d picks)"
              %(MA.ND_CURVE_LAST,abs(_nd_r),_nd_n,len(_ndk)))
    if abs(_nd_r)<=2.0:
        check(True,_gy0_msg)
    elif _gy0_hold is None:
        check(False,_gy0_msg+"  [no #271 Addendum-12 record in release_contract.json held_checks — an "
                             "accepted exception that has lost its record is a FAIL, not a pass]")
    else:
        _ceil=float(_gy0_hold.get('ceiling_pct') or 0.0)
        check(abs(_nd_r)<=_ceil,
              "G-Y0 ceiling: live %.3f%% <= do-not-exceed %.3f%% (2%% bar HELD as a dated exception, #271 "
              "Addendum 12, pending #279; diagnostic map %s)"
              %(abs(_nd_r),_ceil,_gy0_hold.get('diagnostic_map')))
        if abs(_nd_r)<=_ceil:
            print("  HELD %s   [#271 Addendum 12: owner-accepted dated exception, ceiling %.3f%%, pending #279]"
                  %(_gy0_msg,_ceil))
    if _plk:
        _pl_r,_pl_n=_gy0(_plk)
        print("  UNMEASURED  G-Y0 POOL leg: comp-weighted mean v0_start sits %+.3f%% vs the carried-over pool "
              "level %d (n=%d, mean %.1f). REPORTED, NOT GATED, and NOT a licence to move the level."
              %(_pl_r,_p0i[MA.POOL_PICK],_pl_n,sum(_byp[MA.POOL_PICK])/len(_byp[MA.POOL_PICK])))
        print("              READ THIS BEFORE ACTING ON THAT NUMBER — it is NOT evidence the pool is priced low:")
        print("                - it is a mean of v0_start, a ZERO-EVIDENCE PEDIGREE projection, not of realised output;")
        print("                - within this population that projection is INVERTED: among matured pool entrants the")
        print("                  players who NEVER PLAYED A GAME score HIGHER on it (618.3, n=297) than those who did")
        print("                  (553.1, n=429). A quantity where busts outscore contributors cannot set an entry level;")
        print("                  [ERA FIGURES: measured on the pre-split frozen v0surf surface, sig 76498b5a,")
        print("                   over #217's 763-row population. They are kept because they are the evidence")
        print("                   the inversion argument was FIRST made on, not because they describe today's")
        print("                   surface -- #271 stage B re-baked it and the frozen signature is now b781ed25")
        print("                   over the ruled 1,093-row pool. The conclusion is unchanged and re-measured;")
        print("                   only the numbers below are era data. (R4-2, rewritten at #271's re-bake.)]")
        print("                - it exceeds the value of the LAST NATIONAL PICK (curve[%d]=%d), which no pool entry"%(MA.ND_CURVE_LAST,_p0i[MA.ND_CURVE_LAST]))
        print("                  level can coherently do — the pool sits BELOW the curve, by construction;")
        print("                - the population is NOT the ruled pool: this leg admits only ND 65+ and RD, and drops")
        print("                  every MSD/SSP/IRE/UNR/PDA/PDN/PDS row (331 of 1,094 in the 2004-2024 window);")
        print("                - and it is ~7.5% downstream of the level itself (measured by perturbation), so part of")
        print("                  any 'gap' closes itself when the level moves.")
        print("              Setting the pool's level needs a REALISED-OUTCOME basis (#207 stage 2 / ITEM 412) and is")
        print("              the owner's call. Not tuned here, and not to be tuned from this figure.")
    print("       (G-Y0 owner-viewing per-pick residual curve: session_2026-07-17/legd_derivation/out/gy0_residual_curve_v2.json — REPORT-ONLY)")
else:
    print("  NOTE  RL_PVC2=0 (L1b base path): v2-specific asserts skipped; ENTRY CLOSURE above holds either way.")

print("=== (10) #326 PER-DIVISION POOL ENTRY ANCHORS — the N43 signed levels ===")
# THE OWNER'S SIGNED TABLE, ANCHORED HERE. The artifact cannot be its own authority: if this section read the
# levels only from the artifact, an edited level would agree with itself and pass. So the signed numbers are
# written out once, copied verbatim from the owner's N43 signature (#306 comment 5179992080), and everything
# else is checked against them. A wrong level in the artifact and a wrong lookup in the code each go red here.
_N43_FLAT={'MSD':286.8,'SSP':252.8,'PDA':194.3,'PDS':145.0,'IRE':133.4,'PDN':123.0,'UNR':103.7}
_N43_RD={'KPD':300.3,'MID':294.8,'RUCK':282.5,'SD':246.9,'SF':231.5,'KPF':216.0}
_N43_ND65_K15=266.1; _N43_RD_LEVEL=261.6; _N43_RD_TARGET=262.2; _N43_POOL_AGG=235.8; _N43_K=15
_v2doc=json.load(open(hp('pvc_curve_v2.json')))
_pl=_v2doc.get('pool_levels')
check(bool(_pl), "#326: the curve artifact carries a pool_levels block beside pool_value")
if _pl:
    check({_k:float(_v) for _k,_v in _pl['signed_flat'].items()}==_N43_FLAT,
          "#326 signed flat levels verbatim (MSD/SSP/PDA/PDS/IRE/PDN/UNR): %s"%_pl['signed_flat'])
    check({_k:float(_v) for _k,_v in _pl['signed_rd_positional'].items()}==_N43_RD,
          "#326 signed RD positional set verbatim (KPD/MID/RUCK/SD/SF/KPF): %s"%_pl['signed_rd_positional'])
    check(float(_pl['signed_nd65_plus']['measured_k15'])==_N43_ND65_K15
          and int(_pl['signed_nd65_plus']['cap_against_curve_pick'])==MA.ND_CURVE_LAST,
          "#326 ND65+ is stored as the LAW: measured %.1f capped against curve pick %d (never a literal price)"
          %(float(_pl['signed_nd65_plus']['measured_k15']),int(_pl['signed_nd65_plus']['cap_against_curve_pick'])))
    check(_pl['rd_position_field']=='future_position',
          "#326 the RD positional key names future_position (got %r)"%_pl['rd_position_field'])
    check(float(_pl['rd_division_level'])==_N43_RD_LEVEL and float(_pl['rd_positional_shrink_target'])==_N43_RD_TARGET
          and float(_pl['measured_pool_aggregate'])==_N43_POOL_AGG and int(_pl['k'])==_N43_K,
          "#326 the reference quantities are each carried where N43 uses them: RD level %.1f · positional target "
          "%.1f · pool aggregate %.1f · K=%d"%(float(_pl['rd_division_level']),float(_pl['rd_positional_shrink_target']),
                                               float(_pl['measured_pool_aggregate']),int(_pl['k'])))
    _cav=str(_pl.get('msd_completion_optimism_caveat',''))
    check('4.7' in _cav and '8.4' in _cav,
          "#326 MSD's completion-optimism caveat travels with its level: %r"%_cav)
    print("       MSD %.1f  [completion optimism %s]"%(_N43_FLAT['MSD'],_cav))
    # the ui provenance contract mirrors the block, exactly as it mirrors pool_value
    _ccp=globals().get('_curve_contract_path')
    if _ccp and os.path.exists(_ccp):
        check(json.load(open(_ccp)).get('pool_levels')==_pl,
              "#326 ui/release_pick_curve.json mirrors the artifact's pool_levels verbatim")
    # ---- the engine's OWN resolved table, and the cap re-evaluated as the law rather than read back --------
    _want={_k:int(_v) for _k,_v in _N43_FLAT.items()}
    _want.update({'RD:'+_k:int(_v) for _k,_v in _N43_RD.items()})
    _want['ND65+']=int(min(_N43_ND65_K15,float(MA._PVC2M[MA.ND_CURVE_LAST])))
    check(len(_want)==14, "#326 fourteen priced levels: eight flat divisions + six RD positional (got %d)"%len(_want))
    check(MA._POOL_LEVELS==_want,
          "#326 the engine's resolved pool levels == the signed table (ND65+ = min(%.1f, curve[%d]=%d) = %d)"
          %(_N43_ND65_K15,MA.ND_CURVE_LAST,MA._PVC2M[MA.ND_CURVE_LAST],_want['ND65+']))
    # ---- THE CURRENCY LAW (addendum 6 item 5), proven on ONE entrant through EACH SITE CLASS ---------------
    # The signed levels are LADDER/board currency. They enter the ENGINE-VALUE sites (the year-zero floor and
    # the thin-record blend) multiplied by the board factor F, and the LADDER-currency site (the ruck prior
    # cap's basis) unconverted. Both directions are checked on real rows, so a conversion applied in the wrong
    # place — or applied twice — fails here instead of drifting the board 5%.
    _anchor=g['entry_anchor']; _capb=g['_cap_basis']; _plf=g['_PL_F']; _prefloor=g['ev_prefloor']
    _ffrac=g['floor_frac']; _nspro=g['nseas_pro']; _v0s_fn=g['v0_start']
    check(abs(_plf-_F)<1e-12, "#326 currency: the engine's board factor is the certified %.4f (got %.6f)"%(_F,_plf))
    _poolp=[p for p in MA.players if p.get('_pool')]
    _cur_lad=[p for p in _poolp if abs(_capb(p)-float(MA.pool_level(p)))>1e-9]
    check(not _cur_lad,
          "#326 currency (ladder site — the ruck cap's basis): all %d pool entrants enter UNCONVERTED, at the "
          "signed level itself; %d would not"%(len(_poolp),len(_cur_lad)))
    _cur_eng=[p for p in _poolp if abs(_anchor(p)-float(MA.pool_level(p))*_F)>1e-6]
    check(not _cur_eng,
          "#326 currency (engine-value sites — floor and blend): all %d pool entrants enter at level x%.4f; "
          "%d would not"%(len(_poolp),_F,len(_cur_eng)))
    _rk=[p for p in _poolp if MA.gfut(p)=='RUCK']
    if _rk:
        _r0=_rk[0]
        print("       currency proof rows: ladder site %s (%s) basis %.1f == level %d · engine site same row "
              "anchor %.1f == %d x %.4f"%(_r0['player'][:20],MA.pool_division(_r0),_capb(_r0),MA.pool_level(_r0),
                                          _anchor(_r0),MA.pool_level(_r0),_F))
    # A board-currency round trip: an entrant held at the floor displays at the signed level x the schedule,
    # because the board divides by the same F the anchor multiplied by. If the conversion were dropped at the
    # engine site, this figure would be ~5% out.
    print("       board-currency round trip: level x %.4f (engine) / %.4f (display) == the signed level itself"%(_F,_F))
    # ---- NO SILENT REFIT (the frozen-surface trap, addendum 6) ---------------------------------------------
    # The levels resolve in the entry-anchor lookup and are never written into the ladder or its scaffold copy,
    # so the year-zero surface signature cannot move and the frozen surface must LOAD. If it ever refitted,
    # every national draftee's V0 would move and "non-pool veterans do not move" would silently stop being true.
    # THE SPLIT (#344): this is the SILENT half, and it is the second site of the same requirement — the build
    # asserts it too (_merged_recover.py, #326 proof (1)). A DECLARED refit (RL_V0SURF_REFIT=1) is the engine's
    # one committed fit path and passes here; release builds cannot carry one (release contract must_be_unset).
    # The message names WHICH lane passed, because "LOADED, not refitted" on a refitted build is a false report.
    # THREE states, each named truthfully — a message that guesses its lane is the same false-report fault
    # the build-side print was fixed for: loaded (green), declared (green), neither (RED — the silent refit).
    _meta=g['_V0CURVE_META']; _refit_dec=os.environ.get('RL_V0SURF_REFIT')=='1'
    _frz=_meta.get('_v0surf_frozen') is True
    check(_frz or _refit_dec,
          "#326 no SILENT refit of the year-zero surface — %s (sig %s; RL_V0SURF_REFIT=%r)"
          %("frozen surface LOADED, not refitted" if _frz else
            "refit DECLARED, so this build is a fit lane and is barred from release" if _refit_dec else
            "SILENT REFIT: the surface was NOT loaded from the freeze and NO refit was declared",
            str(_meta.get('_v0surf_sig'))[:8],os.environ.get('RL_V0SURF_REFIT')))
    check(int(g['_PVC0'][MA.POOL_PICK])==int(_v2doc['pool_value']),
          "#326 the levels were never written into the ladder's scaffold copy — _PVC0[%d] is still pool_value "
          "%s (the surface signature reads this dict, so writing a level here would refit the surface)"
          %(MA.POOL_PICK,_v2doc['pool_value']))
    # ---- POOL_VALUE ISOLATION: no player price reads the ladder's pool slot --------------------------------
    # Two different claims, both proven. (a) STRUCTURAL: every pool entrant's anchor and cap basis IS his own
    # division's level, so the lookup cannot reach the pool slot. (b) MEASURED: move the ladder's pool slot and
    # watch the board — nothing follows it. (b) needs the V0 caches cleared, or a stale cache would answer for
    # the engine and the check would pass without measuring anything.
    _slot=int(g['_PVC0'][MA.POOL_PICK])
    check(_slot==int(_v2doc['pool_value']),
          "#326 the ladder still carries pool_value %d at index %d (kept for the pick side, the entrant layer "
          "and the display bands)"%(_slot,MA.POOL_PICK))
    _reads_slot=[p['player'] for p in _poolp
                 if abs(_capb(p)-_slot)<1e-9 or abs(_anchor(p)-_slot*_F)<1e-6]
    check(not _reads_slot,
          "#326 pool_value isolation (structural): no pool entrant's basis equals the pool slot %d (%d would)"
          %(_slot,len(_reads_slot)))
    def _clear_v0():
        g['_V0C'].clear(); g['_V0U'].clear(); g['_RUCCEIL'].pop('grid',None); MA._pe_clear()
    _sl_before={}
    _clear_v0()
    with contextlib.redirect_stdout(io.StringIO()):
        for p in MA.players: _sl_before[p['key']]=ev(p,2026)
    _p0=g['_PVC0']; _p0_keep=_p0[MA.POOL_PICK]; _p0[MA.POOL_PICK]=int(_p0_keep)+163
    _clear_v0()
    with contextlib.redirect_stdout(io.StringIO()):
        _sl_movers=[p['player'] for p in MA.players if ev(p,2026)!=_sl_before[p['key']]]
    _p0[MA.POOL_PICK]=_p0_keep; _clear_v0()
    check(not _sl_movers,
          "#326 pool_value isolation (measured): no board price follows the ladder's pool slot — %d row(s) do: %s"
          %(len(_sl_movers),', '.join(sorted(_sl_movers)[:8]) or 'none'))
    # ---- THE WRONG-FIELD DISCRIMINATOR, over the STORE population -----------------------------------------
    # Addendum 3 item 2: the store is where the differing rows live, so the field proof runs there. On the
    # board only the drafted-vs-future case exists.
    _rd=[p for p in MA.data if p.get('type')=='RD']
    _dp=sum(1 for p in _rd if p.get('present_position')!=p.get('future_position'))
    _dd=sum(1 for p in _rd if p.get('drafted_position')!=p.get('future_position'))
    check(_dp>0 and _dd>0,
          "#326 wrong-field discriminator exists over the store: %d of %d RD rows differ present-vs-future, "
          "%d differ drafted-vs-future"%(_dp,len(_rd),_dd))
    _mis_p=[p['player'] for p in _rd
            if MA._POOL_LEVELS['RD:'+(MA.GRP.get(p.get('present_position')) or MA.gfut(p))]
            != MA._POOL_LEVELS['RD:'+MA.gfut(p)]]
    _mis_d=[p['player'] for p in _rd
            if MA._POOL_LEVELS['RD:'+(MA.GRP.get(p.get('drafted_position')) or MA.gfut(p))]
            != MA._POOL_LEVELS['RD:'+MA.gfut(p)]]
    check(len(_mis_p)==_dp and len(_mis_d)==_dd,
          "#326 a present- or drafted-keyed build misprices %d / %d store rows — the wrong field fails "
          "deterministically, not three builds in four"%(len(_mis_p),len(_mis_d)))
    check(all(MA._pool_rd_position(p)==MA.gfut(p) for p in _rd),
          "#326 the engine's RD positional key IS the settled future position on all %d rookie rows"%len(_rd))
    _board_diff=[p for p in _poolp if p.get('type')=='RD'
                 and p.get('drafted_position')!=p.get('future_position')]
    check(len(_board_diff)>0,
          "#326 on-board drafted-vs-future proof population: %d active rookie entrant(s) — %s"
          %(len(_board_diff),', '.join(sorted(x['player'] for x in _board_diff))))
    check(all(MA._POOL_LEVELS['RD:'+(MA.GRP.get(p.get('drafted_position')) or MA.gfut(p))]
              !=MA._POOL_LEVELS['RD:'+MA.gfut(p)] for p in _board_diff),
          "#326 each of those active entrants is priced at a DIFFERENT level under the wrong field")
    print("       present-vs-future has no on-board discriminator today (0 active differing rows) — which is why "
          "the field proof runs over the store population; the drafted-vs-future case does exist on the board.")
    # ---- REACH-THE-ENTRY-PRICE, ALL FOURTEEN LEVELS -------------------------------------------------------
    # Addendum 5 as amended by addendum 6 item 6: a level is proven when a REAL record-thin entrant's board
    # price carries it — through EITHER the year-zero floor OR the thin-record blend; either route satisfies
    # the gate. A level with no live exerciser proves on a real row evaluated off-board (addendum 6 item 7:
    # PDS is 21 retired rows, so it proves by the engine's own retired-row technique — lift the flags,
    # evaluate, restore — never a synthetic key). The exerciser and the route are found from the population
    # at build time, never hardcoded, so a first signing at a dormant pathway flips that level onto the live
    # tier loudly instead of leaving a check that quietly measures nothing.
    _bd={r['key']:r for r in (json.load(open(board_path))['active'] if os.path.exists(board_path) else [])}
    def _board_price(p):
        with contextlib.redirect_stdout(io.StringIO()):
            v=ev(p,2026); ev(p,2024); ev(p,2025); ev(p,2027); ev(p,2028)   # the export's as-of sequence, as (2) above
            return v
    def _price(p):
        with contextlib.redirect_stdout(io.StringIO()): return ev(p,2026)
    def _route(p):
        with contextlib.redirect_stdout(io.StringIO()):
            _pre=_prefloor(p,2026); _post=ev(p,2026); _ns=_nspro(p,2026)
        if _post!=_pre: return 'floor'
        if _ns==0: return 'blend'
        return 'ruck cap'
    def _arith_note(p,level):
        """For a floored entrant, the board price IS the schedule fraction times the signed level — printed
        so the number can be checked by hand rather than taken on trust."""
        _yis=2026-int(p.get('year') or 0)
        if _route(p)!='floor': return ''
        return '  = floor_frac(%d yrs)=%.2f x level %d' % (_yis,_ffrac(_yis),level)
    def _lift(p):
        """The engine's retired-row evaluation: lift the two flags that keep a concluded career off the live
        board, price the row, put them back. The row is real; only its listing status is suspended."""
        return (p.get('_retired'),p.get('_last_listed'))
    _byl={}
    for p in _poolp: _byl.setdefault(MA.pool_division(p),[]).append(p)
    _store_byl={}
    for p in MA.data:
        if p.get('_pool'): _store_byl.setdefault(MA.pool_division(p),[]).append(p)
    _tier={}
    for _k in sorted(_want):
        _on=_byl.get(_k) or []
        _kept=MA._POOL_LEVELS[_k]
        _probe=int(round(_kept*1.5))
        if _on:
            _base={id(p):_price(p) for p in _on}
            MA._POOL_LEVELS[_k]=_probe; MA._pe_clear()
            _moved=[p for p in _on if _price(p)!=_base[id(p)]]
            MA._POOL_LEVELS[_k]=_kept; MA._pe_clear()
            _named=sorted(_moved,key=lambda p:_base[id(p)])[:1]
            # the named entrant is tied back to the SHIPPED board through the export's own as-of sequence, so
            # "reaches the price" means the board row, not a number this file computed for itself.
            _ok=bool(_named) and all(_bd.get(p['key'],{}).get('v')==_num(_board_price(p)) for p in _named)
            _tier[_k]=('live',len(_on),len(_moved),
                       (_named[0]['player'] if _named else None),
                       (_route(_named[0]) if _named else '-'),
                       (_bd.get(_named[0]['key'],{}).get('v') if _named else None),
                       (_arith_note(_named[0],_kept) if _named else ''))
            # END-TO-END CURRENCY, through a real board price. On the floor route the whole chain is
            # visible in one number: the anchor multiplies the signed level by the board factor, the export
            # divides by it again, so the shipped price is EXACTLY the year's floor fraction times the signed
            # level. A conversion dropped, doubled, or applied at the wrong site moves this by ~5% and the
            # check goes red — it bites on the SITES, not just on the anchor function.
            if _named and _route(_named[0])=='floor':
                _pn=_named[0]; _yis=2026-int(_pn.get('year') or 0)
                _expect=round(_ffrac(_yis)*_kept)
                check(abs(int(_bd.get(_pn['key'],{}).get('v') or 0)-_expect)<=1,
                      "#326 currency end-to-end (%s): %s ships at %s == floor_frac(%d)=%.2f x signed level %d "
                      "= %d — the level is quoted in the currency the board displays"
                      %(_k,_pn['player'],_bd.get(_pn['key'],{}).get('v'),_yis,_ffrac(_yis),_kept,_expect))
            check(_ok, "#326 level %s reaches a real entrant's BOARD price — %s via the %s (board v=%s; %d of "
                       "%d live entrants re-price when the level moves)"
                  %(_k,(_named[0]['player'] if _named else 'NO LIVE ENTRANT RE-PRICES'),
                    (_route(_named[0]) if _named else '-'),
                    (_bd.get(_named[0]['key'],{}).get('v') if _named else '-'),len(_moved),len(_on)))
        else:
            _rows=_store_byl.get(_k) or []
            _saved=[(p,_lift(p)) for p in _rows]
            for p,_ in _saved: p['_retired']=False; p['_last_listed']=None
            MA._pe_clear()
            _base={id(p):_price(p) for p in _rows}
            MA._POOL_LEVELS[_k]=_probe; MA._pe_clear()
            _moved=[p for p in _rows if _price(p)!=_base[id(p)]]
            MA._POOL_LEVELS[_k]=_kept; MA._pe_clear()
            _nm=sorted(_moved,key=lambda p:_base[id(p)])[:1]
            _rt=(_route(_nm[0]) if _nm else '-'); _pv=(_base[id(_nm[0])] if _nm else None)
            for p,(_r,_ll) in _saved: p['_retired']=_r; p['_last_listed']=_ll
            MA._pe_clear()
            _tier[_k]=('probe (retired rows lifted)',0,len(_moved),
                       (_nm[0]['player'] if _nm else None),_rt,(_num(_pv) if _pv is not None else None),
                       (_arith_note(_nm[0],_kept) if _nm else ''))
            check(bool(_moved),
                  "#326 level %s has 0 live entrants — proved on its REAL rows off-board (retired flags lifted, "
                  "evaluated, restored): %s via the %s (%d of %d rows re-price when the level moves)"
                  %(_k,(_nm[0]['player'] if _nm else 'NO ROW RE-PRICES'),_rt,len(_moved),len(_rows)))
    print("       reach-the-entry-price, all fourteen levels (route and exerciser found at build time).")
    print("       On the FLOOR route the arithmetic is visible: the board price is the year's floor fraction")
    print("       times the signed level, because the anchor multiplies by the board factor and the board")
    print("       divides by it again — so the level is quoted in the same currency the board displays.")
    print("       %-9s %6s  %-27s %4s %5s  %-9s %s"
          %('level','value','tier','n','moved','route','entrant (board price)'))
    for _k in sorted(_tier):
        _t,_n,_m,_nm,_rt,_bv,_arith=_tier[_k]
        print("       %-9s %6d  %-27s %4d %5d  %-9s %s (%s)%s"
              %(_k,MA._POOL_LEVELS[_k],_t,_n,_m,_rt,_nm,_bv,_arith))
    print("       pool population by division (engine classification, re-derived at build time): %s"
          %(' · '.join('%s %d'%(_k,len(_store_byl.get(_k) or [])) for _k in sorted(_want))))
    print("       MSD's level carries its completion-optimism caveat wherever it is shown: %s"%_cav)

print("=== (11) D14 V0 BOARD LAWS — WIRED INTO THE BUILD (owner ruling 1.2, 2026-08-10; #334) ===")
# WHY THIS SECTION EXISTS. The D14 laws already existed, and they would have gone red on 2026-08-05 the
# day the never-rises law was lost. They did not fire, because they lived ONLY in ship_gates_check.py —
# a HAND-RUN checklist. It last ran 2026-07-17, nineteen days before the break; the #306 landing re-ran
# six other gates and D14 was not among them. That is the process hole the audit named, and a gate that
# is only run when somebody remembers is not a gate. D14a/b/c now run on the STANDING GATED BUILD PATH:
# every board build reaches this file, and this file exits non-zero — the build HALTS.
#   ship_gates_check.py keeps its own D14 block and stays the hand-run SUPERSET (three-column board,
#   snapshots, the whole checklist). This is deliberate duplication of a cheap check, not a move.
#
# D14d is NEW and closes the audit's COVERAGE hole. D14b compares real players; the audit measured that
# real players expose about 8% of the surface's rising steps. D14d scans the surface itself — every
# position x draft-age profile, every adjacent pick pair, zero tolerance.
print("       (D14a/b/c were hand-run-only until this wiring — the 2026-08-05 break went 19 days unseen.)")
try:
    _d14=g['_v0_curve_assert']()
    check(_d14['cross_draft_maxdisp']<1e-6,
          "D14a same pos x draft-age x recorded-pick => IDENTICAL V0* across draft years "
          "(max cross-draft dispersion %.6f over the %d rows the surface prices)"
          %(_d14['cross_draft_maxdisp'],_d14.get('population',0)))
    check(_d14['within_cell_inversions']==0,
          "D14b within (pos x draft-age x draft-year) V0 inversions under V0* = %d (must be 0)"
          %_d14['within_cell_inversions'])
    check(_d14['kpp_depth_monotone'],
          "D14c KPP retention floor O1 preserves depth monotonicity = %s"%_d14['kpp_depth_monotone'])
    # REPORT-ONLY, never a pass/fail: the same two figures over ALL national-draft rows including the
    # pool rows at pick 65+. Those rows are priced off their signed division levels and never read this
    # surface, so a "dispersion" or an "inversion" against them is a comparison of two different price
    # objects — which is why D14a/b were unsatisfiable until the population was corrected. Printed so
    # the number is visible rather than quietly dropped.
    print("       report-only, ALL ND rows incl. %d pool rows at pick 65+ (priced off signed division "
          "levels, not this surface): dispersion %.1f · %d pick pairs — ladder-vs-pool comparisons, "
          "not surface faults"%(_d14.get('pool_rows_excluded',0),_d14.get('report_only_all_nd_maxdisp',0.0),
                                _d14.get('report_only_all_nd_inversions',0)))
except Exception as _ex:
    check(False,"D14a/b/c could not run on this engine: %s: %s"%(type(_ex).__name__,_ex))
try:
    _d14d=g['_v0_surface_assert']()
    check(_d14d['rising_steps_1_64']==0,
          "D14d THE NEVER-RISES LAW ON THE SURFACE (owner R12): %d rising step(s) across %d "
          "position x draft-age profiles x adjacent pick pairs, picks 1-64 — must be 0%s"
          %(_d14d['rising_steps_1_64'],_d14d['cells'],
            ('  || first: '+' | '.join(_d14d['worst'][:3])) if _d14d['worst'] else ''))
    check(_d14d['rising_steps_full_grid']==0,
          "D14d (full grid) %d rising step(s) over the whole 1-%d pick grid the surface carries — must be 0"
          %(_d14d['rising_steps_full_grid'],_d14d['grid']))
    print("       D14d scanned %d cells x %d grid picks = %d adjacent pairs (players expose ~8%% of these)"
          %(_d14d['cells'],_d14d['grid'],_d14d['cells']*(_d14d['grid']-1)))
    _isr=(g['_V0CURVE_META'].get('_iso_restore') or {})
    if _isr: print("       restore provenance: %s | grid points moved %s"
                   %(_isr.get('law'),_isr.get('grid_points_moved')))
except Exception as _ex:
    check(False,"D14d surface scan could not run on this engine: %s: %s"%(type(_ex).__name__,_ex))

print("\n"+("SELF-TEST FAILED: %d check(s)\n  - "%len(FAIL)+"\n  - ".join(FAIL) if FAIL else
      "SELF-TEST PASSED: single source; guards 1-3; board==engine (F1); book==board (F2); Kako+Bontempelli ground-truth; DPP blend stripped; Leg B L-RECENCY + ρ forbidden-list (R105.5/R105.4); collision sentry (King pair) clean."))
print("  (GUARD 4 — correction-sticks canary — runs separately: python3 guard_correction_canary.py)")
sys.exit(1 if FAIL else 0)
