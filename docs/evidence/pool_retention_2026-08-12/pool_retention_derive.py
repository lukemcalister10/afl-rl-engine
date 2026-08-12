#!/usr/bin/env python3
"""ORDER 21 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL DATA.

OWNER RULING (directive D8, comment 5253173347), verbatim:
  "the pool sitter on top penalty should go, and the pool index should be rederived in the same way
   the ND one is where possible not for pick 65, but for the pool."
and, on the axis:
  "They're all part of the pool... for the purposes of this, rookie draft pick 1 and 30 are the same"

This DERIVES the replacement. It wires nothing. The method is
`session_2026-07-03/d13/scripts/d13_derive.py` + `d13_norm_harvest.py` (the ND retention derivation),
carried step for step, with SEVEN declared departures (PREREG_ORDER21.md section B).

READ-ONLY. The engine is loaded from a STAGED COPY under the scratchpad; the checkout is never
written. Pins asserted at entry AND exit.

  usage:  OPENBLAS_NUM_THREADS=1 python pool_retention_derive.py
  writes: POOL_RETENTION_SURFACE.json  (consumed by the board patch and by ORDER 22)
"""
import os, sys, io, json, contextlib, math, hashlib, shutil, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng_stage_o21/rl_after'

PINS = {
    'board': ('data/rl_build/rl_app_data.json', '1dbd1480a34c7823f330273211cbb76a'),
    'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
    'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                   '0f8220351c64c56ccfa90c60edcdfa5f'),
}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = []
    for k, (rel, exp) in PINS.items():
        got = _md5(os.path.join(ROOT, rel))
        if got != exp:
            bad.append("%s %s != pinned %s (%s)" % (k, got, exp, rel))
    if bad:
        raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')

if not os.path.exists(os.path.join(STAGE, '_merged_recover.py')):
    os.makedirs(os.path.dirname(STAGE), exist_ok=True)
    shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
for _f in ('LTI_REGISTER.md',):
    if not os.path.exists(os.path.join(STAGE, _f)):
        shutil.copy(os.path.join(ROOT, _f), STAGE)

os.environ.update(PYTHONHASHSEED='0')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd()
os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)

MA, cp = G['MA'], G['cp']
price6, v0_start, entry_anchor = G['price6'], G['v0_start'], G['entry_anchor']
_sitout_cls, _R_surf, _b_age = G['_sitout_cls'], G['_R_surf'], G['_b_age']
H_POOLSIT, H_UNION = G['H_POOLSIT'], G['H_UNION']

OUT = []


def P(s=''):
    print(s)
    OUT.append(s)


CLASSES = ('nonKPP', 'KPP', 'RUCK')
DEPTHS = list(range(1, 7))
K_LAYER2 = 10.0          # directive D4, ruled: layer-2 within-group borrowing (K_336 / K_338)
N_OWN = 20               # order requirement 3: a cell fits on its own data at n >= 20
WINSOR = 2.0
TARGET_EFFN = 35.0       # the ND rule (D5), carried


def wins(x, cap=WINSOR):
    return float(min(max(x, 0.0), cap))


# ==================================================================================================
# 1. HARVEST -- POOL ROWS ONLY
# ==================================================================================================
P("=" * 118)
P("ORDER 21 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY")
P("=" * 118)
P("  pins asserted at entry: board 1dbd1480..  store d9a24282..  instrument 0f822035..")
P("  engine loaded read-only from a staged copy; checkout untouched.  MA.data n=%d" % len(MA.data))
P("  shipped read being replaced: R=_R_surf(cls, effpk=65, tau) x H_POOLSIT %.3f x H_UNION %.3f"
  % (H_POOLSIT, H_UNION))
P()


def draftyr(p):
    return cp.debutyr(p) - 1


def min_window(p):
    t, pk = p.get('type'), p.get('pick')
    if t == 'ND' and pk and pk <= 20: return 4
    if t == 'ND' and pk and pk <= 40: return 3
    return 2


def listed_through(p):
    if p.get('_last_listed') is not None: return int(p['_last_listed'])
    if not p.get('_retired'): return 2026
    lg = max((x['year'] for x in p['scoring']), default=0)
    dy = p.get('year') or lg
    return max(dy + min_window(p) - 1, lg)


def stream(p):
    t = p.get('type')
    if t == 'ND':
        pk = p.get('pick') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


