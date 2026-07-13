#!/usr/bin/env python3
"""Probe the WIRED engine under the current RL_* env: report named evs + board sum/n.
Run per-config (env gates) in a subprocess so each import reads its own env. No patching — levers are wired."""
import io,contextlib,os,sys
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
names=['louis-emmett','marcus-bontempelli','max-gawn','zach-butters','ned-knobel','sam-darcy','kieren-briggs','tom-holmes']
board=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
tot=0; n=0
for p in board:
    v=ev(p)
    if v is not None: tot+=v; n+=1
cfg=' '.join('%s=%s'%(k,os.environ[k]) for k in ['RL_PVCADOPT','RL_MSD_POOL_EXCL','RL_DIAL14','RL_AGE','RL_L5_PICKLESS'] if k in os.environ)
out=[]
for nm in names:
    p=find(nm.replace('-',' ')); out.append('%s=%s'%(nm.split('-')[-1], ev(p) if p else 'NA'))
print("[%s]  n=%d sum=%d | %s"%(cfg or 'DEFAULT', n, tot, ' '.join(out)))
