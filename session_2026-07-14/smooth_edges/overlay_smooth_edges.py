"""Smooth-edges overlay: three env-gated fixes applied by MONKEYPATCH to a loaded engine.
Does NOT modify the committed engine. Import `load` first, then call apply(cfg).
cfg is a dict of booleans: {'f1':bool,'f2':bool,'f3':bool}. All-off => byte-exact base.
"""
import numpy as np

# ---- FIX 1: smooth small-sample damping in _lvlcurr ----
# reliability rho(g)=g/(g+K1) (data-fit K1~5.8: var(season_mean_dev)=~690/g+119 => k=690/119).
K1=5.8
def make_lvlcurr(G):
    MA=G['MA']; cp=G['cp']; LDECAY_G=G['LDECAY_G']; _ldg=G['_ldg']
    def _lvlcurr_f1(p,Y):
        ld=LDECAY_G[_ldg(MA.gfut(p))]
        rows=[(x['year'],x['games'],x['avg']) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y]
        # reliability-damped game weight: g -> g*rho(g)=g^2/(g+K1)  (thin season counts less than proportionally)
        tw=sum((gm*gm/(gm+K1))*ld**max(0,Y-yr) for yr,gm,_ in rows)
        return float(sum((gm*gm/(gm+K1))*ld**max(0,Y-yr)*a for yr,gm,a in rows)/tw) if tw>0 else 0.0
    return _lvlcurr_f1

# ---- FIX 2: smooth the tolerance step in the LIVE established up-branch (_coreM1 line 244) ----
# base: if Lc>=Lo: return (Lo+S*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and radq) else Lo   [hard step at TOL_M1]
# fix : ramp the credit fraction smoothly over 0..TOL_M1 (smoothstep); radq kept as a soft multiplier.
# ---- FIX 3: extend pedigree fade past PROVEN_N ----
# base: n>=PROVEN_N branch has NO par term; n<PROVEN_N: c*Lc+(1-c)*par, (1-c)=0.75/0.50/0.25/0.
# fix : carry a small continuously-decaying par weight past the boundary: 0.75,0.50,0.25,0.10,0.03,~0.
def wped_tail(n, PROVEN_N):
    # continuous fade past PROVEN_N: w(4)=0.10, ratio 0.30 -> w(5)=0.03, w(6)=0.009, ->0
    if n<PROVEN_N: return 1.0-n/float(PROVEN_N)
    return 0.10*(0.30**(n-PROVEN_N))

def make_coreM1(G, f2, f3):
    MA=G['MA']; cp=G['cp']; PROVEN_N=G['PROVEN_N']; DOWN_TOL=G['DOWN_TOL']
    TOL_M1=G['TOL_M1']; S_M1=G['S_M1']; _L3_AGE=G['_L3_AGE']; _S_AGE=G['_S_AGE']
    _nqual=G['_nqual']; _par_prior=G['_par_prior']; _agemult2=G['_agemult2']; _radq=G['_radq']
    INPROG_Y=G['INPROG_Y']; SEASON_FE=G['SEASON_FE']
    def _lvlcurr(p,Y): return G['_lvlcurr'](p,Y)   # picks up patched _lvlcurr via G
    def _smoothstep(x):
        x=float(np.clip(x,0.0,1.0)); return x*x*(3-2*x)
    def _coreM1_f(p,Y):
        Lo=cp._lvl_eff_orig(p,Y); n=_nqual(p,Y)
        if n==0:
            if Y!=INPROG_Y or any(x['games']>0 and x['year']<Y and (cp.debutyr(p)-1)<x['year'] for x in p['scoring']): return Lo
            gy=sum(x['games'] for x in p['scoring'] if x['year']==Y and (cp.debutyr(p)-1)<x['year'])
            f1c=min(1.0, gy/max(1e-9,10.0*SEASON_FE))
            if f1c<=0.0: return Lo
            return (1.0-f1c)*Lo + f1c*((1.0/PROVEN_N)*_lvlcurr(p,Y)+(1.0-1.0/PROVEN_N)*_par_prior(p,Y))
        Lc=_lvlcurr(p,Y)
        if n>=PROVEN_N:
            S=(_S_AGE(cp._age_asof(p,Y)) if _L3_AGE else S_M1)
            if Lc>=Lo:
                if f2:
                    # smooth ramp of the up-credit over 0..TOL_M1; radq as soft 0.5..1 multiplier
                    r=_smoothstep((Lc-Lo)/TOL_M1)
                    rq=1.0 if _radq(p,Y,Lo) else 0.5
                    est=Lo+S*(Lc-Lo)*r*rq
                else:
                    est=(Lo+S*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo
            else:
                drop=Lo-Lc
                if drop<=DOWN_TOL: est=Lo
                else:
                    sw=float(np.clip((drop-DOWN_TOL)/5,0,1)); est=(1-sw)*Lo+sw*Lc*_agemult2(cp._age_asof(p,Y),Lc-MA.REPL.get(MA.gfut(p),0.0))
            if f3:
                w=wped_tail(n,PROVEN_N)   # small continuing pedigree pull past PROVEN_N
                if w>0: est=(1.0-w)*est+w*_par_prior(p,Y)
            return est
        c=n/PROVEN_N; return c*Lc+(1-c)*_par_prior(p,Y)
    return _coreM1_f

def apply(G, cfg):
    """Patch G in place. cfg keys f1,f2,f3 (bool). Also repatch cp._lvl_eff via _inferM1 wrapper."""
    cp=G['cp']
    # base originals captured once
    if '_ORIG' not in G:
        G['_ORIG']={'lvlcurr':G['_lvlcurr'],'coreM1':G['_coreM1'],'lvl_eff':cp._lvl_eff}
    O=G['_ORIG']
    # F1: swap _lvlcurr (read by coreM1, inferM1, v7, etc. via the G-closure? NO — they captured the name at def)
    G['_lvlcurr']=make_lvlcurr(G) if cfg.get('f1') else O['lvlcurr']
    # rebuild coreM1 (it references G['_lvlcurr'] through the wrapper) and inferM1 chain
    G['_coreM1']=make_coreM1(G, cfg.get('f2',False), cfg.get('f3',False))
    # inferM1 wraps coreM1; rebuild it to call patched coreM1 and patched _lvlcurr
    _eo=G['_eo']; MA=G['MA']; _upS=G['_upS']
    def _inferM1_f(p,Y):
        L0=G['_coreM1'](p,Y); eo=_eo(p,Y)
        if eo<=0: return L0
        avs=[x['avg'] for x in p['scoring'] if x.get('games',0)>=6 and (cp.debutyr(p)-1)<x['year']<=Y]
        if not avs: return L0
        bar=MA.REPL.get(MA.gfut(p),0.0)-3.0; N=Y-cp.debutyr(p)+1
        return (1-eo)*L0+eo*min(L0,max(_upS(max(avs)-bar,N),G['_lvlcurr'](p,Y)))
    cp._lvl_eff=_inferM1_f if (cfg.get('f1') or cfg.get('f2') or cfg.get('f3')) else O['lvl_eff']
    return G
