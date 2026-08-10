"""RUCK CEILING INSTRUMENT — LIVE BOARD (origin/main ef7eff8) BASIS.  READ-ONLY.

Present-lens board evaluation (Y=2026, BASE_REF/AGE_REF at their shipped defaults) for EVERY real
player the engine prices, with the ruck-ceiling site instrumented exactly as ev() reads it.
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_ruck_instr_main'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)

MA = G['MA']; cp = G['cp']; PR = G['PR']
delisted = G['delisted']; nseas_pro = G['nseas_pro']; bestlvl = G['bestlvl']
v0_start = G['v0_start']; _prod_path = G['_prod_path']; ev = G['ev']
_ruc_ceiling = G['_ruc_ceiling']; _v0_uncapped = G['_v0_uncapped']
_cap_basis = G['_cap_basis']; _ruc_head_mult = G['_ruc_head_mult']; _ruc_head_v0 = G['_ruc_head_v0']
draftval = G['draftval']; raw_ev = G['raw_ev']; iso_eff = G['iso_eff']
b6 = G['b6']; price6 = G['price6']; _uncomp_prod = G['_uncomp_prod']
par_pole = G['par_pole']; eff_ten = G['eff_ten']; _expgate = G['_expgate']; recover = G['recover']
_fa_year = G['_fa_year']; _form_anchor_clock = G['_form_anchor_clock']; _isreal = G['_isreal']
RUC_PRIOR_CAP = G['RUC_PRIOR_CAP']; RUC_CEIL_HEAD = G['RUC_CEIL_HEAD']
PL_F = G['_PL_F']

def raw_ev_pole(p, Y=2026):
    _bb = b6(p, Y); pr = price6(p, _bb, Y); pr = _uncomp_prod(pr, p, Y, _bb)
    pos = MA.gfut(p); pk = MA.effpk(p)
    with _form_anchor_clock():
        T  = min(max(PR.tenure(p, _fa_year(Y)), 1), 6)
        et = min(max(eff_ten(p, _fa_year(Y), PR.tenure(p, _fa_year(Y))), 1), 6)
        po, par = par_pole(pos, pk, T); a = MA.age(p)
        wage = float(np.clip(1 - ((a or 21) - 20) / 6, 0, 1))     # <<< STANDARD RAMP (CF-C)
        tfade = float(np.interp(et, [1,2,3,4,5,6], [1.00,0.76,0.40,0.16,0.05,0.05]))
        expgate = _expgate(p, Y)
        w = wage * tfade * expgate
    perf = cp._lvl_wt(p, Y)
    return pr + w * recover(perf, par) * max(0.0, po - pr), w, float(po), float(pr)

OUT = os.environ['RL_OUT']; Y = 2026
rows = []
for p in MA.data:
    if not _isreal(p): continue
    if not MA.GRP.get(p.get('pos')): continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            pos = MA.gfut(p)
            price = ev(p, Y)
            e = _prod_path(p, Y)
            v0s = float(v0_start(p)); v0u = float(_v0_uncapped(p))
            rp, wpole, po, prprod = raw_ev_pole(p, Y)
            ie = float(iso_eff(p, Y)); re_now = float(raw_ev(p, Y))
    except Exception:
        continue
    d = dict(key=p.get('key'), player=p.get('player'), pos=pos, typ=p.get('type'),
             C=p.get('year'), pick=p.get('pick'), epk=int(MA.effpk(p)),
             is_pool=bool(p.get('_pool')), delisted=bool(delisted(p)), retired=bool(p.get('_retired')),
             games_total=sum(x['games'] for x in p['scoring']),
             last_year=max((x['year'] for x in p['scoring'] if x['games'] > 0), default=None),
             age_asof=(cp._age_asof(p, Y) if hasattr(cp, '_age_asof') else None),
             e=float(e), price=float(price), v0s=v0s, v0u=v0u,
             raw_ev=re_now, iso_eff=ie, raw_ev_pole=float(rp), pole_w=float(wpole),
             pole_po=po, pole_pr=prprod, nseas=int(nseas_pro(p, Y)))
    if pos == 'RUCK':
        with contextlib.redirect_stdout(io.StringIO()):
            cpv = float(_ruc_ceiling(p, Y)); s = float(bestlvl(p, Y))
            cb = float(_cap_basis(p)); hm = float(_ruc_head_mult(p, Y)); hv = float(_ruc_head_v0(p))
            _sav = G['_ruc_ceiling']; G['_ruc_ceiling'] = lambda q, YY=2026: float('inf')
            try: price_nc = ev(p, Y)
            finally: G['_ruc_ceiling'] = _sav
        d.update(cpv=cpv, bestlvl=s, cap_basis=cb, head_mult=hm, head_v0=hv,
                 draftval=float(draftval(p)), bind=bool(cpv < e <= v0u), price_nc=float(price_nc),
                 no_production=bool(s <= 0), prior_cap_val=float(RUC_PRIOR_CAP * cb * hv))
    rows.append(d)

json.dump(dict(meta=dict(engine_md5=hashlib.md5(open('_merged_recover.py','rb').read()).hexdigest(),
                         store_md5=hashlib.md5(open('rl_model_data.json','rb').read()).hexdigest(),
                         v0surf_sig=G['_V0CURVE_META'].get('_v0surf_sig'),
                         v0surf_frozen=bool(G['_V0CURVE_META'].get('_v0surf_frozen')),
                         pl_factor=PL_F, ruccei_meta=G['_RUCCEIL_META'],
                         ruc_prior_cap=RUC_PRIOR_CAP, ruc_ceil_head=RUC_CEIL_HEAD),
               rows=rows), open(OUT + '/ruck_instr_main.json', 'w'), indent=0)
print("rows=%d  rucks=%d  engine=%s store=%s v0surf=%s factor=%s"
      % (len(rows), sum(1 for r in rows if r['pos'] == 'RUCK'),
         hashlib.md5(open('_merged_recover.py','rb').read()).hexdigest()[:8],
         hashlib.md5(open('rl_model_data.json','rb').read()).hexdigest()[:8],
         G['_V0CURVE_META'].get('_v0surf_sig'), PL_F))
print("RUCCEIL meta:", G['_RUCCEIL_META'])
