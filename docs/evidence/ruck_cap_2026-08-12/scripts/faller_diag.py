"""ORDER 20C — WHY DO THREE POOL RUCKS GO **DOWN** WHEN THE CAP IS LIFTED?

Lifting a `min()` clamp should never lower a price, and on 14 of the 17 movers it does not. On three
(Flynn Riley, Alex Van Wyk, Vigo Visentini) the board falls by exactly 1. This decomposes those rows —
and a control row that RISES — through the sit-out path, term by term, at whatever cap the caller sets.

Everything is the engine's own function, called on the engine's own player object. Nothing re-derived.

Run: RL_REPO=<tree> RL_RUC_PRIOR_CAP=<cap> OUT=<path.json> python3 faller_diag.py
"""
import os, sys, io, json, contextlib

REPO = os.environ['RL_REPO']
OUT = os.environ.get('OUT', '/tmp/faller.json')
NAMES = os.environ.get('RC_NAMES', 'Flynn Riley,Alex Van Wyk,Vigo Visentini,Liam Reidy,Cameron Owen').split(',')

sys.path.insert(0, REPO + '/vendor')
os.chdir(REPO + '/engine/rl_after'); sys.path.insert(0, '.'); sys.path.insert(0, REPO)
_src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_o20c_faller'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_src, G)

import numpy as np
MA = G['MA']; cp = G['cp']
ev = G['ev']; _prod_path = G['_prod_path']; _ruc_ceiling = G['_ruc_ceiling']
_v0_uncapped = G['_v0_uncapped']; v0_start = G['v0_start']; entry_anchor = G['entry_anchor']
_R_surf = G['_R_surf']; _sitout_cls = G['_sitout_cls']; _fEy = G['_fEy']; _surprise = G['_surprise']
LAM_SIT = G['LAM_SIT']; sitout_ev = G['sitout_ev']; _h_cut = G['_h_cut']; nseas_pro = G['nseas_pro']
_c_w = G['_c_w']; C_H = G['C_H']; RUC_PRIOR_CAP = G['RUC_PRIOR_CAP']
F_NUM = json.load(open('pick_redenomination.json'))['factor']

_back = list(G.get('back_extra') or MA.__dict__.get('back_extra') or [])
by = {p.get('player'): p for p in list(MA.players) + _back}   # `back` rows are not in MA.players
Y = 2026
rows = []
for nm in NAMES:
    p = by.get(nm)
    if p is None:
        rows.append({'name': nm, 'MISSING': True}); continue
    with contextlib.redirect_stdout(io.StringIO()):
        e_raw = float(_prod_path(p, Y))
        cpv0 = float(_ruc_ceiling(p, Y))
        v0u = float(_v0_uncapped(p))
        cpv = cpv0 * (1.0 + _c_w(p, Y, e_raw, float(entry_anchor(p))) * (C_H - 1.0))
        binds = bool(cpv < e_raw <= v0u)
        e_full = cpv if binds else e_raw
        fe = float(_fEy(Y, p))
        tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
        R = float(_R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau))
        gy = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
        gp = min(gy / fe, 6.0)
        anch = R * float(entry_anchor(p))
        lam0 = float(np.interp(gp, [0, 1, 2, 3, 4, 5, 6], LAM_SIT))
        sur = float(_surprise(e_full, anch, gp))
        lam = lam0 ** (1.0 + sur)
        blend = (1.0 - lam) * anch + lam * e_full
        hc = float(_h_cut(p, Y))
        so = float(sitout_ev(p, Y, e_full))
        e26 = float(ev(p, Y))
    rows.append({'name': nm, 'ns_pro': int(nseas_pro(p, Y)), 'pool': bool(MA.is_pool(p)),
                 'RUC_PRIOR_CAP': RUC_PRIOR_CAP,
                 'prod_path': e_raw, 'ruc_ceiling': cpv0, 'ruc_ceiling_cw': cpv, 'v0_uncapped': v0u,
                 'ceiling_binds_in_ev': binds, 'e_full': e_full,
                 'v0_start': float(v0_start(p)), 'entry_anchor': float(entry_anchor(p)),
                 'R': R, 'anch': anch, 'gp': gp, 'lam0': lam0, 'surprise': sur, 'lam': lam,
                 'blend': blend, 'sitout_ev': so, 'h_cut': hc, 'ev26': e26,
                 'v': int(round(e26 / F_NUM))})

json.dump({'cap': RUC_PRIOR_CAP, 'rows': rows}, open(OUT, 'w'), indent=1)
for r in rows:
    if r.get('MISSING'):
        print('  MISSING', r['name']); continue
    print("  %-18s cap=%-5s e_raw=%8.2f ceil=%9.2f binds=%-5s e_full=%8.2f | anch=%8.2f lam0=%.4f "
          "sur=%.4f lam=%.6f | blend=%8.3f h=%.4f ev=%8.3f v=%d"
          % (r['name'], r['RUC_PRIOR_CAP'], r['prod_path'], r['ruc_ceiling_cw'], r['ceiling_binds_in_ev'],
             r['e_full'], r['anch'], r['lam0'], r['surprise'], r['lam'], r['blend'], r['h_cut'],
             r['ev26'], r['v']))
