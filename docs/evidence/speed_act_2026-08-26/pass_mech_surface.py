"""MECH-SURFACE PRICING STUDY — the evidence-conditional capital-retention surface (owner: "Yes please",
2026-08-27), replacing the dead flat floor (v868/v869).

READ-ONLY STUDY, mech_fit skeleton (in-memory patch, real ev() prices everything, byte-exact restore
+ out-of-class invariance asserted). THE DECLARED SURFACE — every number is a measured cell loading
from the resolved cohorts (v869), CONSERVATIVE fixed-horizon line, floored at 0, capped at the
banked-mediocre ceiling (v868: 0.81 mobile / 0.92 tall):

    L(family, evidence, elapsed):            t2/t3            t4
      MOBILE  no games                        0.31            0.01
      MOBILE  poor cameo   (rel<=0.40)       0.19            0.00
      MOBILE  decent cameo (rel=0.525)       0.45            0.66
      MOBILE  good cameo   (rel>=0.65)       0.41            0.66
      TALL    no games                        0.70            0.25
      TALL    poor cameo                      0.21            0.00
      TALL    decent cameo                    0.92*           0.67
      TALL    good cameo                      0.92*           0.67      (*capped from 1.33/0.99)

    rel = career cameo average / position REPL bar; PIECEWISE-LINEAR between the knots 0.40 -> 0.525
    -> 0.65 (no cliff at the 0.45 boundary — mccabe sits on it); pi floored at L inside the class,
    untouched outside. THE CLASS unchanged: no career 6-game season, tenure 2-4, entry age <22.

    THE OWNER'S RULE (v869, hard): no in-class row may end ABOVE his draft-day price on this lift —
    applied as a price cap: fit <= max(current price, draft v0). A row already above draft (route
    floors, e.g. burton) is not lifted further and not clawed back — the cap stops gains past draft,
    it does not repossess standing prices.

Falsifiers: byte-exact restore all rows; zero out-of-class movement; zero rows above the draft cap.
"""
import json

OUT = '/home/user/afl-rl-engine/docs/evidence/speed_act_2026-08-26/MECH_SURFACE_MOVERS.json'
Y = 2026
TALL = {'RUCK', 'KPF', 'KPD'}
L_TABLE = {  # (family, era): [none, poor, decent, good]  era: 0 = t2/t3, 1 = t4
    ('MOBILE', 0): [0.31, 0.19, 0.45, 0.41], ('MOBILE', 1): [0.01, 0.00, 0.66, 0.66],
    ('TALL', 0):   [0.70, 0.21, 0.92, 0.92], ('TALL', 1):   [0.25, 0.00, 0.67, 0.67],
}
KNOTS = (0.40, 0.525, 0.65)
NAMED = {'harrison-oliver', 'thomas-burton', 'noah-roberts-thomson', 'lucas-camporeale',
         'cody-angove', 'zane-peucker', 'archie-ludowyke', 'ollie-greeves', 'noah-howes',
         'rhys-unwin', 'luke-kennedy', 'william-mccabe', 'taylor-goad', 'riak-andrew',
         'matt-whitlock', 'will-green'}


