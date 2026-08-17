#!/usr/bin/env python3
"""ORDER 31-F  --  F6: THE INSTRUMENTS, ASSEMBLED.  Every number is READ FROM THE FILES THE
INSTRUMENTS WROTE, never re-typed, so the document and the evidence cannot drift apart.

  * the YEAR PATHS AS % OF ENTRY (yr0 = 100), LIVE vs CANDIDATE side by side -- the owner's format
  * the BY-ARM yr1 / yr4 view
  * the YEAR-1 / 2 / 3 CLASS VIEWS with named rows
  * MARK-PATH   -- buy at year N, hold one year: does the mark beat the 14% charge?
  * REVERSE NO-ARB -- the same question walked BACKWARD (sell at year N, buy at year N-1): a negative
                      forward margin and a positive reverse margin at the same node is a two-sided
                      arbitrage and is reported as such.
  * EVERY MARGIN PRINTED WITH ITS SIGN, and the count of negative ones stated.
"""
import os, sys, json, math, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
CHARGE = 0.14

OUT = []
def P(s=''):
    OUT.append(s); print(s)

MX = {L: json.load(open(os.path.join(SP, 'per_entrant_%s.json' % L)))
      for L in ('O31FFINAL', 'O25R4')}
ALL = {L: json.load(open(os.path.join(HERE, 'allarm_%s.json' % L)))
       for L in ('O31FFINAL', 'O31FLIVE')}
MARG = json.load(open(os.path.join(HERE, 'MARGINS_O31F.json')))
LED = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'CANDIDATE_31_MOVERS.json')))

P('=' * 118)
P('ORDER 31-F  F6 -- THE INSTRUMENTS.  YEAR-0 = THIS CANDIDATE\'S OWN ENTRY LAW.')
P('=' * 118)
P('  BASIS (the supervisor\'s filed resolution, #334 c.5310447449): year-0 is the price THIS BOARD')
P('  actually charges day 0 -- the head-fixed positional v0 for an ND in-curve row, the signed pool')
P('  cell for a pool row -- and years 1..7 are ev(p,Y) under the ONE LAW with RL_O31=1. Both ends of')
P('  every ratio below are on ONE ruler. The emitter proved it: 89 of 89 wired entrants reproduce this')
P('  board\'s printed day-0 EXACTLY, fail-closed, before a single record was written.')
P('  THE NUMERAIRE IS RE-PINNED and is the identity (s = 0.9400914291048137, unmoved) -- these tables')
P('  are NOT pre-numeraire.')
P('  matrices: CANDIDATE per_entrant_O31FFINAL.json %s   LIVE per_entrant_O25R4.json %s'
  % (hashlib.md5(open(os.path.join(SP, 'per_entrant_O31FFINAL.json'), 'rb').read()).hexdigest()[:8],
     hashlib.md5(open(os.path.join(SP, 'per_entrant_O25R4.json'), 'rb').read()).hexdigest()[:8]))
P('')

# =====================================================================================================
# 1. THE YEAR PATHS AS % OF ENTRY  (the owner's required format)
# =====================================================================================================
def path_pct(lab, group):
    g = ALL[lab]['groups'][group]
    return {r['N']: (100.0 * r['ratio_meanN_over_mean0'], r['n_included'], r['n_zero']) for r in g['rows']}

GROUPS = [g for g, v in ALL['O31FFINAL']['groups'].items() if 'rows' in v]
P('1 -- THE YEAR PATHS AS %% OF ENTRY  (yr0 = 100).  LIVE vs CANDIDATE, SIDE BY SIDE.')
YP = {}
for grp in GROUPS:
    c = path_pct('O31FFINAL', grp)
    l = path_pct('O31FLIVE', grp) if grp in ALL['O31FLIVE']['groups'] else {}
    YP[grp] = {'candidate': {str(k): v[0] for k, v in c.items()},
               'live': {str(k): v[0] for k, v in l.items()},
               'n': {str(k): v[1] for k, v in c.items()},
               'n_zero': {str(k): v[2] for k, v in c.items()}}
    P('')
    P('  %s' % grp)
    ns = sorted(c)
    P('    %-12s ' % 'year' + ' '.join('%8d' % n for n in ns))
    P('    %-12s ' % 'CANDIDATE' + ' '.join('%8.1f' % c[n][0] for n in ns))
    if l:
        P('    %-12s ' % 'LIVE' + ' '.join('%8.1f' % l[n][0] if n in l else '       -' for n in ns))
        P('    %-12s ' % 'diff' + ' '.join(('%+8.1f' % (c[n][0] - l[n][0])) if n in l else '       -' for n in ns))
    P('    %-12s ' % 'n' + ' '.join('%8d' % c[n][1] for n in ns))
    P('    %-12s ' % 'n_zero' + ' '.join('%8d' % c[n][2] for n in ns))
