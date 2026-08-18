#!/usr/bin/env python3
"""ORDER R — CONTINUITY, ON THE EFFECTIVE CONSTANTS.

ORDER Q's oq_continuity.py with ONE substantive change: THETA_R and TMAX are read from the ORDER R
EFFECTIVE constants (O39_THETA_R / O39_TMAX) rather than ORDER P's, so the axes are swept on the
surface the board was actually built on. Reading ORDER P's constants while pricing a softened board
would sweep a surface no board uses. With both ORDER R dials unset the effective constants ARE the
ORDER P constants bit for bit, so every ORDER Q number reproduces.

Original ORDER Q header follows.


ORDER Q — CONTINUITY, INCLUDING THE AXIS ORDER P DID NOT TEST.

THE FINDING THIS SCRIPT EXISTS FOR. ORDER P's own continuity suite (op_continuity.py) has an AGE
axis, but that axis sweeps `MA.o36_bar(pos, age)` — the S1 age BAR — and its own header calls it
"UNCHANGED by this order". It never sweeps `o37_factor` across age and it never sweeps a row's
PRICE across age. So the age-24 handover ORDER P introduced was never tested by ORDER P's suite.
That is confirmed here by re-reading the suite and by running the axis it left out.

Six axes are carried from ORDER P and re-run for every variant, and TWO NEW ONES are added:
  AGE (THE CHARGE)  — the charge factor across ages 18..30 at fixed games and fixed surplus. NEW.
  AGE (THE PRICE)   — every real row's price re-formed with the charge evaluated one year older. NEW.
  GAMES             — the charge across 0..400 games at 0.01, at seven surplus levels.
  SURPLUS           — the charge across 100 points of surplus at 0.01.
  ENTRY PRICE       — the premium, and the charged pedigree LEG, across 40..6,000 at 0.1% of price.
                      Under FIX A the LEG must be non-decreasing. The residual from the engine's own
                      one-decimal rounding of the premium axis is measured here, not asserted.

Usage: oq_continuity.py TAG [dial=value ...]
"""
import os, sys, io, json, math, contextlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import or_lib as L

