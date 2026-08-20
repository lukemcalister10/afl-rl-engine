#!/usr/bin/env python3
"""ORDER 30B-R -- T1 (THE READING, RESOLVED BY DEFINITION) and T4 (THE OBJECT).

T1 asks a DEFINITIONAL question: given how sigma was CONSTRUCTED in the 30B-M harness, which wiring
faithfully reproduces the measured relationship -- the WEIGHT form or the VALUE form?  The answer is
read off `o30bm_measure.py::band_fit` and the algebra is shown, then the three candidate wirings are
priced on the named rows and on the whole blended book so the packet shows what the resolution costs.

T4 quantifies the two candidate pedigree OBJECTS -- the Step-1 positional v0 (wired in the preview)
against `entry_anchor` (the 26A-era object the retired machinery leaned on) -- on the named rows and
the whole book.

READ-ONLY.  The engine is staged under the scratchpad and loaded for `entry_anchor` only.  Nothing
outside this lane and the scratchpad is written.

  usage:  python3 o30br_reading.py     (writes READING.json + READING_out.txt)
"""
import os, sys, io, json, math, hashlib, shutil, contextlib, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng30br_read/rl_after'

MOVP = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'preview', 'PREVIEW_MOVERS.json')
PERSP = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'PERSISTENCE_TABLE.json')
MEASP = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'o30bm_measure.py')

OUT_JSON = os.path.join(HERE, 'READING.json')
OUT_TXT = os.path.join(HERE, 'READING_out.txt')

_LOG = []
def P(s=''):
    print(s)
    _LOG.append(str(s))

def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def disp(xs):
    xs = sorted(float(x) for x in xs)
    if not xs:
        return {}
    n = len(xs)
    def q(f):
        if n == 1:
            return xs[0]
        i = f * (n - 1)
        lo = int(math.floor(i)); hi = min(n - 1, lo + 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)
    return dict(n=n, mean=sum(xs) / n, p10=q(.10), p25=q(.25), median=q(.50), p75=q(.75), p90=q(.90),
                min=xs[0], max=xs[-1],
                sd=(statistics.pstdev(xs) if n > 1 else 0.0))

