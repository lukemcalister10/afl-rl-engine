#!/usr/bin/env python3
"""ORDER P BUILD — THE OWNER'S LAWS, SCORED ON THE BUILT BOARDS, IN BOARD POINTS.

Pure JSON reads over the boards build_allP.sh already wrote — no engine run here, so nothing can
drift between what is scored and what was built.

  candP  1f176444  the landing candidate — the base stack with every ORDER I/P dial off
  Kref   f3101883  ORDER K's ruled line with RL_O37 UNSET. FALSIFIER B1: this must be byte-exact.
  P                THE DECISION BOARD
  Pimp             RL_O37=1 with every RL_O36_* unset — the dial must carry the stack on its own
  P2               the determinism repeat
  Peta0            the same stack with the charge switched off entirely (RL_O36_ETA=0). This is the
                   UNCHARGED board, the ceiling FALSIFIER B10 says no row may price above.
"""
import json, math, os, re, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OP = SP + '/op'
TAGS = [t for t in ('candP', 'Kref', 'P', 'Pimp', 'P2', 'Peta0')
        if os.path.exists(OP + '/bb_%s/rl_after/rl_app_data.json' % t)]
BP = {t: OP + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
RAW = {t: json.load(open(BP[t])) for t in TAGS}
B = {t: {r['key']: r for r in RAW[t]['active']} for t in TAGS}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in TAGS}
KEYS = sorted(V['P'])
AGE = {k: B['P'][k]['age'] for k in KEYS}
POS = {k: (B['P'][k].get('gf') or B['P'][k]['grp']) for k in KEYS}
NAME = {k: B['P'][k].get('name') or k for k in KEYS}
C31 = json.load(open(SP + '/cand31.json'))
R31 = {r['key']: r for r in C31['rows']}
LED = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_P_MOVERS.json')))
LR = {r['key']: r for r in LED['rows']}
OUT = {}
L = []


def P(s=''):
    print(s); L.append(str(s))


P('=' * 118)
P('ORDER P BUILD — THE OWNER\'S LAWS ON THE BUILT BOARD.  board points.')
P('=' * 118)
P('  boards: %s' % {t: MD5[t][:8] for t in TAGS})
P('  active priced rows: %d' % len(KEYS))
P()

# ---- the build-failing identities -------------------------------------------------------------------
P('== THE BUILD-FAILING IDENTITIES ==')
b1 = MD5['Kref'].startswith('f3101883')
b2 = ('P2' in MD5) and MD5['P'] == MD5['P2']
bimp = ('Pimp' in MD5) and MD5['P'] == MD5['Pimp']
bbase = MD5['candP'].startswith('1f176444')
P('  B1  DIAL OFF reproduces ORDER K f3101883 BYTE-EXACT     : %s  (%s)'
  % ('PASS' if b1 else 'FAIL — B1 FIRES', MD5['Kref'][:8]))
P('  B2  determinism x2 on the DECISION board                : %s  (%s vs %s)'
  % ('PASS' if b2 else 'FAIL — B2 FIRES', MD5['P'][:8], MD5.get('P2', '-')[:8]))
P('      the new dial IMPLIES the O32/O35/O36-K stack alone  : %s  (%s vs %s)'
  % ('PASS' if bimp else 'FAIL', MD5['P'][:8], MD5.get('Pimp', '-')[:8]))
P('      the base stack still reproduces 1f176444            : %s  (%s)'
  % ('PASS' if bbase else 'FAIL', MD5['candP'][:8]))
OUT['identities'] = dict(b1=b1, b2=b2, dial_implies=bimp, base=bbase, md5={t: MD5[t] for t in TAGS})
P()

# ---- B10: no row above its own uncharged price -------------------------------------------------------
P('== B10 — NO ROW PRICES ABOVE ITS OWN UNCHARGED PRICE (the forbidden-set bound P-F1) ==')
if 'Peta0' in V:
    over = [(k, V['P'][k], V['Peta0'][k]) for k in KEYS if V['P'][k] > V['Peta0'][k]]
    overK = [(k, V['Kref'][k], V['Peta0'][k]) for k in KEYS if V['Kref'][k] > V['Peta0'][k]]
    P('  the uncharged board (the same stack with the charge switched off, RL_O36_ETA=0) totals %d;'
      % sum(V['Peta0'].values()))
    P('  ORDER P totals %d and ORDER K totals %d.' % (sum(V['P'].values()), sum(V['Kref'].values())))
    P('  rows priced ABOVE their own uncharged price:  ORDER P %d of %d   ·   ORDER K %d of %d'
      % (len(over), len(KEYS), len(overK), len(KEYS)))
    P('  -> B10 %s' % ('DID NOT FIRE — the charge can only ever subtract, so the ceiling this mechanism '
                       'can reach is a board the forbidden set is already absent from'
                       if not over else 'FIRED: %s' % over[:5]))
    OUT['b10'] = dict(n_over=len(over), n_over_K=len(overK), eta0_total=sum(V['Peta0'].values()),
                      rows=[dict(key=k, p=a, eta0=b) for k, a, b in over[:20]])
