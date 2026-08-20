"""Probe 3 — the depth-clock decomposition (Martin) and the score-sensitivity sweep (Kondogiannis/Dolan).

READ-ONLY. No board build. Reports, per player:
  fade30b_clock, o31_played_units, o31_cu (unplayed depth), o31_D (the ruled sitter fade at that depth),
  o41_injured, the D7 parity-guard floor (v_healthy) and whether it binds,
and for the two young players a sweep of the round-23 score.
"""
import io, contextlib, copy, json, os, time

t0 = time.time()
g = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g['MA']; ev = g['ev']
print("LOADED %.1fs  SEASON_FE=%r" % (time.time() - t0, g['SEASON_FE']), flush=True)

FN = {}
for n in ('fade30b_clock', 'o31_played_units', 'o31_cu', 'o31_D', 'o41_injured', 'o41_reversal',
          '_o41_fe', 'o32_delivered', 'fade30b_D', 'o31_fade_D', 'o35_kappa', 'o36_kappa',
          '_entry29b_derived', '_ev_pre43'):
    FN[n] = g.get(n)
D7_FLOOR = g.get('_D7_FLOOR', {})
D7_ROWS = {r['key']: r for r in g.get('_D7_ROWS', [])}
_D7_HEALTHY_KEYS = g.get('_D7_HEALTHY_KEYS', set())
_AVAIL_STATE = g.get('_AVAIL_STATE', {})

out = {'fE': g['SEASON_FE'], 'FADE30B_D': g.get('FADE30B_D'), 'numeraire': g.get('_F', None)}

NAMES = ['Nicholas Martin', 'Tom Green', 'Darcy Jones', 'Joshua Kelly', 'Jack Viney',
         'Max Kondogiannis', 'Josh Dolan', 'William McCabe', 'Lachie Jaques', 'Lachlan Gulbin',
         'Luke Trainor', 'Clay Hall', 'Sid Draper']


def depth(p):
    k = p['key']; Y = 2026
    r = {}
    for n, fn in FN.items():
        if fn is None or n in ('_ev_pre43', 'fade30b_D', 'o31_fade_D', 'o41_reversal', '_entry29b_derived'):
            continue
        try:
            r[n] = fn(p, Y)
        except Exception as e:
            r[n] = 'ERR:%s' % e
    # healthy counterpart depth (injury sites off for this row)
    sv = _AVAIL_STATE.pop(k, None)
    hc, rh = p.get('_avail_hc', 0.0), p.get('_lti_ret_hc', 0.0)
    p['_avail_hc'] = 0.0; p['_lti_ret_hc'] = 0.0
    _D7_HEALTHY_KEYS.add(k)
    try:
        r['HEALTHY_o31_cu'] = FN['o31_cu'](p, 2026)
        r['HEALTHY_o31_D'] = FN['o31_D'](p, 2026)
        r['HEALTHY_ev'] = FN['_ev_pre43'](p, 2026)
        r['HEALTHY_o41_injured'] = FN['o41_injured'](p)
    finally:
        _D7_HEALTHY_KEYS.discard(k)
        if sv is not None:
            _AVAIL_STATE[k] = sv
        p['_avail_hc'] = hc; p['_lti_ret_hc'] = rh
    r['D7_floor'] = D7_FLOOR.get(k)
    r['D7_row'] = D7_ROWS.get(k)
    r['ev'] = ev(p)
    r['ev_pre43'] = FN['_ev_pre43'](p, 2026)
    r['floor_binds'] = (r['D7_floor'] is not None and r['D7_floor'] > r['ev_pre43'])
    try:
        r['fade_at_cu'] = FN['fade30b_D'](r['HEALTHY_o31_cu'])
    except Exception as e:
        r['fade_at_cu'] = 'ERR:%s' % e
    for n in ('o35_kappa', 'o36_kappa'):
        try:
            r[n] = FN[n](p)
        except Exception as e:
            r[n] = 'ERR:%s' % e
    try:
        yd = max((x['year'] for x in p['scoring'] if x.get('games') and FN['o32_delivered'](p, 2026, x)),
                 default=None)
        r['last_delivered_year'] = yd
        if yd is not None:
            xd = next(x for x in p['scoring'] if x['year'] == yd)
            r['delivered_games'] = xd['games']
            r['o41_reversal(r)'] = FN['o41_reversal'](float(xd['games']))
            r['c_pre'] = max(0.0, FN['fade30b_clock'](p, yd) - FN['o31_played_units'](p, yd))
    except Exception as e:
        r['deliver_err'] = str(e)
    return r


for nm in NAMES:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        out[nm] = 'MISSING'; continue
    out[nm] = depth(p)
    print("%-18s cu=%-8s D=%-8s ev=%-10s floorbinds=%s" %
          (nm, round(out[nm].get('HEALTHY_o31_cu', -1), 4) if isinstance(out[nm].get('HEALTHY_o31_cu'), float) else out[nm].get('HEALTHY_o31_cu'),
           round(out[nm].get('HEALTHY_o31_D', -1), 5) if isinstance(out[nm].get('HEALTHY_o31_D'), float) else out[nm].get('HEALTHY_o31_D'),
           round(out[nm]['ev'], 2), out[nm]['floor_binds']), flush=True)

# ---- score sweep: what a round-23 score of X would have done ----
SWEEP = {}
for nm, base_games, base_avg_prev in [('Max Kondogiannis', 9, 36.6), ('Josh Dolan', 9, 50.09)]:
    p = next(x for x in MA.data if x['player'] == nm)
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == 2026)
    res = {}
    # (a) the counterfactual with NO round-23 game at all (9 games, previous average)
    row['games'] = base_games; row['avg'] = base_avg_prev
    res['no_r23_game'] = {'games': base_games, 'avg': base_avg_prev, 'ev': ev(p)}
    # (b) sweep the round-23 score
    for sc in [0, 20, 30, 40, 48, 55, 60, 71, 80, 90, 100, 110, 120, 140]:
        row['games'] = base_games + 1
        row['avg'] = round((base_games * base_avg_prev + sc) / (base_games + 1), 2)
        res['score_%d' % sc] = {'avg': row['avg'], 'ev': ev(p)}
    p['scoring'] = saved
    res['restored_ok'] = (ev(p) == out.get(nm, {}).get('ev'))
    SWEEP[nm] = res
    print("SWEEP %s done restored=%s" % (nm, res['restored_ok']), flush=True)
out['SWEEP'] = SWEEP

json.dump(out, open(os.environ['PROBE_OUT'], 'w'), indent=1, default=str)
print("WROTE", os.environ['PROBE_OUT'], flush=True)
