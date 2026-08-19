#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE STANDING NO-ARB TABLES, in the owner's standing format.

Five ND bands PLUS the classic three (ALL 1-64 / 1-20 / 21-64), in BOTH windows (PRIMARY cohorts
2005-2023, MODERN cohorts 2019-2023), every board as its own baseline row, with:

  * the year path yr0..yr7,
  * the yr0 -> yr1 appreciation,
  * the buy-side margin against the 14% carry,
  * a two-sided verdict,
  * and THE OWNER'S PATH TEST scored on EVERY BREACHING CELL.

THE PATH TEST, as the owner gave it and as PREREG_S.md §7 froze it BEFORE any table was read:
  CARRY compounds at 14% a year: 1.140 1.300 1.482 1.689 1.925 2.195 2.502 for years 1..7.
  A cell BREACHES when its year-1 appreciation exceeds +14%.
  For a breaching cell:
    limb (a) "the path afterwards does not keep beating carry"
             PASSES when the count of years k in 2..7 with path_k > carry_k is ZERO.
    limb (b) "the end destination does not keep increasing"
             PASSES when path_7 <= path_6 AND path_7 <= carry_7.
    The cell PASSES only when BOTH limbs pass.
EVERY RAW YEAR IS PRINTED so the owner can apply his own reading rather than this seat's.

Reading rule in plain words: a group is fairly priced if it appreciates between 0% and +14% over its
first year. Below 0% is a SELL-SIDE RED. Above +14% is a BUY-SIDE RED.

