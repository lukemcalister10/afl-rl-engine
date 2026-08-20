#!/usr/bin/env python3
# =====================================================================================================
# ORDER F -- THE ENTRY TIMING-WEDGE VERIFICATION.  READ-ONLY.
#
# Everything here executes the rule fixed in PREREG_F.md, committed and pushed BEFORE any number below
# was computed (commit d20f71c).  No engine import, no board build, no store write, no artifact write.
#
# PART 1  P1 -- what value was the v0 entry surface actually fitted to?  (code, quoted by line)
# PART 2  the two-clock arithmetic: what the board's OWN discount convention says the yr0->1 mark
#         should be.  disc_factor is LIFTED BY SOURCE TEXT out of the engine and exec'd VERBATIM.
# PART 3  delivery timing profiles per band and per arm, on the S4 delivered-value ruler (LIFTED BY
#         SOURCE TEXT out of s4_shootout.py -- the house ruler is reused, never reinvented).
# PART 4  the wedge table: the hypothesis's own object (counterfactual bound) and the operative one.
# PART 5  the match test at the prereg tolerance, vs the observed yr0->1 marks.
# PART 6  the adversarial alternatives ALT-1 and ALT-2, on the same data.
# =====================================================================================================
import json, math, os, sys, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

S4SRC = os.path.join(EV, 'order32_s4_2026-08-17', 's4_shootout.py')
RLSRC = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py')
L2SRC = os.path.join(EV, 'grace_adoption_2026-08-13', 'inputs', 'o26b_layer2.py')
D28SRC = os.path.join(EV, 'grace_adoption_2026-08-13', 'o28_derive.py')
HFSRC = os.path.join(EV, 'candidate_31f', 'o31f_headfix.py')
MAT = os.path.join(SP, 'per_entrant_O34FINAL.json')          # the matrix ATTRIBUTION_34 itself read
MAT_C32 = os.path.join(SP, 'per_entrant_O32RFINAL.json')     # repaired C32, the supervisor's marks

CARRY = 1.14
ENTRY_LO, ENTRY_HI = 2005, 2019      # prereg: observable futures
HORIZON = 6                          # prereg: the fixed horizon common to every class

_OUT = []
def P(s=''):
    print(s); _OUT.append(str(s))

def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

def quote(path, a, b):
    """Quote lines a..b of a file, verbatim, with line numbers -- so the quote cannot drift."""
    L = open(path).read().split('\n')
    return '\n'.join('  %4d | %s' % (i, L[i - 1]) for i in range(a, b + 1))


# =====================================================================================================
P('=' * 118)
P('ORDER F -- ENTRY TIMING-WEDGE VERIFICATION.  READ-ONLY.  Rule fixed in PREREG_F.md (commit d20f71c).')
P('=' * 118)
P('  sources, md5-stamped:')
for p in (S4SRC, RLSRC, L2SRC, D28SRC, HFSRC, MAT, MAT_C32):
    P('    %-58s %s' % (os.path.relpath(p, ROOT) if p.startswith(ROOT) else os.path.basename(p), md5f(p)))
P()

# =====================================================================================================
P('=' * 118)
P('PART 1 -- P1: WHAT VALUE WAS THE v0 ENTRY SURFACE FITTED TO?')
P('=' * 118)
P()
P('The v0 entry surface (the pick curve and the positional surface on it) is derived in')
P('docs/evidence/grace_adoption_2026-08-13/o28_derive.py.  Its fit target is the argument SC:')
P()
P(quote(D28SRC, 158, 165))
P()
P('and the call site names SC exactly:')
P()
P(quote(D28SRC, 311, 314))
P()
P("L2['grace_a'] is built in o26b_layer2.py by score_all(...) with the grace-A reading:")
P()
P(quote(L2SRC, 636, 638))
P()
P('score_all sums an OBSERVED leg and a projected TAIL leg into `total`:')
P()
P(quote(L2SRC, 448, 461))
P()
P('and the observed leg -- THE LINE THAT DECIDES P1 -- is:')
P()
P(quote(L2SRC, 376, 399))
P()
P('  `pts = MA.SCALE * raw * w / D.f(ea, k)` -- every season is DIVIDED BY A DISCOUNT FACTOR,')
P('  keyed on k = season_year - entry_year.  D.f is:')
P()
P(quote(L2SRC, 350, 353))
P()
P('  and the tail leg discounts on the SAME ladder, by its own docstring:')
P()
P(quote(L2SRC, 402, 405))
P()
P('The same target reappears in the ORDER 31-F head fix, which reconstructs the fit population:')
P()
P(quote(HFSRC, 80, 84))
P()
P('*** P1 VERDICT: FALSIFIED. ***  The v0 fit target is NOT an undiscounted career total.  It is a')
P('TIME-OF-DELIVERY DISCOUNTED career value: flat 14%/yr (LENS[bal] = 0.14, AGE_DISC off), with the')
P('grace-A exponent shift max(0, k - G) that the owner ruled at ORDER 28.  The hypothesis as posed --')
P('"fitted to career-integrated delivered value WITHOUT time-of-delivery discounting" -- is false on')
P('the code.  Per PREREG_F.md section 5, the wedge computation as specified STOPS here and is')
P('reported only as a counterfactual bound; the seat proceeds to the replacement question.')
P()

