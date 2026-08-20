#!/usr/bin/env python3
"""ORDER A REPAIR — R3: THE STANDING NO-ARB DELIVERY, TWO-SIDED, FIVE BANDS + EVERY POOL ARM,
WITH THE VANTAGE-CONSISTENCY MATRIX (DIAGNOSTIC-ONLY, amendment A2).

Plain words for the owner:
 - "Appreciation yr0->1" = how much a group's board value grows from draft day to the end of its
   first season. The carry rule says holding young talent should cost about 14% a year, so a group
   priced fairly appreciates at most 14% (buy side) and never DEPRECIATES (sell side).
 - A group above +14% is a BUY-SIDE RED (you could buy at year 0 and beat the carry).
 - A group below 0% is a SELL-SIDE RED (you could sell at year 0, buy back at year 1, and keep
   the difference).
 - The VANTAGE MATRIX asks the same question from later standpoints: from year 1, year 2 — is
   every group still priced to grow near the carry? It is DIAGNOSTIC ONLY: nothing in this repair
   was tuned to make it greener (amendment A2); what it shows is a finding for the owner.

Instruments: the five-band extended 338 (the owner's disclosed copy, run whole, output re-pointed)
on the draft clock over the harness ND population; the per-arm reader lifts the ALL-ARM cohort
instrument's own semantics (cohort clock, 'pre' rows excluded never zeroed) — constructions are
labeled on every table. Control: the O31FFINAL extended run must reproduce the committed
noarb_table_338_EXT.json ratios exactly.
"""
import os, sys, json, hashlib, subprocess, statistics, shutil
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
RUN = SP + '/o32r_noarb'
CARRY = 1.14

md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

# ==== 1. the extended five-band 338, run whole on both matrices ===================================
os.makedirs(RUN, exist_ok=True)
EXT_SRC = os.path.join(EV, 'candidate_31f', 'ext_2026-08-17', 't338_extended_DISCLOSED.py')
HARN = os.path.join(EV, 'landing_29_2026-08-13', 'noarb', 'harness_pvc_REPINNED_pass3.py')
_txt = open(EXT_SRC).read()
P('extended 338 committed md5 %s (owner five bands standing, yr0..12)' % md5f(EXT_SRC))
P('harness md5 %s (must begin 02dcf28c)' % md5f(HARN))
assert md5f(HARN).startswith('02dcf28c')
shutil.copy(HARN, os.path.join(RUN, 'harness_repointed.py'))
OLD = "    jp = os.path.join(HERE, 'noarb_table_338_EXT.json')"
NEW = "    jp = os.path.join(HERE, 'noarb_table_338_EXT_%s.json' % os.environ.get('O32R_TAG','x'))"
assert _txt.count(OLD) == 1
open(os.path.join(RUN, 't338_ext.py'), 'w').write(_txt.replace(OLD, NEW))
P('THE ONE EDIT to the disclosed copy: output filename tagged per matrix (printed above); as-run md5 %s'
  % hashlib.md5(_txt.replace(OLD, NEW).encode()).hexdigest())
ENV = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1', PYTHONHASHSEED='0')
EXT = {}
for tag, mx in (('31F', SP + '/per_entrant_O31FFINAL.json'), ('32R', SP + '/per_entrant_O32RFINAL.json')):
    env = dict(ENV, O32R_TAG=tag)
    r = subprocess.run([sys.executable, os.path.join(RUN, 't338_ext.py'), mx],
                       capture_output=True, text=True, env=env, cwd=RUN)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-2000:] + r.stderr[-2000:])
        raise SystemExit('extended 338 failed on %s' % tag)
    open(os.path.join(HERE, 't338_ext_%s_console.txt' % tag), 'w').write(r.stdout)
    EXT[tag] = json.load(open(os.path.join(RUN, 'noarb_table_338_EXT_%s.json' % tag)))
# CONTROL: the 31F rerun must reproduce the committed extended table exactly
COMMITTED = json.load(open(os.path.join(EV, 'candidate_31f', 'ext_2026-08-17', 'noarb_table_338_EXT.json')))
dev = 0
for g, G in COMMITTED['groups'].items():
    for row_c, row_n in zip(G['rows'], EXT['31F']['groups'][g]['rows']):
        if row_c['ratio_meanN_over_mean0'] != row_n['ratio_meanN_over_mean0']:
            dev += 1
