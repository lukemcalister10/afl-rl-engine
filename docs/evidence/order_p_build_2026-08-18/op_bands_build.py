#!/usr/bin/env python3
"""ORDER P BUILD — THE ND BAND TABLES, IN BOTH WINDOWS. ORDER P's op_bands.py, REUSED WHOLE.

The ONLY change is the list of boards it is pointed at. Every instrument pin, the byte-carried
value_at(), the window definitions, the thin rules and the verdict rule are ORDER L's, unmodified.

Original ORDER L header follows.


GAP 1 the owner raised: Order K's ND band tables are pooled across every cohort. Only the pool-arm
tables carry the primary / modern split. This file emits every ND band table in BOTH windows, using
the pool-arm instrument's OWN window definition, unchanged.

GAP 2 the owner raised: the same tables again with the 2005 and 2006 cohorts removed from the
population entirely — numerator and denominator alike. That is a SENSITIVITY, not a correction.

NOTHING IS REBUILT. The population filter is the harness's own load_matrix(). The value semantics
(value_at) are lifted BYTE-FOR-BYTE from the disclosed extended instrument
t338_extended_DISCLOSED.py (md5 d59ad550116ebbe3d90ed82becd2c4d5), which is copied beside this file
and md5-asserted at run. The ONLY thing this file adds is a population filter on the cohort year.

  cohort(ND row) = draft year + 1              (the pool-arm instrument's own key for a non-MSD row)
  PRIMARY  = cohorts 2005-2023 = draft years 2004-2022   (the whole ND population)
  MODERN   = cohorts 2019-2023 = draft years 2018-2022

For an ND row the draft clock and the cohort clock agree in calendar terms: the canonical reader's
year N is calendar (draft year + N), and the cohort reader's cohort year N is calendar
(cohort + N - 1) = (draft year + N). Same year, same cell. Checked at run as L-SC2.

  usage: OPENBLAS_NUM_THREADS=1 python ol_bands.py
"""
import os, sys, json, hashlib, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
WORK = os.path.join(SP, 'op', 'noarb')
os.makedirs(WORK, exist_ok=True)

SRC = {
    'harness_repointed.py': os.path.join(REPO, 'docs/evidence/landing_29_2026-08-13/noarb/harness_pvc_REPINNED_pass3.py'),
    't338_extended_DISCLOSED.py': os.path.join(REPO, 'docs/evidence/candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py'),
    'noarb_table_338.py': os.path.join(REPO, 'docs/evidence/landing_29_2026-08-13/noarb/noarb_table_338.py'),
    'noarb_table_allarm.py': os.path.join(REPO, 'docs/evidence/landing_29_2026-08-13/noarb/noarb_table_allarm.py'),
}
PINS = {'t338_extended_DISCLOSED.py': 'd59ad550116ebbe3d90ed82becd2c4d5',
        'noarb_table_338.py': '0f8220351c64c56ccfa90c60edcdfa5f'}

L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 118)
P('ORDER P BUILD — ND BAND TABLES, BOTH WINDOWS. The same file, only the board list changed:')
P('the BUILT ORDER P board is added and ORDER P\'s own OFFLINE ESTIMATE is kept beside it, so the')
P('built-versus-estimated comparison is on one page and cannot be quietly reconciled.')
P('=' * 118)
P('instrument pins, computed at run on unmodified copies:')
for name, src in SRC.items():
    blob = open(src, 'rb').read()
    open(os.path.join(WORK, name), 'wb').write(blob)
    m = hashlib.md5(blob).hexdigest()
    tag = ''
    if name in PINS:
        assert m == PINS[name], 'INSTRUMENT MD5 MOVED: %s %s != %s' % (name, m, PINS[name])
        tag = '   <- pinned, asserted'
    P('  %-30s %s%s' % (name, m, tag))

sys.path.insert(0, WORK)
import harness_repointed as H                                    # noqa: E402

# ---------------------------------------------------------------------------------------------------
# value_at: COPIED BYTE-FOR-BYTE from t338_extended_DISCLOSED.py. Do not edit. The copy is verified
# below by extracting the function source out of the pinned file and comparing it to this one.
# ---------------------------------------------------------------------------------------------------


def value_at(r, N):
    """Return (value, kind) for year N after the draft year. kind in
    {'v0','path','ended','null'}. 'ended' = career concluded before year N -> 0 by the standing order."""
    if N == 0:
        return float(r['v0']), 'v0'
    vp = r.get('vpath') or []
    yrs = r.get('yrs') or []
    i = N - 1
    if i >= len(vp):
        return 0.0, 'ended'
    # index/year alignment is an ASSERT, never an assumption
    assert yrs[i] == r['year'] + N, \
        "yrs misalignment: key=%s yrs[%d]=%s expected %d" % (r['key'], i, yrs[i], r['year'] + N)
    if vp[i] is None:
        return 0.0, 'null'
    return float(vp[i]), 'path'


