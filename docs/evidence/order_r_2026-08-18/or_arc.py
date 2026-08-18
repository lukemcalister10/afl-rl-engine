#!/usr/bin/env python3
"""ORDER R — THE WHOLE-ARC MOVERS LIST. Who the pedigree-conditional mechanism hurt, who it helped,
and by how much, across the entire arc rather than the last step only.

    ORDER K f3101883  ->  ORDER P 374d4e44  ->  the ORDER R variants
    (the last board       (where the           (the softening the owner
     BEFORE this           pedigree-conditional  ruled: the cap at p15/p20
     mechanism path        charge is             and the slope lowered inside
     began; it carries     introduced)           its published CI)
     the OLD blind
     games-only eta charge)

Emits three files:
  ARC_R.csv    one row per active player, machine readable
  ARC_R.json   the same, plus the summary block
  ARC_R.html   the readable page, sorted by the whole-arc absolute delta

THE PRESENTATION POINT THIS FILE IS BUILT AROUND. The board TOTALS differ between these boards.
ORDER K is 673,097 and ORDER P is 666,434. So most rows fall in absolute points for a reason that
has NOTHING to do with any individual player: there are simply fewer points on the board. RANK is
the fair comparison across boards. Absolute points are not. That is printed at the top of every
output and it is not buried.

NO NAMED-PLAYER TARGETS. This is a report. No row's value is an acceptance criterion.
NULLS AS NULLS: a row that cannot be scored on a board prints WHY, and is never dropped or zeroed.
"""
import csv, html, json, math, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

# ---- the boards ---------------------------------------------------------------------------------
# label -> (path, human name). ORDER matters: it is the column order everywhere.
BOARDS = [
    ('LIVE',   SP + '/o25/board_LANDED.json',                    'LIVE 88ce647f — never touched, reference only'),
    ('K',      SP + '/or/bb_KrefR/rl_after/rl_app_data.json',    'ORDER K f3101883 — the last board BEFORE this mechanism path'),
    ('P',      SP + '/or/bb_Roff/rl_after/rl_app_data.json',     'ORDER P 374d4e44 — the pedigree-conditional charge introduced'),
    ('RB1',    SP + '/or/bb_RB1/rl_after/rl_app_data.json',      'FIX B1   p5  b0     A off — ORDER Q, settled; the ORDER R base'),
    ('RAB1',   SP + '/or/bb_RAB1/rl_after/rl_app_data.json',     'FIX A+B1 p5  b0     A ON  — ORDER Q'),
    ('R15',    SP + '/or/bb_R15/rl_after/rl_app_data.json',      'ORDER R  p15 b0     A off'),
    ('R20',    SP + '/or/bb_R20/rl_after/rl_app_data.json',      'ORDER R  p20 b0     A off'),
    ('R15A',   SP + '/or/bb_R15A/rl_after/rl_app_data.json',     'ORDER R  p15 b0     A ON'),
    ('R20A',   SP + '/or/bb_R20A/rl_after/rl_app_data.json',     'ORDER R  p20 b0     A ON'),
    ('Rb1',    SP + '/or/bb_Rb1/rl_after/rl_app_data.json',      'ORDER R  p5  0.111  A off'),
    ('Rb2',    SP + '/or/bb_Rb2/rl_after/rl_app_data.json',      'ORDER R  p5  0.105  A off'),
    ('R15b1',  SP + '/or/bb_R15b1/rl_after/rl_app_data.json',    'ORDER R  p15 0.111  A off'),
    ('R20b2',  SP + '/or/bb_R20b2/rl_after/rl_app_data.json',    'ORDER R  p20 0.105  A off — SOFTEST'),
    ('R20b2A', SP + '/or/bb_R20b2A/rl_after/rl_app_data.json',   'ORDER R  p20 0.105  A ON  — softest + FIX A'),
]
BOARDS = [(l, p, n) for l, p, n in BOARDS if os.path.exists(p)]
LAB = [l for l, _, _ in BOARDS]
NICE = {l: n for l, _, n in BOARDS}
MD5 = {l: hashlib.md5(open(p, 'rb').read()).hexdigest() for l, p, _ in BOARDS}
RAW = {l: json.load(open(p)) for l, p, _ in BOARDS}
ROWS = {l: {r['key']: r for r in RAW[l]['active']} for l in LAB}
V = {l: {k: r.get('v') for k, r in ROWS[l].items()} for l in LAB}
TOT = {l: sum(v for v in V[l].values() if v is not None) for l in LAB}

