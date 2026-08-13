#!/usr/bin/env python3
"""ORDER 28 -- THE IDENTITY GATE RE-RUN UNDER THE DIALED ENGINE.

Adapted from o26b_gate.py (copied verbatim into inputs/, md5 in inputs/MD5SUMS.txt). The ONE
substantive change: the scorer and the engine BOTH run the ORDER 28 grace dial, and the scorer hands
`disc_factor` the SAME grace the engine computes -- MA.grace_years(p) -- rather than re-deriving it.
That is the point of the gate: if the grace reached one side and not the other, the price-function
identity would break, and the 26B-V landing constraint (one rule, both sides) would be unmet.

READ-ONLY on the checkout: the engine is loaded from a staged copy under the scratchpad.

WHAT IS PINNED AND WHAT IS NOT
------------------------------
store and the LIVE board are pinned to the 26B values (unchanged by this order -- ORDER 28 writes no
store byte and lands no board). The three ENGINE files carry the dial, so their md5s MOVED; they are
recorded, not asserted against the 26B values, and the DIAL-OFF byte-identity of the board is the
proof that the move is inert (BYTE_IDENTITY_OFF.txt).

TWO BOARD READINGS, BOTH PRINTED
--------------------------------
Ruling 9's +/-2% leg compares the scorer to A BOARD. With the dial ON the scorer moves, so:
  (1) vs the LIVE board 88ce647f (dial OFF)      -- MUST degrade for young rows; degradation is the
                                                    expected reading, not a failure;
  (2) vs the DIAL-ON variant board (step 3)      -- the like-for-like reading, and the one that means
                                                    something.
Both are computed here when the variant board is present.

  usage:  RL_GRACE=1 python3 o28_gate.py        ->  GATE28.json / GATE28_out.txt
"""
import os, sys, io, json, contextlib, hashlib, shutil, math

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng28_gate/rl_after'
VARIANT_BOARD = SP + '/bb_on1/rl_after/rl_app_data.json'    # the step-3 dial-ON variant board

DIAL = os.environ.get('RL_GRACE', '0')

# store + LIVE board are UNMOVED by this order and are asserted; the engine files carry the dial.
PINS_ASSERT = {'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
               'board': ('engine/rl_after/rl_app_data.json',   '88ce647f531030d8d2e094188b258191')}
PINS_RECORD = {'engine':  'engine/rl_after/_merged_recover.py',
               'model':   'engine/rl_after/rl_model.py',
               'netting': 'engine/forward_valuation/dist_redesign.py',
               'distpx':  'engine/forward_valuation/distribution_pricing.py'}
PRE28 = {'engine': '3f1468e5468462ab789e49aace264c90', 'model': 'e5eb5e4405c09eebef45a9db89f014bc',
         'netting': '48ea1bfeccc6d1ea51add66b0cb93965',
         'distpx': None}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s %s != %s (%s)" % (k, _md5(os.path.join(ROOT, rel)), exp, rel)
           for k, (rel, exp) in PINS_ASSERT.items() if _md5(os.path.join(ROOT, rel)) != exp]
    if bad: raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')
shutil.rmtree(SP + '/eng28_gate', ignore_errors=True)
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

if bool(MA.RL_GRACE) != (DIAL != '0'):
    raise SystemExit("DIAL MISMATCH: RL_GRACE env=%r but MA.RL_GRACE=%r" % (DIAL, MA.RL_GRACE))

BARS = {g: MA.REPL[g] - rd.REPL_DROP.get(g, 0.0) for g in MA.REPL}
CFG = dict(dial='RL_GRACE=%s  (MA.RL_GRACE=%s, GRACE_G=%s, GRACE_MAX_ENTRY_AGE=%s)'
                % (DIAL, MA.RL_GRACE, MA.GRACE_G, MA.GRACE_MAX_ENTRY_AGE),
           disc='rl_model.disc_factor(a, LENS[bal], k, "bal", grace=MA.grace_years(p))',
           disc_rate=float(MA.LENS['bal']), age_disc_on=bool(MA.AGE_DISC),
           gamma=float(MA.GAMMA), scale=float(MA.SCALE), scale_dist=float(dp.SCALE_DIST),
           repl_drop_pts=float(rd.REPL_DROP_PTS), season_games_const=21.0)


