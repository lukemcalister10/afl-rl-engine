#!/usr/bin/env python3
"""BOOT-STORE GUARD — Guard 5 of the single-source family (stale-boot hardening, 2026-07-05).

WHY THIS EXISTS
  The four data guards (single_source.py) protect the DATA MODEL — one writable source, derived
  read-only + stamped, lookalike tripwire, correction canary. They do NOT protect which DIRECTORY a
  script reads: single_source.py resolves `HERE = dirname(__file__)`, so when it (and the self-test)
  run from the persistent workspace copy `/home/claude/rl_workspace/rl_after`, they validate the
  workspace against ITSELF and pass — even when the workspace holds a stale store (e.g. baked-v2.4
  644d1254) while the checked-out repo carries the real candidate (e1b4d8bf). That is the exact hole
  that produced hours of ghost premises. This guard closes it: it asserts, on ENTRY, that the store a
  script is about to read equals BOTH (a) the checked-out repo's store and (b) the pinned expected in
  data/expected_boot.json — and HALTS (non-zero) with a loud message otherwise. No script proceeds
  against an unverified store.

DESIGN
  - Repo-anchored, never workspace-anchored: the checkout is located via RL_REPO / CLAUDE_PROJECT_DIR /
    this file's own directory (boot_guard.py lives at the repo root and is always invoked from the
    checkout), NEVER by walking up from a workspace copy (which has no path back to the checkout).
  - The pinned expected md5s live in ONE place (data/expected_boot.json); this is the manual
    three-assertion check (engine head / store / band) made automatic and permanent.
  - FAILS the build (SystemExit / non-zero exit), never warns — consistent with guards 1-4.

USAGE
  Python:  import boot_guard; boot_guard.assert_boot('ship_gates', store_path=RA + '/rl_model_data.json')
  Shell:   python3 boot_guard.py <label> <store_path> [<engine_head_path> [<band_path>]]  || exit 1
"""
import os, sys, json, hashlib

def repo_root():
    """Locate the CHECKED-OUT repo, robustly, from anywhere (incl. a workspace cwd)."""
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.dirname(os.path.abspath(__file__))):
        if cand and os.path.exists(os.path.join(cand, 'data', 'expected_boot.json')):
            return os.path.abspath(cand)
    # last resort: this file's dir (keeps a clear error if the manifest is genuinely absent)
    return os.path.dirname(os.path.abspath(__file__))

def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()

def expected(root=None):
    root = root or repo_root()
    with open(os.path.join(root, 'data', 'expected_boot.json')) as f:
        return json.load(f)

def _fmt(m):    # pinned file may hold either full md5 or 8-char; compare on the common prefix
    return (m or '')[:8]

def _cmp_on_pin_len(got, pin):
    """Compare a computed md5 against a pin ON THE PINNED LENGTH (S1 fix, register item 24): a FULL 32-char
    pin is enforced at full length; a legacy 8/12-char pin still matches on its prefix. This retires the
    'decorative pin' hole for the board field without breaking the store/register/config short pins."""
    got = got or ''; pin = pin or ''
    return bool(pin) and got[:len(pin)] == pin

