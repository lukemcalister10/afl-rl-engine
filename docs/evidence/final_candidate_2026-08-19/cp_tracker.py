#!/usr/bin/env python3
"""COMPLETION PASS (board a05fe951 — THE PARITY BOARD). fc_tracker.py carried; the CANDIDATE
column is re-pointed at CP_CAND (a05fe951), the D6 consolidation and the D7 parity guard EACH GET
THEIR OWN LEVER LINE, and the outputs are renamed. The header, the delta columns, the moved-row rule
and the lever machinery are UNCHANGED.

ORIGINAL FINAL-CANDIDATE HEADER FOLLOWS.
"""
"""FINAL-CANDIDATE — THE TRACKER and THE PER-LEVER BREAKDOWN. The assembly seat's as_tracker.py
with the candidate column repointed at daa16812 and TWO NEW LEVER LINES added — the unwind (U0=7)
and the D6 injury consolidation — each as its own row, as the order requires. The column set, the
delta set, the moved-row filter, the CSS/JS and the CSV header are otherwise byte-identical, so the
header check against TRACKER_ASSEMBLY is a like-for-like comparison.

ORIGINAL ASSEMBLY HEADER FOLLOWS.
"""
import json, os, hashlib, csv, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM = SP + '/asm'
FCD = SP + '/fc'        # THIS seat's boards


CPD = SP + '/compscratch'   # THIS (completion) seat's own boards


def bdir(t):
    """CP_*/D7_* are THIS seat's builds, FC_* the final-candidate seat's, the rest the assembly's."""
    if t.startswith('CP_') or t.startswith('D7_'):
        return CPD
    return FCD if t.startswith('FC_') else ASM

COLS = [('live', 'live', '88ce647f'), ('IDENT_K', 'K', 'f3101883'),
        ('IDENT_P', 'P', '374d4e44'), ('L0_R', 'R', '7f88f509'), ('CP_CAND', 'CANDIDATE', 'a05fe951')]
STACK = [('L0_R', 'R — the reference (A + B1 + p20 clip)'),
         ('L1_REC', '+ recency w = 0.47'),
         ('L2_COMP', '&nbsp;&nbsp;[superseded] the compressed cap at p20 — kept so the anchor move is visible'),
         ('V750_L2C15', '+ the compressed cap <b>p15</b> and the slope 0.105 (replacing the clip) — ANCHOR RULED AT v750'),
         ('V750_L3MAT', '+ the mature refit'),
         ('V750_L4SD', '+ the SD level offset 2.98, standalone'),
         ('V750_L5A', '+ absence I1 — the measured credit curve'),
         ('V750_L5B', '+ absence I2 — the graded reset (the F4 row swap WITHDRAWN at v750)'),
         ('V750_L5C', '+ absence I3 — the injury stream (live board only)'),
         ('V755_L5CR', '+ D4 — the in-season ramp f**1.5 on the two DEPTH clocks (FOLDED IN, v755)'),
         ('V755_CAND', '+ absence I4 — the R3 production fade'),
         ('FC_BASE', '+ <b>the unwind U0 = 7 return games</b> (RL_O41_BREAK=unwind) — '
                     '<b>OWNER-RULED, DATA-SUPPORTED</b>'),
         ('FC_CAND', '+ <b>D6 — the injury consolidation</b> (RL_O42=1): the owner\'s sheet becomes the '
                     'single injury truth and LTI_REGISTER.md loses its live consumption'),
         ('CP_CAND', '+ <b>D7 — THE PARITY GUARD</b> (RL_O43=1), register v771, owner-ruled: per treated '
                     'row <b>final = max(v_injury_regime, v_healthy_counterpart)</b>. NO FREE PARAMETER '
                     '— a per-row max, so it can only RAISE. 23 rows lifted, none fall  =  '
                     '<b>THE CANDIDATE</b>')]

PATHS = {}
for t, _, _x in COLS:
    q = (SP + '/o29r/seal/rl_after/rl_app_data.json') if t == 'live' \
        else '%s/bb_%s/rl_after/rl_app_data.json' % (bdir(t), t)
    if os.path.exists(q):
        PATHS[t] = q
for t, _ in STACK:
    q = '%s/bb_%s/rl_after/rl_app_data.json' % (bdir(t), t)
    if os.path.exists(q):
        PATHS[t] = q
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
if MD5.get('live', '')[:8] != '88ce647f':
    PATHS.pop('live', None); MD5.pop('live', None)
