#!/usr/bin/env python3
"""ORDER S READ-ONLY — T2. THE SELECTION HANDOFF AUDIT. NO BOARD IS BUILT. NOTHING IS ADOPTED.

Unplayed seasons are SILENT in the ORDER P charge's surplus s_P. Non-selection is priced only by the
sitter machinery. For rows WITH career games but NONE or almost none recent, this file traces BOTH
mechanisms end to end on the engine's own numbers and answers: is non-selection priced once, twice,
or not at all — and is the combined treatment coherent?

NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NO STORE IS WRITTEN. NO BOARD IS BUILT. The engine is
loaded in-process on the ORDER P built board's own dial line, thread-pinned, one run at a time, and
every quantity is READ out of the engine's own functions. Two counterfactuals wrap a function IN THE
LOADED NAMESPACE only, for one row at a time, and both are proved inert at their identity setting.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 os_handoff.py [TAG] [dial=value ...]
"""
import os, sys, io, json, math, contextlib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as SL                                                          # noqa: E402
import numpy as np                                                           # noqa: E402

TAG = sys.argv[1] if len(sys.argv) > 1 else 'P'
DIALS = dict(x.split('=', 1) for x in sys.argv[2:]) or dict(RL_O37='1')
Y = 2026
L = []


def P(s=''):
    print(s); L.append(str(s))


NS = SL.load(**DIALS)
NS['_REC'] = SL.install_recorder(NS)
MA = NS['_MA']
FNUM = json.load(open(SL.ROOT + '/engine/rl_after/pick_redenomination.json'))['factor']
EV = NS['ev']
PR = NS['PR']

with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        EV(p, Y)
ROWS = {p['key']: SL.assemble(NS, p, Y) for p in MA.players}
RAW = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        RAW[p['key']] = EV(p, Y)
BOARD = {k: int(round(RAW[k] / FNUM)) for k in RAW}

P('=' * 118)
P('ORDER S READ-ONLY — T2. THE SELECTION HANDOFF AUDIT. IS NON-SELECTION PRICED ONCE, TWICE, OR NOT AT ALL?')
P('=' * 118)
P('NO BOARD IS BUILT. NO ENGINE FILE IS EDITED. NO DIAL IS ADDED. NOTHING IS ADOPTED.')
P('dial line : %s  (plus ORDER K\'s ruled RL_O36_* setting, register v735)' % DIALS)
P('as-of year: %d   ·   board redenomination factor %.4f' % (Y, FNUM))
P('board total (numeraire): %d over %d rows' % (sum(BOARD.values()), len(BOARD)))
P()

# ---- 0 · the identity, asserted rather than assumed ----------------------------------------------------
errs = []
chain = 0.0
for p in MA.players:
    r = ROWS[p['key']]
    if r is None or r.get('price') is None:
        continue
    errs.append(abs(r['price'] - RAW[p['key']]))
    chain = max(chain, r['D_chain_err'])
P('-' * 118)
P('0 · THE DECOMPOSITION IS THE ENGINE\'S OWN, AND IT IS ASSERTED')
P('-' * 118)
P('   price = rho31(g)*e + pi*ped + o32_age_credit,  pi = pi_base * f,')
P('   pi_base = D_final*(1-rho) + Phi(g,s)*beta(g)*rho,  D_final = min(1, D_raw**kappa * (1+1.08*sigma)).')
P()
P('   reassembled price vs the engine\'s own ev(): worst error %.3g over %d rows with a pedigree leg'
  % (max(errs), len(errs)))
P('   the recomputed fade chain vs the engine\'s own o31_D(): worst error %.3g' % chain)
assert max(errs) < 1e-6, 'SRO-T1 FIRED: the price identity does not hold (worst %.3g)' % max(errs)
assert chain < 1e-12, 'SRO-T2 FIRED: the recomputed fade chain is not o31_D (worst %.3g)' % chain
P('   Falsifiers SRO-T1 and SRO-T2 did not fire. Tolerances were declared in the prereg at 1e-6.')
P()

# ---- 1 · the staleness census -------------------------------------------------------------------------
GY = {}
for p in MA.players:
    d = collections.defaultdict(float)
    for x in (p.get('scoring') or []):
        if x['year'] <= Y and x.get('games'):
            d[int(x['year'])] += float(x['games'])
    GY[p['key']] = d


def win(p, k):
    """Games in the last k seasons counting back from Y inclusive."""
    return sum(GY[p['key']].get(Y - i, 0.0) for i in range(k))


POP = [p for p in MA.players
       if ROWS[p['key']] is not None and ROWS[p['key']].get('price') is not None]
CAREER = {p['key']: NS['pv_games'](p, Y) for p in POP}
AGE = {p['key']: (Y - int(p['_by'])) if p.get('_by') else None for p in POP}


def ageband(a):
    if a is None: return 'no dob'
    if a <= 20: return '<=20'
    if a <= 23: return '21-23'
    if a <= 26: return '24-26'
    return '27+'