# ==================================================================================================
# SOURCES -- pinned
# ==================================================================================================
PINS = dict(preview_movers=md5(MOVP), persistence_table=md5(PERSP), o30bm_measure=md5(MEASP),
            merged_recover=md5(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py')),
            store=md5(os.path.join(ROOT, 'engine/rl_after/rl_model_data.json')))
MOV = json.load(open(MOVP))
PERS = json.load(open(PERSP))
BF = PERS['q1_persistence']['band_fits']
ROWS = MOV['rows']

GAMES_BANDS = [('0-5', 0, 5), ('6-15', 6, 15), ('16-35', 16, 35), ('36-70', 36, 70), ('71+', 71, 10 ** 6)]
MIDS = {nm: (lo + min(hi, 100)) / 2.0 for nm, lo, hi in GAMES_BANDS}

P('=' * 100)
P('ORDER 30B-R -- T1 THE READING (definitional) + T4 THE OBJECT')
P('=' * 100)
P('pins: ' + json.dumps(PINS, sort_keys=True))
P('')

# ==================================================================================================
# T1.1 -- HOW SIGMA WAS CONSTRUCTED, READ OFF THE HARNESS
# ==================================================================================================
P('=' * 100)
P('T1.1 -- SIGMA AS CONSTRUCTED IN o30bm_measure.py::band_fit')
P('=' * 100)
src = open(MEASP).read().splitlines()
for i, ln in enumerate(src, 1):
    if 'sig = b[i] * mv0 / mR' in ln or 'pedigree share sigma = beta*mean(v0)/mean(R)' in ln:
        P('  line %d: %s' % (i, ln.strip()))
P('')
P('  The fitted equation, band b:   R_i = c + gamma\'Z_i + beta_b * v0_i + eps_i')
P('  where Z = [pos dummies, age, age^2, o, o^2, cur, cur3, games_at_Y, log1p(g)].')
P('  Band means:                    Rbar = (c + gamma\'Zbar) + beta_b * v0bar   ==   Pibar + beta_b*v0bar')
P('  Definition of sigma:           sigma_b := beta_b * v0bar / Rbar            ==   (pedigree contribution)/(total)')
P('  Complement, therefore:         1 - sigma_b == Pibar / Rbar                 ==   (production contribution)/(total)')
P('')
P('  READ THAT AGAIN: sigma is a ratio of CONTRIBUTIONS TO THE LEVEL OF THE OUTCOME.')
P('  It is a VALUE share by construction.  It is not, and was never fitted as, a mixing weight.')
P('')

rat = []
P('%-8s %6s %10s %12s %12s %10s %10s' % ('band', 'n', 'beta_v0', 'mean v0', 'mean R', 'v0bar/Rbar', 'sigma'))
for nm, lo, hi in GAMES_BANDS:
    f = BF[nm]
    r = f['mean_v0'] / f['mean_R']
    rat.append((nm, r))
    P('%-8s %6d %10.5f %12.1f %12.1f %10.3f %10.4f'
      % (nm, f['n'], f['beta_v0'], f['mean_v0'], f['mean_R'], r, f['sigma']))
    # identity check: sigma == beta*v0bar/Rbar to machine precision
    assert abs(f['sigma'] - f['beta_v0'] * f['mean_v0'] / f['mean_R']) < 1e-12
P('')
P('  IDENTITY CHECKED: sigma == beta*mean(v0)/mean(R) to 1e-12 in all five bands.')
P('  mean(v0)/mean(R) > 1 in EVERY band -- the pedigree object is systematically LARGER than the')
P('  outcome it is a share of.  That single fact is what breaks the weight reading.')
P('')

# ==================================================================================================
# T1.2 -- THE THREE CANDIDATE WIRINGS, AND WHAT EACH IMPLIES
# ==================================================================================================
P('=' * 100)
P('T1.2 -- THE THREE WIRINGS, AND THE ALGEBRA THAT SEPARATES THEM')
P('=' * 100)
P('''
  W  WEIGHT form (wired in the 30B-P preview)
        price = (1 - sigma) * P  +  sigma * V
        implied value share  s_W = sigma*V / [(1-sigma)*P + sigma*V]
        s_W == sigma  <=>  V == price.  Never true in general; mean(v0)/mean(R) is 1.07..2.36.
        AND: it multiplies the production block by (1 - sigma).  The regression NEVER shrinks the
        production block -- its coefficient on Z is gamma, estimated free, and the production
        contribution at the band mean is (1-sigma)*Rbar, NOT (1-sigma)*Pbar.

  V  VALUE form (harmonic; not built by the preview)
        solve  (1-w)V / [wP + (1-w)V] = sigma   ->   1/price = (1-sigma)/P + sigma/V
        implied value share  s_V == sigma  EXACTLY, for every row, by construction.
        Reproduces the band-mean identity beta*v0bar = sigma*Rbar exactly.
        But it is harmonic in (P, V); the fit is LINEAR in v0, so this is not the fitted form either.

  A  ADDITIVE form (the regression itself)
        price = P + beta(g) * V
        This IS the fitted equation with the production block at unit weight.
        Band-mean check:  mean(P + beta*V) = Pibar + beta*v0bar = Rbar.  Exact, by construction.
        Requires no v0 == price assumption and imposes no production shrink.
        beta -- not sigma -- is the object band_fit actually ESTIMATED; sigma is derived FROM it.
''')

# beta(g): log-linear interpolation between band midpoints, flat outside -- the same interpolation
# o30bm_measure.py::sigma_at uses for sigma.  LABELLED AS AN INTERPOLATION.
BPTS = sorted((MIDS[nm], BF[nm]['beta_v0']) for nm, _, _ in GAMES_BANDS)
def beta_at(g):
    g = max(1e-6, float(g))
    if g <= BPTS[0][0]:
        return BPTS[0][1]
    if g >= BPTS[-1][0]:
        return BPTS[-1][1]
    for i in range(1, len(BPTS)):
        g0, b0 = BPTS[i - 1]; g1, b1 = BPTS[i]
        if g0 <= g <= g1:
            if b0 <= 0 or b1 <= 0:
                return b0 + (b1 - b0) * (g - g0) / (g1 - g0)
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            return math.exp(math.log(b0) + t * (math.log(b1) - math.log(b0)))
    return BPTS[-1][1]

def price_W(Pp, V, s):
    return (1.0 - s) * Pp + s * V
def price_V(Pp, V, s):
    if Pp <= 0 or V <= 0:
        return 0.0
    return 1.0 / ((1.0 - s) / Pp + s / V)
def price_A(Pp, V, g):
    return Pp + beta_at(g) * V

NAMED = ['isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow',
         'cooper-trembath', 'chris-scerri', 'josh-smillie', 'harry-demattia', 'max-knobel']
BYK = {r['key']: r for r in ROWS}

P('=' * 100)
P('T1.3 -- THE FOUR ROWS T1 NAMES, UNDER ALL THREE WIRINGS')
P('=' * 100)
P('%-18s %5s %8s %9s %9s %8s | %8s %8s %8s | %8s %8s %8s'
  % ('row', 'g', 'sigma', 'prod P', 'v0 V', 'beta(g)', 'W price', 'V price', 'A price',
     's_W', 's_V', 's_A'))
t1rows = {}
for k in ['isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow']:
    r = BYK[k]
    Pp = r['production_pts']; V = r['v0_step1_board']; s = r['sigma']; g = r['games_sigma_axis']
    pw, pv, pa = price_W(Pp, V, s), price_V(Pp, V, s), price_A(Pp, V, g)
    sw = s * V / pw if pw else 0.0
    sv = s
    sa = beta_at(g) * V / pa if pa else 0.0
    t1rows[k] = dict(name=r['name'], games=g, sigma=s, beta=beta_at(g), production=Pp, v0=V,
                     price_weight=pw, price_value=pv, price_additive=pa,
                     vshare_weight=sw, vshare_value=sv, vshare_additive=sa,
                     preview_printed=r['preview'], step2=r['step2'], live=r['live'])
    P('%-18s %5.0f %8.4f %9.1f %9.1f %8.4f | %8.1f %8.1f %8.1f | %8.4f %8.4f %8.4f'
      % (k, g, s, Pp, V, beta_at(g), pw, pv, pa, sw, sv, sa))
P('')
P('  s_W is the WEIGHT wiring\'s implied VALUE share.  s_V == sigma exactly.  s_A is the additive')
P('  form\'s.  The measurement\'s sigma column is the middle one -- read the first against it.')
P('')

# ==================================================================================================
# T1.4 -- THE WHOLE BLENDED BOOK UNDER EACH WIRING
# ==================================================================================================
P('=' * 100)
P('T1.4 -- THE WHOLE BLENDED BOOK: what each wiring totals, and what pedigree share it prints')
P('=' * 100)
BL = [r for r in ROWS if not r['day0']]
P('  blended rows: %d of %d' % (len(BL), len(ROWS)))
agg = {}
for tag in ('W', 'V', 'A'):
    tot = ped = 0.0
    shares = []
    for r in BL:
        Pp = r['production_pts']; V = r['v0_step1_board']; s = r['sigma']; g = r['games_sigma_axis']
        if tag == 'W':
            pr = price_W(Pp, V, s); pd = s * V
        elif tag == 'V':
            pr = price_V(Pp, V, s); pd = s * pr
        else:
            pr = price_A(Pp, V, g); pd = beta_at(g) * V
        tot += pr; ped += pd
        if pr > 0:
            shares.append(pd / pr)
    agg[tag] = dict(total=tot, pedigree_points=ped, book_value_share=(ped / tot if tot else None),
                    row_share=disp(shares))
    P('  %s : total %10.0f   pedigree pts %9.0f   book value share %.4f   median row share %.4f'
      % (tag, tot, ped, ped / tot if tot else float('nan'), agg[tag]['row_share']['median']))
P('')
P('  preview printed total (blended rows only, integers): %d'
  % sum(r['preview'] for r in BL))
P('  Step-2 total (blended rows only):                    %d' % sum(r['step2'] for r in BL))
P('')

# by games class, all three wirings
P('%-8s %6s %12s %12s %12s %10s %10s %10s' %
  ('cg', 'n', 'W total', 'V total', 'A total', 'W share', 'V share', 'A share'))
CG = [('1-5', 1, 5), ('6-15', 6, 15), ('16-35', 16, 35), ('36-70', 36, 70), ('71+', 71, 10 ** 9)]
byclass = {}
for nm, lo, hi in CG:
    sub = [r for r in BL if lo <= r['cg'] <= hi]
    if not sub:
        continue
    d = {}
    for tag in ('W', 'V', 'A'):
        tot = ped = 0.0
        for r in sub:
            Pp = r['production_pts']; V = r['v0_step1_board']; s = r['sigma']; g = r['games_sigma_axis']
            if tag == 'W':
                pr = price_W(Pp, V, s); pd = s * V
            elif tag == 'V':
                pr = price_V(Pp, V, s); pd = s * pr
            else:
                pr = price_A(Pp, V, g); pd = beta_at(g) * V
            tot += pr; ped += pd
        d[tag] = dict(total=tot, share=(ped / tot if tot else None))
    byclass[nm] = dict(n=len(sub), **{k: v for k, v in d.items()})
    P('%-8s %6d %12.0f %12.0f %12.0f %10.4f %10.4f %10.4f'
      % (nm, len(sub), d['W']['total'], d['V']['total'], d['A']['total'],
         d['W']['share'], d['V']['share'], d['A']['share']))
P('')

# ==================================================================================================
# T4 -- THE OBJECT.  entry_anchor vs the Step-1 positional v0.
# ==================================================================================================
P('=' * 100)
P('T4 -- THE OBJECT: entry_anchor against the Step-1 positional v0')
P('=' * 100)
shutil.rmtree(SP + '/eng30br_read', ignore_errors=True)
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(os.path.join(ROOT, 'LTI_REGISTER.md'), STAGE)
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1',
                  MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=ROOT + '/data/v0surf.pkl')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; entry_anchor = G['entry_anchor']

