#!/usr/bin/env python3
"""ui/tools/gen_v0_sidecar.py — THE v0 SIDECAR. Generates ui/data_aux/v0.js, READ-ONLY throughout.

WHAT v0 IS, IN THE OWNER'S OWN TERMS
------------------------------------
docs/ENGINE_PRIMER.md:45, his binding definition: v0 is *"the value of a NEWLY DRAFTED player: the
price at entry … 'the true worth of a player the moment they are drafted' — career included, not
year-one output."*  It is a DRAFT-TIME property, not a priced position on this week's board, and it is
the anchor the card and the board column compare his live rating against.

The primer also states the thing a reader must not forget (ENGINE_PRIMER.md:170): *"`v0` in a matrix
row = the surface's slot value — IDENTICAL for every same-(pos, age, pick) player. It is a MODEL
BELIEF, not that player's outcome."*  Every pick-5 mid of the same draft age therefore shares one v0,
by construction. The surfaces below carry that verbatim; nothing here breaks the tie, and NOTHING HERE
RANKS.  A ranking over v0 would put two-thirds of the board into shared blocks (measured: 527 of 804
rows share a slot, largest block 14) and a "rank change vs v0" inside a block would be an artifact of a
tie-break rather than a fact about the player. The owner's ask is the eyeball — his v0, his live
rating, the absolute gap and the ratio — and that half has none of that problem.

EVERY PLAYER HAS A v0, INCLUDING POOL ENTRANTS (owner correction, 2026-08-21)
----------------------------------------------------------------------------
His words: *"Pool entrants do have a v0 though? The moment they are drafted, they have a value. So
isn't that their v0?"*  He is right, and the engine already agrees with him in one function.

  · A player who entered on a NUMBERED PICK draws his entry price from the year-zero pick surface —
    `v0_start(p)`, _merged_recover.py:~2669, off the frozen `data/v0surf.pkl`. ORIGIN: `pick-slot`.
  · A POOL ENTRANT does not. The owner's #326 addendum 6 is explicit — *"for a pool entrant the
    pool-slot-derived v0_start no longer sets his entry price, even where the signed level cuts"* — his
    entry price is his intake division's SIGNED LEVEL, converted into engine-value currency by the
    board factor and age-shaped by ITEM B at constant pool total. ORIGIN: `entry-anchor`.

Both are the same object — the price the model put on him the moment he entered — and the engine
already resolves the two in ONE function, `entry_anchor(p)` (_merged_recover.py:~2765):

    def entry_anchor(p):
        if p.get('_pool'): return float(MA.pool_level(p))*_PL_F*_b_factor(p)
        return v0_start(p)

So this generator does not choose between two numbers or invent a rule: it calls the engine's own
entry-price function per player and RECORDS WHICH BRANCH ANSWERED, so the card can label the source
honestly instead of implying one provenance for both populations. `ui/data_aux/v0.js` carries
`origin` on every row for exactly that reason.

A row whose origin value cannot be recovered at all gets `v0: null` — an explicit absence the reader
renders as an em-dash with its reason, never a fabricated anchor — and the count is reported by this
tool and carried in the bundle stamp so it can never go unnoticed.

WHY A SIDECAR AND NOT A BOARD FIELD (Route B)
---------------------------------------------
The board identity IS md5(rl_app_data.json) — data/expected_boot.json, data/release_contract.json and
both UI bundles all pin it. Adding one field to 804+198 rows changes those bytes, retires the board of
record, and turns a display-only constant into a full lever-class landing (19 declared carriers, a
lineage entry, an owner-set history column, every gate re-proved). v0 is a draft-time constant off a
FROZEN surface: `_ageR(p)` is age as of the draft year and the slot key depends only on
(future position, draft age, pick), so v0 does not move on a round advance. It moves only when the
store changes a player's dob / pick / type / future position, when the v0 surface or a ruled curve is
re-cut, or when the roster changes. Paying a landing every time for a number that does not move is the
wrong trade; the sidecar is the shape `ui/data/ownership.js` and `ui/data/club_valuation.js` already
established for exactly this class.

WHY ui/data_aux/ AND NOT ui/data/
---------------------------------
`ui/data/` is landing-carrier territory: `tools/landing/carriers.py` names those files and a landing
rewrites them. A sidecar that is NOT a landing carrier must not sit inside the set a landing sweeps,
or the two writers will fight over the directory and a lander will one day tidy it away. `ui/data_aux/`
is this file's own address, outside the carrier set, and is declared here rather than assumed.

THE LAW THIS BUNDLE OBEYS — `ui/app/ownership.js:25`: *"A mirror that does not name the identity it was
generated from is not a mirror."*  The bundle is stamped with the FULL board md5 and store md5 it was
generated from, and `MD.v0` refuses (renders nothing, reports the row) when either disagrees with the
board the app is loaded on. Fail closed, and not silently: the reader says which identity broke.

READ-ONLY, AND NO BUILD LOCK. This file opens the engine to ask it questions and writes exactly one
file, under ui/data_aux/. It runs no build, holds no lock, touches no store, no board, no pin, and no
carrier. The engine-load recipe is the day-0 evidence-script pattern
(docs/evidence/staircase_fix_2026-08-20/sfx_day0.py and siblings), which is already the established
way to load the engine read-only, assert the live board, and write a keyed artifact.

    usage:  python3 ui/tools/gen_v0_sidecar.py [--out PATH] [--check]
            --check  regenerate in memory and DIFF against the committed bundle; write nothing.
                     Exit 1 if they differ — the "regenerate and byte-compare" check that the
                     ownership mirror's own doctrine says a generated file must support.
"""
import argparse
import contextlib
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
if os.path.basename(os.path.dirname(HERE)) != 'ui':                 # ui/tools/ -> repo root
    ROOT = os.path.dirname(os.path.dirname(HERE))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))

