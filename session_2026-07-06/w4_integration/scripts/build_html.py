"""Build the self-contained W4 candidate BOARD + BOOK html (owner deliverable).
Reads the session out/ artifacts; emits session_2026-07-06/w4_integration/w4_board_book.html"""
import json, os, html, hashlib

BASE = '/home/user/afl-rl-engine/session_2026-07-06/w4_integration'
OUT = f'{BASE}/out'
REPO = '/home/user/afl-rl-engine'

def j(p, d=None):
    try:
        return json.load(open(p))
    except Exception:
        return d

board = j(f'{OUT}/board_final.json', [])                 # [{player,pos,age,nq,baked,now,...}]
attr = {t: j(f'{OUT}/attr_{t}.json', {}) for t in
        ['full', 'no_ruc', 'no_aging', 'no_v7form', 'no_kpf', 'no_fwdrecal', 'no_young', 'no_ovpx']}
ratio_c = j(f'{OUT}/ratio_candidate.json', {})
ratio_b = j(f'{OUT}/ratio_baked.json', {})
pvc = j(f'{REPO}/engine/rl_after/pvc_fit_candidate.json', {})
pvc0 = j(f'{OUT}/pvc_v34_baseline.json', {})
anchors = j(f'{OUT}/anchors_final.json', {})
guards = open(f'{OUT}/guards_summary.txt').read() if os.path.exists(f'{OUT}/guards_summary.txt') else '(guards summary pending)'
darcy = open(f'{OUT}/darcy_attribution.md').read() if os.path.exists(f'{OUT}/darcy_attribution.md') else ''
book_rows = j(f'{OUT}/book_cohort_rows.json', {})
meta = j(f'{OUT}/build_meta.json', {})

LEVERS = [('no_fwdrecal', 'L1 fwd-recal (credit+fade)'), ('no_young', 'L2 young runway'),
          ('no_ruc', 'L3 ruck (#44+headroom)'), ('no_aging', 'L4 aging decline (#45)'),
          ('no_v7form', 'L5 v7 form-conditioned'), ('no_kpf', 'L6 KPF treatment'),
          ('no_ovpx', 'L7 deep-pick compress')]

key2name = {r['key']: r for r in board}
full = attr['full']

def lever_delta(k):
    out = {}
    for tag, _lab in LEVERS:
        a = attr.get(tag, {}).get(k); f = full.get(k)
        out[tag] = (f - a) if (a is not None and f is not None) else None
    return out

rows_html = []
for r in sorted(board, key=lambda x: -(x['now'] or 0)):
    k = r['key']; d = lever_delta(k)
    dd = ''.join(f'<td class="n">{("%+.0f" % v) if v else "·"}</td>' for v in
                 (d[t] for t, _ in LEVERS))
    pct = 100 * (r['now'] - r['baked']) / r['baked'] if r['baked'] else 0
    cls = 'up' if pct > 0.5 else ('dn' if pct < -0.5 else '')
    rows_html.append(
        f'<tr><td>{html.escape(r["player"])}</td><td>{r["pos"]}</td><td class="n">{r["age"]:.0f}</td>'
        f'<td class="n">{r["nq"]}</td><td class="n">{r["baked"]:.0f}</td><td class="n"><b>{r["now"]:.0f}</b></td>'
        f'<td class="n {cls}">{pct:+.1f}%</td>{dd}</tr>')

anchor_rows = []
for nm, a in anchors.items():
    anchor_rows.append(f'<tr><td><b>{html.escape(nm)}</b></td><td>{a.get("role","")}</td>'
                       f'<td class="n">{a["baked"]}</td><td class="n"><b>{a["now"]}</b></td>'
                       f'<td class="n">{a["dpct"]}</td><td>{html.escape(a.get("read",""))}</td></tr>')

pvc_rows = []
if pvc.get('curve'):
    for k in [1, 2, 3, 5, 8, 10, 15, 20, 30, 45, 60, 80, 99]:
        v1 = pvc['curve'].get(str(k)); v0 = (pvc0 or {}).get(str(k))
        d = f'{100*(v1-v0)/v0:+.0f}%' if (v0 and v1) else ''
        pvc_rows.append(f'<tr><td class="n">{k}</td><td class="n">{v0 or ""}</td><td class="n"><b>{v1 or ""}</b></td><td class="n">{d}</td></tr>')

b1c = ratio_c.get('b1_avg', {}); b1b = ratio_b.get('b1_avg', {})
b1_html = '<tr><th>depth</th>' + ''.join(f'<th>d{n}</th>' for n in range(1, 8)) + '</tr>'
b1_html += '<tr><td>baked v2.5</td>' + ''.join(f'<td class="n">{b1b.get(str(n), b1b.get(n, 0)):.0f}</td>' for n in range(1, 8)) + '</tr>'
b1_html += '<tr><td><b>candidate</b></td>' + ''.join(f'<td class="n"><b>{b1c.get(str(n), b1c.get(n, 0)):.0f}</b></td>' for n in range(1, 8)) + '</tr>'