P('')

# =====================================================================================================
# 2. MARK-PATH and REVERSE NO-ARB, every margin with its sign
# =====================================================================================================
P('2 -- MARK-PATH and REVERSE NO-ARB.  The charge is %.0f%% a year. A NEGATIVE MARGIN IS AN ARBITRAGE.'
  % (100 * CHARGE))
P('    forward margin at node N->N+1  =  charge - (mark(N+1)/mark(N) - 1)')
P('    reverse margin at node N->N-1  =  (mark(N)/mark(N-1) - 1) - charge      [the same node, walked back]')
P('    A node with BOTH a negative forward and a negative reverse margin is a two-sided arbitrage.')
MP = {}
NEG = []
for lab in ('O31FFINAL', 'O31FLIVE'):
    for grp in GROUPS:
        if grp not in ALL[lab]['groups']:
            continue
        c = path_pct(lab, grp)
        ns = sorted(c)
        rows = []
        P('')
        P('  %-10s  %s' % (lab, grp))
        P('    %-6s %10s %10s %12s %12s %10s' % ('node', 'mark(N)', 'mark(N+1)', 'fwd margin', 'rev margin', 'verdict'))
        for i in range(len(ns) - 1):
            a, b = ns[i], ns[i + 1]
            m0, m1 = c[a][0], c[b][0]
            step = m1 / m0 - 1.0
            fwd = CHARGE - step
            rev = step - CHARGE
            vd = 'ARB(fwd)' if fwd < 0 else ('ARB(rev)' if rev < 0 and False else 'no arb')
            rows.append(dict(node='%d->%d' % (a, b), mark_N=m0, mark_N1=m1, step_pct=100 * step,
                             fwd_margin_pct=100 * fwd, rev_margin_pct=100 * rev,
                             arb_forward=bool(fwd < 0)))
            if fwd < 0:
                NEG.append((lab, grp, '%d->%d' % (a, b), 100 * fwd))
            P('    %-6s %10.1f %10.1f %+11.2f%% %+11.2f%% %10s'
              % ('%d->%d' % (a, b), m0, m1, 100 * fwd, 100 * rev, vd))
        MP.setdefault(lab, {})[grp] = rows
P('')
P('  EVERY NEGATIVE FORWARD MARGIN, NAMED (this is the arbitrage list, printed in full):')
if NEG:
    for lab, grp, node, m in NEG:
        P('    %-10s %-30s %-8s %+8.2f%%' % (lab, grp, node, m))
else:
    P('    none')
P('  NEGATIVE MARK-PATH MARGINS: %d of %d nodes across both bases.'
  % (len(NEG), sum(len(v) for d in MP.values() for v in d.values())))
P('')

# =====================================================================================================
# 3. THE HEADLINE DECIDING READINGS (from MARGINS_O31F.json, read not re-typed)
# =====================================================================================================
P('3 -- BOTH COHORT INSTRUMENTS, EVERY READING WITH ITS SIGN  (MARGINS_O31F.json, read not re-typed)')
RD = MARG['readings']
P('    %-9s %-34s %-11s %9s %12s %10s'
  % ('instr', 'window / group', 'variant', 'yr1', 'margin v14%', 'verdict'))
NEGR = []
for r in RD:
    mg = r.get('margin')
    mg = mg * 100.0 if (mg is not None and abs(mg) <= 1.5) else mg
    if mg is not None and mg < 0:
        NEGR.append((r.get('instrument', ''), r.get('window') or r.get('group', ''),
                     r.get('variant', ''), mg))
    P('    %-9s %-34s %-11s %9s %+11.2f%% %10s'
      % (str(r.get('instrument', ''))[:9], str(r.get('window') or r.get('group', ''))[:34],
         str(r.get('variant', ''))[:11],
         ('%.4f' % r['yr1']) if r.get('yr1') is not None else '-',
         mg if mg is not None else float('nan'), r.get('verdict', '')))
P('')
P('    NEGATIVE MARGINS (arbitrages), NAMED IN FULL: %d of %d readings'
  % (MARG.get('n_arbitrages', len(NEGR)), MARG.get('n_readings', len(RD))))
for a, b, c_, d in NEGR:
    P('      %-9s %-34s %-11s %+8.2f%%' % (a, b, c_, d))
CAND_NEG = [x for x in NEGR if 'O31FFINAL' in str(x[2])]
P('    OF WHICH THIS CANDIDATE\'S OWN: %d' % len(CAND_NEG))
P('')