NOTHING IS ADOPTED. NO ENGINE RUN HERE — pure reads over BANDS_ASM.json.
"""
import json, os, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import as_box as BOX
from as_pages import CSS, JS, esc  # same house CSS/sort script, one source

BD = json.load(open(os.path.join(HERE, 'BANDS_ASM.json')))['nd']
CARRY = [1.140, 1.300, 1.482, 1.689, 1.925, 2.195, 2.502]      # years 1..7 at 14%
BANDS = ['ALL picks 1-64', 'picks 1-20', 'picks 21-64',
         'picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
WIN = [('PRIMARY', 'PRIMARY — cohorts 2005-2023 (the whole ND population)'),
       ('MODERN', 'MODERN — cohorts 2019-2023')]
LABS = [('ASMCAND', '*** THE ASSEMBLY CANDIDATE — THE BOARD UNDER REVIEW ***'),
        ('R20A', 'R = R20A 7f88f509 — the owner\'s reference'),
        ('PBUILT', 'ORDER P 374d4e44 — the assembly base'),
        ('OKRULED', 'ORDER K f3101883'),
        ('O35FINAL', 'the landing candidate 1f176444')]
VKEY = 'ALLCOH'


def path_test(path):
    """Returns (breaches, limb_a_pass, limb_b_pass, overall, beat_years)."""
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
    return dict(breaches=True, limb_a=la, limb_b=lb, both=(la and lb), beat=beat,
                ratios=r, a01=a01)


def verdict_cell(a01):
    if a01 is None:
        return ('n/a', '')
    if a01 < 0.0:
        return ('SELL-SIDE RED', 'red')
    if a01 > 0.14:
        return ('BUY-SIDE RED', 'red')
    return ('fair', '')


h = []
h.append('<div class="sub">The owner\'s standing format. A group is fairly priced if it appreciates '
         'between 0% and +14% over its first year — below 0% you could sell at draft day and buy back '
         'cheaper, above +14% you could buy at draft day and beat the cost of carrying him. '
         '<b>Every breaching cell is scored on the owner\'s own path test</b>, and every raw year is '
         'printed so he can apply his own reading. <b>* thin cell · ** very thin.</b></div>')

for lab, nice in LABS:
    if lab not in BD:
        h.append('<h2>%s</h2><div class="sub k">NOT AVAILABLE — no matrix for this board.</div>'
                 % esc(nice))
        continue
    h.append('<h2>%s</h2>' % esc(nice))
    for wkey, wnice in WIN:
        rows = []
        for b in BANDS:
            k = '%s|%s|%s' % (wkey, VKEY, b)
            if k in BD[lab]:
                rows.append((b, BD[lab][k]))
        if not rows:
            continue
        h.append('<h2 style="font-size:13px;color:var(--fg)">%s</h2>' % esc(wnice))
        h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">band</th><th>n</th>'
                 + ''.join('<th>yr%d</th>' % i for i in range(8))
                 + '<th>yr0&rarr;1</th><th>margin</th><th>verdict</th>'
                   '<th>path test</th></tr></thead><tbody>')
        for b, d in rows:
            pth = d.get('path') or []
            a01 = d.get('apprec01')
            mgn = d.get('buy_margin')
            v, cls = verdict_cell(a01)
            pt = path_test(pth)
            if pt is None or not pt.get('breaches'):
                ptxt, pcls = ('—', '')
            elif pt['both']:
                ptxt, pcls = ('PASSES both limbs', '')
            else:
                fails = []
                if not pt['limb_a']:
                    fails.append('beats carry in yr %s' % ','.join(str(x) for x in pt['beat']))
                if not pt['limb_b']:
                    fails.append('still rising at yr7')
                ptxt, pcls = ('FAILS — ' + '; '.join(fails), 'red')
            flags = d.get('flags') or []
            cells = ''
            for i in range(8):
                val = pth[i] if i < len(pth) else None
                fl = flags[i] if i < len(flags) else 'ok'
                mark = {'ok': '', 'thin': '*', 'vthin': '**'}.get(fl, '')
                cells += ('<td data-v="%s">%s</td>'
                          % (val if val is not None else -1,
                             ('%.3f%s' % (val, mark)) if val is not None else '—'))
            h.append('<tr><td class="l">%s</td><td data-v="%d">%d</td>%s'
                     '<td data-v="%s" class="%s">%s</td><td data-v="%s">%s</td>'
                     '<td class="%s">%s</td><td class="%s">%s</td></tr>'
                     % (esc(b), d.get('n', 0), d.get('n', 0), cells,
                        a01 if a01 is not None else -9, cls,
                        ('%+.2f%%' % (100 * a01)) if a01 is not None else '—',
                        mgn if mgn is not None else -9,
                        ('%+.2f%%' % (100 * mgn)) if mgn is not None else '—',
                        cls, v, pcls, ptxt))
        h.append('</tbody></table></div>')

h.append('<div class="sub"><b>THE CARRY LINE the path test is scored against:</b> '
         + ' · '.join('yr%d %.3f' % (i + 1, c) for i, c in enumerate(CARRY)) + '</div>')

page = '\n'.join(['<title>Assembly No-Arb</title>', '<style>%s</style>' % CSS,
                  '<h1>THE NO-ARB TABLES — THE CANDIDATE</h1>',
                  '<div class="sub">Five ND bands plus ALL / 1-20 / 21-64, in BOTH windows, every '
                  'board as its own baseline, with the owner\'s path test on every breaching cell.</div>',
                  BOX.html_box(), '\n'.join(h), '<script>%s</script>' % JS])
open(os.path.join(HERE, 'ASSEMBLY_NOARB.html'), 'w').write(page)
print('ASSEMBLY_NOARB.html written — %d boards' % sum(1 for l, _ in LABS if l in BD))
for lab, _ in LABS:
    if lab not in BD:
        continue
    for wkey, _w in WIN:
        br = []
        for b in BANDS:
            k = '%s|%s|%s' % (wkey, VKEY, b)
            if k not in BD[lab]:
                continue
            pt = path_test(BD[lab][k].get('path') or [])
            if pt and pt.get('breaches'):
                br.append('%s:%s' % (b, 'PASS' if pt['both'] else 'FAIL'))
        if br:
            print('  %-9s %-8s breaching cells -> %s' % (lab, wkey, ' · '.join(br)))
