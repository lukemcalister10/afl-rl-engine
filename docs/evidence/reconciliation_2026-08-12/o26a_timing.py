"""ORDER 26A -- THE TIMING SEPARATION. Read-only.

o26a_wedge.py section E showed the post-entry residual moving a long way when the axis is switched
from calendar to career age. MOST OF THAT MOVE IS NOT TIMING. The career-age axis silently drops
every row that NEVER PLAYED -- and the arms lose very different shares to that (NATIONAL keeps
1250/1443 = 86.6%, RD keeps 379/691 = 54.8%). Reading it as a timing effect would credit the pool
with a survivorship windfall.

This file separates the two properly:
  F1  COMPOSITION control -- calendar axis, both arms restricted to EVER-PLAYED rows only.
  F2  TRUE TIMING -- the career-age composition of each arm's survivors at calendar N=4, and the
      NATIONAL yardstick REWEIGHTED onto the pool's own career-age composition. The difference
      between the yardstick as-read and the yardstick reweighted IS the timing leg (iii), and
      nothing else is.
  F3  the clean three-way decomposition that follows.

    usage: python o26a_timing.py <matrix.json> <out.json>
"""
import sys, json, os, math, collections, statistics

MATRIX = sys.argv[1]; OUTJS = sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
L = []
def P(s=''):
    print(s); L.append(s)

M = json.load(open(MATRIX)); R = M['recs']

def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)

def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t

ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

_V2 = json.load(open(ROOT + '/engine/rl_after/pvc_curve_v2.json'))
CUR = _V2['pool_levels']
LEVI = {k: int(float(v)) for k, v in CUR['signed_flat'].items()}
LEVI['ND65+'] = int(float(CUR['signed_nd65_plus']['measured_k15']))
for k, v in CUR['signed_rd_positional'].items(): LEVI['RD:' + k] = int(float(v))
PL_F = float(json.load(open(ROOT + '/engine/rl_after/pick_redenomination.json'))['factor'])

def division(r):
    t = r.get('type')
    if t == 'RD': return 'RD:' + r['pos']
    if t == 'ND': return 'ND65+'
    return t

def anchor_of(r):
    if r.get('is_pool_engine'):
        d = division(r)
        if d in LEVI: return LEVI[d] * PL_F
    return float(r['v0'])

def v0_of(r): return float(r['v0'])

def mark_at(r, Y):
    if Y > W: return None
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0
    if Y < yrs[0]: return None
    if Y > yrs[-1]: return 0.0
    v = vp[yrs.index(Y)]
    return 0.0 if v is None else float(v)

def firstplay(r):
    s = [x for x in (r.get('seasons') or []) if x.get('games', 0) > 0]
    return min(x['year'] for x in s) if s else None

ND = [r for r in elig if not r.get('is_pool_engine') and r.get('type') == 'ND'
      and r.get('raw_pick') and 1 <= r['raw_pick'] <= 64]
POOL = [r for r in elig if stream(r) in ORDER]
RD = [r for r in elig if stream(r) == 'RD']

def ratio(pop, Yof, DN, surv):
    num = den = 0.0; n = 0
    for r in pop:
        Y = Yof(r)
        if Y is None: continue
        v = mark_at(r, Y)
        if v is None: continue
        if surv and v <= 0: continue
        num += v; den += DN(r); n += 1
    return ((num / den) if den else float('nan'), n)

P("=" * 118)
P("ORDER 26A -- THE TIMING SEPARATION (supplement to WEDGE section E)")
P("=" * 118)
P()
P("-" * 118)
P("F1. COMPOSITION CONTROL -- why the career-age axis looked like a huge timing effect")
P("-" * 118)
F1 = {}
for nm, pop in [('NATIONAL', ND), ('ALL POOL', POOL), ('RD', RD)]:
    ever = sum(1 for r in pop if firstplay(r) is not None)
    P("  %-9s  n=%4d   ever played %4d (%5.1f%%)   NEVER played %4d (%5.1f%%)"
      % (nm, len(pop), ever, 100.0 * ever / len(pop), len(pop) - ever,
         100.0 * (len(pop) - ever) / len(pop)))
    F1[nm] = dict(n=len(pop), ever=ever, never=len(pop) - ever)
