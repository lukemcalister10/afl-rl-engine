#!/usr/bin/env python3
"""ORDER 26B -- STEP 3, LAYER 2: THE VALUATION LAYER (Ruling 11).

    "Layer 2 = valuation (ALL knobs in one config block: bars path, drop, games weights,
     disc_factor, window tiers), recomputable from Layer 1 in seconds."

AUTHORITY TO RUN: #334 comment 5270492281 -- OWNER RULING "Core, resume". The identity gate is ruled
SATISFIED AT THE PRICING CORE (the step-1 leg proved the scorer bit-exact against the engine's own
price6 on 804/804 active rows -- stronger than the +/-2% bar). The four adjustment legs measured in
GATE_REPORT.md §5 (_uncomp_prod, the pedigree-pole blend, ev/raw_ev, the L7 numeraire) are player-STATE
machinery, out of the scorer's scope, deferred whole to the consumption-rewire act.

WHAT THIS FILE IS
-----------------
The gate leg proved ONE season term. This file formalises that term into a career scorer with EVERY
knob in the CFG block below, and scores EVERY career in Layer 1 -- 2,650 of them -- under the window
tiers of Ruling 8.

    INPUT   data/delivered_value/layer1_player_seasons.json   (md5 ad1229ea..., assumption-free)
    OUTPUT  LAYER2.json  LAYER2_out.txt

READ-ONLY.  Engine is loaded from a staged copy; pins asserted at entry and at exit.

  usage:  python3 o26b_layer2.py
"""
import os, sys, io, json, math, contextlib, hashlib, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
# PID-UNIQUE STAGING. The scratchpad path below is session-specific and is baked into this committed
# file, so a SECOND seat that checks this branch out and runs this harness stages the engine into the
# SAME directory -- and each run begins with an rmtree of it. Two concurrent runs therefore delete
# each other's staged engine mid-boot. Observed live on 2026-08-13 with another seat running these
# scripts off the pushed branch. The staging directory is now per-process and is cleaned up on exit.
_STAGE_ROOT = SP + '/eng26b_l2_%d' % os.getpid()
STAGE = _STAGE_ROOT + '/rl_after'
L1P = os.path.join(ROOT, 'data', 'delivered_value', 'layer1_player_seasons.json')
L1_MD5 = 'ad1229ea6f443538479447132382b21c'

PINS = {'store':  ('engine/rl_after/rl_model_data.json',       'd9a24282357cf3083b1640466e3ecd83'),
        'board':  ('engine/rl_after/rl_app_data.json',         '88ce647f531030d8d2e094188b258191'),
        'engine': ('engine/rl_after/_merged_recover.py',       '3f1468e5468462ab789e49aace264c90'),
        'model':  ('engine/rl_after/rl_model.py',              'e5eb5e4405c09eebef45a9db89f014bc'),
        'netting':('engine/forward_valuation/dist_redesign.py','48ea1bfeccc6d1ea51add66b0cb93965')}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s %s != %s (%s)" % (k, _md5(os.path.join(ROOT, rel)), exp, rel)
           for k, (rel, exp) in PINS.items() if _md5(os.path.join(ROOT, rel)) != exp]
    if _md5(L1P) != L1_MD5:
        bad.append("layer1 %s != %s" % (_md5(L1P), L1_MD5))
    if bad: raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')
shutil.rmtree(_STAGE_ROOT, ignore_errors=True)
import atexit
atexit.register(lambda: shutil.rmtree(_STAGE_ROOT, ignore_errors=True))
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(os.path.join(ROOT, 'LTI_REGISTER.md'), STAGE)
# THREAD PINNING. The harness pinned OPENBLAS_NUM_THREADS only. Measured 2026-08-13 on a contended
# box (4 cores, load 24 from other seats): the engine boot burned >14 min of CPU and never finished,
# with the process holding 4 threads and doing no I/O -- BLAS worker threads SPIN-WAITING while
# oversubscribed. Pinning every threading backend to 1 makes the boot single-threaded and immune to
# it. Determinism is unaffected (the engine's own fsum paths are order-fixed by design); this only
# removes a source of wall-clock and CPU waste. Set BEFORE numpy is imported by the engine exec.
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1',
                  OMP_NUM_THREADS='1', MKL_NUM_THREADS='1', NUMEXPR_NUM_THREADS='1',
                  VECLIB_MAXIMUM_THREADS='1')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; cp = G['cp']; dp = G['dp']; rd = G['rd']; b6 = G['b6']
price6 = G['price6']; WQ6 = G['WQ6']; _det_dot = G['_det_dot']

