#!/usr/bin/env python3
"""ORDER 30B-P — THE SCORING CHECKS the movers ledger does not carry.
  (1) the REALISED pedigree share: sigma is the WEIGHT on the pedigree leg by construction; the VALUE
      share sigma*v0/price is a different number, and both are reported rather than conflated.
  (2) P10 — the two rows the decay gate reached under the par denominator, priced both ways.
  (3) P8 second leg and P9 — the mover classes against ablation B (pole+ISO deleted, no blend).
Usage: o30bp_checks.py PREVIEW_MOVERS.json ABL_NOPOLE_NOISO.json STEP2.json PREVIEW.json
"""
import os, sys, io, json, math, contextlib, collections

MV_P, ABL_P, S2_P, PV_P = sys.argv[1:5]
STAGE = os.environ['STAGE']; ROOT = os.environ['RL_REPO']
assert os.environ.get('RL_O30B_PREVIEW') == '1'
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']; PR = G['PR']; cp = G['cp']
BARS = G['_O30BP_BARS']; bestlvl = G['bestlvl']; nseas_pro = G['nseas_pro']; v0_start = G['v0_start']
sigma30bp = G['sigma30bp']; sigma30bp_raw = G['sigma30bp_raw']; pv_games = G['pv_games']
day0_v0 = G['day0_v0']; _PL_F = G['_PL_F']; _fa_year = G['_fa_year']; _form_anchor_clock = G['_form_anchor_clock']
BY = {p['key']: p for p in MA.data if p.get('key')}
MV = json.load(open(MV_P)); R = {r['key']: r for r in MV['rows']}
Y = 2026

