# R2 — render the smooth age curve + 95% ribbon to a self-contained SVG (matplotlib absent in env).
# Two curves: mean-reversion-adjusted (primary) and age-only DiD (prior). Board of record b0c39d78.
import d2common as D, numpy as np
np.random.seed(0)
ev=D.build_events(); ctrl=D.build_control(); exp=D.make_expected(ctrl)
cl=D.build_control_lvl(); pred=D.fit_ctrl_model(cl)
rows=D.effect_rows(ev,exp,ctrl_predict=pred)
age=np.array([r['age_pre'] for r in rows])
yA=np.array([r['effect'] for r in rows]); yB=np.array([r['effect_adj'] for r in rows])
GRID=np.arange(18,35); BW=2.5
def nw(xq,x,y,bw):
    w=np.exp(-0.5*((x-xq)/bw)**2)
    if w.sum()<3: return np.nan
    X=np.column_stack([np.ones(len(x)),x-xq]); W=np.diag(w)
    try: return float(np.linalg.solve(X.T@W@X,X.T@W@y)[0])
    except np.linalg.LinAlgError: return float(np.sum(w*y)/w.sum())
def band(x,y):
    base=np.array([nw(g,x,y,BW) for g in GRID]); B=2000
    bs=np.empty((B,len(GRID)))
    for b in range(B):
        s=np.random.randint(0,len(x),len(x)); bs[b]=[nw(g,x[s],y[s],BW) for g in GRID]
    return base,np.nanpercentile(bs,2.5,0),np.nanpercentile(bs,97.5,0)
bA,loA,hiA=band(age,yA); bB,loB,hiB=band(age,yB)
raw_n={int(a):int(c) for a,c in zip(*np.unique(np.round(age).astype(int),return_counts=True))}

# --- SVG geometry ---
W,Hh=760,460; ml,mr,mt,mb=58,20,34,52; pw,ph=W-ml-mr,Hh-mt-mb
x0,x1=18,34; y0,y1=-14.0,8.0
def X(a): return ml+(a-x0)/(x1-x0)*pw
def Y(v): return mt+(y1-v)/(y1-y0)*ph
def poly(gr,lo,hi):
    pts=[f"{X(g):.1f},{Y(lo[i]):.1f}" for i,g in enumerate(gr)]+[f"{X(g):.1f},{Y(hi[i]):.1f}" for i,g in reversed(list(enumerate(gr)))]
    return " ".join(pts)
def line(gr,b): return " ".join(f"{X(g):.1f},{Y(b[i]):.1f}" for i,g in enumerate(gr))
# support mask: raw n>=3 in a +-1 window -> "supported"; else dashed/declared
def supp(g): return sum(raw_n.get(a,0) for a in (g-1,g,g+1))>=6
supGRID=[g for g in GRID if supp(g)]
def seg(gr,b): return " ".join(f"{X(g):.1f},{Y(b[GRID.tolist().index(g)]):.1f}" for g in gr)

s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {Hh}" font-family="system-ui,Arial" font-size="12">']
s.append(f'<rect width="{W}" height="{Hh}" fill="white"/>')
s.append(f'<text x="{ml}" y="18" font-size="14" font-weight="700">D2 re-cut · return-from-absence effect vs age (smooth, CORE rule 7) · board b0c39d78</text>')
# gridlines + y labels
for v in range(-14,9,2):
    yy=Y(v); s.append(f'<line x1="{ml}" y1="{yy:.1f}" x2="{ml+pw}" y2="{yy:.1f}" stroke="#eee"/>')
    s.append(f'<text x="{ml-8}" y="{yy+4:.1f}" text-anchor="end" fill="#666">{v:+d}</text>')
