#!/usr/bin/env python3
"""Red/green-path proof for gate-integrity (e): the config manifest.

Runs config_manifest.enforce in a CLEAN subprocess env for each case and asserts the outcome:
  GREEN  official env (all model vars at manifest values)           -> loads, exit 0, prints the hash
  RED-1  a DIVERGENT model override (RL_YOUNG=0)                     -> HALT (exit 1), 'DIVERGENT' in stderr
  RED-2  an UNKNOWN model override (RL_BOGUS=1)                      -> HALT (exit 1), 'UNKNOWN' in stderr
  RED-3  RL_PVCFIT=1 (the exact R3 drift this exists to stop)        -> HALT (exit 1), 'DIVERGENT'/'RL_PVCFIT'
  GREEN  dev-shell (no RL_CONFIG_MODE) with RL_YOUNG=0 set           -> NO-OP (exit 0): experimentation is free
Run:  python3 session_2026-07-09/gate_integrity/test_config_manifest.py   (from repo root)
"""
import os, sys, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SNIPPET = "import config_manifest as c; h=c.enforce(); print('ENFORCE_RETURN=%r' % (h,))"


def run(extra_env, mode=None):
    env = {'PATH': os.environ.get('PATH', ''), 'RL_REPO': ROOT}
    if mode:
        env['RL_CONFIG_MODE'] = mode
    env.update(extra_env)
    p = subprocess.run([sys.executable, '-c', SNIPPET], cwd=ROOT, env=env,
                       capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr)


OFFICIAL = {'RL_GAMMA': '0.85', 'RL_PICK1': '3000', 'RL_RUCK_TAX': '0.25',
            'RL_RECENCY_DECAY': '0.72', 'RL_PRIOR_TREES': '400', 'PAR_RAMPS': '22',
            'PYTHONHASHSEED': '0'}

fails = []


def expect(label, cond, detail):
    print(("  PASS " if cond else "  FAIL ") + label + ("" if cond else "  <-- " + detail))
    if not cond:
        fails.append(label)


print("=== gate-integrity (e) config-manifest red/green-path proof ===")

rc, out = run(OFFICIAL, mode='bake')
expect("GREEN bake official env loads (exit 0)", rc == 0 and 'LOADED' in out, "rc=%d" % rc)

rc, out = run(dict(OFFICIAL, RL_YOUNG='0'), mode='bake')
expect("RED-1 divergent RL_YOUNG=0 halts (exit 1)", rc == 1 and 'DIVERGENT' in out, "rc=%d" % rc)

rc, out = run(dict(OFFICIAL, RL_BOGUS='1'), mode='bake')
expect("RED-2 unknown RL_BOGUS=1 halts (exit 1)", rc == 1 and 'UNKNOWN' in out, "rc=%d" % rc)

rc, out = run(dict(OFFICIAL, RL_PVCFIT='1'), mode='bake')
expect("RED-3 R3 drift RL_PVCFIT=1 halts (exit 1)", rc == 1 and 'RL_PVCFIT' in out, "rc=%d" % rc)

rc, out = run(dict(OFFICIAL, RL_YOUNG='0'), mode=None)
expect("GREEN dev-shell no-op with RL_YOUNG=0 (exit 0)", rc == 0 and 'ENFORCE_RETURN=None' in out, "rc=%d" % rc)

print("\nRESULT:", "ALL PASS" if not fails else "FAILED: " + ", ".join(fails))
sys.exit(1 if fails else 0)
