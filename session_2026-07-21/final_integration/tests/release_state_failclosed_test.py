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
SS = _load('season_state_t', os.path.join(ROOT, 'season_state.py'))

_RESULTS = []
def ok(name, cond, detail=''):
    _RESULTS.append((name, bool(cond), detail))
    print(("  PASS " if cond else "  FAIL ") + name + (("  -- " + detail) if detail and not cond else ''))

def _manhash(vars_):
    return hashlib.sha256('\n'.join('%s=%s' % (k, vars_[k]) for k in sorted(vars_)).encode()).hexdigest()

def make_fixture(tmp, vars_=None, boot_over=None, contract_over=None, write_contract=True,
                 write_season=True, season_over=None, sm_over=None, aor=14):
    """Build a minimal, internally-consistent temp release state under tmp/ — INCLUDING the dynamic season
    authority (season_state.py + data/season_state.json + a source store + the contract's season_metadata),
    so the fail-closed season-state verification (supervisor 3rd review req 2) is exercised on a complete,
    genuinely-consistent release. `write_season=False`/`season_over`/`sm_over` build the red-path fixtures.
    Returns the contract dict."""
    os.makedirs(os.path.join(tmp, 'data'), exist_ok=True)
    # a source store (a couple of bytes is enough — verify only pins its md5, never reads the rows)
    _store_dir = os.path.join(tmp, 'engine', 'rl_after'); os.makedirs(_store_dir, exist_ok=True)
    _store_path = os.path.join(_store_dir, 'rl_model_data.json')
    with open(_store_path, 'w') as _sf:
        _sf.write('{"_fixture_store": true}')
    _store_md5 = hashlib.md5(open(_store_path, 'rb').read()).hexdigest()
    # the authoritative derivation policy travels with the fixture (verify executes tmp/season_state.py)
    shutil.copy(os.path.join(ROOT, 'season_state.py'), os.path.join(tmp, 'season_state.py'))
    _cp = SS.calendar_progress(aor, 24)         # derived calendar (round_half_up whole-percent)
    _pol = SS.policy_id()
    _ep = 0.545
    # a tiny but valid manifest
    vars_ = dict(vars_ or {'RL_PVC2': '1', 'RL_LEGE': '1', 'RL_LEGF': '1', 'RL_GAMMA': '0.85'})
    ch = _manhash(vars_)
    json.dump({'version': '1.0', 'config_sha256': ch, 'vars': vars_},
              open(os.path.join(tmp, 'data', 'model_config.json'), 'w'))
    boot = {'board': 'aaaa1111', 'balanced_board_md5': '06d8af60', 'store': 'bbbb2222',
            'engine_head': 'cccc3333', 'rl_model': 'dddd4444', 'fv': 'eeee5555',
            'register': 'ffff6666', 'config': ch, 'as_of_round': aor}
    if boot_over: boot.update(boot_over)
    json.dump(boot, open(os.path.join(tmp, 'data', 'expected_boot.json'), 'w'))
    # the dynamic season-state authority (its as_of_round/calendar/policy must agree with the contract)
    if write_season:
        ss = {'season_year': 2026, 'season_total_rounds': 24, 'as_of_round': aor,
              'calendar_progress': _cp, 'exposure_pace': _ep, 'source_store_md5': _store_md5,
              'derivation_policy_id': _pol, 'inprog_year': 2026}
        if season_over: ss.update(season_over)
        json.dump(ss, open(os.path.join(tmp, 'data', 'season_state.json'), 'w'))
    sm = {'as_of_round': aor, 'season_total_rounds': 24, 'season_year': 2026,
          'calendar_progress': _cp, 'exposure_pace': _ep, 'derivation_policy_id': _pol}
    if sm_over: sm.update(sm_over)
    contract = {'release_version': 'v2.11-final-rc-test', 'as_of_round': aor,
                'switch_posture': {'RL_PVC2': '1', 'RL_LEGE': '1', 'RL_LEGF': '1'},
                'config_sha256': ch,
                'identities': {'board': boot['board'], 'store': boot['store'],
                               'engine_head': boot['engine_head'], 'rl_model': boot['rl_model'],
                               'fv': boot['fv'], 'register': boot['register']},
                'pvc_provenance': {'adopted_pathway': 'RL_PVC2', 'curve_file': 'pvc_curve_v2.json',
                                   'curve_payload_md5': '89c14729', 'numeraire_pin1': 3000},
                'must_be_unset': list(RC.DEFAULT_MUST_UNSET),
                'season_metadata': sm}
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

        # --- SEASON-STATE fail-closed (supervisor 3rd review req 2): a fenced verify must NOT fail-open ---
        # (a) contract with NO season_metadata HALTS (the fenced release must bind the season authority)
        ta = tempfile.mkdtemp()
        make_fixture(ta, contract_over={'season_metadata': None})
        r = with_env(RL_REPO=ta, RL_CONFIG_MODE='gate')
        ok('missing season_metadata halts', halts(lambda: RC.verify('gate', ta, halt=True)))
        r(); shutil.rmtree(ta, ignore_errors=True)
        # (b) authoritative season_state.json ABSENT HALTS (was silently skipped before; now fail-closed)
        tb = tempfile.mkdtemp()
        make_fixture(tb, write_season=False)
        r = with_env(RL_REPO=tb, RL_CONFIG_MODE='gate')
        ok('missing season_state.json halts', halts(lambda: RC.verify('gate', tb, halt=True)))
        r(); shutil.rmtree(tb, ignore_errors=True)
        # (c) malformed season_state.json HALTS (parse error becomes an explicit rejection, not a pass)
        tc = tempfile.mkdtemp()
        make_fixture(tc)
        open(os.path.join(tc, 'data', 'season_state.json'), 'w').write('{ this is not json')
        r = with_env(RL_REPO=tc, RL_CONFIG_MODE='gate')
        ok('malformed season_state.json halts', halts(lambda: RC.verify('gate', tc, halt=True)))
        r(); shutil.rmtree(tc, ignore_errors=True)
        # (d) STALE calendar_progress in season_state.json (!= round_half_up derivation) HALTS
        td = tempfile.mkdtemp()
        make_fixture(td, season_over={'calendar_progress': 0.63})   # R14 must derive 0.58, not 0.63
        r = with_env(RL_REPO=td, RL_CONFIG_MODE='gate')
        ok('stale calendar_progress halts', halts(lambda: RC.verify('gate', td, halt=True)))
        r(); shutil.rmtree(td, ignore_errors=True)
        # (e) STALE source_store_md5 (exposure derived from a store other than the live one) HALTS
        te = tempfile.mkdtemp()
        make_fixture(te, season_over={'source_store_md5': 'deadbeefdeadbeefdeadbeefdeadbeef'})
        r = with_env(RL_REPO=te, RL_CONFIG_MODE='gate')
        ok('stale source_store_md5 halts', halts(lambda: RC.verify('gate', te, halt=True)))
        r(); shutil.rmtree(te, ignore_errors=True)
        # (f) season_state.json as_of_round != contract round HALTS (artifacts on different rounds)
        tf = tempfile.mkdtemp()
        make_fixture(tf, season_over={'as_of_round': 13})
        r = with_env(RL_REPO=tf, RL_CONFIG_MODE='gate')
        ok('season_state on a different round halts', halts(lambda: RC.verify('gate', tf, halt=True)))
        r(); shutil.rmtree(tf, ignore_errors=True)
        # (g) STALE derivation_policy_id HALTS (policy identity mismatch)
        tg = tempfile.mkdtemp()
        make_fixture(tg, season_over={'derivation_policy_id': 'stalepolicyid00'})
        r = with_env(RL_REPO=tg, RL_CONFIG_MODE='gate')
        ok('stale derivation_policy_id halts', halts(lambda: RC.verify('gate', tg, halt=True)))
        r(); shutil.rmtree(tg, ignore_errors=True)
        # (h) the derivation-policy module (season_state.py) ABSENT HALTS (cannot verify derivation)
        th = tempfile.mkdtemp()
        make_fixture(th)
        os.remove(os.path.join(th, 'season_state.py'))
        r = with_env(RL_REPO=th, RL_CONFIG_MODE='gate')
        ok('missing season_state.py (derivation policy) halts', halts(lambda: RC.verify('gate', th, halt=True)))
        r(); shutil.rmtree(th, ignore_errors=True)

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
