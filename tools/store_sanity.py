#!/usr/bin/env python3
"""tools/store_sanity.py — CONTENT invariants on the store, not identity ones.

  python3 tools/store_sanity.py            # non-zero if any row is impossible

WHY THIS EXISTS, AND IT IS NOT A NICE-TO-HAVE. Every guard in this estate polices the store's
IDENTITY — Guard 5 asserts its md5, the manifest gate asserts every carrier names the same md5, the
lander re-measures it. Not one of them looks at what the numbers SAY. So a row can be flatly
impossible — a player credited with sixty games in a season — and every gate in the repository will
go green on it forever, because the wrong number hashes just as well as the right one.

That is not hypothetical. `jesse-joyce` has carried 61 / 60 / 60 games for 2017-2019 since the
INITIAL SEED (f4a4d34, 2026-07-02) and the row has never changed in any commit since. The owner has
corrected it more than once and each correction died somewhere before the store: a fact this file
establishes by looking, not by remembering. A guard that costs milliseconds is the difference
between a correction that sticks and one that has to be made a fourth time.

THE BAR: a season cannot contain more games than a season has. 24 home-and-away rounds plus a
maximum of 4 finals = 28. The ceiling is deliberately generous — it is not trying to detect a
player who missed a week, it is trying to make an IMPOSSIBLE row impossible to ignore. Historic
seasons ran to 22 or 23 rounds, so a tighter per-year table would catch more; it would also be one
more thing to maintain each season, and the failure this exists for is off by a factor of two.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
STORE = os.path.join('engine', 'rl_after', 'rl_model_data.json')

#: 24 home-and-away rounds + at most 4 finals. A season with more games than this did not happen.
SEASON_GAMES_CEILING = 28


def rows(root):
    with open(os.path.join(root, STORE), encoding='utf-8') as f:
        d = json.load(f)
    return d['players'] if isinstance(d, dict) and 'players' in d else d


def offenders(root):
    out = []
    for r in rows(root):
        for s in (r.get('scoring') or []):
            g = int(s.get('games', 0) or 0)
            if g > SEASON_GAMES_CEILING:
                out.append({'key': r.get('key'), 'player': r.get('player'),
                            'retired': bool(r.get('_retired')), 'year': s.get('year'),
                            'games': g, 'avg': s.get('avg')})
            if g < 0:
                out.append({'key': r.get('key'), 'player': r.get('player'),
                            'retired': bool(r.get('_retired')), 'year': s.get('year'),
                            'games': g, 'avg': s.get('avg'), 'why': 'negative games'})
    return out


def main(argv=None):
    root = ROOT
    if argv and len(argv) > 1 and argv[1] == '--root':
        root = os.path.abspath(argv[2])
    bad = offenders(root)
    print('STORE SANITY — a season cannot contain more than %d games (24 H&A + 4 finals)'
          % SEASON_GAMES_CEILING)
    if not bad:
        n = sum(len(r.get('scoring') or []) for r in rows(root))
        print('  PASS — %d season rows, none impossible.' % n)
        return 0
    print('  %d IMPOSSIBLE SEASON ROW(S):' % len(bad))
    for b in bad:
        print('    %-22s %s  year %s: games %s, avg %s%s'
              % (b['player'], '(retired)' if b['retired'] else '(ACTIVE)', b['year'],
                 b['games'], b['avg'], '  [%s]' % b['why'] if b.get('why') else ''))
    print('  A row here is wrong in the store itself. Correct it through `tools/land edit`, which')
    print('  asserts the old value before replacing it — never by hand.')
    return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
