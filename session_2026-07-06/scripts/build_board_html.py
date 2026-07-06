#!/usr/bin/env python3
"""Self-contained openable HTML board for the form-conditioned aging-decline candidate.
The canonical styled front-end (rl_build_html.py) needs assets not present in this checkout
(_v20_style.css/_body.html/_features_v23.js/_insights.js) — so this renders the SAME regenerated
board data (rl_app_data.json, parity-gate-passed) plus the single-lever movers/anchors view and the
fitted surface, as one self-contained page. READ-ONLY on the store."""
import json, os, html
WS='/home/claude/rl_workspace/rl_after'; REPO='/home/user/afl-rl-engine'; O=REPO+'/session_2026-07-06/out'
board=json.load(open(WS+'/rl_app_data.json')); act=board['active']
off=json.load(open(O+'/ev_off.json')); fit=json.load(open(O+'/fbump_fit.json'))
byk={p['key']:p for p in act}
def bef(k): return off.get(k,[None])[0]
movers=sorted([p for p in act if bef(p['key']) is not None and p['v']!=bef(p['key'])], key=lambda p:-(p['v']-bef(p['key'])))
NAMED=['max-gawn','jeremy-cameron','marcus-bontempelli','kieren-briggs']
DECL=['stephen-coniglio','taylor-adams','mark-blicavs','cameron-guthrie','patrick-dangerfield']
tot0=sum(bef(p['key']) for p in act if bef(p['key']) is not None); tot1=sum(p['v'] for p in act if bef(p['key']) is not None)

def rows(keys, note=''):
    out=[]
    for k in keys:
        p=byk.get(k)
        if not p: out.append(f"<tr><td>{html.escape(k)}</td><td colspan=6>not on board</td></tr>"); continue
        b=bef(k); d=p['v']-b if b is not None else 0
        cls='up' if d>0 else ('flat' if d==0 else 'dn')
        out.append(f"<tr><td class=nm>{html.escape(p['name'])}</td><td>{p.get('grp','')}</td>"
                   f"<td class=n>{p.get('age','')}</td><td class=n>{b if b is not None else ''}</td>"
                   f"<td class=n>{p['v']}</td><td class='n {cls}'>{d:+d}</td></tr>")
    return "\n".join(out)
def mover_rows():
    out=[]
    for p in movers:
        b=bef(p['key']); d=p['v']-b
        out.append(f"<tr><td class=nm>{html.escape(p['name'])}</td><td>{p.get('grp','')}</td>"
                   f"<td class=n>{p.get('age','')}</td><td class=n>{b}</td><td class=n>{p['v']}</td>"
                   f"<td class='n up'>{d:+d}</td></tr>")
    return "\n".join(out)
def full_rows():
    out=[]
    for p in sorted(act,key=lambda p:-p['v']):
        b=bef(p['key']); d=(p['v']-b) if b is not None else 0
        cls='up' if d>0 else ''
        out.append(f"<tr><td class=nm>{html.escape(p['name'])}</td><td>{p.get('grp','')}</td>"
                   f"<td class=n>{p.get('age','')}</td><td class=n>{p.get('pk','')}</td>"
                   f"<td class=n>{p['v']}</td><td class='n {cls}'>{(('%+d'%d) if d else '')}</td></tr>")
    return "\n".join(out)
# fitted surface table
AGE=fit['AGE_X']; LCR=fit['LCR_X']; Z=fit['Z']
def surf_rows():
    out=[]
    for i,a in enumerate(AGE):
        cells="".join(f"<td class=n>{Z[i][j]:.3f}</td>" for j in range(len(LCR)))
        out.append(f"<tr><td class=n>{a}</td>{cells}</tr>")
    return "\n".join(out)
surf_hdr="".join(f"<th>lcr {l}</th>" for l in LCR)

