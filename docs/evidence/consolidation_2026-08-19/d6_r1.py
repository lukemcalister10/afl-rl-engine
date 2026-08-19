#!/usr/bin/env python3
"""D6-CONSOLIDATION — THE R1 COMBINED-TAKE GUARD, THE MOVERS, AND THE FALSIFIER SCORING.

Pure JSON reads over boards already built. NO ENGINE RUN HERE.

  D6_IDENT_P  every RL_O38*/O39/O40/O41/O42 dial OFF   -> must be 374d4e44   D6-F2
  D6_IDENT_K  ORDER K's ruled line                     -> must be f3101883   chain
  D6_L0R      R20A, the owner's reference              -> must be 7f88f509   chain
  D6_BASE     the D5-final stack, RL_O42 UNSET         -> must be ff936186   D6-F1
  D6_CAND     + RL_O42=1  THE CONSOLIDATION            = THE PRICED BOARD
  D6_CAND2    determinism repeat                                              D6-F3
  D6_OFF      the D5-final stack with RL_AVAIL=0       = the layer-off control

THE COMBINED TAKE is measured against D6_OFF, the board on which the availability layer is entirely
absent. take(row) = v(board) - v(D6_OFF). That is the WHOLE take (Part 1 + Part 2) at board
resolution, read off the engine's own prices rather than re-derived from unexported internals.

NOTHING HERE IS ADOPTED. These are prices, not proposals.
"""
import json, os, csv, re, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = os.environ.get('RL_SCRATCH', '/home/claude/d6scratch/bb')

EXPECT = {'D6_IDENT_P': '374d4e44', 'D6_IDENT_K': 'f3101883',
          'D6_L0R': '7f88f509', 'D6_BASE': 'ff936186'}
ORDER = ['D6_IDENT_P', 'D6_IDENT_K', 'D6_L0R', 'D6_OFF', 'D6_BASE', 'D6_CAND', 'D6_CAND2']

L = []
def P(s=''):
    print(s); L.append(str(s))

PATHS, MD5, B, V = {}, {}, {}, {}
for t in ORDER:
    q = '%s/bb_%s/rl_after/rl_app_data.json' % (SP, t)
    if os.path.exists(q):
        PATHS[t] = q
        MD5[t] = hashlib.md5(open(q, 'rb').read()).hexdigest()
        B[t] = {r['key']: r for r in json.load(open(q))['active']}
        V[t] = {k: r['v'] for k, r in B[t].items()}
TOT = {t: sum(V[t].values()) for t in V}

# ---- the sheet and the register, as sets of store keys -------------------------------------------
def n2(n):
    return re.sub(r'[^a-z0-9]+', '-', str(n).strip().lower().replace('’', "'")).strip('-')

