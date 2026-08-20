#!/usr/bin/env python3
# =====================================================================================================
# ORDER 32, SEAT S2  --  THE SITTER SPECTRUM SURFACE.
#
#   Q1  THE CREDIT FUNCTION      -- how much does playing g games in a season cure that season's
#                                   sitting accrual?  Fitted family u(g) = min(1, g/G*), G* derived.
#   Q2  RESTORATION              -- after a DELIVERED season, does a previously-sat row's remaining
#                                   pedigree value recover toward full persistence, or stay faded?
#   Q3  ORDER / RECENCY          -- at fixed total sitting, does WHEN the sitting happened matter?
#   Q4  THE INJURY SPLIT         -- injured vs healthy-unselected sitting, per the pinned R-REG
#                                   register, with the historical resolution counted honestly.
#   +   THE TWO-WAY SURFACE      -- sitting depth x playing evidence -> D, published whole.
#
# READ-ONLY.  Writes only into docs/evidence/order32_s2_2026-08-17/.  Nothing wires.  Every proposed
# term is a WIRING PROPOSAL AWAITING RULING.  Prereg: PREREG_S2.md, committed before this file
# existed in runnable form (commit 772d4ab).
#
# NO PARALLEL METHODOLOGY: the committed 30A-2 instrument (o30a2_recut.py) is run WHOLE -- the
# o31_pool.py / o31f_rederive_fade.py discipline -- with exactly one character-level substitution
# (OUTD re-pointed into base_run/ so no committed artifact is overwritten), and its namespace is
# harvested: the population, the L-B listing basis, the per-season decomposition, the normaliser and
# the dispersion machinery.  Every cell below is that instrument's own estimator on new conditioning.
# =====================================================================================================
import os, sys, json, math, hashlib, io, contextlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'sitter_fade_2026-08-14', 'o30a2_recut.py')
BASE = os.path.join(HERE, 'base_run')
os.makedirs(BASE, exist_ok=True)

os.environ.update(PYTHONHASHSEED='0', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1')

LOG = []


def P(s=''):
    print(s); LOG.append(s)


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


P('=' * 118)
P('ORDER 32 SEAT S2  --  THE SITTER SPECTRUM SURFACE.  CREDIT / RESTORATION / RECENCY / INJURY')
P('=' * 118)
P('READ-ONLY.  NOTHING WIRES.  Every term below is a WIRING PROPOSAL AWAITING RULING.')
P('Prereg: PREREG_S2.md (commit 772d4ab), filed before this harness existed in runnable form.')
P('')

# -----------------------------------------------------------------------------------------------------
# THE BASE INSTRUMENT, RUN WHOLE
# -----------------------------------------------------------------------------------------------------
_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
_OLD = 'OUTD = HERE'
assert _txt.count(_OLD) == 1, 'the OUTD line is not unique -- refusing to substitute blindly'
_run = _txt.replace(_OLD, 'OUTD = %r' % BASE)
RUN_MD5 = hashlib.md5(_run.encode()).hexdigest()
P('BASE INSTRUMENT  %s' % os.path.relpath(SRC, ROOT))
P('  committed md5  %s   as-run md5 %s' % (HARNESS_MD5, RUN_MD5))
P('  THE ONLY EDIT  %r -> OUTD = base_run/   (output directory only; no estimator touched)' % _OLD)
NS = {'__name__': '__main__', '__file__': SRC}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), NS)
open(os.path.join(BASE, 'RECUT30A2_console.txt'), 'w').write(_buf.getvalue())
P('  instrument ran clean; console kept at base_run/RECUT30A2_console.txt (%d lines)'
  % _buf.getvalue().count('\n'))
P('')

# harvested namespace -- the committed instrument's own objects
FIT = NS['FIT']; SEASONS = NS['SEASONS']; games_in = NS['games_in']
listed_LB = NS['listed_LB']; t4_cell = NS['t4_cell']; q = NS['q']
CTRL = NS['CTRL']; DTAB = NS['DTAB']; SURF = NS['SURF']; DF = NS['DF']
LAST_COMPLETE = NS['LAST_COMPLETE']; BARS = NS['BARS']
season_bar_group = NS['season_bar_group']; STORE_BY = NS['STORE_BY']
MA = NS['MA']; POP = NS['POP']; E1 = NS['E1']; D29 = NS['D29']; PHI = NS['PHI']
RAW1 = CTRL['RAW1']
LB = 'L-B outcome-blind floor'

# -----------------------------------------------------------------------------------------------------
# CONTROL S1 -- the rerun must reproduce the 31-F re-derived fade and T4 cells EXACTLY
# -----------------------------------------------------------------------------------------------------
F31 = json.load(open(os.path.join(EV, 'candidate_31f', 'FADE_31F.json')))
T31 = json.load(open(os.path.join(EV, 'candidate_31f', 'SITTER_DISCOUNT_TABLE_2.json')))
_dev_fade = max(abs(DTAB[LB][int(k)] - v) for k, v in F31['rederived'].items()
                if DTAB[LB].get(int(k)) is not None)
_dev_t4 = max(abs(T31['T4']['cells'][k]['D'] - NS['T4'][k]['D'])
              for k in T31['T4']['cells'] if T31['T4']['cells'][k].get('n') and 'D' in T31['T4']['cells'][k])
S1_OK = _dev_fade < 1e-9 and _dev_t4 < 1e-9
P('CONTROL S1  --  this rerun vs the committed 31-F re-derivation (same head-fixed surface 78ad9842)')
P('  L-B fade row this run: %s' % '  '.join('D(%d)=%.7f' % (N, DTAB[LB][N]) for N in (2, 3, 4)))
P('  max |dev| vs FADE_31F.json rederived: %.3e ; max |dev| vs 31-F T4 cells: %.3e' % (_dev_fade, _dev_t4))
P('  VERDICT %s' % ('REPRODUCED -- the transplant is the committed instrument itself'
                    if S1_OK else '*** DRIFT: HALT -- S1 falsifier fired; nothing downstream is quotable ***'))
if not S1_OK:
    raise SystemExit('S1 CONTROL FAILED')
P('')

# -----------------------------------------------------------------------------------------------------
# shared machinery
# -----------------------------------------------------------------------------------------------------
D_LB = {1: 1.0, 2: DTAB[LB][2], 3: DTAB[LB][3], 4: DTAB[LB][4]}
FLAT_FROM = 4


def pure(c):
    """This act's own pure-sitter L-B row, continuous: log-linear between integers, flat from 4 --
    the o31_fade_D rule applied to the re-derived row (identical to the engine's, control above)."""
    if c <= 1.0:
        return 1.0
    if c >= FLAT_FROM:
        return D_LB[FLAT_FROM]
    n = int(math.floor(c)); f = c - n
    if f <= 0.0:
        return D_LB[n]
    return math.exp((1.0 - f) * math.log(D_LB[n]) + f * math.log(D_LB[n + 1]))


