#!/usr/bin/env python3
"""FINAL-CANDIDATE — boards, lever stack and the movers ledger, on daa16812.

ORIGINAL ASSEMBLY HEADER FOLLOWS.

ASSEMBLY BUILD — THE BOARDS, SCORED, AND THE LEVER STACK DECOMPOSED. Pure JSON reads over boards
already built. NO ENGINE RUN HERE.

  IDENT_P  374d4e44  every assembly dial unset          — A-F1, must be BYTE-EXACT
  IDENT_K  f3101883  ORDER K's ruled line               — A-F2, must be BYTE-EXACT
  L0_R     7f88f509  R20A, the owner's reference        — A-F1, must be BYTE-EXACT
  L1_REC   + recency 0.47
  L2_COMP  + the compressed cap p20 AND the slope 0.105 (replacing the clip)
  L3_MAT   + the mature refit
  L4_SD    + the SD level offset, standalone
  L5A_CRED + the measured credit curve                  (absence I1)
  L5B_RSET + the graded reset + the F4 depth>=3 row      (absence I2)
  L5C_INJ  + the injury stream, live board only          (absence I3)
  CAND     + the R3 production fade                      (absence I4)  = THE CANDIDATE
  CAND_2   the determinism repeat
  live     88ce647f  NEVER TOUCHED, carried for reference only

NOTHING HERE IS ADOPTED. These are prices, not proposals.
"""
import json, os, hashlib, collections, csv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM = SP + '/asm'
FCD = SP + '/fc'


CPD = SP + '/compscratch'   # THIS (completion) seat's own boards


def bdir(t):
    if t.startswith('CP_') or t.startswith('D7_'):
        return CPD
    return FCD if t.startswith('FC_') else ASM

ORDER = ['IDENT_P', 'IDENT_K', 'L0_R', 'L1_REC', 'L2_COMP', 'V750_L2C15', 'V750_L3MAT',
         'V750_L4SD', 'V750_L5A', 'V750_L5B', 'V750_L5C', 'V755_L5CR', 'V755_CAND',
         'FC_BASE', 'FC_CAND', 'CP_CAND', 'D7_CAND2']
NICE = {
    'IDENT_P':  'every assembly dial OFF          = ORDER P, the identity',
    'IDENT_K':  "ORDER K's ruled line             = the K/landing chain",
    'L0_R':     'R20A  A+B1+p20 clip              = R, the owner\'s reference',
    'L1_REC':   '+ recency w=0.47',
    'L2_COMP':    '  [superseded] compressed cap at p20 + slope 0.105 — kept to show the anchor move',
    'V750_L2C15': '+ compressed cap p15 + slope 0.105  (replaces the clip; ANCHOR RULED AT v750)',
    'V750_L3MAT': '+ the mature refit',
    'V750_L4SD':  '+ the SD level offset 2.98, standalone',
    'V750_L5A':   '+ absence I1  the measured credit curve',
    'V750_L5B':   '+ absence I2  the graded reset (the F4 row swap WITHDRAWN at v750)',
    'V750_L5C':   '+ absence I3  the injury stream (live board only)',
    'V755_L5CR':  '+ D4  the in-season ramp f**1.5 on the two DEPTH clocks  (FOLDED IN, v755)',
    'V755_CAND':  '+ absence I4  the R3 production fade',
    'FC_BASE':    '+ the unwind U0=7 return games (BREAK=unwind)  — OWNER-RULED, DATA-SUPPORTED',
    'FC_CAND':    '+ D6 the injury consolidation (RL_O42=1)',
    'CP_CAND':    '+ D7 THE PARITY GUARD (RL_O43=1) max(injury, healthy)  = THE CANDIDATE',
    'D7_CAND2':   'the determinism repeat of THE CANDIDATE',
}
EXPECT = {'IDENT_P': '374d4e44', 'IDENT_K': 'f3101883', 'L0_R': '7f88f509'}
REF_TOT = {'live': 752429, 'IDENT_K': 673097, 'IDENT_P': 666434, 'L0_R': 664950}

L = []


def P(s=''):
    print(s); L.append(str(s))


PATHS = {}
for t in ORDER:
    q = '%s/bb_%s/rl_after/rl_app_data.json' % (bdir(t), t)
    if os.path.exists(q):
        PATHS[t] = q
_live = SP + '/o29r/seal/rl_after/rl_app_data.json'
if os.path.exists(_live):
    PATHS['live'] = _live
MD5 = {t: hashlib.md5(open(q, 'rb').read()).hexdigest() for t, q in PATHS.items()}
if MD5.get('live', '')[:8] != '88ce647f':
    PATHS.pop('live', None); MD5.pop('live', None)

