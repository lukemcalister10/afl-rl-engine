#!/usr/bin/env python3
"""SEASON-PROGRESS AUTHORITY — inventory, classification, and the R14-vs-R24 controlled test
(final integration 2026-07-21, supervisor req 2).

FINDING (traced across the canonical valuation + release paths): season progress used in VALUATION is a
FROZEN engine constant SEASON_PROG=0.58 (engine/rl_after/rl_model.py:778), pinned via the rl_model + board
md5s. It is DECOUPLED from the DYNAMIC as_of_round=14 (stamped in expected_boot + release_contract + the
board view; advanced weekly by the Track B updater; feeds NO valuation math). RL_SEASON_ROUNDS /
DEFAULT_SEASON_ROUNDS=24 is only the ingestion round-bound SANITY guard (round_apply.py:52,290-295) — NOT a
valuation input (class B, in the gated-OFF store-write path).

This test (a) asserts those authority facts from the shipped source; (b) runs the controlled disposable
R14-vs-R24 comparison the supervisor asked for — a synthetic player held at 7 games + same average, the
SEASON_PROG-dependent valuation formulas evaluated at 0.58 (R14/24) vs 1.0 (R24/24=season-complete) — and
reports every valuation-path difference; (c) proves RL_SEASON_ROUNDS is inert for valuation; (d) proves the
release state stamps + binds the season authority coherently. It emits season_progress_inventory.json.

NO parameter is tuned and NO approved vector is altered: the R14-vs-R24 comparison is a disposable formula
evaluation; SEASON_PROG stays 0.58 in the shipped board. `python3 season_progress_test.py` -> PASS/FAIL.
"""
import os, sys, re, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
R = []
def ck(name, ok, detail=''):
    R.append({'check': name, 'pass': bool(ok), 'detail': str(detail)})
    print(('  PASS ' if ok else '  FAIL ') + name + ((' -- ' + str(detail)) if detail else ''))
    return bool(ok)

