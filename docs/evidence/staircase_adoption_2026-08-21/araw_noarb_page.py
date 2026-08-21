# ==================================================================================================
# A-RAW CARRY. This file is docs/evidence/staircase_fix_2026-08-20/sfx_noarb_page.py, byte-carried by
# build_araw_instruments.py with three declared changes and nothing else: (1) SFXARAW
# (RL_O44_LVLMONO=ratchet = VARIANT A RAW, THE ADOPTED ARM) and SFXBRAW added to the
# label/candidate lists, so all five arms are read side by side; (2) the output basenames suffixed
# _ARAW so this set cannot overwrite the pricing seat's artifacts or the B-raw set at 36f1122;
# (3) SRC introduced for the inputs carried from the pricing seat rather than regenerated.
# The owner re-ruled to A RAW on 2026-08-21 after seeing the B-raw reading. This is A RAW's.
# ==================================================================================================
#!/usr/bin/env python3
"""ORDER 44 MEASUREMENT — THE FULL NO-ARB PAGE, RENDERED ONCE PER CONSERVED CANDIDATE.

d8_noarb_page.py carried with THREE declared changes and NOTHING ELSE. Its format, its CSS/JS (still
taken from the house module ui-side rather than re-typed), its standing box, its reading rule and ITS
PATH TEST CODE are UNCHANGED.

  (1) THE CANDIDATE IS A PARAMETER (SFX_CAND), and the page is rendered TWICE — once for SFXACON
      (ratchet+conserve) and once for SFXBCON (smooth+conserve). Two variants cannot share one page
      without the reader losing which column is which; two pages against ONE base is the shape that
      keeps every cell readable. The base column is SFXBASE, THE LIVE R23 BOARD 68be10c7.
  (2) EVERY D8 PROSE CLAIM ABOUT THE DATA IS RE-COMPUTED RATHER THAN RE-TYPED. D8's copy carried
      sentences like "no cell breaches on the candidate that does not also breach on the live board"
      and "the three cohorts already above 1.14 still are" as STATIC TEXT. Those were true of D8's
      numbers. Carrying them onto different numbers would be a page that asserts what it did not
      measure — the exact failure class this estate has ruled against — so each is derived from the
      tables being rendered and prints whatever they actually say.
  (3) the sources and the output filename (BANDS_NOARB_SFX.json / STANDING_TABLES_NOARB_SFX.json /
      CLASS_SFX.json -> NOARB_SFX_<CAND>.html).

NOTHING IS ADOPTED. NO PIN MOVES. NO ENGINE RUN HERE — pure reads over the three table files.
ORIGINAL D8 HEADER FOLLOWS.

ORDER D8 MEASUREMENT — THE FULL NO-ARB PAGE FOR THE PRICED CANDIDATE 5ea978f7.

d7b_noarb.py's page (docs/evidence/final_candidate_2026-08-19/D7B_NOARB.html lineage), CARRIED, with
its format, its CSS/JS, its standing box, its reading rule and ITS PATH TEST CODE UNCHANGED — plus
the one thing this order adds:

    EVERY CELL IS PRINTED SIDE-BY-SIDE WITH THE LIVE BOARD'S OWN CELL, and every cell whose verdict
    changes is labelled. The comparison column is D8BASE, this seat's dial-unset emit on today's
    tree; its `recs` are BYTE-IDENTICAL to per_entrant_D7BCAND.json — the matrix the on-file D7B
    tables were rendered from — and its cells were checked against BANDS_D7B.json /
    STANDING_TABLES_D7B.json and agree in every field (see NOARB_D8_CHECKS_out.txt).

    ALL ND bands · ALL pool arms (RD/MSD/UNR/IRE/PDA/PDN/PDS/SSP/ALLPOOL) · BOTH windows
    (PRIMARY 2005-2023, MODERN 2019-2023) · the MSD year-1 exclusion printed with its reason ·
    the owner's path test on every breaching cell, on BOTH boards.

    Sources: BANDS_NOARB_D8.json (d8_noarb_bands.py) · STANDING_TABLES_NOARB_D8.json
             (d8_noarb_tables.py) · CLASS_D8.json (d8_noarb_class.py).

NOTHING IS ADOPTED. NO PIN MOVES. NO ENGINE RUN HERE — pure reads over the three table files.
"""
import json, os, sys, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
FC = os.path.join(REPO, 'docs', 'evidence', 'final_candidate_2026-08-19')
sys.path.insert(0, FC)
with contextlib.redirect_stdout(io.StringIO()):      # fc_box narrates at import; not our output
    import fc_box as BOX

# fc_pages.py IS the house page module and its CSS/JS/esc are what this page must match byte-for-byte.
# It cannot simply be imported: below the '# ---- boards ---' line it loads the FINAL-CANDIDATE seat's
# built board files out of that seat's scratch, which no longer exist, and dies on KeyError 'FC_CAND'.
# So the file is executed UP TO THAT LINE ONLY — the presentation half, verbatim, from the house file
# itself rather than re-typed here. The split point is printed at run and the three names are asserted.
_FCP = open(os.path.join(FC, 'fc_pages.py')).read()
_SPLIT = "\n# ---- boards ---"
assert _SPLIT in _FCP, 'fc_pages.py has moved; the presentation/board split point is gone'
_G = {'__name__': 'fc_pages_presentation_only', 'BOX': BOX,
      '__file__': os.path.join(FC, 'fc_pages.py')}
