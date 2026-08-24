# CANONICAL v4 build (cont.19): forward-realised target (best-3 >=Y, completeness-weighted current year) + draft rows (bust-inclusive) + STORE-SOURCED age + games-weighted recency. Produces peak_model_v4.pkl. Run: python3 build_peak_model_v4.py (needs rl_after engine + bust_prior_table.json).
# L4 (#290, 2026-07-31) — three fixes, each reproduced at source before it was made:
#   (1) dob_corrected.json is RETIRED AS AN INPUT CLASS (Addendum 1). It was untracked anywhere in the repo, so
#       bootstrap never copied it and this build could not run at all. Ages now come from the store's _by/_bd.
#   (2) bust_prior_table.json read from .../rl_after/ — where bootstrap.sh actually copies it — not
#       .../forward_valuation/. A one-token path fix; the file was never at the old path.
#   (3) the PVC snapshot loop was range(1,100) against a 65-key live PVC: KeyError at 66, reproduced. It now
#       derives its domain from MA.PVC and ASSERTS the ruled shape (1..64 + pool index 65) so a domain change
#       is loud instead of silent.
# Plus the AGE-SOURCE CENSUS (Addendum 4, a hard L4 acceptance) and the TRAINING-STORE STAMPS on every emitted
# artifact — see the blocks so headed below.
import sys, os
# rl_model provenance (fv-provenance remediation 2026-07-20): hardcoded /home/claude/rl_after insert REMOVED;
# rl_model resolves through the configured environment only (already-imported, else RL_REPO checkout).
if 'rl_model' not in sys.modules and os.environ.get('RL_REPO'):
    _rl_ra = os.path.join(os.environ['RL_REPO'], 'engine', 'rl_after')
    if os.path.isdir(_rl_ra): sys.path.insert(0, _rl_ra)
os.environ.setdefault('RL_GAMMA','1.0'); os.environ.setdefault('RL_PICK1','3000')
import io,contextlib,json,pickle,collections,hashlib
with contextlib.redirect_stdout(io.StringIO()): import rl_model as MA
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
MA.P_HOOK=None; MA.PROD_GATE='off'
allp=[p for p in MA.data if MA.GRP.get(p['pos'])]
POSI={'MID':0,'SD':1,'SF':2,'KPD':3,'KPF':4,'RUCK':5}
# ---- OUTPUT ROOTS (REBAKE ARM 1, 2026-08-24 — ruled at register v831/v833: "fix build_peak_model_v4's
#      two output paths"). BOTH blind design studies spent most of their forensic budget on the same
#      embarrassing detail: THIS SCRIPT ALREADY WRITES EXACTLY THE RIGHT PROVENANCE STAMP, and writes it
#      to /home/claude/rl_workspace/rl_after/ — outside the repository, not seeded in a fresh container,
#      where nothing can read it, assert it, or commit it (study A §3.5 "The sibling's stamp does not
#      exist to read"; study B M-17). The two paths are training_store_stamp.json and
#      age_source_census.json. They are now REPO-ANCHORED: they land in <RL_REPO>/data/model_provenance/,
#      beside the estate, where boot_guard and the release manifest can reach them.
#      _ARM_OUT (RL_ARM1_OUT) redirects the whole emission set — model, snapshot, stamp and census — to a
#      CANDIDATE directory, so a candidate can be built without overwriting a pinned live artifact.
#      UNSET reproduces the shipped emission targets for the pickle and the snapshot exactly.
#      REBAKE ARM 2 (2026-08-24) GENERALISES THE NAME RATHER THAN ADDING A SECOND RESOLVER: RL_ARM2_OUT
#      is read at the SAME site with the SAME meaning, so each arm can emit its own candidate set without
#      a per-arm code path accumulating here. Both are PATH vars (config_manifest.INFRA_ALLOW class):
#      they name WHERE an artifact is written, carry no model semantics, and are not in the value hash,
#      so config_sha256 does not move. UNSET (either name) still reproduces the shipped emission targets.
_ARM_OUT=os.environ.get('RL_ARM2_OUT') or os.environ.get('RL_ARM1_OUT') or None
def _repo_out(name):
    """Where a PROVENANCE artifact goes. Candidate dir if one is declared, else the repo (never the
    out-of-repo workspace this script wrote to for its whole life), else the legacy workspace path as a
    last resort so the script still runs with no RL_REPO bound."""
    if _ARM_OUT: return os.path.join(_ARM_OUT,name)
    _r=os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR')
    if _r:
        _d=os.path.join(_r,'data','model_provenance'); os.makedirs(_d,exist_ok=True)
        return os.path.join(_d,name)
    return '/home/claude/rl_workspace/rl_after/'+name
