#!/usr/bin/env python3
"""LEG B measurement harness (dev-shell). Loads the engine with the un-compress map at the s given by
RL_UNCOMP_S (or inert if unset), and prints the load-time reference/conservation table + optional per-player
board deltas. Run from the workspace rl_after with the standard dev-shell env. Everything printed to STDERR
so rl_export's stdout-redirect never swallows it; the engine is exec'd exactly as the panel/board build do."""
import io,contextlib,sys,json,os
def load_engine():
    g={}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    g['MA'].BASE_REF=g['MA'].AGE_REF=2026; g['MA']._pe_clear()
    return g
def w(*a): sys.stderr.write(' '.join(str(x) for x in a)+'\n')
if __name__=='__main__':
    g=load_engine(); MA=g['MA']; ev=g['ev']
    w("=== RL_UNCOMP state: _UNCOMP=%s  UNCOMP_S=%s  Delta=%s"%(MA._UNCOMP,MA.UNCOMP_S,MA.UNCOMP_DELTA))
    if MA._UNCOMP_LREF:
        w("%-9s %8s %10s %9s"%('pos','L_ref','V_ref','C[pos]'))
        for p in sorted(MA._UNCOMP_LREF):
            w("%-9s %8.3f %10.3f %9.5f"%(p,MA._UNCOMP_LREF[p],MA._UNCOMP_VREF[p],MA._UNCOMP_C.get(p,1.0)))
    else:
        w("(map inert: no reference built)")