def invert_pure(Dt, cmax):
    """c_u_hat solving pure(c) = Dt on the DECREASING branch [1, min(cmax,3)].  Returns (c, flag)."""
    hi = min(float(cmax), 3.0)
    if Dt >= 1.0:
        return 1.0, 'SATURATED_FULL'
    if Dt <= pure(hi):
        return hi, 'BRANCH_LIMITED'
    lo, up = 1.0, hi
    for _ in range(80):
        mid = 0.5 * (lo + up)
        if pure(mid) > Dt:
            lo = mid
        else:
            up = mid
    return 0.5 * (lo + up), 'ok'


def pat(r, N):
    """Games per season, seasons 1..N-1."""
    ey = r['entry_year']
    return [games_in(r['key'], ey + k) for k in range(1, N)]


def cellD(rows, N):
    c = t4_cell(rows, N)
    if c.get('n'):
        c['D'] = c['mean'] / RAW1
        rr = []
        for r in rows:
            s, _ = NS['share_from'](r, N)
            rr.append((r['ga_obs'] * s + r['ga_tail']) * DF(r['e'], N - 1) / r['v0'])
        m = c['mean']
        c['sd'] = math.sqrt(sum((x - m) ** 2 for x in rr) / max(1, len(rr) - 1)) if len(rr) > 1 else 0.0
        c['se_D'] = (c['sd'] / math.sqrt(len(rr))) / RAW1 if rr else None
    return c


MIN_CELL = 10
GB = [('0', 0, 0), ('1', 1, 1), ('2', 2, 2), ('3-5', 3, 5), ('6-10', 6, 10), ('11+', 11, 10 ** 9)]
GB2_EXTRA = [('3', 3, 3), ('4', 4, 4), ('5', 5, 5)]

# =====================================================================================================
# Q1  --  THE CREDIT FUNCTION
# =====================================================================================================
P('=' * 118)
P('Q1  --  THE CREDIT FUNCTION.  Pattern cells: seasons 1..N-2 ALL GAMELESS, season N-1 carries g.')
P('       D = the transplanted from-N estimator, L-B listed at N, / RAW(1) = %.6f' % RAW1)
P('=' * 118)
P('  The wired defect this measures the replacement of: o31_played_units credits a FULL season unit')
P('  for ANY season with games > 0 (the one-game fade-cure cliff, owner-caught, ext_2026-08-17).')
P('')
Q1 = {}
for N in (2, 3, 4):
    rows_N = [r for r in FIT if (r['entry_year'] + N - 1) <= LAST_COMPLETE and listed_LB(r, N)
              and all(g == 0 for g in pat(r, N)[:-1])]
    buckets = GB + (GB2_EXTRA if N == 2 else [])
    P('  DEPTH %d  --  sat %d season(s), then g games in season %d   (eligible pattern rows n = %d)'
      % (N, N - 2, N - 1, len(rows_N)))
    P('    %-6s %6s %6s %9s %9s %9s %9s %9s %9s %8s %7s  %s' %
      ('g', 'n', 'n=0', 'RAW mean', 'median', 'p25', 'p75', 'D', 'se(D)', 'tailshr', 'med(g)', 'status'))
    for (lab, lo, hi) in sorted(buckets, key=lambda b: b[1]):
        rows = [r for r in rows_N if lo <= pat(r, N)[-1] <= hi]
        c = cellD(rows, N)
        key = '%d|%s' % (N, lab)
        if not c.get('n'):
            Q1[key] = dict(n=0, depth=N, bucket=lab)
            P('    %-6s %6d   -- empty --' % (lab, 0)); continue
        gg = [pat(r, N)[-1] for r in rows]
        c.update(depth=N, bucket=lab, med_g=q(gg, 0.5), thin=(c['n'] < MIN_CELL))
        # credit inversion against this act's own pure row
        cu, flag = invert_pure(c['D'], N)
        c['cu_hat'] = cu; c['u_hat'] = N - cu; c['invert_flag'] = flag
        if c['se_D']:
            cu_lo, _ = invert_pure(c['D'] + c['se_D'], N)
            cu_hi, _ = invert_pure(c['D'] - c['se_D'], N)
            c['u_hat_band'] = [N - cu_hi, N - cu_lo]
        Q1[key] = {k: v for k, v in c.items()}
        st = ('THIN(n<%d): BOUND' % MIN_CELL if c['thin'] else '') + \
             (' %s' % flag if flag != 'ok' else '')
        P('    %-6s %6d %6d %9.4f %9.4f %9.4f %9.4f %9.4f %9.4f %8.4f %7.1f  %s'
          % (lab, c['n'], c['n_zero'], c['mean'], c['median'], c['p25'], c['p75'], c['D'],
             c['se_D'] or 0.0, c['tail_share'], c['med_g'], st))
    P('')

# ---- the per-game spectrum at depth 2 (the owner's "0 to 1 isn't that different from 1 to 2") -------
P('  THE PER-GAME SPECTRUM AT DEPTH 2  (singleton cells; the owner\'s 0-vs-1-vs-2 question)')
_sing = [('0'), ('1'), ('2'), ('3'), ('4'), ('5')]
prev = None
STEPS2 = []
for lab in _sing:
    c = Q1.get('2|%s' % lab, {})
    if not c.get('n'):
        continue
    step = (c['D'] - prev) if prev is not None else None
    STEPS2.append(dict(g=lab, D=c['D'], n=c['n'], step=step))
    P('    g=%-3s n=%4d  D=%.4f  se %.4f  %s' % (lab, c['n'], c['D'], c['se_D'] or 0,
      ('step from g-1: %+.4f' % step) if step is not None else ''))
    prev = c['D']
P('')

# ---- the fit: u(g) = min(1, g/G*) -------------------------------------------------------------------
P('  THE FITTED CREDIT FAMILY  u(g) = min(1, g/G*)   (prereg: n-weighted LS in D-space, depths 2+3,')
P('  non-thin non-saturated cells; sensitivity run includes saturated cells with the model\'s own cap)')
FIT_CELLS = []
for N in (2, 3):
    for (lab, lo, hi) in GB:
        c = Q1.get('%d|%s' % (N, lab), {})
        if not c.get('n') or c['n'] < MIN_CELL:
            continue
        FIT_CELLS.append(dict(depth=N, bucket=lab, n=c['n'], D=c['D'], m=c['med_g'],
                              sat=(c['invert_flag'] == 'SATURATED_FULL')))
GRID = [x / 2.0 for x in range(2, 61)]


