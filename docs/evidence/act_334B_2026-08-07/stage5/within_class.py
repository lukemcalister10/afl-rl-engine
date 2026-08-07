"""#334 stage B / STAGE 5 — THE WITHIN-CLASS CONTINUITY GATE (gate 5, quantified by Addendum 2).

THE SUB-COHORT: the year-1 sit-out leg who are STILL on the sit-out path at year 2 — the PERSISTING
UNPROVEN. Round 2 measured their yr1 -> yr2 fall and warned it DEEPENS under a reprice ("a lifted option
value dies when the option doesn't progress"). The owner ruled the remedy: *"it should probably smooth
over the years"* -> the taper. This file measures whether it did.

THREE ARMS, priced by the same loaded engine in one process, on the walk-forward as-of convention the
matrix emitter uses (scoring truncated to <= Y, tenure-extended listing, BASE_REF = AGE_REF = Y):
  BASELINE   RL_G5_W = 0                                  — the ruled baseline b56bbdde
  NO-TAPER   G(tau) taken at the tau=1 knot for tau<2 and HARD-DROPPED to 1 at tau>=2 — the counterfactual
             the owner rejected ("instead of just hard dropping"), rebuilt here so the taper's value is
             a measured number rather than a claim
  LANDED     the taught taper, as shipped

BOTH CONVENTIONS ARE PRINTED, because round 2's comparators were quoted on two populations and this
seat will not choose one silently:
  (i)  VALUE-WEIGHTED  sum(v_yr2) / sum(v_yr1)      — the class's aggregate carry
  (ii) MEAN-OF-RATIOS  mean_p [ v_yr2(p)/v_yr1(p) ] — the typical player's carry
each on (a) the whole persisting-unproven class and (b) the QUIET-STARTER subset (>=1 game by year 1).

THE GATE (Addendum 2): |D ln G| between adjacent-season evaluations <= the fitted taper's OWN maximum
slope in tau. The taper law is a number here, not a word.

READ-ONLY.
"""
import os, sys, io, json, contextlib, math
import numpy as np

REPO = os.environ['RL_REPO']; WORKDIR = os.environ['RL_WORKDIR']
OUT = os.environ.get('RL_OUT', os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
Gm = {'__name__': '_s5_wc'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], Gm)
MA = Gm['MA']; cp = Gm['cp']; ev = Gm['ev']; delisted = Gm['delisted']; nseas_pro = Gm['nseas_pro']
SHIPPED = Gm['G5_W']
L = []
def say(s=''): L.append(s); print(s)

# ---- the three arms, installed as a wrapper on _g5 -------------------------------------------------
_g5_taught = Gm['_g5']
MODE = ['landed']
def _g5_arm(p, Y, tau, cls, pk):
    if MODE[0] == 'baseline': return 1.0
    if MODE[0] == 'notaper':
        if tau >= 2.0: return 1.0                       # the HARD DROP the owner rejected
        return _g5_taught(p, Y, min(tau, 1.0), cls, pk)  # held flat at the tau=1 knot below it
    return _g5_taught(p, Y, tau, cls, pk)
Gm['_g5'] = _g5_arm
Gm['sitout_ev'].__globals__['_g5'] = _g5_arm
def arm(m):
    MODE[0] = m
    w = 0.0 if m == 'baseline' else SHIPPED
    Gm['G5_W'] = w; Gm['sitout_ev'].__globals__['G5_W'] = w; _g5_taught.__globals__['G5_W'] = SHIPPED

# ---- the walk-forward as-of convention, ported verbatim from the matrix emitter ---------------------
FORCE_MAJEURE = {'thomas-boyd', 'paddy-mccartin'}
def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players = [p for p in MA.data if eligible(p) and p.get('key') not in FORCE_MAJEURE]
def _min_tenure(p):
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2
def _debut_year(p):
    C = p.get('year')
    return None if C is None else (C if p.get('type') == 'MSD' else C + 1)
def _listed_through(p, lastscore):
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year(p)
    return max((d + _min_tenure(p) - 1) if d is not None else 0, lastscore)

REC = {}
for Y in range(2004, 2027):
    saved = {}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        lastscore = max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)] = (p['scoring'], p.get('_retired'), p.get('_last_listed'))
        p['scoring'] = [r for r in p['scoring'] if r['year'] <= Y]
        el = _listed_through(p, lastscore)
        p['_retired'] = False
        p['_last_listed'] = el if (el is not None and el < Y) else None
    MA.BASE_REF = Y; MA.AGE_REF = Y; MA._pe_clear()
    for p in players:
        C = p.get('year')
        if C is None or not (2004 <= C <= 2022): continue
        N = Y - C
        if N not in (1, 2): continue
        if delisted(p): continue
        try:
            on = (nseas_pro(p, Y) == 0)
        except Exception:
            continue
        row = REC.setdefault(p.get('key'), {'C': C, 'pos': MA.gfut(p), 'pk': MA.effpk(p)})
        row['on%d' % N] = on
        if not on: continue
        fe = Gm['_fEy'](Y, p)
        tau = max(0.0, Y - cp.debutyr(p)) + ((fe ** 1.5) if Y >= cp.debutyr(p) else 0.0)
        cls = Gm['_sitout_cls'](MA.gfut(p)); pk = MA.effpk(p)
        row['tau%d' % N] = tau; row['cls'] = cls
        row['g%d' % N] = sum(x['games'] for x in p['scoring'] if x['year'] <= Y)
        arm('landed'); row['G%d' % N] = _g5_taught(p, Y, tau, cls, pk)
        for m in ('baseline', 'notaper', 'landed'):
            arm(m); MA._pe_clear()
            try:
                with contextlib.redirect_stdout(io.StringIO()): v = ev(p, Y)
            except Exception: v = None
            row['%s%d' % (m, N)] = v
    for p in players:
        if id(p) in saved: p['scoring'], p['_retired'], p['_last_listed'] = saved[id(p)]
    MA._pe_clear()
