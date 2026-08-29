import os
import io,contextlib,json,collections,numpy as np
import single_source as _SS
try:                            # gate-integrity (e): config manifest. NO-OP unless RL_CONFIG_MODE=bake|gate.
    import config_manifest as _CFG; _CFG.enforce()   # gate mode (matrix regen for B1/B3): clear ambient model env, reject unknown/divergent, load data/model_config.json BEFORE the engine reads the env.
except ImportError:
    _CFG = None
# GUARDS 3 + 3b always; GUARD 2 asserts the board stamp == current source md5 (the book is about to be
# parity-checked against the board -- both MUST derive from the same store). Skipped only if the board is
# routed elsewhere (RL_APP_DATA) for a standalone book build.
_SS.assert_startup(consume=['rl_app_data.json'] if os.environ.get('RL_APP_DATA','rl_app_data.json')=='rl_app_data.json' and os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),'rl_app_data.json')) else [])
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
g['_BOARD_PATH']=False   # D14: BACKTEST/WALK-FORWARD path — Luke's exemption. Board-only laws (V0 curve, KPP floor) OFF here so the historical book reproduces (maxΔ=0 vs v2.3).
MA=g['MA'];ev=g['ev'];delisted=g['delisted']
INCURVE={'ND','RD'}; POOLED={'MSD','SSP','UNR','IRE','PDA','PDN','PDS'}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players=[p for p in MA.data if eligible(p)]
best={}
for p in players:
    k=(p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))  # +year: keep same-name-different-cohort pairs distinct
    if k not in best or len(p['scoring'])>len(best[k]['scoring']): best[k]=p
players=list(best.values())
# ==== S2 PARALLELIZATION (owner word 2026-08-28: "go on walk forward assuming no tradeoffs") =====
# The as-of pricing is per-player independent GIVEN the full-population as-of-Y state, so each
# worker replicates the (cheap) whole-population truncation for every year and prices only its
# shard — every cell's computation is state-identical to the sequential run, whatever the engine
# reads across players. Sharding is by DETERMINISTIC stable-key order (never id()); an OVERLAP set
# of 25 players is priced by EVERY worker and the parent refuses the merge on any disagreement —
# the no-tradeoff bar, checked in the run itself. Names are S4_* (a tool's own flags are never
# RL_*). Default S4_WORKERS=1 is the sequential path, byte-for-byte the code above this line.
players.sort(key=lambda p:(str(p.get('key') or MA.slug(p['player'])),str(p.get('type')),str(p.get('year') or '')))
_S4_WORKERS=max(1,int(os.environ.get('S4_WORKERS','1') or '1'))
_S4_SHARD=os.environ.get('S4_SHARD')            # "i/N" in a worker child
_S4_OVERLAP=25
def _stable_key(p): return '%s|%s|%s'%(p.get('key') or MA.slug(p['player']),p.get('type'),p.get('year'))
if _S4_SHARD:
    _si,_sn=(int(x) for x in _S4_SHARD.split('/'))
    def _mine(j): return j%_sn==_si or j<_S4_OVERLAP
else:
    def _mine(j): return True
_PARENT=(_S4_WORKERS>1 and not _S4_SHARD)
if _PARENT:
    import subprocess as _sp, tempfile as _tf
    _shard_files=[]
    _procs=[]
    for _i in range(_S4_WORKERS):
        _fd,_sf=_tf.mkstemp(prefix='s4_shard_%d_'%_i,suffix='.json'); os.close(_fd)
        _shard_files.append(_sf)
        _env=dict(os.environ); _env['S4_SHARD']='%d/%d'%(_i,_S4_WORKERS); _env['S4_SHARD_OUT']=_sf
        _env.pop('S4_WORKERS',None)
        _procs.append(_sp.Popen([__import__('sys').executable,os.path.abspath(__file__)],env=_env,
                                stdout=_sp.PIPE,stderr=_sp.STDOUT,text=True))
    print('S4_WORKERS=%d — %d shard children pricing in parallel (overlap=%d, stable-key order)'
          %(_S4_WORKERS,_S4_WORKERS,_S4_OVERLAP),flush=True)
