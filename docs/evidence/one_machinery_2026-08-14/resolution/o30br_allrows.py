#!/usr/bin/env python3
"""ALL-804 EMISSION of the RESOLVED configuration (additive reading, v0 object, JOINED lanes).

Wrapper over o30br_resolved.py -- imports the committed module and re-runs its own book() arithmetic
per row, emitting every row instead of the nine named ones. NO new pricing logic: sigma/beta_at/b_lift
and the lane rules are the module's. Written because the owner ruled (2026-08-15, in-session) that no
ruling surface is complete without the full board: "you tell me not to judge the preview board yet cite
this resolution packet/additive pricing, but don't provide a board for me to reference."
Control: the emitted total must equal RESOLVED_ROWS.json's 'RESOLVED: additive, v0, JOINED' total.
"""
import importlib.util, json, math, sys
spec = importlib.util.spec_from_file_location('o30br_resolved', 'o30br_resolved.py')
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
rows_out = []
tot = 0.0
for r in M.MOV['rows']:
    v0 = r['v0_step1_board']; D = r['fade_D']; c = r['fade_clock']
    Pp = r['production_pts']; g = r['games_sigma_axis'] or 0.0
    V = v0
    if r['day0'] or Pp is None:
        pr = V * D; ln = 'sitter'
    elif g <= 10:
        pr = V * D * M.b_lift(g, c); ln = 'thin'
    elif g < 16:
        thin10 = V * D * M.b_lift(10, c)
        d16 = Pp + M.beta_at(16) * V
        t = (math.log1p(g) - math.log1p(10)) / (math.log1p(16) - math.log1p(10))
        pr = thin10 + t * (d16 - thin10); ln = 'bridge'
    else:
        pr = Pp + M.beta_at(g) * V; ln = 'deep'
    tot += pr
    rows_out.append(dict(key=r['key'], name=r['name'], pathway=r['pathway'], pick=r['pick'],
        pos=r['pos'], age=r['age'], cg=r['cg'], pool=r['pool'], lane=ln,
        live=r['live'], step2=r['step2'], preview=r['preview'], resolved=round(pr, 1),
        d_vs_step2=round(pr - (r['step2'] or 0), 1)))
ctrl = json.load(open('RESOLVED_ROWS.json'))['book']['RESOLVED: additive, v0, JOINED']['total']
assert abs(tot - ctrl) < 0.5, (tot, ctrl)
json.dump(dict(control_total=ctrl, emitted_total=tot, rows=rows_out),
          open('RESOLVED_ALLROWS.json', 'w'), indent=1)
print('emitted 804 rows | total %.1f == control %.1f' % (tot, ctrl))