BOARDP = os.path.join(ROOT, 'engine', 'rl_after', 'rl_app_data.json')
STOREP = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')
BOOTP = os.path.join(ROOT, 'data', 'expected_boot.json')
DEFAULT_OUT = os.path.join(ROOT, 'ui', 'data_aux', 'v0.js')

GENERATOR = 'ui/tools/gen_v0_sidecar.py'


def md5_of(path):
    return hashlib.md5(open(path, 'rb').read()).hexdigest()


def load_engine():
    """The day-0 read-only load. Returns (MA, namespace).

    The env block is the one the day-0 scripts carry: the shipped dial expression plus the path vars
    and the five thread pins for determinism. RL_CONFIG_MODE and RL_BUILD_LOCK_HELD are POPPED — the
    thrice-burned rule that no RL_ tooling var is ever shipped into the engine, and this tool holds no
    build lock by design.
    """
    os.environ.update(
        PYTHONHASHSEED='0', RL_REPO=ROOT,
        OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
        NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
        RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
        RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'),
    )
    os.environ.pop('RL_CONFIG_MODE', None)
    os.environ.pop('RL_BUILD_LOCK_HELD', None)

    sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
    cwd = os.getcwd()
    os.chdir(os.path.join(ROOT, 'engine', 'rl_after'))
    ns = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            import rl_model as MA                                    # noqa: E402
            src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
            exec(compile(src, '_merged_recover.py', 'exec'), ns)
    finally:
        os.chdir(cwd)
    return ns.get('MA', MA), ns


def build(board_md5, store_md5):
    MA, ns = load_engine()
    entry_anchor = ns['entry_anchor']
    v0_start = ns['v0_start']

    board = json.load(open(BOARDP))
    # read for the entry-inputs signature below — the raw store, not the engine's view of it, so the
    # reader can recompute the same digest without paying an engine load
    with open(STOREP, encoding='utf-8') as _sf:
        store_rows = json.load(_sf)
    active_keys = [r['key'] for r in board.get('active', [])]
    active_set = set(active_keys)

    by_key = {}
    counts = {'pick-slot': 0, 'entry-anchor': 0, 'absent': 0}
    absent_rows = []
    for p in MA.data:
        k = p.get('key')
        if not k or k not in active_set:
            continue
        pool = bool(p.get('_pool')) or MA.is_pool(p)
        try:
            val = entry_anchor(p)
            val = None if val is None else int(round(float(val)))
        except Exception as exc:                                     # noqa: BLE001 - reported, never silent
            val = None
            absent_rows.append((k, '%s: %s' % (type(exc).__name__, exc)))
        origin = 'entry-anchor' if pool else 'pick-slot'
        if val is None:
            counts['absent'] += 1
            by_key[k] = {'v0': None, 'origin': 'unrecoverable'}
            if not absent_rows or absent_rows[-1][0] != k:
                absent_rows.append((k, 'engine returned no entry price'))
            continue
        counts[origin] += 1
        rec = {'v0': val, 'origin': origin}
        # The SLOT the pick-surface priced him at, so a reader can show WHY two players share a v0
        # without re-deriving the key. Pool rows have no pick slot and carry none.
        if origin == 'pick-slot':
            try:
                rec['slot'] = '%s|%d|%s' % (MA.gfut(p), int(ns['_ageR'](p)), p.get('pick'))
            except Exception:                                        # noqa: BLE001
                pass
        by_key[k] = rec

    missing = [k for k in active_keys if k not in by_key]
    for k in missing:
        by_key[k] = {'v0': None, 'origin': 'unrecoverable'}
        counts['absent'] += 1
        absent_rows.append((k, 'no engine record joins this board key'))

    # THE IDENTITY THAT AUTHENTICATES THIS FILE is entryInputsSig, NOT board/store. Those two move
    # on every round advance and v0 does not (see the module docstring's own statement of the
    # invariant), so gating the join on them refused a perfectly good sidecar the moment any football
    # landed — measured at FW1: 804 of 804 entry prices byte-identical across the store move, and
    # every player card lost its entry price anyway. board/store stay in the stamp as PROVENANCE:
    # what this file was cut on, which is worth recording and is not what makes it valid.
    import sys as _sys
    _sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from v0_identity import entry_inputs_sig, SIG_VERSION
    stamp = {
        'entryInputsSig': entry_inputs_sig(store_rows),
        'entryInputsSigVersion': SIG_VERSION,
        'board': board_md5,
        'store': store_md5,
        'generatedFromStore': store_md5,
        'generator': GENERATOR,
        'source': "engine entry_anchor(p) — v0_start off the frozen year-zero pick surface for a "
                  "numbered-pick entrant, the signed division entry level (#326) for a pool entrant",
        'nRows': len(by_key),
        'nPickSlot': counts['pick-slot'],
        'nEntryAnchor': counts['entry-anchor'],
        'nAbsent': counts['absent'],
    }
    return {'stamp': stamp, 'byKey': by_key}, absent_rows


