#!/usr/bin/env python3
"""ORDER M — THE OWNER DOCUMENT.

  ORDER_M_NOARB.html   what a board with eta = 0 actually reads, in the standing no-arb format,
                       BOTH windows, every ND band and every pool arm, with comparison columns for
                       ORDER K, the landing candidate and candidate 31 — plus the trade-off ladder
                       in board points on the owner's own named rows.

House conventions carried from o32_pages.py (same CSS, same column grammar), exactly as ORDER K and
ORDER L carried them. The click-to-sort script is NOT carried: these are fixed comparison tables with
a meaningful row order, not browsable lists, and a sort control that does nothing would be a lie.

The "what is in this board and what is still broken" box is sliced out of the published ORDER_K_NOARB.html BYTE FOR BYTE, not retyped, so it
cannot drift; ORDER M's own breakage box is written beneath it and clearly labelled as this order's.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
KDIR = os.path.join(ROOT, 'docs', 'evidence', 'order_k_2026-08-18')
B = json.load(open(os.path.join(HERE, 'BANDS_M.json')))
A = json.load(open(os.path.join(HERE, 'ARMS_M.json')))
C = json.load(open(os.path.join(HERE, 'CLASS_M.json')))
G = json.load(open(os.path.join(HERE, 'GATES_M.json')))
LD = json.load(open(os.path.join(HERE, 'LADDER_M.json')))
TD = json.load(open(os.path.join(HERE, 'TRADEOFF_M.json')))
SW = json.load(open(os.path.join(HERE, 'SWEEP_M.json')))

src = open(os.path.join(ROOT, 'docs', 'evidence', 'order_a_2026-08-17', 'o32_pages.py')).read()
CSS = src.split('CSS = """')[1].split('"""')[0]
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
td.hi{background:rgba(255,120,90,.14)}
"""

KHTML = open(os.path.join(KDIR, 'ORDER_K_NOARB.html')).read()
i0 = KHTML.index('<div class="brk">')
i1 = KHTML.index('</div>', KHTML.index('One thing to know about the numbers you were shown before')) + 6
BROKEN_BOX = KHTML[i0:i1]
assert BROKEN_BOX.startswith('<div class="brk">') and BROKEN_BOX.endswith('</div>')
assert 'still broken' in BROKEN_BOX

LABELS = [('M0ETA0', 'ETA = 0'), ('MLOETA0', 'ETA = 0, coolest'), ('MMIN031', 'dose 0, eta .31'),
          ('OKRULED', 'ORDER K'), ('O35FINAL', 'landing'), ('O31FFINAL', 'cand 31')]
BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64', 'picks 1-10', 'picks 11-20',
         'picks 21-30', 'picks 31-40', 'picks 41-64']
ARMS = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']
H = []


def e(s):
    return html.escape(str(s))


def pc(v, rail_hi=0.14, rail_lo=0.0):
    if v is None:
        return '<td class="num">&mdash;</td>'
    cls = 'num'
    if v > rail_hi or v < rail_lo:
        cls = 'num hi'
    return '<td class="%s">%+.2f%%</td>' % (cls, 100 * v)


def head(title, sub):
    return ('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">NOTHING LANDS ON THIS SEAT&rsquo;S WORD &mdash; ORDER M IS A TEST, '
            'NOT A CANDIDATE. NO BOARD HERE IS PROPOSED FOR ADOPTION.</div>\n'
            '<h1>%s</h1><p class="sub">%s</p>\n' % (e(title), CSS, e(title), sub))


H.append(head('ORDER M — the board with eta set to zero',
              'The owner ruled that the counterweight&rsquo;s blind half must not ship. This document is '
              'what the board reads once it is gone. Every number here comes off a BUILT board and the '
              'standing instrument. Both windows on every table, as ORDER L made standing.'))

