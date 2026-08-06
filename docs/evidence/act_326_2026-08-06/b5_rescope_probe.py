#!/usr/bin/env python3
"""#326 — exercise the RE-SCOPED B5 block's logic directly.

ship_gates_check.py cannot run on this tree at all: at its line 64 it hard-sets RL_GAMMA=0.85 and then
enforces the pinned manifest, which carries RL_GAMMA=1.0, so it halts on a config conflict before any gate
runs. That conflict exists at the UNMODIFIED tip (proved by git show) and has nothing to do with #326.

So the re-scoped block is exercised here instead: the same scope test, the same two bars, and the same
floor basis, read out of the live engine. This is a standalone exercise of the block's logic, not a
ship_gates run, and it is labelled as such.
"""
import contextlib, io, os, sys

G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
MA = G['MA']; ev = G['ev']; prefloor = G['ev_prefloor']; delisted = G['delisted']
anchor = G['entry_anchor']; ffrac = G['floor_frac']

B5_FLOORS = {1: 0.45, 2: 0.35, 3: 0.28, 4: 0.21, 5: 0.13, 6: 0.09}
B5_TAIL = 0.05


def scope(p):                                   # verbatim the re-scoped ship_gates_check._b5_scope
    if p.get('_retired') or delisted(p):
        return False
    if not p.get('_pool') and (p.get('type') != 'ND' or p.get('_pickless')):
        return False
    return (2026 - int(p.get('year') or 0)) >= 1


PRE, EV = {}, {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_retired'):
            continue
        try:
            PRE[id(p)] = float(prefloor(p, 2026)); EV[id(p)] = float(ev(p, 2026))
        except Exception:
            PRE[id(p)] = EV[id(p)] = None

live = [p for p in MA.data if not p.get('_retired') and PRE.get(id(p)) is not None]
lowered = [p['player'] for p in live if EV[id(p)] < PRE[id(p)] - 1e-9]
out_moved = [p['player'] for p in live if not scope(p) and abs(EV[id(p)] - PRE[id(p)]) > 1e-9]
saves = [p for p in live if scope(p) and EV[id(p)] > PRE[id(p)] + 1e-9]
pool_scope = [p for p in MA.data if p.get('_pool') and scope(p)]
nd_scope = [p for p in MA.data if not p.get('_pool') and scope(p)]

print('B5 RE-SCOPED (national draftees + engine-pool entrants on their signed division levels)')
print('  scope: %d national-draft rows + %d pool rows' % (len(nd_scope), len(pool_scope)))
print('  saves (floor bound): %d   of which pool: %d'
      % (len(saves), sum(1 for p in saves if p.get('_pool'))))
print('  BAR lowered            = %d (bar 0)  -- the floor is still a pure lower bound' % len(lowered))
print('  BAR moved out of scope = %d (bar 0)  -- nobody outside the floor scope moves' % len(out_moved))
print('  verdict: %s' % ('FEATURE (both bars met)' if not lowered and not out_moved else 'FAIL'))
print()
print('  floor column basis check (the engine\'s own entry anchor, not the retired draftval basis):')
with contextlib.redirect_stdout(io.StringIO()):
    rows = [(p['player'], 2026 - int(p.get('year') or 0), float(anchor(p)), EV[id(p)]) for p in saves[:6]]
for nm, yis, a, v in rows:
    print('    %-24s yrs=%-3d anchor=%8.1f  floor=%8.1f  shipped(engine)=%8.1f'
          % (nm, yis, a, B5_FLOORS.get(yis, B5_TAIL) * a, v))
sys.exit(0 if (not lowered and not out_moved) else 1)