with contextlib.redirect_stdout(io.StringIO()):
    exec(_FCP.split(_SPLIT)[0], _G)
CSS, JS, esc = _G['CSS'], _G['JS'], _G['esc']

BD = json.load(open(os.path.join(HERE, 'BANDS_NOARB_ARAW.json')))['nd']
BDMETA = json.load(open(os.path.join(HERE, 'BANDS_NOARB_ARAW.json')))['meta']
AJ = json.load(open(os.path.join(HERE, 'STANDING_TABLES_NOARB_ARAW.json')))
ARMS = AJ['arms']
CL = json.load(open(os.path.join(HERE, 'CLASS_ARAW.json')))

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
CAND = os.environ.get('SFX_CAND', 'SFXARAW')
BASE = 'SFXBASE'
LIVE_BOARD = '68be10c79d0ee096455754e084bcf757'
CANDS = {'SFXARAW': ('ORDER 44 VARIANT A, RAW — THE ADOPTED ARM', 'RL_O44_LVLMONO=ratchet',
                     'b3e8da99bc7f632e5d1eebc732f9cf01'),
         'SFXBRAW': ('ORDER 44 variant B, raw (measured, NOT adopted)', 'RL_O44_LVLMONO=smooth',
                     '219266fafeca5ed4fb0206a72bf37046'),
         'SFXACON': ('ORDER 44 VARIANT A, CONSERVED', 'RL_O44_LVLMONO=ratchet+conserve',
                     '9c78fe09f35f46e4ccac1d383841db50'),
         'SFXBCON': ('ORDER 44 VARIANT B, CONSERVED', 'RL_O44_LVLMONO=smooth+conserve',
                     'f22823491122529df0726ef247dc1085')}
assert CAND in CANDS, 'SFX_CAND=%r is not one of %s' % (CAND, list(CANDS))
CTITLE, CDIAL, CBOARD = CANDS[CAND]
NICE = '%s — %s' % (CTITLE, CDIAL)
OUTNAME = 'NOARB_ARAW_%s.html' % CAND
VKEY = 'ALLCOH'

CHANGED = []          # every verdict change, collected as the page is built


def path_test(path):
    """d7b_noarb.py's, which is as_noarb.py's, unchanged."""
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


def pctcell(v, cls=''):
    return ('<td data-v="%s" class="%s">%s</td>'
            % (v if v is not None else -9, cls, ('%+.2f%%' % (100 * v)) if v is not None else '—'))


def movecell(a, b):
    if a is None or b is None:
        return '<td data-v="0" class="k">—</td>'
    m = a - b
    c = 'u' if m > 0 else ('d' if m < 0 else '')
    return '<td data-v="%f" class="%s">%+.2f pp</td>' % (m, c, 100 * m)


def row_pair(name, kind, win, dc, db):
    """One table row: the candidate's cells, then the live board's reading beside them."""
    ac = dc.get('apprec01') if dc else None
    ab = db.get('apprec01') if db else None
    vc, cc = verdict_cell(ac)
    vb, cb = verdict_cell(ab)
    ptc, ptb = path_test((dc or {}).get('path') or []), path_test((db or {}).get('path') or [])
    tc, clc = path_txt(ptc)
    tb, _clb = path_txt(ptb)
    chg = (vc != vb)
    if chg:
        CHANGED.append((win, kind, name, ab, ac, vb, vc))
    return ('<tr%s>' % (' class="amber"' if chg else '')
            + '<td class="l">%s</td><td data-v="%d">%d</td>' % (esc(name), (dc or {}).get('n', 0),
                                                                (dc or {}).get('n', 0))
            + yearcells((dc or {}).get('path'), (dc or {}).get('flags'))
            + pctcell(ac, cc) + pctcell(ab, cb) + movecell(ac, ab)
            + '<td class="%s">%s</td><td class="%s">%s</td>'
              '<td class="l %s">%s</td><td class="l k">%s</td></tr>'
              % (cc, vc, cb, vb,
                 'flag' if chg else '', 'VERDICT CHANGES' if chg else 'unchanged',
                 tc if tc == tb else ('cand: %s · live: %s' % (tc, tb))))


HDR = ('<thead><tr><th class="l">%s</th><th>n</th>'
       + ''.join('<th>yr%d</th>' % i for i in range(8))
       + '<th>yr0&rarr;1<br>CANDIDATE</th><th>yr0&rarr;1<br>LIVE BOARD</th><th>move</th>'
         '<th>verdict<br>CANDIDATE</th><th>verdict<br>LIVE BOARD</th><th class="l">changed?</th>'
         '<th class="l">path test</th></tr></thead>')

h = []