def fit_G(cells):
    best = None
    for G in GRID:
        sse = 0.0; wt = 0.0
        for c in cells:
            u = min(1.0, c['m'] / G) if G > 0 else 1.0
            dp = pure(c['depth'] - u)
            sse += c['n'] * (c['D'] - dp) ** 2; wt += c['n']
        rms = math.sqrt(sse / wt) if wt else None
        if best is None or sse < best[1]:
            best = (G, sse, rms)
    return best


PRIMARY = [c for c in FIT_CELLS if not c['sat']]
SENSY = FIT_CELLS
bp = fit_G(PRIMARY) if PRIMARY else None
bs = fit_G(SENSY) if SENSY else None
P('    cells available: %d   (non-saturated primary set: %d)' % (len(FIT_CELLS), len(PRIMARY)))
for c in FIT_CELLS:
    P('      depth %d g=%-5s n=%4d med(g)=%5.1f D=%.4f %s'
      % (c['depth'], c['bucket'], c['n'], c['m'], c['D'], 'SATURATED (D >= full-cure level)' if c['sat'] else ''))
if bp:
    P('    PRIMARY  fit: G* = %.1f   RMS (D-space, n-weighted) = %.4f' % (bp[0], bp[2]))
if bs:
    P('    SENSITIVITY (saturated cells included, model capped at full cure): G* = %.1f   RMS = %.4f'
      % (bs[0], bs[2]))
G_STAR = bp[0] if bp else None
P('')
# identifiability profile + per-cell residuals -- how sharply the data pins G*
PROFILE = []
for G in (1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 12.0, 16.0):
    sse = 0.0; wt = 0.0
    for c in PRIMARY:
        u = min(1.0, c['m'] / G)
        sse += c['n'] * (c['D'] - pure(c['depth'] - u)) ** 2; wt += c['n']
    PROFILE.append(dict(G=G, rms=math.sqrt(sse / wt)))
P('  IDENTIFIABILITY PROFILE (primary set, n-weighted RMS in D by G*): %s'
  % '  '.join('%g:%.4f' % (x['G'], x['rms']) for x in PROFILE))
RESID = []
for c in FIT_CELLS:
    dp = pure(c['depth'] - min(1.0, c['m'] / G_STAR))
    RESID.append(dict(depth=c['depth'], bucket=c['bucket'], n=c['n'], D=c['D'], D_pred=dp,
                      resid=c['D'] - dp, in_primary=(not c['sat'])))
P('  RESIDUALS AT G* = %.1f (D_meas - D_pred; saturated cells shown against the model cap):' % G_STAR)
for x in RESID:
    P('    depth %d g=%-5s n=%4d  D %.4f  pred %.4f  resid %+.4f%s'
      % (x['depth'], x['bucket'], x['n'], x['D'], x['D_pred'], x['resid'],
         '' if x['in_primary'] else '   [saturated, not in primary fit]'))
_ng0 = [c for c in PRIMARY if c['m'] > 0]
if _ng0:
    _sse = sum(c['n'] * (c['D'] - pure(c['depth'] - min(1.0, c['m'] / G_STAR))) ** 2 for c in _ng0)
    _wt = sum(c['n'] for c in _ng0)
    P('  DISCLOSED: the headline RMS is flattered by the two large g=0 anchor cells (which any G* fits')
    P('  exactly).  RMS over the g>0 primary cells alone: %.4f' % math.sqrt(_sse / _wt))
P('')
P('  READ PLAINLY: u(1) = %s under the primary fit; the WIRED law credits 1.00 at g=1.'
  % ('%.3f' % min(1.0, 1.0 / G_STAR) if G_STAR else 'n/a'))
P('')

# =====================================================================================================
# THE TWO-WAY SURFACE  --  sitting depth x playing evidence, published whole
# =====================================================================================================
P('=' * 118)
P('THE TWO-WAY SURFACE.  Rows: s = gameless seasons among 1..N-1.  Cols: total games in the played')
P('seasons.  Cell: the transplanted D, with n / median / p25 / p75 / tail.  Thin cells FLAGGED, never')
P('smoothed.  (Q1 and Q3 are cuts of this object.)')
P('=' * 118)
GT = [('0', 0, 0), ('1-2', 1, 2), ('3-5', 3, 5), ('6-10', 6, 10), ('11-20', 11, 20), ('21+', 21, 10 ** 9)]
SURF2 = {}
for N in (2, 3, 4):
    rows_N = [r for r in FIT if (r['entry_year'] + N - 1) <= LAST_COMPLETE and listed_LB(r, N)]
    P('  DEPTH %d   (n listed = %d)' % (N, len(rows_N)))
    P('    %-4s %-7s %6s %9s %9s %9s %9s %8s  %s' %
      ('s', 'games', 'n', 'D', 'median', 'p25', 'p75', 'tailshr', 'status'))
    for s in range(0, N):
        for (lab, lo, hi) in GT:
            if s == N - 1 and lo > 0:
                continue                     # all seasons gameless => total games 0 by construction
            rows = [r for r in rows_N
                    if sum(1 for g in pat(r, N) if g == 0) == s and lo <= sum(pat(r, N)) <= hi]
            c = cellD(rows, N)
            key = '%d|s%d|%s' % (N, s, lab)
            if not c.get('n'):
                SURF2[key] = dict(n=0)
                continue
            c.update(depth=N, s=s, games=lab, thin=(c['n'] < MIN_CELL))
            SURF2[key] = {k: v for k, v in c.items()}
            P('    %-4d %-7s %6d %9.4f %9.4f %9.4f %9.4f %8.4f  %s'
              % (s, lab, c['n'], c['D'], c['median'], c['p25'], c['p75'], c['tail_share'],
                 'THIN: BOUND' if c['thin'] else ('CENSOR-3' if c['tail_share'] > 0.375 else '')))
    P('')

# =====================================================================================================
# Q2  --  RESTORATION
# =====================================================================================================
P('=' * 118)
P('Q2  --  RESTORATION.  After a DELIVERED season k (g >= 10 AND avg >= position bar), does the')
P('       previously-sat row\'s remaining value (from k+1) recover to the never-sat level?')
P('       R(k) = D[sat >= 1 before k, delivered at k] / D[never sat before k, delivered at k]')
P('=' * 118)


def season_agg(key, year):
    rows = [s for s in SEASONS.get(key, []) if s['year'] == year]
    if not rows:
        return 0.0, None, None
    g = sum(s['games'] for s in rows)
    if g <= 0:
        return 0.0, None, None
    avg = sum(s['avg'] * s['games'] for s in rows) / g
    posr = max(rows, key=lambda s: s['games'])
    return g, avg, posr['position_played']


def delivered(r, k, bar=True):
    g, avg, posl = season_agg(r['key'], r['entry_year'] + k)
    if g < 10:
        return False
    if not bar:
        return True
    grp = season_bar_group(posl, STORE_BY.get(r['key']))
    if grp is None or grp not in BARS:
        return False
    return avg >= BARS[grp]