B = {t: {r['key']: r for r in json.load(open(q))['active']} for t, q in PATHS.items()}
V = {t: {k: r['v'] for k, r in B[t].items()} for t in B}
NAME = {}
POS = {}
AGE = {}
BAND = {}
PICK = {}
CAT = {}
for t in ('FC_CAND', 'L0_R', 'IDENT_P', 'live'):
    for k, r in B.get(t, {}).items():
        NAME.setdefault(k, r.get('name') or k)
        POS.setdefault(k, r.get('grp') or (r.get('fut') or [['?']])[0][0])
        AGE.setdefault(k, r.get('age'))
        BAND.setdefault(k, r.get('band'))
        PICK.setdefault(k, r.get('pk'))
        CAT.setdefault(k, r.get('cat'))

KEYS = sorted(set().union(*[set(V[t]) for t in V]))
TOT = {t: sum(V[t].values()) for t in V}

P('=' * 122)
P('ASSEMBLY BUILD — THE BOARDS AND THE LEVER STACK. NOTHING IS ADOPTED. THE CANDIDATE IS FOR OWNER REVIEW.')
P('=' * 122)
P()
P('  %-9s %-10s %10s %12s %12s %12s  %s'
  % ('board', 'md5', 'total', 'vs live', 'vs K', 'vs R', 'the lever added'))
for t in ORDER + (['live'] if 'live' in V else []):
    if t not in V:
        P('  %-9s %-10s %10s' % (t, 'NO BOARD', '—')); continue
    d_live = (TOT[t] - TOT['live']) if 'live' in TOT else None
    d_k = (TOT[t] - TOT['IDENT_K']) if 'IDENT_K' in TOT else None
    d_r = (TOT[t] - TOT['L0_R']) if 'L0_R' in TOT else None
    P('  %-9s %-10s %10s %12s %12s %12s  %s'
      % (t, MD5[t][:8], '{:,}'.format(TOT[t]),
         ('{:+,}'.format(d_live) if d_live is not None else '—'),
         ('{:+,}'.format(d_k) if d_k is not None else '—'),
         ('{:+,}'.format(d_r) if d_r is not None else '—'),
         NICE.get(t, '')))
P()

# ---- the identities -------------------------------------------------------------------------------
P('THE DIAL-CHAIN IDENTITIES — A-F1 and A-F2. These decide whether anything else is believable.')
FAIL = []
for t, want in EXPECT.items():
    got = MD5.get(t, '')[:8]
    ok = (got == want)
    if not ok:
        FAIL.append('%s: %s != %s' % (t, got or 'NO BOARD', want))
    P('  %-9s expected %s  got %s   %s' % (t, want, got or 'NO BOARD', 'OK' if ok else '*** FIRED ***'))
for t, want in REF_TOT.items():
    if t in TOT:
        ok = (TOT[t] == want)
        if not ok:
            FAIL.append('%s total %d != %d' % (t, TOT[t], want))
        P('  %-9s total expected %s  got %s   %s'
          % (t, '{:,}'.format(want), '{:,}'.format(TOT[t]), 'OK' if ok else '*** FIRED ***'))
if not MD5.get('CP_CAND') or not MD5.get('D7_CAND2'):
    P('  DETERMINISM (A-F4): NOT YET SCORABLE — one of the two repeat boards is missing.')
    FAIL.append('determinism not scorable')
elif MD5['CP_CAND'] == MD5['D7_CAND2']:
    P('  DETERMINISM (A-F4): IDENTICAL on the repeat — %s. Did not fire.' % MD5['CP_CAND'][:8])
else:
    P('  DETERMINISM (A-F4): *** FIRED *** %s vs %s' % (MD5['CP_CAND'][:8], MD5['D7_CAND2'][:8]))
    FAIL.append('determinism')
P()
if FAIL:
    P('*** FALSIFIERS FIRED: %s' % '; '.join(FAIL))
else:
    P('  Every identity holds. A-F1, A-F2 and A-F4 did not fire.')
P()

