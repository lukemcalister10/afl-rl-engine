#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — THE TWO PREVIEW PAGES (the standing presentation ruling: the owner
reads raw data; self-contained sortable HTML, house conventions per order32_s6/S6_LOTTERY_DIAL.html).

  PREVIEW_32_PLAYERS.html  the full player table: rank, player, pathway, pos, games,
                           Live · Candidate 31 · Candidate 32, deltas vs both, every column sortable.
  PREVIEW_32_YEAR1.html    the year-1 class in DRAFT ORDER (ND by pick, then RD, pathways, SSP,
                           MSD): Live · Candidate 31 · Candidate 32 PLUS v0.

Data: docs/ledgers/CANDIDATE_32_MOVERS.json — the composed ledger, nothing recomputed here.
"""
import json, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
J = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_32_MOVERS.json')))
ROWS = J['rows']
T = J['totals']
B = J['boards']

CSS = """
:root{--pitch:#0a0c10;--card:#12151c;--card-2:#181c25;--edge:#232936;--edge-2:#2f3747;
--text:#f2f5f9;--dim:#8b95a6;--faint:#525c6d;--volt:#c8f04a;--volt-soft:rgba(200,240,74,.12);
--up:#4ade80;--dn:#f0655e;--warn:#f5b445;
--cond:"Arial Narrow","Helvetica Neue Condensed","Roboto Condensed",Arial,sans-serif;
--sans:"Helvetica Neue",Arial,sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
*{box-sizing:border-box}
body{margin:0;background:var(--pitch);color:var(--text);font-family:var(--sans);font-size:13px;line-height:1.45}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
.banner{background:var(--volt-soft);border-bottom:1px solid var(--volt);color:var(--volt);
font-family:var(--cond);font-size:11px;letter-spacing:.2em;text-transform:uppercase;text-align:center;
padding:7px 12px;font-weight:700}
.app{max-width:1500px;margin:0 auto;padding:0 18px 80px}
header{display:flex;align-items:flex-end;gap:18px;flex-wrap:wrap;padding:22px 0 14px}
.brand{font-family:var(--cond);font-weight:900;font-size:38px;letter-spacing:.01em;text-transform:uppercase;line-height:.92}
.brand b{color:var(--volt)}
.brand .sub{display:block;font-size:10.5px;letter-spacing:.28em;color:var(--dim);font-weight:700;margin-top:6px}
.spacer{flex:1}
.stamp{font-family:var(--mono);font-size:10.5px;color:var(--dim);text-align:right;line-height:1.75}
.stamp b{color:var(--text)}
h2{font-family:var(--cond);font-weight:700;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--faint);margin:0 0 10px}
.box{background:var(--card);border:1px solid var(--edge);padding:16px 18px;margin:12px 0}
.box.warn{border-color:var(--warn);border-left:4px solid var(--warn)}
.box.warn h2{color:var(--warn)}
table{border-collapse:collapse;width:100%;font-size:12px}
th{font-family:var(--cond);font-weight:700;font-size:10px;letter-spacing:.14em;text-transform:uppercase;
color:var(--dim);text-align:right;padding:6px 8px;border-bottom:1px solid var(--edge-2);cursor:pointer;
position:sticky;top:0;background:var(--card);white-space:nowrap;user-select:none}
th.l,td.l{text-align:left}
th:hover{color:var(--volt)}
th.sorted{color:var(--volt)}
td{padding:4px 8px;border-bottom:1px solid var(--edge);text-align:right}
tr:hover td{background:var(--card-2)}
td.up{color:var(--up)}td.dn{color:var(--dn)}
.k{color:var(--dim)}
.sec{font-family:var(--cond);font-weight:700;font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--volt);padding-top:16px}
.note{color:var(--dim);font-size:11.5px;margin-top:8px}
"""

SORT_JS = """
function sortTable(tid, col, numeric){
  var tb=document.getElementById(tid).tBodies[0];
  var rows=Array.prototype.slice.call(tb.rows).filter(function(r){return !r.classList.contains('sechead')});
  var th=document.getElementById(tid).tHead.rows[0].cells[col];
  var dir=th.dataset.dir==='asc'?'desc':'asc';
  var ths=document.getElementById(tid).tHead.rows[0].cells;
  for(var i=0;i<ths.length;i++){ths[i].classList.remove('sorted');ths[i].dataset.dir='';}
  th.classList.add('sorted');th.dataset.dir=dir;
  rows.sort(function(a,b){
    var x=a.cells[col].dataset.v!==undefined?a.cells[col].dataset.v:a.cells[col].textContent;
    var y=b.cells[col].dataset.v!==undefined?b.cells[col].dataset.v:b.cells[col].textContent;
    if(numeric){x=parseFloat(x)||-1e18;y=parseFloat(y)||-1e18;return dir==='asc'?x-y:y-x;}
    return dir==='asc'?String(x).localeCompare(String(y)):String(y).localeCompare(String(x));
  });
  rows.forEach(function(r){tb.appendChild(r);});
}
"""


def delta_td(v):
    if v is None:
        return '<td class="k">—</td>'
    cls = 'up' if v > 0 else ('dn' if v < 0 else '')
    return '<td class="num %s" data-v="%d">%+d</td>' % (cls, v, v)


def page_head(title, sub, banner):
    return ('<!doctype html>\n<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<title>%s</title>\n<style>%s</style>\n'
            '<div class="banner">%s</div>\n<div class="app">\n'
            '<header><div class="brand">CANDIDATE <b>32</b><span class="sub">%s</span></div>'
            '<div class="spacer"></div>'
            '<div class="stamp">live <b>88ce647f</b> %d · candidate 31 <b>fe6be9d6</b> %d<br>'
            'candidate 32 <b>%s</b> <b>%d</b> · store cb38ef11 · PRE-NUMERAIRE</div></header>\n'
            % (title, CSS, banner, sub, T['live'], T['c31'], B['candidate32'][:8], T['candidate32']))


# ================= PAGE 1: the full player table ==================================================
rows_sorted = sorted(ROWS, key=lambda r: -r['cand'])
H = [page_head('Candidate 32 · The Board', 'ORDER A · THE FULL PLAYER TABLE',
               'NOTHING LANDS WITHOUT THE OWNER\'S WORD — PREVIEW OF A CANDIDATE, PRE-NUMERAIRE, F2 LEVEL QUESTION OPEN')]
H.append('<div class="box"><h2>All %d priced rows · click any column to sort · deltas vs BOTH baselines</h2>' % len(rows_sorted))
H.append('<table id="t1"><thead><tr>')
cols = [('#', True), ('player', False), ('path', False), ('pos', False), ('g', True),
        ('live', True), ('cand 31', True), ('cand 32', True), ('Δ live', True), ('Δ c31', True),
        ('bars', True), ('credit', True), ('reset', True), ('refit', True), ('relief', True), ('re-mix', True)]
for i, (nm, num) in enumerate(cols):
    H.append('<th class="%s" onclick="sortTable(\'t1\',%d,%s)">%s</th>'
             % ('l' if nm in ('player', 'path', 'pos') else '', i, 'true' if num else 'false', nm))
H.append('</tr></thead><tbody>')
for i, r in enumerate(rows_sorted):
    H.append('<tr><td class="num k" data-v="%d">%d</td><td class="l">%s</td><td class="l k">%s</td>'
             '<td class="l k">%s</td><td class="num" data-v="%d">%d</td>'
             % (i + 1, i + 1, html.escape(r['name'] or r['key']), r['pathway'] or '?', r['pos'], int(r['g']), int(r['g'])))
    H.append('<td class="num" data-v="%s">%s</td>' % (r['live'] if r['live'] is not None else '', r['live'] if r['live'] is not None else '—'))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['c31'], r['c31']))
    H.append('<td class="num" data-v="%d"><b>%d</b></td>' % (r['cand'], r['cand']))
    H.append(delta_td(r['d_vs_live']))
    H.append(delta_td(r['d_vs_c31']))
    for leg in ('leg_bars', 'leg_credit', 'leg_reset', 'leg_refit', 'leg_relief', 'leg_remix'):
        H.append(delta_td(r[leg]))
    H.append('</tr>')
H.append('</tbody></table>')
H.append('<div class="note">Legs are REAL BOARD DELTAS from the cumulative stage ladder '
         '(bars → +credit → +reset → +Φ refit → +relief → +re-mix); their sum is Δ vs Candidate 31 exactly. '
         'Board totals: live %d · step-2 %d · C31 %d · C32 %d.</div></div>' % (T['live'], T['step2'], T['c31'], T['candidate32']))
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'PREVIEW_32_PLAYERS.html'), 'w').write('\n'.join(H))

# ================= PAGE 2: the year-1 class, draft order ==========================================
Y1 = [r for r in ROWS if (r['yr'] == 2025) or (r['yr'] == 2026 and r['pathway'] == 'MSD')]
PATH_ORDER = {'ND': 0, 'RD': 1, 'PDA': 2, 'PDN': 3, 'PDS': 4, 'IRE': 5, 'UNR': 6, 'SSP': 7, 'MSD': 8}


def draft_key(r):
    return (PATH_ORDER.get(r['pathway'], 9), r['pick'] if r['pick'] is not None else 999, r['key'])


Y1.sort(key=draft_key)
H = [page_head('Candidate 32 · Year-1 Class', 'ORDER A · THE YEAR-1 CLASS · DRAFT ORDER',
               'NOTHING LANDS WITHOUT THE OWNER\'S WORD — THE CLASS-LEVEL (+6.7 TO +8.4 PT) QUESTION IS HALTED TO THE OWNER (F2)')]
H.append('<div class="box warn"><h2>The level, read before the table</h2>'
         '<div class="note">The W2-fair year-1 class mark is ~1.10–1.11. Candidate 32 marks the class at '
         '1.0334 (walk-forward 2005–15 mean) — the mechanisms and the re-mix close the MIX '
         '(W 0.068→0.091, slope 0.97) but the LEVEL residual is uniform by the shares identity and is '
         'HALTED to the owner (RESIDUAL_32.json): no silent lift. The rows below are the candidate as '
         'built.</div></div>')
H.append('<div class="box"><h2>Year-1 class (2025 entrants + 2026 mid-season) · draft order · %d rows</h2>' % len(Y1))
H.append('<table id="t2"><thead><tr>')
cols = [('order', True), ('player', False), ('path', False), ('pick', True), ('pos', False), ('g', True),
        ('v0', True), ('live', True), ('cand 31', True), ('cand 32', True), ('Δ live', True), ('Δ c31', True)]
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
    H.append('<td class="num" data-v="%s">%s</td>' % (r['live'] if r['live'] is not None else '', r['live'] if r['live'] is not None else '—'))
    H.append('<td class="num" data-v="%d">%d</td>' % (r['c31'], r['c31']))
    H.append('<td class="num" data-v="%d"><b>%d</b></td>' % (r['cand'], r['cand']))
    H.append(delta_td(r['d_vs_live']))
    H.append(delta_td(r['d_vs_c31']))
    H.append('</tr>')
H.append('</tbody></table>')
H.append('<div class="note">Draft order: ND by pick, then RD, pathway routes (PDA/PDN/PDS/IRE/UNR), SSP, MSD '
         '(MSD 2026 = this season\'s mid-season class, its entry season IS season 1 by owner ruling 5). '
         'v0 = the row\'s own day-0 entry object (board currency, the 31-F head-fixed surface — untouched '
         'by this candidate). Every column sortable; the default order is the draft order.</div></div>')
H.append('<script>%s</script></div>' % SORT_JS)
open(os.path.join(HERE, 'PREVIEW_32_YEAR1.html'), 'w').write('\n'.join(H))
print('written: PREVIEW_32_PLAYERS.html (%d rows) / PREVIEW_32_YEAR1.html (%d rows)' % (len(rows_sorted), len(Y1)))