def outcomeO(p, Y):
    """Forward realisation. D1 DEPARTURE: NO era normalisation -- the table, REF and every
    a*REF/era[y] site were retired by owner ruling (_merged_recover.py:52-57)."""
    fwd = [x for x in p['scoring'] if x['games'] >= 6 and Y < x['year'] <= Y + 4]
    if not fwd: return 0.0
    L = max(x['avg'] for x in fwd)
    with contextlib.redirect_stdout(io.StringIO()):
        return float(price6(p, [L] * 6, Y))


cells = []
_nd_seen = 0
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_double_count') or not MA.GRP.get(p.get('pos')): continue
        if not (p.get('pick') or p.get('_ft') or p.get('_pool')): continue
        dy = draftyr(p)
        if dy < 2003 or dy > 2024: continue
        pool = bool(p.get('_pool'))
        if not pool:
            _nd_seen += 1
            continue                          # SEPARATION LAW: pool rows only, at the harvest gate
        lt = listed_through(p)
        rows = sorted(p['scoring'], key=lambda x: x['year'])
        pos = MA.gfut(p); cls = _sitout_cls(pos)
        try: ea = float(entry_anchor(p))
        except Exception: ea = float('nan')
        try: va = float(v0_start(p))
        except Exception: va = float('nan')
        st = stream(p)
        for Y in range(dy + 1, min(lt, 2025) + 1):
            quals = [x for x in rows if x['games'] >= 6 and x['year'] <= Y]
            O = outcomeO(p, Y)
            cells.append(dict(key=p.get('key'), player=p.get('player'), pool=pool, stream=st,
                              cls=cls, pos=pos, d=Y - dy, sitout=bool(not quals),
                              O=round(O, 4), Vanchor=ea, V0start=va,
                              wc=bool(Y <= 2021), typ=p.get('type'),
                              effpk=int(MA.effpk(p))))

P("=" * 118)
P("1. THE POPULATION -- POOL ROWS ONLY (the SEPARATION LAW, asserted at the harvest gate)")
P("=" * 118)
NONPOOL = [c for c in cells if not c['pool']]
assert len(NONPOOL) == 0, "SEPARATION LAW BREACH: %d national cells in the harvest" % len(NONPOOL)
P("  national rows encountered and EXCLUDED at the gate: %d" % _nd_seen)
P("  ASSERTION: non-pool cells in the harvest = %d  -> SEPARATION LAW HOLDS" % len(NONPOOL))

WC = [c for c in cells if c['wc'] and c['Vanchor'] == c['Vanchor'] and c['Vanchor'] > 0]
ALL = [c for c in cells if c['Vanchor'] == c['Vanchor'] and c['Vanchor'] > 0]
SITWC = [c for c in WC if c['sitout']]
P("  cells harvested        : %d   (complete-window Y<=2021, priceable entry anchor: %d)"
  % (len(cells), len(WC)))
P("  of the complete-window : %d sit-out cells (%.4f by count)" % (len(SITWC), len(SITWC) / len(WC)))
P("  pathways present       : %s" % dict(sorted(collections.Counter(c['stream'] for c in WC).items(),
                                                key=lambda kv: -kv[1])))
P()
P("  THE SITTER DEFINITION, STATED ONCE AND USED EVERYWHERE IN THIS ACT:")
P("    a cell is a SIT-OUT iff the player has NO season of >= 6 games at or before Y.")
P("    That is nseas_pro(p,Y)==0 on a completed season -- EXACTLY the gate ev() uses to send a row")
P("    to sitout_ev. It is NOT _h_cut's test (games THIS season <= 0); ORDER 19 measured those two")
P("    populations do not coincide, and _h_cut retires here, so the second population ceases to")
P("    exist in the engine for pool rows.")
P("    MID-SEASON: the engine's clock tau = (Y-debutyr) + fE**1.5 equals d exactly at fE=1, so the")
P("    integer derivation knots sit on the engine's own integer knots; the in-progress season")
P("    interpolates by the existing D12 concave proration (fE=0.58 -> tau=(d-1)+0.4417). tau=0 -> R=1.")
P()

