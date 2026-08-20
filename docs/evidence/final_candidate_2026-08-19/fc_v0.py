#!/usr/bin/env python3
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
             RL_O42='1')

P('=' * 118)
P('THE ENTRY PRICE v0, ON THE CANDIDATE\'S OWN DIAL LINE (RL_O42=1)')
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
GUARD = {'sam-allen': 791.8152857422534,
         'ollie-murphy': 398.35828513161437,
         'kobe-mcdonald': 87.02989219418069}
P('SELF-CHECK — the three rows the ORDER 31-F day-0 guard named must reproduce EXACTLY.')
P('  %-18s %22s %22s %8s' % ('key', 'guard printed', 'read here', 'agree'))
bad = 0
for k, want in GUARD.items():
    got = V0.get(k)
    ok = (got is not None and abs(got - want) == 0.0)
    bad += (not ok)
    P('  %-18s %22.10f %22s %8s'
      % (k, want, ('%.10f' % got) if got is not None else 'MISSING', 'yes' if ok else '*** NO ***'))
if bad:
    P()
    P('*** SELF-CHECK FAILED. No v0 column is written. ***')
    open(os.path.join(HERE, 'V0_FC_out.txt'), 'w').write('\n'.join(OUT) + '\n')
    raise SystemExit(1)
P('  all three reproduce at tolerance 0.')
P()

json.dump(dict(engine=hashlib.md5(open(os.path.join(REPO, 'engine/rl_after/_merged_recover.py'),
                                       'rb').read()).hexdigest(),
               dials=DIALS, pl_f=_PL_F, n=len(V0), n_no_object=none_ct, v0=V0),
          open(os.path.join(HERE, 'V0_FC.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(HERE, 'V0_FC_out.txt'), 'w').write('\n'.join(OUT) + '\n')
P('written: V0_FC.json · V0_FC_out.txt')
