#!/usr/bin/env python3
"""MODEL CONFIG MANIFEST — the durable half of R3 (gate-integrity repair, 2026-07-09).

WHY THIS EXISTS
  The R3 near-miss (a fitted PVC curve riding silently into the baked board) was a CONFIG-vs-RULING
  drift: a model-semantics env var changed the shipped board and no single place pinned the model
  configuration, and no produced artifact carried a config identity. RULING-CONFIG is the stopgap for
  that ONE lever; this is the general, durable fix. ONE versioned file (data/model_config.json)
  enumerates every model-semantics RL_*/PAR_* variable with its canonical value. In BAKE/GATE mode the
  ambient model environment is CLEARED, unknown/divergent overrides are REJECTED (halt-not-warn), the
  manifest is loaded explicitly, and its canonical hash is stamped into produced identity records
  (boot identity, book meta, gate report). Consumers can then verify code + store + CONFIG together.

WHAT IT IS NOT
  It does NO engine math and reimplements NO guard logic. It reads the manifest + the live env only.
  Ordinary dev-shell experimentation (no RL_CONFIG_MODE) is a NO-OP here — `RL_YOUNG=0 python3 ...`
  still works for exploration OUTSIDE bake/gate mode. The existing RL_PVCFIT export bake-guard and the
  CI RULING-CONFIG assertion remain on top, unchanged.

USAGE
  Python (bake producer / gate runner), BEFORE the engine reads the env / loads _merged_recover:
      import config_manifest
      cfg = config_manifest.enforce('bake')   # or 'gate'; None/omit -> read RL_CONFIG_MODE; unset -> no-op
      # cfg is None (dev-shell) or the canonical config hash string (bake/gate)
  Query only (stamp a report without enforcing):
      h = config_manifest.manifest_hash()
"""
import os, sys, json, hashlib, re

_PREFIX = re.compile(r'^(RL_|PAR_)')

# Infrastructure / path / display / mode plumbing — NOT model semantics. Allowed ambient in bake/gate
# mode and never part of the value hash. (CLAUDE_PROJECT_DIR / PYTHONHASHSEED are not RL_/PAR_-prefixed,
# so they are never scanned; listed in the manifest doc for completeness.)
# NOTE (S1 fix, register item 24, 2026-07-13): RL_NO_OWNER_OVERRIDES is DELIBERATELY NOT here. In
# gate/bake mode it must be REJECTED (halt), never silently allowed — the reject-scan below treats it as an
# unknown model override, so a gate/bake cannot disable the standing owner rulings. Dev-shell (no
# RL_CONFIG_MODE) is unaffected: the exclusion test still sets it to build the OFF board for comparison.
INFRA_ALLOW = {'RL_REPO', 'RL_APP_DATA', 'RL_FV',
               'RL_ALLOW_PVCFIT_BOARD', 'RL_CONFIG_MODE', 'RL_VENV'}


def repo_root():
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.dirname(os.path.abspath(__file__))):
        if cand and os.path.exists(os.path.join(cand, 'data', 'model_config.json')):
            return os.path.abspath(cand)
    return os.path.dirname(os.path.abspath(__file__))


def manifest_path(root=None):
    return os.path.join(root or repo_root(), 'data', 'model_config.json')


def load(root=None):
    with open(manifest_path(root)) as f:
        return json.load(f)


def canonical_hash(vars_dict):
    """Deterministic sha256 over the sorted NAME=VALUE lines — independent of JSON key order / whitespace."""
    payload = '\n'.join('%s=%s' % (k, vars_dict[k]) for k in sorted(vars_dict))
    return hashlib.sha256(payload.encode()).hexdigest()


def manifest_hash(root=None):
    return canonical_hash(load(root)['vars'])


def _boot_config_pin(root):
    """The config hash pinned into boot identity (data/expected_boot.json 'config'), if present."""
    try:
        with open(os.path.join(root, 'data', 'expected_boot.json')) as f:
            return json.load(f).get('config')
    except Exception:
        return None


