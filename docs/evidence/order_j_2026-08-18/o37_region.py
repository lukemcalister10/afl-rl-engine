#!/usr/bin/env python3
"""ORDER J — READING THE FEASIBLE REGION, AND THE TRADE-OFF CURVE.

Pure analysis of O37_SWEEP.json. No engine, no new maths. It answers, in the owner's own terms:
  * how big is the region the corrected gate opens, and what shape is it;
  * what is the best reachable year-1 class mark, and at what late-band level;
  * what is the best reachable late-band improvement, and at what class level;
  * the TRADE-OFF CURVE the order asks for: what class level is reachable at each late-band level.
"""
import json, os, collections

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
S = json.load(open(SP + '/O37_SWEEP.json'))
BANDS5 = ['1-10', '11-20', '21-30', '31-40', '41-64']
C = S['control_landing']; T = S['control_tall_only']
ALL = S['ruled_feasible']
OK = [M for M in ALL if not M['law_fails']]
print('ruled-feasible %d · owner-law-ok %d (G1 floor+rail, G2 both improve, G3 <=+14%%)' % (len(ALL), len(OK)))

pct = lambda v: 100.0 * (v - 1.0)
print('\nBASELINES on this instrument:')
print('  landing candidate 1f176444 : class %.4f  bands %s'
      % (C['mean_0515'], ' '.join('%+6.2f%%' % pct(C['band_R'][b]) for b in BANDS5)))
print('  ruled tall factor alone    : class %.4f  bands %s'
      % (T['mean_0515'], ' '.join('%+6.2f%%' % pct(T['band_R'][b]) for b in BANDS5)))

print('\n-- WHICH AXES ACTUALLY MOVE THE INSTRUMENT --')
for ax in ('dose', 'kappa', 'gamma_u', 'eta', 'gamma_d', 'lam_rel'):
    vals = sorted(set(M[ax] for M in OK))
    print('  %-9s values present in the law-ok set: %s' % (ax, vals))