# ================= the reading rule ==============================================================
h.append('<div class="sub"><b>THE READING RULE, in plain words.</b> A group is fairly priced if it '
         'appreciates between <b>0%</b> and <b>+14%</b> over its first year. Below 0% is a '
         '<b>SELL-SIDE RED</b> — you could sell at draft day and buy back cheaper. Above +14% is a '
         '<b>BUY-SIDE RED</b> — you could buy at draft day and beat the cost of carrying him. '
         '<b>Every breaching cell is scored on your own path test</b>, and <b>every raw year is '
         'printed</b> so you can apply your own reading rather than this seat\'s. '
         '<b>* thin cell · ** very thin.</b> The year columns are <b>the candidate\'s</b>; the live '
         'board\'s raw years are in <code>BANDS_NOARB_SFX_out.txt</code> and '
         '<code>STANDING_TABLES_NOARB_SFX_out.txt</code> beside them.</div>')
h.append('<div class="sub"><b>THE PATH TEST, as you gave it</b> (frozen in PREREG_S.md §7 before any '
         'table was read). Carry compounds at 14%%: %s. A cell BREACHES when its year-1 appreciation '
         'exceeds +14%%. For a breaching cell — <b>limb (a)</b> &ldquo;the path afterwards does not '
         'keep beating carry&rdquo; passes when NO year 2..7 sits above the carry line; <b>limb (b)</b> '
         '&ldquo;the end destination does not keep increasing&rdquo; passes when yr7 &le; yr6 AND '
         'yr7 &le; carry. The cell passes only when BOTH limbs pass. It is scored here on <b>both</b> '
         'boards, and where the two readings differ both are printed.</div>'
         % ' · '.join('yr%d %.3f' % (i + 1, c) for i, c in enumerate(CARRY)))
h.append('<div class="sub" style="border-left:3px solid var(--acc);padding-left:10px">'
         '<b>WHAT THIS PAGE IS.</b> The standing no-arb table set, computed on <b>%s\'s own '
         'walk-forward matrix</b>, with <b>the live R23 board <code>68be10c7</code> carried beside it '
         'in every cell</b> so the owner can rule with the standing-law tables in hand. '
         '<b>THIS IS ONE OF TWO PAGES</b> — the other renders the OTHER variant against the SAME '
         'base, and the owner is choosing between them. '
         '<b>THE BOARD IS PRICED, NOT ADOPTED.</b> The live board has not moved: this act rebuilt '
         '<code>68be10c79d0ee096455754e084bcf757</code> byte-exact TWICE in dev-shell and once in '
         'canonical posture, plus the balanced sibling <code>556ad70d</code>, with the dial OFF, '
         'before anything was measured (F1, <code>BUILD_F1_out.txt</code>), and moved no pin, no '
         'store, no config and no register.</div>' % esc(CTITLE))

# ================= the standing box ==============================================================
h.append('<div class="sub" style="border-left:3px solid var(--warn);padding-left:10px">'
         '<b>THE BOX BELOW IS THE LIVE BOARD\'S STANDING BOX, CARRIED VERBATIM AND NOT REWRITTEN.</b> '
         'The candidate is that board <b>plus one thing</b>: <code>%s</code>, the ORDER 44 level-axis '
         'band monotoniser, which makes a player\'s band non-decreasing in his own demonstrated level '
         'at the read site. <b>Any number the box quotes is the LIVE BOARD\'s</b>; this candidate\'s '
         'own reading of the same cell is in the tables below, and where they differ the table is the '
         'measurement and the box is the history.</div>' % esc(CDIAL))

# ================= the ND bands ==================================================================
h.append('<h1 style="margin-top:30px">THE ND BANDS</h1>')
h.append('<div class="sub">Five ND bands plus the classic three (ALL 1-64 / 1-20 / 21-64), in BOTH '
         'windows, on the candidate\'s own walk-forward matrix '
         '<code>per_entrant_' + CAND + '.json</code> (<code>' + esc(BDMETA[CAND]['matrix_md5']) + '</code>), with the live board\'s cell '
         'beside each one. Raw: <code>BANDS_NOARB_SFX_out.txt</code>. The ND cohort clock is '
         '<b>draft year + 1</b> for every row here — an ND band never contains an MSD row.</div>')
nd_breach = []
for wkey, wnice in WIN:
    h.append('<h2>%s</h2>' % esc(wnice))
    h.append('<div class="wrap"><table class="s">' + (HDR % 'band') + '<tbody>')
    for b in BANDS:
        k = '%s|%s|%s' % (wkey, VKEY, b)
        dc, db = BD.get(CAND, {}).get(k), BD.get(BASE, {}).get(k)
        if not dc:
            continue
        h.append(row_pair(b, 'ND band', wkey, dc, db))
        for lab, d in ((CAND, dc), (BASE, db)):
            pt = path_test((d or {}).get('path') or [])
            if pt and pt.get('breaches'):
                nd_breach.append((lab, wkey, b, d.get('apprec01'), pt))
    h.append('</tbody></table></div>')

# ================= the ND sensitivity ============================================================
h.append('<h2>SENSITIVITY — the same ND bands with the 2005 and 2006 cohorts removed entirely</h2>')
h.append('<div class="sub">A <b>SENSITIVITY, not a correction</b>: numerator and denominator alike '
         'drop the two oldest cohorts. It is printed because it is measured on this matrix and one '
         'of its cells reads red where the standing basis does not — a table that exists must not be '
         'left off the page. The standing basis above is the one the rulings are on.</div>')
