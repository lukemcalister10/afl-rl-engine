"""RUCK CEILING INSTRUMENT — BRANCH (act) BASIS.  READ-ONLY.

Replicates measure_g6.py's ASOF walk-forward loop VERBATIM (same population filter, same #338
truncation, same BASE_REF/AGE_REF pinning, same restore) on the stage-B branch engine
(_merged_recover.py md5 910bb422 == origin/landing/334-stage-b bytes), and captures, for every
RUCK (player, evaluation-year) row on the established leg:

   e        = _prod_path(p,Y)            the production price BEFORE the ruck ceiling
   cpv      = _ruc_ceiling(p,Y)          the ceiling the ev() site compares against
   v0u      = _v0_uncapped(p)            the uncapped zero-evidence start value
   bind     = (cpv < e <= v0u)           the ev() binding predicate, verbatim
   price    = ev(p,Y)                    the shipped walk-forward price
   price_nc = ev(p,Y) with the ceiling neutralised (CF-A)
   pole_cf  = raw_ev with the STANDARD wage ramp instead of wage=0 (CF-C, first order)
   v0s      = v0_start(p)                the surface-corrected year-0 anchor  (CF-B numerator)

Nothing is written outside the session scratchpad.
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_ruck_instr'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)

MA = G['MA']; cp = G['cp']; PR = G['PR']
delisted = G['delisted']; nseas_pro = G['nseas_pro']; bestlvl = G['bestlvl']
v0_start = G['v0_start']; entry_anchor = G['entry_anchor']
_sitout_cls = G['_sitout_cls']; _fEy = G['_fEy']; _prod_path = G['_prod_path']
_fa_year = G['_fa_year']; _form_anchor_clock = G['_form_anchor_clock']
ev = G['ev']; _ruc_ceiling = G['_ruc_ceiling']; _v0_uncapped = G['_v0_uncapped']
_cap_basis = G['_cap_basis']; _ruc_head_mult = G['_ruc_head_mult']; _ruc_head_v0 = G['_ruc_head_v0']
draftval = G['draftval']; raw_ev = G['raw_ev']; iso_eff = G['iso_eff']
b6 = G['b6']; price6 = G['price6']; _uncomp_prod = G['_uncomp_prod']
par_pole_u = G['par_pole_u']; _pole_u336 = G['_pole_u336']; _isreal = G['_isreal']
eff_ten = G['eff_ten']; _expgate = G['_expgate']; recover = G['recover']
RUC_PRIOR_CAP = G['RUC_PRIOR_CAP']; RUC_CEIL_HEAD = G['RUC_CEIL_HEAD']

ENGINE_MD5 = hashlib.md5(open('_merged_recover.py','rb').read()).hexdigest()
STORE_MD5  = hashlib.md5(open('rl_model_data.json','rb').read()).hexdigest()

# ---- CF-C: raw_ev with the STANDARD pedigree wage ramp (the branch body, ONE line changed) -------
def raw_ev_pole(p, Y=2026):
    _bb = b6(p, Y); pr = price6(p, _bb, Y); pr = _uncomp_prod(pr, p, Y, _bb)
    pos = MA.gfut(p); pk = MA.effpk(p)
    with _form_anchor_clock():
        T  = min(max(PR.tenure(p, _fa_year(Y)), 1), 6)
        et = min(max(eff_ten(p, _fa_year(Y), PR.tenure(p, _fa_year(Y))), 1), 6)
        po, par = par_pole_u(pos, pk, T, (_pole_u336(p, pos, pk, _fa_year(Y)) if _isreal(p) else 0.0))
        a = MA.age(p)
        wage = float(np.clip(1 - ((a or 21) - 20) / 6, 0, 1))     # <<< STANDARD RAMP (CF-C)
        tfade = float(np.interp(et, [1,2,3,4,5,6], [1.00,0.76,0.40,0.16,0.05,0.05]))
        expgate = _expgate(p, Y)
        w = wage * tfade * expgate
    perf = cp._lvl_wt(p, Y)
    return pr + w * recover(perf, par) * max(0.0, po - pr), w, float(po), float(pr)

MATRIX = os.environ['RL_MATRIX']
MMD5 = hashlib.md5(open(MATRIX,'rb').read()).hexdigest()
MX = json.load(open(MATRIX))
RECS = {(r['key'], r['type'], r['year']): r for r in MX['recs']}
def rec_for(key, C):
    for t in ('ND','MSD','RD','PDA','PDN','PDS','SSP','UNR','IRE'):
        if (key, t, C) in RECS: return RECS[(key, t, C)]
    return None

YR_LO, YR_HI = 2004, 2022
FORCE_MAJEURE = {'thomas-boyd','paddy-mccartin'}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p) and p.get('key') not in FORCE_MAJEURE]

def _min_tenure(p):
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2
def _debut_year(p):
    C = p.get('year')
    return None if C is None else (C if p.get('type') == 'MSD' else C + 1)
def _listed_through(p, lastscore):
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)

OUT = os.environ['RL_OUT']
ROWS = []
V0TAB = {}          # per player: v0_start / _v0_uncapped  (CF-B ratio R), computed inside the loop
for Y in range(2004, 2027):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        eff_last = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for p in players:
        C = p.get('year')
        if C is None or C > Y or not (YR_LO <= C <= YR_HI): continue
        try:
            if delisted(p): continue
            if nseas_pro(p, Y) < 1: continue
            pos = MA.gfut(p)
            fe = _fEy(Y, p)
            tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
            pk = int(MA.effpk(p)); gcum = sum(x['games'] for x in p['scoring'] if x['year'] <= Y)
            with _form_anchor_clock(): el = PR.tenure(p, _fa_year(Y))
            with contextlib.redirect_stdout(io.StringIO()):
                e = _prod_path(p, Y)
                v0s = float(v0_start(p)); v0u = float(_v0_uncapped(p))
                price = ev(p, Y)
                re_now = float(raw_ev(p, Y)); ie = float(iso_eff(p, Y))
                rp, wpole, po, prprod = raw_ev_pole(p, Y)
        except Exception as exc:
            continue
        V0TAB[p.get('key')] = (pos, v0s, v0u)
        if pos != 'RUCK':
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            cpv = float(_ruc_ceiling(p, Y))
            s   = float(bestlvl(p, Y))
            cb  = float(_cap_basis(p)); hm = float(_ruc_head_mult(p, Y)); hv = float(_ruc_head_v0(p))
            dv  = float(draftval(p))
            # CF-A: the SAME ev(), ceiling neutralised (the site's own predicate can never fire)
            _sav = G['_ruc_ceiling']
            G['_ruc_ceiling'] = lambda q, YY=2026: float('inf')
            try: price_nc = ev(p, Y)
            finally: G['_ruc_ceiling'] = _sav
        rec = rec_for(p.get('key'), C)
        sa = 0.0; age = None
        if rec is not None:
            smap = {s2['year']: float(s2.get('avg') or 0.0) for s2 in (rec.get('seasons') or [])}
            sa = smap.get(Y, 0.0); age = rec.get('age_draft')
        ROWS.append(dict(key=p.get('key'), player=p.get('player'), typ=p.get('type'), C=C, Y=Y, N=Y-C,
                         pos=pos, pk=pk, gcum=float(gcum), sa=float(sa), age=age, el=float(el),
                         tau=float(tau), is_pool=bool(p.get('_pool')),
                         e=float(e), cpv=cpv, v0u=v0u, v0s=v0s,
                         bind=bool(cpv < e <= v0u), price=float(price), price_nc=float(price_nc),
                         bestlvl=s, cap_basis=cb, draftval=dv, head_mult=hm, head_v0=hv,
                         raw_ev=re_now, iso_eff=ie, raw_ev_pole=float(rp), pole_w=float(wpole),
                         pole_po=po, pole_pr=prprod,
                         age_asof=(cp._age_asof(p, Y) if hasattr(cp, '_age_asof') else None),
                         prior_cap_val=float(RUC_PRIOR_CAP * cb * hv),
                         no_production=bool(s <= 0)))
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
    print("  ASOF %d done (%d ruck rows so far)" % (Y, len(ROWS)), flush=True)
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

json.dump(dict(meta=dict(engine_md5=ENGINE_MD5, store_md5=STORE_MD5, matrix=MATRIX, matrix_md5=MMD5,
                         v0surf_sig=G['_V0CURVE_META'].get('_v0surf_sig'),
                         v0surf_frozen=bool(G['_V0CURVE_META'].get('_v0surf_frozen')),
                         ruc_prior_cap=RUC_PRIOR_CAP, ruc_ceil_head=RUC_CEIL_HEAD,
                         ruccei_meta=G['_RUCCEIL_META']),
               rows=ROWS,
               v0tab={k: dict(pos=v[0], v0s=v[1], v0u=v[2]) for k, v in V0TAB.items()}),
          open(OUT + '/ruck_instr_branch.json', 'w'), indent=0)
print("engine=%s store=%s v0surf=%s frozen=%s" % (ENGINE_MD5[:8], STORE_MD5[:8],
      G['_V0CURVE_META'].get('_v0surf_sig'), G['_V0CURVE_META'].get('_v0surf_frozen')))
print("ruck rows captured = %d ; v0tab players = %d" % (len(ROWS), len(V0TAB)))
print("RUCCEIL meta:", G['_RUCCEIL_META'])
