#!/usr/bin/env python3
"""ORDER P BUILD — THE MOVERS LEDGER, over the five standing board columns plus the mechanism legs.

Columns: live 88ce647f · Candidate 31 fe6be9d6 · the landing candidate 1f176444 · ORDER K f3101883 ·
ORDER P (the decision board).

The ORDER K legs are CARRIED from docs/ledgers/ORDER_K_MOVERS.json unchanged, so the reader can see
the whole stack in one row rather than two documents:
  leg TALL   the owner-ruled tall/small sitter factor, with the ORDER K re-sited fade floor
  leg S1     the age-referenced projection bar at the RULED dose 0.40
  leg CW     the counterweight's own contribution
  leg FLOOR  what the fade floor fix itself is worth
  residual   ORDER K minus (landing + tall + S1 + CW) — the interaction, SHOWN rather than hidden

THE NEW LEG IS leg P = ORDER P minus ORDER K. It is the whole of this order, because this order
changes exactly one mechanism. Beside it, every input that mechanism reads is printed for the row:

  v0          his entry price, the axis the pedigree premium is read on
  premium     PG(ln v0, class) — how far above the age bar a player at his price normally produces
  s_N         his production minus the AGE bar (what ORDER K's world would have measured)
  s_P         his production minus the PEDIGREE bar (= s_N - premium). THIS is what the charge reads
  charge K    the fraction of his pedigree leg the blind charge removes
  charge P    the fraction the pedigree-conditional charge removes
  A(g), T     the two factors inside it

Pure JSON reads over boards already built by build_allP.sh — no engine run here.
"""
import json, math, os, re, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OP = SP + '/op'
import hashlib
TAGS = ['candP', 'Kref', 'P']
BP = {t: OP + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
B = {t: {r['key']: r for r in json.load(open(BP[t]))['active']} for t in TAGS}
print('boards:', {t: m[:8] for t, m in MD5.items()})
assert MD5['candP'].startswith('1f176444'), 'the base-stack rebuild is %s, not 1f176444 — HALT' % MD5['candP'][:8]
assert MD5['Kref'].startswith('f3101883'), 'B1 FIRES: the dial-off rebuild is %s, not ORDER K f3101883' % MD5['Kref'][:8]
KL = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_K_MOVERS.json')))
KROW = {r['key']: r for r in KL['rows']}
TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))

# ---- the mechanism, read out of the engine source ------------------------------------------------
src = open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py'), encoding='utf-8').read()
GRID = eval(re.search(r'^\s*O37_PG_GRID=\{.*?^\s*\}\s*$', src, re.S | re.M).group(0).split('=', 1)[1],
            {'__builtins__': {}}, {})
C = {}
for nm in ('O37_G0', 'O37_BETA_SAT', 'O37_LAMBDA', 'O37_S0', 'O37_S_P5', 'O37_AGE_GATE'):
    C[nm] = float(re.search(r'^\s*%s=(-?[0-9.eE+-]+)\s' % nm, src, re.M).group(1))
THR = C['O37_BETA_SAT'] / C['O37_LAMBDA']
TMAX = 1.0 - THR * (C['O37_S_P5'] - C['O37_S0'])
GATE = eval(re.search(r'O32_GATE_DELTA=\{.*?\}\}', src, re.S).group(0).split('=', 1)[1], {'__builtins__': {}}, {})
FLAT = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
ETA_K, GD = 0.50, 14.0


def pg(v0, cls):
    lo, hi, y = GRID[cls]
    x = math.log(max(1e-9, float(v0)))
    if x <= lo: return y[0]
    if x >= hi: return y[-1]
    t = (x - lo) / (hi - lo) * (len(y) - 1); i = int(t)
    return y[-1] if i >= len(y) - 1 else y[i] + (t - i) * (y[i + 1] - y[i])


def agebar(pos, age):
    b = FLAT.get(pos)
    if b is None or age is None or age >= 24: return b
    return b - GATE['TALL' if pos in TALLPOS else 'SMALL'][max(18, min(23, int(age)))]


A = lambda g: 1.0 - math.exp(-float(g) / C['O37_G0'])
T = lambda s: min(max(1.0 - THR * (float(s) - C['O37_S0']), 0.0), TMAX)
F_old = lambda g: max(0.0, ETA_K * (float(g) / GD) * math.exp(1.0 - float(g) / GD)) if g > 0 else 0.0
MK = {r['key']: r for r in json.load(open(SP + '/per_entrant_OKRULED.json'))['recs']}


