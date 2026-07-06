#!/usr/bin/env python3
"""Price every real board player once with the current RL_FORMDECL and dump to argv[1] (JSON).
Run twice (RL_FORMDECL=0 and =1) in SEPARATE processes — exec'ing the engine twice in one process
corrupts the cp._lvl_eff monkeypatch chain. READ-ONLY."""
import io, contextlib, os, json, sys
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; cp=g['cp']
_lvlcurr=g['_lvlcurr']; _nqual=g['_nqual']; DOWN_TOL=g['DOWN_TOL']; PROVEN_N=g['PROVEN_N']
lvl_eff_orig=cp._lvl_eff_orig; REPL=MA.REPL
out={}
for p in MA.data:
    if not MA.GRP.get(p.get('pos')): continue
    k=p.get('key')
    if k is None: continue
    n=_nqual(p,2026); Lo=lvl_eff_orig(p,2026); Lc=_lvlcurr(p,2026)
    br='UP-hold' if (n>=PROVEN_N and Lc>=Lo) else ('SHED' if (n>=PROVEN_N and (Lo-Lc)>DOWN_TOL) else ('hold' if n>=PROVEN_N else 'thin'))
    out[k]=[ev(p,2026), p['player'], MA.gfut(p), round(cp._age_asof(p,2026)), n,
            round(Lc-REPL.get(MA.gfut(p),0.0),1), br]
json.dump(out, open(sys.argv[1],'w'))
print("wrote", sys.argv[1], "players", len(out), "RL_FORMDECL=", os.environ.get('RL_FORMDECL','1'))
