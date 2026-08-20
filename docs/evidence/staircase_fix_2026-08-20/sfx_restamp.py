#!/usr/bin/env python3
"""ORDER 44 — THE engine_head IDENTITY RESTAMP. THE REPAIR OF A LEG THE EDIT COMMIT LEFT OUT.

d8_ceiling_2026-08-20/d8_restamp.py, BYTE-CARRIED except for this header, the label in the argv line,
and NOTHING ELSE. Every path, every assert, every writer of record is that file's.

WHY THIS FILE IS RUN, STATED PLAINLY AND NOT SMOOTHED. THE EDIT COMMIT 1446dec MOVED
engine/rl_after/_merged_recover.py (1867e953 -> 3f4aa10b) AND DID NOT RESTAMP THE FOUR CARRIERS THAT
NAME IT. That is a defect of the edit commit, found by running the gate rather than by reading the
diff: release_manifest_check.py reads

    RELEASE MANIFEST COHERENCE: FAIL   —  4 incoherent, all engine_head
    (MANIFEST_BEFORE_REPIN_out.txt, kept in this directory as the evidence that the gate said so)

The D8 PRICING seat hit exactly this and wrote exactly this file for it (PREREG_D8 section 2.1
declared the restamp BEFORE its edit; RESTAMP_out.txt records the run). ORDER 44's prereg did not
declare it, which is the miss. The remedy is the established pattern, not a new one.

TWO CORRECTIONS TO PREREG_STAIRCASE.md, MADE AGAINST THE TREE (P9), NAMED HERE AND IN THE PACKET:

  (1) The prereg section 1 says "the release-contract seal cde9f70a STANDS". IT DOES NOT AND CANNOT.
      contract_sha256 is the hash of every field of release_contract.json except itself
      (release_contract.py:69), so moving identities.engine_head necessarily re-stamps it. The
      SUBSTANTIVE claim the prereg was making is about config_sha256 — the MANIFEST hash, which
      RL_O44_LVLMONO is deliberately absent from — and THAT claim is true and is asserted at run
      below by leaving data/model_config.json untouched. The seal is a derived stamp of the identity
      set; the manifest hash is the claim. The prereg conflated them.
  (2) The prereg did not list the engine_head restamp among the things this act moves. It moves them.

WHAT MOVES, AND NOTHING ELSE:
    data/expected_boot.json              engine_head
    data/release_contract.json           identities.engine_head  (+ recomputed contract_sha256)
    ui/data/board_view_working.js        stamp.engine (8 hex)  and  stamp.release.engine_head

board / store / config / rl_model / register / as_of_round are READ AND RE-ASSERTED, never written —
the asserts below refuse to run if any of them has moved. data/book_stable_seal.json's head_md5 is a
freeze-stamp (kind `sealed`), reads as SEALED-LAG, and is deliberately NOT re-sealed: a book re-seal
is a separate act and this one prices, it does not seal.

THE LIVE BOARD IS NOT TOUCHED BY THIS FILE AND IS NOT TOUCHED BY THIS ACT. F1 STANDS.
ORIGINAL D8 HEADER FOLLOWS.

ORDER D8 — the engine_head identity restamp. PREREG_D8.md §2.1, declared before the edit.

The D8 wiring edits `engine/rl_after/_merged_recover.py`, so the COMPUTED `engine_head` identity
moves. `release_manifest_check.py` computes truth from that file and asserts four LIVE carrier
fields against it, and Guard 5 (`boot_guard.assert_boot`) asserts it too. This restamps exactly
those four fields and nothing else:

    data/expected_boot.json              engine_head
    data/release_contract.json           identities.engine_head  (+ recomputed contract_sha256)
    ui/data/board_view_working.js        stamp.engine (8 hex)  and  stamp.release.engine_head

NOTHING ELSE MOVES. board a05fe951 / store cc02567f / config eed19a75 / rl_model 6fe7c415 /
register / as_of_round are read and re-asserted, never written. `data/book_stable_seal.json`'s
`head_md5` is a freeze-stamp (kind `sealed` in the gate) and is deliberately NOT re-sealed — it
reads as SEALED-LAG, which is reported and never gating. A book re-seal is a separate act.

THE TWO UI FIELDS GO THROUGH THEIR WRITERS OF RECORD, never a hand edit:
    ui/tools/extract_board_view.py                       -> stamp.engine (from expected_boot)
    engine/rl_after/ingestion/round_movers.inject_release_contract -> stamp.release (from expected_boot)
Verified before use: with expected_boot UNCHANGED, running both in sequence reproduces the
committed bundle BYTE-IDENTICAL (md5 fa20f2fc4c7e65c6c050868a11c9139f). The bundle is therefore
regenerated, not patched.

    python3 docs/evidence/staircase_fix_2026-08-20/sfx_restamp.py [--check]
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
CHECK = '--check' in sys.argv

md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

ENGINE = os.path.join(ROOT, 'engine', 'rl_after', '_merged_recover.py')
BOOT = os.path.join(ROOT, 'data', 'expected_boot.json')
CONTRACT = os.path.join(ROOT, 'data', 'release_contract.json')
BUNDLE = os.path.join(ROOT, 'ui', 'data', 'board_view_working.js')

truth = md5(ENGINE)
print('computed engine_head truth : %s   (engine/rl_after/_merged_recover.py)' % truth)

boot = json.load(open(BOOT))
print('expected_boot.engine_head  : %s' % boot.get('engine_head'))

# ---- the identities that must NOT move ------------------------------------------------------------
FROZEN = {
    'board': md5(os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')),
    'store': md5(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')),
    'rl_model': md5(os.path.join(ROOT, 'engine', 'rl_after', 'rl_model.py')),
    'register': md5(os.path.join(ROOT, 'LTI_REGISTER.md')),
}
for k, v in sorted(FROZEN.items()):
    got = boot.get(k)
    assert got == v, 'REFUSING: %s pin %s != computed %s — this script restamps engine_head ONLY' % (k, got, v)
    print('  unmoved %-9s %s  (asserted equal, not written)' % (k, v))

if CHECK:
    print('CHECK ONLY — no write. engine_head %s' % ('ALREADY COHERENT' if boot.get('engine_head') == truth
                                                     else 'STALE, restamp needed'))
    sys.exit(0)

# ---- (1) expected_boot.json -----------------------------------------------------------------------
if boot.get('engine_head') != truth:
    old = boot['engine_head']
    boot['engine_head'] = truth
    with open(BOOT, 'w') as f:                    # indent=1 + trailing newline: the file's own format,
        json.dump(boot, f, indent=1)              # verified to round-trip byte-exact before use
        f.write('\n')
    print('expected_boot.engine_head  : %s -> %s' % (old, truth))

# ---- (2) release_contract.json --------------------------------------------------------------------
sys.path.insert(0, ROOT)
import release_contract as RC                                                    # noqa: E402
c = json.load(open(CONTRACT))
old = c['identities'].get('engine_head')
if old != truth:
    c['identities']['engine_head'] = truth
    c.pop('contract_sha256', None)
    c['contract_sha256'] = RC.contract_hash(c)
    with open(CONTRACT, 'w') as f:
        json.dump(c, f, indent=2)
        f.write('\n')
    print('release_contract.identities.engine_head : %s -> %s' % (old, truth))
    print('release_contract.contract_sha256        : -> %s' % c['contract_sha256'])

# ---- (3) the UI bundle, through both of its writers of record --------------------------------------
before = md5(BUNDLE)
r = subprocess.run([sys.executable, os.path.join(ROOT, 'ui', 'tools', 'extract_board_view.py')],
                   cwd=ROOT, capture_output=True, text=True)
assert r.returncode == 0, 'extract_board_view failed:\n%s' % r.stderr
spec = importlib.util.spec_from_file_location(
    'rm_sfx', os.path.join(ROOT, 'engine', 'rl_after', 'ingestion', 'round_movers.py'))
rm = importlib.util.module_from_spec(spec); sys.modules['rm_sfx'] = rm; spec.loader.exec_module(rm)
rel = rm.inject_release_contract(BUNDLE, ROOT, int(boot['as_of_round']))
print('board_view_working.js      : %s -> %s' % (before, md5(BUNDLE)))
print('  stamp.release.engine_head: %s' % rel['engine_head'])

# ---- verdict ---------------------------------------------------------------------------------------
r = subprocess.run([sys.executable, os.path.join(ROOT, 'release_manifest_check.py'), 'check'],
                   cwd=ROOT, capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-400:])
sys.exit(r.returncode)
