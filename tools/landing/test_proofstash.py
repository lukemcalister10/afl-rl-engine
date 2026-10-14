#!/usr/bin/env python3
"""THE PROOF STASH — unit tests for the build slice (shrink S13).

Run:  python3 tools/landing/test_proofstash.py        (exit 0 = all pass)

RETIRED 2026-10-14: the sibling slice (shrink S8 — `sibling_key`, the `sibling` stash kind and the
`_install_sibling_stash` patch) and every case here that exercised it. The balanced sibling is no
longer built by any landing (owner word, 2026-10-14), so there is no sibling proof to cache.

WHY THIS FILE EXISTS. The stash is the one instrument in the landing whose whole purpose is to NOT
run the thing it is standing in for, and the lander selftest deliberately disables it (a cached proof
would hollow out the legs). That combination means the stash's own logic was, until this file,
proved by nothing at all. What is tested here is exactly the decision boundary: when a key moves,
when it holds, and that every build input the key is meant to cover actually moves it.
"""
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)

from tools.landing import proofstash as PS       # noqa: E402
from tools.landing import steps as ST            # noqa: E402

fails = 0
n = 0


def ok(cond, label):
    global fails, n
    n += 1
    if cond:
        print('  [PASS] ' + label)
    else:
        fails += 1
        print('  [FAIL] ' + label)


class Opts(object):
    def __init__(self, selftest=False):
        self.selftest = selftest


class Ctx(object):
    """The smallest ctx the stash touches: options, fault state, spec, work dir, log."""
    def __init__(self, work_dir, selftest=False, fault=None, act='act-a', root=None):
        self.opts = Opts(selftest)
        self.fault = fault
        self.spec = {'act': act, 'act_kind': 'lever', 'prereg': {'board_after': 'bbb'}}
        self.root = root or ROOT
        self.work_dir = work_dir
        self.lines = []

    def log(self, msg):
        self.lines.append(msg)


def build_tree(root, sheet='docs/owner_annotations/SITTER_2026_v1.csv'):
    """A fake repo root carrying every build input the key covers beyond PIN_MEASURERS."""
    for rel, body in (('data/season_state.json', '{"as_of_round": 24}\n'),
                      ('data/q97m.pkl', 'q97m-bytes'), ('data/cm_400.pkl', 'cm400-bytes'),
                      ('data/v0surf.pkl', 'v0surf-bytes'), (sheet, 'key,injured\na,N\n'),
                      ('data/sheet_pins.json', json.dumps({'sheet_path': sheet}))):
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w') as f:
            f.write(body)


def touch(root, rel, body):
    with open(os.path.join(root, rel), 'w') as f:
        f.write(body)


def with_identities(ids):
    """Replace PIN_MEASURERS with fixed readings, so a test can move one input at a time."""
    return {k: (lambda ctx, v=v: v) for k, v in ids.items()}