def run(ns):
    G, MA = ns['G'], ns['MA']
    for sym in ('o31_pi', 'ev', '_ev_pre45', '_PL_F'):
        if sym not in G:
            raise SystemExit('mech_surface HALT: engine symbol %r absent.' % sym)
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

    def L_of(p):
        fam = 'TALL' if MA.gfut(p) in TALL else 'MOBILE'
        era = 1 if (Y - int(p.get('year') or Y) + 1) >= 4 else 0
        t = L_TABLE[(fam, era)]
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        g = sum(x.get('games', 0) for x in sc)
        if g == 0:
            return t[0]
        rel = (sum(x['avg'] * x['games'] for x in sc) / g) / MA.REPL[MA.gfut(p)]
        lo, mid, hi = KNOTS
        if rel <= lo:
            return t[1]
        if rel <= mid:
            return t[1] + (t[2] - t[1]) * (rel - lo) / (mid - lo)
        if rel <= hi:
            return t[2] + (t[3] - t[2]) * (rel - mid) / (hi - mid)
        return t[3]

    def pi_surface(p, Yv, g=None, _Dov=None):
        v = orig_pi(p, Yv, g, _Dov)
        if in_class(p):
            return max(v, L_of(p))
        return v

    base, cls = {}, {}
    for p in rows:
        repin()
        base[p['key']] = G['ev'](p, Y)
        cls[p['key']] = in_class(p)

    G['o31_pi'] = pi_surface
    try:
        fit = {}
        for p in rows:
            repin()
            fit[p['key']] = G['ev'](p, Y)
    finally:
        G['o31_pi'] = orig_pi

    drift = sum(1 for p in rows if (repin() or G['ev'](p, Y)) != base[p['key']])
    if drift:
        raise SystemExit('mech_surface HALT: %d rows fail byte-exact restore — void.' % drift)
    leak = [p['key'] for p in rows
            if not cls[p['key']] and int(round(fit[p['key']] / F)) != int(round(base[p['key']] / F))]
    if leak:
        raise SystemExit('mech_surface HALT: %d out-of-class rows moved (%s...) — void.' % (len(leak), leak[:5]))

    movers, capped_n = [], 0
    for p in rows:
        k = p['key']
        b_now = int(round(base[k] / F))
        b_raw = int(round(fit[k] / F))
        movers.append((p, b_now, b_raw))
    # draft-day price for the cap: the engine's own day0_v0 (board currency)
    out_rows = []
    for p, b_now, b_raw in movers:
        k = p['key']
        repin()
        d0 = G['day0_v0'](p)
        v0b = int(round(d0)) if d0 is not None else None
        cap = max(b_now, v0b) if v0b is not None else b_raw
        b_fit = min(b_raw, cap)
        if b_fit != b_raw:
            capped_n += 1
        if b_fit == b_now and k not in NAMED:
            continue
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        gtot = sum(x.get('games', 0) for x in sc)
        cam = round(sum(x['avg'] * x['games'] for x in sc) / gtot, 1) if gtot else None
        out_rows.append({
            'key': k, 'player': p.get('player'), 'pos': MA.gfut(p),
            'fam': 'TALL' if MA.gfut(p) in TALL else 'MOBILE',
            'route': p.get('type'), 'pick': p.get('pick'),
            'tenure': Y - int(p.get('year') or Y) + 1, 'games': int(gtot), 'cameo': cam,
            'rel': round(cam / MA.REPL[MA.gfut(p)], 2) if cam else None,
            'L': round(L_of(p), 2) if cls[k] else None,
            'v0_draft': v0b, 'board_now': b_now, 'board_fit': b_fit,
            'delta': b_fit - b_now, 'capped_at_draft': b_fit != b_raw,
            'named': k in NAMED,
        })
    out_rows.sort(key=lambda r: -abs(r['delta']))
    tot0 = sum(int(round(v / F)) for v in base.values())
    net = sum(m['delta'] for m in out_rows)
    out = {'meta': {'date': '2026-08-27',
           'form': 'evidence-conditional capital-retention surface (v869 measured cells, conservative '
                   'fixed-horizon line), piecewise-linear in rel across knots 0.40/0.525/0.65, era t2-3 vs '
                   't4, capped at the banked-mediocre ceiling (0.81/0.92) and at the draft-day price '
                   '(owner rule); class and falsifiers as mech_fit',
           'validations': 'restore byte-exact; out-of-class invariance; draft cap applied to %d rows' % capped_n,
           'board_total_now': tot0, 'board_total_fit': tot0 + net,
           'n_movers': sum(1 for m in out_rows if m['delta'])},
           'movers': out_rows}
    json.dump(out, open(OUT, 'w'), indent=1)
    return {'n_rows': len(rows), 'movers': out['meta']['n_movers'], 'net': net,
            'capped_at_draft': capped_n, 'out': OUT}
