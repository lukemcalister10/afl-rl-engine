#!/usr/bin/env python3
"""v2.9 BAKE — STEP 1 RED-PATH PROOFS. Proves the three override-restoration HALT paths are RED (each
raises / exits non-zero), then restores every file it touched. Run from the bootstrapped workspace AFTER
the full suite (it perturbs repo files in isolation). Exits non-zero if any red path fails to halt.

  (a) missing owner_overrides.json      -> owner_overrides HALT (gate/bake; never silent [])
  (b) listed override key not applied   -> post-export PRESENCE ASSERTION HALT
  (c) wrong board pin in expected_boot  -> boot_guard (Guard 5) HALT (board pin now asserted, full hash)
"""
import os, sys, json, shutil, subprocess, tempfile

ROOT = '/home/user/afl-rl-engine'
RA = '/home/claude/rl_workspace/rl_after'
OVR = os.path.join(ROOT, 'data', 'owner_overrides.json')
BOOT = os.path.join(ROOT, 'data', 'expected_boot.json')
ENV = dict(os.environ, RL_REPO=ROOT, RL_CONFIG_MODE='bake', PYTHONHASHSEED='0',
           PYTHONPATH=RA + ':/home/claude/rl_vendor')
RESULTS = []


def run_export():
    return subprocess.run([sys.executable, 'rl_export.py'], cwd=RA, env=ENV,
                          capture_output=True, text=True, timeout=600)


def backup(p):
    b = p + '.redproof.bak'; shutil.copy2(p, b); return b


def restore(p, b):
    shutil.copy2(b, p); os.remove(b)


# --- (a) MISSING owner_overrides.json -> HALT ------------------------------------------------------------
bak = backup(OVR)
try:
    os.remove(OVR)
    r = run_export()
    halted = (r.returncode != 0) and ('OWNER-OVERRIDE HALT' in (r.stdout + r.stderr))
    RESULTS.append(('(a) missing owner_overrides.json -> HALT', halted, (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout+r.stderr).strip() else ''))
finally:
    restore(OVR, bak)

# --- (b) LISTED override key not applied (key drift) -> PRESENCE ASSERTION HALT --------------------------
bak = backup(OVR)
try:
    doc = json.load(open(OVR))
    doc['overrides'].append({'player_key': 'no-such-player-xyz', 'factor': 0.5,
                             'note': 'red-path proof: unmatched key', 'provenance': 'proof'})
    json.dump(doc, open(OVR, 'w'), indent=2)
    r = run_export()
    halted = (r.returncode != 0) and ('PRESENCE ASSERTION FAILED' in (r.stdout + r.stderr))
    RESULTS.append(('(b) listed-unapplied override -> PRESENCE ASSERTION HALT', halted, [l for l in (r.stdout+r.stderr).splitlines() if 'PRESENCE' in l][:1]))
finally:
    restore(OVR, bak)

# --- (c) WRONG board pin -> boot_guard (Guard 5) HALT ----------------------------------------------------
bak = backup(BOOT)
try:
    b = json.load(open(BOOT)); b['board'] = 'deadbeef' + b['board'][8:]   # corrupt the full-hash board pin
    json.dump(b, open(BOOT, 'w'), indent=2, sort_keys=True)
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'boot_guard.py'), 'redproof',
                        os.path.join(RA, 'rl_model_data.json')], cwd=RA, env=ENV, capture_output=True, text=True)
    halted = (r.returncode != 0) and ('board' in (r.stdout + r.stderr).lower()) and ('Guard 5' in (r.stdout + r.stderr) or 'STALE-BOOT' in (r.stdout + r.stderr))
    RESULTS.append(('(c) wrong board pin -> boot_guard (Guard 5) HALT', halted, [l for l in (r.stdout+r.stderr).splitlines() if 'board' in l.lower()][:1]))
finally:
    restore(BOOT, bak)

print("\n=== RED-PATH PROOFS ===")
allok = True
for name, ok, detail in RESULTS:
    allok = allok and ok
    print(f"  {'RED (halts) OK' if ok else 'NOT RED — FAIL'} : {name}")
    if detail:
        print(f"      -> {detail}")
print("\nVERDICT:", "ALL THREE RED PATHS PROVEN" if allok else "A RED PATH DID NOT HALT")
sys.exit(0 if allok else 1)