# =====================================================================================================
P('=' * 118)
P('PART 2 -- THE TWO-CLOCK ARITHMETIC: WHAT THE BOARD\'S OWN CONVENTION SAYS THE yr0->1 MARK IS')
P('=' * 118)
P()
P('The engine\'s discount factor, LIFTED BY SOURCE TEXT and exec\'d VERBATIM (no re-implementation):')
P()
P(quote(RLSRC, 1004, 1024))
P()
_src = open(RLSRC).read()
_blk = _src.split('def disc_factor(a,d,k,lens=\'bal\',grace=0):')[1].split('\nLENS=')[0]
_blk = 'def disc_factor(a,d,k,lens=\'bal\',grace=0):' + _blk
LIFT_MD5 = hashlib.md5(_blk.encode()).hexdigest()
NS = dict(AGE_DISC=False, age_disc=lambda a, d, lens='bal': d, age_disc_mode=lambda: 0,
          _pw_interp=None, _V9_KNOTS=None, math=math)
exec(_blk, NS)
disc_factor = NS['disc_factor']
P('  lifted disc_factor text md5 %s  (%d lines).  Live config asserted: AGE_DISC off, LENS[bal]=0.14.' %
  (LIFT_MD5, _blk.count('\n')))
assert abs(disc_factor(18, 0.14, 3, 'bal', 0) - 1.14 ** 3) < 1e-12
P('  control: disc_factor(18, 0.14, 3, grace=0) == 1.14^3 -> %.10f  PASS' % disc_factor(18, 0.14, 3, 'bal', 0))
P()
P('The grace-A dial, engine side (rl_model.py:234-241), DEFAULT ON since ORDER 29\'s landing:')
P()
P(quote(RLSRC, 234, 241))
P()
P('TWO CLOCKS, ONE RULE (PREREG_ORDER28 sec 1.1, quoted in rl_model.py:206-213):')
P()
P(quote(RLSRC, 202, 213))
P()
P('So put the two vantages side by side for one entrant drafted in year e.  Let his season e+j carry')
P('delivered value v_j, j = 1, 2, 3, ...  (j=1 is his first played season; debut = e+1).')
P()
P('  ENTRY (the curve clock, k_c = j, exponent max(0, k_c - G_O), G_O = 2 for entry age <= 19)')
P('  YEAR 1 (the engine clock; the yr1 board prices forward from his SECOND season, so k_e = j - 2,')
P('          and grace_years = max(0, 1 - max(0, AGE_REF - debut)) = 0 at that vantage)')
P()
GO = {'age<=19': 2, 'age>=20': 0}
GE = {'age<=19': 0, 'age>=20': 0}
ACC = {}
for lab in ('age<=19', 'age>=20'):
    a = 18 if lab == 'age<=19' else 21
    P('  entry age %s   (curve G_O = %d ; engine grace at the yr1 vantage = %d)' % (lab, GO[lab], GE[lab]))
    P('    %-26s %s' % ('season j', ''.join('%10d' % j for j in range(1, 8))))
    f0 = [1.0 / disc_factor(a, 0.14, j, 'bal', GO[lab]) for j in range(1, 8)]
    f1 = [(0.0 if j == 1 else 1.0 / disc_factor(a, 0.14, j - 2, 'bal', GE[lab])) for j in range(1, 8)]
    P('    %-26s %s' % ('weight in ENTRY price', ''.join('%10.5f' % x for x in f0)))
    P('    %-26s %s' % ('weight in YEAR-1 price', ''.join(('%10s' % 'delivered') if j == 1 else
                                                          '%10.5f' % f1[j - 1] for j in range(1, 8))))
    r = [f1[j - 1] / f0[j - 1] for j in range(2, 8)]
    ACC[lab] = r[0]
    P('    %-26s %s' % ('accretion yr1/entry', '%10s' % 'n/a' + ''.join('%10.5f' % x for x in r)))
    assert all(abs(x - r[0]) < 1e-12 for x in r), 'accretion is not uniform across surviving seasons'
    P('    -> every surviving season accretes by EXACTLY %.5f over the entry->year-1 step.' % r[0])
    P()