P('-' * 118)
P('1 · (a) THE BOARD POPULATION BY STALENESS')
P('-' * 118)
P('   Priced rows carrying a pedigree leg at %d: %d.' % (Y, len(POP)))
P('   A row is STALE(k) when he has career games but ZERO games in the last k seasons counting back')
P('   from %d inclusive. "Almost none" is 2 or fewer games in the window, reported separately and' % Y)
P('   never merged with the zero cell.')
P()
CENS = {}
for k in (1, 2, 3):
    z = [p for p in POP if CAREER[p['key']] > 0 and win(p, k) == 0]
    a = [p for p in POP if CAREER[p['key']] > 0 and 0 < win(p, k) <= 2]
    CENS[k] = dict(zero=len(z), almost=len(a))
    P('   last %d season(s): career games > 0 and ZERO in window: %4d rows   ·   1-2 games in window: %4d rows'
      % (k, len(z), len(a)))
P('   career games == 0 (never played at all): %d rows — NOT this task\'s population, listed for completeness.'
  % sum(1 for p in POP if CAREER[p['key']] <= 0))
P()
P('   THE STALE(1) POPULATION — zero games in %d — BY AGE BAND AND CLASS:' % Y)
P('   %-10s %8s %8s %10s %10s %10s' % ('age band', 'TALL', 'SMALL', 'total', 'med career g', 'med board'))
STALE = {k: [p for p in POP if CAREER[p['key']] > 0 and win(p, k) == 0] for k in (1, 2, 3)}
BYBAND = {}
for b in ('<=20', '21-23', '24-26', '27+', 'no dob'):
    s = [p for p in STALE[1] if ageband(AGE[p['key']]) == b]
    if not s:
        continue
    t = sum(1 for p in s if ROWS[p['key']]['tall'])
    BYBAND[b] = dict(n=len(s), tall=t, small=len(s) - t,
                     med_g=float(np.median([CAREER[p['key']] for p in s])),
                     med_board=float(np.median([BOARD[p['key']] for p in s])))
    P('   %-10s %8d %8d %10d %10.1f %10.0f'
      % (b, t, len(s) - t, len(s), BYBAND[b]['med_g'], BYBAND[b]['med_board']))
P()
P('   THE SAME, BY CAREER GAMES — because the charge reads career games and nothing else:')
P('   %-14s %8s %8s %8s | %-40s' % ('career games', 'stale1', 'stale2', 'stale3', 'A(g) at the band midpoint'))
GB = [(0.001, 3), (3, 10), (10, 25), (25, 60), (60, 150), (150, 1e9)]
CAREERJ = {}
for lo, hi in GB:
    lab = ('%d-%d' % (math.ceil(lo), hi)) if hi < 1e9 else '150+'
    ns = [sum(1 for p in STALE[k] if lo <= CAREER[p['key']] < hi) for k in (1, 2, 3)]
    mid = min(hi, 200) if hi < 1e9 else 200
    A = 1.0 - math.exp(-((lo + mid) / 2) / NS['O37_G0'])
    CAREERJ[lab] = dict(n=ns, A=A)
    P('   %-14s %8d %8d %8d | A = %.3f' % (lab, ns[0], ns[1], ns[2], A))
P()

# ---- 2 · the legs, per staleness class ----------------------------------------------------------------
P('-' * 118)
P('2 · (b) THE LEGS, READ OUT OF THE ENGINE — HOW MUCH OF EACH ROW\'S PRICE EACH MECHANISM MOVED')
P('-' * 118)
P('   All figures in BOARD POINTS (engine currency / %.4f). Positive = the mechanism REMOVED that many' % FNUM)
P('   points from the row; negative = it gave points back.')
P()


def bp(x):
    return x / FNUM


def evidence_age(p):
    """The games-weighted mean age, in seasons, of the evidence s_P actually reads. The charge
    weights every one of these seasons exactly the same, however old it is."""
    num = den = 0.0
    for x in (p.get('scoring') or []):
        if x['year'] > Y or not x.get('games'):
            continue
        g = float(x['games'])
        num += g * (Y - int(x['year']))
        den += g
    return (num / den) if den > 0 else None


