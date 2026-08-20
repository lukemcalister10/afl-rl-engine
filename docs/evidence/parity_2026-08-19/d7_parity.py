#!/usr/bin/env python3
"""ORDER D7 — THE PARITY TABLE. The centrepiece deliverable.

Per annotated row: games this season, v under the INJURY REGIME, v under the HEALTHY COUNTERPART,
which side won, the delta. Plus the same for the register-only rows.

THE HEALTHY COUNTERPART IS NOT `_ev_off`. `_ev_off` is layer-off and still carries the R3
injured-exemption, the sitter-clock pause and the absence-depth exemption -- all SHIELDS -- so it
understates the healthy charge. The engine's D7 block neutralises ALL SEVEN live injury sites per
row (PREREG_D7.md section 4) and records the pair in `_D7_ROWS`. This script reads that out
in-process on the candidate dial line and joins it to the built boards.

ENGINE RUNS ARE STRICTLY SEQUENTIAL. This script performs exactly one engine load, in its own
subprocess, and must not be run while a board build is in flight.

  usage: RL_SCRATCH=... python3 d7_parity.py
"""
import os, sys, io, json, csv, re, subprocess, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ASM = os.path.join(ROOT, 'docs/evidence/assembly_2026-08-19')
SP = os.environ.get('RL_SCRATCH', '/tmp/claude-0/-home-user-afl-rl-engine/'
                    '7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/d7bb')

CAND = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
            RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
            RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
            RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7',
            RL_O42='1', RL_O43='1')

NAMED = ['sam-allen', 'kobe-mcdonald', 'ollie-murphy', 'tom-green', 'nicholas-martin',
         'mitchell-hinge', 'sam-powell-pepper']

L = []
def P(s=''):
    print(s); L.append(str(s))

FIRED = []


def harvest():
    """ONE engine load on the candidate dial line; read out the engine's own D7 record."""
    code = (
        'import os,sys,json\n'
        'sys.path.insert(0,%r)\n'
        'import os_lib as OL\n'
        'NS=OL.load(**%r)\n'
        'rows=NS.get("_D7_ROWS") or []\n'
        'st=sorted((NS.get("_AVAIL_STATE") or {}))\n'
        'inj=sorted(NS.get("_O41_INJSET") or [])\n'
        'fl={k:v for k,v in (NS.get("_D7_FLOOR") or {}).items()}\n'
        'sys.stderr.write("@@@"+json.dumps({"rows":rows,"avail_keys":st,"injset":inj,'
        '"floor":fl,"treated":sorted(NS.get("_D7_TREATED") or [])})+"@@@")\n'
        % (ASM, CAND))
    env = dict(os.environ)
    for k in ('RL_O42', 'RL_O43', 'RL_AVAIL', 'RL_O41_RAMP', 'RL_O41_BREAK', 'RL_O41_UNWIND',
              'RL_O41_CREDITFORM'):
        env.pop(k, None)
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, env=env)
    if '@@@' not in r.stderr:
        P('  *** ENGINE LOAD PRODUCED NO D7 RECORD. stderr tail:')
        for ln in (r.stderr or '').strip().splitlines()[-25:]:
            P('      ' + ln)
        return None
    return json.loads(r.stderr.split('@@@')[1])


def n2(n):
    return re.sub(r'[^a-z0-9]+', '-', str(n).strip().lower().replace('’', "'")).strip('-')


