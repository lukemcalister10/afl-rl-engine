#!/usr/bin/env python3
"""MEASURE the lineage identities for the back-rows repair transition. Nothing is typed.

SOURCE  = the committed tree at 15729e7 — the PREREG commit, immediately before any Act A edit.
          Every identity is re-hashed out of git (`git show <rev>:<path>`), and each is cross-checked
          against THAT TREE'S OWN data/expected_boot.json.
DEST    = the live tree, re-hashed the same way; config and fv are additionally RE-MEASURED by
          config_manifest.manifest_hash / fv_provenance.fv_identity rather than read from the manifest.

Writes lineage_measured.json beside this script.
"""
import hashlib, importlib.util, json, os, subprocess, sys

ROOT = '/home/user/afl-rl-engine'
SRC_REV = '15729e7'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

FILES = {'board': 'data/rl_build/rl_app_data.json',
         'store': 'engine/rl_after/rl_model_data.json',
         'engine_head': 'engine/rl_after/_merged_recover.py',
         'rl_model': 'engine/rl_after/rl_model.py',
         'register': 'LTI_REGISTER.md',
         'v0surf': 'data/v0surf.pkl'}


def git_md5(rev, path):
    b = subprocess.run(['git', 'show', '%s:%s' % (rev, path)], cwd=ROOT,
                       capture_output=True).stdout
    if not b:
        raise SystemExit('HALT: %s:%s is empty or missing' % (rev, path))
    return hashlib.md5(b).hexdigest()


def git_json(rev, path):
    return json.loads(subprocess.run(['git', 'show', '%s:%s' % (rev, path)], cwd=ROOT,
                                     capture_output=True).stdout)


def live_md5(path):
    return hashlib.md5(open(os.path.join(ROOT, path), 'rb').read()).hexdigest()


# ---- SOURCE ---------------------------------------------------------------------------------------
sboot = git_json(SRC_REV, 'data/expected_boot.json')
ssib = git_json(SRC_REV, 'engine/rl_after/ingestion/sibling_repin_state.json')
source = {k: git_md5(SRC_REV, p) for k, p in FILES.items()}
source['config'] = sboot['config']
source['fv'] = sboot['fv']
source['balanced_board_md5'] = ssib['balanced_board_md5']
source['as_of_round'] = sboot['as_of_round']
source['release_version'] = sboot['release_version']
for k in ('board', 'store', 'engine_head', 'rl_model', 'register', 'v0surf', 'balanced_board_md5'):
    if sboot.get(k) != source[k]:
        raise SystemExit('HALT: source %s re-hashed %s but %s expected_boot says %s'
                         % (k, source[k], SRC_REV, sboot.get(k)))
print('SOURCE @ %s: every re-hashed identity agrees with that tree\'s own expected_boot.' % SRC_REV)

# ---- DESTINATION ----------------------------------------------------------------------------------
dboot = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
dsib = json.load(open(os.path.join(ROOT, 'engine', 'rl_after', 'ingestion', 'sibling_repin_state.json')))
dest = {k: live_md5(p) for k, p in FILES.items()}
import config_manifest as CM, fv_provenance as FV
dest['config'] = CM.manifest_hash(ROOT)
dest['fv'] = FV.fv_identity(FV.checkout_fv_dir(ROOT))
dest['balanced_board_md5'] = dsib['balanced_board_md5']
dest['as_of_round'] = dboot['as_of_round']
dest['release_version'] = dboot['release_version']
for k in ('board', 'store', 'engine_head', 'rl_model', 'register', 'v0surf', 'balanced_board_md5',
          'config', 'fv'):
    if dboot.get(k) != dest[k]:
        raise SystemExit('HALT: destination %s measured %s but the landed expected_boot says %s'
                         % (k, dest[k], dboot.get(k)))
print('DESTINATION (live): every measured identity agrees with the landed expected_boot; config and '
      'fv were RE-MEASURED by their own definitions, not read.')

KEYS = ('release_version', 'board', 'store', 'rl_model', 'engine_head', 'fv', 'config', 'register',
        'balanced_board_md5', 'v0surf', 'as_of_round')
moved = [k for k in KEYS if source[k] != dest[k]]
unchanged = [k for k in KEYS if source[k] == dest[k]]
out = {'source': {k: source[k] for k in KEYS}, 'destination': {k: dest[k] for k in KEYS},
       'moved': moved, 'unchanged': unchanged}
open(os.path.join(HERE, 'lineage_measured.json'), 'w').write(json.dumps(out, indent=1, sort_keys=True))
print()
print('MOVED by this transition (%d of %d): %s' % (len(moved), len(KEYS), moved))
for k in moved:
    print('   %-20s %s -> %s' % (k, source[k], dest[k]))
print('UNCHANGED (%d): %s' % (len(unchanged), unchanged))
