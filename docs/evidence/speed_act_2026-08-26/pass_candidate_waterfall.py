"""THE CANDIDATE WATERFALL — one board, every direct mover tracked live -> end candidate, with the
change attributed to each mechanism as it stacks (owner ask, 2026-08-27).

READ-ONLY STUDY on the harness. THE STACK, engine-priced stage by stage through the real ev():
    S0  the LIVE board (baseline sweep)
    S1  + CURVE SMOOTHING S_LL5G — the filed smoothed position curve replaces the day-0 posv table
        in memory (docs/evidence/curve_smooth_study_2026-08-25/S_LL5G_POSV.json; recipe approved,
        confirmation word pending). Moves day-0 anchors, so the young lane's pedigree legs, cameo
        floors and the O45 net all reprice through it.
    S2  + THE PEDIGREE SURFACE (v870 form, word pending): retention floored at the measured cells,
        smoothed in evidence-quality, era t2-3/t4, banked-mediocre ceiling; THE DRAFT CAP is taken
        against the CANDIDATE'S OWN day-0 law (the smoothed v0) — the owner's no-gain-past-draft
        rule lives in the same world as the curve it caps against.

NOT ENGINE-PRICED, DECLARED AS THE PENDING OVERLAY (each lacks a word or a derived law): the
survivorship STEP-UP class (~19 two-sat gameless ND sitters — RULED, but its levels come from the
redesigned fade law the build derives; the registered benchmark rides in the output: dodson board
~85 -> ~100); the POOL DEPTH-3 CAP (17 rows, direction DOWN, his word pending); the O45 BOUNDARY
EASING (ruled "it should fade out" pre-v871 — v871's measured 0.26-vs-0.93 boundary step is the
standing tension for his re-word); MSD wrinkle + t5+ group (design pending); the CONSERVATION
RE-LEVEL (applies at the landing; the totals here are raw).

Falsifiers: full restore reproduces the live board BYTE-EXACT on all rows; stage S2 moves no
out-of-class row beyond S1 (the surface's scope leak check, in the smoothed world).
"""
import json

OUT = '/home/user/afl-rl-engine/docs/evidence/speed_act_2026-08-26/CANDIDATE_WATERFALL.json'
SMOOTH = '/home/user/afl-rl-engine/docs/evidence/curve_smooth_study_2026-08-25/S_LL5G_POSV.json'
Y = 2026
TALL = {'RUCK', 'KPF', 'KPD'}
L_TABLE = {('MOBILE', 0): [0.31, 0.19, 0.45, 0.41], ('MOBILE', 1): [0.01, 0.00, 0.66, 0.66],
           ('TALL', 0):   [0.70, 0.21, 0.92, 0.92], ('TALL', 1):   [0.25, 0.00, 0.67, 0.67]}
KNOTS = (0.40, 0.525, 0.65)
NAMED = {'harrison-oliver', 'thomas-burton', 'william-mccabe', 'taylor-goad', 'james-leake',
         'riak-andrew', 'alex-dodson', 'cody-angove', 'lucas-camporeale', 'ashton-moir'}