g = collections.defaultdict(set)
for M in OK:
    g[(M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'])].add(round(M['mean_0515'], 6))
print('  lam_rel: %d distinct (dose,kappa,gu,eta,gd) cells; class mark distinct values per cell: %s'
      % (len(g), sorted(set(len(v) for v in g.values()))))

print('\n-- THE EXTREMES OF THE REGION --')
def show(nm, M):
    print('  %-34s dose %.2f kappa %.2f gu %.0f eta %.2f gd %.0f rel %.2f | class %.4f maxcls %.4f | %s'
          % (nm, M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['lam_rel'],
             M['mean_0515'], M['max_class'], ' '.join('%+6.2f%%' % pct(M['band_R'][b]) for b in BANDS5)))
show('highest class mark', max(OK, key=lambda m: m['mean_0515']))
show('best picks 31-40', max(OK, key=lambda m: m['band_R']['31-40']))
show('best picks 41-64', max(OK, key=lambda m: m['band_R']['41-64']))
show('best 31-40 + 41-64 together', max(OK, key=lambda m: m['band_R']['31-40'] + m['band_R']['41-64']))
show('lowest SSE (the selection law)', min(OK, key=lambda m: m['obj']))
show('lowest picks 11-20 (G3 headroom)', min(OK, key=lambda m: m['band_R']['11-20']))

print('\n-- THE TRADE-OFF CURVE: the best year-1 class mark reachable at each late-band level --')
print('   (late-band level = the WORSE of picks 31-40 and 41-64, yr0->1, on the calibrator)')
print('   %-14s %8s %8s %8s %8s   %s' % ('late-band >=', 'n pts', 'best cls', '31-40', '41-64', 'the point'))
for thr in [-0.1300, -0.1000, -0.0900, -0.0850, -0.0800, -0.0750, -0.0700, -0.0650, -0.0600, -0.0500, 0.0]:
    sub = [M for M in OK if min(M['band_R']['31-40'], M['band_R']['41-64']) - 1.0 >= thr]
    if not sub:
        print('   %-14s %8d   —' % ('%+.2f%%' % (100 * thr), 0)); continue
    B = max(sub, key=lambda m: m['mean_0515'])
    print('   %-14s %8d %8.4f %+7.2f%% %+7.2f%%   dose %.2f k %.2f gu %.0f eta %.2f gd %.0f'
          % ('%+.2f%%' % (100 * thr), len(sub), B['mean_0515'], pct(B['band_R']['31-40']),
             pct(B['band_R']['41-64']), B['dose'], B['kappa'], B['gamma_u'], B['eta'], B['gamma_d']))

print('\n-- THE MIRROR CURVE: the best late-band level reachable at each class-mark floor --')
print('   %-14s %8s %9s %9s %9s   %s' % ('class >=', 'n pts', 'worst-late', '31-40', '41-64', 'the point'))
for thr in [1.030, 1.040, 1.045, 1.050, 1.055, 1.060, 1.070, 1.080]:
    sub = [M for M in OK if M['mean_0515'] >= thr]
    if not sub:
        print('   %-14s %8d   — unreachable inside the ruled constraints' % ('%.3f' % thr, 0)); continue
    B = max(sub, key=lambda m: min(m['band_R']['31-40'], m['band_R']['41-64']))
    print('   %-14s %8d %+8.2f%% %+8.2f%% %+8.2f%%   dose %.2f k %.2f gu %.0f eta %.2f gd %.0f'
          % ('%.3f' % thr, len(sub), 100 * (min(B['band_R']['31-40'], B['band_R']['41-64']) - 1),
             pct(B['band_R']['31-40']), pct(B['band_R']['41-64']), B['dose'], B['kappa'],
             B['gamma_u'], B['eta'], B['gamma_d']))

print('\n-- WHY THE ASPIRATION (no sell-red) IS OUT OF REACH: what it would take --')
noasp = [M for M in ALL if M['band_R']['31-40'] >= 1.0 or M['band_R']['41-64'] >= 1.0]
print('   ruled-feasible points with 31-40 >= 0%%: %d' % sum(1 for M in ALL if M['band_R']['31-40'] >= 1.0))
print('   ruled-feasible points with 41-64 >= 0%%: %d' % sum(1 for M in ALL if M['band_R']['41-64'] >= 1.0))
B = max(ALL, key=lambda m: m['band_R']['41-64'])
print('   best 41-64 anywhere inside the RULED constraints: %+.2f%% (dose %.2f k %.2f gu %.0f eta %.2f '
      'gd %.0f) — still %.2f points of appreciation short of zero'
      % (pct(B['band_R']['41-64']), B['dose'], B['kappa'], B['gamma_u'], B['eta'], B['gamma_d'],
         -pct(B['band_R']['41-64'])))
B4 = max(ALL, key=lambda m: m['band_R']['31-40'])
print('   best 31-40 anywhere inside the RULED constraints: %+.2f%% — %.2f points short of zero'
      % (pct(B4['band_R']['31-40']), -pct(B4['band_R']['31-40'])))

print('\n-- THE CANDIDATE SHORTLIST FOR THE BOARD GATES (J-TOL, G4, G5) --')
print('   The selection law is min corrected-surface SSE. lam_rel is INERT on this instrument (it')
print('   reaches 5 of 1,986 walk-forward rows), so it is carried at the wired 1.08 here and decided')
print('   on the board. The distinct (dose, kappa, gu, eta, gd) points, in selection order:')
seen = set(); SHORT = []
for M in sorted(OK, key=lambda m: (m['obj'], m['dose'], abs(m['kappa'] - 0.24))):
    k = (M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'])
    if k in seen or M['lam_rel'] != 1.08:
        continue
    seen.add(k); SHORT.append(M)
print('   %3s %5s %6s %5s %5s %5s | %8s %8s %8s | %s'
      % ('#', 'dose', 'kappa', 'gu', 'eta', 'gd', 'class', 'maxcls', 'SSE', 'five bands yr0->1'))
for i, M in enumerate(SHORT, 1):
    print('   %3d %5.2f %6.2f %5.0f %5.2f %5.0f | %8.4f %8.4f %8.2f | %s'
          % (i, M['dose'], M['kappa'], M['gamma_u'], M['eta'], M['gamma_d'], M['mean_0515'],
             M['max_class'], M['obj'], ' '.join('%+6.2f%%' % pct(M['band_R'][b]) for b in BANDS5)))
json.dump(dict(order='ORDER J — the feasible region', n_ruled=len(ALL), n_law_ok=len(OK),
               shortlist=SHORT, control_landing=C, control_tall_only=T),
          open(os.path.join(HERE, 'REGION_J.json'), 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: REGION_J.json  (%d shortlist points)' % len(SHORT))
