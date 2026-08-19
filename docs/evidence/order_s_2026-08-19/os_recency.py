#!/usr/bin/env python3
"""ORDER S — S1. DOES A SEASON'S PREDICTIVE VALUE FOR NEXT-SEASON PRODUCTION DECAY WITH ITS AGE?

READ-ONLY. No engine import, no board build, no store write. PREREG_S.md section 1 fixes every rule
in this file and was pushed before the first engine edit.

THE OBJECT UNDER TEST is o37_surplus's weighting. The engine weights a played season by GAMES ONLY:

    s_P = SUM_k games_{Y-k} * d_{Y-k}  /  SUM_k games_{Y-k}          (the ENGINE, w = 1)

The one-parameter family this order measures is

    L_w = SUM_k games_{Y-k} * w^k * d_{Y-k}  /  SUM_k games_{Y-k} * w^k

with d = season avg - o32_gate_bar(pos, age), the SAME bar object the charge reads, reproduced by
on_lib.bar and asserted against the engine source literal inside on_lib itself (falsifier N2).

ESTIMATION IS WALK-FORWARD AND NEVER IN-SAMPLE: for target season T, w is chosen on states whose
target year is strictly < T and scored only on states whose target year is exactly T.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_recency.py
"""
import json, math, os, sys, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_n_2026-08-18'))
import on_lib as LB                                                          # noqa: E402

SEED = 32
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
WGRID = [round(x, 3) for x in np.arange(0.05, 1.0001, 0.05)]
WFINE = [round(x, 3) for x in np.arange(0.20, 1.0001, 0.01)]
FIRST_TARGET = 2010          # first target year scored walk-forward (earlier years are the seed train set)
L = []


def P(s=''):
    print(s); L.append(str(s))


# =====================================================================================================
# 1 · THE PANEL
# =====================================================================================================
D = json.load(open(STORE))
SERIES = {}
META = {}
for p in D:
    k = p.get('key')
    by = p.get('_by')
    if not k or not by:
        continue
    rows = []
    for x in sorted((p.get('scoring') or []), key=lambda z: z['year']):
        g = float(x.get('games') or 0.0)
        if g <= 0.0:
            continue
        pos = x.get('pos')
        if pos not in LB.BARS or x.get('avg') is None:
            continue
        a = int(x['year']) - int(by)
        b = LB.bar(pos, a)
        if b is None:
            continue
        rows.append(dict(year=int(x['year']), age=a, pos=pos, games=g, avg=float(x['avg']),
                         d=float(x['avg']) - b,
                         cls=('TALL' if pos in LB.TALLPOS else 'SMALL')))
    if rows:
        SERIES[k] = rows
        META[k] = dict(entry=int(p.get('year') or 0), typ=p.get('type'),
                       pick=(p.get('pick') if p.get('type') == 'ND' else None))

STATES = []
for k, rows in SERIES.items():
    byyear = {r['year']: r for r in rows}
    for r in rows:
        T = r['year']                                   # the TARGET season
        if T > LB.LAST_REAL_SEASON:                     # 2026 in-progress is NEVER a target
            continue
        hist = [q for q in rows if q['year'] < T]
        if not hist:
            continue
        STATES.append(dict(key=k, T=T, Y=T - 1, y=r['d'], tg=r['games'], tage=r['age'],
                           tcls=r['cls'], nh=len(hist),
                           hist=[(T - q['year'], q['games'], q['d']) for q in hist],
                           span=T - min(q['year'] for q in hist),
                           entry=META[k]['entry'], pick=META[k]['pick'], typ=META[k]['typ']))

P('=' * 118)
P('ORDER S — S1. THE RECENCY MEASUREMENT. READ-ONLY; NO BOARD IS BUILT.')
P('=' * 118)
P('store   : %s' % LB.SP)
P('bar     : on_lib.bar == the engine o32_gate_bar (asserted against the engine literal, falsifier N2)')
P('ruler   : %s' % LB.check_s4_copy())
P('panel   : %d states / %d players / target years %d..%d' %
  (len(STATES), len(set(s['key'] for s in STATES)),
   min(s['T'] for s in STATES), max(s['T'] for s in STATES)))