# ==================================================================================================
# 2. THE SAME-DEPTH ALL-POOL NORM  (ND step, carried)
# ==================================================================================================
P("=" * 118)
P("2. THE SAME-DEPTH ALL-POOL NORM  E[winsor(O/entry_anchor, 2.0)]  -- developer-inclusive")
P("=" * 118)
P("  The ND method's denominator, re-harvested on the pool. It strips the survivor-selection")
P("  common-mode: deep survivors are increasingly the developers, so the norm RISES with depth and")
P("  dividing by it is what makes a deep retention comparable to a shallow one.")
P("  D2 DEPARTURE: the denominator is entry_anchor(p), not v0_start(p) -- entry_anchor is literally")
P("  what R multiplies at both pool read sites (anch = R*entry_anchor(p)). v0_start is carried")
P("  alongside as a sensitivity.")
P()


def build_norm(sub, denom='Vanchor'):
    nm = {}
    for cls in CLASSES:
        for dd in DEPTHS:
            v = [wins(c['O'] / max(1e-9, c[denom])) for c in sub
                 if c['cls'] == cls and c['d'] == dd and c[denom] == c[denom] and c[denom] > 0]
            nm[(cls, dd)] = (float(np.mean(v)) if v else float('nan'), len(v))
    return nm


NORM = build_norm(WC)
NORM_V0 = build_norm(WC, 'V0start')
P("  %-8s | %s" % ('class', "  ".join("d%d (n)      " % d for d in DEPTHS)))
for cls in CLASSES:
    P("  %-8s | %s" % (cls, "  ".join("%.3f (%4d)" % NORM[(cls, d)] for d in DEPTHS)))
P()
P("  sensitivity, same norm on the v0_start denominator:")
for cls in CLASSES:
    P("  %-8s | %s" % (cls, "  ".join("%.3f (%4d)" % NORM_V0[(cls, d)] for d in DEPTHS)))
P()

# ==================================================================================================
# 3. THE WHOLE-POOL SURFACE
# ==================================================================================================
P("=" * 118)
P("3. THE WHOLE-POOL DERIVED SURFACE  R(class, depth)")
P("=" * 118)
P("  r_sit = Gaussian kernel local mean of winsor(O/entry_anchor,2.0) over the SIT-OUT subset,")
P("  DEPTH AXIS ONLY (D3 departure: no pick axis -- the owner's ruling that the pool is one")
P("  population, and MA.effpk returns the constant POOL_PICK=65 for every pool row, so a pick axis")
P("  is not identified). bw grown through [0.75,1.1,1.6,2.5] until eff-n >= 35.")
P("  R = clip(r_sit / norm, 0.05, 1.0), then ISOTONIC NON-INCREASING IN DEPTH (the owner's law).")
P()


def eff_n(w):
    s = w.sum()
    return float((s * s) / np.sum(w * w)) if s > 0 else 0.0


def kern(cells_, dd, bwd, denom='Vanchor'):
    if not cells_: return float('nan'), 0.0, 0
    dpt = np.array([c['d'] for c in cells_], dtype=float)
    r = np.array([wins(c['O'] / max(1e-9, c[denom])) for c in cells_])
    w = np.exp(-0.5 * ((dpt - dd) / bwd) ** 2)
    if w.sum() <= 0: return float('nan'), 0.0, 0
    return float(np.sum(w * r) / np.sum(w)), eff_n(w), len(cells_)


def rsit_at(cells_, dd, denom='Vanchor'):
    for bwd in (0.75, 1.1, 1.6, 2.5):
        m, en, n = kern(cells_, dd, bwd, denom)
        if en >= TARGET_EFFN:
            return m, bwd, en, n, False
    m, en, n = kern(cells_, dd, 2.5, denom)
    return m, 2.5, en, n, True          # widest; DECLARED thin


def isotonic_noninc(vals):
    out = list(vals)
    for i in range(1, len(out)):
        if out[i] > out[i - 1]: out[i] = out[i - 1]
    return out


def viol(vals):
    return sum(1 for i in range(1, len(vals)) if vals[i] > vals[i - 1] + 1e-12)


