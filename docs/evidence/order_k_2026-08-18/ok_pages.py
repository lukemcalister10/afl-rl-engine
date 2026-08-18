#!/usr/bin/env python3
"""ORDER K — THE THREE DOCUMENTS THE OWNER ASKED FOR.

  ORDER_K_PLAYERS.html  the player list — all 804 rows, four board columns, deltas, mechanism legs
  ORDER_K_YEAR1.html    the year-1 class in draft order, the four board columns PLUS v0
  ORDER_K_NOARB.html    the no-arb tables — year paths yr0-7, appreciation, margin, verdict per band,
                        the owner's five bands PLUS ALL / 1-20 / 21-64, the pool-arm table on BOTH
                        windows, definitions written on the page, the landing candidate and
                        candidate 31 as comparison columns, history collapsed into an archive.

House conventions carried verbatim from o32_pages.py: same CSS, same click-to-sort script, same
column grammar, rank column, definitions in plain words on the page.

EVERY PAGE CARRIES THE SAME "WHAT IS IN THIS BOARD AND WHAT IS STILL BROKEN" BOX AT THE TOP.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_K_MOVERS.json')))
ROWS = J['rows']; T = J['totals']; MD = J['meta']['boards']
ST = json.load(open(os.path.join(HERE, 'STANDING_TABLES_K.json')))
GK = json.load(open(os.path.join(HERE, 'GATES_K.json')))
CK = json.load(open(os.path.join(HERE, 'CLASS_K.json')))
FD = json.load(open(os.path.join(HERE, 'FADE_K.json')))
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
details{background:var(--card);border:1px solid var(--edge);padding:12px 18px;margin:12px 0}
summary{font-family:var(--cond);font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);cursor:pointer}
summary:hover{color:var(--volt)}
.pill{display:inline-block;font-family:var(--mono);font-size:10px;padding:2px 7px;border:1px solid var(--edge-2);color:var(--dim);margin-right:6px}
.pill.red{border-color:var(--dn);color:var(--dn)}
.pill.grn{border-color:var(--up);color:var(--up)}
.pill.amb{border-color:var(--warn);color:var(--warn)}
td.sell{color:var(--dn)}
td.buy{color:var(--warn)}
"""

Y1 = [r for r in ROWS if r['yr'] == 2025 or (r['yr'] == 2026 and r['pathway'] == 'MSD')]
K = GK['kfloor']
ND = ST['nd']; ARMS = ST['arms']
LAND, C31L, OKL = 'O35FINAL', 'O31FFINAL', 'OKRULED'
BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
         'picks 21-30', 'picks 31-40', 'picks 41-64']
ARM_ORDER = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']
pc = lambda v: '%+.2f%%' % (100 * v)


def esc(s):
    return html.escape(str(s if s is not None else ''))


def head(title, sub):
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">NOTHING LANDS ON THIS SEAT\'S WORD &mdash; ORDER K IS THE OWNER\'S '
            'RULED SETTING BUILT FOR REVIEW, WITH ONE DEFECT FIXED. IT IS NOT ADOPTED.</div>\n'
            '<div class="app">\n'
            '<header><div class="brand">ORDER <b>K</b><span class="sub">%s</span></div>'
            '<div class="spacer"></div>'
            '<div class="stamp">live <b>88ce647f</b> %s &middot; candidate 31 <b>fe6be9d6</b> %s<br>'
            'landing candidate <b>1f176444</b> %s &middot; <b>ORDER K %s</b> <b>%s</b><br>'
            'dose 0.40 &middot; kappa 0.20 &middot; eta 0.50 &middot; gamma_u 8 &middot; gamma_d 14 '
            '&middot; relief 1.08 &middot; PRE-NUMERAIRE</div></header>\n'
            % (esc(title), CSS, esc(sub), '{:,}'.format(T['live']), '{:,}'.format(T['cand31']),
               '{:,}'.format(T['landing']), MD['orderk'][:8], '{:,}'.format(T['orderk'])))


