#!/usr/bin/env python3
import os, sys, json, hashlib, subprocess, platform, csv, statistics, html, shutil, pathlib, textwrap
ROOT=pathlib.Path(__file__).resolve().parents[3]
OUT=ROOT/'session_2026-07-21/forward_lens_acceptance'
WS=pathlib.Path('/home/claude/rl_workspace/rl_after')
BASE='f05ebe6df49b653b053f0ebdd82ddc56ee8d4187'
EXPECTED='06d8af60b679a12db07c064c60c065f9'

def run(cmd, cwd=ROOT, env=None):
    p=subprocess.run(cmd, cwd=cwd, env=env, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return {'cmd':cmd,'rc':p.returncode,'out':p.stdout}
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
def jload(p): return json.load(open(p))

def provenance():
    boot=jload(ROOT/'data/expected_boot.json')
    py=sys.version.replace('\n',' ')
    import numpy as np
    show=[]
    try:
        from io import StringIO
        import contextlib
        buf=StringIO()
        with contextlib.redirect_stdout(buf): np.show_runtime()
        show=buf.getvalue().splitlines()
    except Exception as e: show=[repr(e)]
    cpu=open('/proc/cpuinfo').read().split('\n\n')[0] if os.path.exists('/proc/cpuinfo') else ''
    files={'installed_board':'data/rl_build/rl_app_data.json','store':'data/rl_model_data.json','rl_model':'rl_model.py','engine':'engine/forward_valuation/__init__.py','model_config':'data/model_config.json','requirements_lock':'requirements-lock.txt','package_lock':'package-lock.json'}
    fmd5={k:(md5(ROOT/v) if (ROOT/v).exists() else None) for k,v in files.items()}
    fv=run("python3 - <<'PY2'\nimport fv_provenance as f; print(f.identity()) ; print(f.resolve_source_dir())\nPY2", cwd=WS, env=dict(os.environ,RL_REPO=str(ROOT),PYTHONPATH=str(WS)+':/home/claude/rl_vendor',RL_FV=str(ROOT/'engine/forward_valuation')))
    bg=run('RL_REPO=$PWD python3 boot_guard.py bootstrap', cwd=ROOT)
    envvars={k:v for k,v in sorted(os.environ.items()) if k.startswith('RL_') or k.startswith('PAR_')}
    return {'base_sha':BASE,'clean_tree_before':run('git status --short',cwd=ROOT)['out'],'expected_boot':boot,'file_md5':fmd5,'python':py,'numpy':np.__version__,'numpy_show_runtime':show,'cpuinfo_first_processor':cpu,'rl_par_env':envvars,'fv_probe':fv,'boot_guard':bg,'bootstrap_limitation':'bootstrap.sh was run before this script and passed after installing requirements-lock.txt pins.'}

def build(label, lege, legf):
    env={k:v for k,v in os.environ.items() if not (k.startswith('RL_') or k.startswith('PAR_'))}
    env.update(RL_REPO=str(ROOT), RL_FV=str(ROOT/'engine/forward_valuation'), PYTHONHASHSEED='0', PYTHONPATH=str(WS)+':/home/claude/rl_vendor', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1', RL_PVC2='1', RL_LEGE=str(lege), RL_LEGF=str(legf))
    env.pop('RL_CONFIG_MODE',None)
    before_store=md5(WS/'rl_model_data.json'); before_inst=md5(ROOT/'data/rl_build/rl_app_data.json')
    r=run('rm -f rl_app_data.json; python3 rl_export.py', cwd=WS, env=env)
    if r['rc']!=0: raise SystemExit(label+' build failed '+r['out'][-4000:])
    src=WS/'rl_app_data.json'; dest=OUT/(label+'.json'); shutil.copyfile(src,dest)
    return {'label':label,'RL_PVC2':'1','RL_LEGE':str(lege),'RL_LEGF':str(legf),'RL_CONFIG_MODE':'UNSET (diagnostic limitation; not canonical bake)', 'md5':md5(dest), 'stdout_tail':r['out'][-2000:], 'store_before':before_store,'store_after':md5(WS/'rl_model_data.json'),'installed_board_before':before_inst,'installed_board_after':md5(ROOT/'data/rl_build/rl_app_data.json')}

def rank(rows, field):
    return {r['key']:i+1 for i,r in enumerate(sorted(rows,key=lambda x:(-x.get(field,0), x.get('name',''), x.get('key',''))))}
def pct(a,b): return None if a==0 else (b-a)/a*100

def analyze(A,B):
    ar,br=A['active'],B['active']; ka={r['key']:r for r in ar}; kb={r['key']:r for r in br}
    ra=rank(ar,'v'); rb=rank(br,'v'); rp1a=rank(ar,'vP1'); rp1b=rank(br,'vP1'); rp2a=rank(ar,'vP2'); rp2b=rank(br,'vP2')
    fields=sorted(set().union(*[r.keys() for r in ar+br]))
    inv={'added':sorted(set(kb)-set(ka)),'removed':sorted(set(ka)-set(kb)),'current_value_diffs':0,'present_rank_diffs':0,'present_order_diffs':0,'current_sum_A':sum(r['v'] for r in ar),'current_sum_B':sum(r['v'] for r in br),'identity_diffs':0,'pick1_A':A['picks'][0]['v'],'pick1_B':B['picks'][0]['v']}
    diffs={}; rows=[]
    idfields={'name','key','club','grp','gf','pk','draft','cat','h26','ty','age','lti_reg'}; forward={'vP1','vP2','picks_2027','posture_2027_discounts','phantomLayer','phantomPicks','phantomTotals'}
    for k in sorted(set(ka)&set(kb)):
        a,b=ka[k],kb[k]
        if a.get('v')!=b.get('v'): inv['current_value_diffs']+=1
        if ra[k]!=rb[k]: inv['present_rank_diffs']+=1
        for f in fields:
            if a.get(f)!=b.get(f):
                cl='forward-lens' if f in forward or f.startswith('vP') else ('identity/present HARD FAIL' if f in idfields or f=='v' else 'non-forward unexplained')
                diffs.setdefault(f,{'count':0,'classification':cl,'examples':[]}); diffs[f]['count']+=1
                if len(diffs[f]['examples'])<5: diffs[f]['examples'].append({'key':k,'A':a.get(f),'B':b.get(f)})
        v=a['v']; rows.append({'stable_key':k,'player_name':a.get('name'), 'age':a.get('age'),'position':a.get('grp'),'club':a.get('club'),'LTI_status':a.get('lti_reg'),'current_value':v,'current_rank':ra[k],'Board_A_vP1':a.get('vP1'),'Board_B_vP1':b.get('vP1'),'abs_vP1_diff':b.get('vP1')-a.get('vP1'),'pct_vP1_diff':pct(a.get('vP1'),b.get('vP1')),'Board_A_vP2':a.get('vP2'),'Board_B_vP2':b.get('vP2'),'abs_vP2_diff':b.get('vP2')-a.get('vP2'),'pct_vP2_diff':pct(a.get('vP2'),b.get('vP2')),'old_plus1_rank':rp1a[k],'new_plus1_rank':rp1b[k],'old_plus2_rank':rp2a[k],'new_plus2_rank':rp2b[k],'projection_attribution':'Leg E/F forward-lens delta' if (a.get('vP1')!=b.get('vP1') or a.get('vP2')!=b.get('vP2')) else 'unchanged'})
    orderA=[r['key'] for r in sorted(ar,key=lambda x:(-x.get('v',0), x.get('name',''), x.get('key','')))] ; orderB=[r['key'] for r in sorted(br,key=lambda x:(-x.get('v',0), x.get('name',''), x.get('key','')))]
    inv['present_order_diffs']=sum(x!=y for x,y in zip(orderA,orderB))+abs(len(orderA)-len(orderB))
    inv['identity_diffs']=sum(diffs.get(f,{}).get('count',0) for f in idfields)
    # stats
    def summary(vals):
        vals=sorted(vals); return {'n':len(vals),'min':vals[0],'q1':statistics.quantiles(vals,n=4)[0],'median':statistics.median(vals),'q3':statistics.quantiles(vals,n=4)[2],'max':vals[-1]}
    pop={'league_totals':{'A':{f:sum(r[f] for r in ar) for f in ['v','vP1','vP2']},'B':{f:sum(r[f] for r in br) for f in ['v','vP1','vP2']}},'ratios':{'A_vP1_v':summary([r['vP1']/r['v'] for r in ar if r['v']]),'B_vP1_v':summary([r['vP1']/r['v'] for r in br if r['v']]),'A_vP2_v':summary([r['vP2']/r['v'] for r in ar if r['v']]),'B_vP2_v':summary([r['vP2']/r['v'] for r in br if r['v']])}}
    for side,rs in [('A',ar),('B',br)]:
        pop[side+'_counts']={}
        for f in ['vP1','vP2']:
            pop[side+'_counts'][f]={'zero':sum(r[f]==0 for r in rs),'near_zero_lt100':sum(r[f]<100 for r in rs),'fall_gt10':sum(r[f]<.9*r['v'] for r in rs),'fall_gt25':sum(r[f]<.75*r['v'] for r in rs),'fall_gt50':sum(r[f]<.5*r['v'] for r in rs),'rise_gt10':sum(r[f]>1.1*r['v'] for r in rs),'rise_gt25':sum(r[f]>1.25*r['v'] for r in rs),'rise_gt50':sum(r[f]>1.5*r['v'] for r in rs)}
    return inv,diffs,pop,rows

def main():
    prov=provenance(); json.dump(prov,open(OUT/'provenance.json','w'),indent=2)
    ba=build('board_A_lege0_legf0',0,0)
    if ba['md5']!=EXPECTED:
        json.dump({'verdict':'FAIL','reason':'Board A did not reproduce','board_A':ba},open(OUT/'gate_results.json','w'),indent=2); raise SystemExit(2)
    bb=build('board_B_lege1_legf1',1,1)
    A=jload(OUT/'board_A_lege0_legf0.json'); B=jload(OUT/'board_B_lege1_legf1.json')
    inv,diffs,pop,rows=analyze(A,B)
    json.dump({'field_diff_inventory':diffs,'present_invariance':inv},open(OUT/'field_diff_inventory.json','w'),indent=2)
    with open(OUT/'forward_lens_all_players.csv','w',newline='') as f: w=csv.DictWriter(f,fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    # original harnesses
    tests=[]
    cmds=[('bootstrap fail-closed provenance','bootstrap.sh / boot_guard.py','pinned md5 equality','bash bootstrap.sh'),('k=0 dormancy f3','session_2026-07-18/legf3/tests/test_k0_dormancy.py','unchanged script passes','python3 session_2026-07-18/legf3/tests/test_k0_dormancy.py'),('k=0 dormancy f4','session_2026-07-18/legf4/tests/test_k0_dormancy_f4.py','unchanged script passes','python3 session_2026-07-18/legf4/tests/test_k0_dormancy_f4.py'),('k=0 dormancy f5','session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py','unchanged script passes','python3 session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py'),('Leg F4 gate','session_2026-07-18/legf4/scripts/gate_f4.py','predeclared script pass','python3 session_2026-07-18/legf4/scripts/gate_f4.py'),('Leg F5 gate','session_2026-07-18/legf5/scripts/gate_f5.py','predeclared script pass','python3 session_2026-07-18/legf5/scripts/gate_f5.py')]
    for name,src,thr,cmd in cmds:
        rr=run(cmd); art='session_2026-07-21/forward_lens_acceptance/'+name.replace(' ','_')+'.txt'; open(ROOT/art,'w').write(rr['out']); tests.append({'test':name,'source':src,'threshold':thr,'command':cmd,'rc':rr['rc'],'pass':rr['rc']==0,'artifact':art,'freshly_rerun':True,'observed':rr['out'][-1000:]})
    missing=['historical -1 -> now projection comparison unchanged harness','historical -2 -> -1 projection comparison unchanged harness','original ±5% projected league-total gate unchanged harness','developing >= mid-career >= veteran gradient unchanged harness','age/evidence continuity, horizon cliffs, pedigree fading, LTI/availability, retirement/exit unchanged harness inventory']
    gates={'verdict':'FAIL','reason':'One or more original required validations could not be identified/rerun unchanged; directive requires halt/report limitation.','board_A':ba,'board_B':bb,'present_invariance':inv,'tests':tests,'missing_or_unresolved_required_harnesses':missing,'population':pop}
    json.dump(gates,open(OUT/'gate_results.json','w'),indent=2)
    # html
    data=json.dumps(rows)
    open(OUT/'forward_lens_review.html','w').write('<!doctype html><meta charset="utf-8"><title>Forward lens review</title><style>body{font-family:sans-serif}td,th{padding:3px 6px;border-bottom:1px solid #ddd}th{cursor:pointer;position:sticky;top:0;background:#eee}.up{color:green}.down{color:#b00}</style><h1>Forward Lens Review</h1><p>Accepted current v vs Board A old +1/+2 and Board B Leg E/F +1/+2. Self-contained, no network.</p><input id=q placeholder="filter age/position/club/tier/LTI/direction/size/name" style="width:95%;padding:8px"><table id=t></table><script>const rows='+data+';let keys=Object.keys(rows[0]);let sortK="current_rank",dir=1;function tier(v){return v>=5000?"elite":v>=2500?"high":v>=1000?"mid":v>=250?"low":"near-zero"}function draw(){let q=document.getElementById("q").value.toLowerCase();let rs=rows.filter(r=>{let d=(r.abs_vP1_diff>0||r.abs_vP2_diff>0?"up ":"")+(r.abs_vP1_diff<0||r.abs_vP2_diff<0?"down ":"")+tier(r.current_value);return (Object.values(r).join(" ")+" "+d).toLowerCase().includes(q)}).sort((a,b)=>(a[sortK]>b[sortK]?1:-1)*dir);t.innerHTML="<tr>"+keys.map(k=>`<th onclick=\"sortK=\\\'${k}\\\';dir*=-1;draw()\">${k}</th>`).join("")+"</tr>"+rs.map(r=>"<tr>"+keys.map(k=>`<td>${r[k]??""}</td>`).join("")+"</tr>").join("")}draw()</script>')
    # report
    def table(items): return '\n'.join('| '+ ' | '.join(map(str,x))+' |' for x in items)
    top=lambda key,rev=True: sorted(rows,key=lambda r:(r[key] if r[key] is not None else -999999), reverse=rev)[:20]
    report=['# Forward Lens Acceptance Diagnostic','',f'Verdict: **FAIL** — Board A reproduced and present invariance was measured, but required original Leg E/F historical/acceptance harnesses could not all be located and rerun unchanged; directive requires FAIL in that case.','',f'Board A MD5: `{ba["md5"]}`. Board B MD5: `{bb["md5"]}`.','',f'Present value diffs: {inv["current_value_diffs"]}; present rank diffs: {inv["present_rank_diffs"]}; present order diffs: {inv["present_order_diffs"]}; active added/removed: {len(inv["added"])}/{len(inv["removed"]) }; pick 1 A/B: {inv["pick1_A"]}/{inv["pick1_B"]}.','', 'Limitation: RL_CONFIG_MODE was intentionally left unset for diagnostic builds because the manifest cannot represent RL_PVC2/RL_LEGE/RL_LEGF switches correctly; neither board is a canonical bake or release-certified build.','','## Gate Table','','| Test | Source | Threshold | Command | Result | Artifact |','|---|---|---|---|---|---|']
    for t in tests: report.append(f'| {t["test"]} | {t["source"]} | {t["threshold"]} | `{t["command"]}` | {"PASS" if t["pass"] else "FAIL"} | {t["artifact"]} |')
    for m in missing: report.append(f'| {m} | not located as unchanged runnable harness | original threshold unavailable | n/a | FAIL | gate_results.json |')
    report += ['','## Population Summary','```json',json.dumps(pop,indent=2),'```','','## Top changes','See CSV/HTML for sortable complete player-level review. Deterministic cohort rule: sort active players by current rank, choose first five under age 23 (young), first five age 24-28 (prime), and first five age 29+ (veteran); rule defined before listing outputs.','','## Artifact Manifest','- FORWARD_LENS_ACCEPTANCE_REPORT.md\n- forward_lens_all_players.csv\n- forward_lens_review.html\n- board_A_lege0_legf0.json\n- board_B_lege1_legf1.json\n- gate_results.json\n- field_diff_inventory.json\n- provenance.json\n- README.md\n- scripts/run_diagnostic.py']
    open(OUT/'FORWARD_LENS_ACCEPTANCE_REPORT.md','w').write('\n'.join(report)+'\n')
    open(OUT/'README.md','w').write('Read-only diagnostic artifacts for v2.11 forward-lens acceptance. Verdict is FAIL because required original validation harnesses were not all locatable/rerunnable unchanged. Builds intentionally leave RL_CONFIG_MODE unset and are not canonical bakes.\n')
if __name__=='__main__': main()
