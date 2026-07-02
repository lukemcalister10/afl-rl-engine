"""BAND REDESIGN (components 2-3 of the proposal), built on conditional_prior (component 1).
Replaces the band construction in dist_value: NO peak_est-relocation, NO max-of-anchors. Instead a CONTINUOUS reliability-
weighted blend of:
  - the CONDITIONAL PRIOR band  (component 1: resolved-calibrated, asymmetric, games/tenure-conditional pedigree+opportunity)
  - the OWN DEMONSTRATED band   (component 2: recency-weighted recent level = recent_best2 +- the player's own season spread)
weighted by RELIABILITY         (component 3: effective full-seasons of evidence, lightly recency-decayed).
  band = w*own + (1-w)*prior,  w = r/(r+K_REL).   Priced via the SAME v_at_peak chain (the convex VOR baseline stays).
Stability by design: own-band is anchored to demonstrated production (slow-moving) and the blend is continuous (no max
switching), so a thin/partial sample earns its move gradually. Proven players -> w~1 -> own-band -> ~ value().
  Run: cd rl_after && PYTHONHASHSEED=0 python3 ../forward_valuation/dist_redesign.py
"""
import sys; sys.path.insert(0,'/home/claude/rl_after')
import os; os.environ.setdefault('RL_GAMMA','0.85'); os.environ.setdefault('RL_PICK1','3000')
import io,contextlib,numpy as np,copy
import importlib.util
def _load(name,path):
    s=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(s)
    with contextlib.redirect_stdout(io.StringIO()): s.loader.exec_module(m); return m
_HERE=os.path.dirname(__file__)
dp=_load('dp',os.path.join(_HERE,'distribution_pricing.py'))
cp=_load('cp',os.path.join(_HERE,'conditional_prior.py'))
MA=dp.MA

ZQ=np.array([-1.2816,-0.5244,0.0,0.5244,1.2816])    # normal quantiles for Q=.1/.3/.5/.7/.9 (own-band shape)
# ---- SURFACED DIALS (Luke sets these watching the repriced output; none baked) ----
REPL_DROP_PTS = float(os.environ.get('RL_REPL_DROP','3'))   # acquirable-replacement recalibration, UNIFORM -3 (cont.25 dial).
# Per-group split (fwd -4 / other -2) REVERTED to uniform -3 (Luke, 2026-06-28): the DPP strip removes the forward-eligibility
# basis for the forward-specific extra. PLACEHOLDER -> re-validate the drop per position on the clean single-position base.
# NOTE: legacy env RL_REPL_DROP_FWD / RL_REPL_DROP_OTHER are now INERT (ignored); set RL_REPL_DROP to override.
REPL_DROP = {g: REPL_DROP_PTS for g in ['MID','GEN_DEF','GEN_FWD','KEY_DEF','KEY_FWD','RUC']}  # MA.REPL ONLY around the
# v_at_peak pricing here (engine value() untouched until the redesign is wired in). 0 = old behaviour.
K_REL      = 1.2     # reliability half-saturation. w = r^2/(r^2+K_REL^2) (STEEPER than linear: thin players lean prior,
REL_DECAY  = 0.92    # LIGHT recency decay for the EVIDENCE count (old seasons still count as evidence -> vets reach w~1)
MIN_SPREAD = 8.0     # floor on own-band spread (a proven-but-steady player still has injury/form variance)
DEF_SPREAD = 14.0    # own-band spread when <2 qualifying seasons (one season = wide own-band)
RUCK_TAX   = float(os.environ.get('RL_RUCK_TAX','0.25'))  # tax on RUCKS' UNREALISED (speculative) value only. Rucks peak
                                                          # late -> a list spot tied up for years; discount the part of value
                                                          # NOT justified by reliable production. 0 = off. Self-targeting:
                                                          # proven/production-priced rucks have ~no unrealised value -> untaxed.

def qual_seasons(p): return [(x['year'],x['avg'],x['games']) for x in p['scoring'] if x['games']>=6]

def reliability(p):
    """Effective full-seasons of evidence, lightly recency-decayed (vets accumulate -> w~1)."""
    return float(sum((REL_DECAY**max(0,MA.BASE_REF-yr))*min(g/cp.SEASON,1.0) for yr,_,g in qual_seasons(p)))

def own_band(p):
    """Recency-weighted recent level (recent_best2, the existing recency-tapered ceiling) +- the player's OWN season spread."""
    C=dp.recent_best2(p)
    qs=qual_seasons(p)
    if len(qs)>=2:
        w=np.array([REL_DECAY**max(0,MA.BASE_REF-yr) for yr,_,_ in qs]); av=np.array([a for _,a,_ in qs])
        mu=float(np.dot(w,av)/w.sum()); sd=float(np.sqrt(np.dot(w,(av-mu)**2)/w.sum()))
        spread=max(sd,MIN_SPREAD)
    else:
        spread=DEF_SPREAD
    return C+spread*ZQ

def _realised(p, cmodels, lens):
    """Production-only floor: the value a PROVEN version of this player at their reliability-shrunk level would earn (high
    exposure -> narrow band centred at level_eff). redesign_value - _realised = the UNREALISED/speculative part of value."""
    le=max(1.0, cp._lvl_eff(p, MA.BASE_REF)); q=copy.deepcopy(p); q['year']=MA.BASE_REF-8
    q['scoring']=[{'year':y,'games':22,'avg':le} for y in range(MA.BASE_REF-7, MA.BASE_REF+1)]
    return redesign_value(q, cmodels, lens=lens, _tax=False)