def legrow(p):
    r = ROWS[p['key']]
    return dict(key=p['key'], name=p.get('player'), pos=MA.gfut(p), tall=r['tall'],
                evage=evidence_age(p),
                pick=p.get('pick'), pool=r['pool'], typ=p.get('type'),
                age=AGE[p['key']], g=CAREER[p['key']],
                w1=win(p, 1), w2=win(p, 2), w3=win(p, 3),
                board=BOARD[p['key']], v0=NS['day0_v0'](p), ped=r['ped'],
                cu=r['cu'], clock=r['clock'], units=r['units'], sigma=r['sigma'],
                D_raw=r['D_raw'], D_kap=r['D_kap'], D_final=r['D_final'], D_noTS=r['D_noTS'],
                kap=r['kap'], kap_noTS=r['kap_noTS'], effpk=r['effpk'],
                rho=r['rho'], srun=r['srun'], phi=r['phi'], f=r['f_eff'], f_K=r['f_K_eff'],
                s_P=r['s_P'], A=r['A'], T=r['T'],
                a_charge=bp(r['a_charge']), a_fade=bp(r['a_fade_total']),
                a_sched=bp(r['a_fade_schedule']), a_kappa=bp(r['a_fade_kappa']),
                a_relief=bp(r['a_fade_relief']), a_tall=bp(r['a_tall_saved']),
                a_evid=bp(r['a_evidence_saved']), prod=bp(r['prod_leg']),
                pedleg=bp(r['ped_leg']), credit=bp(r['credit']))


LR = {p['key']: legrow(p) for p in POP}
FRESH = [p for p in POP if CAREER[p['key']] > 0 and win(p, 1) > 0]


def summ(name, rows):
    if not rows:
        P('   %-26s %5d   (empty)' % (name, 0)); return None
    q = lambda f: float(np.median([f(LR[p['key']]) for p in rows]))
    s = lambda f: float(np.sum([f(LR[p['key']]) for p in rows]))
    o = dict(n=len(rows), med_g=q(lambda r: r['g']), med_cu=q(lambda r: r['cu']),
             med_D=q(lambda r: r['D_final']), med_f=q(lambda r: r['f']),
             med_rho=q(lambda r: r['rho']), med_board=q(lambda r: r['board']),
             tot_charge=s(lambda r: r['a_charge']), tot_fade=s(lambda r: r['a_fade']),
             med_charge=q(lambda r: r['a_charge']), med_fade=q(lambda r: r['a_fade']),
             tot_kappa=s(lambda r: r['a_kappa']), tot_relief=s(lambda r: r['a_relief']),
             tot_tall=s(lambda r: r['a_tall']))
    P('   %-26s %5d %7.1f %7.2f %7.3f %7.3f %7.3f | %9.0f %9.0f | %8.1f %8.1f'
      % (name, o['n'], o['med_g'], o['med_cu'], o['med_D'], o['med_f'], o['med_rho'],
         o['tot_charge'], o['tot_fade'], o['med_charge'], o['med_fade']))
    return o


P('   %-26s %5s %7s %7s %7s %7s %7s | %9s %9s | %8s %8s'
  % ('group', 'n', 'med g', 'med c_u', 'med D', 'med f', 'med rho', 'CHARGE', 'FADE', 'med chg', 'med fade'))
P('   %-26s %5s %7s %7s %7s %7s %7s | %19s | %17s'
  % ('', '', '', '', '', '', '', 'total board points', 'per row, median'))
SUMJ = {}
SUMJ['fresh'] = summ('FRESH (played in %d)' % Y, FRESH)
for k in (1, 2, 3):
    SUMJ['stale%d' % k] = summ('STALE(%d) zero in window' % k, STALE[k])
for b in ('<=20', '21-23', '24-26', '27+'):
    SUMJ['stale1_' + b] = summ('  stale(1), age %s' % b, [p for p in STALE[1] if ageband(AGE[p['key']]) == b])
SUMJ['stale1_tall'] = summ('  stale(1), TALL', [p for p in STALE[1] if LR[p['key']]['tall']])
SUMJ['stale1_small'] = summ('  stale(1), SMALL', [p for p in STALE[1] if not LR[p['key']]['tall']])
P()
P('   READ THE CHARGE COLUMN AGAINST THE FADE COLUMN. The charge is the ORDER P pedigree charge; the')
P('   fade is the sitter machinery. A mechanism that prices staleness has to show a DIFFERENCE between')
P('   the fresh row and the stale row.')
P()

# ---- 3 · is the charge reading staleness at all? -------------------------------------------------------
P('-' * 118)
P('3 · IS THE CHARGE READING STALENESS AT ALL? (prereg SRO-5)')
P('-' * 118)
P('   The charge is exp(-LAMBDA*A(g)*T(s_P)). A(g) reads CAREER games. s_P is the games-weighted mean')
P('   over PLAYED seasons. Neither carries a date. So the prediction is: at the same career games and')
P('   the same age, a stale row and a fresh row pay the SAME charge unless their production differed.')
P()
P('   %-14s %6s %8s %8s %8s | %6s %8s %8s %8s' %
  ('career games', 'n frsh', 'med f', 'med A', 'med s_P', 'n stale', 'med f', 'med A', 'med s_P'))
