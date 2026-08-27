"""THE CANDIDATE-WORLD EMITTER — the standing 29C emitter, copied, with THE CANDIDATE DELTA.

  Source: docs/evidence/landing_29_2026-08-13/noarb29c/emit_matrix_29c.py, copied byte-for-byte and
  edited ONLY at the sites below. Purpose: the owner's standing no-arb tables under the ruled
  candidate (register v873-v875): S_LL5G smoothing + the evidence-conditional retention surface at
  conservative/0.40/0.92. The walk-forward therefore prices EVERY as-of year under the candidate
  laws, which is what W2 and the rails require.

THE CANDIDATE DELTA — three sites, inserted at the one seam right after the engine load and the
ORIGINAL replication proof:
  SITE A  the BASE-WORLD PROOF RUNS FIRST, UNCHANGED (the unsmoothed law must reproduce the
          published board day-0 EXACTLY — proving the copy's arithmetic before any delta applies);
          THEN the smoothed posv (S_LL5G_POSV.json) replaces BOTH the engine's G['_POSV'] and this
          emitter's local _POSV — one curve, two readers, no mixed basis.
  SITE B  G['o31_pi'] is wrapped with the RULED surface, AS-OF-AWARE: tenure, the class test and
          the cameo-quality cell are all read relative to the year being priced (Yv), exactly as the
          built lever will behave in a walk-forward. Cells = v869 conservative line; knots
          0.40/0.525/0.65; tall ceiling 0.92; class = no >=6-game season as of Yv, tenure 2-4 at Yv,
          entry age <22.
  SITE C  the output filename becomes per_entrant_CANDIDATE.json.
  NOT applied, disclosed: the draft-price cap (a price-level rule; <=9 rows at 2026, negligible to
  cohort rails; exact in the built lever) and the pending fade-law pieces (step-up, depth-3, easing
  sizing) which land at the build.
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

# ==== ORDER 29C — THE LANDED ENTRY LAW (the ONE declared change; see this file's header) ==========
from collections import Counter as Counter0      # aliased: the file's own `Counter` import stays put
# This block computes the year-0 column, PROVES it against the board's own printed day-0 numbers
# BEFORE any record is written, and HALTS if the proof fails. It writes no record field.
_PL_F = G['_PL_F']
_V2J = G['_V2J']
_POSV = {_g: {int(_k): float(_v) for _k, _v in _d.items()} for _g, _d in _V2J['nd_v0']['posv'].items()}

_STANDING_EMITTER = os.environ.get(
    'RL_STANDING_EMITTER', os.path.join(REPO, 'docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py'))
_STANDING_MD5 = hashlib.md5(open(_STANDING_EMITTER, 'rb').read()).hexdigest()
if _STANDING_MD5 != 'bffde2f786be85037483e9f5f1563068':
    raise SystemExit("ORDER 29C HALT: the STANDING emitter is not the file this copy was taken from "
                     "(md5 %s). The 'one declared change' claim is only checkable against the original; "
                     "it is not asserted over a moved target." % _STANDING_MD5)


def _landed_v0_board(p):
    """The row's OWN derived day-0 v0 in BOARD currency, by the ORDER 29B law. Returns None when the
    row is not an entrant object under the law — the caller COUNTS that, never defaults it."""
    if p.get('_pool'):
        return float(MA.pool_v0_of(p))           # the ONE accessor; halts on an unsigned cell
    _pk = p.get('pick')
    if p.get('type') == 'ND' and _pk and 1 <= int(_pk) <= MA.ND_CURVE_LAST:
        _row = _POSV.get(MA.gfut(p))
        if _row is None:
            return None                          # a position the artifact does not publish
        return float(_row[int(_pk)])
    return None


def _landed_v0_engine(p):
    """ENGINE currency, which is the currency `vpath` is already in — so the ratio the instruments
    form at yr0->yr1 is finally a ratio of two prices on the SAME ruler. This is the whole act."""
    _b = _landed_v0_board(p)
    return None if _b is None else _b * _PL_F


# ---- THE REPLICATION PROOF, run before a record is written. FAIL-CLOSED. -------------------------
# For the 89 currently wired entrants the board itself published the answer (DAY0_29B_FINAL.json,
# board 36d5dfc7). If this file's arithmetic is not THE SAME ARITHMETIC, every historical year-0 it
# computes is worthless, so the emit refuses to proceed rather than produce a plausible matrix.
_DAY0 = os.environ.get('RL_DAY0_FINAL',
                       os.path.join(REPO, 'docs/evidence/landing_29_2026-08-13/DAY0_29B_FINAL.json'))
_d0 = json.load(open(_DAY0))
_bykey = {q.get('key'): q for q in MA.data}
_rep_ok = 0
_rep_mis = []
for _row in _d0['rows']:
    _q = _bykey.get(_row['key'])
    _mb = None if _q is None else _landed_v0_board(_q)
    if _mb is not None and int(round(_mb)) == _row['printed'] and abs(_mb - _row['derived_v0']) == 0.0:
        _rep_ok += 1
    else:
        _rep_mis.append((_row['key'], _row['printed'], _mb))
if _rep_ok != len(_d0['rows']) or _rep_mis:
    raise SystemExit(
        "ORDER 29C HALT (replication): %d of %d wired entrants reproduce the board's printed day-0 at "
        "tolerance 0. Mismatches: %s. The year-0 column is only the landed law if it reproduces the "
        "law's own published output EXACTLY; a partial match is a DIFFERENT law and must not be "
        "emitted as this one." % (_rep_ok, len(_d0['rows']), _rep_mis[:10]))
print("ORDER 29C REPLICATION: %d of %d wired entrants on board %s reproduce printed day-0 EXACTLY "
      "(tolerance 0, on the printed integer AND the unrounded derived_v0)"
      % (_rep_ok, len(_d0['rows']), _d0['board_md5'][:8]))
# ==== END OF THE ORDER 29C BLOCK =================================================================

# ==== THE CANDIDATE DELTA (register v873-v875) ===================================================
_SLL5G = json.load(open(os.path.join(REPO, 'docs/evidence/curve_smooth_study_2026-08-25/S_LL5G_POSV.json')))
_POSV_S = {_g: {int(_k): float(_v) for _k, _v in _d.items()} for _g, _d in _SLL5G['posv'].items()}
if set(_POSV_S) != set(_POSV):
    raise SystemExit('CANDIDATE HALT: smoothed posv position set differs from the artifact.')
_POSV = _POSV_S                    # SITE A: this emitter's own year-0 law reads the smoothed curve
G['_POSV'] = _POSV_S               #         and so does the engine's day0_v0 — one curve, two readers
print('CANDIDATE DELTA: S_LL5G posv swapped into BOTH readers (engine + emitter).')

_TALLS = {'RUCK', 'KPF', 'KPD'}
_LT = {('MOBILE', 0): [0.31, 0.19, 0.45, 0.41], ('MOBILE', 1): [0.01, 0.00, 0.66, 0.66],
       ('TALL', 0):   [0.70, 0.21, 0.92, 0.92], ('TALL', 1):   [0.25, 0.00, 0.67, 0.67]}
_orig_pi = G['o31_pi']

def _cand_in_class(p, Yv):
    _yr = int(p.get('year') or 0)
    _t = Yv - _yr + 1
    if not (2 <= _t <= 4):
        return False
    _by = p.get('_by')
    if not _by or _yr - int(_by) >= 22:
        return False
    return not any(x.get('games', 0) >= 6 for x in (p.get('scoring') or []) if x.get('year', 0) <= Yv)

def _cand_L(p, Yv):
    _fam = 'TALL' if MA.gfut(p) in _TALLS else 'MOBILE'
    _era = 1 if (Yv - int(p.get('year') or Yv) + 1) >= 4 else 0
    _t = _LT[(_fam, _era)]
    _sc = [x for x in (p.get('scoring') or []) if x.get('year', 0) <= Yv]
    _g = sum(x.get('games', 0) for x in _sc)
    if _g == 0:
        return _t[0]
    _rel = (sum(x['avg'] * x['games'] for x in _sc) / _g) / MA.REPL[MA.gfut(p)]
    _lo, _mid, _hi = 0.40, 0.525, 0.65
    if _rel <= _lo: return _t[1]
    if _rel <= _mid: return _t[1] + (_t[2] - _t[1]) * (_rel - _lo) / (_mid - _lo)
    if _rel <= _hi: return _t[2] + (_t[3] - _t[2]) * (_rel - _mid) / (_hi - _mid)
    return _t[3]

def _cand_pi(p, Yv, g=None, _Dov=None):        # SITE B: the ruled surface, AS-OF-AWARE
    _v = _orig_pi(p, Yv, g, _Dov)
    if _cand_in_class(p, Yv):
        return max(_v, _cand_L(p, Yv))
    return _v

G['o31_pi'] = _cand_pi
print('CANDIDATE DELTA: the ruled retention surface wrapped into o31_pi (as-of-aware).')
# ==== END OF THE CANDIDATE DELTA ==================================================================

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
# ORDER 29C: the day-0 position key's SOURCE, censused rather than assumed (see the header).
_gfut_src = Counter0('_futpos' if p.get('_futpos') else ('_pos_now' if p.get('_pos_now') else 'pos')
                     for p in players)
# ORDER 29C: rows the landed law cannot map are EXCLUDED and COUNTED. They are never defaulted to the
# position-blind ladder and never carried at a stale surface value, because either would put a row in
# the matrix on a basis this act does not claim.
_unmappable = [dict(key=p.get('key'), player=p.get('player'), type=p.get('type'), pick=p.get('pick'),
                    pickless=bool(p.get('_pickless')), pool=bool(p.get('_pool')), pos=MA.gfut(p))
               for p in players if p.get('year') is not None and _landed_v0_engine(p) is None]
_unmappable_keys = {u['key'] for u in _unmappable}
for p in players:
    C = p.get('year')
    if C is None: continue
    if p.get('key') in _unmappable_keys: continue        # ORDER 29C: excluded, and counted above
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
        # ORDER 29C SITE 1 — THE ONE DECLARED CHANGE. Was `round(v0_start(p), 1)`, the FROZEN FITTED
        # SURFACE, which made this column a pre-landing object while `vpath` beside it is the landed
        # `ev()` — the mixed basis the brief exists to cure. It is now the LANDED ENTRY LAW's own
        # day-0 price, in the same engine currency as `vpath`, proven against the board's 89 printed
        # day-0 numbers above. The `round(·, 1)` convention is CARRIED, not changed.
        v0=round(_landed_v0_engine(p), 1),
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
            emitter=dict(file='docs/evidence/landing_29_2026-08-13/noarb29c/emit_matrix_29c.py',
                         copied_from='docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py',
                         copied_from_md5=_STANDING_MD5,
                         rule_source='engine/rl_after/s4_matrix_M1v7.py:53-70,81,113',
                         rule_commit='30996f8',
                         workdir=WORKDIR),
            # ---- ORDER 29C: the one declared change, and everything a reader needs to check it ----
            basis_29c=dict(
                declared_change='the v0 column is the LANDED ENTRY LAW day-0 price, not v0_start(p)',
                law='ND in-curve -> nd_v0.posv[gfut][pick]; pool -> pool_v0_of(p) cell; x _PL_F',
                law_source='engine/rl_after/_merged_recover.py, ORDER 29B block, commit 13cbebb',
                currency='ENGINE (board currency x _PL_F); the numeraire s is already inside both objects',
                PL_F=_PL_F,
                anchor_factor=float(_V2J['pool_v0']['anchor_factor']),
                borrowed_cells=sorted(_V2J['pool_v0'].get('borrowed_cells') or {}),
                replication_board=_d0['board_md5'],
                replication_ok=_rep_ok, replication_n=len(_d0['rows']), replication_tolerance=0,
                gfut_source_census=dict(_gfut_src),
                n_unmappable=len(_unmappable), unmappable=_unmappable,
                years_1_to_7_untouched=True,
                rounding='round(.,1) CARRIED from the standing emitter; the VALUE changed, not the schema',
                brief='#334 comment 5289123976', prereg='noarb29c/PREREG_29C.md'))
_outpath = os.path.join(OUT, 'per_entrant_CANDIDATE.json')   # SITE C: the candidate matrix
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
print("ORDER 29C year-0 basis: LANDED ENTRY LAW (was v0_start, the frozen fitted surface)")
print("ORDER 29C gfut source census (all STORE columns, so the key is as-of invariant): %s"
      % dict(_gfut_src))
print("ORDER 29C unmappable rows EXCLUDED AND COUNTED: %d%s"
      % (len(_unmappable),
         ("" if not _unmappable else "  -> %s" % [(u['key'], u['type'], u['pick']) for u in _unmappable])))
_z = [r for r in recs if r['v0'] == 0]
print("ORDER 29C year-0 == 0 rows (the artifact's own declared ruck_floor_63_64): %d %s"
      % (len(_z), [(r['key'], r['pos'], r['raw_pick']) for r in _z]))
print("wrote %s" % _outpath)
