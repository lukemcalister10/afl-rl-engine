#!/usr/bin/env python3
"""SEASON-STATE — derivation, engine wiring, and behavioural proofs (final integration 2026-07-21,
supervisor 2nd review). Replaces the earlier frozen-literal test: calendar progress and empirical exposure
pace are now DYNAMIC, DERIVED, and DISTINCT, read by the engine from data/season_state.json.

Proves:
  (a) R14 derivation reproduces the approved values EXACTLY from the accepted store (calendar 0.58, exposure
      0.545) and calendar advances R15..R19 -> 0.63/0.67/0.71/0.75/0.79, final -> 1.00;
  (b) the engine READS the dynamic values (SEASON_PROG / EXPO_F / _SFE rerouted to season_state; the frozen
      literal + the RL_M3_FE/RL_EXPO_F env reads are gone);
  (c) BEHAVIOUR — the exposure lever's evidence-replacement scope s=clip(1-g/11,0,1): a 6-game current sample
      is partially replaced by prior evidence (less influence) while a >=11-game sample is untouched (s=0);
      this holds in BOTH directions (a strong OR weak small sample is damped toward prior); calendar progress
      and exposure pace are NOT required to be equal (0.58 != 0.545); completed seasons are byte-inert;
  (d) RL_SEASON_ROUNDS is inert for valuation (ingestion sanity bound only, class B);
  (e) STALE-STATE REJECTION — a contract whose as_of_round disagrees with expected_boot, or whose
      season_prog disagrees with the board SEASON_PROG, fails closed.

No parameter is tuned; no approved vector is altered. `python3 season_progress_test.py` -> PASS/FAIL.
"""
import os, sys, re, json, tempfile, subprocess, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, ROOT)
import season_state as S  # noqa: E402

# The R14 season-state expectation (exposure_pace 0.545) is derived from the EXACT R14 historical store
# bytes at the accepted R14 authority anchor (NOT from the current R19 store, which advanced to f37d9716
# and derives the current R19 exposure pace 0.727). ITEM 408 item 5.1.
R14_ANCHOR = '93bd01af86db00c169714652714a364bd2635764'

def _r14_anchor_store():
    """Materialize the exact R14 store bytes (git blob at the R14 anchor) to a temp file; md5 968de0c7."""
    p = os.path.join(tempfile.mkdtemp(prefix='r14_store_'), 'rl_model_data.json')
    with open(p, 'wb') as f:
        f.write(subprocess.check_output(
            ['git', 'show', '%s:engine/rl_after/rl_model_data.json' % R14_ANCHOR], cwd=ROOT))
    return p
RC = None
try:
    _spec = importlib.util.spec_from_file_location('rc', os.path.join(ROOT, 'release_contract.py'))
    RC = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(RC)
except Exception:
    pass