# THE SPANNING VARIANT. It is the FAR CORNER of the grid — both levers at their softest, with FIX A.
# IT IS NOT A RECOMMENDATION. THIS SEAT RECOMMENDS NOTHING. It is the cell that spans the whole arc,
# chosen because it is the extreme of the two levers the owner named, not because it is preferred.
SPAN = 'R20b2A' if 'R20b2A' in LAB else ('R20b2' if 'R20b2' in LAB else 'RB1')

# ---- the mechanism diagnostics, from the engine-measured censuses ---------------------------------
# CENSUS_<tag>.json carries, per row, the charge factor the engine ACTUALLY applied at the blend site
# (M3-reassembled), plus the pedigree premium and the two surpluses. Read, never recomputed here.
CTAG = {'K': 'RK', 'P': 'RP', 'RB1': 'RB1', 'RAB1': 'RAB1', 'R15': 'R15', 'R20': 'R20',
        'R15A': 'R15A', 'R20A': 'R20A', 'Rb1': 'Rb1', 'Rb2': 'Rb2', 'R15b1': 'R15b1',
        'R20b2': 'R20b2', 'R20b2A': 'R20b2A'}
CH = {}
MISSING_CENSUS = []
for l in LAB:
    t = CTAG.get(l)
    f = os.path.join(HERE, 'CENSUS_%s.json' % t) if t else None
    if f and os.path.exists(f):
        CH[l] = {c['key']: c for c in json.load(open(f))['charge']}
    else:
        MISSING_CENSUS.append(l)

BASE = 'P' if 'P' in LAB else LAB[0]
KEYS = sorted(ROWS[BASE])
REF = ROWS[BASE]


def cohort_of(r):
    """The engine's own cohort clock, op_class.py:41-43: draft year + 1, EXCEPT MSD where it is the
    draft year itself. Returned as a null, never as a zero, when the row carries no draft year."""
    y = r.get('yr')
    if y is None:
        return None
    return int(y) if r.get('ty') == 'MSD' else int(y) + 1


def band_of(r):
    if r.get('ty') != 'ND' or not r.get('pk'):
        return 'pool'
    p = int(r['pk'])
    return '1-10' if p <= 10 else '11-20' if p <= 20 else '21-30' if p <= 30 else '31-40' if p <= 40 else '41+'


RANK = {}
for l in LAB:
    order = sorted([k for k in V[l] if V[l][k] is not None], key=lambda k: (-V[l][k], k))
    RANK[l] = {k: i + 1 for i, k in enumerate(order)}


def pct(a, b):
    """a against b, as a percent. None when b is zero or either side is missing — a NULL, not a 0."""
    if a is None or b is None or b == 0:
        return None
    return 100.0 * (a - b) / abs(b)