# ISOLATED DATA FIX (Isaac Kako, ND pk13 2024): his real 2025 debut (23g, 55.1 — 2024 Rising Star) was missing
# from the source DB. As of the one-source rewire (2026-07-05) it is FOLDED INTO THE STORE (single source of
# truth), so both the board and this book read it directly -- the former book-local patch is DELETED. Luke
# confirmed this is isolated to Kako (known missing-data case), not systemic.
print(f"eligible players: {len(players)}",flush=True)
# ==== F2 FIX 2026-07-05 (Luke one-source rewire): the stale double-fade harness is DELETED ================
# BEFORE: this generator re-injected its OWN _coreM1/_inferM1/_v7/_b6fix on top of the live engine. That copy
# (1) RESURRECTED the deleted upper-quantile compression cB=0.47*clip((effs-1)/3,0,1) on bb[3]/bb[4] -- gone
# from the engine since 02/07/2026 (_merged_recover v7-cB DELETED) -- and (2) wrapped the engine's ALREADY
# v7-wrapped b6 with _v7 AGAIN, so the age-taper `asc` was applied TWICE. Net: the book UNDER-priced the same
# players the board over-priced (Josh Ward engine 1640 -> book 1233, -24.8%). F2.
# AFTER: nothing is re-injected. The walk-forward book is built from the LIVE gated engine ev() -- the single
# valuation source -- so every book cell equals the engine's gated value by construction. A parity check at the
# end asserts book(current-year) == engine gated ev() for every player, matched by stable key, or the build FAILS.
print("[F2 FIX] double-fade harness removed; book built from live gated engine ev()",flush=True)
# ==== #338 MINIMUM LISTING TENURE (owner word "Fire 338", 2026-08-06) ====================================
# DEFECT: listed-through was `_last_listed` else the last SCORING year — and the last scoring year is 0 for a
# career the source DB kept no rows for, so 619 evidence-less historical records reconstructed as DELISTED at
# every as-of year: ev() returned the 2% remnant (_merged_recover delist branch) before any machinery ran, and
# the yend/yrs window below emitted a single-row career. Delisted on draft day, by absence of evidence.
# THE RULE (the owner's, #338): a drafted player is on a list for a minimum tenure whether or not the DB kept
# his numbers. With NO explicit `_last_listed`: assumed-listed-through = debut + N − 1, where debut is the
# route's own convention (entry year + 1 on every route except MSD — a mid-season draftee debuts in his ENTRY
# year) and N = 4 for ND picks 1-20, 3 for ND 21-40, 2 for everything else (ND 41+ and every pool route).
# OWN DATA EXTENDS: listed-through = max(assumed, last scoring year). An explicit `_last_listed` is a KNOWN
# FACT and stands, even when it is shorter than the minimum. Active players are untouched.
# A year inside listed tenure with no scoring row is a LISTED SITTING-OUT year — priced by the EXISTING sit-out
# machinery, no new pricing rule here. That is the point: era parity by construction, a historical no-data year
# valuing through the same code path as a current player's sit-out year.
def _min_tenure(p):
    """#338: minimum listed seasons implied by the entry route/pick band."""
    if p.get('type')=='ND' and not p.get('_pickless'):
        pk=MA.effpk(p)
        if pk<=20: return 4
        if pk<=40: return 3
    return 2                                      # ND 41+ and every pool route (RD/MSD/SSP/UNR/IRE/PDA/PDN/PDS)
def _debut_year(p):
    """#338: first season ON A LIST. MSD debuts in its entry year; every other route the year after."""
    C=p.get('year')
    return None if C is None else (C if p.get('type')=='MSD' else C+1)