P('predictand d = season avg - o32_gate_bar(pos, age), AFL Fantasy points per game — the SAME units')
P('           and the SAME bar the surplus is built on.')
P('NOTE      : years-back k is measured from the TARGET season T, so k=1 is the season immediately')
P('           before the target. The engine reads seasons up to Y = T-1, so k >= 1 always.')
P()


# =====================================================================================================
# 2 · THE PREDICTOR
# =====================================================================================================
def Lw(hist, w):
    num = den = 0.0
    for k, g, d in hist:
        wt = g * (w ** (k - 1))                        # k-1 so the newest available season has weight g
        num += wt * d; den += wt
    return num / den if den > 0 else None


def cols(states, w):
    return np.array([Lw(s['hist'], w) for s in states], float)


Y = np.array([s['y'] for s in STATES], float)
TG = np.array([s['tg'] for s in STATES], float)
TT = np.array([s['T'] for s in STATES], int)


def ols_fit(x, y, sw):
    X = np.column_stack([np.ones_like(x), x])
    W = sw
    A = X.T @ (X * W[:, None]); b = X.T @ (y * W)
    return np.linalg.solve(A, b)


def sse(pred, y, sw):
    r = y - pred
    return float((sw * r * r).sum()), float(sw.sum())


# =====================================================================================================
# 3 · WALK-FORWARD, NEVER IN-SAMPLE
# =====================================================================================================
P('-' * 118)
P('3 · WALK-FORWARD OUT-OF-SAMPLE FIT. w IS CHOSEN ON TARGET YEARS < T AND SCORED ONLY AT T.')
P('-' * 118)
P('   Two scorings are reported and neither is dropped:')
P('     CALIBRATED — OLS of d_{T} on [1, L_w] fitted on the training years, applied at T. This is the')
P('                  W4-style benchmark: it absorbs mean reversion so the question left is the')
P('                  WEIGHTING alone.')
P('     DIRECT     — prediction = L_w itself, no intercept, no slope. This is what the engine')
P('                  actually does with the object: it uses the weighted mean AS a level.')
P('   Errors are weighted by the TARGET season games, because that is how the surplus weights.')
P()

years = sorted(set(TT))
tgt_years = [t for t in years if t >= FIRST_TARGET]


def walk(grid, weighted=True, states=STATES, tag=''):
    y = np.array([s['y'] for s in states], float)
    tt = np.array([s['T'] for s in states], int)
    sw = np.array([s['tg'] for s in states], float) if weighted else np.ones(len(states))
    C = {w: cols(states, w) for w in grid}
    out = []
    tot_cal = tot_dir = tot_n = 0.0
    tot_eng_cal = tot_eng_dir = 0.0
    for T in tgt_years:
        tr = tt < T; te = tt == T
        if tr.sum() < 200 or te.sum() < 20:
            continue
        best_w = None; best_s = None
        best_wd = None; best_sd = None
        for w in grid:
            x = C[w]
            b = ols_fit(x[tr], y[tr], sw[tr])
            s, _ = sse(b[0] + b[1] * x[tr], y[tr], sw[tr])
            if best_s is None or s < best_s:
                best_s = s; best_w = w
            sd, _ = sse(x[tr], y[tr], sw[tr])
            if best_sd is None or sd < best_sd:
                best_sd = sd; best_wd = w
        xb = C[best_w]; bb = ols_fit(xb[tr], y[tr], sw[tr])
        e_cal, n = sse(bb[0] + bb[1] * xb[te], y[te], sw[te])
        e_dir, _ = sse(C[best_wd][te], y[te], sw[te])
        x1 = C[1.0] if 1.0 in C else cols(states, 1.0)
        b1 = ols_fit(x1[tr], y[tr], sw[tr])
        e1_cal, _ = sse(b1[0] + b1[1] * x1[te], y[te], sw[te])
        e1_dir, _ = sse(x1[te], y[te], sw[te])
        out.append(dict(T=int(T), n_tr=int(tr.sum()), n_te=int(te.sum()),
                        w_cal=best_w, w_dir=best_wd,
                        rms_cal=math.sqrt(e_cal / n), rms_eng_cal=math.sqrt(e1_cal / n),
                        rms_dir=math.sqrt(e_dir / n), rms_eng_dir=math.sqrt(e1_dir / n)))
        tot_cal += e_cal; tot_dir += e_dir; tot_n += n
        tot_eng_cal += e1_cal; tot_eng_dir += e1_dir
    agg = dict(rms_cal=math.sqrt(tot_cal / tot_n), rms_eng_cal=math.sqrt(tot_eng_cal / tot_n),
               rms_dir=math.sqrt(tot_dir / tot_n), rms_eng_dir=math.sqrt(tot_eng_dir / tot_n),
               n=tot_n)
    return out, agg