# ==================================================================================================
# THE ONE CONFIG BLOCK -- RULING 11's "ALL knobs in one place".  Nothing below this block invents a
# number; every constant here is either READ LIVE off the engine or is an owner ruling stated by name.
# ==================================================================================================
CFG = dict(
    # ---- Ruling 1: the replacement bars, via the engine's OWN netting path, never hand-copied ----
    bars_path='BARS[P] = MA.REPL[P] - rd.REPL_DROP[P], read live at import off the UNLOWERED MA.REPL '
              '(the same object price6 lowers inside its own context; taking it there too would net '
              'the drop twice)',
    repl_drop_pts=float(rd.REPL_DROP_PTS),
    # ---- Ruling 3: the production-value function, certified bit-exact at step 1 ----
    price_fn='season_points(X,P) = SCALE * posval( X + capt_prem(X) - BARS[P] ) * 21',
    scale=float(MA.SCALE), scale_dist=float(dp.SCALE_DIST),
    s_sh=float(MA.S_SH), capt_thresh=float(MA.CAPT_THRESH),
    season_games_const=21.0,
    gamma=float(MA.GAMMA),
    gamma_note='GAMMA==1.0 makes val(r)=SCALE*r LINEAR, so delivered value is ADDITIVE across seasons '
               'in board points and a career is a straight sum. This is the fact Ruling 11 rests on.',
    # ---- Ruling 2: discounting ----
    disc='rl_model.disc_factor(entry_age, LENS[bal], k), k = season_year - entry_year',
    disc_rate=float(MA.LENS['bal']),
    disc_variant='flat-14',
    disc_note='FLAT 14%/yr FROM ACQUISITION. The discount ladder is keyed on ENTRY AGE and on years '
              'since entry -- one ladder for the whole career, observed seasons and projected tail '
              'alike. k<=0 discounts at 1.0 (the engine\'s own convention); the pre-cohort pool rows '
              '(ORDER 26A anomaly 3) are the only k<0 cases and are counted, not hidden.',
    age_disc_on=bool(MA.AGE_DISC), age_disc_mode=int(MA.AGE_DISC_MODE or 0),
    # ---- Ruling 10: games weighting ----
    games_weight='w = min(1, sqrt(games/10)); >=10 games = a FULL season at its average',
    games_weight_linear_sensitivity='w = min(1, games/10)  [named cases only, per Ruling 10]',
    availability='otherwise UNPRICED -- no separate availability haircut, matching forward projections',
    # ---- Ruling 4: truncation and the zero floor ----
    truncation='at the last listed season (the store writes no row past it); below-bar seasons credit '
               'ZERO and never negative -- enforced by posval, which is >=0 by construction, so no '
               'longevity penalty is possible',
    # ---- Ruling 5: the two uses of position ----
    position_use='VALUE each season at the position PLAYED that season (its own replacement bar); '
                 'ATTRIBUTE the summed career to the ACQUISITION slot -- ND: pick; pool: mechanism x '
                 'day-0 signed position. Both fields are carried separately in Layer 1 and neither is '
                 'collapsed into the other.',
    season_bar_rule='THE ENGINE\'S OWN rl_model.py::_fit_bar (line 99-104), reused verbatim: a season '
                    'row\'s pos is split on "/", collapsed by _collapse_elig, and the bar is the '
                    'LOWEST-REPL member of the pair (R105.1, the MAX law -- a lower bar gives a higher '
                    'posval, and the netting is floored >=0 by construction). A season row with no pos '
                    'falls back to the CURRENT declaration column via _decl_bar, which is the engine\'s '
                    'own rule for a closed season with no row. 1,877 of the 11,484 Layer-1 season rows '
                    'carry a DUAL label (SF/MID 949, SD/MID 369, KPF/RUCK 199, ...); Layer 1 records '
                    'position_group=null for those because MA.GRP maps single labels only. Dropping '
                    'them would have deleted 16.3 % of the league\'s played seasons.',
    # ---- Ruling 7 ----
    era_norm='NONE',
    # ---- Ruling 8: the three-tier window ----
    window_core='entry_year <= 2014  -- clean fit core. Actives are IN: observed + a small projected '
                'tail off the engine\'s own band machinery, per-player tail share disclosed.',
    window_augmented='2015 <= entry_year <= 2021 -- augmented: observed + gated projected tails, per-'
                     'player tail share disclosed. The gate is SATISFIED AT THE CORE (owner ruling '
                     '5270492281), which is what admits these tails.',
    window_sensitivity='entry_year >= 2022 -- EXCLUDED from every fit; walk-forward sensitivity only.',
    window_floor=2004,
    window_floor_note='entries before 2004 are excluded from the fit population: the store\'s scoring '
                      'data begins in 2005, so a 2003 entry\'s year-1 is structurally unobservable. '
                      '2004 is the engine\'s own curve teaching-window floor (YR_LO).',
    # ---- the projected tail ----
    tail_source='the engine\'s own band machinery: bb = b6(p); each band level L unrolled through '
                'proj_from_peak\'s loop (frac / PEAK_AGE / bnow / futblend / age>38 / frac<0.42), '
                'WQ6-blended at SCALE_DIST -- the same construction step 1 certified bit-exact.',
    tail_window='ONLY seasons whose calendar year is strictly greater than the player\'s last observed '
                'season year. The k=0 projection season is dropped whenever it duplicates an observed '
                'row, so no season is counted twice.',
    tail_multipliers='x1.05 for KPF/KPD and x(1 + runway*elite*PMAX) -- DECLARED. Both belong to the '
                     'engine\'s price of a PROJECTED career and were declared at the gate too.',
    tail_no_floor='MA.prod_floor is NOT applied to a tail. It is a WHOLE-CAREER floor object; applying '
                  'it to a fragment would invent value the band machinery never projected. DECLARED '
                  'as a departure from dp.v_at_peak, which does apply it to a whole career.',
    tail_eligibility='retired == False only. A concluded career has no tail by definition.',
    # ---- Ruling 6 ----
    anchor='pick 1 = 3000 (frozen ruler) -- applied at the CURVE, not at the scorer.',
)