def broken_box():
    dean = GK['g10']['harry-dean']; cdt = GK['g10']['cooper-duff-tytler']
    b3140 = ND[OKL]['picks 31-40']['apprec01']; b4164 = ND[OKL]['picks 41-64']['apprec01']
    ssp = ARMS[OKL]['PRIMARY|SSP']['apprec01']; ssp0 = ARMS[LAND]['PRIMARY|SSP']['apprec01']
    return ('<div class="brk"><h2>What is in this board, and what is still broken</h2>'
            '<p>Read this before you read a single price. It is the same box on all three pages.</p>'

            '<h3>What is wired into this board</h3><ul>'
            '<li><b>The setting you chose.</b> The age-referenced projection bar at dose 0.40, the '
            'counterweight at kappa 0.20 / gamma_u 8 / eta 0.50 / gamma_d 14, and the selection '
            'relief at 1.08. Nothing here was re-searched or re-tuned.</li>'
            '<li><b>Your tall/small sitter factor.</b> Key-position defenders, key-position forwards '
            'and rucks sit out more often than smalls do, so a year on the sidelines costs them less. '
            'That is live.</li>'
            '<li><b>One defect fixed: the fade floor.</b> The fade curve had a hard floor at 0.5. '
            'After the tall factor was applied, small players drafted between picks 6 and 18 fell '
            'through that floor and came out <i>lighter</i> than before &mdash; they were being PAID '
            'by a relief meant only for talls. Seven real players gained 126 points that way, Josh '
            'Smillie most of all at +79. The floor is now sited at each small player\'s own '
            'pre-factor value, so no small can ever be made lighter by the tall factor again. '
            'Smillie is back at <b>772</b>. The four talls you named keep their relief in full: '
            'Will Green +141, Toby Conway +86, William McCabe +70, Alex Dodson +16.</li>'
            '<li><b>Everything the landing candidate already had.</b> Turn the dial off and this '
            'engine rebuilds the landing candidate 1f176444 byte for byte.</li>'
            '</ul>'

            '<h3>What is still broken &mdash; open defects, none of them fixed here</h3><ul>'
            '<li><b>Late picks still lose money in year one.</b> Picks 31-40 read <b>%s</b> and picks '
            '41-64 read <b>%s</b>. Both improved (by %.2f and %.2f points), and both are still '
            'negative. A player drafted there is still worth less a year later. This is a known '
            'limitation of this build, not a failure of it &mdash; no setting inside your rules '
            'reaches zero on either band.</li>'
            '<li><b>Harry Dean and Cooper Duff-Tytler are still below their candidate-31 levels.</b> '
            'Dean reads <b>%d</b> against 2,670 on candidate 31 (%d short). Duff-Tytler reads '
            '<b>%d</b> against 1,832 (%d short) &mdash; and he is also <b>below</b> the landing '
            'candidate\'s 1,572. The age bar lifts them both, and this setting\'s counterweight takes '
            'most of it back: Dean +221 then -218, Duff-Tytler +85 then -152.</li>'
            '<li><b>Supplemental selection (SSP) players still appreciate about 50%% in their first '
            'year.</b> %s on this board, %s on the landing candidate. They enter outside the 1-64 '
            'pick curve, so nothing in this order reaches them. It is a known, separate problem.</li>'
            '<li><b>The development arms still lose money.</b> Next-generation academy %s, '
            'next-generation northern %s, southern %s, unrestricted free agents %s, all in year one.</li>'
            '<li><b>Veteran key-position talls aged 28-30 are over-priced by roughly 30%%, because '
            'the veteran board is parked.</b> Nothing in this order touches them. If you are reading '
            'a 28-year-old key forward or key defender, read him about a third lighter than the '
            'number shown.</li>'
            '<li><b>The engine leans too hard on the most recent season.</b> A player who broke out '
            'once is probably too expensive here &mdash; <b>Xerri, Callaghan, Ash, Thilthorpe</b>. A '
            'good player who had one bad year is probably too cheap &mdash; <b>Coniglio, De Goey, '
            'Langford</b>. Treat those names with your own judgement, not the number.</li>'
            '<li><b>The ceiling column on the dial page is wrong for anyone 22 or older.</b> It '
            'prints roughly the 87th percentile outcome where it should print the 97th. It reads too '
            'low for those players.</li>'
            '</ul>'

            '<h3>Two gates this build BREACHES, reported and not traded away</h3><ul>'
            '<li><b>Daniel Annable rises when he should not.</b> Your law says a player who is below '
            'expectation but has played games must not go up. He goes from 1,530 to <b>1,537</b>, up '
            '7 points. The other two hold: Xavier Taylor -14, Dylan Patterson -27. The cause is that '
            'the age bar lifts him +40 and this setting\'s counterweight only charges him -33 back. '
            'It is a small number and it is still a breach.</li>'
            '<li><b>The veteran-movement cap is breached on the net measure.</b> Order J\'s '
            'preregistered rule allowed the young-player levers to move the veteran pool by at most '
            '668 board points net. The two gated levers move it <b>-695</b>. The churn measure is '
            'inside its cap (695 against 1,002) and the age bar alone moves <b>zero</b> mature rows, '
            'which is its own law and it holds exactly. The breach is entirely the counterweight, '
            'which keys on games played rather than age.</li>'
            '</ul>'

            '<h3>One thing to know about the numbers you were shown before</h3>'
            '<p>The frontier values quoted when you chose this setting (class 1.0519, picks 1-10 '
            '+7.58%%, 11-20 +13.82%%, 31-40 -8.54%%, 41-64 -6.50%%) were computed on the fast '
            'navigation instrument AND on the fade curve with the defective floor still in it. They '
            'are not what the real board reads. The real board, on the standing instrument, reads '
            '<b>1-10 +8.22%% &middot; 11-20 +11.16%% &middot; 21-30 +5.26%% &middot; 31-40 -10.70%% '
            '&middot; 41-64 -6.89%%</b>. Every one of those is better than the landing candidate. '
            'They are not the predicted numbers and this page does not pretend they are.</p>'
            '</div>'
            % (pc(b3140), pc(b4164),
               100 * (b3140 - ND[LAND]['picks 31-40']['apprec01']),
               100 * (b4164 - ND[LAND]['picks 41-64']['apprec01']),
               dean['orderK'], dean['short_of_c31'], cdt['orderK'], cdt['short_of_c31'],
               pc(ssp), pc(ssp0),
               pc(ARMS[OKL]['PRIMARY|PDA']['apprec01']), pc(ARMS[OKL]['PRIMARY|PDN']['apprec01']),
               pc(ARMS[OKL]['PRIMARY|PDS']['apprec01']), pc(ARMS[OKL]['PRIMARY|UNR']['apprec01'])))


