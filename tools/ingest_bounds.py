#!/usr/bin/env python3
"""tools/ingest_bounds.py — the automatic limits on a week of scores. Runs as a landing gate.

    python3 tools/ingest_bounds.py scores/resolved/2026_FW3.json

A week of football moves the players who PLAYED. It also moves everyone else a little, because the
engine re-fits its calibration to the whole population at load — at FW2 the non-players moved by a
median of 0.157% (1 point), 90th percentile 0.448%, largest 16 points. That ripple is the model
re-calibrating and it is fine.

What is NOT fine is the failure this lane has actually had: something other than football moving the
board — the calendar stretching from 1.00 to 0.83 in the first finals attempt repriced every completed
season by about 17%. That shows up as the NON-PLAYERS moving, systematically and by percentages. So
this checks the non-players, against limits about ten times wider than anything a real week produced:

    median |move| of the non-players   <= 1.5%       (FW2: 0.157%)
    any single non-player              <= 60 points or 10%, whichever is larger   (FW2: 16 points)

and one sanity check on the players who did play — the edit reached the board:

    at least half of them moved

It compares the board being landed (the working tree) with the board it replaces (HEAD, which is
the inputs commit — the board is untouched there). Exit 0 = within limits; 1 = refuse the week.
"""
import io
import json
import os
import statistics
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = 'data/rl_build/rl_app_data.json'
MEDIAN_LIMIT_PCT = 1.5
SINGLE_LIMIT_PTS = 60
SINGLE_LIMIT_PCT = 10.0


def board_values(raw):
    d = json.loads(raw)
    return {p['key']: p['v'] for p in d['active']}, {p['key']: p.get('name') for p in d['active']}


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.strip().splitlines()[2].strip())
    played = {p['key'] for p in json.load(io.open(os.path.join(REPO, sys.argv[1]),
                                                   encoding='utf-8'))['players']}
    before_raw = subprocess.run(['git', 'show', 'HEAD:' + BOARD], cwd=REPO, capture_output=True,
                                check=True).stdout
    before, _ = board_values(before_raw)
    after, names = board_values(io.open(os.path.join(REPO, BOARD), 'rb').read())

    fails = []
    common = [k for k in after if k in before]
    others = [k for k in common if k not in played]
    pct = sorted(abs(after[k] - before[k]) / before[k] * 100 for k in others if before[k])
    med = statistics.median(pct) if pct else 0.0
    if med > MEDIAN_LIMIT_PCT:
        fails.append('the players who did NOT play moved by a median of %.2f%% (limit %.1f%%) — '
                     'something other than this week\'s football moved the board'
                     % (med, MEDIAN_LIMIT_PCT))
    big = []
    for k in others:
        d = after[k] - before[k]
        if abs(d) > max(SINGLE_LIMIT_PTS, before[k] * SINGLE_LIMIT_PCT / 100.0):
            big.append('%s %d -> %d (%+d)' % (names.get(k) or k, before[k], after[k], d))
    if big:
        fails.append('%d player(s) who did not play moved beyond the single-player limit: %s'
                     % (len(big), '; '.join(big[:8])))
    on_board = [k for k in played if k in after and k in before]
    moved = [k for k in on_board if after[k] != before[k]]
    if on_board and len(moved) * 2 < len(on_board):
        fails.append('only %d of the %d players who played moved — the edit did not reach the board'
                     % (len(moved), len(on_board)))

    print('INGEST BOUNDS — %d played (%d moved), %d did not play' % (len(on_board), len(moved),
                                                                     len(others)))
    print('  non-players: median |move| %.3f%%, largest %s'
          % (med, max((abs(after[k] - before[k]) for k in others), default=0)))
    if fails:
        print('  REFUSED:\n    ' + '\n    '.join(fails))
        return 1
    print('  WITHIN LIMITS')
    return 0


if __name__ == '__main__':
    sys.exit(main())