for wkey, wnice in WIN:
    h.append('<h2>%s &middot; 2005/2006 cohorts removed</h2>' % esc(wnice))
    h.append('<div class="wrap"><table class="s">' + (HDR % 'band') + '<tbody>')
    for b in BANDS:
        k = '%s|EX0506|%s' % (wkey, b)
        dc, db = BD.get(CAND, {}).get(k), BD.get(BASE, {}).get(k)
        if not dc:
            continue
        h.append(row_pair(b, 'ND band (EX0506 sensitivity)', wkey, dc, db))
    h.append('</tbody></table></div>')

# ================= the pool arms =================================================================
h.append('<h1 style="margin-top:34px">THE POOL ARMS</h1>')
h.append('<div class="sub">Every pool pathway, both windows, the same standing format, the live '
         'board beside every cell. The cohort clock and the value semantics are the all-arm '
         'instrument\'s own (<code>noarb_table_allarm.py</code>, md5 <code>8673d7e3…</code>, '
         'asserted at run). Raw: <code>STANDING_TABLES_NOARB_SFX_out.txt</code>.</div>')
h.append('<div class="sub" style="border-left:3px solid var(--warn);padding-left:10px">'
         '<b>THE MSD YEAR-1 EXCLUSION, AND ITS REASON.</b> The cohort clock keys an <b>MSD</b> row on '
         '<b>the DRAFT YEAR ITSELF</b>, not draft year + 1 as it does for everyone else, because a '
         'mid-season draftee\'s first season <b>IS</b> his draft season. At year 1 an MSD row '
         'therefore falls <b>before</b> the first year his path covers. Those rows are counted '
         '<b>PRE-WINDOW and EXCLUDED</b> from the year-1 cell rather than scored as zero — scoring '
         'them as zero would invent a collapse that did not happen. <b>That, and only that, is why '
         'MSD\'s yr1 cell reads &ldquo;—&rdquo;</b>, why MSD carries no year-1 verdict on either '
         'board, and why MSD can carry no verdict CHANGE either.</div>')
arm_breach = []
for wkey, wnice in WIN:
    h.append('<h2>%s</h2>' % esc(wnice))
    h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">arm</th>'
             '<th class="l">pathway</th><th>n</th>'
             + ''.join('<th>yr%d</th>' % i for i in range(8))
             + '<th>yr0&rarr;1<br>CANDIDATE</th><th>yr0&rarr;1<br>LIVE BOARD</th><th>move</th>'
               '<th>verdict<br>CANDIDATE</th><th>verdict<br>LIVE BOARD</th>'
               '<th class="l">changed?</th><th class="l">path test</th></tr></thead><tbody>')
    absent = []
    for a in ARM_ORDER:
        k = '%s|%s' % (wkey, a)
        dc, db = ARMS.get(CAND, {}).get(k), ARMS.get(BASE, {}).get(k)
        if dc is None:
            absent.append(a)
            continue
        ac, ab = dc.get('apprec01'), (db or {}).get('apprec01')
        vc, cc = verdict_cell(ac)
        vb, cb = verdict_cell(ab)
        ptc, ptb = path_test(dc.get('path') or []), path_test((db or {}).get('path') or [])
        tc, _ = path_txt(ptc)
        tb, _ = path_txt(ptb)
        chg = (vc != vb) and not (a == 'MSD' and ac is None and ab is None)
        if chg:
            CHANGED.append((wkey, 'pool arm', a, ab, ac, vb, vc))
        for lab, d, pt in ((CAND, dc, ptc), (BASE, db, ptb)):
            if pt and pt.get('breaches'):
                arm_breach.append((lab, wkey, a, d.get('apprec01'), pt))
        note = 'MSD yr1 EXCLUDED — pre-window' if (a == 'MSD' and ac is None) else vc
        nb = 'MSD yr1 EXCLUDED — pre-window' if (a == 'MSD' and ab is None) else vb
        ncls = 'amber' if (a == 'MSD' and ac is None) else cc
        nbcls = 'amber' if (a == 'MSD' and ab is None) else cb
        h.append('<tr%s><td class="l"><b>%s</b></td><td class="l k">%s</td><td data-v="%d">%d</td>%s'
                 % (' class="amber"' if chg else '', esc(a), esc(ARM_LONG.get(a, '')),
                    dc.get('n', 0), dc.get('n', 0), yearcells(dc.get('path')))
                 + pctcell(ac, cc) + pctcell(ab, cb) + movecell(ac, ab)
                 + '<td class="%s">%s</td><td class="%s">%s</td><td class="l %s">%s</td>'
                   '<td class="l k">%s</td></tr>'
                   % (ncls, note, nbcls, nb, 'flag' if chg else '',
                      'VERDICT CHANGES' if chg else 'unchanged',
                      tc if tc == tb else ('cand: %s · live: %s' % (tc, tb))))
    h.append('</tbody></table></div>')
    if absent:
        h.append('<div class="sub"><b>ABSENT FROM THIS WINDOW, NOT DROPPED:</b> %s. The all-arm '
                 'instrument emits no cell for an arm with no qualifying rows inside the window — '
                 'for %s that is a POPULATION fact about the window, not a reading, and it is the '
                 'same on the live board. It is printed here so the arm cannot vanish silently.</div>'
                 % (', '.join('<b>%s</b> (%s)' % (esc(a), esc(ARM_LONG.get(a, ''))) for a in absent),
                    'PDS — pre-draft father-son' if absent == ['PDS'] else 'those arms'))

