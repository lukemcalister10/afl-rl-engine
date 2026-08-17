#!/usr/bin/env python3
"""ORDER I — the two preview pages, in the standing presentation formats (o32_pages.py conventions
carried verbatim: same CSS, same sort script, same column grammar).
  PREVIEW_I_PLAYERS.html : the full board — live · C31 · landing candidate · ORDER I + the three legs.
  PREVIEW_I_YEAR1.html   : the year-1 class in DRAFT ORDER with v0, and the four board columns.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_I_MOVERS.json')))
ROWS = J['rows']; T = J['totals']; MD = J['meta']['boards']
src = open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'o32_pages.py')).read()
CSS = src.split('CSS = """')[1].split('"""')[0]
SORT_JS = src.split('SORT_JS = """')[1].split('"""')[0]


def delta_td(v):
    if v is None: return '<td class="k">&mdash;</td>'
    cls = 'up' if v > 0 else ('dn' if v < 0 else '')
    return '<td class="num %s" data-v="%d">%+d</td>' % (cls, v, v)


def page_head(title, sub, banner):
    return ('<!doctype html>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">%s</div>\n<div class="app">\n'
            '<header><div class="brand">ORDER <b>I</b><span class="sub">%s</span></div>'
            '<div class="spacer"></div>'
            '<div class="stamp">live <b>88ce647f</b> %d &middot; candidate 31 <b>fe6be9d6</b> %d<br>'
            'landing candidate <b>%s</b> %d &middot; <b>ORDER I %s</b> <b>%d</b> &middot; PRE-NUMERAIRE</div></header>\n'
            % (title, CSS, banner, sub, T['live'], T['cand31'], MD['landing'][:8], T['landing'],
               MD['order_i'][:8], T['order_i']))


BANNER = ('NOTHING LANDS WITHOUT THE OWNER\'S WORD — ORDER I WIRES THE THREE MEASURED LEVERS '
          '(S1 &middot; THE COUNTERWEIGHT &middot; THE TALL/SMALL SITTER FACTOR) ONTO 1f176444')
rs = sorted(ROWS, key=lambda r: -r['order_i'])
H = [page_head('Order I · The Board', 'THE COORDINATED BUILD · FULL PLAYER TABLE', BANNER)]
H.append('<div class="box"><h2>All %d priced rows &middot; click any column to sort &middot; deltas vs the '
         'landing candidate, C31 and live</h2>' % len(rs))
H.append('<table id="t1"><thead><tr>')
cols = [('#', True), ('player', False), ('path', False), ('pos', False), ('age', True), ('g', True),
        ('live', True), ('cand 31', True), ('landing', True), ('ORDER I', True),
        ('Δ landing', True), ('Δ c31', True), ('Δ live', True),
        ('leg S1', True), ('leg tall', True), ('leg re-mix', True)]
for i, (nm, num) in enumerate(cols):
    H.append('<th class="%s" onclick="sortTable(\'t1\',%d,%s)">%s</th>'
             % ('l' if nm in ('player', 'path', 'pos') else '', i, 'true' if num else 'false', nm))
H.append('</tr></thead><tbody>')
for i, r in enumerate(rs):
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td><td class="l k">%s</td>'
             '<td class="l k">%s</td><td class="num" data-v="%d">%d</td><td class="num" data-v="%d">%d</td>'
             % (i + 1, i + 1, html.escape(r['name'] or r['key']), r['pathway'] or '?', r['pos'],
                r['age'], r['age'], int(r['g']), int(r['g'])))
    for f in ('live', 'cand31', 'landing'):
        H.append('<td class="num" data-v="%d">%d</td>' % (r[f], r[f]))
    H.append('<td class="num" data-v="%d"><b>%d</b></td>' % (r['order_i'], r['order_i']))
    for f in ('d_vs_landing', 'd_vs_cand31', 'd_vs_live', 'leg_s1', 'leg_tall', 'leg_remix'):
        H.append(delta_td(r[f]))
    H.append('</tr>')
H.append('</tbody></table>')
H.append('<div class="note">Legs are REAL BOARD DELTAS, each its own build: <b>leg S1</b> = the '
         'age-referenced projection bar alone at the chosen dose; <b>leg tall</b> = Order H\'s tall/small '
         'sitter factor alone; <b>leg re-mix</b> = the remainder, i.e. the counterweight plus the '
         'interaction between the first two. The legs do NOT sum to the total by construction and the '
         'residual is shown rather than hidden. %d of %d rows move; <b>%d rows aged 24 or over move — '
         'the cap law</b>. Board totals: live %d &middot; C31 %d &middot; landing %d &middot; ORDER I %d.'
         '</div></div>'
         % (J['n_moved'], len(ROWS), J['n_mature_moved'], T['live'], T['cand31'], T['landing'], T['order_i']))
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'PREVIEW_I_PLAYERS.html'), 'w').write('\n'.join(H))

# ---- year-1 class page -------------------------------------------------------------------------------
Y1 = [r for r in ROWS if (r['yr'] == 2025) or (r['yr'] == 2026 and r['pathway'] == 'MSD')]
PATH_ORDER = {'ND': 0, 'RD': 1, 'PDA': 2, 'PDN': 3, 'PDS': 4, 'IRE': 5, 'UNR': 6, 'SSP': 7, 'MSD': 8}
Y1.sort(key=lambda r: (PATH_ORDER.get(r['pathway'], 9), r['pick'] if r['pick'] is not None else 999, r['key']))
moved = [r for r in Y1 if r['d_vs_landing'] != 0]
up = [r for r in moved if r['d_vs_landing'] > 0]
dn = [r for r in moved if r['d_vs_landing'] < 0]
sit = [r for r in Y1 if int(r['g']) == 0]
tot0 = sum(r['landing'] for r in Y1); tot1 = sum(r['order_i'] for r in Y1)
H = [page_head('Order I · Year-1 Class', 'THE YEAR-1 CLASS · DRAFT ORDER', BANNER)]
H.append('<div class="box"><h2>Read this before the table</h2><div class="note">'
         '%d year-1 rows. <b>%d move</b> &mdash; %d up, %d down. The class total goes %d &rarr; %d '
         '(%+.2f%%). The direction is the whole point of the build: a first-year player who is <b>above '
         'the bar his own age actually clears</b> gains, and one who is <b>below it</b> is charged, '
         'because the counterweight moves weight off his draft pedigree and onto what he has actually '
         'shown. %d rows played no games at all; those can only move through the sitter fade, never '
         'through S1. <b>v0 is untouched</b> &mdash; day-0 prints reproduce 89 of 89 at tolerance zero.'
         '</div></div>'
         % (len(Y1), len(moved), len(up), len(dn), tot0, tot1,
            100.0 * (tot1 - tot0) / max(1, tot0), len(sit)))
H.append('<div class="box"><h2>Year-1 class (2025 entrants + 2026 mid-season) &middot; draft order &middot; %d rows</h2>' % len(Y1))
H.append('<table id="t2"><thead><tr>')
cols = [('order', True), ('player', False), ('path', False), ('pick', True), ('pos', False), ('g', True),
        ('v0', True), ('live', True), ('cand 31', True), ('landing', True), ('ORDER I', True),
        ('Δ landing', True), ('Δ c31', True), ('Δ live', True)]
for i, (nm, num) in enumerate(cols):
    H.append('<th class="%s" onclick="sortTable(\'t2\',%d,%s)">%s</th>'
             % ('l' if nm in ('player', 'path', 'pos') else '', i, 'true' if num else 'false', nm))
H.append('</tr></thead><tbody>')
for i, r in enumerate(Y1):
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td><td class="l k">%s</td>'
             '<td class="num" data-v="%s">%s</td><td class="l k">%s</td><td class="num" data-v="%d">%d</td>'
             % (i + 1, i + 1, html.escape(r['name'] or r['key']), r['pathway'] or '?',
                r['pick'] if r['pick'] is not None else '', r['pick'] if r['pick'] is not None else '—',
                r['pos'], int(r['g']), int(r['g'])))
    H.append('<td class="num k" data-v="%.0f">%.0f</td>' % (r['v0'], r['v0']))
    for f in ('live', 'cand31', 'landing'):
        H.append('<td class="num" data-v="%d">%d</td>' % (r[f], r[f]))
    H.append('<td class="num" data-v="%d"><b>%d</b></td>' % (r['order_i'], r['order_i']))
    for f in ('d_vs_landing', 'd_vs_cand31', 'd_vs_live'):
        H.append(delta_td(r[f]))
    H.append('</tr>')
H.append('</tbody></table>')
H.append('<div class="note">Draft order: ND by pick, then RD, the pathway routes, SSP, MSD. '
         'v0 = the row\'s own day-0 entry object &mdash; untouched by ORDER I.</div></div>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'PREVIEW_I_YEAR1.html'), 'w').write('\n'.join(H))
print('written: PREVIEW_I_PLAYERS.html (%d rows) / PREVIEW_I_YEAR1.html (%d rows, %d moved)'
      % (len(rs), len(Y1), len(moved)))