def enforce(mode=None, halt=True):
    """In BAKE/GATE mode: clear ambient model env, reject unknown/divergent overrides, load the manifest,
    verify the manifest hash against the pinned boot identity, and return the canonical config hash.
    Outside bake/gate mode (no RL_CONFIG_MODE and no explicit mode) this is a NO-OP returning None."""
    mode = mode or os.environ.get('RL_CONFIG_MODE')
    if mode not in ('bake', 'gate'):
        return None
    root = repo_root()
    man = load(root)
    cvars = man['vars']
    chash = canonical_hash(cvars)

    # (1) reject scan — every ambient RL_/PAR_ var must be a known manifest var at its canonical value,
    #     or an explicitly-allowed infrastructure var. Anything else halts (the config-drift hole).
    rejects = []
    for k, v in list(os.environ.items()):
        if not _PREFIX.match(k) or k in INFRA_ALLOW:
            continue
        if k not in cvars:
            rejects.append("UNKNOWN model override %s=%r is not in the manifest (data/model_config.json)" % (k, v))
        elif v != cvars[k]:
            rejects.append("DIVERGENT model override %s=%r != manifest %r" % (k, v, cvars[k]))

    # (2) checkout integrity — the manifest hash must equal the pinned boot identity, if stamped.
    pin = _boot_config_pin(root)
    if pin is not None and pin != chash:
        rejects.append("manifest config hash %s != pinned boot config %s (data/expected_boot.json 'config') "
                       "— manifest/pin out of sync" % (chash[:12], str(pin)[:12]))

    if rejects:
        _hdr = "\n============ CONFIG MANIFEST (%s mode) REJECTED — BUILD HALTED ============\n" % mode
        msg = (_hdr + "  - " + "\n  - ".join(rejects) +
               "\n  Bake/gate mode pins the model configuration to data/model_config.json. Unset the "
               "override(s) above (dev-shell experimentation runs OUTSIDE bake/gate mode), or amend the "
               "manifest at a bake in the same commit that re-stamps config_sha256 + expected_boot.json.\n"
               "==========================================================================")
        if halt:
            raise SystemExit(msg)
        raise AssertionError(msg)

    # (3) clear ambient model vars, then load the manifest authoritatively (byte-identical to defaults).
    for k in list(os.environ):
        if _PREFIX.match(k) and k not in INFRA_ALLOW and k in cvars:
            os.environ.pop(k, None)
    for k, v in cvars.items():
        os.environ[k] = v

    print("config manifest (%s mode) LOADED  hash %s  (%d model vars pinned; ambient cleared)"
          % (mode, chash[:12], len(cvars)))
    return chash


if __name__ == '__main__':
    _root = repo_root()
    _man = load(_root)
    _h = canonical_hash(_man['vars'])
    if len(sys.argv) > 1 and sys.argv[1] == 'hash':
        print(_h); sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        # assert the manifest hash matches the pin + the stored config_sha256, non-zero on mismatch.
        _fail = []
        _pin = _boot_config_pin(_root)
        if _pin is not None and _pin != _h:
            _fail.append("boot identity config %s != manifest hash %s" % (str(_pin)[:12], _h[:12]))
        _stored = _man.get('config_sha256')
        if _stored not in (None, 'PLACEHOLDER_STAMPED_BELOW') and _stored != _h:
            _fail.append("model_config.json config_sha256 %s != recomputed %s" % (str(_stored)[:12], _h[:12]))
        print("CONFIG-MANIFEST CHECK: " + ("FAILED\n  - " + "\n  - ".join(_fail) if _fail else
              "PASS (hash %s; %d vars; pin+stored consistent)" % (_h[:12], len(_man['vars']))))
        sys.exit(1 if _fail else 0)
    print("config manifest hash: %s  (%d model vars)" % (_h, len(_man['vars'])))
    print("manifest: %s" % manifest_path(_root))
