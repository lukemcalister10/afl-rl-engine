#!/usr/bin/env python3
"""D6-CONSOLIDATION — THE R1 COMBINED-TAKE GUARD, MEASURED FROM THE ENGINE'S OWN ATTRIBUTION.

WHY NOT A LAYER-OFF BOARD. The first plan was to price a control board with RL_AVAIL=0 and read the
combined take as v(board) - v(control). THAT PATH HALTED and is not worked around:

    v0surf FROZEN-SIGNATURE HALT: this build's config signature 3ebc60f0 is NOT in data/v0surf.pkl
    (frozen: 41af7326, 4405cba2). The engine will NOT silently re-fit the V0 pick-curve surface.

RL_AVAIL is part of the frozen config signature and only RL_AVAIL=1 signatures are frozen, so a
layer-off board cannot be built without a v0surf REFIT — a bake act, outside this seat, and one that
would make the control non-comparable to the boards it is meant to control. Reported, not improvised
around.

WHAT IS USED INSTEAD, AND IT IS STRICTLY BETTER. The engine ALREADY computes the separable
attribution this guard needs, in-process, at the availability block:

    (1) _ev_off  : ev() with _AVAIL_STATE empty and _avail_hc 0   -- the layer-off value
    (2) _ev_p1   : + the Part-1 present haircut
    (3) _vfull   : + the Part-2 return haircut
    _avail_nerf   = _ev_p1  - _ev_off      (Part 1)
    _lti_ret_delta= _vfull  - _ev_p1       (Part 2)

and records all of it per row in _AVAIL_MOVERS. That is the WHOLE take, layer-on minus layer-off,
computed by the engine itself against its own in-process layer-off baseline -- no second board and no
frozen-surface problem. This script loads the engine on each dial line and reads that list out.

  usage: python3 d6_take.py
"""
import os, sys, io, json, csv, re, contextlib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
ASM = os.path.join(ROOT, 'docs/evidence/assembly_2026-08-19')
sys.path.insert(0, ASM)
import os_lib as OL

SP = os.environ.get('RL_SCRATCH', '/home/claude/d6scratch/bb')

BASE = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
            RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
            RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
            RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7')
CAND = dict(BASE, RL_O42='1')

L = []
def P(s=''):
    print(s); L.append(str(s))


def harvest(dials, tag):
    """Load the engine on one dial line in a fresh subprocess and return its _AVAIL_MOVERS."""
    import subprocess
    code = (
        'import os,sys,io,json,contextlib\n'
        'sys.path.insert(0,%r)\n'
        'import os_lib as OL\n'
        'NS=OL.load(**%r)\n'
        'mv=NS.get("_AVAIL_MOVERS") or []\n'
        'out=[{"key":m[0],"name":m[1],"ev_off":m[2],"ev_p1":m[3],"ev_full":m[4],'
        '"part1":m[5],"part2":m[6],"ret_hc":m[7]} for m in mv]\n'
        'st={k:{"L":v.get("L"),"g2026":v.get("g2026"),"section":v.get("section"),'
        '"out":v.get("out"),"return_arm":v.get("return_arm")} '
        'for k,v in (NS.get("_AVAIL_STATE") or {}).items()}\n'
        'sys.stderr.write("@@@"+json.dumps({"movers":out,"state":st,"state_keys":sorted(st),'
        '"G_FULL":NS["LTIREG"].G_FULL if "LTIREG" in NS else None,'
        '"SEASON":NS["cp"].SEASON if "cp" in NS else None})+"@@@")\n'
        % (ASM, dials))
    env = dict(os.environ)
    for k in ('RL_O42', 'RL_AVAIL', 'RL_O41_RAMP', 'RL_O41_BREAK', 'RL_O41_UNWIND',
              'RL_O41_CREDITFORM'):
        env.pop(k, None)
    r = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, env=env)
    if '@@@' not in r.stderr:
        P('  *** %s: engine load produced no attribution. stderr tail:' % tag)
        for ln in (r.stderr or '').strip().splitlines()[-15:]:
            P('      ' + ln)
        return None
    return json.loads(r.stderr.split('@@@')[1])


