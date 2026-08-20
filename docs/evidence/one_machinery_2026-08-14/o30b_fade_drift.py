#!/usr/bin/env python3
# ORDER 30B STEP 2 -- THE FADE RE-DERIVATION DRIFT, MEASURED AND ATTRIBUTED.
# R1 is binding: the law must be calibrated against its own ruler, so o30a2_recut.py (BYTE-IDENTICAL,
# md5 fe6f436ab23056d717f693091946309a) was re-run with POSV = the STEP-1 FINAL cells and nothing else
# changed. This script reads the two runs' JSON side by side and attributes the drift.
import json, os, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OLD = json.load(open(os.path.join(ROOT, 'docs/evidence/sitter_fade_2026-08-14/SITTER_DISCOUNT_TABLE_2.json')))
NEW = json.load(open(os.path.join(HERE, 'FADE30B_TABLE.json')))
LOG = []
def P(s=''):
    print(s); LOG.append(s)

LB = 'L-B outcome-blind floor'
UN = 'UNCONDITIONAL (ORDER 30A)'
LA = 'L-A reconstruction as filed'

P('=' * 110)
P('ORDER 30B STEP 2 -- THE FADE, RE-DERIVED AGAINST THE STEP-1 FINAL v0s (R1)')
P('=' * 110)
P('Instrument: o30a2_recut.py, BYTE-IDENTICAL (md5 fe6f436ab23056d717f693091946309a). The ONLY thing')
P('that changed under it is nd_v0.posv -- the denominator of every ratio it forms.')
P('')
P('THE HEADLINE ROW, BOTH RULERS SIDE BY SIDE')
P('  %-6s | %-28s | %-28s | %-10s' % ('depth', 'ON THE 29B v0s (the RULING)', 'ON THE 30B v0s (R1)', 'drift'))
for N in ('1', '2', '3', '4', '5', '6'):
    for lab, tag in ((LB, 'L-B'), (UN, 'UNC')):
        o = OLD['T1']['D'][lab].get(N); n = NEW['T1']['D'][lab].get(N)
        no = OLD['T1']['surfaces'][lab][N].get('n', 0); nn = NEW['T1']['surfaces'][lab][N].get('n', 0)
        if o is None and n is None:
            continue
        P('  %-3s %-3s| %10s  (n=%4d)         | %10s  (n=%4d)         | %+8s'
          % (N, tag,
             ('%.4f' % o) if o is not None else '--', no,
             ('%.4f' % n) if n is not None else '--', nn,
             ('%.4f' % (n - o)) if (o is not None and n is not None) else '--'))
P('')
P('  RAW(1) normaliser  %.6f -> %.6f  (%+.4f%%)'
  % (OLD['T1']['raw1'], NEW['T1']['raw1'], 100.0 * (NEW['T1']['raw1'] / OLD['T1']['raw1'] - 1.0)))
P('')

# --- monotonicity of the wired depths -------------------------------------------------------------
oD = [OLD['T1']['D'][LB][str(N)] for N in (2, 3, 4)]
nD = [NEW['T1']['D'][LB][str(N)] for N in (2, 3, 4)]
P('MONOTONICITY OF THE L-B ROW OVER THE DEPTHS THE RULING NAMES (2 / 3 / 4)')
P('  RULING  %.4f > %.4f > %.4f   monotone decreasing: %s' % (oD[0], oD[1], oD[2], oD[0] > oD[1] > oD[2]))
P('  R1      %.4f > %.4f ? %.4f   monotone decreasing: %s' % (nD[0], nD[1], nD[2], nD[0] > nD[1] > nD[2]))
P('  the UNCONDITIONAL row stays monotone on BOTH rulers:')
oU = [OLD['T1']['D'][UN][str(N)] for N in (2, 3, 4, 5, 6)]
nU = [NEW['T1']['D'][UN][str(N)] for N in (2, 3, 4, 5, 6)]
P('    RULING  %s' % ' > '.join('%.4f' % x for x in oU))
P('    R1      %s' % ' > '.join('%.4f' % x for x in nU))
P('')

# --- the fitted decay, both rulers ----------------------------------------------------------------
def fit_decay(d2, d3):
    """D(c) = exp(-a*(c-1)^b) through D(2) and D(3) with D(1)=1. The 'fitted decay' ruling 2 extrapolates."""
    a = -math.log(d2)
    x = -math.log(d3) / a
    b = math.log(x) / math.log(2.0)
    return a, b

P('RULING 2 -- "DEEP END = EXTRAPOLATE THE FITTED DECAY PAST YEAR 4", EVALUATED ON BOTH RULERS')
for tag, d2, d3, d4 in (('RULING', oD[0], oD[1], oD[2]), ('R1    ', nD[0], nD[1], nD[2])):
    a, b = fit_decay(d2, d3)
    P('  %s  fitted exp(-%.4f*(c-1)^%.4f)   at c=4 -> %.4f   at c=5 -> %.4f   at c=6 -> %.4f'
      % (tag, a, b, math.exp(-a * 3 ** b), math.exp(-a * 4 ** b), math.exp(-a * 5 ** b)))
    P('           the MEASURED depth-4 cell (n=%s) reads %.4f -- %s the fitted decay by %.4f'
      % (NEW['T1']['surfaces'][LB]['4'].get('n') if tag.strip() == 'R1' else
         OLD['T1']['surfaces'][LB]['4'].get('n'), d4,
         'ABOVE' if d4 > math.exp(-a * 3 ** b) else 'below', abs(d4 - math.exp(-a * 3 ** b))))