CHGCMP = {}
for lo, hi in GB:
    lab = ('%d-%d' % (math.ceil(lo), hi)) if hi < 1e9 else '150+'
    fr = [LR[p['key']] for p in FRESH if lo <= CAREER[p['key']] < hi]
    st = [LR[p['key']] for p in STALE[1] if lo <= CAREER[p['key']] < hi]
    if not fr and not st:
        continue

    def m(rows, f):
        v = [f(r) for r in rows if f(r) is not None]
        return float(np.median(v)) if v else float('nan')
    CHGCMP[lab] = dict(n_fresh=len(fr), n_stale=len(st),
                       f_fresh=m(fr, lambda r: r['f']), f_stale=m(st, lambda r: r['f']),
                       sP_fresh=m(fr, lambda r: r['s_P']), sP_stale=m(st, lambda r: r['s_P']))
    P('   %-14s %6d %8.4f %8.4f %8.2f | %6d %8.4f %8.4f %8.2f'
      % (lab, len(fr), m(fr, lambda r: r['f']), m(fr, lambda r: r['A']), m(fr, lambda r: r['s_P']),
         len(st), m(st, lambda r: r['f']), m(st, lambda r: r['A']), m(st, lambda r: r['s_P'])))
P()
P('   HOW OLD IS THE EVIDENCE THE CHARGE READS? The games-weighted mean age, in seasons, of the')
P('   seasons that enter s_P. The charge weights every one of them exactly the same, whatever its age.')
P()
P('   %-30s %6s %14s %14s' % ('group', 'n', 'med evidence', 'p90 evidence'))
P('   %-30s %6s %14s %14s' % ('', '', 'age, seasons', 'age, seasons'))
EVAGE = {}
for lab, sel in (('FRESH (played in %d)' % Y, FRESH), ('STALE(1)', STALE[1]),
                 ('STALE(2)', STALE[2]), ('STALE(3)', STALE[3]),
                 ('stale(1), career games <= 25', [p for p in STALE[1] if CAREER[p['key']] <= 25])):
    v = [LR[p['key']]['evage'] for p in sel if LR[p['key']]['evage'] is not None]
    if not v:
        continue
    EVAGE[lab] = dict(n=len(v), med=float(np.median(v)), p90=float(np.percentile(v, 90)))
    P('   %-30s %6d %14.2f %14.2f' % (lab, len(v), np.median(v), np.percentile(v, 90)))
P()

# ---- 3b · every stale row, leg by leg ------------------------------------------------------------------
P('-' * 118)
P('3b · EVERY STALE(1) ROW, LEG BY LEG. THE WHOLE POPULATION, NOT A SELECTION.')
P('-' * 118)
P('   c_u is the unplayed clock. D is the fade the pedigree leg carries. f is the ORDER P charge')
P('   factor. Every attribution is in board points: CHARGE and FADE are points REMOVED, EVID and')
P('   TALL are points KEPT ON the row by the evidence weight and by the tall/small sitter factor.')
P()
P('   %-22s %4s %3s %6s %5s %5s %6s %6s %6s %7s | %7s %7s %6s %6s %7s'
  % ('row', 'pos', 'age', 'g', 'pick', 'evage', 'c_u', 'D', 'f', 's_P', 'CHARGE', 'FADE', 'EVID', 'TALL', 'board'))
for p in sorted(STALE[1], key=lambda z: -BOARD[z['key']]):
    r = LR[p['key']]
    P('   %-22s %4s %3s %6.1f %5s %5.2f %6.2f %6.3f %6.3f %7s | %7.1f %7.1f %6.1f %6.1f %7d'
      % (r['name'][:22], r['pos'], (r['age'] if r['age'] is not None else '-'), r['g'],
         (r['pick'] if not r['pool'] else 'pool'), (r['evage'] or 0.0), r['cu'], r['D_final'], r['f'],
         ('%.1f' % r['s_P']) if r['s_P'] is not None else 'n/a',
         r['a_charge'], r['a_fade'], r['a_evid'], r['a_tall'], r['board']))
P()

# ---- 4 · matched pairs ---------------------------------------------------------------------------------
P('-' * 118)
P('4 · (c) MATCHED PAIRS — A STALE ROW AGAINST A FRESH ROW AT THE SAME GAMES, AGE, CLASS AND PATHWAY')
P('-' * 118)
P('   The match rule was written in the prereg before it was run: same class, |career games| <= 3')
P('   apart, |age| <= 1 apart, same pathway (ND / pool). Where several fresh rows match, the closest')
P('   on games then on age is taken. NO named row gates anything; the pairs are whatever the rule finds.')
P()
def make_pairs(price_band=None):
    out = []
    for p in STALE[1]:
        rs = LR[p['key']]
        if rs['age'] is None or not rs['v0']:
            continue
        cand = []
        for q in FRESH:
            rf = LR[q['key']]
            if rf['age'] is None or rf['tall'] != rs['tall'] or rf['pool'] != rs['pool'] or not rf['v0']:
                continue
            if abs(rf['g'] - rs['g']) > 3 or abs(rf['age'] - rs['age']) > 1:
                continue
            if price_band is not None and abs(math.log(rf['v0'] / rs['v0'])) > price_band:
                continue
            cand.append((abs(rf['g'] - rs['g']), abs(rf['age'] - rs['age']), q['key']))
        if cand:
            cand.sort()
            out.append((p['key'], cand[0][2]))
    return out


