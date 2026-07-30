import os,io,contextlib,json
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
# model pick value in the board's own currency: val(pick_raw(k)) — gamma-responsive,
# BEFORE the frozen adopted-ladder repoint. This is the pick quantity gamma actually moves.
picks={}
for k in range(1,65):
    r=MA.pick_raw(k)
    picks[k]={'raw':float(r),'val':int(MA.val(r))}
pool=None
try:
    pp=getattr(MA,'POOL_PICK',None)
    if pp is not None:
        r=MA.pick_raw(pp); pool={'pick':int(pp),'raw':float(r),'val':int(MA.val(r))}
except Exception as e:
    pool={'error':str(e)}
print(json.dumps({'GAMMA':MA.GAMMA,'SCALE':MA.SCALE,'picks':picks,'pool':pool,
                  'shipped_PVC':{int(k):int(v) for k,v in MA.PVC.items()}}))
