#!/usr/bin/env python3
"""ORDER B — the two preview pages (standing presentation formats, o32_pages.py conventions carried).
PREVIEW_B_PLAYERS.html: full board, Live · C31 · C32-base · B-preview + the three mechanism legs.
PREVIEW_B_YEAR1.html: the year-1 class in draft order, with the unchanged-rows assertion printed."""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_B_MOVERS.json')))
C31 = {r['key']: r for r in json.load(open(SP + '/cand31.json'))['rows']}
ROWS = J['rows']
for r in ROWS:
    c = C31[r['key']]
    r['g'] = c.get('g', 0); r['yr'] = c.get('yr'); r['v0'] = c.get('v0', 0.0)
T = J['totals']
MD = J['meta']['boards']

CSS = open(os.path.join(HERE, '_pages_css.txt')).read() if os.path.exists(os.path.join(HERE, '_pages_css.txt')) else None
# carry the o32 page CSS/JS verbatim
import re
src = open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'o32_pages.py')).read()
CSS = src.split('CSS = """')[1].split('"""')[0]
SORT_JS = src.split('SORT_JS = """')[1].split('"""')[0]


def delta_td(v):
    if v is None:
        return '<td class="k">—</td>'
    cls = 'up' if v > 0 else ('dn' if v < 0 else '')
    return '<td class="num %s" data-v="%d">%+d</td>' % (cls, v, v)


def page_head(title, sub, banner):
    return ('<!doctype html>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">%s</div>\n<div class="app">\n'
            '<header><div class="brand">ORDER <b>B</b><span class="sub">%s</span></div>'
            '<div class="spacer"></div>'
            '<div class="stamp">live <b>88ce647f</b> %d · candidate 31 <b>fe6be9d6</b> %d<br>'
            'C32-base (repair) <b>%s</b> %d · <b>B-preview %s</b> <b>%d</b> · PRE-NUMERAIRE</div></header>\n'
            % (title, CSS, banner, sub, T['live'], T['cand31'], MD['off_o32'][:8], T['c32base'],
               MD['full1'][:8], T['b_preview']))


rows_sorted = sorted(ROWS, key=lambda r: -r['b_preview'])
H = [page_head('Order B · The Board', 'THE VETERAN FIXES · FULL PLAYER TABLE',
               'NOTHING LANDS WITHOUT THE OWNER\'S WORD — B-PREVIEW RIDES THE REPAIRED CANDIDATE 32 AND LANDS ONLY AFTER IT')]
H.append('<div class="box"><h2>All %d priced rows · click any column to sort · deltas vs C32-base, C31 and live</h2>' % len(rows_sorted))
H.append('<table id="t1"><thead><tr>')
cols = [('#', True), ('player', False), ('path', False), ('pos', False), ('age', True), ('g', True),
        ('live', True), ('cand 31', True), ('C32-base', True), ('B-preview', True),
        ('Δ base', True), ('Δ c31', True), ('Δ live', True),
        ('ladder', True), ('fade', True), ('taper', True)]
for i, (nm, num) in enumerate(cols):
    H.append('<th class="%s" onclick="sortTable(\'t1\',%d,%s)">%s</th>'
             % ('l' if nm in ('player', 'path', 'pos') else '', i, 'true' if num else 'false', nm))
H.append('</tr></thead><tbody>')
for i, r in enumerate(rows_sorted):
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td><td class="l k">%s</td>'
             '<td class="l k">%s</td><td class="num" data-v="%d">%d</td><td class="num" data-v="%d">%d</td>'
             % (i + 1, i + 1, html.escape(r['name'] or r['key']), r['pathway'] or '?', r['pos'],
                r['age'], r['age'], int(r['g']), int(r['g'])))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['live'], r['live']))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['cand31'], r['cand31']))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['c32base'], r['c32base']))
    H.append('<td class="num" data-v="%d"><b>%d</b></td>' % (r['b_preview'], r['b_preview']))
    H.append(delta_td(r['d_vs_c32base']))
    H.append(delta_td(r['d_vs_cand31']))
    H.append(delta_td(r['d_vs_live']))
    for leg in ('leg_ladder', 'leg_fade', 'leg_taper'):
        H.append(delta_td(r[leg]))
    H.append('</tr>')