# ==================================================================================================
# CORRECTION 26B-C1 -- THE OWNER'S FORCE-MAJEURE EXCLUSION, AS NAMED CONFIG
# ==================================================================================================
# A STANDING owner ruling that ORDER 26B's brief did not carry, re-filed at #334 comment 5274640130
# (2026-08-13). It ships HERE, as named config with its keys, its reason and its provenance -- never
# as a hardcoded special case buried in a loop -- and the deriver asserts it (o26b_derive.py) so that
# a future edit cannot silently drop it again. That is the whole point: this is the third ruling this
# week found living as register prose instead of a machine check.
FORCE_MAJEURE = dict(
    rule='WHOLE-DRAFT SLIDE',
    excluded_keys=['thomas-boyd', 'paddy-mccartin'],
    excluded_detail={'thomas-boyd': 'ND pick 1, 2013', 'paddy-mccartin': 'ND pick 1, 2014'},
    reason='owner force-majeure ruling -- two pick-1 KPF careers ended by acts of god (one '
           'concussion, one mental health). OWNER VERBATIM: "those players were pick 1 KPF busts, '
           'so heavily bias the pool against them, however one retired early with depression, and '
           'another with concussion issues. It\'s a force majeure situation..." They may not teach '
           'the pick-1 cohort, because those acts of god are unlikely to recur at pick 1.',
    provenance='standing owner ruling, register v533-era, verbatim; mechanics settled by the owner\'s '
               'own amendment and re-filed at #334 comment 5274640130 (2026-08-13). Applied to this '
               'order by CORRECTION ORDER 26B-C1.',
    mechanics='In each affected draft year EVERY ND draftee slides UP one pick: natural pick N is '
              'attributed to slid pick N-1. The excluded key (natural pick 1) is dropped from every '
              'cohort input entirely. A natural pick 65 slides to 64, ENTERS the ND 1-64 fit and '
              'LEAVES the ND>64 pathway for that year. Slid effective picks are computed BEFORE the '
              'ND/pool split, so the split is taken on the SLID pick, never the stored one.',
    slide_years=[2013, 2014],
    scope='ND rows in the slide years only. No pool pathway (RD/SSP/MSD/IRE/PDA/PDN/PDS/UNR) is '
          'touched, and no other draft year is touched.',
    store_untouched='THE SLIDE IS A DERIVATION-TIME ATTRIBUTION RULE ONLY. The store is never edited '
                    'and Layer 1 is never edited -- raw facts carry no attribution. Layer 1 keeps the '
                    'natural pick; the slid pick exists only in this attribution map.',
    layer2_scores_unaffected='Per-career delivered value is UNCHANGED by this correction. Only the '
                             'cohort a career is ATTRIBUTED to moves (Ruling 5\'s acquisition slot). '
                             'LAYER2.json::base is byte-identical across the correction.',
)
# ==================================================================================================
# ORDER 26B-V -- THE GRACE-YEARS VARIANTS.  **MEASUREMENT ONLY. NOT RULED.**
# ==================================================================================================
# Owner order #334 comment 5275831956 (2026-08-13). His diagnosis: the flat-from-year-1 fade
# compresses the hits' peak seasons (a year-4 peak carries 1.14^-4 = 0.5921 from day 0) while busts
# score zero under any fade. The variants delay the START of the fade for young entrants only.
#
# THE k MAPPING, STATED (PRESTATEMENT_26BV.md §2). This scorer's k is `season_year - entry_year`, so
# k = 1 IS a normal draftee's first played season and today carries 1.14^-1. The order's formula
# (1.14)^-max(0, j-1-G) has j = k. At G = 0 that formula gives max(0, k-1) -- ONE FREE YEAR FOR
# EVERYONE, which collides with the owner's own "Not mature age players". Both readings are computed;
# neither is silently chosen:
#   READING O (PRIMARY)   exponent max(0, k - G_O)   -- reproduces his stated grace-A weights exactly
#                         (k=1,2 -> 1.0; k=3 -> 1.14^-1) AND leaves mature-agers on today's ladder
#   READING L (SECONDARY) exponent max(0, k - 1 - G) -- the order's formula, taken literally
GRACE = dict(
    status='MEASUREMENT ONLY -- NOT RULED. flat-14 remains the operative basis.',
    provenance='owner order #334 comment 5275831956 (2026-08-13); readings and the k-mapping fixed in '
               'PRESTATEMENT_26BV.md, committed before any variant was computed.',
    owner_diagnosis='the flat-from-year-1 fade compresses the hits\' peak seasons (year-4 weight '
                    '0.5921) while busts score zero under any fade',
    owner_spec_A='"the future season fade only starts after season 1... years 1 and 2 are 100%, then '
                 'year 3 14% less" -- for normal-draft-age entrants only ("19 in their first year. '
                 'Not mature age players")',
    owner_spec_B='"normal draft age kids get two seasons of grace, and kids drafted one year older '
                 'get one"',
    mechanism='an EXPONENT SHIFT in the existing discount ladder: DF(k) = disc_factor(entry_age, '
              '0.14, max(0, k - G)). It still routes through the engine\'s own disc_factor callable; '
              'only the exponent handed to it moves.',
    k_convention='k = season_year - entry_year; k = 1 is a normal draftee\'s FIRST played season and '
                 'carries 1.14^-1 on the current basis. k <= 0 discounts at 1.0 (engine convention).',
    reading_O='PRIMARY. exponent max(0, k - G_O).  grace-A: G_O = 2 if entry_age <= 19 else 0.  '
              'grace-B: G_O = 3 if <= 19, 2 if == 20, else 0.',
    reading_L='SECONDARY. exponent max(0, k - 1 - G).  grace-A: G = 1 if <= 19 else 0.  grace-B: '
              'G = 2 if <= 19, 1 if == 20, else 0.  Gives EVERY entrant one free year at G = 0.',
    grace0_diagnostic='exponent max(0, k - 1) for everyone -- isolates the universal one-year shift '
                      'the literal formula embeds, so the conflation is a number and not an argument.',
    age_source='Layer 1 entry_age (100% coverage); the recorded year-18 fallback is used only where '
               'entry_age is null, and it never overwrites a real age.',
    everything_else='identical to the operative C2 basis: loclin curve, force-majeure slide, window '
                    'tiers, games weighting, K=15, bars, positions, tails.',
    landing_constraint='AT LANDING THE TWO SIDES CANNOT MOVE APART. The identity gate ties this '
                       'scorer to price6, which discounts projected seasons through the same '
                       'disc_factor. A grace on the curve side alone would break that identity and '
                       'the ruled landing assert with it. If a grace is ever ruled in it must be '
                       'ruled into disc_factor itself, and both sides re-derive together.',
)


