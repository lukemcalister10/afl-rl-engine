"""MECHANISM (a) PRICING STUDY — capital-conditional maturation, priced by the engine itself.

READ-ONLY STUDY for the owner's D5 mechanism word (register v864; his ask 2026-08-26: "Can we price
up a movers list under A please?"). NOT a board, NOT a landing: the built lever goes through prereg,
the battery and blind review before any flip. No engine file is touched — the study PATCHES the
loaded namespace's o31_pi in memory, sweeps every row through the real ev() (so the one-law blend,
the D7 guard and the ORDER 45 net all apply exactly as live), then RESTORES and proves the baseline
board reproduces byte-exact on every row.

THE CANDIDATE FORM (declared; zero new constants): the maturation rate inside the pedigree
multiplier becomes capital-conditional through the ALREADY-RULED kappa exponent (o36_kappa — the
same pick-and-class exponent the sitter clock uses):

    rho_a(g, p) = rho31(g) ** (1/kappa(p))

    pi_a = D(c_u)*(1 - rho_a) + Phi(g,s)*beta(g)*rho_a        [then the o38/o37 charge, unchanged]

kappa<1 (high capital, e.g. oliver 0.85) => rho_a < rho => the pedigree residual transfers SLOWER;
kappa=1 => identity; kappa>1 (late picks) => faster. The PRODUCTION leg's rho stays UNTOUCHED —
evidence earns its blend weight exactly as today; only the pedigree residual's retention changes.
Structural invariants preserved: rho_a(0)=0 so pi_a(0)=D exactly (gameless rows and every cameo
floor unchanged); _Dov reference calls (the R3 sizing law) go through the same form.

TWO VARIANTS PRICED: SYM (the exact kappa mirror, late picks mature faster too) and ONE-SIDED
(kappa<1 rows only; kappa>=1 rows identical to live).

VALIDATIONS (P15 — the instrument proves what it measures): (1) pre-patch, a reconstruction of pi
from the engine's own pieces must equal o31_pi on every row to 1e-9 (proves the formula read is the
real one); (2) post-restore, ev() must reproduce the live price BYTE-EXACT on every row (proves the
patch left nothing behind); (3) the patched world must leave every gameless row's price unchanged.
"""
import json, math

OUT = '/home/user/afl-rl-engine/docs/evidence/speed_act_2026-08-26/MECH_A_MOVERS.json'
Y = 2026
NAMED = {'harrison-oliver', 'thomas-burton', 'noah-roberts-thomson', 'lucas-camporeale',
         'cody-angove', 'zane-peucker', 'archie-ludowyke', 'ollie-greeves', 'noah-howes',
         'rhys-unwin', 'luke-kennedy', 'aidan-johnson'}