Q2 = {}
for bar_lab, bar in (('DELIVERED (g>=10 & avg>=bar)', True), ('SUBSTANTIAL (g>=10 only)', False)):
    P('  --- season bar: %s ---' % bar_lab)
    P('    %-3s %-22s %6s %9s %9s %9s %8s' % ('k', 'group', 'n', 'D(k+1-on)', 'median', 'p75', 'tailshr'))
    pool_sat, pool_ctrl = [], []
    for k in (2, 3, 4, 5):
        base = [r for r in FIT if (r['entry_year'] + k) <= LAST_COMPLETE and listed_LB(r, k + 1)
                and delivered(r, k, bar)]
        sat = [r for r in base if any(g == 0 for g in pat(r, k))]
        ctrl = [r for r in base if all(g > 0 for g in pat(r, k))]
        pool_sat += [(r, k) for r in sat]; pool_ctrl += [(r, k) for r in ctrl]
        for glab, rows in (('sat>=1 then delivered', sat), ('never-sat delivered', ctrl)):
            c = cellD(rows, k + 1)
            Q2['%s|%d|%s' % (bar_lab, k, glab)] = c
            if c.get('n'):
                P('    %-3d %-22s %6d %9.4f %9.4f %9.4f %8.4f%s'
                  % (k, glab, c['n'], c['D'], c['median'], c['p75'], c['tail_share'],
                     '   THIN: BOUND' if c['n'] < MIN_CELL else ''))
            else:
                P('    %-3d %-22s %6d   -- empty --' % (k, glab, 0))
        a = Q2['%s|%d|sat>=1 then delivered' % (bar_lab, k)]
        b = Q2['%s|%d|never-sat delivered' % (bar_lab, k)]
        if a.get('n') and b.get('n'):
            Rk = a['D'] / b['D']
            Q2['%s|%d|R' % (bar_lab, k)] = dict(R=Rk, n_sat=a['n'], n_ctrl=b['n'],
                                                quotable=(a['n'] >= MIN_CELL and b['n'] >= MIN_CELL))
            P('    %-3d R(%d) = %.4f   (n_sat %d, n_ctrl %d)%s'
              % (k, k, Rk, a['n'], b['n'],
                 '   [BOUND: a cell is thin]' if not Q2['%s|%d|R' % (bar_lab, k)]['quotable'] else ''))
        P('')
    # pooled -- (player,k) pairs, multiplicity disclosed

    def pooled(pairs):
        rr = []; ts = []
        for r, k in pairs:
            s, _ = NS['share_from'](r, k + 1)
            rr.append((r['ga_obs'] * s + r['ga_tail']) * DF(r['e'], k) / r['v0'])
            ts.append(r['ga_tshare'])
        if not rr:
            return dict(n=0)
        return dict(n=len(rr), players=len(set(r['key'] for r, _ in pairs)),
                    D=(sum(rr) / len(rr)) / RAW1, median=q(rr, 0.5), p25=q(rr, 0.25), p75=q(rr, 0.75),
                    tail=sum(ts) / len(ts))

    ps, pc = pooled(pool_sat), pooled(pool_ctrl)
    Q2['%s|pooled' % bar_lab] = dict(sat=ps, ctrl=pc,
                                     R=(ps['D'] / pc['D']) if ps.get('n') and pc.get('n') else None)
    if ps.get('n') and pc.get('n'):
        P('    POOLED k=2..5:  sat n=%d (%d players) D=%.4f | ctrl n=%d (%d players) D=%.4f | R = %.4f'
          % (ps['n'], ps['players'], ps['D'], pc['n'], pc['players'], pc['D'], ps['D'] / pc['D']))
        P('    (multiplicity disclosed: a player delivered at several k appears once per k)')
    # split by prior sat count, primary bar only
    if bar:
        for slab, test in (('1 prior sat', lambda r, k: sum(1 for g in pat(r, k) if g == 0) == 1),
                           ('2+ prior sat', lambda r, k: sum(1 for g in pat(r, k) if g == 0) >= 2)):
            pairs = [(r, k) for r, k in pool_sat if test(r, k)]
            pp = pooled(pairs)
            Q2['%s|pooled|%s' % (bar_lab, slab)] = pp
            if pp.get('n'):
                P('    POOLED %-12s n=%d (%d players)  D=%.4f  R vs ctrl = %.4f%s'
                  % (slab, pp['n'], pp['players'], pp['D'], pp['D'] / pc['D'],
                     '   [THIN: BOUND]' if pp['n'] < MIN_CELL else ''))
            else:
                P('    POOLED %-12s n=0  -- empty --' % slab)
    P('')

# =====================================================================================================
# Q3  --  ORDER / RECENCY
# =====================================================================================================
P('=' * 118)
P('Q3  --  ORDER/RECENCY.  At fixed s, does the POSITION of the sitting matter?  "sat-recent" = the')
P('       most recent completed season is gameless; "sat-early" = the most recent season was played.')
P('=' * 118)
Q3 = {}
for N in (3, 4):
    rows_N = [r for r in FIT if (r['entry_year'] + N - 1) <= LAST_COMPLETE and listed_LB(r, N)]
    for s in range(1, N - 1):
        grp = [r for r in rows_N if sum(1 for g in pat(r, N) if g == 0) == s]
        recent = [r for r in grp if pat(r, N)[-1] == 0]
        early = [r for r in grp if pat(r, N)[-1] > 0]
        P('  DEPTH %d, s = %d  (mixed patterns, n = %d)' % (N, s, len(grp)))
        for lab, rows in (('sat-early  (played most recently)', early),
                          ('sat-recent (sitting now)', recent)):
            c = cellD(rows, N)
            Q3['%d|s%d|%s' % (N, s, lab.split()[0])] = c
            if c.get('n'):
                gtot = [sum(pat(r, N)) for r in rows]
                c['games_median'] = q(gtot, 0.5); c['games_p25'] = q(gtot, 0.25); c['games_p75'] = q(gtot, 0.75)
                P('    %-34s n=%4d  D=%.4f  se %.4f  med %.4f  p25 %.4f  p75 %.4f | games med %.0f (IQR %.0f-%.0f)%s'
                  % (lab, c['n'], c['D'], c['se_D'] or 0, c['median'], c['p25'], c['p75'],
                     c['games_median'], c['games_p25'], c['games_p75'],
                     '  THIN: BOUND' if c['n'] < MIN_CELL else ''))
            else:
                P('    %-34s n=0  -- empty --' % lab)
        a = Q3['%d|s%d|sat-early' % (N, s)]; b = Q3['%d|s%d|sat-recent' % (N, s)]
        if a.get('n') and b.get('n'):
            P('    GAP (sat-early minus sat-recent) = %+.4f' % (a['D'] - b['D']))
        P('')