def _listed_through(p,lastscore):
    """#338: the year the player's listing runs through, or None if he is still listed (active, untouched)."""
    LL=p.get('_last_listed')
    if LL is not None: return LL                  # known fact — stands even if shorter than the minimum
    if not p.get('_retired'): return None         # active: no listed-through, untouched by this rule
    d=_debut_year(p)
    return max((d+_min_tenure(p)-1) if d is not None else 0, lastscore)   # own data extends the minimum
# WALK-FORWARD as-of value matrix (UNCHANGED — values are correct; only the indexing was wrong)
# S2: the truncation runs over the FULL population in every process; only the PRICING is sharded.
ASOF={}
if not _PARENT:
    for Y in range(2003,2027):
        saved={}
        for p in players:
            if (p.get('year') or 9999)>Y: continue
            LL=p.get('_last_listed'); RET=p.get('_retired'); lastscore=max((r['year'] for r in p['scoring']), default=0)
            saved[id(p)]=(p['scoring'],RET,LL); p['scoring']=[r for r in p['scoring'] if r['year']<=Y]
            # #338 (2026-08-06): was `LL if LL is not None else (lastscore if RET else None)` — lastscore is 0 for an
            # evidence-less career, so the player was delisted at every as-of year. Now the minimum listing tenure.
            eff_last = _listed_through(p,lastscore)
            p['_retired']=False; p['_last_listed']= eff_last if (eff_last is not None and eff_last < Y) else None
        MA.BASE_REF=Y; MA.AGE_REF=Y; MA._pe_clear()
        g['_BOARD_PATH']=(Y==2026)   # F2 parity: the PRESENT-year column uses the BOARD path (V0 curve + KPP floor ON) so `cur` == the board (engine gated); 2003-2025 keep Luke's D14 backtest exemption (board-only laws OFF -> the historical walk-forward book reproduces)
        for _j,p in enumerate(players):
            if not _mine(_j): continue
            if (p.get('year') or 9999)>Y: continue
            try:
                with contextlib.redirect_stdout(io.StringIO()): ASOF[(id(p),Y)]=ev(p,Y)
            except Exception: ASOF[(id(p),Y)]=None
        for p in players:
            if id(p) in saved: p['scoring'],p['_retired'],p['_last_listed']=saved[id(p)]
        MA._pe_clear()
    MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()
def adjavg(y,a): return round(a,1)   # RAW season avg (era normalization removed — #334 stage B owner ruling)
def retired_now(p):
    if delisted(p): return True
    lg=max((r['year'] for r in p['scoring'] if r.get('games',0)>=1), default=None); dy=p.get('year')
    return bool(lg is not None and dy is not None and dy<=2021 and lg<=2024)
