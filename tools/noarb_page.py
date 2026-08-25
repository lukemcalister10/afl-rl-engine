#!/usr/bin/env python3
"""tools/noarb_page.py — the owner-facing no-arb review page, from the class-reading JSON.

    python3 tools/noarb_page.py CLASS_JSON -o OUT.html \
        [--live-key ARM2LIVE --cand-key ARM2CAND] \
        [--live-label "live board 82fcd8bb"] [--cand-label "candidate"] \
        [--movers PRED.json BASE_BOARD.json WITH_BOARD.json LIVE_BOARD.json] \
        [--note "free-text caveat line"]

Reads the arm2_noarb_class.py output (two labeled readings + `_reading` summary) and renders the
per-class table with rail/floor highlighting, the summary strip, and (optionally) the act's mover
table with live / base / with-lever columns. Built for ORDER 45 (owner ask, 2026-08-25: "There
should be a script/template for the no arb table"); reusable for any future class reading."""
import argparse
import json
from string import Template

TPL = Template('''<meta charset="utf-8"><title>No-Arb Reading — $cand_label</title>
<style>
body{font-family:system-ui,sans-serif;max-width:960px;margin:24px auto;padding:0 16px;background:#fafafa;color:#1a1a1a}
h1{font-size:1.35rem}h2{font-size:1.05rem;margin-top:28px}
table{border-collapse:collapse;width:100%;background:#fff;font-variant-numeric:tabular-nums}
th,td{border:1px solid #ddd;padding:5px 9px;text-align:right}
th{background:#f0f0f0;cursor:pointer}td:first-child,th:first-child{text-align:left}
.breach{background:#fde8e8;font-weight:600}.under{background:#fff7e0}
.strip{display:flex;gap:14px;flex-wrap:wrap;margin:14px 0}
.card{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px 14px}
.card b{font-size:1.05rem}.ok{color:#166534}.bad{color:#9a3412}
p.note{color:#444;font-size:.92rem;line-height:1.45}
</style>
<h1>No-arbitrage reading — $cand_label</h1>
<p class="note">The reading asks, per draft-class year: what a class&rsquo;s players are now worth against
what was paid for them. The <b>buy rail is $rail</b> — a class at or over it is priced as a systematic
bargain, which the law treats as an arbitrage smell. The <b>floor is $floor</b>.</p>
<div class="strip">
<div class="card">headline (W2)<br><b>$w2l → $w2c</b> <span class="$w2cls">$w2word</span></div>
<div class="card">worst class<br><b>$mxl ($mxly) → $mxc ($mxcy)</b></div>
<div class="card">classes over the buy rail<br><b>$nl → $nc</b> <span class="$brcls">$brword</span></div>
<div class="card">floor margin<br><b>$fm</b></div>
</div>
<h2>Per draft class</h2>
<table><tr><th>class year</th><th>$live_label</th><th>$cand_label</th><th>move</th></tr>
$yr_rows</table>
<p class="note">⚠ red cells sit at/over the $rail buy rail; amber cells sit under the $floor floor.</p>
$movers_html
$note_html
<script>
document.querySelectorAll('table').forEach(t=>t.querySelectorAll('th').forEach((h,i)=>h.onclick=()=>{
const rs=[...t.rows].slice(1);const num=rs.every(r=>!isNaN(parseFloat(r.cells[i].innerText)));
const asc=h.asc=!h.asc;rs.sort((a,b)=>{let x=a.cells[i].innerText,y=b.cells[i].innerText;
if(num){x=parseFloat(x);y=parseFloat(y)}return (x>y?1:x<y?-1:0)*(asc?1:-1)});rs.forEach(r=>t.appendChild(r))}));
</script>''')


def cell(v, rail, floor):
    if v is None:
        return '<td>—</td>'
    cls = ' class="breach"' if v >= rail else (' class="under"' if v < floor else '')
    return '<td%s>%.4f%s</td>' % (cls, v, ' ⚠' if v >= rail else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('class_json')
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--live-key', default='ARM2LIVE')
    ap.add_argument('--cand-key', default='ARM2CAND')
    ap.add_argument('--live-label', default='live board')
    ap.add_argument('--cand-label', default='candidate board')
    ap.add_argument('--movers', nargs=4, metavar=('PRED', 'BASE', 'WITH', 'LIVE'),
                    help='NET_PREDICTION-style movers json + base/with/live board jsons')
    ap.add_argument('--note', default='')
    a = ap.parse_args()

    d = json.load(open(a.class_json))
    L, C, R = d[a.live_key], d[a.cand_key], d['_reading']
    rail, floor = R['rail'], R['floor']
    years = sorted(set(L['per_class']) | set(C['per_class']))
    yr_rows = '\n'.join(
        '<tr><td>%s</td>%s%s<td>%+.4f</td></tr>'
        % (y, cell(L['per_class'].get(y), rail, floor), cell(C['per_class'].get(y), rail, floor),
           C['per_class'][y] - L['per_class'][y])
        for y in years if y in L['per_class'] and y in C['per_class'])

    movers_html = ''
    if a.movers:
        pred = json.load(open(a.movers[0]))['movers']
        vals = lambda p: {r['key']: r['v'] for r in json.load(open(p))['active']}
        base, withb, liveb = vals(a.movers[1]), vals(a.movers[2]), vals(a.movers[3])
        rows = '\n'.join(
            '<tr><td>%s</td><td>%s</td><td>%d</td><td>%.1f</td><td>%s</td><td>%s</td><td><b>%s</b></td><td>%+d</td></tr>'
            % (m['player'], m['pos'], m['tenure'], m['cameo'], liveb.get(m['key']),
               base.get(m['key']), withb.get(m['key']), withb[m['key']] - base[m['key']])
            for m in pred)
        movers_html = ('<h2>The act&rsquo;s movers</h2>'
                       '<table><tr><th>player</th><th>pos</th><th>tenure</th><th>cameo avg</th>'
                       '<th>live today</th><th>base</th><th>with lever</th><th>lift</th></tr>%s</table>' % rows)

    nl, nc = R['classes_over_rail_live'], R['classes_over_rail_candidate']
    html = TPL.substitute(
        rail='%.2f' % rail, floor='%.2f' % floor,
        live_label=a.live_label, cand_label=a.cand_label,
        w2l='%.4f' % L['w2'], w2c='%.4f' % C['w2'],
        w2cls='ok' if C['w2'] <= L['w2'] else 'bad',
        w2word='improved' if C['w2'] < L['w2'] else ('unchanged' if C['w2'] == L['w2'] else 'WORSE'),
        mxl='%.4f' % L['max_class'], mxly=L['max_class_year'],
        mxc='%.4f' % C['max_class'], mxcy=C['max_class_year'],
        nl=nl, nc=nc,
        brcls='ok' if R['new_breaches'] == 0 else 'bad',
        brword='no new breaches' if R['new_breaches'] == 0 else '%d NEW BREACHES' % R['new_breaches'],
        fm='%+.4f vs %.2f' % (C['w2'] - floor, floor),
        yr_rows=yr_rows, movers_html=movers_html,
        note_html=('<p class="note">%s</p>' % a.note) if a.note else '')
    open(a.out, 'w').write(html)
    print('wrote %s (%d bytes, %d classes%s)' % (a.out, len(html), len(years),
          ', movers table on' if a.movers else ''))


if __name__ == '__main__':
    main()