def grace_O(variant):
    """READING O -- the PRIMARY reading. Returns G_O(entry_age)."""
    if variant == 'A':
        return lambda a: 2 if (a is not None and a <= 19) else 0
    if variant == 'B':
        return lambda a: 3 if (a is not None and a <= 19) else (2 if a == 20 else 0)
    raise ValueError(variant)


def grace_L(variant):
    """READING L -- the order's formula taken literally. Returns G_O-equivalent = 1 + G."""
    if variant == 'A':
        return lambda a: 2 if (a is not None and a <= 19) else 1
    if variant == 'B':
        return lambda a: 3 if (a is not None and a <= 19) else (2 if a == 20 else 1)
    raise ValueError(variant)


def grace_zero(_variant=None):
    """The grace-0 diagnostic: the universal one-year shift, nobody age-targeted."""
    return lambda a: 1


FM_KEYS = set(FORCE_MAJEURE['excluded_keys'])
FM_YEARS = set(FORCE_MAJEURE['slide_years'])
CFG['force_majeure'] = FORCE_MAJEURE


def attribute(e):
    """Ruling 5's ACQUISITION SLOT, with the owner's force-majeure whole-draft slide applied.
    This is the ONLY place a cohort key is decided; the deriver and the comparison harness both read
    its output out of LAYER2.json rather than recomputing it."""
    key, ty, yr, pk = e['key'], e['type'], e['entry_year'], e['pick']
    if key in FM_KEYS:
        return dict(excluded=True, mechanism=None, pick=None, natural_pick=pk, slid=False,
                    why='owner force-majeure exclusion')
    slid = False
    if ty == 'ND' and yr in FM_YEARS and pk:
        pk = pk - 1
        slid = True
    mech = e['mechanism']
    if ty == 'ND':                       # the ND/pool split is taken on the SLID pick, per the ruling
        mech = 'ND 1-64' if (pk and 1 <= pk <= 64) else 'ND>64'
    return dict(excluded=False, mechanism=mech, pick=pk, natural_pick=e['pick'], slid=slid, why=None)

# THE BARS. Computed, never typed. This is the only place a bar number exists in this harness.
BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
RULING1 = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
for g, b in RULING1.items():
    assert abs(BARS[g] - b) < 5e-2, "bar %s %.4f != Ruling 1's %.1f" % (g, BARS[g], b)
CFG['bars'] = {g: round(BARS[g], 6) for g in sorted(BARS)}


def season_raw(X, pos):
    """Ruling 3's pinned callable in the engine's RAW production units. IDENTICAL text to
    o26b_gate.py::season_raw, which step 1 certified bit-exact against price6 on 804/804 rows."""
    return MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0


def season_bar_group(pos_label, p):
    """THE ENGINE'S OWN season-bar rule (rl_model.py::_fit_bar, lines 99-104), reused not reimagined:
    split a season row's pos on '/', collapse it, take the LOWEST-REPL member. No row pos -> the
    current declaration column (_decl_bar), which is the engine's rule for a closed season with no
    row. Returns (group, how)."""
    if pos_label:
        es = MA._collapse_elig(str(pos_label).replace('/', ','))
        if es:
            g = min(es, key=lambda x: MA.REPL[x])
            return g, ('single' if len(es) == 1 else 'dual_lowest_repl')
    if p is not None:
        try:
            return MA._decl_bar(p), 'decl_column_fallback'
        except Exception:
            pass
    return None, 'unresolved'


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


def w_linear(g):
    return min(1.0, max(0.0, g) / 10.0)


# --------------------------------------------------------------------------------------------------
# THE DISCOUNT LADDER.  One object, used by observed seasons and by the tail alike.
# --------------------------------------------------------------------------------------------------
class Disc(object):
    """flat-14 (the live config, Ruling 2) or the V5 age ladder (NOT-RULED appendix).

    V5 is exercised through the ENGINE'S OWN age_disc/disc_factor path by flipping MA.AGE_DISC /
    MA.AGE_DISC_MODE in memory on the STAGED copy -- never by reimplementing the ladder here, and
    never by writing a file."""

    def __init__(self, mode='flat14', grace=None, nodisc=False):
        self.mode = mode
        # ORDER 26B-V: `grace` is a callable entry_age -> G, shifting the EXPONENT handed to the
        # engine's own disc_factor. None = today's ladder, exponent k.
        self.grace = grace
        # ORDER 26B-L: `nodisc` turns the discount OFF entirely -- every season counts equally.
        # It is still routed through the engine's own disc_factor, handed exponent 0 (which the
        # engine defines as 1.0), so the season valuation itself is byte-identical and ONLY the
        # time-weighting changes. Used for the ledger's RAW UNDISCOUNTED column.
        self.nodisc = nodisc

    def __enter__(self):
        self._sav = (MA.AGE_DISC, MA.AGE_DISC_MODE)
        if self.mode == 'V5':
            MA.AGE_DISC = True; MA.AGE_DISC_MODE = 5
        else:
            MA.AGE_DISC = False; MA.AGE_DISC_MODE = 0
        return self

    def __exit__(self, *a):
        MA.AGE_DISC, MA.AGE_DISC_MODE = self._sav
        return False

    def f(self, entry_age, k):
        if self.nodisc:
            k = 0
        elif self.grace is not None:
            k = max(0, k - self.grace(entry_age))
        return MA.disc_factor(entry_age, MA.LENS['bal'], k, 'bal')


# ==================================================================================================
# LOAD LAYER 1 AND THE ENGINE'S OWN RECORD VIEW
# ==================================================================================================
L1 = json.load(open(L1P))
ENTRIES = L1['entries']
SEASONS = collections.defaultdict(list)
for s in L1['player_seasons']:
    SEASONS[s['key']].append(s)