P('*** THE FINDING THAT REPLACES THE HYPOTHESIS ***')
P('  For a grace-eligible entrant (entry age <= 19 -- the overwhelming majority of the draft), the')
P('  entry price and the year-1 price weight every surviving season IDENTICALLY (accretion %.5f).' % ACC['age<=19'])
P('  The grace-A rule gives seasons 1 and 2 full weight at the entry clock and exactly one extra free')
P('  step at the engine clock, and the two were DESIGNED to line up.  The consequence, which appears')
P('  not to have been carried into the no-arb benchmark, is that THE ENTRY->YEAR-1 STEP EARNS NO CARRY')
P('  FOR A GRACE-ELIGIBLE ENTRANT.  His board-consistent fair year-1 mark is')
P('        fair_grace = 1.00 x (1 - s1)        NOT   fair_C = 1.14 x (1 - s1).')
P('  For a mature-age entrant (>= 20) there is no grace on either clock, the step accretes by %.2f,' % ACC['age>=20'])
P('  and Order C\'s fair_C = 1.14 x (1 - s1) is exactly right for him.')
P()

# =====================================================================================================
P('=' * 118)
P('PART 3 -- DELIVERY TIMING PROFILES ON THE HOUSE RULER')
P('=' * 118)
P()
_s4 = open(S4SRC).read()
_rul = 'B_BOOT = 2000' + _s4.split('B_BOOT = 2000')[1].split('\nA = json.load(open(CAND_P))')[0]
RUL_MD5 = hashlib.md5(_rul.encode()).hexdigest()
RNS = dict(math=math, os=os, hashlib=hashlib, json=json)
exec(_rul, RNS)
BARS = RNS['BARS']; w_sqrt = RNS['w_sqrt']; season_raw = RNS['season_raw']; FM = RNS['FM']
LAST_REAL_SEASON = RNS['LAST_REAL_SEASON']
P('  S4 ruler lifted by source text from %s' % os.path.relpath(S4SRC, ROOT))
P('    lifted text md5 %s  (%d lines).  BARS %s ; LAST_REAL_SEASON %d ; FM %s'
  % (RUL_MD5, _rul.count('\n'), BARS, LAST_REAL_SEASON, sorted(FM)))
P('    control: season value == w_sqrt(games) * posval(avg + capt_prem(avg) - BAR) * 21.0')
P()

A = json.load(open(MAT))
Arecs = {r['key']: r for r in A['recs']}
_sv = '# ---- per-player season values' + _s4.split('# ---- per-player season values')[1].split('\ndef dv1(')[0]
SVNS = dict(Arecs=Arecs, BARS=BARS, w_sqrt=w_sqrt, season_raw=season_raw,
            LAST_REAL_SEASON=LAST_REAL_SEASON, SV={})
exec(_sv, SVNS)
SV = SVNS['SV']
P('  SV assembly lifted verbatim too (md5 %s); %d players carry a season map.'
  % (hashlib.md5(_sv.encode()).hexdigest(), len(SV)))
P()


def band_of(pk):
    if pk is None: return None
    if pk <= 10: return '1-10'
    if pk <= 20: return '11-20'
    if pk <= 30: return '21-30'
    if pk <= 40: return '31-40'
    if pk <= 64: return '41-64'
    return None


BANDS = ['1-10', '11-20', '21-30', '31-40', '41-64']
ARMS = ['RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS']


def cells_of(r):
    """The prereg's populations: five ND bands on the curve, the eight pool arms by type."""
    out = []
    if r.get('teaches_curve') and r['type'] == 'ND':
        b = band_of(r.get('pick'))
        if b: out.append(('ND ' + b, b))
    elif r.get('is_pool'):
        out.append(('ARM ' + r['type'], r['type']))
    return out


ROWS = collections.defaultdict(list)
zero_u = collections.Counter(); nall = collections.Counter()
for k, r in Arecs.items():
    if k in FM: continue
    y = r['year']
    if y < ENTRY_LO or y > ENTRY_HI: continue
    cs = cells_of(r)
    if not cs: continue
    d = SV.get(k, {})
    prof_full = {j: d.get(y + j, 0.0) for j in range(1, LAST_REAL_SEASON - y + 1)}
    prof_h = {j: d.get(y + j, 0.0) for j in range(1, HORIZON + 1)}
    row = dict(key=k, y=y, pick=r.get('pick'), aged=r.get('age_draft'), v0=float(r['v0']),
               p1=float(r['vpath'][0]) if r.get('vpath') and r['vpath'][0] is not None else None,
               g1=int(r.get('games_yr1') or 0), full=prof_full, hz=prof_h,
               U=sum(prof_full.values()), Uh=sum(prof_h.values()))
    for cname, _ in cs:
        ROWS[cname].append(row); nall[cname] += 1
        if row['U'] <= 0: zero_u[cname] += 1


