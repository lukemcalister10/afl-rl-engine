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