# ------------------------------------------------------------------ the headline
H.append('<div class="brk"><h2>THE ANSWER, BEFORE ANY TABLE</h2>'
         '<h3>What eta = 0 delivers</h3><ul>'
         '<li><b>Harry Dean goes from 2,403 to 3,069.</b> Your reference was ~2,600. He clears it by 469.</li>'
         '<li><b>Cooper Duff-Tytler goes from 1,505 to 2,057.</b> Your reference was ~1,800. He clears '
         'it by 257.</li>'
         '<li>Picks 31-40 improve from &minus;10.70% to &minus;1.57%. Picks 41-64 turn positive, '
         '&minus;6.89% to +1.71%. That is your G2, satisfied for the first time.</li></ul>'
         '<h3>What eta = 0 breaks</h3><ul>'
         '<li><b>The year-1 class mark goes to 1.2046 on the registered basis.</b> Your buy rail is '
         '1.14. It is over by 0.065. A whole draft class becomes a free trade.</li>'
         '<li><b>Picks 1-10 read +31.58% in the primary window and +37.46% in the modern one.</b> Your '
         'rail is +14%.</li>'
         '<li><b>All three sub-expectation rows rise.</b> Xavier Taylor +169, Daniel Annable +231, '
         'Dylan Patterson +357, against the landing candidate. Kappa alone cannot charge them.</li>'
         '<li><b>There is no dose that fixes this.</b> Every one of the 7,560 settings swept with eta '
         'at zero breaks your +14% band rail. The coolest one reachable still reads picks 1-10 at '
         '+22.40%. Even with the age bar switched off entirely.</li></ul>'
         '<h3>What that means</h3><ul>'
         '<li>Eta was not paying for the age bar. Eta was holding down the whole board&rsquo;s '
         'first-year appreciation. At dose 0.00 &mdash; no age bar at all &mdash; the board still needs '
         'eta of at least 0.31 to stay inside your own rails.</li>'
         '<li>The blind half is load-bearing. The age bar cannot ship in its current form with eta at '
         'zero. The trade-off curve below is so you can choose knowingly.</li></ul></div>')

# ------------------------------------------------------------------ G1
H.append('<h2>G1 &mdash; the year-1 class mark, on the registered basis</h2>')
H.append('<p class="sub">The W2 scorer, draft classes 2005-2015, ENTRY_FLOOR 2005. This is the '
         'instrument your 1.03 floor and your ~1.08 prior were registered against (ORDER L). The '
         'cohort-window reading is printed beside it so the two are never confused again.</p>')
H.append('<table><thead><tr><th>board</th><th class="num">registered basis '
         '(W2, draft 05-15)</th><th class="num">vs the 1.03 floor</th><th class="num">vs the 1.14 buy '
         'rail</th><th class="num">cohort window (ok_class 05-15)</th><th>G1</th></tr></thead><tbody>')
for lab, nice in LABELS:
    v = C['w2'][lab]['mean_0515']; co = C['ok_class'][lab]['mean_0515']
    ok = (v >= 1.03) and (v < 1.14)
    H.append('<tr><td>%s</td><td class="num%s">%.4f</td><td class="num">%+.4f</td>'
             '<td class="num">%+.4f</td><td class="num">%.4f</td><td class="%s">%s</td></tr>'
             % (e(nice), '' if ok else ' hi', v, v - 1.03, v - 1.14, co,
                'ok' if ok else 'warn',
                'PASS' if ok else ('FAIL &mdash; above the 1.14 buy rail' if v >= 1.14
                                   else 'FAIL &mdash; under the 1.03 floor')))
H.append('</tbody></table>')

# ------------------------------------------------------------------ ND bands, both windows
H.append('<h2>The ND bands, year 0 &rarr; 1, in BOTH windows</h2>')
H.append('<p class="sub">Below 0% is a sell-side red. Above +14% is a buy-side red. Cells outside '
         'either rail are shaded. PRIMARY = cohorts 2005-2023. MODERN = cohorts 2019-2023.</p>')
for w in ('PRIMARY', 'MODERN'):
    H.append('<h3>%s window</h3>' % w)
    H.append('<table><thead><tr><th>band</th>'
             + ''.join('<th class="num">%s</th>' % e(n) for _, n in LABELS)
             + '</tr></thead><tbody>')
    for bn in BANDS:
        cells = []
        for lab, _ in LABELS:
            r = B['nd'][lab]['%s|ALLCOH|%s' % (w, bn)]
            cells.append(pc(r['apprec01']))
        H.append('<tr><td>%s</td>%s</tr>' % (e(bn), ''.join(cells)))
    H.append('</tbody></table>')

# ------------------------------------------------------------------ pool arms
H.append('<h2>The pool arms, year 0 &rarr; 1, in BOTH windows</h2>')
H.append('<p class="sub">SSP&rsquo;s buy-side red is INHERITED &mdash; it is on the landing candidate '
         'and on candidate 31 too. It is reported here, never masked, and eta = 0 makes it worse '
         '(+52.71% &rarr; +64.96%).</p>')