def num_td(v, cls=''):
    return '<td class="num %s" data-v="%s">%s</td>' % (cls, v, '{:,}'.format(int(v)))


def delta_td(v):
    if v is None:
        return '<td class="k">&mdash;</td>'
    c = 'up' if v > 0 else ('dn' if v < 0 else '')
    return '<td class="num %s" data-v="%d">%+d</td>' % (c, v, v)


# ==================================================================== 1. THE PLAYER LIST
cols = [('#', True), ('player', False), ('pathway', False), ('pos', False), ('age', True),
        ('pick', True), ('games', True),
        ('live 88ce647f', True), ('cand 31 fe6be9d6', True), ('landing 1f176444', True),
        ('ORDER K', True),
        ('&Delta; vs landing', True), ('&Delta; vs c31', True), ('&Delta; vs live', True),
        ('leg tall', True), ('leg age-bar', True), ('leg counterweight', True),
        ('leg floor fix', True), ('interaction', True)]
H = [head('Order K · The Player List', 'ALL 804 PRICED ROWS · FOUR BOARDS · THE LEGS')]
H.append(broken_box())
H.append('<div class="defs"><h2>What each column means</h2>'
         '<p><b>live 88ce647f</b> &mdash; the price on the board your league is using today.</p>'
         '<p><b>cand 31 fe6be9d6</b> &mdash; the earlier candidate board, kept so you can see how far '
         'a row has travelled.</p>'
         '<p><b>landing 1f176444</b> &mdash; the landing candidate. This is the base. Every gate in '
         'this order is scored against it.</p>'
         '<p><b>ORDER K</b> &mdash; this build: your ruled setting, with the fade floor fixed.</p>'
         '<p><b>leg tall</b> &mdash; how much of the move is the tall/small sitter factor on its own. '
         'Positive means the factor made him cheaper to leave sitting, so he is worth more.</p>'
         '<p><b>leg age-bar</b> &mdash; how much is the age-referenced projection bar at dose 0.40 on '
         'its own. It compares a young player to what a player of HIS age normally produces, instead '
         'of to a flat league bar.</p>'
         '<p><b>leg counterweight</b> &mdash; how much the counterweight adds or takes off after the '
         'age bar has been applied. It moves weight off draft pedigree and onto what the player has '
         'actually shown, and charges the pedigree down as games accumulate. This is the leg that '
         'takes back most of the age bar\'s lift on high-pick, low-games rows.</p>'
         '<p><b>leg floor fix</b> &mdash; what the fade-floor fix itself is worth on this row. It is '
         'zero for almost everyone and negative for the seven smalls the defect was paying.</p>'
         '<p><b>interaction</b> &mdash; the legs are each priced as a real board, so they do not add '
         'up exactly. This column is the leftover. It is shown rather than hidden.</p>'
         '<p>Every column header sorts. Click once for one direction, again for the other.</p></div>')