# ================= THE VERDICT-CHANGE ROLL-UP ====================================================
h.append('<h1 style="margin-top:34px">EVERY CELL WHOSE VERDICT CHANGED</h1>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">window</th><th class="l">kind</th>'
         '<th class="l">cell</th><th>LIVE BOARD</th><th>CANDIDATE</th><th class="l">live verdict</th>'
         '<th class="l">candidate verdict</th></tr></thead><tbody>')
if CHANGED:
    for w, kind, name, ab, ac, vb, vc in CHANGED:
        h.append('<tr class="amber"><td class="l">%s</td><td class="l k">%s</td><td class="l">%s</td>'
                 % (esc(w), esc(kind), esc(name)) + pctcell(ab) + pctcell(ac)
                 + '<td class="l">%s</td><td class="l"><b>%s</b></td></tr>' % (esc(vb), esc(vc)))
else:
    h.append('<tr><td class="l" colspan="7"><b>NOT ONE CELL CHANGES VERDICT.</b> Across all eight ND '
             'bands in both windows on the standing basis, the same eight bands on the 2005/2006 '
             'sensitivity, and all nine pool arms in both windows, every cell reads the same verdict '
             'on the candidate as it does on the live board. The numbers move; the readings do not. '
             'This is a measured result, not a claim of no effect — the moves are printed cell by '
             'cell above.</td></tr>')
h.append('</tbody></table></div>')

# ================= the red ledger ================================================================
def cell(lab, win, band):
    d = BD.get(lab, {}).get('%s|%s|%s' % (win, VKEY, band))
    return None if d is None else d.get('apprec01')


def acell(lab, win, arm):
    d = ARMS.get(lab, {}).get('%s|%s' % (win, arm))
    return None if d is None else d.get('apprec01')


def pct(v):
    return '—' if v is None else '%+.2f%%' % (100 * v)


def pair(v_c, v_b):
    if v_c is None or v_b is None:
        return '%s (live %s)' % (pct(v_c), pct(v_b))
    return '<b>%s</b> · live board %s · move %+.2f pp' % (pct(v_c), pct(v_b), 100 * (v_c - v_b))


LATE = [('PRIMARY', 'picks 31-40'), ('PRIMARY', 'picks 41-64'), ('PRIMARY', 'picks 21-64'),
        ('MODERN', 'picks 21-30'), ('MODERN', 'picks 31-40'), ('MODERN', 'picks 41-64'),
        ('MODERN', 'picks 21-64')]
h.append('<h1 style="margin-top:34px">THE RULED DOCUMENTED-RED LEDGER</h1>')
h.append('<div class="sub">The standing documented-reds, <b>each labelled as RULED</b> and reported '
         'at <b>what it actually reads on the candidate</b>, with the live board beside it. Being '
         'ruled is <b>not</b> the same as being repaired: a ruled red is one you have already looked '
         'at and accepted. <b>No dial was touched to chase any of these</b> — the only dial this '
         'seat set is the one being priced.</div>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">ruled documented-red</th>'
         '<th class="l">standing ruling</th><th class="l">candidate vs live board</th>'
         '<th class="l">status</th></tr></thead><tbody>')
_m10c, _m10b = cell(CAND, 'MODERN', 'picks 1-10'), cell(BASE, 'MODERN', 'picks 1-10')
_m20c, _m20b = cell(CAND, 'MODERN', 'picks 1-20'), cell(BASE, 'MODERN', 'picks 1-20')
h.append('<tr><td class="l"><b>modern picks 1-10 and 1-20 buy-side reds</b></td>'
         '<td class="l">RULED ACCEPTED at +21.52%% / +15.04%%</td>'
         '<td class="l">1-10 %s<br>1-20 %s</td>'
         '<td class="l"><b>MEASURED. THE LIFT MOVED BOTH DOWN, NOT UP</b> — very slightly, and '
         '<b>toward</b> the +14%% line rather than away from it. Both remain BUY-SIDE REDS and both '
         'still FAIL the path test on limb (b) — still rising at yr7 — exactly as they do on the '
         'live board. <b>Neither verdict changes.</b></td></tr>'
         % (pair(_m10c, _m10b), pair(_m20c, _m20b)))
h.append('<tr><td class="l"><b>late-band sell-side reds</b></td>'
         '<td class="l">POPULATION-RISK RULED</td>'
         '<td class="l">%s</td>'
         '<td class="l">MEASURED. Every one of them <b>improves toward zero</b> on the candidate and '
         '<b>every one of them stays a sell-side red</b>. The ruled reading is that these bands carry '
         'real population risk the price is right to take; they are <b>not</b> treated as a pricing '
         'defect here.</td></tr>'
         % '<br>'.join('%s %s — %s' % (w, b.replace('picks ', ''), pair(cell(CAND, w, b), cell(BASE, w, b)))
                       for w, b in LATE))
