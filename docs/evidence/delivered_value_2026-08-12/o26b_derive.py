#!/usr/bin/env python3
"""ORDER 26B -- STEP 4, THE DERIVATIONS.

  (a) THE ALL-IN PICK CURVE      cohort-mean delivered value by ND pick 1-64, smoothed, anchored
                                 pick 1 = 3000 (Ruling 6), pre-anchor scale reported (Ruling 13)
  (b) POSITIONAL ND RELATIVITIES by pick band, with the RECONCILIATION LAW ASSERTED IN CODE:
                                 the position-weighted mean equals the all-in curve at EVERY pick
                                 (Ruling 13 -- a HALT, not a tolerance)
  (c) POOL PATHWAY ALL-INS + POSITIONAL v0s through Ruling 12's BORROWING LADDER, K-shrinkage,
                                 every cell's n and borrowing share disclosed
  (d) THE MSD / YOUNG-PATHWAY QUESTION BOTH WAYS, with numbers under each and a recommendation

INPUT   LAYER2.json (step 3)  +  data/delivered_value/layer1_player_seasons.json (step 2, pinned)
OUTPUT  DERIVE.json  DERIVE_out.txt

THE SMOOTHER IS NOT INVENTED HERE. It is the SHIPPED year-zero aggregator, imported from the
walk-forward panel's own harness -- docs/evidence/composition_2026-08-10/noarb/
harness_pvc_REPINNED_pass3.py::kernel_raw -- a Gaussian kernel over log(pick) whose bandwidth grows
from HMIN until the effective n reaches NMIN, then a weighted mean. Its md5 is pinned below.

READ-ONLY. Nothing under engine/ is written; no board is built; no pin is moved.

  usage:  python3 o26b_derive.py
"""
import os, sys, json, math, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
HARN_DIR = os.path.join(ROOT, 'docs', 'evidence', 'composition_2026-08-10', 'noarb')
HARN = os.path.join(HARN_DIR, 'harness_pvc_REPINNED_pass3.py')
L1P = os.path.join(ROOT, 'data', 'delivered_value', 'layer1_player_seasons.json')


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