def render(bundle):
    head = (
        "/* GENERATED — DO NOT HAND-EDIT. %s\n"
        "   The v0 sidecar: every active board player's ENTRY PRICE, and where it came from.\n"
        "     origin \"pick-slot\"    — the frozen year-zero pick surface (v0_start). All same-(future\n"
        "                             position, draft age, pick) players share one value, by construction.\n"
        "     origin \"entry-anchor\" — a POOL entrant's signed division level (#326 entry anchors), in\n"
        "                             engine-value currency. His v0 is his entry price too; it simply is\n"
        "                             not a pick slot.\n"
        "     origin \"unrecoverable\" — no entry price could be recovered. v0 is null and the reader\n"
        "                             renders an em-dash with the reason. Never a fabricated anchor.\n"
        "   STAMPED WITH THE IDENTITY IT WAS GENERATED FROM. MD.v0 refuses this bundle when the board or\n"
        "   store it names is not the one the app is loaded on — a mirror that does not name its identity\n"
        "   is not a mirror (ui/app/ownership.js:25). Regenerate with:  python3 %s  */\n"
    ) % (GENERATOR, GENERATOR)
    body = json.dumps(bundle, sort_keys=True, separators=(',', ':'))
    return head + 'window.__V0__ = ' + body + ';\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--out', default=DEFAULT_OUT)
    ap.add_argument('--check', action='store_true',
                    help='regenerate and compare against the committed bundle; write nothing')
    args = ap.parse_args(argv)

    board_md5 = md5_of(BOARDP)
    store_md5 = md5_of(STOREP)
    boot = json.load(open(BOOTP))
    want_board = str(boot.get('board', ''))
    if want_board and not board_md5.startswith(want_board[:8]):
        sys.exit('BOARD RING-FENCE FAIL: %s is md5 %s but data/expected_boot.json declares %s'
                 % (os.path.relpath(BOARDP, ROOT), board_md5[:8], want_board[:8]))
    want_store = str(boot.get('store', ''))
    if want_store and not store_md5.startswith(want_store[:8]):
        sys.exit('STORE RING-FENCE FAIL: %s is md5 %s but data/expected_boot.json declares %s'
                 % (os.path.relpath(STOREP, ROOT), store_md5[:8], want_store[:8]))

    bundle, absent = build(board_md5, store_md5)
    text = render(bundle)

    st = bundle['stamp']
    print('v0 sidecar | board %s store %s | rows %d = pick-slot %d + entry-anchor %d + unrecoverable %d'
          % (st['board'][:8], st['store'][:8], st['nRows'], st['nPickSlot'],
             st['nEntryAnchor'], st['nAbsent']))
    for k, why in absent[:20]:
        print('  UNRECOVERABLE %s — %s' % (k, why))
    if len(absent) > 20:
        print('  ... and %d more' % (len(absent) - 20))

    if args.check:
        if not os.path.exists(args.out):
            print('CHECK FAIL: %s does not exist' % os.path.relpath(args.out, ROOT))
            return 1
        have = open(args.out, 'r').read()
        if have != text:
            print('CHECK FAIL: %s differs from a fresh generation on this board/store'
                  % os.path.relpath(args.out, ROOT))
            return 1
        print('CHECK PASS: committed bundle is byte-identical to a fresh generation')
        return 0

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w') as fh:
        fh.write(text)
    print('wrote %s (%d bytes)' % (os.path.relpath(args.out, ROOT), len(text)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
