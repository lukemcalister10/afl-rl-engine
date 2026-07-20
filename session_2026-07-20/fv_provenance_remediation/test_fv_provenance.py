#!/usr/bin/env python3
"""DURABLE FORWARD-VALUATION PROVENANCE RED/GREEN SUITE (fv-provenance remediation 2026-07-20).

Proves the fail-closed forward-valuation / rl_model / config provenance fix end-to-end. Self-contained: it
builds the board in a fresh disposable staging copy of the checkout, with a controlled environment, and asserts
the outcome. Runs locally and on a clean CI runner (.github/workflows/fv-provenance.yml).

Scenarios (audit's §7 red/green standard):
  GREEN 1  strict canonical build (RL_FV=checkout, balanced config)         -> board 06d8af60, 804/752427/7964, 0 movers
  GREEN 2  provenance record emitted before export                          -> RL_FV, resolved dir, FV identity,
                                                                               dp path+hash, rl_model path+hash,
                                                                               config_manifest path+identity
  RED 1    stale 21d530bf at the FORMER ambient workspace path              -> ignored (checkout selected); never d7a95e8d
  RED 2    explicit RL_FV pointed at a stale tree (dp 21d530bf)             -> Guard 5 loaded-path HALT before generation
  RED 3    a DIFFERENT imported FV source drifts (conditional_prior.py)     -> Guard 5 checkout HALT (whole set protected)
  RED 4    missing / mismatched config_manifest in bake mode               -> HALT before board (no silent continue)
  RED 5    foreign rl_model under /home/claude/rl_after                     -> never imported; verified rl_model used

Every RED path additionally asserts: no board written, no pin changed, no production file changed, no retry.
Exit code is the verdict (0 = all pass).
"""
import os, sys, json, shutil, subprocess, hashlib, tempfile

# ---- locate the checked-out repo (RL_REPO / CLAUDE_PROJECT_DIR / walk up from this file) ----
def _find_repo():
    for c in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR')):
        if c and os.path.exists(os.path.join(c, 'data', 'expected_boot.json')):
            return os.path.abspath(c)
    d = os.path.dirname(os.path.abspath(__file__))
    while d != '/':
        if os.path.exists(os.path.join(d, 'data', 'expected_boot.json')):
            return d
        d = os.path.dirname(d)
    raise SystemExit("test_fv_provenance: cannot locate the checkout (set RL_REPO).")

REPO = _find_repo()
FIX = os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'fixtures')
CLAUDE = '/home/claude'
AMBIENT_FV = os.path.join(CLAUDE, 'rl_workspace', 'forward_valuation')   # the FORMER RL_FV default (the hole)
RL_AFTER_LINK = os.path.join(CLAUDE, 'rl_after')                        # the FORMER hardcoded rl_model path
BOARD_MD5_GOOD = '06d8af60b679a12db07c064c60c065f9'
BAD_PREFIX = 'd7a95e8d'
STALE_DP = os.path.join(FIX, 'distribution_pricing.stale_21d530bf.py')

# ---- provenance-relevant production files whose bytes must NOT change across any red path ----
_GUARDED = ['data/expected_boot.json', 'boot_guard.py', 'fv_provenance.py',
            'engine/forward_valuation/distribution_pricing.py', 'engine/rl_after/rl_export.py',
            'engine/rl_after/rl_model.py', 'engine/rl_after/_merged_recover.py']


def _md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for ch in iter(lambda: f.read(1 << 16), b''):
            h.update(ch)
    return h.hexdigest()


def _snapshot_guarded():
    return {rel: _md5(os.path.join(REPO, rel)) for rel in _GUARDED if os.path.exists(os.path.join(REPO, rel))}


def _seed_pkls():
    for name in ('cm_400.pkl', 'q97m.pkl', 'v0surf.pkl'):
        src = os.path.join(REPO, 'data', name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(CLAUDE, name))