P('CONTROL: the O31FFINAL extended rerun vs the committed table — %s'
  % ('EXACT (0 ratio deviations)' if dev == 0 else 'FAIL %d deviations' % dev))
assert dev == 0

# ==== 2. per-arm reader (the ALL-ARM instrument's own semantics, lifted) ==========================
def arm_paths(matrix_path, years=list(range(0, 9))):
    D = json.load(open(matrix_path))
    R = D['recs']
    WINDOW_END = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

    def cohort(r):
        y = r.get('year')
        if y is None: return None
        return y if r.get('type') == 'MSD' else y + 1

    def value_at(r, N):
        if N == 0:
            return float(r['v0']), 'v0'
        Y = cohort(r) + N - 1
        yrs = r.get('yrs') or []
        vp = r.get('vpath') or []
        if not yrs: return 0.0, 'ended'
        if Y < yrs[0]: return None, 'pre'
        if Y > yrs[-1]: return 0.0, 'ended'
        i = yrs.index(Y)
        if vp[i] is None: return 0.0, 'null'
        return float(vp[i]), 'path'

    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
    WINDOWS = [('PRIMARY 2005-2023', 2005, 2023), ('MODERN 2019-2023', 2019, 2023)]
    ARMS = ['RD', 'MSD', 'SSP', 'UNR', 'IRE', 'PDA', 'PDN', 'PDS']
    outw = {}
    for wname, lo, hi in WINDOWS:
        pop = [r for r in elig if lo <= cohort(r) <= hi]
        grp = {}
        sels = [(a, [r for r in pop if r['type'] == a]) for a in ARMS]
        sels.append(('ALLPOOL', [r for r in pop if r.get('is_pool')]))
        for nm, sub in sels:
            rows = {}
            for N in years:
                reached = sub if N == 0 else [r for r in sub if cohort(r) + N - 1 <= WINDOW_END]
                vals, v0s, npre = [], [], 0
                for r in reached:
                    v, k = value_at(r, N)
                    if k == 'pre':
                        npre += 1; continue
                    vals.append(v); v0s.append(float(r['v0']))
                if vals:
                    rows[N] = dict(n=len(vals), n_pre=npre,
                                   ratio=statistics.mean(vals) / statistics.mean(v0s))
            grp[nm] = dict(n=len(sub), rows=rows)
        outw[wname] = grp
    return outw


ARMP = {'31F': arm_paths(SP + '/per_entrant_O31FFINAL.json'),
        '32R': arm_paths(SP + '/per_entrant_O32RFINAL.json')}

# ==== 3. the two-sided tables =====================================================================
def flag(a):
    """(sell, buy) verdicts for a yr0->1 appreciation a."""
    sell = 'RED (depreciates)' if a < 0 else 'ok'
    buy = 'RED (beats the 14% carry)' if a > 0.14 else 'ok'
    return sell, buy


P('')
P('=' * 100)
P('TWO-SIDED FIVE-BAND TABLE (ND, draft clock, extended 338 instrument) — before vs after the repair')
P('=' * 100)
P('A group is fairly priced if it appreciates BETWEEN 0%% and +14%% over its first year.')
P('%-16s | %10s %10s %10s | %10s %10s %10s' % ('band', 'C31 yr0-1', 'sell', 'buy', '32R yr0-1', 'sell', 'buy'))
BANDS5 = ['picks 1-10', 'picks 11-20', 'picks 21-30', 'picks 31-40', 'picks 41-64']
TB = {}
for g in ['ALL picks 1-64', 'picks 1-20', 'picks 21-64'] + BANDS5:
    rows31 = {r['N']: r['ratio_meanN_over_mean0'] for r in EXT['31F']['groups'][g]['rows']}
    rows32 = {r['N']: r['ratio_meanN_over_mean0'] for r in EXT['32R']['groups'][g]['rows']}
    a31 = rows31[1] / rows31[0] - 1.0
    a32 = rows32[1] / rows32[0] - 1.0
    s31, b31 = flag(a31); s32, b32 = flag(a32)
    TB[g] = dict(c31=a31, r32=a32, path31=rows31, path32=rows32)
    P('%-16s | %+9.2f%% %10s %10s | %+9.2f%% %10s %10s'
      % (g, 100 * a31, s31.split()[0], b31.split()[0], 100 * a32, s32.split()[0], b32.split()[0]))