B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
TOT = {t: sum(V[t].values()) for t in V}

META = {}
for t in ('CP_CAND', 'FC_CAND', 'L0_R', 'IDENT_P', 'live'):
    for k, r in B.get(t, {}).items():
        if k not in META:
            META[k] = dict(name=r.get('name') or k, pos=r.get('grp') or (r.get('fut') or [['?']])[0][0],
                           age=r.get('age'), club=r.get('club'), band=r.get('band'),
                           pick=r.get('pk'), cat=r.get('cat'))
KEYS = sorted(set().union(*[set(V[t]) for t in V]))

# ---- the moved-row filter -------------------------------------------------------------------------
present = [t for t, _, _x in COLS if t in V]
ROWS = []
for k in KEYS:
    vals = {t: V[t].get(k) for t in present}
    if vals.get('CP_CAND') is None:
        continue
    seq = [vals[t] for t in present if vals[t] is not None]
    if len(set(seq)) <= 1:
        continue                      # never moved by anything: out of the tracker by the owner's rule
    ROWS.append((k, vals))

def d(a, b):
    return None if (a is None or b is None) else (b - a)

TR = []
for k, vals in ROWS:
    m = META.get(k, {})
    TR.append(dict(key=k, name=m.get('name'), pos=m.get('pos'), age=m.get('age'), club=m.get('club'),
                   band=m.get('band'), pick=m.get('pick'), cat=m.get('cat'),
                   live=vals.get('live'), K=vals.get('IDENT_K'), P=vals.get('IDENT_P'),
                   R=vals.get('L0_R'), cand=vals.get('CP_CAND'),
                   d_live_K=d(vals.get('live'), vals.get('IDENT_K')),
                   d_K_P=d(vals.get('IDENT_K'), vals.get('IDENT_P')),
                   d_P_R=d(vals.get('IDENT_P'), vals.get('L0_R')),
                   d_R_cand=d(vals.get('L0_R'), vals.get('CP_CAND')),
                   d_live_cand=d(vals.get('live'), vals.get('CP_CAND')),
                   d_K_cand=d(vals.get('IDENT_K'), vals.get('CP_CAND'))))
TR.sort(key=lambda r: -abs(r['d_R_cand'] or 0))

CSS = """
:root{--bg:#fbfbfa;--fg:#1a1a18;--mut:#6b6b66;--line:#e0dfdb;--hd:#f2f1ee;--up:#186a3b;--dn:#a03028;--acc:#2b4c7e}
:root[data-theme=dark]{--bg:#16171a;--fg:#e9e8e4;--mut:#9a9a94;--line:#2e2f33;--hd:#1f2024;--up:#4ec27e;--dn:#e8776b;--acc:#7aa7e0}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#16171a;--fg:#e9e8e4;--mut:#9a9a94;--line:#2e2f33;--hd:#1f2024;--up:#4ec27e;--dn:#e8776b;--acc:#7aa7e0}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;margin:0;padding:24px}
h1{font-size:20px;margin:0 0 4px}h2{font-size:15px;margin:26px 0 8px;color:var(--acc)}
.sub{color:var(--mut);font-size:13px;margin-bottom:16px;max-width:70em}
.warn{border-left:3px solid var(--dn);background:color-mix(in srgb,var(--dn) 7%,transparent);padding:10px 14px;margin:14px 0;max-width:70em;border-radius:0 4px 4px 0}
.note{border-left:3px solid var(--acc);background:color-mix(in srgb,var(--acc) 7%,transparent);padding:10px 14px;margin:14px 0;max-width:70em;border-radius:0 4px 4px 0}
.wrap{overflow-x:auto;border:1px solid var(--line);border-radius:6px;max-width:100%}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums;font-size:13px}
th,td{padding:5px 9px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap}
th:nth-child(-n+5),td:nth-child(-n+5){text-align:left}
thead th{background:var(--hd);position:sticky;top:0;cursor:pointer;user-select:none;font-weight:600}
thead th:hover{color:var(--acc)}
tbody tr:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
.u{color:var(--up)}.d{color:var(--dn)}
.tot{font-weight:600}
code{background:var(--hd);padding:1px 5px;border-radius:3px;font-size:12px}
.k{color:var(--mut);font-size:12px}
"""

