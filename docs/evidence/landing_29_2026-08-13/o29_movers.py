#!/usr/bin/env python3
"""ORDER 29 -- THE COMPOSED MOVERS LEDGER.

Decomposes the board movement into LEVERS by building the board once per lever and differencing
consecutive stages, so the per-lever splits sum to the total BY CONSTRUCTION rather than by
reconciliation:

    LIVE  88ce647f   the frozen live board
      |  lever 1: THE UNFLAG-THREE  (store d9a24282 -> cb38ef11; reaches the board through the v3.4
      v              kernel head and hence BOARD_FACTOR -- see P3_INDIRECT_out.txt)
    B_U   71cbb13b   unflagged store, grace dial OFF
      |  lever 2: THE GRACE DIAL    (RL_GRACE default '0' -> '1')
      v
    B_G   0017657e   unflagged store, grace dial ON        <-- the last board this build can produce

    lever 3: THE v0 / CURVE RE-PRINT   ) BLOCKED at STEP 3 by the G-MONO halt
    lever 4: THE NUMERAIRE SCALAR      ) see STOP_STEP3_GMONO.md -- NOT measured, NOT estimated

Writes LANDING_29_MOVERS_2026-08-13.{md,json} into docs/ledgers/.
"""
import os, sys, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o29'
LEDG = ROOT + '/docs/ledgers'

STAGES = [
    ('LIVE', ROOT + '/engine/rl_after/rl_app_data.json'),
    ('B_U',  SP + '/bb_U/rl_after/rl_app_data.json'),
    ('B_G',  SP + '/bb_G/rl_after/rl_app_data.json'),
]
LEVERS = [
    ('lever 1 — THE UNFLAG-THREE', 'LIVE', 'B_U',
     'store d9a24282 -> cb38ef11; reaches every priced row through the v3.4 kernel head '
     '(3917 -> 3966) and hence BOARD_FACTOR (0.761344 -> 0.751937, -1.2355%)'),
    ('lever 2 — THE GRACE DIAL', 'B_U', 'B_G',
     "RL_GRACE code default '0' -> '1'; entry age <= 19 carries seasons 1 and 2 at full weight"),
]
NAMED = ['harrison-ramm', 'kentfield', 'liddy', 'hansen', 'visentini', 'nicholas-martin',
         'herbert', 'jai-newcombe', 'willem-duursma', 'harry-sheezel']


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def load(p):
    return {r['key']: r for r in json.load(open(p))['active']}


B = {n: load(p) for n, p in STAGES}
H = {n: md5(p) for n, p in STAGES}
STORE = {}
for p in json.load(open(ROOT + '/engine/rl_after/rl_model_data.json')):
    k = p.get('key')
    if k and k not in STORE: STORE[k] = p

keys = sorted(B['LIVE'])
for n, _ in STAGES:
    assert set(B[n]) == set(keys), "ROW SET CHANGED at stage %s -- structural defect, halt" % n

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def v(stage, k):
    return B[stage][k].get('v')


AGE_REF = 2026
def by(p): return p.get('_by') or (p['year'] - 18)
def debut(p): return p['year'] if p.get('type') == 'MSD' else p['year'] + 1
def entry_age(p): return p['year'] - by(p)
def grace_of(p): return max(0, 1 - max(0, AGE_REF - debut(p))) if entry_age(p) <= 19 else 0