P('')

# --- the games backbone, both rulers --------------------------------------------------------------
P('THE CUMULATIVE GAMES BACKBONE (ruling 4), BOTH RULERS')
P('  %-8s %-10s %-10s %-8s' % ('<= k', 'RULING', 'R1', 'drift'))
ocum = OLD['T4']['cumulative_leq']; ncum = NEW['T4']['cumulative_leq']
for k in ('0', '2', '5', '10'):
    o = ocum.get('2|<=%s' % k); n = ncum.get('2|<=%s' % k)
    if o and n:
        P('  %-8s %-10.4f %-10.4f %+.4f' % ('<=%s' % k, o['D'], n['D'], n['D'] - o['D']))
P('')

# --- attribution: which rows drove the depth-3 fall ------------------------------------------------
op = {r['key']: r for r in OLD['per_player_fitted']}
np_ = {r['key']: r for r in NEW['per_player_fitted']}
P('ATTRIBUTION -- the drift is ENTIRELY the denominator (v0), by construction')
moved = [(k, op[k]['v0'], np_[k]['v0']) for k in np_ if k in op and abs(op[k]['v0'] - np_[k]['v0']) > 1e-9]
P('  fitted rows whose v0 moved: %d of %d' % (len(moved), len(np_)))
ups = sum(1 for _, a, b in moved if b > a); dns = len(moved) - ups
P('  v0 UP on %d rows, DOWN on %d rows' % (ups, dns))
BOTH = [k for k in np_ if k in op]
NEWONLY = sorted(k for k in np_ if k not in op)
P('  rows PRESENT ONLY IN THE R1 FIT: %d %s' % (len(NEWONLY), NEWONLY))
P('    (the A2 cure re-admits them: their v0 was exactly 0 on the 29B cells and ORDER 30A/30A-2')
P('     dropped every v0 == 0 row from every ratio.)')
P('  mean v0 over the common rows  %.2f -> %.2f  (%+.2f%%)'
  % (sum(op[k]['v0'] for k in BOTH) / len(BOTH), sum(np_[k]['v0'] for k in BOTH) / len(BOTH),
     100.0 * (sum(np_[k]['v0'] for k in BOTH) / sum(op[k]['v0'] for k in BOTH) - 1.0)))
P('  TEN LARGEST v0 MOVES AMONG THE FITTED ROWS')
P('  %-26s %6s %5s %10s %10s %9s' % ('key', 'pos', 'pick', 'v0 RULING', 'v0 R1', 'delta%'))
for k, a, b in sorted(moved, key=lambda t: -abs(t[2] / max(t[1], 1e-9) - 1.0))[:10]:
    P('  %-26s %6s %5s %10.2f %10.2f %+8.1f%%'
      % (k, np_[k]['pos'], np_[k]['pick'], a, b, 100.0 * (b / a - 1.0)))
P('')

json.dump(dict(
    ruling=dict(LB={N: OLD['T1']['D'][LB][N] for N in ('1', '2', '3', '4', '5', '6')},
                UNC={N: OLD['T1']['D'][UN][N] for N in ('1', '2', '3', '4', '5', '6')},
                raw1=OLD['T1']['raw1']),
    r1=dict(LB={N: NEW['T1']['D'][LB][N] for N in ('1', '2', '3', '4', '5', '6')},
            UNC={N: NEW['T1']['D'][UN][N] for N in ('1', '2', '3', '4', '5', '6')},
            raw1=NEW['T1']['raw1']),
    n_LB={N: NEW['T1']['surfaces'][LB][N].get('n', 0) for N in ('1', '2', '3', '4', '5', '6')},
    monotone_ruling=bool(oD[0] > oD[1] > oD[2]), monotone_r1=bool(nD[0] > nD[1] > nD[2]),
    fitted_decay_ruling=dict(zip(('a', 'b'), fit_decay(oD[0], oD[1]))),
    fitted_decay_r1=dict(zip(('a', 'b'), fit_decay(nD[0], nD[1]))),
    backbone_ruling={k: ocum['2|<=%s'%k]['D'] for k in ('0','2','5','10') if '2|<=%s'%k in ocum},
    backbone_r1={k: ncum['2|<=%s'%k]['D'] for k in ('0','2','5','10') if '2|<=%s'%k in ncum},
    v0_rows_moved=len(moved), v0_up=ups, v0_down=dns,
), open(os.path.join(HERE, 'FADE30B_DRIFT.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'FADE30B_DRIFT_out.txt'), 'w').write('\n'.join(LOG) + '\n')
print('wrote FADE30B_DRIFT.json / FADE30B_DRIFT_out.txt')