else:
    P('  the uncharged board has not been built yet — B10 not scored.')
P()

# ---- the mature-row law ------------------------------------------------------------------------------
P('== THE MATURE-ROW LAW AND THE VETERAN CAPS (age 24 and over) ==')
TOT = sum(V['Kref'].values())
CH_RAIL, NET_RAIL = 0.0015 * TOT, 0.0010 * TOT
mat = [k for k in KEYS if AGE[k] >= 24]
mv = [(k, V['P'][k] - V['Kref'][k]) for k in mat]
mv = [(k, d) for k, d in mv if d != 0]
churn = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
mvL = [(k, V['P'][k] - V['candP'][k]) for k in mat]
mvL = [(k, d) for k, d in mvL if d != 0]
churnL = sum(abs(d) for _, d in mvL); netL = sum(d for _, d in mvL)
mvK = [(k, V['Kref'][k] - V['candP'][k]) for k in mat]
mvK = [(k, d) for k, d in mvK if d != 0]
P('  board total (ORDER K) %d   ·   mature rows %d of %d' % (TOT, len(mat), len(KEYS)))
P('  rails: churn <= %.0f (0.15%% of the board)   |net| <= %.0f (0.10%%)' % (CH_RAIL, NET_RAIL))
P('  TWO READINGS, because ORDER P\'s own published estimate was taken against the LANDING CANDIDATE,')
P('  not against ORDER K, and reporting only one of them would be misleading:')
P('    ORDER P vs ORDER K            : %d mature rows move · churn %.0f · net %+.0f  -> %s'
  % (len(mv), churn, net, 'INSIDE BOTH' if (churn <= CH_RAIL and abs(net) <= NET_RAIL) else 'BREACH — B4 FIRES'))
P('    ORDER P vs the landing candidate: %d mature rows move · churn %.0f · net %+.0f  -> %s'
  % (len(mvL), churnL, netL,
     'INSIDE BOTH' if (churnL <= CH_RAIL and abs(netL) <= NET_RAIL) else 'BREACH — B4 FIRES'))
P('    ORDER K vs the landing candidate: %d mature rows move · churn %.0f · net %+.0f  (ORDER K\'s own '
  'published 947 / -601)' % (len(mvK), sum(abs(d) for _, d in mvK), sum(d for _, d in mvK)))
P('  ORDER P\'s PUBLISHED ESTIMATE, on the landing-candidate basis, was churn 951 / net -595.')
if mv:
    P('  every mature row that moves:')
    for k, d in sorted(mv, key=lambda x: -abs(x[1]))[:25]:
        P('    %-28s age %2d  %6d -> %6d  %+5d' % (NAME[k][:28], AGE[k], V['Kref'][k], V['P'][k], d))
OUT['veteran'] = dict(n=len(mv), churn=churn, net=net, n_vs_landing=len(mvL), churn_vs_landing=churnL, net_vs_landing=netL, churn_rail=CH_RAIL, net_rail=NET_RAIL,
                      inside=bool(churn <= CH_RAIL and abs(net) <= NET_RAIL))
P()
P('  THE AGE GATE, read on the whole board:')
for lo, hi, lab in ((0, 20, '20 and under'), (21, 23, '21-23'), (24, 99, '24 and over')):
    s = [k for k in KEYS if lo <= AGE[k] <= hi]
    P('    %-14s rows %4d   total %+7d' % (lab, len(s), sum(V['P'][k] - V['Kref'][k] for k in s)))
P()

# ---- day-0 -------------------------------------------------------------------------------------------
P('== B3 — THE DAY-0 ENTRY VALUES ==')
zero = [k for k in KEYS if (LR.get(k) or {}).get('m_g', 0) == 0]
zmove = [k for k in zero if V['P'][k] != V['Kref'][k]]
P('  rows with ZERO career games on the board: %d.  A(0) = 0 exactly, so not one may move.' % len(zero))
P('  rows with zero games that moved: %d  -> %s' % (len(zmove), 'PASS' if not zmove else 'FAIL — B3 FIRES'))
P('  the emit\'s own printed-day-0 replication proof is run against ORDER K\'s OWN DAY0_K.json, so it')
P('  is the same test at the printed-price level: see EMIT_PBUILT_out.txt for the 89-of-89 line.')
OUT['day0'] = dict(n_zero=len(zero), n_moved=len(zmove))
P()