ANCH = {}
for p in MA.data:
    k = p.get('key')
    if not k or k in ANCH:
        continue
    try:
        ANCH[k] = float(entry_anchor(p))
    except Exception:
        pass
P('  entry_anchor read for %d store rows' % len(ANCH))

miss = [r['key'] for r in BL if r['key'] not in ANCH]
P('  blended rows with NO entry_anchor: %d  %s' % (len(miss), miss[:6]))
COV = [r for r in BL if r['key'] in ANCH]
ratios = [ANCH[r['key']] / r['v0_step1_board'] for r in COV if r['v0_step1_board'] > 0]
above = sum(1 for x in ratios if x > 1.0)
dr = disp(ratios)
P('')
P('  entry_anchor / v0_step1  over %d covered blended rows:' % len(ratios))
P('     share above 1.0  %.4f  (%d of %d)' % (above / len(ratios), above, len(ratios)))
P('     median %.4f   mean %.4f   p25 %.4f   p75 %.4f   p10 %.4f   p90 %.4f   sd %.4f'
  % (dr['median'], dr['mean'], dr['p25'], dr['p75'], dr['p10'], dr['p90'], dr['sd']))

# split ND vs pool
for tag, pred in (('ND (non-pool)', lambda r: not r['pool']), ('POOL', lambda r: r['pool'])):
    rr = [ANCH[r['key']] / r['v0_step1_board'] for r in COV if pred(r) and r['v0_step1_board'] > 0]
    if rr:
        d = disp(rr)
        P('     %-14s n %4d  median %.4f  p25 %.4f  p75 %.4f  above-1 %.3f'
          % (tag, d['n'], d['median'], d['p25'], d['p75'], sum(1 for x in rr if x > 1) / len(rr)))
