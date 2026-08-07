"""ITEM 271 STAGE B EMITTER, RE-ISSUED ON THE #338 CORRECTED TENURE BASIS (owner word 2026-08-06).

PROVENANCE OF THIS FILE
  Source          : session_2026-07-29/item271/emit_matrix_271.py   (COPIED, byte-for-byte, then edited
                    only at the sites listed under THE #338 DELTA below). The original session file is
                    FILED HISTORY and is NOT touched by this act.
  #338 basis      : commit 30996f8 "#338 minimum listing tenure implemented in the walk-forward book —
                    4/3/2 by pick band, own data extends, known facts override; board byte-unchanged
                    113b36f8; book of record refreshed", which changed
                    engine/rl_after/s4_matrix_M1v7.py at exactly two sites, adding three helpers.
  Why this exists : the per_entrant lineage that feeds the no-arb tables (docs/evidence/noarb_2026-08-05)
                    was emitted by the PRE-#338 construction. The walk-forward book of record now carries
                    the minimum-tenure rule; the per_entrant matrix did not. Two constructions, one
                    claimed-identical method, is the defect. This emitter closes it.

  Everything else in this file is carried VERBATIM from emit_matrix_271.py — the force-majeure slide,
  the pw/eq evidence weights, the dedup, the per-season fit bars, the record schema. The acceptance
  criterion is unchanged: a reader can attribute every difference to the #338 rule, never to something
  this seat changed on the side.

THE #338 DELTA — THREE HELPERS ADDED, TWO SITES CHANGED
  The helpers `_min_tenure` / `_debut_year` / `_listed_through` are ported from
  engine/rl_after/s4_matrix_M1v7.py:53-70 with NO logic difference. Only the surrounding style is
  adapted to this file's spacing conventions; the predicates, the constants (4 / 3 / 2), the band
  boundaries (<=20, <=40, else), the MSD debut convention and the max()/known-fact precedence are
  identical expressions.

  SITE 1 — the walk-forward ASOF loop (was emit_matrix_271.py:107):
      -  eff_last = LL if LL is not None else (lastscore if RET else None)
      +  eff_last = _listed_through(p, lastscore)
    `lastscore` is 0 for a career the source DB kept no rows for, so such a player reconstructed as
    DELISTED at every as-of year and ev() returned the 2% remnant before any machinery ran.

  SITE 2 — the emitted window (was emit_matrix_271.py:136):
      -  yend = ((last_active if last_active else C + 1) if rn else 2026)
      +  yend = max(last_active or 0,
      +             _listed_through(p, max((r['year'] for r in p['scoring']), default=0)) or 0) if rn else 2026
    A retired player's window now runs to his LISTED-THROUGH year, not his last PLAYED year: the tenure
    years after his last game are LISTED sitting-out years and must be EMITTED to be priced at all. A
    played year is never truncated (the max), and a player with neither data nor tenure still falls back
    to the single [C+1] row on the `yrs` line, exactly as before.

  Note that `RET` is still read at site 1 (it is part of the save/restore triple); it is simply no longer
  consulted for `eff_last`, because `_listed_through` reads `p['_retired']` itself. This mirrors the
  committed s4 change, which likewise left the `RET` binding in place.

ONE DELIBERATE READING, DISCLOSED
  `_min_tenure` bands on `MA.effpk(p)` — the ENGINE'S OWN pick — exactly as the committed helper does.
  It does NOT band on this file's force-majeure `slid_pick`. That is deliberate and it is the
  conservative reading: #338 is a claim about how long a drafted player was really ON A LIST, which is a
  fact about his actual draft position; the Q-B slide is a fit-population device for the curve, not an
  assertion that anyone was drafted a slot earlier. Porting the helper verbatim also keeps this emitter's
  rule byte-comparable with the book of record's. The emitter REPORTS how many records would band
  differently under the alternative reading, so the choice is measured rather than asserted.

READ-ONLY on the engine and on the store. Nothing here fits, decides, or writes a store.
"""
import os, sys, io, contextlib, json, hashlib

