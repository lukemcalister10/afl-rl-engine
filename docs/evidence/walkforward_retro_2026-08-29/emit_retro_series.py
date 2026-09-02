#!/usr/bin/env python3
"""EMIT THE RETROSPECTIVE SERIES into ui/data/movers.js.

Reads the banked values_rN.json (one per round, priced by retro_walkforward.py through the real
rl_export path under the LIVE engine) and appends, for each round R in 14..25 (25 = FINALS WEEK 1, named not numbered):

  * a POINT  {id: 'retro-rN', label: 'R<N> · current model', kind: 'retro', after_round: N}
  * a byPoint entry {v, rank, pos_rank} on every player the round priced

rank / pos_rank are computed HERE the same way the bundle's own points carry them (value desc over
the priced population; pos_rank within posCode), so the from/to comparator, the sorts and the views
all work on a retro point exactly as they do on a stored one — no new code path in the app.

WHAT THIS IS NOT: the stored as-they-were points are untouched. A retro point is the CURRENT model's
answer for that round's football; a stored point is what the board actually said that week. Mixing
one of each in a comparison is a cross-world read, and the app labels it (movers.js RETRO_BANNER).

Idempotent: re-running replaces any existing retro points/entries rather than duplicating them.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BUNDLE = os.path.join(REPO, 'ui', 'data', 'movers.js')
ROUNDS = list(range(14, 26))   # 25 = FINALS WEEK 1
FINALS_NAMES = {25: 'Finals Week 1', 26: 'Finals Week 2', 27: 'Semi-Final',
                28: 'Preliminary Final', 29: 'Grand Final'}   # round_movers.FINALS_WEEK_NAMES


def load_bundle():
    src = open(BUNDLE).read()
    i = src.index('{', src.index('__MATCHDAY_MOVERS__'))
    depth = 0
    for j, ch in enumerate(src[i:], i):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
    return src[:i], json.loads(src[i:end]), src[end:]


def main():
    banked = {}
    for R in ROUNDS:
        p = os.path.join(HERE, 'values_r%d.json' % R)
        if not os.path.exists(p):
            raise SystemExit('HALT: values_r%d.json not banked — emit only on the complete set '
                             '(a partial series would render as if rounds were missing).' % R)
        banked[R] = json.load(open(p))

    head, mv, tail = load_bundle()
    vals = mv['values']

    # idempotence: strip any prior retro emission first
    mv['points'] = [p for p in mv['points'] if p.get('kind') != 'retro']
    for rec in vals.values():
        for k in [k for k in rec['byPoint'] if str(k).startswith('retro-r')]:
            del rec['byPoint'][k]

    covered = 0
    for R in ROUNDS:
        pid = 'retro-r%d' % R
        vmap = banked[R]['values']
        # rank over the priced population, value desc; ties break on key for determinism
        order = sorted(vmap.items(), key=lambda kv: (-kv[1], kv[0]))
        rank = {k: i + 1 for i, (k, _) in enumerate(order)}
        # positional rank within posCode, read off the bundle's own player records
        bypos = {}
        for k, v in order:
            rec = vals.get(k)
            if not rec:
                continue
            bypos.setdefault(rec.get('posCode') or '—', []).append(k)
        pos_rank = {}
        for _pc, keys in bypos.items():
            for i, k in enumerate(keys):
                pos_rank[k] = i + 1
        n = 0
        for k, v in vmap.items():
            rec = vals.get(k)
            if not rec:
                continue                      # priced but not on the current board view
            rec['byPoint'][pid] = {'v': int(v), 'rank': rank[k], 'pos_rank': pos_rank.get(k)}
            n += 1
        covered = max(covered, n)
        mv['points'].append({
            # A FINALS WEEK IS NAMED, NOT NUMBERED. ui/app/movers.js prefers a retro point's own
            # label, and "R25 · current model" would be a round that does not exist on any fixture.
            'id': pid, 'label': (('%s · current model' % FINALS_NAMES[R]) if R in FINALS_NAMES
                                 else 'R%d · current model' % R), 'kind': 'retro',
            'after_round': R, 'board': banked[R]['board_md5'],
        })
        print('%-10s %4d players  board %s' % (pid, n, banked[R]['board_md5'][:8]))

    mv['_retro_doc'] = ('Walk-forward retrospective (owner ask 2026-08-29, extended to the finals 2026-09-02): '
                        'each round R14-R24 and FINALS WEEK 1 re-priced under the LIVE engine from the current corrected store with the '
                        '2026 season truncated to as-at-R (scores from the weekly reports of '
                        'record) and the season clock set as-of R. The kind:"round" points remain '
                        'the boards as they actually stood. A comparison mixing a retro point with '
                        'a stored point is a cross-world read and the app says so.')
    open(BUNDLE, 'w').write(head + json.dumps(mv, separators=(',', ':')) + tail)
    print('emitted %d retro points covering up to %d players -> %s'
          % (len(ROUNDS), covered, os.path.relpath(BUNDLE, REPO)))


if __name__ == '__main__':
    main()