rec={}; nsat=0
for _j,p in enumerate(players):
    if _PARENT or not _mine(_j): continue
    C=p.get('year')
    if C is None: continue
    played={x['year']:(x['games'],x['avg']) for x in p['scoring'] if x['games']>=1}
    last_active=max(played) if played else None
    rn=retired_now(p)
    # CALENDAR-YEAR-SINCE-DRAFT indexing: Yr_k = C+k whether or not played; missed year = real (pole/staleness) value.
    # ACTIVE players run through 2026 (current value); RETIRED players stop at their LISTED-THROUGH year (#338;
    # was: last played year) — blank after, no post-career floor.
    # #338 (2026-08-06): a retired player's window runs to his LISTED-THROUGH year, not his last PLAYED year —
    # the tenure years after his last game are LISTED sitting-out years and must be emitted to be priced at all.
    # Was `(last_active if last_active else C+1) if rn else 2026`; a played year is never truncated (max), and
    # a player with neither data nor tenure still falls back to the single [C+1] row on the `yrs` line below.
    yend = max(last_active or 0, _listed_through(p,max((r['year'] for r in p['scoring']), default=0)) or 0) if rn else 2026
    yend = min(yend,2026)
    yrs=list(range(C+1, yend+1)) if yend>=C+1 else [C+1]
    Vpath=[ASOF.get((id(p),y)) for y in yrs]
    Ppath=[(adjavg(y,played[y][1]) if y in played else 0.0) for y in yrs]
    anchor=ASOF.get((id(p),C+1))                          # END OF CALENDAR YEAR 1 (regardless of games) = the curve anchor
    fp=min(played) if played else None
    old_anchor=ASOF.get((id(p),fp)) if fp else None       # buggy first-PLAYED anchor (for bias comparison)
    sat=(C+1 not in played) and bool(played)
    if sat and p.get('type') in INCURVE and 2004<=C<=2024: nsat+=1
    rec[id(p)]=dict(player=p['player'],key=p.get('key'),pos=(MA.GRP.get(p.get('pos')) or MA.gfut(p)),cpos=MA.gfut(p),sw=bool(MA.GRP.get(p.get('pos')) and MA.GRP.get(p.get('pos'))!=MA.gfut(p)),type=p.get('type'),pick=MA.effpk(p),pickless=bool(p.get('_pickless')),
                    # THE SPLIT: clamp to the POOL index, not the stale KMAX literal 70. The ladder now ends at
                    # POOL_PICK, so min(effpk,70) would have been a KeyError waiting on any effpk of 66-70.
                    year=C,cat=p.get('_cat'),draftval=round(MA.PVC[min(MA.effpk(p),MA.POOL_PICK)]) if not p.get('_pickless') else None,
                    yrs=yrs,Vpath=Vpath,Ppath=Ppath,cur=ASOF.get((id(p),2026)),anchor=anchor,old_anchor=old_anchor,
                    sat_out_yr1=sat,retired_now=rn,incurve=(p.get('type') in INCURVE))
# ==== S2: worker dump / parent merge =============================================================
if _S4_SHARD:
    # a worker emits its shard keyed by STABLE key (never id()) and exits; the parent owns the file
    _shard={_stable_key(p):rec[id(p)] for _j,p in enumerate(players) if _mine(_j) and id(p) in rec}
    _own=[_stable_key(p) for _j,p in enumerate(players) if _j%_sn==_si and id(p) in rec]
    json.dump({'shard':_S4_SHARD,'own':_own,'rows':_shard},open(os.environ['S4_SHARD_OUT'],'w'))
    print('shard %s: %d rows (%d own + overlap)'%(_S4_SHARD,len(_shard),len(_own)),flush=True)
    raise SystemExit(0)
if _PARENT:
    for _i,_pr in enumerate(_procs):
        _out,_ =_pr.communicate()
        if _pr.returncode!=0:
            raise SystemExit('S4 SHARD %d/%d FAILED (rc=%s):\n%s'%(_i,_S4_WORKERS,_pr.returncode,(_out or '')[-2000:]))
    _by_key={}; _overlap_seen={}
    for _sf in _shard_files:
        _sd=json.load(open(_sf))
        for _k in _sd['own']:
            _by_key[_k]=_sd['rows'][_k]
        for _k,_v in _sd['rows'].items():
            _overlap_seen.setdefault(_k,[]).append(json.dumps(_v,sort_keys=True))
        os.unlink(_sf)
    # THE NO-TRADEOFF BAR, IN-RUN: every overlap row priced by two or more workers must agree
    # EXACTLY (the filed guard). A single disagreement kills the merge — never a quiet average.
    _dis=[_k for _k,_vs in _overlap_seen.items() if len(_vs)>1 and len(set(_vs))!=1]
    if _dis:
        raise SystemExit('S4 PARALLEL DETERMINISM FAILED: %d overlap row(s) disagree across workers: %s'
                         %(len(_dis),_dis[:5]))
    _n_over=sum(1 for _vs in _overlap_seen.values() if len(_vs)>1)
    _missing=[_stable_key(p) for p in players if p.get('year') is not None and _stable_key(p) not in _by_key]
    if _missing:
        raise SystemExit('S4 MERGE INCOMPLETE: %d player(s) unpriced: %s'%(len(_missing),_missing[:5]))
    for _j,_k in enumerate(sorted(_by_key)):
        rec[_j]=_by_key[_k]
    nsat=sum(1 for _v in rec.values() if _v['sat_out_yr1'] and _v['incurve'] and 2004<=_v['year']<=2024)
    print('S4 PARALLEL MERGE: %d rows from %d workers; %d overlap rows agreed exactly across '
          'workers (the no-tradeoff bar); stable-key ordered'%(len(rec),_S4_WORKERS,_n_over),flush=True)
