#!/usr/bin/env python3
"""ORDER P BUILD — FALSIFIER B11: prove the WIRED premium surface is ORDER P's own surface.

The engine carries the pedigree premium as a literal grid. This file reads that literal OUT OF THE
ENGINE SOURCE, re-runs ORDER P's `op_lib.Premium` from scratch on ORDER P's own population, and
compares them. It also rebuilds the whole surplus s_P from the wired arithmetic and compares that,
row by row, against `op_lib.perf_surplus_P` on the ORDER K matrix.

Nothing here is fitted. It is a transcription proof.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 op_surface_check.py
"""
import json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB
ENGINE = os.path.join(REPO, 'engine/rl_after/_merged_recover.py')
L = []


def P(s=''):
    print(s); L.append(str(s))


# ---- the literal, read straight out of the engine ---------------------------------------------------
src = open(ENGINE, encoding='utf-8').read()
m = re.search(r'^\s*O37_PG_GRID=\{.*?^\s*\}\s*$', src, re.S | re.M)
assert m, 'B11 FIRED: O37_PG_GRID is not in the engine source'
GRID = eval(m.group(0).split('=', 1)[1], {'__builtins__': {}}, {})
CONST = {}
for nm in ('O37_G0', 'O37_BETA_SAT', 'O37_LAMBDA', 'O37_S0', 'O37_S_P5', 'O37_AGE_GATE'):
    mm = re.search(r'^\s*%s=(-?[0-9.eE+-]+)\s' % nm, src, re.M)
    assert mm, 'B11 FIRED: %s is not in the engine source' % nm
    CONST[nm] = float(mm.group(1))
CONST['O37_THETA_R'] = CONST['O37_BETA_SAT'] / CONST['O37_LAMBDA']
CONST['O37_TMAX'] = 1.0 - CONST['O37_THETA_R'] * (CONST['O37_S_P5'] - CONST['O37_S0'])


def o37_pg(v0, cls):
    """The engine's own reader, transcribed here character for character."""
    _lo, _hi, _y = GRID[cls]
    _x = math.log(max(1e-9, float(v0)))
    if _x <= _lo:
        return _y[0]
    if _x >= _hi:
        return _y[-1]
    _t = (_x - _lo) / (_hi - _lo) * (len(_y) - 1)
    _i = int(_t)
    if _i >= len(_y) - 1:
        return _y[-1]
    return _y[_i] + (_t - _i) * (_y[_i + 1] - _y[_i])


P('=' * 110)
P('ORDER P BUILD — B11: THE WIRED PREMIUM SURFACE AGAINST ORDER P\'S OWN')
P('=' * 110)
P('the engine literal is read out of %s' % os.path.relpath(ENGINE, REPO))
P()

# ---- 1 · the constants -------------------------------------------------------------------------------
MECH = json.load(open(os.path.join(REPO, 'docs/evidence/order_p_2026-08-18/MECH_P.json')))
S4 = json.load(open(os.path.join(REPO, 'docs/evidence/order_p_2026-08-18/STEP4_P.json')))['mechanism']
P('-' * 110)
P('1 · THE CONSTANTS, AGAINST ORDER P\'S OWN FILES')
P('-' * 110)
P('   %-12s %24s %24s %10s' % ('constant', 'wired in the engine', 'ORDER P published', 'match'))
bad = 0
for nm, want, where in (('O37_G0', MECH['G0'], 'MECH_P.json::G0'),
                        ('O37_BETA_SAT', MECH['BETA_sat'], 'MECH_P.json::BETA_sat'),
                        ('O37_LAMBDA', S4['LAMBDA'], 'STEP4_P.json::LAMBDA'),
                        ('O37_S0', MECH['s0'], 'MECH_P.json::s0'),
                        ('O37_S_P5', MECH['s_p5'], 'MECH_P.json::s_p5'),
                        ('O37_THETA_R', S4['THETA_R'], 'BETA_sat / LAMBDA'),
                        ('O37_TMAX', S4['TMAX'], '1 - THETA_R*(s_p5 - s0)')):
    ok = abs(CONST[nm] - want) <= 1e-15 * max(1.0, abs(want))
    bad += (not ok)
    P('   %-12s %24.17g %24.17g %10s   %s' % (nm, CONST[nm], want, 'yes' if ok else 'NO', where))
P()
ident = CONST['O37_LAMBDA'] * CONST['O37_THETA_R'] - CONST['O37_BETA_SAT']
P('   THE IDENTITY THE TILT RESTS ON: LAMBDA * THETA_R - BETA_sat = %.3e   -> %s'
  % (ident, 'HOLDS' if abs(ident) < 1e-15 else 'BROKEN — B9 FIRES'))
assert abs(ident) < 1e-15, 'B9 FIRED'
P('   A(0) = 1 - exp(-0/G0) = %.17g   -> %s' % (1.0 - math.exp(-0.0 / CONST['O37_G0']),
                                                'EXACTLY ZERO' if (1.0 - math.exp(0.0)) == 0.0 else 'NOT ZERO'))
P()

