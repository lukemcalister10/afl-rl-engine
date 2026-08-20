#!/usr/bin/env python3
"""ORDER S — the shared engine harness. ORDER R's or_lib.py with the FIVE ORDER S dials added to
the environment clear-list so an unset S dial cannot leak in from a previous run. NOTHING ELSE IS
CHANGED: same loader, same leg recorder, same M3 reassembly, byte for byte.

Loads the engine in-process with a chosen dial line, exposes the namespace, and provides a
LEG RECORDER: a wrapper on _PV['blend'] that records the production input `e` the blend site
receives, WITHOUT changing one line of arithmetic. Everything downstream is read out of the
engine's own objects (rho31, o31_pi, pv_pedigree, o32_age_credit, o37_factor).
"""
import io, os, sys, json, math, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
# ORDER K's RULED SETTING — owner comment 5321546243, register v735. Not a search axis.
K = dict(DOSE='0.40', KAP='0.20', GU='8.0', ETA='0.50', GD='14.0', REL='1.08')


def load(**dials):
    """Load the engine. dials: extra env, e.g. RL_O37='1', RL_O38A='1'. RL_O37 absent => ORDER K."""
    env = dict(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1=K['DOSE'], RL_O36_TALL='1',
               RL_O36_FLOORFIX='1', RL_O36_KAPPA=K['KAP'], RL_O36_GAMMA=K['GU'],
               RL_O36_ETA=K['ETA'], RL_O36_GAMMA_D=K['GD'], RL_O36_LAMBDA=K['REL'],
               PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
               MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
               RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'), RL_GAMMA='1.0',
               RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
               RL_PRIOR_TREES='400', PAR_RAMPS='22',
               RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
    env.update({k: str(v) for k, v in dials.items() if v is not None})
    for k in ('RL_O35', 'RL_O37', 'RL_O38A', 'RL_O38B1', 'RL_O38B2',
              'RL_O39_TMAXPCT', 'RL_O39_BETASAT',
              'RL_O40_RECW', 'RL_O40_CAPFORM', 'RL_O40_CAPPCT', 'RL_O40_LAMBDA', 'RL_O40_PGMAT'):
        if k not in env:
            os.environ.pop(k, None)
    os.environ.update(env)
    sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation',
                    ROOT + '/engine/rl_after']
    cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
    NS = {}
    banner = io.StringIO()
    with contextlib.redirect_stdout(banner):
        import rl_model as MA
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NS)
    os.chdir(cwd)
    NS['_MA'] = MA
    NS['_BANNER'] = banner.getvalue()
    return NS


def install_recorder(NS):
    """Wrap the blend so the WHOLE decomposition is captured AT THE CALL SITE, in the exact clock
    state the price is formed in. Arithmetic untouched: the wrapper reads, then delegates.

    A row can reach the blend TWICE at the same year. That is the M3 proportional-tenure/age blend
    (_ev_m3): the engine evaluates the row on the full clock and again on the PINNED clock and returns
    w*click + (1-w)*pin. Both calls are recorded, in order, so the row's real price and its real
    charge can be reassembled instead of guessed."""
    rec = {}
    inner = NS['_PV']['blend']
    import math as _m

    def wrapped(p, Y, e):
        g = NS['pv_games'](p, Y)
        d = dict(key=p.get('key'), Y=int(Y), g=float(g), e=float(e), pin=bool(NS['_M3PIN']['on']))
        d['rho'] = NS['rho31'](g)
        d['credit'] = NS['o32_age_credit'](p, Y, g)
        try:
            d['ped'] = NS['pv_pedigree'](p)
        except SystemExit:
            d['ped'] = None
        d['pi'] = NS['o31_pi'](p, Y, g)
        charged = (NS['_O32S'] >= 6 and NS['O32_ETA'] > 0.0 and g > 0.0)
        d['charged'] = charged
        if charged:
            old_f = max(0.0, 1.0 - NS['O32_ETA'] * ((g / NS['O32_GAMMA_D'])
                                                    * _m.exp(1.0 - g / NS['O32_GAMMA_D'])))
            d['f_K'] = old_f
            # the factor the engine ACTUALLY applied at this site. Under an ORDER Q dial that is
            # o38_factor, not o37_factor -- reading the wrong one puts pi_base out by the whole repair.
            d['f'] = ((NS['o38_factor'](p, Y, g) if NS.get('_O38') else NS['o37_factor'](p, Y, g))
                      if NS.get('_O37') else old_f)
            d['f_P37'] = NS['o37_factor'](p, Y, g) if NS.get('_O37') else old_f
        else:
            d['f_K'] = d['f'] = d['f_P37'] = 1.0
        d['pi_base'] = d['pi'] / d['f'] if d['f'] > 0 else None
        d['s_P'] = NS['o37_surplus'](p, Y) if 'o37_surplus' in NS else None
        d['prod_leg'] = d['rho'] * float(e)
        d['ped_leg'] = (d['pi'] * d['ped']) if d['ped'] is not None else None
        d['price'] = ((d['prod_leg'] + d['ped_leg'] + d['credit'])
                      if d['ped_leg'] is not None else None)
        rec.setdefault((p.get('key'), int(Y)), []).append(d)
        return inner(p, Y, e)
    NS['_PV']['blend'] = wrapped
    return rec


