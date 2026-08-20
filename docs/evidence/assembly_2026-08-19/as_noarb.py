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
# PRESENTATION RULING (owner, standing — supersedes the five-board format ON THIS PAGE):
#   "I only ever want to review the no-arb status of the candidate we are working on (and maybe a
#    live board as a reference) unless otherwise stated — all of those historical progress boards
#    are irrelevant to me."
# So the page carries THE CANDIDATE and, as the one reference, THE LIVE BOARD. The historical
# comparison boards (ORDER K, ORDER P, R, the landing candidate) are GONE FROM THE PAGE. They are
# still built, still scored and still on the record in BANDS_ASM.json / BANDS_ASM_out.txt and in
# STANDING_TABLES_ASM.json. Nothing was deleted; it is only off the owner's page.
#
# THE LIVE REFERENCE IS ABSENT AND THE REASON IS PRINTED ON THE PAGE, NOT BURIED HERE. The no-arb
# test does not read a board — it reads a WALK-FORWARD MATRIX (per_entrant_<LABEL>.json), and no
# matrix for the live board 88ce647f exists anywhere in this project's evidence. Every matrix on
# record stamps an `engine_head`, none stamps a board id, so NOTHING ON DISK CAN BE SHOWN TO BE THE
# LIVE BOARD'S, and picking the closest-looking one would be a guess presented to the owner as a
# reference. Building one means building the LIVE ENGINE HEAD, a different commit from the one this
# candidate stands on. That is a real job, not a rerun. It is offered, not faked.
LIVE_ABSENT = True
LABS = [('ASMCAND', '*** THE ASSEMBLY CANDIDATE — THE BOARD UNDER REVIEW ***')]
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
h.append('<div class="sub"><b>THIS PAGE SHOWS THE CANDIDATE ONLY.</b> On your standing instruction '
         'the historical progress boards — ORDER K, ORDER P, R and the landing candidate — are off '
         'this page. They are still built and still scored; they now live in the raw record '
         '(<span class="k">BANDS_ASM.json</span>, <span class="k">BANDS_ASM_out.txt</span>, '
         '<span class="k">STANDING_TABLES_ASM.json</span>) rather than in front of you.</div>')
if LIVE_ABSENT:
    h.append('<div class="sub" style="border-left:3px solid var(--dn);padding-left:10px">'
             '<b>THE LIVE BOARD IS NOT ON THIS PAGE, AND HERE IS WHY.</b> You asked for the live '
             'board <b>88ce647f</b> alongside the candidate as a reference. The no-arb test does not '
             'read a board — it reads a <b>walk-forward matrix</b>, a separate multi-minute build. '
             '<b>No matrix for the live board exists anywhere in this project\'s evidence.</b> The '
             'matrices that are on disk each stamp the engine commit they came from and none stamps '
             'a board, so not one of them can be SHOWN to be the live board\'s — and putting the '
             'closest-looking one in front of you labelled &ldquo;live&rdquo; would be a guess '
             'dressed as a reference. Building it properly means building the live engine commit, '
             'which is a different commit from the one this candidate stands on. That is a real job '
             'rather than a rerun, so it is offered rather than faked. <b>Say the word and it gets '
             'built.</b></div>')

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

