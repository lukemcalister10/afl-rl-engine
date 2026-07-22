#!/usr/bin/env python3
"""RELEASE-STATE CONTRACT — the authoritative, jointly-stamped release identity (final integration
2026-07-21; closes the canonical switch-manifest defect + the AUDIT ADDENDUM).

WHY THIS EXISTS
  data/model_config.json pins the model-semantics vars and stamps config_sha256. This contract binds
  that config identity TOGETHER with the release identities (board / balanced-baseline / store / engine /
  rl_model / fv / register / as_of_round), the owner-approved switch posture, the PVC provenance, and the
  set of override hooks that MUST be absent. It is loaded deterministically in a CANONICAL build and
  fails closed: missing, stale, contradictory, ambient-only, or unknown state HALTS before any board is
  produced. Changing any bound class-A value necessarily moves either config_sha256 (in the manifest hash)
  or contract_sha256 (this file's own hash), so no live semantic can move without moving the stamped
  identity.

WHAT IT IS NOT
  It does NO engine math. It reads the contract, the manifest, expected_boot, and the live env only.
  Dev-shell exploration (no RL_CONFIG_MODE) is a NO-OP (verify returns None) so `RL_X=0 python3 ...`
  still works for exploration OUTSIDE a canonical/gate/bake build.

CANONICAL MODES
  RL_CONFIG_MODE in {'bake','gate','canonical'} => fenced build. 'canonical' is the release board build;
  a canonical build with RL_CONFIG_MODE UNSET is ambient-only and HALTS (require_canonical()).
"""
import os, sys, json, hashlib

CANON_MODES = ('bake', 'gate', 'canonical')
CONTRACT_PATH = ('data', 'release_contract.json')
# class-A override hooks whose canonical value is ABSENT (setting one would repoint/refit/re-table the
# board). Declared here AND in the contract's must_be_unset; both enforce reject-if-set in a canonical build.
DEFAULT_MUST_UNSET = ('RL_UNCOMP_S', 'RL_LSYM_TAB', 'RL_V0SURF_REFIT')


def repo_root():
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.dirname(os.path.abspath(__file__))):
        if cand and os.path.exists(os.path.join(cand, 'data', 'model_config.json')):
            return os.path.abspath(cand)
    return os.path.dirname(os.path.abspath(__file__))


def contract_path(root=None):
    return os.path.join(root or repo_root(), *CONTRACT_PATH)


def load(root=None):
    with open(contract_path(root)) as f:
        return json.load(f)