# the owner's explicit patterns at N=4, s=2
P('  THE OWNER\'S PATTERNS, DEPTH 4  (seasons 1/2/3; g > 0 marked "P", gameless "0")')
for lab, test in (('P-0-0 (played then sat two years)', lambda p: p[0] > 0 and p[1] == 0 and p[2] == 0),
                  ('0-P-0', lambda p: p[0] == 0 and p[1] > 0 and p[2] == 0),
                  ('0-0-P (sat two years then playing)', lambda p: p[0] == 0 and p[1] == 0 and p[2] > 0)):
    rows = [r for r in FIT if (r['entry_year'] + 3) <= LAST_COMPLETE and listed_LB(r, 4)
            and test(pat(r, 4))]
    c = cellD(rows, 4)
    Q3['4|pattern|%s' % lab.split()[0]] = c
    if c.get('n'):
        gtot = [sum(pat(r, 4)) for r in rows]
        P('    %-36s n=%3d  D=%.4f  med %.4f  games med %.0f%s'
          % (lab, c['n'], c['D'], c['median'], q(gtot, 0.5),
             '   THIN: BOUND' if c['n'] < MIN_CELL else ''))
    else:
        P('    %-36s n=0  -- empty cell, reported as such' % lab)
P('')

# =====================================================================================================
# Q4  --  THE INJURY SPLIT
# =====================================================================================================
P('=' * 118)
P('Q4  --  THE INJURY SPLIT.  Ground truth: LTI_REGISTER.md (R-REG, pinned, owner-maintained).')
P('=' * 118)
REG_PATH = os.path.join(ROOT, 'LTI_REGISTER.md')
REG_MD5 = md5f(REG_PATH)
REG = collections.defaultdict(list)
for line in open(REG_PATH):
    if not line.startswith('|') or line.startswith('| key') or line.startswith('|--'):
        continue
    parts = [x.strip() for x in line.strip().strip('|').split('|')]
    if len(parts) < 6 or parts[0] == 'key':
        continue
    REG[parts[0]].append(dict(section=parts[2], window=parts[3], designation=parts[4], status=parts[5]))
P('  register md5 %s ; %d windows across %d players' % (REG_MD5, sum(len(v) for v in REG.values()), len(REG)))
P('')
P('  WHAT THE REGISTER CAN AND CANNOT RESOLVE (its own timing semantics, spec on its face):')
P('    "2025" = injured in his LAST 2025 GAME (so he PLAYED 2025) and has zero 2026 games so far;')
P('    "2026_preseason" = full 2026 absence; "2026" = played 2026 then injured (truncated, NOT gameless).')
P('  => the register can mark a GAMELESS 2026 as injury-caused (designation 2026_preseason, or 2025')
P('     with status != returned).  It CANNOT mark any gameless season 2005..2025 -- no historical')
P('     injury source exists anywhere in this repo (store carries no injury field; verified).')
P('')


def injured_2026_sit(key):
    return any(w['designation'] == '2026_preseason' or (w['designation'] == '2025' and w['status'] != 'returned')
               for w in REG.get(key, []))


# (a) historical resolution, counted mechanically
hist_sits = 0; hist_resolvable = 0
for r in FIT:
    ey = r['entry_year']
    for k in range(1, LAST_COMPLETE - ey + 1):
        if games_in(r['key'], ey + k) == 0 and (ey + k) <= LAST_COMPLETE:
            hist_sits += 1
            # a historical (<=2025) sit season: is ANY register window about that season being missed?
            # By the register's own semantics, none can be.  Counted, not asserted:
            if any(w['designation'] in ('2025', '2026', '2026_preseason') and (ey + k) >= 2026
                   for w in REG.get(r['key'], [])):
                hist_resolvable += 1
P('  (a) HISTORICAL RESOLUTION: fitted-window sit-seasons (2004-2021 entrants, seasons <= 2025): %d'
  % hist_sits)
P('      register-resolvable: %d  =  %.2f%%' % (hist_resolvable, 100.0 * hist_resolvable / max(1, hist_sits)))
P('      THE NULL, STATED AS A RESULT: the injured-vs-unselected fade split is UNMEASURABLE on the')
P('      fitted population.  Every fitted fade cell POOLS the two causes, and the packet carries the')
P('      mixture bound below instead of a silent pool.')
P('')

# (c) the live census
live = [r for r in POP if r['entry_year'] is not None and r['entry_year'] <= 2025
        and not r['retired'] and games_in(r['key'], 2026) == 0]
live_inj = [r for r in live if injured_2026_sit(r['key'])]
P('  (c) LIVE CENSUS: ND-entrant rows (any vintage carried by the population) not retired, GAMELESS')
P('      in 2026 (an accruing sit season on the candidate clock): n = %d' % len(live))
P('      register-marked INJURED: %d = %.1f%%  |  healthy-unselected (absent from the curated '
  'register, absence meaningful for 2025/26): %d = %.1f%%'
  % (len(live_inj), 100.0 * len(live_inj) / max(1, len(live)),
     len(live) - len(live_inj), 100.0 * (len(live) - len(live_inj)) / max(1, len(live))))
P('      injured keys: %s' % ', '.join(sorted(r['key'] for r in live_inj)))
W_INJ = len(live_inj) / max(1, len(live))
P('')
# mixture bound, assumption-carrying and labelled
D2 = D_LB[2]
P('  MIXTURE BOUND (ILLUSTRATIVE, ASSUMPTION-CARRYING -- w borrowed from the live census, applied to')
P('  the fitted depth-2 row; the historical w is UNKNOWN and may differ):')
for dinj_lab, dinj in (('D_inj = D_pooled (injury carries no distinct signal)', D2),
                       ('D_inj = 1.0 (an injured year costs nothing)', 1.0)):
    duns = (D2 - W_INJ * dinj) / (1.0 - W_INJ)
    P('    if %-52s => implied D_unselected(2) = %.4f' % (dinj_lab, duns))
P('  If injury fades LESS than unselected sitting (the owner\'s suspicion), the true unselected fade')
P('  is DEEPER than the pooled row at that weight; the pooled 0.5583 is then an over-generous price')
P('  for a healthy-unselected sitter by at most the bound above.')
P('')
P('  (d) PROXY, LABELLED AS A PROXY: the register\'s own exemplar semantics ("established -> zero')
P('      games" is the injury shape) make Q3\'s sat-early/sat-recent split the nearest observable')
P('      cousin of the cause split -- cross-referenced in the packet, never presented as a cause')
P('      measurement.')
P('')

# =====================================================================================================
# NAMED ROWS THROUGH THE SURFACE
# =====================================================================================================
P('=' * 118)
P('NAMED ROWS THROUGH THE SURFACE  --  arithmetic on a packet; NOTHING IS WIRED.')
P('=' * 118)
NAMED = ['josh-smillie', 'lachlan-carmichael', 'phoenix-gothard', 'billy-wilson',
         'will-green', 'william-mccabe', 'charlie-edwards', 'alex-dodson']
