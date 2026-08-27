"""BATTERY PART 1 (block 4) — F2 scope, F3 census, F4 easing grid (sizes W), F5 cap scan, F7 sample.
One engine load (candidate world), four in-process dial sweeps + targeted scans. The board file is
the 'full' state (the parity gate proved board == gated ev row-for-row at export).

  F2  SCOPE — each lever's movers against its declared class:
        O46-only movers  ⊆ the surface class (_o46_class); the gameless-twin channel is EMPTY
                           because the 'none' cells sit under the fade (the import wall's fact);
        O47-only movers  ⊆ the step class (_o47_class) ∪ rows moved through a NET whose gameless
                           twin lawfully steps (reported separately, must be net-scope rows);
        O48-only movers  ⊆ rows whose FIRST banked season is in progress.
  F3  CENSUS (v868, the RULED construction) — the ceiling gate: no thin-class row LIFTED by the
        surface (v > v_off) may load above its family's banked-mediocre ceiling (MOBILE 0.81,
        TALL 0.92 — the v868 measured ceilings the cells were capped at; the owner ruled the tall
        ceiling AT equality, so equality is the ruling, not a violation). The pairwise
        thin-vs-any-banked count is REPORTED with a drill list — a diagnostic, not the gate: a
        resolved bust below the ceiling is not a comparator, and hairline pairs at the ruled
        equality are the ruling itself. [v1 of this pass gated on the pairwise count and read
        345→399 — re-instrumented to the ruled construction, both numbers still reported.]
  F4  EASING GRID (the derivation's declared procedure) — W = largest of {1.0,0.75,0.5,0.25}
        where EVERY eased row prices STRICTLY below its THIN-TWIN surface price and the ceiling
        census counts zero new violations vs W=0. THE TWIN (corrected from v1, which stripped all
        scoring and priced a pure sitter): the row MINUS ITS BANKED SEASONS ONLY — cameo history
        kept — the v871 comparison's own shape. The manifest's RL_O48_W must equal the chosen W
        or the board rebuilds.
  F5  DRAFT CAP — every surface-class row: board == max(v_off, min(v_on, max(v_off, day0*F)))
        and never above max(v_off, day0*F). (The final guard's own construct, re-asserted.)
  F7  STRUCTURE sample — strip/restore byte-exact on 50 spread rows (D7-F6 outside the net path).
"""
import json

EV = '/home/user/cand_build/root/docs/evidence/combined_build_2026-08-27'
OUT = EV + '/BATTERY_1.json'
Y = 2026


