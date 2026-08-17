#!/usr/bin/env python3
"""ORDER J — THE OWNER-RULED TALL/SMALL SITTER FACTOR: WIRED, VERIFIED, AND DISCLOSED IN FULL.

R-TALLFACTOR is ADOPTED (owner, issue #334 comment 5320813582). It is therefore EXEMPT from J-TOL and
from the zero-tolerance test. Exempt does not mean unexamined. PREREG_J §2.3 owes the owner five
things and this file produces all five:

  1. the redistribution identity residual, rebuilt from Order H's OWN fitted sitter population;
  2. the transcribed curve re-checked against H_RESULTS.json at every pick H published;
  3. m_TALL, the multiplicative translation the owner asked about;
  4. the FULL moved-row list for every active row aged 24+, with age, pick, value and move;
  5. the day-0 disclosure: derived_v0 bit-identical on 89 of 89, and the printed day-0 movement of
     every wired sitter with its extremes named.

Nothing here is gated. Everything here is printed.
"""
import os, sys, json, io, contextlib, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
H = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'order_h_posfade_2026-08-17', 'H_RESULTS.json')))
HA = H['adjustment_TALL_single_factor']

# ---- the wired constants, read from the engine source so a drift cannot hide -----------------------
SRC = open(os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py')).read()
def wired(name):
    i = SRC.index('\n    %s=' % name)
    return float(SRC[i:].split('=', 1)[1].split('#')[0].split('\n')[0].strip())
TG0, TG1, HT, SN, D2W = (wired('O36_TG0'), wired('O36_TG1'), wired('O36_HTALL'),
                         wired('O36_SNORM'), wired('O36_D2'))
D2 = 0.5582775239783688
print('ORDER J — THE RULED TALL/SMALL SITTER FACTOR, DISCLOSED')
print('\n== 1 · THE WIRED CONSTANTS, AGAINST ORDER H\'S OWN FILE ==')
print('  g0        wired %.16f' % TG0)
print('  g1        wired %.16f' % TG1)
print('  h_TALL    wired %.16f   H_RESULTS %.16f   dev %.1e' % (HT, HA['h_TALL'], abs(HT - HA['h_TALL'])))
print("  s_norm'   wired %.16f   H_RESULTS %.16f   dev %.1e" % (SN, HA['s_norm_prime'], abs(SN - HA['s_norm_prime'])))
print('  the ruled depth-2 fade wired as %.7f (H\'s full-precision value %.16f)' % (D2W, D2))
assert abs(HT - HA['h_TALL']) == 0.0 and abs(SN - HA['s_norm_prime']) == 0.0, \
    'ORDER J HALT: the wire has drifted from H_RESULTS.json'

CLIP = (0.5, 2.0)
kap = lambda p, tall: min(CLIP[1], max(CLIP[0], (TG0 + TG1 * math.log(max(1.0, min(64.0, float(p))))
                                                 + (HT if tall else 0.0)) / SN))

print('\n== 2 · THE TRANSCRIBED CURVE vs H_RESULTS.json, AT EVERY PICK H PUBLISHED ==')
print('  %5s %12s %12s %12s %12s %10s' % ('pick', 'SMALL wired', 'SMALL H', 'TALL wired', 'TALL H', 'max dev'))
wd = 0.0
for pk in sorted(HA['kappa_table'], key=lambda x: int(x)):
    t = HA['kappa_table'][pk]
    a, b = kap(int(pk), False), kap(int(pk), True)
    d = max(abs(a - t['SMALL']), abs(b - t['TALL'])); wd = max(wd, d)
    print('  %5s %12.9f %12.9f %12.9f %12.9f %10.1e' % (pk, a, t['SMALL'], b, t['TALL'], d))
print('  worst deviation over all 11 published picks: %.1e  -> %s' % (wd, 'EXACT' if wd < 1e-12 else 'FAIL'))
assert wd < 1e-12, 'ORDER J HALT: the transcription misses H_RESULTS.json'

mT = sum(kap(p, True) for p in range(1, 65)) / sum(kap(p, False) for p in range(1, 65))
print('\n== 3 · m_TALL, THE MULTIPLICATIVE TRANSLATION ==')
print('  m_TALL over picks 1-64 on the wire        : %.6f' % mT)
print('  m_TALL as H publishes it (H\'s own averaging): %.6f' % HA['m_TALL'])
print('  the order names ~0.677 — H\'s figure. Both are printed; they differ only in how the average')
print('  is taken over the clipped range, and neither is a constant the engine uses.')

print('\n== 4 · THE REDISTRIBUTION IDENTITY, REBUILT FROM ORDER H\'S OWN FITTED SITTERS ==')
GRP = {'RUCK': 'RUCK', 'KPD': 'KPP', 'KPF': 'KPP', 'MID': 'SMALL', 'SD': 'SMALL', 'SF': 'SMALL'}
FM = {'paddy-mccartin', 'thomas-boyd'}
A = json.load(open(SP + '/per_entrant_O32RFINAL.json'))
SAT = []
for r in A['recs']:
    if r['key'] in FM or not (r.get('teaches_curve') and r['type'] == 'ND'):
        continue
    if not (2005 <= r['year'] <= 2020) or not r.get('pick') or not (1 <= r['pick'] <= 64):
        continue
    if int(r.get('games_yr1') or 0) != 0:
        continue
    SAT.append((int(r['pick']), GRP[r['pos']] in ('KPP', 'RUCK')))
print('  Order H\'s fitted sitter population rebuilt: %d rows (ND 2005-2020, picks 1-64, zero year-1 games)'
      % len(SAT))
print('  n_sat printed by H for the fitted spec SAT1|ctl1|TALL-pooled: %d'
      % H['interaction']['SAT1|ctl1|TALL-pooled']['n_sat'])
ident = sum(D2 ** kap(p, t) for p, t in SAT) / len(SAT) - D2
print('  IDENTITY RESIDUAL  mean(D2^kappa) - D2 = %+.3e   (H published -1.11e-16)' % ident)
print('  -> %s  the total fade the board charges is UNCHANGED; this factor only moves fade between'
      % ('PASS at 1e-9' if abs(ident) < 1e-9 else 'FAIL'))
print('     talls and smalls.')
assert abs(ident) < 1e-9, 'ORDER J HALT: F5 FIRES — the redistribution identity does not hold'

print('\n== 5 · THE EXPONENT, SMALL vs TALL, AT THE PICKS THE OWNER ASKED ABOUT ==')
for pk in (1, 7, 10, 16, 24, 25, 30, 40, 55, 64):
    print('  pick %-3d  small %.4f   tall %.4f   %s' % (pk, kap(pk, False), kap(pk, True),
          'both on the 0.5 clip' if max(kap(pk, False), kap(pk, True)) <= 0.5 + 1e-12
          else ('tall on the 0.5 clip' if kap(pk, True) <= 0.5 + 1e-12 else '')))
print('  DECLARED SIDE EFFECT (i): the 0.5 clip binds for TALLS over picks %s and for SMALLS over'
      % ('1-%d' % max(HA['clip_pinned_picks_TALL'])))
print('      picks 1-%d. Over that range the clip, not the fit, sets the price — a flat spot that ends'
      % max(HA['clip_pinned_picks_SMALL']))
print('      abruptly at pick %d. Inherited from Order D\'s clip.' % (max(HA['clip_pinned_picks_TALL']) + 1))
print('  DECLARED SIDE EFFECT (ii): the identity is pinned, so LATE SMALL SITTERS PAY for the talls\'')
D_POOL64 = HA['kappa_table']['64']['D_pooled']
print('      relief — a small at pick 64 goes from Order D\'s wired pooled exponent %.4f to %.4f'
      % (D_POOL64, kap(64, False)))
print('      (D_pooled is H_RESULTS.json\'s own column for Order D\'s curve, not a re-derivation here).')

# ---- 6 · the store-wide mature-row movement, in board points --------------------------------------
os.environ.update(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_TALL='1', RL_O36_LAM_S1='0.0',
                  PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22', RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
os.environ.pop('RL_O32_STAGE', None)
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(cwd)
MA = NSE.get('MA', MA); ev = NSE['ev']
F = 1.0524
BY = {}
for p in MA.data:
    BY.setdefault(p.get('key'), []).append(p)
PB = {k: max(v, key=lambda q: len(q['scoring'])) for k, v in BY.items()}
ACT = [p for p in PB.values() if NSE['_isreal'](p) and not p.get('_retired')
       and not NSE['delisted'](p) and MA.GRP.get(p.get('pos'))]
ALLK = sorted([p.get('key') for p in ACT])
MAT = sorted([p.get('key') for p in ACT if p.get('_by') and MA._age_at(p, 2026) >= 24])
NAME = {p.get('key'): p.get('player') for p in ACT}
AGEOF = {p.get('key'): MA._age_at(p, 2026) for p in ACT}
PICKOF = {p.get('key'): (MA.effpk(p) if not p.get('_pickless') else None) for p in ACT}
POSOF = {p.get('key'): MA.gfut(p) for p in ACT}


def price(keys, dial):
    MA._O36 = bool(dial); NSE['_O36'] = bool(dial)
    MA.O36_LAM_S1 = 0.0
    MA._pe_clear()
    o = {}
    for k in keys:
        with contextlib.redirect_stdout(io.StringIO()):
            o[k] = float(ev(PB[k], 2026)) / F
    return o


OFF = price(ALLK, False)      # the landing candidate 1f176444
ON = price(ALLK, True)        # the ruled tall factor alone (lambda_S1 = 0)
BJ = json.load(open(os.path.join(HERE, 'BASELINE_J.json')))
dev = max(abs(OFF[k] - BJ['all_values'][k] / F) for k in ALLK)
print('\n== 6 · THE FULL MOVED-ROW LIST FOR EVERY ACTIVE ROW AGED 24+ (board points) ==')
print('  dial-off baseline vs BASELINE_J: worst deviation %.1e over %d rows -> %s'
      % (dev, len(ALLK), 'EXACT' if dev == 0 else 'DEVIATION'))
MOV = sorted([(ON[k] - OFF[k], k) for k in MAT if ON[k] != OFF[k]], key=lambda t: -abs(t[0]))
tot_abs = sum(abs(d) for d, _ in MOV); tot_net = sum(d for d, _ in MOV)
mature_total = sum(OFF[k] for k in MAT)
print('  rows aged 24+ that move : %d of %d' % (len(MOV), len(MAT)))
print('  total ABSOLUTE movement : %.1f board points  (%.4f%% of the board, %.4f%% of the mature pool)'
      % (tot_abs, 100 * tot_abs / (BJ['board_total'] / F), 100 * tot_abs / mature_total))
print('  total NET movement      : %+.1f board points (%.4f%% of the board)'
      % (tot_net, 100 * tot_net / (BJ['board_total'] / F)))
up = [t for t in MOV if t[0] > 0]; dn = [t for t in MOV if t[0] < 0]
print('  %d up, %d down · largest up %+.1f (%s) · largest down %+.1f (%s)'
      % (len(up), len(dn), up[0][0] if up else 0.0, NAME.get(up[0][1], '') if up else '',
         dn[0][0] if dn else 0.0, NAME.get(dn[0][1], '') if dn else ''))
print('\n  %-26s %4s %5s %6s %10s %10s %9s %8s' % ('row', 'age', 'pick', 'pos', 'landing', 'with factor', 'move', 'as %'))
for d, k in MOV:
    print('  %-26s %4d %5s %6s %10.1f %10.1f %+9.2f %+7.2f%%'
          % ((NAME.get(k) or k)[:26], AGEOF[k], PICKOF.get(k) if PICKOF.get(k) else '-',
             POSOF.get(k), OFF[k], ON[k], d, 100 * d / max(OFF[k], 1e-9)))
AGEC = collections.Counter(AGEOF[k] for _, k in MOV)
print('\n  age profile of the mature rows that move: %s' % dict(sorted(AGEC.items())))
print('  FOR COMPARISON ONLY — J-TOL would have allowed each of these rows min(25, max(1, 0.5%%)):')
nover = sum(1 for d, k in MOV if abs(d) > min(25.0, max(1.0, 0.005 * OFF[k])))
print('  %d of the %d moved rows exceed that cap. THE FACTOR IS EXEMPT AND IS NOT GATED BY IT — this'
      % (nover, len(MOV)))
print('  line exists so the owner can see the ruled change and the gated one on the same ruler.')

# ---- 7 · the day-0 disclosure ----------------------------------------------------------------------
print('\n== 7 · THE DAY-0 DISCLOSURE (the ruled fade regenerates the printed sitter reference) ==')
ed = NSE['_entry29b_derived']; o31D = NSE['o31_D']
Y = MA.BASE_REF
rows = []
for dial in (False, True):
    MA._O36 = bool(dial); NSE['_O36'] = bool(dial); MA.O36_LAM_S1 = 0.0; MA._pe_clear()
    cur = {}
    for p in MA.data:
        with contextlib.redirect_stdout(io.StringIO()):
            d0 = ed(p, Y)
        if d0 is None:
            continue
        k = p.get('key') or MA.slug(p['player'])
        with contextlib.redirect_stdout(io.StringIO()):
            D = float(o31D(p, Y))
        cur[k] = (float(d0), D, float(d0) * D)
    rows.append(cur)
OFF0, ON0 = rows
ks = sorted(set(OFF0) & set(ON0))
v0same = sum(1 for k in ks if OFF0[k][0] == ON0[k][0])
print('  wired day-0 entrants: %d' % len(ks))
print('  derived_v0 (the raw ENTRY object the walk-forward matrix writes as year-0):')
print('     BIT-IDENTICAL on %d of %d at tolerance 0  -> %s' % (v0same, len(ks), 'PASS' if v0same == len(ks) else 'F4 FIRES'))
assert v0same == len(ks), 'ORDER J HALT: F4 FIRES — derived_v0 moved'
pm = sorted([(ON0[k][2] - OFF0[k][2], k) for k in ks if int(round(ON0[k][2])) != int(round(OFF0[k][2]))],
            key=lambda t: -t[0])
print('  the PRINTED day-0 price (= entry value x the sitting discount):')
print('     moves on %d of %d rows — %d up, %d down' % (len(pm), len(ks), sum(1 for d, _ in pm if d > 0),
                                                        sum(1 for d, _ in pm if d < 0)))
if pm:
    for lbl, t in (('largest up  ', pm[0]), ('largest down', pm[-1])):
        k = t[1]
        print('     %s %-24s %.0f -> %.0f (%+.0f)' % (lbl, (NAME.get(k) or k)[:24],
                                                      OFF0[k][2] / F, ON0[k][2] / F, t[0] / F))
print('  IN PLAIN WORDS: a day-0 price for a man who has never played IS his entry value multiplied by')
print('  the sitting discount. This factor changes the discount for talls. So the printed price of an')
print('  already-sitting player moves BY CONSTRUCTION, while his entry value does not move at all.')
print('  That is the intended effect the owner ruled in, and it is the same regeneration Order D\'s own')
print('  pick-curve fade required when it landed. DISCLOSED, not gated.')

json.dump(dict(order='ORDER J — the owner-ruled tall/small sitter factor, disclosed',
               ruling='R-TALLFACTOR ADOPTED — issue #334 comment 5320813582',
               constants=dict(g0=TG0, g1=TG1, h_TALL=HT, s_norm_prime=SN, d2=D2,
                              m_TALL_wire=mT, m_TALL_H=HA['m_TALL']),
               transcription_worst_dev=wd, identity_residual=ident, n_fitted_sitters=len(SAT),
               kappa_by_pick={str(p): dict(small=kap(p, False), tall=kap(p, True)) for p in range(1, 65)},
               mature_moved=[dict(key=k, name=NAME.get(k), age=AGEOF[k], pick=PICKOF.get(k),
                                  pos=POSOF.get(k), landing=OFF[k], with_factor=ON[k], move=d)
                             for d, k in MOV],
               mature_totals=dict(n_moved=len(MOV), n_mature=len(MAT), abs_total=tot_abs,
                                  net_total=tot_net, mature_pool=mature_total,
                                  pct_of_board=100 * tot_abs / (BJ['board_total'] / F),
                                  n_over_jtol_cap_for_reference=nover),
               day0=dict(n_wired=len(ks), derived_v0_identical=v0same,
                         printed_moved=len(pm), up=sum(1 for d, _ in pm if d > 0),
                         down=sum(1 for d, _ in pm if d < 0),
                         rows={k: dict(derived_v0=OFF0[k][0], printed_off=OFF0[k][2] / F,
                                       printed_on=ON0[k][2] / F) for k in ks})),
          open(os.path.join(HERE, 'TALL_J.json'), 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: TALL_J.json')