WF, AGG = walk(WFINE, weighted=True)
P('   %-6s %7s %7s | %7s %9s %9s %8s | %7s %9s %9s %8s' %
  ('T', 'n_tr', 'n_te', 'w*_cal', 'RMS_cal', 'RMS_w=1', 'gain%', 'w*_dir', 'RMS_dir', 'RMS_w=1', 'gain%'))
for r in WF:
    P('   %-6d %7d %7d | %7.2f %9.4f %9.4f %+8.3f | %7.2f %9.4f %9.4f %+8.3f' %
      (r['T'], r['n_tr'], r['n_te'], r['w_cal'], r['rms_cal'], r['rms_eng_cal'],
       100.0 * (r['rms_eng_cal'] - r['rms_cal']) / r['rms_eng_cal'],
       r['w_dir'], r['rms_dir'], r['rms_eng_dir'],
       100.0 * (r['rms_eng_dir'] - r['rms_dir']) / r['rms_eng_dir']))
wc = [r['w_cal'] for r in WF]; wd = [r['w_dir'] for r in WF]
P()
P('   POOLED OUT-OF-SAMPLE, all scored years together:')
P('     CALIBRATED : RMS %.4f at the walk-forward w, against %.4f at the engine w=1 -> %+.3f%%'
  % (AGG['rms_cal'], AGG['rms_eng_cal'], 100.0 * (AGG['rms_eng_cal'] - AGG['rms_cal']) / AGG['rms_eng_cal']))
P('     DIRECT     : RMS %.4f at the walk-forward w, against %.4f at the engine w=1 -> %+.3f%%'
  % (AGG['rms_dir'], AGG['rms_eng_dir'], 100.0 * (AGG['rms_eng_dir'] - AGG['rms_dir']) / AGG['rms_eng_dir']))
P('     w* path CALIBRATED: min %.2f  median %.2f  max %.2f  SPREAD %.2f  (S1-P2 bar: <= 0.30)'
  % (min(wc), float(np.median(wc)), max(wc), max(wc) - min(wc)))
P('     w* path DIRECT    : min %.2f  median %.2f  max %.2f  SPREAD %.2f'
  % (min(wd), float(np.median(wd)), max(wd), max(wd) - min(wd)))
P()


# =====================================================================================================
# 4 · THE POOLED OOS CURVE ACROSS THE WHOLE w GRID
# =====================================================================================================
P('-' * 118)
P('4 · THE POOLED OUT-OF-SAMPLE ERROR CURVE. EVERY w SCORED THE SAME WALK-FORWARD WAY.')
P('-' * 118)
P('   For each w on the grid: for every target year T, the OLS calibration is fitted on years < T and')
P('   scored at T, then summed. NO year ever scores on its own data. The engine is w = 1.00.')
P()
C_ALL = {w: cols(STATES, w) for w in WFINE}
curve = {}
for w in WFINE:
    x = C_ALL[w]; e_cal = e_dir = n_tot = 0.0
    for T in tgt_years:
        tr = TT < T; te = TT == T
        if tr.sum() < 200 or te.sum() < 20:
            continue
        b = ols_fit(x[tr], Y[tr], TG[tr])
        a, nn = sse(b[0] + b[1] * x[te], Y[te], TG[te])
        c, _ = sse(x[te], Y[te], TG[te])
        e_cal += a; e_dir += c; n_tot += nn
    curve[w] = (math.sqrt(e_cal / n_tot), math.sqrt(e_dir / n_tot))
