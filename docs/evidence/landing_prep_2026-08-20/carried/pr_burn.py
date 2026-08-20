#!/usr/bin/env python3
"""THE BURN CENSUS, R3-LIVE AND RL_O43-LIVE — on the candidate's own dial line.

THE QUESTION (unchanged from os_census.py §1): hold output and games fixed, lower ONLY the row's
entry price in 2% steps, and ask whether any LOWER entry price prices the row HIGHER. Any row for
which it does is BURNED — the board pays him for being cheaper.

WHY IT COULD NOT BE RUN ON THE CANDIDATE BEFORE. os_census.py reconstructs the price analytically as

    price(v) = [rho31(g)*e + age_credit] + pi_base * (v * _PL_F) * factor(v)

and asserts that identity against the engine at 1e-6. That identity carries NO absence-collector
term and NO parity max, so on an R3-live board the assert fires and on an RL_O43 board it would be
wrong on every treated row even if it did not. build_FC_nor3.sh says so in as many words, and the
assembly and FC seats therefore ran their burn censuses on an R3-OFF line — a different board from
the one the owner is being asked to accept.

WHAT THIS DOES INSTEAD. It runs the SAME sweep but re-prices each step THROUGH ev() itself, with the
RL_O43 parity max re-taken at every step. There is no reconstructed identity to be wrong, so R3, the
O42 consolidation and the O43 guard are all carried exactly, and the census runs on THE CANDIDATE.

The population, the 2% step, the v0 floor of 30, the band cut and BOTH reported populations are
os_census.py's, unchanged, so the numbers are comparable with the ones already on the record.

GUARD, build-failing: at step 0 (scale 1.0) the swept price must equal the built board's own value
for that row, on every row in the population. If the sweep cannot reproduce the board at rest it
cannot be believed anywhere else.

usage: LINE=CAND python3 pr_burn.py
"""
import io, os, sys, json, time, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pr_lib as PR
import os_lib as L

LINE = os.environ.get('LINE', 'CAND')
CFG = {'CAND': (PR.DIALS, 'D7B_CAND', True),
       'HIST': (PR.DIALS_HIST, 'MY_V755_CAND', False)}[LINE]
dials, ctag, o43 = CFG
STEP, FLOOR_V0 = 0.98, 30.0
OUT = []


def P(s=''):
    print(s)
    OUT.append(str(s))


CAND, mC = PR.board(ctag)
M = PR.Model(dials, o43=o43)
NS = M.NS
# os_lib's leg recorder, chained OUTSIDE this seat's mode switch, purely to obtain the effective
# charge factors f_K_eff / f_P37_eff the supervisor's population is defined by. It records and then
# delegates; it changes no arithmetic.
NS['_REC'] = L.install_recorder(NS)
M.recording = False
SC = NS.get('_O37_SCACHE')
PC = NS.get('_O38_PCACHE')
orig = NS['day0_v0']
PLF = NS['_PL_F']


def clear():
    if SC is not None:
        SC.clear()
    if PC is not None:
        PC.clear()


def priced(p):
    clear()
    return PR.bint(M.price(p, 'on')[0])


with contextlib.redirect_stdout(io.StringIO()):
    for p in M.MA.players:
        NS['ev'](p, 2026)
ROWS = {p['key']: L.assemble(NS, p, 2026) for p in M.MA.players}
NS['_REC'] = {}          # stop recording; the sweep would otherwise grow it without bound

P('=' * 112)
P('THE BURN CENSUS — R3-LIVE, RL_O42-LIVE, RL_O43-LIVE.  LINE=%s   board %s' % (LINE, mC))
P('=' * 112)
P('  RL_O42 %s · RL_O43 %s · treated %d · lifted %d · step %.2f · v0 floor %.0f · _F %.4f'
  % (NS.get('_O42'), NS.get('_O43'), len(M.TREATED), len(M.D7_FLOOR), STEP, FLOOR_V0, PR._F))


def band(pick, pool):
    if pool or not pick:
        return 'pool'
    k = int(pick)
    return ('1-10' if k <= 10 else '11-20' if k <= 20 else '21-30' if k <= 30
            else '31-40' if k <= 40 else '41+')


# os_census.py's population, verbatim.
POP = [p for p in M.MA.players
       if p.get('_by') and (2026 - int(p['_by'])) < 24 and NS['pv_games'](p, 2026) > 0
       and (p.get('type') == 'ND' or p.get('_pool')) and ROWS[p['key']]['ped'] is not None]
