"""MECH-FIT PRICING STUDY — the D5 fix sized by the measured outcome bounds (owner ask 2026-08-27:
"Can I see the movers list please, just for this change").

READ-ONLY STUDY, same machinery as pass_mech_a.py (in-memory patch of o31_pi, every row priced by
the real ev(), byte-exact restore proven). NOT a board, NOT a landing.

THE DECLARED CANDIDATE FORM — the conservative-bound capital-retention floor from the resolved-cohort
measurement (THIN_STATE_CAPITAL_OUTCOMES.json, register v866):

    inside THE THIN-EVIDENCE CLASS the pedigree multiplier is floored at the measured fair loading:
        pi_fit = max( pi_current , L[position-family] )
        L = 0.41 for mobiles (MID/SD/SF)   — the fixed-horizon slope, the LOWER bound of [0.41, 0.87]
        L = 0.91 for talls  (RUCK/KPF/KPD) — the fixed-horizon slope, the LOWER bound of [0.91, 1.43]

    THE CLASS (the boundary the engine already draws everywhere): no career season of >=6 games,
    tenure 2-4 (entry-year convention), entry age <22 (mature-agers stay the owner's own packet word,
    D3 convention). Outside the class pi is UNTOUCHED — a banked season exits a row to normal pricing.

Notes stated up front: (1) the floor also applies to each row's gameless counterfactual twin, so
cameo floors (and through them the ORDER 45 net) reprice consistently with the same world; (2) this
is the LOWER-bound sizing — the prereg may fit a shaped curve inside the bounds instead of a flat
floor, and must address the class-boundary step (L-SMOOTH) — boundary-adjacent rows are flagged in
the artifact; (3) sitter/cameo ORDERING inside the class is preserved (both sides floor equally and
cameo rows keep their production on top).

FALSIFIERS ASSERTED: (i) restore reproduces the live board BYTE-EXACT on all rows; (ii) NO
out-of-class row moves (their own pi is unfloored and the O45 net's scope excludes them) — one
violation voids the study.
"""
import json

OUT = '/home/user/afl-rl-engine/docs/evidence/speed_act_2026-08-26/MECH_FIT_MOVERS.json'
Y = 2026
TALL = {'RUCK', 'KPF', 'KPD'}
L_MOBILE, L_TALL = 0.41, 0.91
NAMED = {'harrison-oliver', 'thomas-burton', 'noah-roberts-thomson', 'lucas-camporeale',
         'cody-angove', 'zane-peucker', 'archie-ludowyke', 'ollie-greeves', 'noah-howes',
         'rhys-unwin', 'luke-kennedy', 'aidan-johnson'}


def run(ns):
    G, MA = ns['G'], ns['MA']
    for sym in ('o31_pi', 'ev', '_ev_pre45', '_PL_F', 'pv_games'):
        if sym not in G:
            raise SystemExit('mech_fit HALT: engine symbol %r absent — re-map, do not guess.' % sym)
    F = G['_PL_F']
    orig_pi = G['o31_pi']
    rows = [p for p in MA.data if not p.get('_retired') and p.get('key')]

    def repin():
        MA.BASE_REF = MA.AGE_REF = Y
        MA._pe_clear()

    def in_class(p):
        yr = int(p.get('year') or 0)
        ten = Y - yr + 1
        if not (2 <= ten <= 4):
            return False
        by = p.get('_by')
        if not by or yr - int(by) >= 22:
            return False
        return not any(x.get('games', 0) >= 6 for x in (p.get('scoring') or []) if x.get('year', 0) <= Y)

    def pi_fit(p, Yv, g=None, _Dov=None):
        v = orig_pi(p, Yv, g, _Dov)
        if in_class(p):
            return max(v, L_TALL if MA.gfut(p) in TALL else L_MOBILE)
        return v

    base, cls = {}, {}
    for p in rows:
        repin()
        base[p['key']] = G['ev'](p, Y)
        cls[p['key']] = in_class(p)

    G['o31_pi'] = pi_fit
    try:
        fit = {}
        for p in rows:
            repin()
            fit[p['key']] = G['ev'](p, Y)
    finally:
        G['o31_pi'] = orig_pi

    drift = 0
    for p in rows:
        repin()
        if G['ev'](p, Y) != base[p['key']]:
            drift += 1
    if drift:
        raise SystemExit('mech_fit HALT: %d rows fail the byte-exact restore — the study is void.' % drift)

    out_of_class_movers = [p['key'] for p in rows
                           if not cls[p['key']] and int(round(fit[p['key']] / F)) != int(round(base[p['key']] / F))]
    if out_of_class_movers:
        raise SystemExit('mech_fit HALT: %d OUT-OF-CLASS rows moved (%s ...) — the scope leaked; void.'
                         % (len(out_of_class_movers), out_of_class_movers[:5]))

    movers = []
    for p in rows:
        k = p['key']
        b0, b1 = int(round(base[k] / F)), int(round(fit[k] / F))
        if b0 == b1 and k not in NAMED:
            continue
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        gtot = sum(x.get('games', 0) for x in sc)
        repin()
        movers.append({
            'key': k, 'player': p.get('player'), 'pos': MA.gfut(p),
            'fam': 'TALL' if MA.gfut(p) in TALL else 'MOBILE',
            'route': p.get('type'), 'pick': p.get('pick'), 'entry': p.get('year'),
            'tenure': Y - int(p.get('year') or Y) + 1, 'games': int(gtot),
            'cameo': round(sum(x['avg'] * x['games'] for x in sc) / gtot, 1) if gtot else None,
            'pi_now': round(orig_pi(p, Y), 3),
            'floor': (L_TALL if MA.gfut(p) in TALL else L_MOBILE) if cls[k] else None,
            'board_now': b0, 'board_fit': b1, 'delta': b1 - b0,
            'boundary_5g': any(x.get('games', 0) == 5 for x in sc),
            'named': k in NAMED,
        })
    movers.sort(key=lambda r: -abs(r['delta']))
    tot0 = sum(int(round(v / F)) for v in base.values())
    net = sum(m['delta'] for m in movers)
    out = {'meta': {'date': '2026-08-27',
           'form': 'pi floored at the measured conservative loading inside the thin-evidence class '
                   '(no 6-game season, t2-4, entry age <22): L=0.41 mobile / 0.91 tall; outside the '
                   'class untouched. Lower-bound sizing of v866; the prereg fits a shaped curve inside '
                   'the bounds.',
           'validations': 'restore byte-exact %d/%d; out-of-class invariance held' % (len(rows), len(rows)),
           'board_total_now': tot0, 'board_total_fit': tot0 + net,
           'n_movers': sum(1 for m in movers if m['delta'])},
           'movers': movers}
    json.dump(out, open(OUT, 'w'), indent=1)
    return {'n_rows': len(rows), 'movers': out['meta']['n_movers'], 'net': net, 'out': OUT}