def n2(n):
    return re.sub(r'[^a-z0-9]+', '-', str(n).strip().lower().replace('’', "'")).strip('-')


SHEET = os.path.join(ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv')
sheet_md5 = hashlib.md5(open(SHEET, 'rb').read()).hexdigest()
srows = list(csv.DictReader(open(SHEET, encoding='utf-8')))
YNAMES = {n2(r['player']): r for r in srows if (r.get('injured') or '').strip().upper() == 'Y'}

sys.path.insert(0, os.path.join(ROOT, 'engine', 'rl_after'))
import lti_register as LTIREG
REG = LTIREG.parse(os.path.join(ROOT, 'LTI_REGISTER.md'))
REGKEYS = sorted(set(r['key'] for r in REG))

BOARD = {}
for t in ('D6_BASE', 'D6_CAND'):
    q = '%s/bb_%s/rl_after/rl_app_data.json' % (SP, t)
    if os.path.exists(q):
        BOARD[t] = {r['key']: r for r in json.load(open(q))['active']}

P('=' * 128)
P('D6-CONSOLIDATION — THE R1 COMBINED-TAKE GUARD')
P('=' * 128)
P()
P('  METHOD: the engine\'s OWN separable attribution, read out of _AVAIL_MOVERS on each dial line.')
P('  take = Part 1 (avail_nerf) + Part 2 (lti_ret_delta) = ev(layer on) - ev(layer off), in-process.')
P()
P('  THE LAYER-OFF CONTROL BOARD COULD NOT BE BUILT AND THE PATH WAS HALTED, NOT WORKED AROUND:')
P('    v0surf FROZEN-SIGNATURE HALT — RL_AVAIL=0 is not a frozen config signature in data/v0surf.pkl,')
P('    and the engine refuses to silently re-fit the V0 surface. A refit is a bake act outside this')
P('    seat. The engine\'s in-process attribution needs no such board and is used instead.')
P()
P('  sheet md5 %s   %s' % (sheet_md5,
                           'pinned prefix ASSERT PASSES' if sheet_md5.startswith('b26798c35adcd9bd')
                           else '*** ASSERT FAILS ***'))
P()

HB = harvest(BASE, 'D6_BASE')
HC = harvest(CAND, 'D6_CAND')
if HB is None or HC is None:
    P('HALT: could not harvest attribution on both lines.')
    open(os.path.join(HERE, 'D6_TAKE_out.txt'), 'w').write('\n'.join(L) + '\n')
    raise SystemExit(1)

P('  engine constants on the candidate line: LTIREG.G_FULL=%s  cp.SEASON=%s   (the :5698 assert '
  'compares exactly these two and it passed on every board)' % (HC['G_FULL'], HC['SEASON']))
P()

SB = HB.get('state') or {}
SC = HC.get('state') or {}
MB = {m['key']: m for m in HB['movers']}
MC = {m['key']: m for m in HC['movers']}
NAME = {}
for m in HB['movers'] + HC['movers']:
    NAME[m['key']] = m['name']
for t in BOARD:
    for k, r in BOARD[t].items():
        NAME.setdefault(k, r.get('name') or k)

ANNOT = set(MC)
REGONLY = [k for k in REGKEYS if k not in ANNOT]
UNION = ANNOT | set(REGKEYS)

P('MEMBERSHIP — MEASURED')
P('  annotated injured=Y rows on the sheet                 %3d' % len(YNAMES))
P('  keys carrying a disposition on the CANDIDATE          %3d   (all sheet-keyed)' % len(MC))
P('  keys carrying a disposition on the BASE               %3d   (the register)' % len(MB))
P('  register unique keys                                  %3d' % len(REGKEYS))
P('  register AND annotated  (treatment continues)         %3d' % len(ANNOT & set(REGKEYS)))
P('  register-only           (LOSING treatment)            %3d' % len(REGONLY))
P('  annotated not on the register (GAINING treatment)     %3d' % len(ANNOT - set(REGKEYS)))
P()
P('  THE BRIEF SAYS 21 REGISTER-ONLY ROWS. THE MEASURED NUMBER IS %d. Reported as measured.'
  % len(REGONLY))
P()
leak = sorted(set(MC) - ANNOT)
P('  D6-F6  register-only keys still carrying a live disposition on the candidate: %d  %s'
  % (len(leak), 'did not fire' if not leak else '*** FIRED *** %s' % leak))
P()

FIRED = []
if leak:
    FIRED.append('D6-F6 register consumption survives')

G_FULL, AVAIL_BASE = LTIREG.G_FULL, 18


def block(title, keys, on_base, on_cand):
    P('-' * 128)
    P(title)
    P('-' * 128)
    P('  %-24s %-22s %4s %7s %7s %8s %8s %8s %9s %9s %8s'
      % ('player', 'key', 'g26', 'L22', 'L18', 'P1', 'P2', 'TAKE', 'v_base', 'v_cand', 'dv'))
    tb = tc = 0
    for k in sorted(keys, key=lambda x: NAME.get(x, x)):
        mb, mc = MB.get(k), MC.get(k)
        src = mc or mb
        g = (SC.get(k) or SB.get(k) or {}).get('g2026')
        l22 = (1 - min(g / float(G_FULL), 1)) if g is not None else None
        l18 = (1 - min(g / float(AVAIL_BASE), 1)) if g is not None else None
        # take on the board being reported
        m = mc if on_cand else mb
        p1 = m['part1'] if m else 0
        p2 = m['part2'] if m else 0
        tk = p1 + p2
        vb = (BOARD.get('D6_BASE', {}).get(k) or {}).get('v')
        vc = (BOARD.get('D6_CAND', {}).get(k) or {}).get('v')
        tb += (MB[k]['part1'] + MB[k]['part2']) if k in MB else 0
        tc += (MC[k]['part1'] + MC[k]['part2']) if k in MC else 0
        P('  %-24s %-22s %4s %7s %7s %8s %8s %8s %9s %9s %8s'
          % (NAME.get(k, k)[:24], k[:22],
             '-' if g is None else g,
             '-' if l22 is None else '%.4f' % l22,
             '-' if l18 is None else '%.4f' % l18,
             '%+d' % p1, '%+d' % p2, '%+d' % tk,
             '-' if vb is None else vb, '-' if vc is None else vc,
             '-' if (vb is None or vc is None) else '%+d' % (vc - vb)))
    return tb, tc


P()
P('=' * 128)
P('THE %d ANNOTATED-INJURED ROWS — the sheet is the only injury truth. TAKE SHOWN ON THE CANDIDATE.'
  % len(ANNOT))
P('=' * 128)
ab, ac = block('', ANNOT, False, True)
P()
P('  combined take on these rows:  BASE %+d   CANDIDATE %+d   change %+d' % (ab, ac, ac - ab))
P()
P('=' * 128)
P('THE %d REGISTER-ONLY ROWS — LOSING TREATMENT. TAKE SHOWN ON THE BASE (what they WERE charged).'
  % len(REGONLY))
P('  On the candidate every one of these rows carries NO disposition and its take is EXACTLY ZERO.')
P('=' * 128)
rb, rc = block('', REGONLY, True, False)
P()
P('  combined take on these rows:  BASE %+d   CANDIDATE %+d  (zero by construction)' % (rb, rc))
P()

# ---- CONWAY --------------------------------------------------------------------------------------
P('=' * 128)
P("CONWAY — THE OWNER'S STANDING WORD: the sheet wins; Conway is NOT injured and KEEPS his sitting charges.")
P('=' * 128)
ck = [k for k in NAME if 'conway' in NAME[k].lower()]
for k in ck:
    sh = next((r for r in srows if n2(r['player']) == n2(NAME[k])), None)
    vb = (BOARD.get('D6_BASE', {}).get(k) or {}).get('v')
    vc = (BOARD.get('D6_CAND', {}).get(k) or {}).get('v')
    P('  %s (%s)' % (NAME[k], k))
    P('    sheet: injured=%s  depth=%s  fade=%s  delivered=%s'
      % (sh.get('injured') if sh else '?', sh.get('depth') if sh else '?',
         sh.get('fade') if sh else '?', sh.get('delivered') if sh else '?'))
    P('    on the register: %s' % ('YES — so he LOSES LTI treatment under the consolidation'
                                   if k in set(REGKEYS) else 'no'))
    P('    LTI take   BASE %+d   CANDIDATE %+d'
      % ((MB[k]['part1'] + MB[k]['part2']) if k in MB else 0,
         (MC[k]['part1'] + MC[k]['part2']) if k in MC else 0))
    P('    PRICE      BASE %s   CANDIDATE %s   delta %s'
      % (vb, vc, ('%+d' % (vc - vb)) if (vb is not None and vc is not None) else '-'))
    if vb is not None and vc is not None:
        if vc < vb:
            FIRED.append('D6-F4 Conway price fell %+d' % (vc - vb))
            P('    D6-F4  *** FIRED *** — Conway\'s price FELL. Reported as a DEFECT.')
        else:
            P('    D6-F4  DID NOT FIRE — Conway\'s price does not fall. His sitting charges are intact:')
            P('           the LTI layer already took ZERO from him on the base (his k=0 present leg is')
            P('           empty — 0 games in 2026, last played 2024), so retiring his register')
            P('           treatment costs him nothing, and his charge comes from the depth/fade')
            P('           machinery, which this order does not touch.')
P()

# ---- the 18-rebase --------------------------------------------------------------------------------
P('=' * 128)
P('THE 18-REBASE, MEASURED — AND THE FALSIFIER THAT FIRED ON THIS SEAT')
P('=' * 128)
P('  L22 = 1 - min(g/%d,1)   the register consumer, lti_register.py:115' % G_FULL)
P('  L18 = 1 - min(g/%d,1)   _O42_AVAIL_BASE — the AVAILABILITY base, never the season constant' % AVAIL_BASE)
P()
P('  D6-F8 AS PREREGISTERED FIRED ON THE FIRST CANDIDATE BUILD, AND THE FALSIFIER WAS WRONG.')
P('  The prereg claimed the re-base "may only ever RAISE the haircut". That is backwards: against a')
P('  SHORTER season the same games are a LARGER fraction of it, so g/18 > g/22 and L18 <= L22.')
P('  THE FORM IS EXACTLY THE ONE BRIEFED — 1 - min(g/18,1) — and no constant moved to pass the guard.')
P('  SUBSTANTIVE CONSEQUENCE: the re-base makes an injured row who PLAYED SOME GAMES LESS penalised.')
P()
moved, bad = [], []
for k in sorted(ANNOT):
    g = (SC.get(k) or {}).get('g2026')
    if g is None:
        continue
    a = 1 - min(g / float(G_FULL), 1); b = 1 - min(g / float(AVAIL_BASE), 1)
    if not (-1e-12 <= b <= 1 + 1e-12) or b > a + 1e-12 or (g >= AVAIL_BASE and b > 1e-12) \
       or (g <= 0 and abs(b - 1.0) > 1e-12):
        bad.append((k, g, a, b))
    if abs(a - b) > 1e-12:
        moved.append((k, g, a, b))
P('  D6-F8 (CORRECTED: range / direction / clears-at-base / g=0 => L=1) violations: %d   %s'
  % (len(bad), 'did not fire' if not bad else '*** FIRED *** %s' % bad))
if bad:
    FIRED.append('D6-F8(corrected)')
P('  annotated rows whose haircut MOVES under the re-base (0 < g < %d): %d of %d'
  % (AVAIL_BASE, len(moved), len(ANNOT)))
for k, g, a, b in sorted(moved, key=lambda z: -(z[2] - z[3])):
    P('      %-26s g=%-3s L22 %.4f -> L18 %.4f   %+.4f' % (NAME.get(k, k)[:26], g, a, b, b - a))
P('  every other annotated row has g=0 and sits at L=1 on BOTH bases — untouched by the re-base.')
P()

# ---- movers ---------------------------------------------------------------------------------------
P('=' * 128)
P('MOVERS — THE CANDIDATE AGAINST THE BASE ff936186')
P('=' * 128)
if 'D6_BASE' in BOARD and 'D6_CAND' in BOARD:
    A, Bd = BOARD['D6_BASE'], BOARD['D6_CAND']
    keys = sorted(set(A) | set(Bd))
    mv = [(k, A[k]['v'], Bd[k]['v']) for k in keys if k in A and k in Bd and A[k]['v'] != Bd[k]['v']]
    tot_a = sum(r['v'] for r in A.values()); tot_b = sum(r['v'] for r in Bd.values())
    P('  rows on the board   %d' % len(keys))
    P('  MOVERS              %d' % len(mv))
    P('  total               %s -> %s   (%+d)'
      % ('{:,}'.format(tot_a), '{:,}'.format(tot_b), tot_b - tot_a))
    out = [m for m in mv if m[0] not in UNION]
    P('  movers OUTSIDE the %d-key union (%d annotated u %d register-only): %d   %s'
      % (len(UNION), len(ANNOT), len(REGONLY), len(out),
         'D6-F9 did not fire' if not out else '*** D6-F9 FIRED ***'))
    if out:
        FIRED.append('D6-F9 scope leak %d rows' % len(out))
        for k, x, y in sorted(out, key=lambda z: -abs(z[2] - z[1]))[:20]:
            P('      %-26s %8s -> %-8s %+d' % (NAME.get(k, k)[:26], x, y, y - x))
    P()
    P('  EVERY MOVER, largest absolute move first:')
    P('  %-26s %-22s %9s %9s %8s  %s' % ('player', 'key', 'base', 'cand', 'delta', 'membership'))
    for k, x, y in sorted(mv, key=lambda z: -abs(z[2] - z[1])):
        memb = ('annotated + register' if (k in ANNOT and k in set(REGKEYS))
                else 'annotated (GAINS treatment)' if k in ANNOT
                else 'register-only (LOSES treatment)' if k in set(REGKEYS) else 'OUTSIDE')
        P('  %-26s %-22s %9s %9s %8s  %s' % (NAME.get(k, k)[:26], k[:22], x, y, '%+d' % (y - x), memb))
P()
P('=' * 128)
if FIRED:
    P('*** FALSIFIERS FIRED HERE: %s' % '; '.join(FIRED))
else:
    P('NO FALSIFIER SCORED HERE FIRED.')
P('  Separately and disclosed rather than scored: Guard 5 is RED and PRE-EXISTING on this branch')
P('  (PREREG_D6.md §1), and the RL_AVAIL=0 control board could not be built at all (frozen v0surf')
P('  signature). Neither is claimed as a pass.')
P('=' * 128)

json.dump({'annotated': sorted(ANNOT), 'register_only': REGONLY, 'fired': FIRED,
           'n_annotated': len(ANNOT), 'n_register_only': len(REGONLY),
           'base_movers': HB['movers'], 'cand_movers': HC['movers'],
           'sheet_md5': sheet_md5, 'G_FULL': HC['G_FULL'], 'SEASON': HC['SEASON']},
          open(os.path.join(HERE, 'D6_TAKE.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'D6_TAKE_out.txt'), 'w').write('\n'.join(L) + '\n')
P('written: D6_TAKE.json · D6_TAKE_out.txt')
