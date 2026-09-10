#!/usr/bin/env python3
"""BANK THE NEWEST WEEK'S RETRO POINT FROM THE BOARD THAT WAS JUST LANDED — no engine, no pricing.

WHY THIS IS AN IDENTITY AND NOT A SHORTCUT. The retrospective prices round R from a store truncated
by the games played AFTER R. For the NEWEST applied week that truncation removes nothing, so the
truncated store IS the live store and pricing it under the live engine IS the live board. That is
not an approximation to be checked later; it is the same claim the retro pass asserts as its
CONTROL, and the claim was measured once already — FW1, 2026-09-02, r25 vs the live board: 0 diffs,
0 missing, over 804 rows.

So the newest week's bank is a copy of the board, and a 35-minute engine load to re-derive a number
we already hold would be machine time spent proving an identity. The owner's words, 2026-09-09:
"We don't need to reprice previous rounds under the same model here... It's literally just adding a
week, editing the players who played, and creating a single movers list entry."

WHAT THIS DOES NOT DO. It does not touch rounds 14..R-1. Their football has not changed — each was
priced from a store that never contained this week's game in the first place — so they stay exactly
as banked. They carry a hairline of staleness from the load-time calibration refit (FW2 measured it
at a median of 0.157% on players who did not play), which is why `pass_retro_series.py` still
exists: run it when that hairline is worth 35 minutes, not every week.

    python3 docs/evidence/walkforward_retro_2026-08-29/bank_from_landed_board.py <feed_round>
"""
import hashlib
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
BOARD = os.path.join(REPO, 'data', 'rl_build', 'rl_app_data.json')
STORE = os.path.join(REPO, 'engine', 'rl_after', 'rl_model_data.json')
HOME_AND_AWAY_ROUNDS = 24


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__.strip().splitlines()[-1].strip())
    R = int(sys.argv[1])
    if R <= HOME_AND_AWAY_ROUNDS:
        raise SystemExit('HALT: r%d is a home-and-away round. Only a FINALS feed round may be banked '
                         'this way — an in-season round has football after it, so its truncation is '
                         'not a no-op and its values are NOT the live board.' % R)
    out = os.path.join(HERE, 'values_r%d.json' % R)
    # RE-BANKING IS ALLOWED HERE, AND ONLY HERE. A finals feed round's bank IS the live board, so
    # "already banked" and "banked from a different board" are the same question with one answer:
    # take the board in front of you. It matters because an ABORTED flight leaves its bank behind —
    # values_r*.json is evidence, not a landing carrier, so the abort ladder does not restore it —
    # and a stale bank from a board that was rolled back is the one thing that must not survive.
    prev_bank = None
    if os.path.exists(out):
        prev_bank = json.load(io.open(out, encoding='utf-8'))
    prev = os.path.join(HERE, 'values_r%d.json' % (R - 1))
    if not os.path.exists(prev):
        raise SystemExit('HALT: r%d is not banked. The series must be contiguous — banking r%d on a '
                         'hole would render as if a week went unplayed.' % (R - 1, R))

    board = json.load(io.open(BOARD, encoding='utf-8'))
    values = {p['key']: p['v'] for p in board['active']}
    store_md5 = hashlib.md5(io.open(STORE, 'rb').read()).hexdigest()

    rec = {
        'round': R, 'n': len(values), 'store_md5': store_md5,
        'calendar_progress': 1.0, 'exposure_pace': None,
        'board_md5': 'landed-board/%s' % store_md5[:8],
        '_provenance': (
            'BANKED FROM THE LANDED BOARD, not re-priced. For the newest applied week the '
            'retrospective truncation removes nothing, so the truncated store is the live store and '
            'its pricing is the live board — the identity pass_retro_series.py asserts as its '
            'control, measured at FW1 (r25 vs live: 0 diffs over 804 rows). calendar_progress is '
            '1.0 because the calendar reaches 1.00 at round %d and HOLDS through the finals (owner, '
            '2026-09-02); exposure_pace is null because it is not read back and inventing a number '
            'nobody measured would be worse than saying so.' % HOME_AND_AWAY_ROUNDS),
        'values': values,
    }
    json.dump(rec, io.open(out, 'w', encoding='utf-8'), indent=1)
    if prev_bank is None:
        print('banked r%d from the landed board: %d rows, store %s -> %s'
              % (R, len(values), store_md5[:8], os.path.relpath(out, REPO)))
    else:
        moved = sum(1 for k, v in values.items() if (prev_bank.get('values') or {}).get(k) != v)
        print('re-banked r%d from the landed board: %d rows, store %s -> %s (previous bank was '
              'store %s; %d value(s) differ — a bank left behind by an aborted flight is replaced, '
              'never merged)'
              % (R, len(values), store_md5[:8], os.path.relpath(out, REPO),
                 str(prev_bank.get('store_md5'))[:8], moved))


if __name__ == '__main__':
    main()