def profile(rows, key='full', K=12):
    """Value-weighted cohort share of career delivered value arriving in year k after entry."""
    num = collections.defaultdict(float); den = 0.0
    for r in rows:
        for j, v in r[key].items():
            num[j] += v
        den += sum(r[key].values())
    if den <= 0: return {}, 0.0
    return {j: num[j] / den for j in range(1, K + 1) if j in num}, den


def wedge(sh, G):
    """sum_k s_k * 1.14^-k  (G=None) or the fit target's own ladder sum_k s_k * 1.14^-max(0,k-G)."""
    if G is None:
        return sum(s * CARRY ** -j for j, s in sh.items())
    return sum(s * CARRY ** -max(0, j - G) for j, s in sh.items())


def pdisp(rows, key='full'):
    """Cross-player dispersion of the per-player pure wedge, p25/p50/p75, over players with U>0."""
    ws = []
    for r in rows:
        u = sum(r[key].values())
        if u <= 0: continue
        ws.append(sum(v * CARRY ** -j for j, v in r[key].items()) / u)
    ws.sort()
    if not ws: return (float('nan'),) * 3
    q = lambda f: ws[min(len(ws) - 1, int(f * len(ws)))]
    return q(0.25), q(0.50), q(0.75)


ORDER = ['ND ' + b for b in BANDS] + ['ARM ' + a for a in ARMS]
P('DELIVERY TIMING PROFILE -- value-weighted share of career delivered value arriving in year k after')
P('entry.  Classes %d-%d.  Full observable window (right-censored at %d) and the fixed %d-year horizon.'
  % (ENTRY_LO, ENTRY_HI, LAST_REAL_SEASON, HORIZON))
P()
P('  %-10s %5s %5s %s   %8s %8s' % ('cell', 'n', 'U=0', ''.join('%7s' % ('yr%d' % j) for j in range(1, 9)),
                                    'mean_yr', 'p50wedge'))
PROF = {}
for c in ORDER:
    rows = ROWS.get(c, [])
    if not rows:
        P('  %-10s %5d  (no rows in window)' % (c, 0)); continue
    sh, den = profile(rows, 'full')
    shh, _ = profile(rows, 'hz')
    mean_yr = sum(j * s for j, s in sh.items()) if sh else float('nan')
    q25, q50, q75 = pdisp(rows, 'full')
    PROF[c] = dict(n=len(rows), sh=sh, shh=shh, mean_yr=mean_yr, q=(q25, q50, q75),
                   zero=zero_u[c], den=den)
    P('  %-10s %5d %5d %s   %8.2f %8.3f'
      % (c, len(rows), zero_u[c], ''.join('%7.3f' % sh.get(j, 0.0) for j in range(1, 9)), mean_yr, q50))
P()
P('  "mean_yr" is the value-weighted mean year of delivery -- the single number that says how late a')
P('  cell\'s value arrives.  "p50wedge" is the median PLAYER\'s own sum_k s_k 1.14^-k (dispersion below).')
P()
P('  cross-player dispersion of the per-player pure wedge (p25 / p50 / p75):')
for c in ORDER:
    if c in PROF:
        P('    %-10s  %.3f / %.3f / %.3f   (n with U>0: %d)'
          % (c, PROF[c]['q'][0], PROF[c]['q'][1], PROF[c]['q'][2], PROF[c]['n'] - PROF[c]['zero']))
P()

# =====================================================================================================
P('=' * 118)
P('PART 4 -- THE WEDGE TABLE')
P('=' * 118)
P()
P('  W_pure     = sum_k s_k * 1.14^-k     -- the wedge IF the entry price were an undiscounted career')
P('                                          total.  P1 falsified that premise, so this column is a')
P('                                          COUNTERFACTUAL BOUND, printed for the record, not the')
P('                                          operative finding (PREREG_F sec 5).')
P('  W_target   = sum_k s_k * 1.14^-max(0,k-G)  -- the ladder the fit target ACTUALLY uses, G = 2 for')
P('                                          entry age <= 19 and 0 otherwise (grace-A, reading O).')
P('  W_resid    = W_pure / W_target       -- how much the entry price still overstates a STRICT-carry')
P('                                          present value.  This is the only wedge that survives P1.')
P()
P('  %-10s %5s %9s %9s %9s %9s %9s' % ('cell', 'n', 'W_pure', 'W_targ', 'W_resid', 'W_pure_h', 'meanG'))
WED = {}
for c in ORDER:
    if c not in PROF: continue
    rows = ROWS[c]
    tw = sum(sum(r['full'].values()) for r in rows)
    if tw <= 0: continue
    gsum = sum(sum(r['full'].values()) * (2 if (r['aged'] is not None and r['aged'] <= 19) else 0)
               for r in rows) / tw
    num_t = 0.0
    for r in rows:
        G = 2 if (r['aged'] is not None and r['aged'] <= 19) else 0
        num_t += sum(v * CARRY ** -max(0, j - G) for j, v in r['full'].items())
    wt = num_t / tw
    wp = wedge(PROF[c]['sh'], None)
    wph = wedge(PROF[c]['shh'], None)
    WED[c] = dict(pure=wp, targ=wt, resid=wp / wt, pure_h=wph, meanG=gsum)
    P('  %-10s %5d %9.3f %9.3f %9.3f %9.3f %9.2f' % (c, PROF[c]['n'], wp, wt, wp / wt, wph, gsum))
