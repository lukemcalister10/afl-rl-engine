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
# A DECLARED held candidate (#251 part A, owner ruling 2026-07-29). The tree can legitimately carry a new
# board/engine ahead of what is RELEASED — #217 committed the pricing-split board and engine deliberately
# without releasing them. Before this, the gate could not tell that from a genuine drift, so it HALTed on
# an intentional state and hid every later failure behind a permanent red.
#
# The hold is an EXPLICIT DECLARATION, never a pattern the gate infers. Each entry names the field, the
# identity that is RELEASED (== contract identities[field]) and the identity the TREE carries (==
# expected_boot[field]), plus a reason. Only that exact pair is excused: move either side and the
# declaration no longer describes the state, so the gate HALTs again. An UNDECLARED mismatch HALTs exactly
# as it always did.
#
# REMOVAL AT ADOPTION IS SELF-ENFORCING. When the contract is re-stamped to the adopted identity the two
# sides agree, and a declaration that excuses nothing is itself a rejection ("the hold is over") — so the
# adoption commit cannot leave the declaration behind. restamp_dynamic() drops the declarations for the
# fields it re-pins for the same reason.
HELD_KEY = 'held_candidates'
HELD_REQUIRED = ('field', 'release', 'candidate', 'reason')
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


def held_declarations(contract, rejects=None):
    """Parse + STRUCTURALLY validate the declared held candidates. Returns {field: declaration}.

    A malformed, anonymous, duplicated or unbindable declaration is a rejection, never a silent skip — a
    declaration is the one thing in this file that can stop a HALT, so it fails closed on its own shape.
    Passing `rejects` collects the reasons; omitting it just returns the well-formed subset."""
    out, seen = {}, set()
    rj = rejects if rejects is not None else []
    decls = contract.get(HELD_KEY)
    if decls is None:
        return out
    if not isinstance(decls, list):
        rj.append("%s must be a LIST of declarations, got %s" % (HELD_KEY, type(decls).__name__))
        return out
    ids = contract.get('identities') or {}
    for i, d in enumerate(decls):
        where = "%s[%d]" % (HELD_KEY, i)
        if not isinstance(d, dict):
            rj.append("%s is not an object — a hold must name field/release/candidate/reason" % where)
            continue
        missing = [k for k in HELD_REQUIRED if not str(d.get(k) or '').strip()]
        if missing:
            rj.append("%s is missing %s — a hold must be explicit and must state WHY" % (where, missing))
            continue
        f = str(d['field'])
        if f in seen:
            rj.append("%s declares field %r twice (ambiguous hold)" % (where, f))
            continue
        seen.add(f)
        if f not in ids:
            rj.append("%s declares field %r, which is not a bound release identity (%s) — a hold can only"
                      " excuse an identity the gate actually binds" % (where, f, sorted(ids)))
            continue
        if str(d['release']) == str(d['candidate']):
            rj.append("%s declares field %r held with release == candidate (%s) — that excuses nothing"
                      % (where, f, str(d['release'])[:12]))
            continue
        if str(ids[f]) != str(d['release']):
            rj.append("%s declares the released %s as %s but the contract pins %s — the declaration does not"
                      " describe this contract" % (where, f, str(d['release'])[:12], str(ids[f])[:12]))
            continue
        out[f] = d
    return out


