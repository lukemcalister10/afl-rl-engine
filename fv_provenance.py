#!/usr/bin/env python3
"""FORWARD-VALUATION PROVENANCE — fail-closed source-selection + identity (fv-provenance remediation, 2026-07-20).

WHY THIS EXISTS
  The 06d8af60 -> d7a95e8d 109-player wobble was NOT a valuation defect. It was an IMPORT-PROVENANCE
  defect: wire_redesign / par_redesign defaulted RL_FV to the AMBIENT workspace directory
  (/home/claude/rl_workspace/forward_valuation), which bootstrap.sh seeds from WHATEVER branch is checked
  out at container start. A stale distribution_pricing.py (md5 21d530bf, missing the Leg-C §1b current-season
  DPP law) got imported silently, the board diverged, and NO guard fired — data/expected_boot.json pinned the
  store/engine/q97m/v0surf but NOT the forward_valuation modules that feed current `v`. See
  session_2026-07-20/root_cause_109_wobble/ROOT_CAUSE.md.

WHAT THIS MODULE IS (and is NOT)
  It is the SINGLE canonical source-selection rule + the deterministic identity of the COMPLETE imported
  forward-valuation Python source set. It does NO engine math, reimplements NO valuation, tunes NO parameter.
  It only resolves a directory and hashes files. Repo-anchored (RL_REPO / CLAUDE_PROJECT_DIR), never
  workspace-anchored.

CANONICAL SOURCE-SELECTION RULE (fail-closed)
  1. An explicitly-supplied RL_FV wins (its identity is verified against the pin by Guard 5's loaded-path
     assertion — an explicit-but-stale RL_FV therefore HALTS, it is not trusted blindly).
  2. Otherwise the CHECKED-OUT repo's own engine/forward_valuation (located via RL_REPO / CLAUDE_PROJECT_DIR).
  3. Otherwise HALT. There is NO ambient-workspace fallback: a canonical build never silently reads a
     persistent workspace populated by a previous branch.

IDENTITY
  fv_identity(dir) = a canonical tree hash over the SORTED relative paths of every *.py in the directory,
  each combined with the sha256 of its exact bytes. The identity changes when ANY imported forward-valuation
  source changes (not just distribution_pricing.py). Pinned in data/expected_boot.json under 'fv'.
"""
import os, sys, hashlib, json


def repo_root(root=None):
    """Locate the CHECKED-OUT repo root, robustly, from anywhere (incl. a workspace cwd)."""
    for cand in (root, os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.dirname(os.path.abspath(__file__))):
        if cand and os.path.exists(os.path.join(cand, 'data', 'expected_boot.json')):
            return os.path.abspath(cand)
    return os.path.dirname(os.path.abspath(__file__))


def env_root(halt=True):
    """The TRUSTED checkout root, derived INDEPENDENTLY from the canonical environment only
    (RL_REPO / CLAUDE_PROJECT_DIR) — never from a possibly-shadowed module's own resolver, and never by
    walking up from a workspace copy. Must contain data/expected_boot.json. This is the anchor for
    fail-closed config-manifest / rl_model provenance: we decide the trusted root from the environment
    BEFORE trusting or executing any resolver a foreign module might supply."""
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR')):
        if cand and os.path.exists(os.path.join(cand, 'data', 'expected_boot.json')):
            return os.path.abspath(cand)
    if halt:
        raise SystemExit(
            "fv_provenance.env_root: no trusted checkout root — set RL_REPO or CLAUDE_PROJECT_DIR to the "
            "checkout (containing data/expected_boot.json). Refusing to anchor provenance to an untrusted "
            "module's own root (fail-closed).")
    return None


