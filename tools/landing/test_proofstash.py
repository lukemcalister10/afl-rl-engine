#!/usr/bin/env python3
"""THE PROOF STASH — unit tests for both slices (build: shrink S13; sibling: shrink S8).

Run:  python3 tools/landing/test_proofstash.py        (exit 0 = all pass)

WHY THIS FILE EXISTS. The stash is the one instrument in the landing whose whole purpose is to NOT
run the thing it is standing in for, and the lander selftest deliberately disables it (a cached proof
would hollow out the 43 legs). That combination means the stash's own logic was, until this file,
proved by nothing at all. What is tested here is exactly the decision boundary: when a hit is used,
when it is refused, and that a refusal always falls through to the real build rather than to a guess.
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


class FakeSR(object):
    """Stands in for the sibling_repin module: one build_sibling that counts its calls."""
    def __init__(self, sib):
        self.calls = 0
        self._sib = sib

        def build_sibling(repo_root, with_forward=True):
            self.calls += 1
            return dict(self._sib)
        self.build_sibling = build_sibling


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
    SIB = {'board_md5': 'bal-1', 'forward_board_md5': 'fwd-1', 'source_store_md5': 'S1',
           'fv_identity': 'F1', 'rl_model_md5': 'M1', 'vector': {'a': 1}}

    try:
        ST.PIN_MEASURERS = with_identities(IDS)
        print('PROOF STASH TESTS\n  ' + '-' * 60)

        # ---- the key -------------------------------------------------------------------------
        c = Ctx(work)
        k1 = PS.sibling_key(c)
        ST.PIN_MEASURERS = with_identities(dict(IDS, store='S2'))
        k2 = PS.sibling_key(c)
        ok(k1 != k2, 'the sibling key moves when ANY input identity moves (store)')
        ST.PIN_MEASURERS = with_identities(dict(IDS, config='C2'))
        ok(PS.sibling_key(c) != k1, '...and when the config moves')
        ST.PIN_MEASURERS = with_identities(IDS)
        ok(PS.sibling_key(c) == k1, '...and is stable when nothing moved')
        c2 = Ctx(work, act='act-b')
        ok(PS.sibling_key(c2) != k1, 'a different act never shares a key with another act')

        # ---- MISS -> real build, and the proof is banked --------------------------------------
        sr = FakeSR(SIB)
        restore = ST._install_sibling_stash(c, sr)
        got = sr.build_sibling(ROOT)
        restore()
        ok(sr.calls == 1 and got['board_md5'] == 'bal-1', 'a MISS runs the real build')
        ok(PS.load('sibling', k1) is not None, '...and banks the proof under the key')

        # ---- HIT -> installed, nothing rebuilt -------------------------------------------------
        sr2 = FakeSR(SIB)
        c3 = Ctx(work)
        restore = ST._install_sibling_stash(c3, sr2)
        got = sr2.build_sibling(ROOT)
        restore()
        ok(sr2.calls == 0, 'a HIT on unchanged inputs does NOT rebuild')
        ok(got['board_md5'] == 'bal-1' and got['forward_board_md5'] == 'fwd-1',
           '...and returns the proven identity')
        ok(any('PROVEN EARLIER' in x for x in c3.lines), '...and says so in the transcript')

        # ---- the independent provenance check --------------------------------------------------
        # Same key, but the entry's OWN recorded store no longer matches live. This is the check
        # that does not trust the key: it must refuse and rebuild.
        stale = dict(SIB, source_store_md5='S-OLD')
        PS.save('sibling', k1, {'sib': _write(work, stale)}, {'board_md5': 'bal-1'})
        sr3 = FakeSR(SIB)
        c4 = Ctx(work)
        restore = ST._install_sibling_stash(c4, sr3)
        got = sr3.build_sibling(ROOT)
        restore()
        ok(sr3.calls == 1, 'an entry whose OWN recorded store does not match live is REFUSED, and '
                           'the full build runs')
        ok(any('DISCARDED' in x for x in c4.lines), '...and says why')
        ok(got['source_store_md5'] == 'S1', '...and the answer is the freshly built one')

        # the same, one field at a time — fv and rl_model are checked independently of the store
        for field, bad in (('fv_identity', 'F-OLD'), ('rl_model_md5', 'M-OLD')):
            PS.save('sibling', k1, {'sib': _write(work, dict(SIB, **{field: bad}))}, {})
            srx = FakeSR(SIB)
            restore = ST._install_sibling_stash(Ctx(work), srx)
            srx.build_sibling(ROOT)
            restore()
            ok(srx.calls == 1, 'a stale %s is caught independently of the store' % field)

        # ---- a corrupt entry is discarded, never trusted ---------------------------------------
        PS.save('sibling', k1, {'sib': _write(work, SIB)}, {})
        ent = os.path.join(stash, 'sibling_%s' % k1)
        with open(os.path.join(ent, 'sib'), 'w') as f:
            f.write('{"board_md5": "TAMPERED"}')
        ok(PS.load('sibling', k1) is None, 'a tampered entry fails its own md5 and loads as a miss')
        src = FakeSR(SIB)
        restore = ST._install_sibling_stash(Ctx(work), src)
        got = src.build_sibling(ROOT)
        restore()
        ok(src.calls == 1 and got['board_md5'] == 'bal-1',
           '...and the landing rebuilds rather than using tampered bytes')

        # ---- NEVER in a selftest or a fault run ------------------------------------------------
        PS.save('sibling', k1, {'sib': _write(work, SIB)}, {})
        for label, kw in (('selftest', {'selftest': True}), ('fault run', {'fault': 'sibling'})):
            srs = FakeSR(SIB)
            cs = Ctx(work, **kw)
            restore = ST._install_sibling_stash(cs, srs)
            srs.build_sibling(ROOT)
            restore()
            ok(srs.calls == 1, 'the stash is NEVER consulted in a %s' % label)

        # ---- the patch is scoped: the module is restored ---------------------------------------
        srr = FakeSR(SIB)
        original = srr.build_sibling
        restore = ST._install_sibling_stash(Ctx(work), srr)
        ok(srr.build_sibling is not original, 'the step patches build_sibling while it runs')
        restore()
        ok(srr.build_sibling is original,
           '...and restores it, so the gate check and the CLI are untouched by landing policy')

        # ---- with_forward=False is not the cached shape ----------------------------------------
        srf = FakeSR(SIB)
        restore = ST._install_sibling_stash(Ctx(work), srf)
        srf.build_sibling(ROOT, with_forward=False)
        restore()
        ok(srf.calls == 1, 'a with_forward=False build is never served from the stash')

        # ---- a stash failure must never fail a landing -----------------------------------------
        cbad = Ctx('/nonexistent/work/dir')
        srb = FakeSR(SIB)
        ST.PIN_MEASURERS = with_identities(dict(IDS, board='B-NEW'))
        restore = ST._install_sibling_stash(cbad, srb)
        got = srb.build_sibling(ROOT)
        restore()
        ok(srb.calls == 1 and got['board_md5'] == 'bal-1',
           'an unwritable stash does not fail the landing — it just does not cache')
        ok(any('NOT stashed' in x for x in cbad.lines), '...and says so plainly')

        # ---- the key covers the build inputs PIN_MEASURERS never did (Phase 0.5, 2026-10-13) --
        ST.PIN_MEASURERS = with_identities(IDS)
        tree = tempfile.mkdtemp(prefix='proofstash_tree_')
        try:
            build_tree(tree)
            ct = Ctx(work, root=tree)
            kb0, ks0 = PS.build_key(ct), PS.sibling_key(ct)
            ok(PS.build_key(ct) == kb0 and PS.sibling_key(ct) == ks0,
               'both keys are stable while every build input holds')
            for rel, label in (('data/season_state.json', 'season_state.json'),
                               ('docs/owner_annotations/SITTER_2026_v1.csv', 'the pinned sitter sheet'),
                               ('data/q97m.pkl', 'q97m.pkl'), ('data/cm_400.pkl', 'cm_400.pkl'),
                               ('data/v0surf.pkl', 'v0surf.pkl')):
                build_tree(tree)
                before = (PS.build_key(ct), PS.sibling_key(ct))
                touch(tree, rel, 'MOVED ' + rel)
                after = (PS.build_key(ct), PS.sibling_key(ct))
                ok(before[0] != after[0] and before[1] != after[1],
                   'the build key AND the sibling key move when %s moves' % label)
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


def _write(work, obj):
    p = os.path.join(work, 'sib_in.json')
    with open(p, 'w') as f:
        json.dump(obj, f, sort_keys=True)
    return p


if __name__ == '__main__':
    sys.exit(main())
