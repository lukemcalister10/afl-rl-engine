"""AVAILABILITY SMOOTHING STUDY — boolean vs exposure-blend, DIRECT movers only.

Owner ask (2026-08-28, verbatim): "Let's look at the smoothed vs boolean and a movers list
(direct movers only) if we smooth it." Context: the Taylor/Taylor cliff — a 2-game cameo fully
shields the draft prior (xavier-taylor 0.95x of v0) while zero games takes the sitter channel
(oskar-taylor 0.81x), and the gap is a boolean of games>0, not a gradient.

THE CANDIDATE, stated exactly: a player's price becomes the exposure blend of the two channels
the engine already computes —

    v_smoothed = w(cg) * v_live + (1 - w(cg)) * v_sitter,     w(cg) = 1 - exp(-cg / TAU)

where v_live is today's full-path price, v_sitter is the engine's OWN sitter counterfactual for
the same player (scoring stripped -> re-priced -> restored; the verify_cf.py method of record,
same as pass_pedigree_decomp), cg is career games, and TAU=4 so the sitter share is ~100% at 0
games, 39% absorbed at 2 games, ~90% gone by 9. A 0-game row blends to its own counterfactual
identically — sitters move by 0 BY CONSTRUCTION, which the pass asserts. This is a STUDY: it
writes one JSON of evidence and touches no board, no store, no bake.

DIRECT movers only (the owner's words): the per-row blend delta. No re-ranking, no conservation
re-spread, no downstream lens — those belong to a candidate build if the dial is adopted.

Currency discipline: ev() is probed against the shipped board (data/rl_build active[].v) on the
played young class in BOTH conventions (raw and /_PL_F); the convention that reproduces the board
is used, and if neither reproduces >=90% of probes the pass HALTS rather than emit a table in a
wrong currency.
"""
import json, math, os

OUT = '/home/user/afl-rl-engine/docs/evidence/avail_smoothing_2026-08-28/AVAIL_SMOOTHING_STUDY.json'
Y = 2026
TAU = 4.0
NAMED = ['oskar-taylor', 'xavier-taylor', 'dylan-patterson', 'daniel-annable', 'lachy-dovaston',
         'max-kondogiannis', 'kye-fincher', 'matthew-leray', 'finnegan-davis', 'harley-barker']


def run(ns):
    G, MA = ns['G'], ns['MA']
    ev = G['ev']
    F = G['_PL_F']

    board = {r['key']: r for r in json.load(
        open(os.path.join(ns['repo'], 'data', 'rl_build', 'rl_app_data.json')))['active']}

    # ---- the class: young rows (tenure 1-4, not mature-age), any games ------------------------
    rows = []
    for p in MA.data:
        if p.get('_retired') or not p.get('key'):
            continue
        yr = int(p.get('year') or 0)
        ten = Y - yr + 1
        if not (1 <= ten <= 4):
            continue
        by = p.get('_by')
        if not by:
            raise SystemExit('HALT: %r has no _by — mature-age test cannot run silently.' % p['key'])
        if yr - int(by) >= 22:
            continue                                    # D3 convention: mature-agers excluded
        if p['key'] not in board:
            continue
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        gtot = sum(x.get('games', 0) for x in sc)
        if gtot > 12:
            continue                                    # w(13)=0.96: blend delta is noise past here
        rows.append((p, gtot))

    if not rows:
        raise SystemExit('HALT: empty class — the filters no longer match the list shape.')

    # ---- price both channels for every row ----------------------------------------------------
    def price(p):
        MA.BASE_REF = MA.AGE_REF = Y                    # clock discipline (H3 repair class)
        MA._pe_clear()
        return float(ev(p, Y))

    priced = []
    for p, gtot in rows:
        v_live_e = price(p)
        s0 = p['scoring']
        p['scoring'] = []                               # the engine's own sitter counterfactual
        try:
            v_sit_e = price(p)
        finally:
            p['scoring'] = s0
        priced.append((p, gtot, v_live_e, v_sit_e))

    # ---- currency probe: which convention reproduces the shipped board? -----------------------
    def agree(conv):
        n = ok = 0
        for p, gtot, v_live_e, _ in priced:
            n += 1
            if abs(round(v_live_e / conv) - board[p['key']]['v']) <= 1:
                ok += 1
        return ok, n
    ok_raw, n = agree(1.0)
    ok_f, _ = agree(F)
    if ok_f >= ok_raw and ok_f >= 0.9 * n:
        conv, conv_name = F, 'engine/_PL_F'
    elif ok_raw > ok_f and ok_raw >= 0.9 * n:
        conv, conv_name = 1.0, 'raw'
    else:
        raise SystemExit('HALT: neither currency reproduces the board (raw %d/%d, /F %d/%d) — '
                         'wrong conversion would mislabel every figure; map it, do not guess.'
                         % (ok_raw, n, ok_f, n))

    # ---- the blend ----------------------------------------------------------------------------
    out_rows, sitter_viol = [], []
    for p, gtot, v_live_e, v_sit_e in priced:
        v_live = round(v_live_e / conv)
        v_sit = round(v_sit_e / conv)
        w = 1.0 - math.exp(-gtot / TAU)
        v_sm = round(w * v_live + (1.0 - w) * v_sit)
        d = v_sm - v_live
        if gtot == 0 and d != 0:
            sitter_viol.append(p['key'])
        b = board[p['key']]
        out_rows.append({
            'key': p['key'], 'name': p.get('player'), 'pk': b.get('pk'), 'yr': b.get('yr'),
            'grp': b.get('grp'), 'games': gtot, 'w': round(w, 3),
            'v_live': v_live, 'v_sitter': v_sit, 'v_smoothed': v_sm, 'delta': d,
            'board_v': b['v'],
        })
    if sitter_viol:
        raise SystemExit('HALT: %d sitter rows moved under the blend — the construction identity '
                         'failed: %s' % (len(sitter_viol), sitter_viol[:5]))

    movers = sorted([r for r in out_rows if r['delta'] != 0], key=lambda r: r['delta'])
    named = [r for r in out_rows if r['key'] in NAMED]
    verdict = {
        'params': {'TAU': TAU, 'w': '1-exp(-games/TAU)', 'Y': Y,
                   'currency': conv_name, 'currency_probe': {'raw': ok_raw, 'over_F': ok_f, 'n': n}},
        'class_size': len(out_rows),
        'movers_n': len(movers),
        'net_delta': sum(r['delta'] for r in movers),
        'sitters_unmoved': True,
        'named': named,
        'movers': movers,
    }
    json.dump(verdict, open(OUT, 'w'), indent=1)
    return {'class': len(out_rows), 'movers': len(movers),
            'net': verdict['net_delta'], 'currency': conv_name, 'out': OUT}