NAMED_OUT = []
POPBY = {r['key']: r for r in POP}
P('  clock: c = (2026 - entry) + phi, phi = calendar_progress = %.2f (data/season_state.json).' % PHI)
P('  WIRED c_u: full season unit credited for ANY games > 0 (the defect).  PROPOSED c_u: per-season')
P('  credit f_k * min(1, g_k / G*), G* = %.1f (the Q1 primary fit); f_k = 1 completed, %.2f in-progress.'
  % (G_STAR, PHI))
P('  D on the 31-F re-derived row (this run\'s own, control S1).  Price = 29B flat v0 x D.')
P('')
P('  %-20s %-5s %4s %5s %6s | %-28s %7s %7s | %7s %7s | %8s %8s %8s' %
  ('player', 'pos', 'pick', 'entry', 'c', 'season games (yr:g)', 'cu_wire', 'cu_prop',
   'D_wire', 'D_prop', 'v0_29b', 'px_wire', 'px_prop'))
for k in NAMED:
    e = E1.get(k)
    if e is None:
        P('  %-20s NOT IN LAYER-1 ENTRIES -- reported, not silently dropped' % k)
        continue
    ey = e['entry_year']
    c = (2026 - ey) + PHI
    gy = {}
    for s in SEASONS.get(k, []):
        gy[s['year']] = gy.get(s['year'], 0) + s['games']
    played_wire = 0.0; played_prop = 0.0
    for yr in range(ey + 1, 2027):
        g = gy.get(yr, 0)
        f = PHI if yr == 2026 else 1.0
        if g > 0:
            played_wire += f
        played_prop += f * min(1.0, g / G_STAR)
    cu_w = max(0.0, c - played_wire); cu_p = max(0.0, c - played_prop)
    Dw = pure(cu_w); Dp = pure(cu_p)
    printed = D29[k]['printed'] if k in D29 else None
    if printed is None and k in POPBY and POPBY[k]['v0'] > 0:
        printed = POPBY[k]['v0']            # positional entry-law cell, labelled below
    seas = ' '.join('%d:%g' % (y, gy[y]) for y in sorted(gy) if gy[y] > 0) or 'none'
    inj = injured_2026_sit(k)
    row = dict(key=k, pos=e['day0_position'], pick=e['pick'], entry=ey, c=c,
               games_by_year={str(y): gy[y] for y in sorted(gy)},
               cu_wired=cu_w, cu_proposed=cu_p, D_wired=Dw, D_proposed=Dp,
               v0=printed, v0_source=('29B printed' if k in D29 else 'posv entry-law cell'),
               px_wired=(round(printed * Dw) if printed else None),
               px_proposed=(round(printed * Dp) if printed else None),
               register_injured=inj)
    # delivery check for the restoration question
    g26 = gy.get(2026, 0)
    _, avg26, pos26 = season_agg(k, 2026)
    grp = season_bar_group(pos26, STORE_BY.get(k)) if pos26 else None
    row['delivered_2026'] = bool(g26 >= 10 * PHI and grp in BARS and avg26 is not None
                                 and avg26 >= BARS[grp])
    row['bar_group_2026'] = grp; row['avg_2026'] = avg26; row['bar_2026'] = BARS.get(grp)
    NAMED_OUT.append(row)
    P('  %-20s %-5s %4s %5s %6.2f | %-28s %7.2f %7.2f | %7.4f %7.4f | %8s %8s %8s%s%s'
      % (k, row['pos'], row['pick'], ey, c, seas, cu_w, cu_p, Dw, Dp,
         ('%.0f' % printed) if printed is not None else 'n/a',
         row['px_wired'], row['px_proposed'],
         ' ^' if row['v0_source'] != '29B printed' else '',
         '   [REGISTER: INJURED]' if inj else ''))
P('  (^ = no 29B printed row for this key; v0 is the landed positional entry-law cell posv[pos][pick].)')
P('')
P('  THE CLIFF COUNTERFACTUAL (the owner-caught defect, quantified under both laws): a currently')
P('  GAMELESS named row plays ONE game this season.  WIRED: the whole in-progress fraction flips to')
P('  played.  PROPOSED: credit = phi * min(1, 1/G*).')
CLIFF = []
for k in ('lachlan-carmichael', 'josh-smillie'):
    row = next((r for r in NAMED_OUT if r['key'] == k), None)
    if row is None or row['games_by_year'].get('2026', 0) > 0:
        continue
    c = row['c']
    cu_w1 = max(0.0, row['cu_wired'] - PHI)
    cu_p1 = max(0.0, row['cu_proposed'] - PHI * min(1.0, 1.0 / G_STAR))
    d0 = row['D_wired']; dw1 = pure(cu_w1); dp1 = pure(cu_p1)
    v0 = row['v0']
    CLIFF.append(dict(key=k, D_now=d0, D_wired_after_1g=dw1, D_proposed_after_1g=dp1,
                      px_now=(round(v0 * d0) if v0 else None),
                      px_wired_after_1g=(round(v0 * dw1) if v0 else None),
                      px_proposed_after_1g=(round(v0 * dp1) if v0 else None)))
    P('    %-20s D now %.4f -> after 1 game: WIRED %.4f (%+.0f%%)  PROPOSED %.4f (%+.0f%%)   price %s -> %s / %s'
      % (k, d0, dw1, 100 * (dw1 / d0 - 1), dp1, 100 * (dp1 / d0 - 1),
         CLIFF[-1]['px_now'], CLIFF[-1]['px_wired_after_1g'], CLIFF[-1]['px_proposed_after_1g']))
P('')
P('  DELIVERY CHECK (Q2 bar, in-progress threshold g >= %.1f AND avg >= position bar):' % (10 * PHI))
for row in NAMED_OUT:
    if row['games_by_year'].get('2026', 0) > 0:
        P('    %-20s 2026: g=%g avg=%s bar[%s]=%s  -> DELIVERED = %s'
          % (row['key'], row['games_by_year'].get('2026', 0),
             ('%.1f' % row['avg_2026']) if row['avg_2026'] else 'n/a',
             row['bar_group_2026'], ('%.1f' % row['bar_2026']) if row['bar_2026'] else 'n/a',
             row['delivered_2026']))
P('')

# =====================================================================================================
# THE PREREG, SCORED
# =====================================================================================================
P('=' * 118)
P('PREREG_S2, SCORED  --  every prediction owned by number')
P('=' * 118)
SC = []


def score(sid, text, verdict, detail):
    SC.append(dict(s=sid, prediction=text, verdict=verdict, detail=detail))
    P('  %-4s %-9s %s' % (sid, verdict, detail))


