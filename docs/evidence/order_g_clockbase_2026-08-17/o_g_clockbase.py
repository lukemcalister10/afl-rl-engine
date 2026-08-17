#!/usr/bin/env python3
# =====================================================================================================
# ORDER G -- THE CLOCK RE-BASE INSTRUMENT SEAT.  READ-ONLY.
#
# Authority: the owner's R-CLOCKBASE ruling (#334 comment 5317457543), which adopts the Order F
# derivation (docs/evidence/order_f_timing_2026-08-17/PACKET_F.md).  Rule fixed in PREREG_G.md,
# committed and pushed BEFORE any number below was computed.
#
# THIS SEAT CHANGES REPORTING, NOT PRICES.  No engine build, no board build, no store write, no law
# file touched.  Nothing here moves a single board number.
#
# PART 0  identities and lifts
# PART 1  the accretion factors, LIFTED FROM ORDER F (disc_factor exec'd verbatim, md5 asserted)
# PART 2  the house delivered-value ruler (S4), lifted by source text, and s1
# PART 3  the MARKS -- the standing instruments, re-run unchanged, with halting controls
# PART 4  T1  the re-based five-band table, three boards
# PART 5  T2  the re-based pool-arm tables, both windows, three boards
# PART 6  T3  the vantage matrix, refreshed  +  T4 the re-based leg attribution
# PART 7  the W2 class target, re-derived under the clock
# =====================================================================================================
import json, math, os, sys, hashlib, collections, statistics, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
RUN = os.path.join(SP, 'order_g')
os.makedirs(RUN, exist_ok=True)

S4SRC = os.path.join(EV, 'order32_s4_2026-08-17', 's4_shootout.py')
RLSRC = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py')
EXT_SRC = os.path.join(EV, 'candidate_31f', 'ext_2026-08-17', 't338_extended_DISCLOSED.py')
HARN = os.path.join(EV, 'landing_29_2026-08-13', 'noarb', 'harness_pvc_REPINNED_pass3.py')

BOARDS = [('D', 'O35FINAL', '1f17644445f074d11e631b5cbae98a9a', 'THE LANDING CANDIDATE (Order D wire)'),
          ('C32R', 'O32RFINAL', '7802ee977cd5e8972010b09f1bb1bee6', 'the repaired C32 (dial-off identity)'),
          ('C31', 'O31FFINAL', 'fe6be9d6ac76ebc34d26ebc11d796505', 'Candidate 31 (the 31-F head fix)')]
MATP = {t: os.path.join(SP, 'per_entrant_%s.json' % f) for t, f, _, _ in BOARDS}

