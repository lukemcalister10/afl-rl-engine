#!/usr/bin/env python3
"""tools/noarb_standing_page.py — THE OWNER'S STANDING NO-ARB TABLES, through the frozen template.

    python3 tools/noarb_standing_page.py CAND_MATRIX.json REF_MATRIX.json -o OUT.html \
        [--cand-label "..."] [--ref-label "..."] [--board-md5 X --engine-head X --config X \
         --store-md5 X --as-of-round N]

Owner, 2026-08-25: the ad-hoc class-reading page is NOT the standing format — "that format of
no arb table was saved as a template so I wouldn't have to worry about new agents getting it
wrong." This tool renders THAT template (ui/templates/noarb.html, layout frozen from
ASSEMBLY_NOARB.html; seats inject data, never layout) from two walk-forward matrices
(per_entrant_*.json): the CANDIDATE and the REFERENCE (normally the live board).

Semantics carried from the assembly-era instruments, unmodified:
  value_at()      byte-identical to t338_extended_DISCLOSED.py (md5-asserted at run)
  windows         PRIMARY cohorts 2005-2023 · MODERN cohorts 2019-2023
  bands           ALL 1-64 / 1-20 / 21-64 / 1-10 / 11-20 / 21-30 / 31-40 / 41-64
  reading rule    fair = yr0->1 appreciation in [0%, +14%]; below = SELL-RED; above = BUY-RED
  path test       owner's own, on every breaching cell: carry compounds at 14%;
                  limb (a) no year 2..7 keeps beating carry; limb (b) yr7 <= yr6 and yr7 <= carry7
  thin marks      * thin (<30 at yr1) · ** very thin (<10) · not printed below 5
  presentation    the candidate's bands (both windows) + the pool-arm comparison vs the reference
                  (owner's standing ruling: candidate + live reference only, no historical boards)
"""
import argparse
import hashlib
import json
import os
import statistics
import sys
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from ui.templates import slots  # noqa: E402

T338 = os.path.join(REPO, 'docs/evidence/candidate_31f/ext_2026-08-17/t338_extended_DISCLOSED.py')
T338_MD5 = 'd59ad550116ebbe3d90ed82becd2c4d5'

CARRY = [1.140, 1.300, 1.482, 1.689, 1.925, 2.195, 2.502]      # years 1..7 at 14%
CHARGE = 0.14
BANDS = [('ALL picks 1-64', lambda r: True),
         ('picks 1-20', lambda r: 1 <= r['pick'] <= 20),
         ('picks 21-64', lambda r: 21 <= r['pick'] <= 64),
         ('picks 1-10', lambda r: 1 <= r['pick'] <= 10),
         ('picks 11-20', lambda r: 11 <= r['pick'] <= 20),
         ('picks 21-30', lambda r: 21 <= r['pick'] <= 30),
         ('picks 31-40', lambda r: 31 <= r['pick'] <= 40),
         ('picks 41-64', lambda r: 41 <= r['pick'] <= 64)]
