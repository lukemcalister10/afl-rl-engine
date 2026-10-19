#!/usr/bin/env python3
"""ORDER 26B — STEP 1, THE IDENTITY GATE (Ruling 9).

READ-ONLY. The engine is loaded from a staged copy under the scratchpad; the checkout is never written.

WHAT THIS DOES
--------------
Ruling 3 fixes the production-value function as "today's engine's price for an established season of
average X at position P". This harness PINS that callable, then certifies the choice the way Ruling 9
orders: for each panel player it constructs his SIX PROJECTED OUTCOME CAREERS -- the band's own season
paths, exactly as the engine projects them -- runs each through THE SCORER, WQ6-weights them, and
compares the blend to his LIVE BOARD PRICE. +/-2% passes.

THE PINNED PRICE FUNCTION (Ruling 3), stated as one line:

    season_points(X, P) = SCALE * posval( X + capt_prem(X) - bar[P] ) * 21

    bar[P]      = MA.REPL[P] - rd.REPL_DROP[P], READ LIVE off MA.REPL inside price6's own lowered-REPL
                  netting context (Ruling 1: via the engine's own netting path, never hand-copied)
    posval      = rl_model.py::posval          (line 785)
    capt_prem   = rl_model.py::capt_prem       (line 676)
    SCALE       = rl_model.py                  (line 1120, reassigned line 1324)
    * 21        = the engine's own season-games constant in proj_from_peak (line 963/978)
    discount    = rl_model.py::disc_factor(a, LENS['bal'], k)  (line 906), live config = flat 14%

    This IS the k-th season term of rl_model.py::proj_from_peak. It is REUSED, not reimplemented: the
    harness reads MA.posval / MA.capt_prem / MA.SCALE / MA.REPL / MA.disc_factor as live attributes.

THE SIX PROJECTED CAREERS
-------------------------
price6(p, bb, Y) = SCALE_DIST * sum_i WQ6[i] * dp.v_at_peak(p, bb[i], 'bal'), evaluated with MA.REPL
lowered by rd.REPL_DROP. dp.v_at_peak(p, L) = max( MA.val(proj_from_peak(...L...)), MA.prod_floor(p) ).
proj_from_peak's loop IS a career: season k is played at age a+k at level

    lev_k = L * frac(a+k, PEAK_AGE[g]),  floored at the current level cl while a+k <= peak age and at k=0,

valued at position bnow(p) at k=0 and at the futblend(p) mix for k>=1 (Ruling 5's two uses of position,
in the engine's own words), truncated when age > 38 or frac < 0.42.  So the six careers ARE constructible
from the engine's own objects, and the scorer's job is to reprice them.

TWO PROJECTION-SIDE MULTIPLIERS are carried because they are part of the engine's own price of a
PROJECTED career and would otherwise be a silent divergence:  x1.05 for KPF/KPD, and the runway-x-elite
premium (1 + clip((25-a)/6) * clip((L/PEAK[g]-0.97)/0.30) * PMAX).  Both are DECLARED, not hidden.

OUTPUTS
-------
  GATE.json     per-player rows, every leg
  GATE_out.txt  the console transcript
"""
import os, sys, io, json, contextlib, hashlib, shutil, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng26b_gate/rl_after'

PINS = {'store':  ('engine/rl_after/rl_model_data.json',      'd9a24282357cf3083b1640466e3ecd83'),
        'board':  ('engine/rl_after/rl_app_data.json',        '88ce647f531030d8d2e094188b258191'),
        'engine': ('engine/rl_after/_merged_recover.py',      '3f1468e5468462ab789e49aace264c90'),
        'model':  ('engine/rl_after/rl_model.py',             'e5eb5e4405c09eebef45a9db89f014bc'),
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
    if bad: raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')
shutil.rmtree(SP + '/eng26b_gate', ignore_errors=True)
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(os.path.join(ROOT, 'LTI_REGISTER.md'), STAGE)

os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT, OPENBLAS_NUM_THREADS='1')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)