PAIRS = make_pairs(None)
PAIRS_PRICED = make_pairs(0.35)
P('   matched pairs found: %d of %d stale(1) rows' % (len(PAIRS), len(STALE[1])))
P('   DECLARED ADDITION, not in the prereg: the loose rule does NOT match on entry price, so a stale')
P('   row can be paired with a fresh row ten times his price and the retention comparison is then')
P('   about the price, not the staleness. A SECOND, PRICE-MATCHED set is therefore also run — same')
P('   rule plus |ln(v0 ratio)| <= 0.35 (within about 35%% on price). It found %d pairs. BOTH are'
  % len(PAIRS_PRICED))
P('   printed and the prereg rule stays the primary one.')
PAIRJ = {}


def retention(r):
    return (r['board'] / (r['v0'] or 1.0)) if r['v0'] else float('nan')


for nm, PP in (('the prereg rule (no price match)', PAIRS), ('price-matched, within 35%', PAIRS_PRICED)):
    if not PP:
        continue

    def dif(f, PP=PP):
        return float(np.median([f(LR[a]) - f(LR[b]) for a, b in PP]))
    P()
    P('   MEDIAN DIFFERENCE, stale MINUS fresh — %s, n = %d:' % (nm, len(PP)))
    d = {}
    for lab, fn, fmt in (('charge factor f', lambda r: r['f'], '%+10.4f'),
                         ('fade D_final', lambda r: r['D_final'], '%+10.4f'),
                         ('unplayed clock c_u', lambda r: r['cu'], '%+10.4f'),
                         ('rho31(g)', lambda r: r['rho'], '%+10.4f'),
                         ('sigma_sel (selection relief)', lambda r: r['sigma'], '%+10.4f'),
                         ('charge attribution, board points', lambda r: r['a_charge'], '%+10.1f'),
                         ('fade attribution, board points', lambda r: r['a_fade'], '%+10.1f'),
                         ('price / entry price (retention)', retention, '%+10.4f')):
        v = dif(fn)
        d[lab] = v
        P(('     %-34s ' + fmt) % (lab, v))
    PAIRJ[nm] = dict(n=len(PP), diff=d)
P()
P('   THE TEN LARGEST PRICE-MATCHED PAIRS BY THE STALE ROW\'S BOARD PRICE:')
P('   %-20s %4s %5s %6s %6s %6s %6s %6s | %-20s %4s %5s %6s %6s %6s %6s %6s'
  % ('STALE row', 'age', 'g', 'v0', 'f', 'D', 'c_u', 'board',
     'FRESH match', 'age', 'g', 'v0', 'f', 'D', 'c_u', 'board'))
for a, b in sorted(PAIRS_PRICED, key=lambda z: -LR[z[0]]['board'])[:10]:
    ra, rb = LR[a], LR[b]
    P('   %-20s %4d %5.0f %6.0f %6.3f %6.3f %6.2f %6d | %-20s %4d %5.0f %6.0f %6.3f %6.3f %6.2f %6d'
      % (ra['name'][:20], ra['age'], ra['g'], ra['v0'], ra['f'], ra['D_final'], ra['cu'], ra['board'],
         rb['name'][:20], rb['age'], rb['g'], rb['v0'], rb['f'], rb['D_final'], rb['cu'], rb['board']))
P()

# ---- 5 · the tall/small interaction --------------------------------------------------------------------
P('-' * 118)
P('5 · (d) THE TALL/SMALL INTERACTION — THE EVIDENCE WEIGHT AGAINST THE GENTLER TALL SITTER FADE')
P('-' * 118)
P('   Two separate things keep value on a stale TALL row with almost no games:')
P('     (i)  the EVIDENCE WEIGHT A(g) = 1 - exp(-g/%.2f). At 2 games A = %.4f, so at most %.1f%% of the'
  % (NS['O37_G0'], 1 - math.exp(-2 / NS['O37_G0']), 100 * (1 - math.exp(-2 / NS['O37_G0']))))
P('          charge the same surplus would carry at full evidence can reach him.')
P('     (ii) the OWNER-RULED TALL/SMALL sitter factor, which fades a tall\'s sitting years more gently')
P('          than a small\'s at the same pick. Counterfactual: the same row on ORDER D\'s POOLED')
P('          exponent, which is exactly what RL_O36_TALL=0 falls back to.')
P()
P('   %-24s %5s %9s %9s %11s %11s %11s'
  % ('group', 'n', 'med g', 'med A', 'EVIDENCE', 'TALL FACTOR', 'which is bigger'))
P('   %-24s %5s %9s %9s %11s %11s %11s'
  % ('', '', '', '', 'kept, bp', 'kept, bp', ''))
