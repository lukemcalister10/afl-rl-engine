import json, numpy as np, math, re, os
def _season_val(_key, _fb):
    """Read a DYNAMIC season-state value (calendar_progress | exposure_pace) from the authoritative
    data/season_state.json (single source; advances weekly).
    FENCED (RL_CONFIG_MODE in bake|gate|canonical): HALT on any of unresolved/untrusted repo root,
    missing file, malformed JSON, missing key, or a non-numeric / non-finite value — a release build
    must never silently fall back to a stale Round-14 default. UNFENCED dev shell: use the fallback."""
    _mode = (os.environ.get('RL_CONFIG_MODE') or '').strip().lower()
    _fenced = _mode in ('bake', 'gate', 'canonical')
    _r = os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR')
    if not _r:
        if _fenced:
            raise RuntimeError("FENCED season-state read (RL_CONFIG_MODE=%s): repo root unresolved "
                               "(RL_REPO/CLAUDE_PROJECT_DIR unset) — cannot load authoritative season state" % _mode)
        _r = '.'
    _p = os.path.join(_r, 'data', 'season_state.json')
    try:
        _v = float(json.load(open(_p))[_key])
        if _v != _v or _v in (float('inf'), float('-inf')):
            raise ValueError("non-finite %s=%r" % (_key, _v))
        return _v
    except Exception as _e:
        if _fenced:
            raise RuntimeError("FENCED season-state read (RL_CONFIG_MODE=%s): cannot load %r from %s (%s)"
                               % (_mode, _key, _p, _e)) from _e
        return float(_fb)
import pgrid   # establishment-P surface (Praw + mat_mult); ported onto the board 2026-06-21 (was compute.py-only)
from unidecode import unidecode
data=json.load(open('rl_model_data.json')); P=json.load(open('params.json')); PMD=json.load(open('rl_passmark.json'))
# --- POSITION MODEL (DPP STRIP 2026-07-05, final consolidation): the DPP weighted-blend is DELETED. The store
#   now carries THREE clean SINGLE-VALUED columns (no probabilistic legs anywhere):
#   drafted_position : career/draft position -> drives the cohort curves (the engine's internal p['pos'])
#   present_position : the player's CURRENT position -> the YEAR-0 leg of his own valuation (p['_pos_now'])
#   future_position  : the player's SETTLED FUTURE position -> the YEARS-1+ leg + curve/peak/runway (p['_futpos'])
# Pricing reads present_position for the year-0 REPL bar (bnow) and future_position for the years-1+ REPL bar
# and the peak/curve (gfut). In THIS build future_position == present_position for every player, so bnow==gfut
# and every player resolves as a single position -- but the SEAM is live: a later transition model can populate
# future_position where it should differ from present, with no schema change and no code change. The old
# raw_multipos blend (futblend weights, gfut multi-leg, _fut list) is GONE; each dual is collapsed to its
# primary (present/dominant) leg. See evidence/dpp_strip/ for the full re-pricing.
for _p in data:
    _p['pos']=_p['drafted_position']
    _pp=_p.get('present_position')
    _p['_pos_now']=_pp if (_pp and _pp!=_p['pos']) else None
    _p['_futpos']=_p.get('future_position') or _pp    # single settled-future position (fallback to present)
    # LEG C flex (RL_FLEX, item 20b / flex spec §1.2): a player MAY carry ONE dual primary/alternate FUTURE
    # stream — an alternate_position + its probability p_dual_stream (0-100). Parsed once here; consumed by
    # futblend()'s years-1+ REPL blend. Absent on non-dual rows (the store carries it on the 90 dual rows).
    _ap=_p.get('alternate_position'); _pd=_p.get('p_dual_stream')
    _p['_altpos']=(_ap if (_ap and _pd) else None)
    _p['_pdual']=(float(_pd)/100.0 if (_ap and _pd) else 0.0)
# --- MSD/IRE credit machinery SCRUBBED 2026-07-05 (Luke directive, one-source rewire) ------------
# The v3.3.1 MSD mid-season debut standardisation (MSD_Y1_MULT=1.5x debut-year game boost, folded into
# the career total) is DELETED, together with the four credit/bust phantom rows and the _double_count /
# _phantom apparatus. Real mid-season draftees are now priced from their raw recorded games -- no boost,
# no labelled replacement. See evidence/f1f2_rewire/ for the before/after decomposition.
# ------------------------------------------------------------------------------------------------
PEAK=P['PEAK']; PEAK_AGE=P['PEAK_AGE']; pm_pos=PMD['pm_pos']; pm_band={int(k):v for k,v in PMD['pm_band'].items()}; BANDS=PMD['bands']; NB=len(BANDS)
AGE_CURVE={g:{int(a):f for a,f in c.items()} for g,c in P.get('AGE_CURVE',{}).items()}   # per-position empirical age curve (Phase-2 dev projection only; present value() untouched)
def _smooth_tail(c):                                   # enforce monotonic non-increasing post-peak + >=1%/yr continued decline (kills thin-tail plateaus/blips, e.g. RUCK holding flat at 35)
    if not c: return c
    pk=max(c,key=c.get); out=dict(c)
    for a in sorted(c):
        if a>pk: out[a]=min(c[a], out[a-1]-0.010)
    return out
AGE_CURVE={g:_smooth_tail(c) for g,c in AGE_CURVE.items()}
GRP={'MID':'MID','RUCK':'RUCK','SF':'SF','KPF':'KPF','SD':'SD','KPD':'KPD'}   # ITEM 262: identity since the store now speaks the engine's own vocabulary. Kept as the dispatch boundary, NOT redundant. The pre-262 'SD'->'SD' back-catalogue alias is retired: all 136 rows were migrated to SD.
# A player's CAREER/draft position (p['pos']) drives his contribution to the cohort curves.
# An optional p['_pos_now'] is his CURRENT position and drives only his own active valuation
# (e.g. Dangerfield: drafted+developed a MID -> feeds the MID pool; plays FWD now -> valued as a forward).
def _pos_present(p): return GRP.get(p.get('_pos_now')) or GRP[p['pos']]   # the DECLARED present position (this was bnow pre-#271); gfut's fallback stays on this axis
# ITEM 271 item 3, as narrowed by the seam audit's correction 1 and finally ruled at #271 Addendum 4: the YEAR-0
# replacement bar is read from the `eligibilities` COLUMN -- the owner-maintained CURRENT declaration -- not from
# present_position, and not from the 2026 season row. The column is NOW; a season row is THAT SEASON'S record, and
# they are different questions with different sources (the column runs richer for young players: Lalor is SF,MID in
# the column against MID in the row). Season rows remain the per-season FIT bars, 2026 included -- see _fit_bar.
# This cures the recorded Ginbey mechanism, where present position won by default because the bar could not engage.
# A dual declaration collapses under R105.1 (_collapse_elig, :108) and takes the pair's LOWER REPL -- the engine's
# OWN existing eligibility law, the same rule y0dpp_bar applies at :137, which is why §1b RETIRES from the year-0
# path by supersession: the bar now does at source, from the very column §1b always read, what §1b did partially.
# §1b is superseded, NOT deleted -- its code is untouched. Empty column -> plain position (a future-record
# fallback; zero rows exercise it today). THE FUTURE LEG DOES NOT MOVE (correction 1): gfut keeps _pos_present.
def _elig_bar(p):
    es=_collapse_elig(p.get('eligibilities'))
    return min(es,key=lambda g:REPL[g]) if es else None
def _decl_bar(p): return _elig_bar(p) or _pos_present(p)           # the CURRENT declaration's bar; empty column -> plain position
# ITEM 271 item 2 + Addendum 6 — THE BAR FOR ANY SEASON, and the ONE source rule for every bar-taking use
# (the per-season fit, the evidence matrix, career value feeding pick outcomes). Owner word: while the CURRENT
# season is LIVE its bar comes from the eligibilities COLUMN, because the column is the live declaration and the
# season row is only that season's record-so-far; the 2026 row's `pos` remains the sheet's record but sets NO bar
# while the season runs. A CLOSED season (2025 and earlier) is settled, so it takes its OWN row. A closed season
# with no row falls back to the column. This is the bar axis only -- the MODELLING-POSITION axis that drives the
# curve family, peak and runway is gfut and is untouched by this helper.
# LIVE_SEASON is a FIXED FACT ABOUT THE WORLD -- which season is currently being played -- and must NOT be
# BASE_REF, which MOVES: the walk-forward re-values every player as-of 2003..2026 and the back/forward boards
# re-anchor it. Keying off BASE_REF would make every as-of year "live" and read the column for all of them,
# which is precisely what item 2 forbids -- a 2015 season would be measured on a 2026 declaration.
LIVE_SEASON=2026
def _fit_bar(p,Y):
    if Y is None or Y>=LIVE_SEASON: return _decl_bar(p)            # the live season -> the column
    r=next((x for x in p.get('scoring') or [] if x.get('year')==Y),None)
    if r and r.get('pos'):
        es=_collapse_elig(r['pos'].replace('/',','))               # season rows separate on '/', the column on ','
        if es: return min(es,key=lambda g:REPL[g])
    return _decl_bar(p)                                            # a closed season with no row -> the column
# The year-0 bar IS the fit bar read at the season being valued. On the live board BASE_REF==LIVE_SEASON so this
# is the column (Addendum 4); in the walk-forward BASE_REF is the as-of year, so each historical season is
# measured against ITS OWN eligibility row -- which is what makes item 2 true in the fit rather than only stated.
def bnow(p): return _fit_bar(p,BASE_REF)
def gfut(p):                                  # SETTLED FUTURE position (single) -> drives curve/peak/runway + years-1+ REPL
    fp=p.get('_futpos')
    if fp: return GRP.get(fp) or _pos_present(p)
    return _pos_present(p)                    # no future_position (e.g. gate synths) -> present position
_FLEX=os.environ.get('RL_FLEX','1')!='0'       # LEG C kill-switch (RL_ISOFADE pattern): RL_FLEX=0 => single-position stubs => board byte-exact base. Declared exception, not a dial. Gates ALL of Leg C incl. §1b.
def futblend(p):
    # DPP-STRIP base: the years-1+ leg is a SINGLE position (future_position). LEG C flex (RL_FLEX, §1 ruled
    # stream semantics): a dual primary/alternate stream swaps the years-1+ REPLACEMENT BAR for the LOWER of
    # the pair (the MAX law) on a p_dual fraction of the stream. The PRIMARY keys peak/curve/runway/key-premium
    # (g=gfut(p) unchanged upstream); ONLY the bar in the years-1+ posval sum moves. The lower bar gives posval
    # >= the primary-bar posval, so the netting is FLOORED >=0 by construction. RL_FLEX=0 (or a row with no
    # dual) => [(gfut,1.0)] => the years-1+ leg is byte-identical to the base board. This is the VALUE blend.
    pri=gfut(p)
    if not _FLEX: return [(pri,1.0)]
    ap=p.get('_altpos'); q=p.get('_pdual',0.0)
    if not ap or q<=0.0: return [(pri,1.0)]
    alt=GRP.get(ap) or pri
    low=alt if REPL.get(alt,REPL[pri])<REPL[pri] else pri   # LOWER replacement bar of the {primary,alternate} pair
    return [(pri,1.0-q),(low,q)]
def futstreams(p):
    # BOARD-LABEL blend (fut-label fix, item 271): the board's stream array must carry the TRUE alternate
    # label regardless of the bar comparison (futblend collapses the alt->pri when REPL[alt]>=REPL[pri], which
    # is right for VALUE but drops the alternate provenance on the board). Same weights as futblend; the
    # position label is the TRUE alternate. RL_FLEX=0 => [(gfut,1.0)] => byte-exact display.
    pri=gfut(p)
    if not _FLEX: return [(pri,1.0)]
    ap=p.get('_altpos'); q=p.get('_pdual',0.0)
    if not ap or q<=0.0: return [(pri,1.0)]
    return [(pri,1.0-q),(GRP.get(ap) or pri,q)]
# ==== §1b — THE CURRENT-SEASON DPP LAW (item 275, BINDING; RL_FLEX-gated) — the eligibility-collapse helper.
# A player's OFFICIAL current-season dual positions (the store `eligibilities`, collapsed per R105.1: a
# KEY-listed position DROPS its matching GEN — KPF absorbs SF, KPD absorbs SD; <=2 remain) apply to
# the YEAR-0 LEG ONLY. The year-0 REMAINING-SEASON component nets vs whichever post-collapse bar is MORE
# VALUABLE for him (the LOWER REPL); the banked component + the level path stay keyed to present (bnow). The
# SEASON_PROG-scaled blend itself is done at v_at_peak (before val(); item 281). Here we only resolve the bar.
_ELIG_MAP={'MID':'MID','RUCK':'RUCK','SF':'SF','KPF':'KPF','SD':'SD','KPD':'KPD'}   # ITEM 262: identity — `eligibilities` no longer uses a separate hyphenated spelling. Kept so _collapse_elig still validates its input.
def _collapse_elig(elig):
    if not elig: return set()
    s={_ELIG_MAP.get(t.strip().upper()) for t in elig.split(',') if t.strip()}
    s.discard(None)
    if 'KPF' in s: s.discard('SF')      # R105.1: K-X absorbs G-X (a KPD also listed SD is NOT a DPP)
    if 'KPD' in s: s.discard('SD')
    return s
# ==== item-284 (DECISIONS v121) — DPP DATA-ERROR classes. Same-line K/G is the SILENT R105.1 listing-artifact
# collapse above (no flag). The FOUR cross-class combos and present_position ∉ the collapsed set are DATA ERRORS:
# the row is treated SINGLE-POSITION for §1b (y0dpp_bar -> None, NO dual bar), REPORTED BY NAME (the registry
# below -> a committed named-row artifact, not a log line), and the build CONTINUES — never a halt. SILENCE IS A
# RED: y0dpp_bar always resolves (a bar or None) and every error row lands in the registry with a verdict.
_CROSS_CLASS={frozenset({'KPD','SF'}),frozenset({'KPF','SD'}),
              frozenset({'RUCK','SF'}),frozenset({'RUCK','SD'})}
_DPP_DATA_ERRORS={}                              # stable_player_id -> dict(player,reason,collapsed,present); deduped
def _flag_dpp_error(p,es,reason):
    sid=p.get('stable_player_id') or ('name:'+(p.get('player') or '?'))
    _DPP_DATA_ERRORS[sid]={'player':p.get('player'),'reason':reason,
                           'collapsed':sorted(es),'present':p.get('present_position'),
                           'eligibilities':p.get('eligibilities')}
def y0dpp_bar(p):
    # The §1b year-0 REMAINING-SEASON replacement bar (GRP value), or None (single-position / no lower bar).
    if not _FLEX: return None
    es=_collapse_elig(p.get('eligibilities'))
    if len(es)<2: return None
    if frozenset(es) in _CROSS_CLASS:            # item-284: cross-class combo -> DATA ERROR -> single-position + named
        _flag_dpp_error(p,es,'cross-class'); return None
    if bnow(p) not in es:                        # item-284: present_position not in the collapsed set -> DATA ERROR
        _flag_dpp_error(p,es,'present-not-in-set'); return None
    low=min(es,key=lambda g:REPL[g])             # lower REPL = more valuable for him
    return low if REPL[low]<REPL[bnow(p)] else None
# Real-life entry mechanisms. National draft ('ND') is the pick scale. Rookie ('RD') extends it.
# The rest entered with NO national slot -> their _eff (pick-equivalent) is derived empirically AFTER the PVC is built.
PICKLESS={'SSP','MSD','IRE','UNR','PDA','PDN','PDS'}
PMAX=0.25
BETA_POS={'MID':1.10,'SD':0.84,'SF':0.98,'KPF':0.92,'KPD':0.63,'RUCK':0.95}
ICPT_POS={'MID':4.08,'SD':1.92,'SF':2.40,'KPF':1.58,'KPD':0.06,'RUCK':2.79}
BUST_BAND={int(k):v for k,v in PMD['BUST_BAND'].items()}
def norm(n): return " ".join(re.sub(r"[^a-z ]"," ",unidecode(n).lower()).split())
def slug(n): return re.sub(r"[^a-z0-9]+","-",unidecode(n).lower()).strip('-')
# birthyear is carried in-data (_by, from the sheet Age col); no fuzzy matching needed.
AGE_REF=2026                          # "now" anchor for the age clock; bumped by forward/back board views (re-ages everyone, leaves demonstrated form fixed). Default 2026 reproduces the shipped values byte-for-byte.
BASE_REF=2026                         # true-now anchor for demonstrated form + scoring truncation. offset=AGE_REF-BASE_REF drives the Phase-2 dev projection; BASE_REF==AGE_REF==2026 reproduces shipped values byte-for-byte.
_LENS_FORM=None                       # LEG E (R103.3 projection law): the forward-lens form anchor. None => balanced/back path (BASE_REF pinned to the eval year, byte-exact). Set to 2026 by rl_export's forward lens so the +1/+2 view runs offset>0 (AGE_REF>BASE_REF) => _dev_advance credits expected production through the map's OWN growth curve (no lens-only growth term; the Reid constraint). k=0 => AGE_REF==BASE_REF => byte-exact.
_LEVEL_OVR=None                       # when set, level_now returns this (used to integrate value over the level distribution in the variance layer); None in all default/parity paths.
def by(p): return p.get('_by') or (p['year']-18)   # FIX: _by can be present-but-None (cont.22 DOB fold-in wrote explicit None for ~302 DOB-less records); .get(key,default) would return None and crash _age_at. Guard like L367.
def _cycle_year(p): return p['year']-(1 if p.get('type')=='MSD' else 0)   # MSD draft_year IS the debut year, so its ND/RD-cycle equivalent is -1; SSP draft_year already IS the cycle year
def _age_at(p,ref): return max(ref-by(p), 18+(ref-_cycle_year(p)))
def age(p): return _age_at(p,AGE_REF)
def debut(p): return p['year'] if p['type']=='MSD' else p['year']+1   # ONLY MSD (mid-season) debuts in its draft_year; ND/RD/SSP AND post-draft signings (PDA/PDN/PDS/IRE/UNR) are off-season -> debut year+1 (fixes 2025 post-draft first-years leaking onto the -1 backward board)
def seasons(p): return max(1,AGE_REF-debut(p))
# ============================================================================================================
# GRACE-A — the entry-age grace on the future-discount ladder.  ORDER 28, owner ruling #334 comment
# 5276077959: "the diminishing seasons only counts from the second season (i.e. age 20 onwards). Same
# implementation as on the curve. And grace A applies for the pool, for the pathways. For everything."
#
# THE RULE: a normal-age entrant (entry age <= 19) carries seasons 1 AND 2 at FULL weight; his THIRD
# season is the first diminished.  An entrant at 20+ gets no grace and is on today's ladder unchanged.
#
# WHY G=1 HERE AND G_O=2 ON THE CURVE.  Two clocks, one rule (PREREG_ORDER28.md §1.1):
#   curve side  k_c = season_year - entry_year, k_c=1 is the FIRST played season and already discounts;
#               exponent max(0, k_c - 2)  =>  seasons 1,2 free.
#   engine side k_e = seasons AHEAD of the pricing year, and k_e=0 is ALWAYS 1.0 (the standing engine
#               convention in disc_factor: the present season is never discounted).  So the engine only
#               needs ONE extra free step, and only for a player whose present season IS his first:
#               exponent max(0, k_e - remaining), remaining = max(0, G - seasons_elapsed), G = 1.
# Checked season by season in the prereg; the consequence is that a 2nd-year-and-later row is
# byte-unchanged even with the dial ON, which is the rule, not an approximation of it.
#
# ENTRY AGE is taken with the SAME arithmetic Layer 1 used (o26b_layer1.py:121, entry_year - _by, with
# the same 18 fallback) so the curve side and the board side select the IDENTICAL population.
# NOT _age_at(): that carries an `18 + (ref - cycle_year)` floor which would shift every off-season
# entrant by a year and silently change who gets grace.  Named here so it cannot be walked into.
#
# DIAL: RL_GRACE, DEFAULT '1' (ON) — ORDER 29, the landing.  Owner ruling #334 comment 5276077959,
# "I think we can lock grace A in ... And also apply it at board level too ... For everything.",
# carried into register v715 and landed here.
#
# IT REMAINS A REAL DIAL; ONLY ITS DEFAULT INVERTS.  RL_GRACE=0 still reproduces the dial-off board
# byte-for-byte on an otherwise-unchanged tree — proven at the landing, not asserted (P4, and the
# control is recorded in docs/evidence/landing_29_2026-08-13/GRACE_DEFAULT.md).  Off => grace_years()
# returns 0 on its first line => disc_factor's exponent is max(0, k - 0) == k => the pre-order power
# form, bit-for-bit.  The grace-A law itself is UNCHANGED from ORDER 28.
#
# RL_GRACE is now carried in data/model_config.json (the pinned manifest).  It has to be:
# config_manifest.enforce() in bake/gate mode clears the ambient model environment and REJECTS
# unknown RL_* overrides, so a canonical landing build would have refused the dial otherwise —
# named in advance as ORDER 28 packet §9.8 and closed here.
RL_GRACE=os.environ.get('RL_GRACE','1')!='0'
GRACE_G=1                              # grace-A: ONE extra free future season for a normal-age entrant
GRACE_MAX_ENTRY_AGE=19                 # entrants at 20+ get no grace (ruled)
def grace_years(p):
    """Remaining grace seasons for player p at the current AGE_REF. 0 when the dial is off."""
    if not RL_GRACE or p is None: return 0
    if (p['year']-by(p))>GRACE_MAX_ENTRY_AGE: return 0
    return max(0,GRACE_G-max(0,AGE_REF-debut(p)))
# ============================================================================================================
# THE PRICING SPLIT — owner ruling, and RULEBOOK v2.1 law 4 (G-MONO) as amended 2026-07-28.
#
#   The national pick curve covers picks 1-64 and descends across that domain; pick 1 = 3000.
#   EVERYTHING PAST 64 ENTERS THE POOL: national 65+, the whole rookie draft, the pre-season draft, and every
#   pickless mechanism (SSP/MSD/IRE/UNR/PDA/PDN/PDS). The pool is valued BY POSITION, and ORDER OF SELECTION
#   CARRIES NO VALUE INSIDE IT.
#
#   THERE IS NO PRICE FOR PICK 70. Every pool entrant sits at ONE index (POOL_PICK). The per-position value
#   comes from the position layer that already exists — iso_corr(pos, pk) — not from where in the pool he went.
#   One index + that layer == one value per position, which is exactly the ruling.
#
#   So: no player's price may vary with a selection number above 64. If you find an _eff above POOL_PICK, or a
#   curve entry past ND_CURVE_LAST, the old 1-99 ladder has come back.
# ============================================================================================================
ND_CURVE_LAST=64          # last pick ON the national curve
POOL_PICK=65              # THE pool index — one index for every pool entrant, priced by position
def effpk(p): return p.get('_eff', POOL_PICK if not p.get('pick') or p['pick']>ND_CURVE_LAST else p['pick'])
def is_pool(p): return bool(p.get('_pool')) or effpk(p)>=POOL_PICK
def bandof(pk):
    for i,(lo,hi) in enumerate(BANDS):
        if lo<=pk<=hi: return i
    return len(BANDS)-1
DEF_CURVE=[56,62,67,71,74,77,79,80,80,79]
def expected(g,band,s):
    s=max(1,min(10,int(s))); c=pm_pos.get('%d|%s'%(band,g)) or pm_band.get(band) or DEF_CURVE; v=c[s-1]
    if v is None:
        vv=[x for x in c if x is not None]; v=vv[min(s-1,len(vv)-1)] if vv else DEF_CURVE[s-1]
    return v
def bandpeak(g,band):
    c=pm_pos.get('%d|%s'%(band,g)) or pm_band.get(band) or DEF_CURVE; vv=[x for x in c if x is not None]; return max(vv) if vv else 75
# ---- empirical basepk & position mix per band ----
def srel(p):
    d=debut(p); o={}
    for r in p['scoring']:
        s=r['year']-d+1
        if 1<=s<=14 and r['games']>=4: o[s]=(r['avg'],r['games'],r['year'])
    return o
def pkbest(p):
    d=debut(p); s=sorted([r['avg'] for r in p['scoring'] if r['games']>=10 and r['year']>=d],reverse=True)[:2]; return float(np.mean(s)) if s else None
