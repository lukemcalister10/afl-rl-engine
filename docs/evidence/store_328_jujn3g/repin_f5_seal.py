#!/usr/bin/env python3
"""#328 STEP 5 — RE-PIN THE F5 ENTRANT SEAL everywhere it is named, as ONE disclosed act.

WHY: the #323 corrected store changes the recorded intake history the entrant structure is measured
from, and the ruled ladder changes the PVC each expected slot is credited at. Re-sealed from intake
history by the seal's own instrument (`seal_structure.py`), the structure moves:

    seal_sha256_8      ed5b7fcc -> c9e7491b
    entrant PVC total  62726    -> 62931      (draft 55669 -> 55753 · mech 7057 -> 7178)
    expected slots/yr  103.43   -> 103.43     (UNCHANGED — re-measured, not assumed)

THE SEAL FIRED IN ANGER BEFORE THIS RAN, which is the point of it. With the new structure installed
and the pins still stale, `rl_export.py` stopped the render dead:

    LEG F5 HALT (§2.viii): sealed entrant structure seal drift — recomputed c9e7491b vs stored
    c9e7491b vs pinned ed5b7fcc. Re-seal from intake history before rendering.

Recomputed and stored agreed; only the hardcoded pin was stale. That is the seal-first law working:
a re-seal cannot slip past the render, and the pin cannot be moved by accident.

THE FOUR SOURCE FILES THAT NAME IT (found by search, not by memory):
    engine/rl_after/rl_export.py                        the render-time gate + its prose
    session_2026-07-18/legf5/scripts/gate_f5.py         the conservation gate's own assert + banner
    session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py   asserts the literal is present in rl_export
    ui/tests/extract_seam.test.py                       asserts the UI stamp carries seal + PVC exactly

  python3 repin_f5_seal.py <REPO> [--dry-run]
"""
import hashlib, json, os, sys

REPO = sys.argv[1].rstrip('/') if len(sys.argv) > 1 else os.getcwd()
DRY = '--dry-run' in sys.argv
P = lambda *a: os.path.join(REPO, *a)

OLD_SEAL, NEW_SEAL = 'ed5b7fcc', 'c9e7491b'
OLD_PVC, NEW_PVC = '62726', '62931'
OLD_STORE, NEW_STORE = '81d24704', 'f1e8c9fe'
OLD_CURVE, NEW_CURVE = '01f27f02', 'df766dff'

FILES = {
    'engine/rl_after/rl_export.py': [(OLD_SEAL, NEW_SEAL), (OLD_STORE, NEW_STORE), (OLD_CURVE, NEW_CURVE)],
    'session_2026-07-18/legf5/scripts/gate_f5.py': [(OLD_SEAL, NEW_SEAL)],
    'session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py': [(OLD_SEAL, NEW_SEAL), (OLD_PVC, NEW_PVC)],
    'ui/tests/extract_seam.test.py': [(OLD_SEAL, NEW_SEAL), (OLD_PVC, NEW_PVC)],
}


def main():
    struct = json.load(open(P('session_2026-07-18/legf5/sealed_entrant_structure.json')))
    body = {k: v for k, v in struct.items() if k != 'seal_sha256_8'}
    recomputed = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':')).encode()).hexdigest()[:8]
    print('the installed structure: stored seal %s · recomputed %s · MATCH %s'
          % (struct['seal_sha256_8'], recomputed, struct['seal_sha256_8'] == recomputed))
    assert recomputed == struct['seal_sha256_8'] == NEW_SEAL, \
        'the installed structure must already carry and reproduce the new seal'
    assert str(struct['entrant_pvc']['total']) == NEW_PVC, 'entrant total %s' % struct['entrant_pvc']['total']
    print('  entrant PVC total %s · draft %s · mech %s · expected slots/yr %s'
          % (struct['entrant_pvc']['total'], struct['entrant_pvc']['draft'],
             struct['entrant_pvc']['mech'], struct['expected_slots_per_year']))
    print('  stamp (MEASURED, never hardcoded): %s' % json.dumps(struct.get('stamp'), sort_keys=True))

    plan = []
    for rel, subs in FILES.items():
        src = open(P(rel)).read()
        new = src
        counts = []
        for old, nw in subs:
            n = new.count(old)
            counts.append('%s->%s x%d' % (old, nw, n))
            if old == OLD_SEAL:
                assert n >= 1, '%s: expected at least one %s' % (rel, old)
            new = new.replace(old, nw)
        assert len(new.splitlines()) == len(src.splitlines()), '%s: line count moved' % rel
        assert OLD_SEAL not in new, '%s: a stale seal survived' % rel
        plan.append((rel, src, new, counts))
        print('\n%-52s %s' % (rel, ' · '.join(counts)))

    if DRY:
        print('\n--dry-run: nothing written.')
        return
    for rel, _src, new, _c in plan:
        open(P(rel), 'w').write(new)
    print('\nRE-PINNED — %d files.' % len(plan))
    for rel, _s, _n, _c in plan:
        assert OLD_SEAL not in open(P(rel)).read(), '%s still names the old seal' % rel
        assert NEW_SEAL in open(P(rel)).read(), '%s does not name the new seal' % rel
    print('re-read after write: every file names %s and none names %s  ASSERTED' % (NEW_SEAL, OLD_SEAL))


if __name__ == '__main__':
    main()