TSJ = {}
for lab, sel in (('stale(1) TALL, g <= 5', [p for p in STALE[1] if LR[p['key']]['tall'] and 0 < CAREER[p['key']] <= 5]),
                 ('stale(1) TALL, g 6-20', [p for p in STALE[1] if LR[p['key']]['tall'] and 5 < CAREER[p['key']] <= 20]),
                 ('stale(1) TALL, all', [p for p in STALE[1] if LR[p['key']]['tall']]),
                 ('stale(1) SMALL, g <= 5', [p for p in STALE[1] if not LR[p['key']]['tall'] and 0 < CAREER[p['key']] <= 5]),
                 ('stale(1) SMALL, all', [p for p in STALE[1] if not LR[p['key']]['tall']])):
    if not sel:
        P('   %-24s %5d   (empty)' % (lab, 0)); continue
    ev_ = float(np.median([LR[p['key']]['a_evid'] for p in sel]))
    tf = float(np.median([LR[p['key']]['a_tall'] for p in sel]))
    TSJ[lab] = dict(n=len(sel), evid=ev_, tall=tf,
                    med_g=float(np.median([CAREER[p['key']] for p in sel])))
    P('   %-24s %5d %9.1f %9.4f %11.1f %11.1f %11s'
      % (lab, len(sel), np.median([CAREER[p['key']] for p in sel]),
         np.median([LR[p['key']]['A'] for p in sel if LR[p['key']]['A'] is not None] or [float('nan')]),
         ev_, tf, 'EVIDENCE' if abs(ev_) > abs(tf) else 'TALL FACTOR'))
P()
P('   BOTH COLUMNS ARE "BOARD POINTS KEPT ON THE ROW". EVIDENCE is what A(g) < 1 kept against the')
P('   same surplus at full evidence. TALL FACTOR is what the tall/small exponent kept relative to')
P('   ORDER D\'s pooled exponent. A NEGATIVE tall-factor number means the factor COST that group')
P('   value, which is ORDER I\'s own disclosed side effect: the identity is pinned, so late small')
P('   sitters pay for the talls\' relief.')
P()
P('   THE ROW THE ORDER USED TO ILLUSTRATE THE SHAPE, printed wherever the mechanism puts it:')
for nm in ('harry-barnett', 'toby-conway'):
    if nm in LR:
        r = LR[nm]
        P('     %-18s %-5s age %s %4.0f games  s_P %6.1f  charge factor %.3f  fade D %.3f'
          % (r['name'], r['pos'], r['age'], r['g'], (r['s_P'] if r['s_P'] is not None else float('nan')),
             r['f'], r['D_final']))
        P('       %-30s %8.1f board points' % ('the charge REMOVED', r['a_charge']))
        P('       %-30s %8.1f board points' % ('the sitter fade REMOVED', r['a_fade']))
        P('       %-30s %8.1f board points' % ('the evidence weight A(g) KEPT', r['a_evid']))
        P('       %-30s %8.1f board points' % ('the tall/small factor KEPT', r['a_tall']))
        P('       %-30s %8d board points' % ('board price', r['board']))
        if abs(r['a_tall']) > 1e-9:
            P('       the evidence weight is %.1f times the tall factor on this row.'
              % (abs(r['a_evid']) / abs(r['a_tall'])))
P()

# ---- 6 · the other staleness channels ------------------------------------------------------------------
P('-' * 118)
P('6 · THE STALENESS CHANNELS OUTSIDE THE FOUR NAMED LEGS (prereg SRO-9)')
P('-' * 118)
P('   Reading ev() finds three more objects that react to a season not played. They are not part of')
P('   the charge and not part of the fade, and they sit on the PRODUCTION leg or on the whole row.')
P()
P('     A. THE D8 GRADED STALENESS CAP.  el >= onset and ns <= 1  =>  e capped at v0_start*frac, with')
P('        a graded release. onset is 4 for KPD/KPF/RUCK and 3 otherwise.')
P('     B. THE MEDIOCRE-FOR-YEARS DECAY GATE.  el >= onset+2 and bestlvl/par < 0.55  =>  e capped at')
P('        v0_start*frac. No grading — a hard min.')
P('     C. THE ITEM H SITTER CUTS.  a POOL row with no games this year takes H_POOLSIT, and the named')
P('        union subset takes H_UNION on top. This one reads "did not play this year" DIRECTLY.')
P()
CH = {}
nA = nB = nC = nSit = 0
BOTH = []
for p in POP:
    r = LR[p['key']]
    with NS['_form_anchor_clock']():
        el = PR.tenure(p, NS['_fa_year'](Y))
    ns = NS['nseas_pro'](p, Y)
    pos = MA.gfut(p)
    v0s = NS['v0_start'](p)
    onset = 4 if pos in ('KPF', 'KPD', 'RUCK') else 3
    par = (NS['_o34_par'](pos, p, Y) if NS.get('_O34') else NS['_O30BP_BARS'][pos]) \
        if NS['_O30B_PREVIEW'] else None
    pr = NS['bestlvl'](p, Y) / max(1, par) if par else None
    a = b = False
    capA = capB = None
    if ns == 0:
        nSit += 1
    elif el >= onset and ns <= 1:
        a = True
        capA = v0s * (0.25 * max(0.4, 1 - 0.10 * (el - onset)) * (1.6 if onset == 4 else 1.0))
    elif el >= onset + 2 and pr is not None and pr < 0.55:
        b = True
        capB = v0s * (0.45 * max(0.3, 1 - 0.08 * (el - onset)) * (1.5 if onset == 4 else 1.0))
    h = NS['_h_cut'](p, Y)
    c = (h < 1.0 - 1e-12)
    if a: nA += 1
    if b: nB += 1
    if c: nC += 1
    r['ch_A'] = a; r['ch_B'] = b; r['ch_H'] = h; r['ch_sit'] = (ns == 0)
    r['el'] = el; r['ns'] = ns; r['pr'] = pr; r['capA'] = capA; r['capB'] = capB
    if (a or b or c) and r['D_final'] < 1.0 - 1e-12 and r['g'] > 0:
        BOTH.append(p['key'])