def _art_out(name,shipped):
    """Where a FITTED artifact goes. Candidate dir if declared, else the shipped path, byte-for-byte."""
    return os.path.join(_ARM_OUT,name) if _ARM_OUT else shipped
if _ARM_OUT: os.makedirs(_ARM_OUT,exist_ok=True)
# bust_prior_table is an INPUT. Repo-anchored first (the committed single source), then the workspace
# copy bootstrap.sh seeds — L4 fix (2) kept, with the checkout ahead of the mutable shared workspace.
_BUST_PATH=next((_p for _p in (
    os.path.join(os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '',
                 'engine','rl_after','bust_prior_table.json'),
    '/home/claude/rl_workspace/rl_after/bust_prior_table.json') if _p and os.path.exists(_p)), None)
if _BUST_PATH is None:
    raise SystemExit('build_peak_model_v4 HALT: bust_prior_table.json not found under <RL_REPO>/engine/'
                     'rl_after/ or the seeded workspace — it is a TRAINING INPUT to this model.')
PT=json.load(open(_BUST_PATH))
SEASON=22  # reference full home-and-away
def bp(pos,pick): return PT[pos][str(min(max(int(round(pick)),1),70))]
def best(ss,n): a=sorted([x['avg'] for x in ss if x['games']>=6],reverse=True)[:n]; return float(np.mean(a)) if a else None
def by_corr(p): return p.get('_by')   # L4 fix (1): the store is the single source; dob_corrected.json is retired
def age_at(p,Y): by=by_corr(p); return (Y-by) if by else (Y-(MA.debut(p)-18))

# ---- THE AGE-SOURCE CENSUS (Addendum 4 — a hard L4 acceptance) ----------------------------------
# Every TRAINING ROW is classified by the PROVENANCE of the age feature it carries, and the classes must
# SUM TO THE TRAINING POPULATION — a census that does not sum HALTs. This is what makes silent defaulting
# arithmetically impossible: never-played rows were never *excluded*, they trained with the fallback age
# 18.0 + years-since-debut, an included-with-a-guessed-age distortion frozen inside the current model.
# Busts ARE counted (BUST RULING consequence 4): the census counts AGE PROVENANCE, not outcome.
# _bd is an exact subset of _by in this store (848/848 measured), so REAL_DATE implies _by is present too.
def age_source(p):
    if p.get('_bd'): return 'REAL_DATE'    # exact date of birth in the store
    if p.get('_by'): return 'REAL_YEAR'    # year only — a first-class store state (Addendum A.2)
    return 'FALLBACK'                      # 18.0 + years-since-debut: a guessed age, now counted
_CENSUS=collections.Counter(); _CENSUS_PLAYERS=collections.defaultdict(set)
# *** target now includes year Y (>=Y), with the current/partial year weighted by completeness ***
def fwd_peak(p,Y):
    fut=[x for x in p['scoring'] if x['year']>=Y and x['games']>=6]
    if not fut: return None
    # weight each season by completeness (games/SEASON, capped 1) so a partial current year counts less
    w=np.array([min(x['games'],SEASON)/SEASON for x in fut]); a=np.array([x['avg'] for x in fut])
    idx=np.argsort(-a)[:3]; return float(np.average(a[idx],weights=w[idx]))
