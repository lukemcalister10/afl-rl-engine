#!/usr/bin/env python3
"""ORDER S — S2 SCORED ON REAL ROWS. THE GAP PRESERVATION AND THE RELIEF REGRESSIVITY.

Pure JSON reads over censuses already produced. NO ENGINE RUN HERE.

THE OWNER'S FINDING (F1, register v738), restated so the measurement answers it and not something
easier: past TMAX badness is FREE while games NEVER are. Two heavy underperformers whose per-game
records are tens of points apart pay the SAME rate because both are parked at the cap, so GAMES
become the differentiator instead of performance — which inverts the mechanism's founding principle
exactly where the charges are biggest. And cap-lowering relief is REGRESSIVE: the deepest failures,
who carry the most pedigree, are paid first.

MEASURED HERE, on the charged population of each board:
  1 · HOW MANY ROWS ARE PARKED AT THE CAP, and how far apart their records are. Under the hard clip
      these rows are TIED in T. Under the compression none of them is.
  2 · PAIRWISE: among charged rows AT EQUAL GAMES, how often does a WORSE per-game record cost the
      same or less? That is the mechanism question, with A(g) held out of it.
  3 · RELIEF REGRESSIVITY: what share of the total relief against ORDER P lands in the deepest
      surplus decile, under the CAP-LOWERING lever and under the COMPRESSION.

  usage: python3 os_cap.py
"""
import json, math, os, collections
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
L = []


def P(s=''):
    print(s); L.append(str(s))


def load(tag):
    p = os.path.join(HERE, 'CENSUS_%s.json' % tag)
    return json.load(open(p)) if os.path.exists(p) else None


TAGS = ['SB1', 'SAB1', 'SR20A', 'SC15', 'SC20', 'SC20A', 'SW47', 'SW47A', 'SM', 'SMA',
        'SL56', 'SL10', 'SALL']
C = {t: load(t) for t in TAGS}
C = {t: v for t, v in C.items() if v}
NICE = {'SB1': 'FIX B1 — ORDER P\'s p5 HARD CLIP (the control)',
        'SAB1': 'FIX A+B1 — ORDER P\'s p5 HARD CLIP with FIX A',
        'SR20A': 'ORDER R p20 HARD CLIP + FIX A',
        'SC15': 'ORDER S COMPRESSION, p15 anchor',
        'SC20': 'ORDER S COMPRESSION, p20 anchor',
        'SC20A': 'ORDER S COMPRESSION, p20 anchor + FIX A',
        'SW47': 'ORDER S recency w=0.47', 'SW47A': 'ORDER S recency w=0.47 + FIX A',
        'SM': 'ORDER S mature premium', 'SMA': 'ORDER S mature premium + FIX A',
        'SL56': 'ORDER S LAMBDA 0.56', 'SL10': 'ORDER S LAMBDA 0.10',
        'SALL': 'ORDER S all four + FIX A'}

P('=' * 118)
P('ORDER S — S2 SCORED ON REAL ROWS. NOTHING IS ADOPTED. NO ROW IS A TARGET.')
P('=' * 118)
P('  censuses read: %s' % ' '.join(sorted(C)))
if not C:
    P('  NO CENSUS ON DISK — nothing measured. Reported as unmeasured, never as passed.')
    open(os.path.join(HERE, 'CAP_S%s_out.txt' % os.environ.get('OS_CAP_SUF', '')), 'w').write('\n'.join(L) + '\n')
    raise SystemExit(0)

BASE = 'SB1'
K = {r['key']: r for r in C[BASE]['charge']}
CONST = C[BASE].get('constants') or {}
S0 = -2.4527332249999999
LAM = CONST.get('LAMBDA') or 0.1743833036575403
THR = CONST.get('THETA_R') or 0.657439
TMAX_P5 = CONST.get('TMAX') or 21.1233
S_PQ = {5: -33.06133449874688, 15: -22.148794633345666, 20: -19.024574086528315}
P('  ORDER P constants read off the census: LAMBDA %.8f  THETA_R %.6f  TMAX(p5) %.4f  s0 %+.4f'
  % (LAM, THR, TMAX_P5, S0))
P()

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('1 · HOW MANY ROWS ARE PARKED AT THE CAP, AND HOW FAR APART THEIR RECORDS ARE')
P('-' * 118)
P('   A row is PARKED when its surplus is at or below the cap crossing, s_cross = s0 - (TMAX-1)/THETA_R.')
P('   Parked rows are TIED in T under a hard clip: their per-game records no longer separate them at')
P('   all, and only games do. THAT IS THE DEFECT THE OWNER NAMED.')
P()
P('   %-6s %12s %10s %10s %14s %16s' %
  ('anchor', 'TMAX', 's_cross', 'parked n', 'their s_ped', 'spread tied away'))
