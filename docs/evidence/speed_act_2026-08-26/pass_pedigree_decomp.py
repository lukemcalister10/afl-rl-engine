"""D5 ROOT-CAUSE DECOMPOSITION — the young-entrant pricing path, read from the engine's own symbols.

Owner directive (2026-08-26, verbatim, register v862): "It shouldn't be a targetted fix just to close
the Oliver Burton issue, but identify why Oliver is so under priced compared to a Burton and fix that
instead." This pass is the first step of that act: for every young thin-evidence row it decomposes the
live price into the stages the engine actually computes — day-0 anchor -> unplayed-clock fade
D_eff = D(c_u)^kappa x selection relief -> the one-law blend pi -> the pre-45 price -> the ORDER 45
net (lambda, cameo floor) -> the final board price. EVERY number is read from the loaded engine's own
functions (o31_D, o31_pi, o31_cu, o36_kappa, rho31, _ev_pre45, _o45_lam, _PL_F...), never re-derived —
the emit_matrix_31f precedent. Runs on tools/harness (one engine load).

TWO STRUCTURAL IDENTITIES ASSERTED PER ROW (the P15 spirit — the instrument proves it reads the real
path): (1) a gameless row's pre-45 price == day-0 anchor x o31_D (the :5384 rebinding, pi(0)==D);
(2) the cameo-floor strip/restore re-prices to the same pre-45 price EXACTLY (the D7-F6 rule).

NOTE ON A CORRECTED CHAT CLAIM: there is exactly ONE bar-scaled-knot ramp in this engine — the ORDER
45 lambda (bars = REPL - 3; SD lower knot 40 x 75.3/77.1 = 39.066). The earlier chat description of a
separate "cameo ramp knot" was wrong; the pre-45 games machinery is rho31/beta31/phi31/o41_credit,
none of it bar-scaled, and this pass reports rho31 as that family's representative.
"""
import json, os

OUT = '/home/user/afl-rl-engine/docs/evidence/speed_act_2026-08-26/PEDIGREE_DECOMP.json'
Y = 2026
NAMED = {'harrison-oliver', 'thomas-burton', 'noah-roberts-thomson', 'lucas-camporeale',
         'ben-jepson', 'aidan-johnson', 'ollie-greeves', 'archie-ludowyke', 'zane-peucker',
         'noah-howes', 'rhys-unwin', 'luke-kennedy', 'cody-angove', 'harry-o-farrell'}

def run(ns):
    G, MA = ns['G'], ns['MA']
    for sym in ('o31_D', 'o31_pi', 'o31_cu', 'o36_kappa', 'o32_sigma_sel', 'rho31', 'pv_games',
                'pv_pedigree', 'day0_v0', '_ev_pre45', '_o45_lam', '_O45_BARS', '_PL_F',
                'BASE_REF', 'AGE_REF', '_pe_clear', 'ev', 'nseas_pro'):
        if sym not in G:
            raise SystemExit('decomp HALT: engine symbol %r absent — the map this pass was built '
                             'against no longer matches the engine; re-map, do not guess.' % sym)
    F = G['_PL_F']
    rows, viol = [], []
    for p in MA.data:
        if p.get('_retired') or not p.get('key'):
            continue
        yr = int(p.get('year') or 0)
        ten = Y - yr + 1
        if not (1 <= ten <= 4):
            continue
        by = p.get('_by')
        if not by:
            raise SystemExit('decomp HALT: %r has no _by — the mature-age test cannot run silently.' % p['key'])
        if yr - int(by) >= 22:
            continue                                    # D3 convention: mature-agers are their own packet word
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        gtot = sum(x.get('games', 0) for x in sc)
        if gtot > 8 or any(x.get('games', 0) >= 6 for x in sc):
            continue                                    # thin-evidence class: 0-8 games, no banked level
        # THE CLOCK DISCIPLINE (H3 repair, rl_export.py:211): re-pin per row, always.
        G['BASE_REF'] = G['AGE_REF'] = Y
        G['_pe_clear']()
        pos = MA.gfut(p)
        if pos not in G['_O45_BARS']:
            raise SystemExit('decomp HALT: unresolved position group for %r (gfut=%r).' % (p['key'], pos))
        anchor_board = G['day0_v0'](p)                  # board currency day-0
        anchor = G['pv_pedigree'](p)                    # engine currency day-0 (= board x _PL_F)
        c_u = G['o31_cu'](p, Y)
        kappa = G['o36_kappa'](p)
        sig = G['o32_sigma_sel'](p, Y)
        D = G['o31_D'](p, Y)                            # the D7b-wrapped fade multiplier
        gpv = G['pv_games'](p, Y)
        pi = G['o31_pi'](p, Y)
        rho = G['rho31'](gpv)
        v_pre45 = G['_ev_pre45'](p, Y)
        # cameo floor: the engine's own counterfactual, method of record (verify_cf.py)
        s0 = p['scoring']
        p['scoring'] = []
        try:
            cf = G['_ev_pre45'](p, Y)
        finally:
            p['scoring'] = s0
        v_re = G['_ev_pre45'](p, Y)
        if v_re != v_pre45:
            raise SystemExit('decomp HALT: %r re-prices %r != %r after the cf strip/restore — the '
                             'D7-F6 non-destructive rule is broken; nothing this pass emits is safe.'
                             % (p['key'], v_re, v_pre45))
        cam = (sum(x['avg'] * x['games'] for x in sc) / gtot) if gtot >= 1 else None
        lam = G['_o45_lam'](cam, pos) if cam is not None else 0.0
        v_final = G['ev'](p, Y)
        if gtot == 0 and anchor is not None:
            drift = abs(v_pre45 - anchor * D)
            if drift > 1.0:
                viol.append({'key': p['key'], 'drift': round(drift, 2), 'v_pre45': v_pre45,
                             'anchor_x_D': round(anchor * D, 2)})
        rows.append({
            'key': p['key'], 'player': p.get('player'), 'pos': pos, 'route': p.get('type'),
            'pick': p.get('pick'), 'entry': yr, 'entry_age': yr - int(by), 'tenure': ten,
            'games': int(gtot), 'cameo': round(cam, 2) if cam is not None else None,
            'anchor_board': round(anchor_board, 1) if anchor_board is not None else None,
            'anchor_engine': round(anchor, 1) if anchor is not None else None,
            'c_u': round(c_u, 3), 'kappa': round(kappa, 3), 'sigma_sel': round(sig, 4),
            'D_eff': round(D, 4), 'pi': round(pi, 4), 'rho': round(rho, 4),
            'v_pre45': round(v_pre45, 1), 'cf': round(cf, 1), 'o45_lambda': round(lam, 4),
            'ev_final': round(v_final, 1),
            'board_final': int(round(v_final / F)), 'board_pre45': int(round(v_pre45 / F)),
            'board_cf': int(round(cf / F)),
            'retention': round((v_final / anchor), 3) if anchor else None,
            'named': p['key'] in NAMED,
        })
    rows.sort(key=lambda r: (-(r['anchor_engine'] or 0)))
    out = {'meta': {'date': '2026-08-26', 'Y': Y, 'engine_symbols': 'read live from G (map of record: '
           'the speed-act lane map)', 'cohort': 'tenure 1-4, entry age <22, 0-8 games, no banked level',
           'n': len(rows), 'gameless_identity_violations': viol, 'PL_F': F},
           'rows': rows}
    json.dump(out, open(OUT, 'w'), indent=1)
    named = [r for r in rows if r['named']]
    return {'n': len(rows), 'n_named': len(named), 'identity_violations': len(viol), 'out': OUT}
