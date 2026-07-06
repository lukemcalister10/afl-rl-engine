#!/usr/bin/env python3
"""REPORT-ONLY layer attribution for the 3 named anchors (2026-07-06). NO engine logic changes here —
this only toggles individual existing layers in a throwaway exec'd copy to attribute each anchor's value.
Modes (env DIAG_MODE): base | no_v7 (v7 age-taper -> identity) | no_ruccap (RL_RUC_PRIOR_CAP=99).
Prices a small probe set and dumps to argv[1]. Run once per mode in a SEPARATE process."""
import io, contextlib, os, json, sys
MODE=os.environ.get('DIAG_MODE','base')
if MODE=='no_ruccap': os.environ['RL_RUC_PRIOR_CAP']='99'
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
if MODE=='no_v7':
    g['_v7']=lambda bb,p,Y: list(bb)          # neutralise the age-taper on the q97 upside tail bb[5]
MA=g['MA']; ev=g['ev']; cp=g['cp']
_lvlcurr=g['_lvlcurr']; REPL=MA.REPL
PROBE=['max-gawn','jeremy-cameron','marcus-bontempelli','kieren-briggs','darcy-cameron','tim-english',
       'lachie-neale','rory-laird','patrick-cripps','jack-steele','sam-walsh','andrew-brayshaw',
       'nick-daicos','harry-sheezel','caleb-serong']
byk={p['key']:p for p in MA.data if p.get('key')}
out={}
for k in PROBE:
    p=byk.get(k)
    if not p: continue
    out[k]=[ev(p,2026), p['player'], MA.gfut(p), round(cp._age_asof(p,2026)),
            round(_lvlcurr(p,2026),1), round(_lvlcurr(p,2026)-REPL.get(MA.gfut(p),0.0),1)]
json.dump(out, open(sys.argv[1],'w'))
print("MODE",MODE,"->",sys.argv[1])