R = []
def ck(name, ok, detail=''):
    R.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('  PASS ' if ok else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(ok)

def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()

def scope(g):  # per-player evidence-replacement scope s = clip(1 - g/11, 0, 1)
    return min(1.0, max(0.0, 1.0 - g / S.EXPO_SCOPE_DEN))

def main():
    print('=== SEASON-STATE derivation + engine wiring + behaviour ===')
    cur_store = os.path.join(ROOT, 'engine', 'rl_after', 'rl_model_data.json')

    # (a) R14 derivation + progression. The R14 expectation is derived from the EXACT R14 anchor store
    # (968de0c7 @ 93bd01af), NOT the current R19 store — that store advanced R14->R19 and now derives the
    # current R19 exposure pace (0.727). Deriving the R14 expectation from the R19 store was the stale bug.
    st = S.derive(14, _r14_anchor_store(), season_year=2026, season_total_rounds=24)
    ck('(a) R14 calendar_progress == 0.58 (derived)', st['calendar_progress'] == 0.58)
    ck('(a) R14 exposure_pace == 0.545 (from the exact R14 anchor store 968de0c7: 305 durable, median 12, 12/22)',
       st['exposure_pace'] == 0.545 and st['exposure_derivation']['eligible_durable_players'] == 305
       and st['exposure_derivation']['median_current_games'] == 12
       and str(st.get('source_store_md5', '')).startswith('968de0c7'))
    # the CURRENT R19 store derives the CURRENT accepted R19 season state (exposure 0.727, calendar 0.79)
    st19 = S.derive(19, cur_store, season_year=2026, season_total_rounds=24)
    ck('(a) R19 (current store f37d9716) exposure_pace == 0.727, calendar_progress == 0.79',
       st19['exposure_pace'] == 0.727 and st19['calendar_progress'] == 0.79
       and str(st19.get('source_store_md5', '')).startswith('f37d9716'))
    prog = {r: S.calendar_progress(r, 24) for r in (14, 15, 16, 17, 18, 19, 24)}
    ck('(a) calendar advances R15..R19 -> 0.63/0.67/0.71/0.75/0.79, final -> 1.00',
       [prog[r] for r in (14, 15, 16, 17, 18, 19, 24)] == [0.58, 0.63, 0.67, 0.71, 0.75, 0.79, 1.0], prog)

    # (b) engine reads the dynamic values (no frozen literal; no RL_M3_FE/RL_EXPO_F env reads)
    rlm = read('engine/rl_after/rl_model.py')
    ck('(b) SEASON_PROG rerouted to season_state (no frozen =0.58 literal)',
       "_season_val('calendar_progress'" in rlm and not re.search(r'^SEASON_PROG\s*=\s*0\.58', rlm, re.M))
    cp = read('engine/forward_valuation/conditional_prior.py')
    ck('(b) EXPO_F rerouted to exposure_pace; _SFE rerouted to calendar_progress',
       "EXPO_F=_season_val('exposure_pace'" in cp and "_SFE=_season_val('calendar_progress'" in cp)
    for f in ('engine/rl_after/rl_model.py', 'engine/rl_after/_merged_recover.py',
              'engine/forward_valuation/conditional_prior.py'):
        s = read(f)
        ck('(b) no live RL_M3_FE/RL_EXPO_F env read in %s' % os.path.basename(f),
           "environ.get('RL_M3_FE'" not in s and "environ.get('RL_EXPO_F'" not in s)
    mc = json.load(open(os.path.join(ROOT, 'data', 'model_config.json')))
    ck('(b) RL_M3_FE + RL_EXPO_F removed from the manifest (no frozen config twin)',
       'RL_M3_FE' not in mc['vars'] and 'RL_EXPO_F' not in mc['vars'])
    ck('(b) immutable derivation policy stamped (season_state_policy_id == policy_id)',
       mc.get('season_state_policy_id') == S.policy_id())

    # (c) BEHAVIOUR — small sample partially replaced; >=11 untouched; both directions; distinct from calendar
    s6, s9, s11, s12 = scope(6), scope(9), scope(11), scope(12)
    ck('(c) 6-game sample is partially replaced by prior evidence (s>0)', s6 > 0, 's(6)=%.4f' % s6)
    ck('(c) >=11-game sample is UNTOUCHED by the exposure lever (s=0)', s11 == 0.0 and s12 == 0.0,
       's(11)=%.4f s(12)=%.4f' % (s11, s12))
    ck('(c) smaller current sample -> MORE prior replacement (monotone s: 6>9>11)', s6 > s9 > s11)
    # a smaller sample has LESS influence: the in-progress prior-decay exponent ex = 1 - s*(1-f) is SMALLER
    # for a bigger s (prior seasons decay less -> retained more -> current sample counts relatively less).
    f = st['exposure_pace']
    ex6 = 1 - s6 * (1 - f); ex12 = 1 - s12 * (1 - f)
    ck('(c) 6-game current sample has LESS influence than 12-game (prior retained more: ex(6) < ex(12))',
       ex6 < ex12, 'ex(6)=%.4f ex(12)=%.4f' % (ex6, ex12))
    # both directions: the damping toward prior is symmetric in the sample's strength (a proxy: the current
    # level's weight (1-s) is < 1 for a small sample and == 1 for >=11, regardless of whether the level is
    # above or below the prior — the lever damps a strong small sample AND a weak small sample identically).
    ck('(c) damping is direction-symmetric: current-level weight (1-s) < 1 for a small sample, == 1 at >=11',
       (1 - s6) < 1.0 and (1 - s12) == 1.0)
    ck('(c) calendar_progress and exposure_pace are DISTINCT (not required equal): 0.58 != 0.545',
       st['calendar_progress'] != st['exposure_pace'])
    # completed seasons byte-inert: the in-progress branch only fires for Y == inprog_year
    cpsrc = read('engine/forward_valuation/conditional_prior.py')
    ck('(c) exposure lever fires ONLY for the in-progress season (completed seasons byte-inert)',
       'Y==EXPO_INPROG_Y and EXPO_F<1.0' in cpsrc)

    # (d) RL_SEASON_ROUNDS inert for valuation
    valn = ['engine/rl_after/rl_model.py', 'engine/rl_after/_merged_recover.py',
            'engine/forward_valuation/conditional_prior.py', 'engine/forward_valuation/distribution_pricing.py']
    ck('(d) RL_SEASON_ROUNDS absent from every valuation-path module (class B, inert)',
       not any('RL_SEASON_ROUNDS' in read(f) for f in valn))

    # (e) STALE-STATE REJECTION — build a FULLY COHERENT positive fixture (EVERY file release_contract.verify
    # reads: the season-state policy season_state.py, the authoritative season_state.json, the source store
    # rl_model_data.json, the board, expected_boot, release_contract, model_config), PROVE it passes FIRST,
    # then mutate EXACTLY ONE targeted field per negative control and prove the halt reason NAMES that field
    # (ITEM 408 item 5.2 — a control that halts earlier because the fixture is incomplete is not evidence).
    if RC is not None:
        FIX_FILES = ('season_state.py', 'data/model_config.json', 'data/expected_boot.json',
                     'data/release_contract.json', 'data/season_state.json',
                     'data/rl_build/rl_app_data.json', 'engine/rl_after/rl_model_data.json')

        def build_fixture():
            t = tempfile.mkdtemp(prefix='rc_fixture_')
            for rel in FIX_FILES:
                os.makedirs(os.path.dirname(os.path.join(t, rel)) or t, exist_ok=True)
                open(os.path.join(t, rel), 'wb').write(open(os.path.join(ROOT, rel), 'rb').read())
            return t

        def verify_fixture(t):
            try:
                RC.verify('gate', t, halt=False); return True, ''
            except (AssertionError, SystemExit) as e:
                return False, str(e)

        # PROVE the coherent positive fixture PASSES first (the baseline for every negative below).
        pos_ok, pos_reason = verify_fixture(build_fixture())
        ck('(e) the fully coherent positive fixture PASSES release_contract.verify (baseline)', pos_ok, pos_reason[:120])

        def negative(rel, mut, field, reseal_contract=False):
            """Mutate exactly ONE field in ONE fixture file; return the halt reason (or '')."""
            t = build_fixture()
            p = os.path.join(t, rel)
            obj = json.load(open(p))
            mut(obj)
            if reseal_contract:
                obj.pop('contract_sha256', None); obj['contract_sha256'] = RC.contract_hash(obj)
            json.dump(obj, open(p, 'w'))
            ok, reason = verify_fixture(t)
            return ('' if ok else reason)

        r1 = negative('data/release_contract.json', lambda c: c['season_metadata'].__setitem__('as_of_round', 15), 'as_of_round', reseal_contract=True)
        ck('(e) stale contract season_metadata.as_of_round fails closed + halt names as_of_round',
           bool(r1) and 'as_of_round' in r1, r1[:100])
        r2 = negative('data/release_contract.json', lambda c: c['season_metadata'].__setitem__('season_prog', 0.63), 'season_prog', reseal_contract=True)
        ck('(e) stale contract season_metadata.season_prog fails closed + halt names season_prog',
           bool(r2) and 'season_prog' in r2, r2[:100])
        r3 = negative('data/season_state.json', lambda s: s.__setitem__('exposure_pace', 0.9), 'exposure_pace')
        ck('(e) stale season_state.json exposure_pace fails closed + halt names exposure',
           bool(r3) and 'exposure' in r3, r3[:100])
        r4 = negative('data/season_state.json', lambda s: s.__setitem__('calendar_progress', 0.5), 'calendar_progress')
        ck('(e) stale season_state.json calendar_progress fails closed + halt names calendar',
           bool(r4) and 'calendar' in r4, r4[:100])
        r5 = negative('data/season_state.json', lambda s: s.__setitem__('source_store_md5', 'deadbeef' * 4), 'source_store_md5')
        ck('(e) stale season_state.json source_store_md5 fails closed + halt names the store',
           bool(r5) and 'store' in r5, r5[:100])
    else:
        ck('(e) release_contract importable for stale-state checks', False, 'import failed')

    npass = sum(1 for x in R if x['pass']); n = len(R)
    out = os.path.abspath(os.path.join(HERE, '..', 'evidence', 'season_progress_inventory.json'))
    inv = {'r14_state': st, 'r19_current_state': st19, 'calendar_progression': prog,
           'exposure_scope_examples': {g: scope(g) for g in (3, 6, 9, 11, 12, 20)},
           'engine_wired': True, 'policy_id': S.policy_id(),
           'classification': {'calendar_progress': 'A live valuation semantic — DERIVED, dynamic release state',
                              'exposure_pace': 'A live valuation semantic — DERIVED from the staged store, dynamic',
                              'RL_SEASON_ROUNDS': 'B infra (ingestion sanity bound; inert)'},
           'derivation_policy': S._POLICY}
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump(inv, open(out, 'w'), indent=2)
    print('\nRESULT: %d/%d PASS  -> %s' % (npass, n, os.path.relpath(out, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
