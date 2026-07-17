"""LEG-D GROUNDWORK — master evidence matrix (READ-ONLY on the engine; one exec).
Emits per-entrant records that Jobs 2 (circularity), 3 (survivorship), 4c (sample counts) read.

NOTHING here fits or decides. It re-quotes the engine's OWN quantities on the current base
(store 0efdc5d6, legc-relay head 6306378) so the tables are internally consistent. Player VALUES
will move again (R106.7 in flight) — treat every number as design evidence, provisional, never a fit.

Definitions taken VERBATIM from the engine (no re-invention):
 * anchor  = ASOF[C+1]  = END OF CALENDAR YEAR 1 as-of value (s4_matrix_7147.py:62; pvc_fit.py:2-3).
 * pw      = _ev_pw(_ev_qual(p, C+k)) = the engine's pedigree-par weight at the end of career-year k
             (_merged_recover.py:186-189) — 1.0 at zero football evidence, fading to residual 0.11.
             This IS the position/pick-adjusted PRIOR SHARE the model applies in level space.
 * retired_now / delisted / sat_out_yr1 : reused from s4_matrix_7147.py:44-66 verbatim in spirit.
Walk-forward: _ev_qual filters year<=Y internally (line 183); ASOF truncates every player's scoring
to <=Y and resets BASE_REF (leak-free), exactly as s4_matrix does.
"""
import os, sys, io, contextlib, json, math
sys.path.insert(0, '/home/user/afl-rl-engine/vendor')
os.chdir('/home/user/afl-rl-engine/engine/rl_after')
sys.path.insert(0, '.')
import numpy as np

OUT = '/home/user/afl-rl-engine/session_2026-07-17/legd_derivation/out'
os.makedirs(OUT, exist_ok=True)

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_legd_derivation'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; ev = G['ev']; era = G['era']; delisted = G['delisted']
_ev_qual = G['_ev_qual']; _ev_pw = G['_ev_pw']; v0_start = G['v0_start']
REF = G.get('REF', 100)
BANDS = [tuple(b) for b in MA.BANDS]
def band_of(pk):
    for lo, hi in BANDS:
        if lo <= pk <= hi: return f"{lo}-{hi}"
    return None

INCURVE = {'ND', 'RD'}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p)]
# dedup identical to s4_matrix: keep the richest scoring per (key,type,year)
best = {}
for p in players:
    k = (p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring']) > len(best[k]['scoring']): best[k] = p
players = list(best.values())

# ---- WALK-FORWARD ASOF matrix (life-path; s4_matrix_7147.py:24-42 method) ----
ASOF = {}
for Y in range(2003, 2027):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        LL = p.get('_last_listed'); RET = p.get('_retired')
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], RET, LL)
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        eff_last = LL if LL is not None else (lastscore if RET else None)
        p['_retired'] = False
        p['_last_listed'] = eff_last if (eff_last is not None and eff_last < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        try:
            with contextlib.redirect_stdout(io.StringIO()): ASOF[(id(p), Y)] = ev(p, Y)
        except Exception: ASOF[(id(p), Y)] = None
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()

def retired_now(p):  # s4_matrix_7147.py:44-47 verbatim
    if delisted(p): return True
    lg = max((r['year'] for r in p['scoring'] if r.get('games', 0) >= 1), default=None)
    dy = p.get('year')
    return bool(lg is not None and dy is not None and dy <= 2021 and lg <= 2024)

recs = []
for p in players:
    C = p.get('year')
    if C is None: continue
    incurve = p.get('type') in INCURVE
    pickless = bool(p.get('_pickless'))
    pk = MA.effpk(p)
    played = {x['year']: (x['games'], x['avg']) for x in p['scoring'] if x['games'] >= 1}
    last_active = max(played) if played else None
    rn = retired_now(p)
    yend = ((last_active if last_active else C + 1) if rn else 2026); yend = min(yend, 2026)
    yrs = list(range(C + 1, yend + 1)) if yend >= C + 1 else [C + 1]
    Vpath = [ASOF.get((id(p), y)) for y in yrs]
    anchor = ASOF.get((id(p), C + 1))
    # pw (prior share) + games by end of career-year k, k=1..6, walk-forward
    pw = {}; gm_by = {}; eq = {}
    for k in range(1, 7):
        Yk = C + k
        Eq = _ev_qual(p, Yk)
        eq[k] = round(Eq, 3); pw[k] = round(_ev_pw(Eq), 4)
        gm_by[k] = sum(x['games'] for x in p['scoring'] if x['year'] <= Yk and x['games'] > 0)
    last_game_year = max((r['year'] for r in p['scoring'] if r.get('games', 0) >= 1), default=None)
    recs.append(dict(
        player=p['player'], key=p.get('key'), type=p.get('type'), incurve=incurve,
        year=C, pick=pk, pickless=pickless, cat=p.get('_cat'),
        band=band_of(pk) if pk else None, pos=MA.gfut(p),
        anchor=(round(anchor, 1) if anchor else None),
        v0=round(v0_start(p), 1),
        cur=(round(ASOF.get((id(p), 2026)), 1) if ASOF.get((id(p), 2026)) else None),
        peak=(round(max([v for v in Vpath if v is not None]), 1) if any(v is not None for v in Vpath) else None),
        vpath=[round(v, 1) if v is not None else None for v in Vpath], yrs=yrs,
        eq=eq, pw=pw, games_by=gm_by,
        games_yr1=gm_by[1],
        sat_out_yr1=((C + 1) not in played and bool(played)),
        played_yr1=((C + 1) in played),
        retired_now=rn, delisted=bool(delisted(p)),
        last_game_year=last_game_year,
        _eff=p.get('_eff'),
    ))

json.dump(recs, open(OUT + '/per_entrant.json', 'w'), indent=0)
incurve_curve = [r for r in recs if r['incurve'] and r['pick'] and 2004 <= r['year'] <= 2024]
print(f"exec OK. eligible={len(players)}  records={len(recs)}")
print(f"in-curve derivation pool (ND/RD, pick, 2004-2024) = {len(incurve_curve)}")
print(f"  sat-out-yr1 = {sum(1 for r in incurve_curve if r['sat_out_yr1'])}")
print(f"  zero games by end-yr1 = {sum(1 for r in incurve_curve if r['games_yr1']==0)}")
print("wrote out/per_entrant.json")
