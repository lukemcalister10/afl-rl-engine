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
# ORDER K's charge is NOT read from its own census run. It is read from the f_K field the leg
# recorder captures on EVERY board: that field IS ORDER K's blind games-only eta charge, computed by
# the engine at the same call site in the same clock state. Reading it off the ORDER P census gives
# the identical object and saves a thirteenth engine load. The choice is declared, not hidden.
CTAG = {'P': 'RP', 'RB1': 'RB1', 'RAB1': 'RAB1', 'R15': 'R15', 'R20': 'R20',
        'R15A': 'R15A', 'R20A': 'R20A', 'Rb1': 'Rb1', 'Rb2': 'Rb2', 'R15b1': 'R15b1',
        'R20b2': 'R20b2', 'R20b2A': 'R20b2A'}
CH = {}
MISSING_CENSUS = []
for l in LAB:
    t = CTAG.get(l)
    f = os.path.join(HERE, 'CENSUS_%s.json' % t) if t else None
    if f and os.path.exists(f):
        CH[l] = {c['key']: c for c in json.load(open(f))['charge']}
    elif l != 'K':
        MISSING_CENSUS.append(l)
if 'P' in CH:
    CH['K'] = {k: dict(c, f=c.get('f_K')) for k, c in CH['P'].items() if c.get('f_K') is not None}
else:
    MISSING_CENSUS.append('K')

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
    return '' if x is None else '{:,}'.format(int(round(x)))


def f2(x):
    return '' if x is None else '%.2f' % x


def fp(x):
    return '' if x is None else '%+.1f%%' % x


def fs(x):
    return '' if x is None else '{:+,}'.format(int(round(x)))


def fc(x):
    return '' if x is None else '%.1f%%' % (100.0 * x)


def cls_of(x):
    return 'pos' if (x or 0) > 0 else ('neg' if (x or 0) < 0 else 'nil')


def bar(v, mx, klass):
    """A magnitude bar behind a number: size in FORM as well as in digits."""
    if not v or not mx:
        return ''
    return '<span class="bar %s" style="width:%.1f%%"></span>' % (klass, min(100.0, 100.0 * abs(v) / mx))