def feats(p,Y):
    d=MA.debut(p); pos=MA.GRP[p['pos']]; ep=MA.effpk(p); T=Y-d+1
    sub=[x for x in p['scoring'] if x['year']<=Y]; g=sum(x['games'] for x in sub); nss=len([x for x in sub if x['games']>=6])
    b2=best(sub,2); b1=best(sub,1); maxg=max([x['games'] for x in sub],default=0)
    rs=[x for x in sub if x['games']>=6][-2:]  # recency: games-weighted (partial current year down-weighted)
    recent=float(np.average([x['avg'] for x in rs],weights=[x['games'] for x in rs])) if rs else 0
    last=[x for x in sub if x['year']==Y]; la=last[0]['avg'] if last else 0; lg=last[0]['games'] if last else 0
    early=sum(x['games'] for x in sub if x['year']-d+1<=2); seq=[x['avg'] for x in sub if x['games']>=6]; slope=(seq[-1]-seq[0]) if len(seq)>1 else 0.0
    bestyr=max([x['year'] for x in sub if x['games']>=6 and x['avg']==(b1 or -1)],default=Y); ysb=Y-bestyr
    return [np.log(MA.PVC[ep]),ep,POSI[pos],b2 or 0,b1 or 0,recent,la,lg,g,nss,maxg,early,slope,ysb,age_at(p,Y),T,bp(pos,ep)]
def draft_feat(p):
    pos=MA.GRP[p['pos']]; ep=MA.effpk(p); return [np.log(MA.PVC[ep]),ep,POSI[pos],0,0,0,0,0,0,0,0,0,0,0,age_at(p,MA.debut(p)-1),0,bp(pos,ep)]
def build(lo,hi):
    X,y=[],[]
    for p in allp:
        d=MA.debut(p)
        if d<lo or d>hi: continue
        _cls=age_source(p)
        X.append(draft_feat(p)); y.append(best([x for x in p['scoring']],3) or 0.0)
        _CENSUS[_cls]+=1; _CENSUS_PLAYERS[_cls].add(p['player'])   # the draft row counts too
        for Y in sorted(set(x['year'] for x in p['scoring'] if x['games']>0)):
            if len([x for x in p['scoring'] if x['year']>Y and x['games']>=6])>=1:   # >=1 FUTURE season (so it's forward, not echo)
                t=fwd_peak(p,Y)
                if t is not None:
                    X.append(feats(p,Y)); y.append(t)
                    _CENSUS[_cls]+=1; _CENSUS_PLAYERS[_cls].add(p['player'])
    return np.array(X),np.array(y)
def r2(pr,yy): return 1-np.sum((yy-pr)**2)/np.sum((yy-yy.mean())**2)
Xtr,ytr=build(2006,2015)
m=HistGradientBoostingRegressor(max_iter=600,max_depth=5,learning_rate=0.04,min_samples_leaf=30,l2_regularization=2.0,random_state=0).fit(Xtr,ytr)
Xte,yte=[],[]
for p in allp:
    d=MA.debut(p)
    if not(2016<=d<=2019): continue
    for Y in sorted(set(x['year'] for x in p['scoring'] if x['games']>0)):
        if len([x for x in p['scoring'] if x['year']>Y and x['games']>=6])>=2:
            t=fwd_peak(p,Y)
            if t is not None: Xte.append(feats(p,Y)); yte.append(t)
print('forward-peak R2 (out-of-sample, target now >=Y w/ completeness weight): %.3f'%r2(m.predict(np.array(Xte)),np.array(yte)))
print('\nsurvivorship (draft proj late picks>30):')
for pos in ['MID','SD','SF','KPD','KPF','RUCK']:
    pl=[p for p in allp if MA.GRP[p['pos']]==pos and MA.effpk(p)>30 and 2006<=MA.debut(p)<=2018]
    act=np.mean([best([x for x in p['scoring']],3) or 0 for p in pl]); dr=np.mean([m.predict([draft_feat(p)])[0] for p in pl])
    print('  %-9s actual %.1f draft-proj %.1f (%+.0f%%)'%(pos,act,dr,100*(dr-act)/max(act,1)))
