# ==================================================================================================
# B-RAW CARRY. This file is docs/evidence/staircase_fix_2026-08-20/sfx_noarb_bands.py, byte-carried by
# build_braw_instruments.py with three declared changes and nothing else: (1) SFXBRAW
# (RL_O44_LVLMONO=smooth = VARIANT B RAW, THE ADOPTED ARM) added to the label/candidate lists;
# (2) the output basenames suffixed _BRAW so this set cannot overwrite or be confused with the
# pricing seat's committed artifacts; (3) SRC introduced for the inputs carried from that seat
# (DAY0_SFXBASE.json and the EMIT_*_out.txt logs) rather than regenerated here.
# The pricing seat named this leg open in PACKET_STAIRCASE.md section 0. This closes it.
# ==================================================================================================
#!/usr/bin/env python3
"""ORDER 44 MEASUREMENT — THE ND BAND TABLES, BOTH WINDOWS, ON BOTH CONSERVED CANDIDATES.

d8_noarb_bands.py carried with FOUR declared changes and NOTHING ELSE:

  (1) LABELS: TWO candidates rather than one — SFXACON (RL_O44_LVLMONO=ratchet+conserve) and
      SFXBCON (RL_O44_LVLMONO=smooth+conserve) — with SFXBASE (THE LIVE R23 BOARD 68be10c7, dial
      unset, this seat's own emit on the SAME edited tree) beneath them as THE COMPARISON COLUMN.
      The owner is choosing BETWEEN the variants, so both must stand on one page against one base.

  (2) the output filenames (BANDS_NOARB_SFX.json / BANDS_NOARB_SFX_out.txt).

  (3) the scratch WORK dir re-pointed at this seat's own dir.

  (4) THE HARNESS STORE PIN IS RE-POINTED AT THE CALL SITE FOR THE R23 STORE, AND THE ACCEPTED SET
      STAYS CLOSED. The D8 act re-pointed cb38ef11 -> cc02567f and explained why (below). The R23
      ADVANCE moved the store again, cc02567f -> b745002e, and that identity is added to the CLOSED
      accepted set with its reason. Anything else still fails closed. THE INSTRUMENT COPY IS NOT
      EDITED (its md5 is printed at run, unmodified); the pin is re-pointed on the imported module
      here, in the file under review, exactly as the D8 act did.

  THE COMPARISON-COLUMN IDENTITY CLAIM IS NOT CARRIED, AND THAT IS A CORRECTION, NOT A WEAKENING.
  D8's copy ASSERTED that its base matrix was byte-identical to the D7B matrix. That claim CANNOT be
  true here and must not be pretended: the live board moved a05fe951 -> 68be10c7 at the D8 ADOPTION
  and again at the R23 ADVANCE, so this seat's base matrix is a DIFFERENT object by construction. The
  assert is replaced by the assertions this act can actually make and that are worth making:
  non-vacuity (each candidate matrix differs from the base) and separation (the two candidate
  matrices differ from each other — otherwise the owner is choosing between two names for one thing).

THE MEASUREMENT IS UNTOUCHED: value_at() is still byte-asserted against the disclosed instrument, and
the windows, the thin rules, the cohort clock, FLOOR_N=5 and the verdict rule are all the standing
instrument's own.
ORIGINAL D8 HEADER FOLLOWS.

ORDER D8 MEASUREMENT — THE ND BAND TABLES, BOTH WINDOWS, ON THE PRICED CANDIDATE 5ea978f7.

d7b_bands.py (the standing ND-band instrument) carried with FOUR declared changes and NOTHING ELSE:
  (1) LABELS: D8CAND (the priced candidate 5ea978f7 = the live dial line + RL_O33_TAPEROFF=1) at the
      head, with D8BASE (THE LIVE BOARD a05fe951, this seat's own dial-unset emit on the SAME tree)
      directly beneath it as THE COMPARISON COLUMN. D8BASE's `recs` block is BYTE-IDENTICAL to
      per_entrant_D7BCAND.json's — the matrix the on-file D7B tables were rendered from — and to the
      post-flip bare bake's per_entrant_BK.json (all three canonical-md5 e244d914b7e2, printed at run
      below). So the comparison column IS the D7B table, re-emitted on today's store rather than
      re-typed. The other historical boards are dropped from THIS run because this order asks for one
      comparison; their tables are on file unchanged in
      docs/evidence/final_candidate_2026-08-19/BANDS_D7B_out.txt and are not re-derived here.
  (2) the output filenames (BANDS_NOARB_D8.json / BANDS_NOARB_D8_out.txt) — BANDS_D8_out.txt in this
      same directory is the D8 build seat's ceiling-tax band table and is a DIFFERENT instrument;
      it is not touched.
  (3) the scratch WORK dir is re-pointed at this seat's own dir.
  (4) THE HARNESS STORE PIN IS RE-POINTED AT THE CALL SITE, AND THAT IS A FINDING, NOT HOUSEKEEPING.
      harness_pvc_REPINNED_pass3.py carries EXPECT_STORE = 'cb38ef11' and load_matrix() fails closed
      on any matrix whose meta store does not match it. The tree's store of record moved cb38ef11 ->
      cc02567f at commit de9b8eb (the owner's 112 ownership moves + 23 pick-owner moves), whose own
      message records "board byte-identical". EVERY matrix emitted after that commit — including the
      one this seat needs — therefore trips the assert. THE INSTRUMENT COPY IS NOT EDITED (its md5
      02dcf28c is printed at run, unmodified); the pin is re-pointed on the imported module here, in
      the file under review, with the prior value kept, exactly as the harness's own header does at
      every prior landed store. IT IS ALSO PROVED RATHER THAN ASSERTED: this seat rebuilt the board
      on today's tree (store cc02567f) and got a05fe951 byte-exact, and D8BASE's recs are byte-equal
      to the pre-apply D7BCAND's. The ownership apply moved the store identity and not one price.

THE MEASUREMENT IS UNTOUCHED: value_at() is still byte-asserted against the disclosed instrument,
the windows, the thin rules, the cohort clock (draft year + 1 for every ND row — MSD never appears
in an ND band), the FLOOR_N=5 rule and the verdict rule are all d7b_bands.py's own.

NO ENGINE RUN HERE — a pure read over two walk-forward matrices that already exist.
PRICED, NOT ADOPTED. NO PIN MOVES.
ORIGINAL D7b HEADER FOLLOWS.

ORDER D7b — THE ND BAND TABLES, IN BOTH WINDOWS, ON THE PARITY CANDIDATE a05fe951.

fc_bands.py carried with TWO declared changes: D7BCAND added at the head of the LABELS list, and the
output filenames (BANDS_D7B.*). THE MEASUREMENT IS UNTOUCHED.
ORIGINAL FINAL-CANDIDATE / ORDER P HEADER FOLLOWS.

ORDER P BUILD — THE ND BAND TABLES, IN BOTH WINDOWS. ORDER P's op_bands.py, REUSED WHOLE.

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
WORK = os.path.join(SP, 'sfx', 'noarb')
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

# ---- DECLARED CHANGE (4): the harness store pin, re-pointed HERE, never in the instrument ---------
_STORE_PINS = {
    'cb38ef11': 'the ORDER 29 unflag-three store — what harness_pvc_REPINNED_pass3.py is pinned to',
    'cc02567f': "the TREE'S STORE OF RECORD at ORDER D8 (the owner's 112 ownership + 23 pick-owner "
                'moves at de9b8eb; that commit records "board byte-identical")',
    'b745002e': "the TREE'S STORE OF RECORD NOW — R23, the round-23 advance (docs/evidence/"
                'r23_advance_2026-08-20), which is the store data/expected_boot.json pins and the '
                'store the live board 68be10c7 was built on',
}
_TREE_STORE = hashlib.md5(open(os.path.join(REPO, 'engine', 'rl_after',
                                            'rl_model_data.json'), 'rb').read()).hexdigest()[:8]
P()
P('THE HARNESS STORE PIN — RE-POINTED AT THIS CALL SITE, INSTRUMENT COPY UNMODIFIED:')
P('  harness_pvc_REPINNED_pass3.py EXPECT_STORE  = %s   (%s)' % (H.EXPECT_STORE, _STORE_PINS.get(H.EXPECT_STORE, '?')))
P("  this tree's engine/rl_after/rl_model_data.json = %s   (%s)" % (_TREE_STORE, _STORE_PINS.get(_TREE_STORE, '?')))
assert _TREE_STORE == 'b745002e', 'the tree store is not the R23 identity: %s' % _TREE_STORE
P('  Every matrix emitted after the R23 advance carries b745002e and would FAIL CLOSED on the shipped')
P('  pin. The pin is re-pointed per label below and the accepted set is CLOSED to the three identities')
P('  above; anything else still fails closed. WHAT THIS SEAT CAN AND CANNOT PROVE ABOUT THE BASE:')
P('    * CAN: the dial-OFF build on THIS EDITED tree reproduces the LIVE board 68be10c7 BYTE-EXACT,')
P('      dev twice and canonical, plus balanced 556ad70d — BUILD_F1_out.txt. That is F1, and it is')
P('      what makes SFXBASE the live board rather than a near-miss.')
P('    * CANNOT, and does not pretend to: SFXBASE is NOT byte-equal to the D7B/D8 matrices. The live')
P('      board moved a05fe951 -> 68be10c7 at the D8 ADOPTION and the store moved again at R23, so a')
P('      carried identity assert would be false. D8\'s assert is REPLACED, not silently dropped, by')
P('      non-vacuity and separation below.')
_CANON = {}
for _l in ('SFXBRAW', 'SFXACON', 'SFXBCON', 'SFXBASE', 'D8CAND', 'D8BASE'):
    _p = os.path.join(SP, 'per_entrant_%s.json' % _l)
    if os.path.exists(_p):
        _d = json.load(open(_p))
        _CANON[_l] = hashlib.md5(json.dumps(_d['recs'], sort_keys=True).encode()).hexdigest()[:12]
        P('    recs canonical md5  %-9s %s   (store %s, engine %s)'
          % (_l, _CANON[_l], _d['meta']['store_md5'], _d['meta']['engine_head']))
assert _CANON['SFXBRAW'] != _CANON['SFXBASE'], 'VARIANT B RAW DID NOTHING — the pass-through did not fire'
assert _CANON['SFXBRAW'] != _CANON['SFXBCON'], \
    'B RAW EQUALS B CONSERVED — the renormaliser is not in the candidate and the arm is mislabelled'
assert _CANON['SFXACON'] != _CANON['SFXBASE'], 'VARIANT A DID NOTHING — the pass-through did not fire'
assert _CANON['SFXBCON'] != _CANON['SFXBASE'], 'VARIANT B DID NOTHING — the pass-through did not fire'
assert _CANON['SFXACON'] != _CANON['SFXBCON'], \
    'THE TWO VARIANTS ARE THE SAME OBJECT — there is no choice to put in front of the owner'
assert _CANON['SFXBASE'] != _CANON.get('D8BASE', ''), \
    'the base matrix equals the D8 base — the board move did not reach the matrix'
P('  -> both candidate matrices NON-VACUOUS against the base and SEPARATE from each other.')

# ORDER 44: THE TWO PRICED CANDIDATES LEAD THIS LIST AND THE LIVE BOARD SITS DIRECTLY BENEATH THEM.
LABELS = [('SFXBRAW', '*** ORDER 44 VARIANT B RAW — RL_O44_LVLMONO=smooth — THE ADOPTED ARM ***'),
          ('SFXACON', '*** ORDER 44 VARIANT A CONSERVED — RL_O44_LVLMONO=ratchet+conserve ***'),
          ('SFXBCON', '*** ORDER 44 VARIANT B CONSERVED — RL_O44_LVLMONO=smooth+conserve ***'),
          ('SFXBASE', 'THE LIVE R23 BOARD 68be10c7 — dial unset, same tree. THE COMPARISON COLUMN '
                      '(F1: this tree with the dial off rebuilds 68be10c7 byte-exact)')]
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
    # DECLARED CHANGE (4): re-point the harness pin for THIS matrix, from a CLOSED accepted set.
    _s = json.load(open(MX))['meta']['store_md5']
    assert _s in _STORE_PINS, ('MATRIX STORE %s IS NOT AN ACCEPTED IDENTITY — fails closed exactly as '
                               'the harness intends' % _s)
    H.EXPECT_STORE = _s
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

json.dump(OUT, open(os.path.join(HERE, 'BANDS_NOARB_BRAW.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'BANDS_NOARB_BRAW_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote BANDS_NOARB_SFX.json / BANDS_NOARB_SFX_out.txt')