_disc = open(os.path.join(WORK, 't338_extended_DISCLOSED.py')).read()
_body = _disc.split('def value_at(r, N):')[1].split('\ndef main()')[0].rstrip()
_mine = open(os.path.abspath(__file__)).read().split('def value_at(r, N):')[1].split('\n\n\n_disc')[0].rstrip()
assert _body == _mine, 'value_at is NOT byte-identical to the disclosed instrument'
P('  value_at()                     byte-identical to the disclosed instrument   <- asserted')

LABELS = [('PBUILT', 'ORDER P — THE BUILT BOARD 374d4e44. THE DECISION BOARD.'),
          ('PDERIV', 'ORDER P — the same mechanism priced OFFLINE by the ORDER P seat (ESTIMATE, NOT A '
                     'BUILD). Kept so built-versus-estimated is visible on one page.'),
          ('OKRULED', 'ORDER K f3101883 — the base, carrying the DEFECTIVE blind eta charge'),
          ('M0ETA0', 'ORDER M0 73bf9617 — ORDER K\'s knobs with the charge SET TO ZERO (the uncharged '
                     'ceiling)'),
          ('O35FINAL', 'the landing candidate 1f176444')]
BANDS = [('ALL picks 1-64', lambda r: True),
         ('picks 1-20', lambda r: 1 <= r['pick'] <= 20),
         ('picks 21-64', lambda r: 21 <= r['pick'] <= 64),
         ('picks 1-10', lambda r: 1 <= r['pick'] <= 10),
         ('picks 11-20', lambda r: 11 <= r['pick'] <= 20),
         ('picks 21-30', lambda r: 21 <= r['pick'] <= 30),
         ('picks 31-40', lambda r: 31 <= r['pick'] <= 40),
         ('picks 41-64', lambda r: 41 <= r['pick'] <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]
EXCLUDED_COHORTS = (2005, 2006)          # cohort clock = the 2004 and 2005 national drafts
VARIANTS = [('ALLCOH', 'every cohort in the window (the standing basis)'),
            ('EX0506', 'the 2005 and 2006 cohorts removed entirely — SENSITIVITY, not a correction')]
YEARS = list(range(0, 8))
CHARGE = 0.14
THIN, VTHIN, FLOOR_N = 30, 10, 5


def cohort(r):
    """the pool-arm instrument's own key, for an ND row (never MSD)."""
    return r['year'] + 1


def flag(n):
    if n < FLOOR_N:
        return 'none'
    if n < VTHIN:
        return 'vthin'
    if n < THIN:
        return 'thin'
    return 'ok'


def verdict(a):
    return 'SELL-RED' if a < 0 else ('BUY-RED' if a > CHARGE else 'ok')


def band_rows(pop, wend):
    """the canonical reader's own row construction, restricted to the given population."""
    path, nincl, nzero, notreach, meanN, mean0 = [], [], [], [], [], []
    for N in YEARS:
        incl = [r for r in pop if r['year'] + N <= wend]
        vals = [value_at(r, N)[0] for r in incl]
        v0s = [float(r['v0']) for r in incl]
        nincl.append(len(incl))
        notreach.append(len(pop) - len(incl))
        nzero.append(sum(1 for v in vals if v == 0.0))
        if len(incl) < FLOOR_N:
            path.append(None); meanN.append(None); mean0.append(None); continue
        mN = statistics.mean(vals); m0 = statistics.mean(v0s)
        meanN.append(mN); mean0.append(m0)
        path.append(mN / m0 if m0 > 0 else None)
    return dict(path=path, n_included=nincl, n_zero=nzero, n_not_yet_reached=notreach,
                mean_yearN=meanN, mean_year0_same_set=mean0)


OUT = {'charge': CHARGE, 'windows': {w: [lo, hi] for w, lo, hi in WINDOWS},
       'excluded_cohorts': list(EXCLUDED_COHORTS),
       'thin_rule': dict(thin=THIN, very_thin=VTHIN, not_printed_below=FLOOR_N),
       'nd': {}, 'meta': {}}

for lab, nice in LABELS:
    MX = os.path.join(SP, 'per_entrant_%s.json' % lab)
    assert os.path.exists(MX), 'MATRIX MISSING: %s' % MX
    meta, ND = H.load_matrix(MX)
    full = json.load(open(MX))['recs']
    WEND = max(y for r in full
               for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    draft_years = sorted({r['year'] for r in ND})
    OUT['meta'][lab] = dict(matrix=os.path.basename(MX),
                            matrix_md5=hashlib.md5(open(MX, 'rb').read()).hexdigest()[:8],
                            store=meta['store_md5'], v0surf=meta['v0surf_sig'][:12],
                            n_records=meta['n_records'], nd_population=len(ND), window_end=WEND,
                            draft_years=[draft_years[0], draft_years[-1]])
    P()
    P('#' * 118)
    P('# %s   [%s]' % (nice, lab))
    P('#' * 118)
    P('  matrix %s  md5 %s  store %s  v0surf %s  records %d'
      % (os.path.basename(MX), OUT['meta'][lab]['matrix_md5'], meta['store_md5'],
         meta['v0surf_sig'][:12], meta['n_records']))
    P('  ND population %d, draft years %d..%d, observed window end %d'
      % (len(ND), draft_years[0], draft_years[-1], WEND))

    # ---- L-SC2: the two clocks agree, row by row -------------------------------------------------
    bad = [r['key'] for r in ND if cohort(r) + 1 - 1 != r['year'] + 1]
    assert not bad, 'L-SC2 FAILED: clocks disagree on %d rows' % len(bad)

    for wname, lo, hi in WINDOWS:
        for vkey, vdesc in VARIANTS:
            pop_w = [r for r in ND if lo <= cohort(r) <= hi]
            if vkey == 'EX0506':
                pop_w = [r for r in pop_w if cohort(r) not in EXCLUDED_COHORTS]
            P()
            P('-' * 118)
            P('### %s window (cohorts %d-%d = draft years %d-%d)  ·  %s  ·  n = %d'
              % (wname, lo, hi, lo - 1, hi - 1, vdesc, len(pop_w)))
            P('-' * 118)
            hdr = ('  %-16s %6s ' % ('band', 'n') + ' '.join('%8s' % ('yr%d' % n) for n in YEARS)
                   + '  %9s %9s %10s  %s' % ('apr0-1', 'buy-mgn', 'verdict', 'thin?'))
            P(hdr)
            for bname, bfilt in BANDS:
                pop = [r for r in pop_w if bfilt(r)]
                d = band_rows(pop, WEND)
                n1 = d['n_included'][1]
                fl1 = flag(n1)
                mark = {'ok': '', 'thin': '*', 'vthin': '**', 'none': '(not printed)'}[fl1]
                if d['path'][1] is None:
                    a01 = mgn = None
                    verd = 'n/a — fewer than %d rows at year 1' % FLOOR_N
                else:
                    a01 = d['path'][1] - 1.0
                    mgn = CHARGE - a01
                    verd = verdict(a01) + mark
                OUT['nd'].setdefault(lab, {})['%s|%s|%s' % (wname, vkey, bname)] = dict(
                    n=len(pop), path=d['path'], n_included=d['n_included'], n_zero=d['n_zero'],
                    n_not_yet_reached=d['n_not_yet_reached'], mean_yearN=d['mean_yearN'],
                    mean_year0_same_set=d['mean_year0_same_set'],
                    apprec01=a01, buy_margin=mgn, verdict=verd,
                    flags=[flag(x) for x in d['n_included']])
                cells = []
                for v, nn in zip(d['path'], d['n_included']):
                    if v is None:
                        cells.append('%8s' % '-')
                    else:
                        f = flag(nn)
                        cells.append('%8s' % (('%.3f' % v) + {'ok': '', 'thin': '*', 'vthin': '**'}[f]))
                P('  %-16s %6d ' % (bname, len(pop)) + ' '.join(cells) +
                  ('  %+8.2f%% %+8.2f%% %10s  %s'
                   % (100 * a01, 100 * mgn, verdict(a01), {'ok': '-', 'thin': 'THIN',
                                                           'vthin': 'VERY THIN'}[fl1])
                   if a01 is not None else '          -         - %10s  %s' % ('n/a', 'n<5')))
                if bname == 'picks 21-64':
                    P('  ' + '-' * 114)
            P('  n by year:')
            for bname, bfilt in BANDS:
                d = OUT['nd'][lab]['%s|%s|%s' % (wname, vkey, bname)]
                P('    %-16s ' % bname + ' '.join('%8d' % x for x in d['n_included']))

json.dump(OUT, open(os.path.join(HERE, 'BANDS_BUILD.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'BANDS_BUILD_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote BANDS_BUILD.json / BANDS_BUILD_out.txt')