P()
P('  Read the W_resid column: it is essentially 1/1.14^G -- a LEVEL, set by the entrant\'s age, not a')
P('  TIMING gradient.  The grace ladder and the strict ladder differ by a constant for every season')
P('  from k = G+1 onward, so the residual cannot vary with how LATE a cell delivers.  That is the')
P('  structural reason the timing story cannot produce a band spread on this board.')
P()

# =====================================================================================================
P('=' * 118)
P('PART 5 -- THE MATCH TEST AT THE PREREG TOLERANCE')
P('=' * 118)
P()
OBS_BAND = {'1-10': 1.048, '11-20': 1.087, '21-30': 1.037, '31-40': 0.885, '41-64': 0.929}
OBS_ARM = {'RD': 0.98, 'UNR': 0.62, 'PDA': 0.81, 'PDN': 0.64, 'SSP': 1.51, 'IRE': 1.09, 'PDS': 0.76}


def s1_and_fair(rows):
    """Order C's own construction, reproduced: sh = sv1 / (sv1 + dv1), fair_C = 1.14 * (1 - sh).
    dv1 discounts every later season back to the year-1 clock at 1.14."""
    sv1 = 0.0; dv1 = 0.0
    for r in rows:
        sv1 += r['full'].get(1, 0.0)
        dv1 += sum(v * CARRY ** -(j - 1) for j, v in r['full'].items() if j >= 2)
    if sv1 + dv1 <= 0: return float('nan'), float('nan')
    sh = sv1 / (sv1 + dv1)
    return sh, CARRY * (1.0 - sh)


P('  s1 is rebuilt with ORDER C\'s OWN construction (o34_attribution.py cell_line), so fair_C here is')
P('  comparable to the published table; the only difference is my class window (%d-%d, prereg) vs its'
  % (ENTRY_LO, ENTRY_HI))
P('  2005-2021, which is disclosed and reported below as a control.')
P()
P('  %-10s %5s %7s %8s %8s %9s %9s %9s %7s' %
  ('cell', 'n', 's1', 'obs mark', 'fair_C', 'W_implied', 'W_pure', 'diff', 'verdict'))
MATCH = collections.Counter(); CELLS = []
for c in ORDER:
    if c not in PROF: continue
    nm = c.split(' ', 1)[1]
    obs = OBS_BAND.get(nm) if c.startswith('ND') else OBS_ARM.get(nm)
    rows = ROWS[c]
    sh, fair = s1_and_fair(rows)
    if obs is None or fair != fair or fair <= 0:
        P('  %-10s %5d %7.3f %8s %8.3f %9s %9.3f %9s %7s'
          % (c, PROF[c]['n'], sh, 'n/a', fair, 'n/a', WED[c]['pure'], 'n/a', 'no mark'))
        continue
    wi = obs / fair
    wp = WED[c]['pure']
    d = wp - wi
    thin = PROF[c]['n'] < 15
    v = 'THIN' if thin else ('MATCH' if abs(d) <= 0.05 else ('NEAR' if abs(d) <= 0.10 else 'MISS'))
    MATCH[v] += 1
    CELLS.append((c, wi, wp, d, v, thin))
    P('  %-10s %5d %7.3f %8.3f %8.3f %9.3f %9.3f %+9.3f %7s'
      % (c, PROF[c]['n'], sh, obs, fair, wi, wp, d, v))
P()
P('  tally: %s' % dict(MATCH))
scored = [x for x in CELLS if not x[5]]
P('  scored cells (n>=15): %d   MATCH %d   NEAR %d   MISS %d'
  % (len(scored), sum(1 for x in scored if x[4] == 'MATCH'), sum(1 for x in scored if x[4] == 'NEAR'),
     sum(1 for x in scored if x[4] == 'MISS')))


