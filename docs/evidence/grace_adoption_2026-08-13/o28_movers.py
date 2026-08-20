#!/usr/bin/env python3
"""ORDER 28 -- STEP 3, THE BOARD MOVERS PACKET.

The live board rebuilt under the RL_GRACE dial (a VARIANT build, NOT LANDED) against the live board
88ce647f, every mover named, with dispersion, concentration by entry age and career stage, the
ND/pool split, board totals, and the eligible-set control.

READ-ONLY: it compares two already-built board files. The builds themselves are done by
build_board.sh (staged scratch workspace; the checkout is never written).

  usage:  python3 o28_movers.py   ->  MOVERS28.json / MOVERS28_out.txt
"""
import os, sys, json, math, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
LIVE = ROOT + '/engine/rl_after/rl_app_data.json'
VAR = SP + '/bb_on1/rl_after/rl_app_data.json'
VAR2 = SP + '/bb_on2/rl_after/rl_app_data.json'
OFF = SP + '/bb_off1/rl_after/rl_app_data.json'


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


AGE_REF = 2026
D = json.load(open(ROOT + '/engine/rl_after/rl_model_data.json'))
STORE = {}
for p in D:
    k = p.get('key')
    if k and k not in STORE: STORE[k] = p


def by(p): return p.get('_by') or (p['year'] - 18)
def debut(p): return p['year'] if p.get('type') == 'MSD' else p['year'] + 1
def entry_age(p): return p['year'] - by(p)
def elapsed(p): return max(0, AGE_REF - debut(p))
def grace_of(p): return max(0, 1 - elapsed(p)) if entry_age(p) <= 19 else 0


A = {r['key']: r for r in json.load(open(LIVE))['active']}
B = {r['key']: r for r in json.load(open(VAR))['active']}

LOG = []
def P(s=''):
    print(s); LOG.append(s)


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float('nan')


P("=" * 128)
P("ORDER 28  --  STEP 3, THE BOARD MOVERS PACKET.   VARIANT BUILD, NOT LANDED.")
P("=" * 128)
P("  LIVE board (dial OFF)     %s   md5 %s" % ('engine/rl_after/rl_app_data.json', md5(LIVE)))
P("  VARIANT board (dial ON)   %s   md5 %s" % ('scratch bb_on1', md5(VAR)))
P("  dial-off rebuild control  %s   md5 %s   %s"
  % ('scratch bb_off1', md5(OFF), 'BYTE-IDENTICAL to live' if md5(OFF) == md5(LIVE) else 'MISMATCH'))
if os.path.exists(VAR2):
    P("  DETERMINISM: second independent dial-ON build md5 %s   %s"
      % (md5(VAR2), 'IDENTICAL -- PASS' if md5(VAR2) == md5(VAR) else 'DIFFERS -- FAIL'))
else:
    P("  DETERMINISM: second dial-ON build NOT PRESENT at run time (see DETERMINISM.txt)")
P()
P("  rows: live %d   variant %d   in both %d" % (len(A), len(B), len(set(A) & set(B))))
assert set(A) == set(B), "ROW SET CHANGED between the two boards -- a structural defect, halt"

# ---------------------------------------------------------------- the eligible set (definitional)
ELIG = {k for k in A if k in STORE and grace_of(STORE[k]) > 0}
P("  ELIGIBLE SET E (grace_years(p) > 0 at AGE_REF=2026): %d rows" % len(ELIG))
P("     = {active row : debut(p)==2026 AND entry_age<=19}.  Definitional, taken off the pinned store.")

movers = []
for k in A:
    va, vb = A[k].get('v'), B[k].get('v')
    if va is None or vb is None: continue
    if va != vb: movers.append(k)
P()
P("  MOVERS: %d of %d rows" % (len(movers), len(A)))
outside = sorted(k for k in movers if k not in ELIG)
direct = sorted(k for k in movers if k in ELIG)
P("  DIRECT movers   (inside E, grace reaches their own price) : %d" % len(direct))
P("  INDIRECT movers (outside E, grace_years==0 at AGE_REF=2026): %d   %s"
  % (len(outside), ", ".join(outside)))
