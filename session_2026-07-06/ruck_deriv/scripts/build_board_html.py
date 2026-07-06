#!/usr/bin/env python3
# Self-contained HTML board from the authoritative rl_app_data.json (the canonical rl_build_html.py app cannot
# be rebuilt — 6 of its 8 front-end partials are untracked/absent). Ruck-focused: RUC default view, before->after
# deltas merged from the frozen OLD-engine snapshot. No external deps (data + CSS + JS inlined).
import json, sys, html
BOARD = sys.argv[1]           # data/rl_build/rl_app_data.json (NEW)
BASE  = sys.argv[2]           # base_old.json (OLD board values, keyed name|year|pick)
OUT   = sys.argv[3]
d = json.load(open(BOARD)); active = d.get('active') or d
base = json.load(open(BASE))
def bkey(name, yr, pk): return f"{name}|{yr}|{pk}"
rows = []
for p in active:
    k = bkey(p['name'], p.get('yr'), p.get('pk'))
    old = base.get(k, {}).get('v')
    track = [t.get('a') for t in (p.get('track') or [])]
    rows.append(dict(name=p['name'], grp=p.get('grp'), pk=p.get('pk'), age=p.get('age'),
                     v=p.get('v'), old=old, track=track))
rows.sort(key=lambda r: -(r['v'] or 0))
DATA = json.dumps(rows, separators=(',',':'))

STYLE = """
*{box-sizing:border-box} body{margin:0;font:14px/1.45 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#e8eaf0;background:#0f1420}
.wrap{max-width:1080px;margin:0 auto;padding:24px 18px 80px}
h1{font-size:22px;margin:0 0 4px} .sub{color:#9aa4bd;font-size:13px;margin:0 0 18px}
.card{background:#161d2e;border:1px solid #232c42;border-radius:12px;padding:14px 16px;margin:0 0 16px}
.anchors{display:flex;flex-wrap:wrap;gap:10px;margin:0 0 16px}
.anchor{background:#161d2e;border:1px solid #232c42;border-radius:10px;padding:10px 14px;min-width:150px}
.anchor .n{font-size:12px;color:#9aa4bd} .anchor .val{font-size:20px;font-weight:600}
.up{color:#4ade80} .dn{color:#f87171} .flat{color:#9aa4bd}
.controls{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 12px}
button{background:#1c2436;color:#c7d0e6;border:1px solid #2c3752;border-radius:20px;padding:6px 14px;cursor:pointer;font-size:13px}
button.on{background:#3b5bdb;color:#fff;border-color:#3b5bdb}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
th,td{text-align:right;padding:7px 9px;border-bottom:1px solid #202940;white-space:nowrap}
th{color:#8b96b3;font-weight:500;font-size:12px;text-transform:uppercase;letter-spacing:.03em;cursor:pointer;position:sticky;top:0;background:#0f1420}
td.l,th.l{text-align:left} tr.ruc{background:#17233a} tr.ruc td.l{font-weight:600}
.spark{color:#7c88a8;font-size:11px} .tag{display:inline-block;font-size:10px;padding:1px 6px;border-radius:6px;background:#26314d;color:#9fb0d6;margin-left:6px}
.d{font-size:12px}
"""

SCRIPT = """
const D=__DATA__;
const POS=['ALL','RUC','MID','KEY_FWD','KEY_DEF','GEN_FWD','GEN_DEF'];
let cur='RUC', sortKey='v', sortDir=-1;
const el=document.getElementById('tbody'), ctr=document.getElementById('ctr');
POS.forEach(p=>{const b=document.createElement('button');b.textContent=p;b.onclick=()=>{cur=p;draw();};b.dataset.p=p;ctr.appendChild(b);});
function fmt(v){return v==null?'—':v.toLocaleString();}
function draw(){
  [...ctr.children].forEach(b=>b.classList.toggle('on',b.dataset.p===cur));
  let r=D.filter(x=>cur==='ALL'||x.grp===cur);
  r.sort((a,b)=>{let x=a[sortKey],y=b[sortKey];x=x==null?-1:x;y=y==null?-1:y;return (x<y?-1:x>y?1:0)*sortDir;});
  el.innerHTML=r.map((x,i)=>{
    const d=(x.old!=null)?x.v-x.old:null;
    const dc=d==null?'':d>0?'up':d<0?'dn':'flat';
    const ds=d==null?'':(d>0?'+':'')+d;
    const spark=(x.track||[]).slice(-6).map(a=>a==null?'·':Math.round(a)).join(' ');
    return `<tr class="${x.grp==='RUC'?'ruc':''}"><td>${i+1}</td><td class="l">${x.name}${x.grp==='RUC'?'<span class=tag>RUC</span>':''}</td><td class="l">${x.grp||''}</td><td>${x.pk??'—'}</td><td>${x.age??'—'}</td><td>${fmt(x.old)}</td><td><b>${fmt(x.v)}</b></td><td class="d ${dc}">${ds}</td><td class="l spark">${spark}</td></tr>`;
  }).join('');
}
document.querySelectorAll('th[data-k]').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sortKey===k)sortDir*=-1;else{sortKey=k;sortDir=(k==='name'||k==='grp')?1:-1;}draw();});
draw();
"""

def anchor(name, yr, pk):
    for p in active:
        if p['name'] == name:
            k = bkey(p['name'], p.get('yr'), p.get('pk')); old = base.get(k, {}).get('v')
            v = p.get('v'); d = (v-old) if old is not None else None
            cls = 'flat' if not d else ('up' if d>0 else 'dn')
            ds = '' if d is None else f" <span class='{cls}'>({'+' if d>0 else ''}{d})</span>"
            return f"<div class='anchor'><div class='n'>{html.escape(name)} · pick {p.get('pk')}</div><div class='val'>${v}{ds}</div><div class='n'>was ${old}</div></div>"
    return ''

body = f"""<div class="wrap">
<h1>AFL RL Board — ruck values derived off production</h1>
<p class="sub">Candidate BATCH2 (2026-07-06) · store e1b4d8bf · single lever: ruck production leg re-priced off production (HEAD 0.80 × standardized production price at the median ruck slot). Only rucks moved (7); every non-ruck byte-identical. Cross-position check is SANITY only — not a locked calibration.</p>
<div class="anchors">{anchor('Louis Emmett',None,None)}{anchor('Nicholas Naitanui',None,None)}{anchor('Luke Jackson',None,None)}{anchor('Max Gawn',None,None)}</div>
<div class="controls" id="ctr"></div>
<div class="card" style="padding:0;overflow-x:auto">
<table><thead><tr>
<th>#</th><th class="l" data-k="name">Player</th><th class="l" data-k="grp">Pos</th><th data-k="pk">Pick</th><th data-k="age">Age</th><th data-k="old">Old $</th><th data-k="v">$ (new)</th><th>Δ</th><th class="l">Production (last 6 avg)</th>
</tr></thead><tbody id="tbody"></tbody></table>
</div>
<p class="sub">RUC rows shaded. Δ = new − old (blank for non-rucks, which are byte-identical). Click a column header to sort; use the chips to filter by position.</p>
</div>"""

doc = ("<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
       "<title>AFL RL Board — ruck values derived</title><style>" + STYLE + "</style></head><body>"
       + body + "<script>" + SCRIPT.replace('__DATA__', DATA) + "</script></body></html>")
open(OUT, 'w').write(doc)
print("wrote", OUT, "| players:", len(rows), "| bytes:", len(doc))