# ================= THE POOL ARMS — same page, standing law: one document, both populations =========
ARMJ = os.path.join(HERE, 'STANDING_TABLES_ASM.json')
if os.path.exists(ARMJ):
    AJ = json.load(open(ARMJ))
    ARMS = AJ['arms']
    ARM_ORDER = ['RD', 'MSD', 'UNR', 'IRE', 'PDA', 'PDN', 'SSP', 'PDS', 'ALLPOOL']
    h.append('<h1 style="margin-top:34px">THE POOL ARMS</h1>')
    h.append('<div class="sub">Every pool pathway, both windows, the candidate — the same standing '
             'format as the ND bands above. <b>The cohort clock and the value semantics are the '
             'all-arm instrument\'s own</b> (<code>noarb_table_allarm.py</code>, md5 '
             '<code>8673d7e3…</code>, asserted at run). <b>THE MSD YEAR-1 EXCLUSION:</b> an MSD row '
             'keys its cohort on the DRAFT YEAR ITSELF, not draft+1, because a mid-season draftee\'s '
             'first season IS his draft season — so at year 1 he falls before the first year his path '
             'covers, and those rows are counted PRE-WINDOW and EXCLUDED rather than scored as zero. '
             'That is why MSD\'s yr1 cell reads &quot;—&quot;.</div>')
    for lab, nice in LABS:
        if lab not in ARMS:
            continue
        h.append('<h2>%s</h2>' % esc(nice))
        for wkey, wnice in WIN:
            rows = [(a, ARMS[lab]['%s|%s' % (wkey, a)]) for a in ARM_ORDER
                    if '%s|%s' % (wkey, a) in ARMS[lab]]
            if not rows:
                continue
            h.append('<h2 style="font-size:13px;color:var(--fg)">%s</h2>' % esc(wnice))
            h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">arm</th><th>n</th>'
                     + ''.join('<th>yr%d</th>' % i for i in range(8))
                     + '<th>yr0&rarr;1</th><th>margin</th><th>verdict</th><th>path test</th>'
                       '</tr></thead><tbody>')
            for a, d in rows:
                a01 = d.get('apprec01'); mgn = d.get('margin')
                v, cls = verdict_cell(a01)
                pt = path_test(d.get('path') or [])
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
                cells = ''
                for i in range(8):
                    val = (d.get('path') or [None] * 8)[i] if i < len(d.get('path') or []) else None
                    cells += ('<td data-v="%s">%s</td>'
                              % (val if val is not None else -1,
                                 ('%.3f' % val) if val is not None else '—'))
                note = 'MSD yr1 excluded' if (a == 'MSD' and a01 is None) else v
                h.append('<tr><td class="l">%s</td><td data-v="%d">%d</td>%s'
                         '<td data-v="%s" class="%s">%s</td><td data-v="%s">%s</td>'
                         '<td class="%s">%s</td><td class="%s">%s</td></tr>'
                         % (esc(a), d.get('n', 0), d.get('n', 0), cells,
                            a01 if a01 is not None else -9, cls,
                            ('%+.2f%%' % (100 * a01)) if a01 is not None else '—',
                            mgn if mgn is not None else -9,
                            ('%+.2f%%' % (100 * mgn)) if mgn is not None else '—',
                            cls, note, pcls, ptxt))
            h.append('</tbody></table></div>')
    # the arm-by-arm move, candidate vs every baseline
    MOV = AJ.get('moves', {})
    if MOV:
        h.append('<h2>The arm-by-arm move — the candidate against every baseline</h2>')
        h.append('<div class="sub">On the yr0&rarr;1 appreciation. A POSITIVE move means the candidate '
                 'appreciates MORE over year one than the baseline does. <b>A verdict change is called '
                 'out on its own line.</b></div>')
        for key in sorted(MOV):
            wkey, lab = key.split('|')
            h.append('<h2 style="font-size:13px;color:var(--fg)">%s &nbsp;·&nbsp; candidate vs %s</h2>'
                     % (esc(wkey), esc(lab)))
            h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">arm</th>'
                     '<th>candidate</th><th>%s</th><th>move</th><th>verdict</th></tr></thead><tbody>'
                     % esc(lab))
            for a in ARM_ORDER:
                m = MOV[key].get(a)
                if not m:
                    continue
                chg = m.get('changed')
                h.append('<tr%s><td class="l">%s</td><td data-v="%f">%+.2f%%</td>'
                         '<td data-v="%f">%+.2f%%</td><td data-v="%f">%+.2f%%</td>'
                         '<td class="%s">%s &rarr; %s%s</td></tr>'
                         % (' class="red"' if chg else '', esc(a),
                            m['cand'], 100 * m['cand'], m['base'], 100 * m['base'],
                            m['move'], 100 * m['move'], 'flag' if chg else '',
                            esc(m['v_cand']), esc(m['v_base']),
                            ' &nbsp;<b>*** VERDICT CHANGES ***</b>' if chg else ''))
            h.append('</tbody></table></div>')

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