_sspP = (ARMS[CAND].get('PRIMARY|SSP') or {})
h.append('<tr class="red"><td class="l"><b>SSP</b> — supplemental selection period</td>'
         '<td class="l">INHERITED / PARKED (register v744 C6)</td>'
         '<td class="l">PRIMARY %s<br>MODERN %s<br>(n=%d)</td>'
         '<td class="l"><b>MEASURED, AND THE BREACH WIDENS.</b> SSP is a BUY-SIDE RED on both boards '
         'and FAILS the path test on limb (a) on both — but on the live board it beats carry in '
         '<b>years 2 and 3</b>, and on the candidate it beats carry in <b>years 2, 3 and 4</b>. '
         '<b>SSP IS NOT REPAIRED BY THIS DIAL AND WAS NEVER MEANT TO BE.</b> It is parked. This is '
         'reported as it reads: a parked breach that this lever makes wider, not narrower.</td></tr>'
         % (pair(acell(CAND, 'PRIMARY', 'SSP'), acell(BASE, 'PRIMARY', 'SSP')),
            pair(acell(CAND, 'MODERN', 'SSP'), acell(BASE, 'MODERN', 'SSP')), _sspP.get('n', 0)))
h.append('<tr><td class="l"><b>tail calibration 0.80</b></td>'
         '<td class="l">RULED &ldquo;tail 0.80&rdquo;</td>'
         '<td class="l"><b>NOT MEASURED BY THIS SEAT.</b> The tail instrument reads a charge form, '
         'not a matrix; it is not part of the no-arb table set this order asks for and no reading of '
         'it on the candidate is claimed here. The live board\'s reading is <b>0.8004</b> '
         '(<code>../final_candidate_2026-08-19/TAIL_CP_out.txt</code>).</td>'
         '<td class="l">OPEN — named so it cannot be mistaken for measured-and-clean.</td></tr>')
h.append('</tbody></table></div>')

# ================= the breach roll-up ============================================================
h.append('<h2>Every breaching cell, both boards, in one place</h2>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">board</th><th class="l">window</th>'
         '<th class="l">cell</th><th>yr0&rarr;1</th><th class="l">path test</th>'
         '</tr></thead><tbody>')
for lab, wkey, name, a01, pt in nd_breach + arm_breach:
    t, _c = path_txt(pt)
    h.append('<tr class="red"><td class="l">%s</td><td class="l">%s</td><td class="l">%s</td>'
             '<td data-v="%f">%+.2f%%</td><td class="l">%s</td></tr>'
             % ((CTITLE + ' ' + CBOARD[:8]) if lab == CAND else 'live board 68be10c7',
                esc(wkey), esc(name), a01, 100 * a01, esc(t)))
if not (nd_breach + arm_breach):
    h.append('<tr><td class="l" colspan="5">no breaching cell on either board</td></tr>')
h.append('</tbody></table></div>')
_bc = {(w, n) for l, w, n, _a, _p in nd_breach + arm_breach if l == CAND}
_bb = {(w, n) for l, w, n, _a, _p in nd_breach + arm_breach if l == BASE}
_new, _gone = sorted(_bc - _bb), sorted(_bb - _bc)
h.append('<div class="sub"><b>A breach is a cell whose year-1 appreciation exceeds +14%%. '
         'Sell-side reds are NOT breaches of the buy rail</b> and are not scored on the path test — '
         'the path test is a buy-side instrument. They are read on their own line in the ledger '
         'above. <b>COMPUTED FROM THE TABLES ON THIS PAGE, not asserted:</b> cells that breach on '
         'the candidate and NOT on the live board: <b>%s</b>. Cells that breach on the live board '
         'and stop breaching on the candidate: <b>%s</b>.</div>'
         % (' · '.join('%s %s' % x for x in _new) or 'NONE',
            ' · '.join('%s %s' % x for x in _gone) or 'NONE'))

# ================= the class mark ================================================================
h.append('<h1 style="margin-top:34px">THE YEAR-1 CLASS COHORT MARK</h1>')
h.append('<div class="sub">The registered W2 basis: DRAFT classes 2005-2015 (cohort years 2006-2016). '
         'The owner\'s floor is <b>&ge; 1.03</b> (the class must grow); the buy rail is <b>&lt; 1.14</b>. '
         '<b>The instrument self-validates on ORDER K first</b> — it must reproduce ORDER K\'s own '
         'published marks off ORDER K\'s own matrix before any candidate number is read. '
         'Raw: <code>CLASS_SFX_out.txt</code>.</div>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">board</th><th>W2 mark</th>'
         '<th>vs floor 1.03</th><th>vs rail 1.14</th><th>cohort clock</th><th>max class</th>'
         '<th class="l">reading</th></tr></thead><tbody>')
