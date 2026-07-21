#!/usr/bin/env python3
"""AUTHORITATIVE DYNAMIC SEASON STATE (final integration 2026-07-21, supervisor 2nd review).

TWO DISTINCT concepts — never conflated:

  1. CALENDAR SEASON PROGRESS  (how much of the SCHEDULED season has elapsed)
       calendar_progress = round_half_up(100 * as_of_round / season_total_rounds) / 100
     Immutable POLICY: the formula + whole-percentage rounding convention.
     Dynamic VALUE: advances every accepted round (R14=0.58, R15=0.63, ... final=1.00).
     Consumed as the ONE value everywhere the engine previously read SEASON_PROG / RL_M3_FE.

  2. EMPIRICAL EXPOSURE PACE  (so a small sample is not weighted like a large one — NOT calendar progress)
       exposure_pace = round(median(current-season games of the durable population) / EXPO_DEN, 3), capped 1.0
       durable population = prior-season games >= EXPO_DURABLE_MIN ; EXPO_DEN = 22
       per-player evidence-replacement scope s = clip(1 - current_games / EXPO_SCOPE_DEN, 0, 1)
         (players with >= EXPO_SCOPE_DEN=11 current games are untouched BY CONSTRUCTION, s=0)
     Immutable POLICY: population definition, denominator, scope denominator, formula, rounding.
     Dynamic VALUE: freshly DERIVED FROM THE STAGED STORE each accepted round; -> 1.0 at season completion,
     resets next season. Consumed where the engine previously read RL_EXPO_F.

The realised weekly values (calendar_progress, exposure_pace) are DYNAMIC RELEASE STATE; the derivation
POLICY is immutable model/release policy (policy_id() hashes it). The engine reads the VALUES from
data/season_state.json; a canonical/gate build fails closed if that state is stale/contradictory.
"""
import os, json, math, hashlib, statistics

# ---- immutable derivation POLICY (a change here is a class-A model-policy change; hashed by policy_id) ----
EXPO_DURABLE_MIN = 18      # durable population: prior-season games >= this
EXPO_DEN = 22.0            # exposure-pace denominator (games/season)
EXPO_SCOPE_DEN = 11.0      # per-player evidence-replacement scope denominator (on-pace floor; s=0 at >= this)
EXPO_ROUND = 3            # exposure-pace rounding precision
SEASON_TOTAL_ROUNDS_DEFAULT = 24
STATE_PATH = ('data', 'season_state.json')

_POLICY = {
    'calendar_formula': 'round_half_up(100 * as_of_round / season_total_rounds) / 100',
    'exposure_formula': 'round(median(current_games where prior_games>=%d) / %g, %d), cap 1.0' % (
        EXPO_DURABLE_MIN, EXPO_DEN, EXPO_ROUND),
    'exposure_scope': 's = clip(1 - current_games / %g, 0, 1); s=0 (untouched) at >= %g current games' % (
        EXPO_SCOPE_DEN, EXPO_SCOPE_DEN),
    'EXPO_DURABLE_MIN': EXPO_DURABLE_MIN, 'EXPO_DEN': EXPO_DEN, 'EXPO_SCOPE_DEN': EXPO_SCOPE_DEN,
    'EXPO_ROUND': EXPO_ROUND,
}