P("# LANDING 29 — THE COMPOSED MOVERS LEDGER")
P()
P("**2026-08-13 · branch `land/order-29` · ORDER 29, the landing build.**")
P()
P("> ## THIS LEDGER IS PARTIAL, AND SAYS SO IN ITS FIRST LINE.")
P("> The landing **STOPPED at Step 3**: the ruled curve halts the engine on G-MONO strict descent")
P("> (`STOP_STEP3_GMONO.md`). Two of the four levers were built and are measured here in full, every")
P("> player, exactly. The other two — the v0/curve re-print and the numéraire scalar — were **never")
P("> built**, so they are **absent, not estimated**. No row below carries a modelled or inferred")
P("> component; every number is a difference of two boards that exist on disk.")
P()
P("## THE STAGES")
P()
P("| stage | what it is | `rl_app_data.json` md5 |")
P("|---|---|---|")
P("| **LIVE** | the frozen live board | `%s` |" % H['LIVE'])
P("| **B_U** | + the unflag-three (store `cb38ef11`), dial OFF | `%s` |" % H['B_U'])
P("| **B_G** | + the grace dial ON (the last board this build can produce) | `%s` |" % H['B_G'])
P("| ~~B_V~~ | + the curve / v0 re-print | **BLOCKED — never built** |")
P("| ~~B_F~~ | + the numéraire re-pin (the intended FINAL board) | **BLOCKED — never built** |")
P()
P("Each lever is the difference of **consecutive** stages, so the lever columns sum to the total")
P("**by construction**. The reconciliation assert below is therefore a check on the arithmetic and")
P("the row alignment, not a fudge factor: it must be exactly zero for every row.")
P()

# ---------------------------------------------------------------- totals
P("## 1. BOARD TOTALS")
P()
tot = {n: sum(v(n, k) for k in keys if v(n, k) is not None) for n, _ in STAGES}
P("| stage | board total | Δ vs previous | Δ vs LIVE |")
P("|---|---|---|---|")
prev = None
for n, _ in STAGES:
    d1 = "—" if prev is None else "%+d (%+.4f%%)" % (tot[n] - tot[prev], 100.0 * (tot[n] / tot[prev] - 1))
    d2 = "—" if n == 'LIVE' else "%+d (%+.4f%%)" % (tot[n] - tot['LIVE'], 100.0 * (tot[n] / tot['LIVE'] - 1))
    P("| %s | %s | %s | %s |" % (n, "{:,}".format(tot[n]), d1, d2))
    prev = n
P()

# national vs pool split
def is_pool(k):
    p = STORE.get(k)
    if not p: return None
    if p.get('_pickless') or p.get('pick') is None: return True
    return p.get('type') != 'ND' or (p.get('pick') or 0) > 64


nat = [k for k in keys if is_pool(k) is False]
pool = [k for k in keys if is_pool(k) is True]
P("### the national / pool split")
P()
P("| population | n | LIVE | B_U | B_G | Δ vs LIVE |")
P("|---|---|---|---|---|---|")
for lab, ks in (('national (ND 1–64)', nat), ('pool (everything past 64)', pool)):
    s = {n: sum(v(n, k) for k in ks if v(n, k) is not None) for n, _ in STAGES}
    P("| %s | %d | %s | %s | %s | %+d (%+.4f%%) |"
      % (lab, len(ks), "{:,}".format(s['LIVE']), "{:,}".format(s['B_U']), "{:,}".format(s['B_G']),
         s['B_G'] - s['LIVE'], 100.0 * (s['B_G'] / s['LIVE'] - 1)))
P()

# ---------------------------------------------------------------- movers
P("## 2. THE MOVER COUNT, PER LEVER")
P()
P("| lever | movers | up | down | Σ Δ | what it is |")
P("|---|---|---|---|---|---|")
lev_rows = {}
for name, a, b, doc in LEVERS:
    mv = [k for k in keys if v(a, k) is not None and v(b, k) is not None and v(a, k) != v(b, k)]
    up = [k for k in mv if v(b, k) > v(a, k)]
    dn = [k for k in mv if v(b, k) < v(a, k)]
    lev_rows[name] = mv
    P("| %s | **%d** | %d | %d | %+d | %s |"
      % (name, len(mv), len(up), len(dn), sum(v(b, k) - v(a, k) for k in mv), doc))
tot_mv = [k for k in keys if v('LIVE', k) is not None and v('B_G', k) is not None and v('LIVE', k) != v('B_G', k)]
P("| **TOTAL (LIVE → B_G)** | **%d of %d** | %d | %d | %+d | the two landed levers composed |"
  % (len(tot_mv), len(keys),
     len([k for k in tot_mv if v('B_G', k) > v('LIVE', k)]),
     len([k for k in tot_mv if v('B_G', k) < v('LIVE', k)]),
     tot['B_G'] - tot['LIVE']))
P()

