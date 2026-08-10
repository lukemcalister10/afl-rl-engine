"""D4 COUNTERFACTUAL GRID — BRANCH (act) BASIS.  READ-ONLY.

Same ASOF loop as ruck_instr_branch.py.  For every RUCK established-leg row, four prices:

    price          ev()                                  shipped
    price_A        ev() with the ruck ceiling neutralised            (CF-A: ceiling off)
    price_C        ev() with raw_ev's wage = the STANDARD ramp       (CF-C: pole granted)
    price_AC       both                                              (CF-A+C)

CF-C scope, DECLARED: the wage patch is applied to the REAL-player evaluation only.  The import-time
structural scaffolds built from synthetics (the RUCK ISO pick-guard table and the pick-neutral ruck
production->$ ceiling grid) are HELD at their shipped values, so this measures the pole credit denied
to real rucks, not a re-fit of the ruck scaffolds.
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_ruck_cf'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)

MA = G['MA']; cp = G['cp']; PR = G['PR']
delisted = G['delisted']; nseas_pro = G['nseas_pro']
_prod_path = G['_prod_path']; ev = G['ev']
b6 = G['b6']; price6 = G['price6']; _uncomp_prod = G['_uncomp_prod']
par_pole_u = G['par_pole_u']; _pole_u336 = G['_pole_u336']; _isreal = G['_isreal']
eff_ten = G['eff_ten']; _expgate = G['_expgate']; recover = G['recover']
_fa_year = G['_fa_year']; _form_anchor_clock = G['_form_anchor_clock']
RAW_ORIG = G['raw_ev']

def raw_ev_std_wage(p, Y=2026):
    """The branch raw_ev body with ONE line changed: RUCK gets the standard pedigree wage ramp."""
    _bb = b6(p, Y); pr = price6(p, _bb, Y); pr = _uncomp_prod(pr, p, Y, _bb)
    pos = MA.gfut(p); pk = MA.effpk(p)
    with _form_anchor_clock():
        T  = min(max(PR.tenure(p, _fa_year(Y)), 1), 6)
        et = min(max(eff_ten(p, _fa_year(Y), PR.tenure(p, _fa_year(Y))), 1), 6)
        po, par = par_pole_u(pos, pk, T, (_pole_u336(p, pos, pk, _fa_year(Y)) if _isreal(p) else 0.0))
        a = MA.age(p)
        wage = float(np.clip(1 - ((a or 21) - 20) / 6, 0, 1))
        tfade = float(np.interp(et, [1,2,3,4,5,6], [1.00,0.76,0.40,0.16,0.05,0.05]))
        w = wage * tfade * _expgate(p, Y)
    perf = cp._lvl_wt(p, Y)
    return pr + w * recover(perf, par) * max(0.0, po - pr)

INF = float('inf')
def _noceil(q, YY=2026): return INF

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
    C = p.get('year'); return None if C is None else (C if p.get('type') == 'MSD' else C + 1)
def _listed_through(p, lastscore):
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)

OUT = os.environ['RL_OUT']; ROWS = []
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
        if MA.gfut(p) != 'RUCK': continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if delisted(p): continue
                if nseas_pro(p, Y) < 1: continue
                price = ev(p, Y); e = _prod_path(p, Y)
                _sc = G['_ruc_ceiling']; G['_ruc_ceiling'] = _noceil
                try: price_A = ev(p, Y)
                finally: G['_ruc_ceiling'] = _sc
                G['raw_ev'] = raw_ev_std_wage; MA._pe_clear()
                try:
                    price_C = ev(p, Y); e_C = _prod_path(p, Y)
                    G['_ruc_ceiling'] = _noceil
                    try: price_AC = ev(p, Y)
                    finally: G['_ruc_ceiling'] = _sc
                finally:
                    G['raw_ev'] = RAW_ORIG; MA._pe_clear()
                price2 = ev(p, Y)          # re-read after restore: must equal price (identity check)
        except Exception:
            continue
        ROWS.append(dict(key=p.get('key'), C=C, Y=Y, N=Y-C, pk=int(MA.effpk(p)),
                         e=float(e), e_C=float(e_C), price=float(price), price_A=float(price_A),
                         price_C=float(price_C), price_AC=float(price_AC), identity=float(price2)))
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
    print("  CF ASOF %d done (%d rows)" % (Y, len(ROWS)), flush=True)
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
bad = [r for r in ROWS if abs(r['identity'] - r['price']) > 1e-9]
print("restore-identity failures: %d of %d" % (len(bad), len(ROWS)))
json.dump(ROWS, open(OUT + '/ruck_cf_branch.json', 'w'), indent=0)
print("wrote %d rows" % len(ROWS))