# ---- entry classification on REAL pick numbers. ND is the national-pick scale; RD extends it by that
# year's national-pick count. PICKLESS mechanisms (MSD/SSP/Ireland/Unregistered/post-draft) carry NO slot;
# their _eff (pick-equivalent) is derived empirically from realised value AFTER the PVC exists (see below). ----
from collections import Counter as _Cnt
# PICK-CORRECTION (b) 2026-07-11, RE-DERIVED under the OWNER DATA LAW (ii) 2026-07-11: the chaining offset is
# an AUTHORITATIVE per-year LAST-NATIONAL-PICK table (source-stamped sidecar national_draft_last_pick.json),
# replacing the prior inference from the ND row COUNT. Owner convention: rookie/PSD chain onto the database's
# national END, not the row count. The table value is the store's own MAX National ordinal per year (the
# DATABASE UNIVERSE end — owner data law: store ordinals are database-universe with redraft exclusions; the
# real-world/AFL-official count is NOT the authority). The row COUNT equals the MAX only where the sequence is
# gapless (21/23 years); at 2010/2011 gaps (excluded/redrafted players that never consume numbering) make
# count<max, so COUNT would place rookie picks BELOW real national ordinals — MAX is the collision-free end
# (2010=93, 2011=89). Fallback to the row count for any year absent from the table (logged), so the engine
# never silently loses a year.
_NDC_count=dict(_Cnt(p['year'] for p in data if p['type']=='ND'))
try:
    _NDLAST={int(_k):_v for _k,_v in json.load(open('national_draft_last_pick.json'))['last_national_pick'].items()}
except Exception as _e:
    _NDLAST={}; print('WARN: national_draft_last_pick.json unavailable (%r) — falling back to ND row-count offset'%_e)
_NDC={}
for _y in set(_NDC_count)|set(_NDLAST):
    if _y in _NDLAST: _NDC[_y]=_NDLAST[_y]
    else: _NDC[_y]=_NDC_count[_y]; print('WARN: year %s absent from last-national-pick table — using ND row count %d'%(_y,_NDC_count[_y]))
for _p in data:
    _p['_eyr']=_p['year']
    if _p['type']=='ND':
        # THE SPLIT (owner ruling, RULEBOOK v2.1 law 4): the national curve covers picks 1-64. A national
        # selection at 65 or deeper is NOT on the curve — it enters the pool with every other pool entrant.
        _pk=_p['pick'] or 0
        if 1<=_pk<=ND_CURVE_LAST: _p['_ft']=True; _p['_grp']='ND'; _p['_eff']=_pk
        else:                     _p['_ft']=True; _p['_grp']='ND'; _p['_eff']=POOL_PICK; _p['_pool']=True
    elif _p['type']=='RD':
        # THE SPLIT: the rookie draft is pool. The chain onto the national ladder (_eff = last_national_pick +
        # their_pick) is REMOVED — it priced a rookie by his selection order, which the ruling says carries no
        # value. _grp is left at 'RD' deliberately: it governs COHORT membership (hist/BASEPK_REG/establishment/
        # forward valuation), not price, and re-scoping the training cohort is an ITEM 412 question, not this job's.
        _p['_ft']=True; _p['_grp']='RD'; _p['_eff']=POOL_PICK; _p['_pool']=True
    elif _p['type']=='PSD':                                   # Pre-Season Draft
        # THE SPLIT: PSD is a post-national selection, so it is pool. The chain removed with the rookie one above
        # (was: _eff = last_national_pick + psd_slot). Order within the PSD carries no value.
        _p['_ft']=True; _p['_grp']='RD'; _p['_eff']=POOL_PICK; _p['_pool']=True
    else:                                                     # pickless entry mechanism (SSP/MSD/IRE/UNR/PD*)
        # THE SPLIT: pickless mechanisms are pool. Previously a placeholder 75, then overwritten by the
        # PICK-EQUIVALENT (PICKEQ, 90/92) below — both indices ABOVE 64, i.e. the old model. Now the pool index.
        _p['_ft']=False; _p['_grp']=_p['type']; _p['_eff']=POOL_PICK; _p['_pool']=True
# cohort = national draft + first-time RD only (the ND and its extension). MSD/SSP are separate drafts, excluded here.
hist=[p for p in data if p.get('_ft') and p.get('_grp') in ('ND','RD') and 2003<=p['year']<=2021 and p['pos'] in GRP]  # 2003 lower bound (Luke cont.12): folds in the 2003-2005 cohorts; scores comparable at matched experience (no era drift), only ~1% miss a pre-2005 debut season
# --- PVC-pool-only exclusion + slide-up (Luke): players flagged _pvc_exclude are dropped from the PICK-CURVE builders
# (build_pvc / build_pvc_v34 / _natcv34) ONLY; they stay in hist for BASEPK_REG, establishment, and forward valuation,
# so the forward/Now board is byte-identical and they still appear. In the same draft year, remaining players slide UP
# to fill each vacated slot (curve attribution only -- stored pick/effpk untouched). Uses _epk in the curve pools only.
from collections import defaultdict as _dd
_pvc_excl_eff=_dd(list)
for _p in hist:
    if _p.get('_pvc_exclude'): _pvc_excl_eff[_p['year']].append(effpk(_p))
for _p in hist:
    if not _p.get('_pvc_exclude') and _p['year'] in _pvc_excl_eff:
        _e=effpk(_p); _p['_pvc_eff']=_e-sum(1 for _x in _pvc_excl_eff[_p['year']] if _x<_e)
def _in_pvc(p): return not p.get('_pvc_exclude')          # PVC-curve pool membership (forward board unaffected)
def _epk(p):    return p.get('_pvc_eff', effpk(p))         # slid effective pick, curve attribution only
# ============================================================================================================
# THE SPLIT, ADDENDUM 1 (owner, 2026-07-28) — WHO IS ALLOWED TO TEACH THE NATIONAL CURVE.
#
#   "ND pick 64 can only be valued from the outcomes of players who were DRAFTED IN THE NATIONAL DRAFT.
#    Rookies cannot bleed value into the national curve — not by chaining, and not by contributing
#    observations to the fit."
#
# Removing the chaining fixed where a pool entrant SITS. It did not stop his outcome TEACHING the curve.
# Worse: collapsing the pool to ONE index at 65 CONCENTRATED the contamination, because every builder samples
# within +/-4 effective picks, so every pool row landed on picks 61-64 at once instead of spreading to 99.
#
# This is the single gate. Use it at EVERY site that fits or samples the pick curve — fixing one and leaving
# the others is the duplicated-assertion class. It gates the BUILDERS ONLY: _grp stays 'RD', hist is not
# re-scoped, so a pool player is still valued, still on the board, still in BASEPK_REG / establishment /
# forward valuation. He simply stops teaching the national curve.
# ============================================================================================================
def _teaches_curve(p): return _in_pvc(p) and not is_pool(p)
# ---- THE OBSERVED SAMPLE (2026-07-28, after the seam broke two fit sites without the suite noticing) --------
# The first version of the Addendum-1 check RE-IMPLEMENTED the builders' filter inside the selftest and asserted
# on its own copy. That only ever tested the shared helper: break the exclusion at ONE site — _natcv's own line,
# or the build_pvc call site — and the re-implementation still returned a clean set, so the suite stayed green
# while the curve was being taught by pool rows. A check that cannot fail is how a contaminated curve reaches
# the baseline unnoticed, and #225 works in these same sites and has been told to rely on this check.
#
# So the check no longer re-derives anything. Each fit site REGISTERS THE ACTUAL ROW LIST IT SAMPLED, and the
# selftest inspects those recorded populations. Remove the exclusion at any single site and that site's own
# recorded sample contains pool rows, so the assertion fails for that site by name. The selftest also asserts
# the full set of expected sites is present, so deleting a registration is itself a failure.
_CURVE_SAMPLES={}
def _curve_sample(site,k,rows):
    """Register the rows a curve builder is about to consume, and return them unchanged. Records only picks on
    the national curve (k<=ND_CURVE_LAST) — the domain where a pool row is a contamination — so this is bounded.
    Stores references to the builder's own list: it observes, it does not copy or recompute."""
    if k is not None and k<=ND_CURVE_LAST: _CURVE_SAMPLES.setdefault(site,{})[k]=rows
    return rows
CURVE_FIT_SITES=('build_pvc','build_pvc_v34','_natcv','_natcv34','v0_kernel')   # every site that fits/samples the curve
def _rw(y):                                  # v2.1: equal weighting (recency shown immaterial; reverted by request)
    return 1.0
BPK={}; POOL={}; MIX={}
from collections import Counter
# ============================================================================================================
# #336 VARIANT — THE BUST-INCLUSIVE PICK BASELINE.  EXPERIMENT ONLY; branch variant/336-bust-inclusive.
# NEVER MERGED. No pin moves, no artifact ships, no board lands. Issue #336, VARIANT DIRECTIVE 2026-08-06.
#
# THE DEFECT (owner, verbatim): "You can't say busts are counted as busts and then exclude them from the
# sample when it's convenient." / "0 game busts make the history look better than mediocre players."
# The filter below used to read `pkbest(p) is not None`, which excludes 835 of 1,974 hist members (42.3%)
# — every player who never put together a >=10-game season. He is ABSENT, not zero. So the ordering
# best > mediocre > bust maps to measured contributions of "down > invisible", and a strictly worse career
# produces a BETTER-looking baseline. That is the monotonicity breach the law forbids.
#
# MEASURED, on store 37ced3ce, the survivors-only POOL baseline is NON-MONOTONE IN PICK:
#     band  1-3    4-7   8-12  13-20  21-27  28-35  36-48  49-99
#           94.8   85.3  83.9   77.9   74.8   77.5   71.2   72.8      <- RISES at 21-27 -> 28-35 and 36-48 -> 49-99
# The v3.4 clamp at the BASEPK_REG loop below was the patch on that broken sample ("kills the late-pick
# survivorship spike"). It is REMOVED in this variant: keeping it would double-correct, and the repaired
# baseline is required to stand monotone ON ITS OWN or be reported as a red.
#
# THE REPAIR FORM (recorded rule, primer §4.6): each reference cell becomes a true expectation over the
# TENURE-WINDOWED population,
#         E[level]  =  P(establishes)  x  E[level | establishes]
# with never-established players IN THE DENOMINATOR at their realized nothing (0.0).
#
#   establishment : a season of >= QUAL_336 (6) games — the definition at
#                   engine/forward_valuation/build_cohort_book.py:181-185, quoted not re-invented.
#   denominator   : the #338 tenure-windowed population. Every hist member carries a listed window of at
#                   least two seasons under the minimum-listing-tenure rule (4 / 3 / 2 by pick band; helpers
#                   at engine/rl_after/s4_matrix_M1v7.py:53-70, commit 30996f8), so for this CAREER-level
#                   quantity the tenure axis marginalises out and the denominator is the whole (position x
#                   band) cell. "P(establishes)" here is therefore P(EVER establishes inside the window).
#                   The per-tenure strata are derived on the par cohort in forward_valuation/par_build.py.
#   level         : pkbest(p) wherever the engine defines it — UNCHANGED, the top-2 mean of >=10-game
#                   seasons. DISCLOSED SUB-DECISION: 148 of the 1,287 established players have a >=6-game
#                   season but never a >=10-game one, so pkbest is None for them. They are ESTABLISHED, not
#                   busts; scoring them 0 would re-import the very defect at the establishment bar. They
#                   contribute their REALIZED level — the same top-2 mean taken at the >=6-game bar. Every
#                   remaining player (never a >=6-game season) contributes 0.0.
#   pooling       : DELIBERATE AND DECLARED. P is shrunk toward the ALL-POSITION band marginal by
#                   n/(n+K_336), K_336 = 10 pseudo-observations — the same n/(n+k) design par_build already
#                   uses for the ramp. It is not optional: 11 of the 48 (position x band) strata carry n<10
#                   and one carries n=1. The raw counts are recorded on BPK_N / BPK_NEST below so every rate
#                   names its denominator. POOL[b] needs no pooling (min band n = 57) and is taken directly.
#   NOT changed   : the `len(...)>=4` minimum-sample gate on a BPK cell. It is a thin-cell guard, not a
#                   survivorship filter — it does not systematically drop worse careers.
#
# HELD CONSTANT, DELIBERATELY AND DISCLOSED: the frozen year-zero surface. Its signature (_v0surf_sig,
# _merged_recover.py:1324-1330) is blind to these tables and will load the SHIPPED survivors-basis fit.
# That is the ruled basis for this experiment — it isolates the reference-layer effect. The joint
# re-derivation is #334 stage B, after the ruling. No RL_V0SURF_REFIT here.
# ============================================================================================================
# ------------------------------------------------------------------------------------------------------------
# ADDENDUM 1 (issue #336, 2026-08-06) — THIS SITE IS ALREADY ON THE AMENDED FORM, AND IS UNCHANGED BY IT.
# The amendment rules that every level anchor use CAREER-LEVEL P(EVER establishes | position x pick band), with
# tenure entering only as #338 window MEMBERSHIP and never as a probability discount on the anchor. That is
# exactly what _established_336 / _pest_336 below already compute (tenure-marginal, one rate per position x
# band). The site that carried the defect was the PAR SURFACE, whose P was keyed (position x band x TENURE);
# it is amended in engine/forward_valuation/par_build.py. Recorded here so the branch shows both anchors were
# checked against the amendment, not only the one that moved.
QUAL_336 = 6      # establishment bar: a season of >=6 games (build_cohort_book.py:181-185)
K_336    = 10.0   # pooling strength: shrink each (position, band) rate toward the all-position band marginal

# ============================================================================================================
# #336 CHANNEL ABLATION LEVERS — DECLARED MEASUREMENT DIALS, ALL DEFAULT OFF, ALL BYTE-EXACT WHEN OFF.
# Added by #334 ORDER 3 (build brief 5248006413). Precedent for the form: RL_336_DFORCE / RL_336_RFORCE
# already in this file, and RL_ABSENCE at _merged_recover.py:684.
#
# WHY THEY EXIST. DECOMP.txt recorded a real gap: the #336 reference layer owns 80.5% of the main->FULL
# year-1 drop and was THE ONE ITEM IN THE ACT WITH NO DECLARED KILL-SWITCH — its only ablation was a
# whole-commit revert of 9a8bbd9 in a throwaway worktree. These three levers give the layer per-CHANNEL
# switches so the -9.1pp it owns can be attributed rather than left as one lump. They are MEASUREMENT
# levers, not design dials: no owner has ruled any of them on, and nothing here ships.
#
#   RL_336_NOP=1      revert the P-LEG. The unconditional probability factor P(ever establishes) comes off
#                     the pick tables (BPK = E[level|est] instead of P x E[level|est]; POOL becomes the
#                     establisher-only band mean instead of the bust-inclusive one) and the residual
#                     anchor-side discount D goes to 1.0. The de-survivored conditional LEVELS stay.
#                     This is the BUST-CHARGE channel.
#   RL_336_SURVLVL=1  revert the DE-SURVIVORED E-LEVELS. The conditional mean's sample goes back to the
#                     survivor definition (`pkbest(p) is not None`, i.e. a >=10-game season) at the level
#                     pkbest itself, so the 148 established-but-never-10-game players stop teaching; and
#                     the v3.4 late-pick clamp is RESTORED. P is untouched and stays on the >=6-game bar.
#                     This is the HONESTY-REPAIR channel (survivor bias in the level sample).
#   RL_336_PARSURV=1  revert the PAR_BUILD leg — read in engine/forward_valuation/par_build.py, not here.
#
# WHAT THE THREE DO *NOT* SEPARATE, disclosed. Reverting all three together is NOT the same object as the
# whole-commit revert of 9a8bbd9: the amendment-2/3 consumer re-siting (basepk_c -> basepk_c_p at the five
# enumerated sites) stays wired in every arm, because with NOP on, BASEPK_REG == BASEPK_EST and D == 1.0,
# so basepk_c_p collapses to basepk_c IDENTICALLY and the re-siting has no residual effect to strip. The
# gap between the three arms' sum and the whole-commit revert is therefore an interaction residual, and it
# is PRINTED, never normalised away.
#   RL_336_CLAMP=1    restore the v3.4 late-pick clamp on BOTH baseline tables. Held on its OWN lever
#                     rather than folded into RL_336_SURVLVL, because the clamp and the sample are
#                     separable in code and the measurement needs to say WHICH of the two moves the
#                     amendment-2 monotonicity guard. Channel (b) is emitted as SURVLVL=1 CLAMP=1 (the
#                     clamp exists only to patch the spike the survivor sample produces, so reverting the
#                     sample without it would measure a configuration the engine never had).
_NOP_336    = os.environ.get('RL_336_NOP','0')!='0'        # channel (a): the P-leg
_SURVLVL_336= os.environ.get('RL_336_SURVLVL','0')!='0'    # channel (b): the de-survivored E-levels
_CLAMP_336  = os.environ.get('RL_336_CLAMP','0')!='0'      # channel (b) partner: the v3.4 late-pick clamp
# ============================================================================================================

def _established_336(p):
    """Did this player EVER establish inside his listed window? (the ruled definition, >=6 games)"""
    return any(x['games']>=QUAL_336 for x in p['scoring'])

def _level_336(p):
    """The player's REALIZED level. pkbest where the engine defines it (top-2 mean of >=10-game seasons);
    for an established player with no >=10-game season, the same top-2 taken at the ESTABLISHMENT bar so he
    contributes his real number rather than vanishing; never-established -> 0.0, his realized nothing."""
    v=pkbest(p)
    if v is not None: return float(v)
    d=debut(p)
    s=sorted([r['avg'] for r in p['scoring'] if r['games']>=QUAL_336 and (d is None or r['year']>=d)],reverse=True)[:2]
    return float(np.mean(s)) if s else 0.0

BPK_N={}; BPK_NEST={}; BPK_P={}; BPK_COND={}   # disclosure: cell n, n established, pooled P, E[level|est]
POOL_COND336={}                                # #336 AMENDMENT 2: the all-position band E[level|est]
_bnum={}; _bden={}
for b in range(NB):
    _g=[p for p in hist if bandof(effpk(p))==b]
    _bden[b]=len(_g); _bnum[b]=sum(1 for p in _g if _established_336(p))
def _pest_336(g,b):
    """P(ever establishes) for (position, band), shrunk toward the all-position band marginal by n/(n+K)."""
    n=BPK_N.get((g,b),0); k=BPK_NEST.get((g,b),0)
    pbar=(_bnum[b]/_bden[b]) if _bden.get(b) else 0.0
    return (k + K_336*pbar)/(n + K_336)

for b in range(NB):
    grp=[p for p in hist if bandof(effpk(p))==b]   # PICK-CORRECTION (a) 2026-07-11: band pools on the CHAINED effective pick (owner convention), was raw p['pick']. Removes rookie-at-raw contamination (Q2: 657 RD rows, 320 at raw<=20) from the one raw-pick channel on the live board; before/after cited in the eyeball list.
    cc=Counter(gfut(p) for p in grp); MIX[b]={g:cc.get(g,0)/len(grp) for g in sorted(set(GRP.values()))} # ITEM 271 item 4 GROUP B: the TABLE is REBUILT on the played axis (gfut), not the lookup renamed -- cohort_peak/basepk_c already READ it with gfut, so renaming the read alone would have left the two-axis mismatch in place and the build reading clean.
    for g in sorted(set(GRP.values())):
        # #336 VARIANT: was `... for p in grp if gfut(p)==g and pkbest(p) is not None` — the survivorship
        # filter. The cell is now E[level] over the WHOLE (position, band) population: the conditional mean
        # over ESTABLISHERS (the ruled >=6-game definition) times P(establishes) for that stratum. The
        # never-established stay in the denominator at their realized nothing, via the P factor.
        _cell=[p for p in grp if gfut(p)==g]
        BPK_N[(g,b)]=len(_cell); BPK_NEST[(g,b)]=sum(1 for p in _cell if _established_336(p))
        # CHANNEL (b) RL_336_SURVLVL: the CONDITIONAL MEAN's sample reverts to the pre-#336 survivor
        # definition — membership `pkbest(p) is not None` at the level pkbest itself. P's own numerator
        # (BPK_NEST above) is NOT touched: it stays on the ruled >=6-game bar, so channel (b) moves only
        # the E[level|est] leg and channels (a)/(b) stay orthogonal in code.
        if _SURVLVL_336: pw=[(float(pkbest(p)),_rw(p['year'])) for p in _cell if pkbest(p) is not None]
        else:            pw=[(_level_336(p),_rw(p['year'])) for p in _cell if _established_336(p)]
        if len(pw)>=4:                                   # UNCHANGED thin-cell guard (not a survivorship gate)
            _cond=float(np.average([x[0] for x in pw],weights=[x[1] for x in pw]))
            _p=_pest_336(g,b); BPK_P[(g,b)]=_p; BPK_COND[(g,b)]=_cond
            BPK[(g,b)]=_cond if _NOP_336 else _p*_cond   # CHANNEL (a) RL_336_NOP: the P factor comes off the pick table
    # #336 VARIANT: POOL is the all-position band expectation, taken DIRECTLY over the full band population
    # (never-established at 0.0) — no pooling needed, the thinnest band carries n=57.
    # #336 AMENDMENT 2: ew is the same band marginal taken over ESTABLISHERS ONLY — E[level | establishes].
    # It is the gradient donor for the established-conditional BASEPK_EST assembled after BASEPK_REG,
    # exactly as POOL is for BASEPK_REG. Never-establishers are NOT dropped from the world here; they
    # are in P's denominator at their realized nothing, which is the other leg of the identity.
    # (ew is hoisted above POOL only so channel (a) can point POOL at it; its value is unchanged.)
    if _SURVLVL_336:
        aw=[((float(pkbest(p)) if pkbest(p) is not None else 0.0),_rw(p['year'])) for p in grp]
        ew=[(float(pkbest(p)),_rw(p['year'])) for p in grp if pkbest(p) is not None]
    else:
        aw=[((_level_336(p) if _established_336(p) else 0.0),_rw(p['year'])) for p in grp]
        ew=[(_level_336(p),_rw(p['year'])) for p in grp if _established_336(p)]
    _pool_uncond=float(np.average([x[0] for x in aw],weights=[x[1] for x in aw])) if aw else 75
    POOL_COND336[b]=float(np.average([x[0] for x in ew],weights=[x[1] for x in ew])) if ew else _pool_uncond
    # CHANNEL (a) RL_336_NOP: POOL's bust-inclusion IS the P factor at the band marginal (the whole-band
    # mean with never-establishers at 0.0 equals P_band x the establisher-only mean). Reverting the P-leg
    # therefore points POOL at the establisher-only marginal, which is exactly POOL_COND336.
    POOL[b]=POOL_COND336[b] if _NOP_336 else _pool_uncond
# position-anchored, monotone baseline peak: a later pick can't out-baseline an earlier one (kills small-sample inversions),
# and thin bands scale a reliable same-position band by the all-position band gradient instead of borrowing the all-position LEVEL.
BASEPK_REG={}
for g in sorted(set(GRP.values())):
    rel={b:BPK[(g,b)] for b in range(NB) if (g,b) in BPK}
    row=[]
    for b in range(NB):
        if b in rel: row.append(rel[b])
        elif rel:
            b0=min(rel,key=lambda x:abs(x-b)); row.append(rel[b0]*(POOL[b]/POOL[b0]))
        else: row.append(POOL[b])
    # #336 VARIANT — THE v3.4 CLAMP IS REMOVED. It read:
    #     for b in range(1,NB): row[b]=min(row[b],row[b-1])   # v3.4 basepk de-bias: clamp ALL bands
    #     (was 1..5) -> a later pick can never out-baseline an earlier one (kills the late-pick
    #     survivorship spike; fixes Xerri-type)
    # The "late-pick survivorship spike" it killed is the SYMPTOM of the sample defect repaired above, not
    # an independent bias — the engine's own history shows the inversion was SEEN and CLAMPED rather than
    # fixed. Keeping the clamp on a repaired sample would double-correct and would also hide whether the
    # repair actually works. The bust-inclusive baseline must be monotone non-increasing in pick ON ITS OWN.
    # That is now a MEASUREMENT, not an assertion; see the evidence dir for the result and any residual red.
    # RL_336_CLAMP restores it. The clamp exists ONLY to patch the late-pick spike that the survivor
    # sample produces, so channel (b) is emitted with this lever ON alongside RL_336_SURVLVL.
    if _CLAMP_336:
        for b in range(1,NB): row[b]=min(row[b],row[b-1])   # v3.4 basepk de-bias, restored
    for b in range(NB): BASEPK_REG[(g,b)]=row[b]
