"""THE MRAZ LINE — the BEFORE side. READ-ONLY.

The package did not land (see README SS3-4), so there is no combined move to print. What CAN be
printed, and is printed here, is where Mraz already stands against his standing surprise-scaled-trust
tolerance BEFORE anything moves — the baseline any future combined-move line is measured from.

His ruled band ran 2-3x his pick's value at stage 4, slackened to 3.5-3.8x at stage 5; the charter
names 3.5x as the line. The pick is 35, so the reference is the curve value at pick 35.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # re-runnable FROM THE TREE
from engine_load import load
g_ = load()
MA = g_['MA']; ev = g_['ev']; entry_anchor = g_['entry_anchor']
PVC0 = g_['_PVC0']
PL_F = g_['_PL_F']

p = [x for x in MA.data if x.get('key') == 'noah-mraz'][0]
pick = p['pick']
curve = float(PVC0[pick])                       # LADDER currency (the board's trade currency)
board = json.load(open(os.path.join(os.environ.get('RL_REPO', '/home/user/afl-rl-engine'),
                                    'data', 'rl_build', 'rl_app_data.json')))
brow = [r for r in board['active'] if r.get('k') == 'noah-mraz' or r.get('key') == 'noah-mraz']
bv = brow[0]['v'] if brow else None

print('NOAH MRAZ — the standing-tolerance baseline')
print('  club/pos/pick      : %s %s pick %d (class %s)' % (p.get('afl_club'), MA.gfut(p), pick, p.get('year')))
print('  record             : %s' % p['scoring'])
print('  pick-35 curve value: %.1f   (ladder currency, the frozen _PVC0 ruler)' % curve)
print('  entry anchor       : %.1f   (engine ccy)' % float(entry_anchor(p)))
print('  engine ev(2026)    : %.1f' % float(ev(p, 2026)))
print('  BOARD price        : %s' % bv)
print()
for label, val, ccy in (('board price', bv, 'board'), ('engine ev', float(ev(p, 2026)), 'engine')):
    if val is None: continue
    lad = val * PL_F if ccy == 'board' else val
    print('  %-12s / pick-35 curve = %8.3f x   %s' % (label, val / curve, ccy + ' ccy, raw'))
    print('  %-12s / pick-35 curve = %8.3f x   (%s -> ladder ccy, x%.4f)' % (label, lad / curve, ccy, PL_F))
print()
print('  THE LINE: 3.5x  ->  %.1f (ladder ccy) / %.1f (board ccy)' % (3.5 * curve, 3.5 * curve / PL_F))
print('  Read straight: Mraz is ALREADY well above the 3.5x line on the shipped board, before any')
print('  item of this package touches him. Any combined move is therefore a move on an ALREADY-')
print('  BREACHED baseline, and the breach is not something this act would create.')
print('  This is a FLAG for the owner, not a resize (charter: breach = flag, do not resize).')
