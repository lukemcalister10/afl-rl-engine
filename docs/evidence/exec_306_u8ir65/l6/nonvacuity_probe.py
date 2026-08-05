#!/usr/bin/env python3
"""#306 L6 PASS 2 — NON-VACUITY PROBE for the re-pinned harness's identity assert.

The ruling that authorises the re-pin (#306 comment 5186041140, RULING 1) requires the assert to be
proven able to FAIL and able to PASS, before the pin moves and again after. A guard that has never
been seen to fail is hazard class 5 wearing a safety costume, and this project has that on record.

This probe loads a named matrix through `harness_pvc_REPINNED.load_matrix` and reports which way the
identity assert went, with the offending values printed. It does not interpret; it reports.

  python3 nonvacuity_probe.py <REPO> <matrix.json> [<matrix.json> ...]

Imported BY PATH, never by bare module name, and `__pycache__` is cleared first — `pooled_numeraire`
imports its harness by bare name, so which copy loads is otherwise invisible (practice 5).
"""
import os, sys, json, shutil, hashlib, importlib.util

REPO = sys.argv[1].rstrip('/')
MATS = sys.argv[2:]
HP = os.path.join(REPO, 'session_2026-07-30/item279_step4/scripts/harness_pvc_REPINNED.py')

for d in (os.path.join(os.path.dirname(HP), '__pycache__'),):
    if os.path.isdir(d):
        shutil.rmtree(d)

spec = importlib.util.spec_from_file_location('harness_pvc_REPINNED_probe', HP)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

print('HARNESS   %s   md5 %s' % (os.path.basename(HP), hashlib.md5(open(HP, 'rb').read()).hexdigest()[:8]))
print('PINS      EXPECT_STORE %s | EXPECT_V0SURF %s | EXPECT_N %d\n'
      % (h.EXPECT_STORE, h.EXPECT_V0SURF, h.EXPECT_N))

rc = 0
for m in MATS:
    p = m if os.path.isabs(m) else os.path.join(REPO, m)
    sig = json.load(open(p))['meta']['v0surf_sig'][:12]
    try:
        meta, ND = h.load_matrix(p)
        print('LOADS     %-46s sig %s  ND=%d' % (os.path.basename(p), sig, len(ND)))
    except AssertionError as e:
        print('HALTS     %-46s sig %s  -> %s' % (os.path.basename(p), sig, e))
        rc = 1
print('\n(HALTS is the failing direction and is a PASS of the non-vacuity requirement when it is the'
      '\n matrix that should be rejected. Read each line against what it was chosen to demonstrate.)')
sys.exit(0)
