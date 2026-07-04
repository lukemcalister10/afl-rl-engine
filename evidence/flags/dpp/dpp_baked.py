#!/usr/bin/env python3
# FLAG (b) DPP forward-eligibility — BAKED-ENGINE pass  [BAKED c47cb43d]
# For every dual-position player (len(_fut)>1) in the real store, record identity
# (ID.pick.cohort), eligible groups+weights, and the baked engine's:
#   * current ev  = priced on max-weight position only (gfut)  <- what the bake does
#   * optionality ev = max over eligible groups of ev-priced-as-that-group
#       (the only forward-eligibility signal the BAKED engine's mechanics can express:
#        a DPP can be deployed at its best-value eligible line).
# The baked engine has NO futblend / dual-premium (dropped in the merge) — verified:
# gfut is the sole _fut reader. So the optionality gap is expected to be SMALL; the
# rich forward-eligibility value lives in the OLD engine (measured in dpp_old.py).
import io, contextlib, os, json
ENG='/home/claude/rl_workspace/rl_after'; OUT='/home/user/afl-rl-engine/evidence/flags/dpp'
os.chdir(ENG)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; delisted=g['delisted']; GRP=MA.GRP
Y=2026; FWDG={'GEN_FWD','KEY_FWD'}

def egroups(p):
    out={}
    for pos,wt in (p.get('_fut') or []):
        gg=GRP.get(pos)
        if gg: out[gg]=out.get(gg,0)+wt
    s=sum(out.values())
    return {gg:w/s for gg,w in out.items()} if s>0 else {}

def price_as_group(p,grp):
    sav=p.get('_fut'); rawpos=next((rp for rp,gg in GRP.items() if gg==grp),None)
    p['_fut']=[[rawpos,100.0]]; MA._pe_clear()
    try: return ev(p,Y)
    finally: p['_fut']=sav; MA._pe_clear()

rows={}
for p in MA.data:
    if id(p) not in g['_REAL']: continue
    if not (isinstance(p.get('_fut'),list) and len(p['_fut'])>1): continue
    eg=egroups(p)
    MA._pe_clear(); cur=ev(p,Y)
    at={grp:price_as_group(p,grp) for grp in eg}
    best=max(at,key=at.get) if at else MA.gfut(p)
    rows[p['key']]=dict(key=p['key'], pick=(p['pick'] if p.get('pick') else None),
        cohort=cp.debutyr(p), age=cp._age_asof(p,Y), gfut=MA.gfut(p),
        egroups={k:round(v,3) for k,v in eg.items()},
        fwd_elig=bool(set(eg)&FWDG), delist=delisted(p),
        cur=cur, opt_best=best, opt_ev=at.get(best,cur), gap_opt=at.get(best,cur)-cur,
        at={k:int(v) for k,v in at.items()})
with open(os.path.join(OUT,'dpp_baked.json'),'w') as f:
    json.dump(dict(state='BAKED c47cb43d', repl={k:round(v,2) for k,v in MA.REPL.items()},
                   n=len(rows), rows=rows), f, indent=2)
print("baked pass: %d DPPs -> dpp_baked.json" % len(rows))