for k in SEASONS:
    SEASONS[k].sort(key=lambda x: x['year'])

BYKEY = {}
for p in MA.data:
    kk = p.get('key') or MA.slug(p['player'])
    if kk not in BYKEY: BYKEY[kk] = p

NOW = 2026     # MA.AGE_REF / the board's own current season; asserted below
assert int(MA.AGE_REF) == NOW, "AGE_REF %s != %d" % (MA.AGE_REF, NOW)


def observed_value(e, D, wfn):
    """The observed leg of a career: every played season, valued at the position PLAYED, weighted by
    games, discounted to acquisition. Returns (board points, per-season detail, counters)."""
    ey, ea = e['entry_year'], e['entry_age']
    if ea is None: ea = e['entry_age_fallback_if_null']
    tot = 0.0; det = []; ctr = collections.Counter()
    p = BYKEY.get(e['key'])
    for s in SEASONS.get(e['key'], []):
        pos, how = season_bar_group(s['position_played'], p)
        ctr['bar_' + how] += 1
        if pos is None or pos not in BARS:
            ctr['season_no_bar_position'] += 1
            continue
        k = (s['year'] - ey) if ey is not None else 0
        if k < 0: ctr['season_before_entry'] += 1
        w = wfn(s['games'])
        if s['games'] < 10: ctr['season_part_weighted'] += 1
        raw = season_raw(s['avg'], pos)
        if raw <= 0: ctr['season_below_bar_zero'] += 1
        pts = MA.SCALE * raw * w / D.f(ea, k)
        tot += pts
        det.append(dict(year=s['year'], k=k, games=s['games'], avg=s['avg'], pos=pos,
                        w=round(w, 6), pts=pts))
    return tot, det, ctr


def tail_value(e, D):
    """The projected tail off the engine's own band machinery (Ruling 8), discounted to acquisition
    on the SAME ladder as the observed leg. Seasons at or before the last observed year are dropped,
    so nothing is double-counted. Returns (board points, n_tail_seasons, first_tail_year)."""
    p = BYKEY.get(e['key'])
    if p is None or e['retired']: return 0.0, 0, None
    ey, ea = e['entry_year'], e['entry_age']
    if ea is None: ea = e['entry_age_fallback_if_null']
    last_obs = e['last_season']
    sav = dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g] = sav[g] - rd.REPL_DROP.get(g, 0)
        MA._pe_clear()
        with contextlib.redirect_stdout(io.StringIO()):
            bb = [float(x) for x in b6(p)]
            gfut = MA.gfut(p); g0 = MA.bnow(p); cur = MA.level_now(p)
            a = MA.age(p); fut = MA.futblend(p); pa = MA.PEAK_AGE[gfut]
            vals = []; ntail = 0; first = None
            for L in bb:
                cl = cur if cur else L * MA.frac(a, pa)
                acc = 0.0; n = 0
                for k in range(18):
                    ag = a + k
                    if ag > 38 or MA.frac(ag, pa) < 0.42: break
                    lev = L * MA.frac(ag, pa)
                    if ag <= pa: lev = max(lev, cl)
                    if k == 0: lev = max(lev, cl)
                    if k == 0 and p.get('_avail_hc', 0.0) > 0 and MA.BASE_REF == NOW and MA.AGE_REF == NOW:
                        lev *= (1 - p['_avail_hc'])
                    yr = NOW + k
                    if last_obs is not None and yr <= last_obs: continue
                    mix = [(g0, 1.0)] if k == 0 else list(fut)
                    kk = (yr - ey) if ey is not None else k
                    acc += sum(wt * season_raw(lev, gg) for gg, wt in mix) / D.f(ea, kk)
                    n += 1
                    if first is None or yr < first: first = yr
                if gfut in ('KPF', 'KPD'): acc *= 1.05
                runway = MA.clamp((25 - a) / 6.0, 0, 1)
                elite = MA.clamp((L / MA.PEAK[gfut] - 0.97) / 0.30, 0, 1)
                acc *= (1 + runway * elite * MA.PMAX)
                vals.append(MA.SCALE * acc); ntail = max(ntail, n)
        return float(dp.SCALE_DIST * _det_dot(WQ6, vals)), ntail, first
    finally:
        MA.REPL.update(sav)


def score_all(disc_mode='flat14', wfn=w_sqrt, with_tail=True, keys=None, grace=None, nodisc=False):
    out = {}; CTR = collections.Counter()
    with Disc(disc_mode, grace, nodisc) as D:
        for e in ENTRIES:
            if keys is not None and e['key'] not in keys: continue
            obs, det, ctr = observed_value(e, D, wfn)
            CTR.update(ctr)
            tail, ntail, firsty = (tail_value(e, D) if with_tail else (0.0, 0, None))
            tot = obs + tail
            out[e['key']] = dict(key=e['key'], obs=obs, tail=tail, total=tot,
                                 tail_share=(tail / tot if tot > 0 else 0.0),
                                 n_tail_seasons=ntail, first_tail_year=firsty,
                                 n_obs_seasons=len(det))
    return out, CTR


# ==================================================================================================
# RUN
# ==================================================================================================
LOG = []
def P(s=''):
    print(s); LOG.append(s)


P("=" * 112)
P("ORDER 26B  --  STEP 3, LAYER 2: THE VALUATION LAYER (Ruling 11)")
P("=" * 112)
P("authority to run: #334 comment 5270492281 -- OWNER RULING 'Core, resume'.")
P("pins verified: " + ", ".join("%s=%s" % (k, v[1][:8]) for k, v in sorted(PINS.items()))
  + ", layer1=%s" % L1_MD5[:8])