def contract_hash(contract):
    """Deterministic sha256 over the contract with its OWN hash field removed — key-order independent."""
    body = {k: v for k, v in contract.items() if k not in ('contract_sha256', '_doc')}
    payload = json.dumps(body, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(payload.encode()).hexdigest()


def _boot(root):
    with open(os.path.join(root, 'data', 'expected_boot.json')) as f:
        return json.load(f)


def _manifest_vars(root):
    with open(os.path.join(root, 'data', 'model_config.json')) as f:
        return json.load(f)['vars']


def _fail(mode, rejects, halt):
    hdr = "\n======== RELEASE CONTRACT (%s) REJECTED — BUILD HALTED ========\n" % mode
    msg = (hdr + "  - " + "\n  - ".join(rejects) +
           "\n  A canonical release build binds the stamped release-state identity (data/release_contract.json)."
           "\n  Fix the drift above, or re-stamp the contract at a bake in the same commit that moves the"
           "\n  manifest/board identity. Ambient shell overrides must not silently change the release state."
           "\n===============================================================")
    if halt:
        raise SystemExit(msg)
    raise AssertionError(msg)


def require_canonical(mode=None, halt=True):
    """HALT if this is not a fenced canonical/gate/bake build. Used at the canonical board entrypoint so a
    release board can NEVER be produced from ambient-only state (unset RL_CONFIG_MODE) or a diagnostic-only
    invocation. Returns the resolved mode."""
    mode = mode or os.environ.get('RL_CONFIG_MODE')
    if mode not in CANON_MODES:
        _fail('canonical-required', [
            "no fenced config mode: RL_CONFIG_MODE=%r (need one of %s). A canonical release board must not"
            " rely on ambient environment defaults, an unset RL_CONFIG_MODE, implicit feature-switch"
            " defaults, developer shell state, or diagnostic-only invocation behaviour." % (mode, list(CANON_MODES))
        ], halt)
    return mode


def verify(mode=None, root=None, halt=True):
    """Fail-closed release-state verification. NO-OP (returns None) outside a fenced mode (dev shell).
    In a fenced mode: the contract MUST exist and be internally + externally consistent."""
    mode = mode or os.environ.get('RL_CONFIG_MODE')
    if mode not in CANON_MODES:
        return None
    root = root or repo_root()
    rejects = []

    # (1) contract present
    cp = contract_path(root)
    if not os.path.exists(cp):
        _fail(mode, ["release contract ABSENT at %s — a canonical build requires the stamped release-state"
                     " identity" % os.path.relpath(cp, root)], halt)
    contract = load(root)

    # (2) contract self-hash (tamper / stale re-stamp)
    stored = contract.get('contract_sha256')
    recomputed = contract_hash(contract)
    if stored != recomputed:
        rejects.append("contract_sha256 %s != recomputed %s (contract tampered or not re-stamped)"
                       % (str(stored)[:12], recomputed[:12]))

    boot = _boot(root)
    mvars = _manifest_vars(root)

    # (3) config identity coherence: contract.config_sha256 == manifest hash == expected_boot 'config'
    man_hash = hashlib.sha256(
        '\n'.join('%s=%s' % (k, mvars[k]) for k in sorted(mvars)).encode()).hexdigest()
    if contract.get('config_sha256') != man_hash:
        rejects.append("contract config_sha256 %s != live manifest hash %s (stale config pin)"
                       % (str(contract.get('config_sha256'))[:12], man_hash[:12]))
    if boot.get('config') != man_hash:
        rejects.append("expected_boot 'config' %s != live manifest hash %s (stale boot config pin)"
                       % (str(boot.get('config'))[:12], man_hash[:12]))

    # (4) owner-approved switch posture: every declared switch must equal the manifest value (contradiction)
    for k, v in (contract.get('switch_posture') or {}).items():
        if k not in mvars:
            rejects.append("switch_posture %s not present in the manifest vars (unrepresented semantic)" % k)
        elif str(mvars[k]) != str(v):
            rejects.append("switch_posture %s=%r contradicts manifest %r" % (k, v, mvars[k]))

    # (5) release identities must equal the expected_boot pins (stale identity pin)
    idmap = contract.get('identities') or {}
    for field, want in idmap.items():
        have = boot.get(field)
        if have is None:
            rejects.append("contract identity %s has no expected_boot pin to bind against" % field)
        elif str(have) != str(want):
            rejects.append("contract identity %s=%s != expected_boot %s (stale pin)"
                           % (field, str(want)[:12], str(have)[:12]))

    # (6) PVC provenance coherence (single, known pathway; numeraire pinned)
    pv = contract.get('pvc_provenance') or {}
    known = {'RL_PVC2': 'pvc_curve_v2.json', 'RL_PVCADOPT': 'pvc_curve_L1b.json'}
    if pv.get('adopted_pathway') not in known:
        rejects.append("pvc_provenance adopted_pathway %r unknown/contradictory (expected one of %s)"
                       % (pv.get('adopted_pathway'), list(known)))
    elif pv.get('curve_file') != known[pv['adopted_pathway']]:
        rejects.append("pvc_provenance curve_file %r != %r for pathway %s"
                       % (pv.get('curve_file'), known[pv['adopted_pathway']], pv['adopted_pathway']))
    if str(pv.get('numeraire_pin1')) != '3000':
        rejects.append("pvc_provenance numeraire_pin1 %r != 3000 (numeraire law)" % pv.get('numeraire_pin1'))
    # the manifest's own PVC pathway switch must agree with the contract pathway
    if pv.get('adopted_pathway') == 'RL_PVC2' and mvars.get('RL_PVC2') != '1':
        rejects.append("contract pvc pathway RL_PVC2 but manifest RL_PVC2=%r" % mvars.get('RL_PVC2'))

    # (7) override hooks that MUST be absent: any set in the ambient env is a silent override -> HALT
    for k in (list(contract.get('must_be_unset', [])) or list(DEFAULT_MUST_UNSET)):
        if os.environ.get(k) is not None:
            rejects.append("override hook %s is SET (=%r) — canonical build requires it ABSENT (ambient"
                           " override of the authoritative state)" % (k, os.environ.get(k)))

    # (8) DYNAMIC season-state authority coherence (final integration 2026-07-21; supervisor 2nd/3rd review).
    #     as_of_round, calendar_progress and exposure_pace are DYNAMIC weekly release state stamped here +
    #     in expected_boot + season_state.json + the board. calendar_progress replaces the former frozen
    #     SEASON_PROG literal and RL_M3_FE; exposure_pace replaces RL_EXPO_F; both are DERIVED each round and
    #     FEED the valuation. FAIL-CLOSED: a stale/contradictory/absent season authority, or any error while
    #     loading/parsing/verifying it, is an explicit rejection that HALTS.
    sm = contract.get('season_metadata')
    if not sm:
        rejects.append("release contract has NO season_metadata — a fenced release must bind the dynamic "
                       "season-state authority (as_of_round / calendar_progress / exposure_pace)")
    else:
        if str(sm.get('as_of_round')) != str(boot.get('as_of_round')):
            rejects.append("season_metadata as_of_round %s != expected_boot as_of_round %s (stale season stamp)"
                           % (sm.get('as_of_round'), boot.get('as_of_round')))
        _bp = os.path.join(root, 'data', 'rl_build', 'rl_app_data.json')
        if sm.get('season_prog') is not None:
            if not os.path.exists(_bp):
                rejects.append("season_metadata declares season_prog but board %s is ABSENT — cannot verify "
                               "board season-progress coherence" % os.path.relpath(_bp, root))
            else:
                try:
                    _bsp = json.load(open(_bp)).get('SEASON_PROG')
                    if _bsp is None:
                        rejects.append("board %s has no SEASON_PROG field to bind season_metadata against"
                                       % os.path.relpath(_bp, root))
                    elif float(_bsp) != float(sm['season_prog']):
                        rejects.append("season_metadata season_prog %s != board SEASON_PROG %s (contradiction)"
                                       % (sm.get('season_prog'), _bsp))
                except (KeyboardInterrupt, SystemExit):
                    raise
                except Exception as _e:
                    rejects.append("could not verify board SEASON_PROG at %s (fail-closed): %s"
                                   % (os.path.relpath(_bp, root), _e))
        # (8b) VERIFY THE DERIVATION, not merely equality of duplicated fields (supervisor 2nd review req 7).
        #      FAIL-CLOSED (supervisor 3rd review req 2): any error loading/parsing/verifying the derivation
        #      policy (season_state.py), the authoritative season_state.json, or the source store — including
        #      their ABSENCE — is an explicit rejection, never a silent skip. calendar_progress MUST equal
        #      round_half_up(100*as_of_round/season_total_rounds)/100; season_state.json must be internally
        #      consistent + freshly derived (policy, round, calendar) off the LIVE store; season_year agrees.
        try:
            import importlib.util as _il, hashlib as _h
            _ssp = os.path.join(root, 'season_state.py')
            if not os.path.exists(_ssp):
                raise FileNotFoundError("authoritative derivation policy season_state.py ABSENT at %s" % _ssp)
            _sp = _il.spec_from_file_location('season_state_v', _ssp)
            _S = _il.module_from_spec(_sp); _sp.loader.exec_module(_S)
            _tot = int(sm.get('season_total_rounds') or _S.SEASON_TOTAL_ROUNDS_DEFAULT)
            _aor = int(sm.get('as_of_round'))
            _cp_der = _S.calendar_progress(_aor, _tot)
            if sm.get('calendar_progress') is not None and float(sm['calendar_progress']) != _cp_der:
                rejects.append("season_metadata calendar_progress %s != derived round_half_up(100*%d/%d)=%.2f"
                               % (sm.get('calendar_progress'), _aor, _tot, _cp_der))
            if sm.get('derivation_policy_id') and sm['derivation_policy_id'] != _S.policy_id():
                rejects.append("season_metadata derivation_policy_id stale (%s != live policy %s)"
                               % (str(sm.get('derivation_policy_id'))[:12], _S.policy_id()[:12]))
            _ssf = os.path.join(root, 'data', 'season_state.json')
            if not os.path.exists(_ssf):
                rejects.append("authoritative season_state.json ABSENT at %s — cannot verify the season-state "
                               "derivation (a fenced release must carry the dynamic season state)"
                               % os.path.relpath(_ssf, root))
            else:
                _ss = json.load(open(_ssf))
                if str(_ss.get('as_of_round')) != str(_aor):
                    rejects.append("season_state.json as_of_round %s != contract %s (artifacts on different rounds)"
                                   % (_ss.get('as_of_round'), _aor))
                if float(_ss.get('calendar_progress', -1)) != _cp_der:
                    rejects.append("season_state.json calendar_progress %s != derived %.2f (stale calendar)"
                                   % (_ss.get('calendar_progress'), _cp_der))
                if _ss.get('derivation_policy_id') != _S.policy_id():
                    rejects.append("season_state.json derivation_policy_id stale vs live policy")
                if sm.get('season_year') is not None and _ss.get('season_year') != sm.get('season_year'):
                    rejects.append("season_year inconsistent (contract %s vs season_state %s)"
                                   % (sm.get('season_year'), _ss.get('season_year')))
                _store = os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')
                if not os.path.exists(_store):
                    rejects.append("source store %s ABSENT — cannot verify exposure_pace was derived from the "
                                   "live store" % os.path.relpath(_store, root))
                else:
                    _live = _h.md5(open(_store, 'rb').read()).hexdigest()
                    if _ss.get('source_store_md5') != _live:
                        rejects.append("season_state.json source_store_md5 %s != live store %s — exposure_pace "
                                       "was derived from a STALE store" % (str(_ss.get('source_store_md5'))[:8], _live[:8]))
                if sm.get('exposure_pace') is not None and float(_ss.get('exposure_pace', -1)) != float(sm['exposure_pace']):
                    rejects.append("season_state.json exposure_pace %s != contract %s (stale exposure)"
                                   % (_ss.get('exposure_pace'), sm.get('exposure_pace')))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as _e:
            rejects.append("season-state DERIVATION verification could not complete (fail-closed): %s" % _e)

    if rejects:
        _fail(mode, rejects, halt)
    return contract.get('contract_sha256')


def restamp_dynamic(root, as_of_round, store_md5, board_md5, season_state):
    """Re-stamp the DYNAMIC fields of <root>/data/release_contract.json to a newly-accepted round and
    recompute the deterministic self-hash (supervisor 3rd review req 3 — one coherent weekly authority).

    Advances the top-level as_of_round, re-pins identities.store + identities.board to the freshly-staged
    md5s, and refreshes season_metadata (as_of_round / calendar_progress / exposure_pace / season_prog /
    derivation_policy_id / season_year / season_total_rounds) from the authoritative season_state dict.
    EVERYTHING ELSE is preserved byte-for-byte: release_version, config_sha256, switch_posture,
    pvc_provenance, must_be_unset, present_lens_baseline, f5 reconciliation, the descriptive season notes,
    and the immutable engine/rl_model/fv/register/band identities. The immutable present-lens baseline
    (data/release_lineage.json) is NEVER touched here.

    Written atomically to the SAME path (os.replace); returns the new contract_sha256. Called by the Track B
    staged transaction against the WORKSPACE contract so the atomic commit moves store/board/expected_boot/
    season_state AND the release contract to the SAME round."""
    cp = contract_path(root)
    with open(cp) as f:
        c = json.load(f)
    aor = int(as_of_round)
    cal = float(season_state['calendar_progress'])
    c['as_of_round'] = aor
    ids = c.setdefault('identities', {})
    ids['store'] = store_md5
    ids['board'] = board_md5
    sm = c.setdefault('season_metadata', {})
    sm['as_of_round'] = aor
    sm['calendar_progress'] = cal
    sm['exposure_pace'] = float(season_state['exposure_pace'])
    sm['season_prog'] = cal                          # the board's SEASON_PROG == calendar_progress (same dial)
    sm['derivation_policy_id'] = season_state['derivation_policy_id']
    sm['season_year'] = int(season_state['season_year'])
    sm['season_total_rounds'] = int(season_state['season_total_rounds'])
    c.pop('contract_sha256', None)
    c['contract_sha256'] = contract_hash(c)
    tmp = cp + '.tmp_restamp'
    with open(tmp, 'w') as f:
        json.dump(c, f, indent=2)
    os.replace(tmp, cp)
    return c['contract_sha256']


if __name__ == '__main__':
    _root = repo_root()
    if len(sys.argv) > 1 and sys.argv[1] == 'hash':
        print(contract_hash(load(_root))); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        # assert the contract is internally + externally consistent (as a canonical build would), non-zero on fail.
        os.environ.setdefault('RL_CONFIG_MODE', 'gate')
        try:
            h = verify('gate', _root, halt=False)
        except AssertionError as e:
            print("RELEASE-CONTRACT CHECK: FAILED" + str(e)); sys.exit(1)
        print("RELEASE-CONTRACT CHECK: PASS  (contract %s; identities + config + posture consistent)" % str(h)[:12])
        sys.exit(0)
    # default: print the contract hash + a short summary
    try:
        c = load(_root)
        print("release contract %s  version=%s  as_of_round=%s  switches=%s"
              % (contract_hash(c)[:12], c.get('release_version'), c.get('as_of_round'),
                 c.get('switch_posture')))
    except FileNotFoundError:
        print("release contract ABSENT (%s) — not yet stamped" % os.path.relpath(contract_path(_root), _root))
