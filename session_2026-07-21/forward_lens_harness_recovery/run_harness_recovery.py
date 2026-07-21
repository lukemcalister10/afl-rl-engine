import os, subprocess, tempfile, shutil, json, hashlib, pathlib, sys, time
ROOT=pathlib.Path(subprocess.check_output(['git','rev-parse','--show-toplevel'], text=True).strip())
OUT=ROOT/'session_2026-07-21/forward_lens_harness_recovery'; OUT.mkdir(parents=True,exist_ok=True)
base_env=os.environ.copy(); base_env.update({'RL_REPO':str(ROOT),'RL_FV':str(ROOT/'engine/forward_valuation'),'PYTHONPATH':str(ROOT/'engine/rl_after')+':'+str(ROOT/'engine/forward_valuation')+':'+str(ROOT)+':/home/claude/rl_vendor','PYTHONHASHSEED':'0','OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'})
logs=[]; results=[]
def run(name, cmd, cwd, env_extra=None):
    env=base_env.copy();
    if env_extra:
        for k,v in env_extra.items():
            if v is None: env.pop(k,None)
            else: env[k]=v
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
    rec={'name':name,'command':' '.join(cmd),'cwd':str(cwd),'env':{k:env.get(k) for k in ['RL_REPO','PYTHONHASHSEED','OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','RL_PVC2','RL_LEGE','RL_LEGF','RL_CONFIG_MODE']},'stdout':p.stdout,'stderr':p.stderr,'exit_code':p.returncode}
    logs.append(rec); return rec
# provenance
run('bootstrap', ['bash', str(ROOT/'bootstrap.sh')], ROOT)
run('fv_provenance', ['python3','-c','import boot_guard; boot_guard.assert_fv_provenance()'], ROOT)
# board B disposable
TD=pathlib.Path(tempfile.mkdtemp(prefix='legEF_boardB_'))
shutil.copytree(ROOT/'engine/rl_after', TD/'rl_after', symlinks=True)
base_env['PYTHONPATH']=str(TD/'rl_after')+':'+str(ROOT/'engine/forward_valuation')+':'+str(ROOT)+':/home/claude/rl_vendor'
rec=run('build_board_B',['python3','rl_export.py'], TD/'rl_after', {'RL_PVC2':'1','RL_LEGE':'1','RL_LEGF':'1','RL_CONFIG_MODE':None})
board=TD/'rl_after/rl_app_data.json'
md5=hashlib.md5(board.read_bytes()).hexdigest() if board.exists() else None
data=json.load(open(board)) if board.exists() else {}
active=data.get('active',[])
PV=sum(float(p.get('v',0)) for p in active)
board_info={'temporary_path':str(board),'md5':md5,'row_count':len(active),'present_value_total':PV,'command':rec['command']}
# harnesses only if md5 matches full expected
if md5!='1f10220c341679903b79a319f554672c':
    verdict='HALT_BOARD_B_MISMATCH'
else:
    E=ROOT/'engine/rl_after'; B=str(board)
    cmds=[('legf3_k0',['python3',str(ROOT/'session_2026-07-18/legf3/tests/test_k0_dormancy.py')]),('legf4_k0',['python3',str(ROOT/'session_2026-07-18/legf4/tests/test_k0_dormancy_f4.py')]),('legf5_k0',['python3',str(ROOT/'session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py'),B]),('gate_f4',['python3',str(ROOT/'session_2026-07-18/legf4/scripts/gate_f4.py'),B]),('gate_f5',['python3',str(ROOT/'session_2026-07-18/legf5/scripts/gate_f5.py'),B,str(ROOT/'session_2026-07-18/legf5/sealed_entrant_structure.json')])]
    for n,c in cmds: results.append(run(n,c,E))
    verdict='FAIL' if any(r['exit_code'] for r in results) else 'HARNESS_PASS_MISSING_INVENTORY'
# inventory search static
patterns=['historical','league-total','mid-career','veteran','horizon','pedigree','LTI','retirement','RL_LEGF=0','kill switch','age and evidence','continuity']
inv={}
for pat in patterns:
    p=subprocess.run(['rg','-n','-i',pat,'session_2026-07-18','engine','verify'],cwd=ROOT,text=True,capture_output=True)
    inv[pat]=p.stdout.splitlines()[:20]
# classify manually from located files
classifications=[
['historical -1 -> now','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['historical -2 -> -1','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['±5% league-total gate','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['developing ≥ mid-career ≥ veteran gradient','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['age and evidence continuity','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['horizon cliffs','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['pedigree fading','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['LTI/availability','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['retirement and exit behavior','NOT LOCATED','No unchanged runnable gate located by inventory search.'],
['RL_LEGF=0 kill switch','RERUN PASS' if results and all(r['exit_code']==0 for r in results[:3]) else 'RERUN FAIL','Covered by legf3/4/5 k0 dormancy harnesses.'],
]
(OUT/'gate_results.json').write_text(json.dumps({'verdict':'FAIL','board_b':board_info,'harness_results':[{k:r[k] for k in ['name','command','cwd','env','exit_code']} for r in logs+results], 'gate_inventory':classifications,'search_hits':inv},indent=2))
with open(OUT/'commands_and_logs.txt','w') as f:
    for r in logs+results:
        f.write(f"### {r['name']}\nCOMMAND: {r['command']}\nCWD: {r['cwd']}\nENV: {json.dumps(r['env'],sort_keys=True)}\nEXIT: {r['exit_code']}\n--- STDOUT ---\n{r['stdout']}\n--- STDERR ---\n{r['stderr']}\n\n")
(OUT/'provenance.json').write_text(json.dumps({'start_head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'pr_127_verified_head':'f05ebe6df49b653b053f0ebdd82ddc56ee8d4187','board_b':board_info},indent=2))