P()
P("THE CONFIG BLOCK (Ruling 11: ALL knobs in one place)")
for k in sorted(CFG):
    v = CFG[k]
    if isinstance(v, dict): v = json.dumps({a: (round(b, 4) if isinstance(b, float) else b)
                                            for a, b in v.items()}, sort_keys=True)
    P("  %-32s %s" % (k, v))
P()

# ==================================================================================================
# ORDER 26B-L -- THE LEDGER FAST PATH.  `python3 o26b_layer2.py --ledger`
# ==================================================================================================
# Writes ONLY the raw-undiscounted observed-only scoring, to its OWN side file, and exits before the
# eight tail-bearing runs above it. Two reasons it is a side file and not a key in LAYER2.json:
#   1. LAYER2.json is READ by o26b_derive.py, o26b_compare.py and o26b_variants.py, and its md5 is
#      quoted in DERIVE.json. Adding a key would move that md5 and invalidate three committed
#      artifacts for a column that feeds no derivation at all.
#   2. The full script runs eight projected-tail scorings and takes ~15 minutes; the ledger needs
#      one observed-only pass, which takes seconds. A read-only reporting column should not cost a
#      re-derivation.
# The SCORER IS THE SAME OBJECT -- same bars, same games weighting, same truncation, same position
# rule. Only the discount is off, and even that routes through the engine's own disc_factor (handed
# exponent 0, which the engine itself defines as 1.0).
if '--ledger' in sys.argv:
    NODISC, _ctr = score_all('flat14', w_sqrt, with_tail=False, nodisc=True)
    _p = os.path.join(HERE, 'LAYER2_NODISC.json')
    json.dump(dict(what='ORDER 26B-L: observed-only, DISCOUNT OFF -- the ledger\'s raw undiscounted '
                        'column. Same season valuation and games weighting as LAYER2.json::base; '
                        'only the time-weighting differs.',
                   built_by='docs/evidence/delivered_value_2026-08-12/o26b_layer2.py --ledger',
                   layer1_md5=L1_MD5, pins={k: v[1] for k, v in PINS.items()},
                   determinism='no build timestamp, deliberately',
                   season_counters=dict(_ctr), obs=NODISC),
              open(_p, 'w'), indent=None, separators=(',', ':'), sort_keys=True, default=float)
    print("ORDER 26B-L -- wrote LAYER2_NODISC.json  (%d careers, observed only, discount OFF)"
          % len(NODISC))
    assert_pins('exit')
    print("  pins re-verified at exit -- nothing under engine/ was written.")
    raise SystemExit(0)

BASE, CTR = score_all('flat14', w_sqrt, True)
P("SCORED %d careers  (flat-14, sqrt games weighting, gated tails on live careers)" % len(BASE))
P("  season counters: %s" % dict(CTR))

# ---- window tiers ------------------------------------------------------------------------------
TIER = {e['key']: e['window_tier'] for e in ENTRIES}
EMETA = {e['key']: e for e in ENTRIES}


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


def disp(xs):
    """EVERY distributional claim reports dispersion -- the binding law from the gate leg's finding
    that a median can be unbiased while the distribution spans 0.09x to 4.2x."""
    return dict(n=len(xs), mean=(sum(xs) / len(xs) if xs else float('nan')),
                p05=q(xs, .05), median=q(xs, .50), p95=q(xs, .95),
                min=(min(xs) if xs else float('nan')), max=(max(xs) if xs else float('nan')))


P()
P("BY WINDOW TIER (Ruling 8)  -- delivered value, board points, discounted to acquisition")
P("  %-22s %6s %12s %12s %12s %12s %10s %10s" %
  ('tier', 'n', 'mean', 'p05', 'median', 'p95', 'zero%', 'tailshare'))
for t in ['core<=2014', 'augmented2015-2021', 'sensitivity2022+']:
    ks = [k for k in BASE if TIER[k] == t]
    vs = [BASE[k]['total'] for k in ks]
    ts = [BASE[k]['tail_share'] for k in ks if BASE[k]['total'] > 0]
    d = disp(vs)
    P("  %-22s %6d %12.1f %12.1f %12.1f %12.1f %9.1f%% %9.3f" %
      (t, d['n'], d['mean'], d['p05'], d['median'], d['p95'],
       100.0 * sum(1 for v in vs if v <= 0) / max(1, len(vs)),
       (sum(ts) / len(ts) if ts else 0.0)))

P()
P("TAIL SHARES, disclosed per Ruling 8 (live careers only; retired careers carry no tail)")
for t in ['core<=2014', 'augmented2015-2021', 'sensitivity2022+']:
    ks = [k for k in BASE if TIER[k] == t and not EMETA[k]['retired'] and BASE[k]['total'] > 0]
    ts = [BASE[k]['tail_share'] for k in ks]
    d = disp(ts)
    P("  %-22s live n=%4d   mean %.4f   p05 %.4f  median %.4f  p95 %.4f  max %.4f"
      % (t, d['n'], d['mean'], d['p05'], d['median'], d['p95'], d['max']))
P("  (core actives ARE kept: Ruling 8 -- 'dropping old actives would delete the stars')")

# ---- SENSITIVITY 1: linear games weighting, NAMED CASES (Ruling 10) -----------------------------
NAMED = ['willem-duursma', 'callum-moore', 'harrison-ramm', 'vigo-visentini', 'jai-newcombe',
         'nick-daicos', 'harry-sheezel', 'marcus-bontempelli', 'max-gawn', 'harley-reid',
         'josh-treacy', 'izak-rankine', 'lachlan-ash']