REC = []
for k in KEYS:
    r = REF[k]
    d = dict(key=k, player=r.get('name') or k, cohort=cohort_of(r), pos=r.get('grp'),
             pathway=r.get('ty'), pick=r.get('pk'), age=r.get('age'), games=r.get('g'),
             band=band_of(r), draft_year=r.get('yr'))
    ch = (CH.get('P') or {}).get(k)
    d['v0'] = ch.get('v0') if ch else None
    d['pg'] = ch.get('pg') if ch else None
    d['s_age'] = ch.get('s_age') if ch else None
    d['s_ped'] = ch.get('s_ped') if ch else None
    d['note'] = ''
    for l in LAB:
        d['v_' + l] = V[l].get(k)
        d['rank_' + l] = RANK[l].get(k)
        c = (CH.get(l) or {}).get(k)
        d['charge_' + l] = (1.0 - c['f']) if (c and c.get('f') is not None) else None
    if d.get('v_K') is None:
        d['note'] = 'not present on the ORDER K board — the K columns are NULL, never zero'
    if d.get('v_LIVE') is None and 'LIVE' in LAB:
        d['note'] = (d['note'] + '; ' if d['note'] else '') + 'not present on the live board 88ce647f'
    for step, a, b in (('PK', 'P', 'K'), ('SPAN_P', SPAN, 'P'), ('ARC', SPAN, 'K')):
        va, vb = d.get('v_' + a), d.get('v_' + b)
        d['d_' + step] = (va - vb) if (va is not None and vb is not None) else None
        d['dpct_' + step] = pct(va, vb)
        ra, rb = d.get('rank_' + a), d.get('rank_' + b)
        # rank change: POSITIVE means the row moved UP the board (a smaller rank number).
        d['drank_' + step] = (rb - ra) if (ra is not None and rb is not None) else None
    REC.append(d)

# ---- the summary --------------------------------------------------------------------------------
STEPS = [('PK', 'ORDER K -> ORDER P (the mechanism introduced)'),
         ('SPAN_P', 'ORDER P -> %s (the softening)' % SPAN),
         ('ARC', 'ORDER K -> %s (THE WHOLE ARC)' % SPAN)]
SUM = dict(totals=TOT, md5=MD5, nice=NICE, span=SPAN, labels=LAB,
           missing_census=MISSING_CENSUS, n=len(REC), steps={})
for s, nm in STEPS:
    up = [r for r in REC if r['d_' + s] is not None and r['d_' + s] > 0]
    dn = [r for r in REC if r['d_' + s] is not None and r['d_' + s] < 0]
    fl = [r for r in REC if r['d_' + s] == 0]
    nul = [r for r in REC if r['d_' + s] is None]
    e = dict(name=nm, up=len(up), down=len(dn), flat=len(fl), null=len(nul),
             net=sum(r['d_' + s] for r in REC if r['d_' + s] is not None),
             rank_up=sum(1 for r in REC if (r['drank_' + s] or 0) > 0),
             rank_down=sum(1 for r in REC if (r['drank_' + s] or 0) < 0),
             rank_flat=sum(1 for r in REC if r['drank_' + s] == 0))
    e['by_band'] = {}
    for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
        sub = [r for r in REC if r['band'] == b]
        e['by_band'][b] = dict(n=len(sub),
                               up=sum(1 for r in sub if (r['d_' + s] or 0) > 0),
                               down=sum(1 for r in sub if (r['d_' + s] or 0) < 0),
                               net=sum(r['d_' + s] for r in sub if r['d_' + s] is not None),
                               rank_up=sum(1 for r in sub if (r['drank_' + s] or 0) > 0),
                               rank_down=sum(1 for r in sub if (r['drank_' + s] or 0) < 0))
    e['by_cohort'] = {}
    for c in sorted(set(r['cohort'] for r in REC if r['cohort'] is not None)):
        sub = [r for r in REC if r['cohort'] == c]
        e['by_cohort'][c] = dict(n=len(sub),
                                 up=sum(1 for r in sub if (r['d_' + s] or 0) > 0),
                                 down=sum(1 for r in sub if (r['d_' + s] or 0) < 0),
                                 net=sum(r['d_' + s] for r in sub if r['d_' + s] is not None),
                                 rank_up=sum(1 for r in sub if (r['drank_' + s] or 0) > 0),
                                 rank_down=sum(1 for r in sub if (r['drank_' + s] or 0) < 0))
    nc = sum(1 for r in REC if r['cohort'] is None)
    if nc:
        e['by_cohort']['no draft year — a NULL, reported as one'] = dict(n=nc, up=None, down=None,
                                                                         net=None, rank_up=None,
                                                                         rank_down=None)
    ordered = sorted([r for r in REC if r['d_' + s] is not None], key=lambda r: -r['d_' + s])
    e['top_up'] = [dict(player=r['player'], pick=r['pick'], band=r['band'], age=r['age'],
                        d=r['d_' + s], dpct=r['dpct_' + s], drank=r['drank_' + s])
                   for r in ordered[:10] if r['d_' + s] > 0]
    e['top_down'] = [dict(player=r['player'], pick=r['pick'], band=r['band'], age=r['age'],
                          d=r['d_' + s], dpct=r['dpct_' + s], drank=r['drank_' + s])
                     for r in ordered[::-1][:10] if r['d_' + s] < 0]
    SUM['steps'][s] = e