P('  population: %d young rows (os_census.py\'s own selector, unchanged)' % len(POP))
P()

TGT = {'p': None, 's': 1.0}
NS['day0_v0'] = lambda p, _o=orig: (_o(p) * TGT['s'] if (_o(p) is not None and p is TGT['p'])
                                    else _o(p))
res = []
gbad = []
t0 = time.time()
for i, p in enumerate(POP):
    k = p['key']
    v0 = orig(p)
    TGT['p'] = p
    s = 1.0
    path = []
    while True:
        TGT['s'] = s
        path.append((s, v0 * s, priced(p)))
        if v0 * s * STEP < FLOOR_V0:
            break
        s *= STEP
    TGT['p'] = None
    TGT['s'] = 1.0
    clear()
    r0v = path[0][2]
    if r0v != CAND[k]['v']:                    # THE GUARD
        gbad.append((k, CAND[k]['v'], r0v))
    j = max(range(len(path)), key=lambda x: path[x][2])
    bv = path[j][2]
    rr = ROWS[k]
    res.append(dict(key=k, name=p.get('player'), pick=p.get('pick'), pool=bool(p.get('_pool')),
                    band=band(p.get('pick'), p.get('_pool')), age=2026 - int(p['_by']),
                    g=NS['pv_games'](p, 2026), v0=v0, price_board=r0v, best_board=bv,
                    best_v0=path[j][1], burn_board=max(0, bv - r0v), nsteps=len(path),
                    treated=bool(k in M._treated_set), lifted=bool(k in M.D7_FLOOR),
                    fK=rr['f_K_eff'], fP37=rr['f_P37_eff']))
NS['day0_v0'] = orig
clear()
P('GUARD — at scale 1.0 the sweep reproduces the built board : %d of %d rows exact%s'
  % (len(POP) - len(gbad), len(POP), '' if not gbad else '   *** %d WRONG ***' % len(gbad)))
for g in gbad[:8]:
    P('     %s  board %d  swept %d' % g)
P('  (%d full-engine prices in %.0f s)' % (sum(r['nsteps'] for r in res), time.time() - t0))
P()

if gbad:
    P('*** THE GUARD FAILED. This census says NOTHING and is reported as a failure. ***')
else:
    SEL = [r for r in res if abs(r['fK'] - r['fP37']) >= 0.02]
    for nm, POPX in (("the supervisor's population (|fK-fP|>=0.02)", SEL), ('all young rows', res)):
        P('  -- %s, n=%d' % (nm, len(POPX)))
        P('     %-8s %5s %7s %11s' % ('band', 'n', 'burned', 'pts(board)'))
        tb = tp = 0
        for b in ('1-10', '11-20', '21-30', '31-40', '41+', 'pool'):
            sset = [r for r in POPX if r['band'] == b]
            bn = [r for r in sset if r['burn_board'] > 0]
            P('     %-8s %5d %7d %11d' % (b, len(sset), len(bn),
                                          sum(r['burn_board'] for r in bn)))
            tb += len(bn)
            tp += sum(r['burn_board'] for r in bn)
        P('     %-8s %5d %7d %11d' % ('TOTAL', len(POPX), tb, tp))
        P()
    P('  worst five (all young rows):')
    shown = 0
    for r in sorted(res, key=lambda z: -z['burn_board'])[:5]:
        if r['burn_board'] <= 0:
            P('     (none — the census is ZERO)')
            break
        shown += 1
        P('     %-24s %-5s age %2d %4.0fg  v0 %6.0f -> %6.0f   %6d -> %6d  (+%d)%s'
          % (r['name'][:24], r['pick'] if not r['pool'] else 'pool', r['age'], r['g'], r['v0'],
             r['best_v0'], r['price_board'], r['best_board'], r['burn_board'],
             '  [D7 %s]' % ('LIFTED' if r['lifted'] else 'shield') if r['treated'] else ''))
    P()
    nt = sum(1 for r in res if r['treated'])
    P('  D7-treated rows inside this population: %d (%d lifted)'
      % (nt, sum(1 for r in res if r['lifted'])))

json.dump(dict(line=LINE, board=mC, guard_failures=gbad, burn=res),
          open(os.path.join(HERE, 'PR_BURN_%s.json' % LINE), 'w'), indent=1)
open(os.path.join(HERE, 'PR_BURN_%s_out.txt' % LINE), 'w').write('\n'.join(OUT) + '\n')
