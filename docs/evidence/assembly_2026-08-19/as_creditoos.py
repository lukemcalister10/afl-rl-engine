#!/usr/bin/env python3
"""ASSEMBLY BUILD — ADJUDICATING THE I1 CREDIT RULE OUT OF SAMPLE.

THE QUESTION. F1 published two readings of the same measurement — the RAW per-games cells and the
GUARDED isotonic curve — and their intervals overlap heavily. The engine's incumbent is a third rule,
the wired step min(1, g/2). Which one the assembly wired was a SEAT CALL, never owner-ruled. This
file asks the only question that can settle it on evidence rather than taste: WHICH RULE PREDICTS
BEST ON DATA IT HAS NOT SEEN.

THE TEST. Walk-forward on F1's OWN population and F1's OWN estimand, by DRAFT CLASS:

  for each held-out class T:
      TRAIN on every entrant from a class strictly before T
        -> R0_hat  = mean outcome among training rows with g = 0
        -> R11_hat = mean outcome among training rows with g >= 11
      PREDICT on class T, for each row with g games:
        -> ratio_hat(g) = R0_hat + c(g) * (R11_hat - R0_hat)
      SCORE the held-out rows.

`c` is the credit rule under test and NOTHING ELSE CHANGES between arms — same rows, same folds,
same anchors, same estimand. The anchors R0/R11 are re-estimated inside every fold from training data
only, so no held-out information reaches the prediction.

The outcome is F1's own: the DISC-discounted house-ruler value delivered from depth 2 onward, over
the row's own entry price. The population is F1's own, built by its own `rows_at_depth(2)`.

  errors reported: RMSE and MAE on the held-out rows, pooled over folds, and the per-fold path.
  a PAIRED bootstrap over folds gives the interval on each pairwise difference, because the arms are
  scored on IDENTICAL rows and an unpaired interval would overstate the noise.

THIS FILE DOES NOT CHOOSE UNLESS THE DATA CHOOSES. If the intervals on the pairwise differences
include zero, the honest answer is that the test cannot separate the rules, and the decision goes to
the owner on the two priced boards. NO CURVE IS AVERAGED WITH ANOTHER — a blend would be a number no
measurement supplies.

NO ENGINE RUN. NO BOARD IS BUILT. NOTHING IS ADOPTED BY THIS FILE.
"""
import os, sys, json, math, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
F1DIR = os.path.join(REPO, 'docs/evidence/order_s_readonly_2026-08-19')
sys.path.insert(0, F1DIR)

SEED, B_BOOT = 32, 2000

# the three rules, at integer games; interpolated linearly between knots, held from 11
GUARD = [0.0, 0.1286875208353465, 0.23834489196711883, 0.23834489196711883, 0.23834489196711883,
         0.2455042373957035, 0.38568558243890977, 0.38568558243890977, 0.45188866847720316,
         0.8878514765964253, 0.8878514765964253, 1.0]
RAWC = [0.0, 0.1286875208353465, 0.4706058223361502, 0.4706058223361502, 0.4706058223361502,
        0.4706058223361502, 0.5711028628770571, 0.5711028628770571, 0.5711028628770571,
        1.0, 1.0, 1.0]
STEP = [min(1.0, g / 2.0) for g in range(12)]
RULES = [('RAW cells', RAWC), ('GUARDED isotonic', GUARD), ('the wired step min(1,g/2)', STEP)]
L = []


def P(s=''):
    print(s); L.append(str(s))


def c_of(g, tab):
    g = float(g)
    if g <= 0:
        return 0.0
    if g >= 11:
        return 1.0
    n = int(math.floor(g)); f = g - n
    return tab[n] if f <= 0 else (1 - f) * tab[n] + f * tab[min(n + 1, 11)]


# ---- F1's own population, built by F1's own code ---------------------------------------------------
_ns = {'__name__': '__as_oos__', '__file__': os.path.join(F1DIR, 'os_f1.py')}
_cwd = os.getcwd(); os.chdir(F1DIR)
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(os.path.join(F1DIR, 'os_f1.py')).read(), 'os_f1.py', 'exec'), _ns)
os.chdir(_cwd)
D2 = _ns['D2']