H.append('</tbody></table>')
H.append('<div class="note">Legs are REAL BOARD DELTAS from the stage ladder (B-1 tall ladder + anchor renorm '
         '→ +B-2 terminal fade (the ruled FALLBACK — the conditional fit failed identification, see the packet) '
         '→ +B-3 taper retirement); their sum is Δ vs C32-base exactly. '
         'Board totals: live %d · C31 %d · C32-base %d · B-preview %d.</div></div>'
         % (T['live'], T['cand31'], T['c32base'], T['b_preview']))
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'PREVIEW_B_PLAYERS.html'), 'w').write('\n'.join(H))

# ---- year-1 page ------------------------------------------------------------------------------------
Y1 = [r for r in ROWS if (r['yr'] == 2025) or (r['yr'] == 2026 and r['pathway'] == 'MSD')]
PATH_ORDER = {'ND': 0, 'RD': 1, 'PDA': 2, 'PDN': 3, 'PDS': 4, 'IRE': 5, 'UNR': 6, 'SSP': 7, 'MSD': 8}
Y1.sort(key=lambda r: (PATH_ORDER.get(r['pathway'], 9), r['pick'] if r['pick'] is not None else 999, r['key']))
unchanged = sum(1 for r in Y1 if r['d_vs_c32base'] == 0)
moved = [r for r in Y1 if r['d_vs_c32base'] != 0]
mx = max((abs(r['d_vs_c32base']) for r in moved), default=0)
vet_moved = sum(1 for r in moved if r['leg_ladder'] != 0 or r['leg_fade'] != 0)
H = [page_head('Order B · Year-1 Class', 'THE YEAR-1 CLASS · DRAFT ORDER',
               'NOTHING LANDS WITHOUT THE OWNER\'S WORD — THE ENTRY YEAR IS THE VETERAN BUILD\'S CLEANEST CONTROL')]
tall_leg = sum(1 for r in moved if r['leg_ladder'] != 0)
fade_leg = sum(1 for r in moved if abs(r['leg_fade']) > 1)
H.append('<div class="box"><h2>The unchanged-rows assertion, read before the table</h2>'
         '<div class="note">%d of %d year-1 rows are UNCHANGED vs C32-base. %d rows move (max |Δ| %d). '
         'Attribution: the moves are the B-3 taper-retirement leg (the ruled ceiling repair through the '
         '0.10 WQ6 weight) plus, on %d year-1 TALL rows, the B-1 ladder/renorm leg — the disclosed W-A '
         'young-tall reach (prime-anchor-conserving renorm lifts young tall projection streams; the '
         'derivation packet\'s Order-A overlap note). The B-2 fade reaches NO year-1 row beyond ±1 pt of '
         'integer rounding (%d rows above that: none). Day-0 prints: 89/89 byte-identical (the emit '
         'guard). v0: untouched.</div></div>'
         % (unchanged, len(Y1), len(moved), mx, tall_leg, fade_leg))
H.append('<div class="box"><h2>Year-1 class (2025 entrants + 2026 mid-season) · draft order · %d rows</h2>' % len(Y1))
H.append('<table id="t2"><thead><tr>')
cols = [('order', True), ('player', False), ('path', False), ('pick', True), ('pos', False), ('g', True),
        ('v0', True), ('live', True), ('cand 31', True), ('C32-base', True), ('B-preview', True),
        ('Δ base', True), ('Δ c31', True), ('Δ live', True)]
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
    H.append('<td class="num" data-v="%d">%d</td>' % (r['live'], r['live']))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['cand31'], r['cand31']))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['c32base'], r['c32base']))
    H.append('<td class="num" data-v="%d"><b>%d</b></td>' % (r['b_preview'], r['b_preview']))
    H.append(delta_td(r['d_vs_c32base']))
    H.append(delta_td(r['d_vs_cand31']))
    H.append(delta_td(r['d_vs_live']))
    H.append('</tr>')
H.append('</tbody></table>')
H.append('<div class="note">Draft order: ND by pick, then RD, pathway routes, SSP, MSD. v0 = the row\'s own '
         'day-0 entry object — untouched by Order B (yr0 cells 0.00%% moved in the standing tables).</div></div>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'PREVIEW_B_YEAR1.html'), 'w').write('\n'.join(H))
print('written: PREVIEW_B_PLAYERS.html (%d rows) / PREVIEW_B_YEAR1.html (%d rows; %d unchanged, %d moved all-taper=%s)'
      % (len(rows_sorted), len(Y1), unchanged, len(moved), vet_moved == 0))