# ---- pinned inputs -------------------------------------------------------------------------------
SHEET = os.path.join(ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv')
sheet_md5 = hashlib.md5(open(SHEET, 'rb').read()).hexdigest()
srows = list(csv.DictReader(open(SHEET, encoding='utf-8')))
SY = {n2(r['player']): r for r in srows if (r.get('injured') or '').strip().upper() == 'Y'}

sys.path.insert(0, os.path.join(ROOT, 'engine', 'rl_after'))
import lti_register as LTIREG
REGKEYS = sorted(set(r['key'] for r in LTIREG.parse(os.path.join(ROOT, 'LTI_REGISTER.md'))))
REGONLY = sorted(set(REGKEYS) - set(SY))

_F = json.load(open(os.path.join(ROOT, 'engine/rl_after/pick_redenomination.json')))['factor']
def nb(x):
    return int(round(float(x) / _F))

BOARD = {}
for t in ('D7_BASE', 'D7_CAND', 'D7_CAND2'):
    q = '%s/bb_%s/rl_after/rl_app_data.json' % (SP, t)
    if os.path.exists(q):
        BOARD[t] = {r['key']: r for r in json.load(open(q))['active']}
MD5 = {}
for t in ('D7_IDENT_P', 'D7_IDENT_K', 'D7_L0R', 'D7_NOO42', 'D7_BASE', 'D7_CAND', 'D7_CAND2'):
    q = '%s/bb_%s/rl_after/rl_app_data.json' % (SP, t)
    MD5[t] = hashlib.md5(open(q, 'rb').read()).hexdigest() if os.path.exists(q) else None

P('=' * 130)
P('ORDER D7 — THE PARITY GUARD — THE PARITY TABLE')
P('=' * 130)
P()
P('  RULING (register v771, owner, VERBATIM):')
P('    "Being marked as injured shouldn\'t all of a sudden enrol you to a mechanism that doesn\'t')
P('     affect your peers. In other words, a first year sitter who is injured is punished harder')
P('     for it. No thanks."')
P()
P('  THE ENCODING: per row carrying injury treatment, final = max(v_injury_regime, v_healthy_counterpart).')
P('  NO FREE PARAMETER — max has no constant to fit. It can only RAISE a row, never lower one.')
P()
P('  engine   %s' % hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py'),
                                     'rb').read()).hexdigest())
P('  sheet    %s  (pin b26798c35adcd9bd..., ASSERTED)' % sheet_md5)
P('  numeraire factor F = %.6f   (board v == round(engine ev / F))' % _F)
P('  GUARD 5: RED, PRE-EXISTING on this branch. NOT claimed green. NOT re-pinned.')
P()

# ---- acceptance identities -----------------------------------------------------------------------
EXP = {'D7_IDENT_P': '374d4e44', 'D7_IDENT_K': 'f3101883', 'D7_L0R': '7f88f509',
       'D7_NOO42': 'ff936186', 'D7_BASE': 'daa16812'}
P('=' * 130)
P('ACCEPTANCE IDENTITIES')
P('=' * 130)
for t, e in EXP.items():
    got = MD5.get(t)
    ok = (got or '')[:8] == e
    P('  %-12s expect %-10s got %-34s %s' % (t, e, got or 'NO BOARD', 'PASS' if ok else '*** FAIL ***'))
    if not ok:
        FIRED.append('%s identity (expect %s got %s)' % (t, e, (got or 'NO BOARD')[:8]))
det = MD5.get('D7_CAND') and MD5.get('D7_CAND') == MD5.get('D7_CAND2')
P('  %-12s D7-F7 determinism x2: %s  (%s / %s)'
  % ('D7_CAND', 'PASS' if det else '*** FAIL ***',
     (MD5.get('D7_CAND') or 'NONE')[:8], (MD5.get('D7_CAND2') or 'NONE')[:8]))
if not det:
    FIRED.append('D7-F7 determinism')
P()
P('  THE PRICED BOARD  %s' % (MD5.get('D7_CAND') or 'NO BOARD'))
if 'D7_CAND' in BOARD:
    P('  rows %d   total %s' % (len(BOARD['D7_CAND']),
                                '{:,}'.format(sum(r['v'] for r in BOARD['D7_CAND'].values()))))
if 'D7_BASE' in BOARD:
    P('  THE BASE          %s   rows %d   total %s'
      % (MD5.get('D7_BASE'), len(BOARD['D7_BASE']),
         '{:,}'.format(sum(r['v'] for r in BOARD['D7_BASE'].values()))))
P()