# ---- the charge, side by side -------------------------------------------------------------------------
src = open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py'), encoding='utf-8').read()
Cc = {}
for nm in ('O37_G0', 'O37_BETA_SAT', 'O37_LAMBDA', 'O37_S0', 'O37_S_P5'):
    Cc[nm] = float(re.search(r'^\s*%s=(-?[0-9.eE+-]+)\s' % nm, src, re.M).group(1))
THR = Cc['O37_BETA_SAT'] / Cc['O37_LAMBDA']
TMAX = 1.0 - THR * (Cc['O37_S_P5'] - Cc['O37_S0'])
A = lambda g: 1.0 - math.exp(-g / Cc['O37_G0'])
T = lambda s: min(max(1.0 - THR * (s - Cc['O37_S0']), 0.0), TMAX)
FN = lambda g, s: 1.0 - math.exp(-Cc['O37_LAMBDA'] * A(g) * T(s))
FO = lambda g: max(0.0, 0.50 * (g / 14.0) * math.exp(1.0 - g / 14.0)) if g > 0 else 0.0
P('== THE CHARGE, SIDE BY SIDE. Percentage of the pedigree leg removed. ==')
P('  %-6s | %-12s | %-46s' % ('games', 'ORDER K', 'ORDER P, by pedigree-conditional surplus s_P'))
P('  %-6s | %-12s | %10s %10s %10s %10s' % ('', 'blind', 's_P=-25', 's_P=-10', 's_P=0', 's_P=+10'))
CHG = {}
for g in (1, 2, 3, 5, 8, 10, 14, 17, 20, 25, 30, 36, 50):
    cells = [100 * FN(g, s) for s in (-25, -10, 0, 10)]
    CHG[g] = dict(old=100 * FO(g), new=cells)
    P('  %-6d | %11.1f%% | %9.1f%% %9.1f%% %9.1f%% %9.1f%%' % (g, 100 * FO(g), *cells))
P('  READ THE 17-GAME ROW AGAINST THE 36-GAME ROW IN THE ORDER K COLUMN: %.1f%% falls to %.1f%%.'
  % (100 * FO(17), 100 * FO(36)))
P('  A 36-game player kept MORE unearned pedigree than a 17-game player, whatever either of them did.')
P('  The ORDER P column never falls as games rise, at any surplus. That is the defect, removed.')
P('  THE ZERO POINT: T hits zero at s_P = %+.2f. A young player producing within about a point a game'
  % (Cc['O37_S0'] + 1.0 / THR))
P('  of what a player at his price normally produces, at his age, pays NOTHING on his pedigree leg.')
OUT['charge'] = CHG
P()

# ---- the charge by pick band, on the board -------------------------------------------------------------
P('== WHERE THE CHARGE FALLS, BY PICK BAND, ON THE YOUNG BOARD ==')
P('  This is the owner\'s own test: under ORDER K the charge is flat in pick because it only reads')
P('  games. Under ORDER P it should fall HARDEST ON THE TOP OF THE DRAFT, because that is where the')
P('  most expectation is priced in.')


def band(p):
    if p is None: return '41-64 and pool'
    p = int(p)
    return '1-10' if p <= 10 else ('11-20' if p <= 20 else ('21-40' if p <= 40 else '41-64 and pool'))


young = [k for k in KEYS if (LR.get(k) or {}).get('m_sP') is not None and AGE[k] < 24
         and (LR[k].get('m_g') or 0) > 0]
P('  %-18s %6s %12s %12s %12s %12s' % ('pick band', 'rows', 'chg ORDER K', 'chg ORDER P',
                                        'med s vs age', 'med s vs ped'))