CARRY = 1.14
FM = {'paddy-mccartin', 'thomas-boyd'}
F_LO, F_HI = 2005, 2019          # Order F's own window, kept as the disclosed control
BANDS5 = ['picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
WINDOWS_ND = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64']
ARMS = ['RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS']
THIN_N = 15

_OUT = []
def P(s=''):
    print(s); _OUT.append(str(s))

def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

NOTE = ('THIS SEAT CHANGES REPORTING, NOT PRICES.  No board number moves; no price is proposed. '
        'The two exploit rails keep their standing definitions.')

# =====================================================================================================
P('=' * 122)
P('ORDER G -- THE CLOCK RE-BASE INSTRUMENT SEAT.  READ-ONLY.  Rule fixed in PREREG_G.md (pushed first).')
P('=' * 122)
P('  ' + NOTE)
P()
P('  sources, md5-stamped:')
for p in (RLSRC, S4SRC, EXT_SRC, HARN):
    P('    %-62s %s' % (os.path.relpath(p, ROOT), md5f(p)))
for t, f, bh, desc in BOARDS:
    P('    %-62s %s' % ('per_entrant_%s.json  [%s]' % (f, t), md5f(MATP[t])))
P()

# ---- board identity asserts -------------------------------------------------------------------------
MX = {}
for t, f, bh, desc in BOARDS:
    D = json.load(open(MATP[t]))
    got = D['meta']['basis_29c']['replication_board']
    assert got == bh, 'board identity mismatch for %s: %s != %s' % (t, got, bh)
    assert D['meta']['store_md5'] == 'cb38ef11', 'store identity mismatch for %s' % t
    assert D['meta']['n_records'] == len(D['recs']) == 2648, 'record count mismatch for %s' % t
    MX[t] = D
    P('  board %-5s %s  store %s  head %s  n=%d   %s'
      % (t, got[:8], D['meta']['store_md5'], D['meta']['engine_head'], len(D['recs']), desc))
P('  ALL THREE ASSERTED.  Same store, so the delivered-value stream is common to all three boards;')
P('  only v0, the year-1 price, and hence the mark and the v0-weighted age mix move between columns.')
P()

# =====================================================================================================
P('=' * 122)
P('PART 1 -- THE ACCRETION FACTORS, LIFTED FROM ORDER F.  NOT RE-DERIVED.')
P('=' * 122)
P()
_src = open(RLSRC).read()
_blk = _src.split("def disc_factor(a,d,k,lens='bal',grace=0):")[1].split('\nLENS=')[0]
_blk = "def disc_factor(a,d,k,lens='bal',grace=0):" + _blk
LIFT_MD5 = hashlib.md5(_blk.encode()).hexdigest()
assert LIFT_MD5 == '93a198a86f7c832dba79e41de5146d8c', 'disc_factor lift md5 moved: %s' % LIFT_MD5
NS = dict(AGE_DISC=False, age_disc=lambda a, d, lens='bal': d, age_disc_mode=lambda: 0,
          _pw_interp=None, _V9_KNOTS=None, math=math)
exec(_blk, NS)
disc_factor = NS['disc_factor']
P('  disc_factor lifted BY SOURCE TEXT out of engine/rl_after/rl_model.py and exec\'d VERBATIM.')
P('    lifted-text md5 %s  -- ASSERTED equal to Order F\'s (93a198a8...).  PASS' % LIFT_MD5)
assert abs(disc_factor(18, 0.14, 3, 'bal', 0) - CARRY ** 3) < 1e-12
P('    control: disc_factor(18, 0.14, 3, grace=0) == 1.14^3 -> %.10f  PASS' % disc_factor(18, 0.14, 3, 'bal', 0))
P()
GO = {'age<=19': 2, 'age>=20': 0}       # curve clock, grace-A reading O (Order 28)
GE = {'age<=19': 0, 'age>=20': 0}       # engine clock at the year-1 vantage
ACC = {}
for lab in ('age<=19', 'age>=20'):
    a = 18 if lab == 'age<=19' else 21
    f0 = [1.0 / disc_factor(a, 0.14, j, 'bal', GO[lab]) for j in range(1, 8)]
    f1 = [(0.0 if j == 1 else 1.0 / disc_factor(a, 0.14, j - 2, 'bal', GE[lab])) for j in range(1, 8)]
    r = [f1[j - 1] / f0[j - 1] for j in range(2, 8)]
    assert all(abs(x - r[0]) < 1e-12 for x in r), 'accretion not uniform across surviving seasons'
    ACC[lab] = r[0]
    P('  entry %-8s : ENTRY weights %s' % (lab, ' '.join('%.5f' % x for x in f0[:5])))
    P('  %-14s   YEAR-1 weights %s   (season 1 is DELIVERED)'
      % ('', ' '.join(('%.5f' % x) if j else '  --   ' for j, x in enumerate(f1[:5]))))
    P('  %-14s   accretion yr1/entry, every surviving season: %.5f' % ('', r[0]))
assert abs(ACC['age<=19'] - 1.0) < 1e-12, 'ACC[<=19] != 1.00'
assert abs(ACC['age>=20'] - CARRY ** 2) < 1e-12, 'ACC[>=20] != 1.14^2'
P()
P('  ASSERTED: ACC[age<=19] == 1.00000 exactly ; ACC[age>=20] == 1.14^2 == %.5f.  Both PASS.' % ACC['age>=20'])
P('  These are ORDER F\'s numbers, rebuilt by F\'s own loop on F\'s own lifted disc_factor.')
P()

# =====================================================================================================
P('=' * 122)
P('PART 2 -- THE HOUSE DELIVERED-VALUE RULER (S4), LIFTED BY SOURCE TEXT; AND s1')
P('=' * 122)
P()
_s4 = open(S4SRC).read()
_rul = 'B_BOOT = 2000' + _s4.split('B_BOOT = 2000')[1].split('\nA = json.load(open(CAND_P))')[0]
RUL_MD5 = hashlib.md5(_rul.encode()).hexdigest()
assert RUL_MD5 == 'ce730ab0c5fa62da8f920c2c9ec8672c', 'S4 ruler lift md5 moved: %s' % RUL_MD5
RNS = dict(math=math, os=os, hashlib=hashlib, json=json)
exec(_rul, RNS)
BARS = RNS['BARS']; w_sqrt = RNS['w_sqrt']; season_raw = RNS['season_raw']
LAST_REAL_SEASON = RNS['LAST_REAL_SEASON']
assert set(RNS['FM']) == FM
P('  S4 ruler lifted text md5 %s -- ASSERTED equal to Order F\'s (ce730ab0...).  PASS' % RUL_MD5)
P('  BARS %s ; LAST_REAL_SEASON %d ; force-majeure %s' % (BARS, LAST_REAL_SEASON, sorted(FM)))

# the SV assembly, lifted verbatim (same block Order F lifted)
Arecs = {r['key']: r for r in MX['D']['recs']}
_sv = '# ---- per-player season values' + _s4.split('# ---- per-player season values')[1].split('\ndef dv1(')[0]
SVNS = dict(Arecs=Arecs, BARS=BARS, w_sqrt=w_sqrt, season_raw=season_raw,
            LAST_REAL_SEASON=LAST_REAL_SEASON, SV={})
exec(_sv, SVNS)
SV = SVNS['SV']
P('  SV assembly lifted verbatim (md5 %s); %d players carry a season map.'
  % (hashlib.md5(_sv.encode()).hexdigest(), len(SV)))
# the store is common to all three boards -> assert the SV stream really is identical
for t in ('C32R', 'C31'):
    rr = {r['key']: r for r in MX[t]['recs']}
    SVN2 = dict(Arecs=rr, BARS=BARS, w_sqrt=w_sqrt, season_raw=season_raw,
                LAST_REAL_SEASON=LAST_REAL_SEASON, SV={})
    exec(_sv, SVN2)
    assert SVN2['SV'] == SV, 'delivered-value stream differs on %s' % t
P('  ASSERTED: the delivered-value stream is BYTE-IDENTICAL across D / C32R / C31 (same store).')
P('  So s1 is the SAME number in every board column; only the mark and the v0-weighted age mix move.')
P()

# age coverage
for t, _, _, _ in BOARDS:
    miss = sum(1 for r in MX[t]['recs'] if r.get('age_draft') is None)
    assert miss == 0, 'age_draft nulls on %s: %d' % (t, miss)
P('  entry-age field: age_draft.  Nulls on each board: 0 / 0 / 0.  ASSERTED complete.')
P('  Boundary: age_draft <= 19 -> accretion %.5f ; age_draft >= 20 -> accretion %.5f.'
  % (ACC['age<=19'], ACC['age>=20']))
P('  This is the RULED grace-A boundary (Order 28, reading O), not a fitted cut.')
P()


def prof_of(key, entry_year):
    """Order F's per-player delivered profile: {j: value of season entry_year + j}."""
    d = SV.get(key, {})
    return {j: d.get(entry_year + j, 0.0) for j in range(1, LAST_REAL_SEASON - entry_year + 1)}


def s1_of(rows):
    """ORDER C's own construction, reproduced by Order F verbatim (o_f_wedge.py:361-370):
       sv1 = the first post-entry season; dv1 = later seasons discounted to the YEAR-1 clock at 1.14;
       s1 = sv1 / (sv1 + dv1), pooled (value-weighted) at the cell."""
    sv1 = 0.0; dv1 = 0.0
    for r in rows:
        f = r['full']
        sv1 += f.get(1, 0.0)
        dv1 += sum(v * CARRY ** -(j - 1) for j, v in f.items() if j >= 2)
    if sv1 + dv1 <= 0:
        return float('nan'), float('nan')
    return sv1 / (sv1 + dv1), dv1


def accmix(rows, weight='v0'):
    """v0-weighted (default) entry-age accretion mix -- Order F's ALT-2 weighting (o_f_wedge.py:467-471).
       Returns (acc_mix, share_le19, n_le19, n)."""
    if weight == 'v0':
        w = [max(0.0, float(r['v0'])) for r in rows]
    else:
        w = [1.0] * len(rows)
    tot = sum(w)
    if tot <= 0:
        return float('nan'), float('nan'), 0, len(rows)
    le = [1.0 if (r['aged'] is not None and r['aged'] <= 19) else 0.0 for r in rows]
    acc = sum(wi * (ACC['age<=19'] if l else ACC['age>=20']) for wi, l in zip(w, le)) / tot
    sh = sum(wi * l for wi, l in zip(w, le)) / tot
    return acc, sh, int(sum(le)), len(rows)


def exact_clock_ratio(rows):
    """The exactly-clock-consistent object PREREG_G S2.5 names: sum_i Y1_i / sum_i E_i, where
       E_i weights the entrant's delivered stream on the ENTRY clock (grace-A) and Y1_i on the
       ENGINE clock at the year-1 vantage.  Delivered-value weighted, printed as a CONTROL."""
    E = 0.0; Y = 0.0
    for r in rows:
        g = 2 if (r['aged'] is not None and r['aged'] <= 19) else 0
        a = 18 if g == 2 else 21
        for j, v in r['full'].items():
            E += v / disc_factor(a, 0.14, j, 'bal', g)
            if j >= 2:
                Y += v / disc_factor(a, 0.14, j - 2, 'bal', 0)
    return (Y / E) if E > 0 else float('nan')


def rails(m):
    """The two ABSOLUTE exploit rails.  Definitions UNCHANGED by the re-base (the ruling says so)."""
    return ('RED' if m < 1.00 else 'ok', 'RED' if m > 1.14 else 'ok')


def bench(rows):
    """The full clock-fair reading for a cell."""
    s1, _ = s1_of(rows)
    acc, sh19, n19, n = accmix(rows, 'v0')
    accn, sh19n, _, _ = accmix(rows, 'n')
    return dict(n=n, s1=s1, acc=acc, share_le19=sh19, n_le19=n19,
                acc_headcount=accn, share_le19_headcount=sh19n,
                fair_G=acc * (1.0 - s1), fair_C=CARRY * (1.0 - s1),
                exact=exact_clock_ratio(rows))


# =====================================================================================================
P('=' * 122)
P('PART 3 -- THE MARKS.  THE STANDING INSTRUMENTS, RE-RUN UNCHANGED.')
P('=' * 122)
P()
P('  extended-338 five-band instrument md5 %s (the owner\'s disclosed copy)' % md5f(EXT_SRC))
P('  harness md5 %s (must begin 02dcf28c)' % md5f(HARN))
assert md5f(HARN).startswith('02dcf28c')
shutil.copy(HARN, os.path.join(RUN, 'harness_repointed.py'))
_txt = open(EXT_SRC).read()
OLD = "    jp = os.path.join(HERE, 'noarb_table_338_EXT.json')"
NEW = "    jp = os.path.join(HERE, 'noarb_table_338_EXT_%s.json' % os.environ.get('O32R_TAG','x'))"
assert _txt.count(OLD) == 1
_asrun = _txt.replace(OLD, NEW)
open(os.path.join(RUN, 't338_ext.py'), 'w').write(_asrun)
P('  THE ONE EDIT to the disclosed copy: output filename tagged per matrix (identical to Order D\'s')
P('  handling, o35_noarb.py:46-51); as-run md5 %s' % hashlib.md5(_asrun.encode()).hexdigest())
ENV = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')
EXT = {}
for t, _, _, _ in BOARDS:                       # SEQUENTIAL, one process at a time
    env = dict(ENV, O32R_TAG=t)
    r = subprocess.run([sys.executable, os.path.join(RUN, 't338_ext.py'), MATP[t]],
                       capture_output=True, text=True, env=env, cwd=RUN)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-3000:] + r.stderr[-3000:])
        raise SystemExit('extended 338 failed on %s' % t)
    open(os.path.join(HERE, 't338G_%s_console.txt' % t), 'w').write(r.stdout)
    EXT[t] = json.load(open(os.path.join(RUN, 'noarb_table_338_EXT_%s.json' % t)))
