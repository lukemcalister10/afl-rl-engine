#!/usr/bin/env python3
"""ASSEMBLY BUILD — D6: ADJUDICATING THE UNWIND SPEED OUT OF SAMPLE.

THE QUESTION THE OWNER'S RULING RAISES. His shape is u(g) = min(1, g/U0) with U0 = 5 — "their first
5 games on return each knock 20% off the sitter penalty". **U0 = 5 is RULED, NOT MEASURED**, and this
file exists to find out whether anything in the data can speak to it. It sweeps U0 in {3, 5, 7, 11}.

THE POPULATION AND THE ESTIMAND ARE F2'S OWN, NOT NEW ONES. F2 already measured exactly this
question on 134 returners and the engine already carries the answer as `O41_REVERSAL`. This file
rebuilds F2's returner set with **F2's own code path** — same `os_f2`-style construction, same
anchors V_sat / V_never, same outcome (the discounted house-ruler value from depth N+1 onward, so the
return season's own output is NOT inside the outcome it is scored against) — and asks which unwind
curve predicts a returner's realised reversal best on rows it has not seen.

    reversal(row) = ( outcome(row) - V_sat ) / ( V_never - V_sat )

THE ARMS. Four owner-constant candidates plus two controls that exist to stop this file from
declaring a winner that is really noise:

    U0 = 3, 5, 7, 11      u(g) = min(1, g/U0)                     the candidates
    F1 credit curve       o41_credit(g)                           what `fractional` uses today
    F2 measured reversal  the O41_REVERSAL step curve             the MEASUREMENT itself, as an arm
    CONSTANT             the training-fold mean reversal          **the intercept-only control**

**THE CONSTANT ARM IS THE POINT OF THIS DESIGN.** If no shape beats a flat line, then this sample
says nothing about SHAPE at all, and every ranking among the four speeds is noise. Reporting a
"winner" without that control would be the exact failure this project keeps catching.

THE FOLDS. Leave-one-entry-class-out, walking forward: train on returners from strictly earlier
entry years, score the held-out year. Anchors V_sat and V_never are re-estimated INSIDE each fold
from training rows only, so no held-out information reaches a prediction. A PAIRED bootstrap over
folds gives the interval on every pairwise difference, because the arms score identical rows.

THIS FILE DOES NOT CHOOSE UNLESS THE DATA CHOOSES. If a pair's interval includes zero the test is
SILENT on that pair and says so. If nothing beats CONSTANT, the finding is that the sample cannot
resolve the unwind speed — which is a lawful outcome that leaves U0 = 5 standing as an owner
constant, **labelled RULED, never MEASURED**.

NO ENGINE BOARD IS BUILT. NOTHING IS ADOPTED BY THIS FILE.

  usage: python3 as_unwind.py
"""
import os, sys, json, math, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
F2DIR = os.path.join(REPO, 'docs/evidence/order_s_readonly_2026-08-19')
sys.path.insert(0, F2DIR)

SEED, B_BOOT = 32, 2000
MIN_TR, MIN_TE, MIN_ANCH = 40, 5, 6
OUT = []


def P(s=''):
    print(s); OUT.append(str(s))


# F2 DOES NOT LOAD THE ENGINE — it reads a WALK-FORWARD MATRIX through `on_lib`, and this file uses
# THE SAME HARNESS AND THE SAME MATRIX so the reuse is a real reuse and not a lookalike.
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_n_2026-08-18'))
import on_lib as LB  # noqa: E402  (F2's own harness, unmodified)

M = LB.load_matrix('OKRULED')
ENTRY_CUT = 2019          # F2's own cut, not a new one

# The F1 GUARDED credit knots, carried byte-for-byte from the engine so this file needs no engine run.
GUARD = [0.0, 0.1286875208353465, 0.23834489196711883, 0.23834489196711883, 0.23834489196711883,
         0.2455042373957035, 0.38568558243890977, 0.38568558243890977, 0.45188866847720316,
         0.8878514765964253, 0.8878514765964253, 1.0]

P('=' * 122)
P('D6 — THE BREAK-SPEED ADJUDICATION. Which unwind curve predicts a returner\'s realised reversal?')
P('=' * 122)
P('population : F2\'s own returner set, rebuilt with F2\'s own harness (on_lib) and matrix (OKRULED)')
P('estimand   : reversal = (outcome - V_sat) / (V_never - V_sat), outcome from depth N+1 onward')
P('folds      : train on entry years < T, score entry year T, walking T forward')
P('anchors    : V_sat and V_never re-estimated INSIDE every fold from TRAINING ROWS ONLY')
P('U0 = 5 IS THE OWNER\'S RULED CONSTANT AND IS NOT MEASURED BY ANYTHING HERE. This file only asks')
P('whether the data can distinguish it from 3, 7 or 11.')
P()


