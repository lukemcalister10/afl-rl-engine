#!/usr/bin/env python3
"""ORDER P BUILD — THE THREE DOCUMENTS THE OWNER ASKED FOR.

  ORDER_P_PLAYERS.html  the player list — all 804 rows, five board columns, deltas, mechanism legs
  ORDER_P_YEAR1.html    the year-1 class in draft order, the five board columns PLUS v0
  ORDER_P_NOARB.html    the no-arb tables — year paths yr0-7, appreciation, margin, verdict per band,
                        the owner's five bands PLUS ALL / 1-20 / 21-64, in BOTH windows, the pool
                        arms in both windows, both baselines per row, definitions on the page.

House conventions carried verbatim from o32_pages.py / ok_pages.py: same CSS, same click-to-sort
script, same column grammar, rank column, definitions in plain words on the page.

EVERY PAGE CARRIES THE SAME "WHAT IS IN THIS BOARD AND WHAT IS STILL BROKEN" BOX AT THE TOP.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_P_MOVERS.json')))
ROWS = J['rows']; T = J['totals']; MD = J['meta']['boards']; SET = J['meta']['setting']['order_p']
ST = json.load(open(os.path.join(HERE, 'STANDING_TABLES_P.json')))
GP = json.load(open(os.path.join(HERE, 'GATES_P.json')))
CP = json.load(open(os.path.join(HERE, 'CLASS_P.json')))
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
ND = ST['nd']; ARMS = ST['arms']
LAND, OKL, PL = 'O35FINAL', 'OKRULED', 'PBUILT'
BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
         'picks 21-30', 'picks 31-40', 'picks 41-64']
ARM_ORDER = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']
pc = lambda v: '&mdash;' if v is None else '%+.2f%%' % (100 * v)


def esc(s):
    return html.escape(str(s if s is not None else ''))


def head(title, sub):
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">NOTHING LANDS ON THIS SEAT\'S WORD &mdash; ORDER P IS BUILT FOR YOUR '
            'REVIEW AND IS NOT ADOPTED. ONE CELL IS EXPECTED TO BREACH AND IT IS NAMED ON EVERY PAGE.</div>\n'
            '<div class="app">\n'
            '<header><div class="brand">ORDER <b>P</b><span class="sub">%s</span></div>'
            '<div class="spacer"></div>'
            '<div class="stamp">live <b>88ce647f</b> %s &middot; candidate 31 <b>fe6be9d6</b> %s<br>'
            'landing <b>1f176444</b> %s &middot; ORDER K <b>f3101883</b> %s &middot; '
            '<b>ORDER P %s</b> <b>%s</b><br>'
            'the charge: pi &times;= exp(&minus;%.5f &middot; A(g) &middot; T(s_P)) below age 24 '
            '&middot; A(g)=1&minus;e^(&minus;g/%.2f) &middot; PRE-NUMERAIRE</div></header>\n'
            % (esc(title), CSS, esc(sub), '{:,}'.format(T['live']), '{:,}'.format(T['cand31']),
               '{:,}'.format(T['landing']), '{:,}'.format(T['orderk']), MD['orderp'][:8],
               '{:,}'.format(T['orderp']), SET['LAMBDA'], SET['G0']))


def broken_box():
    p1p = ND[PL]['picks 1-10']['apprec01']; k1p = ND[OKL]['picks 1-10']['apprec01']
    b3140 = ND[PL]['picks 31-40']['apprec01']; b4164 = ND[PL]['picks 41-64']['apprec01']
    k3140 = ND[OKL]['picks 31-40']['apprec01']; k4164 = ND[OKL]['picks 41-64']['apprec01']
    ssp = ARMS[PL]['PRIMARY|SSP']['apprec01']; sspK = ARMS[OKL]['PRIMARY|SSP']['apprec01']
    modP = ST['nd_modern'][PL]['picks 1-10']['apprec01']
    modK = ST['nd_modern'][OKL]['picks 1-10']['apprec01']
    w2 = CP['PBUILT']['w2']; w2k = CP['OKRULED']['w2']
    return ('<div class="brk"><h2>What is in this board, and what is still broken</h2>'
            '<p>Read this before you read a single price. It is the same box on all three pages, and '
            'it is written in plain words on purpose.</p>'

            '<h3>The one thing this board changes</h3>'
            '<p>Order K charged a young player\'s draft pedigree down as he played games, and the '
            'charge <b>read nothing except how many games he had played</b>. It peaked at exactly 14 '
            'games and then fell away again, so a player with 36 games kept MORE of his unearned '
            'entry price than a player with 17 games &mdash; however well or badly either of them had '
            'actually played. Two real players, Zeke Uwland and Cooper Harvey, both had 17 games and '
            'both sat about 1.7 points a game below what is normal for their age, and Order K charged '
            'them the identical 49.0%%, to the last decimal.</p>'
            '<p><b>On this board the charge reads performance, and it reads it against the bar the '
            'player\'s own entry price implies.</b> Uwland was pick 2 and cost 2,583; a player at that '
            'price normally produces 19.2 points a game clear of his age bar, so against what is '
            'priced into him he is 20.9 short. Harvey was pick 56 and cost 265; a player at that price '
            'normally produces 1.3 points a game BELOW the age bar, so he is half a point short. Same '
            'production for their age, same games, opposite verdicts &mdash; because they were priced '
            'differently to begin with. That is your own sentence, on two real rows.</p>'
            '<p>The bar a young player is measured against is now his age bar plus a <b>measured</b> '
            'pedigree premium: how far above the age bar a player who entered at his price actually '
            'produces, estimated on 5,041 real seasons over 1,575 players. Nothing in it was chosen. '
            'The level of the charge was SOLVED so it removes exactly the same total number of points '
            'from the year-1 class as the old charge did, and the steepness follows from the '
            'measurement. There is no free parameter and no player\'s value was targeted.</p>'

            '<h3>What is unchanged from Order K</h3><ul>'
            '<li>The age-referenced projection bar at dose 0.40, the counterweight at kappa 0.20 / '
            'gamma_u 8, the selection relief at 1.08.</li>'
            '<li>Your tall/small sitter factor, with the Order K fade-floor fix.</li>'
            '<li>The measured pick-curve fade.</li>'
            '<li><b>Entry values.</b> A player who has never played cannot move on this board at all: '
            'the charge is exactly zero at zero games, by construction. All 89 wired entrants print '
            'bit-identical day-0 prices, and the emit\'s own replication proof was run against Order '
            'K\'s own reference file rather than a regenerated one, so that is a test and not a claim.</li>'
            '<li>Turn the new dial off and this engine rebuilds Order K\'s board <b>f3101883</b> byte '
            'for byte.</li></ul>'

            '<h3>What is still broken &mdash; open defects, none of them fixed here</h3><ul>'
            '<li><b>MODERN picks 1-10 is over your buy rail at %s.</b> On the recent-era window only '
            '(2019-2023, fifty rows) the top ten picks appreciate more than 14%% in their first year. '
            'Order K reads %s there, so that cell had about a third of a point of room before this '
            'order touched anything. <b>This was predicted before the build and it is the branch you '
            'already agreed to rule on.</b> No cap has been bolted on to hide it and no constant was '
            'moved to chase it. In the full-history window the same band reads %s against Order K\'s '
            '%s, which is inside the rail.</li>'
            '<li><b>Late picks still lose money in year one.</b> Picks 31-40 read <b>%s</b> and picks '
            '41-64 read <b>%s</b>. Both are better than Order K (%s and %s), and both are still '
            'negative: a player drafted there is still worth less a year later.</li>'
            '<li><b>Supplemental selection (SSP) still appreciates about half again in year one.</b> '
            '%s on this board against %s on Order K. SSP players enter outside the 1-64 pick curve, '
            'their entry prices are low, so their pedigree bar is low and they clear it easily &mdash; '
            'which means this order pushes the arm FURTHER into the red. <b>It was already over the '
            'rail before this order and it is reported on its own line, never folded into a pass.</b></li>'
            '<li><b>The peaks are not restored.</b> A charge that grows with evidence cannot fall back '
            'in the years where the peaks sit. Growing with evidence is exactly the defect you asked '
            'to have removed, so the two cannot both be had from this shape. The trade is priced on '
            'the no-arb page, not hidden.</li>'
            '<li><b>The pedigree premium is measured on players who play.</b> A cheap player has to be '
            'good to get a game; an expensive one plays anyway. So the measured premium is a lower '
            'bound on the real gap, and the bar is if anything LESS demanding of expensive players '
            'than the truth. Not repaired here.</li>'
            '<li><b>The premium is thin at both ends for talls</b> (effective sample 19 at the cheap '
            'end, 47 at the dear end). Outside the fitted range it is held flat, never extrapolated.</li>'
            '<li><b>Veteran key-position talls aged 28-30 are over-priced by roughly 30%%</b>, because '
            'the veteran board is parked. Nothing in this order touches them.</li>'
            '<li><b>The engine leans too hard on the most recent season.</b> A player who broke out '
            'once is probably too expensive here &mdash; <b>Xerri, Callaghan, Ash, Thilthorpe</b>. A '
            'good player who had one bad year is probably too cheap &mdash; <b>Coniglio, De Goey, '
            'Langford</b>.</li>'
            '<li><b>The ceiling column on the dial page is wrong for anyone 22 or older.</b> It prints '
            'roughly the 87th percentile where it should print the 97th.</li></ul>'

            '<h3>The year-1 class</h3>'
            '<p>Your growth rule is written on draft classes 2005 to 2015. On that basis this board '
            'reads <b>%.4f</b> against Order K\'s <b>%.4f</b>: the class grows more, it clears your '
            '1.03 floor, and it stays under the 1.14 buy rail. That basis is <b>draft</b> classes '
            '2005-2015, which on the cohort clock is cohort years 2006-2016 &mdash; not the same '
            'window as the cohort-clock number printed beside it, and the two are shown together on '
            'the year-1 page so they cannot be confused.</p>'
            '</div>'
            % (pc(modP), pc(modK), pc(p1p), pc(k1p), pc(b3140), pc(b4164), pc(k3140), pc(k4164),
               pc(ssp), pc(sspK), w2, w2k))


def num_td(v, cls=''):
    return '<td class="num %s" data-v="%s">%s</td>' % (cls, v, '{:,}'.format(int(v)))


def delta_td(v):
    if v is None:
        return '<td class="k">&mdash;</td>'
    c = 'up' if v > 0 else ('dn' if v < 0 else '')
    return '<td class="num %s" data-v="%d">%+d</td>' % (c, v, v)


def f_td(v, d=2, suffix=''):
    if v is None:
        return '<td class="num k" data-v="-1e18">&mdash;</td>'
    return '<td class="num" data-v="%.6f">%s%s</td>' % (v, ('%.' + str(d) + 'f') % v, suffix)


# ==================================================================== 1. THE PLAYER LIST
cols = [('#', True), ('player', False), ('pathway', False), ('pos', False), ('age', True),
        ('pick', True), ('games', True),
        ('live 88ce647f', True), ('cand 31 fe6be9d6', True), ('landing 1f176444', True),
        ('ORDER K f3101883', True), ('ORDER P', True),
        ('&Delta; vs ORDER K', True), ('&Delta; vs landing', True), ('&Delta; vs live', True),
        ('v0 entry price', True), ('pedigree premium', True), ('surplus vs AGE bar', True),
        ('surplus vs PEDIGREE bar', True), ('charge ORDER K', True), ('charge ORDER P', True),
        ('leg tall', True), ('leg age-bar', True), ('leg counterweight', True),
        ('leg floor fix', True), ('ORDER K interaction', True)]
H = [head('Order P · The Player List', 'ALL 804 PRICED ROWS · FIVE BOARDS · THE MECHANISM')]
H.append(broken_box())
H.append('<div class="defs"><h2>What each column means</h2>'
         '<p><b>live 88ce647f</b> &mdash; the price on the board your league is using today.</p>'
         '<p><b>cand 31 fe6be9d6</b> and <b>landing 1f176444</b> &mdash; the two earlier boards, kept '
         'so you can see how far a row has travelled.</p>'
         '<p><b>ORDER K f3101883</b> &mdash; the board this one is built on. It carries the blind '
         'charge. Every gate in this order is scored against it.</p>'
         '<p><b>ORDER P</b> &mdash; this build.</p>'
         '<p><b>v0 entry price</b> &mdash; what the engine said the pick itself was worth on draft '
         'day, before the player had done anything. It does not move in this order. It is also the '
         'axis the pedigree premium is read on.</p>'
         '<p><b>pedigree premium</b> &mdash; how many points a game above his AGE bar a player who '
         'entered at that price actually produces, measured on 5,041 real seasons. It is the amount '
         'by which this order raises his bar.</p>'
         '<p><b>surplus vs AGE bar</b> &mdash; his own games-weighted production minus what is normal '
         'for his age in his position. This is what Order K\'s world would have measured. Order K\'s '
         'charge did not read it.</p>'
         '<p><b>surplus vs PEDIGREE bar</b> &mdash; the same thing measured against his age bar PLUS '
         'his premium. <b>This is the number the new charge reads.</b> It is the first column minus '
         'the second.</p>'
         '<p><b>charge ORDER K</b> / <b>charge ORDER P</b> &mdash; the share of his draft pedigree the '
         'board takes off him. Order K\'s reads games only. Order P\'s reads games and performance '
         'against his own bar. A player at or above his pedigree bar pays nothing at all.</p>'
         '<p><b>leg tall / leg age-bar / leg counterweight / leg floor fix / interaction</b> &mdash; '
         'Order K\'s own legs, carried unchanged from that order\'s ledger so the whole stack is in '
         'one row. They explain how the row got from the landing candidate to Order K. The move from '
         'Order K to Order P is the &Delta; column.</p>'
         '<p>Rows aged 24 and over are outside the age gate and keep the old charge exactly. Rows with '
         'zero career games cannot move at all.</p>'
         '<p>Every column header sorts. Click once for one direction, again for the other.</p></div>')
rs = sorted(ROWS, key=lambda r: -r['orderp'])
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
    for f in ('live', 'cand31', 'landing', 'orderk', 'orderp'):
        H.append(num_td(r[f], 'volt' if f == 'orderp' else ''))
    for f in ('leg_p', 'd_vs_landing', 'd_vs_live'):
        H.append(delta_td(r[f]))
    H.append(f_td(r['m_v0'], 0))
    H.append(f_td(r['m_premium'], 2))
    H.append(f_td(r['m_sN'], 2))
    H.append(f_td(r['m_sP'], 2))
    H.append(f_td(None if r['m_charge_k'] is None else 100 * r['m_charge_k'], 1, '%'))
    H.append(f_td(None if r['m_charge_p'] is None else 100 * r['m_charge_p'], 1, '%'))
    for f in ('leg_tall', 'leg_s1', 'leg_cw', 'leg_floor', 'residual'):
        H.append(delta_td(r[f]))
    H.append('</tr>')
H.append('</tbody></table></div>')
H.append('<div class="box"><h2>Board totals</h2><table><thead><tr><th class="l">board</th>'
         '<th>total board points</th><th>vs ORDER K</th></tr></thead><tbody>')
for nm, f in (('live 88ce647f', 'live'), ('candidate 31 fe6be9d6', 'cand31'),
              ('landing candidate 1f176444', 'landing'), ('ORDER K f3101883', 'orderk'),
              ('ORDER P %s' % MD['orderp'][:8], 'orderp')):
    H.append('<tr><td class="l">%s</td><td class="num">%s</td><td class="num">%+d</td></tr>'
             % (nm, '{:,}'.format(T[f]), T[f] - T['orderk']))
H.append('</tbody></table>'
         '<div class="defs"><p><b>%d of %d rows move against Order K</b> &mdash; %d up and %d down. '
         'The board comes down %+.2f%%. Rows aged 24 and over move %+d points between them, which is '
         'the age gate holding.</p></div></div>'
         % (GP['n_move'], len(rs), GP['n_up'], GP['n_down'],
            100 * (T['orderp'] - T['orderk']) / T['orderk'],
            sum(r['leg_p'] for r in ROWS if r['age'] >= 24)))
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_P_PLAYERS.html'), 'w').write('\n'.join(H))
print('wrote ORDER_P_PLAYERS.html  (%d rows)' % len(rs))

# ==================================================================== 2. THE YEAR-1 CLASS
PATH_ORDER = {'ND': 0, 'RD': 1, 'PDA': 2, 'PDN': 3, 'PDS': 4, 'IRE': 5, 'UNR': 6, 'SSP': 7, 'MSD': 8}


def y1key(r):
    return (PATH_ORDER.get(r['pathway'], 9), r['pick'] if r['pick'] else 999, -r['orderp'])


ys = sorted(Y1, key=y1key)
H = [head('Order P · The Year-1 Class', 'THE 2025 INTAKE IN DRAFT ORDER · WITH v0')]
H.append(broken_box())
H.append('<div class="defs"><h2>How to read this page</h2>'
         '<p>These are the players who entered the league in the most recent intake &mdash; the class '
         'whose first-year appreciation your growth rule is written about. They are listed in draft '
         'order: national draft by pick number first, then the rookie draft, then the academy and '
         'father-son pathways, then supplemental selection, then the mid-season draft.</p>'
         '<p><b>v0</b> is the entry value &mdash; what the engine says the pick itself was worth on '
         'draft day, before the player had done anything. <b>Entry values do not move in this order '
         'and cannot.</b> The charge is exactly zero at zero games, so a player who has not played is '
         'bit-identical to Order K.</p>'
         '<p><b>v0 is also the axis the pedigree premium is read on.</b> Two players of the same age '
         'and position with different entry prices now face different bars, and the size of the '
         'difference is the <b>pedigree premium</b> column.</p></div>')
H.append('<div class="box"><h2>%d rows in the year-1 class &middot; %s &rarr; %s board points '
         '(%+.2f%%) &middot; %d up, %d down</h2>'
         '<div class="defs"><p><b>This class\'s prices on today\'s board and the historical class '
         'growth rate are two different questions, and they can move in different directions.</b> The '
         'growth rule asks: across the intake classes of 2005 to 2015, how much did a class appreciate '
         'between draft day and a year later? That number goes UP on this board. This table is the '
         'CURRENT class priced today. The 2025 intake is mostly high picks with very few games behind '
         'them, and a high pick with few games is exactly who this charge is hardest on &mdash; because '
         'his price says a great deal is expected of him and he has not yet shown it. Both are true '
         'and both are printed.</p></div>'
         % (len(ys), '{:,}'.format(sum(r['orderk'] for r in ys)),
            '{:,}'.format(sum(r['orderp'] for r in ys)),
            100 * (sum(r['orderp'] for r in ys) - sum(r['orderk'] for r in ys))
            / max(1, sum(r['orderk'] for r in ys)),
            sum(1 for r in ys if r['leg_p'] > 0), sum(1 for r in ys if r['leg_p'] < 0)))
c2 = [('#', True), ('player', False), ('pathway', False), ('pick', True), ('pos', False),
      ('age', True), ('games', True), ('v0 (entry value)', True), ('pedigree premium', True),
      ('surplus vs AGE bar', True), ('surplus vs PEDIGREE bar', True),
      ('charge ORDER K', True), ('charge ORDER P', True),
      ('live 88ce647f', True), ('cand 31 fe6be9d6', True), ('landing 1f176444', True),
      ('ORDER K f3101883', True), ('ORDER P', True), ('&Delta; vs ORDER K', True),
      ('&Delta; vs landing', True)]
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
    H.append(f_td(r['m_premium'], 2))
    H.append(f_td(r['m_sN'], 2))
    H.append(f_td(r['m_sP'], 2))
    H.append(f_td(None if r['m_charge_k'] is None else 100 * r['m_charge_k'], 1, '%'))
    H.append(f_td(None if r['m_charge_p'] is None else 100 * r['m_charge_p'], 1, '%'))
    for f in ('live', 'cand31', 'landing', 'orderk', 'orderp'):
        H.append(num_td(r[f], 'volt' if f == 'orderp' else ''))
    for f in ('leg_p', 'd_vs_landing'):
        H.append(delta_td(r[f]))
    H.append('</tr>')
H.append('</tbody></table></div>')
H.append('<div class="box"><h2>The class growth rule &middot; how a whole intake prices a year on</h2>'
         '<div class="defs"><p>Your rule: the year-1 class cohort must GROW, must clear a floor of '
         '1.03, and must stay strictly under the 1.14 buy rail. <b>The rule is written on DRAFT '
         'classes 2005 to 2015.</b> On the cohort clock those are cohort years 2006 to 2016, because a '
         'draft class is priced in the year after it is drafted. The second row below is the same '
         'object on a DIFFERENT window &mdash; cohort years 2005 to 2015, i.e. draft classes 2004 to '
         '2014. It is printed only so the two cannot be mistaken for each other.</p></div>'
         '<table><thead><tr><th class="l">reading</th><th>landing candidate</th><th>ORDER K</th>'
         '<th>ORDER P</th><th>move vs ORDER K</th><th>floor 1.03</th><th>rail 1.14</th>'
         '</tr></thead><tbody>')
for nm, key in (('THE REGISTERED BASIS &mdash; draft classes 2005-2015', 'w2'),
                ('the cohort clock &mdash; draft classes 2004-2014 (NOT the rail)', 'cohort')):
    a = CP[LAND][key]; b = CP[OKL][key]; c = CP[PL][key]
    H.append('<tr><td class="l">%s</td><td class="num">%.4f</td><td class="num">%.4f</td>'
             '<td class="num volt">%.4f</td><td class="num %s">%+.4f</td>'
             '<td class="num %s">%+.4f</td><td class="num %s">%+.4f</td></tr>'
             % (nm, a, b, c, 'up' if c > b else 'dn', c - b,
                'up' if c >= 1.03 else 'dn', c - 1.03, 'up' if c < 1.14 else 'dn', c - 1.14))
H.append('</tbody></table>'
         '<div class="defs"><p>Worst single class on this board: <b>%.4f</b> (cohort %d), against the '
         'ruled 1.139 line.</p></div></div>'
         % (CP[PL]['max_class'], CP[PL]['max_class_year']))
H.append('<div class="box"><h2>Every class, ORDER K against ORDER P</h2>'
         '<table id="t3"><thead><tr><th class="l">cohort year</th><th class="l">draft class</th>'
         '<th>ORDER K</th><th>ORDER P</th><th>move</th></tr></thead><tbody>')
for y in sorted(int(k) for k in CP[PL]['per_class'] if CP[PL]['per_class'][k] is not None):
    a = CP[OKL]['per_class'][str(y)]; b = CP[PL]['per_class'][str(y)]
    if a is None or b is None:
        continue
    H.append('<tr><td class="l">%d</td><td class="l k">%d</td><td class="num">%.4f</td>'
             '<td class="num volt">%.4f</td><td class="num %s">%+.4f</td></tr>'
             % (y, y - 1, a, b, 'up' if b > a else 'dn', b - a))
H.append('</tbody></table></div>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_P_YEAR1.html'), 'w').write('\n'.join(H))
print('wrote ORDER_P_YEAR1.html  (%d rows)' % len(ys))

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


def band_table(lab, tid, window='PRIMARY'):
    D = ND if window == 'PRIMARY' else ST['nd_modern']
    cols = ([('#', True, False), ('band', False, True), ('n', True, False)]
            + [('yr%d' % n, True, False) for n in range(8)]
            + [('yr0&rarr;1', True, False), ('margin to the 14% rail', True, False),
               ('verdict', False, True), ('ORDER K', True, False), ('landing', True, False)])
    o = sortable_head(tid, cols)
    for i, b in enumerate(BANDS):
        d = D[lab][b]
        o.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>'
                 '<td class="num k" data-v="%d">%d</td>' % (i + 1, i + 1, b, d['n'], d['n']))
        for v in d['path']:
            o.append('<td class="num" data-v="%s">%s</td>'
                     % (v if v is not None else -1e18, '%.3f' % v if v is not None else '&mdash;'))
        o.append('<td class="num %s" data-v="%.6f">%s</td><td class="num" data-v="%.6f">%s</td>'
                 '<td class="l %s">%s</td>'
                 % (vcls(d['verdict']), d['apprec01'], pc(d['apprec01']),
                    d['buy_margin'], pc(d['buy_margin']), vcls(d['verdict']), d['verdict']))
        for base in (OKL, LAND):
            e = D[base][b]
            o.append('<td class="num k" data-v="%.6f">%s</td>' % (e['apprec01'], pc(e['apprec01'])))
        o.append('</tr>')
    o.append('</tbody></table>')
    return '\n'.join(o)


def arm_table(lab, window, tid):
    cols = ([('#', True, False), ('arm', False, True), ('n', True, False)]
            + [('yr%d' % n, True, False) for n in range(8)]
            + [('yr0&rarr;1', True, False), ('margin', True, False), ('verdict', False, True),
               ('ORDER K', True, False), ('landing', True, False)])
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
                     '<td class="l k" style="font-size:11px">%s</td>' % esc(d['verdict']))
        else:
            o.append('<td class="num %s" data-v="%.6f">%s</td><td class="num" data-v="%.6f">%s</td>'
                     '<td class="l %s">%s</td>'
                     % (vcls(d['verdict']), d['apprec01'], pc(d['apprec01']),
                        d['buy_margin'], pc(d['buy_margin']), vcls(d['verdict']), d['verdict']))
        for base in (OKL, LAND):
            e = ARMS[base].get('%s|%s' % (window, arm))
            v = None if (e is None) else e['apprec01']
            o.append('<td class="num k" data-v="%s">%s</td>'
                     % (v if v is not None else -1e18, pc(v)))
        o.append('</tr>')
    o.append('</tbody></table>')
    return '\n'.join(o)


H = [head('Order P · The No-Arb Tables', 'YEAR PATHS · APPRECIATION · MARGIN · VERDICT · BOTH WINDOWS')]
H.append(broken_box())
H.append('<div class="defs"><h2>What these tables are asking, in plain words</h2>'
         '<p>Every table asks one question: <b>if you owned this group of players on draft day, and '
         'sold them a year later, would you have made money or lost it?</b></p>'
         '<p><b>yr0</b> is always 1.000 &mdash; it is the group\'s own entry value, the starting '
         'point. <b>yr1</b> is what the same group is worth one year later, as a multiple of that '
         'starting point. <b>yr2</b> through <b>yr7</b> carry the same clock forward.</p>'
         '<p><b>yr0&rarr;1</b> is the first-year appreciation. This is the number the verdict is '
         'about. <b>The 14% rail</b> is the cost of carrying a player for a year. <b>margin</b> is '
         'how much room is left before that cost is beaten.</p>'
         '<p><b>SELL-RED</b> means the group loses value in year one: you could sell on draft day, buy '
         'the same players back a year later, and pocket the difference. <b>BUY-RED</b> means the '
         'group gains more than 14% in year one: you could buy on draft day, carry them, and still '
         'beat the cost. Both are arbitrages against the board. <b>ok</b> is between the two lines.</p>'
         '<p>The <b>five bands</b> are your bands: picks 1-10, 11-20, 21-30, 31-40, 41-64. The three '
         'above them (ALL 1-64, 1-20, 21-64) are the coarse view. <b>Both windows are shown for every '
         'band and every arm</b>: the <b>primary</b> window is 2005-2023 (everything the store holds) '
         'and the <b>modern</b> window is 2019-2023 (the recent era only, where the samples are '
         'thinner &mdash; picks 1-10 there is fifty rows).</p>'
         '<p>The last two columns of every table are the two baselines: <b>ORDER K</b>, the board this '
         'one is built on, and <b>landing</b>, the landing candidate underneath it.</p></div>')

H.append('<div class="box"><h2>ORDER P %s &middot; the owner\'s five bands plus the coarse three '
         '&middot; PRIMARY window 2005-2023</h2>%s</div>' % (MD['orderp'][:8], band_table(PL, 'n1')))
H.append('<div class="box warn"><h2>ORDER P &middot; the same bands &middot; MODERN window 2019-2023 '
         '&middot; THIS IS WHERE THE ONE EXPECTED BREACH IS</h2>%s'
         '<div class="defs"><p>Picks 1-10 in this window is the cell that goes over your rail. It '
         'carries <b>%d rows</b>. It was predicted to breach before this board was built, and it is '
         'the branch you already said you would rule on. No cap was added and no constant was '
         'moved.</p></div></div>'
         % (band_table(PL, 'n1m', 'MODERN'), ST['nd_modern'][PL]['picks 1-10']['n']))
H.append('<div class="box"><h2>The move, band by band, in BOTH windows &middot; ORDER P minus ORDER K</h2>')
H.append('\n'.join(sortable_head('mv', [('#', True, False), ('band', False, True),
                                        ('PRI landing', True, False), ('PRI ORDER K', True, False),
                                        ('PRI ORDER P', True, False), ('PRI move', True, False),
                                        ('MOD landing', True, False), ('MOD ORDER K', True, False),
                                        ('MOD ORDER P', True, False), ('MOD move', True, False),
                                        ('verdict PRI', False, True), ('verdict MOD', False, True)])))
for _bi, b in enumerate(BANDS):
    row = ['<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td>' % (_bi + 1, _bi + 1, b)]
    for D in (ND, ST['nd_modern']):
        a0 = D[LAND][b]['apprec01']; ak = D[OKL][b]['apprec01']; ap = D[PL][b]['apprec01']
        row.append('<td class="num k" data-v="%.6f">%s</td><td class="num" data-v="%.6f">%s</td>'
                   '<td class="num volt" data-v="%.6f">%s</td>'
                   '<td class="num %s" data-v="%.4f">%+.2f</td>'
                   % (a0, pc(a0), ak, pc(ak), ap, pc(ap),
                      'up' if ap > ak else 'dn', 100 * (ap - ak), 100 * (ap - ak)))
    row.append('<td class="l %s">%s &rarr; %s</td><td class="l %s">%s &rarr; %s</td></tr>'
               % (vcls(ND[PL][b]['verdict']), ND[OKL][b]['verdict'], ND[PL][b]['verdict'],
                  vcls(ST['nd_modern'][PL][b]['verdict']), ST['nd_modern'][OKL][b]['verdict'],
                  ST['nd_modern'][PL][b]['verdict']))
    H.append(''.join(row))
H.append('</tbody></table></div>')

H.append('<div class="box"><h2>The pool arms &middot; ORDER P &middot; PRIMARY window 2005-2023</h2>%s</div>'
         % arm_table(PL, 'PRIMARY', 'a1'))
H.append('<div class="box"><h2>The pool arms &middot; ORDER P &middot; MODERN window 2019-2023</h2>%s'
         '<div class="defs"><p>The modern window carries small samples. Read it as a direction, not a '
         'measurement.</p></div></div>' % arm_table(PL, 'MODERN', 'a2'))
H.append('<div class="box warn"><h2>The arms above the buy rail, stated separately so they cannot be '
         'mistaken for a pass</h2>'
         '<div class="defs"><p><b>Supplemental selection (SSP) reads %s on this board</b>, against '
         '%s on Order K and %s on the landing candidate. <b>It was already over the rail before this '
         'order existed.</b> SSP players enter at pick 65, outside the 1-64 pick curve; their entry '
         'prices are low, so the bar this order sets for them is low and they clear it easily. That '
         'means this order pushes the arm <b>%+.2f points further into the red</b>, and that is stated '
         'here rather than buried. It is an inherited, separately-tracked problem and nothing in this '
         'order reaches it.</p></div></div>'
         % (pc(ARMS[PL]['PRIMARY|SSP']['apprec01']), pc(ARMS[OKL]['PRIMARY|SSP']['apprec01']),
            pc(ARMS[LAND]['PRIMARY|SSP']['apprec01']),
            100 * (ARMS[PL]['PRIMARY|SSP']['apprec01'] - ARMS[OKL]['PRIMARY|SSP']['apprec01'])))

H.append('<details><summary>The comparison boards, in full, both windows</summary>')
for lab, nice in ((OKL, 'ORDER K f3101883'), (LAND, 'the landing candidate 1f176444')):
    for w, wn in (('PRIMARY', 'primary 2005-2023'), ('MODERN', 'modern 2019-2023')):
        H.append('<div class="box"><h2>%s &middot; ND bands &middot; %s</h2>%s</div>'
                 % (nice, wn, band_table(lab, 'z%s%s' % (lab, w), w)))
        H.append('<div class="box"><h2>%s &middot; pool arms &middot; %s</h2>%s</div>'
                 % (nice, wn, arm_table(lab, w, 'y%s%s' % (lab, w))))
H.append('<div class="box"><h2>Vantage-consistency matrix &middot; diagnostic only</h2>'
         '<div class="defs"><p>This asks the same question from a later starting point: if you bought '
         'at year V and held k more years, did you beat the compounded 14% carry? It is a thermometer. '
         'No decision in this order was made on it and nothing was calibrated toward it.</p></div>')
H.append('<table><thead><tr><th class="l">band</th><th>from year</th><th>k=1</th><th>k=2</th>'
         '<th>k=3</th><th>k=4</th></tr></thead><tbody>')
for b in ['picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']:
    for V in (0, 1, 2):
        g = ST['vantage'][PL]['%s|V%d' % (b, V)]
        H.append('<tr><td class="l">%s</td><td class="num k">%d</td>%s</tr>'
                 % (b if V == 0 else '', V,
                    ''.join('<td class="num">%s</td>' % ('%+.1f%%' % (100 * x) if x is not None else '&mdash;')
                            for x in g)))
H.append('</tbody></table><div class="defs"><p>the compounded carry for reference: '
         'k=1 +14.0% &middot; k=2 +30.0% &middot; k=3 +48.2% &middot; k=4 +68.9%</p></div></div>')
H.append('</details>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'ORDER_P_NOARB.html'), 'w').write('\n'.join(H))
print('wrote ORDER_P_NOARB.html')