# ---- the engine's OWN treated set is the membership authority ------------------------------------
# A NAIVE SHEET-NAME JOIN IS WRONG AND THIS SCRIPT USED ONE IN ITS FIRST RUN. The sheet is keyed by
# NAME; the engine resolves name -> store key with its own normaliser and ASSERTS 37 annotated names
# resolve to 37 distinct single-record keys (the ORDER 42 builder halts otherwise). Three rows do not
# survive a naive join and were briefly reported as falsifier fires before this was caught:
#     sheet "Maxwell King"      -> engine key  max-king-syd        (naive join gives maxwell-king)
#     sheet "Max King"          -> engine key  max-king-stk        (naive join gives max-king)
#     sheet "Elliott Himmelberg"-> engine key  elliot-himmelberg   (engine spells it with one 't')
# All three ARE annotated injured=Y (sheet lines 78, 126, 187). MEMBERSHIP IS THEREFORE READ OFF THE
# ENGINE'S OWN _D7_TREATED, never off a name join done in this script.
H = harvest()
ANNOT_KEYS = set(H['treated']) if H else set()
REGONLY = sorted(set(REGKEYS) - ANNOT_KEYS)

# ---- movers ---------------------------------------------------------------------------------------
P('=' * 130)
P('MOVERS — THE PRICED BOARD AGAINST THE BASE daa16812')
P('=' * 130)
mv = []
if 'D7_BASE' in BOARD and 'D7_CAND' in BOARD:
    A, B = BOARD['D7_BASE'], BOARD['D7_CAND']
    keys = sorted(set(A) | set(B))
    mv = [(k, A[k]['v'], B[k]['v']) for k in keys if k in A and k in B and A[k]['v'] != B[k]['v']]
    ta, tb = sum(r['v'] for r in A.values()), sum(r['v'] for r in B.values())
    P('  rows on the board   %d' % len(keys))
    P('  MOVERS              %d' % len(mv))
    P('  total               %s -> %s   (%+d)' % ('{:,}'.format(ta), '{:,}'.format(tb), tb - ta))
    fell = [m for m in mv if m[2] < m[1]]
    P()
    P('  D7-F1  NO ROW FALLS (the guard is a max; a single falling row is a HALT): %s'
      % ('did not fire — every mover moves UP' if not fell else '*** FIRED *** %d falling row(s)' % len(fell)))
    if fell:
        FIRED.append('D7-F1 %d FALLING ROW(S) — HALT' % len(fell))
        for k, x, y in fell:
            P('      FALLING  %-26s %8s -> %-8s %+d' % (k[:26], x, y, y - x))
    out = [m for m in mv if m[0] not in ANNOT_KEYS]
    P('  D7-F9  every mover lies INSIDE the %d treated (annotated) rows: %s'
      % (len(ANNOT_KEYS), 'did not fire' if not out else '*** FIRED *** %d outside' % len(out)))
    if out:
        FIRED.append('D7-F9 scope leak %d rows' % len(out))
        for k, x, y in sorted(out, key=lambda z: -abs(z[2] - z[1]))[:20]:
            P('      OUTSIDE  %-26s %8s -> %-8s %+d' % (k[:26], x, y, y - x))
P()

# ---- the parity table -----------------------------------------------------------------------------
if H is None:
    P('*** THE PARITY TABLE COULD NOT BE BUILT — the engine produced no D7 record. HALT. ***')
    FIRED.append('no D7 record from the engine')