PARK = {}
rows = [r for r in C[BASE]['charge'] if r.get('cond') and r.get('s_ped') is not None]
for pct in (5, 15, 20):
    tm = 1.0 - THR * (S_PQ[pct] - S0)
    cross = S0 - (tm - 1.0) / THR
    pk = [r for r in rows if r['s_ped'] <= cross]
    PARK[pct] = dict(tmax=tm, cross=cross, n=len(pk),
                     lo=(min(r['s_ped'] for r in pk) if pk else None),
                     hi=(max(r['s_ped'] for r in pk) if pk else None))
    P('   p%-5d %12.4f %10.3f %10d %14s %16s'
      % (pct, tm, cross, len(pk),
         ('%.1f..%.1f' % (PARK[pct]['lo'], PARK[pct]['hi'])) if pk else '-',
         ('%.1f pts a game' % (PARK[pct]['hi'] - PARK[pct]['lo'])) if pk else '-'))
P()
P('   READ THE p20 ROW. At the anchor the OWNER HIMSELF ASKED FOR, %d charged rows are parked and'
  % PARK[20]['n'])
P('   their per-game records span %.1f points a game. Under the hard clip every one of them pays the'
  % ((PARK[20]['hi'] - PARK[20]['lo']) if PARK[20]['n'] else 0.0))
P('   IDENTICAL rate. LOWERING THE CAP MAKES THE DEFECT HE NAMED WORSE, not better — %d rows tied at'
  % PARK[20]['n'])
P('   p20 against %d at ORDER P\'s p5. THAT IS WHY HE ASKED FOR A COMPRESSION INSTEAD OF A LOWER CAP,'
  % PARK[5]['n'])
P('   and it is the single strongest argument in this section. UNDER THE COMPRESSION NO ROW IS TIED:')
P('   T\'(s) is strictly increasing in shortfall everywhere and that is asserted in the engine at load')
P('   (S-S4), on a dense sweep, on every board that carries the form.')
P()

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('2 · PAIRWISE, AT EQUAL GAMES — DOES WORSE PLAY ALWAYS COST MORE?')
P('-' * 118)
P('   Every pair of charged rows whose CAREER GAMES agree to within 1, so A(g) is held fixed and the')
P('   only thing left is the record. A pair INVERTS when the row with the WORSE surplus is charged')
P('   the SAME or LESS. Ties count as inversions: the owner\'s requirement is "at least slightly more".')
P()
P('   ONE EXCLUSION, AND IT IS NECESSARY RATHER THAN CONVENIENT: pairs in which BOTH rows are charged')
P('   NOTHING are dropped. Both sit above the zero clip — they are producing at or above what their')
P('   entry price implies — and a tie at zero charge is the mechanism working, not the cap defect.')
P('   THIS SEAT\'s FIRST RUN DID NOT EXCLUDE THEM and reported 475 "ties" on a compression board,')
P('   which was the zero-clip region being counted as the cap. That was the scorer, not the form.')
P()
P('   %-8s %-46s %10s %10s %10s %12s' %
  ('board', '', 'pairs', 'inverted', 'of which', 'worst gap'))
P('   %-8s %-46s %10s %10s %10s %12s' % ('', '', '', '', 'exact TIES', 'tied away'))
PAIR = {}
GTOL = float(os.environ.get('OS_CAP_GTOL', '1.0'))
P('   games tolerance for a pair: %.2f career games.' % GTOL)
for t in [x for x in TAGS if x in C]:
    rr = [r for r in C[t]['charge'] if r.get('cond') and r.get('s_ped') is not None
          and r.get('g') and r['g'] > 0]
    rr.sort(key=lambda z: z['g'])
    npair = ninv = ntie = 0
    worst = 0.0
    n = len(rr)
    for i in range(n):
        for j in range(i + 1, n):
            if rr[j]['g'] - rr[i]['g'] > GTOL:
                break
            a, b = rr[i], rr[j]
            if a['s_ped'] == b['s_ped']:
                continue
            w, g_ = (a, b) if a['s_ped'] < b['s_ped'] else (b, a)   # w = the WORSE record
            if w['charge'] <= 1e-12 and g_['charge'] <= 1e-12:
                continue                                    # both above the zero clip — not the cap
            npair += 1
            if w['charge'] <= g_['charge'] + 1e-12:
                ninv += 1
                if abs(w['charge'] - g_['charge']) <= 1e-12:
                    ntie += 1
                    worst = max(worst, g_['s_ped'] - w['s_ped'])
    PAIR[t] = dict(pairs=npair, inverted=ninv, ties=ntie, worst=worst)
    P('   %-8s %-46s %10d %10d %10d %12.2f'
      % (t, NICE.get(t, '')[:46], npair, ninv, ntie, worst))