s.append(f'<line x1="{ml}" y1="{Y(0):.1f}" x2="{ml+pw}" y2="{Y(0):.1f}" stroke="#999" stroke-width="1"/>')
for a in range(18,35,2):
    s.append(f'<text x="{X(a):.1f}" y="{Hh-mb+18}" text-anchor="middle" fill="#666">{a}</text>')
    s.append(f'<line x1="{X(a):.1f}" y1="{mt}" x2="{X(a):.1f}" y2="{mt+ph}" stroke="#f6f6f6"/>')
s.append(f'<text x="{ml+pw/2}" y="{Hh-8}" text-anchor="middle" fill="#444">age at last pre-absence season</text>')
s.append(f'<text x="16" y="{mt+ph/2}" text-anchor="middle" fill="#444" transform="rotate(-90 16 {mt+ph/2})">effect (SC pts, − = penalty)</text>')
# ribbons
s.append(f'<polygon points="{poly(GRID,loB,hiB)}" fill="#c62828" opacity="0.13"/>')
s.append(f'<polygon points="{poly(GRID,loA,hiA)}" fill="#1565c0" opacity="0.10"/>')
# unsupported region shading (age<20 no data; 32-34 thin)
s.append(f'<rect x="{X(18):.1f}" y="{mt}" width="{X(20)-X(18):.1f}" height="{ph}" fill="#000" opacity="0.05"/>')
s.append(f'<rect x="{X(31.5):.1f}" y="{mt}" width="{X(34)-X(31.5):.1f}" height="{ph}" fill="#000" opacity="0.05"/>')
s.append(f'<text x="{X(19):.1f}" y="{mt+ph-6}" text-anchor="middle" fill="#999" font-size="10">no data</text>')
s.append(f'<text x="{X(33):.1f}" y="{mt+ph-6}" text-anchor="middle" fill="#999" font-size="10">thin</text>')
# lines (full = supported solid, else dashed)
s.append(f'<polyline points="{line(GRID,bA)}" fill="none" stroke="#1565c0" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.8"/>')
s.append(f'<polyline points="{line(GRID,bB)}" fill="none" stroke="#c62828" stroke-width="1.4" stroke-dasharray="4 3" opacity="0.7"/>')
s.append(f'<polyline points="{seg(supGRID,bB)}" fill="none" stroke="#c62828" stroke-width="2.6"/>')
s.append(f'<polyline points="{seg(supGRID,bA)}" fill="none" stroke="#1565c0" stroke-width="2.2"/>')
# legend
s.append(f'<rect x="{ml+pw-236}" y="{mt+4}" width="230" height="52" fill="white" stroke="#ddd"/>')
s.append(f'<line x1="{ml+pw-226}" y1="{mt+20}" x2="{ml+pw-196}" y2="{mt+20}" stroke="#c62828" stroke-width="2.6"/><text x="{ml+pw-190}" y="{mt+24}" font-size="11">mean-reversion-adjusted (primary)</text>')
s.append(f'<line x1="{ml+pw-226}" y1="{mt+40}" x2="{ml+pw-196}" y2="{mt+40}" stroke="#1565c0" stroke-width="2.2"/><text x="{ml+pw-190}" y="{mt+44}" font-size="11">age-only DiD (prior D2)</text>')
# 3-bin overlay (what rule 7 replaces)
for lo,hi,val in [(18,25,-4.94),(25,29,-1.07),(29,35,-3.32)]:
    s.append(f'<line x1="{X(lo):.1f}" y1="{Y(val):.1f}" x2="{X(min(hi,34)):.1f}" y2="{Y(val):.1f}" stroke="#2e7d32" stroke-width="2" stroke-dasharray="2 2" opacity="0.7"/>')
s.append(f'<text x="{X(25.5):.1f}" y="{Y(-1.07)-6:.1f}" fill="#2e7d32" font-size="10">old 3-bin cut (destroys the U)</text>')
s.append('</svg>')
open('/home/user/afl-rl-engine/session_2026-07-14/d2_recut/fig_r2_agecurve.svg','w').write("\n".join(s))
print("wrote fig_r2_agecurve.svg  (supported ages:",supGRID,")")
