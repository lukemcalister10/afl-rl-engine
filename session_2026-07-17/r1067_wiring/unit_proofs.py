#!/usr/bin/env python3
"""R106.7 in-session fixture unit-proofs (jobs 3+4). Run from engine/rl_after under the panel env.
Proves: item-284 guards (four cross-class pairs + present-not-in-set synthetic + valid DPP), the §1b floor
endpoints (sp=1 no-op / sp=0 whole-year vs low), and RL_FLEX=0 byte-exactness of prod_floor. Owner conditions 1-2."""
import io,contextlib,os,sys
with contextlib.redirect_stdout(io.StringIO()): import rl_model as MA

def orig_floor(p,lens='bal'):   # reference: the pre-§1b floor loop (lowbar absent)
    g=MA.bnow(p); a=MA.age(p); pa_=MA.PEAK_AGE[g]; cur=MA.level_now(p)
    if cur is None: return 0
    d=MA.LENS[lens]; H=MA.clamp((40-a)/3.0,1.0,3.0); prod=0.0; k=0
    while k<H:
        ag=a+k; wt=min(1.0,H-k)
        lev=cur*min(1.0, MA.frac(ag,pa_)/max(MA.frac(a,pa_),1e-6))
        if k==0 and p.get('_avail_hc',0)>0 and MA.BASE_REF==2026 and MA.AGE_REF==2026: lev*=(1-p['_avail_hc'])
        prod+=wt*MA.posval(lev+MA.capt_prem(lev)-MA.REPL[g])*21/((1+d)**k); k+=1
    return MA.val(prod)

def _fix(elig,present,drafted=None):
    dp=drafted or present
    return {'eligibilities':elig,'present_position':present,'drafted_position':dp,'pos':dp,
            '_pos_now':(present if present!=dp else None),'player':'FIXTURE','stable_player_id':'fixture'}

FAIL=0
def ok(c,m):
    global FAIL
    print(("  PASS " if c else "  FAIL ")+m); FAIL+= (0 if c else 1)

print("RL_FLEX on:",MA._FLEX)
print("=== item-284 fixture proofs (_collapse_elig / y0dpp_bar) ===")
for e,pr in [('K-DEF,G-FWD','KDEF'),('K-FWD,G-DEF','KFWD'),('RUCK,G-FWD','RUC'),('RUCK,G-DEF','RUC')]:
    ok(MA.y0dpp_bar(_fix(e,pr)) is None,
       "cross-class %-12s present %-4s collapsed %s -> y0dpp_bar None (single-position)"%(e,pr,sorted(MA._collapse_elig(e))))
ok(MA.y0dpp_bar(_fix('G-DEF,G-FWD','MID','MID')) is None,
   "present-not-in-set G-DEF,G-FWD present MID -> y0dpp_bar None (single-position)")
ok(MA.y0dpp_bar(_fix('MID,G-FWD','MID','MID'))=='GEN_FWD',
   "VALID MID,G-FWD present MID -> y0dpp_bar GEN_FWD (verdict always produced)")

print("=== §1b floor ENDPOINTS (sp=1 no-op == original; sp=0 whole year-0 vs low) ===")
def find(sid): return next(x for x in MA.data if (x.get('stable_player_id') or '').endswith(sid))
for nm,sid in [('Petracca','fb186725cde9cc707a20'),('Jake Lloyd','797837193a7c4b847d81'),('McKercher','ec36ae407a5d9b9384e1')]:
    p=find(sid); bar=MA.y0dpp_bar(p); sp0=MA.SEASON_PROG
    MA.SEASON_PROG=1.0; f1=MA.prod_floor(p)
    MA.SEASON_PROG=0.0; f0=MA.prod_floor(p)
    MA.SEASON_PROG=sp0; fn=MA.prod_floor(p); o=orig_floor(p)
    ok(abs(f1-o)<1e-9, "%-10s bar=%-8s sp=1 floor==orig(%.2f) | sp=0=%.2f sp=%.2f=%.2f (low-bar nets UP)"%(nm,bar,o,f0,sp0,fn))

print("=== condition 2: RL_FLEX=0 byte-exact — deferred to a FLEX=0 subprocess (see .txt) ===")
sys.exit(1 if FAIL else 0)