P()
P("  The career-age axis has no year for a man who never played, so he leaves it. RD loses 45.2%%")
P("  of its rows that way and NATIONAL only 13.4%%. That is a COMPOSITION effect, not timing.")
P()
P("  CALENDAR N=4, BOTH ARMS RESTRICTED TO EVER-PLAYED ROWS (the like-for-like control):")
Yof4 = lambda r: cohort(r) + 3
EVER_ND = [r for r in ND if firstplay(r) is not None]
EVER_RD = [r for r in RD if firstplay(r) is not None]
CTL = {}
for nm, pop, DN, tag in [('NATIONAL ever-played', EVER_ND, v0_of, 'nd'),
                         ('RD ever-played @v0', EVER_RD, v0_of, 'rd_v0'),
                         ('RD ever-played @anchor', EVER_RD, anchor_of, 'rd_anchor')]:
    a, na = ratio(pop, Yof4, DN, False); s, ns = ratio(pop, Yof4, DN, True)
    P("    %-24s  ALL %8.4f (n=%4d)   SURV %8.4f (n=%4d)" % (nm, a, na, s, ns))
    CTL[tag] = dict(all=a, n_all=na, surv=s, n_surv=ns)
P()
P("    wedge on ever-played, ALL      : ND %.4f / RD@v0 %.4f = %.3fx ; after entry fix ND/RD@anchor = %.3fx"
  % (CTL['nd']['all'], CTL['rd_v0']['all'], CTL['nd']['all'] / CTL['rd_v0']['all'],
     CTL['nd']['all'] / CTL['rd_anchor']['all']))
P("    wedge on ever-played, SURVIVORS: ND %.4f / RD@v0 %.4f = %.3fx ; after entry fix ND/RD@anchor = %.3fx"
  % (CTL['nd']['surv'], CTL['rd_v0']['surv'], CTL['nd']['surv'] / CTL['rd_v0']['surv'],
     CTL['nd']['surv'] / CTL['rd_anchor']['surv']))
P()

# =======================================================================================
P("-" * 118)
P("F2. THE TRUE TIMING LEG -- the career-age composition of each arm's SURVIVORS at calendar N=4,")
P("    and the NATIONAL yardstick reweighted onto the pool's own composition.")
P("-" * 118)
def agecomp(pop, DN):
    """entry-weighted career-age composition of the rows ALIVE at calendar N=4."""
    w = collections.Counter(); tot = 0.0; ages = []
    for r in pop:
        Y = Yof4(r); f = firstplay(r)
        if f is None: continue
        v = mark_at(r, Y)
        if v is None or v <= 0: continue
        a = Y - f + 1
        w[a] += DN(r); tot += DN(r); ages.append(a)
    return {k: v / tot for k, v in w.items()}, (statistics.mean(ages) if ages else float('nan')), len(ages)

wnd, mnd, nnd = agecomp(ND, v0_of)
wrd, mrd, nrd = agecomp(RD, anchor_of)
P("  entry-weighted career-age mix of survivors at calendar N=4:")
P("    NATIONAL  n=%4d  mean career age %.3f   mix %s"
  % (nnd, mnd, {k: round(v, 4) for k, v in sorted(wnd.items())}))
P("    RD        n=%4d  mean career age %.3f   mix %s"
  % (nrd, mrd, {k: round(v, 4) for k, v in sorted(wrd.items())}))
P("    the pool is %.3f seasons EARLIER in career time at the same calendar year." % (mnd - mrd))
P()

# the NATIONAL survivor own-entry curve by career age (the yardstick), then reweighted
ndcurve = {}
for a in range(1, 9):
    def Y(r, a=a):
        f = firstplay(r)
        return None if f is None else f + a - 1
    v, n = ratio(ND, Y, v0_of, True)
    ndcurve[a] = dict(ratio=v, n=n)
P("  NATIONAL survivor own-entry curve by career age (the yardstick):")
P("    " + "  ".join("a%d %.4f" % (a, ndcurve[a]['ratio']) for a in range(1, 8)))
yard_asread = ndcurve[4]['ratio']
yard_rw = sum(wrd.get(a, 0.0) * ndcurve[a]['ratio'] for a in ndcurve if a in wrd)
_norm = sum(wrd.get(a, 0.0) for a in ndcurve if a in wrd)
yard_rw = yard_rw / _norm if _norm else float('nan')
yard_ndmix = sum(wnd.get(a, 0.0) * ndcurve[a]['ratio'] for a in ndcurve if a in wnd) / \
             (sum(wnd.get(a, 0.0) for a in ndcurve if a in wnd) or 1.0)