def season_raw(X, pos):
    return MA.posval(X + MA.capt_prem(X) - BARS[pos]) * 21.0


def band_career(p, L):
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


def score_career(path, a, g, L, grace):
    """THE SCORER. ORDER 28: `grace` is handed to the engine's OWN disc_factor, and it is the engine's
    OWN MA.grace_years(p) -- never a second implementation of the rule."""
    d = MA.LENS['bal']; tot = 0.0
    for s in path:
        df = MA.disc_factor(a, d, s['k'], 'bal', grace)
        tot += sum(w * season_raw(s['level'], gg) for gg, w in s['pos']) / df
    if g in ('KPF', 'KPD'): tot *= 1.05
    runway = MA.clamp((25 - a) / 6.0, 0, 1)
    elite = MA.clamp((L / MA.PEAK[g] - 0.97) / 0.30, 0, 1)
    tot *= (1 + runway * elite * MA.PMAX)
    return MA.val(tot), tot


def gate_price(p, bb, Y=2026):
    sav = dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g] = sav[g] - rd.REPL_DROP.get(g, 0)
        MA.AGE_REF = Y
        MA.BASE_REF = (MA._LENS_FORM if getattr(MA, '_LENS_FORM', None) is not None else Y)
        MA._pe_clear()
        gr = MA.grace_years(p)
        vals = []
        with contextlib.redirect_stdout(io.StringIO()):
            floor = MA.prod_floor(p, 'bal')
            for L in bb:
                path, g, a = band_career(p, float(L))
                pts, _raw = score_career(path, a, g, float(L), gr)
                vals.append(max(pts, floor))
        return float(dp.SCALE_DIST * _det_dot(WQ6, vals)), vals, floor, gr
    finally:
        MA.REPL.update(sav)


FIXED = ['willem-duursma', 'nick-daicos', 'harry-sheezel', 'marcus-bontempelli', 'max-gawn',
         'harley-reid', 'jai-newcombe', 'harrison-ramm', 'vigo-visentini']

board = json.load(open(ROOT + '/engine/rl_after/rl_app_data.json'))
BROW = {r['key']: r for r in board['active']}
VROW = {}
if os.path.exists(VARIANT_BOARD):
    VROW = {r['key']: r for r in json.load(open(VARIANT_BOARD))['active']}
BYKEY = {}
for p in MA.data:
    k = p.get('key') or MA.slug(p['player'])
    if k not in BYKEY: BYKEY[k] = p

panel = list(FIXED)
have_pos = set(MA.gfut(BYKEY[k]) for k in panel if k in BYKEY)
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

LOG = []
def P(s=''):
    print(s); LOG.append(s)


P("=" * 122)
P("ORDER 28  --  THE IDENTITY GATE, RE-RUN UNDER THE DIALED ENGINE")
P("=" * 122)
P("  DIAL: %s" % CFG['dial'])
P("  pins ASSERTED (unmoved by this order): store=%s  live board=%s"
  % (PINS_ASSERT['store'][1][:8], PINS_ASSERT['board'][1][:8]))
P("  engine files RECORDED (they carry the dial; dial-off byte-identity is the proof they are inert):")
for k, rel in sorted(PINS_RECORD.items()):
    now = _md5(os.path.join(ROOT, rel))
    P("     %-8s %s  %s%s" % (k, now[:8], rel,
                              ('   (pre-28 %s)' % PRE28[k][:8]) if PRE28.get(k) else ''))
P("  variant (dial-ON) board present: %s%s"
  % (bool(VROW), ('  md5 ' + _md5(VARIANT_BOARD)[:8]) if VROW else ''))