book_html = ''
if book_rows:
    book_html = '<tr><th>cohort</th>' + ''.join(f'<th>d{n}</th>' for n in range(1, 8)) + '</tr>'
    for C in sorted(book_rows):
        book_html += f'<tr><td>{C}</td>' + ''.join(
            f'<td class="n">{book_rows[C].get(str(n), "—")}</td>' for n in range(1, 8)) + '</tr>'

page = f"""<title>W4 integration candidate — board + book</title>
<style>
body{{font:14px/1.45 system-ui,sans-serif;margin:1.2em auto;max-width:1200px;padding:0 1em;color:#1a1d21}}
@media (prefers-color-scheme: dark){{body{{background:#14171a;color:#dfe3e8}} table td,table th{{border-color:#333}} .tag{{background:#2a2e33}}}}
h1{{font-size:1.35em}} h2{{font-size:1.1em;margin-top:1.6em}}
table{{border-collapse:collapse;width:100%;font-size:12.5px}}
td,th{{border:1px solid #ccc;padding:3px 7px;text-align:left}}
td.n{{text-align:right;font-variant-numeric:tabular-nums}}
.up{{color:#0a7d33}} .dn{{color:#b0332a}}
.tag{{background:#eef1f4;border-radius:4px;padding:2px 8px;font-size:12px;display:inline-block;margin:2px 4px 2px 0}}
.wrap{{overflow-x:auto}} pre{{white-space:pre-wrap;font-size:12px;background:rgba(127,127,127,.08);padding:.8em;border-radius:6px}}
.state{{border:2px solid #b0332a;color:#b0332a;font-weight:700;padding:.5em .8em;border-radius:6px;margin:.8em 0}}
</style>
<h1>WAVE-4 INTEGRATION — candidate board + book</h1>
<div class="state">STATE: CANDIDATE — W4 multi-lever integration (engine {meta.get('head','?')} on baked v2.5 store e1b4d8bf) — NOT BAKED, NOT PROMOTED. Rides to the cold audit → owner word → re-bake.</div>
<div>
<span class="tag">store e1b4d8bf (untouched)</span><span class="tag">base: BAKED v2.5 efea88e5</span>
<span class="tag">cohort ratio {ratio_c.get('ratio',0):.1f}% (baked {ratio_b.get('ratio',0):.1f}%, hard ≤130)</span>
<span class="tag">board pool {meta.get('pool_delta','?')}</span>
<span class="tag">{meta.get('n_movers','?')} movers / {meta.get('n_players','?')} players</span>
</div>

<h2>Owner anchors — before → after</h2>
<div class="wrap"><table>
<tr><th>player</th><th>anchor role</th><th>baked v2.5</th><th>candidate</th><th>Δ</th><th>read</th></tr>
{''.join(anchor_rows)}
</table></div>

<h2>Cohort no-arbitrage (walk-forward book, aggregate 2004-2020) + B1 shape</h2>
<p>Aggregate avg-year-4-6 / avg-year-1-2: <b>{ratio_c.get('ratio',0):.1f}%</b> (baked {ratio_b.get('ratio',0):.1f}%; HARD ≤130%, guide 120–125%). B1 cross-cohort average (indexed yr1=100):</p>
<div class="wrap"><table>{b1_html}</table></div>

<h2>Guards</h2>
<pre>{html.escape(guards)}</pre>

<h2>Sam Darcy — three-locus attribution</h2>
<pre>{html.escape(darcy)}</pre>

<h2>Pick-value curve (PVC fit, downstream — candidate)</h2>
<p>Fitted from the candidate book's year-1 anchors ({pvc.get('n_anchors','?')} ND anchors, {html.escape(str(pvc.get('window','')))}); monotone; pick-1 anchored 3000. Picks re-price; players do <b>not</b> read the fit back (draftval frozen on v3.4 — no circularity).</p>
<div class="wrap"><table><tr><th>pick</th><th>v3.4 (baked)</th><th>fitted</th><th>Δ</th></tr>{''.join(pvc_rows)}</table></div>

<h2>Full candidate board — per-lever attribution (leave-one-out Δ = full − without-lever)</h2>
<div class="wrap"><table>
<tr><th>player</th><th>pos</th><th>age</th><th>nq</th><th>baked</th><th>candidate</th><th>Δ%</th>
{''.join(f'<th>{lab.split(" ")[0]}</th>' for _t, lab in LEVERS)}</tr>
{''.join(rows_html)}
</table></div>
<p>Levers: {' · '.join(lab for _t, lab in LEVERS)} · L8 PVC fit (picks only — table above)</p>

<h2>Walk-forward book — per-cohort indexed curves (candidate)</h2>
<div class="wrap"><table>{book_html}</table></div>
"""
open(f'{BASE}/w4_board_book.html', 'w').write(page)
print('wrote', f'{BASE}/w4_board_book.html', len(page), 'bytes')