# The gate workspace is the run target (the repo moved; bootstrap.sh reseeds it). RL_WORKDIR overrides.
REPO = os.environ.get('RL_REPO', '/home/user/afl-rl-engine')
WORKDIR = os.environ.get('RL_WORKDIR', '/home/claude/rl_workspace/rl_after')
VENDOR = os.environ.get('RL_VENDOR', REPO + '/vendor')
sys.path.insert(0, VENDOR)
os.chdir(WORKDIR)
sys.path.insert(0, '.')

OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
os.makedirs(OUT, exist_ok=True)

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_noarb338_emit'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, G)
MA = G['MA']; ev = G['ev']; delisted = G['delisted']
_ev_qual = G['_ev_qual']; _ev_pw = G['_ev_pw']; v0_start = G['v0_start']
META = G['_V0CURVE_META']

STORE_MD5 = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()[:8]
ENGINE_HEAD = hashlib.md5(open('_merged_recover.py', 'rb').read()).hexdigest()[:8]

# ---- 1. THE SLIDE, applied before anything reads a population (VERBATIM from #271) ---------------
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

# ==== #338 MINIMUM LISTING TENURE (owner word "Fire 338", 2026-08-06) ============================
# PORTED VERBATIM from engine/rl_after/s4_matrix_M1v7.py:53-70 (commit 30996f8). See this file's
# header for the defect, the rule and the two changed sites.
# THE RULE: a drafted player is on a list for a minimum tenure whether or not the DB kept his numbers.
# With NO explicit `_last_listed`: assumed-listed-through = debut + N - 1, where debut is the route's
# own convention (entry year + 1 on every route except MSD -- a mid-season draftee debuts in his ENTRY
# year) and N = 4 for ND picks 1-20, 3 for ND 21-40, 2 for everything else (ND 41+ and every pool
# route). OWN DATA EXTENDS: listed-through = max(assumed, last scoring year). An explicit
# `_last_listed` is a KNOWN FACT and stands, even when it is shorter than the minimum. Active players
# are untouched. A year inside listed tenure with no scoring row is a LISTED SITTING-OUT year --
# priced by the EXISTING sit-out machinery, no new pricing rule here.
MIN_TENURE_BANDS = {'ND 1-20': 4, 'ND 21-40': 3, 'ND 41+ and every pool route': 2}

def _min_tenure(p):
    """#338: minimum listed seasons implied by the entry route/pick band."""
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2                        # ND 41+ and every pool route (RD/MSD/SSP/UNR/IRE/PDA/PDN/PDS)

def _debut_year(p):
    """#338: first season ON A LIST. MSD debuts in its entry year; every other route the year after."""
    C = p.get('year')
    return None if C is None else (C if p.get('type') == 'MSD' else C + 1)

def _listed_through(p, lastscore):
    """#338: the year the player's listing runs through, or None if he is still listed (active,
    untouched)."""
    LL = p.get('_last_listed')
    if LL is not None: return LL    # known fact -- stands even if shorter than the minimum
    if not p.get('_retired'): return None   # active: no listed-through, untouched by this rule
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)  # own data extends

def _min_tenure_slid(p):
    """DISCLOSURE ONLY -- never consumed. The alternative reading of the band, on the Q-B slid pick,
    so the header's deliberate choice is measured rather than asserted."""
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = slid_membership(p)[0]
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2

_band_reading_diff = [p.get('key') for p in players if _min_tenure(p) != _min_tenure_slid(p)]

