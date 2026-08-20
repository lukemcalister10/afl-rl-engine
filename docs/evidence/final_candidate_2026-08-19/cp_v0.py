#!/usr/bin/env python3
"""COMPLETION PASS — THE ENTRY PRICE v0 FOR EVERY ROW, ON THE PARITY BOARD'S OWN DIAL LINE.

fc_v0.py carried with THREE declared changes: RL_O43=1 added to the dial line, the SELF-CHECK re-keyed
to the SIX rows the D7 parity harness named (their derived_v0 is BIT-IDENTICAL to the frozen
reference -- assertion A2 of the day-0 regeneration proved 89 of 89, so these are the right numbers to
check against), and the output names. Everything else -- the byte-carried _landed_v0_board, the
none-counting, the halt -- is unchanged.

ORIGINAL FINAL-CANDIDATE HEADER FOLLOWS.
"""
"""FINAL-CANDIDATE — THE ENTRY PRICE v0 FOR EVERY ROW, ON THE CANDIDATE'S OWN DIAL LINE.

WHY THIS FILE EXISTS. The year-1 page prints a v0 column, and an EMPTY v0 column was one of the five
defects the owner caught in an earlier delivery. The assembly page sourced v0 from the candidate's
walk-forward matrix. THIS candidate has no walk-forward matrix: the emit HALTS on the ORDER 31-F
day-0 replication guard (3 of 89 wired entrants move under RL_O42=1 — see PACKET_FINAL §4).

THE WRONG FIX WOULD BE TO BORROW THE BASE'S v0, AND IT IS MEASURABLY WRONG. v0 is NOT dial-invariant:
`_landed_v0_board` reads `_V2J['nd_v0']['posv']` and `MA.pool_v0_of`, both of which come out of the
ENGINE NAMESPACE and therefore move with the dial line. On the three rows the emit guard named, the
base reads 833.3 / 419.2 / 91.6 and the candidate reads 791.815... / 398.358... / 87.030... .
Borrowing the base column would have printed a v0 that is not this board's.

WHAT THIS DOES INSTEAD. It loads the engine ONCE on the candidate's own full dial line and evaluates
`_landed_v0_board` — BYTE-CARRIED from docs/evidence/candidate_31f/emit_matrix_31f.py:105-116, not
re-implemented — for every active row. Read-only on the engine and on the store. No board is rebuilt
and no reference file is regenerated.

SELF-CHECK, PRINTED. The three rows the ORDER 31-F guard named are re-read here and must reproduce
the guard's own numbers at tolerance 0. If they do not, this file HALTS rather than write a column.

  usage: python3 fc_v0.py
"""
import io, json, os, sys, hashlib, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import os_lib as L

REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/fc'
OUT = []


def P(s=''):
    print(s); OUT.append(str(s))


# the candidate's own full dial line
DIALS = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
             RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
             RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
             RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7',
             RL_O42='1', RL_O43='1')

P('=' * 118)
P('THE ENTRY PRICE v0, ON THE PARITY BOARD a05fe951 (RL_O42=1 RL_O43=1)')
P('=' * 118)
P('  engine  %s' % hashlib.md5(open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py'),
                                    'rb').read()).hexdigest()[:8])
P('  dials   %s' % ' '.join('%s=%s' % (k, v) for k, v in sorted(DIALS.items())))

NS = L.load(**DIALS)
MA = NS['_MA']
_PL_F = NS['_PL_F']
_V2J = NS['_V2J']
_POSV = {_g: {int(_k): float(_v) for _k, _v in _d.items()}
         for _g, _d in _V2J['nd_v0']['posv'].items()}


# ---- BYTE-CARRIED from emit_matrix_31f.py:105-116. Not re-implemented, not adapted. ---------------
def _landed_v0_board(p):
    """The row's OWN derived day-0 v0 in BOARD currency, by the ORDER 29B law. Returns None when the
    row is not an entrant object under the law — the caller COUNTS that, never defaults it."""
    if p.get('_pool'):
        return float(MA.pool_v0_of(p))           # the ONE accessor; halts on an unsigned cell
    _pk = p.get('pick')
    if p.get('type') == 'ND' and _pk and 1 <= int(_pk) <= MA.ND_CURVE_LAST:
        _row = _POSV.get(MA.gfut(p))
        if _row is None:
            return None                          # a position the artifact does not publish
        return float(_row[int(_pk)])
    return None


V0 = {}
none_ct = 0
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        v = _landed_v0_board(p)
        if v is None:
            none_ct += 1
        else:
            V0[p['key']] = v

P('  rows with a v0 object : %d' % len(V0))
P('  rows with NO v0 object (not an entrant under the law — COUNTED, never defaulted): %d' % none_ct)
P()

# ---- SELF-CHECK against the ORDER 31-F guard's own printed numbers --------------------------------
# The SIX rows the D7 parity harness named, PLUS the two the guard restores. Their derived_v0 is
# BIT-IDENTICAL to DAY0_K.json (regeneration assertion A2: 89 of 89), so the expected values are READ
# STRAIGHT OUT OF THE FROZEN REFERENCE rather than transcribed into this file. Transcribing them by
# hand cost this seat a false "*** NO ***" on three rows whose values were correct to every digit the
# print showed -- a decimal literal is not the float. The file now cannot disagree with the reference
# about what the reference says.
_REFP = os.path.join(REPO, 'docs/evidence/order_k_2026-08-18/DAY0_K.json')
_REFBY = {r['key']: r for r in json.load(open(_REFP))['rows']}
NAMED8 = ('harley-barker', 'blake-thredgold', 'max-king-syd', 'liam-hetherton',
          'ollie-murphy', 'noah-chamberlain', 'sam-allen', 'kobe-mcdonald')
GUARD = {k: _REFBY[k]['derived_v0'] for k in NAMED8}
P('SELF-CHECK — the six rows the D7 parity harness named, plus the two it restores, must reproduce')
P('EXACTLY the derived_v0 the FROZEN reference carries (read from %s, not transcribed).'
  % os.path.relpath(_REFP, REPO))
P('  %-18s %22s %22s %8s' % ('key', 'guard printed', 'read here', 'agree'))
bad = 0
for k in NAMED8:
    want = GUARD[k]
    got = V0.get(k)
    ok = (got is not None and abs(got - want) == 0.0)
    bad += (not ok)
    P('  %-18s %22.10f %22s %8s'
      % (k, want, ('%.10f' % got) if got is not None else 'MISSING', 'yes' if ok else '*** NO ***'))
if bad:
    P()
    P('*** SELF-CHECK FAILED. No v0 column is written. ***')
    open(os.path.join(HERE, 'V0_CP_out.txt'), 'w').write('\n'.join(OUT) + '\n')
    raise SystemExit(1)
P('  all eight reproduce at tolerance 0.')
P()

json.dump(dict(engine=hashlib.md5(open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py'),
                                       'rb').read()).hexdigest(),
               dials=DIALS, pl_f=_PL_F, n=len(V0), n_no_object=none_ct, v0=V0),
          open(os.path.join(HERE, 'V0_CP.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'V0_CP_out.txt'), 'w').write('\n'.join(OUT) + '\n')
P('written: V0_CP.json · V0_CP_out.txt')