# ---------------------------------------------------------------- reconciliation
P("## 3. THE RECONCILIATION — EXACT, EVERY ROW")
P()
worst = 0
nbad = 0
for k in keys:
    if v('LIVE', k) is None or v('B_G', k) is None: continue
    legs = (v('B_U', k) - v('LIVE', k)) + (v('B_G', k) - v('B_U', k))
    resid = legs - (v('B_G', k) - v('LIVE', k))
    if resid: nbad += 1
    worst = max(worst, abs(resid))
P("For every one of the %d priced rows:" % len([k for k in keys if v('LIVE', k) is not None]))
P()
P("```")
P("  (lever 1) + (lever 2)  ==  total(LIVE -> B_G)")
P("  rows failing to reconcile : %d" % nbad)
P("  max |residual|           : %d" % worst)
P("```")
P()
P("**%s** — the levers sum to the total exactly, with no unexplained remainder."
  % ("PASS" if nbad == 0 else "FAIL"))
assert nbad == 0

# ---------------------------------------------------------------- dispersion
P()
P("## 4. DISPERSION (never a bare mean)")
P()
def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


P("| lever | min | p05 | median | mean | p95 | max |")
P("|---|---|---|---|---|---|---|")
for name, a, b, doc in LEVERS:
    mv = lev_rows[name]
    if not mv:
        P("| %s | — | — | — | — | — | — |" % name); continue
    rel = [100.0 * (v(b, k) / v(a, k) - 1) for k in mv if v(a, k)]
    P("| %s (relative) | %+.2f%% | %+.2f%% | **%+.2f%%** | %+.2f%% | %+.2f%% | %+.2f%% |"
      % (name, min(rel), q(rel, .05), q(rel, .5), sum(rel) / len(rel), q(rel, .95), max(rel)))
    ab = [v(b, k) - v(a, k) for k in mv]
    P("| %s (absolute) | %+d | %+d | **%+d** | %+.1f | %+d | %+d |"
      % (name, min(ab), q(ab, .05), q(ab, .5), sum(ab) / len(ab), q(ab, .95), max(ab)))
P()

# ---------------------------------------------------------------- named rows
P("## 5. THE NAMED ROWS (PREREG P14)")
P()
P("P14 names ten rows to be reported live → landed with their per-lever split. They are reported")
P("here **live → B_G**, which is as far as the landing got. Two of the four levers never ran, so")
P("P14 cannot be scored as written — see the packet.")
P()
P("| row | pos | pick | entry age | grace | LIVE | lever 1 | lever 2 | B_G | Δ vs LIVE |")
P("|---|---|---|---|---|---|---|---|---|---|")
found = []
for want in NAMED:
    ks = [k for k in keys if want in k]
    for k in sorted(ks):
        p = STORE.get(k, {})
        found.append(k)
        P("| **%s** | %s | %s | %s | %d | %d | %+d | %+d | %d | %+d (%+.2f%%) |"
          % (k, p.get('present_position') or p.get('pos') or '—',
             p.get('pick') if p.get('pick') is not None else 'pool',
             entry_age(p) if p else '—', grace_of(p) if p else 0,
             v('LIVE', k), v('B_U', k) - v('LIVE', k), v('B_G', k) - v('B_U', k), v('B_G', k),
             v('B_G', k) - v('LIVE', k), 100.0 * (v('B_G', k) / v('LIVE', k) - 1)))
P()

# ---------------------------------------------------------------- top movers
P("## 6. THE LARGEST MOVERS, LIVE → B_G")
P()
P("| # | key | pos | pick | entry age | grace | LIVE | lever 1 | lever 2 | B_G | Δ | Δ pct |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|")
top = sorted(tot_mv, key=lambda k: -abs(v('B_G', k) - v('LIVE', k)))[:25]
for i, k in enumerate(top, 1):
    p = STORE.get(k, {})
    P("| %d | %s | %s | %s | %s | %d | %d | %+d | %+d | %d | **%+d** | %+.2f%% |"
      % (i, k, p.get('present_position') or p.get('pos') or '—',
         p.get('pick') if p.get('pick') is not None else 'pool',
         entry_age(p) if p else '—', grace_of(p) if p else 0,
         v('LIVE', k), v('B_U', k) - v('LIVE', k), v('B_G', k) - v('B_U', k), v('B_G', k),
         v('B_G', k) - v('LIVE', k), 100.0 * (v('B_G', k) / v('LIVE', k) - 1)))
