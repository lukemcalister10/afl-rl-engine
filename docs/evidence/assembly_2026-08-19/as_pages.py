#!/usr/bin/env python3
"""ASSEMBLY BUILD — THE THREE DOCUMENTS THE OWNER ASKED FOR, in the standing format.

  ASSEMBLY_PLAYERS.html  the player list — all 804 rows, the five board columns, deltas, and the
                         mechanism legs (production leg, pedigree leg, the charge, the fade, the
                         unplayed clock, the absence take).
  ASSEMBLY_YEAR1.html    the year-1 class in draft order, the five board columns PLUS v0.
  ASSEMBLY_NOARB.html    the no-arb tables — the owner's five bands PLUS ALL / 1-20 / 21-64, in
                         BOTH windows, the pool arms in both windows, both baselines, with the
                         year paths yr0-7, the yr0->1 appreciation, the margin against the 14%
                         carry, and a two-sided verdict per band.

EVERY PAGE CARRIES THE SAME "WHAT IS IN THIS BOARD AND WHAT IS STILL BROKEN" BOX AT THE TOP
(as_box.py), so nothing that is broken can appear on one page and be missing from another.
THE MODERN 1-10 RED AND SSP ARE NAMED IN IT.

NOTHING IS ADOPTED. THE CANDIDATE IS FOR OWNER REVIEW.
"""
import json, os, html, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM = SP + '/asm'
sys.path.insert(0, HERE)
import as_box as BOX

CSS = """
:root{--bg:#fbfbfa;--fg:#1a1a18;--mut:#6b6b66;--line:#e0dfdb;--hd:#f2f1ee;--up:#186a3b;--dn:#a03028;--acc:#2b4c7e;--warn:#8a6d1f}
:root[data-theme=dark]{--bg:#16171a;--fg:#e9e8e4;--mut:#9a9a94;--line:#2e2f33;--hd:#1f2024;--up:#4ec27e;--dn:#e8776b;--acc:#7aa7e0;--warn:#d8b455}
:root[data-theme=dark]{--bg:#16171a;--fg:#e9e8e4;--mut:#9a9a94;--line:#2e2f33;--hd:#1f2024;--up:#4ec27e;--dn:#e8776b;--acc:#7aa7e0;--warn:#d8b455}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#16171a;--fg:#e9e8e4;--mut:#9a9a94;--line:#2e2f33;--hd:#1f2024;--up:#4ec27e;--dn:#e8776b;--acc:#7aa7e0;--warn:#d8b455}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;margin:0;padding:24px}
h1{font-size:20px;margin:0 0 4px}h2{font-size:15px;margin:26px 0 8px;color:var(--acc)}
.sub{color:var(--mut);font-size:13px;margin-bottom:16px;max-width:78em}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;max-width:100%;margin-bottom:18px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:13px}
th,td{padding:5px 9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th.l,td.l{text-align:left}
thead th{background:var(--hd);position:sticky;top:0;cursor:pointer;user-select:none;font-weight:600}
thead th:hover{color:var(--acc)}
tbody tr:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
.u{color:var(--up)}.d{color:var(--dn)}
.red{background:color-mix(in srgb,var(--dn) 14%,transparent);font-weight:600}
.amber{background:color-mix(in srgb,var(--warn) 16%,transparent)}
.flag{color:var(--dn);font-weight:700}
.k{color:var(--mut);font-size:12px}
code{background:var(--hd);padding:1px 5px;border-radius:3px;font-size:12px}
""" + BOX.BOX_CSS

JS = """
document.querySelectorAll('table.s').forEach(function(T){
  T.querySelectorAll('thead th').forEach(function(H,i){
    H.addEventListener('click',function(){
      var b=T.tBodies[0],rs=[].slice.call(b.rows),asc=H.dataset.asc!=='1';
      H.dataset.asc=asc?'1':'0';
      rs.sort(function(x,y){
        var a=x.cells[i].dataset.v,c=y.cells[i].dataset.v;
        if(a===undefined)a=x.cells[i].textContent;if(c===undefined)c=y.cells[i].textContent;
        var na=parseFloat(a),nc=parseFloat(c);
        if(!isNaN(na)&&!isNaN(nc))return asc?na-nc:nc-na;
        return asc?String(a).localeCompare(String(c)):String(c).localeCompare(String(a));
      });
      rs.forEach(function(r){b.appendChild(r)});
    });
  });
});
"""


