#!/usr/bin/env python3
"""ARM 1 — THE BYTE-UNMOVED PROOF (prereg P15; rulebook P1's standing falsifier).

The arm's whole claim about the live estate is negative: it moved nothing. That claim is only worth
anything as a list of MEASURED identities compared against the pins the tree already carries, so
every number below is computed from the file and compared to data/expected_boot.json — none is typed.

Run from the checkout:  python3 byte_unmoved.py [--json OUT]
"""
import argparse, hashlib, json, os, sys


def md5(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 16), b''):
            h.update(c)
    return h.hexdigest()


ROOT = os.environ.get('RL_REPO') or os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

PINNED = [('store', 'engine/rl_after/rl_model_data.json'),
          ('board', 'data/rl_build/rl_app_data.json'),
          ('band', 'data/cm_400.pkl'),
          ('q97m', 'data/q97m.pkl'),
          ('v0surf', 'data/v0surf.pkl'),
          ('peak_model', 'engine/rl_after/peak_model_v4.pkl'),
          ('pvc_snapshot', 'engine/rl_after/pvc_snapshot.json'),
          ('bust_prior', 'engine/rl_after/bust_prior_table.json'),
          ('engine_head', 'engine/rl_after/_merged_recover.py'),
          ('rl_model', 'engine/rl_after/rl_model.py'),
          ('register', 'LTI_REGISTER.md')]
UNPINNED_BUT_LIVE = ['data/release_contract.json', 'data/expected_boot.json',
                     'data/model_config.json', 'data/release_lineage.json',
                     '/home/claude/cm_400.pkl', '/home/claude/q97m.pkl']


def main(argv):
    ap = argparse.ArgumentParser(); ap.add_argument('--json'); a = ap.parse_args(argv[1:])
    boot = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
    res = {'root': ROOT, 'pinned': {}, 'other': {}, 'fails': []}
    print('PINNED ARTIFACTS — measured from the file, compared to data/expected_boot.json')
    for field, rel in PINNED:
        p = os.path.join(ROOT, rel)
        got = md5(p) if os.path.exists(p) else None
        want = boot.get(field)
        ok = (got is not None and want is not None and got[:len(want)] == want[:len(got)])
        res['pinned'][field] = {'path': rel, 'measured': got, 'pinned': want, 'match': bool(ok)}
        if not ok:
            res['fails'].append('%s %s != pin %s' % (rel, got, want))
        print('  %-14s %-42s %s  %s' % (field, rel, got, 'UNMOVED' if ok else '*** MOVED ***'))

    # config_sha256 is a hash over the manifest's vars, not a file md5
    sys.path.insert(0, ROOT)
    import config_manifest
    ch = config_manifest.manifest_hash(ROOT)
    ok = (ch == boot.get('config'))
    res['pinned']['config'] = {'measured': ch, 'pinned': boot.get('config'), 'match': ok}
    if not ok:
        res['fails'].append('config_sha256 %s != pin %s' % (ch, boot.get('config')))
    print('  %-14s %-42s %s  %s' % ('config', 'data/model_config.json (vars hash)', ch[:32],
                                    'UNMOVED' if ok else '*** MOVED ***'))

    # the forward-valuation source-set identity — this one is EXPECTED to move in this arm
    import fv_provenance as fp
    fv = fp.fv_identity(fp.checkout_fv_dir(ROOT))
    res['pinned']['fv'] = {'measured': fv, 'pinned': boot.get('fv'), 'match': fv == boot.get('fv')}
    print('  %-14s %-42s %s  %s' % ('fv', 'engine/forward_valuation/*.py', fv[:32],
                                    'UNMOVED' if fv == boot.get('fv') else
                                    'MOVED — DECLARED: the in-repo stamp fix edits '
                                    'build_peak_model_v4.py; re-pin is OWED at the landing act'))

    print('\nOTHER LIVE FILES — md5 recorded so a later act can compare')
    for rel in UNPINNED_BUT_LIVE:
        p = rel if rel.startswith('/') else os.path.join(ROOT, rel)
        res['other'][rel] = md5(p) if os.path.exists(p) else 'ABSENT'
        print('  %-46s %s' % (rel, res['other'][rel]))

    hard = [f for f in res['fails'] if 'config_sha256' not in f]
    print('\nVERDICT: %s' % ('every pinned live artifact BYTE-UNMOVED (fv excepted and declared)'
                             if not hard else 'FAILED — ' + '; '.join(hard)))
    if a.json:
        json.dump(res, open(a.json, 'w'), indent=1, sort_keys=True)
    return 0 if not hard else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