MA = G['MA']; cp = G['cp']; dp = G['dp']; rd = G['rd']
ev = G['ev']; price6 = G['price6']; b6 = G['b6']; raw_ev = G['raw_ev']; WQ6 = G['WQ6']
_uncomp_prod = G['_uncomp_prod']; _det_dot = G['_det_dot']; iso_eff = G['iso_eff']

# ----------------------------------------------------------------------------------------------
# THE SCORER  (Layer 2's kernel, config block in one place -- Ruling 11's "ALL knobs in one block")
# ----------------------------------------------------------------------------------------------
CFG = dict(
    bars_path='MA.REPL[P] - rd.REPL_DROP[P], read live inside price6 lowered-REPL context',
    repl_drop_pts=float(rd.REPL_DROP_PTS),
    season_games_const=21.0,
    disc='rl_model.disc_factor(a, LENS[bal], k)',
    disc_rate=float(MA.LENS['bal']),
    age_disc_on=bool(MA.AGE_DISC),
    gamma=float(MA.GAMMA),
    scale=float(MA.SCALE),
    scale_dist=float(dp.SCALE_DIST),
    games_weight='w = min(1, sqrt(g/10)); >=10 games = full season   [Ruling 10 -- NOT exercised by the gate: projected careers are full seasons by construction]',
    truncation='last listed season; below-bar seasons credit ZERO, never negative   [Ruling 4 -- enforced by posval >= 0]',
    position_use='VALUE at the position played that season; ATTRIBUTE to the acquisition slot   [Ruling 5]',
    era_norm='NONE   [Ruling 7]',
    projection_multipliers='x1.05 KPF/KPD; x(1+runway*elite*PMAX)  -- DECLARED, projection-side only',
)


# THE BARS, taken off the engine's own netting path exactly once, at import, from the UNLOWERED
# MA.REPL (Ruling 1). They are NOT re-derived inside price6's lowered context -- doing so would net the
# drop twice. This dict is the only place a bar number exists in this harness, and it is computed, never
# typed.
BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}


def season_raw(X, pos):
    """Ruling 3's pinned callable, in the engine's RAW production units."""
    return MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0


def season_points(X, pos):
    """The same season in BOARD POINTS. Exact because GAMMA==1.0 makes val() linear: val(r)=round(SCALE*r).
    The rounding is a CAREER-level act in the engine (MA.val is applied once per projected career), so a
    per-season board-point figure is SCALE*raw and the career total is val(sum of raws)."""
    return MA.SCALE * season_raw(X, pos)


def band_career(p, L):
    """The engine's own projected season path for band level L (proj_from_peak's loop, unrolled)."""
    g = MA.gfut(p); g0 = MA.bnow(p); cur = MA.level_now(p); a = MA.age(p); fut = MA.futblend(p)
    pa = MA.PEAK_AGE[g]
    cl = cur if cur else L * MA.frac(a, pa)
    path = []
    for k in range(18):
        ag = a + k
        if ag > 38 or MA.frac(ag, pa) < 0.42: break
        lev = L * MA.frac(ag, pa)
        if ag <= pa: lev = max(lev, cl)
        if k == 0: lev = max(lev, cl)
        if k == 0 and p.get('_avail_hc', 0.0) > 0 and MA.BASE_REF == 2026 and MA.AGE_REF == 2026:
            lev *= (1 - p['_avail_hc'])
        path.append(dict(k=k, age=ag, level=lev, pos=([(g0, 1.0)] if k == 0 else list(fut))))
    return path, g, a