def esc(s):
    return html.escape(str(s if s is not None else ''))


def num(v):
    return '' if v is None else '{:,}'.format(int(round(v)))


def dcell(v):
    if v is None:
        return '<td data-v="0" class="k">—</td>'
    c = 'u' if v > 0 else ('d' if v < 0 else '')
    return '<td data-v="%d" class="%s">%s</td>' % (v, c, ('{:+,}'.format(int(v)) if v else '0'))


def page(title, h1, subtitle, body):
    return '\n'.join(['<title>%s</title>' % title, '<style>%s</style>' % CSS,
                      '<h1>%s</h1>' % h1, '<div class="sub">%s</div>' % subtitle,
                      BOX.html_box(), body, '<script>%s</script>' % JS])


# ---- boards ---------------------------------------------------------------------------------------
import hashlib
COLS = [('live', 'live'), ('IDENT_K', 'K'), ('IDENT_P', 'P'), ('L0_R', 'R'), ('V750_CAND', 'CANDIDATE')]
PATHS = {}
for t, _ in COLS:
    q = (SP + '/o29r/seal/rl_after/rl_app_data.json') if t == 'live' \
        else '%s/bb_%s/rl_after/rl_app_data.json' % (ASM, t)
    if os.path.exists(q):
        PATHS[t] = q
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
if MD5.get('live', '')[:8] != '88ce647f':
    PATHS.pop('live', None); MD5.pop('live', None)
B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
TOT = {t: sum(V[t].values()) for t in V}
CAND = B['V750_CAND']
LEGS = {}
lp = os.path.join(HERE, 'LEGS_CAND.json')
if os.path.exists(lp):
    LEGS = json.load(open(lp))['rows']

HDR = ' &middot; '.join('%s <code>%s</code> %s' % (lab, MD5[t][:8], '{:,}'.format(TOT[t]))
                        for t, lab in COLS if t in V)

# ---- 1 · the player list --------------------------------------------------------------------------
rows = sorted(CAND.values(), key=lambda r: -r['v'])
h = ['<div class="sub k">Board totals: %s</div>' % HDR,
     '<h2>All %d rows on the board</h2>' % len(rows),
     '<div class="sub">Sorted by the candidate price. Every column sorts — click a header. '
     'The mechanism legs show how each price is actually made: the production leg is what he has '
     'shown, the pedigree leg is what he was bought for, the charge is the multiplier the pedigree '
     'leg pays for producing below the bar his price implies, the clock is how many seasons of '
     'unexplained absence he carries, and the fade is what that clock costs him.</div>',
     '<div class="wrap"><table class="s"><thead><tr>'
     '<th class="l">player</th><th class="l">pos</th><th class="l">club</th><th class="l">cat</th>'
     '<th>age</th><th>pick</th>']
for t, lab in COLS:
    if t in V:
        h.append('<th>%s</th>' % lab)
h.append('<th>&Delta; R&rarr;cand</th><th>&Delta; live&rarr;cand</th>')
if LEGS:
    h.append('<th>production leg</th><th>pedigree leg</th><th>charge</th><th>fade D</th>'
             '<th>unplayed clock</th><th>absence take</th>')