w_cal_star = min(curve, key=lambda w: curve[w][0])
w_dir_star = min(curve, key=lambda w: curve[w][1])
P('   %-8s %12s %12s' % ('w', 'OOS RMS cal', 'OOS RMS dir'))
for w in WGRID:
    ww = min(WFINE, key=lambda z: abs(z - w))
    mk = ''
    if abs(ww - w_cal_star) < 1e-9: mk += '  <== OOS-OPTIMAL (calibrated)'
    if abs(ww - w_dir_star) < 1e-9: mk += '  <== OOS-OPTIMAL (direct)'
    if abs(ww - 1.0) < 1e-9: mk += '  <== THE ENGINE'
    P('   %-8.2f %12.5f %12.5f%s' % (ww, curve[ww][0], curve[ww][1], mk))
P()
P('   OOS-OPTIMAL w, CALIBRATED : %.2f' % w_cal_star)
P('   OOS-OPTIMAL w, DIRECT     : %.2f' % w_dir_star)
P()

# in-sample, for the S1-F3 comparison only
ins_cal = {}
for w in WFINE:
    x = C_ALL[w]
    b = ols_fit(x, Y, TG)
    ins_cal[w], _ = sse(b[0] + b[1] * x, Y, TG)
w_in = min(ins_cal, key=lambda w: ins_cal[w])
P('   IN-SAMPLE optimal w (printed ONLY so it can be told apart from the walk-forward number): %.2f'
  % w_in)
P('   S1-F3 gap |OOS - in-sample| = %.2f  (falsifier bar: > 0.20 means the fit is unstable)'
  % abs(w_cal_star - w_in))
P()


# =====================================================================================================
# 5 · WHAT THAT w MEANS AS SEASON WEIGHTS
# =====================================================================================================
P('-' * 118)
P('5 · THE IMPLIED SEASON WEIGHTS, AT EQUAL GAMES, AGAINST THE PRIOR ART')
P('-' * 118)
def norm3(w):
    v = np.array([1.0, w, w * w]); return v / v.sum()
for tag, w in (('THIS ORDER, walk-forward (calibrated)', w_cal_star),
               ('THIS ORDER, walk-forward (direct)', w_dir_star),
               ('W4 (prior art, NOT used)', 0.475),
               ('THE ENGINE, o37_surplus', 1.0)):
    n3 = norm3(w)
    P('   %-40s w=%.3f -> [%.3f, %.3f, %.3f]' % (tag, w, n3[0], n3[1], n3[2]))
P()
P('   W4 measured 0.45-0.50 on a DIFFERENT predictand (its own level column on board points) and is')
P('   quoted for comparison only. The weights this order prices come from the fit above.')
P()


# =====================================================================================================
# 6 · SPLITS
# =====================================================================================================
P('-' * 118)
P('6 · DOES THE DECAY DIFFER BY HISTORY DEPTH, AGE OR CLASS? (each split re-fitted walk-forward)')
P('-' * 118)
SPL = {}


def split_w(states, label):
    if len(states) < 400:
        SPL[label] = None
        P('   %-28s n=%-6d  TOO THIN — not fitted' % (label, len(states)))
        return
    yy = np.array([s['y'] for s in states], float)
    tt = np.array([s['T'] for s in states], int)
    ss = np.array([s['tg'] for s in states], float)
    cc = {w: cols(states, w) for w in WFINE}
    best = None
    for w in WFINE:
        x = cc[w]; e = n = 0.0
        for T in tgt_years:
            tr = tt < T; te = tt == T
            if tr.sum() < 150 or te.sum() < 10:
                continue
            b = ols_fit(x[tr], yy[tr], ss[tr])
            a, nn = sse(b[0] + b[1] * x[te], yy[te], ss[te])
            e += a; n += nn
        if n <= 0:
            continue
        r = math.sqrt(e / n)
        if best is None or r < best[1]:
            best = (w, r, n)
    SPL[label] = dict(w=best[0], rms=best[1], n=len(states))
    n3 = norm3(best[0])
    P('   %-28s n=%-6d  w*=%.2f  OOS RMS %.4f   weights [%.3f, %.3f, %.3f]'
      % (label, len(states), best[0], best[1], n3[0], n3[1], n3[2]))


