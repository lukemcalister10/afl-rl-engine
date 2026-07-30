import os,io,contextlib,json,sys
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
out={'GAMMA':MA.GAMMA,'SCALE':MA.SCALE,
     'derived_PVC':{int(k):int(v) for k,v in MA.PVC.items()},
     'POOL_PICK':getattr(MA,'POOL_PICK',None)}
print(json.dumps(out))
