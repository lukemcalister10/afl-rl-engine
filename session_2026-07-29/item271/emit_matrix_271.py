"""ITEM 271 STAGE B — the evidence matrix, carried from #225 stage 2's emit_matrix_split.py.

Method is carried VERBATIM: the walk-forward ASOF construction, the pw/eq evidence weights, the
retired_now/yend logic and the dedup are unchanged, because the acceptance criterion is that a reader
can attribute every difference to the data or the separation, never to something this seat changed.

WHAT THIS ADDS, and why each is forced by a ruling rather than chosen:

  1. THE FORCE-MAJEURE SLIDE (#271 item 5 + owner ruling Q-B, register v533 verbatim). Thomas Boyd
     (ND 2013 pick 1 KPF) and Paddy McCartin (ND 2014 pick 1 KPF) are dropped from the fit populations
     outright, and EVERY player in those two drafts slides up one pick. Q-B is explicit that the slide
     is computed BEFORE the ND/pool split, so the curve fit, the pool level and the both-directions
     exclusion checks all see ONE membership -- which means a natural pick 65 slides to 64, ENTERS the
     ND 1-64 curve fit and correspondingly LEAVES the pool.

     The engine has its own exclude-and-slide facility (`_pvc_exclude` -> `_pvc_eff` -> `_epk`,
     rl_model.py:276-288) but it is documented "curve attribution only": `is_pool` reads the UNSLID
     `effpk`, so a slid pick-65 row keeps `_pool=True` and still cannot teach the curve. That is not
     what Q-B ruled, and Q-B put the slide HERE ("the slide lives in the evidence-matrix builder"),
     so the engine is left untouched -- no method change, no store edit.

     Membership after the slide is derived by applying the engine's OWN load-time rule
     (rl_model.py:257-258) to the slid pick, rather than by inventing a second rule.

  2. PER-SEASON FIT BARS (#271 item 2 + Addendum 6). Each season carries the bar `MA._fit_bar(p, year)`
     returns -- the eligibilities COLUMN for the live season, that season's own row for a closed one.
     The helper is QUOTED from the engine, never re-implemented here: re-implementing a rule inside the
     instrument that checks it is the defect #217 shipped once.

READ-ONLY on the engine and on the store. Nothing here fits, decides, or writes a store.
"""
import os, sys, io, contextlib, json, hashlib

REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
sys.path.insert(0, REPO + '/vendor')
os.chdir(REPO + '/engine/rl_after')
sys.path.insert(0, '.')

OUT = REPO + '/session_2026-07-29/item271/out'
os.makedirs(OUT, exist_ok=True)

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_item271_stageB'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; ev = G['ev']; delisted = G['delisted']
_ev_qual = G['_ev_qual']; _ev_pw = G['_ev_pw']; v0_start = G['v0_start']
META = G['_V0CURVE_META']

STORE_MD5 = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()[:8]

# ---- 1. THE SLIDE, applied before anything reads a population -----------------------------------
FORCE_MAJEURE = {'thomas-boyd': 2013, 'paddy-mccartin': 2014}
_fm_rows = {}
for _k, _y in FORCE_MAJEURE.items():
    _r = next((p for p in MA.data if p.get('key') == _k), None)
    if _r is None or _r.get('type') != 'ND' or _r.get('year') != _y or _r.get('pick') != 1:
        raise SystemExit("HALT: %s does not match the sealed identification (ND %s pick 1) -- Q-B "
                         "requires a STOP on mismatch, not a guess." % (_k, _y))
    _fm_rows[_k] = _r
SLIDE_YEARS = set(FORCE_MAJEURE.values())

def slid_pick(p):
    """The fit-input pick. Unchanged outside the two drafts; inside them every remaining player moves
    up one slot behind the excluded pick-1 row. The STORE is never written."""
    if p.get('year') not in SLIDE_YEARS or p.get('type') != 'ND' or not p.get('pick'):
        return p.get('pick')
    cut = _fm_rows['thomas-boyd' if p['year'] == 2013 else 'paddy-mccartin']['pick']
    return p['pick'] - 1 if p['pick'] > cut else p['pick']

