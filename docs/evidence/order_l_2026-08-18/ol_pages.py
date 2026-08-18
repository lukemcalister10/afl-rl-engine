#!/usr/bin/env python3
"""ORDER L — THE RE-ISSUED NO-ARB DOCUMENT.

  ORDER_L_NOARB.html   the no-arb tables again, with the two gaps the owner raised closed:
                       (1) every ND band table now exists in BOTH windows, primary and modern,
                       (2) every table also exists with the 2005 and 2006 cohorts removed, labelled
                           a sensitivity check and never as the headline.

House conventions carried from o32_pages.py (same CSS, same click-to-sort script, same column
grammar). The "what is in this board and what is still broken" box is carried over from
ORDER_K_NOARB.html BYTE FOR BYTE — it is sliced out of the published Order K file, not retyped, so
it cannot drift.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
KDIR = os.path.join(ROOT, 'docs', 'evidence', 'order_k_2026-08-18')
B = json.load(open(os.path.join(HERE, 'BANDS_L.json')))
A = json.load(open(os.path.join(HERE, 'ARMS_L.json')))
C = json.load(open(os.path.join(HERE, 'CLASS_L.json')))
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_K_MOVERS.json')))
T = J['totals']; MD = J['meta']['boards']

src = open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'o32_pages.py')).read()
CSS = src.split('CSS = """')[1].split('"""')[0]
SORT_JS = src.split('SORT_JS = """')[1].split('"""')[0]
CSS += """
.brk{background:var(--card-2);border:1px solid var(--warn);border-left:4px solid var(--warn);padding:16px 18px;margin:14px 0}
.brk h2{color:var(--warn);margin-bottom:12px}
.brk h3{font-family:var(--cond);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--text);margin:14px 0 6px}
.brk ul{margin:0 0 4px;padding-left:20px}
.brk li{margin:5px 0;color:var(--text)}
.brk li b{color:var(--warn)}
.ok{color:var(--up)}
.defs{background:var(--card-2);border:1px solid var(--edge-2);padding:14px 18px;margin:12px 0;color:var(--dim)}
.defs b{color:var(--text)}
.defs p{margin:7px 0}
.defs h2{color:var(--faint)}
.defs ul{margin:6px 0;padding-left:20px}
.defs li{margin:4px 0}
details{background:var(--card);border:1px solid var(--edge);padding:12px 18px;margin:12px 0}
summary{font-family:var(--cond);font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);cursor:pointer}
summary:hover{color:var(--volt)}
td.sell{color:var(--dn)}
td.volt{color:var(--volt)}
td.buy{color:var(--warn)}
.wrap{overflow-x:auto}
.new{background:var(--card);border:1px solid var(--volt);border-left:4px solid var(--volt);padding:16px 18px;margin:14px 0}
.new h2{color:var(--volt)}
.new p{margin:8px 0;color:var(--text)}
.sens{background:var(--card);border:1px solid var(--edge-2);border-left:4px solid var(--warn);padding:16px 18px;margin:14px 0}
.sens h2{color:var(--warn)}
tr.mod td{background:rgba(200,240,74,.04)}
td.thin{color:var(--warn)}
.tag{display:inline-block;font-family:var(--mono);font-size:9.5px;padding:1px 6px;border:1px solid var(--edge-2);color:var(--dim);margin-left:6px;vertical-align:middle}
.tag.w{border-color:var(--warn);color:var(--warn)}
.grid2{display:grid;grid-template-columns:1fr;gap:14px}
@media(min-width:1200px){.grid2{grid-template-columns:1fr 1fr}}
"""

BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
         'picks 21-30', 'picks 31-40', 'picks 41-64']
ARM_ORDER = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']
OKL, LAND, C31L = 'OKRULED', 'O35FINAL', 'O31FFINAL'
BOARDS = [(OKL, 'ORDER K f3101883 &mdash; the current candidate'),
          (LAND, 'the landing candidate 1f176444'),
          (C31L, 'candidate 31 fe6be9d6')]
WIN = [('PRIMARY', 'primary &middot; cohorts 2005-2023'), ('MODERN', 'modern &middot; cohorts 2019-2023')]
pc = lambda v: '%+.2f%%' % (100 * v)
MARK = {'ok': '', 'thin': '*', 'vthin': '**', 'none': ''}


def esc(s):
    return html.escape(str(s if s is not None else ''))


# the broken box, sliced verbatim out of the published Order K document
KHTML = open(os.path.join(KDIR, 'ORDER_K_NOARB.html')).read()
i0 = KHTML.index('<div class="brk">')
i1 = KHTML.index('</div>', KHTML.index('One thing to know about the numbers you were shown before')) + 6
BROKEN_BOX = KHTML[i0:i1]
assert BROKEN_BOX.startswith('<div class="brk">') and BROKEN_BOX.endswith('</div>')
assert 'still broken' in BROKEN_BOX


def head(title, sub):
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">NOTHING LANDS ON THIS SEAT\'S WORD &mdash; ORDER L RE-ISSUES THE '
            'TABLES ONLY. NO PRICE MOVED. NO BOARD WAS BUILT.</div>\n'
            '<div class="app">\n'
            '<header><div class="brand">ORDER <b>L</b><span class="sub">%s</span></div>'
            '<div class="spacer"></div>'
            '<div class="stamp">live <b>88ce647f</b> %s &middot; candidate 31 <b>fe6be9d6</b> %s<br>'
            'landing candidate <b>1f176444</b> %s &middot; <b>ORDER K %s</b> <b>%s</b><br>'
            'dose 0.40 &middot; kappa 0.20 &middot; eta 0.50 &middot; gamma_u 8 &middot; gamma_d 14 '
            '&middot; relief 1.08 &middot; PRE-NUMERAIRE</div></header>\n'
            % (esc(title), CSS, esc(sub), '{:,}'.format(T['live']), '{:,}'.format(T['cand31']),
               '{:,}'.format(T['landing']), MD['orderk'][:8], '{:,}'.format(T['orderk'])))


def sortable_head(tid, cols):
    o = ['<div class="wrap"><table id="%s"><thead><tr>' % tid]
    for i, (nm, num, left) in enumerate(cols):
        o.append('<th class="%s" onclick="sortTable(\'%s\',%d,%s)">%s</th>'
                 % ('l' if left else '', tid, i, 'true' if num else 'false', nm))
    o.append('</tr></thead><tbody>')
    return o


def vcls(v):
    return 'sell' if v.startswith('SELL-RED') else ('buy' if v.startswith('BUY-RED') else 'ok')


# ============================================================== the ND band table, BOTH WINDOWS
def band_table(lab, variant, tid):
    """one row per band per window: the split the owner asked for, side by side on the same row set."""
    cols = ([('#', True, False), ('band', False, True), ('window', False, True), ('n', True, False)]
            + [('yr%d' % n, True, False) for n in range(8)]
            + [('yr0&rarr;1', True, False), ('margin to the 14% rail', True, False),
               ('verdict', False, True), ('sample', False, True)])
    o = sortable_head(tid, cols)
    i = 0
    for b in BANDS:
        for w, wnice in WIN:
            d = B['nd'][lab]['%s|%s|%s' % (w, variant, b)]
            i += 1
            o.append('<tr%s><td class="num k" data-v="%d">%d</td>'
                     '<td class="l">%s</td><td class="l k">%s</td>'
                     '<td class="num k" data-v="%d">%d</td>'
                     % (' class="mod"' if w == 'MODERN' else '', i, i, b, w.lower(),
                        d['n'], d['n']))
            for v, fl in zip(d['path'], d['flags']):
                if v is None:
                    o.append('<td class="num k" data-v="-1e18">&mdash;</td>')
                else:
                    o.append('<td class="num%s" data-v="%.9f">%.3f%s</td>'
                             % (' thin' if fl in ('thin', 'vthin') else '', v, v, MARK[fl]))
            f1 = d['flags'][1]
            if d['apprec01'] is None:
                o.append('<td class="num k" data-v="-1e18">&mdash;</td>'
                         '<td class="num k" data-v="-1e18">&mdash;</td>'
                         '<td class="l k">%s</td><td class="l k">n&lt;5, not printed</td></tr>'
                         % esc(d['verdict']))
            else:
                samp = {'ok': 'full', 'thin': 'THIN (n&lt;30)', 'vthin': 'VERY THIN (n&lt;10)',
                        'none': 'n&lt;5'}[f1]
                o.append('<td class="num %s" data-v="%.6f">%s</td>'
                         '<td class="num" data-v="%.6f">%s</td>'
                         '<td class="l %s">%s</td><td class="l k">%s (n=%d at yr1)</td></tr>'
                         % (vcls(d['verdict']), d['apprec01'], pc(d['apprec01']),
                            d['buy_margin'], pc(d['buy_margin']),
                            vcls(d['verdict']), d['verdict'], samp, d['n_included'][1]))
    o.append('</tbody></table></div>')
    return '\n'.join(o)


def split_glance(lab, tid):
    """the four views on one line per band: the whole ask, compressed."""
    cols = [('#', True, False), ('band', False, True),
            ('primary &middot; all cohorts', True, False),
            ('modern &middot; all cohorts', True, False),
            ('modern minus primary', True, False),
            ('primary &middot; excl 05/06', True, False),
            ('modern &middot; excl 05/06', True, False),
            ('verdict primary', False, True), ('verdict modern', False, True)]
    o = sortable_head(tid, cols)
    for i, b in enumerate(BANDS):
        pa = B['nd'][lab]['PRIMARY|ALLCOH|%s' % b]
        ma = B['nd'][lab]['MODERN|ALLCOH|%s' % b]
        px = B['nd'][lab]['PRIMARY|EX0506|%s' % b]
        mx = B['nd'][lab]['MODERN|EX0506|%s' % b]
        gap = ma['apprec01'] - pa['apprec01']
        o.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>'
                 '<td class="num %s" data-v="%.6f">%s</td>'
                 '<td class="num %s" data-v="%.6f">%s</td>'
                 '<td class="num %s" data-v="%.6f">%+.2f</td>'
                 '<td class="num %s" data-v="%.6f">%s</td>'
                 '<td class="num %s" data-v="%.6f">%s</td>'
                 '<td class="l %s">%s</td><td class="l %s">%s</td></tr>'
                 % (i + 1, i + 1, b,
                    vcls(pa['verdict']), pa['apprec01'], pc(pa['apprec01']),
                    vcls(ma['verdict']), ma['apprec01'], pc(ma['apprec01']),
                    'dn' if gap < 0 else 'up', gap, 100 * gap,
                    vcls(px['verdict']), px['apprec01'], pc(px['apprec01']),
                    vcls(mx['verdict']), mx['apprec01'], pc(mx['apprec01']),
                    vcls(pa['verdict']), pa['verdict'], vcls(ma['verdict']), ma['verdict']))
    o.append('</tbody></table></div>')
    return '\n'.join(o)


def arm_table(lab, window, variant, tid):
    cols = ([('#', True, False), ('arm', False, True), ('n', True, False)]
            + [('yr%d' % n, True, False) for n in range(8)]
            + [('yr0&rarr;1', True, False), ('margin', True, False), ('verdict', False, True)])
    o = sortable_head(tid, cols)
    i = 0
    for arm in ARM_ORDER:
        d = A['arms'][lab].get('%s|%s|%s' % (window, variant, arm))
        if d is None:
            continue
        i += 1
        o.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>'
                 '<td class="num k" data-v="%d">%d</td>' % (i, i, arm, d['n'], d['n']))
        for v in d['path']:
            o.append('<td class="num" data-v="%s">%s</td>'
                     % (v if v is not None else -1e18, '%.3f' % v if v is not None else '&mdash;'))
        if d['apprec01'] is None:
            o.append('<td class="num k" data-v="-1e18">&mdash;</td>'
                     '<td class="num k" data-v="-1e18">&mdash;</td>'
                     '<td class="l k" style="font-size:11px">%s</td></tr>' % esc(d['verdict']))
        else:
            o.append('<td class="num %s" data-v="%.6f">%s</td><td class="num" data-v="%.6f">%s</td>'
                     '<td class="l %s">%s</td></tr>'
                     % (vcls(d['verdict']), d['apprec01'], pc(d['apprec01']),
                        d['buy_margin'], pc(d['buy_margin']), vcls(d['verdict']), d['verdict']))
    o.append('</tbody></table></div>')
    return '\n'.join(o)


def nyear_table(lab, tid):
    cols = ([('band', False, True), ('window', False, True), ('cohorts', False, True)]
            + [('n at yr%d' % n, True, False) for n in range(8)])
    o = sortable_head(tid, cols)
    for b in BANDS:
        for w, _ in WIN:
            for v, vn in (('ALLCOH', 'all'), ('EX0506', 'excl 05/06')):
                d = B['nd'][lab]['%s|%s|%s' % (w, v, b)]
                o.append('<tr><td class="l">%s</td><td class="l k">%s</td><td class="l k">%s</td>%s</tr>'
                         % (b, w.lower(), vn,
                            ''.join('<td class="num%s" data-v="%d">%d</td>'
                                    % (' thin' if fl in ('thin', 'vthin') else '', n, n)
                                    for n, fl in zip(d['n_included'], d['flags']))))
    o.append('</tbody></table></div>')
    return '\n'.join(o)


# ==================================================================================== the page
H = [head('Order L · The No-Arb Tables Re-Issued',
          'BOTH WINDOWS · WITH AND WITHOUT THE 2005/06 COHORTS')]

H.append('<div class="new"><h2>What is different about this issue, and nothing else is</h2>'
         '<p>This is Order K\'s no-arb document again. The board has not changed. No price moved. '
         'The engine, the law and the board are untouched by this order. Two things were added, '
         'because you asked for them.</p>'
         '<p><b>1. Every band table is now shown in both windows.</b> Before, only the pool-arm '
         'tables were split into "primary" and "modern". Your five draft bands appeared once, '
         'pooled across every cohort. Now every band appears twice on every table &mdash; once for '
         'the primary window and once for the modern window &mdash; using exactly the same window '
         'definition the arm tables already used.</p>'
         '<p><b>2. Every table is shown a second time with the 2005 and 2006 cohorts removed.</b> '
         'Those players are taken out of the numerator and out of the denominator, so they do not '
         'appear anywhere in that version of the table. This is a <b>sensitivity check</b>. It is '
         'not a correction and it is not the headline. The reason is written out below.</p>'
         '<p>Everything else on this page &mdash; the construction, the captions, the verdicts, the '
         'box below &mdash; is Order K\'s, unchanged. The primary tables here reproduce Order K\'s '
         'published tables digit for digit; that was checked cell by cell, 816 comparisons, zero '
         'mismatches.</p></div>')

H.append('<div class="defs" style="border-left:4px solid var(--edge-2)"><p>The box below is carried '
         'over from Order K <b>unchanged</b>. It is the same text, taken straight out of the Order K '
         'document rather than retyped, so it cannot drift.</p></div>')
H.append(BROKEN_BOX)

# ---- definitions -----------------------------------------------------------------------------------
H.append('<div class="defs"><h2>What these tables are asking, in plain words</h2>'
         '<p>Every table asks one question: <b>if you owned this group of players on draft day, and '
         'sold them a year later, would you have made money or lost it?</b></p>'
         '<p><b>yr0</b> is always 1.000. It is the group\'s own entry value, the starting point. '
         '<b>yr1</b> is what the same group is worth one year later, as a multiple of that starting '
         'point. <b>yr2</b> through <b>yr7</b> carry the same clock forward.</p>'
         '<p><b>yr0&rarr;1</b> is the first-year appreciation. This is the number the verdict is '
         'about.</p>'
         '<p><b>The 14% rail</b> is the cost of carrying a player for a year: the roster spot, the '
         'list place, the opportunity. <b>margin</b> is how much room is left before that cost is '
         'beaten.</p>'
         '<p><b>SELL-RED</b> means the group loses value in year one. You could sell on draft day, '
         'buy the same players back a year later, and keep the difference. That is an arbitrage '
         'against the board and it should not exist.</p>'
         '<p><b>BUY-RED</b> means the group gains more than 14% in year one. You could buy on draft '
         'day, carry them, and still beat the cost. That is the same arbitrage the other way.</p>'
         '<p><b>ok</b> means the group lands between those two lines, which is where a fairly priced '
         'group should land.</p>'
         '<p>The <b>five bands</b> are your bands: picks 1-10, 11-20, 21-30, 31-40, 41-64. The three '
         'above them (ALL 1-64, 1-20, 21-64) are the coarse view.</p>'
         '<p>The <b>pool arms</b> are the entry routes that are not the national draft. RD is the '
         'rookie draft, MSD the mid-season draft, SSP supplemental selection, IRE the Irish '
         'experiment, UNR unrestricted free agents, and PDA/PDN/PDS the academy and father-son '
         'pathways.</p></div>')

H.append('<div class="defs"><h2>What the two windows mean &mdash; the answer to your first question</h2>'
         '<p>A <b>cohort</b> is every player who was eligible to debut in the same year. A national '
         'draft pick taken in November 2018 first plays in 2019, so he is in the <b>2019 cohort</b>. '
         'That is the same rule the pool-arm tables have always used, and it is now used on the band '
         'tables too, so the two sets of tables can be read against each other.</p>'
         '<p><b>Primary window = cohorts 2005 to 2023.</b> On the draft clock that is the national '
         'drafts of <b>2004 to 2022</b>. This is every national-draft player the store holds, so the '
         'primary column is the total &mdash; it is the same number Order K published.</p>'
         '<p><b>Modern window = cohorts 2019 to 2023.</b> On the draft clock that is the national '
         'drafts of <b>2018 to 2022</b>. Five draft classes, 311 players.</p>'
         '<p>Every band row appears twice: the primary line, then the modern line directly under it, '
         'shaded. The tables are sortable &mdash; click any heading.</p>'
         '<p><b>Read the modern window carefully.</b> The later years hold fewer players, and not '
         'because players vanished: a player drafted in 2022 has not had a seventh season yet. At '
         'year 7 the modern window contains only the 2019 and 2020 cohorts. Every count is printed '
         'in the "n by year" table at the bottom of this page, and nothing is smoothed to hide it.</p>'
         '<p><b>Thin cells are flagged, never smoothed.</b> A cell built on fewer than 30 players '
         'carries a <b>*</b> and is coloured. Fewer than 10 carries <b>**</b>. Fewer than 5 is not '
         'printed at all &mdash; the cell shows a dash. That rule was fixed in writing before any '
         'number was computed. On this page the only flagged cells are the year-7 column of the four '
         'ten-pick bands in the modern window, each built on 20 players. <b>Every year-1 cell on '
         'every table &mdash; the cell the verdict is about &mdash; is built on 50 players or more.</b></p>'
         '</div>')

H.append('<div class="sens"><h2>The 2005 and 2006 cohorts &mdash; what was removed, and why this is '
         'a sensitivity check and not a correction</h2>'
         '<p><b>What was removed, in plain words.</b> The 2005 and 2006 cohorts are taken out of the '
         'population entirely. Not their first two seasons &mdash; the players themselves, out of '
         'the year-1 average and out of the entry average alike, everywhere they would otherwise '
         'appear. If this is not what you meant, say so and it will be reissued the other way.</p>'
         '<p><b>Which players those are.</b> On the cohort clock, the 2005 and 2006 cohorts are the '
         'national drafts of <b>2004 and 2005</b>. That is 125 of the 1,200 national-draft players. '
         'The identification was made against the numbers you read, not against a label: those two '
         'classes are the ones that mark <b>0.899</b> and <b>0.856</b> on the year-1 class measure '
         'for this board.</p>'
         '<p><b>Why this is a sensitivity check.</b> You asked because there is a documented data '
         'gap in exactly those years. Fifty-one season rows were back-filled from your own corrected '
         'sheet (14 in 2005, 37 in 2006), and 177 more seasons you confirmed as zero games are held '
         'under the convention that a zero-game season carries no row. Two checks have already been '
         'run on that. First, the number of season rows per player for those classes matches every '
         'other class &mdash; 3.2 to 3.4 rows per player across years 1 to 5. Second, the engine '
         'treats a missing season and a confirmed zero-game season identically, so the no-row '
         'convention does not bias the price. On that evidence the two classes are not known to be '
         'wrong, so removing them is a <b>what-if</b>, not a repair. The headline number on every '
         'table below is still the one with every cohort in it.</p>'
         '<p><b>It changes nothing in the modern window.</b> The modern window starts at the 2019 '
         'cohort, so it never contained a 2005 or 2006 player. That was stated in writing before the '
         'run and then checked: every modern cell is identical to the last decimal place, with and '
         'without the exclusion.</p></div>')

# ---- the current candidate -------------------------------------------------------------------------
H.append('<div class="box"><h2>The current candidate &middot; ORDER K %s &middot; the split at a '
         'glance</h2>'
         '<div class="defs" style="margin-top:0"><p>One line per band. The first two columns are the '
         'answer to your question: <b>primary is the total, modern is the recent era.</b> The last '
         'two columns are the same two windows with the 2005 and 2006 cohorts removed &mdash; the '
         'sensitivity check. The modern column and the modern-excluded column are identical by '
         'construction, and that is the check, not a copy-paste error.</p></div>%s</div>'
         % (MD['orderk'][:8], split_glance(OKL, 'g1')))

H.append('<div class="box"><h2>The current candidate &middot; every cohort &middot; full year paths, '
         'both windows</h2>%s'
         '<div class="defs"><p>This is the headline table. Each band appears twice: the primary '
         'line, then the modern line, shaded. <b>*</b> means the cell rests on fewer than 30 '
         'players.</p></div></div>' % band_table(OKL, 'ALLCOH', 'n1'))

H.append('<div class="sens"><h2>SENSITIVITY ONLY &middot; the current candidate with the 2005 and '
         '2006 cohorts removed</h2>'
         '<div class="defs" style="margin-top:0"><p>This table is <b>not</b> the board\'s number. It '
         'is the same table with 125 players taken out, to show how much of the picture rests on '
         'those two classes.</p></div>%s</div>' % band_table(OKL, 'EX0506', 'n2'))

# ---- comparison boards ------------------------------------------------------------------------------
for lab, nice in ((LAND, 'the landing candidate 1f176444'), (C31L, 'candidate 31 fe6be9d6')):
    H.append('<div class="box"><h2>Comparison board &middot; %s &middot; the split at a glance</h2>%s</div>'
             % (nice, split_glance(lab, 'g%s' % lab)))
    H.append('<details><summary>%s &mdash; full year paths, both windows, both variants</summary>'
             '<div class="box"><h2>%s &middot; every cohort</h2>%s</div>'
             '<div class="sens"><h2>%s &middot; SENSITIVITY: 2005/06 cohorts removed</h2>%s</div>'
             '</details>'
             % (nice, nice, band_table(lab, 'ALLCOH', 'b%sA' % lab),
                nice, band_table(lab, 'EX0506', 'b%sX' % lab)))

# ---- the pool arms ----------------------------------------------------------------------------------
H.append('<div class="box"><h2>The pool arms &middot; ORDER K &middot; primary window 2005-2023 '
         '&middot; every cohort</h2>%s</div>' % arm_table(OKL, 'PRIMARY', 'ALLCOH', 'a1'))
H.append('<div class="box"><h2>The pool arms &middot; ORDER K &middot; modern window 2019-2023 '
         '&middot; every cohort</h2>%s'
         '<div class="defs"><p>The modern window carries small samples on the arms. Read it as a '
         'direction, not a measurement. The mid-season draft has no year-1 cell at all, because an '
         'MSD player debuts in his own draft year; those rows are excluded from that year and '
         'counted, never scored zero. Southern academy (PDS) has no players in the modern window at '
         'all, so it does not appear.</p></div></div>' % arm_table(OKL, 'MODERN', 'ALLCOH', 'a2'))
H.append('<div class="sens"><h2>SENSITIVITY ONLY &middot; the pool arms with the 2005 and 2006 '
         'cohorts removed</h2>'
         '<div class="defs" style="margin-top:0"><p>Only three arms have any 2005 or 2006 cohort '
         'members at all: the rookie draft (623 falls to 531), the Irish experiment (47 to 45), and '
         'therefore the pooled all-pool line (1,016 to 922). Every other arm is unchanged to the '
         'last decimal, because it had no players in those two years. The modern window is unchanged '
         'throughout, for the same reason as the band tables.</p></div>'
         '<h2 style="margin-top:14px">primary window &middot; excl 05/06</h2>%s'
         '<h2 style="margin-top:14px">modern window &middot; excl 05/06</h2>%s</div>'
         % (arm_table(OKL, 'PRIMARY', 'EX0506', 'a3'), arm_table(OKL, 'MODERN', 'EX0506', 'a4')))

H.append('<details><summary>Archive &mdash; the comparison boards\' pool-arm tables, all four views</summary>')
for lab, nice in ((LAND, 'the landing candidate 1f176444'), (C31L, 'candidate 31 fe6be9d6')):
    for w, wn in (('PRIMARY', 'primary'), ('MODERN', 'modern')):
        for v, vn in (('ALLCOH', 'every cohort'), ('EX0506', 'SENSITIVITY: excl 05/06')):
            H.append('<div class="box"><h2>%s &middot; %s window &middot; %s</h2>%s</div>'
                     % (nice, wn, vn, arm_table(lab, w, v, 'z%s%s%s' % (lab, w, v))))
H.append('</details>')

# ---- the class mark ---------------------------------------------------------------------------------
CK = C['ok_class']; W2 = C['w2']
H.append('<div class="box"><h2>The year-1 class mark, on the same exclusion basis</h2>'
         '<div class="defs" style="margin-top:0">'
         '<p>This is a different measurement from the tables above, and it answers a different '
         'question: <b>across the historical intake classes, how much did a class gain in its first '
         'year?</b> Each class gets one number &mdash; the total year-1 price of the class divided '
         'by its total entry price. The published mark is the average of those class numbers over '
         'eleven classes, 2005 to 2015.</p>'
         '<p>The 2005 and 2006 classes here are the same two the tables above remove: the national '
         'drafts of 2004 and 2005. Taking them out leaves nine classes, 2007 to 2015.</p></div>')
H.append('\n'.join(sortable_head('cm', [('board', False, True), ('standing mark', True, False),
                                        ('classes', True, False),
                                        ('excl 05/06', True, False), ('classes', True, False),
                                        ('move', True, False)])))
for lab, nice in BOARDS:
    m = CK[lab]
    H.append('<tr><td class="l">%s</td><td class="num%s" data-v="%.6f">%.4f</td>'
             '<td class="num k" data-v="11">11</td>'
             '<td class="num" data-v="%.6f">%.4f</td><td class="num k" data-v="9">9</td>'
             '<td class="num up" data-v="%.6f">%+.4f</td></tr>'
             % (nice, ' volt' if lab == OKL else '', m['mean_0515'], m['mean_0515'],
                m['mean_0715_ex0506'], m['mean_0715_ex0506'],
                m['mean_0715_ex0506'] - m['mean_0515'],
                m['mean_0715_ex0506'] - m['mean_0515']))
H.append('</tbody></table></div>'
         '<div class="defs"><p>The supervisor computed <b>1.0669</b> for the current candidate on '
         'this basis. This run reproduces it: <b>%.4f</b>. The two agree to within the rounding of '
         'the published four-decimal class rows.</p></div></div>' % CK[OKL]['mean_0715_ex0506'])

H.append('<div class="box"><h2>Every class, printed &middot; the year-1 mark class by class</h2>')
H.append('\n'.join(sortable_head('pcl', [('class', True, False), ('national draft', True, False),
                                         ('ORDER K', True, False), ('landing candidate', True, False),
                                         ('candidate 31', True, False), ('n', True, False),
                                         ('in the mark?', False, True)])))
for y in range(2005, 2022):
    ky = str(y)
    tag = ('<b style="color:var(--warn)">removed by the sensitivity</b>' if y in (2005, 2006)
           else ('in the mark' if 2005 <= y <= 2015 else '&mdash;'))
    vals = [CK[l]['per_class'][ky] for l, _ in BOARDS]
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="num k" data-v="%d">%d</td>'
             '%s<td class="num k" data-v="%d">%d</td><td class="l">%s</td></tr>'
             % (y, y, y - 1, y - 1,
                ''.join('<td class="num%s" data-v="%.6f">%.4f</td>'
                        % (' dn' if v < 1.0 else '', v, v) for v in vals),
                CK[OKL]['n_per_class'][ky], CK[OKL]['n_per_class'][ky], tag))
H.append('</tbody></table></div>'
         '<div class="defs"><p>The two removed classes are the only two in the whole mark window '
         'that sit below 1.00. Every other class in the window reads between 1.006 and 1.136. That '
         'is the pattern that prompted the question.</p></div></div>')

# ---- the W2 instrument answer -----------------------------------------------------------------------
H.append('<div class="new"><h2>Which instrument the 1.03 floor is measured against &mdash; the '
         'question that decides whether this board clears it comfortably or barely</h2>'
         '<p><b>The floor itself was not computed on any instrument.</b> The 1.03 floor and the ~1.08 '
         'ideal are your own prior, recorded as Ruling R-CAL on 2026-08-17 and written into the W2 '
         'pre-registration before a single number was run. The pre-registration calls it "a LOOSE '
         'PRIOR, not a target". So the question is really: <b>what did the seat measure the board '
         'against that prior with?</b></p>'
         '<p><b>The answer is the full built walk-forward matrix.</b> Not the fast navigation '
         'calibrator. The W2 pre-registration names "the walk-forward per-entrant matrix" as its '
         'primary object and pins its md5 before the run. The scorer computes each class mark as '
         '<code>R_cand = P1 / P0</code>, where <code>P1</code> is the sum of each player\'s '
         '<code>vpath[0]</code> &mdash; the engine\'s own walk-forward year-1 valuation &mdash; and '
         '<code>P0</code> is the sum of entry prices. The gate G1 that the boards are scored on was '
         'registered as that scorer\'s <code>mean_0515</code>, and its recorded value for the '
         'landing candidate, 1.0421, is that scorer\'s output on the built matrix.</p>'
         '<p><b>So what is 1.0324?</b> It is the same kind of number on a <b>different set of draft '
         'classes</b>. The Order K class script labels a class by the year it could first debut '
         '(cohort clock) and averages classes 2005-2015, which are the national drafts of '
         '<b>2004-2014</b>. The W2 scorer labels a class by its draft year and averages 2005-2015, '
         'which are the national drafts of <b>2005-2015</b>. The two windows are shifted by one year '
         'at both ends.</p>'
         '<p><b>That shift is the whole gap.</b> Take Order K\'s own class rows and average them over '
         'the same draft classes the W2 scorer uses, and the two land on the same number to five '
         'decimal places, on all three boards. There is no instrument disagreement to reconcile.</p>')
H.append('\n'.join(sortable_head('w2t', [('board', False, True),
                                         ('Order K cohort 2005-2015', True, False),
                                         ('same rows, draft 2005-2015', True, False),
                                         ('W2 scorer, draft 2005-2015', True, False),
                                         ('difference', True, False),
                                         ('margin over the 1.03 floor', True, False)])))
for lab, nice in BOARDS:
    al = sum(CK[lab]['per_class'][str(y)] for y in range(2006, 2017)) / 11.0
    w = W2[lab]['mean_0515']
    H.append('<tr><td class="l">%s</td><td class="num" data-v="%.6f">%.4f</td>'
             '<td class="num" data-v="%.6f">%.4f</td><td class="num volt" data-v="%.6f">%.4f</td>'
             '<td class="num k" data-v="%.9f">%.5f</td>'
             '<td class="num up" data-v="%.6f">%+.4f</td></tr>'
             % (nice, CK[lab]['mean_0515'], CK[lab]['mean_0515'], al, al, w, w,
                al - w, al - w, w - 1.03, w - 1.03))
H.append('</tbody></table></div>'
         '<p><b>What this means for your floor.</b> On the instrument the gate was actually '
         'registered on, the current candidate reads <b>%.4f</b>, which clears the 1.03 floor by '
         '<b>%+.4f</b> &mdash; comfortably, not barely. The 1.0324 figure is not wrong; it is a '
         'different class window and it should not be read against the W2 floor. The fast navigation '
         'calibrator reads 1.0515 on this board, which is the built matrix\'s %.4f to within '
         '0.0002 &mdash; the navigation instrument is an accurate stand-in for the built matrix, not '
         'a rival to it.</p>'
         '<p>On the sensitivity basis, with the 2005 and 2006 cohorts removed, the same numbers are '
         '<b>%.4f</b> on the Order K window and <b>%.4f</b> on the W2 window. Neither is the '
         'headline.</p></div>'
         % (W2[OKL]['mean_0515'], W2[OKL]['mean_0515'] - 1.03, W2[OKL]['mean_0515'],
            CK[OKL]['mean_0715_ex0506'], W2[OKL]['mean_ex0506']))

# ---- disclosure ------------------------------------------------------------------------------------
H.append('<details><summary>Sample sizes &mdash; every band, every window, every year, nothing hidden</summary>'
         '<div class="defs"><p>The count of players actually included in each cell. A count falls in '
         'the later years because a player drafted recently has not had that season yet, not because '
         'anyone was dropped. Amber means the cell is flagged thin.</p></div>'
         '<div class="box"><h2>ORDER K %s</h2>%s</div>'
         '<div class="box"><h2>the landing candidate</h2>%s</div>'
         '<div class="box"><h2>candidate 31</h2>%s</div></details>'
         % (MD['orderk'][:8], nyear_table(OKL, 'ny1'), nyear_table(LAND, 'ny2'),
            nyear_table(C31L, 'ny3')))

H.append('<div class="defs"><h2>How this page was made</h2>'
         '<p>Nothing was rebuilt. The three boards are the three walk-forward matrices Order K '
         'already built. The population filter, the value rules and the window definitions were '
         'taken from the instruments that were already disclosed and pinned: the extended band '
         'instrument (md5 d59ad550&hellip;), the canonical table (0f822035&hellip;), the all-arm '
         'cohort instrument, and the Order-29 harness. Order L added one thing to each of them: a '
         'filter on which cohorts are counted.</p>'
         '<p>Four checks were registered in writing before any number was computed, and all four '
         'were run. The primary tables reproduce Order K\'s published tables digit for digit (816 '
         'comparisons, zero mismatches). The two clocks agree on every row. The exclusion moves '
         'nothing in the modern window (exactly zero). The class arithmetic reproduces the '
         'supervisor\'s 1.0669.</p>'
         '<p>Files: <code>docs/evidence/order_l_2026-08-18/</code> &mdash; PREREG_L.md, PACKET_L.md, '
         'ol_bands.py, ol_arms.py, ol_class.py, ol_selfcheck.py, ol_pages.py, and the raw console '
         'output of every run.</p></div>')

H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_L_NOARB.html'), 'w').write('\n'.join(H))
print('wrote ORDER_L_NOARB.html  (%d bytes)'
      % os.path.getsize(os.path.join(HERE, 'ORDER_L_NOARB.html')))
