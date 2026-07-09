#!/usr/bin/env python3
"""RULING-CONFIG ASSERTION — config-vs-rulings gate (DECISIONS §16, promoted to CI 2026-07-09).

WHY THIS EXISTS
  The R3 near-miss (v2.6 bake) was NOT a guard failure — every data guard was self-consistent. It was a
  CONFIG-vs-RULING drift: `RL_PVCFIT` code-defaulted '1', so the held-out W4 PVC fit silently rode into
  board bcd81363, and no gate asserted the SHIPPED config against the recorded owner ruling. DECISIONS
  §16 made "audit directives assert shipped-config vs recorded rulings" standing doctrine. This script is
  that assertion, made mechanical and wired into CI. It does NO engine math and reimplements NO guard
  logic — it reads the shipped source and the live environment and asserts they match the owner rulings:
      (R3-a)  the engine default for RL_PVCFIT resolves to 0 (compliant-by-default), and
      (R3-b)  the export R3 BAKE GUARD is present and active (a fitted board is unbakeable-wrong).
      (R-i-a) the engine default for RL_LTI_CLOCK resolves to 'advance' (owner ruling R-i, 2026-07-10,
              DECISIONS v90 §36: the L1c fade-clock ADVANCES during injury), and
      (R-i-b) the live env does not silently PAUSE the clock (unset or 'advance'), and
      (R-i-c) the config manifest (data/model_config.json) pins RL_LTI_CLOCK='advance' so it rides
              artifact identity — i.e. a bake/gate run with the clock PAUSED fails loudly here.
  FAILS (non-zero), never warns.

USAGE
  python3 ruling_config_check.py            # asserts against the checked-out repo source + this env
  RL_REPO=/path python3 ruling_config_check.py
"""
import os, re, sys, json

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

# ============================ R-i: RL_LTI_CLOCK = advance ============================
# Owner ruling R-i (2026-07-10, DECISIONS v90 §36): the L1c fade-clock ADVANCES during injury. Same
# assertion family as R3 — the SHIPPED config must match the recorded ruling. A bake/gate run with the
# clock PAUSED must FAIL loudly (here, plus the manifest reject-scan in config_manifest.enforce).
print("--- R-i (RL_LTI_CLOCK=advance by default + manifest-pinned) ---")

# (R-i-a) ENGINE DEFAULT: RL_LTI_CLOCK resolves to 'advance' when unset. The engine reads it as
#         `_LTI_CLOCK = os.environ.get('RL_LTI_CLOCK', <default>)` — the DEFAULT string must be 'advance'.
mc = re.search(r"_LTI_CLOCK\s*=\s*os\.environ\.get\(\s*['\"]RL_LTI_CLOCK['\"]\s*,\s*['\"]([^'\"]*)['\"]\s*\)", eng)
check(mc is not None, "engine reads RL_LTI_CLOCK via os.environ.get('RL_LTI_CLOCK', <default>) (R-i form)")
check(bool(mc) and mc.group(1) == 'advance',
      "engine RL_LTI_CLOCK default string == 'advance' (owner-ruled R-i); got %r" % (mc.group(1) if mc else None))

# (R-i-b, live) the CI/bake ENVIRONMENT must not silently PAUSE the clock. Unset or 'advance' both resolve
#              to advance; an explicit 'pause' (the retired provisional) fails the gate loudly.
_clk = os.environ.get('RL_LTI_CLOCK')
check(_clk in (None, 'advance'),
      "live env RL_LTI_CLOCK is unset or 'advance' (bake env does not pause the L1c clock); got %r" % _clk)

# (R-i-c) MANIFEST PIN: data/model_config.json vars carry RL_LTI_CLOCK='advance', so it rides artifact
#         identity (config_sha256) and bake/gate mode loads it authoritatively (config_manifest.enforce
#         also rejects a divergent ambient 'pause'). A manifest edited back to pause fails here.
_manp = os.path.join(ROOT, 'data', 'model_config.json')
_mv = None
if os.path.exists(_manp):
    try: _mv = json.load(open(_manp)).get('vars', {}).get('RL_LTI_CLOCK')
    except Exception: _mv = None
check(_mv == 'advance',
      "config manifest (data/model_config.json) pins RL_LTI_CLOCK='advance' (rides artifact identity); got %r" % _mv)

print("\n" + ("RULING-CONFIG FAILED: %d check(s)\n  - " % len(FAIL) + "\n  - ".join(FAIL) if FAIL else
      "RULING-CONFIG PASSED: RL_PVCFIT=0 (engine + env) + R3 export bake-guard active; "
      "RL_LTI_CLOCK=advance (engine default + env + manifest pin, owner ruling R-i)."))
sys.exit(1 if FAIL else 0)
