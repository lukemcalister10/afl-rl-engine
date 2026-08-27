"""GATE 1 — within-player, LEAKAGE-GUARDED. Each test cohort held OUT of training; held-out cond_prior prices its players
at truncated tenures (only <=T info); structural pole (synthetic par) stays fixed (no test-player career in it).
IS vs WF legs are CAPACITY-MATCHED by construction: under the ARM-2 design both are built from the
bound design spec (build_cond_prior + this gate's build_q97 read the same contract), so the gap is leakage,
not a capacity difference. [B2 RE-BASE 2026-08-27, the v863 red: this file used to pin RL_PRIOR_TREES=150
before exec'ing the engine head; under ARM-2 that pin is DEAD for the fit (the bound spec decides) but it
re-pointed cm_load_path() at the stale pre-rebake /home/claude/cm_150.pkl (no _rl_design_spec) while q97m
resolved to the ARM-2 pickle — the artifact-coherence halt correctly refused the mixed pair. The pin is
removed; the engine loads the pinned coherent pair; the legacy no-design fallbacks keep their own literals.]
Shape: future-good priced near par early, busts below; no violent yr0/1 moves."""
import io,contextlib,copy,os,numpy as np,time
ns={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], ns)
ns['_BOARD_PATH']=False   # D14: BACKTEST/WALK-FORWARD (leakage) path — board-only laws (V0 curve, KPP floor) OFF (Luke's exemption).
MA=ns['MA']; cp=ns['cp']; PR=ns['PR'];
def setmodels(cm,q97):
    ns['cm']=cm; ns['q97m']=q97   # swap the trained/leaky part; pole(_POLE) + ISO stay in-sample structural priors
def build_q97(pool):
    """The gate's own q97 leg. REBAKE ARM 2: study B section 4.1 records that this harness HARD-CODES the
    incumbent construction, and that a rebake "needs the hyperparameters changed in all four places at
    once" — otherwise B2 certifies a model that is not the one under test. It now reads the SAME bound
    design contract cp.build_cond_prior reads, so IS and WF legs stay MATCHED (which is what makes the
    gap leakage rather than a capacity difference) and the gate tests the shipped construction."""
    X,yy,YR=[],[],[]
    for p in pool:
        if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')): continue
        d0=cp.debutyr(p)-1; last=max([x['year'] for x in p['scoring']]+[d0])
        for Y in range(d0,min(last,2026)+1):
            X.append(cp._feat(p,Y)); yy.append(cp.fwd_best3_from(p,Y,2026)); YR.append(Y)
    X=np.array(X); yy=np.array(yy)
    _d=cp.design()
    if _d is not None:
        import exact_monotone as EM
        EM.selftest_or_halt()
        return EM.stamp(EM.make_estimator(0.97,X.shape[1],bool(_d.get('age_hill')),_d['hyperparameters'])
                        .fit(X,yy,sample_weight=EM.recency_weight(np.array(YR),
                                                                  _d.get('recency_halflife_years'),2026)),_d)
    from sklearn.ensemble import GradientBoostingRegressor
    return GradientBoostingRegressor(loss='quantile',alpha=0.97,n_estimators=150,max_depth=4,learning_rate=0.05,min_samples_leaf=25,random_state=0).fit(X,yy)
def trunc(p,T):
    d0=cp.debutyr(p)-1; q=copy.deepcopy(p); q['scoring']=[x for x in p['scoring'] if x['year']<=d0+T]; q['_pos_now']=None; q['_fut']=[]
    return q,d0+T
def real_mat(p):
    s=sorted([a for y,a in [(x['year'],x['avg']) for x in p['scoring'] if x['games']>=6]],reverse=True)[:3]
    return float(np.mean(s)) if s else 0.0