SIT = {cls: [c for c in SITWC if c['cls'] == cls] for cls in CLASSES}
POOLSURF, POOLRAW, POOLMETA = {}, {}, {}
P("  %-8s | %-42s | %-42s" % ('class', 'RAW  R = r_sit/norm, clip[.05,1]', 'ISOTONIC (wired)'))
P("  %-8s | %s | %s" % ('', "  ".join("d%d   " % d for d in DEPTHS), "  ".join("d%d   " % d for d in DEPTHS)))
for cls in CLASSES:
    raw, meta = [], []
    for dd in DEPTHS:
        m, bwd, en, n, thin = rsit_at(SIT[cls], dd)
        nm = NORM[(cls, dd)][0]
        R = m / nm if (nm == nm and nm > 0) else m
        R = float(min(max(R, 0.05), 1.0))
        raw.append(R)
        meta.append(dict(bwd=bwd, effn=round(en, 1), n_exact=sum(1 for c in SIT[cls] if c['d'] == dd),
                         thin=thin, norm=round(nm, 4), rsit=round(m, 4)))
    iso = isotonic_noninc(raw)
    POOLRAW[cls] = raw; POOLSURF[cls] = iso; POOLMETA[cls] = meta
    P("  %-8s | %s | %s" % (cls, "  ".join("%.3f" % x for x in raw), "  ".join("%.3f" % x for x in iso)))
P()
P("  exact-depth sit-out cell counts (the derivation's own n, before the depth kernel):")
for cls in CLASSES:
    P("  %-8s | %s" % (cls, "  ".join("d%d=%-5d" % (d, sum(1 for c in SIT[cls] if c['d'] == d)) for d in DEPTHS)))
P()
P("  kernel bandwidth / eff-n actually used per cell:")
for cls in CLASSES:
    P("    %-8s %s" % (cls, "  ".join("d%d bw=%.2f effn=%.0f%s" % (DEPTHS[i], POOLMETA[cls][i]['bwd'],
                                                                  POOLMETA[cls][i]['effn'],
                                                                  '*' if POOLMETA[cls][i]['thin'] else '')
                                      for i in range(6))))
P("    (* = eff-n never reached 35 even at the widest bandwidth -- DECLARED THIN)")
P()
_rawviol = {cls: viol(POOLRAW[cls]) for cls in CLASSES}
P("  ISOTONIC STEP: raw violations of the owner's non-increasing law per class: %s" % _rawviol)
P("  ISOTONIC STEP: violations AFTER projection: %s"
  % {cls: viol(POOLSURF[cls]) for cls in CLASSES})
assert all(viol(POOLSURF[cls]) == 0 for cls in CLASSES), "isotonic projection failed"
P()
P("  WHAT THE SHIPPED READ DOES TODAY, for comparison (national surface at effpk=65 x H):")
for cls in CLASSES:
    shipped = [float(_R_surf(cls, 65, float(d))) for d in DEPTHS]
    comp = [x * H_POOLSIT for x in shipped]
    compu = [x * H_POOLSIT * H_UNION for x in shipped]
    P("    %-8s R_natl@65 %s" % (cls, "  ".join("%.3f" % x for x in shipped)))
    P("    %-8s xH_POOLSIT %s   xH_UNION too %s" % ('', "  ".join("%.3f" % x for x in comp),
                                                     "  ".join("%.3f" % x for x in compu)))
    P("    %-8s DERIVED    %s" % ('', "  ".join("%.3f" % x for x in POOLSURF[cls])))
P()

# also the v0_start-denominator sensitivity surface
POOLSURF_V0 = {}
for cls in CLASSES:
    raw = []
    for dd in DEPTHS:
        m, bwd, en, n, thin = rsit_at(SIT[cls], dd, 'V0start')
        nm = NORM_V0[(cls, dd)][0]
        R = m / nm if (nm == nm and nm > 0) else m
        raw.append(float(min(max(R, 0.05), 1.0)))
    POOLSURF_V0[cls] = isotonic_noninc(raw)
P("  SENSITIVITY -- the same surface on the v0_start denominator (D2 alternative):")
for cls in CLASSES:
    P("    %-8s %s" % (cls, "  ".join("%.3f" % x for x in POOLSURF_V0[cls])))
P()

