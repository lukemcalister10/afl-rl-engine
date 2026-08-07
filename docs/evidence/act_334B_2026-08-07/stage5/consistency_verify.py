"""#334 stage B / STAGE 5 — DOES THE CONSISTENCY SOLVE ACTUALLY DO WHAT IT CLAIMS?

The claim: the frozen-lam solve does not price a cell at its measured future F once installed, and the
fixed-point solve does. That claim is checkable directly, and it is checked here BEFORE the surface is
installed, at every resolved node, in the engine's own price expression:

    installed aggregate at G   =  SUM_i w_i * P_i(G)          P_i as in teach_g5_consistency.py
    target                     =  SUM_i w_i * F_i

Printed per node: the target, the installed aggregate under the FROZEN-LAM factor, and the installed
aggregate under the SOLVED factor, each as a ratio to the target. A correct solve puts the second column
away from 1.000 and the third column ON 1.000.

READ-ONLY. This file proves the solver, not the landing.
"""
import os, sys, io, contextlib, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = json.load(open(HERE + '/s5_rows.json'))
WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, '/home/claude/rl_vendor'); os.chdir(WORKDIR); sys.path.insert(0, '.')
EG = {'__name__': '_s5_cv'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], EG)
_rho_res = EG['_rho_res']; _RHO_SIT_BAR = EG['_RHO_SIT_BAR']
SUR_W = EG['SUR_W']; LAM_SIT = EG['LAM_SIT']

OLD = json.load(open(HERE + '/g5_table.json'))
NEW = json.load(open(HERE + '/g5_table_LANDED.json'))
CLASSES = ['nonKPP', 'KPP', 'RUCK']
PK, GK, TK = NEW['pk_knots'], NEW['g_knots'], NEW['tau_knots']
H0 = dict(p=0.35, g=0.45, t=0.35); GROW = 1.15; EFFN_MIN = 35.0

T = [r for r in ROWS if r['tau'] > 1e-9]
for r in T:
    r['_lp'] = math.log(min(max(r['pk'], 1), 90))
    r['_lg'] = math.log1p(min(r['gcum'], 20.0))
    gp = r['gp']
    r['_lam0'] = float(np.interp(gp, [0, 1, 2, 3, 4, 5, 6], LAM_SIT))
    r['_u'] = 1.0 - _rho_res(gp) / _RHO_SIT_BAR
    a1 = r['R'] * r['A']
    s1 = abs(math.log(r['e_full'] / a1)) if (r['e_full'] > 0 and a1 > 0) else 0.0
    r['_xb'] = (math.log(r['lam']) / math.log(r['_lam0']) - SUR_W * s1 * r['_u']) \
        if (0.0 < r['_lam0'] < 1.0 and r['lam'] > 0) else None


def price(r, g):
    a = g * r['R'] * r['A']; l0 = r['_lam0']
    if l0 <= 0.0: return a
    if l0 >= 1.0: return r['e_full']
    s = abs(math.log(r['e_full'] / a)) if (r['e_full'] > 0 and a > 0) else 0.0
    lam = l0 ** (r['_xb'] + SUR_W * s * r['_u'])
    return (1.0 - lam) * a + lam * r['e_full']


BYCLS = {c: [r for r in T if r['cls'] == c] for c in CLASSES}
def node(rows, lp, lg, tk, h):
    w = []; sub = []
    for r in rows:
        a = (r['_lp'] - lp) / h['p']; b = (r['_lg'] - lg) / h['g']; c = (r['tau'] - tk) / h['t']
        ww = math.exp(-0.5 * (a * a + b * b + c * c))
        if ww < 1e-9: continue
        w.append(ww); sub.append(r)
    if not w: return None
    w = np.array(w)
    de = np.array([(1.0 - r['lam']) * r['R'] * r['A'] for r in sub])
    infl = w * np.maximum(de, 0.0)
    effn = ((infl.sum() ** 2) / (infl ** 2).sum()) if (infl ** 2).sum() > 0 else 0.0
    return w, sub, float(effn)


L = []
def P(s=''):
    print(s); L.append(s)