CSS = """
/* ORDER R — whole-arc movers. Cool-slate ledger palette; slab display over a humanist body face.
   Light is the bare :root. Dark redefines TOKENS ONLY, in both the un-stamped and the stamped state,
   so the page resolves as a set whichever of the three theme states the viewer is in. */
:root{
  --ground:#F6F7FA; --surface:#FFFFFF; --raise:#EDF0F5;
  --ink:#14181F; --body:#2C333F; --muted:#5D6675; --faint:#8A93A3;
  --line:#DCE1E9; --line-strong:#C3CAD6;
  --accent:#2E4A7D; --accent-soft:#E7ECF6;
  --pos:#1B6B4A; --pos-soft:#E2F0E9; --neg:#9E3436; --neg-soft:#F7E6E6;
  --flag:#8A5A12; --flag-soft:#FBF1DF; --flag-line:#D9B472;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0E1218; --surface:#161B23; --raise:#1D242E;
    --ink:#E9EDF3; --body:#C7CEDA; --muted:#8C97A8; --faint:#6B7686;
    --line:#262D38; --line-strong:#39424F;
    --accent:#8CAEE4; --accent-soft:#1B2536;
    --pos:#57BC8D; --pos-soft:#12291F; --neg:#E08183; --neg-soft:#2C1719;
    --flag:#E0B166; --flag-soft:#2A2110; --flag-line:#6B5423;
  }
}
:root[data-theme="dark"]{
  --ground:#0E1218; --surface:#161B23; --raise:#1D242E;
  --ink:#E9EDF3; --body:#C7CEDA; --muted:#8C97A8; --faint:#6B7686;
  --line:#262D38; --line-strong:#39424F;
  --accent:#8CAEE4; --accent-soft:#1B2536;
  --pos:#57BC8D; --pos-soft:#12291F; --neg:#E08183; --neg-soft:#2C1719;
  --flag:#E0B166; --flag-soft:#2A2110; --flag-line:#6B5423;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; padding:0 0 5rem;
  background:var(--ground); color:var(--body);
  font-family:"Source Sans 3",ui-sans-serif,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  font-size:15px; line-height:1.6;
  font-variant-numeric:tabular-nums; font-feature-settings:"tnum" 1;
}
.wrap{max-width:1560px;margin:0 auto;padding:0 clamp(1rem,3vw,2.25rem)}
.narrow{max-width:70ch}
.mast{border-bottom:2px solid var(--ink);margin:0 0 1.75rem;padding:2.75rem 0 1.5rem}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);
  display:flex;flex-wrap:wrap;gap:.5rem 1.25rem;margin:0 0 .9rem
}
h1{
  font-family:Bitter,Georgia,"Times New Roman",serif; font-weight:700;
  font-size:clamp(2rem,4.2vw,3.05rem); line-height:1.06; letter-spacing:-.022em;
  color:var(--ink); margin:0 0 .6rem; text-wrap:balance;
}
.dek{font-size:1.05rem;color:var(--muted);margin:0;max-width:76ch}
.dek b{color:var(--ink);font-weight:600}
h2{
  font-family:Bitter,Georgia,serif;font-weight:600;color:var(--ink);
  font-size:1.42rem;letter-spacing:-.014em;margin:3.25rem 0 .2rem;text-wrap:balance;
}
h3{font-weight:600;color:var(--ink);font-size:.95rem;margin:1.8rem 0 .55rem}
.sec-rule{height:1px;background:var(--line-strong);margin:.5rem 0 1.2rem}
p{margin:.55rem 0}
.notice{
  background:var(--flag-soft);border:1px solid var(--flag-line);border-left-width:5px;
  border-radius:4px;padding:1rem 1.25rem;
}
.notice .lbl{
  font-family:"IBM Plex Mono",monospace;font-size:11px;letter-spacing:.12em;
  text-transform:uppercase;color:var(--flag);font-weight:500;display:block;margin-bottom:.4rem
}
.notice p{margin:.35rem 0;color:var(--body);max-width:80ch}
.notice strong{color:var(--ink)}
.notices{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,26rem),1fr));gap:1rem;margin:1rem 0}
.step{
  display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap;
  margin:3rem 0 .2rem;padding-top:1.4rem;border-top:1px solid var(--line-strong);
}
.step .from,.step .to{
  font-family:"IBM Plex Mono",monospace;font-size:12px;font-weight:500;
  padding:.15rem .5rem;border-radius:3px;background:var(--raise);color:var(--ink);
  border:1px solid var(--line);white-space:nowrap
}
.step .arrow{color:var(--accent)}
.step .what{font-family:Bitter,Georgia,serif;font-size:1.18rem;font-weight:600;color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(9.5rem,1fr));gap:1px;
       background:var(--line);border:1px solid var(--line);border-radius:5px;overflow:hidden;margin:1.1rem 0}
.stat{background:var(--surface);padding:.8rem .95rem}
.stat .k{font-size:11px;letter-spacing:.07em;text-transform:uppercase;color:var(--faint);font-weight:600}
.stat .v{font-family:Bitter,Georgia,serif;font-size:1.6rem;font-weight:600;letter-spacing:-.02em;
         line-height:1.15;margin-top:.15rem;color:var(--ink)}
.stat .v.pos{color:var(--pos)} .stat .v.neg{color:var(--neg)}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:5px;background:var(--surface);max-width:100%}
.scroll.tall{max-height:78vh;overflow-y:auto}
table{border-collapse:separate;border-spacing:0;width:100%;font-size:13.5px}
th,td{padding:.4rem .6rem;text-align:right;white-space:nowrap;border-bottom:1px solid var(--line)}
thead th{
  position:sticky;top:0;z-index:3;background:var(--raise);color:var(--muted);
  font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;font-weight:600;
  border-bottom:1px solid var(--line-strong);
}
td.l,th.l{text-align:left}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:var(--accent-soft)}
.pos{color:var(--pos)} .neg{color:var(--neg)} .nil{color:var(--faint)}
td.num{font-weight:600}
.mono{font-family:"IBM Plex Mono",monospace;font-size:12px;color:var(--muted)}
.tot{font-family:Bitter,Georgia,serif;font-weight:600;color:var(--ink)}
.cell-bar{position:relative}
.bar{position:absolute;left:0;top:50%;transform:translateY(-50%);height:1.15em;border-radius:2px;z-index:0}
.bar.pos{background:var(--pos-soft)} .bar.neg{background:var(--neg-soft)}
.cell-bar span.n{position:relative;z-index:1}
.ledger th.name,.ledger td.name{
  position:sticky;left:0;z-index:2;background:var(--surface);
  border-right:1px solid var(--line-strong);text-align:left;
  font-weight:600;color:var(--ink);min-width:11.5rem
}
.ledger thead th.name{z-index:4;background:var(--raise)}
.ledger tbody tr:hover td.name{background:var(--accent-soft)}
.ledger td.sep,.ledger th.sep{border-left:1px solid var(--line-strong)}
.chip{
  display:inline-block;font-size:10.5px;font-weight:600;letter-spacing:.03em;
  padding:.05rem .38rem;border-radius:3px;background:var(--raise);color:var(--muted);
  border:1px solid var(--line)
}
.chip.up{background:var(--pos-soft);color:var(--pos);border-color:transparent}
.chip.dn{background:var(--neg-soft);color:var(--neg);border-color:transparent}
.foot{margin-top:3.5rem;padding-top:1.25rem;border-top:2px solid var(--ink);color:var(--muted)}
.foot strong{color:var(--ink)}
a{color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

H = []
A = H.append
A('<title>Whole-Arc Movers</title>')
A('<link rel="preconnect" href="https://fonts.googleapis.com">')
A('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
A('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
  'family=Bitter:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700&'
  'family=IBM+Plex+Mono:wght@400;500&display=swap">')
A('<style>' + CSS + '</style>')
A('<div class="wrap">')
A('<header class="mast">')
A('<div class="eyebrow"><span>ORDER R</span><span>Measurement only</span>'
  '<span>%d active rows</span><span>%d boards</span></div>' % (len(REC), len(LAB)))
A('<h1>Whole-arc movers</h1>')
A('<p class="dek">Who the pedigree-conditional charge has hurt, who it has helped, and by how much '
  '&mdash; across the entire arc rather than the last step. <b>ORDER K</b> is the last board before '
  'this mechanism path began; <b>ORDER P</b> is where the charge was introduced; the <b>ORDER R</b> '
  'boards are the softening the owner ruled. <b>Nothing here is adopted and nothing lands.</b></p>')
A('</header>')
A('<div class="notices">')
A('<div class="notice"><span class="lbl">Read rank, not points</span>'
  '<p>The board totals are different numbers. ORDER K totals <strong>%s</strong> and ORDER P totals '
  '<strong>%s</strong> &mdash; <strong>%s fewer points</strong> spread across the same %d players. Most '
  'rows therefore fall in absolute terms for a reason that has nothing to do with any individual '
  'player: there are simply fewer points on the board to go round.</p>'
  '<p><strong>Rank is the fair comparison across these boards. Absolute points are not.</strong> Both '
  'are shown; the rank-change columns are the ones to read when comparing one board with another.</p>'
  '</div>'
  % ('{:,}'.format(TOT.get('K', 0)), '{:,}'.format(TOT.get('P', 0)),
     '{:,}'.format(TOT.get('K', 0) - TOT.get('P', 0)), len(REC)))
A('<div class="notice"><span class="lbl">The spanning variant is not a recommendation</span>'
  '<p>The &ldquo;softening&rdquo; and &ldquo;whole arc&rdquo; columns use <strong>%s</strong> &mdash; %s. '
  'It is the far corner of the grid: both levers at their softest. It was chosen because it spans the '
  'arc, <strong>not because this seat prefers it. This seat recommends nothing.</strong></p>'
  '<p>Every other variant carries its own value, rank and charge columns in the ledger below and in '
  '<span class="mono">ARC_R.csv</span>.</p></div>'
  % (SPAN, html.escape(NICE.get(SPAN, SPAN))))
A('</div>')

A('<h2>The boards</h2><div class="sec-rule"></div>')
A('<div class="scroll"><table><thead><tr>'
  '<th class="l">Board</th><th class="l">md5</th><th>Total</th>'
  '<th>vs ORDER K</th><th>vs ORDER P</th><th class="l">What it is</th>'
  '</tr></thead><tbody>')
for l in LAB:
    dk = TOT[l] - TOT.get('K', 0)
    dp = TOT[l] - TOT.get('P', 0)
    A('<tr><td class="l"><b>%s</b></td><td class="l mono">%s</td>'
      '<td class="tot">%s</td><td class="num %s">%s</td><td class="num %s">%s</td>'
      '<td class="l" style="color:var(--muted)">%s</td></tr>'
      % (l, MD5[l][:8], '{:,}'.format(TOT[l]), cls_of(dk), fs(dk), cls_of(dp), fs(dp),
         html.escape(NICE[l])))
A('</tbody></table></div>')
if MISSING_CENSUS:
    A('<p style="color:var(--muted)">Charge columns are absent for %s &mdash; the engine-measured '
      'census for those boards is not on disk. <b>Reported as absent, never as zero.</b></p>'
      % ', '.join(MISSING_CENSUS))

STEPLBL = {'PK': ('ORDER K', 'ORDER P', 'The mechanism is introduced'),
           'SPAN_P': ('ORDER P', SPAN, 'The softening'),
           'ARC': ('ORDER K', SPAN, 'The whole arc')}
for st, nm in STEPS:
    e = SUM['steps'][st]
    fr, to, what = STEPLBL[st]
    A('<div class="step"><span class="from">%s</span><span class="arrow">&rarr;</span>'
      '<span class="to">%s</span><span class="what">%s</span></div>' % (fr, to, what))
    A('<div class="stats">')
    for k, v, c in (('Rows up in points', '{:,}'.format(e['up']), 'pos'),
                    ('Rows down in points', '{:,}'.format(e['down']), 'neg'),
                    ('Unchanged', '{:,}'.format(e['flat']), ''),
                    ('Net points', '{:+,}'.format(e['net']), cls_of(e['net'])),
                    ('Rows up in rank', '{:,}'.format(e['rank_up']), 'pos'),
                    ('Rows down in rank', '{:,}'.format(e['rank_down']), 'neg')):
        A('<div class="stat"><div class="k">%s</div><div class="v %s">%s</div></div>' % (k, c, v))
    A('</div>')
    if e['null']:
        A('<p style="color:var(--muted)">%d rows could not be scored on both sides of this step. They '
          'are counted as <b>nulls, never as zeros</b>, and each carries its reason in the note '
          'column of the ledger.</p>' % e['null'])
    mxb = max([abs(d['net']) for d in e['by_band'].values()] or [1])
    A('<h3>By pick band</h3>')
    A('<div class="scroll"><table><thead><tr><th class="l">Band</th><th>n</th>'
      '<th>Up</th><th>Down</th><th>Net points</th><th class="sep">Rank up</th><th>Rank down</th>'
      '</tr></thead><tbody>')
    for b, d in e['by_band'].items():
        A('<tr><td class="l"><b>%s</b></td><td class="nil">%d</td>'
          '<td class="pos">%d</td><td class="neg">%d</td>'
          '<td class="num cell-bar %s">%s<span class="n">%s</span></td>'
          '<td class="pos sep">%d</td><td class="neg">%d</td></tr>'
          % (b, d['n'], d['up'], d['down'], cls_of(d['net']),
             bar(d['net'], mxb, cls_of(d['net'])), fs(d['net']), d['rank_up'], d['rank_down']))
    A('</tbody></table></div>')
    coh = [(c, d) for c, d in e['by_cohort'].items() if d['up'] is not None]
    mxc = max([abs(d['net']) for _, d in coh] or [1])
    A('<h3>By cohort year <span style="font-weight:400;color:var(--muted)">'
      '(draft year + 1, except MSD where it is the draft year &mdash; the engine&rsquo;s own clock)'
      '</span></h3>')
    A('<div class="scroll"><table><thead><tr><th class="l">Cohort</th><th>n</th>'
      '<th>Up</th><th>Down</th><th>Net points</th><th class="sep">Rank up</th><th>Rank down</th>'
      '</tr></thead><tbody>')
    for c, d in e['by_cohort'].items():
        if d['up'] is None:
            A('<tr><td class="l nil">%s</td><td class="nil">%d</td>'
              '<td class="l nil" colspan="5">not scored &mdash; a null, reported as one</td></tr>'
              % (html.escape(str(c)), d['n']))
            continue
        A('<tr><td class="l"><b>%s</b></td><td class="nil">%d</td>'
          '<td class="pos">%d</td><td class="neg">%d</td>'
          '<td class="num cell-bar %s">%s<span class="n">%s</span></td>'
          '<td class="pos sep">%d</td><td class="neg">%d</td></tr>'
          % (c, d['n'], d['up'], d['down'], cls_of(d['net']),
             bar(d['net'], mxc, cls_of(d['net'])), fs(d['net']), d['rank_up'], d['rank_down']))
    A('</tbody></table></div>')
    A('<h3>The ten largest movers each way</h3>')
    A('<div class="scroll"><table><thead><tr>'
      '<th class="l">Player</th><th>Pick</th><th class="l">Band</th><th>Age</th>'
      '<th>Points</th><th>Percent</th><th>Rank</th>'
      '<th class="sep l">Player</th><th>Pick</th><th class="l">Band</th><th>Age</th>'
      '<th>Points</th><th>Percent</th><th>Rank</th>'
      '</tr></thead><tbody>')
    up, dn = e['top_up'], e['top_down']
    for i in range(max(len(up), len(dn), 1)):
        cells = []
        for j, src in ((0, up), (1, dn)):
            sepc = ' sep' if j else ''
            if i < len(src):
                r = src[i]
                cc = cls_of(r['d']); dr = r['drank']
                cells.append(
                    '<td class="l%s">%s</td><td class="nil">%s</td><td class="l nil">%s</td>'
                    '<td class="nil">%s</td><td class="num %s">%s</td><td class="%s">%s</td>'
                    '<td><span class="chip %s">%s</span></td>'
                    % (sepc, html.escape(str(r['player'])),
                       r['pick'] if r['pick'] else 'pool', r['band'],
                       r['age'] if r['age'] is not None else '',
                       cc, fs(r['d']), cc, fp(r['dpct']),
                       'up' if (dr or 0) > 0 else ('dn' if (dr or 0) < 0 else ''), fs(dr) or '0'))
            else:
                cells.append('<td class="l%s nil">&mdash;</td><td colspan="6"></td>' % sepc)
        A('<tr>' + ''.join(cells) + '</tr>')
    A('</tbody></table></div>')

A('<h2>Every row, sorted by the whole-arc move</h2><div class="sec-rule"></div>')
A('<p class="narrow">Sorted by the size of <b>%s minus ORDER K</b>, largest first, so the biggest '
  'movers in both directions sit at the top. Rank 1 is the most valuable of the %d rows, and a '
  '<b>positive</b> rank change means the row moved <b>up</b> the board. The player column stays put '
  'as you scroll sideways.</p>' % (SPAN, len(REC)))
A('<p class="narrow" style="color:var(--muted)">Mechanism diagnostics: <b>PG</b> is the pedigree '
  'premium at the row&rsquo;s entry price, in points a game. <b>s(age)</b> is production against the '
  'S1 age bar alone; <b>s(ped)</b> is production against that bar <i>plus</i> the premium, which is '
  'what the charge actually reads. By construction s(ped) = s(age) &minus; PG. The <b>chg</b> columns '
  'are the share of the pedigree leg removed on each board.</p>')
A('<div class="scroll tall"><table class="ledger"><thead><tr>')
A('<th class="name">Player</th><th>Coh</th><th class="l">Pos</th><th class="l">Path</th>'
  '<th>Pick</th><th>Age</th><th>G</th><th>v0</th>'
  '<th class="sep">PG</th><th>s(age)</th><th>s(ped)</th>')
for i, l in enumerate(LAB):
    A('<th class="%s">%s</th>' % ('sep' if i == 0 else '', l))
for i, l in enumerate(LAB):
    A('<th class="%s">#%s</th>' % ('sep' if i == 0 else '', l))
_first = True
for l in LAB:
    if l in CH:
        A('<th class="%s">chg %s</th>' % ('sep' if _first else '', l))
        _first = False
for i, lbl in enumerate(('P&minus;K', '%', '&Delta;#', '%s&minus;P' % SPAN, '%', '&Delta;#',
                         'ARC', '%', '&Delta;#')):
    A('<th class="%s">%s</th>' % ('sep' if i == 0 else '', lbl))
A('<th class="l sep">Note</th></tr></thead><tbody>')
for r in REC:
    c = ['<td class="name">%s</td>' % html.escape(str(r['player'])),
         '<td>%s</td>' % (r['cohort'] if r['cohort'] is not None
                          else '<span class="nil">null</span>'),
         '<td class="l">%s</td>' % (r['pos'] or ''),
         '<td class="l">%s</td>' % (r['pathway'] or ''),
         '<td>%s</td>' % (r['pick'] if r['pick'] else '<span class="nil">pool</span>'),
         '<td>%s</td>' % (r['age'] if r['age'] is not None else ''),
         '<td>%s</td>' % f0(r['games']),
         '<td>%s</td>' % f0(r['v0']),
         '<td class="sep">%s</td>' % f2(r['pg']),
         '<td>%s</td>' % f2(r['s_age']),
         '<td>%s</td>' % f2(r['s_ped'])]
    for j, l in enumerate(LAB):
        c.append('<td class="%s">%s</td>' % ('sep' if j == 0 else '', f0(r.get('v_' + l))))
    for j, l in enumerate(LAB):
        c.append('<td class="nil%s">%s</td>' % (' sep' if j == 0 else '', f0(r.get('rank_' + l))))
    fst = True
    for l in LAB:
        if l in CH:
            c.append('<td class="%s">%s</td>' % ('sep' if fst else '', fc(r.get('charge_' + l))))
            fst = False
    for j, (st, _x) in enumerate(STEPS):
        d = r['d_' + st]; dr = r['drank_' + st]
        c.append('<td class="num %s%s">%s</td>' % (cls_of(d), ' sep' if j == 0 else '', fs(d)))
        c.append('<td class="%s">%s</td>' % (cls_of(d), fp(r['dpct_' + st])))
        c.append('<td><span class="chip %s">%s</span></td>'
                 % ('up' if (dr or 0) > 0 else ('dn' if (dr or 0) < 0 else ''), fs(dr) or '0'))
    c.append('<td class="l sep nil">%s</td>' % html.escape(r['note']))
    A('<tr>' + ''.join(c) + '</tr>')
A('</tbody></table></div>')
A('<div class="foot"><p class="narrow"><strong>What this page is not.</strong> It is a report. '
  '<strong>No player&rsquo;s value is an acceptance criterion</strong> and not one constant in ORDER R '
  'was chosen with any row in view &mdash; a standing prohibition in this project after a real error. '
  'Nothing on this page is adopted, nothing lands, and no variant is recommended.</p>'
  '<p class="narrow mono">ORDER R &middot; engine ea5c5e5e &middot; store cb38ef11 &middot; '
  'ARC_R.csv &middot; ARC_R.json</p></div>')
A('</div>')
open(os.path.join(HERE, 'ARC_R.html'), 'w').write('\n'.join(H) + '\n')
print('wrote ARC_R.csv, ARC_R.json, ARC_R.html   (%d rows, %d boards, spanning variant %s)'
      % (len(REC), len(LAB), SPAN))
for _st, _nm in STEPS:
    _e = SUM['steps'][_st]
    print('  %-52s up %3d  down %3d  flat %3d  null %2d  net %+8d'
          % (_nm, _e['up'], _e['down'], _e['flat'], _e['null'], _e['net']))
