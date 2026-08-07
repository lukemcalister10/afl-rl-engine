import os,sys,io,contextlib,json
REPO=os.environ['RL_REPO']; sys.path.insert(0,REPO+'/vendor'); os.chdir('/home/claude/rl_workspace/rl_after'); sys.path.insert(0,'.')
src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
G={'__name__':'_qc'}
with contextlib.redirect_stdout(io.StringIO()): exec(src,G)
MA=G['MA']
out={}
for p in MA.data:
    if G['_isreal'](p): out[p.get('key')]=G['ev'](p,2026)
tag=os.environ.get('QC_TAG','x')
json.dump(out,open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/qc_%s.json'%tag,'w'))
print(tag,"PED_BAR",G['PED_BAR'],"n",len(out),"sum",sum(out.values()),"mraz",out.get('noah-mraz'))