def format_held(field, decl):
    return ("HELD CANDIDATE (declared): %s — released %s, tree carries %s — %s%s"
            % (field, str(decl['release'])[:12], str(decl['candidate'])[:12], decl['reason'],
               (" [%s]" % decl['declared_by']) if decl.get('declared_by') else ''))


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

    # (5) release identities must equal the expected_boot pins (stale identity pin), EXCEPT where the
    #     contract explicitly DECLARES that field as a held candidate: the tree carries a new identity that
    #     is deliberately not released yet. A declared hold reports as its own named status; an UNDECLARED
    #     mismatch HALTs exactly as before. See HELD_KEY above.
    idmap = contract.get('identities') or {}
    declared = held_declarations(contract, rejects)
    held = []
    for field, want in idmap.items():
        have = boot.get(field)
        decl = declared.get(field)
        if have is None:
            rejects.append("contract identity %s has no expected_boot pin to bind against" % field)
        elif str(have) == str(want):
            if decl is not None:
                rejects.append("%s declares %s held (released %s / candidate %s) but the release and the tree"
                               " now AGREE on %s — the hold is OVER. Remove the declaration in the same commit"
                               " that re-stamps the contract at adoption."
                               % (HELD_KEY, field, str(decl['release'])[:12], str(decl['candidate'])[:12],
                                  str(have)[:12]))
        elif decl is not None and str(decl['candidate']) == str(have):
            held.append((field, decl))
        elif decl is not None:
            rejects.append("%s declares %s held against candidate %s but the tree carries %s — an identity"
                           " moved since the hold was declared; re-declare it or re-stamp the contract"
                           % (HELD_KEY, field, str(decl['candidate'])[:12], str(have)[:12]))
        else:
            rejects.append("contract identity %s=%s != expected_boot %s (stale pin; an INTENTIONAL hold must"
                           " be declared in %s)" % (field, str(want)[:12], str(have)[:12], HELD_KEY))

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
    # The release verified. Any declared hold is REPORTED BY NAME so a held release state is visible in
    # every build log rather than being indistinguishable from a fully-adopted one.
    for field, decl in held:
        print("  " + format_held(field, decl))
    return contract.get('contract_sha256')


#: The BAKE-LANE identities — the ones `restamp_dynamic` deliberately does not touch because they
#: move only when the engine itself moves, not when a round advances. `config` is carried at the
#: contract's top level as `config_sha256`; the other three live under `identities`.
BAKE_LANE_IDENTITIES = ('engine_head', 'rl_model', 'fv')

#: Fields a bake-lane restamp must leave byte-identical. Asserted, not assumed: the whole point of a
#: restamp is that it moves exactly what it declares and nothing else.
BAKE_LANE_FROZEN = ('identities.band', 'identities.register', 'release_version', 'switch_posture',
                    'pvc_provenance', 'must_be_unset', 'held_checks', 'adopted',
                    'season_state_policy_id', '_retired_checks')