# ==================================================================================================
# 4. THE PATHWAY LAYER
# ==================================================================================================
P("=" * 118)
P("4. THE PATHWAY LAYER -- own data at n>=20, else K=10 partial pooling to the whole-pool cell")
P("=" * 118)
P("  v = w*own + (1-w)*R_pool(cls,d),  w = n/(n+10).  K=10 is the layer-2 constant RULED at")
P("  directive D4 (K_336 rl_model.py:396, K_338 par_build.py:164 -- the engine's own within-group")
P("  borrowing convention). EVERY pooled cell is disclosed below with its n and its w.")
P()
PATHS = sorted(set(c['stream'] for c in WC), key=lambda s: -sum(1 for c in WC if c['stream'] == s))
PATHSURF, PATHDISC = {}, []
for pw in PATHS:
    sub = [c for c in SITWC if c['stream'] == pw]
    allsub = [c for c in WC if c['stream'] == pw]
    nrm = build_norm(allsub)
    PATHSURF[pw] = {}
    for cls in CLASSES:
        subc = [c for c in sub if c['cls'] == cls]
        raw = []
        for dd in DEPTHS:
            n_ex = sum(1 for c in subc if c['d'] == dd)
            if n_ex >= N_OWN:
                m, bwd, en, n, thin = rsit_at(subc, dd)
                nm = nrm[(cls, dd)][0]
                own = m / nm if (nm == nm and nm > 0) else m
                own = float(min(max(own, 0.05), 1.0))
                w = 1.0
                v = own
                src = 'OWN'
            else:
                m, bwd, en, n, thin = rsit_at(subc, dd) if subc else (float('nan'), 2.5, 0.0, 0, True)
                nm = nrm[(cls, dd)][0]
                own = (m / nm if (nm == nm and nm > 0 and m == m) else m)
                if own != own:
                    own = POOLSURF[cls][dd - 1]
                own = float(min(max(own, 0.05), 1.0))
                w = n_ex / (n_ex + K_LAYER2)
                v = w * own + (1.0 - w) * POOLSURF[cls][dd - 1]
                src = 'POOLED'
            raw.append(v)
            PATHDISC.append(dict(pathway=pw, cls=cls, d=dd, n=n_ex, w=round(w, 4),
                                 own=round(own, 4), donor=round(POOLSURF[cls][dd - 1], 4),
                                 value=round(v, 4), src=src))
        PATHSURF[pw][cls] = isotonic_noninc(raw)

_own = [r for r in PATHDISC if r['src'] == 'OWN']
P("  cells reaching n>=20 and fitting on their OWN data: %d of %d (%d pathways x 3 classes x 6 depths)"
  % (len(_own), len(PATHDISC), len(PATHS)))
if _own:
    P("  %-8s %-7s %-3s %6s %7s %8s %8s" % ('pathway', 'class', 'd', 'n', 'w', 'own', 'wired'))
    for r in _own:
        P("  %-8s %-7s d%-2d %6d %7.4f %8.4f %8.4f" % (r['pathway'], r['cls'], r['d'], r['n'], r['w'],
                                                       r['own'], r['value']))
P()
P("  POOLED CELLS -- every one disclosed with its n and its borrowing weight (only cells with n>0")
P("  shown individually; cells with n==0 take the whole-pool donor outright, w=0):")
P("  %-8s %-7s %-3s %6s %7s %8s %8s %8s" % ('pathway', 'class', 'd', 'n', 'w=n/(n+10)', 'own', 'donor', 'wired'))
for r in PATHDISC:
    if r['src'] == 'POOLED' and r['n'] > 0:
        P("  %-8s %-7s d%-2d %6d %10.4f %8.4f %8.4f %8.4f"
          % (r['pathway'], r['cls'], r['d'], r['n'], r['w'], r['own'], r['donor'], r['value']))
_zero = [r for r in PATHDISC if r['src'] == 'POOLED' and r['n'] == 0]
P("  cells with n==0 taking the donor outright (w=0): %d" % len(_zero))
P("    %s" % collections.Counter("%s/%s" % (r['pathway'], r['cls']) for r in _zero))
P()
P("  THE WIRED PATHWAY SURFACE (after isotonic re-projection):")
for pw in PATHS:
    P("    --- %s ---" % pw)
    for cls in CLASSES:
        v = PATHSURF[pw][cls]
        P("      %-8s %s   (violations %d)" % (cls, "  ".join("%.4f" % x for x in v), viol(v)))
assert all(viol(PATHSURF[pw][cls]) == 0 for pw in PATHS for cls in CLASSES), "pathway isotonic failed"
P()
P("  ISOTONIC VERIFICATION: violations of the non-increasing law over all %d wired pathway x class"
  % (len(PATHS) * 3))
P("  vectors AND the 3 whole-pool vectors: 0. The owner's signed law holds at every fitted cell.")
P()