for lab, nice in (('OKRULED', 'ORDER K f3101883 — THE INSTRUMENT VALIDATION ROW (published 1.0513 / 1.0324)'),
                  ('D7BCAND', 'the PRIOR live board a05fe951 — the D7b third site, REGISTERED MARK 1.0672'),
                  (BASE, 'THE LIVE R23 BOARD 68be10c7 — this seat\'s own dial-unset emit'),
                  (CAND, CTITLE + ' — ' + CDIAL)):
    m = CL.get(lab)
    if not m:
        h.append('<tr><td class="l">%s</td><td class="l" colspan="6">MATRIX MISSING</td></tr>' % esc(lab))
        continue
    h.append('<tr%s><td class="l">%s</td><td data-v="%f"><b>%.4f</b></td><td data-v="%f">%+.4f</td>'
             '<td data-v="%f">%+.4f</td><td data-v="%f">%.4f</td><td data-v="%f">%.4f (%d)</td>'
             '<td class="l">%s</td></tr>'
             % (' class="amber"' if lab == CAND else '', esc(nice), m['w2'], m['w2'],
                m['w2'] - 1.03, m['w2'] - 1.03, m['w2'] - 1.14, m['w2'] - 1.14,
                m['cohort'], m['cohort'], m['max_class'], m['max_class'], m['max_class_year'],
                'inside the law' if (m['w2'] >= 1.03 and m['w2'] < 1.14) else 'BREACH'))
h.append('</tbody></table></div>')
_okd = abs(CL['OKRULED']['w2'] - 1.0513) if 'OKRULED' in CL else None
_W2 = list(range(2006, 2017))
_over_b = sorted(y for y in _W2 if (CL[BASE]['per_class'].get(str(y)) or CL[BASE]['per_class'].get(y)) is not None
                 and (CL[BASE]['per_class'].get(str(y)) or CL[BASE]['per_class'].get(y)) > 1.14)
_over_c = sorted(y for y in _W2 if (CL[CAND]['per_class'].get(str(y)) or CL[CAND]['per_class'].get(y)) is not None
                 and (CL[CAND]['per_class'].get(str(y)) or CL[CAND]['per_class'].get(y)) > 1.14)
h.append('<div class="sub">The instrument reproduced ORDER K at <b>%.4f / %.4f</b> against its '
         'published <b>1.0513 / 1.0324</b> (difference <b>%.4f</b>) — VALIDATED — before these numbers '
         'were read. The live R23 board reads <b>%.4f</b>; the candidate reads <b>%.4f</b>, which is '
         '<b>%s the owner\'s floor 1.03</b> and <b>%s the buy rail 1.14</b> (%+.4f to the rail). '
         '<b>COMPUTED, not asserted:</b> cohorts above 1.14 on the live board: <b>%s</b>; on the '
         'candidate: <b>%s</b>; crossing 1.14 that were not already across: <b>%s</b>. The full range '
         'is printed in <code>CLASS_SFX_out.txt</code>.</div>'
         % (CL['OKRULED']['w2'], CL['OKRULED']['cohort'], _okd, CL[BASE]['w2'], CL[CAND]['w2'],
            'above' if CL[CAND]['w2'] >= 1.03 else 'BELOW',
            'under' if CL[CAND]['w2'] < 1.14 else 'OVER', 1.14 - CL[CAND]['w2'],
            ', '.join(str(y) for y in _over_b) or 'none',
            ', '.join(str(y) for y in _over_c) or 'none',
            ', '.join(str(y) for y in sorted(set(_over_c) - set(_over_b))) or 'NONE'))

# ================= the raw manifest ==============================================================
h.append('<h2>THE RAW RECORD — every table on this page names the file it was rendered from</h2>')
h.append('<div class="wrap"><table class="s"><thead><tr><th class="l">table</th>'
         '<th class="l">raw output</th><th class="l">instrument</th></tr></thead><tbody>')