split_w([s for s in STATES if s['nh'] <= 2], 'history 1-2 seasons')
split_w([s for s in STATES if 3 <= s['nh'] <= 5], 'history 3-5 seasons')
split_w([s for s in STATES if s['nh'] >= 6], 'history 6+ seasons')
split_w([s for s in STATES if s['tage'] <= 21], 'target age <= 21')
split_w([s for s in STATES if 22 <= s['tage'] <= 25], 'target age 22-25')
split_w([s for s in STATES if s['tage'] >= 26], 'target age 26+')
split_w([s for s in STATES if s['tcls'] == 'TALL'], 'TALL')
split_w([s for s in STATES if s['tcls'] == 'SMALL'], 'SMALL')
split_w([s for s in STATES if s['entry'] >= LB.ENTRY_FLOOR], 'entrants 2005+ (board pop)')
split_w([s for s in STATES if s['typ'] == 'ND'], 'ND entrants')
P()

# unweighted scoring, as a robustness read
WF_U, AGG_U = walk(WFINE, weighted=False)
wu = [r['w_cal'] for r in WF_U]
P('   UNWEIGHTED scoring (every state counts once, not by target games):')
P('     w* path min %.2f median %.2f max %.2f ; pooled OOS RMS %.4f vs engine %.4f -> %+.3f%%'
  % (min(wu), float(np.median(wu)), max(wu), AGG_U['rms_cal'], AGG_U['rms_eng_cal'],
     100.0 * (AGG_U['rms_eng_cal'] - AGG_U['rms_cal']) / AGG_U['rms_eng_cal']))
P()


# =====================================================================================================
# 7 · THE VERDICT AGAINST THE PREREG
# =====================================================================================================
P('-' * 118)
P('7 · THE PREREG SCORED')
P('-' * 118)
p1 = 0.30 < w_cal_star < 0.85
p2 = (max(wc) - min(wc)) <= 0.30
f1 = w_cal_star >= 0.95
f3 = abs(w_cal_star - w_in) > 0.20
P('   S1-P1  OOS-optimal w strictly inside (0.30, 0.85)        : w* = %.2f  -> %s'
  % (w_cal_star, 'RIGHT' if p1 else 'WRONG'))
P('   S1-P2  per-year w* spread <= 0.30                        : spread %.2f -> %s'
  % (max(wc) - min(wc), 'RIGHT' if p2 else 'WRONG'))
P('   S1-F1  w* >= 0.95 would mean recency is UNSUPPORTED      : %s'
  % ('*** FIRED — DO NOT PRICE ***' if f1 else 'does not fire'))
P('   S1-F3  |OOS - in-sample| > 0.20 would mean UNSTABLE      : %s'
  % ('*** FIRED ***' if f3 else 'does not fire'))
P()

OUT = dict(meta=dict(n_states=len(STATES), n_players=len(set(s['key'] for s in STATES)),
                     first_target=FIRST_TARGET, wgrid=[WFINE[0], WFINE[-1]], seed=SEED),
           walk_forward=WF, aggregate=AGG, curve={str(k): v for k, v in curve.items()},
           w_cal_star=w_cal_star, w_dir_star=w_dir_star, w_insample=w_in,
           splits=SPL, unweighted=dict(agg=AGG_U, w=[r['w_cal'] for r in WF_U]),
           falsifiers=dict(S1_F1=bool(f1), S1_F3=bool(f3)),
           predictions=dict(S1_P1=bool(p1), S1_P2=bool(p2)))
json.dump(OUT, open(os.path.join(HERE, 'RECENCY_S.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'RECENCY_S_out.txt'), 'w').write('\n'.join(L) + '\n')
P('written: RECENCY_S.json · RECENCY_S_out.txt')