sp31 = max(TB[g]['c31'] for g in BANDS5) - min(TB[g]['c31'] for g in BANDS5)
sp32 = max(TB[g]['r32'] for g in BANDS5) - min(TB[g]['r32'] for g in BANDS5)
P('five-band spread (widest minus narrowest): C31 %.1f points -> repair %.1f points  [DIAGNOSTIC — reported, not targeted]'
  % (100 * sp31, 100 * sp32))

P('')
P('=' * 100)
P('TWO-SIDED POOL-ARM TABLE (cohort clock, all-arm instrument semantics) — repair, both windows')
P('=' * 100)
P('MSD year-1 caption, in plain words: a mid-season draftee debuts in the SAME year he is drafted,')
P('but the matrix stores his seasons starting the year after. His true first-season cell cannot be')
P('read from this matrix, so those rows are EXCLUDED from that one year and counted — never scored')
P('zero and never printed as a blank. The n_pre column is that count.')
ARM_TB = {}
for wname, grp in ARMP['32R'].items():
    P('')
    P('--- %s ---' % wname)
    P('%-8s %5s | %8s %8s %8s %8s %8s | %10s %6s %14s %14s' %
      ('arm', 'n', 'yr0', 'yr1', 'yr2', 'yr4', 'yr8', 'yr0->1', 'n_pre', 'sell side', 'buy side'))
    for nm, d in grp.items():
        rows = d['rows']
        if 1 not in rows or 0 not in rows:
            P('%-8s %5d | (window has no year-1 cell)' % (nm, d['n']))
            continue
        a = rows[1]['ratio'] / rows[0]['ratio'] - 1.0
        s, b = flag(a)
        ARM_TB.setdefault(wname, {})[nm] = dict(n=d['n'], apprec=a,
                                                path={N: rows[N]['ratio'] for N in rows})
        P('%-8s %5d | %8.4f %8.4f %8s %8s %8s | %+9.2f%% %6d %14s %14s'
          % (nm, d['n'], rows[0]['ratio'], rows[1]['ratio'],
             ('%.4f' % rows[2]['ratio']) if 2 in rows else '—',
             ('%.4f' % rows[4]['ratio']) if 4 in rows else '—',
             ('%.4f' % rows[8]['ratio']) if 8 in rows else '—',
             100 * a, rows[1]['n_pre'], s.split()[0], b.split()[0]))

# ==== 4. the vantage-consistency matrix (DIAGNOSTIC-ONLY) =========================================
SC = json.load(open(os.path.join(HERE, 'W2_32R_SCORECARD.json')))
FAIR = SC['band_fair_yr1']
P('')
P('=' * 100)
P('VANTAGE-CONSISTENCY MATRIX — DIAGNOSTIC ONLY (amendment A2: nothing was calibrated toward this)')
P('=' * 100)
P('Reading guide: each cell is how much the group is priced to GROW from vantage year V over the')
P('next k years. The carry column is the fair benchmark (1.14^k). A well-priced group sits near')
P('the carry from EVERY vantage. Divergence is printed RED as a FINDING for investigation.')
VM = {}
for g in BANDS5:
    rows32 = TB[g]['path32']
    VM[g] = {}
    P('')
    P('%s   (fair yr1 mark %.3f; actual yr1 mark %.3f — %s)'
      % (g, FAIR[g.replace('picks ', '')]['fair_yr1'], FAIR[g.replace('picks ', '')]['mark_yr1'],
         'near fair' if abs(FAIR[g.replace('picks ', '')]['gap_vs_fair']) < 0.05 else
         ('%.0f points %s fair' % (100 * abs(FAIR[g.replace('picks ', '')]['gap_vs_fair']),
                                   'below' if FAIR[g.replace('picks ', '')]['gap_vs_fair'] < 0 else 'above'))))
    P('  %-10s %10s %10s %10s %10s | %s' % ('vantage', 'k=1', 'k=2', 'k=3', 'k=4', 'carry: 1.14 1.30 1.48 1.69'))
    for V in (0, 1, 2):
        cells = []
        for k in (1, 2, 3, 4):
            gr = rows32[V + k] / rows32[V] if rows32.get(V) else float('nan')
            VM[g]['V%d_k%d' % (V, k)] = gr
            red = '*' if (gr < 1.0 or gr > CARRY ** k * 1.10) else ' '
            cells.append('%9.3f%s' % (gr, red))
        P('  yr %-7d %s' % (V, ' '.join(cells)))