P()
P("  season_points(X,P) = SCALE * posval( X + capt_prem(X) - (MA.REPL[P] - rd.REPL_DROP[P]) ) * 21")
P("  SCALE %.16f   posval S_SH=%.1f   capt_prem CAPT_THRESH=%.1f   REPL_DROP %.1f"
  % (MA.SCALE, MA.S_SH, MA.CAPT_THRESH, rd.REPL_DROP_PTS))
P("  disc  rl_model::disc_factor  LENS[bal]=%.2f  RL_AGE_DISC=%s  GAMMA=%.1f"
  % (MA.LENS['bal'], MA.AGE_DISC, MA.GAMMA))
P("  effective bars: %s" % {g: round(BARS[g], 4) for g in sorted(BARS)})
P()

rows = []
for k in panel:
    p = BYKEY.get(k)
    if p is None:
        P("  PANEL ROW MISSING FROM STORE: %s" % k); continue
    br = BROW.get(k); vr = VROW.get(k)
    with contextlib.redirect_stdout(io.StringIO()):
        bb = [float(x) for x in b6(p)]
        p6 = price6(p, bb)
        unc = _uncomp_prod(p6, p, 2026, bb)
        rv = raw_ev(p)
        e = ev(p)
        ie = iso_eff(p)
    mine, vals, floor, gr = gate_price(p, bb)
    v = (br or {}).get('v'); vv = (vr or {}).get('v')
    rows.append(dict(key=k, name=p['player'], pos=MA.gfut(p), pos_now=MA.bnow(p), age=MA.age(p),
                     pick=MA.effpk(p), typ=p.get('type'), pool=bool(p.get('_pool')),
                     entry_year=p.get('year'), entry_age=p['year'] - MA.by(p), grace=gr,
                     nqual=G['nseas'](p), band=bb, career_vals=vals, prod_floor=floor,
                     mine=mine, price6=p6, uncomp=unc, raw_ev=rv, ev=e,
                     board_v=v, variant_v=vv, iso_eff=ie,
                     gap_vs_price6=(mine / p6 - 1) if p6 else None,
                     gap_vs_board=(mine / v - 1) if v else None,
                     gap_vs_variant=(mine / vv - 1) if vv else None))

P("-" * 122)
P("PER-PLAYER: the six scored careers, the WQ6 blend, and BOTH board readings")
P("-" * 122)
for r in rows:
    P("\n%s  [%s]   pos %s (day-0 %s)  age %s  %s pick %s  entry %s (age %s)  grace=%d  qual %d  pool=%s"
      % (r['name'], r['key'], r['pos'], r['pos_now'], r['age'], r['typ'], r['pick'],
         r['entry_year'], r['entry_age'], r['grace'], r['nqual'], r['pool']))
    for i, (L, s) in enumerate(zip(r['band'], r['career_vals'])):
        P("      q%-4s %7.2f   %12.2f   w=%.3f" % (['10', '30', '50', '70', '90', '97'][i], L, s, WQ6[i]))
    P("    prod_floor           %12.2f" % r['prod_floor'])
    P("    WQ6 BLEND (mine)     %12.2f" % r['mine'])
    P("    engine price6        %12.2f    gap %+9.6f%%   <-- THE PRICE-FUNCTION IDENTITY (dial on both sides)"
      % (r['price6'], 100 * r['gap_vs_price6']))
    P("    LIVE board (dial-off)%12s    gap %s"
      % (r['board_v'], ("%+9.4f%%" % (100 * r['gap_vs_board'])) if r['gap_vs_board'] is not None else "n/a"))
    P("    VARIANT board (dial-on)%10s    gap %s   <-- the like-for-like Ruling-9 read"
      % (r['variant_v'], ("%+9.4f%%" % (100 * r['gap_vs_variant'])) if r['gap_vs_variant'] is not None else "n/a"))