P()
P("  yardstick on the NATIONAL's own career-age mix   : %.4f" % yard_ndmix)
P("  yardstick REWEIGHTED onto the POOL's career mix  : %.4f" % yard_rw)
P("  TIMING LEG (iii) = %.4f / %.4f = %.4fx   -- this, and ONLY this, is the debut offset."
  % (yard_ndmix, yard_rw, yard_ndmix / yard_rw))
P()

# =======================================================================================
P("-" * 118)
P("F3. THE CLEAN THREE-WAY DECOMPOSITION, calendar N=4, SURVIVORS' OWN-ENTRY convention")
P("-" * 118)
nd_s, _ = ratio(ND, Yof4, v0_of, True)
rd_s_v0, _ = ratio(RD, Yof4, v0_of, True)
rd_s_an, _ = ratio(RD, Yof4, anchor_of, True)
total = nd_s / rd_s_v0
entry = rd_s_an / rd_s_v0
timing = yard_ndmix / yard_rw
marks = total / (entry * timing)
lt = math.log(total)
P("  TOTAL WEDGE           ND %.4f / RD@board-v0 %.4f            = %7.4fx  (100.0%%)" % (nd_s, rd_s_v0, total))
P("  (i)   ENTRY-INFLATION RD@anchor %.4f / RD@v0 %.4f          = %7.4fx  (%+.1f%%)"
  % (rd_s_an, rd_s_v0, entry, 100 * math.log(entry) / lt))
P("  (iii) TIMING          yardstick as-read / reweighted        = %7.4fx  (%+.1f%%)"
  % (timing, 100 * math.log(timing) / lt))
P("  (ii)  MARK-RESIDUAL   the remainder                         = %7.4fx  (%+.1f%%)"
  % (marks, 100 * math.log(marks) / lt))
P("  check: %.4f x %.4f x %.4f = %.6f  vs total %.6f  (residual %.2e)"
  % (entry, timing, marks, entry * timing * marks, total, entry * timing * marks - total))
P()
P("  A MARK-RESIDUAL BELOW 1.0 MEANS THE POOL MARKS ARE **ABOVE** THE NATIONAL YARDSTICK, NOT BELOW.")
P("  A value of %.4f means pool survivors, once entry is restated on the signed anchor, read"
  % marks)
P("  %.3fx the national survivor yardstick at matched career age." % (1.0 / marks))
P()

# the same on the all-in (dead zeroed) convention, ever-played control applied
nd_a, _ = ratio(ND, Yof4, v0_of, False)
rd_a_v0, _ = ratio(RD, Yof4, v0_of, False)
rd_a_an, _ = ratio(RD, Yof4, anchor_of, False)
tA = nd_a / rd_a_v0; eA = rd_a_an / rd_a_v0; mA = tA / (eA * timing)
P("  THE SAME, ALL-IN (dead zeroed, every row kept -- the derivation's own convention):")
P("    TOTAL %.4fx = ENTRY %.4fx x TIMING %.4fx x MARK-RESIDUAL %.4fx   (%.1f%% / %.1f%% / %.1f%%)"
  % (tA, eA, timing, mA, 100 * math.log(eA) / math.log(tA), 100 * math.log(timing) / math.log(tA),
     100 * math.log(mA) / math.log(tA)))
P()