# ---- the lever stack ------------------------------------------------------------------------------
P('=' * 122)
P('THE PER-LEVER BREAKDOWN — each board is the one above it plus ONE lever, so every marginal effect')
P('is a subtraction and not an argument (the owner\'s own ask, register v742).')
P('=' * 122)
P()
# D4 (register v755) — THE RAMP IS ITS OWN STEP IN THE STACK. Without V755_L5CR between L5C and
# the candidate, the R3 marginal would silently absorb the ramp's 8 rows, which is exactly the
# conflation caught and corrected in as_unwindrows.py. One lever, one step, no exceptions.
# D7 (register v771) — THE PARITY GUARD IS ITS OWN STEP IN THE STACK, for the same reason D4 is:
# folded into D6's marginal it would be invisible, and the owner ruled it as its own act.
STACK = ['L0_R', 'L1_REC', 'V750_L2C15', 'V750_L3MAT', 'V750_L4SD', 'V750_L5A', 'V750_L5B',
         'V750_L5C', 'V755_L5CR', 'V755_CAND', 'FC_BASE', 'FC_CAND', 'CP_CAND']
P('  %-9s %10s %12s %8s %8s %8s %10s  %s'
  % ('board', 'total', 'marginal', 'moved', 'up', 'down', 'worst row', 'the lever added'))
LEVER = {}
for i, t in enumerate(STACK):
    if t not in V:
        continue
    if i == 0:
        P('  %-9s %10s %12s %8s %8s %8s %10s  %s'
          % (t, '{:,}'.format(TOT[t]), '—', '—', '—', '—', '—', NICE[t]))
        continue
    prev = STACK[i - 1]
    if prev not in V:
        continue
    mv = [k for k in KEYS if k in V[t] and k in V[prev] and V[t][k] != V[prev][k]]
    up = sum(1 for k in mv if V[t][k] > V[prev][k])
    dn = len(mv) - up
    worst = max(mv, key=lambda k: abs(V[t][k] - V[prev][k])) if mv else None
    LEVER[t] = dict(prev=prev, marginal=TOT[t] - TOT[prev], moved=len(mv), up=up, down=dn,
                    worst=(NAME.get(worst), V[t][worst] - V[prev][worst]) if worst else None,
                    rows={k: V[t][k] - V[prev][k] for k in mv})
    P('  %-9s %10s %12s %8d %8d %8d %10s  %s'
      % (t, '{:,}'.format(TOT[t]), '{:+,}'.format(TOT[t] - TOT[prev]), len(mv), up, dn,
         ('{:+,}'.format(V[t][worst] - V[prev][worst]) if worst else '—'), NICE[t]))
P()
if 'CP_CAND' in TOT and 'L0_R' in TOT:
    P('  THE WHOLE ARC R -> CANDIDATE: %s  (sum of the marginals: %s)'
      % ('{:+,}'.format(TOT['CP_CAND'] - TOT['L0_R']),
         '{:+,}'.format(sum(LEVER[t]['marginal'] for t in STACK[1:] if t in LEVER))))
    P('  These agree by construction — the stack is a chain, not an attribution. Interactions are')
    P('  INSIDE each marginal (each lever is measured on top of the ones above it), which is the')
    P('  honest reading and the one the owner asked for.')
P()

# ---- the absence package, isolated ----------------------------------------------------------------
P('THE ABSENCE PACKAGE ON ITS OWN (L4_SD -> CANDIDATE), sub-part by sub-part:')
if 'V750_L4SD' in TOT and 'FC_CAND' in TOT:
    P('  I1 the credit curve        %12s' % '{:+,}'.format(TOT.get('V750_L5A', 0) - TOT['V750_L4SD']))
    P('  I2 the graded reset + F4   %12s' % '{:+,}'.format(TOT.get('V750_L5B', 0) - TOT.get('V750_L5A', 0)))
    P('  I3 the injury stream       %12s' % '{:+,}'.format(TOT.get('V750_L5C', 0) - TOT.get('V750_L5B', 0)))
    # D4 IS ITS OWN LINE. Attributing the ramp's 8 rows to R3 is the conflation caught in
    # as_unwindrows.py, and it is not allowed back in through this table.
    P('  D4 the in-season ramp      %12s' % '{:+,}'.format(TOT.get('V755_L5CR', 0) - TOT.get('V750_L5C', 0)))
    P('  I4 the R3 production fade  %12s' % '{:+,}'.format(TOT['FC_CAND'] - TOT.get('V755_L5CR', 0)))
    P('  ' + '-' * 44)
    P('  the package total          %12s' % '{:+,}'.format(TOT['CP_CAND'] - TOT['V750_L4SD']))
P()

