"""ORDER 26A -- THE WEDGE DECOMPOSITION. Read-only.

Quantifies the owner's ~2-3x entry-vs-marks wedge into
  (i)   ENTRY-INFLATION  -- the board's pool entry price v0 above the signed entry anchor,
  (ii)  MARK-SUPPRESSION -- living pool players marked below an ND survivor of equal career age,
  (iii) TIMING           -- the legitimate debut-offset effect, held SEPARATE from (ii).

Trajectories are measured on BOTH axes (H4):
  CALENDAR axis   : cohort year N, the all-arm instrument's own clock (Y = cohort + N - 1).
  CAREER-AGE axis : seasons since the player's OWN first playing season (Y = firstplay + a - 1),
                    where firstplay is the earliest emitted season carrying games > 0.

    usage: python o26a_wedge.py <matrix.json> <out.json>
"""
import sys, json, os, hashlib, collections, statistics

MATRIX = sys.argv[1]; OUTJS = sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..'))
L = []
def P(s=''):
    print(s); L.append(s)

M = json.load(open(MATRIX)); R = M['recs']; meta = M['meta']

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
    """the board as-of mark at calendar year Y. None = row leaves the denominator."""
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

# ---- populations, on the derivation's own definitions ---------------------------------
ND = [r for r in elig if not r.get('is_pool_engine') and r.get('type') == 'ND'
      and r.get('raw_pick') and 1 <= r['raw_pick'] <= 64]
POOL = [r for r in elig if stream(r) in ORDER]
RD = [r for r in elig if stream(r) == 'RD']

def band(pop, Yof, DN, survivors_only):
    """sum(mark)/sum(entry). survivors_only -> restrict to rows carrying a NON-ZERO mark."""
    num = den = 0.0; n = 0
    for r in pop:
        Y = Yof(r)
        if Y is None: continue
        v = mark_at(r, Y)
        if v is None: continue
        if survivors_only and v <= 0: continue
        num += v; den += DN(r); n += 1
    return ((num / den) if den else float('nan'), n, den)

P("=" * 118)
P("ORDER 26A -- THE WEDGE DECOMPOSITION.  matrix=%s  window_end=%d  _PL_F=%.4f"
  % (os.path.basename(MATRIX), W, PL_F))
P("=" * 118)
P("  populations (derivation's own): NATIONAL ND1-64 n=%d   ALL POOL n=%d   RD n=%d"
  % (len(ND), len(POOL), len(RD)))
fp = {t: sum(1 for r in p if firstplay(r) is not None) for t, p in
      [('NATIONAL', ND), ('ALL POOL', POOL), ('RD', RD)]}
P("  rows with a first PLAYING season: " + "  ".join("%s %d" % (k, v) for k, v in fp.items()))
offs = {}
for t, p in [('NATIONAL', ND), ('ALL POOL', POOL), ('RD', RD)]:
    o = [firstplay(r) - cohort(r) for r in p if firstplay(r) is not None]
    offs[t] = dict(mean=statistics.mean(o), median=statistics.median(o), n=len(o),
                   dist=dict(sorted(collections.Counter(o).items())))
    P("  first-play offset from cohort  %-9s mean %+.3f  median %+.1f  dist %s"
      % (t, offs[t]['mean'], offs[t]['median'], offs[t]['dist']))
P()

# =======================================================================================
P("-" * 118)
P("A. THE ENTRY-PRICE OBJECTS -- what each arm is divided by")
P("-" * 118)
ENTRY = {}
for t, p in [('NATIONAL', ND), ('ALL POOL', POOL), ('RD', RD)]:
    sv = sum(v0_of(r) for r in p); sa = sum(anchor_of(r) for r in p)
    ENTRY[t] = dict(sum_v0=sv, sum_anchor=sa, inflation=sv / sa)
    P("  %-9s  SUM board v0 %12s   SUM signed anchor %12s   INFLATION v0/anchor = %.4f"
      % (t, format(round(sv), ','), format(round(sa), ','), sv / sa))
P()

# =======================================================================================
P("-" * 118)
P("B. TRAJECTORIES ON THE CALENDAR AXIS (cohort year N).  ALL = dead zeroed & kept.")
P("   SURV = survivors only (non-zero mark), over THEIR OWN entry -- the owner's convention.")
P("-" * 118)
CAL = {}
P("  %-3s | %-28s | %-28s | %-28s" % ('N', 'NATIONAL (v0=anchor)', 'RD  (board v0 entry)', 'RD  (signed anchor entry)'))
P("  %-3s | %8s %8s %8s | %8s %8s %8s | %8s %8s %8s"
  % ('', 'ALL', 'SURV', 'n_surv', 'ALL', 'SURV', 'n_surv', 'ALL', 'SURV', 'n_surv'))
P("  " + "-" * 110)
for N in range(1, 8):
    Yof = lambda r, N=N: cohort(r) + N - 1
    a_nd, _, _ = band(ND, Yof, v0_of, False); s_nd, n_nd, _ = band(ND, Yof, v0_of, True)
    a_r0, _, _ = band(RD, Yof, v0_of, False); s_r0, n_r0, _ = band(RD, Yof, v0_of, True)
    a_ra, _, _ = band(RD, Yof, anchor_of, False); s_ra, n_ra, _ = band(RD, Yof, anchor_of, True)
    P("  %-3d | %8.4f %8.4f %8d | %8.4f %8.4f %8d | %8.4f %8.4f %8d"
      % (N, a_nd, s_nd, n_nd, a_r0, s_r0, n_r0, a_ra, s_ra, n_ra))
    CAL[N] = dict(nd_all=a_nd, nd_surv=s_nd, nd_n_surv=n_nd, rd_v0_all=a_r0, rd_v0_surv=s_r0,
                  rd_n_surv=n_r0, rd_anchor_all=a_ra, rd_anchor_surv=s_ra)