def basepk(g,b): return BASEPK_REG.get((g,b)) or POOL.get(b) or bandpeak(g,b)
# ============================================================================================================
# #336 AMENDMENT 2 (issue #336, OWNER CATCH 2 + "amend and rerun", 2026-08-06) — RESOLVED-STATE CONDITIONING
# AT THE PICK BASELINE.  The tables above are UNCHANGED and remain the UNCONDITIONAL, bust-inclusive
# expectation: they are what a PICK is worth, and a pick has no resolved state — the chance the entrant never
# establishes is exactly the risk it should carry. Everything that prices a pick (pick_raw, base_prod,
# pick_value) keeps reading them, unmoved.
#
# What amendment 2 adds is the OTHER leg, for REAL players whose establishment has already resolved. The
# owner's catch: "Have Trembath and Taylor, for example, not already established?" — they have, and under
# Addendum 1 they were still anchored to P(ever establishes) x E[level | establishes]. An established player
# is anchored to E[level | establishes] with NO probability discount.
#
#   BPK_COND / POOL_COND are already computed above: the conditional mean over ESTABLISHERS (the ruled
#   >=6-game definition, realized level, faded establishers INCLUDED — this is never a survivors-at-tenure
#   average). BASEPK_EST is assembled from them by the SAME thin-cell/gradient construction BASEPK_REG uses,
#   and the v3.4 clamp is removed there too, so the two tables differ ONLY by the P factor and are directly
#   comparable. MONOTONE BY CONSTRUCTION ACROSS THE SEAM: P <= 1 in every cell, so
#         basepk_est(g,b)  >=  basepk(g,b)      for every (g,b)
#   which is the amendment's monotonicity guard — an established player's anchor can never sit below the
#   unconditional expectation for his own cell. Asserted below, not assumed.
# ============================================================================================================
BASEPK_EST={}
for g in sorted(set(GRP.values())):
    rel={b:BPK_COND[(g,b)] for b in range(NB) if (g,b) in BPK_COND}
    row=[]
    for b in range(NB):
        if b in rel: row.append(rel[b])
        elif rel:
            b0=min(rel,key=lambda x:abs(x-b)); row.append(rel[b0]*(POOL_COND336[b]/POOL_COND336[b0]))
        else: row.append(POOL_COND336[b])
    # RL_336_CLAMP restores it HERE TOO, so the two tables keep the SAME construction and remain
    # differ-only-by-P — which is what makes the _A2_GUARD monotonicity check below meaningful in the
    # ablated arm rather than an artefact of two differently-built tables.
    if _CLAMP_336:
        for b in range(1,NB): row[b]=min(row[b],row[b-1])
    for b in range(NB): BASEPK_EST[(g,b)]=row[b]
_A2_GUARD=[(g,b) for g in sorted(set(GRP.values())) for b in range(NB)
           if BASEPK_EST[(g,b)] < BASEPK_REG[(g,b)]-1e-9]
def basepk_est(g,b): return BASEPK_EST.get((g,b)) or POOL_COND336.get(b) or bandpeak(g,b)
def _resolved_336(p,Y=None):
    """#336 AMENDMENT 2: has this player's establishment already RESOLVED? The ruled definition —
    at least one season of >= QUAL_336 (6) games (build_cohort_book.py:181-185), read on his own store
    record AS OF the valuation.

    Y defaults to BASE_REF, the module's own FORM-ANCHOR clock. That matters for one reason and it is a
    measurement-integrity reason, not a style one: the walk-forward emitter re-prices every entrant at
    every as-of year by setting MA.BASE_REF = MA.AGE_REF = Y, and the store carries seasons AFTER that
    year. A career-basis test would hand a year-1 valuation the knowledge that the player establishes in
    year 4 — future information, inflating exactly the early-tenure rows the hump measurement reads.
    Keying on BASE_REF makes the test as-of, and it uses the FORM anchor (not AGE_REF) so the forward
    lens cannot manufacture a resolution the calendar has not reached: k=0 identity by construction.
    On the LIVE board BASE_REF is 2026 and every store row is <= 2026, so the board is untouched by this
    choice — verified by md5, not asserted."""
    if Y is None: Y=BASE_REF
    for r in p['scoring']:
        if r['games']>=QUAL_336 and r['year']<=Y: return True
    return False
# ============================================================================================================
# #336 AMENDMENT 3 — the same two changes, at the BPK anchor. The full statement of both, with their sources
# and their measured shape, is the amendment-3 header block in engine/forward_valuation/par_build.py; it is
# not repeated here. The three constants below are RESTATED, not re-derived — the same "named at the consumer
# so the two cannot drift apart" convention QUAL_336 above already follows.
# ============================================================================================================
RES_K_336 = 5.8                                        # = par_build.RES_K = _merged_recover._ABS_FADE_K
def _rho_336x(g):
    g=float(max(0.0,g)); return (g*g)/(g*g+g+RES_K_336)
_RHO_BAR_336=_rho_336x(QUAL_336)
A3_DBAND =float(os.environ.get('RL_336_DBAND', '0.707707'))  # PINNED: the forward band's OWN charge for
A3_TARGET=float(os.environ.get('RL_336_TARGET','0.707455'))  # establishment failure on the unresolved subset,
                                                       # and the class risk it must total to. Both measured on
                                                       # n=329 unresolved players, value-weighted, against the
                                                       # conservative certainty-equivalent comparator. The full
                                                       # derivation, the three comparator readings and the
                                                       # reason the reconciliation is POOLED rather than
                                                       # per-cell are stated once, in par_build's amendment-3
                                                       # block. THE RESULT: D = 0.9996 — the band already
                                                       # charges the whole class risk, so the anchor charges
                                                       # nothing further, and amendment 2's anchor-side P on
                                                       # unresolved players was a SECOND charge.
A3_D=min(1.0,A3_TARGET/A3_DBAND) if A3_DBAND>0 else 1.0
_DFORCE_336=os.environ.get('RL_336_DFORCE')            # DECLARED measurement ablation lever; unset when reported
_RFORCE_336=os.environ.get('RL_336_RFORCE')            # DECLARED measurement ablation lever (pass-through derivation)
def _resolve_w_336(p,Y=None):
    """#336 AMENDMENT 3: r(p) in [0,1], the smooth resolution weight. Same curve, same K, same bar and the
    same AS-OF discipline _resolved_336 carries (Y defaults to BASE_REF so the walk-forward cannot read a
    resolution the calendar has not reached)."""
    if _RFORCE_336 is not None: return float(_RFORCE_336)
    if Y is None: Y=BASE_REF
    gs=[r['games'] for r in p['scoring'] if r['year']<=Y]
    return min(1.0,_rho_336x(max(gs) if gs else 0)/_RHO_BAR_336)
def _dbpk_336(g,b):
    """#336 AMENDMENT 3: D — the anchor-side discount left after the reconciliation. Pooled, one number.
    _pest_336 is NOT applied here any more; it is still applied in full to PICKS, via basepk()/BASEPK_REG,
    which pick_raw / base_prod / pick_value keep reading unmoved."""
    if _DFORCE_336 is not None: return float(_DFORCE_336)
    if _NOP_336: return 1.0    # CHANNEL (a) RL_336_NOP: the residual anchor-side probability discount comes off too
    return A3_D
def basepk_c_p(p,g,pk):
    """#336 AMENDMENT 2/3 — THE RESOLVED-STATE ANCHOR for every BPK-anchored REAL-PLAYER consumer.
        anchor = E[level | establishes] x [ D + r(p) x (1 - D) ]
    r=1 (established) reproduces amendment 2's established leg, basepk_est, EXACTLY. r=0 is the
    single-charged unresolved leg D x basepk_est — which under amendment 2 was P x basepk_est, i.e. the
    unconditional table basepk(). The band-interpolation in pick space is unchanged."""
    fb=bandcoord(pk); lo=int(fb); hi=min(NB-1,lo+1); f=fb-lo
    r=_resolve_w_336(p)
    def _one(b):
        D=_dbpk_336(g,b); return basepk_est(g,b)*(D+r*(1.0-D))
    return (1-f)*_one(lo)+f*_one(hi)
BAND_ANCHOR=PMD['BAND_ANCHOR']
def bandcoord(pk):
    if pk<=BAND_ANCHOR[0]: return 0.0
    if pk>=BAND_ANCHOR[-1]: return float(NB-1)
    for _i in range(NB-1):
        if BAND_ANCHOR[_i]<=pk<=BAND_ANCHOR[_i+1]:
            return _i+(pk-BAND_ANCHOR[_i])/(BAND_ANCHOR[_i+1]-BAND_ANCHOR[_i])
    return float(NB-1)
def basepk_c(g,pk):
    fb=bandcoord(pk); lo=int(fb); hi=min(NB-1,lo+1); f=fb-lo
    return (1-f)*basepk(g,lo)+f*basepk(g,hi)
def expected_c(g,pk,s):
    fb=bandcoord(pk); lo=int(fb); hi=min(NB-1,lo+1); f=fb-lo
    return (1-f)*expected(g,lo,s)+f*expected(g,hi,s)
# ==== L-CAPTAIN — THE RULED CAPTAIN CURVE (CONSTRAINTS_v1_15 PART 5, R98.1; owner-ruled 2026-07-14) ==========
# credit(L) = G * integral[BAR -> L] P(a) da, P logistic. The marginal IS the captaincy probability P(L), so the
# slope-1 impossibility ceiling is STRUCTURAL (logistic asymptote), not clamped. Closed form: the integral of the
# logistic is W*softplus, so credit(L) = G*W*[softplus((L-M)/W) - softplus((BAR-M)/W)], clamped >=0 (a credit is
# never negative; the clamp bites only below the bar, where credit is 0 exactly at L=BAR -> continuous, L-SMOOTH).
# Asymptote L-109.66 clear of the knee (NOT 107.4 = the retired CAPT_THRESH); per-point rate 0.10->0.50->0.997 at
# bar/mid/120. REPLACES the retired saturating curve (below), which was NEVER owner-ratified.
LCAPT_BAR=105.0; LCAPT_M=109.5; LCAPT_W=1.85; LCAPT_G=1.00   # PINNED in-code (item 114: no os.environ on a board-changing dial)
_CAPT=os.environ.get('RL_CAPT','1')!='0'   # kill-switch (G-ATTR separability): RL_CAPT=0 => retired saturating curve => base board byte-exact. Default ON = the ruled L-CAPTAIN curve.
CAPT_GAIN=0.35; CAPT_EXP=1.25; CAPT_CAP=18.0   # RETIRED saturating-curve constants; reachable ONLY via RL_CAPT=0 (the byte-exact base-reproduction proof)
def _softplus(x):
    return math.log1p(math.exp(x)) if x<30.0 else x   # overflow-safe: for large x, ln(1+e^x) -> x
def _capt_ruled(lev):
    c=LCAPT_G*LCAPT_W*(_softplus((lev-LCAPT_M)/LCAPT_W)-_softplus((LCAPT_BAR-LCAPT_M)/LCAPT_W))
    return c if c>0.0 else 0.0
def _capt_saturating(lev):   # RETIRED (the pre-R98.1 saturating premium, hard 18-pt cap); kept only for RL_CAPT=0
    over=max(0.0,lev-CAPT_THRESH)
    if over<=0: return 0.0
    cb=CAPT_GAIN*over**CAPT_EXP
    return cb*CAPT_CAP/(CAPT_CAP+cb)
_CAPT_OFF={'on':False}   # LEG B seg-3 captain-off pass: force capt_prem->0 to recompute the CAPTAIN-FREE production
                         # value pr0 (memo v1.1 §4). NOT RL_CAPT=0 (that is the RETIRED saturating curve, not zero).
                         # The map (_merged_recover raw_ev hook) sets this True around one price6 recompute, then
                         # takes delta = pr(capt on) - pr(capt off) and adds it back UNCHANGED. Default False =>
                         # capt_prem is the ruled L-CAPTAIN curve => board byte-exact.
def capt_prem(lev):
    if _CAPT_OFF['on']: return 0.0
    return _capt_ruled(lev) if _CAPT else _capt_saturating(lev)
GRACE={'KPF':2.5,'KPD':2.5,'RUCK':2.5,'MID':1.0,'SD':1.0,'SF':1.0}
LOS_C=0.16; LOS_P=1.82                 # progressive: gentle yr2 ~.85, steepening (yr3~.57 yr4~.31 yr5~.16)
def los(p): return AGE_REF-p['year']
def los_decay(p):
    g=gfut(p); s=los(p); over=max(0.0,s-GRACE.get(g,1.0)) # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
    return math.exp(-LOS_C*over**LOS_P)   # yr1 -> pick value (debut signal deferred to next version)
# ---- model core ----
STBL=False                                   # SCALE-anchor mode: project on a stable (v18-equivalent) basis
RW_S={2026:2.0,2025:1.0,2024:0.4,2023:0.2}
def level_stable(p):
    n=d=0
    for r in p['scoring']:
        w=RW_S.get(r['year'],0)
        if w and r['games']>=2: n+=r['avg']*r['games']*w; d+=r['games']*w
    return n/d if d else None
SPIKE_CAP={'KPD':0.60}             # position cap on improving-form confidence (default 0.83). KPD spikes empirically revert (study: ~0.55 retention vs ~0.84 elsewhere); back-test-validated. Knob: other positions overridable for research.
ROLE_HC_MAX=0.07                       # role-decay: max level haircut to a past-peak veteran whose current role+output have collapsed (filtered <3g season). Tuned so an O'Brien-class case lands ~1/3 down on value.
_SG={}
def _season_games():                   # games of the season leader in BASE_REF (season-progress proxy); robust as the year fills in
    if BASE_REF not in _SG:
        _SG[BASE_REF]=max([r['games'] for _p in data for r in _p['scoring'] if r['year']==BASE_REF] or [22])
    return _SG[BASE_REF]
def _role_decay_hc(p,baseline):        # O'Brien rule: a past-peak player who's been dropped on ability (role collapsed, output cratered), not injury
    if baseline is None: return 0.0
    if _season_games() < 7: return 0.0                            # dormant until the season-leader has 7 games (rounds 1-6 too noisy)
    g=gfut(p); a_=_age_at(p,BASE_REF) # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
    if a_ < PEAK_AGE[g]+1: return 0.0                              # not past peak -> spares young cameos (McCabe/Hardeman etc.)
    cur=next((r for r in p['scoring'] if r['year']==BASE_REF),None)
    if not cur or not (1<=cur['games']<3): return 0.0             # only the filtered sub-3-game current season; >=3g already shows in level_demo
    if cur['games']/max(_season_games(),1) >= 0.35: return 0.0    # role didn't actually collapse
    drop=clamp((baseline-cur['avg'])/baseline,0.0,1.0)
    if drop < 0.30: return 0.0                                     # output not far below baseline -> spares elite cameos (Gulden 2g@112.5)
    return clamp(ROLE_HC_MAX*drop,0.0,ROLE_HC_MAX)