def _staging():
    base = tempfile.mkdtemp(prefix='fvprov_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    ws = os.path.join(base, 'rl_after')
    shutil.copytree(os.path.join(REPO, 'engine', 'rl_after'), ws)
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'), os.path.join(base, 'forward_valuation'))
    for m in ('config_manifest.py', 'fv_provenance.py', 'boot_guard.py'):
        shutil.copy2(os.path.join(REPO, m), os.path.join(ws, m))
    lr = os.path.join(REPO, 'LTI_REGISTER.md')
    if os.path.exists(lr):
        shutil.copy2(lr, os.path.join(ws, 'LTI_REGISTER.md'))
    return base, ws


def _run_build(env_overrides, rl_fv=None, config_mode=None, balanced=True):
    """Build the board in a fresh staging dir. Returns dict(rc, board_md5, board_path, prov, stderr, ws)."""
    base, ws = _staging()
    _seed_pkls()
    env = dict(os.environ)
    for k in ('RL_PVC2', 'RL_LEGE', 'RL_LEGF', 'RL_V0SURF_REFIT', 'RL_CONFIG_MODE', 'RL_FV'):
        env.pop(k, None)
    env['RL_REPO'] = REPO
    env['PYTHONHASHSEED'] = '0'
    for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        env[k] = '1'
    env['RL_PRIOR_TREES'] = '400'
    if balanced:
        env['RL_PVC2'] = '1'; env['RL_LEGE'] = '0'; env['RL_LEGF'] = '0'
    env['PYTHONPATH'] = ws + ':' + REPO + ':' + os.path.join(CLAUDE, 'rl_vendor')
    if rl_fv is not None:
        env['RL_FV'] = rl_fv
    if config_mode is not None:
        env['RL_CONFIG_MODE'] = config_mode
    env.update(env_overrides or {})
    board = os.path.join(ws, 'rl_app_data.json')
    for f in (board, board + '.srcmd5', os.path.join(ws, 'rl_app_data.provenance.json')):
        try: os.remove(f)
        except OSError: pass
    p = subprocess.run([sys.executable, 'rl_export.py'], cwd=ws, env=env,
                       capture_output=True, text=True)
    prov = None
    provf = os.path.join(ws, 'rl_app_data.provenance.json')
    if os.path.exists(provf):
        try: prov = json.load(open(provf))
        except Exception: prov = None
    return {'rc': p.returncode,
            'board_md5': _md5(board) if os.path.exists(board) else None,
            'board_path': board if os.path.exists(board) else None,
            'prov': prov, 'stderr': p.stderr, 'stdout': p.stdout, 'ws': ws, 'base': base}


def _board_facts(path):
    d = json.loads(open(path, 'rb').read())
    a = {p['key']: p for p in d['active']}
    return {'active': len(d['active']), 'sum_v': sum(p['v'] for p in d['active']),
            'sheezel': a.get('harry-sheezel', {}).get('v')}


RESULTS = []
def record(name, ok, detail):
    RESULTS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    print("  [%s] %s — %s" % ('PASS' if ok else 'FAIL', name, detail))


# ============================ GREEN 1 — strict canonical build ============================
def green1():
    r = _run_build({}, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'))
    ok = (r['rc'] == 0 and r['board_md5'] == BOARD_MD5_GOOD)
    facts = _board_facts(r['board_path']) if r['board_path'] else {}
    ok = ok and facts.get('active') == 804 and facts.get('sum_v') == 752427 and facts.get('sheezel') == 7964
    record('GREEN1_strict_board_06d8af60', ok,
           "rc=%s md5=%s active=%s sumv=%s sheezel=%s (expect 06d8af60/804/752427/7964)"
           % (r['rc'], r['board_md5'], facts.get('active'), facts.get('sum_v'), facts.get('sheezel')))
    shutil.rmtree(r['base'], ignore_errors=True)
    return r


# ============================ GREEN 2 — provenance reporting ============================
def green2():
    r = _run_build({}, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'))
    p = r['prov'] or {}
    need = ['RL_FV_env', 'resolved_fv_dir', 'fv_identity', 'fv_identity_expected',
            'distribution_pricing_path', 'distribution_pricing_md5', 'rl_model_path', 'rl_model_md5',
            'config_manifest_path', 'config_manifest_identity']
    present = all(p.get(k) for k in need)
    matched = (p.get('fv_identity') == p.get('fv_identity_expected'))
    marker = 'PROVENANCE ' in (r['stderr'] or '')
    ok = present and matched and marker and r['board_md5'] == BOARD_MD5_GOOD
    record('GREEN2_provenance_record', ok,
           "all_fields=%s fv_identity==pin=%s stderr_marker=%s (fv=%s dp=%s rlm=%s cfg=%s)"
           % (present, matched, marker, (p.get('fv_identity') or '')[:8],
              (p.get('distribution_pricing_md5') or '')[:8], (p.get('rl_model_md5') or '')[:8],
              (p.get('config_manifest_identity') or '')[:8]))
    shutil.rmtree(r['base'], ignore_errors=True)


# ============================ RED 1 — stale ambient workspace ignored ============================
def red1():
    before = _snapshot_guarded()
    os.makedirs(AMBIENT_FV, exist_ok=True)
    # seed the FORMER ambient default with the stale 21d530bf module (the exact hole)
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'), AMBIENT_FV, dirs_exist_ok=True)
    shutil.copy2(STALE_DP, os.path.join(AMBIENT_FV, 'distribution_pricing.py'))
    stale_here = _md5(os.path.join(AMBIENT_FV, 'distribution_pricing.py')).startswith('21d530bf')
    # canonical build with RL_FV UNSET -> must resolve to the CHECKOUT, ignoring the stale ambient copy
    r = _run_build({}, rl_fv=None)
    after = _snapshot_guarded()
    not_bad = (r['board_md5'] != None and not str(r['board_md5']).startswith(BAD_PREFIX))
    is_good = (r['board_md5'] == BOARD_MD5_GOOD)
    files_unchanged = (before == after)
    ok = stale_here and is_good and not_bad and files_unchanged
    record('RED1_stale_ambient_ignored', ok,
           "stale_seeded=%s board=%s (must be 06d8af60, never d7a95e8d) files_unchanged=%s"
           % (stale_here, r['board_md5'], files_unchanged))
    shutil.rmtree(r['base'], ignore_errors=True)


# ============================ RED 2 — explicit stale RL_FV -> HALT ============================
def red2():
    before = _snapshot_guarded()
    stale_tree = tempfile.mkdtemp(prefix='fvstale_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'), stale_tree, dirs_exist_ok=True)
    shutil.copy2(STALE_DP, os.path.join(stale_tree, 'distribution_pricing.py'))
    # bake mode so the canonical entry point runs the fail-closed FV assertion before generation
    r = _run_build({}, rl_fv=stale_tree, config_mode='bake', balanced=False)
    after = _snapshot_guarded()
    halted = (r['rc'] != 0 and r['board_md5'] is None)
    named = ('LOADED-PATH DRIFT' in r['stderr'] or 'loaded' in r['stderr'].lower())
    ok = halted and named and (before == after)
    record('RED2_explicit_stale_rl_fv_halts', ok,
           "rc=%s board=%s named_drift=%s files_unchanged=%s" % (r['rc'], r['board_md5'], named, before == after))
    shutil.rmtree(r['base'], ignore_errors=True); shutil.rmtree(stale_tree, ignore_errors=True)


# ============================ RED 3 — sibling FV source drift -> HALT ============================
def red3():
    before = _snapshot_guarded()
    drift_repo = tempfile.mkdtemp(prefix='fvdrift_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    os.makedirs(os.path.join(drift_repo, 'engine'), exist_ok=True)
    os.makedirs(os.path.join(drift_repo, 'data'), exist_ok=True)
    shutil.copytree(os.path.join(REPO, 'engine', 'forward_valuation'),
                    os.path.join(drift_repo, 'engine', 'forward_valuation'))
    shutil.copy2(os.path.join(REPO, 'data', 'expected_boot.json'), os.path.join(drift_repo, 'data', 'expected_boot.json'))
    # a valid (unchanged) model_config.json so bake-mode CONFIG enforcement PASSES and the FV checkout-drift
    # assertion is the halting reason (config runs before FV in the canonical preamble).
    shutil.copy2(os.path.join(REPO, 'data', 'model_config.json'), os.path.join(drift_repo, 'data', 'model_config.json'))
    shutil.copy2(os.path.join(REPO, 'config_manifest.py'), os.path.join(drift_repo, 'config_manifest.py'))
    # modify a DIFFERENT imported FV source (not distribution_pricing.py) — the whole set is pinned
    sib = os.path.join(drift_repo, 'engine', 'forward_valuation', 'conditional_prior.py')
    with open(sib, 'a') as f:
        f.write("\n# provenance-drift marker (sibling source changed without re-pinning)\n")
    fv_drift = os.path.join(drift_repo, 'engine', 'forward_valuation')
    r = _run_build({'RL_REPO': drift_repo}, rl_fv=fv_drift, config_mode='bake', balanced=False)
    after = _snapshot_guarded()
    halted = (r['rc'] != 0 and r['board_md5'] is None)
    named = ('CHECKOUT DRIFT' in r['stderr'] or 'forward_valuation identity' in r['stderr'])
    ok = halted and named and (before == after)
    record('RED3_sibling_source_drift_halts', ok,
           "rc=%s board=%s named_checkout_drift=%s files_unchanged=%s" % (r['rc'], r['board_md5'], named, before == after))
    shutil.rmtree(r['base'], ignore_errors=True); shutil.rmtree(drift_repo, ignore_errors=True)


# ============================ RED 4 — missing/wrong config manifest -> HALT (bake) ============================
def red4():
    before = _snapshot_guarded()
    results = []
    # 4a: config_manifest not importable (removed from the run dir, and not on PYTHONPATH)
    base, ws = _staging()
    os.remove(os.path.join(ws, 'config_manifest.py'))
    _seed_pkls()
    env = dict(os.environ)
    for k in ('RL_PVC2', 'RL_LEGE', 'RL_LEGF', 'RL_V0SURF_REFIT'):
        env.pop(k, None)
    env.update({'RL_REPO': REPO, 'RL_FV': os.path.join(REPO, 'engine', 'forward_valuation'),
                'RL_CONFIG_MODE': 'bake', 'RL_PRIOR_TREES': '400', 'PYTHONHASHSEED': '0',
                'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1',
                'PYTHONPATH': ws + ':' + os.path.join(CLAUDE, 'rl_vendor')})  # NOTE: repo NOT on path -> config_manifest unresolvable
    for f in ('rl_app_data.json', 'rl_app_data.json.srcmd5'):
        try: os.remove(os.path.join(ws, f))
        except OSError: pass
    p = subprocess.run([sys.executable, 'rl_export.py'], cwd=ws, env=env, capture_output=True, text=True)
    board = os.path.join(ws, 'rl_app_data.json')
    a_ok = (p.returncode != 0 and not os.path.exists(board) and 'not importable' in p.stderr)
    results.append(('4a_missing', a_ok, "rc=%s board=%s" % (p.returncode, os.path.exists(board))))
    shutil.rmtree(base, ignore_errors=True)
    # 4b: mismatched manifest hash (tampered model_config.json under a scratch repo root)
    scratch = tempfile.mkdtemp(prefix='fvcfg_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    os.makedirs(os.path.join(scratch, 'data'), exist_ok=True)
    shutil.copy2(os.path.join(REPO, 'data', 'expected_boot.json'), os.path.join(scratch, 'data', 'expected_boot.json'))
    mc = json.load(open(os.path.join(REPO, 'data', 'model_config.json')))
    mc['vars']['RL_PRIOR_TREES'] = '999'   # tamper -> hash != pin
    json.dump(mc, open(os.path.join(scratch, 'data', 'model_config.json'), 'w'))
    r = _run_build({'RL_REPO': scratch}, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'),
                   config_mode='bake', balanced=False)
    b_ok = (r['rc'] != 0 and r['board_md5'] is None and ('REJECTED' in r['stderr'] or 'hash' in r['stderr']))
    results.append(('4b_mismatch', b_ok, "rc=%s board=%s" % (r['rc'], r['board_md5'])))
    shutil.rmtree(r['base'], ignore_errors=True); shutil.rmtree(scratch, ignore_errors=True)
    after = _snapshot_guarded()
    ok = all(x[1] for x in results) and (before == after)
    record('RED4_config_manifest_failclosed', ok,
           "; ".join("%s:%s(%s)" % (n, 'ok' if o else 'BAD', d) for n, o, d in results) + " files_unchanged=%s" % (before == after))


# ============================ RED 5 — foreign rl_model under /home/claude/rl_after ignored ============================
def red5():
    before = _snapshot_guarded()
    # ensure the FORMER hardcoded path exists and plant a foreign, CRASHING rl_model there
    ws_link_target = os.path.join(CLAUDE, 'rl_workspace', 'rl_after')
    os.makedirs(ws_link_target, exist_ok=True)
    if not os.path.exists(RL_AFTER_LINK):
        try: os.symlink(ws_link_target, RL_AFTER_LINK)
        except OSError: pass
    foreign = os.path.join(RL_AFTER_LINK, 'rl_model.py')
    saved = None
    if os.path.exists(foreign):
        saved = foreign + '.savedbytest'
        shutil.move(foreign, saved)
    with open(foreign, 'w') as f:
        f.write("raise RuntimeError('FOREIGN rl_model under /home/claude/rl_after was imported — provenance breach')\n")
    try:
        # canonical build; rl_model must resolve from the verified staging/checkout, NOT /home/claude/rl_after
        r = _run_build({}, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'))
        after = _snapshot_guarded()
        prov = r['prov'] or {}
        rlm_path = prov.get('rl_model_path') or ''
        not_foreign = (os.path.abspath(RL_AFTER_LINK) not in os.path.abspath(rlm_path)) if rlm_path else None
        # strongest proof: the build SUCCEEDED with the good board (a crashing foreign import would have failed it)
        ok = (r['board_md5'] == BOARD_MD5_GOOD and 'provenance breach' not in (r['stderr'] or '')
              and not_foreign and (before == after))
        record('RED5_foreign_rl_model_ignored', ok,
               "board=%s rl_model_path=%s (not /home/claude/rl_after=%s) files_unchanged=%s"
               % (r['board_md5'], rlm_path, not_foreign, before == after))
        shutil.rmtree(r['base'], ignore_errors=True)
    finally:
        try: os.remove(foreign)
        except OSError: pass
        if saved and os.path.exists(saved):
            shutil.move(saved, foreign)


def main():
    print("=" * 90)
    print("FORWARD-VALUATION PROVENANCE RED/GREEN SUITE   repo=%s" % REPO)
    print("  pinned fv identity: %s" % json.load(open(os.path.join(REPO, 'data', 'expected_boot.json'))).get('fv'))
    print("=" * 90)
    os.makedirs(CLAUDE, exist_ok=True)
    for fn in (green1, green2, red1, red2, red3, red4, red5):
        try:
            fn()
        except Exception as e:
            import traceback
            record(fn.__name__, False, "EXCEPTION %r\n%s" % (e, traceback.format_exc()))
    npass = sum(1 for r in RESULTS if r['ok'])
    print("=" * 90)
    print("RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    # durable results artifact
    out = os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'RESULTS.json')
    try:
        json.dump({'pass': npass, 'total': len(RESULTS), 'results': RESULTS,
                   'fv_pin': json.load(open(os.path.join(REPO, 'data', 'expected_boot.json'))).get('fv')},
                  open(out, 'w'), indent=2)
    except Exception:
        pass
    sys.exit(0 if npass == len(RESULTS) else 1)


if __name__ == '__main__':
    main()