P('=' * 122)
P('ADJUDICATING THE I1 CREDIT RULE OUT OF SAMPLE — walk-forward by draft class. NOTHING IS ADOPTED.')
P('=' * 122)
P('population : F1\'s own depth-2 rows, built by its own rows_at_depth(2) — %d entrants' % len(D2))
P('estimand   : F1\'s own — the DISC-discounted house-ruler value from depth 2 on, over entry price')
P('rules      : RAW cells · GUARDED isotonic · the wired step min(1, g/2)')
P('folds      : train on draft classes < T, score on class T, walk T forward')
P('anchors    : R0 and R11 re-estimated INSIDE every fold from TRAINING ROWS ONLY')
P()

years = sorted(set(int(r['entry']) for r in D2))
P('draft classes present: %d to %d' % (years[0], years[-1]))

FOLDS = []
for T in years:
    tr = [r for r in D2 if int(r['entry']) < T]
    te = [r for r in D2 if int(r['entry']) == T]
    if len(tr) < 60 or len(te) < 8:
        continue
    g0 = [r['ratio'] for r in tr if r['g'] <= 0]
    g11 = [r['ratio'] for r in tr if r['g'] >= 11]
    if len(g0) < 8 or len(g11) < 8:
        continue
    FOLDS.append(dict(T=T, tr=tr, te=te,
                      R0=float(np.mean(g0)), R11=float(np.mean(g11)),
                      n_tr=len(tr), n_te=len(te)))
P('usable folds: %d  (a fold needs >=60 training rows, >=8 held-out rows, and >=8 rows at each anchor)'
  % len(FOLDS))
P()

# ---- score ------------------------------------------------------------------------------------------
PRED = {nm: [] for nm, _ in RULES}
TRUE = []
FOLDROWS = []
for F in FOLDS:
    idx0 = len(TRUE)
    for r in F['te']:
        TRUE.append(r['ratio'])
    for nm, tab in RULES:
        for r in F['te']:
            PRED[nm].append(F['R0'] + c_of(r['g'], tab) * (F['R11'] - F['R0']))
    FOLDROWS.append((F['T'], idx0, len(TRUE), F['n_tr'], F['n_te'], F['R0'], F['R11']))
TRUE = np.array(TRUE, dtype=float)
for nm in PRED:
    PRED[nm] = np.array(PRED[nm], dtype=float)
P('held-out rows scored, pooled over folds: %d' % len(TRUE))
P()

P('THE FOLD PATH — RMSE on the held-out class, per rule')
P('  %-8s %7s %7s %9s %9s   %10s %10s %10s'
  % ('class T', 'n_tr', 'n_te', 'R0_hat', 'R11_hat', 'RAW', 'GUARDED', 'STEP'))
for (T, a, b, ntr, nte, R0, R11) in FOLDROWS:
    e = {nm: math.sqrt(float(np.mean((PRED[nm][a:b] - TRUE[a:b]) ** 2))) for nm, _ in RULES}
    P('  %-8d %7d %7d %9.4f %9.4f   %10.4f %10.4f %10.4f'
      % (T, ntr, nte, R0, R11, e['RAW cells'], e['GUARDED isotonic'],
         e['the wired step min(1,g/2)']))
P()

P('POOLED OUT-OF-SAMPLE ERROR')
P('  %-30s %12s %12s' % ('rule', 'RMSE', 'MAE'))
POOL = {}
for nm, _ in RULES:
    rmse = math.sqrt(float(np.mean((PRED[nm] - TRUE) ** 2)))
    mae = float(np.mean(np.abs(PRED[nm] - TRUE)))
    POOL[nm] = dict(rmse=rmse, mae=mae)
    P('  %-30s %12.5f %12.5f' % (nm, rmse, mae))
P()

# ---- the paired differences, bootstrapped over FOLDS -------------------------------------------------
P('PAIRWISE DIFFERENCES, PAIRED BOOTSTRAP OVER FOLDS (B=%d, seed %d).' % (B_BOOT, SEED))
P('The arms are scored on IDENTICAL rows, so the bootstrap resamples FOLDS and keeps the arms paired')
P('inside each fold. A negative difference means the FIRST rule has the LOWER error, i.e. is better.')
P()
rng = np.random.default_rng(SEED)
spans = [(a, b) for (_T, a, b, _x, _y, _r0, _r11) in FOLDROWS]