NAMED = [k for k in NAMED if k in BASE]
LIN, _ = score_all('flat14', w_linear, True, keys=set(NAMED))
P()
P("SENSITIVITY 1 -- LINEAR GAMES WEIGHTING w=min(1,games/10)  [Ruling 10: NAMED CASES ONLY]")
P("  %-22s %12s %12s %10s   %s" % ('key', 'sqrt (base)', 'linear', 'delta%', 'part-seasons'))
for k in NAMED:
    nprt = sum(1 for s in SEASONS.get(k, []) if s['games'] < 10)
    b, l = BASE[k]['total'], LIN[k]['total']
    P("  %-22s %12.1f %12.1f %+9.3f%%   %d" % (k, b, l, (100 * (l / b - 1) if b else 0.0), nprt))
# aggregate, DISCLOSED as beyond the ruling's ask
ALLLIN, _ = score_all('flat14', w_linear, True)
db = [ALLLIN[k]['total'] / BASE[k]['total'] for k in BASE if BASE[k]['total'] > 0]
d = disp(db)
P("  [beyond the ruling's ask, disclosed] whole-population linear/sqrt: n=%d p05 %.4f med %.4f p95 %.4f"
  % (d['n'], d['p05'], d['median'], d['p95']))

# ---- SENSITIVITY 2: the V5 age ladder (NOT-RULED appendix) --------------------------------------
V5, _ = score_all('V5', w_sqrt, True)
P()
P("SENSITIVITY 2 -- THE V5 AGE LADDER  (rl_model.py::_V5_KNOTS, RL_AGE_DISC_MODE=5)  [NOT-RULED]")
P("  knots: %s" % MA._V5_KNOTS)
P("  V5 is exercised through the engine's OWN age_disc()/disc_factor() path (MA.AGE_DISC flipped in")
P("  memory on the staged copy). The ladder is keyed on ENTRY AGE, so a young entrant discounts at")
P("  12.0-13.5%% instead of flat 14%% -- a LOWER rate, hence a HIGHER present value.")
P("  %-14s %6s %12s %12s %10s %10s %10s" % ('entry age', 'n', 'flat14 mean', 'V5 mean', 'p05 r', 'med r', 'p95 r'))
for lo, hi, lbl in [(0, 18, '<=18'), (19, 19, '19'), (20, 21, '20-21'), (22, 25, '22-25'), (26, 99, '26+')]:
    ks = [k for k in BASE if BASE[k]['total'] > 0
          and (EMETA[k]['entry_age'] or EMETA[k]['entry_age_fallback_if_null'] or 0) >= lo
          and (EMETA[k]['entry_age'] or EMETA[k]['entry_age_fallback_if_null'] or 0) <= hi]
    if not ks: continue
    r = [V5[k]['total'] / BASE[k]['total'] for k in ks]
    d = disp(r)
    P("  %-14s %6d %12.1f %12.1f %10.4f %10.4f %10.4f"
      % (lbl, len(ks), sum(BASE[k]['total'] for k in ks) / len(ks),
         sum(V5[k]['total'] for k in ks) / len(ks), d['p05'], d['median'], d['p95']))

# ---- the named rows --------------------------------------------------------------------------
P()
P("THE NAMED ROWS -- delivered value, board points, discounted to acquisition")
P("  %-22s %5s %6s %5s %8s %5s %11s %11s %11s %8s" %
  ('key', 'mech', 'pick', 'd0pos', 'entry', 'nsea', 'observed', 'tail', 'TOTAL', 'tail%'))
for k in NAMED:
    e = EMETA[k]; r = BASE[k]
    P("  %-22s %5s %6s %5s %8s %5d %11.1f %11.1f %11.1f %7.1f%%"
      % (k, (e['mechanism'] or '')[:5], e['pick'], e['position_group'], e['entry_year'],
         e['n_season_rows'], r['obs'], r['tail'], r['total'], 100 * r['tail_share']))

# ---- the attribution map (CORRECTION 26B-C1) -----------------------------------------------------
ATTR = {e['key']: attribute(e) for e in ENTRIES}
P()
P("CORRECTION 26B-C1 -- THE OWNER'S FORCE-MAJEURE EXCLUSION (%s)" % FORCE_MAJEURE['rule'])
P("  provenance: %s" % FORCE_MAJEURE['provenance'])
P("  EXCLUDED  : %s" % ", ".join("%s (%s, delivered %.1f)"
                                % (k, FORCE_MAJEURE['excluded_detail'][k], BASE[k]['total'])
                                for k in FORCE_MAJEURE['excluded_keys']))
P("  slide years %s -- every ND draftee slides UP one pick; the ND/pool split is taken on the SLID pick"
  % sorted(FM_YEARS))
for yr in sorted(FM_YEARS):
    sl = [e for e in ENTRIES if ATTR[e['key']]['slid'] and e['entry_year'] == yr]
    nat = sorted(e['pick'] for e in sl)
    n65 = [e['key'] for e in sl if e['pick'] == 65]
    P("    %d: %d rows slid, natural picks %d..%d -> slid %d..%d   natural-65: %s"
      % (yr, len(sl), nat[0], nat[-1], nat[0] - 1, nat[-1] - 1,
         (n65[0] + ' (enters the ND fit, leaves ND>64)') if n65
         else 'NONE -- this draft ends at natural pick %d' % nat[-1]))
P("  Layer-2 per-career scores are UNCHANGED by this correction; only the cohort attribution moves.")
P("  Layer 1 is UNTOUCHED: it keeps the natural pick, and the slid pick exists only in this map.")

# ---- the fit population -------------------------------------------------------------------------
FITLO = CFG['window_floor']
ND = [e for e in ENTRIES if ATTR[e['key']]['mechanism'] == 'ND 1-64'
      and ATTR[e['key']]['pick'] and 1 <= ATTR[e['key']]['pick'] <= 64
      and e['entry_year'] is not None and FITLO <= e['entry_year'] <= 2021]
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
POOL = [e for e in ENTRIES if ATTR[e['key']]['mechanism'] in POOLM
        and e['entry_year'] is not None and FITLO <= e['entry_year'] <= 2021]