rs = sorted(ROWS, key=lambda r: -r['orderk'])
H.append('<div class="box"><h2>All %d priced rows &middot; click any column to sort</h2>' % len(rs))
H.append('<table id="t1"><thead><tr>')
for i, (nm, num) in enumerate(cols):
    H.append('<th class="%s" onclick="sortTable(\'t1\',%d,%s)">%s</th>'
             % ('l' if nm in ('player', 'pathway', 'pos') else '', i, 'true' if num else 'false', nm))
H.append('</tr></thead><tbody>')
for i, r in enumerate(rs):
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td><td class="l k">%s</td>'
             '<td class="l k">%s</td><td class="num" data-v="%d">%d</td>'
             '<td class="num k" data-v="%s">%s</td><td class="num" data-v="%d">%d</td>'
             % (i + 1, i + 1, esc(r['name'] or r['key']), esc(r['pathway'] or '?'), esc(r['pos']),
                r['age'], r['age'], (r['pick'] if r['pick'] else 999),
                (r['pick'] if r['pick'] else '&mdash;'), int(r['g']), int(r['g'])))
    for f in ('live', 'cand31', 'landing', 'orderk'):
        H.append(num_td(r[f], 'volt' if f == 'orderk' else ''))
    for f in ('d_vs_landing', 'd_vs_cand31', 'd_vs_live'):
        H.append(delta_td(r[f]))
    for f in ('leg_tall', 'leg_s1', 'leg_cw', 'leg_floor', 'residual'):
        H.append(delta_td(r[f]))
    H.append('</tr>')
H.append('</tbody></table></div>')
H.append('<div class="box"><h2>Board totals</h2><table><thead><tr><th class="l">board</th>'
         '<th>total board points</th><th>vs the landing candidate</th></tr></thead><tbody>')
for nm, f in (('live 88ce647f', 'live'), ('candidate 31 fe6be9d6', 'cand31'),
              ('landing candidate 1f176444', 'landing'), ('ORDER K %s' % MD['orderk'][:8], 'orderk')):
    H.append('<tr><td class="l">%s</td><td class="num">%s</td><td class="num">%+d</td></tr>'
             % (nm, '{:,}'.format(T[f]), T[f] - T['landing']))
H.append('</tbody></table></div>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_K_PLAYERS.html'), 'w').write('\n'.join(H))
print('wrote ORDER_K_PLAYERS.html  (%d rows)' % len(rs))

# ==================================================================== 2. THE YEAR-1 CLASS
PATH_ORDER = {'ND': 0, 'RD': 1, 'PDA': 2, 'PDN': 3, 'PDS': 4, 'IRE': 5, 'UNR': 6, 'SSP': 7, 'MSD': 8}


def y1key(r):
    return (PATH_ORDER.get(r['pathway'], 9), r['pick'] if r['pick'] else 999, -r['orderk'])


