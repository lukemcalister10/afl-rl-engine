#!/usr/bin/env python3
# FLAG (b) DPP forward-eligibility — OLD-ENGINE (pre-merge) pass
# The old engine rl_model.py credits forward/dual eligibility via TWO mechanics the
# bake dropped: futblend (REPL blend across eligible positions, feeds proj_from_peak)
# and the level_now dual-premium spike-cap (rl_model.py:233). This pass measures the
# forward-eligibility PREMIUM the old engine assigns each DPP with gfut HELD FIXED:
#     premium = value(p, with _fut) - value(p, _fut collapsed to [[max-weight,100]])
# Collapsing to the SINGLE max-weight position keeps gfut identical (so the resolved
# position/curve does NOT flip) and removes ONLY the second-position blend+premium —
# an isolation of the forward-eligibility credit, not a position reclassification.
# Serong (jai-serong) is the anchor (~+$275; his stored _vpt=377). Reported as
# [OLD rl_model pre-merge] — a DIFFERENT scale from the baked engine; kept in its
# own columns, never subtracted across engines.
import io, contextlib, os, json
ENG='/home/claude/rl_workspace/rl_after'; OUT='/home/user/afl-rl-engine/evidence/flags/dpp'
os.chdir(ENG)
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as RM
def slug(p): return RM.slug(p['player'])
rows={}
for p in RM.players:
    f=p.get('_fut')
    if not (isinstance(f,list) and len(f)>1): continue
    # max-weight raw position (keeps gfut fixed when collapsed to 100%)
    mw=max(f, key=lambda x:x[1])[0]
    with contextlib.redirect_stdout(io.StringIO()):
        v_dual=RM.value(p,'bal'); gf_dual=RM.gfut(p)
        sav=p.get('_fut')
        # (A) prem_fut: value of reading the dual/future role vs the bare LISTED position
        #     (_fut=[] -> gfut falls back to bnow = current/listed position). Matches the
        #     Serong ~+$320 anchor: his _fut lifts him off KEY_DEF onto his GDEF/MID role.
        p['_fut']=[]; v_bare=RM.value(p,'bal'); gf_bare=RM.gfut(p)
        # (B) prem_2nd: SECOND-position blend only, gfut held fixed at max-weight.
        p['_fut']=[[mw,100.0]]; v_solo=RM.value(p,'bal'); gf_solo=RM.gfut(p)
        p['_fut']=sav
    rows[slug(p)]=dict(v_dual=round(v_dual,1), gfut_old=gf_dual,
                       v_bare=round(v_bare,1), prem_fut=round(v_dual-v_bare,1), gf_bare=gf_bare,
                       v_solo=round(v_solo,1), prem_2nd=round(v_dual-v_solo,1),
                       gfut_held=(gf_dual==gf_solo))
with open(os.path.join(OUT,'dpp_old.json'),'w') as f:
    json.dump(dict(state='OLD rl_model pre-merge', n=len(rows), rows=rows), f, indent=2)
print("old pass: %d DPPs -> dpp_old.json" % len(rows))