for w in ('PRIMARY', 'MODERN'):
    H.append('<h3>%s window</h3>' % w)
    H.append('<table><thead><tr><th>arm</th>'
             + ''.join('<th class="num">%s</th>' % e(n) for _, n in LABELS)
             + '</tr></thead><tbody>')
    for arm in ARMS:
        cells = []
        any_row = False
        for lab, _ in LABELS:
            r = A['arms'][lab].get('%s|ALLCOH|%s' % (w, arm))
            v = r.get('apprec01') if r else None
            if v is not None:
                any_row = True
            cells.append(pc(v))
        if any_row:
            H.append('<tr><td>%s</td>%s</tr>' % (e(arm), ''.join(cells)))
    H.append('</tbody></table>')

# ------------------------------------------------------------------ the named rows
H.append('<h2>Your named rows, in board points</h2>')
NROWS = ['harry-dean', 'cooper-duff-tytler', 'isaac-kako', 'alix-tauru', 'jedd-busslinger',
         'xavier-taylor', 'daniel-annable', 'dylan-patterson', 'josh-smillie', 'oskar-taylor',
         'will-green', 'toby-conway', 'william-mccabe', 'alex-dodson', 'milan-murdock']
H.append('<table><thead><tr><th>row</th><th class="num">cand 31</th>'
         '<th class="num">landing</th><th class="num">ORDER K</th><th class="num">ETA = 0</th>'
         '<th class="num">dose 0, eta .31</th><th class="num">eta 0 &minus; ORDER K</th>'
         '</tr></thead><tbody>')
for k in NROWS:
    r = G['named'].get(k)
    if not r:
        continue
    H.append('<tr><td>%s</td><td class="num">%s</td><td class="num">%d</td><td class="num">%d</td>'
             '<td class="num">%d</td><td class="num">%d</td><td class="num">%+d</td></tr>'
             % (e(k), e(r.get('c31') if r.get('c31') is not None else '—'),
                r['cand'], r['K'], r['M0'], r['MMIN'], r['M0'] - r['K']))
H.append('</tbody></table>')

# ------------------------------------------------------------------ the trade-off ladder
H.append('<h2>The trade-off, priced</h2>')
H.append('<p class="sub">Ladder A walks eta from 0 to 0.50 at your ruled dose 0.40, every other knob '
         'held. It answers one question: is there an eta that gives you Harry Dean AND holds the three '
         'sub-expectation rows AND keeps the board legal?</p>')
H.append('<table><thead><tr><th>eta</th><th class="num">harry-dean</th>'
         '<th class="num">duff-tytler</th><th class="num">xavier-taylor</th>'
         '<th class="num">daniel-annable</th><th class="num">dylan-patterson</th>'
         '<th class="num">class (nav)</th><th class="num">picks 1-10 (nav)</th><th>legal?</th>'
         '</tr></thead><tbody>')
base = dict(dean=2400, cdt=1572, xavier=1176, annable=1530, patterson=1467)
H.append('<tr><td>landing</td><td class="num">2400</td><td class="num">1572</td>'
         '<td class="num">1176</td><td class="num">1530</td><td class="num">1467</td>'
         '<td class="num">1.0421</td><td class="num">+7.20%</td><td>&mdash;</td></tr>')
for r in LD['ladderA']:
    legal = 'LEGAL' if r['eta'] >= 0.50 else 'illegal'
    H.append('<tr><td>%.2f</td><td class="num%s">%d</td><td class="num%s">%d</td>'
             '<td class="num%s">%d</td><td class="num%s">%d</td><td class="num%s">%d</td>'
             '<td class="num">%s</td><td class="num">%s</td><td class="%s">%s</td></tr>'
             % (r['eta'],
                '' if r['dean'] >= 2600 else ' hi', r['dean'],
                '' if r['cdt'] >= 1800 else ' hi', r['cdt'],
                ' hi' if r['xavier'] > base['xavier'] else '', r['xavier'],
                ' hi' if r['annable'] > base['annable'] else '', r['annable'],
                ' hi' if r['patterson'] > base['patterson'] else '', r['patterson'],
                e(r['nav_class']), e(r['nav_110']),
                'ok' if legal == 'LEGAL' else 'warn', legal))
H.append('</tbody></table>')
H.append('<p class="sub">Ladder B is the legal frontier itself: at each dose, the smallest eta the '
         'board can carry. It answers the other question: over the whole legal region, what is the '
         'best Harry Dean you can buy?</p>')
H.append('<table><thead><tr><th>dose</th><th class="num">smallest legal eta</th>'
         '<th class="num">harry-dean</th><th class="num">duff-tytler</th>'
         '<th class="num">xavier-taylor</th><th class="num">daniel-annable</th>'
         '<th class="num">dylan-patterson</th><th class="num">veteran net move</th>'
         '</tr></thead><tbody>')
