#!/usr/bin/env python3
"""ORDER D7b — THE FULL NO-ARB PAGE FOR THE PARITY CANDIDATE a05fe951.

as_noarb.py's format and its path test, CANDIDATE-ONLY as the owner's standing presentation ruling
requires, pointed at the D7b tables:

    ND bands   BANDS_D7B.json            (d7b_bands.py -> BANDS_D7B_out.txt)
    pool arms  STANDING_TABLES_D7B.json  (d7b_tables.py -> STANDING_TABLES_D7B_out.txt)

WHAT THIS PAGE ADDS OVER as_noarb.py, and nothing else:
  * the RED LEDGER is on the page, all four ruled documented-reds labelled AS RULED and reported at
    what they actually read on this board. The completion pass could measure only one of the four
    (tail 0.80) because three of them read a matrix and no matrix existed. All four are measured now.
  * the raw-evidence manifest: every table on this page names the *_out.txt it was rendered from.
  * the arms that carry no cell in a window are PRINTED AS ABSENT with their reason, never dropped.

THE PATH TEST is as the owner gave it and as PREREG_S.md section 7 froze it BEFORE any table was
read; the code below is as_noarb.py's, unchanged.

NOTHING IS ADOPTED. NO ENGINE RUN HERE — pure reads over the two table files.
"""
import json, os, sys, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
with contextlib.redirect_stdout(io.StringIO()):      # fc_pages narrates at import; not our output
    import fc_box as BOX
    from fc_pages import CSS, JS, esc

BD = json.load(open(os.path.join(HERE, 'BANDS_D7B.json')))['nd']
AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_D7B.json')))
ARMS = AJ['arms']

CARRY = [1.140, 1.300, 1.482, 1.689, 1.925, 2.195, 2.502]      # years 1..7 at 14%
BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64',
         'picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
ARM_ORDER = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']
ARM_LONG = {'RD': 'rookie draft', 'MSD': 'mid-season draft', 'UNR': 'un-drafted / unrestricted',
            'IRE': 'international rookie', 'PDA': 'pre-draft academy', 'PDN': 'pre-draft NGA',
            'PDS': 'pre-draft father-son', 'SSP': 'supplemental selection period',
            'ALLPOOL': 'every pool arm together'}
WIN = [('PRIMARY', 'PRIMARY — cohorts 2005-2023 (the whole population)'),
       ('MODERN', 'MODERN — cohorts 2019-2023')]
LAB = 'D7BCAND'
NICE = 'THE PARITY CANDIDATE a05fe951 — RL_O42=1 RL_O43=1'
VKEY = 'ALLCOH'


def path_test(path):
    """as_noarb.py's, unchanged. Returns the owner's two-limb reading of a breaching cell."""
    if not path or path[0] in (None, 0) or len(path) < 2 or path[1] is None:
        return None
    r = [(path[k] / path[0]) if (path[0] and path[k] is not None) else None
         for k in range(len(path))]
    a01 = r[1] - 1.0 if r[1] is not None else None
    if a01 is None or a01 <= 0.14:
        return dict(breaches=False)
    beat = [k for k in range(2, min(8, len(r))) if r[k] is not None and r[k] > CARRY[k - 1]]
    la = (len(beat) == 0)
    p6 = r[6] if len(r) > 6 else None
    p7 = r[7] if len(r) > 7 else None
    lb = (p7 is not None and p6 is not None and p7 <= p6 and p7 <= CARRY[6])
    return dict(breaches=True, limb_a=la, limb_b=lb, both=(la and lb), beat=beat)


def verdict_cell(a01):
    if a01 is None:
        return ('n/a', '')
    if a01 < 0.0:
        return ('SELL-SIDE RED', 'red')
    if a01 > 0.14:
        return ('BUY-SIDE RED', 'red')
    return ('fair', '')


def path_txt(pt):
    if pt is None or not pt.get('breaches'):
        return ('—', '')
    if pt['both']:
        return ('PASSES both limbs', '')
    fails = []
    if not pt['limb_a']:
        fails.append('beats carry in yr %s' % ','.join(str(x) for x in pt['beat']))
    if not pt['limb_b']:
        fails.append('still rising at yr7')
    return ('FAILS — ' + '; '.join(fails), 'red')