def level_demo(p):                     # demonstrated form at BASE_REF (the true now); scoring truncated to <=BASE_REF
    if STBL: return level_stable(p)
    sc=[(r['year'],r['avg'],r['games']) for r in p['scoring'] if r['year']<=BASE_REF]
    qs=sorted([(y,a,gm) for (y,a,gm) in sc if gm>=3])
    if not qs: return None
    ly,la,lg=qs[-1]
    # thin-prior MERGE: a sub-3-game CURRENT-year cameo folds into the most-recent qualifying season (kept as that
    # season's games) so those games COUNT (up or down) instead of being dropped by the >=3 filter. Transient by
    # design: once the live season reaches 3 games it becomes its own qualifying season and these games pull back out.
    cur=[(y,a,gm) for (y,a,gm) in sc if y==BASE_REF and 0<gm<3]
    if cur and ly<BASE_REF:
        _ca,_cg=cur[0][1],cur[0][2]; la=(la*lg+_ca*_cg)/(lg+_cg); lg=lg+_cg
    if len(qs)==1: return la
    pn=pd=0
    for (y,a,gm) in qs[:-1]:
        w=(0.60**(ly-y))*min(gm,18)*(0.25 if gm<8 else 1.0); pn+=a*w; pd+=w   # prior: recency-weighted, tiny samples drowned
    prior=pn/pd if pd else la; growth=la-prior; base=lg/16.0
    a_=_age_at(p,BASE_REF); pa_=PEAK_AGE[gfut(p)]; old=a_>pa_+3 # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
    proven=sum(1 for (y,a,gm) in qs if gm>=10)>=4
    if proven and not old:                                   # robust baseline: a one-year spike is as much an outlier as a one-year dip
        rc=sorted(a for (y,a,gm) in qs[-4:]); n=len(rc); med=rc[n//2] if n%2 else (rc[n//2-1]+rc[n//2])/2.0
        baseline=0.5*prior+0.5*med
    else: baseline=prior
    # B1 late-breakout fix: a large, sustained step-up over a weak early base drags the median/prior
    # baseline below the demonstrated level. Raise baseline to the sustained run-mean (K=3, ratio>=1.4),
    # only-raise guard (never drags a steady star down). Lifts the Richards/Xerri/Pickett/Ash/Blakey cohort.
    _b1=[(y,a,gm) for (y,a,gm) in qs if gm>=10]
    if len(_b1)>=3:
        _run=_b1[-3:]; _pre=[a for (y,a,gm) in _b1 if y<_run[0][0]]
        _op=(sum(_pre)/len(_pre)) if _pre else prior; _rm=sum(a for (y,a,gm) in _run)/3.0
        if _op>0 and min(a for (y,a,gm) in _run)>_op and _rm/_op>=1.4: baseline=max(baseline,_rm)
    # thin-prior RECENCY-FLOOR: the most-recent season's games can never weigh LESS, per game, than older games.
    # Floor conf at the recent season's share of the recency-weighted game mass (recency decay -> a recent game
    # weighs MORE than an older one). Fixes the inversion where an equal-games older season out-weighted the recent one.
    _pmass=sum((0.60**(ly-y))*min(gm,18) for (y,a,gm) in qs[:-1])
    _cfloor=min(lg,18)/(min(lg,18)+_pmass) if (min(lg,18)+_pmass)>0 else 0.0
    if growth>=0:                                            # improving: trust the rise but temper (don't fully chase a partial-season jump)
        conf=base*(1.0+growth/40.0); cap=SPIKE_CAP.get(gfut(p),0.83) # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
        _gg=gfut(p)                                          # DPP STRIP: settled-future eligibility lifts the spike cap (was the dual-leg lift; Serong KPD now-MID -> 0.83)
        if _gg: cap=max(cap,SPIKE_CAP.get(_gg,0.83))
        conf=max(conf,_cfloor)                               # recency-floor (binds only when the recent season is under-trusted vs the prior)
    elif old:                                                # older decline: likely real -> trust recent
        agef=clamp((a_-pa_)/6.0,0.0,1.0); conf=base*(0.60+0.60*agef); cap=0.92
    else: conf=base*0.30; cap=0.92                           # proven prime sudden drop -> likely a blip, regress to baseline
    conf=clamp(conf,0.20,cap)
    lvl=conf*la+(1-conf)*baseline
    return lvl*(1.0-_role_decay_hc(p,lvl))
def _agecurve(g,a):                    # interpolated fraction-of-peak from the per-position empirical curve
    c=AGE_CURVE.get(g)
    if not c: return 1.0
    lo,hi=min(c),max(c); a=max(lo,min(hi,a)); a0=int(math.floor(a)); f=a-a0
    return c[a0]*(1-f)+c.get(min(hi,a0+1),c[a0])*f
def _dev_advance(L,p):                  # roll demonstrated form from BASE_REF age to AGE_REF age along the dev curve
    if L is None: return None
    a0=_age_at(p,BASE_REF); a1=age(p)
    if a1==a0: return L                                         # identity at offset 0 -> vP0==v, present board untouched
    g=bnow(p); c0=_agecurve(g,a0); c1=_agecurve(g,a1)
    if c0<1e-6: return L
    cp=basepk_c_p(p,g,effpk(p))                                 # pedigree-implied peak (independent of L -> no recursion). #336 AMENDMENT 2 — enumerated BPK consumer 1: the class peak a real player's demonstrated level catches up toward at weight (1-w). Established -> establisher baseline; unresolved -> unconditional.
    w=clamp(p['games']/130.0,0.30,0.85)                        # own-form trust by sample size; back-test will tune
    L1=L + w*(L*(c1/c0-1.0)) + (1-w)*(cp*(c1-c0))              # blend the CHANGE (own arc vs pedigree catch-up); zero at offset 0
    return clamp(L1, L*0.5, L*1.6)                              # growth/decline guard
def level_now(p): return _LEVEL_OVR if _LEVEL_OVR is not None else _dev_advance(level_demo(p),p)
def latest_avg(p):
    sl=sorted([r for r in p['scoring'] if r['games']>=4],key=lambda r:r['year']); return sl[-1]['avg'] if sl else None
def best2(p):
    d=debut(p); s=sorted([r['avg'] for r in p['scoring'] if r['games']>=7 and r['year']>=d],reverse=True)[:2]; return float(np.mean(s)) if s else 0
REPL={'MID':80.1,'SD':78.3,'RUCK':78.5,'KPD':68.4,'SF':70.9,'KPF':66.8}  # v3.3 derived (rl_replacement_derive.py): Rule-1 pool, kfru 0.5, SD/MID 50/50 @4.16/5.20, KPD@2.0, SF@4.0, KPF@2.0, RUCK@1.64  [BAKE 2026-07-04: KPF REPL-1, 67.8->66.8, owner dial]
DELTAS={-8:.58,-7:.62,-6:.68,-5:.74,-4:.80,-3:.86,-2:.92,-1:.97,0:1.0,1:.99,2:.98,3:.96,4:.94,5:.91,6:.88,7:.84,8:.79,9:.73,10:.66,11:.58,12:.50,13:.42,14:.34}
# ==== ORDER B — THE VETERAN FIXES (RL_O33, DEFAULT OFF; #334 c.5312733761 commission, c.5314553763 the
# owner's B rulings, derivation packet docs/evidence/order_b_derivation_2026-08-17/). NOTHING IS GREENLIT:
# RL_O33 unset => every expression below is inert => the board is BYTE-EXACT to the pre-order tree, and
# this build LANDS ONLY AFTER the repaired Candidate 32 lands (two packets, two reviews — the ruling's
# sequencing). Stage sub-dial RL_O33_STAGE (declared, default 3 = the full candidate):
#   1 = B-1 the ANCHORED TALL LADDER: KPD/KPF post-peak decline rho_j = 0.030 + 0.025*(j-1) (the
#       derivation's fitted family, ADOPTED by ruling B-1 — f(1..5) = .970/.917/.843/.755/.657 at ages
#       28-32), consumed by frac() below only when the caller passes g in {KPD,KPF} and only past peak;
#       pre-peak DELTAS and PEAK_AGE (27/27) untouched; RUCK keeps the current curve (derivation: KEEP).
#       Plus the ANCHOR-PRESERVING renorm s* on the tall projection stream (the naive wiring cut
#       prime/young talls 17-30% and was REJECTED by the prime-anchor evidence) — derived at build time
#       as the fixed point conserving the aggregate board value of KPD/KPF rows aged 23-26, then PINNED
#       below. RL_O33_SSTAR is the derivation-shell override ONLY (the s* fixed-point iteration runs
#       with it at 1.0); it is never set on a shipping board.
#   2 = B-2 the TERMINAL FADE — THE FALLBACK POSITION, and the packet says so plainly: the owner
#       withdrew the universal terminal knob ("are all 31-year-olds equal?") and ordered an
#       OUTPUT-CONDITIONAL fade, fallback flat-hazard ONLY if the conditional fit fails identification.
#       IT FAILED, twice, both shown in RESULTS_B_FADE_FIT{,2}.json: the prereg'd tier-level loss cannot
#       identify any fade (A CI [0.00,0.60] spans 0), and the rate-instrument rescue identifies a fade
#       (A CI [0.14,0.60]) but NOT output-conditionality — s0 runs to the grid ceiling (G(star) CI
#       [0.12,0.77], not below the 0.5 identification bar) because the mid/role rate gaps exhaust the
#       whole discount family (the un-closable remainder is the k=0 exit-hazard channel the derivation
#       named for a future order). So the wired object is the ruled fallback: the HAZARD-ARITHMETIC
#       knots (29: 0.211 · 30: 0.232 · 31: 0.246 — r(a) = 0.14 + the measured excess exit hazard),
#       piecewise-linear in CONTINUOUS age via _pw_interp (no integer cliffs), 0.14 at <=28 (zero rows
#       below 28 move), flat beyond 31, BALANCED LENS ONLY. The fitted-34% boundary value is DEAD
#       (owner ruling). The 34%-family knots do not appear here at all.
#   3 = B-3 TAPER RETIREMENT: the v7 ascending age-taper on the q97 ceiling band is not applied
#       (asc == 1 => band[5] = max(q97m, q90) exactly as _b6_core emits it) — the derivation's quantile
#       re-fit found asc*=1 the boundary solution in EVERY band the taper bites; kills all 341 v-inversions
#       by construction. Wired at the b6 wrapper in _merged_recover.py; the frozen q97m is NOT touched
#       (its censoring-aware refit is bake-time per R-W6).
# Prereg: docs/evidence/order_b_build_2026-08-17/PREREG_B_BUILD.md (pushed before these lines existed).
_O33=os.environ.get('RL_O33','0')!='0'                       # ORDER B: the veteran fixes (default OFF)
_O33S=(int(os.environ.get('RL_O33_STAGE','3')) if _O33 else 0)
def _o33_ladder(rho0=0.030,g=0.025,n=14):                    # B-1 family, the derivation's own construction (b2_fit.ladder_of)
    f,out=1.0,{}
    for j in range(1,n+1):
        f*=(1.0-min(0.60,max(0.0,rho0+g*(j-1)))); out[j]=f
    return out
O33_TALL_LADDER=_o33_ladder()                                # f(1..5)=.970/.9167/.8433/.7548/.6566 (ages 28-32); tail = the family continued (W5 measures nothing past 31 — extrapolation-by-rule, bounded by the frac<0.42 projection stop)
O33_SSTAR_PIN=1.2988                                          # s* PINNED (derived 2026-08-17 on THIS tree at base cf443a6, RL_O32=1 stage-1 ladder-only fixed point ON THE FROZEN PRE-ANCHOR BASIS: conserves the aggregate board value of the 55 KPD/KPF rows aged 23-26 to -0.06%, inside the prereg'd 0.2% tolerance; iteration log docs/evidence/order_b_build_2026-08-17/SSTAR_DERIVE_out.txt. Board-value s* (1.299) vs the derivation's production-stream preview s* (1.365): the pedigree leg and the max(proj, floor) resolution dampen the projection cut — same anchor object, the engine's own arithmetic.)
_o33sstar=os.environ.get('RL_O33_SSTAR')                     # derivation-shell override (the s* fixed point itself); never set on a shipping board
O33_SSTAR=(float(_o33sstar) if _o33sstar not in (None,'') else O33_SSTAR_PIN)
O33_FADE_KNOTS=[(28.0,0.14),(29.0,0.211),(30.0,0.232),(31.0,0.246)]   # B-2 FALLBACK: hazard-arithmetic knots (RESULTS_B_FIT.json hazard_reference; 28 pinned at the 0.14 base so nothing below 28 moves)
def o33_fade(a):
    """B-2 extra per-annum discount above the flat 0.14, continuous in age, 0 at a<=28. Balanced lens only
    (enforced at the call sites). Returns 0 whenever the dial/stage is off — identity by construction."""
    if not _O33 or _O33S<2 or a is None: return 0.0
    return _pw_interp(float(a),O33_FADE_KNOTS)-0.14
def frac(a,pa,g=None):
    j=max(-8,min(14,int(round(a-pa))))
    if _O33 and _O33S>=1 and j>0 and g in ('KPD','KPF'): return O33_TALL_LADDER[j]   # B-1: tall post-peak ladder (two-arg callers and dial-off take the shared DELTAS verbatim)
    return DELTAS[j]
KAPPA=0.10;SCONV=30.0;LOWBASE=54.0;GAMMA=float(__import__('os').environ.get('RL_GAMMA','1.0'))  # 0.85=SCAR(concave); 1.0=VOR(linear) via RL_GAMMA env (for the SCAR-vs-VOR dual-column build)
S_SH=3.0
def comp(v): return v   # no compression (v2.0)
def posval(x): return S_SH*math.log(1+math.exp(min(x/S_SH,40.0)))   # position value above replacement
# ==== LEG B — UN-COMPRESS THE OUTPUT->PRICE MAP (RL_UNCOMP; memo v1.1 / seg-3 2026-07-16, spec §3 Leg B) ==
# OBITUARY (seg-2 posval-COMPONENT wiring — delete-don't-disable, SSI/CORE rule 7). The ORIGINAL design
# (register items 211/213) wrapped the map at SIX posval sites via `posval_uncomp(lev,pos,Eq)`: the k-legs
# of proj_from_peak/prod_floor here AND the W4 _proj_w4/_prod_floor_w4 in _merged_recover. That placement
# was PROVEN to compress BY CONSTRUCTION (register 221): the REPL offset makes local elasticity >=1 at
# posval for elites, so blending toward an elasticity-1 target pulls elite production DOWN, not up. The
# axis finding (register 224) then located the deeper defect — the rho AXIS: level_now's output-elasticity
# is only 0.124 (measured), so any blend toward V_ref*rho(level_now) flattens price-vs-output regardless of
# hook. MEMO v1.1 CURES BOTH: the map moves to the PRODUCTION-VALUE hook (pr=price6, ONCE per player, at
# _merged_recover.py raw_ev:298), and rho tracks REALISED OUTPUT. `posval_uncomp` + the per-leg E/CAL state
# + the L_ref/V_ref dicts are DELETED here; the six posval sites are RESTORED to their pre-seg-2 originals
# (posval(lev+capt_prem(lev)-REPL)). The v1.1 map, its references (RHO_DEN/V_ref_b) and the C[pos]
# conservation now live in _merged_recover (co-located with the hook). This module keeps ONLY the declared
# kill-switch + dials below (the RL_ISOFADE / RL_EVW pattern — NOT a manifest dial). RL_UNCOMP=0 (or the
# strength dial unset) => the map is INERT => board 8d90c9ac BYTE-EXACT (config_sha256 UNMOVED).
_UNCOMP=os.environ.get('RL_UNCOMP','1')!='0'
UNCOMP_DELTA=6.0                       # onset-ramp width (avg-points above replacement); memo §2.2 (~2*S_SH clears the softplus knee)
UNCOMP_DECAY=0.25                      # ρ games×recency decay d per year back; memo §2.1 ⟪v1.3⟫ OWNER-SET (R105.6, register 248 — the owner's ACCEPT: "a recent game counts MORE"; his R105.4 said 'more', v1.3 records HOW much = a QUARTER). u_s=games_s·d^(Ynow−year_s); d=0.25 measured λ_ρ≈0.9225 (strong end of the never-wipe family; the seat's d=0.5 was seat-filled, retired). DECLARED constant (owner-worded, one number), sits NEXT TO Δ=6.0. NO floor/exclusion/phase-test on the ρ axis (acceptance-enforced; L-RECENCY + forbidden-list self-tests guard it).
UNCOMP_TAU=1.1                         # =_EVW_TAU: the saturating evidence-weight rate E=1-exp(-Eq/tau) (memo §2 "same family Leg A's fade rides")
UNCOMP_S_DEFAULT=0.10                  # THE strength dial s -- OWNER-SET (register item 265, verbatim: "Let's lock in s=0.10 and move forward."). The memo v1.3 machine-selection construction (the beta>=0.80 bar + the {0.55-0.70} grid) is RETIRED -- s is now an owner-worded number, like the fade d=0.25; ZERO seat-authored numbers. Was None (map INERT until selection); now the selected literal wires the default path live.
_uncs=os.environ.get('RL_UNCOMP_S')    # dev-shell grid sweep override: RL_UNCOMP_S=<s> per grid point
UNCOMP_S=(float(_uncs) if _uncs not in (None,'') else UNCOMP_S_DEFAULT)
_UNCONSERVE=os.environ.get('RL_UNCONSERVE','0')=='1'   # DEV-SHELL measurement override (RL_ISOFADE/RL_UNCOMP_S pattern; item 256/257 "Measure"): =1 => the memo §3 per-position conservation renorm C[pos] is IDENTITY (C≡1) on the un-compress map (the applied factor at _merged_recover.py:332 becomes 1.0; load-time C is still computed but not applied). Default OFF => shipped behaviour BYTE-EXACT (pure no-op when unset). Ships nothing; measures the DECIDED family UNFUNDED. NOT a manifest dial (config_sha256 UNMOVED); UNCOMP_S_DEFAULT stays None, UNCOMP_DECAY stays 0.25.
CAPT_THRESH=107.4; CAPT_M=116.0; CAPT_W=5.0   # captaincy line (slider); 2026-06-21 M6: last-5 rank-25 ~=107.4 (unbiased upload), was 108.0
def _pcap(a): return 1.0/(1.0+math.exp(-(a-CAPT_M)/CAPT_W))
def capt_bonus(level):
    if level<=CAPT_THRESH: return 0.0
    n=max(2,int(round(level-CAPT_THRESH))*2); h=(level-CAPT_THRESH)/n; ss=0.0
    for i in range(n+1): ss+=(0.5 if i in (0,n) else 1.0)*_pcap(CAPT_THRESH+i*h)
    return CAPT_GAIN*ss*h
def pedmix(pk): return 0.50+0.32*math.exp(-(pk-1)/9.0)
def clamp(x,a,b): return max(a,min(b,x))
# ===== #334 THE AGE-DYNAMIC FUTURE DISCOUNT (owner ruling 5246868843) — MEASURED VARIANT, DIAL-GATED.
# THE OWNER'S ORDER: the flat per-annum future discount becomes a function of the player's CURRENT age at
# pricing — early career discounted LESS, late career MORE — pulled forward from the root-act aiming set as
# the counterbalance to the relativity-guard breach the composed act measured (young players cut 4x harder
# than peak players). This is his ruled rebalance, not a seat's self-tuning; the SIZING word remains his.
#   rate(a) = 0.13            for a <= 21
#           = 0.15            for a >= 26
#           = linear in CONTINUOUS age between (no integer cliffs — the ITEM B discipline)
# SCOPE: the BALANCED lens only. 'now' (0.34) and 'fut' (0.05) are display postures, not the valuation
# integral the ruling names, and moving them would silently re-posture the UI toggles as well.
# RL_AGE_DISC=0 (DEFAULT) => rate(a) is never consulted => byte-identical to the pre-variant board.
AGE_DISC=os.environ.get('RL_AGE_DISC','0')!='0'
AGE_DISC_LO=float(os.environ.get('RL_AGE_DISC_LO','0.13'))   # the young end (age <= 21)
AGE_DISC_HI=float(os.environ.get('RL_AGE_DISC_HI','0.15'))   # the mature end (age >= 26)
AGE_DISC_MODE=os.environ.get('RL_AGE_DISC_MODE','1')   # 1 = V1 two-point current-age · 2 = V2 four-band current-age · 3 = V3 current-age · 4 = V4 current-age · 5 = V5 current-age (owner's fifth ladder) · 9 = seat-proposed age-at-season path product
def _pw_interp(a,knots):
    """Piecewise-linear on CONTINUOUS age through (age, rate) knots; flat outside. No integer cliffs."""
    a=float(a)
    if a<=knots[0][0]: return knots[0][1]
    if a>=knots[-1][0]: return knots[-1][1]
    for (a0,r0),(a1,r1) in zip(knots,knots[1:]):
        if a0<=a<=a1:
            return r0 if a1==a0 else r0+(r1-r0)*(a-a0)/(a1-a0)
    return knots[-1][1]

# V1 (mode 1): two-point current-age curve, the owner's first proposal.
# V2 (mode 2): four-band current-age curve — 12% at <=19 · 13% at 20-21 · 15% at 25-27 · 16% at >=28,
#   smooth joins across 21->25 and 27->28. Same machinery as V1, just more knots.
_V2_KNOTS=[(19.0,0.12),(20.0,0.13),(21.0,0.13),(25.0,0.15),(27.0,0.15),(28.0,0.16)]
# V3 (mode 3): the owner's CORRECTED third proposal — CURRENT-AGE keyed like V1 and V2. His first
#   filing inverted the numbers and this supersedes it. 10% at <=20 · 11% at 21-22 · 12% at 23-25 ·
#   13% at 26-28 · 14% at >=29, smooth joins, continuous age. The most aggressive youth-lifter of the
#   three: a big young-side lift (10% against the current flat 14%) with veterans nearly unchanged
#   (14% is the status quo). Expect the largest relativity recovery and the largest board-total rise,
#   and watch the no-arb frame hardest here — a 10% discount on young futures narrows the gap between
#   expected appreciation and the discount charged.
_V3_KNOTS=[(20.0,0.10),(21.0,0.11),(22.0,0.11),(23.0,0.12),(25.0,0.12),(26.0,0.13),(28.0,0.13),(29.0,0.14)]
# MODE 9 — SEAT-PROPOSED, NOT THE OWNER'S. AGE-AT-SEASON keyed: a different machine, where the rate
#   for future season k is the rate for the age the player will BE then, so PV is the PATH PRODUCT
#   prod_{j=1..k} 1/(1+r(a+j)) rather than (1+r)**k. Built before the correction arrived; kept as a
#   low-priority menu extra, to be run LAST after the owner's three variants and the two menu items.
_V9_KNOTS=[(20.0,0.14),(21.0,0.13),(22.0,0.13),(23.0,0.12),(25.0,0.12),(26.0,0.11),(28.0,0.11),(29.0,0.10)]
# V4 (mode 4): the owner's fourth curve, CURRENT-AGE keyed like V1-V3. 11% at <=19 · 12% at 20 ·
#   13% at 21 · 14% at 22 · a smooth glide 14->15 across 23-25 · 15% at 26-27 · 16% at >=28.
#   Its distinguishing property is that the AGE-22 RATE EQUALS THE FLAT BASELINE (14%), so a player
#   drafted at 18 is discounted identically to the pre-variant engine in his year-4 season. That is
#   the design intent behind expecting year 4 to sit still while years 1-3 lift and years 5+ trim.
_V4_KNOTS=[(19.0,0.11),(20.0,0.12),(21.0,0.13),(22.0,0.14),(23.0,0.14),(25.0,0.15),(27.0,0.15),(28.0,0.16)]
# V5 (mode 5): the owner's FIFTH ladder, filed verbatim in his own words (#334 comment 5248006413):
#   "18 - 12 / 19 - 12.5 / 20 - 13 / 21 - 13.5 / 22/23 - 14 / 24 - 14.5 / 25/26 - 15 / 27 - 15.5 / 28+ - 16."
# Same machinery as V1-V4: CURRENT-AGE keyed, piecewise-linear on CONTINUOUS age through _pw_interp,
# flat outside the end knots, no integer cliffs.
#
# THE 22/23 SHELF IS OWNER-SPECIFIED, AND THAT IS WHAT DISTINGUISHES V5 FROM V2. This is recorded
# because the owner's question that produced V5 rested on a premise about V2 that does not hold:
#   V2's knots are [(19,.12),(20,.13),(21,.13),(25,.15),(27,.15),(28,.16)] — a SMOOTH JOIN from 21 to
#   25, so V2's rate at 22 is 13.5% (interpolated), NOT 14%. V2 has no shelf at 22-23 at all; the
#   14% level is merely passed through on the way up at age 23.
#   V4 pins 22 and 23 at exactly 14% — the shelf exists there, but by a two-knot pin followed by a
#   glide 23->25.
#   V5 states the shelf EXPLICITLY as its own pair of knots (22,.14),(23,.14) and then steps 24 at
#   14.5% — a knot V4 does not have (V4 glides 14->15 across 23-25, giving 14.5% at 24 by
#   interpolation and 15% only at 25). V5 and V4 therefore agree at 22, 23, 24 and 25 by
#   construction and differ ONLY on the young side (<=21) and at 26-27:
#       age      18     19     20     21     22     23     24     25     26     27    28+
#       V4      .110   .110   .120   .130   .140   .140   .145   .150   .150   .150   .160
#       V5      .120   .125   .130   .135   .140   .140   .145   .150   .150   .155   .160
#   So V5 is DEARER than V4 everywhere at or below 21 (it discounts the young future harder, i.e.
#   lifts young value less) and dearer at 27; identical 22-26 and at 28+.
_V5_KNOTS=[(18.0,0.12),(19.0,0.125),(20.0,0.13),(21.0,0.135),(22.0,0.14),(23.0,0.14),
           (24.0,0.145),(25.0,0.15),(26.0,0.15),(27.0,0.155),(28.0,0.16)]
def age_disc_mode():
    try: return int(float(AGE_DISC_MODE))
    except Exception: return 0
def age_disc(a,d,lens='bal'):
    """The per-annum future discount for a player priced at CURRENT age a. Identity when off.
    Modes 1/2/3 return a scalar rate; mode 9 is NOT a scalar and is handled by disc_factor()."""
    if not AGE_DISC or lens not in ('bal','balanced') or a is None: return d
    m=age_disc_mode()
    if m==2: return _pw_interp(a,_V2_KNOTS)
    if m==3: return _pw_interp(a,_V3_KNOTS)
    if m==4: return _pw_interp(a,_V4_KNOTS)
    if m==5: return _pw_interp(a,_V5_KNOTS)   # V5: the owner's fifth ladder, 22/23 shelf explicit
    if m==9: return d                      # mode 9 never uses a single rate; see disc_factor()
    a=float(a)
    if a<=21.0: return AGE_DISC_LO
    if a>=26.0: return AGE_DISC_HI
    return AGE_DISC_LO+(AGE_DISC_HI-AGE_DISC_LO)*(a-21.0)/5.0
def disc_factor(a,d,k,lens='bal',grace=0):
    """THE DISCOUNT FACTOR for future season k, for a player priced at current age a.
    Modes 0/1/2/3: the existing power form (1+r)**k with r fixed at pricing time.
    Mode 9 (seat-proposed): the PATH PRODUCT prod_{j=1..k} (1+r(a+j)) — the rate for each season is the rate for the
    age he will be in it. k=0 is 1.0 in every mode, so the present season is never discounted.

    ORDER 28 GRACE-A (dial-gated, default OFF — see grace_years above). `grace` is the number of
    FUTURE seasons that carry full weight before the ladder engages: the exponent handed to the power
    form becomes max(0, k - grace).  grace=0 gives max(0,k)==k for k>0, i.e. the pre-order form
    BIT-FOR-BIT — the dial-off path is identity by construction, not by tolerance.
    Mode 9 coherence (inactive on the live config, flat 14%): grace drops the EARLIEST factors from
    the path product, j running grace+1..k, so the same seasons go free under either mode."""
    if k<=0: return 1.0
    if grace:
        k=max(0,int(k)-int(grace))
        if k<=0: return 1.0
    if AGE_DISC and lens in ('bal','balanced') and a is not None and age_disc_mode()==9:
        f=1.0; a=float(a)
        for j in range(int(grace)+1,int(grace)+int(k)+1): f*=(1.0+_pw_interp(a+j,_V9_KNOTS))
        return f
    return (1.0+age_disc(a,d,lens))**k
LENS={'now':0.34,'bal':(0.14 if os.environ.get('RL_DIAL14','1')!='0' else 0.15),'fut':0.05}   # v2.9 L2: dial 14 (owner-ruled D5, "14 for now"); gate RL_DIAL14 (default ON; =0 ⇒ 0.15 ⇒ base). bont 3676 gawn 2501.
# LEG E POSTURES (memo §3): NEW VALUES over the SAME dial family — a posture is the per-annum production discount
# d, not a new code path. balanced == 'bal' (owner-ruled, byte-exact, the ONLY board that gates/bakes/seals).
# Strawmen SEALED in session_2026-07-18/lege/posture_presets_v1.json (md5 c2e17c49); owner ratifies at the movers
# report (nothing ruled here). Higher d => future discounted MORE => now-weight up. Gate RL_LEGE (default ON; a
# DECLARED kill-switch like RL_PVC2/RL_EVW — NOT a manifest dial). RL_LEGE=0 => posture keys absent + the forward
# form-anchor inert => board 06d8af60 BYTE-EXACT (the kill-switch proof).
_LEGE=os.environ.get('RL_LEGE','1')!='0'
if _LEGE:
    LENS.update({'balanced':LENS['bal'],   # == 'bal' (byte-exact production path)
                 'contender':0.18,          # sketch 0.14->0.18-0.20 (win-now: near-term weight up). STRAWMAN.
                 'rebuilder':0.10})         # sketch 0.14->~0.10 (future weight up). STRAWMAN.
POSTURES=('balanced','contender','rebuilder')
# ── OBITUARY — lens_tilt (the INTERIM no-improvement-floor lens), DELETED at Leg E (delete-don't-disable) ──
# Was: `def lens_tilt(p,lens): a bounded +/-30% (LTILT=0.30) multiplicative tilt around balanced by age-vs-peak
# phase`, applied as the final multiplier in value() for the 'now'/'fut' display lenses while production stayed
# hard-anchored at 'bal'. It credited NO projected production — the ruled LENS-PROJECTION defect (acceptance
# laws[LENS-PROJECTION]: "interim lens = no-improvement floor, cross-age trades NOT read off it"). RETIRED here:
# the real projection law (R103.3, the forward form-anchor offset in _merged_recover.b6/price6) supersedes it,
# and postures replace the display tilt with a genuine dial re-weighting. `value(p,lens)` now weights, never
# tilts (weight-don't-gate, R105.4). It returned 1.0 for lens=='bal', so its removal is byte-exact on the
# balanced board. The UI +1/+2 toggle re-enables on this landing (SPEC §3).
RWE={1:1.0,2:1.3,3:1.6,4:1.7,5:1.7}
def track_delta(g,pk,sr):
    num=den=tg=0
    for s,(a,gm,yr) in sr.items():
        if STBL and s>8: continue
        rec=1.0 if STBL else 0.78**(2026-yr)     # calendar recency: recent seasons govern the estimate
        w=RWE.get(s,1.7)*min(gm,22)*rec; num+=(a-expected_c(g,pk,s))*w; den+=w; tg+=gm
    return (num/den,tg) if den else (None,0)
def cohort_peak(g,pk,sr,p=None):
    # #336 AMENDMENT 2 — enumerated BPK consumer 2: the cohort peak IS a regression toward the class
    # baseline (baseline + bb*own-delta). `p` is threaded from peak_est so the baseline can condition on
    # the player's resolved state; p=None keeps the unconditional table, which is what a pick-level or
    # synthetic caller must get.
    delta,tg=track_delta(g,pk,sr)
    if delta is None: return None,0
    conf=clamp(tg/45.0,0,1); bb=0.60+(BETA_POS.get(g,0.95)-0.60)*conf
    _base=basepk_c(g,pk) if p is None else basepk_c_p(p,g,pk)
    return _base+bb*delta+ICPT_POS.get(g,2.79)*conf, tg
def survival(b,delta,games):
    # Bust is already priced once in the pedigree curve (PVC carries 1-BUST_BAND); the band-average
    # washout must NOT be re-charged here. So the survival haircut applies ONLY to a player who is
    # tracking *below* his own bar (mult>1) -- an at-par or above-par player gets no extra bust tax.
    bp=BUST_BAND.get(b,0.15); mult=clamp(1.0-delta/20.0,0.4,1.6); fade=max(0.0,1-games/40.0)
    return 1-bp*max(0.0,mult-1.0)*fade
def proj_from_peak(g,lp,a,cur,lens,g0=None,fut=None,pre_hc=0.0,grace=0):
    # ORDER 28: `grace` is threaded from the CALLER (which holds the player record) because this
    # function takes a scalar age, not a record — see PREREG_ORDER28.md §1.2. Synthetic/pick-level
    # callers omit it: a band node is not a person and has no entry age. grace=0 => byte-exact.
    # g = SETTLED (future) position: drives PEAK_AGE, level trajectory, key-premium, runway.
    # g0 = year-0 (present) position for REPL; fut = years-1+ REPL blend [(pos,wt)]. Defaults reproduce single-position behaviour.
    pa=PEAK_AGE[g]; d=age_disc(a,LENS[lens],lens)+(o33_fade(a) if lens in ('bal','balanced') else 0.0); cl=cur if cur else lp*frac(a,pa,g); prod=0.0   # ORDER B: frac carries g (B-1 ladder, dial-off identical); o33_fade = B-2 fallback (0 when off)
    if g0 is None: g0=g
    if fut is None: fut=[(g,1.0)]
    for k in range(18):
        ag=a+k
        if ag>38 or frac(ag,pa,g)<0.42: break
        lev=lp*frac(ag,pa,g)
        if ag<=pa: lev=max(lev,cl)
        if k==0: lev=max(lev,cl)
        if k==0 and pre_hc>0 and BASE_REF==2026 and AGE_REF==2026: lev*=(1-pre_hc)  # B2 present-unavailability haircut (Now board only)
        base=lev+capt_prem(lev)
        _df=disc_factor(a,d,k,lens,grace)
        if k==0: prod+=posval(base-REPL[g0])*21/_df
        else: prod+=sum(w*posval(base-REPL[gg]) for gg,w in fut)*21/_df
    if g in('KPF','KPD'): prod*=1.05
    if _O33 and _O33S>=1 and g in('KPF','KPD'): prod*=O33_SSTAR   # ORDER B B-1: anchor-preserving renorm on the tall PROJECTION stream only (the floor is a current-level object and is NOT renormed — disclosed in the packet)
    runway=clamp((25-a)/6.0,0,1); elite=clamp((lp/PEAK[g]-0.97)/0.30,0,1); prod*=(1+runway*elite*PMAX)
    return prod
def prod_floor(p,lens='bal'):
    g=bnow(p); a=age(p); pa_=PEAK_AGE[g]; cur=level_now(p)
    if cur is None: return 0
    # ==== §1b FLOOR HALF (R106.7, DECISIONS v121 §1; RL_FLEX-gated via y0dpp_bar) — the leg-blind bar, floor half.
    # §1b applies to WHICHEVER leg produces the year-0 number: the projection half is wired at v_at_peak
    # (distribution_pricing.py:250); THIS is the DEMONSTRATED-FLOOR half. The floor's YEAR-0 (k==0) REMAINING-SEASON
    # component nets vs the LOWER post-collapse dual bar (y0dpp_bar); the banked SEASON_PROG component + the level
    # path/horizon stay keyed to PRESENT (bnow). The blend is done OUTSIDE the nonlinearity — TWO posval
    # evaluations at k==0, sp·posval(base-REPL[present]) + (1-sp)·posval(base-REPL[low]) — NEVER a blended bar
    # inside one posval call (owner condition 1). Now-board only (AGE_REF==BASE_REF; remaining-season is a present
    # concept). years-1+ (k>=1) + the banked component untouched. RL_FLEX=0 => y0dpp_bar None => byte-exact off.
    # ⚠ DUPLICATE-LOOP HAZARD (owner condition 4): _merged_recover.py::_prod_floor_w4 is a PARALLEL copy of THIS
    # loop for PROVEN players on the shipped board (run_panel.sh -> ev()). It carries the SAME §1b k==0 split —
    # edit BOTH or neither. Queued hygiene (NOT this build): collapse the copy via option-3 delegation.
    lowbar=y0dpp_bar(p) if (AGE_REF==BASE_REF) else None
    _gr=grace_years(p)                                    # ORDER 28 grace-A (dial-gated; 0 => byte-exact)
    d=age_disc(a,LENS[lens],lens)+(o33_fade(a) if lens in ('bal','balanced') else 0.0); H=clamp((40-a)/3.0,1.0,3.0); prod=0.0; k=0   # ORDER B B-2 fallback fade (0 when off)
    while k<H:
        ag=a+k; wt=min(1.0,H-k)
        lev=cur*min(1.0, frac(ag,pa_,g)/max(frac(a,pa_,g),1e-6))   # ORDER B B-1: the ladder reaches the floor's decline RATIO (dial-off identical)
        if k==0 and p.get('_avail_hc',0)>0 and BASE_REF==2026 and AGE_REF==2026: lev*=(1-p['_avail_hc'])
        base=lev+capt_prem(lev)
        if k==0 and lowbar is not None:
            sp=SEASON_PROG                                    # banked (sp) vs present bar; remaining (1-sp) vs low bar
            pv=sp*posval(base-REPL[g])+(1.0-sp)*posval(base-REPL[lowbar])
        else:
            pv=posval(base-REPL[g])
        prod+=wt*pv*21/disc_factor(a,d,k,lens,_gr); k+=1
    return val(prod)
# ===== cont.20: v4 LEARNED FORWARD-PROJECTION (peak_est spine) =====
# Replaces old blended cohort+demoPeak. Model = forward-realised best-3 (>=Y, completeness-weighted), bust-inclusive.
# Feeds BOTH production (player_raw->proj_from_peak) and the pedestal's `relative`. Lazy-loaded: needs sklearn at
# BUILD time only (shipped board is static HTML). Late-binds PVC (built at line ~503, after this def).
_V4MODEL=None; _BUSTPT=None; _V4PVC=None
_POSI={'MID':0,'SD':1,'SF':2,'KPD':3,'KPF':4,'RUCK':5}
V4_SPIKE_RETAIN={'KPD':0.69}   # cont.20: pull v4 spike-excess toward baseline for UNCONFIRMED KPD spikes (v4 over-trusts +0.28; level_now SPIKE_CAP can't reach the projection). Dial-able; KPF off by default.
# cont.20: EXPLICIT unproven-floor (researched position x pick x tenure expected peak). Beats v4 on OUT-OF-SAMPLE
# GROUP calibration (4.8 vs 6.0 weighted cell bias) — v4 systematically OVER-projects piners (MID +12, generals +5).
# Blended into peak_est by games-played weight: unproven -> explicit floor; proven -> v4 (form). NOT double-count:
# one peak estimate blended (not summed), and prod_floor independently protects demonstrated production.
EXP_PEAK_BASE={'MID':60.5,'SD':56.9,'SF':49.6,'KPD':51.1,'KPF':44.7,'RUCK':66.6}  # T=1 expected peak by pos (realised piner means)
EXP_RETAIN={  # position-specific pining decay normalized to T1 (smoothed monotone from realised outcomes): RUCK/KPD slow-burn, MID/fwds steeper
 'RUCK':[1.00,0.95,0.91,0.85],'KPD':[1.00,0.95,0.95,0.93],'MID':[1.00,0.92,0.83,0.65],
 'SD':[1.00,0.96,0.92,0.88],'SF':[1.00,0.90,0.88,0.83],'KPF':[1.00,0.95,0.85,0.80]}
EXP_PICK_SLOPE=-10.72; EXP_LOGREF=4.0073   # expected peak vs (log effpk - logref); negative = deeper pick projects lower
EXP_BLEND_GAMES=float(os.environ.get('RL_EXP_BLEND_GAMES','45'))    # career games at which v4 (form) fully
# replaces the explicit floor. #334 MENU ITEM (a) — THE COHORT-FORWARD YOUNG ANCHOR. Lowering this makes a
# young player's projection lean on his own FORM sooner and on the year-4/5 cohort prior for less of his
# early career; the owner's menu asks what that does to the relativity guard and the envelope at 45 -> 30
# -> 20. 45 is the shipped value and is therefore the identity. A MENU ITEM FOR HIS SITTING, NOT A DECISION.
def _explicit_peak(p,Y):
    pos=gfut(p) # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
    if pos not in EXP_PEAK_BASE: return None
    T=max(Y-debut(p)+1,1); ret=EXP_RETAIN[pos][min(T,4)-1]
    pe=EXP_PEAK_BASE[pos]*ret+EXP_PICK_SLOPE*(math.log(min(effpk(p),70))-EXP_LOGREF)
    return clamp(pe,30.0,105.0)
def _v4_init():
    global _V4MODEL,_BUSTPT,_V4PVC
    if _V4MODEL is None:
        import pickle as _pk
        _V4MODEL=_pk.load(open('peak_model_v4.pkl','rb'))['model']
        _BUSTPT=json.load(open('bust_prior_table.json'))
        _V4PVC=json.load(open('pvc_snapshot.json'))   # peak-model's TRAIN-TIME PVC feature (logPVC), FROZEN by design to break the SCALE<->PVC<->peak_est bootstrap cycle. This is NOT the live PVC and must NOT track it: build_peak_model_v4.py trained the pickle on THIS PVC (see its co-emit of pvc_snapshot.json); feeding the live (post-bake) PVC here would be train/serve skew. Pinned + stamped read-only (Phase-4 disposition, DPP-strip build); regenerated only by the peak-model build.
def _v4_bp(po,pk): return _BUSTPT[po][str(min(max(int(round(pk)),1),70))]
def _v4_best(ss,n):
    a=sorted([x['avg'] for x in ss if x['games']>=6],reverse=True)[:n]; return float(np.mean(a)) if a else None
def _v4_age(p,Y):
    by=p.get('_by'); return (Y-by) if by else (Y-(debut(p)-18))
def _v4_feats(p,Y):
    d=debut(p); pos=gfut(p); ep=min(effpk(p),70); T=Y-d+1 # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
    sub=[x for x in p['scoring'] if x['year']<=Y]; gg=sum(x['games'] for x in sub); nss=len([x for x in sub if x['games']>=6])
    b2=_v4_best(sub,2); b1=_v4_best(sub,1); maxg=max([x['games'] for x in sub],default=0)
    rs=[x for x in sub if x['games']>=6][-2:]
    recent=float(np.average([x['avg'] for x in rs],weights=[x['games'] for x in rs])) if rs else 0
    last=[x for x in sub if x['year']==Y]; la=last[0]['avg'] if last else 0; lg=last[0]['games'] if last else 0
    early=sum(x['games'] for x in sub if x['year']-d+1<=2); seq=[x['avg'] for x in sub if x['games']>=6]; slope=(seq[-1]-seq[0]) if len(seq)>1 else 0.0
    bestyr=max([x['year'] for x in sub if x['games']>=6 and x['avg']==(b1 or -1)],default=Y); ysb=Y-bestyr
    return [np.log(_V4PVC[str(ep)]),ep,_POSI[pos],b2 or 0,b1 or 0,recent,la,lg,gg,nss,maxg,early,slope,ysb,_v4_age(p,Y),T,_v4_bp(pos,ep)]
def _v4_draft_feat(p):
    pos=gfut(p)  # ITEM 271 item 4 GROUP A
    ep=min(effpk(p),70); return [np.log(_V4PVC[str(ep)]),ep,_POSI[pos],0,0,0,0,0,0,0,0,0,0,0,_v4_age(p,debut(p)-1),0,_v4_bp(pos,ep)]
def _v4_spike_guard(p,Y,pe):           # KPD spike caution on the PROJECTION (level_now SPIKE_CAP is a separate path)
    r=V4_SPIKE_RETAIN.get(gfut(p)) # ITEM 271 item 4 GROUP A: drafted -> played axis (gfut); the board prices on gfut and this site read the drafted position.
    if not r: return pe
    ss=sorted([x for x in p['scoring'] if x['year']<=Y and x['games']>=6],key=lambda x:x['year'])
    if len(ss)<3: return pe             # need 2 prior seasons (baseline) + the spike
    base=(ss[-2]['avg']+ss[-3]['avg'])/2.0
    if base>=55 and ss[-1]['avg']>=1.30*base and pe>base: pe=base+r*(pe-base)   # unconfirmed (spike is latest >=6g season as-of Y)
    return pe
_PE_CACHE={}
def _pe_clear(): _PE_CACHE.clear()     # call after toggling V4_SPIKE_RETAIN or BASE_REF-independent state in tests
def peak_est(p):                       # cont.20: learned v4 forward-projection (MEMOIZED by (player,BASE_REF)); was blended cohort+demoPeak
    _k=(id(p),BASE_REF)
    if _k in _PE_CACHE: return _PE_CACHE[_k]
    g=gfut(p); ln=level_now(p); pk=effpk(p)
    cp,tg=cohort_peak(g,pk,srel(p),p)                           # #336 AMENDMENT 2: thread the player so the cohort baseline conditions on his resolved state
    if cp is None: cp=basepk_c_p(p,g,pk)                        # #336 AMENDMENT 2 — enumerated BPK consumer 3: no track at all -> the PURE class anchor, so the resolved-state selection matters most here
    if ln is None: _PE_CACHE[_k]=cp; return cp   # no demonstrated level -> cohort prior (in-window 0-game players hit unpl_eq in value() before here)
    _v4_init(); Y=BASE_REF
    v4pe=float(_V4MODEL.predict([_v4_feats(p,Y)])[0]) if (Y-debut(p)+1)>=1 else float(_V4MODEL.predict([_v4_draft_feat(p)])[0])
    v4pe=_v4_spike_guard(p,Y,v4pe)
    exp=_explicit_peak(p,Y)
    if exp is not None:
        w=clamp(p.get('games',0)/EXP_BLEND_GAMES,0.0,1.0)   # unproven -> explicit floor; proven -> v4 (form)
        pe=(1.0-w)*exp+w*v4pe
    else:
        pe=v4pe
    _PE_CACHE[_k]=pe
    return pe
def player_raw(p,lens='bal'):
    g0 = bnow(p) if AGE_REF==BASE_REF else gfut(p)   # A2 (PARKED 4): on forward boards (AGE_REF>BASE_REF) the year-0 present has rolled to the future position, so its replacement bar uses gfut, not the present bucket
    return proj_from_peak(gfut(p),peak_est(p),age(p),level_now(p),lens,g0=g0,fut=futblend(p),pre_hc=p.get('_avail_hc',0.0),grace=grace_years(p))   # ORDER 28 grace-A (dial-gated; 0 => byte-exact)
def pa(g): return PEAK_AGE[g]
# unplayed prospects: recent national/rookie draftees not yet debuted (valued on pedigree alone, like the old engine)
extra=[]
for p in data:
    if p['_grp'] in ('ND','RD') and p['year']>=2024 and p['pos'] in GRP and sum(r['games'] for r in p['scoring'])==0:
        q=dict(p); q['_unplayed']=True; extra.append(q)
def active(p):
    if p['pos'] not in GRP or p.get('_retired'): return False
    if p.get('_last_listed') is not None and p['_last_listed']<2026: return False  # delisted before 2026 -> off Now (recalled onto back-boards)
    if p.get('_unplayed') or p.get('_force_active'): return True
    played=any(r['games']>=1 for r in p['scoring'])
    recent=p.get('_has26') or any(r['year']>=2024 for r in p['scoring']) or p['year']>=2024
    return played and recent
players=[p for p in (data+extra) if active(p)]
def _dkey(p): return (p['key'] or slug(p['player']))+('|u' if p.get('_unplayed') and not p['key'] else '')
def _rich(p): return (-(p['year'] or 9999), len(p['scoring']), 1 if p.get('pick') else 0)  # collapse duplicate-key groups to the EARLIEST entry (original draft record); fuller-history/real-pick as tiebreak
_best={}; _order=[]
for p in players:
    k=_dkey(p)
    if k not in _best: _order.append(k); _best[k]=p
    elif _rich(p) > _rich(_best[k]): _best[k]=p     # prefer fuller-history / real-pick record over a thin traded-club row
players=[_best[k] for k in _order]
played=[p for p in players if not p.get('_unplayed')]
STBL=True
# ==== ORDER B (RL_O33): THE PRE-ANCHOR BASIS SECTION RUNS ON THE DIAL-OFF BASIS. ======================
# The ruled mechanisms reprice VETERANS; they must not re-denominate the board. Two anchors in this
# module are computed FROM player/pick streams at load: the P99 `ref` (line below) and the v3.4
# pre-anchor PVC head that BOARD_FACTOR divides by (:~1447). With the dial live during load, the tall
# ladder moves that basis and SCALE lifts EVERY row (+6.4% measured — the leg-1 diagnosis,
# docs/evidence/order_b_build_2026-08-17/QUICKLOOK_out.txt pre-fix). So the stage is forced to 0 from
# here until just after BOARD_FACTOR, then restored: dial-on and dial-off boards share ONE currency, and
# the numeraire s (pick_redenomination.json) is untouched either way. Dial off => nothing happens here.
if _O33 and _O33S>=1: _o33_bas=_O33S; _O33S=0
ref=np.percentile([player_raw(p,'bal') for p in played],99); SCALE=7000/ref**GAMMA   # anchor on stable basis
STBL=False
for p in played: p['_pr']=player_raw(p,'bal')
val=lambda r: round(SCALE*r**GAMMA) if r>0 else 0
# ---- UNIFIED pick value: expected baseline draftee, position-mix + survival weighted, same currency ----
def pick_raw(k,lens='bal'):
    b=bandof(k); s=0
    for g,w in MIX[b].items():
        if w<=0: continue
        s+=w*proj_from_peak(g, basepk(g,b), 19, None, lens)
    return s*(1-BUST_BAND.get(b,0.15))
# value-based pick curve: recency-weighted MEAN PEAK VALUE per pick, monotone-regularised
def peakval(p):
    g=GRP[p['pos']]; pk=pkbest(p); ep=effpk(p)
    if pk is None: return val(pick_raw(ep))*0.25
    # #336 AMENDMENT 2 — enumerated BPK consumer 4: the CURVE-TEACHING normaliser. Reaching this line
    # requires pkbest(p) is not None, i.e. a >=10-game season, i.e. this historical player IS established
    # by the ruled >=6-game bar. He must therefore be normalised against the establisher baseline, not
    # against the entrant expectation — otherwise every established teacher looks artificially far above
    # his class and the pick curve inflates. (This is a curve-fit site on the numeraire chain: its effect
    # shows up as SCALE, which the board delta reports separately from re-ranking.)
    return val(proj_from_peak(g,pk,PEAK_AGE[g],pk,'bal'))*clamp((pk/max(basepk_c_p(p,g,ep),40.0))**2.2,0.40,3.0)
def _sgn(x): return (x>0)-(x<0)
def _edge(h0,h1,d0,d1):
    m=((2*h0+h1)*d0-h0*d1)/(h0+h1)
    if _sgn(m)!=_sgn(d0): m=0.0
    elif _sgn(d0)!=_sgn(d1) and abs(m)>3*abs(d0): m=3*d0
    return m
def _pchip(xs,ys,xq):
    n=len(xs); h=[xs[i+1]-xs[i] for i in range(n-1)]; dl=[(ys[i+1]-ys[i])/h[i] for i in range(n-1)]
    m=[0.0]*n
    m[0]=_edge(h[0],h[1],dl[0],dl[1]) if n>2 else dl[0]
    m[-1]=_edge(h[n-2],h[n-3],dl[n-2],dl[n-3]) if n>2 else dl[-1]
    for i in range(1,n-1):
        if dl[i-1]*dl[i]<=0: m[i]=0.0
        else:
            w1=2*h[i]+h[i-1]; w2=h[i]+2*h[i-1]; m[i]=(w1+w2)/(w1/dl[i-1]+w2/dl[i])
    out=[]
    for x in xq:
        i=0
        while i<n-2 and x>xs[i+1]: i+=1
        t=(x-xs[i])/h[i]; t2=t*t; t3=t2*t
        out.append((2*t3-3*t2+1)*ys[i]+(t3-2*t2+t)*h[i]*m[i]+(-2*t3+3*t2)*ys[i+1]+(t3-t2)*h[i]*m[i+1])
    return out
ALPHA=0.6                                          # risk-aversion dial for pick curve (lower = more risk-averse)
def _ce(vals,al):
    v=np.array([max(x,1.0) for x in vals]); return float((np.mean(v**al))**(1.0/al))
def build_pvc(alpha):
    raw=[float('nan')]*99
    for _k in range(1,100):
        vs=[peakval(p) for p in _curve_sample('build_pvc',_k,                       # ADDENDUM 1: pool rows do not teach the curve;
            [p for p in hist if _teaches_curve(p) and abs(_epk(p)-_k)<=4])]         # registered so the check watches THIS list
        if vs: raw[_k-1]=_ce(vs,alpha)
    for _i in range(99):
        if raw[_i]!=raw[_i]: raw[_i]=raw[_i-1] if _i else 5000.0
    raw=[float(round(x)) for x in raw]                # snap to int so iso pooling is language-stable
    vv=[-v for v in raw]; idx=[[i] for i in range(99)]; i=0       # weighted-equal isotonic (decreasing)
    while i<len(vv)-1:
        if vv[i]>vv[i+1]+1e-9:
            nv=(vv[i]*len(idx[i])+vv[i+1]*len(idx[i+1]))/(len(idx[i])+len(idx[i+1]))
            vv[i]=nv; idx[i]+=idx[i+1]; del vv[i+1]; del idx[i+1]; i=max(0,i-1)
        else: i+=1
    iso=[0.0]*99
    for v,ix in zip(vv,idx):
        for j in ix: iso[j]=-v
    kx=[];ky=[];i=0                                              # PCHIP through plateau centres -> smooth, strict
    while i<99:
        j=i
        while j+1<99 and abs(iso[j+1]-iso[i])<1e-6: j+=1
        kx.append((i+j)/2.0); ky.append(iso[i]); i=j+1
    if kx[0]>0: kx=[0.0]+kx; ky=[iso[0]]+ky
    if kx[-1]<98: kx=kx+[98.0]; ky=ky+[iso[-1]]
    sm=_pchip(list(kx),list(ky),list(range(99)))
    for i in range(1,99): sm[i]=min(sm[i],sm[i-1]-1)
    return {k:max(210,int(round(sm[k-1]))) for k in range(1,100)}
# ============================================================================
# v3.4 PICK-VALUE CURVE (shipped 2026-06-20; the "R-0 proposal", locked by Luke).
# Replaces the legacy build_pvc above (kept for reference + the scale anchor). Method:
#   MEASURE  : posval(best2 + captaincy - REPL), busts -> 0   (NO bust floor, NO survivor clamp)
#   RISK     : tiered CE alpha PVC_ALPHA_LO->HI (0.6 at pick1 -> 0.8 cheap end, flat after pick 50)
#   SMOOTHER : varying-bandwidth local-linear (W 3 at the steep top -> 9 in the noisy tail)
#   TOP      : parametric power-decay a*k^b fit to picks 1-8, blended into loclin below ~pick 12
#   MONOTONE : light isotonic (PAVA) final pass -> non-increasing (plateaus allowed)
#   SCALE    : posval-VOR units mapped to SCAR by anchoring the pooled top band (picks 1-3) to the
#              legacy realised value -> preserves the board's top; players (forward model) untouched.
# Set PVC_REPL_BUF=5 for the R-5 (cheap-end-propped) variant. Full rationale: HANDOVER cont.(10).
# ============================================================================
PVC_ALPHA_LO, PVC_ALPHA_HI = 0.6, 0.8     # tiered risk dial for the pick curve (cost-tiered CE)
PVC_REPL_BUF = 0                          # replacement buffer: 0 = R-0 (shipped); 5 = R-5 (cheap end propped)
def _ce0(vals,al):                        # CE flooring busts at 0 (legacy _ce floors at 1, wrong for busts->0)
    v=np.array([max(x,0.0) for x in vals]); return float((np.mean(v**al))**(1.0/al)) if len(v) else 0.0
def _nv_bwd(p):                           # v3.4 backward per-pick value: posval-VOR on best2, busts -> 0
    b2=best2(p)
    return posval(b2+capt_prem(b2)-(REPL[GRP[p['pos']]]-PVC_REPL_BUF)) if b2>0 else 0.0
def _alpha_pvc(k): return PVC_ALPHA_LO+(PVC_ALPHA_HI-PVC_ALPHA_LO)*min(k-1,49)/49.0
def _loclin1(series,k,W,N):               # weighted local-linear fit over a 1..N series, evaluated at k
    pts=[(j+1,series[j],(W+1-abs(j+1-k))) for j in range(N) if abs(j+1-k)<=W and series[j]==series[j]]
    Wt=sum(w for *_,w in pts); xb=sum(w*x for x,_,w in pts)/Wt; yb=sum(w*y for _,y,w in pts)/Wt
    sxx=sum(w*(x-xb)**2 for x,_,w in pts)
    if sxx<1e-9: return yb
    b=sum(w*(x-xb)*(y-yb) for x,y,w in pts)/sxx
    return (yb-b*xb)+b*k
def build_pvc_v34():
    N=99
    raw=[float('nan')]*N                                          # 1. raw band value, new measure, tiered alpha, +-4
    for k in range(1,N+1):
        vs=[_nv_bwd(p) for p in _curve_sample('build_pvc_v34',k,                    # ADDENDUM 1: pool rows do not teach the curve;
            [p for p in hist if _teaches_curve(p) and abs(_epk(p)-k)<=4])]          # registered so the check watches THIS list
        if vs: raw[k-1]=_ce0(vs,_alpha_pvc(k))
    for i in range(N):
        if raw[i]!=raw[i]: raw[i]=raw[i-1] if i else 0.0
    Wf=lambda k:int(round(3+6*min(k-1,60)/60.0))                  # 2. varying-bandwidth local-linear (3 top -> 9 tail)
    llv=[_loclin1(raw,k,Wf(k),N) for k in range(1,N+1)]
    kf=np.arange(1,9); yf=np.array([max(raw[i],1e-6) for i in range(8)])   # 3. parametric power top, fit to picks 1-8
    _B,_lA=np.polyfit(np.log(kf),np.log(yf),1); _A=math.exp(_lA)
    par=[_A*(k**_B) for k in range(1,N+1)]
    blend=[par[k-1] if k<=6 else llv[k-1] if k>=12 else                    # blend parametric top into loclin below
           ((12-k)/6.0)*par[k-1]+(1-(12-k)/6.0)*llv[k-1] for k in range(1,N+1)]
    vv=[-t for t in blend]; idx=[[i] for i in range(N)]; i=0     # 4. light isotonic (decreasing) -> monotone
    while i<len(vv)-1:
        if vv[i]>vv[i+1]+1e-9:
            m=(vv[i]*len(idx[i])+vv[i+1]*len(idx[i+1]))/(len(idx[i])+len(idx[i+1]))
            vv[i]=m; idx[i]+=idx[i+1]; del vv[i+1]; del idx[i+1]; i=max(0,i-1)
        else: i+=1
    iso=[0.0]*N
    for v,ix in zip(vv,idx):
        for j in ix: iso[j]=-v
    legacy=build_pvc(ALPHA)                                     # 5. SCALE posval-VOR -> SCAR: anchor the pooled top
    legacy_top=float(np.mean([legacy[k] for k in (1,2,3)]))     #    band (picks 1-3) to the CURRENT board's top so the
    new_top=float(np.mean(iso[:3]))                             #    board scale is preserved (players already untouched);
    SCALE_PVC=legacy_top/new_top if new_top>0 else 1.0          #    v3.4 is then a pure SHAPE change. (legacy = old curve,
    pvc=[v*SCALE_PVC for v in iso]                              #    used for the anchor only.)
    for i in range(1,N): pvc[i]=min(pvc[i],pvc[i-1])             # 6. enforce non-increasing (plateaus allowed)
    return {k:max(210,int(round(pvc[k-1]))) for k in range(1,N+1)}
def _load_numeraire(p1, _path='pvc_curve_v2.json'):
    """E6 (#279 step 4): read the ONE measured pooled head the whole economy re-denominates from.

    FAIL-CLOSED BY DESIGN, both directions, because the failure this closes is SILENT one-sided scaling:
      * ABSENCE PATH — an artifact with no `numeraire` block HALTS. It never falls back to the old
        _P1/PVC[1] denominator, because that fallback is exactly the one-sided behaviour being removed and a
        silent restoration of it would look like success. Every PRE-PROPAGATION artifact lacks the block, so
        the edited engine and the candidate artifact are a PAIRED change that lands together.
      * COHERENCE — s is recomputed from the block's own head and pin and compared to the block's published s.
        A disagreeing RL_PICK1, or a doctored block, HALTS NAMING BOTH VALUES rather than scaling one side.
    """
    import json as _j, os as _o
    if not _o.path.exists(_path):
        raise SystemExit("E6 numeraire HALT: %s not found; the pooled head cannot be read." % _path)
    _d = _j.load(open(_path))
    _n = _d.get('numeraire')
    if not isinstance(_n, dict):
        raise SystemExit(
            "E6 numeraire HALT: %s carries NO 'numeraire' block.\n"
            "  The pooled-numeraire economy re-denominates picks and players from ONE measured head; without\n"
            "  it the player side would silently fall back to the v3.4 pre-anchor head (the one-sided defect\n"
            "  #279 step 4 removes). This is not a fallback condition — install the candidate artifact, which\n"
            "  carries {'pooled_head_pre_scale', 's', 'published_pin'}." % _path)
    for _k in ('pooled_head_pre_scale', 's', 'published_pin'):
        if _n.get(_k) is None:
            raise SystemExit("E6 numeraire HALT: 'numeraire' block in %s is missing '%s' (got %s)."
                             % (_path, _k, sorted(_n)))
    _H = float(_n['pooled_head_pre_scale']); _pub = float(_n['published_pin']); _s = float(_n['s'])
    if _H <= 0:
        raise SystemExit("E6 numeraire HALT: pooled_head_pre_scale must be > 0, got %r." % _H)
    _recomputed = _pub / _H
    if abs(_recomputed - _s) > 1e-9:
        raise SystemExit(
            "E6 numeraire COHERENCE HALT: the artifact's published s and its own head disagree.\n"
            "  published s          = %.12f\n  recomputed %g/%g = %.12f\n  difference           = %.3e\n"
            "  One of the two was edited without the other. Both sides of the economy scale from this number,\n"
            "  so a disagreement here is a one-sided repricing waiting to happen."
            % (_s, _pub, _H, _recomputed, abs(_recomputed - _s)))
    if abs(_pub - p1) > 1e-9:
        raise SystemExit(
            "E6 numeraire COHERENCE HALT: RL_PICK1 disagrees with the artifact's published pin.\n"
            "  RL_PICK1             = %.6f\n  artifact published_pin = %.6f\n"
            "  The ladder was published against the artifact's pin; scaling players against a different pin\n"
            "  would move the player side alone. Set RL_PICK1 to the artifact's pin, or re-derive the curve."
            % (p1, _pub))
    return {'H': _H, 's': _s, 'published_pin': _pub}
PVC=build_pvc_v34()
CURVE_H=1.0                          # curve HEIGHT multiplier (slider); 1.0 = natural CE shape (best/pick1~2.96)
PVC={k:max(210,int(round(v*CURVE_H))) for k,v in PVC.items()}
# ── PICK-1 ANCHOR (Luke, 2026-06-21), RE-ANCHORED TWO-SIDED by E6 (#279 step 4, seam word F3 2026-07-30).
#
#    WHAT THE OLD COMMENT CLAIMED, and what was actually measured at the step-4 rehearsal. It said "the WHOLE
#    board (picks + players) scales to it ... one global factor preserves all relativities/trades". That was
#    true when the v3.4 import fit WAS the shipped curve. It is not true now, and the measurement says so:
#      * the player side takes _P1/PVC[1] where PVC[1] here is the v3.4 PRE-ANCHOR head — measured 4441, a
#        curve that NO LONGER SHIPS. BOARD_FACTOR is therefore 3000/4441 = 0.675524, a real and load-bearing
#        player scaling, not a no-op.
#      * the pick side is overwritten downstream by the adopted artifact pvc_curve_v2.json (:928-945,
#        PVC=_PVC2M), head 3000. The rescale on the next line never reaches the shipped curve.
#    So the two sides are anchored on DIFFERENT CURVES and agree today only because RL_PICK1 and the artifact
#    pin are both 3000 — a coincidence of the pin's value, not a property of the construction. Measured:
#    RL_PICK1 3000->3500 moves SCALE 4.719196->5.505729 while the shipped PVC stays 3000/2767/571.
#
#    THE TWO-SIDED ACT. Under the pooled numeraire the derivation measures ONE pooled head H and publishes
#    s = RL_PICK1/H; the installed ladder is already raw x s. The player side must take THE SAME s, applied to
#    its own natural scale — NOT _P1/H, which would mix two different fits' currencies (H is the structural/VOR
#    raw head; 4441 is the v3.4 kernel head; they are not commensurate). So:
#        BOARD_FACTOR = (_P1 / PVC[1]) * s
#    One measured head, one factor, both sides. s is read from the artifact's own `numeraire` block so H lives
#    in exactly ONE place and the two sides cannot be re-derived independently.
_P1=float(__import__('os').environ.get('RL_PICK1','3000'))
_NUM=_load_numeraire(_P1)                                    # LOUD-HALTs on a missing block or an incoherent s
BOARD_FACTOR=(_P1/PVC[1])*_NUM['s']; SCALE=SCALE*BOARD_FACTOR   # SCALE reassigned → val() (late-binding) scales players too
PVC={k:int(round(v*BOARD_FACTOR)) for k,v in PVC.items()}    # pre-swap basis only; the shipped curve comes from the artifact
if _O33 and '_o33_bas' in globals(): _O33S=_o33_bas; del _o33_bas   # ORDER B: end of the dial-off BASIS section (see the block above the P99 ref) — the stage returns live for every runtime consumer
# --- de-plateau (Luke): the monotone pass pools noisy mid-curve bands to a flat run; ramp each interior flat run
#     linearly through its real endpoints so picks decline smoothly, leaving the genuine DEEP-TAIL floor flat
#     (runs starting at pick>=46 are the floor and stay flat). Mid-curve only; pure shape, anchor (pick1) untouched.
def _deplateau(P, start_before=46):
    P=dict(P); N=len(P); i=1
    while i<=N:
        j=i
        while j<N and P[j+1]==P[i]: j+=1
        if j>i and j<N and P[j+1]<P[i] and i<start_before:          # interior flat run with a lower neighbour, mid-curve
            hi=P[i-1] if i>1 else P[i]; lo=P[j+1]; span=j-(i-1)+1
            for t,k in enumerate(range(i,j+1),1): P[k]=int(round(hi+(lo-hi)*t/span))
        i=j+1
    for k in range(2,N+1): P[k]=min(P[k],P[k-1])                    # safety monotone
    return P
PVC=_deplateau(PVC)
# ===== LEG D FIVE-MIGRATION (RL_PVC2, ruling R107.5): carry the OFFLINE-DERIVED, stamped pvc_curve_v2.json
#       to the rl_model.py MA.PVC consumers below. _PVC2M is the v3.4 ruler object PVC by default, so
#       RL_PVC2=0 => the consumers read byte-identical PVC => board 9829d01a byte-exact (the kill-switch
#       proof, re-proven per commit); under RL_PVC2 (default ON) it is the loaded v2 curve. OFFLINE +
#       LOADED, NO new import-time fit (the RL_PVCADOPT/L1b template; rl_export.py:61 already loads this
#       artifact). The consumers are repointed PVC[...] -> _PVC2M[...] ONE AT A TIME (jobs 2-5); the v3.4
#       import fit above still runs and is byte-exact when off. peak-model _V4PVC (:515) is NOT wired here
#       (job 1 HOLD: train/serve skew, retrain = post-bake fallback).
_PVC2M=PVC
def _split_ladder(raw, what, strict=True, legacy_domain=False):
    """THE SPLIT. Take a raw pick->value map and return the ruled ladder: the national curve over 1..64, plus
    ONE entry at POOL_PICK carrying the pool's single position-blind level. Nothing past POOL_PICK survives, so
    no lookup can ever return a value indexed to a selection number above 64 (RULEBOOK v2.1 law 4).

    The DOMAIN restriction is unconditional — it is the ruling, and it applies to every ladder the engine builds.
    G-MONO (strict descent) is asserted with strict=True, which is every ladder that SHIPS. It is relaxed only
    for a TRANSIENT intermediate basis that is overwritten before anything is written — see the RL_PVCADOPT L1b
    load, which _PVC2/_PVC0 replaces a few lines later. That is a scope judgement about where the law bites, not
    a weakening of it: the shipped curve is asserted strictly in rl_export, unconditionally.
    The pool is exempt from monotonicity BY THE RULING, not by leniency — it is one value, not an ordering, so
    'descending' is not a property it can have."""
    # REFUSE an over-long domain rather than silently truncating it. This is the direction that matters: a
    # ladder still carrying entries past the pool index IS the old 1-99 model, and quietly dropping them would
    # let it come back unnoticed — the exact failure this job exists to end. legacy_domain=True is the single
    # declared exception, for the SUPERSEDED L1b artifact which is still on disk at its original 1-99 domain.
    _over=sorted(_k for _k in raw if _k>POOL_PICK)
    assert legacy_domain or not _over, \
        "%s: ladder carries %d entries past the pool index %d (%s...) — there is no price for a pick above %d. "\
        "The 1-99 ladder has come back; restrict the artifact's domain rather than relying on a silent truncation."\
        %(what,len(_over),POOL_PICK,_over[:6],ND_CURVE_LAST)
    nd={_k:int(_v) for _k,_v in raw.items() if _k<=ND_CURVE_LAST}
    assert min(nd)==1 and max(nd)==ND_CURVE_LAST and len(nd)==ND_CURVE_LAST, \
        "%s: national curve must cover exactly 1..%d, got %d entries %s..%s"%(what,ND_CURVE_LAST,len(nd),min(nd),max(nd))
    assert nd[1]==3000, "%s numeraire: curve(1)=%r != 3000"%(what,nd[1])
    if strict:
        _bad=[_k for _k in range(1,ND_CURVE_LAST) if not nd[_k]>nd[_k+1]]
        assert not _bad, "%s G-MONO: national curve 1..%d is not STRICTLY decreasing — %d plateau(s) at picks %s"%(
            what,ND_CURVE_LAST,len(_bad),_bad[:8])
    else:
        assert all(nd[_k]>=nd[_k+1] for _k in range(1,ND_CURVE_LAST)), \
            "%s: transient basis is not even non-increasing over 1..%d"%(what,ND_CURVE_LAST)
    _pool=raw.get(POOL_PICK)
    assert _pool is not None, "%s: no pool level (expected 'pool_value', or an entry at %d)"%(what,POOL_PICK)
    nd[POOL_PICK]=int(_pool)
    return nd
if os.environ.get('RL_PVC2','1')!='0':
    _V2DOC=json.load(open('pvc_curve_v2.json'))
    _V2RAW={int(_k):int(_v) for _k,_v in _V2DOC['curve'].items()}
    if 'pool_value' in _V2DOC: _V2RAW[POOL_PICK]=int(_V2DOC['pool_value'])
    _PVC2M=_split_ladder(_V2RAW,'RL_PVC2 v2 curve')
else:
    # THE SPLIT applies to the kill-switch path too. A ladder that still runs to 99 behind a flag is still the
    # old model on disk, and the next seat reads flags as readily as defaults.
    _PVC2M=_split_ladder(PVC,'v3.4 import fit (RL_PVC2=0)')
# JOB 5 (RL_PVC2): GLOBAL PRODUCER SWAP — the module-level PVC now IS the migrated curve, so the RESIDUAL
# v3.4 readers below (the print-only value->pick-label `pe()` :1108-1110 and the `PVC:` diagnostic :1117)
# read v2 too. Leaf consumers (unpl_eq/pedestal) already read _PVC2M so there is no double-move; the
# build_pvc_v34 import fit + CURVE_H/BOARD_FACTOR/SCALE (computed ABOVE at :714-737, before _PVC2M) are
# untouched — SCALE stays frozen, so no player is rescaled. RL_PVC2=0 => _PVC2M IS PVC (same object) => this
# is `PVC=PVC`, a no-op => board 9829d01a byte-exact. Placed here (after _PVC2M) so the swap never reaches
# the producer transforms. rl_export rebuilds its OWN shipped curve from pvc_curve artifacts keyed by the
# _ADOPTED intersection, so g['PVC']'s key-set change (if any) does not reach the board (verified: board-null).
PVC=_PVC2M
# ===== #326 PER-DIVISION POOL LEVELS — the N43 signed table, resolved once per build ========================
# WHAT THIS IS. Before this, every pool entrant shared ONE number: the ladder's pool slot. The owner's signed
# data gives each intake pathway its own level and prices the rookie draft by position. This block resolves
# the fourteen levels and answers ONE question per player — which signed division is he? Nothing here prices
# anything; the pricing sites live in _merged_recover.py (the entry anchor: the year-zero floor, the
# thin-record blend, and the ruck prior cap's basis), per the owner's consumption ruling (addendum 5).
#
#   THE LEVELS ARE OWNER-SIGNED DATA — read verbatim from the curve artifact's pool_levels block and never
#   recomputed here. They are LADDER/BOARD currency (addendum 6 item 5); the conversion to engine-value
#   currency happens at the consuming site, not here, so this table stays the signed table.
#   ND65+ IS A LAW, NOT A NUMBER: min(the signed K15 measurement, the ruled curve's pick 64) read off the
#   LADDER IN FORCE at build time, so a curve re-derivation moves it with no edit to the signed block.
#   NO SILENT FALLBACK: a row the engine classifies as pool whose division is outside the signed set halts
#   and asks. That is the guard for a future pathway code (PSD or anything new), which must never take the
#   single pool value by default.
_PL_DOC=json.load(open('pvc_curve_v2.json')).get('pool_levels')
assert _PL_DOC, ('#326 HALT: pvc_curve_v2.json carries no pool_levels block — per-division pool pricing has '
                 'no signed data to read, and pricing every division at one level is the thing this replaces.')
_POOL_POS_FIELD=_PL_DOC['rd_position_field']
# ===== #334 ORDER 23 -- THE ND65+ CAP IS AMENDED AWAY (owner ruling, #334 comment 5262928754, owner ruling 2026-08-12) ======================
# OWNER, VERBATIM: "Happy to amend the law for ND > 64. As it's not going to impact many players
# anymore, only historical ones, as the ND never goes beyond pick 64 these days. So very few live
# players draw from that, and those who do would either have been delisted or have production
# determine their price now."
# THE SUPERSEDED LAW, PRESERVED HERE AS HISTORY RATHER THAN DELETED:
#     _ND65 = min(measured_k15, _PVC2M[cap_against_curve_pick])    # "THE CAP IS A LAW, NOT A NUMBER"
# It held a post-64 selection at the curve's pick-64 value so a pick-65 row could never outprice
# pick 64. ORDER 22 measured that this one blocked pathway was the SOLE cause of the residual on
# every other pathway. The owner removed it on the grounds above and accepted the consequence; the
# draft-boundary tension it guarded is queued for the pick-curve re-derivation. The signed block's
# `cap_against_curve_pick` key is retired under a dated name, so this file cannot silently re-cap.
# ND65+ NOW PRICES AT ITS DERIVED LEVEL, READ VERBATIM, LIKE EVERY OTHER SIGNED DIVISION.
_ND65=float(_PL_DOC['signed_nd65_plus']['measured_k15'])
_POOL_LEVELS={_k:int(float(_v)) for _k,_v in _PL_DOC['signed_flat'].items()}
_POOL_LEVELS['ND65+']=int(_ND65)
for _k,_v in _PL_DOC['signed_rd_positional'].items(): _POOL_LEVELS['RD:'+_k]=int(float(_v))
def _pool_rd_position(p):
    """The rookie draft's positional key. Named on ONE field so a wrong-field build is a one-word change
    that the sweep below then catches, rather than a silent misprice of ~85 entrants."""
    return GRP.get(p.get(_POOL_POS_FIELD)) or gfut(p)
def pool_division(p):
    """The signed intake division of a pool-classified entrant. Halts rather than defaulting."""
    _t=p.get('type')
    if _t=='RD': return 'RD:'+_pool_rd_position(p)
    if _t=='ND':
        _pk=p.get('pick') or 0
        if _pk>ND_CURVE_LAST: return 'ND65+'
        raise SystemExit('#326 HALT-AND-ASK: %s is a pool-classified national-draft row carrying pick %r. '
                         'ND65+ is type ND at pick >= %d; a pickless or in-curve national row resolves to no '
                         'signed division and must not take a default level.'%(p.get('player'),p.get('pick'),POOL_PICK))
    if _t in _POOL_LEVELS: return _t
    raise SystemExit('#326 HALT-AND-ASK: %s is classified pool by the engine but carries division type %r, '
                     'which is not in the signed set %s. A new pathway code prices at no level until the '
                     'owner signs one; it never takes the pool-wide value silently.'
                     %(p.get('player'),_t,sorted(_POOL_LEVELS)))
def pool_level(p):
    """The entrant's signed level, in LADDER currency. The consuming site converts (or does not) per the
    currency law: engine-value sites multiply by the board factor, ladder-currency sites do not."""
    return _POOL_LEVELS[pool_division(p)]
# THE WRONG-FIELD DISCRIMINATOR, over the whole store population rather than the priced board. The positional
# key must be the engine's own settled future position; keyed on present_position it differs on 171 of the
# rookie rows and on drafted_position on 181, so a wrong-field build fails here deterministically instead of
# surviving three builds in four. Only 7 of the differing rows are on the board, which is why this sweep runs
# over the store and not over the priced rows.
_rd_field_bad=[p.get('player') for p in data if p.get('type')=='RD' and _pool_rd_position(p)!=gfut(p)]
assert not _rd_field_bad, ('#326 HALT: the rookie-draft positional key reads %r, which disagrees with the '
                           'engine\'s settled future position on %d row(s) (%s). The N43 positional set was '
                           'measured on future_position; any other field misprices.'
                           %(_POOL_POS_FIELD,len(_rd_field_bad),_rd_field_bad[:6]))
# Every pool row resolves to a signed division AT BUILD TIME, so the halt above fires on the build rather than
# on whichever price happens to be asked for first. Membership is the ENGINE's own classification (the _pool
# flag set at :267-281) — never the pick number, which decides only inside type ND.
_POOL_DIV_COUNT=_Cnt(pool_division(p) for p in data if p.get('_pool'))
_pool_slot_mismatch=[p.get('player') for p in data if (effpk(p)>=POOL_PICK)!=bool(p.get('_pool'))]
assert not _pool_slot_mismatch, ('#326 HALT: %d row(s) sit at the pool slot without the pool flag or the '
                                 'reverse (%s) — the per-division lookup and the ladder would disagree about '
                                 'who is a pool entrant.'%(len(_pool_slot_mismatch),_pool_slot_mismatch[:6]))
# ===== ORDER 29 STEP 5 / PREREG P9 — THE UNSIGNED POOL v0 CELLS, AND THE LOUD BOOT ASSERT ==================
# The printed pool day-0 object (pvc_curve_v2.json::pool_v0) carries one cell per pathway x position. TWO
# cells have ZERO fit rows behind them — PDN|KPF and PDS|KPF — and are published as null, UNSIGNED. The
# derivation DID produce a fully-shrunk number for each (92.4 and 84.0, recorded in the artifact's
# `declined_unsigned`); those numbers were DECLINED, because a cell with no observations should not be given
# the appearance of a measurement just because the shrinkage machinery is willing to emit one.
#
# WHY THIS ASSERT EXISTS AT BOOT rather than at a pricing site: today NO pricing leg reads pool_v0 (the
# consumption rewire is deferred by owner ruling — the entry anchors the engine actually consumes are the
# #326 signed `pool_levels` above). So this assert is the guard that makes the deferral SAFE: the moment a
# real entrant lands in an unsigned cell, the build HALTS AND ASKS, instead of a future wiring silently
# reaching for a null or, worse, back-filling it with the declined number.
#
# THE POSITION KEY IS DECLARED, NOT ASSUMED. The cells were FIT on the derivation's day-0 position_group;
# this assert maps live entrants by the ENGINE's own settled future position gfut(p), which is the same field
# #326 requires for the rookie-draft positional key. The two conventions are verified to agree for the whole
# current pool population below (zero entrants map to an unsigned cell under EITHER), so the choice changes
# nothing today and is stated so a later seat can see which key was used and why.
#
# WHAT THE MEASUREMENT ACTUALLY FOUND, AND WHY THIS GUARD IS SHAPED THE WAY IT IS. PREREG P9 predicted
# "zero current entrants map to either cell, so the assert is silent on this board". THAT PREDICTION IS
# BREACHED, and it is breached by a LIVE PRICED ROW: `kalani-white` (type PDN, 2025, future position KPF,
# 0 career games) sits on the ACTIVE board at the pool slot and maps to PDN|KPF. Two further store rows map
# there too — `conrad-williams` (PDN|KPF, on the inactive `back` list) and `scott-reed` (PDS|KPF, on neither
# list). Under the derivation's own day-0 position key kalani-white STILL maps there, so this is not an
# artefact of which position field the mapping uses.
#
# THE GUARD IS THEREFORE SPLIT IN TWO, and neither half is weakened to let the build pass:
#   (1) THE HALT guards the HARM — being PRICED from an unsigned cell. Today no pricing leg reads pool_v0
#       at all (the consumption rewire is deferred by owner ruling; pool entrants are priced from the #326
#       signed `pool_levels`, where PDN and PDS are both SIGNED). So no price on this board comes from a
#       null, and the halt is stated as ARMED rather than as a gate that passed: it goes live in the same
#       commit that wires pool_v0 to a pricing site, and it names the wiring as its trigger.
#   (2) THE DISCLOSURE guards the FORGETTING. Every build prints the named list of rows standing in an
#       unsigned cell, loudly, so the condition cannot decay into a footnote between here and the rewire.
# HALTING THE WHOLE LANDING ON (2) WAS CONSIDERED AND REJECTED as a seat decision: it would block a curve
# the owner has ruled, over a condition that moves no price on this board. It is reported to the owner as
# an OWED DECISION instead — kalani-white needs either a priced answer or a signed PDN|KPF before pool_v0
# is ever consumed.
#
# ===== ORDER 29B — THE OWED DECISION ARRIVED, AND THIS GUARD IS REPLACED RATHER THAN REMOVED ===============
# OWNER RULING (#334 comment 5280881134), OPTION A: the two empty cells are SIGNED as BORROWED — the
# K-shrink limiting case, 100% borrow (pathway level x pool-wide KPF positional relativity). The values are
# PDN|KPF 92.35874340265629 and PDS|KPF 83.97715038537063, carried in the artifact with a per-cell
# `borrowed` disclosure and a `cell_signature` map, and they reproduce ORDER 29's own `declined_unsigned`
# 92.4 / 84.0 exactly — the ruling signed the arithmetic the derivation had already run and declined.
#
# WHY THE SHAPE OF THE GUARD CHANGES, STATED PLAINLY. Under ORDER 29 nothing read pool_v0, so declining a
# number cost nothing and the halt was ARMED-but-never-fired. ORDER 29B WIRES pool_v0 TO THE DAY-0 PRINT,
# so the trigger the old comment named ("it goes live in the same commit that wires pool_v0 to a pricing
# site") has arrived. An unsigned cell is now a MISSING PRICE, not a deferred question.
#   * THE UNSIGNED-CELL HALT RETIRES FOR CELLS SIGNED THIS WAY — there are no unsigned cells left, so a
#     halt keyed on `unsigned_cells` would be a guard that can never fire, which is worse than no guard.
#   * IT IS REPLACED BY A COVERAGE ASSERT, which is the thing that actually matters once the object is
#     consumed: EVERY pathway x position cell an entrant maps to must carry a SIGNED value — borrowed or
#     fitted. Stated over the WHOLE store pool population, not merely the active board, so a row that is
#     not priced today but is listed tomorrow cannot arrive at a null.
#   * `pool_v0_of()` REMAINS THE ONE ACCESSOR AND STILL RAISES on a null or a missing key, so the
#     fail-closed behaviour is intact for any cell a future derivation leaves unsigned. Its non-vacuity is
#     still PROVEN on a real row every build (below) rather than assumed — the proof now temporarily nulls
#     a populated cell and requires the raise, because with nothing unsigned there is no natural specimen.
_PV0=json.load(open('pvc_curve_v2.json')).get('pool_v0')
if _PV0:
    _PV0_UNSIGNED=set(_PV0.get('unsigned_cells') or [])
    _PV0_CELLS=_PV0.get('cells') or {}
    _PV0_SIG=_PV0.get('cell_signature') or {}
    _PV0_BORROWED=sorted(_PV0.get('borrowed_cells') or {})
    def _pool_v0_cell(p):
        """The printed pool day-0 cell an entrant maps to: '<pathway>|<position>'."""
        _d=pool_division(p)
        _path='ND>64' if _d=='ND65+' else _d.split(':')[0]
        return '%s|%s'%(_path,gfut(p))
    # ---- (1) THE HALT: no price may ever be READ from an unsigned cell. LIVE — pool_v0 is now CONSUMED.
    def pool_v0_of(p):
        """The printed pool day-0 v0 for an entrant, in BOARD currency (the numeraire s is already inside
        via the artifact's anchor_factor). ORDER 29B: this IS the pool entrant's printed day-0 price, read
        through this ONE accessor so the halt below cannot be bypassed by reading `cells` directly."""
        _c=_pool_v0_cell(p)
        _v=_PV0_CELLS.get(_c,'MISSING')
        if _v is None or _v=='MISSING':
            raise SystemExit(
                'ORDER 29 P9 HALT: %s maps to pool v0 cell %r, which is UNSIGNED (published null) or absent. '
                'ORDER 29B wires pool_v0 to the DAY-0 PRINT, so this is now a MISSING PRICE and not a '
                'deferred question. An entrant standing here must be priced by an OWNER DECISION — never by '
                'back-filling a declined number, never by silently taking the pathway level. HALT AND ASK.'
                %(p.get('player'),_c))
        return float(_v)
    # ---- (2) THE COVERAGE ASSERT, which is what replaces the unsigned-cell halt now the object is consumed.
    #      EVERY cell any pool row maps to must be signed. Wider than "active entrant" deliberately.
    _pv0_rows=[p for p in data if p.get('_pool')]
    # ACTIVE = membership of the shipped `players` list built at :1166-1174, which IS the board's own
    # population. (ORDER 29's disclosure keyed on p['_active']/p['active'], fields the store does not
    # carry, so it printed 0 active while kalani-white demonstrably stood on the 804-row board. Corrected
    # here rather than carried forward: a disclosure that under-reports is worse than none.)
    _pv0_players=set(map(id,players))
    _pv0_active=[p for p in _pv0_rows if id(p) in _pv0_players]
    _pv0_missing=[(p.get('player'),_pool_v0_cell(p)) for p in _pv0_rows
                  if _PV0_CELLS.get(_pool_v0_cell(p),None) is None]
    assert not _pv0_missing, (
        'ORDER 29B HALT (pool v0 coverage): %d pool row(s) map to a cell carrying no signed value — %s. '
        'pool_v0 is CONSUMED by the day-0 print, so an unsigned cell is a missing price. Sign it by owner '
        'ruling or halt; do not default it.'%(len(_pv0_missing),_pv0_missing[:6]))
    assert not _PV0_UNSIGNED, (
        'ORDER 29B HALT: the artifact still declares unsigned_cells %s while pool_v0 is CONSUMED by the '
        'day-0 print. Every cell must be signed (borrowed or fitted) before this object prices anyone.'
        %sorted(_PV0_UNSIGNED))
    # ---- (3) THE DISCLOSURE: named, loud, every build. The BORROW is never allowed to go quiet.
    _pv0_on_borrowed=[(p.get('player'),_pool_v0_cell(p),'ACTIVE' if id(p) in _pv0_players else 'inactive')
                      for p in _pv0_rows if _PV0_SIG.get(_pool_v0_cell(p))=='borrowed']
    # STDERR, deliberately: rl_export.py execs the engine under contextlib.redirect_stdout, so a stdout
    # print here is SWALLOWED and a "loud" guard would be silent in every build log. Measured, not assumed.
    __import__('sys').stderr.write(
          '#P9/29B POOL v0 IS CONSUMED (day-0 print). COVERAGE: %d of %d pool rows map to a SIGNED cell '
          '(%d of them on the shipped board). BORROWED CELLS %s — owner OPTION A, K-shrink limiting case; '
          '%d row(s) stand on a borrowed cell: %s. The halt in pool_v0_of() is LIVE, not armed.\n'
          %(len(_pv0_rows),len(_pv0_rows),len(_pv0_active),_PV0_BORROWED,len(_pv0_on_borrowed),
            (' · '.join('%s [%s, %s]'%t for t in _pv0_on_borrowed[:6]) or 'none')))
    # ---- NON-VACUITY, proven rather than asserted: the accessor must RETURN for a populated cell and must
    #      RAISE for an unsigned one. With nothing unsigned there is no natural specimen, so the raise is
    #      proven by TEMPORARILY nulling a real, heavily populated cell on the real code path and restoring
    #      it immediately. The guard is never trusted on silence.
    _p9_probe=[p for p in data if p.get('_pool') and _pool_v0_cell(p)=='RD|MID']
    assert _p9_probe and pool_v0_of(_p9_probe[0])>0, (
        'ORDER 29 P9 HALT: the pool v0 accessor did not return a value for the heavily populated RD|MID '
        'cell, so its behaviour on an unsigned cell proves nothing. The mapping is broken.')
    _p9_keep=_PV0_CELLS['RD|MID']
    try:
        _PV0_CELLS['RD|MID']=None
        try:
            pool_v0_of(_p9_probe[0]); _p9_fired=False
        except SystemExit:
            _p9_fired=True
    finally:
        _PV0_CELLS['RD|MID']=_p9_keep
    assert _p9_fired and pool_v0_of(_p9_probe[0])==float(_p9_keep), (
        'ORDER 29B HALT: the unsigned-cell guard did NOT fire on a deliberately nulled cell, or the cell '
        'was not restored. The guard is vacuous.')
    __import__('sys').stderr.write(
          '#P9 NON-VACUITY PROVEN ON A REAL ROW: the accessor returns %.1f for RD|MID (n=%d rows) and '
          'RAISES the moment that same cell is null. The guard is live, not silent.\n'
          %(pool_v0_of(_p9_probe[0]),len(_p9_probe)))
_MSD_CAVEAT=_PL_DOC['msd_completion_optimism_caveat']
print('#326 POOL LEVELS (N43 signed, read verbatim, LADDER currency; ND65+ = %.1f DERIVED, the cap against curve[%d]=%d REMOVED by owner ruling 2026-08-12 -> %d): %s'
      %(float(_PL_DOC['signed_nd65_plus']['measured_k15']),ND_CURVE_LAST,_PVC2M[ND_CURVE_LAST],_POOL_LEVELS['ND65+'],
        ' · '.join('%s %d%s'%(_k,_POOL_LEVELS[_k],' [MSD completion optimism %s]'%_MSD_CAVEAT if _k=='MSD' else '')
                   for _k in sorted(_POOL_LEVELS))))
print('#326 POOL POPULATION (engine classification, re-derived at build time): %s'
      %(' · '.join('%s %d'%(_k,_POOL_DIV_COUNT[_k]) for _k in sorted(_POOL_DIV_COUNT))))
SEASON_PROG=_season_val('calendar_progress',0.58)   # CALENDAR progress from data/season_state.json (dynamic; R14/24=0.58). Was the frozen literal 0.58.
def _playsig(g): return 1-math.exp(-g/6.0)    # saturating establishment from senior games
def debut_factor(p):                          # step-1 debut signal on pick-anchored value; asymmetric by pick
    ep=effpk(p); s=los(p); cg=sum(r['games'] for r in p['scoring'])
    elapsed=clamp((s-1)+SEASON_PROG,0.0,1.6)                  # seasons of opportunity so far (season-aware)
    ref=0.58*min(1.0,elapsed)                                 # expected establishment by now (low mid-yr1)
    sig=_playsig(cg)-ref
    Apos=(0.05+0.30*math.exp(-((ep-34)/24.0)**2))*clamp(ep/14.0,0.30,1.0)*clamp((22-cg)/22.0,0.0,1.0)  # positive: damped for high picks AND fades as a real sample accrues
    Aneg=0.16+0.12*math.exp(-((ep-34)/30.0)**2)              # negative: meaningful across the board
    return clamp(1+(Apos if sig>=0 else Aneg)*sig, 0.78, 1.28)
SLIP_CAP=0.78; SLIP_REF=150.0; SLIP_CONF=12.0; SLIP_MAXLOS=3   # step-2: position-aware DOWNSIDE slip, developing players, sample-confident
def track_slip(dlt,games):                    # dlt = avg pts vs the player's own position+experience bar (track_delta)
    if dlt is None or dlt>=0: return 1.0      # on/above bar -> no slip (upside stays in prior/production: no double-count)
    raw=clamp(1+dlt/SLIP_REF, SLIP_CAP, 1.0)
    conf=clamp(games/SLIP_CONF,0.0,1.0)       # small samples slip only partially (don't over-read a handful of games)
    return 1-conf*(1-raw)
def base_prod(g,k): return proj_from_peak(g, basepk(g,bandof(k)), 19, None, 'bal')   # baseline draftee, that position/pick
# --- v2.3 asymmetric output tilt: lift overperformers fully, drag underperformers GENTLY & sustained-scaled ---
TILT_REF=16.0
GAIN_UP=0.45; W_UP=55.0; UP_MAX=0.75; TILT_HI=1.22     # upside (output lifts: faster, fuller)
GAIN_DN=0.75; W_DN=70.0; DN_MAX=0.85; TILT_LO=0.55    # downside (gentler, slower)
NBAD_REF=2.0; SUS_MIN=0.35                             # sustained below-par scaler (years tracking behind)
def _fa(a,pa): return DELTAS[max(-8,min(14,int(round(a-pa))))]
def sustained_below(p,g,ep):
    n=0
    for s,(av,gm,yr) in srel(p).items():
        if av < expected_c(g,ep,s)-1.0: n+=1
    return n
def out_tilt(p,g,ep):
    ln=level_now(p)
    if ln is None: return 1.0
    sr=srel(p); cs=max(sr) if sr else max(1,los(p))       # current career season
    sig=ln-expected_c(g,ep,cs)                            # output vs the season-stage expected bar (dev curve)
    if sig>=0:
        conf=clamp(p['games']/W_UP,0,UP_MAX)
        t=1.0+GAIN_UP*sig/TILT_REF*conf
    else:
        sus=clamp(sustained_below(p,g,ep)/NBAD_REF,SUS_MIN,1.0)   # 1 half-season barely drags; 2+ yrs behind drags hard
        conf=clamp(p['games']/W_DN,0,DN_MAX)*sus
        t=1.0+GAIN_DN*sig/TILT_REF*conf
    return clamp(t,TILT_LO,TILT_HI)
P_HOOK=None                            # v3.4: when set, P_HOOK(p) supplies the establishment-probability weight on the pedigree track for NOT-yet-established players (replaces the seasons-only `decay`); established players keep `decay`.
PROD_GATE='off'                        # cont.20: rigid establishment blend REMOVED (was 'blenddemo'); v4 projection replaces it. ORIG note: 'blenddemo' = games-weighted rescue-only floor + 2/3 blend toward fully-gated. Modes: 'off' | 'full'/'fulldemo' (straight) | 'blend'/'blenddemo' (2/3). demo = floor at max(pedestal, games-weighted demonstrated value); plain = floor at pedestal.
def established(p):                     # v3.4 establishment definition: 50 career games + one >=11-game season
    cg=sum(r['games'] for r in p['scoring']); bg=max([r['games'] for r in p['scoring']],default=0)
    return cg>=50 and bg>=11
def grp3(p):
    _g=GRP.get(p['pos']); return 'RUCK' if _g=='RUCK' else ('KEY' if _g in('KPD','KPF') else 'GEN')
def _durable(p):
    ys=sorted(r['year'] for r in p['scoring'] if r['games']>=16)
    return any((y+1) in ys for y in ys)
def _recent_starter(p):
    g25=next((r['games'] for r in p['scoring'] if r['year']==2025),0)
    g26=next((r['games'] for r in p['scoring'] if r['year']==2026),0)
    return g25>=16 or g26>=9
def brodie_sig(p):                      # Brodie role-reliability cut (ported onto the board 2026-06-21, was compute.py-only):
    ln=level_now(p)                     # non-ruck, 5+ seasons, NOT a recent starter, NEVER durable, level>=80 -> value x0.5
    return (grp3(p)!='RUCK' and seasons(p)>=5 and not _durable(p) and not _recent_starter(p) and ln is not None and ln>=80)
def value(p,lens='bal'):
    _pd={'balanced':'bal'}.get(lens,lens)   # LEG E: the POSTURE production dial. 'balanced'->'bal' (the exact byte-exact path); 'contender'/'rebuilder' price the SAME streams at their own discount d (weight-don't-gate); 'bal'/'now'/'fut' unchanged. Pedigree pedestals (unpl_eq/pedestal) are NOT re-discounted — a posture re-weights production STREAMS, not the pick pedestal.
    ep=effpk(p); b=bandof(ep); decu=los_decay(p)
    unpl_eq=_PVC2M[min(ep,70)]*decu*debut_factor(p)   # JOB 2 (RL_PVC2): pickless unpl_eq reads the migrated curve; RL_PVC2=0 => _PVC2M is PVC => byte-exact
    if p.get('_unplayed') and (debut(p)>AGE_REF or p.get('_pedonly')): return round(unpl_eq)   # LEG E: pedigree-only prospect has no production stream to re-weight => posture-invariant (lens_tilt retired)
    g=gfut(p)   # settled future position drives pedigree/form-delta/out-tilt (matches peak_est); prod_floor stays present
    if level_now(p) is None:                                          # 0-game but IN opportunity window (debut season+): P applies continuously (prospect-path RETIRED 2026-06-18); genuine pre-debut prospects hit the _unplayed branch above and keep pure pedigree
        Pz = 1.0 if P_HOOK is None else P_HOOK(p)
        return round(unpl_eq * Pz)   # LEG E: pedigree/P only, no production stream => posture-invariant (lens_tilt retired)
    surv=1.0   # cont.20: survival() REMOVED from value path (v4 subsumes the bust-tracking haircut; verified 11.8pt separation vs survival's <=9%)
    Pz = None if P_HOOK is None else P_HOOK(p)                # v3.4: establishment-P, computed ONCE; gates BOTH the production term (below) and the pedigree pedestal (decay_eff), each carrying P exactly once
    prod_v=val(player_raw(p,_pd))*surv                        # LEG E: production priced at the posture dial (was hard-'bal'); balanced=='bal'=byte-exact
    relative=clamp((peak_est(p)/max(basepk_c_p(p,g,ep),40.0))**2.2, 0.40, 3.0)   # #336 AMENDMENT 2 — enumerated BPK consumer 5: the PEDIGREE PEDESTAL multiplier. His own peak against his class baseline; an established player is measured against establishers.
    # out_tilt CUT (cont.21): audited redundant with v4 — corr(out_tilt_sig, realised-v4)=-0.05, marginal R2=+0.001, coef after v4=-0.04. Same form double-count as the removed survival(). relative stays at the v4 pedigree multiplier.
    if g in('RUCK','KPF','KPD') and age(p)<=22 and relative<1.0:   # v3.4 relative-floor: young key-pos debut can't drag the pedestal below the clean pick baseline; YEAR-SCALED (more chances seen -> less lift)
        _sc={1:1.0,2:0.8,3:0.5,4:0.2}.get(2026-p['year'],0.0); relative=relative+_sc*(1.0-relative)
    decay=max(0.0,1-(seasons(p)-1)/4.5)
    decay_eff = decay if Pz is None else min(decay, Pz)   # v3.4: establishment-P only ever PULLS DOWN (min) on the pedigree track; established players P=1 -> min=decay, untouched
    pedestal = _PVC2M[min(ep,70)]*relative*surv*decay_eff   # JOB 3 (RL_PVC2): pedigree pedestal reads the migrated curve; RL_PVC2=0 => _PVC2M is PVC => byte-exact
    pf = prod_floor(p,_pd)                                # LEG E: demonstrated-floor at the posture dial (balanced=='bal'=byte-exact)
    prod_full = max(prod_v, pf)                           # full production estimate: projection OR demonstrated-level floor, whichever is higher
    if Pz is not None and PROD_GATE!='off':                # v3.4 PRODUCTION-GATING. fully_gated = P*production + (1-P)*floor. floor = pedestal ('full'/'blend') OR a games-weighted demonstrated floor ('fulldemo'/'blenddemo') so survivors who banked games aren't stripped to the bare pick. 'full*'=straight; 'blend*'=Luke's 2/3 toward fully-gated.
        if PROD_GATE in ('fulldemo','blenddemo'):
            cred = min(1.0, p['games']/50.0); gfloor = max(pedestal, cred*pf + (1.0-cred)*pedestal)   # rescue-only: never below the pick's pedestal
        else:
            gfloor = pedestal
        fully_gated = Pz*prod_full + (1.0-Pz)*gfloor
        if PROD_GATE in ('full','fulldemo'):     prod_full = fully_gated
        elif PROD_GATE in ('blend','blenddemo'): prod_full = (1.0/3.0)*prod_full + (2.0/3.0)*fully_gated
    res=max(prod_full, pedestal)
    if brodie_sig(p): res*=0.5                            # Brodie role-reliability cut (now on the board; flows to convex/backward via value())
    return round(res)                                     # LEG E: lens_tilt (interim no-improvement tilt) RETIRED; value() weights via the posture dial above, never tilts
# ---- PICK-EQUIVALENT for the no-slot entry mechanisms (MSD/SSP/Ireland/Unregistered/post-draft) ----
# "What national pick is an X player worth?" Build a national realised-career-value curve (no effpk
# dependence, same risk-averse pooling as the PVC), then invert it against each mechanism's pooled value.
def realized_cv(p):   # LEGACY helper, retained ONLY for rl_export's father-son/academy/next-gen overshoot panel
    pk=pkbest(p)
    if pk is None: return 0.0
    _g=GRP[p['pos']]; return float(val(proj_from_peak(_g,pk,PEAK_AGE[_g],pk,'bal')))
_natcv=[None]*100     # LEGACY national curve, retained for the export panel above; the PATHWAY board now uses _natcv34
for _k in range(1,100):
    # ADDENDUM 1: `_grp=='ND'` is NOT sufficient any more — a national selection at 65+ is POOL, and this site
    # windows on the RAW pick, so ND picks 65-68 would still land inside +/-4 of picks 61-64. Gate on is_pool.
    _vs=[realized_cv(p) for p in _curve_sample('_natcv',_k,                         # ADDENDUM 1: registered sample
        [p for p in data if p['_grp']=='ND' and not is_pool(p) and (p['pick'] or 99) and abs((p['pick'] or 99)-_k)<=4 and p['pos'] in GRP])]
    if _vs: _natcv[_k]=_ce(_vs,ALPHA)
for _k in range(1,100):
    if _natcv[_k] is None: _natcv[_k]=_natcv[_k-1] if _k>1 and _natcv[_k-1] else 300.0
_natcv34=[None]*100   # v3.4 (Luke cont.12): pathways measured backward THE SAME WAY as picks -- _nv_bwd (posval-VOR
for _k in range(1,100):   # on best2, busts->0) + tiered alpha, inverted against the v3.4 per-pick national curve (NOT legacy realized_cv).
    _vs=[_nv_bwd(p) for p in _curve_sample('_natcv34',_k,                           # ADDENDUM 1: pool rows do not teach the curve;
        [p for p in hist if _teaches_curve(p) and abs(_epk(p)-_k)<=4])]              # registered so the check watches THIS list
    if _vs: _natcv34[_k]=_ce(_vs,_alpha_pvc(_k))
for _k in range(1,100):
    if _natcv34[_k] is None: _natcv34[_k]=_natcv34[_k-1] if _k>1 and _natcv34[_k-1] else _natcv34[1]
for _k in range(2,100):   # enforce non-increasing: a deeper pick can't realise MORE than a shallower one. The raw
    if _natcv34[_k]>_natcv34[_k-1]: _natcv34[_k]=_natcv34[_k-1]   # tail oscillates on tiny samples, which makes the inversion ill-conditioned; cumulative-min cleans it.
def _pick_equiv(v):
    best=99; bd=1e18
    for _k in range(1,100):
        if _natcv34[_k] is not None and abs(_natcv34[_k]-v)<bd: bd=abs(_natcv34[_k]-v); best=_k
    return best
PATH_LO=2003; PATH_ALPHA=PVC_ALPHA_HI       # same lower bound as the pick curve; pathways land in the cheap tail -> tail alpha (=0.8)
PICKEQ={}; MECH_STATS={}
_MECH_NAME={'MSD':'Mid-Season','SSP':'SSP / pre-season supp.','IRE':'Ireland','UNR':'Unregistered',
            'PDA':'Post-draft Academy','PDN':'Post-draft Next-Gen','PDS':'Post-draft Scholarship'}
for _t in PICKLESS:
    _all=[p for p in data if p['type']==_t and p['pos'] in GRP and _cycle_year(p)>=PATH_LO]
    if not _all: continue
    _best=None                               # per-pathway MOST-FAVOURABLE upper cutoff (>=2021; later if it raises pooled value)
    for _cut in range(2021,2027):
        _coh=[p for p in _all if _cycle_year(p)<=_cut]
        if len(_coh)<8: continue
        _pl=_ce([_nv_bwd(p) for p in _coh],PATH_ALPHA)
        if _best is None or _pl>_best[0]: _best=(_pl,_cut,_coh)
    if _best is None:                        # tiny pathway -> full cohort
        _coh=_all; _pl=_ce([_nv_bwd(p) for p in _coh],PATH_ALPHA); _cut=max(_cycle_year(p) for p in _coh)
    else: _pl,_cut,_coh=_best
    eq=_pick_equiv(_pl); PICKEQ[_t]=eq
    played=[p for p in _coh if pkbest(p) is not None]
    MECH_STATS[_t]={'name':_MECH_NAME.get(_t,_t),'n':len(_coh),'played_n':len(played),'cutoff':_cut,
        'hit_rate':round(100*len(played)/len(_coh),1),
        'pooled_value':round(_pl),'pick_equiv':eq,
        'mean_career_avg':round(float(np.mean([pkbest(p) for p in played])),1) if played else None,
        'mean_career_games':round(float(np.mean([p['games'] for p in _coh])),1)}
# THE SPLIT: the mechanism PICK-EQUIVALENT no longer anchors these players. It mapped each pickless pathway's
# pooled value onto the 1-99 ladder (SSP 92, MSD 90 — both past 64), which is precisely the old model: a pickless
# entrant priced off a pick number. Pickless mechanisms are POOL, set to POOL_PICK in the classification loop
# above, and differentiated by POSITION through iso_corr — not by a pseudo-pick.
# PICKEQ / MECH_STATS are still COMPUTED, because the pooled-value and hit-rate columns they carry are a
# measurement surface the UI reads; but 'pick_equiv' is dropped from MECH_STATS so no consumer can render a
# pick number above 64 as a price. Nothing assigns _eff from PICKEQ any more.
for p in data+extra:
    if p['type'] in PICKEQ: p['_eff']=POOL_PICK; p['_pool']=True
for _ms in MECH_STATS.values(): _ms.pop('pick_equiv',None)
print('PICKLESS MECHANISMS -> POOL (index %d); pooled values:'%POOL_PICK,
      { _MECH_NAME.get(k,k):MECH_STATS[k]['pooled_value'] for k in sorted(PICKEQ) })

# ==== ESTABLISHMENT-P (ported from compute.py 2026-06-21 -> SINGLE SOURCE OF TRUTH; the BOARD now applies it).
# The consuming machinery (PROD_GATE + the min(decay,Pz) line in value()) was already here but inert with P_HOOK=None.
# P personalises bust risk: a not-yet-established player's pedigree track + production are weighted by P(establish).
# Built on REAL types (runs BEFORE the present-identity overrides below, exactly as compute.py did). ====
pgrid.build(data, GRP, debut)           # build the establishment surface from THIS engine's data (no rl_model import inside pgrid)
def entry_age(p): return (debut(p)-1)-by(p)
_PB=[(1,3),(4,6),(7,9),(10,13),(14,18),(19,24),(25,31),(32,39),(40,48),(49,58),(59,99)]
_cohP=[p for p in data if p.get('_grp') in('ND','RD') and debut(p)<=2019 and p['pos'] in GRP]
def _brateP(lo,hi):
    _gg=[p for p in _cohP if lo<=effpk(p)<=hi]
    return (sum(established(p) for p in _gg)/len(_gg), len(_gg)) if _gg else (0.0,0)
_brawP=[_brateP(lo,hi) for lo,hi in _PB]
def _pavaP(vals,wts):                    # weighted isotonic (monotone non-increasing establishment rate by pick)
    b=[[vals[i]*wts[i],wts[i],i,i] for i in range(len(vals))]; i=0
    while i<len(b)-1:
        if b[i][0]/b[i][1] < b[i+1][0]/b[i+1][1]-1e-9:
            b[i][0]+=b[i+1][0]; b[i][1]+=b[i+1][1]; b[i][3]=b[i+1][3]; del b[i+1]; i=max(0,i-1)
        else: i+=1
    f=[0.0]*len(vals)
    for blk in b:
        for k in range(blk[2],blk[3]+1): f[k]=blk[0]/blk[1]
    return f
_pfitP=_pavaP([r for r,_ in _brawP],[max(1,n) for _,n in _brawP]); _pctrP=[(lo+hi)/2.0 for lo,hi in _PB]
def _pick_curveP(ep):                    # smooth monotone-interpolated establishment rate at this pick (no band cliffs)
    if ep<=_pctrP[0]: return _pfitP[0]
    if ep>=_pctrP[-1]: return _pfitP[-1]
    for i in range(len(_pctrP)-1):
        if _pctrP[i]<=ep<=_pctrP[i+1]:
            t=(ep-_pctrP[i])/(_pctrP[i+1]-_pctrP[i]); return _pfitP[i]+t*(_pfitP[i+1]-_pfitP[i])
    return _pfitP[-1]
_ovP=sum(established(p) for p in _cohP)/len(_cohP); _grpoffP={}     # position offset = group est rate / overall (capped)
for _gv in set(GRP.values()):
    _gg=[p for p in _cohP if gfut(p)==_gv] # ITEM 271 item 4 GROUP B: built AND applied on the played axis (gfut). Both sides move together; moving either alone leaves the sibling mismatch.
    _grpoffP[_gv]=(sum(established(p) for p in _gg)/len(_gg))/_ovP if _gg else 1.0
def pick_prior(p): return float(np.clip(_pick_curveP(effpk(p))*_grpoffP.get(gfut(p),1.0),0.05,0.97)) # ITEM 271 item 4 GROUP B: built AND applied on the played axis (gfut). Both sides move together; moving either alone leaves the sibling mismatch.
_PATHK=12; _pfloorP=_pfitP[-1]; _pathpr={}                          # each pathway its own pool, shrunk to the late-pick floor when thin
for _t in ['MSD','SSP','IRE','UNR','PDA','PDN','PDS']:
    _gp=[p for p in data if p.get('type')==_t and debut(p)<=2022 and p['pos'] in GRP]
    if _gp:
        _r=sum(established(p) for p in _gp)/len(_gp); _w=len(_gp)/(len(_gp)+_PATHK); _pathpr[_t]=_w*_r+(1-_w)*_pfloorP
def P_estab(p):
    if established(p): return 1.0
    g3=grp3(p); Y=2026-debut(p)+1; d=debut(p)            # CLOCK FIX: Y = season ordinal (1=debut season)
    def _gm(r): return r['games']   # MSD debut-season game boost SCRUBBED 2026-07-05 (was x2.0 half-season standardisation)
    Gn=sum(_gm(r) for r in p['scoring'] if d<=r['year']<2026)+(sum(r['games'] for r in p['scoring'] if r['year']==2026)/SEASON_PROG)
    base=pgrid.Praw(g3,Y,Gn)*pgrid.mat_mult(entry_age(p),Gn)         # smoothed surface x mature-entry discount
    prior=_pathpr[p['type']] if p['type'] in _pathpr else pick_prior(p)
    base=base+(1-SEASON_PROG)*max(0.0,prior-base)        # mid-season benefit-of-doubt toward the pick/pathway prior
    return float(np.clip(base,0.10,0.99))
P_HOOK=None                            # cont.20: establishment-P gating DEACTIVATED (xP_establish deleted); v4 projection replaces it. (was: P_HOOK=P_estab)

# ---- PRESENT-IDENTITY OVERRIDES (Luke ground-truth, 2026-06-18): value each player's CURRENT self as a fresh
# entry via the named window. DB history is untouched -- real type/year drove every cohort/pool surface, built
# ABOVE this line; only these players' pedigree anchor + entry clock + pathway reset. SINGLE SOURCE OF TRUTH here
# so the EXPORTED BOARD inherits it (this previously lived only in compute.py, so the shipped board never applied
# it -> Keane/McAndrew anchored on raw IRE/MSD; Perez/Hall-Kahan kept their raw entry clock). Forward = SSP fix.
PRESENT_ID_OVERRIDES={
    "Flynn Perez":    ('SSP', 2025),   # 2025 SSP window
    "Hugo Hall-Kahan":('MSD', 2026),   # 2026 mid-season draft
    "Lachlan McAndrew":('SSP', 2024),  # 2024 SSP window
    "Mark Keane":     ('SSP', 2022),   # 2022 SSP window
}
_L5_PICKLESS=os.environ.get('RL_L5_PICKLESS','1')!='0'   # v2.9 L5: complete the SSP re-entry switch — SSP is pickless by convention (register item 17 ii). Default ON; RL_L5_PICKLESS=0 ⇒ retained pick capital ⇒ base.
for _p in data:
    _o=PRESENT_ID_OVERRIDES.get(_p.get('player'))
    if _o:
        # THE SPLIT: these four re-enter through a pickless pathway (SSP/MSD), so they are POOL. Was the PICKEQ
        # pedestal (_eff=92 for SSP, 90 for MSD) — pick indices past 64, i.e. the old model.
        _p['type'],_p['year']=_o; _p['_grp']=_o[0]; _p['_eff']=POOL_PICK; _p['_pool']=True
        if _L5_PICKLESS and _o[0]=='SSP': _p['pick']=None; _p['_pickless']=True   # drop retained pick capital (Perez 35 / McAndrew 12; Keane already None). The pedestal is now the pool index, not 92.

# AVAILABILITY PRESENT HAIRCUT (present component, Now board only). The k=0 present-year level is scaled by
# (1 - _avail_hc). The SOURCE of _avail_hc is the LTI REGISTER (Chapter-3 2026-07-09, RL_AVAIL layer set in
# _merged_recover.py): _avail_hc = L_p = lost-season fraction for register out-for-remainder names. Here we
# only INITIALISE the field to 0.0 (no haircut) for every player; the register layer sets it for its names.
#
# OBITUARY — `_b2hc` RETIRED (R-B2HC=RETIRE, DECISIONS §33; SSI delete-don't-disable). The old transient,
# age-banded INFERENCE (established >=3 seasons, recent peak>=90, 0 games in 2026, season >1/3 done ->
# <27:8.8% / 27-29:3.9% / 30+:0) is DELETED. Its own docstring said "next build's return data supersedes it"
# — this is that build. A curated register + an inference stopgap firing on the same 0-games-2026 signal is a
# double-count; the register beats inference (Luke's word over a heuristic). The k=0 haircut PLUMBING is kept
# and re-pointed to the register-driven _avail_hc (proj_from_peak :328/:408, prod_floor, _proj_w4, rl_export,
# distribution_pricing). `_b2hc` was a runtime-only field (never in the store) -> store md5 UNCHANGED, no
# re-seal. Measured pre-strip: exactly {nicholas-martin, tom-green} carried _b2hc>0, BOTH register names, so
# the strip moves only register names (non-mover parity holds). Full obituary: BOARD_LAYERS_OBITUARY.md.
for _p in data+extra: _p['_avail_hc']=0.0
_pe_clear()   # FIX (cont.22): SCALE@436 memoised peak_est while pickless players still held the placeholder _eff (pick-equivalent isn't applied until L726). Clearing here, after all attributes are finalised and before the board build, makes pickless players price on their real pick-equivalent instead of the stale placeholder (e.g. Sharman 1147->303).
for p in players: p['_vpt']=value(p,'bal'); p['_v']=p['_vpt']   # _vpt = point value (GH integrand basis + JS live-recompute target); _v reset to convex below
players.sort(key=lambda p:-p['_v'])
# --- Phase-2 variance layer: E[value] over the projected level distribution x survival ---
# Calibrated from the back-test: level CoV ~0.23 young / ~0.18 vet (per 2yr); 2yr survival ~0.94 proven
# down to ~0.80 for low-evidence older players. At offset 0: sigma=0, survival=1 -> proj_value==value -> vP0==v.
_GHx=[-2.0201829,-0.9585725,0.0,0.9585725,2.0201829]; _GHw=[0.0199532,0.3936193,0.9453087,0.3936193,0.0199532]
_SQ2PI=math.sqrt(2.0); _SQPI=math.sqrt(math.pi)
def _cov_age(a): return 0.23 if a<=24 else 0.18
def _cov(p): return _cov_age(_age_at(p,BASE_REF)) + 0.12*clamp((90-p['games'])/90.0,0,1)  # thin sample -> wider level spread
def _upside_w(p): return clamp((31-_age_at(p,BASE_REF))/12.0,0.0,1.0)                 # convexity = upside option; applies pre/near-peak, fades to 0 by ~33
def _cliff_disc(p,off):                                                               # prices the cliff for OLD + LOW-evidence only (proven players ~untouched)
    a=_age_at(p,BASE_REF); g=p['games']
    return 1.0 - 0.42*clamp((a-28)/7.0,0,1)*clamp((150-g)/150.0,0,1)*(off/2.0)
PRESENT_VAR=0.25      # present-level sampling-uncertainty variance -> option value priced INTO present value (0.0 = old point value). SHIPPED 0.25: present is more certain than the 0.5 forward dispersion; see HANDOVER conservation note.
CVX_CAP=1.25          # cap on the present convexity multiplier (guards the value-floor threshold artifact for fringe straddlers)
def proj_value(p,off):
    global _LEVEL_OVR
    mu=_dev_advance(level_demo(p),p)
    if mu is None: return value(p,'bal')
    pt=value(p,'bal')
    var = PRESENT_VAR if off==0 else off/2.0          # off=0 carries present sampling uncertainty (option value); off>=1 = forward dispersion (unchanged)
    s=_cov(p)*math.sqrt(var)*_upside_w(p)*mu          # upside dispersion (convexity), gated to pre-peak + evidence
    if s<1e-6: base=value(p,'bal')
    else:
        Ev=0.0
        for x,w in zip(_GHx,_GHw):
            _LEVEL_OVR=max(1.0, mu+_SQ2PI*s*x); Ev+=w*value(p,'bal')                   # Gauss-Hermite E[value | level~N(mu,s)]
        _LEVEL_OVR=None; base=Ev/_SQPI
    if off==0 and pt>0: base=clamp(base, pt, pt*CVX_CAP)    # present option value: additive only (floor pt, cap pt*CVX_CAP); no cliff at off=0
    r=round(_cliff_disc(p,off)*base)                                                  # x cliff discount (old+uncertain only)
    if off==0 and pt>0: r=max(r, round(pt))                # FLOOR present value at the point: guards cliff/rounding from pushing cvx (=v/vpt) below 1.0 (premium is additive-only)
    return r
for off,key in ((0,'_vP0'),(1,'_vP1'),(2,'_vP2')):
    AGE_REF=BASE_REF+off
    for p in players: p[key]=proj_value(p,off)
AGE_REF=BASE_REF
# Present value now PRICES CONVEXITY (option value): _v = proj_value(0) = E[value | present-level uncertainty], capped. vP0==v by construction.
for p in players:
    p['_v']=p['_vP0']
    p['_cvx']=min(round(p['_v']/p['_vpt'],6), CVX_CAP) if p['_vpt']>0 else 1.0   # convexity multiplier in [1.0, CVX_CAP]; min() honours the documented cap (round(v)/round(vpt) could otherwise edge past it at low values)
players.sort(key=lambda p:-p['_v'])
import numpy as _np
_prem=[(p['_cvx']-1) for p in players if not p.get('_unplayed') and p['_vpt']>0]
_poolpt=sum(p['_vpt'] for p in players); _poolcx=sum(p['_v'] for p in players)
print('Phase-2 CONVEXITY into present value: pool +%.1f%%  median premium +%.1f%%  max +%.0f%% (cap %.0f%%)  | vP0==v by construction'
      %(100*(_poolcx/_poolpt-1),100*_np.median(_prem),100*max(_prem),100*(CVX_CAP-1)))
# --- Phase-2 BACKWARD board (vM1/vM2): re-value on KNOWN truncated data, NOT a projection. ---
# "Board as of end-(2026-N) season": value every player who was ON AN AFL LIST at end of year Y=2026-N, using
# data through Y only, de-aged to Y (BASE_REF=AGE_REF=Y so dev_advance no-ops -> pure value(), no leakage). The
# population INCLUDES players who have since retired -- the DB carries retired records (incl. the 2024/2025 leavers
# Luke folded in); they are recalled onto the -N board for the years they were active (collected in `back_extra`,
# exported as board-history-only rows that never appear on the Now/forward board). Frozen 2026 SCALE/PVC.
import copy as _copy
def _trunc_p(p, upto):
    q=_copy.deepcopy(p); q['scoring']=[r for r in p['scoring'] if r['year']<=upto]
    q['games']=sum(r['games'] for r in q['scoring']); return q
def _lastgameyr(p):
    ys=[r['year'] for r in p['scoring'] if r['games']>=1]; return max(ys) if ys else None
def _on_board(p, N):                                    # on an AFL list at end of year Y=2026-N?
    Y=2026-N
    if debut(p)>Y: return False                         # not yet debuted by end of year Y. ND/RD/SSP debut=year+1 (=> year>Y-1, unchanged); MSD is mid-season (debut=year) so it now sits on its OWN entry-year board (mirrors the Now board carrying the current-year MSD class)
    ll=p.get('_last_listed')
    if ll is not None: return p['year']<=Y and ll>=Y     # Luke ground-truth delisting year (overrides the games proxy both ways)
    ly=_lastgameyr(p)
    return (debut(p)<=Y<=debut(p)+1) if ly is None else (ly>=Y)    # unplayed prospect: ONLY within its initial-contract window (matches section-c {entry+1,+2}); fixes long-retired/no-scoring players (Watson/Maibaum/Mohr) being recalled onto every prior board. Played: still active through Y.
def _backval(p, N):
    global BASE_REF, AGE_REF
    if not _on_board(p, N): return None
    Y=2026-N; BASE_REF=AGE_REF=Y
    try: return proj_value(_trunc_p(p, Y), 0)             # convex (option value) at the year-Y snapshot, same as Now -> consistent lens across the slider
    finally: BASE_REF=AGE_REF=2026
for p in players:                                       # (a) active players: vM stored on their record
    p['_vM1']=_backval(p,1); p['_vM2']=_backval(p,2)
_act_keys=set(_dkey(p) for p in players); _rb={}        # (b) retired OR delisted-not-retired players active in 2024/2025: dedup + recall
for p in data:
    _delisted = p.get('_last_listed') is not None and p['_last_listed']<2026
    _valuable = (p['_grp'] in ('ND','RD')) or any(r['games']>=1 for r in p['scoring'])  # pedigree anchor or demonstrated form (else unvalued, same as Now)
    if not (p.get('_retired') or (_delisted and _valuable)) or p['pos'] not in GRP: continue
    k=_dkey(p)
    if k in _act_keys: continue
    if k not in _rb or _rich(p)>_rich(_rb[k]): _rb[k]=p
back_extra=[]
for k,p in _rb.items():
    vM1=_backval(p,1); vM2=_backval(p,2)
    if vM1 is None and vM2 is None: continue            # retired before 2024 -> on neither back-board
    p['_vM1']=vM1; p['_vM2']=vM2; p['_backonly']=True; p['_v']=None; back_extra.append(p)
# (c) unplayed ND/RD prospects: carry on the BACKWARD boards across the entry+1/entry+2 window (mirror of the
#     year>=2024 Now-shell), so -2 values the 2023 class the same way Now/-1 value the 2025/2024 classes. Bounded to
#     (board_year - entry) in {1,2}, so a prospect appears only within its initial-contract window and never leaks onto
#     Now (entry+3 = 3-yrs-no-games bust cutoff). Board-history-only rows (no _v) -> the active pool is unchanged.
_pool_keys=set(_dkey(q) for q in players)|set(_rb.keys())
for p in data:
    if p['pos'] not in GRP or p['_grp'] not in ('ND','RD'): continue
    if any(r['games']>=1 for r in p['scoring']): continue          # unplayed prospects only (played-then-cut handled by the recall loop above)
    if _dkey(p) in _pool_keys: continue
    e=p['year']
    vM1=_backval(p,1) if (2025-e) in (1,2) else None               # board -1 (Y=2025): 2023/2024 entries
    vM2=_backval(p,2) if (2024-e) in (1,2) else None               # board -2 (Y=2024): 2022/2023 entries
    if vM1 is None and vM2 is None: continue
    p['_vM1']=vM1; p['_vM2']=vM2; p['_backonly']=True; p['_v']=None; back_extra.append(p)
_nM1=sum(1 for q in players+back_extra if q.get('_vM1') is not None)
_nM2=sum(1 for q in players+back_extra if q.get('_vM2') is not None)
print('Phase-2 backward board: on-board -1=%d, -2=%d (active %d + retired-recalled %d)'%(_nM1,_nM2,len(players),len(back_extra)))
# --- backward-board CONSERVATION NORMALISATION (Luke; re-ported from rl_build) ---
# The raw backward board inflates (-1 ~1.12x, -2 ~1.22x): going back, every player is younger w/ more runway and the
# diluting intakes are gone. Scale each -N board by (now-total / back-total) over the SHARED active set so the board is
# conserved (-N ~1.00x) and a good player no longer shows a uniformly higher rating one year back. Recalled retirees
# (no _v) ride the same factor. Forward board stays raw/melting (not flagged); symmetrise on request.
for _key in ('_vM1','_vM2'):
    _shared=[q for q in players if q.get(_key) is not None and q.get('_v')]
    _bt=sum(q[_key] for q in _shared)
    _f=(sum(q['_v'] for q in _shared)/_bt) if _bt>0 else 1.0
    for q in players+back_extra:
        if q.get(_key) is not None: q[_key]=int(round(q[_key]*_f))
    print('  %s conservation factor x%.4f (raw board was x%.3f)'%(_key,_f,1.0/_f if _f else 0))
# --- AGE_REF seam (for the Phase-2 forward-board pass) ---
# The age clock (age/seasons/los) reads the module global AGE_REF (default 2026). To re-age the whole
# board to a shifted year, set AGE_REF and recompute value() per player, e.g.:
#     def values_at(off):
#         global AGE_REF; AGE_REF=2026+off
#         try: return [value(p,'bal') for p in players]
#         finally: AGE_REF=2026
# Calibration (PVC/SCALE/dev curve/cohort) stays fixed; only each player's age advances; demonstrated
# form (srel/recency) is unchanged. NOTE (verified this session): a pure clock-advance with NO projected
# development INVERTS the dynasty ranking (young pedigree assets crater as decay=1-(seasons-1)/4.5 fades
# their pick value with nothing to replace it; established older players rise). The forward board is only
# meaningful once Phase 2 projects development to offset that fade -> build the two together.
def pe(v):
    if v>PVC[1]: return '1+'
    for k in range(1,51):
        if PVC[k]<=v: return str(k)
    return '50+'
def rk(nm):
    cs=sorted([p for p in players if norm(nm) in norm(p['player']) and (p.get('_has26') or p['year']>=2023 or p.get('_unplayed'))],key=lambda p:-p['_v'])
    if not cs: cs=sorted([p for p in players if norm(nm) in norm(p['player'])],key=lambda p:-p['_v'])
    if not cs: return '%-20s NF'%nm
    p=cs[0]; return '%-20s #%-3d val%4d ~pk%-3s %-7s pk%2d %-3s'%(p['player'][:20],players.index(p)+1,p['_v'],pe(p['_v']),GRP[p['pos']],p['pick'],p['type'])
print('PVC:',{k:PVC[k] for k in [1,3,5,10,15,20,30,45]})
print('TOP 15:')
for i,p in enumerate(players[:15],1): print('  %2d. %-22s %-7s val%4d ~pk%s'%(i,p['player'][:22],GRP[p['pos']],p['_v'],pe(p['_v'])))
print('--- recent draftees (should be ~>= their pick if producing; played>unplayed) ---')
for nm in ['Sullivan Robey','Sam Cumming','Jacob Farrow','Cooper Duff-Tytler','Harry Dean','Zeke Uwland','Dylan Patterson','Harry Kyle','Connor O\'Sullivan']: print('  '+rk(nm))
print('--- KPD check (established vs young) + anchors ---')
for nm in ['Josh Worrell','Sam Collins','Willem Duursma','Nick Daicos','Dayne Zorko','Finn Callaghan','Harry Sheezel']: print('  '+rk(nm))
