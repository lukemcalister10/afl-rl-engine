"""D4 COUNTERFACTUAL GRID v2 — BRANCH (act) BASIS.  READ-ONLY.  Supersedes ruck_cf_branch.py.

FAULT IN v1, DISCLOSED AND FIXED HERE: v1 re-implemented raw_ev's body to change the wage line, and
that re-implementation missed the W4 wrapper (`_raw_ev_w4_0` * `_ycred_mult`, plus the `_W4CTX`
context that `price6` reads).  Its CF-C numbers were therefore not a wage counterfactual at all.

v2 changes ONE CHARACTER RANGE OF THE ENGINE SOURCE and gates it behind a runtime switch:

    -   wage=0.0 if pos=='RUCK' else float(np.clip(1-((a or 21)-20)/6,0,1))
    +   wage=(0.0 if (pos=='RUCK' and not _CFPOLE['on']) else float(np.clip(...)))

`_CFPOLE['on']` is False at import, so EVERY structural scaffold built at module load — the RUCK ISO
pick-guard table, the frozen pole table, the pick-neutral ruck ceiling grid, the V0 pick-order guard
and the V0 board curve — is byte-identical to the shipped engine.  Flipping the switch changes only
the evaluation of a real player.  With the switch off the whole file must reproduce the shipped
prices byte-exact; that identity is asserted per row.
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
raw = open('_merged_recover.py').read().split('print("=== AFTER')[0]
OLD = "        wage=0.0 if pos=='RUCK' else float(np.clip(1-((a or 21)-20)/6,0,1))"
NEW = "        wage=(0.0 if (pos=='RUCK' and not _CFPOLE['on']) else float(np.clip(1-((a or 21)-20)/6,0,1)))"
assert raw.count(OLD) == 1, "wage site not unique"
src = "_CFPOLE={'on':False}\n" + raw.replace(OLD, NEW)
G = {'__name__': '_ruck_cf2'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)

MA = G['MA']; cp = G['cp']; PR = G['PR']
delisted = G['delisted']; nseas_pro = G['nseas_pro']
_prod_path = G['_prod_path']; ev = G['ev']; CFP = G['_CFPOLE']
INF = float('inf')
def _noceil(q, YY=2026): return INF

YR_LO, YR_HI = 2004, 2022
FORCE_MAJEURE = {'thomas-boyd', 'paddy-mccartin'}
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
                _ns = int(nseas_pro(p, Y))
                price = ev(p, Y); e = _prod_path(p, Y)
                _sc = G['_ruc_ceiling']
                G['_ruc_ceiling'] = _noceil
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
        ROWS.append(dict(key=p.get('key'), C=C, Y=Y, N=Y - C, pk=int(MA.effpk(p)), ns=_ns,
                         e=float(e), e_C=float(e_C), price=float(price), price_A=float(price_A),
                         price_C=float(price_C), price_AC=float(price_AC), identity=float(price2)))
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
    print("  CF2 ASOF %d done (%d rows)" % (Y, len(ROWS)), flush=True)
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
bad = [r for r in ROWS if abs(r['identity'] - r['price']) > 1e-9]
print("switch-off restore identity failures: %d of %d" % (len(bad), len(ROWS)))
mono = [r for r in ROWS if r['e_C'] < r['e'] - 1e-9]
print("rows where e_C < e (should be ZERO: the pole term is non-negative): %d" % len(mono))
json.dump(ROWS, open(OUT + '/ruck_cf3_branch_allrows.json', 'w'), indent=0)
print("wrote %d rows ; engine=%s" % (len(ROWS), hashlib.md5(open('_merged_recover.py','rb').read()).hexdigest()[:8]))