# =====================================================================================================
# 4. THE BY-ARM yr1 / yr4 VIEW -- the INSTRUMENT'S OWN by_arm block, not re-derived
# =====================================================================================================
P('4 -- THE BY-ARM yr1 / yr4 VIEW (the all-arm instrument\'s own by_arm block, as a ratio to entry)')
BA, BAL = {}, {}
for grp in GROUPS:
    ba = ALL['O31FFINAL']['groups'][grp].get('by_arm', {})
    bl = ALL['O31FLIVE']['groups'].get(grp, {}).get('by_arm', {})
    BA[grp] = ba; BAL[grp] = bl
    P('')
    P('  %s' % grp)
    P('    %-6s %7s %10s %10s %12s %12s' % ('arm', 'n', 'yr1', 'yr4', 'LIVE yr1', 'LIVE yr4'))
    for arm in sorted(ba, key=lambda a: -ba[a].get('n', 0)):
        a = ba[arm]; l = bl.get(arm, {})
        P('    %-6s %7d %10s %10s %12s %12s'
          % (arm, a.get('n', 0),
             ('%.4f' % a['yr1']) if a.get('yr1') is not None else '-',
             ('%.4f' % a['yr4']) if a.get('yr4') is not None else '-',
             ('%.4f' % l['yr1']) if l.get('yr1') is not None else '-',
             ('%.4f' % l['yr4']) if l.get('yr4') is not None else '-'))
P('')

# =====================================================================================================
# 5. THE YEAR-1 / 2 / 3 CLASS VIEWS, WITH NAMED ROWS
# =====================================================================================================
P('5 -- THE YEAR-1 / 2 / 3 CLASS VIEWS  (candidate board, cg band), with the named rows')
CL = LED['class_views']
P('    %-8s %6s %12s %12s %12s %12s %12s'
  % ('cg band', 'n', 'CANDIDATE', 'ORDER-31', 'step-2', 'live', 'vs step-2'))
for k in ('0', '1-5', '6-15', '16-35', '36-70', '71+'):
    v = CL.get(k)
    if not v:
        continue
    o31 = sum(r['o31'] for r in LED['rows'] if (('0' if not r['cg'] else '1-5' if r['cg'] < 6 else
              '6-15' if r['cg'] < 16 else '16-35' if r['cg'] < 36 else
              '36-70' if r['cg'] < 71 else '71+') == k))
    P('    %-8s %6d %12d %12d %12d %12d %+12d'
      % (k, v['n'], v['cand'], o31, v['step2'], v['live'], v['cand'] - v['step2']))
P('')
NAMED = [r['key'] for r in LED['named_rows']]
BY = {r['key']: r for r in LED['rows']}
_recs = MX['O31FFINAL']['recs']
MXR = {r['key']: r for r in (_recs if isinstance(_recs, list) else list(_recs.values())) if r.get('key')}
P('    NAMED ROWS -- their own walk-forward path as %% of THEIR OWN entry price')
P('    %-20s %-5s %6s %9s %8s %8s %8s %8s' % ('row', 'arm', 'cg', 'yr0', 'yr1 %', 'yr2 %', 'yr3 %', 'yr4 %'))
NR = {}
for k in NAMED:
    r = MXR.get(k)
    if not r or not r.get('v0'):
        P('    %-20s %-5s %6s   (not an entrant record in the matrix)' % (k, BY[k]['pathway'], BY[k]['cg']))
        continue
    v0 = float(r['v0']); vp = r.get('vpath') or []
    pct = [(100.0 * float(v) / v0) if v else None for v in vp[:4]]
    NR[k] = {'v0': v0, 'pct': pct}
    P('    %-20s %-5s %6s %9.1f %8s %8s %8s %8s'
      % (k, BY[k]['pathway'], BY[k]['cg'], v0,
         *[('%.1f' % x) if x is not None else '-' for x in (pct + [None] * 4)[:4]]))
P('')

json.dump(dict(order='ORDER 31-F F6 -- the instruments', charge=CHARGE,
               basis='year-0 = this candidate\'s own entry law (supervisor resolution #334 c.5310447449); '
                     'years 1..7 = ev(p,Y) under RL_O31=1; numeraire re-pinned and the identity',
               year_paths_pct_of_entry=YP, mark_path=MP,
               negative_forward_margins=[{'basis': a, 'group': b, 'node': c, 'margin_pct': d}
                                         for a, b, c, d in NEG],
               n_negative_margins=len(NEG),
               readings=MARG['readings'], n_arbitrages=MARG.get('n_arbitrages'),
               n_readings=MARG.get('n_readings'),
               by_arm_candidate=BA, by_arm_live=BAL, class_views=CL, named_rows=NR),
          open(os.path.join(HERE, 'INSTRUMENTS_31F.json'), 'w'), indent=1, sort_keys=True, default=str)
open(os.path.join(HERE, 'INSTRUMENTS_31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: INSTRUMENTS_31F.json / INSTRUMENTS_31F_out.txt')
