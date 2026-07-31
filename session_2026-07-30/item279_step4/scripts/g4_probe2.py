import os,sys,io,contextlib,importlib.util
FV=os.environ['RL_FV']; WHICH=sys.argv[1]; LO,HI=int(sys.argv[2]),int(sys.argv[3]); GATE=float(sys.argv[4])
if FV not in sys.path: sys.path.insert(0,FV)
path = os.environ['ORIG_PB'] if WHICH=='original' else os.path.join(FV,'par_build.py')
spec=importlib.util.spec_from_file_location('pb_'+WHICH,path); m=importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()): spec.loader.exec_module(m)
m.DRAFT_LO,m.DRAFT_HI,m.MIN_GAMES = LO,HI,GATE
try:
    F=m.fit(); print("NO HALT — counts: %s"%{g:int(F['POS'][g].shape[0]) for g in m.GROUPS})
except SystemExit as e: print("SystemExit — LOUD HALT:\n%s"%e)
except Exception as e: print("%s — BARE, names nothing: %s"%(type(e).__name__,e))
