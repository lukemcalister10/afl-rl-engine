"""TASK 7 -- THE CONSEQUENCE READ, and the ordered _ruc_prior_cap check.

WHAT THIS DOES AND, JUST AS IMPORTANTLY, WHAT IT DOES NOT.

PHASE 1 DOES NOT WIRE AND DOES NOT MOVE THE SHIPPED BOARD. So the consequence is MODELLED through the
engine's own MEASURED pass-through from entry anchor to price, exactly as the directive's D5 and D6
figures were produced -- not by building a board. That is the directive's own measurement ledger
(section 2): "The chosen option built as a board, to confirm the modelled figures in D5 and D6 against
a real build" is listed as work to run AFTER the owner rules, deliberately, to respect machine time.

THE PASS-THROUGH, measured on the ITEM B natural experiment [POOL]:
    career games 0      -> e = 0.996   essentially all of an entry-price change reaches the price
    career games 1-9    -> e = 0.119   almost none
    career games 10+    -> e = 0.000   NONE AT ALL
A player at ten games or more CANNOT be moved by an entry-price change. price' = price * lambda**e.

The lambda applied to each pool row is ITS OWN CELL's lambda from the shipped layer-2 construction
(pathway x position), read from PHASE1_DERIVE.json -- not a pool-wide number and not a year-4 number.

BOTH COHORT INSTRUMENTS ARE READ, per the owner's standing ruling: the ALL-ARM table is the deciding
lens and the legacy picks 1-64 table is retained. A no-arbitrage margin against the 14% charge is
printed beside every candidate. BOTH headline metrics are reported: the full career profile AND
year-4-value-over-year-0-entry.

READ-ONLY. No emits. Does not touch the shipped configuration.
"""
import sys, json, os, math, statistics, collections

ROOT = '/home/user/afl-rl-engine'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O3 = SP + '/o3'
HERE = os.path.dirname(os.path.abspath(__file__))

D = json.load(open(os.path.join(HERE, 'PHASE1_DERIVE.json')))
R = json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']
BD = {r['key']: r for r in json.load(open(O3 + '/ship_board.json'))['active']}
MX = {r['key']: r for r in R}

CHARGE = 0.14
POS6 = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
POOLS = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
LAM = {s: D['shipped'][s]['lam'] for s in D['shipped']}
NDp = D['nd_profile']


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def stream(r):
    t = r.get('type')
    if t == 'ND' and r.get('pick') and 1 <= r['pick'] <= 64 and not r.get('is_pool'): return 'ND 1-64'
    if t == 'ND': return 'ND>64'
    return t


def games(r): return sum(s.get('games', 0) for s in (r.get('seasons') or []))


def e_of(r):
    g = games(r)
    return 0.996 if g == 0 else (0.119 if g <= 9 else 0.0)


def lam_of(r):
    s = stream(r)
    if s not in LAM: return 1.0
    p = r.get('pos')
    return LAM[s].get(p, D['layer1'][s]['lam']) if p in POS6 else D['layer1'][s]['lam']


elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
W = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)

P = print
P("=" * 118)
P("TASK 7 -- THE CONSEQUENCE READ")
P("=" * 118)
P("  lambda per row = its OWN layer-2 cell (pathway x position), shipped construction, K=10 borrow,")
P("  renormalised. Pass-through e: 0.996 at 0 games, 0.119 at 1-9, 0.000 at 10+.")
P("  MODELLED, not built. A board build belongs to adoption and is not run here.")
P()

# --------------------------------------------------------------- board total
pool_board = [k for k in BD if k in MX and stream(MX[k]) in POOLS]
tb = sum(r['v'] for r in BD.values())
movable = [k for k in pool_board if e_of(MX[k]) > 0]
P("=" * 118)
P("BOARD TOTAL AND REACH")
P("=" * 118)
d = sum(BD[k]['v'] * (lam_of(MX[k]) ** e_of(MX[k]) - 1) for k in pool_board)
P("  board rows total                : %d" % len(BD))
P("  pool rows on the board          : %d" % len(pool_board))
P("  of those, reachable at all (e>0): %d   worth %s points, %.2f%% of the board"
  % (len(movable), format(round(sum(BD[k]['v'] for k in movable)), ','),
     100.0 * sum(BD[k]['v'] for k in movable) / tb))
P()
P("  BOARD TOTAL  %s  ->  %s   (%+.2f%%)" % (format(round(tb), ','), format(round(tb + d), ','), 100.0 * d / tb))
P()
P("  The repair's reach is small BY CONSTRUCTION, not by accident: the engine already lets a player's")
P("  own playing record take over from his entry price, and at ten games it has taken over completely.")
P()

# --------------------------------------------------------------- movers
P("=" * 118)
P("THE MOVERS -- every pool board row that moves at all, largest absolute move first")
P("=" * 118)
mv = []
for k in pool_board:
    e = e_of(MX[k])
    if e <= 0: continue
    l = lam_of(MX[k])
    v0 = BD[k]['v']; v1 = v0 * (l ** e)
    if abs(v1 - v0) < 0.5: continue
    mv.append((abs(v1 - v0), k, v0, v1, l, e))
