#!/usr/bin/env python3
"""ORDER I — STEP 1 OF THE JOINT CALIBRATION: the walk-forward LEG EXTRACTION at every S1 dose.

Plain words. To choose the dose and the counterweight together we have to know, for every player in
every draft class, what his year-1 price is made of: how much comes from his own playing (the
production leg Phat), how much from his draft pedigree (v0 and its weight), and what the sitter fade
charges him. Those legs are extracted ONCE per S1 dose by pinning the engine's clocks to that year
and truncating every record to seasons the engine could actually have seen. The re-mix knobs are
then swept analytically on top of the legs — which is why the sweep is cheap and the extraction is
not.

Engine is loaded at RL_O32_STAGE=5 (no re-mix, no age credit) so the legs are clean, with RL_O36=1
so BOTH S1 and the tall/small fade are live. The identity control: with the re-mix off, the
reconstructed price must equal ev(p, Y) exactly on every row, at every dose.
"""
import os, sys, json, math, io, contextlib, time

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

DOSES = [float(x) for x in os.environ.get('O36_DOSES', '0.00,0.15,0.25,0.35,0.45,0.55,0.70,1.00').split(',')]

os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O32_STAGE='5', RL_O36_LAM_S1='0.0',
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
assert NSE['_O32S'] == 5, 'engine must load at stage 5 (no re-mix) for clean legs'
assert MA._O36 and MA._O36_SCOPE['armed'], 'RL_O36 must be live and S1 armed'
ev = NSE['ev']; PLF = float(NSE['_PL_F'])
G = {k: NSE[k] for k in ('rho31', 'beta31', 'phi31', 'o31_D', 'o31_cu', 'o31_stall_run', 'pv_games',
                         'pv_pedigree', 'o31_pool_D', 'o31_fade_D', 'o36_kappa', 'o32_sigma_sel',
                         '_O30BP_BARS', 'o32_age_gap')}


def d_fade(p, Y):
    """The row's fade BEFORE the selection relief: the ruled schedule at his unplayed clock, raised to
    the tall/small pick exponent. Relief is applied analytically in the sweep so lambda_rel is free."""
    cu = float(G['o31_cu'](p, Y))
    D = float(G['o31_pool_D'](cu) if p.get('_pool') else G['o31_fade_D'](cu))
    if D < 1.0:
        D = D ** float(G['o36_kappa'](p))
    return D


CAND_P = SP + '/per_entrant_O31FFINAL.json'
A = json.load(open(CAND_P))
Arecs = {r['key']: r for r in A['recs']}
FM = {'paddy-mccartin', 'thomas-boyd'}
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
TALL = {'KPD', 'KPF', 'RUCK'}
D_TALL = {18: 22.334475609756097, 19: 20.55500752464971, 20: 16.306362402208926,
          21: 11.588672690048071, 22: 7.826894964594814, 23: 6.439783302063788}
D_SMALL = {18: 20.080511089352214, 19: 20.080511089352214, 20: 14.306977484301457,
           21: 11.265167414136857, 22: 6.761247284555768, 23: 4.584052475875439}


def age_gap(pos, age):
    if age is None or age >= 24:
        return 0.0
    return (D_TALL if pos in TALL else D_SMALL)[max(18, min(23, int(age)))]


S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
CARRY = 1.14
softplus = lambda x: math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(l):
    c = LCAPT_G * LCAPT_W * (softplus((l - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0 else 0.0


posval = lambda x: S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))
w_sqrt = lambda g: min(1.0, math.sqrt(max(0.0, g) / 10.0))


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        return 'RD' if t == 'RD' else ('MSD' if t == 'MSD' else 'OTHERPOOL')
    return None


SV = {}; SVA1 = {}
for k, r in Arecs.items():
    d = {}; yr = r['year']; aged = r.get('age_draft')
    for s in r['seasons']:
        if s['year'] > 2025:
            continue
        gp = s.get('bar')
        if gp not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - BARS[gp]) * 21.0
        if s['year'] == yr + 1:
            a1 = (aged + 1) if aged is not None else None
            SVA1[k] = w_sqrt(s['games']) * posval(s['avg'] + capt_prem(s['avg']) - (BARS[gp] - age_gap(gp, a1))) * 21.0
    SV[k] = d
dv_h6 = lambda k, Y: sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if Y < t <= Y + 6)

POP = []
for k, r in Arecs.items():
    if k in FM:
        continue
    arm = arm_of(r)
    if arm is None:
        continue
    yr = r['year']
    if yr < 2005 or yr > 2021:
        continue
    POP.append(dict(key=k, yr=yr, arm=arm, v0=float(r['v0']), g1=int(r.get('games_yr1') or 0),
                    pick=r.get('pick'), sv1=SV[k].get(yr + 1, 0.0), sv1_age=SVA1.get(k, 0.0),
                    dv1_h6=dv_h6(k, yr + 1)))