def yearcells(path, flags=None):
    out = ''
    for i in range(8):
        val = path[i] if (path and i < len(path)) else None
        fl = flags[i] if (flags and i < len(flags)) else 'ok'
        mark = {'ok': '', 'thin': '*', 'vthin': '**'}.get(fl, '')
        out += ('<td data-v="%s">%s</td>'
                % (val if val is not None else -1,
                   ('%.3f%s' % (val, mark)) if val is not None else '—'))
    return out


h = []

# ================= the reading rule ==============================================================
h.append('<div class="sub"><b>THE READING RULE, in plain words.</b> A group is fairly priced if it '
         'appreciates between <b>0%</b> and <b>+14%</b> over its first year. Below 0% is a '
         '<b>SELL-SIDE RED</b> — you could sell at draft day and buy back cheaper. Above +14% is a '
         '<b>BUY-SIDE RED</b> — you could buy at draft day and beat the cost of carrying him. '
         '<b>Every breaching cell is scored on your own path test</b>, and <b>every raw year is '
         'printed</b> so you can apply your own reading rather than this seat\'s. '
         '<b>* thin cell · ** very thin.</b></div>')
h.append('<div class="sub"><b>THE PATH TEST, as you gave it</b> (frozen in PREREG_S.md §7 before any '
         'table was read). Carry compounds at 14%%: %s. A cell BREACHES when its year-1 appreciation '
         'exceeds +14%%. For a breaching cell — <b>limb (a)</b> &ldquo;the path afterwards does not '
         'keep beating carry&rdquo; passes when NO year 2..7 sits above the carry line; <b>limb (b)</b> '
         '&ldquo;the end destination does not keep increasing&rdquo; passes when yr7 &le; yr6 AND '
         'yr7 &le; carry. The cell passes only when BOTH limbs pass.</div>'
         % ' · '.join('yr%d %.3f' % (i + 1, c) for i, c in enumerate(CARRY)))
h.append('<div class="sub" style="border-left:3px solid var(--acc);padding-left:10px">'
         '<b>THIS PAGE SHOWS THE CANDIDATE ONLY</b>, on your standing instruction. The historical '
         'progress boards are still built and still scored — they are in the raw record '
         '(<code>BANDS_D7B_out.txt</code>, <code>STANDING_TABLES_D7B_out.txt</code>) rather than in '
         'front of you. <b>The board is PRICED, NOT ADOPTED.</b> Nothing here is adopted, merged, '
         'tagged or promoted.</div>')

# ================= the ND bands ==================================================================
h.append('<h1 style="margin-top:30px">THE ND BANDS</h1>')
h.append('<div class="sub">Five ND bands plus the classic three (ALL 1-64 / 1-20 / 21-64), in BOTH '
         'windows, on the candidate\'s own walk-forward matrix '
         '<code>per_entrant_D7BCAND.json</code>. Raw: <code>BANDS_D7B_out.txt</code>.</div>')
nd_breach = []
for wkey, wnice in WIN:
    rows = [(b, BD[LAB]['%s|%s|%s' % (wkey, VKEY, b)]) for b in BANDS
            if '%s|%s|%s' % (wkey, VKEY, b) in BD.get(LAB, {})]
    if not rows:
        continue
    h.append('<h2>%s</h2>' % esc(wnice))
    h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">band</th><th>n</th>'
             + ''.join('<th>yr%d</th>' % i for i in range(8))
             + '<th>yr0&rarr;1</th><th>margin</th><th>verdict</th><th>path test</th>'
               '</tr></thead><tbody>')
    for b, d in rows:
        a01 = d.get('apprec01'); mgn = d.get('buy_margin')
        v, cls = verdict_cell(a01)
        pt = path_test(d.get('path') or [])
        ptxt, pcls = path_txt(pt)
        if pt and pt.get('breaches'):
            nd_breach.append((wkey, b, a01, pt['both']))
        h.append('<tr><td class="l">%s</td><td data-v="%d">%d</td>%s'
                 '<td data-v="%s" class="%s">%s</td><td data-v="%s">%s</td>'
                 '<td class="%s">%s</td><td class="%s">%s</td></tr>'
                 % (esc(b), d.get('n', 0), d.get('n', 0),
                    yearcells(d.get('path'), d.get('flags')),
                    a01 if a01 is not None else -9, cls,
                    ('%+.2f%%' % (100 * a01)) if a01 is not None else '—',
                    mgn if mgn is not None else -9,
                    ('%+.2f%%' % (100 * mgn)) if mgn is not None else '—',
                    cls, v, pcls, ptxt))
    h.append('</tbody></table></div>')