spec=[p for p in allp if MA.effpk(p)>20 and 2006<=MA.debut(p)<=2016 and sum(x['games'] for x in p['scoring'] if x['year']<=MA.debut(p)+2)>=20 and best([x for x in p['scoring']],3)]
print('Kondogiannis bias: %+.1f'%np.mean([(best([x for x in p['scoring']],3))-m.predict([feats(p,MA.debut(p)+2)])[0] for p in spec]))
_PKL_SRC=_art_out('peak_model_v4.pkl','/home/claude/rl_workspace/forward_valuation/peak_model_v4.pkl')
pickle.dump({'model':m,'fnames':['logPVC','effpk','pos','best2','best1','recent_gw','last_avg','last_g','games','nss','maxg','early','slope','yrs_since_best','age','T','bust_prior']},open(_PKL_SRC,'wb'))
# CO-EMIT the TRAIN-TIME PVC snapshot (Phase-4 disposition, DPP-strip build). The logPVC feature above is
# np.log(MA.PVC[ep]); inference (rl_model._v4_init) must read the SAME PVC as a FROZEN feature to break the
# SCALE<->PVC<->peak_est bootstrap cycle. pvc_snapshot.json is therefore a DERIVED artifact of THIS build, not a
# hand-checked-in file -- the model and its train-time PVC are now co-generated so they can never drift apart
# (the report's flagged "next hidden-copy risk"). Emitted read-only + provenance-stamped by the build.
import os as _os, stat as _st, shutil as _sh
# L4 fix (3): the domain is DERIVED from the live PVC, not a literal. It was range(1,100) against a 65-key
# PVC — KeyError at 66, reproduced at source before this change. The ruled post-split shape is picks 1..64
# plus the pool at index 65; the assert makes a domain change LOUD rather than silently reshaping a pinned
# artifact (the I.2 lesson: assert the agreement, or remove the default so the read fails loud).
_pvc_keys=sorted(int(k) for k in MA.PVC)
assert _pvc_keys==list(range(1,66)), (
    'PVC domain moved: expected the ruled 1..64 + pool index 65 (65 keys), measured %d keys %r..%r'
    % (len(_pvc_keys), _pvc_keys[:3], _pvc_keys[-3:]))
_snap={str(k):float(MA.PVC[k]) for k in _pvc_keys}
_snap_path=_art_out('pvc_snapshot.json','/home/claude/rl_workspace/rl_after/pvc_snapshot.json')
_pkl_src=_PKL_SRC
_pkl_dst=_art_out('peak_model_v4.pkl','/home/claude/rl_workspace/rl_after/peak_model_v4.pkl')
try: _os.chmod(_snap_path, _st.S_IWUSR|_st.S_IRUSR|_st.S_IRGRP|_st.S_IROTH)
except Exception: pass
json.dump(_snap, open(_snap_path,'w'))
try:
    if _os.path.abspath(_pkl_src)!=_os.path.abspath(_pkl_dst):
        _sh.copyfile(_pkl_src,_pkl_dst)   # place the pkl where rl_model actually reads it (co-located tier-2 caches)
except Exception: pass

# ---- THE AGE-SOURCE CENSUS, EMITTED AND COUNTED (hard L4 acceptance) ----------------------------
# Totals must sum to the training population. They are asserted here, not reported and hoped over.
_STORE_PATH=os.path.join(os.path.dirname(MA.__file__),'rl_model_data.json')
_store_md5=hashlib.md5(open(_STORE_PATH,'rb').read()).hexdigest()
try: _V0SURF_MD5=hashlib.md5(open(os.path.join(os.environ.get('RL_REPO',''),'data','v0surf.pkl'),'rb').read()).hexdigest()
except Exception: _V0SURF_MD5='UNREADABLE'
try: _CURVE_PAYLOAD=json.load(open(os.path.join(os.path.dirname(MA.__file__),'pvc_curve_v2.json')))['payload_md5']
except Exception:
    try: _CURVE_PAYLOAD=hashlib.md5(json.dumps({str(k):int(round(MA.PVC[k])) for k in _pvc_keys[:64]},sort_keys=True).encode()).hexdigest()[:8]
    except Exception: _CURVE_PAYLOAD='UNREADABLE'