TAG = sys.argv[1]
DIALS = dict(x.split('=', 1) for x in sys.argv[2:])
NS = L.load(**DIALS)
NS['_REC'] = L.install_recorder(NS)
import rl_model as MA
FNUM = json.load(open(L.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
OUT = {}
LL = []


def P(s=''):
    print(s); LL.append(str(s))


LAM, G0 = NS['O37_LAMBDA'], NS['O37_G0']
# ORDER R: the EFFECTIVE cap and slope, not ORDER P's. With the R dials unset these are identical.
THR = NS.get('O39_THETA_R', NS['O37_THETA_R'])
S0 = NS['O37_S0']
TMAX = NS.get('O39_TMAX', NS['O37_TMAX'])
ETA, GD = NS['O32_ETA'], NS['O32_GAMMA_D']
A = lambda g: 1.0 - math.exp(-g / G0)
T = lambda s: min(max(1.0 - THR * (s - S0), 0.0), TMAX)
OLDF = lambda g: max(0.0, 1.0 - ETA * ((g / GD) * math.exp(1.0 - g / GD))) if g > 0 else 1.0
ON38 = bool(NS.get('_O38'))
P('=' * 112)
P('ORDER R — CONTINUITY.  tag=%s  dials=%s' % (TAG, DIALS))
P('  EFFECTIVE CONSTANTS THIS SWEEP USES: THETA_R %.8f  TMAX %.6f  BETA_sat %.8f  LAMBDA %.8f'
  % (THR, TMAX, NS.get('O39_BETA_SAT', NS['O37_BETA_SAT']), LAM))
P('  (ORDER P\'s own: THETA_R %.8f  TMAX %.6f  BETA_sat %.8f)'
  % (NS['O37_THETA_R'], NS['O37_TMAX'], NS['O37_BETA_SAT']))
P('=' * 112)

# ---- NEW AXIS 1: THE CHARGE ACROSS AGE ------------------------------------------------------------
P()
P('== NEW AXIS — THE CHARGE ACROSS AGE. This is the axis ORDER P\'s suite did not test. ==')
P('   The charge factor at 20 career games, at four levels of pedigree surplus, ages 18 to 30.')
P('   The factor is what MULTIPLIES the pedigree leg: 1.000 means no charge at all.')


def w_of(age):
    if ON38: return NS['o38_w'](age)
    return 1.0 if age < NS['O37_AGE_GATE'] else 0.0


def fac_at(age, g, s):
    w = w_of(age)
    fP = math.exp(-LAM * A(g) * T(s))
    fK = OLDF(g)
    if w >= 1.0: return fP
    if w <= 0.0: return fK
    return math.exp(w * math.log(fP) + (1.0 - w) * math.log(fK))


agefail = []
P('   %-8s %s' % ('s_P', ' '.join('%7d' % a for a in range(18, 31))))
for s in (-25.0, -10.0, -3.0, 0.0):
    vals = [fac_at(a, 20.0, s) for a in range(18, 31)]
    P('   %-8.1f %s' % (s, ' '.join('%7.4f' % v for v in vals)))
    for i in range(1, len(vals)):
        j = abs(vals[i] - vals[i - 1])
        if j > 1e-9: agefail.append((s, 17 + i, 18 + i, vals[i - 1], vals[i], j))
worst = max((f[5] for f in agefail), default=0.0)
P('   largest step in the charge factor between two consecutive ages: %.4f' % worst)
if agefail:
    P('   the steps, biggest first (surplus, from age, to age, factor before, factor after, step):')
    for f in sorted(agefail, key=lambda z: -z[5])[:6]:
        P('     s_P %+6.1f   age %d -> %d   %.4f -> %.4f   step %.4f' % (f[0], f[1], f[2], f[3], f[4], f[5]))
else:
    P('   NO STEP AT ANY AGE. The charge does not read current age at all.')
OUT['age_charge'] = dict(worst=worst, steps=agefail)

# ---- NEW AXIS 2: THE PRICE ACROSS AGE, ON REAL ROWS -----------------------------------------------
EV = NS['ev']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players: EV(p, 2026)
ROWS = {p['key']: L.assemble(NS, p, 2026) for p in MA.players}
RAW = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players: RAW[p['key']] = EV(p, 2026)
FAC = NS['o38_factor'] if ON38 else NS['o37_factor']
P()
P('== NEW AXIS — THE PRICE ACROSS AGE, ON EVERY REAL ROW ==')
P('   Each row is re-priced with ONLY the charge evaluated one year older. Games, output, bar,')
P('   fade, everything else is held EXACTLY fixed. This isolates the age channel of the charge.')
steps = []
if ON38:
    w0 = NS['o38_w']
for p in MA.players:
    if not p.get('_by'): continue
    k = p['key']; r = ROWS[k]
    if r['ped'] is None: continue
    age = 2026 - int(p['_by']); g = NS['pv_games'](p, 2026)
    if ON38:
        NS['o38_w'] = lambda a, _w=w0, _t=age + 1: _w(_t)
    else:
        pass
    NS['_O37_SCACHE'].clear()
    if '_O38_PCACHE' in NS: NS['_O38_PCACHE'].clear()
    if ON38:
        f1 = FAC(p, 2026, g)
    else:
        wn = 1.0 if (age + 1) < NS['O37_AGE_GATE'] else 0.0
        s = NS['o37_surplus'](p, 2026)
        f1 = (math.exp(-LAM * A(g) * T(s)) if (s is not None and wn >= 1.0) else OLDF(g)) if g > 0 else 1.0
    if ON38: NS['o38_w'] = w0
    NS['_O37_SCACHE'].clear()
    if '_O38_PCACHE' in NS: NS['_O38_PCACHE'].clear()
    p1 = r['prod_leg'] + r['credit'] + r['pi_base_eff'] * r['ped'] * f1
    a0, a1 = int(round(RAW[k] / FNUM)), int(round(p1 / FNUM))
    if a0 > 0:
        steps.append(dict(key=k, name=p.get('player'), age=age, g=g, now=a0, nextyr=a1,
                          ratio=a1 / a0, delta=a1 - a0))
mv = [s for s in steps if s['delta'] != 0]
P('   rows tested: %d   rows whose price moves on the birthday alone: %d' % (len(steps), len(mv)))
P('   largest single jump: %s'
  % (max(('%.4fx (%s, age %d -> %d, %d -> %d)' % (s['ratio'], s['name'], s['age'], s['age'] + 1, s['now'], s['nextyr'])
          for s in steps), key=lambda z: float(z.split('x')[0])) if steps else 'n/a'))
P('   net points handed across the birthday, all rows: %+d' % sum(s['delta'] for s in steps))
P('   %-6s %5s %8s %10s %12s' % ('age', 'n', 'movers', 'gain 50%+', 'net points'))
for a in sorted(set(s['age'] for s in steps)):
    sa = [s for s in steps if s['age'] == a]
    P('   %-6d %5d %8d %10d %+12d' % (a, len(sa), sum(1 for s in sa if s['delta']),
                                      sum(1 for s in sa if s['ratio'] >= 1.5), sum(s['delta'] for s in sa)))
P('   the five largest jumps:')
for s in sorted(steps, key=lambda z: -z['ratio'])[:5]:
    P('     %-26s age %2d -> %2d  %4.0fg   %6d -> %6d   x%.3f' % (s['name'][:26], s['age'], s['age'] + 1,
                                                                  s['g'], s['now'], s['nextyr'], s['ratio']))
OUT['age_price'] = steps

# ---- GAMES ----------------------------------------------------------------------------------------
P()
P('== GAMES — the charge factor, 0 to 400 at 0.01, at seven surplus levels ==')
grise = gjump = 0.0
gcnt = 0
for s in (-33.0, -25.0, -15.0, -8.0, -3.0, 0.0, 8.0):
    prev = None
    for i in range(0, 40001):
        g = i * 0.01
        f = fac_at(20, g, s) if g > 0 else 1.0
        if prev is not None:
            if f > prev + 1e-12: gcnt += 1; grise = max(grise, f - prev)
            gjump = max(gjump, abs(f - prev))
        prev = f
P('   largest step %.3e ; the charge RISES with games at %d of 280,000 steps (largest rise %.3e)'
  % (gjump, gcnt, grise))
OUT['games'] = dict(jump=gjump, rises=gcnt)

# ---- SURPLUS --------------------------------------------------------------------------------------
P()
P('== SURPLUS — the charge factor across 100 points of surplus at 0.01 ==')
srise = 0; sjump = 0.0; prev = None
for i in range(0, 10001):
    s = -60.0 + i * 0.01
    f = fac_at(20, 20.0, s)
    if prev is not None:
        if f < prev - 1e-12: srise += 1
        sjump = max(sjump, abs(f - prev))
    prev = f
P('   largest step %.3e ; a BETTER player is charged MORE at %d of 10,000 steps' % (sjump, srise))
OUT['surplus'] = dict(jump=sjump, worse=srise)

# ---- ENTRY PRICE: THE PREMIUM AND THE LEG ---------------------------------------------------------
P()
P('== ENTRY PRICE — the premium, and THE CHARGED PEDIGREE LEG, across 40 to 6,000 ==')
P('   FIX A\'s whole claim is that the LEG is non-decreasing in entry price. It is measured here on')
P('   a dense sweep, through the engine\'s own o38/o37 objects, not argued.')
PGF = NS['o37_pg']
pfall = 0; pjump = 0.0; prev = None
vs = []
v = 40.0
while v <= 6000.0:
    vs.append(v); v *= 1.001
for cls in ('TALL', 'SMALL'):
    prev = None
    for v in vs:
        y = PGF(v, cls)
        if prev is not None:
            if y < prev - 1e-12: pfall += 1
            pjump = max(pjump, abs(y - prev))
        prev = y
P('   the premium FALLS with price at %d of %d steps; largest one-step move %.4f' % (pfall, 2 * len(vs), pjump))

legfall = collections.Counter()
legworst = {}
for cls, wT, wS in (('TALL', 1.0, 0.0), ('SMALL', 0.0, 1.0)):
    for gg in (5.0, 20.0, 60.0):
        for OUTv in (-30.0, -12.0, -4.0, 0.0, 8.0):
            prev = None; run = None
            for v in vs:
                ve = round(v * NS['_PL_F'], 1)
                x = math.log(ve)
                sx = OUTv - (wT * NS['o38_pg_at'](x, 'TALL') + wS * NS['o38_pg_at'](x, 'SMALL'))
                psi = x - LAM * A(gg) * T(sx)
                if ON38 and NS.get('_O38A'):
                    # the sweep runs upward in price, so the running maximum is carried forward.
                    # It is the SAME object o38_mono computes exactly on the breakpoints; here it is
                    # accumulated on the sweep grid, which is what a dense continuity check needs.
                    run = psi if run is None else max(run, psi)
                    leg = math.exp(run)
                else:
                    leg = math.exp(psi)
                if prev is not None and leg < prev - 1e-12:
                    legfall[(cls, gg, OUTv)] += 1
                    d = (prev - leg) / max(prev, 1e-9)
                    if d > legworst.get('d', 0.0): legworst = dict(d=d, cls=cls, g=gg, out=OUTv, v=v)
                prev = leg
P('   THE CHARGED PEDIGREE LEG across %d price steps x 30 (class, games, surplus) cells:' % len(vs))
P('     cells where the leg FALLS with price: %d of 30 ; total falling steps: %d'
  % (len(legfall), sum(legfall.values())))
if legworst:
    P('     worst single fall: %.3e of the leg, %s g=%.0f OUT=%+.0f at v0 %.0f'
      % (legworst['d'], legworst['cls'], legworst['g'], legworst['out'], legworst['v']))
else:
    P('     worst single fall: NONE')
OUT['price'] = dict(premium_falls=pfall, leg_fall_cells=len(legfall), leg_fall_steps=sum(legfall.values()),
                    worst=legworst)

open(HERE + '/CONTINUITY_%s_out.txt' % TAG, 'w').write('\n'.join(LL) + '\n')
json.dump(OUT, open(HERE + '/CONTINUITY_%s.json' % TAG, 'w'), indent=1, default=str)
print('\nwrote CONTINUITY_%s_out.txt' % TAG)