P('   %-46s %8s' % ('channel', 'rows'))
P('   %-46s %8d' % ('A · D8 graded staleness predicate TRUE', nA))
P('   %-46s %8d' % ('B · mediocre-for-years predicate TRUE', nB))
P('   %-46s %8d' % ('C · ITEM H sitter cut < 1.0', nC))
P('   %-46s %8d' % ('the ns==0 sit-out arm (a different price path)', nSit))
P('   %-46s %8d' % ('ANY of A/B/C *and* the sitter fade D < 1', len(BOTH)))
CH = dict(A=nA, B=nB, C=nC, sitout=nSit, both=len(BOTH))
P()
P('   ITEM H is %s on this dial line (H_ON = %r), which is why column C reads as it does.'
  % ('LIVE' if NS.get('H_ON') else 'OFF', NS.get('H_ON')))
P()
P('   A PREDICATE BEING TRUE IS NOT THE SAME AS A CAP BINDING. The counterfactual below settles it.')
P('   The %d figure above is the predicate; the binding count is measured next and it is smaller.'
  % len(BOTH))
P()
P('   THE DEFINITION OF DOUBLE-PRICING, fixed in the prereg: ONE fact — a season not played —')
P('   reducing TWO legs that are ADDED TOGETHER in the price identity.')
P()

# ---- 6b · the D8 counterfactual, proved inert -----------------------------------------------------------
P('   THE D8 ARM, PRICED BY A COUNTERFACTUAL THAT IS EXACTLY INERT WHEN IT DOES NOT BIND.')
P('   The arm is  e = min(e, cap + gr*max(0, e - cap)).  At gr = 1 that is min(e, e) = e, identically.')
P('   So wrapping the engine\'s own _staleness_grade to return 1.0 removes the arm and nothing else.')
P('   The wrapper lives in the loaded namespace. NO REPOSITORY FILE IS TOUCHED.')
g0 = NS['_staleness_grade']
NS['_staleness_grade'] = lambda p, Yv, pos, _o=g0: 1.0
RAW2 = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        NS['_O37_SCACHE'].clear()
        RAW2[p['key']] = EV(p, Y)
NS['_staleness_grade'] = g0
NS['_O37_SCACHE'].clear()
d8 = [(p['key'], int(round(RAW2[p['key']] / FNUM)) - BOARD[p['key']]) for p in POP]
d8m = [z for z in d8 if z[1] != 0]
TOTD8 = sum(z[1] for z in d8m)
P()
P('   rows the D8 arm moves: %d   ·   board points it REMOVES in total: %d   ·   worst single row: %d'
  % (len(d8m), TOTD8, max([z[1] for z in d8m] or [0])))
D8ROWS = []
if d8m:
    P('   the five it costs most:')
    for k, v in sorted(d8m, key=lambda z: -z[1])[:5]:
        r = LR[k]
        D8ROWS.append(dict(key=k, name=r['name'], cost=v, board=BOARD[k], nocap=BOARD[k] + v,
                           D=r['D_final'], cu=r['cu'], g=r['g'], age=r['age']))
        P('     %-24s %-5s age %s %5.0fg  c_u %5.2f  fade D %.3f  board %5d  with the D8 arm removed %5d  (it costs him %d)'
          % (r['name'][:24], (r['pick'] if not r['pool'] else 'pool'), r['age'], r['g'], r['cu'],
             r['D_final'], BOARD[k], BOARD[k] + v, v))
P()
P('   OF THOSE %d ROWS, HOW MANY ALSO CARRY A SITTER FADE BELOW 1? — that is the double-price count'
  % len(d8m))
