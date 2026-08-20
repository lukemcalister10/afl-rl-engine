"""READ-ONLY single-player decomposition probe (no board build, no build lock).

Loads the engine in-process against the CURRENT (R23) store + season state, then for each
target player reports the FINAL board-currency ev() under a 2x2:
    { scoring vector: R22-side | R23-side }  x  { M3_FE (calendar progress): 0.92 | 0.96 }
plus the two arms of the M3 in-progress clock blend (click = clocks advanced, pin = clocks held
a year back), the M3 scope s, and the evidence-weight quantities.

Nothing is written to the repo. Every mutation is restored and round-trip asserted.
"""
import io, contextlib, copy, json, time, os

t0 = time.time()
g = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g['MA']; ev = g['ev']
print("LOADED in %.1fs" % (time.time() - t0), flush=True)
print("SEASON_FE=%r  M3_FE=%r  M3_DEN=%r" % (g['SEASON_FE'], g['M3_FE'], g['M3_DEN']), flush=True)
print("store rows=%d" % len(MA.data), flush=True)

_ev_click = g['_ev_click']; _M3PIN = g['_M3PIN']; _m3_s = g['_m3_s']

TARGETS = ['Nicholas Martin', 'Max Kondogiannis', 'William McCabe', 'Josh Dolan']
COMPARE = ['Tom Green', 'Darcy Jones', 'Joshua Kelly', 'Lachie Jaques', 'Luke Trainor',
           'Lachlan Gulbin', 'Sid Draper', 'Clay Hall']

R22 = {p['key']: p for p in json.load(open(os.environ['R22_STORE']))}
FE_LIVE = g['M3_FE']

out = {}


def _at_fe(p, fe):
    sv = g['M3_FE']
    g['M3_FE'] = fe
    try:
        return ev(p)
    finally:
        g['M3_FE'] = sv


def snap(p):
    r = {}
    r['ev'] = ev(p)
    r['ev_fE_0.92'] = _at_fe(p, 0.92)
    r['ev_fE_0.96'] = _at_fe(p, 0.96)
    r['ev_fE_1.00'] = _at_fe(p, 1.00)
    r['click_pre43'] = _ev_click(p, 2026)
    _M3PIN['on'] = True
    try:
        r['pin_pre43'] = _ev_click(p, 2026)
    finally:
        _M3PIN['on'] = False
    r['s'] = _m3_s(p, 2026)
    r['games2026'] = sum(x['games'] for x in p['scoring'] if x['year'] == 2026)
    r['avg2026'] = [x['avg'] for x in p['scoring'] if x['year'] == 2026]
    try:
        Eq = g['_ev_qual'](p, 2026)
        r['Eq'] = Eq
        r['ev_rec(Eq)'] = g['_ev_rec'](Eq)
        r['ev_est(Eq)'] = g['_ev_est'](Eq)
        r['ev_pw(Eq)'] = g['_ev_pw'](Eq)
    except Exception as e:
        r['Eq'] = 'ERR:%s' % e
    for fn in ('_lvlcurr', '_par_prior'):
        try:
            r[fn] = g[fn](p, 2026)
        except Exception as e:
            r[fn] = 'ERR:%s' % e
    for fn in ('bestlvl', 'v0_start', 'draftval'):
        try:
            r[fn] = g[fn](p)
        except Exception as e:
            r[fn] = 'ERR:%s' % e
    try:
        r['nseas_pro'] = g['nseas_pro'](p)
    except Exception as e:
        r['nseas_pro'] = 'ERR:%s' % e
    return r


for nm in TARGETS + COMPARE:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        out[nm] = {'MISSING': True}
        print("MISSING", nm, flush=True)
        continue
    rec = {'key': p['key'], 'pick': p.get('pick'), 'draft_year': p.get('year'), 'type': p.get('type'),
           'pos_drafted': p.get('drafted_position'), 'pos_now': p.get('present_position'),
           'pos_fut': p.get('future_position'), 'career_games': p.get('games'),
           'scoring_r23': copy.deepcopy(p['scoring'])}
    rec['R23_row'] = snap(p)
    old = R22.get(p['key'])
    rec['scoring_r22'] = copy.deepcopy(old['scoring']) if old else None
    if old is not None and json.dumps(old['scoring']) != json.dumps(p['scoring']):
        saved = copy.deepcopy(p['scoring'])
        p['scoring'] = copy.deepcopy(old['scoring'])
        rec['R22_row'] = snap(p)
        p['scoring'] = saved
        rec['roundtrip_ok'] = (ev(p) == rec['R23_row']['ev'])
    else:
        rec['R22_row'] = None
        rec['store_row_identical'] = True
        rec['roundtrip_ok'] = True
    out[nm] = rec
    print("DONE %-18s ev=%-6s  fE.92=%-6s fE.96=%-6s fE1.0=%-6s  s=%.3f  rt=%s"
          % (nm, rec['R23_row']['ev'], rec['R23_row']['ev_fE_0.92'], rec['R23_row']['ev_fE_0.96'],
             rec['R23_row']['ev_fE_1.00'], rec['R23_row']['s'], rec['roundtrip_ok']), flush=True)

json.dump(out, open(os.environ['PROBE_OUT'], 'w'), indent=1, default=str)
print("WROTE", os.environ['PROBE_OUT'], "total %.1fs" % (time.time() - t0), flush=True)