def load_trusted(root, modname):
    """Load EXACTLY <root>/<modname>.py by ABSOLUTE PATH — bypassing sys.path and any shadow — install it as
    sys.modules[modname], and return the module. HALT if the file is absent. Use this to execute a canonical
    module (config_manifest) from the trusted checkout, never whatever `import` happens to resolve."""
    import importlib.util
    path = os.path.join(root, modname + '.py')
    if not os.path.exists(path):
        raise SystemExit("fv_provenance.load_trusted: %s is ABSENT under the trusted root %s — cannot load the "
                         "canonical %s module (fail-closed)." % (path, root, modname))
    spec = importlib.util.spec_from_file_location(modname, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[modname] = mod
    spec.loader.exec_module(mod)
    return mod


def verify_config_manifest(mode, root=None, halt=True):
    """FAIL-CLOSED config-manifest verification for a CANONICAL build (bake/gate). Non-circular:
      1. anchor the trusted root from the ENVIRONMENT (env_root), not from config_manifest;
      2. HALT if a config_manifest is already loaded from a DIFFERENT file with DIFFERENT bytes (a shadow
         pre-empted enforcement) — this is why callers must run this BEFORE anything imports config_manifest;
      3. HALT if a bare `import config_manifest` WOULD resolve, via sys.path, to a DIFFERENT file with
         DIFFERENT bytes than the trusted one (a foreign config_manifest earlier on the path);
      4. execute the EXACT trusted <root>/config_manifest.py by path (install it in sys.modules);
      5. HALT if the manifest data file is absent, or enforce(mode) does not engage / returns no identity
         (enforce also HALTs internally on a manifest-hash-vs-pin mismatch or a divergent override).
    Returns (accepted_config_identity, trusted_root)."""
    root = root or env_root()
    trusted = os.path.join(root, 'config_manifest.py')
    tp = os.path.abspath(trusted)

    def _fail(msg):
        if halt:
            raise SystemExit("CANONICAL BUILD HALT (%s mode) — config provenance: %s" % (mode, msg))
        raise AssertionError(msg)

    if not os.path.exists(trusted):
        _fail("trusted config_manifest %s is ABSENT under the checkout root — cannot enforce the pinned model "
              "configuration (fail-closed)." % trusted)
    # (2) an already-cached config_manifest from a different file with different bytes = shadow that pre-empted us
    pre = sys.modules.get('config_manifest')
    if pre is not None:
        pf = os.path.abspath(getattr(pre, '__file__', '') or '')
        if pf and pf != tp and _file_md5(pf) != _file_md5(tp):
            _fail("a config_manifest is ALREADY loaded from %s (md5 %s), not the trusted %s (md5 %s) — a "
                  "shadow pre-empted enforcement; refusing to generate a board."
                  % (pf, _file_md5(pf)[:8], tp, _file_md5(tp)[:8]))
    # (3) sys.path shadow: what a bare `import config_manifest` WOULD resolve to
    import importlib.machinery as _im
    spec = _im.PathFinder.find_spec('config_manifest', list(sys.path))
    res = os.path.abspath(spec.origin) if (spec and getattr(spec, 'origin', None)) else None
    if res and res != tp and os.path.exists(res) and _file_md5(res) != _file_md5(tp):
        _fail("a foreign config_manifest %s (md5 %s) earlier on sys.path shadows the trusted %s (md5 %s) — "
              "refusing to generate a board (a bare import would execute the shadow)."
              % (res, _file_md5(res)[:8], tp, _file_md5(tp)[:8]))
    # (4) execute the EXACT trusted file by path
    cm = load_trusted(root, 'config_manifest')
    data = cm.manifest_path(root)
    if not os.path.exists(data):
        _fail("config manifest data file %s is ABSENT under the trusted root — cannot enforce." % data)
    # (5) enforce must engage and return the accepted identity (hash-vs-pin + reject-scan are inside enforce)
    h = cm.enforce(mode)
    if not h:
        _fail("config_manifest.enforce(%r) did not return an accepted config identity — enforcement did not "
              "engage; refusing to generate a board." % mode)
    return h, root


def assert_loaded_fv(loaded_files, root=None, halt=True):
    """ACTUAL-LOADED-MODULE proof (not a constructed path): every forward-valuation module Python actually
    LOADED must (a) live in the resolved forward_valuation directory the loader used, and (b) have bytes
    equal to the pinned per-file source hash (== the checkout, which Guard 5 asserts == the 'fv' pin). Covers
    spec-loaded siblings AND bare-import / sys.modules reuse (e.g. conditional_prior). `loaded_files` is a
    {label: abspath} map of the modules' real __file__. HALT on any drift."""
    root = root or env_root()
    fv_dir = os.path.abspath(resolve_fv(root))
    pinned = fv_source_hashes(checkout_fv_dir(root))     # trusted per-file hashes
    fails = []
    seen = 0
    for label, path in (loaded_files or {}).items():
        if not path:
            continue
        ap = os.path.realpath(os.path.abspath(path))
        base = os.path.basename(ap)
        if os.path.realpath(os.path.dirname(ap)) != os.path.realpath(fv_dir):
            fails.append("loaded FV module '%s' at %s is OUTSIDE the resolved forward_valuation dir %s "
                         "(an unpinned / stale source reached the engine)" % (label, ap, fv_dir))
            continue
        if base not in pinned:
            fails.append("loaded FV module '%s' (%s) is not a member of the pinned forward-valuation source "
                         "set" % (label, base))
            continue
        got = _sha256_file(ap)
        if got != pinned[base]:
            fails.append("loaded FV module '%s' (%s) bytes %s != pinned %s — the file actually imported is "
                         "not the pinned source" % (label, base, got[:12], pinned[base][:12]))
            continue
        seen += 1
    if seen == 0 and not fails:
        fails.append("no forward-valuation modules were observed as loaded — cannot prove the actual loaded "
                     "source (fail-closed)")
    if fails:
        msg = ("\n======== ACTUAL-LOADED FORWARD-VALUATION PROOF FAILED — BUILD HALTED ========\n  - "
               + "\n  - ".join(fails) + "\n=============================================================================")
        if halt:
            raise SystemExit(msg)
        raise AssertionError(msg)
    return True


def assert_loaded_rl_model(loaded_path, root=None, halt=True):
    """ACTIVE rl_model provenance: the rl_model the engine actually LOADED (its real __file__) must be
    byte-identical to the trusted checkout/staged engine/rl_after/rl_model.py. Not find_spec, not the
    provenance report — the bytes of the module Python reused. HALT if a foreign or stale rl_model is loaded
    or shadows the intended source. (Compares against the CHECKOUT source, never the boot-pin — the pin's
    pre-existing drift is out of scope and is NOT touched here.)"""
    root = root or env_root()
    trusted = os.path.join(root, 'engine', 'rl_after', 'rl_model.py')

    def _fail(msg):
        if halt:
            raise SystemExit("\n======== ACTIVE rl_model PROVENANCE FAILED — BUILD HALTED ========\n  - " + msg
                             + "\n=================================================================")
        raise AssertionError(msg)

    if not os.path.exists(trusted):
        _fail("trusted checkout rl_model %s is ABSENT — cannot verify the loaded rl_model." % trusted)
    if not loaded_path or not os.path.exists(loaded_path):
        _fail("the engine's loaded rl_model has no resolvable __file__ (%r) — cannot prove it is the trusted "
              "source." % loaded_path)
    lp = os.path.realpath(os.path.abspath(loaded_path))
    if _sha256_file(lp) != _sha256_file(trusted):
        _fail("the engine LOADED rl_model from\n        %s  (sha %s)\n     which is NOT byte-identical to the "
              "trusted checkout\n        %s  (sha %s)\n     — a foreign or stale rl_model was imported / "
              "shadowed the intended source; refusing to generate a board."
              % (lp, _sha256_file(lp)[:12], trusted, _sha256_file(trusted)[:12]))
    return True


def checkout_fv_dir(root=None):
    """The checked-out repo's own engine/forward_valuation (the canonical source)."""
    return os.path.join(repo_root(root), 'engine', 'forward_valuation')


def resolve_fv(root=None, halt=True):
    """Resolve THE directory the engine will import forward-valuation from, per the canonical rule above.
    Returns an absolute path, or (halt=False) None when unresolved. NEVER returns an ambient-workspace default."""
    fv = os.environ.get('RL_FV')
    if fv:
        return os.path.abspath(fv)
    cand = checkout_fv_dir(root)
    if os.path.isdir(cand):
        return os.path.abspath(cand)
    msg = ("fv_provenance: cannot resolve forward_valuation source — RL_FV is unset and no checked-out "
           "engine/forward_valuation was found via RL_REPO / CLAUDE_PROJECT_DIR. Refusing to fall back to an "
           "ambient workspace copy (fail-closed provenance). Set RL_FV to the checked-out "
           "engine/forward_valuation, or set RL_REPO to the checkout root.")
    if halt:
        raise SystemExit(msg)
    return None


def fv_source_files(fv_dir):
    """The COMPLETE imported forward-valuation Python source set: every *.py in the dir, sorted by relpath."""
    if not fv_dir or not os.path.isdir(fv_dir):
        return []
    return sorted(f for f in os.listdir(fv_dir) if f.endswith('.py'))


def _sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def fv_identity(fv_dir):
    """Canonical tree hash over sorted relative paths + exact file-content sha256 for every *.py.
    Deterministic and independent of filesystem ordering / mtime. Returns a full 64-char sha256, or None
    if the directory is absent/empty."""
    files = fv_source_files(fv_dir)
    if not files:
        return None
    h = hashlib.sha256()
    for rel in files:
        h.update(rel.encode('utf-8'))
        h.update(b'\0')
        h.update(_sha256_file(os.path.join(fv_dir, rel)).encode('ascii'))
        h.update(b'\n')
    return h.hexdigest()


def fv_source_hashes(fv_dir):
    """A {relpath: sha256} map of the complete imported source set (for provenance reports / triage)."""
    return {rel: _sha256_file(os.path.join(fv_dir, rel)) for rel in fv_source_files(fv_dir)}


def expected_identity(root=None):
    """The pinned forward-valuation identity from data/expected_boot.json ('fv'), or None if unpinned."""
    try:
        with open(os.path.join(repo_root(root), 'data', 'expected_boot.json')) as f:
            return json.load(f).get('fv')
    except Exception:
        return None


def _file_md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 16), b''):
            h.update(chunk)
    return h.hexdigest()