# =======================================================================================
P("-" * 118)
P("G. THE MORTALITY IDENTITY -- why the two conventions disagree about who is suppressed")
P("-" * 118)
P("  For any arm at a given year:   ALL-IN  =  SURVIVORS' own-entry  x  SURVIVING ENTRY SHARE")
P("  (exact, because the dead contribute 0 to the numerator and their entry stays in the denominator)")
P()
MORT = {}
P("  %-26s %10s %10s %10s %10s" % ('arm @ calendar N=4', 'ALL-IN', 'SURV', 'alive share', 'check'))
P("  " + "-" * 74)
for nm, pop, DN in [('NATIONAL (v0=anchor)', ND, v0_of), ('RD @ signed anchor', RD, anchor_of),
                    ('RD @ board v0', RD, v0_of), ('ALL POOL @ signed anchor', POOL, anchor_of),
                    ('ALL POOL @ board v0', POOL, v0_of)]:
    kept = alive = 0.0; nk = na = 0
    for r in pop:
        v = mark_at(r, Yof4(r))
        if v is None: continue
        kept += DN(r); nk += 1
        if v > 0: alive += DN(r); na += 1
    sh = alive / kept if kept else float('nan')
    a_, _ = ratio(pop, Yof4, DN, False); s_, _ = ratio(pop, Yof4, DN, True)
    P("  %-26s %10.4f %10.4f %9.2f%% %10.6f" % (nm, a_, s_, 100 * sh, s_ * sh))
    MORT[nm] = dict(allin=a_, surv=s_, alive_entry_share=sh, n_kept=nk, n_alive=na,
                    entry_kept=kept, entry_alive=alive)
P()
P("  THE WHOLE STORY IN ONE LINE. At calendar N=4, on the SIGNED ANCHOR:")
_nd = MORT['NATIONAL (v0=anchor)']; _rd = MORT['RD @ signed anchor']
P("    NATIONAL  %.4f = %.4f x %.4f   (%.1f%% of national entry is still alive)"
  % (_nd['allin'], _nd['surv'], _nd['alive_entry_share'], 100 * _nd['alive_entry_share']))
P("    RD        %.4f = %.4f x %.4f   (%.1f%% of rookie entry is still alive)"
  % (_rd['allin'], _rd['surv'], _rd['alive_entry_share'], 100 * _rd['alive_entry_share']))
P("    pool survivors are marked %.3fx the national survivors' level, but only %.3fx as much of the"
  % (_rd['surv'] / _nd['surv'], _rd['alive_entry_share'] / _nd['alive_entry_share']))
P("    pool's entry survives. The two nearly cancel: %.3f x %.3f = %.3f."
  % (_rd['surv'] / _nd['surv'], _rd['alive_entry_share'] / _nd['alive_entry_share'],
     (_rd['surv'] / _nd['surv']) * (_rd['alive_entry_share'] / _nd['alive_entry_share'])))
P("    THERE IS NO MARK SUPPRESSION OF LIVING POOL PLAYERS. There is a MORTALITY GAP, and the")
P("    signed levels have already absorbed it by construction.")
P()
P("  H4 CHECK -- the owner's yardstick band for ND survivors at yr4-5 was 2.2x to 3.1x:")
for a, nmm in [(4, 'yr4'), (5, 'yr5')]:
    Yo = lambda r, a=a: cohort(r) + a - 1
    s_, n_ = ratio(ND, Yo, v0_of, True)
    P("    NATIONAL survivors' own-entry, calendar %s : %.4f  (n=%d)   %s"
      % (nmm, s_, n_, 'IN BAND' if 2.2 <= s_ <= 3.1 else 'BELOW BAND (2.2-3.1)'))
P("    career-age matched a4 %.4f  a5 %.4f   %s"
  % (ndcurve[4]['ratio'], ndcurve[5]['ratio'],
     'IN BAND' if 2.2 <= ndcurve[4]['ratio'] <= 3.1 else 'BELOW BAND (2.2-3.1)'))
P()

json.dump(dict(matrix=os.path.basename(MATRIX), composition=F1, calendar4_everplayed=CTL,
               mortality=MORT,
               age_mix=dict(national={str(k): v for k, v in wnd.items()},
                            rd={str(k): v for k, v in wrd.items()},
                            mean_age_national=mnd, mean_age_rd=mrd, offset=mnd - mrd),
               nd_career_curve={str(k): v for k, v in ndcurve.items()},
               yardstick_asread=yard_ndmix, yardstick_reweighted=yard_rw, timing_factor=timing,
               survivors=dict(nd=nd_s, rd_v0=rd_s_v0, rd_anchor=rd_s_an, total=total,
                              entry=entry, marks=marks),
               allin=dict(nd=nd_a, rd_v0=rd_a_v0, rd_anchor=rd_a_an, total=tA, entry=eA, marks=mA)),
          open(OUTJS, 'w'), indent=1, default=float)
open(OUTJS.replace('.json', '_out.txt'), 'w').write('\n'.join(L) + '\n')
P("wrote %s" % OUTJS)
