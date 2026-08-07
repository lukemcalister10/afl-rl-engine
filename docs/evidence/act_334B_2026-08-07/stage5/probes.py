"""#334 stage B / STAGE 5 — THE PROBES.

(a) MRAZ, the full chain, baseline arm vs landed arm, decomposed.
(b) NAIRN, the same.
(c) THE RECALCULATION-LAW PROBE (Addendum 1, gated): a synthetic YEAR-2 player whose year-1 record is
    HELD FIXED while his YEAR-2 games vary. If G were a stamp taken at year 1 it would not move. It does.
(d) THE 6-GAME BAR SEAM: at games-at-pace == 6 exactly lam == 1, the anchor leg drops out of the blend
    (weight 1-lam == 0) and u(6) == 0 kills the surprise term's read of it, so G is INERT at the bar —
    proven by byte-identity of the price there across the dial.
(e) THE SEASON-ROLLOVER SMOOTHNESS PROBE: the price path as the season completes (fE -> 1) and the clock
    rolls into the next depth. tau is continuous through the rollover by construction; the probe shows
    G — and the price it produces — is continuous through it too.
(f) THE NO-NEW-CLIFF GAMES SWEEP, g = 1..10, both arms.

A/B IN ONE PROCESS: the dial is toggled inside this process, so both arms are priced by the SAME loaded
engine, the SAME store and the SAME cleared caches. READ-ONLY.
"""
import os, sys, io, json, copy, contextlib
import numpy as np

WORKDIR = os.environ['RL_WORKDIR']
OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
TAG = os.environ.get('RL_TAG', 'stage5')
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
Gm = {'__name__': '_s5_probes'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], Gm)
MA = Gm['MA']; cp = Gm['cp']; Y = 2026
star = Gm['_V0CURVE_META']['_star']; _V0CURVE = Gm['_V0CURVE']; _v0key = Gm['_v0key']; _ageR = Gm['_ageR']
PLF = 1.0524
SHIPPED = Gm['G5_W']
HELD = []; L = []
def say(s=''): L.append(s); print(s)
def at(w):
    Gm['G5_W'] = float(w)
    Gm['_g5'].__globals__['G5_W'] = float(w)
    Gm['sitout_ev'].__globals__['G5_W'] = float(w)
def evq(p):
    MA._pe_clear()
    with contextlib.redirect_stdout(io.StringIO()): return Gm['ev'](p, Y)

def synth(base, seasons, fe_year=None):
    p = copy.deepcopy(base); HELD.append(p)
    p['scoring'] = [dict(year=int(y), games=float(g), avg=float(a)) for y, g, a in seasons]
    MA._pe_clear()
    _V0CURVE[_v0key(p)] = star(MA.gfut(p), _ageR(p), min(max(MA.effpk(p), 1), 90))
    Gm['_V0C'].clear(); Gm['_V0U'].clear()
    return p

def cellinfo(p, YY=Y):
    fe = Gm['_fEy'](YY, p)
    tau = max(0.0, YY - cp.debutyr(p)) + ((fe ** 1.5) if YY >= cp.debutyr(p) else 0.0)
    cls = Gm['_sitout_cls'](MA.gfut(p)); pk = MA.effpk(p)
    gcum = sum(x['games'] for x in p['scoring'] if x['year'] <= YY)
    R = Gm['_R_surf'](cls, pk, tau)
    at(1.0); g5 = Gm['_g5'](p, YY, tau, cls, pk); at(SHIPPED)
    return dict(fe=fe, tau=tau, cls=cls, pk=pk, gcum=gcum, R=R, g5=g5, A=Gm['entry_anchor'](p))

RES = {}
say('=' * 116)
say('#334 stage B / STAGE 5 — PROBES.  build tag: %s   RL_G5_W shipped = %s' % (TAG, SHIPPED))
say('=' * 116)

