#!/usr/bin/env python3
"""ORDER S READ-ONLY — the engine harness for T2. READ AND DELEGATE. NO ARITHMETIC IS CHANGED.

ORDER Q's `oq_lib.load` is imported and used UNCHANGED — the same dial line, the same thread pinning,
the same in-process exec. Nothing in this file edits an engine file, adds a dial, or writes a store.

What this file adds is a WIDER recorder. ORDER Q's recorder captured the charge side of the blend.
This one captures the SITTER side as well, at the same call site and in the same clock state:

    price = rho31(g)*e  +  pi*ped  +  o32_age_credit
    pi    = pi_base * f
    pi_base = D_final*(1 - rho) + Phi(g,s)*beta(g)*rho
    D_raw   = the schedule fade at the UNPLAYED depth c_u
    D_kap   = D_raw ** kappa(effective pick, TALL/SMALL)
    D_final = min(1, D_kap * (1 + O32_LAMBDA*sigma_sel))          == the engine's own o31_D

Every one of those is READ out of the engine's own functions. The wrapper reads, then delegates to
the untouched blend. A row can reach the blend twice at the same year (the M3 proportional-tenure
blend) and both calls are recorded, in order, exactly as ORDER Q does.
"""
import os, sys, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'docs/evidence/order_q_2026-08-18'))
import oq_lib as QL                                                          # noqa: E402

load = QL.load
m3_w = QL.m3_w


def install_recorder(NS):
    """The wide recorder. Reads, then delegates. Changes no arithmetic anywhere."""
    rec = {}
    inner = NS['_PV']['blend']
    MA = NS['_MA']
    _m = math

    def wrapped(p, Y, e):
        g = NS['pv_games'](p, Y)
        pool = bool(p.get('_pool'))
        d = dict(key=p.get('key'), Y=int(Y), g=float(g), e=float(e), pin=bool(NS['_M3PIN']['on']),
                 pool=pool)
        # ---- the production side
        d['rho'] = NS['rho31'](g)
        d['rho_base'] = NS['o31_rho_base'](g)
        d['credit'] = NS['o32_age_credit'](p, Y, g)
        try:
            d['ped'] = NS['pv_pedigree'](p)
        except SystemExit:
            d['ped'] = None
        # ---- the sitter side, in this clock state
        d['clock'] = NS['fade30b_clock'](p, Y)
        d['units'] = NS['o31_played_units'](p, Y)
        d['cu'] = NS['o31_cu'](p, Y)
        d['D_raw'] = NS['o31_pool_D'](d['cu']) if pool else NS['o31_fade_D'](d['cu'])
        pk = MA.effpk(p)
        pk = float(pk if pk else 64)
        d['effpk'] = pk
        d['tall'] = MA.gfut(p) in NS['O32_TALLPOS']
        d['kap_pooled'] = NS['o35_kappa_at'](pk)
        d['kap_small'] = NS['o36_kappa_at'](pk, False)
        d['kap_tall'] = NS['o36_kappa_at'](pk, True)
        use36 = bool(NS.get('_O36') and NS.get('_O36_TALL'))
        d['kap'] = (NS['o36_kappa'](p) if use36 else NS['o35_kappa'](p)) if NS.get('_O35') else 1.0
        # the counterfactual exponent this row would carry if the TALL/SMALL factor did not exist:
        # ORDER D's pooled curve, which is exactly what RL_O36_TALL=0 falls back to.
        d['kap_noTS'] = d['kap_pooled'] if NS.get('_O35') else 1.0
        if NS.get('_O35') and d['D_raw'] < 1.0:
            d['D_kap'] = d['D_raw'] ** d['kap']
            d['D_kap_noTS'] = d['D_raw'] ** d['kap_noTS']
        else:
            d['D_kap'] = d['D_kap_noTS'] = d['D_raw']
        d['sigma'] = NS['o32_sigma_sel'](p, Y)
        d['D_final'] = NS['o31_D'](p, Y)
        # structural check: the recomputed chain must be the engine's own o31_D, bit for bit.
        chk = d['D_kap']
        if NS['_O32S'] >= 5 and chk < 1.0 and d['sigma'] > 0.0:
            chk = min(1.0, chk * (1.0 + NS['O32_LAMBDA'] * d['sigma']))
        d['D_chain_err'] = abs(chk - d['D_final'])
        d['D_noTS'] = d['D_kap_noTS']
        if NS['_O32S'] >= 5 and d['D_noTS'] < 1.0 and d['sigma'] > 0.0:
            d['D_noTS'] = min(1.0, d['D_noTS'] * (1.0 + NS['O32_LAMBDA'] * d['sigma']))
        # ---- the stall / beta side
        d['srun'] = NS['o31_stall_run'](p, Y)
        d['phi'] = NS['phi31'](g, d['srun'], pool)
        d['beta'] = NS['beta31'](g, pool)
        # ---- the charge
        d['pi'] = NS['o31_pi'](p, Y, g)
        charged = (NS['_O32S'] >= 6 and NS['O32_ETA'] > 0.0 and g > 0.0)
        d['charged'] = charged
        old_f = max(0.0, 1.0 - NS['O32_ETA'] * ((g / NS['O32_GAMMA_D'])
                                                * _m.exp(1.0 - g / NS['O32_GAMMA_D']))) if g > 0 else 1.0
        if charged:
            d['f_K'] = old_f
            d['f'] = ((NS['o38_factor'](p, Y, g) if NS.get('_O38') else NS['o37_factor'](p, Y, g))
                      if NS.get('_O37') else old_f)
        else:
            d['f_K'] = d['f'] = 1.0
        d['pi_base'] = d['pi'] / d['f'] if d['f'] > 0 else None
        # pi_base recomputed from its own parts, as a check the decomposition is the engine's
        d['pi_base_chk'] = d['D_final'] * (1.0 - d['rho']) + d['phi'] * d['beta'] * d['rho']
        # ---- the ORDER P charge internals
        d['s_P'] = NS['o37_surplus'](p, Y) if 'o37_surplus' in NS else None
        if NS.get('_O37') and d['s_P'] is not None:
            d['A'] = 1.0 - _m.exp(-g / NS['O37_G0'])
            d['T'] = min(max(1.0 - NS['O37_THETA_R'] * (d['s_P'] - NS['O37_S0']), 0.0), NS['O37_TMAX'])
            d['f_A1'] = _m.exp(-NS['O37_LAMBDA'] * 1.0 * d['T'])       # the same T at FULL evidence
        else:
            d['A'] = d['T'] = d['f_A1'] = None
        d['prod_leg'] = d['rho'] * float(e)
        d['ped_leg'] = (d['pi'] * d['ped']) if d['ped'] is not None else None
        d['price'] = ((d['prod_leg'] + d['ped_leg'] + d['credit'])
                      if d['ped_leg'] is not None else None)
        rec.setdefault((p.get('key'), int(Y)), []).append(d)
        return inner(p, Y, e)

    NS['_PV']['blend'] = wrapped
    return rec


