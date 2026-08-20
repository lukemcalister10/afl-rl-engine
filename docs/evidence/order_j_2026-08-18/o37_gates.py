#!/usr/bin/env python3
"""ORDER J — THE OWNER'S GATES, SCORED ON THE BOARDS, IN BOARD POINTS, ROW BY NAMED ROW.

Pure JSON reads over the boards build_all37.sh already wrote — no engine run here, so nothing can
drift between what is scored and what was built.

Every board gate is printed for BOTH columns and they are never mixed:
  * ORDER J RULED     — the owner-ruled tall/small sitter factor alone (R-TALLFACTOR, ADOPTED).
  * ORDER J REFERENCE — the cheapest law-satisfying setting. FAILS J-TOL. NOT CARRIED.

G1/G2/G3 live on the walk-forward instruments and are scored by bb_standing_tables37.py, on the
standing extended-338, which PREREG_J §3.3 registered as the instrument that decides.
"""
import json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O37 = SP + '/o37'
TAGS = ['cand', 'tall', 'tall2', 's1', 'ref']
BP = {t: O37 + '/bb_%s/rl_after/rl_app_data.json' % t for t in TAGS}
MD5 = {t: hashlib.md5(open(BP[t], 'rb').read()).hexdigest() for t in TAGS}
RAW = {t: json.load(open(BP[t])) for t in TAGS}
B = {t: {r['key']: r for r in RAW[t]['active']} for t in TAGS}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in TAGS}
KEYS = sorted(V['cand'])
AGE = {k: B['cand'][k]['age'] for k in KEYS}
NAME = {k: (B['cand'][k].get('player') or k) for k in KEYS}

print('ORDER J — THE BOARD GATES.  board points (the currency the owner reads).')
print('  boards: %s' % {t: MD5[t][:8] for t in TAGS})
print('\n== THE BUILD-FAILING IDENTITIES ==')
f3 = MD5['cand'].startswith('1f176444')
det = (MD5['tall'] == MD5['tall2'])
print('  F3  dial-off reproduces the landing candidate 1f176444 : %s  (%s)'
      % ('PASS' if f3 else 'FAIL — F3 FIRES', MD5['cand'][:32]))
print('  F9  determinism x2 (two identical builds of the ruled board): %s  (%s vs %s)'
      % ('PASS' if det else 'FAIL — F9 FIRES', MD5['tall'][:8], MD5['tall2'][:8]))
assert f3 and det, 'ORDER J HALT: a build-failing identity did not hold'

MAT = [k for k in KEYS if AGE[k] >= 24]
print('\n== THE MATURE-ROW LAW, ON THE WRITTEN BOARDS (integer board points) ==')
for lab, t in (('ORDER J RULED (exempt — R-TALLFACTOR is adopted)', 'tall'),
               ('ORDER J REFERENCE (gated — fails J-TOL)', 'ref'),
               ('S1 alone at the reference dose (zero-tolerance test)', 's1')):
    mv = [(k, V[t][k] - V['cand'][k]) for k in MAT if V[t][k] != V['cand'][k]]
    tot = sum(abs(d) for _, d in mv); net = sum(d for _, d in mv)
    w = max(mv, key=lambda x: abs(x[1])) if mv else (None, 0)
    print('  %-52s %3d of %d move · abs %5d · net %+5d · worst %+4d (%s)'
          % (lab, len(mv), len(MAT), tot, net, w[1], NAME.get(w[0], '-')))

NAMED = [('harry-dean', 'UP', 'S1: 14.9 a game clear of his own age bar'),
         ('cooper-duff-tytler', 'UP', 'S1: 7.1 a game clear of his own age bar'),
         ('xavier-taylor', 'DOWN', 'sub-expectation WITH games (42.0 vs an age bar of 55.2)'),
         ('daniel-annable', 'DOWN', 'sub-expectation WITH games (38.0 vs 57.0)'),
         ('dylan-patterson', 'DOWN', 'sub-expectation WITH games (35.6 vs 55.2)'),
         ('oskar-taylor', 'UP', 'zero games — only the ruled fade can reach him'),
         ('josh-smillie', 'UP', 'the ruled factor\'s 0.5 clip at small picks 1-9'),
         ('chris-scerri', 'UP', 'pool row — production dominates a small pedigree'),
         ('thomas-burton', 'UP', 'same channel, weaker'),
         ('milan-murdock', 'MOVES-INSIDE-JTOL', 'age 26 with 17 games — inside the re-mix\'s active zone'),
         ('will-green', 'UP', 'the ruled factor at pick 16'),
         ('toby-conway', 'UP', 'the ruled factor at pick 24'),
         ('steely-green', 'DOWN', 'a late small pays for the talls\' relief'),
         ('isaac-kako', 'UP', 'S1 on a high-rho row'),
         ('alix-tauru', 'UP', 'S1; tall age gaps are the largest'),
         ('jedd-busslinger', 'UP', 'S1 + the ruled fade on an above-age-bar season')]
EXTRA = ['levi-ashcroft', 'connor-o-sullivan', 'logan-morris', 'finn-o-sullivan', 'sam-taylor',
         'tom-green', 'toby-greene', 'will-ashcroft', 'taylor-walker', 'keidean-coleman',
         'harry-morrison', 'taylor-goad', 'zac-taylor']

