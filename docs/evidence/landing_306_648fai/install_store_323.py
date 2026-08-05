#!/usr/bin/env python3
"""#306 LANDING — install the #323 corrected store (Addenda 1-4) as the live single source.

The fixture IS the batch: no script re-derives the owner's rulings here. The corrected copy was
built from the owner-worded #323 rulings on branch claude/afl-valuation-coordinator-4k9vy5
(commit bcb12ea, docs/recipe/handover_store/rl_model_data.json) and its bytes are installed
verbatim. Both ends are asserted by full md5 before anything is written.

  from  81d2470440a80f72afea4405e94338c5   (the live store, the whole rehearsal's basis)
  to    f1e8c9fed35462536d00add604f69a3f   (#323 acceptance fixture, re-cut at Addendum 4)

Dry-run first, all-or-nothing, per the standing install discipline.

  python3 install_store_323.py --dry-run   # asserts + reports, writes nothing
  python3 install_store_323.py --install   # asserts, writes, re-asserts
"""
import hashlib, json, os, shutil, sys

FROM_MD5 = '81d2470440a80f72afea4405e94338c5'
TO_MD5 = 'f1e8c9fed35462536d00add604f69a3f'

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TARGET = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')


def md5(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else '--dry-run'
    src = os.environ.get('LANDING_STORE_SRC')
    if not src or not os.path.exists(src):
        raise SystemExit('HALT: set LANDING_STORE_SRC to the fetched fixture bytes')

    got_src, got_dst = md5(src), md5(TARGET)
    print('source fixture   %s  (expect %s)' % (got_src, TO_MD5))
    print('live store       %s  (expect %s)' % (got_dst, FROM_MD5))
    if got_src != TO_MD5:
        raise SystemExit('HALT: the fixture is not the #323 acceptance bytes — nothing written')
    if got_dst != FROM_MD5:
        raise SystemExit('HALT: the live store is not the rehearsal basis — nothing written')

    a = json.load(open(TARGET))
    b = json.load(open(src))
    ka = {r.get('key') for r in a}
    kb = {r.get('key') for r in b}
    print('records  %d -> %d   removed %s   added %s'
          % (len(a), len(b), sorted(ka - kb), sorted(kb - ka)))
    ia = {r.get('key'): r for r in a}
    changed = [k for k in sorted(ka & kb) if ia[k] != {r.get('key'): r for r in b}[k]]
    print('records differing on a shared key: %d' % len(changed))

    if mode == '--dry-run':
        print('DRY RUN — nothing written.')
        return
    if mode != '--install':
        raise SystemExit('HALT: pass --dry-run or --install')

    shutil.copyfile(src, TARGET)
    now = md5(TARGET)
    if now != TO_MD5:
        raise SystemExit('HALT: post-write md5 %s != %s' % (now, TO_MD5))
    print('INSTALLED — live store is now %s' % now)


if __name__ == '__main__':
    main()