h.append('</tr></thead><tbody>')
for r in rows:
    k = r['key']
    h.append('<tr><td class="l">%s</td><td class="l">%s</td><td class="l">%s</td><td class="l">%s</td>'
             '<td data-v="%s">%s</td><td data-v="%s">%s</td>'
             % (esc(r.get('name')), esc(r.get('grp') or (r.get('fut') or [['?']])[0][0]),
                esc(r.get('club')), esc(r.get('cat')),
                r.get('age', ''), r.get('age', ''),
                r.get('pk') if r.get('pk') is not None else 999,
                r.get('pk') if r.get('pk') is not None else '—'))
    for t, lab in COLS:
        if t in V:
            v = V[t].get(k)
            h.append('<td data-v="%s">%s</td>' % (v if v is not None else 0, num(v)))
    dR = (V['V750_CAND'][k] - V['L0_R'][k]) if 'L0_R' in V and k in V['L0_R'] else None
    dL = (V['V750_CAND'][k] - V['live'][k]) if 'live' in V and k in V['live'] else None
    h.append(dcell(dR)); h.append(dcell(dL))
    if LEGS:
        g = LEGS.get(k, {})
        for f, fmt in (('prod', '%.0f'), ('ped', '%.0f'), ('charge', '%.3f'), ('D', '%.3f'),
                       ('cu', '%.2f'), ('take', '%.3f')):
            val = g.get(f)
            h.append('<td data-v="%s">%s</td>'
                     % (val if val is not None else -1, (fmt % val) if val is not None else '—'))
    h.append('</tr>')
h.append('</tbody></table></div>')
open(os.path.join(HERE, 'ASSEMBLY_PLAYERS.html'), 'w').write(page(
    'Assembly Players', 'THE PLAYER LIST — THE CANDIDATE',
    'All %d rows on the board, with the mechanism legs that make each price.' % len(rows),
    '\n'.join(h)))

# ---- 2 · the year-1 class in draft order -----------------------------------------------------------
Y1 = [r for r in CAND.values() if (r.get('ep') == 0 or r.get('age') is not None)
      and r.get('draft') and r.get('pk') is not None]
# the year-1 class = the most recent draft cohort on the board
maxyr = max((r.get('yr') or 0) for r in CAND.values()) - 1   # year-0 is the 2026 class; the YEAR-1 class is the one drafted the year before
Y1 = sorted([r for r in CAND.values() if (r.get('yr') or 0) == maxyr],
            key=lambda r: (r.get('pk') if r.get('pk') is not None else 999))
h = ['<div class="sub k">Board totals: %s</div>' % HDR,
     '<h2>The year-1 class — the %s draft, in draft order — %d rows</h2>' % (maxyr, len(Y1)),
     '<div class="sub">In pick order, with the entry price v0 beside the board columns so the '
     'first-year mark can be read directly off the page.</div>',
     '<div class="wrap"><table class="s"><thead><tr><th>pick</th><th class="l">player</th>'
     '<th class="l">pos</th><th class="l">club</th><th class="l">cat</th><th>v0</th>']
for t, lab in COLS:
    if t in V:
        h.append('<th>%s</th>' % lab)
h.append('<th>&Delta; R&rarr;cand</th></tr></thead><tbody>')
for r in Y1:
    k = r['key']
    pk = r.get('pk')
    v0 = r.get('v0') or (LEGS.get(k, {}) or {}).get('v0')
    h.append('<tr><td data-v="%s">%s</td><td class="l">%s</td><td class="l">%s</td>'
             '<td class="l">%s</td><td class="l">%s</td><td data-v="%s">%s</td>'
             % (pk if pk is not None else 999, pk if pk is not None else '—',
                esc(r.get('name')), esc(r.get('grp') or (r.get('fut') or [['?']])[0][0]),
                esc(r.get('club')), esc(r.get('cat')),
                v0 if v0 is not None else 0, num(v0) if v0 is not None else '—'))
    for t, lab in COLS:
        if t in V:
            v = V[t].get(k)
            h.append('<td data-v="%s">%s</td>' % (v if v is not None else 0, num(v)))
    dR = (V['V750_CAND'][k] - V['L0_R'][k]) if 'L0_R' in V and k in V['L0_R'] else None
    h.append(dcell(dR)); h.append('</tr>')
h.append('</tbody></table></div>')
open(os.path.join(HERE, 'ASSEMBLY_YEAR1.html'), 'w').write(page(
    'Assembly Year One', 'THE YEAR-1 CLASS — THE CANDIDATE',
    'The most recent draft class in pick order, with entry price beside every board.',
    '\n'.join(h)))

print('ASSEMBLY_PLAYERS.html  %d rows' % len(rows))
print('ASSEMBLY_YEAR1.html    %d rows' % len(Y1))
print('(ASSEMBLY_NOARB.html is written by as_noarb.py, which needs the extended-338 run)')