def run(ns):
    G, MA = ns['G'], ns['MA']
    for sym in ('o31_pi', 'o31_D', 'rho31', 'beta31', 'phi31', 'o31_stall_run', 'o36_kappa',
                'pv_games', 'pv_pedigree', '_ev_pre45', 'ev', '_PL_F', '_O32S', 'O32_ETA',
                '_O37', '_O38', 'o37_factor', 'o38_factor', 'O32_GAMMA_D', '_D7_FLOOR'):
        if sym not in G:
            raise SystemExit('mech_a HALT: engine symbol %r absent — re-map, do not guess.' % sym)
    F = G['_PL_F']
    orig_pi = G['o31_pi']
    rows = [p for p in MA.data if not p.get('_retired') and p.get('key')]

    def repin():
        MA.BASE_REF = MA.AGE_REF = Y
        MA._pe_clear()

    # ---- VALIDATION 1: the reconstruction equals the engine's own pi on every row --------------
    def pi_form(p, rho_of):
        g = G['pv_games'](p, Y)
        r = rho_of(g, p)
        pl = bool(p.get('_pool'))
        pi = G['o31_D'](p, Y) * (1.0 - r) + G['phi31'](g, G['o31_stall_run'](p, Y), pl) * G['beta31'](g, pl) * r
        if G['_O32S'] >= 6 and G['O32_ETA'] > 0.0 and g > 0.0:
            pi *= ((G['o38_factor'](p, Y, g) if G['_O38'] else G['o37_factor'](p, Y, g)) if G['_O37'] else
                   max(0.0, 1.0 - G['O32_ETA'] * ((g / G['O32_GAMMA_D']) * math.exp(1.0 - g / G['O32_GAMMA_D']))))
        return pi

    bad = 0
    for p in rows:
        repin()
        if abs(pi_form(p, lambda g, q: G['rho31'](g)) - orig_pi(p, Y)) > 1e-9:
            bad += 1
    if bad:
        raise SystemExit('mech_a HALT: the pi reconstruction diverges from o31_pi on %d rows — the '
                         'formula read is NOT the engine\'s; nothing this study prices is safe.' % bad)

    # ---- the baseline sweep ---------------------------------------------------------------------
    base = {}
    for p in rows:
        repin()
        base[p['key']] = G['ev'](p, Y)

    # ---- the patched worlds ---------------------------------------------------------------------
    def make_pi(one_sided):
        def rho_a(g, p):
            k = G['o36_kappa'](p)
            if one_sided and k >= 1.0:
                return G['rho31'](g)
            return G['rho31'](g) ** (1.0 / k)
        def pi_a(p, Yv, g=None, _Dov=None):
            gv = G['pv_games'](p, Yv) if g is None else float(g)
            r = rho_a(gv, p)
            pl = bool(p.get('_pool'))
            D = G['o31_D'](p, Yv) if _Dov is None else float(_Dov)
            pi = D * (1.0 - r) + G['phi31'](gv, G['o31_stall_run'](p, Yv), pl) * G['beta31'](gv, pl) * r
            if G['_O32S'] >= 6 and G['O32_ETA'] > 0.0 and gv > 0.0:
                pi *= ((G['o38_factor'](p, Yv, gv) if G['_O38'] else G['o37_factor'](p, Yv, gv)) if G['_O37'] else
                       max(0.0, 1.0 - G['O32_ETA'] * ((gv / G['O32_GAMMA_D']) * math.exp(1.0 - gv / G['O32_GAMMA_D']))))
            return pi
        return pi_a

    worlds = {}
    for tag, one in (('sym', False), ('one', True)):
        G['o31_pi'] = make_pi(one)
        try:
            w = {}
            for p in rows:
                repin()
                w[p['key']] = G['ev'](p, Y)
        finally:
            G['o31_pi'] = orig_pi
        worlds[tag] = w

    # ---- VALIDATION 2: restore reproduces byte-exact --------------------------------------------
    drift = 0
    for p in rows:
        repin()
        if G['ev'](p, Y) != base[p['key']]:
            drift += 1
    if drift:
        raise SystemExit('mech_a HALT: after restore, %d rows do not reproduce the live price — the '
                         'patch leaked state; the study is void.' % drift)

    # ---- the movers list ------------------------------------------------------------------------
    movers, viol_gameless = [], 0
    for p in rows:
        k = p['key']
        b_now = int(round(base[k] / F))
        b_sym = int(round(worlds['sym'][k] / F))
        b_one = int(round(worlds['one'][k] / F))
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        gtot = sum(x.get('games', 0) for x in sc)
        if gtot == 0 and (b_sym != b_now or b_one != b_now):
            viol_gameless += 1
        if b_sym == b_now and b_one == b_now and k not in NAMED:
            continue
        repin()
        movers.append({
            'key': k, 'player': p.get('player'), 'pos': MA.gfut(p), 'route': p.get('type'),
            'pick': p.get('pick'), 'entry': p.get('year'), 'tenure': Y - int(p.get('year') or Y) + 1,
            'games': int(gtot),
            'cameo': round(sum(x['avg'] * x['games'] for x in sc) / gtot, 1) if gtot else None,
            'kappa': round(G['o36_kappa'](p), 3), 'rho': round(G['rho31'](G['pv_games'](p, Y)), 4),
            'pi_now': round(orig_pi(p, Y), 4),
            'board_now': b_now, 'board_sym': b_sym, 'board_one': b_one,
            'd_sym': b_sym - b_now, 'd_one': b_one - b_now,
            'd7_guarded': k in G['_D7_FLOOR'], 'named': k in NAMED,
        })
    if viol_gameless:
        raise SystemExit('mech_a HALT: %d GAMELESS rows moved — rho_a(0)=0 should make that '
                         'impossible; the candidate form is not what this study declares.' % viol_gameless)
    movers.sort(key=lambda r: -abs(r['d_sym']))
    tot_now = sum(int(round(v / F)) for v in base.values())
    out = {'meta': {'date': '2026-08-26', 'study': 'mechanism (a) capital-conditional maturation, '
           'rho_a=rho^(1/kappa) inside pi only; in-memory patch, engine prices everything; '
           'restore proven byte-exact on all %d rows' % len(rows),
           'board_total_now': tot_now,
           'board_total_sym': tot_now + sum(m['d_sym'] for m in movers),
           'board_total_one': tot_now + sum(m['d_one'] for m in movers),
           'n_movers_sym': sum(1 for m in movers if m['d_sym']),
           'n_movers_one': sum(1 for m in movers if m['d_one'])},
           'movers': movers}
    json.dump(out, open(OUT, 'w'), indent=1)
    return {'n_rows': len(rows), 'movers_sym': out['meta']['n_movers_sym'],
            'movers_one': out['meta']['n_movers_one'],
            'net_sym': sum(m['d_sym'] for m in movers), 'net_one': sum(m['d_one'] for m in movers),
            'out': OUT}