def restamp_bake_identities(root, measured, frozen_extra=(), dry_run=False):
    """Re-stamp the BAKE-LANE identities (config_sha256 + engine_head / rl_model / fv) to values
    MEASURED FROM THE TREE, re-seal, and prove the frozen fields did not move.

    ONE IMPLEMENTATION, TWO CALLERS (shrink S6, 2026-08-30). This logic lived only inside the
    landing transaction's contract step, which meant a change made OUTSIDE a landing — a dial flip
    committed by hand, say — had no way to reach it and had to restamp the contract manually. The
    ORDER 49 flip did exactly that and got it wrong: the contract identities and its self-hash were
    two of five stamps left behind, each found by running a gate rather than by noticing. The lander
    step and `tools/restamp` now both call THIS function, so there is one place where a contract's
    bake-lane identities are written and one definition of what may move while they are.

    `measured` is {'config', 'engine_head', 'rl_model', 'fv'} -> the value read from the tree by the
    caller's own measurers. This function does not measure: it writes what it is given and proves
    what it did, so the caller keeps ownership of what "the tree" means.

    The trailing newline of the committed file is preserved — `json.dump(indent=2)` emits none, and
    a landing that moved no value must still move no byte.

    Returns a report {'moved': [...], 'seal_before', 'seal_after', 'frozen_checked', 'writes'}.
    """
    missing = [k for k in ('config',) + BAKE_LANE_IDENTITIES if k not in measured]
    if missing:
        raise AssertionError('restamp_bake_identities needs a measured value for %s' % missing)
    cp = contract_path(root)
    with open(cp, 'rb') as f:
        raw = f.read()
    rc = json.loads(raw)
    body = json.dumps(rc, indent=2).encode()
    if raw != body and raw != body + b'\n':
        raise AssertionError('release_contract.json does not round-trip at indent=2; '
                             'refusing to reformat it')
    trailing_newline = (raw == body + b'\n')
    if rc['contract_sha256'] != contract_hash(rc):
        raise AssertionError('the contract seal is not self-consistent BEFORE this restamp')

    frozen = tuple(list(BAKE_LANE_FROZEN) + list(frozen_extra or ()))

    def snap(c):
        return {k: json.dumps(c['identities'].get(k.split('.', 1)[1], None), sort_keys=True)
                if k.startswith('identities.') else json.dumps(c.get(k), sort_keys=True)
                for k in frozen}

    fb = snap(rc)
    moved = []
    if rc['config_sha256'] != measured['config']:
        moved.append(('config_sha256', rc['config_sha256'], measured['config']))
    rc['config_sha256'] = measured['config']
    for f in BAKE_LANE_IDENTITIES:
        if rc['identities'].get(f) != measured[f]:
            moved.append(('identities.' + f, rc['identities'].get(f), measured[f]))
        rc['identities'][f] = measured[f]
    seal_before = rc.pop('contract_sha256')
    rc['contract_sha256'] = contract_hash(rc)
    drift = [k for k in fb if fb[k] != snap(rc)[k]]
    if drift:
        raise AssertionError('a field a bake-lane restamp must not touch moved: %s' % drift)

    report = {'moved': moved, 'seal_before': seal_before, 'seal_after': rc['contract_sha256'],
              'frozen_checked': len(frozen), 'writes': False,
              'trailing_newline_in_committed_file': trailing_newline}
    if dry_run:
        return report
    tmp = cp + '.restamp_tmp'
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(rc, indent=2) + ('\n' if trailing_newline else ''))
    os.replace(tmp, cp)
    with open(cp, encoding='utf-8') as fh:
        rc2 = json.load(fh)
    if rc2['contract_sha256'] != contract_hash(rc2):
        raise AssertionError('the seal must verify after the write')
    report['writes'] = True
    return report


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

    Any held_candidates declaration for a field this re-pins (store / board) is DROPPED: re-pinning the
    released identity to the freshly-staged one ends the hold on that field by definition, and a leftover
    declaration would then excuse nothing and reject (see HELD_KEY). Declarations on fields this does NOT
    re-pin (engine_head / rl_model / fv / ...) are preserved, because the hold on them still stands.

    Written atomically to the SAME path (os.replace); returns the new contract_sha256. Called by the Track B
    staged transaction against the WORKSPACE contract so the atomic commit moves store/board/expected_boot/
    season_state AND the release contract to the SAME round."""
    cp = contract_path(root)
    with open(cp) as f:
        c = json.load(f)
    aor = int(as_of_round)
    REPINNED = ('store', 'board')
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
    if isinstance(c.get(HELD_KEY), list):
        kept = [d for d in c[HELD_KEY]
                if not (isinstance(d, dict) and str(d.get('field')) in REPINNED)]
        if kept:
            c[HELD_KEY] = kept
        else:
            c.pop(HELD_KEY, None)
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
        print("RELEASE-CONTRACT CHECK")
        try:
            h = verify('gate', _root, halt=False)
        except AssertionError as e:
            print("RELEASE-CONTRACT CHECK: FAILED" + str(e)); sys.exit(1)
        _n = len(held_declarations(load(_root)))
        print("RELEASE-CONTRACT CHECK: PASS  (contract %s; identities + config + posture consistent%s)"
              % (str(h)[:12], "; %d DECLARED held candidate%s above — the release is NOT fully adopted"
                 % (_n, '' if _n == 1 else 's') if _n else ''))
        sys.exit(0)
    # default: print the contract hash + a short summary
    try:
        c = load(_root)
        print("release contract %s  version=%s  as_of_round=%s  switches=%s"
              % (contract_hash(c)[:12], c.get('release_version'), c.get('as_of_round'),
                 c.get('switch_posture')))
    except FileNotFoundError:
        print("release contract ABSENT (%s) — not yet stamped" % os.path.relpath(contract_path(_root), _root))