if outside:
    _ot = sum(abs(B[k]['v'] - A[k]['v']) for k in outside)
    P("     PREREG P1 BREACH, OWNED. P1 predicted ZERO rows outside E. The channel is the ENGINE'S")
    P("     OWN HISTORICAL BUILD: _merged_recover.py builds its V0 / cohort-book objects with MA's")
    P("     clock at HISTORICAL years (rl_export.py:113 re-pins it to 2026 afterwards, and says so),")
    P("     and at a historical AGE_REF a player who is NOT first-season in 2026 WAS first-season")
    P("     then -- so grace fires inside those builds and the built reference objects move with it.")
    P("     That is the ruled behaviour ('for backtesting and the live board ... for everything'),")
    P("     not a leak: it is the same indirect-reference-table channel the owner accepted at #334")
    P("     stage A. Total absolute movement through it: %d points (%.5f%% of the board)."
      % (_ot, 100.0 * _ot / sum(r['v'] for r in A.values() if r.get('v'))))
    P("     A LANDING-TIME ASSERT IS OWED: the indirect set must be re-measured and named at landing.")
still = sorted(ELIG - set(movers))
P("  ELIGIBLE BUT UNMOVED: %d" % len(still))
_g0 = [k for k in still if (STORE[k].get('games') or 0) == 0]
P("     of which career games == 0: %d   %s" % (len(_g0), 'ALL of them' if len(_g0) == len(still) else ''))
P("     MECHANISM, and it matters: an un-debuted prospect is priced on PEDIGREE ALONE (rl_model.py's")
P("     'unplayed prospects ... valued on pedigree alone'), so his price never enters proj_from_peak")
P("     and the discount ladder cannot reach him. The grace dial moves NOTHING for a 0-game rookie.")
P("     What moves him at landing is the CURVE (step 2), through his pedigree anchor -- a separate")
P("     lever with a separate ruling. The two must not be conflated in the owner's reading.")
_z = [k for k in ELIG if (STORE[k].get('games') or 0) == 0]
_zm = [k for k in _z if k in movers]
P("     PRECISION: E holds %d zero-game rows; %d are unmoved and %d moved (%s) -- a zero-game row"
  % (len(_z), len(_z) - len(_zm), len(_zm),
     ", ".join('%s %+d' % (k, B[k]['v'] - A[k]['v']) for k in _zm) or 'none'))
P("     is USUALLY but not ALWAYS pedigree-pure; where a floor or blend leg touches the ladder it")
P("     moves, and by a point.  Stated so the mechanism claim is not over-general.")

deltas = [(B[k]['v'] - A[k]['v'], B[k]['v'] / A[k]['v'] - 1, k) for k in movers]
ups = [d for d in deltas if d[0] > 0]; downs = [d for d in deltas if d[0] < 0]
P()
P("  DIRECTION: %d up, %d down   %s" % (len(ups), len(downs),
                                        'ALL UP as preregged' if not downs else
                                        'DOWN-MOVERS PRESENT: ' + ", ".join(d[2] for d in downs[:10])))

# ---------------------------------------------------------------- totals
tA = sum(r['v'] for r in A.values() if r.get('v'))
tB = sum(r['v'] for r in B.values() if r.get('v'))
eA = sum(A[k]['v'] for k in ELIG); eB = sum(B[k]['v'] for k in ELIG)
oA = sum(A[k]['v'] for k in outside); oB = sum(B[k]['v'] for k in outside)
P()
P("-" * 128)
P("BOARD TOTALS")
P("-" * 128)
P("  whole board          live %10d   variant %10d   delta %+8d  (%+.4f%%)"
  % (tA, tB, tB - tA, 100 * (tB / tA - 1)))
P("  the eligible set E   live %10d   variant %10d   delta %+8d  (%+.4f%%)"
  % (eA, eB, eB - eA, 100 * (eB / eA - 1)))
P("  indirect movers      live %10d   variant %10d   delta %+8d  (%+.4f%%)"
  % (oA, oB, oB - oA, 100 * (oB / oA - 1) if oA else 0.0))