P('=' * 112)
P('#334 stage B / STAGE 5 — SOLVER VERIFICATION: does the fixed point price each cell at its own F?')
P('=' * 112)
P('  frozen-lam table : g5_table.json            (the first pass, filed with the STOP report)')
P('  solved table     : g5_table_LANDED.json     (this pass)')
P('')
P('  %-28s %8s %12s %14s %14s' % ('node (cls, pick, games, tau)', 'eff-n', 'target F', 'frozen-lam/F', 'SOLVED/F'))
P('  ' + '-' * 82)
rows_out = []
for cls in CLASSES:
    for pk in PK:
        for gk in GK:
            for tk in TK:
                lp = math.log(pk); lg = math.log1p(gk)
                side = (lambda r: r['gcum'] == 0) if gk == 0 else (lambda r: r['gcum'] >= 1)
                pop = [r for r in BYCLS[cls] if side(r)]
                h = dict(H0); nd = None
                for i in range(9):
                    nd = node(pop, lp, lg, tk, h)
                    if nd and nd[2] >= EFFN_MIN: break
                    if i < 8: h = {'p': h['p'] * GROW, 'g': h['g'] * GROW, 't': h['t']}
                pooled = not (nd and nd[2] >= EFFN_MIN)
                if pooled:
                    pop = [r for r in T if side(r)]
                    h = dict(H0)
                    for i in range(17):
                        nd = node(pop, lp, lg, tk, h)
                        if nd and nd[2] >= EFFN_MIN: break
                        if i < 16: h = {'p': h['p'] * GROW, 'g': h['g'] * GROW, 't': h['t']}
                if not nd: continue
                w, sub, effn = nd
                tgt = float(sum(wi * r['F'] for wi, r in zip(w, sub)))
                if tgt <= 0: continue
                go = OLD['table'][cls][str(pk)][str(gk)][TK.index(tk)]
                gn = NEW['table'][cls][str(pk)][str(gk)][TK.index(tk)]
                ao = float(sum(wi * price(r, go) for wi, r in zip(w, sub)))
                an = float(sum(wi * price(r, gn) for wi, r in zip(w, sub)))
                rows_out.append((cls, pk, gk, tk, effn, tgt, ao / tgt, an / tgt, go, gn, pooled))

# print a representative slice in full, then the summary over all nodes
for r in rows_out:
    if r[3] in (1, 2) and r[2] in (2, 5):
        P('  %-28s %8.1f %12.1f %14.4f %14.4f'
          % ('%s pk%-3d g%-3d tau%d' % (r[0], r[1], r[2], r[3]), r[4], r[5], r[6], r[7]))
fo = np.array([r[6] for r in rows_out]); fn = np.array([r[7] for r in rows_out])
P('')
P('  ACROSS ALL %d RESOLVED NODES — installed aggregate as a ratio to the cell\'s own target F:' % len(rows_out))
P('     frozen-lam pass : mean %.4f   median %.4f   max |dev from 1| %.4f' % (fo.mean(), np.median(fo), np.abs(fo - 1).max()))
P('     SOLVED pass     : mean %.4f   median %.4f   max |dev from 1| %.4f' % (fn.mean(), np.median(fn), np.abs(fn - 1).max()))
P('     nodes within 0.1%% of target: frozen-lam %d/%d   SOLVED %d/%d'
  % (int((np.abs(fo - 1) < 0.001).sum()), len(fo), int((np.abs(fn - 1) < 0.001).sum()), len(fn)))
P('')
P('  DIRECTION OF THE CORRECTION. The frozen-lam factor OVERSHOOTS its own cell target (ratio > 1) wherever')
P('  the lam feedback is amplifying — a quiet starter whose e_full sits BELOW his anchor sees s = |log(e/a)|')
P('  GROW when the anchor is lifted, so the evidence bar rises, lam falls, and MORE weight lands on the')
P('  now-higher anchor. The solve therefore returns a SMALLER G for the same price. %d of %d nodes move DOWN.'
  % (sum(1 for r in rows_out if r[9] < r[8] - 1e-9), len(rows_out)))
P('  Nodes where the frozen-lam factor UNDERSHOT (e_full above the anchor, damping feedback): %d.'
  % sum(1 for r in rows_out if r[9] > r[8] + 1e-9))
P('')
P('  WHAT THIS DOES NOT FIX, stated plainly: hitting every CELL target is not the same as hitting a')
P('  POPULATION target. The teaching cells are dominated by the pool routes (2,834 of 5,675 scanned rows);')
P('  the ND 1-64 year-1 slice the no-arb landing is read on is a minority inside those same cells. A cell')
P('  can price its own aggregate at F while the ND subset within it lands elsewhere. That is a BASIS')
P('  question, not a solver question, and this pass does not touch it.')
open(os.path.join(HERE, 'CONSISTENCY_VERIFY.txt'), 'w').write('\n'.join(L) + '\n')