for r in LD['ladderB']:
    H.append('<tr><td>%.2f</td><td class="num">%s</td><td class="num">%d</td><td class="num">%d</td>'
             '<td class="num">%d</td><td class="num">%d</td><td class="num">%d</td>'
             '<td class="num">%+d</td></tr>'
             % (r['dose'], '%.2f' % r['eta'] if r['eta'] > 0 else 'none — ILLEGAL',
                r['dean'], r['cdt'], r['xavier'], r['annable'], r['patterson'], r['vet_net']))
H.append('</tbody></table>')

H.append('<h2>How much eta the board needs, dose by dose</h2>')
H.append('<p class="sub">Kappa, gamma_u, gamma_d and lambda_rel held at your ruled values, so eta is '
         'the only thing moving. Read the top row: even with the age bar switched off entirely, the '
         'board needs eta of 0.31.</p>')
H.append('<table><thead><tr><th>S1 dose</th><th class="num">smallest eta that keeps '
         'every band inside +14%</th><th class="num">smallest eta that keeps every class inside '
         '1.139</th><th class="num">class mark at that eta</th><th class="num">picks 1-10 at that '
         'eta</th></tr></thead><tbody>')
for r in TD['q1_min_eta_by_dose']:
    at = r['at']
    H.append('<tr><td>%.2f</td><td class="num">%s</td><td class="num">%s</td><td class="num">%s</td>'
             '<td class="num">%s</td></tr>'
             % (r['dose'],
                '%.2f' % r['eta_band'] if r['eta_band'] is not None else 'none exists',
                '%.2f' % r['eta_maxclass'] if r['eta_maxclass'] is not None else 'none exists',
                '%.4f' % at['mean_0515'] if at else '&mdash;',
                '%+.2f%%' % (100 * (at['band']['1-10'] - 1)) if at else '&mdash;'))
H.append('</tbody></table>')

# ------------------------------------------------------------------ the sweep
H.append('<h2>The whole eta = 0 grid, and what it breaks</h2>')
H.append('<p class="sub">7,560 settings. S1 dose &times; kappa &times; gamma_u &times; lambda_rel, '
         'with eta pinned at zero. Gamma_d is inert at eta = 0 and was not swept.</p>')
H.append('<table><thead><tr><th>rail</th><th class="num">settings that break it</th>'
         '<th>note</th></tr></thead><tbody>')
for k, v in sorted(SW['law_fail_counts'].items(), key=lambda x: -x[1]):
    H.append('<tr><td>%s</td><td class="num">%d of 7560</td><td>%s</td></tr>'
             % (e(k), v, 'your own law'))
for k, v in sorted(SW['ruled_fail_counts'].items(), key=lambda x: -x[1]):
    H.append('<tr><td>%s</td><td class="num">%d of 7560</td><td>%s</td></tr>'
             % (e(k), v, 'inherited ruled constraint'))
H.append('</tbody></table>')
H.append('<p class="sub"><b>Settings legal on your laws: 0 of 7,560. Settings legal on the inherited '
         'ruled constraints: 0 of 7,560.</b> The coolest setting anywhere in the grid still reads '
         'picks 1-10 at +22.40% and a worst class of 1.2067.</p>')

H.append('<h2>Carried from ORDER K &mdash; what is in this board and what is still broken</h2>')
H.append('<p class="sub">Sliced byte for byte out of the published ORDER_K_NOARB.html so it cannot '
         'drift. Everything it says is still true; ORDER M adds to it, it does not replace it.</p>')
H.append(BROKEN_BOX)
H.append('<div class="brk"><h2>AND WHAT ORDER M ADDS TO THAT LIST</h2><ul>'
         '<li><b>Eta at zero is not shippable at any dose.</b> 0 of 7,560 settings clear your laws.</li>'
         '<li><b>Kappa cannot replace eta as the charge on sub-expectation rows.</b> All three named '
         'rows rise even with the age bar off and kappa at its highest monotone value.</li>'
         '<li><b>The veteran pool moves the wrong way without eta.</b> Net +2,781 board points against '
         'a 668 line &mdash; four times the breach ORDER K reported, and in the opposite direction.</li>'
         '<li><b>The modern window is tighter than the primary one on picks 1-10.</b> Even '
         'dose 0 with eta 0.31 reads +15.11% there, outside your rail, while its primary reading '
         '(+9.84%) looks safe. Read both.</li></ul></div>')

open(os.path.join(HERE, 'ORDER_M_NOARB.html'), 'w').write('\n'.join(H))
print('wrote ORDER_M_NOARB.html  (%d bytes)'
      % os.path.getsize(os.path.join(HERE, 'ORDER_M_NOARB.html')))