# ---- CSV ------------------------------------------------------------------------------------------
COLS = (['key', 'player', 'cohort', 'draft_year', 'pos', 'pathway', 'pick', 'band', 'age', 'games', 'v0',
         'pg', 's_age', 's_ped']
        + ['v_' + l for l in LAB] + ['rank_' + l for l in LAB] + ['charge_' + l for l in LAB]
        + ['d_PK', 'dpct_PK', 'drank_PK', 'd_SPAN_P', 'dpct_SPAN_P', 'drank_SPAN_P',
           'd_ARC', 'dpct_ARC', 'drank_ARC', 'note'])
REC.sort(key=lambda r: -abs(r['d_ARC'] or 0))
with open(os.path.join(HERE, 'ARC_R.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=COLS, extrasaction='ignore')
    w.writeheader()
    for r in REC:
        w.writerow({c: ('' if r.get(c) is None else r.get(c)) for c in COLS})
json.dump(dict(summary=SUM, columns=COLS, rows=REC),
          open(os.path.join(HERE, 'ARC_R.json'), 'w'), indent=1, default=str)


# ---- HTML -----------------------------------------------------------------------------------------
def f0(x):
    return '' if x is None else '%d' % round(x)


def f2(x):
    return '' if x is None else '%.2f' % x


def fp(x):
    return '' if x is None else '%+.1f%%' % x


def fs(x):
    return '' if x is None else '%+d' % round(x)


def fc(x):
    return '' if x is None else '%.1f%%' % (100.0 * x)


H = []
A = H.append
A('<title>Whole-Arc Movers</title>')
A('<style>')
A('''
:root{--bg:#fbfaf8;--fg:#1a1a1a;--mut:#6b6560;--line:#e2ddd6;--card:#ffffff;
      --up:#1f6f43;--upbg:#e8f4ec;--dn:#9b2c2c;--dnbg:#fbeaea;--acc:#2f5d8f;--warnbg:#fdf4e3;--warn:#8a6014;}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
      --bg:#16151a;--fg:#eceaf0;--mut:#9a95a3;--line:#2f2d36;--card:#1e1d24;
      --up:#63c68e;--upbg:#17301f;--dn:#e28585;--dnbg:#331a1a;--acc:#8fb6e5;--warnbg:#2e2510;--warn:#e2b661;}}
:root[data-theme="dark"]{--bg:#16151a;--fg:#eceaf0;--mut:#9a95a3;--line:#2f2d36;--card:#1e1d24;
      --up:#63c68e;--upbg:#17301f;--dn:#e28585;--dnbg:#331a1a;--acc:#8fb6e5;--warnbg:#2e2510;--warn:#e2b661;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);margin:0;padding:2rem 1.25rem 5rem;
     font:15px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
.wrap{max-width:1500px;margin:0 auto}
h1{font-size:1.85rem;line-height:1.2;margin:0 0 .4rem;letter-spacing:-.02em}
h2{font-size:1.15rem;margin:2.4rem 0 .7rem;letter-spacing:-.01em;
   border-bottom:1px solid var(--line);padding-bottom:.35rem}
h3{font-size:.98rem;margin:1.4rem 0 .5rem;color:var(--mut);font-weight:600}
p{margin:.5rem 0;max-width:78ch}
.sub{color:var(--mut);margin:0 0 1.4rem}
.warn{background:var(--warnbg);border:1px solid var(--warn);border-left-width:4px;
      border-radius:6px;padding:.9rem 1.1rem;margin:1.2rem 0}
.warn b{color:var(--warn)}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.9rem 1.1rem;margin:1rem 0}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);
        border-radius:8px;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:13px;font-variant-numeric:tabular-nums}
th,td{padding:.34rem .5rem;text-align:right;white-space:nowrap;border-bottom:1px solid var(--line)}
th{position:sticky;top:0;background:var(--card);text-align:right;font-weight:600;
   font-size:11.5px;letter-spacing:.02em;color:var(--mut);text-transform:uppercase;z-index:2}
td.l,th.l{text-align:left}
tbody tr:hover{background:color-mix(in srgb,var(--acc) 7%,transparent)}
.up{color:var(--up);font-weight:600}
.dn{color:var(--dn);font-weight:600}
.mut{color:var(--mut)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.8rem;margin:1rem 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.75rem .9rem}
.stat .k{font-size:11.5px;text-transform:uppercase;letter-spacing:.03em;color:var(--mut)}
.stat .v{font-size:1.45rem;font-weight:650;letter-spacing:-.02em;margin-top:.15rem}
code{font:12.5px ui-monospace,SFMono-Regular,Menlo,monospace;background:color-mix(in srgb,var(--acc) 10%,transparent);
     padding:.08em .35em;border-radius:3px}
''')
A('</style>')
A('<div class="wrap">')
A('<h1>The whole-arc movers list</h1>')
A('<p class="sub">ORDER K <code>f3101883</code> &rarr; ORDER P <code>374d4e44</code> &rarr; the ORDER R variants. '
  'One row per active player, all %d. <b>Nothing here is adopted and nothing lands.</b></p>' % len(REC))

A('<div class="warn"><b>READ RANK, NOT POINTS.</b><p>The board totals are different numbers. '
  'ORDER K totals <b>%s</b> and ORDER P totals <b>%s</b> &mdash; %s points fewer on the same %d players. '
  'So most rows fall in absolute points for a reason that has nothing to do with any individual player: '
  'there are simply fewer points on the board to go round. <b>RANK is the fair comparison across these '
  'boards. Absolute points are not.</b> Both are printed, and the rank-change columns are the ones to '
  'read when comparing one board with another.</p></div>'
  % ('{:,}'.format(TOT.get('K', 0)), '{:,}'.format(TOT.get('P', 0)),
     '{:,}'.format(TOT.get('K', 0) - TOT.get('P', 0)), len(REC)))

A('<div class="warn"><b>THE SPANNING VARIANT IS NOT A RECOMMENDATION.</b><p>The "softening" and '
  '"whole arc" columns use <code>%s</code> &mdash; %s. It is the FAR CORNER of the grid: both levers at '
  'their softest. It was chosen because it spans the arc, not because this seat prefers it. '
  '<b>This seat recommends nothing.</b> Every other variant has its own value and rank columns in the '
  'table below and in <code>ARC_R.csv</code>.</p></div>' % (SPAN, html.escape(NICE.get(SPAN, SPAN))))

A('<h2>The boards</h2>')
A('<div class="scroll"><table><thead><tr><th class="l">board</th><th class="l">md5</th>'
  '<th>total</th><th>vs ORDER K</th><th>vs ORDER P</th><th class="l">what it is</th></tr></thead><tbody>')
for l in LAB:
    A('<tr><td class="l"><b>%s</b></td><td class="l mut"><code>%s</code></td><td>%s</td>'
      '<td class="%s">%s</td><td class="%s">%s</td><td class="l mut">%s</td></tr>'
      % (l, MD5[l][:8], '{:,}'.format(TOT[l]),
         'up' if TOT[l] > TOT.get('K', 0) else 'dn', '{:+,}'.format(TOT[l] - TOT.get('K', 0)),
         'up' if TOT[l] > TOT.get('P', 0) else 'dn', '{:+,}'.format(TOT[l] - TOT.get('P', 0)),
         html.escape(NICE[l])))
A('</tbody></table></div>')
if MISSING_CENSUS:
    A('<p class="mut">Charge columns are absent for: %s &mdash; the engine-measured census for those '
      'boards is not on disk. Reported as absent, never as zero.</p>' % ', '.join(MISSING_CENSUS))

A('<h2>Summary</h2>')
for s, nm in STEPS:
    e = SUM['steps'][s]
    A('<h3>%s</h3>' % html.escape(nm))
    A('<div class="grid">')
    for kk, vv, cls in (('rows that ROSE in points', e['up'], 'up'),
                        ('rows that FELL in points', e['down'], 'dn'),
                        ('rows unchanged', e['flat'], 'mut'),
                        ('net points', '{:+,}'.format(e['net']), 'up' if e['net'] > 0 else 'dn'),
                        ('rows that ROSE in RANK', e['rank_up'], 'up'),
                        ('rows that FELL in RANK', e['rank_down'], 'dn')):
        A('<div class="stat"><div class="k">%s</div><div class="v %s">%s</div></div>' % (kk, cls, vv))
    A('</div>')
    if e['null']:
        A('<p class="mut">%d rows could not be scored on both sides of this step and are counted as '
          'NULLS, never as zeros. The reason is in each row\'s note column.</p>' % e['null'])
    A('<div class="scroll"><table><thead><tr><th class="l">pick band</th><th>n</th><th>pts up</th>'
      '<th>pts down</th><th>net pts</th><th>rank up</th><th>rank down</th></tr></thead><tbody>')
    for b, d in e['by_band'].items():
        A('<tr><td class="l">%s</td><td>%d</td><td class="up">%d</td><td class="dn">%d</td>'
          '<td class="%s">%s</td><td class="up">%d</td><td class="dn">%d</td></tr>'
          % (b, d['n'], d['up'], d['down'], 'up' if d['net'] > 0 else 'dn',
             '{:+,}'.format(d['net']), d['rank_up'], d['rank_down']))
    A('</tbody></table></div>')
    A('<div class="scroll"><table><thead><tr><th class="l">cohort</th><th>n</th><th>pts up</th>'
      '<th>pts down</th><th>net pts</th><th>rank up</th><th>rank down</th></tr></thead><tbody>')
    for c, d in e['by_cohort'].items():
        if d['up'] is None:
            A('<tr><td class="l mut">%s</td><td>%d</td><td colspan="5" class="l mut">not scored</td></tr>'
              % (html.escape(str(c)), d['n']))
            continue
        A('<tr><td class="l">%s</td><td>%d</td><td class="up">%d</td><td class="dn">%d</td>'
          '<td class="%s">%s</td><td class="up">%d</td><td class="dn">%d</td></tr>'
          % (c, d['n'], d['up'], d['down'], 'up' if d['net'] > 0 else 'dn',
             '{:+,}'.format(d['net']), d['rank_up'], d['rank_down']))
    A('</tbody></table></div>')
    for lab2, key in (('Ten largest movers UP', 'top_up'), ('Ten largest movers DOWN', 'top_down')):
        A('<h3>%s &mdash; %s</h3>' % (lab2, html.escape(nm)))
        if not e[key]:
            A('<p class="mut">(none &mdash; a null, reported as one)</p>')
            continue
        A('<div class="scroll"><table><thead><tr><th class="l">player</th><th>pick</th>'
          '<th class="l">band</th><th>age</th><th>points</th><th>percent</th><th>rank change</th>'
          '</tr></thead><tbody>')
        for r in e[key]:
            A('<tr><td class="l">%s</td><td>%s</td><td class="l">%s</td><td>%s</td>'
              '<td class="%s">%s</td><td class="%s">%s</td><td class="%s">%s</td></tr>'
              % (html.escape(str(r['player'])), r['pick'] if r['pick'] else 'pool', r['band'],
                 r['age'] if r['age'] is not None else '',
                 'up' if r['d'] > 0 else 'dn', fs(r['d']),
                 'up' if r['d'] > 0 else 'dn', fp(r['dpct']),
                 'up' if (r['drank'] or 0) > 0 else 'dn', fs(r['drank'])))
        A('</tbody></table></div>')

A('<h2>Every row, sorted by the whole-arc absolute move</h2>')
A('<p>Sorted by the size of <b>%s minus ORDER K</b>, largest first, so the biggest movers in both '
  'directions are at the top. Rank 1 is the most valuable row of the %d. A POSITIVE rank change means '
  'the row moved UP the board.</p>' % (SPAN, len(REC)))
A('<p class="mut">Mechanism diagnostics: <b>pg</b> is the pedigree premium PG(ln v0, class) in points '
  'a game; <b>s(age)</b> is production against the S1 age bar alone; <b>s(ped)</b> is production '
  'against the age bar PLUS the premium, which is what the charge actually reads. By construction '
  's(ped) = s(age) &minus; pg. <b>chg</b> columns are the share of the pedigree leg removed.</p>')
A('<div class="scroll"><table><thead><tr>')
head = (['player', 'coh', 'pos', 'path', 'pick', 'age', 'g', 'v0', 'pg', 's(age)', 's(ped)']
        + ['%s' % l for l in LAB] + ['#%s' % l for l in LAB]
        + ['chg %s' % l for l in LAB if l in CH]
        + ['P&minus;K', '%', '&Delta;#', '%s&minus;P' % SPAN, '%', '&Delta;#',
           'ARC', '%', '&Delta;#', 'note'])
for i, h in enumerate(head):
    A('<th class="%s">%s</th>' % ('l' if i in (0, 2, 3) or h == 'note' else '', h))
A('</tr></thead><tbody>')
for r in REC:
    c = []
    c.append('<td class="l">%s</td>' % html.escape(str(r['player'])))
    c.append('<td>%s</td>' % (r['cohort'] if r['cohort'] is not None else '<span class="mut">null</span>'))
    c.append('<td class="l">%s</td>' % (r['pos'] or ''))
    c.append('<td class="l">%s</td>' % (r['pathway'] or ''))
    c.append('<td>%s</td>' % (r['pick'] if r['pick'] else ''))
    c.append('<td>%s</td>' % (r['age'] if r['age'] is not None else ''))
    c.append('<td>%s</td>' % f0(r['games']))
    c.append('<td>%s</td>' % f0(r['v0']))
    c.append('<td>%s</td>' % f2(r['pg']))
    c.append('<td>%s</td>' % f2(r['s_age']))
    c.append('<td>%s</td>' % f2(r['s_ped']))
    for l in LAB:
        c.append('<td>%s</td>' % f0(r.get('v_' + l)))
    for l in LAB:
        c.append('<td class="mut">%s</td>' % f0(r.get('rank_' + l)))
    for l in LAB:
        if l in CH:
            c.append('<td>%s</td>' % fc(r.get('charge_' + l)))
    for s, _ in STEPS:
        d = r['d_' + s]
        cls = 'up' if (d or 0) > 0 else ('dn' if (d or 0) < 0 else 'mut')
        c.append('<td class="%s">%s</td>' % (cls, fs(d)))
        c.append('<td class="%s">%s</td>' % (cls, fp(r['dpct_' + s])))
        dr = r['drank_' + s]
        c.append('<td class="%s">%s</td>' % ('up' if (dr or 0) > 0 else ('dn' if (dr or 0) < 0 else 'mut'), fs(dr)))
    c.append('<td class="l mut">%s</td>' % html.escape(r['note']))
    A('<tr>' + ''.join(c) + '</tr>')
A('</tbody></table></div>')
A('<h2>What this page is not</h2>')
A('<p>It is a report. <b>No player\'s value is an acceptance criterion</b> and not one constant in '
  'ORDER R was chosen with any row in view. That is a standing prohibition in this project after a '
  'real error. Nothing on this page is adopted, nothing lands, and no variant is recommended.</p>')
A('</div>')
open(os.path.join(HERE, 'ARC_R.html'), 'w').write('\n'.join(H) + '\n')
print('wrote ARC_R.csv, ARC_R.json, ARC_R.html   (%d rows, %d boards, spanning variant %s)'
      % (len(REC), len(LAB), SPAN))
for s, nm in STEPS:
    e = SUM['steps'][s]
    print('  %-52s up %3d  down %3d  flat %3d  null %2d  net %+8d'
          % (nm, e['up'], e['down'], e['flat'], e['null'], e['net']))
