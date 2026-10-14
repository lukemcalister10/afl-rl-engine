"""THE season-state reader — one copy, no fallback.

Until 2026-10-14 the engine carried three identical private readers (`_season_val` in _merged_recover.py,
rl_model.py and forward_valuation/conditional_prior.py), each with a dev-mode fallback to the frozen
Round-14 literals (0.58 calendar progress, 0.545 exposure pace). A build whose repo root was not set, or
whose data/season_state.json was missing a key, silently priced the board at Round 14 unless the
RL_CONFIG_MODE fence happened to be on. This module is the only reader now, and it halts — in every mode —
when the authoritative value cannot be read. The engine never prices on a guessed season.

The file is data/season_state.json under the repo root named by RL_REPO (or CLAUDE_PROJECT_DIR). The
lander, the build child, the retro harness and every UI generator that loads the engine set RL_REPO.
"""
import os, json, math

STATE_REL = ('data', 'season_state.json')
KEYS = ('calendar_progress', 'exposure_pace')


def repo_root():
    r = os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR')
    if not r:
        raise RuntimeError('season-state read: repo root unresolved (set RL_REPO or CLAUDE_PROJECT_DIR); '
                           'the engine does not price on a guessed season')
    return r


def value(key):
    """The dynamic season-state value for `key` ('calendar_progress' | 'exposure_pace'), as a float."""
    if key not in KEYS:
        raise KeyError('season-state read: %r is not a season-state value %s' % (key, KEYS))
    p = os.path.join(repo_root(), *STATE_REL)
    try:
        with open(p, encoding='utf-8') as fh:
            doc = json.load(fh)
    except (OSError, ValueError) as e:
        raise RuntimeError('season-state read: cannot load %s (%s)' % (p, e)) from e
    if key not in doc:
        raise RuntimeError('season-state read: %s carries no %r' % (p, key))
    v = float(doc[key])
    if not math.isfinite(v):
        raise RuntimeError('season-state read: %s has non-finite %s=%r' % (p, key, doc[key]))
    return v