# ---- 2 · the surface ----------------------------------------------------------------------------------
MK = LB.load_matrix('OKRULED')
ROWS = PB.season_rows(MK)
PG = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=True)
P('-' * 110)
P('2 · THE SURFACE, NODE BY NODE AND THEN DENSELY')
P('-' * 110)
P('   ORDER P\'s surface is re-fitted here from scratch: %d season rows, %d players, %.0f games.'
  % (len(ROWS), len(set(r['key'] for r in ROWS)), sum(r['games'] for r in ROWS)))
worst_node = worst_dense = 0.0
for cls in ('TALL', 'SMALL'):
    gx, gy = PG.grid[cls]
    lo, hi, y = GRID[cls]
    assert len(y) == len(gy), 'B11 FIRED: %s node count' % cls
    assert abs(lo - float(gx[0])) < 1e-15 and abs(hi - float(gx[-1])) < 1e-15, 'B11 FIRED: %s support' % cls
    for i in range(len(y)):
        worst_node = max(worst_node, abs(y[i] - float(gy[i])))
    n = 4000
    for k in range(n + 1):
        x = float(gx[0]) - 1.0 + (float(gx[-1]) - float(gx[0]) + 2.0) * k / n
        worst_dense = max(worst_dense, abs(o37_pg(math.exp(x), cls) - PG.at(x, cls)))
P('   worst node-for-node difference over 242 nodes            : %.3e' % worst_node)
P('   worst difference over 8,002 dense points, support +/- 1 log unit: %.3e' % worst_dense)
P('   -> B11 %s' % ('DID NOT FIRE' if max(worst_node, worst_dense) < 1e-9 else 'FIRED'))
assert max(worst_node, worst_dense) < 1e-9, 'B11 FIRED'
P()
P('   THE PREMIUM, IN POINTS A GAME, READ OFF THE WIRED GRID (PACKET_P section 3 reproduced):')
P('   %10s %12s %12s' % ('entry v0', 'SMALL', 'TALL'))
for v0 in (100, 200, 300, 450, 600, 900, 1200, 1700, 2400, 3200):
    P('   %10d %+12.2f %+12.2f' % (v0, o37_pg(v0, 'SMALL'), o37_pg(v0, 'TALL')))
P()
P('   MONOTONE IN PRICE (a dearer player is never expected to produce less), and the biggest step')
P('   between neighbouring nodes — the largest jump the surface can make anywhere:')
for cls in ('TALL', 'SMALL'):
    lo, hi, y = GRID[cls]
    steps = [y[i] - y[i - 1] for i in range(1, len(y))]
    P('     %-6s min step %+.6f (must be >= 0)   max step %+.6f   support v0 [%.1f, %.1f]'
      % (cls, min(steps), max(steps), math.exp(lo), math.exp(hi)))
P()

# ---- 3 · the surplus ------------------------------------------------------------------------------------
P('-' * 110)
P('3 · THE SURPLUS s_P — THE WIRED ARITHMETIC AGAINST op_lib.perf_surplus_P')
P('-' * 110)
P('   The engine walks p[\'scoring\'] and takes each season\'s own bar from MA._fit_bar, its age from')
P('   the season year minus the birth year, and its premium from the grid above. The matrix carries')
P('   exactly those objects (`bar` per season, `age_draft`), so the same walk is reproduced here.')


def wired_surplus(rec, Y):
    v0 = float(rec.get('v0') or 0.0)
    if not (v0 > 0) or rec.get('age_draft') is None:
        return None
    num = den = 0.0
    for s in rec['seasons']:
        if s['year'] > Y:
            continue
        g = float(s.get('games') or 0.0)
        if g <= 0:
            continue
        pos = s.get('bar')
        b = LB.bar(pos, LB.age_at(rec, s['year']))
        if b is None or s.get('avg') is None:
            return None
        num += g * (float(s['avg']) - (b + o37_pg(v0, 'TALL' if pos in LB.TALLPOS else 'SMALL')))
        den += g
    return (num / den) if den > 0 else None


nchk = 0; nmis = 0; worst = 0.0
for k, r in MK.items():
    for Y in (r.get('yrs') or []) + [2026]:
        a = wired_surplus(r, Y); b = PB.perf_surplus_P(r, Y, PG)
        if (a is None) != (b is None):
            nmis += 1; continue
        if a is None:
            continue
        worst = max(worst, abs(a - b)); nchk += 1
P('   vantages compared %d   worst difference %.3e points a game   None/not-None disagreements %d'
  % (nchk, worst, nmis))
P('   -> %s' % ('the wired surplus IS ORDER P\'s surplus' if (worst < 1e-9 and nmis == 0)
                else 'THE WIRED SURPLUS DIFFERS — B11 FIRES'))
assert worst < 1e-9 and nmis == 0, 'B11 FIRED on the surplus'
P()

json.dump(dict(constants=CONST, worst_node=worst_node, worst_dense=worst_dense,
               surplus_vantages=nchk, surplus_worst=worst, identity_residual=ident),
          open(os.path.join(HERE, 'SURFACE_CHECK_P.json'), 'w'), indent=1)
open(os.path.join(HERE, 'SURFACE_CHECK_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote SURFACE_CHECK_P.json and SURFACE_CHECK_P_out.txt')