# ---- mature rows ----------------------------------------------------------------------------------
P('=' * 122)
P('MATURE-ROW MOVEMENT — BUILT vs EXPECTED. The prereg predicted B1 + the mature refit at about')
P('-7,064 before interactions, and predicted the BUILT number would differ because six other levers')
P('are live. Reported loudly either way.')
P('=' * 122)
mat = [k for k in KEYS if (AGE.get(k) or 0) >= 24]
yng = [k for k in KEYS if (AGE.get(k) or 0) < 24]
P('  mature rows on the board (age >= 24): %d   young rows: %d' % (len(mat), len(yng)))
for base in ('IDENT_P', 'L0_R'):
    if base in V and 'FC_CAND' in V:
        dm = sum(V['FC_CAND'][k] - V[base][k] for k in mat if k in V[base] and k in V['FC_CAND'])
        dy = sum(V['FC_CAND'][k] - V[base][k] for k in yng if k in V[base] and k in V['FC_CAND'])
        nm = sum(1 for k in mat if k in V[base] and k in V['FC_CAND'] and V['FC_CAND'][k] != V[base][k])
        P('  vs %-8s mature %12s on %4d moved rows   ·   young %12s'
          % (base, '{:+,}'.format(dm), nm, '{:+,}'.format(dy)))
if 'V750_L2C15' in V and 'V750_L3MAT' in V:
    dm = sum(V['V750_L3MAT'][k] - V['V750_L2C15'][k] for k in mat if k in V['V750_L2C15'])
    nm = sum(1 for k in mat if k in V['V750_L2C15'] and V['V750_L3MAT'][k] != V['V750_L2C15'][k])
    P('  THE MATURE REFIT LEVER ALONE (V750_L2C15 -> V750_L3MAT): %s on %d moved mature rows'
      % ('{:+,}'.format(dm), nm))
    P('  BUILT vs EXPECTED: the -7,064 estimate was for B1 + refit against a different base and')
    P('  WITHOUT the six other levers. The built refit-alone number above is the like-for-like one.')
P()

# ---- no row above its uncharged price -------------------------------------------------------------
P('A-F7 — NO ROW ABOVE ITS UNCHARGED PRICE. The uncharged ceiling is ORDER P\'s own eta-zero board.')
P('  (checked in as_accept.py against the built ceiling board; reported there)')
P()

# ---- the movers ledger ----------------------------------------------------------------------------
if 'FC_CAND' in V:
    led = {}
    for k in KEYS:
        row = {}
        for t in ('live', 'IDENT_K', 'IDENT_P', 'L0_R', 'FC_CAND'):
            if t in V and k in V[t]:
                row[t] = V[t][k]
        if 'FC_CAND' not in row:
            continue
        moved = any(row.get(t) != row['FC_CAND'] for t in ('live', 'IDENT_K', 'IDENT_P', 'L0_R') if t in row)
        if not moved:
            continue
        led[k] = dict(name=NAME.get(k), pos=POS.get(k), age=AGE.get(k), band=BAND.get(k),
                      pick=PICK.get(k), cat=CAT.get(k),
                      live=row.get('live'), K=row.get('IDENT_K'), P=row.get('IDENT_P'),
                      R=row.get('L0_R'), cand=row['FC_CAND'],
                      d_live_K=(row.get('IDENT_K') - row['live']) if 'live' in row and 'IDENT_K' in row else None,
                      d_K_P=(row.get('IDENT_P') - row.get('IDENT_K')) if 'IDENT_K' in row and 'IDENT_P' in row else None,
                      d_P_R=(row.get('L0_R') - row.get('IDENT_P')) if 'IDENT_P' in row and 'L0_R' in row else None,
                      d_R_cand=(row['FC_CAND'] - row.get('L0_R')) if 'L0_R' in row else None,
                      d_live_cand=(row['FC_CAND'] - row['live']) if 'live' in row else None,
                      d_K_cand=(row['FC_CAND'] - row.get('IDENT_K')) if 'IDENT_K' in row else None,
                      levers={t: LEVER[t]['rows'].get(k) for t in LEVER if k in LEVER[t]['rows']})
    json.dump(dict(totals=TOT, md5={t: MD5[t] for t in MD5}, n_moved=len(led), rows=led),
              open(os.path.join(HERE, 'MOVERS_LEDGER.json'), 'w'), indent=1, sort_keys=True)
    P('MOVERS LEDGER: %d rows moved by the mechanism or the repairs -> MOVERS_LEDGER.json' % len(led))

json.dump(dict(totals=TOT, md5=MD5, lever={t: {kk: vv for kk, vv in LEVER[t].items() if kk != 'rows'}
                                            for t in LEVER}, fail=FAIL),
          open(os.path.join(HERE, 'BOARDS_CP.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'BOARDS_CP_out.txt'), 'w').write('\n'.join(L) + '\n')
P()
P('written: BOARDS_CP.json · BOARDS_CP_out.txt · MOVERS_LEDGER.json')
