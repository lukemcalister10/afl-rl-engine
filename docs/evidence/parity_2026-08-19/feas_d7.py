# D7 FEASIBILITY PROBE — READ ONLY. No engine file is edited. Confirms the healthy counterfactual
# (all injury treatment neutralised per row) can be evaluated in-process.
import os,sys,io,json,contextlib
ROOT='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/wt-d7'
sys.path.insert(0,os.path.join(ROOT,'docs/evidence/assembly_2026-08-19'))
for k in ('RL_O42','RL_AVAIL','RL_O41_RAMP','RL_O41_BREAK','RL_O41_UNWIND','RL_O41_CREDITFORM'):
    os.environ.pop(k,None)
import os_lib as OL
NS=OL.load(RL_O37='1',RL_O38A='1',RL_O38B1='1',RL_O39_BETASAT='0.105',
           RL_O40_CAPFORM='smooth',RL_O40_CAPPCT='15',RL_O40_RECW='0.47',RL_O40_PGMAT='1',
           RL_O41_SDOFF='2.98',RL_O41_CREDIT='1',RL_O41_RESET='1',RL_O41_INJ='1',
           RL_O41_R3='1',RL_O41_RAMP='1',RL_O41_BREAK='unwind',RL_O41_UNWIND='7',RL_O42='1')
ev=NS['ev']; MA=NS['_MA']; ST=NS['_AVAIL_STATE']
print('avail state rows:',len(ST))
print('INJSET size:',len(NS['_O41_INJSET']))
recs={p.get('key'):p for p in MA.data if p.get('key') in ST}
print('records matched:',len(recs))
inj_orig=NS['o41_injured']
def probe(key):
    p=recs[key]
    with contextlib.redirect_stdout(io.StringIO()):
        v_inj=ev(p,2026)
    # ---- healthy counterpart: strip EVERY injury treatment for this row ----
    saved_state=ST.pop(key,None)
    saved_hc=p.get('_avail_hc',0.0); saved_ret=p.get('_lti_ret_hc',0.0)
    p['_avail_hc']=0.0; p['_lti_ret_hc']=0.0
    NS['o41_injured']=lambda q,_o=inj_orig,_k=key: (False if q.get('key')==_k else _o(q))
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            v_h=ev(p,2026)
    finally:
        NS['o41_injured']=inj_orig
        if saved_state is not None: ST[key]=saved_state
        p['_avail_hc']=saved_hc; p['_lti_ret_hc']=saved_ret
    with contextlib.redirect_stdout(io.StringIO()):
        v_back=ev(p,2026)
    return v_inj,v_h,v_back
ks=sorted(recs)[:4]
for k in ks:
    a,b,c=probe(k)
    print('%-24s v_inj=%10.2f  v_healthy=%10.2f  restore_ok=%s'%(k,a,b,abs(c-a)<1e-9))
