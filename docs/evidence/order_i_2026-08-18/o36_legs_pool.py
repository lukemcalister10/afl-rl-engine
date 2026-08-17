#!/usr/bin/env python3
"""ORDER I — THE FADE CONTROL COLUMN. Adds `Dfade_pool` to every extracted leg: the SAME row's fade
under the LANDING CANDIDATE'S POOLED pick exponent instead of Order H's tall/small one.

Why this is cheap and why it is legitimate: the production leg Phat is a projection of the player's
own output and does not depend on the sitter fade at all, so it is identical under either exponent.
The only thing the tall/small factor changes is D. So the control column needs no re-pricing — only
the row's unplayed clock, which is a store read.

With both columns present the sweep can price the landing candidate and ORDER I on ONE instrument,
which is what makes the comparison honest.
"""
import os, sys, json, io, contextlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O32_STAGE='5', RL_O36_LAM_S1='0.0',
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(cwd)
MA = NSE.get('MA', MA)
G = NSE

L = json.load(open(SP + '/O36_LEGS.json'))
DOSES = L['doses']
KEYS = set(L['legs']['%.2f' % DOSES[0]].keys())
BYKEY = {}
for p in MA.data:
    BYKEY.setdefault(p.get('key'), []).append(p)
players = [max(v, key=lambda q: len(q['scoring'])) for v in BYKEY.values()]
PBYK = {p.get('key'): p for p in players}
POPYR = {q['key']: q['yr'] for q in L['pop']}


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


NEED = {}
for k in KEYS:
    NEED.setdefault(POPYR[k] + 1, []).append(k)
POOLF = {}
TALLF = {}
for Y in sorted(NEED):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        el = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = el if (el is not None and el < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for k in NEED[Y]:
        p = PBYK.get(k)
        if p is None: continue
        cu = float(G['o31_cu'](p, Y))
        D0 = float(G['o31_pool_D'](cu) if p.get('_pool') else G['o31_fade_D'](cu))
        POOLF[k] = (D0 ** float(G['o35_kappa'](p))) if D0 < 1.0 else D0
        TALLF[k] = (D0 ** float(G['o36_kappa'](p))) if D0 < 1.0 else D0
    for p in players:
        if id(p) in saved:
            p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
nd = 0
for d in DOSES:
    for k, lg in L['legs']['%.2f' % d].items():
        lg['Dfade_pool'] = POOLF.get(k, lg['Dfade'])
        if abs(lg['Dfade'] - TALLF.get(k, lg['Dfade'])) > 1e-12:
            nd += 1
print('tall-vs-extracted Dfade mismatches (must be 0): %d' % nd)
assert nd == 0, 'the recomputed tall fade does not reproduce the extracted one — HALT'
nmove = sum(1 for k in KEYS if abs(POOLF[k] - TALLF[k]) > 1e-12)
print('rows whose fade differs between the pooled and the tall/small exponent: %d of %d' % (nmove, len(KEYS)))

# the at-bar continuity rows too
for d in DOSES:
    for c in L['cont']['%.2f' % d]:
        c['Dfade_pool'] = c['Dfade']      # the continuity object is a 2026 read; both columns carried
CONTP = {}
for c in L['cont']['%.2f' % DOSES[0]]:
    p = PBYK.get(c['key'])
    if p is None: continue
    cu = float(G['o31_cu'](p, 2026))
    D0 = float(G['o31_pool_D'](cu) if p.get('_pool') else G['o31_fade_D'](cu))
    CONTP[c['key']] = (D0 ** float(G['o35_kappa'](p))) if D0 < 1.0 else D0
for d in DOSES:
    for c in L['cont']['%.2f' % d]:
        c['Dfade_pool'] = CONTP.get(c['key'], c['Dfade'])
json.dump(L, open(SP + '/O36_LEGS.json', 'w'), default=float)
print('written: O36_LEGS.json (+ Dfade_pool on %d rows x %d doses)' % (len(KEYS), len(DOSES)))