PINS = {'layer1': (L1P, 'ad1229ea6f443538479447132382b21c'),
        'smoother': (HARN, None),          # recorded, not gated: the harness is a shared instrument
        'store': (os.path.join(ROOT, 'engine/rl_after/rl_model_data.json'),
                  'd9a24282357cf3083b1640466e3ecd83'),
        'board': (os.path.join(ROOT, 'engine/rl_after/rl_app_data.json'),
                  '88ce647f531030d8d2e094188b258191'),
        'pvc_v2': (os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json'), None)}
for k, (p, exp) in PINS.items():
    got = _md5(p)
    if exp and got != exp:
        raise SystemExit("PIN FAILED %s: %s != %s" % (k, got, exp))

sys.path.insert(0, HARN_DIR)
import harness_pvc_REPINNED_pass3 as HP        # noqa: E402  -- the SHIPPED kernel, imported not copied
sys.path.insert(0, HERE)
import o26b_loclin as LL                        # noqa: E402  -- CORRECTION 26B-C2, the local-linear fit
# The C2 module restates the shipped dials for self-description; they must BE the shipped dials.
assert (LL.NMIN_DEFAULT, LL.HMIN_DEFAULT, LL.HMAX_DEFAULT) == (HP.NMIN, HP.HMIN, HP.HMAX), \
    "26B-C2: the loclin module's dials have drifted from the shipped aggregator's"

L2 = json.load(open(os.path.join(HERE, 'LAYER2.json')))
L1 = json.load(open(L1P))
E = {e['key']: e for e in L1['entries']}
BASE = L2['base']; V5 = L2['v5']
FM = L2['force_majeure']                # CORRECTION 26B-C1 -- named config, read, never re-derived
ATTR = L2['attribution']                # the ONE attribution map; this file does not recompute it
BOARD = json.load(open(os.path.join(ROOT, 'engine/rl_after/rl_app_data.json')))
PVC = {int(k): float(v) for k, v in BOARD['PVC'].items()}

PIN1 = 3000.0
POSN = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLM = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
BANDS = HP.RANGES                    # the engine's own board RANGES
K_SHRINK = 15                        # pvc_curve_v2.json::pool_levels.k -- the owner's own signed-level
                                     # shrinkage constant, reused so 26B does not invent a second one

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


def disp(xs):
    """DISPERSION IS BINDING (the gate leg's own finding: a median of 1.0044 sat on a distribution
    spanning 0.09x to 4.2x). No mean is ever reported here without p05/median/p95 beside it."""
    xs = list(xs)
    return dict(n=len(xs), mean=(sum(xs) / len(xs) if xs else float('nan')),
                p05=q(xs, .05), median=q(xs, .50), p95=q(xs, .95))


def dstr(d):
    return "n=%4d mean %9.1f | p05 %8.1f  med %8.1f  p95 %9.1f" % (
        d['n'], d['mean'], d['p05'], d['median'], d['p95'])


# ==================================================================================================
P("=" * 118)
P("ORDER 26B  --  STEP 4, THE DERIVATIONS")
P("=" * 118)
P("  layer1  %s" % PINS['layer1'][1])
P("  layer2  LAYER2.json md5 %s" % _md5(os.path.join(HERE, 'LAYER2.json')))
P("  store   %s   board %s" % (PINS['store'][1][:8], PINS['board'][1][:8]))
P("  SMOOTHER: harness_pvc_REPINNED_pass3.py::kernel_raw  md5 %s" % _md5(HARN)[:12])
P("            Gaussian kernel over log(pick); bandwidth grows from HMIN=%.2f in 0.02 steps until the"
  % HP.HMIN)
P("            effective n reaches NMIN=%.0f (cap HMAX=%.2f); then a weighted MEAN. This is the"
  % (HP.NMIN, HP.HMAX))
P("            SHIPPED year-zero aggregator, imported -- 26B does not invent a smoother.")
P("  K-shrinkage K=%d  (pvc_curve_v2.json::pool_levels.k -- the owner's own signed-level constant)"
  % K_SHRINK)
REPL = {}


def report_c1():
    """Printed only AFTER the three asserts below have run and passed -- a report of an assert that
    has not yet fired is a claim, not a check."""
    P()
    P("-" * 118)
    P("CORRECTION 26B-C1 -- THE OWNER'S FORCE-MAJEURE EXCLUSION, ASSERTED")
    P("-" * 118)
    P("  rule       %s" % FM['rule'])
    P("  provenance %s" % FM['provenance'])
    P("  EXCLUDED   %s" % ", ".join("%s (%s, delivered %.1f)"
                                    % (k, FM['excluded_detail'][k], BASE[k]['total'])
                                    for k in FM['excluded_keys']))
    P("  ASSERT (a) the two keys appear in NO ND or pool cohort input, at any pick .......... PASS")
    P("  ASSERT (b) each slide year's pick-N cohort holds the natural pick-(N+1) entrant ... PASS")
    for yr in sorted(FM_YEARS):
        P("               %d: %d pick positions checked (natural picks 2..%d -> slid 1..%d)"
          % (yr, _C1B[yr], _MAXNAT[yr], _MAXNAT[yr] - 1))
    P("  ASSERT (c) a natural pick 65 slides to 64, enters the ND fit, leaves ND>64 ........ PASS")
    for yr in sorted(FM_YEARS):
        if _C1C[yr]:
            P("               %d: %s -- natural 65 -> slid 64, in the ND fit, out of ND>64"
              % (yr, ", ".join(_C1C[yr])))
        else:
            P("               %d: NO natural pick 65 EXISTS -- this national draft ends at natural"
              % yr)
            P("                     pick %d, so the 65-clause has nothing to act on. MEASURED, not"
              % _MAXNAT[yr])
            P("                     assumed.")
    P("               => ND>64 loses ONE entrant to the ND fit, not two. The correction order")
    P("                  anticipated two; the 2013 draft is 61 picks long and has no 65th.")
    P()
    P("  WHO REPLACED THE EXCLUDED ROWS IN THE PICK-1 COHORT (the owner's question, answered)")
    P("    %-6s %-22s %-6s %12s   %-26s %-6s %12s" %
      ('year', 'excluded (natural 1)', 'pos', 'delivered', 'natural 2 -> slid pick 1', 'pos',
       'delivered'))
    for yr in sorted(FM_YEARS):
        ex = [k for k in FM['excluded_keys'] if E[k]['entry_year'] == yr]
        n2 = [k for k in ATTR if E[k]['entry_year'] == yr and E[k]['type'] == 'ND'
              and ATTR[k]['natural_pick'] == 2]
        for a, b in zip(ex, n2):
            REPL[yr] = dict(excluded=a, excluded_value=BASE[a]['total'],
                            excluded_pos=E[a]['position_group'], replacement=b,
                            replacement_value=BASE[b]['total'],
                            replacement_pos=E[b]['position_group'],
                            delta=BASE[b]['total'] - BASE[a]['total'])
            P("    %-6d %-22s %-6s %12.1f   %-26s %-6s %12.1f" %
              (yr, a, E[a]['position_group'], BASE[a]['total'], b, E[b]['position_group'],
               BASE[b]['total']))
    P("    the pick-1 cohort gains %.1f board points across the two rows (%.1f -> %.1f)"
      % (sum(v['delta'] for v in REPL.values()),
         sum(v['excluded_value'] for v in REPL.values()),
         sum(v['replacement_value'] for v in REPL.values())))
    P()


# ==================================================================================================
# (a) THE ALL-IN PICK CURVE
# ==================================================================================================
NDROWS = [dict(key=k, pick=ATTR[k]['pick'], natural_pick=ATTR[k]['natural_pick'],
               slid=ATTR[k]['slid'], value=BASE[k]['total'], pos=E[k]['position_group'],
               entry=E[k]['entry_year'], tier=E[k]['window_tier'])
          for k in L2['fit_nd_keys']]

# ==================================================================================================
# CORRECTION 26B-C1 -- THE RULING BECOMES AN ASSERT.  Each limb is able to fire, and the deriver
# HALTS on any violation rather than reporting a curve built on a broken exclusion.
# ==================================================================================================
FM_KEYS = set(FM['excluded_keys']); FM_YEARS = set(FM['slide_years'])
_ALLCOHORT = set(L2['fit_nd_keys']) | set(L2['fit_pool_keys'])

# (a) the two excluded keys appear in NO cohort input, at any pick, on either arm
_leak = sorted(FM_KEYS & _ALLCOHORT)
assert not _leak, ("26B-C1 ASSERT (a) FAILED: force-majeure keys present in a cohort input: %s" % _leak)
_leakpick = sorted(k for k in FM_KEYS if ATTR.get(k, {}).get('pick') is not None)
assert not _leakpick, ("26B-C1 ASSERT (a) FAILED: a force-majeure key still carries a cohort pick: %s"
                       % _leakpick)

# (b) in each slide year, the pick-N cohort contains the NATURAL pick-(N+1) entrant
_bypick = collections.defaultdict(dict)
for r in NDROWS:
    _bypick[r['entry']][r['pick']] = r
_C1B = {}
for yr in sorted(FM_YEARS):
    nat = {ATTR[k]['natural_pick']: k for k in ATTR
           if E[k]['entry_year'] == yr and E[k]['type'] == 'ND' and ATTR[k]['natural_pick']}
    checked = 0
    for N in range(1, 65):
        want = nat.get(N + 1)
        if want is None: continue
        got = _bypick.get(yr, {}).get(N)
        assert got is not None and got['key'] == want, (
            "26B-C1 ASSERT (b) FAILED: %d slid pick %d should hold the natural pick-%d entrant %s, "
            "holds %s" % (yr, N, N + 1, want, (got or {}).get('key')))
        checked += 1
    _C1B[yr] = checked
assert all(v > 0 for v in _C1B.values()), "26B-C1 ASSERT (b) is VACUOUS -- it checked nothing"

# (c) a natural pick 65 in a slide year is in the ND fit and absent from the ND>64 pathway.
#     MEASURED, not assumed: the 2013 national draft ENDS AT NATURAL PICK 61, so it HAS no natural
#     65. The assert is written over the natural-65s that exist, and it records which years have one
#     -- asserting two would be asserting a fact about the world that is false.
_POOLSET = set(L2['fit_pool_keys'])
_C1C = {}
for yr in sorted(FM_YEARS):
    n65 = [k for k in ATTR if E[k]['entry_year'] == yr and E[k]['type'] == 'ND'
           and ATTR[k]['natural_pick'] == 65]
    for k in n65:
        assert ATTR[k]['pick'] == 64 and ATTR[k]['mechanism'] == 'ND 1-64', (
            "26B-C1 ASSERT (c) FAILED: natural 65 %s did not slide into the ND fit (pick %s, mech %s)"
            % (k, ATTR[k]['pick'], ATTR[k]['mechanism']))
        assert k not in _POOLSET, (
            "26B-C1 ASSERT (c) FAILED: natural 65 %s is still in the ND>64 pool pathway" % k)
        assert k in set(L2['fit_nd_keys']), (
            "26B-C1 ASSERT (c) FAILED: natural 65 %s is not in the ND fit population" % k)
    _C1C[yr] = n65
assert any(_C1C.values()), ("26B-C1 ASSERT (c) is VACUOUS -- no slide year has a natural pick 65, so "
                            "the limb never engaged; if that is genuinely true the ruling's 65-clause "
                            "needs re-reading, not silent passing")
_MAXNAT = {yr: max((ATTR[k]['natural_pick'] for k in ATTR if E[k]['entry_year'] == yr
                    and E[k]['type'] == 'ND' and ATTR[k]['natural_pick']), default=None)
           for yr in sorted(FM_YEARS)}
report_c1()          # printed only now: the three asserts above have run and passed
PICKS = list(range(1, 65))
byp = collections.defaultdict(list)
for r in NDROWS: byp[r['pick']].append(r['value'])
RAWMEAN = {p: (sum(byp[p]) / len(byp[p]) if byp.get(p) else 0.0) for p in PICKS}
NPICK = {p: len(byp.get(p, [])) for p in PICKS}

# CORRECTION 26B-C2 -- the estimator is now the LOCAL-LINEAR fit (owner ruling 5275737926). The
# weighted-mean (local-constant) curve is still computed, because the three-way comparison table is a
# deliverable of the correction order and because a boundary claim needs both numbers beside it.
wmean, wmeff = HP.kernel_raw(NDROWS, PICKS)                       # the SHIPPED local-constant estimator
raw, effn, LLDIAG = LL.kernel_loclin(NDROWS, PICKS, HP.NMIN, HP.HMIN, HP.HMAX)
WMEAN = {p: wmean[i] for i, p in enumerate(PICKS)}
PRE_ANCHOR_PICK1 = raw[0]
PRE_ANCHOR_PICK1_WMEAN = wmean[0]
ANCHOR_FACTOR = PIN1 / PRE_ANCHOR_PICK1
ALLIN = {p: raw[i] * ANCHOR_FACTOR for i, p in enumerate(PICKS)}
ALLIN_RAW = {p: raw[i] for i, p in enumerate(PICKS)}
DIAG = {p: LLDIAG[i] for i, p in enumerate(PICKS)}
_fb = [p for p in PICKS if DIAG[p]['fallback']]
_fl = [p for p in PICKS if DIAG[p]['floored']]

P("-" * 118)
P("(a) THE ALL-IN PICK CURVE  --  ND 1-64, entries 2004-2021, busts at 0, delivered value discounted")
P("    to acquisition in board points.  n = %d careers." % len(NDROWS))
P("-" * 118)
P("  ESTIMATOR (CORRECTION 26B-C2, owner ruling #334 comment 5275737926): LOCAL-LINEAR over log(pick),")
P("  applied across the WHOLE curve, picks 1-64 -- one method, no seam. Same Gaussian kernel and same")
P("  bandwidth-growth rule as the shipped aggregator; the solver is the engine's own")
P("  par_build.py::loclin algebra (fsum normal equations, LU with partial pivoting, rank-deficient")
P("  fallback to the local-constant weighted mean at relcond < 1e-9), reused and cited, not reinvented.")
P("  rank-deficient fallbacks fired at picks: %s" % (_fb or 'NONE'))
P("  negative fits floored at 0 at picks:     %s" % (_fl or 'NONE'))
P()
P("  PRE-ANCHOR SCALE at pick 1:  LOCLIN %.1f  (weighted-mean %.1f, raw cohort mean %.1f)"
  % (PRE_ANCHOR_PICK1, PRE_ANCHOR_PICK1_WMEAN, RAWMEAN[1]))
P("  ANCHORING FACTOR to pin pick 1 = 3000 (Ruling 6): x %.4f   (weighted-mean would give x %.4f)"
  % (ANCHOR_FACTOR, PIN1 / PRE_ANCHOR_PICK1_WMEAN))
P("  This SUBSUMES the smoothed-vs-raw anchor question (landing ruling #5): the anchor now reads the")
P("  LOCLIN value at pick 1 -- principled, not special-cased.")
P("  raw per-pick cohort means are printed BESIDE the fitted curve, as PREREG P2.6 pre-committed.")
P()
P("  %5s %6s %12s %12s %12s %12s %12s %10s %7s %7s %7s" %
  ('pick', 'n', 'raw mean', 'wtd-mean', 'LOCLIN', 'ANCHORED', 'today PVC', 'der/PVC',
   'h', 'effn', 'borrow'))
for p in PICKS:
    d = DIAG[p]
    P("  %5d %6d %12.1f %12.1f %12.1f %12.1f %12.0f %10.4f %7.2f %7.1f %6.1f%%" %
      (p, NPICK[p], RAWMEAN[p], WMEAN[p], ALLIN_RAW[p], ALLIN[p], PVC.get(p, float('nan')),
       ALLIN[p] / PVC[p] if PVC.get(p) else float('nan'),
       d['h'], d['effn'], 100 * d['borrowed_share']))
P()
P("  THE THREE-WAY TABLE AT THE HEADLINE PICKS  --  both BOUNDARY REGIONS marked")
P("  %6s %12s %12s %12s %10s %10s   %s" %
  ('pick', 'raw cohort', 'wtd-mean', 'LOCLIN', 'LL-WM', 'LL/WM', 'region'))
for p in [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 64]:
    reg = ('<<< NORTH BOUNDARY' if p <= 3 else ('>>> SOUTH BOUNDARY' if p >= 50 else ''))
    P("  %6d %12.1f %12.1f %12.1f %+10.1f %10.4f   %s"
      % (p, RAWMEAN[p], WMEAN[p], ALLIN_RAW[p], ALLIN_RAW[p] - WMEAN[p],
         ALLIN_RAW[p] / WMEAN[p] if WMEAN[p] else float('nan'), reg))
P("  the boundary correction, stated as one number per end:")
P("    pick  1  LOCLIN/wtd-mean %.4f  (%+.1f%%)   -- the north end, previously dragged DOWN"
  % (ALLIN_RAW[1] / WMEAN[1], 100 * (ALLIN_RAW[1] / WMEAN[1] - 1)))
P("    pick 64  LOCLIN/wtd-mean %.4f  (%+.1f%%)   -- the south end, previously FLATTERED UP"
  % (ALLIN_RAW[64] / WMEAN[64], 100 * (ALLIN_RAW[64] / WMEAN[64] - 1)))
P()
P("  FULL PER-PICK CURVE (anchored), for the record")
P("  %5s %6s %12s %12s %12s %12s %10s" %
  ('pick', 'n', 'raw mean', 'LOCLIN', 'ANCHORED', 'today PVC', 'der/PVC'))
for p in PICKS:
    P("  %5d %6d %12.1f %12.1f %12.1f %12.0f %10.4f" %
      (p, NPICK[p], RAWMEAN[p], ALLIN_RAW[p], ALLIN[p], PVC.get(p, float('nan')),
       ALLIN[p] / PVC[p] if PVC.get(p) else float('nan')))

P()
P("  TAIL SHARE OF THE CURVE ITSELF (Ruling 8's disclosure, VALUE-WEIGHTED -- the honest aggregate:")
P("  a per-player mean tail share understates how much of a COHORT MEAN is projection, because the")
P("  live young careers that carry tails are also the big ones).")
P("  %-8s %6s %12s %12s %10s   %s" % ('band', 'n', 'sum total', 'sum tail', 'tail wt%', 'per-player median'))
NDTAIL = {}
for lo, hi in BANDS:
    sub = [r for r in NDROWS if lo <= r['pick'] <= hi]
    st = sum(BASE[r['key']]['total'] for r in sub)
    sl = sum(BASE[r['key']]['tail'] for r in sub)
    med = q([BASE[r['key']]['tail_share'] for r in sub if BASE[r['key']]['total'] > 0], .50)
    NDTAIL['%d-%d' % (lo, hi)] = dict(n=len(sub), total=st, tail=sl,
                                      weighted=(sl / st if st else 0.0), median_player=med)
    P("  %-8s %6d %12.0f %12.0f %9.1f%%   %.4f"
      % ('%d-%d' % (lo, hi), len(sub), st, sl, 100 * (sl / st if st else 0), med))
_st = sum(BASE[r['key']]['total'] for r in NDROWS); _sl = sum(BASE[r['key']]['tail'] for r in NDROWS)
NDTAIL['ALL'] = dict(n=len(NDROWS), total=_st, tail=_sl, weighted=_sl / _st,
                     median_player=q([BASE[r['key']]['tail_share'] for r in NDROWS
                                      if BASE[r['key']]['total'] > 0], .50))
P("  %-8s %6d %12.0f %12.0f %9.1f%%   %.4f"
  % ('ALL 1-64', len(NDROWS), _st, _sl, 100 * _sl / _st, NDTAIL['ALL']['median_player']))
P("  by tier: core<=2014 %.1f%%   augmented 2015-2021 %.1f%%   (2022+ is EXCLUDED from the curve)"
  % (100 * sum(BASE[r['key']]['tail'] for r in NDROWS if r['tier'] == 'core<=2014')
     / max(1e-9, sum(BASE[r['key']]['total'] for r in NDROWS if r['tier'] == 'core<=2014')),
     100 * sum(BASE[r['key']]['tail'] for r in NDROWS if r['tier'] == 'augmented2015-2021')
     / max(1e-9, sum(BASE[r['key']]['total'] for r in NDROWS if r['tier'] == 'augmented2015-2021'))))

HEAD = [1, 2, 3, 5, 7, 10, 15, 20, 30, 40, 50, 64]
P()
P("  HEADLINE PICKS")
P("  %-14s %s" % ('pick', "".join("%8d" % p for p in HEAD)))
P("  %-14s %s" % ('DERIVED', "".join("%8.0f" % ALLIN[p] for p in HEAD)))
P("  %-14s %s" % ('today PVC', "".join("%8.0f" % PVC[p] for p in HEAD)))
P("  %-14s %s" % ('ratio', "".join("%8.3f" % (ALLIN[p] / PVC[p]) for p in HEAD)))
P()
P("  SHAPE: pick1->pick3 drop  DERIVED %+.2f%%   today %+.2f%%"
  % (100 * (ALLIN[3] / ALLIN[1] - 1), 100 * (PVC[3] / PVC[1] - 1)))
P("  TOP RATIO pick1/pick10    DERIVED %.3f          today %.3f"
  % (ALLIN[1] / ALLIN[10], PVC[1] / PVC[10]))
P("  DEEP TAIL pick64/pick1    DERIVED %.4f         today %.4f"
  % (ALLIN[64] / ALLIN[1], PVC[64] / PVC[1]))
cross = [p for p in PICKS if ALLIN[p] > PVC[p]]
P("  CROSSING (derived first rises above today's curve): pick %s"
  % (cross[0] if cross else 'never'))
mono = [p for p in PICKS[1:] if ALLIN[p] > ALLIN[p - 1] + 1e-9]
P("  MONOTONICITY: the derived curve is %s over picks 1-64 (%d ascents)%s"
  % ('strictly non-increasing' if not mono else 'NOT monotone', len(mono),
     ('' if not mono else '  ascents at picks %s' % mono[:12])))
P("  NOTE: no isotonic step is applied. The shipped fitter PAVA-projects and then HARD-SETS pick 1;")
P("        this derivation reports what the data says and anchors by a single scalar, so that the")
P("        anchoring factor is legible as one number (Ruling 13's 'pre-anchor scale reported').")

# ==================================================================================================
# (b) POSITIONAL ND RELATIVITIES + THE RECONCILIATION LAW
# ==================================================================================================
P()
P("-" * 118)
P("(b) POSITIONAL ND RELATIVITIES BY PICK BAND  --  position = the ACQUISITION SLOT (day-0), Ruling 5")
P("-" * 118)
POSROWS = {g: [r for r in NDROWS if r['pos'] == g] for g in POSN}
NOPOS = [r for r in NDROWS if r['pos'] not in POSN]
P("  rows by day-0 position: %s   (unmapped day-0 position: %d, excluded from the positional split)"
  % ({g: len(POSROWS[g]) for g in POSN}, len(NOPOS)))

SHARE = {}
for g in POSN:
    ind = [dict(key=r['key'], pick=r['pick'], value=(1.0 if r['pos'] == g else 0.0)) for r in NDROWS]
    # THE POSITION SHARES STAY ON THE LOCAL-CONSTANT WEIGHTED MEAN. DECLARED, with the reason: a share
    # is a bounded PROPORTION, and a local-linear extrapolation of an indicator can leave [0,1] at a
    # boundary, which would then have to be clipped -- reintroducing a boundary artefact of a different
    # kind. The C2 ruling is about the declining VALUE curve's boundary bias; the shares are
    # renormalised to sum to 1 at every pick regardless, so a first-order slope term in them cancels.
    s, _ = HP.kernel_raw(ind, PICKS)
    SHARE[g] = {p: s[i] for i, p in enumerate(PICKS)}
# renormalise the shares to sum to 1 at every pick (the unmapped rows carry the remainder)
for p in PICKS:
    tot = sum(SHARE[g][p] for g in POSN)
    for g in POSN: SHARE[g][p] = SHARE[g][p] / tot if tot else 0.0

RAWPOS = {}
POSFB = {}
for g in POSN:
    if len(POSROWS[g]) < 2:
        RAWPOS[g] = {p: ALLIN_RAW[p] for p in PICKS}; POSFB[g] = []; continue
    # the positional VALUE curves take the C2 local-linear estimator too -- same method as the all-in
    # curve, so the relativities carry no seam against it.
    nm = min(HP.NMIN, max(8.0, len(POSROWS[g]) / 4.0))
    v, _e, dg = LL.kernel_loclin(POSROWS[g], PICKS, nm, HP.HMIN, HP.HMAX)
    RAWPOS[g] = {p: v[i] for i, p in enumerate(PICKS)}
    POSFB[g] = [PICKS[i] for i, d in enumerate(dg) if d['fallback'] or d['floored']]

# THE RECONCILIATION LAW, IMPOSED BY CONSTRUCTION AND THEN ASSERTED:
#   V_g(p) = ALLIN(p) * rawpos_g(p) / sum_h share_h(p) rawpos_h(p)
#   =>  sum_g share_g(p) V_g(p) == ALLIN(p) exactly.
POSV = {g: {} for g in POSN}
for p in PICKS:
    nrm = sum(SHARE[g][p] * RAWPOS[g][p] for g in POSN)
    for g in POSN:
        POSV[g][p] = ALLIN[p] * RAWPOS[g][p] / nrm if nrm else ALLIN[p]

RECON_MAX = 0.0
for p in PICKS:
    lhs = sum(SHARE[g][p] * POSV[g][p] for g in POSN)
    RECON_MAX = max(RECON_MAX, abs(lhs / ALLIN[p] - 1.0))
assert RECON_MAX < 1e-12, ("RULING 13 RECONCILIATION LAW BREACHED at %.3e -- this is a HALT, not a "
                           "tolerance" % RECON_MAX)
P("  RECONCILIATION LAW (Ruling 13): position-weighted mean == all-in at EVERY pick.")
P("     max |weighted mean / all-in - 1| over picks 1-64 = %.3e   ASSERTED IN CODE (halt, not"
  % RECON_MAX)
P("     tolerance). The law holds BY CONSTRUCTION -- the positional curves are renormalised onto the")
P("     all-in at each pick -- and the assert exists so a future change that breaks it cannot ship.")
P()
P("  RELATIVITIES (V_pos(pick) / all-in(pick)) BY PICK BAND, and the positional values themselves")
P("  %-6s %10s %10s %10s %10s %10s %10s   %10s" %
  ('band', 'MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK', 'all-in'))
BANDTAB = {}
for lo, hi in BANDS:
    ps = [p for p in PICKS if lo <= p <= hi]
    a = sum(ALLIN[p] for p in ps) / len(ps)
    row = {}
    for g in POSN:
        row[g] = (sum(POSV[g][p] for p in ps) / len(ps)) / a
    BANDTAB['%d-%d' % (lo, hi)] = dict(allin=a, rel=row,
                                       val={g: sum(POSV[g][p] for p in ps) / len(ps) for g in POSN},
                                       n={g: sum(1 for r in POSROWS[g] if lo <= r['pick'] <= hi)
                                          for g in POSN})
    P("  %-6s %10.3f %10.3f %10.3f %10.3f %10.3f %10.3f   %10.0f"
      % ('%d-%d' % (lo, hi), row['MID'], row['SD'], row['SF'], row['KPD'], row['KPF'], row['RUCK'], a))
P("  %-6s %10s %10s %10s %10s %10s %10s" % ('n', *[
    "%d" % sum(1 for r in POSROWS[g]) for g in POSN]))

# ==================================================================================================
# (c) THE POOL LADDERS
# ==================================================================================================
P()
P("-" * 118)
P("(c) POOL PATHWAY ALL-INS AND POSITIONAL v0s  --  Ruling 12's BORROWING LADDER, K=%d" % K_SHRINK)
P("-" * 118)
POOLROWS = [dict(key=k, mech=ATTR[k]['mechanism'], pos=E[k]['position_group'],
                 value=BASE[k]['total'], obs=BASE[k]['obs'], entry=E[k]['entry_year'])
            for k in L2['fit_pool_keys']]


def allin_of(rows):
    vs = [r['value'] for r in rows]
    return (sum(vs) / len(vs) if vs else 0.0), len(vs), disp(vs)


ALLPOOL, N_ALLPOOL, D_ALLPOOL = allin_of(POOLROWS)
POOL_BY_POS = {}
for g in POSN:
    sub = [r for r in POOLROWS if r['pos'] == g]
    POOL_BY_POS[g] = allin_of(sub)
LENS = {g: (POOL_BY_POS[g][0] / ALLPOOL if ALLPOOL else 1.0) for g in POSN}

P("  ALL-POOL all-in            %s" % dstr(D_ALLPOOL))
P("  ALL-POOL POSITIONAL LENS (rung-2's lens; mean_pos / all-pool mean)")
P("    %-6s %8s %12s %12s %12s %12s %8s" % ('pos', 'n', 'mean', 'p05', 'median', 'p95', 'lens'))
for g in POSN:
    m, n, d = POOL_BY_POS[g]
    P("    %-6s %8d %12.1f %12.1f %12.1f %12.1f %8.4f"
      % (g, n, d['mean'], d['p05'], d['median'], d['p95'], LENS[g]))

PATH = {}
for m in POOLM:
    sub = [r for r in POOLROWS if r['mech'] == m]
    a, n, d = allin_of(sub)
    w = n / float(n + K_SHRINK)
    PATH[m] = dict(raw=a, n=n, disp=d, w=w, shrunk=w * a + (1 - w) * ALLPOOL,
                   borrow=1 - w)

# ND-pick equivalent: the pick whose ANCHORED all-in curve equals the pathway all-in (same anchor
# factor applied to the pathway value, so both sides are in the same currency).
def nd_equiv(v):
    a = v * ANCHOR_FACTOR
    if a >= ALLIN[1]: return '<1'
    for p in PICKS:
        if ALLIN[p] <= a:
            return str(p)
    return '>64 (below the pick-64 value %.0f)' % ALLIN[64]


P()
P("  PATHWAY ALL-INS (entries 2004-2021, busts at 0), with ND-pick equivalents on the ANCHORED curve")
P("  %-7s %6s %11s %10s %10s %11s %11s %8s %8s %s" %
  ('path', 'n', 'raw all-in', 'p05', 'median', 'p95', 'shrunk', 'borrow', 'anchored', 'ND-pick equiv'))
for m in sorted(POOLM, key=lambda x: -PATH[x]['raw']):
    e = PATH[m]; d = e['disp']
    P("  %-7s %6d %11.1f %10.1f %10.1f %11.1f %11.1f %7.1f%% %8.0f  %s"
      % (m, e['n'], e['raw'], d['p05'], d['median'], d['p95'], e['shrunk'],
         100 * e['borrow'], e['shrunk'] * ANCHOR_FACTOR, nd_equiv(e['shrunk'])))
P("  ND 1-64 (reference)  n=%d  raw all-in %.1f  anchored %.0f  == the curve's own population"
  % (len(NDROWS), sum(r['value'] for r in NDROWS) / len(NDROWS),
     (sum(r['value'] for r in NDROWS) / len(NDROWS)) * ANCHOR_FACTOR))

P()
P("  THE BORROWING LADDER, CELL BY CELL  (own cell -> pathway-all-in x all-pool lens -> all-pool)")
P("  rung 1 = the cell's own mean.  rung 2 = shrunk pathway all-in x the all-pool positional lens.")
P("  rung 3 = the all-pool all-in (rung 2 collapses to it when the pathway itself is thin).")
P("  cell weight w = n/(n+K); BORROWING SHARE = 1 - w, i.e. the share of the printed v0 that did NOT")
P("  come from the cell's own careers.  TOTAL borrowing compounds the pathway rung's own borrowing.")
P()
P("  %-7s %-5s %5s %11s %11s %11s %8s %8s %9s" %
  ('path', 'pos', 'n', 'own cell', 'rung2', 'v0 (raw)', 'borrow', 'from pool', 'anchored'))
CELLS = {}
for m in POOLM:
    for g in POSN:
        sub = [r for r in POOLROWS if r['mech'] == m and r['pos'] == g]
        n = len(sub)
        own = (sum(r['value'] for r in sub) / n) if n else None
        rung2 = PATH[m]['shrunk'] * LENS[g]
        w = n / float(n + K_SHRINK)
        v0 = w * (own if own is not None else 0.0) + (1 - w) * rung2
        # PROVENANCE OF THE CELL'S v0, in three exhaustive shares that sum to 1:
        #   own_share  = w                      -- this cell's own careers
        #   path_share = (1-w) * PATH.w         -- the pathway's OTHER positions, through rung 2
        #   pool_share = (1-w) * (1 - PATH.w)   -- the whole pool, through rung 3
        own_share = w
        path_share = (1 - w) * PATH[m]['w']
        pool_share = (1 - w) * PATH[m]['borrow']
        CELLS[(m, g)] = dict(n=n, own=own, rung2=rung2, v0=v0, w=w,
                             borrow=1 - w, own_share=own_share,
                             path_share=path_share, pool_share=pool_share,
                             anchored=v0 * ANCHOR_FACTOR,
                             disp=disp([r['value'] for r in sub]) if n else None)
        P("  %-7s %-5s %5d %11s %11.1f %11.1f %7.1f%% %7.1f%% %9.0f"
          % (m, g, n, ("%.1f" % own) if own is not None else '   --   ', rung2, v0,
             100 * (1 - w), 100 * pool_share, v0 * ANCHOR_FACTOR))
P()
P("  BORROWING SUMMARY (share of each cell's v0 NOT from its own careers)")
P("  %-7s %s" % ('path', "".join("%8s" % g for g in POSN)))
for m in POOLM:
    P("  %-7s %s" % (m, "".join("%7.0f%%" % (100 * CELLS[(m, g)]['borrow']) for g in POSN)))

# ==================================================================================================
# (d) THE MSD / YOUNG-PATHWAY QUESTION, BOTH WAYS
# ==================================================================================================
P()
P("-" * 118)
P("(d) THE MSD / YOUNG-PATHWAY QUESTION, BOTH WAYS")
P("-" * 118)
P("  WAY A -- AUGMENTED GATED TAILS. MSD's own careers are scored with their projected tails, and the")
P("           pathway all-in is that mean. The tails are the thinnest-evidence objects in the order.")
P("  WAY B -- STRUCTURAL BORROWING. MSD's careers are scored OBSERVED-ONLY (no tail at all); the")
P("           positional cells are then built from the all-pool position curves times an MSD pathway")
P("           OFFSET (offset = MSD observed-only all-in / all-pool observed-only all-in), so MSD")
P("           never prices off its own projections.")


def obs_allin(rows):
    vs = [r['obs'] for r in rows]
    return (sum(vs) / len(vs) if vs else 0.0), len(vs), disp(vs)


MSD = [r for r in POOLROWS if r['mech'] == 'MSD']
MSD_A, nA, dA = allin_of(MSD)
MSD_B_raw, nB, dB = obs_allin(MSD)
POOL_B, _, dPB = obs_allin(POOLROWS)
OFFSET = MSD_B_raw / POOL_B if POOL_B else 0.0
POOL_B_POS = {g: obs_allin([r for r in POOLROWS if r['pos'] == g])[0] for g in POSN}

tail_shares = [BASE[r['key']]['tail_share'] for r in MSD if BASE[r['key']]['total'] > 0]
dts = disp(tail_shares)
P()
P("  MSD population in the fit window: n=%d" % nA)
P("  MSD tail shares: mean %.4f  p05 %.4f  median %.4f  p95 %.4f  (n=%d live-scored)"
  % (dts['mean'], dts['p05'], dts['median'], dts['p95'], dts['n']))
MSD_TW = (sum(BASE[r['key']]['tail'] for r in MSD)
          / max(1e-9, sum(BASE[r['key']]['total'] for r in MSD)))
P("  MSD tail share VALUE-WEIGHTED: %.4f  -- this, not the per-player median, is what moves the all-in."
  % MSD_TW)
P()
P("  %-34s %11s %11s %11s %11s %10s" % ('', 'all-in', 'p05', 'median', 'p95', 'anchored'))
P("  %-34s %11.1f %11.1f %11.1f %11.1f %10.0f"
  % ('WAY A  MSD with gated tails', MSD_A, dA['p05'], dA['median'], dA['p95'], MSD_A * ANCHOR_FACTOR))
P("  %-34s %11.1f %11.1f %11.1f %11.1f %10.0f"
  % ('WAY B  MSD observed-only', MSD_B_raw, dB['p05'], dB['median'], dB['p95'],
     MSD_B_raw * ANCHOR_FACTOR))
P("  WAY A / WAY B at the all-in level: %.4f  (tails RAISE the MSD all-in by %+.1f%%)"
  % (MSD_A / MSD_B_raw if MSD_B_raw else float('nan'),
     100 * (MSD_A / MSD_B_raw - 1) if MSD_B_raw else float('nan')))
P("  ALL-POOL observed-only all-in %.1f  =>  MSD PATHWAY OFFSET = %.4f" % (POOL_B, OFFSET))
P()
P("  THE TWO MSD POSITIONAL v0 TABLES, SIDE BY SIDE")
P("  %-6s %5s %12s %12s %10s %10s" % ('pos', 'n', 'WAY A (v0)', 'WAY B (v0)', 'A/B', 'brw A'))
MSD_BOTH = {}
for g in POSN:
    a = CELLS[('MSD', g)]['v0']
    b = POOL_B_POS[g] * OFFSET
    MSD_BOTH[g] = dict(A=a, B=b, ratio=(a / b if b else float('nan')),
                       A_anch=a * ANCHOR_FACTOR, B_anch=b * ANCHOR_FACTOR,
                       n=CELLS[('MSD', g)]['n'], borrow_A=CELLS[('MSD', g)]['borrow'])
    P("  %-6s %5d %12.1f %12.1f %10.4f %9.0f%%"
      % (g, MSD_BOTH[g]['n'], a, b, MSD_BOTH[g]['ratio'], 100 * MSD_BOTH[g]['borrow_A']))
P()
P("  RECOMMENDATION -- see DERIVE.json::msd.recommendation and the packet. PREREG §4 P4.2 pre-committed")
P("  to STRUCTURAL BORROWING before any of these numbers existed; the scoring is in the packet.")

# ==================================================================================================
OUT = dict(
    pins={k: (os.path.relpath(p, ROOT), _md5(p)) for k, (p, _e) in PINS.items()},
    smoother=dict(file='docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py',
                  md5=_md5(HARN), fn='kernel_raw', nmin=HP.NMIN, hmin=HP.HMIN, hmax=HP.HMAX,
                  form='Gaussian kernel over log(pick), bandwidth grown until effective n>=NMIN, '
                       'then a weighted mean'),
    correction_26b_c2=dict(
        provenance=LL.PROVENANCE, estimator='local-linear over log(pick), whole curve 1-64',
        weighted_mean_curve=WMEAN, loclin_curve=ALLIN_RAW, raw_cohort_mean=RAWMEAN,
        pre_anchor_loclin=PRE_ANCHOR_PICK1, pre_anchor_weighted_mean=PRE_ANCHOR_PICK1_WMEAN,
        pre_anchor_raw=RAWMEAN[1], anchor_factor_loclin=ANCHOR_FACTOR,
        anchor_factor_weighted_mean=PIN1 / PRE_ANCHOR_PICK1_WMEAN,
        diagnostics=DIAG, rank_deficient_fallback_picks=_fb, floored_picks=_fl,
        positional_fallback_picks=POSFB,
        shares_estimator='local-constant weighted mean, DECLARED -- a share is a bounded proportion'),
    curve=dict(picks=PICKS, n_per_pick=NPICK, raw_mean=RAWMEAN, smoothed=ALLIN_RAW,
               weighted_mean=WMEAN,
               anchored=ALLIN, pre_anchor_pick1=PRE_ANCHOR_PICK1, anchor_factor=ANCHOR_FACTOR,
               pvc_today=PVC, n_population=len(NDROWS),
               crossing_pick=(cross[0] if cross else None), monotone_ascents=mono,
               tail_share_by_band=NDTAIL),
    positional=dict(share=SHARE, raw=RAWPOS, value=POSV, bands=BANDTAB,
                    reconciliation_max_abs_rel_error=RECON_MAX,
                    n_by_pos={g: len(POSROWS[g]) for g in POSN}, n_unmapped=len(NOPOS)),
    pool=dict(all_pool=ALLPOOL, all_pool_disp=D_ALLPOOL, lens=LENS,
              by_pos={g: dict(mean=POOL_BY_POS[g][0], n=POOL_BY_POS[g][1], disp=POOL_BY_POS[g][2])
                      for g in POSN},
              pathways=PATH, K=K_SHRINK,
              cells={('%s|%s' % k): v for k, v in CELLS.items()},
              nd_equiv={m: nd_equiv(PATH[m]['shrunk']) for m in POOLM}),
    msd=dict(way_a=dict(all_in=MSD_A, disp=dA, n=nA),
             way_b=dict(all_in=MSD_B_raw, disp=dB, n=nB, offset=OFFSET,
                        all_pool_observed=POOL_B, by_pos=POOL_B_POS),
             tail_shares=dts, tail_share_value_weighted=MSD_TW, both=MSD_BOTH,
             recommendation='STRUCTURAL BORROWING (WAY B) -- see SHIPPING_PACKET_26B.md'),
    anchor_factor=ANCHOR_FACTOR,
    correction_26b_c1=dict(config=FM, asserts_passed=['a: excluded keys absent from every cohort',
                                                      'b: slid pick-N holds natural pick-(N+1)',
                                                      'c: a natural 65 enters the ND fit and leaves ND>64'],
                           picks_checked_b=_C1B, natural_65_by_year=_C1C,
                           max_natural_pick_by_year=_MAXNAT, replacements=REPL,
                           nd_gt64_entrants_moved=sum(len(v) for v in _C1C.values())))
json.dump(OUT, open(os.path.join(HERE, 'DERIVE.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'DERIVE_out.txt'), 'w').write("\n".join(LOG) + "\n")
P()
P("wrote DERIVE.json / DERIVE_out.txt")
open(os.path.join(HERE, 'DERIVE_out.txt'), 'w').write("\n".join(LOG) + "\n")