def mech(key):
    r = MK.get(key)
    out = dict(v0=None, premium=None, sN=None, sP=None, g=None, age=None,
               charge_k=None, charge_p=None, A=None, T=None, gated=None)
    if r is None: return out
    v0 = float(r.get('v0') or 0.0); ad = r.get('age_draft')
    g = float(r.get('games_total') or 0.0)
    out['v0'] = v0 or None; out['g'] = g
    out['age'] = (int(ad) + (2026 - int(r['year']))) if ad is not None else None
    out['charge_k'] = F_old(g)
    if not (v0 > 0) or ad is None: return out
    num = den = pnum = anum = 0.0
    for s in r['seasons']:
        gg = float(s.get('games') or 0.0)
        if gg <= 0: continue
        pos = s.get('bar'); b = agebar(pos, int(ad) + (int(s['year']) - int(r['year'])))
        if b is None or s.get('avg') is None: return out
        prem = pg(v0, 'TALL' if pos in TALLPOS else 'SMALL')
        anum += gg * (float(s['avg']) - b); pnum += gg * prem
        num += gg * (float(s['avg']) - (b + prem)); den += gg
    if den <= 0:
        out['charge_p'] = out['charge_k']       # no played season: A(0)=0, nothing is charged either way
        return out
    out['sN'] = anum / den; out['premium'] = pnum / den; out['sP'] = num / den
    out['gated'] = (out['age'] is not None and out['age'] >= C['O37_AGE_GATE'])
    if out['gated'] or g <= 0:
        out['charge_p'] = out['charge_k']
    else:
        out['A'] = A(g); out['T'] = T(out['sP'])
        out['charge_p'] = 1.0 - math.exp(-C['O37_LAMBDA'] * out['A'] * out['T'])
    return out


rows = []
for k, kr in KROW.items():
    if k not in B['P']: continue
    vP = B['P'][k]['v']
    m = mech(k)
    rows.append(dict(kr, orderp=vP, leg_p=vP - kr['orderk'],
                     d_vs_orderk=vP - kr['orderk'], d_vs_landing=vP - kr['landing'],
                     d_vs_cand31=vP - kr['cand31'], d_vs_live=vP - kr['live'],
                     m_v0=m['v0'], m_premium=m['premium'], m_sN=m['sN'], m_sP=m['sP'],
                     m_g=m['g'], m_age=m['age'], m_charge_k=m['charge_k'], m_charge_p=m['charge_p'],
                     m_A=m['A'], m_T=m['T'], m_agegated=m['gated']))
print('ledger rows: %d' % len(rows))
tot = {f: sum(r[f] for r in rows) for f in
       ('live', 'cand31', 'landing', 'orderk', 'orderp', 'leg_tall', 'leg_s1', 'leg_cw',
        'leg_floor', 'residual', 'leg_p')}
print('totals:', {k: round(v) for k, v in tot.items()})
MV = [r for r in rows if r['leg_p'] != 0]
print('\nORDER P vs ORDER K: %d of %d rows move (%d up, %d down); aged 24+: %d rows, %+d points'
      % (len(MV), len(rows), sum(1 for r in MV if r['leg_p'] > 0), sum(1 for r in MV if r['leg_p'] < 0),
         sum(1 for r in MV if r['age'] >= 24), sum(r['leg_p'] for r in MV if r['age'] >= 24)))
print('board total: ORDER K %d -> ORDER P %d  (%+.2f%%)'
      % (round(tot['orderk']), round(tot['orderp']), 100 * (tot['orderp'] - tot['orderk']) / tot['orderk']))

BYK = {r['key']: r for r in rows}
NAMED = ['harry-dean', 'cooper-duff-tytler', 'xavier-taylor', 'daniel-annable', 'dylan-patterson',
         'isaac-kako', 'josh-smillie', 'milan-murdock', 'zeke-uwland', 'cooper-harvey',
         'jhye-clark', 'arthur-jones', 'samuel-grlj', 'will-green', 'taylor-goad', 'murphy-reid']