_train_total=int(len(ytr))
_cen={k:int(_CENSUS.get(k,0)) for k in ('REAL_DATE','REAL_YEAR','FALLBACK')}
_cen_sum=sum(_cen.values())
assert _cen_sum==_train_total, ('AGE-SOURCE CENSUS does not sum: %d classified != %d training rows'
                                % (_cen_sum, _train_total))
# store-level counts, for comparison against the Addendum 4 baseline (2,651 / 2,349 / 848 / 302)
_all_store=[p for p in MA.data]
_trained_players={n for s in _CENSUS_PLAYERS.values() for n in s}
_store_cen={'store_rows':len(_all_store),
            'by_present':sum(1 for p in _all_store if p.get('_by')),
            'bd_present':sum(1 for p in _all_store if p.get('_bd')),
            'by_missing':sum(1 for p in _all_store if not p.get('_by'))}
_store_cen['bd_is_subset_of_by']=all(p.get('_by') for p in _all_store if p.get('_bd'))
_census_doc={
 '_doc':('AGE-SOURCE CENSUS (Addendum 4, hard L4 acceptance). Every TRAINING ROW classified by the '
         'provenance of its age feature; classes SUM to the training population or the build HALTs. '
         'REAL_DATE = store _bd; REAL_YEAR = store _by only (a first-class state, Addendum A.2); '
         'FALLBACK = 18.0 + years-since-debut, a guessed age. Busts are COUNTED — the census counts age '
         'provenance, not outcome (BUST RULING consequence 4).'),
 'substrate':{'store_md5':_store_md5,'v0surf_md5':_V0SURF_MD5,'gamma':float(MA.GAMMA)},
 'training_rows':{'total_denominator':_train_total,'by_class':_cen,
                  'sums_to_denominator':bool(_cen_sum==_train_total)},
 'training_players':{k:len(_CENSUS_PLAYERS.get(k,()))for k in ('REAL_DATE','REAL_YEAR','FALLBACK')},
 'training_players_total':len(_trained_players),
 'store_level':_store_cen,
 'excluded_from_training':{'store_rows_not_trained':len(_all_store)-len(_trained_players),
                           '_note':'excluded by the debut window (2006-2015) or by an unmapped position; '
                                   'the census denominator is the TRAINING population, not the store'},
 'WATCHED_NUMBER_fallback':{'rows':_cen['FALLBACK'],'of':_train_total,
                            'pct':round(100.0*_cen['FALLBACK']/_train_total,3) if _train_total else None,
                            '_note':'must fall by EXACTLY the number of rows the DOB courier writes'},
}
_census_path=_repo_out('age_source_census.json')   # OUTPUT PATH 1 of 2, now in-repo (ARM 1)
json.dump(_census_doc, open(_census_path,'w'), indent=1, sort_keys=True)
print('AGE-SOURCE CENSUS: %s = %d of %d training rows (sums OK); fallback %.3f%%'
      % (_cen, _cen_sum, _train_total, 100.0*_cen['FALLBACK']/max(_train_total,1)))

# ---- TRAINING-STORE STAMPS (L4 act 6) -----------------------------------------------------------
# Today cm_400, q97m, peak_model_v4, pvc_snapshot and bust_prior_table are pinned by md5 and NONE records
# the store or curve it was trained on. A stamp beside each closes that for good: an md5 says "this is the
# artifact I expect", a stamp says "and here is the world it was fitted in".
_stamp={'_doc':'TRAINING-STORE STAMP (L4 act 6, #290). What this build was fitted ON.',
        'store_md5':_store_md5,'v0surf_md5':_V0SURF_MD5,'gamma':float(MA.GAMMA),
        'pvc_domain':[_pvc_keys[0],_pvc_keys[-1]],'pvc_n_keys':len(_pvc_keys),
        'curve_payload_md5':_CURVE_PAYLOAD,'training_rows':_train_total,
        'training_window_debut':[2006,2015],'built_by':'build_peak_model_v4.py',
        'artifacts':{}}