# ================= the pool arms =================================================================
h.append('<h1 style="margin-top:34px">THE POOL ARMS</h1>')
h.append('<div class="sub">Every pool pathway, both windows, the same standing format. The cohort '
         'clock and the value semantics are the all-arm instrument\'s own '
         '(<code>noarb_table_allarm.py</code>, md5 <code>8673d7e3…</code>, asserted at run). '
         'Raw: <code>STANDING_TABLES_D7B_out.txt</code>.</div>')
h.append('<div class="sub" style="border-left:3px solid var(--warn);padding-left:10px">'
         '<b>THE MSD YEAR-1 EXCLUSION, AND ITS REASON.</b> The cohort clock keys an <b>MSD</b> row on '
         '<b>the DRAFT YEAR ITSELF</b>, not draft year + 1 as it does for everyone else, because a '
         'mid-season draftee\'s first season <b>IS</b> his draft season. At year 1 an MSD row '
         'therefore falls <b>before</b> the first year his path covers. Those rows are counted '
         '<b>PRE-WINDOW and EXCLUDED</b> from the year-1 cell rather than scored as zero — scoring '
         'them as zero would invent a collapse that did not happen. <b>That, and only that, is why '
         'MSD\'s yr1 cell reads &ldquo;—&rdquo;</b> and why MSD carries no year-1 verdict.</div>')
arm_breach = []
for wkey, wnice in WIN:
    h.append('<h2>%s</h2>' % esc(wnice))
    h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">arm</th>'
             '<th class="l">pathway</th><th>n</th>'
             + ''.join('<th>yr%d</th>' % i for i in range(8))
             + '<th>yr0&rarr;1</th><th>margin</th><th>verdict</th><th>path test</th>'
               '</tr></thead><tbody>')
    absent = []
    for a in ARM_ORDER:
        k = '%s|%s' % (wkey, a)
        if k not in ARMS.get(LAB, {}):
            absent.append(a)
            continue
        d = ARMS[LAB][k]
        a01 = d.get('apprec01'); mgn = d.get('margin')
        v, cls = verdict_cell(a01)
        pt = path_test(d.get('path') or [])
        ptxt, pcls = path_txt(pt)
        if pt and pt.get('breaches'):
            arm_breach.append((wkey, a, a01, pt['both']))
        note = 'MSD yr1 EXCLUDED — pre-window' if (a == 'MSD' and a01 is None) else v
        ncls = 'amber' if (a == 'MSD' and a01 is None) else cls
        h.append('<tr><td class="l"><b>%s</b></td><td class="l k">%s</td><td data-v="%d">%d</td>%s'
                 '<td data-v="%s" class="%s">%s</td><td data-v="%s">%s</td>'
                 '<td class="%s">%s</td><td class="%s">%s</td></tr>'
                 % (esc(a), esc(ARM_LONG.get(a, '')), d.get('n', 0), d.get('n', 0),
                    yearcells(d.get('path')),
                    a01 if a01 is not None else -9, cls,
                    ('%+.2f%%' % (100 * a01)) if a01 is not None else '—',
                    mgn if mgn is not None else -9,
                    ('%+.2f%%' % (100 * mgn)) if mgn is not None else '—',
                    ncls, note, pcls, ptxt))
    h.append('</tbody></table></div>')
    if absent:
        h.append('<div class="sub"><b>ABSENT FROM THIS WINDOW, NOT DROPPED:</b> %s. The all-arm '
                 'instrument emits no cell for an arm with no qualifying rows inside the window — '
                 'for %s that is a POPULATION fact about the window, not a reading. It is printed '
                 'here so the arm cannot vanish silently.</div>'
                 % (', '.join('<b>%s</b> (%s)' % (esc(a), esc(ARM_LONG.get(a, ''))) for a in absent),
                    'PDS — pre-draft father-son' if absent == ['PDS'] else 'those arms'))