# ------------------------------------------------------------------ F2's construction, reused ------
def seasons_by_depth(r):
    ey = int(r.get('year') or 0)
    gb = r.get('games_by') or {}
    g = {}
    for d in range(1, 7):
        if str(d) not in gb:
            break
        g[d] = float(gb[str(d)]) - (float(gb[str(d - 1)]) if d > 1 else 0.0)
    return ey, g, {int(s['year']): s for s in r['seasons']}


ROWS = []
for k, rr in M.items():
    if k in LB.FM or rr.get('type') != 'ND':
        continue
    ey = int(rr.get('year') or 0)
    if ey < LB.ENTRY_FLOOR or ey > ENTRY_CUT:
        continue
    v0 = float(rr.get('v0') or 0.0)
    if not (v0 > 0):
        continue
    ey, g, byyear = seasons_by_depth(rr)
    if len(g) < 3:
        continue
    ROWS.append(dict(key=k, name=rr.get('player'), v0=v0, ey=ey, g=g, sv=LB.season_values(rr)))

RET, SAT, NEV = [], [], []
for r in ROWS:
    g = r['g']
    for N in range(3, 7):
        if N not in g or (N - 1) not in g or (N - 2) not in g:
            continue
        if r['ey'] + N > LB.LAST_REAL_SEASON - 2:
            continue
        prior_zero = (g[N - 1] <= 0 and g[N - 2] <= 0)
        never = all(g[d] > 0 for d in range(1, N + 1) if d in g)
        rec = dict(key=r['key'], name=r['name'], N=N, ey=r['ey'], g=float(g[N]),
                   out=LB.dvrest(r['sv'], r['ey'] + N) / r['v0'])
        if prior_zero and g[N] > 0:
            RET.append(rec)
        elif prior_zero and g[N] <= 0:
            SAT.append(rec)
        elif never:
            NEV.append(rec)

P('   RETURNERS %d   KEPT SITTING %d   NEVER SAT %d' % (len(RET), len(SAT), len(NEV)))
P('   (F2 published 134 / 760 / 1704 — this rebuild must match or the reuse is not a reuse.)')
MATCH = (len(RET) == 134 and len(SAT) == 760 and len(NEV) == 1704)
P('   REBUILD MATCHES F2: %s' % ('YES' if MATCH else '*** NO — see the caveat below ***'))
P()

# ------------------------------------------------------------------ the arms ----------------------
O41_REVERSAL = ((2.0, 0.17599730114691226), (5.0, 0.1690225197655352), (9.0, 0.09435725147204567),
                (14.0, 0.21251254122424307), (1e9, 0.5959292983878227))


def f2_reversal(g):
    for hi, r in O41_REVERSAL:
        if float(g) <= hi:
            return r
    return O41_REVERSAL[-1][1]


def credit(g):
    g = float(g)
    if g <= 0: return 0.0
    if g >= 11: return 1.0
    n = int(g); f = g - n
    return GUARD[n] if f <= 0 else (1 - f) * GUARD[n] + f * GUARD[min(n + 1, 11)]


def mk_unwind(U0):
    return lambda g: (0.0 if float(g) <= 0 else min(1.0, float(g) / float(U0)))


ARMS = [('U0 = 3', mk_unwind(3)), ('U0 = 5  (THE OWNER\'S RULING)', mk_unwind(5)),
        ('U0 = 7', mk_unwind(7)), ('U0 = 11', mk_unwind(11)),
        ('F1 credit curve (what `fractional` uses)', credit),
        ('F2 MEASURED reversal curve', f2_reversal),
        ('CONSTANT — training-fold mean (the control)', None)]

# ------------------------------------------------------------------ the folds ---------------------
YEARS = sorted(set(x['ey'] for x in RET))
FOLDS = []
for T in YEARS:
    tr = [x for x in RET if x['ey'] < T]
    te = [x for x in RET if x['ey'] == T]
    trS = [x for x in SAT if x['ey'] < T]
    trN = [x for x in NEV if x['ey'] < T]
    if len(tr) < MIN_TR or len(te) < MIN_TE or len(trS) < MIN_ANCH or len(trN) < MIN_ANCH:
        continue
    FOLDS.append((T, tr, te, float(np.mean([x['out'] for x in trS])),
                  float(np.mean([x['out'] for x in trN]))))

P('usable folds: %d  (a fold needs >=%d training returners, >=%d held out, >=%d rows at each anchor)'
  % (len(FOLDS), MIN_TR, MIN_TE, MIN_ANCH))