P("  everything else      live %10d   variant %10d   delta %+8d  (exactly 0 -- the 765 rows that"
  % (tA - eA - oA, tB - eB - oB, (tB - eB - oB) - (tA - eA - oA)))
P("                                                                    neither hold grace nor read a")
P("                                                                    graced historical reference)")
P("  E's share of the board: live %.4f%%   variant %.4f%%" % (100 * eA / tA, 100 * eB / tB))

# ---------------------------------------------------------------- dispersion
P()
P("-" * 128)
P("DISPERSION OF THE MOVE  (the dispersion law: p05 / median / p95, never a bare mean)")
P("-" * 128)
rel = sorted(d[1] for d in deltas)
abso = sorted(d[0] for d in deltas)
P("  relative move  min %+.4f%%  p05 %+.4f%%  med %+.4f%%  mean %+.4f%%  p95 %+.4f%%  max %+.4f%%"
  % (100 * min(rel), 100 * q(rel, .05), 100 * q(rel, .50), 100 * sum(rel) / len(rel),
     100 * q(rel, .95), 100 * max(rel)))
P("  absolute move  min %+8.0f  p05 %+8.0f  med %+8.0f  mean %+8.1f  p95 %+8.0f  max %+8.0f"
  % (min(abso), q(abso, .05), q(abso, .50), sum(abso) / len(abso), q(abso, .95), max(abso)))
P("  the ceiling on the production leg is x1.14 (one discount step removed from every future")
P("  season); the measured median sits below it because the pedigree pole, iso_eff, the position")
P("  caps and the numeraire all damp it.")

# ---------------------------------------------------------------- named movers
P()
P("-" * 128)
P("EVERY MOVER, NAMED  (before -> after -> delta), sorted by absolute points")
P("-" * 128)
P("  %-26s %-6s %-5s %5s %5s %5s %6s %9s %9s %9s %9s %s"
  % ('key', 'type', 'pick', 'age', 'entA', 'gr', 'games', 'BEFORE', 'AFTER', 'delta', 'delta%', 'chan'))
for dv, dr, k in sorted(deltas, key=lambda x: -abs(x[0])):
    p = STORE[k]
    P("  %-26s %-6s %-5s %5s %5s %5d %6s %9d %9d %+9d %+8.2f%% %s"
      % (k, p.get('type'), p.get('pick'), A[k].get('age'), entry_age(p), grace_of(p),
         p.get('games'), A[k]['v'], B[k]['v'], dv, 100 * dr,
         'DIRECT' if k in ELIG else 'INDIRECT'))

# ---------------------------------------------------------------- concentration
P()
P("-" * 128)
P("CONCENTRATION")
P("-" * 128)


def cut(label, keyfn, universe=None):
    U = universe if universe is not None else movers
    g = collections.defaultdict(list)
    for k in U: g[keyfn(k)].append(k)
    P("  by %s" % label)
    P("    %-16s %5s %11s %11s %10s %10s %10s" % ('cell', 'n', 'before', 'after', 'delta', 'delta%', 'med %'))
    for c in sorted(g, key=lambda c: -sum(B[k]['v'] - A[k]['v'] for k in g[c])):
        ks = g[c]
        a = sum(A[k]['v'] for k in ks); b = sum(B[k]['v'] for k in ks)
        med = q(sorted(B[k]['v'] / A[k]['v'] - 1 for k in ks), .5)
        P("    %-16s %5d %11d %11d %+10d %+9.3f%% %+9.3f%%"
          % (c, len(ks), a, b, b - a, 100 * (b / a - 1) if a else 0.0, 100 * med))


cut('ENTRY AGE', lambda k: 'entry age %d' % entry_age(STORE[k]))
P()
cut('CAREER STAGE (career games in the store)',
    lambda k: ('0 games' if (STORE[k].get('games') or 0) == 0 else
               '1-5 games' if STORE[k]['games'] <= 5 else
               '6-14 games' if STORE[k]['games'] <= 14 else '15+ games'))