P()
P("=" * 122)
P("GATE VERDICT TABLE")
P("=" * 122)
P("%-22s %5s %4s %6s %5s %11s %11s %11s %10s %10s  %s"
  % ('key', 'pos', 'age', 'pick', 'grace', 'mine', 'price6', 'vs p6 %', 'vs LIVE%', 'vs VAR%', 'R9(var)'))
npass_live = npass_var = npass_p6 = 0
for r in rows:
    okl = (r['gap_vs_board'] is not None and abs(r['gap_vs_board']) <= 0.02)
    okv = (r['gap_vs_variant'] is not None and abs(r['gap_vs_variant']) <= 0.02)
    okp = (r['gap_vs_price6'] is not None and abs(r['gap_vs_price6']) <= 1e-6)
    npass_live += bool(okl); npass_var += bool(okv); npass_p6 += bool(okp)
    P("%-22s %5s %4s %6s %5d %11.2f %11.2f %+10.6f%% %+9.3f%% %s  %s"
      % (r['key'], r['pos'], r['age'], r['pick'], r['grace'], r['mine'], r['price6'],
         100 * r['gap_vs_price6'], 100 * r['gap_vs_board'],
         ("%+9.3f%%" % (100 * r['gap_vs_variant'])) if r['gap_vs_variant'] is not None else "      n/a",
         "PASS" if okv else "FAIL"))
P()
P("  PRICE-FUNCTION IDENTITY (|mine/price6 - 1| <= 1e-6):   %d of %d PASS   <-- THE ORDER-28 GATE"
  % (npass_p6, len(rows)))
P("  RULING 9 +/-2%% vs the LIVE (dial-OFF) board:            %d of %d  [expected to DEGRADE -- the "
  "scorer moved and that board did not]" % (npass_live, len(rows)))
P("  RULING 9 +/-2%% vs the VARIANT (dial-ON) board:          %d of %d  [the like-for-like read]"
  % (npass_var, len(rows)))
_mx = max(abs(r['gap_vs_price6']) for r in rows)
P("  max |mine/price6 - 1| over the panel: %.3e" % _mx)

# ------------------------------------------------------------------ attribution (unchanged shape)
P()
P("=" * 122)
P("ATTRIBUTION -- the multiplicative legs between the scored band careers and the LIVE board price")
P("=" * 122)
P("%-22s %9s %9s %9s %9s %9s   %9s %9s %11s" %
  ('key', 'mine/p6', 'uncomp', 'pole+', 'ev/raw', 'numeraire', 'product', 'measured', 'residual'))
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
    P("%-22s %9.4f %9.4f %9.4f %9.4f %9.4f   %9.4f %9.4f %11.2e" %
      (r['key'], a1, a2, a3, a4, a5, prod, meas, prod - meas))
_maxres = max(abs(r['attr']['residual']) for r in rows if r['attr']['residual'] == r['attr']['residual'])
P("   max |residual| over the panel: %.3e" % _maxres)
assert _maxres < 1e-3, "ATTRIBUTION RESIDUAL NON-ZERO -- an unnamed leg exists"

# ------------------------------------------------------------------ board-wide control
P()
P("=" * 122)
P("BOARD-WIDE CONTROL -- the same checks over all %d active rows" % len(board['active']))
P("=" * 122)
wide = []
for br in board['active']:
    p = BYKEY.get(br['key'])
    if p is None or not br.get('v'): continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            bb = [float(x) for x in b6(p)]
            p6 = price6(p, bb)
        m, _v, _f, gr = gate_price(p, bb)
    except Exception:
        continue
    wide.append((br['key'], m, p6, br['v'], MA.gfut(p), bool(p.get('_pool')), G['nseas'](p),
                 gr, (VROW.get(br['key']) or {}).get('v')))


def _q(xs, f):
    xs = sorted(xs); return xs[min(len(xs) - 1, int(f * len(xs)))]


