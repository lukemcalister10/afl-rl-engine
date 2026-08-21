#!/usr/bin/env python3
"""DURABLE FORWARD-VALUATION PROVENANCE RED/GREEN SUITE (fv-provenance remediation 2026-07-20).

Proves the fail-closed forward-valuation / rl_model / config provenance fix end-to-end. Self-contained: it
builds the board in a fresh disposable staging copy of the checkout, with a controlled environment, and asserts
the outcome. Runs locally and on a clean CI runner (.github/workflows/fv-provenance.yml).

NO GATING CHECK HERE NAMES A BOARD ID (2026-07-28, issue #239). Four of them used to, and #217's pricing
split — which legitimately moved the board and correctly held the reference because nothing is adopted —
turned all four red at once (4/8) while every property they exist to prove still held. The board was
standing in for "a normal build happened". The properties are asserted directly instead, against md5s
computed live from the checkout, so nothing here goes stale when the board moves at #225 or at adoption.

The accepted-board content comparison DOES need a board identity and keeps its pin, but it is opt-in and
does not gate:  python3 test_fv_provenance.py --board-oracle

Scenarios (audit's §7 red/green standard):
  GREEN 1  strict canonical build (RL_FV=checkout, balanced config)         -> the loaded forward-valuation
                                                                               and rl_model are byte-identical
                                                                               to this checkout
  GREEN 2  provenance record emitted before export                          -> RL_FV, resolved dir, FV identity,
                                                                               dp path+hash, rl_model path+hash,
                                                                               config_manifest path+identity
  RED 1    stale 21d530bf at the FORMER ambient workspace path              -> ignored: the loaded dp is the
                                                                               checkout's, not the stale fixture
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
BOARD_MD5_GOOD = '7c32a540578b799922daea41d8acdfa2'   # ITEM 411 D1 (owner rulings v467/v469): accepted R19 balanced/strict board (advanced from 1373e824, the ITEM 408 STOP-1 board)
BAD_PREFIX = 'd7a95e8d'
STALE_DP = os.path.join(FIX, 'distribution_pricing.stale_21d530bf.py')

# The run verdict. NOT committed (see .gitignore) and removed before the first check runs — see main().
RESULTS_PATH = os.path.join(REPO, 'session_2026-07-20', 'fv_provenance_remediation', 'RESULTS.json')

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
    # frozen artifacts the engine loads by ABSOLUTE path (mirrors bootstrap.sh)
    for name in ('cm_400.pkl', 'q97m.pkl', 'v0surf.pkl'):
        src = os.path.join(REPO, 'data', name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(CLAUDE, name))
    # compute.py reads /home/claude/rl_build/rl_app_data.json at IMPORT time (the "before" analysis panel);
    # its CONTENT does not affect the board md5, but the FILE must EXIST or the engine import fails
    # (bootstrap.sh line 58 seeds it). On a fresh runner /home/claude is empty, so seed it here.
    rb_src = os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')
    if os.path.exists(rb_src):
        os.makedirs(os.path.join(CLAUDE, 'rl_build'), exist_ok=True)
        shutil.copy2(rb_src, os.path.join(CLAUDE, 'rl_build', 'rl_app_data.json'))


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


# ---- WHAT THE PROVENANCE CHECKS ASSERT, AND WHY IT IS NOT A BOARD ID -------------------------------
# Until 2026-07-28 four checks (GREEN1, GREEN2, RED1, RED5) gated on `board_md5 == BOARD_MD5_GOOD`. The
# board id was standing in for "a normal build happened", so when #217's pricing split legitimately moved
# the board all four went red at once — 4/8 — while every property they exist to prove still held. The
# board is EVIDENCE, not the property.
#
# The properties are observable directly, in the provenance record the build emits, against md5s computed
# LIVE from the checkout at test time. Nothing below is pinned, so none of it goes stale when the board
# moves at #225 or at adoption.
def _realpath(p):
    return os.path.realpath(p) if p else ''


def _under(child, parent):
    """True when `child` is `parent` or sits beneath it. A real path test — the retired-path check used
    substring containment, which both false-positives on a sibling like /home/claude/rl_after_old and
    silently returns None when the path is empty."""
    c, p = _realpath(child), _realpath(parent)
    if not c or not p:
        return False
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def _fv_selection(prov):
    """Was the CHECKED-OUT forward-valuation the thing actually loaded? Answered from the emitted record
    against the live checkout, never against a remembered value."""
    p = prov or {}
    want_dir = os.path.join(REPO, 'engine', 'forward_valuation')
    live_dp = _md5(os.path.join(want_dir, 'distribution_pricing.py'))
    stale_dp = _md5(STALE_DP) if os.path.exists(STALE_DP) else None
    got_dp = p.get('distribution_pricing_md5')
    return {'dir_ok': _realpath(p.get('resolved_fv_dir')) == _realpath(want_dir),
            'dp_ok': bool(got_dp) and got_dp == live_dp,
            'dp_is_stale': bool(got_dp) and got_dp == stale_dp,
            'got_dp': (got_dp or '')[:8], 'live_dp': live_dp[:8],
            'resolved': p.get('resolved_fv_dir')}


def _rl_model_selection(prov):
    """Was the VERIFIED rl_model used — the checkout's bytes, not something planted on a retired path?"""
    p = prov or {}
    live = _md5(os.path.join(REPO, 'engine', 'rl_after', 'rl_model.py'))
    got = p.get('rl_model_md5')
    path = p.get('rl_model_path') or ''
    return {'md5_ok': bool(got) and got == live, 'path': path,
            'not_retired': bool(path) and not _under(path, RL_AFTER_LINK),
            'got': (got or '')[:8], 'live': live[:8]}