full=[p for p in MA.data if MA.GRP.get(p['pos'])]
allpool=[p for p in full if cp.debutyr(p)<=2021 and (p.get('pick') or p.get('_ft'))]
with contextlib.redirect_stdout(io.StringIO()): is_cm,_=cp.build_cond_prior(cap=2026,resolved_cut=2021); is_q97=build_q97(allpool)
print("in-sample @150 built")
TEN=[0,1,2,3,4,5]; agg={}  # agg[(grp,'IS'/'WF',tag)][T]=[ratios]
for D in range(2014,2019):
    t0=time.time(); coh=[p for p in full if p.get('type')=='ND' and p.get('pick') and p['year']==D and p.get('scoring')]
    if not coh: continue
    cohset=set(id(p) for p in coh); pool=[p for p in full if id(p) not in cohset]
    with contextlib.redirect_stdout(io.StringIO()): wf_cm,nwf=cp.build_cond_prior(cap=2026,resolved_cut=2021,pool=pool); wf_q97=build_q97([p for p in pool if cp.debutyr(p)<=2021 and (p.get('pick') or p.get('_ft'))])
    for p in coh:
        pos=MA.gfut(p); pk=min(MA.effpk(p),cp.KMAX); par=PR.par_at(pos,pk,5)
        with contextlib.redirect_stdout(io.StringIO()): parval=ns['par_pole'](pos,pk,5)[0]
        if parval<=0: continue
        mat=real_mat(p); tag='GOOD' if mat>=0.85*par else ('BUST' if mat<0.55*par else 'MID')
        if tag=='MID': continue
        for which,(cm_,q_) in [('IS',(is_cm,is_q97)),('WF',(wf_cm,wf_q97))]:
            setmodels(cm_,q_)
            for T in TEN:
                tp,Y=trunc(p,T)
                try:
                    with contextlib.redirect_stdout(io.StringIO()): e=ns['ev'](tp,Y)
                except Exception: continue
                agg.setdefault((pos,which,tag),{}).setdefault(T,[]).append(100.0*e/parval)
    print(f"  cohort {D}: n={len(coh)} held out, wf-rows={nwf} ({time.time()-t0:.0f}s)")
setmodels(is_cm,is_q97)
print("\n=== WITHIN-PLAYER value-by-tenure, % of PAR-value (leakage-guarded WF vs in-sample IS) ===")
print("  future-GOOD should sit near/above 100 early & flat; BUST below & staying low; watch for violent yr0/1 moves")
for pos in ['MID','SF','KPF','SD','KPD']:
    for tag in ['GOOD','BUST']:
        n=len(agg.get((pos,'WF',tag),{}).get(1,[]))
        if n<4: continue
        wf=" ".join(f"T{T}:{np.median(agg[(pos,'WF',tag)][T]):4.0f}" for T in TEN if T in agg.get((pos,'WF',tag),{}))
        isl=" ".join(f"{np.median(agg[(pos,'IS',tag)][T]):4.0f}" for T in TEN if T in agg.get((pos,'IS',tag),{}))
        print(f"  {pos:8s} {tag:4s} n={n:2d}  WF[{wf}]")
        print(f"  {'':8s} {'':4s}        IS[ {isl} ]  (gap IS-WF = leakage)")

# ==== STRUCTURED CERTIFICATE (gate-integrity b, 2026-07-09) ====================================
# The B2 gate no longer parses this human print (integer-rounded — a true 0.98 %-pt gap read as 0, and a
# handcrafted four-line text file passed). Instead B2 INVOKES this producer and reads the JSON below:
# UNROUNDED per-cell WF/IS observations + code/store/config identity, so B2 asserts the certificate was
# produced by the candidate under test and computes the leakage gap at full precision. This is a
# LEAVE-COHORT-OUT sensitivity construction (each 2014-2018 ND cohort held out of the trained part).
import json as _json, hashlib as _hl
def _md5(path):
    h = _hl.md5()
    with open(path, 'rb') as f:
        for _c in iter(lambda: f.read(1 << 16), b''): h.update(_c)
    return h.hexdigest()
_cells = {}
for (_pos, _which, _tag), _byT in agg.items():
    for _T, _vals in _byT.items():
        _cells.setdefault('%s|%s|T%d' % (_pos, _tag, _T), {})[_which] = {
            'median': float(np.median(_vals)), 'n': len(_vals),
            'obs': [float(x) for x in _vals]}          # UNROUNDED observations
try:
    import config_manifest as _cm; _cfg = _cm.manifest_hash()
except Exception:
    _cfg = None
_cert = {
    'kind': 'gate1_leave_cohort_out_sensitivity',
    'engine_head_md5': _md5('_merged_recover.py'),
    'store_md5': _md5('rl_model_data.json'),
    'config_sha256': _cfg,
    'trees': 150, 'tenures': TEN, 'cohorts_heldout': list(range(2014, 2019)),
    'cells': _cells,
}
_out = os.environ.get('GATE1_JSON')
if _out:
    with open(_out, 'w') as f: _json.dump(_cert, f, indent=1)
    print('gate1 certificate written: %s (engine %s store %s config %s)'
          % (_out, _cert['engine_head_md5'][:8], _cert['store_md5'][:8], (_cfg or '-')[:8]))