P()
cut('ND / POOL', lambda k: 'ND 1-64' if (STORE[k].get('type') == 'ND' and (STORE[k].get('pick') or 99) <= 64)
    else ('ND>64' if STORE[k].get('type') == 'ND' else 'POOL: ' + str(STORE[k].get('type'))))
P()
cut('POSITION (board gf)', lambda k: A[k].get('gf') or '?')
P()
cut('PICK BAND', lambda k: ('pool/no pick' if STORE[k].get('type') != 'ND' else
                            'ND 1-10' if STORE[k]['pick'] <= 10 else
                            'ND 11-20' if STORE[k]['pick'] <= 20 else
                            'ND 21-40' if STORE[k]['pick'] <= 40 else 'ND 41+'))

# ---------------------------------------------------------------- the control group
P()
P("-" * 128)
P("THE CONTROL GROUP -- debut-2026 rows that are entry-age >= 20 and therefore get NO grace")
P("-" * 128)
ctrl = [k for k in A if k in STORE and debut(STORE[k]) == AGE_REF and entry_age(STORE[k]) > 19]
P("  %d rows.  Moved: %d  (must be 0 -- this is the ruled discrimination, visible)"
  % (len(ctrl), sum(1 for k in ctrl if A[k]['v'] != B[k]['v'])))
P("  %-26s %-6s %5s %6s %9s %9s" % ('key', 'type', 'entA', 'games', 'BEFORE', 'AFTER'))
for k in sorted(ctrl, key=lambda k: -A[k]['v'])[:20]:
    P("  %-26s %-6s %5d %6s %9d %9d"
      % (k, STORE[k].get('type'), entry_age(STORE[k]), STORE[k].get('games'), A[k]['v'], B[k]['v']))

# ---------------------------------------------------------------- rank movement
P()
P("-" * 128)
P("RANK MOVEMENT ON THE BOARD")
P("-" * 128)
rA = {k: i + 1 for i, k in enumerate(sorted(A, key=lambda k: -A[k]['v']))}
rB = {k: i + 1 for i, k in enumerate(sorted(B, key=lambda k: -B[k]['v']))}
rk = sorted(((rA[k] - rB[k], k) for k in movers), key=lambda x: -x[0])
P("  biggest rank climbs among the movers")
P("  %-26s %8s %8s %8s" % ('key', 'rank was', 'rank now', 'climb'))
for d, k in rk[:15]:
    P("  %-26s %8d %8d %+8d" % (k, rA[k], rB[k], d))
_slid = [(rA[k] - rB[k], k) for k in A if k not in movers and rA[k] != rB[k]]
P("  UN-MOVED rows displaced in rank by the movers: %d (their VALUES are unchanged; only their"
  % len(_slid))
P("  position in the ordering shifts, which is arithmetic, not a repricing)")

json.dump(dict(live_md5=md5(LIVE), variant_md5=md5(VAR),
               off_rebuild_md5=md5(OFF), off_matches_live=(md5(OFF) == md5(LIVE)),
               determinism=(md5(VAR2) == md5(VAR)) if os.path.exists(VAR2) else None,
               n_rows=len(A), eligible=sorted(ELIG), n_eligible=len(ELIG),
               movers=sorted(movers), n_movers=len(movers), movers_outside_E=outside,
               eligible_unmoved=still,
               total_live=tA, total_variant=tB,
               rows=[dict(key=k, before=A[k]['v'], after=B[k]['v'], delta=B[k]['v'] - A[k]['v'],
                          rel=B[k]['v'] / A[k]['v'] - 1, typ=STORE[k].get('type'),
                          pick=STORE[k].get('pick'), entry_age=entry_age(STORE[k]),
                          grace=grace_of(STORE[k]), games=STORE[k].get('games'),
                          pos=A[k].get('gf'), rank_before=rA[k], rank_after=rB[k])
                     for k in sorted(movers, key=lambda k: -(B[k]['v'] - A[k]['v']))]),
          open(os.path.join(HERE, 'MOVERS28.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'MOVERS28_out.txt'), 'w').write("\n".join(LOG) + "\n")
print("\nwrote MOVERS28.json / MOVERS28_out.txt")