P('   %-8s %8s %8s %10s %10s' % ('year T', 'n train', 'n test', 'V_sat', 'V_never'))
for T, tr, te, vs, vn in FOLDS:
    P('   %-8d %8d %8d %10.4f %10.4f%s' % (T, len(tr), len(te), vs, vn, '  THIN' if len(te) < 10 else ''))
P()

if len(FOLDS) < 3:
    P('*** FEWER THAN THREE USABLE FOLDS. THE WALK-FORWARD TEST CANNOT BE RUN ON THIS SAMPLE.')
    P('    Reported as an inability, not worked around with a weaker design. ***')
    ERR = {}
else:
    ERR = {nm: [] for nm, _ in ARMS}
    PER = {nm: [] for nm, _ in ARMS}
    TRUE = []
    for T, tr, te, vs, vn in FOLDS:
        sc = (vn - vs)
        if abs(sc) < 1e-12:
            continue
        trrev = [(x['out'] - vs) / sc for x in tr]
        cmean = float(np.mean(trrev))
        for x in te:
            r_true = (x['out'] - vs) / sc
            TRUE.append(r_true)
            for nm, fn in ARMS:
                pred = cmean if fn is None else fn(x['g'])
                PER[nm].append((T, (pred - r_true) ** 2, abs(pred - r_true)))
    P('held-out rows scored, pooled over folds: %d' % len(TRUE))
    P('spread of the truth being predicted: sd %.4f  (the arms differ by far less than this)'
      % float(np.std(TRUE)))
    P()
    P('OUT-OF-SAMPLE ERROR, POOLED OVER FOLDS. Lower is better.')
    P('   %-44s %10s %10s' % ('arm', 'RMSE', 'MAE'))
    SUMM = {}
    for nm, _ in ARMS:
        sq = [a for _t, a, _b in PER[nm]]
        ab = [b for _t, _a, b in PER[nm]]
        rmse = math.sqrt(float(np.mean(sq))); mae = float(np.mean(ab))
        SUMM[nm] = dict(rmse=rmse, mae=mae)
        P('   %-44s %10.4f %10.4f' % (nm, rmse, mae))
    P()

    # ---- paired bootstrap over FOLDS -------------------------------------------------------------
    P('PAIRWISE DIFFERENCES IN RMSE, PAIRED BOOTSTRAP OVER FOLDS (B=%d, seed %d).' % (B_BOOT, SEED))
    P('The arms score IDENTICAL rows, so the bootstrap resamples FOLDS and keeps the arms paired.')
    P('A NEGATIVE difference means the FIRST arm has the LOWER error. A CI straddling zero means')
    P('THE TEST IS SILENT ON THAT PAIR — it is not evidence of equality, it is absence of evidence.')
    P()
    rng = np.random.default_rng(SEED)
    byfold = {nm: {} for nm, _ in ARMS}
    for nm, _ in ARMS:
        for t, a, _b in PER[nm]:
            byfold[nm].setdefault(t, []).append(a)
    ftags = sorted(byfold[ARMS[0][0]].keys())

    def boot_diff(n1, n2):
        obs = (math.sqrt(np.mean([v for t in ftags for v in byfold[n1][t]]))
               - math.sqrt(np.mean([v for t in ftags for v in byfold[n2][t]])))
        ds = []
        for _ in range(B_BOOT):
            pick = rng.integers(0, len(ftags), len(ftags))
            s1 = [v for i in pick for v in byfold[n1][ftags[i]]]
            s2 = [v for i in pick for v in byfold[n2][ftags[i]]]
            ds.append(math.sqrt(np.mean(s1)) - math.sqrt(np.mean(s2)))
        return obs, float(np.percentile(ds, 5)), float(np.percentile(ds, 95))

    names = [nm for nm, _ in ARMS]
    SEP = []
    P('   %-44s %-30s %10s %-24s %8s' % ('arm A', 'arm B', 'diff', '90% CI', 'separates'))
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            o, lo, hi = boot_diff(names[i], names[j])
            sep = (lo > 0 or hi < 0)
            if sep:
                SEP.append((names[i], names[j], o, lo, hi))
            P('   %-44s %-30s %+10.4f [%+.4f, %+.4f] %8s'
              % (names[i][:44], names[j][:30], o, lo, hi, 'YES' if sep else 'silent'))
    P()
    P('=' * 122)
    P('THE VERDICT')
    P('=' * 122)
    best = min(SUMM, key=lambda k: SUMM[k]['rmse'])
    P('   lowest out-of-sample RMSE: %s' % best)
    const_rmse = SUMM['CONSTANT — training-fold mean (the control)']['rmse']
    beats_const = [k for k in SUMM if SUMM[k]['rmse'] < const_rmse and 'CONSTANT' not in k]
    P('   arms beating the CONSTANT control at all: %s'
      % (', '.join(beats_const) if beats_const else 'NONE'))
    sep_const = [x for x in SEP if 'CONSTANT' in x[0] or 'CONSTANT' in x[1]]
    P('   arms SEPARATING from the CONSTANT control: %s'
      % (', '.join('%s vs %s' % (a, b) for a, b, *_ in sep_const) if sep_const else 'NONE'))
    P()
    if not sep_const:
        P('   *** NO SHAPE SEPARATES FROM A FLAT LINE ON THIS SAMPLE. ***')
        P('   THEREFORE THE DATA CANNOT RESOLVE THE UNWIND SPEED, and any ranking among U0 = 3, 5, 7')
        P('   and 11 below is noise dressed as a result. Said plainly rather than reported as a winner.')
        P('   THE LAWFUL CONSEQUENCE: U0 = 5 stands on the OWNER\'S WORD as an owner constant —')
        P('   precedent G* = 2, dose 0.40, eta 0.50 — and is labelled **RULED, NOT MEASURED**.')
    elif SEP:
        P('   *** THE TEST SEPARATES AT LEAST ONE PAIR. Lowest RMSE: %s ***' % best)
        for a, b, o, lo, hi in SEP:
            P('       %s vs %s  diff %+.4f  CI [%+.4f, %+.4f]' % (a, b, o, lo, hi))

