import os,io,json,contextlib
with contextlib.redirect_stdout(io.StringIO()): import rl_model as MA
print(json.dumps({'RL_PICK1':os.environ.get('RL_PICK1','<unset>'),
 'SCALE':round(float(MA.SCALE),6),
 'PVC_1':MA.PVC.get(1),'PVC_64':MA.PVC.get(64),
 'BOARD_FACTOR_implied':round(float(MA.PVC[1])/3000.0,6)}))