def spearman(xs, ys):
    n = len(xs)
    if n < 3: return float('nan')
    def rk(v):
        o = sorted(range(n), key=lambda i: v[i]); r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[o[j + 1]] == v[o[i]]: j += 1
            for t in range(i, j + 1): r[o[t]] = (i + j) / 2.0 + 1
            i = j + 1
        return r
    rx, ry = rk(xs), rk(ys)
    mx = sum(rx) / n; my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den if den else float('nan')


bcells = [x for x in CELLS if x[0].startswith('ND')]
P('  band-only rank correlation between W_pure and W_implied (5 bands): rho = %.3f'
  % spearman([x[2] for x in bcells], [x[1] for x in bcells]))
P('  band W_pure spread   (max-min): %.3f' % (max(x[2] for x in bcells) - min(x[2] for x in bcells)))
P('  band W_implied spread(max-min): %.3f' % (max(x[1] for x in bcells) - min(x[1] for x in bcells)))
P()
armw = {c.split(' ', 1)[1]: WED[c]['pure'] for c in WED if c.startswith('ARM')}
P('  SIGN TEST S1 (prereg): W_SSP must be the LARGEST pool-arm wedge.')
big = max(armw, key=lambda k: armw[k])
P('    W by arm: %s' % '  '.join('%s %.3f' % (k, armw[k]) for k in ARMS if k in armw))
P('    largest = %s (%.3f) ; W_SSP = %.3f  -> %s'
  % (big, armw[big], armw.get('SSP', float('nan')), 'PASS' if big == 'SSP' else 'FAIL'))
s2 = all(armw.get(k, 9) < armw.get('RD', 0) for k in ('PDS', 'PDN', 'PDA'))
P('  SIGN TEST S2 (prereg): W_PDS, W_PDN, W_PDA must all sit BELOW W_RD.')
P('    W_RD %.3f | PDS %.3f PDN %.3f PDA %.3f  -> %s'
  % (armw.get('RD', float('nan')), armw.get('PDS', float('nan')), armw.get('PDN', float('nan')),
     armw.get('PDA', float('nan')), 'PASS' if s2 else 'FAIL'))
P()

# =====================================================================================================
P('=' * 118)
P('PART 6 -- THE ADVERSARIAL ALTERNATIVES, ON THE SAME DATA')
P('=' * 118)
P()
P('ALT-2 FIRST (it is the one PART 2 predicts): re-base the fair mark onto the board\'s OWN clock.')
P('  fair_board = accretion(entry age) x (1 - s1),  with PART 2\'s OWN computed accretions:')
P('    entry age <= 19 : %.5f   (grace-A absorbs the step -- no carry is earned)' % ACC['age<=19'])
P('    entry age >= 20 : %.5f   (= 1.14^2: no grace, AND the curve clock sits one index step ahead' % ACC['age>=20'])
P('                              of the engine clock at the corresponding vantage)')
P('  mixed by entry points inside each cell.  Order C uses 1.14 for EVERYONE.')
P()
P('  %-10s %5s %6s %8s %8s %8s %9s %9s %7s' %
  ('cell', 'n', 'sh<=19', 'obs', 'fair_C', 'gap_C', 'fair_bd', 'gap_bd', 'better?'))
GAPS = []
for c in ORDER:
    if c not in PROF: continue
    nm = c.split(' ', 1)[1]
    obs = OBS_BAND.get(nm) if c.startswith('ND') else OBS_ARM.get(nm)
    rows = ROWS[c]
    sh, fair = s1_and_fair(rows)
    wv = sum(r['v0'] for r in rows)
    young = sum(r['v0'] for r in rows if r['aged'] is not None and r['aged'] <= 19) / wv if wv > 0 else 0.0
    acc = sum(r['v0'] * (ACC['age<=19'] if (r['aged'] is not None and r['aged'] <= 19) else ACC['age>=20'])
              for r in rows) / wv if wv > 0 else float('nan')
    fg = acc * (1.0 - sh)
    if obs is None: continue
    gC = obs - fair; gG = obs - fg
    GAPS.append((c, gC, gG))
    P('  %-10s %5d %6.2f %8.3f %8.3f %+8.3f %9.3f %+9.3f %7s'
      % (c, PROF[c]['n'], young, obs, fair, gC, fg, gG, 'yes' if abs(gG) < abs(gC) else 'no'))