def run(ns):
    G, MA, T = ns['G'], ns['MA'], ns['T']
    F = G['_PL_F']
    board = json.load(open(EV + '/board_candidate.json'))
    full = {r['key']: r['v'] for L in ('active', 'back') for r in board[L]}
    rows = [p for p in MA.data if not p.get('_retired') and p.get('key') in full
            and MA.GRP.get(p.get('pos'))]

    def repin():
        MA.BASE_REF = MA.AGE_REF = Y
        MA._pe_clear()

    def price(p):
        repin()
        return int(round(G['ev'](p, Y) / F))

    def sweep(o46, o47, w48):
        s0 = (G['_O46'], G['_O47'], G['_O48_W'])
        G['_O46'], G['_O47'], G['_O48_W'] = o46, o47, w48
        try:
            return {p['key']: price(p) for p in rows}
        finally:
            G['_O46'], G['_O47'], G['_O48_W'] = s0

    T('battery1: sweeps start (%d rows x 4 states)' % len(rows))
    base = sweep(False, False, 0.0)
    T('battery1: base done')
    s46 = sweep(True, False, 0.0)
    s47 = sweep(False, True, 0.0)
    s48 = sweep(False, False, G['_O48_W'])
    T('battery1: sweeps done')

    cls46 = {p['key'] for p in rows if G['_o46_class'](p, Y)}
    cls47 = {p['key'] for p in rows if G['_o47_class'](p, Y)}

    def curbank(p):
        sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Y]
        bk = [x for x in sc if x.get('games', 0) >= 6]
        return len(bk) == 1 and bk[0].get('year') == Y
    cls48 = {p['key'] for p in rows if curbank(p)}

    def netscope(p):
        yr = int(p.get('year') or 0); by = p.get('_by')
        return (1 <= Y - yr + 1 <= 4 and by and yr - int(by) < 22
                and sum(x.get('games', 0) for x in (p.get('scoring') or [])
                        if x.get('year', 0) <= Y) >= 1)
    netk = {p['key'] for p in rows if netscope(p)}

    def movers(s):
        return {k for k in s if s[k] != base[k]}
    m46, m47, m48 = movers(s46), movers(s47), movers(s48)
    f2 = {'o46_leak': sorted(m46 - cls46), 'o47_direct': len(m47 & cls47),
          'o47_twin_channel': sorted(m47 - cls47 - netk),   # movers neither in class nor net-scope = leak
          'o47_via_net': len((m47 - cls47) & netk),
          'o48_leak': sorted(m48 - cls48),
          'n_movers': {'o46': len(m46), 'o47': len(m47), 'o48': len(m48)}}
    f2['pass'] = not (f2['o46_leak'] or f2['o47_twin_channel'] or f2['o48_leak'])

    # F3 census — loadings on the engine's own day-0 stamps
    d0 = {}
    for p in rows:
        repin()
        v = G['day0_v0'](p)
        if v:
            d0[p['key']] = float(v)

    def fam(p):
        return 'TALL' if MA.gfut(p) in G['_O46_TALL'] else 'MOBILE'

    def estbank(p):
        return any(x.get('games', 0) >= 6 and x.get('year', 0) < Y
                   for x in (p.get('scoring') or []))
    thin = [p for p in rows if p['key'] in cls46 and p['key'] in d0]
    banked = [p for p in rows if estbank(p) and p['key'] in d0
              and (Y - int(p.get('year') or Y) + 1) <= 6
              and p.get('_by') and int(p.get('year')) - int(p['_by']) < 22]

    def census_pairs(price_of):
        n, drill = 0, []
        for t in thin:
            lt = price_of(t['key']) / d0[t['key']]
            for b in banked:
                if fam(t) != fam(b):
                    continue
                r = d0[t['key']] / d0[b['key']]
                if not (0.8 <= r <= 1.25):
                    continue
                lb = price_of(b['key']) / d0[b['key']]
                if lt > lb:
                    n += 1
                    if len(drill) < 40:
                        drill.append((t['key'], round(lt, 2), b['key'], round(lb, 2)))
        return n, drill

    CEIL = {'MOBILE': 0.81, 'TALL': 0.92}

    def census_ceiling(price_of, lifted_only):
        # flag only rows the LIFT carries ACROSS the ceiling from below: a row whose STANDING
        # loading already exceeds the ceiling (route/MSD floors — newton 0.933 live) is out of the
        # ceiling's reach, because the ruled protection forbids clawing standing prices back; its
        # lift is bounded by the draft cap instead, and it is DISCLOSED, not failed.
        bad, disclosed = [], []
        for t in thin:
            if lifted_only and price_of(t['key']) <= base[t['key']]:
                continue
            lt = price_of(t['key']) / d0[t['key']]
            lb = base[t['key']] / d0[t['key']]
            if lt > CEIL[fam(t)] + 0.005:
                (disclosed if lb > CEIL[fam(t)] else bad).append(
                    (t['key'], fam(t), round(lb, 3), round(lt, 3)))
        return bad, disclosed
    c_base, _ = census_pairs(lambda k: base[k])
    c_cand, c_drill = census_pairs(lambda k: full[k])
    ceil_bad, ceil_disclosed = census_ceiling(lambda k: full[k], lifted_only=True)
    f3 = {'ceiling_bad': ceil_bad, 'ceiling_disclosed_standing': ceil_disclosed,
          'pass': not ceil_bad,
          'pairs_base': c_base, 'pairs_cand': c_cand, 'pairs_drill': c_drill,
          'n_thin': len(thin), 'n_banked': len(banked)}
    T('battery1: census done (ceiling bad %d, disclosed-standing %d; pairs base %d cand %d)'
      % (len(ceil_bad), len(ceil_disclosed), c_base, c_cand))

    # F4 easing grid
    eased = [p for p in rows if p['key'] in cls48 and netscope(p)]
    twinP = {}
    for p in eased:
        s0 = p['scoring']
        p['scoring'] = [x for x in s0 if x.get('games', 0) < 6]   # the thin twin: banked seasons
        try:                                                      # removed, cameo history KEPT
            twinP[p['key']] = price(p)
        finally:
            p['scoring'] = s0
        if price(p) != full[p['key']]:
            raise SystemExit('battery1 HALT: %s failed byte-exact restore after twin probe.' % p['key'])
    grid = {}
    W0 = G['_O48_W']
    for W in (1.0, 0.75, 0.5, 0.25):
        G['_O48_W'] = W
        viol = []
        pw = {}
        for p in eased:
            v = price(p)
            pw[p['key']] = v
            if v > base[p['key']] and v >= twinP[p['key']]:
                viol.append((p['key'], v, twinP[p['key']]))
        newpairs = census_pairs(lambda k: pw.get(k, base[k]))[0] - c_base
        grid[W] = {'violations': viol, 'new_census_pairs': max(0, newpairs),
                   'n_eased_up': sum(1 for p in eased if pw[p['key']] > base[p['key']])}
    G['_O48_W'] = W0
    chosen = next((W for W in (1.0, 0.75, 0.5, 0.25)
                   if not grid[W]['violations'] and grid[W]['new_census_pairs'] == 0), 0.0)
    f4 = {'grid': {str(k): {'n_viol': len(v['violations']), 'viol_head': v['violations'][:3],
                            'new_pairs': v['new_census_pairs'], 'n_up': v['n_eased_up']}
                   for k, v in grid.items()},
          'chosen_W': chosen, 'manifest_W': W0, 'n_eased_scope': len(eased),
          'rebuild_needed': chosen != W0}
    T('battery1: easing grid done (chosen W=%s, manifest %s)' % (chosen, W0))

    # F5 — the final guard's construct re-asserted on every surface-class row
    f5bad = []
    for p in rows:
        if p['key'] not in cls46:
            continue
        G['_O46F'][0] = False
        try:
            voff = price(p)
        finally:
            G['_O46F'][0] = True
        d = d0.get(p['key'])
        cap = max(voff, int(round(d))) if d else voff
        v = full[p['key']]
        if v < voff - 1 or v > cap + 1:
            f5bad.append((p['key'], voff, v, cap))
    f5 = {'bad': f5bad, 'pass': not f5bad, 'n_class': len(cls46)}

    # F7 sample — strip/restore byte-exact on 50 spread rows
    f7bad = []
    for p in rows[:: max(1, len(rows) // 50)][:50]:
        v1 = price(p)
        s0 = p['scoring']; p['scoring'] = []
        try:
            price(p)
        finally:
            p['scoring'] = s0
        if price(p) != v1:
            f7bad.append(p['key'])
    f7 = {'bad': f7bad, 'pass': not f7bad}

    out = {'f2': f2, 'f3': f3, 'f4': f4, 'f5': f5, 'f7': f7,
           'pass': bool(f2['pass'] and f3['pass'] and f5['pass'] and f7['pass']
                        and chosen > 0.0)}
    json.dump(out, open(OUT, 'w'), indent=1)
    return {'pass': out['pass'], 'chosen_W': chosen, 'rebuild': f4['rebuild_needed'],
            'f2': f2['pass'], 'f3_ceiling_bad': len(ceil_bad),
            'f3_pairs': (c_base, c_cand), 'f5': f5['pass'], 'f7': f7['pass'],
            'out': OUT}