def rmse_on(nm, picks):
    num = 0.0; den = 0
    for i in picks:
        a, b = spans[i]
        num += float(np.sum((PRED[nm][a:b] - TRUE[a:b]) ** 2)); den += (b - a)
    return math.sqrt(num / den) if den else float('nan')


DIFF = {}
P('  %-46s %10s %24s %s' % ('comparison', 'diff RMSE', '90% CI', 'separates?'))
for i in range(len(RULES)):
    for j in range(i + 1, len(RULES)):
        na, nb = RULES[i][0], RULES[j][0]
        pt = POOL[na]['rmse'] - POOL[nb]['rmse']
        draws = []
        for _ in range(B_BOOT):
            picks = rng.integers(0, len(spans), len(spans))
            draws.append(rmse_on(na, picks) - rmse_on(nb, picks))
        lo, hi = float(np.percentile(draws, 5)), float(np.percentile(draws, 95))
        sep = (lo > 0 or hi < 0)
        DIFF['%s vs %s' % (na, nb)] = dict(diff=pt, lo=lo, hi=hi, separates=bool(sep))
        P('  %-46s %10.5f   [%+.5f, %+.5f]   %s'
          % ('%s  vs  %s' % (na, nb), pt, lo, hi, 'YES' if sep else 'no — includes zero'))
P()

# ---- the verdict --------------------------------------------------------------------------------------
P('=' * 122)
P('THE VERDICT')
P('=' * 122)
any_sep = any(v['separates'] for v in DIFF.values())
best = min(POOL, key=lambda k: POOL[k]['rmse'])
if any_sep:
    P('*** THE TEST SEPARATES AT LEAST ONE PAIR. Lowest out-of-sample RMSE: %s ***' % best)
    for k, v in DIFF.items():
        if v['separates']:
            P('    separating pair: %s  (diff %+.5f, CI [%+.5f, %+.5f])' % (k, v['diff'], v['lo'], v['hi']))
    P('    Where a pair does NOT separate, the test is silent on that pair and says so.')
else:
    P('*** THE TEST CANNOT SEPARATE THE THREE RULES. Every pairwise interval includes zero. ***')
    P('    The lowest pooled RMSE is %s, but that ordering is INSIDE the noise and this seat will not' % best)
    P('    call it a winner. F1 already said the same thing in a different language: the guarded and')
    P('    raw readings have heavily overlapping intervals because the underlying cells hold 25-64')
    P('    players each. A test on the same data cannot manufacture a separation the data does not')
    P('    contain.')
    P()
    P('    SO THE CHOICE GOES TO THE OWNER, ON THE TWO PRICED BOARDS — not to this seat, and not to a')
    P('    tie-break rule invented for the occasion.')
    P()
    P('    AND A MIDDLE VALUE WOULD BE INVENTION. Averaging the guarded and raw curves produces a')
    P('    number that is neither a measured cell nor the house guard\'s output — it is a third object')
    P('    no measurement supplies. THE CURVES ARE NOT AVERAGED.')
P()
P('WHAT THIS TEST IS NOT. It scores how well each rule predicts the F1 estimand out of sample. It does')
P('NOT score board realism, and it cannot: the board is not an out-of-sample observable. A rule that')
P('wins here would still be a rule about credit for a short season, adopted on that basis alone.')

json.dump(dict(n_pop=len(D2), n_folds=len(FOLDS), n_scored=int(len(TRUE)),
               pooled=POOL, diffs=DIFF, separates=bool(any_sep), lowest_rmse=best,
               folds=[dict(T=T, n_tr=ntr, n_te=nte, R0=R0, R11=R11)
                      for (T, a, b, ntr, nte, R0, R11) in FOLDROWS],
               seed=SEED, boot=B_BOOT),
          open(os.path.join(HERE, 'CREDIT_OOS.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CREDIT_OOS_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: CREDIT_OOS.json · CREDIT_OOS_out.txt')