P()

# ---------------------------------------------------------------- the grace control group
P("## 7. THE CONTROL GROUP — WHO THE GRACE DIAL MUST NOT REACH")
P()
ctrl = [k for k in keys if STORE.get(k) and debut(STORE[k]) == 2026 and entry_age(STORE[k]) >= 20]
moved = [k for k in ctrl if v('B_G', k) != v('B_U', k)]
P("Rows debuting 2026 at entry age >= 20 — the ruled discrimination (20+ gets no grace):")
P()
P("```")
P("  rows in the control group          : %d" % len(ctrl))
P("  moved by lever 2 (the grace dial)  : %d" % len(moved))
P("```")
P()
P("**%s** — the dial's own leg moves them by exactly zero, which is the ruling visible in the data"
  % ("PASS" if not moved else "FAIL: %s" % moved[:8]))
P("rather than asserted in a sentence. (They still move under lever 1, which is a board-wide scalar")
P("and reaches every priced row by construction.)")
P()

# ---------------------------------------------------------------- per-player table
P("## 8. EVERY PLAYER")
P()
P("All %d priced rows, per-lever. Rows are ordered by |Δ vs LIVE| descending." % len(keys))
P()
P("| key | pos | pick | LIVE | lever 1 (unflag) | lever 2 (grace) | B_G | Δ | Δ pct |")
P("|---|---|---|---|---|---|---|---|---|")
allrows = sorted([k for k in keys if v('LIVE', k) is not None],
                 key=lambda k: -abs(v('B_G', k) - v('LIVE', k)))
for k in allrows:
    p = STORE.get(k, {})
    P("| %s | %s | %s | %d | %+d | %+d | %d | %+d | %+.2f%% |"
      % (k, p.get('present_position') or p.get('pos') or '—',
         p.get('pick') if p.get('pick') is not None else 'pool',
         v('LIVE', k), v('B_U', k) - v('LIVE', k), v('B_G', k) - v('B_U', k), v('B_G', k),
         v('B_G', k) - v('LIVE', k),
         100.0 * (v('B_G', k) / v('LIVE', k) - 1) if v('LIVE', k) else float('nan')))
P()
P("---")
P()
P("*Levers 3 (v0 / curve re-print) and 4 (the numéraire scalar) are absent because they were never")
P("built. `STOP_STEP3_GMONO.md` records why, with the engine's own halt transcript.*")

os.makedirs(LEDG, exist_ok=True)
open(LEDG + '/LANDING_29_MOVERS_2026-08-13.md', 'w').write("\n".join(LOG) + "\n")

out = {'stages': {n: {'md5': H[n], 'total': tot[n]} for n, _ in STAGES},
       'blocked_levers': ['v0/curve re-print', 'numeraire scalar'],
       'stop': 'STOP_STEP3_GMONO.md — G-MONO strict descent halt',
       'reconciliation': {'rows_failing': nbad, 'max_residual': worst},
       'levers': [{'name': n, 'from': a, 'to': b, 'doc': d, 'movers': len(lev_rows[n]),
                   'sum_delta': sum(v(b, k) - v(a, k) for k in lev_rows[n])}
                  for n, a, b, d in LEVERS],
       'rows': [{'key': k,
                 'pos': (STORE.get(k) or {}).get('present_position'),
                 'pick': (STORE.get(k) or {}).get('pick'),
                 'live': v('LIVE', k), 'b_u': v('B_U', k), 'b_g': v('B_G', k),
                 'lever1_unflag': v('B_U', k) - v('LIVE', k),
                 'lever2_grace': v('B_G', k) - v('B_U', k),
                 'total': v('B_G', k) - v('LIVE', k)}
                for k in allrows]}
json.dump(out, open(LEDG + '/LANDING_29_MOVERS_2026-08-13.json', 'w'), indent=1)
print("\nwritten: docs/ledgers/LANDING_29_MOVERS_2026-08-13.{md,json}")