mv.sort(reverse=True)
P("  %-22s %-7s %-5s %8s %6s %6s %8s %8s %8s" %
  ('player', 'stream', 'pos', 'games', 'e', 'lambda', 'SHIP', 'DERIVED', 'delta'))
P("  " + "-" * 114)
for _, k, v0, v1, l, e in mv[:40]:
    m = MX[k]
    P("  %-22s %-7s %-5s %8d %6.3f %6.3f %8d %8d %+8d" %
      (BD[k]['name'][:22], stream(m), m.get('pos') or '-', games(m), e, l, round(v0), round(v1), round(v1 - v0)))
P("  " + "-" * 114)
P("  movers: %d of %d pool board rows" % (len(mv), len(pool_board)))
P()

# --------------------------------------------------------------- the named lines
P("=" * 118)
P("THE NAMED LINES -- the directive's own D5 roster, on the derived numbers")
P("=" * 118)
NAMED = ['john-noble', 'max-hall', 'james-peatling', 'mark-keane', 'tom-mccarthy', 'lachlan-mcandrew',
         'zac-banch', 'flynn-perez', 'paddy-cross', 'marcus-herbert', 'mitch-podhajski', 'harrison-coe']
P("  %-22s %-7s %-5s %8s %6s %7s %8s %9s" %
  ('player', 'stream', 'pos', 'games', 'e', 'lambda', 'SHIP', 'DERIVED'))
P("  " + "-" * 114)
for k in NAMED:
    if k not in BD or k not in MX: continue
    m = MX[k]; e = e_of(m); l = lam_of(m)
    P("  %-22s %-7s %-5s %8d %6.3f %7.3f %8d %9d" %
      (BD[k]['name'][:22], stream(m), m.get('pos') or '-', games(m), e, l,
       round(BD[k]['v']), round(BD[k]['v'] * (l ** e))))
P()
P("  The owner's expectation is confirmed exactly: the established players do not move, because they")
P("  are priced on their own playing record and carry zero pass-through from the entry price.")
P()

# --------------------------------------------------------------- cohort instruments
P("=" * 118)
P("BOTH COHORT INSTRUMENTS -- all-arm is the DECIDING lens; legacy picks 1-64 retained")
P("=" * 118)


def val(r, N):
    if N == 0: return float(r['v0']), 'v0'
    Y = cohort(r) + N - 1
    yrs = r.get('yrs') or []; vp = r.get('vpath') or []
    if not yrs: return 0.0, 'ended'
    if Y < yrs[0]: return None, 'pre'
    if Y > yrs[-1]: return 0.0, 'ended'
    i = yrs.index(Y)
    return (0.0, 'null') if vp[i] is None else (float(vp[i]), 'path')


def arm_ratio(sub, N, apply_lam):
    num = den = 0.0
    for r in sub:
        if cohort(r) + N - 1 > W: continue
        v, k = val(r, N)
        if k == 'pre': continue
        l = lam_of(r) if apply_lam else 1.0
        num += v * (l ** e_of(r))
        den += float(r['v0']) * l
    return num / den if den else float('nan')


allsub = [r for r in elig if 2005 <= cohort(r) <= 2023]
leg = [r for r in allsub if stream(r) == 'ND 1-64']
P()
P("  %-26s %10s %10s | %11s %10s %9s" %
  ('instrument', 'now', 'DERIVED', 'apprec.', 'charge', 'MARGIN'))
P("  " + "-" * 114)
for lab, sub in (('ALL-ARM (deciding)', allsub), ('legacy picks 1-64', leg)):
    a0 = arm_ratio(sub, 1, False); a1 = arm_ratio(sub, 1, True)
    ap = a1 - 1.0
    P("  %-26s %10.4f %10.4f | %+10.2f%% %9.2f%% %+8.2f%%" %
      (lab + ' yr1', a0, a1, 100 * ap, 100 * CHARGE, 100 * (CHARGE - ap)))
P()
P("  FREE MONEY REQUIRES APPRECIATION TO EXCEED THE CHARGE. A margin above zero is legal.")
P()
P("  the same instruments at year 4, for context (year 4 is NOT a target -- standing law):")
P("  %-26s %10s %10s" % ('instrument', 'now', 'DERIVED'))
for lab, sub in (('ALL-ARM yr4', allsub), ('legacy picks 1-64 yr4', leg)):
    P("  %-26s %10.4f %10.4f" % (lab, arm_ratio(sub, 4, False), arm_ratio(sub, 4, True)))
P()
P("  THE LEGACY INSTRUMENT IS INVARIANT AND THAT IS A STRUCTURAL FACT, NOT A NULL RESULT: the picks")
P("  1-64 table contains national-draft rows only, and no pool level enters any of them. It is")
P("  retained as the owner ruled, and it is reported as unmoved BECAUSE it cannot move.")
P()

