#!/usr/bin/env python3
"""tools/restamp.py — its tests (shrink S6).

Run:  python3 tools/test_restamp.py        (exit 0 = all pass)

WHAT MATTERS HERE. This tool's failure mode is not crashing, it is agreeing. A stamp table that has
quietly stopped reading a real value, or a measurer that has drifted from the landing transaction's
idea of "the tree", would report ALL STAMPS AGREE forever and be worse than not existing. So the
assertions below are mostly non-vacuity: that the comparison really discriminates, that a stamp
claiming nothing is refused rather than passed, that the two tables cannot overlap, and that this
file's measurers are the SAME measurers the lander uses.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import restamp as RS                                          # noqa: E402

fails = 0
n = 0


def ok(cond, label):
    global fails, n
    n += 1
    print(('  [PASS] ' if cond else '  [FAIL] ') + label)
    if not cond:
        fails += 1


TRUTH = {'board': 'b' * 32, 'store': 's' * 32, 'engine_head': 'e' * 32, 'rl_model': 'm' * 32,
         'register': 'r' * 32, 'v0surf': 'v' * 32, 'config': 'c' * 64, 'fv': 'f' * 64}


def fixture(tmp, **over):
    """A tree carrying only the stamped files, each agreeing with TRUTH unless overridden."""
    def w(rel, obj):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as f:
            json.dump(obj, f, indent=2)

    def wjs(rel, obj):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as f:
            f.write('window.__X__ = ' + json.dumps(obj) + ';\n')

    t = dict(TRUTH, **over)
    w('data/expected_boot.json', {k: t[k] for k in TRUTH})
    w('data/release_contract.json', {'identities': {k: t[k] for k in
                                     ('board', 'store', 'engine_head', 'rl_model', 'register', 'fv')},
                                     'config_sha256': t['config']})
    wjs('ui/data/board_view_working.js', {'stamp': {'board': t['board'], 'store': t['store'][:8],
                                                    'engine': t['engine_head'][:8],
                                                    'register': t['register'][:8],
                                                    'config': t['config'][:12]}})
    wjs('ui/data/club_valuation.js', {'stamp': {'board': t['board'], 'store': t['store'][:8],
                                                'engine': t['engine_head'][:8]}})
    w('engine/rl_after/ingestion/sibling_repin_state.json',
      {'source_store_md5': t['store'], 'fv_identity': t['fv']})
    return tmp


def main():
    print('RESTAMP TESTS\n  ' + '-' * 70)
    real_measure = RS.measure
    RS.measure = lambda root: dict(TRUTH)
    tmp = tempfile.mkdtemp(prefix='restamp_test_')
    try:
        # ---- the two tables can never overlap -------------------------------------------------
        stamp_paths = {p for _, p, _, _, _ in RS.STAMPS}
        hist_paths = {p for p, _ in RS.HISTORY_OR_BAKE}
        byd_paths = {p for p, _ in RS.NO_IDENTITY_BY_DESIGN}
        ok(not (stamp_paths & hist_paths), 'no path is both a stamp and a historical record')
        ok(not (stamp_paths & byd_paths), 'no path is both a stamp and declared identity-free')
        ok(len(stamp_paths) == len(RS.STAMPS), 'the stamp table has no duplicate paths')

        # ---- a coherent tree agrees ------------------------------------------------------------
        fixture(tmp)
        _, bad = RS.check(tmp, verbose=False)
        ok(not bad, 'a coherent tree reports every stamp agreeing')

        # ---- NON-VACUITY, PER STAMP AND PER IDENTITY --------------------------------------------
        # Each stamp claims a DIFFERENT subset (the sibling sidecar carries store and fv but no
        # engine id, for instance), so staling one fixed identity across the board would silently
        # skip the stamps that never claimed it — a test that passes by not testing. Every claimed
        # identity of every stamp is corrupted in turn, and every one must be caught.
        for name, path, reader, _why, _w in RS.STAMPS:
            shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
            claimed = [k for k, v in reader(tmp).items() if v]
            ok(bool(claimed), '%s claims at least one identity (it can fail)' % name)
            for ident in claimed:
                shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
                full = os.path.join(tmp, path)
                raw = open(full).read()
                real = TRUTH[ident]
                stale = raw
                for width in (len(real), 12, 8):
                    stale = stale.replace(real[:width], 'd' * width)
                open(full, 'w').write(stale)
                _, bad = RS.check(tmp, verbose=False)
                ok([b for b in bad if b[0] == name],
                   'a stale %s in %s is DETECTED' % (ident, name))

        # ---- short forms are honoured, not flagged ---------------------------------------------
        shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
        _, bad = RS.check(tmp, verbose=False)
        ok(not bad, 'a stamp carrying an 8- or 12-char prefix agrees rather than false-alarming')
        ok(RS._agrees('e' * 8, 'e' * 32) and not RS._agrees('d' * 8, 'e' * 32),
           'prefix agreement discriminates: a matching prefix passes, a different one fails')
        ok(RS._agrees(None, 'e' * 32), 'a stamp that makes no claim for one identity is not a disagreement')

        # ---- THE VACUITY GUARD -----------------------------------------------------------------
        shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
        p = os.path.join(tmp, 'ui/data/club_valuation.js')
        open(p, 'w').write('window.__X__ = ' + json.dumps({'stamp': {'baseYear': 2026}}) + ';\n')
        _, bad = RS.check(tmp, verbose=False)
        ok([b for b in bad if b[0] == 'club_valuation'],
           'a stamp that has stopped claiming ANY identity is REFUSED as vacuous, not passed')

        # ---- an unreadable stamp is a failure, never a pass -------------------------------------
        shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
        open(os.path.join(tmp, 'ui/data/club_valuation.js'), 'w').write('window.__X__ = {oops;\n')
        _, bad = RS.check(tmp, verbose=False)
        ok([b for b in bad if b[0] == 'club_valuation'], 'an unreadable stamp fails closed')

        # ---- apply REFUSES to move the carrier or to run a build --------------------------------
        shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
        b = os.path.join(tmp, 'data/expected_boot.json')
        d = json.load(open(b)); d['engine_head'] = 'd' * 32
        json.dump(d, open(b, 'w'), indent=2)
        try:
            RS.apply(tmp)
            refused = False
        except SystemExit as exc:
            refused = 'CARRIER' in str(exc) or 'carrier' in str(exc).lower()
        ok(refused, 'apply REFUSES to move expected_boot — moving the carrier is a landing act')

        shutil.rmtree(tmp); os.makedirs(tmp); fixture(tmp)
        sp = os.path.join(tmp, 'engine/rl_after/ingestion/sibling_repin_state.json')
        json.dump({'source_store_md5': 'x' * 32, 'fv_identity': TRUTH['fv']}, open(sp, 'w'))
        try:
            RS.apply(tmp)
            refused2 = False
        except SystemExit as exc:
            refused2 = 'sibling' in str(exc).lower()
        ok(refused2, 'apply REFUSES the sibling sidecar — its writer REBUILDS, and a build belongs '
                     'in a transaction that can abort')

        # ---- THE MEASURERS ARE THE LANDER'S, on the real repo ----------------------------------
        RS.measure = real_measure
        from tools.landing import steps as ST

        class _Ctx(object):
            root = ROOT
        mine = RS.measure(ROOT)
        theirs = {k: str(fn(_Ctx())) for k, fn in ST.PIN_MEASURERS.items()}
        ok(set(mine) == set(ST.PIN_MEASURERS),
           'restamp measures exactly the identities the landing transaction pins (%d)' % len(mine))
        ok(all(str(mine[k]) == theirs[k] for k in mine),
           'and every measured value is byte-identical to the lander\'s own measurer')

        # ---- the live tree is coherent ----------------------------------------------------------
        _, bad = RS.check(ROOT, verbose=False)
        ok(not bad, 'the live repository: every stamp agrees with the tree')

        print('  ' + '-' * 70)
        print('RESTAMP TESTS: %s' % ('ALL %d PASS' % n if not fails else '%d FAIL / %d' % (fails, n)))
        return 1 if fails else 0
    finally:
        RS.measure = real_measure
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