JS = """
document.querySelectorAll('table').forEach(function(T){
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


def num(v):
    return '' if v is None else '{:,}'.format(int(v))


def dlt(v):
    if v is None:
        return '<td data-v="0" class="k">—</td>'
    c = 'u' if v > 0 else ('d' if v < 0 else '')
    return '<td data-v="%d" class="%s">%s</td>' % (v, c, ('{:+,}'.format(int(v)) if v else '0'))


def esc(s):
    return html.escape(str(s if s is not None else ''))


# ---------------- THE TRACKER ----------------------------------------------------------------------
hdr = []
for t, lab, want in COLS:
    if t not in V:
        continue
    hdr.append('%s %s %s' % (lab, MD5[t][:8], '{:,}'.format(TOT[t])))

h = ['<title>Final Candidate Tracker</title>', '<style>%s</style>' % CSS]
h.append('<h1>THE TRACKER — live &rarr; K &rarr; P &rarr; R &rarr; THE CANDIDATE</h1>')
h.append('<div class="sub">The owner\'s standing presentation law (register v741, refined v742). '
         'Only players the mechanism or the repairs actually moved are listed. Absolute points only. '
         'Every column sorts — click a header. <b>Nothing here is adopted; the candidate is for owner '
         'review.</b></div>')
h.append('<div class="wrap"><table><thead><tr>'
         '<th>player</th><th>pos</th><th>club</th><th>cat</th><th>age</th>')
for t, lab, _w in COLS:
    if t not in V:
        continue
    h.append('<th>%s</th>' % lab)
    if t == 'IDENT_K':
        h.append('<th>&Delta; live&rarr;K</th>')
    elif t == 'IDENT_P':
        h.append('<th>&Delta; K&rarr;P</th>')
    elif t == 'L0_R':
        h.append('<th>&Delta; P&rarr;R</th>')
    elif t == 'FC_CAND':
        h.append('<th>&Delta; R&rarr;cand</th><th>&Delta; live&rarr;cand</th><th>&Delta; K&rarr;cand</th>')
h.append('</tr></thead><tbody>')
for r in TR:
    h.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td data-v="%s">%s</td>'
             % (esc(r['name']), esc(r['pos']), esc(r['club']), esc(r['cat']),
                r['age'] if r['age'] is not None else '', r['age'] if r['age'] is not None else ''))
    for t, lab, _w in COLS:
        if t not in V:
            continue
        key = {'live': 'live', 'IDENT_K': 'K', 'IDENT_P': 'P', 'L0_R': 'R', 'CP_CAND': 'cand'}[t]
        h.append('<td data-v="%s">%s</td>' % (r[key] if r[key] is not None else 0, num(r[key])))
        if t == 'IDENT_K':
            h.append(dlt(r['d_live_K']))
        elif t == 'IDENT_P':
            h.append(dlt(r['d_K_P']))
        elif t == 'L0_R':
            h.append(dlt(r['d_P_R']))
        elif t == 'FC_CAND':
            h.append(dlt(r['d_R_cand'])); h.append(dlt(r['d_live_cand'])); h.append(dlt(r['d_K_cand']))
    h.append('</tr>')
h.append('</tbody></table></div>')
h.append('<div class="sub k">%d moved rows of 804 on the board. Board totals in the header row above: %s</div>'
         % (len(TR), ' &middot; '.join(hdr)))
h.append('<script>%s</script>' % JS)
open(os.path.join(HERE, 'TRACKER_COMPLETION.html'), 'w').write('\n'.join(h))

with open(os.path.join(HERE, 'TRACKER_COMPLETION.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['player', 'pos', 'club', 'cat', 'age', 'band', 'pick',
                'live', 'K', 'd_live_K', 'P', 'd_K_P', 'R', 'd_P_R', 'candidate',
                'd_R_cand', 'd_live_cand', 'd_K_cand'])
    for r in TR:
        w.writerow([r['name'], r['pos'], r['club'], r['cat'], r['age'], r['band'], r['pick'],
                    r['live'], r['K'], r['d_live_K'], r['P'], r['d_K_P'], r['R'], r['d_P_R'],
                    r['cand'], r['d_R_cand'], r['d_live_cand'], r['d_K_cand']])

# ---------------- THE PER-LEVER BREAKDOWN ----------------------------------------------------------
present_stack = [(t, lab) for t, lab in STACK if t in V]
g = ['<title>Final Candidate Levers</title>', '<style>%s</style>' % CSS]
g.append('<h1>THE PER-LEVER BREAKDOWN — R &rarr; THE CANDIDATE, one lever at a time</h1>')
g.append('<div class="sub">The owner asked to see what each lever is doing (register v742). Each board '
         'below is the one above it <b>plus one lever</b>, built from the dial stack by strictly '
         'sequential engine runs, so every marginal effect is a subtraction and not an argument. '
         'Interactions live <i>inside</i> each marginal — each lever is measured on top of the ones '
         'above it — which is the honest reading and the one that was asked for.</div>')

g.append('<h2>The board, lever by lever</h2>')
g.append('<div class="wrap"><table><thead><tr><th>lever</th><th>md5</th><th>board total</th>'
         '<th>marginal</th><th>rows moved</th><th>up</th><th>down</th><th>cumulative vs R</th>'
         '</tr></thead><tbody>')
LEV = {}
for i, (t, lab) in enumerate(present_stack):
    if i == 0:
        g.append('<tr><td>%s</td><td class="k">%s</td><td data-v="%d" class="tot">%s</td>'
                 '<td class="k">—</td><td class="k">—</td><td class="k">—</td><td class="k">—</td>'
                 '<td class="k">—</td></tr>'
                 % (lab, MD5[t][:8], TOT[t], num(TOT[t])))
        continue
    prev = present_stack[i - 1][0]
    mv = [k for k in KEYS if k in V[t] and k in V[prev] and V[t][k] != V[prev][k]]
    up = sum(1 for k in mv if V[t][k] > V[prev][k])
    LEV[t] = dict(prev=prev, marg=TOT[t] - TOT[prev], moved=len(mv), up=up, dn=len(mv) - up,
                  rows=sorted(((k, V[t][k] - V[prev][k]) for k in mv), key=lambda z: -abs(z[1])))
    g.append('<tr><td>%s</td><td class="k">%s</td><td data-v="%d" class="tot">%s</td>%s'
             '<td data-v="%d">%d</td><td data-v="%d">%d</td><td data-v="%d">%d</td>%s</tr>'
             % (lab, MD5[t][:8], TOT[t], num(TOT[t]), dlt(TOT[t] - TOT[prev]),
                len(mv), len(mv), up, up, len(mv) - up, len(mv) - up,
                dlt(TOT[t] - TOT[present_stack[0][0]])))
g.append('</tbody></table></div>')

g.append('<h2>The rows each lever moves most</h2>')
g.append('<div class="sub">The ten largest absolute movers for every lever. <b>These are consequences, '
         'never targets.</b> No named player gates anything in this build.</div>')
for t, lab in present_stack[1:]:
    if t not in LEV:
        continue
    g.append('<h2 style="font-size:13px;color:var(--fg)">%s <span class="k">&nbsp;marginal %s on %d rows</span></h2>'
             % (lab, '{:+,}'.format(LEV[t]['marg']), LEV[t]['moved']))
    if not LEV[t]['rows']:
        g.append('<div class="sub k">This lever moved no row on this board.</div>'); continue
    g.append('<div class="wrap"><table><thead><tr><th>player</th><th>pos</th><th>age</th>'
             '<th>before</th><th>after</th><th>change</th></tr></thead><tbody>')
    for k, dv in LEV[t]['rows'][:10]:
        m = META.get(k, {})
        g.append('<tr><td>%s</td><td>%s</td><td data-v="%s">%s</td>'
                 '<td data-v="%d">%s</td><td data-v="%d">%s</td>%s</tr>'
                 % (esc(m.get('name')), esc(m.get('pos')),
                    m.get('age') if m.get('age') is not None else '',
                    m.get('age') if m.get('age') is not None else '',
                    V[LEV[t]['prev']][k], num(V[LEV[t]['prev']][k]),
                    V[t][k], num(V[t][k]), dlt(dv)))
    g.append('</tbody></table></div>')
g.append('<script>%s</script>' % JS)
open(os.path.join(HERE, 'LEVERS_COMPLETION.html'), 'w').write('\n'.join(g))

json.dump(dict(totals=TOT, md5=MD5, n_tracked=len(TR),
               lever={t: {kk: vv for kk, vv in LEV[t].items() if kk != 'rows'} for t in LEV}),
          open(os.path.join(HERE, 'TRACKER_CP.json'), 'w'), indent=1, sort_keys=True)
print('TRACKER_COMPLETION.html  %d moved rows' % len(TR))
print('TRACKER_COMPLETION.csv')
print('LEVERS_COMPLETION.html   %d levers' % len(LEV))
for t in TOT:
    print('  %-9s %s %s' % (t, MD5[t][:8], '{:,}'.format(TOT[t])))