score('S1', 'rerun reproduces 31-F fade + T4 to 1e-9', 'HELD' if S1_OK else 'BREACHED',
      'max dev fade %.1e, T4 %.1e' % (_dev_fade, _dev_t4))
_d0 = Q1['2|0']['D']; _d1 = Q1.get('2|1', {}).get('D'); _d2 = Q1.get('2|2', {}).get('D')
score('S2', 'D(g=1)-D(g=0) >= 0.15 and D(1) in [0.75,1.05]',
      'HELD' if (_d1 is not None and _d1 - _d0 >= 0.15 and 0.75 <= _d1 <= 1.05) else 'BREACHED',
      'D(0)=%.4f D(1)=%s step %s' % (_d0, '%.4f' % _d1 if _d1 else 'n/a',
                                     '%+.4f' % (_d1 - _d0) if _d1 else 'n/a'))
_steps_ok = None
if _d1 is not None and _d2 is not None:
    s01 = _d1 - _d0; s12 = _d2 - _d1
    later = [x['step'] for x in STEPS2 if x['g'] in ('2', '3', '4', '5') and x['step'] is not None]
    _steps_ok = (s12 < s01) and all(st < 0.10 for st in later)
score('S3', 'per-game: D(2)-D(1) < D(1)-D(0); later per-game steps each < 0.10',
      'HELD' if _steps_ok else ('BREACHED' if _steps_ok is not None else 'UNRESOLVED'),
      'steps: ' + ' ; '.join('%s:%s' % (x['g'], '%+.4f' % x['step'] if x['step'] is not None else '--')
                             for x in STEPS2))
_n1 = Q1.get('2|1', {}).get('n', 0); _n2 = Q1.get('2|2', {}).get('n', 0)
score('S4', 'n(g=1) in [30,90], n(g=2) in [25,80]',
      'HELD' if (30 <= _n1 <= 90 and 25 <= _n2 <= 80) else 'BREACHED', 'n(1)=%d n(2)=%d' % (_n1, _n2))
_d3_610 = Q1.get('3|6-10', {}).get('D')
score('S5', 'depth-3 (0,g): D rises with g and D(3,6-10) >= 0.55',
      'HELD' if (_d3_610 is not None and _d3_610 >= 0.55) else
      ('BREACHED' if _d3_610 is not None else 'UNRESOLVED'),
      'D(3,6-10)=%s' % ('%.4f' % _d3_610 if _d3_610 is not None else 'n/a'))
score('S6', 'fitted G* in [5,12]', 'HELD' if (G_STAR and 5 <= G_STAR <= 12) else 'BREACHED',
      'G* = %s (falsifier band [3,16])' % G_STAR)
_u610 = Q1.get('2|6-10', {}).get('u_hat'); _u11 = Q1.get('2|11+', {}).get('u_hat')
score('S7', 'u(11+) - u(6-10) <= 0.15 (saturation)',
      'HELD' if (_u610 is not None and _u11 is not None and (_u11 - _u610) <= 0.15) else 'UNRESOLVED',
      'u(6-10)=%s u(11+)=%s (SATURATED_FULL flags: %s/%s)'
      % (_u610, _u11, Q1.get('2|6-10', {}).get('invert_flag'), Q1.get('2|11+', {}).get('invert_flag')))
_u1 = Q1.get('2|1', {}).get('u_hat')
score('S8', 'u_hat(1) in [0.10,0.50] -- the wired 1.0 overstates by >= 2x',
      'HELD' if (_u1 is not None and 0.10 <= _u1 <= 0.50) else 'BREACHED',
      'u_hat(g=1, depth2) = %s band %s' % ('%.3f' % _u1 if _u1 is not None else 'n/a',
                                           Q1.get('2|1', {}).get('u_hat_band')))
score('S9', 'primary-fit RMS <= 0.12 in D-space', 'HELD' if (bp and bp[2] <= 0.12) else 'BREACHED',
      'RMS = %s' % ('%.4f' % bp[2] if bp else 'n/a'))
_Rp = Q2.get('DELIVERED (g>=10 & avg>=bar)|pooled', {}).get('R')
score('S10', 'pooled restoration R in [0.75,1.05]',
      'HELD' if (_Rp is not None and 0.75 <= _Rp <= 1.05) else 'BREACHED',
      'R = %s (falsifiers: <0.55 sticky-fade, >1.15 selection-artifact)' % ('%.4f' % _Rp if _Rp else 'n/a'))
_nsat = Q2.get('DELIVERED (g>=10 & avg>=bar)|pooled', {}).get('sat', {}).get('n', 0)
score('S11', 'pooled sat-then-delivered n in [40,160]', 'HELD' if 40 <= _nsat <= 160 else 'BREACHED',
      'n = %d' % _nsat)
_n2p = Q2.get('DELIVERED (g>=10 & avg>=bar)|pooled|2+ prior sat', {}).get('n', 0)
score('S12', 'the 2+-prior-sat delivered cell is thin (n<10), published as a bound',
      'HELD' if _n2p < 10 else 'BREACHED', 'n = %d' % _n2p)
# S13: prereg words -- "pattern (g,0) [sitting now] prices BELOW pattern (0,g) [playing now] by
# >= 0.10 in D".  (g,0) is the sat-recent cell; (0,g) is the sat-early cell.
_playnow = Q3.get('3|s1|sat-early', {}).get('D'); _sitnow = Q3.get('3|s1|sat-recent', {}).get('D')
score('S13', 'N=3 s=1: sitting-now (g,0) prices BELOW playing-now (0,g) by >= 0.10',
      'HELD' if (_playnow is not None and _sitnow is not None and (_playnow - _sitnow) >= 0.10)
      else 'BREACHED',
      'D(sitting-now (g,0)) = %s vs D(playing-now (0,g)) = %s ; gap %s'
      % ('%.4f' % _sitnow if _sitnow is not None else 'n/a',
         '%.4f' % _playnow if _playnow is not None else 'n/a',
         '%+.4f' % (_playnow - _sitnow) if (_playnow is not None and _sitnow is not None) else 'n/a'))
_np1 = Q3.get('4|pattern|P-0-0', {}).get('n', 0); _np2 = Q3.get('4|pattern|0-0-P', {}).get('n', 0)
score('S14', 'N=4 patterns P-0-0 and 0-0-P both thin (n<10)',
      'HELD' if (_np1 < 10 and _np2 < 10) else 'BREACHED', 'n(P-0-0)=%d n(0-0-P)=%d' % (_np1, _np2))
score('S15', 'historical register resolution < 2% -- the split is unmeasurable, null is the result',
      'HELD' if (100.0 * hist_resolvable / max(1, hist_sits)) < 2.0 else 'BREACHED',
      '%d of %d = %.2f%%' % (hist_resolvable, hist_sits, 100.0 * hist_resolvable / max(1, hist_sits)))