sp = {}
for V in (0, 1, 2):
    for k in (1, 2, 3, 4):
        vals = [VM[g]['V%d_k%d' % (V, k)] for g in BANDS5]
        sp['V%d_k%d' % (V, k)] = max(vals) - min(vals)
P('')
P('band-vs-band spread of forward growth (max band minus min band, in growth-ratio points):')
P('  %-8s %8s %8s %8s %8s' % ('vantage', 'k=1', 'k=2', 'k=3', 'k=4'))
for V in (0, 1, 2):
    P('  yr %-5d %8.3f %8.3f %8.3f %8.3f' % (V, sp['V%d_k1' % V], sp['V%d_k2' % V], sp['V%d_k3' % V], sp['V%d_k4' % V]))
# the same matrix on C31 for the before/after the addendum asked for (yr1 vantage)
VM31 = {}
for g in BANDS5:
    rows31 = TB[g]['path31']
    for k in (1, 2, 3, 4):
        VM31.setdefault(g, {})['k%d' % k] = rows31[1 + k] / rows31[1]
sp31_v1 = {k: max(VM31[g]['k%d' % k] for g in BANDS5) - min(VM31[g]['k%d' % k] for g in BANDS5) for k in (1, 2, 3, 4)}
P('  yr-1-vantage spread BEFORE the repair (C31): k=1 %.3f  k=2 %.3f  k=3 %.3f  k=4 %.3f'
  % (sp31_v1[1], sp31_v1[2], sp31_v1[3], sp31_v1[4]))

# leg attribution per addendum 3, plain words
P('')
P('WHERE EACH BAND\'S INCONSISTENCY LIVES (using the band-level fair yr1 = 1.14 x (1 - yr1 delivered share)):')
for g in BANDS5:
    key = g.replace('picks ', '')
    f = FAIR[key]
    yr1_leg = f['mark_yr1'] - f['fair_yr1']
    rows32 = TB[g]['path32']
    g15 = rows32[5] / rows32[1]
    later_leg = g15 - CARRY ** 4
    P('  %-12s yr1-mark leg %+0.3f (mark %.3f vs fair %.3f) · later-years leg (yr1->5 growth %.3f vs carry %.3f) %+0.3f'
      % (g, yr1_leg, f['mark_yr1'], f['fair_yr1'], g15, CARRY ** 4, later_leg))
P('')
P('Plain reading: a NEGATIVE yr1-mark leg means the band is priced too low at the end of year one;')
P('a POSITIVE later-years leg means its price is then expected to grow faster than the carry —')
P('the two legs of the same mispricing. The late bands carry most of both.')

json.dump(dict(order='ORDER A REPAIR R3 — two-sided five-band + pool-arm no-arb + vantage matrix (diagnostic)',
               ext_control_exact=True,
               five_band=TB, five_band_spread_c31=sp31, five_band_spread_32r=sp32,
               pool_arms=ARM_TB, vantage_matrix_32r=VM, vantage_spread_32r=sp,
               vantage_yr1_spread_c31=sp31_v1,
               band_fair_yr1=FAIR,
               msd_caption='MSD debut-year rows are excluded from that year and counted (n_pre), never zeroed'),
          open(os.path.join(HERE, 'NOARB_32R.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'NOARB_32R_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: NOARB_32R.json / NOARB_32R_out.txt / t338_ext_{31F,32R}_console.txt')