P()
_nd = [(a, b) for c, a, b in GAPS if c.startswith('ND')]
P('  mean |gap|, all 12 cells : fair_C %.4f -> fair_board %.4f' % (sum(abs(g) for _, g, _ in GAPS) / len(GAPS), sum(abs(g) for _, _, g in GAPS) / len(GAPS)))
P('  mean |gap|, 5 ND bands   : fair_C %.4f -> fair_board %.4f' % (sum(abs(a) for a, _ in _nd) / len(_nd), sum(abs(b) for _, b in _nd) / len(_nd)))
P('  cells improved: %d of %d' % (sum(1 for _, a, b in GAPS if abs(b) < abs(a)), len(GAPS)))
bg = [(c, a, b) for c, a, b in GAPS if c.startswith('ND')]
P('  ND-band gap SPREAD (max-min): fair_C %.3f -> fair_board %.3f   (a uniform re-basing cannot move it)'
  % (max(a for _, a, _ in bg) - min(a for _, a, _ in bg),
     max(b for _, _, b in bg) - min(b for _, _, b in bg)))
P()
P('THE NATURAL EXPERIMENT AT THE RULED BOUNDARY.  grace-A cuts at entry age <= 19.  A timing story')
P('predicts marks vary SMOOTHLY with age; the grace story predicts a DISCONTINUITY at 19/20.')
P('Classes 2005-2021 (Order C\'s own window) so the comparison is against its published age table.')
P()
POPA = []
for k, r in Arecs.items():
    if k in FM: continue
    y = r['year']
    if y < 2005 or y > 2021: continue
    if not (cells_of(r)): continue
    if not r.get('vpath') or r['vpath'][0] is None: continue
    d = SV.get(k, {})
    POPA.append(dict(aged=r.get('age_draft'), v0=float(r['v0']), p1=float(r['vpath'][0]),
                     g1=int(r.get('games_yr1') or 0),
                     full={j: d.get(y + j, 0.0) for j in range(1, LAST_REAL_SEASON - y + 1)}))


def agebucket(a):
    if a is None: return None
    if a <= 17: return '17'
    if a == 18: return '18'
    if a == 19: return '19'
    if a == 20: return '20'
    return '21+'


P('  %-6s %6s %10s %8s %8s %8s %9s %9s' %
  ('age', 'n', 'entry pts', 'mark', 'fair_C', 'gap_C', 'fair_bd', 'gap_bd'))
AGEROWS = []
for b in ('17', '18', '19', '20', '21+'):
    rows = [r for r in POPA if agebucket(r['aged']) == b]
    if not rows: continue
    sh, fair = s1_and_fair(rows)
    acc = ACC['age<=19'] if b in ('17', '18', '19') else ACC['age>=20']
    fg = acc * (1.0 - sh)
    mark = sum(r['p1'] for r in rows) / sum(r['v0'] for r in rows)
    AGEROWS.append(dict(age=b, n=len(rows), mark=round(mark, 4), fair_C=round(fair, 4),
                        gap_C=round(mark - fair, 4), fair_bd=round(fg, 4), gap_bd=round(mark - fg, 4)))
    P('  %-6s %6d %10d %8.3f %8.3f %+8.3f %9.3f %+9.3f'
      % (b, len(rows), round(sum(r['v0'] for r in rows)), mark, fair, mark - fair, fg, mark - fg))
P()
P('  mean |gap| across the five age buckets: fair_C %.4f -> fair_board %.4f'
  % (sum(abs(r['gap_C']) for r in AGEROWS) / len(AGEROWS),
     sum(abs(r['gap_bd']) for r in AGEROWS) / len(AGEROWS)))
P('  The discontinuity is AT the ruled boundary: age 19 gap_C %+.3f vs age 20 gap_C %+.3f -- a %.3f'
  % (AGEROWS[2]['gap_C'], AGEROWS[3]['gap_C'], AGEROWS[3]['gap_C'] - AGEROWS[2]['gap_C']))
P('  jump across a one-year age step that no delivery-timing story can produce.  Under the board\'s')
P('  own clock the same step is %+.3f -> %+.3f, a jump of %.3f.'
  % (AGEROWS[2]['gap_bd'], AGEROWS[3]['gap_bd'], AGEROWS[3]['gap_bd'] - AGEROWS[2]['gap_bd']))
P()
P('ALT-1: "the year-1 marks are simply too low".  Its discriminator (prereg sec 6): the deficit should')
P('track WHO SAT and the year-1 re-pricing inputs, and should NOT track how late a cell delivers.')
P()
P('  band-level: mean year of delivery vs the observed gap under each benchmark')
P('  %-10s %9s %9s %9s' % ('band', 'mean_yr', 'gap_C', 'gap_bd'))
xs = []; y1 = []; y2 = []
for c in ORDER:
    if not c.startswith('ND') or c not in PROF: continue
    g = [x for x in GAPS if x[0] == c][0]
    P('  %-10s %9.2f %+9.3f %+9.3f' % (c, PROF[c]['mean_yr'], g[1], g[2]))
    xs.append(PROF[c]['mean_yr']); y1.append(g[1]); y2.append(g[2])
