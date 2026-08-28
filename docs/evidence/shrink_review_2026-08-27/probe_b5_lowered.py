"""B5 LOWERED-ROWS DIAGNOSIS (post-landing certification, 2026-08-28).

The first full ship-gates run on the ORDER 46 world returned B5 FAIL with lowered=9 (bar 0).
B5's PRE is ev_prefloor (the m3 blend: O46 in-body floor ON via the ambient flag, no year-zero
floor, no FINAL GUARD); EV is the finished price (year-zero floor + the FINAL GUARD, which
carries the owner-ruled day-0 cap: final = max(v_off, min(v, max(v_off, day0*F)))).

Hypothesis under test: every lowered row is an ORDER 46 in-class row whose ruled cap binds
(the m3-level surface lift exceeds max(v_off, day0*F)) — i.e. the ruled behavior, invisible to
B5's pre-O46 purity bar. Any lowered row NOT explained that way is a real defect.
"""
import json

OUT = '/home/user/afl-rl-engine/docs/evidence/shrink_review_2026-08-27/PROBE_B5_LOWERED.json'
Y = 2026


def run(ns):
    G, MA = ns['G'], ns['MA']
    F = G['_PL_F']
    ev, evp = G['ev'], G['ev_prefloor']
    o46_class = G['_o46_class']
    day0_v0 = G['day0_v0']
    delisted = ns.get('delisted') or G.get('delisted')

    def repin():
        MA.BASE_REF = MA.AGE_REF = Y
        MA._pe_clear()

    lowered = []
    n = 0
    for p in MA.data:
        if p.get('_retired'):
            continue
        n += 1
        repin()
        try:
            pre = float(evp(p, Y))
        except Exception:
            continue
        repin()
        fin = float(ev(p, Y))
        if fin < pre - 1e-9:
            in_class = bool(o46_class(p, Y))
            d0 = day0_v0(p)
            cap = (float(d0) * F) if d0 is not None else None
            lowered.append({
                'player': p.get('player'), 'key': p.get('key'), 'pos': MA.gfut(p),
                'type': p.get('type'), 'year': p.get('year'), 'pool': bool(p.get('_pool')),
                'delisted': bool(delisted(p)) if delisted else None,
                'pre_m3': round(pre, 1), 'final': round(fin, 1),
                'drop': round(pre - fin, 1),
                'o46_class': in_class,
                'day0_cap': round(cap, 1) if cap is not None else None,
                'cap_explains': (in_class and cap is not None and abs(fin - max(cap, 0)) < max(2.0, 0.01 * fin))
                                or (in_class and fin >= (cap or 0) - 1e-9),
            })
    unexplained = [r for r in lowered if not r['o46_class']]
    out = {'rows_scanned': n, 'lowered_n': len(lowered), 'lowered': lowered,
           'all_o46_class': all(r['o46_class'] for r in lowered),
           'unexplained_n': len(unexplained), 'unexplained': unexplained}
    json.dump(out, open(OUT, 'w'), indent=1)
    print('B5 probe: %d rows scanned, %d lowered, all in ORDER 46 class: %s, unexplained: %d'
          % (n, len(lowered), out['all_o46_class'], len(unexplained)))
    for r in lowered:
        print('  %-22s %-4s %-4s y%s  pre_m3=%-7s final=%-7s drop=%-6s o46=%s cap=%s'
              % (str(r['player'])[:22], r['pos'], r['type'], r['year'], r['pre_m3'],
                 r['final'], r['drop'], r['o46_class'], r['day0_cap']))
    return out['all_o46_class']