_book_out=os.environ.get('S4_MATRIX','s4_matrix.json')
if _book_out=='s4_matrix.json': _SS.prepare_write('s4_matrix.json')   # clear read-only from a prior guarded build
# gate-integrity (a): embed code/store/config identity so the B1/B3 gate runner can assert the regenerated
# candidate matrix WAS produced by the candidate under test (a mismatch is a gate FAIL, not a warning). Thin
# plumbing — reads the source md5s the engine just loaded from cwd; no valuation code touched. '__meta__' is
# skipped by every matrix consumer (keys starting with '__').
def _md5f(_p):
    import hashlib as _h; _hh=_h.md5()
    with open(_p,'rb') as _f:
        for _c in iter(lambda:_f.read(1<<16),b''): _hh.update(_c)
    return _hh.hexdigest()
_matout={str(k):v for k,v in rec.items()}
# __meta__ ONLY on a non-default (gate-regen) path: the DEFAULT s4_matrix.json stays byte-identical for the
# existing consumers (F2 parity filters by 'key' — safe — but the s4_render_* tools iterate all values). The
# B1/B3 gate runner regenerates to a custom S4_MATRIX path and reads this meta; consumers skip '__'-keys.
if _book_out!='s4_matrix.json':
    try:
        import config_manifest as _CFGm; _cfg_h=_CFGm.manifest_hash()
    except Exception:
        _cfg_h=None
    _matout['__meta__']={'kind':'walk_forward_cohort_book','engine_head_md5':_md5f('_merged_recover.py'),
                         'store_md5':_md5f('rl_model_data.json'),'config_sha256':_cfg_h,'n_players':len(rec)}
json.dump(_matout, open(_book_out,'w'))
if _book_out=='s4_matrix.json':
    _bsrc=_SS.stamp_derived('s4_matrix.json',tier=1)                   # GUARD 1: stamp book with source md5 + read-only
    print(f"matrix saved (CALENDAR-indexed): {len(rec)} players | book stamped src={_bsrc[:8]} (read-only)",flush=True)
else:
    print(f"matrix saved (CALENDAR-indexed): {len(rec)} players -> {_book_out}",flush=True)
# ==== BOOK<->ENGINE(BOARD) VALUE-PARITY GATE (F2 regression tripwire, 2026-07-05) =======================
# Every book present-value (`cur`, the 2026 board-path column) MUST equal the board's gated value for that
# player -- the board is built by rl_export in a SEPARATE process/instance, so this cross-checks that the book
# has NOT re-introduced any stale valuation override (the deleted cB / double-v7 double-fade harness). Matched
# by stable key. If any active board player diverges, the build FAILS loudly. The board file must exist (build
# order: rl_export.py then s4_matrix_M1v7.py); if absent the gate is skipped with a loud warning.
_board_path=os.environ.get('RL_APP_DATA','rl_app_data.json')
# L7 NUMÉRAIRE (baked 2026-07-13): the board DISPLAYS round(ev/F) (engine ev()/book cur UNCHANGED — the
# re-base is board-display only). So the F2 book<->board parity holds in the numéraire: board v ==
# round(book cur / F). F is the certified 1.0524. (In ship_gates the matrix regen runs before any board
# exists, so this gate is skipped there; it fires when the board is built first, e.g. the correction canary.)
_F_num=json.load(open('pick_redenomination.json'))['factor'] if os.path.exists('pick_redenomination.json') else 1.0524
if os.path.exists(_board_path):
    _bd={r['key']:r['v'] for r in json.load(open(_board_path)).get('active',[])}
    _bookcur={v['key']:v['cur'] for v in rec.values() if v.get('key')}
    # board players legitimately ABSENT from the cohort book: _pvc_exclude records are excluded by eligible()
    # above (they never join the pick-value cohort). They are still valid board players -- just outside this
    # walk-forward book -- so absence is NOTED, not a parity failure. A VALUE mismatch on a shared player IS a
    # failure (that is the double-fade / stale-override signature).
    _absent=sorted(_k for _k in _bd if _k not in _bookcur)
    _pf=[(_k,_bookcur[_k],_bd[_k]) for _k in _bd if _k in _bookcur and int(round(_bookcur[_k]/_F_num))!=_bd[_k]]
    if _pf:
        raise SystemExit("BOOK<->BOARD PARITY GATE FAILED: %d present-value mismatches (board v != round(book cur / %.4f), numéraire):\n  "%(len(_pf),_F_num)
                         + "\n  ".join("%s: book_cur=%s board=%s"%(k,c,b) for k,c,b in _pf[:25]))
    print(f"BOOK PARITY GATE PASS: all {len(_bd)-len(_absent)} shared board players' present value == round(book cur / {_F_num:.4f}) [numéraire]; {len(_absent)} board players outside the cohort book (_pvc_exclude): {_absent}",flush=True)