for _nm,_pth in (('peak_model_v4.pkl',_pkl_dst),('pvc_snapshot.json',_snap_path),
                 ('bust_prior_table.json',_BUST_PATH),('age_source_census.json',_census_path)):
    try: _stamp['artifacts'][_nm]=hashlib.md5(open(_pth,'rb').read()).hexdigest()
    except Exception as _e: _stamp['artifacts'][_nm]='UNREADABLE: %r'%(_e,)
_stamp_path=_repo_out('training_store_stamp.json')   # OUTPUT PATH 2 of 2, now in-repo (ARM 1)
json.dump(_stamp, open(_stamp_path,'w'), indent=1, sort_keys=True)
print('TRAINING-STORE STAMP: store %s · v0surf %s · gamma %s · %d rows -> %s'
      % (_store_md5[:8], _V0SURF_MD5[:8], MA.GAMMA, _train_total, _stamp_path))
if _ARM_OUT:
    # CANDIDATE mode: the tier-2 frozen stamp is the LIVE artifact's seal (it marks the file the engine
    # loads read-only and records its source md5). A candidate is not that file and must not be sealed as
    # though it were — the stamp would name a live artifact that this run did not write.
    print('CANDIDATE emission -> %s (peak_model_v4.pkl + pvc_snapshot.json); tier-2 freeze stamp NOT '
          'applied: a candidate is not the loaded artifact'%_ARM_OUT)
else:
    try:
        import single_source as _SS   # /home/claude/rl_after on sys.path (line 2) -> tier-2 frozen stamp + read-only
        _SS.stamp_tier2_frozen('pvc_snapshot.json'); _SS.stamp_tier2_frozen('peak_model_v4.pkl')
        print('co-emitted + tier-2-stamped pvc_snapshot.json (train-time PVC) + peak_model_v4.pkl (read-only)')
    except Exception as _e:
        _os.chmod(_snap_path, _st.S_IRUSR|_st.S_IRGRP|_st.S_IROTH)
        print('co-emitted pvc_snapshot.json (train-time PVC, read-only) — %d picks (stamp skipped: %s)'%(len(_snap),_e))
# ===== WIRE-CHECK: do proven guns recover now the current year counts? =====
MA.BASE_REF=2026; MA.AGE_REF=2026; orig=MA.peak_est
def pev4(p):
    if MA.BASE_REF-MA.debut(p)+1<1: return float(m.predict([draft_feat(p)])[0])
    return float(m.predict([feats(p,MA.BASE_REF)])[0])
act=[p for p in allp if not p.get('_retired') and max([r['year'] for r in p['scoring'] if r['games']>0] or [0])>=2025]
print('\n=== control vs v4(>=Y) value, key players ===')
for nm in ['Sean Darcy','Tom Barrass','Brennan Cox','Josh Treacy','Max Holmes','Nick Daicos','Riley Thilthorpe']:
    p=next((x for x in act if x['player']==nm),None)
    if not p: continue
    MA.peak_est=orig; c=MA.value(p); MA.peak_est=pev4; v=MA.value(p)
    print('  %-18s | ctrl %6d  v4 %6d  %+5.0f%%'%(nm,c,v,100*(v-c)/max(c,1)))
MA.peak_est=orig; C={p['player']:MA.value(p) for p in act}; MA.peak_est=pev4; V={p['player']:MA.value(p) for p in act}
proven=[p for p in act if best([x for x in p['scoring']],3) and p.get('games',0)>=80]
dd=[100*(V[p['player']]-C[p['player']])/max(C[p['player']],1) for p in proven if C[p['player']]>50]
big=[p['player'] for p in proven if abs((V[p['player']]-C[p['player']])/max(C[p['player']],1))>1.0]
print('PROVEN active (>=80g, n=%d): median move %+.1f%% (was -7.1%% with strictly-after); |move|>100%%: %d %s'%(len(dd),np.median(dd),len(big),big[:6]))
print('saved peak_model_v4.pkl')