ip6 = [abs(m / p6 - 1) for _k, m, p6, _v, _g, _pl, _n, _gr, _vv in wide if p6]
gb = [m / v for _k, m, _p6, v, _g, _pl, _n, _gr, _vv in wide if v]
gv = [m / vv for _k, m, _p6, _v, _g, _pl, _n, _gr, vv in wide if vv]
P("  rows measured: %d   (of which grace>0: %d)" % (len(wide), sum(1 for r in wide if r[7])))
P("  PRICE-FUNCTION IDENTITY |mine/price6 - 1| :  max %.3e   within 1e-6: %d of %d (%.1f%%)"
  % (max(ip6), sum(1 for x in ip6 if x <= 1e-6), len(ip6),
     100.0 * sum(1 for x in ip6 if x <= 1e-6) / len(ip6)))
P("  vs LIVE board   mine/v :  min %.4f  p05 %.4f  med %.4f  p95 %.4f  max %.4f   within 2%%: %d of %d (%.1f%%)"
  % (min(gb), _q(gb, .05), _q(gb, .50), _q(gb, .95), max(gb),
     sum(1 for x in gb if abs(x - 1) <= 0.02), len(gb),
     100.0 * sum(1 for x in gb if abs(x - 1) <= 0.02) / len(gb)))
if gv:
    P("  vs VARIANT board mine/v:  min %.4f  p05 %.4f  med %.4f  p95 %.4f  max %.4f   within 2%%: %d of %d (%.1f%%)"
      % (min(gv), _q(gv, .05), _q(gv, .50), _q(gv, .95), max(gv),
         sum(1 for x in gv if abs(x - 1) <= 0.02), len(gv),
         100.0 * sum(1 for x in gv if abs(x - 1) <= 0.02) / len(gv)))
for lbl, sel in (('ND, >=4 qualifying seasons', lambda r: not r[5] and r[6] >= 4),
                 ('ND, <4 qualifying seasons', lambda r: not r[5] and r[6] < 4),
                 ('pool, >=4 qualifying seasons', lambda r: r[5] and r[6] >= 4),
                 ('pool, <4 qualifying seasons', lambda r: r[5] and r[6] < 4),
                 ('GRACED rows (grace>0)', lambda r: r[7] > 0),
                 ('UN-graced rows (grace==0)', lambda r: r[7] == 0)):
    sub = [r[1] / r[3] for r in wide if r[3] and sel(r)]
    subv = [r[1] / r[8] for r in wide if r[8] and sel(r)]
    if not sub: continue
    P("    %-28s n=%4d  vs LIVE med %7.4f within2%% %5.1f%%   |  vs VAR med %s within2%% %s"
      % (lbl, len(sub), _q(sub, .50), 100.0 * sum(1 for x in sub if abs(x - 1) <= 0.02) / len(sub),
         ("%7.4f" % _q(subv, .50)) if subv else '    n/a',
         ("%5.1f%%" % (100.0 * sum(1 for x in subv if abs(x - 1) <= 0.02) / len(subv))) if subv else '  n/a'))

WIDE = [dict(key=k, mine=m, price6=p6, board_v=v, variant_v=vv, pos=g, pool=pl, nqual=n, grace=gr)
        for k, m, p6, v, g, pl, n, gr, vv in wide]
json.dump(dict(cfg=CFG, dial=DIAL, pins_asserted={k: v[1] for k, v in PINS_ASSERT.items()},
               pins_recorded={k: _md5(os.path.join(ROOT, rel)) for k, rel in PINS_RECORD.items()},
               panel=panel, rows=rows, identity_pass=npass_p6, gate_n=len(rows),
               r9_pass_live=npass_live, r9_pass_variant=npass_var, board_wide=WIDE),
          open(os.path.join(HERE, 'GATE28.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'GATE28_out.txt'), 'w').write("\n".join(LOG) + "\n")
assert_pins('exit')
P("\nwrote GATE28.json / GATE28_out.txt   (store + live board re-verified unmoved at exit)")