else:
    print(f"WARN: {_board_path} not found -> BOOK<->BOARD parity gate SKIPPED (build the board first: rl_export.py)",flush=True)
# ---- mapping-only proof: a played value is identical old vs new (just a different slot) ----
camp=[v for v in rec.values() if 'seth campbell' in v['player'].lower()][0]
print(f"\nMAPPING-ONLY PROOF — Seth Campbell: yrs={camp['yrs']} Vpath={[round(x) if x else None for x in camp['Vpath']]}")
print(f"  new anchor (calendar Yr1 {camp['year']+1}, no games)={round(camp['anchor'])}; the 465 first-played value now sits at its correct slot {camp['yrs'].index(2024)+1 if 2024 in camp['yrs'] else '?'} (Yr2)")
# ---- CURVE-ANCHOR BIAS (2004-2024 ND+RD) ----
elig=[v for v in rec.values() if v['incurve'] and 2004<=v['year']<=2024]
sat=[v for v in elig if v['sat_out_yr1'] and v['anchor'] and v['old_anchor']]
deltas=[v['old_anchor']-v['anchor'] for v in sat]
print(f"\nCURVE-ANCHOR BIAS (2004-2024 ND+RD, n={len(elig)}):")
print(f"  sat out draft Yr1: {nsat} players ({round(100*nsat/len(elig))}% of curve pool)")
print(f"  over-valuation when anchored at first-played vs real Yr1: total={round(sum(deltas))} SCAR, mean=+{round(np.mean(deltas))}, median=+{round(np.median(deltas))}")
old_sum=sum(v['old_anchor'] for v in elig if v['old_anchor']); new_sum=sum(v['anchor'] for v in elig if v['anchor'])
print(f"  whole-pool anchor sum: buggy={round(old_sum)} -> fixed={round(new_sum)}  ({round(100*(old_sum-new_sum)/old_sum,1)}% lower overall)")
# THE SPLIT: report-only bands. The last band was 41-80 — a label past the end of the curve. National bands now
# stop at 64 and the pool is reported as itself, since selection order inside it carries no value.
for lo,hi,_lab in [(1,20,'picks 1-20'),(21,40,'picks 21-40'),(41,MA.ND_CURVE_LAST,'picks 41-%d'%MA.ND_CURVE_LAST),
                   (MA.POOL_PICK,MA.POOL_PICK,'pool')]:
    s=[v for v in sat if lo<=v['pick']<=hi]
    if s: print(f"  {_lab}: {len(s)} sat-out, mean over-val +{round(np.mean([v['old_anchor']-v['anchor'] for v in s]))} ({round(100*np.mean([(v['old_anchor']-v['anchor'])/v['anchor'] for v in s]))}% of real Yr1)")