P('')

# whole-book pedigree share under each object, WEIGHT wiring (the preview's own wiring, so the
# comparison isolates the OBJECT and nothing else) and under the ADDITIVE wiring
P('  pedigree %% of printed, whole blended book, by OBJECT and by WIRING:')
P('%-14s %12s %12s %12s %12s' % ('wiring', 'obj=v0 tot', 'obj=v0 share', 'obj=anch tot', 'obj=anch share'))
objagg = {}
for tag in ('W', 'A'):
    row = {}
    for onm in ('v0', 'anchor'):
        tot = ped = 0.0
        for r in COV:
            Pp = r['production_pts']; s = r['sigma']; g = r['games_sigma_axis']
            V = r['v0_step1_board'] if onm == 'v0' else ANCH[r['key']]
            if tag == 'W':
                pr = price_W(Pp, V, s); pd = s * V
            else:
                pr = price_A(Pp, V, g); pd = beta_at(g) * V
            tot += pr; ped += pd
        row[onm] = dict(total=tot, share=(ped / tot if tot else None), pedigree=ped)
    objagg[tag] = row
    P('%-14s %12.0f %12.4f %12.0f %12.4f'
      % (tag, row['v0']['total'], row['v0']['share'], row['anchor']['total'], row['anchor']['share']))
P('')
P('  share delta (anchor - v0):  W %+.4f pp/100   A %+.4f pp/100'
  % (100 * (objagg['W']['anchor']['share'] - objagg['W']['v0']['share']),
     100 * (objagg['A']['anchor']['share'] - objagg['A']['v0']['share'])))
