"""Fine (1-point) score sweep with full pricing decomposition, for the two anchored trough rows."""
import copy, json, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']; PR = G['PR']
F = 1.052329
Y = 2026


def gv(n):
    return G.get(n)


def rec_point(p):
    r = {}

    def t(key, fn):
        try:
            v = fn()
            if isinstance(v, (np.floating,)):
                v = float(v)
            if isinstance(v, np.ndarray):
                v = [float(x) for x in v]
            r[key] = v
        except Exception as e:
            r[key] = 'ERR:%s' % e

    t('v_board', lambda: ev(p, Y) / F)
    t('ev_eng', lambda: ev(p, Y))
    t('ev_prefloor', lambda: gv('ev_prefloor')(p, Y))
    t('ev_click', lambda: gv('_ev_click')(p, Y))

    def pin():
        G['_M3PIN']['on'] = True
        try:
            return gv('_ev_click')(p, Y)
        finally:
            G['_M3PIN']['on'] = False
    t('ev_pin', pin)
    t('m3_s', lambda: gv('_m3_s')(p, Y))

    t('prod_path', lambda: gv('_prod_path')(p, Y))
    t('raw_ev', lambda: gv('raw_ev')(p, Y))
    t('iso_eff', lambda: gv('iso_eff')(p, Y))
    t('bb', lambda: [float(x) for x in gv('b6')(p, Y)])
    t('price6', lambda: gv('price6')(p, gv('b6')(p, Y), Y))
    t('feat', lambda: [float(x) for x in cp._feat(p, Y)])
    t('lvl_eff', lambda: float(cp._lvl_eff(p, Y)))
    t('lvl_eff_orig', lambda: float(cp._lvl_eff_orig(p, Y)))
    t('coreM1', lambda: float(gv('_coreM1')(p, Y)))
    t('lvlcurr', lambda: float(gv('_lvlcurr')(p, Y)))
    t('par_prior', lambda: float(gv('_par_prior')(p, Y)))
    t('bestlvl', lambda: float(gv('bestlvl')(p, Y)))
    t('lvl_wt', lambda: float(cp._lvl_wt(p, Y)))
    t('exposure', lambda: float(cp._exposure(p, Y)))
    t('Eq', lambda: float(gv('_ev_qual')(p, Y)))
    t('ev_rec', lambda: float(gv('_ev_rec')(gv('_ev_qual')(p, Y))))
    t('ev_est', lambda: float(gv('_ev_est')(gv('_ev_qual')(p, Y))))
    t('ev_pw', lambda: float(gv('_ev_pw')(gv('_ev_qual')(p, Y))))
    t('eo', lambda: float(gv('_eo')(p, Y)))
    t('expgate', lambda: float(gv('_expgate')(p, Y)))
    t('radq', lambda: bool(gv('_radq')(p, Y, cp._lvl_eff_orig(p, Y))))
    t('v0_start', lambda: float(gv('v0_start')(p)))
    t('entry_anchor', lambda: float(gv('entry_anchor')(p)))
    t('nseas_pro', lambda: gv('nseas_pro')(p, Y))
    t('tenure', lambda: PR.tenure(p, Y))
    t('h_cut', lambda: float(gv('_h_cut')(p, Y)))
    t('stale_grade', lambda: float(gv('_staleness_grade')(p, Y, MA.gfut(p))))
    t('a_share', lambda: float(gv('_a_share')(p, Y)))
    t('first_evidence', lambda: bool(gv('_first_evidence')(p, Y)))
    # the ITEM A blend, reconstructed from its own parts
    try:
        e = gv('_prod_path')(p, Y) * gv('_h_cut')(p, Y)
        tau = max(0.0, Y - cp.debutyr(p)) + (gv('_fEy')(Y, p) ** 1.5)
        R = gv('_R_surf')(gv('_sitout_cls')(MA.gfut(p)), MA.effpk(p), tau)
        anch0 = R * gv('entry_anchor')(p)
        w = gv('_c_w')(p, Y, e, gv('entry_anchor')(p))
        anch = anch0 * (1.0 + w * (gv('C_H') - 1.0))
        s = gv('_a_share')(p, Y)
        r['A_tau'] = float(tau); r['A_R'] = float(R); r['A_anch0'] = float(anch0)
        r['A_w'] = float(w); r['A_anch'] = float(anch); r['A_s'] = float(s)
        r['A_e_pre'] = float(e); r['A_blend'] = float((1 - s) * e + s * anch)
    except Exception as ex:
        r['A_err'] = str(ex)
    return r


CASES = [('Max Kondogiannis', 9, 36.6), ('Josh Dolan', 9, 50.09)]
out = {}
for nm, g0, a0 in CASES:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        print('MISSING', nm); continue
    saved = copy.deepcopy(p['scoring'])
    v_before = ev(p, Y) / F
    row = next(x for x in p['scoring'] if x['year'] == Y)
    rows = []
    for sc in range(0, 151):
        row['games'] = g0 + 1
        row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        d = {'score': sc, 'avg': row['avg']}
        d.update(rec_point(p))
        rows.append(d)
    p['scoring'] = saved
    v_after = ev(p, Y) / F
    out[nm] = {'g0': g0, 'a0': a0, 'v_before': v_before, 'v_after': v_after,
               'rt': abs(v_before - v_after) < 1e-9, 'rows': rows}
    print('%s shipped=%.3f restored=%.3f rt=%s' % (nm, v_before, v_after, out[nm]['rt']))
    vs = [x['v_board'] for x in rows]
    print('  v at 0/30/40/48/60/71/90/120/140: ' +
          ' '.join('%d:%.1f' % (s, vs[s]) for s in (0, 30, 40, 48, 60, 71, 90, 120, 140)))
    steps = sorted(((vs[i + 1] - vs[i], i) for i in range(len(vs) - 1)), key=lambda t: abs(t[0]), reverse=True)[:10]
    print('  biggest 1-point steps:')
    for d, i in steps:
        print('    score %3d->%3d  avg %.4f->%.4f  v %8.2f->%8.2f  (%+8.2f)'
              % (i, i + 1, rows[i]['avg'], rows[i + 1]['avg'], vs[i], vs[i + 1], d))

json.dump(out, open(OUTBASE + '.json', 'w'), indent=1, default=str)
print('WROTE', OUTBASE + '.json')