ys = sorted(Y1, key=y1key)
H = [head('Order K · The Year-1 Class', 'THE 2025 INTAKE IN DRAFT ORDER · WITH v0')]
H.append(broken_box())
H.append('<div class="defs"><h2>How to read this page</h2>'
         '<p>These are the players who entered the league in the most recent intake &mdash; the class '
         'whose first-year appreciation your growth rule is written about. They are listed in draft '
         'order: national draft by pick number first, then the rookie draft, then the academy and '
         'father-son pathways, then supplemental selection, then the mid-season draft.</p>'
         '<p><b>v0</b> is the entry value &mdash; what the engine says the pick itself was worth on '
         'draft day, before the player had done anything. <b>Entry values do not move in this order.</b> '
         'All 89 wired entrants carry a bit-identical v0. What moves is the printed price of a player '
         'who has since sat out, because that price is his entry value multiplied by a sitting '
         'discount, and the sitting discount is exactly what the tall/small factor changes.</p>'
         '<p>The four price columns and the legs mean the same as on the player list.</p></div>')
H.append('<div class="box"><h2>%d rows in the year-1 class &middot; %s &rarr; %s board points '
         '(%+.2f%%) &middot; %d up, %d down</h2>'
         % (len(ys), '{:,}'.format(GK['year1']['landing']), '{:,}'.format(GK['year1']['orderK']),
            100 * (GK['year1']['orderK'] - GK['year1']['landing']) / max(1, GK['year1']['landing']),
            sum(1 for r in ys if r['d_vs_landing'] > 0), sum(1 for r in ys if r['d_vs_landing'] < 0)))
c2 = [('#', True), ('player', False), ('pathway', False), ('pick', True), ('pos', False),
      ('age', True), ('games', True), ('v0 (entry value)', True),
      ('live 88ce647f', True), ('cand 31 fe6be9d6', True), ('landing 1f176444', True),
      ('ORDER K', True), ('&Delta; vs landing', True), ('&Delta; vs c31', True),
      ('leg tall', True), ('leg age-bar', True), ('leg counterweight', True), ('leg floor fix', True)]
H.append('<table id="t2"><thead><tr>')
for i, (nm, num) in enumerate(c2):
    H.append('<th class="%s" onclick="sortTable(\'t2\',%d,%s)">%s</th>'
             % ('l' if nm in ('player', 'pathway', 'pos') else '', i, 'true' if num else 'false', nm))
H.append('</tr></thead><tbody>')
for i, r in enumerate(ys):
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td><td class="l k">%s</td>'
             '<td class="num k" data-v="%s">%s</td><td class="l k">%s</td>'
             '<td class="num" data-v="%d">%d</td><td class="num" data-v="%d">%d</td>'
             '<td class="num k" data-v="%.1f">%s</td>'
             % (i + 1, i + 1, esc(r['name'] or r['key']), esc(r['pathway'] or '?'),
                (r['pick'] if r['pick'] else 999), (r['pick'] if r['pick'] else '&mdash;'),
                esc(r['pos']), r['age'], r['age'], int(r['g']), int(r['g']),
                r['v0'], '{:,.0f}'.format(r['v0'])))
    for f in ('live', 'cand31', 'landing', 'orderk'):
        H.append(num_td(r[f], 'volt' if f == 'orderk' else ''))
    for f in ('d_vs_landing', 'd_vs_cand31', 'leg_tall', 'leg_s1', 'leg_cw', 'leg_floor'):
        H.append(delta_td(r[f]))
    H.append('</tr>')
H.append('</tbody></table></div>')
H.append('<div class="box"><h2>The class growth rule &middot; how the whole class prices a year on</h2>'
         '<div class="defs"><p>Your rule: the year-1 class cohort must GROW, must clear a floor of '
         '1.03, and must stay strictly under the 1.14 buy rail. Your stated ideal of about 1.08 is '
         'known to be out of reach at any setting inside your other rules; the number is reported and '
         'never chased. Below are three readings of the same object on the same boards, so the '
         'instrument is separated from the build.</p></div>'
         '<table><thead><tr><th class="l">reading</th><th>landing candidate</th><th>candidate 31</th>'
         '<th>ORDER K</th><th>move</th></tr></thead><tbody>')