BAL = {}
for b in ('1-10', '11-20', '21-40', '41-64 and pool'):
    sub = [k for k in young if band(LR[k].get('pick')) == b]
    if not sub: continue
    ck = sum(LR[k]['m_charge_k'] for k in sub) / len(sub)
    cp = sum(LR[k]['m_charge_p'] for k in sub) / len(sub)
    sn = sorted(LR[k]['m_sN'] for k in sub); sp = sorted(LR[k]['m_sP'] for k in sub)
    BAL[b] = dict(n=len(sub), chg_k=ck, chg_p=cp, med_sN=sn[len(sn) // 2], med_sP=sp[len(sp) // 2])
    P('  %-18s %6d %11.1f%% %11.1f%% %+12.2f %+12.2f'
      % (b, len(sub), 100 * ck, 100 * cp, sn[len(sn) // 2], sp[len(sp) // 2]))
OUT['bands_charge'] = BAL
P()

# ---- the named rows ------------------------------------------------------------------------------------
P('== THE NAMED ROWS, ON THE DECISION BOARD. CONSEQUENCES, NEVER TARGETS. ==')
P('  Not one constant in this build was chosen with any of these rows in view. The PREREG wrote down')
P('  a DIRECTION for each of them before the engine was touched; the direction is scored, the value')
P('  is not. No row\'s number is an acceptance criterion — that is a standing prohibition here.')
DIRS = [('harry-dean', 'up'), ('cooper-duff-tytler', 'up'), ('xavier-taylor', 'down'),
        ('daniel-annable', 'down'), ('dylan-patterson', 'down'), ('isaac-kako', 'down'),
        ('josh-smillie', 'flat'), ('milan-murdock', 'flat'), ('zeke-uwland', 'down'),
        ('cooper-harvey', 'up')]
P('  %-22s %4s %5s %5s %8s %8s %8s | %7s %7s | %7s %7s %7s %s'
  % ('row', 'age', 'pick', 'g', 'v0', 'premium', 's vs ped', 'chg K', 'chg P',
     'landing', 'ORDER K', 'ORDER P', 'prereg'))
nok = 0; nd = 0
for key, want in DIRS:
    r = LR.get(key)
    if r is None:
        P('  %-22s (not on the 804-row active board)' % key); continue
    got = 'up' if r['leg_p'] > 0 else ('down' if r['leg_p'] < 0 else 'flat')
    nd += 1; nok += (got == want)
    fm = lambda v, w, d: (('%%%d.%df' % (w, d)) % v) if v is not None else ' ' * (w - 1) + '-'
    P('  %-22s %4s %5s %5.0f %8s %8s %8s | %6s%% %6s%% | %7d %7d %7d %s %s'
      % (r['name'][:22], r['age'], r['pick'], r['m_g'] or 0, fm(r['m_v0'], 8, 0),
         fm(r['m_premium'], 8, 2), fm(r['m_sP'], 8, 2),
         fm(100 * r['m_charge_k'] if r['m_charge_k'] is not None else None, 6, 1),
         fm(100 * r['m_charge_p'] if r['m_charge_p'] is not None else None, 6, 1),
         r['landing'], r['orderk'], r['orderp'], want,
         'ok' if got == want else 'MISSED — got %s' % got))
P('  prereg named-row DIRECTION scorecard: %d of %d correct' % (nok, nd))
OUT['named'] = dict(n_ok=nok, n=nd)
P()

# ---- the year-1 class on the 2026 board ------------------------------------------------------------------
P('== THE YEAR-1 CLASS ON THE 2026 BOARD (board points) ==')
y1 = [k for k in KEYS if (LR.get(k) or {}).get('yr') == 2025]
a = sum(V['Kref'][k] for k in y1); b = sum(V['P'][k] for k in y1)
P('  %d rows, %d -> %d (%+.2f%%);  %d up, %d down, %d unchanged'
  % (len(y1), a, b, 100 * (b - a) / a if a else 0,
     sum(1 for k in y1 if V['P'][k] > V['Kref'][k]), sum(1 for k in y1 if V['P'][k] < V['Kref'][k]),
     sum(1 for k in y1 if V['P'][k] == V['Kref'][k])))
OUT['year1_board'] = dict(n=len(y1), orderk=a, orderp=b)
P()

# ---- totals ----------------------------------------------------------------------------------------------
P('== BOARD TOTALS ==')
for t in TAGS:
    P('  %-7s %-10s %8d' % (t, MD5[t][:8], sum(V[t].values())))
P('  ORDER P vs ORDER K: %+d points (%+.2f%%).  %d of %d rows move (%d up, %d down).'
  % (sum(V['P'].values()) - sum(V['Kref'].values()),
     100 * (sum(V['P'].values()) - sum(V['Kref'].values())) / sum(V['Kref'].values()),
     sum(1 for k in KEYS if V['P'][k] != V['Kref'][k]),
     len(KEYS), sum(1 for k in KEYS if V['P'][k] > V['Kref'][k]),
     sum(1 for k in KEYS if V['P'][k] < V['Kref'][k])))
OUT['totals'] = {t: sum(V[t].values()) for t in TAGS}
OUT['n_move'] = sum(1 for k in KEYS if V['P'][k] != V['Kref'][k])
OUT['n_up'] = sum(1 for k in KEYS if V['P'][k] > V['Kref'][k])
OUT['n_down'] = sum(1 for k in KEYS if V['P'][k] < V['Kref'][k])

json.dump(OUT, open(os.path.join(HERE, 'GATES_P.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'GATES_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote GATES_P.json and GATES_P_out.txt')