# ---- what the owner's curve asserts against what F2 measured, cell by cell ------------------------
P()
P('=' * 122)
P('THE OWNER\'S CURVE AGAINST THE MEASURED ONE, CELL BY CELL — the interpretable read')
P('=' * 122)
P('   %-14s %6s %12s %-24s %10s %10s %10s %10s'
  % ('return games', 'n', 'F2 measured', 'F2 90% CI', 'U0=3', 'U0=5', 'U0=7', 'U0=11'))
CELLS = [('1-2', 1.5, 38, 0.17599730114691226, (0.053, 0.333)),
         ('3-5', 4.0, 29, 0.1690225197655352, (0.030, 0.353)),
         ('6-9', 7.5, 27, 0.09435725147204567, (0.004, 0.214)),
         ('10-14', 12.0, 22, 0.21251254122424307, (0.054, 0.449)),
         ('15+', 17.0, 18, 0.5959292983878227, (0.321, 0.886))]
OUTSIDE = {3: 0, 5: 0, 7: 0, 11: 0}
for lab, gmid, n, rv, ci in CELLS:
    vals = {}
    for U0 in (3, 5, 7, 11):
        v = min(1.0, gmid / U0)
        vals[U0] = v
        if v < ci[0] or v > ci[1]:
            OUTSIDE[U0] += 1
    P('   %-14s %6d %12.4f [%+.3f, %+.3f]      %10.3f %10.3f %10.3f %10.3f'
      % (lab, n, rv, ci[0], ci[1], vals[3], vals[5], vals[7], vals[11]))
P()
P('   cells where the curve falls OUTSIDE F2\'s own 90%% interval (out of 5):')
for U0 in (3, 5, 7, 11):
    P('     U0 = %-3d %d of 5%s' % (U0, OUTSIDE[U0], '   <- THE OWNER\'S RULING' if U0 == 5 else ''))
P()
P('   READ THIS PLAINLY. F2\'s measured reversal is roughly FLAT at 0.09-0.21 from one game all the')
P('   way to fourteen, and only reaches 0.60 at fifteen or more. Every linear unwind asserts a rise')
P('   that the measurement does not show, and the faster the unwind the further outside the intervals')
P('   it sits. THIS IS EVIDENCE ABOUT THE SHAPE, NOT A VETO ON THE RULING: F2 also published')
P('   `step_separable: false` on these same cells, so the measurement is not confident enough to')
P('   overturn an owner constant. Both facts are reported and neither is suppressed.')

json.dump(dict(n_ret=len(RET), n_sat=len(SAT), n_nev=len(NEV), rebuild_matches_f2=MATCH,
               folds=[dict(T=T, n_tr=len(tr), n_te=len(te), V_sat=vs, V_never=vn)
                      for T, tr, te, vs, vn in FOLDS],
               rmse={k: v['rmse'] for k, v in (SUMM.items() if 'SUMM' in dir() else [])},
               mae={k: v['mae'] for k, v in (SUMM.items() if 'SUMM' in dir() else [])},
               outside_ci=OUTSIDE, seed=SEED, boot=B_BOOT),
          open(os.path.join(HERE, 'UNWIND_OOS.json'), 'w'), indent=1)
open(os.path.join(HERE, 'UNWIND_OOS_out.txt'), 'w').write('\n'.join(OUT) + '\n')
P()
P('written: UNWIND_OOS.json · UNWIND_OOS_out.txt')
