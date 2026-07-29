#!/usr/bin/env python3
"""SEASON-STATE ANCHORS — PROVEN ABLE TO FAIL (#251 part C).

A guard added must be proven able to fail, and a guard that always fails is the same defect as one that
cannot. The current-round anchor in season_anchor_check.py replaced three hand-typed R19 constants with a
re-derivation compared against the committed stamp. That is only worth having if it still reds on the
things the constants were standing in for. Each case below builds a COMPLETE fixture, proves it PASSES
first, then mutates EXACTLY ONE artifact and requires the named check to red — a control that reds because
the fixture was incomplete is not evidence.

  positive           an untouched copy of the tree passes every current-round check
  store moved        the store advances and nothing re-derives   -> exposure + source-store reds
  store re-bytes     same rows, different bytes, same exposure   -> ONLY the source-store check reds
  round advanced     the manifest moves to R+1, stamps unmoved   -> round-agreement reds
  stamp hand-edited  a stamped value edited to a wrong number    -> derivation reds
  policy drift       the artifacts stamped under an older policy -> policy reds
  R14 wrong round    the fixed anchor derived at R15             -> R14 calendar reds
  R14 wrong store    the fixed anchor derived from the LIVE store-> R14 exposure reds

`python3 season_anchor_check_nonvacuity.py` -> PASS/FAIL, non-zero on any failure.
"""
import os, sys, json, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import season_state as S              # noqa: E402
import season_anchor_check as A       # noqa: E402

FIX_FILES = ('data/expected_boot.json', 'data/season_state.json', 'data/release_contract.json',
             'engine/rl_after/rl_model_data.json')

_R = []
def ok(name, cond, detail=''):
    _R.append((name, bool(cond)))
    print(('  PASS ' if cond else '  FAIL ') + name + ((' -- %s' % detail) if detail else ''))


def fixture():
    t = tempfile.mkdtemp(prefix='anchor_fix_')
    for rel in FIX_FILES:
        dst = os.path.join(t, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, rel), dst)
    return t


def run(t):
    """Return {check_name: passed} for the current-round anchor against fixture root t."""
    checks, _ = A.check_current_round(t)
    return {name: passed for name, passed, _ in checks}


def edit(t, rel, fn):
    p = os.path.join(t, rel)
    obj = json.load(open(p))
    obj = fn(obj) or obj
    json.dump(obj, open(p, 'w'))


def reds(res, needle):
    """The names of the checks that FAILED and mention `needle`."""
    return [n for n, passed in res.items() if not passed and needle in n]


def only_reds(res, needle):
    failed = [n for n, passed in res.items() if not passed]
    return failed and all(needle in n for n in failed)


def main():
    print('=== SEASON-STATE ANCHORS: proven able to fail ===')

    # --- positive baseline: every negative below is measured against this ---------------------------
    t = fixture()
    base = run(t)
    ok('positive: an untouched copy of the tree passes every current-round check',
       all(base.values()), '%d/%d' % (sum(base.values()), len(base)))
    shutil.rmtree(t, ignore_errors=True)

    # --- the store advances and nothing re-derives (the failure the hand-typed constant stood for) ---
    t = fixture()
    def _advance(rows):
        for r in rows:
            for s in (r.get('scoring') or []):
                if s.get('year') == 2026:
                    s['games'] = 22          # every durable player now on a full season
        return rows
    edit(t, 'engine/rl_after/rl_model_data.json', _advance)
    res = run(t)
    ok('store advanced, nothing re-derived: the exposure re-derivation reds',
       bool(reds(res, 'exposure_pace')), str(reds(res, 'exposure_pace'))[:90])
    ok('store advanced, nothing re-derived: the stamped source store reds too',
       bool(reds(res, 'LIVE store')))
    shutil.rmtree(t, ignore_errors=True)

    # --- same rows, different bytes: ONLY the source-store check may red (it is independent) ---------
    t = fixture()
    p = os.path.join(t, 'engine/rl_after/rl_model_data.json')
    json.dump(json.load(open(p)), open(p, 'w'), indent=1)      # re-serialize: same rows, new bytes
    res = run(t)
    ok('store re-serialized (same rows, new bytes): ONLY the source-store check reds',
       only_reds(res, 'LIVE store'), str([n for n, v in res.items() if not v])[:90])
    shutil.rmtree(t, ignore_errors=True)

    # --- the manifest round advances while the stamps stay behind ------------------------------------
    t = fixture()
    edit(t, 'data/expected_boot.json',
         lambda b: b.update({'as_of_round': int(b['as_of_round']) + 1}))
    res = run(t)
    ok('manifest round advanced past the stamps: the round-agreement check reds',
       bool(reds(res, 'all stamp round')), str(reds(res, 'all stamp round'))[:90])
    shutil.rmtree(t, ignore_errors=True)

    # --- a stamped value hand-edited to a wrong number ----------------------------------------------
    t = fixture()
    edit(t, 'data/season_state.json', lambda s: s.update({'exposure_pace': 0.727}))
    res = run(t)
    ok('a stamped exposure_pace hand-edited (to last round\'s value) reds',
       bool(reds(res, 'exposure_pace')))
    shutil.rmtree(t, ignore_errors=True)

    t = fixture()
    edit(t, 'data/season_state.json', lambda s: s.update({'calendar_progress': 0.79}))
    res = run(t)
    ok('a stamped calendar_progress hand-edited (to last round\'s value) reds',
       bool(reds(res, 'calendar_progress')))
    shutil.rmtree(t, ignore_errors=True)

    # --- the contract disagreeing with season_state.json --------------------------------------------
    t = fixture()
    edit(t, 'data/release_contract.json',
         lambda c: c['season_metadata'].update({'exposure_pace': 0.9}))
    res = run(t)
    ok('the release contract carrying a different pair than the derivation reds',
       bool(reds(res, 'same derived pair')))
    shutil.rmtree(t, ignore_errors=True)

    # --- policy drift: the artifacts were stamped under a different derivation policy ----------------
    t = fixture()
    edit(t, 'data/season_state.json', lambda s: s.update({'derivation_policy_id': 'stalepolicy' * 4}))
    res = run(t)
    ok('artifacts stamped under a stale derivation policy red', bool(reds(res, 'POLICY')))
    shutil.rmtree(t, ignore_errors=True)

    # --- the FIXED R14 anchor is non-vacuous too -----------------------------------------------------
    # It is hand-typed on purpose (a historical fact), so prove it actually binds: derived at the wrong
    # round, or from a store other than the pinned historical blob, it reds.
    st15 = S.derive(15, A.r14_anchor_store(ROOT), season_year=2026, season_total_rounds=24)
    ok('R14 anchor derived at R15 no longer matches the 0.58 calendar expectation',
       st15['calendar_progress'] != A.R14_CALENDAR, st15['calendar_progress'])
    st_live = S.derive(14, os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json'),
                       season_year=2026, season_total_rounds=24)
    ok('R14 anchor derived from the LIVE store no longer matches the 0.545 exposure expectation '
       '(so it is genuinely pinned to the historical blob)',
       st_live['exposure_pace'] != A.R14_EXPOSURE, st_live['exposure_pace'])

    npass = sum(1 for _, p in _R if p)
    print('\nRESULT: %d/%d PASS' % (npass, len(_R)))
    return 0 if npass == len(_R) else 1


if __name__ == '__main__':
    sys.exit(main())