P('  three extended-338 runs completed, sequentially, thread-pinned.')

# ---- HALTING CONTROLS ------------------------------------------------------------------------------
PREV_D = json.load(open(os.path.join(EV, 'order_d_2026-08-17', 'NOARB_D.json')))
dev = 0
for g, tb in PREV_D['five_band'].items():
    rw = {x['N']: x['ratio_meanN_over_mean0'] for x in EXT['D']['groups'][g]['rows']}
    if abs((rw[1] / rw[0] - 1.0) - tb['r32']) > 1e-9:
        dev += 1
    rwc = {x['N']: x['ratio_meanN_over_mean0'] for x in EXT['C32R']['groups'][g]['rows']}
    if abs((rwc[1] / rwc[0] - 1.0) - tb['c31']) > 1e-9:
        dev += 1
P('  CONTROL 1: the re-run reproduces NOARB_D.json\'s own five-band yr0->1 numbers for BOTH the')
P('             Order-D and the C32R columns -- %s' % ('EXACT (0 deviations)' if dev == 0 else 'FAIL %d' % dev))
assert dev == 0
PREV_32 = json.load(open(os.path.join(EV, 'order_a_2026-08-17', 'NOARB_32R.json')))
dev2 = 0
for g, tb in PREV_32['five_band'].items():
    rw = {x['N']: x['ratio_meanN_over_mean0'] for x in EXT['C31']['groups'][g]['rows']}
    if abs((rw[1] / rw[0] - 1.0) - tb['c31']) > 1e-9:
        dev2 += 1