for nm, d in (('built walk-forward matrix, every eligible row', CK['readings']['all_rows']),
              ('built matrix, the calibrator\'s own 1,986 teaching rows',
               CK['readings']['calibrator_population'])):
    H.append('<tr><td class="l">%s</td><td class="num">%.4f</td><td class="num">%.4f</td>'
             '<td class="num volt">%.4f</td><td class="num up">%+.4f</td></tr>'
             % (nm, d[LAND], d[C31L], d[OKL], d[OKL] - d[LAND]))
a = CK['readings']['analytic_calibrator']
H.append('<tr><td class="l">the fast navigation instrument (the number quoted when you chose)</td>'
         '<td class="num">%.4f</td><td class="num k">&mdash;</td><td class="num volt">%.4f</td>'
         '<td class="num up">%+.4f</td></tr>' % (a['O35FINAL'], a['OKRULED'], a['OKRULED'] - a['O35FINAL']))
H.append('</tbody></table>'
         '<div class="defs"><p>All three readings move the same way and by very nearly the same '
         'amount. The levels differ because they are different objects: the built matrix scores every '
         'eligible row using the engine\'s own walk-forward value, while the navigation instrument '
         'scores a teaching subset using an analytic year-1 price. <b>%.4f was predicted for this '
         'setting; %.4f is what the same instrument reads once the fade floor is fixed.</b> The floor '
         'fix costs almost nothing on the class mark.</p>'
         '<p>Worst single class on this board: <b>%.4f</b> (%d), against the ruled 1.139 line &mdash; '
         'inside it.</p></div></div>'
         % (a['OKRULED_predicted_on_the_defective_fade'], a['OKRULED'],
            CK[OKL]['max_class'], CK[OKL]['max_class_year']))
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_K_YEAR1.html'), 'w').write('\n'.join(H))
print('wrote ORDER_K_YEAR1.html  (%d rows)' % len(ys))

# ==================================================================== 3. THE NO-ARB TABLES
def vcls(v):
    return 'sell' if v == 'SELL-RED' else ('buy' if v == 'BUY-RED' else 'ok')


def sortable_head(tid, cols):
    o = ['<table id="%s"><thead><tr>' % tid]
    for i, (nm, num, left) in enumerate(cols):
        o.append('<th class="%s" onclick="sortTable(\'%s\',%d,%s)">%s</th>'
                 % ('l' if left else '', tid, i, 'true' if num else 'false', nm))
    o.append('</tr></thead><tbody>')
    return o


def band_table(lab, tid):
    cols = ([('#', True, False), ('band', False, True), ('n', True, False)]
            + [('yr%d' % n, True, False) for n in range(8)]
            + [('yr0&rarr;1', True, False), ('margin to the 14% rail', True, False),
               ('verdict', False, True)])
    o = sortable_head(tid, cols)
    for i, b in enumerate(BANDS):
        d = ND[lab][b]
        o.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>'
                 '<td class="num k" data-v="%d">%d</td>' % (i + 1, i + 1, b, d['n'], d['n']))
        for v in d['path']:
            o.append('<td class="num" data-v="%s">%s</td>'
                     % (v if v is not None else -1e18, '%.3f' % v if v is not None else '&mdash;'))
        o.append('<td class="num %s" data-v="%.6f">%s</td><td class="num" data-v="%.6f">%s</td>'
                 '<td class="l %s">%s</td></tr>'
                 % (vcls(d['verdict']), d['apprec01'], pc(d['apprec01']),
                    d['buy_margin'], pc(d['buy_margin']), vcls(d['verdict']), d['verdict']))
    o.append('</tbody></table>')
    return '\n'.join(o)


def arm_table(lab, window, tid):
    cols = ([('#', True, False), ('arm', False, True), ('n', True, False)]
            + [('yr%d' % n, True, False) for n in range(8)]
            + [('yr0&rarr;1', True, False), ('margin', True, False), ('verdict', False, True)])
    o = sortable_head(tid, cols)
    _i = 0
    for arm in ARM_ORDER:
        d = ARMS[lab].get('%s|%s' % (window, arm))
        if d is None:
            continue
        _i += 1
        o.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>'
                 '<td class="num k" data-v="%d">%d</td>' % (_i, _i, arm, d['n'], d['n']))
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
    o.append('</tbody></table>')
    return '\n'.join(o)


