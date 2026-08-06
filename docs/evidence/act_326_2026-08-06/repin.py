#!/usr/bin/env python3
"""#326 second rehearsal — the identity re-pin sweep.

Every identity that MOVES with this act is re-pinned here, in one place, so the set is auditable:
  * data/expected_boot.json      rl_model, engine_head, board
  * data/release_contract.json   identities.rl_model, identities.engine_head, identities.board,
                                 then contract_sha256 recomputed by release_contract.contract_hash's recipe
  * engine/rl_after/one_source_selftest.py  _contract_md5 (the ui/release_pick_curve.json mirror moved
                                 because pool_levels is mirrored into it)
The curve PAYLOAD identity (df766dff) does NOT move and is asserted unmoved by add_pool_levels.py.

Usage:  repin.py engines            (re-pin the two engine source md5s)
        repin.py board <md5>        (re-pin the board md5 everywhere it is pinned)
        repin.py contract_md5       (re-pin the selftest's ui-contract md5 from the file on disk)
"""
import hashlib, json, os, re, sys

R = '/tmp/claude-0/-home-user-afl-rl-engine/52aec7aa-3e34-5a29-a45f-2e2388143230/scratchpad/rehearsal_326'
BOOT = os.path.join(R, 'data', 'expected_boot.json')
CONTRACT = os.path.join(R, 'data', 'release_contract.json')
SELFTEST = os.path.join(R, 'engine', 'rl_after', 'one_source_selftest.py')


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def load(p):
    return json.load(open(p))


def save(p, d):
    open(p, 'w').write(json.dumps(d, indent=1, sort_keys=True) + '\n')


def set_boot_value(key, new):
    """Text-level replacement so expected_boot.json keeps its existing key ORDER (two trailing notes sit
    outside sorted order); a JSON round-trip would reshuffle the file and bury the one real change."""
    src = open(BOOT).read()
    m = re.search(r'("%s": ")([0-9a-f]+)(")' % re.escape(key), src)
    assert m, 'expected_boot has no %s pin' % key
    print('expected_boot %-12s %s -> %s' % (key, m.group(2), new))
    open(BOOT, 'w').write(src[:m.start(2)] + new + src[m.end(2):])


def contract_hash(c):
    body = {k: v for k, v in c.items() if k not in ('contract_sha256', '_doc')}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def restamp_contract(c):
    c.pop('contract_sha256', None)
    c['contract_sha256'] = contract_hash(c)
    return c['contract_sha256']


cmd = sys.argv[1]
if cmd == 'engines':
    rm = md5(os.path.join(R, 'engine', 'rl_after', 'rl_model.py'))
    eh = md5(os.path.join(R, 'engine', 'rl_after', '_merged_recover.py'))
    set_boot_value('rl_model', rm)
    set_boot_value('engine_head', eh)
    c = load(CONTRACT)
    ids = c['identities']
    print('contract rl_model    %s -> %s' % (ids.get('rl_model'), rm))
    print('contract engine_head %s -> %s' % (ids.get('engine_head'), eh))
    ids['rl_model'] = rm
    ids['engine_head'] = eh
    print('contract_sha256 %s -> %s' % (c.get('contract_sha256'), restamp_contract(c)))
    save(CONTRACT, c)
elif cmd == 'board':
    bm = sys.argv[2]
    set_boot_value('board', bm)
    c = load(CONTRACT)
    print('contract board %s -> %s' % (c['identities'].get('board'), bm))
    c['identities']['board'] = bm
    print('contract_sha256 %s -> %s' % (c.get('contract_sha256'), restamp_contract(c)))
    save(CONTRACT, c)
elif cmd == 'contract_md5':
    new = md5(os.path.join(R, 'ui', 'release_pick_curve.json'))
    src = open(SELFTEST).read()
    m = re.search(r"_contract_md5='([0-9a-f]{32})'", src)
    print('selftest _contract_md5 %s -> %s' % (m.group(1), new))
    src = src.replace(m.group(0), "_contract_md5='%s'" % new, 1)
    open(SELFTEST, 'w').write(src)
else:
    raise SystemExit('unknown: %s' % cmd)