# ==================================================================================================
# 5. THE MEAN-PRESERVING TABLE
# ==================================================================================================
P("=" * 118)
P("5. THE MEAN-PRESERVING TABLE, PER PATHWAY -- the owner's D8 law as arithmetic")
P("=" * 118)
P("  e = entry_anchor(p) (ORDER 19's statistic, carried verbatim). Over the pathway's complete-window")
P("  cells:")
P("      U = ( SUM_all e - SUM_sit e*R ) / SUM_non e")
P("      mean = ( SUM_sit e*R + SUM_non e*U ) / SUM_all e  ==  1.0000000000  exactly")
P("  This step ALSO discharges directive D4's renormalisation guard: whatever the borrowed cells")
P("  deliver, the pathway's entry-weighted mean returns to 1 in one multiplication.")
P()


def R_of(c):
    return float(PATHSURF[c['stream']][c['cls']][min(max(c['d'], 1), 6) - 1])


def shipped_mult(c):
    """what the engine charges this cell TODAY: R_natl(cls, effpk=65, d) x H_POOLSIT [x H_UNION]"""
    R = float(_R_surf(c['cls'], c['effpk'], float(c['d'])))
    f = H_POOLSIT
    age = None
    if (c['typ'] in ('IRE', 'MSD')):
        f *= H_UNION
    return R * f


MP = {}
rows = []
for pw in PATHS + ['ALL POOL']:
    sub = WC if pw == 'ALL POOL' else [c for c in WC if c['stream'] == pw]
    tot = sitw = nonw = num = 0.0
    nsit = 0
    for c in sub:
        e = c['Vanchor']
        tot += e
        if c['sitout']:
            sitw += e; num += e * R_of(c); nsit += 1
        else:
            nonw += e
    U = (tot - num) / nonw if nonw > 0 else float('nan')
    mean = (num + nonw * U) / tot if tot > 0 else float('nan')
    meanR = num / sitw if sitw > 0 else float('nan')
    MP[pw] = dict(cells=len(sub), sitters=nsit, sit_share_w=sitw / tot, meanR=meanR, U=U, mean=mean,
                  sit_share_n=nsit / len(sub) if sub else 0.0)
    rows.append((pw, len(sub), nsit, sitw / tot, meanR, U, mean))

P("  %-9s %7s %8s %10s %10s %10s %16s" % ('pathway', 'cells', 'sitters', 'sit shr', 'mean R', 'U', 'post-redist mean'))
for (pw, n, ns, ss, mr, U, mn) in rows:
    P("  %-9s %7d %8d %10.4f %10.6f %10.6f %16.10f" % (pw, n, ns, ss, mr, U, mn))
_bad = [r for r in rows if abs(r[6] - 1.0) > 1e-9]
P()
P("  ASSERTION: pathways whose post-redistribution entry-weighted mean is not 1.0000000000: %d" % len(_bad))
assert not _bad, "mean-preservation failed on %s" % [r[0] for r in _bad]
P()
P("  THE CONDITIONAL MARKDOWN IS THE FULL UPDATE, NOT A BLENDED AVERAGE. Read the two columns")
P("  together: 'mean R' is what an ACTUAL SITTER carries; U is what everyone else carries. The")
P("  sitter markdown (1 - mean R) is deliberately LARGER than the pathway-blended figure would be,")
P("  and the uplift pays for it exactly.")
P()
P("  Against what the engine charges TODAY (composed R_natl@65 x H_POOLSIT [x H_UNION]), same cells:")
P("  %-9s %12s %12s %12s" % ('pathway', 'today meanM', 'derived R', 'delta'))
for pw in PATHS + ['ALL POOL']:
    sub = WC if pw == 'ALL POOL' else [c for c in WC if c['stream'] == pw]
    sw = sum(c['Vanchor'] for c in sub if c['sitout'])
    if sw <= 0: continue
    tm = sum(c['Vanchor'] * shipped_mult(c) for c in sub if c['sitout']) / sw
    dm = sum(c['Vanchor'] * R_of(c) for c in sub if c['sitout']) / sw
    P("  %-9s %12.6f %12.6f %+12.6f" % (pw, tm, dm, dm - tm))
P()

