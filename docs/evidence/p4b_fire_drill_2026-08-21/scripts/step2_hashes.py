#!/usr/bin/env python3
"""P4b FIRE DRILL — step 2: does every pinned identity in the RESTORED tree hash to what
that tag's OWN expected_boot / release_contract declare?  Bytes, not recipes."""
import os, sys, json, hashlib, time

ROOT = sys.argv[1]
t0 = time.time()

def md5(p):
    if not os.path.exists(p):
        return None
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()

boot = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
contract = json.load(open(os.path.join(ROOT, 'data', 'release_contract.json')))

# md5-pinned file artifacts, path per the tag's own boot_guard / verify_restore
FILEPINS = [
    ('board',        'data/rl_build/rl_app_data.json'),
    ('store',        'engine/rl_after/rl_model_data.json'),
    ('engine_head',  'engine/rl_after/_merged_recover.py'),
    ('rl_model',     'engine/rl_after/rl_model.py'),
    ('band',         'data/cm_400.pkl'),
    ('q97m',         'data/q97m.pkl'),
    ('v0surf',       'data/v0surf.pkl'),
    ('peak_model',   'engine/rl_after/peak_model_v4.pkl'),
    ('pvc_snapshot', 'engine/rl_after/pvc_snapshot.json'),
    ('bust_prior',   'engine/rl_after/bust_prior_table.json'),
    ('register',     'LTI_REGISTER.md'),
]

rows, fails = [], []
print('=' * 100)
print('A. PINNED FILE ARTIFACTS — restored bytes vs the tag\'s own data/expected_boot.json')
print('=' * 100)
print('%-14s %-42s %-34s %-34s %s' % ('pin', 'path', 'pinned', 'restored md5', 'verdict'))
for field, rel in FILEPINS:
    pin = boot.get(field)
    got = md5(os.path.join(ROOT, rel))
    if pin is None:
        verdict = 'NO PIN'
    elif got is None:
        verdict = 'FAIL (file ABSENT)'
    else:
        verdict = 'MATCH' if got[:len(pin)] == pin else 'FAIL'
    if verdict.startswith('FAIL'):
        fails.append('%s: pinned %s got %s' % (field, pin, got))
    rows.append((field, rel, pin, got, verdict))
    print('%-14s %-42s %-34s %-34s %s' % (field, rel, pin, got, verdict))

# fv — sha256 over the sorted forward_valuation source set (the tag's own fv_provenance)
print()
print('=' * 100)
print('B. DERIVED / COMPUTED PINS — recomputed by the TAG\'S OWN code in the restored tree')
print('=' * 100)
sys.path.insert(0, ROOT)
os.environ['RL_REPO'] = ROOT
os.environ['CLAUDE_PROJECT_DIR'] = ROOT
try:
    import fv_provenance as _fv
    ck = _fv.checkout_fv_dir(ROOT)
    fvid = _fv.fv_identity(ck)
except Exception as e:
    fvid, ck = 'ERROR: %r' % (e,), '?'
pin = boot.get('fv')
v = 'MATCH' if fvid == pin else 'FAIL'
if v == 'FAIL':
    fails.append('fv: pinned %s got %s' % (pin, fvid))
print('%-14s %-42s %s' % ('fv', 'engine/forward_valuation (sha256 set)', v))
print('%-14s pinned   %s' % ('', pin))
print('%-14s restored %s' % ('', fvid))

try:
    import config_manifest as _cm
    cfg = _cm.manifest_hash(ROOT)
except Exception as e:
    cfg = 'ERROR: %r' % (e,)
pin = boot.get('config')
v = 'MATCH' if cfg == pin else 'FAIL'
if v == 'FAIL':
    fails.append('config: pinned %s got %s' % (pin, cfg))
print('%-14s %-42s %s' % ('config', 'config_manifest.manifest_hash()', v))
print('%-14s pinned   %s' % ('', pin))
print('%-14s restored %s' % ('', cfg))

# board srcmd5 sidecar
src = os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json.srcmd5')
if os.path.exists(src):
    print('%-14s %-42s %s' % ('board.srcmd5', 'data/rl_build/..srcmd5 (content)',
                              open(src).read().strip()[:80]))

# balanced_board_md5 has no in-tree artifact (STATE.md records this)
print('%-14s %-42s %s' % ('balanced_board', '(no in-tree artifact)', boot.get('balanced_board_md5')))

print()
print('=' * 100)
print('C. THE TAG\'S OWN release_contract.json identities vs the SAME tag\'s expected_boot')
print('=' * 100)
print('%-20s %-34s %-34s %s' % ('field', 'contract says', 'expected_boot says', 'verdict'))
cfails = []
for field, want in sorted((contract.get('identities') or {}).items()):
    have = boot.get(field)
    v = 'AGREE' if str(have) == str(want) else 'DIFFER'
    if v == 'DIFFER':
        cfails.append(field)
    print('%-20s %-34s %-34s %s' % (field, str(want)[:32], str(have)[:32], v))
v = 'AGREE' if contract.get('config_sha256') == boot.get('config') else 'DIFFER'
if v == 'DIFFER':
    cfails.append('config_sha256')
print('%-20s %-34s %-34s %s' % ('config_sha256', str(contract.get('config_sha256'))[:32],
                                str(boot.get('config'))[:32], v))
print('%-20s %-34s %-34s %s' % ('as_of_round', contract.get('as_of_round'), boot.get('as_of_round'),
                                'AGREE' if contract.get('as_of_round') == boot.get('as_of_round') else 'DIFFER'))
print('held_candidates declared in the contract: %r' % (contract.get('held_candidates'),))
print('release_version: %r' % contract.get('release_version'))

# contract self-seal
sys.path.insert(0, ROOT)
try:
    import release_contract as _rc
    stored = contract.get('contract_sha256')
    recomputed = _rc.contract_hash(contract)
    print('contract_sha256 stored     %s' % stored)
    print('contract_sha256 recomputed %s  -> %s' % (recomputed, 'SEAL INTACT' if stored == recomputed else 'SEAL BROKEN'))
except Exception as e:
    print('contract seal recompute ERROR: %r' % (e,))

print()
print('=' * 100)
print('BYTE-RESTORE VERDICT (expected_boot leg): %s' % ('PASS — every pinned identity matches' if not fails else 'FAIL'))
for f in fails:
    print('  - %s' % f)
print('CONTRACT-COHERENCE LEG: %s' % ('coherent' if not cfails else 'INCOHERENT at the tag — fields: %s' % ', '.join(cfails)))
print('STEP2_HASH_SECONDS=%.3f' % (time.time() - t0))
sys.exit(1 if fails else 0)