P()
P('   "worst gap tied away" is the largest distance in points a game between two players who pay')
P('   EXACTLY the same rate at the same games. On a hard-clip board it is the whole width of the')
P('   parked region. On a compression board it must be 0.00 — no two distinct records can tie.')
P()

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('3 · RELIEF REGRESSIVITY — WHO GETS PAID BY EACH REPAIR?')
P('-' * 118)
P('   Relief is measured as the FALL IN THE CHARGE against the ORDER P baseline on the same dial')
P('   line, in points of the pedigree leg (charge share x leg). Rows are put in deciles of s_ped on')
P('   the BASELINE board, so the decile a row sits in cannot move with the variant.')
P('   D1 is the DEEPEST tenth — the rows the owner said were paid first.')
P()
base_rows = {r['key']: r for r in C[BASE]['charge'] if r.get('cond') and r.get('s_ped') is not None}
sped = sorted(base_rows.values(), key=lambda z: z['s_ped'])
nb = len(sped)
DEC = {}
for i, r in enumerate(sped):
    DEC[r['key']] = min(9, int(10 * i / nb))
REG = {}
COMP = [('SC15', 'SB1', 'S2 COMPRESSION p15   vs ORDER P\'s clip'),
        ('SC20', 'SB1', 'S2 COMPRESSION p20   vs ORDER P\'s clip'),
        ('SC20A', 'SAB1', 'S2 COMPRESSION p20+A vs ORDER P\'s clip+A'),
        ('SR20A', 'SAB1', 'ORDER R p20 CLIP  +A vs ORDER P\'s clip+A'),
        ('SW47', 'SB1', 'S1 recency w=0.47'),
        ('SM', 'SB1', 'S5 mature premium'),
        ('SL10', 'SB1', 'S3 LAMBDA 0.10'),
        ('SALL', 'SAB1', 'ALL FOUR + A')]
P('   %-30s %11s | %s' % ('lever', 'total relief', '  '.join('D%d' % (d + 1) for d in range(10))))
P('   %-30s %11s | %s' % ('', '(leg points)', '  '.join('%4s' % 'shr%' for _ in range(10))))
for t, b, lab in COMP:
    if t not in C or b not in C:
        continue
    vr = {r['key']: r for r in C[t]['charge'] if r.get('cond')}
    br = {r['key']: r for r in C[b]['charge'] if r.get('cond')}
    tot = 0.0
    per = [0.0] * 10
    for k, r in br.items():
        if k not in vr or k not in DEC:
            continue
        leg = r.get('ped_leg') or 0.0
        d = (r['charge'] - vr[k]['charge']) * leg
        tot += d
        per[DEC[k]] += d
    REG[t] = dict(total=tot, per=per, base=b, label=lab,
                  share=[100.0 * p / tot if tot else 0.0 for p in per])
    P('   %-30s %11.1f | %s'
      % (lab[:30], tot, '  '.join('%4.0f' % (100.0 * p / tot if tot else 0.0) for p in per)))
P()
P('   THE HEADLINE COMPARISON, and it answers the owner\'s regressivity question directly:')
for a, b in (('SR20A', 'SC20A'),):
    if a in REG and b in REG:
        P('     the CAP-LOWERING lever (%s) puts %.0f%% of its relief in the deepest decile D1'
          % (a, REG[a]['share'][0]))
        P('     the COMPRESSION      (%s) puts %.0f%% of its relief in the deepest decile D1'
          % (b, REG[b]['share'][0]))
        P('     deepest THREE deciles: cap-lowering %.0f%% · compression %.0f%%'
          % (sum(REG[a]['share'][:3]), sum(REG[b]['share'][:3])))
        P('     S2-P4 said the compression would concentrate LESS relief in the deepest decile: %s'
          % ('RIGHT' if REG[b]['share'][0] < REG[a]['share'][0] else 'WRONG'))
P()

# ---------------------------------------------------------------------------------------------------
P('-' * 118)
P('4 · THE CHARGE DISTRIBUTION, BOARD BY BOARD')
P('-' * 118)
P('   %-8s %-46s %6s %9s %6s %6s %6s' %
  ('board', '', 'n', 'max chg', '>90%', '>75%', '>50%'))
DIST = {}
for t in [x for x in TAGS if x in C]:
    rr = [r for r in C[t]['charge'] if r.get('cond')]
    ch = [r['charge'] for r in rr]
    DIST[t] = dict(n=len(rr), mx=max(ch) if ch else 0.0,
                   g90=sum(1 for c in ch if c > 0.90), g75=sum(1 for c in ch if c > 0.75),
                   g50=sum(1 for c in ch if c > 0.50))
    P('   %-8s %-46s %6d %8.2f%% %6d %6d %6d'
      % (t, NICE.get(t, '')[:46], DIST[t]['n'], 100 * DIST[t]['mx'],
         DIST[t]['g90'], DIST[t]['g75'], DIST[t]['g50']))
P()

json.dump(dict(parked=PARK, pairs=PAIR, regressivity=REG, distribution=DIST),
          open(os.path.join(HERE, 'CAP_S%s.json' % os.environ.get('OS_CAP_SUF', '')), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CAP_S%s_out.txt' % os.environ.get('OS_CAP_SUF', '')), 'w').write('\n'.join(L) + '\n')
print('\nwrote CAP_S_out.txt / CAP_S.json')