def fv_provenance_fails(root=None):
    """FORWARD-VALUATION PROVENANCE assertions (Guard 5, fv-provenance remediation 2026-07-20). Returns a list
    of failure strings (empty == pass). Asserts BOTH:
      (a) CHECKOUT integrity  — the checked-out engine/forward_valuation source set == the pin ('fv');
      (b) LOADED-PATH integrity — the EXACT RL_FV directory the engine WILL import == the pin.
    On any mismatch (or an unresolved RL_FV path) the failure names the resolved RL_FV, the computed identity,
    the expected identity, and the failure class (checkout drift / loaded-path drift / unresolved path).
    Backward-compatible: no-op (empty list) when the 'fv' pin is absent from the manifest. FAIL-CLOSED: if the
    pin is present but fv_provenance cannot be imported, that is itself a failure (we cannot verify -> HALT)."""
    root = root or repo_root()
    exp = expected(root)
    pin = exp.get('fv')
    if pin is None:
        return []
    try:
        import fv_provenance as _fv
    except Exception as e:
        return ["fv pin present (%s) but fv_provenance is not importable (%r) — cannot verify the "
                "forward-valuation source set; refusing to boot on an unverified forward_valuation "
                "(fail-closed)." % (_fmt(pin), e)]
    fails = []
    # (a) checkout integrity — the repo's own engine/forward_valuation must equal the pin.
    ck_dir = _fv.checkout_fv_dir(root)
    ck_id = _fv.fv_identity(ck_dir)
    if ck_id is None:
        fails.append("fv CHECKOUT DRIFT: engine/forward_valuation source set is ABSENT/empty at %s — cannot "
                     "assert the forward-valuation pin %s (restore the checkout, or re-pin at a bake)."
                     % (ck_dir, _fmt(pin)))
    elif ck_id != pin:
        fails.append("fv CHECKOUT DRIFT: checked-out forward_valuation identity\n        %s\n        %s  !=  "
                     "pinned %s (data/expected_boot.json 'fv')\n        An engine/forward_valuation source "
                     "changed without re-stamping the pin (or the pin drifted). Re-pin at a bake in the same "
                     "commit that moves the source; never boot on an unverified forward_valuation."
                     % (ck_dir, ck_id, pin))
    # (b) loaded-path integrity — the EXACT dir the engine will import (RL_FV / checkout) must equal the pin.
    ld_dir = _fv.resolve_fv(root, halt=False)
    if ld_dir is None:
        fails.append("fv LOADED-PATH UNRESOLVED: RL_FV is unset and no checked-out engine/forward_valuation "
                     "was found via RL_REPO / CLAUDE_PROJECT_DIR — the engine has no verified forward-valuation "
                     "source to import (refusing an ambient-workspace fallback). Set RL_FV to the checked-out "
                     "engine/forward_valuation, or RL_REPO to the checkout root. (expected identity %s)"
                     % _fmt(pin))
    else:
        ld_id = _fv.fv_identity(ld_dir)
        if ld_id != pin:
            fails.append("fv LOADED-PATH DRIFT: the engine will IMPORT forward-valuation from\n        RL_FV=%s\n"
                         "        resolved dir %s\n        identity %s  !=  pinned %s (data/expected_boot.json "
                         "'fv')\n        An explicit RL_FV (or a stale workspace copy) points at a "
                         "forward_valuation tree that is NOT the pinned source — the exact stale-import hole "
                         "Guard 5 exists to close. Point RL_FV at the checked-out engine/forward_valuation (or "
                         "unset it so the checkout is used); never boot on an unverified loaded forward_valuation."
                         % (os.environ.get('RL_FV'), ld_dir, ld_id, pin))
    return fails


def assert_fv_provenance(root=None, halt=True):
    """Standalone fail-closed entry point for the forward-valuation provenance assertions (green/red proofs +
    the canonical board-build entry point call this before generation). HALT (SystemExit) on any failure."""
    fails = fv_provenance_fails(root)
    if fails:
        msg = ("\n============ FORWARD-VALUATION PROVENANCE (Guard 5) FAILED — BUILD HALTED ============\n"
               "  - " + "\n  - ".join(fails) +
               "\n=====================================================================================")
        if halt:
            raise SystemExit(msg)
        raise AssertionError(msg)
    return True