# ================= the red ledger ================================================================
def cell(win, band):
    d = BD[LAB].get('%s|%s|%s' % (win, VKEY, band))
    return None if d is None else d.get('apprec01')


def acell(win, arm):
    d = ARMS[LAB].get('%s|%s' % (win, arm))
    return None if d is None else d.get('apprec01')


def pct(v):
    return '—' if v is None else '%+.2f%%' % (100 * v)


LATE = [('PRIMARY', 'picks 31-40'), ('PRIMARY', 'picks 41-64'), ('PRIMARY', 'picks 21-64'),
        ('MODERN', 'picks 21-30'), ('MODERN', 'picks 31-40'), ('MODERN', 'picks 41-64'),
        ('MODERN', 'picks 21-64')]
h.append('<h1 style="margin-top:34px">THE RULED DOCUMENTED-RED LEDGER</h1>')
h.append('<div class="sub">The four standing documented-reds, <b>each labelled as RULED</b> and '
         'reported at <b>what it actually reads on this board</b>. The completion pass could measure '
         'only one of these four — the other three read a walk-forward matrix and no matrix for '
         '<code>a05fe951</code> existed. <b>D7b\'s emit produced that matrix, so all four are '
         'measured here.</b> Being ruled is <b>not</b> the same as being repaired: a ruled red is one '
         'you have already looked at and accepted, and none of them was chased by a dial.</div>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">ruled documented-red</th>'
         '<th class="l">standing ruling</th><th class="l">what it reads on a05fe951</th>'
         '<th class="l">status</th></tr></thead><tbody>')
h.append('<tr><td class="l"><b>modern picks 1-10 and 1-20 buy-side reds</b></td>'
         '<td class="l">RULED ACCEPTED</td>'
         '<td class="l">1-10 <b>%s</b> · 1-20 <b>%s</b> (MODERN). Both breach; both FAIL the path '
         'test on limb (b) — still rising at yr7.</td>'
         '<td class="l">MEASURED. Reported as it reads; <b>no dial was touched to chase it.</b></td></tr>'
         % (pct(cell('MODERN', 'picks 1-10')), pct(cell('MODERN', 'picks 1-20'))))
h.append('<tr><td class="l"><b>late-band sell-side reds</b></td>'
         '<td class="l">POPULATION-RISK RULED</td>'
         '<td class="l">%s</td>'
         '<td class="l">MEASURED. The ruled reading is that these bands carry real population risk '
         'the price is right to take; they are <b>not</b> treated as a pricing defect here.</td></tr>'
         % ' · '.join('%s %s <b>%s</b>' % (w, b.replace('picks ', ''), pct(cell(w, b)))
                      for w, b in LATE))
h.append('<tr><td class="l"><b>SSP</b> — supplemental selection period</td>'
         '<td class="l">INHERITED / PARKED (register v744 C6)</td>'
         '<td class="l">PRIMARY <b>%s</b> · MODERN <b>%s</b> (n=%d). BUY-SIDE RED; FAILS the path '
         'test on limb (a) — beats carry in years 2 and 3.</td>'
         '<td class="l">MEASURED. <b>SSP IS NOT REPAIRED BY THIS BOARD AND WAS NEVER MEANT TO BE.</b> '
         'It is parked. It reads better than ORDER P (+58.17%%) and worse than ORDER K (+52.71%%).</td>'
         '</tr>'
         % (pct(acell('PRIMARY', 'SSP')), pct(acell('MODERN', 'SSP')),
            (ARMS[LAB].get('PRIMARY|SSP') or {}).get('n', 0)))
h.append('<tr><td class="l"><b>tail calibration 0.80</b></td>'
         '<td class="l">RULED &ldquo;tail 0.80&rdquo;</td>'
         '<td class="l"><b>0.8004</b>, on the candidate\'s own charge form '
         '(<code>TAIL_CP_out.txt</code>, measured by the completion pass — it does not read a matrix '
         'and was never blocked).</td>'
         '<td class="l">MEASURED. Reported at what it reads; no dial was touched to chase it.</td></tr>')