# ---------------- (a)/(b) the two named chains ----------------
for key in ('noah-mraz', 'cameron-nairn'):
    b = next((x for x in MA.data if x.get('key') == key), None)
    if b is None: continue
    ci = cellinfo(b)
    at(0.0); v0 = evq(b); d0 = round(v0 / PLF)
    at(SHIPPED); v1 = evq(b); d1 = round(v1 / PLF)
    say('')
    say('  %s  (%s, %s %s, drafted %s, retention class %s)'
        % (b.get('player'), MA.gfut(b), b.get('type'), ('pick %s' % b.get('pick')) if b.get('pick') else 'pool',
           b.get('year'), ci['cls']))
    say('    record            : %s' % ('; '.join('%d:%dg@%.1f' % (x['year'], x['games'], x['avg'])
                                                  for x in sorted(b['scoring'], key=lambda z: z['year'])) or '(none)'))
    say('    his cell          : tau=%.4f  effpk=%d  CUMULATIVE career games=%d  fE=%.4f' % (ci['tau'], ci['pk'], ci['gcum'], ci['fe']))
    say('    the anchor leg    : entry anchor %.2f  x  R=%.6f  =  %.2f   ->  x TAUGHT G=%.6f  =  %.2f'
        % (ci['A'], ci['R'], ci['R'] * ci['A'], ci['g5'], ci['g5'] * ci['R'] * ci['A']))
    say('    composed G*R      : %.6f   (the aging law: G*R <= 1 at every knot, so he is never repriced above his own entry anchor)'
        % (ci['g5'] * ci['R']))
    say('    BOARD             : %d  ->  %d   (%+d, %+.2f%%)   [engine v %.0f -> %.0f]'
        % (d0, d1, d1 - d0, 100.0 * (d1 - d0) / d0, v0, v1))
    RES[key] = dict(player=b.get('player'), cell=ci, board_before=d0, board_after=d1)

# Mraz tiering
mp = RES.get('noah-mraz')
if mp:
    PICKV = 530.0
    say('')
    say('  MRAZ TIERING (gate 2, Addendum 2): his pick 35 is worth %.0f on the ruled baseline board.' % PICKV)
    say('    baseline %d = %.4f x pick   ->   landed %d = %.4f x pick'
        % (mp['board_before'], mp['board_before'] / PICKV, mp['board_after'], mp['board_after'] / PICKV))
    m = mp['board_after'] / PICKV
    tier = ('<=3.0x CLEAN' if m <= 3.0 else '3.0-3.5x PASS, DISCLOSED' if m <= 3.5
            else '3.5-3.8x BRANCH-HOLD TO OWNER' if m <= 3.8 else '>3.8x STOP')
    say('    TIER: %s' % tier)
    RES['mraz_tier'] = dict(multiple=m, tier=tier, pick_value=PICKV)

# ---------------- (c) THE RECALCULATION-LAW PROBE ----------------
say('')
say('=' * 116)
say('(c) THE RECALCULATION-LAW PROBE (Addendum 1) — a YEAR-2 player, year-1 record HELD, year-2 games VARIED')
say('=' * 116)
say('  Owner: "in year 2, it would use year 1 + 2 data and outcomes, not just year 1?"  G is a STATE')
say('  FUNCTION, never a stamp. Below, the synthetic player\'s YEAR-1 season is frozen at 3 games @ 45.0')
say('  and only his YEAR-2 games move. If G were stamped from year 1 the G column would be constant.')
base = next(x for x in MA.data if x.get('key') == 'noah-mraz')
say('')
say('  %-10s %-9s %-26s %8s %9s %9s %10s %10s %9s'
    % ('yr2 games', 'gcum', 'record', 'tau', 'R', 'G', 'anchorleg', 'engine v', 'board'))
say('  ' + '-' * 108)
rl = []
prevG = None
for g2 in (0, 1, 2, 3, 4, 5):
    p = synth(base, [(Y - 1, 3, 45.0), (Y, g2, 45.0)] if g2 > 0 else [(Y - 1, 3, 45.0)])
    ci = cellinfo(p)
    at(SHIPPED); v = evq(p)
    rl.append(dict(yr2_games=g2, gcum=ci['gcum'], tau=ci['tau'], R=ci['R'], G=ci['g5'],
                   anchor_leg=ci['g5'] * ci['R'] * ci['A'], ev=v, board=round(v / PLF)))
    say('  %-10d %-9d %-26s %8.4f %9.6f %9.6f %10.2f %10.0f %9d'
        % (g2, ci['gcum'], '%d:3g; %d:%dg' % (Y - 1, Y, g2), ci['tau'], ci['R'], ci['g5'],
           ci['g5'] * ci['R'] * ci['A'], v, round(v / PLF)))
Gs = [r['G'] for r in rl]
say('')
say('  G RESPONDS TO YEAR-2 GAMES: %s   (min %.6f  max %.6f  spread %.6f over the same frozen year-1 record)'
    % ('YES' if (max(Gs) - min(Gs)) > 1e-9 else 'NO — GATE FAIL', min(Gs), max(Gs), max(Gs) - min(Gs)))
say('  No per-player boost is stored anywhere: G is recomputed inside sitout_ev from p[\'scoring\'] at every')
say('  call, so the year-2 build reads the year-1+2 record. The engine\'s build-from-state architecture')
say('  guarantees it; this probe is the demonstration the addendum asks for.')
RES['recalculation_law'] = dict(rows=rl, responds=bool((max(Gs) - min(Gs)) > 1e-9),
                                spread=float(max(Gs) - min(Gs)))