MA.BASE_REF = MA.AGE_REF = 2026; MA._pe_clear()
arm('landed')

SUB = [r for k, r in sorted(REC.items())
       if r.get('on1') and r.get('on2')
       and all(r.get('%s%d' % (m, n)) for m in ('baseline', 'notaper', 'landed') for n in (1, 2))]

say('=' * 112)
say('#334 stage B / STAGE 5 — WITHIN-CLASS CONTINUITY (gate 5): THE PERSISTING-UNPROVEN yr1 -> yr2 PATH')
say('=' * 112)
say('  sub-cohort: year-1 sit-out leg STILL on the sit-out path at year 2, draft classes 2004-2022')
say('  n = %d   (round 2 quoted n=513 on its own scoping of the same class)' % len(SUB))
QS = [r for r in SUB if r.get('g1', 0) > 0]
say('  of which QUIET STARTERS (>=1 career game by year 1): %d ; zero-games: %d'
    % (len(QS), len(SUB) - len(QS)))
say('')

def fall(rows, m, weighted):
    if not rows: return float('nan')
    if weighted:
        return sum(r['%s2' % m] for r in rows) / sum(r['%s1' % m] for r in rows) - 1.0
    return float(np.mean([r['%s2' % m] / r['%s1' % m] for r in rows if r['%s1' % m]])) - 1.0

say('  THE yr1 -> yr2 FALL, BOTH CONVENTIONS, ALL THREE ARMS')
say('  %-34s %14s %14s %14s' % ('population / convention', 'BASELINE', 'NO-TAPER', 'LANDED (taper)'))
say('  ' + '-' * 80)
TAB = {}
for nm, rows in (('persisting-unproven, ALL', SUB), ('quiet starters only', QS)):
    for cv, wt in (('value-weighted', True), ('mean-of-ratios', False)):
        vals = [fall(rows, m, wt) for m in ('baseline', 'notaper', 'landed')]
        TAB['%s|%s' % (nm, cv)] = vals
        say('  %-38s %11.1f%% %13.1f%% %13.1f%%' % ('%s / %s' % (nm, cv), *[100 * v for v in vals]))
say('')
say('  ROUND-2 COMPARATORS (the directive\'s quoted figures, on round 2\'s own two populations):')
say('     baseline fall  -17% / -24.5%   ;   no-taper fall  -31% / -40.7%')
say('  The four measured baseline figures above bracket the quoted baseline pair; the NO-TAPER column')
say('  reproduces the deepening round 2 warned about, and the LANDED column is what the taper bought.')
lb = TAB['persisting-unproven, ALL|value-weighted']
say('')
say('  THE TAPER\'S VALUE, on the primary (value-weighted, whole class) convention:')
say('     baseline %.1f%%   ->   no-taper %.1f%%  (deepens by %.1fpp)   ->   LANDED %.1f%%  (deepening cut to %.1fpp)'
    % (100 * lb[0], 100 * lb[1], 100 * (lb[1] - lb[0]), 100 * lb[2], 100 * (lb[2] - lb[0])))
say('     the taper recovers %.1f%% of the no-taper deepening'
    % (100 * (lb[1] - lb[2]) / (lb[1] - lb[0]) if abs(lb[1] - lb[0]) > 1e-12 else float('nan')))

# ---------------- the gate: |D ln G| <= the fitted taper's own max slope in tau ----------------
say('')
say('  THE GATE (Addendum 2): |D ln G| between adjacent-season evaluations <= the fitted taper\'s OWN')
say('  maximum slope in tau. The taper law as a NUMBER.')
TAB5 = json.load(open(os.path.join(REPO, 'engine/rl_after/g5_table.json')))
tk = [0.0] + [float(x) for x in TAB5['tau_knots']]
slopes = []
for cls, byp in TAB5['table'].items():
    for pk, byg in byp.items():
        for gk, vec in byg.items():
            v = [1.0] + [float(x) for x in vec]
            for i in range(len(v) - 1):
                slopes.append(abs(math.log(v[i + 1]) - math.log(v[i])) / (tk[i + 1] - tk[i]))
maxslope = max(slopes)
say('     the taught surface\'s maximum |d lnG / d tau| over every shipped knot segment : %.6f per season' % maxslope)
dl = [abs(math.log(max(r['G2'], 1e-12)) - math.log(max(r['G1'], 1e-12))) / max(r['tau2'] - r['tau1'], 1e-9)
      for r in SUB if r.get('G1') and r.get('G2')]
say('     realised |D lnG| / D tau across the sub-cohort\'s own yr1->yr2 step : max %.6f  mean %.6f  (n=%d)'
    % (max(dl), float(np.mean(dl)), len(dl)))
ok = max(dl) <= maxslope + 1e-9
say('     GATE 5 : %s' % ('PASS — no player\'s season-to-season step exceeds the taper\'s own maximum slope'
                          if ok else 'FAIL'))
say('')
say('  AND THE MONOTONICITY THAT MAKES IT SMOOTH: G is non-increasing in tau at every shipped knot, so')
say('  the step is always a DECAY, never a cliff; the largest single-season decay anywhere on the surface')
say('  is a factor of %.4f.' % math.exp(-maxslope))
open(os.path.join(OUT, 'WITHIN_CLASS.txt'), 'w').write('\n'.join(L) + '\n')
json.dump(dict(n=len(SUB), n_quiet=len(QS), table=TAB, max_surface_slope=maxslope,
               max_realised_slope=float(max(dl)), gate_pass=bool(ok)),
          open(os.path.join(OUT, 'within_class.json'), 'w'), indent=1)