# ==================================================================================================
# 6. RECONCILIATION TO ORDER 18
# ==================================================================================================
P("=" * 118)
P("6. RECONCILIATION -- ORDER 18's pool-history depth-1 figures on ITS convention vs mine")
P("=" * 118)
P("  ORDER 18 published pool-history depth-1 retention nonKPP 0.5725 / KPP 0.7528 / RUCK 0.8783.")
P("  Mine differs by three declared departures: the denominator (D2 entry_anchor vs v0_start), the")
P("  norm population (pool-only here) and era (D1). Both are printed so the gap is visible, not")
P("  argued.")
P()
O18 = {'nonKPP': 0.5725, 'KPP': 0.7528, 'RUCK': 0.8783}
P("  %-8s %12s %14s %16s" % ('class', 'ORDER 18', 'ORDER 21 d1', 'ORDER 21 d1 (v0 denom)'))
for cls in CLASSES:
    P("  %-8s %12.4f %14.4f %16.4f" % (cls, O18[cls], POOLSURF[cls][0], POOLSURF_V0[cls][0]))
P()

# ==================================================================================================
# 7. THE OWNER-OVERRIDE O1 READING (KPP floor), printed both ways, not chosen
# ==================================================================================================
P("=" * 118)
P("7. OWNER OVERRIDE O1 (the KPP retention floor) -- PRINTED BOTH WAYS, NOT CHOSEN (departure D7)")
P("=" * 118)
P("  O1 is Luke's signed override on the NATIONAL surface, board path only: KPP := max(KPP, nonKPP)")
P("  pointwise. Whether it extends to an object derived on pool data is an owner question. The")
P("  derived surface as wired here does NOT apply it; the floored reading is printed for the ruling.")
kfl = [max(a, b) for a, b in zip(POOLSURF['KPP'], POOLSURF['nonKPP'])]
P("    whole-pool KPP as derived : %s" % "  ".join("%.4f" % x for x in POOLSURF['KPP']))
P("    whole-pool KPP under O1   : %s" % "  ".join("%.4f" % x for x in kfl))
P("    cells where O1 would bind : %d of 6" % sum(1 for i in range(6) if kfl[i] > POOLSURF['KPP'][i] + 1e-9))
P()

# ==================================================================================================
# WRITE
# ==================================================================================================
SURF = dict(
    meta=dict(order=21, pins={k: v[1] for k, v in PINS.items()},
              method='d13 ND retention derivation, departures D1-D7 (PREREG_ORDER21.md)',
              K_layer2=K_LAYER2, n_own=N_OWN, winsor=WINSOR, target_effn=TARGET_EFFN,
              denom='entry_anchor', cells_wc=len(WC), sitters_wc=len(SITWC),
              nonpool_cells=len(NONPOOL)),
    whole_pool={cls: [round(x, 6) for x in POOLSURF[cls]] for cls in CLASSES},
    whole_pool_raw={cls: [round(x, 6) for x in POOLRAW[cls]] for cls in CLASSES},
    whole_pool_v0denom={cls: [round(x, 6) for x in POOLSURF_V0[cls]] for cls in CLASSES},
    whole_pool_meta={cls: POOLMETA[cls] for cls in CLASSES},
    norm={"%s|%d" % (k[0], k[1]): [round(v[0], 6) if v[0] == v[0] else None, v[1]]
          for k, v in NORM.items()},
    pathway={pw: {cls: [round(x, 6) for x in PATHSURF[pw][cls]] for cls in CLASSES} for pw in PATHS},
    pathway_disclosure=PATHDISC,
    mean_preserving={pw: {k: (round(v, 10) if isinstance(v, float) else v) for k, v in MP[pw].items()}
                     for pw in MP},
    uplift={pw: round(MP[pw]['U'], 10) for pw in PATHS},
    o1_floored_kpp=[round(x, 6) for x in kfl],
)
with open(os.path.join(HERE, 'POOL_RETENTION_SURFACE.json'), 'w') as f:
    json.dump(SURF, f, indent=1)
P("wrote POOL_RETENTION_SURFACE.json  md5 %s"
  % _md5(os.path.join(HERE, 'POOL_RETENTION_SURFACE.json')))

assert_pins('exit')
P()
P("PINS RE-ASSERTED AT EXIT -- all three UNMOVED.")
with open(os.path.join(HERE, 'pool_retention_derive_out.txt'), 'w') as f:
    f.write("\n".join(OUT) + "\n")