def slid_membership(p):
    """(eff_pick, is_pool) under the slid pick, derived by APPLYING THE ENGINE'S OWN load-time rule
    (rl_model.py:257-258) -- ND inside 1..ND_CURVE_LAST keeps its pick, anything past it collapses to
    the single pool index. Outside the two drafts the engine's own values are quoted unchanged."""
    if p.get('year') not in SLIDE_YEARS or p.get('type') != 'ND' or not p.get('pick'):
        return MA.effpk(p), bool(MA.is_pool(p))
    pk = slid_pick(p)
    if pk is not None and 1 <= pk <= MA.ND_CURVE_LAST:
        return pk, False
    return MA.POOL_PICK, True

BANDS = [tuple(b) for b in MA.BANDS]
def band_of(pk):
    for lo, hi in BANDS:
        if lo <= pk <= hi: return f"{lo}-{hi}"
    return None

INCURVE = {'ND', 'RD'}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p) and p.get('key') not in FORCE_MAJEURE]
best = {}
for p in players:
    k = (p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring']) > len(best[k]['scoring']): best[k] = p
players = list(best.values())

# ---- WALK-FORWARD ASOF matrix (carried verbatim from #225 stage 2) ------------------------------
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

def retired_now(p):
    if delisted(p): return True
    lg = max((r['year'] for r in p['scoring'] if r.get('games', 0) >= 1), default=None)
    dy = p.get('year')
    return bool(lg is not None and dy is not None and dy <= 2021 and lg <= 2024)

recs = []
for p in players:
    C = p.get('year')
    if C is None: continue
    eff_slid, pool_slid = slid_membership(p)
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
        # the engine's own predicates, quoted (pre-slide) ...
        is_pool_engine=bool(MA.is_pool(p)), teaches_curve_engine=bool(MA._teaches_curve(p)),
        # ... and the SLID membership the fits actually consume (Q-B)
        is_pool=pool_slid,
        teaches_curve=bool(p.get('type') == 'ND' and not pool_slid and MA._in_pvc(p)),
        slid=bool(p.get('year') in SLIDE_YEARS and p.get('type') == 'ND'),
        pick_stored=p.get('pick'), pick_slid=slid_pick(p),
        in_hist=bool(p.get('_ft') and p.get('_grp') in ('ND', 'RD')
                     and 2003 <= (p.get('year') or 0) <= 2021 and p['pos'] in MA.GRP),
        year=C, pick=eff_slid, raw_pick=p.get('pick'), epk=MA._epk(p),
        pickless=bool(p.get('_pickless')), cat=p.get('_cat'),
        band=band_of(eff_slid) if eff_slid else None, pos=MA.gfut(p),
        anchor=(round(anchor, 1) if anchor else None),
        v0=round(v0_start(p), 1),
        cur=(round(ASOF.get((id(p), 2026)), 1) if ASOF.get((id(p), 2026)) else None),
        peak=(round(max([v for v in Vpath if v is not None]), 1) if any(v is not None for v in Vpath) else None),
        vpath=[round(v, 1) if v is not None else None for v in Vpath], yrs=yrs,
        eq=eq, pw=pw, games_by=gm_by, games_yr1=gm_by[1],
        # seasons now carry THAT SEASON'S BAR, quoted from the engine helper (item 2 + Addendum 6)
        seasons=[dict(year=x['year'], games=x['games'], avg=round(x['avg'], 2),
                      pos=x.get('pos'), bar=MA._fit_bar(p, x['year'])) for x in p['scoring']],
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
            force_majeure=sorted(FORCE_MAJEURE), slide_years=sorted(SLIDE_YEARS),
            n_records=len(recs))
json.dump(dict(meta=meta, recs=recs), open(OUT + '/per_entrant_271.json', 'w'), indent=0)

nd64 = [r for r in recs if r['teaches_curve']]
pool = [r for r in recs if r['is_pool']]
crossers = [r for r in recs if r['slid'] and r['is_pool_engine'] and not r['is_pool']]
print("exec OK. store=%s  v0surf=%s frozen=%s" % (STORE_MD5, meta['v0surf_sig'], meta['v0surf_frozen']))
print("records=%d   ND 1-64 (teaches curve)=%d   ruled pool=%d" % (len(recs), len(nd64), len(pool)))
print("force-majeure excluded: %s" % sorted(FORCE_MAJEURE))
print("boundary crossers (pool -> ND fit via the slide): %s" % [r['player'] for r in crossers])
from collections import Counter
print("pool by type:", Counter(r['type'] for r in pool).most_common())
print("wrote out/per_entrant_271.json")