def policy_id():
    """Immutable derivation-policy identity (changes only when the formula/population/denominators change)."""
    return hashlib.sha256(json.dumps(_POLICY, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def round_half_up(x):
    return int(math.floor(x + 0.5))


def calendar_progress(as_of_round, season_total_rounds):
    """Whole-percentage calendar progress: round_half_up(100*round/total)/100. R14/24 -> 0.58; final -> 1.00."""
    return round_half_up(100.0 * int(as_of_round) / float(season_total_rounds)) / 100.0


def _games(row, year):
    for s in (row.get('scoring') or []):
        if s.get('year') == year:
            return int(s.get('games', 0) or 0)
    return 0


def exposure_pace(store_rows, inprog_year):
    """Empirical exposure pace from the store: median current-season games of the durable population / EXPO_DEN.
    Returns (value, metadata). Capped at 1.0 (season complete). Independent of calendar progress."""
    prior_year = inprog_year - 1
    durable = [r for r in store_rows if _games(r, prior_year) >= EXPO_DURABLE_MIN]
    cur = [_games(r, inprog_year) for r in durable]
    med = statistics.median(cur) if cur else 0.0
    raw = med / EXPO_DEN
    val = min(1.0, round(raw, EXPO_ROUND))
    meta = {'eligible_durable_players': len(durable), 'median_current_games': med, 'denominator': EXPO_DEN,
            'raw_ratio': raw, 'released_value': val, 'rounding': 'round(., %d) then cap 1.0' % EXPO_ROUND,
            'scope_denominator': EXPO_SCOPE_DEN, 'durable_min_prior_games': EXPO_DURABLE_MIN}
    return val, meta


def _store_md5(path):
    try:
        return hashlib.md5(open(path, 'rb').read()).hexdigest()
    except Exception:
        return None


def derive(as_of_round, store_path, season_year=2026, season_total_rounds=SEASON_TOTAL_ROUNDS_DEFAULT):
    """Derive the FULL authoritative season-state from an as-of round + a (staged) store. Pure function of
    (as_of_round, season_total_rounds, store bytes) + the immutable policy."""
    rows = json.load(open(store_path))
    ep, ep_meta = exposure_pace(rows, season_year)
    cp = calendar_progress(as_of_round, season_total_rounds)
    return {
        'season_year': season_year,
        'season_total_rounds': int(season_total_rounds),
        'as_of_round': int(as_of_round),
        'calendar_progress': cp,
        'exposure_pace': ep,
        'exposure_derivation': ep_meta,
        'source_store_md5': _store_md5(store_path),
        'derivation_policy_id': policy_id(),
        'inprog_year': season_year,
        '_doc': 'AUTHORITATIVE DYNAMIC SEASON STATE. calendar_progress (scheduled-season elapsed) and '
                'exposure_pace (empirical durable-sample pace — NOT calendar) are DISTINCT and both DYNAMIC; '
                'the engine reads these values; the derivation policy is immutable (derivation_policy_id).',
    }


def repo_root(root=None):
    for cand in (root, os.environ.get('RL_REPO'), os.environ.get('CLAUDE_PROJECT_DIR'),
                 os.path.dirname(os.path.abspath(__file__))):
        if cand and os.path.exists(os.path.join(cand, *STATE_PATH)):
            return os.path.abspath(cand)
    return root or os.environ.get('RL_REPO') or os.path.dirname(os.path.abspath(__file__))


def load(root=None):
    p = os.path.join(repo_root(root), *STATE_PATH)
    with open(p) as f:
        return json.load(f)


# ---- engine-facing accessors: the DYNAMIC values the engine consumes (fallback preserves dev-shell) -------
def calendar_progress_value(root=None, fallback=0.58):
    try:
        return float(load(root)['calendar_progress'])
    except Exception:
        return float(fallback)


def exposure_pace_value(root=None, fallback=0.545):
    try:
        return float(load(root)['exposure_pace'])
    except Exception:
        return float(fallback)


if __name__ == '__main__':
    import sys
    root = os.environ.get('RL_REPO') or os.path.dirname(os.path.abspath(__file__))
    if len(sys.argv) > 1 and sys.argv[1] == 'derive':
        aor = int(sys.argv[2]) if len(sys.argv) > 2 else 14
        sp = sys.argv[3] if len(sys.argv) > 3 else os.path.join(root, 'engine', 'rl_after', 'rl_model_data.json')
        print(json.dumps(derive(aor, sp), indent=2))
    else:
        try:
            st = load(root)
            print('season_state: year %s round %s/%s | calendar_progress %.2f | exposure_pace %.3f | policy %s'
                  % (st['season_year'], st['as_of_round'], st['season_total_rounds'],
                     st['calendar_progress'], st['exposure_pace'], st['derivation_policy_id'][:12]))
        except FileNotFoundError:
            print('season_state.json ABSENT (%s)' % os.path.join(root, *STATE_PATH))