P()
P("THE FIT POPULATION (Ruling 8: <=2014 core + 2015-2021 augmented; 2022+ EXCLUDED)")
P("  ND 1-64, picks 1-64, entries %d-2021 : %d" % (FITLO, len(ND)))
P("  pool pathways,           entries %d-2021 : %d" % (FITLO, len(POOL)))
P("  EXCLUDED (2022+ sensitivity only)          : %d"
  % sum(1 for e in ENTRIES if e['entry_year'] and e['entry_year'] >= 2022))
P("  EXCLUDED (pre-%d, scoring data begins 2005): %d"
  % (FITLO, sum(1 for e in ENTRIES if e['entry_year'] and e['entry_year'] < FITLO)))
P("  EXCLUDED (owner force-majeure)             : %d  %s"
  % (len(FM_KEYS), sorted(FM_KEYS)))
byp = collections.Counter(ATTR[e['key']]['pick'] for e in ND)
P("  per-pick n, picks 1-64: min %d  median %d  max %d   (picks 1-20 mean %.1f)"
  % (min(byp.values()), sorted(byp.values())[len(byp) // 2], max(byp.values()),
     sum(byp[i] for i in range(1, 21)) / 20.0))

# ---- control: the scorer still reproduces the certified object -----------------------------------
P()
P("CONTROL -- the scorer is the SAME object step 1 certified.  season_raw() is byte-identical text to")
P("o26b_gate.py::season_raw, and the bars are recomputed here off the engine, not copied:")
P("  bars %s" % {g: round(BARS[g], 4) for g in sorted(BARS)})
P("  Ruling 1 %s" % RULING1)

# ---- ORDER 26B-V: the grace variants, as separate labelled Layer-2 runs -------------------------
GA_O, _ = score_all('flat14', w_sqrt, True, grace=grace_O('A'))
GB_O, _ = score_all('flat14', w_sqrt, True, grace=grace_O('B'))
GA_L, _ = score_all('flat14', w_sqrt, True, grace=grace_L('A'))
GB_L, _ = score_all('flat14', w_sqrt, True, grace=grace_L('B'))
G0, _ = score_all('flat14', w_sqrt, True, grace=grace_zero())
P()
P("ORDER 26B-V -- THE GRACE-YEARS VARIANTS  **MEASUREMENT ONLY, NOT RULED**")
P("  %s" % GRACE['mechanism'])
P("  READING O (primary):   %s" % GRACE['reading_O'])
P("  READING L (secondary): %s" % GRACE['reading_L'])
P("  %-26s %10s %10s %10s %10s %10s" % ('whole population', 'flat-14', 'graceA_O', 'graceB_O',
                                        'graceA_L', 'graceB_L'))
_nz = [k for k in BASE if BASE[k]['total'] > 0]
P("  %-26s %10.1f %10.1f %10.1f %10.1f %10.1f"
  % ('mean delivered (n>0)', sum(BASE[k]['total'] for k in _nz) / len(_nz),
     sum(GA_O[k]['total'] for k in _nz) / len(_nz), sum(GB_O[k]['total'] for k in _nz) / len(_nz),
     sum(GA_L[k]['total'] for k in _nz) / len(_nz), sum(GB_L[k]['total'] for k in _nz) / len(_nz)))
for lo, hi, lbl in [(0, 19, 'entry age <=19'), (20, 20, 'entry age 20'), (21, 99, 'entry age 21+')]:
    ks = [k for k in _nz if lo <= (EMETA[k]['entry_age'] or EMETA[k]['entry_age_fallback_if_null']
                                   or 0) <= hi]
    if not ks: continue
    P("    %-24s n=%4d   A_O %.4f  B_O %.4f  A_L %.4f  B_L %.4f   (x flat-14)"
      % (lbl, len(ks),
         sum(GA_O[k]['total'] for k in ks) / sum(BASE[k]['total'] for k in ks),
         sum(GB_O[k]['total'] for k in ks) / sum(BASE[k]['total'] for k in ks),
         sum(GA_L[k]['total'] for k in ks) / sum(BASE[k]['total'] for k in ks),
         sum(GB_L[k]['total'] for k in ks) / sum(BASE[k]['total'] for k in ks)))
P("  ZEROS ARE INVARIANT under every ladder (a bust scores 0 whatever the discount): flat-14 %d, "
  "graceA_O %d, graceB_O %d"
  % (sum(1 for k in BASE if BASE[k]['total'] <= 0), sum(1 for k in GA_O if GA_O[k]['total'] <= 0),
     sum(1 for k in GB_O if GB_O[k]['total'] <= 0)))

OUT = dict(cfg=CFG, pins={k: v[1] for k, v in PINS.items()}, layer1_md5=L1_MD5,
           now=NOW, base=BASE, v5=V5, linear_named={k: LIN[k] for k in NAMED},
           grace_cfg=GRACE, grace_a=GA_O, grace_b=GB_O,
           grace_a_readingL=GA_L, grace_b_readingL=GB_L, grace_zero=G0,
           linear_all=ALLLIN, named=NAMED,
           force_majeure=FORCE_MAJEURE, attribution=ATTR,
           fit_nd_keys=[e['key'] for e in ND], fit_pool_keys=[e['key'] for e in POOL],
           season_counters=dict(CTR))
json.dump(OUT, open(os.path.join(HERE, 'LAYER2.json'), 'w'), indent=None,
          separators=(',', ':'), sort_keys=True, default=float)
open(os.path.join(HERE, 'LAYER2_out.txt'), 'w').write("\n".join(LOG) + "\n")
assert_pins('exit')
P()
P("wrote LAYER2.json  (pins re-verified at exit: engine, store, board and Layer 1 untouched)")
open(os.path.join(HERE, 'LAYER2_out.txt'), 'w').write("\n".join(LOG) + "\n")