H = [head('Order K · The No-Arb Tables', 'YEAR PATHS · APPRECIATION · MARGIN · VERDICT')]
H.append(broken_box())
H.append('<div class="defs"><h2>What these tables are asking, in plain words</h2>'
         '<p>Every table asks one question: <b>if you owned this group of players on draft day, and '
         'sold them a year later, would you have made money or lost it?</b></p>'
         '<p><b>yr0</b> is always 1.000 &mdash; it is the group\'s own entry value, the starting '
         'point. <b>yr1</b> is what the same group is worth one year later, as a multiple of that '
         'starting point. <b>yr2</b> through <b>yr7</b> carry the same clock forward.</p>'
         '<p><b>yr0&rarr;1</b> is the first-year appreciation. This is the number the verdict is '
         'about.</p>'
         '<p><b>The 14% rail</b> is the cost of carrying a player for a year &mdash; the roster spot, '
         'the list place, the opportunity. <b>margin</b> is how much room is left before that cost is '
         'beaten.</p>'
         '<p><b>SELL-RED</b> means the group loses value in year one. You could sell on draft day, buy '
         'the same players back a year later, and pocket the difference. That is an arbitrage against '
         'the board and it should not exist.</p>'
         '<p><b>BUY-RED</b> means the group gains more than 14% in year one. You could buy on draft '
         'day, carry them, and still beat the cost. That is the same arbitrage in the other '
         'direction.</p>'
         '<p><b>ok</b> means the group lands between those two lines, which is where a fairly priced '
         'group should land.</p>'
         '<p>The <b>five bands</b> are your bands: picks 1-10, 11-20, 21-30, 31-40, 41-64. The three '
         'above them (ALL 1-64, 1-20, 21-64) are the coarse view.</p>'
         '<p>The <b>pool arms</b> are the non-national-draft entry routes. RD is the rookie draft, MSD '
         'the mid-season draft, SSP supplemental selection, IRE the Irish experiment, UNR unrestricted '
         'free agents, and PDA/PDN/PDS the academy and father-son pathways. Both windows are shown: '
         'the <b>primary</b> window is 2005-2023 (everything the store holds) and the <b>modern</b> '
         'window is 2019-2023 (the recent era only, where the samples are thinner).</p></div>')

H.append('<div class="box"><h2>The current candidate &mdash; ORDER K %s &middot; the owner\'s five '
         'bands plus the coarse three</h2>%s</div>' % (MD['orderk'][:8], band_table(OKL, 'n1')))
H.append('<div class="box"><h2>The move, band by band &middot; ORDER K minus the landing candidate</h2>')
H.append('\n'.join(sortable_head('mv', [('#', True, False), ('band', False, True),
                                        ('landing candidate', True, False), ('candidate 31', True, False),
                                        ('ORDER K', True, False), ('move vs landing', True, False),
                                        ('verdict', False, True)])))
for _bi, b in enumerate(BANDS):
    a0 = ND[LAND][b]['apprec01']; a1 = ND[OKL][b]['apprec01']; a2 = ND[C31L][b]['apprec01']
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>'
             '<td class="num" data-v="%.6f">%s</td><td class="num" data-v="%.6f">%s</td>'
             '<td class="num volt" data-v="%.6f">%s</td>'
             '<td class="num %s" data-v="%.4f">%+.2f</td><td class="l %s">%s &rarr; %s</td></tr>'
             % (_bi + 1, _bi + 1, b, a0, pc(a0), a2, pc(a2), a1, pc(a1),
                'up' if a1 > a0 else 'dn', 100 * (a1 - a0), 100 * (a1 - a0),
                vcls(ND[OKL][b]['verdict']), ND[LAND][b]['verdict'], ND[OKL][b]['verdict']))
H.append('</tbody></table>'
         '<div class="defs"><p><b>Every band improves.</b> Picks 31-40 and 41-64 remain SELL-RED and '
         'that is the known limitation carried in the box at the top of this page &mdash; they are '
         'better, not fixed.</p></div></div>')