# ---- PEDIGREE SOFT FLOOR (cont.25, Luke's spec form) -----------------------------------------------------------
#   value = production + w * max(0, pedigree_pole - production)     (a blend on VALUES, lift-only; NOT a band-blend)
#   production = E[v] over the level-conditioned band; pole = E[v] over the position-adjusted AT-DRAFT band.
#   w (pedigree weight) decays with evidence: GENERAL = games-based (1 - games/DENOM); KPP = year-based schedule.
#   Lift-only by the max(0,..): can never DRAG a player below production (honours "pedigree lifts, never drags").
KPP_SCHED={1:1.0, 2:0.8, 3:0.5, 4:0.2}                      # KEY_FWD/KEY_DEF by YEARS-since-draft (old relative-floor), age<=22
FLOOR_DENOM=float(os.environ.get('RL_FLOOR_DENOM','30'))    # GENERAL games-weight denominator (dial)
FLOOR_GRACE=float(os.environ.get('RL_FLOOR_GRACE','2'))     # GENERAL: full games-weight through this many years, then taper
FLOOR_TAPER=float(os.environ.get('RL_FLOOR_TENURE_TAPER','0'))  # GENERAL tenure taper: per-year decrement after grace (0=off/current)
def _adraft_band(p, cm):                                    # the position-adjusted at-draft pedigree band (the pole)
    oh=[0.0]*len(cp.GROUPS); oh[cp.GIDX[MA.gfut(p)]]=1.0
    f=np.array([oh+[np.log(min(MA.effpk(p),cp.KMAX)),0.0,0.0,0.0,18.5]])
    return np.sort([float(cm[q].predict(f)[0]) for q in cp.Q])
def _price_repl(p, band, scale, lens):                      # REPL-adjusted E[v] over a band (pre brodie / lens-tilt)
    if not REPL_DROP: return scale*float(np.dot(dp.WQ,[dp.v_at_peak(p,L,lens) for L in band]))
    _sav=dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g]=_sav[g]-REPL_DROP.get(g,0)
        return scale*float(np.dot(dp.WQ,[dp.v_at_peak(p,L,lens) for L in band]))
    finally: MA.REPL.update(_sav)
def _floor_w(p):                                            # pedigree-protection weight (rucks excluded; lift-only)
    g=MA.gfut(p); a=MA.age(p); yr=MA.BASE_REF-p['year']
    if g=='RUC': return 0.0                                 # rucks: unrealised-production TAX only, NO pedigree floor
    if g in ('KEY_FWD','KEY_DEF'):                          # KPP: year-based schedule (slow developers hold pedigree longer)
        young=(a<=22) if a is not None else (yr<=4)
        return KPP_SCHED.get(yr,0.0) if young else 0.0
    young=(a<=23) if a is not None else (yr<=4)             # GENERAL: games (sample) evidence x tenure (time) taper
    if not young: return 0.0
    gw=1.0 - min(sum(x['games'] for x in p['scoring']), FLOOR_DENOM)/FLOOR_DENOM   # sample evidence: games played
    return gw*max(0.0, 1.0 - FLOOR_TAPER*max(0.0, yr-FLOOR_GRACE))                 # x time evidence: tenure taper (TAPER=0 -> off)

def redesign_value(p, cmodels, scale=None, lens='bal', _tax=True):
    if scale is None: scale=dp.SCALE_DIST
    if MA.level_now(p) is None: return MA.value(p,lens)          # pre-debut pedigree path (unchanged)
    band=cp.cond_prior_band(p,cmodels)                          # level+tenure+games+pedigree-conditioned PEAK projection
    prod=_price_repl(p, band, scale, lens)                      # PRODUCTION value
    w=_floor_w(p)
    if w>0:                                                     # SOFT FLOOR: value = production + w*max(0, pole - production)
        pole=_price_repl(p, _adraft_band(p,cmodels), scale, lens)
        ev=prod + w*max(0.0, pole-prod)
    else:
        ev=prod
    if MA.brodie_sig(p): ev*=0.5
    ev=round(ev*MA.lens_tilt(p,lens))
    if _tax and RUCK_TAX and MA.gfut(p)=='RUC':                # tax rucks' speculative (non-production) value only
        ev-=round(RUCK_TAX*max(0, ev-_realised(p,cmodels,lens)))
    return ev

def build(cap=2026, resolved_cut=2021):
    cmodels,_=cp.build_cond_prior(cap=cap, resolved_cut=resolved_cut)
    return cmodels

# ----------------------- validation -----------------------
if __name__=='__main__':
    cmodels=build()
    models,prior,META=dp.build()                                # OLD dist, for before/after comparison
    names=['Sheezel','Daicos','Bontempelli','Serong','Sharman','Caminiti','Phillipou','Dowling',
           'Farrow','Duff-Tytler','Berry','Sam Darcy','Rowell']
    def find(nm):
        c=[p for p in MA.players if nm.lower() in p['player'].lower() and MA.GRP.get(p['pos'])]
        return c[0] if c else None
    print('REDESIGN = level-conditioned prior priced via v_at_peak (no blend). value() / old_dist / REDESIGN / prior_p50:')
    print('player              pos      pick |  value()   old_dist   REDESIGN | prior_p50')
    for nm in names:
        p=find(nm)
        if not p: print(f'  {nm:18s} (not found)'); continue
        v=MA.value(p); od=dp.dist_value(p,models,prior,META,30,1.0); rd=redesign_value(p,cmodels)
        nmp=p['player'][:18]
        if MA.level_now(p) is None:
            print(f'  {nmp:18s} {MA.gfut(p):8s} {MA.effpk(p):4d} | {v:7d}  {od:8d}  {rd:8d}   (pre-debut->value())')
            continue
        pp=cp.cond_prior_band(p,cmodels)[2]
        print(f'  {nmp:18s} {MA.gfut(p):8s} {MA.effpk(p):4d} | {v:7d}  {od:8d}  {rd:8d} |   {pp:5.1f}')