P('  CONTROL 2: the C31 re-run reproduces NOARB_32R.json\'s committed C31 five-band numbers -- %s'
  % ('EXACT (0 deviations)' if dev2 == 0 else 'FAIL %d' % dev2))
assert dev2 == 0
P()


# ---- the ND band populations, matched to the mark's own year-1 cell ---------------------------------
sys.path.insert(0, RUN)
import harness_repointed as H

GROUPS = [('ALL picks 1-64', lambda r: True),
          ('picks 1-20', lambda r: 1 <= r['pick'] <= 20),
          ('picks 21-64', lambda r: 21 <= r['pick'] <= 64),
          ('picks 1-10', lambda r: 1 <= r['pick'] <= 10),
          ('picks 11-20', lambda r: 11 <= r['pick'] <= 20),
          ('picks 21-30', lambda r: 21 <= r['pick'] <= 30),
          ('picks 31-40', lambda r: 31 <= r['pick'] <= 40),
          ('picks 41-64', lambda r: 41 <= r['pick'] <= 64)]


def nd_rows(t):
    """The extended-338 instrument's OWN year-1 population, per group, on board t."""
    _meta, ND = H.load_matrix(MATP[t])
    full = MX[t]['recs']
    WEND = max(y for r in full
               for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    out = {}
    for gname, gf in GROUPS:
        pop = [r for r in ND if gf(r)]
        incl = [r for r in pop if r['year'] + 1 <= WEND]      # the mark's own inclusion rule at N=1
        out[gname] = [dict(key=r['key'], y=r['year'], aged=r.get('age_draft'), v0=float(r['v0']),
                           full=prof_of(r['key'], r['year'])) for r in incl]
    return out, WEND


NDROWS = {}
for t, _, _, _ in BOARDS:
    NDROWS[t], WEND_T = nd_rows(t)
P('  ND benchmark population = the extended-338 instrument\'s OWN year-1 included set')
P('    (harness filter: teaches_curve & pick 1..64 & year %d..%d ; then draft_year + 1 <= %d).'
  % (H.YR_LO, H.CLASS_CUT, WEND_T))
P('  Benchmark and mark therefore stand on ONE population -- no cell is judged against a benchmark')
P('  built on a different set of players.')
P()


# ---- the pool-arm populations, matched to the all-arm reader's own year-1 cell ----------------------
def arm_paths(t, years=list(range(0, 9))):
    """Lifted verbatim from o35_noarb.py:77-124, with the year-1 row POPULATION also returned."""
    R = MX[t]['recs']
    WINDOW_END = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

    def cohort(r):
        y = r.get('year')
        if y is None: return None
        return y if r.get('type') == 'MSD' else y + 1

    def value_at(r, N):
        if N == 0:
            return float(r['v0']), 'v0'
        Y = cohort(r) + N - 1
        yrs = r.get('yrs') or []
        vp = r.get('vpath') or []
        if not yrs: return 0.0, 'ended'
        if Y < yrs[0]: return None, 'pre'
        if Y > yrs[-1]: return 0.0, 'ended'
        i = yrs.index(Y)
        if vp[i] is None: return 0.0, 'null'
        return float(vp[i]), 'path'

    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
    WINDOWS = [('PRIMARY 2005-2023', 2005, 2023), ('MODERN 2019-2023', 2019, 2023)]
    outw = {}; popw = {}
    for wname, lo, hi in WINDOWS:
        pop = [r for r in elig if lo <= cohort(r) <= hi]
        grp = {}; pg = {}
        sels = [(a, [r for r in pop if r['type'] == a]) for a in ARMS]
        sels.append(('ALLPOOL', [r for r in pop if r.get('is_pool')]))
        for nm, sub in sels:
            rows = {}
            for N in years:
                reached = sub if N == 0 else [r for r in sub if cohort(r) + N - 1 <= WINDOW_END]
                vals, v0s, npre, keep = [], [], 0, []
                for r in reached:
                    v, k = value_at(r, N)
                    if k == 'pre':
                        npre += 1; continue
                    vals.append(v); v0s.append(float(r['v0'])); keep.append(r)
                if vals:
                    rows[N] = dict(n=len(vals), n_pre=npre,
                                   ratio=statistics.mean(vals) / statistics.mean(v0s))
                    if N == 1:
                        pg[nm] = [dict(key=r['key'], y=r['year'], aged=r.get('age_draft'),
                                       v0=float(r['v0']), full=prof_of(r['key'], r['year']))
                                  for r in keep]
            grp[nm] = dict(n=len(sub), rows=rows)
        outw[wname] = grp; popw[wname] = pg
    return outw, popw


ARMP = {}; ARMPOP = {}
for t, _, _, _ in BOARDS:
    ARMP[t], ARMPOP[t] = arm_paths(t)
P('  Pool-arm benchmark population = the all-arm reader\'s OWN year-1 cell, per window, with the')
P('  n_pre rows excluded exactly as the standing instrument excludes them (never zeroed, always')
P('  counted).  MSD has no year-1 cell in either window and therefore receives no benchmark.')
P()

# =====================================================================================================
P('=' * 122)
P('PART 4 -- T1: THE RE-BASED FIVE-BAND STANDING TABLE.  THREE READINGS PER CELL.')
P('=' * 122)
P()
P('  ' + NOTE)
P()
P('  fair_G = (v0-weighted entry-age accretion mix) x (1 - s1).   accretion 1.0000 for entry age <=19,')
P('  %.4f for >=20 -- the board\'s OWN ruled grace clock, read off its own disc_factor.' % ACC['age>=20'])
P('  fair_C = 1.14 x (1 - s1) is the OLD flat ruler, printed so the move is visible.')
P('  The two RAIL columns are the ABSOLUTE exploit tests and are UNCHANGED by the re-base.')
P()

T1 = {}
for t, _, bh, desc in BOARDS:
    P('-' * 122)
    P('BOARD %s  [%s]  -- %s' % (t, bh[:8], desc))
    P('-' * 122)
    P('  %-15s %5s %9s | %7s %8s | %8s %8s | %8s %8s | %6s %6s'
      % ('cell', 'n', 'mark', 'sh<=19', 'acc_mix', 'fair_G', 'gap_G', 'fair_C', 'gap_C', 'SELL', 'BUY'))
    T1[t] = {}
    for g in WINDOWS_ND + BANDS5:
        rw = {x['N']: x['ratio_meanN_over_mean0'] for x in EXT[t]['groups'][g]['rows']}
        m = rw[1] / rw[0]
        b = bench(NDROWS[t][g])
        s, bu = rails(m)
        T1[t][g] = dict(mark=m, apprec=m - 1.0, sell=s, buy=bu, path={N: rw[N] for N in rw}, **b)
        P('  %-15s %5d %+8.2f%% | %7.3f %8.4f | %8.4f %+8.4f | %8.4f %+8.4f | %6s %6s'
          % (g, b['n'], 100 * (m - 1.0), b['share_le19'], b['acc'],
             b['fair_G'], m - b['fair_G'], b['fair_C'], m - b['fair_C'], s, bu))
    P()
P('  READING: gap_G is the CLOCK-FAIR GAP -- mark minus the board\'s own ruled benchmark.  It is a')
P('  FAIRNESS reading and carries no RED of its own.  SELL/BUY are the absolute exploit rails.')
P()

# controls for T1
P('  CONTROLS on the benchmark (Order-D column):')
P('    %-15s %9s %9s %9s %9s %9s'
  % ('cell', 's1(prim)', 's1(F wdw)', 'fairG(F)', 'exact', 'acc(head)'))
CTRL1 = {}
for g in WINDOWS_ND + BANDS5:
    rowsF = [r for r in NDROWS['D'][g] if F_LO <= r['y'] <= F_HI]
    bF = bench(rowsF)
    b = T1['D'][g]
    CTRL1[g] = dict(s1_primary=b['s1'], s1_Fwindow=bF['s1'], fairG_Fwindow=bF['fair_G'],
                    exact_primary=b['exact'], acc_headcount=b['acc_headcount'])
    P('    %-15s %9.4f %9.4f %9.4f %9.4f %9.4f'
      % (g, b['s1'], bF['s1'], bF['fair_G'], b['exact'], b['acc_headcount']))
P('    s1(F wdw) = Order F\'s own entry window 2005-2019.  Later classes are right-censored on the')
P('    delivered ruler, which OVERSTATES s1 and so UNDERSTATES fair_G; both columns printed.')
P('    exact = the exactly-clock-consistent ratio of PREREG_G S2.5 (delivered-value weighted).')
P()

# =====================================================================================================
P('=' * 122)
P('PART 5 -- T2: THE RE-BASED POOL-ARM TABLES.  BOTH WINDOWS, THREE BOARDS.')
P('=' * 122)
P()
P('  ' + NOTE)
P('  MSD caption, carried unchanged: a mid-season draftee debuts in the SAME year he is drafted, but')
P('  the matrix stores his seasons starting the year after; his true first-season cell cannot be read')
P('  from this matrix, so those rows are EXCLUDED from that one year and COUNTED (n_pre) -- never')
P('  scored zero, never printed blank.  Mid-year entrants keep age_draft as stored (Order F\'s')
P('  construction); this is a disclosed choice point.')
P('  Any arm with n < %d in the window is printed THIN and carries NO clock-fair verdict; the two' % THIN_N)
P('  exploit rails still print, as they always have.')
P()
T2 = {}
for t, _, bh, desc in BOARDS:
    T2[t] = {}
    for wname in ('PRIMARY 2005-2023', 'MODERN 2019-2023'):
        P('-' * 122)
        P('BOARD %s [%s]  --  %s' % (t, bh[:8], wname))
        P('  %-10s %5s %9s %6s | %7s %8s | %8s %8s | %8s %8s | %6s %6s %6s'
          % ('arm', 'n', 'mark', 'n_pre', 'sh<=19', 'acc_mix', 'fair_G', 'gap_G', 'fair_C', 'gap_C',
             'SELL', 'BUY', 'thin?'))
        T2[t][wname] = {}
        grp = ARMP[t][wname]
        for nm in ARMS + ['ALLPOOL']:
            d = grp[nm]
            rows = d['rows']
            if 1 not in rows or 0 not in rows:
                P('  %-10s %5d | (window has no year-1 cell -- every row is n_pre)' % (nm, d['n']))
                T2[t][wname][nm] = dict(n=d['n'], no_year1=True)
                continue
            m = rows[1]['ratio'] / rows[0]['ratio']
            pop = ARMPOP[t][wname][nm]
            b = bench(pop)
            s, bu = rails(m)
            thin = b['n'] < THIN_N
            T2[t][wname][nm] = dict(mark=m, apprec=m - 1.0, n_pre=rows[1]['n_pre'],
                                    sell=s, buy=bu, thin=thin,
                                    path={N: rows[N]['ratio'] for N in rows}, **b)
            P('  %-10s %5d %+8.2f%% %6d | %7.3f %8.4f | %8.4f %+8.4f | %8.4f %+8.4f | %6s %6s %6s'
              % (nm, b['n'], 100 * (m - 1.0), rows[1]['n_pre'], b['share_le19'], b['acc'],
                 b['fair_G'], m - b['fair_G'], b['fair_C'], m - b['fair_C'], s, bu,
                 'THIN' if thin else ''))
        P()
P('  THE TWO ALL-ARM WINDOWS are the ALLPOOL rows above -- PRIMARY 2005-2023 and MODERN 2019-2023.')
P()

# =====================================================================================================
P('=' * 122)
P('PART 6 -- T3: THE VANTAGE MATRIX, REFRESHED.  T4: THE RE-BASED LEG ATTRIBUTION.')
P('=' * 122)
P()
P('  DIAGNOSTIC ONLY (standing amendment A2: nothing was calibrated toward this).')
P('  The carry columns 1.14^k are UNCHANGED: from the year-1 vantage the grace is exhausted and the')
P('  two clocks agree (PACKET_F S5, P4), so those legs were already benchmarked correctly.')
P('  Only the yr-1 CAPTION is re-based.')
P()
VM = {}
for g in BANDS5:
    rw = T1['D'][g]['path']
    b = T1['D'][g]
    VM[g] = {}
    gG = b['mark'] - b['fair_G']
    P('  %s   (mark %.3f | clock-fair %.3f, gap %+.3f | OLD flat-1.14 fair %.3f, gap %+.3f)'
      % (g, b['mark'], b['fair_G'], gG, b['fair_C'], b['mark'] - b['fair_C']))
    P('    %-10s %10s %10s %10s %10s | carry: 1.14 1.30 1.48 1.69' % ('vantage', 'k=1', 'k=2', 'k=3', 'k=4'))
    for V in (0, 1, 2):
        cells = []
        for k in (1, 2, 3, 4):
            gr = rw[V + k] / rw[V]
            VM[g]['V%d_k%d' % (V, k)] = gr
            cells.append('%9.3f%s' % (gr, '*' if (gr < 1.0 or gr > CARRY ** k * 1.10) else ' '))
        P('    yr %-7d %s' % (V, ' '.join(cells)))
    P()
SPV = {}
for V in (0, 1, 2):
    for k in (1, 2, 3, 4):
        vals = [VM[g]['V%d_k%d' % (V, k)] for g in BANDS5]
        SPV['V%d_k%d' % (V, k)] = max(vals) - min(vals)
P('  band-vs-band spread of forward growth (max band minus min band):')
P('    %-8s %8s %8s %8s %8s' % ('vantage', 'k=1', 'k=2', 'k=3', 'k=4'))
for V in (0, 1, 2):
    P('    yr %-5d %8.3f %8.3f %8.3f %8.3f'
      % (V, SPV['V%d_k1' % V], SPV['V%d_k2' % V], SPV['V%d_k3' % V], SPV['V%d_k4' % V]))
P()
P('  T4 -- WHERE EACH BAND\'S INCONSISTENCY LIVES, RE-BASED (yr-1 leg vs the CLOCK-fair mark):')
T4 = {}
for g in BANDS5:
    b = T1['D'][g]
    rw = b['path']
    g15 = rw[5] / rw[1]
    T4[g] = dict(yr1_leg_G=b['mark'] - b['fair_G'], yr1_leg_C=b['mark'] - b['fair_C'],
                 later_leg=g15 - CARRY ** 4, growth_1_5=g15)
    P('    %-14s yr1 leg %+0.3f (was %+0.3f on the flat ruler) . later-years leg (yr1->5 growth %.3f '
      'vs carry %.3f) %+0.3f' % (g, T4[g]['yr1_leg_G'], T4[g]['yr1_leg_C'], g15, CARRY ** 4,
                                 T4[g]['later_leg']))
P()
P('  The later-years leg is UNTOUCHED by this seat -- it never depended on the entry clock.')
P()

# =====================================================================================================
P('=' * 122)
P('PART 7 -- THE W2 CLASS TARGET, RE-DERIVED UNDER THE CLOCK')
P('=' * 122)
P()
P('  ' + NOTE)
P()
P('  The band [1.100, 1.117] was built on the FLAT identity  R* = 1.14 x (1 - SV1sh).')
P('  Under the clock the identity becomes  R* = acc_mix x (1 - SV1sh), acc_mix the v0-weighted')
P('  entry-age accretion mix of the class.  Object, class set, population and ruler are W2\'s own;')
P('  the ONLY thing that changes is the benchmark.')
P()
import numpy as np

W2MAT = MATP['C31']            # the registered W2 object
W2rec = {r['key']: r for r in MX['C31']['recs']}
ENTRY_FLOOR = 2005


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        return t if t in ('RD', 'MSD') else 'OTHERPOOL'
    return None


def dv_full(k, Y):
    return sum((CARRY ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


POP = []
for k, r in W2rec.items():
    if k in FM: continue
    if arm_of(r) is None: continue
    yr = r['year']
    if yr < ENTRY_FLOOR or yr > 2021: continue
    assert r['vpath'] and r['vpath'][0] is not None, 'missing year-1 vantage: ' + k
    POP.append(dict(key=k, yr=yr, aged=r.get('age_draft'), v0=float(r['v0']),
                    p1=float(r['vpath'][0]), sv1=SV[k].get(yr + 1, 0.0),
                    dv0=dv_full(k, yr), dv1=dv_full(k, yr + 1),
                    full=prof_of(k, yr)))
P('  population: %d players, classes 2005-2021, all-arm (W2\'s own filter).' % len(POP))
P()

W2PUB = {2005: 1.1161, 2006: 1.1198, 2007: 1.1086, 2008: 1.1020, 2009: 1.0692, 2010: 1.0998,
         2011: 1.0978, 2012: 1.1165, 2013: 1.1329, 2014: 1.1288, 2015: 1.1038, 2016: 1.1130,
         2017: 1.1014, 2018: 1.1012, 2019: 1.0968, 2020: 1.1214, 2021: 1.0532}
P('  %-6s %5s %9s %9s %9s %8s %9s %9s %9s %9s'
  % ('class', 'n', 'R_cand', 'R*flat', 'SV1sh', 'sh<=19', 'acc_mix', 'R*CLOCK', 'exact', 'acc(head)'))
CLS = []
devw = 0
for y in range(2005, 2022):
    rows = [p for p in POP if p['yr'] == y]
    P0 = sum(p['v0'] for p in rows); P1 = sum(p['p1'] for p in rows)
    DV0 = sum(p['dv0'] for p in rows); DV1 = sum(p['dv1'] for p in rows)
    SV1 = sum(p['sv1'] for p in rows)
    rflat = DV1 / DV0
    sv1sh = SV1 / (SV1 + DV1)
    acc, sh19, _, _ = accmix(rows, 'v0')
    accn, sh19n, _, _ = accmix(rows, 'n')
    rclock = acc * (1.0 - sv1sh)
    ex = exact_clock_ratio(rows)
    if abs(round(rflat, 4) - W2PUB[y]) > 1e-4:
        devw += 1
    CLS.append(dict(cls=y, n=len(rows), R_cand=P1 / P0, R_flat=rflat, SV1sh=sv1sh,
                    share_le19=sh19, acc_mix=acc, R_clock=rclock, exact=ex,
                    acc_headcount=accn, R_clock_headcount=accn * (1.0 - sv1sh)))
    P('  %-6d %5d %9.4f %9.4f %9.4f %8.3f %9.4f %9.4f %9.4f %9.4f'
      % (y, len(rows), P1 / P0, rflat, sv1sh, sh19, acc, rclock, ex, accn))
P()
P('  CONTROL 3: R*flat reproduces PACKET_W2\'s published per-class R*full column -- %s'
  % ('EXACT on all 17 classes' if devw == 0 else 'FAIL %d classes' % devw))
assert devw == 0, 'R*flat does not reproduce W2'
P('  CONTROL 4: the flat identity 1.14 x (1 - SV1sh) reproduces R*flat to %.2e'
  % max(abs(CARRY * (1 - c['SV1sh']) - c['R_flat']) for c in CLS))
P()

WELL = [c for c in CLS if c['cls'] <= 2015]
RNG = np.random.default_rng(33)


def cls_boot(vals):
    v = np.array(vals, dtype=float)
    idx = RNG.integers(0, len(v), size=(2000, len(v)))
    m = v[idx].mean(axis=1)
    return [float(np.percentile(m, 5)), float(np.percentile(m, 95))]


def summ(vals):
    v = np.array(vals, dtype=float)
    return dict(n=len(v), mean=float(v.mean()), median=float(np.median(v)),
                lo=float(v.min()), hi=float(v.max()))


S_flat = summ([c['R_flat'] for c in WELL]); CI_flat = cls_boot([c['R_flat'] for c in WELL])
S_clk = summ([c['R_clock'] for c in WELL]); CI_clk = cls_boot([c['R_clock'] for c in WELL])
S_ex = summ([c['exact'] for c in WELL]); CI_ex = cls_boot([c['exact'] for c in WELL])
S_hd = summ([c['R_clock_headcount'] for c in WELL]); CI_hd = cls_boot([c['R_clock_headcount'] for c in WELL])
S_cand = summ([c['R_cand'] for c in WELL])
CAND_ALL = summ([c['R_cand'] for c in CLS])

P('  THE 2005-2015 CLASS MEAN (W2\'s own estimator; class bootstrap B=2000, seed 33):')
P('    %-34s mean %.4f  median %.4f  range [%.4f, %.4f]  90%% CI [%.4f, %.4f]'
  % ('OLD, flat-1.14 ruler', S_flat['mean'], S_flat['median'], S_flat['lo'], S_flat['hi'], CI_flat[0], CI_flat[1]))
P('    %-34s mean %.4f  median %.4f  range [%.4f, %.4f]  90%% CI [%.4f, %.4f]'
  % ('NEW, CLOCK ruler (PRIMARY)', S_clk['mean'], S_clk['median'], S_clk['lo'], S_clk['hi'], CI_clk[0], CI_clk[1]))
P('    %-34s mean %.4f  median %.4f  range [%.4f, %.4f]  90%% CI [%.4f, %.4f]'
  % ('control: exact clock ratio', S_ex['mean'], S_ex['median'], S_ex['lo'], S_ex['hi'], CI_ex[0], CI_ex[1]))
P('    %-34s mean %.4f  median %.4f  range [%.4f, %.4f]  90%% CI [%.4f, %.4f]'
  % ('control: head-count age mix', S_hd['mean'], S_hd['median'], S_hd['lo'], S_hd['hi'], CI_hd[0], CI_hd[1]))
P()
P('    candidate class marks R_cand 2005-2015: mean %.4f  median %.4f  range [%.4f, %.4f]'
  % (S_cand['mean'], S_cand['median'], S_cand['lo'], S_cand['hi']))
P('    candidate class marks R_cand all 17   : mean %.4f  median %.4f  range [%.4f, %.4f]'
  % (CAND_ALL['mean'], CAND_ALL['median'], CAND_ALL['lo'], CAND_ALL['hi']))
P()
LAND = 1.042
lo, hi = CI_clk
where = 'INSIDE' if lo <= LAND <= hi else ('BELOW' if LAND < lo else 'ABOVE')
P('  THE CORRECTED CLASS TARGET BAND: [%.4f, %.4f]   (was [1.100, 1.117])' % (lo, hi))
P('  The landing candidate\'s class number 1.042 sits %s it.  Distance to the near edge: %+.4f'
  % (where, (LAND - lo) if LAND < lo else ((LAND - hi) if LAND > hi else 0.0)))
P('  Old shortfall vs the old band: %+.4f.  New shortfall vs the new band: %+.4f.'
  % (LAND - 1.100, (LAND - lo) if LAND < lo else 0.0))
P()
# per-board acc_mix sensitivity: the v0 weights differ between boards
P('  acc_mix sensitivity across the three boards (2005-2015 class mean of acc_mix):')
for t, _, bh, _ in BOARDS:
    rr = {r['key']: r for r in MX[t]['recs']}
    vals = []
    for y in range(2005, 2016):
        rows = [dict(aged=p['aged'], v0=float(rr[p['key']]['v0'])) for p in POP if p['yr'] == y]
        vals.append(accmix(rows, 'v0')[0])
    P('    %-6s [%s]  acc_mix mean %.4f  ->  target mean %.4f'
      % (t, bh[:8], sum(vals) / len(vals),
         sum(v * (1 - c['SV1sh']) for v, c in zip(vals, WELL)) / len(vals)))
P()

# =====================================================================================================
P('=' * 122)
P('SUMMARY OF THE RE-BASE')
P('=' * 122)
P()
allcells = []
for g in BANDS5:
    b = T1['D'][g]
    allcells.append((g, b['mark'], b['fair_C'], b['fair_G'], b['sell'], b['buy'], False))
for nm in ARMS + ['ALLPOOL']:
    d = T2['D']['PRIMARY 2005-2023'][nm]
    if d.get('no_year1'): continue
    allcells.append((nm + ' (primary)', d['mark'], d['fair_C'], d['fair_G'], d['sell'], d['buy'], d['thin']))
d = T2['D']['MODERN 2019-2023']['ALLPOOL']
allcells.append(('ALLPOOL (modern)', d['mark'], d['fair_C'], d['fair_G'], d['sell'], d['buy'], d['thin']))
nimp = sum(1 for c in allcells if abs(c[1] - c[3]) < abs(c[1] - c[2]))
P('  cells whose |gap| improves under the clock ruler: %d of %d' % (nimp, len(allcells)))
flips = [c[0] for c in allcells if (c[1] - c[2]) < 0 <= (c[1] - c[3])]
P('  cells that flip from SHORT (under the old flat ruler) to AT-OR-OVER (under the clock): %s'
  % (', '.join(flips) if flips else 'none'))
worse = [c[0] for c in allcells if abs(c[1] - c[3]) > abs(c[1] - c[2])]
P('  cells that get WORSE under the correction: %s' % (', '.join(worse) if worse else 'none'))
reds = [c[0] for c in allcells if (c[4] == 'RED' or c[5] == 'RED') and (c[1] - c[3]) < 0 and not c[6]]
P('  cells RED on a rail AND still short of the clock-fair benchmark (n >= %d): %s'
  % (THIN_N, ', '.join(reds) if reds else 'none'))
P()
P('  ' + NOTE)
P()

json.dump(dict(order='ORDER G -- clock re-base instrument seat (reporting only; no price moves)',
               note=NOTE,
               accretion=ACC, lifts=dict(disc_factor=LIFT_MD5, s4_ruler=RUL_MD5),
               boards={t: bh for t, _, bh, _ in BOARDS},
               five_band=T1, five_band_controls=CTRL1, pool_arms=T2,
               vantage_matrix_D=VM, vantage_spread_D=SPV, leg_attribution_D=T4,
               controls=dict(ext_reproduces_NOARB_D=True, ext_reproduces_NOARB_32R=True,
                             sv_identical_across_boards=True, rstar_flat_reproduces_W2=True),
               thin_n=THIN_N),
          open(os.path.join(HERE, 'CLOCKBASE_G.json'), 'w'), indent=1, sort_keys=True, default=float)

json.dump(dict(order='ORDER G -- the W2 class target re-derived under the clock benchmark',
               object='per_entrant_O31FFINAL.json (the registered W2 matrix)',
               old_band=[1.100, 1.117], old_construction='fair = 1.14 x (1 - SV1sh)',
               new_construction='fair = v0-weighted entry-age accretion mix x (1 - SV1sh)',
               per_class=CLS,
               well_observed=dict(flat=dict(summary=S_flat, ci90=CI_flat),
                                  clock=dict(summary=S_clk, ci90=CI_clk),
                                  exact_control=dict(summary=S_ex, ci90=CI_ex),
                                  headcount_control=dict(summary=S_hd, ci90=CI_hd),
                                  candidate=S_cand),
               corrected_band=CI_clk, landing_candidate_class=LAND, verdict_where=where),
          open(os.path.join(HERE, 'W2_TARGET_G.json'), 'w'), indent=1, sort_keys=True, default=float)

open(os.path.join(HERE, 'CLOCKBASE_G_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
print('\nwritten: CLOCKBASE_G.json / W2_TARGET_G.json / CLOCKBASE_G_out.txt / t338G_*_console.txt')