P('')

# named rows under both objects
P('  THE NAMED ROWS UNDER BOTH OBJECTS (weight wiring = the preview\'s own, then additive):')
P('%-18s %5s %8s %9s %9s %9s | %8s %8s | %8s %8s'
  % ('row', 'g', 'sigma', 'prod', 'v0', 'anchor', 'W(v0)', 'W(anch)', 'A(v0)', 'A(anch)'))
t4rows = {}
for k in NAMED:
    r = BYK.get(k)
    if r is None:
        continue
    A = ANCH.get(k)
    Pp = r['production_pts']; V = r['v0_step1_board']; s = r['sigma']; g = r['games_sigma_axis']
    if r['day0'] or s is None:
        # DAY-0 / gameless row: it never reaches the blend at all -- it prints the Step-2 sitter law
        # v0 x D(c).  Reported here under BOTH objects so the T4 comparison covers it.
        d = dict(name=r['name'], pathway=r['pathway'], pick=r['pick'], pos=r['pos'], games=0.0,
                 sigma=None, beta=None, production=Pp, v0=V, entry_anchor=A, day0=True,
                 fade_D=r['fade_D'], fade_clock=r['fade_clock'], pool=r['pool'],
                 W_v0=V * r['fade_D'], A_v0=V * r['fade_D'], V_v0=V * r['fade_D'],
                 W_anchor=(A * r['fade_D'] if A else None),
                 A_anchor=(A * r['fade_D'] if A else None),
                 V_anchor=(A * r['fade_D'] if A else None),
                 preview=r['preview'], step2=r['step2'], live=r['live'])
        t4rows[k] = d
        P('%-18s %5s %8s %9s %9.1f %9s | %8.1f %8s | %8.1f %8s   (DAY-0: sitter law v0 x D=%.4f)'
          % (k, 'day0', '-', ('%.1f' % Pp) if Pp is not None else 'none', V,
             ('%.1f' % A) if A else 'n/a', d['W_v0'],
             ('%.1f' % d['W_anchor']) if A else 'n/a', d['A_v0'],
             ('%.1f' % d['A_anchor']) if A else 'n/a', r['fade_D']))
        continue
    d = dict(name=r['name'], pathway=r['pathway'], pick=r['pick'], pos=r['pos'], games=g,
             sigma=s, beta=beta_at(g), production=Pp, v0=V, entry_anchor=A,
             W_v0=price_W(Pp, V, s), A_v0=price_A(Pp, V, g),
             W_anchor=(price_W(Pp, A, s) if A else None),
             A_anchor=(price_A(Pp, A, g) if A else None),
             V_v0=price_V(Pp, V, s), V_anchor=(price_V(Pp, A, s) if A else None),
             preview=r['preview'], step2=r['step2'], live=r['live'],
             fade_D=r['fade_D'], fade_clock=r['fade_clock'], pool=r['pool'])
    t4rows[k] = d
    P('%-18s %5.0f %8.4f %9.1f %9.1f %9s | %8.1f %8s | %8.1f %8s'
      % (k, g, s, Pp, V, ('%.1f' % A) if A else 'n/a', d['W_v0'],
         ('%.1f' % d['W_anchor']) if A else 'n/a', d['A_v0'],
         ('%.1f' % d['A_anchor']) if A else 'n/a'))
P('')

RES = dict(order='30B-R', task='T1 reading + T4 object', pins=PINS,
           sigma_construction=dict(
               formula='sigma_b := beta_v0 * mean(v0) / mean(R)',
               source='o30bm_measure.py::band_fit line 531',
               identity_checked_to=1e-12,
               band_ratio_v0_over_R={nm: r for nm, r in rat}),
           beta_curve=dict(points=BPTS, interpolation='log-linear in log(games) between band midpoints, flat outside -- AN INTERPOLATION, the same one o30bm_measure.py::sigma_at uses for sigma'),
           t1_named=t1rows, t1_book=agg, t1_by_games_class=byclass,
           t4=dict(n_covered=len(COV), n_missing_anchor=len(miss),
                   ratio_anchor_over_v0=dr, share_above_one=above / len(ratios),
                   object_aggregates=objagg, named=t4rows))
json.dump(RES, open(OUT_JSON, 'w'), indent=1, sort_keys=True, default=float)
open(OUT_TXT, 'w').write('\n'.join(_LOG) + '\n')
P('wrote %s and %s' % (OUT_JSON, OUT_TXT))