def _built(r):
    """A canonical build completed and wrote a board. Replaces `board_md5 == <pin>` as the green control:
    it says the build succeeded without saying which board this month's engine produces."""
    return r['rc'] == 0 and r['board_md5'] is not None


RESULTS = []
def record(name, ok, detail):
    RESULTS.append({'name': name, 'ok': bool(ok), 'detail': detail})
    print("  [%s] %s — %s" % ('PASS' if ok else 'FAIL', name, detail))


# ============================ GREEN 1 — strict canonical build + full-vector zero movers ============================
def green1():
    """The green control: an explicit RL_FV=checkout build succeeds and demonstrably loaded the checkout.

    It no longer asserts WHICH board comes out. That was the stand-in for "a normal build happened", and it
    made this check a hostage to every legitimate engine change. What it proves now is stronger and is the
    thing the suite is actually for: the forward-valuation that got loaded is the one in this checkout,
    byte-for-byte, and the rl_model with it."""
    r = _run_build({}, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'))
    fv, rlm = _fv_selection(r['prov']), _rl_model_selection(r['prov'])
    built = _built(r)
    ok = built and fv['dir_ok'] and fv['dp_ok'] and not fv['dp_is_stale'] and rlm['md5_ok']
    _tail = '' if ok else '  ::STDERR_TAIL:: ' + ' | '.join((r['stderr'] or '').strip().splitlines()[-4:])
    record('GREEN1_checkout_fv_selected', ok,
           "built=%s(rc=%s board=%s) fv_dir_is_checkout=%s loaded_dp=%s/checkout_dp=%s dp_is_stale_fixture=%s "
           "loaded_rl_model=%s/checkout_rl_model=%s%s"
           % (built, r['rc'], (r['board_md5'] or '')[:8], fv['dir_ok'], fv['got_dp'], fv['live_dp'],
              fv['dp_is_stale'], rlm['got'], rlm['live'], _tail))
    shutil.rmtree(r['base'], ignore_errors=True)
    return r


# ==================== BOARD-CONTENT ORACLE — opt-in, NOT one of the gating checks ====================
def board_oracle():
    """Does the canonical build still reproduce the ACCEPTED board, value for value?

    This one genuinely cannot be expressed without a board identity: "has any player's value moved since
    the accepted reference" has no meaning except against a specific accepted board, and the reference
    vector is that board. So it keeps its pin — and it is deliberately NOT in the gating list, because its
    expected answer is *false* for the whole of a baseline effort. #217's split moved the board on purpose
    and #225 will move it again; a check that reads "red" throughout is the shape issue #231 removed.

    Run it when the answer is supposed to be yes:  python3 test_fv_provenance.py --board-oracle

    The pinned tokens below (BOARD_MD5_GOOD, the reference filename, the three aggregates and the
    expect-string) are ALSO the six structural anchors sibling_repin._repair_fv_oracle rewrites on every
    board move, and it raises SiblingRepinError unless each matches exactly once. Do not delete or
    duplicate them — removing the pin from this file breaks the machine that maintains it."""
    r = _run_build({}, rl_fv=os.path.join(REPO, 'engine', 'forward_valuation'))
    ok = (r['rc'] == 0 and r['board_md5'] == BOARD_MD5_GOOD)
    facts = _board_facts(r['board_path']) if r['board_path'] else {}
    ok = ok and facts.get('active') == 804 and facts.get('sum_v') == 700756 and facts.get('sheezel') == 10476
    # C5: compare the COMPLETE active-player value vector against the accepted reference — require ZERO movers.
    movers = None
    ref_path = os.path.join(FIX, 'reference_vector_7c32a540.json')
    if r['board_path'] and os.path.exists(ref_path):
        ref = json.load(open(ref_path))['vector']
        built = {p['key']: p['v'] for p in json.loads(open(r['board_path'], 'rb').read())['active']}
        both = set(ref) & set(built)
        movers = [k for k in both if ref[k] != built[k]]
        only_ref = set(ref) - set(built); only_built = set(built) - set(ref)
        ok = ok and len(movers) == 0 and not only_ref and not only_built and len(both) == 804
    else:
        # The reference must exist or this proves nothing — previously its absence silently skipped the
        # whole vector comparison and the check still passed on the aggregates alone.
        ok = False
        movers = None
    record('ORACLE_accepted_board_zero_movers', ok,
           "rc=%s md5=%s active=%s sumv=%s sheezel=%s vector_movers=%s ref_present=%s (expect 7c32a540/804/700756/10476/0)"
           % (r['rc'], r['board_md5'], facts.get('active'), facts.get('sum_v'), facts.get('sheezel'),
              (len(movers) if movers is not None else '?'), os.path.exists(ref_path)))
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
    missing = [k for k in need if not p.get(k)]
    matched = (p.get('fv_identity') == p.get('fv_identity_expected'))
    marker = 'PROVENANCE ' in (r['stderr'] or '')
    built = _built(r)
    # EVERY conjunct below appears in the record string. The previous version gated on four conditions and
    # printed three, so when it failed on the unprinted one it reported all-True and failed anyway — which
    # cost a full diagnosis cycle before anyone could see the cause. A check must name its own failure.
    ok = present and matched and marker and built
    record('GREEN2_provenance_record', ok,
           "all_fields=%s%s fv_identity==expected=%s stderr_marker=%s built=%s(rc=%s board=%s) "
           "(fv=%s dp=%s rlm=%s cfg=%s)"
           % (present, ('' if present else ' missing=%s' % ','.join(missing)), matched, marker,
              built, r['rc'], (r['board_md5'] or '')[:8], (p.get('fv_identity') or '')[:8],
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
    fv = _fv_selection(r['prov'])
    # The property is "the stale ambient module was NOT the one loaded", and the provenance record answers
    # that directly: the loaded distribution_pricing is byte-identical to the checkout's and is not the
    # stale fixture. That is the mechanism itself, where the old board-id comparison was an inference from
    # a downstream artifact — and unlike the board id, neither value moves when the engine changes.
    not_bad = (r['board_md5'] is not None and not str(r['board_md5']).startswith(BAD_PREFIX))
    files_unchanged = (before == after)
    ok = (stale_here and _built(r) and fv['dir_ok'] and fv['dp_ok']
          and not fv['dp_is_stale'] and not_bad and files_unchanged)
    record('RED1_stale_ambient_ignored', ok,
           "stale_seeded=%s built=%s(rc=%s) loaded_dp=%s/checkout_dp=%s dp_is_stale_fixture=%s "
           "fv_dir_is_checkout=%s board=%s never_%s=%s files_unchanged=%s"
           % (stale_here, _built(r), r['rc'], fv['got_dp'], fv['live_dp'], fv['dp_is_stale'],
              fv['dir_ok'], (r['board_md5'] or '')[:8], BAD_PREFIX, not_bad, files_unchanged))
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


# ============================ RED 4 — config manifest fail-closed (4 cases) -> HALT before board ============================
def _config_red_build(rl_repo, prepend_pp=None, strip_ws_config=False):
    """Bake-mode rl_export with controlled RL_REPO + import path. The trusted config_manifest is loaded BY PATH
    from RL_REPO; prepend_pp / strip_ws_config let us control exactly what a bare `import config_manifest` could
    resolve to on sys.path. Returns dict(rc, board(bool), stderr, base)."""
    base, ws = _staging()
    _seed_pkls()
    if strip_ws_config:
        try: os.remove(os.path.join(ws, 'config_manifest.py'))
        except OSError: pass
    env = dict(os.environ)
    for k in ('RL_PVC2', 'RL_LEGE', 'RL_LEGF', 'RL_V0SURF_REFIT'):
        env.pop(k, None)
    pp = ([prepend_pp] if prepend_pp else []) + [ws, os.path.join(CLAUDE, 'rl_vendor')]
    env.update({'RL_REPO': rl_repo, 'RL_FV': os.path.join(REPO, 'engine', 'forward_valuation'),
                'RL_CONFIG_MODE': 'bake', 'RL_PRIOR_TREES': '400', 'PYTHONHASHSEED': '0',
                'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1',
                'PYTHONPATH': ':'.join(pp)})
    board = os.path.join(ws, 'rl_app_data.json')
    try: os.remove(board)
    except OSError: pass
    p = subprocess.run([sys.executable, 'rl_export.py'], cwd=ws, env=env, capture_output=True, text=True)
    return {'rc': p.returncode, 'board': os.path.exists(board), 'stderr': p.stderr, 'base': base}


def _scratch_root(with_config=True, tamper=False, stub_enforce=False):
    d = tempfile.mkdtemp(prefix='fvcfg_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    os.makedirs(os.path.join(d, 'data'), exist_ok=True)
    shutil.copy2(os.path.join(REPO, 'data', 'expected_boot.json'), os.path.join(d, 'data', 'expected_boot.json'))
    mc = json.load(open(os.path.join(REPO, 'data', 'model_config.json')))
    if tamper:
        mc['vars']['RL_PRIOR_TREES'] = '999'
    json.dump(mc, open(os.path.join(d, 'data', 'model_config.json'), 'w'))
    if stub_enforce:
        with open(os.path.join(d, 'config_manifest.py'), 'w') as f:
            f.write("import os\n"
                    "def repo_root(root=None): return os.environ.get('RL_REPO') or '.'\n"
                    "def manifest_path(root=None): return os.path.join(repo_root(root),'data','model_config.json')\n"
                    "def manifest_hash(root=None): return 'stub'\n"
                    "def enforce(mode=None, halt=True): return None   # never returns an accepted identity\n")
    elif with_config:
        shutil.copy2(os.path.join(REPO, 'config_manifest.py'), os.path.join(d, 'config_manifest.py'))
    return d


def red4():
    before = _snapshot_guarded()
    results = []
    # 4a MISSING: RL_REPO has no config_manifest.py -> load-by-path ABSENT -> HALT
    root_a = _scratch_root(with_config=False)
    ra = _config_red_build(root_a)
    results.append(('4a_missing', ra['rc'] != 0 and not ra['board'] and 'ABSENT' in ra['stderr'],
                    "rc=%s board=%s" % (ra['rc'], ra['board'])))
    shutil.rmtree(ra['base'], ignore_errors=True); shutil.rmtree(root_a, ignore_errors=True)
    # 4b MISMATCH: tampered model_config.json under RL_REPO -> enforce hash-vs-pin -> HALT
    root_b = _scratch_root(tamper=True)
    rb = _config_red_build(root_b, strip_ws_config=True)
    results.append(('4b_mismatch', rb['rc'] != 0 and not rb['board'] and ('REJECTED' in rb['stderr'] or 'hash' in rb['stderr']),
                    "rc=%s board=%s" % (rb['rc'], rb['board'])))
    shutil.rmtree(rb['base'], ignore_errors=True); shutil.rmtree(root_b, ignore_errors=True)
    # 4c SHADOW: a foreign config_manifest earlier on sys.path (diff bytes, fake-valid identity) -> HALT
    shadow_dir = tempfile.mkdtemp(prefix='fvshadow_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    with open(os.path.join(shadow_dir, 'config_manifest.py'), 'w') as f:
        f.write("import os\n# FOREIGN config_manifest (red fixture) — returns an apparently valid identity\n"
                "def repo_root(root=None): return os.environ.get('RL_REPO') or '.'\n"
                "def manifest_path(root=None): return os.path.join(repo_root(root),'data','model_config.json')\n"
                "def manifest_hash(root=None): return 'c0ffee'*10\n"
                "def enforce(mode=None, halt=True): return 'c0ffee'*10   # pretends to accept, enforces nothing\n")
    rc = _config_red_build(REPO, prepend_pp=shadow_dir, strip_ws_config=True)
    results.append(('4c_shadow', rc['rc'] != 0 and not rc['board'] and 'shadow' in rc['stderr'].lower(),
                    "rc=%s board=%s" % (rc['rc'], rc['board'])))
    shutil.rmtree(rc['base'], ignore_errors=True); shutil.rmtree(shadow_dir, ignore_errors=True)
    # 4d NO-IDENTITY: trusted config_manifest.enforce() returns None -> HALT
    root_d = _scratch_root(stub_enforce=True)
    rd = _config_red_build(root_d, strip_ws_config=True)
    results.append(('4d_noident', rd['rc'] != 0 and not rd['board'] and ('accepted config identity' in rd['stderr'] or 'did not return' in rd['stderr']),
                    "rc=%s board=%s" % (rd['rc'], rd['board'])))
    shutil.rmtree(rd['base'], ignore_errors=True); shutil.rmtree(root_d, ignore_errors=True)
    after = _snapshot_guarded()
    ok = all(x[1] for x in results) and (before == after)
    record('RED4_config_manifest_failclosed_4cases', ok,
           "; ".join("%s:%s" % (n, 'ok' if o else 'BAD(%s)' % d) for n, o, d in results) + " files_unchanged=%s" % (before == after))


# ============================ RED 5 — RETIRED /home/claude/rl_after path ignored (defence-in-depth) ============================
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
        rlm = _rl_model_selection(r['prov'])
        no_breach = 'provenance breach' not in (r['stderr'] or '')
        # Strongest proof: the build SUCCEEDED at all. The planted rl_model raises on import, so any build
        # that completes did not import it — that holds whatever board the engine currently produces, which
        # is why this no longer compares a board id. Additionally the record must name a verified rl_model
        # (checkout bytes) that does not sit under the retired path.
        ok = (_built(r) and no_breach and rlm['not_retired'] and rlm['md5_ok'] and (before == after))
        record('RED5_retired_rl_after_path_ignored', ok,
               "built=%s(rc=%s board=%s) no_breach_on_stderr=%s rl_model_path=%s not_under_%s=%s "
               "loaded_rl_model=%s/checkout_rl_model=%s files_unchanged=%s"
               % (_built(r), r['rc'], (r['board_md5'] or '')[:8], no_breach, rlm['path'] or '<none>',
                  RL_AFTER_LINK, rlm['not_retired'], rlm['got'], rlm['live'], before == after))
        shutil.rmtree(r['base'], ignore_errors=True)
    finally:
        try: os.remove(foreign)
        except OSError: pass
        if saved and os.path.exists(saved):
            shutil.move(saved, foreign)


# ============================ RED 6 — ACTIVE foreign rl_model preloaded/reused -> HALT before board ============================
def red6():
    """Actively make a FOREIGN rl_model the module Python reuses: a sitecustomize on the path preloads a
    byte-different rl_model (a real copy + a marker comment, so the engine still runs) into sys.modules BEFORE
    rl_export imports it. The engine reuses that preloaded module; the actual-loaded rl_model proof must HALT
    (loaded bytes != trusted checkout) before any board is written. Proves protection of the rl_model ACTUALLY
    used, not merely the retired hardcoded path (RED5)."""
    before = _snapshot_guarded()
    base, ws = _staging()
    _seed_pkls()
    # foreign rl_model = the real one + a marker comment (functionally identical, byte-different)
    preload = tempfile.mkdtemp(prefix='fvpreload_', dir=CLAUDE if os.path.isdir(CLAUDE) else None)
    foreign_rl = os.path.join(preload, 'foreign_rl_model.py')
    with open(foreign_rl, 'w') as f:
        f.write("# FOREIGN rl_model (red fixture) — real engine bytes + this marker => byte-different, provenance breach\n")
        f.write(open(os.path.join(REPO, 'engine', 'rl_after', 'rl_model.py')).read())
    with open(os.path.join(preload, 'sitecustomize.py'), 'w') as f:
        f.write("import os, sys, importlib.util as _u\n"
                "_p = os.environ.get('FV_FOREIGN_RL')\n"
                "if _p and os.path.exists(_p):\n"
                "    _s = _u.spec_from_file_location('rl_model', _p); _m = _u.module_from_spec(_s)\n"
                "    sys.modules['rl_model'] = _m; _s.loader.exec_module(_m)\n")
    env = dict(os.environ)
    for k in ('RL_PVC2', 'RL_LEGE', 'RL_LEGF', 'RL_V0SURF_REFIT', 'RL_CONFIG_MODE'):
        env.pop(k, None)
    env.update({'RL_REPO': REPO, 'RL_FV': os.path.join(REPO, 'engine', 'forward_valuation'),
                'RL_PVC2': '1', 'RL_LEGE': '0', 'RL_LEGF': '0', 'RL_PRIOR_TREES': '400', 'PYTHONHASHSEED': '0',
                'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1', 'NUMEXPR_NUM_THREADS': '1',
                'FV_FOREIGN_RL': foreign_rl,
                'PYTHONPATH': ':'.join([preload, ws, REPO, os.path.join(CLAUDE, 'rl_vendor')])})
    board = os.path.join(ws, 'rl_app_data.json')
    try: os.remove(board)
    except OSError: pass
    p = subprocess.run([sys.executable, 'rl_export.py'], cwd=ws, env=env, capture_output=True, text=True)
    after = _snapshot_guarded()
    halted = (p.returncode != 0 and not os.path.exists(board))
    named = ('ACTIVE rl_model PROVENANCE' in p.stderr or 'not byte-identical to the trusted' in p.stderr)
    ok = halted and named and (before == after)
    record('RED6_active_foreign_rl_model_halts', ok,
           "rc=%s board=%s named_rl_model_halt=%s files_unchanged=%s"
           % (p.returncode, os.path.exists(board), named, before == after))
    shutil.rmtree(base, ignore_errors=True); shutil.rmtree(preload, ignore_errors=True)


def main():
    # The gating suite asserts PROVENANCE properties only — none of them names a board id, so the suite
    # does not need editing when the board moves at #225 or at adoption. `--board-oracle` additionally runs
    # the accepted-board content comparison, whose expected answer is only "yes" once a board is adopted.
    oracle = '--board-oracle' in sys.argv[1:]
    print("=" * 90)
    print("FORWARD-VALUATION PROVENANCE RED/GREEN SUITE   repo=%s" % REPO)
    print("  pinned fv identity: %s" % json.load(open(os.path.join(REPO, 'data', 'expected_boot.json'))).get('fv'))
    print("  mode: provenance%s" % (" + accepted-board oracle" if oracle else
                                    "  (board-content oracle NOT run — pass --board-oracle)"))
    print("=" * 90)
    os.makedirs(CLAUDE, exist_ok=True)

    # THE VERDICT MUST NEVER OUTLIVE THE RUN THAT WROTE IT.
    # RESULTS.json used to be committed, carrying `pass: 8/8` from the 06d8af60 era, and
    # fv-provenance.yml uploads whatever is on disk (`if: always()`, `if-no-files-found: ignore`) while
    # the write below used to sit in a bare `except: pass`. So a run that died early, or whose write
    # failed, published a green verdict for a suite that had not passed — a false success signal sitting
    # in the tree. Deleting it here, BEFORE any check runs, means the only file that can ever be uploaded
    # is one this run wrote. Absence uploads nothing, and absence cannot be mistaken for a pass.
    try:
        os.remove(RESULTS_PATH)
    except FileNotFoundError:
        pass
    except OSError as e:
        print("  [FAIL] could not clear the previous RESULTS.json (%r) — refusing to run, because a "
              "stale verdict could be uploaded as this run's." % (e,))
        sys.exit(1)

    checks = (green1, green2, red1, red2, red3, red4, red5, red6)
    if oracle:
        checks = checks + (board_oracle,)
    for fn in checks:
        try:
            fn()
        except Exception as e:
            import traceback
            record(fn.__name__, False, "EXCEPTION %r\n%s" % (e, traceback.format_exc()))
    npass = sum(1 for r in RESULTS if r['ok'])
    print("=" * 90)
    print("RESULT: %d/%d PASS" % (npass, len(RESULTS)))
    # Durable results artifact. The write is NO LONGER swallowed: a run that cannot record its own
    # verdict does not get to exit 0, because "succeeded but left no evidence" is the same false-success
    # shape as the stale committed file this replaced.
    wrote = True
    try:
        with open(RESULTS_PATH, 'w') as fh:
            json.dump({'pass': npass, 'total': len(RESULTS), 'results': RESULTS,
                       'fv_pin': json.load(open(os.path.join(REPO, 'data', 'expected_boot.json'))).get('fv')},
                      fh, indent=2)
    except Exception as e:
        wrote = False
        print("  [FAIL] RESULTS.json could not be written: %r" % (e,))
        print("         No artifact will be uploaded, so nothing can read this run as a pass — but the")
        print("         run itself is now a FAILURE, because it has no durable record of what it proved.")
    sys.exit(0 if (npass == len(RESULTS) and wrote) else 1)


if __name__ == '__main__':
    main()