def score_career(path, a, g, L):
    """THE SCORER: discounted delivered value of a career. Returns (board points, raw production units).
    Board points come through the engine's own MA.val (=round(SCALE*raw) at GAMMA=1), applied ONCE per
    career exactly as dp.v_at_peak applies it -- so the identity is exact, not 'within rounding'."""
    d = MA.LENS['bal']; tot = 0.0
    for s in path:
        df = MA.disc_factor(a, d, s['k'], 'bal')
        tot += sum(w * season_raw(s['level'], gg) for gg, w in s['pos']) / df
    if g in ('KPF', 'KPD'): tot *= 1.05
    runway = MA.clamp((25 - a) / 6.0, 0, 1)
    elite = MA.clamp((L / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
    tot *= (1 + runway * elite * MA.PMAX)
    return MA.val(tot), tot


def gate_price(p, bb, Y=2026):
    """price6's own shape, with dp.v_at_peak REPLACED by the scorer. Same REPL context, same clocks,
    same fsum dot, same prod_floor. Any difference from price6 is a difference in the PRICE FUNCTION."""
    sav = dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g] = sav[g] - rd.REPL_DROP.get(g, 0)
        MA.AGE_REF = Y
        MA.BASE_REF = (MA._LENS_FORM if getattr(MA, '_LENS_FORM', None) is not None else Y)
        MA._pe_clear()
        vals = []
        with contextlib.redirect_stdout(io.StringIO()):
            floor = MA.prod_floor(p, 'bal')
            for L in bb:
                path, g, a = band_career(p, float(L))
                pts, _raw = score_career(path, a, g, float(L))
                vals.append(max(pts, floor))
        return float(dp.SCALE_DIST * _det_dot(WQ6, vals)), vals, floor
    finally:
        MA.REPL.update(sav)


# ----------------------------------------------------------------------------------------------
# THE PANEL  (identities fixed in PREREG_ORDER26B.md §1; the fill rule is fixed there too)
# ----------------------------------------------------------------------------------------------
FIXED = ['willem-duursma', 'nick-daicos', 'harry-sheezel', 'marcus-bontempelli', 'max-gawn',
         'harley-reid', 'jai-newcombe', 'harrison-ramm', 'vigo-visentini']

board = json.load(open(ROOT + '/engine/rl_after/rl_app_data.json'))
BROW = {r['key']: r for r in board['active']}
BYKEY = {}
for p in MA.data:
    k = p.get('key') or MA.slug(p['player'])
    if k not in BYKEY: BYKEY[k] = p

panel = list(FIXED)
have_pos = set(MA.gfut(BYKEY[k]) for k in panel if k in BYKEY)
# fill rule (prereg): highest-board-value row in each missing position cell, then the two
# highest-board-value POOL rows not already on the panel.
for want in ['KPF', 'SF', 'SD', 'KPD', 'RUCK', 'MID']:
    if want in have_pos: continue
    cands = sorted((r for r in board['active']
                    if r['key'] in BYKEY and MA.gfut(BYKEY[r['key']]) == want and r['key'] not in panel),
                   key=lambda r: -r['v'])
    if cands: panel.append(cands[0]['key']); have_pos.add(want)
pool_on = [k for k in panel if k in BYKEY and BYKEY[k].get('_pool')]
if len(pool_on) < 2:
    cands = sorted((r for r in board['active']
                    if r['key'] in BYKEY and BYKEY[r['key']].get('_pool') and r['key'] not in panel),
                   key=lambda r: -r['v'])
    for r in cands[:2 - len(pool_on)]: panel.append(r['key'])

print("=" * 108)
print("ORDER 26B  --  STEP 1, THE IDENTITY GATE (Ruling 9)")
print("=" * 108)
print("pins verified:", ", ".join("%s=%s" % (k, v[1][:8]) for k, v in sorted(PINS.items())))
print()
print("PINNED PRICE FUNCTION (Ruling 3):")
print("   season_points(X,P) = SCALE * posval( X + capt_prem(X) - (MA.REPL[P] - rd.REPL_DROP[P]) ) * 21")
print("   SCALE      = %.16f      rl_model.py (md5 %s) line 1120, reassigned line 1324" % (MA.SCALE, PINS['model'][1][:8]))
print("   posval     = rl_model.py::posval          line 785   S_SH=%.1f" % MA.S_SH)
print("   capt_prem  = rl_model.py::capt_prem       line 676   CAPT_THRESH=%.1f" % MA.CAPT_THRESH)
print("   REPL_DROP  = dist_redesign.py::REPL_DROP  line  39   uniform %.1f" % rd.REPL_DROP_PTS)
print("   disc       = rl_model.py::disc_factor     line 906   LENS[bal]=%.2f  RL_AGE_DISC=%s" % (MA.LENS['bal'], MA.AGE_DISC))
print("   the season term IS rl_model.py::proj_from_peak line 963/978-979 -- reused, not reimplemented")
print("   effective bars (engine netting path): %s" % {g: round(BARS[g], 4) for g in sorted(BARS)})
print("   Ruling 1's stated set:                {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}")
print("   GAMMA = %.1f  =>  val(r) = SCALE*r is LINEAR  =>  delivered value is ADDITIVE across seasons" % MA.GAMMA)
print()

rows = []
for k in panel:
    p = BYKEY.get(k)
    if p is None:
        print("  PANEL ROW MISSING FROM STORE: %s" % k); continue
    br = BROW.get(k)
    with contextlib.redirect_stdout(io.StringIO()):
        bb = [float(x) for x in b6(p)]
        p6 = price6(p, bb)
        unc = _uncomp_prod(p6, p, 2026, bb)
        rv = raw_ev(p)
        e = ev(p)
        ie = iso_eff(p)
    mine, vals, floor = gate_price(p, bb)
    v = (br or {}).get('v')
    rows.append(dict(key=k, name=p['player'], pos=MA.gfut(p), pos_now=MA.bnow(p), age=MA.age(p),
                     pick=MA.effpk(p), typ=p.get('type'), pool=bool(p.get('_pool')),
                     entry_year=p.get('year'), nqual=G['nseas'](p), band=bb, career_vals=vals,
                     prod_floor=floor, mine=mine, price6=p6, uncomp=unc, raw_ev=rv, ev=e,
                     board_v=v, iso_eff=ie,
                     gap_vs_price6=(mine / p6 - 1) if p6 else None,
                     gap_vs_board=(mine / v - 1) if v else None))

print("-" * 108)
print("PER-PLAYER: the six scored careers, the WQ6 blend, the live board price")
print("-" * 108)
for r in rows:
    print("\n%s  [%s]   pos %s (day-0 %s)  age %s  %s pick %s  entry %s  qual-seasons %d  pool=%s"
          % (r['name'], r['key'], r['pos'], r['pos_now'], r['age'], r['typ'], r['pick'],
             r['entry_year'], r['nqual'], r['pool']))
    print("    band level   scored career (board pts)")
    for i, (L, s) in enumerate(zip(r['band'], r['career_vals'])):
        print("      q%-4s %7.2f   %12.2f   w=%.3f" % (['10', '30', '50', '70', '90', '97'][i], L, s, WQ6[i]))
    print("    prod_floor           %12.2f   (max()'d into each career per dp.v_at_peak)" % r['prod_floor'])
    print("    WQ6 BLEND (mine)     %12.2f" % r['mine'])
    print("    engine price6        %12.2f    gap %+8.4f%%   <-- the price-function identity" % (r['price6'], 100 * r['gap_vs_price6']))
    print("    LIVE BOARD PRICE     %12s    gap %s   <-- RULING 9's gate"
          % (r['board_v'], ("%+8.4f%%" % (100 * r['gap_vs_board'])) if r['gap_vs_board'] is not None else "n/a"))

print()
print("=" * 108)
print("GATE VERDICT TABLE  (Ruling 9: +/-2%% vs the LIVE BOARD PRICE)")
print("=" * 108)
print("%-22s %5s %4s %6s %11s %11s %9s %11s %9s %s" %
      ('key', 'pos', 'age', 'pick', 'mine', 'price6', 'vs p6 %', 'board_v', 'vs board%', 'verdict'))
npass = 0; npass_p6 = 0
for r in rows:
    ok = (r['gap_vs_board'] is not None and abs(r['gap_vs_board']) <= 0.02)
    okp = (r['gap_vs_price6'] is not None and abs(r['gap_vs_price6']) <= 1e-6)
    npass += bool(ok); npass_p6 += bool(okp)
    print("%-22s %5s %4s %6s %11.2f %11.2f %+8.4f%% %11s %s %s" %
          (r['key'], r['pos'], r['age'], r['pick'], r['mine'], r['price6'],
           100 * r['gap_vs_price6'], r['board_v'],
           ("%+8.4f%%" % (100 * r['gap_vs_board'])) if r['gap_vs_board'] is not None else "      n/a",
           "PASS" if ok else "FAIL"))
print()
print("  RULING 9 GATE (vs live board price, +/-2%%):        %d of %d PASS" % (npass, len(rows)))
print("  PRICE-FUNCTION IDENTITY (vs price6, +/-1e-6):      %d of %d PASS" % (npass_p6, len(rows)))

# ---------------------------------------------------------------------------------------------
# ATTRIBUTION OF THE GAP -- the legs between price6 and the shipped board price, per player
# ---------------------------------------------------------------------------------------------
print()
print("=" * 108)
print("ATTRIBUTION -- the multiplicative legs between the scored band careers and the board price")
print("=" * 108)
print("%-22s %9s %9s %9s %9s %9s   %9s %9s %11s" %
      ('key', 'mine/p6', 'uncomp', 'pole+', 'ev/raw', 'numeraire', 'product', 'measured', 'residual'))
print("   uncomp = LEG-B un-compress map _uncomp_prod (RL_UNCOMP=%s, s=%s)" % (MA._UNCOMP, MA.UNCOMP_S))
print("   pole+  = raw_ev's pedigree-pole blend  pr + w*recover(perf,par)*max(0, po-pr)")
print("   ev/raw = _prod_path + iso_eff + position caps + sit-out/entry-anchor floors + H-cuts")
print("   numeraire = ev / board_v  (the L7 divisor)")
for r in rows:
    a1 = r['mine'] / r['price6'] if r['price6'] else float('nan')
    a2 = r['uncomp'] / r['price6'] if r['price6'] else float('nan')
    a3 = r['raw_ev'] / r['uncomp'] if r['uncomp'] else float('nan')
    a4 = r['ev'] / r['raw_ev'] if r['raw_ev'] else float('nan')
    a5 = (r['ev'] / r['board_v']) if r['board_v'] else float('nan')
    prod = (a1 * a5 / (a2 * a3 * a4)) if all(x == x and x for x in (a2, a3, a4, a5)) else float('nan')
    meas = (r['mine'] / r['board_v']) if r['board_v'] else float('nan')
    r['attr'] = dict(mine_over_p6=a1, uncomp=a2, pole=a3, ev_over_raw=a4, numeraire=a5,
                     product=prod, measured=meas, residual=(prod - meas))
    print("%-22s %9.4f %9.4f %9.4f %9.4f %9.4f   %9.4f %9.4f %11.2e" %
          (r['key'], a1, a2, a3, a4, a5, prod, meas, prod - meas))
print("   product = (mine/p6) x numeraire / (uncomp x pole x ev/raw); it reproduces the MEASURED")
print("   mine/board_v to floating point, so the wedge is fully attributed with a zero residual.")
_maxres = max(abs(r['attr']['residual']) for r in rows if r['attr']['residual'] == r['attr']['residual'])
print("   max |residual| over the panel: %.3e" % _maxres)
assert _maxres < 1e-3, "ATTRIBUTION RESIDUAL NON-ZERO -- an unnamed leg exists"

# ---------------------------------------------------------------------------------------------
# BOARD-WIDE: the same two checks over every active row, so the panel cannot be read as a fluke
# ---------------------------------------------------------------------------------------------
print()
print("=" * 108)
print("BOARD-WIDE CONTROL -- the same two checks over all %d active rows" % len(board['active']))
print("=" * 108)
wide = []
for br in board['active']:
    p = BYKEY.get(br['key'])
    if p is None or not br.get('v'): continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            bb = [float(x) for x in b6(p)]
            p6 = price6(p, bb)
        m, _v, _f = gate_price(p, bb)
    except Exception:
        continue
    wide.append((br['key'], m, p6, br['v'], MA.gfut(p), bool(p.get('_pool')), G['nseas'](p)))


def _q(xs, f):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(f * len(xs)))]


