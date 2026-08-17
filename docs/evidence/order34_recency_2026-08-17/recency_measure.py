#!/usr/bin/env python3
"""RECENCY AUDIT SEAT -- effective past-season weights of the production price.

READ-ONLY: the engine is STAGED (bb31f.sh file set) into the scratchpad and loaded in-process;
every perturbed player is an in-memory dict copy; no store file, engine file, board or law is
written. Protocol per PREREG_RECENCY.md (committed and pushed before this ran).

Usage:  recency_measure.py primary   -> RL_O31=1 lane, full sample, writes RECENCY_WEIGHTS.json
        recency_measure.py o32      -> RL_O32=1 lane, 12-player subsample, writes RECENCY_O32.json
"""
import os, sys, io, json, math, shutil, hashlib, contextlib, random, collections

MODE = sys.argv[1] if len(sys.argv) > 1 else 'primary'
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
WS = SP + '/recaudit_' + MODE

_LOG = []
def P(s=''):
    print(s, flush=True)
    _LOG.append(str(s))

def md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

# ---- STAGE (bb31f.sh file set, verbatim) --------------------------------------------------------
shutil.rmtree(WS, ignore_errors=True)
os.makedirs(WS, exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', WS + '/rl_after')
shutil.copytree(ROOT + '/engine/forward_valuation', WS + '/forward_valuation')
for f in ('config_manifest.py', 'fv_provenance.py', 'boot_guard.py', 'LTI_REGISTER.md'):
    shutil.copy(os.path.join(ROOT, f), WS + '/rl_after/' + f)

os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, RL_FV=WS + '/forward_valuation',
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=ROOT + '/data/v0surf.pkl',
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22')
if MODE == 'o32':
    os.environ['RL_O32'] = '1'          # ORDER-A repair candidate (implies RL_O31)
else:
    os.environ['RL_O31'] = '1'          # the Candidate-31 dial ON (the seat's named build)

sys.path[:0] = [ROOT, ROOT + '/vendor', WS + '/forward_valuation', WS + '/rl_after']
_cwd = os.getcwd(); os.chdir(WS + '/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
cp = NSE['cp']; ev = NSE['ev']; delisted = NSE['delisted']; _ldg = NSE['_ldg']
_nqual = NSE['_nqual']
STORE_MD5 = md5(ROOT + '/engine/rl_after/rl_model_data.json')
P('RECENCY AUDIT [%s]  store %s  dial %s  BASE_REF=%d' %
  (MODE, STORE_MD5[:8], ('RL_O32=1' if MODE == 'o32' else 'RL_O31=1'), MA.BASE_REF))

Y = 2026
KEEP = []                                  # hold every perturbed dict alive (id-keyed cache hazard)

def played(p):
    d0 = cp.debutyr(p) - 1
    return sorted([x for x in p['scoring'] if (x.get('games') or 0) > 0 and d0 < x['year'] <= Y],
                  key=lambda x: x['year'])

def pert(p, year, d):
    q = dict(p)
    q['scoring'] = [({**x, 'avg': x['avg'] + d} if x['year'] == year else {**x})
                    for x in p['scoring']]
    KEEP.append(q)
    return q

def price(p):
    with contextlib.redirect_stdout(io.StringIO()):
        return float(ev(p, Y))

# ---- SAMPLE (prereg section 2) ------------------------------------------------------------------
cells = collections.defaultdict(list)
for p in MA.data:
    if not p.get('key') or p.get('_retired') or p.get('_pool') or delisted(p):
        continue
    ns = len(played(p))
    if not (2 <= ns <= 6):
        continue
    cells[(_ldg(MA.gfut(p)), ns)].append(p)

rng = random.Random(3334)
SAMPLE = []
for cell in sorted(cells, key=lambda c: (c[0], c[1])):
    pool = sorted(cells[cell], key=lambda p: p['key'])
    take = pool if len(pool) <= 3 else rng.sample(pool, 3)
    for p in sorted(take, key=lambda p: p['key']):
        bp = price(p)
        if bp >= 100.0:
            SAMPLE.append((p, bp))
if MODE == 'o32':
    SAMPLE = SAMPLE[:12]                 # prereg section 1: 12-player disclosure subsample
P('sample: %d players (cells %d; base ev >= 100 filter applied)' % (len(SAMPLE), len(cells)))

# ---- MEASUREMENT (prereg section 3) -------------------------------------------------------------
DELTA = 2.0
ROWS = []
for p, base in SAMPLE:
    rows = played(p)
    resp = []
    for x in rows:
        dv = price(pert(p, x['year'], DELTA)) - base
        resp.append(dict(year=x['year'], back=Y - x['year'], games=x['games'], avg=x['avg'],
                         dv=dv))
    tot = sum(r['dv'] for r in resp)
    for r in resp:
        r['w'] = (r['dv'] / tot) if tot > 1e-9 else None
    ROWS.append(dict(key=p['key'], name=p.get('player'), pos=MA.gfut(p), grp=_ldg(MA.gfut(p)),
                     age=cp._age_asof(p, Y), pick=p.get('pick'), typ=p.get('type'),
                     nseasons=len(rows), base=base, total_dv=tot,
                     latest_completed_games=(max([x for x in rows if x['year'] <= 2025],
                                                 key=lambda x: x['year'])['games']
                                             if any(x['year'] <= 2025 for x in rows) else None),
                     resp=resp))
    P('  %-28s %-4s ns=%d base=%8.1f  totdv=%7.3f  w=[%s]' %
      (p['key'][:28], MA.gfut(p), len(rows), base, tot,
       ', '.join(('%d:%s' % (r['back'], ('%.3f' % r['w']) if r['w'] is not None else 'NA'))
                 for r in resp)))

usable = [r for r in ROWS if r['total_dv'] > 1e-9]
P('')
P('usable (positive total response): %d of %d;  unresponsive: %s' %
  (len(usable), len(ROWS), [r['key'] for r in ROWS if r['total_dv'] <= 1e-9]))
neg = [(r['key'], q['year'], q['dv']) for r in ROWS for q in r['resp'] if q['dv'] < -1e-9]
P('negative single-season responses (disclosed): %d  %s' % (len(neg), neg[:12]))

def q(v, f):
    v = sorted(v); n = len(v)
    if n == 0: return float('nan')
    i = f * (n - 1); lo = int(math.floor(i)); hi = min(lo + 1, n - 1)
    return v[lo] + (i - lo) * (v[hi] - v[lo])

def agg(rows, label):
    P('')
    P('EFFECTIVE WEIGHT BY YEARS-BACK -- %s  (n players = %d)' % (label, len(rows)))
    P('%8s %6s %8s %8s %8s %8s' % ('back', 'n', 'mean', 'median', 'q25', 'q75'))
    by = collections.defaultdict(list)
    for r in rows:
        for x in r['resp']:
            if x['w'] is not None:
                by[x['back']].append(x['w'])
    for b in sorted(by):
        v = by[b]
        P('%8d %6d %8.3f %8.3f %8.3f %8.3f' %
          (b, len(v), sum(v) / len(v), q(v, .5), q(v, .25), q(v, .75)))
    lat = [sum(x['w'] for x in r['resp'] if x['back'] <= 1 and x['w'] is not None)
           for r in rows if any(x['w'] is not None for x in r['resp'])]
    l26 = [sum(x['w'] for x in r['resp'] if x['back'] == 0 and x['w'] is not None) for r in rows]
    l25 = [sum(x['w'] for x in r['resp'] if x['back'] == 1 and x['w'] is not None) for r in rows]
    P('LATEST-SEASON SHARE (back<=1 = 2025 completed + 2026 in-progress): '
      'mean %.3f  median %.3f  IQR [%.3f, %.3f]' % (sum(lat) / len(lat), q(lat, .5),
                                                    q(lat, .25), q(lat, .75)))
    P('  of which 2026 in-progress alone: median %.3f;  2025 alone: median %.3f' %
      (q(l26, .5), q(l25, .5)))
    return lat

LAT = agg(usable, 'ALL')
agg([r for r in usable if r['nseasons'] <= 3], 'seasons-of-history 2-3')
agg([r for r in usable if r['nseasons'] >= 4], 'seasons-of-history 4-6')
for lo, hi, lab in ((0, 9, 'latest completed <10 games'), (10, 17, '10-17'), (18, 99, '18+')):
    agg([r for r in usable if r['latest_completed_games'] is not None
         and lo <= r['latest_completed_games'] <= hi], lab)
for g in ('KEY', 'GEN', 'MR'):
    agg([r for r in usable if r['grp'] == g], 'group ' + g)

# ---- NONLINEARITY (prereg section 3; primary lane only) -----------------------------------------
NONLIN = []
if MODE == 'primary':
    P('')
    P('PERTURBATION-SIZE SENSITIVITY (delta 1 vs 4), first 10 sampled players')
    for p, base in SAMPLE[:10]:
        rows = played(p)
        ws = {}
        for d in (1.0, 4.0):
            resp = [(x['year'], price(pert(p, x['year'], d)) - base) for x in rows]
            tot = sum(v for _, v in resp)
            ws[d] = {yr: (v / tot if tot > 1e-9 else None) for yr, v in resp}
        diffs = [abs(ws[1.0][yr] - ws[4.0][yr]) for yr in ws[1.0]
                 if ws[1.0][yr] is not None and ws[4.0][yr] is not None]
        m = max(diffs) if diffs else None
        NONLIN.append(dict(key=p['key'], max_abs_dw=m,
                           w1={str(k): v for k, v in ws[1.0].items()},
                           w4={str(k): v for k, v in ws[4.0].items()}))
        P('  %-28s max|dw(1)-dw(4)| = %s' % (p['key'][:28],
                                             ('%.4f' % m) if m is not None else 'NA'))
    mm = sorted(x['max_abs_dw'] for x in NONLIN if x['max_abs_dw'] is not None)
    med = q(mm, .5) if mm else float('nan')
    P('  sample median max|dw| = %.4f  (trip at > 0.10: %s)' %
      (med, 'FIRED' if med > 0.10 else 'not fired'))

# ---- DIVERGENCE RANK on current board rows (store-only; for section 5 material) -----------------
DIVERG = []
if MODE == 'primary':
    LED = json.load(open(os.path.join(ROOT, 'docs/ledgers/CANDIDATE_31_MOVERS.json')))
    ledger = {r['key']: r for r in LED['rows']}
    for p in MA.data:
        k = p.get('key')
        if not k or k not in ledger or p.get('_retired') or delisted(p):
            continue
        rows = played(p)
        comp = [x for x in rows if x['year'] <= 2025]
        if len(comp) < 2:
            continue
        latest = max(comp, key=lambda x: x['year'])
        pri = [x for x in comp if x['year'] < latest['year']]
        pw = sum(x['games'] * (0.72 ** (latest['year'] - x['year'])) for x in pri)
        pa = (sum(x['games'] * (0.72 ** (latest['year'] - x['year'])) * x['avg'] for x in pri) / pw
              if pw > 0 else None)
        if pa is None or latest['games'] < 6:
            continue
        DIVERG.append(dict(key=k, pos=MA.gfut(p), latest_avg=latest['avg'],
                           latest_games=latest['games'], prior_avg=pa,
                           div=latest['avg'] - pa, cand=ledger[k].get('cand'),
                           o31=ledger[k].get('o31')))
    DIVERG.sort(key=lambda r: -abs(r['div']))
    P('')
    P('BOARD ROWS WITH LARGEST LATEST-vs-HISTORY DIVERGENCE (store-only; top 12 each side)')
    up = [r for r in DIVERG if r['div'] > 0][:12]; dn = [r for r in DIVERG if r['div'] < 0][:12]
    for lab, rs in (('LATEST ABOVE HISTORY (risers)', up), ('LATEST BELOW HISTORY (faders)', dn)):
        P('  ' + lab)
        for r in rs:
            P('    %-26s %-4s latest %6.1f (%2dg) vs prior %6.1f  div %+6.1f  board(cand) %s'
              % (r['key'][:26], r['pos'], r['latest_avg'], r['latest_games'],
                 r['prior_avg'], r['div'], r['cand']))

OUT = dict(mode=MODE, store_md5=STORE_MD5, dial=('RL_O32=1' if MODE == 'o32' else 'RL_O31=1'),
           base_ref=MA.BASE_REF, delta=DELTA, n_sample=len(SAMPLE), n_usable=len(usable),
           latest_share=dict(mean=sum(LAT) / len(LAT), median=q(LAT, .5),
                             q25=q(LAT, .25), q75=q(LAT, .75)),
           rows=ROWS, nonlin=NONLIN, divergence_top=DIVERG[:60],
           prereg='PREREG_RECENCY.md pushed before this ran')
fn = 'RECENCY_O32.json' if MODE == 'o32' else 'RECENCY_WEIGHTS.json'
json.dump(OUT, open(os.path.join(HERE, fn), 'w'))
open(os.path.join(HERE, 'MEASURE_RECENCY_%s_out.txt' % MODE), 'w').write('\n'.join(_LOG) + '\n')
P('')
P('wrote %s + MEASURE_RECENCY_%s_out.txt' % (fn, MODE))