def assemble(NS, p, Y=2026):
    """The row's whole price and EVERY leg attribution, M3-weighted, from the recorded calls."""
    cs = NS['_REC'].get((p.get('key'), int(Y)))
    if not cs:
        return None
    w = m3_w(NS, p, Y)
    if len(cs) == 1:
        w = 1.0
    c = cs[0]
    q = cs[1] if len(cs) > 1 else cs[0]
    ws = (w, 1.0 - w)

    def mix(k):
        return ws[0] * c[k] + ws[1] * q[k]

    o = dict(key=p.get('key'), Y=int(Y), n_calls=len(cs), m3=len(cs) > 1, w=w, ped=c['ped'],
             g=mix('g'), rho=mix('rho'), credit=mix('credit'), prod_leg=mix('prod_leg'),
             cu=mix('cu'), clock=mix('clock'), units=mix('units'), sigma=mix('sigma'),
             D_raw=mix('D_raw'), D_kap=mix('D_kap'), D_final=mix('D_final'), D_noTS=mix('D_noTS'),
             kap=c['kap'], kap_noTS=c['kap_noTS'], effpk=c['effpk'], tall=c['tall'],
             srun=c['srun'], phi=mix('phi'), beta=mix('beta'), s_P=c['s_P'],
             A=c['A'], T=c['T'], pool=c['pool'],
             D_chain_err=max(c['D_chain_err'], q['D_chain_err']))
    if c['ped'] is None:
        o['price'] = None
        return o
    ped = c['ped']
    o['pi_eff'] = mix('pi')
    o['pi_base_eff'] = mix('pi_base')
    o['f_eff'] = o['pi_eff'] / o['pi_base_eff'] if o['pi_base_eff'] else 1.0
    o['f_K_eff'] = (ws[0] * c['pi_base'] * c['f_K'] + ws[1] * q['pi_base'] * q['f_K']) / o['pi_base_eff'] \
        if o['pi_base_eff'] else 1.0
    o['ped_leg'] = o['pi_eff'] * ped
    o['price'] = o['prod_leg'] + o['ped_leg'] + o['credit']

    # ---- THE ATTRIBUTIONS, in ENGINE currency. Each is a counterfactual on ONE object.
    def leg(k_from, k_to):
        """f * (1-rho) * ped * (D[k_from] - D[k_to]), M3-weighted call by call."""
        tot = 0.0
        for wi, cc in zip(ws, (c, q)):
            tot += wi * cc['f'] * (1.0 - cc['rho']) * ped * (cc[k_from] - cc[k_to])
        return tot

    one = dict(D_one=1.0)
    tot_fade = 0.0
    for wi, cc in zip(ws, (c, q)):
        tot_fade += wi * cc['f'] * (1.0 - cc['rho']) * ped * (1.0 - cc['D_final'])
    o['a_fade_total'] = tot_fade
    sched = 0.0
    for wi, cc in zip(ws, (c, q)):
        sched += wi * cc['f'] * (1.0 - cc['rho']) * ped * (1.0 - cc['D_raw'])
    o['a_fade_schedule'] = sched
    o['a_fade_kappa'] = leg('D_raw', 'D_kap')
    o['a_fade_relief'] = leg('D_kap', 'D_final')
    # SIGN CONVENTION for the two "kept" objects: POSITIVE = board points the mechanism KEPT ON the
    # row that would otherwise have gone. Everything else above is POSITIVE = points REMOVED.
    o['a_tall_saved'] = leg('D_final', 'D_noTS')      # >0 = the TALL/SMALL factor KEPT value on him
    chg = 0.0
    chg_A = 0.0
    for wi, cc in zip(ws, (c, q)):
        chg += wi * (1.0 - cc['f']) * cc['pi_base'] * ped
        if cc.get('f_A1') is not None:
            chg_A += wi * (cc['f'] - cc['f_A1']) * cc['pi_base'] * ped
    o['a_charge'] = chg                               # what the ORDER P charge removed
    o['a_evidence_saved'] = chg_A                     # what A(g) < 1 KEPT on him against full evidence
    return o
