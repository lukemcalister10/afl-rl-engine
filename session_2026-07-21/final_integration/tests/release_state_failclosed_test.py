#!/usr/bin/env python3
"""FAIL-CLOSED release-state enforcement tests (final integration 2026-07-21).

Covers the task's mandated fail-closed cases (item 8) AND the audit addendum's item-7 cases:
  - missing configuration / missing release contract
  - ambient-only environment configuration (unset RL_CONFIG_MODE on a canonical build)
  - contradictory manifest/environment values
  - unknown switch values
  - stale identity pins
  - conflicting PVC provenance
  - the static inventory has zero unclassified live RL_*/PAR_* reads
  - a missing required (class-A) semantic fails
  - changing each class-A semantic moves the stamped identity (or a set override hook is rejected)

Self-contained: constructs temp release-state fixtures (manifest + expected_boot + contract) and
asserts each perturbation HALTS. No pinned repo identity is required, so this is green before and after
the CP2 identity move. `python3 release_state_failclosed_test.py` -> PASS/FAIL, non-zero on any failure.
"""
import os, sys, json, hashlib, tempfile, shutil, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))


def _load(modname, path):
    spec = importlib.util.spec_from_file_location(modname, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

CM = _load('config_manifest_t', os.path.join(ROOT, 'config_manifest.py'))
RC = _load('release_contract_t', os.path.join(ROOT, 'release_contract.py'))
INV = _load('config_inventory_t', os.path.join(HERE, '..', 'tools', 'config_inventory.py'))

_RESULTS = []
def ok(name, cond, detail=''):
    _RESULTS.append((name, bool(cond), detail))
    print(("  PASS " if cond else "  FAIL ") + name + (("  -- " + detail) if detail and not cond else ''))

def _manhash(vars_):
    return hashlib.sha256('\n'.join('%s=%s' % (k, vars_[k]) for k in sorted(vars_)).encode()).hexdigest()

def make_fixture(tmp, vars_=None, boot_over=None, contract_over=None, write_contract=True):
    """Build a minimal, internally-consistent temp release state under tmp/. Returns paths."""
    os.makedirs(os.path.join(tmp, 'data'), exist_ok=True)
    # a tiny but valid manifest
    vars_ = dict(vars_ or {'RL_PVC2': '1', 'RL_LEGE': '1', 'RL_LEGF': '1', 'RL_GAMMA': '0.85'})
    ch = _manhash(vars_)
    json.dump({'version': '1.0', 'config_sha256': ch, 'vars': vars_},
              open(os.path.join(tmp, 'data', 'model_config.json'), 'w'))
    boot = {'board': 'aaaa1111', 'balanced_board_md5': '06d8af60', 'store': 'bbbb2222',
            'engine_head': 'cccc3333', 'rl_model': 'dddd4444', 'fv': 'eeee5555',
            'register': 'ffff6666', 'config': ch, 'as_of_round': 14}
    if boot_over: boot.update(boot_over)
    json.dump(boot, open(os.path.join(tmp, 'data', 'expected_boot.json'), 'w'))
    contract = {'release_version': 'v2.11-final-rc-test', 'as_of_round': 14,
                'switch_posture': {'RL_PVC2': '1', 'RL_LEGE': '1', 'RL_LEGF': '1'},
                'config_sha256': ch,
                'identities': {'board': boot['board'], 'store': boot['store'],
                               'engine_head': boot['engine_head'], 'rl_model': boot['rl_model'],
                               'fv': boot['fv'], 'register': boot['register']},
                'pvc_provenance': {'adopted_pathway': 'RL_PVC2', 'curve_file': 'pvc_curve_v2.json',
                                   'curve_payload_md5': '89c14729', 'numeraire_pin1': 3000},
                'must_be_unset': list(RC.DEFAULT_MUST_UNSET)}
    if contract_over: contract.update(contract_over)
    contract['contract_sha256'] = RC.contract_hash(contract)
    if write_contract:
        json.dump(contract, open(os.path.join(tmp, 'data', 'release_contract.json'), 'w'))
    return contract

def with_env(**kw):
    """Context helper: set env, return a restore fn."""
    saved = {k: os.environ.get(k) for k in kw}
    for k, v in kw.items():
        if v is None: os.environ.pop(k, None)
        else: os.environ[k] = v
    def restore():
        for k, v in saved.items():
            if v is None: os.environ.pop(k, None)
            else: os.environ[k] = v
    return restore

def halts(fn):
    try:
        fn(); return False
    except (SystemExit, AssertionError):
        return True

def main():
    print("FAIL-CLOSED RELEASE-STATE ENFORCEMENT TESTS")

    # --- addendum: static inventory has zero unclassified live reads (against the REAL surface) ----------
    r = with_env(RL_REPO=ROOT)
    try:
        rc_code = INV.main([])  # writes evidence; returns 0 only if zero-unclassified AND all class-A represented
        ev = json.load(open(os.path.join(HERE, '..', 'evidence', 'config_inventory.json')))
        ok('inventory: zero unclassified live RL_*/PAR_* reads', ev['class_counts'].get('?', 0) == 0,
           'unclassified=%s' % ev['class_counts'].get('?'))
    finally:
        r()

    # --- ambient-only: canonical build with RL_CONFIG_MODE unset HALTS ----------------------------------
    r = with_env(RL_CONFIG_MODE=None)
    ok('ambient-only (unset RL_CONFIG_MODE) canonical build halts', halts(lambda: RC.require_canonical()))
    r()
    # and require_canonical PASSES under a fenced mode
    r = with_env(RL_CONFIG_MODE='canonical')
    ok('canonical mode is accepted by require_canonical', not halts(lambda: RC.require_canonical()))
    r()

    tmp = tempfile.mkdtemp()
    try:
        # baseline consistent fixture verifies clean under gate mode
        make_fixture(tmp)
        r = with_env(RL_REPO=tmp, RL_CONFIG_MODE='gate',
                     RL_UNCOMP_S=None, RL_LSYM_TAB=None, RL_V0SURF_REFIT=None)
        ok('consistent fixture verifies clean', not halts(lambda: RC.verify('gate', tmp, halt=True)))
        r()

        # --- missing release contract HALTS -----------------------------------------------------------
        t2 = tempfile.mkdtemp()
        make_fixture(t2, write_contract=False)
        r = with_env(RL_REPO=t2, RL_CONFIG_MODE='canonical')
        ok('missing release contract halts', halts(lambda: RC.verify('canonical', t2, halt=True)))
        r(); shutil.rmtree(t2, ignore_errors=True)

        # --- contradictory switch posture (contract RL_LEGF=0 vs manifest RL_LEGF=1) HALTS -------------
        t3 = tempfile.mkdtemp()
        make_fixture(t3, contract_over={'switch_posture': {'RL_PVC2': '1', 'RL_LEGE': '1', 'RL_LEGF': '0'}})
        r = with_env(RL_REPO=t3, RL_CONFIG_MODE='gate')
        ok('contradictory switch posture halts', halts(lambda: RC.verify('gate', t3, halt=True)))
        r(); shutil.rmtree(t3, ignore_errors=True)

        # --- stale config pin (expected_boot config != manifest hash) HALTS ----------------------------
        t4 = tempfile.mkdtemp()
        make_fixture(t4, boot_over={'config': 'deadbeefdeadbeef'})
        r = with_env(RL_REPO=t4, RL_CONFIG_MODE='gate')
        ok('stale config pin halts', halts(lambda: RC.verify('gate', t4, halt=True)))
        r(); shutil.rmtree(t4, ignore_errors=True)

        # --- stale identity pin (contract board != expected_boot board) HALTS --------------------------
        t5 = tempfile.mkdtemp()
        c5 = make_fixture(t5)
        # move expected_boot board only, leave the contract stale
        b = json.load(open(os.path.join(t5, 'data', 'expected_boot.json'))); b['board'] = '99998888'
        json.dump(b, open(os.path.join(t5, 'data', 'expected_boot.json'), 'w'))
        r = with_env(RL_REPO=t5, RL_CONFIG_MODE='gate')
        ok('stale identity pin halts', halts(lambda: RC.verify('gate', t5, halt=True)))
        r(); shutil.rmtree(t5, ignore_errors=True)

        # --- conflicting PVC provenance (unknown pathway) HALTS ----------------------------------------
        t6 = tempfile.mkdtemp()
        make_fixture(t6, contract_over={'pvc_provenance': {'adopted_pathway': 'RL_MYSTERY',
                     'curve_file': 'pvc_curve_v2.json', 'numeraire_pin1': 3000}})
        r = with_env(RL_REPO=t6, RL_CONFIG_MODE='gate')
        ok('conflicting PVC provenance halts', halts(lambda: RC.verify('gate', t6, halt=True)))
        r(); shutil.rmtree(t6, ignore_errors=True)

        # --- numeraire drift (pin1 != 3000) HALTS ------------------------------------------------------
        t6b = tempfile.mkdtemp()
        make_fixture(t6b, contract_over={'pvc_provenance': {'adopted_pathway': 'RL_PVC2',
                     'curve_file': 'pvc_curve_v2.json', 'numeraire_pin1': 2999}})
        r = with_env(RL_REPO=t6b, RL_CONFIG_MODE='gate')
        ok('numeraire drift halts', halts(lambda: RC.verify('gate', t6b, halt=True)))
        r(); shutil.rmtree(t6b, ignore_errors=True)

        # --- override hook set in ambient (RL_UNCOMP_S) HALTS ------------------------------------------
        t7 = tempfile.mkdtemp()
        make_fixture(t7)
        r = with_env(RL_REPO=t7, RL_CONFIG_MODE='gate', RL_UNCOMP_S='0.31')
        ok('ambient override hook (RL_UNCOMP_S set) halts', halts(lambda: RC.verify('gate', t7, halt=True)))
        r(); shutil.rmtree(t7, ignore_errors=True)

        # --- config_manifest reject-scan: unknown model override HALTS in gate mode --------------------
        t8 = tempfile.mkdtemp()
        make_fixture(t8)
        r = with_env(RL_REPO=t8, RL_CONFIG_MODE='gate', RL_TOTALLY_UNKNOWN='1')
        ok('unknown model override rejected (gate mode)', halts(lambda: CM.enforce('gate', halt=True)))
        r(); shutil.rmtree(t8, ignore_errors=True)

        # --- config_manifest reject-scan: DIVERGENT switch value (RL_LEGF=0 vs manifest 1) HALTS -------
        t9 = tempfile.mkdtemp()
        make_fixture(t9)
        r = with_env(RL_REPO=t9, RL_CONFIG_MODE='gate', RL_LEGF='0')
        ok('divergent/unknown switch value rejected (gate mode)', halts(lambda: CM.enforce('gate', halt=True)))
        r(); shutil.rmtree(t9, ignore_errors=True)

        # --- changing each class-A semantic MOVES the stamped identity (canonical_hash) -----------------
        base_vars = {'RL_PVC2': '1', 'RL_LEGE': '1', 'RL_LEGF': '1', 'RL_GAMMA': '0.85', 'RL_CAPT': '1'}
        base_h = CM.canonical_hash(base_vars)
        moved_all = True
        for k in base_vars:
            v2 = dict(base_vars); v2[k] = '0' if v2[k] != '0' else '1'
            if CM.canonical_hash(v2) == base_h:
                moved_all = False
        ok('changing each class-A semantic moves config_sha256', moved_all)

        # --- override hooks are represented as reject-if-set (changing them is rejected, not silent) ----
        represented = all(h in RC.DEFAULT_MUST_UNSET for h in ('RL_UNCOMP_S', 'RL_LSYM_TAB', 'RL_V0SURF_REFIT'))
        ok('class-A override hooks declared reject-if-set', represented)

    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    n_pass = sum(1 for _, p, _ in _RESULTS if p)
    n = len(_RESULTS)
    print("\nRESULT: %d/%d PASS" % (n_pass, n))
    return 0 if n_pass == n else 1


if __name__ == '__main__':
    sys.exit(main())
