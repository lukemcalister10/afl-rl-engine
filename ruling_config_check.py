#!/usr/bin/env python3
"""RULING-CONFIG ASSERTION — config-vs-rulings gate (DECISIONS §16, promoted to CI 2026-07-09).

WHY THIS EXISTS
  The R3 near-miss (v2.6 bake) was NOT a guard failure — every data guard was self-consistent. It was a
  CONFIG-vs-RULING drift: `RL_PVCFIT` code-defaulted '1', so the held-out W4 PVC fit silently rode into
  board bcd81363, and no gate asserted the SHIPPED config against the recorded owner ruling. DECISIONS
  §16 made "audit directives assert shipped-config vs recorded rulings" standing doctrine. This script is
  that assertion, made mechanical and wired into CI. It does NO engine math and reimplements NO guard
  logic — it reads the shipped source and the live environment and asserts they match ruling R3:
      (R3-a) the engine default for RL_PVCFIT resolves to 0 (compliant-by-default), and
      (R3-b) the export R3 BAKE GUARD is present and active (a fitted board is unbakeable-wrong).
  FAILS (non-zero), never warns.

USAGE
  python3 ruling_config_check.py            # asserts against the checked-out repo source + this env
  RL_REPO=/path python3 ruling_config_check.py
"""
import os, re, sys

def repo_root():
    for cand in (os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.dirname(os.path.abspath(__file__))):
        if cand and os.path.exists(os.path.join(cand, 'engine', 'rl_after', '_merged_recover.py')):
            return os.path.abspath(cand)
    return os.path.dirname(os.path.abspath(__file__))

ROOT = repo_root()
ENGINE = os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py')
EXPORT = os.path.join(ROOT, 'engine', 'rl_after', 'rl_export.py')

FAIL = []
def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond: FAIL.append(msg)

print("=== RULING-CONFIG ASSERTION (R3: RL_PVCFIT=0 by default + export bake-guard active) ===")
print("    repo = %s" % ROOT)

eng = open(ENGINE).read() if os.path.exists(ENGINE) else ''
exp = open(EXPORT).read() if os.path.exists(EXPORT) else ''
check(bool(eng), "engine source present (%s)" % ENGINE)
check(bool(exp), "export source present (%s)" % EXPORT)

# (R3-a) ENGINE DEFAULT: RL_PVCFIT resolves to 0 when unset. The engine reads it as
#        `_W4PVC = os.environ.get('RL_PVCFIT','0') != '0'` — the DEFAULT string must be '0'.
m = re.search(r"_W4PVC\s*=\s*os\.environ\.get\(\s*['\"]RL_PVCFIT['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*\)\s*!=\s*['\"]0['\"]", eng)
check(m is not None, "engine reads RL_PVCFIT via os.environ.get('RL_PVCFIT', <default>) != '0' (R3 form)")
check(bool(m) and m.group(1) == '0',
      "engine RL_PVCFIT default string == '0' (compliant-by-default); got %r" % (m.group(1) if m else None))

# (R3-a, live) the CI/bake ENVIRONMENT must not silently turn the fit on. Unset or '0' both resolve to 0.
_envv = os.environ.get('RL_PVCFIT')
check(_envv in (None, '0'),
      "live env RL_PVCFIT is unset or '0' (bake env does not enable the held-out fit); got %r" % _envv)

# (R3-b) EXPORT BAKE GUARD present and active: rl_export refuses to write the board when the fit is on
#        unless the explicit non-bakeable escape hatch RL_ALLOW_PVCFIT_BOARD=1 is set.
has_guard_cond = re.search(
    r"if\s+_ens\.get\(\s*['\"]_W4PVC['\"]\s*\)\s+and\s+os\.environ\.get\(\s*['\"]RL_ALLOW_PVCFIT_BOARD['\"]\s*,\s*['\"]0['\"]\s*\)\s*==\s*['\"]0['\"]\s*:",
    exp)
check(has_guard_cond is not None,
      "export R3 BAKE GUARD condition present (_W4PVC on + no RL_ALLOW_PVCFIT_BOARD -> refuse)")
check(('R3 BAKE GUARD' in exp) and ('raise SystemExit' in exp),
      "export R3 BAKE GUARD raises SystemExit (halt-not-warn: a fitted board is unbakeable)")
# guard must fire BEFORE the board is written (json.dump of rl_app_data.json)
gpos = exp.find('R3 BAKE GUARD'); wpos = exp.find("json.dump(out")
check(gpos != -1 and wpos != -1 and gpos < wpos,
      "export R3 BAKE GUARD sits BEFORE json.dump(rl_app_data.json) (guards the write)")

print("\n" + ("RULING-CONFIG FAILED: %d check(s)\n  - " % len(FAIL) + "\n  - ".join(FAIL) if FAIL else
      "RULING-CONFIG PASSED: RL_PVCFIT=0 by default (engine + env) and the R3 export bake-guard is present and active."))
sys.exit(1 if FAIL else 0)