def m3_w(NS, p, Y):
    """The M3 weight on the FULL-CLICK evaluation. 1.0 when M3 does not run for this row/year."""
    if int(Y) != NS['M3_INPROG_Y'] or NS['M3_FE'] >= 1.0 or NS['delisted'](p):
        return 1.0
    s = NS['_m3_s'](p, Y)
    if s <= 0.0:
        return 1.0
    return 1.0 - s * (1.0 - NS['M3_FE'])


def assemble(NS, p, Y=2026):
    """The row's whole price, reassembled from the engine's own recorded legs, M3 included.

        price = w*(rho_c*e_c + pi_c*ped + credit_c) + (1-w)*(rho_p*e_p + pi_p*ped + credit_p)

    The pedigree object `ped` is the same in both calls (it carries no clock). So the row's
    EFFECTIVE uncharged pedigree weight is  w*pi_base_c + (1-w)*pi_base_p  and its EFFECTIVE charge
    factor is the leg-weighted mixture of the two calls' factors, NOT either one of them.
    """
    cs = NS['_REC'].get((p.get('key'), int(Y)))
    if not cs:
        return None
    w = m3_w(NS, p, Y)
    if len(cs) == 1:
        w = 1.0
    c = cs[0]
    q = cs[1] if len(cs) > 1 else cs[0]
    ws = [w, 1.0 - w]
    o = dict(key=p.get('key'), Y=int(Y), n_calls=len(cs), m3=len(cs) > 1, w=w,
             ped=c['ped'], g_c=c['g'], g_p=q['g'])
    o['prod_leg'] = ws[0] * c['prod_leg'] + ws[1] * q['prod_leg']
    o['credit'] = ws[0] * c['credit'] + ws[1] * q['credit']
    if c['ped'] is None:
        o['ped_leg'] = o['pi_eff'] = o['pi_base_eff'] = o['f_eff'] = o['f_K_eff'] = None
        o['price'] = None
        return o
    o['pi_eff'] = ws[0] * c['pi'] + ws[1] * q['pi']
    o['pi_base_eff'] = ws[0] * c['pi_base'] + ws[1] * q['pi_base']
    o['pi_K_eff'] = ws[0] * c['pi_base'] * c['f_K'] + ws[1] * q['pi_base'] * q['f_K']
    o['ped_leg'] = o['pi_eff'] * c['ped']
    o['ped_leg_K'] = o['pi_K_eff'] * c['ped']
    o['f_eff'] = o['pi_eff'] / o['pi_base_eff'] if o['pi_base_eff'] else 1.0
    o['f_K_eff'] = o['pi_K_eff'] / o['pi_base_eff'] if o['pi_base_eff'] else 1.0
    o['f_c'], o['f_p'], o['fK_c'], o['fK_p'] = c['f'], q['f'], c['f_K'], q['f_K']
    o['pi_P37_eff'] = ws[0] * c['pi_base'] * c['f_P37'] + ws[1] * q['pi_base'] * q['f_P37']
    o['f_P37_eff'] = o['pi_P37_eff'] / o['pi_base_eff'] if o['pi_base_eff'] else 1.0
    o['s_P'] = c['s_P']
    o['price'] = o['prod_leg'] + o['ped_leg'] + o['credit']
    return o