print('population: %d players (classes 2005-2021, all-arm)' % len(POP))

BYKEY = {}
for p in MA.data:
    BYKEY.setdefault(p.get('key'), []).append(p)
players = [max(v, key=lambda q: len(q['scoring'])) for v in BYKEY.values()]
PBYK = {p.get('key'): p for p in players}


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
for q in POP:
    NEED.setdefault(q['yr'] + 1, []).append(q)

LEGS = {d: {} for d in DOSES}
CTRL_FAIL = []
T0 = time.time()
for Y in sorted(NEED):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y:
            continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        eff_last = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y
    for dose in DOSES:
        MA.O36_LAM_S1 = dose
        MA._pe_clear()
        for q in NEED[Y]:
            p = PBYK.get(q['key'])
            if p is None:
                continue
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    e = float(ev(p, Y))
            except Exception:
                continue
            g = float(G['pv_games'](p, Y))
            r = float(G['rho31'](g))
            D = float(G['o31_D'](p, Y))
            s = int(G['o31_stall_run'](p, Y))
            pl = bool(p.get('_pool'))
            ph = float(G['phi31'](g, s, pl))
            be = float(G['beta31'](g, pl))
            V0 = float(G['pv_pedigree'](p))
            pi = D * (1.0 - r) + ph * be * r
            Phat = (e - pi * V0) / r if g > 0 else 0.0
            rec = (r * Phat + pi * V0) if g > 0 else D * V0
            if abs(rec - e) > 1e-6 * max(1.0, abs(e)):
                CTRL_FAIL.append((q['key'], Y, dose))
            LEGS[dose][q['key']] = dict(g=g, rho=r, Dfade=d_fade(p, Y), sig=float(G['o32_sigma_sel'](p, Y)),
                                        s=s, pool=pl, Phi=ph, beta=be, V0=V0, Phat=Phat, p1_s5=e,
                                        agap=float(G['o32_age_gap'](p, Y)))
    for p in players:
        if id(p) in saved:
            p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    print('  year %d done (%d rows x %d doses)  %.0fs elapsed' % (Y, len(NEED[Y]), len(DOSES), time.time() - T0), flush=True)
MA.BASE_REF = MA.AGE_REF = 2026; MA.O36_LAM_S1 = 0.0; MA._pe_clear()
if CTRL_FAIL:
    sys.exit('ORDER I HALT: leg identity failed on %d rows (first: %r)' % (len(CTRL_FAIL), CTRL_FAIL[:3]))
n0 = len(LEGS[DOSES[0]])
print('leg-identity control PASS on %d rows x %d doses' % (n0, len(DOSES)))

# ---- the at-bar continuity rows, extracted once per dose (the ruled gate's own object) ------------
CONT_KEYS = ['lachlan-carmichael', 'josh-smillie', 'harry-demattia', 'max-knobel', 'dyson-sharp',
             'isaac-kako', 'noah-mraz', 'willem-duursma', 'toby-conway', 'luke-beecken', 'chris-scerri']
CONT = {d: [] for d in DOSES}
for dose in DOSES:
    MA.O36_LAM_S1 = dose; MA._pe_clear()
    for ck in CONT_KEYS:
        p = PBYK.get(ck)
        if p is None:
            continue
        with contextlib.redirect_stdout(io.StringIO()):
            e = float(ev(p, 2026))
        g = float(G['pv_games'](p, 2026))
        r = float(G['rho31'](g))
        D = float(G['o31_D'](p, 2026))
        s = int(G['o31_stall_run'](p, 2026))
        pl = bool(p.get('_pool'))
        V0 = float(G['pv_pedigree'](p))
        pi = D * (1.0 - r) + float(G['phi31'](g, s, pl)) * float(G['beta31'](g, pl)) * r
        bar = float(G['_O30BP_BARS'].get(MA.gfut(p), 70.0)) * 20.0 * PLF
        Phat = (e - pi * V0) / r if g > 0 else bar
        CONT[dose].append(dict(key=ck, Phat=Phat, V0=V0, Dfade=d_fade(p, 2026),
                               sig=float(G['o32_sigma_sel'](p, 2026)), s=s, pool=pl,
                               atbar=bool(Phat >= bar), agap=float(G['o32_age_gap'](p, 2026))))
MA.O36_LAM_S1 = 0.0; MA._pe_clear()

out = dict(doses=DOSES, pop=POP, legs={('%.2f' % d): LEGS[d] for d in DOSES},
           cont={('%.2f' % d): CONT[d] for d in DOSES}, PLF=PLF,
           n_rows=n0, leg_identity='PASS')
json.dump(out, open(SP + '/O36_LEGS.json', 'w'), default=float)
print('written: %s/O36_LEGS.json  (%.0fs total)' % (SP, time.time() - T0))