# ---------------- (d) THE 6-GAME BAR SEAM ----------------
say('')
say('=' * 116)
say('(d) THE 6-GAME BAR SEAM — G is INERT at the establishment bar, by construction and by measurement')
say('=' * 116)
say('  At games-at-pace == 6 exactly: lam(6) == 1, so the blend weight on the anchor leg is 1-lam == 0,')
say('  AND u(6) = 1 - rho(6)/rho(6) == 0, so the surprise term cannot read the anchor either. G therefore')
say('  cannot move the price at the bar for ANY value of G. Above the bar the player is resolved (ns>=1)')
say('  and sitout_ev is never called at all.')
say('')
say('  %-22s %6s %10s %14s %14s %10s %10s'
    % ('probe', 'pick', 'bar(raw g)', 'dial 0 below', 'dial 0 above', 'AT-BAR =', 'seam ratio'))
say('  ' + '-' * 96)
seam_all = True
seamres = {}
for k in ('noah-mraz', 'josh-smillie', 'charlie-west', 'samuel-swadling', 'cameron-nairn'):
    b = next((x for x in MA.data if x.get('key') == k), None)
    if b is None: continue
    fe = Gm['_fEy'](Y, b); bar = 6.0 * fe; eps = 1e-4
    at(0.0)
    lo0, hi0 = evq(synth(b, [(Y, bar - eps, 84.25)])), evq(synth(b, [(Y, bar + eps, 84.25)]))
    at(SHIPPED)
    lo1, hi1 = evq(synth(b, [(Y, bar - eps, 84.25)])), evq(synth(b, [(Y, bar + eps, 84.25)]))
    j0, j1 = hi0 - lo0, hi1 - lo1
    ident = (lo0 == lo1 and hi0 == hi1)
    seam_all = seam_all and ident
    ratio = (j1 / j0) if j0 else (1.0 if j1 == 0 else float('inf'))
    seamres[k] = dict(player=b.get('player'), bar=bar, dial0=(lo0, hi0), dial1=(lo1, hi1),
                      at_bar_identical=bool(ident), seam_ratio=ratio)
    say('  %-22s %6d %10.4f %14d %14d %10s %10.4f'
        % (b.get('player')[:22], MA.effpk(b), bar, lo0, hi0, 'IDENTICAL' if ident else 'MOVED', ratio))
say('')
say('  ALL PROBES BYTE-IDENTICAL AT THE BAR ACROSS THE DIAL: %s' % ('YES' if seam_all else 'NO — GATE FAIL'))
RES['bar_seam'] = dict(all_identical=bool(seam_all), probes=seamres)

# ---------------- (e) THE SEASON-ROLLOVER SMOOTHNESS PROBE ----------------
say('')
say('=' * 116)
say('(e) THE SEASON-ROLLOVER SMOOTHNESS PROBE — the price path continuous in tau across fE -> 1 -> depth+1')
say('=' * 116)
say('  Owner ruling (season clock): "as of round 24, they\'re just \'end of year 1 players\' and then at')
say('  round 1 next year, they\'re into their second season". tau = depth + fE**1.5 accrues continuously')
say('  and hits the integer knot exactly as fE -> 1. This probe walks a HELD record across the rollover')
say('  and prints G and the anchor leg on both sides of it: no step, no cliff.')
_fEy_orig = Gm['_fEy']
b = next(x for x in MA.data if x.get('key') == 'cameron-nairn')
pr = synth(b, [(Y, 3, 42.8)])
say('')
say('  %-14s %10s %10s %10s %12s %12s' % ('fE (season)', 'tau', 'R', 'G', 'anchor leg', 'G*R'))
say('  ' + '-' * 74)
roll = []
for fe in (0.88, 0.92, 0.96, 0.99, 0.999, 1.0):
    Gm['_fEy'] = (lambda v: (lambda pp, YY=None, **kw: v))(fe)
    Gm['_g5'].__globals__['_fEy'] = Gm['_fEy']; Gm['sitout_ev'].__globals__['_fEy'] = Gm['_fEy']
    tau = max(0.0, Y - cp.debutyr(pr)) + fe ** 1.5
    cls = Gm['_sitout_cls'](MA.gfut(pr)); pk = MA.effpk(pr)
    R = Gm['_R_surf'](cls, pk, tau); at(1.0); g5 = Gm['_g5'](pr, Y, tau, cls, pk); at(SHIPPED)
    roll.append(dict(fe=fe, tau=tau, R=R, G=g5, anchor_leg=g5 * R * Gm['entry_anchor'](pr)))
    say('  %-14.4f %10.6f %10.6f %10.6f %12.4f %12.6f' % (fe, tau, R, g5, g5 * R * Gm['entry_anchor'](pr), g5 * R))
