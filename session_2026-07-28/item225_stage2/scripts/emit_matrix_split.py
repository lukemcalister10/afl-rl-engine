"""ITEM 225 STAGE 2 — the evidence matrix, widened for THE SPLIT.

This is emit_matrix.py (LEG-D groundwork, session_2026-07-17) re-run on the CURRENT store, with
three additions and NO method change. The walk-forward ASOF construction, the pw/eq evidence
weights, the retired_now/yend logic and the dedup are carried over VERBATIM in method — the
whole point of stage 2 is that a reader can attribute every difference to the data or the
separation, never to something the seat changed.

WHAT IS ADDED (and why each is forced, not chosen):
  1. `is_pool` / `teaches_curve` — the engine's OWN split predicates (MA.is_pool, MA._teaches_curve),
     quoted rather than re-implemented. Re-implementing them here is the exact defect #217 shipped
     once: a check that watches its own copy of the rule instead of what the engine consumed.
  2. `seasons` — the raw (year, games, avg) rows. The bust-priors target is "best-3 season average
     over seasons with >=6 games, never-established entered as 0.0" and per_entrant.json never
     carried the seasons needed to compute it. Emitted, not derived here, so the fits derive it.
  3. The population is WIDENED past INCURVE={'ND','RD'} to every GRP-eligible row, because the
     RULED POOL is ND 65+, all rookie draft, pre-season draft AND every pickless mechanism. The
     763-row population #217 measured admitted only ND 65+ and RD and dropped the rest; the ruled
     pool is the population here. `type` and `is_pool` let each fit select its own.

READ-ONLY on the engine. Nothing here fits or decides.
"""
import os, sys, io, contextlib, json, hashlib

REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
sys.path.insert(0, REPO + '/vendor')
os.chdir(REPO + '/engine/rl_after')
sys.path.insert(0, '.')

OUT = REPO + '/session_2026-07-28/item225_stage2/out'
os.makedirs(OUT, exist_ok=True)

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_item225_stage2'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; ev = G['ev']; delisted = G['delisted']
_ev_qual = G['_ev_qual']; _ev_pw = G['_ev_pw']; v0_start = G['v0_start']
META = G['_V0CURVE_META']

STORE_MD5 = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()[:8]

BANDS = [tuple(b) for b in MA.BANDS]
def band_of(pk):
    for lo, hi in BANDS:
        if lo <= pk <= hi: return f"{lo}-{hi}"
    return None

INCURVE = {'ND', 'RD'}                      # the OLD in-curve set, kept only to reproduce the old flag
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p)]
best = {}
for p in players:                            # dedup identical to s4_matrix: richest scoring per (key,type,year)
    k = (p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring']) > len(best[k]['scoring']): best[k] = p
players = list(best.values())

# ---- WALK-FORWARD ASOF matrix (life-path; s4_matrix_7147.py:24-42 method, verbatim) ----
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
    print("  ASOF %d done" % Y, flush=True)
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
    pk = MA.effpk(p)
    played = {x['year']: (x['games'], x['avg']) for x in p['scoring'] if x['games'] >= 1}
    last_active = max(played) if played else None
    rn = retired_now(p)
    yend = ((last_active if last_active else C + 1) if rn else 2026); yend = min(yend, 2026)
    yrs = list(range(C + 1, yend + 1)) if yend >= C + 1 else [C + 1]
    Vpath = [ASOF.get((id(p), y)) for y in yrs]
    anchor = ASOF.get((id(p), C + 1))
    pw = {}; gm_by = {}; eq = {}
    for k in range(1, 7):
        Yk = C + k
        Eq = _ev_qual(p, Yk)
        eq[k] = round(Eq, 3); pw[k] = round(_ev_pw(Eq), 4)
        gm_by[k] = sum(x['games'] for x in p['scoring'] if x['year'] <= Yk and x['games'] > 0)
    last_game_year = max((r['year'] for r in p['scoring'] if r.get('games', 0) >= 1), default=None)
    recs.append(dict(
        player=p['player'], key=p.get('key'), type=p.get('type'),
        incurve=(p.get('type') in INCURVE),
        # --- THE SPLIT: the engine's own predicates, quoted not re-implemented ---
        is_pool=bool(MA.is_pool(p)),
        teaches_curve=bool(MA._teaches_curve(p)),
        in_hist=bool(p.get('_ft') and p.get('_grp') in ('ND', 'RD')
                     and 2003 <= (p.get('year') or 0) <= 2021 and p['pos'] in MA.GRP),
        year=C, pick=pk, raw_pick=p.get('pick'), epk=MA._epk(p),
        pickless=bool(p.get('_pickless')), cat=p.get('_cat'),
        band=band_of(pk) if pk else None, pos=MA.gfut(p),
        anchor=(round(anchor, 1) if anchor else None),
        v0=round(v0_start(p), 1),
        cur=(round(ASOF.get((id(p), 2026)), 1) if ASOF.get((id(p), 2026)) else None),
        peak=(round(max([v for v in Vpath if v is not None]), 1) if any(v is not None for v in Vpath) else None),
        vpath=[round(v, 1) if v is not None else None for v in Vpath], yrs=yrs,
        eq=eq, pw=pw, games_by=gm_by, games_yr1=gm_by[1],
        # --- the raw seasons the bust-priors target needs (emitted, not derived here) ---
        seasons=[dict(year=x['year'], games=x['games'], avg=round(x['avg'], 2)) for x in p['scoring']],
        games_total=sum(x['games'] for x in p['scoring']),
        debut=(MA.debut(p) if played else None),
        age_draft=p.get('_by') and (C - p['_by']),
        sat_out_yr1=((C + 1) not in played and bool(played)),
        played_yr1=((C + 1) in played),
        retired_now=rn, delisted=bool(delisted(p)),
        last_game_year=last_game_year, _eff=p.get('_eff'),
    ))

meta = dict(store_md5=STORE_MD5,
            v0surf_sig=META.get('_v0surf_sig'), v0surf_frozen=bool(META.get('_v0surf_frozen')),
            nd_curve_last=MA.ND_CURVE_LAST, pool_pick=MA.POOL_PICK,
            n_records=len(recs))
json.dump(dict(meta=meta, recs=recs), open(OUT + '/per_entrant_split.json', 'w'), indent=0)

nd64 = [r for r in recs if r['type'] == 'ND' and not r['is_pool']]
pool = [r for r in recs if r['is_pool']]
print("exec OK. store=%s  v0surf=%s frozen=%s" % (STORE_MD5, meta['v0surf_sig'], meta['v0surf_frozen']))
print("records=%d   ND 1-64=%d   ruled pool=%d" % (len(recs), len(nd64), len(pool)))
from collections import Counter
print("pool by type:", Counter(r['type'] for r in pool).most_common())
print("wrote out/per_entrant_split.json")