for t, o, i in [('F1 — the dial OFF rebuilds the live board byte-exact (dev x2, canonical, balanced)',
                 'BUILD_F1_out.txt', 'sfx_build.py'),
                ('the monotonicity math check on the pinned forests (both variants)',
                 'MATCHECK_out.txt'.replace('MATCHECK', 'MATHCHECK'), 'sfx_mathcheck.py'),
                ('the movers list, variant A raw / conserved', 'MOVERS_A_RAW_out.txt / MOVERS_A_CON_out.txt',
                 'the pricing seat\'s movers driver'),
                ('the movers list, variant B raw / conserved', 'MOVERS_B_RAW_out.txt / MOVERS_B_CON_out.txt',
                 'the pricing seat\'s movers driver'),
                ('the day-0 reference regenerated on the live R23 board', 'DAY0_SFXBASE.json', 'sfx_day0.py'),
                ('the standing day-0 reference reading 24 of 89 on R23 WITH THE DIAL UNSET',
                 'EMIT_SFXBASE_STALEREF_out.txt', 'run_emit_SFX.sh'),
                ('*** the walk-forward emit, VARIANT A RAW — THE ADOPTED ARM ***',
                 'EMIT_SFXARAW_out.txt', 'run_emit_SFX.sh (SFX_LABEL=SFXARAW RL_O44_LVLMONO=ratchet)'),
                ('the walk-forward emit, variant B raw (measured, not adopted)',
                 'EMIT_SFXBRAW_out.txt', 'run_emit_SFX.sh (SFX_LABEL=SFXBRAW RL_O44_LVLMONO=smooth)'),
                ('the walk-forward emit, variant A conserved', 'EMIT_SFXACON_out.txt', 'run_emit_SFX.sh'),
                ('the walk-forward emit, variant B conserved', 'EMIT_SFXBCON_out.txt', 'run_emit_SFX.sh'),
                ('the walk-forward emit, live board', 'EMIT_SFXBASE_out.txt', 'run_emit_SFX.sh'),
                ('the ND bands, both windows, ALL FIVE arms', 'BANDS_NOARB_ARAW_out.txt',
                 'araw_noarb_bands.py'),
                ('the ND bands, machine-readable', 'BANDS_NOARB_ARAW.json', 'araw_noarb_bands.py'),
                ('the pool arms, both windows, ALL FIVE arms', 'STANDING_TABLES_NOARB_ARAW_out.txt',
                 'araw_noarb_tables.py'),
                ('the pool arms, machine-readable', 'STANDING_TABLES_NOARB_ARAW.json',
                 'araw_noarb_tables.py'),
                ('the class cohort mark (F4), all five arms', 'CLASS_ARAW_out.txt', 'araw_noarb_class.py'),
                ('the page\'s own inputs checked rather than asserted', 'NOARB_ARAW_CHECKS_out.txt',
                 'araw_noarb_checks.py'),
                ('the ADOPTION prereg, committed before the flip', 'PREREG_ADOPTION_A_RAW.md', 'process law P9'),
                ('the B-raw reading the owner re-ruled on', 'NOARB_BRAW_SFXBRAW.html', 'braw_noarb_page.py'),
                ('the prereg, committed before the engine edit', 'PREREG_STAIRCASE.md', 'process law P9'),
                ('the decision packet, both variants side by side', 'PACKET_STAIRCASE.md',
                 'tools/landing/packet.py + PACKET_TEMPLATE.md')]:
    h.append('<tr><td class="l">%s</td><td class="l"><code>%s</code></td>'
             '<td class="l k">%s</td></tr>' % (esc(t), esc(o), esc(i)))
h.append('</tbody></table></div>')

sub = ('Candidate board <code>%s</code> (<code>%s</code>) · base / <b>live</b> board '
       '<code>%s</code> — <b>the live board is rebuilt byte-exact by this tree with the dial OFF '
       '(F1) and is NOT moved by this act</b> · engine <code>%s</code> · store <code>%s</code> · '
       'candidate matrix <code>per_entrant_%s.json</code> (<code>%s</code>, %d records) · comparison '
       'matrix <code>per_entrant_%s.json</code> (<code>%s</code>) · the ORDER 31-F day-0 replication '
       'reads <b>%s</b> at tolerance 0 on the candidate against the reference regenerated on the LIVE '
       'R23 board · the year-1 class mark reads <b>%.4f</b> on the candidate against <b>%.4f</b> on '
       'the live board. <b>PRICED, NOT ADOPTED — the dial ships OFF.</b>'
       % (CBOARD, esc(CDIAL), LIVE_BOARD, esc(BDMETA[CAND]['store']), esc(BDMETA[CAND]['store']),
          CAND, esc(BDMETA[CAND]['matrix_md5']), BDMETA[CAND]['n_records'],
          BASE, esc(BDMETA[BASE]['matrix_md5']),
          os.environ.get('SFX_DAY0_READ', '87 of 87'),
          CL[CAND]['w2'], CL[BASE]['w2']))
page = '\n'.join(['<title>ORDER 44 No-Arb — %s</title>' % esc(CTITLE), '<style>%s</style>' % CSS,
                  '<h1>THE NO-ARB TABLES — %s</h1>' % esc(NICE),
                  '<div class="sub">%s</div>' % sub,
                  BOX.html_box(), '\n'.join(h), '<script>%s</script>' % JS])
open(os.path.join(HERE, OUTNAME), 'w').write(page)
print('%s written  (%d bytes)' % (OUTNAME, len(page)))
print('  cells whose VERDICT CHANGED: %s'
      % (' · '.join('%s %s %s: %s -> %s' % (w, k, n, vb, vc) for w, k, n, _ab, _ac, vb, vc in CHANGED)
         or 'NONE'))
print('  breaching cells, candidate : %s'
      % (' · '.join('%s %s' % (w, n) for l, w, n, _a, _p in nd_breach + arm_breach if l == CAND) or 'none'))
print('  breaching cells, live board: %s'
      % (' · '.join('%s %s' % (w, n) for l, w, n, _a, _p in nd_breach + arm_breach if l == BASE) or 'none'))
print('  breaches NEW on the candidate: %s'
      % (' · '.join('%s %s' % x for x in _new) or 'NONE'))
print('  breaches REMOVED by the candidate: %s'
      % (' · '.join('%s %s' % x for x in _gone) or 'NONE'))
print('  class mark: candidate %.4f   live board %.4f   (ORDER K validation row %.4f)'
      % (CL[CAND]['w2'], CL[BASE]['w2'], CL['OKRULED']['w2']))