WINDOWS = [('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)]
YEARS = list(range(0, 8))
THIN, VTHIN, FLOOR_N = 30, 10, 5
POOL_ARMS = ('RD', 'UNR', 'IRE', 'SSP', 'PDA', 'PDN')


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


def assert_value_at_pinned():
    blob = open(T338, 'rb').read()
    m = hashlib.md5(blob).hexdigest()
    assert m == T338_MD5, 'INSTRUMENT MD5 MOVED: t338_extended_DISCLOSED.py %s != %s' % (m, T338_MD5)
    body = blob.decode().split('def value_at(r, N):')[1].split('\ndef main()')[0].rstrip()
    mine = open(os.path.abspath(__file__)).read().split('def value_at(r, N):')[1] \
        .split('\n\n\ndef assert_value_at_pinned')[0].rstrip()
    assert body == mine, 'value_at is NOT byte-identical to the disclosed instrument'


def cohort(r):
    return r['year'] + 1


def flag(n):
    return 'none' if n < FLOOR_N else ('vthin' if n < VTHIN else ('thin' if n < THIN else 'ok'))


def band_path(pop, wend):
    path, nincl = [], []
    for N in YEARS:
        incl = [r for r in pop if r['year'] + N <= wend]
        nincl.append(len(incl))
        if len(incl) < FLOOR_N:
            path.append(None)
            continue
        m0 = statistics.mean(float(r['v0']) for r in incl)
        mN = statistics.mean(value_at(r, N)[0] for r in incl)
        path.append(mN / m0 if m0 > 0 else None)
    return path, nincl


def fmt_path_cell(v, n):
    if v is None:
        return 'not printed (n<%d)' % FLOOR_N
    return '%.3f%s' % (v, {'ok': '', 'thin': '*', 'vthin': '**', 'none': ''}[flag(n)])


def verdict_word(a01, mark=''):
    if a01 is None:
        return 'n/a'
    if a01 < 0.0:
        return 'SELL-SIDE RED' + mark
    if a01 > CHARGE:
        return 'BUY-SIDE RED' + mark
    return 'fair' + mark


def path_test_word(path):
    """The owner's path test on a breaching cell; '—' when the cell does not breach."""
    if not path or path[0] in (None, 0) or len(path) < 2 or path[1] is None:
        return 'n/a'
    r = [(path[k] / path[0]) if path[k] is not None else None for k in range(len(path))]
    a01 = r[1] - 1.0
    if a01 <= CHARGE:
        return 'no breach (yr0→1 within the rail)'
    beat = [k for k in range(2, min(8, len(r))) if r[k] is not None and r[k] > CARRY[k - 1]]
    la = len(beat) == 0
    p6, p7 = (r[6] if len(r) > 6 else None), (r[7] if len(r) > 7 else None)
    lb = p7 is not None and p6 is not None and p7 <= p6 and p7 <= CARRY[6]
    return ('PASS (a: no later year beats carry; b: destination settles)' if (la and lb) else
            'FAIL (%s%s)' % ('' if la else 'a: beats carry in yr %s ' % ','.join(map(str, beat)),
                             '' if lb else 'b: destination still rising'))


def load_matrix(path):
    d = json.load(open(path))
    recs = d['recs']
    nd = [r for r in recs if r.get('type') == 'ND' and r.get('pick') and not r.get('pickless')]
    wend = max(y for r in recs for y, v in zip(r.get('yrs') or [], r.get('vpath') or [])
               if v is not None)
    return d.get('meta', {}), recs, nd, wend


def arm_a01(recs, arm, wend, lo, hi):
    pop = [r for r in recs if r.get('type') == arm and lo <= cohort(r) <= hi
           and r['year'] + 1 <= wend and float(r.get('v0') or 0) > 0]
    if len(pop) < FLOOR_N:
        return None, len(pop)
    m0 = statistics.mean(float(r['v0']) for r in pop)
    m1 = statistics.mean(value_at(r, 1)[0] for r in pop)
    return (m1 / m0 - 1.0) if m0 > 0 else None, len(pop)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cand_matrix')
    ap.add_argument('ref_matrix')
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--cand-label', default='THE CANDIDATE')
    ap.add_argument('--ref-label', default='the live board')
    ap.add_argument('--board-md5', required=True)
    ap.add_argument('--store-md5', required=True)
    ap.add_argument('--engine-head', required=True)
    ap.add_argument('--config', required=True)
    ap.add_argument('--as-of-round', required=True)
    a = ap.parse_args()

    assert_value_at_pinned()
    _, crecs, cnd, cwend = load_matrix(a.cand_matrix)
    _, rrecs, rnd, rwend = load_matrix(a.ref_matrix)

    bands = []
    for wname, lo, hi in WINDOWS:
        popw = [r for r in cnd if lo <= cohort(r) <= hi]
        for bname, bfilt in BANDS:
            pop = [r for r in popw if bfilt(r)]
            path, nincl = band_path(pop, cwend)
            a01 = (path[1] - 1.0) if path[1] is not None else None
            mark = {'ok': '', 'thin': '*', 'vthin': '**', 'none': ''}[flag(nincl[1])]
            row = {'band': '%s · %s' % (wname, bname), 'n': len(pop)}
            for i in YEARS:
                row['yr%d' % i] = fmt_path_cell(path[i], nincl[i])
            row['yr0_1'] = '%+.2f%%' % (100 * a01) if a01 is not None else 'n/a'
            row['margin'] = '%+.2f%%' % (100 * (CHARGE - a01)) if a01 is not None else 'n/a'
            row['verdict'] = verdict_word(a01, mark)
            row['path_test'] = path_test_word(path)
            bands.append(row)

    arms = []
    lo, hi = WINDOWS[0][1], WINDOWS[0][2]
    for arm in POOL_ARMS:
        ca, cn = arm_a01(crecs, arm, cwend, lo, hi)
        ra, rn = arm_a01(rrecs, arm, rwend, lo, hi)
        arms.append({
            'arm': arm, 'n': cn,
            'candidate': '%+.2f%%' % (100 * ca) if ca is not None else 'n/a (n=%d)' % cn,
            'reference': '%+.2f%%' % (100 * ra) if ra is not None else 'n/a (n=%d)' % rn,
            'delta': '%+.2f%%' % (100 * (ca - ra)) if (ca is not None and ra is not None) else 'n/a',
            'verdict': '%s → %s' % (verdict_word(ra), verdict_word(ca))})

    html = slots.render('noarb', {
        'page_title': 'THE NO-ARB TABLES — %s' % a.cand_label,
        'subtitle': '%s against %s. A group is fairly priced if it appreciates between 0%% and '
                    '+14%% over its first year — below 0%% you could sell at draft day and buy back '
                    'cheaper; above +14%% you could buy at draft day and beat the cost of carry. '
                    'Every breaching cell is scored on your own path test; every raw year is '
                    'printed. * thin cell · ** very thin.' % (a.cand_label, a.ref_label),
        'standing_note': 'Your standing presentation ruling applies: the candidate and the live '
                         'reference only — no historical progress boards on this page.',
        'cohort_heading': 'The ND band tables — %s (PRIMARY cohorts 2005-2023, then MODERN '
                          'cohorts 2019-2023)' % a.cand_label,
        'arms_heading': 'The pool-arm comparison — candidate vs %s (PRIMARY window, yr0→1 '
                        'appreciation)' % a.ref_label,
        'bands': bands, 'arms': arms,
        'board_md5': a.board_md5, 'store_md5': a.store_md5, 'engine_head': a.engine_head,
        'config': a.config, 'as_of_round': a.as_of_round,
        'generated_at': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()),
    })
    # SELF-CONTAINED DELIVERY: the frozen template links _base.css by relative path, which never
    # loads when the page is viewed as a single file. Inline the stylesheet VERBATIM — the layout
    # law is untouched (same bytes, different transport).
    css = open(os.path.join(REPO, 'ui/templates/_base.css')).read()
    html = html.replace('<link rel="stylesheet" href="_base.css">',
                        '<style>\n%s\n</style>' % css)
    open(a.out, 'w').write(html)
    print('wrote %s (%d bands rows, %d arms rows, css inlined)' % (a.out, len(bands), len(arms)))


if __name__ == '__main__':
    main()
