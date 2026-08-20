import os, sys, json, importlib.util, time
REPO = os.environ['H3REPO']
sys.path.insert(0, os.path.join(REPO, 'engine', 'rl_after', 'ingestion'))
spec = importlib.util.spec_from_file_location('sr_repro', os.path.join(REPO,'engine','rl_after','ingestion','sibling_repin.py'))
m = importlib.util.module_from_spec(spec); sys.modules['sr_repro']=m; spec.loader.exec_module(m)
t=time.time()
res = m._run_sibling_build(REPO, balanced=bool(int(os.environ.get('H3BAL','1'))))
print("ELAPSED %.1fs rc=%s board_md5=%s" % (time.time()-t, res.get('rc'), res.get('board_md5')))
out = os.environ['H3OUT']
open(out+'.stderr','w').write(res.get('stderr') or '')
open(out+'.stdout','w').write(res.get('stdout') or '')
print("ws=", res.get('ws'), "base=", res.get('base'))
# keep ws for inspection
open(out+'.meta.json','w').write(json.dumps({'rc':res.get('rc'),'board_md5':res.get('board_md5'),'ws':res.get('ws'),'base':res.get('base'),'board_path':res.get('board_path')}))