def run(ns):
    G, MA = ns['G'], ns['MA']
    for sym in ('o31_pi', 'ev', '_PL_F', '_POSV', 'day0_v0'):
        if sym not in G:
            raise SystemExit('waterfall HALT: engine symbol %r absent.' % sym)
    F = G['_PL_F']
    orig_pi, orig_posv = G['o31_pi'], G['_POSV']
    sm = json.load(open(SMOOTH))
    posv_s = {g: {int(k): float(v) for k, v in d.items()} for g, d in sm['posv'].items()}
    if set(posv_s) != set(orig_posv):
        raise SystemExit('waterfall HALT: smoothed posv position set %s != engine %s.'
                         % (sorted(posv_s), sorted(orig_posv)))
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
        if rel <= lo: return t[1]
        if rel <= mid: return t[1] + (t[2] - t[1]) * (rel - lo) / (mid - lo)
        if rel <= hi: return t[2] + (t[3] - t[2]) * (rel - mid) / (hi - mid)
        return t[3]

    def pi_surface(p, Yv, g=None, _Dov=None):
        v = orig_pi(p, Yv, g, _Dov)
        return max(v, L_of(p)) if in_class(p) else v

    def sweep():
        w = {}
        for p in rows:
            repin()
            w[p['key']] = G['ev'](p, Y)
        return w

    s0 = sweep()                                   # LIVE
    v0_live = {}
    for p in rows:
        repin()
        d = G['day0_v0'](p)
        v0_live[p['key']] = int(round(d)) if d is not None else None

    G['_POSV'] = posv_s
    try:
        s1 = sweep()                               # + smoothing
        v0_sm = {}
        for p in rows:
            repin()
            d = G['day0_v0'](p)
            v0_sm[p['key']] = int(round(d)) if d is not None else None
        G['o31_pi'] = pi_surface
        try:
            s2 = sweep()                           # + surface (in the smoothed world)
        finally:
            G['o31_pi'] = orig_pi
    finally:
        G['_POSV'] = orig_posv

    drift = 0
    for p in rows:
        repin()
        if G['ev'](p, Y) != s0[p['key']]:
            drift += 1
    if drift:
        raise SystemExit('waterfall HALT: %d rows fail byte-exact restore — void.' % drift)
    cls = {p['key']: in_class(p) for p in rows}
    leak = [p['key'] for p in rows if not cls[p['key']]
            and int(round(s2[p['key']] / F)) != int(round(s1[p['key']] / F))]
    if leak:
        raise SystemExit('waterfall HALT: surface stage moved %d out-of-class rows (%s...) — void.'
                         % (len(leak), leak[:5]))

    def stepup_class(p):
        # the RULED class: gameless ND sitters with two completed sat seasons (tenure 3), entry age <22
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        return (p.get('type') == 'ND' and sum(x.get('games', 0) for x in sc) == 0
                and (Y - int(p.get('year') or Y) + 1) == 3
                and p.get('_by') and int(p.get('year')) - int(p['_by']) < 22)

    out_rows = []
    for p in rows:
        k = p['key']
        b0 = int(round(s0[k] / F))
        b1 = int(round(s1[k] / F))
        b2r = int(round(s2[k] / F))
        cap = max(b1, v0_sm[k]) if v0_sm[k] is not None else b2r
        b2 = min(b2r, cap)                          # the owner's draft cap, in the candidate's own law
        if b2 == b0 and k not in NAMED and not stepup_class(p):
            continue
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        gtot = sum(x.get('games', 0) for x in sc)
        out_rows.append({
            'key': k, 'player': p.get('player'), 'pos': MA.gfut(p),
            'fam': 'TALL' if MA.gfut(p) in TALL else 'MOBILE', 'route': p.get('type'),
            'pick': p.get('pick'), 'tenure': Y - int(p.get('year') or Y) + 1, 'games': int(gtot),
            'cameo': round(sum(x['avg'] * x['games'] for x in sc) / gtot, 1) if gtot else None,
            'v0_live': v0_live[k], 'v0_cand': v0_sm[k],
            'b_live': b0, 'b_smooth': b1, 'b_cand': b2,
            'd_smooth': b1 - b0, 'd_surface': b2 - b1, 'd_total': b2 - b0,
            'd_vs_v0': (b2 - v0_live[k]) if v0_live[k] is not None else None,
            'capped': b2 != b2r, 'stepup_pending': stepup_class(p), 'named': k in NAMED,
        })
    out_rows.sort(key=lambda r: -abs(r['d_total']))
    t0 = sum(int(round(v / F)) for v in s0.values())
    t1 = sum(int(round(v / F)) for v in s1.values())
    t2 = t0 + sum(m['d_total'] for m in out_rows) + (t1 - t0 - sum(m['d_smooth'] for m in out_rows))
    out = {'meta': {'date': '2026-08-27',
           'stack': 'S0 live -> S1 +S_LL5G smoothing (in-memory posv swap) -> S2 +pedigree surface '
                    '(v870 form; draft cap vs the SMOOTHED day-0 law). Engine-priced end to end; '
                    'restore byte-exact; surface scope leak zero.',
           'pending_overlay': ['step-up class (ruled; levels await the redesigned fade law; registered '
                               'benchmark dodson board ~85->~100)', 'pool depth-3 cap (17 rows DOWN, word '
                               'pending)', 'O45 boundary easing (ruled pre-v871; re-word owed)',
                               'MSD wrinkle + t5+ (design pending)', 'conservation re-level (at landing)'],
           'board_total_live': t0, 'board_total_smooth': t1, 'board_total_cand': t2,
           'n_movers': sum(1 for m in out_rows if m['d_total'])},
           'movers': out_rows}
    json.dump(out, open(OUT, 'w'), indent=1)
    return {'n_rows': len(rows), 'movers': out['meta']['n_movers'],
            'net_smooth': t1 - t0, 'net_total': t2 - t0, 'out': OUT}