def assert_boot(label, store_path=None, engine_head_path=None, band_path=None, register_path=None, halt=True):
    """Assert the store (and optionally engine head / band / register) a script is about to READ matches the
    checked-out repo AND the pinned expected. HALT (SystemExit) on any mismatch. Returns True on pass.

    label            : short name of the caller, quoted in the halt message (e.g. 'run_panel').
    store_path       : the rl_model_data.json the caller will actually read (the workspace copy for the
                       engine-loading scripts). REQUIRED for the store assertion.
    engine_head_path : optional _merged_recover.py the caller will read (three-assertion parity).
    band_path        : optional cm_400.pkl the caller will read.
    register_path    : optional LTI_REGISTER.md the caller will read (R-REG=R2 pinned availability input).
    """
    root = repo_root()
    exp = expected(root)
    fails = []

    # (0) checkout integrity: the repo's own store must equal the pin. Catches a store swapped into the
    #     checkout without updating the pin (or a pin edited without re-baking) — either direction fails.
    repo_store = os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')
    repo_md5 = _md5(repo_store) if os.path.exists(repo_store) else None
    if _fmt(repo_md5) != _fmt(exp.get('store')):
        fails.append("checkout store %s != pinned store %s (data/expected_boot.json) — repo/pin out of sync"
                     % (_fmt(repo_md5), _fmt(exp.get('store'))))

    # (0r) register checkout integrity (R-REG=R2): the repo's own LTI_REGISTER.md must equal the pin, if a
    #      register pin is present. Backward-compatible: skipped when 'register' is absent from the manifest.
    exp_reg = exp.get('register')
    if exp_reg is not None:
        repo_reg = os.path.join(root, 'LTI_REGISTER.md')
        repo_reg_md5 = _md5(repo_reg) if os.path.exists(repo_reg) else None
        if _fmt(repo_reg_md5) != _fmt(exp_reg):
            fails.append("checkout register %s != pinned register %s (data/expected_boot.json 'register') — "
                         "owner edited LTI_REGISTER.md without re-pinning, or the pin drifted"
                         % (_fmt(repo_reg_md5), _fmt(exp_reg)))

    # (0b) config integrity (gate-integrity 2026-07-09, the durable half of R3): the model-config manifest
    #     hash must equal the pinned boot config. Makes Guard 5 a code+store+CONFIG check — a model-semantics
    #     var can no longer drift into a bake unnoticed. Backward-compatible: skipped if either the manifest
    #     (data/model_config.json) or the pinned 'config' field is absent.
    exp_cfg = exp.get('config')
    if exp_cfg is not None and os.path.exists(os.path.join(root, 'data', 'model_config.json')):
        try:
            import config_manifest as _cm
            got_cfg = _cm.manifest_hash(root)
        except Exception:
            got_cfg = None
        if got_cfg is not None and got_cfg != exp_cfg:
            fails.append("model config hash %s != pinned boot config %s (data/expected_boot.json 'config') — "
                         "the model configuration (data/model_config.json) and the pin are out of sync"
                         % (_fmt(got_cfg), _fmt(exp_cfg)))

    # (0c) board checkout-integrity (S1 fix, register item 24): expected_boot's 'board' pin was DECORATIVE —
    #      boot_guard never asserted it, so a board could drift from the pin unnoticed (the exact hole that let
    #      the override-less board ship). Assert the checked-out board (data/rl_build/rl_app_data.json) equals
    #      the pin, AT FULL HASH when the pin is full (the 8-char _fmt truncation is retired for this field).
    #      Backward-compatible: skipped when the 'board' pin is absent.
    exp_board = exp.get('board')
    if exp_board is not None:
        repo_board = os.path.join(root, 'data', 'rl_build', 'rl_app_data.json')
        repo_board_md5 = _md5(repo_board) if os.path.exists(repo_board) else None
        if repo_board_md5 is None:
            fails.append("board pin present (%s) but data/rl_build/rl_app_data.json is ABSENT — cannot assert "
                         "the board (re-generate + re-pin the board)" % _fmt(exp_board))
        elif not _cmp_on_pin_len(repo_board_md5, exp_board):
            fails.append("checkout board %s != pinned board %s (data/expected_boot.json 'board', full-hash "
                         "compare) — the board and its pin are out of sync (re-generate + re-pin, or the pin "
                         "drifted)" % (_fmt(repo_board_md5), _fmt(exp_board)))

    # (0f) rl_model checkout-integrity (L-CAPTAIN prerequisite (1), 2026-07-15): the 'rl_model' pin has always
    #      been present and CORRECT — it was simply never CHECKED (the one engine source Guard 5 did not assert;
    #      capt_prem lived in the one file the guard could not see). Assert the checked-out rl_model source
    #      (engine/rl_after/rl_model.py) equals the pin exactly as (0) asserts the store: compute its md5, compare
    #      to the pin, HALT (never warn) on mismatch. Full-hash compare (the pin is a full 32-char md5). SILENCE
    #      IS A RED — the verdict prints on the PASS line below, or the boot HALTs here. Backward-compatible:
    #      skipped when the 'rl_model' pin is absent from the manifest.
    exp_rl = exp.get('rl_model')
    repo_rl_md5 = None
    if exp_rl is not None:
        repo_rl = os.path.join(root, 'engine', 'rl_after', 'rl_model.py')
        repo_rl_md5 = _md5(repo_rl) if os.path.exists(repo_rl) else None
        if repo_rl_md5 is None:
            fails.append("rl_model pin present (%s) but engine/rl_after/rl_model.py is ABSENT — cannot assert the "
                         "rl_model source (restore rl_model.py, or re-pin at a bake)" % _fmt(exp_rl))
        elif not _cmp_on_pin_len(repo_rl_md5, exp_rl):
            fails.append("checkout rl_model %s != pinned rl_model %s (data/expected_boot.json 'rl_model', full-hash "
                         "compare) — the rl_model source (engine/rl_after/rl_model.py) and its pin are out of sync "
                         "(re-pin at a bake, or the pin drifted; never boot on an unverified rl_model)"
                         % (_fmt(repo_rl_md5), _fmt(exp_rl)))

    # (0d) FITTED-ARTIFACT checkout-integrity (q97m FREEZE 2026-07-14, owner ruling): assert every FITTED artifact
    #      that determines the board equals its pin, exactly as (0)/(0c) do for the store/board. These run
    #      automatically on EVERY assert_boot entry (no caller need pass a path), so a wrong or missing frozen
    #      artifact HALTS on line one for panel, gate, build and self-test alike. Backward-compatible: each field
    #      is skipped when absent from the manifest. Full-hash compare (the pins are full 32-char md5s).
    _FITTED = (('q97m',         os.path.join('data', 'q97m.pkl')),
               ('v0surf',       os.path.join('data', 'v0surf.pkl')),   # LEG F6 FREEZE 2026-07-18: the frozen V0 pick-curve surface (_iso_dec residual weather)
               ('peak_model',   os.path.join('engine', 'rl_after', 'peak_model_v4.pkl')),
               ('pvc_snapshot', os.path.join('engine', 'rl_after', 'pvc_snapshot.json')),
               ('bust_prior',   os.path.join('engine', 'rl_after', 'bust_prior_table.json')))
    for _field, _rel in _FITTED:
        _pin = exp.get(_field)
        if _pin is None:
            continue
        _fp = os.path.join(root, _rel)
        _fm = _md5(_fp) if os.path.exists(_fp) else None
        if _fm is None:
            fails.append("%s pin present (%s) but %s is ABSENT — cannot assert the frozen artifact (re-freeze + "
                         "re-pin; for q97m run refit_q97m.py at a bake)" % (_field, _fmt(_pin), _rel))
        elif not _cmp_on_pin_len(_fm, _pin):
            fails.append("checkout %s %s != pinned %s (data/expected_boot.json '%s', full-hash compare) — the "
                         "FROZEN artifact %s and its pin are out of sync (re-freeze + re-pin, or the pin drifted; "
                         "the board's identity is made of this — never boot on an unverified fitted artifact)"
                         % (_field, _fmt(_fm), _fmt(_pin), _field, _rel))

    # (0e) LOADED-PATH integrity (q97m/cm load-path hole, register item 91; owner-caught 2026-07-14): block (0d)
    #      above asserts the REPO copy of each fitted artifact — but the ENGINE loads through its OWN precedence,
    #      and the workspace copy (and an env var) WIN over the repo. _load_q97m() (_merged_recover.py) resolves
    #      $RL_Q97M_PKL -> /home/claude/q97m.pkl -> <repo>/data/q97m.pkl; wire_redesign.build() loads
    #      /home/claude/cm_<RL_PRIOR_TREES>.pkl. So (0d) can PASS while the engine loads a DIFFERENT pickle — an
    #      env var could point the engine at ANY pickle on disk and the guard still passed (a guard that cannot
    #      fail; the very stale-boot hole Guard 5 exists to close, re-opened on the just-frozen artifact). This
    #      block resolves each artifact through the engine's EXACT precedence and asserts THE PATH THAT WILL
    #      ACTUALLY BE LOADED == the pin. HALT names the resolved path AND the expected pin. Skipped per-field
    #      when the pin is absent (backward-compatible).
    def _resolve_q97m_load():                 # mirror _merged_recover._load_q97m precedence, byte-for-byte
        for _c in (os.environ.get('RL_Q97M_PKL'), '/home/claude/q97m.pkl',
                   os.path.join(os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '', 'data', 'q97m.pkl')):
            if _c and os.path.exists(_c):
                return _c
        return None
    def _resolve_cm_load():                    # mirror wire_redesign.build() cache precedence
        _trees = os.environ.get('RL_PRIOR_TREES', '400')
        _cache = '/home/claude/cm_%s.pkl' % _trees
        return _cache if os.path.exists(_cache) else None
    def _resolve_v0surf_load():                # mirror _merged_recover._load_v0surf precedence, byte-for-byte
        for _c in (os.environ.get('RL_V0SURF_PKL'), '/home/claude/v0surf.pkl',
                   os.path.join(os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '', 'data', 'v0surf.pkl')):
            if _c and os.path.exists(_c):
                return _c
        return None
    _LOADED = (('q97m', exp.get('q97m'), _resolve_q97m_load(),
                '$RL_Q97M_PKL -> /home/claude/q97m.pkl -> <repo>/data/q97m.pkl',
                'the engine would FIT q97m at build time (the exact defect the freeze removed)'),
               ('v0surf', exp.get('v0surf'), _resolve_v0surf_load(),
                '$RL_V0SURF_PKL -> /home/claude/v0surf.pkl -> <repo>/data/v0surf.pkl',
                'the engine would FIT the shipped V0 pick-curve surface at build time (the _iso_dec weather the freeze removed)'),
               ('band', exp.get('band'), _resolve_cm_load(),
                '/home/claude/cm_%s.pkl (RL_PRIOR_TREES)' % os.environ.get('RL_PRIOR_TREES', '400'),
                'the engine would RETRAIN a non-canonical cm forest (DYNAMIC_ARCH, not bit-stable)'))
    for _fld, _pin, _lp, _prec, _elsemsg in _LOADED:
        if _pin is None:
            continue
        if _lp is None:
            fails.append("%s LOAD-PATH unresolved: the engine's precedence (%s) finds NO file on disk, so %s. "
                         "Re-run bootstrap.sh to seed the workspace copy." % (_fld, _prec, _elsemsg))
            continue
        _lm = _md5(_lp)
        if not _cmp_on_pin_len(_lm, _pin):
            fails.append("%s LOAD-PATH MISMATCH: the engine will LOAD\n        %s\n        md5 %s  !=  pinned %s "
                         "(data/expected_boot.json '%s', full-hash compare).\n        The engine's own precedence "
                         "(%s) resolved to a file that is NOT the pinned frozen artifact — an env var or a stale "
                         "workspace copy is shadowing the frozen source. Re-run bootstrap.sh (or unset the "
                         "override); never boot on an unverified LOADED artifact." % (_fld, _lp, _fmt(_lm), _fmt(_pin), _fld, _prec))

    def _chk(kind, path, pin, ref_md5):
        if path is None:
            return
        if not os.path.exists(path):
            fails.append("%s to read %s at %s — FILE ABSENT (re-run bootstrap.sh to seed the workspace)"
                         % (label, kind, path)); return
        got = _md5(path)
        if _fmt(got) != _fmt(pin):
            fails.append("%s about to read %s\n        at %s\n        md5 %s  !=  expected %s (pinned; repo checkout %s)\n"
                         "        STALE BOOT: this is not the checked-out store. Re-run bootstrap.sh to re-seed the "
                         "workspace from the checked-out source; never boot on an unverified store."
                         % (label, kind, path, _fmt(got), _fmt(pin), _fmt(ref_md5)))

    _chk('STORE  rl_model_data.json', store_path,       exp.get('store'),       repo_md5)
    _chk('ENGINE _merged_recover.py', engine_head_path, exp.get('engine_head'), None)
    _chk('BAND   cm_400.pkl',         band_path,        exp.get('band'),        None)
    if exp.get('register') is not None:
        _chk('REGISTER LTI_REGISTER.md', register_path, exp.get('register'),    None)

    # (0g) FORWARD-VALUATION provenance (fv-provenance remediation 2026-07-20): assert the checked-out
    #      engine/forward_valuation source set == the pin AND the EXACT RL_FV dir the engine will import ==
    #      the pin. Closes the exact hole that produced the 06d8af60 -> d7a95e8d 109-wobble (a stale
    #      distribution_pricing.py imported silently with no guard firing). Backward-compatible: no-op when
    #      the 'fv' pin is absent.
    fails.extend(fv_provenance_fails(root))

    if fails:
        msg = ("\n==================== STALE-BOOT GUARD (Guard 5) FAILED — BUILD HALTED ====================\n"
               "  - " + "\n  - ".join(fails) +
               "\n=========================================================================================")
        if halt:
            raise SystemExit(msg)
        raise AssertionError(msg)
    _rl_verdict = ("  |  rl_model %s == pinned %s" % (_fmt(repo_rl_md5), _fmt(exp_rl))) if exp_rl is not None else ""
    _fv_verdict = ("  |  fv %s == pinned %s (checkout+loaded-path)" % (_fmt(exp.get('fv')), _fmt(exp.get('fv')))) if exp.get('fv') is not None else ""
    print("boot-store guard (Guard 5) PASS  [%s]  store %s == pinned %s%s%s (%s)"
          % (label, _fmt(repo_md5), _fmt(exp.get('store')), _rl_verdict, _fv_verdict, exp.get('tag')))
    return True

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: boot_guard.py <label> <store_path> [<engine_head_path> [<band_path> [<register_path>]]]", file=sys.stderr)
        sys.exit(2)
    _label = sys.argv[1]
    _store = sys.argv[2]
    _eng   = sys.argv[3] if len(sys.argv) > 3 else None
    _band  = sys.argv[4] if len(sys.argv) > 4 else None
    _reg   = sys.argv[5] if len(sys.argv) > 5 else None
    try:
        assert_boot(_label, store_path=_store, engine_head_path=_eng, band_path=_band, register_path=_reg, halt=True)
    except SystemExit as e:
        if isinstance(e.code, str):
            print(e.code, file=sys.stderr)
            sys.exit(1)
        raise