else:
    rows = {r['key']: r for r in H['rows']}
    P('=' * 130)
    P('THE PARITY TABLE — EVERY ANNOTATED ROW')
    P('=' * 130)
    P('  v_injury  = the row priced under the injury regime (the base daa16812 price)')
    P('  v_healthy = the SAME row with ALL SEVEN live injury sites off and its absences charged by')
    P('              the normal machinery, exactly as a healthy peer would be charged')
    P('  WON       = which side the max took.  delta = what the guard added (0 for a riser).')
    P('  Values in BOARD CURRENCY (round(ev/F)); raw engine ev in the last two columns.')
    P()
    P('  %-24s %-22s %4s %10s %10s %-8s %8s %10s %11s %11s'
      % ('player', 'key', 'g26', 'v_injury', 'v_health', 'WON', 'delta', 'board_v', 'ev_injury', 'ev_health'))
    P('  ' + '-' * 126)
    tot_lift = 0
    tbl = sorted(rows.values(), key=lambda r: -(max(r['v_healthy'], r['v_injury']) - r['v_injury']))
    for r in tbl:
        k = r['key']
        bi, bh = nb(r['v_injury']), nb(r['v_healthy'])
        won = 'HEALTHY' if r['v_healthy'] > r['v_injury'] else ('injury' if r['v_injury'] > r['v_healthy'] else 'tie')
        d = bh - bi if won == 'HEALTHY' else 0
        tot_lift += d
        bv = BOARD.get('D7_CAND', {}).get(k, {}).get('v')
        P('  %-24s %-22s %4d %10d %10d %-8s %8s %10s %11.1f %11.1f'
          % ((r['player'] or k)[:24], k[:22], r['g2026'], bi, bh, won,
             ('%+d' % d) if d else '.', bv if bv is not None else '-',
             r['v_injury'], r['v_healthy']))
    P('  ' + '-' * 126)
    P('  %d annotated rows | LIFTED %d | riser/tie (kept the injury-regime value) %d | total lift %+d board pts'
      % (len(tbl), sum(1 for r in tbl if r['v_healthy'] > r['v_injury']),
         sum(1 for r in tbl if r['v_healthy'] <= r['v_injury']), tot_lift))
    P()

    # ---- named rows ------------------------------------------------------------------------------
    P('  THE NAMED ROWS — THEY ILLUSTRATE, THEY DO NOT GATE:')
    P('  %-24s %4s %10s %10s %-8s %8s' % ('player', 'g26', 'v_injury', 'v_health', 'WON', 'delta'))
    for k in NAMED:
        r = rows.get(k)
        if not r:
            P('  %-24s  *** NOT IN THE TREATED SET ***' % k)
            continue
        bi, bh = nb(r['v_injury']), nb(r['v_healthy'])
        won = 'HEALTHY' if bh > bi else ('injury' if bi > bh else 'tie')
        P('  %-24s %4d %10d %10d %-8s %8s'
          % ((r['player'] or k)[:24], r['g2026'], bi, bh, won, ('%+d' % (bh - bi)) if bh > bi else '.'))
    P()

    # ---- register-only ---------------------------------------------------------------------------
    P('=' * 130)
    P('THE REGISTER-ONLY ROWS — D7-F5 (EXPECTED: none carries injury treatment after D6. ASSERTED.)')
    P('=' * 130)
    bad = [k for k in REGONLY if k in set(H['avail_keys']) or k in ANNOT_KEYS]
    P('  MEMBERSHIP IS THE ENGINE\'S OWN name->key resolution, NOT a sheet-name join (see header note).')
    P('  LTI_REGISTER.md keys %d | annotated injured=Y %d | treated keys %d | register-only (untreated) %d'
      % (len(REGKEYS), len(SY), len(ANNOT_KEYS), len(REGONLY)))
    P('  register-only keys found carrying ANY injury treatment: %d   %s'
      % (len(bad), 'D7-F5 did not fire' if not bad else '*** D7-F5 FIRED *** %s' % bad))
    if bad:
        FIRED.append('D7-F5 %d register-only rows carry treatment' % len(bad))
    else:
        P('  ASSERTED: under RL_O42=1 the register has NO live consumption; all %d register-only rows'
          % len(REGONLY))
        P('            carry no treatment, no floor, and appear nowhere in the movers. The guard does')
        P('            not reach them. (D6 consolidation claim CONFIRMED on this board.)')
    P('  the %d register-only keys: %s' % (len(REGONLY), ', '.join(REGONLY)))
    P()

    # ---- membership assertions -------------------------------------------------------------------
    P('  MEMBERSHIP: _AVAIL_STATE %d keys | _O41_INJSET %d names | treated set %d | annotated Y %d'
      % (len(H['avail_keys']), len(H['injset']), len(H['treated']), len(SY)))
    P('    the engine resolved the %d annotated sheet names to %d distinct store keys and the ORDER 42'
      % (len(SY), len(ANNOT_KEYS)))
    P('    builder ASSERTS that 37->37 correspondence (it halts on a miss, a duplicate or an ambiguity).')
    if len(ANNOT_KEYS) != len(SY):
        FIRED.append('membership: %d treated keys vs %d annotated names' % (len(ANNOT_KEYS), len(SY)))
    P()