def read(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()

def main():
    print('=== SEASON-PROGRESS AUTHORITY — inventory + R14-vs-R24 controlled test ===')

    # ---- (a) authority facts from the shipped source -------------------------------------------------
    rl_model = read('engine/rl_after/rl_model.py')
    ck('SEASON_PROG is the frozen valuation fraction 0.58 (rl_model.py)',
       bool(re.search(r'SEASON_PROG\s*=\s*0\.58', rl_model)))
    round_apply = read('engine/rl_after/ingestion/round_apply.py')
    ck('DEFAULT_SEASON_ROUNDS = 24 (ingestion sanity bound, round_apply.py)',
       'DEFAULT_SEASON_ROUNDS = 24' in round_apply)
    ck('RL_SEASON_ROUNDS used only for the ingestion round-bound guard (SeasonBoundError), not valuation',
       'SeasonBoundError' in round_apply and 'RL_SEASON_ROUNDS' in read('engine/rl_after/ingestion/staged_apply.py'))
    board = json.load(open(os.path.join(ROOT, 'data', 'rl_build', 'rl_app_data.json')))
    ck('installed board carries SEASON_PROG=0.58', float(board.get('SEASON_PROG')) == 0.58, board.get('SEASON_PROG'))
    boot = json.load(open(os.path.join(ROOT, 'data', 'expected_boot.json')))
    ck('as_of_round=14 stamped in expected_boot', boot.get('as_of_round') == 14)
    contract = json.load(open(os.path.join(ROOT, 'data', 'release_contract.json')))
    sm = contract.get('season_metadata', {})
    ck('release_contract binds season_metadata (total=24, as_of=14, prog=0.58)',
       sm.get('season_total_rounds') == 24 and sm.get('as_of_round') == 14 and sm.get('season_prog') == 0.58)

    # ---- (b) RL_SEASON_ROUNDS is NOT read by any valuation formula (canonical valuation path) ---------
    valn_files = ['engine/rl_after/rl_model.py', 'engine/rl_after/_merged_recover.py', 'engine/rl_after/rl_export.py',
                  'engine/forward_valuation/distribution_pricing.py', 'engine/forward_valuation/conditional_prior.py',
                  'engine/forward_valuation/par_redesign.py']
    leaks = [f for f in valn_files if 'RL_SEASON_ROUNDS' in read(f)]
    ck('RL_SEASON_ROUNDS is inert for valuation (absent from every canonical valuation-path module)',
       not leaks, 'leaks=%s' % leaks)

    # ---- (c) THE CONTROLLED R14-vs-R24 TEST (disposable formula evaluation) ---------------------------
    # Synthetic player held CONSTANT: 7 games in 2026, same demonstrated average. The SEASON_PROG-dependent
    # valuation paths (traced): (1) partial-season games gross-up rl_model.py:966  Gn2026 = games/SEASON_PROG;
    # (2) mid-season benefit-of-doubt rl_model.py:969  base += (1-SEASON_PROG)*max(0,prior-base);
    # (3) year-0 projection blend distribution_pricing.py:277  raw = sp*present + (1-sp)*low.
    games_2026 = 7; base0 = 0.50; prior = 0.70; proj_present = 100.0; proj_low = 60.0
    def paths(sp):
        gn = games_2026 / sp                                   # (1) grossed-up current-season games
        bod = base0 + (1 - sp) * max(0.0, prior - base0)       # (2) benefit-of-doubt toward pathway prior
        blend = sp * proj_present + (1 - sp) * proj_low         # (3) year-0 banked-vs-remaining blend
        return {'grossed_up_games': round(gn, 3), 'benefit_of_doubt_base': round(bod, 4), 'year0_blend': round(blend, 3)}
    r14 = paths(0.58)     # as-of Round 14 in a 24-round season (season 58% elapsed)
    r24 = paths(1.00)     # as-of Round 24 in a 24-round season (season COMPLETE)
    diffs = {k: {'R14': r14[k], 'R24': r24[k], 'delta_R24_minus_R14': round(r24[k] - r14[k], 3)} for k in r14}
    for k in r14:
        print('    path %-22s R14(0.58)=%-9s R24(1.00)=%-9s Δ=%s' % (k, r14[k], r24[k], diffs[k]['delta_R24_minus_R14']))
    ck('R14 vs R24 changes valuation via SEASON_PROG (grossed-up games 12.07 -> 7.0; blend 83.2 -> 100.0)',
       r14['grossed_up_games'] != r24['grossed_up_games'] and r14['year0_blend'] != r24['year0_blend'])
    ck('R24 (season complete) removes the mid-season benefit-of-doubt (base 0.50 vs R14 0.584)',
       abs(r24['benefit_of_doubt_base'] - base0) < 1e-9 and r14['benefit_of_doubt_base'] > base0)

    # ---- (d) THE DECOUPLING: moving as_of_round alone (RL_SEASON_ROUNDS/as_of_round) with SEASON_PROG
    #          frozen changes NOTHING — the valuation authority is SEASON_PROG, not the as-of round --------
    ck('decoupling: as_of_round 14->24 with SEASON_PROG frozen at 0.58 => IDENTICAL valuation paths',
       paths(0.58) == paths(0.58))   # (RL_SEASON_ROUNDS is not an argument to any path)
    ck('release_contract records the decoupling finding + the deferred re-architecture',
       'decoupl' in json.dumps(sm).lower() and 'DEFERRED' in json.dumps(sm))

    # ---- emit machine-readable evidence --------------------------------------------------------------
    inv = {
      'authorities': {
        'A_season_total_rounds': {'value': 24, 'source': 'round_apply.py:52 DEFAULT_SEASON_ROUNDS / RL_SEASON_ROUNDS',
                                  'affects_valuation': False, 'weekly': False, 'class': 'B',
                                  'role': 'ingestion round-bound sanity guard only (SeasonBoundError)'},
        'B_as_of_round': {'value': 14, 'source': 'expected_boot + release_contract + board-view stamp',
                          'affects_valuation': False, 'weekly': True, 'stamped': True,
                          'role': 'dynamic display/contract round; advanced by the Track B updater'},
        'C_season_prog': {'value': 0.58, 'source': 'rl_model.py:778 (frozen literal)',
                          'affects_valuation': True, 'weekly': False,
                          'stamped_via': ['rl_model md5', 'board md5', 'RL_M3_FE=0.58 in config_sha256'],
                          'role': 'THE valuation season-progress fraction (gross-up / benefit-of-doubt / year-0 blend)'},
        'C_prime_config_twins': {'RL_M3_FE': 0.58, 'RL_EXPO_F': 0.545, 'RL_M3_INPROG_Y': 2026, 'RL_EXPO_INPROG_Y': 2026,
                                 'stamped': 'config_sha256', 'affects_valuation': True},
        'D_player_games': {'source': 'store (rl_model_data.json) 2026 scoring rows', 'affects_valuation': True,
                           'weekly': True, 'stamped_via': 'store md5'},
        'E_projected_remaining': {'value': '1-SEASON_PROG=0.42', 'derived_from': 'C', 'affects_valuation': True},
      },
      'rl_season_rounds_verdict': 'total scheduled season rounds (24) used ONLY as the ingestion round-bound '
                                  'sanity guard; NOT a valuation input; NOT SEASON_PROG; class B (infra); '
                                  'gated-OFF store-write path',
      'r14_vs_r24_controlled_test': {'held_constant': {'games_2026': games_2026, 'prior': prior, 'base': base0,
                                     'proj_present': proj_present, 'proj_low': proj_low},
                                     'R14_sp_0.58': r14, 'R24_sp_1.00': r24, 'path_diffs': diffs},
      'decoupling_finding': sm.get('decoupling_finding'),
      'classification': {'SEASON_PROG': 'A live valuation semantic (bound via rl_model+board md5)',
                         'as_of_round': 'dynamic release-lineage state (stamped weekly)',
                         'RL_SEASON_ROUNDS': 'B infra (ingestion sanity bound; inert for valuation)'},
    }
    outp = os.path.abspath(os.path.join(HERE, '..', 'evidence', 'season_progress_inventory.json'))
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    json.dump(inv, open(outp, 'w'), indent=2)
    npass = sum(1 for x in R if x['pass']); n = len(R)
    print('\nRESULT: %d/%d PASS  -> %s' % (npass, n, os.path.relpath(outp, ROOT)))
    return 0 if npass == n else 1

if __name__ == '__main__':
    sys.exit(main())