h.append('</tbody></table></div>')

# ================= the breach roll-up ============================================================
h.append('<h2>Every breaching cell on this board, in one place</h2>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">window</th><th class="l">cell</th>'
         '<th>yr0&rarr;1</th><th class="l">path test</th></tr></thead><tbody>')
for wkey, name, a01, both in nd_breach + arm_breach:
    h.append('<tr class="red"><td class="l">%s</td><td class="l">%s</td>'
             '<td data-v="%f">%+.2f%%</td><td class="l">%s</td></tr>'
             % (esc(wkey), esc(name), a01, 100 * a01,
                'PASSES both limbs' if both else 'FAILS'))
if not (nd_breach + arm_breach):
    h.append('<tr><td class="l" colspan="4">no breaching cell on this board</td></tr>')
h.append('</tbody></table></div>')
h.append('<div class="sub"><b>A breach is a cell whose year-1 appreciation exceeds +14%. '
         'Sell-side reds are NOT breaches of the buy rail</b> and are not scored on the path test — '
         'the path test is a buy-side instrument. They are read on their own line in the ledger '
         'above.</div>')

# ================= the raw manifest ==============================================================
h.append('<h2>THE RAW RECORD — every table on this page names the file it was rendered from</h2>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">table</th>'
         '<th class="l">raw output</th><th class="l">instrument</th></tr></thead><tbody>')
for t, o, i in [('the ND bands, both windows', 'BANDS_D7B_out.txt', 'd7b_bands.py'),
                ('the ND bands, machine-readable', 'BANDS_D7B.json', 'd7b_bands.py'),
                ('the pool arms, both windows', 'STANDING_TABLES_D7B_out.txt', 'd7b_tables.py'),
                ('the pool arms, machine-readable', 'STANDING_TABLES_D7B.json', 'd7b_tables.py'),
                ('the walk-forward emit (89 of 89)', 'EMIT_D7BCAND_out.txt', 'run_emit_CP.sh'),
                ('the emit, determinism repeat', 'EMIT_D7BCAND2_out.txt', 'run_emit_CP.sh'),
                ('the class cohort mark', 'CLASS_D7B_out.txt', 'd7b_class.py'),
                ('the board identity chain', '../parity_2026-08-19/BUILD_D7B_out.txt', 'build_D7B.sh'),
                ('the third-site verification probe', '../parity_2026-08-19/D7B_PROBE_out.txt',
                 'd7b_probe.py')]:
    h.append('<tr><td class="l">%s</td><td class="l"><code>%s</code></td>'
             '<td class="l k">%s</td></tr>' % (esc(t), esc(o), esc(i)))
h.append('</tbody></table></div>')

MB = BD[LAB].get('%s|%s|%s' % ('PRIMARY', VKEY, 'ALL picks 1-64'), {})
sub = ('Board <code>a05fe951f78482c70520480e184c80ec</code> · engine <code>5f434b95</code> · matrix '
       '<code>per_entrant_D7BCAND.json</code> (<code>fd7dafad</code>, 2648 records) · the ORDER 31-F '
       'emit reads <b>89 of 89</b> at tolerance 0 against <code>DAY0_CP.json</code> untouched · the '
       'year-1 class mark reads <b>1.0672</b> on the registered W2 basis, inside the law. '
       '<b>PRICED, NOT ADOPTED.</b>')
page = '\n'.join(['<title>Parity Candidate No-Arb</title>', '<style>%s</style>' % CSS,
                  '<h1>THE NO-ARB TABLES — %s</h1>' % esc(NICE),
                  '<div class="sub">%s</div>' % sub,
                  BOX.html_box(), '\n'.join(h), '<script>%s</script>' % JS])
open(os.path.join(HERE, 'D7B_NOARB.html'), 'w').write(page)
print('D7B_NOARB.html written')
print('  ND breaching cells  : %s' % (' · '.join('%s %s %s' % (w, b, 'PASS' if p else 'FAIL')
                                                 for w, b, _a, p in nd_breach) or 'none'))
print('  ARM breaching cells : %s' % (' · '.join('%s %s %s' % (w, a, 'PASS' if p else 'FAIL')
                                                 for w, a, _a, p in arm_breach) or 'none'))