def main():
    stash = tempfile.mkdtemp(prefix='proofstash_test_')
    work = tempfile.mkdtemp(prefix='proofstash_work_')
    os.environ['LANDING_PROOF_STASH'] = stash
    saved_measurers = ST.PIN_MEASURERS

    IDS = {'board': 'B1', 'store': 'S1', 'engine_head': 'E1', 'rl_model': 'M1',
           'register': 'R1', 'v0surf': 'V1', 'config': 'C1', 'fv': 'F1'}

    try:
        ST.PIN_MEASURERS = with_identities(IDS)
        print('PROOF STASH TESTS\n  ' + '-' * 60)

        # ---- the retirement is structural, not a comment ----------------------------------------
        ok(not hasattr(PS, 'sibling_key') and not hasattr(ST, '_install_sibling_stash')
           and not hasattr(ST, 'sibling'),
           'the sibling slice is GONE: no sibling_key, no stash patch, no sibling step (2026-10-14)')
        ok('sibling' not in [s[0] for s in ST.LEVER_SEQUENCE]
           and 'sibling' not in [s[0] for s in ST.EDIT_SEQUENCE]
           and 'sibling' not in [s[0] for s in ST.ROUND_SEQUENCE],
           '...and no sequence registers a `sibling` step')

        # ---- the key -------------------------------------------------------------------------
        tree = tempfile.mkdtemp(prefix='proofstash_tree_')
        try:
            build_tree(tree)
            c = Ctx(work, root=tree)
            k1 = PS.build_key(c)
            ST.PIN_MEASURERS = with_identities(dict(IDS, store='S2'))
            k2 = PS.build_key(c)
            ok(k1 != k2, 'the build key moves when ANY input identity moves (store)')
            ST.PIN_MEASURERS = with_identities(dict(IDS, config='C2'))
            ok(PS.build_key(c) != k1, '...and when the config moves')
            ST.PIN_MEASURERS = with_identities(IDS)
            ok(PS.build_key(c) == k1, '...and is stable when nothing moved')
            c2 = Ctx(work, act='act-b', root=tree)
            ok(PS.build_key(c2) != k1, 'a different act never shares a key with another act')
            c3 = Ctx(work, root=tree)
            c3.spec['prereg'] = {'board_after': 'other'}
            ok(PS.build_key(c3) != k1, 'a different prereg prediction never shares a key either')

            # ---- the stash round-trips and verifies its own bytes ---------------------------------
            src = os.path.join(work, 'board.json')
            with open(src, 'w') as f:
                f.write('{"board": "bbb"}')
            PS.save('build', k1, {'board': src}, {'board_md5': 'bbb'})
            hit = PS.load('build', k1)
            ok(hit is not None and hit[1].get('board_md5') == 'bbb'
               and open(hit[0]['board']).read() == '{"board": "bbb"}',
               'a saved build proof loads back under its key with its facts and bytes')
            ok(PS.load('build', 'no-such-key') is None, 'an unknown key is a MISS, not an error')
            with open(os.path.join(stash, 'build_%s' % k1, 'board'), 'w') as f:
                f.write('{"board": "TAMPERED"}')
            ok(PS.load('build', k1) is None, 'a tampered entry fails its own md5 and loads as a miss')

            # ---- the key covers the build inputs PIN_MEASURERS never did (Phase 0.5, 2026-10-13) --
            ct = Ctx(work, root=tree)
            kb0 = PS.build_key(ct)
            ok(PS.build_key(ct) == kb0, 'the key is stable while every build input holds')
            for rel, label in (('data/season_state.json', 'season_state.json'),
                               ('docs/owner_annotations/SITTER_2026_v1.csv', 'the pinned sitter sheet'),
                               ('data/q97m.pkl', 'q97m.pkl'), ('data/cm_400.pkl', 'cm_400.pkl'),
                               ('data/v0surf.pkl', 'v0surf.pkl')):
                build_tree(tree)
                before = PS.build_key(ct)
                touch(tree, rel, 'MOVED ' + rel)
                ok(PS.build_key(ct) != before, 'the build key moves when %s moves' % label)
            # the sheet is whichever file the pins name — repoint the pins, the key moves with it
            build_tree(tree)
            k_pinned = PS.build_key(ct)
            build_tree(tree, sheet='docs/owner_annotations/SITTER_2027_v1.csv')
            ok(PS.build_key(ct) != k_pinned, 'repointing data/sheet_pins.json at another sheet moves the key')
            # v0surf is in the key EVEN WHEN the act declares it as moving (build_key skips moved pins)
            build_tree(tree)
            ct.spec['identities'] = {'moves': ['v0surf']}
            k_mv = PS.build_key(ct)
            touch(tree, 'data/v0surf.pkl', 'MOVED anyway')
            ok(PS.build_key(ct) != k_mv, 'v0surf moves the build key even when the act declares it moving')
            ct.spec.pop('identities')
            # an absent input is an identity of its own, not an error
            build_tree(tree)
            k_all = PS.build_key(ct)
            os.remove(os.path.join(tree, 'data', 'season_state.json'))
            ok(PS.build_key(ct) != k_all, 'an absent season_state.json is its own identity (no error, no match)')
            # a stash written under the old key shape is never confirmed: the schema is in the basis
            ok(PS.KEY_SCHEMA >= 2, 'the key schema was bumped, so every pre-existing stash misses')
            inputs = PS._build_inputs(ct)
            ok(set(inputs) >= {'data/season_state.json', 'data/q97m.pkl', 'data/cm_400.pkl',
                               'data/v0surf.pkl', 'sheet:docs/owner_annotations/SITTER_2026_v1.csv'},
               '_build_inputs names every covered file: %s' % sorted(inputs))
        finally:
            shutil.rmtree(tree, ignore_errors=True)

        print('  ' + '-' * 60)
        print('PROOF STASH TESTS: %s' % ('ALL %d PASS' % n if not fails else '%d FAIL / %d' % (fails, n)))
        return 1 if fails else 0
    finally:
        ST.PIN_MEASURERS = saved_measurers
        shutil.rmtree(stash, ignore_errors=True)
        shutil.rmtree(work, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