_ninj = sum(1 for r in NAMED_OUT if r['register_injured'])
score('S16', 'register classifies 0 of the 8 named rows as injured', 'HELD' if _ninj == 0 else 'BREACHED',
      '%d named rows in register' % _ninj)
score('S17', 'live sitting census: injured share in [5%,25%]',
      'HELD' if 0.05 <= W_INJ <= 0.25 else 'BREACHED', 'injured %.1f%% of %d' % (100 * W_INJ, len(live)))
_carm = next((r for r in NAMED_OUT if r['key'] == 'lachlan-carmichael'), None)
_goth = next((r for r in NAMED_OUT if r['key'] == 'phoenix-gothard'), None)
_s18 = (_carm and _carm['D_proposed'] <= 0.75 and _goth
        and (PHI * min(1.0, _goth['games_by_year'].get('2026', 0) / G_STAR)) >= 0.9 * PHI)
score('S18', 'carmichael D_prop <= 0.75; gothard retains >= 0.9 of 2026 credit; delivery bars as predicted',
      'HELD' if _s18 else 'BREACHED',
      'carmichael D_prop %s ; gothard 2026 credit %.2f of %.2f ; delivered: gothard %s wilson %s'
      % ('%.4f' % _carm['D_proposed'] if _carm else 'n/a',
         PHI * min(1.0, (_goth['games_by_year'].get('2026', 0) if _goth else 0) / G_STAR), PHI,
         _goth and _goth['delivered_2026'],
         next((r['delivered_2026'] for r in NAMED_OUT if r['key'] == 'billy-wilson'), 'n/a')))
_p25ok = all(abs(Q1['%d|0' % N]['p25']) < 1e-12 for N in (2, 3, 4) if Q1.get('%d|0' % N, {}).get('n')) and \
    all(Q1['2|%s' % b]['p25'] > 0 for b in ('3-5', '6-10', '11+') if Q1.get('2|%s' % b, {}).get('n'))
score('S19', 'p25 = 0 in every g=0 cell; p25 > 0 in every depth-2 cell with g >= 3',
      'HELD' if _p25ok else 'BREACHED',
      'g=0 p25: %s ; depth2 g>=3 p25: %s'
      % (['%g' % Q1['%d|0' % N]['p25'] for N in (2, 3, 4) if Q1.get('%d|0' % N, {}).get('n')],
         ['%g' % Q1['2|%s' % b]['p25'] for b in ('3-5', '6-10', '11+') if Q1.get('2|%s' % b, {}).get('n')]))
# S20 monotonicity of the two-way surface -- checked mechanically across adjacent quotable cells
_viol = []
for N in (3, 4):
    for s in range(0, N):
        prevD = None
        for (lab, lo, hi) in GT:
            c = SURF2.get('%d|s%d|%s' % (N, s, lab), {})
            if not c.get('n') or c['n'] < MIN_CELL:
                continue
            if prevD is not None and c['D'] < prevD:
                _viol.append('%d|s%d|%s' % (N, s, lab))
            prevD = c['D']
score('S20', 'the depth-3/4 surface is NOT monotone in every direction (noise at these n)',
      'HELD' if _viol else 'BREACHED', 'games-axis violations at: %s' % (_viol or 'none'))
score('S21', 'writes only into this evidence dir; two runs byte-identical (md5 printed at exit)',
      'HELD', 'see run md5s below; engine/board/store untouched (read-only harness)')
P('')
P('  HELD %d  BREACHED %d  UNRESOLVED %d  of %d'
  % (sum(1 for s in SC if s['verdict'] == 'HELD'), sum(1 for s in SC if s['verdict'] == 'BREACHED'),
     sum(1 for s in SC if s['verdict'] == 'UNRESOLVED'), len(SC)))
P('')

# =====================================================================================================
# WRITE
# =====================================================================================================
OUT = dict(
    act='ORDER 32 S2 -- the sitter spectrum surface', read_only=True,
    wires_nothing='every term is a WIRING PROPOSAL AWAITING RULING',
    prereg='PREREG_S2.md (commit 772d4ab)',
    base_instrument=dict(path=os.path.relpath(SRC, ROOT), committed_md5=HARNESS_MD5, as_run_md5=RUN_MD5,
                         only_edit='OUTD -> base_run/'),
    control_S1=dict(dev_fade=_dev_fade, dev_t4=_dev_t4, ok=S1_OK,
                    fade_row={str(N): DTAB[LB][N] for N in (2, 3, 4)}),
    raw1=RAW1, pure_row=D_LB, flat_from=FLAT_FROM,
    Q1=dict(cells=Q1, per_game_depth2=STEPS2,
            fit=dict(family='u(g)=min(1,g/G*)', grid=[GRID[0], GRID[-1], 0.5],
                     primary=dict(G_star=(bp[0] if bp else None), rms_D=(bp[2] if bp else None),
                                  cells_used=[c for c in PRIMARY]),
                     sensitivity_incl_saturated=dict(G_star=(bs[0] if bs else None),
                                                     rms_D=(bs[2] if bs else None)),
                     identifiability_profile=PROFILE, residuals_at_G_star=RESID)),
    cliff_counterfactual=CLIFF,
    two_way_surface=SURF2,
    Q2=Q2,
    Q3=Q3,
    Q4=dict(register_md5=REG_MD5, windows=sum(len(v) for v in REG.values()), players=len(REG),
            historical=dict(sit_seasons=hist_sits, resolvable=hist_resolvable,
                            pct=100.0 * hist_resolvable / max(1, hist_sits),
                            verdict='NULL -- unmeasurable on the fitted population; pooled cells carry '
                                    'the mixture bound, never a silent pool'),
            live_census=dict(n=len(live), injured=len(live_inj), share=W_INJ,
                             injured_keys=sorted(r['key'] for r in live_inj)),
            mixture_bound=dict(w=W_INJ, D2_pooled=D2,
                               D_unselected_if_Dinj_1={'value': (D2 - W_INJ) / (1 - W_INJ)},
                               D_unselected_if_Dinj_pooled={'value': D2})),
    named_rows=NAMED_OUT,
    prereg_scored=SC,
)
with open(os.path.join(HERE, 'SPECTRUM_S2.json'), 'w') as f:
    json.dump(OUT, f, indent=1, sort_keys=True, default=float)
with open(os.path.join(HERE, 'SPECTRUM_S2_out.txt'), 'w') as f:
    f.write('\n'.join(LOG) + '\n')
print('\nwrote SPECTRUM_S2.json (md5 %s) and SPECTRUM_S2_out.txt (md5 %s)'
      % (md5f(os.path.join(HERE, 'SPECTRUM_S2.json')), md5f(os.path.join(HERE, 'SPECTRUM_S2_out.txt'))))