print('\n%-22s %4s %5s %5s %7s %8s %8s %8s | %7s %7s %7s | %7s %7s %7s'
      % ('row', 'age', 'pick', 'g', 'v0', 'premium', 's vs age', 's vs ped', 'chg K', 'chg P',
         'legP', 'landing', 'ORDER K', 'ORDER P'))
for k in NAMED:
    r = BYK.get(k)
    if r is None:
        print('%-22s (not on the 804-row active board)' % k); continue
    f = lambda v, w, d: (('%%%d.%df' % (w, d)) % v) if v is not None else ' ' * (w - 1) + '-'
    print('%-22s %4s %5s %5.0f %7s %8s %8s %8s | %6s%% %6s%% %+7d | %7d %7d %7d'
          % (r['name'][:22], r['age'], r['pick'], r['m_g'] or 0, f(r['m_v0'], 7, 0),
             f(r['m_premium'], 8, 2), f(r['m_sN'], 8, 2), f(r['m_sP'], 8, 2),
             f(100 * r['m_charge_k'] if r['m_charge_k'] is not None else None, 6, 1),
             f(100 * r['m_charge_p'] if r['m_charge_p'] is not None else None, 6, 1),
             r['leg_p'], r['landing'], r['orderk'], r['orderp']))

for nm, rev in (('TOP 20 UP', True), ('TOP 20 DOWN', False)):
    print('\n%s — ORDER P vs ORDER K:' % nm)
    for r in sorted(MV, key=lambda x: (-x['leg_p'] if rev else x['leg_p']))[:20]:
        print('  %-26s %-5s %3s %4s %4.0fg  v0 %6s  s_P %7s  chgK %5.1f%% -> chgP %5.1f%%  %6d -> %6d  %+5d'
              % (r['name'][:26], r['pos'], r['age'], r['pick'], r['m_g'] or 0,
                 ('%.0f' % r['m_v0']) if r['m_v0'] else '-',
                 ('%+.2f' % r['m_sP']) if r['m_sP'] is not None else '-',
                 100 * (r['m_charge_k'] or 0), 100 * (r['m_charge_p'] or 0),
                 r['orderk'], r['orderp'], r['leg_p']))

print('\nage profile of the rows that move: %s' % dict(sorted(collections.Counter(r['age'] for r in MV).items())))
print('games profile:')
for lo, hi, lab in ((0, 0, '0'), (1, 4, '1-4'), (5, 9, '5-9'), (10, 15, '10-15'), (16, 29, '16-29'),
                    (30, 59, '30-59'), (60, 10 ** 9, '60+')):
    s = [r for r in rows if lo <= (r['m_g'] or 0) <= hi]
    if not s: continue
    print('  %-8s rows %4d  total %+7d  per row %+7.1f'
          % (lab, len(s), sum(r['leg_p'] for r in s), sum(r['leg_p'] for r in s) / len(s)))
print('age bands:')
for lo, hi, lab in ((0, 20, '20 and under'), (21, 23, '21-23'), (24, 99, '24 and over')):
    s = [r for r in rows if lo <= int(r['age']) <= hi]
    print('  %-14s rows %4d  total %+7d' % (lab, len(s), sum(r['leg_p'] for r in s)))

out = dict(order='ORDER P — the movers ledger',
           meta=dict(boards=dict(live=KL['meta']['boards']['live'], cand31=KL['meta']['boards']['cand31'],
                                 landing=MD5['candP'], orderk=MD5['Kref'], orderp=MD5['P']),
                     setting=dict(dose=0.40, kappa=0.20, gamma_u=8.0, eta=0.50, gamma_d=14.0,
                                  lam_rel=1.08, tall_factor='R-TALLFACTOR, ORDER K fade floor',
                                  order_p=dict(G0=C['O37_G0'], BETA_sat=C['O37_BETA_SAT'],
                                               LAMBDA=C['O37_LAMBDA'], THETA_R=THR, s0=C['O37_S0'],
                                               TMAX=TMAX, age_gate=C['O37_AGE_GATE'],
                                               form='pi *= exp(-LAMBDA*A(g)*T(s_P))'))),
           totals=tot, rows=rows)
json.dump(out, open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_P_MOVERS.json'), 'w'),
          indent=1, sort_keys=True, default=float)
print('\nwrote docs/ledgers/ORDER_P_MOVERS.json')