def resolve_rl_model_path():
    """The rl_model.py source file the engine WILL import, resolved through the configured environment only
    (an already-loaded rl_model, else the checkout's engine/rl_after). NEVER a hardcoded /home/claude path.
    Returns an absolute path or None. Used for provenance reporting, not for import (the engine imports
    rl_model through the ordinary configured PYTHONPATH)."""
    m = sys.modules.get('rl_model')
    if m is not None and getattr(m, '__file__', None):
        return os.path.abspath(m.__file__)
    try:
        import importlib.util as _ilu
        spec = _ilu.find_spec('rl_model')
        if spec is not None and spec.origin and spec.origin != 'built-in':
            return os.path.abspath(spec.origin)
    except Exception:
        pass
    base = os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR')
    if base:
        cand = os.path.join(base, 'engine', 'rl_after', 'rl_model.py')
        if os.path.exists(cand):
            return os.path.abspath(cand)
    return None


def provenance_report(root=None):
    """Assemble the pre-export provenance record (GREEN 2): RL_FV, resolved dir, full FV source-set identity,
    distribution_pricing.py path+hash, rl_model path+hash, config_manifest path+identity. Pure observation —
    it enforces nothing; boot_guard / the canonical entry point does the fail-closed assertion."""
    root = repo_root(root)
    resolved = resolve_fv(root, halt=False)
    dp_path = os.path.join(resolved, 'distribution_pricing.py') if resolved else None
    rl_path = resolve_rl_model_path()
    rec = {
        'RL_FV_env': os.environ.get('RL_FV'),
        'resolved_fv_dir': resolved,
        'fv_identity': fv_identity(resolved) if resolved else None,
        'fv_identity_expected': expected_identity(root),
        'fv_source_hashes': fv_source_hashes(resolved) if resolved else {},
        'distribution_pricing_path': dp_path,
        'distribution_pricing_md5': _file_md5(dp_path) if dp_path and os.path.exists(dp_path) else None,
        'rl_model_path': rl_path,
        'rl_model_md5': _file_md5(rl_path) if rl_path and os.path.exists(rl_path) else None,
    }
    try:
        import config_manifest as _cm
        rec['config_manifest_path'] = _cm.manifest_path(root)
        rec['config_manifest_identity'] = _cm.manifest_hash(root)
    except Exception as e:
        rec['config_manifest_path'] = None
        rec['config_manifest_identity'] = None
        rec['config_manifest_error'] = repr(e)
    return rec


if __name__ == '__main__':
    _root = repo_root()
    if len(sys.argv) > 1 and sys.argv[1] == 'identity':
        _dir = sys.argv[2] if len(sys.argv) > 2 else checkout_fv_dir(_root)
        print(fv_identity(_dir))
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'report':
        print(json.dumps(provenance_report(_root), indent=2, sort_keys=True))
        sys.exit(0)
    _dir = checkout_fv_dir(_root)
    print("forward_valuation dir : %s" % _dir)
    print("source set (%d files) : %s" % (len(fv_source_files(_dir)), ', '.join(fv_source_files(_dir))))
    print("fv identity           : %s" % fv_identity(_dir))
    print("pinned identity       : %s" % expected_identity(_root))