SHEET = os.path.join(ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv')
sheet_md5 = hashlib.md5(open(SHEET, 'rb').read()).hexdigest()
srows = list(csv.DictReader(open(SHEET, encoding='utf-8')))
YROWS = {n2(r['player']): r for r in srows if (r.get('injured') or '').strip().upper() == 'Y'}

import sys
sys.path[:0] = [os.path.join(ROOT, 'engine', 'rl_after')]
import lti_register as LTIREG
REG = LTIREG.parse(os.path.join(ROOT, 'LTI_REGISTER.md'))
REGKEYS = sorted(set(r['key'] for r in REG))
REGNAME = {r['key']: r['player'] for r in REG}

REF = B.get('D6_CAND') or B.get('D6_BASE') or {}
NAME = {k: (r.get('name') or k) for k, r in REF.items()}

# resolve the 37 annotated names -> store keys, using the engine's own normaliser
ANNOT = {}
for k, r in REF.items():
    for f in ('key', 'name'):
        val = r.get(f)
        if val and n2(val) in YROWS:
            ANNOT[k] = YROWS[n2(val)]
ANNOT_K = set(ANNOT)
REG_ONLY = [k for k in REGKEYS if k not in ANNOT_K]
UNION = ANNOT_K | set(REGKEYS)

P('=' * 124)
P('D6-CONSOLIDATION — THE INJURY CONSOLIDATION. THE BOARD IS PRICED, NOT ADOPTED.')
P('=' * 124)
P()
P('  sheet  %s  md5 %s' % ('docs/owner_annotations/SITTER_2026_v1.csv', sheet_md5))
P('         pinned prefix b26798c35adcd9bd -> %s' % ('ASSERT PASSES' if sheet_md5.startswith('b26798c35adcd9bd') else '*** ASSERT FAILS ***'))
P('         %d rows, %d annotated injured=Y' % (len(srows), len(YROWS)))
P()

# ---- boards -------------------------------------------------------------------------------------
P('THE BOARDS')
P('  %-12s %-10s %12s %12s   %s' % ('board', 'md5', 'total', 'vs BASE', 'what it is'))
NICE = {'D6_IDENT_P': 'every O38/O39/O40/O41/O42 dial OFF  = ORDER P identity',
        'D6_IDENT_K': "ORDER K's ruled line                = the K chain",
        'D6_L0R':     'R20A A+B1+p20 clip                  = the owner\'s reference',
        'D6_OFF':     'the D5-final stack, RL_AVAIL=0      = the layer-off control',
        'D6_BASE':    'the D5-final stack, RL_O42 UNSET    = THE BASE (U0=7, owner-ruled/data-supported)',
        'D6_CAND':    '+ RL_O42=1                          = THE CONSOLIDATION',
        'D6_CAND2':   'determinism repeat of D6_CAND'}
for t in ORDER:
    if t not in V:
        P('  %-12s %-10s %12s' % (t, 'NO BOARD', '-')); continue
    d = (TOT[t] - TOT['D6_BASE']) if 'D6_BASE' in TOT else None
    P('  %-12s %-10s %12s %12s   %s'
      % (t, MD5[t][:8], '{:,}'.format(TOT[t]),
         ('{:+,}'.format(d) if d is not None else '-'), NICE.get(t, '')))
P()

# ---- falsifiers on identity ----------------------------------------------------------------------
FIRED = []
P('FALSIFIERS ON IDENTITY')
for t, want in EXPECT.items():
    got = MD5.get(t, '')[:8]
    ok = (got == want)
    tag = {'D6_IDENT_P': 'D6-F2', 'D6_BASE': 'D6-F1'}.get(t, 'chain')
    if not ok:
        FIRED.append('%s (%s): %s != %s' % (t, tag, got or 'NO BOARD', want))
    P('  %-6s %-12s expected %s  got %s   %s'
      % (tag, t, want, got or 'NO BOARD', 'did not fire' if ok else '*** FIRED ***'))
if 'D6_CAND' in MD5 and 'D6_CAND2' in MD5:
    ok = MD5['D6_CAND'] == MD5['D6_CAND2']
    if not ok:
        FIRED.append('D6-F3 determinism: %s vs %s' % (MD5['D6_CAND'][:8], MD5['D6_CAND2'][:8]))
    P('  D6-F3  determinism  two identical RL_O42=1 runs  %s   %s'
      % (MD5['D6_CAND'][:8], 'IDENTICAL - did not fire' if ok else '*** FIRED ***'))
else:
    FIRED.append('D6-F3 not scorable (a repeat board is missing)')
    P('  D6-F3  determinism  NOT SCORABLE - a repeat board is missing')
P()

# ---- membership ------------------------------------------------------------------------------------
P('MEMBERSHIP — THE MEASURED CROSS')
P('  annotated injured=Y rows                              %3d' % len(YROWS))
P('  annotated rows resolved to a board row                %3d' % len(ANNOT_K))
P('  register unique keys                                  %3d  (%d rows)' % (len(REGKEYS), len(REG)))
P('  register AND annotated-Y  (treatment continues)       %3d' % len(ANNOT_K & set(REGKEYS)))
P('  register-only             (LOSING treatment)          %3d' % len(REG_ONLY))
P('  annotated-Y not on the register (GAINING treatment)   %3d' % len(ANNOT_K - set(REGKEYS)))
P()
P('  THE BRIEF SAYS 21 REGISTER-ONLY ROWS. THE MEASURED NUMBER IS %d.' % len(REG_ONLY))
P('  Reported as measured, not as briefed (PREREG_D6.md §4).')
P()

# ---- D6-F6: no register-only key may still carry a live availability disposition -------------------
cand_lti = {k for k, r in B.get('D6_CAND', {}).items() if r.get('lti_reg')}
leak = sorted(cand_lti - ANNOT_K)
P('  D6-F6  register-only keys still carrying a disposition on D6_CAND: %d   %s'
  % (len(leak), 'did not fire' if not leak else '*** FIRED *** ' + str(leak[:10])))
if leak:
    FIRED.append('D6-F6 register consumption survives: %s' % leak[:10])
sect = collections.Counter((r.get('lti_reg') or {}).get('section') for k, r in B.get('D6_CAND', {}).items() if r.get('lti_reg'))
P('  D6_CAND dispositions by section: %s   (S = sheet; A/B are register-only and must be absent)' % dict(sect))
P()

# ---- the R1 combined-take table ---------------------------------------------------------------------
def take(t, k):
    if t not in V or 'D6_OFF' not in V:
        return None
    if k not in V[t] or k not in V['D6_OFF']:
        return None
    return V[t][k] - V['D6_OFF'][k]

def row_of(t, k):
    return B.get(t, {}).get(k) or {}

G_FULL = LTIREG.G_FULL
AVAIL_BASE = 18

def g26_of(k):
    r = row_of('D6_CAND', k) or row_of('D6_BASE', k)
    lr = r.get('lti_reg') or {}
    if 'g2026' in lr:
        return lr['g2026']
    return None

P('=' * 124)
P('THE R1 COMBINED-TAKE GUARD — PER ROW. take = v(board) - v(D6_OFF), the WHOLE availability take.')
P('=' * 124)

def block(title, keys, membership):
    P()
    P(title)
    P('  %-24s %-22s %4s %7s %7s %9s %9s %9s %9s %9s'
      % ('player', 'key', 'g26', 'L22', 'L18', 'v_OFF', 'v_BASE', 'take_B', 'v_CAND', 'take_C'))
    tb = tc = 0
    for k in sorted(keys, key=lambda x: (NAME.get(x) or x)):
        nm = NAME.get(k) or REGNAME.get(k) or k
        g = g26_of(k)
        if g is None:
            sh = ANNOT.get(k)
            g = int(float((sh.get('games_2026') or 0))) if sh else None
        l22 = (1 - min(g / float(G_FULL), 1)) if g is not None else None
        l18 = (1 - min(g / float(AVAIL_BASE), 1)) if g is not None else None
        vo = V.get('D6_OFF', {}).get(k)
        vb = V.get('D6_BASE', {}).get(k)
        vc = V.get('D6_CAND', {}).get(k)
        kb, kc = take('D6_BASE', k), take('D6_CAND', k)
        if kb: tb += kb
        if kc: tc += kc
        P('  %-24s %-22s %4s %7s %7s %9s %9s %9s %9s %9s'
          % (nm[:24], k[:22],
             ('-' if g is None else g),
             ('-' if l22 is None else '%.4f' % l22),
             ('-' if l18 is None else '%.4f' % l18),
             ('-' if vo is None else vo), ('-' if vb is None else vb),
             ('-' if kb is None else '%+d' % kb),
             ('-' if vc is None else vc),
             ('-' if kc is None else '%+d' % kc)))
    P('  %-24s %-22s %4s %7s %7s %9s %9s %9s %9s %9s'
      % ('TOTAL (%d rows)' % len(keys), membership, '', '', '', '', '', '%+d' % tb, '', '%+d' % tc))
    return tb, tc

tb1, tc1 = block('THE %d ANNOTATED-INJURED ROWS — the sheet is the only injury truth' % len(ANNOT_K),
                 ANNOT_K, 'annotated')
tb2, tc2 = block('THE %d REGISTER-ONLY ROWS — LOSING TREATMENT' % len(REG_ONLY),
                 REG_ONLY, 'register-only')
P()
P('  combined take, annotated rows      base %+d   cand %+d   delta %+d' % (tb1, tc1, tc1 - tb1))
P('  combined take, register-only rows  base %+d   cand %+d   delta %+d' % (tb2, tc2, tc2 - tb2))
P()

# ---- CONWAY — the owner's standing word --------------------------------------------------------------
P('=' * 124)
P("CONWAY — THE OWNER'S STANDING WORD: the sheet wins; Conway is NOT injured and KEEPS his sitting charges.")
P('=' * 124)
ck = [k for k in REF if 'conway' in (NAME.get(k) or '').lower()]
for k in ck:
    rb, rc, ro = row_of('D6_BASE', k), row_of('D6_CAND', k), row_of('D6_OFF', k)
    P('  %s (%s)   sheet injured = %s' % (NAME.get(k), k,
      next((r['injured'] for r in srows if n2(r['player']) == n2(NAME.get(k) or '')), '?')))
    P('    v   OFF %s   BASE %s   CAND %s      delta CAND-BASE %+d'
      % (ro.get('v'), rb.get('v'), rc.get('v'), (rc.get('v', 0) - rb.get('v', 0))))
    P('    availability take   base %s   cand %s' % (take('D6_BASE', k), take('D6_CAND', k)))
    P('    lti_reg  BASE %s' % (rb.get('lti_reg')))
    P('    lti_reg  CAND %s' % (rc.get('lti_reg')))
    for fld in ('gf', 'mech', 'losd', 'pedDecay', 'g', 'cg'):
        if fld in rb or fld in rc:
            P('    %-10s BASE %-22s CAND %-22s' % (fld, rb.get(fld), rc.get(fld)))
    d = rc.get('v', 0) - rb.get('v', 0)
    if d < 0:
        FIRED.append('D6-F4 Conway: price FELL %+d' % d)
        P('    D6-F4  *** FIRED *** Conway\'s price FELL by %d. Reported as a DEFECT.' % (-d))
    else:
        P('    D6-F4  did not fire — Conway does not lose value (delta %+d).' % d)
P()

# ---- movers ------------------------------------------------------------------------------------------
P('=' * 124)
P('MOVERS — D6_CAND vs THE BASE ff936186')
P('=' * 124)
if 'D6_CAND' in V and 'D6_BASE' in V:
    keys = sorted(set(V['D6_CAND']) | set(V['D6_BASE']))
    mv = [(k, V['D6_BASE'].get(k), V['D6_CAND'].get(k)) for k in keys
          if V['D6_BASE'].get(k) != V['D6_CAND'].get(k)]
    P('  rows on the board            %d' % len(keys))
    P('  MOVERS                       %d' % len(mv))
    P('  total                        base %s -> cand %s   (%+d)'
      % ('{:,}'.format(TOT['D6_BASE']), '{:,}'.format(TOT['D6_CAND']),
         TOT['D6_CAND'] - TOT['D6_BASE']))
    inside = [m for m in mv if m[0] in UNION]
    outside = [m for m in mv if m[0] not in UNION]
    P('  movers INSIDE  the %d-key union (37 annotated u %d register-only)  %d'
      % (len(UNION), len(REG_ONLY), len(inside)))
    P('  movers OUTSIDE that union                                          %d' % len(outside))
    if outside:
        FIRED.append('D6-F9 scope leak: %d rows outside the union moved' % len(outside))
        P('  D6-F9  *** FIRED *** — %d rows outside the union moved. Largest:' % len(outside))
        for k, a, b in sorted(outside, key=lambda m: -abs((m[2] or 0) - (m[1] or 0)))[:25]:
            P('      %-26s %8s -> %-8s %+d' % (NAME.get(k, k)[:26], a, b, (b or 0) - (a or 0)))
    else:
        P('  D6-F9  did not fire — every mover is inside the union.')
    P()
    P('  EVERY MOVER, largest absolute move first:')
    P('  %-28s %-22s %10s %10s %9s  %s' % ('player', 'key', 'base', 'cand', 'delta', 'membership'))
    for k, a, b in sorted(mv, key=lambda m: -abs((m[2] or 0) - (m[1] or 0))):
        memb = ('annotated' if k in ANNOT_K else ('register-only' if k in set(REGKEYS) else 'OUTSIDE'))
        P('  %-28s %-22s %10s %10s %9s  %s'
          % (NAME.get(k, k)[:28], k[:22], a, b, '%+d' % ((b or 0) - (a or 0)), memb))
P()

# ---- the 18-rebase, measured -------------------------------------------------------------------------
P('=' * 124)
P('THE 18-REBASE, MEASURED ON THE ANNOTATED ROWS')
P('=' * 124)
P('  L22 = 1 - min(g/%d,1)   (lti_register.py:115, G_FULL=%d)' % (G_FULL, G_FULL))
P('  L18 = 1 - min(g/%d,1)   (_O42_AVAIL_BASE=%d — the AVAILABILITY base, never the season constant)'
  % (AVAIL_BASE, AVAIL_BASE))
P('  D6-F8 AS PREREGISTERED WAS WRONG AND IT FIRED ON THE FIRST CANDIDATE BUILD. The prereg claimed the')
P('  re-base "may only ever RAISE the haircut". It is the other way round: against a SHORTER season the')
P('  same games are a LARGER fraction of it, so g/18 > g/22 and L18 <= L22. The FORM is exactly the one')
P('  briefed; only the direction claimed about it was wrong. See PREREG_D6.md §11.')
P()
bad = []
moved = []
for k in sorted(ANNOT_K):
    g = g26_of(k)
    if g is None:
        continue
    l22 = 1 - min(g / float(G_FULL), 1); l18 = 1 - min(g / float(AVAIL_BASE), 1)
    if not (-1e-12 <= l18 <= 1 + 1e-12) or l18 > l22 + 1e-12 \
       or (g >= AVAIL_BASE and l18 > 1e-12) or (g <= 0 and abs(l18 - 1.0) > 1e-12):
        bad.append((k, g, l22, l18))
    if abs(l18 - l22) > 1e-12:
        moved.append((k, g, l22, l18))
P('  D6-F8 (CORRECTED)  rows violating range / direction / clears-at-base / g=0 => L=1 : %d   %s'
  % (len(bad), 'did not fire' if not bad else '*** FIRED *** ' + str(bad)))
if bad:
    FIRED.append('D6-F8(corrected) re-base form: %s' % bad[:5])
P('  rows whose haircut MOVES under the re-base (0 < g < %d): %d of %d annotated'
  % (AVAIL_BASE, len(moved), len(ANNOT_K)))
for k, g, a, b in sorted(moved, key=lambda z: -(z[2] - z[3])):
    P('      %-26s g=%-3s L22 %.4f -> L18 %.4f   %+.4f' % (NAME.get(k, k)[:26], g, a, b, b - a))
P('  every other annotated row has g=0 and is untouched at L=1 on both bases.')
P()

# ---- summary -------------------------------------------------------------------------------------------
P('=' * 124)
if FIRED:
    P('*** FALSIFIERS FIRED: %s' % '; '.join(FIRED))
else:
    P('NO FALSIFIER SCORED HERE FIRED. (Guard 5 is a disclosed pre-existing RED, not a falsifier — PREREG_D6.md §1.)')
P('=' * 124)

json.dump({'md5': {t: MD5[t] for t in MD5}, 'total': TOT, 'fired': FIRED,
           'annotated': sorted(ANNOT_K), 'register_only': REG_ONLY,
           'n_annotated': len(ANNOT_K), 'n_register_only': len(REG_ONLY),
           'sheet_md5': sheet_md5},
          open(os.path.join(HERE, 'D6_R1.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'D6_R1_out.txt'), 'w').write('\n'.join(L) + '\n')
P('written: D6_R1.json · D6_R1_out.txt')