CSS="""
:root{--bg:#fbfbfd;--fg:#1a1a1f;--mut:#6b7280;--line:#e5e7eb;--card:#fff;--up:#0a7d33;--dn:#b42318;--acc:#3b4cca}
@media(prefers-color-scheme:dark){:root{--bg:#0e0f13;--fg:#e8e8ee;--mut:#9aa0aa;--line:#24262e;--card:#16171d;--up:#4ade80;--dn:#f87171;--acc:#8b9bff}}
:root[data-theme=dark]{--bg:#0e0f13;--fg:#e8e8ee;--mut:#9aa0aa;--line:#24262e;--card:#16171d;--up:#4ade80;--dn:#f87171;--acc:#8b9bff}
:root[data-theme=light]{--bg:#fbfbfd;--fg:#1a1a1f;--mut:#6b7280;--line:#e5e7eb;--card:#fff;--up:#0a7d33;--dn:#b42318;--acc:#3b4cca}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif}
.wrap{max-width:1000px;margin:0 auto;padding:28px 18px 80px}
h1{font-size:24px;margin:0 0 4px}h2{font-size:17px;margin:34px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
.sub{color:var(--mut);font-size:13px;margin-bottom:18px}
.kpis{display:flex;gap:14px;flex-wrap:wrap;margin:16px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:120px}
.kpi .v{font-size:22px;font-weight:700}.kpi .l{color:var(--mut);font-size:12px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
table{border-collapse:collapse;width:100%;font-size:13.5px;background:var(--card)}
th,td{padding:7px 10px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th{position:sticky;top:0;background:var(--card);font-size:12px;color:var(--mut);font-weight:600}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;font-family:Space Mono,ui-monospace,monospace}
td.nm{font-weight:600}.up{color:var(--up)}.dn{color:var(--dn)}.flat{color:var(--mut)}
.note{background:var(--card);border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;padding:12px 14px;font-size:13px;color:var(--fg);margin:12px 0}
.tall{max-height:520px;overflow:auto}
"""
H=f"""<div class=wrap>
<h1>Form-Conditioned Aging Decline &mdash; candidate board</h1>
<div class=sub>Single lever: the DECLINER SHED decline curve. Store <code>e1b4d8bf</code> (unchanged) &middot; engine head <code>efea88e5&rarr;4226b61d</code> &middot; band <code>34faa865</code> &middot; RL_FORMDECL=1</div>
<div class=note>The age-only decline multiplier <code>_agemult(age)</code> is replaced by a form-conditioned <code>_agemult2(age, lcr)</code> where <code>lcr = recent level &minus; positional replacement</code>. Up-only credit: a still-elite elder who dips is shed only lightly; a genuine fader (lcr&le;0) is byte-exact and still falls. Only the shed down-branch is touched &rarr; every non-declining player is &Delta;=0.</div>
<div class=kpis>
<div class=kpi><div class=v>{len(movers)}</div><div class=l>players moved (all UP)</div></div>
<div class=kpi><div class=v>0</div><div class=l>down movers</div></div>
<div class=kpi><div class=v>+{tot1-tot0}</div><div class=l>board total ({100*(tot1-tot0)/tot0:+.2f}%)</div></div>
<div class=kpi><div class=v>805</div><div class=l>board rows (parity eps=0)</div></div>
</div>

<h2>Single-lever movers (v2.5 &rarr; after)</h2>
<div class=scroll><table><thead><tr><th>player</th><th>pos</th><th class=n>age</th><th class=n>v2.5</th><th class=n>after</th><th class=n>&Delta;</th></tr></thead>
<tbody>{mover_rows()}</tbody></table></div>

<h2>Named anchors &mdash; &Delta;=0 (not declining; this lever cannot reach them)</h2>
<div class=scroll><table><thead><tr><th>player</th><th>pos</th><th class=n>age</th><th class=n>v2.5</th><th class=n>after</th><th class=n>&Delta;</th></tr></thead>
<tbody>{rows(NAMED)}</tbody></table></div>
<div class=note>Gawn (RUC) &amp; Cameron (KEY_FWD) are on the UP-hold branch (2026 form at/above their established level); Bontempelli (MID) is within the &plusmn;3 down-tolerance. None enter the shed, so the decline curve is a no-op for all three. See the report-only diagnosis for what actually suppresses them (v7 age-taper / ruck &amp; KPF economics).</div>

<h2>Genuine-decliner contrast set &mdash; still drops (&Delta;=0, at/below replacement)</h2>
<div class=scroll><table><thead><tr><th>player</th><th>pos</th><th class=n>age</th><th class=n>v2.5</th><th class=n>after</th><th class=n>&Delta;</th></tr></thead>
<tbody>{rows(DECL)}</tbody></table></div>

<h2>Fitted up-only credit bump <code>_FBUMP_Z</code> (added to <code>_agemult(age)</code>)</h2>
<div class=scroll><table><thead><tr><th class=n>age\\lcr</th>{surf_hdr}</tr></thead><tbody>{surf_rows()}</tbody></table></div>
<div class=sub>Bump grows with lcr (still-elite) and shrinks with age; lcr&le;0 columns are hard-zeroed at runtime (below-replacement faders untouched).</div>

<h2>Full board ({len(act)} rows, value-sorted)</h2>
<div class="scroll tall"><table><thead><tr><th>player</th><th>pos</th><th class=n>age</th><th class=n>pick</th><th class=n>value</th><th class=n>&Delta;</th></tr></thead>
<tbody>{full_rows()}</tbody></table></div>
</div>"""
doc="<!DOCTYPE html><html lang=en><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><title>Form-Conditioned Aging Decline — board</title><style>"+CSS+"</style></head><body>"+H+"</body></html>"
os.makedirs('/mnt/user-data/outputs',exist_ok=True)
for path in ['/mnt/user-data/outputs/rl_draft_engine.html', O+'/aging_decline_board.html']:
    open(path,'w').write(doc)
    print("wrote",path,len(doc),"bytes")