# ---- WALK-FORWARD ASOF matrix (carried verbatim from #225 stage 2; ONE #338 site) ----------------
ASOF = {}
for Y in range(2003, 2027):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        LL = p.get('_last_listed'); RET = p.get('_retired')
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], RET, LL)
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        # #338 SITE 1 (2026-08-06): was `LL if LL is not None else (lastscore if RET else None)` --
        # lastscore is 0 for an evidence-less career, so the player was delisted at every as-of year.
        # Now the minimum listing tenure. Ported from s4_matrix_M1v7.py:81 (commit 30996f8).
        eff_last = _listed_through(p, lastscore)
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
n_extended = 0
for p in players:
    C = p.get('year')
    if C is None: continue
    eff_slid, pool_slid = slid_membership(p)
    played = {x['year']: (x['games'], x['avg']) for x in p['scoring'] if x['games'] >= 1}
    last_active = max(played) if played else None
    rn = retired_now(p)
    # #338 SITE 2 (2026-08-06): a retired player's window runs to his LISTED-THROUGH year, not his
    # last PLAYED year -- the tenure years after his last game are LISTED sitting-out years and must
    # be emitted to be priced at all. Was `(last_active if last_active else C + 1) if rn else 2026`;
    # a played year is never truncated (max), and a player with neither data nor tenure still falls
    # back to the single [C+1] row on the `yrs` line below. Ported from s4_matrix_M1v7.py:113.
    _old_yend = min(((last_active if last_active else C + 1) if rn else 2026), 2026)
    yend = max(last_active or 0,
               _listed_through(p, max((r['year'] for r in p['scoring']), default=0)) or 0) if rn else 2026
    yend = min(yend, 2026)
    if yend != _old_yend: n_extended += 1
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
        # #338 disclosure, per record: the tenure the rule assigned and the window it produced.
        min_tenure_338=_min_tenure(p),
        window_extended_338=bool(yend != _old_yend),
        last_game_year=last_game_year, _eff=p.get('_eff'),
    ))

meta = dict(store_md5=STORE_MD5,
            engine_head=ENGINE_HEAD,
            v0surf_sig=META.get('_v0surf_sig'), v0surf_frozen=bool(META.get('_v0surf_frozen')),
            nd_curve_last=MA.ND_CURVE_LAST, pool_pick=MA.POOL_PICK,
            force_majeure=sorted(FORCE_MAJEURE), slide_years=sorted(SLIDE_YEARS),
            n_records=len(recs),
            basis='#338 minimum listing tenure (owner word 2026-08-06)',
            rule_338=dict(min_tenure_by_band=MIN_TENURE_BANDS,
                          debut_convention='entry year + 1 on every route except MSD (entry year)',
                          own_data_extends=True,
                          explicit_last_listed_is_a_known_fact=True,
                          active_players_untouched=True,
                          banded_on='MA.effpk (engine pick), NOT the Q-B slid pick — see emitter header',
                          n_records_window_extended=n_extended,
                          n_records_band_differs_under_slid_reading=len(_band_reading_diff),
                          keys_band_differs_under_slid_reading=sorted(x for x in _band_reading_diff if x)),
            emitter=dict(file='docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py',
                         copied_from='session_2026-07-29/item271/emit_matrix_271.py',
                         rule_source='engine/rl_after/s4_matrix_M1v7.py:53-70,81,113',
                         rule_commit='30996f8',
                         workdir=WORKDIR))
_outpath = os.path.join(OUT, 'per_entrant_338_confirmation.json')
json.dump(dict(meta=meta, recs=recs), open(_outpath, 'w'), indent=0)

nd64 = [r for r in recs if r['teaches_curve']]
pool = [r for r in recs if r['is_pool']]
crossers = [r for r in recs if r['slid'] and r['is_pool_engine'] and not r['is_pool']]
print("exec OK. store=%s engine=%s v0surf=%s frozen=%s"
      % (STORE_MD5, ENGINE_HEAD, meta['v0surf_sig'], meta['v0surf_frozen']))
print("records=%d   ND 1-64 (teaches curve)=%d   ruled pool=%d" % (len(recs), len(nd64), len(pool)))
print("#338 windows extended: %d of %d records" % (n_extended, len(recs)))
print("#338 band reading differs under the slid pick on %d records: %s"
      % (len(_band_reading_diff), sorted(x for x in _band_reading_diff if x)))
print("force-majeure excluded: %s" % sorted(FORCE_MAJEURE))
print("boundary crossers (pool -> ND fit via the slide): %s" % [r['player'] for r in crossers])
from collections import Counter
print("pool by type:", Counter(r['type'] for r in pool).most_common())
print("wrote %s" % _outpath)