# ---- (1) the two readings of "pedigree share" -------------------------------------------------------
print('=== (1) THE TWO READINGS OF "THE PEDIGREE SHARE", BOTH REPORTED')
print('  WEIGHT share  = sigma(g)                      -- EXACT BY CONSTRUCTION for every blended row.')
print('  VALUE  share  = sigma(g) x v0 / printed price -- what fraction of the PRINTED number the')
print('                  pedigree leg actually is. They coincide only where v0 == the price.')
bl = [r for r in MV['rows'] if r['sigma'] is not None and r['preview']]
for lab, lo, hi in (('cg 1-5', 1, 5), ('cg 6-15', 6, 15), ('cg 16-35', 16, 35), ('cg 36-70', 36, 70), ('cg 71+', 71, 10 ** 6)):
    s = [r for r in bl if lo <= (r['cg'] or 0) <= hi]
    if not s: continue
    w = sorted(r['sigma'] for r in s)
    v = sorted(r['pedigree_pts'] / r['preview'] for r in s if r['preview'] > 0)
    print('  %-9s n %3d   sigma(weight) med %.4f [%.4f..%.4f]   VALUE share med %.4f [%.4f..%.4f]'
          % (lab, len(s), w[len(w) // 2], w[0], w[-1], v[len(v) // 2], v[0], v[-1]))
allv = sorted(r['pedigree_pts'] / r['preview'] for r in bl if r['preview'] > 0)
print('  whole blended book: total pedigree points %.0f of %d printed = %.4f'
      % (sum(r['pedigree_pts'] for r in bl), sum(r['preview'] for r in bl),
         sum(r['pedigree_pts'] for r in bl) / sum(r['preview'] for r in bl)))

# ---- (2) P10: the decay-gate rows ------------------------------------------------------------------
print('\n=== (2) P10 — THE DECAY GATE UNDER THE TWO DENOMINATORS')
print('  the gate: el >= onset+2 AND ns >= 1 AND pr = bestlvl/par < 0.55  ->  e = min(e, v0 x frac)')
print('  %-20s %-5s %8s %8s %8s %8s %9s %9s %10s %10s'
      % ('key', 'pos', 'bestlvl', 'par@pick', 'bar', 'pr(par)', 'pr(bar)', 'v0 x frac', 'prod leg', 'gate cut?'))
for k in ('campbell-chesser', 'finlay-macrae'):
    p = BY[k]; pos = MA.gfut(p)
    with _form_anchor_clock(): el = PR.tenure(p, _fa_year(Y))
    keyruc = pos in ('KPF', 'KPD', 'RUCK'); onset = 4 if keyruc else 3
    par = float(PR.par_at(pos, min(MA.effpk(p), cp.KMAX), min(max(el, 1), 6))); bar = BARS[pos]
    b = bestlvl(p, Y); v0 = v0_start(p)
    frac = 0.45 * max(0.3, 1 - 0.08 * (el - onset)) * (1.5 if keyruc else 1.0)
    prod = R[k]['production_pts'] * _PL_F if R[k]['production_pts'] is not None else None
    cut = (v0 * frac) < prod if prod else None
    print('  %-20s %-5s %8.2f %8.2f %8.2f %8.4f %9.4f %9.1f %10.1f %10s'
          % (k, pos, b, par, bar, b / max(1, par), b / max(1, bar), v0 * frac, prod,
             ('YES by %.0f engine pts' % (prod - v0 * frac)) if cut else 'no'))
    print('  %-20s   under the PAR denominator the gate FIRES (pr %.4f < 0.55); under the BAR denominator '
          'it does NOT (pr %.4f). Step-2 %d -> PREVIEW %d.'
          % ('', b / max(1, par), b / max(1, bar), R[k]['step2'], R[k]['preview']))
    # what the same preview configuration would print WITH the gate applied
    if prod:
        pg = min(prod, v0 * frac); s = R[k]['sigma']
        alt = int(round(((1 - s) * pg + s * day0_v0(p) * _PL_F) / _PL_F))
        print('  %-20s   the SAME preview configuration with the par denominator retained would print %d '
              '(%+d vs the preview\'s %d).' % ('', alt, R[k]['preview'] - alt, R[k]['preview']))

# ---- (3) mover classes vs ablation B ---------------------------------------------------------------
print('\n=== (3) P8 SECOND LEG — THE PREVIEW AGAINST ABLATION B (pole+ISO deleted, NO blend)')
A = json.load(open(ABL_P)); AB = {r['key']: r['new'] for r in A['rows']}
S2 = {r['key']: r['v'] for r in json.load(open(S2_P))['active']}
PVv = {r['key']: r['v'] for r in json.load(open(PV_P))['active']}
def ablv(k): return AB.get(k, S2.get(k))          # ablation rows list only movers; non-movers are Step-2
cls = collections.defaultdict(lambda: [0, 0, 0])
for k, r in R.items():
    if r['sigma'] is None: continue
    a = ablv(k); pv = PVv[k]
    c = ('1-5' if (r['cg'] or 0) <= 5 else '6-15' if r['cg'] <= 15 else '16-35' if r['cg'] <= 35
         else '36-70' if r['cg'] <= 70 else '71+')
    cls[c][0] += 1; cls[c][1] += pv - a; cls[c][2] += a
print('  %-8s %5s %14s %14s %10s' % ('cg', 'n', 'sum ablB', 'sum PREVIEW-ablB', 'mean/row'))
for c in ('1-5', '6-15', '16-35', '36-70', '71+'):
    if not cls[c][0]: continue
    print('  %-8s %5d %14d %+14d %+10.1f' % (c, cls[c][0], cls[c][2], cls[c][1], cls[c][1] / cls[c][0]))

# ---- P9: the at-bar class -----------------------------------------------------------------------
print('\n=== (4) P9 — THE AT-BAR / TREMBATH CLASS vs THE STAR CLASS (|delta %| vs Step-2)')
def sa(p):
    gt = num = 0.0
    for s in p['scoring']:
        if s['games'] <= 0: continue
        gt += s['games']; num += s['games'] * s['avg']
    return (num / gt) if gt > 0 else 0.0
atbar, star = [], []
prices = sorted((r['step2'] for r in MV['rows'] if r['sigma'] is not None), reverse=True)
top10 = prices[max(0, len(prices) // 10 - 1)]
for k, r in R.items():
    if r['sigma'] is None or not r['step2']: continue
    p = BY[k]; q = sa(p) / BARS[MA.gfut(p)]
    if 16 <= (r['cg'] or 0) <= 70 and 0.9 <= q <= 1.1: atbar.append(abs(r['pct_vs_step2']))
    if (r['cg'] or 0) >= 100 and r['step2'] >= top10: star.append(abs(r['pct_vs_step2']))
for lab, v in (('AT-BAR (cg 16-70, career avg within 10%% of its positional bar)', atbar),
               ('STAR   (cg 100+, top-decile Step-2 price)', star)):
    v = sorted(v)
    print('  %-62s n %3d  median |delta%%| %6.2f  mean %6.2f' % (lab, len(v), v[len(v) // 2], sum(v) / len(v)))

# ---- the sigma alternative: the raw log-linear midpoint interpolation ---------------------------
print('\n=== (5) THE DECLARED ALTERNATIVE sigma (raw log-linear between band midpoints), NOT WIRED')
print('  %-20s %6s %9s %9s %10s %10s %9s' % ('key', 'games', 'sigma fit', 'sigma raw', 'PREVIEW', 'raw-sigma', 'delta'))
for k in ('isaac-kako', 'willem-duursma', 'dyson-sharp', 'jacob-farrow', 'cooper-trembath', 'chris-scerri'):
    r = R[k]; g = r['games_sigma_axis']; s1 = sigma30bp(g); s2 = sigma30bp_raw(g)
    prod = r['production_pts']
    alt = int(round((1 - s2) * prod + s2 * r['v0_step1_board']))
    print('  %-20s %6.1f %9.4f %9.4f %10d %10d %+9d' % (k, g, s1, s2, r['preview'], alt, alt - r['preview']))
