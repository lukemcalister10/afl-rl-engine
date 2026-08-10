import os,sys,io,contextlib,json
import numpy as np
WORKDIR=os.environ['RL_WORKDIR']; sys.path.insert(0,os.environ.get('RL_VENDOR','/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0,'.')
src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
G={'__name__':'_yc'}
with contextlib.redirect_stdout(io.StringIO()): exec(src,G)
MA=G['MA']; cp=G['cp']; yc=G['_ycred_mult']
rows=json.load(open(os.environ['RL_DEC']))
keys={r['key']:r for r in rows}
byk={p['key']:p for p in MA.data if p.get('key') in keys}
out=[]
for k,r in keys.items():
    p=byk.get(k)
    if p is None: continue
    sv=p['scoring']
    Y1=r['Y']; Y0=cp.debutyr(p)-1
    p['scoring']=[x for x in sv if x['year']<=Y1]
    c1=float(yc(p,Y1))
    p['scoring']=[]
    c0=float(yc(p,Y0))
    p['scoring']=sv
    out.append(dict(key=k,pos=r['pos'],pk=r['pk'],c0=c0,c1=c1,price=r['s6_price'],v0=r['v0'],v0u=r['v0u']))
json.dump(out,open(os.environ['RL_OUT'],'w'))
def A(rs,f): return sum(f(x) for x in rs)
print("L1c expected-re-rating credit (_ycred_mult), value-weighted by v0_uncapped")
print(f"{'pos':6s} {'n':>4s} {'cred@yr0':>9s} {'cred@yr1':>9s} {'ratio':>7s}")
for p in ['MID','SD','SF','KPF','KPD','RUCK','ALL']:
    rs=[x for x in out if p=='ALL' or x['pos']==p]
    a=A(rs,lambda x:x['c0']*x['v0u'])/A(rs,lambda x:x['v0u']); b=A(rs,lambda x:x['c1']*x['v0u'])/A(rs,lambda x:x['v0u'])
    print(f"{p:6s} {len(rs):4d} {a:9.4f} {b:9.4f} {b/a:7.4f}")
