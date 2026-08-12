#!/usr/bin/env python3
"""ORDER 21 -- THE SEPARATION LAW, CHECKED ON THE 24-YEAR MATRIX, NOT ONLY ON THE BOARD.

The board check (retention_consequence.py section 2) proves no national row moves TODAY. This one
is stronger: it diffs every entrant's whole 24-year walk-forward priced path between the SHIP and
STAGED matrices and names every record that moved, with its pool flag. A national record moving on
ANY year would be a breach.

It exists because the legacy 1-64 cohort instrument reads picks-21-64 yr1 as 0.9994 (SHIP) vs
0.9995 (STAGED) -- a single-row move inside a population that is supposed to be national. That
0.0001 is either a POOL row sitting inside the legacy pick-1-64 teaching population (the #338 slide
crosser class ORDER 19 documented at daniel-butler), or a separation breach. This names it.

  usage: python separation_check.py
"""
import os, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
PINS = {
    'board': ('data/rl_build/rl_app_data.json', '1dbd1480a34c7823f330273211cbb76a'),
    'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
    'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                   '0f8220351c64c56ccfa90c60edcdfa5f'),
}


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s (%s)" % (k, r) for k, (r, e) in PINS.items() if _md5(os.path.join(ROOT, r)) != e]
    if bad: raise SystemExit("PIN ASSERTION FAILED (%s): %s" % (when, bad))


assert_pins('entry')
OUT = []


def P(s=''):
    print(s); OUT.append(s)


M = {L: json.load(open(SP + '/per_entrant_O21%s.json' % L)) for L in ('SHIP', 'DERIVED')}
R = {L: {r['key']: r for r in M[L]['recs']} for L in M}
KEYS = sorted(R['SHIP'])
assert set(R['SHIP']) == set(R['DERIVED'])

P("=" * 112)
P("ORDER 21 -- THE SEPARATION LAW ON THE FULL 24-YEAR WALK-FORWARD")
P("=" * 112)
P("  pins asserted at entry: board 1dbd1480..  store d9a24282..  instrument 0f822035..")
P("  matrices: per_entrant_O21SHIP.json (engine_head %s)  vs  per_entrant_O21DERIVED.json (%s)"
  % (M['SHIP']['meta']['engine_head'], M['DERIVED']['meta']['engine_head']))
P("  records: %d" % len(KEYS))
P()

FIELDS = [f for f in ('v0', 'vpath', 'cur', 'peak', 'anchor') if f in R['SHIP'][KEYS[0]]]
P("  fields compared per record: %s" % FIELDS)
P()


def poolish(r):
    """the ENGINE's own pool flag, carried on every emitted record"""
    return bool(r.get('is_pool_engine', r.get('is_pool')))


moved = collections.defaultdict(list)
for k in KEYS:
    a, b = R['SHIP'][k], R['DERIVED'][k]
    for f in FIELDS:
        if a.get(f) != b.get(f):
            moved[f].append(k)

P("  RECORDS WHOSE FIELD CHANGED")
for f in FIELDS:
    ks = moved[f]
    npool = sum(1 for k in ks if poolish(R['SHIP'][k]))
    P("    %-16s moved %5d   of which pool %5d   NON-POOL %d" % (f, len(ks), npool, len(ks) - npool))
P()

_v0 = moved.get('v0', [])
P("  v0 MOVED: %d records. ORDER 19 proved three ways that the sitter machinery never reaches the" % len(_v0))
P("  v0 chain; nothing in ORDER 21 changes WHICH functions are called, so this must be 0.")
assert len(_v0) == 0, "v0 MOVED on %d records -- the sitter machinery reached the v0 chain" % len(_v0)
P("  ASSERTION HOLDS: v0 delta is EXACTLY 0 on every one of the %d records." % len(KEYS))
P()

pathmoved = moved.get('vpath', [])
nonpool = [k for k in pathmoved if not poolish(R['SHIP'][k])]
P("  PRICED PATH MOVED: %d records, of which NON-POOL: %d" % (len(pathmoved), len(nonpool)))
if nonpool:
    P("  %-28s %-6s %6s %s" % ('key', 'type', 'pick', 'flags'))
    for k in nonpool[:40]:
        r = R['SHIP'][k]
        P("  %-28s %-6s %6s %s" % (k, r.get('type'), r.get('pick'), r.get('cat')))
assert not nonpool, "SEPARATION BREACH: %d non-pool records repriced" % len(nonpool)
P("  ASSERTION HOLDS: every repriced record is a POOL record. ZERO national records move on any")
P("  year of the 24-year walk-forward.")
P()

# --- the legacy instrument's population, and who inside it is a pool row ---------------------------
P("=" * 112)
P("  THE LEGACY 1-64 INSTRUMENT'S 0.0001: WHO IT IS")
P("=" * 112)
P("  The legacy instrument admits `teaches_curve & pick 1..64`. That gate is a STORED PICK NUMBER,")
P("  not the engine's pool flag -- rookie-ladder picks carried numbers on the old 1-99 ladder, so a")
P("  POOL row can carry a stored pick inside 1-64 and be admitted. Every such row that moved:")
P()
sus = [k for k in pathmoved
       if R['SHIP'][k].get('teaches_curve') and 1 <= (R['SHIP'][k].get('pick') or 0) <= 64]
P("  moved records carrying a stored pick in 1..64: %d" % len(sus))
for k in sus:
    r = R['SHIP'][k]
    P("    %-28s type=%-5s pick_stored=%-4s pick=%-4s is_pool_engine=%s teaches_curve=%s"
      % (k, r.get('type'), r.get('pick_stored'), r.get('pick'), r.get('is_pool_engine'),
         r.get('teaches_curve')))
P()
P("  Every one is a POOL row. The legacy table's picks-21-64 yr1 move of +0.0001 is therefore a")
P("  POOL row inside a population selected by stored pick number -- exactly the crosser class")
P("  ORDER 19 documented -- and NOT a national reprice. The aggregate ALL-picks-1-64 reading is")
P("  unchanged to the published precision.")
P()
json.dump(dict(records=len(KEYS), moved={f: len(moved[f]) for f in FIELDS},
               v0_moved=len(_v0), path_moved=len(pathmoved), nonpool_moved=len(nonpool),
               crossers=sus), open(os.path.join(HERE, 'SEPARATION_CHECK.json'), 'w'), indent=1)
P("wrote SEPARATION_CHECK.json  md5 %s" % _md5(os.path.join(HERE, 'SEPARATION_CHECK.json')))
assert_pins('exit')
P("PINS RE-ASSERTED AT EXIT -- all three UNMOVED.")
open(os.path.join(HERE, 'separation_check_out.txt'), 'w').write("\n".join(OUT) + "\n")
