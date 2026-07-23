"""FAIL-CLOSED R14 DISPOSABLE-FIXTURE tests + NEGATIVE CONTROLS (ITEM 408 item 6).

Proves scratch_fixture.materialize_r14 reconstructs the accepted Round-14 baseline INSIDE a disposable
scratch and FAILS CLOSED on every wrong historical relationship — and that the scratch uses the CURRENT
implementation code + CURRENT immutable model inputs (only the R14 dynamic release/runtime state is
historical). It never touches the real checkout.

Directive item-6 negative controls covered HERE (fixture boundary):
  1  an unavailable R14 anchor halts;
  2  a wrong expected R14 store md5 halts;
  3  a wrong expected R14 board md5 halts;
  4  a non-ancestor anchor halts;
  5  R19 ledger state cannot leak into an R14 scratch;
  6  R19 finalization state cannot leak into an R14 scratch;
  7  R19 movers outputs cannot leak into an R14 scratch;
  15 missing sibling support trees fail closed (rather than a partial sibling advance);
  16 historical dynamic restoration does NOT replace the current implementation source;
  17 the current immutable model inputs remain current (not overwritten by R14 dynamic restore);
  18 release-contract verification passes on the restored R14 fixture.

Controls (8)-(14) — a genuinely repeated applied round still refused by production dedup, the shipped
score-write gate OFF, no canonical production file changed during a proof, a disposable R14->R15 apply
advancing the canonical AND balanced/strict sibling targets under ONE transaction, failure injection /
rollback / crash recovery over the expanded canonical+sibling set — are PRESERVED in
failure_injection_proof.py, finalization_injection_proof.py, two_round_proof.py and catchup_proof.py.

Run:  python3 engine/rl_after/ingestion/test_r14_fixture.py
Exit 0 = ALL PASS.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RA = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(RA))
for p in (RA, HERE, os.path.join(REPO, 'session_2026-07-20', 'weekly_updater_hardening')):
    if p not in sys.path:
        sys.path.insert(0, p)

import scratch_fixture as SF          # noqa: E402


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


def _scratch_base():
    return os.environ.get('WK_SCRATCH_BASE') or tempfile.gettempdir()


def _good_r14_scratch():
    """A coherent R14 scratch via the shared factory (make_scratch -> materialize_r14)."""
    import failure_injection_proof as FI
    return FI.make_scratch('r14test')


def _expect_fixture_error(fn, needle=None, label=''):
    try:
        fn()
    except SF.FixtureError as e:
        if needle and needle.lower() not in str(e).lower():
            raise AssertionError("%s: FixtureError raised but message lacks %r:\n%s" % (label, needle, e))
        return str(e)
    raise AssertionError("%s: expected FixtureError, none raised" % label)


# ================================================================================================
# POSITIVE CONTROL — the fixture IS the accepted R14 baseline
# ================================================================================================
def test_positive_r14_baseline():
    scr = _good_r14_scratch()
    try:
        store = os.path.join(scr, 'engine', 'rl_after', 'rl_model_data.json')
        board = os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json')
        assert _md5(store) == SF.R14_STORE_MD5, "store not R14"
        assert _md5(board) == SF.R14_BOARD_MD5, "board not R14"
        boot = json.load(open(os.path.join(scr, 'data', 'expected_boot.json')))
        assert boot['as_of_round'] == 14 and boot['store'] == SF.R14_STORE_MD5
        assert boot['board'] == SF.R14_BOARD_MD5 and boot['balanced_board_md5'] == SF.R14_BALANCED_BOARD_MD5
        ss = json.load(open(os.path.join(scr, 'data', 'season_state.json')))
        assert ss['as_of_round'] == 14 and ss['source_store_md5'] == SF.R14_STORE_MD5
        led = json.load(open(os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json')))
        assert led.get('applied') == [], "R14 ledger must be empty"
        # control 18: the restored + re-sealed release contract verifies under a fenced mode
        _assert_contract_verifies(scr)
        print("  [PASS] positive: fixture is the accepted R14 baseline (store/board/boot/season/ledger + contract seal)")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def _assert_contract_verifies(scr):
    """control 18 — release_contract.verify(gate) passes on the restored R14 fixture."""
    import importlib.util
    spec = importlib.util.spec_from_file_location('rc_r14test', os.path.join(scr, 'release_contract.py'))
    rc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rc)
    saved = os.environ.get('RL_CONFIG_MODE')
    os.environ['RL_CONFIG_MODE'] = 'gate'
    try:
        rc.verify('gate', scr, halt=False)     # raises AssertionError on any incoherence
    finally:
        if saved is None:
            os.environ.pop('RL_CONFIG_MODE', None)
        else:
            os.environ['RL_CONFIG_MODE'] = saved


# ================================================================================================
# NEGATIVE CONTROLS — every wrong historical relationship fails closed
# ================================================================================================
def test_unavailable_anchor_halts():                                             # control 1
    non_git = tempfile.mkdtemp(prefix='r14_nogit_', dir=_scratch_base())
    scr = tempfile.mkdtemp(prefix='r14_scr_', dir=_scratch_base())
    try:
        _expect_fixture_error(lambda: SF.materialize_r14(scr, non_git),
                              needle='does not resolve', label='unavailable anchor')
        print("  [PASS] control 1: an unavailable R14 anchor halts (fail-closed)")
    finally:
        shutil.rmtree(non_git, ignore_errors=True)
        shutil.rmtree(scr, ignore_errors=True)


def test_non_ancestor_anchor_halts():                                            # control 4
    # A commit that RESOLVES but is NOT an ancestor of HEAD must halt. Build an isolated temp repo with
    # a diverging commit so the control never depends on which remote refs a runner happened to fetch.
    tmp = tempfile.mkdtemp(prefix='r14_divrepo_', dir=_scratch_base())

    def g(*a):
        return subprocess.run(['git', '-C', tmp, '-c', 'user.name=t', '-c', 'user.email=t@t', *a],
                              capture_output=True, text=True)
    g('init', '-q')
    with open(os.path.join(tmp, 'a'), 'w') as f:
        f.write('base\n')
    g('add', 'a'); g('commit', '-q', '-m', 'base')
    g('checkout', '-q', '-b', 'sidebranch')
    with open(os.path.join(tmp, 'b'), 'w') as f:
        f.write('side\n')
    g('add', 'b'); g('commit', '-q', '-m', 'side')
    side_sha = g('rev-parse', 'HEAD').stdout.strip()
    # move HEAD back to the base line (master/main) so `side_sha` is NOT an ancestor of HEAD
    base_branch = g('rev-parse', '--abbrev-ref', 'master').stdout.strip()
    if base_branch in ('', 'HEAD', 'master') and g('rev-parse', '-q', '--verify', 'master').returncode != 0:
        base_branch = 'main'
    g('checkout', '-q', base_branch if base_branch and base_branch != 'HEAD' else 'master')
    saved = SF.R14_ANCHOR
    scr = tempfile.mkdtemp(prefix='r14_scr_', dir=_scratch_base())
    try:
        SF.R14_ANCHOR = side_sha
        _expect_fixture_error(lambda: SF.materialize_r14(scr, tmp),
                              needle='not an ancestor', label='non-ancestor anchor')
        print("  [PASS] control 4: a non-ancestor anchor halts (fail-closed)")
    finally:
        SF.R14_ANCHOR = saved
        shutil.rmtree(tmp, ignore_errors=True)
        shutil.rmtree(scr, ignore_errors=True)


def test_wrong_store_md5_halts():                                                # control 2
    scr = _good_r14_scratch()
    try:
        store = os.path.join(scr, 'engine', 'rl_after', 'rl_model_data.json')
        with open(store, 'ab') as f:                      # tamper: no longer the R14 store bytes
            f.write(b'\n')
        _expect_fixture_error(lambda: SF._verify_r14(scr), needle='store md5', label='wrong store md5')
        print("  [PASS] control 2: a wrong R14 store md5 halts (fail-closed)")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def test_wrong_board_md5_halts():                                                # control 3
    scr = _good_r14_scratch()
    try:
        board = os.path.join(scr, 'data', 'rl_build', 'rl_app_data.json')
        with open(board, 'ab') as f:
            f.write(b'\n')
        _expect_fixture_error(lambda: SF._verify_r14(scr), needle='board md5', label='wrong board md5')
        print("  [PASS] control 3: a wrong R14 canonical-board md5 halts (fail-closed)")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def test_r19_ledger_cannot_leak():                                               # control 5
    scr = _good_r14_scratch()
    try:
        lp = os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'applied_rounds_ledger.json')
        led = json.load(open(lp))
        led.setdefault('applied', []).append('afl-player-v1-deadbeefdeadbeefdead|2026|15')
        with open(lp, 'w') as f:
            json.dump(led, f)
        _expect_fixture_error(lambda: SF._verify_r14(scr), needle='R15+', label='R19 ledger leak')
        print("  [PASS] control 5: R19 ledger state cannot leak into an R14 scratch (fail-closed)")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def test_r19_finalization_cannot_leak():                                         # control 6
    scr = _good_r14_scratch()
    try:
        fp = os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'finalization_state.json')
        with open(fp, 'w') as f:
            json.dump({'finalized': [15, 16, 17, 18, 19]}, f)
        _expect_fixture_error(lambda: SF._verify_r14(scr), needle='finalization_state',
                              label='R19 finalization leak')
        print("  [PASS] control 6: R19 finalization state cannot leak into an R14 scratch (fail-closed)")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def test_r19_movers_cannot_leak():                                               # control 7
    scr = _good_r14_scratch()
    try:
        md = os.path.join(scr, 'engine', 'rl_after', 'ingestion', 'movers')
        os.makedirs(md, exist_ok=True)
        with open(os.path.join(md, 'movers_R19.json'), 'w') as f:
            f.write('{}')
        _expect_fixture_error(lambda: SF._verify_r14(scr), needle='movers', label='R19 movers leak')
        print("  [PASS] control 7: R19 movers outputs cannot leak into an R14 scratch (fail-closed)")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def test_missing_sibling_trees_fail_closed():                                    # control 15
    empty_repo = tempfile.mkdtemp(prefix='r14_norepo_', dir=_scratch_base())     # lacks the sibling trees
    scr = tempfile.mkdtemp(prefix='r14_scr_', dir=_scratch_base())
    try:
        _expect_fixture_error(lambda: SF.install_sibling_support_trees(scr, empty_repo),
                              needle='sibling support tree', label='missing sibling trees')
        print("  [PASS] control 15: missing sibling support trees fail closed (no partial advance)")
    finally:
        shutil.rmtree(empty_repo, ignore_errors=True)
        shutil.rmtree(scr, ignore_errors=True)


def test_current_source_not_replaced():                                          # control 16
    scr = _good_r14_scratch()
    try:
        for rel in ('engine/rl_after/_merged_recover.py', 'engine/rl_after/rl_model.py',
                    'engine/rl_after/ingestion/staged_apply.py', 'engine/rl_after/ingestion/round_apply.py'):
            assert _md5(os.path.join(scr, rel)) == _md5(os.path.join(REPO, rel)), \
                "%s in the scratch != current checkout (historical restore replaced current source!)" % rel
        # and the engine identity the manifest pins is the CURRENT engine, NOT the R14-era engine head
        boot = json.load(open(os.path.join(scr, 'data', 'expected_boot.json')))
        cur = _md5(os.path.join(REPO, 'engine', 'rl_after', '_merged_recover.py'))
        assert boot['engine_head'] == cur, "manifest engine_head is not the CURRENT engine"
        assert boot['engine_head'] != 'dc7e34b0d50470897af237c638236868', "manifest pins the R14-era engine head"
        print("  [PASS] control 16: historical restore does NOT replace current implementation source")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def test_current_immutable_inputs_stay_current():                                # control 17
    scr = _good_r14_scratch()
    try:
        for rel in ('data/model_config.json', 'LTI_REGISTER.md'):
            assert _md5(os.path.join(scr, rel)) == _md5(os.path.join(REPO, rel)), \
                "%s in the scratch != current checkout (immutable input drifted)" % rel
        # the whole forward_valuation source set matches the current checkout, file by file
        fv_rel = os.path.join('engine', 'forward_valuation')
        for name in sorted(os.listdir(os.path.join(REPO, fv_rel))):
            if name.endswith('.py'):
                assert _md5(os.path.join(scr, fv_rel, name)) == _md5(os.path.join(REPO, fv_rel, name)), \
                    "forward_valuation/%s drifted from the current checkout" % name
        print("  [PASS] control 17: current immutable model inputs remain current")
    finally:
        shutil.rmtree(scr, ignore_errors=True)


def run_all():
    tests = [
        test_positive_r14_baseline,
        test_unavailable_anchor_halts,
        test_non_ancestor_anchor_halts,
        test_wrong_store_md5_halts,
        test_wrong_board_md5_halts,
        test_r19_ledger_cannot_leak,
        test_r19_finalization_cannot_leak,
        test_r19_movers_cannot_leak,
        test_missing_sibling_trees_fail_closed,
        test_current_source_not_replaced,
        test_current_immutable_inputs_stay_current,
    ]
    print("R14 disposable-fixture fail-closed tests + negative controls:")
    for t in tests:
        t()
    print("ALL R14 FIXTURE CONTROLS PASS")


if __name__ == '__main__':
    run_all()
    sys.exit(0)
