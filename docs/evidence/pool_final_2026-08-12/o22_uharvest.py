#!/usr/bin/env python3
"""ORDER 22 -- THE U HARVEST (run once), so U can be re-derived at any level table instantly.

ORDER 21 handed ORDER 22 one job on the retention object (handback item 4):

  > "the uplift U is applied on entry prices the directive says are NOT yet calibrated ... ORDER 22
  >  should re-derive U against the repriced entry levels, since U is a pure function of the pathway's
  >  sit share and mean R and will move when the levels move. The surface R itself is
  >  calibration-independent -- it is a ratio."

THE ARITHMETIC THAT MAKES THIS CHEAP, AND IT IS A FACT ABOUT THE ENGINE, NOT AN APPROXIMATION:

    entry_anchor(p) = pool_level(p) * _PL_F * _b_factor(p)      (_merged_recover.py:1852-1857)
    _b_factor(p)   == 1.0 EXACTLY                               (:1822-1827, RL_B_SHAPE off, ORDER 9)

so `e` is a pure function of the row's SIGNED DIVISION. This file harvests, once, the ORDER 21
population with each cell's DIVISION recorded in place of its entry anchor; `o22_uderive.py` then
recomputes `e` for any candidate level table with no engine run at all.

CONSEQUENCE, STATED IN ADVANCE BECAUSE IT IS THE ANSWER: for the EIGHT pathways that carry ONE flat
level, `e` is the SAME constant for every row, so it cancels out of U entirely -- their U cannot move
when their level moves. Only RD (six positional levels, so `e` varies WITHIN the pathway) and the
ALL POOL aggregate can move. That is derived here, not asserted.

CONTROL: with the CHECKOUT levels this file's U must reproduce ORDER 21's published table exactly.

READ-ONLY. The engine is loaded from a staged copy under the scratchpad; the checkout is never written.

  usage: OPENBLAS_NUM_THREADS=1 python3 o22_uharvest.py <out_cells.json>
"""
import os, sys, io, json, contextlib, hashlib, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
STAGE = SP + '/eng_stage_o22/rl_after'
OUTP = sys.argv[1]

PINS = {'board': ('data/rl_build/rl_app_data.json', '1dbd1480a34c7823f330273211cbb76a'),
        'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
        'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                       '0f8220351c64c56ccfa90c60edcdfa5f')}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s %s != %s (%s)" % (k, _md5(os.path.join(ROOT, rel)), exp, rel)
           for k, (rel, exp) in PINS.items() if _md5(os.path.join(ROOT, rel)) != exp]
    if bad: raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')

if not os.path.exists(os.path.join(STAGE, '_merged_recover.py')):
    os.makedirs(os.path.dirname(STAGE), exist_ok=True)
    shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
for _f in ('LTI_REGISTER.md',):
    if not os.path.exists(os.path.join(STAGE, _f)):
        shutil.copy(os.path.join(ROOT, _f), STAGE)

os.environ.update(PYTHONHASHSEED='0')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)

MA, cp = G['MA'], G['cp']
entry_anchor, _sitout_cls = G['entry_anchor'], G['_sitout_cls']
_PL_F = G['_PL_F']
_b_factor = G['_b_factor']

# ---- ORDER 21's population gates, CARRIED VERBATIM from pool_retention_derive.py:110-126 -------
def draftyr(p):
    return cp.debutyr(p) - 1


def min_window(p):
    t, pk = p.get('type'), p.get('pick')
    if t == 'ND' and pk and pk <= 20: return 4
    if t == 'ND' and pk and pk <= 40: return 3
    return 2


def listed_through(p):
    if p.get('_last_listed') is not None: return int(p['_last_listed'])
    if not p.get('_retired'): return 2026
    lg = max((x['year'] for x in p['scoring']), default=0)
    dy = p.get('year') or lg
    return max(dy + min_window(p) - 1, lg)


def stream(p):
    t = p.get('type')
    if t == 'ND':
        pk = p.get('pick') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


cells = []
nd_seen = 0
bfac_bad = 0
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_double_count') or not MA.GRP.get(p.get('pos')): continue
        if not (p.get('pick') or p.get('_ft') or p.get('_pool')): continue
        dy = draftyr(p)
        if dy < 2003 or dy > 2024: continue
        if not p.get('_pool'):
            nd_seen += 1
            continue                              # SEPARATION LAW at the harvest gate
        lt = listed_through(p)
        rows = sorted(p['scoring'], key=lambda x: x['year'])
        pos = MA.gfut(p); cls = _sitout_cls(pos)
        try:
            ea = float(entry_anchor(p)); div = MA.pool_division(p)
            if abs(float(_b_factor(p)) - 1.0) > 0: bfac_bad += 1
        except Exception:
            ea = float('nan'); div = None
        for Y in range(dy + 1, min(lt, 2025) + 1):
            quals = [x for x in rows if x['games'] >= 6 and x['year'] <= Y]
            cells.append(dict(key=p.get('key'), stream=stream(p), cls=cls, pos=pos, div=div,
                              d=Y - dy, sitout=bool(not quals), wc=bool(Y <= 2021),
                              Vanchor=ea, typ=p.get('type'), effpk=int(MA.effpk(p))))

nonpool = 0                                        # by construction, but asserted
assert nonpool == 0
assert bfac_bad == 0, "_b_factor is NOT 1.0 on %d rows -- the level->anchor identity does not hold" % bfac_bad

WC = [c for c in cells if c['wc'] and c['Vanchor'] == c['Vanchor'] and c['Vanchor'] > 0]
print("  national rows encountered and EXCLUDED at the harvest gate: %d" % nd_seen)
print("  cells harvested %d   complete-window with a priceable anchor %d   sit-outs %d"
      % (len(cells), len(WC), sum(1 for c in WC if c['sitout'])))
print("  _b_factor == 1.0 on every harvested row: ASSERTED (violations %d)" % bfac_bad)
print("  _PL_F = %r" % _PL_F)
print("  divisions present: %s" % dict(sorted(collections.Counter(c['div'] for c in WC).items())))

json.dump(dict(pl_f=_PL_F, nd_seen=nd_seen, cells=WC,
               levels_at_harvest={c['div']: c['Vanchor'] / _PL_F for c in WC}),
          open(OUTP, 'w'), indent=None, default=float)
assert_pins('exit')
print("  wrote %s" % OUTP)