# --------------------------------------------------------------- both headline metrics
P("=" * 118)
P("BOTH HEADLINE METRICS -- the career profile AND year-4-over-year-0. Neither is a target.")
P("=" * 118)
P("  %-8s %6s | %14s %10s | %14s %10s | %10s" %
  ('pathway', 'n', 'CAREER PROF', 'vs ND', 'YR4/YR0', 'vs ND', 'derived L1'))
P("  " + "-" * 114)
for s in POOLS:
    L = D['layer1'][s]
    sub = [r for r in elig if stream(r) == s]
    y4 = arm_ratio(sub, 4, False)
    P("  %-8s %6d | %14.4f %10.4f | %14.4f %10.4f | %10.1f" %
      (s, L['n'], L['profile'], L['lam_raw'], y4, y4 / D['nd_yr4'], D['derived_levels_layer1'][s]))
P("  " + "-" * 114)
P("  %-8s %6d | %14.4f %10.4f | %14.4f %10.4f |" %
  ('ND 1-64', len([r for r in elig if stream(r) == 'ND 1-64']), NDp, 1.0, D['nd_yr4'], 1.0))
P()

# --------------------------------------------------------------- ruck cap
P("=" * 118)
P("THE ORDERED _ruc_prior_cap CHECK -- the only surviving v0-chain law that touches this act")
P("=" * 118)
P()
P("    _ruc_prior_cap(p,v) = min(v, RUC_PRIOR_CAP * _cap_basis(p) * _ruc_head_v0(p))  for gfut=='RUCK'")
P("    _cap_basis(p)       = pool_level(p) for a pool row  (_merged_recover.py:1209-1213)")
P()
P("  SO THE CAP IS EXACTLY PROPORTIONAL TO THE LEVEL THIS ACT CHANGES. Lower the level by lambda and")
P("  the ceiling drops by the same lambda. Whether it BINDS depends on whether the capped quantity")
P("  falls with it -- and _v0_uncapped = raw_ev(p, debutyr-1) * iso_eff(...) is a production-side")
P("  object that does NOT read pool_level. So a level CUT tightens the cap against an unchanged v0.")
P()
rucks = [r for r in elig if stream(r) in POOLS and r.get('pos') == 'RUCK']
P("  pool rucks in the eligible population: %d" % len(rucks))
P("  %-8s %6s %12s %12s %12s" % ('pathway', 'n', 'level now', 'lambda RUCK', 'level derived'))
P("  " + "-" * 114)
for s in POOLS:
    g = [r for r in rucks if stream(r) == s]
    if not g: continue
    cur = D['current_levels']['rd_positional']['RUCK'] if s == 'RD' else D['current_levels']['flat'].get(s)
    l = LAM[s]['RUCK']
    P("  %-8s %6d %12.1f %12.4f %12.1f" % (s, len(g), cur, l, D['derived_levels_layer2'][s]['RUCK']))
P()
P("  THE DIRECTION OF THE RISK, stated plainly: every pool pathway's RUCK cell has the HIGHEST")
P("  lambda in its pathway (rucks are the best-delivering pool cell everywhere), so the ruck ceiling")
P("  falls LESS than its pathway's other cells. Where a pathway is cut hard overall, the ruck cap is")
P("  the least-tightened cell, not the most.")
P()
P("  WHAT THIS CHECK CANNOT SETTLE HERE, AND SO DOES NOT CLAIM TO: whether the cap actually BINDS on")
P("  any given derived ruck v0 is a property of the machinery's OUTPUT, and the outputs only exist")
P("  once the levels are wired and the engine re-run. That is adoption work by the order's own scope")
P("  boundary. What is established here is the STRUCTURE -- the cap moves with the level, is not a")
P("  fixed ceiling, and cannot silently clip a derived ruck without the level having moved first.")
P()

out = dict(board_total_now=tb, board_total_derived=tb + d, board_pct=100.0 * d / tb,
           pool_board_rows=len(pool_board), reachable=len(movable), movers=len(mv),
           allarm_yr1_now=arm_ratio(allsub, 1, False), allarm_yr1_derived=arm_ratio(allsub, 1, True),
           legacy_yr1_now=arm_ratio(leg, 1, False), legacy_yr1_derived=arm_ratio(leg, 1, True),
           allarm_yr4_now=arm_ratio(allsub, 4, False), allarm_yr4_derived=arm_ratio(allsub, 4, True),
           charge=CHARGE,
           named={k: dict(ship=BD[k]['v'], derived=BD[k]['v'] * (lam_of(MX[k]) ** e_of(MX[k])),
                          games=games(MX[k]), e=e_of(MX[k]), lam=lam_of(MX[k]))
                  for k in NAMED if k in BD and k in MX})
json.dump(out, open(os.path.join(HERE, 'PHASE1_CONSEQUENCE.json'), 'w'), indent=1, default=float)
P("wrote PHASE1_CONSEQUENCE.json")
