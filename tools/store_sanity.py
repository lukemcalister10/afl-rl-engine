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

THE BAR: a season cannot contain more games than a season has. 23 home-and-away GAMES (24
rounds, less every club's bye) plus at most 5 finals (FW1 / FW2 / SF / PF / GF) = 28. The ceiling is deliberately generous — it is not trying to detect a
player who missed a week, it is trying to make an IMPOSSIBLE row impossible to ignore. Historic
seasons ran to 22 or 23 rounds, so a tighter per-year table would catch more; it would also be one
more thing to maintain each season, and the failure this exists for is off by a factor of two.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
STORE = os.path.join('engine', 'rl_after', 'rl_model_data.json')

#: 23 home-and-away GAMES + at most 5 finals. A season with more games than this did not happen.
#:
#: ROUNDS ARE NOT GAMES, and that distinction is the whole of this number (owner, 2026-08-30: "28 is
#: the max games, as 23 is the max in the regular season"). The calendar carries 24 rounds — which
#: is what `season_state.season_total_rounds` means and what calendar progress divides by — but
#: every club has a bye, so no player can play more than 23 of them. A ceiling built from the ROUND
#: count would be one game too generous and would let a genuinely impossible 24-game home-and-away
#: season through.
#:
#: THE FIVE IS THE OWNER'S FINALS STRUCTURE, NOT AN ASSUMPTION (2026-08-30, verbatim): "FW1 is 4
#: teams playing / FW2 is 8 teams / SF is 4 teams / PF is 4 teams / GF is 2 teams". A club entering
#: at FW1 and reaching the Grand Final plays all five. So 23 + 5 = 28.
#:
#: Both halves were wrong in earlier drafts, in opposite directions and for the same reason —
#: assuming rather than asking. The first draft used a four-week finals series (28 by luck, from
#: 24+4); the second corrected the finals to five and carried the round-count error into 29.
SEASON_GAMES_CEILING = 28


def rows(root, spec_path=None):
    """The store's rows — AS THE ACT WOULD LEAVE THEM when a store-edit spec is given.

    A CORRECTING ACT MUST NOT BE BLOCKED BY THE THING IT CORRECTS. The first wiring of this check
    ran against the tree as it stands, and the immediate consequence was that the landing which
    fixes the four impossible rows could not launch, because four impossible rows were present.
    That is the same self-reference shrink S4 removed for PREFLIGHT.json, and it makes a guard into
    an obstacle.

    So the bar is on the OUTPUT: given a store-edit spec, the declared edits are applied in memory
    first — through `apply_store_edits`, the one implementation, with every assertion it makes — and
    the check asks whether the act LEAVES an impossible row. An act that corrects them passes; an
    act that introduces or preserves one does not, which is the property actually worth having.
    """
    with open(os.path.join(root, STORE), encoding='utf-8') as f:
        text = f.read()
    if spec_path:
        with open(spec_path, encoding='utf-8') as f:
            spec = json.load(f)
        edits = list((spec.get('edit') or {}).get('store') or ())
        if edits:
            sys.path.insert(0, root)
            from tools.landing.steps import apply_store_edits
            text, _applied = apply_store_edits(text, edits)
    d = json.loads(text)
    return d['players'] if isinstance(d, dict) and 'players' in d else d


def offenders(root, spec_path=None):
    out = []
    for r in rows(root, spec_path):
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
    argv = list(argv or sys.argv)
    root, spec_path = ROOT, None
    if '--root' in argv:
        root = os.path.abspath(argv[argv.index('--root') + 1])
    if '--spec' in argv:
        spec_path = os.path.abspath(argv[argv.index('--spec') + 1])
    bad = offenders(root, spec_path)
    print('STORE SANITY — a season cannot contain more than %d games (23 H&A games + 5 finals)%s'
          % (SEASON_GAMES_CEILING,
             '\n  (judged on the tree THIS ACT WOULD LEAVE: its declared store edits applied first)'
             if spec_path else ''))
    if not bad:
        n = sum(len(r.get('scoring') or []) for r in rows(root, spec_path))
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
