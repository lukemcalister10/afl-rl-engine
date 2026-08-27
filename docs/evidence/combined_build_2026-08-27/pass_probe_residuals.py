"""RESIDUAL ATTRIBUTION PROBE — the 7 rows the board verification could not attribute, plus two
exact-match controls. One engine load (candidate world: baked curve, refit v0surf, dials on);
each row is priced under in-process dial toggles so every residual gets a per-lever attribution:
    full      all dials as built (must reproduce the board row exactly — parity anchor)
    no_o48    _O48_W=0    (the easing's contribution)
    no_o47    _O47=False  (the step-up's contribution)
    no_o46    _O46=False  (the surface floor+cap's contribution)
    dials_off all three   (what remains = smoothing/v0surf channel vs the live board)
"""
import json

OUT = '/home/user/cand_build/root/docs/evidence/combined_build_2026-08-27/PROBE_RESIDUALS.json'
KEYS = ['noah-mraz', 'taylor-goad', 'will-green', 'wil-dawson', 'jordan-croft',
        'latrelle-pickett', 'rhys-unwin', 'charlie-edwards', 'harrison-oliver']
Y = 2026


def run(ns):
    G, MA = ns['G'], ns['MA']
    F = G['_PL_F']
    rows = {p['key']: p for p in MA.data if p.get('key') in KEYS}

    def repin():
        MA.BASE_REF = MA.AGE_REF = Y
        MA._pe_clear()

    def price(p):
        repin()
        return int(round(G['ev'](p, Y) / F))

    out = {}
    base_flags = (G['_O46'], G['_O47'], G['_O48_W'])
    for k in KEYS:
        p = rows.get(k)
        if p is None:
            out[k] = 'MISSING'
            continue
        sc = [(x.get('year'), x.get('games', 0)) for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        bk = sum(1 for _, g in sc if g >= 6)
        repin()
        g = sum(gg for _, gg in sc)
        d = {'pos': MA.gfut(p), 'route': p.get('type'), 'pick': p.get('pick'),
             'year': p.get('year'), 'by': p.get('_by'), 'seasons': sc, 'bk': bk,
             'o46_class': bool(G['_o46_class'](p, Y)), 'o47_class': bool(G['_o47_class'](p, Y)),
             'L': round(G['_o46_L'](p, Y), 4) if G['_o46_class'](p, Y) else None,
             'o31_D': round(G['o31_D'](p, Y), 4),
             'pi': round(G['o31_pi'](p, Y, float(g)), 4),
             'pi_nofloor': round(G['o31_pi'](p, Y, float(g), _nofloor=True), 4),
             'day0_v0': (lambda v: round(v, 1) if v is not None else None)(G['day0_v0'](p))}
        d['full'] = price(p)
        G['_O48_W'] = 0.0
        d['no_o48'] = price(p)
        G['_O48_W'] = base_flags[2]
        G['_O47'] = False
        d['no_o47'] = price(p)
        G['_O47'] = base_flags[1]
        G['_O46'] = False
        d['no_o46'] = price(p)
        G['_O46'] = base_flags[0]
        G['_O46'] = False; G['_O47'] = False; G['_O48_W'] = 0.0
        d['dials_off'] = price(p)
        G['_O46'], G['_O47'], G['_O48_W'] = base_flags
        # restore proof on this row
        if price(p) != d['full']:
            raise SystemExit('probe HALT: %s did not restore after toggles.' % k)
        out[k] = d
    json.dump(out, open(OUT, 'w'), indent=1)
    return {'out': OUT, 'n': len(out)}
