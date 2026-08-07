"""STAGE 6 — the AXIS PROBE.  Measurement first, then the choice (the stage-4 lesson).

The directive's conditioning list names a "demonstrated level" axis whose job is the owner's
"already priced in" cell.  Three engine-native continuous candidates are measured here on the SAME
frozen rows; the one that separates the residual best (value-weighted deviance under a single
one-dimensional shape) is the one the teach uses, and the choice is declared in the memo.

  pr    bestlvl(p,Y)/par            — level against the CLASS par, what ev() already computes
  rerate log(price/entry_anchor)    — how far the engine has ALREADY re-rated him off his entry price
  ppg   gcum-normalised level       — level x exposure

No fitting here, no tuning: this is a printed table.
"""
import os, json
import numpy as np

OUT = os.environ.get('RL_OUT', '.')
R = json.load(open(OUT + '/s6_rows.json'))
Y1 = [x for x in R if x['N'] == 1 and x['nd'] and 1 <= x['pk'] <= 64]

def vw(rows):
    sp = sum(x['price'] for x in rows)
    return (sum(x['F'] for x in rows) / sp) if sp > 0 else float('nan')

def dev(rows, key, nq=5):
    """value-weighted deviance of the residual r=F-price about a step function on `key` (nq quantiles)."""
    xs = sorted(rows, key=lambda x: x[key])
    tot = 0.0; base = 0.0
    gm = vw(rows) - 1.0
    for j in range(nq):
        sub = xs[j * len(xs) // nq:(j + 1) * len(xs) // nq]
        if not sub: continue
        d = vw(sub) - 1.0
        for x in sub:
            tot += x['price'] * (x['F'] / x['price'] - 1.0 - d) ** 2
            base += x['price'] * (x['F'] / x['price'] - 1.0 - gm) ** 2
    return 1.0 - tot / base, [(round(vw(xs[j*len(xs)//nq:(j+1)*len(xs)//nq]), 4),
                               round(xs[j*len(xs)//nq]['_k'], 4)) for j in range(nq)]

for x in Y1:
    # THE RE-RATE STATISTIC, computed off the PRODUCTION leg `e` (never off the corrected price):
    # a pure state function of the record to date, so no build-to-build feedback channel exists.
    x['rerate'] = float(np.log(max(x['e'], 1.0) / max(x['A'], 1.0)))
    x['ppg'] = x['pr'] * min(x['gcum'], 22.0) / 22.0
    x['lpk'] = float(np.log(max(x['pk'], 1)))

print("year-1 established ND 1-64: n=%d  value-weighted agg F' = %.4f  median F' = %.4f"
      % (len(Y1), vw(Y1), float(np.median([x['F'] / x['price'] for x in Y1]))))
print()
for key in ('pr', 'rerate', 'ppg', 'gcum', 'lpk'):
    for x in Y1: x['_k'] = x[key]
    r2, cells = dev(Y1, key)
    print("%-8s  R2(vw, 5 quantiles) = %7.4f   cell aggs (F' , knot) = %s" % (key, r2, cells))
print()
print("== the already-priced cells under each candidate ==")
for key, lab in (('pr', 'pr'), ('rerate', 'log(price/anchor)')):
    xs = sorted(Y1, key=lambda x: x[key]); med = xs[len(xs) // 2][key]; t2 = xs[2 * len(xs) // 3][key]
    a = [x for x in Y1 if x['pk'] <= 20 and x[key] >= med]
    b = [x for x in Y1 if x['pk'] <= 10 and x[key] >= t2]
    print("  %-18s picks 1-20 x above-median: n=%3d agg %.4f  |  picks 1-10 x top-tercile: n=%3d agg %.4f"
          % (lab, len(a), vw(a), len(b), vw(b)))