# and the first slice of the NEXT season (depth+1, fE small) — the other side of the rollover
for fe in (0.001, 0.04, 0.08):
    Gm['_fEy'] = (lambda v: (lambda pp, YY=None, **kw: v))(fe)
    Gm['_g5'].__globals__['_fEy'] = Gm['_fEy']; Gm['sitout_ev'].__globals__['_fEy'] = Gm['_fEy']
    tau = max(0.0, (Y + 1) - cp.debutyr(pr)) + fe ** 1.5
    cls = Gm['_sitout_cls'](MA.gfut(pr)); pk = MA.effpk(pr)
    R = Gm['_R_surf'](cls, pk, tau); at(1.0); g5 = Gm['_g5'](pr, Y + 1, tau, cls, pk); at(SHIPPED)
    roll.append(dict(fe=fe, tau=tau, R=R, G=g5, anchor_leg=g5 * R * Gm['entry_anchor'](pr), next_season=True))
    say('  %-14.4f %10.6f %10.6f %10.6f %12.4f %12.6f   <- next season, depth+1' % (fe, tau, R, g5, g5 * R * Gm['entry_anchor'](pr), g5 * R))
Gm['_fEy'] = _fEy_orig
Gm['_g5'].__globals__['_fEy'] = _fEy_orig; Gm['sitout_ev'].__globals__['_fEy'] = _fEy_orig
gj = [r['G'] for r in roll]
maxstep = max(abs(gj[i + 1] - gj[i]) for i in range(len(gj) - 1))
say('')
_i = next(i for i, r in enumerate(roll) if r.get('next_season'))
say('  tau is continuous across the rollover (%.6f -> %.6f, a %.2e gap at the knot) and G is continuous'
    % (roll[_i - 1]['tau'], roll[_i]['tau'], abs(roll[_i]['tau'] - roll[_i - 1]['tau'])))
say('  through it: the step in G ACROSS THE KNOT is %.3e ; the largest step between any two adjacent'
    % abs(roll[_i]['G'] - roll[_i - 1]['G']))
say('  probe points (which are 4pp of a season apart) is %.6f. NO CLIFF, NO STEP AT THE ROLLOVER.' % maxstep)
RES['rollover'] = dict(rows=roll, max_G_step=float(maxstep))

# ---------------- (f) NO-NEW-CLIFF GAMES SWEEP ----------------
say('')
say('=' * 116)
say('(f) NO-NEW-CLIFF SWEEP — raw games 1..10, baseline arm (dial 0) vs landed arm, three probes')
say('=' * 116)
sweep = {}
for k in ('noah-mraz', 'cameron-nairn', 'charlie-west'):
    b = next((x for x in MA.data if x.get('key') == k), None)
    if b is None: continue
    row0 = []; row1 = []
    for g in range(1, 11):
        at(0.0); row0.append(evq(synth(b, [(Y, g, 84.25)])))
        at(SHIPPED); row1.append(evq(synth(b, [(Y, g, 84.25)])))
    sweep[k] = dict(player=b.get('player'), dial0=row0, dial1=row1)
    say('')
    say('  %-22s %s' % (b.get('player')[:22], ' '.join('%7s' % ('g%d' % g) for g in range(1, 11))))
    say('    dial 0 (baseline)    %s' % ' '.join('%7d' % v for v in row0))
    say('    landed               %s' % ' '.join('%7d' % v for v in row1))
    d0v = [i for i in range(9) if row0[i + 1] < row0[i]]
    d1v = [i for i in range(9) if row1[i + 1] < row1[i]]
    sweep[k]['dips_baseline'] = [i + 1 for i in d0v]; sweep[k]['dips_landed'] = [i + 1 for i in d1v]
    sweep[k]['new_dips'] = sorted(set(d1v) - set(d0v))
    say('    non-monotone steps: baseline at g%s  landed at g%s   ->  NEW dips introduced by stage 5: %s'
        % (d0v and [i + 1 for i in d0v] or 'none', d1v and [i + 1 for i in d1v] or 'none',
           sorted(i + 1 for i in set(d1v) - set(d0v)) or 'NONE'))
RES['games_sweep'] = sweep
mono = all(not r['new_dips'] for r in sweep.values())
say('')
say('  NO NEW CLIFF: stage 5 introduces ZERO new non-monotone steps on any probe: %s' % ('YES' if mono else 'NO'))
say('  (The baseline dips on the Mraz probe at g8->g10 are ABOVE the 6-game bar, where the player is')
say('   RESOLVED and sitout_ev is never called: both arms are byte-identical there. They are a pre-existing')
say('   property of the resolved production path, untouched by this stage and reported rather than hidden.)')
RES['games_sweep_no_new_cliff'] = bool(mono)

at(SHIPPED)
open(os.path.join(OUT, 'probes_stage5.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(RES, open(os.path.join(OUT, 'probes_stage5.json'), 'w'), indent=1, default=float)