print('\n== THE NAMED ROWS (board points) ==')
print('%-22s %4s %9s %9s %9s | %9s %9s | %-10s %-8s %s'
      % ('row', 'age', 'landing', 'J RULED', 'J REF', 'd ruled', 'd ref', 'predicted', 'actual', 'hit?'))
SC = []
for k, pred, why in NAMED:
    if k not in V['cand']:
        print('%-22s (not on the 804-row active board)' % k); continue
    a, r, f = V['cand'][k], V['tall'][k], V['ref'][k]
    d = f - a
    act = 'FLAT' if d == 0 else ('UP' if d > 0 else 'DOWN')
    hit = (act == pred) if pred in ('UP', 'DOWN') else (d != 0)
    SC.append(dict(key=k, pred=pred, actual=act, hit=bool(hit), landing=a, ruled=r, ref=f,
                   d_ruled=r - a, d_ref=d, why=why))
    print('%-22s %4d %9d %9d %9d | %+9d %+9d | %-10s %-8s %s'
          % (k, AGE[k], a, r, f, r - a, d, pred, act, 'HIT' if hit else 'MISS'))
print('\nprereg scorecard (scored on the REFERENCE board, the only one with all three levers live): '
      '%d of %d named-row directions correct' % (sum(1 for s in SC if s['hit']), len(SC)))

print('\n== G4 — THE OWNER\'S TWO REFERENCE LEVELS (board points) ==')
G4 = {}
for k, target, c31 in (('harry-dean', 2600, 2670), ('cooper-duff-tytler', 1800, 1832)):
    a, r, f = V['cand'][k], V['tall'][k], V['ref'][k]
    G4[k] = dict(target=target, c31=c31, landing=a, ruled=r, ref=f)
    print('  %-20s target ~%d (C31 %d) · landing %d · J RULED %d (short %d) · J REF %d (short %d)  -> %s'
          % (k, target, c31, a, r, target - r, f, target - f,
             'BOTH FAIL' if max(r, f) < target * 0.98 else 'see numbers'))

print('\n== G5 — SUB-EXPECTATION-WITH-GAMES ROWS MUST NOT RISE (board points) ==')
G5 = {}
for k in ('xavier-taylor', 'daniel-annable', 'dylan-patterson'):
    a, r, f = V['cand'][k], V['tall'][k], V['ref'][k]
    G5[k] = dict(landing=a, ruled=r, ref=f)
    print('  %-20s landing %5d · J RULED %5d (%+d) · J REF %5d (%+d)  -> %s'
          % (k, a, r, r - a, f, f - a,
             'ROSE — G5 FAIL on the reference' if f > a else ('held' if f == a else 'FELL — G5 holds')))

print('\n== SIDE — josh-smillie\'s ruled ~700s range (board points) ==')
k = 'josh-smillie'
print('  landing %d · J RULED %d · J REF %d  -> %s'
      % (V['cand'][k], V['tall'][k], V['ref'][k],
         'HOLDS the 700s' if 700 <= V['tall'][k] < 800 else
         'LEAVES the 700s — and the whole move is the OWNER-RULED factor, disclosed not gated'))

print('\n== CONTROLS AND OTHER ROWS OF RECORD (board points) ==')
for k in EXTRA:
    if k in V['cand']:
        print('  %-22s landing %6d · J RULED %6d (%+5d) · J REF %6d (%+5d)'
              % (k, V['cand'][k], V['tall'][k], V['tall'][k] - V['cand'][k],
                 V['ref'][k], V['ref'][k] - V['cand'][k]))

LED = json.load(open(os.path.join(ROOT, 'docs', 'ledgers', 'ORDER_J_MOVERS.json')))
Y1 = [r['key'] for r in LED['rows']
      if (r['yr'] == 2025) or (r['yr'] == 2026 and r['pathway'] == 'MSD')]
print('\n== THE YEAR-1 CLASS ON THE 2026 BOARD (board points) ==')
for lab, t in (('J RULED', 'tall'), ('J REF', 'ref')):
    t0 = sum(V['cand'][k] for k in Y1); t1 = sum(V[t][k] for k in Y1)
    up = sum(1 for k in Y1 if V[t][k] > V['cand'][k]); dn = sum(1 for k in Y1 if V[t][k] < V['cand'][k])
    print('  %-8s %d rows, %d -> %d (%+.2f%%);  %d up, %d down, %d unchanged'
          % (lab, len(Y1), t0, t1, 100 * (t1 - t0) / max(1, t0), up, dn, len(Y1) - up - dn))

json.dump(dict(order='ORDER J — the board gates',
               boards={t: MD5[t] for t in TAGS}, f3_dial_off=f3, f9_determinism=det,
               scorecard=SC, g4=G4, g5=G5,
               smillie=dict(landing=V['cand']['josh-smillie'], ruled=V['tall']['josh-smillie'],
                            ref=V['ref']['josh-smillie']),
               extra={k: dict(landing=V['cand'][k], ruled=V['tall'][k], ref=V['ref'][k])
                      for k in EXTRA if k in V['cand']},
               year1={lab: dict(n=len(Y1), landing=sum(V['cand'][k] for k in Y1),
                                board=sum(V[t][k] for k in Y1))
                      for lab, t in (('ruled', 'tall'), ('ref', 'ref'))}),
          open(os.path.join(HERE, 'GATES_J.json'), 'w'), indent=1, sort_keys=True, default=float)
print('\nwritten: GATES_J.json')
