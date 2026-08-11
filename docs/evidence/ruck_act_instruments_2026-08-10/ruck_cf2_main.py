"""LIVE BOARD (origin/main) — ceiling + pole counterfactual grid, same source-switch technique."""
import os, sys, io, contextlib, json, hashlib
import numpy as np
WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
raw = open('_merged_recover.py').read().split('print("=== AFTER')[0]
OLD = "        wage=0.0 if pos=='RUCK' else float(np.clip(1-((a or 21)-20)/6,0,1))"
NEW = "        wage=(0.0 if (pos=='RUCK' and not _CFPOLE['on']) else float(np.clip(1-((a or 21)-20)/6,0,1)))"
assert raw.count(OLD) == 1
src = "_CFPOLE={'on':False}\n" + raw.replace(OLD, NEW)
G = {'__name__': '_ruck_cf2_main'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)
MA = G['MA']; cp = G['cp']; ev = G['ev']; CFP = G['_CFPOLE']; _isreal = G['_isreal']
delisted = G['delisted']; _prod_path = G['_prod_path']; bestlvl = G['bestlvl']
_ruc_ceiling = G['_ruc_ceiling']; _v0_uncapped = G['_v0_uncapped']; v0_start = G['v0_start']
INF = float('inf')
def _noceil(q, YY=2026): return INF
Y = 2026; rows = []
for p in MA.data:
    if not _isreal(p) or not MA.GRP.get(p.get('pos')): continue
    if MA.gfut(p) != 'RUCK': continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            price = ev(p, Y); e = _prod_path(p, Y)
            v0s = float(v0_start(p)); v0u = float(_v0_uncapped(p)); cpv = float(_ruc_ceiling(p, Y))
            _sc = G['_ruc_ceiling']; G['_ruc_ceiling'] = _noceil
            try: price_A = ev(p, Y)
            finally: G['_ruc_ceiling'] = _sc
            CFP['on'] = True; MA._pe_clear()
            try:
                price_C = ev(p, Y); e_C = _prod_path(p, Y)
                G['_ruc_ceiling'] = _noceil
                try: price_AC = ev(p, Y)
                finally: G['_ruc_ceiling'] = _sc
            finally:
                CFP['on'] = False; MA._pe_clear()
            price2 = ev(p, Y)
    except Exception:
        continue
    rows.append(dict(key=p.get('key'), player=p.get('player'), C=p.get('year'), typ=p.get('type'),
                     epk=int(MA.effpk(p)), games=sum(x['games'] for x in p['scoring']),
                     age=(cp._age_asof(p, Y) if hasattr(cp, '_age_asof') else None),
                     bestlvl=float(bestlvl(p, Y)), e=float(e), e_C=float(e_C), cpv=cpv, v0u=v0u, v0s=v0s,
                     bind=bool(cpv < e <= v0u), price=float(price), price_A=float(price_A),
                     price_C=float(price_C), price_AC=float(price_AC), identity=float(price2),
                     delisted=bool(delisted(p)), retired=bool(p.get('_retired'))))
bad = [r for r in rows if abs(r['identity'] - r['price']) > 1e-9]
print("identity failures: %d of %d ; e_C<e: %d" % (len(bad), len(rows), sum(1 for r in rows if r['e_C'] < r['e'] - 1e-9)))
json.dump(rows, open(os.environ['RL_OUT'] + '/ruck_cf2_main.json', 'w'), indent=0)
print("wrote %d ruck records ; engine=%s" % (len(rows), hashlib.md5(open('_merged_recover.py','rb').read()).hexdigest()[:8]))