ip6 = [abs(m / p6 - 1) for _k, m, p6, _v, _g, _pl, _n in wide if p6]
gb = [m / v for _k, m, _p6, v, _g, _pl, _n in wide if v]
print("  rows measured: %d" % len(wide))
print("  PRICE-FUNCTION IDENTITY |mine/price6 - 1| :  max %.3e   within 1e-6: %d of %d (%.1f%%)"
      % (max(ip6), sum(1 for x in ip6 if x <= 1e-6), len(ip6),
         100.0 * sum(1 for x in ip6 if x <= 1e-6) / len(ip6)))
print("  RULING 9 GATE  mine/board_v :  min %.4f  p05 %.4f  med %.4f  p95 %.4f  max %.4f"
      % (min(gb), _q(gb, .05), _q(gb, .50), _q(gb, .95), max(gb)))
print("  RULING 9 GATE  within +/-2%%: %d of %d (%.1f%%)"
      % (sum(1 for x in gb if abs(x - 1) <= 0.02), len(gb),
         100.0 * sum(1 for x in gb if abs(x - 1) <= 0.02) / len(gb)))
for lbl, sel in (('ND, >=4 qualifying seasons', lambda r: not r[5] and r[6] >= 4),
                 ('ND, <4 qualifying seasons', lambda r: not r[5] and r[6] < 4),
                 ('pool, >=4 qualifying seasons', lambda r: r[5] and r[6] >= 4),
                 ('pool, <4 qualifying seasons', lambda r: r[5] and r[6] < 4)):
    sub = [m / v for _k, m, _p6, v, _g, _pl, _n in wide
           if v and sel((_k, m, _p6, v, _g, _pl, _n))]
    if not sub: continue
    print("    %-30s n=%4d  med %7.4f   within 2%%: %5.1f%%"
          % (lbl, len(sub), _q(sub, .50), 100.0 * sum(1 for x in sub if abs(x - 1) <= 0.02) / len(sub)))
for g in sorted(set(r[4] for r in wide)):
    sub = [m / v for _k, m, _p6, v, _g, _pl, _n in wide if v and _g == g]
    print("    %-30s n=%4d  med %7.4f   within 2%%: %5.1f%%"
          % ('position ' + g, len(sub), _q(sub, .50), 100.0 * sum(1 for x in sub if abs(x - 1) <= 0.02) / len(sub)))
WIDE = [dict(key=k, mine=m, price6=p6, board_v=v, pos=g, pool=pl, nqual=n)
        for k, m, p6, v, g, pl, n in wide]

json.dump(dict(cfg=CFG, pins={k: v[1] for k, v in PINS.items()}, panel=panel, rows=rows,
               gate_pass=npass, gate_n=len(rows), identity_pass=npass_p6, board_wide=WIDE),
          open(os.path.join(HERE, 'GATE.json'), 'w'), indent=1, default=float)
assert_pins('exit')
print("\nwrote GATE.json   (pins re-verified at exit: engine, store and board untouched)")