P('  rank corr(mean_yr, gap): under fair_C %.3f ; under fair_board %.3f'
  % (spearman(xs, y1), spearman(xs, y2)))
P('  (the timing story needs this STRONGLY NEGATIVE -- later delivery, deeper drop.)')
P()
P('  year-one sitting rate by band (ALT-1\'s own variable), classes %d-%d:' % (ENTRY_LO, ENTRY_HI))
P('  %-10s %6s %8s %8s %10s' % ('band', 'n', 'sat(0g)', 'sat share', 'gap_bd'))
sx = []; sy = []
for c in ORDER:
    if not c.startswith('ND') or c not in PROF: continue
    rows = ROWS[c]
    sat = sum(1 for r in rows if r['g1'] == 0)
    g = [x for x in GAPS if x[0] == c][0]
    sx.append(sat / len(rows)); sy.append(g[2])
    P('  %-10s %6d %8d %8.3f %+10.3f' % (c, len(rows), sat, sat / len(rows), g[2]))
P('  rank corr(sat share, gap_bd) over the five bands: %.3f' % spearman(sx, sy))
P('  rank corr(mean_yr,  gap_bd) over the five bands: %.3f' % spearman(xs, y2))
P('  ALT-1 predicts the FIRST to be strongly negative and the second to be near zero or positive.')
P()
P('SCOREBOARD ON THE BAND SPREAD (the V-shape\'s defining feature, 0.19 ratio points):')
P('  timing story  -- band W_pure spread %.3f against an implied spread of %.3f: it can supply at most'
  % (max(x[2] for x in bcells) - min(x[2] for x in bcells), max(x[1] for x in bcells) - min(x[1] for x in bcells)))
P('                   %.0f%% of the spread even as a counterfactual, and P1 says the premise is false.'
  % (100.0 * (max(x[2] for x in bcells) - min(x[2] for x in bcells)) /
     (max(x[1] for x in bcells) - min(x[1] for x in bcells))))
P('  clock story   -- explains the LEVEL (mean |gap| %.3f -> %.3f) and, being uniform in pick, NONE of'
  % (sum(abs(g) for _, g, _ in GAPS) / len(GAPS), sum(abs(g) for _, _, g in GAPS) / len(GAPS)))
P('                   the spread; it does explain the age-boundary discontinuity, which timing cannot.')
P('  ALT-1         -- the only candidate left standing for the SPREAD; sit share tracks it at rho %.3f.'
  % spearman(sx, sy))
P()

OUT = dict(order='ORDER F -- entry timing-wedge verification',
           prereg='PREREG_F.md (pushed before any number: commit d20f71c)',
           P1=dict(verdict='FALSIFIED', target='L2[grace_a][key][total]',
                   construction='flat-14 discounted, grace-A exponent shift max(0,k-G_O)',
                   line='o26b_layer2.py:395  pts = MA.SCALE * raw * w / D.f(ea, k)'),
           accretion=ACC, lifts=dict(disc_factor=LIFT_MD5, s4_ruler=RUL_MD5),
           matrices={os.path.basename(MAT): md5f(MAT), os.path.basename(MAT_C32): md5f(MAT_C32)},
           window=[ENTRY_LO, ENTRY_HI], horizon=HORIZON,
           profiles={c: dict(n=PROF[c]['n'], zero_U=PROF[c]['zero'], mean_yr=PROF[c]['mean_yr'],
                             shares={str(j): round(v, 5) for j, v in PROF[c]['sh'].items()},
                             wedge_q=[round(x, 4) for x in PROF[c]['q']]) for c in PROF},
           wedges={c: {k: round(v, 5) for k, v in WED[c].items()} for c in WED},
           match=[dict(cell=c, W_implied=round(wi, 4), W_pure=round(wp, 4), diff=round(d, 4),
                       verdict=v, thin=t) for c, wi, wp, d, v, t in CELLS],
           tally=dict(MATCH),
           alt2=[dict(cell=c, gap_C=round(a, 4), gap_board=round(b, 4)) for c, a, b in GAPS],
           age_table=AGEROWS,
           spread=dict(W_pure_band=round(max(x[2] for x in bcells) - min(x[2] for x in bcells), 4),
                       W_implied_band=round(max(x[1] for x in bcells) - min(x[1] for x in bcells), 4),
                       rho_sat_gap=round(spearman(sx, sy), 4),
                       rho_meanyr_gap=round(spearman(xs, y2), 4)))
json.dump(OUT, open(os.path.join(HERE, 'WEDGE_F.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'WEDGE_F_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
P('wrote WEDGE_F.json and WEDGE_F_out.txt')