dbl = [k for k, v in d8m if LR[k]['D_final'] < 1.0 - 1e-12]
P('   %d of %d. Their names and both legs:' % (len(dbl), len(d8m)))
for k in sorted(dbl, key=lambda z: -LR[z]['board'])[:8]:
    r = LR[k]
    cost = dict(d8m)[k]
    P('     %-24s g %4.0f  c_u %5.2f  fade D %.3f (removes %6.1f bp)  D8 cap (removes %4d bp)  board %5d'
      % (r['name'][:24], r['g'], r['cu'], r['D_final'], r['a_fade'], cost, r['board']))
D8J = dict(n_moved=len(d8m), points=TOTD8, worst=max([z[1] for z in d8m] or [0]),
           n_double=len(dbl), rows=D8ROWS)
P()

# ---- 7 · where staleness goes UNPRICED ------------------------------------------------------------------
P('-' * 118)
P('7 · WHERE STALENESS GOES UNPRICED (prereg SRO-6 and SRO-7)')
P('-' * 118)
P('   SRO-6 — the fade schedule is 1.0 at every unplayed depth c_u <= 1. A row who played last season')
P('   and nothing this one sits at c_u under 1 and carries NO fade, while the charge is silent on the')
P('   unplayed season because s_P reads played seasons only. For that row the missing season costs')
P('   nothing anywhere in the price.')
P()
UNP = [p for p in STALE[1] if LR[p['key']]['D_final'] >= 1.0 - 1e-12]
P('   stale(1) rows carrying D_final == 1 (no fade at all): %d of %d' % (len(UNP), len(STALE[1])))
if UNP:
    P('   %-24s %5s %6s %7s %7s %7s %8s' % ('row', 'age', 'g', 'c_u', 'clock', 'units', 'board'))
    for p in sorted(UNP, key=lambda z: -BOARD[z['key']])[:10]:
        r = LR[p['key']]
        P('   %-24s %5s %6.0f %7.2f %7.2f %7.2f %8d'
          % (r['name'][:24], r['age'], r['g'], r['cu'], r['clock'], r['units'], r['board']))
P()
P('   SRO-7 — o31_played_units credits min(1, games/2) per season, so a TWO-GAME season cancels a FULL')
P('   season of sitter clock. The credit a season buys is capped at 1 and reached at 2 games.')
P()
TOK = []
TOKREC = []
for p in POP:
    if CAREER[p['key']] <= 0:
        continue
    tok = [(yy, gg) for yy, gg in GY[p['key']].items() if 0 < gg <= 2 and yy <= Y]
    if not tok:
        continue
    TOK.append(p['key'])
    if any(yy >= Y - 3 for yy, gg in tok):     # inside the window the fade clock is still counting
        TOKREC.append((p['key'], sorted(tok)[-1]))
P('   board rows with at least one season of 1-2 games: %d  (a 2-game season buys the full 1.00 unit;' % len(TOK))
P('   a 1-game season buys 0.50, because the credit is min(1, g/2))')
P('   of those, rows whose token season falls inside the last four seasons — where the credit is')
P('   still holding the sitter clock down: %d' % len(TOKREC))
stset = set(x['key'] for x in STALE[1])
tokstale = [k for k, t in TOKREC if k in stset]
P('   of THOSE, stale(1): %d' % len(tokstale))
if TOKREC:
    P('   the eight with the most unplayed time behind them:')
    P('   %-22s %6s %5s %7s %7s %7s %6s %7s'
      % ('row', 'token', 'year', 'clock', 'units', 'c_u', 'D', 'board'))
    for k, (yy, gg) in sorted(TOKREC, key=lambda z: -(LR[z[0]]['clock'] - LR[z[0]]['units']))[:8]:
        r = LR[k]
        P('   %-22s %6.1f %5d %7.2f %7.2f %7.2f %6.3f %7d'
          % (r['name'][:22], gg, yy, r['clock'], r['units'], r['cu'], r['D_final'], r['board']))
P()
P('   Read the units column against the clock. A season of two games advances "played units" by a')
P('   full 1.00, the same credit a twenty-two game season buys, and c_u is clock minus units. So two')
P('   games and a full season are the same object to the sitter fade.')
P()

json.dump(dict(tag=TAG, dials=DIALS, board_total=sum(BOARD.values()), n_rows=len(POP),
               census=CENS, byband=BYBAND, career=CAREERJ, summ=SUMJ, chgcmp=CHGCMP,
               evage=EVAGE, channels=CH, d8=D8J, n_pairs=len(PAIRS), pairs=PAIRJ,
               unpriced=len(UNP), token=len(TOK), token_recent=len(TOKREC), token_stale=len(tokstale),
               rows={p['key']: {kk: (None if isinstance(vv, float) and math.isnan(vv) else vv)
                                for kk, vv in LR[p['key']].items()} for p in STALE[1]}),
          open(os.path.join(HERE, 'HANDOFF_%s.json' % TAG), 'w'), indent=1, default=str)
open(os.path.join(HERE, 'HANDOFF_%s_out.txt' % TAG), 'w').write('\n'.join(L) + '\n')
print('\nwrote HANDOFF_%s.json and HANDOFF_%s_out.txt' % (TAG, TAG))