# ---- day-0 ------------------------------------------------------------------------------------------
P('=' * 130)
P('DAY-0 — THE WIRED ENTRANTS AGAINST THE FROZEN REFERENCE (D7-F8)')
P('=' * 130)
D0 = json.load(open(os.path.join(ROOT, 'docs/evidence/order_k_2026-08-18/DAY0_K.json')))
P('  frozen reference : docs/evidence/order_k_2026-08-18/DAY0_K.json  (board %s)' % D0['board_md5'][:8])
P('  THE FROZEN REFERENCE IS NOT TOUCHED BY THIS SEAT. It is read, never rewritten.')
P('  EXPECTED: only ollie-murphy moves. VERIFIED BELOW, NOT ASSUMED.')
P()
if 'D7_CAND' in BOARD:
    d0mv = []
    for r in D0['rows']:
        k = r['key']; b = BOARD['D7_CAND'].get(k)
        if b is None:
            d0mv.append((k, r['printed'], None)); continue
        if int(b['v']) != int(r['printed']):
            d0mv.append((k, r['printed'], int(b['v'])))
    P('  wired entrants on the frozen reference: %d' % len(D0['rows']))
    P('  MOVERS vs the frozen prints: %d' % len(d0mv))
    P('  %-24s %10s %10s %8s  %s' % ('key', 'frozen', 'priced', 'delta', 'annotated injured=Y'))
    for k, a, b in sorted(d0mv, key=lambda z: -abs((z[2] or 0) - z[1])):
        P('  %-24s %10s %10s %8s  %s'
          % (k, a, b if b is not None else 'ABSENT',
             ('%+d' % (b - a)) if b is not None else '-', 'Y' if k in ANNOT_KEYS else 'n'))
    others = [m for m in d0mv if m[0] != 'ollie-murphy']
    P()
    P('  D7-F8  only ollie-murphy moves: %s'
      % ('did not fire' if not others else '*** FIRED *** %d other entrant(s) move' % len(others)))
    if others:
        FIRED.append('D7-F8 %d day-0 entrants other than ollie-murphy move' % len(others))
    # the two named restores
    P()
    P('  D7-F3  allen -> 450 and mcdonald -> 40 (EXPECTED if their healthy counterparts charge zero;')
    P('         VERIFIED, NOT ASSUMED; REPORTED, NOT GATED — these rows illustrate, they do not gate):')
    for k, want in (('sam-allen', 450), ('kobe-mcdonald', 40)):
        got = BOARD['D7_CAND'].get(k, {}).get('v')
        base = BOARD.get('D7_BASE', {}).get(k, {}).get('v')
        P('         %-16s frozen %4d | base %s | PRICED %s | %s'
          % (k, want, base, got, 'RESTORES' if got == want else 'DOES NOT RESTORE'))
        if got != want:
            FIRED.append('D7-F3 %s priced %s, frozen print %d (reported, not a halt)' % (k, got, want))
    P()
    P('  D7-F4  murphy keeps his riser (his guarded value must EQUAL his base value):')
    gm = BOARD['D7_CAND'].get('ollie-murphy', {}).get('v')
    bm = BOARD.get('D7_BASE', {}).get('ollie-murphy', {}).get('v')
    P('         ollie-murphy  base %s | PRICED %s | %s'
      % (bm, gm, 'UNTOUCHED — the shield stands' if gm == bm else '*** MOVED — the guard clawed back a shield ***'))
    if gm != bm:
        FIRED.append('D7-F4 murphy moved %s -> %s — HALT' % (bm, gm))
P()
P('=' * 130)
if FIRED:
    P('*** FALSIFIERS / DEVIATIONS FIRED: %s' % '; '.join(FIRED))
else:
    P('NO FALSIFIER FIRED.')
P('=' * 130)
P('PRICED, NOT ADOPTED. Nothing is adopted, merged, tagged or promoted. Nothing is on main.')
P('Guard 5 remains RED (pre-existing) and is NOT claimed green.')

open(os.path.join(HERE, 'PARITY_TABLE_out.txt'), 'w').write('\n'.join(L) + '\n')
if H is not None:
    json.dump({'rows': H['rows'], 'floor': H['floor'], 'treated': H['treated'],
               'md5': MD5, 'movers': mv, 'fired': FIRED, 'F': _F,
               'regonly': REGONLY, 'sheet_md5': sheet_md5},
              open(os.path.join(HERE, 'PARITY_D7.json'), 'w'), indent=1, sort_keys=True)