H.append('<div class="box"><h2>The comparison columns &middot; the landing candidate 1f176444</h2>%s</div>'
         % band_table(LAND, 'n2'))
H.append('<div class="box"><h2>The comparison columns &middot; candidate 31 fe6be9d6</h2>%s'
         '<div class="defs"><p>Candidate 31 is shown for context only. Note that on candidate 31 '
         'picks 1-10 read +16.19%%, which is a BUY-RED &mdash; over the 14%% rail. That is one of the '
         'reasons it was left behind.</p></div></div>' % band_table(C31L, 'n3'))

H.append('<div class="box"><h2>The pool arms &middot; ORDER K &middot; primary window 2005-2023</h2>%s</div>'
         % arm_table(OKL, 'PRIMARY', 'a1'))
H.append('<div class="box"><h2>The pool arms &middot; ORDER K &middot; modern window 2019-2023</h2>%s'
         '<div class="defs"><p>The modern window carries small samples. Read it as a direction, not a '
         'measurement.</p></div></div>' % arm_table(OKL, 'MODERN', 'a2'))
H.append('<div class="box warn"><h2>The one arm above the buy rail, stated separately so it cannot be '
         'mistaken for a new problem</h2>'
         '<div class="defs"><p><b>Supplemental selection (SSP) reads %s on this board</b>, against '
         '%s on the landing candidate and %s on candidate 31. It was already a buy-red before this '
         'order and it is a buy-red after. SSP players enter at pick 65, outside the 1-64 pick curve, '
         'so no lever in this order reaches them &mdash; but this setting does move the arm '
         '<b>%+.2f points further into the red</b>, and that is stated here rather than buried. '
         'It is an inherited, separately-tracked problem.</p>'
         '<p>Every ND band on this board is under the rail. The highest is picks 11-20 at %s.</p>'
         '</div></div>'
         % (pc(ARMS[OKL]['PRIMARY|SSP']['apprec01']), pc(ARMS[LAND]['PRIMARY|SSP']['apprec01']),
            pc(ARMS[C31L]['PRIMARY|SSP']['apprec01']),
            100 * (ARMS[OKL]['PRIMARY|SSP']['apprec01'] - ARMS[LAND]['PRIMARY|SSP']['apprec01']),
            pc(ND[OKL]['picks 11-20']['apprec01'])))

H.append('<details><summary>Archive &mdash; the earlier boards\' pool-arm tables, kept for the record</summary>')
for lab, nice in ((LAND, 'the landing candidate 1f176444'), (C31L, 'candidate 31 fe6be9d6')):
    for w in ('PRIMARY', 'MODERN'):
        H.append('<div class="box"><h2>%s &middot; %s window</h2>%s</div>'
                 % (nice, w.lower(), arm_table(lab, w, 'z%s%s' % (lab, w))))
H.append('<div class="box"><h2>Vantage-consistency matrix &middot; diagnostic only</h2>'
         '<div class="defs"><p>This asks the same question from a later starting point: if you bought '
         'at year V and held k more years, did you beat the compounded 14% carry? It is a diagnostic. '
         'No decision in this order was made on it.</p></div>')
H.append('<table><thead><tr><th class="l">band</th><th>from year</th><th>k=1</th><th>k=2</th>'
         '<th>k=3</th><th>k=4</th></tr></thead><tbody>')
for b in ['picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']:
    for V in (0, 1, 2):
        g = ST['vantage'][OKL]['%s|V%d' % (b, V)]
        H.append('<tr><td class="l">%s</td><td class="num k">%d</td>%s</tr>'
                 % (b if V == 0 else '', V,
                    ''.join('<td class="num">%s</td>' % ('%+.1f%%' % (100 * x) if x is not None else '&mdash;')
                            for x in g)))
H.append('</tbody></table><div class="defs"><p>the compounded carry for reference: '
         'k=1 +14.0% &middot; k=2 +30.0% &middot; k=3 +48.2% &middot; k=4 +68.9%</p></div></div>')
H.append('</details>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_K_NOARB.html'), 'w').write('\n'.join(H))
print('wrote ORDER_K_NOARB.html')
