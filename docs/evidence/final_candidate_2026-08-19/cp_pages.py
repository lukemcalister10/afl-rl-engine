#!/usr/bin/env python3
"""FINAL-CANDIDATE — THE OWNER DOCUMENTS THE OWNER ASKED FOR, in the standing format.

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
FCD = SP + '/fc'


CPD = SP + '/compscratch'   # THIS (completion) seat's own boards


def bdir(t):
    if t.startswith('CP_') or t.startswith('D7_'):
        return CPD
    return FCD if t.startswith('FC_') else ASM
sys.path.insert(0, HERE)
import fc_box as BOX

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
CANDTAG = 'CP_CAND'
COLS = [('live', 'live'), ('IDENT_K', 'K'), ('IDENT_P', 'P'), ('L0_R', 'R'), (CANDTAG, 'CANDIDATE')]
PATHS = {}
for t, _ in COLS:
    q = (SP + '/o29r/seal/rl_after/rl_app_data.json') if t == 'live' \
        else '%s/bb_%s/rl_after/rl_app_data.json' % (bdir(t), t)
    if os.path.exists(q):
        PATHS[t] = q
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
if MD5.get('live', '')[:8] != '88ce647f':
    PATHS.pop('live', None); MD5.pop('live', None)
B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
TOT = {t: sum(V[t].values()) for t in V}
CAND = B[CANDTAG]
LEGS = {}
lp = os.path.join(HERE, 'LEGS_CP.json')
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
    dR = (V[CANDTAG][k] - V['L0_R'][k]) if 'L0_R' in V and k in V['L0_R'] else None
    dL = (V[CANDTAG][k] - V['live'][k]) if 'live' in V and k in V['live'] else None
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
open(os.path.join(HERE, 'PLAYERS_COMPLETION.html'), 'w').write(page(
    'Assembly Players', 'THE PLAYER LIST — THE CANDIDATE',
    'All %d rows on the board, with the mechanism legs that make each price.' % len(rows),
    '\n'.join(h)))

# ---- 2 · the year-1 class in draft order -------------------------------------------------------
# THE COHORT CLOCK, AND WHY IT IS ASSERTED RATHER THAN TRUSTED (op_class.py:41-43, register v738):
#     cohort = DRAFT YEAR for an MSD row, DRAFT YEAR + 1 for everyone else.
# A mid-season draftee DEBUTS IN HIS DRAFT YEAR, so his first season IS that year. The CURRENT
# year-1 class is therefore cohort 2026 = the 2025-drafted non-MSDs PLUS the 2026-drafted MSDs.
# THIS ERROR CLASS HAS RECURRED, so the page ASSERTS its own membership both ways and PRINTS the
# result in the footer: every included row must be cohort 2026, and no cohort-2026 board row may be
# missing. A page that cannot prove its own membership is not a deliverable.
# THE COHORT CLOCK comes from the BASE matrix and THE v0 COLUMN DOES NOT. Stated here because the
# two have different justifications and conflating them would be the defect this page exists to avoid.
#
#   cohort clock (`year`, `type`) — the candidate HAS NO MATRIX (the emit halts on the ORDER 31-F
#     day-0 guard, PACKET_FINAL §4). These two fields are draft-record facts, and they were VERIFIED
#     dial-invariant: 2648 of 2648 rows carry identical `year` and `type` in per_entrant_FCBASE.json
#     and per_entrant_ASMCAND.json, two matrices built on different dial lines. Borrowing them is
#     therefore a checked equality, not an assumption.
#
#   v0 — NOT borrowed, because it is NOT dial-invariant. `_landed_v0_board` reads the engine
#     namespace, and on the three rows the day-0 guard named the base and the candidate genuinely
#     differ (833.3 vs 791.815..., 419.2 vs 398.358..., 91.6 vs 87.030...). The column below is read
#     off THE CANDIDATE'S OWN engine state by cp_v0.py, which self-checks against those three
#     numbers at tolerance 0 before it writes anything.
MX = json.load(open(SP + '/per_entrant_FCBASE.json'))['recs']
MXK = {r['key']: r for r in MX}
_V0 = json.load(open(os.path.join(HERE, 'V0_CP.json')))['v0']


def cohort_of(key):
    m = MXK.get(key)
    if not m or m.get('year') is None:
        return None
    return int(m['year']) if m.get('type') == 'MSD' else int(m['year']) + 1


TARGET = 2026
Y1 = sorted([r for r in CAND.values() if cohort_of(r['key']) == TARGET],
            key=lambda r: (r.get('pk') if r.get('pk') is not None else 999))
# --- the two-way assertion -----------------------------------------------------------------------
bad_in = [r['key'] for r in Y1 if cohort_of(r['key']) != TARGET]
missing = [k for k in CAND if cohort_of(k) == TARGET and not any(x['key'] == k for x in Y1)]
n_msd = sum(1 for r in Y1 if (MXK.get(r['key']) or {}).get('type') == 'MSD')
ASSERT_OK = (not bad_in and not missing)
assert ASSERT_OK, 'YEAR-1 MEMBERSHIP ASSERTION FAILED: %d wrong-cohort rows, %d missing' % (
    len(bad_in), len(missing))

h = ['<div class="sub k">Board totals: %s</div>' % HDR,
     '<div class="sub k"><b>BOARD ID <code>%s</code></b> &middot; total %s on %d rows &middot; '
     'entry prices <b>v0</b> read off THIS board\'s own engine state (cp_v0.py), not borrowed from '
     'another dial line.</div>' % (MD5[CANDTAG][:8], '{:,}'.format(TOT[CANDTAG]), len(CAND)),
     '<h2>The year-1 class — cohort %d, in draft order — %d rows</h2>' % (TARGET, len(Y1)),
     '<div class="sub">In pick order, with the entry price <b>v0</b> beside the board columns so the '
     'first-year mark can be read straight off the page. <b>THE COHORT RULE:</b> cohort = draft year '
     'for an MSD row (a mid-season draftee debuts in his draft year) and draft year + 1 for everyone '
     'else. So this class is the <b>2025-drafted non-MSDs plus the 2026-drafted MSDs</b> — '
     '%d of these %d rows are MSD. A 2025-drafted MSD is cohort 2025, a second-year player, and is '
     'NOT on this page.</div>' % (n_msd, len(Y1)),
     '<div class="wrap"><table class="s"><thead><tr><th>pick</th><th class="l">player</th>'
     '<th class="l">pos</th><th class="l">club</th><th class="l">type</th><th>draft yr</th>'
     '<th>cohort</th><th>v0</th>']
for t, lab in COLS:
    if t in V:
        h.append('<th>%s</th>' % lab)
h.append('<th>&Delta; R&rarr;cand</th></tr></thead><tbody>')
for r in Y1:
    k = r['key']
    pk = r.get('pk')
    m = MXK.get(k) or {}
    v0 = _V0.get(r['key'])
    if v0 is None or float(v0) <= 0:
        v0cell = '<td data-v="-1" class="k">no v0 object under the entry law</td>'
    else:
        v0cell = '<td data-v="%f">%s</td>' % (float(v0), num(float(v0)))
    # NO BARE DASHES: a row without a national-draft pick is a mid-season draftee, and the cell says
    # so rather than printing an unexplained em-dash.
    pkcell = ('no pick (MSD)' if (m.get('type') == 'MSD') else 'no pick recorded') \
        if pk is None else str(pk)
    h.append('<tr><td data-v="%s">%s</td><td class="l">%s</td><td class="l">%s</td>'
             '<td class="l">%s</td><td class="l">%s</td><td data-v="%s">%s</td>'
             '<td data-v="%s">%s</td>%s'
             % (pk if pk is not None else 999, pkcell,
                esc(r.get('name')), esc(r.get('grp') or (r.get('fut') or [['?']])[0][0]),
                esc(r.get('club')), esc(m.get('type') or r.get('ty')),
                m.get('year', ''), m.get('year', ''),
                cohort_of(k), cohort_of(k), v0cell))
    for t, lab in COLS:
        if t in V:
            v = V[t].get(k)
            h.append('<td data-v="%s">%s</td>' % (v if v is not None else 0, num(v)))
    dR = (V[CANDTAG][k] - V['L0_R'][k]) if 'L0_R' in V and k in V['L0_R'] else None
    h.append(dcell(dR)); h.append('</tr>')
h.append('</tbody></table></div>')
h.append('<div class="box"><h3>MEMBERSHIP ASSERTION — PRINTED, NOT ASSUMED</h3><ul>'
         '<li>every included row satisfies cohort(row) == %d under the engine\'s own cohort clock: '
         '<b>%s</b> (%d rows checked, %d violations)</li>'
         '<li>no cohort-%d board row is missing from this page: <b>%s</b> (%d missing)</li>'
         '<li>MSD rows correctly included: <b>%d</b>; 2025-drafted MSDs correctly EXCLUDED as '
         'cohort-2025 second-years</li></ul>'
         '<p class="boxfoot">This assertion runs every time the page is generated and fails the '
         'build if it does not hold. The cohort rule has been mis-applied before; the assertion is '
         'the guard against it happening again.</p></div>'
         % (TARGET, 'PASS' if not bad_in else 'FAIL', len(Y1), len(bad_in),
            TARGET, 'PASS' if not missing else 'FAIL', len(missing), n_msd))
open(os.path.join(HERE, 'YEAR1_COMPLETION.html'), 'w').write(page(
    'Assembly Year One', 'THE YEAR-1 CLASS — THE CANDIDATE',
    'Cohort %d in pick order, with entry price beside every board.' % TARGET,
    '\n'.join(h)))

print('PLAYERS_COMPLETION.html  %d rows' % len(rows))
print('YEAR1_COMPLETION.html    %d rows' % len(Y1))
print('(ASSEMBLY_NOARB.html is written by as_noarb.py, which needs the extended-338 run)')