P()

# =======================================================================================
P("-" * 118)
P("C. TRAJECTORIES ON THE CAREER-AGE AXIS (seasons since the player's OWN first playing season).")
P("   Only rows that ever played carry a career age; the never-played are OUT of this axis by")
P("   construction and are reported separately so nothing hides.")
P("-" * 118)
CAR = {}
P("  %-3s | %-28s | %-28s | %-28s" % ('age', 'NATIONAL (v0=anchor)', 'RD  (board v0 entry)', 'RD  (signed anchor entry)'))
P("  %-3s | %8s %8s %8s | %8s %8s %8s | %8s %8s %8s"
  % ('', 'ALL', 'SURV', 'n_surv', 'ALL', 'SURV', 'n_surv', 'ALL', 'SURV', 'n_surv'))
P("  " + "-" * 110)
for a in range(1, 8):
    def Yof(r, a=a):
        f = firstplay(r)
        return None if f is None else f + a - 1
    a_nd, _, _ = band(ND, Yof, v0_of, False); s_nd, n_nd, _ = band(ND, Yof, v0_of, True)
    a_r0, _, _ = band(RD, Yof, v0_of, False); s_r0, n_r0, _ = band(RD, Yof, v0_of, True)
    a_ra, _, _ = band(RD, Yof, anchor_of, False); s_ra, n_ra, _ = band(RD, Yof, anchor_of, True)
    P("  %-3d | %8.4f %8.4f %8d | %8.4f %8.4f %8d | %8.4f %8.4f %8d"
      % (a, a_nd, s_nd, n_nd, a_r0, s_r0, n_r0, a_ra, s_ra, n_ra))
    CAR[a] = dict(nd_all=a_nd, nd_surv=s_nd, nd_n_surv=n_nd, rd_v0_all=a_r0, rd_v0_surv=s_r0,
                  rd_n_surv=n_r0, rd_anchor_all=a_ra, rd_anchor_surv=s_ra)
P()

# =======================================================================================
P("-" * 118)
P("D. THE WEDGE, DECOMPOSED.  Multiplicative, split in LOG SPACE so the shares sum to 100%.")
P("-" * 118)
DEC = {}
for axis, T, key in [('CALENDAR  N=4', CAL[4], 'cal4'), ('CALENDAR  N=5', CAL[5], 'cal5'),
                     ('CAREER-AGE a=4', CAR[4], 'car4'), ('CAREER-AGE a=3', CAR[3], 'car3')]:
    for mode, ndk, r0k, rak in [('ALL (dead zeroed)', 'nd_all', 'rd_v0_all', 'rd_anchor_all'),
                                ('SURVIVORS own-entry', 'nd_surv', 'rd_v0_surv', 'rd_anchor_surv')]:
        nd = T[ndk]; rv = T[r0k]; ra = T[rak]
        wedge = nd / rv                      # total: ND over RD-as-the-board-prices-it
        entry = ra / rv                      # removed by restating entry on the signed anchor
        resid = nd / ra                      # what the marks still owe after the entry fix
        import math
        lw = math.log(wedge)
        DEC[key + '|' + mode] = dict(nd=nd, rd_v0=rv, rd_anchor=ra, wedge=wedge,
                                     entry_factor=entry, residual_factor=resid,
                                     entry_share_pct=100 * math.log(entry) / lw,
                                     residual_share_pct=100 * math.log(resid) / lw)
        P("  %-16s %-20s ND %7.4f | RD@v0 %7.4f | RD@anchor %7.4f | WEDGE %6.3fx"
          % (axis, mode, nd, rv, ra, wedge))
        P("      %-37s entry-inflation %6.3fx (%5.1f%%)   residual %6.3fx (%5.1f%%)"
          % ('', entry, 100 * math.log(entry) / lw, resid, 100 * math.log(resid) / lw))
P()

# ---- the TIMING leg: how much of the residual closes by switching the axis --------------
import math
P("-" * 118)
P("E. THE TIMING LEG (iii) -- how much of the post-entry residual is the debut offset alone")
P("-" * 118)
tim = {}
for mode, ndk, rak in [('ALL (dead zeroed)', 'nd_all', 'rd_anchor_all'),
                       ('SURVIVORS own-entry', 'nd_surv', 'rd_anchor_surv')]:
    rc = CAL[4][ndk] / CAL[4][rak]
    ra_ = CAR[4][ndk] / CAR[4][rak]
    P("  %-22s residual on CALENDAR N=4 %6.4fx    on CAREER-AGE a=4 %6.4fx    axis moves it %+.4fx"
      % (mode, rc, ra_, ra_ - rc))
    tim[mode] = dict(residual_calendar=rc, residual_career=ra_, axis_delta=ra_ - rc)
P()
P("  Career-age matching is the SEPARATION the brief demands: it compares a pool player in his")
P("  a-th playing season with a national player in HIS a-th playing season, so the later-debut")
P("  effect cannot be charged to mark suppression.")
P()

json.dump(dict(matrix=os.path.basename(MATRIX), window_end=W, PL_F=PL_F,
               n=dict(ND=len(ND), POOL=len(POOL), RD=len(RD)), first_play_offsets=offs,
               entry_objects=ENTRY, calendar=CAL, career_age=CAR, decomposition=DEC, timing=tim),
          open(OUTJS, 'w'), indent=1, default=float)
open(OUTJS.replace('.json', '_out.txt'), 'w').write('\n'.join(L) + '\n')
P("wrote %s" % OUTJS)
